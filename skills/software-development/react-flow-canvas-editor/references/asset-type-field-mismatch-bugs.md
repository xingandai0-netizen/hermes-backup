# Asset Type & Field Name Mismatch Bugs (2026-06-14)

## Bug 1: assetType Storage Location Mismatch

**Symptom:** ImageNode couldn't detect that connected VideoNode outputs VIDEO type.

**Root Cause:**
- VideoNode stores `assetType` at `node.data` level (correct)
- ImageNode was reading from `node.data.config.assetType` (wrong!)

**Fix:**
```typescript
// Read from both locations with fallback
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

**Rule:** When storing metadata about a node's output type, always store at `node.data` level, not inside `config`.

## Bug 2: Result Field Name Mismatch

**Symptom:** ImageNode couldn't read upstream VideoNode's generated URL.

**Root Cause:**
- VideoNode stores result as `assetUrl` in both `node.data` and `config`
- ImageNode was reading `sourceConfig?.resultUrl` (wrong!)

**Fix:**
```typescript
// Read with fallback
const url = (sourceConfig?.assetUrl || sourceConfig?.resultUrl) as string | undefined;
```

**Rule:** Use consistent field names across all nodes. Current convention: `assetUrl` for generated media URLs.

## Bug 3: Video-to-Image API Doesn't Accept Base64

**Symptom:** API returns "base64 image is not allowed" error.

**Root Cause:** API (toapis.com) expects URLs, not base64 data URLs.

**Fix:** Pass video URL directly to API, let it handle video-to-image conversion:
```typescript
if (req.reference_video_url) {
    payload["image_urls"] = [req.reference_video_url];
}
```

**Bug 4: Localhost URLs Not Accessible by External APIs**
**Symptom:** API returns "connection refused" when trying to download from localhost.
**Fix:** Never pass localhost URLs to external APIs. Use publicly accessible URLs only.

## Asset Type Storage Convention

| Node | Stores assetType | Stores assetUrl |
|------|-----------------|-----------------|
| VideoNode | `node.data.assetType = "VIDEO"` | `node.data.assetUrl` + `config.assetUrl` |
| ImageNode | `node.data.assetType = "IMAGE"` | `node.data.assetUrl` + `config.assetUrl` |
| CompositeNode | `node.data.assetType = "VIDEO"` | `node.data.assetUrl` + `config.assetUrl` |
