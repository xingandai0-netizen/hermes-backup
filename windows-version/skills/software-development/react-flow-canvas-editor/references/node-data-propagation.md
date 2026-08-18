# Node Data Propagation Pattern (Upstream Data Reading)

## Problem

React Flow nodes do NOT automatically share data through edges. When ImageGenNode produces a `resultUrl` and connects to an ExportNode, the ExportNode cannot magically see that URL. Each node is self-contained — it only knows its own `data.config`.

This means **export nodes, composite nodes, and any downstream consumer** must explicitly find and read data from connected upstream nodes.

## ⚠️ CRITICAL PITFALL: node.data vs node.data.config (2026-06-14)

**Bug that wasted hours:** When `updateNodeData` is called with:
```typescript
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO",      // ← stored at node.data level
  assetUrl: url,
  config: { ...cfg, assetUrl: url }
});
```

The `assetType` is at `node.data.assetType`, NOT `node.data.config.assetType`.

**Wrong pattern (reads from wrong location):**
```typescript
const sourceConfig = sourceNode.data?.config;
if (sourceConfig?.assetType === 'VIDEO') { ... }  // ← NEVER MATCHES!
```

**Correct pattern (reads from both locations):**
```typescript
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown>;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

**Rule:** When reading upstream node data, check `node.data` FIRST, then `node.data.config` as fallback.

## Solution: Store-Based Upstream Lookup

Every node that needs input data from upstream must:

1. Access the Zustand store (`useWorkflowStore`) to get `nodes` and `edges`
2. Find incoming edges: `edges.filter(e => e.target === id)`
3. For each edge, find the source node: `nodes.find(n => n.id === edge.source)`
4. Read from `node.data` first, then `node.data.config` as fallback
5. For multi-input nodes, use `edge.targetHandle` to distinguish inputs

## Correct Implementation Pattern (2026-06-14 verified)

```tsx
for (const edge of incomingEdges) {
  const sourceNode = nodes.find(n => n.id === edge.source);
  if (!sourceNode) continue;
  
  // Read from node.data level first (where updateNodeData stores top-level fields)
  const sourceData = sourceNode.data as unknown as NodeData;
  const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
  
  // URL can be in either location
  const url = (sourceConfig?.assetUrl || sourceConfig?.resultUrl) as string | undefined;
  if (!url) continue;

  // assetType is at node.data level, NOT in config
  const assetType = sourceData?.assetType || sourceConfig?.assetType;
  
  if (edge.targetHandle === 'image' || assetType === 'IMAGE') {
    referenceImageUrls.push(url);
  } else if (edge.targetHandle === 'video' || assetType === 'VIDEO') {
    referenceVideoUrl = url;
  }
}
```

## Single-Input Export Node (ImageExportNode)

```tsx
'use client';
import { Handle, Position, NodeProps } from '@xyflow/react';
import type { NodeData } from '@/types/workflow';
import BaseNode from './BaseNode';
import { useWorkflowStore } from '@/stores/workflowStore';

export default function ImageExportNode({ id, data, selected }: NodeProps) {
  const { nodes, edges } = useWorkflowStore();

  // Find connected upstream node
  const incomingEdge = edges.find(e => e.target === id);
  const sourceNode = incomingEdge ? nodes.find(n => n.id === incomingEdge.source) : null;
  const sourceData = sourceNode?.data as unknown as NodeData;
  const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
  const imgUrl = (sourceConfig?.assetUrl || sourceConfig?.resultUrl as string) || null;

  return (
    <BaseNode {...props}>
      {imgUrl ? (
        <img src={imgUrl} alt="输出图片" />
      ) : (
        <div>{incomingEdge ? '等待上游生成...' : '连接图片生成节点'}</div>
      )}
      <Handle type="target" position={Position.Left} />
    </BaseNode>
  );
}
```

## Multi-Input Composite Node (VideoCompositeNode)

For nodes with multiple inputs (e.g., IMAGE + VIDEO), use `edge.targetHandle` to distinguish:

```tsx
export default function VideoCompositeNode(props: NodeProps) {
  const { nodes, edges } = useWorkflowStore();

  const incomingEdges = edges.filter(e => e.target === props.id);
  let imgUrl: string | null = null;
  let videoUrl: string | null = null;

  for (const edge of incomingEdges) {
    const sourceNode = nodes.find(n => n.id === edge.source);
    if (!sourceNode) continue;
    
    const sourceData = sourceNode.data as unknown as NodeData;
    const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
    const url = (sourceConfig?.assetUrl || sourceConfig?.resultUrl) as string | undefined;
    if (!url) continue;

    // Read assetType from node.data level
    const assetType = sourceData?.assetType || sourceConfig?.assetType;
    
    if (edge.targetHandle === 'image' || assetType === 'IMAGE') imgUrl = url;
    else if (edge.targetHandle === 'video' || assetType === 'VIDEO') videoUrl = url;
  }

  // Render previews for both inputs...
}
```

## Key Rules

1. **Always read `assetType` from `node.data` first** — `updateNodeData` stores top-level fields there, not in `config`
2. **URL can be in either `assetUrl` or `resultUrl`** — check both locations
3. **Cast data to `NodeData`** — `sourceNode.data as unknown as NodeData`
4. **Null-check everything** — source node may not exist (deleted), config may not have url (not yet generated)
5. **Differentiate empty states**: "连接xxx节点" (not connected) vs "等待上游生成..." (connected but no data yet)

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Read `sourceConfig?.assetType` | Always undefined | Read `sourceData?.assetType` first |
| Read only `resultUrl` | Misses `assetUrl` | Check both: `assetUrl \|\| resultUrl` |
| Skip null checks | Runtime crash | Always check `sourceNode`, `url`, `assetType` |
| Use `e.target === props.id` | Wrong if destructured | Use `e.target === id` from NodeProps |
