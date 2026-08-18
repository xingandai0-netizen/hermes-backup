---
name: crypto-operations
description: |
  加密货币钱包管理、交易所操作、Gas费优化、链上查询的实战技能。
  覆盖OKX/币安安装配置、imToken/MetaMask钱包、Tron/ETH链上操作、
  Gas费机制与优化、资金费率套利等。触发：加密货币、钱包、交易所、
  Gas费、USDT转账、链上查询、套利、OKX、imToken、MetaMask。
version: 1.0
platforms: [macOS, linux]
metadata:
  hermes:
    tags: [crypto, defi, wallet, tron, ethereum, okx, gas]
    category: security
---

# Crypto Operations — 加密货币实战操作

## 关键安全规则

### ⚠️ 钱包插件安全
- **imToken没有官方Chrome浏览器插件** — 官方确认仅提供手机App
- Chrome商店里所有声称是imToken的插件全部是**恶意钓鱼工具**
- 2026年3月慢雾安全团队已发安全警报（socket.dev也确认）
- 类似地，任何声称是知名钱包的浏览器插件都要警惕
- **只从官方渠道下载钱包App**

### 助记词/私钥安全
- 绝不在任何网站、插件、对话框中输入助记词
- 公开地址可以分享，助记词/私钥绝对不能给任何人
- 钱包地址可以用来查询余额，不需要任何权限

## OKX桌面端安装 (macOS)

### 下载
- 官方下载页：https://www.okx.com/download
- 直接下载链接：https://static.okx.com/upgradeapp/OKX.dmg
- 当前版本约196MB，universal版支持Intel和Apple Silicon

### 安装流程
```bash
# 1. 下载
curl -L -o ~/Downloads/OKX.dmg "https://static.okx.com/upgradeapp/OKX.dmg"

# 2. 挂载DMG（需要接受许可证，用yes自动确认）
yes | hdiutil attach ~/Downloads/OKX.dmg -nobrowse

# 3. 复制到桌面和Applications
cp -R "/Volumes/OKX */OKX.app" ~/Desktop/
cp -R "/Volumes/OKX */OKX.app" /Applications/

# 4. 卸载DMG
hdiutil detach "/Volumes/OKX *"
```

### 坑点
- DMG会弹出许可证确认，直接回车会取消，必须用 `yes |` 管道
- 挂载卷名可能带版本号，用通配符匹配

## Tron链操作

### 钱包地址格式
- Tron地址以 `T` 开头（如 `TBQN...boGv`）
- ETH地址以 `0x` 开头
- 同一个私钥在不同链上地址不同

### 链上余额查询（TronGrid API）
Tronscan会被Cloudflare拦截，用API替代：
```bash
# 查询账户余额（TRX + TRC20代币）
curl -s "https://api.trongrid.io/v1/accounts/<TRON_ADDRESS>" | python3 -m json.tool

# 返回值解读：
# balance: 78957300 = 78.96 TRX（6位小数）
# trc20: [{"TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t": "13936920"}] = 13.94 USDT
# assetV2: 其他TRC10代币（很多是空投垃圾币，不要碰）
```

### 常用合约地址
- USDT (TRC20): `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`

### Gas费机制
- **TRX转账** = 简单记账操作，Gas约1-2 TRX（~$0.15）
- **TRC20 USDT转账** = 调用智能合约transfer()函数，Gas约8-9 TRX（~$1.3）
- Gas费由区块链网络决定，**跟用什么钱包无关**
- Gas费跟转账金额无关，转1 USDT和转1000 USDT的Gas一样

### 降低Gas费的方法
1. **质押TRX换能量(Energy)** — 最有效，但需要至少200+ TRX
2. **选择低峰时段** — 北京时间凌晨3-6点Gas最低
3. **换链** — 同一种USDT在不同链上Gas差异巨大

### 各链USDT转账Gas费对比
| 链 | Gas费 | 到账速度 |
|---|---|---|
| ETH主网 | $2-20+ | 快 |
| Tron (TRC20) | $0.5-1.5 | 秒到 |
| BSC | $0.1-0.3 | 快 |
| Arbitrum | $0.1-0.5 | 快 |
| Optimism | $0.1-0.5 | 快 |
| Polygon | 几乎免费 | 快 |

## MetaMask配置

### 安装
- Chrome Web Store搜索"MetaMask"
- 开发者：Consensys Software Inc.（官方）
- 注意：MetaMask评分2.7星是因为很多人遇到兼容性问题，不是安全问题

### 支持的网络
- 以太坊、Bitcoin、Solana、BNB Chain等主流网络
- BTC、ETH、USDT、SOL及数十万种代币

## OKX交易所操作

### 充值注意事项
- 充值地址和网络**必须匹配**，选错链资金会丢失
- TRX和USDT的Tron充值地址一样（T开头），但OKX充值时要选对币种
- USDT充值选TRC20网络最便宜

### 资金费率套利（详细操作）

**原理：** 永续合约每8小时结算一次资金费率。市场看涨时做多付钱给做空，看跌时反之。

**操作步骤：**
1. 现货买入等值的币（如买100U的BTC）
2. 同时在永续合约开等量空单（100U的BTC空单）
3. 方向对冲，价格涨跌都不亏
4. 吃资金费率，每8小时结算一次

**实操要点：**
- OKX → 交易 → 永续合约 → 查看当前资金费率
- 费率>0.01%时值得做，<0.01%收益太低
- 需要保证金，杠杆不要太高（2-3倍）
- 年化约10-30%，取决于市场情绪
- 最低几十U就能开始

**风险：**
- 极端行情可能爆仓（杠杆太高时）
- 资金费率可能突然变负
- 交易所API延迟可能导致对冲不及时

### OKX赚币产品
- USDT简单赚币：10%年化，活期，随时取
- USDC简单赚币：10%年化
- 双币赢：结构化产品，最高485%年化但有锁仓风险
- Jumpstart：新币挖矿，需要关注活动时间

### 小资金策略（$140以下）
1. **先放USDT简单赚币**（10%年化，零风险）
2. **关注Jumpstart新活动**（低成本参与新币）
3. **小仓位配置AKT+RENDER**（去中心化算力赛道）
4. **不要All in meme币**（如$BEHEMOTH，纯投机）

## ETH链Gas费优化
- 使用L2网络（Arbitrum/Optimism/Base）代替ETH主网
- 铸造NFT等操作选在Gas低的时段
- 使用Gas追踪工具（Etherscan Gas Tracker）监控实时Gas

## OKX桌面端 computer_use 坑点

OKX桌面端App虽然进程可见（list_apps能发现），但窗口不会暴露给accessibility API：
- `computer_use(action="capture", app="OKX")` 返回0元素
- `focus_app` 返回 "No on-screen window found"
- osascript `activate` 也无法让capture看到内容

**解决方案**：用OKX网页版 `https://www.okx.com` 替代桌面端进行自动化操作。

## macOS/Windows跨平台备份坑点

**不要把macOS和Windows版本混在同一个仓库的子目录里！**
- 用户明确要求分开两个独立仓库
- 正确做法：创建独立仓库（如 `hermes-backup-windows`）
- 原仓库（`hermes-backup`）保持macOS版本纯净
- 两个仓库完全独立，互不影响

**Windows版本需要处理的差异：**
1. 移除macOS专属MCP服务器（lldb-mcp, memscan-mcp）
2. 移除macOS专属skills（apple/*, macos-computer-use等）
3. SOUL.md添加Windows路径/编码/权限说明
4. 添加PowerShell替代bash的命令对照
5. 添加图片分析替代方案（用browser打开本地图片）

## 骗局识别 — 黑U/非法USDT平台

### 特征
- 声称提供"黑USDT兑换"、"冻结包赔"
- 商业模式：低价买黑U → 交易所高价卖 → 赚差价
- 招募代理体系，Telegram客服
- 域名注册时间短，无真实公司信息
- 声称"无司法风险"、"24小时冻结包赔"

### 判断方法（外部评估，不与网站交互）

**第一步：搜索引擎查口碑**
```bash
web_search(query="域名 诈骗 骗局")
web_search(query="domain scam review")
```

**第二步：信任评分工具**
- Gridinsoft: gridinsoft.com（信任评分65/100以下要警惕）
- ScamLens: scamlens.org（综合30+情报源）
- ScamAdviser: scamadviser.com（老牌反诈骗工具）

**第三步：WHOIS查询**
```bash
whois domain.com
# 看注册时间（<1年要警惕）、注册商、隐私保护
```

**第四步：网站内容分析**
```bash
web_extract(urls=["https://domain.com"])
# 很多黑产网站会直接在页面上描述其非法业务模式
# 比如htxusdt.com直接写了"黑USDT兑换"的完整流程
```

**第五步：链上验证（如有钱包地址）**
```bash
# Tron链查询
curl -s "https://api.trongrid.io/v1/accounts/<ADDRESS>"
# 看余额、交易记录、是否有可疑大额转账
```

### 实战案例：htxusdt.com
- 网站自称"老牌USDT承兑系统-黑USDT兑换-黑U冻结包赔"
- 商业模式赤裸裸写在页面上：买黑U → 交易所卖 → 赚差价
- Gridinsoft评分65/100，ScamLens评分100/100（矛盾，说明自动化工具有局限）
- **结论：100%洗钱平台，参与即违法**

### 法律风险
- 参与黑U交易 = "掩饰、隐瞒犯罪所得罪"（刑法第312条，最高7年）
- 交易所账户会被冻结
- 平台本身也会跑路
- 你的个人信息（身份证、银行卡）全部暴露给犯罪团伙

### 正确做法
- 发现可疑网站 → 直接举报（网信办12377.cn / 公安部cyberpolice.cn）
- 不要自己去"渗透测试" — 未授权访问是违法的
- 保留截图证据，不要与网站交互

## TapeOut Protocol（BNB链上硬件制造协议）

详见 `references/tapeout-protocol.md`。

核心概念：1 Token = 1颗晶体管（NAND门），可连线组成电路（NFT），电路可拼装成CPU。
链上BTC矿机是技术Demo，算力极低，不具备实际挖矿价值。
$BEHEMOTH是社区发的meme币，非官方，高风险。

## 去中心化算力项目（DePIN）

详见 `references/decentralized-compute-projects.md`。

核心项目：Render (RENDER)、Akash (AKT)、io.net (IO)、Aethir (ATH)。
赛道逻辑：聚合全球闲置GPU，替代AWS等中心化云算力，比AWS便宜60-80%。
小资金建议：AKT（市值最小上涨空间最大）+ RENDER（最成熟）。
