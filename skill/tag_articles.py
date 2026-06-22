#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tag_articles.py — 基于关键词规则自动为文章补充语义话题标签

用法：
  python3 tag_articles.py <articles_dir>   # 默认 ~/Desktop/ai-blogs/articles
  python3 tag_articles.py --dry-run        # 预览，不写入
"""
import os, re, sys, json, argparse
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent.resolve()

# ── 话题检测规则（名称 + 关键词列表，在标题+摘要+正文前1000字中匹配）──────
TOPIC_RULES = [
    ("Agent",      ["agent", "agentic", "智能体", "multi-agent", "orchestrator"]),
    ("Eval/评测",    ["eval", " evals", "评测", "benchmark", "grader", "pass@k", "swe-bench"]),
    ("RAG/检索",     ["rag", "retrieval-augmented", "检索增强", "向量检索", "embedding",
                      "lightrag", "graphrag", "pageindex", "chunking", "reranking"]),
    ("MCP",        ["mcp", "model context protocol", "desktop extension"]),
    ("Claude Code",["claude code", "claude-code"]),
    ("可解释性",      ["interpretability", "mechanistic", "circuit tracing", "attribution",
                      "sparse autoencoder", "feature steering", "可解释性"]),
    ("安全/对齐",     ["safety", "alignment", "constitutional", "rlhf", "sycophancy",
                      "reward hacking", "对齐", "安全研究", "jailbreak", "red team"]),
    ("推理模型",      ["reasoning model", "extended thinking", "think tool", "chain-of-thought",
                      "deepseek-r1", "deepseek r1", "推理模型", "reasoning"]),
    ("代码模型",      ["code model", "coding model", "coder", "deepseekcoder",
                      "code generation", "代码模型", "编程模型"]),
    ("多模态",       ["multimodal", "vision", "-vl", "vl-", "vlm", "多模态",
                      "image generation", "audio model", "kimi-vl", "qwen-vl"]),
    ("经济影响",      ["economic index", "labor market", "productivity", "经济指数",
                      "劳动力市场", "生产力", "job displacement"]),
    ("MoE",        ["mixture-of-experts", "mixture of experts", "moe model", "sparse moe"]),
    ("长上下文",      ["long-context", "long context", "长上下文", "128k", "1m context",
                      "million token", "kimi", "context window"]),
    ("Harness工程",  ["harness engineering", "agent harness", "eval harness",
                      "scaffold", "agent infrastructure"]),
    ("开源模型",      ["open-source", "open source", "开源模型", "open weight",
                      "llama", "qwen", "baichuan", "minicpm", "deepseek-v"]),
    ("工具调用",      ["tool use", "tool design", "function call", "tool calling",
                      "工具调用", "工具设计"]),
]

# 这些是 org 名称，不应作为话题标签（避免重复）
ORG_NAMES = set()
try:
    for b in json.load(open(HERE / "blogs.json", encoding="utf-8"))["blogs"]:
        ORG_NAMES.add(b["org"])
except Exception:
    pass
# 合成类 org
ORG_NAMES |= {"AI 工程实践", "RAG 研究", "行业实践", "记忆系统", "其他"}


def parse_fm(content):
    if not content.lstrip().startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_raw, body = parts[1], parts[2]
    meta = {}
    for line in fm_raw.split("\n"):
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"\'')
    m = re.search(r'tags:\s*\[([^\]]*)\]', fm_raw)
    if m:
        meta["tags"] = [t.strip().strip('"\'') for t in m.group(1).split(",") if t.strip()]
    return meta, body


def detect_topics(title, summary, body_head):
    """根据规则检测话题标签"""
    text = (title + " " + summary + " " + body_head).lower()
    matched = []
    for topic, kws in TOPIC_RULES:
        if any(kw.lower() in text for kw in kws):
            matched.append(topic)
    return matched


def update_article(f, dry_run=False):
    content = f.read_text(encoding="utf-8")
    meta, body = parse_fm(content)
    title   = meta.get("title", f.stem).lower()
    summary = meta.get("summary", "").lower()
    body_head = body[:1500].lower()

    # 当前标签（剔除 org 名称和语义无关标签）
    current = meta.get("tags", [])
    if not isinstance(current, list):
        current = []
    keep = [t for t in current
            if t not in ORG_NAMES and t not in ("开源", "技术报告", "Release Notes")]

    # 检测新话题
    new_topics = detect_topics(title, summary, body_head)

    # 合并：org 来自 org 字段、旧保留标签、新话题（去重）
    org = meta.get("org", "")
    merged = []
    if org and org not in ORG_NAMES:   # 非官方公司 org 保留
        merged.append(org)
    for t in keep:
        if t not in merged:
            merged.append(t)
    for t in new_topics:
        if t not in merged:
            merged.append(t)
    merged = merged[:6]   # 最多 6 个标签

    if set(merged) == set(current):
        return False, merged   # 无变化

    if not dry_run:
        tags_str = ", ".join(f'"{t}"' for t in merged)
        # 替换 tags 行
        parts = content.split("---", 2)
        fm_raw = parts[1]
        if "tags:" in fm_raw:
            fm_raw = re.sub(r'tags:\s*\[[^\]]*\]', f'tags: [{tags_str}]', fm_raw)
        else:
            fm_raw = fm_raw.rstrip() + f'\ntags: [{tags_str}]\n'
        f.write_text("---" + fm_raw + "---" + parts[2], encoding="utf-8")

    return True, merged


def main():
    p = argparse.ArgumentParser(description="自动为文章补充语义话题标签")
    p.add_argument("dir", nargs="?",
                   default=str(Path.home() / "Desktop" / "ai-blogs" / "articles"),
                   help="articles 目录路径")
    p.add_argument("--dry-run", action="store_true", help="预览，不写入")
    args = p.parse_args()

    articles_dir = Path(args.dir)
    if not articles_dir.exists():
        print(f"[错误] 目录不存在: {articles_dir}"); sys.exit(1)

    files = sorted(articles_dir.glob("*.md"))
    print(f"{'预览' if args.dry_run else '处理'} {len(files)} 篇文章...\n")

    changed = 0
    topic_count = Counter()
    for f in files:
        updated, tags = update_article(f, dry_run=args.dry_run)
        if updated:
            changed += 1
            for t in tags:
                topic_count[t] += 1

    print(f"{'更新' if not args.dry_run else '将更新'}: {changed} 篇\n")
    print(f"{'标签':20s} 篇数")
    print("─" * 30)
    for tag, cnt in topic_count.most_common():
        print(f"  {tag:18s} {cnt}")


if __name__ == "__main__":
    main()
