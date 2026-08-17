---
name: lazygit-advanced
description: 高级Git终端客户端lazygit使用指南
version: 1.0.0
author: Hermes Agent
---

# Lazygit高级使用指南

## 核心功能

### 界面布局
- 左上：状态和提交历史
- 右上：文件列表
- 左下：分支列表
- 右下：详情面板

### 常用快捷键

#### 基础操作
- `q`：退出
- `?`：帮助菜单
- `Enter`：选择/打开
- `Esc`：返回/取消
- `Tab`：切换面板

#### 文件操作
- `space`：暂存/取消暂存文件
- `d`：查看文件diff
- `e`：编辑文件
- `o`：打开文件
- `c`：提交更改
- `a`：暂存所有文件

#### 提交操作
- `p`：推送提交
- `P`：拉取提交
- `F`：快进分支
- `M`：合并分支
- `n`：新建分支

#### 分支操作
- `b`：查看分支
- `c`：检出分支
- `d`：删除分支
- `m`：合并分支

### 高级功能

#### 交互式变基
- 选中提交
- 按 `i` 进入交互式变基
- 支持：pick, squash, fixup, reword, drop

#### 储藏操作
- `s`：储藏更改
- `g`：应用储藏
- `d`：删除储藏

#### 远程操作
- `f`：获取远程更新
- `r`：拉取远程分支
- `S`：推送并设置上游

## 常用工作流

### 快速提交
1. `space` 暂存文件
2. `c` 打开提交框
3. 输入提交信息
4. `Enter` 确认提交

### 分支合并
1. `b` 打开分支面板
2. 选择目标分支
3. `M` 合并到当前分支
4. 解决冲突（如果有）

### 变基操作
1. 选择要变基的提交
2. `i` 进入交互式变基
3. 调整提交顺序或操作
4. 保存并执行

## 配置建议

```yaml
# ~/.config/lazygit/config.yml
gui:
  showIcons: true
  showFileTree: true
git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never
```

## 与原生Git对比

| 操作 | Git命令 | Lazygit |
|------|---------|---------|
| 暂存文件 | `git add .` | `space` |
| 提交 | `git commit -m "msg"` | `c` → 输入 |
| 推送 | `git push` | `p` |
| 拉取 | `git pull` | `P` |
| 分支 | `git branch` | `b` |
| 合并 | `git merge` | `M` |

## 安装

```bash
# macOS
brew install lazygit

# Ubuntu
sudo apt install lazygit

# Arch
sudo pacman -S lazygit
```

## 快速启动
```bash
# 在项目目录中运行
cd your-project
lazygit
```
