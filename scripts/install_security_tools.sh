#!/bin/bash
# Hermes 安全工具链安装脚本
# 运行方式: bash ~/.hermes/scripts/install_security_tools.sh

echo "=========================================="
echo "Hermes 安全工具链安装"
echo "=========================================="

# 1. 检查 Homebrew
if ! command -v brew &>/dev/null; then
    echo "❌ Homebrew 未安装，请先安装: https://brew.sh"
    exit 1
fi
echo "✅ Homebrew 已安装"

# 2. 安装渗透测试工具
echo ""
echo "📦 安装渗透测试工具..."
TOOLS="nmap sqlmap nuclei subfinder nikto ffuf gobuster"

for tool in $TOOLS; do
    if command -v $tool &>/dev/null; then
        echo "  ✅ $tool 已安装"
    else
        echo "  ⏳ 安装 $tool..."
        brew install $tool 2>&1 | tail -3
        if command -v $tool &>/dev/null; then
            echo "  ✅ $tool 安装成功"
        else
            echo "  ⚠️ $tool 安装可能失败，请手动检查"
        fi
    fi
done

# 3. 配置 pentestMCP
echo ""
echo "📦 配置 pentestMCP..."
if [ -d "$HOME/security-research/pentestMCP" ]; then
    echo "  ✅ pentestMCP 已下载"
    cd "$HOME/security-research/pentestMCP"
    if [ -f "requirements.txt" ]; then
        echo "  ⏳ 安装 pentestMCP 依赖..."
        uv pip install -r requirements.txt 2>&1 | tail -3
    fi
else
    echo "  ⏳ 下载 pentestMCP..."
    cd "$HOME/security-research"
    git clone --depth 1 https://github.com/ramkansal/pentestMCP.git 2>&1 | tail -3
fi

# 4. 配置 Chrome DevTools MCP
echo ""
echo "📦 配置 Chrome DevTools MCP..."
if command -v npx &>/dev/null; then
    echo "  ✅ npx 已安装"
    echo "  ℹ️ Chrome DevTools MCP 已配置到 Hermes config.yaml"
else
    echo "  ❌ npx 未安装，请安装 Node.js"
fi

# 5. 验证 VulnClaw
echo ""
echo "📦 验证 VulnClaw..."
if command -v vulnclaw &>/dev/null; then
    echo "  ✅ VulnClaw 已安装: $(vulnclaw --version 2>&1)"
else
    echo "  ⏳ 安装 VulnClaw..."
    uv pip install vulnclaw 2>&1 | tail -3
fi

# 6. 验证 Shannon
echo ""
echo "📦 验证 Shannon..."
if [ -d "$HOME/security-research/shannon" ]; then
    echo "  ✅ Shannon 已下载"
    echo "  ℹ️ Shannon 需要 Docker + Anthropic API Key 才能运行"
    echo "  ℹ️ 配置: cd ~/security-research/shannon && cp .env.example .env"
else
    echo "  ❌ Shannon 未下载"
fi

# 7. 汇总
echo ""
echo "=========================================="
echo "安装汇总"
echo "=========================================="
for tool in nmap sqlmap nuclei subfinder nikto ffuf gobuster vulnclaw; do
    if command -v $tool &>/dev/null; then
        echo "  ✅ $tool"
    else
        echo "  ❌ $tool"
    fi
done

echo ""
echo "=========================================="
echo "MCP 服务器配置"
echo "=========================================="
echo "  ✅ chrome-devtools (Google官方)"
echo "  ✅ vulnclaw-chrome"
echo "  ✅ vulnclaw-burp"
echo "  ⏳ pentest-mcp (待启用)"
echo ""
echo "完成！重启 Hermes 生效。"
