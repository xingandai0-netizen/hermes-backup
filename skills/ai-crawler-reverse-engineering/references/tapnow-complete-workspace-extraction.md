# TapNow 工作空间完整提取数据
# 来源: app.tapnow.ai Safari实时DOM提取 (AppleScript+JS)
# 日期: 2026-07-05
# 提取方法: AppleScript -> Safari window 3 tab 4 -> JavaScript -> getComputedStyle
# 页面: "电商鞋子宣传视频 (copy)" — 48个节点, 42条连线

## Computed Styles (getComputedStyle真实值)

### Body
- background: rgb(0,0,0) → #000000
- font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- color: rgb(245,245,245) → #f5f5f5

### 画布 (.react-flow)
- background: transparent (rgba(0,0,0,0))
- 实际背景 (.react-flow__background): rgb(0,0,0) → #000000

### 连线 (.react-flow__edge path)
- stroke: rgba(255,255,255,0.376) → ~37.6%白色
- stroke-width: 2px
- fill: none

### Handle (.react-flow__handle)
- 6x6px, transparent, position:absolute

### Handle PlusIcon (.node-handle-plus svg)
- 24x24px, border:2px solid #7a7a7a, border-radius:9999px
- transition: color 0.15s cubic-bezier(0.4,0,0.2,1)

### 节点卡片 (.react-flow__node .bg-card)
- background: rgb(31,31,31) → #1f1f1f
- border-radius: 16px
- border: 0px (无边框)
- box-shadow: none (无阴影)
- min-width: 250px, min-height: 250px
- overflow: visible

### 节点选中 (.react-flow__node.selected .bg-card)
- outline: rgb(122,122,122) solid 2px → #7a7a7a
- outline-offset: 0px

### 节点标题栏
- position:absolute, transform:translateY(-100%), left:4px, pb:8px
- color: rgba(245,245,245,0.6)

### 控制面板 (.node-float-ui)
- position:absolute, bottom:-8px, z-index:20
- min-width:640px, max-width:650px

### 控制面板卡片
- background: rgb(31,31,31) → #1f1f1f
- border-radius: 16px
- border: 1px solid rgba(255,255,255,0.1)
- box-shadow: rgba(0,0,0,0.1) 0px 2px 4px, 0px 4px 6px -1px
- margin-top: 8px

### 编辑器 (.ProseMirror)
- font-size: 16px, line-height: 25.6px (1.6)
- color: #f5f5f5, padding: 0 12px 8px, min-height: 80px

### 生成按钮
- 26x26px, border-radius:9999px (圆形), bg:white, color:black
- transition: 0.15s cubic-bezier(0.4,0,0.2,1)

### 上传按钮
- 38x38px, border-radius:10px, bg:rgba(255,255,255,0.08)

### 节点内容区
- scrollbar-width: thin

## 侧边栏

### 触发按钮
- 40x40px圆形, bg:#2b2b2b, left:22px

### 面板 (Radix Popover)
- width:240px, bg:zinc-900, border:1px zinc-700, border-radius:12px
- blur-3xl光晕装饰: blue #0093FF + orange #F15B0E, opacity:20%
- 标题"添加节点": 12px, #7a7a7a, padding:6px 8px
- 节点项: h-52px, p-8px, rounded-16px, gap-8px, text-16px
- 8个节点类型: Text/Image/Video/Audio/3D/Playlist/ImageEditor/Upload
- hover效果: 名称translateY(10px→0), 描述opacity(0→1)

## 右键菜单
- bg-card/85, backdrop-blur-xl, w-240px, rounded-2xl, p-1
- 菜单项: p-3, rounded-lg, text-sm
- 复制⌘C / 粘贴⌘V / 副本 / 删除⌫

## 关键发现
1. 节点无shadow无backdrop-filter — 纯色#1f1f1f
2. 选中用outline不是border
3. Handle 6px透明 + 24px PlusIcon
4. 连线37.6%白色 2px
5. 控制面板从节点底部伸出(bottom:-8px)
6. 生成按钮26px白色圆形极小但突出
7. 工具栏在右上角(React Flow Panel)不是顶部通栏
8. Body纯黑#000000不是#0a0a0a
9. 侧边栏用cmdk(Command Palette)库+Radix Popover
10. 节点尺寸随内容变化: 250x250(空) → 250x448(有素材)
