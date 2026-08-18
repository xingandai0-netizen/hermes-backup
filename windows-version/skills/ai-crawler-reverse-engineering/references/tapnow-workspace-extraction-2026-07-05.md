# TapNow 工作空间 UI 完整逆向数据 (v2)
# 来源: app.tapnow.ai Safari实时DOM提取 (AppleScript + JavaScript)
# 日期: 2026-07-05
# 验证: 所有值均为getComputedStyle真实返回值
# 提取方法: osascript + base64编码JS + getComputedStyle + outerHTML

---

## 一、Computed Styles (getComputedStyle实测)

### Body
- background-color: rgb(0, 0, 0) → #000000
- font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- color: rgb(245, 245, 245) → #f5f5f5
- margin: 0px, padding: 0px

### 画布 (.react-flow)
- background-color: rgba(0, 0, 0, 0) → 透明
- 实际背景 (.react-flow__background): rgb(0, 0, 0) → #000000
- dot radius: 0.155 (极小点阵)

### 连线 (.react-flow__edge path)
- stroke: rgba(255, 255, 255, 0.376) → ~37.6%白色
- stroke-width: 2px
- stroke-dasharray: none, fill: none

### Handle (.react-flow__handle)
- 6x6px, 透明, position:absolute
- 可见部分 .node-handle-plus svg: 24x24px
- color: rgb(122, 122, 122) → #7a7a7a
- border: 2px solid, border-radius: 9999px
- transition: 0.15s cubic-bezier(0.4, 0, 0.2, 1)

### 节点卡片 (.bg-card)
- background-color: rgb(31, 31, 31) → #1f1f1f
- border-radius: 16px
- border: 0px solid rgba(255, 255, 255, 0.1)
- box-shadow: none
- min-width: 250px, min-height: 250px
- overflow: visible

### 节点选中 (.selected .bg-card)
- outline: rgb(122, 122, 122) solid 2px → #7a7a7a
- outline-offset: 0px
- z-index: 1000 (选中节点提升)

### 节点标题栏
- position: absolute, z-index: 1, transform: translateY(-100%)
- left: 4px, top: 0px, padding-bottom: 8px
- color: rgba(245, 245, 245, 0.6)
- font-size: ~38px (随缩放), gap: 4px

### 控制面板 - 展开形态 (.node-float-ui, 无素材时)
- position: absolute, bottom: -8px, z-index: 20
- min-width: 640px, max-width: 650px
- 卡片: #1f1f1f, 16px圆角, 1px solid rgba(255,255,255,0.1)
- margin-top: 8px
- box-shadow: rgba(0,0,0,0.1) 0px 2px 4px, rgba(0,0,0,0.1) 0px 4px 6px -1px

### 控制面板 - 紧凑形态 (有素材+选中时)
- class: node-float-ui nodrag cursor-default w-fit h-12 p-1 rounded-full flex flex-nowrap items-center justify-between bg-popover/80 backdrop-blur-lg border whitespace-nowrap gap-1 text-white/90
- height: 48px (h-12), padding: 4px (p-1)
- border-radius: 9999px (rounded-full)
- background: #262626 80% (bg-popover/80)
- backdrop-filter: blur(12px) (backdrop-blur-lg)
- 与展开形态完全不同——胶囊式紧凑栏

### 编辑器 (.ProseMirror)
- font-size: 16px, line-height: 25.6px (1.6)
- color: #f5f5f5, padding: 0px 12px 8px, min-height: 80px

### 生成按钮 (aria-label="Generate")
- 26x26px, 圆形(9999px), 白色背景, 黑色文字
- transition: 0.15s cubic-bezier(0.4, 0, 0.2, 1)
- hover: bg-white/50, disabled: opacity 0.5

### 上传按钮 (.size-[38px])
- 38x38px, border-radius: 10px
- background: rgba(255,255,255,0.08), hover: rgba(255,255,255,0.12)

### 节点尺寸实测
- Text: 250x250px
- Image(空): 250x250px, Image(有图): 250x373~448px
- Video(空): 250x250px, Video(有视频): 250x373~444x250px

### 节点内容图片
- class: w-full h-full object-contain rounded-2xl absolute inset-0 z-1
- src带 ?variant_name=small 参数（小图预览）

### 滚动条
- scrollbar-width: thin

---

## 二、侧边栏 (Node Panel)

### 触发按钮
- 40x40px, bg: #2b2b2b, border-radius: 9999px (圆形)
- position: left 22px, top 240px

### 面板容器 (Radix Popover Dialog)
- width: 240px, overflow: hidden
- 内层: bg-zinc-900, 1px solid zinc-700, border-radius: 12px, padding: 0

### 背景模糊装饰 (blur-3xl, opacity:20%)
- 蓝色 #0093FF: top:55% left:83% w:28% h:45%
- 蓝色 #0093FF: top:95% left:40% w:58% h:25%
- 橙色 #F15B0E: top:80% left:75% w:29% h:35%
- 橙色 #F15B0E: top:-10% left:-4% w:20% h:23%

### 标题 "添加节点"
- font-size: 12px, color: #7a7a7a, padding: 6px 8px

### 节点类型项 (通用)
- height: 52px (h-13), padding: 8px, border-radius: 16px (rounded-xl)
- cursor: pointer, gap: 8px, font-size: 16px, color: white
- 图标容器: aspect-ratio:1, rounded-md, bg-accent/40
- 文字: 名称 font-medium text-sm 14px, 描述 text-xs 12px #7a7a7a
- hover效果: 名称translateY(10px→0), 描述opacity(0→1), duration:200ms

### 节点列表
1. 文本 (Text) — "脚本、广告词、品牌文案" [canvas-dockbar-add-text-node-btn]
2. 图片 (Image) — "宣传图、海报、封面" [canvas-dockbar-add-image-node-btn]
3. 视频 (Video) — "宣传视频、动画、电影" [canvas-dockbar-add-video-node-btn]
4. 音频 (Audio) — "音乐、配音、音效" [canvas-dockbar-add-audio-node-btn]
5. 3D世界 (3D World) — "Beta场景与资产生成、导演编排"
6. 播放列表 (Playlist) — "Beta时间轴串联多段素材"
7. 图片编辑器 (Image Editor) — "编辑和处理图片" [canvas-dockbar-add-image-editor-node-btn]
8. 上传 (Upload) — "支持图片、视频、音频和3D资产"

---

## 三、右键菜单

### 画布右键菜单
- testId: canvas-pane-context-menu-container
- class: bg-white dark:bg-card/85 border backdrop-blur-xl p-1 !rounded-2xl max-h-[500px] fixed w-60
- width: 240px, bg: ~#1f1f1f 85%, border-radius: 16px, padding: 4px
- position: fixed, z-index: 10
- animation: animate-in zoom-in fade-in

菜单项: p-3(12px), rounded-lg(8px), text-sm(14px), cursor:pointer
选中态: bg-muted (#2b2b2b)
快捷键: text-sm text-muted-foreground tracking-widest (#7a7a7a)
分隔线: h-px bg-border my-1

菜单内容:
- 组1: 上传 / 添加资产
- 组2: 添加节点 / 添加辅助工具
- 组3: 撤销 ⌘Z / 重做 ⇧⌘Z
- 组4: 粘贴 ⌘V

### 节点右键菜单
- testId: canvas-node-context-menu-container
- 同样式，内容: 复制⌘C / 粘贴⌘V(disabled) / 副本 / ---分隔线--- / 删除⌫,del / --- / 反馈问题

---

## 四、模型选择下拉框

### 容器 (Radix Popover)
- testId: canvas-node-video-model-select-dropdown
- width: 280px, border: 1px solid border-border/60, border-radius: 16px
- data-side="top" (向上弹出), overflow: hidden

### 内层
- background: #292929, padding: 8px, scrollbar隐藏
- max-height: 400px, overflow-y: auto

### 模型选项
- padding: 8px, border-radius: 12px, cursor: pointer
- 选中态: bg-white/10, 悬停态: bg-white/5
- 图标: 16x16px, rounded-sm
- 名称: 12px, font-medium, white/90
- 能力标签: bg-[#363636], px-1.5 py-1, rounded-md, 10px, #AFAFAF
- 选中check: absolute right-2, 32x32px容器, 白色✓ 14px

---

## 五、预览覆盖层 (非弹窗)

### 关键发现: 没有独立预览弹窗
选中有素材的节点后，内容在节点内inline显示。点击内容区域触发的是节点内的absolute覆盖层。

### 覆盖层样式
- position: absolute, inset: 0, z-index: 1000
- background: ~#1a1a1a 80% (bg-background/80)
- border-radius: 16px, padding: 16px, gap: 8px
- display: flex, column, center-center
- pointer-events: auto

### 错误状态
- 图标: 48x48, opacity: 0.2
- 标题: 14px, font-medium, #f5f5f5 ("预览加载失败")
- 描述: 12px, #7a7a7a, max-width: 200px
- 按钮: h-32px, rounded-md(6px), border input, bg-background

---

## 六、画布面板布局 (react-flow__panel)

### 关键发现
- 没有 .react-flow__controls (无默认缩放控件)
- 没有 .react-flow__minimap (无小地图)
- 5个自定义React Flow Panel

Panel布局:
1. **左Dockbar触发器**: left:0, 54x338px, z-50
2. **顶部中心**: pointer-events-none, 0x40px (空)
3. **底部左侧(缩放控件)**: bottom:0, left:0, 257x40px
4. **右上角工具栏**: top:0, right:0, 214x40px ("193 社区")
5. **React Flow归属**: hidden (0x0)

---

## 七、CSS变量 (148个, 完整列表)

### 背景色
--background: #0f0f0f | --background-canvas: #0a0a0a | --card: #1f1f1f
--popover: #262626 | --chat-background: #141414 | --sidebar: #1c1c1c
--muted: #2b2b2b | --secondary: #222 | --accent: #404040

### 文字色
--foreground: #f5f5f5 | --card-foreground: #fafafa | --muted-foreground: #7a7a7a
--text-text-primary: #e6e6e6 | --text-text-secondary: #9c9c9c | --text-text-tertiary: #737373

### 主题色
--primary: #1fa2dc | --tap-primary-1: #33a8ff | --border: #ffffff1a | --input: #ffffff26

### 字体
--font-sans: Inter, sans-serif | --font-mono: JetBrains Mono, monospace

### 圆角
--radius: .75rem (12px)

### 阴影
--shadow-sm: 0px 2px 4px 0px #0000001a, 0px 1px 2px -1px #0000001a
--shadow-lg: 0px 2px 4px 0px #0000001a, 0px 4px 6px -1px #0000001a
--shadow-xl: 0px 2px 4px 0px #0000001a, 0px 8px 10px -1px #0000001a

### TapNow专属
--tap-bg-1: #32454c | --tap-bg-2: #2b373b | --tap-pink: #e896c9 | --tap-red: #db5a4d
--tap-state-success: #4caf50 | --tap-state-error: #f44336
--tap-gradient-pink: linear-gradient(90deg, #de77df 0%, #f8c4a7 100%)

---

## 八、动画关键帧 (40+个, 完整)

### 核心画布
- nodeNewHighlight: box-shadow蓝色脉冲 0.2→0.4→0.2
- canvasNodeFocusHighlight: box-shadow蓝色脉冲 0.18→0.42→0.18
- dashdraw: stroke-dashoffset: 10 (连线流动)
- fadeIn: opacity 0→1
- patchExitPulse: 蓝色shadow + scale(1→1.08→1)

### 控制面板
- float-ui-enter: opacity + translateY + scale
- tapPriceShimmer: background-position 200%→-200%
- tapPriceChange: opacity 0.35→1 + translateY 2px→0

### 通用
- spin/spinning: rotate(360deg) | pulse: opacity 0.5
- ProseMirror-cursor-blink: visibility hidden
- spin: rotate(360deg) | ping: opacity 0 + scale(2)
- enter/exit: Tailwind动画系统
- accordion-down/up: height 0→auto | collapsible-down/up: 同上

### Sonner Toast
- sonner-fade-in: opacity 0 + scale(0.8) → 1
- sonner-fade-out: 反向

---

## 九、data-testid 映射

| 组件 | data-testid |
|------|-------------|
| Text节点 | canvas-node-text-{uuid} |
| Image节点 | canvas-node-image-{uuid} |
| Video节点 | canvas-node-video-{uuid} |
| 图片内容 | canvas-node-image-content |
| 视频内容 | canvas-node-video-content |
| 控制面板 | canvas-node-generation-input-bar |
| 操作栏 | canvas-node-generation-action-bar |
| Text模型选择 | canvas-node-text-model-select |
| Video模型选择 | canvas-node-video-model-select |
| Video模型下拉 | canvas-node-video-model-select-dropdown |
| 画布右键菜单 | canvas-pane-context-menu-container |
| 节点右键菜单 | canvas-node-context-menu-container |
| 工具栏 | canvas-editor-toolbar |
| 侧边栏-文本 | canvas-dockbar-add-text-node-btn |
| 侧边栏-图片 | canvas-dockbar-add-image-node-btn |
| 侧边栏-视频 | canvas-dockbar-add-video-node-btn |
| 侧边栏-音频 | canvas-dockbar-add-audio-node-btn |

---

## 十、技术栈确认

- 框架: React 18+ (Vite构建, 非Next.js)
- 画布: @xyflow/react (React Flow v12)
- 样式: Tailwind CSS + CSS变量
- 编辑器: TipTap (ProseMirror)
- 弹出层: Radix UI (Dialog, Popover) + cmdk (command palette)
- Toast: Sonner
- 图标: Tabler Icons
- 字体: Inter + JetBrains Mono
- 图片预览: react-advanced-yarl (Yet Another React Lightbox)
- 媒体CDN: files.tapnow.media
