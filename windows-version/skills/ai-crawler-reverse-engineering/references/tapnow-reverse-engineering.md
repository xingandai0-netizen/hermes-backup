# TapNow.ai 逆向工程完整案例

## 目标信息
- **URL**: https://www.tapnow.ai (主页) / https://app.tapnow.ai (应用)
- **产品**: AI创意画布平台（类似Antoken）
- **技术栈**: Next.js (App Router) + Vite + React

## 逆向结果

### 域名架构
| 域名 | 用途 |
|------|------|
| `app.tapnow.ai` | 主应用（SPA） |
| `fe-assets.tapnow.media` | 静态资源CDN（JS/CSS/图片） |
| `files.tapnow.art` | 用户上传文件服务 |

### 主JS文件
CDN路径模式: `https://fe-assets.tapnow.media/{hash}/assets/{name}.js`

关键文件:
- `index-kqMVjXuo.js` - 主应用入口（479KB，包含所有业务逻辑）
- `vendor-libs-DmQnlliI.js` - 核心库
- `vendor-packages-ClBOHPXJ.js` - 第三方包
- `vendor-pkg-canvas-BWJDHYHZ.js` - 画布功能

### API端点
```
认证:
POST /api/auth/email/send-code
POST /api/auth/email/verify-code
POST /api/auth/email/login
POST /api/auth/google/login
GET  /api/user/info

图像生成:
POST /api/image/generate
GET  /api/image/status/{task_id}
GET  /api/image/result/{task_id}

视频生成:
POST /api/video/generate
GET  /api/video/status/{task_id}
GET  /api/video/result/{task_id}

对话:
POST /api/conversation/create
POST /api/conversation/message
GET  /api/conversation/{id}/history
POST /api/conversation/storage/uploads/{id}

社区:
GET /api/community/works
GET /api/community/works/{id}

计费:
GET /api/billing/plans
GET /api/billing/wallet/balance
GET /api/billing/transactions

团队:
GET /api/team/info
GET /api/team/members

文件:
POST /api/storage/upload
```

### 支持的AI模型
**图像**: Flux, Midjourney, GPT Image, Hailuo, Jimeng, Vidu, Pixverse, Grok, Gemini
**视频**: Veo, Kling, Luma, Sora, Hailuo, Jimeng, Vidu

### 定价
- BASIC: $15/月 (年付$90)
- PRO: $60/月 (年付$360) - 最受欢迎
- ULTIMATE: $180/月 (年付$2160)

### 第三方集成
- TikTok像素 (analytics.tiktok.com)
- Facebook像素 (connect.facebook.net)
- Google Tag Manager (googletagmanager.com)
- Google Ads (googleads.g.doubleclick.net)
- Sentry错误监控
- Mixpanel数据分析

### 错误码系统
完整的错误码定义在JS中，格式: `{code: "message"}`
关键错误码:
- 1001: 输入有误
- 1101: 未登录
- 1102: 登录失效
- 1402: Tapies已用完
- 100108: 短信发送过于频繁
- 100216: 已发送验证邮件，60秒后可再次请求

## 逆向过程中的坑

1. **Next.js App Router没有__NEXT_DATA__**: 用`document.getElementById('__NEXT_DATA__')`找不到，需要直接分析JS文件
2. **JS文件巨大（479KB）**: 不能直接在浏览器console中分析，需要下载到本地用grep搜索
3. **拦截器重复声明**: 在console中多次声明`const originalFetch`会报错，需要先检查是否已存在
4. **登录页面跳转**: 点击"Get started"会跳转到`app.tapnow.ai/auth-login`，需要在这个页面分析登录API
5. **CDN域名与主域名不同**: 静态资源在`fe-assets.tapnow.media`，不在`app.tapnow.ai`

## 生成的代码
- `/Users/macpro/ai-crawler-reverse/output/tapnow_crawler.py` - 完整爬虫
- `/Users/macpro/ai-crawler-reverse/output/tapnow_environment.py` - 环境注入
