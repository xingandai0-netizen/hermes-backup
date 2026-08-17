# Testing React Flow Connections via Browser Console

## Problem
When testing a React Flow canvas editor, you need to verify that drag-to-connect works. But browser tools can't directly simulate React Flow's internal drag events.

## Solution: Simulate mousedown/mousemove/mouseup on handles

### Step 1: Find all handles
```javascript
const allH = document.querySelectorAll('.react-flow__handle');
const handleData = Array.from(allH).map((h, i) => ({
  index: i,
  handleId: h.getAttribute('data-handleid'),
  handlePos: h.getAttribute('data-handlepos'),
  nodeId: h.closest('.react-flow__node')?.getAttribute('data-id'),
  isSource: h.classList.contains('source'),
  rect: {
    x: Math.round(h.getBoundingClientRect().x + h.getBoundingClientRect().width/2),
    y: Math.round(h.getBoundingClientRect().y + h.getBoundingClientRect().height/2),
  }
}));
JSON.stringify(handleData, null, 2);
```

### Step 2: Simulate drag connection
```javascript
// Connect handle[2] (source) to handle[5] (target)
const allH = document.querySelectorAll('.react-flow__handle');
const src = allH[2];
const tgt = allH[5];

const s = src.getBoundingClientRect();
const t = tgt.getBoundingClientRect();

src.dispatchEvent(new MouseEvent('mousedown', {
  bubbles: true, cancelable: true, view: window,
  clientX: s.x + s.width/2, clientY: s.y + s.height/2, button: 0
}));

document.dispatchEvent(new MouseEvent('mousemove', {
  bubbles: true, cancelable: true, view: window,
  clientX: t.x + t.width/2, clientY: t.y + t.height/2, button: 0
}));

tgt.dispatchEvent(new MouseEvent('mouseup', {
  bubbles: true, cancelable: true, view: window,
  clientX: t.x + t.width/2, clientY: t.y + t.height/2, button: 0
}));
```

### Step 3: Verify
```javascript
const edgeCount = document.querySelectorAll('.react-flow__edge').length;
// Should be > 0 if connection succeeded
```

## Pitfalls
- Handle query selectors with `[data-nodeid="..."]` may not work — use index-based approach instead
- `mousedown` must be on the source handle, `mouseup` on the target handle
- `mousemove` must be on `document`, not on the target
- Variable names must be unique across console evaluations (browser remembers previous declarations)
- Connection validation may reject the connection silently — check `console.warn` output
