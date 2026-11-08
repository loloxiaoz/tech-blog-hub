---
title: "Supercharging Codex with JetBrains MCP at Skyscanner（Skyscanner 用 JetBrains MCP 增强 Codex）"
org: "OpenAI"
date: 2026-01-11
source_url: "https://developers.openai.com/blog/supercharging-codex-with-jetbrains-mcp-at-skyscanner"
tags: ["OpenAI", "Codex", "MCP", "JetBrains"]
summary_zh: "Skyscanner 把 JetBrains MCP 接给 Codex，让模型直接读取 IDE 的文件诊断和运行配置，缩短调试回路。"
summary_en: ""
---

# Supercharging Codex with JetBrains MCP at Skyscanner（Skyscanner 用 JetBrains MCP 增强 Codex）

## 给 Codex 补上 IDE 上下文

接入 JetBrains MCP 后，Codex 可以：

- 查找文件问题：用 IntelliJ 检查分析文件中的错误与警告
- 执行运行配置：运行预定义的 run configuration，并取回退出码和输出

## 更快发现错误

- 没有 MCP：生成代码 → 跑测试 → 读失败信息 → 修错
- 有 MCP：生成代码 → 向 JetBrains 查询文件问题 → 直接修准确的位置

## 预置测试与格式化

Codex 可以按需发现并运行已有的运行配置，从而减少所需上下文。示例 `AGENTS.md` 指令：

```text
## Code edit instructions
After you've finished editing:
- Use the jetbrains mcp (if available) to find any problems
- Run format command if available
- Run lint command if available
```

## 收益

- 反馈回路更快
- 往返提示更少
- 建议质量更高
- 更贴合现有工作流

