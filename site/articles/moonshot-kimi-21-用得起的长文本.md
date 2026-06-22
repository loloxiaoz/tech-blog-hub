---
title: "用得起的长文本"
org: "Moonshot AI"
date: 2024-06-19
source_url: "https://platform.kimi.com/blog/posts/introduction-to-context-caching"
tags: ["Moonshot AI"]
summary: "在业务的合适场景中使用 Context Caching，根据您的业务特性，最高可以节省 90% 的调用成本。同时，Context Caching 还能大幅降低 API 的接口响应耗时（或者说首字返回速度）。简单来说，越是规模化、重复度高的 prompt 场景，Context Ca"
summary_zh: "在业务的合适场景中使用 Context Caching，根据您的业务特性，最高可以节省 90% 的调用成本。同时，Context Caching 还能大幅降低 API 的接口响应耗时（或者说首字返回速度）。简单来说，越是规模化、重复度高的 prompt 场景，Context Ca"
summary_en: ""
---

# 用得起的长文本

用得起的长文本
发表于 2024年06月19日
•
4 min read
web
development
返回
大幅降本！响应提速！

在业务的合适场景中使用 Context Caching，根据您的业务特性，最高可以节省 90% 的调用成本。同时，Context Caching 还能大幅降低 API 的接口响应耗时（或者说首字返回速度）。简单来说，越是规模化、重复度高的 prompt 场景，Context Caching 功能带来的收益就越大。

Context Caching 的典型使用场景

Context Caching 特别适合于用
频繁请求，重复引用大量初始上下文
的情况，通过重用已缓存的内容，可以显著提高效率并降低费用。因为这个功能具有强烈的业务属性，我们下面简单列举一些合适的业务场景：

提供大量预设内容的 QA Bot，例如 Kimi API 小助手。

针对固定的文档集合的频繁查询，例如上市公司信息披露问答工具。

对静态代码库或知识库的周期性分析，例如各类 Copilot Agent。

瞬时流量巨大的爆款 AI 应用，例如哄哄模拟器，LLM Riddles。

交互规则复杂的 Agent 类应用，例如什么值得买 Kimi+ 等。

Context Caching 与 RAG 方案的比较

一直以来，长文本大模型虽然效果更好，但是使用成本高是个绕不开的话题。之前业界广泛采用 RAG 方案来进行业务降本，下面我们简单说明加上 Context Caching 功能后的长文本模型与 RAG 方案的区别：

Context Caching

业务成本：与业务特性高度相关，特定场景下成本压缩程度极高，根据我们测算，最高能达到 90% 降本。

研发成本：相对较低，仅需按照接口完成一次性接入，后续无需额外调优，即可完成整体业务的稳定降本。

额外优势：提升长文本场景下的响应速度，对客服等低延迟业务场景有巨大优势。

RAG

业务成本：与业务特性无关，任何业务都可以通过此方案实现降本。但本身因为 RAG 方案的召回精度问题，可能会造成回答准确率的下降。

研发成本：相对较高，需要通过 RAG 与 Embedding 结合，并且不断进行业务定制化的调优，才能实现较好的效果。当业务发生变化时，需要额外的研发调优成本。

额外优势：原始文本长度可以扩展到非常长，对一次性需要几百万字的上下文的场景更友好。

Coming Soon

即将发布 Context Caching 功能的场景最佳实践/计费方案/技术文档，敬请期待。
2025
 © Moonshot AI
用户中心
文档