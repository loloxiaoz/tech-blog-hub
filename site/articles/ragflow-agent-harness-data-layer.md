---
title: "Agent harness 时代的数据底座：RAGFlow 为何而变"
org: ""
date: 2026-04-28
source_url: "https://zhuanlan.zhihu.com/p/2032559018770683864"
tags: ["Agent", "Eval/评测", "RAG/检索", "Harness工程"]
summary: "Anthropic 最新将 LLM + Harness 统一抽象为 Brain："
summary_zh: ""
summary_en: "Anthropic 最新将 LLM + Harness 统一抽象为 Brain："
---



# Agent harness 时代的数据底座：RAGFlow 为何而变

## 基本信息

- **作者**：entities/infiniflow / entities/ragflow 团队
- **性质**：RAGFlow 战略定位更新，对 Context Engine 方向的阶段性审视（是 sources/rag-2025-year-end-review 的续篇）
- **核心主张**：RAGFlow 的定位从 Context Engine 进一步明确为——**Agent 的数据底座（状态层）**

## 核心架构：Brain / State Layer 分离

Anthropic 最新将 LLM + Harness 统一抽象为 **Brain**：
- **Brain（无状态决策核心）**：负责任务规划与分发，可任意启停
- **状态层（数据底座）**：存储所有持久化状态，独立于 Brain 存在

```
无状态层：Brain（LLM + Harness）
           ↑↓ 调用
状态层  ：数据底座（RAGFlow 所在位置）
           ├── 非结构化文档库
           ├── 结构化数据接口说明
           └── 会话记忆（Memory）
```

这一分离的战略意义：企业无需被特定厂商的 Brain 实现绑定，自主掌控数据基础设施。

详见 concepts/brain-state-separation

## 为什么数据底座必须以 Retrieval 为核心

排除"在数据库上扩展向量检索"方案的理由：

**1. 非结构化文档处理 ≠ 存储+检索**
涉及异构数据源接入、治理、清洗、语义增强，以及动态的检索策略（索引选型、实时补全、语义联想）——这些逻辑无法在数据库内部以封闭方式完成。

**2. 结构化数据无需重复构建**
企业现有系统已承载结构化资产。Agent 真正需要的是这些系统的访问接口 + 配套说明文档（API 参考、调用范例、Skills 最佳实践）。提供强搜索能力的文档元数据，足以帮助 Agent 过滤不符合意图的工具选项。

**3. 会话记忆的双重诉求**
- 作为 harness 的 source of truth：可靠存储与治理
- 为后续行为提供记忆供给：高效检索（但检索控制逻辑在 harness 侧）

**OpenClaw ContextEngine API 示例（简易 Memory Harness）**：
```
assemble()  → 调用 Tools 前准备上下文
compact()   → 上下文过长时压缩
afterTurn() → Tools 执行后持久化消息
```

## Agentic Retrieval 的新特征

### 与传统 IR（人类用户）的根本差异

| 维度 | 传统 IR（人类） | Agentic IR（AI） |
|------|--------------|----------------|
| 请求量级 | 基准 | **高 2 个数量级** |
| 查询轨迹 | 短、离散 | 长、探索式、连续 |
| 用户特征 | 不熟练的搜索者，需要"猜"意图 | 熟练的研究员，但可能"钻牛角尖"，需要"拦" |
| 停止机制 | 人类遇困难自然放弃 | Agent 不会放弃，需要设计截断策略 |

### 新机遇与新挑战

**语义缓存**：同一任务轨迹内查询语义高度相似，但精确文本匹配率极低 → 传统精确缓存失效，语义缓存空间巨大

**停止策略**：Agent 不会自动放弃，需设计无效检索截断机制，防止无限蔓延

**需要重新定义的 IR 概念**：相关性的定义、用户模型、基准测试体系

详见 concepts/agentic-retrieval

## RAGFlow 的具体演进方向

| 方向 | 内容 |
|------|------|
| **Go 语言重写 API 层** | Python 快速迭代后的性能升级，承接 Agentic Retrieval 100x 访问增量 |
| **统一 ContextEngine CLI** | 单一 `search` 命令跨异构数据源检索，降低 harness 接入复杂度 |
| **更丰富的数据处理 Pipeline** | 语义增强深度决定检索上限，持续扩展 |

RAGFlow 1.0 发布后的下一阶段命题：
- Agent 视角下"相关性"如何定义
- 数百次连续调用的累积检索效用评估
- 语义缓存的粒度与策略设计
- 截断/重试机制与 Agent 任务规划的协同

## 注意事项

本文由 RAGFlow 团队出品，对自身产品方向存在立场倾向。Brain/State Layer 的框架描述值得参考，但具体演进时间线和产品承诺需交叉验证。

## 相关概念

- concepts/context-engine — RAGFlow 之前的定位（Context Engine），本文是其进化
- concepts/agentic-retrieval — Agentic Retrieval 新特征（本文新建）
- concepts/brain-state-separation — Brain/State Layer 架构抽象（本文新建）
- concepts/memory-systems — Memory Harness 详细概念
- concepts/rag — RAG 向 Agentic 场景的演进

## 相关实体

- entities/ragflow — 本文作者产品
- entities/infiniflow — 本文作者公司
- entities/openclaw — 文中引用其 ContextEngine API 作为 Memory Harness 示例
