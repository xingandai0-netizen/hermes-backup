# 案例分析: 982博彩站安全审计 (2026-08)

## 目标
- URL: b1qtfhjzt5p.982827.com/m/#/home
- 品牌: 澳门新葡京
- 主题标识: "uu"

## 技术栈
| 组件 | 技术 | 版本/备注 |
|------|------|----------|
| 前端框架 | Vue 3 + Vite | v1.5.13.315 |
| UI库 | Vant (移动端) | - |
| HTTP库 | Axios | - |
| jQuery | 1.10.2 | CVE-2019-11358 |
| CAPTCHA | Geetest v4 (极验) | captchaId: 26a8228fcfee3424d7ea11653a8e5783 |
| 后端 | PHP + Nginx | 确认: .php文件返回403 |
| 路由 | Hash模式 | /m/#/home |
| 站点类型 | credit (信用盘) | - |

## API加密算法
**反转字符串 + Base64解码**
```python
import base64, json
def decrypt(encoded):
    reversed_str = encoded[::-1]
    return json.loads(base64.b64decode(reversed_str).decode('utf-8'))
```

验证: CheckSession返回明文JSON `{"state":"error","message":"温馨提示(60323):登录超时。"}`，其他接口用此算法解密后得到相同格式。

## 认证机制
- Token头: `Token: {"USER_SESSION_KEY":"xxx","LOGIN_USER_KEY":"xxx"}`
- 存储: localStorage
- 设备指纹: cuid, browserId, dudibt, dudibr, dudit, dudir (cookies)
- 密码编码: MD5 (无盐)

## 注册流程
1. 表单: mobile + password(MD5) + confirmPassword + realName + msgCode
2. 短信验证: Geetest滑块 → SendSmsCode
3. 提交: POST api/User/Register (form-urlencoded)
4. 安全问题列表: 10个问题（车牌照、初中同桌等）

## 发现的漏洞
| 严重度 | 漏洞 | 状态 |
|--------|------|------|
| 高 | jQuery 1.10.2 原型污染 (CVE-2019-11358) | 已确认可利用 |
| 高 | API响应加密可逆 (反转+Base64) | 已确认 |
| 高 | 网站配置未授权泄露 | 已确认 |
| 中 | 无CSP/X-Frame-Options/HSTS | 已确认 |
| 中 | document.write协议绕过 | 已确认代码存在 |
| 中 | 密码仅MD5无盐 | 已确认 |
| 中 | Geetest captchaId硬编码 | 已确认 |
| 低 | jQuery版本泄露 | 已确认 |
| 低 | PHP后端泄露 | 已确认 |

## 未发现的漏洞
- 无SQL注入（输入已参数化）
- 无IDOR（session认证，不接受id参数）
- 管理后台不暴露（admin子域名不存在）
- 密码重置已关闭
- SMS登录已关闭

## 提取的API端点 (42个)
详见上方SKILL.md Phase 2部分。

## 敏感信息泄露
- 客服系统: uu982zaixiankf.jhg81lkj68iu96.com/chat/402207265
- 投诉邮箱: gfts982@163.com
- APP下载: 多个子域名 (appxz982.com)
- Talkblink客服: talkblink.co
- 安全问题: 10个完整问题列表
- 代理系统: AGENT_MODE=1 (已启用)
