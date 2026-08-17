# Control Panel Visibility Pattern

## Problem
When clicking a node's preview area, we want to show the control panel (prompt input, model selector, generate button). But we DON'T want the property panel (right sidebar) to open.

## Solution: selectNodeQuietly + selectedNodeId Check

### 1. Add selectNodeQuietly to workflowStore
```typescript
// Interface
selectNodeQuietly: (nodeId: string | null) => void;

// Implementation
selectNodeQuietly: (nodeId) => {
  set({ selectedNodeId: nodeId });
  // Does NOT set propertyPanelOpen unlike selectNode
},
```

### 2. Use selectedNodeId for visibility
```typescript
// In node component
const { selectedNodeId, selectNodeQuietly, setShowControlPanel } = useWorkflowStore();
const showControls = selectedNodeId === props.id;

// On preview area click
onClick={() => { selectNodeQuietly(props.id); setShowControlPanel(true); }}

// On input/button click - stopPropagation to prevent ReactFlow selection
onMouseDown={(e) => e.stopPropagation()}
```

### 3. Hide on pane click
```typescript
// In WorkflowCanvas
const handlePaneClick = useCallback(() => {
  selectNode(null);  // clears selectedNodeId → all panels hide
  setContextMenu(null);
}, [selectNode]);
```

## Key Points
- `selectNode(id)` sets BOTH `selectedNodeId` AND `propertyPanelOpen` → use for explicit node selection
- `selectNodeQuietly(id)` sets ONLY `selectedNodeId` → use for control panel visibility
- Always check `selectedNodeId === props.id` not a local state
- This ensures only ONE node's control panel is visible at a time
