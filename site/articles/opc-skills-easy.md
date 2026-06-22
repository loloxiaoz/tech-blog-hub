---
title: "Easy OPC Agent Skills 集（9 个）"
org: "AI 工程实践"
date: 2026-05-24
source_url: ""
tags: ["Agent", "Claude Code", "安全/对齐"]
summary: "每个 Skill 都遵循相同的目录结构（与 [[concepts/agent-skills]] 标准对齐）："
summary_zh: "每个 Skill 都遵循相同的目录结构（与 [[concepts/agent-skills]] 标准对齐）："
summary_en: ""
---



# Easy OPC Agent Skills 集（9 个）

**来源**：[GitHub: easychen/opc-methodology/skills/](https://github.com/easychen/opc-methodology/tree/main/skills)
**作者**：Easy（陈一斌 / @easychen）
**新增日期**：2026-04
**网站**：[https://opc-skills.ft07.com/](https://opc-skills.ft07.com/)
**视频讲解**：[B 站 BV1JMDQBiEjx](https://www.bilibili.com/video/BV1JMDQBiEjx)
**位置**：`~/devspace/opc-methodology/skills/`

> 这是 sources/opc-methodology-easy 一书的 **Skills 化落地**——把整套方法论封装成 9 个可被 Codex/Claude Code 等 Agent 调用的 SKILL.md 工程包，跑出"建盘期 + 运营循环"的完整工作流。是本 wiki 看到的**最完整、最专业的生产级 Agent Skills 实战参考**，远超 sources/colleague-skill 和 sources/nuwa-skill 的设计深度。

---

## 整体架构

每个 Skill 都遵循相同的目录结构（与 concepts/agent-skills 标准对齐）：
```
opc-{skill-name}/
├── SKILL.md            # 主 Skill 文件（含 frontmatter）
├── agents/openai.yaml  # Codex/openai-agents 的注册配置
└── references/         # 该 Skill 自带的方法论参考资产（2-3 个 md）
```

Skills 集分为 3 个层次：

```
            opc-orchestrator（00 总编排）
           ├── 路由 + 用户模式判断 + 阶段越界管控
           │
建盘期 ─────┬─→ 01 opc-resource-audit（资源盘点）
（线性，   ├─→ 02 opc-niche-positioning（利基定位）
 一次性） ├─→ 03 opc-value-proposition（价值主张）
           ├─→ 04 opc-business-model-design（商业模式）
           ├─→ 06 opc-mvp-designer（MVP 设计）
           └─→ 07 opc-conversion-loop（转化闭环）
                          ↓
              ↓ 建盘期完成 → 进入执行阶段 ↓
                          ↓
运营循环 ──┬─→ 08 opc-asset-ops（资产沉淀，无固定顺序，可重复）
（无固定 └─→ 09 opc-dashboard-review（经营复盘，无固定顺序，可重复）
 顺序）
```

注：阶段编号 05 在文档中跳过（按 Easy 一贯的灵活编号习惯）。

---

## 9 个 Skills 详解

### 00 opc-orchestrator（总编排器）

**职责**：判断用户阶段 + 用户对方法论术语熟悉度 + 选择交互模式 + 决定下一步调用哪个 Skill + **确保对话先行、文件随后**。

**用户模式三档**：
- **教学模式**：每步先解释做什么、解释术语、说明在整体流程中的作用
- **引导模式**：解释关键概念，保持问题简洁，通过选项和反馈帮用户表达
- **直通模式**：减少解释，保留关键确认和对话摘要

**阶段越界严格管控**（最值得借鉴的设计）：

每个 Skill 严格限定"只做这些 / 绝不做这些"，例如：
- 01 资源盘点：只摸资源，**不分析方向、不判断偏好、不评估风险承受力**
- 02 利基定位：三环叠加+六维评分，**不写文案、不选平台、不定价**
- 03 价值主张：拆 Jobs/Pains/Gains，**不写广告话术、不做选题、不定价**

**越界处理协议**：
> "这个属于[X 阶段]的范围，我们到那一步专门处理。现在先把当前阶段完成。"

**用户跳步处理协议**（三步走）：
1. 说清跳步代价 + 二选一确认
2. 用户确认后立即切换技能，**不在当前对话预讨论目标阶段**
3. 被跳过阶段在 `current-stage.json` 做标记

**会话恢复协议**（每次新会话第一件事）：
1. 读 `opc-doc/state/current-stage.json`
2. 读 `opc-doc/state/decisions.json`
3. 读当前阶段对应 outputs 目录
4. 向用户展示"上次进度摘要"，等用户确认是否继续

**首轮三件事**（不立刻抛业务问题）：
1. 询问用户对方法论/精益创业/利基/价值主张/精益画布的熟悉度
2. 判断用户更适合哪种模式
3. 询问是否希望术语边走边解释

**默认决策模板**：3 个备选 + `4. 我有自己的方案`

**层级越界自检**（每轮输出前先做）：
- 当前阶段属于哪个层级（战略 / 验证 / 执行）？
- 准备输出的内容是否超出该层级边界？
- 是否因为"理解太充分"而自动滑入执行层？

References：
- `file-contract.md` — 目录契约
- `interaction-protocol.md` — 统一交互方式
- `stage-map.md` — 阶段判断

### 01 opc-resource-audit（资源盘点）

**唯一产出：资源清单**。按 8 个类别逐一确认 + 深挖每项资源（分布、可用方式、代价）。

绝不做：方向分析、偏好评价、风险承受力评估——那些是后续 Skill 的工作。

References：
- `resource-categories.md` — 8 个资源类别定义
- `scoring-rubric.md` — 资源评分标准

### 02 opc-niche-positioning（利基定位）

**框架：三环合一 + 六维评分**

三环：
- **环 1：新杠杆与元杠杆**——代码/媒体/AI（详见 concepts/leverage-types）
- **环 2：边界变动带来的新机会**——技术/信息传播/政策三类边界变动
- **环 3：创始人独有资源和优势**

三环重叠 = 最优利基，再用六维评分进一步筛选确认。

References：
- `market-scan-checklist.md`
- `niche-evaluation.md` — 六维评分模型
- `positioning-formula.md`

### 03 opc-value-proposition（价值主张）

**框架：Jobs / Pains / Gains**（Value Proposition Canvas）

只做"为什么买你"的结构化分析，不进入话术或内容创作。

References：
- `messaging-template.md`
- `vpc-lite.md` — VPC 轻量版

### 04 opc-business-model-design（商业模式设计）

**框架：Lean Canvas + 轻量商业模式画布**

一次只填一个模块，不一次性填完整张画布。识别高风险假设。不进入 MVP 设计或运营 SOP。

References：
- `bmc-lite.md` — 商业模式画布轻量版
- `lean-canvas-lite.md` — Lean Canvas 轻量版
- `pricing-checklist.md` — 定价清单

### 06 opc-mvp-designer（MVP 设计）

**核心认知矫正：MVP 不是"简陋产品"，而是"最小验证"**

确定最先验证什么 + 最小验证形式（服务先行 / 内容验证 / 工具原型等）+ 划定边界 + 明确成功标准。

不做：具体内容文案、交付 SOP。

References：
- `experiment-template.md`
- `mvp-patterns.md` — 各种 MVP 模式

### 07 opc-conversion-loop（转化闭环）

**框架：触达 → 承接 → 成交**

确认目标渠道 + 线索承接方式 + 第一次成交动作 + 完整路径结构。

不做：具体帖子骨架、文案。

References：
- `channel-playbook.md`
- `conversion-patterns.md`

### 08 opc-asset-ops（资产沉淀）

**核心认知：复利 = 让重复出现的成果沉淀为可复用资产**。

识别哪些成果值得沉淀（判断而非执行）+ 资产类别和优先级 + 资产沉淀方案（规划层）。

不做：直接生产资产内容（除非用户明确要求）。

**触发条件**：有东西开始重复出现、想系统化沉淀。

References：
- `asset-taxonomy.md` — 资产分类
- `knowledge-structure.md` — 知识结构化方法

### 09 opc-dashboard-review（经营复盘）

**核心认知：复盘不是流水账，而是找瓶颈**。

经营状态摘要 + 主要瓶颈识别 + 下周期优先重点确认。

**触发条件**：运营卡住找不到问题；周期性回顾。

**优先确认顺序**：
1. 最近最卡的地方
2. 最可能的瓶颈类型

References：
- `review-metrics.md` — 复盘指标
- `stop-loss-rules.md` — 止损规则
- `weekly-review-template.md` — 周度复盘模板

---

## 这套 Skills 集为什么值得参考

### 1. 阶段边界管控是 Skill 工程的最佳实践
每个 Skill 都用"做这些 / 不做这些"二元表显式划界，再加 orchestrator 的层级越界自检——**几乎杜绝了 Skill 互相串台的失败模式**。这与 concepts/agent-skills 中"渐进式披露"和"作用域明确"的原则完全一致。

### 2. 用户模式三档是面向不同熟悉度用户的优雅解法
教学/引导/直通三档不只是"详略差别"，而是问题密度和确认密度的差别。这是把 concepts/persona-distillation 的"诚实边界"和"分层提炼"思想运用到 UX 层。

### 3. 文件状态机 + 会话恢复协议
`opc-doc/state/current-stage.json` 等状态文件让多次对话之间能无缝接续——这正是 concepts/memory-systems 中"持久状态"在 Skill 工程层面的实现，与 Claude Code 的 CLAUDE.md 三层记忆机制（参见 entities/claude-code）异曲同工。

### 4. "对话先行，文件随后"原则
**用户确认前，不把单一结论写入正式产物**——这是经典的 human-in-the-loop 模式，与 concepts/spec-driven-development 的"先在 Markdown 改而不是改代码"逻辑相通：把决策成本左移到对话层。

### 5. 决策模板 3 + 1（"我有自己的方案"）
默认 3 个备选 + 第 4 个永远是"我有自己的方案"——这是把 LLM 从"决策代理"降级回"决策辅助"，与 sources/spec-is-code / sources/how-to-be-top-agentic-engineer 中"AI 是放大器而不是替代品"的论调一致。

---

## 实战调用方式

支持的运行环境：
- Codex（通过 `agents/openai.yaml` 注册）
- Claude Code（通过 SKILL.md frontmatter 即可被识别）

预设共享目录：当前工作目录下的 `opc-doc/`，包含：
- `state/` — 4 个状态 JSON（current-stage / decisions / assumptions / user-preferences）
- `inputs/` — 用户提供的输入素材
- `outputs/` — 各阶段产物（按阶段编号命名子目录）

---

## 相关页面

- sources/opc-methodology-easy — 这套 Skills 背后的方法论书
- entities/easy-easychen — 作者
- concepts/opc — OPC 核心概念
- concepts/agent-skills — Skills 标准
- concepts/persona-distillation — 用户模式三档的方法论根基
- concepts/spec-driven-development — "对话先行，文件随后"的同源逻辑
- concepts/cognitive-arbitrage — 整套 Skills 的最终目的：把创业者的认知套利杠杆化
- sources/colleague-skill / sources/nuwa-skill — Skills 工程的另两种参考形态（行为蒸馏 / 认知蒸馏）
