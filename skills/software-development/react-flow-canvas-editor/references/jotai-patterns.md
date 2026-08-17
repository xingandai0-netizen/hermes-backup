# Jotai State Management for React Flow Canvas Apps

Comprehensive guide to Jotai patterns specifically for React Flow canvas-based applications. Merged from react-jotai-refactoring, react-flow-jotai-migration, and antoken-jotai-migration.

## When to use Jotai vs Zustand

| Dimension | Jotai | Zustand |
|-----------|-------|---------|
| Model | Multiple atoms, distributed | Single store, centralized |
| Update granularity | Per-atom subscription (finer) | Whole store subscription |
| Code volume | Many small files | One large file |
| Best for | New projects, fine-grained optimization | Rapid prototyping, simple state |

**Real impact**: For small projects (<50 nodes), performance difference is negligible. Choose based on existing codebase.

## Critical Pitfall: useAtom vs useStore.get()

```tsx
// ❌ WRONG: useAtom subscribes to changes, re-renders on every viewport change
const [viewport] = useAtom(viewportAtom);

// ✅ CORRECT: useStore.get() reads on demand, no subscription
const store = useStore();
const getViewport = () => store.get(viewportAtom);

// Use in event handlers
const handleAddNode = useCallback(() => {
  const viewport = getViewport(); // Only read when needed
  // ...
}, [getViewport]);
```

**When to use useStore.get()**:
- Canvas pan/zoom (frequently changing state)
- Values only needed in event handlers
- Reads that shouldn't trigger re-renders

## atomFamily Pattern for Node-Level Subscriptions

### Problem: Global atoms cause full re-renders
```ts
// ❌ WRONG: All nodes subscribe to global nodesAtom
const nodes = useAtomValue(nodesAtom);
```

### Solution: atomFamily for precise subscriptions
```ts
// ✅ CORRECT: Each node only subscribes to its own upstream data
export const upstreamNodesAtomFamily = (nodeId: string) => {
  return atom((get) => {
    const nodes = get(nodesAtom);
    const edges = get(edgesAtom);
    
    const incomingEdges = edges.filter(e => e.target === nodeId);
    return incomingEdges.map(edge => {
      const sourceNode = nodes.find(n => n.id === edge.source);
      if (!sourceNode) return null;
      const sourceData = sourceNode.data as NodeData;
      return {
        node: sourceNode,
        edge,
        assetName: sourceData?.assetName || '素材',
        assetType: sourceData?.assetType,
        assetUrl: sourceData?.assetUrl,
      };
    }).filter(Boolean);
  });
};

// In component
const upstreamNodes = useAtomValue(upstreamNodesAtomFamily(props.id));
```

**Performance comparison**:
- ❌ `useAtom(nodesAtom)` → any node changes → ALL nodes re-render
- ✅ `useAtomValue(upstreamNodesAtomFamily(id))` → only upstream data changes → current node re-renders

**Notes**:
- `atomFamily` creates new atom instance per call; call at component top level
- Derived atoms still depend on global `nodesAtom`/`edgesAtom`, but Jotai caches derived results
- For <50 nodes, difference is negligible; for 200+ nodes, difference is significant

## UpstreamNode Typed Interface

```tsx
export interface UpstreamNode {
  node: Node<NodeData>;
  edge: Edge;
  assetName: string;
  assetType?: string;
  assetUrl?: string;
}

export const upstreamNodesAtomFamily = atomFamily((nodeId: string) =>
  atom((get): UpstreamNode[] => {
    const nodes = get(nodesAtom);
    const edges = get(edgesAtom);
    const incomingEdges = edges.filter(e => e.target === nodeId);
    const results: UpstreamNode[] = [];
    for (const edge of incomingEdges) {
      const sourceNode = nodes.find(n => n.id === edge.source);
      if (sourceNode) {
        results.push({
          node: sourceNode as Node<NodeData>,
          edge,
          assetName: sourceNode.data.assetName || '素材',
          assetType: sourceNode.data.assetType,
          assetUrl: sourceNode.data.assetUrl,
        });
      }
    }
    return results;
  })
);
```

## downstreamNodesAtomFamily (for text-node)

```tsx
export const downstreamNodesAtomFamily = (nodeId: string) => {
  return atom((get) => {
    const nodes = get(nodesAtom);
    const edges = get(edgesAtom);
    const outgoingEdges = edges.filter(e => e.source === nodeId);
    return outgoingEdges.map(edge => {
      const targetNode = nodes.find(n => n.id === edge.target);
      if (!targetNode) return null;
      const targetData = targetNode.data as NodeData;
      return {
        node: targetNode,
        edge,
        assetName: targetData?.assetName || '素材',
        assetType: targetData?.assetType,
        assetUrl: targetData?.assetUrl,
      };
    }).filter(Boolean);
  });
};
```

## nodesAtom Generic Type

```tsx
import type { NodeData } from '@/types/workflow-v1';

// ✅ CORRECT: Use generic
export const nodesAtom = atom<Node<NodeData>[]>([]);

// node.data auto-infers as NodeData
const sourceData = sourceNode.data; // Auto-typed as NodeData
```

**Note**: `applyNodeChanges` and `addEdge` return `Node[]`, need type assertion:
```tsx
set(nodesAtom, applyNodeChanges(changes, get(nodesAtom)) as Node<NodeData>[]);
```

## NodeProps Generic

```tsx
import type { NodeProps } from '@xyflow/react';
import type { NodeData } from '@/types/workflow-v1';

// ✅ CORRECT: Use NodeProps
function ImageNode(props: NodeProps<NodeData>) {
  const d = props.data; // Auto-typed as NodeData
}

export default memo(ImageNode);
```

## updateNodeDataAtom Signature

```tsx
// ❌ OLD: Dual signature, runtime type check
export const updateNodeDataAtom = atom(
  null,
  (get, set, ...args: [string, Record<string, unknown>] | [{ nodeId: string; data: Record<string, unknown> }]) => {
    if (typeof args[0] === 'string') { ... }
  }
);

// ✅ NEW: Single signature
export const updateNodeDataAtom = atom(
  null,
  (get, set, nodeId: string, data: Record<string, unknown>) => {
    set(nodesAtom, get(nodesAtom).map((n) =>
      n.id === nodeId ? { ...n, data: { ...n.data, ...data } } : n
    ));
  }
);
```

## usePollPublicUrl Hook

Polling must support interruption (AbortController):

```tsx
export function usePollPublicUrl() {
  const [, updateNodeData] = useAtom(updateNodeDataAtom);
  const abortControllerRef = useRef<AbortController | null>(null);

  const startPolling = useCallback((assetId: string, nodeId: string) => {
    if (abortControllerRef.current) abortControllerRef.current.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;

    (async () => {
      for (let i = 0; i < 30; i++) {
        if (controller.signal.aborted) return;
        await new Promise(r => setTimeout(r, 2000));
        if (controller.signal.aborted) return;
        try {
          const resp = await fetch(url, { signal: controller.signal });
          const data = await resp.json();
          if (data.ready && data.public_url) {
            updateNodeData(nodeId, { assetUrl: data.public_url });
            return;
          }
        } catch {}
      }
    })();
  }, [updateNodeData]);

  useEffect(() => {
    return () => { abortControllerRef.current?.abort(); };
  }, []);

  return startPolling;
}
```

## Polling Update Pitfall

```tsx
// ❌ WRONG: Using stale cfg closure to update config
updateNodeData(nodeId, { config: { ...cfg, assetUrl: url } });

// ✅ CORRECT: Only update top-level field, don't touch config
updateNodeData(nodeId, { assetUrl: url });
```

## useCallback Dependency Cleanup

```typescript
// ❌ cfg in dependency but not used in function body → closure trap
const updateResult = useCallback((url: string) => {
  updateNodeData(props.id, { assetUrl: url });
}, [props.id, cfg, updateNodeData]);

// ✅ Only depend on actually used values
const updateResult = useCallback((url: string) => {
  updateNodeData(props.id, { assetUrl: url });
}, [props.id, updateNodeData]);
```

## useMemo Cache Return Values

```typescript
// ❌ Returns new object every render → child re-renders
function useSettingsStore() {
  return { imageApi, videoApi, ... };
}

// ✅ useMemo cache
function useSettingsStore() {
  return useMemo(() => ({ imageApi, videoApi, ... }), [imageApi, videoApi, ...]);
}
```

## Undo Stack Limit

```tsx
const MAX_UNDO_STACK = 50;
const newStack = stack.length >= MAX_UNDO_STACK
  ? [...stack.slice(1), snapshot]
  : [...stack, snapshot];
```

## Zustand → Jotai Migration Checklist

1. Create `workflow-store-jotai.ts`, define all atoms
2. Create compatibility layer Hook (e.g., `useWorkflowStoreCompat`) or update components directly
3. Replace `useWorkflowStore()` → `useAtom(xxxAtom)` component by component
4. Remove Zustand dependency
5. Run tests to verify

## Critical: Dual State Management Conflict

PersistentCanvas uses Jotai (nodesAtom), v1 components use Zustand (useWorkflowStore) → state out of sync → nodes don't display. Must unify to one.

## selectNodeQuietly Pattern

```typescript
// Zustand: selectNodeQuietly(nodeId) — only set selectedNodeId, don't open property panel
// Jotai: Support quiet mode in selectNodeAtom, or split into two atoms
export const selectedNodeIdAtom = atom<string | null>(null);
export const propertyPanelOpenAtom = atom(false);
// selectNodeQuietly = only set selectedNodeIdAtom
// selectNode = set selectedNodeIdAtom + set propertyPanelOpenAtom(true)
```

## Testing Pattern

```typescript
import { createStore } from 'jotai';

describe('addNodeAtom', () => {
  it('should add a node', () => {
    const store = createStore();
    store.set(addNodeAtom, { id: 'test', type: 'IMAGE', data: {} });
    expect(store.get(nodesAtom)).toHaveLength(1);
  });
});

describe('upstreamNodesAtomFamily', () => {
  it('should return upstream nodes for a specific node', () => {
    const store = createStore();
    store.set(nodesAtom, [
      { id: 'node1', data: { assetName: '图素材1' } },
      { id: 'node2', data: { assetName: '视频素材1' } },
    ]);
    store.set(edgesAtom, [{ source: 'node1', target: 'node2' }]);
    const upstream = store.get(upstreamNodesAtomFamily('node2'));
    expect(upstream).toHaveLength(1);
    expect(upstream[0].assetName).toBe('图素材1');
  });
});
```

## Third-Party Code Review

After migration, have third party (DeepSeek etc.) review — they catch blind spots you miss.
