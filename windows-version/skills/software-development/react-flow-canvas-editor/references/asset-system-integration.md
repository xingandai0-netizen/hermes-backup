# Asset System Integration for AI APIs

## Problem
Many AI image/video APIs (like toapis.com) don't accept:
- base64 encoded images
- Direct URLs to external files

They require assets to be uploaded to their asset system first, then referenced by `asset_id`.

## TapNow's Approach
TapNow uses an asset management system:
1. Upload asset → get `asset_id`
2. Reference using `asset://asset_id` format
3. API internally resolves the asset

## Implementation Pattern

### 1. Create Asset Group
```python
async def create_asset_group(base_url: str, api_key: str) -> str:
    url = f"{base_url}/videos/doubao-seedance-2-0/private-avatar/groups"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json={}, headers=headers)
        data = resp.json()
        return data["data"]["group_id"]
```

### 2. Upload Asset
```python
async def upload_asset(base_url: str, api_key: str, group_id: str, source_url: str, asset_type: str) -> str:
    url = f"{base_url}/videos/doubao-seedance-2-0/private-avatar/assets"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "group_id": group_id,
        "source_url": source_url,  # URL that API can access
        "asset_type": asset_type   # "image" or "video"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload, headers=headers)
        data = resp.json()
        return data["data"]["asset_id"]
```

### 3. Wait for Asset Active
```python
async def wait_asset_active(base_url: str, api_key: str, asset_id: str, max_wait: int = 60):
    url = f"{base_url}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    for _ in range(max_wait):
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)
            data = resp.json()
            if data["data"]["status"] == "active":
                return True
        await asyncio.sleep(1)
    raise Exception("Asset activation timeout")
```

### 4. Use Asset in API Call
```python
# For image generation
payload = {
    "model": "gemini-3-pro-image-preview-official",
    "prompt": "描述...",
    "image_urls": [f"asset://{asset_id}"]  # Use asset:// format
}

# For video generation
payload = {
    "model": "seedance-2",
    "prompt": "描述...",
    "image_with_roles": [{"url": f"asset://{asset_id}", "role": "reference_image"}]
}
```

## Video Frame Extraction + Asset Upload
When using a video as reference for image generation:
1. Extract first frame using ffmpeg
2. Save to local temp file
3. Serve via local proxy endpoint
4. Upload proxy URL to asset system
5. Use `asset://asset_id` in API call

```python
async def extract_and_upload_frame(video_url: str, base_url: str, api_key: str) -> str:
    # 1. Extract frame
    frame_url = await extract_video_frame(video_url)  # Returns local proxy URL
    
    # 2. Create group and upload
    group_id = await create_asset_group(base_url, api_key)
    asset_id = await prepare_asset(base_url, api_key, group_id, frame_url, "image")
    
    # 3. Return asset:// format
    return f"asset://{asset_id}"
```

## Critical Rules
1. **NEVER use base64** - Most APIs reject it
2. **NEVER use direct URLs** - Must upload to asset system first
3. **ALWAYS use asset:// format** - `asset://asset_id`
4. **ALWAYS wait for activation** - Asset must be "active" before use
5. **Source URL must be accessible** - Use proxy endpoint for local files

## API Endpoints (toapis.com)
- Create group: `POST /videos/doubao-seedance-2-0/private-avatar/groups`
- Upload asset: `POST /videos/doubao-seedance-2-0/private-avatar/assets`
- Check status: `GET /videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}`
