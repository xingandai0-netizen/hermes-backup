# i18n 多语言支持实现

## 架构

```
src/lib/i18n.ts          ← 语言配置 + 翻译文本 + t()函数
src/components/LanguageSelector.tsx  ← I18nProvider + 下拉选择器
src/app/layout.tsx       ← 包裹I18nProvider
```

## 翻译key命名规范

```
nav.home, nav.tools, nav.daily, nav.books, nav.calendar, nav.login
hero.brand, hero.pinyin, hero.slogan, hero.desc, hero.cta, hero.daily
features.title, features.desc, features.tools, features.books, features.tarot, features.all
tool.sanshu, tool.sanshu.desc, tool.liuren, tool.liuren.desc, ...
guide.title, guide.subtitle, guide.desc, guide.step1-4, guide.step1-4.desc, guide.motto
daily.title, daily.today, daily.desc, daily.ben, daily.bian, daily.reminder, daily.open
knowledge.title, knowledge.subtitle, knowledge.desc, knowledge.wuxing, ...
quote.title, quote.change
about.title, about.subtitle, about.free, about.desc, about.more
footer.brand, footer.disclaimer, footer.tools, footer.books, ...
```

## 传统文化专有名词处理

英文/日文模式下，以下术语保留中文：
- 五行、九宫、八卦
- 天干、地支
- 节气名称
- 签文内容
- 道藏话语

## localStorage key

```typescript
localStorage.getItem('locale')  // 'zh-CN' | 'zh-TW' | 'en' | 'ja'
```

## 下拉菜单UI

```tsx
<button onClick={() => setIsOpen(!isOpen)}>
  <span>🌐</span>
  <span>{currentLocale.name}</span>
  <svg className={isOpen ? 'rotate-180' : ''}>▼</svg>
</button>

{isOpen && (
  <div className="absolute right-0 mt-2 w-48 bg-white/95 backdrop-blur-xl rounded-xl shadow-2xl">
    {Object.entries(locales).map(([key, config]) => (
      <button onClick={() => setLocale(key)}>
        <span>{config.flag}</span>
        <span>{config.label}</span>
      </button>
    ))}
  </div>
)}
```
