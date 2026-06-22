---
title: "Making Claude a Chemist: NMR 预测与结构解析评测"
org: "Anthropic"
date: 2026-06-05
source_url: "https://www.anthropic.com/research/making-claude-a-chemist"
tags: ["Eval/评测", "多模态"]
summary: "在 20 个化合物（ChemRxiv 训练截止后预印本）的正向 NMR 预测中，Opus 4.7 ¹H 误差 ±0.079 ppm（容许窗口 ±0.20 ppm），¹³C 误差 ±1.37 ppm（与 MestReNova ±1.48 ppm 持平）。峰型预测和子峰间距命中率 ~"
summary_zh: "在 20 个化合物（ChemRxiv 训练截止后预印本）的正向 NMR 预测中，Opus 4.7 ¹H 误差 ±0.079 ppm（容许窗口 ±0.20 ppm），¹³C 误差 ±1.37 ppm（与 MestReNova ±1.48 ppm 持平）。峰型预测和子峰间距命中率 ~"
summary_en: ""
---



# Making Claude a Chemist: NMR 预测与结构解析评测

## 核心观点

**1. 正向预测：Claude Opus 4.7 达到专业软件水平**

在 20 个化合物（ChemRxiv 训练截止后预印本）的正向 NMR 预测中，Opus 4.7 ¹H 误差 ±0.079 ppm（容许窗口 ±0.20 ppm），¹³C 误差 ±1.37 ppm（与 MestReNova ±1.48 ppm 持平）。峰型预测和子峰间距命中率 ~80%，远超 ChemDraw 和 MestReNova 的 26-35%。

**2. 逆向预测（结构解析）：填补专业软件空白**

15 个结构解析任务中，8 个简单化合物（单环/双片段）从谱图+分子式出发全部 3 次命中。7 个复杂化合物（稠环/螺环）在提供起始原料 SMILES 提示后，4/7 三次全对，3/7 两次命中。现有专业软件需要二维 NMR、专业培训和付费工具才能完成此类任务；Claude 从相同的 HRMS + 一维峰表出发即可运行。

**3. 化学数据困境与多模态突破口**

化学 AI 多年来受困于：零结果数据稀缺、格式不统一、期刊付费墙。前沿多模态 LLM 的关键突破是可直接读取期刊图表/手绘结构/实验支持信息，无需预策划数据库。这改变了"哪些问题尽管存在数据困境仍可解决"的边界。

**4. 评测局限性明确声明**

- 样本量小（正向 20 化合物，逆向 15 化合物），应视为指示性而非精确结论
- 复杂逆向目标在无提示条件下可能无法收敛到结构
- 未覆盖：2D NMR（COSY/HSQC/HMBC）、立体化学、天然产物复杂结构
- 溶剂仅覆盖 DMSO-d₆、CDCl₃、D₂O

**5. 化学助手路线图**

Anthropic 明确四个改进方向：① 化学结构读写/格式互换；② 反应与合成推理（逆合成规划）；③ 反应机理；④ 化学文献理解。逆合成规划目前仍在设计阶段，光谱分析最为成熟。

## 关键术语

- **NMR spectroscopy（核磁共振光谱）**：用射频与磁场探测分子中氢/碳原子化学环境的光谱技术，输出峰位（化学位移，ppm）和峰型。
- **正向预测（Forward Prediction）**：已知分子结构 → 预测 NMR 谱图；SMILES 字符串输入，峰表输出。
- **逆向预测/结构解析（Inverse Prediction / Structure Elucidation）**：已知谱图 + 分子式 → 推断分子结构；化学家日常最核心的解析任务。
- **SMILES**：化学家用于在软件中输入分子结构的线性文本表示法（Simplified Molecular Input Line Entry System）。
- **MAE / RMSE**：平均绝对误差 / 均方根误差，NMR 预测精度的主要量化指标。
- **化学位移（Chemical Shift, ppm）**：NMR 峰在频率轴上的位置，对应原子周围电子环境。
- **逆合成规划（Retrosynthesis）**：从目标分子逆向推导合成路径，AI 工具存在多年但实际采用率低。
- **ChemRxiv**：化学领域预印本服务器，本文用作训练截止后的无偏评测数据来源。
- **HRMS（高分辨质谱）**：给出精确分子式，是逆向预测任务的标准输入之一。

## 相关概念

- concepts/eval-awareness — 本文采用训练截止后取样防污染，与 Eval 感知问题正面对应
- concepts/agent-evaluation — 多次重复运行取平均的评测方法论（三次独立运行 + min-max range）
- concepts/tool-design-for-agents — 化学工具作为 Claude 能力扩展的接口设计方向

## 相关实体

- entities/anthropic — 发布者，扩展 AI for Science 项目
- entities/claude-opus-4-6 — 参照对象（Opus 4.6 表现居中，在氨基哒嗪 NH 峰预测中多次偏差数个 ppm）
