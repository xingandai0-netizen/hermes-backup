# TapNow 画布+登录逆向实战记录 (2026-07-05)

## 登录尝试结果

### 方法1: Google OAuth
- 结果: **失败** - Google返回"此浏览器或应用可能不安全"
- 原因: Browserbase的headless Chrome被Google识别为不安全环境
- 教训: Google OAuth在自动化浏览器中基本不可用

### 方法2: 邮箱+密码注册
- 结果: **部分成功** - 注册流程走到"请查收邮件"步骤
- 问题: 需要用户去Gmail点击验证链接才能继续
- 教训: 新账号注册需要邮件验证，无法自动化完成

### 方法3: 邮箱+密码登录（已有账号）
- 结果: **未测试** - 需要账号已存在且已验证

## 从落地页成功提取的真实数据

### 1. CSS变量 (100个) - 从index-ojNnE14B.css
```css
--background: #0f0f0f;
--background-canvas: #0a0a0a;
--primary: #1fa2dc;
--card: #1f1f1f;
--popover: #262626;
--border: #ffffff1a;
--font-sans: Inter, sans-serif;
--font-mono: JetBrains Mono, monospace;
--radius: .75rem;
```

### 2. React Flow CSS变量 (37个) - 从vendor-pkg-canvas-B1dDS-3J.css
```css
--xy-edge-stroke-default: #3e3e3e;
--xy-background-color-default: #141414;
--xy-background-pattern-dots-color-default: #777;
--xy-node-background-color-default: #1e1e1e;
--xy-node-border-default: 1px solid #3c3c3c;
--xy-handle-background-color-default: #bebebe;
--xy-minimap-background-color-default: #141414;
```

### 3. 动画关键帧 (57个) - 从document.styleSheets
关键动画:
- `fadeIn` - 基础淡入
- `nodeNewHighlight` - 节点新建高亮 (rgba(59,130,246,0.2)脉冲)
- `canvasNodeFocusHighlight` - 画布焦点高亮
- `dashdraw` - 虚线绘制动画 (React Flow连线)
- `flowingLight` - 流光效果
- `accordion-down/up` - 手风琴展开/收起
- `sonner-fade-in/out` - Toast通知

### 4. 节点HTML结构 (4种) - 从DOM直接读取
```
Node 0: Reference (imageNode) - 252x142.2px, translate(120px, -1680px)
Node 1: Image Generation (imageNode) - 336x189.6px, translate(600px, -1780px)
Node 2: Poem (textNode) - 198px宽, font-size 11.7px, translate(1000px, -1480px)
Node 3: Video Generation (videoNode) - 400x250px, translate(440px, -1500px)
```

### 5. 节点卡片真实样式 (computed)
```css
/* .rounded-xl.bg-zinc-900/70.backdrop-blur-xl */
background: rgba(24, 24, 27, 0.7);
backdrop-filter: blur(24px);
border-radius: 10.8px;
transition: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
outline: 0.5px solid rgba(255, 255, 255, 0.2);
/* hover时: outline-color变为 rgba(255, 255, 255, 0.45) */
```

### 6. 工具栏真实样式 (computed)
```css
/* .w-fit.h-12.p-1.rounded-full.bg-popover/80.backdrop-blur-lg */
width: fit-content;
height: 48px;
padding: 4px;
border-radius: 9999px;
background: rgba(38, 38, 38, 0.8);
backdrop-filter: blur(16px);
border: 1px solid rgba(255, 255, 255, 0.1);
```

### 7. Handle (连接点) 真实样式
```
Handle本身: background: transparent, border: none, width: 0, height: 0
可见按钮: .node-handle-plus 内的SVG plus图标
容器尺寸: 39.6px / 52.8px (随节点大小缩放)
缩放: transform: scale(0.81) / scale(1.08)
```

## 通过用户浏览器提取的数据 (2026-07-05 补充)

用户在已登录的TapNow画布中执行JS代码，提取了以下真实数据。

### 认证信息（localStorage）
```json
{
  "refresh_token": "1aca677d-5352-4f46-863b-...",
  "device_id": "f8a74b50-0b78-4e19-9d92-7428b40ef50c",
  "user_id": "53abfd65-f246-4a83-b88d-be1f8972ac7b",
  "canvas_id": "3dd46839-0252-4f5e-a71c-3560085ded36"
}
```
**注意**: auth token无法注入agent浏览器（安全限制），只能用用户浏览器继续操作。

### Light主题CSS变量（真实值）
```css
/* 用户画布使用light主题: class="react-flow light" */
--xy-background-color-default: transparent;
--xy-background-pattern-dots-color-default: #91919a;
--xy-node-background-color-default: #fff;
--xy-edge-stroke-default: #ffffff60;
--xy-node-border-default: 1px solid #1a192b;
```
**注意**: 与之前从落地页提取的dark主题值不同！用户画布用light主题。

### 节点样式（Light主题 computed values）
```css
background-color: rgb(31, 31, 31); /* 深灰色节点在浅色画布上 */
border-radius: 16px; /* rounded-2xl */
width: 250px;
min-height: 250px;
border: 0px solid rgba(255, 255, 255, 0.1);
backdrop-filter: none;
box-shadow: none;
body background: rgb(0, 0, 0); /* 黑色body */
```

### 节点展开状态DOM（Text节点示例）
展开后的节点包含完整的控制面板，详见 `references/tapnow-control-panel-dom.md`。

关键发现：
- 节点默认折叠（只有标题+占位图标），点击后展开显示控制面板
- 控制面板使用 `.node-float-ui` 类，绝对定位在节点底部
- 输入区域使用 TipTap (ProseMirror) 富文本编辑器，不是普通textarea
- 生成按钮是圆形白色 `w-6.5 h-6.5 rounded-full bg-white text-black`
- 模型选择器显示当前模型名称（如 "Gemini 3.1 Flash Lite"）

## 已提取到的内容（本次session）

- [x] 节点内的输入区域（PromptPanel） → TipTap编辑器
- [x] 模型选择器UI → 按钮显示模型名
- [x] 生成按钮样式 → 圆形白色26x26px
- [ ] 参数设置区域（比例、分辨率等） → 部分（变体数量"1×"）
- [ ] 生成中loading状态
- [ ] 展开/折叠动画
- [ ] 选中时的蓝色/紫色发光边框
- [x] 对话框/控制面板的完整UI → DOM结构已提取
- [ ] 预览区域（视频播放器、图片预览）

## 产出文件

- `/tmp/tapnow-ui-code.zip` - CSS变量 + 画布样式 + 动画 + 节点HTML + React组件
- `/tmp/tapnow-canvas-dialog-code.zip` - 画布CSS + 对话框CSS + 对话框HTML + 对话框组件
- 控制面板DOM结构 → 见 `references/tapnow-control-panel-dom.md`
