# 卦气值日算法详解

## 算法来源

汉代孟喜「卦气说」，正统易学体系。

**核心原理**：
- 64卦中去掉乾坤坎离四正卦，剩余60卦
- 60卦分配到一年365天
- 每卦主管约6天（"六日七分说"）
- 从冬至开始，复卦为首卦

**古籍依据**：
- 《周易章句》（孟喜）
- 《京氏易传》（京房）
- 《新唐书》卷二十七（僧一行《卦义》）

## 算法实现

### 卦气值日序列（60卦）

```typescript
const GUAQI_SEQUENCE = [
  // 子月（农历十一月）- 冬至开始
  24, 27, 3, 42, 51, 21, 17, 25, 36, 22,
  // 丑月（农历十二月）
  63, 37, 55, 49, 13, 19, 41, 60, 61, 54,
  // 寅月（农历正月）
  38, 58, 10, 11, 26, 5, 9, 34, 14, 43,
  // 卯月（农历二月）
  44, 32, 50, 28, 48, 18, 46, 6, 47, 64,
  // 辰月（农历三月）
  40, 59, 4, 7, 33, 31, 56, 62, 53, 39,
  // 巳月（农历四月）
  52, 15, 12, 45, 35, 16, 20, 8, 23, 2
]
```

### 计算逻辑

```typescript
export function getDailyHexagram(date: Date = new Date()) {
  const year = date.getFullYear()
  
  // 获取今年冬至（12月21日）
  const winterSolstice = new Date(year, 11, 21)
  
  // 如果当前日期在今年冬至之前，用去年冬至
  let startDate: Date
  if (date < winterSolstice) {
    startDate = new Date(year - 1, 11, 21)
  } else {
    startDate = winterSolstice
  }
  
  // 计算从冬至开始的天数
  const daysFromStart = Math.floor(
    Math.abs((date.getTime() - startDate.getTime()) / (24 * 60 * 60 * 1000))
  )
  
  // 每卦主管6天，计算今日是第几个卦
  const hexagramIndex = Math.floor(daysFromStart / 6) % 60
  
  // 获取对应的卦序号
  const hexagramNumber = GUAQI_SEQUENCE[hexagramIndex]
  
  return {
    hexagram: HEXAGRAMS[hexagramNumber],
    dayIndex: daysFromStart,
    // ...
  }
}
```

## 验证结果（2026-07-15）

```
2026-07-14: 第206天, 序列第34个, 卦象: 水风井 (48号)
2026-07-15: 第207天, 序列第34个, 卦象: 水风井 (48号)
2026-07-19: 第211天, 序列第35个, 卦象: 山风蛊 (18号)
2026-07-20: 第212天, 序列第35个, 卦象: 山风蛊 (18号)
2026-07-31: 第223天, 序列第37个, 卦象: 天水讼 (6号)
```

**结论**：
- ✓ 每天都根据日期计算
- ✓ 每6天换一个卦象
- ✓ 不是随机，是固定算法
- ✓ 今天和明天一样（因为同属一个6天周期）

## 64卦数据结构

每卦需要包含以下字段：

```typescript
{
  name: '地天泰',           // 卦名
  symbol: '䷊',            // 卦象符号
  upper: '坤',             // 上卦
  lower: '乾',             // 下卦
  judgment: '小往大来，吉亨', // 卦辞
  fortune: '大吉',         // 吉凶等级
  goodFor: ['一切事宜'],    // 宜
  badFor: [],              // 忌
  advice: '今日大吉大利...', // 建议
  meaning: '泰卦象征...',   // 卦意
  yaoCi: '初九：...',       // 爻辞
  xiang: '天地交泰...',     // 象辞
  guaDe: '泰，小往大来...', // 卦德
  tiShi: '今日适合...'      // 人事提示
}
```

## 与梅花易数的区别

| 特性 | 卦气值日 | 梅花易数 |
|------|----------|----------|
| 用途 | 看日子吉凶 | 推测具体事情 |
| 起卦方式 | 根据日期自动计算 | 需要用户输入（时间/数字/方位） |
| 古籍来源 | 汉代孟喜「卦气说」 | 北宋邵雍《梅花易数》 |
| 每日一卦 | ✓ 适合 | ✗ 不适合（用于占卜） |
| 结果 | 当日整体吉凶 | 具体事情的预测 |

## UI实现要点

**⚠️ 用户明确要求**：
1. "不要红绿分栏" - 宜忌用标签样式，不用绿色/红色分栏
2. "这个要一直白着，不受渐变黑影响" - 固定浅色背景(#f5f0e8)
3. 所有文字颜色固定（深棕/棕色系），不随滚动变化

**推荐实现**：
```tsx
<section className="py-20 px-6" style={{ backgroundColor: '#f5f0e8' }}>
  <div className="rounded-2xl p-8" style={{ backgroundColor: '#fff', border: '1px solid #e5ddd0' }}>
    {/* 宜忌用标签样式 */}
    <div className="flex flex-wrap gap-2">
      {hexagram.goodFor.map((item, i) => (
        <span key={i} className="text-xs px-2 py-1 rounded" 
          style={{ backgroundColor: '#f5f0e8', color: '#6b5b4b' }}>
          {item}
        </span>
      ))}
    </div>
  </div>
</section>
```
