---
title: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
org: "记忆系统"
date: 2026-05-10
source_url: ""
tags: ["Agent", "Eval/评测", "长上下文"]
summary: "LLM 固定上下文窗口无法维持跨会话的一致性。即便 GPT-4o（128K）、Claude 3.7 Sonnet（200K）、Gemini（10M）这样的大窗口，也只是延迟而非解决问题——真实对话中信息主题跳跃，关键偏好会被大量无关内容淹没，注意力在远端 token 上退化。"
summary_zh: "LLM 固定上下文窗口无法维持跨会话的一致性。即便 GPT-4o（128K）、Claude 3.7 Sonnet（200K）、Gemini（10M）这样的大窗口，也只是延迟而非解决问题——真实对话中信息主题跳跃，关键偏好会被大量无关内容淹没，注意力在远端 token 上退化。"
summary_en: ""
---



# Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

**来源**：`raw/Building Production-Ready AI Agents.pdf`
**arXiv**：2504.19413v1（2025-04-28）
**作者**：Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav（mem0.ai）
**代码**：https://mem0.ai/research

---

## 核心问题

LLM 固定上下文窗口无法维持跨会话的一致性。即便 GPT-4o（128K）、Claude 3.7 Sonnet（200K）、Gemini（10M）这样的大窗口，也只是**延迟**而非解决问题——真实对话中信息主题跳跃，关键偏好会被大量无关内容淹没，注意力在远端 token 上退化。

---

## 两种架构

### Mem0：增量提取范式

以消息对 (m_{t-1}, m_t) 为处理单元，pipeline 两阶段：

**提取阶段（Extraction）**：
1. 从对话历史提取上下文摘要 S
2. 结合当前消息对，用专用模块抽取显著信息
3. 对新提取信息进行分类：ADD / UPDATE / DELETE / NOOP

**更新阶段（Update）**：
- 将处理后的信息写入持久化记忆库
- 支持增量合并，不覆盖历史

### Mem0^G：图记忆增强变体

将记忆存储为**有向标签图**：实体为节点，关系为有向边。同一实体在多条记忆中出现时，图结构自动关联，支持跨记忆多跳推理。

---

## LOCOMO 基准结果

| 维度 | Mem0 提升 |
|------|---------|
| vs OpenAI 官方记忆 | +26%（LLM-as-Judge） |
| vs 全上下文方法 | -91% p95 延迟 |
| Token 成本 | 节省 90%+ |
| Mem0^G vs 基础 Mem0 | +~2% 整体得分 |

四类问题均优于对比方案：单跳（single-hop）、时序（temporal）、多跳（multi-hop）、开放域（open-domain）。

---

## 关键洞察

- **结构化提取 >> 全量上下文**：主动提取+合并，而非被动放进更长的窗口
- **增量范式天然适配流式对话**：每次处理一个消息对，无需重新处理全历史
- **图结构捕捉对话元素间关系**：纯文本记忆无法做多跳推理，图结构使之成为可能
- 91% 延迟降低来自避免了全上下文 attention 的二次复杂度

---

## 相关 Wiki 页面

- concepts/memory-systems — Mem0 是 Agent 记忆系统的生产级实现
- concepts/agentic-retrieval — 跨会话记忆是 Agentic Retrieval 的关键场景
