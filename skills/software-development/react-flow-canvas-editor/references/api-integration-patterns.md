# API Integration Patterns for Antoken

## Multi-Provider Configuration

When the project calls MULTIPLE AI providers (e.g., GPT-Image-2 for images, Seedance 2 for video), use separate API configs per provider type.

### settingsStore Pattern

```typescript
export interface ApiProviderConfig {
  apiUrl: string;
  apiKey: string;
  modelName: string;
}

export interface SettingsState {
  imageApi: ApiProviderConfig;  // GPT-Image-2, DALL-E, FLUX
  videoApi: ApiProviderConfig;  // Seedance 2, Kling, Runway
  // ...
}
```

### Frontend Request Pattern

**CRITICAL**: Pass api_url + api_key in request body. Do NOT use Authorization header for forwarding — the backend needs to extract and forward credentials to the actual AI API.

```typescript
// ❌ WRONG: Authorization header
headers: { "Authorization": `Bearer ${apiKey}` }

// ✅ RIGHT: Body parameters
body: JSON.stringify({
  prompt, model, api_url, api_key  // backend reads these
})
```

### Backend Forwarding Pattern

```python
# ❌ WRONG: Using env vars
headers["Authorization"] = f"Bearer {os.getenv('API_KEY')}"

# ✅ RIGHT: Using request body
headers["Authorization"] = f"Bearer {request.api_key}"
api_url = f"{request.api_url.rstrip('/')}/images/generations"
```

## Node Component Template

Every generation node follows this pattern:

```tsx
export default function XxxNode(props: NodeProps) {
  const d = props.data as unknown as NodeData;
  const cfg = d.config as { prompt?: string; ... };
  const { xxxApi } = useSettingsStore();
  const { updateNodeData } = useWorkflowStore();
  const [prompt, setPrompt] = useState(cfg.prompt ?? "");
  const [progress, setProgress] = useState(0);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isRunning = d.status === "running";
  const isSuccess = d.status === "success";

  const handleGenerate = async () => {
    if (isRunning) return;
    if (!prompt.trim()) { setError("请输入描述"); return; }
    if (!xxxApi.apiKey) { setError("请先配置API Key"); return; }

    setError(null);
    updateNodeData(props.id, { status: "running", progress: 0 });

    try {
      const response = await fetch("http://localhost:8000/api/generate/xxx", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt, model: xxxApi.modelName,
          api_url: xxxApi.apiUrl, api_key: xxxApi.apiKey,
        }),
      });
      // ... handle response, update preview, set success
    } catch (err) {
      setError(err.message);
      updateNodeData(props.id, { status: "error", error: err.message });
    }
  };

  return (
    <BaseNode {...props}>
      {/* Input field */}
      {/* Error display */}
      {/* Generate button with state */}
      {/* Progress bar (when running) */}
      {/* Preview (when success) */}
      {/* Config badges */}
    </BaseNode>
  );
}
```

## Common Pitfalls

1. **Mock data**: Never use placeholder/mock data for generation. User will be furious.
2. **Authorization header**: Don't put API key in Authorization header for frontend→backend calls. Pass in body.
3. **Environment variables**: Backend should NOT use os.getenv() for user-configured API keys. Use request body.
4. **Missing validation**: Always check if apiKey exists before calling API. Show clear error if not configured.
5. **Timeout**: Image generation can take 30-120s. Video can take 60-300s. Set appropriate httpx timeouts.
