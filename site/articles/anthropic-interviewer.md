---
title: "Introducing Anthropic Interviewer: What 1,250 professionals told us about working with AI"
org: "Anthropic"
date: 2025-12-04
source_url: "https://www.anthropic.com/news/anthropic-interviewer"
tags: ["Eval/评测", "安全/对齐", "经济影响"]
summary: "86% 的受访专业人士表示 AI 节省了时间，65% 对 AI 在工作中的角色感到满意。然而，69% 提到因使用 AI 而受到同事的隐性否定——\"我不告诉任何人我的流程，因为我知道很多人对 AI 的感受\"（事实核查员）。社会污名与实际生产力收益形成张力，促成了「隐性 AI 使"
summary_zh: "86% 的受访专业人士表示 AI 节省了时间，65% 对 AI 在工作中的角色感到满意。然而，69% 提到因使用 AI 而受到同事的隐性否定——\"我不告诉任何人我的流程，因为我知道很多人对 AI 的感受\"（事实核查员）。社会污名与实际生产力收益形成张力，促成了「隐性 AI 使"
summary_en: ""
---



# Introducing Anthropic Interviewer: What 1,250 professionals told us about working with AI

## 核心观点

**1. AI 生产力提升显著，但社会污名（Social Stigma）普遍压制公开采用**

86% 的受访专业人士表示 AI 节省了时间，65% 对 AI 在工作中的角色感到满意。然而，69% 提到因使用 AI 而受到同事的隐性否定——"我不告诉任何人我的流程，因为我知道很多人对 AI 的感受"（事实核查员）。社会污名与实际生产力收益形成张力，促成了「隐性 AI 使用」行为模式。

**2. 增强 vs 自动化：自我认知与实际行为存在系统性偏差**

受访者自我报告：65% 视 AI 为增强协作工具，35% 视为自动化执行工具。但 Anthropic 的 Clio 工具对实际对话的分析显示几乎均分（47% 增强 / 49% 自动化）。这一对比揭示人们倾向于将自己定义为 AI 的「引导者」，即便实际使用中已大量委托给 AI。

**3. 创意工作者：效率提升与身份焦虑并存**

97% 表示 AI 节省时间，68% 表示提高了作品质量（从每天 2000 字到 5000 字）。但全部 125 名创意受访者都提到维持对创意输出控制的欲望——其中一位艺术家坦承"AI 驱动了相当多的概念，我只是尝试引导它……60% AI，40% 我的想法"。经济焦虑层面：配音演员细分市场已受 AI 实质冲击，作曲家担心平台用 AI 无限生成廉价音乐。

**4. 科学家：信任门槛最高，核心研究任务不信任 AI**

79% 的科学家访谈中，信任与可靠性是首要障碍；27% 提到技术局限。当前实际使用局限于：文献综述、代码调试、论文写作。核心研究任务（假设生成、实验设计）几乎无人委托给 AI。然而 91% 表达了希望 AI 提供更多研究协助的愿望，核心诉求是能生成新科学假设的 AI 合作伙伴。

**5. Anthropic Interviewer 是方法论创新，也是 AI 社会影响研究的基础设施**

三阶段自动访谈流程（规划 → 实时自适应访谈 → AI 辅助分析），将以往需要巨额成本的千人定性研究变为可行。所有访谈数据已公开发布（HuggingFace）。该工具定位为 Collective Constitutional AI 工作的延续——将公众声音系统化引入 Claude 的训练与政策方向。

## 关键术语

- **Anthropic Interviewer**：Anthropic 开发的 AI 驱动访谈工具，由 Claude 支持，支持千人量级全自动定性访谈
- **增强（Augmentation）**：AI 与用户协作完成任务的模式，用户保留主导决策权
- **自动化（Automation）**：AI 直接完成任务的模式，人类主要扮演监督角色
- **Social Stigma（社会污名）**：在工作场所公开使用 AI 工具所面临的同事否定态度，驱动隐性 AI 采用
- **Clio**：Anthropic 的隐私保护对话分析工具，用于分析 Claude.ai 对话模式（非访谈工具，与 Interviewer 互补）
- **Collective Constitutional AI**：Anthropic 收集公众意见塑造 Claude 行为准则的研究方法论
- **pass@k / 隐性委托**：受访者声称「只是让 AI 提供建议」，但实际创意控制权已大幅转移给 AI（创意工作者群体中的普遍现象）
- **Tacit Knowledge（隐性知识）**：科学家保留人工判断的核心理由——如细菌颜色判断等无法数字化的经验感知

## 相关概念

- concepts/workflow-patterns — 增强 vs 自动化的概念框架，本文数据可丰富实证部分
- concepts/agent-evaluation — AI 访谈本身是一种新型评估/研究工具
- concepts/agentic-systems — Anthropic Interviewer 作为三阶段 agentic pipeline 的典型案例

## 相关实体

- entities/anthropic — 本文作者机构，Anthropic Interviewer 的开发者
- entities/claude-opus-4-6 — Anthropic Interviewer 底层模型（文章提及由 Claude 驱动）
