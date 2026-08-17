# toapis.com Asset 上传模式（2026-06-27 验证）

## 核心限制

toapis.com Asset API **只接受公开可访问的 HTTP/HTTPS URL**：
- 不接受 data URL（`data:image/png;base64,...`）
- 不接受局域网 URL（`http://192.168.x.x`）
- 不接受二进制 multipart 上传
- **只接受** `source_url` 字段指向公开 CDN 的 URL

## AI生成素材 vs 导入素材

| 类型 | URL来源 | toapis.com能访问？ | 结果 |
|------|---------|-------------------|------|
| AI生成 | `https://files.toapis.com/...` | ✅ 能 | 成功 |
| 拖拽/导入 | `http://192.168.0.102:8000/api/upload/file/...` | ❌ 不能 | `invalid request body` |

## 解决方案：前端直传 + asset:// 引用

### 前端上传流程
1. 用户拖拽文件到画布/节点
2. 前端同时上传到：
   - 后端 `/api/upload` → 拿到后端URL（用于**预览显示**）
   - toapis.com Asset API → 拿到 `assetId`（用于**生成**）
3. 节点存储：
   - `assetUrl = asset://{assetId}`（生成用）
   - `previewUrl = 后端URL`（显示用）

### toapis.com Asset API 流程
```
1. 创建Group: POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/groups
   Body: {"name": "antoken-upload"}
   Response: {"data": {"group_id": "xxx"}}

2. 上传文件: POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets
   Headers: Authorization: Bearer {apiKey}
   Body: multipart/form-data
     - file: 文件二进制
     - group_id: 上一步的group_id
     - asset_type: "image" 或 "video"
   Response: {"data": {"asset_id": "xxx"}}

3. 轮询状态: GET {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}
   等待 status == "active"（最多60秒）
```

### 后端处理
```python
# prepare_asset 检测 asset:// 前缀，跳过上传
if source_url.startswith("asset://"):
    asset_id = source_url.replace("asset://", "")
    await wait_asset_active(base_url, api_key, asset_id)
    return asset_id
```

### 上游连接逻辑（不变）
- `getUpstreamAssets` 读取节点的 `assetUrl`
- 发送 `reference_image_urls: ["asset://{assetId}"]` 给后端
- 后端识别 `asset://` 前缀 → 直接用 `assetId`，不重新上传

## 代码位置

- 前端上传函数: `src/lib/assetUpload.ts` → `uploadToAsset()`
- 画布拖拽: `src/components/canvas/WorkflowCanvas.tsx` → `handleFileSelect`, `onDrop`
- 侧边栏导入: `src/components/sidebar/CircleNavPanel.tsx` → `handleFileSelect`
- 节点拖拽: `src/components/nodes/VideoNode.tsx`, `ImageNode.tsx` → `handleFileUpload`
- 后端处理: `backend/app/api/generate.py` → `prepare_asset()`

## 常见陷阱

1. **旧节点没有assetId**: 代码修改前创建的节点 `assetUrl` 是后端URL，不是 `asset://` 格式。必须删除旧节点，重新拖拽创建新节点。

2. **静默回退**: 如果 `uploadToAsset` 失败（如额度用完），不能静默回退到后端URL。必须报错阻止节点创建，否则后续生成会报 `invalid request body`。

3. **API额度**: `uploadToAsset` 需要消耗 toapis.com 额度。如果额度用完，上传会失败。

4. **预览显示**: `asset://{assetId}` 不是有效URL，不能用于预览。必须同时上传到后端获取预览URL。节点需要两个字段：
   - `assetUrl` = `asset://{assetId}`（生成用）
   - `previewUrl` = 后端URL（显示用）

5. **后端必须重启**: 修改 `prepare_asset` 后，后端必须重启才能生效。`--reload` 标志应该会自动重载，但有时需要手动重启。
