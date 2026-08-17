# Dialog Interaction Patterns (2026-06-29)

## 防误触关闭对话框

### 问题
从对话框内按住鼠标拖到对话框外释放，React Flow 的 paneClick 会关闭对话框。

### 解决方案
全局监听 mousedown，记录按下位置，paneClick 时检查目标是否在对话框内。

### 实现
```typescript
// WorkflowCanvas.tsx
const mouseDownTarget = useRef<EventTarget | null>(null);

useEffect(() => {
  const handleMouseDown = (e: MouseEvent) => {
    mouseDownTarget.current = e.target;
  };
  document.addEventListener('mousedown', handleMouseDown);
  return () => document.removeEventListener('mousedown', handleMouseDown);
}, []);

const handlePaneClick = useCallback(() => {
  if (mouseDownTarget.current) {
    const target = mouseDownTarget.current as HTMLElement;
    const dialog = target.closest('[data-dialog="true"]');
    if (dialog) return;  // 鼠标在对话框内按下，不关闭
  }
  selectNode(null);
  setContextMenu(null);
  setShowControlPanel(false);
}, [selectNode, setShowControlPanel]);
```

对话框容器添加属性：
```tsx
<div data-dialog="true" style={{...}}>
  {/* 对话框内容 */}
</div>
```

## 滚动穿透防护

### 问题
在对话框内的 textarea 滚动鼠标滚轮，会移动/缩放画布。

### 解决方案
三层防护：

1. 对话框容器阻止滚轮事件冒泡
2. ReactFlow 动态禁用滚动
3. textarea 使用 addEventListener (passive: false)

### 实现
```typescript
// 1. 对话框容器
<div onWheel={(e) => e.stopPropagation()}
     onMouseEnter={() => document.body.setAttribute('data-hover-dialog', 'true')}
     onMouseLeave={() => document.body.removeAttribute('data-hover-dialog')}>

// 2. ReactFlow 动态禁用
const [hoveringDialog, setHoveringDialog] = useState(false);
useEffect(() => {
  const observer = new MutationObserver(() => {
    setHoveringDialog(document.body.getAttribute('data-hover-dialog') === 'true');
  });
  observer.observe(document.body, { attributes: true, attributeFilter: ['data-hover-dialog'] });
  return () => observer.disconnect();
}, []);

<ReactFlow panOnScroll={!hoveringDialog} zoomOnScroll={!hoveringDialog} />

// 3. textarea 使用 addEventListener
ref={(el) => {
  if (el) {
    el.addEventListener('wheel', (e) => {
      e.preventDefault();
      el.scrollTop += e.deltaY;
    }, { passive: false });
  }
}}
```

**注意**：React 的 `onWheel` 无法设置 `passive: false`，必须用 `addEventListener`。

## overflow:hidden 裁切问题

### 问题
BaseNode 的节点卡片有 `overflow: "hidden"`，会裁切绝对定位的控制面板。

### 解决方案
移除节点卡片的 `overflow: "hidden"`。

```tsx
// ❌ 错误：裁切控制面板
<div style={{ ..., overflow: "hidden" }}>

// ✅ 正确：控制面板可见
<div style={{ ..., /* 没有 overflow */ }}>
```

## 双击需要 onNodeDoubleClick

### 问题
单击选中节点但不显示对话框，需要显式双击处理器。

### 解决方案
```tsx
// WorkflowCanvas.tsx
const onNodeDoubleClick = useCallback((_: any, node: any) => {
  selectNodeQuietly(node.id);
  setShowControlPanel(true);
}, [selectNodeQuietly, setShowControlPanel]);

<ReactFlow onNodeDoubleClick={onNodeDoubleClick} ... />
```

**注意**：不要在 showControls 条件中加 `showControlPanel`，否则对话框无法显示。
