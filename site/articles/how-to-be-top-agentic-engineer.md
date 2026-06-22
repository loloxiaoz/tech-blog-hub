---
title: "如何成为顶级 Agentic 工程师"
org: "AI 工程实践"
date: 2026-03-06
source_url: "https://x.com/systematicls/status/2028814227004395561"
tags: ["Agent", "安全/对齐"]
summary: "作者用最素的配置（基础 CLI）做着有史以来最有突破性的工作。"
summary_zh: "作者用最素的配置（基础 CLI）做着有史以来最有突破性的工作。"
summary_en: ""
---



# 如何成为顶级 Agentic 工程师

## 核心洞见

> **你不需要最新的 agentic harness，不需要装一堆包，更不需要每天刷新资讯才能保持竞争力。你的"卷劲"本身可能才是最大的障碍。**

作者用最素的配置（基础 CLI）做着有史以来最有突破性的工作。

## 原则 1：越简洁越好（随模型进化更新）

**核心逻辑**：每一代新 agent 都会改变什么是最优解，堆复杂结构是把自己锁定在"针对不存在问题"的解法里。

判断一个工具是否值得用：**如果 OpenAI 和 Claude 都实现了或收购了某个东西，那它大概率真的有用。** （Skills、memory、planning 都是这样进化来的）

偶尔更新 CLI，看更新日志——这已经够了。

## 原则 2：上下文就是一切（对抗 Context Bloat）

> 只给 agent 完成任务所需的精确信息，不多一个字。

**分离研究与实现**：
- 不要说"去搭建一个认证系统"（agent 要研究所有方案，上下文膨胀）
- 要说"用 JWT 实现认证，bcrypt-12 做密码哈希，refresh token 轮换，7 天过期"（直接实现）
- 不知道具体实现时：先跑研究任务，**另起干净上下文**再执行

CLAUDE.md 应该是**逻辑目录**，包含 IF-ELSE 导航逻辑，本身尽可能精简。

## 原则 3：主动利用"讨好性"（Sycophancy）

Agent 天然倾向于同意和执行指令——这是优势也是陷阱。

**中性提示**：不说"找数据库里的 bug"，而说"通读数据库代码，汇报所有发现"。

**对抗型多 Agent 模式**（Bug 审查实例）：
1. **查找 Agent**：找到低影响 bug +1分，严重 bug +10分（热情找一切可能）
2. **对抗 Agent**：推翻一个 bug 得该 bug 的分，但推翻错了扣 2 倍（谨慎攻击）
3. **裁判 Agent**：谎称有正确答案，判对 +1、判错 -1（认真综合判断）

## 原则 4：给 Agent 明确的终点

**Tests = 最好的终点标准**：不允许修改测试，所有测试通过才算完成。

**CONTRACT.md**：为每个任务创建合同文件，包含测试、截图验证等，不满足不允许结束 session。

**Stophook**：在所有 contract 完成前，不允许 agent 终止 session。

## 原则 5：上下文压缩后重新抓取

每次 compaction 之后重新读取任务计划和相关文件，再继续工作——带来显著稳定性提升。

## 原则 6：一个 contract 一个新 session

长时间单 session = 上下文膨胀 + 不同任务互相污染。

**更好的做法**：有任务 → 生成 contract → 开新 session 执行 → 编排层管理。

## Rules + Skills 累积管理

- **Rules**：不想让 agent 做某事，写成规则，告诉它在特定场景读哪个规则文件
- **Skills**：希望 agent 用特定方式做某事，先让 agent 研究它会怎么做，把方法写成 skill 文件，再引用
- 定期让 agent **清理和整合**规则/技能，消除矛盾

## 相关概念

- concepts/harness-engineering — Harness 工程的实践层
- concepts/agent-skills — Skills 的具体设计
- concepts/agentic-systems — Agent 系统基础
- concepts/agent-evaluation — Tests 作为任务完成标准
