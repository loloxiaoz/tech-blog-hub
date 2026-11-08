---
title: "Using Codex for education at Dagster Labs（Dagster Labs 用 Codex 做文档与教学）"
org: "OpenAI"
date: 2025-10-27
source_url: "https://developers.openai.com/blog/using-codex-for-education-at-dagster-labs"
tags: ["OpenAI", "Codex", "教育", "工程实践"]
summary_zh: "Dagster Labs 把 Codex 用在文档覆盖度评估、PR 解释和跨媒介内容转换上。"
summary_en: ""
---

# Using Codex for education at Dagster Labs（Dagster Labs 用 Codex 做文档与教学）

## CONTRIBUTING.md 的作用

结构良好的 `CONTRIBUTING.md` 既是给人看的文档，也是给 AI 看的地图。

## 用 Codex 理解代码

在 Codex 里使用 `gh` 命令解释 pull request：让它阅读 PR 描述与 diff，总结这个功能为什么要这样实现。

## 单体仓库的优势

代码、文档和示例都在同一个仓库里，Codex 能获得完整上下文。

## 跨媒介转换

Codex 很擅长在不同媒介之间转换：把教程整理成视频字幕，或把偏底层的教程改写成博客文章。

## 评估文档覆盖度

让 Codex 只依据文档生成代码，再对生成的代码跑测试，就能间接衡量文档的完整度。如果 Codex 仅凭文档就能写出可运行的代码，通常说明人也能做到。

