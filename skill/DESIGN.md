---
title: 网站设计规范
scope: generate_site.py 样式层
---

# 设计规范 — Warm Minimalism（Anthropic 风格）

`generate_site.py` 产出的网站对齐 Anthropic 官方视觉语言，以此文档为唯一真实来源。

## CSS Design Token

```css
:root {
  --bg:        #F0EEE6;   /* 暖米白 — Anthropic 页面底色 */
  --surface:   #FAFAF7;   /* 卡片面板白 */
  --surface-2: #E8E5DB;   /* 标签、代码背景、次级填充 */
  --ink:       #191919;   /* 主文字，近黑 */
  --ink-2:     #3D3B33;   /* 正文，带暖色调 */
  --muted:     #6B6B63;   /* 辅助文字、日期、说明 */
  --line:      #DBD7CC;   /* 主要分隔线/边框 */
  --line-2:    #C8C4B8;   /* 悬停时加深的边框 */

  /* 主色调 — Anthropic 陶土橙 */
  --accent:       #D97757;
  --accent-hover: #C15F3C;
  --accent-soft:  rgba(217,119,87,.10);

  --success:  #3D8B5E;    /* 已读绿 */
  --code-bg:  #ECEAE0;

  --shadow-sm: 0 1px 3px rgba(25,20,10,.07), 0 1px 2px rgba(25,20,10,.04);
  --shadow-md: 0 4px 18px rgba(25,20,10,.09), 0 2px 6px rgba(25,20,10,.05);

  --radius:      12px;
  --radius-sm:   8px;
  --radius-pill: 999px;
}
```

## 字体系统

```css
--font-serif: 'Fraunces', 'Noto Serif SC', Georgia, serif;  /* 大标题 */
--font-sans:  'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;  /* 正文 */
```

Google Fonts 引入（已内置于 generate_site.py）：
```
Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;0,9..144,900
Noto+Serif+SC:wght@500;600;700
Inter:wght@300;400;500;600;700
```

## 机构配色（org badge）

| 机构 | Hex | 机构 | Hex |
|---|---|---|---|
| Anthropic | `#D97757` | Qwen / 阿里 | `#615CED` |
| OpenAI | `#10A37F` | DeepSeek | `#4D6BFE` |
| Google DeepMind | `#4285F4` | 字节跳动 | `#325AB4` |
| Meta AI | `#0064E0` | 腾讯 | `#0052D9` |
| Microsoft | `#0A84FF` | 百度 | `#2932E1` |
| Mistral AI | `#FF7000` | MiniMax | `#E1341E` |
| Hugging Face | `#FF9D00` | 其他 | `#64748B` |
| NVIDIA | `#76B900` | | |

## 关键视觉规则

1. **Hero 背景纹理**：`radial-gradient` 圆点网格（18px pitch，opacity 0.45），仅限 hero 区域
2. **Eyebrow 标签**：全大写 + `letter-spacing .15em` + 右侧橙色短横线装饰
3. **卡片悬停**：仅 `translateY(-2px)` + shadow，背景色不变
4. **数字**：Fraunces serif，`font-weight 700`，`letter-spacing -.02em`
5. **Active chip**：`background: var(--ink)` + `color: #F0EEE6`（保持暖调）
6. **代码块背景**：`#1C1917`（暖黑）+ 文字 `#D6D3D1`
7. **Blockquote**：左侧 3px 陶土橙边框 + `var(--accent-soft)` 背景

## 禁止事项

- ❌ 冷蓝色（`#2563EB` 等）作为主色调
- ❌ 纯白（`#FFFFFF`）作为页面底色
- ❌ emoji 作为图标（用 SVG 代替）
- ❌ 无衬线字体用于 hero/文章大标题
- ❌ hover 时背景跳变为白色
