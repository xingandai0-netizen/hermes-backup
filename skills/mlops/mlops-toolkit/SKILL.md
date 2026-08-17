---
name: mlops-toolkit
description: "MLOps toolkit: LLM inference, serving, evaluation, experiment tracking, and HuggingFace Hub operations."
version: 1.0.0
author: Curator (consolidated)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [MLOps, LLM, Inference, Serving, Evaluation, Experiment Tracking, HuggingFace, vLLM, llama.cpp, W&B, GGUF]
---

# MLOps Toolkit

Class-level skill for ML model operations: running models locally, serving them in production, evaluating quality, tracking experiments, and managing assets on HuggingFace Hub.

## When to use

Use this skill when you need to:
- Run LLMs locally (CPU, GPU, Apple Silicon)
- Serve LLMs as production APIs
- Benchmark models on academic evaluations
- Track ML experiments with metrics dashboards
- Search, download, or upload models/datasets on HuggingFace

## Quick decision matrix

| Task | Tool | Reference |
|------|------|-----------|
| Local inference (CPU/edge) | llama.cpp | [references/llama-cpp.md](references/llama-cpp.md) |
| Production LLM API serving | vLLM | [references/vllm-serving.md](references/vllm-serving.md) |
| Benchmark models (MMLU, GSM8K, etc.) | lm-eval-harness | [references/lm-evaluation-harness.md](references/lm-evaluation-harness.md) |
| Track experiments, sweeps, model registry | Weights & Biases | [references/weights-and-biases.md](references/weights-and-biases.md) |
| Search/download/upload on HF Hub | hf CLI | [references/huggingface-hub.md](references/huggingface-hub.md) |

## Architecture overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HuggingFace Hub                            │
│         (models, datasets, Spaces, endpoints)                │
└──────────┬──────────────────────────────┬───────────────────┘
           │                              │
    ┌──────▼──────┐               ┌───────▼───────┐
    │  llama.cpp  │               │     vLLM      │
    │  (local/    │               │  (production  │
    │   edge)     │               │   serving)    │
    └──────┬──────┘               └───────┬───────┘
           │                              │
    ┌──────▼──────────────────────────────▼───────┐
    │           lm-eval-harness                    │
    │         (quality benchmarking)               │
    └──────────────────┬──────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────┐
    │         Weights & Biases                     │
    │    (tracking, sweeps, model registry)        │
    └─────────────────────────────────────────────┘
```

## Inference: Local vs Production

**llama.cpp** — Local/edge inference:
- CPU, Apple Silicon, CUDA, ROCm, Intel GPUs
- GGUF quantized models (Q4_K_M, Q5_K_M, etc.)
- Single-user, low-latency
- OpenAI-compatible server mode available

**vLLM** — Production serving:
- PagedAttention for 24x throughput over standard transformers
- Continuous batching for multi-user scenarios
- OpenAI-compatible API endpoints
- Tensor parallelism for large models (70B+)
- Quantization support (AWQ, GPTQ, FP8)

**Rule of thumb**: llama.cpp for dev/edge/single-user, vLLM for production/multi-user.

## Evaluation workflow

1. Choose benchmarks (MMLU, GSM8K, HumanEval, etc.)
2. Run lm-eval-harness with appropriate backend (HF, vLLM, API)
3. Log results to W&B for tracking and comparison
4. Use W&B sweeps for hyperparameter optimization

## Common pitfalls

- **GGUF quant selection**: Start with Q4_K_M for general chat, Q5_K_M/Q6_K for code. Use HF's `?local-app=llama.cpp` page for repo-specific recommendations.
- **vLLM OOM**: Reduce `--gpu-memory-utilization`, `--max-model-len`, or use quantization.
- **lm-eval speed**: Use vLLM backend for 5-10x faster evaluation. Use 0-shot for quick checks.
- **W&B offline**: Set `WANDB_MODE=offline` for unstable connections, sync later with `wandb sync`.
- **HF CLI**: The `hf` command replaces deprecated `huggingface-cli`.

## References

- [llama-cpp.md](references/llama-cpp.md) — Local GGUF inference, model discovery, quant selection
- [vllm-serving.md](references/vllm-serving.md) — Production LLM serving, deployment, optimization
- [lm-evaluation-harness.md](references/lm-evaluation-harness.md) — Benchmarking, training progress tracking
- [weights-and-biases.md](references/weights-and-biases.md) — Experiment tracking, sweeps, artifacts
- [huggingface-hub.md](references/huggingface-hub.md) — HF CLI reference
