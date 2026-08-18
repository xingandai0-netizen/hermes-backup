# lunar-javascript 在 Next.js 中的使用

> 创建日期：2026-07-08
> 基于项目：小算 v2 (/Users/macpro/xiaosuan-v2)

## 安装

```bash
npm install lunar-javascript
```

## 基础用法

```typescript
'use client'
import { Solar, Lunar } from 'lunar-javascript'

// 从Date对象创建
const solar = Solar.fromDate(new Date())
const lunar = solar.getLunar()

// 从年月日时创建
const solar = Solar.fromYmdHms(2000, 8, 16, 12, 0, 0)
const lunar = solar.getLunar()
```

## 万年历页面实现

### 日历生成

```typescript
const generateCalendar = (year: number, month: number) => {
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDay = firstDay.getDay()
  const totalDays = lastDay.getDate()
  
  const days = []
  
  // 上个月的日期
  const prevLastDay = new Date(year, month, 0).getDate()
  for (let i = startDay - 1; i >= 0; i--) {
    const day = prevLastDay - i
    const date = new Date(year, month - 1, day)
    const solar = Solar.fromDate(date)
    const lunar = solar.getLunar()
    
    days.push({
      day,
      month: month - 1,
      year: year,
      isCurrentMonth: false,
      isToday: false,
      lunarDay: lunar.getDayInChinese(),  // "初一", "初二"
      lunarMonth: lunar.getMonthInChinese(),
      jieQi: lunar.getPrevJieQi()?.getName() || ''
    })
  }
  
  // 本月的日期
  const today = new Date()
  for (let i = 1; i <= totalDays; i++) {
    const date = new Date(year, month, i)
    const solar = Solar.fromDate(date)
    const lunar = solar.getLunar()
    
    days.push({
      day: i,
      month: month,
      year: year,
      isCurrentMonth: true,
      isToday: date.toDateString() === today.toDateString(),
      lunarDay: lunar.getDayInChinese(),
      lunarMonth: lunar.getMonthInChinese(),
      jieQi: lunar.getJieQi() || ''
    })
  }
  
  // 下个月的日期
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(year, month + 1, i)
    const solar = Solar.fromDate(date)
    const lunar = solar.getLunar()
    
    days.push({
      day: i,
      month: month + 1,
      year: year,
      isCurrentMonth: false,
      isToday: false,
      lunarDay: lunar.getDayInChinese(),
      lunarMonth: lunar.getMonthInChinese(),
      jieQi: ''
    })
  }
  
  return days
}
```

### 日期详情信息

```typescript
const getSelectedDateInfo = (selectedDate: Date) => {
  const solar = Solar.fromDate(selectedDate)
  const lunar = solar.getLunar()
  
  return {
    // 阳历
    solarYear: solar.getYear(),
    solarMonth: solar.getMonth(),
    solarDay: solar.getDay(),
    weekday: ['日', '一', '二', '三', '四', '五', '六'][selectedDate.getDay()],
    
    // 农历
    lunarYear: lunar.getYear(),
    lunarMonth: lunar.getMonth(),
    lunarDay: lunar.getDay(),
    lunarMonthChinese: lunar.getMonthInChinese(),
    lunarDayChinese: lunar.getDayInChinese(),
    
    // 干支
    yearGanZhi: lunar.getYearInGanZhi(),
    monthGanZhi: lunar.getMonthInGanZhi(),
    dayGanZhi: lunar.getDayInGanZhi(),
    
    // 生肖
    shengXiao: lunar.getYearShengXiao(),
    
    // 节气
    jieQi: lunar.getJieQi(),
    prevJieQi: lunar.getPrevJieQi(),
    nextJieQi: lunar.getNextJieQi(),
    
    // 纳音
    yearNaYin: lunar.getYearNaYin(),
    monthNaYin: lunar.getMonthNaYin(),
    dayNaYin: lunar.getDayNaYin(),
  }
}
```

## 梅花易数时间起卦

```typescript
const qiguaByTime = () => {
  const now = new Date()
  const solar = Solar.fromDate(now)
  const lunar = solar.getLunar()
  
  // 获取农历时间
  const lunarYear = lunar.getYear()
  const lunarMonth = lunar.getMonth()
  const lunarDay = lunar.getDay()
  
  // 获取时辰（地支序数）
  const hour = now.getHours()
  const shichenIndex = Math.floor((hour + 1) / 2) % 12 + 1
  
  // 梅花易数时间起卦公式
  const mod8 = (n: number) => { const r = n % 8; return r === 0 ? 8 : r }
  const mod6 = (n: number) => { const r = n % 6; return r === 0 ? 6 : r }
  
  const totalBasic = lunarYear + lunarMonth + lunarDay
  const upNum = mod8(totalBasic)
  const totalFull = totalBasic + shichenIndex
  const downNum = mod8(totalFull)
  const dongYao = mod6(totalFull)
  
  // 农历信息
  const lunarInfo = `农历${lunar.getMonthInChinese()}月${lunar.getDayInChinese()} ${lunar.getYearInGanZhi()}年`
  
  return { upNum, downNum, dongYao, lunarInfo }
}
```

## 每日一签时辰显示

```typescript
// 获取当前时辰
const getShichen = () => {
  const now = new Date()
  const solar = Solar.fromDate(now)
  const lunar = solar.getLunar()
  const hour = now.getHours()
  const shichenList = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
  const index = Math.floor((hour + 1) / 2) % 12
  return shichenList[index] + '时'
}

// 页面显示农历信息
const [lunarInfo, setLunarInfo] = useState('')
const [shichen, setShichen] = useState('')

useEffect(() => {
  const now = new Date()
  const solar = Solar.fromDate(now)
  const lunar = solar.getLunar()
  setLunarInfo(`农历${lunar.getMonthInChinese()}月${lunar.getDayInChinese()} ${lunar.getYearInGanZhi()}年`)
  
  const hour = now.getHours()
  const shichenList = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
  const index = Math.floor((hour + 1) / 2) % 12
  setShichen(shichenList[index] + '时')
}, [])
```

## 抽签逻辑（使用农历）

```typescript
const drawQian = () => {
  const now = new Date()
  const solar = Solar.fromDate(now)
  const lunar = solar.getLunar()
  
  // 获取时辰索引
  const hour = now.getHours()
  const shichenIndex = Math.floor((hour + 1) / 2) % 12
  
  // 生成随机数字（1-30）
  const randomNum = Math.floor(Math.random() * 30) + 1
  
  // 计算签号（时辰 + 随机数字）
  const qianIndex = (shichenIndex + randomNum) % qianData.length
  
  // 获取农历时间信息
  const lunarTime = `农历${lunar.getMonthInChinese()}月${lunar.getDayInChinese()} ${lunar.getYearInGanZhi()}年`
  const shichen = getShichen()
  
  return {
    qian: qianData[qianIndex],
    lunarTime,
    shichen,
    randomNum
  }
}
```

## 常见问题

### 1. 节气对象API限制

```typescript
const prevJieQi = lunar.getPrevJieQi()
prevJieQi.getName()   // ✅ "小暑"
prevJieQi.getMonth()  // ❌ 可能不存在
prevJieQi.getDay()    // ❌ 可能不存在

// 安全做法：只用getName()
if (prevJieQi) {
  const name = prevJieQi.getName()
}
```

### 2. getDay() vs getDayInChinese()

```typescript
// getDay() 返回数字
lunar.getDay() === 1  // 判断是否初一

// getDayInChinese() 返回中文
lunar.getDayInChinese()  // "初一", "初二", "十五", "廿九"

// UI显示用 getDayInChinese()
// 判断逻辑用 getDay() === 1
```

### 3. TypeScript类型扩展

```typescript
// 当需要给状态对象添加新字段时
const [state, setState] = useState<
  (typeof baseState & { newField: string }) | null
>(null)
```
