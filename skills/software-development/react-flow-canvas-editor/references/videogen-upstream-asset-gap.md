# VideoGenNode Missing Upstream Asset Collection

## Problem (2026-06-28)

VideoGenNode.tsx does NOT collect upstream assets from connected nodes. When a user connects an image or video node upstream and clicks generate on the VideoGenNode, the upstream content is silently ignored.

## Evidence

Grep for upstream collection patterns across all node files:

```
Node Type           | Has getUpstreamAssets?
--------------------|----------------------
ImageGenNode.tsx    | ✅ (10 matches)
ImageNode.tsx       | ✅ (7 matches)
VideoNode.tsx       | ✅ (13 matches)
CompositeNode.tsx   | ✅ (6 matches)
Img2VideoNode.tsx   | ✅ (3 matches)
VideoCompositeNode  | ✅ (2 matches)
VideoExportNode     | ✅ (2 matches)
VideoGenNode.tsx    | ❌ (0 matches)
```

## Root Cause

VideoGenNode.tsx calls `/api/generate/video` directly without:
1. Filtering incoming edges (`edges.filter(e => e.target === props.id)`)
2. Getting source node URLs from `sourceConfig.resultUrl` or `sourceConfig.assetUrl`
3. Passing `reference_image_urls` or `reference_video_urls` in the request body

## Fix Pattern

Copy the upstream collection pattern from ImageGenNode.tsx (lines 63-88, 125-157):

```typescript
// 1. Add getUpstreamAssets callback
const getUpstreamAssets = useCallback(() => {
  const incomingEdges = edges.filter((e) => e.target === props.id);
  const assets: { image?: { url: string; assetId: string }; video?: { url: string; assetId: string } } = {};
  for (const edge of incomingEdges) {
    const sourceNode = nodes.find((n) => n.id === edge.source);
    if (sourceNode) {
      const nodeData = sourceNode.data as unknown as NodeData;
      const config = nodeData.config as Record<string, unknown> | undefined;
      const url = (config?.resultUrl || nodeData.assetUrl) as string | undefined;
      const assetId = (config?.assetId || nodeData.assetId) as string | undefined;
      if (url) {
        const assetType = detectAssetType(url);
        if (assetType === "IMAGE") assets.image = { url, assetId: assetId || "" };
        else if (assetType === "VIDEO") assets.video = { url, assetId: assetId || "" };
      }
    }
  }
  return assets;
}, [edges, nodes, props.id]);

// 2. In handleGenerate, collect and send upstream assets
const assets = getUpstreamAssets();
const body: Record<string, unknown> = {
  prompt, api_url: videoApi.apiUrl, api_key: videoApi.apiKey,
  model: selectedModel, resolution: selectedSize,
};
if (assets.image) body.reference_image_urls = [assets.image.url];
if (assets.video) body.reference_video_urls = [assets.video.url];
```

## Related

- ImageGenNode.tsx: lines 63-88 (getUpstreamAssets), lines 125-157 (handleGenerate with upstream)
- ImageNode.tsx: lines 152-176 (upstream collection in handleGenerate)
- references/multi-edge-handle-patterns.md
