# Next.js i18n Pattern (No Library)

Simple client-side i18n for Next.js App Router without next-intl or i18next.

## Architecture

```
src/lib/i18n.ts              # Translations + types
src/components/LanguageSelector.tsx  # Context + dropdown UI
src/app/layout.tsx            # Wrap with I18nProvider
src/app/page.tsx              # useI18n() hook
```

## i18n.ts Structure

```typescript
export type Locale = 'zh-CN' | 'zh-TW' | 'en' | 'ja'

export const locales: Record<Locale, { name: string; flag: string; label: string }> = {
  'zh-CN': { name: '中文', flag: '🇨🇳', label: '简体中文' },
  'zh-TW': { name: '繁體', flag: '🇹🇼', label: '繁體中文' },
  'en': { name: 'EN', flag: '🇺🇸', label: 'English' },
  'ja': { name: '日本語', flag: '🇯🇵', label: '日本語' },
}

export const translations: Record<Locale, Record<string, string>> = {
  'zh-CN': { 'hero.brand': '小算', 'hero.cta': '小算一下', /* ... */ },
  'en': { 'hero.brand': 'Xiao Suan', 'hero.cta': 'Start Reading', /* ... */ },
  // ...
}

export function t(key: string, locale: Locale): string {
  return translations[locale]?.[key] || translations['zh-CN']?.[key] || key
}
```

## Provider Pattern

```tsx
// components/LanguageSelector.tsx
const I18nContext = createContext({ locale: 'zh-CN', setLocale: () => {}, t: (k: string) => k })

export function I18nProvider({ children }) {
  const [locale, setLocale] = useState<Locale>('zh-CN')
  useEffect(() => {
    const saved = localStorage.getItem('locale') as Locale
    if (saved && locales[saved]) setLocale(saved)
  }, [])
  const handleSet = (l: Locale) => { setLocale(l); localStorage.setItem('locale', l) }
  const t = (key: string) => translate(key, locale)
  return <I18nContext.Provider value={{ locale, setLocale: handleSet, t }}>{children}</I18nContext.Provider>
}

export function useI18n() { return useContext(I18nContext) }
```

## Layout Integration

```tsx
// app/layout.tsx
import { I18nProvider } from '@/components/LanguageSelector'
export default function RootLayout({ children }) {
  return <html><body><I18nProvider>{children}</I18nProvider></body></html>
}
```

## Usage in Pages

```tsx
'use client'
import { useI18n, LanguageSelector } from '@/components/LanguageSelector'

export default function Home() {
  const { t } = useI18n()
  return (
    <nav><LanguageSelector /></nav>
    <h1>{t('hero.brand')}</h1>
  )
}
```

## Key Notes

- No SSR support — `useEffect` + `localStorage` for persistence
- Traditional culture terms (五行, 九宫, 八卦) typically stay in Chinese across all locales
- Language selector uses globe icon (🌐) + current locale name + dropdown arrow
