# toapis.com Asset Upload 限制（2026-06-27 发现）

## 问题

toapis.com 的 Asset API (`/videos/doubao-seedance-2-0/private-avatar/assets`) 对 `source_url` 字段有严格限制：

| URL 类型 | 是否接受 | 示例 |
|---------|---------|------|
| 公开 HTTP/HTTPS URL | ✅ 接受 | `https://files.toapis.com/xxx.mp4` |
| 局域网 URL | ❌ 拒绝 | `http://192.168.0.102:8000/api/upload/file/xxx.mp4` |
| Data URL | ❌ 拒绝 | `data:image/png;base64,iVBOR...` |
| localhost URL | ❌ 拒绝 | `http://localhost:8000/api/upload/file/xxx.mp4` |

错误响应：`{"message":"invalid request body","success":false}`

## 后端 prepare_asset 的问题

当前后端 `prepare_asset` 流程：
1. 检测到 LAN/localhost URL → 下载文件
2. 转成 data URL (`data:mime;base64,...`)
3. 调用 `upload_asset` 上传到 toapis.com
4. `upload_asset` 检测到 data URL → 解码 base64 → multipart 上传
5. **toapis.com 拒绝**（不接受 data URL）

```python
# generate.py prepare_asset 问题代码
if source_url.startswith("http://localhost") or source_url.startswith("http://192.168."):
    # 下载 → 转 data URL → 传给 upload_asset
    final_url = f"data:{mime};base64,{b64}"  # ❌ toapis.com 不接受

asset_id = await upload_asset(base_url, api_key, group_id, final_url, asset_type)
```

## 解决方案

### 方案1：前端直接上传到 toapis.com（推荐）
前端拿到用户文件后，直接调用 toapis.com 的 Asset API 上传：
1. 创建 Group: `POST /videos/doubao-seedance-2-0/private-avatar/groups`
2. 上传 Asset: `POST /videos/doubao-seedance-2-0/private-avatar/assets` (multipart)
3. 轮询状态: `GET /videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}`
4. 拿到 asset_id 存到节点

优点：简单直接，不需要后端参与
缺点：需要前端存储 toapis.com API key

### 方案2：后端上传到公开 CDN
后端下载文件 → 上传到公开可访问的 CDN → 拿到公开 URL → 传给 toapis.com

优点：前端不需要 API key
缺点：需要额外的 CDN 服务

### 方案3：后端直接 multipart 上传（绕过 data URL）
修改 `prepare_asset`，不经过 data URL 中间步骤，直接把下载的二进制内容用 multipart 上传到 toapis.com。

```python
async def prepare_asset(base_url, api_key, group_id, source_url, asset_type):
    if is_local_url(source_url):
        # 直接下载二进制
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(source_url)
            file_content = resp.content
            mime = detect_mime(source_url)
        
        # 直接 multipart 上传到 toapis.com（不经过 data URL）
        url = f"{base_url}{ASSET_UPLOAD_URL}"
        files = {"file": (f"asset{get_ext(mime)}", file_content, mime)}
        data = {"group_id": group_id, "asset_type": asset_type}
        headers = {"Authorization": f"Bearer {api_key}"}
        
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, headers=headers, files=files, data=data)
            # ... 处理响应
```

注意：此方案需要验证 toapis.com 是否接受 multipart 上传（目前未验证）。

## 关键教训

- **"前端直连toapis.com"整个架构被用户否决** — 不要再提这个方案
- 但**素材上传这一步**可能需要前端直接上传，这是局部修改不是架构变更
- 用户要求"先检查再修改" — 必须先确认问题根因再动手
