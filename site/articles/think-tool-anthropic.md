---
title: "The \"think\" tool: Enabling Claude to stop and think in complex tool use situations"
org: "Anthropic"
date: 2025-03-20
source_url: "https://www.anthropic.com/engineering/claude-think-tool"
tags: ["Eval/评测", "推理模型", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# The "think" tool: Enabling Claude to stop and think in complex tool use situations

## 核心观点

**think 工具与 extended thinking 的本质区别**：extended thinking 发生在生成响应之前（预规划阶段），Claude 在此深度迭代计划；think 工具发生在生成过程中段，专门用于处理工具调用返回的外部信息，而非初始问题本身。两者互补而非替代：think 工具聚焦于"发现新信息后如何推理"，extended thinking 聚焦于"行动前如何规划"。2025年12月更新：Anthropic 建议多数情况下改用 extended thinking，后者集成度更好。

**benchmark 数据验证效果显著**：在 τ-Bench 航空客服域，think 工具配合优化 Prompt 将 pass^1 从 0.332 提升至 0.584（相对提升 76%），且一致性优势在 k=1 到 k=5 均保持；零售域无需额外提示即达到最高分 0.812（基线 0.783）；SWE-Bench 中统计显著提升 1.6%（p<0.001，效应量 d=1.47）。

**领域复杂度决定 Prompt 策略**：简单策略域（如零售），提供 think 工具本身即有效；复杂策略域（如航空），必须在 system prompt 中提供领域特定的推理示例才能释放最大效果。仅提供 think 工具定义而无示例，效果与 extended thinking 相近。System prompt 比 tool description 更适合放置复杂的使用说明。

**三类最适合场景与两类不适合场景**：最适合：工具输出分析（需在行动前处理前序调用结果）、策略密集环境（需遵循详细政策并验证合规）、顺序决策（每步依赖前步、错误代价高）。不适合：非顺序工具调用（单次或并行调用）、简单指令遵循（默认行为已足够）。think 工具会增加 token 消耗，应避免滥用。

**实现成本极低，风险极小**：think 工具本质上是一个 JSON 工具定义，不会改变外部行为（除非 Claude 主动选择使用），不干扰现有工具和工作流。Claude 自主决定何时调用，最差情况不过是多消耗少量 token。

## 关键术语

- **think 工具**：无副作用的特殊工具，让 Claude 在工具调用链中途进行结构化推理，仅将思考追加到日志，不获取新信息也不修改外部状态
- **extended thinking**：Claude 在生成响应之前的深度推理阶段，适合预规划和非顺序场景
- **τ-Bench（tau-bench）**：评测模型在真实客服场景中工具使用能力的综合 benchmark，包含航空和零售两个域
- **pass^k**：τ-Bench 主指标，测量所有 k 次独立试验均成功的概率均值，衡量一致性和可靠性
- **pass@k**：常见 LLM 评测指标，测量 k 次试验中至少一次成功的概率，衡量峰值性能
- **SWE-Bench**：软件工程 benchmark，Claude 3.7 Sonnet 加入 think 工具后达到当时最优 0.623
- **scratchpad（草稿本）**：think 工具的比喻，Claude 在此记录中间推理过程，不产生外部效果
- **顺序决策（sequential decision making）**：每步依赖前步结果的决策链，think 工具在此类场景效益最大
- **策略密集环境（policy-heavy environment）**：需要遵循大量详细规则并验证合规性的场景
- **优化 Prompt**：在 system prompt 中提供领域特定推理示例，指导 Claude 如何在 think 工具中进行有效推理

## 相关概念

- concepts/think-tool — think 工具机制与适用场景详解
- concepts/extended-thinking — extended thinking 与 think 工具的对比
- concepts/agent-evaluation — τ-Bench 评测框架、pass^k 指标
- concepts/agentic-systems — Agent 工具调用链设计
- concepts/aci — Agent-Computer Interface，think 工具作为特殊无副作用工具的设计模式

## 相关实体

- entities/anthropic — 发布 think 工具研究
- entities/claude-code — Claude 3.7 Sonnet 使用 think 工具在 SWE-Bench 达到 0.623
