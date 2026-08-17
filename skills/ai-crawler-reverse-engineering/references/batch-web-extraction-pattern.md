# Batch Web Extraction Pattern (2026-07-08 验证)

## 场景

当Safari AppleScript不可用（用户未登录、网站不需要登录、browser_navigate超时）时，
用execute_code + web_extract批量提取页面内容。

## 核心模式

```python
from hermes_tools import web_extract, write_file

# 定义页面列表
pages = [
    {"url": "https://example.com/page1", "filename": "page1.html"},
    {"url": "https://example.com/page2", "filename": "page2.html"},
    # ...
]

# 分批提取（web_extract每次最多5个URL）
for i in range(0, len(pages), 5):
    batch = pages[i:i+5]
    for page in batch:
        result = web_extract(urls=[page["url"]])
        if result and "results" in result and len(result["results"]) > 0:
            content = result["results"][0].get("content", "")
            if content:
                write_file(path=f"/output/dir/{page['filename']}", content=content)
                print(f"✅ {page['filename']}")
```

## 与Safari AppleScript的区别

| 方面 | Safari AppleScript | Batch web_extract |
|------|-------------------|-------------------|
| 需要登录 | 是（用户已登录的浏览器） | 否 |
| 获取真实DOM | 是（getComputedStyle） | 否（markdown格式） |
| 执行JS | 是 | 否 |
| 速度 | 慢（手动定位tab） | 快（自动化批量） |
| 适用场景 | 逆向CSS/JS/交互 | 提取页面结构/内容 |

## 实战验证

suanlemeai.cn逆向（2026-07-08）：
- 成功提取32/33个页面（96.97%成功率）
- 用execute_code分4批提取，每批5-10个页面
- 失败原因：zhuge.html（诸葛神数）内容为空

## 注意事项

1. **web_extract限制**：每次最多5个URL，超大页面会LLM摘要（5000字符上限）
2. **内容格式**：提取的是markdown格式，不是原始HTML
3. **动态内容**：需要JavaScript渲染的页面无法提取（用browser工具替代）
4. **GitHub raw文件**：可直接提取README等raw文件
   ```python
   url = "https://raw.githubusercontent.com/user/repo/main/README.md"
   ```
