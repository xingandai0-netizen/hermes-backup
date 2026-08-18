# Cloudflare DNS Configuration Guide

## Common DNS Record Types

| Type | Name | Content | Use Case |
|------|------|---------|----------|
| A | @ | 76.76.21.21 | Root domain → IP |
| CNAME | www | example.com | WWW subdomain |
| CNAME | * | example.com | Wildcard subdomain |

## Adding A Record for Vercel

1. Login to Cloudflare dashboard
2. Select domain (e.g., `antokex.com`)
3. Go to DNS → Records
4. Click "Add record"
5. Configure:
   - Type: A
   - Name: @ (for root domain)
   - IPv4 address: 76.76.21.21 (Vercel IP)
   - Proxy status: Proxied (orange cloud)
   - TTL: Auto
6. Click Save

## Common Issues

### "A CNAME record with that host already exists"

**Cause**: There's already a CNAME or Tunnel record for the same name.

**Fix**:
1. Find the existing record (usually a Tunnel record)
2. Delete it first
3. Then add the new A record

### SSL 525 Error

**Symptom**: "SSL handshake failed" when accessing site

**Cause**: Cloudflare SSL mode is "Full" or "Full (Strict)" but origin doesn't have valid SSL.

**Fix**:
1. Go to SSL/TLS → Overview
2. Change mode to "Flexible"
3. Wait 5-10 minutes

### DNS Not Propagating

**Symptom**: `nslookup` returns no results or old IP

**Fix**:
- Wait 5-30 minutes for propagation
- Try different DNS server: `nslookup antokex.com 8.8.8.8`
- Clear local DNS cache: `sudo dscacheutil -flushcache`

## Cloudflare API Token Issues

### "Invalid format for Authorization header"

**Cause**: Token format is wrong or token is invalid.

**Fix**:
1. Create new token at https://dash.cloudflare.com/profile/api-tokens
2. Use "Custom token" template
3. Set permissions: Zone:DNS:Edit
4. Set zone: antokex.com
5. Copy token immediately (only shown once)

### "No zones found"

**Cause**: Token doesn't have access to the zone.

**Fix**:
1. Check token permissions include the correct zone
2. Or use Global API Key instead of token

## DNS Verification Commands

```bash
# Check DNS resolution
nslookup antokex.com

# Check with specific DNS server
nslookup antokex.com 8.8.8.8

# Check HTTP response
curl -s -o /dev/null -w "%{http_code}" https://antokex.com

# Check SSL certificate
curl -vI https://antokex.com 2>&1 | grep -i "ssl\|certificate"
```
