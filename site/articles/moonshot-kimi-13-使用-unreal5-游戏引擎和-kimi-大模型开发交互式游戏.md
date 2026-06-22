---
title: "使用 Unreal5 游戏引擎和 Kimi 大模型开发交互式游戏"
org: "Moonshot AI"
date: 2024-09-02
source_url: "https://platform.kimi.com/blog/posts/enpower-your-own-ai-agent-inside-unreal5-with-kimi"
tags: ["Moonshot AI"]
summary: "使用 Unreal5 游戏引擎和 Kimi 大模型开发交互式游戏"
summary_zh: "使用 Unreal5 游戏引擎和 Kimi 大模型开发交互式游戏"
summary_en: ""
---

# 使用 Unreal5 游戏引擎和 Kimi 大模型开发交互式游戏

使用 Unreal5 游戏引擎和 Kimi 大模型开发交互式游戏
小岛
,
发表于 2024年09月02日
•
3 min read
agent
gaming
aigc
返回
最近
国产 3A 游戏《黑神话：悟空》在 Steam 上取得了优异的成绩
 (opens in a new tab)
，坊间也带来了一股西游热。而在《黑神话：悟空》成功的背后，不仅依靠着西游这一经典 IP，现代技术对于游戏开发的助力同样功不可没。开发团队巧妙地将现代化的AI技术与中国传统文化相结合，用前沿科技讲述了一个植根于中国文化的经典故事。在游戏的制作过程中，AI 不仅仅是提升游戏体验的工具，更是推动文化创作和创新的重要抓手。

而游戏中的如意卷轴描绘的六丁六甲镇所提供的养成玩法一定也让玩家印象深刻，只可惜这些角色虽然人物特点鲜明，但受限于篇幅可供玩家互动的内容却略显不足。结合 AIGC 技术，我们可以快速扩充这些角色的对白，构建出一个更加生动的西游世界。

包括 Unreal5 在内的众多游戏引擎都使用 cpp 作为自己的底层开发语言，
使用 cpp 版本的 OpenAI SDK
 (opens in a new tab)
 也可以在原生 cpp 的基础上调用 Kimi 大模型生成角色对白与设定。

#include

<iostream>

#include

"openai/openai.hpp"

int

main
() {

    openai
::
start
(

"$YOUR_API_KEY"
,

""
,
 // organization id

true
,
 // throw exception

"https://api.moonshot.cn/v1/"
  // base url

    );

auto
 chat
=
 openai
::
chat
()
.
create
(
R"(

        {

            "model": "moonshot-v1-32k",

            "messages":[{"role":"system", "content":"你是戌狗，是《黑神话：悟空》中六丁六甲中的一员，你擅长炼丹术，会给玩家讲述道家学说，并分享自己炼制的各种丹药。"}, {"role":"user", "content":"讨个丹吃。"}, {"role":"assistant", "role":"戌狗"'}]

        }

    )"
_json
);

    std
::
cout
<<

"Response is:\n"

<<

chat
.
dump
(
2
)
<<

'\n'
;

}

使用 cpp 版本的 OpenAI SDK 库，需要玩家安装 libcurl 库，建议使用 vcpkg，或者也可以使用 Unreal 商店的 ChatGPT 插件进行交互，请参考如何从 OpenAI 迁移一节了解详细。
2025
 © Moonshot AI
用户中心
文档