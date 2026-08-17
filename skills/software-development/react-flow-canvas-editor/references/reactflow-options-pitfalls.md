# ReactFlow Options Pitfalls (2026-06-14)

## Options That CAUSE FREEZING

```typescript
// ❌ CAUSES PAGE FREEZE — do not use
onlyRenderVisibleElements={true}
```
Caused entire page to become unresponsive. Canvas renders but no clicks or interactions work.

## Options That BREAK CLICK INTERACTIONS

```typescript
// ❌ BREAKS CLICKS — nodes become unresponsive
elevateNodesOnSelect={false}
deleteKeyCode={null}
```
These two options together caused the canvas to stop responding to clicks entirely. Page loads but clicking on nodes, edges, or canvas had no effect.

## Safe ReactFlow Configuration

```typescript
<ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={onConnect}
  nodeTypes={nodeTypes}
  fitView
  snapToGrid
  snapGrid={[16, 16]}
  defaultEdgeOptions={{
    animated: false,  // animated: true causes performance issues
    style: { stroke: "#ffffff", strokeWidth: 2, strokeOpacity: 0.6 },
    type: "smoothstep",
  }}
  proOptions={{ hideAttribution: true }}
  minZoom={0.2}
  maxZoom={3}
  defaultViewport={{ x: 0, y: 0, zoom: 1 }}
/>
```

## Key Rules
1. **NEVER batch multiple ReactFlow config changes** — test each one individually
2. **animated: true on edges** causes performance issues with many edges
3. **onlyRenderVisibleElements** has bugs in some versions — avoid
4. **deleteKeyCode={null}** can break keyboard event handling
5. Always test click interactions after changing ReactFlow options
