# 异步上传模式（2026-06-27 验证）

## 问题

文件上传到公开文件托管（如 tmpfiles.org）需要时间，不能阻塞 UI。

## 解决方案

三步异步模式：

### 1. 后端：立即返回，后台上传

```python
# upload.py
import asyncio

_public_url_cache: dict[str, str] = {}
_uploading: dict[str, bool] = {}

async def _upload_to_public(file_path: str, filename: str, unique_name: str):
    """后台上传到 tmpfiles.org"""
    _uploading[unique_name] = True
    try:
        async with httpx.AsyncClient(timeout=60, proxy=PROXY) as client:
            with open(file_path, "rb") as f:
                resp = await client.post(
                    "https://tmpfiles.org/api/v1/upload",
                    files={"file": (filename, f)},
                )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    raw_url = data["data"]["url"]
                    public_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                    _public_url_cache[unique_name] = public_url
    except Exception as e:
        logger.warning(f"[上传] tmpfiles.org上传异常: {e}")
    finally:
        _uploading.pop(unique_name, None)

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    # 保存本地
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    # 后台异步上传（不阻塞返回）
    asyncio.create_task(_upload_to_public(file_path, file.filename, unique_name))
    return {"success": True, "asset_id": unique_name, "path": f"/api/upload/file/{unique_name}"}

@router.get("/public-url/{asset_id}")
async def get_public_url(asset_id: str):
    if asset_id in _public_url_cache:
        return {"ready": True, "public_url": _public_url_cache[asset_id]}
    if asset_id in _uploading:
        return {"ready": False, "uploading": True}
    return {"ready": False, "uploading": False}
```

### 2. 前端：立即创建节点，后台轮询

```typescript
// WorkflowCanvas.tsx
const uploadToBackend = async (file: File) => {
  const resp = await fetch(`${getApiBase()}/api/upload`, { method: "POST", body: formData });
  const data = await resp.json();
  return { localUrl: `${getApiBase()}${data.path}`, assetId: data.asset_id };
};

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

// 使用
const uploadResult = await uploadToBackend(file);
createAssetNode(type, uploadResult.localUrl, ...);  // 立即创建（本地URL预览）
pollPublicUrl(uploadResult.assetId, nodeId);         // 后台轮询公开URL
```

### 3. 节点组件：也支持轮询

VideoNode/ImageNode 的 handleFileUpload 也需要轮询：
```typescript
const result = await uploadAsset(file, apiKey, onProgress);
if (result.success && result.url) {
  updateResult(result.url, result.assetId || "");
  if (result.assetId) {
    pollPublicUrl(result.assetId, props.id);
  }
}
```

## 关键点

- 上传到后端是快速操作（本地），立即返回
- 上传到 tmpfiles.org 是慢速操作（外部服务），后台异步
- 用户立即看到节点（本地URL预览），不等待公开URL
- 公开URL就绪后自动更新，用户无感知
- 生成时如果公开URL还没就绪，会使用本地URL（可能失败）
