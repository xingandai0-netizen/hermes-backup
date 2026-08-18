---
name: chinese-nlp-toolkit
description: 中文自然语言处理工具包，支持文本分析、信息提取、情感分析等
version: 1.0.0
author: Hermes Agent
---

# 中文NLP工具包

## 核心功能

### 文本预处理
- 中文分词
- 去除停用词
- 词性标注
- 命名实体识别

### 信息提取
- 手机号提取
- 邮箱提取
- 身份证提取
- 地址提取
- 人名识别

### 情感分析
- 文本情感分析
- 评论分析
- 舆情监控

### 文本相似度
- 词汇相似度
- 句子相似度
- 文档相似度

## 常用库

### jieba - 中文分词
```python
import jieba

# 精确模式
text = "我来到北京清华大学"
words = jieba.lcut(text)
print(words)

# 搜索模式
words = jieba.lcut_for_search(text)
print(words)

# 添加自定义词典
jieba.add_word("清华大学")
```

### snownlp - 中文NLP
```python
from snownlp import SnowNLP

# 情感分析
s = SnowNLP("这家餐厅很好吃")
print(s.sentiments)  # 0-1, 越大越正面

# 中文分词
print(s.words)

# 拼音转换
print(s.pinyin)

# 繁体转简体
print(SnowNLP("繁體").han)
```

### pyltp - 语言技术平台
```python
from pyltp import Segmentor, Postagger, NamedEntityRecognizer

# 分词
segmentor = Segmentor()
segmentor.load("ltp_data_v3.4.0/cws.model")
words = segmentor.segment("他叫汤明去黄冈市计算机学院")
print("	".join(words))

# 词性标注
postagger = Postagger()
postagger.load("ltp_data_v3.4.0/pos.model")
postags = postagger.postag(words)
print("	".join(postags))
```

### HanLP - 多功能NLP库
```python
from hanlp import HanLP

# 中文分词
HanLP.segment("你好欢迎使用HanLP")

# 实体识别
HanLP.ner("小明在北京大学学习")

# 依存句法分析
HanLP.parse("小明在图书馆看书")
```

## 实用工具

### 手机号提取
```python
import re

def extract_phone(text):
    """提取中国大陆手机号"""
    pattern = r'1[3-9]\d{9}'
    return re.findall(pattern, text)

text = "我的手机号是13800138000"
phones = extract_phone(text)
print(phones)  # ['13800138000']
```

### 身份证提取
```python
def extract_id_card(text):
    """提取身份证号码"""
    pattern = r'[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]'
    return re.findall(pattern, text)

text = "身份证号是11010119900307457X"
id_cards = extract_id_card(text)
print(id_cards)
```

### 邮箱提取
```python
def extract_email(text):
    """提取邮箱地址"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

text = "联系邮箱：user@example.com"
emails = extract_email(text)
print(emails)  # ['user@example.com']
```

### 人名识别
```python
import jieba.posseg as pseg

def extract_names(text):
    """提取人名"""
    words = pseg.cut(text)
    names = []
    for word, flag in words:
        if flag == 'nr':  # 人名
            names.append(word)
    return names

text = "张三和李四一起去了北京"
names = extract_names(text)
print(names)  # ['张三', '李四']
```

## 情感分析实战

### 商品评论分析
```python
from snownlp import SnowNLP

reviews = [
    "这个商品非常好，值得购买！",
    "质量太差了，不推荐",
    "一般般吧，没什么特别的",
    "非常满意，物流也快",
]

for review in reviews:
    s = SnowNLP(review)
    sentiment = s.sentiments
    if sentiment > 0.6:
        label = "正面"
    elif sentiment < 0.4:
        label = "负面"
    else:
        label = "中性"
    print(f"{review} -> {label} ({sentiment:.2f})")
```

## 文本相似度

### 词汇相似度
```python
from snownlp import SnowNLP

def word_similarity(word1, word2):
    """计算两个词的相似度"""
    s1 = SnowNLP(word1)
    s2 = SnowNLP(word2)
    # 使用拼音相似度作为示例
    return 1.0 if s1.pinyin == s2.pinyin else 0.0

sim = word_similarity("苹果", "苹果")
print(sim)  # 1.0
```

## 安装

```bash
# 基础NLP包
pip install jieba snownlp

# 科学计算
pip install numpy pandas scikit-learn

# 深度学习NLP
pip install transformers torch

# HanLP（需要Java）
pip install hanlp
```

## 应用场景

### 1. 文本分类
- 新闻分类
- 垃圾邮件检测
- 情感分析

### 2. 信息提取
- 简历解析
- 合同分析
- 评论挖掘

### 3. 智能客服
- 意图识别
- 实体提取
- 自动回复

### 4. 内容审核
- 敏感词过滤
- 广告检测
- 违规内容识别
