# Antoken 实战踩坑记录 (2026-06-14)

## 1. assetType存储位置不一致（关键Bug）

**问题：** VideoNode存储assetType在`node.data.assetType`，但ImageNode从`node.data.config.assetType`读取，导致视频→图片工作流失败。

**根因：**
```typescript
// VideoNode存储（正确位置）
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO",  // ← node.data.assetType
  assetUrl: url,
  config: { ...cfg, assetUrl: url }
});

// ImageNode读取（错误位置）
const sourceConfig = sourceNode.data?.config;
if (sourceConfig?.assetType === 'VIDEO') { ... }  // ← 读不到！
```

**修复：**
```typescript
// 正确：从node.data读取assetType
const sourceData = sourceNode.data as unknown as NodeData;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

**教训：** React Flow节点数据有两层：`node.data` 和 `node.data.config`。存储时要明确在哪一层，读取时要兼容两层。

---

## 2. 字段名不一致（resultUrl vs assetUrl）

**问题：** 不同节点使用不同字段名存储结果URL：
- VideoNode/ImageNode: `config.assetUrl`
- 某些旧节点: `config.resultUrl`

**修复：** 读取时兼容两种字段名：
```typescript
const url = (sourceConfig?.assetUrl || sourceConfig?.resultUrl) as string | undefined;
```

**教训：** 统一字段命名很重要。如果无法统一，读取时要兼容所有可能的字段名。

---

## 3. 媒体代理播放（CORS问题）

**问题：** 外部媒体URL（如files.toapis.com）没有CORS头，浏览器无法直接播放。

**修复：** 
1. 后端添加代理端点：`GET /api/generate/proxy?url=xxx`
2. 前端使用`proxyUrl()`包装所有外部URL
3. video/img元素使用代理后的URL

```typescript
// mediaProxy.ts
export function proxyUrl(url: string | null): string {
  if (!url) return '';
  if (url.startsWith('http://localhost') || url.startsWith('blob:') || url.startsWith('data:')) {
    return url;
  }
  return `${PROXY_BASE}?url=${encodeURIComponent(url)}`;
}

// VideoNode.tsx
<video src={proxyUrl(previewUrl)} crossOrigin="anonymous" />
```

**关键：** video元素需要`crossOrigin="anonymous"`属性才能支持CORS代理。

---

## 4. API不接受base64图片

**问题：** `extract_video_frame`返回base64 data URL，但API报错"base64 image is not allowed"。

**错误方案：** 提取首帧→base64→传给API ❌
**正确方案：** 直接传递视频URL给API，让API自行处理 ✓

```python
# 简化方案：直接传递视频URL
if req.reference_video_url:
    payload["image_urls"] = [req.reference_video_url]
```

**教训：** 不要假设API支持所有格式。先测试API支持哪些输入格式。

---

## 5. localhost URL对外部API不可用

**问题：** 提取的视频首帧保存在本地，通过`http://localhost:8000/api/generate/temp-file/xxx`访问。但外部API（toapis.com）无法访问localhost。

**错误：** 本地文件→本地URL→传给外部API ❌
**正确：** 直接使用原始视频URL ✓

**教训：** 外部API需要公网可访问的URL。本地开发时的localhost URL对第三方服务不可用。

---

## 6. 连接线颜色CSS覆盖

**问题：** React Flow的边颜色被CSS `!important`覆盖，修改组件内联样式无效。

**修复：** 必须同时修改CSS和内联样式：
```css
/* globals.css */
.react-flow__edge-path {
  stroke: #ffffff !important;  /* 白色边 */
}
```

```typescript
// workflowStore.ts onConnect
style: { stroke: "#ffffff", strokeWidth: 2 }
```

**教训：** CSS `!important`会覆盖内联样式。修改React Flow样式时，检查globals.css是否有!important规则。

---

## 7. 节点尺寸优化（用户反馈）

**用户反馈：** "素材框太窄了"

**最终尺寸：**
- 节点宽度: 280px（从220px增加）
- 素材预览: 150px（Video/Image节点）
- 素材预览: 120px（Composite节点，多素材时稍小）
- 上传区域: 80px（从60px增加）

**教训：** 节点尺寸要根据实际内容调整。纯文本节点可以小，有预览图的节点需要更大。

---

## 8. 连接验证策略

**用户要求：** "和TapNow一样没有类型限制"

**实现：** 只禁止自连接，允许所有其他连接：
```typescript
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  // 允许所有连接，不检查类型
  ...
}
```

**教训：** 连接验证策略取决于用户需求。严格验证会限制用户灵活性，宽松验证允许更多创意工作流。
