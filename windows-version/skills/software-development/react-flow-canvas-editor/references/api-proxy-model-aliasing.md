# API Proxy Model Name Aliasing

## Problem
When using third-party API proxies (antokex.com, new-api, one-api), model names may differ from the standard OpenAI names. A request for `gpt-image-2` may fail with "no available channel for model_name" because the proxy uses a different name.

## Solution: Multi-Alias Retry Pattern

### Frontend: Pass credentials in request body
```typescript
// ❌ WRONG: Authorization header
headers: { "Authorization": `Bearer ${imageApi.apiKey}` }

// ✅ RIGHT: Credentials in body
headers: { "Content-Type": "application/json" }
body: JSON.stringify({
  prompt, model: imageApi.modelName,
  api_url: imageApi.apiUrl,
  api_key: imageApi.apiKey,  // ← pass in body
})
```

### Backend: Try multiple model names and endpoints

```python
MODEL_ALIASES = {
    "gpt-image-2": ["gpt-image-2", "gpt-image2", "dall-e-3", "dalle-3"],
    "seedance-2": ["seedance-2", "seedance-2.0", "seedance-2.0-lite", "seedance-v2"],
    "kling": ["kling", "kling-v1", "kling-1.0", "kling-ai"],
    "runway-gen-3": ["runway-gen-3", "gen-3", "gen3", "runway-gen3"],
}

def get_model_names(model: str) -> list:
    if model in MODEL_ALIASES:
        return MODEL_ALIASES[model]
    for key, aliases in MODEL_ALIASES.items():
        if model in aliases:
            return aliases
    return [model]
```

### Multi-endpoint retry
```python
endpoints = [
    f"{api_base}/images/generations",   # OpenAI standard
    f"{api_base}/v1/images/generations", # with v1 prefix
]

for endpoint in endpoints:
    for model_name in model_names:
        try:
            response = await client.post(endpoint, json=payload, headers=headers)
            if response.status_code == 200:
                return parse_response(response.json())
        except:
            continue
```

### Response format parsing
```python
# OpenAI format: {"data": [{"url": "..."}]}
# Custom format: {"images": ["url1", "url2"]}
# Single image: {"url": "..."}
# Async task: {"task_id": "...", "status": "pending"}
```

## Key Rules
1. NEVER use env vars for API keys — always use request-provided credentials
2. Try multiple model aliases automatically
3. Try multiple endpoint formats automatically
4. Log every attempt for debugging
5. Return first success, not all failures
