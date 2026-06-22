---
title: "Agent Skills：打通可复用专业领域知识的最后一公里"
org: "AI 工程实践"
date: 2026-04-01
source_url: "https://mp.weixin.qq.com/s/PonVlfEFbGLkaDt_1oWfdA"
tags: ["Agent", "MCP", "工具调用"]
summary: "TechCrunch 称 Agent Skills 为 \"AI 领域的 Dockerfile\"——让 AI 能力可移植、可组合、可版本控制。"
summary_zh: "TechCrunch 称 Agent Skills 为 \"AI 领域的 Dockerfile\"——让 AI 能力可移植、可组合、可版本控制。"
summary_en: ""
---



# Agent Skills：打通可复用专业领域知识的最后一公里

## 基本信息

- **来源**：微信公众号，阿里巴巴开发者
- **核心主张**：Skills 是让 AI 从"知道分子"变为"行动专家"的关键，解决 Agent 的"可复用性"问题

## Agent Skills 发展史

| 时间 | 事件 |
|------|------|
| 2025-10-16 | Anthropic 在 Claude 3.7 Sonnet/Opus 中正式推出 Claude Skills |
| 2025-12-18 | Anthropic 联合生态伙伴开源 Agent Skills Specification V1.0，发布官方 SDK（Python/TypeScript/Java） |
| 2026-02 | 公开可用 Skills 超过 85,000 个；支持平台 27 家；Linux 基金会启动纳入讨论 |

TechCrunch 称 Agent Skills 为 **"AI 领域的 Dockerfile"**——让 AI 能力可移植、可组合、可版本控制。

## Skills 的本质与结构

> Skills are organized collections of files that package composable procedural knowledge for agents.

Skills 本质上是一个文件夹：

```
my-skill/
├── SKILL.md       # 必须：SKILL描述、逻辑编排、核心指令
├── scripts/       # 可选：可执行代码（.py、.sh等）
├── references/    # 可选：参考文档、规则、规范
└── assets/        # 可选：静态资源（图片、模板等）
```

**SKILL.md 必要字段**：`name`（≤64字符）、`description`（描述作用和何时使用）

**渐进式披露（Progressive Disclosure）**：SKILL.md 建议控制在 500 行，超出内容按需加载。name 和 description 在启动时加载，其余内容在模型识别到相关任务时才加载——避免无效上下文污染。

## Skills vs Prompt vs MCP 三者分工

| 维度 | Prompt | MCP | Skills |
|------|--------|-----|--------|
| 定位 | 一次性指令 | 工具调用通信协议 | 任务执行标准能力包 |
| 粒度 | 单次对话内 | 工具接口（类似 OpenAPI for AI） | 跨会话独立功能单元（类似 Docker 镜像） |
| 可复用性 | 低 | 中 | **高** |
| 工程化程度 | 脚本级 | 接口级 | 应用级 |

**三者协同**：Prompt 告诉模型当前任务 → 模型匹配合适 Skill → Skill 内部逻辑通过 MCP 调用工具 → 完成闭环。

- Skills ≠ Prompt 替代品，而是 Prompt 的**容器**
- Skills ≠ MCP 替代品，而是 MCP 的**消费者**

## 为什么需要 Skills（解决可复用性问题）

过去方式：通过 Prompt 编排流程 + Function Calling/MCP 定义外部能力 → 本质是精心设计的 Workflow，场景适配性强但**可复用性差**（非 AGI 模式）。

Skills 方案：封装领域沉淀的成熟方法论，不依赖精细 Workflow，借助模型理解能力 + 渐进式披露，**同一个 Agent 基座（Claude Code）通过不断沉淀 Skills 完成专业领域任务**。

> "不需要再建新的 agent，只需要不断沉淀 skills，基于 Claude Code 底座就可以完成以前专业 agent 才能完成的工作。"

## 生态

- Anthropic 官方 Skills：github.com/anthropics/skills
- 规模最大集合 SkillsMP：skillsmp.com
- 最火社区 Skill.sh（每小时新增 550+ 技能）

## 相关概念

- concepts/agent-skills — Agent Skills 详细技术概念
- concepts/harness-engineering — Skills 是 Harness 的关键模块
- entities/mcp — Skills 通过 MCP 调用外部工具
- concepts/tool-retrieval — 大量 Skills 时，检索选择合适的 Skill
