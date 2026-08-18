# Tron链上查询实战记录

## TronGrid API 查询波场账户

```bash
curl -s "https://api.trongrid.io/v1/accounts/{地址}" | python3 -m json.tool
```

### 返回结构关键字段

```json
{
  "data": [{
    "balance": 78957300,           // TRX余额，单位sun（÷1,000,000 = TRX）
    "trc20": [{
      "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t": "13936920"  // USDT，÷1,000,000 = 13.94
    }],
    "assetV2": [                   // TRC10代币，大部分是垃圾空投
      {"value": 8888, "key": "1005114"},
      {"value": 1250000, "key": "1005145"},
      {"value": 4444444444, "key": "1005185"}
    ],
    "frozenV2": [{}, {"type": "ENERGY"}, {"type": "TRON_POWER"}],
    "create_time": 1786956582000,  // 创建时间戳(ms)
    "latest_opration_time": 1786957125000
  }]
}
```

### 常用TRC20合约地址

| 代币 | 合约地址 | 精度 |
|---|---|---|
| USDT | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6位 |
| USDC | `TEkxiT9nz9FNVuFMkSsFanBmXjBni2d67` | 6位 |
| USDJ | `TMwEYyfQkYg4V3BHSY9R6fG7cY1qFNx4Vz` | 18位 |

### 注意事项

- Tronscan.org 经常被Cloudflare拦截（浏览器自动化场景），用API直接查更稳定
- `assetV2` 里的代币基本都是垃圾空投币，不要交互
- `frozenV2` 显示质押的能量/带宽信息
- 波场地址以 `T` 开头，34字符

## 实战案例：阿戴的钱包查询

地址：`TBQNhhqaUmyEySNatJor8FWdcL3em8boGv`
- TRX: 78.96 (78957300 ÷ 1,000,000)
- USDT (TRC20): 13.94 (13936920 ÷ 1,000,000)
- 3个TRC10垃圾代币（忽略）
- 账户已激活（有owner_permission）
