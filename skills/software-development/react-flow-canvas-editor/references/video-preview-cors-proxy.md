# Video/Image Preview CORS Proxy Pattern

## Problem
External media URLs (from API providers like toapis.com) don't have CORS headers. Browsers block direct access, causing video/image preview to fail with a broken play icon.

## Solution
1. **Backend proxy endpoint**: `/api/generate/proxy?url=<encoded_url>`
2. **Frontend proxyUrl() utility**: Wraps external URLs through the proxy
3. **crossOrigin="anonymous"** attribute on video/img elements

## Implementation

### Backend (FastAPI)
```python
@router.get("/proxy")
async def proxy_media(url: str):
    """代理外部媒体文件，绕过CORS限制"""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code != 200:
            raise HTTPException(resp.status_code, "资源获取失败")
        
        return Response(
            content=resp.content,
            media_type=resp.headers.get("content-type", "application/octet-stream"),
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
                "Accept-Ranges": "bytes",
                "Content-Length": str(len(resp.content)),
            },
        )
```

### Frontend (mediaProxy.ts)
```typescript
const PROXY_BASE = 'http://localhost:8000/api/generate/proxy';

export function proxyUrl(url: string | null): string {
  if (!url) return '';
  if (url.startsWith('http://localhost') || url.startsWith('blob:') || url.startsWith('data:')) {
    return url;
  }
  return `${PROXY_BASE}?url=${encodeURIComponent(url)}`;
}
```

### Node Components
```tsx
import { proxyUrl } from "@/lib/mediaProxy";

// Video preview
<video
  src={proxyUrl(previewUrl)}
  crossOrigin="anonymous"  // REQUIRED for CORS
  style={{ width: "100%", height: 150, objectFit: "cover" }}
  muted
  playsInline
/>

// Image preview
<img src={proxyUrl(previewUrl)} crossOrigin="anonymous" />
```

## Critical Rules
1. **ALWAYS use proxyUrl()** for external media URLs in video/img elements
2. **ALWAYS add crossOrigin="anonymous"** to video/img elements
3. **Domain whitelist**: Expand `allowed_domains` in proxy endpoint for new API providers
4. **Large files**: Proxy endpoint should have size limit (50MB recommended)

## Common Pitfall
Forgetting to apply proxyUrl() to the video src attribute. The PreviewModal uses it, but the inline node preview often doesn't. Check ALL video/img elements in node components.
