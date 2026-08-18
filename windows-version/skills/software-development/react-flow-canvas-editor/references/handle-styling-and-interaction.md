# Handle Styling, Hover Zones, and Interaction Patterns

## Handle (Connection Node) Styling

Position handles OUTSIDE the node with glow animation and delayed hide:

```tsx
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
  opacity: isHovered ? 1 : 0,
  pointerEvents: isHovered ? "auto" : "none",
};

// Handle position: -28px from node edge
<Handle style={{ ...handleStyle, left: -28, transformOrigin: "right center" }} />
<Handle style={{ ...handleStyle, right: -28, transformOrigin: "left center" }} />
```

## Hover Zone Extension (40px around node)

Use `padding: 40` + `margin: -40` on outer container to extend hover detection:

```tsx
<div
  onMouseEnter={handleMouseEnter}
  onMouseLeave={handleMouseLeave}
  style={{ position: "relative", width: 280, padding: 40, margin: -40 }}
>
  {/* Node content */}
  <Handle left: 12 />  {/* 40 - 28 = 12 */}
  <Handle right: 12 />
</div>
```

## Delayed Hide (10s after mouse leave)

Keeps handles visible for 10s after mouse leaves, useful during connection dragging:

```tsx
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) clearTimeout(hideTimerRef.current);
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => setIsHovered(false), 10000);
}, []);
```

## Viewport-Aware Node Positioning

New nodes should appear at current viewport center, not fixed position:

```tsx
// In workflowStore.ts
viewport: { x: 0, y: 0, zoom: 1 },
updateViewport: (viewport) => set({ viewport }),

// In WorkflowCanvas.tsx - track viewport
const onMove = useCallback((_, viewport) => updateViewport(viewport), []);

// In sidebar node creation
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
newNode.position = { x: centerX - 140, y: centerY - 100 };
```

## Click Event Handling Pitfalls

ReactFlow intercepts click/double-click events on nodes.

1. **Single click → show control panel**: Add `onClick` on node's preview container that calls `setShowControls(true)`. Don't stopPropagation on the preview container.
2. **Fullscreen preview**: Use a button in the controls area, NOT double-click (ReactFlow intercepts dblclick).
3. **VideoPreview component**: Must NOT have `onClick` that stops propagation on its outer div, or ReactFlow can't select the node.
4. **Controls area**: Use `onMouseDown={(e) => e.stopPropagation()}` to prevent node drag while interacting with controls.
5. **Don't add `e.preventDefault()` on click** — blocks all click behavior.

## Video Preview Component (TapNow-style)

```tsx
<VideoPreview
  src={url}
  height={220}
  loop
  muted
  controls
  hoverToPlay          // play on hover, pause on leave
  onExpand={() => setShowPreview(true)}  // fullscreen button callback
/>
```

Key behaviors:
- Hover → play from start
- Leave → pause and reset
- Single click → no action (let ReactFlow handle selection)
- Fullscreen button in controls → opens PreviewModal
- Controls area uses `onMouseDown` stopPropagation to prevent node drag

## Asset Naming Convention

Auto-name assets based on type and creation order:

```tsx
let imageCounter = 0;
let videoCounter = 0;

function getAssetName(nodeType: string): string {
  if (nodeType === "IMAGE") { imageCounter++; return `图素材${imageCounter}`; }
  if (nodeType === "VIDEO") { videoCounter++; return `视频素材${videoCounter}`; }
  return "素材";
}
```

Pass asset names in prompt for model reference:
```
[图片素材: 图素材1] [视频素材: 视频素材1]
让图素材1中的人物穿着视频素材1中的衣服...
```
