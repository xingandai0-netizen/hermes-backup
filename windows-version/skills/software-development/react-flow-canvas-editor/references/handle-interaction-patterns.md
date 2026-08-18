# Handle & Interaction Patterns (2026-06-15)

## Handle (Connection Node) Styling

Position handles OUTSIDE the node with distance, hover-reveal, and outward expansion:

```tsx
// BaseNode.tsx
const [isHovered, setIsHovered] = useState(false);

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

// Wrap node in hover zone (40px padding) - hover anywhere in zone triggers handles
<div style={{ padding: 40, background: "transparent" }}
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}>
  <div style={{ width: 280, ... }}>
    {children}
    <Handle type="target" position={Position.Left} id="input"
      style={{ ...handleStyle, left: 12, transformOrigin: "right center" }} />
    <Handle type="source" position={Position.Right} id="output"
      style={{ ...handleStyle, right: 12, transformOrigin: "left center" }} />
  </div>
</div>
```

**Key:** `transformOrigin` must be set per-side so scale expands OUTWARD (away from node), not inward.

## Viewport-Based Node Placement

New nodes should appear at current viewport center, not fixed position:

```tsx
// workflowStore.ts - add viewport tracking
interface ViewportPosition { x: number; y: number; zoom: number; }
// State: viewport: { x: 0, y: 0, zoom: 1 }
// Action: updateViewport: (viewport) => set({ viewport })

// WorkflowCanvas.tsx - track viewport changes
const { updateViewport } = useWorkflowStore();
const onMove = useCallback((_: any, viewport: { x: number; y: number; zoom: number }) => {
  updateViewport(viewport);
}, [updateViewport]);
// Add onMove={onMove} to <ReactFlow>

// Sidebar node creation - use viewport center
const { viewport } = useWorkflowStore();
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
const newNode = { position: { x: centerX - 140, y: centerY - 100 }, ... };
```

## Delete Key Optimization

Delete/Backspace should work even when input is focused, IF input is empty:

```tsx
const handler = (e: KeyboardEvent) => {
  const target = e.target as HTMLElement;
  const tag = target.tagName;
  const isInputFocused = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
  
  if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
    if (isInputFocused) {
      const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
      if (inputValue && inputValue.length > 0) return; // Don't delete node if input has content
    }
    e.preventDefault();
    removeNode(selectedNodeId);
  }
};
```

## VideoPreview Component Pattern

Hover to play, click shows control panel, expand button for PreviewModal:

```tsx
interface VideoPreviewProps {
  src: string;
  hoverToPlay?: boolean;  // default true
  onExpand?: () => void;  // called by expand button in controls
  // NO onClick - let events bubble to ReactFlow for node selection
}

// Key: Do NOT add onClick to VideoPreview outer div
// This prevents ReactFlow from selecting the node
// Instead, parent div handles click to show control panel
```

## UI Terminology (阿戴 specific)

- "对话交流框" / "对话框" = Control panel inside node (input prompt, model select, generate button)
- "放大预览" = PreviewModal fullscreen preview
- These are DIFFERENT - never confuse them
