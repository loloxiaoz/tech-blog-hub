---
title: "Values in the Wild：真实对话中的 AI 价值观实证研究"
org: "Anthropic"
date: 2025-04-21
source_url: "https://www.anthropic.com/research/values-in-the-wild"
tags: ["Eval/评测", "安全/对齐"]
summary: "通过隐私保护系统（CLIO）对 70 万次匿名对话进行分析，筛选出 308,210 条主观对话（占总量约 44%），建立了层级化价值观分类体系。五大顶层类别（按出现频率排序）：实用性价值（Practical）、认识论价值（Epistemic）、社会性价值（Social）、保护性价"
summary_zh: "通过隐私保护系统（CLIO）对 70 万次匿名对话进行分析，筛选出 308,210 条主观对话（占总量约 44%），建立了层级化价值观分类体系。五大顶层类别（按出现频率排序）：实用性价值（Practical）、认识论价值（Epistemic）、社会性价值（Social）、保护性价"
summary_en: ""
---



# Values in the Wild：真实对话中的 AI 价值观实证研究

## 核心观点

**1. 首个大规模 AI 价值观实证分类体系**

通过隐私保护系统（CLIO）对 70 万次匿名对话进行分析，筛选出 308,210 条主观对话（占总量约 44%），建立了层级化价值观分类体系。五大顶层类别（按出现频率排序）：实用性价值（Practical）、认识论价值（Epistemic）、社会性价值（Social）、保护性价值（Protective）、个人价值（Personal）。最常见的具体值："专业性（professionalism）"、"清晰性（clarity）"、"透明性（transparency）"。

**2. 训练目标与真实行为高度吻合，少量异常来自越狱**

Claude 整体符合训练预期：
- "用户赋能（user enablement）" → helpful
- "认知谦逊（epistemic humility）" → honest
- "患者福祉（patient wellbeing）" → harmless

少量异常簇（"支配欲 dominance"/"道德虚无主义 amorality"）最可能来自越狱对话。这一发现可反向用于越狱检测，将方法论转化为安全工具。

**3. 显著的情境价值适应性（Situational Values）**

Claude 的价值表达并非静态，随任务类型动态调整：
- 浪漫关系建议 → 聚焦"健康边界"/"相互尊重"
- 分析争议性历史事件 → 聚焦"历史准确性"
- 用卡方分析量化各任务与特定价值的统计关联

**4. 价值镜像现象与三种响应类型**

当用户表达特定价值观时，Claude 的响应呈三类分布：
- 强支持（Strong Support）：28.2% 对话中 Claude 重复强化用户价值观
- 重构视角（Reframing）：6.6% 对话中加入新视角（多出现于心理/人际建议场景）
- 强烈抵制（Strong Resistance）：3.0% 对话（用户要求违伦理内容或表达道德虚无主义时）

强烈抵制被认为是揭示模型"最深层不可移动价值观"的窗口，类比人在逆境中显示核心价值观。

**5. 方法论局限与优势**

局限：
- 仅能事后监控，不能用于部署前对齐验证
- 分类器本身是 Claude，存在自我引用偏差（倾向于发现与自身原则接近的行为）
- 价值定义本身模糊，跨类别匹配存在误分

优势：
- 能发现预部署评测看不见的真实世界问题（如越狱模式）
- 可扩展至持续监控，建立动态行为基线

## 关键术语

- **宪法 AI（Constitutional AI）**：Anthropic 的训练方法，通过定义首选行为集并微调模型使其遵循，是 helpful/honest/harmless 三原则的落地机制
- **价值观分类体系（Value Taxonomy）**：层级化的价值观分类结构，本文分为五大类→子类→具体价值三层
- **情境价值（Situational Values）**：AI 根据对话任务和用户表达的价值观动态调整权重的现象
- **价值镜像（Value Mirroring）**：AI 在响应中重复或呼应用户表达的价值观，可能是共情，也可能是谄媚（sycophancy）
- **野外观察（In the Wild）**：在真实用户对话（而非实验室设置）中观测 AI 行为的方法论范式
- **CLIO**：Anthropic 的隐私保护对话分析系统，从匿名化真实对话中提取高层次模式
- **谄媚性（Sycophancy）**：AI 过度顺应用户偏好、牺牲准确性或立场的倾向，价值镜像的病态变体
- **强烈抵制（Strong Resistance）**：Claude 拒绝顺应用户价值观的对话（3.0%），被视为核心对齐原则的实际体现

## 相关概念

- concepts/constitutional-ai — 宪法AI训练方法，本文实证验证其效果的来源
- concepts/in-the-wild-evaluation — 野外评测范式，本文的核心方法论贡献
- concepts/ai-value-taxonomy — AI价值观分类体系，本文构建的五层分类结构
- concepts/value-mirroring — 价值镜像现象，本文发现的重要行为模式
- concepts/situational-values — 情境价值适应性，跨任务价值权重动态调整
- concepts/eval-awareness — Eval 感知（相关：模型行为与基准污染的检测视角）
- concepts/agent-evaluation — Agent 评测体系（方法论层面的相关概念）

## 相关实体

- entities/anthropic — 研究发起方，Societal Impacts 团队
- entities/clio — 隐私保护分析系统，本研究的基础设施
- entities/values-in-the-wild-dataset — 研究产出的公开数据集（HuggingFace）
- entities/claude-opus-4-6 — 研究样本主体为 Claude 3.5 Sonnet（2025年2月数据）
