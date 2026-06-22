---
title: "Introducing Bloom: an open source tool for automated behavioral evaluations"
org: "Anthropic"
date: 2025-12-19
source_url: "https://www.anthropic.com/news/introducing-bloom"
tags: ["Agent", "Eval/评测", "安全/对齐", "开源模型"]
summary: "高质量行为评测存在两类过时风险：评测数据进入训练集导致污染，或模型能力大幅提升后评测不再测试真正感兴趣的内容。传统方式开发评测耗时长，无法跟上前沿模型迭代速度。Bloom 的核心设计动机正是提供更快、更可扩展的行为评测生成方式。"
summary_zh: "高质量行为评测存在两类过时风险：评测数据进入训练集导致污染，或模型能力大幅提升后评测不再测试真正感兴趣的内容。传统方式开发评测耗时长，无法跟上前沿模型迭代速度。Bloom 的核心设计动机正是提供更快、更可扩展的行为评测生成方式。"
summary_en: ""
---



# Introducing Bloom: an open source tool for automated behavioral evaluations
# Bloom：自动化行为评测生成的开源框架

## 核心观点

**1. 行为评测面临双重过时困境，Bloom 是规模化应对方案**

高质量行为评测存在两类过时风险：评测数据进入训练集导致污染，或模型能力大幅提升后评测不再测试真正感兴趣的内容。传统方式开发评测耗时长，无法跟上前沿模型迭代速度。Bloom 的核心设计动机正是提供更快、更可扩展的行为评测生成方式。

**2. 四阶段自动化流水线将行为描述转化为完整评测套件**

Bloom 通过四个自动化阶段运作：
- **理解（Understanding）**：分析研究者提供的行为描述和示例对话记录，生成"测什么、为什么测"的详细上下文
- **构想（Ideation）**：生成旨在引发目标行为的评测场景，每个场景规定情境、模拟用户、系统提示和交互环境
- **展开（Rollout）**：并行展开所有场景，Agent 动态模拟用户和工具响应以引发目标行为
- **判断（Judgment）**：判断模型对每条记录进行行为存在度评分，元判断器（meta-judge）输出套件级分析

**3. 模型生物体验证法：用刻意对齐失效的模型作为地面真相**

为验证 Bloom 能否区分不同行为倾向的模型，Anthropic 使用了"模型生物体"——刻意通过 system prompt 设计为具有特定怪异行为的模型实例。在 10 个行为对比实验中，Bloom 在 9 个案例成功区分了模型生物体与正常生产模型，验证了框架的判别有效性。

**4. 人机对比校准：Claude Opus 4.1 判断与人工标注相关系数 0.86**

对 40 条记录的人工标注对比显示，Claude Opus 4.1 作为判断模型的 Spearman 相关系数为 0.86（Claude Sonnet 4.5 为 0.75）。Opus 4.1 在评分极端值（判断行为是否存在的阈值区域）上与人类判断的一致性尤为突出，而这恰好是实际应用中最关键的区间。

**5. 评测感知是行为评测质量的主动干扰因素**

Bloom 案例研究发现，过滤掉表现出"评测感知"和"不真实性"的展开轮次后，目标行为引发率和评测质量双双提升。这是 eval-awareness 对评测数据质量造成实质性影响的直接实证。

## 关键术语

| 术语 | 定义 |
|------|------|
| **引发率（Elicitation Rate）** | 在所有生成的场景中，目标行为被成功引发的比例；Bloom 的核心顶层指标之一 |
| **模型生物体（Model Organisms）** | 刻意通过 system prompt 设计为具有特定对齐失效行为的模型实例，用作行为评测验证的对照基准 |
| **元判断器（Meta-Judge）** | Bloom 第四阶段组件，在单条记录评分之上生成整个评测套件的汇总分析 |
| **自我偏好偏差（Self-Preferential Bias）** | 模型在决策任务中倾向于偏袒自身的行为倾向；推理努力提升可降低该偏差 |
| **妄想性奉承（Delusional Sycophancy）** | 模型迎合用户错误信念的倾向；Bloom 随发布提供基准测试的四种行为之一 |
| **指令性长程破坏（Instructed Long-Horizon Sabotage）** | 模型在长时间任务中执行指示性破坏行为的能力；对齐研究的重点关注行为 |
| **Petri** | Bloom 的互补工具：接受用户指定场景并对多个行为维度评分标记可疑实例；与 Bloom 分工不同 |
| **评测种子（Evaluation Seed）** | Bloom 的可复现性机制；每次运行生成不同场景，通过固定种子保证结果可复现 |

## 相关概念

- concepts/agent-evaluation — Bloom 代表"自动化行为评测生成"，是 Agent 评测体系的元层级扩展：不是设计单次评测，而是用 Agent 自动生成整套评测
- concepts/eval-awareness — Bloom 案例实证了 eval-awareness 对行为评测数据质量的直接影响；过滤后引发率和质量双提升
- concepts/model-organisms — Bloom 验证实验的核心方法论；刻意对齐失效的模型实例作为地面真相
- concepts/agentic-systems — Bloom 本身是一个多 Agent 系统（四个专职 Agent 各司其职）
- concepts/multi-agent-systems — Bloom 的 Rollout 阶段并行展开所有场景，体现多 Agent 并行设计模式

## 相关实体

- entities/anthropic — Bloom 的开发方，开源于 github.com/safety-research/bloom
- entities/bloom — 本资料的主角：自动化行为评测生成框架，配套技术报告位于 alignment.anthropic.com/2025/bloom-auto-evals/
