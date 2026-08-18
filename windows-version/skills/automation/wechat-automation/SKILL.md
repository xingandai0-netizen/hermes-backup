---
name: wechat-automation
description: "WeChat automation on macOS: AppleScript GUI automation, message/file sending, and troubleshooting. Covers multiple approaches (AppleScript, WeChatBot, WeChatFerry) and advanced failure handling."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [wechat, automation, applescript, macos, gui, messaging]
---

# WeChat Automation (macOS)

Automate WeChat on macOS through GUI automation. Multiple approaches available for different use cases.

## When to Use

- Sending messages or files via WeChat programmatically
- Automating WeChat workflows (scheduled messages, auto-replies)
- Interacting with WeChat UI elements
- Troubleshooting WeChat automation failures

## Approaches

| Approach | Reliability | Capabilities | Requirements |
|----------|------------|--------------|--------------|
| **AppleScript GUI** | Medium | Send messages, click buttons | Accessibility permissions |
| **WeChatBot** | High | Full API access | Running bot server |
| **WeChatFerry** | High | Hook-based | Windows only |
| **chatgpt-on-wechat** | High | Bot framework | Running service |

---

## 1. AppleScript GUI Automation

The primary approach for macOS. Uses Accessibility API to control WeChat's UI.

### Prerequisites

1. Grant Accessibility permission: System Settings → Privacy & Security → Accessibility → Add Terminal/Hermes
2. WeChat must be running and logged in

### Send a Message

```applescript
tell application "System Events"
    tell process "WeChat"
        -- Activate WeChat
        set frontmost to true
        delay 0.5
        
        -- Click on the search field
        -- (implementation depends on WeChat version)
    end tell
end tell
```

### Common Operations

- **Send text message:** Activate chat → type message → press Enter
- **Send file:** Use drag-and-drop or menu commands
- **Search contact:** Use search field, type name, select result
- **Read messages:** Access message list UI elements

### Pitfalls

- **WeChat UI changes frequently** — AppleScript may break after updates
- **Accessibility permissions reset** — macOS may revoke after updates
- **Timing is critical** — add `delay` between actions for reliability
- **Chinese input method** — may interfere with text input; switch to English first
- **Multiple WeChat windows** — target the correct window

---

## 2. Advanced Troubleshooting

### Common Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| "Not allowed to send keystrokes" | Accessibility not granted | Re-grant in System Settings |
| UI element not found | WeChat updated, changed UI | Re-inspect with Accessibility Inspector |
| Message sent to wrong chat | Window focus issue | Verify active chat before sending |
| Input method interference | Chinese IME active | Switch to English input first |
| WeChat not responding | App frozen | Force quit and relaunch |

### Debugging Steps

1. **Check accessibility:** `osascript -e 'tell application "System Events" to get name of every process'`
2. **Inspect UI:** Use Accessibility Inspector (Xcode → Open Developer Tool)
3. **Test with simple script:** Start with just activating WeChat
4. **Add delays:** Increase delay values if actions are unreliable

### Recovery Patterns

- If WeChat is unresponsive: `killall WeChat && sleep 3 && open -a WeChat`
- If automation fails mid-sequence: reset state by clicking outside WeChat, then retry
- If messages go to wrong chat: verify chat name before sending

---

## 3. Alternative Approaches

### WeChatBot (Recommended for production)

Full API-based automation. Runs as a separate service.

See [references/wechatbot-setup.md](references/wechatbot-setup.md) for setup guide.

### chatgpt-on-wechat

Bot framework with WeChat integration. Good for chatbot use cases.

See [references/chatgpt-on-wechat.md](references/chatgpt-on-wechat.md) for configuration.

---

## Rules

1. **Always confirm before sending** — automation mistakes are hard to undo in WeChat
2. **Test with a personal chat first** — don't experiment in group chats
3. **Add generous delays** — reliability over speed
4. **Handle failures gracefully** — WeChat automation is inherently fragile
5. **Check WeChat is running** — before any automation attempt
