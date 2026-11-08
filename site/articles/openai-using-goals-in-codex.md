---
title: "Using Goals in Codex（在 Codex 中使用 Goals）"
org: "OpenAI"
date: 2026-05-09
source_url: "https://cookbook.openai.com/examples/codex/using_goals_in_codex"
tags: ["OpenAI", "Codex", "Agent"]
summary_zh: "Goals 是 Codex 中跨轮次持续的目标契约：定义完成条件、验证方式与约束，让线程在空闲后继续工作，直到有证据证明目标达成。它不是后台自主性，而是用户可控的完成合同。"
summary_en: ""
---

# Using Goals in Codex（在 Codex 中使用 Goals）

## 什么是 Goal

Goals 是 Codex 中的持久目标，让一个线程跨轮次持续朝既定结果工作。Goal 给 Codex 一个完成条件：什么应当为真、如何验证成功、哪些约束必须保持。

Goal 不是后台自主性，而是一份有范围、用户可控的完成契约。

读完本指南，你将能够：

- 判断什么时候 Goal 比一次性提示更合适
- 写出一个带可度量结果、验证面与约束的 Goal
- 用 `/goal`、`/goal pause`、`/goal resume`、`/goal clear` 管理生命周期

## 快速开始

安装或更新 Codex（Goals 从 0.128.0 起可用）：

```bash
npm install -g @openai/codex@latest
codex --version
```

用 `/goal` 加上结果来设置：

```
/goal Reduce p95 latency below 120 ms without regressing correctness tests
```

生命周期：

```
/goal          # 查看当前 Goal
/goal pause    # 暂停
/goal resume   # 恢复
/goal clear    # 移除
```

## Goals 与 Prompts 的区别

| | Prompt | Goal |
|---|---|---|
| 循环 | 提问 → 工作 → 结果 → 等待 | 工作 → 检查 → 继续或完成 |
| 含义 | 做下一件事 | 持续做到这个结果为真 |

Prompt 让 Codex 做下一件事；Goal 给它一条终点线。工作仍然必须用证据审计，而不是因为模型「觉得」完成了。

## 如何写 Goal

一个好的 Goal 定义六件事：

1. **结果**：工作完成时什么应当为真
2. **验证面**：证明它的测试、基准、报告或产物
3. **约束**：Codex 工作时不能破坏什么
4. **边界**：可以使用哪些文件、工具或资源
5. **迭代策略**：每次尝试后如何决定下一步
6. **阻塞停止条件**：什么时候应当停下并报告

弱：

```
/goal Improve performance
```

强：

```
/goal Reduce p95 checkout latency below 120 ms, verified by checkout benchmark,
while keeping correctness suite green. Use only checkout service, benchmark
fixtures, and related tests. Between iterations, record what changed,
what benchmark showed, and next best experiment to try. If benchmark
cannot run or no valid paths remain, stop with attempted paths,
evidence gathered, the blocker, and next input needed.
```

## Goal 激活后有什么变化

- **目标始终可见**：附着在线程上，跨轮次存在
- **可以继续**：Goal 激活且在预算内时，Codex 可以从空闲线程继续
- **完成必须基于证据**：不是因为模型相信自己做完了

## Codex 里 Goal 是怎么实现的

Goal 是持久化的线程状态，不是全局记忆。架构上，它记录：

- 目标
- 生命周期（active / paused / complete / budget-limited）
- 预算核算
- 进度核算

Codex 只在安全边界检查是否继续：

- 一轮已经结束
- 没有其他待办工作
- 没有排队等待的用户输入
- 线程处于空闲

## 把弱 Goal 变强

### 性能调优

弱：`/goal Improve performance`
强：`/goal Reduce p95 latency below 120 ms on checkout benchmark while keeping correctness tests green`

### 修复不稳定的测试

弱：`/goal Fix the failing checkout test`
强：`/goal Make checkout test suite pass on current branch without changing public API behavior. Verify by running full suite. If test is non-deterministic, document reproduction steps and recommended stability fix.`

### 复现论文

弱：`/goal Reproduce the paper`
强：`/goal Produce strongest evidence-backed reproduction of Bühlmann et al., "Deep Hedging," using available paper materials and local resources. Attempt every headline result, verify outputs where possible, and end with report that separates confirmed findings, approximate reconstructions, blocked claims, and remaining uncertainty.`

## 用 Goals 做复杂研究

研究型 Goal 应当：

- 把论文拆成论点清单
- 把论点映射到可获得的证据
- 诚实标注阻塞项（没有原始训练状态就无法精确重放）
- 产出区分「已确认 / 近似重建 / 被阻塞 / 仍不确定」的审计报告

## 什么时候不要用 Goals

- 一行修改、简单解释、短代码评审 → 用普通 prompt
- 终点模糊 → 不要用 Goal
- 想隐藏不确定性 → 不要用 Goal（把不确定性写进 Goal）

Goals 在任务同时具备三个属性时最强：

- 持久的目标
- 基于证据的终点
- 可能需要多轮调查的路径

## 结论：让目标持续，让证据决定

Goals 改变了 Codex 的工作模型：从一串孤立的提示，变成围绕既定结果的有状态工作循环。

这个架构是有意设限的：Goal 限定在一个线程内，携带生命周期状态与预算核算，可以被暂停、恢复、清除、完成，或因预算停止。

对复杂研究而言，这就是「生成一个答案」与「产出可审计的工件」之间的差别。
