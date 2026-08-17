# TapNow.ai 完整UI逆向详情

**最后验证**: 2026-07-05
**提取方法**: 浏览器DevTools API（document.styleSheets, getComputedStyle, querySelectorAll）

---

## 技术栈

- **构建工具**: Vite（`__vite__mapDeps` 可见）
- **前端框架**: React（JSX语法 e.jsx()）
- **画布**: React Flow (@xyflow/react)
- **样式**: Tailwind CSS + CSS Variables
- **动画**: CSS Keyframes + Framer Motion
- **图标**: Tabler Icons
- **字体**: Inter, JetBrains Mono
- **CDN域名**: `fe-assets.tapnow.media`
- **主JS文件**: `assets/index-kqMVjXuo.js`（1.5MB, 无sourcemap）

---

## 一、CSS变量（100个，真实计算值）

从 `index-ojNnE14B.css` 的 `:root` 规则提取：

```css
:root {
  /* 背景 */
  --background: #0f0f0f;
  --background-canvas: #0a0a0a;
  --card: #1f1f1f;
  --card-background: #1f1f1f;
  --popover: #262626;
  --chat-background: #141414;
  --sidebar: #1c1c1c;

  /* 前景 */
  --foreground: #f5f5f5;
  --card-foreground: #fafafa;
  --popover-foreground: #ccc;
  --text-text-primary: #e6e6e6;
  --text-text-secondary: #9c9c9c;
  --text-text-tertiary: #737373;
  --muted-foreground: #7a7a7a;

  /* 主色 */
  --primary: #1fa2dc;
  --primary-foreground: #fafafa;

  /* 边框 */
  --border: #ffffff1a;
  --input: #ffffff26;

  /* 字体 */
  --font-sans: Inter, sans-serif;
  --font-mono: JetBrains Mono, monospace;

  /* 圆角 */
  --radius: .75rem;

  /* 阴影 */
  --shadow-sm: 0px 2px 4px 0px #0000001a, 0px 1px 2px -1px #0000001a;
  --shadow-md: 0px 2px 4px 0px #0000001a, 0px 2px 4px -1px #0000001a;
  --shadow-lg: 0px 2px 4px 0px #0000001a, 0px 4px 6px -1px #0000001a;
}
```

---

## 二、React Flow画布CSS变量（37个，真实值）

从 `vendor-pkg-canvas-B1dDS-3J.css` 提取，暗色主题覆盖值：

```css
.react-flow.dark {
  /* 边线 */
  --xy-edge-stroke-default: #3e3e3e;
  --xy-edge-stroke-selected-default: #727272;
  --xy-connectionline-stroke-default: #b1b1b7;

  /* 背景 */
  --xy-background-color-default: #141414;
  --xy-background-pattern-dots-color-default: #777;

  /* 节点 */
  --xy-node-color-default: #f8f8f8;
  --xy-node-border-default: 1px solid #3c3c3c;
  --xy-node-background-color-default: #1e1e1e;
  --xy-node-boxshadow-hover-default: 0 1px 4px 1px rgba(255,255,255,0.08);
  --xy-node-boxshadow-selected-default: 0 0 0 .5px #999;

  /* 句柄 */
  --xy-handle-background-color-default: #bebebe;
  --xy-handle-border-color-default: #1e1e1e;

  /* 控件 */
  --xy-controls-button-background-color-default: #2b2b2b;
  --xy-controls-button-color-default: #f8f8f8;
  --xy-controls-button-border-color-default: #5b5b5b;

  /* 小地图 */
  --xy-minimap-background-color-default: #141414;
  --xy-minimap-node-background-color-default: #2b2b2b;

  /* 边线标签 */
  --xy-edge-label-background-color-default: #141414;
  --xy-edge-label-color-default: #f8f8f8;
}
```

---

## 三、节点真实HTML结构（4种类型）

从DOM直接提取，className未被混淆（Tailwind保持原样）：

### 节点类型
| 类型 | className | 内容类型 |
|------|-----------|----------|
| imageNode | `react-flow__node-imageNode nopan selectable draggable` | 图片 |
| textNode | `react-flow__node-textNode nopan selectable draggable` | 文本 |
| videoNode | `react-flow__node-videoNode nopan selectable draggable` | 视频 |

### 节点卡片样式（真实computed值）
```css
/* 节点内容容器 */
.node-card {
  background: rgba(24, 24, 27, 0.7); /* bg-zinc-900/70 */
  backdrop-filter: blur(24px); /* backdrop-blur-xl */
  border-radius: 10.8px; /* rounded-xl 在252px宽度下 */
  overflow: hidden;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  outline: 0.5px solid rgba(255, 255, 255, 0.2); /* outline-white/20 */
}

.node-card:hover {
  outline-color: rgba(255, 255, 255, 0.45); /* hover:outline-white/45 */
}
```

### 节点标题样式
```css
.node-title {
  font-family: 'Inter', sans-serif;
  font-size: 8px;
  letter-spacing: 0.05em; /* tracking-wider */
  color: rgba(255, 255, 255, 0.6); /* text-foreground/60 */
  display: flex;
  align-items: center;
  gap: 4px; /* gap-1 */
  margin-bottom: 6px;
}
```

### Handle（连接点）结构
```html
<div data-handleid="left" data-nodeid="0" data-handlepos="left"
     class="react-flow__handle react-flow__handle-left nodrag nopan target connectable"
     style="background: transparent; border: none; width: 0; height: 0;">
  <div class="absolute top-1/2 -translate-y-1/2 right-0 rounded-full flex justify-center items-center cursor-crosshair"
       style="width: 39.6px; height: 39.6px;">
    <div class="node-handle-plus node-handle-plus-left">
      <svg class="tabler-icon tabler-icon-plus border-[1.5px] rounded-full text-muted-foreground transition-colors hover:text-foreground border-muted-foreground hover:border-foreground">
        <!-- plus icon -->
      </svg>
    </div>
  </div>
</div>
```

---

## 四、浮动工具栏（真实computed值）

```css
.canvas-toolbar {
  width: fit-content;
  height: 48px; /* h-12 */
  padding: 4px; /* p-1 */
  border-radius: 9999px; /* rounded-full */
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  gap: 4px; /* gap-1 */
  background: rgba(38, 38, 38, 0.8); /* bg-popover/80 */
  backdrop-filter: blur(16px); /* backdrop-blur-lg */
  border: 1px solid rgba(255, 255, 255, 0.1); /* border-border */
  white-space: nowrap;
  color: rgba(255, 255, 255, 0.9); /* text-white/90 */
}

.toolbar-divider {
  width: 1px;
  height: 18px;
  background: rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}
```

---

## 五、动画关键帧（57个，真实提取）

关键TapNow专用动画：

```css
/* 节点新建高亮 */
@keyframes nodeNewHighlight {
  0%, 100% { box-shadow: rgba(59,130,246,0.2) 0 0 8px 2px; }
  50% { box-shadow: rgba(59,130,246,0.4) 0 0 16px 4px; }
}

/* 画布节点焦点 */
@keyframes canvasNodeFocusHighlight {
  0%, 100% { box-shadow: rgba(59,130,246,0.18) 0 0 8px 2px; }
  35% { box-shadow: rgba(59,130,246,0.42) 0 0 20px 6px; }
}

/* 小地图节点脉冲 */
@keyframes minimapNodePulse {
  0%, 100% { opacity: 0.4; filter: drop-shadow(rgba(59,130,246,0.4) 0 0 2px); }
  50% { opacity: 1; filter: drop-shadow(rgb(59,130,246) 0 0 6px); }
}

/* 流光效果 */
@keyframes flowingLight {
  0% { background-position: var(--flow-start) 50%; }
  100% { background-position: var(--flow-end) 50%; }
}

/* 虚线绘制（React Flow连线） */
@keyframes dashdraw {
  0% { stroke-dashoffset: 10; }
}

/* 价格闪烁 */
@keyframes tapPriceShimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 浮动UI进入 */
@keyframes float-ui-enter {
  0% { opacity: 0; transform: translate(-50%) translateY(calc(var(--float-y) + var(--float-offset))) scale(var(--float-scale)); }
  100% { opacity: 1; transform: translate(-50%) translateY(var(--float-y)) scale(var(--float-scale)); }
}

/* 手风琴展开/收起 */
@keyframes accordion-down {
  0% { height: 0; }
  100% { height: var(--radix-accordion-content-height, auto); }
}
@keyframes accordion-up {
  0% { height: var(--radix-accordion-content-height, auto); }
  100% { height: 0; }
}
```

---

## 六、对话框/Popover样式（从JS+CSS提取）

### Radix Dialog模式
```css
dialog { padding: 0; }

.dialog-content {
  background: hsl(var(--popover)); /* #262626 */
  border: 1px solid hsl(var(--border)); /* rgba(255,255,255,0.1) */
  border-radius: var(--radius); /* 0.75rem */
  animation: scaleIn 0.2s ease-out;
}
```

### 控制面板（节点点击后弹出）
```css
.control-panel {
  background: rgba(38, 38, 38, 0.95); /* bg-popover/95 */
  backdrop-filter: blur(24px); /* backdrop-blur-xl */
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px; /* rounded-2xl */
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
  animation: slideUp 0.3s ease-out;
}
```

### Tooltip
```css
.tooltip {
  background: hsl(var(--popover));
  border: 1px solid hsl(var(--border));
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: hsl(var(--popover-foreground));
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}
```

---

## 七、素材框组件结构（从minified JS提取）

```
jo (主页面)
├── VirtualList (虚拟滚动, columnCount:4, viewportBuffer:1000)
│   └── hR (素材卡片, hover状态管理)
├── iR (素材详情弹窗, template_data加载)
└── uR (创作对话框)
```

### API端点
```
GET /api/community/works?page=1&page_size=20
GET /api/community/works/{id}
POST /api/conversation/storage/uploads/{id}
```

---

## 关键逆向教训

1. **Tailwind类名在minified JS中保持原样** — className不会被混淆
2. **CSS变量值需要从运行时获取** — 不能从JS文件中grep
3. **React Flow用`--xy-`前缀** — 暗色主题在`.react-flow.dark`选择器下
4. **Radix UI的Dialog/Popover** — 检查`role="dialog"`, `data-state`属性
5. **节点位置在style.transform中** — `translate(120px, -1680px)`
6. **Handle样式被覆盖为透明** — 实际可见的Plus按钮在Handle内部
7. **border-radius会随宽度变化** — `rounded-xl`在252px宽度=10.8px

---

## 输出文件

实际逆向输出位于 `/Users/macpro/ai-crawler-reverse/output/`：
- `tapnow-real-variables.css` — 100个CSS变量
- `tapnow-real-canvas.css` — React Flow画布样式
- `tapnow-real-animations.css` — 57个动画关键帧
- `tapnow-nodes-structure.html` — 4种节点HTML
- `tapnow-complete-ui.tsx` — React组件代码
- `canvas-styles.css` — 画布完整CSS
- `dialog-styles.css` — 对话框完整CSS
- `dialog-structure.html` — 对话框HTML结构
- `dialog-component.tsx` — 对话框React组件
