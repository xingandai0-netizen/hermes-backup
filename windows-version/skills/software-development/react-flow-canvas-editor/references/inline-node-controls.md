# Inline Node Controls Pattern

## Problem
Users need to configure node parameters (model selection, prompt input) directly on the canvas node, not just in a separate property panel.

## Solution: Inline Controls in Node Components

### Model Selection Dropdown
```tsx
// Inside a node component (e.g., ImageGenNode.tsx)
const [selectedModel, setSelectedModel] = useState(cfg.model ?? defaultModel);
const [availableModels, setAvailableModels] = useState<string[]>([]);

// Auto-discover models from API
useEffect(() => {
  if (apiUrl && apiKey && availableModels.length === 0) {
    fetch(`/api/generate/models/discover?api_url=...&api_key=...`)
      .then(r => r.json())
      .then(data => {
        if (data.image_models?.length > 0) {
          setAvailableModels(data.image_models);
          if (!data.image_models.includes(selectedModel)) {
            setSelectedModel(data.recommended.image);
          }
        }
      })
      .catch(() => {});
  }
}, [apiUrl, apiKey]);

// Render dropdown inside node
<select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}
  style={{
    width: "100%", marginBottom: 4, fontSize: 8, color: "#d0d6e0",
    background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: 3, padding: "3px 4px", outline: "none",
  }}>
  {availableModels.length > 0 
    ? availableModels.map(m => <option key={m} value={m}>{m}</option>)
    : <><option value="default-model">default-model</option></>
  }
</select>
```

### Prompt Textarea
```tsx
<textarea value={prompt} onChange={(e) => setPrompt(e.target.value)}
  placeholder="输入描述..." disabled={loading}
  style={{
    width: "100%", height: 36, fontSize: 9, color: "#d0d6e0",
    background: "rgba(255,255,255,0.03)",
    border: `1px solid ${error ? "#ef4444" : "rgba(255,255,255,0.08)"}`,
    borderRadius: 4, padding: "4px 6px", resize: "none", outline: "none",
  }} />
```

### Progress Bar with Real Progress
```tsx
// Use real progress from API polling, not simulated
const [progress, setProgress] = useState(0);

// In poll callback:
setProgress(data.progress || 0);

// Render
{loading && (
  <div style={{ marginTop: 3, height: 3, background: "rgba(255,255,255,0.05)", borderRadius: 2, overflow: "hidden" }}>
    <div style={{ 
      width: `${progress}%`, height: "100%", 
      background: "linear-gradient(90deg, #5e6ad2, #7170ff)", 
      borderRadius: 2, transition: "width 0.5s ease" 
    }} />
  </div>
)}
```

### Error Display with word-break
```tsx
{error && (
  <div style={{ marginTop: 3, padding: "3px 5px", background: "rgba(239,68,68,0.1)", borderRadius: 3, border: "1px solid rgba(239,68,68,0.2)" }}>
    <p style={{ fontSize: 7, color: "#ef4444", wordBreak: "break-all" }}>{error}</p>
  </div>
)}
```

## Async Task Polling Pattern

**CRITICAL: Never use backend-blocking polling!** The backend must return immediately with task_id, and the frontend polls.

```typescript
const pollRef = useRef<NodeJS.Timeout | null>(null);

const pollTask = (taskId: string) => {
  pollRef.current = setInterval(async () => {
    const resp = await fetch(`/api/generate/task/${taskType}/${taskId}?api_url=...&api_key=...`);
    const data = await resp.json();
    setProgress(data.progress || 0);
    
    if (data.status === "completed" && data.url) {
      clearInterval(pollRef.current!);
      // Show result
    } else if (data.status === "failed") {
      clearInterval(pollRef.current!);
      // Show error
    }
  }, 5000); // Poll every 5 seconds
};

// Cleanup on unmount
useEffect(() => {
  return () => { if (pollRef.current) clearInterval(pollRef.current); };
}, []);
```

## Pitfalls

1. **Don't simulate progress** — Use real progress from API polling
2. **Don't block backend** — Return task_id immediately, let frontend poll
3. **Clean up intervals** — Always clear polling on component unmount
4. **Handle model discovery failure** — Fallback to default models if discovery fails
5. **word-break: break-all** on error messages — API errors can be long strings without spaces
