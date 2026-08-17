# Multi-Asset Workflow & Edge Handling (2026-06-15)

## ReactFlow Edge Replacement Bug

**Symptom**: Connecting multiple source nodes to same target handle → only last connection kept.

**Root cause**: `addEdge()` from `@xyflow/react` may generate duplicate edge IDs for connections to the same target handle.

**Fix**: Generate unique edge IDs with `Date.now()` and append directly to array:

```typescript
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  set((s) => {
    const edgeId = `edge-${connection.source}-${connection.sourceHandle || 'output'}-${connection.target}-${connection.targetHandle || 'input'}-${Date.now()}`;
    const newEdge = { id: edgeId, ...connection, animated: true, style: { stroke: "#ffffff", strokeWidth: 2 }, type: "smoothstep" };
    const updated = [...s.edges, newEdge]; // Direct append, NOT addEdge()
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},
```

## Multi-Asset Collection Pattern

**Problem**: Using `elif` logic when collecting multiple assets misses some assets.

**Wrong**: `if video: urls = [video] elif images: urls = images`

**Correct**: Collect all assets separately, then combine:
```python
all_urls = []
if videos: all_urls.extend(videos)
if images: all_urls.extend(images)
```

**Frontend**: Use arrays for all reference types:
```typescript
// ❌ Wrong - only supports single
let referenceVideoUrl: string | null = null;

// ✅ Correct - supports multiple
let referenceVideoUrls: string[] = [];
```

## getUpstreamAssets Must Use nodeType, Not URL

**Problem**: Nodes without uploaded assets (no URL) are skipped, but they should still be counted as connected.

**Fix**: Use `nodeType` to determine asset type, not URL presence:
```typescript
const nodeType = nodeData.nodeType || (nodeData.config as any)?.nodeType;
if (nodeType === "IMAGE") assets.images.push({ url: url || "", assetName });
else if (nodeType === "VIDEO") assets.videos.push({ url: url || "", assetName });
```

## Asset Naming with localStorage

**Problem**: Module-level counters reset on page refresh. Window global counters may be called twice in React strict mode.

**Solution**: Use localStorage for persistent, correct counting:
```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

**Alternative**: Count existing nodes with matching names:
```typescript
const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
const count = existingNames.filter(n => n.startsWith('图素材')).length + 1;
```

## Asset Name Storage Location

**Critical**: `assetName` is stored at `node.data.assetName`, NOT `node.data.config.assetName`.

```typescript
// ✅ Correct read
const assetName = nodeData.assetName || (nodeData.config as any)?.assetName || "素材";

// ❌ Wrong - only checks config
const assetName = (nodeData.config as any)?.assetName || "素材";
```

## Prompt Construction with Asset References

```typescript
let fullPrompt = prompt;
const refs: string[] = [];
let idx = 1;
upstream.images.forEach((img) => {
  refs.push(`[素材${idx}: ${img.assetName}]`);
  idx++;
});
upstream.videos.forEach((vid) => {
  refs.push(`[素材${idx}: ${vid.assetName}]`);
  idx++;
});
if (refs.length > 0) {
  fullPrompt = `${refs.join(' ')}\n${prompt}`;
}
```

## API Payload Structure

**Frontend sends**:
```json
{
  "prompt": "[素材1: 图素材5] [素材2: 图素材7]...",
  "reference_image_urls": ["url1", "url2"],
  "reference_video_urls": ["url3"]
}
```

**Backend converts to**:
```json
{
  "image_with_roles": [
    {"url": "asset://id1", "role": "reference_image"},
    {"url": "asset://id2", "role": "reference_image"}
  ],
  "video_with_roles": [
    {"url": "asset://id3", "role": "reference_video"}
  ]
}
```
