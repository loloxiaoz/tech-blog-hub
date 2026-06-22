---
title: "Introducing Contextual Retrieval"
org: "Anthropic"
date: 2024-09-19
source_url: "https://www.anthropic.com/engineering/contextual-retrieval"
tags: ["Eval/评测", "RAG/检索"]
summary: "Claude Haiku 的 Chunk 上下文生成 Prompt："
summary_zh: ""
summary_en: "Claude Haiku 的 Chunk 上下文生成 Prompt："
---



# Introducing Contextual Retrieval

## 核心观点

**传统 RAG 的根本缺陷是上下文丢失**。文档分块后，单个 Chunk 失去了定位信息（如"本段来自 ACME 公司 2023 年 Q2 财报，上季度营收为 3.14 亿美元"），导致检索阶段无法精准匹配用户查询，即使内容相关也会被漏掉。

**Contextual Retrieval 的解法是在预处理阶段为每个 Chunk 自动添加上下文说明**。使用 Claude Haiku 为每个 Chunk 生成 50-100 token 的简短上下文描述，前置到 Chunk 内容，使每个 Chunk 具备自定位能力。该上下文前缀同时用于向量嵌入（Contextual Embeddings）和 BM25 索引（Contextual BM25）。

**实验数据证明各优化效果可叠加**。在多知识领域（代码库、小说、ArXiv 论文、科学论文）的系统性实验中：

- Contextual Embeddings：top-20 检索失败率 5.7% → 3.7%（降低 35%）
- Contextual Embeddings + Contextual BM25：5.7% → 2.9%（降低 49%）
- 全套方案（Contextual Embeddings + Contextual BM25 + Reranking）：5.7% → 1.9%（降低 67%）

**Prompt Caching 是该方案经济可行的关键**。生成每个 Chunk 的上下文需要传入整份文档，如果每次都全量传入成本极高。Claude 的 Prompt Caching 允许文档只上传一次，后续 Chunk 的上下文生成均引用缓存，将每百万 Document Token 的一次性处理成本控制在 $1.02。

**知识库大小决定最优策略选择**。知识库小于 200K tokens（约 500 页）时，直接将全部内容放入 Prompt 配合 Prompt Caching 是最简单且高效的方案（延迟降低 >2x，成本降低最多 90%）；更大规模知识库才需要 Contextual Retrieval。

## 关键术语

- **Contextual Retrieval**：Anthropic 提出的 RAG 检索增强方法，通过 LLM 为 Chunk 自动生成上下文前缀，同时提升向量检索和 BM25 精度。
- **Contextual Embeddings**：Contextual Retrieval 的子技术，为每个 Chunk 添加上下文后再进行向量嵌入，使语义向量携带定位信息。
- **Contextual BM25**：Contextual Retrieval 的子技术，在 BM25 索引中使用含上下文前缀的 Chunk，提升精确词匹配的精度。
- **BM25（Best Matching 25）**：基于 TF-IDF 改进的词法检索算法，通过考虑文档长度和词频饱和函数解决关键词精确匹配问题，对精确技术词汇（错误码、型号）尤为有效。
- **Reranking（重排序）**：在初始检索（top-N）后，使用独立的排序模型对候选 Chunk 依据查询相关性进行精排，筛选出最终 top-K 个 Chunk 传入 LLM。
- **Prompt Caching**：Claude API 特性，允许将长 Prompt（含文档）缓存于服务端，后续调用直接引用缓存，减少重复传输成本。本文中降低 Contextual Retrieval 预处理成本的核心机制。
- **recall@20**：检索评估指标，衡量相关文档被包含在 top-20 结果中的比例；本文用「1 - recall@20」即失败率作为主要评估指标。
- **Rank Fusion（排名融合）**：将向量检索和 BM25 结果合并去重的技术，常用 RRF（Reciprocal Rank Fusion）算法。

## 实现细节

Claude Haiku 的 Chunk 上下文生成 Prompt：

```
<document>
{{WHOLE_DOCUMENT}}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{{CHUNK_CONTENT}}
</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
```

**实现注意事项**：
1. Chunk 边界（大小、重叠）影响检索效果，需针对业务调优
2. Gemini 和 Voyage 是实验中表现最优的 Embedding 方案
3. 可针对特定领域定制上下文生成 Prompt（如加入专有词汇表）
4. 传入 top-20 Chunk 比 top-10 或 top-5 效果更好，但并非越多越好
5. 始终运行 Eval 以验证效果

## 相关概念

- concepts/rag — RAG 基础架构，Contextual Retrieval 是对检索阶段的增强
- concepts/hybrid-retrieval — 混合检索（向量 + BM25），Contextual BM25 是其上下文增强变体
- concepts/context-window — Prompt Caching 与上下文窗口成本的关系
- concepts/context-engineering — 上下文工程方法论，RAG 是其核心组件
- concepts/memory-systems — 记忆系统与 RAG 同源，共同构成 Agent 数据底座

## 相关实体

- entities/anthropic — 本文作者所在机构，发布 Contextual Retrieval 方法
