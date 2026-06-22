---
title: "GSPO: Towards Scalable Reinforcement Learning for Language Models"
org: "阿里巴巴"
date: 2025-07-27
source_url: "https://qwenlm.github.io/blog/gspo/"
tags: ["阿里巴巴"]
summary: "Introduction Reinforcement Learning (RL) has emerged as a pivotal paradigm for scaling language models and enhancing their deep reasoning an"
summary_zh: ""
summary_en: "Introduction Reinforcement Learning (RL) has emerged as a pivotal paradigm for scaling language models and enhancing their deep reasoning and problem-"
---

# GSPO: Towards Scalable Reinforcement Learning for Language Models

PAPER DISCORD
Introduction Reinforcement Learning (RL) has emerged as a pivotal paradigm for scaling language models and enhancing their deep reasoning and problem-solving capabilities. To scale RL, the foremost prerequisite is maintaining stable and robust training dynamics. However, we observe that existing RL algorithms (such as GRPO) exhibit severe instability issues during long training and lead to irreversible model collapse, hindering further performance improvements with increased compute.
To enable successful RL scaling, we propose the Group Sequence Policy Optimization (GSPO) algorithm.