# antokex.com 完整记忆

## 架构
- 阿里云47.99.55.244 → Cloudflare Tunnel → nginx:8088 → Sub2API Docker:8080
- nginx配置: /etc/nginx/sites-available/antokex
- CSS/JS文件: /var/www/antokex/assets/
- 首页=静态HTML，Sub2API仅处理/api/*后端

## 首页渲染历史
Sub2API通过`window.__APP_CONFIG__.home_content`配置项渲染首页，该字段存储在数据库中。home_content包含完整CSS+HTML+JS，但CSS语法被破坏（大括号`{`丢失）。nginx sub_filter注入的外部CSS/JS是冗余的——SPA先用home_content渲染，外部文件加载太晚。Sub2API暗色主题用`html.dark` + `body:is(.dark *)`高特异性选择器，我们的CSS必须用`#antokex-home` ID前缀覆盖。

## 当前状态 (2026-05-06)
- 首页=静态HTML，品牌=文字ANTOKEX
- 登录/注册页=静态HTML+四语i18n(中英日韩)+白底黑字A logo+纯黑左侧面板
- Sub2API仅处理/api/*后端
- Nginx v11.1: 新增/assets/静态路由(try_files $uri =404)修复图片Content-Type问题
- CSS/JS文件:/var/www/antokex/assets/
- 首页"为什么选择ANTOKEX"区域图片为4张真实花朵摄影(600x400)：樱花/向日葵/睡莲/郁金香 ✅

## 图片替换历程
1. v1: AI生成青蓝色调梦幻花朵 → 阿戴批评"太模糊，虚焦太重"
2. v4: AI生成莲花/樱花/玫瑰/大丽花 → 阿戴批评"不如之前，没有真实性"
3. v5: 真实花朵摄影(Unsplash) → 阿戴确认 ✅

## Skill记录
- antokex-website-modification (devops): 架构概览、文件路径速查、部署流程、Logo规范、图片规范(600x400 PIL裁切)、四语i18n系统、Sub2API品牌替换、踩坑记录6条、验证清单、服务器信息

## 踩坑记录
1. /assets/ 路由被catch-all拦截 → 需显式location /assets/ { try_files $uri =404; }
2. Cloudflare缓存导致图片不更新 → 文件名加版本号
3. Sub2API home_content CSS破坏 → 改用静态HTML首页绕过
4. Nginx sub_filter只替换第一次 → 需sub_filter_once off
5. PIL不在execute_code sandbox中 → 用terminal直接运行python3
6. 竖版图片在横版网格中变形 → 上传前用PIL中心裁切到600x400

## 成功的真实花朵图片URL
- 樱花: https://images.unsplash.com/photo-1522383225653-ed111181a951?w=800&h=500&fit=crop
- 向日葵: https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=800&h=500&fit=crop
- 睡莲: https://images.unsplash.com/photo-1518882174711-1de40238921b?w=800&h=500&fit=crop
- 郁金香: https://images.unsplash.com/photo-1524386416438-98b9b2d4b433?w=800&h=500&fit=crop
