# assetUpload.ts 字段名不匹配问题（2026-06-27 发现）

## 问题

后端 `/api/upload` 返回：
```json
{
  "success": true,
  "asset_id": "uuid.ext",
  "filename": "test.mp4",
  "size": 12345,
  "path": "/api/upload/file/uuid.ext"  // ← 是 path，不是 url！
}
```

但 `assetUpload.ts` 的 `uploadAsset()` 读的是：
```typescript
url: data.url || data.asset_url  // ❌ 两个都是 undefined
```

## 画布级 uploadToBackend 正确实现

```typescript
// WorkflowCanvas.tsx 和 CircleNavPanel.tsx 中的 uploadToBackend
const uploadToBackend = async (file: File): Promise<string | null> => {
  const resp = await fetch(`${getApiBase()}/api/upload`, { method: "POST", body: formData });
  const data = await resp.json();
  return `${getApiBase()}${data.path}`;  // ✅ 正确拼接
};
```

## 修复后的 assetUpload.ts

```typescript
// 修复 uploadAsset() 和 uploadFromUrl()
return {
  success: true,
  assetId: data.asset_id || data.assetId,
  url: data.url || data.asset_url || (data.path ? `${getApiBase()}${data.path}` : undefined),
};
```

同时把 `const API_BASE = getApiBase()` （模块加载时固定）改为调用时 `getApiBase()` 动态获取。

## 影响范围

- `VideoNode.handleFileUpload` — 使用 `uploadAsset`，之前拿到 `url: undefined`
- `ImageNode.handleFileUpload` — 使用 `uploadAsset`，同上
- `CircleNavPanel.handleFileSelect` — 使用自己的 `uploadToBackend`，不受影响
- `WorkflowCanvas.handleFileSelect` — 使用自己的 `uploadToBackend`，不受影响

## 教训

- 画布级上传和节点级上传用了**两套不同的函数**，逻辑不一致
- 后端返回的字段名 (`path`) 和前端期望的字段名 (`url`) 不匹配
- 修复后仍有根本问题：toapis.com Asset API 不接受 LAN URL（见 toapis-asset-upload-limits.md）
