# -*- coding: utf-8 -*-
"""Anthropic 研究地图 · 小红书竖版信息图 + 可浏览网页。
风格：Anthropic 官方暖风——暖米白 #F0EEE6 + 陶土橙 #D97757 + 衬线大标题 + 大留白。
结构：每页 = 海报区(固定 1080×1440，用于截图 PNG) + 原文阅读区(仅浏览，含摘要/原文节选)。
浏览时内容居中、可翻页跳转；渲染 PNG 时用 #shot 锚点隐藏阅读区与导航，图片不变。
"""
import os, re, html

OUT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(OUT, "..", "..", "raw"))
W, H = 1080, 1440  # 小红书 3:4 竖版海报

# ── 章节数据：article = (英文标题, 一句话要点, raw 文件名) ─────────────────────
CHAPTERS = [
    {
        "no": "01",
        "cn": "智能体工程", "en": "Agent Engineering",
        "hook": "让一个 AI 自己干活一整天，中途不掉链子——这一年 Anthropic 全在攻这件事。",
        "metrics": [("16", "篇方法论"), ("跨窗口", "长周期不断片"), ("多智能体", "并行协作")],
        "articles": [
            ("Building Effective Agents", "智能体设计基石：工具怎么用、何时才该上多智能体",
             "01-Building effective agents.md"),
            ("Effective Context Engineering", "长周期工作流的上下文管理：压缩 · 检索 · 记忆 · 预算",
             "02-Effective context engineering for AI agents.md"),
            ("Effective Harnesses for Long-Running Agents", "跨多个上下文窗口保持一致进展的 Harness 架构",
             "16-Effective harnesses for long-running agents.md"),
            ("Agent Skills", "用一个文件夹封装可复用领域知识，打通专业 Agent",
             "19-Equipping agents for the real world with Agent Skills.md"),
            ("Building a C Compiler with Parallel Claudes", "多个 Claude 并行造出 C 编译器，预演自主开发",
             "14-Building a C compiler with parallel Claudes.md"),
        ],
        "insight": "主线很清晰：上下文工程 → Harness 设计 → 工具编写 → 自主性度量。把 Agent 从「能跑 demo」推到「能在生产里长期、可控地干活」。",
    },
    {
        "no": "02",
        "cn": "可解释性与对齐", "en": "Interpretability & Alignment",
        "hook": "别人忙着调模型，Anthropic 在拆模型的脑子——还想让 AI 自己研究怎么对齐 AI。",
        "metrics": [("2025", "电路追踪起点"), ("→", "思维变可读"), ("自动化", "对齐研究者")],
        "articles": [
            ("Tracing the Thoughts of an LLM", "里程碑：用机制可解释性追踪大模型内部的「思维回路」",
             "21-Tracing-the-thoughts-of-a-large-language-model.md"),
            ("Natural Language Autoencoders", "把 Claude 的内部表征翻译成自然语言，让思维可读",
             "01-Natural-Language-Autoencoders.md"),
            ("Teaching Claude Why", "超越规则、让模型理解行为背后的原因",
             "02-Teaching-Claude-why.md"),
            ("Automated Alignment Researchers", "用 LLM 扩展可扩展监督：让 AI 来做对齐研究",
             "14-Automated-Alignment-Researchers.md"),
            ("From Shortcuts to Sabotage", "奖励攻击如何自然涌现成错位行为的实证研究",
             "23-From-shortcuts-to-sabotage.md"),
        ],
        "insight": "递进逻辑：先「看见」内部（电路追踪）→ 再「读懂」（自然语言自编码器）→ 最后「自动化」对齐。可解释性正从科研奇观变成工程基础设施。",
    },
    {
        "no": "03",
        "cn": "模型行为与角色", "en": "Model Behavior & Persona",
        "hook": "AI 也有性格吗？它的「人设」从哪来、能不能调？这是安全问题，也是产品问题。",
        "metrics": [("人格", "可定位向量"), ("情感", "功能性表征"), ("价值观", "涌现与控制")],
        "articles": [
            ("Persona Vectors", "量化并可控调节 LLM 性格特征的向量技术",
             "30-Persona-vectors.md"),
            ("The Assistant Axis", "「助理性格」为何稳定：可解释性视角的角色分析",
             "28-The-assistant-axis.md"),
            ("Emotion Concepts & Function", "LLM 中的情感概念：是模拟，还是有功能性表征？",
             "18-Emotion-concepts-and-their-function.md"),
            ("Values in the Wild", "真实交互中 LLM 价值观的涌现、冲突与分布",
             "27-Values-in-the-wild.md"),
            ("Claude for Companionship", "用户与 AI 的情感连接：陪伴、支持与依赖的边界",
             "07-How-people-use-Claude-for-support-advice-and-companionship.md"),
        ],
        "insight": "Anthropic 把「AI 性格」从玄学变成可测量、可干预的对象：用向量定位、用可解释性归因、用真实数据验证。",
    },
    {
        "no": "04",
        "cn": "安全与防御", "en": "Safety & Defense",
        "hook": "怎么不让 AI 闯祸？答案不是口号，是分类器、沙箱和一份份公开复盘。",
        "metrics": [("93%", "Auto 同意率"), ("双边界", "文件+网络隔离"), ("1 年", "威胁全景")],
        "articles": [
            ("Next-Gen Constitutional Classifiers", "更高效对抗通用越狱的宪法分类器防护体系",
             "17-Next-generation-Constitutional-Classifiers.md"),
            ("How We Built Claude Code Auto Mode", "用分类器自动化权限决策，93% 用户同意率背后的工程",
             "23-How we built Claude Code auto mode.md"),
            ("Beyond Permission Prompts: Sandboxing", "文件系统 + 网络双边界隔离，更自主也更安全",
             "18-Beyond permission prompts Claude Code sandboxing.md"),
            ("Mapping AI-Enabled Cyber Threats", "一整年 AI 辅助网络威胁全景：攻击向量与防御启示",
             "06-What-we-learned-mapping-AI-enabled-cyber-threats.md"),
            ("A Postmortem of Three Recent Issues", "三个间歇性质量降级问题的完整技术复盘",
             "20-A postmortem of three recent issues.md"),
        ],
        "insight": "安全在这里是能跑的代码，不是合规话术。透明复盘和威胁映射，把信任建立在证据而非承诺上。",
    },
    {
        "no": "05",
        "cn": "AI 经济影响", "en": "Economic Impact",
        "hook": "AI 到底抢了谁的活、帮了谁？Anthropic 用真实对话数据，把感觉变成了可追踪的证据。",
        "metrics": [("81,000", "人需求调研"), ("多国", "澳·印·全球"), ("1,250", "专业人士访谈")],
        "articles": [
            ("Economic Index: Claude 3.7 Insights", "Claude 使用的经济任务分布：哪些工作最依赖 AI",
             "09-Anthropic-Economic-Index-Insights-from-Claude-3.7-Sonnet.md"),
            ("Economic Primitives", "AI 经济影响的基础框架：任务 · 技能 · 职业",
             "36-Economic-Index-Economic-primitives.md"),
            ("What 81,000 People Want from AI", "8.1 万用户调研：AI 真正被需要的场景与期望",
             "07-What-81000-people-want-from-AI.md"),
            ("Labor Market Impacts of AI", "AI 劳动力市场影响的新度量方法与早期证据",
             "33-Labor-market-impacts-of-AI.md"),
            ("AI Assistance & Coding Skills", "AI 辅助编程对开发者技能形成的正负两面",
             "24-How-AI-assistance-impacts-coding-skills.md"),
        ],
        "insight": "方法论才是核心资产：用真实对话 + 标准化框架，把 AI 的经济影响做成可跨国、跨时间比较的指数——别人难复制的数据壁垒。",
    },
    {
        "no": "06",
        "cn": "政策治理与商业化", "en": "Policy & Commercialization",
        "hook": "一年时间，从研究实验室烧到 IPO 门口——资本、产品、政策三条线全速齐发。",
        "metrics": [("$65B", "H 轮融资"), ("S-1", "IPO 启动"), ("2028", "领导力情景")],
        "articles": [
            ("Introducing Claude Opus 4.8", "最强旗舰发布：推理与编码全面领跑",
             "01-Introducing-Claude-Opus-4-8.md"),
            ("Anthropic Raises $65B Series H", "约 9650 亿美元估值完成 650 亿 H 轮",
             "11-Anthropic-raises-65B-Series-H-funding.md"),
            ("Confidentially Files S-1 to SEC", "秘密提交 S-1 草稿，IPO 进程正式启动",
             "12-Anthropic-confidentially-submits-draft-S-1-to-SEC.md"),
            ("2028: Two Scenarios for AI Leadership", "全球 AI 领导力两种未来：合作共赢 vs 竞争分裂",
             "08-2028-Two-scenarios-for-global-AI-leadership.md"),
            ("Making Claude a Chemist", "化学领域专业化突破：分子设计与合成推理",
             "03-Making-Claude-a-chemist.md"),
        ],
        "insight": "2026 上半年的关键词是「加速」：资本（$65B + IPO）、产品（Opus 4.8 + 垂直化）、政策（Glasswing + 2028 情景）三线齐发。",
    },
]

# ── 从 raw 原文提取 日期 / 摘要 / 原文节选 ───────────────────────────────────
def _clean(s):
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)   # [text](url) -> text
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)        # images
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    s = re.sub(r'\*([^*]+)\*', r'\1', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'^\s*[\*\-+]\s+', '', s, flags=re.M)   # 列表符号
    s = re.sub(r'\s+', ' ', s).strip()
    return s

_DATE_ONLY = re.compile(r'^(Published\s+)?(\*\*Date\*\*:\s*)?'
                        r'([A-Z][a-z]{2,8}\.?\s+\d{1,2},?\s+\d{4})\s*$')

def extract(fname):
    path = os.path.join(RAW, fname)
    date = ""
    paras = []
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return {"date": "", "summary": "(原文缺失)", "excerpt": "", "url": ""}
    # 日期：扫描前若干行
    for ln in text.split("\n")[:8]:
        m = re.search(r'([A-Z][a-z]{2,8}\.?\s+\d{1,2},?\s+\d{4})', ln)
        if m and ("Date" in ln or "Published" in ln or _DATE_ONLY.match(ln.strip())):
            date = m.group(1); break
    # 原文链接
    um = re.search(r'(https?://www\.anthropic\.com[^\s)]+)', text)
    url = um.group(1) if um else ""
    # 段落
    for blk in re.split(r'\n\s*\n', text):
        b = blk.strip()
        if not b or b == "---" or b.startswith("#"):
            continue
        if re.match(r'^https?://', b):
            continue
        if _DATE_ONLY.match(b) or re.match(r'^\*\*Date\*\*', b):
            continue
        c = _clean(b)
        if len(c) < 45:
            continue
        paras.append(c)
        if len(paras) >= 4:
            break

    def cap(s, n):
        return s if len(s) <= n else s[:n].rstrip() + "…"

    summary = cap(paras[0], 300) if paras else "(暂无摘要)"
    excerpt = cap(" ".join(paras[1:3]), 680) if len(paras) > 1 else ""
    return {"date": date, "summary": summary, "excerpt": excerpt, "url": url}

# ── 字体 & 基础样式 ──────────────────────────────────────────────────────────
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&'
         'family=Noto+Serif+SC:wght@500;600;700;900&'
         'family=Inter:wght@400;500;600&display=swap" rel="stylesheet">')

BASE_CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#F0EEE6;--ink:#191919;--ink2:#6B6B63;--clay:#D97757;--clay2:#C15F3C;
  --line:#DBD7CC;--card:#E8E5DB}}
html,body{{width:100%;min-height:100%;background:var(--bg)}}
body{{color:var(--ink);font-family:'Inter','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased}}
.serif{{font-family:'Fraunces','Noto Serif SC',serif}}
.cnserif{{font-family:'Noto Serif SC','Fraunces',serif}}
/* 居中列 */
.page{{width:{W}px;margin:0 auto}}
/* 海报区：固定尺寸，截图就截这块 */
.poster{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--bg)}}
.poster::after{{content:'';position:absolute;inset:0;z-index:0;opacity:.5;pointer-events:none;
  background-image:radial-gradient(circle at 50% 50%,rgba(180,170,150,.05) 1px,transparent 1px);
  background-size:5px 5px}}
.wrap{{position:relative;z-index:1;height:100%;padding:84px 80px 64px;display:flex;flex-direction:column}}
.mark{{width:46px;height:4px;background:var(--clay);border-radius:4px;margin-bottom:22px}}
/* ── 导航（浏览显示，截图隐藏）── */
.navbtn{{position:fixed;z-index:50;width:56px;height:56px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;text-decoration:none;
  background:rgba(25,25,25,.86);color:#F0EEE6;font-size:26px;font-weight:500;
  box-shadow:0 6px 22px rgba(60,40,20,.22);transition:transform .15s,background .15s}}
.navbtn:hover{{transform:scale(1.08);background:var(--clay)}}
.nav-prev{{left:34px;top:50%;margin-top:-28px}}
.nav-next{{right:34px;top:50%;margin-top:-28px}}
.nav-home{{left:34px;top:34px;width:auto;height:auto;border-radius:30px;
  padding:11px 22px;font-size:14px;letter-spacing:2px;gap:8px}}
.nav-page{{position:fixed;z-index:50;right:34px;top:40px;font:600 13px 'Inter',sans-serif;
  letter-spacing:2px;color:var(--ink2);background:var(--card);padding:9px 16px;border-radius:30px}}
.shot .navbtn,.shot .nav-page,.shot .reading{{display:none!important}}
/* ── 原文阅读区（仅浏览）── */
.reading{{padding:64px 80px 110px}}
.rd-inner{{max-width:900px;margin:0 auto}}
.rd-head{{font:600 14px 'Inter',sans-serif;letter-spacing:3px;color:var(--ink2);
  text-transform:uppercase;display:flex;align-items:center;gap:12px;margin-bottom:8px}}
.rd-head::before{{content:'';width:26px;height:2.5px;background:var(--clay)}}
.rd-sub{{font-size:15px;color:var(--ink2);margin-bottom:40px}}
.src{{padding:30px 0;border-bottom:1px solid var(--line)}}
.src:last-child{{border-bottom:none}}
.src-top{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}}
.src-no{{font:600 18px 'Fraunces',serif;color:var(--clay);flex:none}}
.src-title{{font:600 25px 'Fraunces',serif;color:var(--ink);line-height:1.25}}
.src-date{{margin-left:auto;font:500 13px 'Inter',sans-serif;color:var(--ink2);
  background:var(--card);padding:4px 12px;border-radius:20px;white-space:nowrap}}
.src-one{{font-size:16px;color:var(--clay2);margin:10px 0 18px;font-weight:500}}
.lbl{{font:600 11px 'Inter',sans-serif;letter-spacing:2px;text-transform:uppercase;
  color:var(--ink2);margin-bottom:7px}}
.src-sum{{font-size:17.5px;line-height:1.8;color:#2b2a26;
  border-left:3px solid var(--clay);padding-left:18px;margin-bottom:18px}}
.src-exc{{font-size:16px;line-height:1.85;color:#56544c}}
.src-link{{display:inline-block;margin-top:14px;font:500 14px 'Inter',sans-serif;
  color:var(--clay2);text-decoration:none}}
.src-link:hover{{text-decoration:underline}}
.src-link::after{{content:' ↗'}}
'''

def esc(s): return html.escape(s)

def nav(prev, nxt, idx, total, is_cover=False):
    parts = []
    if not is_cover:
        parts.append('<a class="navbtn nav-home" href="00-cover.html">☰ 目录</a>')
        parts.append('<div class="nav-page">%d / %d</div>' % (idx, total))
    if prev:
        parts.append('<a class="navbtn nav-prev" href="%s">‹</a>' % prev)
    if nxt:
        parts.append('<a class="navbtn nav-next" href="%s">›</a>' % nxt)
    pj = ('"%s"' % prev) if prev else "null"
    nj = ('"%s"' % nxt) if nxt else "null"
    js = ('<script>'
          'if(location.hash==="#shot")document.body.classList.add("shot");'
          'var P=%s,N=%s;'
          'document.addEventListener("keydown",function(e){'
          'if(e.key==="ArrowLeft"&&P)location.href=P;'
          'if(e.key==="ArrowRight"&&N)location.href=N;});'
          '</script>') % (pj, nj)
    return "".join(parts) + js

def reading_section(ch):
    items = []
    for i, (title, one, src) in enumerate(ch["articles"]):
        info = extract(src)
        date = f'<span class="src-date">{esc(info["date"])}</span>' if info["date"] else ""
        exc = f'<div class="lbl">原文节选 · Excerpt</div><div class="src-exc">{esc(info["excerpt"])}</div>' if info["excerpt"] else ""
        link = f'<a class="src-link" href="{esc(info["url"])}" target="_blank">阅读原文</a>' if info["url"] else ""
        items.append(f'''<div class="src">
          <div class="src-top"><span class="src-no">{i+1:02d}</span>
            <span class="src-title">{esc(title)}</span>{date}</div>
          <div class="src-one">{esc(one)}</div>
          <div class="lbl">摘要 · Summary</div>
          <div class="src-sum">{esc(info["summary"])}</div>
          {exc}{link}
        </div>''')
    return f'''<div class="reading"><div class="rd-inner">
      <div class="rd-head">原文摘要与节选 · Source Material</div>
      <div class="rd-sub">本章精选 {len(ch["articles"])} 篇 Anthropic 官方文章，以下为各篇原文的日期、摘要与正文节选。</div>
      {"".join(items)}
    </div></div>'''

def chapter_html(ch, prev, nxt, idx, total):
    metrics = "".join(
        f'<div class="m"><div class="mv cnserif">{esc(v)}</div><div class="ml">{esc(l)}</div></div>'
        for v, l in ch["metrics"]
    )
    arts = "".join(
        f'''<div class="art"><div class="ah"><span class="an cnserif">{i+1:02d}</span>
          <span class="at">{esc(t)}</span></div>
          <div class="as">{esc(s)}</div></div>'''
        for i, (t, s, _src) in enumerate(ch["articles"])
    )
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{FONTS}<style>{BASE_CSS}
.kick{{display:flex;align-items:center;gap:16px;margin-bottom:30px}}
.chno{{font:600 15px 'Fraunces',serif;letter-spacing:3px;color:var(--clay);
  border:1.5px solid var(--clay);padding:5px 14px;border-radius:30px}}
.kline{{flex:1;height:1.5px;background:var(--line)}}
.brand{{font:500 12px 'Inter',sans-serif;letter-spacing:2.5px;color:var(--ink2);text-transform:uppercase}}
.en{{font:500 22px 'Fraunces',serif;color:var(--clay2);letter-spacing:.5px;margin-bottom:6px}}
.cn{{font-weight:900;font-size:68px;line-height:1.04;letter-spacing:1px;margin-bottom:24px}}
.hook{{font-size:23px;line-height:1.65;color:#33312b;font-weight:500;
  border-left:4px solid var(--clay);padding-left:20px;margin-bottom:34px}}
.metrics{{display:flex;gap:16px;margin-bottom:40px}}
.m{{flex:1;background:var(--card);border-radius:16px;padding:20px 18px;text-align:center}}
.mv{{font-size:34px;font-weight:700;color:var(--clay2);line-height:1}}
.ml{{font-size:14px;color:var(--ink2);margin-top:8px;font-weight:500}}
.ltt{{font:600 14px 'Inter',sans-serif;letter-spacing:3px;color:var(--ink2);
  text-transform:uppercase;margin-bottom:18px;display:flex;align-items:center;gap:10px}}
.ltt::before{{content:'';width:22px;height:2.5px;background:var(--clay)}}
.list{{flex:1;display:flex;flex-direction:column;gap:0}}
.art{{padding:16px 0;border-bottom:1px solid var(--line)}}
.art:first-child{{padding-top:0}}
.ah{{display:flex;align-items:baseline;gap:14px}}
.an{{font-size:18px;font-weight:600;color:var(--clay);flex:none;width:30px}}
.at{{font-size:22px;font-weight:600;color:var(--ink);line-height:1.3}}
.as{{font-size:16px;color:var(--ink2);line-height:1.5;margin-top:5px;margin-left:44px}}
.insight{{margin-top:24px;background:var(--clay);color:#FBF6EE;border-radius:18px;padding:24px 28px}}
.itag{{font:600 12px 'Inter',sans-serif;letter-spacing:2.5px;margin-bottom:10px;opacity:.85}}
.itext{{font-size:18px;line-height:1.65;font-weight:500}}
.foot{{margin-top:18px;display:flex;justify-content:space-between;
  font:500 12px 'Inter',sans-serif;letter-spacing:1.5px;color:var(--ink2)}}
</style></head><body>
<div class="page">
  <div class="poster"><div class="wrap">
    <div class="kick"><span class="chno">CH · {ch["no"]}</span><span class="kline"></span>
      <span class="brand">Anthropic Research Map</span></div>
    <div class="mark"></div>
    <div class="en serif">{esc(ch["en"])}</div>
    <div class="cn cnserif">{esc(ch["cn"])}</div>
    <div class="hook">{esc(ch["hook"])}</div>
    <div class="metrics">{metrics}</div>
    <div class="ltt">精选研究 · Key Papers</div>
    <div class="list">{arts}</div>
    <div class="insight"><div class="itag">核心洞察 · KEY INSIGHT</div><div class="itext">{esc(ch["insight"])}</div></div>
    <div class="foot"><span>{esc(ch["en"])}</span><span>tech-blog-downloader</span></div>
  </div></div>
  {reading_section(ch)}
</div>{nav(prev, nxt, idx, total)}</body></html>'''

def cover_html(nxt, total):
    toc = "".join(
        f'''<a class="ti" href="{ch["no"]}-{ch["en"].split()[0].lower().rstrip("&")}.html">
          <span class="tn cnserif">{ch["no"]}</span>
          <span class="tc cnserif">{esc(ch["cn"])}</span>
          <span class="te serif">{esc(ch["en"])}</span><span class="tgo">›</span></a>'''
        for ch in CHAPTERS
    )
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{FONTS}<style>{BASE_CSS}
.wrap{{padding:90px 80px 70px}}
.top{{font:500 14px 'Inter',sans-serif;letter-spacing:3px;color:var(--clay2);
  text-transform:uppercase;margin-bottom:28px}}
.big{{font-weight:900;font-size:82px;line-height:1.05;letter-spacing:1px;margin-bottom:8px}}
.big .o{{color:var(--clay)}}
.ensub{{font:500 30px 'Fraunces',serif;color:var(--ink2);margin-bottom:26px}}
.lead{{font-size:22px;line-height:1.7;color:#33312b;font-weight:500;margin-bottom:40px}}
.lead b{{color:var(--clay2);font-weight:700}}
.divider{{height:1.5px;background:var(--line);margin-bottom:8px}}
.toc{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.ti{{display:flex;align-items:center;gap:20px;padding:17px 0;border-bottom:1px solid var(--line);
  text-decoration:none;transition:padding-left .15s}}
.ti:hover{{padding-left:8px}}
.ti:hover .tgo{{color:var(--clay);transform:translateX(4px)}}
.tn{{font-size:24px;font-weight:700;color:var(--clay);width:46px;flex:none}}
.tc{{font-size:30px;font-weight:700;color:var(--ink);flex:none}}
.te{{font-size:17px;color:var(--ink2);font-weight:400;flex:1;text-align:right}}
.tgo{{font-size:26px;color:var(--line);width:24px;text-align:center;transition:.15s}}
.foot{{margin-top:26px;display:flex;justify-content:space-between;align-items:center;
  font:500 13px 'Inter',sans-serif;letter-spacing:1.5px;color:var(--ink2)}}
.foot .tag{{background:var(--ink);color:var(--bg);padding:7px 16px;border-radius:30px;letter-spacing:2px}}
</style></head><body>
<div class="page"><div class="poster"><div class="wrap">
  <div class="top">Anthropic Research Map · 2025–2026</div>
  <div class="big">读完 <span class="o">80+ 篇</span><br>Anthropic 研究</div>
  <div class="ensub serif">I read it all, so you don't have to.</div>
  <div class="lead">从智能体工程到可解释性，从 AI 经济学到 <b>$65B 融资与 IPO</b>——
    把这家最「反硅谷」的 AI 公司一年半的官方博客与论文，<b>拆成 6 张图讲清楚</b>。点开每章还能读原文摘要。</div>
  <div class="divider"></div>
  <div class="toc">{toc}</div>
  <div class="foot"><span>tech-blog-downloader</span><span class="tag">6 CHAPTERS</span></div>
</div></div></div>{nav(None, nxt, 0, total, is_cover=True)}</body></html>'''

# ── 生成 ────────────────────────────────────────────────────────────────────
pages = ["00-cover"] + [f'{ch["no"]}-{ch["en"].split()[0].lower().rstrip("&")}' for ch in CHAPTERS]
files = [p + ".html" for p in pages]
total = len(CHAPTERS)

def prev_next(i):
    return (files[i-1] if i > 0 else None), (files[i+1] if i < len(files)-1 else None)

p, n = prev_next(0)
with open(os.path.join(OUT, files[0]), "w", encoding="utf-8") as f:
    f.write(cover_html(n, total))
print(files[0])
for i, ch in enumerate(CHAPTERS):
    p, n = prev_next(i + 1)
    with open(os.path.join(OUT, files[i + 1]), "w", encoding="utf-8") as f:
        f.write(chapter_html(ch, p, n, i + 1, total))
    print(files[i + 1])

with open(os.path.join(OUT, "manifest.txt"), "w") as f:
    for p in pages:
        f.write(f"{p} {W} {H}\n")
print("done ·", len(pages), "pages")
