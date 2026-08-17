---
name: baseline-ui
description: UI基线校验器。验证动画时长、排版层级、组件无障碍、防布局反模式。触发：构建UI组件、审查CSS、React视图样式、设计一致性。
version: 1.0
source: ibelick/ui-skills (1.6K stars)
---

# Baseline UI

## 使用方式
- `/baseline-ui` — 对当前对话的UI工作施加约束
- `/baseline-ui <file>` — 审查文件，输出违规项+原因+修复

## 技术栈
- 默认Tailwind CSS，除非已有自定义值
- JS动画用motion/react(原framer-motion)
- 入场微动画用tw-animate-css
- class合并用cn(clsx+tailwind-merge)

## 组件规范
- 键盘/焦点行为必须用无障碍组件(Base UI/React Aria/Radix)
- 优先用项目已有组件
- 图标按钮必须加aria-label
- 严禁手写键盘/焦点逻辑

## 交互规范
- 破坏性操作必须用AlertDialog
- 加载状态用骨骼屏
