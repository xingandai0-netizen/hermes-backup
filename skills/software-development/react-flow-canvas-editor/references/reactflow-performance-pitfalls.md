# ReactFlow Performance Pitfalls (2026-06-14)

## DANGEROUS Options - DO NOT USE without testing

The following ReactFlow options caused the page to freeze or become unresponsive to clicks:

### 1. `onlyRenderVisibleElements={true}`
- **Symptom**: Page freezes, completely unresponsive
- **Cause**: Can cause infinite re-renders with dynamic node sizes
- **Status**: AVOID

### 2. `elevateNodesOnSelect={false}`
- **Symptom**: Click events may not propagate correctly
- **Status**: AVOID - use default (true)

### 3. `deleteKeyCode={null}`
- **Symptom**: May interfere with other keyboard events
- **Status**: AVOID - use default

### 4. React.memo on node components
- **Symptom**: Can cause stale renders when node data changes
- **Status**: TEST CAREFULLY

## CSS Pitfalls

### DO NOT add:
```css
/* DANGEROUS - breaks ReactFlow rendering */
.react-flow {
  width: 100% !important;
  height: 100% !important;
}
```

ReactFlow manages its own dimensions. Overriding with !important causes:
- Canvas not responding to mouse events
- Nodes not rendering correctly
- Edge calculations failing

## Safe Optimizations

```typescript
// Safe - reduces GPU usage
defaultEdgeOptions={{ animated: false }}

// Safe - zoom limits
minZoom={0.2}
maxZoom={3}

// Safe - snap to grid
snapToGrid
snapGrid={[16, 16]}
```

## Testing Protocol

1. Create git branch: `git checkout -b perf-test`
2. Apply ONE change at a time
3. Test: click, drag, connect, pan, zoom
4. If ANY issue: `git checkout main` immediately
5. Never commit broken optimizations to main

## Recovery

```bash
git checkout <last-working-commit> -- frontend/src/components/canvas/WorkflowCanvas.tsx
git checkout <last-working-commit> -- frontend/src/styles/globals.css
git add -A && git commit -m "revert: restore working state" && git push
```

## Key Lesson (2026-06-14)
User said "没性能优化前是正常的" → revert immediately. 
阿戴's tolerance for broken UI is ZERO. A slightly slower page that works > a fast page that's broken.
