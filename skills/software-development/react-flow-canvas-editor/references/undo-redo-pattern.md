# React Flow + Zustand Undo/Redo 完整方案 (2026-06-29)

## 问题分析

React Flow 和 Zustand 的状态同步问题：
1. Zustand store 变化 → React 组件重新渲染
2. 但 React Flow 维护自己的内部状态（节点位置、选中状态等）
3. 当 Zustand 恢复旧状态时，React Flow 的内部状态没有同步更新
4. 结果：UI 显示旧的节点位置/状态

## 解决方案

### 1. Store 层

```typescript
interface WorkflowState {
  nodes: Node<NodeData>[];
  edges: Edge[];
  undoStack: Snapshot[];
  redoStack: Snapshot[];
  undoVersion: number;  // 关键：用于强制 React Flow 重新挂载
}

// 初始化
undoVersion: 0,

// undo 函数
undo: () => {
  const { undoStack, nodes, edges } = get();
  if (undoStack.length === 0) return;
  const prev = undoStack[undoStack.length - 1];
  set((s) => ({
    nodes: prev.nodes,
    edges: prev.edges,
    undoStack: s.undoStack.slice(0, -1),
    redoStack: [...s.redoStack, { nodes, edges }],
    undoVersion: s.undoVersion + 1,  // 递增版本号
  }));
  saveToStorage({ nodes: prev.nodes, edges: prev.edges, workflowName: get().workflowName });
},
```

### 2. 原子操作

所有修改节点/边的操作必须在同一个 `set()` 中完成快照保存和操作执行：

```typescript
// ❌ 错误：两个 set() 有竞争条件
removeNode: (nodeId) => {
  get().saveSnapshot();  // 异步 set()
  set(() => { ... });    // 另一个 set()
}

// ✅ 正确：原子操作
removeNode: (nodeId) => {
  set((s) => {
    const snap = { nodes: s.nodes, edges: s.edges };
    const undoStack = [...s.undoStack, snap].slice(-MAX_UNDO_STEPS);
    const nodes = s.nodes.filter(n => n.id !== nodeId);
    const edges = s.edges.filter(e => e.source !== nodeId && e.target !== nodeId);
    return { nodes, edges, undoStack, redoStack: [], undoVersion: s.undoVersion + 1 };
  });
},
```

需要改为原子操作的函数：
- addNode
- removeNode
- removeEdge
- clearWorkflow
- loadWorkflow

### 3. ReactFlow 绑定 key

```tsx
<ReactFlow key={undoVersion} nodes={nodes} edges={edges} ... />
```

当 `undoVersion` 变化时，React Flow 组件会完全重新挂载，使用全新的 nodes/edges 状态。

## 参考

- [React Flow 官方 Undo/Redo 示例](https://reactflow.dev/examples/interaction/undo-redo)
- [日本开发者文章](https://zenn.dev/suwash/articles/react_flow_undo_20251012)
- [Zustand 状态同步问题](https://github.com/pmndrs/zustand/discussions/1653)
