---
title: "Confidential Inference via Trusted Virtual Machines（基于可信虚拟机的机密推理）"
org: "Anthropic"
date: 2025-06-18
source_url: "https://www.anthropic.com/research/confidential-inference-trusted-vms"
tags: ["安全/对齐", "隐私"]
summary: "敏感数据除被处理的一瞬外全程加密。Anthropic 用可信执行环境与 TPM 建立信任链，只有经签名校验的可信 loader 才能解密模型权重与用户数据。"
summary_zh: "敏感数据除被处理的一瞬外全程加密。Anthropic 用可信执行环境与 TPM 建立信任链，只有经签名校验的可信 loader 才能解密模型权重与用户数据。"
summary_en: ""
---

# Confidential Inference via Trusted Virtual Machines（基于可信虚拟机的机密推理）

## 核心目标

每天有数百万用户把敏感信息托付给 Claude——从专有代码到机密商业策略。Anthropic 与 Pattern Labs 合作发布报告，介绍 Confidential Inference（机密推理）：一套处理加密数据、并证明这些数据只能在「可证明自身可信」的服务器内被读取的技术。

采用它的两个主要动机：

- **模型权重安全**：作为保护 Claude 等前沿模型免受高能力攻击者威胁的一环（参考 RAND 关于保护 AI 模型权重的报告）。
- **用户数据安全**：证明敏感用户数据始终私密。

指导原则很简单：**敏感数据在被处理的那一刻之外，都应保持加密；即便是处理时，也只能发生在高度受限、可验证的环境里。**

## 推理服务架构

落地这个原则依赖机密计算：先建立一条证明软件安全的信任链（attestation），再用该证明来限定「哪段软件有权使用解密密钥」。

用户数据在两个位置需要接触明文：

1. **API Server**：处理 prompt、分词、执行 Claude API 请求的大部分逻辑。
2. **Inference Server**：在加速器上运行 Claude 的「大脑」，根据 prompt 生成 completion token。模型权重只交给 Inference Server。

因为并非所有加速器都完整支持机密计算，Anthropic 探索的架构是：Inference Server 大部分运行在「不可信」侧（可频繁变更，且变更不影响整体安全），只保留一个很小的**可信 loader** 运行在由 hypervisor 隔离的独立虚拟机中，向 Inference Server 暴露成一个与模型架构无关的「虚拟加速器」。

loader 只做三件简单的事：接收并解密加密数据后送进加速器；调用加速器并返回加密结果；确保只有自己能访问解密数据。它只接受由安全 CI 服务器签名的程序，从而保证运行的代码经过多位工程师评审。只要 loader 正确运行，无论系统其余部分做什么，机密性要求都能满足——因此「证明 loader 正确运行」至关重要。

## 可信环境的三个特征

报告要求 loader 运行在具备以下能力的机密计算环境中：

- 由硬件与其它工作负载隔离的加密内存；
- 关闭调试功能；
- 能提供密码学证明，证实运行的是正确代码。

其中加密内存可防御部分物理攻击与恶意 hypervisor，但「与加速器共享加密主机内存」所需特性目前尚不成熟，短期内仍需依赖算力供应商在物理数据中心与 hypervisor 层的安全保障。

后两项可通过广泛支持的可信计算实践实现，以 TPM（可信平台模块）为信任根：TPM 度量启动的每个阶段并报告最终哈希，形成 attestation，证明 loader 服务器被正确隔离、运行的是已签名且评审过的代码、且已关闭相关调试功能。密钥服务器（keyserver）校验通过后才会释放解密密钥。

是否「可信」最终由 keyserver 判定。Anthropic 也在探索由其它方验证可信代码、管理独立 keyserver 的模式，以便对每份数据给出更强的机密性保证。

## 一次用户请求的完整流程

1. 请求在到达 Anthropic 服务器之前就被加密；
2. 到达 API Server 后解密、处理，再重新加密后继续传递；
3. Inference Server 以加密形式处理请求，仅在送往可信 loader 时才解密；
4. completion 在离开 loader 前加密，经 API Server 返回调用方。

模型权重更简单：加密存储，在 loader 处解密，且永不离开 loader。

## 局限与未来方向

- 若加速器本身带有硬件信任根，这套系统的信任边界可以显著缩小；硬件设计者应考虑在芯片中内置机密计算能力。
- 随着前沿模型能力增强，可能需要在可信 loader 层叠加更多防护，例如对持有明文模型权重的服务器增加出口带宽限制，或要求推理前出示安全分类器的签名。
- 这项研究仍处早期，官方强调只是勾勒方向以引发讨论，尚不宜预测会演化为哪些具体产品能力。

## 相关概念

- concepts/agentic-systems — 安全边界是部署 Agent 的前提
- entities/anthropic — 报告发布方
