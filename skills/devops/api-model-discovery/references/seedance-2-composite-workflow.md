# Seedance-2 Composite Workflow (toapis.com)

## Backend Logic (v0.3 final)

```python
# generate_video function - three modes
if req.reference_image_url or req.reference_video_url:
    # Video editing mode: upload assets to system
    # Supports: image only, video only, or both
    group_id = await create_asset_group(base, req.api_key)
    
    image_with_roles = []
    video_with_roles = []
    
    if req.reference_image_url:
        img_asset_id = await prepare_asset(base, req.api_key, group_id, req.reference_image_url, "image")
        image_with_roles.append({"url": f"asset://{img_asset_id}", "role": "reference_image"})
    
    if req.reference_video_url:
        vid_asset_id = await prepare_asset(base, req.api_key, group_id, req.reference_video_url, "video")
        video_with_roles.append({"url": f"asset://{vid_asset_id}", "role": "reference_video"})
    
    if image_with_roles: payload["image_with_roles"] = image_with_roles
    if video_with_roles: payload["video_with_roles"] = video_with_roles

elif req.image_url:
    # Image-to-video mode: use image_urls directly
    payload["image_urls"] = [req.image_url]

else:
    # Text-to-video mode: only prompt
    pass
```

## Asset Upload API Endpoints

```
POST /v1/videos/doubao-seedance-2-0/private-avatar/groups
  → {data: {group_id: "pg_xxx"}}

POST /v1/videos/doubao-seedance-2-0/private-avatar/assets
  body: {group_id, source_url, asset_type: "image"|"video"}
  → {data: {asset_id: "pa_xxx"}}

GET /v1/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}
  → {data: {status: "processing"|"active"|"failed"}}
```

## API Parameters (seedance-2)

```json
{
  "model": "seedance-2",
  "prompt": "描述",
  "duration": 5,
  "ratio": "16:9",
  "image_urls": ["url"],           // 首帧图（不能和image_with_roles同时用）
  "image_with_roles": [            // 参考图片（需要asset://格式）
    {"url": "asset://pa_xxx", "role": "reference_image"}
  ],
  "video_with_roles": [            // 参考视频（需要asset://格式）
    {"url": "asset://pa_xxx", "role": "reference_video"}
  ]
}
```

## Constraints

1. `image_urls` 和 `image_with_roles` **不能同时使用**
2. `image_with_roles` 的url必须是 `asset://` 格式
3. Asset上传后需要等待 `status=active` 才能使用
4. `image_with_roles` 支持的role: `reference_image`, `first_frame`, `last_frame`
5. `video_with_roles` 支持的role: `reference_video`

## Frontend Flow

1. VideoCompositeNode收集上游图片和视频URL
2. 构造带素材名称的prompt: `[图片素材: 折扇] [视频素材: 人物] 让人物拿着扇子`
3. 发送 `{prompt, model, resolution, reference_image_url, reference_video_url}` 给后端
4. 后端上传素材 → 等待active → 构造payload → 调用API
5. 前端轮询任务状态 → 显示结果

## Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `UnsupportedImageFormat` | image_with_roles传了HTTP URL | 先上传获取asset_id |
| `image_urls cannot be used together with image_with_roles` | 同时用了两个参数 | 二选一 |
| `copyright restrictions` | 素材URL写在prompt里 | 用image_with_roles参数 |
| Asset创建Group失败 | API端点路径错误 | 检查 `/videos/doubao-seedance-2-0/private-avatar/groups` |
