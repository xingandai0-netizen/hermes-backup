# Antokex Deployment 归档索引

## 服务器信息
- IP: 47.99.55.244 (阿里云)
- SSH: root@47.99.55.244
- 域名: antokex.com (Cloudflare DNS)
- Nginx监听: 8088
- Sub2API: Docker容器 localhost:8080

## 登录凭证
- 管理员: 18957167833@163.com / Dxa19990210

## 架构
```
用户浏览器 → Cloudflare → 阿里云47.99.55.244:443/80 → Nginx:8088
  /        → /var/www/antokex/index.html (静态)
  /login   → /var/www/antokex/login.html (静态)
  /register→ /var/www/antokex/register.html (静态)
  /admin   → /var/www/antokex/admin.html (自定义管理后台)
  /dashboard → 302重定向到 /admin
  /assets/ → /var/www/antokex/assets/ (静态文件)
  /api/*   → Sub2API Docker localhost:8080
  /*       → Sub2API Docker localhost:8080 (Vue SPA)
```

## Admin API端点
前缀: `/api/v1/admin/*`
已验证: system/version, settings, dashboard/stats, users, groups, accounts, channels, promo-codes

## 关键文件
- `/var/www/antokex/admin.html` — 自定义管理后台(白底+浅灰侧栏+AK logo+5菜单)
- `/etc/nginx/sites-available/antokex` — Nginx配置
- `/var/www/antokex/login.html` — 跳转目标=/admin
- `/var/www/antokex/register.html` — 跳转目标=/admin
- `/var/www/antokex/index.html` — 首页(四语i18n)
- Logo: `/var/www/antokex/assets/logo.png` (512x512, MD5: 4f155339bf9d005bcad8f88d26944811)

## 踩坑记录
1. Sub2API内置后台(13菜单)必须屏蔽 → /dashboard 302到/admin + 静态页跳转改为/admin
2. Sub2API CSS黑屏 → 不能移除class="dark"，:is(.dark *)选择器依赖
3. 新容器users表空 → 手动bcrypt插入管理员
4. Cloudflare缓存 → 图片加版本号或查询参数

## 已完成里程碑
- [x] 首页部署(v12) — 四语i18n+真实花朵图+暗色主题
- [x] 视觉升级 — 克制高级感动效(光球呼吸/Chat微浮/打字绿点)
- [x] 登录后台修复 — bcrypt插入管理员账户
- [x] 管理后台黑屏修复 — 停止移除dark class
- [x] 自定义admin.html — Codex(小白)编写,白底+浅灰侧栏+AK logo
- [x] 登录跳转修复 — login.html/register.html跳转到/admin
- [x] /dashboard重定向 — 302到/admin防止进入Sub2API内置后台
