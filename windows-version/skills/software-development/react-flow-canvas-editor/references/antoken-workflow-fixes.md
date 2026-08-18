# Antoken Workflow Fixes (2026-06-14)

Session-specific fixes for the Antoken project. Reference these patterns when debugging similar issues.

## 1. assetType Storage Location Mismatch

**Bug**: ImageNode couldn't read upstream video assetType because it was stored at wrong location.

**Root Cause**:
- VideoNode stores `assetType` at `node.data.assetType` (correct)
- ImageNode reads from `node.data.config.assetType` (wrong - doesn't exist)

**Fix**: Read from both locations with fallback:
```typescript
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

**Rule**: Always store `assetType` at `node.data` level, not inside `config`.

## 2. Video Preview CORS Fix

**Bug**: Video preview showed play icon with diagonal lines (failed to load).

**Root Cause**: External video URLs (files.toapis.com) don't have CORS headers. Browser blocks direct access.

**Fix**:
1. Use `proxyUrl()` from `@/lib/mediaProxy` for all external URLs
2. Add `crossOrigin="anonymous"` to video elements
3. Backend proxy endpoint must return proper CORS headers

```typescript
import { proxyUrl } from "@/lib/mediaProxy";

<video 
  src={proxyUrl(previewUrl)} 
  crossOrigin="anonymous"
  style={{ width: "100%", height: 150, objectFit: "cover" }}
  muted
  playsInline
/>
```

## 3. Connection Validation (TapNow Style)

**Bug**: Type-based connection validation blocked valid user workflows.

**Fix**: Remove type restrictions. Allow all connections except self-connection:
```typescript
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  // Allow all other connections
  get().saveSnapshot();
  set((s) => ({ edges: addEdge(connection, s.edges) }));
},
```

## 4. Video Frame Extraction for Image Generation

**Bug**: API rejected base64 images (`base64 image is not allowed`).

**Root Cause**: `extract_video_frame` returned `data:image/jpeg;base64,...` but API only accepts URLs.

**Fix**: Save extracted frame to local file, serve via endpoint, pass URL to API:
```python
# 1. Extract frame with ffmpeg
subprocess.run(["ffmpeg", "-i", video_path, "-vframes", "1", "-ss", "0", frame_path])

# 2. Save to temp directory with unique name
frame_filename = f"frame_{uuid.uuid4().hex[:12]}.jpg"
frame_path = os.path.join(tempfile.gettempdir(), frame_filename)

# 3. Return local URL
return f"http://localhost:8000/api/generate/temp-file/{frame_filename}"
```

## 5. Edge Color Configuration

**Multiple locations** must be updated for consistent edge colors:
1. `globals.css` - `.react-flow__edge-path { stroke: #ffffff !important; }`
2. `workflowStore.ts` - `style: { stroke: "#ffffff", strokeWidth: 2 }`
3. `WorkflowCanvas.tsx` - `connectionLineStyle={{ stroke: "#ffffff" }}`

CSS `!important` overrides inline styles - always update both.

## 6. Node Width Reference

Final approved sizes:
- Node width: 280px (was 220px, user requested larger)
- Material preview: 150px (Video/Image), 120px (Composite)
- Upload area: 80px
