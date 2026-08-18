# shadcn/ui + Tailwind v4 Setup Pitfalls

## Version Compatibility

| shadcn/ui | Tailwind | Status |
|-----------|----------|--------|
| 4.x | v4 | ✅ Required |
| 4.x | v3 | ❌ `border-border` class not found |
| 0.x (legacy) | v3 | ✅ Old format |

## Common Errors

### 1. `border-border` class does not exist

**Error**: `The 'border-border' class does not exist. If 'border-border' is a custom class, make sure it is defined within a @layer directive.`

**Cause**: Tailwind v4 doesn't support `@apply` with CSS variable-based utility classes the same way v3 does.

**Fix**: Replace `@apply` with direct CSS in globals.css:
```css
/* ❌ */
* { @apply border-border outline-ring/50; }
body { @apply bg-background text-foreground; }
html { @apply font-sans; }

/* ✅ */
* { border-color: var(--border); outline-color: var(--ring); }
body { background-color: var(--background); color: var(--foreground); }
html { font-family: var(--font-sans, system-ui, sans-serif); }
```

### 2. PostCSS config must use `@tailwindcss/postcss`

**Old (v3)**:
```js
export default { plugins: { tailwindcss: {} } };
```

**New (v4)**:
```js
export default { plugins: { "@tailwindcss/postcss": {} } };
```

### 3. CSS import syntax

**Old (v3)**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**New (v4)**:
```css
@import "tailwindcss";
```

### 4. `@import "shadcn/tailwind.css"` required

shadcn/ui 4.x adds this import to globals.css. It provides the CSS variable definitions for the design system. Don't remove it.

## Installation Steps

```bash
# 1. Create Next.js project
npx create-next-app@14 frontend --typescript --tailwind --eslint --app --src-dir

# 2. Initialize shadcn/ui (this installs Tailwind v4 automatically)
cd frontend
npx shadcn@latest init -d

# 3. Add components
npx shadcn@latest add button card dialog input select badge tabs textarea

# 4. Install animation deps
npm install framer-motion

# 5. Fix PostCSS if needed
# Ensure postcss.config.mjs uses "@tailwindcss/postcss" not "tailwindcss"

# 6. Fix globals.css if needed
# Replace @apply border-border etc. with direct CSS

# 7. Build and verify
npm run build
```

## Dark Theme

shadcn/ui provides dark theme CSS variables out of the box. The `.dark` class on `<html>` activates dark mode:

```tsx
<html lang="zh-CN" className="dark">
```

CSS variables are defined in globals.css under `.dark { ... }` block.
