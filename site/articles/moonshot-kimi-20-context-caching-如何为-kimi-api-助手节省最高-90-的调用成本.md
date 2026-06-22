---
title: "Context Caching 如何为 Kimi API 助手节省最高 90% 的调用成本"
org: "Moonshot AI"
date: 2024-07-01
source_url: "https://platform.kimi.com/blog/posts/how-to-save-90-percent-with-context-caching"
tags: ["Moonshot AI"]
summary: "Context Caching 如何为 Kimi API 助手节省最高 90% 的调用成本"
summary_zh: "Context Caching 如何为 Kimi API 助手节省最高 90% 的调用成本"
summary_en: ""
---

# Context Caching 如何为 Kimi API 助手节省最高 90% 的调用成本

Context Caching 如何为 Kimi API 助手节省最高 90% 的调用成本
进击的黑咻
,
发表于 2024年07月01日
•
7 min read
agent
development
caching
返回
Kimi API 助手（简称小助手）的实现原理并不复杂，我们把所有和 API 相关的接口文档、使用案例、博客文章和具体代码以 system prompt 的形式加入到 messages 中，作为 Kimi 大模型的参考知识，以此来回答开发者用户们的提问。随着 API 不断丰富、博客文章的不断增多、demo 代码的不断迭代，截至今天（2024 年 7月 1 日），小助手的知识总量已经超过五万字，折算成 Tokens 数量达到 35k，按照目前官网对于
moonshot-v1-128k
 模型的定价，每次请求都会至少消耗
35,000 × 60 ÷ 1,000,000 ＝ 2.1
 元余额。

在小助手使用的高峰期，每小时的问答轮数超过 100 次（含微信群小助手和网页端 Kimi+ 小助手），按照上述计算的价格，高峰期每小时的使用成本为
2.1 × 100 ＝ 210
 元；每日总调用轮数约为 300 次，日调用成本为
2.1 × 300 ＝ 630
 元。积少成多，随着开发者数量的不断增多，API 功能的不断丰富，这个数量还会持续上升。

使用 Context Caching 为小助手降本

Context Caching 的收费规则为：

创建 Cache 时，按 Tokens 数量收取一次性费用，当前的收费标准为 ￥24/M Tokens；

Cache 生效期间，按 Cache 生效时长和 Tokens 数收取存储费用，当前的收费标准为 ￥10/M Tokens/Minute；

每次调用 Cache 时，收取固定费用 0.02 元；

通过阅读收费标准，我们可以发现，要实现降本，我们必须找到 Cache 存储费用、调用次数及普通 Tokens 消耗的平衡点，我们将场景简化为，一小时内，每次调用消耗 35k Tokens，总调用次数为 x，使用方程表示为：

10 × ( 35,000 ÷ 1,000,000 ) × 60 ＋ 24 × ( 35,000 ÷ 1,000,000 ) ＋ 0.02 × x ＝ 60 × ( 35,000 ÷ 1,000,000 ) × x

我们将上述等式转换为函数
y ＝ 60 × ( 35,000 ÷ 1,000,000 ) × x － ( 10 × ( 35,000 ÷ 1,000,000 ) × 60 ＋ 24 × ( 35,000 ÷ 1,000,000 ) ＋ 0.02 × x )
，并绘制函数图像：

从函数图像可得，当每小时的请求数达到 11（原值为 10.5，取整后为 11）时，函数值 y 大于 0，即使用 Context Cache 的费用将会比不使用 Cache 所消耗的费用更低。而在请求高峰期，小助手的对话轮次远超 11 次，高达 100 次，在不使用 Context Cache 的场合，需要消耗 210 元，而当应用了 Cache 后，每小时的消耗额则变成 23.84 元，降本幅度高达
( 210 － 23.84 ) ÷ 210 ＝ 88.65%
，效果显著！

根据流量分布制定 Cache 启停策略

虽然在流量高峰期，我们成功使用 Context Caching 技术为小助手节省了（四舍五入）90% 的费用消耗，然而，由于 Cache 会根据其有效期收取存储费用，因此，我们需要额外地考虑：
当每小时请求数不足 11 次时，应该暂停使用 Cache 以避免额外的存储费用消耗
。

我们绘制出每日不同时间段的平均请求数量折线图，如下图所示：

可以发现，用户询问小助手的高峰时间点集中在上午 9 点至夜间 24 点前，这个时间段每个小时的用户请求数量都超过了“降本临界值”，即 11 次每小时，因此我们考虑在上午 9 点开启 Cache ，并在夜间 24 点结束 Cache （
0 点到 1 点的请求数量虽然超过了 11 次，但由于过于接近临界值，且这是平均水平，实际情况会有浮动，因此我们放弃在此时间段开启 Cache
），达到
在高峰期使用 Cache 降本，在低谷期结束 Cache 节流
的目的。

具体的做法，需要我们在代码中做一些小调整，具体的步骤如下：

在上午 9 点时，我们需要在调用
/chat/completions
 接口时，在 Headers 中添加
X-Msh-Context-Cache
 以启用 Cache ，同时添加
X-Msh-Context-Cache-Reset-TTL
 Header 以更新 Cache 存活期，这里以小助手为例，存活期为 3600s，即 1 小时；

由于我们要在凌晨 0 点结束 Cache ，因此夜间 23 点是我们最后一次刷新 Cache 存活期的时点，在此之后，我们需要移除 Headers 中的
X-Msh-Context-Cache-Reset-TTL
 参数，以保证 Cache 能在 0 点被顺利移除；

以 Python 代码为例，大致的代码逻辑为：

if
 current_time
.
hour
>=

9

and
 current_time
.
hour
<

23
:

	completion
=
 client
.
chat
.
completion
.
create
(

		model
=
"moonshot-v1-128k"
,

		messages
=
messages,

		extra_headers
=
{

"X-Msh-Context-Cache"
:
"cache_id"
,

"X-Msh-Context-Cache-Reset-TTL"
:
"3600"
,

	    },

	)

else
:

	completion
=
 client
.
chat
.
completion
.
create
(

		model
=
"moonshot-v1-128k"
,

		messages
=
messages,

	)

按照这种方式，我们可以计算出，一整天的降本成果：

每次请求 Tokens：35,000；

每次请求价格：2.1 元；

存储时长：上午 9 点至夜间 24 点，共 15 小时；

存储消耗：
10 × ( 35,000 ÷ 1,000,000 ) × 60 × 15 ＋ 24 × ( 35,000 ÷ 1,000,000 ) ＝ 315.84
 元；

总调用次数：639 次；

调用消耗：
0.02 × 639 = 12.78
 元；

不使用 Cache 时的请求消耗：
639 × 2.1 ＝ 1,341.9
 元；

最终的降本幅度为
( 1,341.9 - ( 315.84 + 12.78 ) ) ÷ 1,341.9 ＝ 75.51%
，也就是说，在合理使用 Cache 的场合，每天能节省
四分之三
的费用消耗。
2025
 © Moonshot AI
用户中心
文档