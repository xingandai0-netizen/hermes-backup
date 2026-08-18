# Antoken v0.1 - Complete Working Patterns

## Session Date: 2026-06-07

### What Worked
1. **Click-to-add nodes** — onClick handler on sidebar node cards, staggered positions
2. **Drag-to-connect** — mousedown/mousemove/mouseup on Handle elements via browser_console
3. **Real API calls** — Frontend passes api_url + api_key in body, backend forwards to user's proxy
4. **Model name aliasing** — Try gpt-image-2, gpt-image2, dall-e-3 automatically
5. **Multi-endpoint retry** — Try /images/generations and /v1/images/generations
6. **Chinese UI** — All text in Chinese, keep brand names in English
7. **Compact nodes** — 160px width, 8px handles, narrow sidebar (w-48)
8. **Progress display** — Progress bar + percentage in button text
9. **Preview system** — Image thumbnails, video covers with play button, fullscreen modal
10. **localStorage conditional loading** — initializeWorkflow() pattern, not auto-load

### What Failed
1. **browserbase for localhost** — Always loses state, use local Safari instead
2. **Mock data** — User furious when generation was simulated
3. **Exact model name match** — Proxy uses different names, need aliasing
4. **Authorization header for credentials** — Pass in request body instead
5. **Large nodes** — User rejected 200px and 240px, final: 160px
6. **Wide sidebar** — User rejected w-60, final: w-48
7. **Emoji in UI** — taste-skill forbids, use letter abbreviations
8. **Auto-load localStorage** — User confused about "ghost nodes"

### Key Code Patterns

#### Node Component (Inline Editing)
```tsx
// textarea + generate button directly on node
// Progress bar during generation
// Preview (thumbnail + fullscreen) after generation
// Error display with red border
```

#### Backend API (Proxy Forwarding)
```python
# Use request.api_url and request.api_key (NOT env vars)
# Try multiple model aliases
# Try multiple endpoint formats
# Log every attempt
```

#### Store (Conditional Init)
```typescript
// Don't auto-load localStorage
// Use initializeWorkflow() called from useEffect
// Clear button removes localStorage
```
