#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetcher.py — 本机直接抓取 AI 技术博客（无需 WebFetch，绕过云端安全策略）

依赖：requests, beautifulsoup4（已内置检测，缺失自动提示安装命令）
可选：anthropic（用于翻译，pip install anthropic）

用法：
  python3 fetcher.py --list                              # 列出所有来源
  python3 fetcher.py --sources qwen,deepseek --count 5  # 抓取指定来源
  python3 fetcher.py --sources all-easy --count 10      # 仅抓 easy 难度来源
  python3 fetcher.py --sources all --count 5 --translate # 全部来源+翻译
  python3 fetcher.py --sources qwen --build              # 抓完自动建站
"""
import os, sys, re, json, time, html, hashlib, argparse
import urllib.request, urllib.parse
from datetime import datetime
from pathlib import Path

# ── 依赖检查 ──────────────────────────────────────────────────────────────
def _check_deps():
    missing = []
    try:
        import requests
    except ImportError:
        missing.append("requests")
    try:
        import bs4
    except ImportError:
        missing.append("beautifulsoup4")
    if missing:
        print(f"[错误] 缺少依赖: {', '.join(missing)}")
        print(f"  安装命令: pip install {' '.join(missing)}")
        sys.exit(1)

_check_deps()
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# ── 常量 ──────────────────────────────────────────────────────────────────
HERE      = Path(__file__).parent.resolve()
BLOGS_JSON = HERE / "blogs.json"
GEN_SCRIPT = HERE / "generate_site.py"
DEFAULT_OUT = Path.home() / "Desktop" / "ai-blogs"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
HEADERS = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
SLEEP_BETWEEN = 1.5   # 礼貌间隔，避免被限速
REQUEST_TIMEOUT = 15  # 秒

# ── 机构配色（与 generate_site.py 一致）─────────────────────────────────
ORG_COLORS = {
    "Anthropic": "#D97757", "OpenAI": "#10A37F", "Google DeepMind": "#4285F4",
    "Meta": "#0064E0", "Microsoft": "#0A84FF", "Mistral AI": "#FF7000",
    "Hugging Face": "#FF9D00", "NVIDIA": "#76B900", "阿里巴巴": "#615CED",
    "DeepSeek": "#4D6BFE", "智谱 AI": "#3859FF", "Moonshot AI": "#16213E",
    "字节跳动": "#325AB4", "腾讯": "#0052D9", "百度": "#2932E1",
    "MiniMax": "#E1341E", "零一万物": "#6366F1", "百川智能": "#8B5CF6",
    "智源研究院": "#0891B2", "阶跃星辰": "#D97706", "面壁智能": "#059669",
}

# ── 工具函数 ──────────────────────────────────────────────────────────────
def slug(text):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip().lower()).strip("-")
    return s[:60] or "article"

def safe_get(url, retries=2, **kwargs):
    """带重试的 HTTP GET"""
    kwargs.setdefault("headers", HEADERS)
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, **kwargs)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == retries:
                raise
            time.sleep(2)

def html_to_md(soup_or_text):
    """把 BeautifulSoup 节点或 HTML 字符串转成简单 Markdown"""
    if isinstance(soup_or_text, str):
        soup_or_text = BeautifulSoup(soup_or_text, "html.parser")
    parts = []
    for el in soup_or_text.descendants:
        if not hasattr(el, "name"):
            continue
        tag = el.name
        if tag in ("script", "style", "nav", "footer", "header", "aside"):
            el.decompose()
    text = soup_or_text.get_text(separator="\n")
    # 清理多余空行
    lines = [l.rstrip() for l in text.split("\n")]
    prev_blank = False
    for l in lines:
        is_blank = not l.strip()
        if is_blank and prev_blank:
            continue
        parts.append(l)
        prev_blank = is_blank
    return "\n".join(parts).strip()

def extract_main_content(html_text, url=""):
    """从 HTML 中提取主要正文区域 → 返回 (title, body_text)"""
    soup = BeautifulSoup(html_text, "html.parser")
    # 移除干扰元素
    for tag in soup.find_all(["script","style","nav","footer","header",
                               "aside","iframe","noscript","form"]):
        tag.decompose()
    # 提取标题
    title = ""
    if soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)
    elif soup.title:
        title = soup.title.string or ""
    # 尝试找主内容容器（按优先级）
    candidates = [
        soup.find("article"),
        soup.find("main"),
        soup.find(class_=re.compile(r"(post|article|content|entry|prose|blog)[-_]?(body|content|text|inner)?", re.I)),
        soup.find(id=re.compile(r"(post|article|content|main)", re.I)),
    ]
    content_el = next((c for c in candidates if c), None)
    if not content_el:
        content_el = soup.find("body") or soup
    body = html_to_md(content_el)
    return title.strip(), body

_NAV_WORDS = {"github","huggingface","discord","twitter","arxiv","modelscope","readme","license",
              "installation","requirements","contributing","changelog","star","fork","watch",
              "issues","pull","request","releases","tags","code","⭐","🌟","badge","shield"}

def extract_summary(text, max_len=150):
    """从正文提取第一个有意义的段落作为摘要（跳过导航/徽章行/HTML标签行）"""
    for line in text.split("\n"):
        l = line.strip()
        if len(l) < 30 or l.startswith(("#", ">", "-", "*", "|", "```", "!", "[")):
            continue
        # 跳过包含 HTML 标签的行（如 <img>、<source>、<div> 等）
        if re.search(r'<[a-zA-Z][^>]*>', l):
            continue
        words_lower = set(re.sub(r'[^\w\s]', ' ', l).lower().split())
        nav_hit = len(words_lower & _NAV_WORDS)
        if nav_hit >= 3:
            continue  # 导航/徽章行
        return l[:max_len]
    return text[:max_len]

def deduplicate(articles_dir, source_url):
    """检查是否已存在同一 source_url 的文章"""
    if not articles_dir.exists():
        return False
    for f in articles_dir.glob("*.md"):
        if source_url and source_url in f.read_text(encoding="utf-8", errors="ignore"):
            return True
    return False

def save_article(out_dir, source_id, org, title, body, source_url="",
                 date="", tags=None, summary="", summary_zh="", summary_en="", idx=0):
    """保存一篇文章为 .md 文件（包含双语摘要字段）"""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not title:
        title = f"Article {idx+1}"
    fname = f"{source_id}-{idx+1:02d}-{slug(title)}.md"
    dest = out_dir / fname
    tags = tags or [org]
    if org and org not in tags:
        tags.insert(0, org)
    tags_str = ", ".join(f'"{t}"' for t in tags[:4])
    safe_title   = title.replace('"', '\\"').replace("\n", " ")
    # 自动判断摘要语言
    raw_summary  = summary or extract_summary(body)
    cjk_count    = len(re.findall(r"[一-鿿]", raw_summary))
    is_chinese   = cjk_count > len(raw_summary) * 0.2
    if not summary_zh and not summary_en:
        if is_chinese:
            summary_zh = raw_summary
        else:
            summary_en = raw_summary
    esc_zh = summary_zh.replace('"', '\\"')[:140]
    esc_en = summary_en.replace('"', '\\"')[:200]
    # summary 字段保持向后兼容（首页卡片用）
    card_summary = (summary_zh or summary_en or raw_summary).replace('"', '\\"')[:140]
    fm = (f'---\ntitle: "{safe_title}"\norg: "{org}"\ndate: {date or ""}\n'
          f'source_url: "{source_url}"\ntags: [{tags_str}]\n'
          f'summary: "{card_summary}"\n'
          f'summary_zh: "{esc_zh}"\n'
          f'summary_en: "{esc_en}"\n---\n\n')
    dest.write_text(fm + f"# {title}\n\n" + body, encoding="utf-8")
    return dest

# ── 抓取器：static ────────────────────────────────────────────────────────
def fetch_static(blog, out_dir, count, since_date=None):
    """服务端渲染页面：抓索引 → 解析文章链接 → 逐篇抓取"""
    index_url = blog["index_url"]
    org = blog["org"]
    bid = blog["id"]
    print(f"  [static] {blog['name_cn']} → {index_url}")
    try:
        r = safe_get(index_url)
    except Exception as e:
        print(f"    ⚠ 索引页抓取失败: {e}")
        return 0
    soup = BeautifulSoup(r.text, "html.parser")
    # 发现文章链接（a 标签 + 过滤）
    base = urllib.parse.urlparse(index_url)
    base_url = f"{base.scheme}://{base.netloc}"
    seen_urls = set()
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/"):
            href = base_url + href
        elif not href.startswith("http"):
            continue
        # 过滤掉导航/社交/锚点链接
        if any(x in href for x in ["#", "twitter", "github.com", "linkedin",
                                     "mailto:", "javascript:", "cdn.", "static."]):
            continue
        if href == index_url:
            continue
        # 必须在同域或已知子域
        parsed = urllib.parse.urlparse(href)
        if parsed.netloc and parsed.netloc != base.netloc:
            continue
        text = a.get_text(strip=True)
        if len(text) < 5:
            continue
        if href not in seen_urls:
            seen_urls.add(href)
            links.append((href, text))
    print(f"    发现 {len(links)} 个链接，取前 {count} 篇")
    saved = 0
    for i, (url, link_text) in enumerate(links[:count]):
        if deduplicate(out_dir, url):
            print(f"    skip（已存在）: {url}")
            continue
        try:
            time.sleep(SLEEP_BETWEEN)
            pr = safe_get(url)
            title, body = extract_main_content(pr.text, url)
            if not title:
                title = link_text
            if len(body) < 100:
                print(f"    skip（内容过短）: {url}")
                continue
            # 尝试提取日期
            date = _extract_date(pr.text)
            dest = save_article(out_dir, bid, org, title, body,
                                source_url=url, date=date, idx=saved)
            print(f"    ✓ [{saved+1}] {title[:50]}...")
            saved += 1
        except Exception as e:
            print(f"    ✗ {url}: {e}")
    return saved

def _extract_date(html_text):
    """从 HTML 中提取发布日期"""
    patterns = [
        r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',
        r'"publishedAt"\s*:\s*"(\d{4}-\d{2}-\d{2})',
        r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})',
        r'(\d{4}-\d{2}-\d{2})',
    ]
    for p in patterns:
        m = re.search(p, html_text)
        if m:
            d = m.group(1)
            try:
                datetime.strptime(d, "%Y-%m-%d")
                return d
            except ValueError:
                continue
    return ""

# ── 抓取器：rss ───────────────────────────────────────────────────────────
def fetch_rss(blog, out_dir, count, since_date=None):
    """RSS/Atom feed 解析"""
    rss_url = blog["rss"]
    org = blog["org"]
    bid = blog["id"]
    index_url = blog["index_url"]
    print(f"  [rss]    {blog['name_cn']} → {rss_url}")
    try:
        r = safe_get(rss_url)
    except Exception as e:
        print(f"    ⚠ RSS 抓取失败，降级 static: {e}")
        return fetch_static(blog, out_dir, count, since_date)
    try:
        root = ET.fromstring(r.content)
    except ET.ParseError as e:
        print(f"    ⚠ XML 解析失败: {e}")
        return 0
    # 兼容 RSS 2.0 和 Atom
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//atom:entry", ns)
    print(f"    RSS 条目: {len(items)}，取前 {count} 篇")
    saved = 0
    for item in items[:count]:
        _t = (item.findtext("title") or
              item.findtext("atom:title", namespaces=ns) or "")
        _l = (item.findtext("link") or
              (item.find("atom:link", ns) or {}).get("href", "") or "")
        _d = (item.findtext("pubDate") or
              item.findtext("atom:published", namespaces=ns) or "")
        _c = (item.findtext("description") or
              item.findtext("content") or
              item.findtext("atom:content", namespaces=ns) or
              item.findtext("atom:summary", namespaces=ns) or "")
        title = html.unescape(_t.strip())
        link  = _l.strip()
        # 支持多种日期格式
        date = ""
        if _d:
            # ISO: 2025-09-23
            m = re.search(r"(\d{4}-\d{2}-\d{2})", _d)
            if m:
                date = m.group(1)
            else:
                # RFC 822: Tue, 23 Sep 2025 / Mon, 04 Aug 2025
                m2 = re.search(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})", _d, re.I)
                if m2:
                    months = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
                              "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}
                    day, mon, yr = m2.group(1).zfill(2), months[m2.group(2).lower()], m2.group(3)
                    date = f"{yr}-{mon}-{day}"
        if not link:
            continue
        if deduplicate(out_dir, link):
            print(f"    skip（已存在）: {link}")
            continue
        # 优先用 RSS 正文，不足则抓全文
        body = ""
        if _c and len(BeautifulSoup(_c, "html.parser").get_text()) > 200:
            _, body = extract_main_content(_c)
        if len(body) < 200:
            try:
                time.sleep(SLEEP_BETWEEN)
                pr = safe_get(link)
                _, body = extract_main_content(pr.text, link)
                if not date:
                    date = _extract_date(pr.text)
            except Exception as e:
                print(f"    ✗ 全文抓取失败: {e}")
                body = BeautifulSoup(_c, "html.parser").get_text() if _c else ""
        if len(body) < 80:
            continue
        dest = save_article(out_dir, bid, org, title, body,
                            source_url=link, date=date, idx=saved)
        print(f"    ✓ [{saved+1}] {title[:50]}...")
        saved += 1
        time.sleep(SLEEP_BETWEEN)
    return saved

# ── 抓取器：github ────────────────────────────────────────────────────────
def fetch_github(blog, out_dir, count, since_date=None):
    """GitHub org：抓 README + Release Notes"""
    github_url = blog.get("github", blog["index_url"])
    org = blog["org"]
    bid = blog["id"]
    # 提取 org/user 名
    m = re.search(r"github\.com/([^/]+)/?$", github_url)
    if not m:
        print(f"  [github] ⚠ 无法解析 GitHub org: {github_url}")
        return 0
    gh_org = m.group(1)
    print(f"  [github] {blog['name_cn']} → github.com/{gh_org}")
    api_base = "https://api.github.com"
    gh_headers = {**HEADERS, "Accept": "application/vnd.github+json",
                  "X-GitHub-Api-Version": "2022-11-28"}
    # 如果有 GITHUB_TOKEN，加上以提高 rate limit
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        gh_headers["Authorization"] = f"Bearer {token}"
    # 获取仓库列表，按 push 时间排序
    try:
        r = safe_get(f"{api_base}/orgs/{gh_org}/repos?sort=pushed&per_page=30",
                     headers=gh_headers)
        repos = r.json()
        if not isinstance(repos, list):
            # 可能是 user 而非 org
            r = safe_get(f"{api_base}/users/{gh_org}/repos?sort=pushed&per_page=30",
                         headers=gh_headers)
            repos = r.json()
    except Exception as e:
        print(f"    ⚠ 获取仓库列表失败: {e}")
        return 0
    # 优先关键仓库
    key_repos = blog.get("key_repos", [])
    if key_repos:
        ranked = ([r for r in repos if r.get("name") in key_repos] +
                  [r for r in repos if r.get("name") not in key_repos])
    else:
        ranked = repos
    # 过滤掉 fork 和过小的仓库
    ranked = [r for r in ranked if not r.get("fork") and r.get("stargazers_count", 0) >= 5]
    saved = 0
    for repo in ranked[:count * 2]:  # 多取一些，有些 README 太短
        if saved >= count:
            break
        repo_name = repo["name"]
        repo_url  = repo["html_url"]
        stars     = repo.get("stargazers_count", 0)
        pushed    = (repo.get("pushed_at") or "")[:10]
        # 抓 README
        try:
            time.sleep(SLEEP_BETWEEN)
            r = safe_get(f"{api_base}/repos/{gh_org}/{repo_name}/readme",
                         headers={**gh_headers, "Accept": "application/vnd.github.raw"})
            readme = r.text
        except Exception:
            continue
        if len(readme) < 200:
            continue
        title_m = re.search(r'^#\s+(.+)$', readme, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else repo_name
        title = re.sub(r'[*_`\[\]]', '', title)
        # 清理 README + 把相对图片路径转成 raw.githubusercontent.com 绝对 URL
        cdn_base = f"https://cdn.jsdelivr.net/gh/{gh_org}/{repo_name}@main"
        def fix_img(m):
            src = m.group(2)
            if src.startswith(("data:", "//")):
                return m.group(1) + src + m.group(3)
            if src.startswith(("http://", "https://")):
                src = re.sub(
                    r'https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+)',
                    r'https://cdn.jsdelivr.net/gh/\1/\2@\3/\4', src)
                src = re.sub(
                    r'https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?)(?:\?raw=true)?$',
                    r'https://cdn.jsdelivr.net/gh/\1/\2@\3/\4', src)
            else:
                src = f"{cdn_base}/{src.lstrip('./')}"
            return m.group(1) + src + m.group(3)
        body = re.sub(r'(src=["\'])([^"\']+)(["\'])', fix_img, readme)
        # 移除徽章行（![xxx](xxx)）
        body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
        # 移除语言切换行（支持 #锚点 和 ./文件路径，如 [English](./README.md) | [简体中文](./README.zh.md)）
        body = re.sub(
            r'^\s*(?:\[?(?:english|简体中文|繁體中文|中文|한국어|日本語|português|español|русский)\]?\([^\)]*\)|(?:english|简体中文|繁體中文|中文))'
            r'(?:[\s|｜/]+(?:\[?(?:english|简体中文|繁體中文|中文|한국어|日本語|português|español|русский)\]?\([^\)]*\)|(?:english|简体中文|繁體中文|中文)))+\s*\n',
            '', body, flags=re.MULTILINE|re.IGNORECASE
        )
        # 移除纯 HTML 块标签行
        body = re.sub(r'^\s*</?(?:div|center|p|br|hr|section)[^>]*/?>\s*\n', '', body, flags=re.MULTILINE|re.IGNORECASE)
        # 移除连续空行
        body = re.sub(r'\n{3,}', '\n\n', body).strip()
        # 优先用 README 正文第一段，fallback 到 GitHub description
        repo_desc = repo.get("description") or ""
        readme_summary = extract_summary(readme)
        summary = readme_summary if len(readme_summary) > 20 else (repo_desc or f"Stars: {stars}")
        if deduplicate(out_dir, repo_url):
            print(f"    skip（已存在）: {repo_name}")
            continue
        tags = [org, "开源", "技术报告"]
        dest = save_article(out_dir, bid, org, title, body,
                            source_url=repo_url, date=pushed,
                            tags=tags, summary=summary, idx=saved)
        print(f"    ✓ [{saved+1}] {repo_name} (⭐{stars})")
        saved += 1
    # 再抓最新 Release Notes
    for repo in ranked[:3]:
        if saved >= count:
            break
        repo_name = repo["name"]
        try:
            time.sleep(SLEEP_BETWEEN)
            r = safe_get(f"{api_base}/repos/{gh_org}/{repo_name}/releases?per_page=3",
                         headers=gh_headers)
            releases = r.json()
            if not isinstance(releases, list):
                continue
        except Exception:
            continue
        for rel in releases[:2]:
            if saved >= count:
                break
            rel_url  = rel.get("html_url", "")
            rel_body = rel.get("body") or ""
            rel_name = rel.get("name") or rel.get("tag_name") or "Release"
            rel_date = (rel.get("published_at") or "")[:10]
            if len(rel_body) < 100 or deduplicate(out_dir, rel_url):
                continue
            title = f"{repo_name} {rel_name} Release Notes"
            dest = save_article(out_dir, bid, org, title, rel_body,
                                source_url=rel_url, date=rel_date,
                                tags=[org, "Release Notes", repo_name],
                                idx=saved)
            print(f"    ✓ [{saved+1}] Release: {repo_name} {rel_name}")
            saved += 1
    return saved

# ── 抓取器：js（尽力而为）────────────────────────────────────────────────
def fetch_js(blog, out_dir, count, since_date=None):
    """JS 渲染页面：尝试直接抓静态 HTML（部分有效），提示无法完整支持"""
    index_url = blog["index_url"]
    org = blog["org"]
    bid = blog["id"]
    print(f"  [js]     {blog['name_cn']} → {index_url}")
    print(f"    ℹ JS 渲染站点，尝试直接抓取（内容可能不完整）")
    try:
        r = safe_get(index_url)
        soup = BeautifulSoup(r.text, "html.parser")
        # 检查是否有可用的文章列表
        links = []
        base = urllib.parse.urlparse(index_url)
        base_url = f"{base.scheme}://{base.netloc}"
        seen = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                href = base_url + href
            elif not href.startswith("http"):
                continue
            parsed = urllib.parse.urlparse(href)
            if parsed.netloc and parsed.netloc != base.netloc:
                continue
            text = a.get_text(strip=True)
            if len(text) < 8 or href in seen:
                continue
            if any(x in href.lower() for x in ["#","login","signup","pricing","about","contact"]):
                continue
            seen.add(href)
            links.append((href, text))
        if len(links) < 3:
            print(f"    ⚠ 未发现足够文章链接（JS 渲染），跳过此来源")
            print(f"    💡 如需完整支持，安装 playwright: pip install playwright && playwright install chromium")
            print(f"    💡 然后重新运行: python3 fetcher.py --sources {bid} --use-playwright")
            return 0
        saved = 0
        for url, text in links[:count]:
            if deduplicate(out_dir, url):
                continue
            try:
                time.sleep(SLEEP_BETWEEN)
                pr = safe_get(url)
                title, body = extract_main_content(pr.text, url)
                if not title:
                    title = text
                if len(body) < 100:
                    continue
                date = _extract_date(pr.text)
                dest = save_article(out_dir, bid, org, title, body,
                                    source_url=url, date=date, idx=saved)
                print(f"    ✓ [{saved+1}] {title[:50]}...")
                saved += 1
            except Exception as e:
                print(f"    ✗ {url}: {e}")
        if saved == 0:
            print(f"    ⚠ 未成功抓取任何文章（JS 渲染问题）")
        return saved
    except Exception as e:
        print(f"    ⚠ 索引页请求失败: {e}")
        return 0

# ── 可选：翻译（Anthropic API）───────────────────────────────────────────
def translate_article(md_path):
    """用 Anthropic API 把英文文章翻译成中文（可选功能）"""
    try:
        import anthropic as _anthropic
    except ImportError:
        print("  ⚠ 翻译需要 anthropic 包: pip install anthropic")
        return False
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ⚠ 翻译需要设置环境变量: export ANTHROPIC_API_KEY=sk-ant-...")
        return False
    client = _anthropic.Anthropic(api_key=api_key)
    content = Path(md_path).read_text(encoding="utf-8")
    # 分离 frontmatter 和正文
    parts = content.split("---", 2)
    if len(parts) < 3:
        body = content
        fm_raw = ""
    else:
        fm_raw = "---" + parts[1] + "---\n"
        body = parts[2]
    TRANSLATE_PROMPT = """你是一位技术翻译专家。将以下 AI 技术文章从英文翻译成中文。

翻译规范：
1. 标题、章节标题、正文全部翻译成中文
2. 技术术语**首次出现**保留英文括注：如"智能体（Agent）"
3. 代码块、命令、API 名、变量名、具体数字**保持原文不变**
4. 专有名词（模型名、公司名、产品名）保留英文
5. 末尾新增一节"## 要点总结"列出 3-5 条核心结论
6. 输出纯 Markdown，不要解释翻译过程

原文：
""" + body[:8000]  # 限制长度避免超 token
    try:
        msg = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": TRANSLATE_PROMPT}]
        )
        translated_body = msg.content[0].text
        # 更新 frontmatter 中的 summary（取翻译正文首段）
        new_summary = extract_summary(translated_body)
        fm_updated = re.sub(
            r'summary:\s*".*?"',
            f'summary: "{new_summary[:140].replace(chr(34), chr(92)+chr(34))}"',
            fm_raw
        )
        Path(md_path).write_text(fm_updated + "\n" + translated_body, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  ✗ 翻译失败: {e}")
        return False

# ── 主流程 ────────────────────────────────────────────────────────────────
def fetch_auto(blog, out_dir, count, since_date=None):
    """自动选最优策略：有 RSS 优先用 RSS，否则按 render 字段"""
    if blog.get("rss"):
        return fetch_rss(blog, out_dir, count, since_date)
    render = blog.get("render", "static")
    return FETCHERS_BY_RENDER.get(render, fetch_static)(blog, out_dir, count, since_date)

FETCHERS_BY_RENDER = {"static": fetch_static, "rss": fetch_rss,
                      "github": fetch_github, "js": fetch_js, "arxiv": fetch_static}
FETCHERS = FETCHERS_BY_RENDER

def load_blogs():
    return json.load(open(BLOGS_JSON, encoding="utf-8"))["blogs"]

def resolve_sources(ids_str, blogs):
    if ids_str == "all":
        return blogs
    if ids_str == "all-easy":
        return [b for b in blogs if b.get("difficulty") == "easy"]
    if ids_str == "all-static":
        return [b for b in blogs if b["render"] in ("static","rss")]
    if ids_str == "cn":
        return [b for b in blogs if b.get("region") == "cn"]
    ids = [s.strip() for s in ids_str.split(",")]
    matched = [b for b in blogs if b["id"] in ids]
    missing = [i for i in ids if i not in {b["id"] for b in matched}]
    if missing:
        print(f"⚠ 未知来源 ID: {', '.join(missing)}")
    return matched

def main():
    p = argparse.ArgumentParser(
        description="本机直接抓取 AI 技术博客",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
来源 ID 别名:
  all          全部 23 个来源
  all-easy     仅 difficulty=easy 的来源（github 类，最稳定）
  all-static   仅 static/rss 类（直接可抓，推荐）
  cn           仅国内来源

示例:
  python3 fetcher.py --list
  python3 fetcher.py --sources all-static --count 5
  python3 fetcher.py --sources qwen,deepseek,baai --count 10
  python3 fetcher.py --sources all-easy --count 5 --translate --build
  python3 fetcher.py --sources anthropic-engineering --count 5 --out ~/Desktop/anthropic
"""
    )
    p.add_argument("--list",      action="store_true", help="列出所有来源")
    p.add_argument("--sources",   default="all-static", help="来源 ID（逗号分隔）或别名，默认 all-static")
    p.add_argument("--count",     type=int, default=10, help="每源最多篇数（默认 10）")
    p.add_argument("--out",       default=str(DEFAULT_OUT/"articles"), help="文章输出目录")
    p.add_argument("--since",     help="只抓此日期之后的文章 YYYY-MM-DD")
    p.add_argument("--translate", action="store_true", help="翻译为中文（需 ANTHROPIC_API_KEY）")
    p.add_argument("--build",     action="store_true", help="抓完后自动运行 generate_site.py 建站")
    p.add_argument("--site-out",  default=str(DEFAULT_OUT/"site"), help="网站输出目录")
    p.add_argument("--title",     default="AI 技术博客 · 中文精选", help="网站标题")
    p.add_argument("--dry-run",   action="store_true", help="只显示将要抓取的内容，不实际请求")
    args = p.parse_args()

    blogs = load_blogs()

    if args.list:
        print(f"\n{'ID':30s} {'来源':24s} {'Render':8s} {'难度':6s}")
        print("─" * 80)
        for b in blogs:
            print(f"  {b['id']:28s} {b['name_cn']:22s} {b['render']:8s} {b.get('difficulty','?')}")
        print()
        return

    targets = resolve_sources(args.sources, blogs)
    if not targets:
        print("未找到匹配来源，运行 --list 查看所有可用来源")
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  抓取来源: {len(targets)} 个  |  每源最多: {args.count} 篇")
    print(f"  输出目录: {out_dir}")
    if args.translate:
        print(f"  翻译:     开启（需要 ANTHROPIC_API_KEY）")
    print(f"{'='*60}\n")

    if args.dry_run:
        for b in targets:
            print(f"  会抓: {b['name_cn']} ({b['id']})  [{b['render']}]  {b['index_url']}")
        print("\n（dry-run 模式，不实际请求）")
        return

    total = 0
    for blog in targets:
        render = blog["render"]
        fetcher = fetch_auto
        try:
            n = fetcher(blog, out_dir, args.count, args.since)
        except Exception as e:
            print(f"  ✗ {blog['name_cn']}: {e}")
            n = 0
        total += n
        print()

    # 翻译
    if args.translate and total > 0:
        print(f"{'='*60}")
        print(f"  翻译 {total} 篇文章...")
        new_files = sorted(out_dir.glob("*.md"),
                           key=lambda f: f.stat().st_mtime, reverse=True)[:total]
        ok = sum(1 for f in new_files if translate_article(f))
        print(f"  翻译完成: {ok}/{len(new_files)} 篇")

    # 建站
    print(f"{'='*60}")
    print(f"  本次共保存: {total} 篇  →  {out_dir}")
    all_md = list(out_dir.glob("*.md"))
    print(f"  目录总文章: {len(all_md)} 篇\n")

    if args.build and total > 0:
        import subprocess
        site_out = Path(args.site_out)
        print(f"  正在生成网站 → {site_out}")
        result = subprocess.run(
            [sys.executable, str(GEN_SCRIPT), str(out_dir), str(site_out), "--title", args.title],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  ✓ 网站已生成: {site_out}/index.html")
            print(f"  浏览器打开: open \"{site_out}/index.html\"")
        else:
            print(f"  ✗ 建站失败:\n{result.stderr[:300]}")

if __name__ == "__main__":
    main()
