---
title: "Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 3"
org: "Moonshot AI"
date: 2024-07-08
source_url: "https://platform.kimi.com/blog/posts/enhance-kimi-api-bot-with-context-caching-3"
tags: ["Moonshot AI"]
summary: "Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 3"
summary_zh: "Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 3"
summary_en: ""
---

# Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 3

Kimi API 助手的氮气加速装置 —— 以 Golang 为例实践 Context Caching 3
进击的黑咻
,
发表于 2024年07月08日
•
11 min read
agent
development
caching
返回
在我们先前发布的两篇文章中，分别介绍了：

如何使用 HTTP Headers 方式启用 Cache
 (opens in a new tab)

如何使用 role=cache 的 Message 方式启用 Cache
 (opens in a new tab)

同时，经过计算和测试，我们也发现了，当合理使用 Cache 时，最高能为 Kimi API 助手（简称小助手）
节省 90% 的调用成本
 (opens in a new tab)
！这无疑是小助手职业生涯的又一巅峰时刻。然而，由于一些历史原因，小助手的整体架构并不是那么科学和先进，尤其是配合 Context Caching 功能时，总是会出现一些心智负担十分繁重的情况，我们尝试用简单的语言为各位读者描述当前的处境，并介绍我们的解决方案：

小助手的应用架构非常简单，简单到只需要一个
main.go
 文件就能跑起来，甚至在为小助手添加 Context Caching 功能时，我们也只是简单使用了 sqlite 数据库为其保存与 Cache 相关的各种数据。众所周知，sqlite 是一个轻量级数据库，通常情况下我们只能在 sqlite 的宿主机器上访问和修改数据内容，设想一下，假如小助手 Cache 的内容发生了变动或是产生了更新，我们需要为小助手生成一个新的 Cache ，那需要连接到小助手所在的机器上，手动修改 sqlite 数据库中的数据以达到更新 Cache 的目的（具体来说，就是删除数据库中旧的 Cache ，并添加一条新的 Cache ，以便小助手能用新的
cache_id
 发起请求）。这一过程通常需要让小助手暂时停机，等待 Cache 更新完毕后再重新开始服务。

我们希望有一种办法，能在小助手不停机的情况下，在小助手宿主机器以外的地方完成 Cache 的更新。更进一步地说，我们希望使用一个不变的
cache_id
 来启用 Cache，不论怎么修改 Cache，
cache_id
 都不变。

使用 Context Caching Tag

为了达到上述目的，我们引入了 Context Caching 标签系统（Tag），来管理和使用 Cache：

在使用 Context Caching 的过程中，如果想对已 Cache 的内容进行修改（例如有新的知识需要加入的上下文中，或是某些时效性强的数据需要更新），我们推荐的做法是删除原 Cache，再使用更新后的内容创建新 Cache。这一过程会导致 Context Cache 的 ID 发生变化，在实际开发中，可能需要开发者编写一些额外的代码来管理 Cache，例如通过业务上自定义的 key 与 cache_id 进行匹配映射，这无疑会增加开发者在使用 Cache 时的心智负担。

你可以为 Context Cache 打上任意多的标签，并通过在 Message 中指定 tag 名称来使用其对应的 Cache。使用标签的一个好处在于，标签完全由开发者决定，并且不会随着 Cache 变动而发生变化（它的反面，cache_id 是会随着 Cache 变动而发生变化的）。

我们仍然使用具体代码来讲解 Context Caching Tag 的用法。

首先，我们需要改造
Client
 及对应的请求体和响应体

type

Client

interface
 {

// RetrieveContextCacheTag GET {{ $.Client.BaseUrl }}/caching/refs/tags/{{ $.tag }}

// Content-Type: application/json

// Authorization: Bearer {{ $.Client.Key }}

RetrieveContextCacheTag
(ctx context.Context, tag
string
) (
*
ContextCacheTag,
error
)
// <-- 在本次示例中，我们仅使用了 RetrieveContextCacheTag 接口

}

type

CreateContextCacheRequest

struct
 {

	Messages    []
*
Message
`json:"messages"`

	Model
string

`json:"model"`

	Tools       []
*
Tool
`json:"tools"`

	Name
string

`json:"name,omitempty"`

	Description
string

`json:"description,omitempty"`

	Metadata
map
[
string
]
string

`json:"metadata,omitempty"`

	ExpiredAt
int

`json:"expiredAt,omitempty"`

	TTL
int

`json:"ttl,omitempty"`

	Tags        []
string

`json:"tags,omitempty"`

// <-- 我们为 CreateContextCacheRequest 添加了一个额外的 tags 字段，以便于在创建 Cache 时指定 Tag

}

// ContextCacheTag 用于记录 Tag 与 Cache 的映射关系

type

ContextCacheTag

struct
 {

	Tag
string

`json:"tag"`

	CacheID
string

`json:"cache_id"`

}

随后，我们改造
initKnowledge
 函数，添加和 Tag 相关的逻辑：

var
 documents
=
 []
string
{

"kimi-api-doc-001.pdf"
,

"kimi-api-doc-002.pdf"
,

"kimi-api-doc-003.pdf"
,

}

func

initKnowledge
(ctx context.Context, client Client, tag
string
) (err
error
) {

// 通过 RetrieveContextCacheTag 接口，我们检查当前 tag 是否有可用的 Cache，并通过返回结果决定我们是新增 Cache、或是

// 使用 tag 绑定的 Cache。

	_, err
=
 client.
RetrieveContextCacheTag
(ctx, tag)

if
 err
!=

nil
 {

// 通过 error.type 判断 tag 对应的 Cache 是否存在，在 tag 系统的设计中，一个 tag 必须与一个 cache_id 绑定，

// 如果查询不到 tag，意味着我们还没有创建 Cache ，需要初始化 Cache 并与当前 tag 绑定。

//

// 我们将需要 Caching 的文件逐个通过文件抽取接口获得文件内容，然后再组装成 messages 创建 Cache，在创建 Cache

// 时，通过 tags 字段指定 tag。

if
 parsed
:=

ParseError
(err); parsed
!=

nil

&&
 parsed.Type
==

"resource_not_found_error"
 {

// 逐个抽取文件内容，并组装成 messages

			messages
:=

make
([]
*
Message,
0
,
len
(documents))

for
 _, document
:=

range
 documents {

				file, err
:=
 os.
Open
(document)

if
 err
!=

nil
 {

return
 err

				}

				uploadedFile, err
:=
 client.
UploadFile
(ctx,
&
UploadFileRequest{

					File:    file,

					Purpose:
"file-extract"
,

				})

				file.
Close
()

if
 err
!=

nil
 {

return
 err

				}

				fileContent, err
:=
 client.
RetrieveFileContent
(ctx, uploadedFile.ID)

if
 err
!=

nil
 {

return
 err

				}

				messages
=

append
(messages,
&
Message{

					Role:    RoleSystem,

					Content:
&
Content{Text:
string
(fileContent)},

				})

			}

// 使用组装好的 messages 创建缓存，并打上 tag

			_, err
=
 client.
CreateContextCache
(ctx,
&
CreateContextCacheRequest{

				Messages: messages,

				Model:
"moonshot-v1"
,

				TTL:
3600
,

				Tags:     []
string
{tag},

			})

if
 err
!=

nil
 {

return
 err

			}

		}
else
 {

return
 err

		}

	}

// 如果当前 tag 已经绑定 Cache，我们不需要做任何额外操作，直接使用这个 tag 即可（返回 nil error）

return

nil

}

可以明显看出，这个版本的
initKnowledge
 比上一章节中的同名函数要简洁许多，甚至
ContextCacheManager
 也被优化掉了。我们回忆一下，我们最初建立
ContextCacheManager
 的目的是什么：

使用 ContextCacheManager Key 的意义在于，删除或重新创建缓存，会导致缓存 cache_id 发生变化，因此我们使用一个业务的 Key 来绑定 Kimi 大模型创建的 cache_id。

当我们使用 Context Cache Tag 时，这个 tag 充当了我们用来绑定
cache_id
 的业务 Key，因此我们不再需要手动维护和管理 Context Cache 和业务 Key 的关系，这一切都由 tag 代劳。同样的，我们在使用缓存时，也可以通过
tag
 指定缓存，而不需要再使用会变化的
cache_id
：

// ContextCacheOptions 依然是在上一个章节就出现过的老朋友了

type

ContextCacheOptions

struct
 {

	CacheID
string

	Tag
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

if
 tag
:=
 c.Cache.Tag; tag
!=

""
 {

			cacheOptionsBuilder.
WriteString
(
"tag="
)

			cacheOptionsBuilder.
WriteString
(c.Cache.Tag)

		}
else
 {

			cacheOptionsBuilder.
WriteString
(
"cache_id="
)

			cacheOptionsBuilder.
WriteString
(c.Cache.CacheID)

		}

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

func

chatWithCacheByMessage
(

	ctx context.Context,

	client Client[moonshot],

	tag
string
,

) {

if
 err
:=

initKnowledge
(ctx, client, tag); err
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

	messages
=
 []
*
Message{

		{Role: RoleCache, Content:
&
Content{Cache:
&
ContextCacheOptions{Tag: tag, ResetTTL:
3600
}}},

		{Role: RoleUser, Content:
&
Content{Text: input}},

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

在完成了上述代码改造后，我们的小助手现在可以通过我们预设的
tag
 来启用 tag 对应的 Cache，假如现在我需要对 Cache 内容做修改，我只需要：

使用小助手的
tag
 查询对应的
cache_id
；

删除
cache_id
 对应的 Cache；

使用新的知识创建一个新的 Cache，并为其打上与步骤一相同的
tag
；

在这个过程中，小助手的主程序完全不需要停机或重启；

将上述步骤打包成一个单独的函数：

func

updateKnowledge
(ctx context.Context, client Client[moonshot], tag
string
) (err
error
) {

// 步骤一：使用小助手的 tag 查询对应的 cache_id

	cacheTag, err
:=
 client.
RetrieveContextCacheTag
(ctx, tag)

// 额外的，我们会忽略在查询 tag 过程中产生的错误，我们简单地认为，不管遇到什么错误，

// 我们都默认需要重新创建 Cache。

if
 err
==

nil

&&
 cacheTag
!=

nil
 {

// 步骤二：删除 cache_id 对应的 Cache

if
 err
=
 client.
DeleteContextCache
(ctx, cacheTag.CacheID); err
!=

nil
 {

return
 err

		}

	}

// 步骤三：使用新的知识创建一个新的 Cache，并为其打上与步骤一相同的 tag

return

initKnowledge
(ctx, client, tag)

}

这个函数可以放置在与小助手主程序隔离的其他机器上执行，并且可以通过定时任务设计为每天或每周执行一次，且不会对小助手主程序造成影响。
2025
 © Moonshot AI
用户中心
文档