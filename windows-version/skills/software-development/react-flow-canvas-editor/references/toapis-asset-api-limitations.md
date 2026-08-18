# toapis.com Asset API 限制（2026-06-27 实测确认）

## 核心结论

toapis.com 的 asset API **只接受 JSON 格式的 `source_url`**，不接受任何二进制上传。

## 验证过程

### 测试1：multipart 二进制上传
```
POST /videos/doubao-seedance-2-0/private-avatar/assets
Content-Type: multipart/form-data
Body: file=<binary>, group_id=xxx, asset_type=image

Response: {"message":"invalid request body","success":false}
```
❌ 失败

### 测试2：JSON + data URL
```json
{
  "group_id": "xxx",
  "source_url": "data:image/png;base64,iVBOR...",
  "asset_type": "image"
}
```
❌ 失败（不接受 data URL）

### 测试3：JSON + LAN URL
```json
{
  "group_id": "xxx",
  "source_url": "http://192.168.0.102:8000/api/upload/file/xxx.png",
  "asset_type": "image"
}
```
❌ 失败（toapis.com 无法访问内网）

### 测试4：JSON + 公开 URL
```json
{
  "group_id": "xxx",
  "source_url": "https://files.toapis.com/images/xxx.png",
  "asset_type": "image"
}
```
✅ 成功（AI 生成的素材用这种方式）

## 正确的导入素材方案

**不要用 asset 系统**，直接把文件传给生成 API：

1. 前端上传文件到后端 `/api/upload`（用于预览）
2. 后端收到生成请求时：
   - 检测到 LAN URL → 下载文件 → 转 base64 data URL
   - 直接传给生成 API 的 `image_urls` 字段
3. 生成 API 接受 data URL 格式

```python
# 后端 generate.py
if req.reference_image_urls:
    image_urls = []
    for url in req.reference_image_urls:
        if url.startswith("http://192.168.") or url.startswith("http://localhost"):
            # 下载并转 data URL
            resp = await httpx.AsyncClient().get(url)
            b64 = base64.b64encode(resp.content).decode()
            image_urls.append(f"data:{mime};base64,{b64}")
        else:
            image_urls.append(url)
    payload["image_urls"] = image_urls
```

## API 端点参考

| 功能 | 端点 | 接受格式 |
|------|------|---------|
| 创建 Group | POST `/videos/doubao-seedance-2-0/private-avatar/groups` | JSON |
| 上传 Asset | POST `/videos/doubao-seedance-2-0/private-avatar/assets` | JSON (source_url 必须是公开URL) |
| 查询 Asset | GET `/videos/doubao-seedance-2-0/private-avatar/assets/{id}` | - |
| 图片生成 | POST `/images/generations` | JSON (image_urls 接受 data URL) |
| 视频生成 | POST `/video/generations` | JSON (image_urls 接受 data URL) |
