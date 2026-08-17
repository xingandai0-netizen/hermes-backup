# Antoken v0.5 UI & Workflow Learnings (2026-06-15)

## Critical Pitfalls

### ReactFlow Edge Replacement Bug
**Symptom**: When connecting multiple source nodes to the same target handle, only the last connection is kept.
**Root cause**: `addEdge()` from `@xyflow/react` may generate duplicate edge IDs for connections to the same target handle, replacing earlier edges.
**Fix**: Generate unique edge IDs with `Date.now()` and append directly to the array:
```typescript
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  set((s) => {
    const edgeId = `edge-${connection.source}-${connection.sourceHandle || 'output'}-${connection.target}-${connection.targetHandle || 'input'}-${Date.now()}`;
    const newEdge = { id: edgeId, ...connection, animated: true, style: { stroke: "#ffffff", strokeWidth: 2 }, type: "smoothstep" };
    const updated = [...s.edges, newEdge];
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},
```

### File Corruption with read_file/write_file
**Symptom**: Files get corrupted with line numbers embedded in content (e.g., `1|1|"use client";`).
**Root cause**: Using `read_file` then `write_file` to modify files corrupts them.
**Fix**: Always use the `patch` tool for edits. Never use `read_file` + `write_file` pattern.

### stopPropagation Blocks Node Selection
**Symptom**: Clicking a node's preview area doesn't select the node, making Delete key impossible to trigger.
**Root cause**: `e.stopPropagation()` on child elements prevents ReactFlow from receiving the click event.
**Fix**: Remove `stopPropagation` from preview areas. Only use it on specific interactive elements (buttons, inputs, control panels).

---

## UI Patterns (TapNow-style)

### Video Preview Interaction
```tsx
<VideoPreview
  src={url}
  height={220}
  loop
  muted
  controls
  hoverToPlay           // Mouse enter = play, mouse leave = pause + reset
  onExpand={() => setShowPreview(true)}  // Fullscreen button opens PreviewModal
/>
```
- **Hover play**: Mouse enter → play from start, mouse leave → pause + reset to 0
- **Click**: No action (only stops propagation)
- **Fullscreen button**: Opens PreviewModal (not click on video)

### Handle Visibility Pattern
```tsx
// Hide by default, show on hover with 40px detection zone, 10s delay before hiding
const [isHovered, setIsHovered] = useState(false);
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) { clearTimeout(hideTimerRef.current); hideTimerRef.current = null; }
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => setIsHovered(false), 10000);
}, []);
```

Handle style:
```tsx
const handleStyle = {
  width: 20, height: 20,
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

Handle position: `left: -28` / `right: -28` (outside node, with padding 40px hover zone)

### Hover Detection Zone (40px around node)
```tsx
<div
  onMouseEnter={handleMouseEnter}
  onMouseLeave={handleMouseLeave}
  style={{ position: "relative", width: 280, padding: 40, margin: -40, boxSizing: "content-box" }}
>
  {/* Node content */}
  {/* Handles positioned inside padding area */}
</div>
```

---

## Asset Naming Pattern (localStorage Persistent Counter)

```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

Display in node: `{d.assetName || "视频素材"}` (read from `data.assetName`, NOT `config.assetName`)

---

## @Mention Input Component

For referencing connected assets in prompts:
- Input `@` → popup menu with connected assets
- Keyboard navigation (↑↓, Enter, Escape)
- Show default options when no connections exist
- Use `mentions` array from `getUpstreamAssets()`

---

## Multi-Asset Upload Logic

### Correct Pattern
```typescript
const getUpstreamAssets = useCallback(() => {
  const incomingEdges = edges.filter((e) => e.target === props.id);
  const assets = { images: [], videos: [] };
  
  for (const edge of incomingEdges) {
    const sourceNode = nodes.find((n) => n.id === edge.source);
    if (sourceNode) {
      const nodeData = sourceNode.data as unknown as NodeData;
      const url = nodeData.assetUrl || (nodeData.config as any)?.assetUrl;
      const assetName = nodeData.assetName || (nodeData.config as any)?.assetName || "素材";
      const nodeType = nodeData.nodeType || (nodeData.config as any)?.nodeType;
      
      // Use nodeType, NOT url presence, to determine type
      if (nodeType === "IMAGE") assets.images.push({ url: url || "", assetName });
      else if (nodeType === "VIDEO") assets.videos.push({ url: url || "", assetName });
    }
  }
  return assets;
}, [edges, nodes, props.id]);
```

### Prompt Construction
```
[素材1: 图素材5] [素材2: 图素材7] [素材3: 视频素材1]
让@图素材5的角色穿着@图素材7的衣服跳舞
```

### API Payload
```json
{
  "prompt": "[素材1: 图素材5] [素材2: 图素材7]...",
  "reference_image_urls": ["url1", "url2"],
  "reference_video_urls": ["url3"]
}
```
Backend converts to `image_with_roles` / `video_with_roles` with `asset://` protocol.

---

## Node Positioning (Viewport Center)

New nodes should appear at current viewport center, not fixed position:
```typescript
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
// Node position: { x: centerX - 140, y: centerY - 100 }
```

Store viewport state in workflowStore, update via `onMove` callback on ReactFlow.
