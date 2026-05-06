On this page
This guide walks you through running a local LLM server on macOS with an OpenAI-compatible API. You get full privacy, zero API costs, and surprisingly good performance on Apple Silicon.
We cover two backends:
Backend| Install| Best at| Format  
---|---|---|---  
**llama.cpp**| `brew install llama.cpp`| Fastest time-to-first-token, quantized KV cache for low memory| GGUF  
**omlx**| [omlx.ai](<https://omlx.ai>)| Fastest token generation, native Metal optimization| MLX (safetensors)  
Both expose an OpenAI-compatible `/v1/chat/completions` endpoint. Hermes works with either one — just point it at `http://localhost:8080` or `http://localhost:8000`.
Apple Silicon only
This guide targets Macs with Apple Silicon (M1 and later). Intel Macs will work with llama.cpp but without GPU acceleration — expect significantly slower performance.
* * *
## Choosing a model[​](<#choosing-a-model> "Direct link to Choosing a model")
For getting started, we recommend **Qwen3.5-9B** — it's a strong reasoning model that fits comfortably in 8GB+ of unified memory with quantization.
Variant| Size on disk| RAM needed (128K context)| Backend  
---|---|---|---  
Qwen3.5-9B-Q4_K_M (GGUF)| 5.3 GB| ~10 GB with quantized KV cache| llama.cpp  
Qwen3.5-9B-mlx-lm-mxfp4 (MLX)| ~5 GB| ~12 GB| omlx  
**Memory rule of thumb:** model size + KV cache. A 9B Q4 model is ~5 GB. The KV cache at 128K context with Q4 quantization adds ~4-5 GB. With default (f16) KV cache, that balloons to ~16 GB. The quantized KV cache flags in llama.cpp are the key trick for memory-constrained systems.
For larger models (27B, 35B), you'll need 32 GB+ of unified memory. The 9B is the sweet spot for 8-16 GB machines.
* * *
## Option A: llama.cpp[​](<#option-a-llamacpp> "Direct link to Option A: llama.cpp")
llama.cpp is the most portable local LLM runtime. On macOS it uses Metal for GPU acceleration out of the box.
### Install[​](<#install> "Direct link to Install")
[code] 
    brew install llama.cpp  
    
[/code]
This gives you the `llama-server` command globally.
### Download the model[​](<#download-the-model> "Direct link to Download the model")
You need a GGUF-format model. The easiest source is Hugging Face via the `huggingface-cli`:
[code] 
    brew install huggingface-cli  
    
[/code]
Then download:
[code] 
    huggingface-cli download unsloth/Qwen3.5-9B-GGUF Qwen3.5-9B-Q4_K_M.gguf --local-dir ~/models  
    
[/code]
Gated models
Some models on Hugging Face require authentication. Run `huggingface-cli login` first if you get a 401 or 404 error.
### Start the server[​](<#start-the-server> "Direct link to Start the server")
[code] 
    llama-server -m ~/models/Qwen3.5-9B-Q4_K_M.gguf \  
      -ngl 99 \  
      -c 131072 \  
      -np 1 \  
      -fa on \  
      --cache-type-k q4_0 \  
      --cache-type-v q4_0 \  
      --host 0.0.0.0  
    
[/code]
Here's what each flag does:
Flag| Purpose  
---|---  
`-ngl 99`| Offload all layers to GPU (Metal). Use a high number to ensure nothing stays on CPU.  
`-c 131072`| Context window size (128K tokens). Reduce this if you're low on memory.  
`-np 1`| Number of parallel slots. Keep at 1 for single-user use — more slots split your memory budget.  
`-fa on`| Flash attention. Reduces memory usage and speeds up long-context inference.  
`--cache-type-k q4_0`| Quantize the key cache to 4-bit. **This is the big memory saver.**  
`--cache-type-v q4_0`| Quantize the value cache to 4-bit. Together with the above, this cuts KV cache memory by ~75% vs f16.  
`--host 0.0.0.0`| Listen on all interfaces. Use `127.0.0.1` if you don't need network access.  
The server is ready when you see:
[code] 
    main: server is listening on http://0.0.0.0:8080  
    srv  update_slots: all slots are idle  
    
[/code]
### Memory optimization for constrained systems[​](<#memory-optimization-for-constrained-systems> "Direct link to Memory optimization for constrained systems")
The `--cache-type-k q4_0 --cache-type-v q4_0` flags are the most important optimization for systems with limited memory. Here's the impact at 128K context:
KV cache type| KV cache memory (128K ctx, 9B model)  
---|---  
f16 (default)| ~16 GB  
q8_0| ~8 GB  
**q4_0**| **~4 GB**  
On an 8 GB Mac, use `q4_0` KV cache and reduce context to `-c 32768` (32K). On 16 GB, you can comfortably do 128K context. On 32 GB+, you can run larger models or multiple parallel slots.
If you're still running out of memory, reduce context size first (`-c`), then try a smaller quantization (Q3_K_M instead of Q4_K_M).
### Test it[​](<#test-it> "Direct link to Test it")
[code] 
    curl -s http://localhost:8080/v1/chat/completions \  
      -H "Content-Type: application/json" \  
      -d '{  
        "model": "Qwen3.5-9B-Q4_K_M.gguf",  
        "messages": [{"role": "user", "content": "Hello!"}],  
        "max_tokens": 50  
      }' | jq .choices[0].message.content  
    
[/code]
### Get the model name[​](<#get-the-model-name> "Direct link to Get the model name")
If you forget the model name, query the models endpoint:
[code] 
    curl -s http://localhost:8080/v1/models | jq '.data[].id'  
    
[/code]
* * *
## Option B: MLX via omlx[​](<#option-b-mlx-via-omlx> "Direct link to Option B: MLX via omlx")
[omlx](<https://omlx.ai>) is a macOS-native app that manages and serves MLX models. MLX is Apple's own machine learning framework, optimized specifically for Apple Silicon's unified memory architecture.
### Install[​](<#install-1> "Direct link to Install")
Download and install from [omlx.ai](<https://omlx.ai>). It provides a GUI for model management and a built-in server.
### Download the model[​](<#download-the-model-1> "Direct link to Download the model")
Use the omlx app to browse and download models. Search for `Qwen3.5-9B-mlx-lm-mxfp4` and download it. Models are stored locally (typically in `~/.omlx/models/`).
### Start the server[​](<#start-the-server-1> "Direct link to Start the server")
omlx serves models on `http://127.0.0.1:8000` by default. Start serving from the app UI, or use the CLI if available.
### Test it[​](<#test-it-1> "Direct link to Test it")
[code] 
    curl -s http://127.0.0.1:8000/v1/chat/completions \  
      -H "Content-Type: application/json" \  
      -d '{  
        "model": "Qwen3.5-9B-mlx-lm-mxfp4",  
        "messages": [{"role": "user", "content": "Hello!"}],  
        "max_tokens": 50  
      }' | jq .choices[0].message.content  
    
[/code]
### List available models[​](<#list-available-models> "Direct link to List available models")
omlx can serve multiple models simultaneously:
[code] 
    curl -s http://127.0.0.1:8000/v1/models | jq '.data[].id'  
    
[/code]
* * *
## Benchmarks: llama.cpp vs MLX[​](<#benchmarks-llamacpp-vs-mlx> "Direct link to Benchmarks: llama.cpp vs MLX")
Both backends tested on the same machine (Apple M5 Max, 128 GB unified memory) running the same model (Qwen3.5-9B) at comparable quantization levels (Q4_K_M for GGUF, mxfp4 for MLX). Five diverse prompts, three runs each, backends tested sequentially to avoid resource contention.
### Results[​](<#results> "Direct link to Results")
Metric| llama.cpp (Q4_K_M)| MLX (mxfp4)| Winner  
---|---|---|---  
**TTFT (avg)**| **67 ms**|  289 ms| llama.cpp (4.3x faster)  
**TTFT (p50)**| **66 ms**|  286 ms| llama.cpp (4.3x faster)  
**Generation (avg)**|  70 tok/s| **96 tok/s**|  MLX (37% faster)  
**Generation (p50)**|  70 tok/s| **96 tok/s**|  MLX (37% faster)  
**Total time (512 tokens)**|  7.3s| **5.5s**|  MLX (25% faster)  
### What this means[​](<#what-this-means> "Direct link to What this means")
  * **llama.cpp** excels at prompt processing — its flash attention + quantized KV cache pipeline gets you the first token in ~66ms. If you're building interactive applications where perceived responsiveness matters (chatbots, autocomplete), this is a meaningful advantage.
  * **MLX** generates tokens ~37% faster once it gets going. For batch workloads, long-form generation, or any task where total completion time matters more than initial latency, MLX finishes sooner.
  * Both backends are **extremely consistent** — variance across runs was negligible. You can rely on these numbers.


### Which one should you pick?[​](<#which-one-should-you-pick> "Direct link to Which one should you pick?")
Use case| Recommendation  
---|---  
Interactive chat, low-latency tools| llama.cpp  
Long-form generation, bulk processing| MLX (omlx)  
Memory-constrained (8-16 GB)| llama.cpp (quantized KV cache is unmatched)  
Serving multiple models simultaneously| omlx (built-in multi-model support)  
Maximum compatibility (Linux too)| llama.cpp  
* * *
## Connect to Hermes[​](<#connect-to-hermes> "Direct link to Connect to Hermes")
Once your local server is running:
[code] 
    hermes model  
    
[/code]
Select **Custom endpoint** and follow the prompts. It will ask for the base URL and model name — use the values from whichever backend you set up above.
* * *
## Timeouts[​](<#timeouts> "Direct link to Timeouts")
Hermes automatically detects local endpoints (localhost, LAN IPs) and relaxes its streaming timeouts. No configuration needed for most setups.
If you still hit timeout errors (e.g. very large contexts on slow hardware), you can override the streaming read timeout:
[code] 
    # In your .env — raise from the 120s default to 30 minutes  
    HERMES_STREAM_READ_TIMEOUT=1800  
    
[/code]
Timeout| Default| Local auto-adjustment| Env var override  
---|---|---|---  
Stream read (socket-level)| 120s| Raised to 1800s| `HERMES_STREAM_READ_TIMEOUT`  
Stale stream detection| 180s| Disabled entirely| `HERMES_STREAM_STALE_TIMEOUT`  
API call (non-streaming)| 1800s| No change needed| `HERMES_API_TIMEOUT`  
The stream read timeout is the one most likely to cause issues — it's the socket-level deadline for receiving the next chunk of data. During prefill on large contexts, local models may produce no output for minutes while processing the prompt. The auto-detection handles this transparently.
  * [Choosing a model](<#choosing-a-model>)
  * [Option A: llama.cpp](<#option-a-llamacpp>)
    * [Install](<#install>)
    * [Download the model](<#download-the-model>)
    * [Start the server](<#start-the-server>)
    * [Memory optimization for constrained systems](<#memory-optimization-for-constrained-systems>)
    * [Test it](<#test-it>)
    * [Get the model name](<#get-the-model-name>)
  * [Option B: MLX via omlx](<#option-b-mlx-via-omlx>)
    * [Install](<#install-1>)
    * [Download the model](<#download-the-model-1>)
    * [Start the server](<#start-the-server-1>)
    * [Test it](<#test-it-1>)
    * [List available models](<#list-available-models>)
  * [Benchmarks: llama.cpp vs MLX](<#benchmarks-llamacpp-vs-mlx>)
    * [Results](<#results>)
    * [What this means](<#what-this-means>)
    * [Which one should you pick?](<#which-one-should-you-pick>)
  * [Connect to Hermes](<#connect-to-hermes>)
  * [Timeouts](<#timeouts>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/local-llm-on-mac -->
