# Multi-Material Composition Pattern

## Core Concept

Composition nodes combine multiple upstream素材 using AI. The node itself does NOT do the composition — it sends素材 URLs + user prompt to an AI model that does the work.

## Architecture

```
素材A (IMAGE) ──┐
                 ├──→ Composition Node ──→ AI API ──→ Result
素材B (VIDEO) ──┘
```

## Key Differences from Generation Nodes

| Aspect | Generation Node | Composition Node |
|--------|----------------|------------------|
| Input | TEXT prompt only | Multiple IMAGE/VIDEO + prompt |
| Model | Single provider | May use different model per material type |
| API call | `{prompt, model}` | `{prompt, model, reference_urls: [...]}` |
| Purpose | Create new content | Transform/combine existing content |

## Backend Pattern

```python
# Collect reference URLs and embed in prompt
def build_composite_prompt(prompt: str, reference_urls: List[str]) -> str:
    if not reference_urls:
        return prompt
    refs = "\n".join([f"素材{i+1}: {url}" for i, url in enumerate(reference_urls)])
    return f"""{prompt}\n\n参考素材：\n{refs}\n\n请根据以上素材和要求，完成合成任务。"""
```

## Frontend Pattern

```tsx
function CompositionNode({ id, data, selected }: NodeProps<NodeData>) {
  const { nodes, edges } = useWorkflowStore();
  
  // Collect ALL upstream素材 URLs
  const incomingEdges = edges.filter(e => e.target === id);
  const referenceUrls: string[] = [];
  
  for (const edge of incomingEdges) {
    const sourceNode = nodes.find(n => n.id === edge.source);
    const sourceConfig = sourceNode?.data?.config as Record<string, unknown>;
    const url = sourceConfig?.resultUrl as string;
    if (url) referenceUrls.push(url);
  }
  
  // Model selection + prompt + generate button
  // Send: { prompt, model, reference_urls: referenceUrls }
}
```

## UI Requirements

Every composition node MUST have:
1. Model selection dropdown (user chooses which AI model to use)
2. Prompt textarea (user describes how to combine素材)
3. Generate/compose button with progress
4. Output preview + download
5.素材 preview thumbnails (show what's being combined)

## Content Moderation Pitfall

Some APIs reject "modification" prompts as copyright violations. Rephrase:
- Bad: "将视频中女生手中放上图片中的笔" (modify existing)
- Good: "生成一个女生手中拿着笔在海边走路的视频" (generate new)
