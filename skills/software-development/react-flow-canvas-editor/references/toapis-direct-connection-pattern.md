# ⚠️ ABANDONED - toapis.com Direct Connection Pattern

## Status: DEAD END (2026-06-27)

**阿戴明确声明：这是废案，不要使用。**

The "frontend direct connection to toapis.com" approach was tried and abandoned.
All API calls MUST go through the backend proxy. Do NOT attempt this approach again.

## Why It Failed

The direct connection approach did not solve the LAN access problem and introduced
unnecessary complexity. The correct architecture is:

```
Browser → Backend (localhost:8000) → toapis.com
```

Backend handles ALL API calls to toapis.com, including:
- Image generation
- Video generation
- Task polling
- Asset upload

## What Actually Works

- Frontend uses `getApiBase()` to get dynamic backend URL
- Backend proxies all toapis.com calls
- LAN computers access via `http://<host-ip>:3000` (frontend) and `http://<host-ip>:8000` (backend)
