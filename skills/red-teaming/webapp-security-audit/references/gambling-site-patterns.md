# 赌博诈骗站技术模式库

基于 982827.com 系列站点（澳门新葡京）的实战分析 (2026-08)。

## 已知站点指纹

| 项目 | 982827.com |
|------|------------|
| 前端 | Vue3 + Pinia + Vite + jQuery 1.10.2 |
| 后端 | nginx/openresty (ASP.NET MVC风格API) |
| 验证码 | botion CAPTCHA (自托管) |
| 加密 | 反转+Base64 |
| Token | JSON {USER_SESSION_KEY, LOGIN_USER_KEY}，绑定浏览器 |
| POST格式 | FormData (multipart/form-data) |
| 域名轮换 | b1qtfhjzt5p → f5phwmack3a |
| SSL证书 | 通配符覆盖10+域名 |
| APP下载 | mn4l411f.appxz982.com, gstpk413.appxz982.com |
| 客服 | uu982zaixiankf.jhg81lkj68iu96.com/chat/402207265 |
| 代理TB | wanlitalk.vip/co/net, TB号982982 |
| 投诉邮箱 | gfts982@163.com |
| 漏洞 | 15个（高危5/中危7/低危3） |

## 基础设施模式

### 域名轮换
- 主域名频繁更换（短命站，注册2-6个月）
- 通过302重定向跳转到新子域
- 例: 41834.me → f5phwmack3a.982827.com
- 子域名格式: 随机字符串.主域名 (如 b1qtfhjzt5p, f5phwmack3a)

### SSL证书
- 通配符证书覆盖多个关联域名
- SAN字段是OSINT金矿：一张证书覆盖10+域名 = 同一团伙
- 例: *.982827.com 的证书同时覆盖 *.982559.com, *.982952.com, *.982875.com 等
- 证书签发时间短（6个月），频繁更换

### CDN/真实IP
- Cloudflare隐藏真实IP
- nmap扫描到的IP可能是CDN节点
- 真实IP需要通过历史DNS/子域名/邮件头等获取

### 服务器
- nginx / openresty（最常见）
- 很少用Apache/IIS

## 前端技术栈

### 典型组合
- **Vue3 + jQuery 1.x** — SPA + 老旧jQuery（原型污染）
- **版本号格式**: v1.5.13.315（主版本.功能.修复.构建号）
- **移动端优先**: 大量 meta viewport/screen-orientation 标签

### JS文件结构
```
/m/static/
├── jquery-1.10.2.min.js        # 老旧jQuery
├── lib.js                       # 第三方库
├── gt.js                        # 极验验证码
├── assets/js/
│   ├── polyfills-*.js           # Polyfills
│   ├── index-*.js               # 主入口（含所有API路径）
│   └── polyfills-legacy-*.js    # 兼容性
```

## 后端API模式

### 路由风格
- ASP.NET MVC风格: `/api/Controller/Action`
- 常见Controller: Web, User, Pay, Act, Agent, YuBao, Api, shop, userfan, Spt

### 响应加密
- **反转+Base64** — 最常见
- 算法: `json.loads(base64.b64decode(response_text[::-1]))`
- 所有API响应都加密，但解密方式公开

### 认证机制
- Token存储在localStorage的`user`键中
- **APPEND_HEADER格式**（从`userInfo.APPEND_HEADER`获取）:
  ```
  uuv-user-loginkey: {LOGIN_USER_KEY}
  uuv-user-session-{USER_ID}: {SESSION_KEY}
  platform-ident: uu
  ```
- **不是** JSON格式的`Token: {...}` header
- userId从`userInfo.ID`获取（如4797147）
- **Session绑定浏览器**: Token从Python/curl发起请求返回"会话已过期"，必须通过Safari的JS引擎执行
- 会话验证有效，伪造Token会被拒绝
- **提现密码(DRAW_PASSWORD)**: 转账/提现需要独立的提现密码，与登录密码不同。用户未设置时返回NB103539错误

### 无需认证的API（信息泄露金矿）
```
# 网站配置
/api/Web/GetAllBasicWebsiteConfigurationNew  # 客服URL、邮箱、下载链接
/api/Web/GetAccountList                       # 游戏账户列表(50+个)
/api/Web/GetMenuList                          # 完整菜单HTML
/api/Web/GetMobileList                        # 彩票游戏列表
/api/Web/GetPhoneCallBackConfig               # 电话回拨配置
/api/Web/GetNavRecharge                       # 充值比例
/api/Web/GetWebPrefeClick                     # 点击计数器

# 注册相关
/api/User/RegProperties                       # 注册字段配置
/api/User/RegQuestions                        # 安全问题列表(10个)
/api/User/GetAgentMode                        # 代理模式配置

# 消息系统 (IDOR)
/api/User/GetMessageList                      # 所有系统消息 ⭐
/api/User/GetNoReadMessageCount               # 未读消息数 ⭐

# 游戏/代理
/api/Agent/GetGameList                        # 完整游戏列表
/api/Agent/GetFundChgDtlList                  # 需认证

# 推荐/返佣
/api/userfan/TotolSelfFanAMT                  # 推荐总额
/api/userfan/UserFanRate                      # 返佣比例
/api/userfan/UserFanInfo                      # 推荐详情

# 活动
/api/Act/GetActTasksConfigList                # 任务配置
/api/Act/GetActVsList                         # 活动列表
/api/Act/GetActRedEnvelopesConfig             # 红包配置
/api/Act/GetActWebActivityList                # 活动类型

# 验证码配置
/api/Api/GetVerifyCodeNew                     # 验证码场景配置
/api/Api/GetCldSiteConfig                     # 站点配置

# 余额宝
/api/YuBao/GetTrsConfig                       # 转账配置
```

### 支付系统
- 支付回调端点: /api/Pay/CallBack, /api/Pay/Notify, /api/Pay/Return
- 这些通常是服务端路由，前端API层返回404
- 实际回调由支付网关直接调用后端

### 注册流程
- 注册端点: /api/User/Register
- 需要: 手机号、真实姓名、短信验证码、密码(MD5)、安全问题
- 参数名不统一（大小写、下划线混合），需通过浏览器抓包确认
- **密码明文泄露**: `checkpwd`和`ATTR1`字段发送明文密码
- **短信验证码**: 有效期内可被爆破(6位数字)，但有频率限制
- **验证码配置**: `/api/Api/GetVerifyCodeNew` 泄露哪些场景需要验证码
- 详细参数格式见 `references/gambling-site-registration.md`

### nuclei扫描结果
- 5536模板扫描，0匹配
- 原因: 自研框架，无标准CMS/CVE漏洞
- 需要手工测试业务逻辑漏洞

### 认证后API测试结果 (2026-08, 用户4797147)
- ✅ GetUserInfo: 返回完整用户信息(ID, 用户名, 代理状态, 上级代理)
- ✅ GetAccount: 返回50+个游戏钱包(余额全0)
- ✅ GetOrderList_New: 返回订单列表(空)
- ✅ GetTransList: 返回交易列表(空)
- ✅ GetLotterList: 返回彩票列表(空)
- ✅ shop/GetShopIndex: 返回商城数据
- ✅ shop/GetMyBalance: 返回钱包余额=0
- ✅ YuBao/GetTrsOrderDetail: 返回交易记录(空)
- ❌ GetUserbetRpt: 系统异常(60352)
- ❌ Agent/GetFundChgDtlList: 需要查询金额参数
- ❌ TransferOperate: 使用password字段返回NB103539，但使用正确的FormData字段(transfer_amt/OUT_INT_IDENT_CD/IN_INT_IDENT_CD)时不需要密码——仅受余额限制 ⭐高危漏洞
- ❌ UpdateUserInfo: 404(端点不存在)
- SQL注入: SLEEP(3)无延迟效果，确认不可注入
- IDOR: ?id=参数被忽略，始终返回当前用户数据
- 竞态条件: 无法测试(需要提现密码)

## 代理体系
- 12级代理，佣金20%-75%
- 有效会员门槛: 5-50人
- 有效投注门槛: 1元-5000万+
- TB聊天软件: wanlitalk.vip/co/net
- 代理TB号: 982982

## 游戏平台
50+个游戏平台账户，包括:
- 真人: AG, BG, DG, BB, OG, WM, DB
- 电子: PT, PG, XG, PP, MG, CQ9, JDB, MW, HB, SG, KA, YGG 等
- 体育: 皇冠, 三升, 沙巴, IM, FB, 熊猫
- 电竞: IM, 雷火, DB
- 棋牌: 开元, 天游, 乐游
- 彩票: 香港六合彩

## 防御评估
- Token验证有效（无法伪造会话）
- 但20+个API完全不需要认证
- 消息系统读操作不需要认证（IDOR）
- 写操作（删除/修改）需要认证
- nuclei 5536模板0匹配（自研框架无标准CVE）
- **转账API无密码保护** — 使用正确参数名时不需要提现密码 ⭐

## 新账号限制
新注册且未充值的账号，以下API全部返回404（端点不存在，不是空数据）：
- 签到奖励 (ActSignIn, ActSignUp)
- 活动奖励 (所有活动页面)
- VIP奖励 (GetVipBonus)
- 代理佣金 (GetCommission)
- 免费奖金 (GetFreeBonus, GetActHandselConfig)
- 新用户奖励 (GetActNewUserBonus)
- 邀请奖励 (GetActInviteBonus)
- 红包雨 (GetActHongbaoyu)
- 转盘抽奖 (GetActRotary)
- 充值/支付 (Recharge/Apply, Pay/GetPayChannel)
- 试玩 (GeTrialUrl, GetTrialBalance)
- 任务奖励 (GetActTasksConfigList返回空数组)

**结论**: 赌博站对新账号的安全限制非常严格，所有奖励/活动API在首次充值前都不可用。测试资金相关漏洞需要已充值账号。
