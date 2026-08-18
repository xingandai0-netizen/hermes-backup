---
name: browser-screenshot-to-xiaohongshu
description: 截取网页完整内容并直接发布到小红书。适用于需要截图长页面（如AI回答、文档、聊天记录）并发布到小红书的场景。支持识别滚动容器、分段截图、直接发布。
version: 2.0.0
author: 小黑
---

# 网页截图发布小红书技能

## 使用场景
- 截图AI回答（Gemini、ChatGPT等）发布到小红书
- 截图长网页内容发布到小红书
- 保留原始内容格式，不做压缩总结
- 将网页内容转化为Apple风格HTML报告后截图（推荐，更美观）

## 关键决策：何时用哪种方法

### 方法A：直接截图原始页面
- 用户要求"截图这个页面"
- 页面本身设计美观
- 需要保留原始UI上下文

### 方法B：创建Apple风格HTML报告（推荐）
- 用户要求"完整内容"而非摘要
- 原始页面有加载问题或内容缺失
- 需要高端视觉效果
- 科普、教程、长文类内容

## Apple风格HTML报告生成流程

### Step 0: 提取完整内容
```python
# 使用browser_snapshot获取完整页面文本
snapshot = browser_snapshot(full=True)
# 从snapshot中提取所需内容
```

### Step 0.5: 创建HTML报告模板
```python
# Apple风格HTML模板 - 深色主题，适合技术/科普内容
html_template = '''
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #f0f0f0;
    padding: 40px;
    margin: 0;
    line-height: 1.6;
  }
  .container {
    max-width: 900px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 40px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  h1 {
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(90deg, #e94560, #f39c12);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px;
  }
  h2 {
    font-size: 24px;
    color: #e94560;
    margin-top: 30px;
    border-left: 4px solid #e94560;
    padding-left: 15px;
  }
  p {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.85);
    margin: 15px 0;
  }
  .highlight {
    background: rgba(233, 69, 96, 0.2);
    padding: 3px 8px;
    border-radius: 4px;
    color: #ff6b8a;
  }
  .quote {
    border-left: 4px solid #f39c12;
    padding: 15px 20px;
    margin: 20px 0;
    background: rgba(243, 156, 18, 0.1);
    border-radius: 0 10px 10px 0;
    font-style: italic;
  }
</style>
</head>
<body>
<div class="container">
  <h1>{title}</h1>
  {content}
</div>
</body>
</html>
'''
```

### Step 1: 导航到目标页面获取内容

### Step 1: 导航到目标页面获取内容
```python
# 打开目标页面
browser_navigate(url="https://目标网址")
# 等待加载
time.sleep(3)
# 获取完整页面内容
snapshot = browser_snapshot(full=True)
```

### Step 2: 保存HTML并渲染
```python
# 保存HTML文件
with open("report.html", "w") as f:
    f.write(html_content)

# 加载到浏览器预览
browser_navigate(url=f"file:///Users/.../report.html")
```

### Step 3: 系统性滚动截图
```python
# 使用window.scrollTo滚动整个页面
# 先计算页面总高度
height = browser_console(expression="document.documentElement.scrollHeight")
# 每次滚动约800px，留重叠
positions = list(range(0, height, 750))

for i, pos in enumerate(positions):
    browser_console(expression=f"window.scrollTo(0, {pos})")
    time.sleep(0.5)
    browser_vision(question="Screenshot")
    # 保存截图到指定目录
    terminal(f"cp ~/.hermes/cache/screenshots/*.png ~/screenshots/report_{i}.png")
```

## 直接截图原始页面流程

### Step 1: 导航到目标页面
```python
browser_navigate(url="https://目标网址")
```

### Step 2: 识别滚动容器
```python
# 在browser_console中执行，找到实际的滚动容器
containers = document.querySelectorAll('*');
let scrollContainer = null;
let maxHeight = 0;
for (const el of containers) {
  if (el.scrollHeight > el.clientHeight && el.scrollHeight > maxHeight) {
    maxHeight = el.scrollHeight;
    scrollContainer = el;
  }
}
// 如果没有明显容器，使用window
```

### Step 3: 计算截图次数
```
截图次数 = ceil(scrollHeight / clientHeight)
例如：总高7092px，可视650px → 需要11次截图
每次滚动 = clientHeight * 0.9（留重叠确保不漏内容）
```

### Step 4: 系统性滚动截图
```python
# 滚动到顶部
browser_console(expression="window.scrollTo(0, 0)")

# 循环截图
for i, pos in enumerate(scroll_positions):
    browser_console(expression=f"window.scrollTo(0, {pos})")
    time.sleep(0.5)
    browser_vision(question="Screenshot")
```

### Step 5: 发布到小红书
```python
# 使用xiaohongshu-content-creation技能发布
# 或直接调用publish脚本
```

## 关键经验教训

### 1. "完整内容" vs "摘要内容"
- **用户说"完整内容"时**：不要自己总结，直接截图原始页面或生成完整HTML报告
- **用户说"摘要"时**：可以提炼核心内容

### 2. Gemini页面内容获取
- 共享的Gemini对话URL可能内容不完整
- 使用`browser_snapshot(full=True)`获取文本更可靠
- 结合HTML报告渲染可确保内容完整

### 3. 截图质量保证
- 每次滚动后等待0.5秒让渲染完成
- 使用`time.sleep(0.5)`确保内容加载
- 小红书最多支持18张图片

## 注意事项
1. 小红书最多支持18张图片
2. 每次滚动高度建议 = clientHeight * 0.9（留一些重叠确保不漏内容）
3. 截图前确保页面完全加载（等2-3秒）
4. 如果页面高度超过18*clientHeight，需要分批发布
5. Apple风格HTML适合科技、科普、教程类内容

## 常见问题
Q: 页面没有明显的滚动容器怎么办？
A: 直接滚动整个页面：`window.scrollTo(0, position)`

Q: 截图太模糊怎么办？
A: 浏览器工具默认截图质量足够，无需额外处理

Q: 用户要求"完整内容"但我用了摘要怎么办？
A: 重新截图原始页面或生成完整HTML报告，不要自己总结

Q: HTML报告模板如何自定义？
A: 修改颜色、字体、间距等CSS属性，保持Apple设计语言的一致性
    # 截图（browser_vision会自动保存截图）
    browser_vision(question="Screenshot")
    # 复制截图到指定目录
    terminal(f"cp ~/.hermes/cache/screenshots/browser_screenshot_*.png ~/screenshots/page_{i+1}.png")
```

### Step 5: 直接发布到小红书
```bash
# 不需要渲染，直接用截图发布
export XHS_COOKIE="你的cookie"
python3 scripts/publish_xhs.py \
  --title "标题" \
  --desc "描述" \
  --images ~/screenshots/page_1.png ~/screenshots/page_2.png ...
```

## 注意事项
1. 小红书最多支持18张图片
2. 每次滚动高度建议 = clientHeight * 0.9（留一些重叠确保不漏内容）
3. 截图前确保页面完全加载（等2-3秒）
4. 如果页面高度超过18*clientHeight，需要分批发布

## 常见问题
Q: 页面没有明显的滚动容器怎么办？
A: 直接滚动整个页面：`window.scrollTo(0, position)`

Q: 截图太模糊怎么办？
A: 浏览器工具默认截图质量足够，无需额外处理

Q: 如何获取小红书Cookie？
A: 登录小红书后从浏览器开发者工具获取，参考xiaohongshu-content-creation技能
