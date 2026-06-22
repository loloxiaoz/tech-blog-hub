---
title: "Scaling Managed Agents: Decoupling the brain from the hands"
org: "Anthropic"
date: 2026-04-08
source_url: "https://www.anthropic.com/engineering/managed-agents"
tags: ["Agent", "MCP", "多模态", "长上下文", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Scaling Managed Agents: Decoupling the brain from the hands

## 核心观点

**Harness 会随模型能力升级而过时，接口设计比实现更重要。** Harness 本质上编码了对"模型当前做不到什么"的假设。Claude Sonnet 4.5 时代为解决"context anxiety"（模型临近 context 上限时提前结束任务）而加入的 context reset 逻辑，在 Claude Opus 4.5 上成了死代码。Managed Agents 的设计哲学类比操作系统：就像 `read()` 命令对 1970 年代磁盘包和现代 SSD 一视同仁，接口保持稳定，实现自由替换。

**Brain/Hands/Session 三组件解耦是核心架构决策。** 初始设计将 session、harness、sandbox 全部放入一个容器——这制造了"宠物服务器"问题：容器故障即会话丢失，调试需要进入持有用户数据的容器。解耦后：harness（brain）以 `execute(name, input) → string` 调用 sandbox（hands），容器成为可随时替换的"牲口"；session log 独立于 harness 之外，harness 崩溃后通过 `wake(sessionId)` 从任意一点恢复。

**Session 是独立于 context window 的外部持久化上下文。** 长时任务超出 context window 时，传统的 compaction（摘要压缩）和 trimming（裁剪旧 token）会造成不可逆信息损失。Managed Agents 将 session 设计为 append-only 事件日志，harness 通过 `getEvents()` 按位置切片按需加载，同时可在传入 Claude context 前做任意转换（如提高 prompt cache 命中率）。关键分离：session 保证持久可查，context 管理策略留给 harness——因为我们无法预测未来模型需要什么样的 context 工程。

**安全边界需要结构性隔离，而非依赖权限收窄。** 耦合设计中，prompt injection 只需让 Claude 读取容器内环境变量即可获取所有凭证，进而创建不受限制的新会话。解耦后：Git token 在 sandbox 初始化时写入 git remote 配置，agent 代码调用 `push/pull` 时凭证对 agent 不可见；MCP OAuth token 存于独立 vault，Claude 调用 MCP 工具时通过 proxy 转发，proxy 以 session token 换取 vault 凭证，harness 和 sandbox 均无法接触真实凭证。

**解耦带来量化的扩展性与性能收益。** 解耦前每个 brain 都要等待容器初始化才能开始推理，即使会话根本不需要沙箱。解耦后，推理在 orchestration layer 拉取 session log 后立即开始，容器按需通过工具调用 `provision({resources})` 创建。结果：p50 TTFT 下降约 60%，p95 TTFT 下降超过 90%。水平扩展变为：增加无状态 harness 实例（many brains），按需连接任意执行环境（many hands）。

## 关键术语

| 术语 | 定义 |
|------|------|
| Managed Agents | Anthropic 平台上的托管 agent 服务，运行长时任务，通过稳定接口屏蔽 harness 实现细节 |
| Meta-harness | 对 harness 本身的虚拟化——不规定用哪种 harness，只规定 harness 与其他组件交互的接口 |
| Brain | Claude 模型及其 harness（调度逻辑），负责推理和决策 |
| Hands | Sandbox、工具、MCP server 等执行环境，接受 `execute(name, input) → string` 调用 |
| Session | Append-only 事件日志，独立于 context window，通过 `getEvents()` 按切片查询 |
| Pets vs Cattle | 基础设施类比：宠物（命名、手工维护、不可丢失）vs 牲口（可替换、故障直接换新） |
| TTFT (Time-to-first-token) | 会话接受任务到产生第一个 token 的延迟，是用户感知最明显的延迟指标 |
| Context anxiety | 模型感知到 context 窗口即将耗尽时提前结束任务的行为（已在较新模型中消失） |
| Credential vault | 独立于 sandbox 的凭证存储，harness 和 sandbox 均无法直接访问 |
| `execute(name, input) → string` | Brain 调用任意 hand 的统一接口，支持容器、MCP server、自定义工具等 |

## 相关概念

- concepts/harness-engineering — Managed Agents 是 harness engineering 的产品化形态，meta-harness 设计
- concepts/agentic-systems — many-brains/many-hands 扩展模式，stateless harness 水平扩展
- concepts/context-window — session 作为 context window 外部持久化的解决方案
- concepts/context-engineering — compaction/trimming 方法的局限性，session log 作为互补方案
- concepts/memory-systems — session log 作为外部记忆层
- concepts/managed-agents — 本文核心主题，待新建

## 相关实体

- entities/anthropic — 本文作者所在公司，Managed Agents 的构建者
- entities/claude-code — 被引用为优秀 harness 代表，Managed Agents 可兼容
- entities/mcp — 在安全架构中通过 proxy+vault 模式集成外部工具
