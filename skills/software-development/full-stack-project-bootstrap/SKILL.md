---
name: full-stack-project-bootstrap
description: "Bootstrap a full-stack web project with parallel frontend/backend delegation. Covers project skeleton creation, dependency installation, build verification, and common pitfalls."
version: 1.0.0
author: xiaohei
triggers:
  - 搭建项目
  - 新建项目
  - 初始化前后端
  - bootstrap project
  - scaffold full-stack
  - create new app
---

# Full-Stack Project Bootstrap

When 阿戴 asks to build a new web application from scratch, use this workflow. The pattern is: **skeleton → parallel delegation → fix → install → verify**.

## Standard Workflow

### Phase 1: Project Skeleton (agent creates directly)
```bash
mkdir -p ~/projectname/{frontend/src/{app,components,stores,hooks,types,lib,styles},backend/app/{api,core,models,schemas,services},docs}
```
- Create README.md with tech stack table, quick start, project structure, core features
- Create directory structure matching the expected layout

### Phase 2: Parallel Delegation (delegate_task with 2 tasks)
Delegate frontend and backend to separate subagents simultaneously:

**Frontend subagent receives:**
- Project path, tech stack (Next.js / React Flow / Zustand / Tailwind)
- Complete file list with descriptions
- Design requirements (theme colors, port colors, size presets)
- Key pitfalls to avoid (see references/reactflow-v12-pitfalls.md)

**Backend subagent receives:**
- Project path, tech stack (FastAPI / SQLAlchemy / Pydantic)
- Complete file list with descriptions
- API endpoint definitions
- Environment variable placeholders (URL/KEY empty → mock data)

### Phase 3: Fix Build Errors
After delegation completes:
1. `cd frontend && npx next build` — catches TypeScript errors that `npm run dev` misses
2. Fix errors iteratively (common ones in references/)
3. `cd backend && python -c "from app.main import app"` — catches import errors

### Phase 4: Install Dependencies
```bash
# Frontend
cd frontend && npm install

# Backend (NEVER use system pip on macOS Homebrew Python)
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### Phase 5: Verify
```bash
# Frontend build pass
cd frontend && npx next build

# Backend starts
cd backend && ./venv/bin/uvicorn app.main:app --reload
```

### Phase 6: API Configuration (MANDATORY for AI tools)
If the project calls any AI model API, it MUST have a settings modal from day one. Users will immediately ask "where do I put my API key?"

1. Create `stores/settingsStore.ts` — Zustand store with apiUrl, apiKey, modelName, load/save to localStorage
2. Create `components/settings/SettingsModal.tsx` — modal with URL input, key input (password toggle), model dropdown, test connection button
3. Add settings button to top bar in `page.tsx`
4. Show API status indicator (green "已连接" / yellow "未配置")

See `react-flow-canvas-editor` skill for full implementation code.

**PITFALL**: Never leave API URL/Key as hardcoded empty strings with no UI to set them. User will hit this immediately and lose confidence in the project.

### Phase 7: Model Discovery (for AI generation projects)
If the project generates images/videos via AI APIs, add auto model discovery:

1. Backend: `services/model_discovery.py` — fetch `/v1/models`, classify by keywords + endpoint types
2. Backend: `GET /api/generate/models/discover` endpoint
3. Frontend: "自动发现模型" button in settings modal
4. Show available models as clickable tags

**PITFALL:** Don't hardcode model names. Different API proxies use different names for the same model. Always discover from the API and fuzzy-match.

**PITFALL:** Always test API calls with curl before writing integration code. Don't assume a model or endpoint works — verify it.

## Pitfalls

### 1. Python 3.14+ and pydantic-core
pydantic-core fails to compile on Python 3.14+. Workaround:
```bash
./venv/bin/pip install --no-deps fastapi pydantic
./venv/bin/pip install uvicorn sqlalchemy pydantic-settings python-jose passlib python-multipart websockets aiofiles httpx aiosqlite
./venv/bin/pip install starlette annotated-doc  # fastapi deps sometimes missed
```

### 2. macOS Homebrew Python PEP 668
Never `pip install` directly on Homebrew Python 3.12+. Always create a venv first:
```bash
python3 -m venv venv && source venv/bin/activate
```

### 3. npm install timeout
`npm install` can take 2-3 minutes for large projects. Set timeout=300.

### 4. TypeScript errors hidden by dev mode
`npm run dev` compiles lazily and hides type errors. Always run `npx next build` to catch them all.

### 5. User says "一个个继续完成"
When 阿戴 has multiple pending tasks and says "一个个继续完成" or similar, execute them sequentially WITHOUT asking for confirmation between steps. Just do them one by one and report progress.

## References
- `references/reactflow-v12-pitfalls.md` — React Flow v12 TypeScript gotchas
- `references/fastapi-project-template.md` — Standard FastAPI project structure
- `references/nextjs-supabase-auth.md` — Next.js 14 + Supabase Auth integration guide
- `references/vercel-railway-cloudflare-deploy.md` — Vercel + Railway + Cloudflare deployment guide
- `references/antoken-deployment-case-study.md` — Real deployment case study with issues encountered
