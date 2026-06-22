---
title: "Introducing Claude Opus 4.8（Claude Opus 4.8 发布公告）"
org: "Anthropic"
date: 2026-05-28
source_url: "https://www.anthropic.com/news/claude-opus-4-8"
tags: ["Agent", "Eval/评测", "Claude Code", "安全/对齐", "Harness工程", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Introducing Claude Opus 4.8（Claude Opus 4.8 发布公告）

## 核心观点

**诚实性作为可量化的对齐指标首次突出。** Opus 4.8 将代码缺陷未标记率降低约 4 倍，更主动标记不确定性、拒绝无依据断言，并在分析中主动指出输入/输出缺陷。对齐团队评估显示其"亲社会特征"（支持用户自主性、以用户利益为先）得分创新高，欺骗与配合滥用率大幅低于 Opus 4.7，与 Claude Mythos Preview 持平。

**Agent 能力在多项权威基准上全面领先。** Super-Agent Benchmark 首家完成所有端到端用例；CursorBench 所有 effort 档位均超越前代；Legal Agent Benchmark 首次突破 10% all-pass；Online-Mind2Web 达 84%，超越 GPT-5.5。覆盖编码、法律、金融、计算机操控等场景，工具调用效率更高（更少步骤完成相同任务）。

**Dynamic Workflows 是大规模 Multi-Agent 并行的产品化落地。** Claude Code 新功能（研究预览），支持在单次会话内规划并并行启动数百个子 Agent，运行结束后自动验证输出再汇报用户。实际案例：跨数十万行代码的仓库级迁移，从启动到合并 PR 全程无人工介入。

**Effort Control 正式面向用户开放。** claude.ai 与 Cowork 新增努力等级选择器（high / extra / max），高档位推理更深、质量更好，低档位速度快且消耗 rate limit 更慢。Fast Mode 价格降至前代三分之一（$10/$50 per M tokens）。Opus 4.8 默认 high，与 Opus 4.7 默认档位 token 消耗相当但性能更优。

**Messages API mid-task system entry 改变 Agent harness 设计范式。** 开发者可在 messages 数组中插入 system 类型条目，在 Agent 运行过程中动态更新权限、token 预算和环境上下文，无需破坏 prompt cache 或经由 user turn 中转。对长时运行的自主 Agent 工作流有重要工程价值。

## 关键术语

- **Dynamic Workflows**：Claude Code 新功能，单次会话内并行运行数百子 Agent 并自动验证输出，支持仓库级大规模任务
- **Effort Control**：用户端推理努力等级控制（high / extra / max），平衡质量与速度/成本
- **Fast Mode**：Opus 4.8 以 2.5x 速度运行的加速模式，价格为普通模式的 2x（$10/$50 per M tokens），较前代 Fast Mode 降价 3x
- **Mid-task system entry**：Messages API 新机制，允许在对话数组中动态插入 system 指令而不破坏 prompt cache
- **Model Honesty**：可评测、可训练的模型诚实特征——主动标记不确定性、避免无依据断言、主动指出缺陷
- **Project Glasswing / Claude Mythos**：Anthropic 下一代超旗舰模型项目，能力超越 Opus，目前限网络安全领域小范围测试
- **Prosocial Traits**：对齐评估维度，衡量模型支持用户自主性、以用户利益为先等亲社会行为
- **Super-Agent Benchmark**：企业 Agent 综合评测，覆盖翻译、深度研究、幻灯片制作、数据分析等场景
- **Online-Mind2Web**：网页浏览 Agent 评测基准，Opus 4.8 达 84%
- **Legal Agent Benchmark**：法律 Agent 专项评测，Opus 4.8 首次突破 10% all-pass 门槛

## 相关概念

- concepts/reasoning-effort — Effort Control 的底层机制与档位设计
- concepts/dynamic-workflows — 本次发布的核心新功能，Multi-Agent 并行执行产品化
- concepts/model-honesty — 诚实性作为可量化对齐指标
- concepts/mid-task-system-entry — Messages API 新机制，harness 工程的重要工具
- concepts/multi-agent-systems — Dynamic Workflows 的架构基础
- concepts/harness-engineering — mid-task system entry 改变 harness 设计模式
- concepts/agent-evaluation — 多项 Agent 基准评测（Super-Agent, Legal, Mind2Web）
- concepts/eval-awareness — 对齐评估方法论背景
- concepts/swe-bench-verified — 编码能力评测背景
- concepts/test-time-compute — Effort Control 的计算原理
- concepts/extended-thinking — high/extra/max effort 的技术实现

## 相关实体

- entities/claude-opus-4-8 — 本文主角，Anthropic 旗舰模型新版本
- entities/claude-mythos — Project Glasswing 下一代超旗舰，本文预告
- entities/anthropic — 发布方，对齐评估责任主体
- entities/claude-code — Dynamic Workflows 功能载体
- entities/claude-cowork — Effort Control 新增功能的产品之一
- entities/swe-bench — 编码评测基准参考
- entities/browsecomp — 浏览器 Agent 评测背景（与 Online-Mind2Web 对比）
