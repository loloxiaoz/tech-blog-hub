---
title: "Kimi 长思考模型 API 正式发布"
org: "Moonshot AI"
date: 2025-05-06
source_url: "https://platform.kimi.com/blog/posts/kimi-thinking"
tags: ["Moonshot AI"]
summary: "模型是月之暗面提供的具有多模态推理能力和通用推理能力的多模态思考模型，它擅长深度推理，帮助解决更多更难的事情，当你遇到难解的代码问题、数学问题、工作问题时，都可以找"
summary_zh: "模型是月之暗面提供的具有多模态推理能力和通用推理能力的多模态思考模型，它擅长深度推理，帮助解决更多更难的事情，当你遇到难解的代码问题、数学问题、工作问题时，都可以找"
summary_en: ""
---

# Kimi 长思考模型 API 正式发布

Kimi 长思考模型 API 正式发布
发表于 2025年05月06日
•
7 min read
product
announcement
返回
kimi-thinking-preview
 模型是月之暗面提供的具有多模态推理能力和通用推理能力的多模态思考模型，它擅长深度推理，帮助解决更多更难的事情，当你遇到难解的代码问题、数学问题、工作问题时，都可以找
kimi-thinking-preview
 模型来帮忙。

使用模型

kimi-thinking-preview
 模型是目前最新的 k 系列思考模型，你可以简单地通过更换 model 来使用它：

$ curl https://api.moonshot.cn/v1/chat/completions \

    -H "Content-Type: application/json" \

    -H "Authorization: Bearer $MOONSHOT_API_KEY" \

    -d '{

        "model": "kimi-thinking-preview",

        "messages": [

            {
"role"
:

"user"
,

"content"
:

"你好"
}

        ]

   }'

{

"id"
:

"chatcmpl-6810567267ee141b4630dccb"
,

"object"
:

"chat.completion"
,

"created"
:

1745901170
,

"model"
:

"kimi-thinking-preview"
,

"choices"
:

    [

        {

"index"
:

0
,

"message"
:

            {

"role"
:

"assistant"
,

"content"
:

"你好！😊 我是Kimi，很兴见到你！有什么可以帮你的吗？"
,

"reasoning_content"
:

"用户说“你好”，这是一句简单的问候语，没有包含复杂的信息或需求。我判断用户可能只是想开启一段对话，或者测试我的反应能力。这种情况下，我的目标是用友好且简洁方式回应，保持对话的轻松氛围，同时为后续可能的交流做好准备。\n\n我决定用“你好！😊 我是Kimi，很高兴见到你！有什么可以帮你的吗？”作为回复。这样既回应了用户的问候，又主动表达了愿意提供帮助的态度，同时通过添加情符号让语气更亲切自然。"

            }
,

"finish_reason"
:

"stop"

        }

    ]
,

"usage"
:

    {

"prompt_tokens"
:

8
,

"completion_tokens"
:

142
,

"total_tokens"
:

150

    }

}

或是通过 openai SDK：

import
 os

import
 openai

client
=
 openai
.
Client
(

    base_url
=
"https://api.moonshot.cn/v1"
,

    api_key
=
os.
getenv
(
"MOONSHOT_API_KEY"
),

)

stream
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
"kimi-thinking-preview"
,

    messages
=
[

        {

"role"
:
"system"
,

"content"
:
"你是 Kimi。"
,

        },

        {

"role"
:
"user"
,

"content"
:
"请解释 1+1=2。"

        },

    ],

    max_tokens
=
1024
*
32
,

    stream
=
True
,

)

thinking
=

False

for
 chunk
in
 stream
:

if
 chunk
.
choices
:

        choice
=
 chunk
.
choices
[
0
]

# 由于 openai SDK 并不支持输出思考过程，也没有表示思考过程内容的字段，因此我们无法直接通过 .reasoning_content 获取自定义的表示 kimi 推理过程的

# reasoning_content 字段，只能通过 hasattr 和 getattr 来间接获取该字段。

#

# 我们先通过 hasattr 判断当前输出内容是否包含 reasoning_content 字段，如果包含，再通过 getattr 取出该字段并打印。

if
 choice
.
delta
and

hasattr
(choice.delta,
"reasoning_content"
):

if

not
 thinking
:

                thinking
=

True

print
(
"=============开始思考============="
)

print
(
getattr
(choice.delta,
"reasoning_content"
), end
=
""
)

if
 choice
.
delta
and
 choice
.
delta
.
content
:

if
 thinking
:

                thinking
=

False

print
(
"\n=============思考结束============="
)

print
(choice.delta.content, end
=
""
)

注意到，在使用
kimi-thinking-preview
 模型时，我们的 API 响应中使用了
reasoning_content
 字段作为模型思考内容的载体，对于
reasoning_content
 字段：

openai SDK 中的 ChoiceDelta 和 ChatCompletionMessage 类型并不提供
reasoning_content
 字段，因此无法直接通过
.reasoning_content
 的方式访问该字段，仅支持通过
hasattr(obj, "reasoning_content")
 来判断是否存在字段，如果存在，则使用
getattr(obj, "reasoning_content")
 获取字段值

如果你使用其他框架或自行通过 HTTP 接口对接，可以直接获取与
content
 字段同级的
reasoning_content
 字段

在流式输出（stream=True）的场合，
reasoning_content
 字段一定会先于
content
 字段出现，你可以在业务代码中通过判断是否出现
content
 字段来识别思考内容（或称推理过程）是否结束

reasoning_content
 中包含的 Tokens 也受
max_tokens
 参数控制，
reasoning_content
 的 Tokens 数加上
content
 的 Tokens 数应小于等于
max_tokens

多轮会话

使用
kimi-thinking-preview
 进行多轮对话时，
思考内容（或称推理过程）不需要放入请求模型的上下文中
。我们通过如下例子说明如何正确使用
kimi-thinking-preview
 进行多轮对话：

import
 os

import
 openai

client
=
 openai
.
Client
(

    base_url
=
"https://api.moonshot.cn/v1"
,

    api_key
=
os.
getenv
(
"MOONSHOT_API_KEY"
),

)

messages
=
 [

{

"role"
:

"system"
,

"content"
:

"你是 Kimi。"
,

},

]

# 第一轮对话

messages
.
append
({

"role"
:
"user"
,

"content"
:
"请解释 1+1=2。"

})

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
"kimi-thinking-preview"
,

    messages
=
messages,

    max_tokens
=
1024

*

32
,

)

# 获取第一轮对话的结果

message
=
 completion
.
choices
[
0
].
message

if

hasattr
(message,
"reasoning_content"
):

print
(
"=============开始第一次思考============="
)

print
(
getattr
(message,
"reasoning_content"
))

print
(
"=============第一次思考结束============="
)

print
(message.content)

# 移除 message 中的 reasoning_content，并将 message 拼接到上下文中

if

hasattr
(message,
"reasoning_content"
):

delattr
(message,
"reasoning_content"
)

messages
.
append
(message)

# 第二轮对话

messages
.
append
({

"role"
:
"user"
,

"content"
:
"我没听懂，再解释一遍。"
,

})

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
"kimi-thinking-preview"
,

    messages
=
messages,

    max_tokens
=
1024

*

32
,

)

# 获取第二轮对话的结果

message
=
 completion
.
choices
[
0
].
message

if

hasattr
(message,
"reasoning_content"
):

print
(
"=============开始第二次思考============="
)

print
(
getattr
(message,
"reasoning_content"
))

print
(
"=============第二次思考结束============="
)

print
(message.content)

注：即使你不小心把
reasoning_content
 字段放入上下文中，也不要过于担忧，
reasoning_content
 的内容不会计入 Tokens 消耗。

模型限制

kimi-thinking-preview
 目前仍处于预览版阶段，仍有如下限制：

不支持工具调用（ToolCalls），联网搜索功能也暂不支持

不支持 JSON Mode（即设置
response_format={"type": "json_object"}
）

不支持 Partial 模式

不支持 Context Caching

注：如果强行对
kimi-thinking-preview
 启用以上特性，模型可能会输出预期之外的内容。

最佳实践

我们会提供一些关于使用
kimi-thinking-preview
 的最佳实践建议，遵循这些最佳实践通常来说能提升模型使用体验：

使用流式输出（stream=True）：
kimi-thinking-preview
 模型的输出内容包含了
reasoning_content
，相比普通模型其输出内容更多，启用流式输出能获得更好的用户体验，同时一定程度避免网络超时问题

建议设置 temperature=0.8，你可以根据实际需求调高或调低 temperature 参数

建议设置 max_tokens>=4096 以避免无法输出完整的
reasoning_content
 和
content

了解更多：
https://platform.moonshot.cn/docs/guide/use-kimi-thinking-preview-model
 (opens in a new tab)
2025
 © Moonshot AI
用户中心
文档