# toapis.com API URL 限制分析（2026-06-27）

## 问题背景

Antoken 的素材导入功能：用户拖拽文件到画布 → 存储到后端 → 作为上游参考生成新素材。

## 测试结果

| 传给 toapis.com 的 URL 类型 | 结果 | 错误信息 |
|---------------------------|------|---------|
| 公开 HTTP URL（如 `https://files.toapis.com/...`） | ✅ 成功 | - |
| 局域网 URL（`http://192.168.x.x:8000/...`） | ❌ 失败 | `invalid request body` |
| 二进制 multipart 上传到 asset API | ❌ 失败 | `invalid request body` |
| base64 data URL 传给生成 API | ❌ 失败 | `base64 image is not allowed` |

## 结论

toapis.com 的所有 API 端点（asset API、图片生成、视频生成）都只接受**公开可访问的 HTTP/HTTPS URL**。
它会通过 URL 去下载文件，所以 URL 必须是它能访问到的。

## 解决方案

### 本地开发
后端上传文件时同时传到 0x0.st（免费文件托管），拿到公开 URL：
```python
# backend/app/api/upload.py
async def upload_to_public(file_path, filename):
    async with httpx.AsyncClient(timeout=60) as client:
        with open(file_path, "rb") as f:
            resp = await client.post("https://0x0.st", files={"file": (filename, f)})
        if resp.status_code == 200:
            return resp.text.strip()  # https://0x0.st/xxxx.mp4
```

### 线上部署
后端有公网域名（如 `https://antoken.com`），上传文件的 URL 本身就是公开的：
- `https://antoken.com/api/upload/file/xxx.mp4`
- toapis.com 能直接访问，不需要 0x0.st

## 废弃的方案

1. **前端直连 toapis.com** — 废案，前端无法绕过 URL 限制
2. **后端下载 LAN 文件 → 转 data URL → 传给生成 API** — 不行，`base64 image is not allowed`
3. **后端下载 LAN 文件 → 二进制上传到 asset API** — 不行，asset API 只接受 `source_url` 字段

## 正确的架构

```
用户拖拽文件 → 前端上传到后端 /api/upload
                ↓
后端保存本地 + 上传到 0x0.st 拿公开 URL
                ↓
返回 { path: "/api/upload/file/xxx", public_url: "https://0x0.st/xxx" }
                ↓
前端存储 assetUrl = public_url（用于生成）
前端用 localUrl 做预览显示
                ↓
生成时：前端发 public_url 给后端 → 后端传给 toapis.com → 成功
```
