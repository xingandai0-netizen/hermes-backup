---
name: design-motion-principles
description: 动效设计审计。基于Emil Kowalski/Jakub Krehel/Jhey Tompkins的技术进行动效审查。触发：审查UI动画、过渡效果、hover状态、动效设计。
version: 1.0
source: kylezantos/design-motion-principles (405 stars)
---

# Design Motion Audit

## 三大设计师视角
- **Emil Kowalski** (Linear/ex-Vercel): 克制、速度、有目的的动效。适合生产力工具
- **Jakub Krehel**: 微妙的产级打磨。适合消费级App
- **Jhey Tompkins**: 趣味实验、CSS创新。适合创意站点

## 审计流程

### Step 1: 上下文理解
- 了解项目类型和设计意图
- 检查package.json判断应用类型
- 搜索现有动画模式: motion/animate/transition/@keyframes
- 分析组件结构: 创意站/SaaS/营销/儿童App

### Step 2: 动效缺口分析
- 查找条件渲染未包裹AnimatePresence
- 检查enter/exit动画缺失
- 搜索UI切换无过渡效果

### Step 3: 加权审查
根据项目类型分配设计师权重，对比各设计师标准

### Step 4: 按优先级输出建议
1. 破坏性缺陷(布局偏移/闪烁)
2. WCAG无障碍(prefers-reduced-motion)
3. 视觉打磨
4. 创意加分
