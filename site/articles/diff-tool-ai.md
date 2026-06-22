---
title: "A \"diff\" tool for AI: 为新模型寻找行为差异（跨架构模型 Diffing）"
org: "Anthropic"
date: 2026-03-13
source_url: "https://www.anthropic.com/engineering/diff-tool-ai"
tags: ["Eval/评测", "安全/对齐", "推理模型", "代码模型", "开源模型"]
summary: "原文：https://www.anthropic.com/research/diff-tool"
summary_zh: ""
summary_en: "原文：https://www.anthropic.com/research/diff-tool"
---



# A "diff" tool for AI: 为新模型寻找行为差异（跨架构模型 Diffing）

原文：https://www.anthropic.com/research/diff-tool
论文：https://arxiv.org/abs/2602.11729

## 核心观点

**1. 传统安全评测是反应式的，存在"未知的未知"盲区**

现有基准测试（benchmark）只能测试人类已知并会测量的风险。这意味着模型中新兴的、未被预想到的行为——即"未知的未知"——会被漏检。传统评测相当于拿到百万行代码从头找安全漏洞，效率极低。

**2. 模型 Diffing：把注意力集中在"变化的部分"**

软件工程的 diff 工具让开发者只审查真正改变的 50 行代码而非百万行全量审计。模型 diffing 将这一思路移植到神经网络：自动定位两个模型之间行为差异最显著的特征，将审计资源集中到真正新增或变化的内容。

- **base-vs-finetune diffing**：适用于新模型是旧模型微调版的场景，相对成熟
- **跨架构 diffing**：适用于来自不同开发者、不同"内部语言"的模型对比，难度更高

**3. Dedicated Feature Crosscoder（DFC）解决跨架构 diffing 的核心难题**

标准 crosscoder 倾向于为所有特征强行找到跨模型的"翻译"，当一个模型有某独有特征时，它会错误地与另一模型中相近的特征匹配，导致安全审计者误以为"这不是新东西"而漏过。

DFC 的三段式架构：
1. **共享字典**：映射两模型共有的概念（等价词汇）
2. **模型 A 专有区**：专门容纳 A 独有的特征
3. **模型 B 专有区**：专门容纳 B 独有的特征

通过保留专有区，DFC 避免了强制匹配的陷阱，确保独有特征被正确标记为"需要重点审查的新内容"。

**4. Steering 验证因果关系：三个模型专有特征的发现**

验证方法：人工抑制或放大 DFC 识别的特征，观察模型输出变化（即"steering"），从而确立特征与行为之间的因果关系。

| 模型 | 特征名称 | 行为表现 | Steering 效果 |
|------|----------|----------|--------------|
| Qwen3-8B（阿里云） | CCP 对齐（中共对齐） | 拒绝讨论天安门等敏感话题，生成亲政府内容 | 抑制→愿意讨论；放大→亲政府声明增强 |
| DeepSeek-R1-0528-Qwen3-8B | CCP 对齐（同上） | 同上，独立复现 5/5 次 | 同上 |
| Llama-3.1-8B-Instruct（Meta） | 美国例外主义 | 生成断言美国优越性的内容 | 放大→断言增强；抑制→无明显变化 |
| GPT-OSS-20B（OpenAI） | 版权拒绝机制 | 拒绝生成版权内容 | 抑制→拒绝消失；放大→过度拒绝（如连 PBJ 食谱都拒绝） |

**5. 高召回筛查工具 + 监控模型更新的潜力**

DFC 是高召回率（high-recall）筛查工具，会标记数千个候选特征，其中只有少部分对应真正风险。价值在于作为审计入口，而非最终判断。

潜在用途：若将 DFC 用于对比 GPT-4o 前后版本，可能在 2025 年 4 月谄媚（sycophancy）行为回归发布前自动将其标记为异常变化，从而在发布前介入纠正。

## 关键术语

| 术语 | 定义 |
|------|------|
| **模型 Diffing（Model Diffing）** | 自动比较两个 AI 模型，定位行为差异最显著的内部特征，类比代码 diff 工具 |
| **跨架构 Diffing** | 对比来自不同开发者、不同内部表示空间的模型，比 base-vs-finetune diffing 难度更高 |
| **特征（Feature）** | 可解释性研究中对神经网络内部激活进行稀疏分解后得到的基本语义单元 |
| **Crosscoder** | 跨模型特征对应学习器，将两个模型的特征空间映射到共同表示 |
| **DFC（Dedicated Feature Crosscoder）** | 带专有区的改进型 crosscoder，通过三段式结构（共享+A专有+B专有）避免强制匹配 |
| **Steering（特征操控）** | 在模型推理时人工抑制或放大特定特征，验证特征-行为因果关系的实验方法 |
| **CCP 对齐特征** | 在 Qwen3 和 DeepSeek 模型中发现的控制亲政府内容生成的内部特征 |
| **未知的未知（Unknown Unknowns）** | 评测设计者未预想到、无法被现有基准覆盖的新兴风险行为 |
| **高召回筛查工具** | 宁可多报也不漏报的安全工具，用于初步筛选候选风险，后续由人工深入审查 |

## 相关概念

- concepts/model-diffing — 本文提出的跨架构模型差异比较技术（待建页）
- concepts/mechanistic-interpretability — 机理可解释性，理解神经网络内部特征的研究方向（待建页）
- concepts/feature-steering — 特征操控，验证因果关系的实验手段（待建页）
- concepts/agent-evaluation — 模型 diffing 是传统评测的补充，专注"未知的未知"
- concepts/eval-awareness — 评测感知，与本文"高召回筛查"理念互补

## 相关实体

- entities/anthropic — 研究发布方，通过 Anthropic Fellows 项目推进
- entities/deepseek — DeepSeek-R1-0528-Qwen3-8B 被发现含 CCP 对齐特征（待建页）
