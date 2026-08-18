# TapNow邮箱登录验证流程

## 实测验证的登录流程（2026-07-05）

### Google OAuth登录
- **结果**: 被Google拦截，提示"此浏览器或应用可能不安全"
- **原因**: headless浏览器被Google识别为自动化工具
- **解决方案**: 不要尝试Google OAuth，改用邮箱登录

### 邮箱登录流程
1. 访问 https://app.tapnow.ai/auth-login
2. 输入邮箱地址 (如 xingandai0@gmail.com)
3. 勾选"同意服务条款、社区准则与隐私政策"
4. 点击"继续"按钮
5. TapNow发送验证邮件到用户邮箱
6. **用户去Gmail点击验证链接**（可能在垃圾邮件文件夹）
7. 验证完成后回到登录页面继续

### 自动化操作步骤
```javascript
// 1. 输入邮箱
browser_type(ref='@e11', text='xingandai0@gmail.com')

// 2. 勾选同意协议
browser_click(ref='@e12')  // checkbox

// 3. 如果弹出协议确认框，点击"同意并继续"
browser_click(ref='@e4')  // "同意并继续"按钮

// 4. 点击继续按钮
browser_click(ref='@e7')  // "继续"按钮
```

### 常见问题

**Q: 用户说没收到验证邮件**
A: 让用户检查垃圾邮件文件夹，或者重新发送验证邮件

**Q: 如何重新发送验证邮件**
A: 重复步骤1-4，TapNow会重新发送

**Q: 验证完成后如何继续**
A: 用户点击验证链接后，回到登录页面，此时应该已经登录成功

### 关键提醒
- **提前告诉用户**: "需要登录才能看到真实UI，落地页只有静态展示"
- **不要反复尝试Google OAuth**: 会被拦截，浪费时间
- **告诉用户去垃圾邮件文件夹找**: 验证邮件可能被过滤

### 🔴 Browserbase会话隔离（重要）

`browser_navigate` 使用的 Browserbase 会话与用户的真实浏览器**完全隔离**。

**这意味着**：用户在自己的浏览器中点击验证链接后，Browserbase会话**不会**获得登录状态。两者是完全独立的浏览器实例。

**正确的登录流程**：
1. 在 Browserbase 会话中完成**整个**登录流程（输入邮箱 → 发送验证 → 用户点击链接 → 回到同一 Browserbase 会话）
2. **或者**让用户从已登录的浏览器导出 session cookie，然后注入到 Browserbase 会话

**错误的做法**：
- ❌ 让用户在自己浏览器验证，然后期望 Browserbase 会话自动登录
- ❌ 反复刷新 Browserbase 会话的页面（不会生效）

**获取cookie的方法**（让用户操作）：
```javascript
// 在用户已登录的TapNow页面Console中执行
JSON.stringify({
  cookies: document.cookie,
  localStorage: Object.fromEntries(
    Object.entries(localStorage).filter(([k]) => 
      k.includes('token') || k.includes('auth') || k.includes('session') || k.includes('user')
    )
  )
})
```

**2026-07-05 实测**：用户在自己浏览器验证邮箱后，Browserbase会话仍显示登录页面。需要用户导出cookie或在同一Browserbase会话中完成验证。

## 与UI逆向的关系

登录成功后才能提取：
- 节点内的输入区域（PromptPanel）
- 模型选择器（下拉菜单）
- 参数设置（尺寸、步数等）
- 生成按钮、上传按钮
- 节点内部的真实结构

落地页只能提取：
- CSS变量
- 动画关键帧
- React Flow样式
- 节点HTML骨架（静态图片）
