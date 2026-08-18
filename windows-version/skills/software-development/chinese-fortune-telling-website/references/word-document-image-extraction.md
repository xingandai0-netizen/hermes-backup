# Word文档中的图片查看方法

## 场景
用户说"图片自己在word文件中看"或提供.doc/.docx文件需要查看其中的UI设计图。

## 方法

### 1. 用Preview打开（推荐）
```bash
open -a "Preview" "/path/to/document.doc"
```

### 2. 等待加载
```bash
sleep 3
```

### 3. 截图当前页面
```bash
screencapture -x /tmp/word-screenshot.png
```

### 4. 用vision_analyze查看
```python
vision_analyze(image_url="/tmp/word-screenshot.png", question="请详细描述文档中的UI设计图内容")
```

### 5. 滚动查看更多内容
```bash
for i in {1..5}; do
    osascript -e 'tell application "System Events" to key code 125'  # 向下箭头
    sleep 0.5
done
```

### 6. 继续截图和分析
```bash
screencapture -x /tmp/word-scroll1.png
```

## 关键点

- **不能只提取文字**，必须查看图片中的UI设计
- **截图后用vision_analyze分析设计细节**
- **每次滚动后都要截图**，确保看到所有设计图
- **至少滚动3-5次**，因为文档通常有多页

## 备选方法

如果Preview无法打开.doc文件：
```bash
# 用Pages打开
open -a "Pages" "/path/to/document.doc"

# 用Microsoft Word打开（如果安装了）
open -a "Microsoft Word" "/path/to/document.doc"
```

## Python-docx提取（不推荐用于查看图片）
```python
# python-docx可以提取图片，但无法直接查看UI设计图
from docx import Document
import zipfile

# 更好的方法是直接用Preview打开
```
