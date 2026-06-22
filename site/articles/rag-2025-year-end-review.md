---
title: "从 RAG 到 Context：2025 年 RAG 技术年终总结"
org: "RAG 研究"
date: 2026-01-05
source_url: "https://zhuanlan.zhihu.com/p/1984948557493592394"
tags: ["Agent", "Eval/评测", "RAG/检索", "MCP", "多模态", "长上下文"]
summary: "RAG 没有消亡，而是从\"检索增强生成\"的具体技术，升维为以智能检索为核心的上下文引擎（Context Engine），成为所有 LLM 应用的统一数据底座。"
summary_zh: "RAG 没有消亡，而是从\"检索增强生成\"的具体技术，升维为以智能检索为核心的上下文引擎（Context Engine），成为所有 LLM 应用的统一数据底座。"
summary_en: ""
---



# 从 RAG 到 Context：2025 年 RAG 技术年终总结

## 基本信息

- **作者**：entities/infiniflow 团队
- **发布**：2026-01-05（知乎）
- **性质**：行业年终综述 + 产品视角（RAGFlow 作者出品，有一定立场倾向）

## 核心主张（一句话）

RAG 没有消亡，而是从"检索增强生成"的具体技术，升维为以**智能检索**为核心的**上下文引擎（Context Engine）**，成为所有 LLM 应用的统一数据底座。

## 五大论点

### 1. 长上下文 vs RAG：争论已有结论
- 长上下文 ≠ RAG 替代品，两者成本差约 2 个数量级
- KV Cache 方案成本仍比 RAG 高一个数量级，且有架构约束
- 无索引 RAG（Grep）仅适合结构化代码库，不适合企业非结构化数据
- **结论**：协同而非对立——RAG 精准检索，长上下文完整容纳
- 详见 concepts/long-context-vs-rag

### 2. RAG 效果改进：解耦 Search 与 Retrieve
- 根本矛盾：单一 Chunk 同时承担"语义匹配（需小）"和"上下文理解（需大）"
- 解决方案：离线建树状摘要（TreeRAG）或知识图谱（GraphRAG），在线先小块定位再大块组装
- 详见 concepts/tree-rag、concepts/graph-rag、concepts/chunking

### 3. RAG → 企业数据底座（PTI Pipeline）
- RAG 引擎需要强大的 Ingestion Pipeline，类比结构化数据的 ETL
- PTI = Parse（解析多模态文档） + Transform（LLM 语义增强） + Index（混合索引）
- Transform 阶段是价值核心，决定数据被"理解"的深度
- 详见 concepts/ingestion-pipeline

### 4. Agent 时代：Context Engineering 的三类检索
- 上下文 = 领域知识（RAG）+ 工具信息（Tool Retrieval）+ 会话状态（Memory）
- MCP 解决"如何调用工具"，Tool Retrieval 解决"选哪个工具"
- Memory 系统与 RAG 技术同源，数据来源不同
- 详见 concepts/context-engineering、concepts/tool-retrieval、concepts/memory-systems

### 5. 多模态 RAG：理论清晰，工程瓶颈尚未突破
- ColPali 路线（延迟交互 + 多向量）理论优势明确
- 工程瓶颈：1页图像 ≈ 512KB 张量，百万页文档库 → TB 级索引
- 两条出路：张量量化压缩、Token 剪枝
- 预计 2026 年逐渐成熟
- 详见 concepts/multimodal-rag、concepts/late-interaction

## 关键数据点

| 对比项 | 数值 |
|--------|------|
| 长上下文 vs RAG 成本差 | ~100x（2个数量级） |
| KV Cache vs RAG 成本差 | ~10x（1个数量级） |
| ColPali 默认每页 Token 数 | 1024 |
| ColPali 每页张量存储（float32, dim=128） | ~512 KB |
| Tool Retrieval BM25 召回 | 作为强 Baseline |

## 相关实体

- entities/ragflow — 本文作者产品，文中多处案例来自 RAGFlow 实践
- entities/infiniflow — RAGFlow 背后公司
- entities/theory-ventures — "Context Platform" 概念提出者
- entities/alayadb — KV Cache 数据库，文中作为对比案例
- entities/colpali — 多模态 RAG 核心模型
- entities/deepdoc — RAGFlow 的文档解析组件
- entities/mcp — 工具调用协议，文中澄清其边界

## 注意事项

本文由 RAGFlow 团队出品，对 RAGFlow 自身的评价偏正面，对竞争路线（KV Cache、纯 Grep）的分析较为批判。结论总体可信，但技术细节应结合其他来源交叉验证。
