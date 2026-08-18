# toapis.com API 参考（2026-06-27 验证）

## 核心限制（重要！）

toapis.com 的所有 API（Asset API + 生成 API）**只接受公开可访问的 HTTP/HTTPS URL**。

**不接受的格式：**
- ❌ 二进制文件上传（multipart form data）→ `{"message":"invalid request body","success":false}`
- ❌ Base64 data URL → `base64 image is not allowed`
- ❌ 局域网 URL（`http://192.168.x.x`）→ toapis.com 无法访问
- ❌ localhost URL → toapis.com 无法访问

**唯一能用的格式：**
- ✅ 公开 HTTP/HTTPS URL（如 `https://files.toapis.com/...`、`https://tmpfiles.org/dl/...`）

## 视频生成 API 参数

**关键：使用 `aspect_ratio` 不是 `ratio`！**

```json
{
  "model": "seedance-2",
  "prompt": "描述文本",
  "duration": 5,
  "aspect_ratio": "9:16",
  "resolution": "1080p"
}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | `seedance-2` | 模型名 |
| `prompt` | string | | 视频描述 |
| `duration` | int | 0 | 秒数（4-15s，0=自动） |
| `aspect_ratio` | string | | `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` |
| `resolution` | string | `720p` | `480p`, `720p`, `1080p`, `4k` |
| `image_urls` | string[] | | 首帧图/参考图 URL |

**⚠️ 2026-06-28 教训：** 后端发送 `ratio` 参数被 API 静默忽略，导致所有视频都是 16:9。必须用 `aspect_ratio`。

## 正确端点

| 功能 | 正确端点 |
|------|---------|
| 视频生成 | `POST /video/generations` 或 `/videos/generations` |
| 图片生成 | `POST /images/generations` |
| 视频轮询 | `GET /video/generations/{task_id}` |
| 图片轮询 | `GET /images/generations/{task_id}` |

## Asset API 端点

```
创建Group: POST /videos/doubao-seedance-2-0/private-avatar/groups
上传Asset: POST /videos/doubao-seedance-2-0/private-avatar/assets
查询Asset: GET  /videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}
```

## 生成 API 传参考图

- 图片生成：`payload["image_urls"] = [url1, url2]`（直接传 URL）
- 视频生成：同样支持 `payload["image_urls"] = [url1, url2]`
- **不需要**走 Asset 系统（`image_with_roles`），直接传 `image_urls` 即可

## 本地开发解决方案

由于本地文件 URL（`http://192.168.x.x:8000/api/upload/file/xxx`）不是公开 URL，
需要将文件上传到公开文件托管服务获取公开 URL。

### 推荐方案：tmpfiles.org + 代理

```python
PROXY = os.environ.get("UPLOAD_PROXY", "http://127.0.0.1:6324")

async with httpx.AsyncClient(timeout=60, proxy=PROXY) as client:
    with open(file_path, "rb") as f:
        resp = await client.post(
            "https://tmpfiles.org/api/v1/upload",
            files={"file": (filename, f)},
        )
    data = resp.json()
    raw_url = data["data"]["url"]  # https://tmpfiles.org/xxxxx/filename
    public_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")  # 直接下载链接
```

**⚠️ 代理必须**：Mac 上外部 HTTP 请求需要通过 `127.0.0.1:6324` 代理，否则超时。

### 异步上传流程（2026-06-27 验证）

1. 前端上传文件到后端 `/api/upload`（本地存储 + 预览）→ **立即返回**
2. 后端后台异步上传到 tmpfiles.org → 获取公开 URL
3. 前端立即创建节点（本地 URL 预览）
4. 前端轮询 `/api/upload/public-url/{asset_id}` 获取公开 URL
5. 公开 URL 就绪后自动更新节点的 `assetUrl`
6. 生成时，前端发公开 URL 给后端，后端传给 toapis.com

### 已知文件托管服务状态（2026-06-27）

- ❌ 0x0.st — 已关闭上传（"uploads disabled because of AI botnet spam"）
- ✅ tmpfiles.org — 可用（需要代理）
- ❌ transfer.sh — 不稳定
- ❌ file.io — 301 重定向问题

## 常见错误

- `{"message":"invalid request body","success":false}` → Asset API 不接受二进制上传
- `base64 image is not allowed` → 生成 API 不接受 data URL
- `{'code': 'quota_not_enough'}` → 账户额度用完
- 上传超时 → 检查代理设置

## 架构原则

- **后端代理**所有 API 调用（生成、轮询、模型发现）
- **后端负责**文件上传到公开托管服务获取公开 URL
- **前端只存储**公开 URL，不直连 toapis.com
- **线上部署**时后端有公网域名，不需要第三方托管
- "前端直连 toapis.com" 是**废案**
