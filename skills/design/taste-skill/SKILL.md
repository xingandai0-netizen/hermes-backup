---
name: taste-skill
description: AI品味引擎。消除AI生成的乏味/slop UI，强制使用工程化设计规则。触发：UI设计、网页生成、前端开发、视觉审计。
version: 1.0
source: Leonxlnx/taste-skill (16.5K stars)
---

# Taste-Skill — AI品味层

## 基线配置
- DESIGN_VARIANCE: 8 (1=完美对称, 10=艺术混乱)
- MOTION_INTENSITY: 6 (1=静态, 10=电影级)
- VISUAL_DENSITY: 4 (1=极简, 10=驾驶舱密集)

## 核心规则

### Rule 1: 排版
- 标题默认 text-4xl md:text-6xl tracking-tighter leading-none
- 正文 text-base text-gray-600 leading-relaxed max-w-[65ch]
- 禁止Inter用于"高级/创意"场景，用Geist/Outfit/Satoshi
- 仪表盘/软件UI严禁Serif字体

### Rule 2: 色彩
- 最多1种强调色，饱和度<80%
- 严禁AI紫色/蓝色霓虹美学
- 用中性基调(Zinc/Slate) + 单一强调色

### Rule 3: 布局
- LAYOUT_VARIANCE>4时严禁居中Hero
- 强制分屏/左对齐/不对称留白

### Rule 4: 卡片纪律
- VISUAL_DENSITY>7时禁止generic卡片
- 用border-t/divide-y/负空间替代

### Rule 5: 状态完整性
- 必须实现Loading(骨骼屏)/Empty/Error全状态

### 铁律
- 严禁Emoji → 用Phosphor/Radix图标
- 严禁h-screen → 用min-h-[100dvh]
- 严禁复杂的flex百分比数学 → 用CSS Grid
- 用前检查package.json，不假设库存在
- **中文界面**：用户(阿戴)要求所有UI文字使用中文，不使用英文。按钮、标签、提示、状态信息全部中文化。品牌名(Antoken)和技术术语(Prompt、API)可保留英文。
