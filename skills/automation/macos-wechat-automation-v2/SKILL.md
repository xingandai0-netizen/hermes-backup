---
name: macos-wechat-automation
description: Control WeChat on macOS through AppleScript GUI automation
tags: [wechat, macos, applescript, automation]
last_modified: 2026-06-07
---

# macOS WeChat Automation

## Current Status (2026-06-07)
**PARTIALLY WORKING** — Can send messages, but CANNOT reliably read incoming messages.

## What Works
- Activating WeChat: `tell application "WeChat" to activate`
- Switching chats: Use clipboard paste for Chinese contact names
- Sending messages: Set clipboard, then Cmd+V + Enter
- Taking screenshots of WeChat window

## What Does NOT Work
- **Reading messages via AppleScript** — WeChat does not expose message content through Accessibility API
- **Typing Chinese characters directly** — AppleScript `keystroke` sends wrong characters when Chinese input method is active. ALWAYS use clipboard paste instead.
- **wechaty-puppet-wechat4u** — WeChat has restricted web API access. The puppet cannot log in.
- **OCR-based message monitoring** — Too slow and unreliable for real-time chat

## Recommended Approach for Sending Messages

```applescript
-- CORRECT: Use clipboard to send Chinese text
tell application "WeChat" to activate
delay 0.5
set the clipboard to "你的中文消息"
delay 0.3
tell application "System Events"
    tell process "WeChat"
        keystroke "v" using {command down}
        delay 0.5
        key code 36
    end tell
end tell
```

```applescript
-- WRONG: This will type garbage characters
tell application "System Events"
    tell process "WeChat"
        keystroke "中文消息"  -- DO NOT DO THIS
    end tell
end tell
```

## Pitfalls
- **Never use `keystroke` for Chinese text** — Always use clipboard paste. The user will see "啊啊啊啊" in the search box if you try to type Chinese directly.
- **Search vs Chat** — Using Cmd+F opens WeChat's built-in search (搜一搜), which finds articles, NOT contacts. To open a specific chat, use the chat list or Cmd+1/2/3 for recent chats.
- **wechaty is NOT a solution** — wechaty-puppet-wechat4u cannot authenticate because WeChat has blocked web API access since 2022. Don't waste time trying to set it up.
- **No message receive API** — There is no way to automatically detect new messages on macOS WeChat. The only option is periodic screenshot + OCR, which is too slow for real-time chat.

## Alternative Solutions for Two-Way Communication
1. **File Transfer Helper + Manual Notification** — User sends message, then tells agent in terminal. Agent reads screenshot and replies.
2. **Use Telegram/Discord instead** — These platforms have proper bot APIs for two-way communication.
3. **Use Hermes CLI directly** — Most reliable, but requires terminal access.
