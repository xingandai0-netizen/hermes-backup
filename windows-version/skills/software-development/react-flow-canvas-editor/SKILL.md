---
name: react-flow-canvas-editor
description: "Build canvas-based workflow editors with React Flow v12 + Next.js 14 + Zustand + Tailwind CSS. Covers TypeScript pitfalls, drag-and-drop, dark themes, node systems, execution engines, CSS/JS safety patterns, and Antoken-specific development workflows."
version: 1.13.0
author: xiaohei
triggers:
  - react flow
  - canvas editor
  - workflow editor
  - node editor
  - 画布编辑器
  - 工作流编辑器
  - reactflow
  - xyflow
---

# React Flow Canvas Editor

Build production-grade infinite canvas workflow editors using React Flow v12, Next.js 14 (App Router), Zustand, and Tailwind CSS.

## Jotai State Management

For Jotai patterns specific to React Flow canvas apps (atomFamily, useUpstreamData, usePollPublicUrl, Zustand→Jotai migration), see [references/jotai-patterns.md](references/jotai-patterns.md).

## Antoken v2 Production Architecture

For a complete case study of a production React Flow + Jotai + FastAPI + Supabase app (deployment, security, API integration, code review workflow), see [references/antoken-v2-architecture.md](references/antoken-v2-architecture.md).

## References

- **`references/antoken-project-structure.md`** — Complete Antoken project structure, node definitions, port colors, CSS variables.
- **`references/antoken-ui-conventions.md`** — Antoken UI conventions, design tokens, component patterns.
- **`references/api-proxy-model-aliasing.md`** — API proxy model aliasing, multi-endpoint retry.
- **`references/multi-edge-handle-patterns.md`** — Multiple edges to same target handle, upstream asset collection.
- **`references/reactflow-performance-optimization.md`** — Edge highlighting O(n²)→O(n), viewport throttling, node re-render avoidance.
- **`references/asset-upload-path-analysis.md`** — Three upload paths, URL field mismatches, LAN URL → toapis.com flow.
- **`references/toapis-asset-upload-pattern.md`** — Frontend direct upload to toapis.com, double upload pattern, asset:// prefix.
- **`references/toapis-api-reference.md`** — toapis.com API endpoints, CORS, asset upload, direct frontend connection.
- **`references/video-preview-patterns.md`** — Hover-to-play, control panel, fullscreen preview, asset name labels.
- **`references/mention-input-pattern.md`** — @ mention input component with autocomplete.
- **`references/toapis-api-reference.md`** — toapis.com API endpoints, CORS support, asset upload flow.
- **`references/canvas-context-menu-and-file-drop.md`** — Right-click canvas menu, drag-and-drop file upload patterns.
- **`references/sidebar-import-material-pattern.md`** — Sidebar "导入素材" implementation: file input, upload, node creation.
- **`references/dialog-interaction-patterns.md`** — Dialog click propagation, mouse wheel scroll isolation, overflow clipping fix, double-click handler, right-click context menu patterns.
- **`references/lan-access-and-file-upload.md`** — LAN access (CORS, dynamic API base, WebSocket), local file upload flow, canvas context menu, drag-and-drop assets.
- **`references/asset-upload-field-mapping.md`** — Backend /api/upload returns `path` not `url`, correct concatenation pattern, API_BASE module-level init trap.
- **`references/lan-url-upload-open-issue.md`** — UNRESOLVED: LAN computer uploads fail with "invalid request body" from toapis.com. Debug steps and possible causes.
- **`references/lan-deployment-and-file-upload.md`** — LAN access (dynamic API URL, CORS), local file upload flow, data URL conversion for external APIs.
- **`references/canvas-context-menu-and-file-drop.md`** — Right-click canvas menu, file drag-drop, hidden file input, createAssetNode helper.
- **`references/local-asset-handling.md`** — isLocalAsset flag, objectFit contain vs cover, original metadata extraction, cfg type updates.
- **`references/dynamic-api-base-for-lan.md`** — Replace hardcoded localhost with dynamic hostname for LAN access, WebSocket protocol detection.

## ⚠️ ARCHITECTURE RULES

### API calls: Backend proxy
ALL generation/polling API calls go through backend proxy: `Browser → Backend → toapis.com`. "Frontend direct connection for ALL API calls" was tried and rejected (阿戴: "这是废案").

### Asset upload: Backend uploads to public hosting (2026-06-27 verified)

**Core finding**: toapis.com ALL APIs (Asset + Generation) ONLY accept publicly accessible HTTP/HTTPS URLs.
- ❌ Binary upload → `invalid request body`
- ❌ Data URL → `base64 image is not allowed`
- ❌ LAN URL → toapis.com can't access

**Solution**: Backend uploads files to tmpfiles.org (with proxy) to get public URLs. Frontend stores public URL as `assetUrl`.

See `references/toapis-api-reference.md` for full details.

---

## Core Patterns

### Control Panel Scaling with Viewport Zoom (2026-06-27)
When canvas is zoomed out, control panels become too small. Use `1/zoom` to keep them the same visual size:
```typescript
const { viewport } = useWorkflowStore();
const controlScale = 1 / viewport.zoom;
// Apply to control panel div:
style={{ transform: `scale(${controlScale})`, transformOrigin: "top left" }}
```
Apply to both VideoNode and ImageNode control panels. The old formula `1 + (1-zoom)*0.3` was too subtle.

### Full-Screen Preview Button Must Have onClick (2026-06-27)
The expand button (square-with-corners SVG) in control panels was missing onClick. Always bind:
```typescript
<button onClick={() => previewUrl && setShowPreview(true)} ...>
```

### Edge Highlighting Performance (2026-06-27)
Recursive `getDownstreamNodes` called per-edge per-render = O(n²). Fix with `useMemo` + BFS:
```typescript
const highlightedEdgeIds = useMemo(() => {
  if (!selectedNodeId) return new Set<string>();
  const ids = new Set<string>();
  const downstream = new Set<string>();
  const queue = [selectedNodeId];
  while (queue.length > 0) {
    const nid = queue.shift()!;
    for (const e of edges) {
      if (e.source === nid && !downstream.has(e.target)) {
        downstream.add(e.target);
        queue.push(e.target);
      }
    }
  }
  for (const e of edges) {
    if (e.source === selectedNodeId || e.target === selectedNodeId ||
        downstream.has(e.source) || downstream.has(e.target)) {
      ids.add(e.id);
    }
  }
  return ids;
}, [selectedNodeId, edges]);

// Then in render:
edges={edges.map(edge => ({
  ...edge,
  style: { ...edge.style, stroke: highlightedEdgeIds.has(edge.id) ? "#ffffff" : "rgba(255,255,255,0.2)" },
}))}
```

### Node System
- Each node type = separate component extending `BaseNode`
- Node data stored in `node.data` (not `node.data.config`)
- Use `nodeType` for type checks, not `assetType`

### Edge System
- Use unique edge IDs with timestamp+random for multi-target connections
- Don't use `addEdge` for multi-target - append directly to array with `[...s.edges, newEdge]`
- Filter edges by `e.target === props.id` for upstream collection
- `onEdgesChange` must ONLY process `select` type (filter out `remove` and `replace`)
- Separate `removeEdge` function for user-initiated deletion via context menu
- `ConnectionMode.Loose` required for multiple incoming edges to same handle

### Video Preview
- Hover to play, leave to pause and reset
- Don't use `stopPropagation` on main container (blocks node selection)
- Use `onExpand` prop for fullscreen button
- Show asset name label outside preview area

### @ Mention Input
- Detect @ before cursor position
- Show default mentions when no upstream assets
- Position menu above input
- Support keyboard navigation (arrows + enter + escape)

### LAN Deployment
- **Never hardcode localhost** — use `getApiBase()` from `src/lib/api.ts` that reads `window.location.hostname`
- **CORS** — backend must set `CORS_ORIGINS = ["*"]` for LAN access
- **Backend proxies ALL API calls** — frontend never calls toapis.com directly
- **LAN URL format**: `http://<host-ip>:3000` (frontend), `http://<host-ip>:8000` (backend)
- See `references/dynamic-api-base-for-lan.md` for full patterns

### Local File Upload (BROKEN - toapis.com 限制)

**关键发现（2026-06-27 实测）：toapis.com 只接受公开可访问的 HTTP/HTTPS URL，所有其他格式均被拒绝。**

已验证失败的上传方式：
- LAN URL (`http://192.168.x.x`) → `invalid request body`
- Data URL (`data:image/png;base64,...`) → `invalid request body`
- Base64 in `image_urls` 字段 → `base64 image is not allowed`
- Multipart binary upload to Asset API → `invalid request body`

**结果：导入/拖拽的本地文件无法作为上游素材生成。需要先上传到公开 CDN 获取公开 URL。**

AI 生成的素材可以正常使用（结果存在 toapis.com CDN，公开可访问）。

详见 `references/toapis-api-limitations.md`。

### LAN Access (Dynamic API Base)
- NEVER hardcode `http://localhost:8000` in fetch calls
- Use `getApiBase()` from `src/lib/api.ts` that reads `window.location.hostname`
- Backend port is fixed at 8000, frontend at 3000
- Also handle WebSocket: detect `https:` → `wss:`, `http:` → `ws:`
- See `references/dynamic-api-base-for-lan.md` for migration checklist

## User Preferences (阿戴)

1. **Don't modify working logic** - Ask before changing backend/API code
2. **Test before claiming done** - "没完成不要说完成"
3. **No incremental patching** - Understand complete logic first, fix all at once
4. **High design standards** - Linear/Vercel dark theme, no emoji, CSS icons
5. **No AI hallucination** - Every feature must be actually tested
6. **Node highlight colors** - Gray tones, NOT purple/blue/green. No glow effects on selection.
7. **Backup before risky changes** - `git commit` current state before refactoring; revert if unhappy
8. **Research before coding** - Check API docs, existing code patterns, skill references FIRST
9. **Delete key safety** - Never delete nodes when focus is in input/textarea (any content)
10. **Don't break working things** - "改东西不要瞎改不要让原本好好的地方不能运行" — verify server is ready, test before telling user to refresh, never assume something works without checking
11. **Investigate before changing** - "你先检查先不要乱改" — when user reports a bug, check logs and trace the code path FIRST. Don't propose architecture changes before understanding the root cause. The simplest fix is usually correct.
12. **Don't pollute memory with dead ends** - If an approach is abandoned (废案), clean up ALL references to it in memory. Otherwise future sessions will re-propose the same dead end.
13. **Git backup before major changes** - Always commit current state before refactoring. User explicitly asks "先备份现在的版本后再进行本次修改". Use descriptive commit messages so `git reset --hard <hash>` works for rollback.
14. **Don't overcomplicate** - When user says "你搞复杂了", they mean the solution is simpler than what was built. Step back and think about the simplest approach before building complex workarounds.
15. **Don't change upstream asset connection logic** - "不要改上传上游素材逻辑" — `getUpstreamAssets` and how `reference_image_urls`/`reference_video_urls` are constructed should NOT be modified. The `asset://` prefix approach works by having `assetUrl` already contain the correct format.

## 异步上传模式（2026-06-27）

文件上传需要两步（本地存储 + 公开 URL），但不能阻塞 UI：

```typescript
// 1. 上传到后端（立即返回本地 URL）
const uploadResult = await uploadToBackend(file);
// 2. 立即创建节点（本地 URL 用于预览）
createAssetNode(type, uploadResult.localUrl, ...);
// 3. 后台轮询公开 URL，完成后自动更新节点
pollPublicUrl(uploadResult.assetId, nodeId);
```

详见 `references/toapis-file-upload-limits.md`

### Viewport onMove Throttling (2026-06-27)
`onMove` fires on every pixel of pan/zoom. Updating store on every event triggers full re-render of all viewport-dependent components. Fix with rAF throttle:

```typescript
const moveTimerRef = useRef<number | null>(null);

const onMove = useCallback((_: any, vp: { x: number; y: number; zoom: number }) => {
  if (moveTimerRef.current) return;
  moveTimerRef.current = requestAnimationFrame(() => {
    updateViewport(vp);
    setZoomLevel(Math.round(vp.zoom * 100));  // sync zoom display here
    moveTimerRef.current = null;
  });
}, [updateViewport]);
```

### Zoom Display Must Update from onMove (2026-06-29)

**Problem**: Zoom percentage display stuck at initial value (e.g. 120%) and doesn't update when zooming.

**Root cause**: Using `setTimeout(() => setZoomLevel(Math.round(getZoom() * 100)), 100)` in button click handlers. `getZoom()` returns stale values, and this doesn't capture scroll/pinch zoom at all.

**Fix**: Update `zoomLevel` in the `onMove` callback (see above). Remove all `setTimeout + getZoom()` from button handlers:

```tsx
// ❌ Broken: stale getZoom, only fires on button click
<button onClick={() => { zoomIn(); setTimeout(() => setZoomLevel(Math.round(getZoom() * 100)), 100); }}>

// ✅ Correct: onMove handles ALL zoom sources (buttons, scroll, pinch, fitView)
<button onClick={() => zoomIn()}>
// setZoomLevel is called in onMove callback with vp.zoom
```

### ReactFlow `fitView` Prop Causes Zoom Jump (2026-06-29)

**Problem**: Adding the first node causes canvas zoom to jump from 70% to ~300%.

**Root cause**: `<ReactFlow fitView>` boolean prop auto-adjusts viewport to fit all nodes whenever nodes change. With a single node, it zooms in to fill the viewport.

**Fix**: Remove `fitView` prop. Use `defaultViewport` for initial zoom. Users can manually trigger fitView via the "适应画布" button:

```tsx
// ❌ Causes zoom jump on node add
<ReactFlow fitView defaultViewport={{ x: 0, y: 0, zoom: 0.7 }}>

// ✅ Stable initial zoom, manual fitView only
<ReactFlow defaultViewport={{ x: 0, y: 0, zoom: 0.7 }}>
  <button onClick={() => fitView()}>适应画布</button>
```

### Aspect Ratio String Must Use Colon Format (2026-06-29)

**Problem**: Image preview box appears as flat rectangle instead of 1:1 square.

**Root cause**: `defaultConfig.size` was `"1024x1024"` but `getPreviewHeight` splits by `:`:
```typescript
const getPreviewHeight = (ratio: string) => {
  const [w, h] = ratio.split(':').map(Number);  // "1024x1024" → [NaN, undefined]
  return Math.round(320 * h / w);  // NaN → CSS fallback → flat rectangle
};
```

**Fix**: Always use `"w:h"` format for ratio strings: `"1:1"`, `"3:4"`, `"16:9"`, etc. Never `"1024x1024"`.
Also guard against NaN: `return Math.round(320 * h / w) || 320;`

### Avoid viewport Dependency in Node Components (2026-06-27)
If VideoNode/ImageNode read `viewport` from store for control panel scaling, every zoom/pan triggers re-render of ALL nodes. Instead:
- Remove `viewport` from node component destructuring
- Don't use `controlScale` based on store viewport
- If scaling is needed, use CSS or a separate non-reactive mechanism

## Zustand Undo/Redo with React Flow (2026-06-29 — UNRESOLVED)

**⚠️ 状态：未完全解决。已尝试多种方案均不稳定。**

**核心问题**：Undo 后 Zustand 状态恢复（日志确认 `restoring nodes: 1`），但 React Flow UI 不刷新，节点不显示。

**已尝试的方案**：
1. `key={undoVersion}` 强制重新挂载 → 有时有效有时无效
2. 原子操作（快照保存+操作在同一个 `set()`）→ 已实现但问题仍在
3. 直接依赖 Zustand 响应式更新 → 不工作
4. `useEffect` 监听 undoVersion 变化 → 未尝试

**可能的根因**：
- React Flow 内部维护自己的状态，与外部 nodes/edges 不同步
- `key` 变化导致重新挂载时，React Flow 可能从 localStorage 恢复旧状态
- 快照可能保存了错误的状态（空状态）

**调试日志确认**：
```
[RemoveNode] saving snapshot, nodes: 1 -> undoStack: 2
[Undo] undoStack length: 2
[Undo] current nodes: 1
[Undo] restoring nodes: 1
```
Undo 确实在恢复节点，但 UI 不显示。

**临时方案**：暂不实现 Undo/Redo，使用 localStorage 持久化 + 页面刷新恢复。

**参考资源**：
- [React Flow 官方 Undo/Redo 示例](https://reactflow.dev/examples/interaction/undo-redo) - Pro 版本
- [React Flow + Zustand Undo/Redo 指南](https://zenn.dev/suwash/articles/react_flow_undo_20251012) - 日文，详细解决方案
- [use-undoable 库](https://www.npmjs.com/package/use-undoable) - React Flow 社区方案

**详见 `antoken-undo-redo-unsolved` skill**

## 对话框交互模式 (2026-06-29)

### 防误触关闭

```typescript
// 全局监听 mousedown
const mouseDownTarget = useRef<EventTarget | null>(null);
useEffect(() => {
  const handle = (e: MouseEvent) => { mouseDownTarget.current = e.target; };
  document.addEventListener('mousedown', handle);
  return () => document.removeEventListener('mousedown', handle);
}, []);

// paneClick 检查
const handlePaneClick = useCallback(() => {
  if (mouseDownTarget.current) {
    const target = mouseDownTarget.current as HTMLElement;
    if (target.closest('[data-dialog="true"]')) return;
  }
  selectNode(null);
}, [selectNode]);
```

### 滚动穿透防护

```typescript
// 对话框容器
<div onWheel={(e) => e.stopPropagation()}
     onMouseEnter={() => document.body.setAttribute('data-hover-dialog', 'true')}
     onMouseLeave={() => document.body.removeAttribute('data-hover-dialog')}>

// ReactFlow 动态禁用
<ReactFlow panOnScroll={!hoveringDialog} zoomOnScroll={!hoveringDialog} />

// textarea 使用 addEventListener (passive: false)
el.addEventListener('wheel', (e) => { e.preventDefault(); el.scrollTop += e.deltaY; }, { passive: false });
```

## Critical Fixes

### selectNodeQuietly - Select Without Opening Property Panel
When you need to track which node is selected (e.g., for control panel visibility) WITHOUT opening the property panel:

```typescript
// In workflowStore
selectNodeQuietly: (nodeId) => {
  set({ selectedNodeId: nodeId });
  // Does NOT set propertyPanelOpen
},

// In node component
const { selectedNodeId, selectNodeQuietly } = useWorkflowStore();
const showControls = selectedNodeId === props.id;
onClick={() => selectNodeQuietly(props.id)}
```

### Control Panel Visibility Pattern
Use `selectedNodeId === props.id` AND `showControlPanel` from store for control panel visibility:

```typescript
// In node component
const { selectedNodeId, selectNodeQuietly, setShowControlPanel, showControlPanel } = useWorkflowStore();
const showControls = selectedNodeId === props.id && showControlPanel;

// On click
onClick={() => { selectNodeQuietly(props.id); setShowControlPanel(true); }}

// In WorkflowCanvas handlePaneClick
selectNode(null);  // clears selectedNodeId → hides all panels
```

**Key fix (2026-06-28):** Missing `showControlPanel` check caused control panel to show on node selection even when it should be hidden. Both conditions must be true:
1. `selectedNodeId === props.id` (node is selected)
2. `showControlPanel` (panel is explicitly opened)

Also update preview height calculation to match new node width (320px):
```typescript
const getPreviewHeight = (ratio: string) => {
  const [w, h] = ratio.split(':').map(Number);
  return Math.round(320 * h / w);  // was 280
};
```

### Multi-Edge Connection (Critical - 2026-06-16, verified 2026-06-17)
ReactFlow v12 has TWO mechanisms that silently replace edges when connecting multiple sources to same target handle:

1. **`onEdgesChange` remove type** — fires when new connection replaces old one
2. **`onEdgesChange` replace type** — fires when ReactFlow detects edges array changes internally

The full fix requires FIVE changes (all mandatory):

```tsx
// 1. ConnectionMode.Loose
import { ConnectionMode } from "@xyflow/react";
<ReactFlow connectionMode={ConnectionMode.Loose} />

// 2. Intercept onEdgesChange - ONLY process 'select' type
// ⚠️ Filtering just 'remove' is NOT enough! 'replace' type also causes edge loss!
onEdgesChange: (changes) => {
  set((s) => {
    const filtered = changes.filter((c) => c.type === 'select');
    if (filtered.length === 0) return s;
    const updated = applyEdgeChanges(filtered, s.edges);
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},

// 3. onConnect: direct append, no addEdge, unique ID, animated:false
// ⚠️ animated must be false! Otherwise dynamic dashed lines appear (user explicitly banned)
// ⚠️ style must match defaultEdgeOpts! Otherwise new edges have different style
onConnect: (connection) => {
  if (connection.source === connection.target) return;
  set((s) => {
    const edgeId = `edge-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    const newEdge = {
      id: edgeId,
      source: connection.source,
      target: connection.target,
      sourceHandle: connection.sourceHandle || null,
      targetHandle: connection.targetHandle || null,
      animated: false,
      style: { stroke: "rgba(255,255,255,0.4)", strokeWidth: 1.5 },
      type: "smoothstep",
    };
    const updated = [...s.edges, newEdge];
    saveToStorage({ nodes: s.nodes, edges: updated, workflowName: s.workflowName });
    return { edges: updated };
  });
},

// 4. Add independent removeEdge for user-initiated deletion
removeEdge: (edgeId) => {
  get().saveSnapshot();
  set((s) => {
    const edges = s.edges.filter((e) => e.id !== edgeId);
    saveToStorage({ nodes: s.nodes, edges, workflowName: s.workflowName });
    return { edges };
  });
},

// 5. Use removeEdge in context menu (not onEdgesChange)
if (contextMenu?.edgeId) {
  removeEdge(contextMenu.edgeId);
}
```

**Debugging tip:** If edges are still lost after filtering `remove`, check for `replace` type changes in `onEdgesChange`.

### Multi-Reference Upload (Video Generation)
Pass all upstream assets as arrays to backend:
```typescript
// Frontend
reference_image_urls: upstream.images.filter(i => i.url).map(i => i.url),
reference_video_urls: upstream.videos.filter(v => v.url).map(v => v.url),

// Backend: upload each to asset system, create image_with_roles/video_with_roles
for img_url in req.reference_image_urls:
    img_asset_id = await prepare_asset(base, api_key, group_id, img_url, "image")
    image_with_roles.append({"url": f"asset://{img_asset_id}", "role": "reference_image"})
```

### Asset Naming
Use localStorage-based counter with max+1 logic to avoid duplicates:
```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

### Right-Click Canvas Context Menu — 添加素材 vs 导入素材

阿戴要求右键菜单分为两个功能区：
- **添加素材** → 直接在画布上创建空白素材框（不弹文件选择器），用户之后可以拖拽文件或连接AI生成
- **导入素材** → 打开文件选择器，用户选择本地文件上传后创建带内容的节点

实现方式：两个独立handler：
```tsx
// 添加空白素材（不打开文件选择器）
const handleCreateEmptyAsset = useCallback((assetType: 'IMAGE' | 'VIDEO') => {
  setContextMenu(null);
  const assetNumber = getNextAssetNumber(assetType);
  const assetName = assetType === 'IMAGE' ? `图素材${assetNumber}` : `视频素材${assetNumber}`;
  // 计算视口中心位置，创建空白节点（config只有assetName，没有assetUrl）
  const newNode = { ... data: { config: { assetName }, assetName } };
  addNode(newNode);
}, [addNode, viewport]);

// 导入素材（打开文件选择器）
const handleImportAsset = useCallback((assetType: 'IMAGE' | 'VIDEO') => {
  setAddingAssetType(assetType);
  setContextMenu(null);
  fileInputRef.current?.click();
}, []);
```

菜单UI用分隔线隔开两组：
```tsx
{/* 添加素材 */}
<div style={{ padding: "6px 14px 4px", fontSize: 10, color: "#62666d" }}>添加素材</div>
<button onClick={() => handleCreateEmptyAsset('IMAGE')}>图片素材</button>
<button onClick={() => handleCreateEmptyAsset('VIDEO')}>视频素材</button>
{/* 分隔线 */}
<div style={{ height: 1, background: "rgba(255,255,255,0.06)", margin: "4px 14px" }} />
{/* 导入素材 */}
<div style={{ padding: "6px 14px 4px", fontSize: 10, color: "#62666d" }}>导入素材</div>
<button onClick={() => handleImportAsset('IMAGE')}>导入图片</button>
<button onClick={() => handleImportAsset('VIDEO')}>导入视频</button>
```

左侧菜单（CircleNavPanel）底部也添加"导入素材"选项，需要：useRef for file input, uploadToBackend function, handleFileSelect handler。

### Right-Click Node Download (2026-06-28)

Nodes with content (assetUrl/resultUrl) support right-click → download:

```tsx
// Context menu state — add 'node' type
const [contextMenu, setContextMenu] = useState<{
  x: number; y: number; type: 'edge' | 'canvas' | 'node'; edgeId?: string; nodeId?: string;
} | null>(null);

// Node right-click handler — only show menu if node has content
const onNodeContextMenu = useCallback((e: React.MouseEvent, node: any) => {
  e.preventDefault();
  const nodeData = node.data as NodeData;
  const config = nodeData.config as Record<string, unknown> | undefined;
  const url = (config?.assetUrl || config?.resultUrl || nodeData.assetUrl) as string | undefined;
  if (url) {
    setContextMenu({ x: e.clientX, y: e.clientY, type: 'node', nodeId: node.id });
  }
}, []);

// Download handler — uses backend proxy to avoid CORS
const handleDownloadAsset = useCallback(() => {
  if (!contextMenu?.nodeId) return;
  const node = nodes.find(n => n.id === contextMenu.nodeId);
  if (!node) return;
  const nodeData = node.data as NodeData;
  const config = nodeData.config as Record<string, unknown> | undefined;
  const url = (config?.assetUrl || config?.resultUrl || nodeData.assetUrl) as string | undefined;
  if (url) {
    const proxyUrl = `${getApiBase()}/api/generate/proxy?url=${encodeURIComponent(url)}`;
    const a = document.createElement('a');
    a.href = proxyUrl;
    a.download = nodeData.assetName || '素材';
    a.target = '_blank';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
  setContextMenu(null);
}, [contextMenu, nodes]);

// Add to ReactFlow
<ReactFlow onNodeContextMenu={onNodeContextMenu} ... />

// Menu UI — between edge menu and canvas menu
{contextMenu.type === 'node' ? (
  <button onClick={handleDownloadAsset} style={{...}}>
    <svg ...>download icon</svg>
    下载素材
  </button>
) : contextMenu.type === 'edge' ? ( ... ) : ( ... )}
```

Add `onPaneContextMenu` to ReactFlow for canvas-level right-click menu (e.g., "Add Image Asset", "Add Video Asset"):

```tsx
// TypeScript: must use MouseEvent | React.MouseEvent (not just React.MouseEvent)
const onPaneContextMenu = useCallback((e: MouseEvent | React.MouseEvent) => {
  e.preventDefault();
  setContextMenu({ x: e.clientX, y: e.clientY, type: 'canvas' });
}, []);

<ReactFlow
  onPaneContextMenu={onPaneContextMenu}
  onEdgeContextMenu={onEdgeContextMenu}
  // ...
/>
```

Menu renders as `position: fixed` div at click coordinates. Close on `onPaneClick`.

## Local Asset Upload (Right-Click → File Picker)

When user uploads their own files (not AI-generated), preserve original properties:

```tsx
// Hidden file input
const fileInputRef = useRef<HTMLInputElement>(null);
<input ref={fileInputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileSelect} />

// Create blob URL (no upload to server, no modification)
const fileUrl = URL.createObjectURL(file);

// Get original dimensions BEFORE creating node
if (assetType === 'IMAGE') {
  const img = new window.Image();
  img.onload = () => createNode(assetType, fileUrl, { width: img.naturalWidth, height: img.naturalHeight });
  img.src = fileUrl;
} else {
  const video = document.createElement('video');
  video.onloadedmetadata = () => createNode(assetType, fileUrl, { width: video.videoWidth, height: video.videoHeight, duration: video.duration });
  video.src = fileUrl;
}
```

### isLocalAsset Flag

Mark local assets in config to differentiate rendering:

```tsx
// In node creation
data: {
  config: {
    assetUrl: fileUrl,
    isLocalAsset: true,  // Flag for rendering behavior
    originalWidth: img.naturalWidth,
    originalHeight: img.naturalHeight,
  }
}

// In ImageNode: use contain (preserve ratio) vs cover (crop to fit)
<img style={{ objectFit: cfg.isLocalAsset ? "contain" : "cover", background: cfg.isLocalAsset ? "#1a1a1a" : "transparent" }} />

// In VideoPreview: pass isLocalAsset prop
<VideoPreview isLocalAsset={cfg.isLocalAsset} ... />
```

### cfg Type Must Include isLocalAsset

```typescript
const cfg = d.config as {
  // ... existing fields
  isLocalAsset?: boolean;
  originalWidth?: number;
  originalHeight?: number;
  originalDuration?: number;
};
```

### LAN Access & File Upload
- **Dynamic API URL** — Replace all `http://localhost:8000` with `getApiBase()` from `lib/api.ts`
- **CORS for LAN** — Backend needs `CORS_ORIGINS: ["*"]` for cross-network access
- **File upload endpoint** — Create `/api/upload` for local file uploads (blob URLs inaccessible by backend)
- **Upload flow** — blob URL → get dimensions → upload to backend → use backend URL in node data
- See `references/lan-access-and-file-upload.md` for full implementation

### Asset Upload Path Analysis
- **Three upload paths** store URLs differently — canvas drag, node upload, AI generation
- **assetUpload.ts bug**: returns `url: undefined` because backend returns `path` not `url`
- **LAN URL handling**: backend downloads from self → data URL → binary upload to toapis.com
- See `references/asset-upload-path-analysis.md` for full analysis and fix

### Canvas Context Menu & File Drag-drop
- **Right-click menu** — Use `onPaneContextMenu` for canvas, `onEdgeContextMenu` for edges
- **File drag-drop** — Handle `e.dataTransfer.files` in `onDrop`, detect image/video by MIME type
- **Event type** — `onPaneContextMenu` accepts `MouseEvent | React.MouseEvent`, not just `React.MouseEvent`
- See `references/lan-access-and-file-upload.md` for implementation details

### Right-Click Canvas Menu
- Use `onPaneContextMenu` on ReactFlow for canvas right-click
- Menu position: `e.clientX, e.clientY` (fixed positioning)
- Context menu type: `'edge'` for edge menu, `'canvas'` for canvas menu
- Canvas menu options: "添加图片素材", "添加视频素材"

### Right-Click Canvas Menu (添加素材 vs 导入素材)
Two distinct operations in the context menu:
- **添加素材** (Add) — creates empty asset node directly, no file picker. For later drag-drop or AI generation.
- **导入素材** (Import) — opens file picker, uploads file to backend, creates node with content.
- Separated by a divider line in the menu.
- Left sidebar (CircleNavPanel) also has "导入素材" at the bottom of the + menu.

### Drag-and-Drop File Upload
- Handle file drops in `onDrop` callback
- Check `e.dataTransfer.files` for native file drops
- Detect type: `file.type.startsWith('image/')` or `'video/'`
- Upload to backend first, store backend URL (not blob URL)
- Get original dimensions via `Image.onload` / `video.onloadedmetadata`

### Delete Key Behavior
- When focus is in input/textarea, Delete/Backspace should NOT delete node
- Check `isInputFocused` and `return` early — always, regardless of input content
- Previous logic: "only delete if input is empty" → caused accidental deletions

### Selection Styling (阿戴 preference)
- Border: `1.5px solid rgba(255,255,255,0.3)` (white, not category color)
- Box shadow: `"0 0 0 1px rgba(255,255,255,0.1), 0 12px 32px rgba(0,0,0,0.6)"`
- No glow, no colored borders, no `0 0 0 Npx` patterns
- Hover: `"0 8px 24px rgba(0,0,0,0.4)"`

### Control Panel Scaling with Viewport Zoom (2026-06-27)

When canvas is zoomed out, control panels become too small. Scale them inversely:

```typescript
const { viewport } = useWorkflowStore();
const controlScale = viewport.zoom < 1 ? 1 + (1 - viewport.zoom) * 0.3 : 1;

// Apply to control panel div
style={{ transform: `scale(${controlScale})`, transformOrigin: "top left" }}
```

Formula: zoom=1 → 1x, zoom=0.5 → 1.15x. Apply to both VideoNode and ImageNode.

### Full-Screen Preview Button Must Have onClick (2026-06-27)

The expand button (square-with-corners SVG) in control panels was missing onClick. Always bind:
```typescript
<button onClick={() => previewUrl && setShowPreview(true)} ...>
```

## toapis.com 视频生成 API 参数（2026-06-28 关键发现）

**toapis.com 视频生成 API 要求 `aspect_ratio` 参数，不是 `ratio`。**

```python
# ❌ 错误：API 会忽略这个参数，默认生成 16:9
payload = {"model": model, "prompt": prompt, "duration": 5, "ratio": "9:16"}

# ✅ 正确：API 会按指定比例生成视频
payload = {"model": model, "prompt": prompt, "duration": 5, "aspect_ratio": "9:16"}
```

**支持的 aspect_ratio 值：** `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`

**前端 resolution → 后端 aspect_ratio 转换：**
```python
def resolution_to_ratio(resolution: str) -> str:
    mapping = {
        "720p": "16:9", "1080p": "16:9",
        "720p_vertical": "9:16", "1080p_vertical": "9:16",
        "720p_square": "1:1", "1080p_square": "1:1",
    }
    return mapping.get(resolution, "16:9")
```

**症状：** 用户选择 9:16 竖屏，但生成的视频始终是 16:9。不是前端裁切问题，是后端发送了错误的参数名。

**教训：** 调用第三方 API 时，必须对照官方文档验证参数名。`ratio` 和 `aspect_ratio` 看似相同，但 API 会静默忽略不认识的参数。

## seedance-2 视频生成模式（2026-06-29）

**toapis.com seedance-2 API 支持 4 种生成模式，通过 `image_with_roles` 参数控制：**

| 模式 | 参数 | 说明 |
|------|------|------|
| 文生视频 | 无 image_with_roles | 纯文字描述 |
| 首帧模式 | `[{url, role: "first_frame"}]` | 指定视频开头画面 |
| 首尾帧模式 | `[{url, role: "first_frame"}, {url, role: "last_frame"}]` | 指定开头和结尾 |
| 全能参考 | `[{url, role: "reference_image"}]` | 参考图片风格 |

**关键限制**：
- `first_frame`/`last_frame` 不能与 `reference_image` 混用
- `seedance-2-mini` 只支持 `reference_image`，不支持帧模式
- 后端直接传递 `image_with_roles` 给 API，不需要转换

**前端实现**：模式选择器 + 帧上传区域（点击输入 URL，显示预览）
**详见 `references/seedance-video-modes.md`**

## toapis.com 图片生成 API 清晰度参数（2026-06-29）

**nano_banana_2 (Gemini 3.1 Flash) 支持 `metadata.resolution` 参数控制输出清晰度：**

```json
{
  "model": "gemini-3.1-flash-image-preview",
  "prompt": "...",
  "aspect_ratio": "16:9",
  "metadata": {
    "resolution": "2K"
  }
}
```

**支持的清晰度值：**
- `0.5K` — 快速预览
- `1K` — 标准（默认）
- `2K` — 高清
- `4K` — 超清（更贵）

**前端实现：** 仅当选择 `nano_banana_2` 模型时显示清晰度选择器：
```tsx
{model === "nano_banana_2" && (
  <select value={resolution} onChange={(e) => setResolution(e.target.value)}>
    <option value="1K">标准 1K</option>
    <option value="2K">高清 2K</option>
    <option value="4K">超清 4K</option>
    <option value="0.5K">快速 0.5K</option>
  </select>
)}
```

**后端传递：** 将 resolution 放入 metadata 字段：
```python
if req.resolution:
    payload["metadata"] = {"resolution": req.resolution}
```

### VideoNode 同时发送 ratio 和 resolution 的陷阱（2026-06-28）

VideoNode.tsx 有**两个独立的状态变量**：
- `ratio`: 直接比例值（如 `"9:16"`, `"3:4"`, `"1:1"`, `"16:9"`）
- `resolution`: 清晰度值（如 `"480p"`, `"720p"`, `"1080p"`）

前端同时发送两个参数：
```typescript
body: JSON.stringify({
  prompt, model, resolution: resolution, ratio: ratio, ...
})
```

**后端陷阱**：`resolution_to_ratio()` 函数只认带后缀的格式：
```python
mapping = {
    "720p": "16:9",        # ← VideoNode 发的 "720p" 会被转成 "16:9"！
    "1080p": "16:9",
    "720p_vertical": "9:16",  # ← VideoGenNode 发的才长这样
    "1080p_vertical": "9:16",
    "720p_square": "1:1",
}
```

**结果**：用户在 VideoNode 选了 `ratio: "9:16"` + `resolution: "720p"`，后端用 `resolution_to_ratio("720p")` 返回 `"16:9"`，忽略了 `ratio`。

**修复**：后端优先使用 `ratio`（如果包含 `":"`），其次才用 `resolution` 转换：
```python
if req.ratio and ":" in req.ratio:
    ratio = req.ratio
elif req.resolution:
    ratio = resolution_to_ratio(req.resolution)
else:
    ratio = "16:9"
```

**教训**：当前端发送多个相关参数时，后端必须明确优先级。不能假设只有一个参数会被使用。

## toapis.com Asset 上传（2026-06-27 关键发现）

**toapis.com Asset API 限制：**
- `source_url` 必须是**公开可访问的 HTTP/HTTPS URL**
- **不接受** data URL（`data:image/png;base64,...`）→ 返回 "invalid request body"
- **不接受** 局域网 URL（`http://192.168.x.x`、`http://localhost`）→ toapis.com 无法访问

**正确的上传流程（前端直传 toapis.com）：**
1. 前端拿到用户文件 → 直接调 toapis.com Asset API 上传
2. 拿到 `assetId` → 存到节点 `assetUrl = asset://{assetId}`
3. 同时上传到后端 `/api/upload` → 拿到后端 URL → 存为 `previewUrl`（预览显示用）
4. 生成时 `getUpstreamAssets` 读 `assetUrl`（即 `asset://{assetId}`）→ 发给后端
5. 后端 `prepare_asset` 检测到 `asset://` 前缀 → 跳过上传，直接用已有的 `assetId`

**上传失败时必须报错，不能静默回退到后端 URL：**
- 如果 `uploadToAsset` 失败（额度不够、网络错误等）→ 弹窗报错，不创建节点
- 绝不能静默回退到后端 URL，否则后续生成会报 "invalid request body" 迷惑用户

**架构原则：**
- 前端**不直连** toapis.com 做 API 调用（生成、轮询等走后端代理）
- 前端**只在素材上传**这一步直连 toapis.com（因为 toapis 不接受 LAN URL）
- 后端代理所有其他 API 调用

## toapis.com Asset API 不接受二进制上传（2026-06-27 关键发现）

**toapis.com 的 asset API（`/videos/doubao-seedance-2-0/private-avatar/assets`）只接受 JSON 格式的 `source_url`，不接受 multipart 二进制上传。**

尝试二进制上传会返回 `{"message":"invalid request body","success":false}`。

**正确的 LAN 文件处理方式（2026-06-27 验证）：**
1. 前端只上传到后端 `/api/upload`（用于预览显示）
2. 后端收到生成请求时，检测 LAN URL → 下载文件 → 转 base64 data URL → 直接传给生成 API 的 `image_urls` 字段
3. **不走 asset 系统**，直接用 `image_urls` 传给视频生成 API

```python
# 后端：LAN 文件转 data URL
async def resolve_url(url: str) -> str:
    if url.startswith("http://192.168.") or url.startswith("http://localhost"):
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                b64 = base64.b64encode(resp.content).decode()
                mime = mime_map.get(ext, "application/octet-stream")
                return f"data:{mime};base64,{b64}"
    return url

# 直接传给生成 API
payload["image_urls"] = [await resolve_url(url) for url in req.reference_image_urls]
```

**错误方案（已验证失败）：**
- ❌ 前端直传 toapis.com asset 系统（不接受二进制）
- ❌ 后端转 data URL 后传给 asset 系统（asset 系统只接受公开 URL）
- ❌ 用 `asset://` 格式绕过（需要先成功上传到 asset 系统）

**关键区别：**
- 图片生成 API：直接用 `image_urls` 传 URL
- 视频生成 API：也可以直接用 `image_urls` 传 URL（不需要 asset 系统）
- asset 系统：只用于已公开的 URL（如 AI 生成的 toapis.com CDN URL）

## assetUpload.ts 字段名陷阱（2026-06-27）

后端 `/api/upload` 返回 `{ path: "/api/upload/file/xxx.ext" }`，不是 `{ url: ... }`。

前端 `uploadAsset` 必须拼接：
```typescript
url: data.url || data.asset_url || (data.path ? `${getApiBase()}${data.path}` : undefined)
```

同时 `API_BASE` 必须用 `getApiBase()` 动态获取，不能在模块加载时固定。

## toapis.com API 限制（2026-06-27 血泪教训）

**toapis.com 的 asset API 和生成 API 都只接受公开可访问的 HTTP/HTTPS URL：**
- ❌ 不接受二进制文件上传（multipart form）→ `invalid request body`
- ❌ 不接受 base64 data URL → `base64 image is not allowed`
- ❌ 不接受局域网 URL（`http://192.168.x.x`）→ toapis.com 访问不了
- ✅ 只接受公开 HTTP/HTTPS URL（如 `https://files.toapis.com/...`、`https://0x0.st/...`）

**"前端直连toapis.com"是废案**（2026-06-27确认）——前端无法绕过这个URL限制。

**本地开发解决方案：** 后端上传文件时同时传到 `0x0.st`（免费文件托管），拿到公开URL存储为 `assetUrl`。
**线上部署：** 后端有公网域名，上传文件的URL本身就是公开的，不需要0x0.st。

**代码实现：**
- `backend/app/api/upload.py` — `upload_to_public()` 函数上传到0x0.st
- 响应增加 `public_url` 字段
- 前端 `assetUrl` 优先用 `publicUrl`，本地URL仅用于预览

## toapis.com 素材上传架构（2026-06-27 重大教训）

**核心约束：toapis.com 只接受公开可访问的 HTTP/HTTPS URL**

不接受的格式（全部会报错）：
- 二进制文件上传（multipart form data）→ `invalid request body`
- base64 data URL → `base64 image is not allowed`
- 局域网 URL（192.168.x.x）→ toapis.com 无法访问

**正确架构：**
1. 前端上传文件到后端 `/api/upload`（本地存储，用于预览）
2. 后端同时上传到公开文件托管服务（如 tmpfiles.org）→ 拿到公开 URL
3. 前端存储公开 URL 作为 `assetUrl`
4. 生成时，后端/toapis.com 通过公开 URL 访问文件

**异步优化：**
- 后端立即返回本地 URL，后台异步上传到公开托管
- 前端创建节点用本地 URL（预览），轮询 `/api/upload/public-url/{asset_id}` 获取公开 URL
- 公开 URL 就绪后自动更新节点的 `assetUrl`

**代理问题：**
- 本地开发时，Mac 可能有代理（如 127.0.0.1:6324）
- httpx 请求外部服务需要设置 `proxy=PROXY`
- 环境变量 `UPLOAD_PROXY` 可配置代理地址

**公开文件托管选择：**
- 0x0.st：2026-06 已关闭上传（AI botnet spam）
- tmpfiles.org：可用，URL 格式 `https://tmpfiles.org/dl/{id}/{filename}`
- 线上部署时不需要：后端有公网域名，文件直接通过后端 URL 访问

## 排版/CSS异常必查缓存（2026-06-27 教训）

**每次改代码后如果页面排版异常、CSS 404、JS加载失败，必须同时清除三个缓存目录：**

```bash
cd ~/antoken/frontend
rm -rf .next .swc node_modules/.cache
npm run dev
```

只清 `.next` 不清 `.swc` 仍然会出问题。`node_modules/.cache` 也可能积累旧的编译结果。

**症状：** CSS 文件 URL 返回 404 HTML 页面（不是 CSS），`<link>` 标签的 `sheet.cssRules.length === 0`。

**验证方法：**
```bash
curl -s http://localhost:3000/_next/static/css/app/layout.css | head -5
# 如果返回 HTML（<!DOCTYPE html>）而不是 CSS，说明缓存问题
```

这是反复出现的老问题，每次大改代码后都要执行。

## toapis.com API 素材限制（2026-06-27 确认）

**toapis.com 的 asset API 和生成 API 只接受公开可访问的 HTTP/HTTPS URL。不接受：**
- 二进制文件上传（multipart form data）→ `invalid request body`
- base64 data URL → `base64 image is not allowed`
- 局域网 URL（192.168.x.x）→ toapis.com 无法访问

**正确做法：** 文件必须先上传到公开可访问的位置，拿到公开 URL 后再传给 toapis.com。

**架构：**
```
用户拖拽文件 → 上传到后端（本地存储）→ 同时上传到公开文件托管（tmpfiles.org）
                                      → 拿到公开 URL（https://tmpfiles.org/dl/xxx）
                                      → 前端存储公开 URL 作为 assetUrl
                                      → 生成时传给 toapis.com
```

**上线后：** 后端有公网域名，文件直接通过后端 URL 访问，不需要第三方托管。

## 异步上传优化模式（2026-06-27）

为避免上传到公开文件托管阻塞 UI：

1. 上传到后端 → 立即返回本地 URL
2. 创建节点（本地 URL 预览）
3. 后台异步上传到公开文件托管
4. 轮询公开 URL 端点（`GET /api/upload/public-url/{asset_id}`）
5. 完成后自动更新节点的 `assetUrl`

```python
# 后端：立即返回，后台上传
asyncio.create_task(_upload_to_public(file_path, filename, unique_name))
return {"path": f"/api/upload/file/{unique_name}", "asset_id": unique_name}

# 后端：查询公开URL端点
@router.get("/public-url/{asset_id}")
async def get_public_url(asset_id: str):
    if asset_id in _public_url_cache:
        return {"ready": True, "public_url": _public_url_cache[asset_id]}
    return {"ready": False}
```

```typescript
// 前端：轮询公开URL
const pollPublicUrl = async (assetId: string, nodeId: string) => {
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 2000));
    const resp = await fetch(`${getApiBase()}/api/upload/public-url/${assetId}`);
    const data = await resp.json();
    if (data.ready && data.public_url) {
      updateNodeData(nodeId, { assetUrl: data.public_url });
      return;
    }
  }
};
```

## 公开文件托管服务（2026-06-27）

**0x0.st 已关闭上传**（2026-06-27 确认）：`uploads disabled because it's been almost nothing but AI botnet spam`

**替代方案：tmpfiles.org**
- API: `POST https://tmpfiles.org/api/v1/upload`（multipart form data）
- 返回: `{"status":"success","data":{"url":"https://tmpfiles.org/xxxxx/filename"}}`
- 直接下载链接需转换: `tmpfiles.org/` → `tmpfiles.org/dl/`

**⚠️ 本地开发需要代理：** Mac 上需要通过 `127.0.0.1:6324` 代理访问外部服务：
```python
async with httpx.AsyncClient(timeout=60, proxy="http://127.0.0.1:6324") as client:
    resp = await client.post("https://tmpfiles.org/api/v1/upload", files={"file": ...})
```

**上线后不需要：** 服务器直连外网，不需要代理，也不需要 tmpfiles.org。

## Node Right-Click Context Menu (2026-06-29)

Nodes with content support right-click with download and delete options:

```tsx
// Menu structure
{contextMenu.type === 'node' ? (
  <>
    <button onClick={handleDownloadAsset} style={{ color: "rgba(235, 235, 245, 0.85)" }}>
      <svg>download icon</svg>
      下载素材
    </button>
    <button onClick={() => {
      if (contextMenu.nodeId) removeNode(contextMenu.nodeId);
      setContextMenu(null);
    }} style={{ color: "#ff453a" }}>
      <svg>trash icon</svg>
      删除素材
    </button>
  </>
) : contextMenu.type === 'edge' ? ( ... ) : ( ... )}
```

Delete button uses red color (#ff453a) with red hover background (rgba(255, 69, 58, 0.12)).

## Control Panel Dialog Pitfalls (2026-06-29)

### overflow:hidden clips control panel
**Problem**: BaseNode's node card has `overflow: "hidden"` which clips the control panel that's positioned below (`top: "100%"`).

**Fix**: Remove `overflow: "hidden"` from the node card div in BaseNode.tsx.

```tsx
// ❌ Wrong: clips control panel
<div style={{ ..., overflow: "hidden" }}>

// ✅ Correct: control panel visible
<div style={{ ..., /* no overflow */ }}>
```

### Double-click requires onNodeDoubleClick handler
**Problem**: Single click selects node but doesn't show dialog. Need explicit double-click handler.

**Fix**: Add `onNodeDoubleClick` to ReactFlow:

```tsx
// In WorkflowCanvas
const onNodeDoubleClick = useCallback((_: any, node: any) => {
  selectNodeQuietly(node.id);
  setShowControlPanel(true);
}, [selectNodeQuietly, setShowControlPanel]);

<ReactFlow onNodeDoubleClick={onNodeDoubleClick} ... />
```

### Control panel sizing (Apple Glass style)
Width 480px, padding 16px, separate generate button area:

```tsx
<div style={{
  position: "absolute",
  top: "100%",
  left: -40,
  width: 480,
  marginTop: 12,
  background: "rgba(28, 28, 30, 0.9)",
  backdropFilter: "saturate(180%) blur(20px)",
  border: "0.5px solid rgba(255, 255, 255, 0.12)",
  borderRadius: 16,
  boxShadow: "0 12px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.06)",
}}>
```

### Scrollbar on left side of textarea
Use `direction: rtl` on container + `direction: ltr` on textarea:

```tsx
<div style={{ position: 'relative', direction: 'rtl' }}>
  <textarea style={{ ..., direction: 'ltr' }} />
</div>
```

### Separate generate button area
Don't overlay button on textarea. Use flex layout:

```tsx
<div style={{ display: "flex", gap: 12, alignItems: "stretch" }}>
  <div style={{ flex: 1 }}>
    <textarea ... />
  </div>
  <button style={{ width: 48, height: 48, flexShrink: 0 }}>
    {/* generate icon */}
  </button>
</div>
```

## Video-to-Image Workflow (2026-06-28 关键发现)

**toapis.com 图片生成 API 不支持 `video_urls` 参数，只支持 `image_urls`。**

当上游节点是视频、下游节点是图片时，不能直接传视频 URL 给图片 API。

**解决方案：自动提取视频首帧作为图片参考**

后端 `generate.py` 已有 `extract_video_frame()` 函数（用 ffmpeg 提取首帧），在 `generate_image` 中自动处理：

```python
# 参考素材处理
all_image_urls = list(req.reference_image_urls) if req.reference_image_urls else []

# 如果有视频参考，提取首帧作为图片参考（API不支持视频URL）
if req.reference_video_urls:
    logger.info(f"[图片] 检测到视频参考: {len(req.reference_video_urls)}个，提取首帧...")
    for video_url in req.reference_video_urls:
        try:
            frame_url = await extract_video_frame(video_url)
            all_image_urls.append(frame_url)
        except Exception as e:
            logger.warning(f"[图片] 视频首帧提取失败: {e}")

if all_image_urls:
    payload["image_urls"] = all_image_urls
```

**前端逻辑（ImageNode.tsx）已正确**：
- `getUpstreamAssets()` 收集上游节点的 `resultUrl`/`assetUrl`
- 根据 `edge.targetHandle` 或 `assetType` 区分图片/视频
- 分别发送 `reference_image_urls` 和 `reference_video_urls`

**VideoGenNode 缺少上游素材收集逻辑**（已知问题）：
- ImageGenNode 和 ImageNode 都有 `getUpstreamAssets()`
- VideoGenNode 没有，连接的上游节点被忽略

**Google Gemini 3.1 Flash 原生支持 video-to-image**，但 toapis.com 封装后不暴露此功能。

**`extract_video_frame` 必须返回公开 URL**（2026-06-28 修复）：
- 旧代码返回 `http://localhost:8000/api/generate/temp-file/{filename}`（本地 URL）
- toapis.com 无法访问本地 URL → 生成失败
- 修复：提取首帧后上传到 tmpfiles.org，返回公开 URL
- 使用 `upload.py` 的 `_upload_to_public()` 函数

```python
# 旧代码（错误）
local_url = f"http://localhost:8000/api/generate/temp-file/{frame_filename}"
return local_url

# 新代码（正确）
from app.api.upload import _upload_to_public, _public_url_cache
unique_name = frame_filename
await _upload_to_public(tmp_frame_path, frame_filename, unique_name)
if unique_name in _public_url_cache:
    return _public_url_cache[unique_name]
```

## Apple Glass UI 设计系统（2026-06-28）

阿戴要求 Apple 风格流动玻璃效果，替代之前的 Linear 暗色风格。

### 毛玻璃面板
```css
background: rgba(28, 28, 30, 0.72);
backdrop-filter: saturate(180%) blur(20px);
-webkit-backdrop-filter: saturate(180%) blur(20px);
border: 0.5px solid rgba(255, 255, 255, 0.08);
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06);
```

### 色彩系统
- 主背景：`#000000`
- 面板：`rgba(28, 28, 30, 0.8)`
- 强调色：`#0a84ff`（Apple Blue）
- 成功：`#30d158`
- 错误：`#ff453a`
- 文字层级：`#fff` / `rgba(235, 235, 245, 0.6)` / `rgba(235, 235, 245, 0.3)`

### 字体栈
```css
--font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'Inter', sans-serif;
```

### 交互动效
- 过渡曲线：`cubic-bezier(0.4, 0, 0.2, 1)`
- 按钮悬停：`scale(1.05)` + 阴影
- 点击反馈：`scale(0.98)`
- 菜单项悬停：`rgba(255, 255, 255, 0.08)` 背景

详见 `references/apple-glass-morphism.md`（open-design skill）

## FastAPI 调试日志技巧（2026-06-28）

uvicorn 的 `logger.info()` 输出可能被后台进程捕获但不显示在 `process(action='log')` 中。调试时同时使用 `print()` 和 `logger.info()`：

```python
@router.post("/video")
async def generate_video(req: VideoRequest):
    print(f"[DEBUG-视频] 收到请求: model={req.model}, resolution={req.resolution}")
    logger.info(f"[视频] 收到请求: model={req.model}")
```

`print()` 输出会直接出现在 uvicorn 的 stdout，更容易在进程日志中看到。

## 交互动效系统（2026-06-28）

创建 `styles/interactions.ts` 统一管理所有交互动效，避免内联样式重复：

```typescript
// styles/interactions.ts
export const btnSecondary: CSSProperties = {
  background: 'rgba(255,255,255,0.02)',
  color: '#d0d6e0',
  padding: '8px 16px',
  borderRadius: 8,
  fontSize: 12,
  border: '1px solid rgba(255,255,255,0.08)',
  cursor: 'pointer',
  transition: 'all 0.15s cubic-bezier(0.4, 0, 0.2, 1)',
};

export const btnSecondaryHover: CSSProperties = {
  background: 'rgba(255,255,255,0.06)',
  color: '#f7f8f8',
  borderColor: 'rgba(255,255,255,0.15)',
};

// 使用方式
const btnHoverHandlers = {
  onMouseEnter: (e: React.MouseEvent<HTMLElement>) => {
    Object.assign(e.currentTarget.style, btnSecondaryHover);
  },
  onMouseLeave: (e: React.MouseEvent<HTMLElement>) => {
    Object.assign(e.currentTarget.style, btnSecondary);
  },
};

// 在组件中
<button style={btnSecondary} {...btnHoverHandlers}>设置</button>
```

**全局 CSS 动效**（`globals.css`）：
```css
button {
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

button:active {
  transform: scale(0.98);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
}
```

**动画 keyframes**：
- `scaleIn` - 缩放进入
- `pulse` - 脉冲（加载状态）
- `shimmer` - 闪光（骨架屏）

**设计原则**（Linear 风格）：
- 过渡曲线：`cubic-bezier(0.4, 0, 0.2, 1)`（快速启动，缓慢结束）
- 过渡时长：0.15s（按钮）、0.2s（卡片）
- 悬停效果：背景变亮 + 边框变亮
- 点击效果：`scale(0.98)` 缩小反馈
- 禁用状态：`opacity: 0.5`

## Control Panel Consolidation (2026-06-28)

React Flow's built-in `<Controls>` component and custom buttons (grid snap, etc.) can overlap. Consolidate into a single unified panel:

```tsx
// 1. Hide default React Flow Controls
<Controls showInteractive={false} style={{ display: 'none' }} />

// 2. Create unified control panel with Apple Glass style
<div style={{
  position: "absolute",
  bottom: 16,
  left: 16,
  display: "flex",
  flexDirection: "column",
  gap: 1,
  background: "rgba(28, 28, 30, 0.72)",
  backdropFilter: "saturate(180%) blur(20px)",
  WebkitBackdropFilter: "saturate(180%) blur(20px)",
  border: "0.5px solid rgba(255, 255, 255, 0.08)",
  borderRadius: 12,
  overflow: "hidden",
  zIndex: 5,
  boxShadow: "0 4px 16px rgba(0, 0, 0, 0.2)",
}}>
  {/* Grid Snap Toggle */}
  <button onClick={() => setSnapEnabled(!snapEnabled)} style={{
    width: 36, height: 36,
    background: snapEnabled ? "rgba(10, 132, 255, 0.2)" : "none",
    color: snapEnabled ? "#0a84ff" : "rgba(235, 235, 245, 0.5)",
    // ...
  }}>
    <svg>/* grid icon */</svg>
  </button>

  {/* Divider */}
  <div style={{ height: 0.5, background: "rgba(255, 255, 255, 0.06)", margin: "0 8px" }} />

  {/* Zoom In */}
  <button onClick={() => {/* dispatch wheel event with ctrlKey */}} style={{...}}>
    <svg>/* plus icon */</svg>
  </button>

  {/* Zoom Out */}
  <button onClick={() => {/* dispatch wheel event with ctrlKey */}} style={{...}}>
    <svg>/* minus icon */</svg>
  </button>

  {/* Fit View */}
  <button onClick={() => {/* access react-flow instance */}} style={{...}}>
    <svg>/* fit view icon */</svg>
  </button>
</div>
```

**Key points:**
- Single control panel in bottom-left (not multiple scattered buttons)
- Apple Glass style with `backdrop-filter: saturate(180%) blur(20px)`
- Grid snap toggle with active state (blue highlight)
- Divider separates snap toggle from zoom controls
- Hover effect: `rgba(255, 255, 255, 0.06)` background

## Node Card Sizing (2026-06-28)

Default node width 280px → 320px for better content visibility:

```tsx
// BaseNode.tsx
<div style={{
  width: 320,  // was 280
  background: "rgba(28, 28, 30, 0.85)",  // Apple Glass
  backdropFilter: "saturate(180%) blur(20px)",
  WebkitBackdropFilter: "saturate(180%) blur(20px)",
  border: selected
    ? "1px solid rgba(255, 255, 255, 0.2)"
    : "0.5px solid rgba(255, 255, 255, 0.08)",
  borderRadius: 16,  // was 20
  boxShadow: selected
    ? "0 0 0 1px rgba(255, 255, 255, 0.1), 0 12px 32px rgba(0, 0, 0, 0.5)"
    : "0 2px 8px rgba(0, 0, 0, 0.2)",
  transition: "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
  overflow: "hidden",
}}>
```

Also update the wrapper div width to match:
```tsx
<div style={{ position: "relative", width: 320, padding: 40, margin: -40, boxSizing: "content-box" }}>
```

## Removing Placeholder Buttons (2026-06-28)

Node control panels had star (⭐) and plus (+) buttons with NO `onClick` handlers — pure decoration. Remove them to reduce visual clutter:

```tsx
// ❌ Before: 3 buttons (star, plus, expand) — star and plus do nothing
<div style={{ display: "flex", justifyContent: "space-between", padding: "10px 14px" }}>
  <div style={{ display: "flex", gap: 6 }}>
    <button style={{...}}><svg>star</svg></button>  {/* no onClick! */}
    <button style={{...}}><svg>plus</svg></button>  {/* no onClick! */}
  </div>
  <button onClick={() => setShowPreview(true)} style={{...}}>
    <svg>expand</svg>
  </button>
</div>

// ✅ After: only expand button, right-aligned
<div style={{ display: "flex", justifyContent: "flex-end", padding: "10px 14px" }}>
  <button onClick={() => setShowPreview(true)} style={{...}}>
    <svg>expand</svg>
  </button>
</div>
```

**Rule:** Every interactive button MUST have an `onClick` handler. If it's decorative, remove it or make it functional.

## Pitfalls

**pointerEvents container blocks elements behind it (2026-06-29)**: A parent div with `pointerEvents: "auto"` and `flex: 1` covers its full allocated area (e.g. 100vh), even if the actual interactive child is only 48x48px. Elements positioned behind it (like zoom controls) become unclickable. `elementFromPoint` at the blocked position returns the container div, not the target button. **Fix**: Remove `pointerEvents: "auto"` from the container, put it only on the actual interactive element. Debug with `document.elementFromPoint(x, y)` to identify what's blocking.

**修改代码后必须确认改动实际生效再让用户测试：**
1. 前端：确认 dev server 重启成功（`curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`）
2. 后端：确认 uvicorn 重新加载（检查日志或重启）
3. 浏览器：用户必须 Cmd+Shift+R 强制刷新
4. **旧节点不受影响**：代码修改只影响新创建的节点，旧节点仍用旧逻辑。必须删除旧节点重新创建才能验证。

## Pitfalls

**问题**：toapis.com的Asset API不接受data URL和局域网URL，`source_url`必须是公开HTTP/HTTPS URL。后端的`prepare_asset`尝试下载LAN文件→转data URL→上传，会被toapis.com拒绝（"invalid request body"）。

**解决方案**：前端直接上传到toapis.com asset系统，后端跳过已上传的asset。

前端流程（拖拽/导入文件时）：
1. 上传到后端 `/api/upload` → 拿到后端URL（用于预览显示）
2. 上传到 toapis.com asset API → 拿到 `assetId`（用于生成）
3. 节点存储 `assetUrl = asset://{assetId}` + `previewUrl = 后端URL`

后端 `prepare_asset` 检测 `asset://` 前缀 → 跳过上传，直接用 `assetId`。

**关键代码见** `references/toapis-asset-upload-flow.md`

## Pitfalls
- CSS 文件返回 404
- JS chunks 加载失败
- 页面布局错乱但控制台无错误
- 幻影语法错误（文件正确但编译报错）

**根因：** `.next` 和 `.swc` 缓存积累旧编译结果，新旧代码冲突。

## toapis.com Asset 上传（2026-06-27 重要）

toapis.com Asset API **不接受** data URL 和局域网 URL。前端必须直接上传到 toapis.com 拿到 assetId，后端收到 `asset://{assetId}` 跳过上传。

详见 `references/toapis-asset-upload-architecture.md`。

**废案记录**: "前端直连 toapis.com 做所有API调用" 被阿戴否决。只在素材上传这一步前端直连，其他仍走后端代理。

**关键教训**: uploadToAsset 失败时必须 alert 报错，不能静默回退到后端URL——后续生成必报 `invalid request body`。

## Pitfalls

1. **assetUpload.ts 字段名不匹配** — 后端 `/api/upload` 返回 `{ path: "/api/upload/file/xxx" }`，但 `assetUpload.ts` 读的是 `data.url || data.asset_url`，导致 `url: undefined`。画布拖拽正确使用 `getApiBase() + data.path`。修复：加 `data.path ? getApiBase() + data.path : undefined`。
2. **Multiple edges lost** - ReactFlow's `addEdge` may deduplicate; use unique IDs with `[...s.edges, newEdge]`
2. **Only 1 incoming edge** - Must set `connectionMode={ConnectionMode.Loose}` AND filter `replace` type in `onEdgesChange`
3. **onEdgesChange replace type** - ReactFlow sends `replace` changes internally that also cause edge loss; only process `select` type
3. **Node not selected** - `stopPropagation` on preview blocks ReactFlow selection
4. **Asset name not showing** - Read from `nodeData.assetName`, not `config.assetName`
5. **@ menu empty** - Always show default mentions when no upstream assets
6. **Video not playing** - Check `hoverToPlay` prop and `isHovered` state
7. **Asset numbering duplicate** - Use max+1 logic, not count+1
8. **Handle click area too small** - Use padding+margin trick for hover zone expansion
9. **Handle hidden but clickable** - Set `pointerEvents: "none"`` when opacity is 0
10. **margin shifts node** - Use `boxSizing: "content-box"` with padding+margin trick
11. **Timer not cleared** - Always clear hideTimerRef in handleMouseEnter
12. **selectNode opens property panel** - Use `selectNodeQuietly` when you only need `selectedNodeId` without opening property panel
13. **All nodes show control panel** - Don't use global `showControlPanel` state; use `selectedNodeId === props.id` check
14. **Control panel doesn't appear on click** - Must call `selectNodeQuietly(props.id)` before `setShowControlPanel(true)`
15. **Canvas pan feels sluggish** - Add `panOnScroll`, `panOnScrollSpeed`, `autoPanOnNodeDrag`, `autoPanOnConnect` props
16. **panOnScrollMode TypeScript error** - Use `PanOnScrollMode.Free` enum, not string `"free"`
17. **Preview height always same** - Don't use fixed `height: 220`; calculate dynamically from ratio: `Math.round(280 * h / w)`
18. **Edge highlight not working** - CSS `!important` in globals.css overrides JS-set styles; remove `stroke: #ffffff !important` from `.react-flow__edge-path`
19. **resp.text is a function** - Use `await resp.text()`, not `resp.text` (returns function reference)
20. **toapis endpoints wrong** - Correct: `/video/generations`, `/images/generations`. NOT `/generate/video`. See `references/toapis-api-reference.md`
21. **LAN access fails** - toapis.com can't access `http://192.168.x.x` URLs. Solution: frontend calls toapis.com directly (CORS `*`), backend only for file upload + proxy
22. **Delete key deletes node from input** - Always check `isInputFocused` and return early, regardless of input content. Previous "empty check" caused accidental deletions
23. **Local file upload to toapis** - Data URLs rejected. Must use publicly accessible HTTP URL or binary multipart upload
19. **`resp.text` vs `resp.text()`** - In JavaScript, `resp.text` is a function reference, not a call. Always use `await resp.text()` to get the string content
20. **External API CORS** - Check `access-control-allow-origin` header before attempting direct browser calls. toapis.com supports `*`, so frontend can call directly
21. **Wrong API endpoints** - Always verify endpoints from actual API responses or documentation. Guessing `/generate/video` when it's `/video/generations` causes 404/invalid URL errors
19. **Data URLs rejected by toapis.com** - The asset API's `source_url` field requires `http://` or `https://` URLs. Data URLs (`data:image/png;base64,...`) are rejected with "http must be a valid http or https URL"
20. **LAN URLs can't be fetched by external APIs** - toapis.com fetches `source_url` server-side. LAN URLs (192.168.x.x) are unreachable. Use binary upload or direct file upload instead.
21. **Don't overcomplicate solutions** - 阿戴's preference: "你搞复杂了" (you overcomplicated it). Always check if a simpler approach exists before building complex workarounds. Example: instead of converting LAN URLs to data URLs and uploading binary, just call the external API directly from the browser.
19. **LAN access fails** - Hardcoded `localhost:8000` in 24 places; CORS blocks non-localhost origins; WebSocket also needs dynamic host. See `references/lan-access-and-file-upload.md`
20. **Local file upload to toapis.com fails** - toapis.com rejects both LAN URLs and data URLs via JSON. Must decode data URL to binary and upload via multipart form data.
21. **VPN blocks files.toapis.com** - Video preview stuck loading when VPN is active. Disable VPN or check CDN connectivity.
22. **sed import merging** - Batch sed insertions can merge two import lines. Always verify file headers after bulk edits.
20. **`updateViewport` vs `viewport`** - `updateViewport` is a setter function, `viewport` is the state object with `{x, y, zoom}`. Don't call `updateViewport.x` — use `viewport.x` from the store
21. **onPaneContextMenu TypeScript error** - ReactFlow's `onPaneContextMenu` expects `(event: MouseEvent | React.MouseEvent) => void`, not just `React.MouseEvent`
22. **File drop vs node drop** - Check `e.dataTransfer.files` BEFORE checking `application/antoken-node` data; `return` after handling file drop
23. **useCallback dependency order** - If hook A uses hook B in its deps, define B before A. TypeScript: "Block-scoped variable used before its declaration"
24. **sed breaks string quoting** - Don't use sed to replace URLs in JS/TS files; use Python `content.replace()` instead
25. **Merged import lines** - sed-added imports may merge on one line; fix with `replace('";import ', '";\nimport ')`
26. **Blob URLs inaccessible by backend** - `blob:http://...` URLs are client-side only. Must upload file to backend first, use backend URL in node data
27. **CORS blocks LAN access** - Backend `CORS_ORIGINS` must include `["*"]` or specific LAN IPs for cross-network access
28. **External API rejects local URL** - toapis.com can't access `http://192.168.x.x`; backend converts to data URL in `prepare_asset()`
29. **VPN blocks files.toapis.com** - Some VPNs cause `files.toapis.com` CDN to timeout. If video preview stuck loading, ask user to disable VPN
30. **Local assets need blob URL cleanup** - `URL.createObjectURL()` creates persistent blob URLs; consider `URL.revokeObjectURL()` on node removal
31. **HEIC format not supported by vision_analyze** - macOS screenshots from iPhone are HEIC; convert with `sips -s format png input.HEIC --out output.png`
22. **Local assets need blob URL cleanup** - `URL.createObjectURL()` creates persistent blob URLs. For production, consider `URL.revokeObjectURL()` on node removal to prevent memory leaks.
27. **VPN blocks files.toapis.com** — Some VPNs cause `files.toapis.com` CDN to timeout. If video preview stuck loading, ask user to disable VPN and retry. Direct test: `curl -s -o /dev/null -w "%{http_code} %{time_total}s" https://files.toapis.com/...`
28. **0x0.st shut down (2026-06)** — Uploads disabled due to AI botnet spam. Use tmpfiles.org instead.
29. **Proxy required for external uploads** — Mac has proxy at `127.0.0.1:6324`. External HTTP requests (file hosting, etc.) must use this proxy or they'll timeout. Backend uses `httpx.AsyncClient(proxy=PROXY)`.
30. **toapis.com only accepts public URLs** — All APIs (asset + generation) reject binary uploads, data URLs, and LAN URLs. Must upload files to public hosting (tmpfiles.org) first, then pass public URL to toapis.com.
31. **Don't confuse image API vs video API** — 阿戴: "图片生成走图片api，视频生成走视频api". Each has its own endpoint and payload format. Don't mix them up.
25. **Dev server not ready when asking user to test** — Starting `npm run dev` in background then immediately telling user to refresh Safari causes "cannot connect to server" error. ALWAYS verify with `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000` returning 200 before asking user to test. The server needs 5-8 seconds to be ready. User explicitly said: "改东西不要瞎改不要让原本好好的地方不能运行" — don't break working things by rushing.
25. **Hardcoded localhost breaks LAN** — If another device on LAN gets "Failed to fetch", the codebase still has `http://localhost:8000`. Migrate to `getApiBase()` pattern. See `references/dynamic-api-base-for-lan.md`.
26. **Backend CORS blocks LAN** — Even after fixing frontend URLs, "Failed to fetch" persists if backend `CORS_ORIGINS` only includes `localhost`. Check `backend/app/core/config.py`: change `CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]` to `CORS_ORIGINS: list[str] = ["*"]`. Then restart backend. Verify with: `curl -s -H "Origin: http://192.168.x.x:3000" -X OPTIONS http://localhost:8000/api/generate/video -I | grep access-control`
27. **toapis.com只接受公开URL** — 不能传data URL、LAN URL、或二进制文件。必须先上传到公开文件托管（tmpfiles.org），拿到公开URL后再传。详见上方"toapis.com API 素材限制"章节。
28. **0x0.st已关闭** — 2026-06-27确认uploads disabled。用tmpfiles.org替代。
29. **本地开发需要代理** — Mac上通过`127.0.0.1:6324`代理访问外部服务。上线后不需要。
30. **前端VideoNode/ImageNode也需要轮询公开URL** — 不只是画布拖拽和侧边栏导入，节点内的文件上传也要异步获取公开URL。
27. **toapis.com Asset API rejects data URLs and LAN URLs** — `source_url` in Asset API must be a publicly accessible HTTP/HTTPS URL. `data:` URLs and `http://192.168.x.x` are rejected with `{"message":"invalid request body","success":false}`. Backend's `prepare_asset` converts LAN URL → data URL → multipart upload, but toapis.com STILL rejects it. See `references/toapis-asset-upload-limits.md`.
28. **"前端直连toapis.com" is a DEAD END** — User explicitly rejected full architecture change to frontend-direct-toapis.com. DO NOT re-introduce this approach. Asset upload to toapis.com needs a different solution (frontend direct upload for assets only, or public CDN).
29. **Investigate before fixing** — User rule: "先检查先不要乱改". Always examine logs, trace the code path, and explain the root cause BEFORE making any code changes. Don't guess and patch.
25. **assetUpload.ts returns url: undefined** — Backend `/api/upload` returns `{ path: "/api/upload/file/xxx.ext" }`, NOT `{ url: "..." }`. The `uploadAsset()` function used `data.url || data.asset_url` → both undefined → `url: undefined`. Fix: `data.path ? getApiBase() + data.path : undefined`. Canvas drag-and-drop worked because it manually concatenated `getApiBase() + data.path`. This caused LAN users to have empty assetUrl on VideoNode/ImageNode direct uploads.
26. **Module-level API_BASE breaks LAN** — `const API_BASE = getApiBase()` at module load time captures `localhost` before LAN context is available. Must call `getApiBase()` at invocation time, not store it. Pattern: remove `const API_BASE = getApiBase();` line, replace all `API_BASE` refs with inline `getApiBase()`.
25. **Hardcoded localhost breaks LAN** — If another device on LAN gets "Failed to fetch", the codebase still has `http://localhost:8000`. Migrate to `getApiBase()` pattern. See `references/dynamic-api-base-for-lan.md`.
26. **Backend CORS blocks LAN** — Even after fixing frontend URLs, "Failed to fetch" persists if backend `CORS_ORIGINS` only includes `localhost`. Check `backend/app/core/config.py`: change `CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]` to `CORS_ORIGINS: list[str] = ["*"]`. Then restart backend. Verify with: `curl -s -H "Origin: http://192.168.x.x:3000" -X OPTIONS http://localhost:8000/api/generate/video -I | grep access-control`
27. **toapis.com只接受公开URL** — 不能传data URL、LAN URL、或二进制文件。必须先上传到公开文件托管（tmpfiles.org），拿到公开URL后再传。详见上方"toapis.com API 素材限制"章节。
28. **0x0.st已关闭** — 2026-06-27确认uploads disabled。用tmpfiles.org替代。
29. **本地开发需要代理** — Mac上通过`127.0.0.1:6324`代理访问外部服务。上线后不需要。
30. **前端VideoNode/ImageNode也需要轮询公开URL** — 不只是画布拖拽和侧边栏导入，节点内的文件上传也要异步获取公开URL。
26. **assetUpload.ts returns undefined url** — Backend `/api/upload` returns `{path: "/api/upload/file/xxx"}`, NOT `{url: ...}`. Must use `data.path` with `getApiBase()` prefix: `data.url || data.asset_url || (data.path ? getApiBase() + data.path : undefined)`
27. **toapis.com rejects data URLs and LAN URLs** — Asset API `source_url` must be publicly accessible HTTP/HTTPS. Backend's download→data URL→upload approach FAILS. Must upload directly from frontend to toapis.com. See `references/toapis-asset-upload-flow.md`
28. **Silent fallback creates broken nodes** — If `uploadToAsset` fails (quota, network), DON'T silently create node with backend URL. Show alert and abort. Otherwise generation fails later with confusing "invalid request body" error.
29. **Preview URL vs Generation URL** — Nodes need TWO URLs: `assetUrl = asset://{assetId}` for generation, `previewUrl = backend URL` for display. Preview components must read `previewUrl` first, fall back to `assetUrl`. `asset://` URLs are NOT valid for `<img>` or `<video>` src.
31. **Old nodes won't work after asset upload fix** — Nodes created before the toapis direct upload change have `assetUrl = backend URL`. User must create NEW nodes after the fix. Old nodes silently fail during generation.
32. **VideoGenNode missing upstream asset collection** — Unlike ImageGenNode and ImageNode which have `getUpstreamAssets()` to collect `reference_image_urls`/`reference_video_urls` from connected upstream nodes, VideoGenNode.tsx has NO such logic. It directly calls `/api/generate/video` without collecting upstream references. This means connected upstream image/video nodes are silently ignored during video generation. Fix: add the same `getUpstreamAssets` pattern from ImageGenNode to VideoGenNode. See `references/videogen-upstream-asset-gap.md`.
33. **Image API doesn't support video_urls** — toapis.com Gemini 3.1 Flash Image API only accepts `image_urls`, NOT `video_urls`. When upstream is video, backend must extract first frame via `extract_video_frame()` and pass as image reference. Google's native API supports video-to-image but toapis.com doesn't expose it.
34. **VideoNode ratio vs resolution conflict** — VideoNode sends both `ratio: "9:16"` and `resolution: "720p"`. Backend's `resolution_to_ratio("720p")` returns `"16:9"`, ignoring the `ratio` value. Fix: backend must check `ratio` first (if contains ":"), then fall back to `resolution` conversion. See "VideoNode 同时发送 ratio 和 resolution 的陷阱" section above.
31. **Debug logging with prefixes** — When debugging upload/generation flow, use `console.log("[Upload] ...")`, `console.log("[Asset] ...")`, `console.log("[Generate] ...")` with descriptive prefixes. Helps trace the exact flow in browser console.
26. **assetUpload.ts returns undefined URL** — `uploadAsset()` returns `url: data.url || data.asset_url` but backend `/api/upload` returns `data.path`, not `data.url`. Result: `assetUrl = undefined` in node data. Canvas-level `uploadToBackend()` correctly does `getApiBase() + data.path`. Node-level upload (VideoNode/ImageNode) uses the broken path. See `references/asset-upload-path-analysis.md` for full analysis.
27. **Three upload paths store URLs differently** — (a) Canvas drag-and-drop → `assetUrl` = backend URL ✓ (b) Node-level upload → `assetUrl = undefined` ❌ (c) AI generation → `resultUrl` only, no `assetUrl`. VideoNode's `getUpstreamAssets()` only reads `assetUrl`, so AI-generated materials are never sent for composition. See `references/asset-upload-path-analysis.md`.
28. **LAN URL "invalid request body" from toapis.com** — When backend receives LAN URL for asset upload, `prepare_asset` downloads from self → converts to data URL → multipart upload. If download fails, falls back to passing raw LAN URL as JSON `source_url` → toapis.com can't access private IP → returns `{"message":"invalid request body","success":false}`. Check backend logs for `[Upload] 下载本地文件失败` to confirm. See `references/asset-upload-path-analysis.md`.
