---
title: "Building a C compiler with a team of parallel Claudes"
org: "Anthropic"
date: 2026-02-05
source_url: "https://www.anthropic.com/engineering/parallel-claudes-c-compiler"
tags: ["Agent", "Claude Code", "长上下文"]
summary: "16个Claude实例通过git锁文件（current_tasks/目录）分配任务，每个Agent在独立Docker容器中工作，推送到共享bare git repo，合并冲突由Claude自行处理。没有编排Agent，每个Agent自主决定\"下一步最显而易见的问题\"是什么。作"
summary_zh: "16个Claude实例通过git锁文件（current_tasks/目录）分配任务，每个Agent在独立Docker容器中工作，推送到共享bare git repo，合并冲突由Claude自行处理。没有编排Agent，每个Agent自主决定\"下一步最显而易见的问题\"是什么。作"
summary_en: ""
---



# Building a C compiler with a team of parallel Claudes

## 核心观点

**1. Agent Teams：无中央编排器的去中心化并行协作**

16个Claude实例通过git锁文件（current_tasks/目录）分配任务，每个Agent在独立Docker容器中工作，推送到共享bare git repo，合并冲突由Claude自行处理。没有编排Agent，每个Agent自主决定"下一步最显而易见的问题"是什么。作者刻意保持极简：无Agent间通信协议，无高层目标管理机制。

**2. 长期自主运行的瓶颈在环境设计，不在Prompt**

Harness的核心是让Claude在没有人类监督的情况下能够自我定向。四个关键设计：①测试验证器必须接近完美（否则Agent解错问题）；②控制上下文污染（测试输出只打印几行，详情写入日志文件，日志格式为grep友好的ERROR行）；③补偿时间盲区（--fast选项用1%-10%随机采样跑测试，每个VM采样不同文件，合起来覆盖全部）；④维护面向Agent的README和进度文档（fresh container中无历史上下文，必须从文档中重建状态）。

**3. 并行化的真正难题：任务粒度**

测试套件阶段（99%通过率之前）天然可并行——每个Agent选不同的失败测试。但Linux内核编译是单一巨型任务，16个Agent都卡在同一个bug上，互相覆盖修改。解法：用GCC作为oracle，让每个Agent只负责内核中一个随机子集的文件，通过二分法定位Claude编译器的问题文件。任务分解粒度决定了多Agent系统的实际并行上限。

**4. 专业化Agent分工带来额外收益**

除主力编译任务外，作者分配了专职角色：代码去重Agent、性能优化Agent、编译输出优化Agent、Rust代码审查Agent、文档维护Agent。LLM代码容易产生重复实现，专职去重Agent是解决这一问题的务实方案。

**5. Opus 4.6的能力边界：已接近上限**

2000次Claude Code会话、2B输入tokens、140M输出tokens、$20,000，产出10万行Rust C编译器：能编译Linux 6.9（x86/ARM/RISC-V）、QEMU、FFmpeg、postgres、redis，通过GCC torture test suite 99%，能编译运行Doom。但无法独立实现16位x86实模式引导（编译输出超过Linux 32k限制），生成代码效率低于GCC -O0。能力边界的精确刻画本身是研究价值：stress-test极限，才能预判下一代模型的可靠能力区间。

## 关键术语

| 术语 | 定义 |
|------|------|
| **Agent Teams** | 多Claude实例无人监督并行协作，通过环境机制（git锁）分工，无中央编排器 |
| **Ralph-loop** | 将Claude置于无限bash循环的简单Harness模式，会话结束自动重启 |
| **任务锁（Task Lock）** | Agent通过在current_tasks/目录写文件占用任务，git冲突机制防止重复认领 |
| **GCC Oracle** | 用已知正确的参照编译器验证输出，通过二分法定位被测编译器的问题文件 |
| **Context Window Pollution（上下文污染）** | 测试输出过多无效字节消耗上下文，导致Agent无法聚焦关键信息 |
| **Time Blindness（时间盲区）** | Claude无法感知时间流逝，可能花大量时间跑测试而非推进任务 |
| **--fast 采样** | 每个Agent以1%-10%随机子集跑测试，跨VM采样不同文件，平衡速度与覆盖率 |
| **Delta Debugging** | 通过二分缩小找到最小失败用例集，用于定位成对互相干扰的文件 |
| **SSA IR** | Static Single Assignment中间表示，支持多优化Pass的编译器内部形式 |
| **Clean-room实现** | 全程无互联网访问，仅依赖Rust标准库的独立实现 |

## 相关概念

- concepts/harness-engineering — Harness工程范式，本文是其最大规模实践案例之一
- concepts/agentic-systems — 多Agent架构的理论框架，本文是去中心化多Agent的典型实现
- concepts/agent-evaluation — GCC Oracle是面向并行Agent的特殊任务验证器设计
- concepts/agent-teams — 本文核心概念，待新建
- concepts/context-window — 上下文污染问题与Claude的Token预算约束
- concepts/workflow-patterns — 并行化Workflow模式的具体工程实践

## 相关实体

- entities/anthropic — 作者所在机构，项目发布在github.com/anthropics/claudes-c-compiler
- entities/claude-code — 本文Harness的核心工具，以--dangerously-skip-permissions模式运行
