---
title: "mimalloc: A new, high-performance, scalable memory allocator for the modern era"
org: "Microsoft"
date: 2026-05-13
source_url: "https://www.microsoft.com/en-us/research/blog/mimalloc-a-high-performance-scalable-memory-allocator-for-the-modern-era/"
tags: ["Microsoft"]
summary: "mimalloc is an open-source, modern, scalable memory allocator that is a drop-in replacement for malloc and free. It is relatively small (~12"
summary_zh: ""
summary_en: "mimalloc is an open-source, modern, scalable memory allocator that is a drop-in replacement for malloc and free. It is relatively small (~12K lines), "
---

# mimalloc: A new, high-performance, scalable memory allocator for the modern era

mimalloc is an open-source, modern, scalable memory allocator that is a drop-in replacement for malloc and free. It is relatively small (~12K lines), with clear internal data structures, and is easy to build and integrate into other projects. It provides bounded worst-case allocation times (up to OS primitives), bounded space overhead, low internal fragmentation, and minimal contention by relying almost exclusively on atomic operations.

The post
mimalloc: A new, high-performance, scalable memory allocator for the modern era
 appeared first on
Microsoft Research
.