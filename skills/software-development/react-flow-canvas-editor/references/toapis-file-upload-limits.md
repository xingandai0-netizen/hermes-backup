# toapis.com 文件上传限制（2026-06-27 确认）

## 核心限制

toapis.com 的所有 API（asset、generation）**只接受公开可访问的 HTTP/HTTPS URL**：

| 尝试的方式 | 结果 |
|-----------|------|
| 公开 URL（如 `https://files.toapis.com/...`） | 成功 |
| 局域网 URL（`http://192.168.x.x`） | 失败：`invalid request body` |
| base64 data URL（`data:image/png;base64,...`） | 失败：`base64 image is not allowed` |
| 二进制 multipart 上传到 asset API | 失败：`invalid request body` |

## 正确的文件上传架构

### 生产环境（公网部署）
后端有公网域名 → 上传的文件直接通过公网 URL 访问 → 不需要额外处理

### 本地开发（LAN）
1. 文件上传到后端 `/api/upload`（本地存储，快速）
2. 后端异步上传到 tmpfiles.org（通过代理 `http://127.0.0.1:6324`）获取公开 URL
3. 前端轮询 `/api/upload/public-url/{asset_id}` 获取公开 URL
4. 公开 URL 存入节点 `assetUrl`，供 toapis.com 访问

### 为什么不直接上传到 toapis.com
toapis.com 的 asset API 只接受 `source_url` 字段（公开 URL），不接受文件二进制内容。没有直接的文件上传端点。

## tmpfiles.org 使用

```python
# 上传
async with httpx.AsyncClient(timeout=60, proxy="http://127.0.0.1:6324") as client:
    with open(file_path, "rb") as f:
        resp = await client.post("https://tmpfiles.org/api/v1/upload", files={"file": (filename, f)})
    data = resp.json()
    # 返回: {"status":"success","data":{"url":"https://tmpfiles.org/xxxxx/filename"}}
    # 转换为直接下载链接: https://tmpfiles.org/dl/xxxxx/filename
    public_url = data["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")
```

## 已知问题
- **0x0.st 已关闭上传**（2026-06-27，因 AI botnet spam）
- **代理必需**：Mac 环境需要通过 `127.0.0.1:6324` 代理访问外部服务
- **tmpfiles.org 有大小限制**：大文件可能上传失败
- **公开 URL 有时效性**：tmpfiles.org 的文件会过期，不适合长期存储
