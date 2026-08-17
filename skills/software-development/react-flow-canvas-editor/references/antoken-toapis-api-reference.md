# Antoken API Reference — toapis.com

## Video Generation API

**Endpoint**: `POST /v1/videos/generations`

### Key Parameters
- `aspect_ratio` (NOT `ratio`! The latter is silently ignored)
- `image_with_roles` supports first_frame/last_frame/reference modes

### Modes and Parameter Format

| Mode | image_with_roles format |
|------|------------------------|
| Text-to-video | Don't pass |
| First frame | `[{url, role: "first_frame"}]` |
| First + last frame | `[{url, role: "first_frame"}, {url, role: "last_frame"}]` |
| Full reference | `[{url, role: "reference_image"}]` |

### Model Capabilities

| Model | Frame modes | Reference images | Max resolution |
|-------|-------------|-----------------|----------------|
| seedance-2 | ✅ | ✅ | 4k |
| seedance-2-fast | ✅ | ✅ | 720p |
| seedance-2-mini | ❌ | ✅ | 720p |

## Image Generation API

**Endpoint**: `POST /v1/images/generations`

### Resolution
Via `metadata.resolution`: `0.5K`, `1K`, `2K`, `4K`

### Limitations
- No video_urls support; extract first frame from video
- Max 14 reference images

## Text Generation API

**Endpoint**: `POST /v1/chat/completions` (OpenAI compatible)

### Critical Pitfall
- Must use `messages` format, NOT `prompt` field
- Older models like gpt-4o report "model channel capability mismatch"

## Local Development
- Proxy address: `127.0.0.1:6324`
- tmpfiles.org for obtaining public URLs
- 0x0.st is shut down

## Async Task Pattern
- Submit returns `task_id`
- Poll `GET /v1/tasks/{task_id}` for results

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Video always 16:9 | Sent `ratio` instead of `aspect_ratio` | Change to `aspect_ratio` |
| Reference image not working | Sent video URL to image API | Extract video first frame first |
| Upload failed | Used LAN URL | Get public URL via tmpfiles.org |
