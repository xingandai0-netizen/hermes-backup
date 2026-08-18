# Performance Pitfalls - Critical Learnings (2026-06-14)

## CRITICAL: Options that FREEZE the page

### onlyRenderVisibleElements={true}
```tsx
// ❌ CAUSES COMPLETE FREEZING - DO NOT USE
<ReactFlow onlyRenderVisibleElements={true} />

// ✅ SAFE - omit this option entirely
<ReactFlow />
```
**Severity:** Page becomes completely unresponsive. No click events fire. Requires hard refresh.
**Root cause:** ReactFlow's visibility calculation conflicts with certain node configurations.

### elevateNodesOnSelect={false} + deleteKeyCode={null}
```tsx
// ❌ CAUSES CLICK UNRESPONSIVENESS
<ReactFlow elevateNodesOnSelect={false} deleteKeyCode={null} />

// ✅ SAFE - use defaults
<ReactFlow />
```
**Severity:** Nodes become unclickable. Canvas events stop firing.

## CRITICAL: React.memo on node components

### Problem
```tsx
// ❌ DANGEROUS - can break ReactFlow event handling
const VideoNode = React.memo(function VideoNode(props: NodeProps) { ... });
export default VideoNode;
```

**Symptoms:**
- Page loads but clicks don't work
- Nodes render but can't be selected
- Canvas pan/zoom works but node interactions fail

**Root cause:** React.memo's comparison function may prevent necessary re-renders for canvas interactions. ReactFlow relies on specific re-render patterns for event handling.

### Solution
```tsx
// ✅ SAFE - use function export
export default function VideoNode(props: NodeProps) { ... }
```

**Rule:** DO NOT use React.memo on ReactFlow node components unless absolutely necessary for performance. If you must use it, ensure the memo comparison function accounts for ReactFlow's internal state changes.

## CRITICAL: CSS conflicts with Tailwind

### Problem
Adding CSS with `!important` or overriding Tailwind utility classes can break the entire layout.

```css
/* ❌ BAD - conflicts with Tailwind's flex-1 */
.flex-1 {
  flex: 1 1 0%;
  min-height: 0;
}

/* ❌ BAD - conflicts with Tailwind's h-screen */
.h-screen {
  height: 100vh;
  height: 100dvh;
}
```

### Solution
```css
/* ✅ SAFE - only override ReactFlow-specific styles */
.react-flow {
  width: 100% !important;
  height: 100% !important;
}

/* ✅ SAFE - use Tailwind classes in JSX instead */
<div className="flex-1 min-h-0">
```

**Rule:** Never add CSS that overrides Tailwind utility classes. Use Tailwind classes in JSX instead.

## Safe ReactFlow Configuration (PROVEN STABLE)

```tsx
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
    animated: false,  // Disable for performance
    style: { stroke: "#ffffff", strokeWidth: 2 },
    type: "smoothstep",
  }}
  proOptions={{ hideAttribution: true }}
  minZoom={0.2}
  maxZoom={3}
  defaultViewport={{ x: 0, y: 0, zoom: 1 }}
  // DO NOT ADD: onlyRenderVisibleElements, elevateNodesOnSelect, deleteKeyCode
/>
```

## Debugging Frozen/Unresponsive Page

If page becomes unresponsive:
1. Check for `onlyRenderVisibleElements={true}` - REMOVE IT
2. Check for `elevateNodesOnSelect={false}` - REMOVE IT
3. Check for `deleteKeyCode={null}` - REMOVE IT
4. Check if node components use `React.memo` - REVERT to function export
5. Check globals.css for `!important` overrides conflicting with Tailwind
6. Hard refresh: `Cmd+Shift+R`

## Edge Animation Performance

```tsx
// ❌ BAD - all edges animated (expensive with 10+ edges)
defaultEdgeOptions={{ animated: true }}

// ✅ GOOD - disable animation by default
defaultEdgeOptions={{ animated: false }}
```

**Rule:** Only animate edges that are actively processing (connected to running nodes).
