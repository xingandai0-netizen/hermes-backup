# ReactFlow 双击事件拦截问题

## 问题描述

ReactFlow 的 `onNodeDoubleClick` handler 会拦截所有双击事件，导致节点内部的 VideoPreview 组件的 `onDoubleClick` 回调不会被触发。

## 症状

- 用户双击视频预览区时，ReactFlow 执行节点扩大操作
- VideoPreview 的 `onDoubleClick` 回调不会被调用
- PreviewModal 对话框不会打开

## 根因

ReactFlow 内部有双击事件处理机制，会优先处理 `onNodeDoubleClick` prop。即使传空函数 `() => {}`，也不能完全阻止拦截。

## 解决方案

### 方案1：移除 onNodeDoubleClick（推荐）

直接从 WorkflowCanvas.tsx 中移除 `onNodeDoubleClick` handler 和 ReactFlow 组件上的 `onNodeDoubleClick` 属性：

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

### 方案2：放弃双击，改用单击 + 按钮（最终采用）

由于双击行为不可靠，最终采用：
- 单击视频区域 → 显示控制面板（对话交流框）
- 点击放大按钮 → 打开 PreviewModal

## 测试过的方案

1. ✅ `onNodeDoubleClick={selectNode}` → 拦截双击，节点扩大
2. ❌ `onNodeDoubleClick={() => {}}` → 仍然拦截！双击不冒泡
3. ❌ 移除 `onNodeDoubleClick` prop + 保留 handler → 无效果
4. ❌ 在节点内部用 `onDoubleClick` → 被 ReactFlow 拦截
5. ✅ 完全移除 `onNodeDoubleClick` prop 和 handler → 双击冒泡到节点
6. ✅ **最终方案：放弃双击，用单击 + 放大按钮**

## 教训

1. ReactFlow 的事件处理机制会拦截某些事件（如双击）
2. 不要依赖双击作为主要交互方式
3. 使用单击 + 按钮的组合更可靠
