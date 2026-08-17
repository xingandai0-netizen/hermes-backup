# Error Source Identification for Antoken

## How to Identify Which System Returned an Error

When debugging API integration issues, the error format tells you exactly which system generated it:

| Error Format | Source | Where to Look |
|---|---|---|
| `{"message":"...", "success":false}` | **toapis.com** external API | The toapis.com response; check request format, URL validity, auth |
| `{"detail":"..."}` | **Local FastAPI backend** | `generate.py` or `upload.py`; check the HTTPException at that line |
| `{"error": {"message": "..."}}` | **toapis.com** (OpenAI-style error) | Usually model/endpoint errors |
| `TypeError: Failed to fetch` | **Browser** can't reach backend | CORS, backend down, wrong URL |
| `net::ERR_CONNECTION_REFUSED` | **Browser** can't connect | Backend not running or wrong port |
| `素材上传失败: {str(e)}` | **Local backend wrapping** toapis error | The inner exception is from toapis.com |

## Tracing the Full Chain

```
Frontend (browser)
  → POST /api/generate/video (local backend)
    → prepare_asset() downloads file
      → upload_asset() sends to toapis.com
        → toapis.com Asset API responds
      ← Exception if toapis returns error
    ← Exception if download/upload fails
  ← HTTPException(500, "素材上传失败: ...")
← Frontend displays error
```

Each `←` is a potential failure point. The error message format at each level is different.

## Key Insight: Silent Fallback in prepare_asset

The `prepare_asset` function (generate.py:209-240) has a dangerous pattern:

```python
if source_url.startswith("http://192.168."):
    try:
        resp = await client.get(source_url)  # Download from self
        if resp.status_code == 200:
            final_url = f"data:{mime};base64,{b64}"  # Convert to data URL
    except Exception as e:
        logger.warning(f"下载失败: {e}")  # Just logs warning!
# Falls through with original LAN URL if download fails
```

If the self-download fails, `final_url` stays as the LAN URL, which gets passed to toapis.com. toapis.com can't access private IPs → returns "invalid request body".

This silent fallback makes the error confusing because:
1. The error looks like a "request format" issue (invalid body)
2. But the real cause is a "URL accessibility" issue (toapis can't fetch LAN URL)
