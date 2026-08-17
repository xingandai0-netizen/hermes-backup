---
name: defi-security-research
description: "DeFi smart contract vulnerability research, abandoned project discovery, and exploit analysis. Use when: auditing smart contracts, finding abandoned DeFi projects with residual funds, classifying vulnerability types, analyzing PoC exploit code, or generating vulnerability reports."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [DeFi, blockchain, smart-contract, vulnerability, security, Solidity, exploit]
    related_skills: [github-security-arsenal, diagnose]
---

# DeFi Security Research

Systematic methodology for discovering abandoned DeFi projects, analyzing smart contract vulnerabilities, and generating audit reports.

## When to Use

- User wants to find abandoned/defunct DeFi projects
- User wants to audit smart contracts for vulnerabilities
- User wants to analyze historical DeFi exploits
- User wants to generate vulnerability reports
- User wants to find malicious crypto projects on GitHub for bounty reporting
- User mentions "DeFi漏洞", "合约审计", "废弃项目", "智能合约安全"
- User mentions "灰产", "黑色产业", "恶意项目举报", "赏金"

## Step 1: Data Sources

### Primary Databases

| Source | Content | URL |
|--------|---------|-----|
| **Rekt.news Leaderboard** | 300+ ranked exploits by loss | rekt.news/leaderboard |
| **DefiLlama Hacks** | 821+ security incidents | defillama.com/hacks |
| **DeadDeFi.com** | Verified dead protocols with contract addresses + residual TVL | deaddefi.com |
| **ChainSec.io** | 191+ documented exploits, $6.1B total | chainsec.io/defi-hacks |
| **RootData** | Annual dead project lists | rootdata.com |

### PoC Exploit Repositories

| Repository | Content | Use Case |
|------------|---------|----------|
| `kismp123/DeFi-Security-Incident` | 821 incidents, organized by year + vulnerability type | Primary reference, no Solidity files, markdown analysis |
| `SunWeb3Sec/DeFiHackLabs` | Runnable Foundry PoC exploits | Local testing, fork mainnet simulation |
| `pcaversaccio/defi-vulns` | Vulnerability classification database | Taxonomy reference |

**Clone the primary repo:**
```bash
git clone --depth 1 https://github.com/kismp123/DeFi-Security-Incident.git
```

Structure: `2020/`, `2021/`, ..., `2026/` (year folders with markdown incident reports) + `vulns/` (vulnerability type index files).

## Step 2: Vulnerability Taxonomy (25 Types)

### Top Vulnerability Types by Frequency

| Rank | Type | Cases | Typical Loss | Difficulty |
|------|------|-------|--------------|------------|
| 1 | Flash Loan Manipulation | 116 | $24M-$200M | Low-Medium |
| 2 | Oracle Price Manipulation | 96 | $7M-$120M | Medium |
| 3 | Access Control | 96 | $1M-$235M | Low |
| 4 | Reentrancy | 61 | $2M-$25M | Medium |
| 5 | NFT-related | 35 | $1M-$10M | Medium |
| 6 | Business Logic | 8 | $5M-$50M | High |
| 7 | Arbitrary Call | 5 | $5M-$14M | Medium |
| 8 | Bridge/CrossChain | 4 | $100M-$624M | Very High |
| 9 | Private Key Compromise | 3 | $7M-$140M | Low |
| 10 | Governance Attack | 70 | $5M-$182M | High |

### Vulnerability Detection Patterns (Regex for Source Code Analysis)

```python
VULNERABILITY_PATTERNS = {
    "reentrancy": [
        r"\.call\{value:.*\}\(.*\)[\s\S]*?(?=balance|Balance|state)",
        r"\.call\.value\(.*\)\(.*\)",
        r"\.transfer\(.*\)[\s\S]*?state",
        r"\.send\(.*\)[\s\S]*?state",
    ],
    "flash_loan": [
        r"flashLoan", r"flash_loan", r"flashswap",
        r"IFlashLoan", r"function.*flash",
        r"getAmountsOut", r"getReserves",
    ],
    "oracle_manipulation": [
        r"getReserves", r"getAmountOut", r"getAmountsOut",
        r"balanceOf.*pair", r"UniswapV2Library",
        r"\.spot\(", r"totalSupply.*balanceOf",
    ],
    "access_control": [
        r"function.*mint.*public(?!.*only)",
        r"function.*initialize.*public(?!.*only)",
        r"selfdestruct\(", r"delegatecall\(",
    ],
    "unchecked_call": [
        r"\.call\{.*\}\(.*\)(?![\s\S]*require)",
        r"\.delegatecall\(.*\)(?![\s\S]*require)",
    ],
}
```

## Step 3: Finding Abandoned Projects

### Categories of Abandoned Projects

1. **Hacked and abandoned** — Was exploited, team left, contract still on-chain
2. **Rug pulled** — Developer drained funds and disappeared
3. **Forked and abandoned** — Copied code from successful project, never maintained
4. **Ecosystem collapse casualties** — Died when Terra/FTX collapsed
5. **Deprecated old versions** — V1 contracts when V2/V3 launched

### High-Value Targets (Residual Funds Confirmed)

DeadDeFi.com maintains a verified list of dead protocols with:
- Contract addresses
- Residual TVL (Total Value Locked)
- Verification status

As of 2026-08: 13 protocols with ~$16.6M total residual funds.

### Search Strategy

```bash
# Search GitHub for abandoned DeFi projects
# Queries to use:
"abandoned DeFi projects" list
"dead DeFi protocols"
"rugged DeFi projects" list 2020 2021
"DeFi hacks" complete list
DeFi Llama "dead" protocols
"forked DeFi" abandoned
```

## Step 4: Contract Analysis

### Tool Installation

```bash
# Slither (static analysis)
pip install slither-analyzer

# Note: May fail on Python 3.14+ due to cbor2 build issues
# Fallback: Use Python regex patterns on source code

# Foundry (development + testing)
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

### Etherscan Source Code Fetching

```python
import requests

def fetch_contract_source(address, chain="eth"):
    apis = {
        "eth": "https://api.etherscan.io/api",
        "bsc": "https://api.bscscan.com/api",
        "polygon": "https://api.polygonscan.com/api",
    }
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": ""  # Free tier, no key needed
    }
    resp = requests.get(apis[chain], params=params, timeout=15)
    data = resp.json()
    if data.get("status") == "1" and data.get("result"):
        return data["result"][0].get("SourceCode")
    return None
```

**Pitfall:** Etherscan free API has rate limits (~5 req/sec). Add `time.sleep(0.5)` between calls.

**Pitfall:** Etherscan free API (no key) often returns empty results for `getsourcecode` on older contracts. Verified contracts from 2020-2021 era may not return source code without an API key. **Workaround:** Use GitHub PoC repos (kismp123/DeFi-Security-Incident) which already have the vulnerability analysis — don't rely solely on Etherscan API for batch scanning.

**Pitfall:** `pip install slither-analyzer` fails on Python 3.14+ due to `cbor2` build failure. `pip install --no-deps` won't work either because crytic-compile dependency chain is complex. **Workaround:** Use regex-based pattern matching on source code (see Step 4 patterns) or use Foundry's `forge` for analysis.

**Pitfall:** Many old contracts are NOT verified on Etherscan. For unverified contracts, you can only analyze bytecode, not source code.

### Manual Audit Checklist

```
1. Check access control on all external/public functions
2. Check state updates before external calls (reentrancy)
3. Check price oracle source (is it manipulable?)
4. Check flash loan protection (same-transaction check?)
5. Check initialize function (can it be called again?)
6. Check selfdestruct/delegatecall usage
7. Check signature verification logic (replay risk?)
8. Check integer overflow/precision loss
9. Check event logging completeness
10. Check emergency pause mechanism
```

## Step 5: Report Generation

### Report Structure

```markdown
# [Project Name] Vulnerability Analysis

## Summary
- Contract address: 0x...
- Chain: Ethereum/BSC/Polygon
- Status: Abandoned/Hacked/Rug Pulled
- Residual funds: $X
- Vulnerability count: N

## Vulnerabilities Found
### [CRITICAL] Reentrancy in withdraw()
- Location: contract.sol:123
- Description: ...
- PoC: ...
- Impact: $X at risk

## Recommendations
1. ...
2. ...
```

## 桌面产出文件（2026-08-09生成）

- `~/Desktop/废弃DeFi项目清单.md` — 188个项目完整列表
- `~/Desktop/DeFi漏洞分析完整报告.md` — 漏洞类型详解+PoC代码模式
- `~/Desktop/DeFi漏洞PoC完整清单.md` — 821个PoC清单(203KB)
- `~/Desktop/DeFi审计日志.md` — 完整执行日志
- `~/Desktop/all_defi_pocs.json` — 821个PoC结构化数据
- `~/Desktop/etherscan_batch_scanner.py` — Etherscan批量扫描器(18个目标)
- `~/Desktop/defi_vuln_scanner.py` — 基础漏洞扫描器
- `~/Desktop/audit_deaddefi.py` — DeadDeFi专用扫描器
- `~/Desktop/extract_all_pocs.py` — PoC元数据提取器
- `~/Desktop/DeFi-Security-Incident/` — 821个PoC源码仓库

## Step 6: Malicious Project Discovery for Bounty Reporting

**Use when**: User wants to find malicious crypto projects on GitHub for bounty reporting (举报拿赏金). This is legitimate security research — finding and reporting malicious tools helps protect the ecosystem.

### Taxonomy of Crypto Malicious Projects

| Category | Description | Risk Level | Bounty Value |
|----------|-------------|------------|--------------|
| **Wallet Drainer** | Steal funds via phishing/approval exploit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Clipboard Hijacker** | Replace crypto addresses in clipboard | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Address Poisoning** | Generate similar addresses to trick victims | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Honeypot Token** | Token that prevents selling after buy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Seed Phrase Cracker** | Brute force mnemonic phrases | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Private Key Scanner** | Generate keys and check balances | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Phishing Kit** | Fake wallet/DApp pages | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Sandwich Bot** | MEV frontrunning attack | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Fake Token Generator** | Create scam tokens | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **DaaS (Drainer as a Service)** | Commercial drainer platforms | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### "闭环" (Closed-Loop) Assessment Criteria

A project is "闭环" if it can **actually generate financial profit** end-to-end:

1. **Complete workflow** — Has all components needed (generate → attack → steal)
2. **Working code** — Not just PoC or documentation
3. **Deployable** — Can be packaged and distributed
4. **Profit path** — Clear mechanism to extract funds

**Example**:
- ✅ **闭环**: `matifanger/crypto-replacer` — Clipboard monitor + address replacement + .exe builder
- ❌ **非闭环**: Educational reentrancy PoC — Only demonstrates concept, can't actually steal

### Search Strategies for Niche/Unknown Projects

**Key principle**: Most dangerous tools have LOW stars (0-50). High-star projects get taken down quickly.

#### Search Queries by Category

**Wallet Drainers**:
```
"wallet drainer" "web3" "approve" "transferFrom"
"wallet drain" "metamask" "ethers.js"
"drainer" "phishing" "seed phrase"
```

**Clipboard Hijackers**:
```
"clipboard" "replace" "btc" "address" "stealth"
"cryptocurrency" "hijack" "background" "monitor"
"clipTakeOver" OR "crypto-replacer" OR "address-clipper"
```

**Address Poisoning**:
```
"address poisoning" "vanity" "generate" "similar"
"fake USDT" "poison" "transaction"
"Eth-Address-Poisoning"
```

**Honeypot Tokens**:
```
"honeypot" "token" "create" "bsc" "uniswap"
"rug pull" "liquidity" "remove" "scam"
"cryptokoki-services" honeypot
```

**Seed Phrase Tools**:
```
"mnemonic" "brute force" "balance" "sweep"
"seed phrase" "crack" "generate" "wallet"
"WalletGen" OR "Crypto-Sweeper" OR "Ethereum-Stealer"
```

**Phishing Kits**:
```
"metamask" "phishing" "seed" "verify"
"wallet connect" "fake" "template" "drain"
"tonconnect" "phishing" "telegram"
```

**Sandwich/MEV Bots**:
```
"sandwich" "frontrun" "mev" "bot" "pancake"
"mempool" "monitor" "flashbot"
"pancake-sandwich-bot"
```

#### High-Value Repositories Found (2026-08)

| Repository | Stars | Type | Closed-Loop? | Notes |
|------------|-------|------|--------------|-------|
| matifanger/crypto-replacer | 20 | Clipboard Hijacker | ✅ Yes | 11 cryptos, .exe builder |
| Muhammad-Ramazanovich/Eth-Address-Poisoning-Tools | 6 | Address Poisoning | ✅ Yes | Fake-USDT.sol included |
| cryptokoki-services/bsc-honeypot | 0 | Honeypot Token | ✅ Yes | Complete BSC workflow |
| Modyev/Crypto-Address-Clipper | 3 | Clipboard Hijacker | ✅ Yes | C# silent operation |
| SamSamDev9/pancake-sandwich-bot-2026 | 0 | Sandwich Bot | ✅ Yes | BSC/ETH/AVAX/MATIC |
| Cr0mb/Crypto-Sweeper | 4 | Seed Phrase Scanner | ✅ Yes | BTC/ETH, API check |
| Michal2SAB/Ethereum-Stealer | 203 | Private Key Scanner | ✅ Yes | High stars, likely to be taken down |
| Tkkytrs/Trustwallet-Mnemonic-Grabber | 23 | Seed Phrase Grabber | ✅ Yes | TrustWallet specific |
| netrandom/tonconnect | - | TON Phishing | ✅ Yes | Telegram Mini App |

### Bounty Reporting Workflow

1. **Discovery** — Use search queries above to find suspicious repos
2. **Assessment** — Check if "闭环" (complete workflow, working code)
3. **Analysis** — Document:
   - What malicious activity it enables
   - How complete/sophisticated it is
   - Potential financial damage
   - Star/fork count (传播程度)
4. **Report** — Submit through bounty platform with:
   - Repository URL
   - Category (drainer/clipper/honeypot/etc.)
   - Closed-loop assessment
   - Evidence of malicious intent (README, code comments)
   - Real-world damage examples if available

### Key Statistics (2025-2026)

- **$19.3B** stolen via wallet drainers in H1 2025
- **65.4M** address poisoning attacks blocked by Blockaid
- **$494M** stolen by Inferno Drainer alone (332K victims)
- **DaaS ecosystem**: Telegram-based, $500-$10,000 per kit
- **GitVenom campaign**: Hundreds of malicious GitHub repos distributing stealers

## 用户术语注意

阿戴说"偏门财运"= 漏洞赏金/安全研究，不是玄学/算命。

## Pitfalls

1. **"偏门财运" terminology confusion** — User (阿戴) uses "偏门财运" to mean security vulnerabilities/bug bounty, NOT fortune-telling/玄学. If user mentions this term, clarify they mean security research, not divination.

2. **"闭环" assessment is critical** — User specifically wants projects that are "闭环" (complete/closed-loop). Don't report educational PoC or incomplete tools. Check: complete workflow, working code, deployable, profit path.

3. **Focus on LOW-star projects** — High-star malicious repos get taken down quickly. The most dangerous tools have 0-50 stars. Use niche search queries to find unknown projects.

4. **DaaS ecosystem is Telegram-based** — Complete drainer kits (Inferno, Angel, Pink, Quark Lab) are sold via Telegram for $500-$10,000, NOT hosted on GitHub. GitHub only has fragments, gists, or older versions.

5. **Etherscan免费API限速** — 无key时约1次/秒，注册后5次/秒

2. **Unverified contracts** — Many old contracts don't have verified source code. You can only do bytecode analysis for these.

3. **Slither Python version issues** — Slither may fail to install on Python 3.14+ due to cbor2 build failures. Fallback to regex-based pattern matching on source code.

4. **False positives in regex scanning** — Pattern matching catches syntax but not semantics. A `\.call` followed by `balance` isn't necessarily vulnerable — context matters. Always verify manually.

5. **Legal boundaries** — Finding vulnerabilities is legitimate security research. Exploiting them to steal funds is a crime. Always encourage responsible disclosure.

6. **DeadDeFi.com data freshness** — Residual TVL numbers change as funds move. Always verify current balance on-chain before acting.

7. **Fork project code drift** — Forked projects may have modified the original code. Don't assume they have the same vulnerabilities as the original.

8. **Gas costs for on-chain verification** — Testing exploits on mainnet fork requires ETH for gas estimation. Use Foundry's `--fork-url` for free local testing.

## References

- `references/vulnerability-database.md` — Complete vulnerability type classification with PoC patterns
- `references/abandoned-projects.md` — Verified list of 188 abandoned DeFi projects with contract addresses
- `references/exploit-code-patterns.md` — Copy-paste ready exploit code patterns for each vulnerability type
- `references/vulnerability-statistics.md` — 821 PoC stats: annual trend, type distribution, top 10 hacks, DeadDeFi verified contracts with addresses and residual TVL
- `references/malicious-project-taxonomy.md` — Complete taxonomy of crypto malicious projects for bounty reporting (wallet drainers, clipboard hijackers, honeypot tokens, address poisoning, etc.) with "闭环" assessment criteria and search strategies
- `references/malicious-project-bounty-research.md` — Full bounty research workflow: discovery, closed-loop assessment, technical analysis, revenue/cost analysis, report preparation (absorbed from standalone skill)
- `references/bounty-external-services.md` — Common gray-market service documentation for bounty research
- `references/bounty-platform-analysis.md` — Platform-specific security mechanism comparisons
- `references/bounty-validated-projects.md` — Validated malicious project database
- `scripts/defi_vuln_scanner.py` — Python scanner for Etherscan source code analysis (regex-based, no Slither needed)
