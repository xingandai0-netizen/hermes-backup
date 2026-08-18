# 大块JSX替换 + 批量样式修改模式

## 大块JSX替换（head/tail拆分法）

**场景**：替换 `{showControls && (...)}` 这种跨越200+行的JSX块。patch工具对如此大的old_string容易匹配失败。

**正确流程**：
```bash
# 1. 找到要替换的块的起止行号
grep -n "showControls" file.tsx  # 找起始行
# 手动或用awk找到结束行

# 2. 拆分文件
head -381 file.tsx > /tmp/before.tsx          # 块之前的内容
tail -n +601 file.tsx > /tmp/after.tsx        # 块之后的内容

# 3. 写新块到临时文件
# 用 write_file 写 /tmp/new-block.tsx

# 4. 重新组装
cat /tmp/before.tsx /tmp/new-block.tsx /tmp/after.tsx > file.tsx

# 5. ⚠️ 必须验证！
wc -l file.tsx                    # 确认行数合理
grep -c "关键函数名" file.tsx     # 确认关键引用还在
npm run build 2>&1 | tail -5      # 构建验证
```

**⚠️ 关键陷阱：tail截断导致语法错误**

`tail -6` 可能截断多行JSX结构。例如：
```
# 原文件末尾：
{showPreview && previewUrl && (
  <PreviewModal ... />
)}
</BaseNode>

# tail -6 只拿到：
<PreviewModal ... />
)}
</BaseNode>...（缺了 {showPreview && 开头）
```

**修复**：tail 后检查第一行是否完整。如果不完整，改为 `tail -n +<行号>` 从正确位置开始。

**验证**：替换后必须 `npm run build`。本次session中video-node.tsx因此报错 `Parsing error: Unexpected token`。

## sed 批量样式替换

**场景**：同一文件中多处相同的border/background值需要统一修改。

```bash
# 替换所有 0.08 border 为 none
sed -i '' 's/border: "0.5px solid rgba(255, 255, 255, 0.08)"/border: "none"/g' file.tsx

# 替换所有 0.06 background 为 0.04
sed -i '' 's/background: "rgba(255, 255, 255, 0.06)"/background: "rgba(255, 255, 255, 0.04)"/g' file.tsx

# 验证替换数量
grep -c 'border: "none"' file.tsx
grep -c '0.5px solid' file.tsx  # 应该为0
```

**⚠️ sed追加行陷阱**

`sed -i '' '/pattern/a\` 在macOS上会把追加内容和下一行合并：
```bash
# ❌ 结果：两行合并成一行
sed -i '' '/background: "#000",/a\
            backdropFilter: "saturate(180%) blur(20px)",' file.tsx
# 输出：background: "#000",backdropFilter: "saturate(180%) blur(20px)",

# ✅ 修复：手动用patch拆开合并行
```

**更好的方式**：用patch工具做精确的单行替换，避免sed的多行问题。

## 完整的TapNow UI修改流程（2026-07-04验证）

1. 读取所有要改的文件，用grep定位修改点
2. 简单修改（单行border/background）→ 用patch或sed
3. 大块替换（showControls面板）→ 用head/tail拆分法
4. 每个文件改完立即验证关键引用（grep -c）
5. 全部改完后 `npm run build` 验证
6. 构建通过后部署
