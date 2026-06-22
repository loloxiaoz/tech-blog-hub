---
title: "Building Effective AI Agents（构建有效的 AI Agent）"
org: "Anthropic"
date: 2024-12
source_url: "https://www.anthropic.com/engineering/building-effective-agents"
tags: ["Agent", "Eval/评测", "MCP", "工具调用"]
summary: "Anthropic 给出了明确的架构区分："
summary_zh: "Anthropic 给出了明确的架构区分："
summary_en: ""
---



# Building Effective AI Agents（构建有效的 AI Agent）

## 基本信息

- **来源**：Anthropic 官方工程博客
- **背景**：基于与数十个跨行业团队合作构建 LLM Agent 的经验总结
- **核心结论**：最成功的实现不依赖复杂框架，而是使用简单、可组合的模式

## 核心主张

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."

**首选原则**：找到最简单的解决方案，只在必要时才增加复杂度。对很多应用，优化单次 LLM 调用 + 检索 + 上下文示例已经足够。

## Workflow vs Agent 的权威定义

Anthropic 给出了明确的架构区分：

| 类型 | 定义 | 特点 |
|------|------|------|
| **Workflow（工作流）** | LLM 和工具通过**预定义代码路径**编排 | 可预测、一致性强，适合有明确步骤的任务 |
| **Agent（智能体）** | LLM **动态决定**自己的流程和工具使用 | 灵活性高，适合无法预测步骤数量的开放性任务 |

两者统称为 **Agentic Systems（智能体系统）**。

详见 concepts/agentic-systems

## 五种 Workflow 模式

详见 concepts/workflow-patterns

| 模式 | 核心机制 | 适用场景 |
|------|---------|---------|
| **Prompt Chaining** | 任务分解为顺序步骤，每步输出作为下步输入 | 任务可清晰分解为固定子任务 |
| **Routing** | 分类输入，路由到专门的后续任务 | 输入有明显类别，各类别最优处理方式不同 |
| **Parallelization** | 并行处理独立子任务（Sectioning）或多次运行求共识（Voting） | 子任务可并行，或需要多视角提高置信度 |
| **Orchestrator-Workers** | 中央 LLM 动态分解任务，委派给 Worker LLM | 无法预测所需子任务的复杂任务 |
| **Evaluator-Optimizer** | 一个 LLM 生成，另一个评估并反馈，形成循环 | 有明确评估标准，且迭代改进可量化 |

## 何时使用 Agent

**使用 Agent 的判断标准**：
- 无法预测所需步骤数量
- 无法硬编码固定路径
- 任务需要动态决策

**Agent 的代价**：
- 更高的成本
- 延迟增加
- **错误累积风险**（compounding errors）

建议：在沙盒环境中进行大量测试，配合适当的护栏（guardrails）。

## 基础构建块：增强型 LLM

所有 Agentic System 的基础是配备了**检索、工具、记忆**的 LLM。通过 entities/mcp，开发者可以轻松集成第三方工具生态。

## ACI（Agent-Computer Interface）

类比 HCI（人机界面），工具设计是 Agent 成败的关键。三大原则：

1. **站在模型角度**：工具描述和参数是否一目了然？如果对人来说需要思考，对模型也一样
2. **像给初级开发者写文档**：包含使用示例、边缘情况、输入格式要求、与其他工具的边界
3. **防呆设计（Poka-yoke）**：修改参数让模型更难犯错（如强制绝对路径而非相对路径）

**实践数据**：Anthropic 在 SWE-bench 实现中，花在工具优化上的时间多于整体 Prompt 优化。

详见 concepts/aci

## 三条核心原则

1. 保持 Agent 设计的**简洁性**
2. 通过显式展示规划步骤来确保**透明度**
3. 通过工具文档和测试精心构建 **ACI（Agent-Computer Interface）**

## 框架使用建议

- 建议优先直接使用 LLM API（许多模式只需几行代码）
- 如果使用框架，务必理解底层代码
- 框架带来的抽象层可能遮蔽 Prompt 和响应，增加调试难度

## Appendix：Agent 的两大应用场景

**客户支持**：自然对话流 + 外部系统访问 + 可程序化执行动作 + 可量化成功标准（按成功解决计费）

**代码 Agent**：代码可通过测试验证 + Agent 可用测试结果迭代 + 问题空间结构化 + 质量可客观衡量

## 相关概念

- concepts/agentic-systems — Workflow vs Agent 定义与何时使用
- concepts/workflow-patterns — 五种 Workflow 模式详解
- concepts/aci — Agent-Computer Interface 设计原则
- concepts/tool-retrieval — 工具检索，Agent 的核心能力之一
- concepts/context-engineering — 上下文工程，与 Agent 上下文组装相关

## 相关实体

- entities/mcp — 工具集成协议，增强型 LLM 的实现方式之一
- entities/anthropic — 本文作者所在公司
