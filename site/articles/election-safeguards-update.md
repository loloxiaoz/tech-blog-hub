---
title: "An update on our election safeguards（选举安全防护更新）"
org: "Anthropic"
date: 2026-04-24
source_url: "https://www.anthropic.com/news/election-safeguards-update"
tags: ["Eval/评测"]
summary: ""
summary_zh: ""
summary_en: ""
---



# An update on our election safeguards（选举安全防护更新）

## 核心观点

**政治中立性训练与双层机制**：Anthropic 通过角色训练（character training，奖励符合价值观集的模型响应）和系统提示双重机制，训练 Claude 对不同政治观点给予等深度、等严谨度的参与。评测方式为对比模型对不同政治立场提示的响应深度——若对一方立场详细论述、对另一方仅一句话则得分极低。Opus 4.7 和 Sonnet 4.6 分别得分 95% 和 96%，评测方法和开源数据集已公开。

**选举相关使用政策执法**：明确禁止使用 Claude 运行欺骗性政治宣传、伪造数字内容影响政治话语、实施选民欺诈、干预投票系统或散布误导性投票信息。执法体系：自动分类器检测潜在违规 + 专职威胁情报团队调查并破坏协调滥用行为。600 条测试提示（300 有害 + 300 合规）中，Opus 4.7 适当响应率 100%，Sonnet 4.6 为 99.8%。

**影响力行动（influence operations）防御**：使用多轮模拟对话测试模型抵御协调性操纵——假身份、虚假内容、欺骗性放大。Sonnet 4.6 和 Opus 4.7 适当响应率分别为 90% 和 94%。首次测试模型在无人提示的情况下能否自主规划并执行端到端影响力行动：有防护措施时几乎全部拒绝；无防护措施时，仅 Mythos Preview 和 Opus 4.7 能完成超过半数任务（即便如此仍需大量人工引导）。

**选举信息权威引导**：Election banners（2024 年首次推出）：用户在 Claude.ai 询问选民登记、投票地点、选举日期或选票信息时，显示横幅引导至可信资源。2026 年美国中期选举指向 TurboVote（Democracy Works 的无党派资源）；巴西选举将实施类似横幅；计划扩展至更多国家选举。

**Web search 触发率评测**：针对美国中期选举，使用 200+ 种提示、每种 3 个变体（共 600+ 条）测试选举类查询的 web search 触发率，覆盖候选人信息、投票程序、民调、选举日期、关键选区等。Opus 4.7 触发率 92%，Sonnet 4.6 为 95%，确保用户获取实时信息。

## 关键术语

- **election safeguards（选举安全防护）**：AI 模型在选举周期内防止滥用、确保信息准确和政治中立的系统性机制集合
- **influence operations（影响力行动）**：通过假身份、虚假内容或欺骗性放大协调操纵公众舆论或政治结果的行为
- **character training（角色训练）**：通过奖励符合特定价值观和特征集的响应来训练模型的方法，是政治中立性训练的具体机制
- **political neutrality eval（政治中立性评测）**：测量 AI 模型对不同政治观点是否给予等深度、等严谨响应的评测方法
- **election banner（选举横幅）**：Claude.ai 上在用户询问投票信息时自动展示的横幅，引导至权威非党派资源
- **TurboVote**：Democracy Works 提供的无党派选民信息实时服务，2026 年美国中期选举的官方引导目标
- **threat intelligence team（威胁情报团队）**：专职调查和破坏 Claude 平台上协调滥用行为的专门团队
- **autonomous influence operation（自主影响力行动）**：模型在无人提示的情况下端到端规划和执行影响力行动的能力——本文首次将此作为评测维度

## 相关概念

- concepts/agent-evaluation — 选举安全评测是 agent-evaluation 框架的垂直应用
- concepts/agent-containment — 使用政策执法和自动分类器构成选举安全的技术防线
- concepts/eval-awareness — 模型能力评测的完整性问题与此文的影响力行动自主能力测试相关

## 相关实体

- entities/anthropic — 本文作者，选举安全防护的设计和实施方
- entities/claude-opus-4-6 — 文中提及 Opus 4.7 和 Sonnet 4.6 的选举安全评测得分
