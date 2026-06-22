---
title: "How we contain Claude across products"
org: "Anthropic"
date: 2026-05-25
source_url: "https://www.anthropic.com/engineering/how-we-contain-claude"
tags: ["Agent", "Claude Code"]
summary: "人类监督（Human-in-the-loop）是概率性防御——遥测数据显示用户批准了约 93% 的权限提示，批准越多注意力越低，形成\"批准疲劳\"。环境隔离（沙箱/VM/出口控制）是确定性防御，限制的是 Agent 能做什么，而非它倾向做什么。两者需要互补，不能互相替代。"
summary_zh: "人类监督（Human-in-the-loop）是概率性防御——遥测数据显示用户批准了约 93% 的权限提示，批准越多注意力越低，形成\"批准疲劳\"。环境隔离（沙箱/VM/出口控制）是确定性防御，限制的是 Agent 能做什么，而非它倾向做什么。两者需要互补，不能互相替代。"
summary_en: ""
---



# How we contain Claude across products

## 核心观点

**1. 两种防御范式：HITL 与环境隔离**

人类监督（Human-in-the-loop）是概率性防御——遥测数据显示用户批准了约 93% 的权限提示，批准越多注意力越低，形成"批准疲劳"。环境隔离（沙箱/VM/出口控制）是确定性防御，限制的是 Agent 能做什么，而非它倾向做什么。两者需要互补，不能互相替代。

**2. 三类风险，三层防御**

风险分类：用户滥用（主动/无意）、模型失控（能力越强越擅长绕过未明文禁止的限制）、外部攻击（提示注入、supply chain）。防御对应三层：运行环境（沙箱/VM/文件边界/出口控制）、模型层（system prompt/classifier/training，Claude Opus 4.7 对单次攻击的成功率约 0.1%）、外部内容（工具输出同样是攻击面，审计 connector ≠ 审计数据）。

**3. 三种隔离模式匹配三种用户**

| 产品 | 模式 | 用户 | 爆炸半径 |
|------|------|------|---------|
| claude.ai | gVisor 临时容器（服务端） | 所有用户 | 服务端容器 |
| Claude Code | OS 级沙箱 + HITL | 开发者（能读懂 bash） | 本地工作区 |
| Claude Cowork | 完整 VM | 非技术知识工作者 | 挂载工作区 |

隔离强度必须与用户监督能力匹配：过度摩擦伤害专家，过度信任伤害非技术用户。

**4. 自建组件是最薄弱的环节**

成熟原语（gVisor、seccomp、hypervisor）经受多年对抗性强化，全部可靠。两次最严重安全事故——直接提示注入泄露 AWS 凭证（Claude Code）、通过 api.anthropic.com 白名单外泄文件（Claude Cowork）——都出在 Anthropic 自行构建的代理/allowlist 上。自建代码应像来自互联网的任意请求一样对待。

**5. 新兴威胁正在改变攻击面**

- **持久记忆投毒**：CLAUDE.md、product memory、agent 状态目录跨 session 持久化，注入载荷每次启动重新加载
- **多 Agent 信任升级**：sub-agent 输出被视为高可信，成为新的注入向量
- **Agent 身份**：Agent 应持有独立主体身份（可独立撤销的 scoped token）还是继承用户权限？答案可能是两者混合

## 关键术语

- **Blast Radius（爆炸半径）**：Agent 一次失控行为理论上能造成的最大破坏范围，是 Agent 部署的核心风险度量指标
- **Containment（隔离/收容）**：通过环境约束限制 Agent 能访问什么，而非监督它做了什么；是确定性防御的主体
- **Approval Fatigue（批准疲劳）**：用户因频繁看到权限提示而降低审查质量，93% 批准率说明 HITL 在大量使用场景下效果衰减
- **Ephemeral Container（临时容器）**：每 session 独立、用完销毁的 gVisor 容器，claude.ai 代码执行的隔离方式，爆炸半径最小
- **Egress Control（出口控制）**：限制 Agent 能向外发送数据的目标，是防数据外泄的关键环境层手段；allowlist 应视为能力授权而非目标过滤
- **Prompt Injection（提示注入）**：通过工具输出、文件内容、外部数据等向模型上下文注入恶意指令；直接注入（经用户输入）时模型层无法检测异常
- **HITL Sandbox（人工监督沙箱）**：允许文件读写但限制网络，配合人工审批写/bash/网络操作；适合具备技术判断力的用户
- **Sealed VM（密封 VM）**：完整虚拟机，Agent 执行环境与宿主完全隔离，无外部进程持有"逃脱钥匙"；适合无法判断 bash 命令的用户
- **Trust Escalation（信任升级）**：多 Agent 系统中子 Agent 输出被错误赋予高于工具输出的信任级别，引入新注入向量
- **Persistent Memory Poisoning（持久记忆投毒）**：将恶意指令注入跨 session 持久化的 Agent 状态（CLAUDE.md/product memory），实现类似 APT 的持久驻留

## 相关概念

- concepts/harness-engineering — 约束护栏层的工程实现：沙箱、VM、出口控制
- concepts/agentic-systems — Agent 能力增强与安全风险的双重增长关系
- concepts/agent-containment — 本文核心：爆炸半径控制方法论（待建）
- concepts/prompt-injection — 提示注入攻击分类与防御（待建）
- concepts/memory-systems — 持久记忆投毒威胁面
- concepts/mcp — MCP 服务的 remote vs local 信任差异

## 相关实体

- entities/anthropic — 本文作者团队，Glasswing 安全倡议发起方
- entities/claude-code — HITL 沙箱模式，OS 级沙箱，auto mode，直接提示注入事故
- entities/claude-cowork — 完整 VM 模式，api.anthropic.com 白名单外泄事故（待建）
