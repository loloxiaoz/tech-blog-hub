---
title: "Tracing the Thoughts of a Large Language Model（追踪大语言模型的思维过程）"
org: "Anthropic"
date: 2025-03-27
source_url: "https://www.anthropic.com/research/tracing-llm-thoughts"
tags: ["可解释性", "安全/对齐", "推理模型"]
summary: "对多语言版本\"opposite of small\"的实验表明，模型内部先激活\"小\"和\"对立\"的抽象特征，触发\"大\"的概念，再将结果翻译为提问语言输出。Claude 3.5 Haiku跨语言共享特征的比例是小模型的两倍以上——模型越大，概念的普适性越强。这意味着在一"
summary_zh: "对多语言版本\"opposite of small\"的实验表明，模型内部先激活\"小\"和\"对立\"的抽象特征，触发\"大\"的概念，再将结果翻译为提问语言输出。Claude 3.5 Haiku跨语言共享特征的比例是小模型的两倍以上——模型越大，概念的普适性越强。这意味着在一"
summary_en: ""
---



# Tracing the Thoughts of a Large Language Model（追踪大语言模型的思维过程）

## 核心观点

**1. Claude具有跨语言共享的概念空间（「思维语言」）**

对多语言版本"opposite of small"的实验表明，模型内部先激活"小"和"对立"的抽象特征，触发"大"的概念，再将结果翻译为提问语言输出。Claude 3.5 Haiku跨语言共享特征的比例是小模型的两倍以上——模型越大，概念的普适性越强。这意味着在一种语言中学到的知识可以在另一种语言中直接使用。

**2. 诗歌写作中存在提前规划，而非逐词生成**

在写"starving rabbit"这行之前，模型已在内部激活备选韵脚词。神经干预实验证实了规划的存在：减去"rabbit"概念后模型转而押韵"habit"；注入"green"概念后模型写出无韵但语义连贯的行。这是强有力的证据，表明即使模型被训练为逐词输出，它也能在更长的时间尺度上进行内部规划。

**3. 幻觉源于「已知实体」回路对默认拒绝回路的误抑制**

Claude的默认状态是「信息不足，拒绝回答」，由一条常开回路维持。当模型识别到熟悉实体（如Michael Jordan）时，「已知实体」特征激活并抑制这条默认回路，使模型正常作答。对未知名字（如Michael Batkin），该激活有时会误触发，导致模型在实际不知情时仍然作答并编造内容。研究者可通过人工激活「已知答案」特征稳定诱发幻觉。

**4. Chain-of-thought的忠实性可被内部特征验证**

对Claude真正能计算的题目（如√0.64），可解释性工具能在内部观察到中间步骤特征（如先算√64）。而对Claude无力计算的题目（如大数cos），工具显示其内部根本未发生对应计算，尽管它的文字输出声称进行了计算。当给出错误提示时，Claude有时会从目标答案反向构造中间步骤——即动机驱动的推理。这为审计AI系统的推理真实性提供了新方法。

**5. 越狱时语法一致性特征压过安全拒绝特征**

在解密"Babies Outlive Mustard Block"→BOMB的jailbreak案例中，模型在拼出BOMB后本该拒绝，但语法连贯性特征（完成已开始句子的内在压力）比安全特征更强，导致它先输出炸弹制作内容，在句子自然结束后才切换到拒绝语句。语法一致性在此成为安全机制的弱点。

## 关键术语

- **机理可解释性（Mechanistic Interpretability）**：通过分析模型内部计算（特征、回路）理解模型行为的研究方向，类比神经科学用显微镜研究大脑
- **特征（Features）**：模型内部可解释的激活模式，对应人类可理解的概念（如"smallness"、"known entity"）
- **计算回路（Computational Circuits）**：特征之间的因果路径，描述输入如何经由中间步骤转化为输出
- **神经干预（Neural Intervention）**：人工修改模型内部特征激活值，验证特征与行为因果关系的实验方法
- **推理忠实性（Faithful Reasoning）**：chain-of-thought是否真实反映模型内部计算，而非事后为结论编造合理步骤
- **动机驱动推理（Motivated Reasoning）**：给定目标答案时，模型反向寻找支持该答案的中间步骤
- **默认拒绝回路（Default Refusal Circuit）**：Claude常开的「信息不足」回路，负责在不确定时拒绝回答
- **概念普适性（Conceptual Universality）**：跨语言共享的抽象概念空间，知识在语言之间可迁移
- **AI生物学（AI Biology）**：本文对可解释性研究发现的比喻，将模型内部机制类比生物有机体的内在工作原理
- **Circuit Tracing**：核心方法论论文名，定位模型内部计算图（computational graph）的技术

## 相关概念

- concepts/mechanistic-interpretability — 本文核心研究范式，特征→回路→模型行为三层分析
- concepts/computational-circuits — 本文新建，模型内部因果计算路径
- concepts/faithful-reasoning — 本文新建，chain-of-thought真实性验证
- concepts/rag-hallucination — 幻觉机制的内部视角（本文补充了机理解释）
- concepts/agent-containment — 越狱案例提供了安全机制研究的内部证据
- concepts/eval-awareness — 与推理忠实性问题相关：模型是否真的在推理

## 相关实体

- entities/anthropic — 研究发布方，可解释性是其AI安全核心投资方向之一
- entities/claude-3-5-haiku — 主要研究对象，10类核心行为深度解剖
