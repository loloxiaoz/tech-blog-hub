---
title: "Desktop Extensions: One-click MCP server installation for Claude Desktop"
org: "Anthropic"
date: 2025-06-26
source_url: "https://www.anthropic.com/engineering/desktop-extensions"
tags: ["MCP", "Claude Code"]
summary: "Desktop Extensions 通过 `.mcpb`（MCP Bundle）格式将完整 MCP 服务器及其依赖打包为单一 ZIP 压缩文件，解决了普通用户因需要手动安装运行时环境、编辑配置文件、处理依赖冲突而无法使用本地 MCP 服务器的核心痛点。安装流程从「下载 → np"
summary_zh: "Desktop Extensions 通过 `.mcpb`（MCP Bundle）格式将完整 MCP 服务器及其依赖打包为单一 ZIP 压缩文件，解决了普通用户因需要手动安装运行时环境、编辑配置文件、处理依赖冲突而无法使用本地 MCP 服务器的核心痛点。安装流程从「下载 → np"
summary_en: ""
---



# Desktop Extensions: One-click MCP server installation for Claude Desktop

## 核心观点

Desktop Extensions 通过 `.mcpb`（MCP Bundle）格式将完整 MCP 服务器及其依赖打包为单一 ZIP 压缩文件，解决了普通用户因需要手动安装运行时环境、编辑配置文件、处理依赖冲突而无法使用本地 MCP 服务器的核心痛点。安装流程从「下载 → npm install → 编辑 JSON → 重启」压缩为「下载 .mcpb → 双击 → 点击安装」三步。

架构设计以 `manifest.json` 为核心声明文件，支持 Node.js、Python、二进制三种服务器类型。通过模板字面量（`${__dirname}`、`${user_config.key}`、`${HOME}`）实现安装路径和用户配置的动态替换，API 密钥等敏感配置自动存入操作系统 Keychain，Claude Desktop 内置了 Node.js 运行时从而消除外部依赖。

Anthropic 同步开源了完整的 MCPB 规范、打包工具链（`@anthropic-ai/mcpb`）和参考实现（TypeScript 类型与 Schema），目标是让 MCPB 格式成为跨应用的行业标准，做到「打包一次，处处运行」，不只服务于 Claude Desktop，而是所有支持 MCP 的 AI 桌面应用。

企业级支持涵盖 Windows Group Policy / macOS MDM 管控、预装审批扩展、发布者黑名单、私有扩展目录等，说明 Desktop Extensions 被定位为面向组织部署的正式工程能力。Claude Code 可辅助开发者从规范阅读到代码生成全流程构建扩展。

内部实践（PyBoy GameBoy 模拟器扩展）展示了该格式如何将实验性能力快速分发给用户：一个 `.mcpb` 文件即可把任意本地工具能力交付给终端用户，构成「从 MCP 服务器到百万用户」的最后一公里分发链路。

## 关键术语

- **Desktop Extension / MCPB**：`.mcpb`（MCP Bundle）文件，ZIP 压缩包格式，包含 MCP 服务器代码、依赖和 manifest.json，可在 Claude Desktop 中一键安装
- **manifest.json**：扩展的声明文件，描述服务器类型、入口点、用户配置需求、功能列表（tools/prompts）、兼容性约束等元数据
- **user_config**：manifest 中的用户配置声明区块，定义需从用户收集的参数类型（string/directory/number）、是否敏感（sensitive）、是否必填（required）
- **模板字面量（Template Literals）**：manifest 中的动态变量语法，如 `${__dirname}`（扩展安装目录）、`${user_config.key}`（用户提供的配置值）、`${HOME}`（系统环境变量）
- **扩展目录（Extension Directory）**：Claude Desktop 内置的扩展浏览/搜索/安装界面，取代了原先在 GitHub 搜索的发现机制
- **mcpb init / mcpb pack**：官方 CLI 工具命令，分别用于交互式生成 manifest.json 和打包 `.mcpb` 文件
- **OS Keychain**：操作系统密钥存储（macOS Keychain / Windows Credential Manager），Desktop Extensions 将 API Key 等敏感信息自动存储于此
- **平台覆盖（Platform Override）**：manifest 中 `platforms.win32` / `platforms.darwin` 配置块，用于在不同操作系统下使用不同命令或环境变量

## 相关概念

- entities/mcp — MCP 协议实体页，Desktop Extensions 是 MCP 服务器的分发与安装层
- concepts/agentic-systems — 本地 MCP 服务器是 Agent 获取工具能力的核心途径
- concepts/aci — Agent-Computer Interface，MCP 服务器设计即是 ACI 的实践

## 相关实体

- entities/anthropic — Desktop Extensions 的发布方，同时开源 MCPB 规范
- entities/claude-code — 文章推荐使用 Claude Code 辅助构建 Desktop Extensions
