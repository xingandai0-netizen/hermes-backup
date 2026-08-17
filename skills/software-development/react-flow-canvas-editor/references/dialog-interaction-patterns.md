# Dialog Interaction Patterns (2026-06-29)

## Problem: Pane Click Closes Dialog

When user clicks inside dialog and releases outside, React Flow's `onPaneClick` fires and closes the dialog.

### Solution: `data-dialog` Attribute + Mousedown Target Tracking

```tsx
// 1. Mark dialog with data attribute
<div data-dialog="true" style={{...}}>
  {/* dialog content */}
</div>

// 2. Track mousedown target globally
const mouseDownTarget = useRef<EventTarget | null>(null);

useEffect(() => {
  const handleMouseDown = (e: MouseEvent) => {
    mouseDownTarget.current = e.target;
  };
  document.addEventListener('mousedown', handleMouseDown);
  return () => document.removeEventListener('mousedown', handleMouseDown);
}, []);

// 3. Check mousedown target in pane click handler
const handlePaneClick = useCallback(() => {
  if (mouseDownTarget.current) {
    const target = mouseDownTarget.current as HTMLElement;
    const dialog = target.closest('[data-dialog="true"]');
    if (dialog) {
      mouseDownTarget.current = null;
      return; // Don't close - mousedown was inside dialog
    }
  }
  mouseDownTarget.current = null;
  selectNode(null);
  setContextMenu(null);
  setShowControlPanel(false);
}, [selectNode, setShowControlPanel]);
```

**Why this works**: React Flow's `onPaneClick` fires on mouseup. By tracking where mousedown happened, we can determine if the "click" started inside the dialog.

---

## Problem: Mouse Wheel Scrolls Canvas Instead of Textarea

When hovering over textarea inside dialog, mouse wheel should scroll the textarea content, not pan/zoom the canvas.

### Solution: `addEventListener` with `preventDefault` + MutationObserver

```tsx
// 1. On textarea: add wheel listener that prevents default
<textarea
  ref={(el) => {
    if (el) {
      el.addEventListener('wheel', (e) => {
        e.preventDefault();
        el.scrollTop += e.deltaY;
      }, { passive: false });
    }
  }}
/>

// 2. On dialog: track hover state via DOM attribute
<div
  onMouseEnter={() => document.body.setAttribute('data-hover-dialog', 'true')}
  onMouseLeave={() => document.body.removeAttribute('data-hover-dialog')}
>

// 3. In WorkflowCanvas: observe attribute changes
const [hoveringDialog, setHoveringDialog] = useState(false);

useEffect(() => {
  const observer = new MutationObserver(() => {
    setHoveringDialog(document.body.getAttribute('data-hover-dialog') === 'true');
  });
  observer.observe(document.body, { attributes: true, attributeFilter: ['data-hover-dialog'] });
  return () => observer.disconnect();
}, []);

// 4. Conditionally disable canvas scroll
<ReactFlow
  panOnScroll={!hoveringDialog}
  zoomOnScroll={!hoveringDialog}
/>
```

**Key**: `{ passive: false }` is required for `preventDefault()` to work on wheel events. React's `onWheel` can't do this because React event handlers are passive by default.

---

## Problem: `overflow: hidden` Clips Control Panel

BaseNode's node card has `overflow: "hidden"` which clips the control panel positioned below (`top: "100%"`).

### Fix: Remove `overflow: "hidden"` from node card

```tsx
// ❌ Wrong: clips control panel
<div style={{ ..., overflow: "hidden" }}>

// ✅ Correct: control panel visible
<div style={{ ..., /* no overflow */ }}>
```

---

## Problem: Double-Click Doesn't Show Dialog

Single click selects node but doesn't show dialog. Need explicit `onNodeDoubleClick` handler.

### Fix

```tsx
const onNodeDoubleClick = useCallback((_: any, node: any) => {
  selectNodeQuietly(node.id);
  setShowControlPanel(true);
}, [selectNodeQuietly, setShowControlPanel]);

<ReactFlow onNodeDoubleClick={onNodeDoubleClick} ... />
```

---

## Node Right-Click Context Menu (Download + Delete)

```tsx
// Handler - only show menu if node has content
const onNodeContextMenu = useCallback((e: React.MouseEvent, node: any) => {
  e.preventDefault();
  const nodeData = node.data as NodeData;
  const config = nodeData.config as Record<string, unknown> | undefined;
  const url = (config?.assetUrl || config?.resultUrl || nodeData.assetUrl) as string | undefined;
  if (url) {
    setContextMenu({ x: e.clientX, y: e.clientY, type: 'node', nodeId: node.id });
  }
}, []);

// Menu with download + delete
{contextMenu.type === 'node' && (
  <>
    <button onClick={handleDownloadAsset}>下载素材</button>
    <button onClick={() => {
      if (contextMenu.nodeId) removeNode(contextMenu.nodeId);
      setContextMenu(null);
    }} style={{ color: '#ff453a' }}>删除素材</button>
  </>
)}
```
