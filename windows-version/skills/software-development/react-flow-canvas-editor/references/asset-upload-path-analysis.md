# Asset Upload Path Analysis (2026-06-27)

## Problem: Different Upload Paths Store Different URL Fields

There are **3 distinct upload paths** in Antoken, each storing URLs differently:

### Path 1: Canvas Drag-and-Drop (WorkflowCanvas.tsx)
```
User drags file to canvas → onDrop → handleFileSelect
  → uploadToBackend(file) → POST /api/upload
  → returns `${getApiBase()}${data.path}`  // e.g., http://192.168.0.102:8000/api/upload/file/xxx.mp4
  → createAssetNode(type, backendUrl, ...)
  → stores: data.assetUrl = backendUrl ✓
```
**Result**: Node has correct `assetUrl` pointing to backend.

### Path 2: Node-Level File Upload (VideoNode.tsx / ImageNode.tsx)
```
User drags file to node's upload area → handleFileUpload
  → uploadAsset(file, apiKey) from assetUpload.ts
  → POST /api/upload
  → returns: { url: data.url || data.asset_url }  // BUG: backend returns data.path, not data.url!
  → updateResult(result.url, ...) 
  → stores: data.assetUrl = undefined ❌
```
**Result**: Node has `assetUrl = undefined` due to field name mismatch.

### Path 3: AI Generation (ImageGenNode / VideoGenNode)
```
User clicks generate → API returns task → poll → completed
  → updateNodeData({ config: { resultUrl: data.url } })
  → stores: config.resultUrl = "https://files.toapis.com/..." 
  → NO assetUrl field set
```
**Result**: Node has `resultUrl` but no `assetUrl`.

## Impact on Video Generation

When VideoNode's `getUpstreamAssets()` collects upstream materials:
```typescript
const url = nodeData.assetUrl || (nodeData.config as any)?.assetUrl;
```

- Canvas drag-and-drop materials: url = `http://192.168.0.102:8000/api/upload/file/xxx.mp4` ✓
- Node-level upload materials: url = undefined → empty string ✗
- AI-generated materials: url = undefined → empty string ✗

Only canvas drag-and-drop materials get sent to the backend for generation.

## LAN URL → toapis.com Asset Upload Flow

When backend receives a LAN URL (e.g., `http://192.168.0.102:8000/api/upload/file/xxx.mp4`):

```python
# prepare_asset in generate.py
if source_url.startswith("http://192.168."):
    # 1. Download from self
    resp = await client.get(source_url)  # timeout=30
    # 2. Convert to data URL
    final_url = f"data:{mime};base64,{b64}"
    # 3. Upload via multipart to toapis.com
    files = {"file": (f"asset{ext}", file_content, mime)}
    data = {"group_id": group_id, "asset_type": asset_type}
    resp = await client.post(url, headers=headers, files=files, data=data)
```

**If download from self fails** (timeout, connection refused):
- Falls back to passing raw LAN URL as JSON: `{"source_url": "http://192.168.x.x/..."}`
- toapis.com can't access private LAN URL → returns `{"message":"invalid request body", "success":false}`

## The assetUpload.ts Bug

**File**: `frontend/src/lib/assetUpload.ts`

**Bug**: Lines 52-55 return wrong field name:
```typescript
return {
  success: true,
  assetId: data.asset_id || data.assetId,
  url: data.url || data.asset_url,  // ❌ Backend returns data.path, not data.url
};
```

**Backend returns** (`upload.py` line 38-44):
```python
return {
    "success": True,
    "asset_id": unique_name,
    "path": f"/api/upload/file/{unique_name}",  # ← This is the field
}
```

**Fix**: Change to `url: data.url || data.asset_url || (data.path ? getApiBase() + data.path : undefined)`

Or better: make backend return `url` field directly.

## Verification Steps

To debug upload issues:
1. Check browser console for `assetUrl` value in node data
2. Check backend terminal for `[Upload]` logs
3. Look for `[Upload] 检测到本地URL，下载中:` — confirms LAN URL detection
4. Look for `[Upload] 下载本地文件失败:` — confirms download failure
5. Look for `[Upload] 二进制上传 (N bytes)` — confirms data URL conversion worked
