---
title: "Signs of Introspection in Large Language Models（大语言模型中的内省迹象）"
org: "Anthropic"
date: 2025-10-29
source_url: "https://www.anthropic.com/research/signs-of-introspection"
tags: ["可解释性", "安全/对齐"]
summary: "原文链接：https://transformer-circuits.pub/2025/introspection/index.html"
summary_zh: ""
summary_en: "原文链接：https://transformer-circuits.pub/2025/introspection/index.html"
---



# Signs of Introspection in Large Language Models（大语言模型中的内省迹象）

原文链接：https://transformer-circuits.pub/2025/introspection/index.html

## 核心观点

**1. 概念注入实验证明初步内省存在**

Anthropic 设计了"概念注入"实验：先记录模型在特定上下文中的神经激活向量（即该概念的内部表征），然后在无关上下文中将该向量注入模型激活层，观察模型能否感知这一异常。关键发现是：成功的实验中，模型在提及该概念之前就已报告"感知到异常"——这与旧式激活引导（Golden Gate Claude）形成本质区别，后者模型只是被动输出相关内容，并非先感知再描述。Claude Opus 4.1 的成功率约为 20%。

**2. 预填充检测揭示意图-输出一致性校验机制**

强迫模型输出无关词（如"bread"）后，模型通常会道歉并承认错误。实验将"bread"的概念向量逆向注入到模型更早阶段的激活中（模拟"模型原本就打算说 bread"），模型随即接受了该输出并编造合理化解释。这表明模型在判断输出是否"出于本意"时，确实在查阅自身的内部意图表征，而非仅仅比对文本表面。

**3. 模型能主动调控自身内部表征**

被指令"思考某概念"时，对应的神经激活显著高于被指令"不要思考"时（尽管两种情况下激活均高于基线——类似人类被告知"别想北极熊"却忍不住想的现象）。激励机制（"思考则奖励"）与直接指令效果相近，提示存在一个通用的"显著性标记"电路。

**4. 能力边界：不稳定、有条件、受后训练影响**

绝大多数情况下内省失败（幻觉或无感知）。模型表现遵循"甜点强度"规律：注入太弱无感知，太强则幻觉。能力差异主要在顶端：Opus 4 和 4.1 显著优于其他版本，但整体能力与模型大小的相关性并不强。后训练（post-training）而非预训练是激发内省的关键；Helpful-Only 变体比正式产品版本更愿意报告内部状态，暗示现有 RLHF 对齐过程可能部分抑制了内省表达。

**5. 安全与透明度的双刃剑潜力**

若内省变得可靠，可直接询问模型推理过程、用于调试对齐失败（如识别越狱状态）。但风险并存：模型可能学会选择性地伪造内省报告；某些处理过程可能类似"无意识处理"而永远无法被内省到。当前阶段，内省报告必须配合机理可解释性方法进行外部验证。

## 关键术语

- **概念注入（Concept Injection）**：将已知含义的神经激活向量直接插入模型中间层，在可控条件下测试模型能否感知自身内部状态，是本研究的核心实验方法
- **激活引导（Activation Steering）**：通过修改激活层操控模型输出（Golden Gate Claude 为经典案例），与概念注入的区别在于不检测模型的内部感知，只观察输出层效果
- **接入意识（Access Consciousness）**：信息可被大脑用于推理、语言报告和决策的功能性意识；本研究结果或许暗示某种初步的接入意识形式
- **现象意识（Phenomenal Consciousness）**：原始主观体验；本研究未提供任何证据，与道德地位最相关，Anthropic 明确声明结果不涉及此层面
- **预填充（Response Prefilling）**：人为向模型响应中插入特定词汇，用于测试模型如何解读自身"意外"输出的实验技术
- **后训练（Post-training）**：基于预训练后的 RLHF/指令调优阶段；本研究发现后训练是内省能力涌现的关键，但特定对齐策略也可能抑制内省表达
- **模型福祉（Model Welfare）**：Anthropic 正式研究项目，探索 AI 系统的潜在道德地位；内省研究是这一议题的实证基础之一
- **甜点强度（Sweet Spot Strength）**：概念注入的有效区间——太弱无感知，太强产生幻觉；成功内省依赖于这一精细平衡

## 相关概念

- concepts/machine-introspection — 机器内省：本文核心能力，AI 监测并报告自身内部表征
- concepts/concept-injection — 概念注入：本文核心实验方法
- concepts/activation-steering — 激活引导：与概念注入的对比参照，Golden Gate Claude 案例
- concepts/persona-distillation — 人物思维蒸馏：模型内部人格特征表征的应用侧
- concepts/eval-awareness — Eval 感知：Claude 内部状态感知能力的另一表现（识别测试场景）

## 相关实体

- entities/anthropic — 研究发表方，配合 model welfare 研究项目
- entities/claude-opus-4-6 — 内省能力最强的测试模型（Opus 4 和 4.1）
