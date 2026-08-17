# TapNow 工作空间真实DOM数据（Safari提取 2026-07-05）

## 提取方法
AppleScript + base64编码JS → Safari `do JavaScript` → getComputedStyle

## CSS变量（:root真实值）
- --background: #0f0f0f
- --background-canvas: #0a0a0a
- --card: #1f1f1f
- --foreground: #f5f5f5
- --muted-foreground: #7a7a7a
- --primary: #1fa2dc
- --border: #ffffff1a
- --font-sans: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- --font-mono: JetBrains Mono, monospace
- --radius: .75rem (12px)

## Body
background: rgb(0,0,0) → #000000（纯黑）
margin: 0, padding: 0

## 画布 (.react-flow)
background: transparent; 背景层: rgb(0,0,0); 点阵radius: 0.155

## 连线 (.react-flow__edge path)
stroke: rgba(255,255,255,0.376), stroke-width: 2px

## Handle
6x6px transparent; PlusIcon: 24x24px, border 2px solid #7a7a7a, border-radius full

## 节点卡片
bg: #1f1f1f, border-radius: 16px, no shadow, no border, min 250px

## 节点选中
outline: #7a7a7a solid 2px (不是border)

## 控制面板
absolute bottom:-8px, z-index:20, min-width:640px
卡片: #1f1f1f, 16px, 1px border rgba(255,255,255,0.1)

## 生成按钮
26px白色圆形, bg:white, color:black

## 侧边栏 (Radix Popover)
240px, bg zinc-900, border zinc-700, 12px圆角
blur-3xl装饰(蓝#0093FF+橙#F15B0E), opacity:20%
节点选项: 52px高, 16px圆角

## 右键菜单
bg-card/85, backdrop-blur-xl, w-240px, 16px圆角
cmdk库实现, 快捷键: #7a7a7a tracking-widest

## 模型下拉框
280px, bg #292929, 16px圆角, 选中 bg-white/10

## 关键发现
1. 无MiniMap, 无默认Controls
2. 预览是节点内absolute覆盖层(z-1000), 非独立弹窗
3. 控制面板两种形态: 展开面板(640px) vs 胶囊栏(h-12 rounded-full)
4. 无box-shadow无backdrop-filter
5. 所有弹出层用cmdk库
