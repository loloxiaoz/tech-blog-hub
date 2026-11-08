---
title: "Build an Agent Improvement Loop with Traces, Evals, and Codex（构建 Agent 改进闭环：追踪、评测与 Codex 交接）"
org: "OpenAI"
date: 2026-05-12
source_url: "https://cookbook.openai.com/examples/agents_sdk/agent_improvement_loop_with_traces_evals_and_codex"
tags: ["OpenAI", "Codex", "Evals", "Agent", "Traces"]
summary_zh: "用 OpenAI Agents SDK 搭一个财务分析师 Agent，把 traces → 反馈 → Promptfoo 评测 → HALO 优化 → Codex 交接串成改进飞轮，让每次运行的经验都沉淀下来。"
summary_en: ""
---

# Build an Agent Improvement Loop with Traces, Evals, and Codex（构建 Agent 改进闭环：追踪、评测与 Codex 交接）

## 改进飞轮

这个 notebook 为一个 agent 构建改进闭环：

1. 创建一个由 OpenAI Agents SDK 支持的财务分析师
2. 在合成公司数据上运行，捕获 trace
3. 加入来自这些运行的人类与模型反馈
4. 把反馈变成 Promptfoo 评测
5. 用 HALO 排列下一轮 harness 改动的优先级，并写出 Codex 可直接执行的交接

这里的 harness 指模型周围的完整契约：指令、工具、路由、输出要求、校验检查。

## 你会构建什么

- Agents SDK 支持的财务分析师，审查虚构公司的尽调材料
- 覆盖带 trace 运行的人类与 LLM 反馈
- 自动生成的 Promptfoo 评测套件
- 基于 trace、反馈与评测结果的 HALO 优化
- 面向开发者的 Codex 交接，用于实现 harness 改动

## 步骤 1：创建合成公司数据

FictionalCorp XYZ 是一家收入智能 SaaS 公司，ARR 4,300 万美元，增长 71%。

合成文件：

- `overview.md`：管理层摘要
- `product_strategy.md`：路线图 + 未经验证的 NRR 估计
- `go_to_market.md`：销售动作背景
- `board_deck.md`：打磨过的管理层叙述
- `financials/revenue_recognition_notes.md`：会计背景
- `legal/contracts_summary.md`：合同层面的风险
- `legal/open_issues.md`：未决法律事项
- `security/security_overview.md`：SOC 2 状态
- `sales/security_faq.md`：销售口径的安全说明
- `notes/qa_log.md`：尽调问答

刻意埋入的冲突（为改进而设计）：

- 董事会口径 ARR（4,300 万）≠ 财务口径 ARR（3,690 万）
- NRR 估计 122% 是管理层估计，未经财务验证
- 销售 FAQ 说 SOC 2「已完成」≠ 实际 Type II 报告状态
- 前两大客户集中度 34%，管理层却说是 15%

## 步骤 2：定义 Agents SDK 财务分析师

`AgentConfig` 包含：

- 带证据规则的系统提示
- 工具策略（允许的数据根、必需产物）
- 模型设置（`gpt-5.5`，`reasoning_effort: medium`）
- 运行时校验工具

必需产物：

- `outputs/summary_answer.md`
- `outputs/investment_memo.md`
- `outputs/risk_register.json`
- `outputs/open_questions.md`
- `outputs/citations.json`
- `outputs/evidence_table.csv`

校验工具：

- `data/tools/check_evidence_coverage.py`：对照引用的数据室文件审计草稿中的断言
- `data/tools/validate_output_contract.py`：校验必需产物与 JSON 形状

## 步骤 3：生成带 trace 的运行

5 次带 trace 的运行，问题覆盖：

- 现金跑道与烧钱速度 → 融资风险
- 收入质量，以及该信哪个 ARR 数字
- 母账户合并后的真实客户集中度风险
- 企业安全审查准备度
- 应拒绝推断的无依据指标

每次运行写出：

- 通过 HALO JSONL exporter 导出完整 trace
- 全部 6 个必需产物
- agent 的最终回答

## 步骤 4-8：闭环的其余部分

- 步骤 4：加入人类与 LLM 反馈——对 trace 输出做结构化反馈
- 步骤 5：生成 Promptfoo 评测——把反馈转成可复用的评测套件
- 步骤 6：运行 Promptfoo 验证门——用评测套件测试当前 agent
- 步骤 7：运行 HALO 优化——分析 trace、反馈与评测结果
- 步骤 8：生成 Codex 交接——写出带建议的 `codex_handoff.md`

## 关键设计模式

- trace 导出：从 Agents SDK span 生成本地 HALO JSONL
- 评测生成：反馈 → Promptfoo YAML 配置
- 优化：HALO 按预期提升排列 harness 改动
- 交接：结构化 Markdown，供 Codex 实现改动

## 结论

这个闭环保留了每次运行学到的东西：trace 说明发生了什么，反馈解释什么重要，评测让期望可复用，Codex 执行变更集。
