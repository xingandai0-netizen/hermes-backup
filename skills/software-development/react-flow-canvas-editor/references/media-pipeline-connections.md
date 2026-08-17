# Media Pipeline Connection Rules (Antoken v0.2)

## 连接逻辑（2026-06-14更新）

**关键规则：无类型限制，允许所有连接（和TapNow一致）**

用户明确要求："连接限制我需要和tapnow一样没有类型限制"

```typescript
// onConnect实现 - 只禁止自连接
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  // 直接添加边，不做类型验证
  addEdge({ ...connection, style: { stroke: "#ffffff" } }, edges);
}
```

**不要添加isValidConnection验证逻辑** - 即使有validation.ts中的TYPE_COMPAT矩阵，也不要调用它。

## 节点assetType设置（重要）

生成结果时必须设置assetType，否则下游节点无法正确识别素材类型：

```typescript
// VideoNode updateResult
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO" as const,  // 必须设置
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});

// ImageNode updateResult
updateNodeData(props.id, {
  status: "success",
  assetType: "IMAGE" as const,  // 必须设置
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});
```

## 上游素材读取模式

```typescript
const getUpstreamAssets = useCallback(() => {
  const incomingEdges = edges.filter((e) => e.target === props.id);
  const assets: { image?: { url: string; assetId: string }; video?: { url: string; assetId: string } } = {};

  for (const edge of incomingEdges) {
    const sourceNode = nodes.find((n) => n.id === edge.source);
    if (sourceNode) {
      const nodeData = sourceNode.data as unknown as NodeData;
      const url = nodeData.assetUrl || (nodeData.config as any)?.assetUrl;
      const assetId = nodeData.assetId || (nodeData.config as any)?.assetId;

      if (url) {
        const assetType = nodeData.assetType || (url.match(/\.(mp4|mov|avi)$/i) ? "VIDEO" : "IMAGE");
        if (assetType === "IMAGE") {
          assets.image = { url, assetId: assetId || "" };
        } else if (assetType === "VIDEO") {
          assets.video = { url, assetId: assetId || "" };
        }
      }
    }
  }

  return assets;
}, [edges, nodes, props.id]);
```

## API参数传递

```typescript
// 传递上游素材给API
const resp = await fetch("http://localhost:8000/api/generate/video", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt,
    api_url: videoApi.apiUrl,
    api_key: videoApi.apiKey,
    model,
    resolution: size,
    reference_image_url: upstream.image?.url || undefined,  // 图片参考
    reference_video_url: upstream.video?.url || undefined,  // 视频参考
    duration,
  }),
});
```

## 边颜色设置

边颜色必须同时修改CSS和内联样式：

```css
/* globals.css */
.react-flow__edge-path {
  stroke: #ffffff !important;
  stroke-width: 2 !important;
}
```

```typescript
// workflowStore.ts onConnect
style: { stroke: "#ffffff", strokeWidth: 2 }
```
