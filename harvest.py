#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harvest.py — AI 技术博客全流程自动化收割脚本

两种运行模式：

  模式 A：AI 辅助模式（推荐）
    由 Claude Code / OpenClaw 调用 SKILL.md 工作流执行实际抓取，
    本脚本负责：来源发现 → 构建抓取任务清单 → 格式标准化 → 建站。

  模式 B：转化模式（无需网络）
    把已有的 Markdown 文章目录（格式不限）转换为网站格式。

用法：
  # 列出所有来源（不抓取，供 Agent 参考）
  python3 harvest.py --list

  # 生成抓取指令（输出给 Agent 执行）
  python3 harvest.py --plan --sources anthropic-engineering,qwen --count 10

  # 转化已有文章目录并建站（无需网络）
  python3 harvest.py --convert <articles_dir> --out <site_dir>

  # 全流程（假设 articles_dir 已由 Agent 填充）
  python3 harvest.py --build --articles ~/Desktop/harvest/articles --out ~/Desktop/harvest/site
"""
import os, sys, re, json, glob, argparse, shutil, subprocess
from datetime import datetime, timezone

HERE     = os.path.dirname(os.path.abspath(__file__))
BLOGS_JSON  = os.path.join(HERE, "blogs.json")
GEN_SCRIPT  = os.path.join(HERE, "generate_site.py")
DEFAULT_OUT = os.path.expanduser("~/Desktop/ai-blogs")

# ── 机构配色（与 generate_site.py 保持一致）────────────────────────────────
ORG_COLORS = {
    "anthropic": "#D97757", "openai": "#10A37F", "deepmind": "#4285F4",
    "google": "#4285F4", "meta": "#0064E0", "microsoft": "#0A84FF",
    "mistral": "#FF7000", "hugging": "#FF9D00", "nvidia": "#76B900",
    "qwen": "#615CED", "阿里": "#615CED", "deepseek": "#4D6BFE",
    "智谱": "#3859FF", "zhipu": "#3859FF", "moonshot": "#16213E",
    "kimi": "#16213E", "月之暗面": "#16213E", "字节": "#325AB4",
    "bytedance": "#325AB4", "腾讯": "#0052D9", "tencent": "#0052D9",
    "百度": "#2932E1", "baidu": "#2932E1", "minimax": "#E1341E",
    "零一": "#6366F1", "01.ai": "#6366F1", "百川": "#8B5CF6",
    "baichuan": "#8B5CF6", "baai": "#0891B2", "智源": "#0891B2",
    "阶跃": "#D97706", "stepfun": "#D97706", "面壁": "#059669",
    "openbmb": "#059669", "minicpm": "#059669",
}

def load_blogs():
    return json.load(open(BLOGS_JSON, encoding="utf-8"))

def color_for(org):
    o = (org or "").lower()
    for k, v in ORG_COLORS.items():
        if k in o:
            return v
    return "#64748B"

# ── 模式 A：生成抓取计划（输出给 Agent）───────────────────────────────────
def cmd_list(args):
    data = load_blogs()
    print(f"\n{'ID':30s} {'来源':24s} {'Render':8s} {'难度':6s} 入口")
    print("─" * 100)
    sources = args.sources.split(",") if args.sources else None
    for b in data["blogs"]:
        if sources and b["id"] not in sources:
            continue
        diff  = b.get("difficulty", "?")
        print(f"  {b['id']:28s} {b['name_cn']:22s} {b['render']:8s} {diff:6s} {b['index_url']}")
    print()

def cmd_plan(args):
    """输出结构化抓取指令，供 Agent（Claude Code / OpenClaw）执行"""
    data = load_blogs()
    sources = args.sources.split(",") if args.sources else None
    count = args.count or 10
    out_dir = os.path.abspath(args.articles or os.path.join(DEFAULT_OUT, "articles"))

    plan = []
    for b in data["blogs"]:
        if sources and b["id"] not in sources:
            continue
        plan.append(b)

    print(f"\n# AI 技术博客抓取任务计划")
    print(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"# 目标目录: {out_dir}")
    print(f"# 来源数量: {len(plan)}  每源最多: {count} 篇")
    print(f"\n## 执行说明")
    print(f"将此计划交给 Claude Code 执行（SKILL.md 工作流第 1-4 步）。")
    print(f"执行完成后运行：python3 harvest.py --build --articles {out_dir}\n")
    print("─" * 60)

    for b in plan:
        render = b["render"]
        print(f"\n### {b['name_cn']} ({b['id']})")
        print(f"- org 字段: \"{b['org']}\"")
        print(f"- render:   {render}")

        if render == "static":
            print(f"- 策略: WebFetch(\"{b['index_url']}\", \"列出所有文章标题、URL、日期，时间倒序，取最新{count}篇\")")
            print(f"        → 逐篇 WebFetch 正文")
        elif render == "rss" and b.get("rss"):
            print(f"- 策略: WebFetch(\"{b['rss']}\", \"解析 RSS feed，列出最新{count}条：标题/链接/日期\")")
            print(f"        → 逐篇 WebFetch 正文")
        elif render == "js":
            domain = re.sub(r'https?://', '', b['index_url']).split('/')[0]
            print(f"- 策略: WebSearch(\"site:{domain} 技术 2026\") → 发现文章 URL")
            print(f"        → 逐篇 WebFetch 正文（最新{count}篇）")
        elif render == "github":
            gh = b.get("github", b["index_url"])
            key_repos = b.get("key_repos", [])
            print(f"- 策略: WebFetch(\"{gh}\", \"列出所有仓库名称和描述\")")
            if key_repos:
                print(f"        重点仓库: {', '.join(key_repos)}")
            print(f"        → 逐仓库 WebFetch README + Release Notes")
        elif render == "arxiv":
            print(f"- 策略: WebSearch(\"arxiv.org {b['org']} 2026\") → WebFetch 摘要页")

        print(f"- 每篇存为: {out_dir}/{b['id']}-NNN.md")
        print(f"  frontmatter 必填: title / org:\"{b['org']}\" / date / source_url / tags / summary")

ORG_PREFIXES = [
    (["anthropic","claude-","c-compiler","advanced-tool","ai-transforming","ai-resistant",
      "ai-cyber-threats","ai-coding-skills","ai-productivity","ai-software-dev","assistant-axis",
      "auditing","automated-align","building-effective","chris-olah","circuit-tracing",
      "code-execution-mcp","coding-agents","context-engineering","contextual-retrieval",
      "demystifying-evals","diff-tool","disempowerment","donating-align","economic-index",
      "education-report","effective-harnesses","election-safeguards","emotion-concepts",
      "eval-awareness","harness-design","india-country-brief","infrastructure-noise",
      "introducing-bloom","labor-market","making-claude","mcp-desktop","measuring-agent",
      "model-deprecation","multi-agent-research","natural-language-auto","next-gen-constitutional",
      "persona-selection","persona-vectors","postmortem","project-deal","project-glasswing",
      "project-vend","scaling-managed","services-track","shortcuts-to","signs-of",
      "swe-bench-verified","teaching-claude","think-tool-anthropic","tracing-llm",
      "values-in-the-wild","what-people-want","widening-frontier","writing-effective-tools",
      "australia-claude","2028-ai","anthropic-series","anthropic-s1","anthropic-korea",
      "anthropic-milan","anthropic-institute","anthropic-interview","anthropic-economic"],
     "Anthropic"),
    (["qwen","tongyi"], "阿里巴巴"),
    (["deepseek"], "DeepSeek"),
    (["lightrag","graphrag","pageindex","tree-rag","graph-rag","multimodal-rag",
      "hybrid-retrieval","reranking","metadata-design","rag-eval","rag-retrieval","rag-2025",
      "rag-interview","enterprise-rag","industrial-rag","llm-wiki","llm-rag","kg-llm",
      "document-quality","long-context","late-interaction","chunking","lightrag-paper",
      "lightrag-code"], "RAG 研究"),
    (["opc-","nuwa-skill","colleague-skill","embrace-agent","spec-is-code",
      "agent-skills","sft-to-rl","how-to-be-top","openclaw-vs"], "AI 工程实践"),
    (["ant-afoo","dataagent-netease","enterprise-ai-landscape","copilot-to-director",
      "nio-sales","agent-kb-market"], "行业实践"),
    (["memorylake","memos","mem0","second-me","hipporag2","titans"], "记忆系统"),
]

def _derive_org(slug, author, source_url):
    a, u, s = (author or "").lower(), (source_url or "").lower(), slug.lower()
    if "anthropic" in a or "anthropic.com" in u: return "Anthropic"
    if "openai" in a or "openai.com" in u: return "OpenAI"
    if "deepseek" in a or "deepseek" in u: return "DeepSeek"
    if "qwen" in a or "qwenlm" in u: return "阿里巴巴"
    for prefixes, org in ORG_PREFIXES:
        if any(s.startswith(p) or p in s for p in prefixes):
            return org
    return ""

def _parse_fm(text):
    meta, body = {}, text
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw, body = parts[1], parts[2]
            for line in raw.split("\n"):
                if ":" in line and not line.startswith((" ", "\t")):
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip("\"'")
            m = re.search(r'tags:\s*\[([^\]]*)\]', raw)
            if m:
                meta["tags"] = [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    return meta, body

def cmd_convert(args):
    """把任意 Markdown 目录转换为 generate_site.py 标准格式，自动派生 org 字段"""
    src = os.path.abspath(args.convert)
    out_articles = os.path.abspath(args.articles or os.path.join(DEFAULT_OUT, "articles"))
    os.makedirs(out_articles, exist_ok=True)

    files = sorted(glob.glob(os.path.join(src, "**/*.md"), recursive=True))
    converted = 0
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        content = open(f, encoding="utf-8").read()
        meta, body = _parse_fm(content)

        # 派生字段
        author = meta.get("author", "")
        src_url = meta.get("source_url", meta.get("feishu_url", ""))
        org = meta.get("org") or _derive_org(slug, author, src_url)
        date = meta.get("original_date") or meta.get("date", "")
        # title from frontmatter or first H1
        h1 = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        title = meta.get("title") or (re.sub(r'[*_`]', '', h1.group(1)).strip() if h1 else slug)
        # summary from first real paragraph
        summary = meta.get("summary", "")
        if not summary:
            for line in body.split("\n"):
                l = line.strip()
                if l and not l.startswith(("#", "|", "```", ">", "-", "*")):
                    t = re.sub(r'\*+', '', l).strip()
                    if len(t) > 20:
                        summary = t[:140]
                        break
        # tags
        raw_tags = meta.get("tags", [])
        tags = [t for t in (raw_tags if isinstance(raw_tags, list) else [])
                if t not in ("source","ai-llm","engineering","product-biz","safety","")]
        if org and org not in tags:
            tags.insert(0, org)
        tags_str = ", ".join(f'"{t}"' for t in tags[:4])

        # clean body: remove wiki [[links]]
        clean_body = re.sub(r'\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]',
                            lambda m: m.group(2) if m.group(2) else m.group(1), body)
        safe_title = title.replace('"', '\\"')
        safe_summary = summary.replace('"', '\\"')[:140]
        # 判断摘要语言并分配到对应字段
        cjk_count = len(re.findall(r'[一-鿿]', summary))
        is_chinese = cjk_count > len(summary) * 0.2 if summary else False
        summary_zh = safe_summary if is_chinese else ""
        summary_en = "" if is_chinese else safe_summary

        new_content = (
            f'---\ntitle: "{safe_title}"\norg: "{org}"\ndate: {date}\n'
            f'source_url: "{src_url}"\ntags: [{tags_str}]\n'
            f'summary: "{safe_summary}"\n'
            f'summary_zh: "{summary_zh}"\n'
            f'summary_en: "{summary_en}"\n---\n\n'
            + clean_body
        )
        dest = os.path.join(out_articles, os.path.basename(f))
        open(dest, "w", encoding="utf-8").write(new_content)
        converted += 1

    print(f"✓ 转换完成：{converted} 篇 → {out_articles}")
    return converted, out_articles

def cmd_build(args):
    """调用 generate_site.py 生成网站"""
    articles = os.path.abspath(args.articles or os.path.join(DEFAULT_OUT, "articles"))
    site_out  = os.path.abspath(args.out or os.path.join(DEFAULT_OUT, "site"))
    title = args.title or "AI 技术博客 · 中文学习站"

    if not os.path.isdir(articles):
        print(f"[错误] 文章目录不存在: {articles}")
        print(f"  先运行: python3 harvest.py --plan --sources <来源ID> 并让 Agent 抓取")
        sys.exit(1)

    md_count = len(glob.glob(os.path.join(articles, "*.md")))
    if md_count == 0:
        print(f"[错误] {articles} 下没有 .md 文章")
        sys.exit(1)

    print(f"  {md_count} 篇文章 → 正在生成网站...")
    result = subprocess.run(
        [sys.executable, GEN_SCRIPT, articles, site_out, "--title", title],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[错误] generate_site.py 失败:\n{result.stderr}")
        sys.exit(1)

    index_path = os.path.join(site_out, "index.html")
    print(f"✓ 网站已生成: {index_path}")
    print(f"  浏览器打开: open \"{index_path}\"")
    return index_path

def cmd_stats(args):
    """统计文章目录情况"""
    articles = os.path.abspath(args.articles or os.path.join(DEFAULT_OUT, "articles"))
    files = glob.glob(os.path.join(articles, "*.md"))
    if not files:
        print("暂无文章")
        return

    from collections import Counter
    orgs = Counter()
    dates = []
    for f in files:
        content = open(f, encoding="utf-8").read()
        m_org = re.search(r'^org:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        m_date = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})["\']?', content, re.MULTILINE)
        org = m_org.group(1).strip() if m_org else "未知"
        orgs[org] += 1
        if m_date:
            dates.append(m_date.group(1))

    print(f"\n文章目录: {articles}")
    print(f"总计: {len(files)} 篇\n")
    print(f"{'来源':<20} 文章数")
    print("─" * 30)
    for org, cnt in orgs.most_common():
        print(f"  {org:<18} {cnt}")
    if dates:
        dates.sort()
        print(f"\n时间范围: {dates[0]} → {dates[-1]}")

# ── 主入口 ────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(
        description="AI 技术博客自动化收割工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看所有来源
  python3 harvest.py --list

  # 只看国内容易抓的来源
  python3 harvest.py --list --sources qwen,deepseek,baai

  # 生成抓取计划（给 Agent 看）
  python3 harvest.py --plan --sources anthropic-engineering,qwen,deepseek --count 10

  # 转化已有 wiki/sources/ 并建站
  python3 harvest.py --convert ~/path/to/wiki/sources \
    --articles ~/Desktop/ai-blogs/articles \
    --out ~/Desktop/ai-blogs/site \
    --title "AI 知识库"

  # 文章已由 Agent 填充后直接建站
  python3 harvest.py --build \
    --articles ~/Desktop/ai-blogs/articles \
    --out ~/Desktop/ai-blogs/site
"""
    )
    p.add_argument("--list",    action="store_true", help="列出所有已知来源")
    p.add_argument("--plan",    action="store_true", help="生成抓取指令计划（输出给 Agent）")
    p.add_argument("--convert", metavar="DIR",       help="转化已有 Markdown 目录为标准格式")
    p.add_argument("--build",   action="store_true", help="调用 generate_site.py 建站")
    p.add_argument("--stats",   action="store_true", help="统计文章目录情况")

    p.add_argument("--sources",  metavar="IDS",  help="逗号分隔的来源 ID，如 anthropic-engineering,qwen")
    p.add_argument("--articles", metavar="DIR",  help=f"文章目录（默认 {DEFAULT_OUT}/articles）")
    p.add_argument("--out",      metavar="DIR",  help=f"网站输出目录（默认 {DEFAULT_OUT}/site）")
    p.add_argument("--title",    metavar="TEXT", help="网站标题")
    p.add_argument("--count",    type=int, default=10, help="每源最多抓取篇数（默认 10）")

    args = p.parse_args()

    if args.list:
        cmd_list(args)
    elif args.plan:
        cmd_plan(args)
    elif args.convert:
        converted, out = cmd_convert(args)
        if converted > 0 and args.build:
            args.articles = out
            cmd_build(args)
    elif args.build:
        cmd_build(args)
    elif args.stats:
        cmd_stats(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
