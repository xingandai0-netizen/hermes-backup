# ReactFlow Event Handling Pitfalls

## Problem: ReactFlow Intercepts Node Events

ReactFlow has built-in event handlers that intercept clicks, double-clicks, and other mouse events on nodes. This can break custom click handlers if not handled properly.

## Pitfall 1: onNodeDoubleClick Interception

ReactFlow's `onNodeDoubleClick` callback intercepts double-click events on nodes. Even passing an empty function doesn't fully prevent the interception.

```tsx
// ❌ This doesn't work - ReactFlow still intercepts
<ReactFlow
  onNodeDoubleClick={() => {}}
  ...
/>

// ✅ Solution: Use single-click instead
// Don't rely on double-click for node interactions
```

## Pitfall 2: VideoPreview onClick Stops Propagation

If you add `onClick` to VideoPreview's root div with `e.stopPropagation()`, it prevents the event from bubbling to ReactFlow. This means:
- Node won't be selected
- Property panel won't show
- The click handler runs but doesn't trigger node selection

```tsx
// ❌ This breaks node selection
<div onClick={(e) => { e.stopPropagation(); ... }}>
  <VideoPreview ... />
</div>

// ✅ Let events bubble naturally
<div>
  <VideoPreview ... />
</div>
```

## Pitfall 3: Control Panel Click Handling

When showing a control panel on click, you need to stop propagation to prevent node selection, but only on the click handler that shows the panel.

```tsx
// ✅ Correct approach
<div
  onClick={(e) => { 
    e.stopPropagation(); // Prevent node selection
    setShowControls(true); // Show control panel
  }}
>
  <VideoPreview ... />
</div>
```

## Pitfall 4: Right-Click Upload

For right-click to upload, use `onContextMenu` with `e.preventDefault()` to prevent the browser context menu.

```tsx
// ✅ Right-click to upload
<div
  onContextMenu={(e) => {
    e.preventDefault();
    e.stopPropagation();
    fileInputRef.current?.click();
  }}
>
```

## Best Practices

1. **Don't add onClick to VideoPreview root div** — Let events bubble to ReactFlow for node selection
2. **Use stopPropagation sparingly** — Only on specific UI elements (buttons, progress bar, control panel trigger)
3. **Single-click for control panel** — Don't rely on double-click (ReactFlow intercepts it)
4. **Right-click for upload** — Use `onContextMenu` with `preventDefault()`
5. **Test node selection** — After adding click handlers, verify that clicking the node still selects it and shows the property panel
