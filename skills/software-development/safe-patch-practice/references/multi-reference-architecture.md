# 多参考架构模式

## 问题
上游素材被简单收集为 URL 列表，没有角色区分。主流 AI 画布工具（ComfyUI、Krea.ai）都支持多参考角色。

## 解决方案

### 数据结构
```typescript
// types/workflow-v1.ts
export type ReferenceRole = 'style' | 'subject' | 'composition' | 'content';

// hooks/use-upstream-data.ts
export interface UpstreamNode {
  node: Node<NodeData>;
  edge: Edge;
  assetName: string;
  assetType?: string;
  assetUrl?: string;
  role: ReferenceRole;  // 从 edge.targetHandle 获取
}
```

### 角色含义
| 角色 | 含义 | 用途 |
|------|------|------|
| style | 风格参考 | 参考图片的风格（色彩、笔触） |
| subject | 主体参考 | 保持主体不变（人物、产品） |
| composition | 构图参考 | 参考构图（布局、角度） |
| content | 内容参考 | 通用参考（默认） |

### 前端实现
```typescript
// use-upstream-data.ts
const role = (edge.targetHandle || 'content') as ReferenceRole;
results.push({
  node: sourceNode as Node<NodeData>,
  edge,
  assetName: sourceNode.data.assetName || '素材',
  assetType: sourceNode.data.assetType,
  assetUrl: sourceNode.data.assetUrl,
  role,
});
```

### 后端 Schema
```python
class ReferenceImage(BaseModel):
    url: str
    role: str = "content"
    name: str = ""

class ImageGenerateRequest(BaseModel):
    reference_images: Optional[List[ReferenceImage]] = None
    reference_videos: Optional[List[ReferenceVideo]] = None
```

### 提示词增强
```typescript
const styleRefs = referenceImages.filter(r => r.role === 'style');
const subjectRefs = referenceImages.filter(r => r.role === 'subject');

let enhancedPrompt = prompt;
if (styleRefs.length > 0) {
  enhancedPrompt = `参考风格：${styleRefs.map(r => `[${r.name}]`).join('、')}\n${enhancedPrompt}`;
}
if (subjectRefs.length > 0) {
  enhancedPrompt = `保持主体：${subjectRefs.map(r => `[${r.name}]`).join('、')}\n${enhancedPrompt}`;
}
```

## 多 Handle 连线（P1 优化）
```tsx
// base-node.tsx - 多个输入 Handle
<Handle type="target" position={Position.Left} id="style" style={{ ...handleStyle, top: '25%' }} />
<Handle type="target" position={Position.Left} id="subject" style={{ ...handleStyle, top: '50%' }} />
<Handle type="target" position={Position.Left} id="composition" style={{ ...handleStyle, top: '75%' }} />
<Handle type="target" position={Position.Left} id="content" style={{ ...handleStyle, top: '100%' }} />
```

## 参考资料
- ComfyUI 节点系统：https://github.com/comfyanonymous/ComfyUI
- Krea.ai 多参考设计：https://krea.ai
