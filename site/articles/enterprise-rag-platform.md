---
title: "企业级 RAG 中台怎么做：从文档解析到溯源和评测闭环"
org: "RAG 研究"
date: 2026-04-30
source_url: "https://zhuanlan.zhihu.com/p/2033253724131419834"
tags: ["Eval/评测", "RAG/检索"]
summary: "多源数据接入 → 文档解析 → 数据清洗 → chunk切分 → metadata构建"
summary_zh: "多源数据接入 → 文档解析 → 数据清洗 → chunk切分 → metadata构建"
summary_en: ""
---



# 企业级 RAG 中台怎么做：从文档解析到溯源和评测闭环

## 基本信息

- **定位**：企业 RAG 中台完整架构指南，适合产品经理和工程师视角

## 核心论断

> 企业级 RAG 的上限，很多时候不是由大模型决定的，而是由数据解析、切分、召回和评测闭环决定的。

## 完整链路（一句话总览）

```
多源数据接入 → 文档解析 → 数据清洗 → chunk切分 → metadata构建
→ embedding向量化 → 向量库/关键词索引 → 混合检索 → rerank重排序
→ Prompt组装 → LLM生成 → 答案溯源 → 日志记录 → 评测集/badcase回流
```

## 关键模块详解

### 文档解析分类（地基）
| PDF 类型 | 处理方式 |
|---------|---------|
| 文本型 | 直接抽取文字，保留页码/段落/标题 |
| 扫描型 | OCR + 旋转矫正 + 去噪 + 版面分析 |
| 图文混排 | 文字抽取 + OCR + layout analysis |
| 表格型 | 表格识别 + 单元格合并 + 表头识别 |
| 双栏论文 | 版面识别 + 阅读顺序重排 |

### OCR 能力清单
旋转矫正、倾斜校正、去噪、印章/水印处理、有框/无框表格识别、公式识别、阅读顺序排序、多栏文本处理

### 切分策略选择
| 文档类型 | 推荐切分方式 |
|---------|------------|
| 操作手册 | 按章节 + 步骤切 |
| 合同 | 按条款切 |
| FAQ | 一问一答切 |
| 表格 | 按行/业务块/sheet 切 |
| PPT | 按页 + 标题切 |
| 工单 | 标题+描述+处理+解决方案组合切 |

### 元数据设计（溯源基础）
必须包含：doc_id、chunk_id、file_name、page_number、section_title、source_url、storage_path、start_offset/end_offset、permission、business_tag

### 答案溯源实现路径
```
每个 chunk 保存 metadata
→ 检索结果带 source_id/chunk_id
→ Prompt 中保留 chunk 编号
→ 要求模型按编号引用
→ 答案返回引用列表
→ 前端展示文档名/页码/段落/URL（支持点击跳转原文）
```

### Badcase 回流链路
```
问题记录 → 召回结果记录 → 答案记录 → 人工标注原因
→ 调整切分/metadata/embedding/rerank/prompt → 重新评测
```

Badcase 分类诊断：
| 问题类型 | 可能原因 |
|---------|---------|
| 没召回正确文档 | embedding不合适、chunk切分问题、metadata过滤过严 |
| 召回了但排序靠后 | rerank效果差、融合权重不合理 |
| 召回正确但回答错 | prompt设计、模型幻觉、上下文过长 |
| 引用错误 | chunk metadata缺失、引用编号不稳定 |
| 答案不完整 | chunk太小、缺少父级上下文 |

## 向量数据库选型

| 方案 | 适合场景 |
|------|---------|
| FAISS | 本地轻量，适合原型和小中规模 |
| Milvus | 大规模、分布式、高并发 |
| pgvector | 已有 PostgreSQL 体系 |
| Elasticsearch dense vector | 已有 ES 栈，关键词+向量混合 |
| Qdrant/Weaviate | 独立向量检索服务 |

## 算法中台价值

核心价值：可配置、可视化、可复用、可评测、可持续优化。
没有召回可视化，就无法做 RAG Badcase 分析。

## 相关概念

- concepts/hybrid-retrieval — BM25 + 向量检索混合
- concepts/reranking — 重排序
- concepts/metadata-design — 元数据设计
- concepts/rag-evaluation — 评测与 Badcase 回流
- concepts/ingestion-pipeline — 数据摄入流水线
- concepts/chunking — 切分策略
