# Model Selector Dropdown on Nodes

## Problem
User wants to select which model to use DIRECTLY on the node, not just in Settings.
"节点上要有模型选择下拉框"

## Pattern: Model Dropdown on AI Nodes

Each AI generation node (ImageGen, VideoGen, Img2Video) should have a model selector dropdown that:
1. Auto-discovers available models from the API's `/v1/models` endpoint
2. Filters by `supported_endpoint_types` (image-generation vs video-generation)
3. Falls back to hardcoded verified models if discovery fails
4. Shows current selection with a small indicator

### Frontend: Model Discovery Hook

```typescript
// hooks/useModelDiscovery.ts
import { useState, useEffect } from 'react';

interface DiscoveredModel {
  id: string;
  name: string;
  endpoint_types: string[];
}

export function useModelDiscovery(apiUrl: string, apiKey: string, filterType: 'image' | 'video') {
  const [models, setModels] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!apiUrl || !apiKey) return;
    setLoading(true);
    fetch(`${apiUrl}/models`, {
      headers: { 'Authorization': `Bearer ${apiKey}` },
    })
      .then(r => r.json())
      .then(data => {
        const all: DiscoveredModel[] = data.data || [];
        const filtered = all.filter(m => {
          const types = m.supported_endpoint_types || m.endpoint_types || [];
          if (filterType === 'image') return types.some(t => t.includes('image'));
          if (filterType === 'video') return types.some(t => t.includes('video'));
          return false;
        });
        setModels(filtered.map(m => m.id));
      })
      .catch(() => {
        // Fallback to verified models
        if (filterType === 'image') setModels(['gemini-3-pro-image-preview-official', 'nano_banana_2']);
        if (filterType === 'video') setModels(['seedance-2']);
      })
      .finally(() => setLoading(false));
  }, [apiUrl, apiKey, filterType]);

  return { models, loading };
}
```

### Node: Model Selector in Header

```tsx
// nodes/ImageGenNode.tsx — model dropdown in node
function ImageGenNode(props: NodeProps) {
  const { imageApi } = useSettingsStore();
  const { updateNodeData } = useWorkflowStore();
  const d = props.data as unknown as NodeData;
  const cfg = d.config as { model?: string; prompt?: string };

  const { models, loading: modelsLoading } = useModelDiscovery(
    imageApi.apiUrl, imageApi.apiKey, 'image'
  );

  const currentModel = cfg.model || imageApi.modelName;

  const handleModelChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateNodeData(props.id, { config: { ...cfg, model: e.target.value } });
  };

  return (
    <BaseNode {...props}>
      {/* Model selector */}
      <div style={{ padding: '0 8px 4px 10px' }}>
        <select value={currentModel} onChange={handleModelChange} disabled={modelsLoading}
          style={{
            width: '100%', fontSize: 10, color: '#8a8f98',
            background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: 4, padding: '2px 4px', outline: 'none',
          }}>
          {models.map(m => <option key={m} value={m}>{m}</option>)}
          {!models.length && <option value={currentModel}>{currentModel}</option>}
        </select>
      </div>
      {/* Rest of node content... */}
    </BaseNode>
  );
}
```

## Key Rules

1. **Don't duplicate model config** — node-level model overrides Settings default. If node has `config.model`, use it; otherwise fall back to Settings store model.
2. **Don't guess model names** — always discover from API, with verified fallbacks.
3. **Filter by endpoint_types, NOT by name** — `gpt-4o-image` has "image" in name but empty `endpoint_types`, so it can't generate images.
4. **Compact dropdown** — font 10px, no padding waste, fits inside 220px node width.
5. **Disable while loading** — show loading state while fetching models.
