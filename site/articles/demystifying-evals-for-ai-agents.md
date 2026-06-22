---
title: "Demystifying Evals for AI Agents（揭秘 AI Agent 评测体系）"
org: "Anthropic"
date: 2026-05
source_url: "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"
tags: ["Agent", "Eval/评测", "Claude Code", "Harness工程", "工具调用"]
summary: "Evals 的价值复利：新模型发布时，有 eval 的团队几天内完成迁移评估，无 eval 的团队需要数周。"
summary_zh: "Evals 的价值复利：新模型发布时，有 eval 的团队几天内完成迁移评估，无 eval 的团队需要数周。"
summary_en: ""
---



# Demystifying Evals for AI Agents（揭秘 AI Agent 评测体系）

## 基本信息

- **来源**：Anthropic 官方工程博客（与 Building Effective AI Agents 系列配套）
- **核心主张**：好的评测让团队更自信地发布 Agent；没有评测，团队陷入被动修复循环，价值随 Agent 生命周期复利积累

## 核心论点

> "Teams without evals get bogged down in reactive loops—fixing one failure, creating another, unable to distinguish real regressions from noise."

Evals 的价值复利：新模型发布时，有 eval 的团队几天内完成迁移评估，无 eval 的团队需要数周。

## 关键概念定义

| 术语 | 定义 |
|------|------|
| **Task**（任务） | 单个测试，有明确输入和成功标准 |
| **Trial**（试验） | 对一个 Task 的单次尝试，因模型输出可变需多次运行 |
| **Grader**（评分器） | 评分某方面性能的逻辑，一个 Task 可有多个 Grader，每个含多个 assertion |
| **Transcript**（轨迹） | 完整试验记录：输出、工具调用、推理、中间结果（= Anthropic API 完整 messages 数组） |
| **Outcome**（结果） | 试验结束时环境的**实际状态**（≠ Agent 说的话：数据库里是否真的有预订记录） |
| **Evaluation harness** | 端到端运行 eval 的基础设施：提供指令和工具、并发运行任务、记录步骤、评分、聚合结果 |
| **Agent harness (scaffold)** | 使模型能作为 Agent 行动的系统（Claude Code 是灵活的 agent harness；Agent SDK 提供核心原语）。评测的是 harness + model 的组合，不只是模型 |
| **Evaluation suite** | 为测量特定能力/行为设计的任务集合；一个 suite 通常围绕一个宏观目标 |

> **Eval harness ≠ Agent harness**：前者是跑测试的基础设施；后者是让模型成为 Agent 的系统。两者在评测时共同工作。

## 三类 Grader

| 类型 | 优点 | 缺点 | 适用 |
|------|------|------|------|
| **代码 Grader** | 快、便宜、客观、可复现、易调试 | 对有效变体脆弱、缺乏细微差别 | 确定性判断：测试通过、工具调用验证、状态检查 |
| **模型 Grader** | 灵活、可扩展、捕捉细微差别、处理开放任务 | 非确定性、更贵、需人工校准 | 开放性任务、主观质量评估、多维 rubric |
| **人类 Grader** | 黄金标准、专家判断 | 昂贵、缓慢、难规模化 | 校准模型 Grader、高风险主观评估 |

评分方式：加权（各 grader 分数达到阈值）/ 二进制（全部 grader 通过）/ 混合。

## Capability vs Regression Evals

- **Capability eval**：从低通过率开始，测试 Agent 还做不好的事，是"要爬的山"
- **Regression eval**：近 100% 通过率，防止已有能力退步，是"不能倒塌的底线"
- 两者关系：高通过率的 capability eval "毕业"后成为 regression suite

## 各类 Agent 的评测要点

### 代码 Agent

天然确定性评分：代码是否运行？测试是否通过？也需评 Transcript（代码质量规则、工具调用行为）。

参考基准：SWE-bench Verified（从 40% → >80%，一年内）、Terminal-Bench（端到端技术任务，如从源码编译 Linux 内核）

**YAML 示例（修复认证绕过漏洞）**：

```yaml
task:
  id: "fix-auth-bypass_1"
  desc: "Fix authentication bypass when password field is empty and ..."
  graders:
    - type: deterministic_tests
      required: [test_empty_pw_rejected.py, test_null_pw_rejected.py]
    - type: llm_rubric
      rubric: prompts/code_quality.md
    - type: static_analysis
      commands: [ruff, mypy, bandit]
    - type: state_check
      expect:
        security_logs: {event_type: "auth_blocked"}
    - type: tool_calls
      required:
        - {tool: read_file, params: {path: "src/auth/*"}}
        - {tool: edit_file}
        - {tool: run_tests}
  tracked_metrics:
    - type: transcript
      metrics: [n_turns, n_toolcalls, n_total_tokens]
    - type: latency
      metrics: [time_to_first_token, output_tokens_per_sec, time_to_last_token]
```

> 注：此示例展示全部可用 grader 类型。实践中编码 eval 通常只用单元测试（正确性）+ LLM rubric（质量），其余按需添加。

### 对话 Agent

多维度成功标准：状态检查（票单已解决）+ Transcript 约束（<10 轮）+ LLM rubric（语气恰当）。需要第二个 LLM 模拟用户。

参考基准：τ-Bench、τ2-Bench（零售支持 + 机票预订，Agent 应对用户角色扮演）

**YAML 示例（处理愤怒客户退款）**：

```yaml
graders:
  - type: llm_rubric
    rubric: prompts/support_quality.md
    assertions:
      - "Agent showed empathy for customer's frustration"
      - "Resolution was clearly explained"
      - "Agent's response grounded in fetch_policy tool results"
  - type: state_check
    expect:
      tickets: {status: resolved}
      refunds: {status: processed}
  - type: tool_calls
    required:
      - {tool: verify_identity}
      - {tool: process_refund, params: {amount: "<=100"}}
      - {tool: send_confirmation}
  - type: transcript
    max_turns: 10
```

### 研究 Agent

质量只能相对任务判断；专家可能意见不一；参考内容持续变化；长输出有更多出错空间。

组合 Grader：Groundedness check（声明是否有来源支撑）+ Coverage check（关键事实是否覆盖）+ Source quality check（来源是否权威）+ LLM rubric（一致性和完整性）。

参考基准：BrowseComp（全网大海捞针，容易验证但难解决）

### Computer Use Agent

必须在真实/沙盒环境运行，验证实际 Outcome 而非 Agent 声称结果。注意 **DOM 交互 vs 截图交互的权衡**：DOM 快但耗 token；截图慢但 token 效率高（如让 Claude 在 Amazon 找商品，用截图更高效）。Claude for Chrome 开发了专项 eval 检测 Agent 是否为每个上下文选了正确工具。

参考基准：WebArena（浏览器任务）、OSWorld（全 OS 控制）

## 非确定性指标：pass@k vs pass^k

| 指标 | 定义 | 随 k 增大 | 适用 |
|------|------|---------|------|
| **pass@k** | k 次尝试中至少 1 次成功的概率 | 升高（趋向 100%） | 工具类（一次成功即可） |
| **pass^k** | k 次全部成功的概率 | 降低（趋向 0%） | 面向用户（每次都要可靠）；75% 成功率 × k=3 → 42% |

k=1 时两者相同；k=10 时讲述完全相反的故事。

## 从零构建评测的 8 步路线图

**Step 0：早开始**
20-50 个任务足够。早期 Agent 每次改动影响大，小样本即可检测。越晚越难——需要从生产系统逆向工程成功标准。

**Step 1：从已手动测试的内容开始**
从 bug tracker 和用户反馈中提取失败案例，转为测试用例。已在生产的团队按用户影响排优先级。

**Step 2：写清晰无歧义任务 + 参考解答**
好任务 = 两位领域专家独立得出相同 pass/fail 结论。每个 grader 检查的内容都应能从任务描述推导出来。

**重要**：为每个任务创建参考解答（a known working output that passes all graders），以证明任务可解且 grader 配置正确。0% pass@100 通常意味着 eval 坏了，而非 Agent 差——这是检查任务规范和 grader 的信号。

**Step 3：构建均衡问题集**
不只测"行为应触发"的情况，也测"行为不应触发"的情况。单边 eval 产生单边优化。

**案例**：Claude.ai 网页搜索 eval 面临"过度搜索 vs 不够搜索"的均衡难题。团队同时构建"应该搜索"（查天气）和"不应搜索"（谁创立了苹果？）两类用例，经过多轮迭代才找到平衡。

**Step 4：构建稳健的 eval harness + 环境隔离**
Agent 在 eval 中要与生产中运行方式基本一致。每次试验从干净环境开始，避免跨 trial 共享状态。

**反例**：内部 eval 中观察到 Claude 能查看之前 trial 的 git 历史记录，从而获得不公平优势。若多次独立 trial 因同一环境限制（如 CPU 内存）失败，结果不独立，eval 失去可靠性。

**Step 5：慎重设计 Grader**
- 优先确定性 grader，必要时用 LLM grader，人工 grader 用于额外验证
- **评结果不评路径**：检查特定工具调用顺序过于死板；Agent 经常找到 eval 设计者没预料到的有效方法
- 多组件任务设计**部分积分**（完成一半比直接失败有意义）
- 给 LLM grader 一条"出路"（如返回 "Unknown" 而非强行判断）
- 针对每个维度独立评分，而非用一个 LLM 评所有维度
- **反 bypass 设计**：通过 eval 应该真正需要解决问题

**Step 6：读 Transcript**
失败应该"看起来公平"——清楚知道 Agent 错在哪里。这是验证 eval 是否测了真正重要的事的核心方式。Anthropic 专门投资了 eval transcript 查看工具，定期阅读是团队习惯。

**Step 7：监控 Capability eval 饱和**
eval 接近 100% 时只剩回归价值，无改进信号。SWE-bench Verified 已从年初 30% 接近 80% 饱和。

**案例**：Qodo（代码审查初创）初始对 Opus 4.5 不感冒——因为他们用 one-shot 编码 eval，看不出它在更长、更复杂任务上的提升。开发专门的 agentic eval 框架后，才清晰看到进步。

**Step 8：长期维护评测套件**
专门 evals 团队负责核心基础设施所有权；领域专家和产品团队贡献具体任务并自己运行 eval。

**Eval-driven development**：先写 eval 定义计划中的能力（从低通过率开始），再迭代实现直到通过。产品经理、客户成功经理、销售人员可以通过 Claude Code 贡献 eval 任务 PR——积极赋能他们这样做。

## Eval 质量问题：真实案例

### CORE-Bench：42% → 95%

Opus 4.5 初始得 42%，Anthropic 研究员深挖后发现多个问题：
- 刚性评分：期望 "96.124991…"，但答案 "96.12" 被判失败
- 任务规范歧义
- 随机任务无法精确复现

修复评测 bug + 使用限制更少的 scaffold 后，分数跳至 95%。

### METR 时间线基准测试

METR 发现基准中多个配置错误任务：要求 Agent 优化到某个分数阈值，但评分要求**超过**该阈值。遵循指令的模型（如 Claude）被惩罚，忽略指令的模型反而得高分。

> **教训**：总分数不能直接信任，需有人深入挖掘 eval 细节并阅读 transcript。

## Eval 与其他方法的分层（Swiss Cheese 模型）

| 方法 | 最适合阶段 | 优点 | 缺点 |
|------|----------|------|------|
| 自动化 eval | 发布前、CI/CD、每次 commit | 快速迭代、可复现、无用户影响 | 需前期投入；可能与真实使用模式偏差 |
| 生产监控 | 上线后 | 真实用户行为、发现合成 eval 遗漏的问题 | 问题先触达用户；缺乏评分基准 |
| A/B 测试 | 重要变更、有足够流量 | 测量真实用户结果 | 慢（数天到数周）；只测部署了的变更 |
| 用户反馈 | 持续 | 发现意外问题、真实例子 | 稀疏、自我选择；偏向严重问题 |
| 手动 transcript 审查 | 持续 | 建立直觉、发现细微质量问题 | 费时；覆盖不一致 |
| 系统性人工评估 | 按需 | 黄金标准判断 | 贵、慢；复杂领域需专家 |

没有单一方法能捕获所有问题，多层组合漏过一层的被下一层捕获。

## Eval 框架附录

| 框架 | 特点 | 适合场景 |
|------|------|---------|
| **Harbor** | 容器化环境运行 Agent、云规模并发试验、标准化任务/grader 格式；Terminal-Bench 2.0 通过其 registry 分发 | 需要隔离环境 + 规模化运行的 Agent eval |
| **Braintrust** | 离线 eval + 生产可观测性 + 实验追踪；内置 `autoevals` 库（Factuality、Relevance 等） | 既要开发迭代又要监控生产质量的团队 |
| **LangSmith** | tracing + 离线/在线 eval + LangChain 生态集成 | LangChain 用户 |
| **Langfuse** | LangSmith 的自托管开源替代，满足数据驻留要求 | 有数据主权需求的团队 |
| **Arize Phoenix** | 开源 LLM tracing/调试/离线或在线 eval；AX 是其企业 SaaS 版 | 需要深度调试和可观测性的团队 |

> 框架的价值取决于跑进去的 eval 任务质量。选一个适合工作流的框架，把精力放在迭代高质量测试用例和 grader 上。

## 相关概念

- concepts/agent-evaluation — Agent 评测完整体系（综合方法论）
- concepts/agentic-systems — 所评测的系统类型
- concepts/rag-evaluation — RAG 评测，与 Agent 评测有共通之处

## 相关来源

- sources/building-effective-ai-agents — 同系列前置文章
