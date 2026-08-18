---
name: design-skills-ecosystem
description: 设计类Claude Code skills的完整生态系统映射。覆盖taste-skill、ui-skills、design-motion-principles、better-icons、open-design等核心设计技能。包含GitHub repo对应关系、安装方法、关键特性。当用户提到设计技能、品味技能、UI技能、动效审计、图标搜索、设计语言文档包时触发。
tags: [design, skills, claude-code, taste, ui, motion, icons, open-design]
version: 1.0
created: 2026-05-10
---

# 设计技能生态系统

## 核心设计技能映射

| 常用名称 | GitHub Repo | Stars | 说明 |
|---------|------------|-------|------|
| impeccable/taste | `Leonxlnx/taste-skill` | 16.5K | AI品味/反slop，含12个子skill |
| skill/ui skills | `ibelick/ui-skills` | 1.6K | 设计工程师技能，4个skill |
| motion ai kit | `kylezantos/design-motion-principles` | 405 | 动效设计审计(Emil Kowalski/Jakub Krehel/Jhey Tompkins) |
| better icons | `better-auth/better-icons` | 995 | 图标搜索MCP Server，200K+图标150+集合 |
| design.cd | `nexu-io/open-design` | 35.6K | 大厂设计语言AI文档包，123个skill+149套设计系统 |

## 安装方法

所有技能安装到 `~/.claude/skills/`，Claude Code自动发现。

### 批量克隆安装
```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills
git clone https://github.com/Leonxlnx/taste-skill.git &
git clone https://github.com/ibelick/ui-skills.git &
git clone https://github.com/kylezantos/design-motion-principles.git &
git clone https://github.com/better-auth/better-icons.git &
git clone https://github.com/nexu-io/open-design.git design-cd &
wait
```

### 各技能安装细节

**taste-skill**: 用skill.sh注册，或直接复制skills目录
```bash
cp -r taste-skill/skills/* ~/.claude/skills/taste-skills/
```

**ui-skills**: 运行install.sh
```bash
cd ui-skills && bash install.sh
```

**design-motion-principles**: 注意skills嵌套在`skills/design-motion-principles/`下
```bash
cp -r design-motion-principles/skills/design-motion-principles ~/.claude/skills/
```

**better-icons**: 单文件skill
```bash
cp better-icons/skills/SKILL.md ~/.claude/skills/better-icons.md
```

**open-design (design.cd)**: 123个skill，复制skills目录
```bash
cp -r design-cd/skills ~/.claude/skills/open-design-skills
```
另有149套设计系统在`design-cd/design-systems/`（Apple, Material, IBM, Airbnb, Stripe等）

## 搜索技巧

当用户提到不明确的技能名称时：
1. 先按精确repo名搜索：`curl api.github.com/repos/<name>`
2. 按关键词搜索：`curl api.github.com/search/repositories?q=<keywords>`
3. 若"design.cd"等带点号的名字找不到，可能是约定俗成的别名，需找最匹配的仓库
4. 设计类技能常以"skill"结尾，taste类在Leonxlnx组织下

## macOS图片编辑（Pillow）

用于生成设计类技能所需图片时的参考：

```python
from PIL import Image, ImageDraw, ImageFont

# macOS中文字体
font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
font = ImageFont.truetype(font_path, size=54, index=2)  # index=2是粗体
# 其他可选: index=0(常规), index=1(常规), index=2(粗体), index=3(粗体)

# 简洁卡片生成
img = Image.new("RGBA", (1200, 380), (245, 245, 245, 255))
draw = ImageDraw.Draw(img)
text = "开始使用ANTOKEX"
bbox = draw.textbbox((0, 0), text, font=font)
x = (W - (bbox[2]-bbox[0])) // 2
y = (H - (bbox[3]-bbox[1])) // 2
draw.text((x, y), text, fill=(0, 0, 0), font=font)
img.save("output.png", "PNG")
```

## 坑点

- `design-motion-principles`的skills目录嵌套了一层，不能直接`cp skills/*`
- `better-icons`是单SKILL.md而非目录结构
- `open-design`是全栈应用(Electron+Next.js+daemon)，仅取其skills/和design-systems/目录用于Claude Code
- macOS上`fc-list`不可用，需用`find /System/Library/Fonts`找字体
- Hiragino Sans GB是.ttc格式，Pillow需指定index参数
