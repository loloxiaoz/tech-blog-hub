---
title: "How Codex ran OpenAI DevDay 2025（Codex 如何撑起 OpenAI DevDay 2025）"
org: "OpenAI"
date: 2025-10-10
source_url: "https://developers.openai.com/blog/how-codex-ran-openai-devday-2025"
tags: ["OpenAI", "Codex", "DevDay"]
summary_zh: "DevDay 2025 背后的 Codex 实战：一个下午实现 90 年代的 VISCA 协议并做出控制会场灯光的 MCP server，七个终端并行写 Phaser 游戏，午休回来应用已从 Streamlit 迁到 Next.js。"
summary_en: ""
---

# How Codex ran OpenAI DevDay 2025（Codex 如何撑起 OpenAI DevDay 2025）

## 控制摄像机与会场灯光

Romain Huet 的主题演讲 demo：Codex 实现了 1990 年代初的 VISCA 协议，并构建了一个控制会场灯光的 MCP server，全程只用一个下午。

## 节拍垫

Katia Gil Guzman 用 Codex Cloud 与 best-of-N，为 Apps SDK demo 并行迭代多个节拍垫设计。

## 多任务游戏设计

Kevin Whinnery 同时开了七个终端，每个跑一个 Codex CLI 实例，为 ArcadeGPT 编写单文件 Phaser 游戏实现。

## 重写 demo 应用

Dominik 用 Codex IDE 扩展把 Streamlit 应用迁到 Next.js + FastAPI。他去吃了个午饭，回来时应用已经完整实现。

## 把想法做成展台

Erika Kettleson 用 Codex 把草图变成展台 demo、为 SVG 生成写评测、评估单 agent 与多 agent 架构、并绘制 Mermaid 图。

## 规模化评审

Kaz 用 Codex 熟悉代码库、找出 bug、修复它们，并在 Guardrails SDK 发布时使用 Codex 代码评审。

## 同时处理多个项目

同时运行 3 到 4 个独立任务：快速下提示、把任务发出去、稍后再查状态。

## 整理文档

Codex Cloud 把零散的文档拆分、转换成 MDX、搭好导航结构，并开 PR。

## 处理顺手的小任务

Katia 用 Codex Web 的 best-of-n 功能，5 分钟上线了一个重新设计的 404 页面。
