# Antoken Project Structure (Real-World Example)

## Overview
E-commerce AI workflow platform with infinite canvas editor. Built with Next.js 14 + React Flow v12 + Zustand + Tailwind CSS + FastAPI.

## Frontend Structure
```
frontend/src/
├── app/
│   ├── layout.tsx          # Root layout, imports styles
│   ├── page.tsx            # Main page: sidebar + canvas + panels
│   └── globals.css         # Unused (styles in styles/)
├── components/
│   ├── canvas/
│   │   ├── WorkflowCanvas.tsx  # ReactFlow + drop handler + empty state
│   │   └── CanvasControls.tsx  # Zoom/fit/minimap buttons
│   ├── nodes/
│   │   ├── BaseNode.tsx        # Universal shell (memo + children)
│   │   ├── ImageGenNode.tsx    # Prompt input + generate button + preview
│   │   ├── VideoGenNode.tsx    # Same pattern for video
│   │   ├── Img2VideoNode.tsx   # Image-to-video with source image detection
│   │   ├── SKUImportNode.tsx   # CSV/Excel drag-drop upload
│   │   ├── ImageProcessNode.tsx
│   │   ├── SizeAdapterNode.tsx # E-commerce size presets
│   │   ├── ExportNode.tsx
│   │   └── index.ts            # nodeTypes registry (module level!)
│   ├── sidebar/
│   │   └── NodePanel.tsx       # Click-to-add + drag-to-canvas
│   ├── properties/
│   │   ├── PropertyPanel.tsx   # Double-click opens inspector
│   │   └── fields/             # TextField, SelectField, NumberField, ImageSizeField
│   ├── execution/
│   │   └── ExecutionPanel.tsx  # Workflow execution status
│   └── settings/
│       └── SettingsModal.tsx   # API config + model discovery
├── stores/
│   ├── workflowStore.ts        # Nodes/edges CRUD + undo/redo + localStorage
│   └── settingsStore.ts        # Multi-provider API config (imageApi + videoApi)
├── hooks/
│   ├── useWebSocket.ts         # Auto-reconnect + heartbeat
│   └── useKeyboardShortcuts.ts # Ctrl+Z undo, Del delete
├── types/
│   ├── workflow.ts             # NodeData extends Record<string, unknown>
│   └── api.ts
├── lib/
│   ├── api.ts              # getApiBase() for dynamic LAN access
│   ├── assetUpload.ts      # File upload to backend
│   ├── mediaProxy.ts       # CORS proxy for external media
│   ├── constants.ts            # Port colors, category colors, size presets
│   └── validation.ts           # TYPE_COMPAT matrix for connection validation
└── styles/
    └── globals.css             # Linear design system + React Flow overrides
```

## Backend Structure
```
backend/app/
├── main.py                     # FastAPI app + CORS + router registration
├── api/
│   ├── auth.py                 # JWT login/register
│   ├── workflows.py            # CRUD + version management + rollback
│   ├── executions.py           # Start/cancel/status
│   ├── generate.py             # Image/video generation (async task model)
│   ├── upload.py               # File upload endpoint for local assets
│   └── ws.py                   # WebSocket execution progress
├── core/
│   ├── config.py               # Pydantic Settings
│   ├── database.py             # SQLAlchemy async engine
│   ├── security.py             # JWT + bcrypt
│   └── deps.py                 # FastAPI dependencies
├── models/                     # SQLAlchemy models
├── schemas/                    # Pydantic schemas
└── services/
    ├── workflow_engine.py      # DAG execution (Kahn + parallel)
    ├── ai_client.py            # AI API client
    ├── content_safety.py       # Content moderation (placeholder)
    └── model_discovery.py      # Auto-discover image/video models
```

## Key Design Decisions
1. **Click-to-add from sidebar** — Users expect clicking to add nodes, not just drag
2. **Async task polling** — Image/video APIs return task IDs, frontend/backend poll for completion
3. **Multi-provider support** — Separate imageApi and videoApi configs in settings
4. **Model auto-discovery** — Fetch `/v1/models`, classify by keywords + endpoint types
5. **Linear dark theme** — `#08090a` bg, `#f7f8f8` text, `#5e6ad2` accent, semi-transparent borders
