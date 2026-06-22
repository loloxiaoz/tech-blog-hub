---
title: "Best Practices for Claude Code（Anthropic 官方指南）"
org: "Anthropic"
date: 2026-06-06
source_url: "https://www.anthropic.com/engineering/claude-code-best-practices"
tags: ["Agent", "Claude Code"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Best Practices for Claude Code（Anthropic 官方指南）

## 核心观点

**上下文窗口是第一约束，所有最佳实践都服务于此。** LLM 性能随上下文填充而下降——Claude 会开始"遗忘"早期指令、犯更多错误。上下文窗口是最重要的资源，不是功能之一，而是整篇指南的底层逻辑。/clear、compaction、subagent 隔离、CLAUDE.md 精简，这些操作的底层逻辑都是同一件事：保护上下文质量。

**给 Claude 一个可以自己运行的验证机制，才能走开。** 没有验证闭环，"看起来完成"就是唯一信号，每次错误都等你来发现。验证机制可以是：测试套件、构建退出码、linter、脚本对比输出与 fixture、浏览器截图与设计稿对比。有了 pass/fail 信号，循环就能自我闭合——这是"看着跑"和"放心走开"的分界线。

**探索→计划→实现→提交四阶段工作流。** Plan mode 将研究与实现分离，避免 Claude 在错误问题上写出正确代码。具体步骤：①进入 plan mode 读文件不修改（Explore）；②要求 Claude 生成详细实现计划（Plan）；③退出 plan mode 开始编码并验证（Implement）；④提交并创建 PR（Commit）。任务清晰且改动小时跳过 plan mode；任务模糊时必须先探索。

**Hooks 是确定性保证，CLAUDE.md 是建议性指导。** 两者都是 Harness 配置，但性质不同：CLAUDE.md 指令由模型读取后尽力遵守（建议性），Hooks 由运行时强制执行（每次必然发生）。需要"零例外"的事项——如格式化、测试运行、lint——必须用 Hooks 实现，而不是写进 CLAUDE.md 祈祷 Claude 记住。

**并行化和 fan-out 是单 Claude 的乘数。** 通过 `claude -p` 非交互模式（CI/scripts）、多 worktrees 并行会话、subagent 隔离调查，单个工程师产出可数倍放大。adversarial review 模式（让新鲜上下文的 subagent 审查 diff）是廉价质量门。

## 关键术语

- **Plan mode（计划模式）**：Claude Code 内置模式，仅读文件和回答问题，不执行修改。用于探索和规划阶段，防止过早编码。
- **Verification loop（验证闭环）**：提供给 Claude 一个可自主运行的 pass/fail 检验机制（测试/构建/截图对比），使 Agent 能在无人监督时自行校正结果。
- **Context compaction（上下文压缩）**：当上下文填充时，Claude 自动（auto compaction）或手动（`/compact <指令>`）将关键信息提炼摘要，释放窗口空间。
- **Checkpoint（检查点）**：每次发送 prompt 自动创建的还原点，可通过 `/rewind` 或 `Esc+Esc` 恢复对话状态和代码状态。
- **Subagent（子代理）**：在独立上下文中执行隔离任务的 Claude 实例。用于"调查类"任务，避免污染主对话上下文；也用于 adversarial review（对抗性审查）。
- **Adversarial review（对抗性审查）**：任务完成后，启动一个全新上下文的 subagent 审查 diff，报告遗漏的边缘情况和实现缺口。
- **Non-interactive mode（非交互模式）**：`claude -p "prompt"` 形式，在 CI、pre-commit hooks、脚本中运行。可加 `--output-format stream-json --verbose` 获取流式 JSON。
- **Fan-out pattern（扇出模式）**：循环调用 `claude -p` 对每个文件/任务执行并行操作，使用 `--allowedTools` 限制权限范围。
- **CLAUDE.md**：Claude 每次对话开始时读取的特殊文件。包含 Bash 命令、代码风格规则、工作流约束。精简原则：去掉这行 Claude 会犯错吗？不会就删掉。
- **Hooks**：事件驱动的确定性自动化，与 CLAUDE.md 建议性指令形成互补。适用于"必须每次发生、零例外"的动作。

## CLAUDE.md 写作原则

| 应该包含 | 不应包含 |
|---------|---------|
| Claude 无法猜到的 Bash 命令 | Claude 读代码能推断出的信息 |
| 与默认值不同的代码风格规则 | Claude 已知的语言标准规范 |
| 测试指令和首选测试运行器 | 详细 API 文档（链接即可） |
| 仓库礼仪（分支命名、PR 规范）| 频繁变化的信息 |
| 项目特定的架构决策 | 长篇解释或教程 |
| 开发环境怪癖（必要环境变量）| 逐文件的代码库描述 |
| 常见坑点和非显而易见的行为 | 不言而喻的惯例（如"写干净的代码"）|

## 五种常见失败模式

| 失败模式 | 症状 | 修复方法 |
|---------|------|---------|
| **kitchen sink session（大杂烩会话）** | 上下文充满无关信息 | 任务切换时 `/clear` |
| **correcting over and over（反复纠正）** | 上下文被失败尝试污染 | 连续纠错两次后 `/clear` 并重写更精确的初始 prompt |
| **over-specified CLAUDE.md（过度规范）** | 重要规则淹没在噪音里 | 无情删减 |
| **trust-then-verify gap（信任后验证缺口）** | 看起来可用但不处理边缘情况 | 始终提供验证机制 |
| **infinite exploration（无限探索）** | Claude 读取数百文件填满上下文 | 用 subagent 隔离调查，或明确限定探索范围 |

## 相关概念

- concepts/context-window — 上下文窗口：Token 预算四类消耗者，KV Cache 成本，管理操作集
- concepts/harness-engineering — Harness Engineering：AI 工程第三阶段，模型外的工程能力
- concepts/agent-skills — Agent Skills：可复用专业知识包，SKILL.md 结构，渐进式披露
- concepts/agentic-systems — Agentic Systems：Workflow vs Agent 区分，adversarial review 模式
- concepts/aci — ACI：工具设计原则，防呆设计
- concepts/agent-evaluation — Agent 评测：外部质量闭环，验证机制设计
- concepts/workflow-patterns — 五种 Workflow 模式

## 相关实体

- entities/anthropic — Anthropic：本指南发布方
- entities/claude-code — Claude Code：本指南的主题工具，CLI 命令体系
- entities/mcp — MCP：工具连通性协议，`claude mcp add` 连接外部工具
