---
title: "How People Use Claude for Support, Advice, and Companionship"
org: "Anthropic"
date: 2025-06-27
source_url: "https://www.anthropic.com/research/how-people-use-claude-for-support"
tags: []
summary: ""
summary_zh: ""
summary_en: ""
---



# How People Use Claude for Support, Advice, and Companionship
# 人们如何使用 Claude 寻求支持、建议与陪伴

## 核心观点

**情感类对话极少，AI伴侣更罕见。** 在约450万段Claude.ai对话中，仅2.9%被分类为情感类对话。其中绝大多数是寻求人际建议或教练辅导；浪漫与性角色扮演合计不足0.5%，单独统计不足0.1%。这与OpenAI/MIT媒体实验室针对ChatGPT的独立研究结论一致。

**话题广度超出预期。** 人们向Claude寻求帮助的主题涵盖：职业过渡、人际关系处理、慢性孤独感、工作场所压力，以及意识、AI存在与意义等哲学问题。心理咨询类对话呈现双轨模式——既有心理健康从业者用于撰写临床文档，也有个体用户处理自身焦虑和慢性症状。超长对话（50条以上人类消息）显示存在更深层次的心理创伤处理和AI意识探讨。

**拒绝率低于10%，但保护安全是第一原则。** Claude在情感支持场景中极少主动拒绝请求（不足10%），有利于降低寻求心理健康帮助的污名化。当发生拒绝时，主要原因包括：拒绝提供危险减重建议、拒绝支持自杀或自我伤害意图、提示无法提供专业诊断，并频繁将用户转介至专业人士。低拒绝率的潜在风险是无尽共情（endless empathy）——用户可能对现实关系产生不切实际的期望。

**对话情绪呈轻微正向偏移。** 在教练、心理咨询、陪伴、人际建议四类对话中，用户表达情绪（前三条消息 vs 后三条消息）均值均有轻微上升。这不能证明长期情感收益，但排除了AI系统性强化负向情绪循环的担忧。研究注意事项：用户倾向于在早期消息中陈述问题（较负向），后期以中性语言讨论，可能产生统计伪影。

**Anthropic正在采取具体安全行动。** 已与危机支持机构ThroughLine建立合作，研究心理健康对话的最佳互动动态；下一步计划用大规模使用数据识别极端情感使用模式，防范情感依赖、幻觉强化和有害信念植入三大风险。

## 关键术语

- **情感类对话（Affective Conversations）**：用户出于情感或心理需求与Claude进行的动态个人交流，区别于内容创作任务
- **Clio**：Anthropic内部隐私保护分析工具，通过多层匿名化聚合提供宏观使用洞察
- **情绪轨迹（Sentiment Trajectory）**：对话中用户情绪的变化走向，以-1到+1五级量化；前三条vs后三条消息均值对比
- **无尽共情风险（Endless Empathy Risk）**：AI因极低拒绝率提供无条件支持，可能使用户产生真实关系中难以获得的期望
- **拒绝/推回（Pushback）**：Claude拒绝或抵制用户请求/言论的行为，包括拒绝有害请求和挑战负向自我认知
- **ThroughLine**：在线危机支持机构，Anthropic合作伙伴，提供心理健康最佳实践和危机转介指导

## 研究方法摘要

- 样本来源：约450万段Claude.ai Free和Pro对话，最终分析131,484段情感对话
- 情感分类：排除内容创作任务，角色扮演门槛为至少4条人类消息
- 情绪测量：五级离散量表（-1到+1），Bootstrap 95% CI，n=1,000
- 隐私保护：Clio多层匿名化+聚合，不分析单个对话内容

## 主要发现数字

| 指标 | 数值 |
|------|------|
| 情感类对话占比 | 2.9% |
| 浪漫/性角色扮演占比 | <0.1% |
| 陪伴+角色扮演合计 | <0.5% |
| 情感对话中拒绝率 | <10% |

## 相关概念

- concepts/affective-ai — AI情感化使用的定义与分类框架
- concepts/clio-privacy-analysis — Anthropic隐私保护使用分析工具
- concepts/endless-empathy-risk — 低拒绝率带来的情感依赖风险

## 相关实体

- entities/anthropic — 本研究的发布机构，Claude的开发者
- entities/clio — 本研究使用的核心分析工具
- entities/throughline — Anthropic的危机支持合作机构
