# React Flow Handle 重复定义问题

## 问题描述

当使用 BaseNode 组件根据 `inputs`/`outputs` 数组自动渲染 Handle 时，子节点组件**不应该再手动添加 Handle 组件**，否则每个端口会出现两个圆点。

## 错误模式

```tsx
// BaseNode 已经根据 d.inputs 自动渲染了 Handle
// 但子节点又手动加了一遍：

// BaseNode 自动渲染（正确）：
{d.inputs.map((port) => (
  <Handle type="target" id={port.id} ... />
))}

// 子节点手动添加（重复！）：
<Handle type="target" position={Position.Left} id="image"
  className="w-3 h-3 bg-blue-500 ..." style={{ left: -6 }} />
<Handle type="source" position={Position.Right} id="image"
  className="w-3 h-3 bg-blue-500 ..." style={{ right: -6 }} />
```

**结果：** 每个端口出现两个连接点，用户体验混乱。

## 正确做法

如果 BaseNode 已经根据 `inputs`/`outputs` 渲染 Handle，子节点**不要**再手动添加 Handle：

```tsx
// VideoCompositeNode - 不需要 Handle
export default function VideoCompositeNode({ id, data, selected }: NodeProps) {
  return (
    <BaseNode data={data} selected={selected} color="#a855f7">
      {/* 只放自定义内容，Handle 由 BaseNode 统一管理 */}
      <div>...</div>
    </BaseNode>
  );
}
```

## 何时需要手动 Handle

只有当节点的 Handle 不在 `inputs`/`outputs` 数组中时才需要手动添加。例如：
- 动态端口（运行时才知道有几个）
- 非标准位置的端口
- 特殊样式的端口

## Antoken 项目实例

在 Antoken 中，3 个合成节点（VideoCompositeNode、ImageExportNode、VideoExportNode）都有此问题：

**修复前：** 每个节点有 4-6 个 Handle（BaseNode 渲染的 + 手动添加的）
**修复后：** 删除手动 Handle，只保留 BaseNode 自动渲染的

同时需要删除不再使用的 `import { Handle, Position }` 导入。

## React Flow 导入路径注意

项目使用 `@xyflow/react`，不是 `reactflow`：

```typescript
// ✅ 正确
import type { NodeProps } from '@xyflow/react';

// ❌ 错误（会导致编译失败 Module not found）
import type { NodeProps } from 'reactflow';
```
