---
title: "nuwa-skill：人物思维蒸馏方法论"
org: "AI 工程实践"
date: 2026-05-10
source_url: ""
tags: ["Agent", "Claude Code"]
summary: "colleague-skill 证明了\"把人蒸馏成 AI Skill\"是可行的。既然能蒸馏同事，为什么不去蒸馏芒格、费曼、纳瓦尔？"
summary_zh: "colleague-skill 证明了\"把人蒸馏成 AI Skill\"是可行的。既然能蒸馏同事，为什么不去蒸馏芒格、费曼、纳瓦尔？"
summary_en: ""
---



# nuwa-skill：人物思维蒸馏方法论

**来源**：GitHub 项目 `alchaincyf/nuwa-skill`，作者花叔（Huashu/AlchainHust）
**类型**：Claude Code Skill + 方法论文档
**核心文件**：`SKILL.md`（执行流程）、`references/extraction-framework.md`（提炼方法论）、`references/skill-template.md`（输出模板）

---

## 核心主张

colleague-skill 证明了"把人蒸馏成 AI Skill"是可行的。既然能蒸馏同事，为什么不去蒸馏芒格、费曼、纳瓦尔？

**关键区分**：nuwa 提炼的不是"他说过什么"（语录复读机），而是"他怎么思考"——认知操作系统（cognitive OS）。

> "女娲造的不是人，是一面镜子。"

---

## 五层提炼模型

| 层次 | 提炼内容 |
|------|---------|
| 表达层 | 表达 DNA：语气、节奏、词汇偏好 |
| 思维层 | 心智模型、认知框架（核心） |
| 判断层 | 决策启发式 |
| 价值层 | 绝对不会做的事（反模式） |
| 诚实层 | Skill 真正做不到什么（诚实边界） |

---

## 心智模型三重验证

一个论点要被认定为"心智模型"而非"随口一说"，必须同时通过：

1. **跨域复现**：同一框架在 ≥2 个不同领域出现
2. **生成力**：能推断此人对新问题的可能立场
3. **排他性**：不是所有聪明人都这样想，有区分度

只通过 1-2 重 → 降级为决策启发式；0 重 → 丢弃。

---

## 6 Agent 并行调研框架（Phase 1）

| Agent | 搜索维度 | 输出文件 |
|-------|---------|---------|
| 1 著作 | 书籍、长文、newsletter | `01-writings.md` |
| 2 对话 | 播客、深度采访、AMA | `02-conversations.md` |
| 3 表达 | 社交媒体碎片、风格DNA | `03-expression-dna.md` |
| 4 他者 | 他人分析、批评、传记 | `04-external-views.md` |
| 5 决策 | 重大决策、行为记录 | `05-decisions.md` |
| 6 时间线 | 完整时间线+最近12个月 | `06-timeline.md` |

**硬性要求**：每个 Agent 结果必须落文件，不存文件的调研等于没做。

---

## 完整工程流程（Phase 0-5）

| 阶段 | 工作 |
|------|------|
| Phase 0 | 入口分流：明确人名（直接路径）vs 模糊需求（诊断路径） |
| Phase 0A/B | 需求澄清 / 需求诊断 → 候选推荐 |
| Phase 0.5 | 创建 Skill 目录结构（调研前必须完成） |
| Phase 1 | 6 Agent 并行采集 |
| Phase 1.5 | 调研质量检查点（人工确认后推进） |
| Phase 2 | 框架提炼：心智模型 + 决策启发式 + 表达DNA + 价值观 + 诚实边界 |
| Phase 2.5 | 提炼确认检查点 |
| Phase 3 | 按模板构建 SKILL.md |
| Phase 4 | 质量验证：已知测试 + 边缘测试 + 风格测试 |
| Phase 5 | 双 Agent 精炼（结构评估 + 触发条件评审） |

---

## 诚实边界原则

每个 Skill 必须显式声明局限：
- 不能蒸馏直觉和创造力，框架可提取，灵感不行
- 只是截至调研时间的快照，之后变化未覆盖
- 公开表达 ≠ 真实想法，只基于公开信息
- 调研来源不足时，宁可标注"信息不足"，不强行生成

> "不告诉你局限的 Skill 不值得信任。"

---

## 质量通过标准

| 检查项 | 通过标准 | 不通过信号 |
|--------|---------|-----------|
| 心智模型数量 | 3-7 个，每个有来源证据 | <3 或 >10 |
| 每个模型的局限性 | 明确写出失效条件 | 只写优点 |
| 表达DNA辨识度 | 读100字能认出是谁 | 像通用 ChatGPT |
| 诚实边界 | ≥3 条具体局限 | 只有"不能替代本人" |
| 内在张力 | ≥2 对矛盾 | 观点高度一致（太假）|
| 一手来源占比 | >50% | 主要依赖二手转述 |

---

## 已有 Examples

`naval-perspective`、`elon-musk-perspective`、`munger-perspective`、`feynman-perspective`、`paul-graham-perspective`、`taleb-perspective`、`zhang-yiming-perspective` 等 14 个。

---

## 相关 Wiki 页面

- concepts/persona-distillation — 人物思维蒸馏：核心概念
- concepts/agent-skills — nuwa-skill 是 Agent Skills 的特殊子类型
