---
name: emilkowalski-apple-design
description: "Apple设计品味Skill (25K⭐) — Emil Kowalski的WWDC设计原则+设计工程哲学。10个skill覆盖：Apple流体界面、动画决策框架、Spring物理、组件构建、手势交互、CSS Transform、clip-path动画、性能优化。严格Apple原版，零AI味。"
version: 1.0.0
author: emilkowalski + 小黑
license: MIT
metadata:
  hermes:
    tags: [apple, design, animation, ui, css, spring, gesture, typography]
    related_skills: [taste-skill, design-taste-system, nothing-design, open-design]
---

# Apple Design Skill — 25K⭐ 原版部署

**来源:** https://github.com/emilkowalski/skills
**作者:** Emil Kowalski (前Vercel/Linear设计师)
**核心:** WWDC 2018 Designing Fluid Interfaces + WWDC 2020 Typography + WWDC 2026 Principles

## 10个子Skill

| Skill | 行数 | 用途 |
|-------|------|------|
| **apple-design** | 282 | Apple流体界面17条原则（响应/直接操控/可中断/弹簧/速度传递/动量投射/空间一致性/橡皮筋/材质/排版） |
| **emil-design-eng** | 674 | 设计工程哲学（动画决策框架/Spring配置/组件构建/CSS Transform/clip-path/手势/性能） |
| **animate** | 199 | 动画实现指南 |
| **animation-vocabulary** | 173 | 动画词汇表（描述动效的标准语言） |
| **find-animation-opportunities** | 132 | 发现动画机会 |
| **improve-animations** | 101 | 改进现有动画 |
| **review-animations** | 112 | 动画审查标准 |
| **prototype** | 90 | 快速原型 |
| **ask-sonner** | 80 | Toast通知（Sonner库） |
| **pick-ui-library** | 77 | UI库选型 |

## 核心规则（强制执行）

### 设计原则
1. **响应** — pointer-down就反馈，不等click
2. **直接操控** — 拖拽1:1跟踪手指
3. **可中断性** — 所有动画必须可随时中断反转
4. **弹簧>时长** — 用spring不用fixed-duration
5. **速度传递** — 手势结束时传递释放速度
6. **动量投射** — 用速度预测落点，不snap最近边界
7. **空间对称** — 进出同路径
8. **橡皮筋** — 边界渐进阻力，不硬停
9. **材质层次** — 毛玻璃半透明，不抢焦点
10. **排版** — 字间距随字号变化，大字号收紧

### 动画决策框架（必须遵守）
- 100次/天的操作 → **禁止动画**
- 10次/天 → 移除或大幅减少
- 偶尔 → 标准动画
- 罕见 → 可加delight

### Spring默认值
```css
/* 默认临界阻尼，无回弹 */
{ type: "spring", bounce: 0, duration: 0.4 }
/* 动量交互才有轻微回弹 */
{ type: "spring", bounce: 0.2, duration: 0.4 }
```

### 禁止行为
- ❌ `ease-in` 用于UI动画（启动慢=感觉迟钝）
- ❌ `scale(0)` 入场（现实中东西不会从无到有）
- ❌ `transition: all` （必须指定具体属性）
- ❌ 键盘触发动画（高频操作禁止动画）
- ❌ `transform-origin: center` 用于弹出框（必须跟随触发源）
- ❌ 硬编码像素值（用百分比/rem）

### 必须行为
- ✅ `:active` 状态 `scale(0.97)` （按钮必须有按压反馈）
- ✅ `ease-out` 用于入场（启动快=感觉响应）
- ✅ `backdrop-filter: blur()` 用于导航/工具栏
- ✅ 字间距随字号变化（大字号 `-0.02em`，正文 `0`）
- ✅ 只动画 `transform` 和 `opacity` （GPU加速）
- ✅ `@starting-style` 替代JS入场动画

## 使用方式

当用户要求设计UI/网页/组件时：
1. 加载 `references/apple-design/SKILL.md` — Apple设计原则
2. 加载 `references/emil-design-eng/SKILL.md` — 设计工程实践
3. 按规则生成代码，不加任何AI味装饰

## 与现有skill的关系

| Skill | 关系 |
|-------|------|
| taste-skill | 反AI味引擎，本skill提供Apple正面范例 |
| design-taste-system | 8种风格，本skill是Apple风格的权威实现 |
| nothing-design | Nothing品牌风格，独立体系 |
| open-design | 149套大厂设计语言，本skill是Apple的深度版 |

## 关键Pitfall

- **Spring不是duration** — spring没有固定时长，settling time是参数的涌现结果
- **bounce只用于动量交互** — 菜单淡入不要bounce，卡片flick才要
- **CSS变量有继承开销** — 大量子元素时直接改transform，不改CSS变量
- **Framer Motion的x/y不是GPU加速** — 必须用完整transform字符串
- **blur不要超过20px** — Safari性能问题
