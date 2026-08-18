# botion CAPTCHA 分析

## 概述

botion是赌博/诈骗站常用的自托管验证码系统。与极验(Geetest)不同，botion完全自托管，验证码图片和验证API都在目标服务器上。重度混淆，有AI检测层。

## 三种验证码类型

### 1. slide (滑块拼图)
- 背景图 + 缺口 + 滑块
- 需要拖动滑块到缺口位置
- 缺口位置可通过图像分析(边缘检测/亮度差异)估算
- 验证参数需要加密，不能直接提交坐标

### 2. word (文字点击)
- 背景图上有多个中文字符
- 题目图片显示需要点击的字符
- 需要按顺序点击正确的字符
- 字符位置需要图像识别

### 3. nine (九宫格)
- 3x3网格，需要点击特定格子
- 题目图片显示需要点击的格子位置

## API端点

```
# 加载验证码
GET /bcaptcha-botion/load?captcha_id={id}&challenge={uuid}&client_type=web&risk_type=slide&lang=zho

响应:
{
  "status": "success",
  "data": {
    "lot_number": "唯一标识",
    "captcha_type": "slide|word|nine",
    "imgs": "图片路径",
    "ques": ["题目图片路径"],
    "nine_nums": 3
  }
}

# 验证
POST /bcaptcha-botion/verify
Content-Type: application/json

{
  "captcha_id": "固定值",
  "lot_number": "从load获取",
  "captcha_type": "slide|word|nine",
  "points": [{"x": 100, "y": 100}]  // 加密后的坐标
}

响应:
- 成功: {"status": "success", "data": {"validate": "token值"}}
- 失败: {"status": "error", "code": "-50002", "msg": "param decrypt error"}
- 过期: {"status": "error", "code": "-50302", "msg": "not lot_number"}
```

## 图片URL格式

```
# 背景图
https://TARGET/static-botion/pictures/v4_pic/slide_2024_09_02/{hash}/bg/{image_hash}.png

# 文字点击题目
https://TARGET/static-botion/nerualpic/v4_pic/click_2021_06_16/word/{hash}.jpg

# 九宫格题目
https://TARGET/static-botion/nerualpic/v4_pic/nine_prompt/{hash}.png
```

## 绕过尝试记录（全部失败）

### ❌ 直接伪造verify请求
- 返回 `param decrypt error` - 参数需要加密
- 加密方式未知，可能用RSA或AES

### ❌ 空/假validate值
- 返回 `param decrypt error`

### ❌ 滑块位置暴力枚举
- 每次验证码刷新后图片不同
- 需要图像分析找到正确位置
- 即使找到位置，verify参数仍需加密

### ❌ JavaScript合成鼠标事件
- `dispatchEvent(new MouseEvent(...))` 不会触发验证
- botion监听的是真实OS级别鼠标事件
- 需要用computer_use工具的真实鼠标操作

### ❌ 滑块图像分析+JS拖拽
- 用PIL分析缺口位置可行（scripts/captcha-gap-detect.py）
- 但JS拖拽不触发验证逻辑
- 即使位置正确，verify参数仍需加密

### ❌ 拦截fetch/XHR响应
- 尝试拦截fetch返回假success响应
- CAPTCHA内部不依赖fetch返回值判断成功
- 验证逻辑在CAPTCHA JS内部，拦截响应无效

### ❌ 直接调用Vue Store登录函数
- Vue3 Pinia store有 `act_CheckLoginFirstStep`, `fetchLoginState` 等函数
- 但这些函数内部会读取CAPTCHA验证状态
- 缺少captcha_validate参数时返回"系统异常"(5011111)
- 函数源码被Pinia wrapper包装，看不到实际实现

### ❌ 调用CAPTCHA对象的onSuccess
- `window._captchaObj_` 存在，有 `onSuccess`, `getValidate`, `showBox`, `reset` 等方法
- 调用 `onSuccess({validate: "fake"})` 不会更新内部状态
- `getValidate()` 在未验证时返回null
- CAPTCHA对象属性名被混淆: `$_BAIe`, `$_BAJq`

### ❌ 查找CAPTCHA回调函数
- 加载脚本URL中有 `callback=botion_{timestamp}`
- 但回调函数在脚本加载后被删除/不可访问
- `window[callbackName]` 返回undefined

### ✅ 可行方案
1. **用户手动过验证码** - 让用户在浏览器中手动完成一次验证码
2. **抓取验证成功后的Token** - 从localStorage的`user`键中提取`loginState.token`
3. **用Token调用登录API** - 绕过验证码直接登录
4. **computer_use真实鼠标** - 用computer_use工具模拟真实鼠标操作（需要先截图分析缺口位置）
5. **Safari osascript** - 用户手动在Safari中登录，然后用osascript提取Token并通过Safari的JS引擎执行所有认证后的测试。详见`references/safari-auth-testing.md`。这是最可靠的方案，因为Token绑定浏览器会话。

## botion CAPTCHA内部对象结构

```javascript
// 全局变量
window._captchaObj_  // CAPTCHA实例
window.Botion        // CAPTCHA类
window.initBotion    // 初始化函数

// CAPTCHA实例方法
_captchaObj_.onSuccess(callback)  // 验证成功回调
_captchaObj_.onFail(callback)     // 验证失败回调
_captchaObj_.onReady(callback)    // CAPTCHA就绪回调
_captchaObj_.onClose(callback)    // CAPTCHA关闭回调
_captchaObj_.getValidate()        // 获取验证token（未验证时返回null）
_captchaObj_.showBox()            // 显示CAPTCHA弹窗
_captchaObj_.showCaptcha()        // 显示CAPTCHA
_captchaObj_.reset()              // 重置CAPTCHA
_captchaObj_.destroy()            // 销毁CAPTCHA
_captchaObj_.uploadExtraData()    // 上传额外数据

// 混淆的内部属性（不可读）
_captchaObj_.$_BAIe  // number
_captchaObj_.$_BAJq  // boolean

// DOM元素命名规则（hash为随机后缀）
// botion_{hash} - CAPTCHA容器
// botion_box_{hash} - 弹窗
// botion_btn_{hash} - 滑块按钮
// botion_bg_{hash} - 背景图
// botion_slice_{hash} - 缺口拼图
// botion_slider_{hash} - 滑块轨道
// botion_{0-8}_{hash} - 九宫格/文字点击的9个格子
// botion_ghost_{n}_{hash} - 选中状态
// botion_ai_detect_{hash} - AI检测层
// botion_close_{hash} - 关闭按钮
// botion_refresh_{hash} - 刷新按钮
```

## Vue3 Pinia Store登录流程

```javascript
// 获取Pinia store
const app = document.querySelector('#app')?.__vue_app__;
const pinia = app?.config?.globalProperties?.$pinia;
const userStore = pinia?._s?.get('user');

// 登录相关方法
userStore.act_CheckLoginFirstStep()  // 第一步登录（需要CAPTCHA token）
userStore.fetchLoginState()          // 获取登录状态
userStore.fetchUserInfo()            // 获取用户信息
userStore.act_Register()             // 注册
userStore.logout()                   // 登出

// 登录表单数据
userStore.formData.account   // 手机号
userStore.formData.password  // 密码

// 登录状态
userStore.loginState.state       // "success" | "error"
userStore.loginState.token       // Token字符串
userStore.loginState.sessionKey  // Session Key

// localStorage存储
localStorage.getItem('user')  // JSON字符串，包含loginState、formData等
```

## 与极验(Geetest)的区别

| 特性 | botion | Geetest |
|------|--------|---------|
| 托管方式 | 自托管 | 云端 |
| API域名 | 同目标域名 | api.geetest.com |
| 验证码类型 | slide/word/nine | slide/click |
| 参数加密 | 是 | 是 |
| 绕过难度 | 高 | 中(有开源工具) |
| 识别方式 | 自研 | 广泛研究 |
| AI检测 | 有(ai_detect层) | 无 |
| 混淆程度 | 高(属性名混淆) | 中 |

## 实战案例: 982827.com (2026-08)

- captcha_id: 26a8228fcfee3424d7ea11653a8e5783
- 验证码类型: 随机切换(slide/word/nine)
- 刷新间隔: ~30秒
- 图片URL: /static-botion/pictures/v4_pic/...
- 验证API: /bcaptcha-botion/verify
- 结果: 无法自动绕过，需要手动过验证码
- b1qtfhjzt5p.982827.com 已下线(502)
- f5phwmack3a.982827.com 活跃，使用相同CAPTCHA
- **Session Token绑定浏览器**: 用户手动登录后，Token从Python/curl发起请求返回"会话已过期"。必须通过Safari的JS引擎执行所有认证后的测试。
- **解决方案**: 用户手动在Safari登录 → osascript提取Token → 通过Safari的fetch执行所有API测试
