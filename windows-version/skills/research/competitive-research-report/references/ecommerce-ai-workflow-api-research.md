# 电商AI工作流平台 - API深度研究参考

> 来源：2026-06-07 session，基于OpenAI官方文档、火山引擎方舟平台、ComfyUI源码分析

## GPT-Image-2 (gpt-image-1) API要点

### 端点
| 端点 | 方法 | 用途 |
|------|------|------|
| `/v1/images/generations` | POST | 文生图 |
| `/v1/images/edits` | POST | 图生图编辑 |

### 关键参数
- `model`: "gpt-image-1"（当前官方模型名）
- `size`: 1024x1024 / 1536x1024 / 1024x1536 / auto
- `quality`: low / medium / high / auto
- `background`: transparent / opaque / auto（transparent输出必须png/webp）
- `output_format`: png / jpeg / webp
- `n`: 仅支持1（gpt-image-1限制，批量需循环调用）

### 电商关键用法
```python
# 透明背景（电商抠图）
result = client.images.generate(
    model="gpt-image-1",
    prompt="产品描述",
    background="transparent",
    output_format="png"
)

# 图生图编辑（保持产品一致性）
result = client.images.edit(
    model="gpt-image-1",
    image=open("product.png", "rb"),
    prompt="将背景改为海边场景"
)
```

### 踩坑
- n=1 only，批量需并发调用或循环
- URL有有效期，建议b64_json格式或立即下载
- 不同批次颜色可能不一致，用图生图编辑保持一致性
- high质量约$0.12/张，low约$0.04/张

---

## Seedance 2 API要点

### 平台
火山引擎方舟平台 (Volcengine Ark)

### 模型ID
| 模型 | ID |
|------|-----|
| 标准版 | `doubao-seedance-2-0-260128` |
| 快速版 | `doubao-seedance-2-0-fast-260128` |

### SDK安装
```bash
pip install 'volcengine-python-sdk[ark]'
```

### 调用模式
```python
from volcenginesdkarkruntime import Ark
client = Ark(api_key=os.environ.get("ARK_API_KEY"))

# 创建任务（异步）
resp = client.content_generation.tasks.create(
    model="doubao-seedance-2-0-260128",
    content=[{"type": "text", "text": prompt}],
    duration="5",        # 5/10/15秒
    resolution="720p",   # 480p/720p/1080p
    aspect_ratio="16:9"
)

# 轮询结果
result = client.content_generation.tasks.get(task_id=resp.task_id)
# status: pending → processing → succeeded/failed
```

### 图生视频
```python
resp = client.content_generation.tasks.create(
    model="doubao-seedance-2-0-260128",
    content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
    ],
    duration="5"
)
```

### 定价
- 约$0.10-0.25/秒
- 1080p比720p贵约1.4倍

### 踩坑
- 异步任务需轮询，建议设置5分钟超时 + 指数退避
- 视频质量可能不稳定，用参考图模式提高一致性
- API限流需实现请求队列

---

## ComfyUI执行引擎核心逻辑

### 执行流程
```
用户构建工作流 → 导出JSON → PromptQueue
    → PromptExecutor接收
    → validate_prompt() 参数校验
    → ExecutionGraph构建DAG
    → Kahn算法拓扑排序
    → 逐节点执行（同步）
    → 缓存检查（CacheKeySetInputSignature递归哈希上游链）
    → WebSocket推送结果
```

### 核心类
- `PromptExecutor`: 执行引擎入口
- `ExecutionGraph`: DAG图结构（adjacency list + in-degree table）
- `HierarchicalCache`: 4种缓存模式（Classic/LRU/RAM Pressure/Null）
- `DynamicPrompt`: 运行时动态修改图结构

### 关键设计
1. **缓存最精妙**: CacheKeySetInputSignature递归哈希整个上游依赖链，换prompt不重载模型
2. **执行是同步的**: GPU操作串行性和显存管理约束决定
3. **执行线程独立**: 不阻塞HTTP/WebSocket，通过队列解耦
4. **DynamicPrompt**: 支持循环/条件分支等高级功能

### API格式JSON结构
```json
{
  "nodes": [{"id": 1, "type": "LoadImage", "pos": [100,200], ...}],
  "links": [[link_id, from_node, from_slot, to_node, to_slot, type]]
}
```

---

## React Flow关键经验

### 必须遵守
- `nodeTypes`定义在组件外，否则每次渲染重建 = 性能灾难
- 自定义节点必须`memo()`包裹
- 连接验证必须实现BFS环形检测

### v12推荐模式
```tsx
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
// 受控模式（Controlled Mode）
```

### 性能优化
- `onlyRenderVisibleElements` 只渲染可视区域
- `nodeTypes`组件外定义 + `memo`
- `useCallback`包装事件处理
- dagre自动布局
