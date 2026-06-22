---
title: "Expanding Project Glasswing（扩大 Project Glasswing）"
org: "Anthropic"
date: 2026-06-02
source_url: "https://www.anthropic.com/news/expanding-project-glasswing"
tags: []
summary: "Project Glasswing 初期 50 家合作伙伴已累计发现超过 10,000 个高危或严重安全漏洞。此次扩大至约 150 个新组织，总计 200+ 家，覆盖 15+ 个国家，新增电力、水务、医疗、通信、硬件等此前代表性不足的行业。大多数新合作伙伴是供应商型组织——其代码"
summary_zh: "Project Glasswing 初期 50 家合作伙伴已累计发现超过 10,000 个高危或严重安全漏洞。此次扩大至约 150 个新组织，总计 200+ 家，覆盖 15+ 个国家，新增电力、水务、医疗、通信、硬件等此前代表性不足的行业。大多数新合作伙伴是供应商型组织——其代码"
summary_en: ""
---



# Expanding Project Glasswing（扩大 Project Glasswing）

## 核心观点

**1. 从 50 家到 200+ 家：受控扩大关键基础设施覆盖**

Project Glasswing 初期 50 家合作伙伴已累计发现超过 10,000 个高危或严重安全漏洞。此次扩大至约 150 个新组织，总计 200+ 家，覆盖 15+ 个国家，新增电力、水务、医疗、通信、硬件等此前代表性不足的行业。大多数新合作伙伴是供应商型组织——其代码库被全球众多其他组织（含各国政府）依赖，一旦遭受攻击可能影响 1 亿+ 用户。

**2. 6-12 个月预警窗口：强力网络模型即将普及**

Anthropic 判断：未来 6-12 个月内，多家 AI 公司将拥有 Mythos 级网络能力模型，且可能不带防滥用保护措施发布。届时网络攻击将更频繁、形式更不可预测。Glasswing 的使命是在此之前帮助网络防御者建立操作规范、积累最佳实践，推动行业级的防御体系适应。

**3. 防御链条已延伸：从发现到修补**

AI 辅助网络安全覆盖完整防御链：漏洞扫描 → 补丁编写 → 上线预检 → 渗透测试 → 威胁检测响应 → 遗留代码迁移（内存安全语言）。当前瓶颈已从"发现漏洞"转移到"验证、披露、修补"。Anthropic 正与第三方讨论大规模扩展开源软件漏洞审查与修补，并整理漏洞披露报告最佳实践。

**4. 双重角色：能力普及 + 推动行业规范**

Anthropic 将自身定位为双重角色：一是安全地向安全行业提供先进模型、工具和共同基础设施；二是推动支撑工作重心从"发现漏洞"向"披露、修补、部署补丁"全链路迁移。同期发布面向更广受众的 Claude Security 商业产品（使用 Claude Opus 4.8）。

**5. 通用发布的核心挑战：攻守两用性**

将 Mythos 级能力纳入通用发布需要"既强且精准"的保护措施——既能有效阻止恶意使用，又不过度限制防御用途。这是网络安全与其他 AI 能力的关键差异：攻守两用性意味着无法简单屏蔽。Cyber Verification Program 是当前的过渡方案，向更多组织授权特定网络防御任务的 Mythos 级能力。

## 关键术语

- **Project Glasswing**：Anthropic 发起的关键软件安全合作计划，利用 Claude Mythos Preview 帮助受审查的关键基础设施组织扫描代码漏洞
- **Claude Mythos Preview**：Anthropic 具备强大网络能力的前沿模型，当前仅通过受控合作伙伴项目发布，尚未通用发布
- **Claude Security**：基于 Claude Opus 4.8 等公开模型的商业安全产品，面向更广泛的安全团队扫描代码并建议补丁
- **Cyber Verification Program**：向经过验证的更多组织授权特定网络防御任务使用 Mythos 级能力的程序，是通用发布前的过渡机制
- **Dual-use（攻守两用性）**：AI 网络能力同时可用于攻击和防御，导致保护措施设计极为困难——必须精准区分用途而非简单屏蔽
- **能力门槛（Capability Threshold）**：模型能力跨越某一域的关键节点，触发受控发布和配套规范建设的必要性；Mythos 级网络能力是第一个大规模应用此框架的案例
- **漏洞修补瓶颈**：AI 扫描速度已远超人工验证/披露/修补速度，当前网络安全最大瓶颈在修补链路而非发现

## 相关概念

- concepts/agent-containment — 受控发布的隔离机制与爆炸半径控制
- concepts/agentic-systems — AI Agent 在防御链各环节的自主能力
- concepts/harness-engineering — 安全发布所需的工具与基础设施层
- concepts/managed-agents — 受控组织接入与权限分级管理模式

## 相关实体

- entities/anthropic — Project Glasswing 发起方，Glasswing 安全合作倡议发起方
- entities/claude-opus-4-6 — Claude Opus 4 系列，Claude Security 商业产品使用 Opus 4.8
