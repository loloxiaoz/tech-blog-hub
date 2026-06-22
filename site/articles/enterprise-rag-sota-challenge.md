---
title: "企业RAG挑战赛 SOTA 方案（赢得全部类别）"
org: "RAG 研究"
date: 2025-06-10
source_url: "https://zhuanlan.zhihu.com/p/1915060185329796001"
tags: ["RAG/检索", "推理模型", "开源模型"]
summary: "→ 分块（300 Token，50 Token overlap）"
summary_zh: ""
summary_en: "→ 分块（300 Token，50 Token overlap）"
---



# 企业RAG挑战赛 SOTA 方案（赢得全部类别）

## 基本信息

- **任务**：基于 100 份公司年度报告（PDF）构建问答系统，2.5 小时内完成解析建库并回答 100 个随机问题
- **结果**：赢得比赛全部类别
- **开源**：github.com/IlyaRice/RAG-Challenge-2

## 获奖系统架构

```
PDF 解析（Docling）
  → 文本清洗（正则规则）
  → 表格序列化（HTML → 行级子句）
  → 分块（300 Token，50 Token overlap）
  → 向量化（text-embedding-3-large，per-document FAISS）
  → 混合检索（向量检索 Top-30 → 父页面扩展 → LLM 重排 Top-10）
  → 查询路由（数据库路由 + 提示路由 + 复合查询分解）
  → CoT + 结构化输出生成
```

## 核心技术要点

### 解析：Docling + 定制改造
- 比赛中表现最好的解析器
- 作者 hack 了 Docling 源码，定制输出带全部元数据的 JSON
- 关键配置：GPU 加速（4090），40分钟内解析 100 份文档（约 15000 页）

### 分块：300 Token + 父页面检索
- 小块（300 Token）用于精准语义匹配
- 检索结果作为"指针"，实际输入 LLM 的是**完整父页面**
- 每份文档独立建一个 FAISS 索引（避免跨公司数据混淆）

### 表格序列化（关键创新）
大型表格中水平/垂直标题相距太远，语义割裂。
解法：将表格转为一组**上下文独立的子句**：
```
subject_core_entity: "Shareholders' equity"
information_block: "Shareholders' equity for years 2012-2022: ..."
```
*注意：最终获奖方案并未使用表格序列化（Docling 解析已足够，额外文本反而降低信噪比）*

### LLM 重排序（核心替代交叉编码器）
- 用 GPT-4o-mini 对候选页面打 0-1 相关性分数，同时返回 reasoning
- 每次请求发送 3 页（提高一致性、降低成本）
- 加权平均：vector_weight=0.3, llm_weight=0.7
- 成本：每个问题不到 1 美分

### 查询路由
1. **数据库路由**：用公司名从 100 个独立 FAISS 索引中定位目标库（搜索空间缩小 100x）
2. **提示路由**：根据答案类型（int/float/bool/str/list）选对应提示（规则越少 LLM 遵守越好）
3. **复合查询分解**：比较型问题（苹果 vs 微软收入）分解为子问题，分别检索再合并

### CoT + 结构化输出
```
step_by_step_analysis → reasoning_summary → relevant_pages → final_answer
```
关键：通过 one-shot 示例教会 LLM 从不同角度分析，防止"伪造推理"（直接给答案然后追溯性证明）。

## 意外发现
- BM25 混合检索：在这个场景里不仅没有提升，反而略有下降（向量检索已足够，不通用）
- 表格序列化：精心设计但最终没用，Docling 解析效果足够好
- Llama 3.3 70b 表现仅比 o3-mini 低几个点

## 相关概念

- concepts/reranking — LLM 重排是本文核心贡献
- concepts/hybrid-retrieval — 混合检索（本文中效果不稳定）
- concepts/chunking — 小块检索 + 父页面上下文模式
- concepts/ingestion-pipeline — 解析流水线

## 相关实体

- entities/docling — 竞赛最优解析器
