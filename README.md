# tech-blog-hub

> AI 大厂技术博客聚合站 —— 下载 · 中文翻译 · 静态学习网站一键生成

把 Anthropic、OpenAI、DeepSeek、Qwen、Kimi 等 **23 个** AI 机构的英文技术博客，通过 Claude Code 技能自动完成：

```
发现文章 → 抓取正文 → 翻译为中文 → 生成可离线浏览的静态学习站
```

---

## 目录结构

```
tech-blog-hub/
├── skill/                   # Claude Code 技能（核心）
│   ├── SKILL.md             # Agent 执行流程（主入口）
│   ├── blogs.json           # 23 个来源注册表（URL / 抓取策略 / 配色）
│   ├── generate_site.py     # Markdown → HTML 静态站生成器（零依赖）
│   ├── harvest.py           # 全流程自动化脚本（列出 / 规划 / 建站）
│   ├── fetcher.py           # 本机直接抓取工具（需 requests + bs4）
│   ├── tag_articles.py      # 文章标签自动打标
│   ├── check.py             # 文章质量检查
│   ├── check_render.py      # HTML 渲染验证
│   ├── install.py           # 安装辅助脚本
│   ├── install.sh           # 一键安装到 Claude Code
│   ├── DESIGN.md            # 网站视觉设计规范（Anthropic 品牌风格）
│   ├── SKILL.md             # 技能描述与执行指令
│   ├── skill.json           # 技能元数据
│   ├── references/
│   │   └── blogs.md         # 23 个来源详细说明（人类可读）
│   └── examples/
│       ├── articles/        # 4 篇样例文章（可直接测试建站）
│       └── site/            # 对应演示站点
└── site/                    # 已生成的学习网站
    ├── index.html           # 首页（搜索 + 筛选 + 卡片）
    ├── manifest.json        # 文章清单（机器可读）
    ├── graph.html           # 知识图谱
    └── articles/            # 各篇阅读页（.md 原文 + .html 渲染页）
```

---

## 快速开始

### 方式一：使用 Claude Code 技能（推荐）

**安装技能：**

```bash
cd skill
bash install.sh
```

安装后，在 Claude Code 中直接用自然语言：

```
抓取 Anthropic 工程博客最新 10 篇，翻译成中文，生成学习站
```

```
列出 Qwen 最近发布的文章
```

```
翻译这篇文章 https://www.anthropic.com/engineering/...
```

### 方式二：本地 Demo（无需网络）

用内置 4 篇样例文章快速体验建站效果：

```bash
cd skill
python3 generate_site.py
# → examples/site/index.html
open examples/site/index.html
```

### 方式三：从已有文章目录建站

```bash
python3 skill/generate_site.py <articles_dir> <output_dir> --title "我的 AI 学习站"
```

示例：

```bash
python3 skill/generate_site.py ~/Desktop/articles ~/Desktop/site --title "Anthropic 精选"
open ~/Desktop/site/index.html
```

---

## 支持的博客来源（23 个）

### 国际机构

| 机构 | 抓取策略 | 主要话题 |
|---|---|---|
| Anthropic 工程博客 | 静态页 | Agent、Eval、MCP、Claude Code |
| Anthropic 研究与新闻 | 静态页 | 可解释性、对齐、安全 |
| OpenAI 新闻与研究 | JS 渲染 | GPT、研究、产品 |
| Google DeepMind | JS 渲染 | Gemini、强化学习、Agent |
| Google Research | JS 渲染 | ML、系统、NLP |
| Meta AI | JS 渲染 | Llama、FAIR、开源 |
| Microsoft Research | RSS | Phi、系统、Agent |
| Mistral AI | JS 渲染 | 开源权重模型 |
| Hugging Face | 静态 + RSS | Transformers、微调、社区 |
| NVIDIA | — | GPU、推理、系统 |

### 国内机构

| 机构 | 抓取策略 | 主要话题 |
|---|---|---|
| 阿里 Qwen / 通义千问 | RSS（GitHub Pages）| Qwen、多模态、Agent |
| DeepSeek 深度求索 | 静态页 + GitHub | V3、R1、MoE、推理 |
| 智谱 AI（GLM） | JS 渲染 + GitHub | GLM-4、Z1、长文本 |
| 月之暗面（Kimi） | 静态页 + GitHub | Kimi-k2、长文本、MoE |
| 字节跳动 Seed（豆包）| JS 渲染 + GitHub | 豆包、Seed、多模态 |
| 腾讯混元 | GitHub + arXiv | 混元、MoE、3D、视频 |
| 百度文心（ERNIE） | 静态页 | ERNIE、PaddlePaddle |
| MiniMax 稀宇科技 | GitHub + arXiv | MiniMax-01、长文本、音频 |
| 零一万物（Yi） | JS 渲染 + GitHub | Yi、视觉、长文本 |
| 北京智源 BAAI | 静态页 + GitHub | BGE、数据集、Aquila |
| 阶跃星辰 StepFun | GitHub + arXiv | Step-2、音频、多模态 |

完整 URL 和抓取策略见 `skill/blogs.json`，人类可读版见 `skill/references/blogs.md`。

---

## 生成网站功能

**首页：**
- 实时全文搜索（标题 + 摘要 + 标签）
- 按来源机构筛选（机构色彩徽章）
- 文章卡片：发布日期、摘要、标签、预计阅读时长
- 已读计数

**阅读页：**
- 自动 H2/H3 目录（桌面端侧边栏固定）
- 上一篇 / 下一篇导航
- 原文链接按钮
- 已读标记（localStorage 持久化）

**技术特点：**
- 纯静态 HTML，零依赖
- `file://` 直接打开，无需服务器
- 可部署到 GitHub Pages / Vercel / 任意静态托管

---

## Markdown 文章格式

每篇文章为 `.md` 文件，支持以下 frontmatter（均可选）：

```markdown
---
title: "构建有效的 AI Agent"
org: "Anthropic"
date: 2026-01-15
source_url: "https://www.anthropic.com/engineering/building-effective-agents"
tags: ["Agent", "工程实践", "MCP"]
summary: "最成功的 Agent 实现依赖简单可组合的模式，而非复杂框架。"
---

# 构建有效的 AI Agent

正文...
```

| 字段 | 必须 | 说明 |
|---|---|---|
| `title` | 建议 | 缺失时取首个 `#` 标题 |
| `org` | **强烈建议** | 决定卡片配色和来源筛选 |
| `date` | 建议 | 决定排序（倒序） |
| `source_url` | 建议 | 阅读页"原文链接"按钮 |
| `tags` | 可选 | 数组，首页最多显示 3 个 |
| `summary` | 建议 | 缺失时自动取首段截断至 120 字 |

---

## 环境要求

- Python 3.7+
- `generate_site.py` / `harvest.py`：**零依赖**（仅用标准库）
- `fetcher.py`（本机直接抓取）：需要 `requests` + `beautifulsoup4`

```bash
pip install requests beautifulsoup4
```

- 翻译功能（`--translate`）：需要 `anthropic` 包 + `ANTHROPIC_API_KEY`

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## 视觉设计

网站对齐 Anthropic 官方视觉语言（Warm Minimalism 风格）：

- 主色：陶土橙 `#D97757`，暖米白底 `#F0EEE6`
- 字体：Fraunces（衬线大标题）+ Inter（正文）
- 详细设计规范见 `skill/DESIGN.md`

---

## License

MIT
