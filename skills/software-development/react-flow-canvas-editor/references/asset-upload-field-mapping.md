# assetUpload.ts 字段映射参考

## 后端 /api/upload 返回格式
```json
{
  "path": "/api/upload/file/{uuid}.{ext}",
  "filename": "xxx.mp4",
  "size": 1234567
}
```

注意：没有 `url` 或 `asset_url` 字段！只有 `path`。

## 前端正确拼接方式
```typescript
// 正确 ✓
const fullUrl = data.path ? `${getApiBase()}${data.path}` : undefined;

// 错误 ✗ — data.url 和 data.asset_url 都是 undefined
const url = data.url || data.asset_url;
```

## 画布拖拽 vs 节点直接上传

| 路径 | 代码位置 | URL处理 |
|------|---------|---------|
| 画布拖拽文件 | WorkflowCanvas.tsx onDrop | `getApiBase() + data.path` ✓ |
| 右键导入素材 | WorkflowCanvas.tsx handleFileSelect | `getApiBase() + data.path` ✓ |
| 左侧导入素材 | CircleNavPanel.tsx handleFileSelect | `getApiBase() + data.path` ✓ |
| VideoNode直接上传 | VideoNode.tsx → assetUpload.ts | `data.url \|\| data.asset_url` ✗ (已修复) |
| ImageNode直接上传 | ImageNode.tsx → assetUpload.ts | `data.url \|\| data.asset_url` ✗ (已修复) |

## API_BASE 模块级初始化陷阱

```typescript
// 错误 ✗ — 模块加载时固定，LAN访问时可能拿到 localhost
const API_BASE = getApiBase();

// 正确 ✓ — 每次调用时动态获取
const response = await fetch(`${getApiBase()}/api/upload`, { ... });
```

## 后端 LAN URL 处理流程

当后端收到 LAN URL（如 `http://192.168.0.102:8000/api/upload/file/xxx.mp4`）时：

1. `prepare_asset()` 检测到 LAN URL（192.168.x.x / 10.x.x.x / 172.x.x.x / localhost）
2. 下载文件内容 → 转 base64 data URL
3. `upload_asset()` 检测到 data URL → 解码二进制 → multipart 上传到 toapis.com
4. 等待 asset active → 返回 asset_id

此流程已验证可用，前提是 assetUrl 不是 undefined。
