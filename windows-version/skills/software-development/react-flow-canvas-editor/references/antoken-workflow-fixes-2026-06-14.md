# Antoken Workflow Fixes — 2026-06-14

## Issues Fixed

### 1. VideoNode size→resolution parameter
**Problem**: VideoNode sent `size` parameter but backend expected `resolution`
**Fix**: Changed `size` to `resolution` in request body

### 2. CompositeNode API endpoints
**Problem**: CompositeNode called `/api/composite/video` and `/api/composite/image` which don't exist
**Fix**: Changed to `/api/generate/video` (single endpoint handles all video generation)

### 3. CompositeNode parameter names
**Problem**: Used `video_url`, `image_url`, `video_asset_id`, `image_asset_id`
**Fix**: Changed to `reference_video_url`, `reference_image_url` (matching backend VideoRequest schema)

### 4. VideoNode upstream asset detection
**Problem**: VideoNode didn't pass connected upstream images/videos to backend
**Fix**: Added `getUpstreamAssets()` function that reads from edges, passes `reference_image_url`/`reference_video_url` to API

### 5. Edge color hardcoded to purple
**Problem**: CSS globals.css had `stroke: #5e6ad2 !important` overriding inline styles
**Fix**: Changed ALL edge colors to white `#ffffff` in both CSS and inline styles

### 6. Missing connection validation
**Problem**: onConnect only checked self-connection, no type validation
**Fix**: Added `isValidConnection` check with warn-but-allow pattern

### 7. Missing assetType on node results
**Problem**: Nodes didn't set `assetType` when generating/uploading content, breaking connection validation
**Fix**: Added `assetType: "VIDEO" as const` or `assetType: "IMAGE" as const` to all `updateResult` functions

### 8. ImageNode lowercase assetType
**Problem**: ImageNode used `sourceConfig?.assetType === 'image'` (lowercase)
**Fix**: Changed to `'IMAGE'` (uppercase) to match type system

## Key Patterns Discovered

### CSS !important Override Pitfall
When changing React Flow edge colors, MUST update BOTH:
1. Inline styles in workflowStore.ts onConnect handler
2. CSS globals.css `.react-flow__edge-path` rules

### assetType Must Be Set on Results
Every node that generates/uploads content must set `assetType` in `updateNodeData`:
```typescript
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO" as const,  // or "IMAGE"
  assetUrl: url,
  assetId,
  config: { ...cfg, assetUrl: url, assetId },
});
```

### Connection Validation Pattern
```typescript
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  
  const { nodes } = get();
  const sourceNode = nodes.find(n => n.id === connection.source);
  const targetNode = nodes.find(n => n.id === connection.target);
  
  if (sourceNode && targetNode) {
    const sourceType = (sourceNode.data as NodeData).assetType || "IMAGE";
    const targetType = (targetNode.data as NodeData).assetType || "IMAGE";
    
    if (!isValidConnection(sourceType, targetType)) {
      console.warn(`类型不匹配: ${sourceType} → ${targetType}`);
    }
  }
  
  // ... addEdge with white stroke
}
```

## Verification Checklist

After making workflow changes:
- [ ] TypeScript compiles (`npx tsc --noEmit`)
- [ ] All edge colors are white (check CSS + inline)
- [ ] All nodes set assetType in updateResult
- [ ] Connection validation uses isValidConnection
- [ ] Frontend and backend services running
- [ ] Browser force-refreshed (Cmd+Shift+R)
