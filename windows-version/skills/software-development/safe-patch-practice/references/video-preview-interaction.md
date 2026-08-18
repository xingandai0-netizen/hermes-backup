# Video Preview Interaction Patterns (Antoken)

## 用户期望的交互方式（TapNow风格）

### 1. 视频预览区
- **悬停** → 从头播放视频
- **移开** → 暂停并重置到开头
- **单击** → 显示控制面板（对话交流框）
- **右键** → 上传素材（仅空白素材框）
- **全屏按钮** → 打开PreviewModal（放大预览）

### 2. 底部控件区域（悬停时显示）
- 进度条（可拖拽）
- 播放/暂停按钮
- 快退/快进 5 秒
- 时间显示
- 播放速度切换
- 静音控制
- 全屏按钮

### 3. 控制面板（单击后弹出）
- 输入提示词
- 模型选择下拉框
- 分辨率/比例选择
- 生成按钮
- 弹出动画：`popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)`

## 关键实现细节

### VideoPreview组件
```tsx
<VideoPreview
  src={url}
  height={220}
  loop
  muted
  controls
  hoverToPlay  // 悬停播放
  onExpand={() => setShowPreview(true)}  // 全屏按钮回调
/>
```

**注意：** 不要在VideoPreview根div添加onClick，让事件正常冒泡到ReactFlow节点。

### ReactFlow事件处理
- ReactFlow的`onNodeDoubleClick`会拦截双击事件
- 传空函数`onNodeDoubleClick={() => {}}`也无效
- 解决方案：用单击显示控制面板，不用双击

### 节点onClick处理
```tsx
// 空白素材框
<div
  onClick={(e) => { e.stopPropagation(); setShowControls(true); }}
  onContextMenu={(e) => {
    e.preventDefault();
    e.stopPropagation();
    fileInputRef.current?.click();
  }}
>

// 已有素材的预览框
<div
  onClick={(e) => { e.stopPropagation(); setShowControls(true); }}
>
```

## 用户术语区分
- "对话交流框"/"对话框" = 控制面板（输入提示词、选择模型）
- "放大预览" = PreviewModal全屏预览
- "属性面板" = 右侧PropertyPanel
