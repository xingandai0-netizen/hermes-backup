# Session Archive: 2026-05-08 大规模antokex.com改造

## 时间
2026-05-08 05:05 - 08:45 (约3.5小时)

## 任务概览
本次session完成了antokex.com平台的全面改造，包括后端定价、前端UI、团队协作等多个方面。

## 完成任务清单

### 1. Sub2API账号重建
- 删除旧Account 5, 6
- 新建Account 7 (OpenAI, Group 3) + Account 8 (Anthropic, Group 4)
- 手动INSERT account_groups关联
- API Key: tp-cbfq09kodybh93u15ir9op45oijremttcw8l7s5bqgp5xk6q

### 2. 模型定价配置（CNY，与小米官网一致）
- mimo-v2.5-pro: ¥7/¥21/¥1.4 per 1M tokens
- mimo-v2-pro: ¥7/¥21/¥1.4
- mimo-v2.5: ¥2.8/¥14/¥0.56
- mimo-v2-omni: ¥2.8/¥14/¥0.56
- mimo-v2-flash: ¥0.7/¥2.1/¥0.07
- TTS系列: 免费
- Channel 4 配置了8条定价规则（OpenAI+Anthropic各4条）

### 3. 首页改造
- 删除定价展示section
- 添加"最新支持ANTOKEX"大封面卡片（抽象花朵图片，无文字叠加）
- 封面图片来源: ~/Desktop/图片池/抽象花_05.png
- 点击跳转到 /antokex-tools 详细工具页面

### 4. 工具页面 /antokex-tools
- 创建独立HTML页面，17个AI工具
- 原有10个: ChatBox, NextChat, LobeChat, Cherry Studio, Cursor, Cline, Roo Code, Claude Code, OpenCode, BotGem
- 新增7个: Open WebUI, FastGPT, Dify, ComfyUI, Stable Diffusion WebUI, SillyTavern, KoboldCpp
- 每个工具有官网链接+配置指南链接
- Nginx添加 /antokex-tools 路由

### 5. 管理后台增强 (brand-replace.js v4→v9)
- Logo点击返回首页（admin→/admin, user→/dashboard）
- 侧边栏新增"ANTOKEX工具"分组（2个菜单项）
  - 快速配置工具: 12个工具accordion详细攻略
  - 快速更换本站模型: 12个工具模型切换指南
- 新增Hermes Agent攻略
- CSP修复: inline onclick改为addEventListener
- 兼容admin和user两种侧边栏DOM结构
- localStorage key: access_token + auth_user
- 首页登录状态: setTimeout(1500ms)防i18n覆盖
- $→¥货币替换（正则 /\$(\s*\d)/g）

### 6. 用户后台修复
- 移除Nginx /dashboard→/admin 重定向
- 用户后台侧边栏菜单项注入（DOM结构不同）
- 用户点击账号跳转: admin→/admin, user→/dashboard

### 7. 首页登录状态
- 检查localStorage access_token + auth_user
- 登录按钮隐藏，显示用户名
- admin用户跳/admin，普通用户跳/dashboard

### 8. 小黑中转站配置
- 创建Hermes Agent Key (ID 25, 541098012@qq.com, Group 3)
- config.yaml改为antokex provider
- .env添加ANTOKEX_API_KEY
- 当�session仍用旧配置（直连小米），新session生效

## 关键技术决策
1. CSP安全策略: 禁止inline onclick，改用addEventListener
2. Sub2API localStorage keys: access_token + auth_user
3. Nginx静态文件路由: /antokex-tools, /ai-tools等需要单独location块
4. account_groups表需手动INSERT+restart
5. $→¥替换: 只替换后跟数字的$，不影响其他上下文

## 踩坑记录
1. Nginx sed插入location块容易破坏配置结构
2. Sub2API Key创建后只返回一次完整key，数据库存掩码
3. mimo-v2-flash模型列表有但不支持chat completions
4. mimo-v2.5-pro响应慢(30s+)，推理token消耗大
5. 首页i18n系统会覆盖JS设置的按钮文字，需延迟执行
6. Cloudflare CSP阻止inline onclick事件处理

## 当前状态
- antokex.com: HTTP 530 (阿里云欠费，服务器暂停)
- 小黑: 直连小米API正常工作
- 定价: CNY配置完成
- 工具页面: 17个工具已部署
- 管理后台: v9版本功能完整

## 待办
- [ ] 阿里云充值后验证网站恢复
- [ ] 小黑切换到antokex中转站（新session生效）
- [ ] 实测新增7个工具能否通过中转站
