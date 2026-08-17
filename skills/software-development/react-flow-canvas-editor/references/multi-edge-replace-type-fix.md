# ReactFlow Multi-Edge: replace type discovery (2026-06-16)

## Problem
After implementing the standard multi-edge fix (ConnectionMode.Loose + filter `remove` in onEdgesChange), edges were STILL being lost. Only the last connected edge survived.

## Root Cause
ReactFlow v12 sends TWO types of destructive changes in `onEdgesChange`:
1. `remove` — when a new connection replaces an old one (well-known)
2. `replace` — when ReactFlow detects edges array changes internally (lesser-known)

The `replace` type comes from `@xyflow/system`'s `applyChanges` function (line 596-631 in index.mjs):
```javascript
else if (change.type === 'remove' || change.type === 'replace') {
    changesMap.set(change.id, [change]);
}
// ...
if (changes[0].type === 'replace') {
    updatedElements.push({ ...changes[0].item });
    continue;
}
```

The `replace` change is triggered when ReactFlow's internal lookup detects that the edges array has changed (e.g., when we add a new edge via `onConnect`).

## Solution
Filter `onEdgesChange` to ONLY process `select` type changes:
```typescript
onEdgesChange: (changes) => {
  set((s) => {
    const filtered = changes.filter((c) => c.type === 'select');
    if (filtered.length === 0) return s;
    const updated = applyEdgeChanges(filtered, s.edges);
    ...
  });
},
```

## Debugging
If edges are still lost after filtering `remove`, check the browser console for `trigger edge changes` debug output. Look for `replace` type changes in the array.

## Key Insight
Filtering just `remove` is NOT enough. The `replace` type is equally destructive and often overlooked because it's less documented.
