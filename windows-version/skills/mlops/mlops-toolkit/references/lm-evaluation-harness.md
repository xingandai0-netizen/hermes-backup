# lm-evaluation-harness — LLM Benchmarking

Evaluate LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag).

## Install

```bash
pip install lm-eval
```

## Quick start

```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8
```

## Core benchmarks

| Benchmark | What it measures |
|-----------|-----------------|
| MMLU | 57 subjects, multiple choice |
| GSM8K | Grade school math |
| HellaSwag | Common sense reasoning |
| TruthfulQA | Truthfulness |
| ARC | Science questions |
| HumanEval | Python code generation |
| MBPP | Python coding |

## Standard evaluation suite

```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --num_fewshot 5 \
  --batch_size 8 \
  --output_path results/llama2-7b-eval.json
```

## vLLM backend (5-10x faster)

```bash
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu \
  --batch_size auto
```

## Quantized evaluation

```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,load_in_4bit=True \
  --tasks mmlu
```

## Training progress tracking

```bash
# Evaluate checkpoints during training
lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 \
  --output_path results/step-$STEP.json
```

## Quick benchmarks for frequent eval

- HellaSwag: ~10 min on 1 GPU
- GSM8K: ~5 min
- PIQA: ~2 min
- Avoid MMLU (~2 hours) and HumanEval (needs code execution) for frequent eval

## Results format

```json
{
  "results": {
    "mmlu": { "acc": 0.459, "acc_stderr": 0.004 },
    "gsm8k": { "exact_match": 0.142, "exact_match_stderr": 0.006 }
  }
}
```

## Common issues

| Issue | Fix |
|-------|-----|
| Too slow | Use vLLM backend, reduce fewshot, use task subsets |
| OOM | Reduce batch_size, use quantization, CPU offloading |
| Different results | Check fewshot count (5-shot standard), exact task name |

## Hardware requirements

- 7B: 16GB (bf16) or 8GB (8-bit)
- 13B: 28GB (bf16) or 14GB (8-bit)
- 70B: Multi-GPU or quantization

## Resources
- GitHub: https://github.com/EleutherAI/lm-evaluation-harness
- Leaderboard: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
