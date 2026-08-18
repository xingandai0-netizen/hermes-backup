---
name: webapp-recon
description: "Web application frontend security reconnaissance via browser console. Systematic methodology for tech stack fingerprinting, security header audit, API endpoint enumeration, client-side crypto analysis, and attack surface mapping. Works on any web app accessible via browser."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, recon, webapp, pentest, api-enum, header-audit, frontend-recon, attack-surface]
    related_skills: [pentest-pipeline, vulnclaw, ai-pentest-toolkit, reverse-skill-router, godmode]
---

# Web App Frontend Security Reconnaissance

Systematic methodology for analyzing any web application's security posture through frontend reconnaissance. Uses browser console as the primary tool — no external scanners needed for initial recon.

## When to Use This Skill

Trigger when the user:
- Asks to analyze a website's security
- Wants to find vulnerabilities in a web app
- Says "security research" about a URL
- Asks about a site's tech stack or architecture
- Wants API endpoint enumeration
- Asks to reverse engineer a web app's frontend
- Mentions pentesting a web application

## Quick Start (One Call)

For a fast initial recon, run `scripts/reon-oneliner.js` via browser_console — returns tech stack, scripts, inputs, config, and page structure in one call. Then run `scripts/api-enumerator.js` to extract all API endpoints from JS bundles.

## Real-World Case
See `references/case-982827-gambling-site.md` for a complete recon example (Chinese gambling site analysis with 50+ API endpoints, encryption analysis, and attack vectors).

## Recon Workflow (7 Phases)

Execute phases sequentially. Each phase builds on prior findings.

### Phase 1: Tech Stack Fingerprinting

```javascript
(function(){
  const r = {
    url: window.location.href,
    host: window.location.host,
    framework: null,
    ui_library: null,
    build_tool: null,
    jquery_version: typeof jQuery !== 'undefined' ? jQuery.fn.jquery : 'none',
    // Vue detection
    vue2: !!(document.querySelector('#app')?.__vue__),
    vue3: !!(document.querySelector('#app')?.__vue_app__),
    // React detection
    react: !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__,
    // Angular detection
    angular: !!window.ng || !!document.querySelector('[ng-version]'),
    // Vite detection
    vite: !!document.querySelector('script[type="module"]'),
    // Version leakage
    app_version: window.__APP_VERSION__ || 'not exposed',
    // Server info (from earlier HEAD request)
    scripts_count: document.querySelectorAll('script').length,
  };
  return JSON.stringify(r, null, 2);
})();
```

Also check:
- `lib.js` or `config.js` for site configuration (theme, API base, captcha keys)
- Script filenames for framework/library version hashes
- `__APP_VERSION__` or similar version globals

### Phase 2: Security Header Audit

```javascript
fetch(window.location.href, {method: 'HEAD'})
  .then(r => {
    const headers = {};
    r.headers.forEach((v, k) => headers[k] = v);
    // Check for missing critical headers
    const required = [
      'content-security-policy',
      'x-frame-options',
      'x-content-type-options',
      'strict-transport-security',
      'x-xss-protection',
      'access-control-allow-origin'
    ];
    const missing = required.filter(h => !Object.keys(headers).some(k => k.toLowerCase() === h));
    return JSON.stringify({headers, missing_critical: missing}, null, 2);
  });
```

**Report missing headers as vulnerabilities:**
- No CSP → XSS risk, script injection
- No X-Frame-Options → Clickjacking
- No HSTS → SSL stripping
- No X-Content-Type-Options → MIME sniffing

### Phase 3: API Endpoint Enumeration

Extract ALL API routes from frontend JavaScript bundles:

```javascript
// Find all JS bundle URLs
const jsUrls = [...document.querySelectorAll('script[src]')].map(s => s.src);

// For each bundle, search for API paths
Promise.all(jsUrls.map(url =>
  fetch(url).then(r => r.text()).then(t => {
    const apiPaths = t.match(/["'](api\/[^"']+)["']/gi) || [];
    return {url, apis: [...new Set(apiPaths.map(p => p.replace(/["']/g, '')))]};
  })
)).then(results => {
  const allApis = results.flatMap(r => r.apis);
  const unique = [...new Set(allApis)].sort();
  console.log(JSON.stringify({total: unique.length, endpoints: unique}, null, 2));
});
```

**Categorize endpoints:**
- Auth: login, register, verify, session, logout
- User: profile, account, settings, password
- Financial: deposit, withdraw, transfer, balance
- Admin: if any admin endpoints leak → critical finding
- Public: game lists, banners, notices

### Phase 4: Client-Side Crypto Analysis

Many apps encrypt API responses. Find the decryption logic:

```javascript
// Search main bundle for crypto-related patterns
fetch(MAIN_BUNDLE_URL).then(r => r.text()).then(t => {
  const patterns = ['decrypt', 'encrypt', 'AES', 'DES', 'CryptoJS', 'cipher', 'secret', 'Jr=function', 'function Jr'];
  const found = {};
  patterns.forEach(p => {
    const idx = t.indexOf(p);
    if (idx !== -1) found[p] = t.substring(Math.max(0,idx-100), idx+300);
  });
  return JSON.stringify(found, null, 2);
});
```

**Common patterns in Chinese gambling/scam sites:**
- DES/AES with hardcoded key in JS
- Base64 + custom XOR
- Response wrapper with encrypted `data` field
- Password encoding (simple base64 or custom hash)

### Phase 5: CAPTCHA & Anti-Bot Analysis

```javascript
// Check for CAPTCHA configuration
const captcha = {
  geetest: window.initGeetest ? 'Geetest detected' : 'none',
  recaptcha: window.grecaptcha ? 'reCAPTCHA detected' : 'none',
  hcaptcha: window.hcaptcha ? 'hCaptcha detected' : 'none',
  captcha_id: null,
};

// Search config for captcha keys
if (typeof lib !== 'undefined') {
  captcha.captcha_id = lib.captchaId || 'not in lib';
  captcha.theme = lib.theme || 'unknown';
}

return JSON.stringify(captcha, null, 2);
```

**Check if captchaId is hardcoded** → can be reused for automated requests

### Phase 6: localStorage/sessionStorage/Storage Analysis

```javascript
(function(){
  const r = {
    localStorage_keys: Object.keys(localStorage),
    sessionStorage_keys: Object.keys(sessionStorage),
    cookies: document.cookie,
    // Check for sensitive data in storage
    tokens: Object.keys(localStorage).filter(k =>
      /token|session|auth|jwt|key|secret/i.test(k)
    ).map(k => ({key: k, value_preview: localStorage.getItem(k)?.substring(0, 50)})),
  };
  return JSON.stringify(r, null, 2);
})();
```

### Phase 7: Registration/Auth Flow Analysis

When the target has registration or login, trace the complete flow:

```javascript
// 1. Access Vue/Pinia stores for form config
const app = document.querySelector('#app');
const pinia = app.__vue_app__.config.globalProperties.$pinia;
const userStore = pinia._s.get('user'); // or 'auth', 'login', 'member'
const s = userStore.$state;
JSON.stringify({
  registerFormData: s.registerFormData,
  registerFormConfig: s.registerFormConfig,
  registerRequiredConfig: s.registerRequiredConfig,
  verifyCodeTypeList: s.verifyCodeTypeList,
  inviteConfig: s.inviteConfig,
}, null, 2);
```

```javascript
// 2. Find password encoding function
fetch(MAIN_BUNDLE_URL).then(r => r.text()).then(t => {
  // Search for password hash call
  const pwIdx = t.indexOf('.password)');
  const pw = pwIdx !== -1 ? t.substring(Math.max(0,pwIdx-300), pwIdx+100) : 'not found';
  // Search for common hash libraries
  const hashLibs = ['JS_MD5', 'CryptoJS', 'md5(', 'sha256(', 'Jr=', 'te='];
  const found = {};
  hashLibs.forEach(h => {
    const idx = t.indexOf(h);
    if (idx !== -1) found[h] = t.substring(idx, idx+200);
  });
  return JSON.stringify({password_call: pw, hash_libs: found}, null, 2);
});
```

```javascript
// 3. Analyze CAPTCHA parameters for SMS/code sending
fetch(MAIN_BUNDLE_URL).then(r => r.text()).then(t => {
  const smsIdx = t.indexOf('SendSmsCode');
  const sms = smsIdx !== -1 ? t.substring(Math.max(0,smsIdx-200), smsIdx+300) : 'not found';
  // Find Geetest result fields
  const gtIdx = t.indexOf('captchaObj_result');
  const gt = gtIdx !== -1 ? t.substring(Math.max(0,gtIdx-100), gtIdx+400) : 'not found';
  return JSON.stringify({sms_flow: sms, geetest_params: gt}, null, 2);
});
```

**Key fields to extract:**
- Password encoding: MD5? SHA256? Custom? Is it salted?
- SMS verification: What scene types? What Geetest params needed?
- Registration API: POST or GET? JSON or form-urlencoded?
- Required vs optional fields (from store config, not just HTML)

### Phase 8: Attack Surface Summary

Compile all findings into a structured report:

```
## Attack Surface Report: [domain]

### Tech Stack
- Framework: [Vue/React/Angular + version]
- Server: [nginx/apache + version if leaked]
- Libraries: [jQuery version, UI lib, crypto libs]
- Build: [Vite/Webpack + version hash]

### Critical Vulnerabilities
1. [Header] — missing [header name] → [impact]
2. [Library] — [CVE number] in [library@version] → [impact]
3. [Crypto] — [encryption method] reversible → [impact]

### API Surface
- Total endpoints: [N]
- Auth endpoints: [list]
- Financial endpoints: [list]
- Sensitive endpoints: [list]

### Recommendations
- [Priority 1]: [fix]
- [Priority 2]: [fix]
```

## Pitfalls

1. **Some sites block console access** — Use `browser_console` tool instead of manual DevTools. If blocked, fall back to `web_extract` on JS bundle URLs.

2. **Encrypted responses need JS context** — API responses may be encrypted. Call APIs from within the page's JS context (browser_console) so the app's own interceptor/decryptor processes the response.

3. **SPA hash routing** — Sites with `#/` routing may load different JS chunks per route. Check all chunk files, not just the main bundle.

4. **Dynamic API base URLs** — Some apps configure API base URL at build time (injected into HTML or lib.js). Check `<script>` inline configs and `lib.js`/`config.js` files.

5. **CORS blocks direct fetch** — If fetching API endpoints directly fails with CORS, use the page's own axios/fetch instance via browser_console: `axios.get('api/...')`.

6. **CAPTCHA bypass ≠ automation** — Finding a hardcoded captchaId doesn't mean you can bypass CAPTCHA. Geetest v4 requires solving challenges. But knowing the captchaId helps understand the flow.

7. **Don't trigger real actions** — During recon, only call GET endpoints (lists, configs, public data). Don't POST to registration/login/payment endpoints unless explicitly requested.

8. **Version hash in filenames** — JS bundles often have content hashes (e.g., `index-69fd45ccc37b3f7290f4.js`). Extract the full URL before fetching, not just the filename.

9. **Vue store access requires waiting** — Pinia stores may not be populated immediately. Use `setTimeout(() => {...}, 3000)` or check that `pinia._s.get('storeName')` returns a store before accessing `$state`. Store names vary: 'user', 'auth', 'login', 'member', 'app'.

10. **Variable name conflicts in console** — When running multiple `fetch().then()` chains in sequence, variable names from previous calls persist. Use IIFEs `(function(){...})()` or unique variable names to avoid `SyntaxError: Identifier 'x' has already been declared`.

11. **Password encoding detection** — Search for `function Jr` or `Jr=` patterns, then trace back to the hash library. Common in Chinese sites: `JS_MD5`, `CryptoJS`, custom base64. The variable name (Jr, te, zr) is minified but the library signature (e.g., `JS_MD5_NO_WINDOW`) is not.

## Chinese Gambling/Scam Site Patterns

Common characteristics (from field analysis):
- Disposable domains (random subdomain + numeric main domain)
- Vue 3 + Vant + jQuery (very old jQuery versions)
- Geetest CAPTCHA with hardcoded ID in lib.js
- API responses encrypted (DES/AES with key in frontend JS)
- Theme identifier in lib.js (e.g., "uu", "ao", "as")
- "credit" or "money" site type in config
- No security headers whatsoever
- Version info exposed via `__APP_VERSION__`
- Registration uses form-urlencoded (not JSON)
- Passwords "encoded" with reversible function before sending
