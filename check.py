#!/usr/bin/env python3
"""环境检查 + 快速功能验证 — 安装后运行此脚本确认一切正常"""
import sys, os, json, subprocess, platform

HERE = os.path.dirname(os.path.abspath(__file__))
OK, WARN, FAIL = "✅", "⚠️ ", "❌"

def check(label, ok, detail=""):
    symbol = OK if ok else FAIL
    print(f"  {symbol} {label}" + (f"  ({detail})" if detail else ""))
    return ok

def main():
    print(f"\ntech-blog-downloader — 环境检查\n{'─'*40}")
    all_ok = True

    # Python 版本
    v = sys.version_info
    ok = v >= (3, 7)
    all_ok &= check(f"Python {v.major}.{v.minor}.{v.micro}", ok,
                    "需要 3.7+" if not ok else "")

    # 关键文件存在
    for fname in ["generate_site.py", "blogs.json", "SKILL.md", "DESIGN.md"]:
        p = os.path.join(HERE, fname)
        all_ok &= check(fname, os.path.exists(p),
                        "文件缺失" if not os.path.exists(p) else "")

    # blogs.json 格式
    try:
        data = json.load(open(os.path.join(HERE, "blogs.json")))
        count = len(data.get("blogs", []))
        check(f"blogs.json 解析正常（{count} 个来源）", True)
    except Exception as e:
        all_ok &= check("blogs.json 解析", False, str(e))

    # 样例文章存在
    articles_dir = os.path.join(HERE, "examples", "articles")
    articles = [f for f in os.listdir(articles_dir) if f.endswith(".md")] if os.path.isdir(articles_dir) else []
    check(f"样例文章（{len(articles)} 篇）", len(articles) > 0, "examples/articles/ 为空" if not articles else "")

    # 试跑 generate_site.py
    print(f"\n  正在试跑 generate_site.py（使用样例文章）...")
    try:
        out_dir = os.path.join(HERE, "_check_output")
        result = subprocess.run(
            [sys.executable, os.path.join(HERE, "generate_site.py"),
             articles_dir, out_dir, "--title", "检查测试站"],
            capture_output=True, text=True, timeout=30
        )
        ok = result.returncode == 0 and os.path.exists(os.path.join(out_dir, "index.html"))
        all_ok &= check("generate_site.py 运行成功", ok,
                        result.stderr.strip()[:80] if not ok else "")
        if ok:
            import shutil
            shutil.rmtree(out_dir, ignore_errors=True)
    except subprocess.TimeoutExpired:
        all_ok &= check("generate_site.py 运行超时", False, "超过 30s")
    except Exception as e:
        all_ok &= check("generate_site.py 运行异常", False, str(e))

    # Claude Code 技能安装状态
    skills_path = os.path.expanduser("~/.claude/skills/tech-blog-downloader/SKILL.md")
    installed = os.path.exists(skills_path)
    status = "已安装" if installed else "未安装（运行 bash install.sh）"
    check(f"Claude Code 技能安装状态", installed, status)

    print(f"\n{'─'*40}")
    if all_ok:
        print(f"  {OK} 全部检查通过！可以开始使用了。")
        print(f"\n  快速体验：")
        print(f"    python3 generate_site.py")
        print(f"    open examples/site/index.html")
    else:
        print(f"  {FAIL} 有问题需要修复，请查看上方错误信息。")
        print(f"  如有疑问，确认 Python >= 3.7 且技能文件完整。")
    print()

if __name__ == "__main__":
    main()
