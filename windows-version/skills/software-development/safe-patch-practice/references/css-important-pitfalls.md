# CSS !important Pitfalls (2026-06-14)

## Problem: !important Breaks Layout

Adding CSS with `!important` for React Flow overrides can break Tailwind utility classes and cause layout issues.

**Example that caused page freeze:**
```css
.react-flow {
  width: 100% !important;
  height: 100% !important;
}

.react-flow__renderer {
  width: 100% !important;
  height: 100% !important;
}

.flex-1 {
  flex: 1 1 0%;
  min-height: 0;
}

.h-screen {
  height: 100vh;
  height: 100dvh;
}
```

**Why it failed:** The `!important` declarations conflicted with Tailwind's utility classes and ReactFlow's internal styling, causing the entire page layout to break.

## Solution

1. **Use ReactFlow's style prop** instead of CSS overrides:
```typescript
<ReactFlow style={{ width: '100%', height: '100%' }} />
```

2. **Ensure parent containers have proper dimensions:**
```tsx
<div className="flex flex-col flex-1 min-w-0" style={{ minHeight: 0 }}>
  <WorkflowCanvas />
</div>
```

3. **Never use !important for ReactFlow styling** — it causes more problems than it solves.

## Layout Structure

```tsx
// Correct layout structure
<div className="flex h-screen overflow-hidden">
  <Sidebar /> {/* width: 60px */}
  <div className="flex flex-col flex-1 min-w-0">
    <TopBar className="h-11 flex-shrink-0" />
    <div className="flex-1 min-h-0"> {/* This wrapper is crucial */}
      <WorkflowCanvas />
    </div>
  </div>
</div>
```

**Key:** The `min-h-0` on the canvas wrapper is essential for flex children to scroll properly.
