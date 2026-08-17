# Antoken 工作流逻辑说明

## 核心原则（不咨询不改）

所有生成节点必须参考所有上游连接线素材（多个图片+多个视频）。

### 支持的工作流模式
- 图图生图：多个图片作为参考
- 图视频生图：图片+视频同时作为参考  
- 图视频生视频：图片+视频同时作为参考
- 视频视频生视频：多个视频作为参考

### API传递方式

**图片生成 (ImageRequest):**
```python
class ImageRequest(BaseModel):
    reference_image_urls: List[str] = []  # 多个图片
    reference_video_urls: List[str] = []  # 多个视频
```
用 `image_urls` 传递所有素材（图片+视频URL混合）。

**视频生成 (VideoRequest):**
```python
class VideoRequest(BaseModel):
    reference_image_urls: List[str] = []
    reference_video_urls: List[str] = []
```
用 `image_with_roles` 和 `video_with_roles` 分别传递，需要先上传到asset系统获取asset_id。

### 前端收集模式

```typescript
// ❌ 错误 - 只支持单个
let referenceVideoUrl: string | null = null;

// ✅ 正确 - 支持多个
let referenceVideoUrls: string[] = [];
let referenceImageUrls: string[] = [];

for (const edge of incomingEdges) {
  const sourceNode = nodes.find(n => n.id === edge.source);
  const url = sourceNode.data.assetUrl;
  const assetType = sourceNode.data.assetType;
  
  if (assetType === "IMAGE") referenceImageUrls.push(url);
  if (assetType === "VIDEO") referenceVideoUrls.push(url);
}
```

### 提示词自动注入素材名称

```typescript
let fullPrompt = prompt;
const refs: string[] = [];
upstream.images.forEach(img => refs.push(`[图片素材: ${img.assetName}]`));
upstream.videos.forEach(vid => refs.push(`[视频素材: ${vid.assetName}]`));
if (refs.length > 0) fullPrompt = `${refs.join(' ')}\n${prompt}`;
```

## 已知API错误

### "no images in AIX generateContent response"
**原因**: 将视频URL作为image_urls传递给图片生成API。
**解决**: 视频URL应该直接传递，让API自行处理。

### "quota_not_enough"
**原因**: toapis.com账户余额不足。
**解决**: 充值账户。

### "UnsupportedImageFormat"
**原因**: 直接传URL作为参考图（应该先上传获取asset_id）。
**解决**: 先通过/assets/upload上传，再用asset://asset_id格式传入。
