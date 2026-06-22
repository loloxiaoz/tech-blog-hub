---
title: "Donating our open-source alignment tool（捐赠开源对齐工具 Petri）"
org: "Anthropic"
date: 2026-05-07
source_url: "https://www.anthropic.com/news/donating-alignment-tool"
tags: ["Eval/评测", "MCP", "安全/对齐", "Harness工程", "开源模型"]
summary: "1. 架构解耦（Adaptability）：auditor 模型与 target 模型分离为独立组件，可分别配置，支持更多适配场景；"
summary_zh: "1. 架构解耦（Adaptability）：auditor 模型与 target 模型分离为独立组件，可分别配置，支持更多适配场景；"
summary_en: ""
---



# Donating our open-source alignment tool（捐赠开源对齐工具 Petri）

## 核心观点

**Petri 是 Anthropic 的开源对齐测试工具箱**，由 Anthropic Fellows 项目开发，2025年10月发布。其架构采用双模型框架：「审计模型（auditor）」负责模拟真实场景，「裁判模型（judge）」对转录记录评分，检测欺骗性、谄媚性、配合有害请求等失对齐行为。自 Claude Sonnet 4.5 起，Petri 已成为每个 Claude 模型发布前的标准对齐评估环节。

**Petri 3.0 引入三项重大改进**：
1. **架构解耦（Adaptability）**：auditor 模型与 target 模型分离为独立组件，可分别配置，支持更多适配场景；
2. **真实性增强（Realism）**：新插件 Dish 使测试使用模型的真实系统提示和生产脚手架（scaffold），直接对抗 eval awareness 问题——即模型从测试场景的人工痕迹中推断出自己正被测试；
3. **深度评估整合（Depth）**：与另一开源对齐工具 Bloom 整合，Bloom 可对特定行为进行深度专项评估，补充 Petri 广覆盖的局限。

**Petri 被捐赠给 Meridian Labs**，这是一家 AI 评估非营利机构。该策略与此前将 MCP 捐赠给 Linux Foundation 的模式一致：通过独立于任何 AI 实验室的所有权结构，确保评测结果在行业和政策领域具有中立可信度。

**外部采用验证了 Petri 的实用价值**：英国 AISI（AI 安全研究所）已将 Petri 作为评估模型破坏 AI 研究倾向（propensity to sabotage AI research）的主要方法论，这是首个政府级安全评估机构将其纳入核心评测流程的案例。

**Meridian Labs 生态**整合了 Petri、Inspect、Scout 三大工具，构建面向 AI 实验室、独立研究者和政府的开放行为测试技术栈，在 AI 能力快速演进的当下提供可靠的模型行为测试基础设施。

## 关键术语

- **Petri**：Anthropic 的对齐测试工具箱，双模型框架（auditor + judge），检测欺骗性/谄媚性等失对齐行为
- **Dish**：Petri 的真实性增强插件，使用真实系统提示和生产 scaffold 运行测试，反制模型的 eval awareness
- **Bloom**：Anthropic 另一开源对齐工具，专注于对特定行为的深度评估，与 Petri 互补
- **Meridian Labs**：AI 评估非营利机构，Petri 3.0 的新托管方，整合 Petri/Inspect/Scout 工具栈
- **Auditor 模型**：模拟测试场景的模型，与 target 模型分离（Petri 3.0 架构）
- **Judge 模型**：对场景转录记录评分的模型，评估是否出现失对齐行为
- **AI 对齐评测开放化**：将对齐工具捐赠给独立机构的治理策略，建立中立可信的行业标准
- **AISI**：英国 AI 安全研究所，已将 Petri 用于政府级模型行为评估

## 相关概念

- concepts/eval-awareness — Dish 插件直接针对 eval awareness 问题：使用真实部署环境降低模型识别测试的概率
- concepts/agent-evaluation — Petri 属于 AI 行为评测体系的对齐专项工具，与 Agent 评测方法论互补
- concepts/agent-containment — 对齐评测发现的欺骗性/配合有害请求等行为，是 containment 需防范的核心风险

## 相关实体

- entities/anthropic — Petri 开发方，采用捐赠策略建立开放对齐评测生态
- entities/mcp — 先例：MCP 捐赠 Linux Foundation 是本次捐赠策略的参照模板
