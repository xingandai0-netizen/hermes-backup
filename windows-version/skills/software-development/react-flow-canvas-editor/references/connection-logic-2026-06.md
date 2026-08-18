# Connection Logic & assetType Pattern (2026-06-14)

## 关键规则：无类型限制

用户明确要求："连接限制我需要和tapnow一样没有类型限制"

**不要添加isValidConnection验证**，只禁止自连接：

```typescript
// workflowStore.ts onConnect
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  addEdge({ ...connection, style: { stroke: "#ffffff" } }, edges);
}
```

## assetType必须设置

节点生成结果时必须设置assetType，否则下游节点无法识别素材类型：

```typescript
// VideoNode updateResult
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO" as const,
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});

// ImageNode updateResult  
updateNodeData(props.id, {
  status: "success",
  assetType: "IMAGE" as const,
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});
```

## 边颜色

边颜色必须同时修改CSS和内联样式：

```css
/* globals.css */
.react-flow__edge-path {
  stroke: #ffffff !important;
}
```

```typescript
// workflowStore.ts
style: { stroke: "#ffffff", strokeWidth: 2 }
```
