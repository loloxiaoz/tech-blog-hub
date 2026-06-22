---
title: "Building Effective Agents（构建有效的 Agent）"
org: "Anthropic"
date: 2024-12-19
source_url: "https://www.anthropic.com/research/natural-language-autoencoders"
tags: ["Agent", "Eval/评测", "工具调用"]
summary: "最成功的 Agent 实现不依赖复杂框架，而是用简单、可组合的模式构建。对于许多应用，优化单次 LLM 调用 + 检索 + 上下文示例就已足够。只有在能证明改善效果时才增加复杂度。"
summary_zh: "最成功的 Agent 实现不依赖复杂框架，而是用简单、可组合的模式构建。对于许多应用，优化单次 LLM 调用 + 检索 + 上下文示例就已足够。只有在能证明改善效果时才增加复杂度。"
summary_en: ""
---



# Building Effective Agents（构建有效的 Agent）

## 核心观点

**1. 简单优先，复杂按需**
最成功的 Agent 实现不依赖复杂框架，而是用简单、可组合的模式构建。对于许多应用，优化单次 LLM 调用 + 检索 + 上下文示例就已足够。只有在能证明改善效果时才增加复杂度。

**2. Workflow vs Agent 的架构区分**
Anthropic 将所有 Agentic Systems 分为两类：
- **Workflow**：LLM 和工具通过预定义代码路径编排，提供一致性和可预测性
- **Agent**：LLM 动态决定自己的流程和工具使用，适合无法预测步骤数的开放式问题

**3. 五种核心 Workflow 模式**
按复杂度递进：Prompt Chaining（顺序任务分解）→ Routing（分类路由）→ Parallelization（并行化，含 Sectioning 和 Voting 两种变体）→ Orchestrator-Workers（动态子任务编排）→ Evaluator-Optimizer（生成-评估反馈循环）。

**4. ACI 工具接口设计是 Agent 成败关键**
Agent-Computer Interface（ACI）的设计应投入与 HCI 同等的工程精力。工具格式需贴近自然文本、避免计数/转义等认知负担。在 SWE-bench Agent 实践中，Anthropic 花在工具优化上的时间多于整体 Prompt 优化。

**5. Agent 三条核心原则**
保持简单（Simplicity）、确保透明（Transparency，显式展示规划步骤）、精心设计 ACI（工具文档与测试）。自主 Agent 有更高成本和错误累积风险，建议在沙盒环境中大量测试。

## 关键术语

- **Agentic Systems**：将 LLM 与工具/外部环境结合以完成任务的系统总称，包含 Workflow 和 Agent 两类
- **Augmented LLM**：增强型 LLM，基础构建块，集成了检索、工具、记忆三类能力
- **Prompt Chaining**：将任务分解为顺序步骤，每个 LLM 调用处理上一步输出，可插入 Gate 校验
- **Parallelization**：并行化工作流；Sectioning 变体分解为独立子任务并行，Voting 变体多次运行求共识
- **Orchestrator-Workers**：编排者 LLM 动态分解任务并委派给 Worker LLM，子任务不预定义
- **Evaluator-Optimizer**：生成者-评估者循环，通过迭代反馈逐步改进输出质量
- **ACI（Agent-Computer Interface）**：Agent 与工具/外部系统的接口设计，类比 HCI
- **Poka-yoke（防呆设计）**：修改工具参数设计使模型更难犯错，如强制绝对路径
- **Ground truth**：Agent 执行中每步从环境获取的真实反馈（工具调用结果、代码执行结果）
- **Compounding errors（错误累积）**：多步骤 Agent 中早期错误在后续步骤中被放大的风险

## 相关概念

- concepts/agentic-systems — 本文是该概念的核心来源
- concepts/workflow-patterns — 五种 Workflow 模式的详细展开
- concepts/aci — ACI 工具接口设计，本文的重要原创贡献
- concepts/tool-design-for-agents — 工具设计最佳实践
- concepts/multi-agent-systems — Orchestrator-Workers 延伸至多 Agent 架构

## 相关实体

- entities/anthropic — 本文作者机构，发布该实践总结
- entities/claude-agent-sdk — 文中列为参考框架之一
- entities/mcp — 文中推荐用于集成第三方工具生态
- entities/swe-bench — 文中代码 Agent 的实战验证基准
