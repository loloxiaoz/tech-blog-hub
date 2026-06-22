---
title: "A Postmortem of Three Recent Issues"
org: "Anthropic"
date: 2025-09-17
source_url: "https://www.anthropic.com/engineering/april-23-postmortem"
tags: ["Eval/评测", "Claude Code"]
summary: ""
summary_zh: ""
summary_en: ""
---



# A Postmortem of Three Recent Issues

## 核心观点

**三个叠加Bug造成大规模响应退化**。2025年8月至9月间，Anthropic的三个基础设施Bug同时存在，造成Claude响应质量间歇性下降：(1) 上下文窗口路由错误——短上下文请求被路由到1M token上下文服务器，最严重时影响16%的Sonnet 4请求，约30%的Claude Code用户至少有一条消息受影响；(2) 输出污染——TPU服务器配置错误导致token生成时偶发高概率输出不相关字符（如英文回复中出现泰文）；(3) XLA:TPU编译器误编译——approximate top-k操作在特定批大小和配置下偶发返回完全错误的结果。

**XLA编译器Bug根因是混合精度不一致**。模型以bf16（16位浮点）计算下一个token的概率，但TPU向量处理器是fp32原生的，XLA编译器在`xla_allow_excess_precision`标志（默认开启）下会把部分操作转换为fp32，造成精度不一致——参与比较的操作对"最高概率token是谁"产生分歧，导致最高概率token有时被完全排除在外。更复杂的是，2024年12月为修复temperature=0时丢失最高概率token问题而部署的临时补丁，无意中掩盖了approximate top-k的深层Bug；修复原始问题时移除了该补丁，反而暴露了更根本的问题。

**检测困难揭示评测体系的结构性盲区**。三大原因导致检测滞后：一是评测集无法捕获真实退化——Claude往往能从孤立错误中恢复，使得评测分数不能反映用户体验；二是隐私保护限制了工程师查阅用户交互进行诊断；三是三个Bug在不同平台以不同比例产生不同症状，制造了混乱的矛盾报告，直到负载均衡变更扩大影响范围才触发系统性调查。

**改进方向：从测试环境评测转向持续生产评测**。核心变化是将质量评测部署到真实生产系统上持续运行（而非仅在测试和发布前），同时开发更敏感的评测（能区分正常和异常实现）、开发不侵犯隐私的调试工具。此外，社区用户反馈（具体变化描述、意外行为示例、跨用例规律）是内部评测的重要互补信号。

**Anthropic明确否认流量压力降质**。文章开篇明确声明"我们从不因需求量、时段或服务器负载降低模型质量"，并首次公开如此详细的基础设施技术细节，体现了对透明度的承诺。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Sticky routing（粘性路由）** | 一旦某个请求被分配到某台服务器，后续的追问请求也会被路由到同一服务器——路由错误因此会持续影响整个对话 |
| **approximate top-k** | 性能优化操作，通过接受最低概率token的少量不准确来快速找到最高概率token；bug触发时会错误丢弃最高概率token |
| **top-p sampling** | 仅考虑累积概率达到阈值（通常0.99或0.999）的token进行采样，避免无意义输出 |
| **bf16 / fp32** | bf16（bfloat16）是16位浮点格式，fp32是32位标准浮点；二者精度不同，混用会造成数值不一致 |
| **xla_allow_excess_precision** | XLA编译器标志，默认开启，允许编译器将bf16操作提升为fp32以优化性能，是本次Bug的根本触发条件 |
| **XLA:TPU** | 将JAX/XLA高层优化语言编译为TPU机器指令的优化编译器；本次Bug在编译器层面存在 |
| **canary deployment** | 金丝雀发布，先部署到小比例流量验证，再全量推送；本次事件说明canary阶段评测覆盖不够充分 |
| **context window routing（上下文窗口路由）** | 根据请求的上下文长度将请求分配到相应配置服务器的路由机制；Bug导致短上下文请求被分配到1M token服务器 |
| **output corruption（输出污染）** | TPU服务器配置错误导致token生成时偶发高概率输出不相关字符（如英文提问中出现泰文）的现象 |

## 相关概念

- concepts/agent-evaluation — 本文揭示了评测体系的关键盲区：间歇性Bug难以被标准评测捕获，以及生产持续评测的必要性
- concepts/harness-engineering — 多平台部署（AWS Trainium/NVIDIA GPU/Google TPU）的等价性挑战，强化了跨平台Harness验证的重要性
- concepts/context-window — 上下文窗口路由Bug直接涉及不同上下文长度请求的服务器配置差异

## 相关实体

- entities/anthropic — 本文作者机构，首次发布详细基础设施Bug技术复盘
- entities/claude-code — 受影响最严重的用户群（约30%用户至少有一条消息路由错误），内置/bug反馈命令
