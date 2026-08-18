# Webflow → React Conversion Checklist

## Phase 1: Asset Setup
1. Copy CSS to `public/css/` (rename to simple name like `cyrclo.css`)
2. Copy JS to `public/js/` (GSAP, jQuery, ScrollTrigger, SplitText, Webflow runtime)
3. Add `<link>` for CSS in `layout.tsx` `<head>`
4. Add `<Script>` tags in `layout.tsx` before `</body>`
5. Add Google Fonts `<link>` if template uses custom fonts

## Phase 2: Component Extraction
1. Identify sections from HTML (navbar, hero, features, pricing, FAQ, footer)
2. Create one component per section: `cyrclo-{section}.tsx`
3. Keep ALL Webflow class names exactly as-is
4. Keep ALL data attributes (data-w-id, data-animation, etc.)
5. Convert HTML→JSX: class→className, for→htmlFor, self-closing tags
6. Replace text content with target language/brand
7. Replace links with app routes
8. Update `index.tsx` to import and render all components

## Phase 3: Auth Integration
1. Import `useAuth` from auth context
2. Replace static nav buttons with conditional rendering
3. Logged in: show "进入工作空间" → /workspace
4. Logged out: show "登录" + "免费开始" → /login

## Phase 4: Build & Fix
1. Run `npm run build`
2. Fix ESLint errors (common: unescaped quotes, unused imports)
3. Fix TypeScript errors (common: JSX element types)
4. Deploy and verify

## Common Pitfalls
- **JSX quotes**: Chinese `"` in text → use `&ldquo;`/`&rdquo;`
- **Unused imports**: Remove `import Link` if not used in component
- **Webflow JS**: May not work perfectly in React - check interactions
- **CSS conflicts**: Cyrclo CSS may conflict with existing Tailwind
- **Font loading**: Add `<link>` to Google Fonts, don't rely on Webflow's webfont.js
