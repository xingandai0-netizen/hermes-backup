#!/usr/bin/env python3
"""
小白 (Xiao Bai) — 可对话的GUI自动化Agent
基于Agent-S + MiMo-V2-Omni

两种模式:
  1. 对话模式: 普通聊天(用MiMo直接回复)
  2. GUI模式: 检测到GUI操作指令时，调用Agent-S执行桌面操作

启动方式: ~/agent-s-xiaobai.sh
"""

import os
import sys
import io

# 确保agent-s在路径中
sys.path.insert(0, os.path.expanduser("~/github-skills/agent-s"))

import openai

API_BASE = "https://antokex.com/v1"
API_KEY = os.environ.get("XIAOBAI_API_KEY", "")
MODEL = "mimo-v2-omni"

SYSTEM_PROMPT = """你是小白(Xiao Bai)，一个AI助手。你是小黑(Hermes Agent)的搭档，组成'黑白双煞'团队服务阿戴。

你可以：
1. 普通对话——直接回答问题
2. GUI操作——当用户要求操作电脑(打开应用、点击、截图等)，你会截图分析屏幕并执行操作

回答风格：简洁、友好、实用。中文为主。"""

def load_shared_memory():
    """加载共享记忆"""
    memory_path = os.path.expanduser("~/xiaobai/memory/shared-memory.md")
    skills_dir = os.path.expanduser("~/xiaobai/skills/")
    parts = []
    if os.path.exists(memory_path):
        with open(memory_path, 'r') as f:
            parts.append("## 共享记忆\n" + f.read()[:3000])
    if os.path.isdir(skills_dir):
        for fn in sorted(os.listdir(skills_dir))[:5]:
            fp = os.path.join(skills_dir, fn)
            if fn.endswith('.md'):
                with open(fp, 'r') as f:
                    parts.append(f"## {fn}\n" + f.read()[:1000])
    return "\n\n".join(parts)

def main():
    print("=" * 50)
    print("  小白 (Xiao Bai) — AI助手 + GUI自动化")
    print("  模型: mimo-v2-omni via antokex.com")
    print("  输入 'quit' 退出")
    print("=" * 50)
    print()

    if not API_KEY:
        print("ERROR: XIAOBAI_API_KEY not set!")
        sys.exit(1)

    # 加载共享记忆
    shared = load_shared_memory()
    system = SYSTEM_PROMPT
    if shared:
        system += "\n\n" + shared

    client = openai.OpenAI(base_url=API_BASE, api_key=API_KEY)
    messages = [{"role": "system", "content": system}]

    while True:
        try:
            user_input = input("\033[36m阿戴 > \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q', 'n'):
            print("再见！")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            print("\033[33m小白 > \033[0m", end="", flush=True)
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_tokens=2000,
                stream=True,
            )
            full_reply = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    print(text, end="", flush=True)
                    full_reply += text
            print()
            messages.append({"role": "assistant", "content": full_reply})
        except Exception as e:
            print(f"\n错误: {e}")

if __name__ == "__main__":
    main()
