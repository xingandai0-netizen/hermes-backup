# Readable Node Sizing — Final Working Values

User (阿戴) first said "素材框太大了" (240px), then after reducing to 160px said "素材框清晰度不足，十分模糊" (too blurry). Final balance: **220px** with larger fonts.

## Node Dimensions (BaseNode.tsx)

| Property | Initial | After Fix 1 | After Fix 2 | Final (Working) |
|----------|---------|-------------|-------------|-----------------|
| Width | 240px | 200px | 160px | **220px** |
| Border-radius | 12px | 8px | 8px | **8px** |
| Icon size | 24x24 | 20x20 | 16x16 | **22x22** |
| Title font | 13px | 12px | 11px | **13px (weight 600)** |
| Port font | 11px | 9px | 9px | **11px** |
| Port type badge | 9px | 7px | 7px | **9px** |
| Handle size | 12px | 10px | 8px | **10px** |
| Handle border | 2px | 1.5px | 1.5px | **2px solid #1a1a2e** |
| Header padding | 10px 12px | 8px 10px | 6px 8px | **8px 10px** |
| Body padding | 8px 12px | 6px 10px | 4px 8px | **6px 10px** |
| Input textarea height | — | — | 40px | **50px** |
| Input textarea font | — | — | 9px | **12px** |
| Button font | — | — | 9px | **12px** |
| Button padding | — | — | 4px 8px | **6px 10px** |
| Preview image height | — | — | 80px | **100px** |

## Sidebar Dimensions (NodePanel.tsx)

| Property | Initial | Final |
|----------|---------|-------|
| Width | w-60 (240px) | **w-48 (192px)** |
| Padding | p-3 (12px) | **p-2 (8px)** |
| Category spacing | space-y-4 | **space-y-3** |
| Node card padding | px-3 py-2 | **px-2 py-1.5** |

## Working BaseNode Style (copy-paste ready)

```tsx
style={{
  width: 220,
  background: "linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.015) 100%)",
  border: selected ? `1.5px solid ${categoryColor}` : "1px solid rgba(255,255,255,0.1)",
  borderRadius: 8,
  boxShadow: selected
    ? `0 0 0 1px ${categoryColor}50, 0 0 12px ${categoryColor}20, 0 4px 12px rgba(0,0,0,0.3)`
    : "0 2px 6px rgba(0,0,0,0.2)",
  transition: "all 0.2s ease",
  overflow: "hidden",
  position: "relative",
}}
```

## Working Handle Style

```tsx
<Handle
  type="target"
  position={Position.Left}
  id={port.id}
  style={{
    background: portColor(port.type),
    border: "2px solid #1a1a2e",
    width: 10,
    height: 10,
    top: "auto",
    left: -14,
    transition: "all 0.15s ease",
  }}
/>
```

## Chinese Localization Map

All UI text MUST be in Chinese. Keep only brand names (Antoken) and technical terms (API, URL) in English.

### Top Bar
- AI Workflow → AI工作流
- API Connected → API已连接
- No API Key → 未配置API
- Clear → 清空
- Execute → 执行
- Settings → 设置
- Close → 关闭

### Sidebar
- Nodes → 节点面板
- Click to add / drag to canvas → 点击添加 / 拖拽到画布
- Input → 输入
- AI Generation → AI生成
- Processing → 处理
- Output → 输出
- SKU Import → SKU导入
- Image Gen → 图片生成
- Video Gen → 视频生成
- Image Process → 图片处理
- Size Adapter → 尺寸适配
- Export → 导出

### Node Fields
- Prompt → Prompt (keep English)
- Size → 尺寸
- Quality → 质量
- N → 数量
- Duration → 时长
- Resolution → 分辨率
- Format → 格式
- Platform → 平台
- Operation → 操作
- Model → 模型
- Input → 输入
- Output → 输出

### Controls
- Fit view → 适应视图
- Mini map → 小地图
- Undo → 撤销
- Redo → 重做

### Canvas
- Drag nodes from the sidebar → 从左侧拖拽节点到画布
- Double-click to edit properties → 双击节点编辑属性

### Settings Modal
- API Settings → API设置
- Configure AI model connection parameters → 配置AI模型连接参数
- Model Selection → 模型选择
- Temperature → 温度
- Test Connection → 测试连接
- Cancel → 取消
- Save Settings → 保存设置
- Connection successful → 连接成功
- Connection failed → 连接失败
- Image Generation Model → 图片生成模型
- Video Generation Model → 视频生成模型

## Lesson Learned

"compact" does NOT mean "unreadable". 160px with 7-9px fonts is too small for Chinese text and makes nodes look blurry. The sweet spot for this user is 220px with 13px title / 11px body fonts. Only reduce further if user explicitly asks.
