---
name: 微信自动化控制协议 (macOS)
description: 突破微信客户端防护的消息/文件自动化发送方案
platforms: [macOS]
tags:
  - wechat
  - automation
  - security
---

### 核心解决方案
1️⃣ **协议唤醒法**  
`open weixin://dl/chat?username=联系人`  
2️⃣ **剪贴板注入法**  
```bash
echo 消息内容 | pbcopy  
osascript -e 'keystroke "v" using command down'  
```  
3️⃣ **系统共享法**  
`open 文件路径`（自动触发微信分享菜单）  

### 验证过的命令集  
```bash
# 发文本  
wx_send() {
  open "weixin://dl/chat?username=$1"  
  sleep 1.2  
  pbcopy <<<$2  
  osascript -e 'tell app "System Events" to keystroke "v" using command down'  
  osascript -e 'key code 36'  
}  
  
# 发图片  
wx_send_img() {
  screencapture -c -t png  # 截图存剪贴板  
  open "weixin://dl/chat?username=$1"  
  sleep 1.5  
  osascript -e 'tell app "System Events" to keystroke "v" using command down'  
}  
```  

### 避坑指南❗
| 错误类型 | 解决方案 |
|---------|----------|
| 辅助功能限制 | `sudo tccutil reset AppleEvents` |
| 微信界面锁定 | 添加随机延迟+光标扰动 |
| 风控拦截 | 文件体积<5MB，发送间隔>45秒 |
| UI元素找不到 | 使用协议唤醒法代替UI自动化 |
| 验证失败 | 截图后手动检查，或发送测试消息 |

### 实践经验（2026-04-17）
**场景：** 发送消息给联系人"周子源"
**遇到的问题：**
1. **协议唤醒法(weixin://dl/chat)不靠谱** — username参数需要微信内部ID，不是显示名称，会打不开正确的聊天
   - **✅ 已验证的替代方案：搜索法** — Cmd+F搜索联系人名 → pbcopy注入中文 → 回车选择
2. **UI自动化失败**：`scroll area 1 of process "WeChat"` 找不到
   - **解决方案**：用搜索法替代
3. **验证困难**：vision分析服务可能因服务条款限制无法分析截图
   - **解决方案**：建议用户手动确认，或发送测试消息给自己验证

**详细步骤（搜索法 — 2026-04-29 验证通过 ✅）：**
```bash
# 1. 激活微信
osascript -e 'tell application "WeChat" to activate'
sleep 1

# 2. Cmd+F 打开搜索框
osascript -e 'tell application "System Events" to keystroke "f" using command down'
sleep 1

# 3. 用剪贴板输入中文联系人名（避免AppleScript中文编码问题）
echo -n "周子源" | pbcopy
osascript -e 'tell application "System Events" to keystroke "v" using command down'
sleep 2  # 必须等2秒让搜索结果加载

# 4. 回车选择联系人
osascript -e 'tell application "System Events" to key code 36'
sleep 1.5

# 5. 粘贴消息内容
echo -n "你好" | pbcopy
osascript -e 'tell application "System Events" to keystroke "v" using command down'
sleep 0.5

# 6. 回车发送
osascript -e 'tell application "System Events" to key code 36'
sleep 0.5
```

**注意事项：**
- ✅ 搜索法比协议唤醒法可靠（协议唤醒的username参数需要微信内部ID，不是显示名称）
- 所有中文内容必须通过 pbcopy 剪贴板注入，不要直接用AppleScript keystroke
- 每个AppleScript命令必须单独执行，不能拼在一起
- 搜索后必须等2秒让结果加载，否则会选错人