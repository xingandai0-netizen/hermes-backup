# 赌博诈骗站注册参数模式

## 常见注册请求格式

### ASP.NET MVC 风格 (最常见)
```
POST /api/User/Register?t={timestamp}&envvv=1
Content-Type: application/x-www-form-urlencoded

mobile={手机号}
password={MD5(密码)}
checkpwd={明文密码}  ← 密码泄露!
ATTR1={明文密码}     ← 密码泄露!
ATTR2=
USER_TYPE_CD=credit
mob=1
INVITE_CODE=
REAL_NAME={真实姓名}
LOGIN_ACCOUNT=
WECHAT=
QQ=
EMAIL=
guid=
smsCode={短信验证码}
login_www={站点URL}
device_type=wap
client_id=
client_cd=ios_web
jmptwo=1
device_no={设备指纹MD5}
version={前端版本号}
```

### 密码处理
- `password` = MD5(明文密码)，32位小写hex
- `checkpwd` = 明文密码 ⚠️
- `ATTR1` = 明文密码 ⚠️
- 服务端可能只校验 `password` 字段，`checkpwd`/`ATTR1` 是冗余泄露

### 短信验证码
- 空验证码 → 错误码 5011111 "系统异常"
- 错误/过期验证码 → 错误码 103251 "短信验证码已失效"
- 频繁请求 → 错误码 10999 "操作太频繁"
- 验证码通常6位数字，有效期2-5分钟
- 部分站点验证码场景配置可通过 `/api/Api/GetVerifyCodeNew` 获取
- 验证码配置返回格式: `{"SceneUserLogin":1, "SceneAgentPostUser":2, "SceneFindUserPwd":-1, "SceneUserRegister":2, ...}`
  - 值=1: 开启验证码
  - 值=2: 可能可绕过
  - 值=-1: 关闭

### 设备指纹
- `device_no` 通常是浏览器指纹的MD5
- 可以固定使用一个随机值
- 部分站点用此做限流，换device_no可绕过频率限制

## 登录请求格式

### ASP.NET MVC 风格
```
POST /api/User/CheckLoginFirstStep?t={timestamp}&envvv=1
Content-Type: application/x-www-form-urlencoded

mobile={手机号}
password={MD5(密码)}
device_no={设备指纹}
version={前端版本号}
client_cd=ios_web
device_type=wap
login_www={站点URL}
```

**注意**: 登录通常需要验证码(botion/极验)，直接调API会被拦截。
- 无验证码 → "系统异常"(5011111)
- 假验证码token → "param decrypt error"
- 需要用户手动过验证码后抓取Token

### 登录相关API
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/User/CheckLoginFirstStep | 登录第一步 | ❌(需验证码) |
| /api/User/GetUserLoginKey | 获取登录密钥 | ❌(需先登录) |
| /api/User/CheckSession | 检查会话状态 | ✅ |
| /api/User/OutLogin | 退出登录 | ✅ |

## 验证码系统

### botion CAPTCHA (自托管)
- 赌博站最常用
- 3种类型: slide(滑块), word(文字点击), nine(九宫格)
- API: /bcaptcha-botion/load + /bcaptcha-botion/verify
- 参数加密，无法直接伪造
- 详见 `botion-captcha-analysis.md`

### 极验 Geetest (云端)
- 更正规的站点使用
- API: api.geetest.com
- 有开源绕过工具

## 关联API端点

### 注册/登录相关
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/User/Register | 注册 | ❌ |
| /api/User/SendSmsCode | 发送验证码 | ❌ |
| /api/User/GetAuthCode | 获取图形验证码 | ❌ |
| /api/Api/GetVerifyCodeNew | 验证码配置 | ❌ |
| /api/User/RegProperties | 注册字段配置 | ❌ |
| /api/User/RegQuestions | 安全问题列表 | ❌ |

### 消息系统IDOR
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/User/GetMessageList | 所有系统消息 | ❌ 读 |
| /api/User/GetNoReadMessageCount | 未读消息数 | ❌ 读 |
| /api/User/UpdMessageState?MsgID= | 标记已读 | ✅ 写 |
| /api/User/DelMessage?detail_id= | 删除消息 | ✅ 写 |

### 推荐/返佣系统
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/userfan/TotolSelfFanAMT | 推荐总额 | ❌ |
| /api/userfan/UserFanRate | 返佣比例 | ❌ |
| /api/userfan/UserFanInfo | 推荐详情 | ❌ |
| /api/userfan/FanReceive | 领取返佣 | ❌ |

### 活动系统
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/Act/GetActTasksConfigList | 任务列表 | ❌ |
| /api/Act/GetActVsList | 活动列表 | ❌ |
| /api/Act/GetActRedEnvelopesConfig | 红包配置 | ❌ |
| /api/Act/GetActWebActivityList | 活动类型 | ❌ |
| /api/Act/GetActSlyderAdventuresConfig | 滑块活动配置 | ❌ |

### 游戏/账户系统
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/Agent/GetGameList | 游戏列表 | ❌ |
| /api/User/GetAccount | 账户结构(余额0) | ❌ |
| /api/Web/GetAccountList | 游戏账户代码 | ❌ |
| /api/Web/GetMobileList | 彩票列表 | ❌ |
| /api/YuBao/GetTrsConfig | 余额宝配置 | ❌ |

### 配置系统
| 端点 | 用途 | 认证 |
|------|------|------|
| /api/Web/GetAllBasicWebsiteConfigurationNew | 网站配置 | ❌ |
| /api/Api/GetCldSiteConfig | 皮肤/支付配置 | ❌ |
| /api/Web/GetPhoneCallBackConfig | 回调配置 | ❌ |
| /api/Web/GetNavRecharge | 充值比例 | ❌ |
| /api/User/GetVipUrl | VIP URL | ❌ |

## 注册绕过尝试

1. **空验证码**: 通常返回"系统异常"，不通过
2. **固定验证码(000000/123456)**: 返回"已失效"
3. **验证码爆破**: 6位=100万种，需高频请求，有频率限制
4. **跳过验证码字段**: 可能返回不同错误，暴露后端逻辑
5. **换手机号重试**: 每个手机号有独立的验证码

## 域名轮换特征

- 赌博站经常换域名（打一枪换一个）
- SSL证书SAN字段揭示关联域名网络
- 同一证书覆盖 *.982827.com, *.982559.com, *.982952.com 等
- 域名注册时间通常<3个月
- CDN: Cloudflare（隐藏真实IP）
- 服务器: nginx/openresty

## 实战案例: 982827.com (2026-08)

### 基础设施
- 前端: Vue3 + jQuery 1.10.2
- 后端: nginx + ASP.NET MVC风格API
- 版本: v1.5.13.315
- 加密: 反转+Base64
- SSL: 通配符证书覆盖10+域名
- 验证码: botion (slide/word/nine随机切换)

### 确认的漏洞
1. jQuery原型污染 (CVE-2019-11358)
2. API响应加密可逆 (反转+Base64)
3. 安全头全部缺失
4. 密码MD5无盐 + 明文传输(checkpwd/ATTR1)
5. document.write协议绕过
6. 20+个未认证API端点泄露敏感数据
7. 消息系统IDOR (读操作无需认证)
8. 账户结构/游戏列表/推荐系统泄露

### 无法测试的
- SQL注入: sqlmap SSL连接失败
- 竞态条件: 需要认证
- 支付回调伪造: 端点404(服务端路由)
- 注册绕过: 短信验证码有效
- 登录绕过: botion验证码无法自动破解
