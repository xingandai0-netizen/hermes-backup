# Platform Security Mechanism Comparison

## Discord

| Aspect | Mechanism | Difficulty |
|--------|-----------|------------|
| Registration | Email + optional phone | ⭐⭐ |
| Captcha | hCaptcha | ⭐⭐ (easily bypassed via anti-captcha) |
| Phone verification | International numbers OK | ⭐⭐ |
| Cost per account | $0.1-0.5 | Low |
| Risk level | Medium (US jurisdiction) | - |

**Known bypass tools**: 3281448091/Discord-Token-Gen (346★), my-personal-hell/discord-account-generator (124★)

## KOOK (开黑啦)

| Aspect | Mechanism | Difficulty |
|--------|-----------|------------|
| Registration | Chinese phone number required | ⭐⭐⭐⭐⭐ |
| Captcha | Geetest/Tencent captcha | ⭐⭐⭐⭐ |
| Phone verification | Chinese real-name only | ⭐⭐⭐⭐⭐ |
| Cost per account | $2-5 | High |
| Risk level | High (Chinese law) | - |

**Key restrictions** (from ToS):
- Same phone = 1 account only
- Same identity ≤ 3 accounts
- 7-day security observation period
- Real-name required for certain features

**Transferability**: Discord tools CANNOT be used for KOOK. Complete rewrite needed.

## Cross-Platform Non-Transferability (Critical Finding)

When user asks "can I use Discord tools for KOOK/Telegram/etc?", the answer is **NO** for each combination:

| From → To | API Match? | Captcha Match? | Phone Match? | Verdict |
|-----------|-----------|---------------|-------------|---------|
| Discord → KOOK | ❌ | ❌ (hCaptcha vs Geetest) | ❌ (Intl vs CN real-name) | **Impossible** |
| Discord → Telegram | ❌ | N/A (SMS only) | ⚠️ (Intl OK) | Partial overlap |
| KOOK → Discord | ❌ | ❌ | ❌ | **Impossible** |

Each platform requires completely independent tooling. The only transferable knowledge is:
- Architecture patterns (how bypass modules are structured)
- External service integrations (same sms-activate, same captcha solvers)
- Code patterns (how to handle API responses)

## Telegram

| Aspect | Mechanism | Difficulty |
|--------|-----------|------------|
| Registration | Phone number | ⭐⭐⭐ |
| Captcha | None (SMS only) | ⭐ |
| Phone verification | International OK | ⭐⭐⭐ |
| Cost per account | $0.5-2 | Medium |
| Risk level | Medium | - |

## General Pattern

```
Verification difficulty ranking:
KOOK > Discord > Telegram

Cost ranking:
KOOK > Telegram > Discord

Legal risk ranking:
KOOK (Chinese law) > Telegram > Discord (US law)
```
