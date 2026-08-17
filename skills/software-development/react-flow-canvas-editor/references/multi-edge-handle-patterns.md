# Multi-Edge Handle Patterns

## Problem: ReactFlow Only Allows One Incoming Connection

ReactFlow v12 default `ConnectionMode.Strict` silently replaces edges when connecting a second source to the same target handle.

## Solution: ConnectionMode.Loose

```tsx
import { ConnectionMode } from "@xyflow/react";

<ReactFlow
  connectionMode={ConnectionMode.Loose}
  ...
/>
```

## Edge ID Uniqueness

`addEdge()` from ReactFlow may generate duplicate IDs. Use direct array append:

```tsx
// In workflowStore.ts onConnect handler
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  
  get().saveSnapshot();
  set((s) => {
    const edgeId = `edge-${connection.source}-${connection.sourceHandle || 'output'}-${connection.target}-${connection.targetHandle || 'input'}-${Date.now()}`;
    const newEdge = {
      id: edgeId,
      ...connection,
      animated: true,
      style: { stroke: "#ffffff", strokeWidth: 2 },
      type: "smoothstep",
    };
    const updated = [...s.edges, newEdge];
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},
```

## Upstream Asset Collection

Collect ALL connected assets (multiple images + videos):

```typescript
const getUpstreamAssets = useCallback(() => {
  const incomingEdges = edges.filter((e) => e.target === props.id);
  const assets = { images: [], videos: [] };

  for (const edge of incomingEdges) {
    const sourceNode = nodes.find((n) => n.id === edge.source);
    if (!sourceNode) continue;
    
    const nodeData = sourceNode.data as unknown as NodeData;
    const url = nodeData.assetUrl || (nodeData.config as any)?.assetUrl;
    const assetName = nodeData.assetName || (nodeData.config as any)?.assetName || "素材";
    const nodeType = nodeData.nodeType || (nodeData.config as any)?.nodeType;

    if (nodeType === "IMAGE") {
      assets.images.push({ url: url || "", assetName });
    } else if (nodeType === "VIDEO") {
      assets.videos.push({ url: url || "", assetName });
    }
  }
  return assets;
}, [edges, nodes, props.id]);
```

## API Request Format

```typescript
// Frontend sends arrays
const resp = await fetch("http://localhost:8000/api/generate/video", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: fullPrompt,
    reference_image_urls: upstream.images.filter(i => i.url).map(i => i.url),
    reference_video_urls: upstream.videos.filter(v => v.url).map(v => v.url),
  }),
});

// Backend uploads each to asset system
for img_url in req.reference_image_urls:
    img_asset_id = await prepare_asset(base, api_key, group_id, img_url, "image")
    image_with_roles.append({"url": f"asset://{img_asset_id}", "role": "reference_image"})
```

## Pitfalls

1. **Only 1 edge stored** - Must set `connectionMode={ConnectionMode.Loose}`
2. **Edges replaced** - Use `[...s.edges, newEdge]` not `addEdge()`
3. **Asset name undefined** - Read from `nodeData.assetName`, not `config.assetName`
4. **Empty URLs passed** - Filter with `.filter(i => i.url)` before sending
