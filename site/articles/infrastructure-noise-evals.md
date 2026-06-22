---
title: "Quantifying infrastructure noise in agentic coding evals"
org: "Anthropic"
date: 2026-02-05
source_url: "https://www.anthropic.com/engineering/infrastructure-noise"
tags: ["Agent", "Eval/评测"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Quantifying infrastructure noise in agentic coding evals

## 核心观点

**基础设施配置可显著偏移 Agent 编程基准分数。** 在 Terminal-Bench 2.0 上，最宽松与最严格的资源配置之间成功率差距达 6 个百分点（p<0.01），而排行榜顶级模型间的差距往往也只有几个百分点。这意味着一个"2分领先"可能反映的是硬件差异而非能力差异。

**资源配置存在两种作用区间，3x 是关键阈值。** 在 3x 以下，额外资源主要修复基础设施可靠性问题——减少瞬时内存峰值导致的 OOM kill，基础设施错误率从 5.8% 降至 2.1%（p<0.001），但成功率变化在噪声范围内（p=0.40）。在 3x 以上，额外资源开始帮助 Agent 尝试原本行不通的解法（安装大型依赖如 pandas/networkx/scikit-learn、运行内存密集型测试套件），实质上改变了测试所衡量的内容，成功率再跳升约 4pp。

**容器运行时资源执行方式存在两个参数，应分别指定。** 容器资源限制有两个参数：保证分配（guaranteed allocation）和硬限制（hard kill threshold）。将两者设为同一值会导致零余量，任何瞬时内存波动都可能误杀本可成功的容器。Terminal-Bench 官方排行榜使用更宽松的 sandbox provider 隐式允许临时超分配。建议 eval 设计者分别指定两个参数，并通过实验将分数在上下限的波动控制在噪声范围内。

**Agent 评测是端到端系统测试，任何组件都可能成为混淆变量。** 除资源外，时间限制、集群健康、硬件规格、并发度、出口带宽乃至一天中的时段（API 延迟随流量变化）都可影响评测结果。"模型能力"和"基础设施行为"之间的边界比单一 benchmark 分数所呈现的更加模糊。

**实践建议：低于 3pp 的排行榜差距应保持怀疑。** 资源配置应被视为一类实验变量，与 prompt 格式、采样温度同等严格地文档化和控制。Benchmark 维护者应不仅发布推荐配置，还应标准化资源执行方法论（guaranteed allocation 与 kill threshold 分离、报告具体倍数）。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Infrastructure noise（基础设施噪声）** | 与模型能力无关、由评测环境配置引起的分数波动 |
| **Guaranteed allocation** | 容器运行时预先保留的资源量，确保容器能获得该量资源 |
| **Hard kill threshold** | 容器超过该资源量时被强制终止的上限 |
| **OOM kill** | Out-of-Memory kill，容器因超出内存限制被操作系统杀死 |
| **Resource headroom（资源余量）** | Guaranteed allocation 与 kill threshold 之间的缓冲空间 |
| **Terminal-Bench 2.0** | 面向 Agent 编程能力的基准测试，2.0 版本按任务指定推荐 CPU/RAM |
| **SWE-bench** | 业界广泛使用的软件工程 Agent 基准测试，资源敏感度相对较低 |
| **Infra error rate（基础设施错误率）** | 因 pod/容器错误（非模型能力）导致任务失败的比率 |
| **Resource confounder（资源混淆变量）** | 资源配置对评测结果的非预期影响，可能掩盖真实的模型能力差异 |
| **3x headroom 经验法则** | 将 kill threshold 设为 guaranteed allocation 的3倍，可在减少 infra 错误的同时不改变评测实质难度 |

## 相关概念

- concepts/agent-evaluation — Agent 评测的完整方法论，本文为其新增基础设施噪声维度
- concepts/harness-engineering — Eval Harness 工程，本文聚焦容器资源配置的实验设计
- concepts/agentic-systems — Agent 系统的定义与分类

## 相关实体

- entities/anthropic — 本文作者所在机构，在 GKE 上进行 Terminal-Bench 2.0 评测实验
