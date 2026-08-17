# 连接逻辑 — TapNow风格（无类型限制）

## 设计决策

**2026-06-14 阿戴明确要求：** "连接限制我需要和tapnow一样没有类型限制"

### 实现

```typescript
// stores/workflowStore.ts - onConnect
onConnect: (connection) => {
  // 只禁止自连接，允许所有其他连接（和TapNow一样）
  if (connection.source === connection.target) return;

  get().saveSnapshot();
  set((s) => {
    const updated = addEdge(
      {
        ...connection,
        animated: true,
        style: { stroke: "#ffffff", strokeWidth: 2 },
        type: "smoothstep",
      },
      s.edges
    );
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},
```

### 关键点

1. **不导入isValidConnection** — 不需要类型验证
2. **只检查自连接** — `connection.source === connection.target`
3. **白色连接线** — `stroke: "#ffffff"`
4. **smoothstep类型** — 平滑折线

### 与TapNow一致

TapNow的设计理念：用户知道自己的工作流，不需要系统限制连接。
- 任意节点可以连接到任意节点
- 类型不匹配在执行时处理，不在连接时阻止
- 用户可以自由探索不同的工作流组合

## 边颜色配置

所有边颜色必须统一为白色 `#ffffff`：

```typescript
// workflowStore.ts - onConnect
style: { stroke: "#ffffff", strokeWidth: 2 }

// WorkflowCanvas.tsx - defaultEdgeOptions
style: { stroke: "#ffffff", strokeWidth: 2 }

// WorkflowCanvas.tsx - connectionLineStyle
connectionLineStyle={{ stroke: "#ffffff", strokeWidth: 3, strokeDasharray: "8 4" }}

// globals.css
.react-flow__edge-path {
  stroke: #ffffff !important;
  stroke-width: 2 !important;
}
```

**注意：** CSS中的 `!important` 会覆盖内联样式。必须同时修改CSS和内联样式。
