## MiMo（小米）— 官方定价（2026-08 更新）

**API平台**: https://platform.xiaomimimo.com
**API基础URL**: https://token-plan-cn.xiaomimimo.com/v1 (OpenAI) / /anthropic (Anthropic)
**协议**: OpenAI + Anthropic 双协议
**计费模型**: Token Plan 预付费套餐制 + 按量API
**定价文档**: https://platform.xiaomimimo.com/static/docs/pricing.md
**llms.txt**: https://platform.xiaomimimo.com/llms.txt

---

## 一、按量API定价（元/1M tokens, ≤256K上下文）

### 国内定价

| 模型 | Input(Cache Hit) | Input(Cache Miss) | Output |
|------|:-:|:-:|:-:|
| mimo-v2.5-pro | ¥1.40 | ¥7.00 | ¥21.00 |
| mimo-v2.5 | ¥0.56 | ¥2.80 | ¥14.00 |
| mimo-v2-flash | ¥0.07 | ¥0.70 | ¥2.10 |
| TTS全系 | 限时免费 | — | — |

> 超过256K上下文时价格翻倍（如pro: Input Miss ¥14.00, Output ¥42.00）
> V2系列（mimo-v2-pro, mimo-v2-omni等）已于2026-06-30下线

### 海外定价（$/1M tokens, ≤256K上下文）

| 模型 | Input(Cache Hit) | Input(Cache Miss) | Output |
|------|:-:|:-:|:-:|
| mimo-v2.5-pro | $0.20 | $1.00 | $3.00 |
| mimo-v2.5 | $0.08 | $0.40 | $2.00 |
| mimo-v2-flash | $0.01 | $0.10 | $0.30 |
| TTS全系 | 限时免费 | — | — |

### 网络搜索插件
- 国内: ¥25/1000次
- 海外: $5/1000次

---

## 二、Token Plan 订阅套餐

### 四档月度套餐

| 档位 | 月费 | 包年月均 | Credits/月 | 约Pro模型输出token量 |
|------|------|----------|-----------|-------------------|
| Lite | ¥39 ($6) | ¥34.32 | 41亿 | ~680万token |
| Standard | ¥99 ($16) | ¥87.12 | 110亿 | ~1,830万token |
| Pro | ¥329 ($50) | ¥289.52 | 380亿 | ~6,330万token |
| Max | ¥659 ($100) | ¥579.92 | 820亿 | ~1.37亿token |

> 四档模型权限完全相同，区别仅在Credits额度。Lite一样能调mimo-v2.5-pro，只是消耗更快。

### ⚠️ Credits ≠ Tokens（常见混淆）

"110亿Credits" ≠ "110亿tokens"。Credits是MiMo内部计量单位，需按倍率换算。
- Standard的110亿Credits，用Pro模型约=1.8亿token
- 用标准模型约=11亿token
- 闲鱼/论坛上说的"百亿token"实际是Credits

### Credits消耗倍率（Token Plan内）

| 模型 | 缓存命中 | 未命中输入 | 输出 | 单位 |
|------|---------|-----------|------|------|
| MiMo-V2.5-Pro | 2.5 | 300 | 600 | Credits/百万token |
| MiMo-V2.5（标准版） | 2 | 100 | 200 | Credits/百万token |
| ASR | — | 30M/小时 | 30M/小时 | Credits/音频小时 |
| TTS系列（3款） | 限时免费 | 限时免费 | 限时免费 | 0x不消耗 |

### 优惠体系

**支付层折扣：**
- 首购88折（仅首月，每账号1次）
- 连续包年88折（全年每月自动扣款）
- 邀请码首单9折（双方各得¥10体验金）
- 自动续费：新用户77折、老用户7折（与首购互斥）

**消耗层折扣：**
- 北京时间0:00-8:00非高峰期，Credits消耗×0.8（等于多25%额度）

### 0.01元续费漏洞（已修复，2026-05-30后失效）

**原理：** 早期正价订阅的用户，系统在续费时自动补偿23%差价（因新用户有77折但老用户没有）。补偿金额+77折=价格变负数，最低只收0.01元。

**操作：** 开启自动续费→点击续订→支付宝实际扣0.01元→关闭自动续费

**当前状态：** 5月30日后小米已取消月续费折扣，此漏洞已修复。闲鱼上仍有库存或新号首购渠道在售（约¥40/月Standard）。

---

## 三、API Key格式区分

- Token Plan专用Key: `tp-xxxxx`（Base URL不同）
- 开放API按量Key: `sk-xxxxx`
- 两者互不通用，不能混用

## 四、支持的编程工具

OpenCode、OpenClaw、Claude Code、Kilo Code、Cline、Roo Code、Codex、Qwen Code、Cherry Studio、Zed、TRAE

## 五、套餐规则

- 同时只能买1个套餐
- 支持补差价升级，不支持降级
- Credits用完或到期即停服，不退不转
- 只能用于编程工具场景，禁止用于自动化脚本/自建后端
- TTS限时免费不等于永远免费，随时可能收费

## 六、获取方式

需要小米账号 → platform.xiaomimimo.com → Token Plan后台 → 购买套餐
