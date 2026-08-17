# HelpViewer Window Blocking Case Study (2026-06-07)

## Scenario
Sending a task to 小黄 (Claude Desktop) via GUI automation. Claude Desktop was running (PID visible in list_apps) but its window was covered by macOS HelpViewer ("中文和粤语输入方式使用手册").

## What was tried (all failed)

1. **osascript close HelpViewer window**
   ```
   osascript -e 'tell application "Help" to close window 1'
   ```
   Error: `不能获得"application "Help"` (-1728)` — wrong app name

2. **System Events keystroke Cmd+W on HelpViewer**
   ```
   osascript -e 'tell application "System Events" to tell process "HelpViewer" to keystroke "w" using {command down}'
   ```
   No error but no effect — HelpViewer didn't close

3. **killall HelpViewer**
   ```
   killall HelpViewer
   ```
   `No matching processes belonging to you were found` — process name mismatch or permission issue

4. **cliclick close button**
   ```
   cliclick c:36,22
   ```
   Timed out (15s) — possibly clicking wrong area or triggering modal

5. **osascript activate Claude + screencapture**
   ```
   osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
   screencapture -x /tmp/shot.png
   ```
   Screenshot still showed HelpViewer in front — activate didn't bring Claude window above HelpViewer

6. **computer_use capture with app='Claude'**
   ```
   computer_use(action='capture', app='Claude', mode='vision')
   ```
   `no on-screen window matched app='Claude'` — window not on current Space or occluded

## What worked (fallback)
Gave content to user via clipboard (pbcopy) and asked them to paste manually into Claude Desktop.

## Lessons
- HelpViewer is a stubborn window that resists scripted closing
- `osascript activate` doesn't guarantee window ordering when other windows are in front
- When more than 2 attempts fail, switch to fallback immediately — don't keep trying GUI hacks
- The skill's "快速回退方案" (manual paste) is the correct approach for this scenario
