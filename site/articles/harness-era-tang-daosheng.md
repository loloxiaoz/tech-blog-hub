---
title: "汤道生：人工智能正式进入 Harness 时代"
org: ""
date: 2026-04-13
source_url: "https://mp.weixin.qq.com/s/腾讯研究院"
tags: ["Agent", "Eval/评测", "Harness工程", "工具调用"]
summary: "Harness（马具）：缰绳+辔头+马鞍+挽具的统称，把野马力量转化为可控能力的系统。AI 领域的 Harness = 代码+配置+执行逻辑+反馈循环+约束机制。"
summary_zh: "Harness（马具）：缰绳+辔头+马鞍+挽具的统称，把野马力量转化为可控能力的系统。AI 领域的 Harness = 代码+配置+执行逻辑+反馈循环+约束机制。"
summary_en: ""
---



# 汤道生：人工智能正式进入 Harness 时代

## 基本信息

- **作者**：汤道生，腾讯集团高级执行副总裁、云与智慧产业事业群 CEO
- **视角**：产业/战略视角，非技术细节，更多是 framing 和判断

## 核心框架

**大模型是发动机，Harness 是线束，使用者是驾驶员。**

Harness（马具）：缰绳+辔头+马鞍+挽具的统称，把野马力量转化为可控能力的系统。AI 领域的 Harness = 代码+配置+执行逻辑+反馈循环+约束机制。

## 核心论断

> 真正稀缺的能力，不在模型里面，在模型外面。

**四个实践发现**：

1. **模型能力天花板在模型外面**
   - 同一模型换 Harness：编程成功率 42%→78%（Nate B Jones）
   - Terminal Bench 2.0：52.8%→66.5%，排名进前五（LangChain）
   - Anthropic 数据：完整 Harness 交付真正可用产品，简单方式完全无效

2. **约束是对智能的引导，不是压制**
   - 清晰边界让 Agent 更快收敛到正确答案（Cursor 团队发现）

3. **Harness 让 AI 更安全**
   - 权限边界+沙箱隔离+操作审计+人工审批节点

4. **AI 无法可靠评价自己**
   - "开箱即用的 Claude 是一个很差的 QA Agent"（Anthropic 工程师）
   - 必须在模型外部建立独立评估机制

## AI 工程演进三阶段

```
Prompt Engineering（2022-2025）：如何写好一条指令 → 地图
Context Engineering（2025）    ：如何动态构建上下文 → 导航系统
Harness Engineering（2026）    ：如何搭建整个工作环境 → 完整的车
```

三者是包含关系，不是替代。

## Skills 模块

基于自然语言描述的能力单元，告诉模型"工具是什么、能干什么、怎么调用"。通用性：能被不同 Harness 框架调用。SkillHub 是 Skills 的流通平台。

## 对人的要求更高，不是更低

类比自动驾驶：能监督自动驾驶系统的人，比普通驾驶员要求更高。

真正稀缺的能力：**品味**——判断什么是好的、什么是对的、什么是值得做的能力。

## 终局判断

模型正在内化今天需要外部搭建的能力（工具调用、上下文管理、记忆系统）。**外面的脚手架正在变薄。**

但有一件事模型永远无法自己生成：**目的地**。方向、意义、价值判断，永远是人的责任。

## 与 wiki 已有概念的关联

- concepts/harness-engineering — Harness 工程详细概念页
- concepts/context-engineering — 上一阶段：Context Engineering
- concepts/agentic-systems — 智能体系统，Harness 的核心应用场景
- concepts/tool-retrieval — Skills 的检索机制，Harness 的关键能力
