# toapis.com API Integration Reference

## Video Generation (seedance-2)

### Endpoints
- Create task: `POST /v1/video/generations` or `POST /v1/videos/generations`
- Query task: `GET /v1/video/generations/{task_id}`

### Three Modes

#### 1. Text-to-Video (文生视频)
```json
{
  "model": "seedance-2",
  "prompt": "描述",
  "duration": 5,
  "ratio": "16:9"
}
```

#### 2. Image-to-Video (图生视频)
```json
{
  "model": "seedance-2",
  "prompt": "描述",
  "image_urls": ["https://xxx.jpg"]
}
```

#### 3. Video Compositing (视频合成/编辑)
Requires asset upload first. Cannot use `image_urls` and `image_with_roles` together.

```json
{
  "model": "seedance-2",
  "prompt": "让人物手中拿着图片中的笔",
  "image_with_roles": [{"url": "asset://pa_xxx", "role": "reference_image"}],
  "video_with_roles": [{"url": "asset://pa_yyy", "role": "reference_video"}]
}
```

### Asset Upload Flow (REQUIRED for video compositing)
1. Create group: `POST /v1/videos/doubao-seedance-2-0/private-avatar/groups`
   - Body: `{"name": "xxx"}`
   - Returns: `group_id`
2. Upload asset: `POST /v1/videos/doubao-seedance-2-0/private-avatar/assets`
   - Body: `{"group_id": "...", "source_url": "https://...", "asset_type": "image|video"}`
   - Returns: `asset_id`
3. Poll status: `GET /v1/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}`
   - Wait until `status = "active"` (usually 2-12 seconds)
4. Use in generation: `asset://{asset_id}` format

### Role Types
- `reference_image` — reference image for style/content
- `reference_video` — reference video for style/motion
- `first_frame` — use as video first frame
- `last_frame` — use as video last frame

## Image Generation (gemini-3-pro-image-preview-official)

### Endpoint
- `POST /v1/images/generations`

### With Reference Images
```json
{
  "model": "gemini-3-pro-image-preview-official",
  "prompt": "把笔放到手中",
  "image_urls": ["https://pen.jpg", "https://hand.jpg"],
  "n": 1,
  "size": "1024x1024"
}
```
- Up to 14 reference images via `image_urls`
- No asset upload needed — direct URLs work

## Task Response Format
```json
{
  "status": "completed",
  "progress": 100,
  "result": {
    "data": [{"url": "https://files.toapis.com/..."}],
    "type": "image"
  }
}
```
URL extracted from: `result.data[0].url`

## CORS Issue
`files.toapis.com` does NOT set CORS headers. Must proxy through backend.
Proxy must return: `Content-Length`, `Accept-Ranges: bytes`, `Access-Control-Allow-Origin: *`

## Pitfalls
- `image_urls` and `image_with_roles` CANNOT be used together (API returns error)
- Asset upload endpoints use path `/v1/videos/doubao-seedance-2-0/private-avatar/...` (not `/v1/assets`)
- Asset must be `active` before use — poll until ready
- Copyright filter may block certain composite requests
