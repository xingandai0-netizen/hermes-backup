# LAN URL Upload to toapis.com — Open Issue (2026-06-27)

## Status: UNRESOLVED

## Problem
When a LAN computer (not the host machine) uploads a file and then triggers video generation, the backend fails with:
```
素材上传失败: 上传失败，{"message":"invalid request body","success":false}
```

## Expected Flow
1. LAN computer uploads file to `http://192.168.0.102:8000/api/upload`
2. Backend saves file, returns `{ path: "/api/upload/file/{uuid}.mp4" }`
3. Frontend constructs `assetUrl = http://192.168.0.102:8000/api/upload/file/{uuid}.mp4`
4. Video generation sends this URL to backend
5. Backend's `prepare_asset()` detects LAN URL (starts with `http://192.168.`)
6. Backend downloads from itself → converts to data URL → binary upload to toapis.com

## What We Know
- Backend can download from itself (`curl http://192.168.0.102:8000/api/upload/file/xxx` returns 200)
- `assetUpload.ts` was fixed to correctly return `getApiBase() + data.path` (was returning `undefined`)
- Local machine (192.168.0.102) works fine
- LAN computer fails with "invalid request body" from toapis.com

## Possible Causes
1. **Download timing issue** — Backend might be busy with the generation request and can't handle simultaneous download
2. **File not found** — Upload might have failed silently, file doesn't exist when backend tries to download
3. **Data URL too large** — Large video files create huge base64 strings that toapis.com rejects
4. **Multipart upload format** — The binary upload to toapis.com might have wrong format

## Debug Steps (for next session)
1. Check backend terminal for `[Upload]` log messages
2. Look for: `[Upload] 检测到本地URL，下载中:` or `[Upload] 下载本地文件失败:`
3. If download fails, check if file exists at `/tmp/antoken_uploads/`
4. Test manually: `curl -s http://192.168.0.102:8000/api/upload/file/{uuid}` from the host machine

## Key Code Location
- `backend/app/api/generate.py` line 209: `prepare_asset()` function
- `backend/app/api/generate.py` line 119: `upload_asset()` function
- Error at line 410: `raise HTTPException(500, detail=f"素材上传失败: {str(e)}")`
