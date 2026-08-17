# CORS Media Proxy for Video/Image Preview

When using external API providers (toapis.com, OpenAI, etc.), generated media URLs often lack CORS headers. Browsers block direct playback/preview.

## Backend Proxy (FastAPI)

```python
@router.get("/proxy")
async def proxy_media(url: str):
    """代理外部媒体文件，绕过CORS限制"""
    try:
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
                    "Access-Control-Allow-Headers": "*",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(len(resp.content)),
                },
            )
    except httpx.TimeoutException:
        raise HTTPException(504, "资源获取超时")
```

## Frontend Proxy Utility

```typescript
// frontend/src/lib/mediaProxy.ts
const PROXY_BASE = 'http://localhost:8000/api/generate/proxy';

export function proxyUrl(url: string | null): string {
  if (!url) return '';
  if (url.startsWith('http://localhost') || url.startsWith('blob:') || url.startsWith('data:')) {
    return url;
  }
  return `${PROXY_BASE}?url=${encodeURIComponent(url)}`;
}
```

## Usage in Components

```tsx
import { proxyUrl } from "@/lib/mediaProxy";

// Image preview
<img src={proxyUrl(previewUrl)} />

// Video preview - MUST add crossOrigin for CORS
<video
  src={proxyUrl(previewUrl)}
  crossOrigin="anonymous"  // CRITICAL for video CORS
  muted
  playsInline
/>
```

## Pitfalls

1. **Video crossOrigin**: Video elements need `crossOrigin="anonymous"` attribute in addition to proxy
2. **Domain whitelist**: Proxy must support all domains in development. Use whitelist only in production
3. **Common CDN domains to allow**: files.toapis.com, cdn.toapis.com, files.openai.com, storage.googleapis.com, replicate.delivery
4. **All nodes need proxy**: VideoNode, ImageNode, CompositeNode all need proxyUrl() for preview
