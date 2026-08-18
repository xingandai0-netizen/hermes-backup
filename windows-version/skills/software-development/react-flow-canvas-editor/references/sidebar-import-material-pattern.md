# 侧边栏导入素材模式

## 概述
左侧CircleNavPanel菜单底部添加"导入素材"选项，功能与右键菜单的"导入素材"一致。

## 实现步骤

### 1. 添加imports和state
```tsx
import React, { useState, useCallback, useRef } from "react";
import { getApiBase } from "@/lib/api";

// 在组件内
const [importingType, setImportingType] = useState<'IMAGE' | 'VIDEO' | null>(null);
const fileInputRef = useRef<HTMLInputElement>(null);
```

### 2. 添加upload和import函数
```tsx
// 上传文件到后端
const uploadToBackend = useCallback(async (file: File): Promise<string | null> => {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const resp = await fetch(`${getApiBase()}/api/upload`, { method: "POST", body: formData });
    if (!resp.ok) return null;
    const data = await resp.json();
    return `${getApiBase()}${data.path}`;
  } catch { return null; }
}, []);

// 导入素材（打开文件选择器）
const handleImport = useCallback((assetType: 'IMAGE' | 'VIDEO') => {
  setImportingType(assetType);
  setShowMenu(false); // 关闭菜单
  if (fileInputRef.current) {
    fileInputRef.current.accept = assetType === 'IMAGE' ? 'image/*' : 'video/*';
    fileInputRef.current.click();
  }
}, []);

// 处理文件选择（获取尺寸 → 上传 → 创建节点）
const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file || !importingType) return;
  // 获取原始尺寸（图片用Image，视频用video元素）
  // 上传到后端
  // 创建节点（包含isLocalAsset: true）
  // 重置input和importingType
}, [importingType, uploadToBackend, addNode, viewport]);
```

### 3. UI菜单项
在NODE_DEFINITIONS.map之后添加分隔线和导入素材按钮：
```tsx
{/* 分隔线 */}
<div style={{ height: 1, background: "rgba(255,255,255,0.06)", margin: "6px 0" }} />
{/* 导入素材 */}
<div onClick={() => handleImport('IMAGE')} style={{...}}>
  {/* 紫色上传图标 + "导入素材" + "选择本地图片或视频文件" */}
</div>
```

### 4. 隐藏的文件输入
在Logo区域前添加：
```tsx
<input ref={fileInputRef} type="file" style={{ display: 'none' }} onChange={handleFileSelect} />
```

## 注意事项
- 导入的素材需要设置 `isLocalAsset: true` 和 `objectFit: contain`
- 必须上传到后端获取backend URL（blob URL对后端不可访问）
- 导入图片时用 `Image.onload` 获取原始尺寸
- 导入视频时用 `video.onloadedmetadata` 获取尺寸和时长
