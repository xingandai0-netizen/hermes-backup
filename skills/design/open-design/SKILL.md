---
name: open-design
description: 大厂设计语言AI文档包。149套企业设计系统(Apple/Material/IBM/Meta/Airbnb等)+123个产出技能。触发：需要参考大厂设计规范、应用特定品牌设计语言、生成符合企业设计标准的界面。
version: 1.0
source: nexu-io/open-design (35.6K stars)
---

# Open Design — 大厂设计语言包

## 设计系统 (149套)
位于 `~/.claude/skills/design-cd/design-systems/`

### 常用品牌
- apple: Apple Human Interface
- material: Google Material Design
- ibm: IBM Carbon
- meta: Meta设计语言
- airbnb: Airbnb设计系统
- ant: Ant Design
- stripe: Stripe设计语言
- notion: Notion设计风格
- linear: Linear设计
- vercel: Vercel设计

### 使用方式
```bash
# 查看某品牌设计规范
cat ~/.claude/skills/design-cd/design-systems/<brand>/DESIGN.md

# 列出所有可用设计系统
ls ~/.claude/skills/design-cd/design-systems/
```

## 产出技能 (123个)
位于 `~/.claude/skills/design-cd/skills/`

### 常用技能类型
- 网页: landing-page, dashboard, docs-page, portfolio
- 移动: dating-web, mobile-app
- 内容: blog-post, editorial, magazine
- 商业: pitch-deck, design-brief, proposal
- 视觉: 8-bit-orbit-video, audio-jingle

## Craft规则 (通用)
位于 `~/.claude/skills/design-cd/craft/`
- anti-ai-slop.md: 反AI垃圾设计
- typography.md + typography-hierarchy.md: 排版体系
- color.md: 色彩理论
- animation-discipline.md: 动画纪律
- accessibility-baseline.md: 无障碍基线
- laws-of-ux.md: UX法则
- rtl-and-bidi.md: 多语言适配
