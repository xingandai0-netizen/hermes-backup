# 批量颜色替换模式（2026-06-15）

## 问题

批量替换颜色时，如果用 `read_file` + `write_file`，文件会被损坏（行号嵌入内容）。

## 正确做法：使用 patch 工具

```python
from hermes_tools import patch

# 逐个文件、逐个颜色替换
files_and_replacements = [
    ("/path/to/file1.tsx", [
        ("#5e6ad2", "#ffffff"),
        ("rgba(94,106,210,0.06)", "rgba(255,255,255,0.06)"),
    ]),
    ("/path/to/file2.tsx", [
        ("#5e6ad2", "#ffffff"),
    ]),
]

for file_path, replacements in files_and_replacements:
    for old_color, new_color in replacements:
        patch(
            path=file_path,
            old_string=old_color,
            new_string=new_color,
            replace_all=True
        )
```

## 完整替换清单（蓝紫色 → 白色）

```python
# 替换规则
hex_replacements = [
    ("#5e6ad2", "#ffffff"),
    ("#7c7cf8", "#e0e0e0"),
    ("#828fff", "#ffffff"),
]

rgba_replacements = [
    ("rgba(94,106,210,0.06)", "rgba(255,255,255,0.06)"),
    ("rgba(94,106,210,0.08)", "rgba(255,255,255,0.08)"),
    ("rgba(94,106,210,0.12)", "rgba(255,255,255,0.12)"),
    ("rgba(94,106,210,0.3)", "rgba(255,255,255,0.3)"),
    ("rgba(94, 106, 210, 0.06)", "rgba(255, 255, 255, 0.06)"),
    ("rgba(94, 106, 210, 0.3)", "rgba(255, 255, 255, 0.3)"),
]
```

## 涉及文件

- `src/styles/globals.css` — CSS 变量
- `src/components/nodes/*.tsx` — 所有节点组件（进度条、状态色）
- `src/components/nodes/BaseNode.tsx` — 类别颜色
- `src/components/sidebar/NodePanel.tsx` — 侧边栏
- `src/components/properties/PropertyPanel.tsx` — 属性面板
- `src/components/VideoPreview.tsx` — 播放器
- `src/components/canvas/WorkflowCanvas.tsx` — 画布

## 替换后验证

```bash
cd ~/antoken/frontend
npm run build  # 必须通过
```

## 陷阱

1. **不要用 read_file + write_file** — 行号会嵌入文件内容
2. **不要用 sed 多行替换** — macOS 上不稳定
3. **替换后必须 build** — 验证编译通过
4. **用 replace_all=True** — 确保所有出现都被替换
