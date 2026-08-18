# Jotai atomFamily 性能优化模式

## 问题
节点组件通过 `useAtom(nodesAtom)` 订阅全局状态，导致任意节点变化时所有节点重渲染。

## 解决方案：atomFamily

### 基本用法
```typescript
import { atom } from 'jotai';
import { atomFamily } from 'jotai/utils';

// 为每个节点创建独立的派生原子
export const upstreamNodesAtomFamily = atomFamily((nodeId: string) =>
  atom((get) => {
    const nodes = get(nodesAtom);
    const edges = get(edgesAtom);
    
    const incomingEdges = edges.filter(e => e.target === nodeId);
    return incomingEdges.map(edge => {
      const sourceNode = nodes.find(n => n.id === edge.source);
      if (!sourceNode) return null;
      return {
        node: sourceNode,
        edge,
        assetName: sourceNode.data.assetName || '素材',
        assetType: sourceNode.data.assetType,
        assetUrl: sourceNode.data.assetUrl,
        role: (edge.targetHandle || 'content') as ReferenceRole,
      };
    }).filter(Boolean);
  })
);
```

### 组件使用
```typescript
import { useAtomValue } from 'jotai';

function ImageNode(props: NodeProps) {
  // 只订阅当前节点的上游数据
  const upstreamNodes = useAtomValue(upstreamNodesAtomFamily(props.id));
  const mentions = useAtomValue(mentionsAtomFamily(props.id));
  
  // 不再订阅全局 nodesAtom/edgesAtom
}
```

### 性能对比
| 方式 | 任意节点变化时 | 10个节点 |
|------|--------------|---------|
| useAtom(nodesAtom) | 所有节点重渲染 | 10次渲染 |
| atomFamily | 只有相关节点重渲染 | 1-2次渲染 |

### 关键点
1. **atomFamily 内部仍读取全局 atoms**，但 Jotai 的派生原子只有当结果变化时才触发重渲染
2. **节点 A 的数据变化不会触发节点 B 的上游数据重算**（因为结果不同）
3. **使用 `useAtomValue` 而不是 `useAtom`**（只读，不需要 setter）

### NodeData 类型安全
```typescript
// nodesAtom 使用 Node<NodeData> 泛型
export const nodesAtom = atom<Node<NodeData>[]>([]);

// 这样 node.data 自动推断为 NodeData，不需要 as NodeData 断言
```

### 参考
- Jotai atomFamily 文档：https://jotai.org/docs/utilities/atom-family
- React Flow 性能优化：https://reactflow.dev/learn/troubleshooting/performance
