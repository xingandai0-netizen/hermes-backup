# Handle, Viewport, VideoPreview, and Delete Key Optimizations

## Handle (Connection Point) Styling

### Recommended Configuration (20px, outward glow, hover animation)
```typescript
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${color}, 0 0 10px ${color}80, 0 0 5px ${color}60`
    : `0 0 10px ${color}70, 0 0 4px ${color}50`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
};
```

### Rules
- **Size**: 20×20px minimum (14px too small to click)
- **Distance**: `left: -20px` / `right: -20px` (outside node, with gap)
- **Glow**: 3-layer box-shadow for neon effect
- **Hover**: scale(1.5) with elastic cubic-bezier(0.34, 1.56, 0.64, 1)
- **Transform-origin**: Left handle → `right center`, Right → `left center` (expand outward)
- **z-index**: 20

### Handle JSX
```tsx
<Handle type="target" position={Position.Left} id="input"
  style={{ ...handleStyle, left: -20, zIndex: 20, transformOrigin: "right center" }} />
<Handle type="source" position={Position.Right} id="output"
  style={{ ...handleStyle, right: -20, zIndex: 20, transformOrigin: "left center" }} />
```

---

## Viewport-Aware Node Placement

New nodes appear at current viewport center, not fixed (300,150).

### Zustand Store
```typescript
interface ViewportPosition { x: number; y: number; zoom: number; }
// In state:
viewport: { x: 0, y: 0, zoom: 1 },
updateViewport: (viewport) => set({ viewport }),
```

### Canvas (track viewport)
```typescript
const { updateViewport } = useWorkflowStore();
const onMove = useCallback((_, viewport) => updateViewport(viewport), [updateViewport]);
<ReactFlow onMove={onMove} ...>
```

### Sidebar (place at center)
```typescript
const { addNode, viewport } = useWorkflowStore();
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
newNode.position = { x: centerX - 140, y: centerY - 100 };
```

---

## Delete Key Optimization

Default: blocked when focus is INPUT/TEXTAREA/SELECT. Fix: delete node if input is empty.

```typescript
const handler = (e: KeyboardEvent) => {
  const target = e.target as HTMLElement;
  const isInputFocused = target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.tagName === "SELECT";
  
  if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
    if (isInputFocused) {
      const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
      if (inputValue && inputValue.length > 0) return; // input has content, don't delete node
    }
    e.preventDefault();
    removeNode(selectedNodeId);
  }
};
```

---

## VideoPreview Component (TapNow-style)

### Behavior
| Action | Result |
|--------|--------|
| Hover | Play from start |
| Leave | Pause and reset to 0 |
| Click | No action (bubble to ReactFlow) |
| Double-click | Open PreviewModal |
| Controls bar | Show on hover |
| Fullscreen btn | Opens PreviewModal |

### Critical Pitfall
**Do NOT** add `onClick={e => e.stopPropagation()}` on the VideoPreview wrapper div. This prevents ReactFlow from selecting the node, and the property panel won't show on click.

### Component Interface
```typescript
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;
  loop?: boolean;
  muted?: boolean;
  controls?: boolean;
  hoverToPlay?: boolean;
  onExpand?: () => void;  // fullscreen button callback
  className?: string;
  style?: React.CSSProperties;
}
```

### Usage in Nodes
```tsx
<VideoPreview
  src={proxyUrl(videoUrl) || videoUrl}
  height={220}
  loop
  muted
  controls
  hoverToPlay
  onExpand={() => setShowPreview(true)}
/>
```
