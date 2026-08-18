# Antoken Model Integration Guide

## Core Principle
**Research first, implement later. Never guess model capabilities.**

## Research Flow

### Step 1: Check API docs
- https://toapis.com/en/market — Model marketplace
- https://docs.toapis.com — API documentation

### Step 2: Call model discovery API
```bash
curl -s "http://localhost:8000/api/generate/models?api_url=https://toapis.com/v1&api_key=YOUR_KEY" | jq '.'
```

### Step 3: Test API call
```bash
# Image generation test
curl -X POST "https://toapis.com/v1/images/generations" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_NAME", "prompt": "test", "aspect_ratio": "1:1"}'
```

## Verified Model Capability Matrix

### Image Models
| Model | Resolution | Ratios |
|-------|-----------|--------|
| gemini-3-pro-image-preview-official | 1K/2K/4K | 1:1, 16:9, 9:16, 4:3, 3:4, 21:9 |
| nano_banana_2 | 0.5K/1K/2K/4K | Same as above |

### Video Models
| Model | Resolution | Duration | Special params |
|-------|-----------|----------|----------------|
| seedance-2 | 480p-4k | 4-15s | image_with_roles |
| seedance-2-fast | 720p | 4-15s | image_with_roles |
| seedance-2-mini | 720p | 4-15s | reference_image only |

## UI Adaptation Rules

### Dynamic resolution options
```typescript
const MODEL_RESOLUTIONS: Record<string, string[]> = {
  "gemini-3-pro-image-preview-official": ["1K", "2K", "4K"],
  "nano_banana_2": ["0.5K", "1K", "2K", "4K"],
};
```

### Auto-adjust on model switch
```typescript
useEffect(() => {
  const supported = getSupportedResolutions(model);
  if (!supported.includes(resolution)) setResolution(supported[0]);
}, [model]);
```

## Common Pitfalls
- ❌ Assume all image models support 4K → ✅ Check docs first
- ❌ Hardcode model list → ✅ Dynamically fetch from API
- Image models: `metadata.resolution` (1K/2K/4K)
- Video models: `resolution` (480p/720p/1080p/4k) — format differs!
