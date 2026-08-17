---
name: drission-page-automation
description: 基于DrissionPage的网页自动化工具
version: 1.0.0
author: Hermes Agent
---

# DrissionPage网页自动化

## 核心功能

### 浏览器控制
from DrissionPage import ChromiumPage
page = ChromiumPage()
page.get("https://www.example.com")
page.ele("text=登录").click()
page.ele("#username").input("用户名")

### 数据包模式
from DrissionPage import Session
session = Session()
resp = session.get("https://api.example.com/data")

### 混合模式
page.set.request.data_mode()
resp = page.get("https://api.example.com/data")
page.set.request.browser_mode()

## 常用操作

### 元素定位
page.ele("#element-id")  # ID
page.ele(".class-name")  # class
page.ele("text=按钮文本")  # 文本
page.ele("xpath://div")  # XPath
page.ele("css:div.container")  # CSS

### 元素操作
element.click()  # 点击
element.input("文本")  # 输入
element.text  # 获取文本
element.attr("href")  # 获取属性

### 等待机制
page.wait.eles_loaded(".content", timeout=10)
page.wait.load_start()

## 实战示例

### 自动化登录
page = ChromiumPage()
page.get("https://example.com/login")
page.ele("#username").input("user")
page.ele("#password").input("pass")
page.ele("text=登录").click()

### 数据采集
products = page.ele(".product-item")
data = []
for p in products:
    data.append({
        "name": p.ele(".name").text,
        "price": p.ele(".price").text
    })

## 安装
```bash
pip install DrissionPage
```

## 与Playwright对比

| 特性 | DrissionPage | Playwright |
|------|-------------|------------|
| 学习曲线 | 低 | 中 |
| 数据包模式 | 支持 | 不支持 |
| 中文文档 | 完善 | 一般 |
