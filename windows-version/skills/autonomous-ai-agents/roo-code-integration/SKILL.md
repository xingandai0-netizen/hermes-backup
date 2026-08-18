---
name: roo-code-integration
description: |
  Roo Code (小白猪) 配置和集成指南。包括安装、API配置、团队协作设置。
tags: [roo-code, vs-code, team, xiaobaizhu, mimo, antokex]
version: 1.0
created: 2026-05-08
---

# Roo Code (小白猪) 配置指南

## 概述

Roo Code 是 VS Code 扩展，作为团队中的代码润色者（小白猪）。
- 角色：代码润色、质量把关
- 模型：mimo-v2.5-pro (通过 antokex.com 中转)
- 安装：VS Code 扩展市场

## 安装步骤

### 1. 安装 VS Code
```bash
# macOS (Intel)
curl -L "https://update.code.visualstudio.com/latest/darwin/stable" -o /tmp/vscode.zip
unzip /tmp/vscode.zip -d /tmp/vscode_extract
cp -R "/tmp/vscode_extract/Visual Studio Code.app" /Applications/

# 配置 PATH
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
```

### 2. 安装 Roo Code 扩展
```bash
code --install-extension RooVeterinaryInc.roo-cline
```

### 3. 配置 API
```json
// ~/Library/Application Support/Code/User/settings.json
{
  "roo-cline.apiProvider": "openai",
  "roo-cline.openaiBaseUrl": "https://antokex.com/v1",
  "roo-cline.openaiApiKey": "用户的API Key",
  "roo-cline.openaiModelId": "mimo-v2.5-pro",
  "roo-cline.model": "mimo-v2.5-pro",
  "roo-cline.customInstructions": "系统提示词..."
}
```

## 团队协作

### 角色定位
- 小白猪 = 代码润色者
- 接收小白(Codex)的初始代码
- 执行2次润色：风格→性能
- 交还小白检查

### 记忆共享
- 共享目录：`~/.roo-code/shared-memory/`
- Skills目录：`~/.roo-code/skills/`
- 与小黑、小白、小黄共享

### 系统提示词
```
你是小白猪 (Xiao Bai Zhu)，阿戴的AI编程助理。
角色：代码润色者
- 接收小白的初始代码
- 第1次润色：代码风格、命名规范、注释完善
- 第2次润色：性能优化、错误处理、边界情况
```

## 使用方法

1. 打开 VS Code
2. `Cmd+Shift+P` → 输入 "Roo"
3. 选择 "Roo Code: Open in Editor"
4. 直接对话，自动调用 MiMo 2.5 Pro

## 计费

- Input: $1/1M tokens
- Output: $3/1M tokens
- 从用户余额自动扣除

## 注意事项

- VS Code 需要匹配系统架构（x86_64 vs arm64）
- 扩展配置存在 VS Code settings.json 中
- 系统提示词通过 customInstructions 设置
