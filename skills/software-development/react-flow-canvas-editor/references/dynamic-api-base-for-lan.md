# Dynamic API Base URL for LAN Access

## Problem

Hardcoding `http://localhost:8000` in frontend fetch calls means the app ONLY works when accessed from the same machine. Other devices on the LAN (e.g., testing on a phone or another PC at `http://192.168.x.x:3000`) get "Failed to fetch" because their `localhost` doesn't have the backend.

## Solution

Create a single `getApiBase()` utility that dynamically resolves the backend URL based on the browser's current hostname:

```typescript
// src/lib/api.ts
export function getApiBase(): string {
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8000`;  // backend always on :8000
  }
  return 'http://localhost:8000';  // SSR fallback
}
```

Then replace ALL hardcoded `http://localhost:8000` references across the codebase.

## Migration Steps

1. Create `src/lib/api.ts` with `getApiBase()`
2. Find all files: `grep -rl 'localhost:8000' src/ --include='*.ts' --include='*.tsx'`
3. For each file:
   - Add `import { getApiBase } from "@/lib/api";` (after the first import line)
   - Replace `"http://localhost:8000/api/..."` → `getApiBase() + "/api/..."`
   - Replace `'http://localhost:8000/api/...'` → `getApiBase() + '/api/...'`
   - Replace template literals: `` `http://localhost:8000/api/...` `` → `` `${getApiBase()}/api/...` ``
   - Replace WebSocket: `ws://localhost:8000` → dynamic based on protocol
4. Also update any constant definitions:
   - `const API_BASE = "http://localhost:8000"` → `const API_BASE = getApiBase()`
   - `const PROXY_BASE = 'http://localhost:8000/api/...'` → `const PROXY_BASE = getApiBase() + '/api/...'`
5. Build to verify: `npm run build`

## Antoken-Specific: 14 Files Updated (2026-06-25)

Files that had `http://localhost:8000` hardcoded:
- `lib/assetUpload.ts` — API_BASE constant
- `lib/mediaProxy.ts` — PROXY_BASE constant
- `components/settings/SettingsModal.tsx` — model discovery
- `hooks/useWorkflowExecution.ts` — workflow execution + WebSocket
- `components/nodes/CompositeNode.tsx`
- `components/nodes/ImageExportNode.tsx`
- `components/nodes/ImageGenNode.tsx`
- `components/nodes/ImageNode.tsx`
- `components/nodes/Img2VideoNode.tsx`
- `components/nodes/VideoCompositeNode.tsx`
- `components/nodes/VideoExportNode.tsx`
- `components/nodes/VideoGenNode.tsx`
- `components/nodes/VideoNode.tsx`

## WebSocket Fix

For WebSocket connections, detect protocol dynamically:
```typescript
const wsUrl = `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.hostname}:8000/ws/...`;
const ws = new WebSocket(wsUrl);
```

## Pitfalls

1. **sed replacement breaks quotes** — When doing bulk replacement of `"http://localhost:8000`, sed eats the opening quote. Use Python string replacement instead:
   ```python
   content = content.replace('"http://localhost:8000', 'getApiBase() + "')
   content = content.replace("'http://localhost:8000", "getApiBase() + '")
   ```
2. **Import on same line** — sed `a\` appends can merge imports on one line. Verify with `grep -n 'getApiBase.*import'` after batch edits.
3. **Template literals need `${}`** — `` `http://localhost:8000/api/${id}` `` → `` `${getApiBase()}/api/${id}` `` (not `getApiBase() + '/api/' + id` inside template)
4. **Constants must be function calls** — `const API_BASE = getApiBase()` works at module load time in client components (`"use client"`), but NOT in SSR. For SSR-safe code, call `getApiBase()` inline at each use site.
5. **Backend CORS also blocks LAN** — Even after fixing all frontend URLs, "Failed to fetch" persists if the backend CORS config only allows `localhost`. In `backend/app/core/config.py`, change `CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]` to `CORS_ORIGINS: list[str] = ["*"]`. Restart backend after change. Verify with: `curl -s -H "Origin: http://192.168.x.x:3000" -H "Access-Control-Request-Method: POST" -X OPTIONS http://localhost:8000/api/generate/video -I | grep access-control`
