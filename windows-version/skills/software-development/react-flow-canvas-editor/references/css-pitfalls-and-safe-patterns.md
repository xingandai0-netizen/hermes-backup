# React Flow CSS/JS Pitfalls & Safe Patterns

> Absorbed from `react-flow-css-pitfalls` skill (archived 2026-06-21).

## Absolute Prohibitions

### Never override node transform
React Flow uses `transform: translate(x, y)` for node positioning. Overriding breaks positioning.

```css
/* ❌ BREAKS React Flow positioning */
.react-flow__node:hover { transform: translateY(-1px) !important; }
.react-flow__node.dragging { transform: scale(1.02) !important; }
```

### Never use onlyRenderVisibleElements
```jsx
/* ❌ May cause rendering issues */
<ReactFlow onlyRenderVisibleElements={true} />
```

## CSS !important Conflicts with JS Edge Styles (Critical)

`globals.css` `.react-flow__edge-path` with `!important` completely overrides JS-set edge styles (selection highlighting).

```css
/* ❌ Overrides all JS edge styling */
.react-flow__edge-path { stroke: #ffffff !important; stroke-width: 2 !important; }

/* ✅ Only transition, let JS control styles */
.react-flow__edge-path { transition: stroke 0.2s ease; }
```

## Safe Patterns

| Element | transform safe? | Reason |
|---------|----------------|--------|
| `.react-flow__node` | ❌ | RF uses transform for positioning |
| `.react-flow__edge` | ❌ | RF uses transform for positioning |
| `.react-flow__handle` | ✅ | Handle positioning doesn't depend on transform |
| `.react-flow__minimap` | ✅ | Independent component |
| `.react-flow__controls` | ✅ | Independent component |

Safe hover effects:
```css
.react-flow__node:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important; }
.react-flow__node.selected { box-shadow: none !important; } /* Remove RF default purple glow */
.react-flow__handle:hover { width: 14px !important; height: 14px !important; }
```

## Multi-Edge Connection Loss (Hardest RF Bug)

Three mandatory fixes — all required:

1. `ConnectionMode.Loose` on ReactFlow
2. `onEdgesChange` must filter to ONLY `select` type (not just `remove` — `replace` also causes edge loss!)
3. `onConnect` must direct-append `[...s.edges, newEdge]`, never use `addEdge`
4. Separate `removeEdge` function for user-initiated deletion
5. Context menu uses `removeEdge`, not `onEdgesChange`

## Interactive Element Drag Conflict

Use RF's built-in `nodrag` class (official recommended approach):
```tsx
<select className="nodrag" onChange={handleChange}>
<textarea className="nodrag" ref={inputRef}>
<input className="nodrag" onChange={handleChange}>
```

## stopPropagation: Use onMouseDown, NOT onClick

```tsx
{/* ❌ Blocks all child click events */}
<div onClick={(e) => e.stopPropagation()}>

{/* ✅ Only blocks drag, doesn't affect click */}
<div onMouseDown={(e) => e.stopPropagation()}>
```

## snapToGrid: Default Off

Default-on causes "laggy" feel. Make it opt-in with a toggle button.

## Node Selection Highlight (Gray Tones)

```typescript
const CATEGORY_COLORS: Record<NodeCategory, string> = {
  INPUT: "#6b7280",      // deep gray
  GENERATION: "#9ca3af",  // medium gray
  COMPOSITE: "#d1d5db",   // light gray
};
```

Must override RF default purple glow in globals.css:
```css
.react-flow__node.selected { box-shadow: none !important; }
```

## Canvas Pan/Zoom Optimization

```tsx
<ReactFlow
  panOnDrag={true} panOnScroll={true} panOnScrollSpeed={1}
  panOnScrollMode={PanOnScrollMode.Free}
  zoomOnScroll={true} zoomOnPinch={true} zoomOnDoubleClick={false}
  autoPanOnNodeDrag={true} autoPanOnConnect={true}
/>
```

## Control Panel Visibility Pattern

Use `selectedNodeId === props.id`, NOT global `showControlPanel` boolean (which shows all panels simultaneously).

## When Page Gets Stuck

1. Don't debug one-by-one — git revert all optimization code
2. Confirm page recovers
3. Re-add optimizations one at a time, testing each

```bash
cd ~/antoken/frontend
git checkout <last-working> -- src/styles/globals.css src/components/canvas/WorkflowCanvas.tsx
rm -rf .next .swc && npm run dev
```
