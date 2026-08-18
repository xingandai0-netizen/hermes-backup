# Media Proxy Pattern (CORS Bypass)

## Problem

External media URLs (from toapis.com, OpenAI, etc.) don't have CORS headers. Browsers cannot directly play/load these URLs in `<video>` or `<img>` elements.

## Solution: Backend Proxy

All external media must go through the backend proxy endpoint.

### Frontend: proxyUrl utility

```typescript
// frontend/src/lib/mediaProxy.ts
import { getApiBase } from "@/lib/api";

const PROXY_BASE = getApiBase() + '/api/generate/proxy';

export function proxyUrl(url: string | null): string {
  if (!url) return '';
  // Local URLs don't need proxy (localhost, blob:, data:)
  if (url.startsWith('http://localhost') || url.startsWith('blob:') || url.startsWith('data:')) {
    return url;
  }
  // External URLs go through proxy
  return `${PROXY_BASE}?url=${encodeURIComponent(url)}`;
}
```

### Backend: proxy endpoint

```python
@router.get("/proxy")
async def proxy_media(url: str):
    """Proxy external media files, bypass CORS"""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url, follow_redirects=True)
        content_type = resp.headers.get("content-type", "application/octet-stream")
        return Response(
            content=resp.content,
            media_type=content_type,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Accept-Ranges": "bytes",
                "Content-Length": str(len(resp.content)),
            },
        )
```

## ⚠️ CRITICAL: Must use proxyUrl for ALL media previews

**Bug that wasted hours:** Video preview showed broken play icon because `previewUrl` was used directly without proxy.

### Wrong:
```tsx
<video src={previewUrl} />  // ← CORS error, video won't play
```

### Correct:
```tsx
import { proxyUrl } from "@/lib/mediaProxy";

<video src={proxyUrl(previewUrl)} crossOrigin="anonymous" />
```

## Rules

1. **ALL external media URLs must go through `proxyUrl()`** — video, image, audio
2. **Video elements need `crossOrigin="anonymous"`** — required for proxied content
3. **Check BOTH CSS and inline styles** — CSS `!important` overrides inline styles
4. **Proxy endpoint should allow all domains during development** — use whitelist for production
5. **Test proxy with curl first** — `curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/api/generate/proxy?url=https://example.com/video.mp4"`

## CSS Override Pitfall

When edge/connection colors don't change despite updating inline styles:

```tsx
// This WON'T work if CSS has !important
style={{ stroke: "#ffffff" }}

// Check globals.css for:
.react-flow__edge-path {
  stroke: #5e6ad2 !important;  // ← This overrides inline!
}
```

**Fix:** Update BOTH the CSS `!important` rule AND the inline style.

## Domain Whitelist

During development, allow all domains. For production, restrict:

```python
allowed_domains = [
    "files.toapis.com", "toapis.com",
    "cdn.toapis.com", "storage.toapis.com",
    "files.openai.com", "cdn.openai.com",
    "storage.googleapis.com",
    "replicate.delivery", "pbxt.replicate.delivery",
]
```
