# Video-to-Image Workflow Pattern

## Problem

When connecting a video node to an image node, the image generation should use the video as reference material.

## Failed Approaches (Do NOT use)

### 1. Base64 Data URL
```python
# Extract frame → base64 → pass to API
frame_b64 = base64.b64encode(frame_bytes).decode()
data_url = f"data:image/jpeg;base64,{frame_b64}"
payload["image_urls"] = [data_url]
```
**Result:** API rejects with "base64 image is not allowed"

### 2. Localhost URL
```python
# Extract frame → save locally → serve via local endpoint
local_url = f"http://localhost:8000/api/generate/temp-file/{filename}"
payload["image_urls"] = [local_url]
```
**Result:** External API cannot access localhost, connection refused

## Working Solution (2026-06-14 verified)

**Pass the video URL directly to the API.** The API handles video-to-image conversion internally.

```python
# In backend generate_image endpoint
if req.reference_video_url:
    # Direct pass-through - API handles video conversion
    payload["image_urls"] = [req.reference_video_url]
    logger.info(f"[图片] 已传递视频URL作为参考")
```

## Key Insight

External APIs (toapis.com, OpenAI, etc.) cannot access `localhost:8000`. Never pass local URLs to external API endpoints.

## Implementation Pattern

```python
# backend/app/api/generate.py
@router.post("/image")
async def generate_image(req: ImageRequest):
    # ...
    if req.reference_video_url:
        # Video reference: pass URL directly
        payload["image_urls"] = [req.reference_video_url]
    elif req.reference_image_urls:
        # Image reference: pass URLs directly
        payload["image_urls"] = req.reference_image_urls
```

## Node Connection Flow

```
VideoNode (assetUrl: "https://files.toapis.com/...mp4")
    ↓ connected via edge
ImageNode (reads upstream assetUrl)
    ↓ passes to API
API receives: {"image_urls": ["https://files.toapis.com/...mp4"]}
    ↓ API processes
API returns: generated image based on video content
```
