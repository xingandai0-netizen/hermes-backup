# Event Handling & Node Selection Pitfalls

## stopPropagation Prevents Node Selection

**Problem:** Using `e.stopPropagation()` on node content prevents ReactFlow from selecting the node, making delete key impossible to trigger.

```tsx
// BAD - prevents node selection
<div onClick={(e) => { e.stopPropagation(); setShowControls(true); }}>

// GOOD - allows node selection
<div onClick={() => setShowControls(true)}>
```

**Rule:** Only use `stopPropagation` on interactive elements inside nodes (buttons, inputs, sliders) that need to handle their own clicks without triggering node drag/selection.

## Multi-Select Behavior

ReactFlow supports multi-select by default (Ctrl/Cmd + click). If users report "two nodes selected at once", they may be holding modifier keys.

## Delete Key Not Working

Common causes:
1. Focus is on an INPUT/TEXTAREA element inside the node
2. `stopPropagation` prevented node selection
3. `selectedNodeId` is null in workflowStore

Fix: Allow delete even when input is focused IF the input is empty:
```typescript
if (isInputFocused) {
  const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
  if (inputValue && inputValue.length > 0) return; // Don't delete if typing
}
```

## Handle Positioning & Hover Zones

### Extended Hover Area with Padding
To make handles easier to click, extend the hover zone beyond the node boundary:

```tsx
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  style={{
    position: "relative",
    width: 280,
    padding: 40,      // Extend hover zone
    margin: -40,       // Compensate layout
    boxSizing: "content-box",
  }}
>
```

### Handle Visual Feedback
Handles should have glow effects and scale on hover:

```tsx
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${categoryColor}, 0 0 10px ${categoryColor}80`
    : `0 0 10px ${categoryColor}70`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
  opacity: isHovered ? 1 : 0,
};
```

### Handle Position Outside Node
Position handles outside the node boundary:

```tsx
<Handle
  type="target"
  position={Position.Left}
  id="input"
  style={{
    ...handleStyle,
    left: -28,  // Outside the node
    zIndex: 20,
    transformOrigin: "right center",  // Scale outward
  }}
/>
```

## Viewport-Aware Node Placement

Store viewport position in Zustand to place new nodes at the center of the current view:

```typescript
// In workflowStore
interface ViewportPosition { x: number; y: number; zoom: number; }

// Track viewport changes
const onMove = useCallback((_: any, viewport: ViewportPosition) => {
  updateViewport(viewport);
}, [updateViewport]);

// Calculate center position when creating nodes
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
```

## Asset Naming System

Generate unique names for nodes based on type and count:

```typescript
const getAssetName = (nodeType: string): string => {
  const type = nodeType.toUpperCase();
  const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
  if (type === "IMAGE") {
    const existingNumbers = existingNames
      .filter(n => n.startsWith('图素材'))
      .map(n => parseInt(n.replace('图素材', '')) || 0);
    const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
    return `图素材${maxNum + 1}`;
  }
  // ... similar for VIDEO
};
```

**Pitfall:** Using simple `count + 1` causes duplicates after deletion. Use `max(existing) + 1` instead.
