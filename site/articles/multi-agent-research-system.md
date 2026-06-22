---
title: "How we built our multi-agent research system"
org: "Anthropic"
date: 2025-06-13
source_url: "https://www.anthropic.com/engineering/multi-agent-research-system"
tags: ["Agent", "Eval/评测", "推理模型", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# How we built our multi-agent research system

## 核心观点

**Token 用量是多智能体性能的核心驱动因素。** BrowseComp 评测中，三个因素解释了 95% 的性能方差：Token 用量（80%）、工具调用次数、模型选择。多智能体系统通过分配独立上下文窗口给并行子智能体，有效扩展了 Token 使用量，这是相比单智能体性能提升的根本机制。实验数据：Opus 4 主导 + Sonnet 4 子智能体的多智能体系统比单智能体 Opus 4 在内部研究评测中高出 90.2%。

**提示工程是多智能体协调的主控制杆。** 8 条核心原则：（1）思考像 Agent 一样运作（建立心智模型）；（2）教导编排者如何分解任务并给子 Agent 清晰目标和任务边界；（3）按查询复杂度分配 Agent 数量（1 个到 10+ 个）；（4）工具设计和描述质量至关重要（坏描述会让 Agent 走错路）；（5）让 Agent 改进自身（Claude 4 可诊断失败并重写工具描述，使任务完成时间下降 40%）；（6）先宽后窄的搜索策略；（7）用扩展思考作为可控推理草稿本；（8）并行工具调用将复杂查询研究时间缩短 90%。

**多智能体评测必须评结果不评路径。** 不同 Agent 可能走完全不同路径到达同一正确答案，传统步骤验证失效。实践方法：从 20 条小样本立即起步（不要等百条 eval）；LLM-as-judge 按五维度打分（事实准确性、引用准确性、完整性、来源质量、工具效率）；单次 LLM 调用输出 0-1 分值比多个 Judge 更稳定且与人工判断更一致；人工评测不可替代（发现了 SEO 内容农场偏好等自动化遗漏的偏差）。

**生产可靠性需要全新工程范式。** 多智能体系统中错误复利效应严重放大：一步失败会导致 Agent 走向完全不同的探索轨迹。必须支持断点续跑（checkpoint + resume）而非从头重启；使用 rainbow deployment 处理长期运行有状态系统的版本更新；生产追踪（production tracing）用于诊断根因；监控 Agent 决策模式而不监控对话内容（保护用户隐私）。

**多智能体有明确适用边界。** 适合：重度可并行化任务、信息量超出单上下文窗口、需与大量复杂工具交互、价值高于 15x Token 成本的任务（多智能体 Token 消耗约为 Chat 的 15 倍）。不适合：需要所有 Agent 共享同一上下文、任务间依赖多、实时协调要求高（如多数编码任务）。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Orchestrator-Worker 模式** | 主 Agent（Lead Researcher）负责分解查询、生成策略、协调子 Agent；Worker 子 Agent 并行执行具体搜索任务 |
| **breadth-first query** | 需要同时探索多个独立方向的查询，是多智能体系统的最佳适用场景 |
| **BrowseComp** | 测试浏览 Agent 定位难以找到信息能力的评测基准，Anthropic 用于衡量多智能体研究系统性能 |
| **extended thinking（扩展思考）** | Claude 输出额外可见推理 Token 的模式，在多智能体中用作可控的推理草稿本 |
| **interleaved thinking** | 子 Agent 在获得工具结果后穿插思考的模式，用于评估结果质量和细化下一步查询 |
| **rainbow deployment** | 渐进式流量切换部署策略，新旧版本同时运行，用于避免更新破坏长期运行的有状态 Agent |
| **CitationAgent** | 专门处理引用的 Agent，在主 Agent 完成研究后对文档和报告进行引用定位 |
| **end-state evaluation** | 评测最终状态是否正确，而非验证每个中间步骤，适用于有状态变更的 Agent 评测 |
| **error compounding（错误复利）** | 多智能体系统中，早期错误在后续步骤中放大，导致完全不同的探索轨迹 |
| **game of telephone（传话游戏）** | 子 Agent 结果需经过主 Agent 中转时的信息损耗问题，推荐用文件系统 artifact 模式绕过 |

## 相关概念

- concepts/agentic-systems — Workflow vs Agent 区分，多智能体是 Agent 的扩展形式
- concepts/agent-evaluation — 评测方法论，本文补充了多智能体特有的评结果不评路径原则
- concepts/harness-engineering — 生产工程范式，rainbow deployment 和断点续跑是其关键组件
- concepts/aci — Agent-Computer Interface，工具描述质量直接影响 Agent 效率
- concepts/context-engineering — 上下文工程，子 Agent 的上下文隔离是并行压缩的基础
- concepts/memory-systems — LeadResearcher 将研究计划存入 Memory 防 200K 截断，文件系统 artifact 模式
- concepts/workflow-patterns — Orchestrator-Worker 是五种模式之一的实战深化

## 相关实体

- entities/anthropic — 本文作者，描述了 Claude Research 功能的多智能体架构
- entities/mcp — 子 Agent 使用 MCP 工具，工具描述质量问题在 MCP 场景下更突出
