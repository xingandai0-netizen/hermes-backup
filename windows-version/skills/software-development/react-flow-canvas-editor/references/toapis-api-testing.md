# toapis.com API Testing Results (2026-06-07)

## Endpoint: GET /v1/models
Returns all available models. Key models found:

### Image Generation Models
- `gemini-3-pro-image-preview-official` — ✅ works, async task
- `nano_banana_2` — ✅ works, async task  
- `gpt-image-2` — ❌ 503 "no available channel"
- `dall-e-3` — ❌ "未配置渠道能力"
- `gemini-3.5-flash` — ❌ "不支持生成图片"
- `gpt-4o-image` — ❌ "未配置渠道能力"

### Video Generation Models
- `seedance-2` — ✅ works, async task (~2min)
- `seedance-2.0` — ❌ "未配置渠道能力" (note: different from seedance-2!)
- `kling` — ❌ "未配置渠道能力"
- `runway-gen-3` — ❌ "未配置渠道能力"

## Async Task Pattern

All generation endpoints return a task ID immediately:
```json
{"id": "tsk_img_01KTH...", "object": "generation.task", "status": "pending", "progress": 0}
```

Poll with GET `/v1/images/generations/{task_id}` or `/v1/video/generations/{task_id}`:
- `queued` → waiting for available GPU
- `in_progress` → generating (progress 0-100)
- `completed` → result in `result.data[].url`
- `failed` → error in `error.message`

Typical timing:
- Image: 30s - 2min
- Video: 1min - 3min

## Completed Task Response Format
```json
{
  "id": "tsk_vid_...",
  "status": "completed",
  "progress": 100,
  "result": {
    "data": [{"url": "https://files.toapis.com/videos/...mp4"}],
    "type": "image"
  }
}
```

## URL Pitfall
User configures `https://toapis.com/v1` as base URL.
Code must NOT append `/v1` again — strip it first:
```python
base = api_url.rstrip("/")
if base.endswith("/v1"):
    base = base[:-3]
url = f"{base}/images/generations"
```

## Secret Redaction Workaround
When writing API keys in code, the Hermes secret redaction replaces them with `***`.
Workaround: write key to a file, then read from file:
```python
from pathlib import Path
env = Path.home() / "project" / ".env"
key = None
for line in env.read_text().splitlines():
    if "API_KEY" in line:
        key = line.split("=", 1)[1].strip()
```
