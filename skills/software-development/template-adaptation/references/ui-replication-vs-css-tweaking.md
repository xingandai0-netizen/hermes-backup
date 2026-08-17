# 1:1复刻 vs CSS微调 — 关键区分（2026-07-05实测）

## 背景

阿戴要求将antoken-v2的工作空间UI"原封不动"替换成TapNow的UI。小黑尝试了增量CSS修改（改变量值、改inline style、改圆角/阴影），结果用户看了效果后说"改了个寂寞"、"到底在几把改啥"，然后git reset回退所有改动。

## 核心教训

**1:1复刻 ≠ 改CSS属性值。1:1复刻 = 整体组件替换。**

### 错误做法（改CSS）
```
1. 改globals.css中的CSS变量值
2. 改组件inline style中的borderRadius、boxShadow等
3. 改字体、改颜色、改间距
4. 保留现有组件的DOM结构和交互逻辑
```

结果：用户看到的还是"那个东西"，只是颜色/圆角稍微不同。

### 正确做法（整体替换）
```
1. 获取目标产品的完整组件代码（DOM + CSS + JS交互）
2. 用目标代码整体替换现有组件文件
3. 只保留业务逻辑（API调用、状态管理、数据流）
4. UI层完全用目标代码
```

## 判断标准

| 用户说的话 | 你的做法 | 对不对 |
|-----------|---------|--------|
| "照搬"、"原封不动"、"1:1复刻" | 整体组件替换 | ✅ |
| "改颜色/改圆角" | 增量CSS修改 | ✅ |
| "参考风格"、"类似" | 增量CSS修改 | ✅ |
| "照搬"+"给我代码" | 整体组件替换 | ✅ |
| "照搬"+"我自己来" | 整体组件替换 | ✅ |

## 具体案例

用户给了TapNow的：
- CSS变量（148个）
- 组件代码（NodeCard、ControlPanel、TextToolbar）
- 动画关键帧（40+个）
- DOM结构（outerHTML）

小黑做了：
- ✅ 替换CSS变量值 → 这步没问题
- ❌ 改inline style中的borderRadius 12→16 → 不够
- ❌ 改box-shadow → 不够
- ❌ 改backdrop-filter → 不够
- ❌ 保留旧的组件结构（带backdrop-filter的Apple Glass风格） → 根本问题

应该做的：
- ✅ 用TapNow的NodeCard组件替换antoken的BaseNode
- ✅ 用TapNow的ControlPanel替换antoken的控制面板
- ✅ 用TapNow的DOM结构替换antoken的节点结构
- ✅ 保留antoken的API调用和状态管理逻辑
