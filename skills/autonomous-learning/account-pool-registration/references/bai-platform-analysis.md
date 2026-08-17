# B.AI (AINFT) 平台分析

> 来源: 2026-05-10 session | 分析人: 小黑

## 基本信息

- 主站: https://b.ai
- 后台/母公司: AINFT (https://ainft.com)
- API网关: https://api.b.ai (仅开放 /v1/chat/completions, /v1/messages, /v1/models)
- 后端Analytics: posthog.prd.ainft.com

## 注册机制

**确认: 加密钱包连接注册，无需邮箱/手机/实名。**

代码证据:
```
"链上地址作为永久身份（ID）"
"无摩擦、匿名的API通道"
"加密钱包进行资金自筹和自主结算"
```

注册时需要:
1. 连接MetaMask/OKX等加密钱包
2. 签名验证（Sign Message）
3. 无需任何传统身份信息

## 积分/赠送

- 注册赠送: 500,000 积分（用户声称，未实测验证）
- 充值优惠: "充值立享 1:1 赠送，最高...等额积分"
- 积分价值换算: 待实测（不清楚1积分 = 多少token）

## 联系渠道

从JS提取的联系方式:
- Telegram
- Discord
- X (Twitter)
- Medium
- 邮箱: 平台提到了 "邮箱" 但未找到具体地址

## 批量注册可行性

**极高** — Python一行代码生成一个钱包地址，无需任何外部依赖。

潜在障碍:
1. 需要浏览器自动化连接钱包（Playwright + MetaMask扩展）
2. 平台可能有IP风控
3. 积分可能有使用限制（特定模型、有效期）
4. 需实测验证具体流程

## 技术栈

- 前端: React SPA
- 国际化: i18next (支持 zh, en, es, ja)
- Analytics: PostHog
- Cookie Domain: b.ai

## 待验证项

- [ ] 实际注册确认钱包签名流程
- [ ] 积分到账方式（自动/手动领取）
- [ ] 积分与API调用量的换算
- [ ] 支持的模型列表（需要有效API Key）
- [ ] 积分有效期
- [ ] 同一钱包地址是否可以多次注册
