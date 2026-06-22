# tech-blog-downloader

> AI 大厂技术博客下载器 + 中文学习站生成器

把 Anthropic、OpenAI、DeepSeek 等 23 个 AI 机构的英文博客，**下载 → 翻译成中文 → 生成一个可离线浏览的学习网站**。

---

## 30 秒体验 Demo

```bash
python3 generate_site.py
# 用内置 4 篇样例文章生成演示站
# → examples/site/index.html
open examples/site/index.html
```

---

## 安装为 Claude Code 技能

```bash
bash install.sh
```

安装后在 Claude Code 中直接说：

> "抓取 Anthropic 工程博客最新 10 篇，生成中文学习站"

---

## 独立使用（无需 Claude Code）

### 1. 准备文章

每篇文章存为 `.md` 文件，建议加 frontmatter：

```markdown
---
title: "构建有效的 AI Agent"
org: "Anthropic"
date: 2026-01-15
source_url: "https://www.anthropic.com/engineering/building-effective-agents"
tags: ["Agent", "工程实践"]
summary: "最成功的 Agent 实现依赖简单可组合的模式，而非复杂框架。"
---

# 构建有效的 AI Agent

正文...
```

字段说明：

| 字段 | 必须 | 说明 |
|---|---|---|
| `title` | 建议 | 缺失时取首个 `#` 标题 |
| `org` | **强烈建议** | 决定首页卡片配色和来源筛选 |
| `date` | 建议 | 决定文章排序（倒序） |
| `source_url` | 建议 | 阅读页"原文链接"按钮 |
| `tags` | 可选 | 数组，最多显示 3 个 |
| `summary` | 建议 | 缺失时自动取首段，最多 120 字 |

### 2. 生成网站

```bash
python3 generate_site.py <articles_dir> <output_dir> --title "我的 AI 学习站"
```

示例：

```bash
python3 generate_site.py ~/Desktop/articles ~/Desktop/site --title "Anthropic 精选"
open ~/Desktop/site/index.html
```

---

## 支持的博客来源（23 个）

| 类型 | 来源 | 抓取难度 |
|---|---|---|
| 国外 | Anthropic 工程/研究、OpenAI、Google DeepMind、Google Research | 中等 |
| 国外 | Meta AI、Microsoft Research、Mistral、Hugging Face、NVIDIA | 中等 |
| 国内 | Qwen、DeepSeek | 容易（静态/RSS）|
| 国内 | 智谱 GLM、Kimi、字节 Seed、腾讯混元、百度文心、MiniMax | 需 GitHub/arXiv |
| 国内 | 零一万物（Yi）、百川智能、智源 BAAI、阶跃星辰、面壁 MiniCPM | 需 GitHub/arXiv |

完整 URL 和抓取策略见 `blogs.json`。

---

## 网站功能

首页：
- 实时全文搜索（标题 + 摘要 + 标签）
- 按来源机构筛选
- 文章卡片：机构色彩徽章、日期、摘要、标签、阅读时长
- 已读计数

阅读页：
- 自动 H2/H3 目录（桌面端侧边栏）
- 上一篇 / 下一篇导航
- 原文链接
- 已读标记（localStorage 持久化）

**纯静态 HTML，零依赖，`file://` 直接打开，可部署到任意静态托管服务。**

---

## 文件说明

| 文件 | 作用 |
|---|---|
| `SKILL.md` | Claude Code 技能指令（agent 执行流程）|
| `DESIGN.md` | 网站视觉设计规范（Anthropic 品牌风格）|
| `blogs.json` | 来源注册表（机器可读）|
| `references/blogs.md` | 来源详解（人类可读）|
| `generate_site.py` | Markdown → HTML 静态站生成器 |
| `install.sh` | 一键安装到 Claude Code |
| `examples/` | 4 篇样例文章 + 演示网站 |
| `anthropic-cards/` | 进阶：Anthropic 研究信息图卡片 |

---

## 要求

- Python 3.7+
- `generate_site.py` / `harvest.py`：**零依赖**（仅用 Python 标准库）
- `fetcher.py`（本机抓取）：需要 `requests` + `beautifulsoup4`

```bash
pip install requests beautifulsoup4
```

- 网络访问（抓取时需要；本地生成网站不需要）
- `--translate` 翻译功能：需要 `anthropic` 包 + `ANTHROPIC_API_KEY` 环境变量
