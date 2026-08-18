# TapNow 三种节点类型对比（2026-07-05 实测）

## 关键发现：Image和Video的控制面板结构完全一样

| 元素 | Text | Image | Video |
|------|------|-------|-------|
| 卡片样式 | 相同 | 相同 | 相同 |
| 图标 | 文字图标 | 图片图标 | 视频图标 |
| 内容区 | TipTap富文本编辑器 | TipTap提示词输入 | TipTap提示词输入 |
| 工具栏 | 格式化工具栏（H1/H2/H3/段落/加粗/斜体/下划线/删除线/代码/引用/列表） | 无 | 无 |
| 控制面板 | 无（工具栏替代） | 上传+模型选择+设置+变体+生成 | 上传+模型选择+设置+变体+生成 |

## 节点类型通过data-testid区分
- `canvas-node-text-*`
- `canvas-node-image-*`
- `canvas-node-video-*`

## 控制面板结构（Image/Video共用）

```
.bg-card.rounded-2xl.border.border-border.shadow-lg
├── .px-3.pt-3.pb-2.flex.gap-2  (工具栏行)
│   └── button.size-[38px]  (上传/加号按钮)
├── .relative.flex.justify-between  (输入区域)
│   └── .overflow-y-auto  (TipTap编辑器, min-h:80px, max-h:400px)
└── .flex.items-center.justify-between.h-14  (底部操作栏)
    ├── button (模型选择器, h:36px, rounded:12px)
    ├── button (设置按钮, 32x32px, rounded:12px)
    ├── .w-px.h-4 (分隔线)
    ├── button (变体数量 "1×", rounded:12px)
    └── button (生成按钮, 26x26px圆形, bg:white, color:black)
```

## Text节点工具栏结构

```
ul.flex.flex-nowrap.gap-[2px]
├── button (颜色选择器, 圆形)
├── .w-px.h-[18px].bg-primary-border (分隔线)
├── button (H1)
├── button (H2)
├── button (H3)
├── button (段落)
├── .w-px.h-[18px].bg-primary-border (分隔线)
├── button (加粗)
├── button (斜体)
├── button (下划线)
├── button (删除线)
├── button (代码)
├── button (引用)
└── button (列表)
```

## 关键样式值

### 控制面板容器
```css
background: rgb(31, 31, 31);
border-radius: 16px;
border: 1px solid rgba(255, 255, 255, 0.1);
box-shadow: 0px 2px 4px rgba(0,0,0,0.1), 0px 4px 6px rgba(0,0,0,0.1);
position: absolute;
bottom: -8px;
z-index: 20;
min-width: 640px;
max-width: 650px;
```

### 上传按钮
```css
width: 38px; height: 38px;
border-radius: 10px;
background: rgba(255, 255, 255, 0.08);
```

### 生成按钮
```css
width: 26px; height: 26px;
border-radius: 50%;
background: white;
color: black;
```

### 工具栏按钮（Text节点）
```css
height: 32px;
padding: 8px;
border-radius: 9999px;
aspect-ratio: 1;
background: transparent;
color: rgb(122, 122, 122);
/* 选中状态 */
background: rgb(34, 34, 34);
color: rgb(240, 240, 240);
```
