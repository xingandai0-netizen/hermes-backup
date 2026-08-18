# DeepSeek 代码审查工作流

## 模式描述
将代码分模块发送给 DeepSeek（Claude Desktop）审查，然后根据反馈逐个修复。这是阿戴的标准代码审查流程。

## 工作流程

### Step 1: 分模块
将代码按功能分为 6 个模块：
- 模块1：状态管理（workflow-store-jotai.ts, settings-store-*.ts）
- 模块2：Hooks（use-upstream-data.ts, use-poll-public-url.ts, use-asset-upload.ts）
- 模块3：节点组件（base-node.tsx, image-node.tsx, video-node.tsx, text-node.tsx, composite-node.tsx）
- 模块4：Canvas和UI（persistent-canvas.tsx, node-sidebar.tsx, error-boundary.tsx）
- 模块5：后端（main.py, config.py, database.py, api/*.py, services/*.py）
- 模块6：账号系统（auth-context.tsx, route.ts, supabase.ts, asset-management.ts）

### Step 2: 生成文件
```python
from hermes_tools import terminal

files = ["file1.tsx", "file2.tsx", ...]
output = "# 模块N：名称\n\n## 本轮改动\n- 改动1\n- 改动2\n\n"

for f in files:
    result = terminal(f"cat {f}")
    content = result.get("output", "")
    filename = f.split("/")[-1]
    output += f"\n## {filename}\n```tsx\n{content}\n```\n"

with open("/tmp/antoken-moduleN.txt", "w") as f:
    f.write(output)
```

### Step 3: 用户操作
用户执行 `cat /tmp/antoken-moduleN.txt | pbcopy` 然后粘贴给 DeepSeek。

### Step 4: DeepSeek 返回审查报告
包含：问题列表、严重程度、修复建议、代码片段。

### Step 5: 逐个修复
按 TDD/BDD 流程逐个修复：
1. 写 BDD 场景
2. 写 failing test
3. 实现代码
4. 运行测试
5. 构建验证

### Step 6: 验证修复
```bash
npm run build 2>&1 | tail -5
npm test 2>&1 | tail -5
npx vercel --prod --yes --force 2>&1 | tail -3
```

### Step 7: 再次发送给 DeepSeek
修复后再次发送代码给 DeepSeek 确认。

## 关键原则
- **不要声称"已完成"除非真正验证过** — DeepSeek 每次都能发现未落实的修改
- **每个修复都要走 TDD/BDD 流程** — 不要跳过测试
- **修复后要再次发送给 DeepSeek 确认** — 形成闭环
- **"先发我再检查"** — 阿戴要求先提供代码，让他发给 DeepSeek 确认后再继续

## 文件命名规范
- `/tmp/antoken-module{N}-{name}.txt` — 模块代码
- `/tmp/antoken-final-v{N}-module{N}.txt` — 修复后代码（带版本号）
- `/tmp/antoken-module{N}-final.txt` — 最终版本

## 常见问题
1. **文件太大** — 一个模块可能 80-90KB，需要分批发送
2. **代码过时** — 修复后需要重新生成文件
3. **DeepSeek 反馈需要多轮** — 一个模块可能需要 2-3 轮修复
