# DAG Execution Engine Pattern

## Overview

TapNow-style DAG (Directed Acyclic Graph) execution engine for concurrent node execution.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     DAG Executor                        │
├─────────────────────────────────────────────────────────┤
│  1. Build dependency graph from nodes + edges           │
│  2. Topological sort → execution levels                 │
│  3. Execute each level concurrently (asyncio.gather)    │
│  4. Broadcast progress via WebSocket                    │
└─────────────────────────────────────────────────────────┘
```

## Backend Implementation

### DAG Engine (`backend/app/services/dag_engine.py`)

```python
class DAGExecutor:
    def __init__(self, nodes: List[Dict], edges: List[Dict]):
        self.nodes: Dict[str, DAGNode] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)
        
        # Build graph
        for edge in edges:
            source, target = edge["source"], edge["target"]
            self.adjacency[source].append(target)
            self.nodes[target].dependencies.add(source)
            self.in_degree[target] += 1
    
    def get_execution_levels(self) -> List[List[str]]:
        """Kahn's algorithm grouped by level for parallel execution"""
        in_degree = dict(self.in_degree)
        queue = [nid for nid in self.nodes if in_degree[nid] == 0]
        levels = []
        
        while queue:
            levels.append(queue[:])
            next_queue = []
            for nid in queue:
                for dep in self.adjacency[nid]:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        next_queue.append(dep)
            queue = next_queue
        
        return levels
    
    async def execute(self, executor_func, concurrency: int = 3):
        levels = self.get_execution_levels()
        results = {}
        
        for level in levels:
            # Parallel execution of independent nodes
            tasks = [self.execute_node(nid, executor_func) for nid in level]
            level_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for nid, result in zip(level, level_results):
                if isinstance(result, Exception):
                    results[nid] = {"status": "error", "error": str(result)}
                else:
                    results[nid] = {"status": "success", "result": result}
        
        return results
```

### WebSocket Progress (`backend/app/api/ws.py`)

```python
_workflow_connections: dict[str, set[WebSocket]] = {}

async def broadcast_workflow_progress(workflow_id: str, message: dict):
    connections = _workflow_connections.get(workflow_id, set())
    for ws in connections:
        try:
            await ws.send_json(message)
        except:
            connections.discard(ws)

@router.websocket("/ws/workflow/{workflow_id}")
async def ws_workflow(websocket: WebSocket, workflow_id: str):
    await websocket.accept()
    _workflow_connections.setdefault(workflow_id, set()).add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        _workflow_connections.get(workflow_id, set()).discard(websocket)
```

## Frontend Implementation

### useWorkflowExecution Hook

```typescript
export function useWorkflowExecution() {
  const wsRef = useRef<WebSocket | null>(null);
  
  const connectWebSocket = useCallback((workflowId: string) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/workflow/${workflowId}`);
    wsRef.current = ws;
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case "node_progress":
          updateNodeData(data.node_id, { 
            status: data.status, 
            progress: data.progress 
          });
          break;
        case "workflow_complete":
          // Update all nodes with results
          break;
      }
    };
  }, []);
  
  const executeWorkflow = useCallback(async (options) => {
    const resp = await fetch("http://localhost:8000/api/workflow/execute", {
      method: "POST",
      body: JSON.stringify({ nodes, edges, concurrency: 3 })
    });
    const result = await resp.json();
    if (result.workflow_id) {
      connectWebSocket(result.workflow_id);
    }
  }, [nodes, edges]);
}
```

## Key Design Decisions

1. **Topology sort for execution order** - Ensures dependencies are met
2. **Level-based concurrency** - Nodes at same level run in parallel
3. **WebSocket for progress** - Real-time updates without polling
4. **Error isolation** - One node failure doesn't crash entire workflow

## Comparison with TapNow

| Feature | TapNow | Antoken |
|---------|--------|---------|
| Execution | DAG concurrent | DAG concurrent ✓ |
| Progress | WebSocket | WebSocket ✓ |
| Max concurrency | Configurable | 3 (default) |
| Error handling | Per-node | Per-node ✓ |
