# ReactFlow Performance Optimization Patterns (2026-06-27)

## 1. Edge Highlighting: O(n²) → O(n)

**Problem**: Recursive `getDownstreamNodes` called per-edge per-render.

**Solution**: `useMemo` + BFS precomputation:

```typescript
const highlightedEdgeIds = useMemo(() => {
  if (!selectedNodeId) return new Set<string>();
  const ids = new Set<string>();
  const downstream = new Set<string>();
  const queue = [selectedNodeId];
  while (queue.length > 0) {
    const nid = queue.shift()!;
    for (const e of edges) {
      if (e.source === nid && !downstream.has(e.target)) {
        downstream.add(e.target);
        queue.push(e.target);
      }
    }
  }
  for (const e of edges) {
    if (e.source === selectedNodeId || e.target === selectedNodeId ||
        downstream.has(e.source) || downstream.has(e.target)) {
      ids.add(e.id);
    }
  }
  return ids;
}, [selectedNodeId, edges]);
```

## 2. Viewport onMove Throttling

**Problem**: `onMove` fires on every pixel, updating store triggers full re-render.

**Solution**: `requestAnimationFrame` throttle:

```typescript
const moveTimerRef = useRef<number | null>(null);

const onMove = useCallback((_: any, vp: { x: number; y: number; zoom: number }) => {
  if (moveTimerRef.current) return;
  moveTimerRef.current = requestAnimationFrame(() => {
    updateViewport(vp);
    moveTimerRef.current = null;
  });
}, [updateViewport]);
```

## 3. Remove viewport Dependency from Node Components

**Problem**: If nodes read `viewport` from store (e.g., for control panel scaling), every zoom/pan re-renders ALL nodes.

**Solution**: 
- Don't destructure `viewport` in VideoNode/ImageNode
- Don't compute `controlScale` from store viewport
- If scaling needed, use CSS or a non-reactive mechanism

## 4. Inline Object/Function Creation

**Problem**: Creating objects/functions in JSX render path causes child re-renders.

**Solution**: Use `useMemo`/`useCallback` for:
- Style objects passed to child components
- Event handlers passed as props
- Computed values used in render

## 5. Edge Mapping Optimization

**Problem**: `edges.map(edge => ({ ...edge, style: ... }))` creates new array every render.

**Solution**: Combine with `useMemo`:

```typescript
const styledEdges = useMemo(() => 
  edges.map(edge => ({
    ...edge,
    style: {
      ...edge.style,
      stroke: highlightedEdgeIds.has(edge.id) ? "#ffffff" : "rgba(255,255,255,0.2)",
    },
  })),
  [edges, highlightedEdgeIds]
);
```
