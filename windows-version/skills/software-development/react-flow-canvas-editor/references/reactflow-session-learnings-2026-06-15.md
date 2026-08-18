# React Flow Session Learnings (2026-06-15)

## stopPropagation Prevents Node Selection

**Symptom:** Clicking node content doesn't select node, Delete key doesn't work.

**Root Cause:** `e.stopPropagation()` on inner elements prevents click bubbling to ReactFlow's node selection handler.

**Fix:**
```typescript
// ❌ BAD - prevents node selection
<div onClick={(e) => { e.stopPropagation(); setShowControls(true); }}>

// ✅ GOOD - node gets selected, controls still show
<div onClick={() => setShowControls(true)}>
```

**Exception:** Control panel inner elements (buttons, inputs) SHOULD stopPropagation to prevent triggering node drag:
```typescript
<div onMouseDown={(e) => e.stopPropagation()}>  // Control panel
```

## Handle Styling with Hover Zone

**Pattern:** `margin: -40` + `padding: 40` creates invisible hover zone without affecting layout.

```typescript
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  style={{ position: "relative", width: 280, padding: 40, margin: -40 }}
>
  {/* Node content */}
  <div style={{ width: 280, ... }}>
    {children}
  </div>
  
  {/* Handles positioned in padding area */}
  <Handle
    type="target"
    position={Position.Left}
    style={{
      width: 20, height: 20,
      left: 12,  // 40px padding - 28px offset
      opacity: isHovered ? 1 : 0,
      transform: isHovered ? "scale(1.5)" : "scale(1)",
      transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
    }}
  />
</div>
```

## Asset Naming with localStorage Counter

**Problem:** Module-level counters reset on page refresh. Using `nodes.length` causes duplicates after deletion.

**Solution:** Use localStorage for persistent numbering:

```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

## Color Replacement: Use patch, Not read_file+write_file

**Problem:** Using `read_file` + `write_file` for bulk color replacement corrupts files (embeds line numbers).

**Solution:** Always use `patch` tool for find-and-replace operations:

```python
# ❌ BAD - corrupts files
content = read_file(path)["content"]
content = content.replace(old, new)
write_file(path, content)

# ✅ GOOD - safe replacement
patch(path=path, old_string=old, new_string=new)
```

## Video Preview Component Patterns

### Hover-to-Play (TapNow Style)
```typescript
useEffect(() => {
  if (!hoverToPlay || !videoRef.current) return;
  if (isHovered) {
    videoRef.current.currentTime = 0;
    videoRef.current.play().catch(() => {});
  } else {
    videoRef.current.pause();
    videoRef.current.currentTime = 0;
  }
}, [isHovered, hoverToPlay]);
```

### Click Behavior
- Single click: Select node (don't stopPropagation)
- Double click: Open full preview dialog
- Hover: Show controls

## @Mention Input Pattern

```typescript
// Detect @ symbol and show menu
const handleInput = (e) => {
  const cursorPos = e.target.selectionStart || 0;
  const textBeforeCursor = value.substring(0, cursorPos);
  const lastAtIndex = textBeforeCursor.lastIndexOf('@');
  
  if (lastAtIndex !== -1) {
    const textAfterAt = textBeforeCursor.substring(lastAtIndex + 1);
    if (!textAfterAt.includes(' ')) {
      setFilterText(textAfterAt);
      setShowMenu(true);
    }
  }
};
```
