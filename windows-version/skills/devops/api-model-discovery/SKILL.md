---
name: api-model-discovery
description: "自动从API中转站发现可用的图片/视频生成模型。根据模型名和endpoint类型智能匹配。包含异步任务轮询模式和URL规范化。"
version: 2.0.0
author: xiaohei
triggers:
  - 模型发现
  - model discovery
  - 获取模型列表
  - API模型
  - 图片生成
  - 视频生成
  - AI生成API
  - toapis
  - 素材合成
  - 视频合成API
---

# API模型自动发现与AI生成集成

## 核心原则（阿戴要求）

1. **不要猜测模型名** — 必须从 `/v1/models` 实际获取
2. **不要AI幻觉** — 每个功能都要实际测试验证
3. **模糊匹配** — 差不多名字的模型就行，不要揪着符号
4. **自动发现** — 设置里输入URL和Key后，自动获取可用模型

## 模型发现流程

### Step 1: 获取模型列表
```
GET {api_url}/models
Authorization: Bearer {api_key}
```

### Step 2: 严格分类（只看endpoint_types，不靠名字猜）
**关键教训：** `gpt-4o-image` 名字带"image"但 `supported_endpoint_types` 为空，实际不支持图片生成。

**图片生成模型识别：**
- 唯一可靠规则：`supported_endpoint_types` 包含 `image-generation`
- 不满足的模型即使名字带 `image`/`dall-e`/`flux` 也不要标记为可用
- 兜底：维护已验证模型列表（实际API调用确认能用的）

**视频生成模型识别：**
- 唯一可靠规则：`supported_endpoint_types` 包含 `video-generation`
- 兜底：维护已验证模型列表

### Step 3: 选择最佳模型
优先级排序（已验证可用）：
- 图片: `gemini-3-pro-image-preview-official` > `nano_banana_2` > `dall-e-3`
- 视频: `seedance-2` > `kling` > `runway-gen-3`

## 异步任务轮询模式（关键！）

大多数中转站的图片/视频生成是**异步**的，不是同步返回结果：

### 后端实现（立即返回模式）
```python
# POST 创建任务 → 立即返回 task_id
@router.post("/image")
async def generate_image(req: ImageRequest):
    resp = await client.post(url, json=payload, headers=headers)
    data = resp.json()
    return {"task_id": data.get("id"), "status": "pending"}

# GET 轮询状态 → 前端每5秒调用
@router.get("/task/{task_type}/{task_id}")
async def get_task_status(task_type, task_id, api_url, api_key):
    resp = await client.get(f"{url}/{task_id}", headers=headers)
    data = resp.json()
    result = {"status": data.get("status"), "progress": data.get("progress", 0)}
    if data.get("status") == "completed":
        result["url"] = data["result"]["data"][0]["url"]
    return result
```

### 前端实现（轮询模式）
```typescript
// 创建任务后立即返回，前端轮询
const pollTask = (taskId: string) => {
  pollRef.current = setInterval(async () => {
    const resp = await fetch(`/api/generate/task/image/${taskId}?api_url=...&api_key=...`);
    const data = await resp.json();
    setProgress(data.progress || 0);
    if (data.status === "completed" && data.url) {
      clearInterval(pollRef.current!);
      setPreviewUrl(data.url);
      setLoading(false);
    } else if (data.status === "failed") {
      clearInterval(pollRef.current!);
      setError(data.error);
      setLoading(false);
    }
  }, 5000); // 每5秒轮询
};
```

**关键：不要用后端阻塞式轮询！** 后端阻塞会导致前端卡死不动。

## URL规范化

用户配置的API URL可能带 `/v1` 后缀，需要处理：

```python
def normalize_api_url(api_url: str) -> str:
    url = api_url.rstrip('/')
    if url.endswith('/v1'):
        url = url[:-3]  # 去掉末尾的/v1
    return url

# 尝试多个端点
endpoints = [
    f"{base}/images/generations",    # 不带v1
    f"{base}/v1/images/generations", # 带v1
]
```

## 节点内模型选择（UI模式）

节点上应该有模型选择下拉框，而不是只在设置里配置：

```tsx
// 节点内模型选择
<select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
  {availableModels.length > 0 ? (
    availableModels.map(m => <option key={m} value={m}>{m}</option>)
  ) : (
    <><option value="gemini-3-pro-image-preview-official">gemini-3-pro-image</option></>
  )}
</select>

// 自动发现模型
useEffect(() => {
  if (apiUrl && apiKey) {
    fetch(`/api/generate/models/discover?api_url=...&api_key=...`)
      .then(r => r.json())
      .then(data => {
        if (data.image_models?.length > 0) {
          setAvailableModels(data.image_models);
        }
      });
  }
}, [apiUrl, apiKey]);
```

## 已验证的中转站

### toapis.com
- URL: `https://toapis.com/v1`
- 图片模型: `gemini-3-pro-image-preview-official` ✅, `nano_banana_2` ✅
- 视频模型: `seedance-2` ✅
- 端点: `/images/generations`, `/video/generations`
- 异步轮询: 5秒间隔，图片约1-2分钟，视频约2-5分钟
- 注意: `gpt-image-2` 渠道不可用（503错误）

## 第三方API集成原则（阿戴核心要求）

**"不要缝缝补补，先搞明白所有逻辑再一次性修改"**

### 集成新API的正确流程

1. **先查官方文档** — 不要猜测参数用法
2. **研究竞品实现** — 看看tapnow/lovart/liblibai等是怎么做的
3. **理解完整参数规则** — 所有参数的组合约束、互斥关系
4. **用curl测试** — 在写代码之前，先用curl验证API行为
5. **一次性写对** — 不要写一半测一半改一半

### 当API报错时

1. **读错误信息** — 错误信息通常告诉你 exactly 什么问题
2. **查文档** — 看看参数是否有特殊约束
3. **研究竞品** — 其他平台是怎么调用同一个API的
4. **不要猜测** — 不要"试试这个参数"，要确认再改

**阿戴原话："你要先明白目的逻辑，工作逻辑，代码运行逻辑，调用模型逻辑。再有问题给你删了"**

## 诊断优先原则（阿戴要求）

**遇到错误时，先确定原因和问题，不要急着修改代码。**

诊断步骤：
1. **识别错误来源** — 看错误格式判断是哪个系统返回的
   - `{"message":"...", "success":false}` → toapis.com 返回的
   - `{"detail":"..."}` → 本地 FastAPI 后端返回的
   - 浏览器控制台 `TypeError: Failed to fetch` → 前端无法连接后端
2. **对比正常场景** — 同样的代码在哪里能用？差异在哪？
3. **追踪完整链路** — 前端 → 后端 → 外部API，哪一环断了？

## LAN 素材上传 "invalid request body" 排查

**症状：** localhost 正常，LAN 电脑上传素材时报 `素材上传失败: ("message":"invalid request body", "success":false)`

**根因链路：**
1. 前端上传文件到后端 → 后端保存 → 返回 URL `http://192.168.x.x:8000/api/upload/file/xxx.mp4`
2. 用户触发生成 → 后端 `prepare_asset` 检测到 LAN URL
3. 后端尝试从 `http://192.168.x.x:8000` 下载自己 → **可能失败**
4. 下载失败时，退回到把原始 LAN URL 传给 toapis.com
5. toapis.com 无法访问内网地址 → 返回 "invalid request body"

**关键检查点：**
- `prepare_asset` 的下载逻辑（generate.py:213-236）：如果下载失败，`final_url` 保持原始 LAN URL
- `upload_asset` 的 JSON 分支（generate.py:159-181）：直接把 LAN URL 作为 `source_url` 发给 toapis.com
- toapis.com 收到内网 URL 后无法 fetch → 返回 "invalid request body"

**排查命令：**
```bash
# 1. 检查后端是否绑定了 0.0.0.0（否则无法从 LAN IP 访问自己）
ps aux | grep uvicorn
# 应该看到 --host 0.0.0.0

# 2. 测试后端能否从 LAN IP 下载自己
curl -s -o /dev/null -w "%{http_code}" http://192.168.x.x:8000/api/upload/file/test.mp4

# 3. 查看后端日志中的 [Upload] 行，确认是走了 data URL 分支还是 JSON 分支
grep "\[Upload\]" backend.log
```

**修复方向（确认原因后再改）：**
- 如果是 uvicorn 没绑 0.0.0.0 → 加 `--host 0.0.0.0`
- 如果是下载超时 → 增加 timeout 或改用 `http://127.0.0.1` 替换 LAN IP
- 如果是 toapis.com 不接受 multipart → 改用 JSON + 公开 URL 方案

## 常见错误与解决

| 错误 | 原因 | 解决 |
|------|------|------|
| `Invalid URL (POST /v1/v1/...)` | URL重复了/v1 | 用normalize_api_url去掉末尾/v1 |
| `未配置渠道能力` | 模型名不对 | 从/models获取实际可用模型 |
| `所有渠道都失败` | 端点不存在 | 尝试多个端点格式 |
| 前端卡住不动 | 后端阻塞式轮询 | 改为立即返回+前端轮询 |
| `无效的令牌` | Key错误或.env被清 | 检查.env文件 |
| `copyright restrictions` | 素材URL写在prompt里 | 用image_with_roles参数传入参考素材 |
| `UnsupportedImageFormat` | image_with_roles传了HTTP URL | 先上传获取asset_id，用asset://格式 |
| `image_urls cannot be used together with image_with_roles` | 同时用了两个参数 | 二选一：合成用image_with_roles，图生视频用image_urls |
| `invalid request body` (Asset API) | source_url是内网LAN URL(toapis无法访问)或data URL格式不对 | 后端prepare_asset应先下载LAN文件转data URL再binary上传；检查下载是否超时/失败。详见 `references/asset-api-invalid-body-debug.md` |

## 素材合成工作流（电商场景核心）

**目的：** 把多个素材（图片/视频）按用户要求融合成新素材。
例如：笔的图片 + 人物视频 → 人物手中拿着笔的视频

**⚠️ 阿戴核心要求：先搞明白所有合成逻辑，再一次性修改代码。不要缝缝补补。**
遇到API问题时：先查官方文档 → 理解完整参数规则 → 再写代码。不要猜测参数用法。

**三种合成模式：**
| 模式 | 输入 | API参数 | 场景 |
|------|------|---------|------|
| 文生视频 | prompt | 只用prompt | 从零生成 |
| 图生视频 | 图片+prompt | `image_urls: [url]` | 静态图变视频 |
| 视频编辑 | 图片+视频+prompt | `image_with_roles` + `video_with_roles` | 在原视频基础上添加/修改 |
| 图片合成 | 多张图片+prompt | `image_urls: [url1, url2, ...]` | 多图融合（最多14张） |

**图片合成（多图融合）：**
```python
# 支持传入多张参考图片
payload = {
    "model": "gemini-3-pro-image-preview-official",
    "prompt": "[素材: 扇子] [素材: 男人]\n让男人手中拿着扇子",
    "image_urls": [fan_url, man_url],  # 最多14张
}
```

**素材名称嵌入prompt：**
```typescript
// 前端收集素材名称，嵌入prompt
const refs = referenceUrls.map((_, i) => `[素材: ${referenceNames[i]}]`).join(' ');
const fullPrompt = `${refs}\n${userPrompt}`;
```

**⚠️ 错误做法（会导致版权审核拦截）：**
```python
# 错误！把URL拼接到prompt里
prompt = f"让人物手中拿着这支笔\n参考图片: {img_url}\n参考视频: {video_url}"
```

**✅ 正确做法（4步流程）：**
```python
# Step 1: 创建Asset Group
resp = POST f"{base}/videos/doubao-seedance-2-0/private-avatar/groups"
group_id = resp.json()["data"]["group_id"]

# Step 2: 上传素材
resp = POST f"{base}/videos/doubao-seedance-2-0/private-avatar/assets"
payload = {"group_id": group_id, "source_url": img_url, "asset_type": "image"}
asset_id = resp.json()["data"]["asset_id"]

# Step 3: 轮询等待active
resp = GET f"{base}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}"
# 重复直到 data.status == "active"

# Step 4: 用asset://格式传入
payload = {
    "model": "seedance-2",
    "prompt": "让人物手中拿着这支笔",
    "image_with_roles": [
        {"url": f"asset://{asset_id}", "role": "reference_image"}
    ]
}
```

**⚠️ 关键约束：**
- `image_urls` 和 `image_with_roles` **不能同时使用**，会报错
- `image_with_roles` 的url**必须是 `asset://` 格式**，直接传HTTP URL会报 `UnsupportedImageFormat`
- Asset上传后需要等待状态变为 `active` 才能使用

## React Flow 节点数据传递（Antoken项目）

**关键：** React Flow的节点之间不会自动传递数据。下游节点必须手动从edges读取上游数据。

```typescript
// 在节点组件中读取上游数据
const { nodes, edges } = useWorkflowStore();
const incomingEdge = edges.find(e => e.target === nodeId);
const sourceNode = incomingEdge ? nodes.find(n => n.id === incomingEdge.source) : null;
const sourceConfig = sourceNode?.data?.config as Record<string, unknown>;
const upstreamUrl = sourceConfig?.resultUrl as string;
```

**导入路径：** 项目用 `@xyflow/react`，不是 `reactflow`。
```typescript
// ✅ 正确
import { Handle, Position } from '@xyflow/react';
import type { NodeProps } from '@xyflow/react';

// ❌ 错误（会导致编译失败）
import { Handle, Position, NodeProps } from 'reactflow';
```

## CORS代理（外部媒体文件预览）

**问题：** `files.toapis.com` 生成的图片/视频URL没有CORS头，浏览器`<video>`和`<img>`标签无法跨域播放/显示。

**症状：** 任务显示"合成完成"，视频URL有效（curl可访问），但前端显示播放图标占位符，无法预览。

**验证方法：**
```bash
curl -sI "https://files.toapis.com/images/xxx.mp4" | grep -i "access-control"
# 如果没有access-control头，就是CORS问题
```

**解决方案：后端代理端点 + 前端proxyUrl工具**

后端：`GET /api/generate/proxy?url={encoded_url}` — 获取外部媒体并返回带CORS头的响应
前端：`mediaProxy.ts` 的 `proxyUrl(url)` 函数 — 自动将外部URL走代理

**⚠️ 代理端点必须返回正确的头信息，否则视频无法播放：**
```python
# 必须用 Response（不是 StreamingResponse），必须包含 Content-Length 和 Accept-Ranges
from fastapi.responses import Response
content = resp.content
return Response(
    content=content,
    media_type=content_type,
    headers={
        "Access-Control-Allow-Origin": "*",
        "Accept-Ranges": "bytes",
        "Content-Length": str(len(content)),
    },
)
```

**关键：所有显示外部媒体URL的节点都需要用proxyUrl()包装。** 包括：ImageGenNode、VideoGenNode、Img2VideoNode、VideoCompositeNode、ImageExportNode、VideoExportNode。

完整实现见 `react-flow-canvas-editor` 技能的 `references/cors-media-proxy-pattern.md`。

## 相关文件位置
- 后端模型发现: `backend/app/services/model_discovery.py`
- 后端生成API: `backend/app/api/generate.py`
- 前端设置: `frontend/src/stores/settingsStore.ts`
- 前端节点: `frontend/src/components/nodes/ImageGenNode.tsx`, `VideoGenNode.tsx`
- 前端媒体代理: `frontend/src/lib/mediaProxy.ts`
- 前端预览Modal: `frontend/src/components/PreviewModal.tsx`

## Reference Files
- `references/toapis-api-integration.md` — toapis.com API integration details
- `references/toapis-api-reference.md` — API endpoints, CORS, asset upload
- `references/seedance-2-composite-workflow.md` — seedance-2 composite workflow
- `references/video-editing-composite.md` — video editing composite patterns
- `references/asset-api-invalid-body-debug.md` — "invalid request body" error debugging guide

## 参考文件
- `references/error-source-identification.md` — 错误来源识别方法，判断错误来自 toapis.com 还是本地后端
- `references/toapis-api-integration.md` — toapis API 集成详情
- `references/toapis-api-reference.md` — toapis API 端点参考
- `references/seedance-2-composite-workflow.md` — seedance-2 素材合成流程
- `references/video-editing-composite.md` — 视频编辑合成参考

## v0.3关键修复记录

### CORS代理必须返回正确头信息
```python
# 错误：StreamingResponse没有Content-Length
return StreamingResponse(iter([resp.content]), media_type=content_type)

# 正确：Response + Content-Length + Accept-Ranges
return Response(
    content=content,
    media_type=content_type,
    headers={
        "Access-Control-Allow-Origin": "*",
        "Accept-Ranges": "bytes",
        "Content-Length": str(len(content)),
    },
)
```

### 多素材必须全部传给API
```typescript
// 错误：只传第一个素材
reference_image_url: referenceUrls[0] || undefined

// 正确：传所有素材
reference_image_urls: referenceUrls  // 数组
```

### 素材名称嵌入prompt
```typescript
// 构造带名称的prompt
const refs = referenceUrls.map((_, i) => `[素材: ${referenceNames[i]}]`).join(' ');
const fullPrompt = `${refs}\n${userPrompt}`;
```
