# ANTOKEX 后台管理页面 — 最终状态归档 (2026-05-07 最终版)

## 任务总结
将后台管理从自定义admin.html(5菜单)切回Sub2API原生dashboard(13+菜单)，
用CSS/JS注入实现白色ANTOKEX品牌主题，保持所有Sub2API功能不变。

**状态: ✅ 已完成**

## 架构（当前生效）
```
/admin     → Nginx proxy → Sub2API (127.0.0.1:8080) + CSS/JS注入白色主题
/dashboard → 302 /admin
/login     → 静态 login.html → 跳转 /admin
/register  → 静态 register.html → 跳转 /admin
```

## 服务器: 47.99.55.244
- Sub2API Docker: port 8080, healthy, v0.1.114
- Nginx: port 8088, active
- PostgreSQL: port 5432
- Redis: port 6379

## 生效的注入文件（/var/www/antokex/assets/）
| 文件 | 大小 | 用途 |
|------|------|------|
| antokex-admin-theme.css | 10,092B | 白色主题CSS，覆盖Sub2API的.dark深色 |
| antokex-brand-replace.js | 5,124B (v4) | 品牌文字替换+CSS注入+侧边栏inline白化 |

## 品牌替换内容
- Sub2API → ANTOKEX
- Subscription to API Conversion Platform → Multi-Model AI API Platform
- © 2026 Sub2API → © 2026 ANTOKEX
- 侧边栏/主区域背景全部白化(#FFFFFF/#F8FAF9)
- 主色: #2D8C5A (绿色)

## Nginx注入机制
```nginx
# /admin location块关键行:
sub_filter '</head>' '<link rel="icon" ... href="/favicon.ico"></head>';
sub_filter '</body>' '<script src="/assets/antokex-brand-replace.js?v=3"></script></body>';
sub_filter_once off;
sub_filter_types text/html;
```

## Sub2API原生菜单(13+)
Dashboard, Ops, Users, Groups, Channels, Subscriptions, Accounts,
Announcements, Proxies, Redeem Codes, Promo Codes, Usage, Settings
+ My Account: API Keys, Usage, My Subscriptions, Redeem, Profile

## ⚠️ 关键踩坑
1. 不能移除Sub2API的class="dark" → 会导致CSS全失（Sub2API用:is(.dark *)选择器）
2. 侧边栏用inline style强制覆盖 → Sub2API侧边栏选择器特异性极高
3. 旧admin.html(79KB)仍存在于服务器但Nginx不再代理它
4. Codex进程残留输出会触发watch pattern通知 → 忽略即可

## 废弃文件（服务器上仍存在，不再使用）
- /var/www/antokex/admin.html (79KB) — 旧自定义后台，已废弃
- antokex-brand.js, antokex-brand-v9.js — 旧品牌脚本
- antokex-dashboard-override.css/js — 旧覆盖文件
- antokex-home.css/js — 首页专用（非后台相关）

## 登录凭证
Email: 18957167833@163.com
Password: Dxa19990210
