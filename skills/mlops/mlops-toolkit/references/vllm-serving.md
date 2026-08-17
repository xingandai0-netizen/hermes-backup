# vLLM — High-Performance LLM Serving

Production LLM serving with PagedAttention, continuous batching, and OpenAI-compatible API.

## When to use
- Deploying production LLM APIs (100+ req/sec)
- Serving OpenAI-compatible endpoints
- Limited GPU memory but need large models
- Multi-user applications

## Install

```bash
pip install vllm
```

## Basic offline inference

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")
sampling = SamplingParams(temperature=0.7, max_tokens=256)
outputs = llm.generate(["Explain quantum computing"], sampling)
print(outputs[0].outputs[0].text)
```

## OpenAI-compatible server

```bash
vllm serve meta-llama/Llama-3-8B-Instruct

# Query with OpenAI SDK
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')
print(client.chat.completions.create(
    model='meta-llama/Llama-3-8B-Instruct',
    messages=[{'role': 'user', 'content': 'Hello!'}]
).choices[0].message.content)
```

## Production deployment

```bash
# 7B-13B on single GPU
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --port 8000

# 30B-70B with tensor parallelism
vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9 \
  --quantization awq \
  --port 8000

# With caching and metrics
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching \
  --enable-metrics \
  --metrics-port 9090
```

## Docker deployment

```bash
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching
```

## Quantization

- **AWQ**: Best for 70B models, minimal accuracy loss
- **GPTQ**: Wide model support, good compression
- **FP8**: Fastest on H100 GPUs

```bash
vllm serve TheBloke/Llama-2-70B-AWQ --quantization awq
```

## Key metrics

- TTFT (time to first token) < 500ms
- Throughput > target req/sec
- GPU utilization > 80%
- `vllm:time_to_first_token_seconds`, `vllm:num_requests_running`, `vllm:gpu_cache_usage_perc`

## Common issues

| Issue | Fix |
|-------|-----|
| OOM during loading | Reduce `--gpu-memory-utilization`, `--max-model-len`, or use quantization |
| Slow first token | Enable `--enable-prefix-caching` |
| Low throughput | Increase `--max-num-seqs 512`, check GPU util with nvidia-smi |
| Inference slow | Use power of 2 GPUs for tensor parallelism |

## Hardware requirements

- 7B-13B: 1x A10 (24GB) or A100 (40GB)
- 30B-40B: 2x A100 (40GB) with tensor parallelism
- 70B+: 4x A100 (40GB) or 2x A100 (80GB), use AWQ/GPTQ

## Resources
- Docs: https://docs.vllm.ai
- GitHub: https://github.com/vllm-project/vllm
