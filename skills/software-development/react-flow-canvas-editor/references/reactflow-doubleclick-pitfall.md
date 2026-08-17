# ReactFlow Double-Click Interception Pitfall

## Problem
ReactFlow's `onNodeDoubleClick` handler intercepts ALL double-click events on nodes. Child components (like VideoPreview) won't receive dblclick events.

## Symptoms
- Double-clicking a video preview area triggers ReactFlow's zoom-to-node behavior
- VideoPreview's `onDoubleClick` callback never fires
- PreviewModal dialog doesn't open

## Root Cause
ReactFlow captures double-click events at the canvas level and processes them before they reach child components. The `onNodeDoubleClick` handler runs, but the event doesn't bubble down to the node's internal elements.

## Solution
Remove or empty the `onNodeDoubleClick` prop from `<ReactFlow>`:

```tsx
// Option 1: Remove entirely
<ReactFlow
  // No onNodeDoubleClick prop
  onPaneClick={handlePaneClick}
/>

// Option 2: Empty function (prevents default zoom-to-node)
<ReactFlow
  onNodeDoubleClick={() => {}}
  onPaneClick={handlePaneClick}
/>
```

## What Does NOT Work
Manual event dispatching is unreliable:
```tsx
// ❌ Does not work - ReactFlow still intercepts
const onNodeDoubleClick = (event, node) => {
  const el = document.querySelector(`[data-id="${node.id}"]`);
  el.dispatchEvent(new MouseEvent('dblclick', { bubbles: true }));
};
```

## VideoPreview Integration
After fixing ReactFlow, VideoPreview's `onDoubleClick` prop works correctly:

```tsx
<VideoPreview
  src={videoUrl}
  hoverToPlay
  onDoubleClick={() => setShowPreview(true)}  // Opens PreviewModal
/>
```

## Related Patterns
- **Hover-to-play**: Mouse enter plays video, leave pauses and resets
- **Single click**: No action (only `stopPropagation`)
- **Double click**: Opens PreviewModal dialog
- **Fullscreen button**: Also opens PreviewModal dialog
