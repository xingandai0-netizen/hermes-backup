# Antoken Architecture Audit (2026-06-14 Updated)

## Edge Color Management (CRITICAL)

### Problem: CSS !important overrides inline styles
When changing edge colors, MUST update BOTH places:
1. `frontend/src/styles/globals.css` - `.react-flow__edge-path { stroke: #xxx !important; }`
2. `frontend/src/stores/workflowStore.ts` - `onConnect` handler `style: { stroke: "#xxx" }`
3. `frontend/src/components/canvas/WorkflowCanvas.tsx` - `defaultEdgeOptions` and `connectionLineStyle`

**Lesson learned:** Only changing inline styles doesn't work because CSS `!important` overrides them.

### Current edge color: `#ffffff` (white)
```css
/* globals.css */
.react-flow__edge-path {
  stroke: #ffffff !important;
  stroke-width: 2 !important;
}
.react-flow__edge.animated .react-flow__edge-path {
  stroke: #ffffff !important;
}
.react-flow__edge:hover .react-flow__edge-path {
  stroke: #cccccc !important; /* slightly dimmer on hover */
}
```

## assetType Storage Location (CRITICAL BUG FIX)

### Problem: Inconsistent storage location
- **VideoNode/ImageNode/CompositeNode** store `assetType` at `node.data` level:
  ```typescript
  updateNodeData(props.id, {
    status: "success",
    assetType: "VIDEO" as const,  // ← data level
    assetUrl: url,
    config: { ...cfg, assetUrl: url }
  });
  ```

- **Downstream nodes** must read from `node.data.assetType`, NOT `config.assetType`:
  ```typescript
  // CORRECT
  const sourceData = sourceNode.data as unknown as NodeData;
  const assetType = sourceData?.assetType || sourceConfig?.assetType;
  
  // WRONG - will miss the type
  const assetType = sourceConfig?.assetType;
  ```

### Fix: Always check both locations
```typescript
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

## Video-to-Image Workflow (CRITICAL)

### Problem: API doesn't accept base64 images
When passing video reference for image generation:
1. ~~Extract first frame → base64 → pass to API~~ (FAILS: "base64 image not allowed")
2. ~~Extract frame → save locally → serve via proxy → pass URL~~ (FAILS: localhost not accessible from external API)
3. **CORRECT: Pass video URL directly to API** - API handles video-to-image internally

### Working implementation:
```python
# backend/app/api/generate.py
if req.reference_video_url:
    # Direct pass - API handles video-to-image
    payload["image_urls"] = [req.reference_video_url]
```

### VideoNode must pass upstream assets:
```typescript
const upstream = getUpstreamAssets();
const resp = await fetch("http://localhost:8000/api/generate/video", {
  method: "POST",
  body: JSON.stringify({
    prompt,
    api_url: videoApi.apiUrl,
    api_key: videoApi.apiKey,
    model,
    resolution: size,
    reference_image_url: upstream.image?.url || undefined,
    reference_video_url: upstream.video?.url || undefined,
  }),
});
```

## Connection Validation Approach

### TapNow approach: Allow all connections
TapNow does NOT restrict connections by type. Users can connect any node to any node.
Only self-connection is blocked.

### Implementation:
```typescript
onConnect: (connection) => {
  // Only block self-connection
  if (connection.source === connection.target) return;
  
  // Allow all other connections (no type validation)
  get().saveSnapshot();
  set((s) => {
    const updated = addEdge({
      ...connection,
      animated: false,
      style: { stroke: "#ffffff", strokeWidth: 2 },
      type: "smoothstep",
    }, s.edges);
    return { edges: updated };
  });
},
```

## Performance Pitfalls (2026-06-14) ⚠️ CRITICAL LESSONS

### 1. onlyRenderVisibleElements FREEZES the page
```tsx
// ❌ CAUSES FREEZING - page becomes completely unresponsive
<ReactFlow onlyRenderVisibleElements={true} />

// ✅ SAFE - don't use this option
<ReactFlow />
```

### 2. deleteKeyCode={null} and elevateNodesOnSelect={false} BREAK clicks
These options may seem harmless but can make the entire page unresponsive to clicks.
```tsx
// ❌ BREAKS click handling
<ReactFlow deleteKeyCode={null} elevateNodesOnSelect={false} />

// ✅ SAFE - use defaults
<ReactFlow />
```

### 3. React.memo wrapper syntax is FRAGILE
When adding memo to node components, the closing bracket must be EXACT:
```tsx
// ❌ WRONG - syntax error
const VideoNode = React.memo(function VideoNode(props: NodeProps) {
  // ...
}
export default VideoNode;

// ❌ ALSO WRONG - puts export on same line as });
});export default VideoNode;

// ✅ CORRECT
const VideoNode = React.memo(function VideoNode(props: NodeProps) {
  // ...
});
export default VideoNode;
```

**Rule:** If memo causes ANY issues, IMMEDIATELY revert to `export default function` pattern.
The performance gain is minimal compared to the risk of breaking the UI.

### 4. Adding CSS with !important BREAKS the layout
```css
/* ❌ BREAKS everything - interferes with React Flow internals */
.react-flow {
  width: 100% !important;
  height: 100% !important;
}

/* ✅ SAFE - don't override React Flow's internal CSS */
```

**Rule:** NEVER add CSS that overrides React Flow's internal styles.
React Flow manages its own dimensions. External overrides cause layout collapse.

### 5. When optimization breaks UI, REVERT IMMEDIATELY
```bash
# Revert specific files to last known good commit
git checkout <commit-hash> -- frontend/src/components/canvas/WorkflowCanvas.tsx
git checkout <commit-hash> -- frontend/src/components/nodes/*.tsx
git checkout <commit-hash> -- frontend/src/styles/globals.css
```

**Lesson learned (2026-06-14):** Performance optimizations that seem safe can completely
break the UI. Always test each optimization individually. If the page freezes or becomes
unresponsive, revert immediately - don't try to "fix forward".

### 6. snapToGrid must be a state variable for toggling
```tsx
// ✅ CORRECT - state variable for toggle
const [snapToGrid, setSnapToGrid] = useState(true);
<ReactFlow snapToGrid={snapToGrid} />

// ❌ WRONG - hardcoded, can't toggle
<ReactFlow snapToGrid />
```

## DAG Execution Engine (2026-06-14)

### New: Workflow execution with parallel node processing
```typescript
// frontend/src/hooks/useWorkflowExecution.ts
const { executeWorkflow, executeNode } = useWorkflowExecution();

// Execute entire workflow with DAG engine
await executeWorkflow({
  concurrency: 3,
  onComplete: (results) => console.log("Done", results),
  onError: (error) => console.error("Failed", error)
});
```

### Backend: WebSocket real-time progress
```python
# backend/app/api/ws.py
@router.websocket("/ws/workflow/{workflow_id}")
async def ws_workflow_progress(websocket: WebSocket, workflow_id: str):
    # Real-time progress updates
```

## Proxy Configuration

### All domains allowed in development
```python
# backend/app/api/generate.py
# Domain whitelist disabled for development
# if parsed.hostname not in allowed_domains:
#     raise HTTPException(403, f"Domain not allowed: {parsed.hostname}")
```

### CORS headers required for video preview
```python
return Response(
    content=content,
    media_type=content_type,
    headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
        "Access-Control-Allow-Headers": "*",
        "Accept-Ranges": "bytes",
        "Content-Length": str(len(content)),
    },
)
```

## Snap-to-Grid Toggle (2026-06-14)

Added toggle button for canvas grid snapping:
```tsx
const [snapToGrid, setSnapToGrid] = useState(true);

<ReactFlow
  snapToGrid={snapToGrid}
  snapGrid={[16, 16]}
  // ... other props
/>

// Toggle button in UI
<button onClick={() => setSnapToGrid(!snapToGrid)}>
  SN
</button>
```
