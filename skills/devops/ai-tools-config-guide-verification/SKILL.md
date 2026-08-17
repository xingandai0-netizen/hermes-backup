---
name: ai-tools-config-guide-verification
description: |
  验证AI工具配置攻略的正确性。对比官方文档、检查配置参数、
  实地测试连接。适用于antokex.com的12+工具攻略维护。
tags: [verification, guides, ai-tools, configuration, testing]
version: 1.0
created: 2026-05-08
---

# AI工具配置攻略验证指南

## 概述

当维护多个AI工具的配置攻略时，需要系统化验证每个攻略的正确性。
本指南提供标准化的验证流程。

## 验证标准

对每个攻略页面检查以下内容：

### 1. BASE_URL 正确性
- OpenAI格式: `https://antokex.com/v1`
- Anthropic格式: `https://antokex.com`（不含/v1）
- 特殊工具（TRAE、CodeBuddy）: 需要完整端点 `/v1/chat/completions`

### 2. 模型名称
- 统一使用: `mimo-v2.5-pro`
- 检查是否与上游API的实际模型名一致

### 3. 配置文件路径
- 检查路径是否正确（macOS/Linux/Windows）
- 检查目录是否存在或需要创建

### 4. 配置示例代码
- JSON/TOML/YAML语法正确
- 所有占位符有说明
- 代码可直接复制使用

### 5. 安装命令
- 命令是否正确
- 依赖是否说明（Node.js版本等）

### 6. 特殊要求
- Codex: 需要v0.80.0版本（新版不支持自定义Provider）
- TRAE/CodeBuddy: 需要完整端点URL
- Claude Code: 需要`~/.claude.json`文件

## 验证流程

```
Step 1: 下载所有攻略页面
  ssh root@server 'cat /var/www/antokex/guides/*.html' > /tmp/guides/

Step 2: 对比官方文档
  访问 https://platform.xiaomimimo.com/docs/zh-CN/integration/
  逐个对比每个工具的配置

Step 3: 检查HTML结构
  - DOCTYPE、html、head、body标签完整
  - UTF-8编码，无乱码
  - 所有链接可点击

Step 4: 实地测试
  - 用测试Key调用API验证连通性
  - 检查计费是否正常

Step 5: 修复并部署
  - 修复发现的问题
  - 部署到服务器
  - 验证修复
```

## 工具列表与格式

| 工具 | 格式 | 特殊要求 |
|------|------|---------|
| Claude Code | Anthropic | 需要~/.claude.json |
| OpenCode | OpenAI | - |
| Cline | OpenAI | - |
| Kilo Code | OpenAI | - |
| Roo Code | OpenAI | - |
| Cherry Studio | OpenAI | 内置Xiaomi MiMo |
| Codex | OpenAI | 需要v0.80.0 |
| Zed | OpenAI | - |
| TRAE | OpenAI | 完整端点URL |
| Qwen Code | OpenAI | - |
| CodeBuddy | OpenAI | 完整端点URL |
| OpenClaw | OpenAI | - |

## 参考链接

- 小米官方集成文档: https://platform.xiaomimimo.com/docs/zh-CN/integration/
- antokex.com攻略页面: https://antokex.com/ai-tools
