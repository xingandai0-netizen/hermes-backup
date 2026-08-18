# AssetType Field Location Bug (2026-06-14)

## Problem
VideoNode stores `assetType` at `node.data.assetType` level, but ImageNode was reading from `node.data.config.assetType`.

## Root Cause
```typescript
// VideoNode stores at data level
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO",  // ← node.data.assetType
  assetUrl: url,
  config: { ...cfg, assetUrl: url }
});

// ImageNode was reading from config (WRONG!)
const sourceConfig = sourceNode.data?.config;
if (sourceConfig?.assetType === 'IMAGE') { ... }  // ← undefined!

// Fix: Read from both locations
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

## Solution Pattern
When reading upstream node data, ALWAYS check both locations:
```typescript
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
const url = (sourceConfig?.assetUrl || sourceConfig?.resultUrl) as string | undefined;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

## Video-to-Image Workflow (2026-06-14)

### Problem
API returned "base64 image is not allowed" when trying to use video reference for image generation.

### Root Cause
1. `extract_video_frame()` returned base64 data URL
2. API doesn't accept base64 format
3. Tried to upload to asset system but API key was invalid for testing

### Solution
Pass video URL directly to API - let API handle video-to-image conversion:
```typescript
// In generate_image endpoint
if (req.reference_video_url) {
  payload["image_urls"] = [req.reference_video_url];  // Direct URL
}
```

### Key Insight
Many AI APIs (like toapis.com) can handle video URLs directly for image generation. They extract frames internally. No need for client-side frame extraction.

## Proxy Endpoint Requirements

### Problem
Video preview failed because API couldn't access localhost:8000 URLs.

### Solution
1. Proxy endpoint must allow ALL domains (development mode)
2. Video element must have `crossOrigin="anonymous"` for CORS
3. Use `proxyUrl()` wrapper for all external media URLs

```typescript
// In VideoNode.tsx
<video
  src={proxyUrl(previewUrl)}
  crossOrigin="anonymous"
  ...
/>
```
