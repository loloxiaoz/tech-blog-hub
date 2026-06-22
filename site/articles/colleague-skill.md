---
title: "COLLEAGUE.SKILL: Automated AI Skill Generation via Expert Knowledge Distillation"
org: "AI 工程实践"
date: 2026-05-10
source_url: ""
tags: []
summary: "组织内大量隐性知识（tacit knowledge）——编码规范、review 标准、安全实践、决策模式、沟通风格——分散在聊天记录、代码评审、内部文档、邮件里。"
summary_zh: "组织内大量隐性知识（tacit knowledge）——编码规范、review 标准、安全实践、决策模式、沟通风格——分散在聊天记录、代码评审、内部文档、邮件里。"
summary_en: ""
---



# COLLEAGUE.SKILL: Automated AI Skill Generation via Expert Knowledge Distillation

**来源**：学术论文，`raw/colleague_skill.pdf`
**作者**：Tianyi Zhou, Dongrui Liu, Leitao Yuan, Jing Shao, Xia Hu（上海人工智能实验室）
**GitHub**：https://github.com/titanwings/colleague-skill
**许可**：MIT License

---

## 核心问题

组织内大量**隐性知识**（tacit knowledge）——编码规范、review 标准、安全实践、决策模式、沟通风格——分散在聊天记录、代码评审、内部文档、邮件里。

传统知识转移方法（交接文档、wiki、入职培训）只能捕捉**显性表面**，留不住 nuanced 判断、决策启发式和行为模式。这些知识在人员离职时永久丢失。

COLLEAGUE.SKILL 的方案：**从专家的数字痕迹自动挖掘并蒸馏为可调用的 AI Skill**。

---

## 两段架构

### Part A — Work Skill（工作能力层）

编码领域技术知识，包括：
- 负责的系统与服务
- 编码规范（命名、风格、review 标准）
- API 设计标准、安全实践（输入校验、敏感数据脱敏、注入防护）
- Incident 处理流程
- 经验知识库（如"对外暴露前必须加密用户ID"、"禁止暴露自增主键"）

### Part B — Persona（人格层）

五层行为画像，从强到弱依次：

| 层次 | 内容 |
|------|------|
| **L1 Hard rules** | 不可违反的行为约束，覆盖所有其他层 |
| **L2 Identity** | 角色、公司、级别、MBTI、企业文化归属 |
| **L3 Expression style** | 口头禅、句长、回复延迟模式、emoji 使用、对话模板 |
| **L4 Decision & judgment** | 优先级排序（如 data > feasibility > business logic）、反驳条件、拒绝请求策略 |
| **L5 Interpersonal behavior** | 对上级/同级/下级的差异化行为、压力下的反应 |

**运行时顺序**：receive task → Persona 决定态度 → Work Skill 执行 → 用本人语气输出

---

## 自动化数据采集

所有数据**本地处理，不上传服务器**：

| 数据源 | 采集方式 |
|-------|---------|
| 飞书 | 全量 API 自动采集（消息+文档） |
| 钉钉 | 浏览器自动化 + API |
| Slack | Bot API |
| 微信 | SQLite 导出 |
| 邮件 | .eml / .mbox 解析 |
| PDF / 图片 | Claude 原生读取 |
| 直接粘贴 / MD | 直接输入 |

---

## Skill 生成流程

用户提供三项轻量输入：
1. Alias（别名）
2. 一句话职业简介（公司、级别、角色）
3. 个性描述（MBTI、标签、文化归属）

两条并行分析链路：
- `work_analyzer` → `work_builder` → Work Skill 部分
- `persona_analyzer` → `persona_builder` → Persona 部分

合并输出为一个可在 Claude Code 中直接调用的 `SKILL.md`。

---

## 增量演化机制

Skill 生成后支持三种更新路径：

1. **追加新素材**：新文件/消息只做增量分析，新结论合并进来，不覆盖已有内容
2. **对话纠错**：用户说"他不会这样做，他应该是 X"→ `correction_handler` 将其转为类型化纠错记录，立即生效
3. **版本控制**：每次更新通过 `version_manager.py` 归档历史版本，可回滚到任意历史状态

---

## 使用方式

```bash
/create-colleagues          # 创建
/{slug}                     # 全技能调用
/{slug}-work                # 仅工作能力
/{slug}-persona             # 仅人格层
/list-colleagues            # 列出所有
/colleague-rollback         # 回滚
/delete-colleague           # 删除
```

---

## dot-skill：从同事生成器到通用引擎

colleague-skill 正在演进为 **dot-skill**——任何人都可以被蒸馏为 `.skill`。

**Phase 2 新增人物类型**：
- `/create-colleague` — 同事、导师、下级
- `/create-ex` — 前任、旧友、失联的关系
- `/create-icon` — 公众人物、历史人物
- `/create-self` — 蒸馏自己
- 以及虚构角色

**Phase 3 规划**：多 Skill 协作（`/meeting @zhangsan @lisi`，多角色讨论同一话题）、关系图谱、一键安装、持续进化。

**Phase 4 规划**：多模态——角色专属表情包/贴纸、语音克隆、短视频生成。

---

## Skill 类型抽象架构（v2 设计方向）

核心思路：**不再是"同事生成器"，而是"通用 Skill 生成引擎 + 类型 Preset"**。

```
命令 → Preset → Schema → Generator → 产物
```

**三层拆分**：

| 层 | 职责 |
|----|------|
| **Skill Schema** | 统一元数据结构（身份 / 语义 / 生命周期三层） |
| **Type Preset** | 类型差异配置（prompt bundle、目录规则、身份 framing）|
| **Generator Pipeline** | 通用生成引擎，读 Preset 决策，不感知具体类型 |

**关键原则**：新增类型时只需新增 Preset，不需要复制整套实现（prompt / writer / 目录结构）。

**Collector 与 Preset 解耦**：
- Collector 是 **source adapter**：只负责把外部来源转换为标准化原始材料
- Preset 是 **semantic adapter**：决定材料对应哪个类型、work/persona 怎么切分
- 两者解耦后，不会出现"ex 专属 iMessage collector"这种语义逻辑耦合进采集逻辑的问题

---

## 相关 Wiki 页面

- concepts/persona-distillation — colleague-skill 是人物蒸馏的"组织行为"变体，与 nuwa 的"认知OS"变体并列
- concepts/agent-skills — colleague-skill 是 Agent Skills 的自动化生成实践
