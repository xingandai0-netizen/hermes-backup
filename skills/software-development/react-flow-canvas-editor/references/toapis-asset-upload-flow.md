# toapis.com Asset Upload Flow (2026-06-27)

## Problem

toapis.com Asset API has strict URL requirements:
- `source_url` MUST be publicly accessible HTTP/HTTPS URL
- **REJECTS** data URLs (`data:image/png;base64,...`)
- **REJECTS** LAN URLs (`http://192.168.x.x`, `http://localhost`)
- Error: `{"message":"invalid request body","success":false}`

The backend's `prepare_asset` tried: LAN URL → download → data URL → upload to toapis.com → FAILS.

## Solution: Frontend Direct Upload

### Frontend (assetUpload.ts → uploadToAsset)

```
1. POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/groups
   Body: {"name": "antoken-upload"}
   → returns group_id

2. POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets
   Content-Type: multipart/form-data
   Fields: file (binary), group_id, asset_type ("image"|"video")
   → returns asset_id

3. GET {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}
   Poll every 2s until status === "active"
   → asset ready to use
```

### Node Data Storage

```typescript
{
  assetUrl: `asset://${assetId}`,  // for generation (sent to backend)
  assetId: assetId,                // direct reference
  previewUrl: backendUrl,          // for display (http://192.168.x.x:8000/api/upload/file/xxx)
  config: {
    assetUrl: `asset://${assetId}`,
    assetId,
    previewUrl: backendUrl,
  }
}
```

### Backend (generate.py → prepare_asset)

```python
# Skip upload if already an asset reference
if source_url.startswith("asset://"):
    asset_id = source_url.replace("asset://", "")
    await wait_asset_active(base_url, api_key, asset_id)
    return asset_id
```

### getUpstreamAssets (VideoNode)

Reads `assetUrl` from upstream nodes → sends `asset://{assetId}` to backend → backend skips upload.

## Pitfalls

1. **assetUpload.ts field name**: Backend `/api/upload` returns `{path: "/api/upload/file/xxx"}`, NOT `{url: ...}`. Must use `data.path` with `getApiBase()` prefix.

2. **Silent fallback is BAD**: If `uploadToAsset` fails, show alert and DON'T create node. Silent fallback to backend URL causes "invalid request body" error later during generation.

3. **API Key required**: `uploadToAsset` needs `videoApi.apiUrl` and `videoApi.apiKey`. Check before calling.

4. **Quota exhaustion**: If toapis.com returns `quota_not_enough`, the upload fails. User must recharge.

5. **Preview vs Generation URL**: `assetUrl` (asset://) is for generation, `previewUrl` (http://backend) is for display. Don't mix them up. Preview components must read from `previewUrl` first, fall back to `assetUrl`.

6. **Old nodes won't work**: Nodes created before this change have `assetUrl = backend URL`. Must create NEW nodes after the fix.

## Debug Logging

Add console.log with prefixes for tracing:
- `[Upload]` - frontend upload to toapis.com
- `[Asset]` - asset upload function internals  
- `[Generate]` - what URLs are sent to backend
