# Crypto Malicious Project Taxonomy

Complete reference for identifying and categorizing cryptocurrency malicious projects on GitHub for bounty reporting.

## Category 1: Wallet Drainers

**What they do**: Steal funds by tricking users into signing malicious transactions or approving token spending.

**Attack vectors**:
- Phishing pages that request unlimited token approval
- Fake airdrop claims that drain wallet
- Malicious smart contracts with hidden drain functions

**Key indicators**:
- `approve()` or `setApprovalForAll()` calls
- `transferFrom()` in contract code
- Phishing page templates with wallet connect
- README with "educational purposes only" disclaimer

**Examples**:
- `CashBears/testt` — BUSD drainer with stealth forwarding (8★, 108 forks)
- `otsybizov/wallet-drainer` — Multi-chain EVM drainer CLI
- `btelemaque/dual-chain-crypto-drainer` — ETH + Solana cross-chain

**DaaS ecosystem** (not on GitHub, distributed via Telegram):
- Inferno Drainer — $494M stolen from 332K victims
- Angel Drainer — $200M+ stolen
- Pink Drainer — Active 2024-2025
- Quark Lab — Complete panel with 400+ landing pages

---

## Category 2: Clipboard Hijackers

**What they do**: Monitor clipboard for crypto addresses and replace with attacker's address.

**How it works**:
1. Run in background (silent, no UI)
2. Monitor clipboard for address patterns (regex)
3. Replace matched address with predefined attacker address
4. User unknowingly sends funds to attacker

**Key indicators**:
- Clipboard monitoring code (`GetClipboardData`, `pbcopy`, `xclip`)
- Address regex patterns (`^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$` for BTC)
- Address replacement logic
- Persistence mechanisms (startup registry, cron)

**Examples**:
- `matifanger/crypto-replacer` — 11 cryptos, .exe builder (20★)
- `Modyev/Crypto-Address-Clipper` — C# silent operation (3★)
- `mr3moe/clipTakeOver` — Multi-coin support (5★)

**Damage potential**: Unlimited — any transaction amount can be stolen.

---

## Category 3: Address Poisoning Tools

**What they do**: Generate vanity addresses similar to victim's address, then send small transactions to poison transaction history.

**How it works**:
1. Scan victim's transaction history
2. Generate vanity address matching first/last characters
3. Send fake USDT/small ETH transaction from vanity address
4. Victim copies poisoned address from history
5. Funds go to attacker's vanity address

**Key indicators**:
- Vanity address generation code
- Transaction history scanning
- Fake token contracts (Fake-USDT.sol)
- Address similarity matching

**Examples**:
- `Muhammad-Ramazanovich/Eth-Address-Poisoning-Tools` — Complete workflow (6★)

**Real-world damage**: Single attack stole $71M in WBTC (later recovered via negotiation).

---

## Category 4: Honeypot Tokens

**What they do**: Create tokens that allow buying but prevent selling, trapping victim's funds.

**How it works**:
1. Deploy token contract with hidden honeypot logic
2. Add liquidity to DEX (Uniswap/PancakeSwap)
3. Victims buy token (transaction succeeds)
4. Victims try to sell (transaction fails or taxed 99%)
5. Attacker removes liquidity

**Key indicators**:
- `canSell` or `isHoneypot` flags in contract
- Hidden owner functions to toggle sell restriction
- Whitelist addresses that CAN sell (attacker's addresses)
- High sell tax (99%+)

**Examples**:
- `cryptokoki-services/bsc-honeypot` — Complete BSC workflow
- `cryptokoki-services/honeypot-token-v6` — Updated version
- `cryptokoki-services/solana-honeypot-token` — Solana + Raydium
- `cryptokoki-services/solana-honeypot-pro` — Batch freeze holders

**Real-world damage**: #4Agent token honeypot drained $100,000 (170 BNB).

---

## Category 5: Seed Phrase / Private Key Tools

**What they do**: Generate or brute-force mnemonic phrases/private keys and check for funded wallets.

**How it works**:
1. Generate random mnemonic phrases (BIP-39)
2. Derive wallet addresses
3. Check balance via API or offline database
4. Save wallets with funds
5. Transfer funds to attacker

**Key indicators**:
- BIP-39 wordlist usage
- HD wallet derivation (`m/44'/60'/0'/0/0`)
- Balance checking code (Etherscan API, blockchain.info)
- Multi-threaded generation

**Examples**:
- `Cr0mb/Crypto-Sweeper` — BTC/ETH, API check (4★)
- `Michal2SAB/Ethereum-Stealer` — Random key generation (203★)
- `Tkkytrs/Trustwallet-Mnemonic-Grabber` — TrustWallet specific (23★)
- `LizardX2/BTCMiner` — Bitcoin seed brute force (23★)
- `Pymmdrza/AttackAIO_Crypto` — All-in-one attack tool

**Probability**: Astronomically low (~1 in 76 trillion for BTC), but tools automate millions of attempts.

---

## Category 6: Phishing Kits

**What they do**: Complete phishing page templates that mimic legitimate wallet/DApp interfaces.

**How it works**:
1. Clone legitimate wallet UI (MetaMask, Trust Wallet)
2. Host on lookalike domain
3. Request seed phrase or wallet connection
4. Send stolen data to attacker's server
5. Drain wallet

**Key indicators**:
- HTML/CSS matching wallet UI
- Form submission to external server
- Wallet Connect integration
- Seed phrase input fields

**Examples**:
- `netrandom/tonconnect` — TON Connect phishing for Telegram Mini Apps
- Cloudflare Pages-based kits (distributed via Telegram)

---

## Category 7: Sandwich / MEV Bots

**What they do**: Monitor mempool for pending DEX trades and frontrun them for profit.

**How it works**:
1. Monitor mempool for large DEX swaps
2. Buy token before victim (frontrun)
3. Victim's trade executes (price increases)
4. Sell token after victim (backrun)
5. Profit from price difference

**Key indicators**:
- Mempool monitoring code
- Flashbots integration
- Gas price optimization
- DEX router interactions

**Examples**:
- `SamSamDev9/pancake-sandwich-bot-2026` — BSC/ETH/AVAX/MATIC (0★)

**Profit potential**: Claims "0.1 BNB into 2 BNB in 1 day". MEV bots earn $50-100M annually.

---

## Category 8: Fake Token Generators

**What they do**: Create tokens that mimic legitimate tokens (USDT, USDC) for scam purposes.

**How it works**:
1. Deploy ERC-20/BEP-20 token with same name/symbol as real token
2. Add liquidity to DEX
3. Use in phishing/OTC scams
4. Victim receives worthless fake tokens

**Key indicators**:
- Token name/symbol matching legitimate tokens
- No verification on block explorer
- Suspicious deployment patterns

**Examples**:
- `Multi-Chain-Fake-Token-Tools` — ETH/BSC/Polygon
- `ERC-20-Fake-Token-Generator`
- `Fake-USDT.sol` (included in address poisoning tools)

---

## "闭环" Assessment Checklist

Use this checklist to determine if a project is "闭环" (complete/closed-loop):

| Criterion | Check |
|-----------|-------|
| **1. Complete workflow** | Does it have all components (generate → attack → steal)? |
| **2. Working code** | Is it actually functional, not just PoC? |
| **3. Deployable** | Can it be packaged (.exe, .apk, web app)? |
| **4. Profit path** | Is there a clear mechanism to extract funds? |
| **5. Documentation** | Does README explain how to use it? |
| **6. Dependencies** | Are all required libraries/tools listed? |
| **7. Examples** | Does it include example usage or demo? |

**Scoring**:
- 7/7 = Fully closed-loop (highest bounty value)
- 5-6/7 = Mostly closed-loop (high value)
- 3-4/7 = Partially closed-loop (medium value)
- 0-2/7 = Not closed-loop (low value, may be educational only)

---

## Search Strategy Summary

### Focus on LOW stars (0-50)
Most dangerous tools are unknown. High-star projects get taken down quickly.

### Check README for "educational purposes only"
Often indicates malicious intent disguised as research.

### Look for complete workflows
Not just PoC — look for full attack chains.

### Check recent commits
Active projects are more dangerous than abandoned ones.

### Verify deployability
Can it be packaged and distributed? (.exe, .apk, web app)

---

## Bounty Reporting Template

```markdown
# Malicious Project Report

## Repository
- URL: https://github.com/...
- Stars: X
- Forks: Y
- Last updated: YYYY-MM-DD

## Category
[Wallet Drainer / Clipboard Hijacker / Address Poisoning / Honeypot Token / Seed Phrase Cracker / Phishing Kit / Sandwich Bot / Fake Token]

## Closed-Loop Assessment
- [ ] Complete workflow
- [ ] Working code
- [ ] Deployable
- [ ] Profit path
- Score: X/7

## What It Does
[Detailed description of malicious activity]

## Potential Financial Damage
[Estimated damage per attack or total]

## Evidence of Malicious Intent
- README quotes
- Code comments
- Real-world damage examples

## Recommendation
[Remove repository / Ban user / etc.]
```
