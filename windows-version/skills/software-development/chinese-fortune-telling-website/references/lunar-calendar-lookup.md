# 农历查表法参考

## 为什么需要查表法

农历是基于天文观测的阴阳历，不是简单的数学公式能算出来的。农历的月份是根据月亮运行周期确定的，每年的农历日期都不同。

**禁止使用简化数学公式**，如：
```typescript
// ❌ 完全错误
const lunarMonth = (month + 1 + 12) % 12
const lunarDay = day
```

## 正确做法

### 方法1：使用lunar-javascript库（推荐）

```typescript
import { Solar } from 'lunar-javascript'

const solar = Solar.fromDate(new Date())
const lunar = solar.getLunar()

lunar.getDayInChinese()      // "初二"
lunar.getMonthInChinese()    // "六"
lunar.getYearInGanZhi()      // "丙午"
lunar.getYearShengXiao()     // "马"
```

### 方法2：查表法（当无法使用库时）

对于特定年份，可以使用查表法。以下是2026年7月的农历数据：

```typescript
const lunarData2026: Record<string, { month: string, day: string }> = {
  '7-1': { month: '五', day: '十七' },
  '7-2': { month: '五', day: '十八' },
  '7-3': { month: '五', day: '十九' },
  '7-4': { month: '五', day: '二十' },
  '7-5': { month: '五', day: '廿一' },
  '7-6': { month: '五', day: '廿二' },
  '7-7': { month: '五', day: '廿三' },
  '7-8': { month: '五', day: '廿四' },
  '7-9': { month: '五', day: '廿五' },
  '7-10': { month: '五', day: '廿六' },
  '7-11': { month: '五', day: '廿七' },
  '7-12': { month: '五', day: '廿八' },
  '7-13': { month: '五', day: '廿九' },
  '7-14': { month: '六', day: '初一' },
  '7-15': { month: '六', day: '初二' },
  '7-16': { month: '六', day: '初三' },
  '7-17': { month: '六', day: '初四' },
  '7-18': { month: '六', day: '初五' },
  '7-19': { month: '六', day: '初六' },
  '7-20': { month: '六', day: '初七' },
  '7-21': { month: '六', day: '初八' },
  '7-22': { month: '六', day: '初九' },
  '7-23': { month: '六', day: '初十' },
  '7-24': { month: '六', day: '十一' },
  '7-25': { month: '六', day: '十二' },
  '7-26': { month: '六', day: '十三' },
  '7-27': { month: '六', day: '十四' },
  '7-28': { month: '六', day: '十五' },
  '7-29': { month: '六', day: '十六' },
  '7-30': { month: '六', day: '十七' },
  '7-31': { month: '六', day: '十八' },
}
```

## 干支计算

### 2026年7月15日的干支

- 干支年：丙午年（2026-1900=126, 126%10=6=庚, 126%12=6=午）
- 干支月：乙未月
- 干支日：庚寅日
- 生肖：马
- 五行：水（丙午年纳音天河水）

## 数据来源

农历数据需要从权威来源获取：
1. 万年历网站（如 rili.com.cn）
2. 专业农历库（lunar-javascript）
3. 天文算法

**⚠️ 警告**：绝对不能使用简化数学公式计算农历，会导致日期完全错误，引起用户极度不满。
