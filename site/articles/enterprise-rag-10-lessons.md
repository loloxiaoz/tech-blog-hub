---
title: "企业级 RAG 系统实战（2万+文档）：10 个项目踩过的坑"
org: "RAG 研究"
date: 2025-10-11
source_url: "https://zhuanlan.zhihu.com/p/1960251424324682438"
tags: ["Eval/评测", "RAG/检索", "开源模型"]
summary: "评分维度：文本提取质量（50%）+ 格式一致性（30%）+ 表格完整性（20%），采样前 3 页评估。"
summary_zh: "评分维度：文本提取质量（50%）+ 格式一致性（30%）+ 表格完整性（20%），采样前 3 页评估。"
summary_en: ""
---



# 企业级 RAG 系统实战（2万+文档）：10 个项目踩过的坑

## 基本信息

- **背景**：在受监管行业（制药、金融、法律）为中型企业（100-1000人）构建 10+ 个 RAG 系统
- **文档规模**：1万~5万份，来自 SharePoint 或 2005 年的文档管理系统
- **核心论断**：企业 RAG = 70% 工程 + 20% 领域知识 + 10% 模型

## 五大核心教训

### 1. 文档质量检测优先（最大发现）

> "This single change fixed more retrieval issues than any embedding model upgrade."

文档需要先**分级路由**再处理：

| 等级 | 分数 | 处理方式 |
|------|------|---------|
| Clean | 80+ | 完整层级化处理 |
| Decent | 50-80 | 基础分块 + 清理 |
| Garbage | <50 | 固定分块 + 人工复查标记 |

评分维度：文本提取质量（50%）+ 格式一致性（30%）+ 表格完整性（20%），采样前 3 页评估。

详见 concepts/document-quality-scoring

### 2. 元数据架构比 Embedding 模型更重要

花了 40% 开发时间在元数据，ROI 最高。
建议用**关键词匹配**（不是 LLM）提取元数据：
- 查询包含"FDA" → 过滤 `regulatory_category: "FDA"`
- 查询提到"儿科" → 应用患者群体过滤器

领域专用元数据示例：
- 制药：文档类型、药物分类、患者人口统计、监管类别、治疗领域
- 金融：时间周期、财务指标、业务部门、地理区域

详见 concepts/metadata-design

### 3. 混合检索是必须的

语义搜索在专业领域失败率 **15-20%**（不是大家以为的 5%）。
主要失败模式：
- 缩写混淆（"CAR" = 嵌合抗原受体 OR 计算机辅助放射学）
- 精确技术查询（表格特定行的数值）
- 交叉引用链（文档间互引关系）

详见 concepts/hybrid-retrieval

### 4. 表格处理是关键

> "If you can't handle tabular data, you're missing half the value."

处理方式：独立流程 + 双重 Embedding（结构化数据 + 语义描述）。

### 5. 基础设施决定成败

最大挑战：多并发用户的资源竞争。解法：信号量限制并发 + 队列管理。
选型建议：Qwen QWQ-32B 量化到 4-bit 只需 24GB VRAM，比 GPT-4o 便宜 85%。

## 四大工程要点（含代码）

### 置信度驱动的检索路由
```
初始段落级检索
  score >= 0.85 → 段落级足够
  0.70-0.85 + 有精确关键词 → 切换句子级
  0.50-0.70 → 下钻句子级
  < 0.50 → 降级关键词搜索兜底
```

### 层级化分块
Document（2048）→ Section（1024）→ Paragraph（512）→ Sentence（128）
查询复杂度决定检索层级，宽泛问题用 Paragraph，精确问题用 Sentence。

## 相关概念

- concepts/document-quality-scoring — 文档质量评分路由
- concepts/metadata-design — 元数据架构设计
- concepts/hybrid-retrieval — 混合检索
- concepts/chunking — 层级化分块策略
