# Viewport-Based Node Positioning

## Problem
New nodes appear at fixed position (300, 150) instead of current viewport center.

## Solution
Track viewport state in Zustand store and use it to calculate center position.

### 1. Add Viewport State to Store
```typescript
interface ViewportPosition {
  x: number;
  y: number;
  zoom: number;
}

interface WorkflowState {
  // ... existing state
  viewport: ViewportPosition;
  updateViewport: (viewport: ViewportPosition) => void;
}

// Initial state
viewport: { x: 0, y: 0, zoom: 1 },

// Action
updateViewport: (viewport) => {
  set({ viewport });
},
```

### 2. Track Viewport Changes in Canvas
```tsx
const { updateViewport } = useWorkflowStore();

const onMove = useCallback((_: any, viewport: { x: number; y: number; zoom: number }) => {
  updateViewport(viewport);
}, [updateViewport]);

<ReactFlow
  onMove={onMove}
  // ... other props
/>
```

### 3. Calculate Center Position
```tsx
const { viewport } = useWorkflowStore();

const handleAddNode = useCallback(() => {
  const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
  const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
  
  const newNode = {
    // ...
    position: { x: centerX - 140, y: centerY - 100 },
  };
}, [viewport]);
```

## Formula Explanation
- `viewport.x/y` - Canvas offset (negative when panned right/down)
- `window.innerWidth/2` - Screen center
- `/viewport.zoom` - Adjust for zoom level
- `-140/-100` - Offset to center node (half of node width/height)

## Pitfalls
1. **Node width assumption** - Assumes 280px node width, offset by 140
2. **Node height assumption** - Assumes ~200px height, offset by 100
3. **Zoom affects position** - Must divide by zoom to get canvas coordinates
4. **Initial viewport** - Must set initial viewport in store before first render
