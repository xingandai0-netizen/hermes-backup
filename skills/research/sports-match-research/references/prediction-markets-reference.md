# Polymarket & Prediction Markets Reference

> Absorbed from `prediction-research` skill (archived 2026-06-21).

## Polymarket APIs

1. **Gamma API** — `gamma-api.polymarket.com` — Discovery, search, browsing
2. **CLOB API** — `clob.polymarket.com` — Real-time prices, orderbooks, history
3. **Data API** — `data-api.polymarket.com` — Trades, open interest

### Key Concepts
- Events contain Markets (1:many)
- Markets are binary outcomes with Yes/No prices 0.00–1.00
- Prices ARE probabilities: 0.65 = 65%
- `outcomePrices` is double-encoded JSON: `["0.80", "0.20"]`
- Volume in USDC

### Rate Limits
- Gamma: 4,000 req / 10 sec
- CLOB: 9,000 req / 10 sec
- Data: 1,000 req / 10 sec

### Parsing Double-Encoded Fields
```python
import json
prices = json.loads(market['outcomePrices'])  # ["0.652", "0.348"] → 65.2% Yes
```

## Prediction Market Sources
- **Robinhood** — Correct score markets priced in cents (18¢ = 18%)
- **Kalshi** — Game outcome + correct score markets
- **Coinbase Predictions** — Similar to Kalshi

These are crowd-sourced probability benchmarks, not expert picks.

## Scripts
See `scripts/polymarket.py` for ready-to-use Python script.
