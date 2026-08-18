---
name: social-media-automation
description: >-
  社交媒体自动化管理，支持定时发布、内容生成、多平台同步。
  集成OpenAI API生成内容，支持Instagram、Twitter、小红书等平台。
version: 1.0.0
author: Hermes Agent (基于 SakethSripada/Flask-SocialMedia-Automation)
metadata:
  created: 2026-04-17
  sources:
    - https://github.com/SakethSripada/Flask-SocialMedia-Automation
---

# 社交媒体自动化

自动化社交媒体内容创作、定时发布和多平台管理。

## 功能特性

### 1. 内容生成
- OpenAI GPT生成文案
- DALL-E生成配图
- NewsAPI获取热点新闻

### 2. 定时发布
- 一次性定时
- 周期性发布
- Cron表达式支持

### 3. 多平台支持
| 平台 | 发布 | 分析 | 状态 |
|------|------|------|------|
| Twitter | ✅ | ✅ | 稳定 |
| Instagram | ✅ | ✅ | 需企业账号 |
| 小红书 | 🔧 | ❌ | 需手动验证 |

## 快速开始

### 1. 安装依赖
```bash
pip install flask apscheduler openai tweepy instaloader
```

### 2. 配置密钥
创建 `config.py`:
```python
# Twitter
TWITTER_API_KEY = "your-key"
TWITTER_API_SECRET = "your-secret"
TWITTER_ACCESS_TOKEN = "your-token"

# OpenAI
OPENAI_API_KEY = "your-key"

# Instagram (可选)
INSTAGRAM_USERNAME = "your-username"
INSTAGRAM_PASSWORD = "your-password"
```

### 3. 运行
```bash
python app.py
```

## 使用示例

### 生成推文
```python
from openai import OpenAI

client = OpenAI()

def generate_tweet(topic, style="casual"):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"你是一个{style}风格的社交媒体写手"},
            {"role": "user", "content": f"写一条关于{topic}的推文，不超过280字"}
        ]
    )
    return response.choices[0].message.content
```

### 定时发布
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=9, minute=0)
def morning_post():
    topic = get_trending_topic()
    tweet = generate_tweet(topic)
    post_to_twitter(tweet)

scheduler.start()
```

### 批量处理
```python
def batch_post(content_list, platforms=["twitter"]):
    results = []
    for content in content_list:
        for platform in platforms:
            if platform == "twitter":
                result = post_to_twitter(content)
            elif platform == "instagram":
                result = post_to_instagram(content)
            results.append(result)
            time.sleep(60)  # 避免频率限制
    return results
```

## 定时任务配置

```python
# 每天早上9点发布
scheduler.add_job(post_morning, 'cron', hour=9)

# 每2小时发布一次
scheduler.add_job(post_regular, 'interval', hours=2)

# 每周一上午10点
scheduler.add_job(post_weekly, 'cron', day_of_week='mon', hour=10)
```

## 数据分析

```python
def get_analytics(platform, period="7d"):
    if platform == "twitter":
        return get_twitter_analytics(period)
    elif platform == "instagram":
        return get_instagram_analytics(period)
```

## 最佳实践

1. **内容多样性**: 混合原创、转发、互动内容
2. **发布时间**: 根据受众活跃时间调整
3. **频率控制**: 避免过度发布，建议每天3-5条
4. **数据追踪**: 定期分析表现，优化策略
