# Antoken v0.5 已知问题归档

## 1. API报错 "no images in AIX generateContent response"

**原因**: 将视频URL作为 `image_urls` 传递给图片生成API。
**解决**: 视频URL应该直接传递，让API自行处理。

```python
# ✅ 正确：直接传视频URL
if req.reference_video_urls:
    all_image_urls.extend(req.reference_video_urls)
```

## 2. elif只选一个素材

**原因**: 使用 `elif` 导致只能选择视频或图片其中一个。
**解决**: 改为同时收集所有素材。

```python
# ❌ 错误
if video:
    image_urls = [video]
elif images:
    image_urls = images

# ✅ 正确
all_urls = []
if video: all_urls.extend(video)
if images: all_urls.extend(images)
```

## 3. 视频首帧URL是localhost

**原因**: `extract_video_frame` 返回 `http://localhost:8000/...`，外部API无法访问。
**解决**: 不要提取首帧，直接传视频URL。

## 4. 素材名称计数器重置

**原因**: 模块级 `let` 变量在HMR时重置。
**解决**: 使用全局window变量。

```typescript
const getGlobalCounter = (type: string) => {
  if (typeof window !== 'undefined') {
    const key = `__assetCounter_${type}`;
    (window as any)[key] = ((window as any)[key] || 0) + 1;
    return (window as any)[key];
  }
  return 1;
};
```

## 5. ReactFlow双击被拦截

**原因**: ReactFlow默认双击行为是缩放到节点。
**解决**: 使用单击显示控制面板，不要依赖双击。

## 6. VideoPreview onClick阻止冒泡

**原因**: VideoPreview的onClick调用 `e.stopPropagation()`，阻止ReactFlow选中节点。
**解决**: 不在VideoPreview外层div添加onClick，让事件正常冒泡。

## 7. resp.text vs resp.text() 函数调用

**原因**: `resp.text` 是函数引用，不加括号会返回 `function text() { [native code] }`。
**解决**: 必须用 `await resp.text()` 调用。

```typescript
// ❌ 错误
throw new Error(`失败: ${resp.text}`)

// ✅ 正确
throw new Error(`失败: ${await resp.text()}`)
```

## 8. 局域网访问 toapis.com

**问题**: 后端代理模式下，LAN 电脑无法使用（局域网 URL 对 toapis.com 不可见）。
**解决**: 前端直连 toapis.com（CORS 支持 `*`），后端只做文件上传和媒体代理。
**详细**: 见 `references/toapis-api-reference.md`

## 9. toapis.com API 端点格式

**问题**: 前端直连时用了错误端点 `/generate/video`。
**正确**: `/video/generations` 或 `/videos/generations`。
**详细**: 见 `references/toapis-api-reference.md`
