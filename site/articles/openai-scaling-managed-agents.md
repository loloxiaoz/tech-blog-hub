---
title: "Scaling Managed Agents: Decoupling the brain from the hands（扩展托管式 Agent：把「大脑」和「双手」解耦）"
org: "OpenAI"
date: 2026-01-14
source_url: "https://developers.openai.com/blog/scaling-managed-agents"
tags: ["OpenAI", "Agent", "Managed Agents", "架构"]
summary_zh: "Anthropic 的托管服务 Managed Agents 把 session、harness、sandbox 虚拟化成稳定接口，让「大脑」与「双手」独立替换、独立失败：p50 首 token 延迟降低约 60%，p95 降低 90% 以上。"
summary_en: ""
---

# Scaling Managed Agents: Decoupling the brain from the hands（扩展托管式 Agent：把「大脑」和「双手」解耦）

## 问题：harness 会过时

工程博客上反复出现的一个主题，是如何构建有效的 agent、如何为长时间运行的任务设计 harness。这些工作有一个共同点：harness 总是在编码「Claude 自己做不到什么」的假设。而随着模型进步，这些假设会过时，必须经常被重新质疑。

一个例子：此前发现 Claude Sonnet 4.5 会在感觉接近上下文上限时提前收尾任务——有时被称为 context anxiety。于是 harness 里加了 context reset。但把同一套 harness 用在 Claude Opus 4.5 上时，这个行为消失了，reset 成了纯粹的负担。

harness 会继续演化。因此 Anthropic 构建了 Managed Agents：Claude 平台上的托管服务，通过一小组接口替你运行长周期 agent，这些接口的设计目标是比任何具体实现活得更久——包括今天在跑的实现。

## 借鉴操作系统

这其实是计算机科学的老问题：如何为「尚未被想到的程序」设计系统。几十年前，操作系统通过把硬件虚拟化成进程、文件等足够通用的抽象来解决它。抽象比硬件活得更久：read() 不关心背后是 1970 年代的磁盘组还是现代 SSD。上层抽象保持稳定，底层实现可以自由更换。

Managed Agents 采用同样的模式，把 agent 的组件虚拟化：

- session：只追加的事件日志，记录发生的一切
- harness：调用 Claude、把 Claude 的工具调用路由到相关基础设施的循环
- sandbox：Claude 可以运行代码、编辑文件的执行环境

这样每个组件的实现都可以在不打扰其他组件的情况下替换。Anthropic 对接口的形状有明确主张，对接口背后跑什么不设限。

## 不要养宠物

最初，所有组件被塞进一个容器：session、harness、sandbox 共享同一环境。好处是文件编辑就是直接 syscall，也不需要设计服务边界。

但把所有东西耦合成一个容器，撞上了一个老的基础设施问题：我们养了一只宠物。在 pets-vs-cattle 的比喻里，宠物是有名字、需要亲手照料、不能失去的个体；牛则是可互换的。在这里，容器成了那只宠物：容器挂了，session 就丢了；容器无响应，就得把它「护理」回来。

护理容器意味着调试卡死的 session。唯一的观察窗口是 WebSocket 事件流，但它无法告诉你故障发生在哪里——harness 的 bug、事件流丢包、容器掉线，看起来都一样。想定位问题，工程师得进容器开 shell；但容器里往往还有用户数据，这实际上等于无法调试。

第二个问题：harness 假设「Claude 处理的东西」就住在同一个容器里。客户要求把 Claude 接到自己的 VPC 时，只能对等网络，或者在自家环境跑 Anthropic 的 harness。一个写死在 harness 里的假设，在需要连接不同基础设施时就成了障碍。

## 把「大脑」和「双手」解耦

解法是把「大脑」（Claude 与它的 harness）从「双手」（执行动作的 sandbox 与工具）以及「session」（事件日志）中解耦。每个都成为对其他组件假设很少的接口，可以独立失败、独立替换。

**harness 离开容器。** 调用容器的方式变成一次工具调用：`execute(name, input) → string`。容器成了「牛」：容器死了，harness 把失败当作工具调用错误捕获，交回给 Claude；Claude 若决定重试，就用标准配方 `provision({resources})` 重新初始化一个新容器。不再需要护理失败的容器。

**harness 失败也能恢复。** harness 同样成了「牛」。因为 session 日志在 harness 之外，harness 里没有任何东西需要在崩溃后存活。新的 harness 用 `wake(sessionId)` 启动，用 `getSession(id)` 取回事件日志，从最后一个事件继续。代理循环中，harness 用 `emitEvent(id, event)` 写入 session，保持持久记录。

**安全边界。** 在耦合设计里，Claude 生成的不可信代码与凭证跑在同一个容器中，提示注入只需说服 Claude 读取自己的环境。攻击者一旦拿到这些 token，就能开新的、不受限制的 session 并委派工作。缩小 token 权限是显然的缓解，但这又编码了「Claude 拿到受限 token 后做不到什么」的假设——而 Claude 正变得越来越聪明。结构性解法是让 token 永远无法从 Claude 生成代码所在的 sandbox 触及。

具体用两种模式：

- Git：初始化沙箱时用仓库的访问 token 克隆仓库，并把它写进本地 git remote。push 与 pull 都在 sandbox 内完成，agent 从不亲手处理 token
- 自定义工具：支持 MCP，把 OAuth token 存在 sandbox 之外的安全 vault。Claude 通过专用代理调用 MCP 工具；代理接收与会话关联的 token，从 vault 取出对应凭证，再对外部服务发起调用。harness 始终不知道任何凭证

## Session 不是 Claude 的上下文窗口

长周期任务常常超出上下文窗口，而标准的应对方式都涉及「保留什么」的不可逆决定。例如 compaction 让 Claude 保存上下文窗口的摘要，memory 工具让 Claude 把上下文写入文件、跨会话学习；这些还可以配合上下文裁剪，选择性移除旧工具结果或 thinking block。

但对上下文做选择性的保留或丢弃，可能带来失败。很难知道未来轮次需要哪些 token。如果消息被压缩步骤改写，harness 会把它从 Claude 的上下文窗口中移除，只有存下来才能恢复。

在 Managed Agents 中，session 提供了同样的好处：它是一个活在 Claude 上下文窗口之外的上下文对象。但上下文不是存在 sandbox 或 REPL 里，而是持久化在 session 日志中。`getEvents()` 接口让「大脑」通过选择事件流的位置切片来查询上下文：从上次停下的地方继续、回退几个事件看前因、或在某个动作前重读上下文。

取回的事件还可以在 harness 中做任意变换，再送进 Claude 的上下文窗口。这些变换由 harness 决定，包括组织上下文以获得高 prompt cache 命中率，以及各种上下文工程。Anthropic 把「可恢复的上下文存储」放在 session，「任意的上下文管理」放在 harness，因为无法预测未来的模型需要什么样的上下文工程。

## 多个大脑，多双手

**多大脑。** 解耦解决了最早的客户抱怨之一：团队想让 Claude 处理自己 VPC 里的资源时，过去只能对等网络；harness 离开容器后，这个假设消失了。

同一改动还带来性能收益。大脑放在容器里时，多少大脑就要多少容器；每个大脑都必须等容器配置完成才能开始推理，每个会话都要先付完整的容器启动成本。

这段空转体现在 time-to-first-token（TTFT）上——用户感受最强烈的延迟。解耦后，容器由大脑通过工具调用按需创建；不需要容器的会话就不必等待。编排层一从 session 日志取到待处理事件，推理就能开始。p50 TTFT 降低约 60%，p95 降低 90% 以上。扩展到多大脑，只是启动多个无状态 harness，需要时再连接双手。

**多双手。** Anthropic 也希望每个大脑能连接多双手。这意味着 Claude 必须推理多个执行环境并决定把工作发到哪里——比在单一 shell 中操作更难。早期模型做不到，所以最初把大脑放进单个容器；随着智能提升，单容器反而成了限制：容器一挂，大脑伸向的每一双手都丢状态。

解耦后，每只手都是一个工具：`execute(name, input) → string`，输入名字与参数，返回字符串。这个接口支持任何自定义工具、任何 MCP server，以及 Anthropic 自家工具。harness 不需要知道 sandbox 是容器、手机还是 Pokémon 模拟器。因为没有手与某个大脑绑定，大脑之间可以互相传递手。

## 结论

面对的仍是一个老问题：如何为「尚未被想到的程序」设计系统。操作系统靠把硬件虚拟化成足够通用的抽象，活了几十年。Managed Agents 的目标，是设计一个能容纳未来 harness、sandbox 或其他围绕 Claude 的组件的系统。

Managed Agents 是一个「元 harness」：对未来 Claude 需要什么具体 harness 不设限，而是一个拥有通用接口、允许许多不同 harness 的系统。Claude Code 是 Anthropic 广泛使用的优秀 harness；任务专用的 harness 在狭窄领域也表现出色。Managed Agents 可以容纳其中任何一种，随 Claude 的智能一起演进。

元 harness 设计意味着对 Claude 周围的接口有明确主张：Claude 需要操作状态（session）与执行计算（sandbox），也需要扩展到多大脑与多双手。接口被设计成能在长时间跨度内可靠、安全地运行。
