# toapis.com API 限制（2026-06-27 实测确认）

## 核心约束（未解决）

**toapis.com 只接受公开可访问的 HTTP/HTTPS URL。所有其他格式均被拒绝。**

### 已验证的失败路径

| 尝试方式 | 结果 | 错误信息 |
|---------|------|---------|
| LAN URL (`http://192.168.x.x`) | ❌ | `invalid request body` |
| Data URL (`data:image/png;base64,...`) | ❌ | `invalid request body` |
| Base64 in `image_urls` 字段 | ❌ | `base64 image is not allowed` |
| Multipart binary upload to Asset API | ❌ | `invalid request body` |

### 什么能用

- AI 生成的素材：结果存在 toapis.com CDN（`https://files.toapis.com/...`），公开可访问 ✅
- 在线图片/视频 URL：公开可访问 ✅

## 受影响的功能

1. **拖拽/导入文件到画布** → 存储为 LAN URL → 无法作为上游素材生成
2. **画布右键导入** → 同上
3. **侧边栏导入** → 同上

## 解决方案（待实现）

需要将本地文件上传到公开 CDN 获取公开 URL：
- 选项1：临时文件托管（file.io, transfer.sh）— 免费但不稳定
- 选项2：Cloudflare R2 / S3 — 稳定但需配置
- 选项3：ngrok 隧道 — 把后端临时暴露为公网地址

## API 端点

```
视频生成: POST {base}/video/generations 或 /videos/generations
图片生成: POST {base}/images/generations
视频轮询: GET {base}/video/generations/{task_id}
图片轮询: GET {base}/images/generations/{task_id}

Asset Group: POST {base}/videos/doubao-seedance-2-0/private-avatar/groups
Asset Upload: POST {base}/videos/doubao-seedance-2-0/private-avatar/assets
Asset Query: GET {base}/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}
```

## 常见错误

- `{"message":"invalid request body","success":false}` → URL 不是公开可访问的
- `{'code': 'quota_not_enough'}` → 账户额度用完，需充值
- `base64 image is not allowed` → 传了 data URL，不支持
