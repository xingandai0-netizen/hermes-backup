# 小黑 (Xiao Hei) Windows 安装脚本
# 用法: 以管理员身份运行 PowerShell，然后执行:
# Set-ExecutionPolicy Bypass -Scope Process -Force
# .\install-windows.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  小黑 (Xiao Hei) Windows 版本安装器  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[!] 需要管理员权限，请右键以管理员身份运行此脚本" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[✓] 管理员权限确认" -ForegroundColor Green

# 设置路径
$hermesDir = "$env:USERPROFILE\.hermes"
$backupDir = "$PSScriptRoot"

Write-Host ""
Write-Host "[1/6] 创建Hermes目录..." -ForegroundColor Yellow
if (-not (Test-Path $hermesDir)) {
    New-Item -ItemType Directory -Path $hermesDir -Force | Out-Null
    Write-Host "  [✓] 创建 $hermesDir" -ForegroundColor Green
} else {
    Write-Host "  [✓] 目录已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/6] 复制配置文件..." -ForegroundColor Yellow
Copy-Item -Path "$backupDir\SOUL.md" -Destination "$hermesDir\SOUL.md" -Force
Copy-Item -Path "$backupDir\config.yaml" -Destination "$hermesDir\config.yaml" -Force
Write-Host "  [✓] SOUL.md 已复制" -ForegroundColor Green
Write-Host "  [✓] config.yaml 已复制" -ForegroundColor Green

Write-Host ""
Write-Host "[3/6] 复制Skills..." -ForegroundColor Yellow
$skillsDir = "$hermesDir\skills"
if (-not (Test-Path $skillsDir)) {
    New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null
}
Copy-Item -Path "$backupDir\skills\*" -Destination $skillsDir -Recurse -Force
$skillCount = (Get-ChildItem -Path $skillsDir -Directory).Count
Write-Host "  [✓] 已复制 $skillCount 个skills" -ForegroundColor Green

Write-Host ""
Write-Host "[4/6] 检查Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [✓] Python已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  [!] Python未安装，请先安装Python 3.10+" -ForegroundColor Red
    Write-Host "      下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[5/6] 安装Python依赖..." -ForegroundColor Yellow
pip install requests pyautogui pillow 2>&1 | Out-Null
Write-Host "  [✓] Python依赖已安装" -ForegroundColor Green

Write-Host ""
Write-Host "[6/6] 配置UTF-8编码..." -ForegroundColor Yellow
# 设置系统区域设置支持UTF-8
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage"
$current = Get-ItemProperty -Path $regPath -Name "ACP" -ErrorAction SilentlyContinue
if ($current.ACP -ne "65001") {
    Write-Host "  [!] 建议在系统设置中启用Beta: 使用Unicode UTF-8提供全球语言支持" -ForegroundColor Yellow
    Write-Host "      设置 → 时间和语言 → 语言和区域 → 管理语言设置 → 更改系统区域设置" -ForegroundColor Yellow
    Write-Host "      勾选"Beta: 使用Unicode UTF-8提供全球语言支持"" -ForegroundColor Yellow
}
Write-Host "  [✓] 编码配置完成" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 安装Hermes: npm install -g @anthropic-ai/hermes" -ForegroundColor White
Write-Host "2. 运行: hermes" -ForegroundColor White
Write-Host "3. 开始使用小黑！" -ForegroundColor White
Write-Host ""
Write-Host "可选工具安装：" -ForegroundColor Yellow
Write-Host "- x64dbg (动态调试): https://x64dbg.com/" -ForegroundColor White
Write-Host "- Process Hacker (进程分析): https://processhacker.sourceforge.io/" -ForegroundColor White
Write-Host "- Ghidra (逆向分析): https://ghidra-sre.org/" -ForegroundColor White
Write-Host "- radare2 (命令行逆向): choco install radare2" -ForegroundColor White
Write-Host ""
pause
