---
title: "Harness design for long-running application development"
org: "Anthropic"
date: 2026-03-24
source_url: "https://www.anthropic.com/engineering/harness-design-long-running-apps"
tags: ["Agent", "Eval/评测", "MCP"]
summary: "Naive 单 Agent 实现面临两类持续性问题。第一，模型在长任务中随上下文窗口填满而丧失连贯性，部分模型还会出现「上下文焦虑」（Context Anxiety）——在接近其预期上下文上限时提前收尾工作。解法是上下文重置：完全清空上下文窗口，启动新 Agent 实例，通过结构"
summary_zh: "Naive 单 Agent 实现面临两类持续性问题。第一，模型在长任务中随上下文窗口填满而丧失连贯性，部分模型还会出现「上下文焦虑」（Context Anxiety）——在接近其预期上下文上限时提前收尾工作。解法是上下文重置：完全清空上下文窗口，启动新 Agent 实例，通过结构"
summary_en: ""
---



# Harness design for long-running application development

## 核心观点

**1. 两个根本性缺陷：上下文连贯性崩溃与自我评估盲区**

Naive 单 Agent 实现面临两类持续性问题。第一，模型在长任务中随上下文窗口填满而丧失连贯性，部分模型还会出现「上下文焦虑」（Context Anxiety）——在接近其预期上下文上限时提前收尾工作。解法是上下文重置：完全清空上下文窗口，启动新 Agent 实例，通过结构化交接传递状态。第二，当被要求评估自己的输出时，Agent 倾向于自信地给予正面评价，即使质量明显欠佳。分离执行角色与评分角色是解决这一问题的强力杠杆。

**2. 主观审美质量可以被评分化并用于驱动迭代**

前端设计的核心挑战是「美不美」这类主观判断难以量化。解法是将设计原则和偏好编码为可打分的评分标准（Rubric），分四个维度：设计质量（整体连贯性）、原创性（是否有自定义决策而非模板复制）、工艺（排版层次/间距一致性/色彩对比）、功能性。标准同时提供给生成者和评估者，两者共享目标函数。标准显式惩罚「AI slop」——高度通用的 AI 生成风格模板。

**3. GAN 启发的 Generator-Evaluator 反馈循环**

受生成对抗网络（GAN）启发，构建两智能体反馈循环：Generator 创建前端，Evaluator 通过 Playwright MCP 与运行中的真实页面交互后打分并写详细批评，反馈流回 Generator 作为下一轮输入。每次生成运行 5 到 15 轮迭代，完整运行时间可达四小时。关键：评估者不是分析静态代码，而是像用户一样操作真实运行的应用，这使其能够捕捉仅靠代码审查无法发现的交互缺陷。

**4. 三智能体架构将 GAN 模式扩展至全栈开发**

全栈版本构建于三智能体架构：Planner（接收 1-4 句提示，扩展为完整产品规格，强调产品上下文和高层技术设计而非实现细节）、Generator（按 sprint 逐功能实现，参照产品规格推进）、Evaluator（使用 Playwright MCP 模拟用户操作，测试 UI 功能、API 端点和数据库状态）。该架构成本约为单 Agent 的 20 倍，但输出质量差异立竿见影。经过精简迭代（去除 sprint 构造、改为运行结束后单次 QA），以 4 小时 $124 的成本完成了一个包含排列视图、混音台和传输控制的浏览器 DAW。

**5. Harness 设计空间随模型进步而移动，不会消失**

随着模型能力提升，能够可靠独立完成的任务范围扩大，今天需要 Harness 辅助的任务明天或许模型自己能做。但这并不意味着 Harness 工程价值下降——有趣的 Harness 组合空间会移动到新的能力边界外。AI 工程师的核心任务是持续识别「当前模型单独做不可靠」的任务，并在该边界设计有效的 Harness 组合。评估者是否值得其成本，取决于任务是否超出当前模型的可靠独立完成范围。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Context Anxiety（上下文焦虑）** | 模型在接近其预期上下文上限时提前收尾工作的行为模式 |
| **Context Reset（上下文重置）** | 完全清空上下文窗口并启动新 Agent 实例，通过结构化交接传递状态 |
| **Generator-Evaluator Loop** | GAN 启发的两智能体反馈循环：生成者创建输出，评估者交互测试后提供批评，循环迭代 |
| **AI Slop** | 高度通用的 AI 生成模板风格，缺乏原创性决策，评分标准显式惩罚此类输出 |
| **Playwright MCP** | 赋予 Agent 操控浏览器与运行中应用交互能力的 MCP 工具，用于评估 UI/API/数据库状态 |
| **Sprint Construct** | 将生成任务分解为按功能点逐一推进的 sprint 单元（后被简化移除） |
| **Structured Handoff（结构化交接）** | 跨 Agent 会话传递上下文状态的结构化 Artifact，是上下文重置后维持连贯性的机制 |
| **Self-Evaluation Bias（自我评估盲区）** | Agent 被要求评估自身输出时倾向于过度正面评价的系统性偏差 |
| **Rubric（评分标准）** | 将主观判断转化为可打分维度的标准，同时提供给生成者和评估者以对齐目标 |
| **Claude Agent SDK** | Anthropic 提供的多智能体系统构建基础设施，用于实现 generator-evaluator 反馈循环 |

## 相关概念

- concepts/harness-engineering — Harness 工程范式，本文是其「外部质量闭环」的具体实现案例
- concepts/agent-evaluation — Agent 评测体系，本文的 Evaluator 是其「模型 Grader + Playwright 实测」的结合应用
- concepts/agentic-systems — 多智能体架构，本文三智能体系统的架构背景
- concepts/aci — Agent-Computer Interface，Playwright MCP 作为评估工具的 ACI 设计
- concepts/context-window — 上下文窗口管理，Context Anxiety 和 Context Reset 的理论背景
- concepts/workflow-patterns — Workflow 模式，planner-generator-evaluator 是编排模式的应用

## 相关实体

- entities/anthropic — 本文作者所属的 Anthropic Labs 团队
- entities/claude-code — 前端设计 Skill 和长时间编程 Harness 的基础平台
