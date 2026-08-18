# Antoken 工作流逻辑归档

## 核心原则（不咨询不改）

所有生成节点必须参考所有上游连接线素材（多图+多视频）：
- 图图生图：多个图片作为参考
- 图视频生图：图片+视频同时作为参考
- 图视频生视频：图片+视频同时作为参考
- 视频视频生视频：多个视频作为参考

## API传递方式

### 图片生成 (ImageRequest)
```python
class ImageRequest(BaseModel):
    reference_image_urls: List[str] = []
    reference_video_urls: List[str] = []
```
- 用 `image_urls` 传递所有素材（图片+视频URL混合）

### 视频生成 (VideoRequest)
```python
class VideoRequest(BaseModel):
    reference_image_urls: List[str] = []
    reference_video_urls: List[str] = []
```
- 用 `image_with_roles` 和 `video_with_roles` 分别传递
- 素材先通过 `/assets/upload` 上传获取 `asset_id`
- 再用 `asset://asset_id` 格式传入

## 前端收集模式

```typescript
// ❌ 错误 - 只支持单个
let referenceVideoUrl: string | null = null;

// ✅ 正确 - 支持多个
let referenceVideoUrls: string[] = [];
let referenceImageUrls: string[] = [];

for (const edge of incomingEdges) {
  const sourceNode = nodes.find(n => n.id === edge.source);
  const url = sourceNode.data.assetUrl;
  const assetType = sourceNode.data.assetType;
  
  if (assetType === "IMAGE") {
    referenceImageUrls.push(url);
  } else if (assetType === "VIDEO") {
    referenceVideoUrls.push(url);
  }
}
```

## 素材自动命名系统

### 命名规则
- 图片节点：图素材1、图素材2...（按创建时间递增）
- 视频节点：视频素材1、视频素材2...
- 名称存储在 `node.data.assetName`

### 创建节点时自动生成名称

**重要：** 使用模块级变量做计数器，页面刷新后重置。必须用 `window` 全局变量。

```typescript
const getGlobalCounter = (type: string) => {
  if (typeof window !== 'undefined') {
    const key = `__assetCounter_${type}`;
    (window as any)[key] = ((window as any)[key] || 0) + 1;
    return (window as any)[key];
  }
  return 1;
};

function getAssetName(nodeType: string): string {
  const type = nodeType.toUpperCase();
  if (type === "IMAGE") return `图素材${getGlobalCounter("IMAGE")}`;
  if (type === "VIDEO") return `视频素材${getGlobalCounter("VIDEO")}`;
  return "素材";
}
```

**存储位置陷阱：** `assetName` 存储在 `node.data.assetName`，不是 `node.data.config.assetName`。

```typescript
// 创建节点时
data: { label, category, nodeType, config: {...}, assetName } as NodeData

// 读取时 - 从 data 读取，不是 cfg
const d = props.data as unknown as NodeData;
const cfg = d.config as { assetName?: string; ... };

// ❌ 错误 - cfg.assetName 是 undefined
<span>{cfg.assetName || "素材"}</span>

// ✅ 正确 - 从 d.assetName 读取
<span>{d.assetName || "素材"}</span>
```

### 提示词自动注入素材名称
```typescript
let fullPrompt = prompt;
const refs: string[] = [];
upstream.images.forEach(img => refs.push(`[图片素材: ${img.assetName}]`));
upstream.videos.forEach(vid => refs.push(`[视频素材: ${vid.assetName}]`));
if (refs.length > 0) fullPrompt = `${refs.join(' ')}\n${prompt}`;
```

### @提及输入组件
文件：`frontend/src/components/MentionInput.tsx`
- 输入@弹出素材列表
- 支持键盘导航（↑↓箭头、回车选择、ESC关闭）
- 按类型显示不同图标（图片/视频）
- **没有连接素材时显示默认选项**（图素材、视频素材）

```tsx
// 没有连接素材时显示默认选项
const defaultMentions: MentionItem[] = [
  { id: 'default-image', name: '图素材', type: 'image' },
  { id: 'default-video', name: '视频素材', type: 'video' },
];
const allMentions = mentions.length > 0 ? filteredMentions : defaultMentions.filter(m =>
  m.name.toLowerCase().includes(filterText.toLowerCase())
);
```

### 素材名称标签位置
在素材框外面（左上角），不是在预览区内部：

```tsx
// ✅ 正确 - 在预览区外面
<div style={{ position: "relative" }}>
  <div style={{
    display: "flex", alignItems: "center", gap: 4,
    padding: "4px 8px 4px 4px", marginBottom: 4,
  }}>
    <svg ...>{/* 图标 */}</svg>
    <span>{d.assetName || "素材"}</span>
  </div>
  <div style={{ ... }}>
    <VideoPreview ... />
  </div>
</div>
```

## 已知问题归档

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| API报错 "no images in AIX generateContent response" | 视频URL当图片用 | 直接传递视频URL，让API处理 |
| elif只选一个素材 | 使用了elif逻辑 | 改为同时收集所有素材 |
| 视频首帧URL是localhost | 提取的帧保存在本地 | 不要提取首帧，直接传视频URL |
| API额度不足 | 账户余额不足 | 充值toapis.com账户 |
| quota_not_enough | toapis.com积分用完 | 充值后重试 |
| "call upstream API failed: connection refused" | 本地URL外部API无法访问 | 不传localhost URL给外部API |
| 素材名称都叫"素材" | 模块级变量页面刷新后重置 | 用window全局变量 |
| cfg.assetName读不到 | assetName在data中不在config中 | 用d.assetName读取 |

## v0.5 里程碑（2026-06-15）

工作流逻辑跑通，支持所有上游素材（多图+多视频）：
- 图图生图 ✅
- 图视频生图 ✅  
- 图视频生视频 ✅
- 视频视频生视频 ✅

前端：Next.js 14 + React Flow + Zustand
后端：FastAPI
API：toapis.com
节点：280px，主色 #ffffff，暗色主题

## toapis.com API关键限制

1. `image_urls` 和 `image_with_roles` 不能同时使用
2. 参考图片必须先通过 `/assets/upload` 上传获取 `asset_id`
3. 直接传URL作为参考图会报 `UnsupportedImageFormat`
4. 合成节点正确逻辑：收集上游素材URL → 上传获取asset_id → 用image_with_roles传入

## 文件路径

- 后端API: `backend/app/api/generate.py`
- 工作流引擎: `backend/app/api/workflow.py`
- 前端节点: `frontend/src/components/nodes/`
- @提及组件: `frontend/src/components/MentionInput.tsx`
