# 语言选择器自定义模式（已验证）

## 去除地球图标

阿戴要求语言选择器简洁，不要地球图标：

```tsx
// ❌ 有图标
<span className="text-sm">🌐</span>
<span className="text-sm">{currentLocale.name}</span>

// ✅ 无图标，只显示语言名
<span className="text-sm" style={{ color }}>{currentLocale.name}</span>
```

## 动态颜色传递

当页面有滚动渐变效果时，语言选择器颜色也需要随滚动变化：

```tsx
// LanguageSelector.tsx - 接受color属性
export function LanguageSelector({ color = '#111827' }: { color?: string }) {
  // ...
  <span className="text-sm" style={{ color }}>{currentLocale.name}</span>
  // ...
}

// page.tsx - 传递动态颜色
<LanguageSelector color={textColor900} />
```

## 阿戴的UI简化偏好（反复出现）

**模式**：阿戴会反复要求删除装饰性元素

常见删除请求：
- 删除地球图标（🌐）
- 删除按钮旁的表情包（🎋）
- 删除按钮箭头（→）
- 删除装饰性标签（如"东方命理，云海问卦"）
- 删除小道童动画

**规则**：当用户说"删了"或"这个删了"，立即执行，不要问为什么。

## 品牌命名最终状态

| 元素 | 最终值 | 备注 |
|------|--------|------|
| Logo | 安 | 圆形按钮中的书法字 |
| 品牌名 | 小算 | 导航栏显示 |
| 主标题 | 小算 | 页面中心大字 |
| 主按钮 | 小算一下 | 无箭头（曾有→） |
| 次按钮 | 每日一签 | 无表情包（曾有🎋） |
| 标语 | 已删除 | 曾有"东方命理，云海问卦" |

## 品牌命名变更历史

1. 算了么 → 小算一下（阿戴要求改名）
2. 小算一下 → 小算（品牌名简化）
3. 按钮"小算一下 →" → "小算一下"（删除箭头）
4. 按钮"🎋 每日一签" → "每日一签"（删除表情包）

**教训**：品牌名和按钮文字要分开管理，不要混用。
