---
title: "Beyond permission prompts: making Claude Code more secure and autonomous"
org: "Anthropic"
date: 2025-10-20
source_url: "https://www.anthropic.com/engineering/claude-code-sandboxing"
tags: ["Agent", "MCP", "Claude Code"]
summary: "Claude Code 原本运行在权限审批模型下：默认只读，修改或执行命令均需用户逐一批准。频繁点击\"批准\"不仅拖慢开发节奏，还会引发 approval fatigue——用户逐渐不再仔细审查就点过去，反而使安全性下降。沙箱的解法是反转思路：预先定义一个安全边界，边界内 Cl"
summary_zh: "Claude Code 原本运行在权限审批模型下：默认只读，修改或执行命令均需用户逐一批准。频繁点击\"批准\"不仅拖慢开发节奏，还会引发 approval fatigue——用户逐渐不再仔细审查就点过去，反而使安全性下降。沙箱的解法是反转思路：预先定义一个安全边界，边界内 Cl"
summary_en: ""
---



# Beyond permission prompts: making Claude Code more secure and autonomous

## 核心观点

**1. 沙箱以预定义边界取代逐次审批，同时提升自主性与安全性**

Claude Code 原本运行在权限审批模型下：默认只读，修改或执行命令均需用户逐一批准。频繁点击"批准"不仅拖慢开发节奏，还会引发 approval fatigue——用户逐渐不再仔细审查就点过去，反而使安全性下降。沙箱的解法是反转思路：预先定义一个安全边界，边界内 Claude 可自由行动、无需提示，边界外立即通知用户。Anthropic 内部测试数据：沙箱将权限提示减少 **84%**。

**2. 文件系统隔离与网络隔离缺一不可**

有效沙箱必须同时具备两层防护：
- **文件系统隔离**：Claude 只能读写当前工作目录，无法修改系统文件或其他敏感路径。
- **网络隔离**：Claude 只能通过外部代理服务访问白名单域名，无法直连任意服务器。

两层互为补充：仅有网络隔离，被攻陷的 Agent 仍可读取并通过合法渠道泄露 SSH Key 等文件；仅有文件系统隔离，Agent 可通过网络逃逸并获取网络访问权。两者组合才能让 prompt injection 攻击完全被隔离。

**3. 沙箱基于 OS 级原语实现，覆盖所有子进程**

实现层基于 **Linux bubblewrap** 和 **macOS Seatbelt**（操作系统沙箱原语），约束不仅作用于 Claude Code 的直接调用，还覆盖其生成的所有脚本、程序和子进程。网络层通过 Unix domain socket 连接到沙箱外部的代理服务器，由代理强制执行域白名单并处理新域名的用户确认。两项均可独立配置（允许/禁止特定路径或域名）。

**4. Claude Code Web 版通过云端沙箱确保凭证安全**

Web 版在云端为每个会话启动独立沙箱。关键设计原则：敏感凭证（git credentials、代码签名密钥）**永远不进入沙箱**。Git 操作通过外部自定义代理服务处理：沙箱内 git client 用限定权限的临时凭证认证到代理，代理验证操作内容（如仅允许推送到指定分支），再附上真实 token 发往 GitHub。即使沙箱内代码被攻破，攻击者无法获取真实 git 凭证。

**5. 沙箱运行时已开源，鼓励 Agent 生态采用**

Anthropic 将沙箱运行时开源（[anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime)），可用于沙箱化任意进程、Agent 和 MCP Server，无需启动和管理容器。Anthropic 明确呼吁其他 Agent 团队采用，视其为提升 Agent 整体安全姿态的通用基础设施。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Sandboxing（沙箱）** | 为进程预定义资源访问边界，越界行为被 OS 强制阻止或通知用户，替代逐次权限审批 |
| **Filesystem isolation（文件系统隔离）** | 限制 Agent 只能读写指定目录，阻止修改边界外文件（尤其是系统文件和敏感配置） |
| **Network isolation（网络隔离）** | 通过代理强制执行域白名单，阻止 Agent 连接未授权服务器，防止数据外泄和恶意下载 |
| **Approval fatigue（审批疲劳）** | 频繁权限提示导致用户习惯性点过，不再仔细审查，反而降低安全性 |
| **Prompt injection（提示注入）** | 攻击者通过恶意内容控制 Agent 行为，沙箱确保即使注入成功也无法突破边界 |
| **Linux bubblewrap** | Linux 用户空间沙箱工具，用于文件系统命名空间隔离 |
| **macOS Seatbelt** | macOS 系统级沙箱机制，用于限制进程的资源访问 |
| **Unix domain socket 代理** | 沙箱内网络出口，所有外部请求必须经过此代理服务器，由代理强制执行网络策略 |
| **Scoped credential（限域凭证）** | Claude Code Web 版中沙箱内 git 使用的临时限权凭证，不含真实认证 token |
| **sandbox runtime** | Anthropic 开源的沙箱运行时，可沙箱化任意进程/Agent/MCP Server，无需容器开销 |

## 相关概念

- concepts/agent-sandboxing — 本文介绍的核心技术：Agent 沙箱隔离
- concepts/harness-engineering — 沙箱是 Harness 约束护栏层的具体实现
- concepts/agentic-systems — Agent 自主性与安全性权衡的系统设计视角
- concepts/aci — Agent-Computer Interface，沙箱工具是 ACI 的安全边界层

## 相关实体

- entities/claude-code — 本文的核心产品，沙箱 Bash 工具和 Web 版的实现平台
- entities/anthropic — 开发方，同时开源了 sandbox-runtime
- entities/mcp — sandbox runtime 也支持对 MCP Server 进行沙箱化
