---
title: "Effective context engineering for AI agents"
org: "Anthropic"
date: 2025-09-29
source_url: "https://www.anthropic.com/engineering/context-engineering"
tags: ["Agent", "Claude Code"]
summary: "提示工程聚焦于如何写好提示词，是一次性的文字创作任务。上下文工程关注的是更大的问题：在每次LLM推理时，如何从不断增长的候选信息宇宙中，动态筛选出最优Token集合。区别在于：提示工程是离散的，而上下文工程是迭代的——每次决定传递给模型什么信息时，上下文工程就在发生。"
summary_zh: "提示工程聚焦于如何写好提示词，是一次性的文字创作任务。上下文工程关注的是更大的问题：在每次LLM推理时，如何从不断增长的候选信息宇宙中，动态筛选出最优Token集合。区别在于：提示工程是离散的，而上下文工程是迭代的——每次决定传递给模型什么信息时，上下文工程就在发生。"
summary_en: ""
---



# Effective context engineering for AI agents

## 核心观点

**1. 上下文工程是提示工程的自然演进**

提示工程聚焦于如何写好提示词，是一次性的文字创作任务。上下文工程关注的是更大的问题：在每次LLM推理时，如何从不断增长的候选信息宇宙中，动态筛选出最优Token集合。区别在于：提示工程是离散的，而上下文工程是迭代的——每次决定传递给模型什么信息时，上下文工程就在发生。

**2. 注意力预算（Attention Budget）是上下文工程的根本约束**

Transformer架构使每个Token可以关注上下文中的所有其他Token，形成O(n2)的成对关系。随着上下文增长，模型维护这些关系的能力被稀释。Chroma Research发现的"上下文衰减"（context rot）现象表明：Token数越多，模型从中精确召回信息的能力越低。这是性能梯度而非硬截断，因此必须把上下文视为具有递减边际回报的有限资源。

**3. 有效上下文的四个组件与右海拔原则**

好的上下文工程目标：用最小的高信号Token集，最大化目标行为的发生概率。四个主要组件：系统提示（保持Right Altitude，避免硬编码脆性逻辑，也避免语义模糊的高层指引）；工具（精简、无歧义、职责不重叠）；Few-shot示例（选多样化典型案例，而非穷举边缘case）；消息历史（保持紧凑，定期清理）。

**4. Just-in-Time Context：运行时动态检索优于预加载**

与传统嵌入式预检索相比，Just-in-Time方法让Agent维护轻量标识符（文件路径、查询语句、URL等），在运行时才动态加载。优势：节省上下文空间、允许渐进式信息披露（progressive disclosure）、利用元数据（文件名、目录结构、时间戳）作为导航线索。Claude Code是典型实践：CLAUDE.md提前注入，glob/grep实时检索文件。局限：速度较慢，需要工程保障Agent有正确工具和启发式规则。

**5. 长周期任务的三大技术**

当任务超过单个上下文窗口时，三种互补技术：Compaction（对话临近窗口上限时摘要压缩并重启，保留架构决策、未解决Bug等关键信息，丢弃冗余工具输出）；Structured Note-taking（Agent周期性将关键信息写入外部文件，跨上下文窗口持久化，Claude玩宝可梦是跨领域验证案例）；Sub-agent架构（主Agent维持高层计划，子Agent各自使用干净上下文完成专项任务，仅向主Agent返回精炼摘要1,000-2,000 tokens）。

## 关键术语

| 术语 | 定义 |
|------|------|
| Context Engineering | 在LLM推理时动态筛选最优Token集合的策略集，是提示工程的超集与演进 |
| Attention Budget | LLM解析大量上下文时消耗的注意力容量，每引入新Token就减少一点 |
| Context Rot | 随上下文Token增加，模型信息召回精度下降的现象（Chroma Research提出）|
| Right Altitude | 系统提示的Goldilocks区间——既不过于具体（脆性）也不过于模糊（失效）|
| Just-in-Time Context | Agent运行时按需动态加载数据，而非提前批量预处理 |
| Progressive Disclosure | 通过探索逐层发现相关上下文，每次交互信息增量辅助下一步决策 |
| Compaction | 对话压缩摘要并重启上下文窗口的技术，长周期任务的首要杠杆 |
| Tool Result Clearing | Compaction最轻量实践：清除历史工具调用结果以节省上下文 |
| Structured Note-taking | Agent主动将关键信息写入外部持久存储，在需要时重新拉入上下文 |
| Sub-agent架构 | 主Agent协调，子Agent各自使用干净上下文完成专项任务并返回压缩摘要 |

## 相关概念

- concepts/context-engineering — 上下文工程总体方法论（本文大幅扩充其内涵）
- concepts/context-window — Token预算与KV Cache约束（本文补充Attention Budget视角）
- concepts/memory-systems — Agent记忆系统（本文补充Structured Note-taking实践）
- concepts/agentic-systems — Workflow vs Agent模式（本文补充Just-in-Time Context策略）
- concepts/aci — 工具设计原则（本文补充工具与上下文效率的关系）
- concepts/compaction — 对话压缩重启技术（本文为该概念主要来源，待新建）
- concepts/context-rot — 上下文衰减现象（本文为该概念主要来源，待新建）

## 相关实体

- entities/anthropic — 本文作者机构，Applied AI团队出品
- entities/claude-code — Just-in-Time Context与Compaction的标杆实践案例
- entities/mcp — Model Context Protocol，本文提及的上下文数据来源之一
