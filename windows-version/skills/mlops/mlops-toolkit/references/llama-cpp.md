# llama.cpp + GGUF Local Inference

Local GGUF inference, quant selection, and HuggingFace repo discovery for llama.cpp.

## When to use
- Run local models on CPU, Apple Silicon, CUDA, ROCm, or Intel GPUs
- Find the right GGUF for a specific HuggingFace repo
- Build a `llama-server` or `llama-cli` command from the Hub
- Decide between Q4/Q5/Q6/IQ variants for RAM/VRAM constraints

## Install

```bash
brew install llama.cpp  # macOS/Linux
winget install llama.cpp  # Windows
```

## Run from HuggingFace Hub

```bash
llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

## Exact file fallback

```bash
llama-server \
    --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \
    --hf-file Phi-3-mini-4k-instruct-q4.gguf \
    -c 4096
```

## Python bindings

```bash
pip install llama-cpp-python
# CUDA: CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
# Metal: CMAKE_ARGS="-DGGML_METAL=on" ...
```

```python
from llama_cpp import Llama

llm = Llama(model_path="./model-q4_k_m.gguf", n_ctx=4096, n_gpu_layers=35, n_threads=8)
out = llm("What is machine learning?", max_tokens=256, temperature=0.7)
print(out["choices"][0]["text"])
```

## Load from Hub

```python
llm = Llama.from_pretrained(
    repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
    filename="*Q4_K_M.gguf",
    n_gpu_layers=35,
)
```

## Choosing a quant

- Prefer exact quant HF marks as compatible for user's hardware
- General chat: `Q4_K_M`
- Code/technical: `Q5_K_M` or `Q6_K`
- Tight RAM: `Q3_K_M`, `IQ` variants
- Don't normalize repo-native labels (if page says `UD-Q4_K_M`, report `UD-Q4_K_M`)

## Model Discovery URLs

```
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending
https://huggingface.co/<repo>?local-app=llama.cpp
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
```

## Output format for discovery

```
Repo: <repo>
Recommended quant from HF: <label> (<size>)
llama-server: <command>
Other GGUFs:
- <filename> - <size>
Source URLs:
- <local-app URL>
- <tree API URL>
```

## References
- GitHub: https://github.com/ggml-org/llama.cpp
- HF docs: https://huggingface.co/docs/hub/gguf-llamacpp
