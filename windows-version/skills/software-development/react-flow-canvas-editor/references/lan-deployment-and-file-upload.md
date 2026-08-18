# LAN Deployment & Local File Upload Patterns

## Dynamic API Base URL (Critical for LAN Access)

Hardcoding `http://localhost:8000` breaks when accessing from another machine on the LAN.

**Solution**: Create `src/lib/api.ts`:
```typescript
export function getApiBase(): string {
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8000`;
  }
  return 'http://localhost:8000';
}
```

Then replace ALL `http://localhost:8000` references across the codebase with `getApiBase()`. This includes:
- `lib/assetUpload.ts` (API_BASE constant)
- `lib/mediaProxy.ts` (PROXY_BASE constant)
- All node components (fetch calls)
- `hooks/useWorkflowExecution.ts` (WebSocket URL uses `window.location.hostname`)
- `components/settings/SettingsModal.tsx`

**Pitfall**: The WebSocket URL needs special handling:
```typescript
const ws = new WebSocket(`${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.hostname}:8000/ws/workflow/${workflowId}`);
```

## CORS for LAN Access

Backend `app/core/config.py` must allow all origins for LAN access:
```python
CORS_ORIGINS: list[str] = ["*"]
```

Without this, requests from `http://192.168.x.x:3000` are blocked by CORS.

## Local File Upload Flow

When users drag or right-click to add local files, the flow is:

1. **Frontend**: Upload file to backend `/api/upload` endpoint
2. **Backend**: Save to temp directory, return path like `/api/upload/file/{uuid}.{ext}`
3. **Frontend**: Construct full URL `http://{hostname}:8000/api/upload/file/{uuid}.{ext}`
4. **Store**: Use this URL as `assetUrl` in node data

**Backend upload endpoint** (`app/api/upload.py`):
```python
router = APIRouter(prefix="/api/upload", tags=["upload"])
TEMP_DIR = os.path.join(tempfile.gettempdir(), "antoken_uploads")

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    # Save file, return path
    
@router.get("/file/{filename}")
async def serve_file(filename: str):
    # Serve with CORS headers
```

**Register in main.py**:
```python
from app.api.upload import router as upload_router
app.include_router(upload_router)
```

## Data URL Conversion for External APIs

When local URLs need to be sent to external APIs (like toapis.com), the external API can't access `http://192.168.x.x:8000/...`. 

**Solution**: In `prepare_asset()`, detect local URLs and convert to data URLs:
```python
if source_url.startswith("http://localhost") or source_url.startswith("http://192.168.") or ...:
    # Download file content
    # Convert to data:{mime};base64,{content}
    # Send data URL to external API
```

**Pitfall**: Data URLs can be very large for videos. The toapis.com API accepts data URLs for the `source_url` parameter in asset upload.

## File Drag & Drop Implementation

In `WorkflowCanvas.tsx`:
1. `onDragOver`: `e.preventDefault()` + `e.dataTransfer.dropEffect = "move"`
2. `onDrop`: Check `e.dataTransfer.files` first (file drag), then check `application/antoken-node` (node drag from sidebar)
3. Get file metadata (dimensions) via `Image()` or `video` element
4. Upload to backend, get URL
5. Create node with `isLocalAsset: true` in config

**Key**: `onDrop` must be `async` since upload is awaited.

**Pitfall**: Must `URL.revokeObjectURL()` after reading metadata to avoid memory leaks.
