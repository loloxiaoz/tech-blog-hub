#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_render.py — 检查生成的 HTML 文章页是否存在渲染问题

检测项：
  1. HTML 标签显示为文字（<img>, <table> 等出现在 .prose 文本节点中）
  2. 语言切换链接残留（[English] | [简体中文] 显示为文字链接）
  3. 摘要字段为空或为星数格式（⭐ 数字）
  4. 文章标题为无意义值（"or", "and", "README" 等）
  5. 正文过短（< 200 字符，可能抓取失败）

用法：
  python3 check_render.py                         # 检查默认 site 目录
  python3 check_render.py --site ~/Desktop/site   # 指定目录
  python3 check_render.py --fix                   # 检查后重新生成网站
"""
import os, re, sys, json, argparse
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    BS4 = True
except ImportError:
    BS4 = False

HERE      = Path(__file__).parent.resolve()
GEN_SCRIPT = HERE / "generate_site.py"
DEFAULT_SITE = Path.home() / "Desktop" / "ai-blogs" / "site"

# ── 检测规则 ──────────────────────────────────────────────────────────────
# 1. prose 文本节点中出现 HTML 标签
RE_RAW_HTML = re.compile(r'<(?:img|table|div|p|tr|td|th|ul|ol|li|a|iframe|b|strong|i|em)\s', re.I)
# 2. 语言切换文字残留
RE_LANG_SWITCH = re.compile(r'\[(?:English|简体中文|繁體中文|中文)\]\s*\(', re.I)
# 3. 星数摘要
RE_STAR_SUMMARY = re.compile(r'[⭐★🌟]\s*\d+')
# 4. 无意义标题
BAD_TITLES = {"or", "and", "readme", "index", "table of contents", "目录", "contents", "introduction"}
# 5. 正文最小长度
MIN_BODY_LEN = 200

SEVERITY = {"error": "❌", "warn": "⚠️ ", "info": "ℹ️ "}

def check_html_file(html_path):
    """检查单个 HTML 文章页，返回问题列表"""
    issues = []
    content = html_path.read_text(encoding="utf-8", errors="ignore")

    if BS4:
        soup = BeautifulSoup(content, "html.parser")
        prose = soup.find(class_="prose")
        title_el = soup.find("h1")
        title = title_el.get_text(strip=True) if title_el else ""

        # 检查 1：prose 中的 HTML 标签文字
        if prose:
            for text_node in prose.find_all(string=True):
                t = text_node.strip()
                # 跳过 HTML 注释（Comment 类型节点）
                if hasattr(text_node, 'name'):
                    continue
                from bs4 import Comment
                if isinstance(text_node, Comment):
                    continue
                if RE_RAW_HTML.search(t):
                    snippet = t[:80].replace("\n", " ")
                    issues.append(("error", f"HTML标签渲染为文字: {snippet}..."))
                    break  # 每文件只报一次
            # 检查 2：语言切换残留
            prose_text = prose.get_text()
            if RE_LANG_SWITCH.search(prose_text):
                issues.append(("warn", "语言切换链接 [English]|[简体中文] 残留"))
            # 检查 5：正文过短
            body_len = len(prose_text.strip())
            if body_len < MIN_BODY_LEN:
                issues.append(("warn", f"正文过短({body_len}字符)，可能抓取失败"))

        # 检查 4：无意义标题
        if title.strip().lower() in BAD_TITLES:
            issues.append(("warn", f"标题无意义: \"{title}\""))

        # 检查摘要卡片是否为空
        sc = soup.find(class_="summary-card")
        if sc:
            sc_text = sc.get_text(strip=True)
            if RE_STAR_SUMMARY.search(sc_text):
                issues.append(("warn", f"摘要为星数格式: {sc_text[:50]}"))
            elif len(sc_text.replace("中文摘要","").replace("English Summary","").strip()) < 10:
                issues.append(("info", "摘要内容为空"))
    else:
        # 无 BS4 时用正则降级检查
        if RE_RAW_HTML.search(content):
            issues.append(("error", "HTML 标签可能渲染为文字（需安装 beautifulsoup4 精确检测）"))
        if RE_LANG_SWITCH.search(content):
            issues.append(("warn", "语言切换链接残留"))
        if RE_STAR_SUMMARY.search(content):
            issues.append(("warn", "摘要为星数格式"))

    return issues

def check_site(site_dir, verbose=False):
    articles_dir = site_dir / "articles"
    if not articles_dir.exists():
        print(f"[错误] articles 目录不存在: {articles_dir}")
        return {}

    html_files = sorted(articles_dir.glob("*.html"))
    print(f"检查 {len(html_files)} 篇文章...\n")

    by_severity = {"error": [], "warn": [], "info": []}
    total_issues = 0

    for f in html_files:
        issues = check_html_file(f)
        if not issues:
            if verbose:
                print(f"  ✅ {f.name}")
            continue
        total_issues += len(issues)
        for sev, msg in issues:
            by_severity[sev].append((f.name, msg))

    # 输出报告
    for sev in ("error", "warn", "info"):
        items = by_severity[sev]
        if not items:
            continue
        label = {"error": "严重错误", "warn": "警告", "info": "提示"}[sev]
        print(f"{SEVERITY[sev]} {label} ({len(items)} 个)")
        print("─" * 60)
        for fname, msg in items:
            print(f"  {fname[:55]:55s} {msg}")
        print()

    # 汇总
    errors = len(by_severity["error"])
    warns  = len(by_severity["warn"])
    clean  = len(html_files) - len(set(n for n,_ in by_severity["error"]+by_severity["warn"]))

    print("─" * 60)
    print(f"总计: {len(html_files)} 篇  |  "
          f"❌ {errors} 严重  ⚠️  {warns} 警告  ✅ {clean} 通过")
    return by_severity

def main():
    p = argparse.ArgumentParser(description="检查生成网站的渲染问题")
    p.add_argument("--site", default=str(DEFAULT_SITE), help="网站目录（含 articles/）")
    p.add_argument("--fix",  action="store_true", help="检查后重新生成网站")
    p.add_argument("--verbose", "-v", action="store_true", help="显示所有通过的文章")
    args = p.parse_args()

    site_dir = Path(args.site)
    if not BS4:
        print("⚠️  未安装 beautifulsoup4，降级为正则检测（精度较低）")
        print("   建议: pip install beautifulsoup4\n")

    issues = check_site(site_dir, verbose=args.verbose)

    if args.fix and (issues.get("error") or issues.get("warn")):
        # 找 articles md 目录
        articles_md = site_dir / "articles"
        # md 源文件在同一目录
        md_files = list(articles_md.glob("*.md"))
        if md_files and GEN_SCRIPT.exists():
            import subprocess
            print(f"\n重新生成网站...")
            result = subprocess.run(
                [sys.executable, str(GEN_SCRIPT), str(articles_md), str(site_dir)],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✅ 重新生成完成: open \"{site_dir}/index.html\"")
            else:
                print(f"❌ 生成失败: {result.stderr[:200]}")

if __name__ == "__main__":
    main()
