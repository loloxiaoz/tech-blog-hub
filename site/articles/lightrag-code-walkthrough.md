---
title: "LightRAG 技术框架解读（代码级）"
org: "RAG 研究"
date: 2024-12-19
source_url: "https://zhuanlan.zhihu.com/p/13261291813"
tags: ["RAG/检索"]
summary: "LightRAG 使用三种独立存储，各司其职："
summary_zh: "LightRAG 使用三种独立存储，各司其职："
summary_en: ""
---



# LightRAG 技术框架解读（代码级）

## 基本信息

- **性质**：LightRAG 源码级实现解析，含完整代码示例和 I/O 示例
- **赞同数**：213（技术社区高质量文章）
- **补充定位**：sources/lightrag-paper 和 sources/graphrag-lightrag-advanced 讲原理，本文讲**代码如何实现**

## 三层存储架构

LightRAG 使用三种独立存储，各司其职：

| 存储类型 | 默认实现 | 存储内容 |
|---------|---------|---------|
| **KV 存储** | JsonKVStorage | full_docs（原始文档）、text_chunks（分块文本） |
| **向量存储** | NanoVectorDBStorage | chunks_vdb（文本块）、entities_vdb（实体）、**relationships_vdb**（关系） |
| **图存储** | NetworkXStorage | chunk_entity_relation_graph（实体关系图） |

关键细节：`relationships_vdb` 独立于 `entities_vdb`——关系有自己的向量索引，内容为 `keywords + src_id + tgt_id + description` 的拼接。这解释了双层检索的底层机制。

## 知识库构建流程（6步）

### 1. 文档摄入与分块
```python
# 默认分块参数
chunk_token_size: int = 1200
chunk_overlap_token_size: int = 100
```
同一文本同时构建**普通向量库**（chunks_vdb）和**知识图谱**，两条路并行。

### 2. LLM 实体关系提取（核心步骤）

使用预定义的 `entity_extraction` Prompt 模板，输出格式：
```
("entity"<|>"苹果公司"<|>"organization"<|>"全球知名科技公司")##
("relationship"<|>"史蒂夫·乔布斯"<|>"苹果公司"<|>"联合创始人"<|>"创立,领导"<|>1.0)##
```

**Gleaning 多轮提取**：`entity_extract_max_gleaning` 控制轮数（默认 1），LLM 自判断是否继续（返回 "yes"/"no"）。这是确保实体不遗漏的关键机制。

### 3. 节点合并规则
- **描述**：多次出现的实体，描述用 `<SEP>` 分隔拼接
- **来源**：source_id 同样用 `<SEP>` 拼接（保留来源溯源）

```
merged_node = {
    "description": "全球知名科技公司<SEP>市值超过3万亿美元的科技巨头",
    "source_id": "chunk-3a4b5c<SEP>chunk-6d7e8f"
}
```

### 4. 边合并规则
- **描述**：用 `<SEP>` 拼接
- **关键词**：用 `<SEP>` 拼接
- **权重**：**累加**（不是取最大值或平均值）

```
merged_edge = {
    "description": "联合创始人<SEP>担任CEO",
    "weight": 1.8,  # 0.8 + 1.0 累加
}
```

### 5. 向量索引更新
- **entities_vdb**：存 `entity_name + description`（用于实体相似度检索）
- **relationships_vdb**：存 `keywords + src_id + tgt_id + description`（用于关系相似度检索）

## 检索流程（关键机制）

### 关键词提取：双层检索的真正入口

`kg_query` 首先调用 LLM 提取两类关键词：

```python
# LLM 输出示例
{
    "high_level_keywords": ["创立", "领导", "公司历史"],  # 用于 Global 模式
    "low_level_keywords": ["苹果公司", "创始人"]          # 用于 Local 模式
}
```

**映射关系**：
- `low_level_keywords` → 搜索 `entities_vdb` → **Local 模式**（具体实体检索）
- `high_level_keywords` → 搜索 `relationships_vdb` → **Global 模式**（关系/主题检索）
- **Hybrid 模式** = 同时执行 Local + Global，然后 `combine_contexts`

### LLM 接收的上下文格式（三段 CSV）

```
-----Entities-----
```csv
id,entity,type,description,rank
0,苹果公司,organization,全球知名科技公司,5
```
-----Relationships-----
```csv
id,source,target,description,keywords,weight,rank
0,史蒂夫·乔布斯,苹果公司,联合创始人,创立/领导,1.0,1
```
-----Sources-----
```csv
id,content
0,苹果公司由史蒂夫·乔布斯和沃兹尼亚克在1976年创立。
```
```

**`rank` 字段**：实体/关系在图中的连接度（degree），用于排序。连接越多的实体排名越高。

### 缓存机制
缓存键 = `compute_args_hash(query_param.mode, query)`，模式（local/global/hybrid）是 cache key 的一部分，同一查询不同模式会分别缓存。

## 关键实现洞见

| 机制 | 实现方式 | 设计意图 |
|------|---------|---------|
| 双层检索 | hl_keywords → relationships_vdb；ll_keywords → entities_vdb | 用关键词类型区分检索层级，而非维护两个独立图谱 |
| 实体去重 | 描述用 `<SEP>` 拼接，weight 累加 | 不丢失任何来源信息，同时合并重复节点 |
| Gleaning | LLM 自判断是否继续提取 | 自适应多轮提取，不依赖固定轮数 |
| 上下文格式 | 三段 CSV（Entities + Relationships + Sources） | 结构化输入，让 LLM 能区分实体信息、关系信息和原文 |
| 关系向量化 | `keywords + src_id + tgt_id + description` | 关键词是检索关系的主要入口，description 提供补充语义 |

## 相关概念

- concepts/lightrag — LightRAG 概念层（本文是其代码实现）
- sources/lightrag-paper — LightRAG 原始论文
- sources/graphrag-lightrag-advanced — GraphRAG vs LightRAG 选型对比
