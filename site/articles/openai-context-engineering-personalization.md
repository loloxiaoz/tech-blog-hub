---
title: "Context Engineering for Personalization（面向个性化的上下文工程）"
org: "OpenAI"
date: 2026-01-05
source_url: "https://cookbook.openai.com/examples/context_engineering_for_personalization"
tags: ["OpenAI", "API", "Context Engineering", "个性化"]
summary_zh: "OpenAI Cookbook 用旅行管家 Agent 演示个性化记忆架构：状态化记忆、会话内蒸馏、会话结束合并、注入时明确优先级，并给出蒸馏、注入、合并三类评测与护栏。"
summary_en: ""
---

# Context Engineering for Personalization（面向个性化的上下文工程）

## 为什么上下文个性化重要

现代 AI agent 不再只是被动反应的助手，正在变成自适应协作者。上下文工程关心的是：在任意时刻，如何塑造模型所知道的东西。

- 用户视角：agent 记住偏好，体验才像「为我而定」
- 公司视角：这是战略护城河——捕获高信号的行为数据

## 场景：旅行管家 Agent

要构建的 agent：

- 每次会话以结构化的用户画像 + 记忆笔记开始
- 通过专用工具捕获新的持久偏好
- 会话结束时把偏好合并进长期记忆
- 解决冲突：最新用户输入 → 会话覆盖 → 全局默认

## 架构流程

- 会话前：state 对象（profile + global memory）保存在本地
- 会话开始：state 注入 system prompt（YAML frontmatter + Markdown 记忆列表）
- 会话中：用 `save_memory_note(...)` 捕获候选记忆
- 上下文裁剪：会话级记忆重新注入 system prompt
- 会话结束：合并任务把会话笔记并入全局记忆
- 下次运行：复用更新后的 state

## 四个记忆架构决策

### 1. 检索式还是状态式

本 Cookbook 选择状态式：

- 把用户知识编码成结构化、权威的字段
- 优先级清晰（全局 vs 会话）
- 支持信念更新，而不只是事实堆积
- 决策可确定

### 2. 记忆的形态

结构化记忆（schema 驱动、可预测）：

- 身份与核心画像（客户 ID、姓名、护照有效期）
- 忠诚度与会员计划（航空/酒店等级、会员号）
- 偏好与保障（座位偏好、保险画像）
- 约束（签证要求）

非结构化记忆（叙述式、上下文式）：

- 「用户通常喜欢靠走道的座位」
- 「一周以内的行程，用户通常不托运」

### 3. 记忆的范围

- 用户级（全局笔记）：跨会话的持久偏好
- 会话级（会话笔记）：短期、上下文相关，只服务当前交互

规则：会影响未来行程的 → 全局；只对现在重要的 → 会话。

### 4. 记忆的生命周期

- 蒸馏（会话进行中）：通过 `save_memory_note()` 捕获偏好
- 合并（会话结束、异步）：并入全局记忆、去重、解冲突、清理过期记忆。这是最敏感的环节，合并做得差会导致上下文污染
- 注入（每次会话开始）：通过 hooks 注入精选后的记忆

## 涵盖的技术

- 状态管理：`RunContextWrapper` 持久状态
- 记忆注入：YAML frontmatter + Markdown 笔记
- 记忆蒸馏：会话中通过专用工具捕获
- 记忆合并：合并 + 去重 + 冲突解决
- 遗忘：清理过期、低置信度的记忆

## 分步实现

### 步骤 0-2：前置条件与状态对象

定义 `TravelState` dataclass：profile、global_memory、session_memory、trip_history。

### 步骤 3-4：蒸馏与裁剪

- `save_memory_note()` 工具实时捕获
- `TrimmingSession` 只保留最近 N 轮用户消息

### 步骤 5-7：注入与 hooks

- 把 state 渲染成 YAML frontmatter + Markdown
- `MemoryHooks.on_start()` 在会话开始时注入
- 优先级：最新用户输入 > 会话 > 全局

### 步骤 8：会话后合并

`consolidate_memory()`：

- 把会话笔记并入全局记忆
- 用 LLM 去重、解冲突
- 合并后清空会话记忆
- 清理低质量或过期记忆

## 记忆评测

- 蒸馏评测（捕获质量）：精确率、召回率、安全性
- 注入评测（使用质量）：时效正确性、过度影响、token 效率
- 合并评测（整理质量）：去重、冲突解决、不发明

实用指标：

- 每 100 轮的 `memory_write_rate`
- `blocked_write_rate`
- `memory_conflict_rate`
- `time_to_personalization`（达到个性化的时间）

## 记忆护栏

蒸馏检查：

- 拒绝敏感模式（社保号、支付信息）
- 拒绝指令形态的载荷
- 约束工具 schema

合并检查：

- 强制「不得发明」
- 最新优先的冲突解决
- 语义等价的记忆去重

注入检查：

- 用明确分隔符包裹注入的记忆
- 强制优先级：当前用户消息 > 会话上下文 > 记忆
- 把记忆当作建议，而非权威

## 结论

上下文工程 + 状态管理，把个性化变成可持续的差异化优势。记忆设计应随系统学习「什么持久、什么情境化」而演进。

迭代闭环：

1. 上线零样本记忆管线与评测框架
2. 收集真实失败案例
3. 微调记忆专用模型
4. 重跑评测并量化改进
