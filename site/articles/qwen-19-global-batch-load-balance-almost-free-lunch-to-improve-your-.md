---
title: "Global-batch load balance almost free lunch to improve your MoE LLM training"
org: "阿里巴巴"
date: 2025-01-21
source_url: "https://qwenlm.github.io/blog/global-load-balance/"
tags: ["阿里巴巴"]
summary: "Background The Mixture-of-Experts (MoEs) architecture has become a popular model-parameter-scale-up technique. Typically, one MoE layer cons"
summary_zh: ""
summary_en: "Background The Mixture-of-Experts (MoEs) architecture has become a popular model-parameter-scale-up technique. Typically, one MoE layer consists of a "
---

# Global-batch load balance almost free lunch to improve your MoE LLM training

GITHUB HUGGING FACE MODELSCOPE DISCORD
Background The Mixture-of-Experts (MoEs) architecture has become a popular model-parameter-scale-up technique. Typically, one MoE layer consists of a router (often parameterized as one single Linear layer) and a group of experts (for transformer-based models, each expert is one feedforward layer). Given an input, only a subset of experts will be activated, and then their outputs will be aggregated based on the scores the router assigned.