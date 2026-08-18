# TapNow 完整CSS变量系统 (getComputedStyle实测 2026-07-05)

## 提取方法
从`:root`选择器中提取，使用以下代码：
```javascript
(function() {
  var allVars = {};
  var sheets = document.styleSheets;
  for (var i = 0; i < sheets.length; i++) {
    try {
      var rules = sheets[i].cssRules;
      for (var j = 0; j < rules.length; j++) {
        if (rules[j].selectorText === ':root' || rules[j].selectorText === '.dark') {
          var style = rules[j].style;
          for (var k = 0; k < style.length; k++) {
            var prop = style[k];
            if (prop.startsWith('--')) {
              allVars[prop] = style.getPropertyValue(prop);
            }
          }
        }
      }
    } catch(e) {}
  }
  console.log(JSON.stringify(allVars, null, 2));
})();
```

## 背景色

```css
--background: #0f0f0f;           /* 主背景 */
--background-canvas: #0a0a0a;    /* 画布背景 */
--card: #1f1f1f;                 /* 卡片背景 */
--card-background: #1f1f1f;      /* 卡片背景（别名） */
--popover: #262626;              /* 弹出层背景 */
--chat-background: #141414;      /* 聊天背景 */
--chat-bubble-surface: #2e2e2e;  /* 聊天气泡 */
--chat-bubble-header: #1a1a1a;   /* 聊天气泡头部 */
--muted: #2b2b2b;                /* 静音区域背景 */
--sidebar: #1c1c1c;              /* 侧边栏背景 */
--sidebar-accent: #262626;       /* 侧边栏高亮 */
--accent: #404040;               /* 强调色背景 */
--secondary: #222;               /* 次要背景 */
--surface-secondary: #1f1f1f;    /* 次要表面 */
--input: #ffffff26;              /* 输入框背景 (15%白色) */
--ring: #7373731a;               /* 焦点环 */
--nav-bar-scrim: #1d1d1d85;      /* 导航栏遮罩 */
```

## 文字色

```css
--foreground: #f5f5f5;            /* 主文字 */
--card-foreground: #fafafa;       /* 卡片文字 */
--popover-foreground: #ccc;       /* 弹出层文字 */
--primary-foreground: #fafafa;    /* 主色调上的文字 */
--secondary-foreground: #f0f0f0;  /* 次要文字 */
--accent-foreground: #fafafa;     /* 强调色上的文字 */
--muted-foreground: #7a7a7a;      /* 静音文字 */
--text-text-primary: #e6e6e6;     /* 主要文字 */
--text-text-secondary: #9c9c9c;   /* 次要文字 */
--text-text-tertiary: #737373;    /* 三级文字 */
--secondary-muted-foreground: #a3a3a3; /* 次要静音文字 */
--sidebar-foreground: #cfcece;    /* 侧边栏文字 */
--sidebar-primary-foreground: #1c1c1c; /* 侧边栏主色调上的文字 */
--sidebar-accent-foreground: #fafafa; /* 侧边栏强调色上的文字 */
--chat-foreground: #d4d4d8;       /* 聊天文字 */
--destructive-foreground: #ff6163; /* 破坏性操作文字 */
```

## 主题色

```css
--primary: #1fa2dc;              /* 主色调（蓝色） */
--primary-selected-border: white; /* 选中边框 */
--tap-primary-1: #33a8ff;        /* TapNow主色1 */
--tap-primary-2: var(--color-blue-300); /* TapNow主色2 */
--tap-primary-3: #f6fafe;        /* TapNow主色3 */
--tap-pink: #e896c9;             /* 粉色 */
--tap-red: #db5a4d;              /* 红色 */
--star-active: #fdce8b;          /* 星标激活 */
--like-active: #fd9c8b;          /* 点赞激活 */
--accent-primary: #90c4e5;       /* 强调主色 */
```

## 边框

```css
--border: #ffffff1a;             /* 10%白色 */
--input: #ffffff26;              /* 15%白色 */
--primary-border: var(--color-zinc-600); /* 主边框 */
--sidebar-border: #ffffff1a;     /* 侧边栏边框 */
--sidebar-ring: #fafafaa3;       /* 侧边栏焦点环 */
--tap-lines: #ffffff80;          /* TapNow线条 (50%白色) */
```

## 圆角

```css
--radius: .75rem;                /* 12px - 全局圆角 */
```

## 字体

```css
--font-sans: Inter,sans-serif;
--font-serif: serif;
--font-mono: JetBrains Mono,monospace;
```

## 阴影

```css
--shadow-x: 0px;
--shadow-y: 2px;
--shadow-blur: 4px;
--shadow-spread: 0px;
--shadow-opacity: .1;
--shadow-color: #000;
--shadow-2xs: 0px 2px 4px 0px #0000000d;
--shadow-xs: 0px 2px 4px 0px #0000000d;
--shadow-sm: 0px 2px 4px 0px #0000001a, 0px 1px 2px -1px #0000001a;
--shadow: 0px 2px 4px 0px #0000001a, 0px 1px 2px -1px #0000001a;
--shadow-md: 0px 2px 4px 0px #0000001a, 0px 2px 4px -1px #0000001a;
--shadow-lg: 0px 2px 4px 0px #0000001a, 0px 4px 6px -1px #0000001a;
--shadow-xl: 0px 2px 4px 0px #0000001a, 0px 8px 10px -1px #0000001a;
--shadow-2xl: 0px 2px 4px 0px #00000040;
```

## 状态色

```css
--tap-state-success: #4caf50;
--tap-state-warning: #ff9800;
--tap-state-error: #f44336;
--tap-state-info: #2196f3;
--destructive: #934c4c;
```

## TapNow专属变量

```css
--tap-bg-1: #32454c;
--tap-bg-2: #2b373b;
--tap-text-1: white;
--tap-text-2: var(--color-zinc-300);
--tap-text-3: var(--color-zinc-400);
--tap-container-1: #0000004d;
--tap-container-2: #0000004d;
--tap-secondary: var(--color-zinc-500);
--tap-background: var(--color-zinc-950);
--tap-background-secondary: var(--color-zinc-800);
--tap-container-background: var(--color-zinc-900);
--tap-default-1: var(--color-zinc-400);
--tap-default-2: var(--color-zinc-500);
--tap-input-background: var(--color-zinc-700);
--tap-primary-card: var(--color-zinc-700);
--tap-gradient-pink: linear-gradient(90deg, #de77df 0%, #f8c4a7 100%);
--tap-gradient-red: linear-gradient(90deg, #dc3f44 0%, #db7555 81.25%);
--tap-primary-gradient: radial-gradient(circle, #5893be 0%, #c9f0ff 100%);
```

## 图表色

```css
--chart-1: #c6edfa;
--chart-2: #8dd8f3;
--chart-3: #4dc2eb;
--chart-4: #1fa2dc;
--chart-5: #198dbc;
```

## 侧边栏

```css
--sidebar: #1c1c1c;
--sidebar-foreground: #cfcece;
--sidebar-primary: #fafafa;
--sidebar-primary-foreground: #1c1c1c;
--sidebar-accent: #262626;
--sidebar-accent-foreground: #fafafa;
--sidebar-border: #ffffff1a;
--sidebar-ring: #fafafaa3;
```

## Cookie Consent相关（非UI核心）

```css
--cc-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
--cc-modal-border-radius: .5rem;
--cc-btn-border-radius: .4rem;
--cc-bg: #fff;
--cc-primary-color: #2c2f31;
--cc-btn-primary-bg: #30363c;
--cc-btn-primary-color: #fff;
--cc-btn-primary-hover-bg: #000;
```

## 节点卡片实测值

```css
/* .bg-card 节点卡片 */
background-color: rgb(31, 31, 31);  /* #1f1f1f */
border-radius: 16px;
border: 0px solid rgba(255, 255, 255, 0.1);
box-shadow: none;
backdrop-filter: none;
width: 250px;
min-height: 250px;

/* .bg-card 控制面板 */
background-color: rgb(31, 31, 31);
border-radius: 16px;
border: 1px solid rgba(255, 255, 255, 0.1);
box-shadow: 0px 2px 4px rgba(0,0,0,0.1), 0px 4px 6px rgba(0,0,0,0.1);
```

## 画布实测值

```css
/* body */
background-color: rgb(0, 0, 0);  /* 纯黑 */

/* .react-flow 画布 */
background-color: transparent;
/* CSS变量都是空的——TapNow不用React Flow的--xy-*变量 */

/* Handle连接点 */
width: 6px;
height: 6px;
background: transparent;
```
