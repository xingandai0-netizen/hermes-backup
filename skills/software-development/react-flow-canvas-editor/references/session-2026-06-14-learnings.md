# Session Learnings - 2026-06-14

## Node Preview Media Proxy (CRITICAL)

External media URLs (files.toapis.com, etc.) don't have CORS headers. Browser cannot play them directly. ALL preview elements must use `proxyUrl()`:

```typescript
import { proxyUrl } from "@/lib/mediaProxy";

// Video preview
<video src={proxyUrl(previewUrl)} ... />

// Image preview
<img src={proxyUrl(previewUrl)} ... />
```

**PITFALL**: `sed` multi-line replacement often fails silently. Use `patch` tool for JSX changes, not `sed`.

## Node assetType Setting (CRITICAL for Connection Workflow)

When nodes generate content, they MUST set `assetType` in `updateNodeData` so downstream nodes can detect the type:

```typescript
const updateResult = useCallback((url: string, assetId: string) => {
  updateNodeData(props.id, {
    status: "success",
    assetType: "VIDEO" as const,  // or "IMAGE"
    assetUrl: url,
    assetId,
    config: { ...cfg, assetUrl: url, assetId },
  });
}, [...]);
```

Without this, connection-based workflow (upstream→downstream素材传递) won't work because `getUpstreamAssets()` can't detect asset types.

## Connection Validation: No Type Restrictions

**User preference**: Connection validation should be like TapNow - NO type restrictions. Allow all connections. Only block self-connection.

```typescript
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  // No type validation - allow all connections
  get().saveSnapshot();
  set((s) => ({
    edges: addEdge({ ...connection, animated: true, style: { stroke: "#ffffff" }, type: "smoothstep" }, s.edges),
  }));
},
```

## CSS !important Overrides Inline Styles

**PITFALL**: React Flow edge colors set via `style={{ stroke: "#5e6ad2" }}` are OVERRIDDEN by CSS `!important` rules. Must update BOTH:
1. Component inline styles in `onConnect`
2. CSS global styles in `globals.css`

```css
.react-flow__edge-path {
  stroke: #ffffff !important;  /* This overrides inline styles */
}
```

## DAG Execution Engine Pattern

For workflow editors that need parallel node execution:

```python
# backend/app/services/dag_engine.py
class DAGExecutor:
    def get_execution_levels(self) -> List[List[str]]:
        """Topological sort + level grouping for parallel execution"""
        # Kahn's algorithm grouped by level
        
    async def execute(self, executor_func, concurrency=3):
        """Execute DAG level by level, nodes within level in parallel"""
        for level in levels:
            await asyncio.gather(*[self.execute_node(nid, executor_func) for nid in level])
```

## write_file Line Number Corruption

**PITFALL**: `read_file` returns content with line numbers (e.g., `1|content`). If this output is passed to `write_file`, the file gets corrupted with line numbers embedded. Always strip line numbers before writing, or use `patch` tool instead.

```python
# Wrong: read_file output has line numbers
content = read_file("path.tsx")["content"]  # "1|\"use client\";\n2|..."
write_file("path.tsx", content)  # CORRUPTS FILE

# Correct: strip line numbers
lines = content.split("\n")
fixed = [line.split("|", 2)[2] if "|" in line else line for line in lines]
write_file("path.tsx", "\n".join(fixed))

# Better: just use patch tool
```
