# 视频编辑模式：image_with_roles + video_with_roles 组合使用

## 关键发现

`image_with_roles` 和 `video_with_roles` **可以同时使用**（文档明确允许）。
这是实现"图片+视频合成"的正确方式。

## 视频编辑请求示例

```json
{
  "model": "seedance-2",
  "prompt": "让视频中人物手中拿着图片中的笔",
  "duration": 8,
  "ratio": "16:9",
  "image_with_roles": [
    {"url": "asset://asset_img_xxx", "role": "reference_image"}
  ],
  "video_with_roles": [
    {"url": "asset://asset_vid_xxx", "role": "reference_video"}
  ]
}
```

## 前端节点逻辑

```typescript
// 根据连接的素材自动选择模式
const body: Record<string, unknown> = {
  prompt,
  api_url: videoApi.apiUrl,
  api_key: videoApi.apiKey,
  model: selectedModel,
};

if (imgUrl && videoUrl) {
  // 视频编辑模式：图片+视频合成
  body.reference_image_url = imgUrl;
  body.reference_video_url = videoUrl;
} else if (imgUrl) {
  // 图生视频模式：图片作为首帧
  body.image_url = imgUrl;
}
```

## 后端处理

```python
if req.reference_image_url and req.reference_video_url:
    # 视频编辑模式
    group_id = await create_asset_group(base, api_key)
    img_asset_id = await prepare_asset(base, api_key, group_id, req.reference_image_url, "image")
    vid_asset_id = await prepare_asset(base, api_key, group_id, req.reference_video_url, "video")
    payload["image_with_roles"] = [{"url": f"asset://{img_asset_id}", "role": "reference_image"}]
    payload["video_with_roles"] = [{"url": f"asset://{vid_asset_id}", "role": "reference_video"}]
elif req.image_url:
    # 图生视频模式
    payload["image_urls"] = [req.image_url]
```

## 竞品平台做法

调研发现 tapnow/lovart/liblibai 的视频合成本质上是：
- **不是直接传多个URL给模型**
- 而是**Agent编排系统**，把复杂任务拆分成多个步骤
- 图生视频 = 传一张图片作为首帧 + prompt
- 视频合成 = 多个步骤的结果拼接

Lovart用的模型：可灵(Kling)、Veo、Runway、海螺(Hailuo)、Seedance
LiblibAI用的模型：Seedance 2.0、可灵、万相(Wan2.1/2.2)
