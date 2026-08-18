# 素材自动命名 + @提及系统

## 自动命名规则

每个素材节点创建时自动命名，按类型递增编号：
- 图片节点：图素材1、图素材2、图素材3...
- 视频节点：视频素材1、视频素材2、视频素材3...

### 计数器实现（重要：使用全局window变量）

**错误做法（模块级let变量）：**
```typescript
// ❌ HMR时会重置，导致所有素材都叫"图素材1"
let imageCounter = 0;
let videoCounter = 0;
```

**正确做法（全局window变量）：**
```typescript
// ✅ 跨HMR保持状态
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

### 名称存储

名称存储在节点数据中：
```typescript
const newNode = {
  data: {
    assetName: getAssetName(def.type),
    // ...
  }
};
```

cfg类型定义必须包含assetName：
```typescript
const cfg = d.config as {
  content?: string;
  model?: string;
  assetName?: string;  // 必须加
  // ...
};
```

## 素材名称标签

**位置：在预览区外面（左上角），不是里面！**

```tsx
{/* 素材名称标签 - 在预览区外面 */}
<div style={{
  display: "flex",
  alignItems: "center",
  gap: 4,
  padding: "4px 8px 4px 4px",
  marginBottom: 4,
}}>
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="2">
    {/* 图片用 rect+circle+polyline, 视频用 polygon play */}
    <polygon points="5 3 19 12 5 21 5 3" />
  </svg>
  <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>
    {cfg.assetName || "素材"}
  </span>
</div>

{/* 预览区在下面 */}
<div style={{ ... }}>
  <VideoPreview ... />
</div>
```

## @提及输入组件

文件：`frontend/src/components/MentionInput.tsx`

### 功能
- 输入@弹出素材列表
- 键盘导航：↑↓箭头、回车选择、ESC关闭
- 按类型显示不同图标（图片/视频）
- 选择后自动插入 `@素材名 `

### 使用方式

```tsx
import MentionInput from "@/components/MentionInput";

// 收集上游素材名称
const getUpstreamMentions = useCallback(() => {
  const incomingEdges = edges.filter(e => e.target === props.id);
  const mentions: Array<{ id: string; name: string; type: 'image' | 'video' }> = [];
  
  for (const edge of incomingEdges) {
    const sourceNode = nodes.find(n => n.id === edge.source);
    if (!sourceNode) continue;
    const sourceData = sourceNode.data as unknown as NodeData;
    const assetName = sourceData?.assetName || "素材";
    
    if (sourceData?.assetType === "IMAGE") {
      mentions.push({ id: assetName, name: assetName, type: 'image' });
    } else if (sourceData?.assetType === "VIDEO") {
      mentions.push({ id: assetName, name: assetName, type: 'video' });
    }
  }
  
  return mentions;
}, [edges, nodes, props.id]);

const upstreamMentions = getUpstreamMentions();

// 在控制面板中使用
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={upstreamMentions}
  placeholder="输入@引用素材，如：@图素材1中的什么替换成@视频素材1中的什么"
  disabled={loading}
/>
```

### 实现细节

MentionInput组件内部：
1. 监听textarea的input事件
2. 检测光标前是否有@符号
3. 如果有，显示素材列表菜单
4. 选择后替换@及其后的文本为 `@素材名 `
5. 支持键盘导航和过滤

## 提示词示例

```
@图素材1 中的首饰替换成 @视频素材1 中的穿搭
```

生成时自动转换为：
```
[图片素材: 图素材1] [视频素材: 视频素材1]
@图素材1 中的首饰替换成 @视频素材1 中的穿搭
```
