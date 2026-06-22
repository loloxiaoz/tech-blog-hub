---
title: "Next-generation Constitutional Classifiers: 更高效的通用越狱防护"
org: "Anthropic"
date: 2026-01-09
source_url: "https://www.anthropic.com/research/constitutional-classifiers"
tags: ["可解释性", "安全/对齐"]
summary: "原文：https://www.anthropic.com/research/constitutional-classifiers-2"
summary_zh: ""
summary_en: "原文：https://www.anthropic.com/research/constitutional-classifiers-2"
---



# Next-generation Constitutional Classifiers: 更高效的通用越狱防护

原文：https://www.anthropic.com/research/constitutional-classifiers-2
论文：https://arxiv.org/abs/2601.04603

## 核心观点

**1. CC++ 在效率与鲁棒性上双重突破**

第一代 Constitutional Classifiers 将越狱成功率从86%降至4.4%，但带来23.7%计算开销和0.38%误拒率。CC++ 将计算开销压缩至约1%，误拒率从0.38%降至0.05%，同时检测率进一步提升（0.005高危漏洞/千次查询）。

**2. 两阶段级联架构：把误拒变成升级**

核心架构：轻量级线性探针（复用模型内部激活）筛全流量 → 疑似有害交换升级至重量级交换分类器。第一阶段保持较高假阳性率而不直接拒绝用户，相当于"交给上级判断"而非直接说不。这一设计将用户体验与安全鲁棒性的权衡解耦。

**3. 交换分类器替代单边分类器**

原系统分别处理输入和输出；新系统用「交换分类器」同时看输入+输出上下文。这使得输出混淆攻击（如用"食用香料"指代化学试剂）和重构攻击（跨代码片段隐藏有害内容）无所遁形。孤立看输出无法识别，结合输入语境立刻暴露。红队测试中，交换分类器将越狱成功率减半，代价是50%计算开销（随后由级联架构摊薄）。

**4. 内部激活探针：机理可解释性的生产应用**

Claude 在处理有害请求时，即使尚未生成回复，内部激活模式已显示「这似乎有害」的信号。通过线性探针直接读取这些内部状态：(a) 计算几乎免费（复用已有前向传播计算）；(b) 攻击者难以操控（操控最终输出比操控内部表示容易得多）；(c) 与外部分类器形成互补覆盖。这是 Anthropic 可解释性研究从理论走向生产部署的直接例证。

**5. 两类新型攻击的发现与应对**

重构攻击：将有害查询拆散嵌入代码函数中，模型被指示重新组合并响应隐藏信息。输出混淆攻击：指示模型用隐语或谜语/隐喻输出危险内容，使单独看输出的分类器失效。两类攻击的副作用是会严重降低模型能力（GPQA Diamond 从74%降至32%），但攻击者可能开发出能保留更多模型能力的变体，这是持续威胁。

## 关键术语

- **Constitutional Classifiers（宪法分类器）**：用自然语言规则（"宪法"）生成合成训练数据，训练出的内容安全分类器；例：Claude 可帮助大学化学作业，但不能协助合成管制化学品
- **Universal Jailbreak（通用越狱）**：可跨多种查询复用的一致性攻击策略，危害最大，是 Anthropic 重点防御目标
- **Exchange Classifier（交换分类器）**：同时处理输入+输出对的分类器，比单边输出分类器更能识别上下文依赖的伪装攻击
- **Cascade Architecture（级联架构）**：两阶段分类系统，轻量级第一阶段做粗筛，仅将疑似有害内容升级到重量级第二阶段
- **Internal Activation Probe（内部激活探针）**：读取模型神经网络中间层状态的线性分类器，复用模型前向传播已产生的中间计算，成本极低
- **Reconstruction Attack（重构攻击）**：将有害信息分散隐藏于代码或多个片段中，依赖模型将碎片重新组合
- **Output Obfuscation Attack（输出混淆攻击）**：指示模型用替代词汇/隐喻输出有害内容，绕过只看输出的分类器
- **GPQA Diamond**：衡量生物/化学/物理PhD级概念的基准，本文用于量化越狱攻击对模型能力的损耗

## 相关概念

- concepts/constitutional-classifiers — 宪法分类器：合成数据驱动的安全分类器，CC++ 两阶段级联架构
- concepts/jailbreak-attacks — 越狱攻击类型：通用越狱、重构攻击、输出混淆攻击
- concepts/mechanistic-interpretability — 机理可解释性：内部激活探针是可解释性研究的生产应用案例
- concepts/agent-containment — Agent 爆炸半径控制：分类器是 Anthropic 多层防御体系的一部分
- concepts/prompt-injection — 提示注入：与越狱攻击同属 AI 安全威胁，防御逻辑互补
- concepts/eval-awareness — Eval 感知：模型识别测试情境，与红队测试的有效性问题相关

## 相关实体

- entities/anthropic — 本文作者，CC++ 的研发与部署方，论文 arXiv:2601.04603
