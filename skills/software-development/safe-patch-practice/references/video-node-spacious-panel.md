# 视频节点舒展布局面板模式（2026-07-04）

## 核心设计参数

| 项目 | 紧凑版 | 舒展版 |
|------|--------|--------|
| 面板内边距 | 14px | 20px |
| 面板圆角 | 20px | 20px |
| 面板marginTop | 12px | 20px |
| 行间距 | gap: 8px | gap: 16px (flexDirection: column) |
| 第一行间距 | gap: 8px | gap: 12px |
| 加号按钮 | 28×28 | 36×36 |
| 1x按钮 | padding: 4px 8px | padding: 8px 12px + border |
| 发送胶囊 | padding: 6px 14px | padding: 8px 18px + border |
| 模型/参数按钮 | padding: 6px 12px | padding: 10px 16px |
| 弹出面板内边距 | 12px | 18px |
| 弹出面板间距 | gap: 12px | gap: 16px |
| 弹出面板选项按钮 | padding: 6px 10px | padding: 10px 16px |
| 弹出面板遮罩 | 无 | 有（fixed inset:0，点击关闭） |
| 所有按钮边框 | 无或0.1透明度 | 统一 1px solid rgba(255,255,255,0.06) |

## 面板结构

```
面板容器 (flex column, gap: 16)
├── 第一行 (flex row, gap: 12, alignItems: flex-start)
│   ├── 加号按钮 (36x36, 仅非text模式显示)
│   ├── 输入框 (flex: 1, paddingTop: 4)
│   └── 右侧操作组 (flex row, gap: 8)
│       ├── 1x数量按钮 (padding: 8px 12px)
│       └── 发送胶囊 (padding: 8px 18px, borderRadius: 24)
├── 参考帧缩略图 (仅reference模式)
├── 第二行 (flex row, gap: 10)
│   ├── 模型按钮 (padding: 10px 16px)
│   └── 参数设置按钮 + 弹出面板 (flex: 1)
│       ├── 遮罩 (fixed inset:0, zIndex: 199)
│       └── 弹出面板 (position: absolute, bottom: 100%)
│           ├── 生成方式
│           ├── 比例
│           ├── 清晰度
│           ├── 时长
│           └── 音频开关
└── 错误提示
```

## 弹出面板遮罩模式

```tsx
{showSettingsPopup && (
  <>
    {/* 遮罩：点击关闭 */}
    <div
      style={{ position: "fixed", inset: 0, zIndex: 199 }}
      onClick={() => setShowSettingsPopup(false)}
    />
    {/* 实际面板 */}
    <div style={{ position: "absolute", zIndex: 200, ... }}>
      ...
    </div>
  </>
)}
```

## 状态变量

```tsx
const [showSettingsPopup, setShowSettingsPopup] = useState(false);
const [generateCount, setGenerateCount] = useState(1);
const [audioEnabled, setAudioEnabled] = useState(true);
```

## 设计原则

1. **呼吸空间** — 按钮之间有足够的间距，不会误触
2. **统一边框** — 所有按钮使用 `1px solid rgba(255,255,255,0.06)` 或 `0.08`
3. **圆角层次** — 面板20px，按钮8-10px，胶囊24px
4. **遮罩关闭** — 弹出面板必须有遮罩层，点击空白关闭
5. **箭头加粗** — 发送按钮的箭头用 strokeWidth 2.5
