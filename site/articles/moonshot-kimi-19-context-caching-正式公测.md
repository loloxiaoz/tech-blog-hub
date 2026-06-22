---
title: "Context Caching 正式公测"
org: "Moonshot AI"
date: 2024-07-01
source_url: "https://platform.kimi.com/blog/posts/context-caching"
tags: ["Moonshot AI"]
summary: "Context Caching （上下文缓存）是一种高效的数据管理技术，它允许系统预先存储那些可能会被频繁请求的大量数据或信息。这样，当您再次请求相同信息时，系统可以直接从缓存中快速提供，而无需重新计算或从原始数据源中检索，从而节省时间和资源。"
summary_zh: "Context Caching （上下文缓存）是一种高效的数据管理技术，它允许系统预先存储那些可能会被频繁请求的大量数据或信息。这样，当您再次请求相同信息时，系统可以直接从缓存中快速提供，而无需重新计算或从原始数据源中检索，从而节省时间和资源。"
summary_en: ""
---

# Context Caching 正式公测

Context Caching 正式公测
发表于 2024年07月01日
•
10 min read
product
announcement
返回
Context Caching 正式开启公测，快来体验吧！

Context Caching 功能介绍

Context Caching （上下文缓存）是一种高效的数据管理技术，它允许系统预先存储那些可能会被频繁请求的大量数据或信息。这样，当您再次请求相同信息时，系统可以直接从缓存中快速提供，而无需重新计算或从原始数据源中检索，从而节省时间和资源。

应用效果

Context Caching 特别适合用于
频繁请求
，重复引用
大量初始上下文
的场景，可以显著
提高效率
并
降低费用
！

费用最高降低 90%

场景举例：需要对固定文档大量提问的场景

某硬件产品说明书大概 9万字，换算 Tokens 长度大概 64K，该产品售前支持人员需要在 10 分钟内，密集对产品的功能/使用方式进行 40 次问答，每次的问题大概 100 个字，要求模型的输出需要基于产品说明书来回答，回答问题在 120 字以内。

原始花费：按照大模型问答的 Tokens 计算逻辑，售前支持人员需要每次向模型输入的 Tokens =文档 Tokens +问题 Tokens，10 分钟内 40 次的问答共计需要消耗 Tokens 2.56 M，128k 模型价格为 60元/M，预计需花费 153.84 元。

若该场景接入 Context Caching：9万字的文档只收取一次创建 Cache 和存储 10 分钟 Cache 的费用，10分钟内的40次提问，将只收取问题的 100 字+ 回答的 120 字的费用，预计花费 11.88 元，
预计节省
141.95
元，费用降低
92.27%

首 Token 延迟降低 83%

以 128k 模型的一次 4w 字（30k tokens）的推理请求为例，通常向模型提问，平均要 30s 返回首 Token。接入 Context Caching 后，如下图，最快可 1s 内完成首 Token 返回。
经过大量测试，接入 Context Caching（上下文缓存）功能，128K 的请求，首 Token 延迟平均可降至
5s
 内，首 Token 延迟降低
83%
 左右！

以上应用效果，基于 1 token = 1～1.5个文字和字符，128k 模型进行测算。具体的效果根据您的业务情况/模型选择不同，会有略微的差别。

快速开始

使用 Context Caching 时，您首先需要通过 API 创建缓存，指定要存储的数据类型和内容，然后设置一个合适的过期时间以保持数据的时效性。一旦缓存创建完成，任何对该数据的请求都会首先检查缓存，如果缓存有效，就直接使用，否则需要重新生成并更新缓存。这种方法特别适用于需要处理大量重复请求的应用程序，可以显著提高响应速度和系统性能。以下示例分创建 Cache 和使用 Cache 两个步骤来介绍

创建 Cache

from
 openai
import
 OpenAI

import
 requests

import
 json

client
=

OpenAI
(

    api_key
=

"$MOONSHOT_API_KEY"
,

    base_url
=

"https://api.moonshot.cn/v1"
,

)

res
=
 requests
.
post
(

    url
=

"https://api.moonshot.cn/v1/caching"
,

    headers
=
 {

"Authorization"
:
"Bearer $MOONSHOT_API_KEY"

    },

    json
=
 {

"model"
:
"moonshot-v1"
,

"messages"
: [

            {

"role"
:
"system"
,

"content"
:
"你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"

            },

        ],

"tools"
: [{

"type"
:
"function"
,

"function"
: {

"name"
:
"CodeRunner"
,

"description"
:
"代码执行器，支持运行 python 和 javascript 代码"
,

"parameters"
: {

"properties"
: {

"language"
: {

"type"
:
"string"
,

"enum"
: [
"python"
,
"javascript"
]

                        },

"code"
: {

"type"
:
"string"
,

"description"
:
"代码写在这里"

                        }

                    },

"type"
:
"object"

                }

            }

        }],

"name"
:
"CodeRunner"
,

"ttl"
:
3600

    }

)

print
(json.
loads
(res.text))

运行上述代码，返回：

{
'id'
:

'cache-essqmysd6h1111dauub1'
,

'object'
:

'context_cache_object'
,

'model'
:

'moonshot-v1'
,

'messages'
:
 [
{
'role'
:

'system'
,

'content'
:

'你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。'
}
]
,

'tools'
:
 [
{
'function'
:

{
'name'
:

'CodeRunner'
,

'description'
:

'代码执行器，支持运行 python 和 javascript 代码'
,

'parameters'
:

{
'properties'
:

{
'code'
:

{
'description'
:

'代码写在这里'
,

'type'
:

'string'
},

'language'
:

{
'enum'
:
 [
'python'
,

'javascript'
]
,

'type'
:

'string'
}},

'type'
:

'object'
}},

'type'
:

'function'
}
]
,

'name'
:

'CodeRunner'
,

'description'
:

''
,

'metadata'
:

None
,

'expired_at'
:

1718847499
,

'status'
:

'pending'
,

'tokens'
:

72
}

使用 Cache

你可以直接使用
role="cache"
来引用一段已经创建好的 cache，需要注意的是当 cache 处在非
active
状态下时， 默认情况下调用依然会成功，但此时并不会触发对应的优化，如希望避免这种情况，可以在参数列表中设置
dry_run=1
。

from
 openai
import
 OpenAI

client
=

OpenAI
(

    api_key
=

"$MOONSHOT_API_KEY"
,

    base_url
=

"https://api.moonshot.cn/v1"
,

)

completion
=
 client
.
chat
.
completions
.
create
(

    model
=
"moonshot-v1-8k"
,

    messages
=
[

        {

"role"
:
"cache"
,

"content"
:
"cache_id=cache-essqmysd6h1111dauub1;reset_ttl=3600"
,

        },

        {

"role"
:
"user"
,

"content"
:
"编程判断 3214567 是否是素数。"
,

        },

    ],

    temperature
=
0.3
,

)

print
(completion.choices[
0
].message)

运行上述代码，返回：

ChatCompletionMessage(content='判断一个数是否是素数，我们可以使用一个简单的算法：检查从2到该数的平方根之间的所有整数是否能整除该数。如果有一个能整除，那么这个数就不是素数。如果没有任何数能整除它，那么它就是素数。\n\n对于给定的数3214567，我们可以编写一个程序来实现这个算法。下面是一个使用Python语言的示例代码：\n\n```python\nimport math\n\ndef is_prime(number):\n    if number <= 1:\n        return False\n    for i in range(2, int(math.sqrt(number)) + 1):\n        if number % i == 0:\n            return False\n    return True\n\nnumber_to_check = 3214567\nprint(is_prime(number_to_check))\n```\n\n这段代码定义了一个函数`is_prime`，它接受一个整数作为参数，并返回一个布尔值，表示这个数是否是素数。然后，我们使用这个函数来检查3214567是否是素数。', role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='CodeRunner:0', function=Function(arguments='{\n    "code": "import math\\n\\ndef is_prime(number):\\n    if number <= 1:\\n        return False\\n    for i in range(2, int(math.sqrt(number)) + 1):\\n        if number % i == 0:\\n            return False\\n    return True\\n\\nnumber_to_check = 3214567\\nis_prime(number_to_check)"\n}', name='CodeRunner'), type='function', index=0)])

以上是 python 示例，其他代码示例请见：
上下文缓存接入指南
 (opens in a new tab)

计费说明

Context Caching 的收费模式主要分为以下三个部分：

Cache 创建费用：

调用 Cache 创建接口，成功创建 Cache 后，按照 Cache 中 Tokens 按实际量计费。24元/M token

Cache 存储费用

Cache 存活时间内，按分钟收取 Cache 存储费用。10元/M token/分钟

Cache 调用费用

Cache 调用增量 token 的收费：按模型原价收费

Cache 调用次数收费：Cache 存活时间内，用户通过 chat 接口请求已创建成功的 Cache，若 chat message 内容与存活中的 Cache 匹配成功，将按调用次数收取 Cache 调用费用。0.02 元/次

详细计费项说明请见：
定价与计费
 (opens in a new tab)

接入参考示例

Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching
 (opens in a new tab)

公测时间和资格说明

公测时间：功能上线后，公测3个月，公测期价格可能随时调整。

公测资格：公测期间 Context Caching 功能仅开放给 Tier5 等级用户，用户范围放开时间，敬请期待。

问题反馈

欢迎扫码添加客服，和我们分享您的业务场景，期待您的反馈。

欢迎关注 Kimi 开放平台，关注我们最新产品动态。

2025
 © Moonshot AI
用户中心
文档