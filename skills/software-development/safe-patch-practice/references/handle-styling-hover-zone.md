# Handle Styling and Hover Zone Pattern (2026-06-15)

## Handle Positioning Outside Node

**Goal:** Connection handles should be outside the node, not overlapping content.

**Pattern:** Use `margin: -N` + `padding: N` to create invisible hover zone.

```tsx
const HOVER_ZONE = 40;

<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  style={{
    position: "relative",
    width: 280,
    padding: HOVER_ZONE,    // 扩展 hover 检测范围
    margin: -HOVER_ZONE,    // 补偿布局偏移，不影响 ReactFlow 定位
  }}
>
  {/* Node content - 保持不变 */}
  <div style={{ width: 280, ... }}>
    {children}
  </div>

  {/* Handles positioned in padding area */}
  <Handle
    type="target"
    position={Position.Left}
    style={{
      width: 20,
      height: 20,
      left: HOVER_ZONE - 28,  // 40px padding - 28px offset = 12px
      opacity: isHovered ? 1 : 0,
      transform: isHovered ? "scale(1.5)" : "scale(1)",
      transformOrigin: "right center",  // 向左扩展
      transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
    }}
  />
  <Handle
    type="source"
    position={Position.Right}
    style={{
      width: 20,
      height: 20,
      right: HOVER_ZONE - 28,
      opacity: isHovered ? 1 : 0,
      transform: isHovered ? "scale(1.5)" : "scale(1)",
      transformOrigin: "left center",  // 向右扩展
      transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
    }}
  />
</div>
```

## Handle Size and Distance

**Final configuration (user-approved):**
- Size: 20×20px (14 too small, 16 barely ok, 20 perfect)
- Distance: -20px from node edge (-7 too close, -14 still touching, -20 just right)
- Hover scale: 1.5× with elastic curve
- Glow: 3-layer box-shadow

```tsx
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${color}, 0 0 10px ${color}80, 0 0 5px ${color}60`
    : `0 0 10px ${color}70, 0 0 4px ${color}50`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
};
```

## Handle Delayed Hiding

**Problem:** When user is connecting lines, mouse leaves the node area and handles disappear immediately.

**Solution:** Delay hiding by 10 seconds after mouse leaves.

```tsx
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) {
    clearTimeout(hideTimerRef.current);
    hideTimerRef.current = null;
  }
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => {
    setIsHovered(false);
  }, 10000); // 10 seconds delay
}, []);
```

## Hover Zone Technique Explained

**Why `margin: -40` + `padding: 40` works:**

1. `padding: 40` extends the element's box model, making the hover detection area larger
2. `margin: -40` compensates for the padding, so the element doesn't shift in the layout
3. ReactFlow positions nodes using `transform: translate(x, y)`, so negative margin doesn't affect positioning
4. The handles are positioned within the padding area, appearing outside the node content

**Alternative (doesn't work):** Using an absolutely positioned transparent div for hover detection has z-index issues - the div blocks hover events on the node content.
