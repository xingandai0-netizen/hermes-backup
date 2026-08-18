---
name: new-api-operations
description: "new-api (QuantumNous/new-api) deployment, channel management, and operations. Covers Docker deployment, admin API, channel creation, load balancing, rate limiting, and brand replacement."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [new-api, api-proxy, channel-management, deployment, load-balancing, quantumnous]
    related_skills: [antokex-operations]
---

# new-api Operations

Complete guide for deploying and managing [new-api](https://github.com/QuantumNous/new-api) — an API proxy/reverse-proxy for LLM providers.

## When to Use

- Deploying new-api (Docker or bare metal)
- Creating and managing API channels
- Configuring load balancing and rate limiting
- Brand replacement and customization
- Troubleshooting channel issues

## Quick Deploy (Docker)

```bash
docker run -d \
  --name new-api \
  -p 3000:3000 \
  -e SQL_DSN="postgres://user:pass@host/db" \
  -e SESSION_SECRET="random-secret" \
  -v ./data:/data \
  quantumnous/new-api:latest
```

## Channel Management

### Creating Channels

See [references/channel-creation.md](references/channel-creation.md) for the full browser UI flow.

**Key points:**
- Each channel represents an upstream API provider
- Set base URL, API key, model list, and priority
- Test channels before enabling them
- Use self-use mode for personal channels

### Channel Operations

See [references/channel-management.md](references/channel-management.md) for the full operational guide.

**Load balancing:**
- Multiple channels with the same model → automatic round-robin
- Priority field controls fallback order
- Weight field controls distribution ratio

**Rate limiting:**
- Per-channel rate limits prevent upstream abuse
- Per-user rate limits prevent single-user monopolization
- Token-based quotas for billing

### Advanced Operations

**Rate multipliers (pricing):**
- Set channel rate multiplier for cost recovery
- Example: 1.5x means users pay 1.5x the upstream cost
- Balance between profitability and user retention

**Risk control:**
- Automatic channel disabling on consecutive failures
- Alert thresholds for unusual usage patterns
- IP-based blocking for abuse prevention

**Connection pooling:**
- Group channels by upstream provider
- Distribute load across multiple API keys
- Automatic failover when a channel is exhausted

---

## Admin API

```bash
# List channels
curl -s -H "Authorization: Bearer $ADMIN_KEY" http://localhost:3000/api/channel/

# Create channel
curl -s -X POST -H "Authorization: Bearer $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:3000/api/channel/ \
  -d '{"name":"openai","type":1,"base_url":"https://api.openai.com/v1","key":"sk-...","models":"gpt-4,gpt-3.5-turbo"}'

# Test channel
curl -s -X POST -H "Authorization: Bearer $ADMIN_KEY" \
  http://localhost:3000/api/channel/test/1
```

---

## Brand Replacement

For custom branding (e.g., replacing upstream's brand name):

**Nginx sub_filter approach:**
```nginx
location / {
    proxy_pass http://localhost:3000;
    sub_filter 'OriginalBrand' 'YourBrand';
    sub_filter_once off;
    sub_filter_types text/html text/css application/javascript;
}
```

**Pitfalls:**
- `sub_filter` only works on proxied responses, not static files
- JavaScript-rendered content won't be filtered (use client-side brand-replace.js)
- Cloudflare cache must be purged after changes

---

## PostgreSQL Configuration

```bash
# Environment variable
SQL_DSN="postgres://user:password@localhost:5432/new_api_db"

# Create database
createdb new_api_db

# Migrations run automatically on startup
```

---

## Pitfalls

- **Channel test may pass but generation fails** — test endpoint may not exercise all code paths
- **Model names must match exactly** — upstream providers are case-sensitive
- **Rate multiplier = 1.0 means no markup** — verify before going live
- **Admin key is in .env or environment** — never commit it to git
- **Database backups** — new-api stores all keys and usage data in PostgreSQL
- **Docker Hub rate limits** — use mirror registries for CI/CD pulls
