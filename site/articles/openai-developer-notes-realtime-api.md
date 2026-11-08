---
title: "Developer notes on the Realtime API（Realtime API 开发者笔记）"
org: "OpenAI"
date: 2025-09-12
source_url: "https://developers.openai.com/blog/developer-notes-on-the-realtime-api"
tags: ["OpenAI", "Audio", "Realtime API"]
summary_zh: "Realtime API 正式版的变化：图像输入、长上下文、异步函数调用、MCP、欧盟数据驻留、空闲超时等。"
summary_en: ""
---

# Developer notes on the Realtime API（Realtime API 开发者笔记）

## 模型改进

- 在 realtime playground 里试验提示词
- 使用 marin 或 cedar 音色以获得最佳质量
- 为新模型重写提示词，具体指令现在更有效

## API 形态变化

正式版包含：图像输入、长上下文、异步函数调用、MCP（配合异步函数调用最佳）、音频 token 转文本、欧盟数据驻留、SIP、空闲超时。

正式版接口移除了 temperature；Beta 版限制在 0.6–1.2，默认 0.8。

## 新功能

**会话空闲超时**：在 `server_vad` 设置中配置 `idle_timeout_ms`，静音一段时间后触发模型说「你还在吗？」

**长会话与上下文处理**：

- 单个会话最长 60 分钟（原为 30 分钟）
- token 窗口 32,768；最大响应 4,096；最大输入 28,672
- 自动截断，可配置保留比例（推荐 0.8，对缓存友好）

**异步函数调用**：正式版 API 在等待函数返回时加入占位响应。

**欧盟数据驻留**：特定模型快照可通过 `https://eu.api.openai.com` 使用。

**追踪**：把 trace 记录到开发者控制台，并新增事件类型。

**托管提示词**：通过 ID 引用提示词，支持版本固定与变量。

**Sideband 连接**：同一 realtime 会话可以同时有客户端和服务端两条连接，服务端可监控会话、更新指令并响应工具调用。

