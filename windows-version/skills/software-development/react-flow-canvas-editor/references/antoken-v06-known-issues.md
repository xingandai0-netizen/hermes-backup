# Antoken v0.6 已知问题归档

## 1. 局域网访问：本地文件上传到toapis失败

**场景**: 从LAN电脑(192.168.x.x)访问antoken，拖入本地文件后生成视频/图片报错。

**根因**: 
- 本地文件存到后端temp目录 → 返回LAN URL (http://192.168.0.102:8000/api/upload/file/xxx)
- toapis.com的asset API要求source_url是公开可访问的URL
- toapis.com服务端无法访问LAN URL

**尝试过的方案（都失败）**:
1. Data URL转换: data:image/png;base64,... → toapis拒绝: "http must be a valid http or https URL"
2. Multipart二进制上传 → asset端点不接受: "invalid request body"
3. 后端代理所有请求 → LAN电脑无法访问localhost后端

**最终解决方案**: 
- 前端直接调toapis.com（CORS已支持allow-origin: *）
- API调用（创建任务、轮询状态）直连toapis
- 后端只保留文件上传和媒体代理

## 2. toapis.com CORS支持

**发现**: toapis.com返回完整的CORS头:
- access-control-allow-origin: *
- access-control-allow-methods: GET,POST,PUT,DELETE,OPTIONS
- access-control-allow-headers: *

**意义**: 浏览器可以直接调用toapis.com API，不需要后端代理。

## 3. VPN导致files.toapis.com超时

**场景**: 开着VPN时，视频预览加载卡住（spinner一直转）。

**根因**: VPN导致files.toapis.com CDN连接超时。

**解决**: 关掉VPN后立即恢复（HTTP 200, 3.4MB, 2.2秒）。

## 4. CORS只允许localhost

**场景**: LAN电脑调用后端API报 "Failed to fetch"。

**根因**: 后端CORS配置只允许 ["http://localhost:3000", "http://localhost:3001"]。

**解决**: 改为 ["*"] 允许所有来源。
