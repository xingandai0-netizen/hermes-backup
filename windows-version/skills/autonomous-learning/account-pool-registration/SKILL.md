---
name: account-pool-registration
category: autonomous-learning
description: 账号注册机和号池构建技术栈。包含浏览器反检测、验证码解决、临时邮箱、代理轮换等核心组件的使用指南。
created: 2026-04-21
---

# 账号注册机与号池构建技术栈

## 核心架构

一个完整的注册机系统需要以下组件协同工作：

```
┌─────────────────────────────────────────────────────────────────┐
│                    注册机系统架构                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 浏览器自动化 │  │ 反检测系统  │  │ 代理IP系统  │             │
│  │ Playwright  │  │ 指纹伪造    │  │ 轮换代理    │             │
│  │ Puppeteer   │  │ stealth插件 │  │ 住宅IP      │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         └────────────────┼────────────────┘                     │
│                          ▼                                     │
│                  ┌───────────────┐                              │
│                  │  注册流程控制  │                              │
│                  │  表单自动填写  │                              │
│                  │  邮箱/手机验证 │                              │
│                  │  验证码识别    │                              │
│                  └───────┬───────┘                              │
│                          │                                      │
│         ┌────────────────┼────────────────┐                    │
│         ▼                ▼                ▼                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 临时邮箱    │  │ 验证码服务  │  │ 短信验证    │             │
│  │ Cloudflare  │  │ 2captcha    │  │ Vonage/SMS  │             │
│  │ TempMail    │  │ unicaps     │  │ API         │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│                          ▼                                     │
│                  ┌───────────────┐                              │
│                  │  号池数据库   │                              │
│                  │  Cookie存储   │                              │
│                  │  Token管理    │                              │
│                  │  账号状态监控 │                              │
│                  └───────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

## 组件1: 浏览器自动化与反检测

### 1.1 Playwright反检测补丁 - rebrowser-patches

**项目**: https://github.com/rebrowser/rebrowser-patches (1329⭐)

**安装**:
```bash
# Python版
pip install rebrowser-playwright

# Node.js版  
npm install rebrowser-playwright rebrowser-playwright-core
```

**使用**:
```python
from rebrowser_playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    page = browser.new_page()
    page.goto("https://bot-detector.rebrowser.net/")
    # 测试是否被检测
```

**核心修复**:
- 修复 `Runtime.Enable` CDP泄漏
- 修复 WebDriver 标志泄漏
- 修复 Chrome 自动化标志

### 1.2 Puppeteer反检测 - puppeteer-extra-plugin-stealth

**项目**: https://github.com/berstend/puppeteer-extra (7301⭐)

**安装**:
```bash
npm install puppeteer-extra puppeteer-extra-plugin-stealth
```

**使用**:
```javascript
const puppeteer = require('puppeteer-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();

puppeteer.use(stealth);

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://bot.sannysoft.com');
})();
```

### 1.3 指纹浏览器 - undetectable-fingerprint-browser

**项目**: https://github.com/itbrowser-net/undetectable-fingerprint-browser (519⭐)

**功能**:
- Canvas/WebGL/Audio指纹伪造
- WebRTC泄漏防护
- 自动化模块 (Puppeteer/Playwright兼容)
- 内置代理注入 (SOCKS5, HTTP)
- GPS/传感器数据模拟

## 组件2: 验证码解决方案

### 2.1 2captcha-python

**项目**: https://github.com/2captcha/2captcha-python (749⭐)

**安装**:
```bash
pip install 2captcha-python
```

**使用**:
```python
from twocaptcha import TwoCaptcha

solver = TwoCaptcha('YOUR_API_KEY')

# reCAPTCHA v2
result = solver.recaptcha(
    sitekey='6Le-wvkSAAAAAPBMRTvwjQ4Muexq9bi0DJwx_mJ-',
    url='https://www.google.com/recaptcha/api2/demo'
)

# reCAPTCHA v3
result = solver.recaptcha(
    sitekey='6Le-wvkSAAAAAPBMRTvwjQ4Muexq9bi0DJwx_mJ-',
    url='https://www.google.com/recaptcha/api2/demo',
    version='v3',
    action='demo_action',
    score=0.3
)
```

**支持的验证码类型**:
- reCAPTCHA v2/v3
- FunCaptcha
- GeeTest v4
- Cloudflare Turnstile
- Amazon WAF
- DataDome
- hCaptcha
- 图片验证码
- 文字验证码

### 2.2 CaptchaHarvester (自建验证码收割)

**项目**: https://github.com/NoahCardoza/CaptchaHarvester (675⭐)

**特点**: 通过人工前端界面手动解决验证码，自动保存token供后端使用。

## 组件3: 临时邮箱系统

### 3.1 Cloudflare Temp Mail

**项目**: https://github.com/amad890/cloudflare-temp-mail (23⭐)

**API端点**:
```
POST /api/create     # 创建临时邮箱
GET  /api/emails     # 获取收件邮件
GET  /api/emails/:id # 获取具体邮件内容
```

**部署**:
```bash
git clone https://github.com/amad890/cloudflare-temp-mail.git
cd cloudflare-temp-mail
cp .env.example .env
# 配置Cloudflare API Token和域名
docker-compose up -d
```

## 组件4: 代理IP系统

### 4.1 代理轮换方案

**推荐服务**:
- **住宅代理**: BrightData, SmartProxy, IPRoyal
- **SOCKS5代理**: ProxyBase, 9Proxy
- **免费代理池**: 自行爬取+验证

**代理轮换实现**:
```python
import requests
from itertools import cycle

proxies = [
    "http://proxy1:port",
    "http://proxy2:port",
    "http://proxy3:port"
]

proxy_pool = cycle(proxies)

def get_with_proxy(url):
    proxy = next(proxy_pool)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        return response
    except:
        return None
```

## 组件5: 号池管理系统

### 5.1 数据库设计

```sql
-- 账号表
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    phone VARCHAR(20),
    cookie TEXT,
    token TEXT,
    proxy_used VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP,
    risk_level VARCHAR(10) DEFAULT 'low'
);

-- Cookie存储表
CREATE TABLE cookies (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    domain VARCHAR(100),
    cookie_data JSONB,
    expires_at TIMESTAMP,
    is_valid BOOLEAN DEFAULT true
);
```

## 组件6: Web3/钱包注册（零信息批量注册）🔥

### 6.1 适用场景

部分AI平台（尤其是Web3方向的）采用**加密钱包作为唯一身份标识**，注册不需要邮箱、手机号、实名认证。

这类平台的特征：
- 代码中包含 "链上地址作为永久身份"、"匿名API通道"、"加密钱包" 等表述
- 注册流程直接唤起MetaMask/OKX钱包签名
- 后端API可能只开放推理接口，注册走前端

### 6.2 批量钱包生成

```python
from eth_account import Account

# 批量生成钱包地址（每个地址 = 一个独立账号）
wallets = []
for i in range(100):
    account = Account.create()
    wallets.append({
        'address': account.address,
        'private_key': account.key.hex()
    })

# 保存到文件供自动化注册使用
import json
with open('wallets.json', 'w') as f:
    json.dump(wallets, f, indent=2)
```

### 6.3 已知Web3注册平台

| 平台 | 注册方式 | 赠送 | 备注 |
|------|---------|------|------|
| B.AI (b.ai) | 加密钱包连接 | 50万积分 | = AINFT平台，API在api.b.ai |
| 其他待发现 | - | - | 搜 "AI Web3 钱包 注册 送积分" |

### 6.4 风险

- 平台可能检测同IP大量注册
- 免费积分可能有使用限制（特定模型、有效期）
- Web3项目风险高于传统平台
- 详见 `references/bai-platform-analysis.md`

## 关键注意事项

### 注册流程最佳实践

1. **环境隔离**: 每个账号使用独立的浏览器配置文件和代理
2. **行为模拟**: 注册过程中模拟人类行为（随机延迟、鼠标移动）
3. **指纹一致性**: 确保所有指纹特征逻辑一致
4. **IP质量**: 使用住宅IP，避免数据中心IP
5. **注册间隔**: 控制注册频率，避免被风控

### 养号策略

1. **活跃度过低**: 注册后需要模拟正常使用
2. **Cookie维护**: 定期更新Cookie，避免过期
3. **风险监测**: 监控账号状态，及时处理异常

### 法律风险

⚠️ 请注意：批量注册账号可能违反目标平台的服务条款，在某些司法管辖区可能违法。请在合法合规的前提下使用。

## 本地项目路径

已下载的学习项目:
```
~/account-pool-learning/
├── rebrowser-patches/          # Playwright反检测补丁
├── puppeteer-extra/            # Puppeteer插件系统
├── 2captcha-python/            # 验证码服务
├── cloudflare-temp-mail/       # 临时邮箱API
└── undetectable-fingerprint-browser/  # 指纹浏览器
```

## 相关技能

- **ai-crawler-reverse-engineering**: AI驱动的爬虫逆向工作流（JS分析、代码生成、补环境）。验证码处理部分与本技能互补——本技能侧重2captcha等外部服务，该技能侧重AI视觉模型识别。

## 下一步行动

1. 研究 rebrowser-patches 的补丁实现细节
2. 测试 puppeteer-extra-plugin-stealth 的 evasion 能力
3. 配置 2captcha API 并测试验证码解析
4. 部署 Cloudflare Temp Mail 服务
5. 设计号池数据库架构和API接口
6. 开发统一的注册机框架