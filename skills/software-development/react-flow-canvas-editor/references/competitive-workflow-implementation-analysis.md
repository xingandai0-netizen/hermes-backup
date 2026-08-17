# Competitive Workflow Implementation Analysis (Source-Code Level)

## Research Methodology

Use delegate_task with 3 parallel subagents, each targeting one competitor:
- Each subagent gets ['web', 'browser'] toolsets
- Goal must specify: "read actual source code, not README"
- Each subagent outputs to stdout (no file writing needed)
- Parent agent synthesizes findings after all complete

## TapNow Studio (chapterv/Tapnow-Studio-PP)

### Connection System
- Data structure: {id, from, to, inputType} -- NO sourcePort/targetPort
- inputType: 'default' | 'oref' | 'sref' -- only 3 types
- No type compatibility validation -- any output connects to any input
- Duplicate prevention: same from+to+inputType combo
- oref/sref: one-to-one (new replaces old); default: many-to-many
- Style: fixed gray SVG bezier, not port-type-dependent

### Execution Model
- NO unified execution engine -- event-driven, per-node trigger
- User clicks node generate button -> startGeneration() -> API call -> poll -> update preview
- Data propagation: downstream PULLS from upstream via getConnectedInputImages()
- NodeIOEnvelope: {version, kind, media:[{url,type}], text, meta}
- Cache: useMemo on connections+nodes dependency

### Asset Storage (3-tier)
1. IndexedDB (tapnow_images_db) via LocalImageManager -- primary
2. localStorage (tapnow_autosave) -- metadata
3. Memory cache (blobUrlCache Map) -- fastest

### Batch Processing
- Storyboard node manages multiple shots
- State machine: idle -> running -> cooling (1s cooldown)
- Pipeline (serial) and Parallel (configurable concurrency) modes
- 60s timeout watchdog, 5s re-evaluation interval

## Lovart (lovartai/lovart-skill)

### Architecture
- Skill is pure messenger -- all intelligence server-side
- MCoT engine on server: task decomposition + model routing
- Client sends prompt, polls status, downloads artifacts

### API Call Chain
send(prompt) -> POST /v1/openapi/chat -> thread_id
poll(thread_id) -> GET /status every 3s
  -> status=="done" -> wait 5s (sub-agent race protection)
  -> check pending_confirmation (high-cost ops)
get_result(thread_id) -> items[] with text + artifacts

### Artifact Handling
- Upload: multipart/form-data -> CDN URL
- Attachments: URL string array in request body
- Download: SHA1 hash URL as filename (idempotent)
- Canvas sync: automatic on result fetch, idempotent

## LiblibAI (liblib-mcp-server, alphasnow/liblib)

### ComfyUI Workflow API
- Submit: POST /api/generate/comfyui/app
- Body: {templateUuid, generateParams: {workflowUuid, "nodeId": {class_type, inputs}}}
- User provides override params only -- full graph stored server-side
- Server does DAG topo-sort internally

### Async Task Status Codes
1=Waiting, 2=Running, 3=Image generated, 4=Under review, 5=Success, 6=Failed

### Asset Transfer
- Direct URL passing (no pre-upload required for most cases)
- image_with_roles: [{url, role:'first_frame'|'last_frame'|'reference'}]
- image_urls and image_with_roles cannot be used simultaneously
- Auth: HMAC-SHA1 signature (more complex than Bearer token)

## Key Differences Summary

| Dimension | TapNow | Lovart | LiblibAI | Antoken |
|-----------|--------|--------|----------|---------|
| Execution | Per-node trigger | Server agent | Server DAG | Per-node direct API |
| Data flow | Pull via envelope | Server-managed | Server-managed | Pull via config |
| Connections | Free (no validation) | None (chat) | ComfyUI native | Warn but allow |
| Storage | 3-tier IndexedDB | CDN URL | OSS URL | localStorage only |
| Batch | State machine+cooldown | Agent-managed | ComfyUI batch | None |
