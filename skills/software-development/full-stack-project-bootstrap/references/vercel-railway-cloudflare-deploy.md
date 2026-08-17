# Vercel + Railway + Cloudflare Deployment

Complete deployment guide for Next.js frontend + FastAPI backend with custom domain.

## Architecture

```
User → Cloudflare (DNS/CDN) → Vercel (Next.js frontend)
                                    ↓
                              FastAPI backend (Railway)
```

## When to Use
- Next.js frontend + FastAPI backend
- Need custom domain
- Don't want to manage servers

## Key Steps

### 1. GitHub Push
```bash
cd ~/project
git add -A && git commit -m "deploy"
# If gh auth fails, use token directly
git remote set-url origin https://USERNAME:TOKEN@github.com/USER/REPO.git
git push origin main
```

**Pitfall**: `gh auth login` often fails. Using token in remote URL is more reliable.

### 2. Vercel Deploy Frontend
```bash
npm install -g vercel
# CLI at ~/.hermes/node/bin/vercel, not in PATH

~/.hermes/node/bin/vercel login --github
cd frontend
~/.hermes/node/bin/vercel --prod --yes

# Add env vars
~/.hermes/node/bin/vercel link --yes
echo "VALUE" | ~/.hermes/node/bin/vercel env add KEY production

# Add domain
~/.hermes/node/bin/vercel domains add example.com
```

**Pitfalls**:
- Vercel CLI installs to `~/.hermes/node/bin/`, not in PATH
- `vercel login` needs browser auth, 60s timeout
- `NEXT_PUBLIC_` vars need redeployment to take effect
- After adding domain, configure DNS (A record → 76.76.21.21)

### 3. Railway Deploy Backend
```bash
npm install -g @railway/cli
~/.hermes/node/bin/railway login
cd backend
~/.hermes/node/bin/railway init --name PROJECT_NAME
~/.hermes/node/bin/railway up --service SERVICE_NAME --detach
~/.hermes/node/bin/railway domain
```

**Pitfalls**:
- Python projects need `Procfile` or `Dockerfile`
- Railway defaults to Python 3.13, pydantic-core incompatible
- Fix: create `runtime.txt` with `python-3.11.9`
- Or use Dockerfile: `FROM python:3.11-slim`

### 4. Cloudflare DNS
```bash
# API Token needs Zone:DNS:Edit permission
curl -s "https://api.cloudflare.com/client/v4/zones?name=DOMAIN" \
  -H "Authorization: Bearer TOKEN"

# Add A record
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"@","content":"76.76.21.21","ttl":1,"proxied":true}'
```

**Pitfalls**:
- API Token must start with `cfat_` (not `ghp_`)
- Domain must be added to Cloudflare account first
- Vercel A record IP is `76.76.21.21`
- DNS propagation can take up to 24 hours

## FastAPI Backend Config

### Procfile
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Dockerfile (recommended)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### runtime.txt
```
python-3.11.9
```

### CORS Config
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Frontend API Address Config

```typescript
// src/lib/api.ts
export function getApiBase(): string {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location;
    if (hostname === 'your-domain.com') {
      return process.env.NEXT_PUBLIC_API_URL || '';
    }
    return `${protocol}//${hostname}:8000`;
  }
  return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
}
```

## Verification Checklist

- [ ] GitHub push successful
- [ ] Vercel build successful (check build log)
- [ ] Railway build successful (check logs)
- [ ] Environment variables set (NEXT_PUBLIC_API_URL)
- [ ] Frontend URL accessible
- [ ] Backend URL accessible (/docs)
- [ ] DNS A record added
- [ ] Custom domain accessible
- [ ] API calls work (frontend→backend)

## SSL Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| Flexible | CF → HTTP → Origin | ❌ Causes redirect loops with Vercel |
| **Full** | CF → HTTPS → Origin | ✅ Recommended |
| Full (Strict) | CF → HTTPS → Valid Cert | ✅ When origin has valid cert |

## Deployment Verification

```bash
# DNS resolution
nslookup antokex.com

# Vercel deployment
vercel ls

# Railway status
railway status

# API test
curl https://backend.railway.app/docs

# Frontend→backend communication
curl -s https://your-domain.com/api/health
```

## Cost
- Vercel: Free tier sufficient for personal projects
- Railway: Free $5/month credit
- Cloudflare: Free plan
- Total: $0/month (within free tiers)
