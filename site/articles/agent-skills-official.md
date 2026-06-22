---
title: "Equipping agents for the real world with Agent Skills"
org: "AI 工程实践"
date: 2025-10-16
source_url: ""
tags: ["Agent", "Eval/评测"]
summary: "原文：https://www.anthropic.com/engineering/agent-skills-equipping-agents"
summary_zh: ""
summary_en: "原文：https://www.anthropic.com/engineering/agent-skills-equipping-agents"
---



# Equipping agents for the real world with Agent Skills

原文：https://www.anthropic.com/engineering/agent-skills-equipping-agents
发布：2025年10月16日 | 更新：2025年12月18日（发布为开放标准 agentskills.io）

## 核心观点

**1. Agent Skills 是通用 Agent 获得领域专业能力的标准化机制**

Skills 是组织成文件夹的指令、脚本和资源集合，核心是 `SKILL.md` 文件。与为每个用例构建碎片化专用 Agent 不同，Skills 让任何人都能通过封装和共享程序性知识，将通用 Agent 专化为满足特定需求的专业 Agent。构建 Skill 类比于为新员工准备入职指南。

**2. 渐进式披露（Progressive Disclosure）使 Skill 内容量趋于无上限**

三层加载机制：
- **第一层**：`name` + `description`（Agent 启动时预加载进系统提示，用于触发判断）
- **第二层**：完整 `SKILL.md` 内容（Agent 判断 Skill 与当前任务相关时按需加载）
- **第三层及以上**：`SKILL.md` 引用的额外文件（Claude 按需自主导航发现）

因为有文件系统和代码执行工具，Agent 无需将 Skill 全部读入上下文，可打包的知识量在实践中「effectively unbounded」。

**3. Skills 可内嵌可执行代码，补充 LLM 的确定性能力短板**

LLM 擅长语言任务，但排序、表单字段提取等算法操作更适合传统代码执行——更高效且具备确定性。Skills 可以打包预写 Python 脚本，Claude 可直接运行脚本而无需将脚本或数据加载入上下文，兼得灵活性与可靠性。PDF skill 为典型案例：内嵌脚本提取 PDF 表单字段，Claude 调用脚本而非 token-by-token 重新实现。

**4. Skills 上下文窗口序列（官方描述）**

1. 初始态：系统提示 + 所有已安装 Skills 元数据 + 用户消息
2. 触发：Claude 通过 Bash 工具读取 `pdf/SKILL.md`
3. 深化：Claude 读取 `forms.md`（Skill 内部子文件）
4. 执行：携带完整 Skill 指令完成用户任务

**5. 构建与评测 Skills 的最佳实践**

- **从评测出发**：先跑 Agent 在代表性任务上的表现，识别能力缺口，再针对性构建 Skill
- **结构化分拆**：SKILL.md 过长时拆分为子文件并引用；互斥或罕见场景的上下文分路径存储以节省 token
- **从 Claude 视角看**：监控实际触发路径，重点关注 `name` 和 `description` 的准确度（Claude 用这两者决定是否触发）
- **与 Claude 迭代**：让 Claude 将成功做法和常见错误主动写入 Skill，而非提前预测所有需求

**6. 安全注意事项**

恶意 Skills 可能引入漏洞或指令 Claude 外泄数据。建议：
- 只安装可信来源的 Skills
- 不可信来源需完整审计文件内容，尤其是代码依赖和外部网络连接指令
- 关注内嵌图片或脚本等捆绑资源

## 关键术语

| 术语 | 定义 |
|------|------|
| **Agent Skills** | 包含 SKILL.md 的文件夹，打包指令、脚本和资源，供 Agent 动态发现并加载以执行特定任务 |
| **SKILL.md** | Skill 的核心文件，必须以包含 `name` 和 `description` 的 YAML frontmatter 开头 |
| **渐进式披露** | 将 Skill 信息分层（元数据→核心→细节），按需加载，最小化上下文占用 |
| **Progressive Disclosure** | 同上，英文术语 |
| **PDF skill** | Anthropic 官方示例 Skill，为 Claude 添加 PDF 操纵能力（含表单填写），内嵌 Python 脚本提取表单字段 |
| **Skills 触发** | Claude 根据当前任务匹配 Skill 的 name/description，决定是否读取完整 SKILL.md |
| **可执行 Skill** | 内嵌代码脚本的 Skill，Claude 可直接执行而无需将代码加载入上下文 |
| **agentskills.io** | Agent Skills 开放标准网站（2025年12月发布），支持跨平台移植 |
| **Claude Agent SDK** | Anthropic 提供的 Agent 开发 SDK，原生支持 Skills |

## 相关概念

- concepts/agent-skills — Agent Skills 完整概念页（含标准结构、与 MCP 对比、生态数据）
- concepts/context-window — Skills 的渐进式披露本质是上下文窗口管理优化
- concepts/context-engineering — 动态组装最优上下文，Skills 是其中的「专业知识层」
- concepts/harness-engineering — Skills 是 Harness 工程体系中最关键的能力模块
- concepts/aci — Skills 中工具设计与 Agent-Computer Interface 原则
- concepts/agentic-systems — Skills 如何让通用 Agent 专化，对应 Workflow vs Agent 区分

## 相关实体

- entities/anthropic — Skills 作者所在公司，将 Skills 发布为开放标准
- entities/claude-code — 原生支持 Skills 的核心 Agent 平台，PDF skill 案例即在 Claude Code 场景下展示
- entities/mcp — Skills 与 MCP 互补：Skills 负责流程知识，MCP 负责工具连通；Anthropic 计划探索两者协同
