---
name: better-icons
description: 图标搜索引擎。从200+图标库(Iconify)搜索和获取SVG。触发：需要图标、搜索图标、获取SVG。
version: 1.0
source: better-auth/better-icons (995 stars)
---

# Better Icons

## CLI命令
```bash
# 搜索图标
better-icons search <query> [--prefix <prefix>] [--limit <n>] [--json]

# 搜索并下载为SVG
better-icons search <query> -d [dir] [--color <color>] [--size <px>]

# 获取图标SVG(输出到stdout)
better-icons get <icon-id> [--color <color>] [--size <px>] [--json]
```

## 安装
```bash
npm install -g better-icons
# 或
bun add -g better-icons
```

## 常用前缀
- lucide: — 通用UI图标
- phosphor: — Phosphor图标集
- material-symbols: — Material Design
- tabler: — Tabler图标
- radix-icons: — Radix UI图标
- carbon: — IBM Carbon

## 示例
```bash
better-icons search arrow --limit 10
better-icons get lucide:home > icon.svg
better-icons search "settings" --prefix lucide: --json
```
