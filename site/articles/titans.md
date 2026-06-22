---
title: "Titans: Learning to Memorize at Test Time"
org: "记忆系统"
date: 2026-05-10
source_url: ""
tags: ["RAG/检索", "长上下文"]
summary: "Transformer 因二次复杂度难以处理超长上下文；线性 Transformer（状态空间模型）虽可扩展，但压缩历史会丢失信息。两者在记忆方面存在根本性权衡。"
summary_zh: "Transformer 因二次复杂度难以处理超长上下文；线性 Transformer（状态空间模型）虽可扩展，但压缩历史会丢失信息。两者在记忆方面存在根本性权衡。"
summary_en: ""
---



# Titans: Learning to Memorize at Test Time

**来源**：`raw/Learning to Memorize At Test Time.pdf`
**arXiv**：2501.00663v1（2024-12-31）
**作者**：Ali Behrouz, Peilin Zhong, Vahab Mirrokni（Google Research）

---

## 核心问题

Transformer 因二次复杂度难以处理超长上下文；线性 Transformer（状态空间模型）虽可扩展，但压缩历史会丢失信息。两者在记忆方面存在根本性权衡。

Titans 的方案：设计一个**神经长期记忆模块**，可在测试时主动学习什么值得记住，与 Transformer 注意力互补。

---

## 核心创新："惊奇度"驱动记忆

**惊奇度（Surprise）**：当前输入对联想记忆损失的梯度大小。

- 违反预期的信息（高梯度） → 更值得记住
- 符合预期的信息（低梯度） → 不值得额外存储

这与认知科学一致：人类对"意外"信息记忆更深刻。

**衰减机制（Decaying）**：按记忆大小与数据惊奇度的比例衰减，等价于现代循环网络的遗忘机制的泛化形式。

**并行化**：等价于用 mini-batch 梯度下降 + 动量 + 权重衰减训练元神经网络，可高效并行训练。

---

## 三组件架构

| 组件 | 类比 | 功能 | 技术实现 |
|------|------|------|---------|
| **Core** | 短期记忆 | 主数据流，精确处理当前上下文 | Attention（有限窗口）|
| **Long-term Memory** | 长期记忆 | 主动记忆历史，按惊奇度选择性保留 | 神经记忆模块（可学习参数）|
| **Persistent Memory** | 元记忆 | 与输入无关的任务知识 | 可学习的固定参数集 |

**三种集成变体**：
- **MAC**（Memory as Context）：记忆注入为上下文
- **MAL**（Memory as Layer）：记忆作为网络层
- **MAG**（Memory as Gate）：记忆作为门控分支

---

## 实验结果

- 超越所有现代循环模型（含 Mamba、RWKV 等）
- 超越使用相同上下文窗口的 Transformer
- 与使用全部上下文的 Transformer 在针刺大海捞针（Needle-in-haystack）任务上有竞争力
- **可扩展到 2M+ token 上下文窗口**，Transformer 在该规模下无法运行

---

## 关键洞察

- **"记忆是多个系统的联合"**（Cowan 2008）：Titans 用三组件分别对应短期/长期/元记忆，比单一机制更符合人类神经科学
- 注意力 = 短期记忆（精确但有长度限制）；神经记忆 = 长期记忆（有损但可扩展）
- 惊奇度机制使记忆**主动选择**而非被动压缩——这是与 LSTM/SSM 等方法的本质区别
- 测试时学习（Test-time learning）：记忆模块在推理阶段持续更新参数

---

## 相关 Wiki 页面

- concepts/memory-systems — Titans 提供神经架构层面的长期记忆实现视角
- concepts/long-context-vs-rag — Titans 代表了超长上下文的第三条路（神经记忆）
