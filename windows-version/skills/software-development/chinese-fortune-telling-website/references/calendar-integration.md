# 万年历集成指南

## 功能需求

在首页添加万年历区域，显示：
- 公历日期（年月日+星期）
- 农历日期（如：七月十五）
- 干支年（如：丙午年）
- 生肖（如：马）
- 当前节气（如：小暑）
- 宜忌（3个宜+3个忌）

## 实现方式

### 方案1：使用 lunar-javascript 库（推荐）

```bash
npm install lunar-javascript
```

```typescript
'use client'
import { useState, useEffect } from 'react'
import { Solar, Lunar } from 'lunar-javascript'

export default function CalendarSection() {
  const [currentDate, setCurrentDate] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setCurrentDate(new Date()), 60000)
    return () => clearInterval(timer)
  }, [])

  // 阳历转农历
  const solar = Solar.fromDate(currentDate)
  const lunar = solar.getLunar()

  // 获取农历信息
  const lunarMonth = lunar.getMonthInChinese()  // "正"、"二"等
  const lunarDay = lunar.getDayInChinese()      // "初一"、"初二"等
  const ganZhi = lunar.getYearInGanZhi()        // "丙午"
  const shengXiao = lunar.getYearShengXiao()    // "马"

  // 获取节气
  const jieQi = lunar.getJieQi()  // 当天节气（如有）

  return (
    <section className="py-12 px-6" style={{ backgroundColor: '#f5f0e8' }}>
      <div className="max-w-4xl mx-auto">
        <div className="rounded-2xl p-8" style={{ backgroundColor: '#fff', border: '1px solid #e5ddd0' }}>
          {/* 顶部日期 */}
          <div className="text-center mb-6">
            <div className="text-4xl font-bold mb-2" style={{ color: '#2c1810' }}>
              {currentDate.getFullYear()}年{currentDate.getMonth() + 1}月{currentDate.getDate()}日
            </div>
            <div className="text-lg" style={{ color: '#8b7355' }}>
              星期{['日', '一', '二', '三', '四', '五', '六'][currentDate.getDay()]}
            </div>
          </div>

          {/* 农历信息 */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-3 rounded-lg" style={{ backgroundColor: '#f5f0e8' }}>
              <div className="text-xs mb-1" style={{ color: '#8b7355' }}>农历</div>
              <div className="text-lg font-medium" style={{ color: '#2c1810' }}>
                {lunarMonth}月{lunarDay}
              </div>
            </div>
            <div className="text-center p-3 rounded-lg" style={{ backgroundColor: '#f5f0e8' }}>
              <div className="text-xs mb-1" style={{ color: '#8b7355' }}>干支</div>
              <div className="text-lg font-medium" style={{ color: '#2c1810' }}>
                {ganZhi}年
              </div>
            </div>
            <div className="text-center p-3 rounded-lg" style={{ backgroundColor: '#f5f0e8' }}>
              <div className="text-xs mb-1" style={{ color: '#8b7355' }}>生肖</div>
              <div className="text-lg font-medium" style={{ color: '#2c1810' }}>
                {shengXiao}
              </div>
            </div>
            <div className="text-center p-3 rounded-lg" style={{ backgroundColor: '#f5f0e8' }}>
              <div className="text-xs mb-1" style={{ color: '#8b7355' }}>节气</div>
              <div className="text-lg font-medium" style={{ color: '#2c1810' }}>
                {jieQi || '无'}
              </div>
            </div>
          </div>

          {/* 宜忌 */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-lg" style={{ backgroundColor: '#f5f0e8' }}>
              <div className="text-sm font-medium mb-2" style={{ color: '#4CAF50' }}>宜</div>
              <div className="flex flex-wrap gap-2">
                {/* 宜事项标签 */}
              </div>
            </div>
            <div className="p-4 rounded-lg" style={{ backgroundColor: '#f5f0e8' }}>
              <div className="text-sm font-medium mb-2" style={{ color: '#F44336' }}>忌</div>
              <div className="flex flex-wrap gap-2">
                {/* 忌事项标签 */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
```

### 方案2：简化版（不使用库）

如果不想引入依赖，可以用简化算法：

```typescript
// 简化的农历计算（精度较低）
const getLunarInfo = (date: Date) => {
  const year = date.getFullYear()
  const month = date.getMonth()
  const day = date.getDate()
  
  const lunarYear = year - 1900
  const lunarMonth = (month + 1 + 12) % 12
  const lunarDay = day
  
  const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
  const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
  const SHENG_XIAO = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
  
  const ganIndex = lunarYear % 10
  const zhiIndex = lunarYear % 12
  
  return {
    lunarMonth: ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊'][lunarMonth],
    lunarDay: ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
      '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'][lunarDay - 1] || '初一',
    ganZhi: `${TIAN_GAN[ganIndex]}${DI_ZHI[zhiIndex]}`,
    shengXiao: SHENG_XIAO[zhiIndex]
  }
}
```

## 宜忌数据

宜忌可以根据日期生成（简化版本）：

```typescript
const YI_ITEMS = ['祭祀', '祈福', '求嗣', '开光', '出行', '解除', '伐木', '盖屋', '起基', '修坟', '安葬', '移柩', '入殓', '破土', '启钻', '造桥', '作灶', '修造', '动土', '竖柱', '上梁', '掘井', '开池', '放水', '牧养', '纳畜', '栽种']
const JI_ITEMS = ['嫁娶', '纳采', '入宅', '开市', '交易', '立券', '挂匾', '开光', '出行', '入宅', '移徙', '安床', '作灶', '修造', '动土', '破土', '安葬', '启钻']

const getYiJi = (date: Date) => {
  const day = date.getDate()
  const yiIndex = day % YI_ITEMS.length
  const jiIndex = (day + 3) % JI_ITEMS.length
  
  return {
    yi: [YI_ITEMS[yiIndex], YI_ITEMS[(yiIndex + 1) % YI_ITEMS.length], YI_ITEMS[(yiIndex + 2) % YI_ITEMS.length]],
    ji: [JI_ITEMS[jiIndex], JI_ITEMS[(jiIndex + 1) % JI_ITEMS.length], JI_ITEMS[(jiIndex + 2) % JI_ITEMS.length]]
  }
}
```

## 位置

万年历区域应该放在：
- Hero区域下方
- 功能概览区域上方
- 固定浅色背景（#f5f0e8）

```tsx
{/* Hero区域 */}
<section>...</section>

{/* 万年历 */}
<CalendarSection />

{/* 功能概览 */}
<section>...</section>
```

## UI设计要点

**⚠️ 用户明确要求**：
- 固定浅色背景（#f5f0e8），不随滚动变化
- 文字颜色固定（深棕/棕色系）
- 宜忌用标签样式，不用红绿分栏
- 整体风格与每日一卦区域一致
