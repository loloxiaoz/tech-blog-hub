---
title: "Effective harnesses for long-running agents（长时运行Agent的有效Harness设计）"
org: "Anthropic"
date: 2025-11-26
source_url: "https://www.anthropic.com/research/disempowerment-patterns"
tags: ["Agent", "MCP"]
summary: "每个新会话从零开始，没有任何前一个会话的记忆。上下文压缩（compaction）虽然能防止单个会话耗尽Token，但无法解决跨多个上下文窗口的持续进展问题。即使是Opus 4.5这样的前沿模型，在只给高层提示（如\"构建claude.ai的克隆\"）的情况下，也会在多会话循环中失"
summary_zh: "每个新会话从零开始，没有任何前一个会话的记忆。上下文压缩（compaction）虽然能防止单个会话耗尽Token，但无法解决跨多个上下文窗口的持续进展问题。即使是Opus 4.5这样的前沿模型，在只给高层提示（如\"构建claude.ai的克隆\"）的情况下，也会在多会话循环中失"
summary_en: ""
---



# Effective harnesses for long-running agents（长时运行Agent的有效Harness设计）

## 核心观点

**1. 长时运行Agent的根本挑战是跨会话失忆**

每个新会话从零开始，没有任何前一个会话的记忆。上下文压缩（compaction）虽然能防止单个会话耗尽Token，但无法解决跨多个上下文窗口的持续进展问题。即使是Opus 4.5这样的前沿模型，在只给高层提示（如"构建claude.ai的克隆"）的情况下，也会在多会话循环中失败。

**2. 双Agent架构是解法核心：初始化Agent + 编码Agent**

第一个会话使用专用初始化Agent，负责搭建所有后续Agent赖以工作的环境基础：结构化功能列表（feature_list.json）、环境启动脚本（init.sh）、进度追踪文件（claude-progress.txt）和初始git commit。之后的每个会话由编码Agent承担，固定流程：读取进度文件 → 运行基础测试 → 选取一个未完成功能 → 实现并测试 → 提交git + 更新进度。

**3. JSON格式的Feature List是防止「提前宣布完工」的核心机制**

初始化Agent生成包含200+功能的JSON文件，每条功能初始标记为`passes: false`，并包含详细的端到端测试步骤。使用JSON而非Markdown，原因是模型更不容易意外修改或覆盖JSON文件。编码Agent被严格指示只能通过修改`passes`字段来更新功能状态，禁止删除或编辑测试条目。

**4. 端到端测试必须显式要求，否则模型只做单元测试**

实验观察到Claude默认倾向于用单元测试或curl命令验证功能，而不会像真实用户一样进行端到端操作。显式要求使用Puppeteer MCP等浏览器自动化工具后，功能验证完整性显著提升。当前仍存在局限：Claude无法通过Puppeteer MCP看到浏览器原生alert弹窗，导致依赖alert的功能容易出现Bug。

**5. Clean state契约：git history成为Agent间通信媒介**

每次会话结束时必须处于"可合并到主分支"的清洁状态：无重大Bug、代码有序且文档完整。具体实现：每次进展都提交带描述性信息的git commit，并更新进度文件。这让后续Agent能通过git log和进度文件快速了解状态，也让模型可以回滚到已知良好状态。

## 关键术语

- **Initializer Agent（初始化Agent）**：仅在第一个会话运行，专用于搭建后续所有编码Agent需要的工作环境基础设施
- **Coding Agent（编码Agent）**：每个后续会话运行，执行固定的"上下文 → 测试 → 实现 → 提交"循环
- **Feature List（功能列表）**：JSON格式的端到端功能需求文件，每条功能含测试步骤和通过状态，由初始化Agent生成
- **claude-progress.txt**：跨会话进度日志文件，记录每个Agent会话的工作摘要，是会话间的文字通信媒介
- **init.sh**：环境启动脚本，每个编码Agent会话开始时执行，确保开发服务器处于运行状态
- **Clean State（清洁状态）**：会话结束时的代码质量要求，等同于可合并到主分支的代码：无重大Bug、有序、有文档
- **Compaction（上下文压缩）**：Claude Agent SDK的内置机制，防止单个会话耗尽上下文窗口，但不足以解决跨会话问题
- **Multi-context window workflow（多上下文窗口工作流）**：跨多个会话窗口持续推进同一复杂任务的工程架构模式
- **Puppeteer MCP**：浏览器自动化MCP工具，用于让Agent进行端到端功能验证

## 相关概念

- concepts/harness-engineering — 本文是Harness Engineering在长时任务场景的具体工程实践
- concepts/memory-systems — claude-progress.txt + git history是外部化Agent情景记忆的工程实现
- concepts/agentic-systems — 双Agent架构体现了多Agent协作的工作流设计
- concepts/compaction — 本文明确指出compaction不足以解决跨会话问题
- concepts/workflow-patterns — 初始化-编码双阶段是工作流模式的具体实例
- concepts/agent-evaluation — Feature List的passes字段实质上是内嵌在任务中的自动化验收标准

## 相关实体

- entities/anthropic — 本文作者所在机构，Claude Agent SDK的开发方
- entities/claude-agent-sdk — 本文实验的基础Agent Harness平台
- entities/claude-code — Claude Agent SDK是Claude Code生态的核心组件
