# toapis.com Asset Upload 限制（2026-06-27 验证）

## 核心约束

toapis.com 的 asset API 和生成 API 都**只接受公开可访问的 HTTP/HTTPS URL**。

### 不接受的格式

| 格式 | 错误信息 | 来源 |
|------|---------|------|
| 二进制 multipart 上传 | `{"message":"invalid request body","success":false}` | asset API |
| base64 data URL | `Invalid request, base64 image is not allowed` | 生成 API `image_urls` |
| 局域网 URL (192.168.x.x) | toapis.com 无法访问 | asset API |

### 接受的格式

- 公开 HTTP/HTTPS URL（如 `https://files.toapis.com/...`、`https://tmpfiles.org/dl/...`）
- `asset://{asset_id}` 格式（已上传到 asset 系统的素材）

## 正确的上传架构

### 线上部署（后端有公网域名）
```
用户文件 → 后端 /api/upload → 本地存储
                                ↓
                        返回公网 URL（如 https://antoken.com/api/upload/file/xxx.mp4）
                                ↓
                        toapis.com 可直接访问 → 无需额外步骤
```

### 本地开发（后端在 LAN）
```
用户文件 → 后端 /api/upload → 本地存储（用于预览）
                ↓
        后台异步上传到 tmpfiles.org（通过代理）
                ↓
        返回公开 URL（如 https://tmpfiles.org/dl/xxx/file.mp4）
                ↓
        前端轮询获取公开 URL → 更新节点 assetUrl
                ↓
        toapis.com 通过公开 URL 访问文件
```

## 后端实现要点

### upload.py 关键代码
```python
# 代理设置
PROXY = os.environ.get("UPLOAD_PROXY", "http://127.0.0.1:6324")

async def _upload_to_public(file_path, filename, unique_name):
    """后台上传到 tmpfiles.org"""
    async with httpx.AsyncClient(timeout=60, proxy=PROXY) as client:
        with open(file_path, "rb") as f:
            resp = await client.post(
                "https://tmpfiles.org/api/v1/upload",
                files={"file": (filename, f)},
            )
        # 返回格式: {"status":"success","data":{"url":"https://tmpfiles.org/xxxxx/filename"}}
        # 转换为直接下载链接: https://tmpfiles.org/dl/xxxxx/filename
        raw_url = resp.json()["data"]["url"]
        public_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
```

### 异步上传模式
```python
@router.post("")
async def upload_file(file: UploadFile = File(...)):
    # 1. 保存到本地（立即完成）
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 2. 后台异步上传到公开托管（不阻塞返回）
    asyncio.create_task(_upload_to_public(file_path, filename, unique_name))
    
    return {"path": f"/api/upload/file/{unique_name}", "asset_id": unique_name}
```

### 公开 URL 查询端点
```python
@router.get("/public-url/{asset_id}")
async def get_public_url(asset_id: str):
    if asset_id in _public_url_cache:
        return {"ready": True, "public_url": _public_url_cache[asset_id]}
    if asset_id in _uploading:
        return {"ready": False, "uploading": True}
    return {"ready": False, "uploading": False}
```

## 前端实现要点

### 创建节点后轮询公开 URL
```typescript
const pollPublicUrl = async (assetId: string, nodeId: string) => {
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 2000));
    const resp = await fetch(`${getApiBase()}/api/upload/public-url/${assetId}`);
    const data = await resp.json();
    if (data.ready && data.public_url) {
      updateNodeData(nodeId, { assetUrl: data.public_url });
      return;
    }
  }
};
```

## 代理排查

```bash
# 检查系统代理设置
networksetup -getwebproxy Wi-Fi
scutil --proxy

# 测试代理连通性
curl -x http://127.0.0.1:6324 -s https://tmpfiles.org/api/v1/upload -F "file=@test.txt"

# 不用代理测试
curl --noproxy '*' -s https://tmpfiles.org/api/v1/upload -F "file=@test.txt"
```
