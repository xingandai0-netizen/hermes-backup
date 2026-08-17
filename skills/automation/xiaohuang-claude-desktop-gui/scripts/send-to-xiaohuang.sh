#!/bin/bash
# send-to-xiaohuang.sh — 一键发送任务给小黄并等待+提取回复
# 用法: bash send-to-xiaohuang.sh <task-file.md> [wait-seconds]
# 依赖: cliclick, swift, screencapture

set -e
TASK_FILE="${1:?用法: $0 <task-file.md> [wait-seconds]}"
WAIT_SECONDS="${2:-120}"
SKILL_DIR="$(dirname "$0")"
WORK_DIR="/tmp/team-collab"

mkdir -p "$WORK_DIR"

echo "=== 小黄GUI对接 ==="
echo "任务文件: $TASK_FILE"
echo "等待时间: ${WAIT_SECONDS}秒"

# ===== Step 1: 发送任务 =====
echo "[1/4] 发送任务到小黄..."
cat "$TASK_FILE" | pbcopy
sleep 0.3

osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 2

# 运行paste脚本（粘贴+清空旧内容）
swift "${SKILL_DIR}/paste.swift"

sleep 1

# ===== Step 2: Enter发送 =====
echo "[2/4] 发送Enter..."
swift -e '
import Cocoa
let src = CGEventSource(stateID: .hidSystemState)
let enter = CGEvent(keyboardEventSource: src, virtualKey: 0x24, keyDown: true)!
enter.post(tap: .cghidEventTap)
usleep(50000)
let enterUp = CGEvent(keyboardEventSource: src, virtualKey: 0x24, keyDown: false)!
enterUp.post(tap: .cghidEventTap)
print("Enter sent")
'

# ===== Step 3: 等待 =====
echo "[3/4] 等待 ${WAIT_SECONDS} 秒让Claude生成回复..."

# 每30秒做一次OCR快检
for ((i=1; i<=WAIT_SECONDS/30; i++)); do
    sleep 30
    elapsed=$((i * 30))
    
    osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate' 2>/dev/null
    sleep 1
    screencapture -x "$WORK_DIR/poll-${i}.png"
    osascript -e 'tell application "Terminal" to activate' 2>/dev/null
    sleep 0.5
    sips -z 900 1440 "$WORK_DIR/poll-${i}.png" --out "$WORK_DIR/poll-${i}-s.png" 2>/dev/null
    
    # 检查是否包含完成标志
    OCR=$(swift "${SKILL_DIR}/ocr-file.swift" "$WORK_DIR/poll-${i}-s.png" 2>/dev/null)
    if echo "$OCR" | grep -q "Claude is AI\|Next time, try\|Write a message"; then
        echo "  [${elapsed}s] 检测到回复完成！"
        break
    else
        echo "  [${elapsed}s] 仍在生成中..."
    fi
done

# 额外等10秒确保完整
sleep 10

# ===== Step 4: 提取完整回复 =====
echo "[4/4] 提取小黄回复..."

osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 1
cliclick c:700,400
sleep 0.3

# Cmd+A + Cmd+C
swift -e '
import Cocoa
let src = CGEventSource(stateID: .hidSystemState)

// Cmd+A
let keyA = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: true)!
keyA.flags = .maskCommand
keyA.post(tap: .cghidEventTap)
usleep(100000)
let keyAUp = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: false)!
keyAUp.flags = .maskCommand
keyAUp.post(tap: .cghidEventTap)
usleep(200000)

// Cmd+C
let keyC = CGEvent(keyboardEventSource: src, virtualKey: 0x08, keyDown: true)!
keyC.flags = .maskCommand
keyC.post(tap: .cghidEventTap)
usleep(100000)
let keyCUp = CGEvent(keyboardEventSource: src, virtualKey: 0x08, keyDown: false)!
keyCUp.flags = .maskCommand
keyCUp.post(tap: .cghidEventTap)
print("Cmd+A Cmd+C done")
'

sleep 1
osascript -e 'tell application "Terminal" to activate'
sleep 0.5

OUTPUT="$WORK_DIR/xiaohuang-response-$(date +%Y%m%d_%H%M%S).md"
pbpaste > "$OUTPUT"
LINES=$(wc -l < "$OUTPUT")
CHARS=$(wc -c < "$OUTPUT")

echo ""
echo "=== 完成 ==="
echo "响应已保存: $OUTPUT"
echo "总行数: $LINES  总字节: $CHARS"
echo ""
echo "注意: 响应包含UI杂文，需程序化清理后使用"
