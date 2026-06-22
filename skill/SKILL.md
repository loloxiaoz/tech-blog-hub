---
name: tech-blog-downloader
description: "下载 AI 大厂博客（Anthropic/OpenAI/DeepSeek/Qwen/Kimi 等 23 个来源），翻译为中文，生成可离线浏览的静态学习站。Use when: 抓取/翻译 AI 技术文章、生成中文学习网站、列出博客文章列表。NOT for: 实时新闻、付费墙内容。"
description_zh: "抓取 23 个 AI 大厂博客 → 中文翻译 → 静态学习网站"
description_en: "Download AI tech blogs (Anthropic/OpenAI/DeepSeek etc.), translate to Chinese, generate offline learning site."
version: 1.2.0
license: MIT
user-invocable: true
keywords:
  - ai-blog
  - tech-blog
  - anthropic
  - deepseek
  - openai
  - chinese-translation
  - static-site
homepage: https://clawhub.com/skills/tech-blog-downloader
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "python3",
              "bins": ["python3"],
              "label": "Install Python 3 (brew)"
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "python3",
              "bins": ["python3"],
              "label": "Install Python 3 (apt)"
            },
            {
              "id": "pip-requests",
              "kind": "pip",
              "package": "requests",
              "label": "Install requests (fetcher.py 本机抓取用)"
            },
            {
              "id": "pip-bs4",
              "kind": "pip",
              "package": "beautifulsoup4",
              "label": "Install beautifulsoup4 (fetcher.py 本机抓取用)"
            }
          ]
      }
  }
---

# AI 技术博客下载与中文学习站

## 快速决策树

```
用户请求
├── "列出 XX 博客文章"     → 仅执行第 1-2 步，输出文章列表表格
├── "翻译这篇文章 [URL]"   → 仅执行第 3-4 步，输出单篇 .md 文件
├── "抓 XX 最新 N 篇"     → 执行第 1-5 步，建站
└── "整合多个来源建站"     → 执行第 1-5 步（多来源），建站
```

## 文件结构

```
tech-blog-downloader/
├── SKILL.md          # 本文件（agent 执行指令）
├── DESIGN.md         # 网站视觉设计规范
├── blogs.json        # 来源注册表（URL / 渲染策略 / 抓取建议）
├── references/
│   └── blogs.md      # 来源人类可读版
├── generate_site.py  # Markdown → HTML 静态站生成器（零依赖）
└── examples/
    ├── articles/     # 4 篇样例文章（可直接测试建站）
    └── site/         # 对应的演示网站
```

## 第 1 步：确定来源

读取 `blogs.json`，找到目标来源的条目，记录：`id`、`index_url`、`render` 策略。

来源不在列表时，用 `WebSearch("site:<域名>")` 探测，建立临时条目。

## 第 2 步：发现文章列表

| `render` 值 | 抓取方式 |
|---|---|
| `static` | `WebFetch(index_url, "列出所有文章：标题、URL、发布日期，时间倒序")` |
| `rss` | `WebFetch(rss_url, "解析 RSS feed，列出条目：标题、链接、日期")` |
| `js` | `WebSearch("site:<域名> <主题关键词> 2026")` 发现 URL |
| `github` | WebFetch GitHub 仓库 README / Release Notes；或搜索 arXiv / HuggingFace |

> ⚠️ URL 经常随站点改版失效。发现变化时立即回写 `blogs.json`，不要继续用失效 URL。

**向用户确认范围**（避免抓取过多）：全部 / 最新 N 篇 / 指定主题 / 时间范围。

## 第 3 步：逐篇抓取正文

**抓一篇、处理一篇，不要攒齐后再处理**（防止中途失败丢全部）。

```
WebFetch(article_url,
  "提取完整文章正文：标题、作者、发布日期、所有章节标题与正文、
   关键数据/结论、代码块、表格。不要省略章节。")
```

抓取失败（网络超时、内容为空）时：记录跳过，继续下一篇，最后汇报跳过列表。

## 第 4 步：翻译 → 写 Markdown 文件

### 强制 frontmatter 格式（缺失字段会降级，但影响网站体验）

```markdown
---
title: "文章中文标题"
org: "Anthropic"
date: 2026-06-01
source_url: "https://..."
tags: ["Agent", "上下文工程", "Eval"]
summary: "一句话中文摘要，60字以内，用于首页卡片展示。"
---

# 文章中文标题

正文内容...

## 要点总结

- 要点一
- 要点二
```

### 翻译规范

- 标题、章节、正文：全部中文
- 技术术语**首次出现**保留英文括注：`智能体（Agent）`、`评测（Eval）`
- 代码块、命令、API 名、数字：**原样保留**，不翻译
- 每篇末尾追加 `## 要点总结`（3-5 条 bullet，提炼核心结论）

### 文件保存路径约定

```
~/Desktop/ai-blogs/                ← 默认工作目录（询问用户确认或使用此默认值）
└── articles/
    ├── 01-building-effective-agents.md
    ├── 02-context-engineering.md
    └── ...
```

文件名格式：`序号-slug.md`（如 `01-building-effective-agents.md`）

## 第 5 步：生成网站

```bash
# 在 tech-blog-downloader 目录或任意位置调用均可（路径自动解析）
python3 /path/to/generate_site.py \
  ~/Desktop/ai-blogs/articles \
  ~/Desktop/ai-blogs/site \
  --title "Anthropic 工程博客 · 中文精选"
```

生成产出：
- `site/index.html` — 首页（搜索 + 来源筛选 + 卡片）
- `site/articles/*.html` — 各篇阅读页（TOC + 上下篇 + 已读标记）
- `site/manifest.json` — 文章清单（可机读）

## 第 6 步：汇报结果

向用户报告：
1. 文章数量、来源数量、总阅读时长
2. 网站路径：`open ~/Desktop/ai-blogs/site/index.html`
3. 跳过的文章列表（如有）及原因

---

## 常见模式

| 用户说 | 执行路径 |
|---|---|
| "列出 Qwen 最近的文章" | 步骤 1-2，输出表格 |
| "翻译这篇 https://..." | 步骤 3-4，输出单个 .md |
| "抓 Anthropic 工程博客最新 10 篇" | 步骤 1-5，建完整站 |
| "把 Anthropic + DeepSeek 最新各 5 篇做成学习站" | 步骤 1-5（两来源），建站，首页可按来源筛选 |
| "演示 demo" | `python3 generate_site.py`（默认用 examples/ 数据） |

---

## 注意事项

1. **URL 随时会失效** — `blogs.json` 是起点，每次使用前现场验证，不是缓存答案
2. **国内来源抓取策略** — Qwen（静态+RSS 最稳）、DeepSeek（Docusaurus 静态）、其余走 GitHub/arXiv
3. **`org` 字段决定配色** — 必须与 `blogs.json` 的 `name_cn` 字段对齐，否则 badge 显示"未标注"
4. **去重** — 写入前检查 `articles/` 下已有同名文件，跳过重复抓取
5. **进阶可视化** — 需要把某机构研究做成信息图卡片，参考 `anthropic-cards/` 目录
6. **网站样式规范** — 修改 generate_site.py 视觉时，以 `DESIGN.md` 为唯一真实来源
