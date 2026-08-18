# Case Study: 982827.com Gambling Site Recon (2026-08-12)

## Target
- URL: https://b1qtfhjzt5p.982827.com/m/#/home
- Type: Macau Lisboa online gambling platform
- Theme: uu, Site type: credit

## Tech Stack
- Vue 3 + Vite (v1.5.13.315)
- Vant UI (mobile)
- jQuery 1.10.2 (CVE-2015-9251, CVE-2019-11358, CVE-2020-11022/11023)
- Axios, Geetest CAPTCHA v4, Nginx, Hash routing

## Key JS Files
- /m/static/lib.js — Site config (theme, captchaId, device type)
- /m/static/assets/js/api-*.js — API endpoint definitions
- /m/static/assets/js/store2-*.js — State management
- /m/static/assets/js/index-*.js — Main bundle (auth, crypto)
- /m/static/gt.js — Geetest CAPTCHA loader (Botion Inc v1.0.3)

## Security Headers: ALL MISSING
CSP, X-Frame-Options, X-Content-Type-Options, HSTS, X-XSS-Protection, CORS

## Information Leakage
- Server: nginx
- App version: 1.5.13.315
- CAPTCHA ID hardcoded in lib.js: 26a8228fcfee3424d7ea11653a8e5783
- Full API surface in client-side JS

## API Endpoints Extracted (50+)
Auth: POST api/User/Register, api/User/CheckLoginFirstStep, api/User/SendSmsCode, api/Api/GetVerifyCodeNew, api/User/RegProperties (encrypted), api/User/CheckSession, api/User/OutLogin, api/User/GetUserLoginKey, api/User/GetAuthCode
User: api/User/GetUserInfo, api/User/GetAccount, api/User/UpdateUserInfo, api/User/GetAccountNew, api/User/ModifyMemberInformation, api/User/ReName, api/User/UpdPass
Financial: api/User/TransferOperate, api/User/GetOrderList_New, api/User/GetTransList, api/User/GetUserbetRpt, api/User/GetReturnAmtToWallet, api/YuBao/UserAccoutBal2TrsAccountBal
Game: api/Web/GetMobileAllGameList, api/Web/GetHotMainList, api/Web/GetEGamesList, api/Web/GetHotEGamesList, api/Web/GetNewEGamesList, api/Web/GetRecEGamesList, api/Web/GetHotBrandList, api/Web/GetHotFishList, api/Web/GetBuYuSubClassList
Promo: api/Act/GetSignConfigInfo, api/Act/PostSignIn, api/Act/RotaryPost, api/Act/GetRotary, api/Act/GetFriendList, api/Act/GetAwardsList, api/Act/GetHongbaoyuInfo, api/Act/PostHongbaoyu
Config: api/Web/isOpenSmsLogin, api/Web/GetAllBasicWebsiteConfigurationNew, api/Web/WhetherGoLoginPage, api/User/GetAgentMode, api/User/RegProperties
Message: api/User/GetMessageList, api/User/GetNoReadMessageCount, api/User/AddUserMsgConsult, api/User/GetUserMsgConsultList
Shop: api/shop/GetShopUserAddressList, api/shop/ShopUserAddressAdd

## Registration Flow Detail

### Form Fields (from Pinia store `user.$state`)
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| mobile | tel | yes | 11-digit Chinese phone |
| password | password | yes | 6-15 alphanumeric |
| confirmPassword | password | yes | Must match |
| realName | text | no | From config |
| wechat/qq/email | text | no | Optional contact |
| inviteCode | text | no | Referral code |
| imgCode | text | no | Image CAPTCHA |
| msgCode | text | no | SMS verification code |

### Password Encoding
- Function: `Jr(r.password)` where `Jr = te(zr)`
- `zr` = JS_MD5 library (detected by `JS_MD5_NO_WINDOW` env check)
- **Encoding: plain MD5, no salt**
- Sent as form-urlencoded, not JSON

### Geetest v4 CAPTCHA Flow
1. Geetest initialized: captchaId="26a8228fcfee3424d7ea11653a8e5783", product="float", riskType="slide", language="zho"
2. After slide challenge, result stored in `window.captchaObj_result`
3. SMS sending params:
   - `GeeVer: 40`
   - `userkey`: `captchaObj_result.gen_time`
   - `geetest_challenge`: `captchaObj_result.lot_number`
   - `geetest_validate`: `captchaObj_result.captcha_output`
   - `geetest_seccode`: `captchaObj_result.pass_token`

### Registration API Call
```
POST api/User/Register
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Body: mobile=...&password=MD5hex(...)&confirmPassword=MD5hex(...)&realName=...&msgCode=...&version=1.5.13.315
```
Response: encrypted (frontend JS decrypts)

### Pinia Store Keys (user store)
`userInfo, account, loginState, errors, formData, loading, openRegisterBonus, clearNoticeCount, loginType, registerFormData, registerFormConfig, registerRequiredConfig, registerAttrNames, inviteConfig, isCode, verifyCodeTypeList, getWebConfig, isAllPeopleAgent, isMyRecommend`

## Attack Vectors
1. jQuery 1.10.2 known CVEs (CVE-2015-9251, CVE-2019-11358, CVE-2020-11022/11023)
2. Clickjacking (no X-Frame-Options, site can be iframed)
3. Crypto reversal (encryption keys in frontend JS)
4. CAPTCHA bypass (hardcoded captchaId in lib.js)
5. No CSP (arbitrary script injection possible)
6. MD5 password hashing (weak, no salt, rainbow-tableable)
7. Version info leakage (__APP_VERSION__ = 1.5.13.315)
8. Disposable domain pattern (random subdomain + numeric main domain)
