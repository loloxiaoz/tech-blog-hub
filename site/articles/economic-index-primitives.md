---
title: "Anthropic Economic Index Report: Economic Primitives"
org: "Anthropic"
date: 2026-01-15
source_url: "https://www.anthropic.com/research/economic-index-primitives"
tags: ["RAG/检索", "经济影响"]
summary: "本报告引入五个\"经济原语（Economic Primitives）\"，通过让 Claude 自评匿名对话批量生成：任务复杂度（人工完成耗时）、人机技能水平（理解提示/响应所需教育年限）、使用场景（工作/课程/个人）、AI自主度（1-5分决策委托程度）、任务成功率（Claude"
summary_zh: "本报告引入五个\"经济原语（Economic Primitives）\"，通过让 Claude 自评匿名对话批量生成：任务复杂度（人工完成耗时）、人机技能水平（理解提示/响应所需教育年限）、使用场景（工作/课程/个人）、AI自主度（1-5分决策委托程度）、任务成功率（Claude"
summary_en: ""
---



# Anthropic Economic Index Report: Economic Primitives
# Anthropic 经济指数报告：经济原语

## 核心观点

**1. 五项经济原语：量化AI经济影响的基础测量层**

本报告引入五个"经济原语（Economic Primitives）"，通过让 Claude 自评匿名对话批量生成：任务复杂度（人工完成耗时）、人机技能水平（理解提示/响应所需教育年限）、使用场景（工作/课程/个人）、AI自主度（1-5分决策委托程度）、任务成功率（Claude自评是否完成任务）。这些原语覆盖 Claude.ai 消费者端和 1P API 企业端，并支持按国家/美国各州分解。

**2. 任务成功率揭示真实能力边界：任务时间视野**

Claude 在大多数任务上成功，但成功率随复杂度系统性下降。在 API 流量中，不足1小时任务成功率约60%，5小时以上降至45%，50%成功率临界点（任务时间视野）约3.5小时。Claude.ai 因多轮对话将复杂任务分解为小步骤，时间视野延伸至约19小时——验证了多轮交互对长时程任务的实质性价值。

**3. 有效AI覆盖率重新评估职业自动化程度**

引入"有效 AI 覆盖率"（Effective AI Coverage）= 任务覆盖率 × 成功率加权。数据录入员虽只有2/9个任务被覆盖，但最主要任务（读取录入原始文档）成功率高，有效覆盖率反而靠前。将任务成功率纳入后，美国劳动生产率年增估算从1.8个百分点降至1.0-1.2个百分点；即便如此，仍相当于回归1990年代末至2000年代初的生产力增长水平。

**4. Claude偏向高技能任务，净效果是职业去技能化**

Claude 覆盖的任务平均所需教育14.4年，高于经济整体的13.2年。这意味着如果 AI 辅助任务从工作中移除，留下的是更低技能的工作——差旅顾问失去复杂规划留下订票（去技能化），物业管理员失去记账保留合同谈判（升技能化）。影响并非均一，具体取决于职业内任务技能分布。

**5. 地理扩散双轨：全球差距稳定，美国快速收敛**

全球层面，人均GDP与Claude使用率强相关（国家级 r=0.925），低收入国家集中于课程学习用途，高收入国家个人/工作用途多元化——符合技术扩散的"早期采纳者→成熟市场"曲线。全球区域间差距稳定，无收敛或扩大迹象。美国各州则相反：Gini系数从0.37降至0.32，按当前速率2-5年内可实现人均使用均等化，远快于历史技术扩散约50年的先例。

## 关键术语

- **Economic Primitives（经济原语）**：五项基础测量维度，通过 Claude 自评批量标注匿名对话，用于量化 AI 经济影响的简单、可组合指标集
- **Task Horizon（任务时间视野）**：AI 成功率随任务持续时长下降的曲线，50%成功率对应的时长为临界点；API约3.5小时，Claude.ai约19小时
- **Effective AI Coverage（有效AI覆盖率）**：任务覆盖率×成功率的加权和，比纯任务覆盖率更准确反映职业自动化暴露程度
- **Anthropic AI Usage Index（AUI）**：某国 Claude 使用份额除以其劳动年龄人口份额，标准化跨国使用率的相对指标
- **Augmentation vs Automation（增强型 vs 自动化型）**：两大交互类别，前者含学习/任务迭代/验证，后者含指令式/反馈循环；2025年11月 Claude.ai 增强型重新占主导（52%）
- **Deskilling（去技能化）**：AI 覆盖某职业中相对高技能任务后，剩余工作平均技能要求下降的效应
- **Elasticity of Substitution（替代弹性）**：衡量任务互补/替代关系的参数；弹性=0.5（互补性强）时生产力效应降至0.7-0.9个百分点/年
- **O*NET Tasks**：美国劳工部职业信息网络标准任务分类，用于将 Claude 对话映射到职业

## 相关概念

- concepts/economic-primitives — 五项经济原语定义与局限性
- concepts/task-horizon — 任务时间视野：成功率随时长的衰减曲线
- concepts/effective-ai-coverage — 有效AI覆盖率：任务覆盖×成功率加权
- concepts/ai-labor-market-impact — AI对劳动力市场的结构性影响
- concepts/anthropic-ai-usage-index — AUI：跨国使用率标准化指标
- concepts/augmentation-vs-automation — 增强型 vs 自动化型交互分类（数据更新：2025年11月）
- concepts/harness-engineering — Harness 工程：API 侧自动化主导背景下的工程范式
- concepts/agent-evaluation — Agent 评测体系：与任务成功率原语的方法论关联

## 相关实体

- entities/anthropic — 报告发布方，第四期经济指数
- entities/anthropic-economic-index — 报告系列实体页
