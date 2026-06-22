---
title: "Kimi K2 模型更新，带来更强的代码能力、更快的 API"
org: "Moonshot AI"
date: 2025-09-05
source_url: "https://platform.kimi.com/blog/posts/kimi-k2-0905"
tags: ["Moonshot AI"]
summary: "Kimi K2 模型更新，带来更强的代码能力、更快的 API"
summary_zh: "Kimi K2 模型更新，带来更强的代码能力、更快的 API"
summary_en: ""
---

# Kimi K2 模型更新，带来更强的代码能力、更快的 API

Kimi K2 模型更新，带来更强的代码能力、更快的 API
发表于 2025年09月05日
•
3 min read
product
announcement
返回

今天，我们发布 Kimi K2 模型的最新版本 0905，进一步提升其在真实编程任务中的表现：

Agentic Coding 能力提升
：在公开基准测试和真实的编程任务中均展现出更好的性能

前端编程体验升级
：提升了前端代码的美观度和实用性

扩展上下文长度
：从 128K 升级到 256K，为复杂长线任务提供更好的支持

提供高速版 API
：支持高达 60-100 Token/s 的输出速度

在侧重考察真实软件工程任务的 SWE-bench Verified 等基准测试中，新版 Kimi K2 模型的表现如下：

Kimi 应用和网页版中的 K2 模型已全量升级到 0905 最新版，
下载 Kimi 应用
 (opens in a new tab)
 或访问
kimi.com
 (opens in a new tab)
 即可体验新版模型。

Kimi 开放平台
pplatform.moonshot.cn
 (opens in a new tab)
 已上架 kimi-k2-0905-preview 模型 API：

上下文升级到
256K

Token Enforcer 保证 toolcall
100% 格式正确

完全兼容 Anthropic API、并支持 WebSearch Tool，提供更好的 K2 + Claude Code 使用体验

支持全自动 Context Caching，有助于节省 Input Token

定价与之前的 0711 版相同

速度达 60-100 Token/s 的高速版 API（kimi-k2-turbo-preview）已同步升级新模型

如需自行部署模型，可在
Hugging Face
 (opens in a new tab)
、
ModelScope
 (opens in a new tab)
 等平台下载。

Kimi K2 模型最初发布于 7 月 11 日，它是一款混合专家架构（MoE）的开源基础模型，总参数 10000 亿，激活参数 320 亿。目前，AI 编程工具 Cursor、Windsurf、Trae、Cline、RooCode、Kilo Code 等已内置或接入了 Kimi K2 模型。国内外云服务厂商均部署了 Kimi K2 模型，为开发者提供更多选择。

Kimi K2 资料夹

技术博客：
https://moonshotai.github.io/Kimi-K2/
 (opens in a new tab)

技术报告：
https://arxiv.org/abs/2507.20534
 (opens in a new tab)

Github：
https://github.com/moonshotai/kimi-K2
 (opens in a new tab)

知乎讨论：
https://www.zhihu.com/question/1927140506573435010
 (opens in a new tab)
2025
 © Moonshot AI
用户中心
文档