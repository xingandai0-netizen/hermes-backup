# External Services Used by Gray-Market Tools

## Phone Verification Services

| Service | Purpose | Cost | Notes |
|---------|---------|------|-------|
| sms-activate.ru | Temporary phone numbers | $0.1-0.5/number | Most common, supports many platforms |
| kopeechka | Temporary email verification | $0.01-0.05/email | Email-based verification |

## Captcha Solving Services

| Service | Purpose | Cost | Notes |
|---------|---------|------|-------|
| anti-captcha | Solve hCaptcha/reCAPTCHA | $0.001-0.005/solve | API-based, Python/JS libs |
| capmonster | Solve hCaptcha/reCAPTCHA | $0.001-0.005/solve | Similar to anti-captcha |
| 2captcha | Multi-captcha solver | $0.001-0.003/solve | Supports Geetest |

## Proxy Services

| Service | Purpose | Cost | Notes |
|---------|---------|------|-------|
| Residential proxies | IP rotation | $1-5/GB | Needed for bulk operations |
| SOCKS5 proxies | Connection routing | $0.5-2/GB | Lower detection rate |

## Exfiltration Channels

| Method | Purpose | Notes |
|--------|---------|-------|
| Discord webhook | Data exfiltration | Free, easy to set up |
| Telegram bot | Data exfiltration | Free, more reliable |
| C2 panels | Command & control | Commercial, more features |

## Cost Calculation Template

```
Per-unit cost:
- Phone number: $X
- Captcha solve: $X
- Email (if needed): $X
- Proxy (amortized): $X
─────────────────────
Total: $X/unit

Revenue:
- Selling price: $X/unit
- Profit margin: X%

Daily potential:
- Units/day: X
- Daily profit: $X
```
