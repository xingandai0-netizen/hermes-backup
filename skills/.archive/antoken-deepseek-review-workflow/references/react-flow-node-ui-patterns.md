# React Flow Node UI Modification Patterns (2026-07-04, updated)

## JSX Large Block Replacement Workflow

When replacing large JSX blocks (like `{showControls && (...)}`) in React Flow node components:

```bash
# 1. Find exact line numbers
grep -n "{showControls && (\|{showPreview\|showPreview" file.tsx

# 2. Extract before (everything before the block)
head -N file.tsx > /tmp/before.tsx   # N = block_start_line - 1

# 3. Extract after (everything after the block)
tail -n +M file.tsx > /tmp/after.tsx  # M = the NEXT section's start line

# 4. VERIFY after file is non-empty!
wc -l /tmp/after.tsx
cat /tmp/after.tsx | head -3

# 5. Write new block to temp file, then combine
cat /tmp/before.tsx /tmp/controls.tsx /tmp/after.tsx > file.tsx

# 6. Verify critical content preserved
grep -c "showPreview" file.tsx
npm run build
```

**ALWAYS use `tail -n +行号` NOT `tail -N`**

**ALWAYS verify the after-file is non-empty** — state variable additions shift line numbers.

## Zoom-Adaptive Panel Pattern

```tsx
import { useReactFlow } from "@xyflow/react";
const { getZoom } = useReactFlow();
const currentZoom = getZoom();
style={{ transform: `scale(${1 / currentZoom})`, transformOrigin: "top left" }}
```

## State Variables — Use patch, NOT sed

sed append creates duplicates. Use patch tool with unique old_string/new_string.

## TapNow UI Replication (Verified by Screenshot)

### Buttons — FILLED #2a2a2a, radius 4px, thin border
```tsx
style={{ width: 30, height: 30, background: "#2a2a2a", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 4 }}
```

### Panel — Solid #1c1c1e, attached to preview, compact
```tsx
style={{ width: "100%", background: "#1c1c1e", borderRadius: "0 0 16px 16px", padding: "10px 12px 8px", gap: 6 }}
```

### Top Row — Evenly spaced buttons with gap:6, NO separators

### Model Icon — Three thick lines (strokeWidth 2.5)

### Send — Circular 30px, filled #3a3a3a, arrow only (no number)

### Input — Transparent, minHeight 28, just text

### Bottom — Model name + params text + send button

### Settings Popup — Solid bg, #2a2a2a/#3a3a3a options, 4px radius

## Common Pitfalls
1. tail -6 truncation — use `tail -n +N` AND verify non-empty
2. sed creating duplicates — use patch instead
3. State additions shift line numbers — re-grep after insertion
4. Transparent buttons wrong — TapNow uses filled #2a2a2a
5. Large radius wrong — TapNow uses 4px
