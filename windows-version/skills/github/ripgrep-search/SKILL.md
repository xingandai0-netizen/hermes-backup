---
name: ripgrep-search
description: 使用ripgrep进行高效代码搜索
version: 1.0.0
author: Hermes Agent
---

# Ripgrep高级搜索指南

## 核心特性

### 超快搜索速度
- 预编译正则表达式
- 并行搜索
- 忽略.gitignore中的文件
- 支持多种编码

## 基础用法

### 基本搜索
```bash
# 搜索当前目录
rg "pattern"

# 指定目录
rg "pattern" /path/to/search

# 搜索特定文件类型
rg "pattern" --type py
```

### 常用选项

#### 搜索选项
- `-i`：忽略大小写
- `-v`：反向匹配
- `-w`：全词匹配
- `-r`：替换匹配文本
- `-l`：只显示文件名
- `-c`：显示匹配数量

#### 输出控制
- `-n`：显示行号
- `-H`：显示文件名
- `-C NUM`：显示上下文
- `-A NUM`：显示后文
- `-B NUM`：显示前文

#### 文件过滤
- `-t TYPE`：文件类型
- `-g GLOB`：文件模式
- `-T TYPE`：排除文件类型
- `--hidden`：包含隐藏文件

## 实用示例

### 代码搜索
```bash
# 搜索TODO注释
rg "TODO|FIXME|XXX" --type py

# 搜索函数定义
rg "def \w+\(" --type py

# 搜索类定义
rg "class \w+" --type py

# 搜索import语句
rg "^import |^from " --type py
```

### 配置文件搜索
```bash
# 搜索配置项
rg "config\[|CONFIG\[" --type py

# 搜索环境变量
rg "process\.env\.|os\.environ" --type py

# 搜索URL
rg "https?://[^\s]+" --type py
```

### 日志分析
```bash
# 搜索错误日志
rg "ERROR|FATAL|CRITICAL" /var/log/

# 搜索特定时间段
rg "2024-01-" /var/log/app.log

# 搜索IP地址
rg "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" --type log
```

## 高级技巧

### 组合搜索
```bash
# 搜索多个模式
rg "pattern1|pattern2" --type py

# 逻辑与搜索
rg "pattern1" | rg "pattern2"

# 排除特定目录
rg "pattern" --glob '!vendor/'
```

### 性能优化
```bash
# 限制搜索深度
rg "pattern" --max-depth 3

# 限制文件大小
rg "pattern" --max-filesize 1M

# 并行线程数
rg "pattern" -j 4
```

### 输出格式
```bash
# JSON输出
rg "pattern" --json

# 自定义格式
rg "pattern" --replace 'Found: $0'

# 零终止符
rg -0 "pattern" | xargs -0 echo
```

## 与grep对比

| 特性 | ripgrep | grep |
|------|---------|------|
| 速度 | 极快 | 快 |
| 默认递归 | 是 | 否 |
| 忽略.gitignore | 是 | 否 |
| Unicode支持 | 是 | 有限 |
| 并行处理 | 是 | 否 |

## 安装

```bash
# macOS
brew install ripgrep

# Ubuntu
sudo apt install ripgrep

# Arch
sudo pacman -S ripgrep

# 从源码
cargo install ripgrep
```

## 别名配置
```bash
# .bashrc 或 .zshrc
alias rg="rg --hidden --follow"
alias rgt="rg --type"
alias rgpy="rg --type py"
alias rgjs="rg --type js"
```

## 实战技巧

### 查找函数使用
```bash
# 查找函数调用
rg "function_name\(" --type py

# 查找方法定义
rg "def function_name\(" --type py

# 查找类方法
rg "class.*:\s*$" -A 10 --type py
```

### 代码审查
```bash
# 查找潜在问题
rg "TODO|FIXME|XXX|HACK" --type py

# 查找硬编码字符串
rg '"[^"]{10,}"' --type py

# 查找敏感信息
rg "password|secret|token" -i --type py
```
