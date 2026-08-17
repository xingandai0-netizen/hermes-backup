---
name: antoken-deepseek-review-workflow
description: DeepSeek代码审查工作流 - 分模块发送→收集反馈→逐项修复→重新验证
version: 3.0
tags: [deepseek, code-review, workflow, antoken, tdd, bdd, iterative]
---

# DeepSeek 代码审查工作流 v3

## 触发条件
- 完成一组重构任务后
- 阿戴说"给DeepSeek检查一下"
- 重大架构变更后

## 核心原则

### ⚠️ 绝对不能声称"已完成"但实际没改！
阿戴多次发现我说"已修复"但代码没变。这是最严重的信任问题。

**必须遵守的验证流程**：
1. 执行 patch/write_file 后，立即用 search_files 验证修改生效
2. 运行 npm run build 确认无构建错误
3. 运行 npm test 确认测试通过
4. 只有验证通过后才能说"已完成"

### ⚠️ 必须严格按要求修改，不能自作主张
- 用户说改 A 就改 A，不要改 B
- 遇到技术限制要说明，不要用替代方案
- 修改后必须验证

## 工作流程

### 0. ⚠️ 确认正确的项目目录（最高优先级）
**必须先确认读的是线上版本仓库，不是备份仓库！**
```bash
# 检查remote指向哪个GitHub仓库
cd /Users/macpro/antoken-v2 && git remote -v
# 必须是 antoken.git（线上版本），不是 antoken1.git（v1备份）

# 确认Jotai迁移状态
cat frontend/package.json | grep -E "zustand|jotai"
# 应该只有 jotai，没有 zustand
```
**教训（2026-07-04）**：曾误读v1备份仓库生成全部模块，阿戴发现代码还在用Zustand。v1备份仓库(/Users/macpro/antoken)已锁死不用。

### 1. 准备代码（分模块）
不要一次发送全部代码。按功能模块拆分，**单个模块不超80KB**：
```
模块1: 状态管理 (stores/) - ~18KB
模块2: Hooks (hooks/) - ~21KB
模块3: 节点组件 (components/nodes/) - ~93KB
模块4: Canvas/UI (components/canvas/) - ~97KB
模块5: 后端 (backend/) - ~42KB
模块6: 拆分为子模块（见下方）
```

**模块6超大时的拆分模式**（按功能拆为6a/6b/6c...，每块不超80KB）：
```
6a: 账号系统+核心工具库 (contexts/ + lib核心) - ~23KB
6b: 电商功能+商业化 (templates/batch/pricing/stripe) - ~32KB
6c: Types+样式+路由页面 (types/styles/pages) - ~80KB
6d: Landing Page (components/landing/) - ~24KB
6e: UI组件+配置+Sentry (ui/sentry/config) - ~50KB
```

### 2. 生成模块文件
**⚠️ 用 terminal+shell cat 生成，不要用 execute_code！** execute_code 有50 tool call限制，读70+文件会超限→静默失败（不报错，生成的文件为空或不完整）。
```bash
cd /Users/macpro/antoken-v2
{
echo "=== 模块标题 ==="
echo "描述"
for f in file1 file2 ...; do
  echo "--- FILE: $f ---"
  cat "$f" 2>/dev/null || echo "[NOT FOUND]"
  echo ""
done
} > /tmp/antoken-module{N}-{name}.txt
wc -c /tmp/antoken-module{N}-{name}.txt  # 验证非空
```

### 3. 发送方式
```bash
cat /tmp/antoken-module1-state.txt | pbcopy
# 粘贴给 DeepSeek
```

### 4. 收到反馈后
- 逐项分析 DeepSeek 的评价
- 区分：✅已完成 / ❌未完成 / ⚠️部分完成
- 按优先级修复（P0→P1→P2→P3）
- 每个修复走 TDD/BDD

### 5. 修复后重新提交
- 修复完成后重新生成模块文件
- 再次发送给 DeepSeek 验证
- DeepSeek 确认后才能声称"完成"

## 关键教训（2026-07-05）

### 1. 代码优先验证模式
阿戴要求每次修改后先提供代码，再由 DeepSeek 验证。

**正确流程**：
```
1. 收到 DeepSeek 反馈
2. 执行修改
3. 验证构建和测试
4. 生成最新模块文件
5. 提供给阿戴（"改完的代码给你"）
6. 阿戴发送给 DeepSeek 验证
7. DeepSeek 确认后才能声称"完成"
```

**反模式**：
- ❌ 修改后直接推进下一个模块
- ❌ 声称"已修复"但没有提供代码
- ❌ 跳过 DeepSeek 验证步骤

### 2. 模块文件命名规范
```
/tmp/antoken-module{N}-{name}.txt
例如：
/tmp/antoken-module1-state.txt
/tmp/antoken-module2-hooks.txt
/tmp/antoken-module3-nodes.txt
/tmp/antoken-module4-canvas.txt
/tmp/antoken-module5-backend.txt
/tmp/antoken-module6-account.txt
```

### 3. 迭代审查模式
DeepSeek 审查是迭代的，每轮可能发现新问题：
- 第1轮：发现 12 个问题
- 第2轮：修复后重新审查，发现 3 个残留
- 第3轮：修复后重新审查，发现 1 个遗漏
- 第4轮：全部通过

**不能跳过迭代**：必须等 DeepSeek 确认后才能进入下一个模块。

## React Flow 类型限制

**问题**：React Flow 的 `NodeProps` 类型不直接接受 `NodeData` 作为泛型参数。

**正确做法**：
```tsx
// ✅ 使用 NodeProps + 类型断言
interface BaseNodeProps extends NodeProps { ... }
function BaseNodeComponent({ data, selected, children, className }: BaseNodeProps) {
  const d = data as NodeData;
  // ...
}
```

**原因**：React Flow 的 `NodeProps` 期望一个 `Node` 类型，不是 `NodeData`。当前版本的类型定义不支持直接泛型。

## Python 文件修改陷阱

**问题**：Python 文件的 patch 可能静默失败，特别是当字符串包含特殊字符（引号、花括号）时。

**正确做法**：
```bash
# 修改后必须验证
grep -n "raise ValueError\|logger.warning" app/config.py
# 确认输出中只有 raise ValueError，没有 logger.warning
```

## DeepSeek 常见发现的模式
1. **cfg 闭包问题** — useCallback 依赖过时的闭包
2. **全局状态订阅** — useAtomValue(nodesAtom) 导致全量重渲染
3. **字段路径不统一** — data.assetUrl vs data.config.assetUrl
4. **废弃依赖未清理** — zustand 仍在 package.json
5. **类型安全** — any 类型、弱类型参数
6. **异常细节泄露** — detail=str(e) 暴露内部信息
7. **配置缺失不阻止启动** — logger.warning 应改为 raise ValueError
8. **SSRF 防护缺失** — 代理端点未阻止内网地址
9. **积分配额硬编码** — 应根据订阅计划动态获取
10. **Stripe webhook 未处理** — 只 print 不更新数据库

## toapis.com API 模式（2026-07-05）

### 文本生成
**关键发现**：文本生成使用 `messages` 格式，不是 `prompt`。

```python
# ❌ 错误
body = {"prompt": "写一段产品描述", "model": "gemini-3.5-flash"}

# ✅ 正确
body = {
    "messages": [{"role": "user", "content": "写一段产品描述"}],
    "model": "gemini-3.5-flash"
}
```

### 图片/视频生成
```python
# 图片生成
body = {"prompt": "...", "model": "gemini-3-pro-image-preview-official", "size": "1:1"}

# 视频生成
body = {"prompt": "...", "model": "seedance-2", "duration": 5}
```

### 任务状态查询
- 图片任务：`GET /v1/images/generations/{task_id}`
- 视频任务：`GET /v1/videos/generations/{task_id}`
- 文本任务：直接返回结果，无 task_id

## 图片预览优化模式（2026-07-05）

### 问题
AI 生成的 2K/4K 图片（2-5MB）直接在 320px 预览框中显示，导致"从上到下慢慢加载"。

### 解决方案
后端代理增加图片缩放能力，前端请求时传入预览尺寸。

**前端**：
```typescript
export function proxyUrl(url: string, width?: number, height?: number): string {
  const base = `${getApiBase()}/api/generate/proxy?url=${encodeURIComponent(url)}`;
  if (width && height) {
    return `${base}&width=${width}&height=${height}`;
  }
  return base;
}

// 使用
<img src={proxyUrl(previewUrl, 320, previewHeight)} />
```

**后端**（Pillow 缩放 + 本地缓存）：
```python
@router.get("/generate/proxy")
async def proxy_media(url: str, width: int = None, height: int = None):
    # ... 获取原图 ...
    if width and height and content_type.startswith("image/"):
        cache_key = hashlib.md5(f"{url}_{width}_{height}".encode()).hexdigest()
        # 缩放并缓存
```

## 多参考架构模式（2026-07-05）

### 问题
上游素材被简单收集为 URL 列表，没有角色区分（风格/主体/构图），AI 无法理解参考意图。

### 解决方案
```typescript
// types/workflow-v1.ts
export type ReferenceRole = 'style' | 'subject' | 'composition' | 'content';

// hooks/use-upstream-data.ts
export interface UpstreamNode {
  node: Node<NodeData>;
  edge: Edge;
  assetName: string;
  assetType?: string;
  assetUrl?: string;
  role: ReferenceRole; // 从 edge.targetHandle 获取
}
```

## 参数透传规则（2026-07-05）

**核心原则**：用户设置的每个参数都必须 100% 传递到 AI API，中间不得截断。

### 常见断裂点
1. **字段名不匹配**：前端 `ratio` vs 后端 `aspect_ratio`
2. **Schema 缺失字段**：前端发送 `video_mode`，后端未定义
3. **参数位置错误**：`resolution` 包装在 `metadata` 中
4. **参考数据丢失**：`reference_images` 未在 Schema 中定义

## 后端安全模式（2026-07-05）

### 全局异常处理器 + 配置校验 + SSRF 防护 + 积分动态配额

详细代码见 `references/backend-security-patterns.md`。

## JSX大块替换的tail/head拆分陷阱（2026-07-04）

**问题**：用 `head -N` + `tail -N` 拆分文件保留首尾、中间替换为新代码时，`tail` 的行号选错会截断JSX块，导致语法错误。

**案例**：video-node.tsx 中 showControls 块在行413-821，showPreview在行822。用 `tail -6`（从末尾取6行），结果 `{showPreview && previewUrl && (` 这一行被截断，只剩 `<PreviewModal .../>` + `)}`，导致 `Unexpected token` 错误。

**正确做法**：
1. **精确找到块结束行** — 用 `grep -n "showPreview\|showControls" file.tsx` 确定行号
2. **tail 从正确行号开始** — `tail -n +822 file.tsx` 而不是 `tail -6 file.tsx`
3. **合并后立即验证** — `grep -c "showPreview" file.tsx` 确认关键字段完整
4. **构建验证** — `npm run build` 必须通过才能继续

**反模式**：
```bash
# ❌ tail -6 从末尾取，不确定取到哪行
tail -6 file.tsx > after.tsx

# ✅ tail -n +N 从指定行开始，精确可控
tail -n +822 file.tsx > after.tsx
```

## sed追加合并行陷阱（2026-07-04）

**问题**：`sed -i '' '/pattern/a\` 追加多行时，如果上一行没有正确换行，追加内容会和已有行合并到同一行。

**案例**：`sed -i '' '/background: "#000",/a\ backdropFilter...'` 把 backdropFilter 和 border 合并到同一行：
```
WebkitBackdropFilter: "saturate(180%) blur(30px)",            border: "none",
```

**修复**：追加后用 `sed -i '' 's/pattern/replacement/'` 分开合并行。或者直接用 patch 工具代替 sed。

## React Flow 节点UI修改模式（2026-07-04）

详见 `references/react-flow-node-ui-patterns.md`。核心要点：
- **JSX大块替换**：用 `head -N` + `tail -n +M` 精确拆分，不用 `tail -N`。**必须验证after文件非空**。
- **状态变量添加**：用 `patch` 工具，不用 `sed -i ''`（sed会创建重复行）
- **缩放自适应**：`useReactFlow` + `transform: scale(1/zoom)`
- **弹窗遮罩关闭**：`position: fixed; inset: 0` 透明遮罩
- **TapNow风格（截图验证）**：按钮填充#2a2a2a（非透明）、圆角4px（非8-20px）、间距6px无分隔线、面板solid #1c1c1e吸附预览区底部、输入框透明无背景、模型图标三条粗线、发送按钮圆形30px无数字

## 验证清单

每次修改后必须执行：
```bash
# 1. 确认修改生效
search_files("old_code_pattern")  # 确认旧代码已移除
search_files("new_code_pattern")  # 确认新代码已添加

# 2. 构建验证
npm run build 2>&1 | tail -5  # 确认构建成功

# 3. 测试验证
npm test 2>&1 | tail -10  # 确认测试通过

# 4. 部署验证
npx vercel --prod --yes --force 2>&1 | tail -5  # 确认部署成功

# 5. 生成最新模块文件
# 重新生成 /tmp/antoken-module{N}-{name}.txt
```
