---
title: "Open-sourcing circuit tracing tools（开源电路追踪工具）"
org: "Anthropic"
date: 2025-05-29
source_url: "https://www.anthropic.com/research/open-sourcing-circuit-tracing"
tags: ["可解释性", "安全/对齐", "代码模型", "开源模型"]
summary: "原文：https://www.anthropic.com/research/open-source-circuit-tracing"
summary_zh: ""
summary_en: "原文：https://www.anthropic.com/research/open-source-circuit-tracing"
---



# Open-sourcing circuit tracing tools（开源电路追踪工具）

原文：https://www.anthropic.com/research/open-source-circuit-tracing

代码库：https://github.com/safety-research/circuit-tracer

## 核心观点

**归因图是揭示模型内部推理的核心工具。** Anthropic 将其可解释性研究方法论具体化为"归因图"（Attribution Graph）——一种部分展现模型从输入到输出内部决策路径的图结构。这不是黑盒探针，而是对"模型如何一步步得出答案"的机理追踪。

**开源形成完整研究闭环。** 发布的 circuit-tracer 库支持三类核心操作：（1）追踪电路，在 Gemma-2-2b、Llama-3.2-1b 等开放权重模型上生成归因图；（2）通过 Neuronpedia 前端可视化、标注、分享图谱；（3）修改特征值验证假设，观察模型输出如何随内部状态变化。三者合一构成"假设→实验→验证"的科学研究循环。

**已验证多步推理与多语言表示。** 研究团队用该工具研究了 Gemma-2-2b 的多步推理链路和跨语言表示机制，发现语言模型内部存在可识别的、跨语言共享的功能性电路结构。Demo Notebook 中提供了具体分析案例。

**能力进步已超越内部理解速度，开源是追赶策略。** Dario Amodei 指出当前 AI 能力进步远超人类对 AI 内部机制的理解，这一差距本身构成安全风险。开源工具包是通过扩大研究社区来加速缩小这一差距的战略选择。

**Anthropic Fellows + Decode Research 联合生产模式。** 该工具由 Anthropic Fellows 项目研究员 Michael Hanna 和 Mateusz Piotrowski 主导开发，Decode Research 负责 Neuronpedia 集成，底层 Transcoder 来自 Google GemmaScope 项目，展示了跨机构可解释性研究协作模式。

## 关键术语

- **归因图（Attribution Graph）**：图结构，节点为模型内部特征或注意力头，边为归因权重，展示特定输出的内部决策路径
- **电路追踪（Circuit Tracing）**：识别神经网络中执行特定功能的子网络（电路）的技术方法，是机理可解释性的核心实验手段
- **机理可解释性（Mechanistic Interpretability）**：研究神经网络内部工作机制的子领域，目标是从机理层面理解模型如何表示和处理信息
- **特征（Feature）**：可解释性研究中，模型内部激活空间中可以被人类概念对应的方向或子空间
- **Transcoder**：将模型中间层激活分解为稀疏可解释特征的组件，GemmaScope 提供了 Gemma-2-2b 的公开 Transcoder
- **Neuronpedia**：Decode Research 运营的可解释性研究平台，提供特征可视化和归因图交互式探索界面
- **Anthropic Fellows**：Anthropic 的研究员项目，由外部研究员在 Anthropic 指导下推进前沿研究

## 相关概念

- concepts/mechanistic-interpretability — 机理可解释性：理解神经网络内部机制的研究领域
- concepts/attribution-graphs — 归因图：电路追踪的核心输出，可视化模型内部决策路径
- concepts/circuit-tracing — 电路追踪：识别执行特定功能子网络的方法

## 相关实体

- entities/anthropic — 本工具开发方，将可解释性定位为安全核心议题
- entities/neuronpedia — Decode Research 运营的可解释性平台，托管交互式图浏览器
- entities/dario-amodei — Anthropic CEO，发文《可解释性研究的紧迫性》提供战略背景
