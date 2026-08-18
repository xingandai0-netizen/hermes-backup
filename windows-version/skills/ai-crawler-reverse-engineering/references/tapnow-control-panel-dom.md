# TapNow 控制面板(Control Panel) DOM结构 (2026-07-05)

## 触发条件
控制面板只在**节点被点击/选中**后出现。节点默认是折叠状态（只有标题+占位图标）。

## 控制面板容器结构

```html
<!-- 浮动控制面板 - 吸附在节点底部 -->
<div class="node-float-ui nodrag cursor-default absolute -bottom-2 z-20 w-full min-w-[640px] max-w-[650px] node-float-ui-hidden">
  <div class="bg-card rounded-2xl border border-border shadow-lg mt-2 w-full relative group">
    
    <!-- 顶部输入行 -->
    <div class="px-3 pt-3 pb-2 flex gap-2 items-center min-w-0">
      <!-- 上传按钮 -->
      <button class="size-[38px] flex items-center justify-center rounded-[10px] shrink-0 transition-all focus:outline-none bg-white/[0.08] hover:bg-white/[0.12] cursor-pointer">
        <svg class="lucide lucide-plus size-4 text-white/60">...</svg>
      </button>
    </div>
    
    <!-- 输入区域 (TipTap富文本编辑器) -->
    <div class="relative flex justify-between flex-1 nodrag nowheel" data-testid="canvas-node-prompt-textarea">
      <div class="relative w-full">
        <div class="overflow-y-auto text-sm! min-h-[80px] max-h-[400px]">
          <div contenteditable="true" 
               class="tiptap ProseMirror prose prose-sm dark:prose-invert 
                      max-w-none focus:outline-none px-3 pb-2">
            <p class="leading-6!">我要生成一个修仙者视频</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 底部操作栏 -->
    <div class="flex items-center justify-between w-full p-2 h-14" data-testid="canvas-node-generation-action-bar">
      <div class="flex items-center gap-1 min-w-0">
        <!-- 模型选择器 -->
        <button class="h-9 gap-1 hover:bg-muted active:bg-white/[0.1] 
                       px-2 py-1 text-sm rounded-lg"
                data-testid="canvas-node-text-model-select">
          Gemini 3.1 Flash Lite
        </button>
        
        <!-- 设置按钮 -->
        <button class="flex size-8 shrink-0 items-center justify-center p-0 focus:outline-none rounded-lg">
          <!-- 图标 -->
        </button>
        
        <!-- 分隔线 -->
        <div class="w-px h-4 bg-border shrink-0"></div>
        
        <!-- 变体数量选择 -->
        <button aria-label="Generate 1 variations" class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm font-medium text-foreground">
          1×
        </button>
        
        <!-- 价格显示 -->
        <div class="flex items-center gap-1 rounded-full p-1 border border-white/10">
          <div class="flex items-center text-sm text-popover-foreground font-medium">
            <span class="inline-flex w-full justify-center whitespace-nowrap tap-price-change">价格</span>
          </div>
        </div>
      </div>
      
      <!-- 生成按钮 -->
      <div class="relative z-20 flex shrink-0 items-center gap-1 ml-2 delay-200">
        <button aria-label="Generate" class="aspect-square w-6.5 h-6.5 rounded-full cursor-pointer flex items-center justify-center bg-white text-black hover:bg-white/50">
          <!-- 箭头图标 -->
        </button>
      </div>
    </div>
    
  </div>
</div>
```

## 控制面板CSS（getComputedStyle实测值 2026-07-05）

```css
/* 容器 .node-float-ui */
position: absolute;
width: 100%;
min-width: 640px;
max-width: 650px;

/* 卡片 .bg-card.rounded-2xl */
background-color: rgb(31, 31, 31); /* --card: #1f1f1f */
border-radius: 16px;
border: 1px solid rgba(255, 255, 255, 0.1); /* --border: #ffffff1a */
box-shadow: 0px 2px 4px rgba(0,0,0,0.1), 0px 4px 6px rgba(0,0,0,0.1);

/* 上传按钮 */
width: 38px; height: 38px;
border-radius: 10px;
background: rgba(255, 255, 255, 0.08); /* bg-white/[0.08] */
color: rgb(245, 245, 245);
/* hover: rgba(255, 255, 255, 0.12) */

/* 模型选择器按钮 */
height: 36px;
border-radius: 12px; /* 实测值，非Tailwind默认的8px */
background: transparent;
color: rgb(245, 245, 245);

/* 设置按钮 */
width: 32px; height: 32px;
border-radius: 12px;
background: transparent;
color: rgb(245, 245, 245);

/* 变体数量按钮 "1×" */
border-radius: 12px;
background: transparent;
color: rgb(245, 245, 245);

/* 生成按钮（圆形） */
width: 26px; height: 26px;
border-radius: 50%; /* 实测值，完全圆形 */
background: rgb(255, 255, 255); /* 白色 */
color: rgb(0, 0, 0); /* 黑色文字 */
/* hover: rgba(255, 255, 255, 0.5) */

/* 输入区域 */
height: 36px;
background: transparent;
color: rgb(245, 245, 245);

/* TipTap编辑器 */
font-size: 16px; /* 实测值，非text-sm的14px */
color: rgb(245, 245, 245);
padding: 0px 12px 8px;
```

## 提取的按钮详情（getComputedStyle实测）

| 按钮 | className前缀 | 尺寸 | 背景色 | 圆角 |
|------|--------------|------|--------|------|
| 上传 | `size-[38px]...rounded-[10px]` | 38x38px | rgba(255,255,255,0.08) | 10px |
| 模型选择器 | `h-9...rounded-lg` | auto x 36px | transparent | 12px |
| 设置 | `size-8...rounded-lg` | 32x32px | transparent | 12px |
| 变体数量 | `px-3 py-1.5 rounded-lg` | auto | transparent | 12px |
| 生成 | `w-6.5 h-6.5 rounded-full` | 26x26px | white | 50% |
| 价格 | `rounded-full p-1` | auto | transparent | 9999px |

## TipTap编辑器样式

```css
.ProseMirror {
  min-height: inherit;
  font-size: 16px; /* 实测值 */
  line-height: 24px; /* leading-6 */
  color: rgb(245, 245, 245);
  padding: 0 12px 8px;
  outline: none;
}

/* 空状态placeholder */
.ProseMirror.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  color: var(--muted-foreground);
  float: left;
  height: 0;
  pointer-events: none;
}

/* @mention样式 */
.ProseMirror .mention-image {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.2);
  height: 24px;
  border-radius: 9999px;
  padding: 0 8px 0 4px;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
}

.ProseMirror .mention-video {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.ProseMirror .mention-element {
  background: rgba(168, 85, 247, 0.15);
  color: #c084fc;
  border: 1px solid rgba(168, 85, 247, 0.2);
}
```

## 提取方法

控制面板需要节点被点击后才会出现在DOM中。提取步骤：
1. 用户在已登录的TapNow画布中点击一个节点
2. 在Console执行 `document.querySelector('.node-float-ui')` 确认面板已出现
3. 执行IIFE代码获取完整的HTML和computed styles
4. 注意：`node-float-ui-hidden` 类表示面板正在隐藏/显示过渡中

## 提取代码模板

```javascript
(function() {
  var panel = document.querySelector('.node-float-ui');
  if (!panel) {
    console.log('No control panel found. Click a node first.');
    return;
  }
  
  var card = panel.querySelector('.bg-card');
  var cardStyles = card ? getComputedStyle(card) : null;
  
  var buttons = panel.querySelectorAll('button');
  var btnInfo = Array.from(buttons).map(function(b) {
    var s = getComputedStyle(b);
    return {
      text: b.textContent?.trim()?.substring(0, 30),
      classes: b.className?.substring(0, 150),
      w: s.width,
      h: s.height,
      bg: s.backgroundColor,
      radius: s.borderRadius
    };
  });
  
  var editor = panel.querySelector('.ProseMirror');
  var edStyles = editor ? getComputedStyle(editor) : null;
  
  console.log(JSON.stringify({
    panelHTML: panel.outerHTML?.substring(0, 8000),
    cardStyles: cardStyles ? {
      bg: cardStyles.backgroundColor,
      radius: cardStyles.borderRadius,
      border: cardStyles.border,
      shadow: cardStyles.boxShadow
    } : null,
    buttons: btnInfo,
    editorStyles: edStyles ? {
      fontSize: edStyles.fontSize,
      lineHeight: edStyles.lineHeight,
      color: edStyles.color,
      padding: edStyles.padding
    } : null
  }, null, 2));
})();
```
