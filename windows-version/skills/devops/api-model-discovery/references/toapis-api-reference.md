# toapis.com API Reference

## Base URL
`https://toapis.com/v1`

## Authentication
```
Authorization: Bearer {api_key}
```

## Endpoints

### Models
```
GET /models
```
Returns list of available models with `supported_endpoint_types`.

### Image Generation (Async)
```
POST /images/generations
{
  "model": "gemini-3-pro-image-preview-official",
  "prompt": "描述文字",
  "n": 1,
  "size": "1024x1024"
}
```
Response: `{"id": "tsk_img_xxx", "status": "pending"}`

### Image Task Status
```
GET /images/generations/{task_id}
```
Response when completed:
```json
{
  "id": "tsk_img_xxx",
  "status": "completed",
  "progress": 100,
  "result": {
    "data": [{"url": "https://files.toapis.com/images/..."}],
    "type": "image"
  }
}
```

### Video Generation (Async)
```
POST /video/generations
{
  "model": "seedance-2",
  "prompt": "描述文字",
  "duration": 5,
  "ratio": "16:9"
}
```
Also works: `POST /videos/generations`

#### seedance-2 完整参数（从官方文档确认）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | `seedance-2` 或 `seedance-2-fast` |
| prompt | string | 是 | 视频描述 |
| duration | int | 否 | 4-15秒，默认5 |
| ratio | string | 否 | `16:9`, `9:16`, `1:1`, `4:3` |
| image_urls | string[] | 否 | 首帧图片URL数组（只用第一张） |
| image_with_roles | object[] | 否 | 带角色的参考图片 |
| video_with_roles | object[] | 否 | 带角色的参考视频 |
| audio_with_roles | object[] | 否 | 带角色的参考音频 |

#### image_with_roles 格式
**⚠️ 必须用 `asset://` 格式，不能直接传HTTP URL！**
```json
{
  "image_with_roles": [
    {"url": "asset://asset-20260318071009-*****", "role": "reference_image"}
  ]
}
```
完整上传流程见 `references/seedance-2-composite-workflow.md`

#### video_with_roles 格式
```json
{
  "video_with_roles": [
    {"url": "asset://asset_id_xxx", "role": "reference_video"}
  ]
}
```

#### ⚠️ 关键教训：合成素材传参方式
**不要把素材URL拼接到prompt文本里！** 必须用 `image_with_roles` / `video_with_roles` 参数传入参考素材。
把URL写在prompt里会导致：
1. API不识别为素材引用，只当作普通文本
2. 触发 "copyright restrictions" 审核拦截
3. AI无法获取素材内容，生成结果与素材无关

**正确合成工作流：**
1. 先上传素材图片到 toapis.com 获取 asset_id（POST /assets）
2. 用 `image_with_roles` 传入素材，role 为 `reference_image`
3. prompt 描述如何合成素材（如"让人物手中拿着这支笔"）

### Video Task Status
```
GET /video/generations/{task_id}
```
Also works: `GET /videos/generations/{task_id}`

Response when completed:
```json
{
  "id": "tsk_vid_xxx",
  "status": "completed",
  "progress": 100,
  "result": {
    "data": [{"url": "https://files.toapis.com/videos/...xxx.mp4"}],
    "type": "video"
  }
}
```

## Verified Models

| Model | Type | Status | Notes |
|-------|------|--------|-------|
| gemini-3-pro-image-preview-official | Image | ✅ | 约1-2分钟 |
| nano_banana_2 | Image | ✅ | 约1-2分钟 |
| gpt-image-2 | Image | ❌ | 503 渠道不可用 |
| seedance-2 | Video | ✅ | 约2-5分钟，支持参考素材合成 |
| seedance-2-fast | Video | ✅ | 快速版 |
| seedance-2.0 | Video | ❌ | 未配置渠道 |
| kling | Video | ❌ | 未配置渠道 |

## Task Status Values
- `pending` - 排队中
- `queued` - 排队中
- `in_progress` - 生成中
- `completed` - 完成
- `failed` - 失败

## Polling Interval
- Recommended: 5 seconds
- Image timeout: 3 minutes (36 polls)
- Video timeout: 5 minutes (60 polls)

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid URL (POST /v1/v1/...)` | URL重复了/v1 | 用normalize_api_url去掉末尾/v1 |
| `未配置渠道能力` | 模型名不对 | 从/models获取实际可用模型 |
| `所有渠道都失败` | 端点不存在 | 尝试多个端点格式 |
| `copyright restrictions` | 素材URL写在prompt里 | 用image_with_roles参数传入 |
| `UnsupportedImageFormat` | image_with_roles传了HTTP URL | 先上传获取asset_id，用asset://格式 |
| `image_urls cannot be used together with image_with_roles` | 同时用了两个参数 | 二选一：合成用image_with_roles，图生视频用image_urls |
| `无效的令牌` | Key错误或.env被清 | 检查.env文件 |
