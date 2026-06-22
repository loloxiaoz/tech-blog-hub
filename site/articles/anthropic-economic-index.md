---
title: "Anthropic Economic Index: Insights from Claude 3.7 Sonnet"
org: "Anthropic"
date: 2025-03-27
source_url: "https://www.anthropic.com/research/anthropic-economic-index"
tags: ["Agent", "Eval/评测", "推理模型", "经济影响"]
summary: "Claude 3.7 Sonnet 发布后11天、100万条对话的分析显示，编程类使用占比增幅最大（计算机与数学职业类别 +3%），教育、科学和医疗类也有上升。这既反映 3.7 在编程 benchmark 上的能力提升，也可能反映 AI 向更多行业扩散的大趋势。"
summary_zh: "Claude 3.7 Sonnet 发布后11天、100万条对话的分析显示，编程类使用占比增幅最大（计算机与数学职业类别 +3%），教育、科学和医疗类也有上升。这既反映 3.7 在编程 benchmark 上的能力提升，也可能反映 AI 向更多行业扩散的大趋势。"
summary_en: ""
---



# Anthropic Economic Index: Insights from Claude 3.7 Sonnet
# Anthropic 经济指数：Claude 3.7 Sonnet 洞察报告

## 核心观点

**1. 编程/教育/科学用量随模型升级小幅上升**
Claude 3.7 Sonnet 发布后11天、100万条对话的分析显示，编程类使用占比增幅最大（计算机与数学职业类别 +3%），教育、科学和医疗类也有上升。这既反映 3.7 在编程 benchmark 上的能力提升，也可能反映 AI 向更多行业扩散的大趋势。

**2. 扩展思考模式集中用于高复杂度技术任务**
Extended thinking（扩展思考）在计算机信息研究科学家相关任务中使用率约 10%，软件开发者约 8%，多媒体艺术家约 7%，视频游戏设计师约 6%。使用模式表明：用户在感知到题目需要深度推理时才会主动开启，集中在技术与创意技术领域。

**3. 增强与自动化比例稳定，学习型交互增长**
增强型使用（augmentation）仍占 57%，整体比例基本不变；但子类别中「学习」型（用户请求解释/信息）从约 23% 升至 28%，说明更多用户将 Claude 作为知识获取渠道而非单纯任务执行工具。

**4. 不同职业呈现显著的增强/自动化分化**
- 文案编辑：任务迭代（Task Iteration）占比最高，约 58%——人机共同打磨输出
- 翻译/口译：指令型（Directive）自动化占比最高——最小人工干预下完成文档翻译
- 社区与社会服务类：增强接近 75%
- 计算机与数学类：接近 50-50 均衡

**5. 首发自下而上 630 类细粒度使用分类法**
Clio 工具从实际对话中归纳生成 630 个使用场景聚类，三层层级结构，覆盖 O*NET 无法描述的通用模型使用案例（如「字体选型与故障排查」「电池技术指导」「时区处理代码」）。数据集开源于 Hugging Face。

## 关键术语

- **Anthropic Economic Index**：Anthropic 定期发布的 AI 经济影响研究项目，追踪劳动力市场变化
- **Clio**：隐私保护对话分析工具，将对话映射到 O*NET 任务体系，同时用于底层分类法生成
- **O*NET**：美国劳工部职业信息网络，17000 个职业任务分类，作为顶层分析框架
- **Extended Thinking（扩展思考）**：Claude 3.7 新增模式，用户主动开启以处理高复杂度问题，深度推理前置
- **Augmentation（增强型使用）**：学习、任务迭代、验证、反馈循环——人机协作，AI 辅助人完成任务
- **Automation（自动化型使用）**：指令型——人类最小介入，AI 直接完成任务
- **Task Iteration**：五种交互模式之一，用户与模型共同迭代改进输出（文案编辑类最典型）
- **Directive**：五种交互模式之一，模型以最少人类参与直接完成任务（翻译类最典型）
- **Bottom-up Taxonomy（自下而上分类法）**：从实际对话聚类生成的 630 类使用场景，区别于 O*NET 的预定义自上而下分类

## 相关概念

- concepts/eval-awareness — 模型能力评估的方法论背景（Clio 工具的准确性评估方式）
- concepts/agentic-systems — 扩展思考模式在 Agentic 场景下的使用分布
- concepts/think-tool — think 工具与 extended thinking 的关系与区别

## 相关实体

- entities/anthropic — 本报告发布方，Anthropic 经济指数的主导机构
- entities/claude-opus-4-6 — Claude 3.7 Sonnet 为本报告分析对象（即 claude-3-7-sonnet 系列）
