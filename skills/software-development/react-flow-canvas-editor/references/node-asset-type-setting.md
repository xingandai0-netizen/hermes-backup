# 节点AssetType设置 — 连接系统基础

## 问题

节点生成结果时必须设置 `assetType`，否则：
1. 连接验证无法判断节点输出类型
2. 下游节点无法正确读取上游素材
3. 合成节点不知道输入是图片还是视频

## 正确实现

### 所有节点的updateResult必须设置assetType

```typescript
// VideoNode.tsx
const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  updateNodeData(props.id, {
    status: "success",
    assetType: "VIDEO" as const,  // ← 必须设置
    assetUrl: url,
    assetId,
    config: { ...cfg, assetUrl: url, assetId },
  });
}, [props.id, cfg, updateNodeData]);

// ImageNode.tsx
const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  setMode("upload");
  updateNodeData(props.id, {
    status: "success",
    assetType: "IMAGE" as const,  // ← 必须设置
    assetUrl: url,
    assetId,
    config: { ...cfg, assetUrl: url, assetId },
  });
}, [props.id, cfg, updateNodeData]);

// CompositeNode.tsx
const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  updateNodeData(props.id, {
    status: "success",
    assetType: "VIDEO" as const,  // ← 合成结果通常是视频
    assetUrl: url,
    assetId,
    config: { ...cfg, assetUrl: url, assetId },
  });
}, [props.id, cfg, updateNodeData]);
```

## AssetType类型定义

```typescript
// types/workflow.ts
export type AssetType = "IMAGE" | "VIDEO" | "TEXT";
```

## 上游素材读取

```typescript
// VideoNode.tsx / CompositeNode.tsx
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
        // 优先使用assetType，其次根据URL判断
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

## 常见错误

### 1. 忘记设置assetType
```typescript
// ❌ 错误 - 没有assetType
updateNodeData(props.id, {
  status: "success",
  config: { ...cfg, assetUrl: url, assetId },
});

// ✅ 正确 - 设置assetType
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO" as const,
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});
```

### 2. 大小写不一致
```typescript
// ❌ 错误 - 小写
sourceConfig?.assetType === 'image'
sourceConfig?.assetType === 'video'

// ✅ 正确 - 大写
sourceConfig?.assetType === 'IMAGE'
sourceConfig?.assetType === 'VIDEO'
```

### 3. 只在config中设置
```typescript
// ❌ 错误 - 只在config中
updateNodeData(props.id, {
  status: "success",
  config: { ...cfg, assetUrl: url, assetId, assetType: "VIDEO" },
});

// ✅ 正确 - 在顶层设置
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO" as const,
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});
```

## 验证检查

```bash
# 检查所有节点是否设置了assetType
grep -n "assetType.*VIDEO\|assetType.*IMAGE" frontend/src/components/nodes/*.tsx

# 检查大小写一致性
grep -rn "assetType.*===.*'" frontend/src/components/nodes/*.tsx
```
