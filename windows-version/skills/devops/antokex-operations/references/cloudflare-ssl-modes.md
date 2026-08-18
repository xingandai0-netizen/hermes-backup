# Cloudflare SSL/TLS Configuration for Vercel

## SSL Modes

| Mode | Cloudflare → Origin | Use Case |
|------|---------------------|----------|
| **Off** | No encryption | ❌ Never use |
| **Flexible** | HTTP | ❌ Causes redirect loops with Vercel |
| **Full** | HTTPS (any cert) | ✅ Works with Vercel |
| **Full (Strict)** | HTTPS (valid cert only) | ✅ When Vercel cert issued |

## Common Errors

### 525 SSL Handshake Failed
**Symptoms:** Browser shows "SSL handshake failed Error code 525"
**Cause:** Cloudflare can't establish SSL to origin
**Fix:**
1. Change SSL mode to "Full" (not "Full (Strict)")
2. Wait 5-10 minutes for Vercel to issue certificate
3. Can change back to "Full (Strict)" after certificate issued

### ERR_TOO_MANY_REDIRECTS
**Symptoms:** Browser shows redirect loop error
**Cause:** SSL mode set to "Flexible"
- Cloudflare connects via HTTP
- Vercel redirects to HTTPS
- Cloudflare connects via HTTP again
- Loop continues
**Fix:** Change SSL mode to "Full"

### 404 NOT_FOUND (Vercel)
**Symptoms:** Vercel returns 404 page
**Cause:** Domain not attached to Vercel project
**Fix:**
```bash
vercel domains add antokex.com frontend
```

## DNS Configuration

### A Record (for root domain)
```
Type: A
Name: @
Content: 76.76.21.21
Proxy: Enabled (orange cloud)
TTL: Auto
```

### CNAME Record (for subdomain)
```
Type: CNAME
Name: www
Content: cname.vercel-dns.com
Proxy: Enabled (orange cloud)
TTL: Auto
```

## Verification Commands

```bash
# Check DNS resolution
nslookup antokex.com

# Check SSL certificate
curl -vI https://antokex.com 2>&1 | grep -i "ssl\|certificate"

# Check Vercel domain status
vercel domains inspect antokex.com

# Verify domain attached to project
vercel domains verify antokex.com
```

## Vercel Domain Commands

```bash
# Add domain to project
vercel domains add antokex.com <project-name>

# List domains
vercel domains ls

# Remove domain
vercel domains rm antokex.com

# Check domain status
vercel domains inspect antokex.com
```
