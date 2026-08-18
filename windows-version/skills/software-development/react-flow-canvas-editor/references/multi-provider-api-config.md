# Multi-Provider API Configuration Pattern

## Problem
E-commerce AI workflow platforms call MULTIPLE AI providers (e.g., GPT-Image-2 for images, Seedance 2 for video). A single "API Key" field doesn't work — different providers have different URLs, keys, and model names.

## Solution: Tab-Based Settings Modal

### Store Design (settingsStore.ts)
```typescript
export interface ApiProviderConfig {
  apiUrl: string;
  apiKey: string;
  modelName: string;
}

export interface SettingsState {
  imageApi: ApiProviderConfig;
  videoApi: ApiProviderConfig;
  temperature: number;
  maxTokens: number;
  // Per-provider actions
  setImageApi: (config: Partial<ApiProviderConfig>) => void;
  setVideoApi: (config: Partial<ApiProviderConfig>) => void;
  getImageHeaders: () => Record<string, string>;
  getVideoHeaders: () => Record<string, string>;
  testImageConnection: () => Promise<{ success: boolean; message: string }>;
  testVideoConnection: () => Promise<{ success: boolean; message: string }>;
}

const DEFAULT_IMAGE_API = { apiUrl: 'https://api.openai.com/v1', apiKey: '', modelName: 'gpt-image-2' };
const DEFAULT_VIDEO_API = { apiUrl: 'https://api.siliconflow.cn/v1', apiKey: '', modelName: 'seedance-2' };
```

### SettingsModal with Tabs
- Two tabs: "Image Generation Model" / "Video Generation Model"
- Each tab has independent: URL, Key, Model dropdown, Test button
- Image models: GPT-Image-2, DALL-E 3, Stable Diffusion 3, FLUX 1.1 Pro, Custom
- Video models: Seedance 2, Kling, Runway Gen-3, Pika, Custom

### Migration from Single API
```typescript
// In loadFromStorage(), handle old format:
if (parsed.apiUrl && !parsed.imageApi) {
  return {
    ...DEFAULT_SETTINGS,
    imageApi: { apiUrl: parsed.apiUrl, apiKey: parsed.apiKey, modelName: parsed.modelName }
  };
}
```

### Node Components Read Correct Provider
```typescript
// ImageGenNode.tsx
const { imageApi } = useSettingsStore();
// VideoGenNode.tsx
const { videoApi } = useSettingsStore();
```

### Top Bar Status
```typescript
const { imageApi, videoApi } = useSettingsStore();
const anyConfigured = imageApi.apiKey || videoApi.apiKey;
// Show: green "API Configured" / yellow "No API Key" / orange "Partially Configured"
```
