# Next.js 14 + Supabase Auth Integration

Complete guide for adding authentication to Next.js 14 (App Router) projects with Supabase.

## When to Use
- Adding login/register to an existing Next.js 14 project
- Need GitHub/Google/email-password authentication
- Want route protection (redirect unauthenticated users)

## Prerequisites
- Supabase project at https://supabase.com/dashboard
- Supabase URL and anon key (JWT format `eyJ...`, NOT `sb_publishable_...`)
- GitHub OAuth App (for GitHub login)

## Step-by-Step

### 1. Install Dependencies
```bash
npm install @supabase/supabase-js
```

### 2. Environment Variables (.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
```

⚠️ **Pitfall**: `sb_publishable_*` keys do NOT work with `@supabase/supabase-js`. Use JWT anon key from Dashboard → Settings → API → `anon` `public`.

### 3. Supabase Client (`src/lib/supabase.ts`)
```typescript
import { createClient } from '@supabase/supabase-js';
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### 4. Auth Context (`src/contexts/AuthContext.tsx`)
- Create `AuthProvider` with `useState` for `user`, `session`, `loading`
- `useEffect` → `supabase.auth.getSession()` + `onAuthStateChange` listener
- Expose: `signInWithGitHub`, `signInWithGoogle`, `signInWithEmail`, `signUpWithEmail`, `signOut`
- Export `useAuth()` hook

### 5. Providers Wrapper (`src/components/Providers.tsx`)
```tsx
"use client";
import { AuthProvider } from "@/contexts/AuthContext";
export default function Providers({ children }: { children: React.ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}
```

### 6. Wrap Layout (`src/app/layout.tsx`)
```tsx
import Providers from "@/components/Providers";
// ...
<body><Providers>{children}</Providers></body>
```

⚠️ **Pitfall**: `layout.tsx` is a Server Component. AuthProvider is a Client Component. Must use separate `Providers.tsx` wrapper.

### 7. OAuth Callback (`src/app/auth/callback/route.ts`)
```typescript
import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  if (code) {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    );
    await supabase.auth.exchangeCodeForSession(code);
  }
  return NextResponse.redirect(`${origin}/workspace`);
}
```

### 8. Login Page (`src/app/login/page.tsx`)
- GitHub button → `signInWithGitHub()`
- Email/password form → `signInWithEmail()` / `signUpWithEmail()`
- Toggle between login/register modes
- If already logged in, redirect to workspace

### 9. Route Protection
```tsx
const { user, loading } = useAuth();
const router = useRouter();
useEffect(() => {
  if (!loading && !user) router.replace("/login");
}, [loading, user, router]);
if (loading || !user) return null;
```

## GitHub OAuth Setup
1. Go to https://github.com/settings/developers
2. New OAuth App
3. **Homepage URL**: `http://localhost:3000` (local) or your domain
4. **Authorization callback URL**: `https://<project-ref>.supabase.co/auth/v1/callback`
5. Copy Client ID and Client Secret
6. Supabase Dashboard → Authentication → Providers → GitHub → Enable → Paste credentials → Save

## Deployment Pitfalls

### Vercel: "supabaseUrl is required"
Supabase env vars must be set in Vercel project settings (Settings → Environment Variables). `.env.local` is NOT uploaded.

### Supabase Key Format
- `eyJ...` (JWT) — works with `@supabase/supabase-js` ✅
- `sb_publishable_...` — works with REST API but NOT with JS client ❌

### getSession() Causes Loading Stall
If navbar buttons never show (loading always true), check:
1. Supabase URL/Key correctness
2. Browser can reach Supabase (test with `fetch`)
3. Key format not truncated

### Type Conflicts
`e.target as Node` conflicts with React Flow's `Node` type. Use `globalThis.Node` instead.

## File Checklist
```
src/lib/supabase.ts              # Client
src/contexts/AuthContext.tsx      # Auth state
src/components/Providers.tsx      # Client wrapper
src/app/layout.tsx                # Wrap with Providers
src/app/auth/callback/route.ts    # OAuth callback
src/app/login/page.tsx            # Login UI
src/app/workspace/page.tsx        # Route protection
.env.local                        # Supabase URL + key
```
