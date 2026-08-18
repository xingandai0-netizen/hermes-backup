# Video Preview & Asset Naming Patterns

## VideoPreview Component (Hover-to-Play)

### Core Implementation
```tsx
interface VideoPreviewProps {
  src: string;
  height?: number;
  autoPlay?: boolean;
  loop?: boolean;
  muted?: boolean;
  controls?: boolean;
  hoverToPlay?: boolean;
  onExpand?: () => void;
}

// Usage in node
<VideoPreview
  src={proxyUrl(previewUrl) || previewUrl}
  height={220}
  loop
  muted
  controls
  hoverToPlay
  onExpand={() => setShowPreview(true)}
/>
```

### Hover-to-Play Logic
```tsx
useEffect(() => {
  if (!hoverToPlay || !videoRef.current) return;
  
  if (isHovered) {
    videoRef.current.currentTime = 0;
    videoRef.current.play().catch(() => {});
  } else {
    videoRef.current.pause();
    videoRef.current.currentTime = 0;
  }
}, [isHovered, hoverToPlay]);
```

### Interaction Model (TapNow Style)
- **Hover**: Play from beginning
- **Leave**: Pause and reset to start
- **Click**: No action (only stopPropagation)
- **Double-click**: Open fullscreen preview dialog
- **Expand button**: Open PreviewModal

### Pitfalls
1. ❌ Don't add onClick to outer div - prevents ReactFlow node selection
2. ✅ Use onMouseDown for controls area to stop propagation
3. ✅ Double-click opens PreviewModal, not single click

## Asset Naming System

### localStorage Counter
```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}

// In node creation
const assetName = type === "IMAGE" 
  ? `图素材${getNextAssetNumber('IMAGE')}`
  : `视频素材${getNextAssetNumber('VIDEO')}`;
```

### Display Location
- **Position**: Outside preview area, top-left corner
- **Style**: Icon + name, semi-transparent background
- **Data source**: `d.assetName` (NOT `cfg.assetName`)

```tsx
{/* Asset name label - outside preview */}
<div style={{
  display: "flex",
  alignItems: "center",
  gap: 4,
  padding: "4px 8px 4px 4px",
  marginBottom: 4,
}}>
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" 
       stroke="rgba(255,255,255,0.6)" strokeWidth="2">
    {/* Icon based on type */}
  </svg>
  <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)" }}>
    {d.assetName || "素材"}
  </span>
</div>
```

## @Mention System

### MentionInput Component
```tsx
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ 
      id: img.assetName, 
      name: img.assetName, 
      type: 'image' as const 
    })),
    ...upstream.videos.map(vid => ({ 
      id: vid.assetName, 
      name: vid.assetName, 
      type: 'video' as const 
    })),
  ]}
  placeholder="输入@引用素材"
/>
```

### Features
- Input @ to show asset list
- Keyboard navigation (↑↓, Enter, ESC)
- Type-specific icons
- Default options when no connected assets

## Upstream Asset Detection

### getUpstreamAssets Function
```typescript
const getUpstreamAssets = useCallback(() => {
  const incomingEdges = edges.filter((e) => e.target === props.id);
  const assets = { images: [], videos: [] };

  for (const edge of incomingEdges) {
    const sourceNode = nodes.find((n) => n.id === edge.source);
    if (sourceNode) {
      const nodeData = sourceNode.data as unknown as NodeData;
      const assetName = nodeData.assetName || "素材";
      const nodeType = nodeData.nodeType;

      // Judge by node type, not by URL existence
      if (nodeType === "IMAGE") {
        assets.images.push({ url: url || "", assetId: "", assetName });
      } else if (nodeType === "VIDEO") {
        assets.videos.push({ url: url || "", assetId: "", assetName });
      }
    }
  }
  return assets;
}, [edges, nodes, props.id]);
```

## Prompt Construction with Asset References

### Format
```
[图片素材1: 图素材1] [图片素材2: 图素材2] [视频素材1: 视频素材1]
User's prompt here
```

### Implementation
```typescript
const refs: string[] = [];
upstream.images.forEach((img, i) => {
  refs.push(`[图片素材${i + 1}: ${img.assetName}]`);
});
upstream.videos.forEach((vid, i) => {
  refs.push(`[视频素材${i + 1}: ${vid.assetName}]`);
});
if (refs.length > 0) {
  fullPrompt = `${refs.join(' ')}\n${prompt}`;
}
```

## Handle/Connector Styling

### Best Practices
```typescript
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${categoryColor}, 0 0 10px ${categoryColor}80`
    : `0 0 10px ${categoryColor}70`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
  opacity: isHovered ? 1 : 0,
};
```

### Position & Interaction
- Distance from node: `left/right: -28px`
- Hover detection zone: outer container `padding: 40px`
- Delayed hide: 10 seconds after mouse leave
- Outward expansion: `transformOrigin: "right center"` (left) / `"left center"` (right)
