# Module Splitting Pattern for DeepSeek Code Review

## When to Split
- Single module > 80KB → split into sub-modules (6a, 6b, 6c...)
- DeepSeek has token limits — smaller modules get better review quality

## Antoken v2 Module Map (2026-07-04)

### Core Modules (1-5)
| Module | Content | Size | Files |
|--------|---------|------|-------|
| 1: State | workflow-store-jotai, settings-store-jotai, project-store, compat | ~18KB | 5 |
| 2: Hooks | execution, keyboard, upload, upstream, poll | ~21KB | 5 |
| 3: Nodes | base/image/video/text/composite + index | ~93KB | 6 |
| 4: Canvas | persistent-canvas, panels, zoom, context-menu, sidebar, preview, toolbar, providers | ~97KB | 14 |
| 5: Backend | FastAPI routes, schemas, services, tests | ~42KB | 26 |

### Module 6 Split (when > 80KB)
| Sub | Content | Size | Files |
|-----|---------|------|-------|
| 6a | Auth + core libs (supabase, api, media-proxy, upload, constants, validation) | ~23KB | 12 |
| 6b | Ecommerce + commercial (templates, batch, presets, collaboration, pricing, stripe) | ~32KB | 8 |
| 6c | Types + styles + pages (workflow types, API types, globals.css, all route pages) | ~80KB | 22 |
| 6d | Landing Page (12 section components) | ~24KB | 12 |
| 6e | UI components + config + Sentry (shadcn/ui, sentry configs, package.json, tailwind, etc.) | ~50KB | 23 |

## Generation Method
Always use `terminal` + shell `cat` loop, NOT `execute_code`.
`execute_code` has a 50 tool-call limit — reading 70+ files silently fails (empty output, no error).

## Delivery Flow
1. Generate all module files → verify each is non-empty with `wc -c`
2. `cat /tmp/antoken-module{N}-{name}.txt | pbcopy` one at a time
3. 阿戴 says "继续/下一个" → copy next module
4. After all sent → wait for DeepSeek feedback
