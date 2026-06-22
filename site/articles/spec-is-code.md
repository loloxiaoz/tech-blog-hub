---
title: "别再幻想用 Spec 替代写代码"
org: "AI 工程实践"
date: 2026-03-23
source_url: "https://haskellforall.com/2026/03/a-sufficiently-detailed-spec-is-code"
tags: ["Agent", "Claude Code", "工具调用"]
summary: "向\"信徒\"推销 Agentic Coding 时用这个：工程师只需当管理者，写 Spec 扔给 Agent。"
summary_zh: "向\"信徒\"推销 Agentic Coding 时用这个：工程师只需当管理者，写 Spec 扔给 Agent。"
summary_en: ""
---



# 别再幻想用 Spec 替代写代码

## 一句话总结

> **足够详尽的 Spec 就是代码。** A sufficiently detailed spec is code.

## 两个常见误解

### 误解 1：Spec 文档比对应代码更简单

向"信徒"推销 Agentic Coding 时用这个：工程师只需当管理者，写 Spec 扔给 Agent。

**反驳**：如果你想让 Spec 精确到能可靠生成可运行的实现，你不得不把文档写成代码，或者高度接近代码的东西（极其结构化的形式化英文）。Spec 本身的复杂度不比代码低。

Dijkstra：
> 选择接口并不只是把工作一分为二，改变接口很容易导致接口两端工作量都增加。改用自然语言与机器通信会大大加重机器的负担，但我们必须质疑：这样做真的能让人的工作变得更简单吗？

### 误解 2：写 Spec 一定比写代码更深思熟虑

向"怀疑者"推销时用这个：先写 Spec 再生成代码，倒逼质量提升。

**反驳**：在追求交付速度的压力下，没有人会做 Spec 写作要求的那种费力的深度思考工作。这就是为什么 OpenAI 的 Symphony 这份"Spec"读起来像 AI 生成的垃圾——作者优化的是交付速度而非连贯性。

## 案例分析：OpenAI Symphony Spec

OpenAI 把 Symphony 当作"从 Spec 生成项目"的标杆案例。但仔细看，这份 SPEC.md：
- 用大段文字列出数据库字段（这是伪代码）
- 用文字"描述"本质上就是代码的逻辑
- 专门为"喂"模型加了速查表章节
- 有整段直接就是代码（但被标注为 `text` 而非语言）

**实测**：作者按照 README 让 Claude Code 用 Haskell 实现 Symphony，结果代码有多个 bug，即使修复后 codex Agent 也只在那里空转。

## 核心洞见

编码 Agent 不会读心术。即使它们会，如果你的思路本身就是混乱的，它们也帮不了你。

> 垃圾进，垃圾出。你给 Agent 一份含糊不清的文档，Agent 不能替你把缺失的清晰度补上。

**Spec 从来就不是用来省时间的。** 如果目标是缩短交付时间，直接写代码大概率更好，而不是绕一圈写中间 Spec 文档。

## 对 ACI/工具设计的启示

与 concepts/aci 的 Poka-yoke 原则相呼应：精确定义 > 自然语言描述。工具/接口设计需要"窄接口"——这正是 Dijkstra 所说的形式化符号系统的力量。

## 相关概念

- concepts/aci — ACI 设计：工具描述需要精确，不能依赖模糊自然语言
- concepts/harness-engineering — Harness 是"窄接口"的工程化实践
