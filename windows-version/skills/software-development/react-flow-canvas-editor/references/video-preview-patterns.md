# Video Preview Patterns (TapNow Style)

## Core Interaction Model

| Action | Behavior | Implementation |
|--------|----------|----------------|
| Hover | Play video from start | `onMouseEnter` → `video.currentTime = 0; video.play()` |
| Leave | Pause and reset | `onMouseLeave` → `video.pause(); video.currentTime = 0` |
| Single click | Show control panel (对话交流框) | Parent div `onClick` → `setShowControls(true)` |
| Expand button | Open PreviewModal fullscreen | Button `onClick` → `onExpand()` |

## CRITICAL: VideoPreview Outer Div Must NOT Have onClick

```tsx
// ❌ WRONG - blocks parent click events
<div onClick={togglePlay}>
  <video ... />
</div>

// ✅ CORRECT - let events bubble to parent
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  // NO onClick!
>
  <video ... />
</div>
```

## Component Props

```tsx
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;      // default: false
  loop?: boolean;           // default: true
  muted?: boolean;          // default: true
  controls?: boolean;       // default: true
  hoverToPlay?: boolean;    // default: true
  onExpand?: () => void;    // fullscreen button callback
  className?: string;
  style?: React.CSSProperties;
}
```

## Asset Name Label (Outside Preview)

```tsx
{/* 素材名称标签 - 在预览区外面 */}
<div style={{
  display: "flex",
  alignItems: "center",
  gap: 4,
  padding: "4px 8px 4px 4px",
  marginBottom: 4,
}}>
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="2">
    <polygon points="5 3 19 12 5 21 5 3" /> {/* video icon */}
  </svg>
  <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>
    {d.assetName || "视频素材"}
  </span>
  {upstream.images.length + upstream.videos.length > 0 && (
    <span style={{ fontSize: 9, color: "rgba(255,255,255,0.4)", marginLeft: 4 }}>
      ({upstream.images.length + upstream.videos.length}个素材)
    </span>
  )}
</div>
```

## Control Panel (对话交流框)

```tsx
{showControls && (
  <div onMouseDown={(e) => e.stopPropagation()}>
    <textarea placeholder="输入@引用素材..." />
    <select>{/* 模型选择 */}</select>
    <button onClick={handleGenerate}>生成</button>
  </div>
)}
```

## Controls Area

```tsx
{controls && isHovered && !isLoading && !hasError && (
  <div
    style={{
      position: "absolute",
      bottom: 0,
      left: 0,
      right: 0,
      background: "linear-gradient(transparent, rgba(0,0,0,0.8))",
      padding: "20px 8px 8px",
      zIndex: 20,
    }}
    onMouseDown={(e) => e.stopPropagation()}  // Prevent drag
  >
    {/* Progress bar */}
    {/* Play/Pause, Skip, Time, Speed, Volume, Expand buttons */}
  </div>
)}
```

## Pitfalls

1. **onClick on outer div** - Blocks parent click, prevents control panel from showing
2. **stopPropagation on controls div** - Use `onMouseDown` not `onClick` to prevent drag
3. **autoPlay=true default** - Changed to false, hoverToPlay=true instead
4. **Asset name in config** - Read from `d.assetName`, not `cfg.assetName`
5. **Controls always visible** - Only show on hover: `isHovered && !isLoading`
