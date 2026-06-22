---
title: "Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 2"
org: "Moonshot AI"
date: 2024-07-02
source_url: "https://platform.kimi.com/blog/posts/enhance-kimi-api-bot-with-context-caching-2"
tags: ["Moonshot AI"]
summary: "Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 2"
summary_zh: "Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 2"
summary_en: ""
---

# Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 2

Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 2
进击的黑咻
,
发表于 2024年07月02日
•
7 min read
agent
development
caching
返回
在
上一个章节
中，我们以 Golang 为例实践了
使用 Context Caching 为 Kimi API 助手（简称小助手）提速
，让我们简单地回顾一下主要内容：

小助手会将所有知识以 system prompt 的形式放置在上下文（Context）中（即
initKnowledge
 函数）；

我们使用 Context Caching 功能，缓存小助手的 system prompt；

我们新增了一个缓存管理模块（以 sqlite 为例），使用业务的 Key 与缓存 cache_id 进行映射，以解决 cache_id 变动的问题；

改造
initKnowledge
 函数，加入查询和新增缓存功能；

改造
CreateChatCompletion
 接口，通过设置 HTTP Headers 以使用缓存；

在实际使用缓存的过程中，我们也陆续收到很多小伙伴的意见和建议，其中最频繁被提到的问题是，使用 HTTP Headers 的方式使用缓存时，仍然需要在 messages 列表中附上完整的缓存 messages，既增加了网络传输的开销，又容易出现因错误操作缓存 messages 导致缓存无法命中的问题，甚至有同学提出，使用 HTTP Headers 的方式调用缓存，本身就非常不直观，在某些场合下并不能“无痛”改造原有业务逻辑，不可避免地会产生 Breaking Change。

因此，我们听取和吸纳了一些小伙伴提出的建议，为 Context Caching 添加了一个语法糖，现在你可以在 messages 列表中的第一位，使用一条
role="cache"
 的 message 来
引用
已被缓存的内容，这条 message 的样子看起来是这样：

{

"role"
:

"cache"
,

"content"
:

"cache_id=cache-xxxxxxxxxxxxxxxxxxxxx;reset_ttl=3600"

}

使用这样的 message 时，你需要遵循以下几个约定：

这条 message 必须放在 messages 列表的第一位；

这条 message 的 role 固定为
cache
；

这条 message 的 content 内容的必填项为
cache_id
，
reset_ttl
 为选填项，他们之间使用分号
;
 分隔；（其中，
cache_id
 对应 HTTP Headers 中的
X-Msh-Context-Cache
，
reset_ttl
 对应 HTTP Headers 中的
X-Msh-Context-Cache-Reset-TTL
）；

这条 message 会被替换成已被缓存的消息内容（包含已被缓存的
tools
），因此你不需要重复添加已被缓存的内容，
并且需要把
tools
 字段置为空值
；

我们会通过实际的例子来讲解如何使用这一项语法糖，并且看看这个语法糖有多甜。

通过设置 Message 的方式调用缓存

我们仍然使用上一章节所使用的
initKnowledge
 函数，以及缓存管理模块
ContextCacheManager
，我们将重点放在如何快速、正确地构造一个
role="cache"
 的 message，并且尽最大可能不产生 Breaking Change。

改造
Content
 结构体

细心的小伙伴们应该会发现，在上一篇中，我们在构造
Message
 结构体时，使用的
Content
 字段并不是
string
 类型，而是使用了一个自定义结构体
Content
，我们先来看看这个结构体的布局：

type

Content

struct
 {

	Text
string

}

func
 (c
*
Content)
MarshalJSON
() ([]
byte
,
error
) {

if
 c
==

nil
 {

return
 json.
Marshal
(
nil
)

	}

return
 json.
Marshal
(c.Text)

}

注：使用
Content
 结构体而非
string
 类型，是因为我们预期
message.content
 的值会有不同的类型，因此预留了这样的结构体以便于后续迭代，目前看来，确实派上用场了。

为了兼容
role="cache"
 的 message，我们会给
Content
 结构体新增一个字段
Cache
，并改写
MarshalJSON
 方法使其能支持特性的 Cache 语法，改造后的
Content
 看起来像这样：

// ContextCacheOptions 是在上一个章节出现过的老朋友了

type

ContextCacheOptions

struct
 {

	CacheID
string

	ResetTTL
int

}

type

Content

struct
 {

	Text
string

	Cache
*
ContextCacheOptions

}

func
 (c
*
Content)
MarshalJSON
() ([]
byte
,
error
) {

if
 c
==

nil
 {

return
 json.
Marshal
(
nil
)

	}

if
 c.Cache
!=

nil
 {

var
 cacheOptionsBuilder strings.Builder

		cacheOptionsBuilder.
WriteString
(
"cache_id="
)

		cacheOptionsBuilder.
WriteString
(c.Cache.CacheID)

if
 resetTTL
:=
 c.Cache.ResetTTL; resetTTL
>

0
 {

			cacheOptionsBuilder.
WriteString
(
";"
)

			cacheOptionsBuilder.
WriteString
(
"reset_ttl="
)

			cacheOptionsBuilder.
WriteString
(strconv.
Itoa
(resetTTL))

		}

return
 json.
Marshal
(cacheOptionsBuilder.
String
())

	}

return
 json.
Marshal
(c.Text)

}

当使用
Content
 结构体时，我们可以任意选择赋值
Text
 字段或
Cache
 字段，二者选其一，当使用
Text
 字段时，它将被序列化为一个普通的
string
 类型的值；而当使用
Cache
 字段时，它将按照约定的格式，将
Cache
 相关信息（包括
cache_id
 和
reset_ttl
）转换为特定的格式，并生成一个满足要求的
string
 类型的值。

使用
Content
 结构体启用缓存

我们仍然会使用
initKnowledge
 函数和
ContextCacheManager
 接口，我们新建一个函数名为
ChatWithCacheByMessage
：

func

chatWithCacheByMessage
(

	ctx context.Context,

	client Client[moonshot],

	cacheManager ContextCacheManager,

) {

	messages, cacheID, err
:=

initKnowledge
(ctx, client, cacheManager)

if
 err
!=

nil
 {

if
 parsed
:=

ParseError
(err); parsed
!=

nil
 {

			log.
Fatalln
(
"("
+
parsed.Type
+
")"
, parsed.Message)

		}

		log.
Fatalln
(err)

	}

// 当缓存存在时，我们直接使用通过 Message 引用缓存内容，通过设置 Message.Content.Cache

// 值的方式传递 cache_id 和 reset_ttl 参数，以此在调用 CreateChatCompletion 接口时开

// 启缓存。

//

// 当缓存不存在时，我们需要从 ContextCacheManager 中取回 Cache 原本的 messages 信息，

// 然后以不启用缓存的形式调用 CreateChatCompletion 接口。

if
 cacheID
!=

""
 {

		messages
=
 []
*
Message{

			{Role: RoleCache, Content:
&
Content{Cache:
&
ContextCacheOptions{CacheID: cacheID, ResetTTL:
3600
}}},

			{Role: RoleUser, Content:
&
Content{Text: input}},

		}

	}
else
 {

		messages
=

append
(messages,
&
Message{

			Role:    RoleUser,

			Content:
&
Content{Text: input},

		})

	}

	stream, err
:=
 client.
CreateChatCompletionStream
(ctx,
&
ChatCompletionStreamRequest{

		Messages: messages,

		Model:    ModelMoonshot128K,

	})

if
 err
!=

nil
 {

if
 parsed
:=

ParseError
(err); parsed
!=

nil
 {

			log.
Fatalln
(
"("
+
parsed.Type
+
")"
, parsed.Message)

		}

		log.
Fatalln
(err)

	}

defer
 stream.
Close
()

for
 chunk
:=

range
 stream.C {

		fmt.
Printf
(
"
%s
"
, chunk.
GetDeltaContent
())

	}

}

注：原
chat
 函数被重命名为
ChatWithCacheByContext
。

通过改造
Message.Content
，我们实现了
引用
已经创建成功的缓存，在减少网络传输开销的同时，我们还避免了代码的 Breaking Change，只需要在生成 messages 列表时，额外在列表首尾置入一个特殊的 message（即
role="cache"
 的 message）即可完成缓存启用操作，同时，在配置缓存时，我们还使用了结构体来规范缓存配置项，
做到代码有补全，阅读能跳转，编译器能检查
三手都要抓，三手都要硬。

相关代码及代码示例中所涉及的 SDK 均可在我们的
Github
 (opens in a new tab)
 中获取。
2025
 © Moonshot AI
用户中心
文档