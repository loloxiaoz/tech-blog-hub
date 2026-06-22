---
title: "Measuring AI Agent Autonomy in Practice（实测AI Agent自主性）"
org: "Anthropic"
date: 2026-02-18
source_url: "https://www.anthropic.com/engineering/measuring-agent-autonomy"
tags: ["Agent", "Eval/评测", "Claude Code"]
summary: "Claude Code 最长任务时长（99.9百分位）在2025年10月至2026年1月间从不足25分钟增长至超过45分钟，三个月内接近翻倍。但METR测评显示Claude Opus 4.5可处理需人类5小时才能完成的任务（50%成功率）。两组数据揭示了一个\"部署过滞后\"（d"
summary_zh: "Claude Code 最长任务时长（99.9百分位）在2025年10月至2026年1月间从不足25分钟增长至超过45分钟，三个月内接近翻倍。但METR测评显示Claude Opus 4.5可处理需人类5小时才能完成的任务（50%成功率）。两组数据揭示了一个\"部署过滞后\"（d"
summary_en: ""
---



# Measuring AI Agent Autonomy in Practice（实测AI Agent自主性）

## 核心观点

**1. 部署自主度存在系统性滞后**

Claude Code 最长任务时长（99.9百分位）在2025年10月至2026年1月间从不足25分钟增长至超过45分钟，三个月内接近翻倍。但METR测评显示Claude Opus 4.5可处理需人类5小时才能完成的任务（50%成功率）。两组数据揭示了一个"部署过滞后"（deployment overhang）：模型可处理的自主度远超用户实际授予的自主度，差距主要来自信任建立时间，而非模型能力本身。

值得注意的是，这一增长在模型版本更新节点处是平滑的——说明自主度增加不是模型能力跃升的结果，更可能是用户积累信任、尝试更有野心的任务的结果。

**2. 经验用户形成"放手+监控"双升范式**

用户行为随经验积累出现反直觉的双向变化：新用户约20%的会话使用完全自动批准，到750次会话时升至超过40%；与此同时，中断率从约5%升至约9%。这并非矛盾——它反映了监管策略的质变：从"每步审批"转向"主动监控、择机干预"。

内部数据印证了这一趋势的正面效果：Anthropic员工使用Claude Code的成功率翻倍，同时人均干预次数从5.4次降至3.3次。

**3. Agent主动暂停是被低估的安全机制**

在最复杂的任务中，Claude Code主动请求澄清的频率超过人工中断频率的两倍。Agent停止自身的五类原因：呈现方案选择（35%）、收集诊断信息（21%）、澄清模糊需求（13%）、请求缺失凭证（12%）、行动前寻求批准（11%）。训练模型识别并响应自身不确定性，是独立于外部防护措施的重要安全属性。

**4. 风险域渗透已开始但尚未规模化**

软件工程占公共API Agent活动近50%。在医疗、金融、网络安全领域已出现早期使用。低复杂度任务（如编辑单行代码）87%有某种形式的人工介入，高复杂度任务（如自主发现零日漏洞或编写编译器）仅67%——有人工介入的比例反而更低，与Claude Code的经验用户行为模式一致。

**5. 有效监管是质量而非频率的问题**

核心结论：有效的监管不要求审批每一个行动，而是在关键时刻有能力介入。这需要两个条件：一是部署后监控基础设施，使人类能够追踪Agent行为；二是新的人机交互范式，帮助人类和AI共同管理自主度和风险。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Deployment Overhang（部署滞后）** | 模型可处理的自主度远超用户在实践中授予的自主度，两者之间的系统性差距 |
| **Auto-approve（自动批准）** | Claude Code的配置模式，用户让Claude无需逐步确认地自主运行 |
| **Agent-initiated Stop（Agent主动暂停）** | Agent因不确定性主动停止并请求澄清，区别于人工中断 |
| **Turn Duration（任务时长）** | Claude Code中从Claude开始工作到停止之间的时间，用于衡量实际自主度的代理指标 |
| **Post-deployment Monitoring（部署后监控）** | 在Agent产品上线后持续追踪真实世界使用行为的基础设施能力 |
| **METR测评** | 外部机构对模型能力的基准评测，捕捉理想化条件下的上限，与实际部署行为形成互补 |
| **Tool call（工具调用）** | 本研究在公共API层面的基本分析单元，可跨越不同客户的架构差异进行一致观测 |

## 相关概念

- concepts/agentic-systems — Agent系统定义与架构，本文提供了大规模实证数据
- concepts/agent-evaluation — Agent评测体系，本文揭示能力测评与部署实践的差距
- concepts/agent-containment — Agent安全边界控制，本文补充了人类监管行为数据
- concepts/agent-sandboxing — Agent沙箱隔离，与本文探讨的监管模式互补
- concepts/harness-engineering — Harness工程，本文提供了Claude Code的实际运行数据
- concepts/managed-agents — 托管Agent架构，本文的监管发现对托管策略有直接意义

## 相关实体

- entities/anthropic — 本研究发布机构，建立了隐私保护Agent分析基础设施
- entities/claude-code — 主要研究对象，提供了深度的会话级自主度数据
- entities/claude-opus-4-6 — 文中作为能力参照的模型，METR评测中可完成5小时难度任务
- entities/browsecomp — 类似的Agent能力外部评测参照
- entities/swe-bench — 相关代码Agent评测基准，与本文的实测数据形成对比
