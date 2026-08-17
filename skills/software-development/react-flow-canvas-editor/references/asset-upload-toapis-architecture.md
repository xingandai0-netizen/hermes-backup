# Antoken Asset 上传架构（2026-06-27）

## 问题背景

toapis.com 的 Asset API 限制：
- `source_url` 必须是**公开可访问的 HTTP/HTTPS URL**
- **不接受** data URL（`data:image/png;base64,...`）
- **不接受** 局域网 URL（`http://192.168.x.x`）
- **不接受** localhost URL

后端 `prepare_asset` 原来的逻辑：检测到 LAN URL → 下载 → 转 data URL → 上传到 toapis.com → **失败**（不接受 data URL）

## 解决方案

**前端直传 toapis.com Asset 系统（唯一例外，不是全面改架构）**

### 上传流程（前端）

1. 用户拖拽/导入文件
2. 上传到后端 `/api/upload` → 拿到后端 URL（用于预览显示）
3. 同时上传到 toapis.com Asset API → 拿到 `assetId`（用于生成）
4. 节点存储：
   - `assetUrl = asset://{assetId}`（生成用，被 `getUpstreamAssets` 读取）
   - `previewUrl = 后端URL`（显示用，被预览组件读取）
   - `assetId`（备用）

### toapis.com Asset API 流程

```
1. 创建 Group:   POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/groups
   Body: {"name": "antoken-upload"}
   Response: {"data": {"group_id": "xxx"}}

2. 上传文件:     POST {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets
   Body: multipart/form-data (file + group_id + asset_type)
   Response: {"data": {"asset_id": "xxx"}}

3. 轮询状态:     GET {apiUrl}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}
   等待 status === "active"
```

### 后端处理

`prepare_asset` 函数新增 `asset://` 前缀检测：

```python
if source_url.startswith("asset://"):
    asset_id = source_url.replace("asset://", "")
    await wait_asset_active(base_url, api_key, asset_id)
    return asset_id  # 跳过上传，直接返回
```

### 前端代码位置

- `assetUpload.ts`: `uploadToAsset()` 函数 — 直传 toapis.com
- `VideoNode.tsx`: `handleFileUpload` — 上传到 toapis.com + 后端
- `ImageNode.tsx`: `handleFileUpload` — 上传到 toapis.com + 后端
- `WorkflowCanvas.tsx`: `handleFileSelect`, `onDrop` — 画布拖拽
- `CircleNavPanel.tsx`: `handleFileSelect` — 侧边栏导入

### 后端代码位置

- `generate.py`: `prepare_asset()` — 检测 `asset://` 前缀
- `generate.py`: `upload_asset()` — 上传到 toapis.com
- `generate.py`: `create_asset_group()` — 创建 Group

## 关键 Pitfalls

1. **上传失败时不能静默回退** — 如果 `uploadToAsset` 失败（如额度不够），必须报错，不能回退到后端 URL。否则后续生成会报 "invalid request body"
2. **需要同时上传两处** — toapis.com（生成用）+ 后端（预览用）。`asset://` 格式不能用于预览显示
3. **后端需要重启** — 修改 `prepare_asset` 后，即使有 `--reload`，有时后端不会自动加载新代码，需要手动重启
4. **API 额度** — `uploadToAsset` 需要消耗 toapis.com 额度。额度用完会报 `quota_not_enough`
5. **旧节点不兼容** — 代码改动前创建的节点没有 `assetId`，需要重新拖拽创建
6. **后端重启方法** — `cd ~/antoken/backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000`
