# 小黑 (Xiao Hei) — Windows 版本

> Hermes Agent 的 Windows 适配版本，针对 Windows 系统做了全面兼容性处理。

## 📋 功能对比：macOS vs Windows

### ✅ 完全可用

| 功能 | 说明 |
|---|---|
| AI对话 | 所有模型正常工作 |
| 文件操作 | read_file/write_file/patch/search_files |
| 终端命令 | PowerShell/CMD（替换了bash） |
| 浏览器自动化 | browser_navigate/click/type等 |
| 网络搜索 | web_search/web_extract |
| 图片生成 | image_generate |
| 代码编写 | 所有编程语言 |
| Skills系统 | 77个skills可用 |
| 知识库 | SOUL.md + memories |
| 定时任务 | cronjob |
| 子代理 | delegate_task |
| 任务管理 | todo |
| 会话搜索 | session_search |
| 消息发送 | send_message |
| 文字转语音 | text_to_speech |
| 文件投递 | write_file/read_file |

### ⚠️ 部分可用（需要替代方案）

| 功能 | macOS | Windows替代 |
|---|---|---|
| 桌面自动化 | cua-driver (computer_use) | PyAutoGUI / 请用户手动操作 |
| 本地图片分析 | vision_analyze 直接读取 | 用browser打开图片再分析 |
| 逆向调试 | LLDB MCP | x64dbg / WinDbg / GDB |
| 内存扫描 | Memscan MCP | Process Hacker / Cheat Engine |
| 终端自动化 | bash/zsh 脚本 | PowerShell 脚本 |
| 包管理 | brew | choco / winget / scoop |
| 路径格式 | /Users/... | C:\Users\... |

### ❌ 不可用（macOS专属）

| 功能 | 原因 | 替代建议 |
|---|---|---|
| computer_use | cua-driver 仅支持 macOS | 用PyAutoGUI或手动操作 |
| Ghidra MCP | 需要配置Java环境 | 安装Ghidra后配置路径 |
| LLDB MCP | LLDB是macOS/LLVM专属 | 用WinDbg或GDB |
| Memscan MCP | 基于LLDB | 用Process Hacker |
| AppleScript | macOS专属语言 | 用PowerShell替代 |
| Find My / iMessage | Apple生态 | 无替代 |
| macOS WeChat自动化 | 基于AppleScript | 用Python + pyautogui |

## 🛠️ 安装指南

### 前置要求

1. **Python 3.10+**
   ```powershell
   # 检查Python版本
   python --version
   # 如果没有，去 https://www.python.org/downloads/ 下载
   ```

2. **Node.js 18+**（Hermes需要）
   ```powershell
   # 检查Node版本
   node --version
   # 如果没有，去 https://nodejs.org/ 下载
   ```

3. **Git**
   ```powershell
   git --version
   # 如果没有，去 https://git-scm.com/download/win 下载
   ```

### 安装Hermes

```powershell
# 1. 克隆仓库
git clone https://github.com/xingandai0-netizen/hermes-backup.git
cd hermes-backup

# 2. 切换到windows-version分支
git checkout windows-version

# 3. 复制配置到Hermes目录
# Windows上Hermes配置目录在：
# C:\Users\<你的用户名>\.hermes\
Copy-Item -Path "SOUL.md" -Destination "$env:USERPROFILE\.hermes\SOUL.md" -Force
Copy-Item -Path "config.yaml" -Destination "$env:USERPROFILE\.hermes\config.yaml" -Force

# 4. 复制skills
Copy-Item -Path "skills\*" -Destination "$env:USERPROFILE\.hermes\skills\" -Recurse -Force

# 5. 安装Python依赖
pip install requests pyautogui pillow
```

### 安装Windows替代工具

```powershell
# 安装Chocolatey（Windows包管理器）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装常用工具
choco install radare2 -y    # 命令行逆向
choco install git -y        # Git
choco install python -y     # Python
choco install nodejs -y     # Node.js

# 手动下载安装（推荐）
# x64dbg: https://x64dbg.com/ （动态调试）
# Process Hacker: https://processhacker.sourceforge.io/ （进程/内存分析）
# dnSpy: https://github.com/dnSpy/dnSpy （.NET逆向）
# Ghidra: https://ghidra-sre.org/ （需要Java）
```

## 📁 目录结构

```
windows-version/
├── SOUL.md              # 小黑人格定义（Windows适配版）
├── config.yaml          # Hermes配置（已移除macOS专属MCP）
├── README.md            # 本文件
├── skills/              # 77个Windows兼容skills
│   ├── security/        # 安全研究
│   ├── software-development/  # 软件开发
│   ├── design/          # UI/UX设计
│   ├── research/        # 研究分析
│   ├── devops/          # 运维部署
│   ├── mlops/           # 机器学习运维
│   ├── productivity/    # 生产力工具
│   ├── github/          # GitHub工作流
│   ├── red-teaming/     # 红队工具
│   ├── autonomous-ai-agents/  # AI代理
│   └── ...              # 更多分类
├── bin/                 # 工具二进制文件
├── scripts/             # 辅助脚本
└── memories/            # 记忆数据
```

## 🔧 常见问题

### Q: 权限不足怎么办？
A: 右键点击PowerShell → "以管理员身份运行"

### Q: 中文乱码怎么办？
A: 在PowerShell中执行：
```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Q: 路径错误怎么办？
A: Windows路径用反斜杠或正斜杠都可以：
```powershell
# 正确
C:\Users\username\Desktop
C:/Users/username/Desktop

# 错误（这是macOS路径）
/Users/username/Desktop
```

### Q: 如何查看图片？
A: 用browser工具打开图片文件：
```
browser_navigate(url="file:///C:/Users/username/Desktop/image.png")
browser_vision(question="这张图片是什么内容？")
```

### Q: 如何执行bash命令？
A: 安装Git Bash后可以用bash语法，或者用PowerShell语法：
```powershell
# PowerShell
Get-ChildItem          # 等同于 ls
Copy-Item              # 等同于 cp
Remove-Item            # 等同于 rm
Set-Location           # 等同于 cd
```

## 📊 性能对比

| 指标 | macOS版 | Windows版 |
|---|---|---|
| Skills数量 | 90+ | 77 |
| MCP工具 | 3个（Ghidra/LLDB/Memscan） | 1个（Ghidra，需配置） |
| 桌面控制 | ✅ 完整支持 | ❌ 不支持 |
| 逆向分析 | ✅ 完整工具链 | ⚠️ 需手动安装工具 |
| 自动化 | ✅ AppleScript+终端 | ⚠️ PowerShell+PyAutoGUI |
| 启动速度 | 快 | 快 |
| 稳定性 | 高 | 高 |

## 📝 更新日志

### 2026-08-18
- 初始版本发布
- 移除macOS专属MCP服务器
- 更新SOUL.md添加Windows适配说明
- 保留77个跨平台兼容skills
- 添加Windows安装指南
- 添加常见问题解答

## ⚠️ 已知限制

1. **桌面自动化受限** — 无法像macOS版那样完全控制桌面
2. **逆向工具链不完整** — 需要手动安装x64dbg等工具
3. **部分skills引用macOS命令** — 可能需要手动修改路径
4. **Ghidra MCP需要Java** — 需要先安装JDK
5. **图片分析需要browser** — 无法直接用vision_analyze读取本地图片

## 🤝 贡献

如果你在Windows上发现了兼容性问题或有更好的替代方案，请提交Issue或Pull Request。

## 📄 许可

与主仓库保持一致。
