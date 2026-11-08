---
title: "Building Reliable Agents with Memory and Compaction（用记忆与压缩构建可靠的长时间运行 Agent）"
org: "OpenAI"
date: 2026-05-01
source_url: "https://cookbook.openai.com/examples/agents_sdk/building_reliable_agents_with_memory_and_compaction"
tags: ["OpenAI", "API", "Agent", "Memory", "Compaction"]
summary_zh: "OpenAI Cookbook 用合规调查证据审查 Agent 演示两个可靠性原语：compaction 让长对话在有限上下文里继续，memory 让后续运行复用流程经验，而最终备忘录始终是人类复核的事实来源。"
summary_en: ""
---

# Building Reliable Agents with Memory and Compaction（用记忆与压缩构建可靠的长时间运行 Agent）

## 两个可靠性原语

这个 Cookbook 用 OpenAI Agents SDK 构建一个用于合成合规调查的证据审查 agent，并引入长周期 agent 工作流的两个核心可靠性原语：

- **Compaction（压缩）**：让长对话在有限的模型上下文窗口内继续
- **Memory（记忆）**：让未来的 agent 运行复用此前运行的流程经验

## 核心设计原则：职责分离

- **上下文**帮助当前这次 agent 运行完成工作
- **记忆**帮助未来的 agent 运行更有效
- **最终生成的产物**（合规审查备忘录）仍是人类复核的事实来源

## 用例：合规调查的证据审查 agent

合规团队调查某供应商例外是否遵守内部政策。证据以文件形式提供：政策文本、例外说明、审计观察、审批记录、整改计划。

agent 的职责：

- 帮审查者梳理证据
- 跟踪记录随时间的变化
- 写一份简洁备忘录，把「有依据的结论」与「开放问题」分开

## 这个模式适用在哪里

- 客服团队应用新政策
- 安全团队审查事件证据
- 财务团队核对例外
- 产品团队更新竞争定位
- 法务/采购团队审查合同
- 并购团队吸收新业务规则

## 记忆 vs 压缩

| 问题 | Compaction | Memory |
|---|---|---|
| 帮助什么 | 继续一次长运行 | 改善未来运行 |
| 总结什么 | 当前对话与工作状态 | 模式、偏好、流程经验 |
| 是否存调查结论 | 否 | 否 |
| 何时有用 | 审查中途、后续批次之前 | 重复审查之间 |

## 三种压缩模式

- `Compaction()` 自动压缩：上下文压力需要时，交给 SDK 决定
- 阈值压缩：设置明确阈值，行为可预测
- 强制检查点压缩：在应用定义的阶段边界压缩

## 最佳实践

压缩：

- 在有意义的工作流边界压缩
- 为下一阶段保留足够的工作状态
- 把被引用的事实留在生成的产物里

记忆：

- 只用于稳定的流程经验与用户偏好
- 个案事实留在复核过的产物里
- 在依赖之前，先检查生成的记忆

## 结论

你现在拥有构建可靠长周期 agent 工作流的积木：沙箱工作区、清单、压缩、记忆，以及作为可复核调查产物的生成备忘录。
