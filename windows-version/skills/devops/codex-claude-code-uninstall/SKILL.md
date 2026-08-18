---
name: codex-claude-code-uninstall
description: "Codex CLI 和 Claude Code CLI 完全卸载指南。覆盖npm包、二进制、配置目录、Library缓存/日志/偏好、AppSupport临时文件、Keychain的全量清理。"
tags: [devops, uninstall, codex, claude-code, cleanup]
triggers:
  - 删除/卸载 Codex CLI
  - 删除/卸载 Claude Code CLI
  - 删除/卸载 Codex.app / Claude.app 桌面应用
  - 清理AI编码工具残留
---

# Codex & Claude Code CLI 完全卸载指南

## ⚠️ 关键坑点

### 路径展开陷阱
`rm -rf ~/.codex` 在 Hermes 的 `execute_code` > `terminal()` 中可能**静默失败**（返回成功但文件仍在）。
**必须使用绝对路径**。验证方法：执行删除后**必须再次 ls 确认**，不能只信 terminal 返回值。

## 完整清理清单

### Codex CLI (@openai/codex)
| # | 目标 | 类型 |
|---|------|------|
| 1 | ~/.codex/ | 主配置目录（sqlite数据库70MB+、session、config、auth） |
| 2 | ~/.local/bin/codex | 符号链接 → npm global |
| 3 | npm @openai/codex | 全局包 |
| 4 | ~/Library/Caches/com.openai.codex | 系统缓存 |
| 5 | ~/Library/Logs/com.openai.codex | 系统日志 |
| 6 | ~/Library/Preferences/com.openai.codex.plist | 偏好设置 |
| 7 | ~/Library/Application Support/Codex/.com.openai.codex.* | Electron临时文件（30+个） |

### Claude Code CLI (@anthropic-ai/claude-code)
| # | 目标 | 类型 |
|---|------|------|
| 1 | ~/.claude/ | 主配置目录（sessions、plugins、skills、settings.json） |
| 2 | ~/.local/bin/claude | 符号链接 → npm global |
| 3 | ~/.claude.json | 全局状态 |
| 4 | npm @anthropic-ai/claude-code | 全局包 |

### macOS .app 桌面应用（Launchpad可见）
| # | 目标 | 类型 |
|---|------|------|
| 1 | /Applications/Codex.app | Codex桌面应用 (Electron, com.openai.codex) |
| 2 | /Applications/Claude.app | Claude Desktop桌面应用 (com.anthropic.claudefordesktop) |
| 3 | ~/Applications/Claude Code URL Handler.app | Claude Code URL跳转处理器 (claude-cli:// 协议) |
| 4 | ~/Library/Preferences/com.claudechat.app.plist | ClaudeChat偏好设置 |
| 5 | ~/Library/Preferences/ClaudeChatSelfTests.plist | ClaudeChat测试偏好 |
| 6 | ~/Library/Application Support/Claude/ | Claude Desktop AppSupport数据 |
| 7 | ~/Library/Caches/com.claudechat.app | Claude Desktop缓存 |

> ⚠️ Claude.app 是Claude Desktop桌面聊天应用，和Claude Code CLI是不同的东西。用户可能想保留它，执行前确认。

### Keychain（通常无条目，尝试清理）
- `security delete-generic-password -s 'codex-cli'`
- `security delete-generic-password -s 'com.openai.codex'`

## 执行步骤

1. **npm卸载**: `npm uninstall -g @openai/codex @anthropic-ai/claude-code`
2. **符号链接**: 删除 ~/.local/bin/codex 和 ~/.local/bin/claude
3. **主配置目录**: 删除 ~/.codex/ 和 ~/.claude/ 和 ~/.claude.json（⚠️用绝对路径）
4. **Library缓存/日志/偏好**: 删除 Caches/com.openai.codex、Logs/com.openai.codex、Preferences/com.openai.codex.plist
5. **AppSupport临时文件**: 删除 Application Support/Codex/.com.openai.codex.*
6. **Keychain**: 尝试删除 codex-cli 和 com.openai.codex 条目
7. **macOS .app 应用**: 删除 /Applications/Codex.app、~/Applications/Claude Code URL Handler.app，以及可选的 /Applications/Claude.app + 其相关Library文件（需用户确认）
8. **⚠️ 每一步删除后都必须 ls 验证**，不要假设成功

## 验证清单

执行完后逐项检查（每一项都必须实际 ls/which 确认）：
- which codex → 无输出
- which claude → 无输出
- ls ~/.codex → No such file
- ls ~/.claude → No such file
- ls ~/.claude.json → No such file
- npm list -g 无 codex/claude 条目
- ls ~/Library/Caches/com.openai.codex → 无输出
- ls ~/Library/Logs/com.openai.codex → 无输出
- ls ~/Library/Preferences/com.openai.codex.plist → 无输出

## 注意事项
- **Claude.app (Claude Desktop)** — 和Claude Code CLI是不同的东西。用户可能想保留或删除，执行前**必须确认**
- **Desktop下载文件** — 用户桌面上可能有刚下载的安装包，不要误删
- **Hermes Agent** (~/.hermes/) — 绝对不能碰

## 踩坑记录
- 2026-05-08: execute_code中terminal()用`~`路径删除失败（静默成功），必须用绝对路径
- Library缓存首次rm -rf后ls仍显示内容，需要二次删除+验证
