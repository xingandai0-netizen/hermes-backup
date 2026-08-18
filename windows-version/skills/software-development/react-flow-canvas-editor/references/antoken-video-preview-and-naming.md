# Antoken VideoPreview & Material Naming Patterns

## VideoPreview Component (TapNow Style)

### Interaction Model
- **Hover to play**: Mouse enters → play from start; mouse leaves → pause and reset
- **Single click**: Select node (for delete key) + show control panel
- **Double click**: Open PreviewModal fullscreen (if onDoubleClick provided)
- **Expand button**: In controls bar, opens PreviewModal

### Key Implementation Rules
1. **NO stopPropagation on preview area** — breaks node selection
2. **Controls show on hover** (not just when playing)
3. **Progress bar + time display** in bottom controls
4. **Play/pause, skip ±5s, speed, mute, expand** buttons in controls

```tsx
<VideoPreview
  src={proxyUrl(url) || url}
  height={220}
  loop
  muted
  controls
  hoverToPlay
  onExpand={() => setShowPreview(true)}
/>
```

### Component Structure
```tsx
// VideoPreview.tsx
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;  // default false
  loop?: boolean;      // default true
  muted?: boolean;     // default true
  controls?: boolean;  // default true
  hoverToPlay?: boolean; // default true
  onDoubleClick?: () => void;
  onExpand?: () => void;
  className?: string;
  style?: React.CSSProperties;
}
```

## Material Naming System

### Storage
- `assetName` stored in `node.data` (NOT `node.data.config`)
- Read with `d.assetName` not `cfg.assetName`

### Counter Logic (localStorage persistent)
```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

### Naming Convention
- Images: 图素材1, 图素材2, 图素材3...
- Videos: 视频素材1, 视频素材2, 视频素材3...

### Display Location
- **Outside preview area** (top-left, above preview)
- Icon + name label
- Semi-transparent background

```tsx
{/* 素材名称标签 - 在预览区外面 */}
<div style={{ display: "flex", alignItems: "center", gap: 4, padding: "4px 8px 4px 4px", marginBottom: 4 }}>
  <svg ... /> {/* image or video icon */}
  <span>{d.assetName || "图素材"}</span>
</div>
```

## @ Mention System (MentionInput)

### Component: MentionInput.tsx
- Input @ to trigger material list popup
- Keyboard navigation (↑↓ arrows, Enter to select, Esc to close)
- Shows connected materials OR default options if none connected

### Usage
```tsx
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ id: img.assetName, name: img.assetName, type: 'image' })),
    ...upstream.videos.map(vid => ({ id: vid.assetName, name: vid.assetName, type: 'video' })),
  ]}
  placeholder="输入@引用素材..."
  disabled={loading}
/>
```

### Default Options (when no connections)
```typescript
const defaultMentions = [
  { id: 'default-image-1', name: '图素材1', type: 'image' },
  { id: 'default-video-1', name: '视频素材1', type: 'video' },
];
```

## Handle (Connection Node) Styling

### Dimensions & Position
- Size: 20×20px
- Distance from node: -28px (left/right)
- Hover scale: 1.5x
- Glow effect: 3-layer box-shadow

### Visibility
- **Hidden by default** (opacity: 0)
- **Shown on hover** with 10-second delay before hiding
- Hover zone extends 40px beyond node boundary

```typescript
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${categoryColor}, 0 0 10px ${categoryColor}80, 0 0 5px ${categoryColor}60`
    : `0 0 10px ${categoryColor}70, 0 0 4px ${categoryColor}50`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
  opacity: isHovered ? 1 : 0,
  pointerEvents: (isHovered ? "auto" : "none") as React.CSSProperties["pointerEvents"],
};
```

### Hover Delay Implementation
```typescript
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) {
    clearTimeout(hideTimerRef.current);
    hideTimerRef.current = null;
  }
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => {
    setIsHovered(false);
  }, 10000); // 10 seconds
}, []);
```

## Node Selection & Delete

### Rules
1. Click preview area → node selected (NO stopPropagation)
2. Delete key works when node selected AND no input focused
3. Delete key also works when input focused BUT input is empty
