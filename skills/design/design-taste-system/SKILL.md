---
name: design-taste-system
description: >-
  设计品味系统：给AI注入高级设计品味，生成高端、非通用的UI界面。
  包含8种设计风格（taste-skill、gpt-taste、minimalist、soft、brutalist等），
  反AI垃圾设计，Awwwards级别输出。
version: 1.0.0
author: Hermes Agent (基于 Leonxlnx/taste-skill)
activation: /taste
license: MIT
metadata:
  created: 2026-04-17
  sources:
    - https://github.com/Leonxlnx/taste-skill
    - https://tasteskill.dev
---

# /taste

设计品味系统：给AI注入高级设计品味，生成高端、非通用的UI界面。

## 触发条件

当用户提到以下内容时激活：
- "设计要有品味"
- "不要AI味"
- "高端UI"
- "Awwwards级别"
- "反通用设计"
- "premium design"

## 核心理念

**问题**：标准LLM有严重的统计偏差，会生成：
- 无聊、通用的界面
- 6行换行的标题
- 丑陋的空白间隙
- 重复的左/右布局
- 便宜的emoji和图标

**解决方案**：注入设计品味规则，强制打破默认模式。

## 基准配置

### 默认参数
```yaml
DESIGN_VARIANCE: 8      # 1=完美对称, 10=艺术混乱
MOTION_INTENSITY: 6     # 1=静态, 10=电影级动效
VISUAL_DENSITY: 4       # 1=画廊级留白, 10=驾驶舱级密集
```

### 架构约定
- **框架**：React/Next.js (默认Server Components)
- **样式**：Tailwind CSS v3/v4（先检查版本）
- **状态**：useState/useReducer（本地），全局状态避免prop-drilling
- **图标**：Radix、Phosphor（禁止emoji）
- **布局**：CSS Grid（禁止复杂flex计算）

## 8种设计风格

### 1. taste-skill（主技能）
**核心规则**：
- 硬件加速CSS动画
- 平衡的设计工程
- 严格组件架构
- 基于度量的规则

**使用场景**：通用高端前端

### 2. gpt-taste（Awwwards级）
**核心规则**：
- Python驱动的真随机布局（打破循环）
- AIDA页面结构
- 宽编辑器排版（禁止6行换行）
- GSAP ScrollTriggers（pinning, stacking, scrubbing）
- 无间隙bento grids

**使用场景**：获奖级作品集、品牌官网

### 3. minimalist-skill（极简编辑风）
**核心规则**：
- 暖单色调色板
- 排版对比
- 扁平bento grids
- 柔和粉彩
- 无渐变、无重阴影

**禁用**：Inter/Roboto字体、Lucide图标、重阴影

**使用场景**：Notion/Linear风格工具

### 4. soft-skill（高端软UI）
**核心规则**：
- 贵族级字体（Geist、Clash Display、PP Editorial New）
- 超细线条图标（Phosphor Light）
- 微妙阴影（< 0.05不透明度）
- 弹簧动画
- 触觉深度感

**使用场景**：高端SaaS、 agency作品

### 5. output-skill（强制完整输出）
**核心规则**：
- 禁止省略代码（// ... , // rest of code）
- 禁止占位符（// TODO, // implement here）
- 禁止截断输出
- 交叉检查交付物数量

**使用场景**：任何需要完整代码的任务

### 6. brutalist-skill（工业粗野主义）
**核心规则**：
- 瑞士排版 + 军事终端美学
- 极端字体比例对比
- 纯实用色彩
- 模拟退化效果（半色调、CRT扫描线）
- 高数据密度

**使用场景**：数据仪表板、解密蓝图风格

### 7. redesign-skill（项目升级）
**核心规则**：
- 审计现有设计问题
- 修复优先
- 渐进升级

**使用场景**：改造旧项目

### 8. stitch-skill（Google Stitch）
**核心规则**：
- 生成DESIGN.md文件
- 语义设计系统
- AI友好的自然语言规则

**使用场景**：配合Google Stitch使用

## 核心规则详解

### 视口稳定性
```css
/* ❌ 错误 - 移动端布局跳跃 */
h-screen

/* ✅ 正确 - 稳定高度 */
min-h-[100dvh]
```

### Grid > Flex
```css
/* ❌ 复杂flex计算 */
w-[calc(33%-1rem)]

/* ✅ CSS Grid */
grid-cols-3 gap-4
```

### 字体选择
```css
/* ❌ 禁用 - AI默认 */
Inter, Roboto, Open Sans, Arial, Helvetica

/* ✅ 高端字体 */
Geist, Clash Display, PP Editorial New, Plus Jakarta Sans, Satoshi, Cabinet Grotesk, Outfit
```

### 图标选择
```css
/* ❌ 禁用 - 粗线条 */
Lucide, FontAwesome, Material Icons, Heroicons

/* ✅ 细线条 */
Phosphor Light, Remix Line, Radix Icons
```

### 阴影处理
```css
/* ❌ 禁用 - 重阴影 */
shadow-md, shadow-lg, shadow-xl

/* ✅ 超微妙 */
shadow-[0_1px_2px_rgba(0,0,0,0.02)]
```

## 实战示例

### 示例1：使用taste-skill生成Hero区域
```tsx
// 高端Hero - 硬件加速动效
<section className="min-h-[100dvh] flex items-center">
  <div className="max-w-[1400px] mx-auto px-6">
    <h1 className="text-7xl font-semibold tracking-tight">
      未来已来
    </h1>
    <p className="mt-6 text-xl text-neutral-500 max-w-2xl">
      重新定义数字体验
    </p>
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-8 px-8 py-4 bg-neutral-900 text-white"
    >
      开始探索
    </motion.button>
  </div>
</section>
```

### 示例2：使用gpt-taste的AIDA结构
```tsx
// A: Attention - 创意导航栏
<nav className="fixed top-6 left-1/2 -translate-x-1/2 z-50">
  <div className="px-6 py-3 bg-white/80 backdrop-blur-xl rounded-full">
    {/* 玻璃效果导航 */}
  </div>
</nav>

// I: Interest - Hero + GSAP动画
// D: Desire - 功能展示 + bento grid
// A: Action - CTA + 表单
```

### 示例3：minimalist风格
```tsx
// 极简编辑风
<article className="max-w-3xl mx-auto px-6 py-24">
  <header className="border-b border-neutral-200 pb-8">
    <time className="text-sm text-neutral-400">2026年4月</time>
    <h1 className="mt-2 text-4xl font-light tracking-tight">
      设计的未来
    </h1>
  </header>
  <div className="mt-12 prose prose-neutral">
    {/* 内容 */}
  </div>
</article>
```

## 与标准AI输出对比

| 特征 | 标准AI | taste-skill |
|------|--------|-------------|
| 字体 | Inter | Geist/Clash Display |
| 布局 | 重复左/右 | 真随机变化 |
| 间距 | 不一致 | 基于度量 |
| 动效 | 简单fade | GSAP ScrollTrigger |
| 输出 | 截断/省略 | 完整交付 |
| emoji | 滥用 | 完全禁止 |

## 安装使用

### 通过npx安装
```bash
npx skills add https://github.com/Leonxlnx/taste-skill
```

### 手动复制技能
```bash
# 复制特定技能到你的skills目录
cp -r taste-skill/skills/taste-skill ~/.hermes/skills/design/
```

## 最佳实践

1. **先选择风格** - 根据项目类型选择合适的skill
2. **遵守禁用规则** - 严格避免禁用的字体、图标、模式
3. **使用真随机** - 打破重复布局模式
4. **硬件加速** - 所有动效使用transform/opacity
5. **完整输出** - 不要省略任何代码

## 常见错误

### 错误1：使用Inter字体
```tsx
// ❌
font-family: 'Inter', sans-serif

// ✅
font-family: 'Geist', sans-serif
```

### 错误2：复杂flex计算
```tsx
// ❌
<div className="w-[calc(33.333%-1rem)]">

// ✅
<div className="col-span-1">
```

### 错误3：使用emoji
```tsx
// ❌
<span>🚀 开始</span>

// ✅
<span>开始</span>
// 或使用图标
< RocketIcon />
```

---
*基于 Leonxlnx/taste-skill 仓库 (9072 stars)*
*支持风格: taste-skill, gpt-taste, minimalist, soft, output, brutalist, redesign, stitch*
