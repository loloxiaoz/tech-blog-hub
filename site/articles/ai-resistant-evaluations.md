---
title: "Designing AI-resistant technical evaluations"
org: "Anthropic"
date: 2026-01-21
source_url: "https://www.anthropic.com/research/ai-resistant-evaluations"
tags: ["Eval/评测"]
summary: "测试发布版（允许无限时间）中 Claude 的表现（单位：时钟周期，越低越好）："
summary_zh: "测试发布版（允许无限时间）中 Claude 的表现（单位：时钟周期，越低越好）："
summary_en: ""
---



# Designing AI-resistant technical evaluations

## 核心观点

**AI 能力迭代正在使传统技术评测快速失效。** Anthropic 性能工程团队自 2024 年初使用一套「模拟加速器代码优化」的带回测试，1000+ 名候选人完成了测试，数十人因此被录用。然而 Claude 3.7 Sonnet 已让 50% 以上候选人委托 AI 更优；Claude Opus 4 在 4 小时内超越几乎所有人类；Claude Opus 4.5 在 2 小时内与最强人类持平。测试设计者被迫三次重写测试。

**「超出分布」比「更难」更能对抗 AI。** 第一次迭代失败后，作者尝试了更难的数据转置问题（TPU register transpose + bank conflict），Claude Opus 4.5 不仅解决了，还发现了作者未想到的优化（计算转置而非数据转置）；用 ultrathink 进一步扩展后完全解决。原因在于：数据转置和 bank conflict 是工程界高频问题，Claude 训练数据极为充足。最终奏效的方案是借鉴 Zachtronics 编程游戏风格——设计极度受限的指令集和极少见的约束环境，让 Claude 无训练先例可循。

**允许 AI 辅助的评测比禁止更难设计，但更贴近真实工作。** 作者拒绝了「禁用 AI」的建议，坚持认为应该能在「与 AI 协作」的环境下评测人类区分度。核心挑战是：Claude 执行速度极快，人类花一半时间在理解问题，在 2 小时内根本无法有效驾驭 AI；主导策略可能退化为「坐等 AI 完成」。真正能评测的能力越来越趋向调试、系统设计、正确性验证、判断力——但这些难以客观量化。

**时间维度是人类相对 AI 最后的优势空间。** 无限时间下，人类最快提交仍显著超越 Claude 的 test-time compute 最优结果。METR 的研究也支持这一点：在足够长的时间维度上，人类专家保持优势。2 小时时间窗口的压缩直接消除了人类的相对优势。

**测试从「模拟真实工作」被迫转向「模拟新颖工作」。** 原版成功正是因为贴近真实性能工程任务（模拟 TPU 架构特性：VLIW、SIMD、scratchpad 内存）；新版的有效性依赖于 Claude 没有先例可循的新颖约束。作者坦言：「原版的成功因为它像真实工作；替代版的成功因为它模拟了新颖工作。真实性可能是我们再也负担不起的奢侈品。」

## 关键术语

| 术语 | 定义 |
|------|------|
| **AI-resistant evaluation** | 在 AI 辅助普及后仍能区分人类能力高低的测试设计方法 |
| **test-time compute harness** | Anthropic 内部的扩展计算测试框架，让模型在更长时间/更多算力下持续优化，用于基准测试 |
| **out-of-distribution (OOD)** | 超出 AI 训练数据分布的任务设计，是评测 AI 抗性的核心原则 |
| **VLIW** | Very Long Instruction Word，多执行单元并行指令集架构，模拟加速器特性之一 |
| **SIMD** | Single Instruction Multiple Data，向量化指令，每条指令处理多个数据元素 |
| **scratchpad memory** | 加速器上手动管理的暂存内存（区别于 CPU 的自动缓存），模拟 TPU 特性 |
| **Zachtronics** | 以极度受限约束和创意编程著称的独立游戏工作室，其游戏风格成为 v3 测试的灵感来源 |
| **ultrathink** | Claude Code 的扩展思考功能，允许更长的思考预算 |
| **带回测试（take-home）** | 候选人在自己环境中独立完成的评测任务，允许更长时间窗口和真实工具使用 |
| **cycle count** | 模拟机器的时钟周期数，作为性能优化任务的客观评分指标（越低越好） |

## 性能基准数据

测试发布版（允许无限时间）中 Claude 的表现（单位：时钟周期，越低越好）：

| 模型/条件 | 周期数 |
|-----------|--------|
| Claude Opus 4（多小时 harness） | 2164 |
| Claude Opus 4.5（随意 Claude Code 会话，约 2h） | 1790 |
| Claude Opus 4.5（2h test-time compute harness） | 1579 |
| Claude Sonnet 4.5（多小时 test-time compute） | 1548 |
| Claude Opus 4.5（11.5h harness） | 1487 |
| Claude Opus 4.5（改进版 harness，多小时） | 1363 |

击败 1487 cycles 即超越 Claude 发布时最佳表现，Anthropic 邀请挑战者投递简历。

## 三版测试演变

| 版本 | 时间窗口 | 被击败者 | 被击败原因 |
|------|---------|---------|----------|
| v1 | 4 小时 | Claude Opus 4 | 贴近真实工程，训练数据充足 |
| v2 | 2 小时 | Claude Opus 4.5 | 2h 内匹配最强人类，test-time compute 持续提升 |
| v3 | 2 小时（现用） | 暂未被击败 | OOD 设计，无调试工具，判断力是核心信号 |

## 相关概念

- concepts/agent-evaluation — Agent 评测体系，本文是其在招聘场景的具体应用
- concepts/harness-engineering — test-time compute harness 是 harness 工程的典型案例
- concepts/agentic-systems — Claude Code 作为 Agent 执行性能工程任务的实例

## 相关实体

- entities/anthropic — 本文作者所在公司，测试服务于 Anthropic 性能工程招聘
- entities/claude-code — 执行 take-home 测试的 AI Agent，测试的「对手」
