---
name: browser-use-automation
category: automation
description: >
  Browser-use (91K+ stars) AI web automation framework. Use for ANY browser automation task:
  web scraping, form filling, website interaction, data extraction, UI testing, screenshot capture,
  multi-tab browsing. Triggers: browser, scrape, crawl, fill form, interact with website, web automation.
---

# Browser-Use Deep Architecture & Usage Guide

## Overview
Browser-use is a 91K+ star Python framework that lets LLMs control a real Chromium browser.
It combines Playwright (via CDP) with an LLM-powered agent loop to automate any web task.

## Architecture (5 Layers)

```
Agent Layer (orchestration loop)
  ├── LLM Layer (OpenAI/Google/Azure/Browser-Use cloud)
  ├── Browser Layer (CDP-based Chromium control)
  ├── DOM Layer (accessibility tree + DOM serialization)
  └── Tools Layer (action registry + execution)
```

### Layer 1: Agent (agent/ — 11 files)
Core class: `Agent` in `agent/service.py`
- Orchestrates the LLM → browser → tools loop
- Uses `MessageManager` for conversation state + history compaction
- Uses `SystemPrompt` for dynamic prompt generation
- Supports multi-step reasoning, error recovery, task decomposition

Key classes:
- `Agent(service.py)` — Main orchestrator. Imports: EventBus (bubus), pydantic, MessageManager, SystemPrompt, AgentHistoryList, Tools, BrowserSession, TokenCost, FileSystem, ProductTelemetry
- `AgentState(views.py)` — Runtime state tracking
- `AgentHistory(views.py)` — Step-by-step history with screenshots
- `MessageManager(message_manager/service.py)` — Conversation management with compaction (keeps first + recent items, omits middle when exceeding max_history_items)
- `SystemPrompt(prompts.py)` — Dynamic system prompt with agent history items, max_history_items limit
- `AgentOutput(views.py)` — Structured LLM output model
- `AgentStepInfo(views.py)` — Per-step metadata

MessageManager compaction: When history exceeds max, keeps first item (initialization), adds `<sys>[... N previous steps omitted...]</sys>`, then most recent items. `add_new_task()` wraps in `<follow_up_user_request>` tags.

### Layer 2: LLM (llm/ — 52 files)
Protocol: `BaseChatModel` in `llm/base.py`
- Runtime-checkable Protocol with `ainvoke(messages, output_format)` method
- Returns `ChatInvokeCompletion` with usage tracking

Providers (all implement BaseChatModel):
- `ChatOpenAI(llm/openai/chat.py)` — AsyncOpenAI wrapper, reasoning_effort, frequency_penalty=0.3, structured output via response_format
- `ChatGoogle(llm/google/chat.py)` — Gemini via google.genai, thinking_budget, Vertex AI support
- `ChatAzureOpenAI(llm/azure/chat.py)` — Azure OpenAI, auto-detects Responses API for codex models
- `ChatBrowserUse(llm/browser_use/chat.py)` — Cloud API at llm.api.browser-use.com, models: bu-latest, bu-1-0, bu-2-0
- `ChatCerebras(llm/cerebras/)` — Cerebras inference
- `ChatMistral(llm/mistral/)` — Mistral AI

Model factory: `get_llm_by_name(name)` in `llm/models.py` — parses "provider_model" format

### Layer 3: Browser (browser/ — 28+ files)
Core: `BrowserSession` in `browser/session.py`
- CDP-based Chromium control via `cdp_use` library
- Manages pages, tabs, navigation, screenshots
- Event-driven architecture via `EventBus` (from bubus)
- `BrowserProfile(session.py)` — Configuration: headless, viewport, proxy, user-agent, extensions

Key classes:
- `BrowserSession` — Main browser controller (CDP connection, page management)
- `BrowserProfile` — Browser configuration dataclass
- `CDPClient` — Chrome DevTools Protocol client (from cdp_use)
- `EventBus` — Event system from bubus library
- Watchdogs (14 files) — Health monitoring, crash recovery, session management
- `demo_mode.py` — Step-by-step visualization mode
- `cloud/cloud.py` — Cloud browser support via browser-use SDK

Browser events (tools/service.py imports):
ClickCoordinateEvent, ClickElementEvent, CloseTabEvent, GetDropdownOptionsEvent,
GoBackEvent, NavigateToUrlEvent, ScrollEvent, ScrollToTextEvent, SendKeysEvent,
SwitchTabEvent, TypeTextEvent, UploadFileEvent

### Layer 4: DOM (dom/ — 12 files)
Core: `DomService` in `dom/service.py`
- Extracts accessibility tree + DOM via CDP
- `EnhancedDOMTreeNode` — Rich node with computed styles, bounds, visibility
- `DOMTreeSerializer(dom/serializer/)` — Serializes DOM to LLM-friendly text
- `ClickableElementDetector(dom/serializer/clickable_elements.py)` — Identifies interactive elements

Key classes:
- `DomService` — Main DOM extraction service (configurable: cross_origin_iframes, paint_order_filtering, max_iframes=100, max_iframe_depth=5, viewport_threshold=1000)
- `EnhancedDOMTreeNode(views.py)` — DOM node with enhanced properties
- `EnhancedAXNode(views.py)` — Accessibility tree node
- `SerializedDOMState(views.py)` — Final serialized output
- `MatchLevel(views.py)` — Element matching: EXACT, STABLE, XPATH, AX_NAME, ATTRIBUTE

### DOM includes 50+ default attributes for automation: title, type, checked, id, name, role, value, placeholder, aria-label, pattern, min, max, accept, contenteditable, etc.

Dynamic class filtering: Removes transient state classes (focus, hover, active, etc.) for stable hashing.

## Known Website Patterns

### Canvas LMS (Instructure) — LMS platform
Canvas uses session-based authentication. Key patterns for file downloads:
- **Download files**: Navigate to the file page, find and click the download link (ref=ex21, "Download FE7066SR Assessment 2 Submission Form 70%.docx")
- **API access**: `/api/v1/courses/{id}/files/{file_id}` returns JSON with metadata including `url` (download link) and `size` (bytes)
- **curl limitation**: Canvas requires session cookies. `document.cookie` only exposes `_csrf_token` which is insufficient for curl downloads — session cookie is HttpOnly. Use browser_click instead.
- **Download URL pattern**: `https://{domain}/files/{id}/download?download_frd=1`
- **Page timeout**: Canvas pages can take 60s+ to load — set appropriate timeouts
- **Iframe preview**: Canvas renders previews in iframes which often show "403 Forbidden" — ignore the iframe, use download link
- **Page ref change**: After session expires, all element refs become invalid; must re-navigate and get new snapshot
- **Session expire**: Canvas sessions expire and require re-login; page navigations to authenticated routes redirect to /login/canvas
- **Session management**: Canvas may require re-login between long page loads — check for login redirect before proceeding

## Downloading Files from Authenticated Web Platforms

When you need to download files from sites requiring login (Canvas LMS, university portals, internal tools), direct `curl` downloads fail even with CSRF cookies because the session cookie is HttpOnly or uses a different auth mechanism.

### Pitfalls
- Canvas LMS: `document.cookie` only exposes `_csrf_token` — the actual session cookie is likely HttpOnly. curl with just `_csrf_token` returns login page HTML (~23KB) instead of the actual file.
- `fetch()` in browser console may fail due to CSP or CORS policies on some platforms.
- Don't retry curl with different cookies — if `_csrf_token` alone doesn't work, no JS-accessible cookie will.

### Recommended Approaches (in order of reliability)
1. **Hermes `browser_click` download link**: Navigate to the file page, click the download link. The CDP-based browser has the full session. Check `~/Downloads/` for the downloaded file.
2. **Canvas REST API**: `/api/v1/courses/{id}/files/{file_id}` returns metadata. Download URL: `/api/v1/files/{file_id}/download?download_frd=1`. Requires API token (Profile > Settings > New Access Token).
3. **Persistent browser context**: Use Playwright with `launch_persistent_context(user_data_dir)` to preserve login state across runs.
- **Page ref change**: After session expires, all element refs become invalid; must re-navigate and get new snapshot

Canvas auth pattern (if using DrissionPage):
```python
# Login then get cookies
page.get("https://stanfort.instructure.com/login/canvas")
page.ele("@id=email").input(email)
page.ele("@id=password").input(password)
page.ele("text=Log In").click()
# Now page has session cookies for authenticated requests
```

### Other Platform Patterns
- **GitHub**: Rate limiting requires token auth for heavy scraping
- **Google**: OAuth flow needed for Drive/Sheets API access
- **Notion**: API token in Authorization header
- **Linear**: GraphQL API with Bearer token auth

### Layer 5: Tools (tools/ — 8 files)
Core: `Controller` (aliased from `tools/service.py` → `controller/__init__.py`)
- Action registry system with domain-filtered actions
- 20+ built-in actions: click_element, type_text, navigate, scroll, search, extract, done, etc.
- Global action timeout: 180s default (configurable via BROWSER_USE_ACTION_TIMEOUT_S env var)
- Sensitive data detection for password/credential handling

Key classes:
- `Tools(service.py)` — Action execution engine with timeout guards
- `Registry(tools/registry/service.py)` — Action registration and domain filtering
- `RegisteredAction(views.py)` — Action model: name, description, function, param_model, terminates_sequence, domains
- `ActionModel(views.py)` — Base model for dynamically created action models
- `ActionRegistry(views.py)` — Registry with domain matching (glob patterns like *.google.com)
- `SpecialActionParameters(views.py)` — Injectable params: context, browser_session, page_url, cdp_client, page_extraction_llm, file_system

Action views (tools/views.py): ClickElementAction, TypeTextAction, NavigateAction, ScrollAction, SearchAction, ExtractAction, DoneAction, CloseTabAction, SwitchTabAction, GetDropdownOptionsAction, SendKeysAction, UploadFileAction, SaveAsPdfAction, ScreenshotAction, SearchPageAction, FindElementsAction, StructuredOutputAction, etc.

### Supporting Modules

**Skills System (skills/ — 4 files)**
- `SkillService(skills/service.py)` — Manages domain-specific skill files
- Skills are loaded as context for specific websites (e.g., Google, GitHub)
- Files in `skills/` directory

**MCP Integration (mcp/ — 5 files)**
- `MCPClient(mcp/client.py)` — MCP server client
- `MCPToolWrapper(mcp/controller.py)` — Wraps MCP tools as browser-use actions
- `BrowserUseServer(mcp/server.py)` — Exposes browser-use as MCP server

**Sandbox (sandbox/ — 3 files)**
- `@sandbox` decorator for cloud deployment
- Docker-based execution environment

**Filesystem (filesystem/ — 2 files)**
- `FileSystem(file_system.py)` — Agent file I/O (md, txt, json, csv, pdf)
- `CsvFile` — Auto-normalizes LLM-generated CSV (RFC 4180)
- Validates file extensions, rejects binary files

**Tokens (tokens/ — 6 files)**
- `TokenCost` — Tracks token usage and costs
- Supports multiple providers' pricing

**Telemetry (telemetry/ — 3 files)**
- `ProductTelemetry` — Anonymous usage tracking (opt-out via ANONYMIZED_TELEMETRY)
- Cloud events: CreateAgentOutputFileEvent, CreateAgentSessionEvent, CreateAgentStepEvent

**Config (config.py)**
- `CONFIG` — Global configuration (ANONYMIZED_TELEMETRY, etc.)

## CLI Entry Points
- `browser-use`, `browseruse`, `bu`, `browser` → `skill_cli.main:main`
- `browser-use task "..." --agent --model <model>` — Run a task
- `browser-use serve` — Start API server
- `browser-use record` — Record browser session
- `browser-use install` — Install browser dependencies

## Quick Start
```python
from browser_use import Agent
from browser_use.llm.models import get_llm_by_name

llm = get_llm_by_name('openai_gpt_4o')  # or 'google_gemini_2_5_pro'
agent = Agent(
    task="Go to github.com and find trending repos",
    llm=llm,
)
result = await agent.run(max_steps=30)
```

## Dependencies
pydantic, openai, anthropic, google-genai, mcp, playwright (via cdp-use), browser-use-sdk, httpx, cloudpickle, markdownify, bubus (event bus), cdp_use (CDP client)

## Key Design Patterns
1. **Event-driven**: EventBus for browser actions, decoupled handlers
2. **Protocol-based LLM**: BaseChatModel is a Protocol, not ABC — any class with `ainvoke()` works
3. **Domain-filtered actions**: Actions can be scoped to specific URL patterns
4. **History compaction**: Keeps first + recent messages, drops middle to save tokens
5. **Action timeout guard**: 180s global timeout prevents hung event handlers
6. **Sensitive data detection**: Auto-detects password fields, masks sensitive input
7. **Skill files**: Domain-specific knowledge injected per website

## Downloading Files from Authenticated Web Platforms

When you need to download files from sites requiring login (Canvas LMS, university portals, internal tools), direct `curl` downloads fail even with CSRF cookies because the session cookie is HttpOnly or uses a different auth mechanism.

### Pitfalls
- Canvas LMS: `document.cookie` only exposes `_csrf_token` — the actual session cookie is likely `canvas_session` (HttpOnly). curl with just `_csrf_token` returns login page HTML (23KB) instead of the actual file (~714KB).
- `fetch()` in browser console may fail due to CSP or CORS policies on platforms like Canvas.
- Don't retry curl with different cookies — if `_csrf_token` alone doesn't work, no JS-accessible cookie will.

### Recommended Approaches (in order of reliability)
1. **Hermes `browser_click` download link**: Navigate to the file page, click the download link. The CDP-based browser has the full session. Check `~/Downloads/` for the downloaded file.
2. **DrissionPage** (see `drission-page-automation` skill): Use `Session()` mode after logging in via `ChromiumPage` — session cookies transfer automatically.
3. **Playwright with persistent context**: `browser.launch_persistent_context(user_data_dir)` preserves login state across runs.
4. **Canvas REST API** (Canvas-specific): `/api/v1/courses/{id}/files/{file_id}` returns metadata JSON. Use `/api/v1/files/{file_id}/download?download_frd=1` with an API token (not browser session) for programmatic access.

### Canvas LMS Specifics
- API endpoint for file metadata: `GET /api/v1/courses/{course_id}/files/{file_id}` (returns JSON with `url`, `size`, `content-type`)
- Download URL pattern: `/files/{file_id}/download?download_frd=1`
- File preview uses iframe with Canvadocs — 403 on preview is normal, download link still works
- API token can be generated at: Profile > Settings > New Access Token

### See Also
- `references/canvas-lms-file-download.md` — Detailed Canvas LMS download patterns, API endpoints, and troubleshooting
