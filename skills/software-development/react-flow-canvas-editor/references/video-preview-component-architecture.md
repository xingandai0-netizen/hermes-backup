# Video Preview Component Architecture

## Component Props

```tsx
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;   // Default: '100%'
  height?: number | string;  // Default: 220
  autoPlay?: boolean;        // Default: false (conflicts with hoverToPlay)
  loop?: boolean;            // Default: true
  muted?: boolean;           // Default: true
  controls?: boolean;        // Default: true
  hoverToPlay?: boolean;     // Default: true
  onExpand?: () => void;     // For fullscreen preview button
  className?: string;
  style?: React.CSSProperties;
}
```

## Event Handling (CRITICAL)

### 外层div事件
```tsx
<div
  // ✅ 只有hover事件，没有onClick
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
>
```

### 控件区域事件
```tsx
<div
  // ✅ 用onMouseDown阻止拖拽，不影响click
  onMouseDown={(e) => e.stopPropagation()}
>
  <button onClick={togglePlay}>Play</button>
  <div onClick={handleSeek}>Progress</div>
</div>
```

### 全屏按钮事件
```tsx
<button
  onClick={(e) => {
    e.stopPropagation();
    if (onExpand) onExpand();
  }}
  onMouseDown={(e) => e.stopPropagation()}
>
  <FullscreenIcon />
</button>
```

## Hover-to-Play Pattern

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

## Controls Layout

```
[⏮] [⏯] [⏭] | 0:05 / 0:10 | [1x] [🔇] [⛶]
```

- Left: skip back, play/pause, skip forward
- Center: time display
- Right: playback speed, mute, fullscreen

## Parent Component Integration

```tsx
// VideoNode.tsx
<div
  onClick={(e) => {
    e.stopPropagation();
    setShowControls(true);  // 显示控制面板（对话交流框）
  }}
>
  <VideoPreview
    src={proxyUrl(previewUrl)}
    hoverToPlay
    onExpand={() => setShowPreview(true)}  // 全屏按钮
  />
</div>

{showControls && (
  <div onMouseDown={(e) => e.stopPropagation()}>
    {/* 控制面板内容 */}
  </div>
)}
```

## Pitfalls

1. **onClick on outer div** → Prevents parent from catching click → No dialog appears
2. **onClick on control area** → Breaks child buttons → Use onMouseDown instead
3. **autoPlay=true** → Conflicts with hoverToPlay → Set autoPlay=false
4. **No pointerEvents: 'none' on play overlay** → Overlay blocks click events
