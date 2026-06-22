---
title: "拥抱Agent，卷死其他牛马"
org: "AI 工程实践"
date: 2026-04-14
source_url: "https://zhuanlan.zhihu.com/p/2025676117307138196"
tags: ["Agent", "Claude Code", "推理模型", "工具调用"]
summary: "把自己的薪水换成等价的 claude code token，产出只会更多。"
summary_zh: "把自己的薪水换成等价的 claude code token，产出只会更多。"
summary_en: ""
---



# 拥抱Agent，卷死其他牛马

## 核心论点

> **当下，没有任何事情比"去学习更好地使用 agent"更加重要。**

把自己的薪水换成等价的 claude code token，产出只会更多。

## LLM 发展三阶段框架

| 阶段 | 特点 |
|------|------|
| **Chat Model** | 普通人的智商和情商 |
| **Reasoning Model** | 硕博水平的知识能力 |
| **Agent Model** | 职场人的能力：主观能动性，独立发现问题、解决问题，在 environment 内找收益 |

## Agent 能力的关键：Environment

> 模型自身的理解能力 = 知识；训练时能接触到的 Environment = 所处的平台。二者共同决定 agent 所能达到的高度。

**提升 Agent 能力的两条训练思路**：
1. **Hacking Claude CoT → SFT**：跟最优秀的员工学习（泛化差但效率高）
2. **Scaling RL**：自己摸索（泛化好但 token efficiency 差，训练消耗高）

**两者殊途同归**：都指向 **exploring environment is all you need**。SFT 带来 exploring environment 的成功经验，RL 是在 exploring environment 的过程中成长。

**Environment 对 Agent 的决定性影响**：
- 权限越多、工具越丰富 → 可探索空间越大 → 主观能动性发挥越好
- Environment 越稳定、Reward 越公允 → 工具调用时机学习越准确

**比喻**：员工能力由知识（模型参数）和平台（Environment）共同决定，两者拉开差距的往往是后者。

## 当前 Agent 能力（2026年判断）

- claude code/codex 在 agent 能力上断层领先，国内外差距比以往任何时候都大
- Agent 时代红利正在虚位以待（Reasoning 时代已被 DeepSeek 获取）

## 相关概念

- concepts/agentic-systems — Agent 系统的完整框架
- concepts/harness-engineering — Environment + Harness 的工程化
