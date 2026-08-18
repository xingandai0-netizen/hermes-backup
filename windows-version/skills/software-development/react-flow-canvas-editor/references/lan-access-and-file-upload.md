# LAN Access & Local File Upload Patterns

## Problem: Accessing Antoken from Another Computer on LAN

When accessing `http://<server-ip>:3000` from another computer, three things break:

### 1. Hardcoded localhost:8000 in Frontend

**Fix**: Create `src/lib/api.ts` with dynamic API base:
```typescript
export function getApiBase(): string {
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8000`;
  }
  return 'http://localhost:8000';
}
```
Then replace ALL `"http://localhost:8000"` with `getApiBase()` across the codebase (~24 occurrences in 14 files).

**Files to update**: All node components, hooks/useWorkflowExecution.ts, lib/assetUpload.ts, lib/mediaProxy.ts, components/settings/SettingsModal.tsx

### 2. CORS Blocks LAN Requests

**Fix**: In `backend/app/core/config.py`:
```python
CORS_ORIGINS: list[str] = ["*"]  # Allow all origins for dev
```

### 3. WebSocket URL

In `hooks/useWorkflowExecution.ts`, WebSocket must also use dynamic host:
```typescript
const ws = new WebSocket(
  `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.hostname}:8000/ws/workflow/${workflowId}`
);
```

---

## Local File Upload Flow

### The Problem
When user drags/right-clicks to add a local file:
1. File uploaded to backend `/api/upload` → saved to temp dir → returns LAN URL
2. LAN URL stored in node's `assetUrl`
3. When generating, LAN URL sent to toapis.com as `source_url`
4. **toapis.com can't access LAN URLs** → error: "http must be a valid http or https URL"
5. **Data URLs also rejected** by toapis.com

### The Solution (3-step chain)

**Step 1**: Backend `/api/upload` endpoint saves file locally:
```python
# backend/app/api/upload.py
TEMP_DIR = os.path.join(tempfile.gettempdir(), "antoken_uploads")

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    # Save to temp dir, return path like /api/upload/file/<uuid>.ext
```
Register in `main.py`: `app.include_router(upload_router)`

**Step 2**: Frontend `WorkflowCanvas.tsx` uploads file before creating node:
```typescript
const uploadToBackend = async (file: File): Promise<string | null> => {
  const formData = new FormData();
  formData.append("file", file);
  const resp = await fetch(`${getApiBase()}/api/upload`, { method: "POST", body: formData });
  const data = await resp.json();
  return `${getApiBase()}${data.path}`;
};
```
Both `handleFileSelect` and `onDrop` must: get file dimensions → upload to backend → create node with backend URL.

**Step 3**: Backend `prepare_asset` detects local URLs → downloads → converts to data URL → `upload_asset` decodes and sends as binary multipart:
```python
# In prepare_asset:
if source_url.startswith("http://192.168.") or ...:
    # Download file, convert to data URL
    
# In upload_asset:
if source_url.startswith("data:"):
    # Decode base64 → upload as multipart form data to toapis.com
    files = {"file": (f"asset{ext}", file_content, mime)}
    data = {"group_id": group_id, "asset_type": asset_type}
    resp = await client.post(url, headers=headers, files=files, data=data)
```

### Pitfalls
- **VPN blocks files.toapis.com**: If VPN is on, video file hosting CDN may timeout. Disable VPN or check connectivity.
- **Large files**: Data URL approach doubles memory usage (base64). Fine for images, may be slow for large videos.
- **HEIC format**: Safari/WebKit handles HEIC but browsers may not display it. The upload still works.
- **Node function ordering**: `createAssetNode` must be defined BEFORE `handleFileSelect` in WorkflowCanvas.tsx (useCallback dependency issue).
- **Import merging**: sed-based import insertion can merge two imports on one line. Always verify with `head -5` after batch edits.

---

## Canvas Context Menu for Adding Assets

### Right-Click Menu
Add `onPaneContextMenu` handler to ReactFlow:
```typescript
const onPaneContextMenu = useCallback((e: MouseEvent | React.MouseEvent) => {
  e.preventDefault();
  setContextMenu({ x: e.clientX, y: e.clientY, type: 'canvas' });
}, []);
```
Menu shows: "图片素材" and "视频素材" options with file picker.

### Drag-and-Drop Files
Extend `onDrop` to check `e.dataTransfer.files` before checking for node drag data:
```typescript
const files = e.dataTransfer.files;
if (files?.length > 0) {
  const file = files[0];
  if (file.type.startsWith('image/') || file.type.startsWith('video/')) {
    // Get dimensions, upload to backend, create node
    return;
  }
}
// Fall through to existing node drag logic
```

### Asset Display for Local Files
For local assets, use `objectFit: "contain"` instead of `"cover"` to preserve original dimensions:
```typescript
// In ImageNode:
objectFit: cfg.isLocalAsset ? "contain" : "cover"
background: cfg.isLocalAsset ? "#1a1a1a" : "transparent"

// Pass isLocalAsset prop to VideoPreview
```
