---
name: chinese-fortune-telling-website
description: "搭建中国传统命理算命网站的完整指南。覆盖梅花易数、四柱八字、奇门遁甲、紫微斗数、每日一签等核心功能。包含道教风格UI设计、卦象算法、真灵应宝签数据库、AI解签/解卦集成。"
version: 1.4.0
author: Hermes Agent
triggers:
  - "算命网站"
  - "命理网站"
  - "梅花易数"
  - "四柱八字"
  - "奇门遁甲"
  - "紫微斗数"
  - "每日一签"
  - "道教风格"
  - "fortune telling website"
  - "divination website"
  - "Chinese astrology"
related_skills:
  - ai-fortune-telling-platform
  - chinese-divination-platform
  - ui-ux-pro-max-skill
  - ai-crawler-reverse-engineering
---

# 中国传统命理算命网站搭建指南

## 项目背景

基于"小算"项目实战经验，涵盖从UI设计到算法实现的完整流程。

### 品牌名称（阿戴明确要求）

**品牌名**：小算一下（不是"算了么"，那是竞品的名字）
**拼音**：XIAO SUAN YI XIA
**定价模式**：完全免费（"价格不用，我们完全免费"）

### 已验证的项目

| 项目 | 目录 | 状态 | 说明 |
|------|------|------|------|
| 小算 v2 | /Users/macpro/xiaosuan-v2 | ✅ 运行中 | 道教风格，Next.js 14，完全免费 |
| 天机阁（已备份） | tianji-ge-backup-20260708 | 备份 | 原始项目 |
| suanlemeai逆向文件库 | ~/Desktop/suanlemeai-逆向文件库 | 完成 | 76个文件 |

---

## 一、道教风格UI设计系统

### 1.1 配色方案（已验证）

```css
:root {
  /* 道教玄色系 - 主色调 */
  --xuan-black: #0a0a0f;      /* 主背景色（深色模式） */
  --taiji-white: #faf8f5;      /* 主背景色（浅色模式） */
  --cinnabar: #c23a2b;         /* 朱砂红 - 主强调色 */
  --daopao: #2d5a4a;           /* 道袍青 - 次强调色 */
  --gold: #d4a843;             /* 金箔黄 - 高亮、VIP */
  
  /* 五行配色 */
  --wu-metal: #d4a843;         /* 金 */
  --wu-wood: #2d5a4a;          /* 木 */
  --wu-water: #1a3a5c;         /* 水 */
  --wu-fire: #c23a2b;          /* 火 */
  --wu-earth: #8b7355;         /* 土 */
  
  /* 辅助色 */
  --smoke: #6b7280;            /* 烟灰 - 次要文字 */
  --xuan-paper: #e5e2db;       /* 宣纸灰 - 边框 */
  --ink: #1f1f2e;              /* 墨影 - 卡片背景 */
  --jade: #f5f3ef;             /* 玉白 - 卡片背景（浅色） */
}
```

### 1.1.1 首页背景渐变（已验证）

**阿戴要求**：由白变黑的道教风格背景

```jsx
{/* 由白变黑的道教风格背景 */}
<div className="fixed inset-0 bg-gradient-to-b from-[#1a1a2e] via-[#0d1f3c] to-[#0a0a0f]">
  {/* 云雾纹理 */}
  <div className="absolute inset-0 opacity-30">
    <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_rgba(255,255,255,0.15)_0%,_transparent_50%)]"/>
    <div className="absolute bottom-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_bottom,_rgba(255,255,255,0.05)_0%,_transparent_50%)]"/>
  </div>
  
  {/* 动态背景散字 */}
  {bgCharacters.map((char, index) => (
    <div
      key={index}
      className="absolute text-white/[0.03] font-brush select-none pointer-events-none animate-float"
      style={{
        top: `${10 + (index * 8) % 80}%`,
        left: `${5 + (index * 12) % 90}%`,
        fontSize: `${80 + (index * 20) % 100}px`,
        transform: `rotate(${-15 + (index * 10) % 30}deg)`,
        animationDelay: `${index * 0.5}s`,
        animationDuration: `${6 + index % 4}s`,
      }}
    >
      {char}
    </div>
  ))}
</div>
```

### 1.2 字体搭配

```css
/* 中文 */
--font-serif: 'Noto Serif SC', 'Source Han Serif SC', '宋体', serif;      /* 标题 */
--font-sans: 'Noto Sans SC', 'Source Han Sans SC', '微软雅黑', sans-serif; /* 正文 */
--font-brush: 'Ma Shan Zheng', 'KaiTi', cursive;                          /* 书法装饰 */

/* 英文 */
--font-heading: 'Playfair Display', Georgia, serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

### 1.3 设计原则

1. **留白为美**：大量留白，营造禅意空间感
2. **虚实相生**：毛玻璃效果 + 阴影层次
3. **动静结合**：微动画 + 静态内容平衡
4. **五行和谐**：配色遵循五行相生原则
5. **简约风格**：UI设计为简约风格，不堆砌装饰

### 1.4 核心CSS组件

```css
/* 毛玻璃卡片 */
.glass-card {
  @apply bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl;
}

/* 主按钮 - 朱砂红渐变 */
.btn-primary {
  @apply bg-gradient-to-r from-cinnabar to-red-700 text-white px-6 py-3 
         rounded-lg font-semibold shadow-lg shadow-cinnabar/30;
}

/* 金色按钮 */
.btn-gold {
  @apply bg-gradient-to-r from-gold to-yellow-600 text-xuan-black px-6 py-3 
         rounded-lg font-semibold shadow-lg shadow-gold/30;
}

/* 结果卡片 */
.card-result {
  @apply bg-gradient-to-br from-gold/10 to-cinnabar/5 border border-gold/20 rounded-xl p-6;
}
```

### 1.5 动画系统

```css
/* 太极旋转 */
.animate-taiji { animation: taiji-rotate 20s linear infinite; }

/* 摇签筒 */
.animate-shake { animation: shake 1s ease-in-out; }

/* 脉冲发光 */
.animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }

/* 浮动 */
.animate-float { animation: float 6s ease-in-out infinite; }

/* 小道士扫地 */
.animate-sweep { animation: sweep 4s ease-in-out infinite; }
.animate-sweep-path { animation: sweep-path 4s ease-in-out infinite; }

/* 渐入 */
.animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
```

### 1.6 角色动画实现（p5.js / Canvas）

**阿戴要求**：不要用SVG图，要用skills本地生成动画

**推荐方案**：HTML5 Canvas + requestAnimationFrame

```typescript
// 在React组件中使用Canvas动画
const canvasRef = useRef<HTMLCanvasElement>(null)

useEffect(() => {
  if (canvasRef.current) {
    initMonkAnimation(canvasRef.current)
  }
}, [])

// Canvas动画初始化函数（在组件外定义）
function initMonkAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  let time = 0

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    time += 0.02
    // 绘制角色、动画帧...
    requestAnimationFrame(draw)
  }
  draw()
}
```

**p5.js方案**（更复杂的动画）：
- 参考 `/public/xiaodaoshi-sweep.html`
- 使用 p5.js 1.11.3 CDN
- 单个HTML文件，可独立运行

详见 `references/p5js-animation.md`

---

## 二、核心页面设计（Word文档要求）

### 2.0 Word文档UI提取流程（已验证）

当用户提供Word文档中的UI设计图时：

```bash
# 1. 用Preview打开Word文档
open -a "Preview" "/path/to/document.doc"

# 2. 等待文档加载
sleep 3

# 3. 截图当前页面
screencapture -x /tmp/word-screenshot.png

# 4. 用vision_analyze查看截图
# 问题示例："请详细描述文档中的UI设计图内容"

# 5. 滚动查看更多内容
for i in {1..5}; do
    osascript -e 'tell application "System Events" to key code 125'
    sleep 0.5
done

# 6. 继续截图和分析
screencapture -x /tmp/word-scroll1.png
```

**⚠️ 关键点**：
- 用户说"图片自己在word文件中看" = 必须用上述方法提取图片
- 不能只提取文字，必须查看图片中的UI设计
- 截图后用vision_analyze分析设计细节
- 每次滚动后都要截图，确保看到所有设计图

### 2.1 首页设计

**品牌名**：小算一下（不是"算了么"）
**定价**：完全免费，不显示任何价格/会员信息

**布局要求**（来自suanlemeai.cn逆向分析 + Word文档）：
- 左上角："算"logo + "小算一下"品牌名
- 导航栏：首页、工具、每日一签、传统文化书籍整合、万年历
- 右上角：语言切换(EN)、登录、汉堡菜单
- 中心主标题：大号书法字体"小算一下" + 发光效果 + 拼音
- 标语：东方命理，云海问卦
- 哲学标语：天地之间，万事皆有迹可循
- 功能说明：八字、紫微、六爻、塔罗、古籍与人格测试，一屏进入
- 两个CTA按钮："小算一下 →"（白色主按钮）+ "每日一签"（半透明次按钮）
- 背景：由白变黑的道教风格渐变（#1a1a2e → #0d1f3c → #0a0a0f）+ 动态散字
- 可选：小道士扫地动画（Canvas实现）

**⚠️ 首页下方必须包含的完整内容（按suanlemeai.cn排版）**：
1. 功能概览 - 27工具/55古籍/78塔罗统计 + 8个核心功能卡片
2. 使用指南 - 4步骤（定时→取象→断事→复核）
3. 每日一卦 - 今日卦象预览
4. 知识图解 - 6个教育模块
5. 时间签文 - 随机道藏话语
6. 关于 - 品牌介绍
7. 页脚 - 导航链接

**⚠️ 重写页面时的严重警告（已犯错）**：
阿戴："怎么只有这么点页面了"
**重写任何页面时，必须先读取现有完整内容，然后保留所有现有section。**
不能只写Hero区域就交差，下方的功能概览、使用指南、知识图解等必须全部包含。

**道藏随机话语示例**：
```typescript
const daocangQuotes = [
  "道可道，非常道；名可名，非常名。",
  "上善若水，水善利万物而不争。",
  "天地不仁，以万物为刍狗。",
  "知人者智，自知者明。",
  "大音希声，大象无形。",
  "道生一，一生二，二生三，三生万物。",
  "人法地，地法天，天法道，道法自然。",
]
```

### 2.2 每日一卦页面（卦气值日 - 已验证）

**阿戴明确要求**：
- "不要梅花易数，看看易经或者别的道藏有没有每日出一卦的"
- "不推事情只看日子吉凶" - 只显示当日吉凶，不用于占卜具体事情
- 使用传统"卦气值日"体系，有古籍依据
- "确定一下每日卦象都不一样吗？是算出来的吗" - 必须验证算法正确性
- "先补全再改这个，要随着卦象变" - 必须完整实现64卦数据

**UI偏好（已验证）**：
- "不要红绿分栏" - 宜忌不用绿色/红色分栏，改用标签样式
- "这个要一直白着，不受渐变黑影响" - 每日一卦区域固定浅色背景(#f5f0e8)
- 所有文字颜色固定（深棕/棕色系），不随滚动变化
- 宜忌用标签样式（flex flex-wrap gap-2），不用列表

**算法来源**：汉代孟喜「卦气说」
- 60卦（去掉乾坤坎离四正卦）分配到一年365天
- 每卦主管约6天（"六日七分说"）
- 从冬至开始，复卦为首卦
- 反映当日天地之气，用于判断日子吉凶

**布局要求**：
- 水墨风格背景（深棕色 #1a1610）
- 金色/琥珀色主色调
- 展示：卦名、上卦/下卦符号、吉凶等级、卦辞、卦意、今日建议
- 可展开查看详细宜忌（宜什么/忌什么）
- framer-motion动画（进入、展开、列表项）
- 底部注明古籍依据

**核心算法**（已实现于 `/src/lib/hexagram.ts`）：
```typescript
// 卦气值日序列（60卦，从冬至开始）
const GUAQI_SEQUENCE = [
  24, 27, 3, 42, 51,  // 子月：复、颐、屯、益、震
  21, 17, 25, 36, 22,  // 噬嗑、随、无妄、明夷、贲
  63, 37, 55, 49, 13,  // 既济、家人、丰、革、同人
  // ... 完整60卦序列
]

// 获取今日卦象
export function getDailyHexagram(date: Date = new Date()) {
  const year = date.getFullYear()
  const winterSolstice = new Date(year, 11, 21) // 12月21日
  const startDate = date < winterSolstice 
    ? new Date(year - 1, 11, 21) 
    : winterSolstice
  
  const daysFromStart = Math.floor(Math.abs((date.getTime() - startDate.getTime()) / (24*60*60*1000)))
  const hexagramIndex = Math.floor(daysFromStart / 6) % 60
  const hexagramNumber = GUAQI_SEQUENCE[hexagramIndex]
  
  return { hexagram: HEXAGRAMS[hexagramNumber], dayIndex: daysFromStart, ... }
}
```

**64卦数据结构**（每卦包含）：
```typescript
{
  name: '地天泰',
  symbol: '䷊',
  upper: '坤',
  lower: '乾',
  judgment: '小往大来，吉亨',
  fortune: '大吉',  // 大吉/吉/中吉/平/小凶/凶
  goodFor: ['一切事宜', '开业', '婚嫁', '出行', '求财'],
  badFor: [],
  advice: '泰卦象征天地交泰，万事亨通。今日大吉大利，诸事皆宜。',
  meaning: '泰卦象征天地交通，万物通达。今日气运极佳，是难得的好日子。'
}
```

**依赖安装**：
```bash
npm install framer-motion  # 动画库
```

**⚠️ Pitfall**：
- 用户明确说"不要梅花易数"用于每日一卦 - 梅花易数用于推事，不是看日子吉凶
- 卦气值日是正统易学体系，有汉代古籍依据
- 需要完整的64卦数据（卦辞、吉凶、宜忌），当前只实现了约20卦，需要补充完整

### 2.3 梅花易数页面（已实现）

**实际实现**: `/src/app/meihua/page.tsx`，路由 `/meihua`
**参考UI**: destinyseek.com 梅花易数页面排版（2026-07-15实现）

**布局要求（已验证）**：
- 标题"梅花易数" + 副标题
- 提问输入框（placeholder: "例如：我是否应该接受这个工作机会？"）
- 起卦方式切换（数字起卦/时间起卦/手动起卦）— 三个tab按钮
- 数字输入区域（两个1-99输入框）
- "起卦解析"按钮
- 结果展示：本卦（含卦名+卦辞+邵雍诗词+吉凶+建议）、互卦（含卦名+诗词）、变卦（含卦名+诗词）、体用分析
- "重新起卦"按钮
- **⚠️ 64卦数据已完整实现**：64个组合全部覆盖，每卦含卦名、卦辞、吉凶、建议、邵雍诗词。互卦变卦显示完整卦名+诗词。
- 时辰起卦必须用农历地支序数（邵雍原法），验证示例：2026-07-16午时→地山谦五爻动

### 2.3.1 万年历页面（已实现）

**实际实现**: `/src/app/calendar/page.tsx`，路由 `/calendar`
**参考UI**: destinyseek.com/zh/tools/huangli/ 完整排版（2026-07-15实现）

**布局（单栏垂直，从上到下）**：
1. 标题"万年历" + 副标题"帮你读懂传统黄历，每天吉凶早知道。"
2. 日历卡片（年月下拉选择器 + 左右翻页 + "今天"按钮 + 7列日期网格 + 农历日期 + 节气红字标注）
3. 日期信息栏（公历 + 干支 + 生肖 + 星期周数）
4. 宜忌（橙色宜标签 + 灰色忌标签 + 查吉日按钮 + 五行·冲煞·值神三栏）
5. 时辰吉凶（12方块，吉=绿底/凶=红底）
6. 详细信息（建除十二神 + 吉神宜趋 + 胎神 + 凶神宜忌 + 二十八宿 + 彭祖百忌）
7. 方位神祇（财神/喜神/福神/阳贵神 四宫格）
8. 补充历法（生肖/纳音/二十八宿/物候/空亡/月相/九星/六曜/节气）
9. 时辰宜忌（当前时辰详情 + "看更多"展开全部12时辰）
10. 查吉日（宜/忌切换 + 12个活动类别按钮）

**技术要点**：
- 使用 `lunar-javascript` 库，不用查表法
- 必须用 `useState` + `useEffect`（不能用 `useMemo`），否则SSR时lunar对象序列化丢失方法
- TypeScript类型声明：`/src/types/lunar-javascript.d.ts`
- **SSR陷阱**: lunar-javascript对象在Next.js build时序列化丢失方法，必须用useState+useEffect，不能用useMemo。详见xiaosuan-project skill。
- "起卦解析"按钮（全宽，深色背景）
- 结果展示：本卦（上下卦符号+卦名+卦辞+吉凶）、互卦、变卦、体用分析
- "重新起卦"按钮

**卦象显示组件（不用SVG）**：
```tsx
function YaoLine({ isYang }: { isYang: boolean }) {
  if (isYang) return <div className="w-12 h-1 rounded-full mx-auto" style={{ backgroundColor: '#2c1810' }}/>
  ### 2.3 梅花易数页面

  **布局要求**（参考destinyseek.com）：
  - 标题"梅花易数" + 副标题
  - 提问输入框
  - 起卦方式切换标签（数字起卦/时间起卦/手动起卦）
  - 数字输入区域（两个1-99输入框）
  - "起卦解析"按钮
  - 结果展示：
    - 本卦：上卦+卦名+下卦、卦辞、动爻、吉凶、邵雍诗词、建议
    - 互卦：卦名 + 上下卦 + 诗词
    - 变卦：卦名 + 上下卦 + 诗词
    - 体用分析：体卦（五行）+ 用卦（五行）

  **关键算法**：
  ```python
  # 先天八卦数映射
  TRIGRAMS = {1:'乾', 2:'兑', 3:'离', 4:'震', 5:'巽', 6:'坎', 7:'艮', 8:'坤'}

  # 时间起卦（必须用农历！）
  上卦 = (年支数 + 月 + 日) % 8  # 余0取8
  下卦 = (年支数 + 月 + 日 + 时支) % 8
  动爻 = (年支数 + 月 + 日 + 时支) % 6  # 余0取6

  # 数字起卦
  上卦 = A % 8  # 余0取8
  下卦 = B % 8
  动爻 = (A + B) % 6  # 余0取6
  ```

  **64卦数据**：每卦含name/judgment/fortune/advice/poem，完整数据在 `/src/app/meihua/page.tsx` 的 HEXAGRAMS 对象。

  **时辰计算**：
  ```typescript
  // 地支序数
  const ZHI_INDEX = { '子':1,'丑':2,'寅':3,'卯':4,'辰':5,'巳':6,'午':7,'未':8,'申':9,'酉':10,'戌':11,'亥':12 }
  // 时辰索引
  const shichenIndex = Math.floor((hour + 1) / 2) % 12  // 0=子,1=丑,...11=亥
  ```

  **汉堡菜单**：所有页面统一，包含"签 每日一签"、"历 万年历"、"卦 梅花易数"三个选项。动画效果：三横线变X + 下拉滑出。

**⚠️ 64卦数据已完整实现**：64个组合全部覆盖，每卦含卦名、卦辞、吉凶、建议、邵雍诗词。互卦变卦显示完整卦名+诗词。

### 2.4 四柱八字页面

**布局要求**：
- 精确排盘（四柱表格）
- 十神分析
- 五行统计（柱状图）
- 大运排列
- 地支藏干

---

## 三、算法实现参考

### 3.1 核心开源库

| 库 | 用途 | Stars | NPM |
|---|---|---|---|
| [iztro](https://github.com/SylarLong/iztro) | 紫微斗数排盘 | 3,900 | `npm install iztro` |
| [lunar-javascript](https://github.com/6tail/lunar-javascript) | 农历/节气/八字 | 1,600 | `npm install lunar-javascript` |

### 3.2 算法文档

详见 references/ 目录：
| `references/meihua-algorithms.md` | 梅花易数完整算法 |
| `references/lunar-javascript-nextjs.md` | lunar-javascript在Next.js中的使用（万年历、农历转换） |
| `references/xiaodaoshi-animation.md` | 小道童扫地Canvas动画实现（角色设计+代码+React集成） |

---

## 四、竞品逆向参考

### suanlemeai.cn（算了么）

**技术栈**：Next.js 14 + React 18 + TypeScript + Tailwind CSS
**功能**：27个命理工具，基础免费 + 会员付费（30元/月起）
**逆向文件库**：`/Users/macpro/Desktop/suanlemeai-逆向文件库/`

**关键发现**：
- 客户端计算为主（基础排盘零网络请求）
- 暗色主题（#0a0a0a背景 + #1fa2dc主色调）
- 3种主题：light、dark、ocean
- 使用localStorage保存用户数据

### 参考项目

| 项目 | GitHub | 参考价值 |
|------|--------|----------|
| jishiyu（吉时雨） | chxb/jishiyu | 功能最全（18种术数） |
| mingyu（命语） | Brhiza/mingyu | API设计 + AI提示词 |
| MingPan（命盘） | Jam0731/MingPan | TypeScript引擎架构 |
| ziwei（紫微知道） | ruijayfeng/ziwei | React前端实现 |

---

## 五、项目文件结构规范

**阿戴明确要求**：所有项目代码必须按规范工程文件结构整理，不要按模块拆分。

**标准结构**：
```
项目名/
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router
│   │   ├── pages/        # 页面
│   │   ├── components/   # 组件
│   │   ├── contexts/     # Context
│   │   ├── hooks/        # Hooks
│   │   ├── stores/       # 状态管理
│   │   ├── lib/          # 工具函数
│   │   └── types/        # 类型定义
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── postcss.config.js
│
└── backend/
    ├── main.py
    ├── requirements.txt
    └── ...
```

**⚠️ 关键点**：
- 不能按module1-state、module2-hooks这种方式拆分
- 必须包含完整配置文件（package.json、tsconfig.json等）
- 必须包含README文档

---

## 六、Apple风格滚动渐变背景（已验证）

### 效果描述
米白色背景 → 滚动时慢慢变暗 → 底部变成黑色

### 实现方法

```tsx
'use client'
import { useState, useEffect } from 'react'

export default function Page() {
  const [scrollProgress, setScrollProgress] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY
      const docHeight = document.documentElement.scrollHeight - window.innerHeight
      const progress = Math.min(scrollTop / docHeight, 1)
      setScrollProgress(progress)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // 计算背景色渐变 - 从米白色到黑色
  const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`

  return (
    <div style={{ backgroundColor: bgColor }}>
      {/* 所有文字、按钮颜色都随scrollProgress变化 */}
    </div>
  )
}
```

### ⚠️ Pitfall: CSS body背景色覆盖React style

**问题**：globals.css中`body { background: var(--xuan-black); }`会覆盖React组件的inline style。

**症状**：scrollProgress计算正确，但背景色不变。

**解决**：
```css
/* globals.css */
body {
  background: transparent; /* 不是黑色！让React的style生效 */
}
```

---

## 七、Canvas角色动画（已验证）

### 小道童扫地动画实现

```tsx
const canvasRef = useRef<HTMLCanvasElement>(null)

useEffect(() => {
  if (canvasRef.current) {
    initMonkAnimation(canvasRef.current)
  }
}, [])

// JSX中
<canvas ref={canvasRef} width={200} height={200} />
```

```typescript
function initMonkAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  let time = 0

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    time += 0.03

    const monkX = canvas.width / 2 + Math.sin(time * 0.8) * 15
    const sweepAngle = Math.sin(time * 2) * 0.4
    const breathe = Math.sin(time * 1.5) * 3

    // 绘制身体、头、帽子、手臂、腿、扫帚
    // ...

    requestAnimationFrame(draw)
  }
  draw()
}
```

**关键点**：
- 使用`requestAnimationFrame`实现流畅动画
- `Math.sin`实现周期性运动（呼吸、摇摆、扫地）
- 需要设置`background: transparent`让canvas透明叠加

---

## 八、关键Pitfalls

### 5.1 lunar-python陷阱

```python
# ❌ 错误：Lunar.fromYmdHms接收的是农历日期！
lunar = Lunar.fromYmdHms(2024, 1, 1, 12, 0, 0)

# ✅ 正确：用Solar→Lunar转换
solar = Solar.fromYmdHms(2024, 1, 1, 12, 0, 0)
lunar = solar.getLunar()
```

### 5.2 八字十神获取

```python
# ❌ 错误：getShiShenGan()不存在
bazi.getShiShenGan()

# ✅ 正确：逐柱获取
bazi.getYearShiShenGan()
bazi.getMonthShiShenGan()
bazi.getDayShiShenGan()
bazi.getTimeShiShenGan()
```

### 5.3 奇门遁甲八宫序列

```python
# ❌ 错误：使用1-9序列
positions = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ✅ 正确：跳过中五宫
positions = [1, 2, 3, 4, 6, 7, 8, 9]  # 中五宫天干寄坤二
```

### 5.10 农历计算严重警告：禁止使用数学公式（已犯错）

**阿戴原话**："什么原因，不能出现这种问题啊"

**错误做法**：使用简化数学公式计算农历
```typescript
// ❌ 完全错误：农历不是简单的数学公式能算出来的
const lunarMonth = (month + 1 + 12) % 12
const lunarDay = day
```

**为什么错**：农历是基于天文观测的阴阳历，月份根据月亮运行周期确定，每年的农历日期都不同。简化公式会导致日期完全错误。

**正确做法**：
1. 使用查表法（查万年历数据）
2. 使用专业库（如 `lunar-javascript`）
3. 调用专业农历API

```typescript
// ✅ 正确：使用查表法
const lunarData2026: Record<string, { month: string, day: string }> = {
  '7-15': { month: '六', day: '初二' },
  // ... 完整数据
}
const key = `${month + 1}-${day}`
const lunarInfo = lunarData2026[key]

// ✅ 正确：使用lunar-javascript库
import { Solar } from 'lunar-javascript'
const solar = Solar.fromDate(new Date())
const lunar = solar.getLunar()
lunar.getDayInChinese()  // "初二"
lunar.getMonthInChinese()  // "六"
```

**⚠️ 这是严重错误，会导致用户极度不满。农历、节气、干支等传统历法必须查证准确数据。**

### 5.11 CSS body背景覆盖React inline style（已验证）

**问题**：在globals.css中设置了`body { background: var(--xuan-black); }`后，React组件中的`style={{ backgroundColor: ... }}`无法生效，因为CSS优先级更高。

**解决**：
```css
/* ❌ 错误：CSS背景色覆盖React动态style */
body {
  background: var(--xuan-black);
}

/* ✅ 正确：设置为transparent让React控制 */
body {
  background: transparent;
}
```

### 5.11 Apple风格滚动渐变背景（米白→黑）

**需求**：页面顶部米白色背景，滚动时逐渐变暗，底部完全变黑。

**实现**：
```typescript
const [scrollProgress, setScrollProgress] = useState(0)

useEffect(() => {
  const handleScroll = () => {
    const scrollTop = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = Math.min(scrollTop / docHeight, 1)
    setScrollProgress(progress)
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
  return () => window.removeEventListener('scroll', handleScroll)
}, [])

// 米白色(245,240,230) → 黑色(10,10,15)
const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`
```

**⚠️ 必须**：globals.css中body的background必须设为`transparent`，否则不生效。

**文字颜色也需要动态切换**：
```typescript
color: scrollProgress > 0.5 ? '#fff' : '#333'        // 主文字
color: scrollProgress > 0.5 ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.4)'  // 次要文字
```

### 5.12 Canvas小道童动画实现（React + useRef）

**模式**：在React中使用Canvas实现动画角色
```typescript
const canvasRef = useRef<HTMLCanvasElement>(null)

useEffect(() => {
  if (canvasRef.current) {
    initMonkAnimation(canvasRef.current)
  }
}, [])

// JSX
<canvas ref={canvasRef} width={200} height={200} />
```

**动画函数结构**：
```typescript
function initMonkAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  let time = 0
  
  function draw() {
    ctx.clearRect(0, 0, width, height)
    time += 0.03
    // 绘制角色：身体、头、帽子、眼睛、手臂、腿
    // 绘制道具：扫帚
    // 绘制特效：灰尘粒子
    requestAnimationFrame(draw)
  }
  draw()
}
```

**⚠️ 已知问题**：Canvas元素在某些情况下可能不被浏览器snapshot工具检测到（显示为不存在），但实际在页面上是正常渲染的。

### 5.13 Word文档中的图片查看方法

**当用户说"图片自己在word文件中看"时**：
```bash
# 1. 用Preview打开Word文档
open -a "Preview" "/path/to/document.doc"

# 2. 等待加载
sleep 3

# 3. 截图
screencapture -x /tmp/word-screenshot.png

# 4. 用vision_analyze查看
# 5. 滚动查看更多
for i in {1..5}; do
    osascript -e 'tell application "System Events" to key code 125'
    sleep 0.5
done
screencapture -x /tmp/word-scroll1.png
```

### 5.14 UI设计优先级

**阿戴明确要求**：
- "功能可以都不要，但是ui一定要设计好"
- "你的ui排版得按照我给你的word中的图来"
- UI设计 > 功能实现

**正确顺序**：
1. 先设计好UI（严格按照需求文档）
2. 再实现功能
3. 功能可以简化，UI不能妥协

### 5.15 阿戴的UI颜色偏好（已验证）

**明确禁止**：
- "不要红绿分栏" - 宜忌不用绿色/红色分栏，改用标签样式
- 不要随机色彩，保持统一色调

**固定背景要求**：
- "这个要一直白着，不受渐变黑影响" - 每日一卦、万年历等区域使用固定背景色(#f5f0e8)
- 所有文字颜色固定（深棕/棕色系），不随滚动变化

**实现方式**：
```tsx
{/* 固定背景，不受滚动渐变影响 */}
<section className="py-20 px-6" style={{ backgroundColor: '#f5f0e8' }}>
  <div className="text-sm mb-4" style={{ color: '#8b7355' }}>标题</div>
  <div className="text-3xl font-bold" style={{ color: '#2c1810' }}>内容</div>
</section>
```

**宜忌标签样式（不用红绿色）**：
```tsx
<div className="flex flex-wrap gap-2">
  {items.map((item, i) => (
    <span key={i} className="text-xs px-2 py-1 rounded" style={{ 
      backgroundColor: '#f5f0e8',
      color: '#6b5b4b' 
    }}>
      {item}
    </span>
  ))}
</div>
```

### 5.16 道藏/易经每日名言（已验证）

**阿戴要求**："这个改成从道藏和易经中每日随机抽取一句话放进去"

**实现方式**：使用日期作为种子，确保每天显示不同的名言
```typescript
// 道藏+易经名言库
const daocangQuotes = [
  // 道德经
  "道可道，非常道；名可名，非常名。",
  "上善若水，水善利万物而不争。",
  // 易经
  "天行健，君子以自强不息。",
  "地势坤，君子以厚德载物。",
  "穷则变，变则通，通则久。",
  // 庄子
  "相濡以沫，不如相忘于江湖。",
  // 周易
  "一阴一阳之谓道。",
]

// 使用日期作为种子，确保每天不同
const today = new Date()
const dayIndex = (today.getFullYear() * 366 + today.getMonth() * 31 + today.getDate()) % daocangQuotes.length
setQuote(daocangQuotes[dayIndex])
```

### 5.17 SVG图形禁用（已验证）

**阿戴明确要求**："这种svg以后都不要有了，删这个"

**规则**：不要使用SVG图形作为UI元素（如签筒、太极图等）。使用：
1. 纯CSS/HTML按钮
2. 图片帧动画（PNG序列）
3. Canvas动画

**替代方案**：
```tsx
// ❌ 不要SVG签筒
<svg width="200" height="300">...</svg>

// ✅ 用简洁按钮
<button className="px-12 py-6 rounded-2xl text-xl font-bold" 
  style={{ backgroundColor: '#2c1810', color: '#fff' }}>
  摇签
</button>
```

### 5.18 动画速度要慢（已验证）

**阿戴明确要求**："图片转换太快"

**解决方案**：
- 每帧300ms（原来150ms）
- 循环2次（原来3次）
- 总时长约6秒（原来4.5秒）

```typescript
const frameDuration = 300 // 每帧300ms
const maxLoops = 2        // 循环2次
```

### 5.19 导航栏毛玻璃效果（已验证）

**阿戴明确要求**：
- "首页导航栏白底虚化掉"
- "每日一签页面要和主页导航栏一样"

**实现方式**：
```tsx
<nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md" 
     style={{ backgroundColor: 'rgba(245, 240, 232, 0.8)', 
              borderBottom: '1px solid rgba(44, 24, 16, 0.1)' }}>
```

**所有页面导航栏必须统一**：首页、每日一签、每日一卦等页面使用相同样式。

### 5.18 玄真灵应宝签系统（已验证）

**签文来源**：《玄真灵应宝签》（正统道藏）
**结构**：十二时辰 × 每时辰30签 = 360签 + 五行5签 = 365签

**取签逻辑**：
1. 根据当前时辰确定签池（子时→子时30签）
2. 在该时辰30签中随机抽取1签
3. 每用户每日限摇3签

**时辰对应**：
```typescript
const SHI_CHEN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
const SHI_CHEN_HOURS = ['23:00-01:00', '01:00-03:00', '03:00-05:00', ...]
```

**每日限制实现**（localStorage）：
```typescript
function getDrawCount(): number {
  const today = new Date().toDateString()
  const stored = localStorage.getItem('lottery-draw-count')
  if (!stored) return 0
  const data = JSON.parse(stored)
  if (data.date === today) return data.count
  return 0
}
```

**超限提示**：
```
道法自然，不可强求
今日已摇三签，签运已尽
《玄真灵应宝签》云：每日三签为限，过则不灵。
```

### 5.19 图片帧动画（已验证）

**场景**：用户提供多张PNG图片，需要做成摇签动画

**实现方式**：
```typescript
// FortuneAnimation组件
const [currentFrame, setCurrentFrame] = useState(1)
const frameCount = 10
const frameDuration = 150  // 每帧150ms

// 循环播放3次后完成
const animate = () => {
  setTimeout(() => {
    setCurrentFrame(prev => {
      if (prev >= frameCount) {
        loops++
        if (loops >= maxLoops) {
          onComplete()
          return frameCount
        }
        return 1
      }
      return prev + 1
    })
    animate()
  }, frameDuration)
}
```

**图片命名规范**：`Q版道童摇签循环图生成-1.png` 到 `Q版道童摇签循环图生成-10.png`
**存放位置**：`/public/fortune-animation/`

### 5.20 Next.js App Router <head>标签陷阱（已验证）

**问题**：在layout.tsx中添加`<head>`标签会导致白屏

```tsx
// ❌ 错误：Next.js App Router不允许在组件中添加<head>
<html lang="zh-CN">
  <head>
    <link href="https://fonts.googleapis.com/..." rel="stylesheet" />
  </head>
  <body>...</body>
</html>

// ✅ 正确：使用metadata或globals.css中的@import
<html lang="zh-CN">
  <body style={{ fontFamily: "'Noto Sans SC', 'PingFang SC', sans-serif" }}>
    {children}
  </body>
</html>
```

### 5.21 万年历集成到首页（已验证）

**阿戴要求**：在首页功能概览区域上方加入万年历区域

**组件结构**：
- CalendarSection.tsx - 独立组件，包含完整万年历功能
- 使用查表法获取准确农历数据
- 支持日期选择器（点击展开日历）
- 显示：公历、农历、干支年/月/日、生肖、五行、节气、时辰、宜忌

**首页布局顺序**：
1. Hero区域
2. 每日一卦
3. 万年历
4. 功能概览
5. 使用指南
6. 知识图解

**⚠️ 阿戴会要求交换区域位置**，如"把万年历区域和每日一卦区域换个位置"，需要灵活调整。

### 5.18 日期选择器（已验证）

**阿戴要求**："不要前一天后一天直接可以选择日历"

**实现方式**：点击日期区域展开日历选择器
```tsx
const [showCalendar, setShowCalendar] = useState(false)

{/* 点击展开日历 */}
<div className="inline-block cursor-pointer" onClick={() => setShowCalendar(!showCalendar)}>
  <div className="text-4xl font-bold">{selectedDate.getFullYear()}年...</div>
  <div className="text-lg">{showCalendar ? '收起日历' : '选择日期'}</div>
</div>

{/* 日历选择器 */}
{showCalendar && (
  <div className="mb-6 p-4 rounded-lg">
    {/* 月份导航 */}
    {/* 星期标题 */}
    {/* 日期网格 */}
  </div>
)}
```

**交互动画**：
- 日历展开/收起过渡效果
- 日期选择过渡效果
- 信息卡片hover放大效果

### 5.4.1 重写页面时保留所有内容（严重警告）

**阿戴原话**："怎么只有这么点页面了"

**问题**：重写page.tsx时只写了Hero区域，丢失了下方的功能概览、使用指南、知识图解等所有section。

**规则**：重写任何页面前，必须：
1. 先读取现有完整文件（read_file，不要limit截断）
2. 列出所有现有section清单
3. 重写时确保每个section都在
4. 写完后对比确认没有丢失

**这是阿戴的严重痛点，违反会极度烦躁。**

### 5.5 Word文档中的图片查看

```bash
# 用Preview打开Word文档
open -a "Preview" "/path/to/document.doc"

# 滚动查看
osascript -e 'tell application "System Events" to key code 125'  # 向下

# 截图
screencapture -x /tmp/screenshot.png

# 用vision_analyze查看截图内容
```

### 5.6 卦象符号实现（已验证）

**用户明确要求的卦象对应**：
- 梅花易数：乾卦（☰）- 三条实线
- 四柱八字：离卦（☲）- 实线、断线、实线
- 每日一签：兑卦（☱）- 实线、实线、断线

**React组件实现**：
```tsx
// 卦象爻线组件
function YaoLine({ isYang }: { isYang: boolean }) {
  if (isYang) {
    return <div className="w-16 h-1.5 bg-white/90 rounded-full mx-auto"/>
  }
  return (
    <div className="flex justify-center gap-2 mx-auto">
      <div className="w-6 h-1.5 bg-white/90 rounded-full"/>
      <div className="w-6 h-1.5 bg-white/90 rounded-full"/>
    </div>
  )
}

// 卦象组件
function TrigramSymbol({ lines }: { lines: boolean[] }) {
  return (
    <div className="flex flex-col gap-2.5">
      {lines.map((isYang, index) => (
        <YaoLine key={index} isYang={isYang}/>
      ))}
    </div>
  )
}

// 使用示例
<TrigramSymbol lines={[true, true, true]}/>   // 乾卦
<TrigramSymbol lines={[true, false, true]}/>   // 离卦
<TrigramSymbol lines={[true, true, false]}/>   // 兑卦
```

### 5.7 Scroll-Based Color Transition (Apple Style)

When the user wants a white→dark scroll-driven background transition:

```typescript
'use client'
const [scrollProgress, setScrollProgress] = useState(0)

useEffect(() => {
  const handleScroll = () => {
    const scrollTop = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = Math.min(scrollTop / docHeight, 1)
    setScrollProgress(progress)
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
  return () => window.removeEventListener('scroll', handleScroll)
}, [])

// Background: white (245,240,230) → dark (10,10,15)
const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`

// Dynamic text colors
const textColor = scrollProgress > 0.5 ? '#fff' : '#111827'
const textMuted = scrollProgress > 0.5 ? 'rgba(255,255,255,0.6)' : '#6b7280'
```

**⚠️ Critical Pitfall**: Tailwind className (`text-gray-900`, `bg-white`) are STATIC — they don't respond to scroll. You MUST use `style={{ color: textColor }}` for scroll-driven colors. If you try to replace className strings with style objects via sed, it breaks JSX syntax. Define color variables once, use them everywhere.

**⚠️ Critical Pitfall**: globals.css `body { background: #0a0a0f; }` OVERRIDES React inline styles. Set `body { background: transparent; }` in globals.css so the React component's `style={{ backgroundColor: bgColor }}` takes effect.

### 5.8 Video Transparency for Character Animations

To show only a character (no background) from a video:

```bash
# Convert MP4 to WebM with alpha channel (VP9)
ffmpeg -i input.mp4 \
  -vf "colorkey=0x0a0a0f:0.1:0.2,format=yuva420p" \
  -c:v libvpx-vp9 -b:v 2M -an \
  -y output-transparent.webm
```

```tsx
<video autoPlay loop muted playsInline className="w-64 h-64 object-cover">
  <source src="/output-transparent.webm" type="video/webm" />
  <source src="/input.mp4" type="video/mp4" />  {/* fallback */}
</video>
```

**⚠️ Pitfall**: `mix-blend-multiply` CSS can make video invisible on light backgrounds. Test without it first.

### 5.9 lunar-javascript在Next.js中的使用

**安装**：
```bash
npm install lunar-javascript
```

**万年历页面实现**：
```typescript
'use client'
import { Solar, Lunar } from 'lunar-javascript'

// 阳历转农历
const solar = Solar.fromDate(new Date())
const lunar = solar.getLunar()

// 获取农历信息
lunar.getDayInChinese()      // "初一"、"初二"等
lunar.getMonthInChinese()    // "正"、"二"等
lunar.getYearInGanZhi()      // "丙午"
lunar.getYearShengXiao()     // "马"

// 节气
lunar.getJieQi()             // 当天节气（如有）
lunar.getPrevJieQi()         // 上一节气
lunar.getNextJieQi()         // 下一节气
```

**⚠️ 已知问题**：
- `lunar.getJieQi()` 返回的是节气名称字符串或null
- `prevJieQi` 对象只有 `getName()` 方法，没有 `getMonth()` 和 `getDay()` — 调用会报 TypeError
- 干支月柱计算可能有误差（需验证）
- `getDayInChinese()` 返回 "初一"、"初二"等
- `getMonthInChinese()` 返回 "正"、"二"等

### 5.10 Canvas Animation Hook Ordering (React)

```tsx
// ❌ WRONG: useRef after useEffect that uses it
useEffect(() => {
  if (canvasRef.current) initAnimation(canvasRef.current)  // canvasRef not yet declared!
}, [mounted])
const canvasRef = useRef<HTMLCanvasElement>(null)

// ✅ CORRECT: Declare first, use in separate useEffect
const canvasRef = useRef<HTMLCanvasElement>(null)
useEffect(() => { setMounted(true) }, [])
useEffect(() => {
  if (canvasRef.current) initAnimation(canvasRef.current)
}, [mounted])  // Runs after mount when canvas exists
```

**⚠️ Pitfall**: If canvas shows `hasContent: false` but element exists, the animation function likely ran before the canvas was bound. Use a separate `useEffect` dependent on `mounted` state.

### 5.11 Word Doc Image Extraction

When user says "图片自己在word文件中看" or provides a .doc file:

```bash
# 1. Open in Preview.app (supports .doc on macOS)
open -a "Preview" "/path/to/document.doc"

# 2. Wait for load
sleep 3

# 3. Screenshot
screencapture -x /tmp/word-screenshot.png

# 4. Scroll down for more content
for i in {1..5}; do
  osascript -e 'tell application "System Events" to key code 125'  # Arrow Down
  sleep 0.5
done

# 5. Screenshot again
screencapture -x /tmp/word-scroll1.png

# 6. Use vision_analyze to examine each screenshot
```

**⚠️ Pitfall**: `textutil -convert txt` loses all images. Must use Preview.app + screencapture to see embedded images.

### 5.8 万年历接入到各个功能页面（已验证）

**梅花易数时间起卦**（使用农历）：
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

**每日一签时辰显示**：
```typescript
// 获取当前时辰（使用农历）
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
useEffect(() => {
  const now = new Date()
  const solar = Solar.fromDate(now)
  const lunar = solar.getLunar()
  setLunarInfo(`农历${lunar.getMonthInChinese()}月${lunar.getDayInChinese()} ${lunar.getYearInGanZhi()}年`)
}, [])
```

**⚠️ 关键点**：
- 梅花易数必须使用农历时间起卦，不能用阳历
- 每日一签需要显示当前时辰和农历信息
- 万年历页面需要同时显示阳历和农历

### 5.9 Apple风格滚动渐变背景（已验证）

**效果**：米白色背景 → 滚动时慢慢变暗 → 底部变成黑色

**实现**：
```typescript
// 1. globals.css中body背景必须设为透明
body {
  background: transparent;  // ❌ 不能用 var(--xuan-black)
}

// 2. 监听滚动事件
const [scrollProgress, setScrollProgress] = useState(0)

useEffect(() => {
  const handleScroll = () => {
    const scrollTop = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = Math.min(scrollTop / docHeight, 1)
    setScrollProgress(progress)
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
  return () => window.removeEventListener('scroll', handleScroll)
}, [])

// 3. 动态计算背景色
const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`

// 4. 应用到容器
<div style={{ backgroundColor: bgColor }}>
```

**⚠️ 关键陷阱**：
- globals.css中`body { background: var(--xuan-black) }`会覆盖React的inline style
- 必须改为`body { background: transparent }`才能让动态背景生效
- 所有文字、按钮颜色都要随scrollProgress变化（深色文字→浅色文字）

### 5.10 Canvas动画初始化陷阱（已验证）

**问题**：Canvas动画不显示，canvas元素存在但内容为空

**原因**：useEffect中canvasRef.current可能还未绑定到DOM元素

**解决方案**：使用单独的useEffect依赖mounted状态
```typescript
// ❌ 错误：canvasRef.current可能为null
useEffect(() => {
  if (canvasRef.current) {
    initMonkAnimation(canvasRef.current)
  }
}, [])

// ✅ 正确：等mounted为true后再初始化
useEffect(() => {
  setMounted(true)
}, [])

useEffect(() => {
  if (canvasRef.current) {
    initMonkAnimation(canvasRef.current)
  }
}, [mounted])
```

### 5.11 Next.js常见构建错误（已验证）

**阿戴原话**："那你别按模块拆分啊，这是画布项目的。你按照正常工程文件整理好全部给工程师啊，前后端所有代码都要。" "以后都这样整理文件"

**禁止按模块拆分**，必须按标准工程文件结构整理：

```
项目名/
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router
│   │   ├── pages/        # 页面
│   │   ├── components/   # 组件
│   │   ├── contexts/     # Context
│   │   ├── hooks/        # Hooks
│   │   ├── stores/       # 状态管理
│   │   ├── lib/          # 工具函数
│   │   └── types/        # 类型定义
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── postcss.config.js
│
└── backend/
    ├── main.py
    ├── requirements.txt
    └── ...
```

**必须包含的配置文件**：package.json、tsconfig.json、next.config.js、tailwind.config.ts、postcss.config.js、requirements.txt、README.md

### 5.10 suanlemeai.cn首页排版结构（已逆向）

完整首页从上到下9个区块：

1. **Hero区域** - 八卦符号+背景散字+发光标题"算了么"+拼音+哲学标语+两个CTA按钮
2. **功能概览** - "一屏入局，诸术同参" + 27工具/55古籍/78塔罗统计 + 8个功能卡片
3. **使用指南** - "观象不是堆工具，先把问法立住" + 4步骤（定时→取象→断事→复核）
4. **每日一卦** - 今日卦象预览 + CTA按钮
5. **知识图解** - 6个教育模块（五行生克环、洛书九宫、八字判断顺序、起卦到断卦、二十四节气、六壬四课三传）
6. **服务方式** - 0元/3引擎/100%本地计算/30元月起
7. **时间签文** - 随机道藏话语
8. **关于** - 品牌介绍
9. **页脚** - 导航链接

详见 `references/suanlemeai-homepage-layout.md`

### 5.11 Word文档UI设计图查看方法（已验证）

**阿戴原话**："图片自己在word文件中看"

当用户提供.doc文件包含UI设计图时，不能只提取文字，必须查看图片：

```bash
# 1. 用Preview打开Word文档
open -a "Preview" "/path/to/document.doc"

# 2. 等待文档加载
sleep 3

# 3. 截图当前页面
screencapture -x /tmp/word-screenshot.png

# 4. 用vision_analyze查看截图
# 问题示例："请详细描述文档中的UI设计图内容"

# 5. 滚动查看更多内容
for i in {1..5}; do
    osascript -e 'tell application "System Events" to key code 125'
    sleep 0.5
done

# 6. 继续截图和分析
screencapture -x /tmp/word-scroll1.png
```

**⚠️ 关键点**：
- `.doc`是二进制格式，textutil只能提取文字不能提取图片
- 必须用Preview打开然后截图，再用vision_analyze分析
- 每次滚动后都要截图，确保看到所有设计图

### 5.12 lunar-javascript API陷阱补充

```typescript
// prevJieQi 只有 getName() 方法
lunar.getPrevJieQi()?.getName()  // ✅ "小暑"
// lunar.getPrevJieQi()?.getMonth()  // ❌ 不存在
// lunar.getPrevJieQi()?.getDay()    // ❌ 不存在

// getDayInChinese() 返回 "初一"、"初二" 等
// getMonthInChinese() 返回 "正"、"二" 等
// 不是数字，是中文
```

### 5.13 获取网站真实HTML源码方法（已验证）

**web_extract返回的是markdown格式，不是原始HTML！** 要获取真实源码必须用curl：

```bash
# ✅ 正确：curl获取原始HTML
curl -s -L "https://suanlemeai.cn/" -o /tmp/index.html
# 然后用正则提取script/link标签
grep -oE 'src="[^"]*\.js"' /tmp/index.html
grep -oE 'href="[^"]*\.css"' /tmp/index.html

# ❌ 错误：web_extract返回markdown，没有script/link标签
```

**批量下载JS/CSS文件**：
```bash
# 从HTML中提取资源URL后批量下载
curl -s -L "https://suanlemeai.cn/_next/static/css/xxx.css" -o ./css/xxx.css
curl -s -L "https://suanlemeai.cn/_next/static/chunks/xxx.js" -o ./js/xxx.js
```

### 5.14 Next.js常见构建错误（已验证）

**函数提升问题**：
```typescript
// ❌ 错误：useEffect中调用未定义的函数
useEffect(() => {
  generateCalendar(year, month)  // ReferenceError!
}, [])

const generateCalendar = (year, month) => { ... }

// ✅ 正确：先定义函数，再在useEffect中调用
const generateCalendar = (year, month) => { ... }

useEffect(() => {
  generateCalendar(year, month)
}, [])
```

**TypeScript状态类型扩展**：
```typescript
// ❌ 错误：状态类型不包含新增字段
const [currentQian, setCurrentQian] = useState<typeof qianData[0] | null>(null)
// 添加lunarTime字段后会报错

// ✅ 正确：用交叉类型扩展
const [currentQian, setCurrentQian] = useState<
  (typeof qianData[0] & { lunarTime: string; shichen: string; randomNum: number }) | null
>(null)
```

**模块路径解析失败**：
```
Module not found: Can't resolve '@/contexts/auth-context'
Module not found: Can't resolve '@/stores/workflow-store-jotai'
```

**原因**：源码按模块拆分（module1-state、module2-hooks等），但没有按Next.js标准目录结构组织。

**解决方案**：
```
module6-account/auth-context.tsx  →  src/contexts/auth-context.tsx
module2-hooks/use-keyboard-shortcuts.ts  →  src/hooks/use-keyboard-shortcuts.ts
module1-state/  →  src/stores/
module4-canvas/  →  src/components/canvas/
```

---

## 六、项目结构模板

```
project/
├── package.json
├── next.config.js
├── tailwind.config.ts
├── postcss.config.js
├── tsconfig.json
└── src/
    ├── app/
    │   ├── layout.tsx          # 根布局
    │   ├── page.tsx            # 首页
    │   ├── globals.css         # 全局样式（道教风格）
    │   ├── meihua/page.tsx     # 梅花易数
    │   ├── bazi/page.tsx       # 四柱八字
    │   ├── qian/page.tsx       # 每日一签
    │   ├── books/page.tsx      # 古籍书楼
    │   └── calendar/page.tsx   # 万年历
    ├── components/
    │   ├── Navbar.tsx
    │   ├── Footer.tsx
    │   └── TaijiSymbol.tsx
    └── lib/
        ├── meihua.ts           # 梅花易数算法
        ├── bazi.ts             # 四柱八字算法
        └── qian-data.ts        # 签文数据库
```

### execute_code文件操作危险（已验证）
**问题**: 用execute_code的Python脚本批量修改.tsx文件时，如果字符串替换模式不精确匹配，会破坏文件结构，导致Next.js编译失败（"Unexpected token `div`. Expected jsx identifier"）。
**教训**: 批量修改多个文件时，不要用execute_code做字符串替换。应该逐个文件用skill_manage(action='patch')或直接write_file重写。
**已损坏文件**: page.tsx（首页）、daily-lot/page.tsx、calendar/page.tsx — 全部需要重写修复。

## 附录：算法速查

### 卦气值日算法
60卦（去掉乾坤坎离四正卦）从冬至开始循环，每卦主管约6天。完整60卦序列和实现代码见 `references/guaqi-daily-algorithm.md`。

### 万年历计算
- **禁止用数学公式计算农历**，必须用查表法或 `lunar-javascript` 库
- lunar-javascript SSR陷阱：必须用 `useState`+`useEffect`，不能用 `useMemo`
- 方法名陷阱：`getXiu()` 不是 `getDayXiu()`，`getJieQi()` 无节气时返回空字符串

> 📎 完整算法实现: `references/chinese-metaphysics-algorithms.md`
> 📎 农历/干支/签文系统: `references/chinese-metaphysics-calendar.md`
> 📎 小算项目开发指南: `references/xiaosuan-project-guide.md`

## Consolidated From (archived skills)

This skill consolidates content from the following previously separate skills (archived in `~/.hermes/skills/.archive/`):

| Former Skill | Unique Content | Archive References |
|---|---|---|
| `ai-fortune-telling-platform` | 三种数术完整算法、竞品分析、开源库选型、合规策略、lunar-python陷阱 | `references/open-source-divination-libraries.md`, `references/three-divination-algorithms.md`, `references/deepseek-qimen-corrections.md`, `references/lunar-python-pitfalls.md`, `references/suanlemeai-reverse-engineering.md`, `references/website-architecture.md`, `references/lunar-javascript-integration-patterns.md` |
| `chinese-divination-platform` | 梅花易数Python算法、小算项目创建流程 | `references/xiaosuan-project-workflow.md`, `references/lunar-python-gotchas.md` |
| `lunar-python-api` | lunar-python/lunar-javascript API正确用法和陷阱 | `references/lunar-javascript-api.md` |

> **Note**: The archived skills' reference files are preserved in their original `.archive/` directories. If you need content from the archived references, access them from `~/.hermes/skills/.archive/<skill-name>/references/`.

### lunar-python / lunar-javascript API Pitfalls (from lunar-python-api)

**Critical**: `Lunar.fromYmdHms()` receives **lunar** dates, not solar! Always use `Solar.fromYmdHms().getLunar()` for solar→lunar conversion.

**EightChar methods**: No `getShiShenGan()` or `getWuXing()` — use per-pillar methods: `getYearShiShenGan()`, `getMonthShiShenGan()`, etc.

**getYun()**: On EightChar object, not Lunar: `lunar.getEightChar().getYun(gender)`

**lunar-javascript Next.js**: Must use static imports (not `await import()`), needs TypeScript declarations, needs `transpilePackages` config. SSR serialization loses methods — use `useState`+`useEffect` not `useMemo`. JieQi must be stored as plain `{name, solar}` objects.

**LunarTime method names differ from Lunar**: `getYi()`/`getJi()` not `getDayYi()`/`getDayJi()`. `getXiu()`/`getXiuLuck()` not `getDayXiu()`/`getDayXiuLuck()`. `getJieQi()` returns string or object — check with `typeof`.

> Full API reference: archived in `~/.hermes/skills/.archive/lunar-python-api/references/lunar-javascript-api.md`
> Type declarations: see `references/lunar-javascript-type-declarations.md` in xiaosuan-project skill

## References

| File | Contents |
|------|----------|
| `references/apple-scroll-gradient.md` | Apple风格滚动渐变背景实现（米白→黑） |
| `references/canvas-animation-react.md` | Canvas动画在React中的实现模式（小道童角色） |
| `references/word-document-image-extraction.md` | Word文档中的图片查看方法 |
| `references/meihua-algorithms.md` | 梅花易数完整算法 |
| `references/lunar-javascript-nextjs.md` | lunar-javascript在Next.js中的使用（万年历、农历转换） |
| `references/xiaodaoshi-animation.md` | 小道童扫地Canvas动画实现（角色设计+代码+React集成） |
| `references/p5js-animation.md` | p5.js动画实现（复杂角色动画） |
| `references/i18n-language-selection.md` | 多语言/i18n支持实现（中/繁/英/日） |
| `references/video-animation-integration.md` | 视频动画集成（MP4替换Canvas） |
| `references/video-background-removal.md` | 视频去背景（ffmpeg colorkey转WebM透明） |
| `references/i18n-language-selector-custom.md` | 语言选择器自定义（去图标、动态颜色、品牌命名） |
| `references/video-animation-workflow.md` | 视频动画工作流（Canvas→Video→删除） |
| `references/iterative-ui-refinement.md` | 迭代式UI精炼模式（阿戴的调整偏好） |
| `references/guaqi-daily-algorithm.md` | 卦气值日算法详解（汉代孟喜卦气说，64卦数据结构） |
| `references/calendar-integration.md` | 万年历集成指南（lunar-javascript使用，宜忌数据） |
| `references/lunar-calendar-lookup.md` | 农历查表法参考（禁止数学公式，2026年数据示例） |
---

## 十一、语言选择器自定义（已验证）

### 去除地球图标

阿戴要求语言选择器简洁，不要地球图标：

```tsx
// ❌ 有图标
<span className="text-sm">🌐</span>
<span className="text-sm">{currentLocale.name}</span>

// ✅ 无图标，只显示语言名
<span className="text-sm" style={{ color }}>{currentLocale.name}</span>
```

### 动态颜色传递

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

详见 `references/i18n-language-selector-custom.md`

## 十二、迭代式UI精炼模式（重要）

### 阿戴的UI调整模式

阿戴会反复要求UI调整，通常是简化和删除：

**常见删除请求**：
- 删除地球图标（🌐）
- 删除按钮旁的表情包（🎋）
- 删除按钮箭头（→）
- 删除装饰性标签（如"东方命理，云海问卦"）
- 删除小道童动画

**响应策略**：
- **立即执行**：当用户说"删了"或"这个删了"
- **不要问**：为什么删除、是否确认、建议保留
- **不要解释**：删除的影响、技术细节

### Rollback工作流

用户会反复要求"回退"，需要支持多级回退：

```
阶段1: Canvas动画 → 阶段2: 替换为Video → 阶段3: 去背景WebM → 阶段4: 删除动画
         ↑                  ↑                    ↑                ↑
       回退到这 ←──────── 回退到这 ←────────── 回退到这 ←────── 回退到这
```

**回退到Canvas动画**：恢复canvasRef、useEffect、initMonkAnimation函数
**回退到Video**：删除WebM source标签，只保留MP4
**回退到删除**：系统性删除useRef、useEffect、函数、import

**⚠️ 规则**：用户说"再回退"时，用clarify问具体回退到哪个阶段。如果用户没回复，按最佳判断选择上一个稳定状态。

### 导航栏最终结构

```
左侧：Logo(安) + 品牌名(小算)
右侧：语言选择器(中文) + 登录按钮(✦ 登录) + 汉堡菜单(☰)
```

**汉堡菜单按钮**（登录按钮右边）：
```tsx
<button className="w-10 h-10 rounded-full flex items-center justify-center hover:opacity-90 transition-colors"
  style={{ backgroundColor: scrollProgress > 0.5 ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)' }}>
  <div className="flex flex-col gap-1.5">
    <div className="w-5 h-0.5" style={{ backgroundColor: textColor900 }}/>
    <div className="w-5 h-0.5" style={{ backgroundColor: textColor900 }}/>
    <div className="w-5 h-0.5" style={{ backgroundColor: textColor900 }}/>
  </div>
</button>
```

**⚠️ 规则**：阿戴问"XXX右边的导航栏呢"= 缺少UI元素，立即添加不要问。

---

## 十二、字体文件整理（已验证）

### Geist字体（Vercel开源）

画布项目使用Geist字体，需要整理成工程文件：

**下载地址**：
```bash
curl -L -o GeistVF.woff "https://github.com/vercel/geist-font/raw/main/fonts/GeistVF.woff"
curl -L -o GeistMonoVF.woff "https://github.com/vercel/geist-font/raw/main/fonts/GeistMonoVF.woff"
```

**字体文件结构**：
```
画布网站字体文件/
├── GeistVF.woff          # 主字体（无衬线，304KB）
├── GeistMonoVF.woff      # 等宽字体（304KB）
├── fonts.css             # @font-face配置
└── README.md             # 使用说明
```

**Next.js集成**：
```tsx
import localFont from "next/font/local";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-sans",
  weight: "100 900",
});
```

**⚠️ Pitfall**：layout.tsx引用字体文件但文件不存在时，Next.js构建会失败但开发模式可能不报错（显示空字体）。必须确认字体文件实际存在。

---

## 十三、迭代式UI精炼模式（重要）

| 元素 | 最终值 | 历史变更 |
|------|--------|----------|
| Logo | 安 | 算 → 安 |
| 品牌名 | 小算 | 算了么 → 小算一下 → 小算 |
| 主按钮 | 小算一下 | 小算一下 → → 小算一下 |
| 次按钮 | 每日一签 | 🎋 每日一签 → 每日一签 |
| 标语 | 已删除 | 东方命理，云海问卦 → 删除 |

### 滚动渐变颜色系统

**所有元素都要随滚动变化**：
- 背景色：米白色 → 黑色
- 文字颜色：黑色 → 白色
- 按钮颜色：深色 → 浅色
- 卡片背景：白色 → 半透明
- 边框颜色：浅灰 → 半透明白色
- 图标颜色：深色 → 浅色

**实现方式**：
```typescript
// 颜色辅助函数
const getTextColor = (progress: number, light: string, dark: string) => 
  progress > 0.5 ? light : dark

// 在组件外计算颜色变量
const textColor900 = getTextColor(scrollProgress, '#fff', '#111827')
const textColor500 = getTextColor(scrollProgress, 'rgba(255,255,255,0.6)', '#6b7280')

// 在JSX中使用
<h1 style={{ color: textColor900 }}>标题</h1>
<p style={{ color: textColor500 }}>正文</p>
```

**⚠️ Pitfall**：Tailwind的className（如`text-gray-900`）是静态的，不会随滚动变化。必须使用style属性。

详见 `references/iterative-ui-refinement.md`

## 十三、视频动画工作流（已验证）

### 完整工作流：Canvas → Video → 删除

**阶段1**：Canvas动画实现（useRef + requestAnimationFrame）
**阶段2**：替换为MP4视频（用户提供动画文件）
**阶段3**：视频去背景（ffmpeg colorkey转WebM透明）
**阶段4**：完全删除动画

### ⚠️ Pitfalls

1. **mix-blend-multiply隐藏视频**：视频背景是白色时，混合模式会使视频不可见
2. **视频不自动播放**：必须同时添加`autoPlay`和`muted`属性
3. **删除代码不完整**：系统性删除useRef、useEffect、函数定义、import

详见 `references/video-animation-workflow.md`

---

## 七、Apple风格滚动渐变背景（已验证）

### 实现原理

页面背景色随滚动进度从米白色渐变到黑色：

```typescript
const [scrollProgress, setScrollProgress] = useState(0)

useEffect(() => {
  const handleScroll = () => {
    const scrollTop = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = Math.min(scrollTop / docHeight, 1)
    setScrollProgress(progress)
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
  return () => window.removeEventListener('scroll', handleScroll)
}, [])

// 背景色：米白色(245,240,230) → 黑色(10,10,15)
const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`
```

### ⚠️ 关键Pitfall：globals.css body背景色会覆盖React style

```css
/* ❌ 错误：这会覆盖React的inline style */
body {
  background: var(--xuan-black); /* 黑色，覆盖一切 */
}

/* ✅ 正确：设为transparent让React控制 */
body {
  background: transparent;
}
```

**症状**：scrollProgress计算正确，但背景色不变。
**原因**：CSS specificity - CSS的body样式优先级高于React的inline style。
**解决**：`body { background: transparent; }`，让React组件的style控制背景色。

### 文字/按钮颜色也要随滚动变化

```tsx
style={{ color: scrollProgress > 0.5 ? '#fff' : '#333' }}
style={{ backgroundColor: `rgba(${scrollProgress > 0.5 ? 255 : 0}, ...)` }}
```

---

## 八、Canvas动画在React中的初始化（已验证）

### ⚠️ 关键Pitfall：useRef + useEffect时序

```typescript
// ❌ 错误：canvasRef.current可能还没绑定
useEffect(() => {
  setMounted(true)
  if (canvasRef.current) {
    initAnimation(canvasRef.current)  // 可能是null！
  }
}, [])

// ✅ 正确：分开两个useEffect，依赖mounted
useEffect(() => {
  setMounted(true)
}, [])

useEffect(() => {
  if (canvasRef.current) {
    initAnimation(canvasRef.current)  // mounted后canvas一定存在
  }
}, [mounted])
```

**症状**：canvas元素存在但无内容（所有像素alpha=0）。
**原因**：首次渲染时canvasRef还没绑定，initAnimation在canvas挂载前执行。
**解决**：把canvas初始化放在依赖mounted的单独useEffect中。

### Canvas动画函数模板

```typescript
function initMonkAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  let time = 0
  const width = canvas.width
  const height = canvas.height

  function draw() {
    ctx.clearRect(0, 0, width, height)
    time += 0.03
    // ... 绘制逻辑 ...
    requestAnimationFrame(draw)
  }
  draw()
}
```

### 检查Canvas是否有内容

```javascript
// 在浏览器控制台执行
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
let nonZeroPixels = 0;
for (let i = 3; i < imageData.data.length; i += 4) {
  if (imageData.data[i] > 0) nonZeroPixels++;
}
console.log('Has content:', nonZeroPixels > 0);
```

---

## 九、多语言/i18n支持（已验证）

### 语言选择器实现

**支持语言**：简体中文、繁體中文、English、日本語

**文件结构**：
```
src/
├── lib/
│   └── i18n.ts                    # 语言配置、翻译文本、t()函数
├── components/
│   └── LanguageSelector.tsx       # I18nProvider + LanguageSelector组件
└── app/
    └── layout.tsx                 # 包裹I18nProvider
```

**i18n.ts核心结构**：
```typescript
export type Locale = 'zh-CN' | 'zh-TW' | 'en' | 'ja'

export const translations: Record<Locale, Record<string, string>> = {
  'zh-CN': { 'hero.brand': '小算', 'hero.cta': '小算一下', ... },
  'zh-TW': { 'hero.brand': '小算', 'hero.cta': '小算一下', ... },
  'en': { 'hero.brand': 'Xiao Suan', 'hero.cta': 'Start Reading', ... },
  'ja': { 'hero.brand': '小算', 'hero.cta': '占い始める', ... },
}

export function t(key: string, locale: Locale): string {
  return translations[locale]?.[key] || translations['zh-CN']?.[key] || key
}
```

**LanguageSelector组件**：
```typescript
'use client'
import { createContext, useContext, useState, useEffect } from 'react'

const I18nContext = createContext({ locale: 'zh-CN', setLocale: () => {}, t: (k: string) => k })

export function I18nProvider({ children }) {
  const [locale, setLocale] = useState('zh-CN')
  useEffect(() => {
    const saved = localStorage.getItem('locale')
    if (saved) setLocale(saved)
  }, [])
  // ...
}

export function LanguageSelector() {
  // 下拉菜单：🌐图标 + 当前语言名 + 箭头
  // 选项：🇨🇳 简体中文 / 🇹🇼 繁體中文 / 🇺🇸 English / 🇯🇵 日本語
}
```

**页面中使用**：
```typescript
const { t } = useI18n()
<h1>{t('hero.brand')}</h1>
<Link href="/tools">{t('hero.cta')}</Link>
```

**⚠️ 关键点**：
- 传统文化专有名词（五行、九宫、八字等）在英文/日文模式下可保留中文
- 语言设置保存到localStorage
- I18nProvider包裹在layout.tsx中

### 动态颜色系统（滚动主题）

**问题**：Tailwind的固定颜色类（如`text-gray-900`）不会随滚动变化

**解决方案**：使用辅助函数动态计算颜色

```typescript
// 颜色辅助函数
const getTextColor = (scrollProgress: number, lightColor: string, darkColor: string) => {
  return scrollProgress > 0.5 ? lightColor : darkColor
}

const getBgColor = (scrollProgress: number, lightColor: string, darkColor: string) => {
  return scrollProgress > 0.5 ? lightColor : darkColor
}

// 在组件中使用
const textColor900 = getTextColor(scrollProgress, '#fff', '#111827')
const textColor500 = getTextColor(scrollProgress, 'rgba(255,255,255,0.6)', '#6b7280')
const bgColorWhite = getBgColor(scrollProgress, 'rgba(255,255,255,0.1)', '#fff')

// JSX中应用
<h1 style={{ color: textColor900 }}>标题</h1>
<p style={{ color: textColor500 }}>正文</p>
<div style={{ backgroundColor: bgColorWhite }}>卡片</div>
```

**⚠️ Pitfall: 不能用sed批量替换Tailwind类**
尝试用sed把`text-gray-900`替换为`style={{ ... }}`会破坏JSX语法（重复的style属性）。
必须手动创建颜色变量，然后在每个元素上应用。

**颜色映射参考**：
| Tailwind类 | 深色模式(scrollProgress>0.5) | 浅色模式(scrollProgress<0.5) |
|------------|---------------------------|---------------------------|
| text-gray-900 | #fff | #111827 |
| text-gray-700 | rgba(255,255,255,0.8) | #374151 |
| text-gray-500 | rgba(255,255,255,0.6) | #6b7280 |
| text-gray-400 | rgba(255,255,255,0.5) | #9ca3af |
| bg-white | rgba(255,255,255,0.1) | #fff |
| bg-gray-50 | rgba(255,255,255,0.05) | #f9fafb |
| border-gray-200 | rgba(255,255,255,0.2) | #e5e7eb |

---

### 十、视频动画集成（已验证）

### 替换Canvas动画为MP4视频

**场景**：用户提供的动画文件（MP4格式）需要集成到页面中

**实现**：
```tsx
<video
  autoPlay
  loop
  muted
  playsInline
  className="w-64 h-64 object-cover rounded-lg shadow-lg"
>
  <source src="/xiaodaoshi.mp4" type="video/mp4" />
</video>
```

**⚠️ 关键属性**：
- `autoPlay` + `muted`：现代浏览器要求静音才能自动播放
- `playsInline`：iOS内联播放
- `loop`：循环播放
- 视频文件放在`/public/`目录下

**样式调整**：
- `object-cover`：裁剪适配
- `rounded-lg`：圆角
- `shadow-lg`：阴影
- 可加`mix-blend-multiply`实现背景融合（但可能使视频不可见）

**⚠️ Pitfall: mix-blend-multiply可能隐藏视频**
如果视频背景是白色的，`mix-blend-multiply`会使视频与背景融合而不可见。先不加混合模式，确认可见后再调整。

### 视频去背景（ffmpeg色度键）

**场景**：用户要求"只要人物，背景透明色"

**实现**：使用ffmpeg的`colorkey`滤镜去除纯色背景，转换为WebM格式（支持alpha通道）

```bash
# 去除黑色背景，转换为透明WebM
ffmpeg -i input.mp4 \
  -vf "colorkey=0x0a0a0f:0.1:0.2,format=yuva420p" \
  -c:v libvpx-vp9 -b:v 2M -an \
  -y output-transparent.webm
```

**参数说明**：
- `colorkey=0x0a0a0f:0.1:0.2`：去除颜色(十六进制)、相似度(0-1)、混合度(0-1)
- `format=yuva420p`：带alpha通道的像素格式
- `libvpx-vp9`：VP9编码器，支持透明通道
- `-an`：去除音频（动画通常不需要）

**页面中使用**：
```tsx
<video autoPlay loop muted playsInline className="w-64 h-64 object-cover">
  <source src="/xiaodaoshi-transparent.webm" type="video/webm" />
  <source src="/xiaodaoshi.mp4" type="video/mp4" />  {/* 回退 */}
</video>
```

**⚠️ 关键点**：
- WebM VP9是唯一支持透明通道的Web视频格式
- 优先加载WebM透明版本，回退到MP4原版
- `colorkey`的颜色值需要从视频中提取（用ffmpeg截取第一帧分析）
- 相似度和混合度需要根据实际效果调整

---

## 十一、小算项目v2最终配置（已验证）

### 品牌配置

| 元素 | 值 | 说明 |
|------|-----|------|
| Logo | 安 | 圆形按钮中的书法字 |
| 品牌名 | 小算 | 导航栏显示 |
| 主标题 | 小算 | 页面中心大字 |
| 主按钮 | 小算一下 | 无箭头 |
| 次按钮 | 每日一签 | 无表情包 |
| 定价 | 完全免费 | 不显示任何价格 |

**⚠️ 阿戴的UI调整模式**（反复出现）：
- 删除装饰性标签（如"东方命理，云海问卦"）
- 删除按钮旁的表情包/emoji
- 删除按钮箭头（→）
- 简化、简化、再简化
- **规则：当用户说"删了"或"这个删了"，立即执行，不要问为什么**

### 首页结构（suanlemeai.cn风格）

1. **Hero区域** - 背景散字 + 发光主标题 + 双按钮
2. **功能概览** - 数字统计(27/55/78) + 8个功能卡片
3. **使用指南** - 4步骤(定时→取象→断事→复核)
4. **每日一卦** - 本卦/变卦展示
5. **知识图解** - 6个模块(五行/九宫/八字/起卦/节气/六壬)
6. **时间签文** - 随机道藏话语
7. **关于** - 免费+无广告

### 设计系统

- 背景：米白色→黑色滚动渐变
- 导航栏：毛玻璃效果(`backdrop-blur-xl`)
- 按钮：`hover:scale-105` + `hover:shadow-2xl` + `active:scale-95`
- 卡片：`hover:bg-white/10` + `hover:border-white/20`
- 文字：fadeInUp动画(0.2s-1.4s延迟)

---

## 更新日志

### v1.4.0 (2026-07-09)
- 新增：Rollback工作流（Canvas→Video→删除多级回退）
- 新增：导航栏最终结构（汉堡菜单按钮代码）
- 新增：字体文件整理（Geist字体下载+Next.js集成）
- 新增：UI元素缺失检测规则（"XXX右边的导航栏呢"=立即添加）

### v1.3.0 (2026-07-08)
- 新增：语言选择器自定义（去图标、动态颜色传递）
- 新增：迭代式UI精炼模式（阿戴的调整偏好）
- 新增：视频动画工作流（Canvas→Video→删除）
- 更新：品牌命名最终状态（小算、安logo）
- 更新：滚动渐变颜色系统完整指南

### v1.2.0 (2026-07-08)
- 新增：Apple风格滚动渐变背景
- 新增：Canvas动画在React中的初始化陷阱
- 新增：多语言/i18n支持
- 新增：视频去背景（ffmpeg colorkey）

### v1.1.0 (2026-07-08)
- 新增：Word文档UI提取流程
- 新增：suanlemeai.cn逆向分析
- 新增：项目文件结构规范

### v1.0.0 (2026-07-08)
- 初始版本
- 道教风格UI设计系统
- 核心页面设计
- 算法实现参考

---

**最后更新**: 2026-07-08
**基于项目**: 小算 v2、suanlemeai.cn逆向、天机阁
**许可**: MIT
