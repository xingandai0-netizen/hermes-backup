# ReactFlow Performance Optimization Patterns (2026-06-14)

## Memoize ReactFlow Props (CRITICAL)

**Problem:** ReactFlow props create new object references every render if defined inline, triggering unnecessary internal updates.

**Solution:** Use `useMemo` for all object/array props:

```tsx
const defaultEdgeOpts = useMemo(() => ({
  animated: true,
  style: { stroke: "#ffffff", strokeWidth: 2.5, strokeOpacity: 0.8 },
  type: "smoothstep" as const,
}), []);

const connLineStyle = useMemo(() => ({
  stroke: "#ffffff", strokeWidth: 3, strokeDasharray: "8 4"
}), []);

const snapGridValue: [number, number] = useMemo(() => [16, 16], []);
const proOpts = useMemo(() => ({ hideAttribution: true }), []);
const defaultVP = useMemo(() => ({ x: 0, y: 0, zoom: 1 }), []);

// Background/MiniMap styles
const bgStyle = useMemo(() => ({ background: "#000" }), []);
const miniMapStyle = useMemo(() => ({
  background: "#0f1011",
  border: "1px solid rgba(255,255,255,0.08)",
  borderRadius: 8,
}), []);

// nodeColor for MiniMap
const nodeColor = useCallback((node: Node) => {
  const d = node.data as unknown as NodeData;
  const colors: Record<string, string> = {
    INPUT: "#27a644",
    AI_GENERATION: "#7170ff",
    PROCESSING: "#3b82f6",
    OUTPUT: "#f59e0b",
  };
  return colors[d.category] ?? "rgba(255,255,255,0.05)";
}, []);
```

## Safe vs Unsafe Optimizations

| Optimization | Status | Notes |
|-------------|--------|-------|
| `useMemo` on object/array props | ✅ Safe | Prevents unnecessary re-renders |
| `useCallback` on event handlers | ✅ Safe | Standard React optimization |
| `useCallback` on `nodeColor` | ✅ Safe | For MiniMap component |
| `React.memo` on node components | ❌ Unsafe | BREAKS ReactFlow event handling |
| `onlyRenderVisibleElements` | ❌ Unsafe | Causes page freeze |
| CSS `transform` on `.react-flow__node` | ❌ Unsafe | Breaks positioning |
| CSS `!important` overrides | ❌ Unsafe | Interferes with ReactFlow internals |

## Snap-to-Grid: Default Off with Toggle

**UX Pattern:** `snapToGrid` should default to `false` for smooth movement. Add toggle button.

```tsx
const [snapEnabled, setSnapEnabled] = useState(false);

<ReactFlow
  snapToGrid={snapEnabled}
  snapGrid={snapGridValue}
/>

// Toggle button near Controls
<button
  onClick={() => setSnapEnabled(!snapEnabled)}
  style={{
    position: "absolute",
    bottom: 80,
    left: 12,
    width: 32,
    height: 32,
    background: snapEnabled ? "var(--accent-bright, #5e6ad2)" : "var(--bg-elevated, #191a1b)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: 6,
    color: snapEnabled ? "#fff" : "#8a8f98",
    cursor: "pointer",
  }}
  title={snapEnabled ? "关闭网格吸附" : "开启网格吸附"}
>
  {/* Grid icon SVG */}
</button>
```

## CSS Animation Safety Rules

**Safe properties:**
- `box-shadow` — hover/selected states
- `border` — selection indicators
- `width`/`height` — handle hover effects
- `background` — control buttons

**NEVER use on `.react-flow__node`:**
- `transform` — ReactFlow uses `transform: translate(x,y)` for positioning
- `scale` — breaks node position calculations
- `translateY`/`translateX` — overrides internal positioning

**Safe hover example:**
```css
.react-flow__node:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
.react-flow__node.selected {
  box-shadow: 0 0 0 2px var(--accent-bright), 0 4px 24px rgba(113, 112, 255, 0.2);
}
```

## Multiple Sidebar Components

Antoken has TWO sidebar components:
1. `NodePanel.tsx` — Simple list-style
2. `CircleNavPanel.tsx` — Card-style with icons

When modifying visible nodes, check BOTH files.

**Filtering pattern:**
```tsx
{NODE_DEFINITIONS.filter(d => d.type !== "COMPOSITE").map((def) => {
  // render card
})}
```
