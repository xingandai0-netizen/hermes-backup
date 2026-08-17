# Antoken Deployment Reference (2026-06-29)

## Actual Deployment Details

### URLs
- **Frontend**: https://frontend-zeta-dun-89.vercel.app
- **Backend**: https://antoken-backend-production.up.railway.app
- **Target Domain**: antokex.com (DNS not yet configured)

### Vercel Project
- Project: xingandai0-netizens-projects/frontend
- Root Directory: `frontend`
- Framework: Next.js
- Environment Variable: `NEXT_PUBLIC_API_URL=https://antoken-backend-production.up.railway.app`

### Railway Project
- Project: antoken-backend (ID: 3235bbf0-afe4-47e8-b773-1a65bcd0138f)
- Service: antoken-backend (ID: 967aa6d0-01fc-471a-a7e6-1e196f098df7)
- Region: sfo
- Domain: https://antoken-backend-production.up.railway.app

### GitHub
- Repo: xingandai0-netizen/antoken
- Auth: Token in remote URL (gh auth login keeps failing)

### Cloudflare
- Domain: antokex.com
- Zone: NOT YET ADDED to the Cloudflare account
- Required DNS: A record @ → 76.76.21.21 (Vercel IP)

## Issues Encountered

1. **gh auth login keeps failing** - Token expires or doesn't persist. Solution: embed token in git remote URL.
2. **Railway Python 3.13 incompatibility** - pydantic-core fails to build. Solution: use Dockerfile with python:3.11-slim.
3. **Railway Procfile not detected** - Railpack doesn't auto-detect FastAPI. Solution: use Dockerfile instead.
4. **Cloudflare zone not found** - Domain must be added to Cloudflare account before API can manage DNS.
5. **Vercel CLI not in PATH** - Installed to ~/.hermes/node/bin/vercel.

## Pending

- [ ] Add antokex.com to Cloudflare account
- [ ] Configure A record → 76.76.21.21
- [ ] Verify domain works at https://antokex.com
