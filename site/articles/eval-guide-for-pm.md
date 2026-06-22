---
title: "Eval 正在取代 PRD？产品经理的 Eval 入门到落地指南"
org: ""
date: 2026-06-09
source_url: ""
tags: ["Agent", "Eval/评测"]
summary: "综合 Anthropic《Demystifying Evals for AI Agents》、Meta PM Daniel McKinnon《Show, Don't Tell》、Braintrust《Evals Are the New PRD / Evals for PMs》、H"
summary_zh: ""
summary_en: "综合 Anthropic《Demystifying Evals for AI Agents》、Meta PM Daniel McKinnon《Show, Don't Tell》、Braintrust《Evals Are the New PRD / Evals for PMs》、H"
---



# Eval 正在取代 PRD？产品经理的 Eval 入门到落地指南

**来源**：[人人都是产品经理](https://www.woshipm.com/pd/6376492.html)，2026-04-14
**作者**：游瑶的产品笔记

综合 Anthropic《Demystifying Evals for AI Agents》、Meta PM Daniel McKinnon《Show, Don't Tell》、Braintrust《Evals Are the New PRD / Evals for PMs》、Hamel Husain（教过 700+ 工程师/PM 的 Eval 专家）、OpenAI 官方文档，以 PM 视角串联。

---

## 核心主张

OpenAI CPO Kevin Weil 和 Anthropic CPO Mike Krieger 说过几乎一模一样的话：

> **写 Eval 是 AI 时代 PM 最重要的能力。**

Meta PM Daniel McKinnon 的操作版本：

> "别给建模团队发 PRD 了，直接给他们一个 Eval。"

**原因**：Eval 的核心不是技术，而是**定义"什么算好"**——这是产品判断，PM 是最合适的人。工程师能搭基础设施，但"出什么题、怎么评分"应由 PM 来定。

**产品开发流程的演变（Braintrust）**：

```
传统流程：发现问题 → 写 PRD → 出设计 → 排开发 → 上线
AI 流程：  发现问题 → 写 Eval 定义"好"的标准 → 针对 Eval 做优化 → 上线
```

PRD 写完就落灰。Eval 可以每次代码提交自动跑一遍——活的、持续运行的质量标准。

---

## Eval 的三个组件

| 组件 | 别名 | 定义 | PM 的职责 |
|-----|------|------|-----------|
| **Dataset** | 考试题 | 测试 AI 的输入集合；覆盖：核心场景 + 边缘情况 + 已知失败点 | 决定"出哪些题"，20-50 题足够起步 |
| **Task** | 考试规则 | 执行环境：用哪个模型、什么 Prompt、参数设置、是否调外部工具 | 知道当前配置、能改 Prompt 措辞（最直接的质量变量） |
| **Scorer** | 阅卷标准 | 判断输出好坏；**每个维度单独打分** | 把"好用"拆成可量化的维度——这是 PM 在 Eval 里最核心的活 |

**核心原则**："好"不是整体，是多个维度拼成的。混一个总分会掩盖维度间的退步（语气好了但准确率跌了）。

---

## 三种 Scorer 选型

| Scorer | 优点 | 局限 | Anthropic 建议 |
|--------|------|------|---------------|
| **代码 Scorer** | 快、便宜、稳定 | 死板，创新答案可能误判 | **优先用**：凡是能用代码判的场景 |
| **LLM-as-Judge** | 灵活，处理模糊场景，可批量 | 结果有波动，需定期与人类校准 | 每个维度独立 LLM；给"不确定"出路；定期校准 |
| **人类 Grader** | 金标准 | 贵、慢、标注一致性陷阱 | 只用于验证和校准 LLM Scorer |

**Hamel Husain 补充**：用**通过/不通过**二分法，不用 1-5 分——1-5 分下标注员对"3 分"和"4 分"的理解差距太大。二分法逼着你把"什么算过"定义清楚。

**Inter-annotator Agreement 陷阱（McKinnon）**：

3 个标注员做二选一题，结果 2 个选 A、1 个选 B：

- 看起来：66% 一致
- 实际（pairwise 计算）：3 对中只有 1 对一致 → **33%**
- 随机猜的期望：50%

33% < 50%（随机），等于白做。结论：做人类评测前，必须把判断标准写到极其精确以确保标注员间高度一致。

---

## 从 0 到 1 建 Eval：7 步

**第 1 步：立即开始，别等"准备好"**
- Anthropic：越晚越难建；早期产品需求天然能转化为测试题，上线后逆向工程更难
- 起步：找最懂用户的人，30 分钟手标 20-50 个 AI 输出，好/不好——这是最小可行 Eval

**第 2 步：把手动在做的事变成 Eval**
- 每次发版前手动试的 case → 写下来 = 第一批 Dataset
- 产品已在跑：翻 bug 记录 + 客服工单，按影响面排序

**第 3 步：把"好用"拆成可打分的信号**

食谱自动生成示例（来自 Braintrust + McKinnon）：
- 信号 1：格式对不对（食材在前、步骤在后）→ LLM-as-Judge 对比示例
- 信号 2：视频里提到的食材食谱里都有 → 语音识别 + 字符串匹配（Code Scorer）
- 信号 3：步骤够不够简短 → 统计字数（Code）或 LLM 对比好坏写法

**第 4 步：写好题目，消除歧义**
- 好 Eval 题的标准：两位领域专家分别看完，独立给出同一个 pass/fail → 如果都不确定，是题出了问题
- 必备：给每道题写"参考解答（Reference Solution）"，标准答案过不了自己的 Scorer → Scorer 有 bug

**第 5 步：正反两面都测**
- 只测"应该做 X"→ 训出对所有问题都做 X 的 AI（Claude.ai 搜索 eval 案例：只测"应搜索"→ 过度搜索）
- 必须同时测"不应该做 X"

**第 6 步：评结果，不评过程**
- 别检查 AI 是否按特定步骤调用工具——Agent 经常找到你没预料到的正确路径
- 允许 Partial Credit：正确识别问题 + 验证身份但退款没走通，比直接崩溃好，Scorer 要体现差别

**第 7 步：跑完后，一定要读 Transcript**
- 不要只看分数，点开失败 case 看完整日志
- 很多时候：不是 AI 做错了，是 Scorer 拒绝了一个实际挺好的方案
- Anthropic 内部规矩：在有人读完 Transcript 之前，不把任何 Eval 分数当作事实

---

## Eval Flywheel（评测飞轮）

**Braintrust 提出**：Eval 真正的价值在于持续运转，而非一次性检查。

**飞轮的 4 个环节**：
```
观察 (Observe)    → 记录线上输入/输出/Transcript
分析 (Analyze)    → 找规律：什么场景出问题，哪类用户受影响最多
转化 (Evaluate)   → 失败模式 → 加进 Dataset（每次线上翻车 = 一道新题）
改进 (Improve)    → 团队针对新 Eval 优化 → 发布 → 回到 Observe
```

**用户其实一直在"出题"**：
- 差评 = 一道新题
- 用户编辑了 AI 输出 = 一份"标准答案"
- 用户换了三种说法问同一需求 = 一个未覆盖场景

**成熟度 4 档**：

| 档位 | 状态 | 描述 |
|------|------|------|
| **0 档** | 靠感觉 | 手动试几个、凭直觉判断、等用户投诉 |
| **1 档** | 有测试但不常考 | 有测试题和标准，大版本发布前跑一遍 |
| **2 档** | 自动化 | Eval 接进 CI/CD，质量不过关的版本自动拦截 |
| **3 档** | 飞轮转起来 | 线上失败案例自动变新 Eval 题，系统每周变好 |

大多数团队应以 **3 档** 为目标——竞争优势是积累型的。

---

## Capability Eval vs Regression Eval

| 类型 | 比喻 | 初始通过率 | 目的 |
|------|------|-----------|------|
| **Capability Eval** | 爬山 | 低（如 30%） | AI 还能多做好什么新的事 |
| **Regression Eval** | 守城 | 接近 100% | AI 还能不能做好它以前会做的事 |

**"毕业"机制**：Capability Eval 通过率稳定在高位后，转为 Regression Eval——从"能做到吗"变为"还能稳定做到吗"。

注意 **Eval Saturation（评测饱和）**：通过率到 100% 后对改进无指引价值，需要主动建更难的 Eval（Qodo 案例：one-shot eval 饱和 → 切换 agentic eval 才看清 Opus 4.5 的真实提升）。

---

## PM 的参考周节奏（Braintrust）

| 天 | 动作 |
|----|------|
| 周一 | 翻线上 Transcript，标记 20 条有问题的 AI 输出 |
| 周二 | 从中挑 5 个最典型的，加进 Dataset |
| 周三 | 用更新后的 Eval 跑当前方案 vs 候选改进方案 |
| 周四 | 看结果：哪个维度提升了，哪个退步了？数据决定发不发 |
| 周五 | 飞轮又多转了一圈 |

---

## 不同 AI 产品的 Eval 侧重

### 对话类（客服、销售、教练）
- 不只看"任务完成"，还看"过程体验"（对话本身是产品）
- 多维度：工单关掉了（Code）+ 对话轮数未超限（Code）+ 语气有同理心（LLM-as-Judge）+ 符合策略（LLM/Code）
- 通常用 AI 扮演用户测试，不能每次找真人
- 案例：Descript 从人工打分 → LLM-as-Judge + 定期人类校准；维护两套 Eval（质量基准 + Regression）
- 案例：Bolt.new 三个月内搭好：静态分析（代码质量）+ 浏览器 Agent（能不能用）+ LLM-as-Judge（指令遵循）

### 编码类
- 天然判断标准：能跑吗？测试过了吗？（Code Scorer 为主）
- 仅看"跑没跑通"不够，还需：代码质量/安全隐患/多余操作 → 补充 LLM-as-Judge 或静态分析

### 检索/研究类
- 最难做 Eval（"好"无唯一答案）
- Anthropic 推荐组合打分：Groundedness（有出处）+ Coverage（要点覆盖全）+ Source Quality（来源权威性）

---

## 常见的 6 个坑

| 坑 | 来源 | 说明 |
|----|------|------|
| 衡量"AI 聪不聪明" | McKinnon | 那是 MMLU/GPQA 的活，你的 Eval 只回答"这个场景做得好不好" |
| 让太多人设计 Eval | McKinnon | 人多出折中方案，McKinnon 很多 Eval 就是自己一人写的 |
| 拿来别人的 Eval 直接用 | McKinnon | 再有名的开源基准也可能有错，第一件事是手动抽几个样本看结果合不合理 |
| 只在发版时跑一次 | 通用 | 模型在变、数据在漂移，Eval 要持续跑 |
| 盯着分数不看业务 | Hamel | 通过率 100% 说明 Eval 太简单了；70% 可能更说明问题 |
| 用脏环境跑 Eval | Anthropic | Claude 曾在 Eval 里读上一次 trial 的 git 历史"作弊"；每次必须从干净环境开始 |

---

## Eval 的 4 个额外价值

1. **模型切换变快**：新模型出来，有 Eval 的团队几天内完成切换，无 Eval 的团队要花几周手动测试
2. **团队认知对齐**：两个工程师读同一个 spec 对边缘情况理解可能完全不同，Eval 直接给出答案
3. **产品和研发的共同语言**：Anthropic："Eval 是产品和研究团队之间最高带宽的沟通渠道"——比 PRD 更精确的优化指标
4. **更多人可以参与改进 AI**：PM/客户成功/销售可以贡献 Eval 用例，主动给他们工具和权限

---

## 参考来源索引

- Anthropic 官方：sources/demystifying-evals-for-ai-agents
- CORE-Bench 42%→95% 案例详见：concepts/agent-evaluation
- Claude.ai 搜索过度案例详见：concepts/agent-evaluation
- Qodo 饱和案例详见：concepts/agent-evaluation
