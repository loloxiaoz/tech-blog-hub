---
title: "MemOS: A Memory OS for AI System"
org: "记忆系统"
date: 2026-05-10
source_url: ""
tags: ["Eval/评测", "RAG/检索"]
summary: "现有 LLM 记忆方案（参数记忆 + RAG）存在系统性缺口：既无法统一管理记忆生命周期，也无法在不同记忆形态间迁移和融合。"
summary_zh: "现有 LLM 记忆方案（参数记忆 + RAG）存在系统性缺口：既无法统一管理记忆生命周期，也无法在不同记忆形态间迁移和融合。"
summary_en: ""
---



# MemOS: A Memory OS for AI System

**来源**：`raw/MEMOS.pdf`
**arXiv**：2507.03724v4（2025-12-03）
**作者**：Zhiyu Li 等（MemTensor + 多所高校）
**项目**：https://memos.openmem.net
**代码**：https://github.com/MemTensor/MemOS

---

## 核心主张

现有 LLM 记忆方案（参数记忆 + RAG）存在系统性缺口：既无法统一管理记忆生命周期，也无法在不同记忆形态间迁移和融合。

MemOS 的类比：**记忆 = OS 资源**。就像操作系统统一调度 CPU/RAM/I/O，MemOS 统一调度 LLM 的三种记忆形态。

---

## 记忆类型三分框架

| 类型 | 存储介质 | 特点 | 示例 |
|------|---------|------|------|
| **明文记忆（Plaintext）** | 外部文本 | 可读可编辑，RAG 方式检索 | 对话摘要、用户偏好 |
| **激活记忆（Activation）** | KV-Cache | 推理阶段存在，高速但不持久 | 当前会话中间状态 |
| **参数记忆（Parameter）** | 模型权重 | 最持久，更新成本高 | 预训练/微调知识 |

**MemOS 的核心工程价值**：支持三种记忆形态之间的**无缝转换**——如将多次对话中的用户规则从明文记忆压缩进参数记忆（LoRA 适配器）。

---

## MemCube：最小可调度单元

```
MemCube = 内容 + 元数据
元数据包括：
  - 来源（Provenance）：这条记忆从何而来
  - 版本（Versioning）：记忆的演化历史
  - 权限（Permissions）：谁可以读/写/迁移
  - 生命周期标签：激活/归档/过期
```

MemCube 可组合、可迁移、可融合——多个 MemCube 可合并为更高层次的抽象记忆。

---

## 四大系统挑战（现有方案未解决）

1. **长程依赖建模**：上下文窗口有限，跨多轮或多阶段的指令状态无法维持
2. **知识演化适配**：RAG 是无状态补丁机制，无法版本管理、无法退役旧知识
3. **个性化与多角色支持**：各会话重置为空白状态，无持久"记忆痕迹"；现有工具（ChatGPT/Claude）记忆容量有限，更新不透明
4. **跨平台记忆迁移**：记忆被锁在特定平台实例，形成"记忆孤岛"（ChatGPT 的想法带不进 Cursor）

---

## 三核心能力

- **可控性（Controllability）**：全生命周期管理——记忆的创建、激活、融合、归档、过期。多级权限控制，用户可见可审计
- **可塑性（Plasticity）**：记忆切片、标签、层级映射、上下文绑定——模型可为不同任务激活不同"记忆视图"，角色切换时快速认知适应
- **可演化性（Evolvability）**：三种记忆形态之间动态转换和统一调度——如将长期对话中的用户偏好从明文压缩进 LoRA 参数

---

## SOTA 基准结果

MemOS-1031 在所有评测上均超越 MIRIX、Mem0、Zep、Memobase、MemU、Supermemory：

| 基准 | MemOS 得分 |
|------|----------|
| PreFEval (0-turn) | **77.2** |
| PreFEval (10-turn) | **71.9** |
| PersonaMem | **61.2** |
| LongMemEval | **77.8** |
| LoCoMo | **75.8** |

---

## LLM 记忆系统四阶段演进（MemOS 总结）

| 阶段 | 特征 | 代表工作 |
|------|------|---------|
| Stage 1：定义与探索 | 分类记忆类型，分析机制 | 短期/长期记忆分类论文 |
| Stage 2：类人记忆开发 | 仿神经科学，弥补性能缺口 | HippoRAG、Titans |
| Stage 3：工具化记忆管理 | CRUD API，但仍是孤立操作 | Mem0、Zep、Memobase |
| **Stage 4：系统化记忆治理** | OS 级资源调度，统一表示与生命周期 | **MemOS** |

---

## 相关 Wiki 页面

- concepts/memory-systems — MemOS 提供了最完整的记忆系统分类框架
- concepts/context-engine — MemOS 是 Context Engine 在系统层面的具体实现方向
