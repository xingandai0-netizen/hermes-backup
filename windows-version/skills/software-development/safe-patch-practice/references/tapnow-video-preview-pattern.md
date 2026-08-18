# TapNow风格视频预览交互模式（最终版 2026-06-15）

## 核心交互

### 1. 悬停播放（Hover to Play）
- 鼠标进入预览区：从头播放视频
- 鼠标离开预览区：暂停并重置到开头

```tsx
useEffect(() => {
  if (!hoverToPlay || !videoRef.current) return;

  if (isHovered) {
    videoRef.current.currentTime = 0;
    videoRef.current.play().catch(() => {});
  } else {
    videoRef.current.pause();
    videoRef.current.currentTime = 0;
    setProgress(0);
    setCurrentTime(0);
  }
}, [isHovered, hoverToPlay]);
```

### 2. 单击显示控制面板（对话交流框）⭐ 最终版
- **VideoPreview 组件本身不处理 onClick** — 让事件冒泡到父容器
- **父容器的 onClick** → 显示控制面板（showControls）
- **放大按钮**（控件区域右下角）→ 打开 PreviewModal

```tsx
// VideoPreview 内部 — 不添加 onClick，让事件冒泡
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  // 没有 onClick！事件会冒泡到父容器
>
  {/* 视频内容 */}
  {/* 控件区域用 onMouseDown 防止拖拽 */}
  <div onMouseDown={(e) => e.stopPropagation()}>
    {/* 播放/暂停、进度条、放大按钮 */}
  </div>
</div>
```

### 3. 三种"框"的区分（CRITICAL）

| 名称 | 含义 | 触发方式 |
|------|------|----------|
| "对话交流框" | 节点内控制面板（输入提示词、模型选择、生成按钮） | 单击预览区（父容器 onClick） |
| "属性面板" | 右侧 PropertyPanel | ReactFlow 自动选中节点 |
| "放大预览"/"预览对话框" | PreviewModal 全屏模态框 | 点击控件区域的放大按钮 |

## 组件接口（最终版）

```tsx
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;      // 默认 false（由悬停控制）
  loop?: boolean;          // 默认 true
  muted?: boolean;         // 默认 true
  controls?: boolean;      // 默认 true
  hoverToPlay?: boolean;   // 默认 true
  onExpand?: () => void;   // 放大按钮回调（打开 PreviewModal）
  className?: string;
  style?: React.CSSProperties;
}
```

## 在节点中使用（最终版）

```tsx
// VideoNode.tsx
const [showPreview, setShowPreview] = useState(false);
const [showControls, setShowControls] = useState(false);

{/* 父容器 — 单击显示控制面板 */}
<div
  onClick={(e) => { e.stopPropagation(); setShowControls(true); }}
  style={{ position: "relative" }}
>
  {previewUrl ? (
    <VideoPreview
      src={proxyUrl(previewUrl) || previewUrl}
      height={220}
      loop
      muted
      controls
      hoverToPlay
      onExpand={() => previewUrl && setShowPreview(true)}
    />
  ) : (
    <div>上传区域</div>
  )}
</div>

{/* 控制面板（对话交流框）— 用 onMouseDown 防止拖拽 */}
{showControls && (
  <div onMouseDown={(e) => e.stopPropagation()}>
    <textarea placeholder="描述任何你想要生成的内容" ... />
    <select>模型选择</select>
    <button onClick={handleGenerate}>生成</button>
  </div>
)}

{/* PreviewModal — 放大按钮触发 */}
{showPreview && previewUrl && (
  <PreviewModal url={previewUrl} type="video" onClose={() => setShowPreview(false)} />
)}
```

## 完整控件区域（带播放/暂停、快进退、速度、静音、放大）

```tsx
{/* 控件区域 - 悬停时显示 */}
{controls && isHovered && !isLoading && !hasError && (
  <div
    style={{
      position: 'absolute',
      bottom: 0,
      left: 0,
      right: 0,
      background: 'linear-gradient(transparent, rgba(0,0,0,0.8))',
      padding: '20px 8px 8px',
      zIndex: 20,
    }}
    onMouseDown={(e) => e.stopPropagation()}  // 防止拖拽，但不影响 click
  >
    {/* 进度条 */}
    <div onClick={handleSeek} style={{ width: '100%', height: 4, background: 'rgba(255,255,255,0.2)', borderRadius: 2, marginBottom: 6, cursor: 'pointer' }}>
      <div style={{ width: `${progress}%`, height: '100%', background: '#ffffff', borderRadius: 2 }} />
    </div>

    {/* 控制栏 */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <button onClick={togglePlay}>{isPlaying ? <PauseIcon /> : <PlayIcon />}</button>
        <button onClick={(e) => { e.stopPropagation(); skip(-5); }}><RewindIcon /></button>
        <button onClick={(e) => { e.stopPropagation(); skip(5); }}><ForwardIcon /></button>
        <span>{formatTime(currentTime)} / {formatTime(duration)}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
        <button onClick={(e) => { e.stopPropagation(); changePlaybackRate(); }}>{playbackRate}x</button>
        <button onClick={(e) => { e.stopPropagation(); toggleMute(); }}><MuteIcon /></button>
        {/* 放大按钮 — 打开 PreviewModal */}
        <button
          onClick={(e) => { e.stopPropagation(); if (onExpand) onExpand(); }}
          onMouseDown={(e) => e.stopPropagation()}
          title="全屏预览"
        >
          <FullscreenIcon />
        </button>
      </div>
    </div>
  </div>
)}
```

## 控件设计规范

- 播放按钮：36px 圆圈
- 进度条：底部 3-4px 细条
- 时间显示：悬停时右下角
- 图标大小：12-14px
- 不要文字提示（快捷键说明等）
- 间距紧凑，padding 减小

## 陷阱

### 1. 父容器 onClick 阻止子元素点击
```tsx
// ❌ 错误 - e.preventDefault() 阻止子元素点击
<div onClick={(e) => { e.stopPropagation(); e.preventDefault(); setShowControls(true); }}>
  <VideoPreview onExpand={() => setShowPreview(true)} />  {/* 点击无效 */}
</div>

// ✅ 正确 - 只用 stopPropagation
<div onClick={(e) => { e.stopPropagation(); setShowControls(true); }}>
  <VideoPreview onExpand={() => setShowPreview(true)} />  {/* 正常 */}
</div>
```

### 2. 控件区域用 onMouseDown 不用 onClick
```tsx
// ❌ 错误 - onClick 阻止冒泡会导致子按钮失效
<div onClick={(e) => e.stopPropagation()}>
  <button onClick={togglePlay}>不工作！</button>
</div>

// ✅ 正确 - onMouseDown 只阻止拖拽，不影响 click
<div onMouseDown={(e) => e.stopPropagation()}>
  <button onClick={togglePlay}>正常工作</button>
</div>
```

### 3. VideoPreview 不添加 onClick
```tsx
// ❌ 错误 - VideoPreview 自己处理 onClick，事件不冒泡
<div onClick={handleClick} onDoubleClick={handleDoubleClick}>
  {/* 父容器收不到点击事件 */}
</div>

// ✅ 正确 - VideoPreview 不处理 onClick，让事件冒泡
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  // 没有 onClick
>
  {/* 父容器的 onClick 会被触发 */}
</div>
```

### 4. ReactFlow onNodeDoubleClick 拦截
不要在 ReactFlow 组件上设置 `onNodeDoubleClick`，即使是空函数也会拦截双击事件。完全移除该 prop。

### 5. setShowPreview 类型
```tsx
// ❌ showPreview 是 boolean，但 PreviewModal 需要 string URL
const [showPreview, setShowPreview] = useState(false);
{showPreview && previewUrl && <PreviewModal url={previewUrl} ... />}
// ✅ 正确：条件是 showPreview && previewUrl，两个都要检查
```
