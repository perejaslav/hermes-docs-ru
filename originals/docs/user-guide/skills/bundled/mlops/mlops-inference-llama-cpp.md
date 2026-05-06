On this page
llama.cpp local GGUF inference + HF Hub model discovery.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/mlops/inference/llama-cpp`  
Version| `2.1.2`  
Author| Orchestra Research  
License| MIT  
Dependencies| `llama-cpp-python>=0.2.0`  
Tags| `llama.cpp`, `GGUF`, `Quantization`, `Hugging Face Hub`, `CPU Inference`, `Apple Silicon`, `Edge Deployment`, `AMD GPUs`, `Intel GPUs`, `NVIDIA`, `URL-first`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# llama.cpp + GGUF
Use this skill for local GGUF inference, quant selection, or Hugging Face repo discovery for llama.cpp.
## When to use[​](<#when-to-use> "Direct link to When to use")
  * Run local models on CPU, Apple Silicon, CUDA, ROCm, or Intel GPUs
  * Find the right GGUF for a specific Hugging Face repo
  * Build a `llama-server` or `llama-cli` command from the Hub
  * Search the Hub for models that already support llama.cpp
  * Enumerate available `.gguf` files and sizes for a repo
  * Decide between Q4/Q5/Q6/IQ variants for the user's RAM or VRAM


## Model Discovery workflow[​](<#model-discovery-workflow> "Direct link to Model Discovery workflow")
Prefer URL workflows before asking for `hf`, Python, or custom scripts.
  1. Search for candidate repos on the Hub:
     * Base: `https://huggingface.co/models?apps=llama.cpp&sort=trending`
     * Add `search=<term>` for a model family
     * Add `num_parameters=min:0,max:24B` or similar when the user has size constraints
  2. Open the repo with the llama.cpp local-app view:
     * `https://huggingface.co/<repo>?local-app=llama.cpp`
  3. Treat the local-app snippet as the source of truth when it is visible:
     * copy the exact `llama-server` or `llama-cli` command
     * report the recommended quant exactly as HF shows it
  4. Read the same `?local-app=llama.cpp` URL as page text or HTML and extract the section under `Hardware compatibility`:
     * prefer its exact quant labels and sizes over generic tables
     * keep repo-specific labels such as `UD-Q4_K_M` or `IQ4_NL_XL`
     * if that section is not visible in the fetched page source, say so and fall back to the tree API plus generic quant guidance
  5. Query the tree API to confirm what actually exists:
     * `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`
     * keep entries where `type` is `file` and `path` ends with `.gguf`
     * use `path` and `size` as the source of truth for filenames and byte sizes
     * separate quantized checkpoints from `mmproj-*.gguf` projector files and `BF16/` shard files
     * use `https://huggingface.co/<repo>/tree/main` only as a human fallback
  6. If the local-app snippet is not text-visible, reconstruct the command from the repo plus the chosen quant:
     * shorthand quant selection: `llama-server -hf <repo>:<QUANT>`
     * exact-file fallback: `llama-server --hf-repo <repo> --hf-file <filename.gguf>`
  7. Only suggest conversion from Transformers weights if the repo does not already expose GGUF files.


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Install llama.cpp[​](<#install-llamacpp> "Direct link to Install llama.cpp")
[code] 
    # macOS / Linux (simplest)  
    brew install llama.cpp  
    
[/code]
[code] 
    winget install llama.cpp  
    
[/code]
[code] 
    git clone https://github.com/ggml-org/llama.cpp  
    cd llama.cpp  
    cmake -B build  
    cmake --build build --config Release  
    
[/code]
### Run directly from the Hugging Face Hub[​](<#run-directly-from-the-hugging-face-hub> "Direct link to Run directly from the Hugging Face Hub")
[code] 
    llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0  
    
[/code]
[code] 
    llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0  
    
[/code]
### Run an exact GGUF file from the Hub[​](<#run-an-exact-gguf-file-from-the-hub> "Direct link to Run an exact GGUF file from the Hub")
Use this when the tree API shows custom file naming or the exact HF snippet is missing.
[code] 
    llama-server \  
        --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \  
        --hf-file Phi-3-mini-4k-instruct-q4.gguf \  
        -c 4096  
    
[/code]
### OpenAI-compatible server check[​](<#openai-compatible-server-check> "Direct link to OpenAI-compatible server check")
[code] 
    curl http://localhost:8080/v1/chat/completions \  
      -H "Content-Type: application/json" \  
      -d '{  
        "messages": [  
          {"role": "user", "content": "Write a limerick about Python exceptions"}  
        ]  
      }'  
    
[/code]
## Python bindings (llama-cpp-python)[​](<#python-bindings-llama-cpp-python> "Direct link to Python bindings \(llama-cpp-python\)")
`pip install llama-cpp-python` (CUDA: `CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir`; Metal: `CMAKE_ARGS="-DGGML_METAL=on" ...`).
### Basic generation[​](<#basic-generation> "Direct link to Basic generation")
[code] 
    from llama_cpp import Llama  
      
    llm = Llama(  
        model_path="./model-q4_k_m.gguf",  
        n_ctx=4096,  
        n_gpu_layers=35,     # 0 for CPU, 99 to offload everything  
        n_threads=8,  
    )  
      
    out = llm("What is machine learning?", max_tokens=256, temperature=0.7)  
    print(out["choices"][0]["text"])  
    
[/code]
### Chat + streaming[​](<#chat--streaming> "Direct link to Chat + streaming")
[code] 
    llm = Llama(  
        model_path="./model-q4_k_m.gguf",  
        n_ctx=4096,  
        n_gpu_layers=35,  
        chat_format="llama-3",   # or "chatml", "mistral", etc.  
    )  
      
    resp = llm.create_chat_completion(  
        messages=[  
            {"role": "system", "content": "You are a helpful assistant."},  
            {"role": "user", "content": "What is Python?"},  
        ],  
        max_tokens=256,  
    )  
    print(resp["choices"][0]["message"]["content"])  
      
    # Streaming  
    for chunk in llm("Explain quantum computing:", max_tokens=256, stream=True):  
        print(chunk["choices"][0]["text"], end="", flush=True)  
    
[/code]
### Embeddings[​](<#embeddings> "Direct link to Embeddings")
[code] 
    llm = Llama(model_path="./model-q4_k_m.gguf", embedding=True, n_gpu_layers=35)  
    vec = llm.embed("This is a test sentence.")  
    print(f"Embedding dimension: {len(vec)}")  
    
[/code]
You can also load a GGUF straight from the Hub:
[code] 
    llm = Llama.from_pretrained(  
        repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",  
        filename="*Q4_K_M.gguf",  
        n_gpu_layers=35,  
    )  
    
[/code]
## Choosing a quant[​](<#choosing-a-quant> "Direct link to Choosing a quant")
Use the Hub page first, generic heuristics second.
  * Prefer the exact quant that HF marks as compatible for the user's hardware profile.
  * For general chat, start with `Q4_K_M`.
  * For code or technical work, prefer `Q5_K_M` or `Q6_K` if memory allows.
  * For very tight RAM budgets, consider `Q3_K_M`, `IQ` variants, or `Q2` variants only if the user explicitly prioritizes fit over quality.
  * For multimodal repos, mention `mmproj-*.gguf` separately. The projector is not the main model file.
  * Do not normalize repo-native labels. If the page says `UD-Q4_K_M`, report `UD-Q4_K_M`.


## Extracting available GGUFs from a repo[​](<#extracting-available-ggufs-from-a-repo> "Direct link to Extracting available GGUFs from a repo")
When the user asks what GGUFs exist, return:
  * filename
  * file size
  * quant label
  * whether it is a main model or an auxiliary projector


Ignore unless requested:
  * README
  * BF16 shard files
  * imatrix blobs or calibration artifacts


Use the tree API for this step:
  * `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`


For a repo like `unsloth/Qwen3.6-35B-A3B-GGUF`, the local-app page can show quant chips such as `UD-Q4_K_M`, `UD-Q5_K_M`, `UD-Q6_K`, and `Q8_0`, while the tree API exposes exact file paths such as `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` and `Qwen3.6-35B-A3B-Q8_0.gguf` with byte sizes. Use the tree API to turn a quant label into an exact filename.
## Search patterns[​](<#search-patterns> "Direct link to Search patterns")
Use these URL shapes directly:
[code] 
    https://huggingface.co/models?apps=llama.cpp&sort=trending  
    https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending  
    https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending  
    https://huggingface.co/<repo>?local-app=llama.cpp  
    https://huggingface.co/api/models/<repo>/tree/main?recursive=true  
    https://huggingface.co/<repo>/tree/main  
    
[/code]
## Output format[​](<#output-format> "Direct link to Output format")
When answering discovery requests, prefer a compact structured result like:
[code] 
    Repo: <repo>  
    Recommended quant from HF: <label> (<size>)  
    llama-server: <command>  
    Other GGUFs:  
    - <filename> - <size>  
    - <filename> - <size>  
    Source URLs:  
    - <local-app URL>  
    - <tree API URL>  
    
[/code]
## References[​](<#references> "Direct link to References")
  * **[hub-discovery.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/hub-discovery.md>)** \- URL-only Hugging Face workflows, search patterns, GGUF extraction, and command reconstruction
  * **[advanced-usage.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/advanced-usage.md>)** — speculative decoding, batched inference, grammar-constrained generation, LoRA, multi-GPU, custom builds, benchmark scripts
  * **[quantization.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/quantization.md>)** — quant quality tradeoffs, when to use Q4/Q5/Q6/IQ, model size scaling, imatrix
  * **[server.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/server.md>)** — direct-from-Hub server launch, OpenAI API endpoints, Docker deployment, NGINX load balancing, monitoring
  * **[optimization.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/optimization.md>)** — CPU threading, BLAS, GPU offload heuristics, batch tuning, benchmarks
  * **[troubleshooting.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/troubleshooting.md>)** — install/convert/quantize/inference/server issues, Apple Silicon, debugging


## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/ggml-org/llama.cpp>
  * **Hugging Face GGUF + llama.cpp docs** : <https://huggingface.co/docs/hub/gguf-llamacpp>
  * **Hugging Face Local Apps docs** : <https://huggingface.co/docs/hub/main/local-apps>
  * **Hugging Face Local Agents docs** : <https://huggingface.co/docs/hub/agents-local>
  * **Example local-app page** : <https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF?local-app=llama.cpp>
  * **Example tree API** : <https://huggingface.co/api/models/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main?recursive=true>
  * **Example llama.cpp search** : [https://huggingface.co/models?num_parameters=min:0,max:24B&apps=llama.cpp&sort=trending](<https://huggingface.co/models?num_parameters=min:0,max:24B&apps=llama.cpp&sort=trending>)
  * **License** : MIT


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Model Discovery workflow](<#model-discovery-workflow>)
  * [Quick start](<#quick-start>)
    * [Install llama.cpp](<#install-llamacpp>)
    * [Run directly from the Hugging Face Hub](<#run-directly-from-the-hugging-face-hub>)
    * [Run an exact GGUF file from the Hub](<#run-an-exact-gguf-file-from-the-hub>)
    * [OpenAI-compatible server check](<#openai-compatible-server-check>)
  * [Python bindings (llama-cpp-python)](<#python-bindings-llama-cpp-python>)
    * [Basic generation](<#basic-generation>)
    * [Chat + streaming](<#chat--streaming>)
    * [Embeddings](<#embeddings>)
  * [Choosing a quant](<#choosing-a-quant>)
  * [Extracting available GGUFs from a repo](<#extracting-available-ggufs-from-a-repo>)
  * [Search patterns](<#search-patterns>)
  * [Output format](<#output-format>)
  * [References](<#references>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-inference-llama-cpp -->
