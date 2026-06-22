---
title: "From RAG to Memory: Non-Parametric Continual Learning for Large Language Models"
org: "记忆系统"
date: 2026-05-10
source_url: ""
tags: ["Eval/评测", "RAG/检索"]
summary: "提出记忆能力的三维评测框架，揭示现有 RAG 系统的结构性缺陷，并提出 HippoRAG 2 解决联想性维度的不足。"
summary_zh: "提出记忆能力的三维评测框架，揭示现有 RAG 系统的结构性缺陷，并提出 HippoRAG 2 解决联想性维度的不足。"
summary_en: ""
---



# From RAG to Memory: Non-Parametric Continual Learning for Large Language Models

**来源**：`raw/From RAG to Memory.pdf`
**arXiv**：2502.14802v2（2025-06-19）
**作者**：Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, Yu Su（Ohio State + UIUC）
**发表**：ICML 2025
**代码**：https://github.com/OSU-NLP-Group/HippoRAG

---

## 核心贡献

提出记忆能力的**三维评测框架**，揭示现有 RAG 系统的结构性缺陷，并提出 HippoRAG 2 解决联想性维度的不足。

---

## 记忆三维度

| 维度 | 定义 | 代表任务 | 标准 RAG |
|------|------|---------|---------|
| **事实记忆（Factual）** | 检索离散的可核实事实 | NaturalQuestions, PopQA | ✅ 已经够用 |
| **意义构建（Sense-making）** | 理解大规模、复杂语篇事件 | NarrativeQA | ⚠️ 一般 |
| **联想性（Associativity）** | 跨不相邻文档连接多跳事实 | MuSiQue, 2Wiki, HotpotQA | ❌ 结构性失败 |

**根本原因**：向量检索每次独立运行，无法跨片段建立多跳连接——这正是人类联想记忆的核心能力。

---

## HippoRAG 2 架构

仿神经生物学的三组件设计（来自 HippoRAG 1 延续）：

| 组件 | 类比人脑 | 功能 |
|------|---------|------|
| LLM 新皮质 | 海马-新皮质接口 | 从查询提取实体，判断何时检索无效 |
| 知识图谱（KG）| 海马体 | 用 OpenIE 构建，存储段落→KG三元组 |
| 检索编码器 | 海马旁区 | 负责同义检测，连接 LLM 与 KG |

**关键改进（vs HippoRAG 1）**：
- 更深的段落集成：KG 检索时直接引用相关段落
- 在线 LLM 使用：检索过程中实时判断 KG 三元组是否相关（减少噪声）
- 个性化 PageRank（PPR）：在 KG 上计算相关性分布，自然支持多跳

---

## 实验结果

HippoRAG 2 在全部基准类别上均胜出：

| 任务类型 | vs 标准 RAG | vs GraphRAG |
|---------|-----------|-----------|
| 联想性 | **+7%** 平均 | 显著优于 |
| 事实记忆 | 无退化 | 优于 |
| 意义构建 | 轻微提升 | 优于 |

此前问题：所有结构增强型 RAG（GraphRAG、LightRAG、RAPTOR）在自己最擅长的维度外都出现性能下降，HippoRAG 2 是首个在三维度均无退化的方案。

---

## 关键洞察

- **联想性缺失是 RAG 的结构性问题**，不是调参能解决的，需要图结构 + PageRank
- LLM 在线判断 KG 三元组相关性：引入的噪声更少（GraphRAG/LightRAG 离线构图，噪声难以去除）
- 非参数化持续学习：知识更新不需要重新训练模型，只需更新 KG

---

## 相关 Wiki 页面

- concepts/memory-systems — 三维记忆框架补充了记忆评测维度
- concepts/graph-rag — HippoRAG 2 是 GraphRAG 类方案的最新进展
- concepts/lightrag — 对比：LightRAG 离线建图 vs HippoRAG 2 在线 LLM 判断
