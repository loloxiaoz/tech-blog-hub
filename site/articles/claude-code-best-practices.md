---
title: "Claude Code 最佳实践指南（2026年版）"
org: "Anthropic"
date: 2026-05-06
source_url: "https://www.anthropic.com/engineering/claude-code-best-practices"
tags: ["Claude Code"]
summary: "Claude 的上下文窗口（~200K tokens）会快速填满，填满后性能下降——几乎所有最佳实践都围绕这个约束展开。"
summary_zh: "Claude 的上下文窗口（~200K tokens）会快速填满，填满后性能下降——几乎所有最佳实践都围绕这个约束展开。"
summary_en: ""
---



# Claude Code 最佳实践指南（2026年版）

**原文**：知乎专栏《AI 编程》，820 赞
**来源 URL**：https://zhuanlan.zhihu.com/p/2009744974980331332
**版本截止**：2026 年 2 月（Claude Code 发布满一年）
**作者**：Alex Hu
**核心贡献**：整合 Anthropic 官方最佳实践 + Boris Cherny（Claude Code 之父）X 上的真实工作流 + 团队实践模板

---

## 一句话摘要

Claude 的上下文窗口（~200K tokens）会快速填满，填满后性能下降——几乎所有最佳实践都围绕这个约束展开。

---

## 核心观点

### 1. 上下文窗口是第一约束

- 200K tokens 看似很大，但调试会话和代码库探索轻松产生数万 token
- **`/clear` 是最高频命令**：任务切换时必用，干净上下文 + 好提示词 >> 长会话 + 反复修正
- 子代理 = 上下文防火墙：子代理探索代码库，只返回摘要给主会话
- Token 效率目标：基础上下文 < 20K，CLAUDE.md < 2K tokens，每 ~60K tokens 清理一次

### 2. 验证是质量倍增器（B2）

- 不给 Claude 验证手段 = 让它猜；有验证手段时质量提升 **2-3x**
- 四种验证策略：提供测试用例、截图对比、根因修复、指定验证命令
- **TDD 防幻觉**：测试先行，不让 Claude 同时写代码和测试（会写验证错误逻辑的测试）
- 三层保护：提示词约束 + 权限系统 `deny: Write(*_test.go)` + Git 兜底

### 3. 探索→计划→编码 三段论（B3）

- `Shift+Tab` 切换 Plan Mode（只读）→ 探索代码库 → 制定计划 → 切回执行
- `Ctrl+G` 在外部编辑器中编辑计划，可直接修改 Claude 生成的方案
- **SDD（规范驱动开发）**：大型功能先写 spec.md → plan.md → tasks.md，将"发现理解偏差"的成本从改代码左移到改 Markdown
- 第二个 Claude 会话独立审计计划（Boris 的流程）

### 4. 环境配置是长期杠杆（B5/B6/B7/B8）

**CLAUDE.md**（团队记忆）：
- 检验标准：删掉这行 Claude 会犯错吗？不会就删
- 强调语法：`**IMPORTANT**`、`**NEVER**`、`**YOU MUST**` 提高遵从度
- 分层加载：企业策略 > 本地项目 > 共享项目 > 用户级 > 自动记忆

**Hooks**（确定性自动化）：
- 与 CLAUDE.md 规则的区别：CLAUDE.md 是"建议性"，Hooks 是"确定性执行"
- PostToolUse Hook：每次文件编辑后自动 Prettier 格式化（B7）
- PreToolUse Hook：硬性阻止编辑受保护文件
- Stop Hook：验证任务完成度

**Skills**（按需知识）：
- SKILL.md 的两级加载：description 常驻，完整内容按需加载（节省上下文）
- `/simplify`：并行启动 3 个审查代理（复用/质量/效率），PR 前最后一道关卡
- `/batch`：大规模并行迁移，自动拆分任务，每个任务独立 PR

**权限系统**：
- 预批准安全命令而非 `--dangerously-skip-permissions`（B6）
- `deny` 优先 → `ask` → `allow`，首次匹配生效

### 5. 多会话并行是产出倍增器（B11）

- Worktrees：每个 Claude 会话独立 `git worktree`，互不干扰
- Boris 日常维护 3-5 个 worktrees，最长单次 Claude 运行 42 小时
- 产出效率：单会话 → 并行多会话 = 1x → 3-5x
- Headless 模式（`claude -p`）：打通 CI/CD，`--json-schema` 强制结构化输出，`--continue/--resume` 链式调用
- GitHub Actions：`@claude` 触发 PR 审查、Issue 修复

---

## 关键术语

- **Adaptive Thinking**：Opus 4.6 引入，根据任务复杂度自动决定推理深度
- **Effort Level**：三档（low/medium/high），Boris 全程用 high（B1）
- **Plan Mode**：只读模式，`Shift+Tab` 切换，Claude 不修改任何文件
- **SDD（Spec-Driven Development）**：见 concepts/spec-driven-development
- **Auto Memory**：`~/.claude/projects/<project>/memory/`，MEMORY.md 前 200 行自动注入
- **Worktree 隔离**：独立 git worktree，独立 memory 目录，互不影响
- **`/btw`**：侧边快速提问，有上下文但无工具，不进入会话历史，不阻塞主 Claude

---

## Boris Cherny Pro Tips 索引

| 编号 | 核心内容 |
|------|---------|
| B1 | Opus + High Effort for everything |
| B2 | 验证是 2-3x 质量的关键，给反馈循环，不给就是在猜 |
| B3 | Plan Mode 是基础而非可选，双会话审计计划 |
| B4 | 语音输入（fn×2）比打字快 3x，天然产出更详细描述 |
| B5 | 团队共维 CLAUDE.md，让 Claude 自己更新规则 |
| B6 | /permissions 预批准而非跳过权限 |
| B7 | PostToolUse Hook 自动格式化，规则变成确定性 |
| B8 | /commit-push-pr 每天几十次 |
| B9 | 挑战式提示："grill me"/"prove to me"/"elegant solution" |
| B10 | 5 个并行 Claude + 系统通知 + --teleport 拉回本地 |
| B11 | 3-5 worktrees，42h 最长运行，analysis worktree 只读日志 |
| B12 | 犯错后让 Claude 自己更新 CLAUDE.md，自我改进循环 |
| B13 | 每个人的 statusline 不一样，按个人工作习惯配置 |

---

## 相关实体

- entities/claude-code — 文章的主题工具
- entities/boris-cherny — Claude Code 之父，本文 Pro Tips 来源
- entities/anthropic — Claude Code 开发方

## 相关概念

- concepts/spec-driven-development — 规范驱动开发，大型功能的结构化工作流
- concepts/agent-skills — Claude Code 原生 Skills 系统（/simplify、/batch）
- concepts/memory-systems — CLAUDE.md 三层记忆体系
- concepts/context-engineering — 200K tokens 约束下的上下文管理实践
