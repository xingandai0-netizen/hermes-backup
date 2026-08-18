#!/bin/bash
# 小白 (Xiao Bai) — 启动脚本
# 视觉引擎: mimo-v2-omni via antokex
# 使用: ~/agent-s-xiaobai.sh ["任务指令"]
# 不带参数 = 交互模式(输入Query对话)
# 带参数 = 单次任务模式

export XIAOBAI_API_KEY="sk-HwIi53zWV9doQayy8FwUhHYJiCrguvA16eOHHt4K8anDdrjY"
export OPENAI_API_KEY="$XIAOBAI_API_KEY"

VENV=~/agent-s-venv
source "$VENV/bin/activate"

echo ""
echo "=================================================="
echo "  小白 (Xiao Bai) — AI助手 + GUI自动化"
echo "  模型: mimo-v2-omni via antokex.com"
echo "  输入 'quit' 退出"
echo "=================================================="
echo ""

if [ -n "$1" ]; then
    # 单次任务模式
    python3 ~/xiaobai/xiaobai.py <<< "$1
quit"
else
    # 交互模式
    python3 ~/xiaobai/xiaobai.py
fi
