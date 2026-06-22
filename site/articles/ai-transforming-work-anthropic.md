---
title: "How AI Is Transforming Work at Anthropic"
org: "Anthropic"
date: 2025-12-02
source_url: "https://www.anthropic.com/research/how-ai-is-transforming-work"
tags: ["Agent", "Claude Code", "多模态", "经济影响", "工具调用"]
summary: "原文：https://www.anthropic.com/news/how-ai-is-transforming-work-at-anthropic"
summary_zh: ""
summary_en: "原文：https://www.anthropic.com/news/how-ai-is-transforming-work-at-anthropic"
---



# How AI Is Transforming Work at Anthropic
# AI 如何改变 Anthropic 的工作方式

原文：https://www.anthropic.com/news/how-ai-is-transforming-work-at-anthropic

## 核心观点

**1. AI使用量与生产力在一年内双倍增长**
工程师自报Claude参与59%工作（去年28%），生产力提升+50%（去年+20%）。14%的超级用户生产力提升超100%。产出量增长显著大于时间节省——在几乎所有任务类别中，产出量净增加，而时间净减少幅度相对较小。

**2. 全栈化民主化：AI开启了以前不可能的工作**
27%的Claude辅助工作是没有AI就不会做的增量新工作（扩展项目、交互式仪表盘、文档测试等）。8.6%的Claude Code任务专门修复长期积压的"纸划伤"（papercut）小问题——代码可维护性重构、终端快捷键等。Claude Code使后端工程师能独立完成UI、研究员能生成前端数据可视化，"everyone is becoming more full-stack"。

**3. Claude Code自主性持续提升（数据）**
分析20万条内部Claude Code记录（2025年2月 vs 8月）：
- 平均最大连续工具调用次数：9.8 → 21.2（+116%）
- 每次对话平均人工干预次数：6.2 → 4.1（-33%）
- 平均任务复杂度评分：3.2 → 3.8（0-5分）
- 特征实现占比：14.3% → 36.9%
- 代码设计/规划占比：1.0% → 9.9%

**4. 监督悖论（Paradox of Supervision）**
AI加速了技能广化（front-end、数据库、API等新领域），但深度编码技能因缺乏练习而萎缩。关键矛盾：有效监督Claude的输出恰恰需要这些可能萎缩的深度技能。"当产出变得如此容易和快速，反而很难花时间去真正学习某件事。"部分工程师通过刻意不使用Claude来保持技能。

**5. 职业与社会动态深度重塑**
Claude成为同事问题的"第一窗口"，80-90%的问题先问Claude，传统导师制和协作文化被弱化。工程师角色向"AI agent管理者"转变，有人估计70%+的工作已转为代码审查/修订而非净新增编写。长期职业前景广泛不确定，部分人表达了"我每天来上班是在把自己变得多余"的情绪。

## 关键术语

**Papercut Fix**：修复长期被忽视的小质量问题（代码可维护性重构、终端快捷键、小工具），8.6%的Claude Code任务属于此类，是AI开启新增工作的典型形式。

**Paradox of Supervision（监督悖论）**：使用AI可能导致深度技能萎缩，而有效监督AI恰恰需要这些技能——形成自我强化的负向循环。

**AI Delegation Strategy（AI委托策略）**：工程师发展出的任务委托框架——低背景知识+易验证+可隔离+非关键质量+重复无聊的任务适合委托；与METR外部研究独立发现的AI生产力障碍因素高度吻合。

**Full-Stack Democratization（全栈化民主化）**：借助AI，专业背景工程师突破专业边界，后端做前端、研究员做可视化，边界持续重新谈判。

**Power User**：内部定义为生产力提升超100%的工程师，占受访者14%，代表AI最大化利用的上限。

**Collateral Learning（附带学习）**：手动解决问题时的附带学习——阅读不直接相关的文档和代码构建系统认知；AI直接跳过这一过程，是技能萎缩的深层机制。

**Task Complexity Score**：Claude Code任务复杂度评分（1-5分），1=基础编辑，5=需要数周专家工作；Anthropic内部从3.2升至3.8，代表AI被委托的任务愈加复杂。

## 调研方法

- 问卷调查：132名工程师/研究员（2025年8月）
- 深度访谈：53人（首批回复者）
- Claude Code transcript分析：20万条（2025年2月 vs 8月），使用Clio隐私保护分析工具

## 主要局限性

- 选择性偏差：对Claude强烈关注的人更可能参与调查
- 社会期望偏差：非匿名调查，正面评价可能被放大
- 回忆偏差：回顾一年前的使用情况存在记忆失真
- Claude Code transcript分析只能测量相对分布变化，不能测量绝对工作量变化

## 相关概念

- concepts/cognitive-arbitrage — 本文是认知套利框架的大规模实证：碳基决策+硅基执行的企业级验证
- concepts/harness-engineering — Claude Code作为核心Harness，自主工具调用增加是Harness能力提升的直接体现
- concepts/context-engineering — 工程师委托策略与上下文工程中"任务适配性"判断高度呼应
- concepts/agent-evaluation — 任务复杂度评分方法（1-5级）是评测体系的实际应用案例
- concepts/compaction — 上下文管理在长任务（平均21次工具调用）中的重要性
- concepts/eval-awareness — 监督悖论与eval-awareness同源：过度依赖AI可能降低识别AI错误的能力

## 相关实体

- entities/anthropic — 本研究的主体，首次公布内部AI使用深度数据
- entities/claude-code — 研究主要工具，提供20万条transcript的使用数据
