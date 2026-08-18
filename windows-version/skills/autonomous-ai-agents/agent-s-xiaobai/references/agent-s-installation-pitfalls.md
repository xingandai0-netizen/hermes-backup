## Agent-S 安装踩坑记录 (2026-05-13)

### 1. Python版本限制
setup.py限制 `python_requires=">=3.9, <=3.12"`，但实际是严格比较：
- Python 3.12.9 会被 `<=3.12` 拒绝（PEP440比较 3.12.9 > 3.12）
- **修复**: 直接改setup.py为 `python_requires=">=3.9"`
- 系统Python 3.14太新也不行，需要用brew的python3.12

### 2. 依赖极重
- pyobjc全套（macOS）、paddlepaddle+paddleocr（首次运行下载模型）
- 必须用venv隔离，否则污染系统环境
- venv路径: ~/agent-s-venv (Python 3.12.9)

### 3. CLI交互模式限制
- `cli_app.py` 无 `--task` 参数时调用 `input("Query: ")` — 需要PTY
- 从execute_code/subprocess调用会报 EOFError
- **必须**通过 `osascript` 开新Terminal窗口运行

### 4. osascript环境变量丢失
- `osascript -e 'do script "export FOO=bar && command"'` 的环境变量不可靠
- **修复**: 把所有key直接写在脚本文件里，不依赖继承
- 启动脚本: ~/agent-s-xiaobai.sh (key硬编码在内)

### 5. osascript注入查询到Terminal
```applescript
tell application "Terminal"
    repeat with i from 1 to (count of windows)
        try
            if (processes of selected tab of window i) contains "python3" then
                set frontmost of window i to true
                do script "你的任务" in selected tab of window i
                return "sent to window " & i
            end if
        end try
    end repeat
end tell
```

### 6. Agent-S双模型架构
- `--model`: 生成/推理模型 (Worker)
- `--ground_model`: 视觉定位模型 (Grounding) — 理解截图坐标
- 两个可以用同一个模型（如mimo-v2-omni），也可以不同
- `--grounding_width/height`: 屏幕分辨率缩放后的值，影响上下文大小

### 7. 星辰API模型发现
```
curl -s "https://api.ai6800.com/v1/skills/models?type=image" -H "Authorization: Bearer <key>"
curl -s "https://api.ai6800.com/v1/skills/models?type=video" -H "Authorization: Bearer <key>"
```
- Nano Banana = gemini-3-pro-image-preview
- Nano Banana 2 = gemini-3.1-flash-image-preview
