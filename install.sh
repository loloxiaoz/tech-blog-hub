#!/usr/bin/env bash
# install.sh — 一键安装 tech-blog-downloader 技能
# 支持：Claude Code (CC) / OpenClaw / WorkBuddy
set -e

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 检测目标平台 ──────────────────────────────────────────────────────────
detect_platform() {
  if [ -n "$WORKBUDDY_HOME" ] || [ -d "${HOME}/.workbuddy" ]; then
    echo "workbuddy"
  else
    echo "claude"   # Claude Code / OpenClaw 共用 ~/.claude/skills/
  fi
}

PLATFORM="${INSTALL_PLATFORM:-$(detect_platform)}"

case "$PLATFORM" in
  workbuddy)
    SKILL_DIR="${HOME}/.workbuddy/skills-marketplace/skills/tech-blog-downloader"
    ;;
  *)
    SKILL_DIR="${HOME}/.claude/skills/tech-blog-downloader"
    ;;
esac

echo "📦 Installing tech-blog-downloader skill..."
echo "   Platform: $PLATFORM"
echo "   From: $SRC_DIR"
echo "   To:   $SKILL_DIR"

mkdir -p "$SKILL_DIR"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude='wiki-site/' --exclude='output/' --exclude='*/site/' \
    --exclude='.git/' --exclude='__pycache__/' --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='.obsidian/' \
    --exclude='anthropic-cards/*.png' \
    "$SRC_DIR/" "$SKILL_DIR/"
else
  cp -r "$SRC_DIR/." "$SKILL_DIR/"
  rm -rf "$SKILL_DIR/examples/site" "$SKILL_DIR/__pycache__" \
         "$SKILL_DIR/.git" "$SKILL_DIR/.obsidian"
  find "$SKILL_DIR" -name "*.pyc" -delete 2>/dev/null || true
  find "$SKILL_DIR/anthropic-cards" -name "*.png" -delete 2>/dev/null || true
fi

echo ""
echo "✅ Done! Restart your AI assistant, then say:"
echo "   \"抓取 Anthropic 工程博客最新 10 篇，生成中文学习站\""
echo ""
echo "🎬 Preview demo:"
echo "   python3 $SKILL_DIR/generate_site.py"
echo "   open $SKILL_DIR/examples/site/index.html"
echo ""

# 提示安装 Python 依赖（fetcher.py 本机抓取需要）
if ! python3 -c "import requests, bs4" 2>/dev/null; then
  echo "⚠️  Optional: install Python deps for local fetching (fetcher.py):"
  echo "   pip install requests beautifulsoup4"
fi
