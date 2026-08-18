# MiMo API 集成归档 — 2026-05-07

## 概述
将小米 MiMo v2.5 API 完整集成到 Sub2API (antokex.com) 平台，实现用户自助注册→充值→创建Key→调用MiMo全流程。

## 最终成果
- **状态**: ✅ 完成
- **中转地址**: https://antokex.com/v1/chat/completions
- **认证方式**: Bearer Token (Sub2API生成的sk-开头key)
- **兼容格式**: OpenAI Chat Completions

## 服务器信息
- **IP**: 47.99.55.244 (域名antokex.com不可SSH，必须用IP)
- **部署方式**: Docker Compose @ /opt/sub2api/deploy/
- **容器**: sub2api (port 8080, 健康), sub2api-postgres (port 5432), sub2api-redis (port 6379)
- **Sub2API版本**: v0.1.124 (commit e872cbe, 2026-05-07部署)
- **旧版本问题**: v0.1.114缺少 forwardAsRawChatCompletions 导致 /v1/chat/completions 被路由到 /v1/responses 返回404

## MiMo 账户配置
| 项目 | 值 |
|------|-----|
| Sub2API Account ID | 3 |
| Group ID | 3 ("Xiaomi MiMo") |
| Platform | OpenAI |
| MiMo Base URL | https://api.xiaomimimo.com/v1 |
| MiMo API Key | sk-c2jttr2m1loqo5ho6l81uwx4wr8gwhobq814vsorj95xhle8 |
| openai_responses_supported | false (关键! 必须关闭) |
| model_whitelist | ["mimo-v2-flash", "mimo-v2-omni", "mimo-v2-pro", "mimo-v2.5", "mimo-v2.5-pro"] |

## 模型测试结果 (antokex.com 中转)

### ✅ 可用 (Chat模型 — 5个)
| 模型 | HTTP | 说明 |
|------|------|------|
| mimo-v2.5-pro | 200 | 旗舰模型, 1T参数, 1M上下文 |
| mimo-v2.5 | 200 | V2.5标准版 |
| mimo-v2-pro | 200 | V2 Pro |
| mimo-v2-flash | 200 | 轻量快速版 |
| mimo-v2-omni | 200 | 多模态版 |

### ❌ 不可用 (TTS模型 — 4个, 预期行为)
| 模型 | HTTP | 原因 |
|------|------|------|
| mimo-v2-tts | 400 | TTS不走chat/completions格式 |
| mimo-v2.5-tts | 400 | TTS不走chat/completions格式 |
| mimo-v2.5-tts-voiceclone | 400 | TTS不走chat/completions格式 |
| mimo-v2.5-tts-voicedesign | 400 | TTS不走chat/completions格式 |

## 踩坑记录

### 1. 404错误 — 路由问题
**问题**: 用户key调用返回404, admin key正常
**根因**: 旧版Sub2API (v0.1.114) 将OpenAI ChatCompletions路由到 /v1/responses 端点, 而MiMo只支持 /v1/chat/completions
**解决**: 升级到v0.1.124, 新版有 forwardAsRawChatCompletions 逻辑, openai_responses_supported=false 时直接转发
**验证**: 检查 openai_gateway_chat_completions.go 中 shouldUseResponsesAPI() 返回false时的代码路径

### 2. INVALID_API_KEY — Redis缓存问题
**问题**: 容器重启后, 之前创建的user key返回401 INVALID_API_KEY
**原因**: Redis缓存清空后key未重新加载
**解决**: 删除旧key, 重新创建新key即可

### 3. INSUFFICIENT_BALANCE — 余额检查
**问题**: 用户DB余额=100但API返回余额不足
**原因**: Redis billing:balance 缓存未同步
**解决**: 重启容器清Redis缓存 + 用户充值后重新测试

### 4. 模型名大小写
**问题**: 大写模型名(MiMo-V2.5)返回400
**解决**: MiMo API要求全小写(mimo-v2.5)

### 5. TTS模型
**问题**: 4个TTS模型都返回400 Param Incorrect
**原因**: TTS模型不支持chat/completions格式, 需要特殊的TTS API端点
**结论**: 这是预期行为, TTS模型不通过中转站使用

## 用户自助流程 (已验证通过)
1. 访问 antokex.com → 注册账号
2. 登录 → 充值余额
3. 进入 Dashboard → 创建 API Key (选择 Group: Xiaomi MiMo)
4. 使用 Key 调用 https://antokex.com/v1/chat/completions

## 订阅计划
| 项目 | 值 |
|------|-----|
| Plan ID | 1 |
| 名称 | MiMo Pro |
| Group | 3 (Xiaomi MiMo) |
| 价格 | $9.99 (原价$19.99, 5折) |

## 关键配置
```yaml
# accounts table (id=3)
platform: openai
extra:
  model_whitelist: ["mimo-v2-flash", "mimo-v2-omni", "mimo-v2-pro", "mimo-v2.5", "mimo-v2.5-pro"]
  openai_responses_supported: false  # 关键! 必须设为false

# groups table (id=3)
supported_model_scopes: []  # 清空, 不需要Antigravity平台的scopes

# channel_model_pricing (id=1)
account_id: 4
models: ["mimo-v2.5-pro"]
input: $0.000001/token
output: $0.000003/token

# settings
default_balance: 0  # 新用户默认无余额, 需手动充值
```

## 首页对话框集成 (2026-05-07)

### 概述
将首页静态展示对话框改造为真实MiMo API流式对话功能，用户可在首页直接与MiMo对话。

### Demo架构
| 项目 | 值 |
|------|-----|
| Demo User ID | 6 (demo@antokex.com) |
| Demo Account ID | 4 (platform=openai, priority=10) |
| Demo Key ID | 9 (sk-demo-...49fe) |
| 余额限制 | $10 |
| 模型限制 | mimo-v2.5-pro only (account level) |
| 前端限流 | 10条消息/session, 超限提示注册 |

### 实现方案
- **方案**: 前端直接调用Sub2API relay, demo key嵌入HTML (公开但限额)
- **API端点**: `/v1/chat/completions` (相对路径, 走同源Nginx代理)
- **流式输出**: SSE streaming, ReadableStream解析
- **多轮对话**: 从DOM提取历史消息构建messages数组, 跳过欢迎消息
- **模型切换**: 下拉框5个MiMo模型可选, 默认V2.5 Pro
- **四语支持**: zh/en/ja/ko全部更新, 含chat_welcome/chat_limit/chat_error/chat_thinking

### 关键文件
| 文件 | 说明 |
|------|------|
| `/var/www/antokex/index.html` | 首页HTML, 含chat CSS+HTML+JS |
| Demo Key SQL | `INSERT INTO api_keys (user_id, key, name, group_id, status) VALUES (6, 'sk-demo-...', 'Homepage Demo', 3, 'active')` |

### JS架构
- IIFE闭包, DEMO_KEY/API_URL/MAX_FREE_MSGS常量
- getDict() 读取当前语言翻译
- sendChat() 异步流式调用
- appendUserMsg/createAiMsg/createTyping/removeTyping DOM操作
- showLimitMsg() 超限提示+注册链接
- Enter键发送 + 打字动画 + 滚动到底部

### 依赖
- Sub2API v0.1.124 (streaming support)
- Demo account (ID=4) with mimo-v2.5-pro whitelist
- Nginx proxy `/v1/*` → Sub2API Docker

## 未完成
- [ ] TTS模型需要特殊API端点, 当前不支持
- [ ] "小米"平台UI选项 (CreateAccountModal.vue修改) — 需要前端代码变更
- [ ] 新用户默认余额设置 (目前default_balance=0)
