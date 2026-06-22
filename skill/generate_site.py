# -*- coding: utf-8 -*-
"""把一批（已翻译为中文的）AI 技术博客 Markdown 文章，生成一个可离线浏览的中文学习网站。

用法：
    python3 generate_site.py [articles_dir] [out_dir] [--title "站点标题"]

- articles_dir：存放 .md 文章的目录（默认 ./examples/articles）
- out_dir：输出网站目录（默认 ./examples/site）

每篇 .md 可带 YAML frontmatter（均可选）：
    ---
    title: 文章中文标题
    org: Anthropic            # 来源机构，用于分组与配色
    date: 2025-11-26
    source_url: https://...   # 原文链接
    tags: [Agent, 上下文工程]  # 标签，逗号分隔或 [] 列表
    summary: 一句话中文摘要
    ---
    正文（中文 Markdown）...

无 frontmatter 时：标题取首个 # 一级标题，其余字段留空。
产出：index.html（学习首页：搜索/按来源筛选/已读标记/阅读时长）+ articles/<id>.html（阅读页：目录/上一篇下一篇/原文链接）。
纯静态、零依赖、可直接用浏览器打开（file://）。
"""
import os, re, sys, json, html

# ── 机构配色（品牌色，找不到则用默认）────────────────────────────────────────
ORG_COLORS = [
    ("anthropic", "#D97757"), ("openai", "#10A37F"), ("deepmind", "#4285F4"),
    ("google", "#4285F4"), ("meta", "#0064E0"), ("microsoft", "#0A84FF"),
    ("mistral", "#FF7000"), ("hugging", "#FF9D00"), ("nvidia", "#76B900"),
    ("qwen", "#615CED"), ("阿里", "#615CED"), ("deepseek", "#4D6BFE"),
    ("智谱", "#3859FF"), ("zhipu", "#3859FF"), ("glm", "#3859FF"),
    ("moonshot", "#16213E"), ("kimi", "#16213E"), ("月之暗面", "#16213E"),
    ("字节", "#325AB4"), ("bytedance", "#325AB4"), ("豆包", "#325AB4"),
    ("腾讯", "#0052D9"), ("tencent", "#0052D9"), ("混元", "#0052D9"),
    ("百度", "#2932E1"), ("baidu", "#2932E1"), ("ernie", "#2932E1"),
    ("minimax", "#E1341E"),
]
DEFAULT_COLOR = "#64748B"

def org_color(org):
    o = (org or "").lower()
    for key, col in ORG_COLORS:
        if key in o:
            return col
    return DEFAULT_COLOR

def esc(s):
    return html.escape(s, quote=True)

def inline_md(s):
    """把摘要文本中的 Markdown inline 语法转为 HTML（先 esc 再替换）"""
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         s)
    s = re.sub(r'`(.+?)`',       r'<code>\1</code>',     s)
    return s

def slugify(name):
    s = re.sub(r"[^\w一-鿿]+", "-", name.strip().lower()).strip("-")
    return s or "article"

# ── frontmatter ─────────────────────────────────────────────────────────────
def _unquote(s):
    """剥掉配对的外层引号，不影响值内部的引号。"""
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s

def parse_frontmatter(text):
    meta = {}
    body = text
    if text.lstrip().startswith("---"):
        t = text.lstrip()
        end = t.find("\n---", 3)
        if end != -1:
            fm = t[3:end].strip("\n")
            body = t[end + 4:].lstrip("\n")
            pending_list_key = None
            for ln in fm.split("\n"):
                # YAML 块列表项：  - value
                if ln.lstrip().startswith("- ") and pending_list_key:
                    meta[pending_list_key].append(_unquote(ln.lstrip()[2:]))
                    continue
                pending_list_key = None
                if ":" not in ln:
                    continue
                k, v = ln.split(":", 1)
                k, v = k.strip(), v.strip()
                if k == "tags":
                    if v.startswith("["):
                        # 行内列表：[Agent, "上下文工程"]
                        v = v.strip("[]")
                        meta[k] = [_unquote(x) for x in v.split(",") if x.strip()]
                    elif v == "":
                        # 块列表：tags:\n  - Agent
                        meta[k] = []
                        pending_list_key = "tags"
                    else:
                        meta[k] = [_unquote(x) for x in v.split(",") if x.strip()]
                else:
                    meta[k] = _unquote(v)
    return meta, body

# ── 极简 Markdown → HTML（零依赖，覆盖博客常见语法）─────────────────────────
_HTML_TAG_RE = re.compile(r'(<!--[\s\S]*?-->|<[a-zA-Z/!][^>]*?>)', re.DOTALL)
_BLOCKED_TAGS = re.compile(r'^<(?:script|iframe|style|form|object|embed|base|meta|link)', re.I)

def _inline(s):
    """Markdown 行内转换：文本部分 HTML 转义，HTML 标签直通（安全标签）"""
    # 将字符串按 HTML 标签分割，对文本部分 esc，对标签部分直通（过滤危险标签）
    parts = _HTML_TAG_RE.split(s)
    out_parts = []
    for p in parts:
        if _HTML_TAG_RE.match(p):
            # 过滤危险标签，其余直通；img 加载失败时自动隐藏
            if not _BLOCKED_TAGS.match(p):
                if re.match(r'<img\b', p, re.I) and 'onerror' not in p:
                    p = re.sub(r'(/??>)$', " onerror=\"this.style.display='none'\">", p)
                out_parts.append(p)
        else:
            out_parts.append(esc(p))
    s = ''.join(out_parts)
    # Markdown 内联格式（在转义后的文本部分应用）
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)",
               lambda m: f'<img alt="{esc(m.group(1))}" src="{m.group(2)}" loading="lazy" onerror="this.style.display=\'none\'">',
               s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

_BLOCK_START = re.compile(r"^(#{1,6}\s|```|>|\s*[-*+]\s|\s*\d+\.\s)")
_HR = re.compile(r"^(\*{3,}|-{3,}|_{3,})$")
# 语言切换行（GitHub README 常见，支持 #锚点 和 ./文件路径 两种形式）
_LANG_NAMES = r"english|简体中文|繁體中文|中文|한국어|日本語|português|español|deutsch|français|русский|العربية"
_LANG_LINK  = rf"\[?(?:{_LANG_NAMES})\]?\([^\)]*\)"  # [英文名](任意路径)
_LANG_PLAIN = rf"(?:{_LANG_NAMES})"                   # 无括号的裸文本
_LANG_SEP   = r"[\s|｜/\\]+"
_LANG_SWITCH = re.compile(
    rf"^\s*(?:{_LANG_LINK}|{_LANG_PLAIN})(?:{_LANG_SEP}(?:{_LANG_LINK}|{_LANG_PLAIN}))+\s*$",
    re.I
)

def md_to_html(md):
    lines = md.split("\n")
    out, toc = [], []
    used = {}
    i, n = 0, len(lines)

    def mkid(text):
        s = slugify(text)
        if s in used:
            used[s] += 1
            s = f"{s}-{used[s]}"
        else:
            used[s] = 0
        return s

    while i < n:
        line = lines[i]
        # 原生 HTML 块直通：行以 < 标签开头，收集整块，sanitize 后原样输出
        if re.match(r'^\s*<[a-zA-Z!]', line) and not line.strip().startswith('<!--'):
            buf = [line]; i += 1
            # 收集直到空行（HTML 块结束）
            while i < n and lines[i].strip():
                # 如果遇到 Markdown 标题/引用/代码围栏，停止收集
                if re.match(r'^#{1,6}\s|^```|^>', lines[i]):
                    break
                buf.append(lines[i]); i += 1
            raw = '\n'.join(buf)
            # 安全清理：移除事件处理器和危险标签
            raw = re.sub(r'\s+on\w+="[^"]*"', '', raw, flags=re.I)
            raw = re.sub(r'<script[\s\S]*?</script>', '', raw, flags=re.I)
            raw = re.sub(r'<iframe[\s\S]*?</iframe>', '', raw, flags=re.I)
            # img 加载失败时自动隐藏
            raw = re.sub(r'(<img\b(?![^>]*onerror)[^>]*?)(/??>)',
                         r"""\1 onerror="this.style.display='none'"\2""", raw, flags=re.I)
            out.append(raw)
            continue
        # 跳过语言切换锚链接行（GitHub README 中 [English](#) | [简体中文](#)）
        if _LANG_SWITCH.match(line):
            i += 1; continue
        # 代码块
        if line.startswith("```"):
            lang = line[3:].strip()
            buf = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append(f'<pre><code class="lang-{esc(lang)}">{esc(chr(10).join(buf))}</code></pre>')
            continue
        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lv, txt = len(m.group(1)), m.group(2).strip()
            sid = mkid(txt)
            if lv in (2, 3):
                toc.append((lv, txt, sid))
            out.append(f'<h{lv} id="{sid}">{_inline(txt)}</h{lv}>')
            i += 1; continue
        # 分割线
        if _HR.match(line.strip()):
            out.append("<hr>"); i += 1; continue
        # 引用
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i][1:].lstrip()); i += 1
            out.append(f"<blockquote>{_inline(' '.join(buf))}</blockquote>")
            continue
        # 表格
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            th = "".join(f"<th>{_inline(c)}</th>" for c in header)
            trs = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>")
            continue
        # 无序列表
        if re.match(r"^\s*[-*+]\s+", line):
            buf = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                buf.append(re.sub(r"^\s*[-*+]\s+", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in buf) + "</ul>")
            continue
        # 有序列表
        if re.match(r"^\s*\d+\.\s+", line):
            buf = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                buf.append(re.sub(r"^\s*\d+\.\s+", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{_inline(x)}</li>" for x in buf) + "</ol>")
            continue
        # 空行
        if not line.strip():
            i += 1; continue
        # 段落
        buf = [line]; i += 1
        while i < n and lines[i].strip() and not _BLOCK_START.match(lines[i]) and not _HR.match(lines[i].strip()):
            buf.append(lines[i]); i += 1
        out.append(f"<p>{_inline(' '.join(buf))}</p>")
    return "\n".join(out), toc

def fix_github_img_urls(text, source_url):
    """把 GitHub 来源文章中的相对/blob 图片路径转为 jsDelivr CDN URL（国内访问快）
    raw.githubusercontent.com 在国内 ~20s，jsDelivr 在国内 ~1s。
    格式：https://cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/{path}
    """
    if not source_url or "github.com" not in source_url:
        return text
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:/|$)", source_url)
    if not m:
        return text
    owner, repo = m.group(1), m.group(2).rstrip(".git")
    cdn_base = f"https://cdn.jsdelivr.net/gh/{owner}/{repo}@main"

    def rewrite_src(src):
        src = src.strip()
        if src.startswith(("data:", "//")):
            return src
        if src.startswith(("http://", "https://")):
            # raw.githubusercontent.com → jsDelivr
            src = re.sub(
                r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+)",
                r"https://cdn.jsdelivr.net/gh/\1/\2@\3/\4",
                src
            )
            # GitHub blob URL → jsDelivr
            src = re.sub(
                r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?)(?:\?raw=true)?$",
                r"https://cdn.jsdelivr.net/gh/\1/\2@\3/\4",
                src
            )
            return src
        # 相对路径 → jsDelivr
        clean = src.lstrip("./")
        return f"{cdn_base}/{clean}"

    def sub_src(m):
        return m.group(1) + rewrite_src(m.group(2)) + m.group(3)

    text = re.sub(r'(src=["\'])([^"\']+)(["\'])', sub_src, text)
    return text

def reading_minutes(text):
    cjk = len(re.findall(r"[一-鿿]", text))
    words = len(re.findall(r"[A-Za-z0-9]+", text))
    return max(1, round(cjk / 400 + words / 220))

# ── 加载文章 ─────────────────────────────────────────────────────────────────
def load_articles(src_dir):
    arts = []
    for fn in sorted(os.listdir(src_dir)):
        if not fn.endswith(".md"):
            continue
        raw = open(os.path.join(src_dir, fn), encoding="utf-8").read()
        meta, body = parse_frontmatter(raw)
        # 剥离正文首个一级标题，避免与阅读页标题重复；无 frontmatter 标题时用它
        h1 = re.search(r"^#\s+(.+)$", body, flags=re.M)
        h1_text = h1.group(1).strip() if h1 else ""
        if h1:
            body = (body[:h1.start()] + body[h1.end():]).lstrip("\n")
        title = meta.get("title") or h1_text or os.path.splitext(fn)[0]
        summary_zh = meta.get("summary_zh", "")
        summary_en = meta.get("summary_en", "")
        summary    = meta.get("summary", "")
        # 兼容旧格式：只有 summary 字段时，根据内容语言分配
        if summary and not summary_zh and not summary_en:
            cjk = len(re.findall(r"[一-鿿]", summary))
            if cjk > len(summary) * 0.2:
                summary_zh = summary
            else:
                summary_en = summary
        # 自动从正文补充缺失的摘要
        if not summary_zh and not summary_en:
            for para in re.split(r"\n\s*\n", body):
                p = para.strip()
                if p and not p.startswith(("#", "`", ">", "-", "*", "|")):
                    t = re.sub(r"\s+", " ", p)[:120]
                    cjk = len(re.findall(r"[一-鿿]", t))
                    if cjk > len(t) * 0.2:
                        summary_zh = t
                    else:
                        summary_en = t
                    break
        # 首页卡片摘要：优先中文
        summary = summary_zh or summary_en or summary
        source_url = meta.get("source_url", "")
        # 修正 GitHub 来源文章中的相对/blob 图片路径
        body = fix_github_img_urls(body, source_url)
        body_html, toc = md_to_html(body)
        arts.append({
            "id": slugify(os.path.splitext(fn)[0]),
            "title": title,
            "org": meta.get("org", ""),
            "date": meta.get("date", ""),
            "source_url": meta.get("source_url", ""),
            "tags": meta.get("tags", []) if isinstance(meta.get("tags"), list) else [],
            "summary": summary,
            "summary_zh": summary_zh,
            "summary_en": summary_en,
            "minutes": reading_minutes(body),
            "body_html": body_html,
            "toc": toc,
        })
    arts.sort(key=lambda a: (a["date"] or "0000"), reverse=True)
    return arts

# ── 页面模板 ─────────────────────────────────────────────────────────────────
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;'
         '1,9..144,400&family=Noto+Serif+SC:wght@500;600;700&'
         'family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">')

# SVG icon helpers (no emoji)
ICON_SEARCH = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
ICON_CLOCK  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
ICON_CAL    = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
ICON_LINK   = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
ICON_CHECK  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_BACK   = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>'

CSS = """
@media(prefers-reduced-motion:reduce){*{transition-duration:.01ms!important;animation-duration:.01ms!important}}
*{margin:0;padding:0;box-sizing:border-box}

/* ─────────────────────────────────────────────
   Anthropic Brand Design Tokens
   Warm Minimalism: parchment bg + clay orange accent
   ───────────────────────────────────────────── */
:root{
  /* Core palette */
  --bg:#F0EEE6;          /* warm parchment — Anthropic page background */
  --surface:#FAFAF7;     /* off-white card surface */
  --surface-2:#E8E5DB;   /* subtle warm fill, tags, code bg */
  --ink:#191919;         /* near-black primary text */
  --ink-2:#3D3B33;       /* body text, slightly warm */
  --muted:#6B6B63;       /* secondary / caption text */
  --line:#DBD7CC;        /* dividers & borders */
  --line-2:#C8C4B8;      /* stronger divider on hover */

  /* Accent — Anthropic clay orange */
  --accent:#D97757;
  --accent-hover:#C15F3C;
  --accent-soft:rgba(217,119,87,.10);

  /* Semantic */
  --success:#3D8B5E;
  --code-bg:#ECEAE0;

  /* Elevation */
  --shadow-sm:0 1px 3px rgba(25,20,10,.07),0 1px 2px rgba(25,20,10,.04);
  --shadow-md:0 4px 18px rgba(25,20,10,.09),0 2px 6px rgba(25,20,10,.05);

  /* Shape */
  --radius:12px;--radius-sm:8px;--radius-pill:999px;

  /* Typography */
  --font-serif:'Fraunces','Noto Serif SC',Georgia,serif;
  --font-sans:'Inter','PingFang SC','Microsoft YaHei',sans-serif;
}

html{scroll-behavior:smooth;font-size:16px}
body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;line-height:1.6}
a{color:var(--accent);text-decoration:none;cursor:pointer}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}

/* ── Layout ── */
.container{max-width:1200px;margin:0 auto;padding:0 clamp(16px,4vw,32px)}

/* ── Hero — dot-grid texture background ── */
.hero{background:var(--bg);border-bottom:1px solid var(--line);position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle,rgba(25,20,10,.12) 1px,transparent 1px);
  background-size:18px 18px;opacity:.45}
.hero-in{max-width:1200px;margin:0 auto;position:relative;z-index:1;
  padding:clamp(48px,7vw,84px) clamp(16px,4vw,32px) clamp(36px,5vw,60px)}
.hero-eyebrow{font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;
  color:var(--muted);margin-bottom:16px;display:flex;align-items:center;gap:10px}
.hero-eyebrow::after{content:'';flex:none;width:28px;height:2px;background:var(--accent);border-radius:2px}
.hero h1{font-family:var(--font-serif);font-size:clamp(34px,5.5vw,58px);
  font-weight:900;letter-spacing:-.03em;line-height:1.08;color:var(--ink)}
.hero h1 .dot{color:var(--accent)}
.hero-desc{color:var(--muted);margin-top:18px;font-size:clamp(14px,2vw,16px);
  max-width:560px;line-height:1.8;font-weight:300}
.stats{display:flex;gap:clamp(24px,5vw,48px);margin-top:clamp(28px,4vw,40px);flex-wrap:wrap}
.stat{display:flex;flex-direction:column;gap:3px}
.stat b{font-family:var(--font-serif);font-size:clamp(24px,3.5vw,34px);
  font-weight:700;color:var(--ink);letter-spacing:-.02em}
.stat span{font-size:11px;color:var(--muted);font-weight:600;letter-spacing:.08em;text-transform:uppercase}

/* ── Sticky controls ── */
.controls{position:sticky;top:0;z-index:40;
  background:rgba(240,238,230,.93);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid var(--line);padding:12px 0}
.ctrl-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.search-wrap{position:relative;flex:1;min-width:200px;max-width:380px}
.search-wrap .ico{position:absolute;left:12px;top:50%;transform:translateY(-50%);
  color:var(--muted);pointer-events:none;display:flex}
.search{width:100%;padding:10px 14px 10px 38px;border:1.5px solid var(--line);
  border-radius:var(--radius-sm);font-size:14px;font-family:var(--font-sans);
  background:var(--surface);color:var(--ink);transition:border-color .15s,box-shadow .15s}
.search:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.search::placeholder{color:var(--muted)}
/* 两行筛选区 */
.filter-rows{display:flex;flex-direction:column;gap:8px;margin-top:10px}
/* label 固定左侧，chips 独立换行 */
.filter-row{display:flex;align-items:flex-start;gap:8px}
.filter-label{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);white-space:nowrap;min-width:52px;padding-top:7px;flex-shrink:0}
.chips{display:flex;gap:6px;flex-wrap:wrap;align-items:center;flex:1}
.chip{padding:5px 13px;border:1.5px solid var(--line);border-radius:var(--radius-pill);
  font-size:12.5px;font-weight:600;font-family:var(--font-sans);letter-spacing:.01em;
  color:var(--muted);background:var(--surface);cursor:pointer;
  transition:all .15s ease;white-space:nowrap;user-select:none}
.chip:hover{border-color:var(--accent);color:var(--accent)}
.chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.chip.active{background:var(--ink);color:#F0EEE6;border-color:var(--ink)}
/* 话题类 chip 用稍淡的样式区分 */
.chip.topic{border-style:dashed}
.chip.topic.active{background:var(--accent);border-color:var(--accent);border-style:solid}

/* ── Card grid ── */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
  gap:clamp(12px,2vw,18px);padding:clamp(20px,3vw,32px) 0 clamp(60px,8vw,96px)}
.card{background:var(--surface);border:1.5px solid var(--line);border-radius:var(--radius);
  padding:22px;display:flex;flex-direction:column;position:relative;
  transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;cursor:pointer}
.card:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);border-color:var(--line-2)}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.badge{display:inline-flex;align-items:center;font-size:10.5px;font-weight:700;
  letter-spacing:.05em;color:#fff;padding:3px 9px;border-radius:var(--radius-pill);text-transform:uppercase}
.card-date{font-size:11.5px;color:var(--muted);font-weight:400}
.card h3{font-size:16.5px;font-weight:700;line-height:1.4;margin-bottom:10px;letter-spacing:-.01em}
.card h3 a{color:var(--ink);transition:color .15s}
.card h3 a:hover{color:var(--accent)}
/* 整张卡片可点击：伪元素覆盖整个 card（card 已有 position:relative）*/
.card h3 a::after{content:'';position:absolute;inset:0;z-index:1}
/* 卡片内其他链接（标签、徽章等）需高于覆盖层才能独立点击 */
.card .badge,.card .tags,.card .rt{position:relative;z-index:2}
.card .sum{font-size:13px;color:var(--muted);line-height:1.75;flex:1;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card-foot{display:flex;justify-content:space-between;align-items:center;
  margin-top:16px;padding-top:14px;border-top:1px solid var(--line);gap:8px}
.tags{display:flex;gap:5px;flex-wrap:wrap;flex:1;min-width:0}
.tag{font-size:10.5px;font-weight:600;color:var(--muted);background:var(--surface-2);
  padding:2px 7px;border-radius:4px;white-space:nowrap;letter-spacing:.02em}
.rt{font-size:11.5px;color:var(--muted);white-space:nowrap;
  display:flex;align-items:center;gap:4px;flex-shrink:0}
.readdot{position:absolute;top:16px;right:16px;width:7px;height:7px;border-radius:50%;
  background:var(--success);display:none;box-shadow:0 0 0 2.5px rgba(61,139,94,.2)}
.card.read .readdot{display:block}
.card.read{opacity:.6}
.empty{text-align:center;color:var(--muted);padding:72px 0;font-size:15px}
.empty strong{display:block;font-family:var(--font-serif);font-size:28px;
  font-weight:700;color:var(--line-2);margin-bottom:8px}

/* ── Article page navbar ── */
.abar{position:sticky;top:0;z-index:40;
  background:rgba(240,238,230,.93);backdrop-filter:blur(14px);
  -webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.abar-in{max-width:1200px;margin:0 auto;padding:12px clamp(16px,4vw,32px);
  display:flex;align-items:center;gap:12px}
.back{font-size:13px;font-weight:600;color:var(--muted);
  display:inline-flex;align-items:center;gap:5px;
  padding:6px 10px;border-radius:var(--radius-sm);transition:all .15s ease}
.back:hover{background:var(--surface-2);color:var(--ink)}
.abar .spacer{flex:1}
.btn{font-size:13px;font-weight:600;font-family:var(--font-sans);
  padding:7px 16px;border-radius:var(--radius-sm);
  border:1.5px solid var(--line);background:var(--surface);
  color:var(--ink);cursor:pointer;transition:all .15s ease;
  display:inline-flex;align-items:center;gap:6px}
.btn:hover{border-color:var(--line-2);background:var(--surface-2)}
.btn.done{background:var(--success);color:#fff;border-color:var(--success)}
.btn.done:hover{filter:brightness(.92)}

/* ── Article layout ── */
.alayout{display:grid;grid-template-columns:1fr 248px;gap:clamp(32px,5vw,64px);
  max-width:1200px;margin:0 auto;padding:clamp(28px,4vw,48px) clamp(16px,4vw,32px) 100px}
.article{min-width:0}
.ahead{margin-bottom:32px;padding-bottom:28px;border-bottom:1px solid var(--line)}
.ahead h1{font-family:var(--font-serif);font-size:clamp(26px,4vw,40px);
  font-weight:900;line-height:1.15;margin:14px 0 16px;letter-spacing:-.03em;color:var(--ink)}
.ahead .m{font-size:13px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.ahead .m svg{flex-shrink:0}
.ahead .m a{color:var(--accent);font-weight:600;display:inline-flex;align-items:center;gap:4px}
.ahead .m a:hover{color:var(--accent-hover)}
.ahead .m .tag{font-size:11px}

/* ── Prose ── */
.prose{font-size:16.5px;line-height:1.9;color:var(--ink-2)}
.prose h2{font-family:var(--font-serif);font-size:clamp(19px,2.5vw,24px);font-weight:700;
  margin:44px 0 16px;color:var(--ink);letter-spacing:-.02em;
  border-bottom:2px solid var(--line);padding-bottom:10px}
.prose h3{font-size:clamp(16px,2vw,19px);font-weight:700;margin:32px 0 12px;color:var(--ink)}
.prose h4{font-size:16px;font-weight:600;margin:24px 0 10px}
.prose p{margin:14px 0}
.prose ul,.prose ol{margin:14px 0;padding-left:24px}
.prose li{margin:6px 0;line-height:1.75}
.prose a{color:var(--accent);border-bottom:1px solid rgba(217,119,87,.3);
  transition:border-color .15s,color .15s}
.prose a:hover{color:var(--accent-hover);border-color:var(--accent-hover)}
.prose blockquote{border-left:3px solid var(--accent);background:var(--accent-soft);
  padding:14px 20px;margin:22px 0;border-radius:0 var(--radius-sm) var(--radius-sm) 0;
  color:var(--ink-2);font-style:normal}
.prose code{background:var(--code-bg);padding:2px 6px;border-radius:4px;
  font-size:.875em;font-family:'SF Mono','JetBrains Mono',Menlo,Consolas,monospace;
  color:var(--accent-hover);border:1px solid var(--line)}
.prose pre{background:#1C1917;color:#D6D3D1;padding:20px 22px;border-radius:var(--radius);
  overflow-x:auto;margin:22px 0;box-shadow:var(--shadow-sm)}
.prose pre code{background:none;padding:0;color:inherit;font-size:13.5px;line-height:1.65;border:none}
.prose img{max-width:100%;border-radius:var(--radius);margin:20px 0;
  box-shadow:var(--shadow-sm);border:1px solid var(--line)}
.prose table{border-collapse:collapse;width:100%;margin:22px 0;font-size:14px;
  border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.prose th,.prose td{border:1px solid var(--line);padding:10px 14px;text-align:left}
.prose th{background:var(--surface-2);font-weight:700;font-size:12.5px;
  color:var(--ink);letter-spacing:.04em;text-transform:uppercase}
.prose tr:hover td{background:var(--accent-soft)}
.prose hr{border:none;border-top:1px solid var(--line);margin:36px 0}

/* ── TOC ── */
.toc{position:sticky;top:72px;align-self:start;
  max-height:calc(100vh - 96px);overflow-y:auto;overflow-x:hidden;
  scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.toc .t{font-size:11px;font-weight:800;letter-spacing:.12em;
  color:var(--muted);text-transform:uppercase;margin-bottom:14px;
  display:flex;align-items:center;gap:8px}
.toc .t::after{content:'';flex:1;height:1px;background:var(--line)}
.toc a{display:block;color:var(--muted);padding:5px 8px 5px 12px;
  border-left:2px solid var(--line);line-height:1.5;font-size:13px;
  border-radius:0 4px 4px 0;transition:all .15s ease}
.toc a:hover{color:var(--accent);border-left-color:var(--accent);background:var(--accent-soft)}
.toc a.lv3{padding-left:24px;font-size:12px}

/* ── Summary card ── */
.summary-card{background:var(--accent-soft);border:1px solid rgba(217,119,87,.2);
  border-radius:var(--radius);padding:18px 20px;margin-bottom:28px}
.summary-card .sc-row{display:flex;gap:16px;flex-wrap:wrap}
.summary-card .sc-block{flex:1;min-width:200px}
.summary-card .sc-label{font-size:10.5px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:var(--accent-hover);margin-bottom:6px}
.summary-card .sc-text{font-size:14.5px;line-height:1.7;color:var(--ink-2)}
.summary-card .sc-divider{width:1px;background:rgba(217,119,87,.25);flex-shrink:0;align-self:stretch}
/* ── Source link button ── */
.source-btn{display:inline-flex;align-items:center;gap:7px;
  padding:9px 18px;border-radius:var(--radius-pill);
  background:var(--accent);color:#fff;font-size:13px;font-weight:700;
  letter-spacing:.02em;transition:background .15s,transform .15s;
  margin-top:16px;text-decoration:none}
.source-btn:hover{background:var(--accent-hover);transform:translateY(-1px);color:#fff}
.source-btn svg{flex-shrink:0}
/* ── Prev/Next nav ── */
.anav{display:flex;justify-content:space-between;gap:14px;
  margin-top:52px;padding-top:24px;border-top:1px solid var(--line)}
.anav a{flex:1;padding:16px 18px;border:1.5px solid var(--line);border-radius:var(--radius);
  background:var(--surface);transition:all .2s ease}
.anav a:hover{border-color:var(--accent);background:var(--accent-soft);box-shadow:var(--shadow-sm)}
.anav .lbl{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.anav .ti{font-size:14px;font-weight:600;color:var(--ink);margin-top:5px;line-height:1.4}
.anav .next{text-align:right}

/* ── Footer ── */
.foot{text-align:center;color:var(--muted);font-size:12px;
  padding:36px 0 56px;letter-spacing:.06em;text-transform:uppercase}

/* ── Responsive ── */
@media(max-width:1024px){.alayout{grid-template-columns:1fr;gap:0}.toc{display:none}}
@media(max-width:768px){
  .grid{grid-template-columns:1fr}
  .ctrl-row{flex-direction:column;align-items:stretch}
  .search-wrap{max-width:100%}
  .filter-row{flex-wrap:nowrap;overflow-x:auto;padding-bottom:2px;
    scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .filter-row::-webkit-scrollbar{display:none}
  .filter-label{display:none}
  .chips{flex-wrap:nowrap}
  .ahead h1{font-size:26px}
  .anav{flex-direction:column}
}
@media(max-width:480px){.stats{gap:20px}.card{padding:18px}}
"""

def page(title, body, css_extra=""):
    return (f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title>{FONTS}<style>{CSS}{css_extra}</style></head><body>{body}</body></html>')

def render_graph(arts, site_title):
    """生成全局知识图谱页 graph.html"""
    ORG_COLOR_MAP = {
        "Anthropic": "#D97757", "OpenAI": "#10A37F", "Google DeepMind": "#4285F4",
        "Meta (FAIR)": "#0064E0", "Microsoft": "#0A84FF", "Mistral AI": "#FF7000",
        "Hugging Face": "#FF9D00", "阿里巴巴": "#615CED", "DeepSeek": "#4D6BFE",
        "智谱 AI": "#3859FF", "Moonshot AI": "#1a1a2e", "字节跳动": "#325AB4",
        "腾讯": "#0052D9", "百度": "#2932E1", "MiniMax": "#E1341E",
        "零一万物": "#6366F1", "智源研究院": "#0891B2", "阶跃星辰": "#D97706",
    }
    def nc(org): return ORG_COLOR_MAP.get(org, "#94a3b8")

    # 统计 tag 频次，只保留出现 ≥3 次的 tag 作为枢纽节点
    tag_count = {}
    for a in arts:
        for t in a.get("tags", []):
            tag_count[t] = tag_count.get(t, 0) + 1
    hub_tags = {t for t, c in tag_count.items() if c >= 3}

    # 节点：文章节点 + tag 节点
    nodes = []
    for a in arts:
        nodes.append({
            "id": a["id"], "label": a["title"][:20],
            "url": "articles/" + a["id"] + ".html",
            "color": nc(a.get("org", "")),
            "org": a.get("org", ""), "type": "article",
            "tags": a.get("tags", []),
            "r": 7
        })
    for t in hub_tags:
        nodes.append({
            "id": "__tag__" + t, "label": t,
            "url": None, "color": "#94a3b8",
            "org": "", "type": "tag",
            "tags": [], "r": 5 + min(tag_count[t], 15)
        })

    # 边：文章 → 其 tag 枢纽节点
    edges = []
    seen = set()
    for a in arts:
        for t in a.get("tags", []):
            if t in hub_tags:
                k = (a["id"], "__tag__" + t)
                if k not in seen:
                    seen.add(k)
                    edges.append({"s": a["id"], "t": "__tag__" + t})

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    # 图例
    orgs = sorted({a.get("org","") for a in arts if a.get("org","")})
    legend = "".join(
        f'<span><i style="background:{nc(o)}"></i>{esc(o)}</span>' for o in orgs
    )
    legend += '<span><i style="background:#94a3b8"></i>知识标签（≥3篇）</span>'

    graph_css = """
body{margin:0;background:var(--bg);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif}
:root{--bg:#F0EEE6;--surface:#FAFAF7;--ink:#191919;--muted:#6B6B63;--line:#DBD7CC;--accent:#D97757}
.gbar{position:fixed;top:0;left:0;right:0;height:52px;background:var(--surface);
  border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;
  padding:0 20px;z-index:10}
.gbar a{color:var(--muted);font-size:13px;text-decoration:none;display:flex;align-items:center;gap:5px}
.gbar a:hover{color:var(--accent)}
.gtitle{font-size:14px;font-weight:700;color:var(--ink);margin-left:4px}
.ginfo{margin-left:auto;font-size:12px;color:var(--muted)}
#canvas{display:block;position:fixed;top:52px;left:0;right:0;bottom:0;cursor:grab}
#canvas:active{cursor:grabbing}
.glegend{position:fixed;bottom:16px;left:16px;background:var(--surface);
  border:1px solid var(--line);border-radius:8px;padding:10px 14px;
  font-size:11.5px;color:var(--muted);display:flex;flex-wrap:wrap;gap:10px;max-width:600px}
.glegend span{display:flex;align-items:center;gap:4px}
.glegend i{display:inline-block;width:9px;height:9px;border-radius:50%;flex-shrink:0}
.gtooltip{position:fixed;pointer-events:none;background:rgba(20,20,20,.88);color:#fff;
  font-size:12px;padding:6px 10px;border-radius:6px;white-space:nowrap;display:none;z-index:20}
.gfilter{position:fixed;top:62px;right:14px;background:var(--surface);
  border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:12px;
  color:var(--muted);display:flex;flex-direction:column;gap:6px;max-width:160px}
.gfilter label{display:flex;align-items:center;gap:6px;cursor:pointer;white-space:nowrap}
.gfilter input[type=range]{width:100%;accent-color:var(--accent)}
"""

    html_body = f"""
<div class="gbar">
  <a href="index.html">&#8592; 返回首页</a>
  <span class="gtitle">知识图谱</span>
  <span class="ginfo" id="ginfo">{len(arts)} 篇文章 · {len(hub_tags)} 个标签节点</span>
</div>
<canvas id="canvas"></canvas>
<div class="gtooltip" id="tooltip"></div>
<div class="glegend">{legend}</div>
<div class="gfilter">
  <label>排斥力 <input type="range" id="repulse" min="30" max="200" value="90"></label>
  <label>显示标签 <input type="checkbox" id="showTags" checked></label>
  <label>显示文字 <input type="checkbox" id="showLabel" checked></label>
</div>
<script>
(function(){{
var NODES={nodes_json};
var EDGES={edges_json};
var W,H,ctx,cvs,dpr=window.devicePixelRatio||1;
var pos={{}},vel={{}},drag=null,hover=null,panX=0,panY=0,panning=false,lastPan=null,scale=1;
var repulse=90,showTags=true,showLabel=true;

document.getElementById("repulse").addEventListener("input",function(){{repulse=+this.value;}});
document.getElementById("showTags").addEventListener("change",function(){{showTags=this.checked;}});
document.getElementById("showLabel").addEventListener("change",function(){{showLabel=this.checked;}});

function init(){{
  cvs=document.getElementById("canvas");
  resize();
  // 初始布局：tag 节点按角度均匀分布在中圈，文章节点随机散布
  var tags=NODES.filter(function(n){{return n.type==="tag";}});
  var arts=NODES.filter(function(n){{return n.type==="article";}});
  tags.forEach(function(n,i){{
    var a=i/tags.length*2*Math.PI;
    var r=Math.min(W,H)*0.22;
    pos[n.id]={{x:W/2+r*Math.cos(a),y:H/2+r*Math.sin(a)}};
    vel[n.id]={{x:0,y:0}};
  }});
  arts.forEach(function(n,i){{
    var a=i/arts.length*2*Math.PI+.3;
    var r=Math.min(W,H)*(0.3+Math.random()*0.2);
    pos[n.id]={{x:W/2+r*Math.cos(a),y:H/2+r*Math.sin(a)}};
    vel[n.id]={{x:(Math.random()-.5),y:(Math.random()-.5)}};
  }});
  cvs.addEventListener("mousemove",onMove);
  cvs.addEventListener("click",onClick);
  cvs.addEventListener("mousedown",onDown);
  cvs.addEventListener("mouseup",onUp);
  cvs.addEventListener("wheel",onWheel,{{passive:false}});
  window.addEventListener("resize",resize);
  tick();
}}

function resize(){{
  W=window.innerWidth; H=window.innerHeight-52;
  cvs.width=W*dpr; cvs.height=H*dpr;
  cvs.style.width=W+"px"; cvs.style.height=H+"px";
  ctx=cvs.getContext("2d"); ctx.scale(dpr,dpr);
}}

function wx(x){{return (x-W/2)*scale+W/2+panX;}}
function wy(y){{return (y-H/2)*scale+H/2+panY;}}
function ix(sx){{return (sx-panX-W/2)/scale+W/2;}}
function iy(sy){{return (sy-panY-H/2)/scale+H/2;}}

function force(){{
  var nodes=showTags?NODES:NODES.filter(function(n){{return n.type==="article";}});
  var k=repulse;
  for(var i=0;i<nodes.length;i++)for(var j=i+1;j<nodes.length;j++){{
    var a=nodes[i],b=nodes[j];
    if(!pos[a.id]||!pos[b.id]) continue;
    var dx=pos[b.id].x-pos[a.id].x,dy=pos[b.id].y-pos[a.id].y;
    var d=Math.sqrt(dx*dx+dy*dy)||1;
    var f=k*k/d*0.04;
    vel[a.id].x-=f*dx/d; vel[a.id].y-=f*dy/d;
    vel[b.id].x+=f*dx/d; vel[b.id].y+=f*dy/d;
  }}
  EDGES.forEach(function(e){{
    if(!showTags&&e.t.indexOf("__tag__")===0) return;
    if(!pos[e.s]||!pos[e.t]) return;
    var dx=pos[e.t].x-pos[e.s].x,dy=pos[e.t].y-pos[e.s].y;
    var d=Math.sqrt(dx*dx+dy*dy)||1;
    var f=(d-k*0.9)*0.035;
    vel[e.s].x+=f*dx/d; vel[e.s].y+=f*dy/d;
    vel[e.t].x-=f*dx/d; vel[e.t].y-=f*dy/d;
  }});
  nodes.forEach(function(n){{
    vel[n.id].x+=(W/2-pos[n.id].x)*0.0008;
    vel[n.id].y+=(H/2-pos[n.id].y)*0.0008;
  }});
  nodes.forEach(function(n){{
    if(drag===n.id) return;
    vel[n.id].x*=0.82; vel[n.id].y*=0.82;
    pos[n.id].x+=vel[n.id].x; pos[n.id].y+=vel[n.id].y;
  }});
}}

function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.save();
  // 边
  EDGES.forEach(function(e){{
    if(!showTags&&e.t.indexOf("__tag__")===0) return;
    if(!pos[e.s]||!pos[e.t]) return;
    var a={{x:wx(pos[e.s].x),y:wy(pos[e.s].y)}};
    var b={{x:wx(pos[e.t].x),y:wy(pos[e.t].y)}};
    ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y);
    ctx.strokeStyle="rgba(148,163,184,.3)"; ctx.lineWidth=.8; ctx.stroke();
  }});
  // hover 节点高亮边
  if(hover){{
    EDGES.forEach(function(e){{
      if(e.s!==hover&&e.t!==hover) return;
      if(!pos[e.s]||!pos[e.t]) return;
      var a={{x:wx(pos[e.s].x),y:wy(pos[e.s].y)}};
      var b={{x:wx(pos[e.t].x),y:wy(pos[e.t].y)}};
      ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y);
      ctx.strokeStyle="rgba(217,119,87,.7)"; ctx.lineWidth=1.5; ctx.stroke();
    }});
  }}
  // 节点
  var visNodes=showTags?NODES:NODES.filter(function(n){{return n.type==="article";}});
  visNodes.forEach(function(n){{
    if(!pos[n.id]) return;
    var px=wx(pos[n.id].x), py=wy(pos[n.id].y);
    var r=n.r*Math.max(0.5,Math.min(scale,1.5));
    var isHover=hover===n.id;
    ctx.beginPath(); ctx.arc(px,py,r+(isHover?2:0),0,2*Math.PI);
    ctx.fillStyle=n.color; ctx.fill();
    if(isHover){{ctx.strokeStyle="#fff";ctx.lineWidth=1.5;ctx.stroke();}}
    if(showLabel&&scale>0.5){{
      ctx.font=(n.type==="tag"?"bold ":"")+(Math.max(9,10*scale))+"px -apple-system,sans-serif";
      ctx.fillStyle=n.type==="tag"?"#374151":"#1e293b";
      ctx.textAlign="center"; ctx.textBaseline="top";
      var lbl=n.label; if(lbl.length>12) lbl=lbl.slice(0,11)+"…";
      ctx.fillText(lbl,px,py+r+3);
    }}
  }});
  ctx.restore();
}}

var raf; function tick(){{force();draw();raf=requestAnimationFrame(tick);}}

function nodeAt(sx,sy){{
  var visNodes=showTags?NODES:NODES.filter(function(n){{return n.type==="article";}});
  for(var i=visNodes.length-1;i>=0;i--){{
    var n=visNodes[i];
    if(!pos[n.id]) continue;
    var dx=sx-wx(pos[n.id].x), dy=sy-wy(pos[n.id].y);
    var r=(n.r+4)*Math.max(0.5,Math.min(scale,1.5));
    if(dx*dx+dy*dy<=r*r) return n;
  }}
  return null;
}}
function evXY(e){{
  var r=cvs.getBoundingClientRect();
  return {{x:e.clientX-r.left,y:e.clientY-r.top}};
}}
var tip=document.getElementById("tooltip");
function onMove(e){{
  var xy=evXY(e),n=nodeAt(xy.x,xy.y);
  hover=n?n.id:null;
  cvs.style.cursor=n?"pointer":(panning?"grabbing":"grab");
  if(n){{
    var tags=n.tags&&n.tags.length?(" · "+n.tags.slice(0,3).join(", ")):"";
    tip.textContent=n.label+tags;
    tip.style.display="block";
    tip.style.left=(e.clientX+14)+"px";
    tip.style.top=(e.clientY-8)+"px";
  }} else {{
    tip.style.display="none";
  }}
  if(drag){{
    pos[drag].x=ix(xy.x); pos[drag].y=iy(xy.y);
    vel[drag]={{x:0,y:0}};
  }} else if(panning&&lastPan){{
    panX+=xy.x-lastPan.x; panY+=xy.y-lastPan.y;
    lastPan=xy;
  }}
}}
function onDown(e){{
  var xy=evXY(e),n=nodeAt(xy.x,xy.y);
  if(n){{drag=n.id; panning=false;}}
  else{{panning=true; lastPan=xy;}}
}}
function onUp(){{drag=null; panning=false; lastPan=null;}}
function onClick(e){{
  var xy=evXY(e),n=nodeAt(xy.x,xy.y);
  if(n&&n.url) window.location.href=n.url;
}}
function onWheel(e){{
  e.preventDefault();
  var f=e.deltaY>0?0.9:1.1;
  scale=Math.max(0.3,Math.min(4,scale*f));
}}
if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",init);
else init();
}})();
</script>
"""
    return (f'<!DOCTYPE html><html lang="zh-CN"><head>'
            f'<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>知识图谱 · {esc(site_title)}</title>{FONTS}'
            f'<style>{graph_css}</style></head><body>{html_body}</body></html>')


def render_index(arts, site_title):
    # 从 blogs.json 获取官方公司 org 集合
    try:
        _bj = json.load(open(os.path.join(os.path.dirname(__file__), "blogs.json"), encoding="utf-8"))
        _company_orgs = {b["org"] for b in _bj["blogs"]}
    except Exception:
        _company_orgs = set()

    orgs = []
    for a in arts:
        if a["org"] and a["org"] not in orgs:
            orgs.append(a["org"])
    total_min = sum(a["minutes"] for a in arts)

    # 公司 chips（来自 org 字段）
    company_orgs = [o for o in orgs if o in _company_orgs]

    # 话题 chips（来自 tags 字段，排除 org 名称和无意义标签）
    _skip_tags = _company_orgs | {"开源", "技术报告", "Release Notes", "company",
                                   "interpretability", "FlagAI", "AI 工程实践",
                                   "RAG 研究", "行业实践", "记忆系统", "其他"}
    tag_counter = {}
    for a in arts:
        for t in a.get("tags", []):
            if t and t not in _skip_tags:
                tag_counter[t] = tag_counter.get(t, 0) + 1
    # 按频次排序，只显示出现 ≥2 次的话题
    topic_tags = [t for t, cnt in sorted(tag_counter.items(), key=lambda x: -x[1]) if cnt >= 2]

    all_chip = '<button class="chip active" data-org="__all__" data-tag="" data-dim="all">全部</button>'
    company_chips = "".join(
        f'<button class="chip" data-org="{esc(o)}" data-tag="" data-dim="company">{esc(o)}</button>'
        for o in company_orgs)
    topic_chips = "".join(
        f'<button class="chip topic" data-org="" data-tag="{esc(t)}" data-dim="topic">{esc(t)}</button>'
        for t in topic_tags)
    cards = []
    for a in arts:
        col = org_color(a["org"])
        tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in a["tags"][:3])
        badge = f'<span class="badge" style="background:{col}">{esc(a["org"] or "未标注")}</span>'
        cards.append(f'''<article class="card" data-org="{esc(a["org"])}"
        data-tags="{esc(','.join(a['tags']))}"
        data-text="{esc((a["title"]+" "+a["summary"]+" "+" ".join(a["tags"])).lower())}" data-id="{a["id"]}">
        <span class="readdot" aria-hidden="true"></span>
        <div class="card-top">{badge}<span class="card-date">{esc(a["date"])}</span></div>
        <h3><a href="articles/{a["id"]}.html">{esc(a["title"])}</a></h3>
        <p class="sum">{esc(a["summary"])}</p>
        <div class="card-foot">
          <div class="tags">{tags}</div>
          <span class="rt" aria-label="{a["minutes"]} 分钟阅读">{ICON_CLOCK}{a["minutes"]} 分钟</span>
        </div>
        </article>''')
    body = f'''
    <div class="hero"><div class="hero-in">
      <div class="hero-eyebrow">AI 技术知识库</div>
      <h1>{esc(site_title)}<span class="dot">.</span></h1>
      <p class="hero-desc">汇集国内外 AI 大厂的工程与研究博客，整理为结构化中文知识。点击卡片进入阅读页，含自动目录、原文链接与已读标记。</p>
      <div class="stats">
        <div class="stat"><b>{len(arts)}</b><span>篇文章</span></div>
        <div class="stat"><b>{len(orgs)}</b><span>个来源</span></div>
        <div class="stat"><b>{total_min}</b><span>分钟总时长</span></div>
        <div class="stat"><b id="readN">0</b><span>已读</span></div>
      </div>
    </div></div>
    <div class="controls"><div class="container">
      <div class="ctrl-row">
        <div class="search-wrap">
          <span class="ico" aria-hidden="true">{ICON_SEARCH}</span>
          <input class="search" id="q" type="search" placeholder="搜索标题、摘要或标签…" aria-label="搜索文章">
        </div>
        <a href="graph.html" style="display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:99px;background:var(--surface-2);color:var(--ink-2);font-size:12.5px;font-weight:600;text-decoration:none;border:1px solid var(--line);white-space:nowrap;transition:all .15s" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--line)'"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="5" r="3"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><line x1="12" y1="8" x2="5" y2="16"/><line x1="12" y1="8" x2="19" y2="16"/></svg>知识图谱</a>
      </div>
      <div class="filter-rows">
        <div class="filter-row">
          <span class="filter-label">公司</span>
          <div class="chips" id="chips" role="group" aria-label="按公司筛选">
            {all_chip}{company_chips}
          </div>
        </div>
        {f'<div class="filter-row"><span class="filter-label">话题</span><div class="chips" id="chips-topic" role="group" aria-label="按话题筛选">{topic_chips}</div></div>' if topic_chips else ''}
      </div>
    </div></div>
    <div class="container">
      <div class="grid" id="grid" role="list">{''.join(cards)}</div>
      <div class="empty" id="empty" style="display:none" role="status">
        <strong>—</strong>没有匹配的文章，换个关键词试试
      </div>
    </div>
    <div class="foot">由 tech-blog-downloader 生成</div>
    <script>
    var RK="techblog_read";
    function readSet(){{try{{return new Set(JSON.parse(localStorage.getItem(RK)||"[]"))}}catch(e){{return new Set()}}}}
    function paintRead(){{var s=readSet();document.querySelectorAll(".card").forEach(function(c){{
      c.classList.toggle("read",s.has(c.dataset.id));}});document.getElementById("readN").textContent=s.size;}}
    var curOrg="__all__",curTag="",tid=0;
    function apply(){{
      var q=document.getElementById("q").value.trim().toLowerCase();
      var vis=0;
      document.querySelectorAll(".card").forEach(function(c){{
        var orgOk=(curOrg==="__all__"||c.dataset.org===curOrg);
        var tagOk=(!curTag||(","+c.dataset.tags+",").indexOf(","+curTag+",")>=0);
        var ok=orgOk&&tagOk&&(!q||c.dataset.text.indexOf(q)>=0);
        c.style.display=ok?"":"none";if(ok)vis++;}});
      document.getElementById("empty").style.display=vis?"none":"block";
    }}
    document.getElementById("q").addEventListener("input",function(){{clearTimeout(tid);tid=setTimeout(apply,120);}});
    document.querySelectorAll(".chips").forEach(function(row){{
      row.addEventListener("click",function(e){{
        var t=e.target.closest(".chip");if(!t)return;
        if(t.dataset.dim==="all"){{
          // 全部：清除所有筛选
          document.querySelectorAll(".chip").forEach(function(c){{c.classList.remove("active")}});
          t.classList.add("active");curOrg="__all__";curTag="";
        }} else if(t.dataset.dim==="company"){{
          // 公司：清除公司行其他选中，清除话题行选中，按 org 过滤
          document.querySelectorAll("#chips .chip").forEach(function(c){{c.classList.remove("active")}});
          document.querySelectorAll("#chips-topic .chip").forEach(function(c){{c.classList.remove("active")}});
          t.classList.add("active");curOrg=t.dataset.org;curTag="";
        }} else {{
          // 话题：清除公司行选中，清除话题行其他选中，按 tag 过滤
          document.querySelectorAll("#chips .chip").forEach(function(c){{c.classList.remove("active")}});
          document.querySelectorAll("#chips-topic .chip").forEach(function(c){{c.classList.remove("active")}});
          t.classList.add("active");curOrg="__all__";curTag=t.dataset.tag;
        }}
        apply();
      }});
    }});
    paintRead();window.addEventListener("focus",paintRead);
    </script>'''
    return page(site_title, body)


def render_article(a, prev, nxt, site_title):
    col = org_color(a["org"])
    toc_html = ""
    if a["toc"]:
        items = "".join(
            f'<a class="{"lv3" if lv==3 else "lv2"}" href="#{sid}">{esc(txt)}</a>'
            for lv, txt, sid in a["toc"])
        toc_html = f'<nav class="toc"><div class="t">本页目录</div>{items}</nav>'
    meta_bits = []
    if a["org"]:
        meta_bits.append(f'<span class="badge" style="background:{col}">{esc(a["org"])}</span>')
    head_m = []
    if a["date"]:
        head_m.append(f'<span style="display:inline-flex;align-items:center;gap:4px">{ICON_CAL}{esc(a["date"])}</span>')
    head_m.append(f'<span style="display:inline-flex;align-items:center;gap:4px">{ICON_CLOCK}约 {a["minutes"]} 分钟</span>')
    if a["tags"]:
        head_m.append("".join(f'<span class="tag">{esc(t)}</span>' for t in a["tags"]))
    # 双语摘要卡片
    zh = inline_md(a.get("summary_zh", ""))
    en = inline_md(a.get("summary_en", ""))
    # 如果只有一种语言摘要，根据内容语言决定放哪边
    if not zh and not en:
        s = inline_md(a.get("summary",""))
        cjk = len(re.findall(r"[一-鿿]", a.get("summary","")))
        if cjk > len(a.get("summary","")) * 0.2:
            zh = s
        else:
            en = s
    summary_card = ""
    if zh or en:
        blocks = []
        if zh:
            blocks.append(f'<div class="sc-block"><div class="sc-label">中文摘要</div><div class="sc-text">{zh}</div></div>')
        if zh and en:
            blocks.append('<div class="sc-divider"></div>')
        if en:
            blocks.append(f'<div class="sc-block"><div class="sc-label">English Summary</div><div class="sc-text">{en}</div></div>')
        summary_card = f'<div class="summary-card"><div class="sc-row">{"".join(blocks)}</div></div>'
    # 醒目原文按钮
    source_btn = ""
    if a["source_url"]:
        source_btn = (f'<a class="source-btn" href="{esc(a["source_url"])}" '
                      f'target="_blank" rel="noopener">{ICON_LINK} 阅读原文</a>')
    nav_prev = (f'<a class="prev" href="{prev["id"]}.html"><div class="lbl">‹ 上一篇</div>'
                f'<div class="ti">{esc(prev["title"])}</div></a>') if prev else '<span style="flex:1"></span>'
    nav_next = (f'<a class="next" href="{nxt["id"]}.html"><div class="lbl">下一篇 ›</div>'
                f'<div class="ti">{esc(nxt["title"])}</div></a>') if nxt else '<span style="flex:1"></span>'
    body = f'''
    <div class="abar"><div class="abar-in">
      <a class="back" href="../index.html" aria-label="返回学习站">{ICON_BACK}返回</a>
      <div class="spacer"></div>
      <button class="btn" id="readBtn" aria-pressed="false">标记已读</button>
    </div></div>
    <div class="alayout">
      <article class="article">
        <div class="ahead">
          {''.join(meta_bits)}
          <h1>{esc(a["title"])}</h1>
          <div class="m">{''.join(head_m)}</div>
          {source_btn}
        </div>
        {summary_card}
        <div class="prose">{a["body_html"]}</div>
        <div class="anav">{nav_prev}{nav_next}</div>
      </article>
      {toc_html}
    </div>
    <div class="foot">{esc(site_title)}</div>
    <script>
    var RK="techblog_read",ID="{a["id"]}";
    function rset(){{try{{return new Set(JSON.parse(localStorage.getItem(RK)||"[]"))}}catch(e){{return new Set()}}}}
    var btn=document.getElementById("readBtn");
    btn.addEventListener("click",function(){{var s=rset();if(s.has(ID))s.delete(ID);else s.add(ID);
      localStorage.setItem(RK,JSON.stringify([...s]));paint();}});
    function paint(){{var on=rset().has(ID);btn.classList.toggle("done",on);
      btn.setAttribute("aria-pressed",on?"true":"false");
      btn.innerHTML=on?'{ICON_CHECK} 已读':' 标记已读';}}
    paint();
    </script>'''
    return page(f'{a["title"]} · {site_title}', body)

# ── 主流程 ───────────────────────────────────────────────────────────────────
# 脚本自身所在目录（无论从哪里调用都稳定）
_HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    # 默认路径相对于脚本自身，而非调用目录
    src = os.path.abspath(args[0]) if len(args) > 0 else os.path.join(_HERE, "examples", "articles")
    out = os.path.abspath(args[1]) if len(args) > 1 else os.path.join(_HERE, "examples", "site")
    title = "AI 技术博客 · 中文学习站"
    if "--title" in sys.argv:
        idx = sys.argv.index("--title")
        if idx + 1 < len(sys.argv):
            title = sys.argv[idx + 1]
    if not os.path.isdir(src):
        print(f"[错误] 文章目录不存在：{src}")
        print(f"  用法：python3 generate_site.py <articles_dir> <out_dir> [--title 标题]")
        print(f"  示例：python3 generate_site.py ~/Desktop/articles ~/Desktop/site --title \"AI 学习站\"")
        sys.exit(1)
    arts = load_articles(src)
    if not arts:
        print(f"[错误] {src} 下没有 .md 文章")
        print(f"  每篇文章须为 .md 格式，建议带 frontmatter（title/org/date/tags/summary）")
        sys.exit(1)
    os.makedirs(os.path.join(out, "articles"), exist_ok=True)
    print(f"  正在生成 {len(arts)} 篇文章 → {out}")
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index(arts, title))
    with open(os.path.join(out, "graph.html"), "w", encoding="utf-8") as f:
        f.write(render_graph(arts, title))
    for i, a in enumerate(arts):
        prev = arts[i - 1] if i > 0 else None
        nxt = arts[i + 1] if i < len(arts) - 1 else None
        with open(os.path.join(out, "articles", a["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(render_article(a, prev, nxt, title))
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump([{k: a[k] for k in ("id","title","org","date","tags","minutes","source_url")} for a in arts],
                  f, ensure_ascii=False, indent=2)
    index_path = os.path.join(out, "index.html")
    print(f"✓ 生成完成：{len(arts)} 篇")
    print(f"  网站首页：{index_path}")
    print(f"  浏览器打开：open \"{index_path}\"")

if __name__ == "__main__":
    main()
