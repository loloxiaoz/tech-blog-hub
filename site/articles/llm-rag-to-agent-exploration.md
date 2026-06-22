---
title: "从LLM+RAG到Agent：我们团队这一年的AI探索"
org: "RAG 研究"
date: 2026-05-08
source_url: ""
tags: ["Agent", "RAG/检索", "MCP", "Claude Code", "Harness工程"]
summary: "AI落地的真正难点从来不在\"能不能用上\"，而在能不能跑通整条工作流。"
summary_zh: "AI落地的真正难点从来不在\"能不能用上\"，而在能不能跑通整条工作流。"
summary_en: ""
---



# 从LLM+RAG到Agent：我们团队这一年的AI探索

**来源**：微信公众号"冰叔的AI笔记"，entities/bingshu，2026-05-07
**原文链接**：https://mp.weixin.qq.com/s/Nwcxok7roTH0-4mmXIqOCA
**一句话**：一个做直播ToC产品的技术团队，从单点AI嵌入走向体系化Agent落地的一年认知演变与接下来四件事。

---

## 核心主张

AI落地的真正难点从来不在"能不能用上"，而在能不能跑通**整条工作流**。

25年的玩法（LLM+RAG+Workflow）是那个时间点最成熟的做法，每家公司都得走一遍。MCP、Skills、Agent Harness成熟之后，路才有条件变宽——AI从"调一次模型"变成可以"作为体系化工作流运转"。

**AI全栈的真正含义**：不是技术栈意义上的全（前端/后端/数据/模型），而是把技术周围所有上下游环节全部变成AI可协作的形态。代码要AI可读，PRD要AI可解析，运营SOP要Skill化，产品入口要CLI化——任何一环没AI化，整条链路就断在那一环。

---

## 四大主题

### 一、AI Coding：三层规范才能整体提效

**问题**：每个人都用上了AI工具，整体没提效。根本原因在工程基础设施缺失，不在工具本身。

三个具体症结：
1. 无团队级"AI使用分级"（辅助/主力/必须人工把关的边界）
2. 老项目代码不友好——2万行单文件、无文档、随意命名；AI建立项目认知要烧掉大量Token
3. 开发只是工作流的一环，前后端联调/测试/发布仍是瓶颈

**解法：三层规范同时立起来**：
- 代码层：老项目重构、清晰架构分层、每个目录有给Agent定位用的**元文档**（不是给人看的README）
- 组内层：所有SOP固化成Skills，从老员工带新人的"口头规矩"变成AI可调用的标准
- 组间层：接口规范、pb定义、测试介入点变成Agent可识别/校验/串联的结构化约定

详见 concepts/ai-coding-three-layers

### 二、Agent平台：组织级AI化基础设施

**问题**：技术团队的AI化路径（装Cursor/Claude Code/理解MCP）无法直接复制给非技术人员。需要的不是让所有人懂AI，而是让AI变成所有人都能用的工具。

**解法：公司级Agent平台**——技术团队把所有AI工程化能力收口、抽象、封装，业务方用"业务语言"配置Agent。

平台四层下沉：模型层（LLM调用/成本控制/降级）、会话层（上下文/长期记忆）、能力层（Skills/MCP/RAG管理）、基础设施层（授权/审计/追踪/灰度）。

技术团队角色转变：从"自己用AI的人"→"让所有人都能用AI的基础设施团队"。

详见 concepts/agent-platform-middle-layer

### 三、CLI：ToC产品未来的AI调用面

**判断**：APP形态将从"独立入口"变为"被调用的能力提供方"。以前"怎么让用户在界面里多停留"，未来"怎么让AI最快从我这里取到结果"——两套设计哲学完全不同。

**CLI作为现阶段答案**：不再是给开发者用的低级工具，而是产品对外的"AI调用面"。

直播场景演示：用户对AI说"我想看唱歌主播"→AI调CLI拿主播列表→用户说"进去看看"→AI再调CLI进入直播间→整条交互在AI对话窗口里闭环，不需要打开APP。

当前限制：主流AI客户端还不能播放任意来源的实时流。但ChatGPT已和视频平台约定在对话里播视频，口子打开只是时间问题。

详见 concepts/cli-as-ai-interface

### 四、产运×技术新协作范式

**旧范式**：需求单 → 技术排期 → 开发后台页面 → 上线 → 运营点点点 → 再提单。两个恶果：产运想象力被排期卡住；技术精力被无穷后台需求消耗。

**新范式两层**：
1. 技术把公司所有能力做成"AI可调用的积木"：MCP（原子能力入口）+ Skills（固化业务流程）→ 公司级能力池
2. 产运直接与Agent对话：自然语言提需求，Agent拆任务调MCP串Skill给答案，甚至直接执行动作

结果：后台页面消失（但这只是结果）；技术产出物从"具体页面"变成"可组合能力单元"；每多一个MCP/Skill，所有产运能力同步扩展。

详见 concepts/capability-bricks

---

## 关键术语

- **AI全栈**：上下游所有环节AI化，而非技术栈全覆盖
- **元文档**：给Agent建立项目认知的索引，区别于给人看的README
- **AI调用面**：产品为AI可调用而设计的接口层
- **能力积木**：MCP（原子能力）+ Skills（业务流程），可组合、可复用
- **Agent Harness**：模型外的工程框架；同一模型换Harness能力差异巨大（延伸：代码本身也要为Agent调用而设计）

---

## 相关实体

- entities/bingshu — 作者，直播ToC产品技术负责人
- entities/anthropic — MCP和Skills的发布方（文中明确提及）
- entities/mcp — 文中作为"能力积木"的原子能力层协议

## 相关概念

- concepts/ai-coding-three-layers — AI Coding三层规范框架
- concepts/agent-platform-middle-layer — 公司级Agent平台
- concepts/cli-as-ai-interface — CLI作为AI调用面
- concepts/capability-bricks — 能力积木化与新协作范式
- concepts/harness-engineering — Harness概念在本文的工程层延伸
- concepts/agent-skills — Skills在组织SOP固化中的应用

---

## 可信度评注

作者自述为做直播ToC产品的技术团队，所有观点来自实际落地经验，具体问题描述（2万行单文件、单点提效但整体没提效）可信度高。CLI和产运新范式部分目前"才刚开始做技术储备"，属前瞻性判断而非已验证落地。
