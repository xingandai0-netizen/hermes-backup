# 用户浏览器Auth Token提取流程

## 背景
当agent的headless浏览器被网站拦截（Google OAuth、验证码、bot检测）时，
需要让用户在自己的浏览器中登录，然后提取auth token给agent使用。

## 完整流程

### Step 1: 让用户提供账号
用户提供目标网站的登录凭据（邮箱+密码）。

### Step 2: 尝试agent浏览器登录（通常会失败）
```
browser_navigate → 登录页面
输入邮箱密码 → Google OAuth拦截 / 邮箱验证码
```

### Step 3: 切换到用户浏览器提取模式
告诉用户：
```
"请在你的浏览器中登录目标网站，然后：
1. 按 Cmd + Option + I 打开DevTools（Mac）
2. 点击Console标签
3. 执行以下代码..."
```

### Step 4: 提取localStorage中的auth信息
让用户执行：
```javascript
JSON.stringify(Object.entries(localStorage).filter(([k, v]) => 
  k.includes('token') || k.includes('auth') || k.includes('session') || 
  k.includes('user') || k.includes('login') || k.includes('device') || k.includes('refresh')
))
```

如果上面没结果，试更宽泛的：
```javascript
JSON.stringify(Object.entries(localStorage).filter(([k, v]) => 
  v && v.length > 10 && v.length < 500
))
```

### Step 5: 提取cookie（通常是httpOnly，JS读不到）
```javascript
document.cookie
```
注意：httpOnly cookie无法通过JS读取，但会自动随请求发送。

### Step 6: 获取画布ID和用户ID
从localStorage中找：
- `starter-tutorial-storage:*` → 包含 canvasId 和 userId
- `mp_*_mixpanel` → 包含 distinct_id 和 $user_id
- `refresh_token` → 认证token

## 关键发现（TapNow案例）

TapNow的auth存储在localStorage中：
```
refresh_token: "xxx.xxx.xxx"  (JWT格式)
device_id: "uuid"
user_id: "uuid"
canvas_id: "uuid" (从starter-tutorial-storage获取)
```

**注意**: auth token无法注入到agent的headless浏览器。
原因：`localStorage.setItem()` 在跨域/跨会话时会被浏览器安全策略阻止。

## 替代方案：让用户执行提取代码

既然无法注入token，就让用户在自己的浏览器执行提取代码：

```javascript
// 用户在自己浏览器Console执行
(function() {
  const nodes = document.querySelectorAll('.react-flow__node');
  const firstNode = nodes[0];
  const nodeContainer = firstNode?.querySelector('[class*="rounded-2xl"]');
  const nodeStyles = nodeContainer ? window.getComputedStyle(nodeContainer) : null;
  
  const result = {
    canvasClass: document.querySelector('.react-flow')?.className,
    nodeCount: nodes.length,
    nodeStyles: nodeStyles ? {
      backgroundColor: nodeStyles.getPropertyValue('background-color'),
      borderRadius: nodeStyles.getPropertyValue('border-radius'),
      backdropFilter: nodeStyles.getPropertyValue('backdrop-filter'),
      boxShadow: nodeStyles.getPropertyValue('box-shadow'),
      outline: nodeStyles.getPropertyValue('outline'),
      border: nodeStyles.getPropertyValue('border'),
      width: nodeStyles.getPropertyValue('width'),
      minHeight: nodeStyles.getPropertyValue('min-height'),
    } : null,
    nodeHTML: firstNode?.innerHTML?.substring(0, 3000)
  };
  
  console.log(JSON.stringify(result, null, 2));
})();
```

用户把输出结果发回给agent，agent分析并提取需要的样式值。

## Mac快捷键参考（给用户的）

| 操作 | 快捷键 |
|------|--------|
| 打开DevTools | `Cmd + Option + I` |
| 直接打开Console | `Cmd + Option + C` |
| 复制 | `Cmd + C` |
| 粘贴 | `Cmd + V` |
| 截图 | `Cmd + Shift + 4` |

**注意**: Mac没有F12键！很多用户不知道这一点。
