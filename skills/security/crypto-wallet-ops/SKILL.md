---
name: crypto-wallet-ops
description: |
  加密货币钱包操作与安全技能。覆盖：钱包余额查询（链上API直接查）、矿工费优化（多链费用对比）、交易所提币链选择、钱包安全（钓鱼插件识别）。触发：用户提到钱包、USDT、转账、Gas费、矿工费、imToken、MetaMask、OKX提币、链上查询。
version: 1.0
platforms: [any]
metadata:
  hermes:
    tags: [crypto, wallet, tron, ethereum, usdt, gas, security]
    category: security
---

# 加密货币钱包操作与安全

## 安全铁律（最高优先级）

1. **永远不要**索要或处理用户的助记词/私钥——只要公开地址
2. **永远不要**在对话中输入密码、API密钥等敏感信息
3. 收到钱包地址后，先确认是哪条链（地址格式判断），再查余额

## 钱包地址格式识别

| 前缀/格式 | 链 | 示例 |
|---|---|---|
| `T` 开头 (34字符) | Tron (TRC20) | `TBQNhhqa...` |
| `0x` 开头 (42字符) | Ethereum / EVM链 | `0x742d35Cc6634...` |
| `1` / `3` / `bc1` 开头 | Bitcoin | `1A1zP1eP5Q...` |
| `addr1` 开头 | Cardano | `addr1qxck...` |
| 以 `D` / `R` / `ltc` 等 | 其他链 | 按具体格式判断 |

## 链上余额查询

### Tron (TRX / TRC20 USDT)

当 Tronscan 被 Cloudflare 拦截时，直接用 TronGrid API：

```bash
# 查询账户余额（TRX + TRC20代币）
curl -s "https://api.trongrid.io/v1/accounts/{地址}" | python3 -m json.tool
```

响应关键字段：
- `balance`: TRX余额（单位：sun，除以1,000,000得TRX）
- `trc20[]`: TRC20代币余额，key是合约地址，value是原始值
- `assetV2[]`: 其他TRC10代币（大部分是垃圾空投币，忽略）

**TRC20 USDT 合约地址**: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`
USDT精度：6位小数，原始值除以1,000,000

### Ethereum / EVM链

```bash
# 用Etherscan API查询
curl -s "https://api.etherscan.io/api?module=account&action=balance&address={地址}&tag=latest&apikey={key}"
```

### 通用方案

如果特定区块链浏览器被封，尝试：
1. 直接用链的官方RPC/API（如TronGrid、Infura、Alchemy）
2. 换一个区块链浏览器（如 tronscan → trxplorer → blockchair）
3. 用 `web_extract` 抓取浏览器页面内容

## 矿工费(Gas)优化

### 各链转账费用对比（USDT为例，2026年数据）

| 链 | 类型 | 转账费用 | 到账速度 |
|---|---|---|---|
| ETH主网 | L1 | $2-20+ | 15秒-5分钟 |
| Tron (TRC20) | L1 | $1-2 | 1-3分钟 |
| BSC (BEP20) | L1 | $0.1-0.3 | 3秒 |
| Arbitrum | L2 | $0.1-0.5 | 即时 |
| Optimism | L2 | $0.1-0.5 | 即时 |
| Polygon | Sidechain | 几乎免费 | 2秒 |
| Solana | L1 | <$0.01 | 即时 |

### 降低Gas费的实操方法

1. **选对链**（最重要）：同一种USDT在不同链上费用差几十倍
2. **挑低峰时段**：北京时间凌晨3-6点（UTC 19:00-22:00）最便宜，周末比工作日便宜
3. **手动调Gas**：imToken/MetaMask转账时可以进"高级设置"调低Gas Price，代价是到账慢
4. **从交易所提币选链**：OKX/Binance提USDT时选TRC20或Arbitrum链，费用最低

### OKX提币最优方案

从OKX提USDT到外部钱包：
- 最便宜：选 **TRC20（波场）** 链，手续费约1 USDT
- 次选：选 **Arbitrum** 或 **BSC** 链
- 最贵：选 **ETH主网**，手续费可能$5-20

## 常见钓鱼/诈骗识别

### imToken Chrome插件骗局（2026年3月慢雾安全团队确认）

**imToken从未发布过Chrome浏览器插件。** Chrome商店里所有声称是imToken的钱包扩展全部是恶意钓鱼工具，专门窃取助记词和私钥。

识别特征：
- 声称是imToken但实际是Chrome插件
- 安装后自动跳转到钓鱼页面
- 要求输入12/24词助记词或私钥
- 假装在"升级钱包"或"同步数据"

### 通用防钓鱼原则

1. 只从官方渠道下载钱包App
2. 永远不在浏览器插件中输入助记词
3. 转账前核实合约地址
4. 大额资产用硬件钱包（Ledger/Trezor）
5. 不点击社交媒体/邮件中的"钱包升级"链接

## 常用工具

- **TronGrid API**: https://api.trongrid.io/v1/ — Tron链上数据查询
- **Etherscan**: https://etherscan.io — Ethereum浏览器
- **Tronscan**: https://tronscan.org — Tron浏览器（可能被Cloudflare拦截）
- **DeBank**: https://debank.com — 多链资产总览
- **MetaMask**: 官方Chrome插件，Consensys出品
