#!/usr/bin/env python3
"""install.py — 跨平台安装脚本（macOS / Linux / Windows 均适用）

bash install.sh 仅支持 macOS/Linux，此脚本作为通用替代。
"""
import os, sys, shutil
from pathlib import Path

SRC = Path(__file__).parent.resolve()
DEST = Path.home() / ".claude" / "skills" / "tech-blog-downloader"

EXCLUDES = {
    "wiki-site", ".git", "__pycache__", ".DS_Store",
    ".obsidian",    # 个人 Obsidian 工作区配置
    "install.py",   # 不把自身复制进去
}
EXCLUDE_SUFFIXES = {".pyc", ".png"}   # .png = anthropic-cards 本地截图产物
EXCLUDE_DIR_PATTERNS = {"site", ".obsidian"}   # */site/ 生成产物；.obsidian 个人配置


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    if path.is_dir() and path.name in EXCLUDE_DIR_PATTERNS:
        return True
    return False


def copy_tree(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if should_skip(item):
            continue
        d = dst / item.name
        if item.is_dir():
            copy_tree(item, d)
        else:
            shutil.copy2(item, d)


def main():
    print(f"📦 Installing tech-blog-downloader skill...")
    print(f"   From: {SRC}")
    print(f"   To:   {DEST}")

    # 删除旧版本（相当于 rsync --delete）
    if DEST.exists():
        shutil.rmtree(DEST)

    copy_tree(SRC, DEST)

    print()
    print("✅ Done! Restart Claude Code, then say:")
    print('   "抓取 Anthropic 工程博客最新 10 篇，生成中文学习站"')
    print()
    demo = DEST / "examples" / "site" / "index.html"
    if demo.exists():
        print(f"🎬 Preview demo site:")
        if sys.platform == "win32":
            print(f"   start {demo}")
        else:
            print(f"   open \"{demo}\"")


if __name__ == "__main__":
    main()
