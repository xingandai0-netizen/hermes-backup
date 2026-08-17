# v1 → v2 代码迁移模式

## 背景
当现有项目代码质量差、架构混乱时，选择新建仓库而非修补。
但UI代码如果已经稳定可用，应该直接复制而非重新实现。

## 核心原则
**用户说"用v1的UI" = 复制v1的代码，一模一样**
不是"风格相似"，不是"参考设计"，是直接 `cp` 文件。

## 迁移步骤

### 1. 复制组件文件
```bash
cp v1/src/components/nodes/*.tsx v2/src/components/nodes/
cp v1/src/components/sidebar/*.tsx v2/src/components/canvas/
cp v1/src/components/*.tsx v2/src/components/
```

### 2. 创建兼容层
v1可能用Zustand，v2用Jotai。需要创建兼容的stores：

```typescript
// stores/v1-compat.ts
export { useWorkflowStore } from "./workflow-store-zustand";
export { useSettingsStore } from "./settings-store";
```

### 3. 创建v1类型定义
```typescript
// types/workflow-v1.ts
export type NodeFlowType = "TEXT" | "IMAGE" | "VIDEO" | "COMPOSITE";
export interface NodeData extends Record<string, unknown> { ... }
```

### 4. 批量替换导入路径
| v1路径 | v2路径 |
|--------|--------|
| `@/stores/workflowStore` | `@/stores/v1-compat` |
| `@/stores/settingsStore` | `@/stores/v1-compat` |
| `@/types/workflow` | `@/types/workflow-v1` |
| `@/lib/api` | `@/lib/api-base` |
| `@/lib/assetUpload` | `@/lib/asset-upload` |
| `@/lib/mediaProxy` | `@/lib/media-proxy` |
| `@/lib/constants` | `@/lib/constants-v1` |
| `./BaseNode` | `./base-node` |
| `@/components/PreviewModal` | `@/components/preview-modal` |

### 5. 处理ESLint错误
v1代码可能有`any`类型，需要添加：
```typescript
/* eslint-disable @typescript-eslint/no-explicit-any */
```

### 6. 验证
```bash
npm run build  # 必须通过
npm test       # 必须通过
```

## 常见陷阱
1. **v1用Zustand，v2用Jotai** → 创建Zustand兼容层，不要改v1代码
2. **v1的settingsStore是对象结构**（videoApi.apiUrl），不是字符串
3. **v1的workflowStore有undo/redo**，需要在Zustand store中实现
4. **文件名大小写不同**（BaseNode vs base-node）→ 统一小写

## 何时使用此模式
- 用户明确说"用v1的UI/代码"
- 现有代码已稳定可用
- 新项目架构不同（Jotai vs Zustand等）
