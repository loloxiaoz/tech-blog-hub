---
title: "Writing effective tools for agents — with agents"
org: "Anthropic"
date: 2025-09-11
source_url: "https://www.anthropic.com/engineering/writing-effective-tools"
tags: ["Agent", "Eval/评测", "Claude Code", "工具调用"]
summary: "工具是确定性系统与非确定性 Agent 之间的新型软件契约。传统软件开发假设调用方行为可预测，而 Agent 可能以多种路径使用（或误用）工具。因此，工具设计必须专门为 Agent 的认知模式服务，而非简单地将现有 API 包装暴露。"
summary_zh: "工具是确定性系统与非确定性 Agent 之间的新型软件契约。传统软件开发假设调用方行为可预测，而 Agent 可能以多种路径使用（或误用）工具。因此，工具设计必须专门为 Agent 的认知模式服务，而非简单地将现有 API 包装暴露。"
summary_en: ""
---



# Writing effective tools for agents — with agents

## 核心观点

工具是确定性系统与非确定性 Agent 之间的新型软件契约。传统软件开发假设调用方行为可预测，而 Agent 可能以多种路径使用（或误用）工具。因此，工具设计必须专门为 Agent 的认知模式服务，而非简单地将现有 API 包装暴露。

构建工具的最佳实践路径是：快速原型 → 基于真实复杂任务的评估 → 让 Claude Code 分析评估 transcript 自动优化工具描述和实现 → 再次评估，形成闭环。评估任务应具有真实复杂度，强任务往往需要数十次工具调用；弱任务仅需一次精确调用，无法暴露工具的真实缺陷。

工具选择策略上，少而精优于多而杂。应将高频链式调用合并为单一语义工具（例如用 `schedule_event` 替代 `list_users + list_events + create_event` 的组合），从而减少 Agent 的 context 消耗，并降低其在工具选择时犯错的风险。工具命名空间（namespacing）也至关重要：按服务或资源类型给工具加前缀（如 `asana_projects_search`），帮助 Agent 在数百个工具中快速定位。

工具响应应返回高信息密度内容，而非原始技术数据。用自然语言名称替代 UUID 等技术标识符可显著降低幻觉率。可为工具提供 `response_format` 参数，支持 `concise`（约 72 tokens）和 `detailed`（约 206 tokens）双模式，让 Agent 按需选择；响应格式（XML/JSON/Markdown）也需根据具体任务和模型通过评估来选择。

工具描述本身就是 Prompt Engineering。应像给新员工写文档一样写工具描述：精确命名参数（用 `user_id` 而非 `user`），明确说明专有查询格式、术语定义和资源间关系。即使微小的描述改进也可带来显著提升——精炼工具描述是 Claude Sonnet 3.5 在 SWE-bench Verified 上取得 SOTA 的关键因素之一。

## 关键术语

- **工具（Tool）**：确定性系统与非确定性 Agent 之间的软件契约，区别于传统函数/API 的调用方是人或确定性系统
- **工具命名空间（Tool Namespacing）**：按服务或资源类型为工具添加统一前缀或后缀，帮助 Agent 在大量工具中准确选择（如 `asana_projects_search`）
- **ResponseFormat 枚举**：通过 `concise`/`detailed` 参数让 Agent 控制工具响应详细程度，平衡信息完整性与 token 消耗
- **held-out test set**：评估中预留的未参与优化的测试集，防止对"训练集"评估过拟合
- **工具亲和力（Tool Affordance）**：Agent 感知并理解工具可执行操作的能力，与传统软件用户的感知方式不同
- **interleaved thinking**：Claude 的交错思考模式，在工具调用前后插入推理过程，可用于分析 Agent 选择/不选择特定工具的原因
- **工具截断（Tool Truncation）**：对过长工具响应主动截断并附带引导信息，鼓励 Agent 转向更精准的小批量查询策略
- **工具描述 Prompt Engineering**：将工具描述视为系统 Prompt 的一部分，通过精确描述参数名称、边界条件、示例来引导 Agent 的工具调用行为

## 相关概念

- concepts/aci — Agent-Computer Interface，工具设计的核心框架，本文是其最详细的实践指南
- concepts/agent-evaluation — 工具评估是 Agent 评估的专项子集，本文补充了工具专项评估指标和方法
- concepts/agentic-systems — 工具是 Agentic System 的核心组件
- concepts/context-window — 工具响应的 token 消耗管理是 context window 优化的重要方向
- concepts/harness-engineering — 工具开发流程（原型→评估→优化循环）是 harness 工程的组成部分
- concepts/workflow-patterns — 合并语义工具与工作流模式中的工具链设计直接相关

## 相关实体

- entities/anthropic — 文章作者所在机构，分享了内部 Slack/Asana 工具的评估数据
- entities/claude-code — 工具开发流程中的核心协作 Agent，用于生成原型、分析 transcript、批量优化工具描述
- entities/mcp — 工具通过 MCP 协议暴露给 Agent，命名空间设计和工具注解均依赖 MCP 规范
