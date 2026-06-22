---
title: "Anthropic Economic Index report: Learning curves"
org: "Anthropic"
date: 2026-03-24
source_url: "https://www.anthropic.com/research/economic-index-learning-curves"
tags: ["经济影响"]
summary: "Claude.ai 前10大任务占流量从 24%（2025年11月）降至 19%（2026年2月），平均任务时薪从 $49.3 降至 $47.9。主因是个人类查询（体育比分、产品比较、家庭维护等）的涌入，以及编码任务向 API 侧迁移。这符合标准\"采用曲线\"叙事：早期用户偏向"
summary_zh: "Claude.ai 前10大任务占流量从 24%（2025年11月）降至 19%（2026年2月），平均任务时薪从 $49.3 降至 $47.9。主因是个人类查询（体育比分、产品比较、家庭维护等）的涌入，以及编码任务向 API 侧迁移。这符合标准\"采用曲线\"叙事：早期用户偏向"
summary_en: ""
---



# Anthropic Economic Index report: Learning curves
# Anthropic 经济指数报告：学习曲线

## 核心观点

**1. 使用场景多元化，平均任务价值略降**

Claude.ai 前10大任务占流量从 24%（2025年11月）降至 19%（2026年2月），平均任务时薪从 $49.3 降至 $47.9。主因是个人类查询（体育比分、产品比较、家庭维护等）的涌入，以及编码任务向 API 侧迁移。这符合标准"采用曲线"叙事：早期用户偏向高价值专业用途，后期大众用户带来更广泛的日常任务。

**2. 高使用经验用户显著更成功**

使用 Claude 超过 6 个月的用户，对话成功率比新用户高约 4-5 个百分点。控制任务类型（O*NET 任务固定效应）、语言、国家、模型选择等变量后，该效应依然显著且稳健。高年限用户的任务平均教育年限要求高出近 1 年，个人查询占比少 6%，工作相关查询多 7%。可能机制：learning-by-doing（边用边学）效应，或早期采用者本身具备更强的技术背景（cohort/survivorship bias）。

**3. 用户会按任务价值选择模型**

在付费 Claude.ai 账户中，Opus 模型在高薪任务中的使用率显著更高：软件开发任务使用 Opus 的比例（34%）约是辅导类任务（12%）的 3 倍；每增加 $10 时薪，Opus 使用比例在 Claude.ai 上升 1.5 个百分点，在 API 上升 2.8 个百分点（API 用户响应灵敏度约为 2 倍）。

**4. 美国各州使用量持续收敛，但国际差距扩大**

美国州级前5州份额从 30% 降至 24%，Gini 系数持续下降，预测各州达到人均均等需5-9年（前报告预测2-5年，收敛速度放缓）。国际层面与之相反：顶级20国占总使用量的份额从 45% 升至 48%，发展中国家在全球扩散中继续落后。

**5. 自动化新兴场景：B2B销售与量化交易**

与3个月前相比，API 流量中两类自动化工作流份额翻倍：（1）B2B 销售外展与线索资格审核，（2）市场监控与量化投资建议生成。这可能预示相关职业（销售代表、交易员）工作性质的临近变化。

## 关键术语

- **Anthropic Economic Index（AEI）**：Anthropic 的隐私保护经济影响追踪系统，通过聚合分析百万级对话样本描绘 Claude 在经济活动中的渗透态势
- **AUI（Anthropic AI Usage Index）**：按工作年龄人口调整后的人均 Claude 使用量指数，用于跨地域公平对比
- **O\*NET 任务分类**：美国劳工部职业信息网络的标准职业任务分类体系，本文用于将 Claude 对话映射至具体劳动任务和对应时薪
- **经济基元（Economic Primitives）**：本系列报告的分析框架，包括交互类型（augmentation/automation）、任务教育年限、任务时薪估值、任务完成时间等标准化指标
- **增强 vs 自动化（Augmentation vs Automation）**：五种交互类型的二分归类——增强（validation/learning/task-iteration）表示人机协作，自动化（directive/feedback-loop）表示 AI 独立执行
- **使用年限（Tenure）**：用户注册至今的时长，本文以 6 个月为高/低年限分界点，用于研究学习曲线效应
- **Learning-by-doing（边用边学）**：经济学概念，指通过实际使用积累经验，本文用于解释高年限用户更高成功率的可能机制
- **技能偏向型技术变革（Skill-Biased Technological Change, SBTC）**：经济学概念，指技术创新对高技能劳动者有利而对低技能劳动者不利的变化模式；本文提出 AI 可能成为新的 SBTC 驱动力

## 相关概念

- concepts/agentic-systems — augmentation vs automation 二分类是 Workflow vs Agent 的实证对应
- concepts/managed-agents — API 自动化工作流的扩张，与 Managed Agents 架构扩散相关
- concepts/harness-engineering — API 侧任务集中化和自动化模式涌现，正是 Harness Engineering 规模化的体现
- concepts/eval-awareness — 本报告与 eval-awareness 研究同期（2026-03），Opus 4.6 相关
- concepts/multi-agent-systems — Claude Code 的多 Agent 架构导致编码任务在 API 侧碎片化分布于多个任务类别

## 相关实体

- entities/anthropic — 报告发布方，第三期 Economic Index（继2025-08和2026-01之后）
- entities/claude-opus-4-6 — 本报告采样期（2026-02-05至12）与 Opus 4.6 发布重合；API 中 Opus 在高价值任务上的使用弹性约为 Claude.ai 的 2 倍
