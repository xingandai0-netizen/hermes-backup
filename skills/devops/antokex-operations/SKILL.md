---
name: antokex-operations
description: "antokex.com operations: architecture, deployment, troubleshooting, 502 debugging, SPA routing, brand replacement, admin dashboard, token procurement, and security hardening."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [antokex, api-proxy, new-api, nginx, deployment, troubleshooting, operations]
    related_skills: [new-api-operations, hermes-troubleshooting]
---

# antokex.com Operations

Complete operational guide for antokex.com — an API proxy/reverse-proxy service built on new-api (QuantumNous/new-api).

## When to Use

- Troubleshooting antokex.com issues (502, routing, caching)
- Deploying or modifying the site (Nginx, new-api, brand replacement)
- Managing the admin dashboard
- Optimizing API token procurement and costs
- SPA routing and frontend modifications
- Security hardening

## Architecture Overview

### Current (2026-06-29): Vercel + Railway + Cloudflare

```
Internet → Cloudflare (DNS/CDN) → Vercel (Next.js frontend)
                                       ↓
                                 Railway (FastAPI backend)
```

**Key components:**
- **Vercel:** Next.js frontend, auto-deploy from GitHub
- **Railway:** FastAPI backend with Dockerfile
- **Cloudflare:** DNS (A record → 76.76.21.21), CDN, SSL
- **GitHub:** Source repo at xingandai0-netizen/antoken

**Deployment commands:**
```bash
# Frontend
cd ~/antoken/frontend && vercel --prod --yes

# Backend
cd ~/antoken/backend && railway up --service antoken-backend --detach

# Domain
vercel domains add antokex.com
```

## Architecture Overview (2026-06-29 Updated)

```
Internet → Cloudflare (DNS/CDN/SSL) → Vercel (Next.js frontend)
                                          ↓
                                    Railway (FastAPI backend)
```

**Key components:**
- **Vercel:** Next.js frontend hosting, auto-deploy from GitHub
- **Railway:** FastAPI backend hosting, Docker deployment
- **Cloudflare:** DNS, CDN, SSL termination, caching
- **GitHub:** Source repository, triggers Vercel auto-deploy

**Old Architecture (deprecated):**
```
Internet → Cloudflare → Nginx → new-api (upstream)
```

---

## 2026-06-29 更新：迁移到 Vercel + Railway

antokex.com 已从阿里云 ECS 迁移到 Vercel + Railway 架构：

### 新架构
```
用户 → Cloudflare (DNS/CDN) → Vercel (Next.js 前端)
                                    ↓
                              Railway (FastAPI 后端)
```

### 关键配置
- **Cloudflare SSL**: Full 模式（不能用 Flexible）
- **Vercel 域名**: 需要显式绑定项目 `vercel domains add antokex.com frontend`
- **Railway**: 需要 Dockerfile + Procfile + runtime.txt
- **API Key**: 存在 Railway 环境变量，不暴露给前端

### URL
- 前端: https://antokex.com
- 后端: https://antoken-backend-production.up.railway.app

详见 `antoken-deployment` skill。

## 1. 502 Bad Gateway Troubleshooting

See [references/502-debugging.md](references/502-debugging.md) for the full diagnostic flow.

**Quick diagnosis:**
```bash
# Check upstream health
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/status

# Check Nginx error log
tail -20 /var/log/nginx/error.log

# Check Docker container status
docker ps | grep new-api
docker logs new-api --tail 50
```

**Common root causes:**
- Upstream container not running
- DNS resolution failure for upstream domain
- Nginx config syntax error
- Port conflict

---

## 2. Website Modification and Deployment

See [references/website-modification.md](references/website-modification.md) for the full guide.

**Key areas:**
- **Brand replacement:** Nginx `sub_filter` for changing upstream branding
- **SPA routing:** `try_files $uri $uri/ /index.html` for client-side routing
- **Image management:** Static asset paths, CDN cache busting
- **Static pages:** Admin dashboard, custom landing pages

**Deployment flow:**
1. Edit files on server
2. Test Nginx config: `nginx -t`
3. Reload Nginx: `systemctl reload nginx`
4. Clear Cloudflare cache if needed

---

## 3. SPA Route Fixes

See [references/spa-route-fixes.md](references/spa-route-fixes.md) for the full history.

**Key pitfalls:**
- `brand-replace.js` must sync with i18n locale changes
- `DOMContentLoaded` may not fire if script loads after DOM ready — use `document.readyState` check
- `MutationObserver` can create infinite loops if not properly disconnected
- Internal scroll containers need `overflow: hidden` on parent, not `overflow: visible`
- Cloudflare cache must be purged after static asset changes

---

## 4. Admin Dashboard

See [references/admin-dashboard.md](references/admin-dashboard.md) for the full guide.

- Custom `admin.html` deployed alongside new-api
- Nginx routes `/admin` to custom dashboard (isolated from new-api's built-in admin)
- Admin API interaction for channel/user management
- CSS overrides for brand customization

---

## 5. Token Procurement and Cost Optimization

See [references/token-procurement.md](references/token-procurement.md) for the full strategy.

**Key strategies:**
- B2B wholesale channel research
- GPU self-hosting for high-volume use cases
- Multi-node architecture planning
- Upstream provider comparison and negotiation

---

## 6. Security Hardening

See [references/security-plan.md](references/security-plan.md) for the phased plan.

**4 phases:**
1. **Passive defense:** WAF rules, rate limiting, input validation
2. **Active trapping:** Honeypots, anomaly detection
3. **Attack simulation:** Penetration testing
4. **Continuous monitoring:** Log analysis, alerting

---

## Pitfalls

### Vercel + Railway + Cloudflare Deployment Pitfalls

- **Cloudflare DNS with existing Tunnel records**: If `antokex.com` already has a Tunnel record, you cannot add an A record for `@`. Delete the Tunnel record first, then add A record pointing to `76.76.21.21` (Vercel IP).

- **Cloudflare SSL 525 error**: When using Cloudflare proxy with Vercel, set SSL mode to **Flexible** (not Full or Full Strict). Vercel handles SSL on its end; Cloudflare only needs to proxy HTTP.

- **Railway Python version**: Railway defaults to Python 3.13 which breaks pydantic-core. Create `runtime.txt` with `python-3.11.9` in the backend root.

- **Railway Procfile**: FastAPI needs explicit start command. Create `Procfile` with `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

- **Vercel environment variables**: Backend URL must be set as `NEXT_PUBLIC_API_URL` in Vercel project settings. Without this, frontend will try to connect to localhost:8000.

- **GitHub token auth**: For git push via HTTPS, set remote URL with token: `git remote set-url origin https://USERNAME:TOKEN@github.com/USER/REPO.git`

- **Vercel domain verification**: After adding domain via `vercel domains add`, check with `vercel domains inspect` to see if DNS is properly configured.

### Legacy (Alibaba Cloud + Nginx) Pitfalls

- **Cloudflare cache:** Always purge after deploying static changes. CF caches aggressively.
- **sub_filter scope:** Nginx `sub_filter` only works on proxied responses, not static files served directly.
- **new-api admin vs custom admin:** The custom admin.html is at `/admin`, new-api's built-in admin is at a different path. Don't confuse them.
- **Database migrations:** new-api updates may include PostgreSQL migrations. Always backup before upgrading.
- **Docker Hub rate limits:** Use mirror registries for image pulls in CI/CD.
