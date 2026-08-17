# VideoPreview Component Patterns

## TapNow-Style Video Preview

### Core Interaction Model
1. **Hover** → Play video from start
2. **Leave** → Pause and reset to start
3. **Click** → Show control panel (对话交流框)
4. **Expand button** → Open PreviewModal (全屏预览)

### Component Structure
```tsx
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;  // default: false
  loop?: boolean;      // default: true
  muted?: boolean;     // default: true
  controls?: boolean;  // default: true
  hoverToPlay?: boolean; // default: true
  onExpand?: () => void; // Opens PreviewModal
  className?: string;
  style?: React.CSSProperties;
}
```

### Key Implementation Rules

1. **No onClick on outer div** - Let clicks bubble to ReactFlow for node selection
2. **Use onMouseDown for controls** - Prevent drag initiation on control buttons
3. **Use onExpand not onDoubleClick** - Double-click is intercepted by ReactFlow

### Hover Play Logic
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

### Control Panel (Bottom)
- Show on hover (always, not just when playing)
- Contains: progress bar, play/pause, skip ±5s, time, speed, mute, expand
- Use `onMouseDown={(e) => e.stopPropagation()}` on control buttons

### Expand Button
```tsx
<button
  onClick={(e) => {
    e.stopPropagation();
    if (onExpand) onExpand();
  }}
  onMouseDown={(e) => e.stopPropagation()}
>
  {/* Fullscreen icon */}
</button>
```

## Pitfalls

1. **ReactFlow intercepts double-click** - Don't use onDoubleClick, use onExpand button instead
2. **stopPropagation breaks node selection** - Don't add onClick to VideoPreview outer div
3. **Controls should show on hover** - Not just when playing
4. **Plyr doesn't work in Next.js** - Use native video + custom controls
5. **Progress bar seeking** - Use onMouseDown for drag, onClick for click-to-seek

## Animation
```css
@keyframes popUp {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Use with cubic-bezier for spring effect */
animation: popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
```
