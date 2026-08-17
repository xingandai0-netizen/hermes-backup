# seedance-2 Video Generation Modes (2026-06-29)

## API Modes

toapis.com seedance-2 API 支持 4 种生成模式，通过 `image_with_roles` 参数控制：

| 模式 | 参数 | 说明 |
|------|------|------|
| 文生视频 | 无 image_with_roles | 纯文字描述 |
| 首帧模式 | `[{url, role: "first_frame"}]` | 指定视频开头画面 |
| 首尾帧模式 | `[{url, role: "first_frame"}, {url, role: "last_frame"}]` | 指定开头和结尾 |
| 全能参考 | `[{url, role: "reference_image"}]` | 参考图片风格 |

**重要限制**：
- `first_frame` 和 `last_frame` 不能与 `reference_image` 混用
- `seedance-2-mini` 只支持 `reference_image`，不支持帧模式
- 每种角色的数量限制：first_frame ≤ 1, last_frame ≤ 1, reference_image ≤ 9

## API Request Example

```json
{
  "model": "seedance-2",
  "prompt": "A cat walking in the garden",
  "duration": 5,
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "image_with_roles": [
    {"url": "https://example.com/first.jpg", "role": "first_frame"},
    {"url": "https://example.com/last.jpg", "role": "last_frame"}
  ]
}
```

## Frontend Implementation

### Mode Selector
```tsx
const VIDEO_MODES = [
  { label: "文生视频", value: "text" },
  { label: "首帧模式", value: "first_frame" },
  { label: "首尾帧模式", value: "first_last_frame" },
  { label: "全能参考", value: "reference" },
];

// Mode selector buttons
{VIDEO_MODES.map((mode) => (
  <button
    key={mode.value}
    onClick={() => setVideoMode(mode.value)}
    style={{
      background: videoMode === mode.value ? "rgba(10, 132, 255, 0.2)" : "rgba(255, 255, 255, 0.04)",
      border: `0.5px solid ${videoMode === mode.value ? "rgba(10, 132, 255, 0.4)" : "rgba(255, 255, 255, 0.06)"}`,
    }}
  >
    {mode.label}
  </button>
))}
```

### Frame Upload UI
```tsx
// First frame upload area
{(videoMode === "first_frame" || videoMode === "first_last_frame") && (
  <div style={{ display: "flex", gap: 8 }}>
    <div style={{ flex: 1 }}>
      <div style={{ fontSize: 10, color: "rgba(235, 235, 245, 0.4)" }}>首帧图片</div>
      <div onClick={() => {/* open file picker or URL input */}} style={{
        height: 60,
        background: firstFrameUrl ? "rgba(48, 209, 88, 0.1)" : "rgba(255, 255, 255, 0.04)",
        border: `0.5px solid ${firstFrameUrl ? "rgba(48, 209, 88, 0.3)" : "rgba(255, 255, 255, 0.08)"}`,
        borderRadius: 8,
      }}>
        {firstFrameUrl ? <img src={firstFrameUrl} /> : <PlusIcon />}
      </div>
    </div>
    {/* Last frame - only for first_last_frame mode */}
    {videoMode === "first_last_frame" && (/* similar upload area */)}
  </div>
)}
```

### Request Construction
```typescript
const image_with_roles: Array<{url: string, role: string}> = [];

if (videoMode === "first_frame" && firstFrameUrl) {
  image_with_roles.push({ url: firstFrameUrl, role: "first_frame" });
} else if (videoMode === "first_last_frame" && firstFrameUrl && lastFrameUrl) {
  image_with_roles.push({ url: firstFrameUrl, role: "first_frame" });
  image_with_roles.push({ url: lastFrameUrl, role: "last_frame" });
} else if (videoMode === "reference") {
  referenceUrls.forEach(url => {
    image_with_roles.push({ url, role: "reference_image" });
  });
}

// Send to backend
body: JSON.stringify({
  prompt, model, resolution, ratio, duration,
  image_with_roles: image_with_roles.length > 0 ? image_with_roles : undefined,
  videoMode,
})
```

## Backend Implementation

```python
class VideoRequest(BaseModel):
    # ... existing fields
    image_with_roles: Optional[List[Dict[str, str]]] = None
    videoMode: Optional[str] = None

@router.post("/video")
async def generate_video(req: VideoRequest):
    payload = {
        "model": req.model,
        "prompt": req.prompt,
        "duration": req.duration,
        "aspect_ratio": ratio,
    }
    
    # Pass image_with_roles directly to API
    if req.image_with_roles:
        payload["image_with_roles"] = req.image_with_roles
    
    # Handle video references separately (needs asset upload)
    if req.reference_video_urls:
        # Upload to asset system, create video_with_roles
        ...
```

## Validation

```typescript
// Frontend validation before sending
if (videoMode === "first_frame" && !firstFrameUrl) {
  setError("首帧模式需要上传首帧图片");
  return;
}
if (videoMode === "first_last_frame" && (!firstFrameUrl || !lastFrameUrl)) {
  setError("首尾帧模式需要上传首帧和尾帧图片");
  return;
}
```
