# Verified API Integration Pattern (Antoken v0.1)

## Problem
All AI generation was mock (setTimeout + picsum.photos). User discovered and was frustrated:
"生成的图片和我的要求根本不符合"

## Solution: Real API Pipeline

### Frontend Flow
```
User types prompt → clicks "生成图片" → fetch POST to backend → 
backend calls AI API → returns image/video URL → 
frontend shows preview on node
```

### Backend Endpoints Required

| Endpoint | Method | Request Body | Response |
|----------|--------|--------------|----------|
| `/api/generate/image` | POST | `{prompt, n, size, quality, model, api_url}` | `{images: [{url}]}` |
| `/api/generate/video` | POST | `{prompt, duration, resolution, model, api_url, mode, image_url?}` | `{video: {url, thumbnail}}` |

### Error Handling (Required)
- Empty prompt → "请输入图片描述"
- Missing API Key → "请先配置API Key"
- API timeout → "API请求超时"
- HTTP error → show error detail from response
- Empty response → "未返回图片/视频"

### Status Transitions
```
idle → running(progress%) → success(preview shown)
idle → running → error(error message shown)
success → running (re-generate)
```

### Key Implementation Notes
1. Use `async/await` with `fetch`, NOT `setTimeout` simulation
2. Pass `api_url` from frontend settings to backend (don't hardcode)
3. Backend proxies to AI API (frontend doesn't call AI API directly)
4. Progress is indeterminate during API call (no real % available)
5. Button shows "生成中..." during call, "重新生成" after success
