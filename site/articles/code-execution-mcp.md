---
title: "Code execution with MCP: Building more efficient agents"
org: "Anthropic"
date: 2025-11-04
source_url: "https://www.anthropic.com/engineering/code-execution-mcp"
tags: ["Agent", "MCP", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Code execution with MCP: Building more efficient agents

## 核心观点

**直接工具调用的两大效率瓶颈。** 大规模MCP接入面临两个结构性问题：第一，工具定义批量加载——数千个工具的定义全部预注入上下文，在模型读取请求前就消耗数十万token；第二，中间结果流经模型——每次工具调用的返回值都必须经过模型，一份2小时会议纪要在"读取+写入"流程中被重复计算约50,000 token。

**将MCP工具呈现为文件系统代码API是核心解法。** 把每个MCP服务器的工具生成为对应的TypeScript文件，组成文件树。Agent通过浏览目录发现可用服务器，按需读取特定工具文件理解接口，再编写代码调用。实测将150,000 token的消耗降至2,000 token，节省98.7%。Cloudflare独立验证了相同结论，将其命名为"Code Mode"。

**代码执行在执行环境中处理数据，不污染模型上下文。** 大数据集（如10,000行表格）可在执行环境中先过滤、聚合、提取，只将结果（如5行）返回给模型；循环、条件、错误处理用原生代码完成，无需在Agent循环中逐步调用；if-else判断在执行环境运行，节省"首token延迟"。

**代码执行天然支持隐私保护。** 中间数据默认留在执行环境，不进入模型上下文。Harness层可进一步在MCP Client拦截并自动tokenize PII字段（邮件、电话、姓名替换为占位符），数据在工具间流动时由MCP Client反向解码，真实敏感信息全程不经过模型。

**与Skills深度融合，Agent工具箱可自我进化。** Agent可将执行中产生的有效代码保存为 `./skills/*.ts` 函数文件，添加SKILL.md后形成结构化Skills供后续任务引用。随时间推移，Agent逐步积累高阶能力工具箱。代码执行也引入沙箱、资源限制、监控等基础设施要求，实施前需权衡收益与复杂度成本。

## 关键术语

- **Code Mode**：Cloudflare命名的模式，与本文"代码执行with MCP"同义，指Agent以编写代码而非直接调用工具的方式与MCP服务器交互。
- **Progressive Disclosure（渐进式工具发现）**：Agent不预加载全部工具定义，而是通过浏览文件系统或调用 `search_tools` 按需发现并加载所需工具。
- **执行环境（Execution Environment）**：运行Agent生成代码的安全隔离环境，中间数据在此处理，不流入模型上下文。
- **PII Tokenization**：MCP Client拦截数据流，将个人敏感信息（邮件、电话、姓名）替换为占位符再传给模型；调用其他MCP工具时再反向解码，敏感数据全程绕过模型。
- **工具定义膨胀**：大量MCP工具的描述、参数、返回值说明在上下文中累积，成为token消耗主体，是直接工具调用模式的核心扩展性瓶颈。
- **文件树工具注册**：将MCP服务器工具以文件系统目录树形式组织（`./servers/<server-name>/<tool-name>.ts`），让Agent可通过文件操作探索和读取工具接口定义。
- **沙箱（Sandboxing）**：代码执行模式的必要基础设施，对Agent生成代码的运行环境进行隔离、资源限制和监控，防止安全风险。
- **Skills持久化**：Agent将执行中开发的有效函数保存为 `./skills/` 下的可复用文件，配合SKILL.md形成结构化技能，供后续任务调用。

## 相关概念

- entities/mcp — MCP协议整体，本文是其高效使用模式的深度扩展
- concepts/context-window — 工具定义膨胀直接导致context window压力，代码执行是缓解方案
- concepts/agent-skills — 代码执行产生的函数可直接持久化为Skills，两者深度融合
- concepts/harness-engineering — 代码执行层（沙箱、PII tokenization、文件系统）是Harness工程的核心组件
- concepts/agentic-systems — 代码执行模式改变了Agent的工具调用范式，从直接调用转为代码生成

## 相关实体

- entities/anthropic — 文章作者所在机构，MCP协议发起方
- entities/mcp — 本文核心协议，代码执行模式围绕MCP展开
- entities/claude-code — Claude Code沙箱是代码执行安全运行的基础设施参考
