# Vercel + Railway + Cloudflare Deployment Guide

## Architecture

```
Internet → Cloudflare (DNS/CDN) → Vercel (Next.js frontend)
                                       ↓
                                 Railway (FastAPI backend)
```

## Prerequisites

- GitHub account with repo: `xingandai0-netizen/antoken`
- Vercel account (login via GitHub)
- Railway account (login via GitHub)
- Cloudflare account with `antokex.com` domain

## Step 1: Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy frontend
cd ~/antoken/frontend
vercel --prod --yes

# Add custom domain
vercel domains add antokex.com

# Set environment variable
echo "https://antoken-backend-production.up.railway.app" | vercel env add NEXT_PUBLIC_API_URL production

# Redeploy with env var
vercel --prod --yes
```

## Step 2: Deploy Backend to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
cd ~/antoken/backend
railway init --name antoken-backend

# Deploy
railway up --service antoken-backend --detach

# Get domain
railway domain
```

### Backend Configuration Files

**Procfile** (required):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**runtime.txt** (required - Python 3.11):
```
python-3.11.9
```

**Dockerfile** (optional, more control):
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

## Step 3: Configure Cloudflare DNS

1. Login to Cloudflare dashboard
2. Select `antokex.com` domain
3. Go to DNS → Records
4. Delete any existing Tunnel records for `@`
5. Add A record:
   - Name: `@`
   - IPv4 address: `76.76.21.21`
   - Proxy status: Proxied (orange cloud)
   - TTL: Auto

## Step 4: Configure Cloudflare SSL

1. Go to SSL/TLS → Overview
2. Set SSL mode to **Flexible** (not Full)
3. Wait 5-10 minutes for Vercel SSL certificate

## Environment Variables

### Vercel
```
NEXT_PUBLIC_API_URL=https://antoken-backend-production.up.railway.app
```

### Railway
No special environment variables needed for basic setup.

## Verification

```bash
# Check frontend
curl -s -o /dev/null -w "%{http_code}" https://antokex.com
# Should return 200

# Check backend
curl -s -o /dev/null -w "%{http_code}" https://antoken-backend-production.up.railway.app/docs
# Should return 200

# Check DNS
nslookup antokex.com
# Should show Cloudflare IPs (104.21.x.x, 172.67.x.x)
```

## Common Issues

### SSL 525 Error
**Symptom**: Cloudflare shows "SSL handshake failed"
**Fix**: Change Cloudflare SSL mode to "Flexible"

### DNS Not Resolving
**Symptom**: `nslookup` returns no results
**Fix**: Wait 5-30 minutes for DNS propagation

### Backend Build Failure
**Symptom**: Railway shows "Failed" status
**Fix**: Check logs with `railway logs --service antoken-backend`
- Python version issue: Add `runtime.txt` with `python-3.11.9`
- Missing Procfile: Add `Procfile` with start command

### Frontend Can't Connect to Backend
**Symptom**: API calls fail in browser console
**Fix**: 
1. Check `NEXT_PUBLIC_API_URL` is set in Vercel
2. Redeploy frontend after setting env var

## Update Deployment

### Frontend
```bash
cd ~/antoken/frontend
git push  # Vercel auto-deploys from GitHub
```

### Backend
```bash
cd ~/antoken/backend
railway up --service antoken-backend --detach
```

## Cost

- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: Free tier ($5 credit/month)
- **Cloudflare**: Free plan
- **Total**: $0/month for small projects
