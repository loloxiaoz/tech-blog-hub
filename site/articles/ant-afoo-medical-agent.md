---
title: "蚂蚁阿福：从 0 到生产的医疗 Agent 工程化落地"
org: "行业实践"
date: 2026-05-11
source_url: ""
tags: ["Agent", "Eval/评测", "RAG/检索"]
summary: "1. EBDD（Evaluation and Badcase Driven Development） 是医疗 Agent 的核心研发范式"
summary_zh: ""
summary_en: "1. EBDD（Evaluation and Badcase Driven Development） 是医疗 Agent 的核心研发范式"
---



# 蚂蚁阿福：从 0 到生产的医疗 Agent 工程化落地

**演讲者**：郭春晓，蚂蚁集团医疗工程引擎  
**会议**：QCon 全球软件开发大会，2026年  
**核心主张**：AI Agent 正在重新定义医疗健康

---

## 核心观点

1. **EBDD（Evaluation and Badcase Driven Development）** 是医疗 Agent 的核心研发范式
2. 医疗 Agent 有四大特殊挑战：专业性/非确定性/长期记忆缺失/风控合规
3. 主子 Agent 架构使深度检索准确率提升 **19%**
4. AQ 问答准确率业界对抗第一（MedResearcher-R1-32B：27.5），BRIGHT benchmark SOTA
5. 医疗记忆是四层架构，难点在多身份管理和长期记忆遗忘策略

---

## EBDD：评测驱动研发范式

**EBDD = Evaluation → Badcase → Driven → Development**

传统开发流程：评测耗时 1-2 天，反馈慢，优化迭代慢。  
EBDD 流程：评测耗时**小时级**，快速定位 Badcase，针对性改进。

**可靠评测三要素**：
1. 稳定数据集（避免分布漂移）
2. 足够样本量（统计置信度）
3. 可信评审者（LLM-as-Judge + 专家校验）

---

## 医疗四大核心挑战

| 挑战 | 描述 |
|------|------|
| **专业性要求极高** | 需引用权威医学指南，不能凭 LLM 通用知识回答 |
| **非确定性** | 同一症状多种可能诊断，需循证支持 |
| **长期记忆缺失** | 患者多次就诊，历史病史需跨会话保持 |
| **风控合规** | 医疗建议有法律风险，需人工审批节点 |

---

## 整体技术架构

```
数据层
├── 权威库（医学指南/药品说明书/医保政策）
├── 标准库（ICD编码/药品标准）
└── post-train 数据（医疗对话/问诊样本）
    ↓
AI infra + 模型层
    ↓
Agent 层
├── Agent-RAG（Agentic 循证检索）
├── Agent-Mem（分层记忆系统）
├── Agent 迭代范式（EBDD）
└── 智能体协作（主子 Agent）
    ↓
应用层（问诊/健康管理/药物咨询等）
```

---

## Agentic RAG 三阶段

医疗场景的 RAG 不是简单向量检索，而是三阶段 Agent 驱动的循证检索：

```
Stage 1: Query 理解
  — 意图识别、医学实体抽取、查询改写
  ↓
Stage 2: 循证检索
  — 权威指南检索 + 药品说明书检索 + 医保政策检索
  — 多源融合、交叉验证
  ↓
Stage 3: 证据融合
  — 多文档摘要聚合、置信度评估、引用标注
```

**主子 Agent 升级效果**：深度检索准确率提升 **19%**

---

## 医疗上下文四大挑战

| 挑战 | 解决方案 |
|------|---------|
| 信息密度高（病历/检验报告密集） | 关键信息结构化抽取 |
| 多轮对话依赖（问诊需跨轮连贯） | 会话记忆 + 渐进式摘要 |
| 上下文窗口有限 | 上下文压缩 + 选择性传递 |
| 跨 Agent 共享（主子 Agent 传递上下文） | 分层记忆 + 结构化接口 |

---

## 医疗记忆四层架构

### Layer 1：输入与身份识别层（难点：多身份）
- 身份识别引擎：意图 + 角色 + 权限
- 患者本人 vs 家属/代理人 → 独立记忆空间 + 差异化权限边界 + 隐私隔离

### Layer 2：记忆处理层
```
记忆提取(LLM，结构化医疗事实抽取)
  → 冲突检测（新旧记忆矛盾识别）
  → 重置度评估（医疗事实可信度打分）
  → 高置信度 → 入库
  → 低置信度 → 确认 → 人工确认（关键事实复核）
```

### Layer 3：记忆存储层（难点：长期记忆 + 记忆遗忘）
| 类型 | 内容 | 存储 |
|------|------|------|
| 会话记忆（Session） | 当前症状、意图、推理中间状态 | 向量数据库，会话结束自动清除 |
| 病例级记忆（Case） | 诊断结论、治疗方案、用药检验结果 | 图数据库，结构关联存储 |
| 长期记忆（Profile） | 慢性病史、过敏史、家族病史、用药偏好 | 结构化存储，持久化主动管理 |

**遗忘策略引擎**：
- TTL 衰减：短期记忆到时自动过期
- 合规删除：用户撤回 / GDPR / 医疗法规
- 置信度淘汰：低置信度记忆定期清理
- 合并去重 & 主动修正：矛盾记忆合并，错误记忆纠正

### Layer 4：检索与应用层
```
语义检索（向量相似度匹配）
  → 身份权限过滤（按身份角色可见范围）
  → 时效性排序（近期优先 + 衰减加权）
  → 上下文装载（动态 Context Packing）
  → Agent 响应生成（Grounded + 个性化）
```

---

## 训推优化

### 推理加速
**TTFT（首Token时间）优化**：
- Prompt 缓存：复用高频 Prompt 的 KV Cache
- Prefill 优化：分离 Prefill 与 Decode 阶段
- 模型量化：FP8/INT8 降低计算开销
- 业务隔离：长短分离

**TPOT（每Token时间）优化**：
- Continuous Batching：动态批处理请求
- Speculative Decoding：小模型预测 + 大模型验证
- 长短分离

### Agent RL 性能优化
**训练架构挑战**：1T 模型单 step 43 分钟（Rollout 1200s / Reward 600s / Reshard 800s）

**优化成果**：
| 措施 | 效果 |
|------|------|
| 升级 Agent 训练架构（解耦运行/训练环境） | 基础改善 |
| FP8 量化加速 | Rollout 1200s → 1080s |
| 半异步化训练 | 进一步降至 960s |
| Reward Service 升级 | 600s → 120s |
| 社区代码优化 | Reshard 800s → 48s |

**行业首创**：全球首个支持开源 FP8 训推方案 + 全球首个支持开源 QAT 训练方案

---

## 效果数据

- AQ 问答准确率：业界对抗**第一**（MedResearcher-R1-32B：27.5 分）
- BRIGHT benchmark：**SOTA**
- 主子 Agent 架构：深度检索准确率提升 **19%**
- EBDD 流程：评测耗时从 1-2 天降至**小时级**

---

## 关键术语

- **EBDD**：Evaluation and Badcase Driven Development，评测驱动开发
- **Agentic RAG**：Agent 驱动的多阶段循证检索
- **Context Packing**：动态上下文装载，将记忆按需组装注入
- **遗忘策略引擎**：TTL衰减/合规删除/置信度淘汰/合并去重四类遗忘策略

---

## 相关概念

- concepts/agentic-retrieval — Agentic RAG 的理论框架
- concepts/memory-systems — Agent 记忆系统全景（医疗四层架构是典型实现）
- concepts/agent-evaluation — EBDD 是评测驱动研发的典型案例
- concepts/context-window — 医疗场景的上下文挑战与解决方案
- concepts/rag-evaluation — RAG 评测体系
