---
title: "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet"
org: "Anthropic"
date: 2025-01-06
source_url: "https://www.anthropic.com/engineering/swe-bench-sonnet"
tags: ["Agent", "Eval/评测", "多模态", "Harness工程"]
summary: ""
summary_zh: ""
summary_en: ""
---



# Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

## 核心观点

**SWE-bench衡量的是完整Agent系统，而非单纯的模型能力。** 评测对象是「模型+软件Scaffold」的组合。Scaffold负责生成Prompt、解析模型输出并执行动作、将动作结果注入下一轮Prompt。相同模型配不同Scaffold，性能差异显著——这也是开源社区和初创公司能持续刷榜的原因。

**最优Scaffold哲学是「最小化控制、最大化模型自主权」。** Anthropic只为Claude 3.5 Sonnet配备了两个通用工具（Bash Tool和Edit Tool），不预设任何步骤跳转逻辑，让模型自行决定如何推进问题。Prompt只提供建议性方向，而非严格的分步指令。不在乎Token成本时，鼓励模型产出更长响应也能提升性能。

**工具描述（tool description）比Schema本身更关键，需要像设计人机界面一样认真对待。** Bash Tool的Schema极简（仅接收命令字符串），但工具描述包含了转义输入、无法访问互联网、后台运行命令等详细指引。Edit Tool更复杂，描述中内嵌了完整的使用规范。团队通过大量测试发现模型误解点，并在描述中预先规避这些问题。

**工具防错设计（error-proofing）是实际工程核心。** 模型在切换工作目录后常弄错相对路径，解决方案是强制要求绝对路径。文件编辑策略经多轮实验后选定字符串替换（old_str → new_str），且只有精确唯一匹配时才执行，否则返回明确错误供模型重试，可靠性最高。

**SWE-bench实际运行面临四类工程挑战。** （1）高成本：成功运行常需数百轮、超10万Token；（2）评分噪音：环境配置问题或Patch重复应用导致误判失败；（3）隐藏测试集：模型无法看到评分用的单元测试，常误以为已解决问题，部分失败源于抽象层面选错（打补丁而非深层重构）；（4）多模态未充分利用：未接入文件系统图片查看能力，影响Matplotlib等视觉相关任务。

## 关键术语

- **SWE-bench Verified**：SWE-bench的500题人工审核子集，剔除了因缺少外部上下文而不可解的任务，是当前最权威的代码Agent能力评测基准
- **Agent Scaffold**：围绕AI模型构建的软件脚手架，负责Prompt生成、模型输出解析、动作执行和交互循环管理，与模型本身共同构成完整Agent
- **Bash Tool**：让模型执行Shell命令的工具，Schema极简只接收命令字符串，关键信息通过工具描述传递
- **Edit Tool**：包含文件查看、创建、编辑全部能力的复合工具，采用old_str/new_str字符串替换机制，唯一匹配才执行
- **Error-proofing（防错设计）**：通过工具约束主动避免模型常见错误，如强制绝对路径、精确匹配才执行编辑
- **String replacement（字符串替换）**：SWE-bench实验中可靠性最高的文件编辑策略，指定old_str和new_str，仅唯一匹配时执行
- **Self-correction（自我纠错）**：新版Claude 3.5 Sonnet相比旧版更频繁地自我纠正，能尝试多种不同解法而非反复犯相同错误
- **SWE-Agent框架**：开源Agent运行框架，Anthropic以其为基础构建SWE-bench评测Agent

## 相关概念

- concepts/agent-evaluation — SWE-bench Verified作为代码Agent评测标杆的具体实践
- concepts/aci — 工具描述设计、防错机制是ACI原则的实际应用
- concepts/harness-engineering — 最小化Scaffold哲学与Harness设计高度相关
- concepts/agentic-systems — 评测对象是完整Agent（模型+Scaffold），印证了Agent系统定义

## 相关实体

- entities/anthropic — 文章作者所在机构，Claude 3.5 Sonnet研发方
- entities/claude-code — SWE-bench实验工具设计与Claude Code工具链设计一脉相承
