# Next.js 14 App Router Pitfalls

## Critical: Cannot use `<head>` tag in layout.tsx

**Symptom:** White screen / 500 error after adding `<head>` tag to layout.tsx

**Cause:** Next.js App Router manages `<head>` internally. Adding a `<head>` JSX element inside the layout component causes a server-side error.

**Fix:** Remove the `<head>` tag. Use Next.js metadata API instead:
```typescript
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
}
```

For external stylesheets, add them in `globals.css` or use `next/head` in individual pages (Pages Router only).

---

## Critical: `.next` directory corruption causes persistent 404

**Symptom:** Dev server returns 404 for all routes, even after restart. Error page shows "Pages Router" style instead of "App Router" style.

**Cause:** Corrupted `.next` build manifest files from previous failed builds or killed processes.

**Fix:**
```bash
# 1. Kill ALL Next.js processes
pkill -f "next dev"
pkill -f "next-server"

# 2. Clean .next directory
rm -rf .next

# 3. Restart dev server
npm run dev
```

**Prevention:** Always kill processes cleanly before restarting. Don't use Ctrl+C multiple times.

---

## Critical: Multiple dev servers conflict on same port

**Symptom:** 404 errors, stale content, or "missing required error components" message.

**Cause:** Multiple `next dev` processes running simultaneously, or old `next-server` processes still holding port 3000.

**Diagnosis:**
```bash
# Check what's on port 3000
lsof -i :3000

# Check for multiple Next.js processes
ps aux | grep "next dev" | grep -v grep
ps aux | grep "next-server" | grep -v grep
```

**Fix:**
```bash
# Kill all Next.js processes
pkill -9 -f "next dev"
pkill -9 -f "next-server"

# Wait for port to release
sleep 2

# Restart
npm run dev
```

---

## Floating point array indices cause undefined

**Symptom:** UI shows "undefinedundefined" instead of expected values.

**Cause:** JavaScript array indices must be integers. Using floating point division (`/`) in index calculations produces non-integer values.

**Bad:**
```typescript
const index = (year / 4 + month * 30 + day) % 10  // Float!
const value = dataArray[index]  // undefined
```

**Good:**
```typescript
const index = Math.floor((year / 4 + month * 30 + day)) % 10  // Integer
const value = dataArray[index]  // Works
```

**Rule:** Always use `Math.floor()` when using division in array index calculations.

---

## Dev server takes time to compile

**Symptom:** First request returns 404 or "missing required error components" message.

**Cause:** Next.js dev server needs time to compile pages on first request.

**Fix:** Wait 10-15 seconds after starting dev server before checking. The server will auto-reload when compilation completes.

**Pattern:**
```bash
# Start server in background
npm run dev &

# Wait for compilation
sleep 15

# Then check
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
```
