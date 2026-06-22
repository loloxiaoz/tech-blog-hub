---
title: "AI 网络威胁全景图：Anthropic 一年追踪报告"
org: "Anthropic"
date: 2026-06-03
source_url: "https://www.anthropic.com/research/mapping-ai-cyber-threats"
tags: ["Agent", "Claude Code", "Harness工程"]
summary: "研究期间（2025/03—2026/03），67.3%（560/832）的恶意账号使用 AI 编写恶意软件，这是最普遍的用途。但更值得警惕的是后渗透阶段的 AI 化：6.5%（54/832）的账号用 AI 辅助横向移动（lateral movement），账号发现（account"
summary_zh: "研究期间（2025/03—2026/03），67.3%（560/832）的恶意账号使用 AI 编写恶意软件，这是最普遍的用途。但更值得警惕的是后渗透阶段的 AI 化：6.5%（54/832）的账号用 AI 辅助横向移动（lateral movement），账号发现（account"
summary_en: ""
---



# AI 网络威胁全景图：Anthropic 一年追踪报告
# What We Learned Mapping AI-Enabled Cyber Threats

## 核心观点

**1. AI 使攻击者向攻击链后段深度转移**

研究期间（2025/03—2026/03），67.3%（560/832）的恶意账号使用 AI 编写恶意软件，这是最普遍的用途。但更值得警惕的是后渗透阶段的 AI 化：6.5%（54/832）的账号用 AI 辅助横向移动（lateral movement），账号发现（account discovery）的 AI 使用率上升 8.9%，而用于初始访问的钓鱼攻击（phishing）则下降 8.6%。后渗透技术过去需要高级技能，AI 正在将这些能力下放给低技能攻击者。

**2. 威胁等级快速升级，传统评级指标失效**

第一个六个月内，33% 的攻击者被评为中高风险；第二个六个月这一比例跃升至 56%（约 1.7 倍）。传统上用于衡量威胁等级的两个信号——使用技术数量、使用的工具/界面类型——都已失去区分度：最低技能攻击者平均使用约 16 种技术，最高技能者约 20 种，差距微乎其微；使用 Claude Code、API 还是聊天界面也与风险等级无关。

**3. 真正的区分因素：自主攻击编排架构**

高风险攻击者的核心特征不是使用更多技术，而是将 AI 集中应用于操作复杂度高的环节（账号发现、横向移动、权限提升），更重要的是：他们构建了允许模型串联攻击链各阶段、以最少人工干预自主执行的编排架构（agentic orchestration scaffolding）。这是目前最可靠的区分信号，但随着更多攻击者向高风险转移，这一信号正在被稀释。

**4. MITRE ATT&CK 框架存在根本性盲区**

2025 年 11 月 Anthropic 打断了一起国家级网络间谍行动：攻击者操控 Claude Code 充当自主 Agent，以极少人工干预执行命令、漏洞利用、凭证窃取和战术决策。将该行动映射至 MITRE ATT&CK，仅得出 13 个战术/30 个技术——与数据集中许多中等风险攻击者相当，但 Anthropic 内部风险评分为 100（满分）。ATT&CK 框架目前没有任何 ID 覆盖 AI 自主编排行为，Anthropic 正与 MITRE 合作推动框架演化。

**5. 防御优先承诺与 Project Glasswing**

Anthropic 已在高能力模型上部署专项网络安全防护，检测和阻断被识别出的恶意行为模式（恶意软件开发、大规模数据外泄等）。通过 Project Glasswing 和与 Verizon DBIR 的合作，承诺持续向防御方共享情报，优先将最强工具交到防御方手中。

## 关键术语

- **后渗透（Post-Compromise）** — 攻击者进入目标系统后开展的活动（横向移动、账号发现、权限提升、数据外泄），与获取初始访问的前期阶段相对；AI 正将这些高技能操作平民化
- **横向移动（Lateral Movement）** — 在已入侵的网络内部横向扩散，访问更多系统和账户的技术，原本需要深度系统知识
- **自主攻击编排（Agentic Attack Orchestration）** — 攻击者围绕 AI 模型构建的脚手架架构，使模型能够自主串联攻击链多个阶段并实时决策，最小化人工干预
- **MITRE ATT&CK** — 网络攻击战术与技术权威分类框架，被安全社区广泛用于威胁评估；当前版本缺乏对 AI 自主编排行为的覆盖
- **风险评分体系** — Anthropic 内部评估攻击者威胁等级的方法论，侧重 AI 使用位置、编排复杂度，而非技术数量
- **Project Glasswing** — Anthropic 网络安全情报项目，收集 AI 被滥用的真实案例，向防御方共享威胁情报
- **爆炸半径（Blast Radius）** — 攻击或 Agent 失控时影响扩散的范围；自主攻击编排架构大幅扩大了单次攻击的爆炸半径

## 相关概念

- concepts/agent-containment — AI Agent 爆炸半径控制；本文提供了自主攻击编排对 containment 挑战的真实攻击侧案例
- concepts/agentic-systems — 自主 Agent 系统设计；攻击者正将 agentic 架构应用于进攻侧
- concepts/multi-agent-systems — 多 Agent 编排；攻击者的自主编排架构与防御侧 multi-agent 设计形成镜像
- concepts/eval-awareness — 模型识别测试环境的能力边界；与模型被操控执行恶意操作的意识边界问题相关

## 相关实体

- entities/anthropic — 报告发布方，Frontier Red Team 主导分析，与 MITRE 合作推动框架更新
- entities/claude-code — 被国家级攻击者操控为自主攻击 Agent 的工具（2025 年 11 月事件）
