# toapis.com Asset API "invalid request body" Debug Guide

## Error Signature
```json
{"message": "invalid request body", "success": false}
```

## When This Happens
Returned by `POST /v1/videos/doubao-seedance-2-0/private-avatar/assets` when:
1. `source_url` is a private LAN IP (192.168.x.x, 10.x.x.x, 172.16-31.x.x) — toapis.com can't fetch it
2. `source_url` is a data URL (`data:image/png;base64,...`) — not accepted in JSON body
3. Request body JSON is malformed or missing required fields

## Common Scenario: LAN Access
When Antoken runs on LAN and user uploads local files:
1. Frontend uploads file to backend → returns `http://192.168.x.x:8000/api/upload/file/xxx.mp4`
2. Frontend sends this URL to `/api/generate/video`
3. Backend's `prepare_asset` should detect LAN URL → download from self → convert to data URL → binary upload
4. **If download fails** (timeout, backend not listening on LAN IP): falls back to raw LAN URL → toapis rejects

## Backend Code Path
```python
# generate.py - prepare_asset()
if source_url.startswith("http://192.168."):
    resp = await client.get(source_url)  # Download from self
    if resp.status_code == 200:
        final_url = f"data:{mime};base64,{b64}"  # Convert to data URL
    # else: falls through with original LAN URL

# upload_asset()
if source_url.startswith("data:"):
    # Binary multipart upload (correct path for LAN files)
    files = {"file": (f"asset{ext}", file_content, mime)}
    resp = await client.post(url, files=files, data={"group_id": ..., "asset_type": ...})
else:
    # JSON upload with source_url (fails if URL is private)
    payload = {"group_id": ..., "source_url": source_url, "asset_type": ...}
    resp = await client.post(url, json=payload)
```

## Debugging Steps
1. Check backend terminal for `[Upload] 检测到本地URL，下载中:` — confirms LAN detection
2. Look for `[Upload] 下载本地文件失败:` — confirms download failure (root cause)
3. Look for `[Upload] 二进制上传 (N bytes)` — confirms data URL path worked
4. If none of above: URL pattern not matching LAN detection (check `prepare_asset` conditions)

## Fix Priority
1. Ensure backend is listening on `0.0.0.0` (not just `127.0.0.1`)
2. Ensure backend can access itself at its LAN IP
3. If download still fails: increase timeout (currently 30s for large video files)
