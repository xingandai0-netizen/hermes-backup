---
name: wechat-automation-reference
description: >-
  微信自动化参考方案，收集了多种微信自动化方法。
  包括：WeChatBot、ChatALL、WeChatFerry、chatgpt-on-wechat等。
  注意：需要用户确认合法性，仅用于个人自动化需求。
version: 1.0.0
author: Hermes Agent (基于多个GitHub仓库)
metadata:
  created: 2026-04-17
  sources:
    - https://github.com/nicepkg/WeChatBot
    - https://github.com/94bond(ChatALL
    - https://github.com/nicepkg/WeChatFerry
    - https://github.com/zhayujie/chatgpt-on-wechat
---

# 微信自动化参考

⚠️ **重要声明**
- 使用前请确认符合微信使用条款
- 建议仅用于个人自动化需求
- 不要用于垃圾信息或骚扰

## 方案对比

| 方案 | 难度 | 功能 | 风险 |
|------|------|------|------|
| WeChatBot | 中 | 基础自动回复 | 低 |
| ChatALL | 易 | 多平台聊天 | 中 |
| WeChatFerry | 高 | 完整API | 高 |
| chatgpt-on-wechat | 中 | AI对话 | 中 |

## 快速开始

### 1. WeChatBot (推荐新手)
```bash
git clone https://github.com/nicepkg/WeChatBot
cd WeChatBot
pip install -r requirements.txt
python bot.py
```

### 2. ChatALL (桌面应用)
```bash
# macOS
brew install --cask chatall

# 或下载DMG
# https://github.com/94bond/ChatALL/releases
```

### 3. chatgpt-on-wechat
```bash
git clone https://github.com/zhayujie/chatgpt-on-wechat
cd chatgpt-on-wechat
pip install -r requirements.txt
python app.py
```

## 自动化场景

### 自动回复
```python
# 伪代码示例
def on_message_received(message):
    if "关键词" in message.content:
        reply = generate_reply(message.content)
        send_message(message.sender, reply)
```

### 定时发送
```python
import schedule
import time

def send_daily_message():
    message = "每日问候"
    send_to_contacts(["朋友1", "朋友2"], message)

schedule.every().day.at("09:00").do(send_daily_message)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 注意事项

1. **账号安全**: 使用小号测试，避免主账号被封
2. **频率控制**: 避免频繁发送，建议间隔>30秒
3. **内容合规**: 不发送违规内容
4. **本地运行**: 优先选择本地方案，保护隐私
