---
title: "Introducing Advanced Tool Use on the Claude Developer Platform"
org: "Anthropic"
date: 2025-11-24
source_url: "https://www.anthropic.com/engineering/advanced-tool-use"
tags: ["Agent", "RAG/检索", "MCP", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Introducing Advanced Tool Use on the Claude Developer Platform

## 核心观点

**Tool Search Tool 解决工具库 Token 膨胀问题。** 随着 MCP server 增多，工具定义的 Token 开销急剧累积（GitHub 35 个工具 ~26K tokens，Slack 11 个工具 ~21K tokens，Anthropic 内部曾见到 134K tokens 的工具定义开销）。Tool Search Tool 通过 `defer_loading: true` 将工具定义从初始上下文中剥离，Claude 仅在需要时主动搜索并加载 3-5 个相关工具。实测上下文消耗从 77K 降至 8.7K（减少 85%），Opus 4 的 MCP 评估准确率从 49% 提升至 74%，Opus 4.5 从 79.5% 提升至 88.1%。

**Programmatic Tool Calling 解决中间结果污染上下文的问题。** 传统工具调用每次都需要完整的推理轮次，且所有中间结果都堆入上下文。PTC 允许 Claude 生成 Python 编排代码，在沙箱（Code Execution 环境）中批量调用工具，支持 asyncio 并行执行；中间数据在沙箱内处理，仅最终结果（如聚合摘要）返回给模型。Token 消耗平均减少 37%（43,588 → 27,297），GPQA 基准从 46.5% 提升至 51.2%。Claude for Excel 用此特性处理数千行电子表格。

**Tool Use Examples 弥补 JSON Schema 无法表达的使用惯例。** Schema 定义了"结构合法性"，但无法表达日期格式（YYYY-MM-DD vs ISO 8601）、ID 命名约定（USR-12345 vs UUID）、嵌套字段的使用时机、参数之间的业务关联（critical 级别 bug 需要 escalation，feature request 不需要）。通过 `input_examples` 字段注入 1-5 个真实示例，内部测试准确率从 72% 提升至 90%。

**三项特性针对不同瓶颈，可按需叠加。** 最佳实践是从最大瓶颈入手：工具定义 Token 过多 → Tool Search Tool；大量中间结果污染上下文 → Programmatic Tool Calling；参数格式错误 → Tool Use Examples。三者互补：Search 确保找到正确工具，PTC 确保高效执行，Examples 确保正确调用。

**这组特性标志着工具调用的范式跃迁。** 从"每次调用 = 一次推理轮次"的简单函数调用，迈向"动态发现 + 代码编排 + 示例引导"的智能编排。为 Agent 无缝协作数百乃至数千个工具奠定基础。

## 关键术语

- **Tool Search Tool**：工具按需发现机制，将工具定义标记为延迟加载，Claude 通过搜索调用来按需展开定义；支持 regex、BM25、自定义 embedding 等后端
- **defer_loading**：工具定义字段，设为 `true` 时该工具不进入初始上下文，仅在被搜索时展开
- **Programmatic Tool Calling（PTC）**：Claude 生成 Python 代码在沙箱中编排工具调用，中间结果不进入 Claude 上下文；通过 `allowed_callers` 字段 opt-in
- **allowed_callers**：工具定义字段，指定哪些工具可以被代码执行环境调用（如 `["code_execution_20250825"]`）
- **input_examples**：工具定义字段，提供具体的参数调用示例，补充 JSON Schema 的语义盲区
- **Code Execution Tool**：沙箱执行环境，PTC 的运行载体；工具调用结果在此处理，不返回模型上下文
- **context pollution**：中间结果大量堆入上下文窗口，推挤有效信息的问题
- **defer_loading + Tool Search**：配合使用可将工具定义开销从 72K+ tokens 降至 3K 级别
- **BM25**：基于词频的检索算法，Claude 平台内置的 Tool Search 后端之一
- **beta header**：`advanced-tool-use-2025-11-20`，启用这三项特性所需的 API beta 标识

## 相关概念

- concepts/aci — 工具设计原则；Tool Search 对工具描述质量有更高要求；PTC 要求文档化返回格式
- concepts/context-window — 工具定义是 Token 四类消耗者之一；本文提供了具体量化数据
- concepts/agentic-systems — 多工具 Agent 编排的基础设施层
- concepts/harness-engineering — PTC 是 Harness 层的能力延伸，控制哪些中间结果进入模型上下文
- concepts/mcp — Tool Search Tool 专为 MCP 多 server 场景设计；defer_loading 可作用于 mcp_toolset 整体

## 相关实体

- entities/anthropic — 发布方；Claude for Excel 使用 PTC 的内部产品案例
- entities/mcp — MCP server 的工具定义 Token 消耗问题是本文三项特性的核心驱动场景
