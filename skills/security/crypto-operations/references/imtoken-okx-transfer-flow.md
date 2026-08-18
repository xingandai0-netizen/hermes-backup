# imToken → OKX 转账流程

## 场景：从imToken钱包转账到OKX交易所

### 前置条件
- imToken钱包有资产（TRX + USDT）
- OKX已注册并完成KYC
- 两端都在同一链上（如Tron链）

### 操作步骤

#### 第一步：获取OKX充值地址
1. 打开OKX → 资产 → 充值
2. 选择币种（USDT或TRX）
3. **选择网络（关键！）**
   - USDT → 选 **TRC20**（波场链）
   - TRX → 选 **Tron (TRC20)**
4. 复制充值地址（T开头）

#### 第二步：imToken发起转账
1. 打开imToken → 选择对应资产（USDT或TRX）
2. 点"转账"
3. 粘贴OKX充值地址
4. 输入金额
5. **注意Gas费**：TRX转账~1.5 TRX，USDT转账~8.5 TRX
6. 建议先转USDT（Gas贵的先处理），再转TRX
7. 确认 → 输入密码 → 完成

#### 第三步：等待到账
- Tron链通常1-3分钟到账
- OKX会自动识别并入账

### ⚠️ 关键注意事项
1. **地址和网络必须匹配** — 选错链资金会丢失且无法找回
2. **TRX和USDT的Tron充值地址一样**（都是T开头），但OKX充值时要选对币种
3. **先转USDT再转TRX** — 因为转USDT需要消耗TRX作为Gas，确保留够Gas费
4. **不要把所有TRX都转了** — 至少留1-2 TRX作为Gas

### Gas费计算示例
假设钱包有13.94 USDT + 78.96 TRX：
1. 转USDT到OKX：扣~8.5 TRX Gas → 到账13.94 USDT
2. 剩余~70.5 TRX再转：扣~1.5 TRX Gas → 到账~69 TRX
3. 最终OKX到账：13.94 USDT + 69 TRX

### 从OKX转出到imToken
反向操作，但更简单：
1. OKX → 资产 → 提币
2. 选择币种和网络（TRC20）
3. 粘贴imToken的接收地址
4. 确认提币
- OKX提币USDT(TRC20)通常扣1 USDT手续费
