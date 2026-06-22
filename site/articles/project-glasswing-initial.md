---
title: "Project Glasswing: An initial update（项目蜻蜓：初步进展报告）"
org: "Anthropic"
date: 2026-05-22
source_url: "https://www.anthropic.com/news/project-glasswing-initial"
tags: ["Agent", "安全/对齐"]
summary: "Project Glasswing 联合约 50 家合作伙伴（Cloudflare、Mozilla、Cisco 等）使用 Claude Mythos Preview，在一个月内在全球最关键软件中发现超过 10,000 个高危或严重漏洞。Cloudflare 单独发现 2,000 "
summary_zh: "Project Glasswing 联合约 50 家合作伙伴（Cloudflare、Mozilla、Cisco 等）使用 Claude Mythos Preview，在一个月内在全球最关键软件中发现超过 10,000 个高危或严重漏洞。Cloudflare 单独发现 2,000 "
summary_en: ""
---



# Project Glasswing: An initial update（项目蜻蜓：初步进展报告）

## 核心观点

**1. 漏洞发现速率提升超 10 倍，合作伙伴一个月发现超万个高危漏洞**

Project Glasswing 联合约 50 家合作伙伴（Cloudflare、Mozilla、Cisco 等）使用 Claude Mythos Preview，在一个月内在全球最关键软件中发现超过 10,000 个高危或严重漏洞。Cloudflare 单独发现 2,000 个漏洞（400 个高危/严重），误报率优于人工测试；Mozilla Firefox 150 中发现 271 个漏洞，是 Opus 4.6 在 Firefox 148 中发现量的 10 倍以上。UK AISI 证实 Mythos Preview 是首个端到端完成两套完整网络攻击模拟的模型。

**2. 网安瓶颈已从"发现"转移到"修复"**

AI 大规模加速漏洞发现后，真正的瓶颈变成了人类验证、披露和修补漏洞的能力。开源项目维护者面临 AI 生成的大量低质量漏洞报告浪潮，处于严重过载状态——部分维护者甚至请求 Anthropic 放慢披露节奏。一个高危漏洞从发现到修补平均需要两周时间。这种"发现-修复不对称"是当前网安的核心挑战。

**3. 开源项目扫描：1000+ 项目，真正阳性率 90.6%**

Anthropic 扫描了超 1,000 个开源项目，Mythos Preview 估计发现 6,202 个高危/严重漏洞（共 23,019 个）。独立安全研究机构评估后真正阳性率为 90.6%，62.4% 被确认为高危/严重。典型案例：wolfSSL 证书伪造漏洞（CVE-2026-5194），可影响数十亿设备。已披露 530 个高危/严重漏洞，75 个已被修补。

**4. Mythos 级模型因防滥用能力不足暂不公开发布**

Mythos 级模型尚未向公众发布，核心原因是当前没有任何公司（包括 Anthropic）拥有足够强的防滥用保障。Project Glasswing 的战略逻辑是：在同等能力的模型被其他人无防护地发布之前，先帮助最关键的网络防御方建立非对称优势——即"偷跑窗口期的定向赋能"。

**5. 配套工具包：将内部工具开放给合规安全团队**

同步推出 Claude Security（企业级漏洞扫描公测版，Opus 4.7 驱动，三周修补 2100+ 漏洞）、Cyber Verification Program（安全专业人员受控访问通道）、以及完整 Harness 套件（Skills + 代码库映射 + 子 Agent 扫描 + 威胁建模工具）。

## 关键术语

- **Claude Mythos Preview** — Anthropic 尚未公开的最高能力模型，网安能力远超现有公开模型，能端到端完成多步骤网络攻击模拟
- **Project Glasswing** — Anthropic 主导的协作式软件安全计划，约 50 家关键基础设施合作伙伴
- **发现-修复不对称（Discovery-Remediation Asymmetry）** — AI 使漏洞发现成本趋近于零，但修复成本仍由人类承担，造成严重不平衡
- **协调漏洞披露（CVD）** — 行业惯例：发现后 90 天披露，有补丁则 45 天后披露，AI 时代面临流程再设计压力
- **Cyber Verification Program** — 允许合法安全研究者（渗透测试/红队）绕过部分防护的访问计划
- **ExploitBench / ExploitGym** — 量化 AI 模型漏洞利用能力的新一代学术基准
- **Claude Security** — Anthropic 面向企业的代码漏洞扫描工具（公测），底层 Opus 4.7
- **威胁建模工具（Threat Model Builder）** — 映射代码库潜在攻击目标并优先级排序的自动化工具
- **Glasswing Harness 套件** — 包含 Skills + 代码库扫描 Harness + 威胁建模工具的完整安全扫描工程套件

## 相关概念

- concepts/harness-engineering — Glasswing 安全扫描套件是 Harness Engineering 在网安垂直领域的典型实例
- concepts/agent-skills — Glasswing 发布套件包含合作伙伴共建共享的 Skills，印证可复用知识包定位
- concepts/agent-containment — Mythos 因防滥用能力不足不公开，是 agent-containment 在最高能力层面的政策体现
- concepts/multi-agent-systems — 扫描 Harness 采用子 Agent 并行扫描架构（映射代码库→子 Agent 扫描→汇总报告）
- concepts/eval-awareness — ExploitBench/ExploitGym 等新基准的出现与 Eval 感知问题相关，旨在量化真实网安能力

## 相关实体

- entities/anthropic — 项目主导方，负责 Mythos Preview 开发与 Project Glasswing 运营
- entities/claude-opus-4-6 — 与 Mythos Preview 形成能力对比基准（Mozilla Firefox 案例：10 倍漏洞发现量差距）
- entities/mcp — Glasswing Harness 套件依托 Claude Code / MCP 生态交付给合规客户
