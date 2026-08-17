# AI工作流平台技术实现参考

> 基于2026年6月对TapNow、Lovart、LiblibAI的深度技术分析
> 聚焦电商场景：GPT-Image-2 + Seedance 2

## 一、ComfyUI执行引擎核心逻辑（所有平台的底层参考）

### 执行流程
```
用户构建工作流 → 导出JSON → 提交到PromptQueue
                                    ↓
                            PromptExecutor 接收
                                    ↓
                            validate_prompt() 参数校验
                                    ↓
                            构建执行图（DAG有向无环图）
                                    ↓
                            深度优先遍历执行节点
                                    ↓
                            缓存机制（跳过重复计算）
                                    ↓
                            返回结果到前端
```

### 工作流JSON结构
```json
{
  "last_node_id": 10,
  "last_link_id": 15,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [100, 200],
      "widgets_values": ["image.png"],
      "inputs": [{"name": "image", "type": "IMAGE", "link": 5}],
      "outputs": [{"name": "IMAGE", "type": "IMAGE", "links": [5, 8]}]
    }
  ],
  "links": [
    [5, 1, 0, 3, 0, "IMAGE"]  // [link_id, from_node, from_slot, to_node, to_slot, type]
  ]
}
```

### ComfyUI源码结构
```
ComfyUI/
├── api_server/          # web服务端
├── comfy/               # 核心执行引擎
│   ├── execution.py     # DAG引擎、智能缓存（重点分析对象）
│   ├── model_management.py  # 显存/内存管理
│   └── samplers.py      # 采样算法
├── comfy_execution/     # 执行框架：DAG定义、缓存、合法性校验
├── custom_nodes/        # 第三方插件
└── web/                 # 前端（LiteGraph.js）
```

**关键设计点：**
- DAG依赖解析：自动分析节点依赖关系，确定执行顺序（拓扑排序）
- 智能缓存：相同输入的节点不重复计算
- 增量执行：只执行变化的节点及其下游
- 深度优先遍历 + 入度表

### API调用模式
```python
import json, urllib.request

# 加载工作流JSON → 修改参数（模板替换）→ 提交任务
data = json.dumps({"prompt": workflow}).encode('utf-8')
req = urllib.request.Request("http://localhost:8188/prompt", data=data,
    headers={"Content-Type": "application/json"})
response = json.loads(urllib.request.urlopen(req).read())
prompt_id = response["prompt_id"]
# WebSocket监听进度 → 获取结果图片
```

---

## 二、GPT-Image-2 API

**官方文档**: https://developers.openai.com/api/docs/guides/image-generation
**端点**: `/v1/images/generations` 和 `/v1/images/edits`

### 文生图
```python
from openai import OpenAI
import base64

client = OpenAI()
result = client.images.generate(
    model="gpt-image-2",
    prompt="一款精美的白色运动鞋，纯白背景，电商产品摄影风格，8K高清",
    size="1024x1024",       # 1024x1024, 1536x1024, 1024x1536
    quality="high",          # low, medium, high
    n=1,
    background="transparent" # 透明背景（电商抠图）
)
image_data = base64.b64decode(result.data[0].b64_json)
```

### 图生图（编辑）
```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("product.png", "rb"),
    prompt="将背景改为海边沙滩场景，保持产品不变",
    size="1024x1024"
)
```

### 电商适用场景
- ✅ 产品主图（高质量渲染，支持透明背景）
- ✅ 场景图（自动生成不同使用场景）
- ✅ 模特图（虚拟试穿/展示）
- ✅ 文字渲染（精准生成图片内文字，促销标签等）

### 限制
- 速率限制：取决于账户等级
- 成本：约$0.04-0.12/张（取决于quality）
- 延迟：2-10秒

---

## 三、Seedance 2 API（火山引擎方舟平台）

**平台**: https://www.volcengine.com/product/ark
**兼容OpenAI SDK**，只需修改base_url和api_key

### 文生视频
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-ark-api-key",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

response = client.video.generate(
    model="doubao-seedance-2-0-t2v",
    prompt="一款白色运动鞋在T台上旋转展示，专业电商视频",
    duration=5,
    resolution="1080p"
)
```

### 图生视频（电商重点）
```python
response = client.video.generate(
    model="doubao-seedance-2-0-i2v",
    image="product.png",
    prompt="产品缓慢旋转，光影变化，高端感",
    duration=5
)
```

### 异步任务处理
```python
task_id = response.id
import time
while True:
    result = client.video.retrieve(task_id)
    if result.status == "completed":
        video_url = result.video_url
        break
    elif result.status == "failed":
        raise Exception(result.error)
    time.sleep(5)
```

### 限制
- 异步任务：需轮询获取结果
- 延迟：30秒-3分钟/视频
- 成本：约¥0.5-2/秒视频
- 时长限制：通常5-10秒

---

## 四、工作流引擎实现模式

### 核心类设计
```python
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import asyncio

class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class WorkflowNode:
    id: str
    type: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    status: NodeStatus = NodeStatus.PENDING
    result: Any = None

class WorkflowEngine:
    """参考ComfyUI的DAG执行逻辑"""
    
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: List[tuple] = []
    
    def get_execution_order(self) -> List[str]:
        """拓扑排序获取执行顺序"""
        in_degree = {nid: 0 for nid in self.nodes}
        adjacency = {nid: [] for nid in self.nodes}
        for from_id, to_id, _, _ in self.edges:
            adjacency[from_id].append(to_id)
            in_degree[to_id] += 1
        
        queue = [nid for nid, d in in_degree.items() if d == 0]
        order = []
        while queue:
            nid = queue.pop(0)
            order.append(nid)
            for neighbor in adjacency[nid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return order
    
    async def execute(self, callback=None) -> dict:
        """按拓扑序执行节点"""
        execution_order = self.get_execution_order()
        results = {}
        for node_id in execution_order:
            node = self.nodes[node_id]
            input_data = self._collect_inputs(node_id, results)
            try:
                node.status = NodeStatus.RUNNING
                result = await self._execute_node(node, input_data)
                node.status = NodeStatus.COMPLETED
                results[node_id] = result
            except Exception as e:
                node.status = NodeStatus.FAILED
                raise
        return results
```

### 节点执行器工厂模式
```python
class NodeExecutorFactory:
    _executors = {}
    
    @classmethod
    def register(cls, node_type: str, executor_class):
        cls._executors[node_type] = executor_class
    
    @classmethod
    def get_executor(cls, node_type: str):
        return cls._executors[node_type]()

# 注册执行器
NodeExecutorFactory.register("gpt_image_generate", GPTImageExecutor)
NodeExecutorFactory.register("seedance_generate", SeedanceExecutor)
```

---

## 五、React Flow前端实现

### 技术栈
- React 18 + TypeScript
- React Flow 11（节点编辑器核心）
- Zustand（状态管理）
- Socket.io Client（WebSocket实时通信）
- Tailwind CSS

### 自定义节点模式
```tsx
// React Flow的节点就是普通React组件
const GPTImageNode = ({ data }) => {
  return (
    <div className="custom-node">
      <Handle type="target" position={Position.Top} />
      <div>GPT-Image-2</div>
      <input value={data.prompt} onChange={...} />
      <select value={data.size}>...</select>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};
```

### 工作流JSON导出
React Flow内置`toObject()`方法可导出节点和边的JSON，直接对应后端工作流格式。

---

## 六、电商工作流模板

### 模板1: 商品主图批量生成
```
输入(产品白底图+描述) → GPT-Image-2(多场景生成) → 自动抠图 → GPT-Image-2(换背景) → 批量裁剪 → 输出8-12张主图
```

### 模板2: 产品展示视频
```
输入(主图+角度描述) → GPT-Image-2(多角度图) → Seedance(图生视频旋转) → Seedance(场景视频) → 拼接 → 15秒视频
```

### 模板3: 模特穿搭展示
```
输入(服装图+风格) → GPT-Image-2(虚拟模特) → GPT-Image-2(多场景) → Seedance(走秀视频) → 输出图+视频
```

---

## 七、预算参考

### 开发成本（外包）
- 前端（React Flow + UI）：¥3-5万
- 后端（API + 任务引擎）：¥3-5万
- 测试+部署：¥1-2万
- **合计：¥7-12万**

### 月运营成本
- 云服务器：¥1,000-3,000
- OpenAI API：¥2,000-10,000
- 火山引擎API：¥1,000-5,000
- CDN/存储：¥500-1,000
- **合计：¥4,500-19,000/月**

### 核心优势（vs完整平台）
- 轻量：只用2个API，无需GPU集群
- 快速：2-3个月可上线MVP
- 成本可控：按调用付费
- 维护简单：不运维ComfyUI/模型服务
