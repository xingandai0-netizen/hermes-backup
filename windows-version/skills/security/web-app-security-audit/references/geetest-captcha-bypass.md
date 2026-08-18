# Geetest CAPTCHA绕过

## Geetest v4架构
- captchaId硬编码在前端JS中
- 滑块验证，结果存储在 window.captchaObj_result
- 验证结果: gen_time, lot_number, captcha_output, pass_token

## 硬编码的captchaId
```javascript
// 在lib.js中
captchaId: "26a8228fcfee3424d7ea11653a8e5783"  // 生产环境
// 测试环境: "c157dc324815a110de124e910f166349"
```

## 验证结果格式
```javascript
{
  GeeVer: 40,
  userkey: captchaObj_result.gen_time,        // 时间戳
  geetest_challenge: captchaObj_result.lot_number,  // 随机数
  geetest_validate: captchaObj_result.captcha_output, // 验证结果
  geetest_seccode: captchaObj_result.pass_token,    // 通过令牌
}
```

## 绕过方法

### 方法1: 第三方打码平台
- 2Captcha: ~$0.003/次
- AntiCaptcha: ~$0.002/次
- CapSolver: ~$0.001/次

API调用:
```python
import requests

# 提交打码任务
resp = requests.post('https://2captcha.com/in.php', data={
    'key': 'YOUR_API_KEY',
    'method': 'geetest_v4',
    'captcha_id': '26a8228fcfee3424d7ea11653a8e5783',
    'pageurl': 'https://target.com/m/#/home',
    'api_server': 'api.geetest.com',
})
task_id = resp.text.split('|')[1]

# 获取结果
result = requests.get(f'https://2captcha.com/res.php?key=YOUR_API_KEY&action=get&id={task_id}')
```

### 方法2: 浏览器自动化
```python
# 用Playwright/Selenium模拟滑块
# 缺点: 容易被检测，成功率低
```

### 方法3: 直接伪造验证结果
如果captchaId已知，理论上可以构造验证结果。但Geetest v4的签名算法较复杂，不推荐。

## 检测captchaId
```javascript
// 方法1: 搜索lib.js
fetch('/m/static/lib.js').then(r=>r.text()).then(t=>{
  const match = t.match(/captchaId:\s*"([^"]+)"/);
  console.log(match?.[1]);
});

// 方法2: 搜索所有JS
// 搜索 "captchaId" 或 "geetest" 或 "gt.js"
```

## 注意事项
1. Geetest有频率限制，批量请求会被封IP
2. 打码平台需要付费
3. 部分站点会检测打码平台的IP
4. captchaId可能随域名变化
5. 测试环境和生产环境的captchaId不同
