# TapNow Workspace UI Reverse Engineering Data
# Extracted: 2026-07-05 via Safari AppleScript JS execution
# Source: https://app.tapnow.ai/canvas/34e9f150-6b4d-4350-ba5d-26840ba83576
# Project: 电商鞋子宣传视频 (copy) — 48 nodes, 42 edges

## Tech Stack (confirmed)
- React 18+ (Vite, NOT Next.js)
- @xyflow/react (React Flow v12)
- Tailwind CSS + CSS Variables
- TipTap (ProseMirror) rich text editor
- Radix UI (Dialog, Popover)
- cmdk (command palette) for menus
- Sonner for toasts
- Tabler Icons
- react-advanced-yarl (Yet Another React Lightbox) for previews
- Inter + JetBrains Mono fonts

## Canvas & Background
- Body: #000000 (pure black), margin:0, padding:0
- Canvas (.react-flow): transparent bg, 1199x820px
- Background (.react-flow__background): #000000, opacity:1
- NOTE: --background-canvas is #0a0a0a but actual computed is #000000

## Edges
- stroke: rgba(255,255,255,0.376) — ~37.6% white
- stroke-width: 2px
- fill: none
- No dash array (solid line)
- Animation: @keyframes dashdraw { 0% { stroke-dashoffset: 10; } }

## Handles
- React Flow handle: 6x6px, transparent, position:absolute
- PlusIcon container: 24x24px, positioned at handle edge
- PlusIcon SVG: 2px solid border, border-radius:9999px, color:#7a7a7a
- Transition: color 0.15s cubic-bezier(0.4,0,0.2,1), bg 0.15s, border-color 0.15s
- Hover: color → #f5f5f5, border-color → #f5f5f5

## Node Card (.bg-card)
- bg: #1f1f1f (rgb(31,31,31))
- border-radius: 16px
- border: 0px solid rgba(255,255,255,0.1) — effectively no border
- box-shadow: none
- min-width: 250px, min-height: 250px
- overflow: visible
- NO backdrop-filter (unlike previous assumption)

## Node Selected
- outline: rgb(122,122,122) solid 2px (#7a7a7a)
- outline-offset: 0px
- NOT a border, NOT a box-shadow

## Node Title (above card)
- position: absolute, transform: translateY(-100%)
- left: 4px, top: 0, padding-bottom: 8px
- color: rgba(245,245,245,0.6) — 60% white
- font-size: scales with zoom (~38px at default zoom)
- flex layout with gap:4px, overflow:hidden, text-overflow:ellipsis

## Node Content Area
- padding: 12px 16px (p-3 px-4)
- overflow-y: scroll
- scrollbar-width: thin
- cursor: default

## Node Dimensions (real)
- Text: 250x250px
- Image (empty): 250x250px
- Image (with image): 250x373~448px
- Video (empty): 250x250px
- Video (with thumbnail): 250x373~448px or 444x250px

## Control Panel (.node-float-ui)
- position: absolute, bottom: -8px
- z-index: 20
- width: 100%, min-width: 640px, max-width: 650px
- Container card: #1f1f1f, 16px radius, 1px solid rgba(255,255,255,0.1)
- Box shadow: rgba(0,0,0,0.1) 0 2px 4px, rgba(0,0,0,0.1) 0 4px 6px -1px
- margin-top: 8px

## ProseMirror Editor (in control panel)
- font-size: 16px, line-height: 25.6px (1.6em)
- color: #f5f5f5
- padding: 0 12px 8px
- min-height: 80px
- Placeholder: ::before with content: attr(data-placeholder), color: muted-foreground

## Generate Button
- 26x26px, border-radius:9999px (circle)
- bg: white, color: black
- cursor: pointer
- transition: 0.15s cubic-bezier(0.4,0,0.2,1)
- Hover: bg → rgba(255,255,255,0.5)
- Disabled: opacity 0.5, cursor: not-allowed

## Upload Button (+)
- 38x38px, border-radius: 10px
- bg: rgba(255,255,255,0.08)
- Hover: bg → rgba(255,255,255,0.12)
- Icon: 16x16px, color: rgba(255,255,255,0.6)

## Model Selector Button
- height: 36px, padding: 4px 8px
- border-radius: 12px
- bg: transparent
- Hover: bg → #2b2b2b (muted)
- Active: bg → rgba(255,255,255,0.1)
- font-size: 14px, font-weight: 500

## Model Dropdown
- width: 280px, opens upward (data-side="top")
- bg: #292929, padding: 8px
- border-radius: 16px, overflow: hidden
- scrollbar-width: none (hidden)
- Max height: 400px

### Model Item
- padding: 8px, border-radius: 12px
- Selected: bg rgba(255,255,255,0.1)
- Hover: bg rgba(255,255,255,0.05)
- Icon: 16x16px, rounded-sm
- Name: 12px, font-weight:500, color: rgba(255,255,255,0.9)
- Badges: bg #363636, px-1.5 py-1, rounded-md, 10px, color #AFAFAF
- Check icon: absolute right, 12px, white

## Sidebar (Node Panel)
- Radix Popover, 240px wide
- Container: bg zinc-900, 1px solid zinc-700, 12px radius
- Background decoration: blur-3xl with colored dots (#0093FF blue + #F15B0E orange), opacity 20%
- Heading "添加节点": 12px, #7a7a7a, padding 6px 8px
- Items: 52px height, 16px radius, 8px padding, 16px font
- Icon container: aspect-ratio 1, bg accent/40, rounded-md
- Hover animation: title translateY 10px→0, description opacity 0→1, duration 200ms

### Node Types in Sidebar
1. 文本 (Text) — "脚本、广告词、品牌文案"
2. 图片 (Image) — "宣传图、海报、封面"
3. 视频 (Video) — "宣传视频、动画、电影"
4. 音频 (Audio) — "音乐、配音、音效"
5. 3D世界 (3D World) — "Beta场景与资产生成、导演编排"
6. 播放列表 (Playlist) — "Beta时间轴串联多段素材"
7. 图片编辑器 (Image Editor) — "编辑和处理图片"
8. 上传 (Upload) — "支持图片、视频、音频和3D资产"

## Context Menu (Canvas right-click)
- Same cmdk pattern as sidebar
- 240px wide, bg-card/85, 16px radius, backdrop-blur-xl, p-1 (4px)
- Fixed position, z-index:10
- Animation: animate-in zoom-in fade-in
- Items: p-3 (12px), rounded-lg (8px), text-sm (14px)
- Selected: bg-muted (#2b2b2b)
- Hotkeys: text-sm, muted-foreground (#7a7a7a), tracking-widest
- Separators: 1px, #ffffff1a, my-1

### Menu Groups
1. 上传 / 添加资产
2. 添加节点 / 添加辅助工具
3. 撤销 ⌘Z / 重做 ⇧⌘Z
4. 粘贴 ⌘V

### Node Right-Menu (hidden, separate)
- 复制 ⌘C / 粘贴 ⌘V / 副本 / 删除 ⌫,del / 反馈问题

## Animations (key @keyframes)
- fadeIn: opacity 0→1
- dashdraw: stroke-dashoffset 10→0
- nodeNewHighlight: box-shadow pulse (blue)
- canvasNodeFocusHighlight: box-shadow pulse (blue, stronger)
- patchExitPulse: box-shadow + scale pulse (cyan)
- minimapNodePulse: opacity + drop-shadow pulse (blue)
- float-ui-enter: opacity + translateY + scale
- tapPriceShimmer: background-position shimmer
- tapPriceChange: opacity + translateY + scale
- spin: rotate 360deg
- pulse: opacity 0.5
- sonner-fade-in/out: opacity + scale
- accordion-down/up: height 0→auto
- enter/exit: Tailwind animate-in/out
