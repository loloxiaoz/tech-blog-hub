# AI 大厂技术博客来源指南

本文件是 `blogs.json` 的人类可读详解版，按**国外 / 国内**分组，给出每个来源的索引页、渲染方式、URL 模式与抓取建议。机器可读的注册表见 `../blogs.json`。

> ⚠️ 站点会改版，URL 与渲染方式可能变化。**使用前请现场用 WebFetch/WebSearch 校验**，发现变化后回写到 `blogs.json`。

## 抓取策略速查

| 策略（render） | 含义 | 操作 |
|---------------|------|------|
| `static` | 索引页服务端渲染 | 单次 WebFetch 索引页提取列表 → 逐篇 WebFetch 正文 |
| `rss` | 有 RSS/Atom feed | 优先 WebFetch feed（结构稳、含摘要/全文）→ 补抓正文 |
| `js` | 索引页客户端渲染 | WebFetch 常拿不全；先 WebSearch（`site:` 限定域名）发现 URL → 逐篇 WebFetch |
| `github` | 无传统博客 | 正文多在 GitHub README/Release/技术报告 PDF、HuggingFace 模型卡、arXiv |
| `arxiv` | 论文为主 | WebSearch(`arxiv.org <机构名> <模型名> 2026`) 找论文 → WebFetch 摘要页 |

通用 WebFetch 提示词：

```
列出本页所有文章的标题、完整 URL 和发布日期，按时间倒序，不要遗漏。
```
```
提取完整文章内容：标题、作者、日期、所有章节与各级小标题、正文、关键数据、代码块与表格。
```

---

# 国外（International）

## Anthropic
- **工程博客**：`https://www.anthropic.com/engineering` — `static`，约 25 篇，时间倒序，单次 WebFetch 即可拿全。
- **研究/新闻**：`https://www.anthropic.com/research`、`/news` — `static`。
- **文章 URL**：`/engineering/{slug}`、`/research/{slug}`。
- 主题：智能体、评估、MCP、Claude Code、可解释性、对齐、经济影响。

## OpenAI
- **索引**：`https://openai.com/news/` — `js`（客户端渲染）。
- **文章 URL**：研究/公告多为 `/index/{slug}/`，旧研究为 `/research/{slug}`。
- 抓取：WebFetch 索引常拿不全，优先 `WebSearch("site:openai.com/index <关键词> 2026")` 发现 URL，再逐篇 WebFetch。

## Google DeepMind
- **索引**：`https://deepmind.google/discover/blog/` — `js`，带主题筛选。
- **文章 URL**：`/discover/blog/{slug}/`。
- 主题：Gemini、科学（AlphaFold 系）、强化学习、智能体。

## Google Research
- **索引**：`https://research.google/blog/` — `js`。
- **文章 URL**：`/blog/{slug}/`。与 DeepMind 互补，偏系统/ML 工程。

## Meta AI（FAIR）
- **索引**：`https://ai.meta.com/blog/` — `js`。
- **文章 URL**：`/blog/{slug}/`；论文见 `ai.meta.com/research`。
- 主题：Llama 系列、开源、视觉、FAIR 研究。

## Microsoft Research
- **索引**：`https://www.microsoft.com/en-us/research/blog/` — `rss`。
- **RSS**：`https://www.microsoft.com/en-us/research/feed/`（优先用）。
- 主题：Phi 系列、系统、智能体、理论。

## Mistral AI
- **索引**：`https://mistral.ai/news/` — `js`。
- **文章 URL**：`/news/{slug}`。欧洲开源权重代表。

## Hugging Face
- **索引**：`https://huggingface.co/blog` — `static`，另有 `huggingface.co/blog/feed.xml`。
- **文章 URL**：`/blog/{slug}`。官方 + 社区博客，实操教程多（微调、量化、部署）。

## NVIDIA Technical Blog
- **索引**：`https://developer.nvidia.com/blog/` — `rss`：`https://developer.nvidia.com/blog/feed/`。
- 主题：CUDA、推理优化、TensorRT、训练加速。偏工程落地。

---

# 国内（China）

> 国内厂商的共同点：**官方"博客"常是微信公众号或 JS 渲染的产品页**，不利于直接抓取。最稳定的技术来源往往是 **GitHub 仓库（README / Release / 技术报告 PDF）、HuggingFace/ModelScope 模型卡、arXiv 论文**。下表给出每家"最易抓"的入口。

## 阿里通义千问 Qwen ⭐（国内最规范）
- **博客**：`https://qwenlm.github.io/blog/` — `static`（GitHub Pages/Jekyll），**有 RSS**：`/blog/index.xml`。
- **文章 URL**：`/blog/{slug}/`。中英双语，结构规范，强烈推荐作为国内首选抓取源。
- 模型：ModelScope + HuggingFace。代码：`github.com/QwenLM`。

## DeepSeek 深度求索
- **新闻**：`https://api-docs.deepseek.com/news/` — `static`（Docusaurus 文档站，易抓）。
- **代码/报告**：`github.com/deepseek-ai`；完整论文在 arXiv；模型在 HuggingFace。
- 主题：DeepSeek-V 系、R 系推理模型、MoE。

## 智谱 AI（GLM / Z1）
- **博客**：`https://z.ai/blog` — `js`。策略：`WebSearch("site:z.ai/blog 2026")` 发现文章 URL，再逐篇 `WebFetch`。
- **代码/报告**：`github.com/THUDM`（GLM-4、CogVLM2）、`github.com/zai-org`（Z1 推理模型）。
- 动态多发微信/知乎；WebSearch 可补充发布公告。
- 难度：**中**

## 月之暗面 Moonshot AI（Kimi）
- **无独立博客**。主要来源：
  - GitHub `github.com/MoonshotAI`：重点仓库 Kimi-k2、Kimi-VL、kimi-audio（README + Release）
  - arXiv：WebSearch(`arxiv.org MoonshotAI Kimi 2026`) 找论文
  - WebSearch 发现产品公告
- 难度：**中**

## 字节跳动 Seed（豆包）
- **研究站**：`https://seed.bytedance.com/en/blog` — `js`，中英双语。
- **代码/论文**：`github.com/ByteDance-Seed`、arXiv。

## 腾讯混元 Hunyuan
- **入口**：`github.com/Tencent-Hunyuan` — `github`（文/图/视频/3D 模型开源）。
- 官网 `hunyuan.tencent.com` 偏产品；技术细节看 GitHub README 与 arXiv。

## 百度文心 ERNIE
- **研究院博客**：`http://research.baidu.com/Blog` — `js`。
- **代码/模型**：`github.com/PaddlePaddle/ERNIE`。

## MiniMax 稀宇科技
- **无独立博客**。主要来源：
  - GitHub `github.com/MiniMax-AI`：MiniMax-01、MiniMax-Text-01、MiniMax-VL-01 README + 技术报告
  - arXiv：WebSearch(`arxiv.org MiniMax 2026`)
  - WebSearch 补充新闻
- 官网 `minimaxi.com` 偏产品展示，不含技术内容。
- 难度：**易**

---

## 新增国内来源

### 零一万物 Yi / 01.AI ⭐（有英文博客）
- **博客**：`https://www.01.ai/en/blog` — `js`。策略：`WebSearch("site:01.ai/en/blog")` 发现文章。
- **代码/报告**：`github.com/01-ai`（Yi 系列模型）。
- 李开复创立，Yi 模型是国内开源长上下文领域的重要成果。
- 难度：**中**

### 百川智能 Baichuan
- **无独立博客**。主要来源：
  - GitHub `github.com/baichuan-inc`：Baichuan2、Baichuan-7B/13B README + 技术报告
  - arXiv：WebSearch(`arxiv.org Baichuan 2026`)
- 难度：**易**

### 北京智源研究院 BAAI ⭐⭐（有静态博客，最易抓）
- **博客**：`https://www.baai.ac.cn/blog.html` — `static`，直接 WebFetch 即可列出文章列表。
- **代码**：`github.com/FlagAI-Open`（FlagAI、Aquila）、`github.com/FlagOpen`（BGE Embedding、COIG 数据集）。
- 国内学术 AI 影响力最大机构之一，BGE 向量模型被广泛使用，COIG 是主流中文指令微调数据集。
- 难度：**易** ← 推荐作为国内学术来源首选

### 阶跃星辰 StepFun
- **无独立博客**。主要来源：
  - WebSearch 发现 Step-2/Step-Audio 等发布公告
  - GitHub `github.com/stepfun-ai` 技术报告
  - arXiv：WebSearch(`arxiv.org StepFun 2026`)
- 难度：**中**

### 面壁智能 MiniCPM / OpenBMB
- **无独立博客**。主要来源：
  - GitHub `github.com/OpenBMB`：MiniCPM、MiniCPM-V、ToolBench、AgentBench README（内容质量高）
  - arXiv：WebSearch(`arxiv.org MiniCPM OpenBMB 2026`)
- 清华 NLP 实验室背景，MiniCPM 小模型领域国内最重要的开源成果之一。
- 难度：**易**

---

## 维护说明

1. 新增来源：在 `blogs.json` 的 `blogs[]` 增加一项，并在本文件对应分组补一节。
2. URL 失效：现场校验后更新 `index_url` / `article_pattern` / `render`。
3. 字段含义见 `blogs.json` 顶部的 `fetch_strategies`。
