# 节点assetType传播 — 连接验证基础

## 问题
连接验证需要知道源节点和目标节点的类型，但节点生成结果时没有设置assetType，导致验证无法工作。

## 关键发现（2026-06-14）

### 1. 节点必须在updateResult中设置assetType

```tsx
// ❌ 错误 - 没有设置assetType
const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  updateNodeData(props.id, {
    status: "success",
    config: { ...cfg, assetUrl: url, assetId },
  });
}, [props.id, cfg, updateNodeData]);

// ✅ 正确 - 设置assetType
const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  updateNodeData(props.id, {
    status: "success",
    assetType: "VIDEO" as const,  // 或 "IMAGE"
    assetUrl: url,
    assetId,
    config: { ...cfg, assetUrl: url, assetId },
  });
}, [props.id, cfg, updateNodeData]);
```

### 2. 各节点类型的assetType

| 节点类型 | assetType | 说明 |
|----------|-----------|------|
| ImageNode | "IMAGE" | 图片生成/导入 |
| VideoNode | "VIDEO" | 视频生成/导入 |
| CompositeNode | "VIDEO" | 合成结果通常是视频 |
| TextNode | - | 文本节点不需要assetType |

### 3. 上游节点读取逻辑

```tsx
// 获取上游连接的素材
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
        // 使用assetType或从URL推断
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

### 4. assetType大小写一致性

**问题：** 不同节点使用不同大小写的assetType会导致匹配失败。

```tsx
// ❌ 错误 - 小写
sourceConfig?.assetType === 'image'
sourceConfig?.assetType === 'video'

// ✅ 正确 - 大写
sourceConfig?.assetType === 'IMAGE'
sourceConfig?.assetType === 'VIDEO'
```

**规则：** 所有节点统一使用大写 `"IMAGE"` / `"VIDEO"` / `"TEXT"`。

## 连接验证（TapNow风格）

TapNow允许所有连接，只禁止自连接。Antoken采用相同策略：

```tsx
// workflowStore.ts
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

## 调试检查清单

连接验证不工作时，检查：

1. **assetType是否设置？**
   ```bash
   grep -n "assetType.*VIDEO\|assetType.*IMAGE" frontend/src/components/nodes/*.tsx
   ```

2. **大小写是否一致？**
   ```bash
   grep -n "assetType.*===.*'" frontend/src/components/nodes/*.tsx
   # 应该全部是大写 'IMAGE' / 'VIDEO'
   ```

3. **updateResult是否包含assetType？**
   ```bash
   grep -A 5 "const updateResult = useCallback" frontend/src/components/nodes/VideoNode.tsx
   ```

4. **getUpstreamAssets是否正确读取？**
   ```bash
   grep -A 20 "getUpstreamAssets" frontend/src/components/nodes/VideoNode.tsx
   ```
