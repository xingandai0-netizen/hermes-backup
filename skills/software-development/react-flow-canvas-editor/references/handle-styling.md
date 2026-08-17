# Handle Styling Patterns

## Connection Point Design

### Recommended Style (v0.5)
```tsx
const handleStyle = {
  width: 16,
  height: 16,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 14px ${categoryColor}, 0 0 6px ${categoryColor}80, 0 0 3px ${categoryColor}60`
    : `0 0 10px ${categoryColor}70, 0 0 4px ${categoryColor}50`,
  transition: "all 0.2s ease",
};
```

### Position Outside Node
```tsx
<Handle
  type="target"
  position={Position.Left}
  id="input"
  style={{
    ...handleStyle,
    left: -10,  // Outside node boundary
    zIndex: 20,
  }}
/>

<Handle
  type="source"
  position={Position.Right}
  id="output"
  style={{
    ...handleStyle,
    right: -10,  // Outside node boundary
    zIndex: 20,
  }}
/>
```

## Glow Effect Layers

### 3-Layer Glow (Hover)
- Layer 1: `0 0 14px` - Outer glow
- Layer 2: `0 0 6px 80` - Middle glow
- Layer 3: `0 0 3px 60` - Inner glow

### 2-Layer Glow (Default)
- Layer 1: `0 0 10px 70` - Outer glow
- Layer 2: `0 0 4px 50` - Inner glow

## Selection State
- When node is selected, handle color matches categoryColor
- Border: `2px solid #0a0a0f` (dark background)
- Glow intensity increases on hover
