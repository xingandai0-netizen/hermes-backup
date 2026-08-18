# Canvas Pan/Zoom Performance Optimization

## Optimal ReactFlow Props for Smooth Canvas Movement

```tsx
<ReactFlow
  // Pan behavior
  panOnDrag={true}           // Drag to pan (default)
  panOnScroll={true}         // Scroll to pan
  panOnScrollSpeed={1}       // Pan speed multiplier
  panOnScrollMode={"free"}   // Free panning in all directions (use PanOnScrollMode.Free)
  
  // Zoom behavior
  zoomOnScroll={true}        // Scroll to zoom
  zoomOnPinch={true}         // Pinch to zoom (trackpad)
  zoomOnDoubleClick={false}  // Disable double-click zoom (conflicts with node interaction)
  
  // Auto-pan during interactions
  autoPanOnNodeDrag={true}   // Auto-pan when dragging node to edge
  autoPanOnConnect={true}    // Auto-pan when connecting to off-screen handle
  
  // Scroll prevention
  preventScrolling={true}    // Prevent page scroll when over canvas
/>
```

## Required Imports
```tsx
import { PanOnScrollMode } from "@xyflow/react";
// Use PanOnScrollMode.Free, not string "free"
```

## Common Issues
- `panOnScrollMode={"free"}` causes TypeScript error → use `PanOnScrollMode.Free`
- `zoomOnDoubleClick={true}` conflicts with node double-click handlers → set to `false`
