# Antoken v2 Production Architecture

Case study: production React Flow canvas app with Jotai + FastAPI + Supabase. This is a reference for building similar apps, not a standalone guide.

## Architecture

```
Frontend (Next.js 14)          Backend (FastAPI)
├── React Flow canvas          ├── /api/generate/* (AI generation)
├── Jotai state management     ├── /api/upload (file upload)
├── Supabase auth              ├── /api/generate/proxy (media proxy)
└── Tailwind CSS               └── Supabase (database + auth)
```

## Key Design Decisions

### State Management: Jotai atomFamily (not Zustand)
- `atomFamily` from `jotai/utils` for node-level precise subscriptions
- `nodesAtom` typed as `Node<NodeData>[]`, eliminates all `as NodeData` assertions
- Action atoms return void, enforcing unidirectional data flow
- Snapshot strategy separated: regular operations vs drag-end

### API Key Security: All through backend proxy
- Frontend stores NO API keys
- All AI generation requests go through backend `/api/generate/*`
- Backend reads keys from environment variables
- `settings-store-jotai.ts` only exposes `apiUrl` and `modelName`, not `apiKey`

### Node Component Pattern
- All node components wrapped with `React.memo`
- Use `useAtomValue(upstreamNodesAtomFamily(props.id))` for upstream data
- Use `useAtomValue(mentionsAtomFamily(props.id))` for mentions
- Never subscribe to global `nodesAtom`/`edgesAtom` directly

### Upload Flow
- All uploads through backend `/api/upload` endpoint
- `useAssetUpload` Hook encapsulates complete flow
- After upload, auto-starts `usePollPublicUrl` polling
- `assetUrl` uses top-level field, NOT `config.assetUrl`

### Keyboard Shortcuts
- Use `useRef` for `selectedNodeId` to avoid re-binding event listeners
- Ctrl+Z undo, Ctrl+Shift+Z / Ctrl+Y redo
- Input focus protection (skip when in INPUT/TEXTAREA/SELECT)

## Backend Patterns

### Supabase Client Singleton
```python
from functools import lru_cache

@lru_cache()
def get_supabase() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
```

### Credit Deduction Atomic Operation
- Use Supabase RPC function `deduct_credits`
- Database-level row lock for concurrency safety
- SQL migration: `migrations/001_deduct_credits_rpc.sql`

### Stripe Webhook
- Pass `metadata.user_id` and `metadata.plan` when creating Checkout Session
- Webhook reads metadata to update subscription status

## Code Review Workflow

### Module Split (v2 actual sizes)
```
Module 1: State management (stores/)     ~18KB, 5 files
Module 2: Hooks (hooks/)                 ~21KB, 5 files
Module 3: Node components (nodes/)       ~93KB, 6 files
Module 4: Canvas/UI (canvas/ etc.)       ~97KB, 14 files
Module 5: Backend (backend/)             ~42KB, 26 files
Module 6: Account/tools/Types/config     ~209KB, 70+ files (must split 6a-6e)
```

### Verification Protocol
```
1. search_files confirms old code removed
2. search_files confirms new code added
3. npm run build confirms no errors
4. npm test confirms tests pass
```

### Common Findings
- cfg closure issues (useCallback with stale closures)
- Global state subscription (useAtomValue causing full re-renders)
- Field path inconsistency (data.assetUrl vs data.config.assetUrl)
- Type safety (any types, weak type parameters)

## Deployment (Vercel + Railway + Cloudflare)

### Architecture
```
User → Cloudflare (DNS/CDN) → Vercel (Next.js frontend)
                                    ↓
                              Supabase (database)
                                    ↓
                              FastAPI backend (Railway)
```

### Critical Pitfalls
- **Cloudflare SSL**: Must use Full mode (not Flexible) — Flexible causes redirect loops
- **Railway Dockerfile**: Must use `${PORT:-8000}` env var, not hardcoded port
- **Railway runtime.txt**: Specify `python-3.11.9` (3.13 breaks pydantic-core)
- **Vercel domain**: Must bind domain: `vercel domains add antokex.com frontend`

### Deploy Commands
```bash
cd ~/antoken/frontend && npx vercel --prod --yes --force
cd ~/antoken && git add -A && git commit -m "msg" && git push origin main
```

## Backend Security Patterns

### Global Exception Handler
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please contact support."}
    )
```

### SSRF Protection (media proxy)
```python
def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return False
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        if hostname in ('localhost', '127.0.0.1', '0.0.0.0'):
            return False
    return True
```

### Config Startup Validation
```python
class Settings(BaseSettings):
    def validate_required(self):
        missing = []
        if not self.SUPABASE_URL: missing.append("SUPABASE_URL")
        if not self.TOAPIS_API_KEY: missing.append("TOAPIS_API_KEY")
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")

@app.on_event("startup")
async def startup():
    settings.validate_required()
    get_supabase()  # Warm up connection
```

## Multi-Reference Architecture

Support multi-image reference (style, subject, composition) via ReferenceRole:

```typescript
export type ReferenceRole = 'style' | 'subject' | 'composition' | 'content';

export interface UpstreamNode {
  node: Node<NodeData>;
  edge: Edge;
  assetName: string;
  assetType?: string;
  assetUrl?: string;
  role: ReferenceRole;  // From edge.targetHandle
}
```

## Image Preview Optimization

Backend proxy adds image scaling for 2K/4K previews:
```typescript
// Frontend
<img src={proxyUrl(previewUrl, 320, previewHeight)} />

// Backend: Pillow resize + local cache (/tmp/antoken_proxy_cache)
```

## CSS/Layout Rules

### Apple Glass Design System
```
Background:    rgba(28, 28, 30, 0.85/0.9)
Glass effect:  backdropFilter: saturate(180%) blur(20px)
Border:        0.5px solid rgba(255, 255, 255, 0.08/0.12)
Radius:        16px (cards/modals), 12px (controls)
Text:          rgba(235,235,245,0.9) primary, 0.5 secondary, 0.3 weak
Primary:       rgba(10, 132, 255, 0.8) buttons
Input:         bg: rgba(255,255,255,0.04), border: 0.5px solid rgba(255,255,255,0.08)
```

### shadcn Select White Screen in Nodes
All selectors inside nodes must use native `<select>` + inline styles, not shadcn Select (CSS variable scoping issue).

### pointer-events Layering
Parent `pointer-events-none` overrides child `pointer-events: auto`. Interactive UI elements must be moved out of that container.

## Undo/Redo Unsolved Problem

React Flow + Jotai/Zustand architecture has state sync issues with undo/redo:
- Zustand/Jotai state restores correctly (logs prove it), but React Flow UI doesn't refresh
- `key={undoVersion}` approach is unstable
- React Flow maintains its own internal node state cache

**Suggested direction**: React Flow Pro's useUndoRedo hook, or zustand-undo middleware.

## Repository Paths
- `/Users/macpro/antoken-v2` = v2 production (remote: antoken.git) ← USE THIS
- `/Users/macpro/antoken` = v1 backup (remote: antoken1.git) ← LOCKED

## File Structure
```
frontend/src/
├── stores/
│   ├── workflow-store-jotai.ts   # Core canvas state (atomFamily)
│   ├── settings-store-jotai.ts   # Settings (no apiKey)
│   └── settings-store-compat.ts  # Compat layer (useMemo)
├── hooks/
│   ├── use-upstream-data.ts      # atomFamily precise subscription
│   ├── use-poll-public-url.ts    # Polling interruption (AbortController)
│   ├── use-asset-upload.ts       # Unified file upload
│   └── use-keyboard-shortcuts.ts # Shortcuts (useRef optimization)
├── components/
│   ├── nodes/                    # React.memo wrapped
│   ├── canvas/                   # Canvas components
│   └── error-boundary.tsx        # Global error boundary
└── types/
    └── workflow-v1.ts            # NodeData type definition

backend/
├── app/
│   ├── main.py                   # FastAPI entry
│   ├── config.py                 # Pydantic v2 config
│   ├── database.py               # Supabase singleton
│   ├── api/v1/                   # API routes
│   └── services/                 # Business logic
└── migrations/                   # SQL migrations
```

## toapis.com API Integration

### Image Generation
- Endpoint: `POST /v1/images/generations`
- Parameter: `aspect_ratio` (NOT `size`, `ratio`)
- Resolution via `metadata.resolution`: `0.5K`, `1K`, `2K`, `4K`
- Reference images: `image_urls` array (max 14)

### Video Generation
- Endpoint: `POST /v1/videos/generations`
- Parameter: `aspect_ratio` (NOT `ratio` — silently ignored!)
- Modes: text-to-video, first_frame, first_last_frame, reference

### Text Generation
- Endpoint: `POST /v1/chat/completions` (OpenAI compatible)
- Must use `messages` format, NOT `prompt` field (causes 500 error)

### Key Limitations
- Only public HTTP/HTTPS URLs (no data URLs, no LAN)
- Content moderation rejects "sensitive content"
- Async task pattern: submit → poll `GET /v1/tasks/{task_id}`
