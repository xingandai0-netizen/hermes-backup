# ANTOKEX 详细日志

## 概要索引
- 部署架构: 47.99.55.244 | Cloudflare Tunnel → nginx:8088 → Sub2API:8080
- 前端注入: nginx sub_filter 注入 antokex-home.css + antokex-home.js + antokex-brand.js
- 首页内容: home_content 存储在数据库，通过 window.__APP_CONFIG__ 渲染

## 关键问题与修复
1. CSS排版丢失(2026-05-05): antokex-home.css选择器以#antokex-home开头，但SPA容器无此ID。修复: brand.js v7自动注入id。
2. CSP阻断onclick(2026-05-05): Sub2API CSP头无'unsafe-inline'，阻断所有inline事件处理器。
3. Logo替换(2026-05-05): 替换了3个位置的logo.png，但当前仍是Sub2API默认蓝底S图标。**需替换为白底黑字大写"A"**。
4. Cloudflare缓存: 无有效API Token无法手动purge。
5. 标题重复: "多模型 多模型" 和 "常见问题问题" 由SPA组件与home_content重叠导致。

## 文件清单
- /var/www/antokex/assets/antokex-brand.js (v7, 自动注入#antokex-home)
- /var/www/antokex/assets/antokex-home.css (CSS样式，#antokex-home作用域)
- /var/www/antokex/assets/antokex-home.js (交互逻辑)
- /var/www/antokex/logo.png (需替换为白底黑字A)
- /var/www/antokex/assets/logo.png (需替换)
- /var/lib/docker/volumes/deploy_sub2api_data/_data/public/logo.png (需替换)
