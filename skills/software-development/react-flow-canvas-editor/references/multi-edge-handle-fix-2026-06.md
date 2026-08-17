# Multi-Edge Handle Patterns

## Problem
ReactFlow v12 (ConnectionMode.Strict) silently replaces edges when multiple sources connect to the same target handle. Only the last connection survives.

## Root Cause
ReactFlow fires events in this order:
1. `onEdgesChange` with `type: "remove"` for the old edge
2. `onConnect` with the new connection

Without intercepting step 1, old edges are lost.

## Complete Fix (3 parts needed)

### Part 1: ConnectionMode.Loose
```tsx
import { ConnectionMode } from "@xyflow/react";

<ReactFlow
  connectionMode={ConnectionMode.Loose}
  // ... other props
>
```

### Part 2: Intercept edge removal in onEdgesChange
```tsx
// In workflowStore.ts
onEdgesChange: (changes) => {
  set((s) => {
    // Filter out automatic removals from ReactFlow
    const filteredChanges = changes.filter((c) => c.type !== 'remove');
    const updated = applyEdgeChanges(filteredChanges, s.edges);
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},
```

### Part 3: Independent removeEdge function
```tsx
// In workflowStore.ts - add to interface and implementation
removeEdge: (edgeId: string) => void;

removeEdge: (edgeId) => {
  get().saveSnapshot();
  set((s) => {
    const edges = s.edges.filter((e) => e.id !== edgeId);
    saveToStorage({ nodes: s.nodes, edges, workflowName: s.workflowName });
    return { edges };
  });
},
```

### Part 4: Use removeEdge for user-initiated deletion
```tsx
// In WorkflowCanvas.tsx - context menu handler
const handleDeleteEdge = useCallback(() => {
  if (contextMenu?.edgeId) {
    removeEdge(contextMenu.edgeId);  // NOT onEdgesChange([{type: "remove"}])
    setContextMenu(null);
  }
}, [contextMenu, removeEdge]);
```

### Part 5: Check duplicates in onConnect
```tsx
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  
  // Prevent duplicate connections
  const exists = get().edges.some(
    (e) => e.source === connection.source && 
           e.target === connection.target &&
           e.sourceHandle === (connection.sourceHandle || 'output') && 
           e.targetHandle === (connection.targetHandle || 'input')
  );
  if (exists) return;

  get().saveSnapshot();
  set((s) => {
    const edgeId = `edge-${connection.source}-${connection.sourceHandle || 'output'}-${connection.target}-${connection.targetHandle || 'input'}-${Date.now()}`;
    const newEdge = {
      id: edgeId,
      ...connection,
      animated: true,
      style: { stroke: "#ffffff", strokeWidth: 2 },
      type: "smoothstep",
    };
    const updated = [...s.edges, newEdge];
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},
```

## Verification
1. Create 3 source nodes + 1 target node
2. Connect all 3 sources to the same target handle
3. Check edges array has 3 edges (not 1)
4. Right-click delete edge still works
5. Node deletion still removes associated edges

## Common Mistakes
- Only adding ConnectionMode.Loose without intercepting onEdgesChange → still loses edges
- Using addEdge() which may deduplicate → use [...s.edges, newEdge]
- Not checking duplicates → same connection added multiple times
- Filtering ALL remove actions → need separate removeEdge for user deletion
