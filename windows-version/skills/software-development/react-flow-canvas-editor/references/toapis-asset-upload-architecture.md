# toapis.com Asset 上传架构

## 核心问题

toapis.com 的 Asset API **不接受**：
- data URL (`data:image/png;base64,...`)
- 局域网 URL (`http://192.168.x.x:8000/...`)

只接受**公开可访问的 HTTP/HTTPS URL**。

## 正确架构

```
用户拖拽文件 → 前端直接上传到 toapis.com asset 系统 → 拿到 assetId
                                                    ↓
              同时上传到后端 /api/upload → 拿到后端URL（用于预览显示）
                                                    ↓
              节点存储 assetUrl = asset://{assetId}（生成用）
                     + previewUrl = 后端URL（显示用）
                                                    ↓
              生成时，后端收到 asset://{assetId} → 跳过上传 → 直接用 assetId
```

## 错误架构（废案）

```
前端直连 toapis.com 做所有API调用 ← 这是废案，阿戴明确否决
```

正确理解：只在**素材上传**这一步前端直连 toapis.com，其他所有 API 调用（生成、轮询等）仍然通过后端代理。

## toapis.com Asset API 流程

1. **创建 Group**: `POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/groups`
   - Body: `{"name": "antoken-upload"}`
   - 返回: `{data: {group_id: "xxx"}}`

2. **上传文件**: `POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets`
   - multipart form: `file` + `group_id` + `asset_type`（"image" 或 "video"）
   - Header: `Authorization: Bearer {apiKey}`
   - 返回: `{data: {asset_id: "xxx"}}`

3. **轮询状态**: `GET {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}`
   - 等待 `status === "active"`（最多60秒，每2秒轮询）

## 后端 prepare_asset 修改

```python
# 如果已经是asset://引用，直接返回asset_id（前端已上传）
if source_url.startswith("asset://"):
    asset_id = source_url.replace("asset://", "")
    await wait_asset_active(base_url, api_key, asset_id)
    return asset_id
```

## 关键教训

1. **不要静默回退**: 当 uploadToAsset 失败时，直接报错 alert，不要创建节点用后端URL回退——后续生成必定失败
2. **双重上传**: 前端同时上传到 toapis.com（生成用）和后端（预览用）
3. **asset:// 格式**: 节点的 assetUrl 存 `asset://{assetId}`，不是普通URL
4. **previewUrl 字段**: 节点额外存 `previewUrl`（后端URL）用于预览显示
