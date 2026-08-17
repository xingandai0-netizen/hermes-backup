# ReactFlow onNodeDoubleClick 拦截陷阱

## 问题描述

ReactFlow 的 `onNodeDoubleClick` handler 会拦截所有双击事件，导致节点内部组件的 `onDoubleClick` 回调不执行。

## 症状

- 用户双击节点内的预览区域时，ReactFlow 执行节点扩大操作
- VideoPreview 的 `onDoubleClick` 回调不触发
- PreviewModal 对话框不打开

## 根因

ReactFlow 在 `onNodeDoubleClick` 中处理双击事件，不会将事件冒泡到节点内部的子组件。

## 解决方案：移除 onNodeDoubleClick handler

```tsx
// ❌ 错误 - 这会拦截所有双击事件
const onNodeDoubleClick: NodeMouseHandler = useCallback((_, node) => {
  selectNode(node.id);
}, [selectNode]);

<ReactFlow
  onNodeDoubleClick={onNodeDoubleClick}  // 移除这行
/>

// ✅ 正确 - 移除后双击事件会传递到节点内部
<ReactFlow
  // 不设置 onNodeDoubleClick
/>
```

## 为什么移除而不是修改

1. 手动派发事件的方式不可靠（事件可能被 ReactFlow 内部机制再次拦截）
2. 移除后，双击事件会自然冒泡到子组件的 onDoubleClick handler
3. 节点选中功能可以通过单击实现，不需要双击

## 验证

移除后，双击节点内的预览区域会正确触发子组件的 onDoubleClick 回调。

## 应用场景

- 视频预览组件需要双击打开全屏预览对话框
- 图片预览组件需要双击打开大图查看
- 任何需要在节点内部使用双击交互的场景

## 相关文件

- `frontend/src/components/canvas/WorkflowCanvas.tsx` - 移除 onNodeDoubleClick handler 和 ReactFlow 属性
- `frontend/src/components/VideoPreview.tsx` - 添加 onDoubleClick 回调
- `frontend/src/components/nodes/*.tsx` - 传递 onDoubleClick 回调到 VideoPreview

## 记录时间

2026-06-15
