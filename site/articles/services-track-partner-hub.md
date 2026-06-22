---
title: "An update on recent Claude Code quality reports"
org: "Anthropic"
date: 2026-04-23
source_url: "https://www.anthropic.com/news/services-track-partner-hub"
tags: ["Agent", "Eval/评测", "Claude Code", "推理模型", "工具调用"]
summary: ""
summary_zh: ""
summary_en: ""
---



# An update on recent Claude Code quality reports
# Claude Code 质量退化复盘（2026-04）

## 核心观点

**三项独立变更叠加导致质量退化难以定位。** 3 月至 4 月间，Claude Code 经历了三次独立的工程变更，分别影响不同的流量切片和时间窗口，叠加后呈现为宽泛的随机性退化，加上内部实验干扰了复现路径，使根因定位耗时数周。所有问题已在 4 月 20 日（v2.1.116）修复完毕。

**推理努力等级默认值下调是错误取舍。** 将 Opus 4.6 的默认 reasoning effort 从 `high` 降至 `medium` 的出发点是减少长尾延迟，但代价是用户感知到的智能下降。最终在用户反馈压力下回滚，并将 Opus 4.7 的默认值进一步提升至 `xhigh`，确立了「**默认高智能、让用户主动降速**」的产品原则。

**Caching 优化 Bug 造成 thinking 历史持续丢失。** `clear_thinking_20251015` header 本应在会话空闲超一小时后仅清除一次旧 thinking，但 Bug 导致此后每轮都清除。Claude 在没有历史推理上下文的情况下继续执行，表现为失忆、重复操作和异常工具调用，且连续缓存 miss 加速消耗用量限额。该 Bug 通过了多轮人工与自动化代码审查，仅在边缘场景（空闲会话）触发，复现极困难。

**System Prompt 字数限制的影响超出预期。** 为压制 Opus 4.7 高冗余性而添加的一行限制（工具调用间 ≤25 词、最终回复 ≤100 词）在原始 eval 套件中未发现问题，但更广泛的 ablation 评估显示对 Opus 4.6 和 4.7 均造成约 **3% 的质量下滑**，说明原有 eval 覆盖面不足。

**事后改进聚焦 eval 覆盖、提示变更管控和工程透明度。** 核心措施：每次 System Prompt 变更须跑全量 per-model eval 和 ablation；对可能牺牲智能的变更增加浸泡期和渐进发布；扩大内部员工使用公开构建版本的比例；Code Review 工具引入更多代码库上下文（Opus 4.7 能找到 Opus 4.6 找不到的 Bug）；创建 @ClaudeDevs 账号提升工程透明度。

## 关键术语

- **reasoning effort（推理努力等级）**：控制模型在回复前投入多少 test-time compute 的参数，档位包括 medium / high / xhigh，通过 Messages API 的 effort 参数传入，也可用 `/effort` 命令切换。
- **extended thinking（扩展思考）**：模型生成回复前的显式推理过程，以 thinking blocks 形式保存在对话历史中，供后续轮次参照，是 Agent 上下文连续性的关键。
- **prompt caching（提示缓存）**：Anthropic API 层的 KV Cache 机制，将输入 token 写入缓存以加速和降低连续 API 调用成本；空闲超时后缓存被逐出，导致缓存 miss。
- **clear_thinking_20251015**：Anthropic API header，用于在特定条件下裁剪历史 thinking blocks，`keep:1` 表示仅保留最近一条 thinking。
- **ablation 评估**：逐行删除 System Prompt 以量化每行对模型表现影响的评估方法，是诊断提示回归的核心手段。
- **test-time compute curve**：描述模型思考时长与输出质量关系的曲线，effort 等级是在该曲线上选取的采样点。
- **soak period（浸泡期）**：变更上线后在有限流量上观察一段时间再全量推出的发布策略，用于捕捉低频边缘场景问题。
- **dogfooding**：让内部员工使用产品以发现问题的测试方式；本文指出内部测试版本与公开构建版本存在差异，导致某些 Bug 在内部未被发现。

## 相关概念

- concepts/harness-engineering — System Prompt 变更管控与 eval 流程；本文是反面教材+改进范本
- concepts/agent-evaluation — ablation 评估方法、per-model eval 套件、soak period 发布策略
- concepts/compaction — thinking history 管理；本文 caching Bug 是 compaction 失控的典型案例
- concepts/context-rot — thinking history 持续丢失导致 Agent 失忆，是上下文腐蚀的一种实例

## 相关实体

- entities/claude-code — 受影响的产品，三项变更均发生在其 harness 层，v2.1.116 全部修复
- entities/anthropic — 事故披露方，事后改进措施的制定者，创建 @ClaudeDevs 提升透明度
- entities/claude-cowork — 受 reasoning effort 变更和 caching Bug 两项影响
- entities/claude-agent-sdk — 受部分变更波及，API 推理层未受影响
