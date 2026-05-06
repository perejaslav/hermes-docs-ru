On this page
vLLM: high-throughput LLM serving, OpenAI API, quantization.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/mlops/inference/vllm`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `vllm`, `torch`, `transformers`  
Tags| `vLLM`, `Inference Serving`, `PagedAttention`, `Continuous Batching`, `High Throughput`, `Production`, `OpenAI API`, `Quantization`, `Tensor Parallelism`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# vLLM - High-Performance LLM Serving
## When to use[​](<#when-to-use> "Direct link to When to use")
Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism.
## Quick start[​](<#quick-start> "Direct link to Quick start")
vLLM achieves 24x higher throughput than standard transformers through PagedAttention (block-based KV cache) and continuous batching (mixing prefill/decode requests).
**Installation** :
[code] 
    pip install vllm  
    
[/code]
**Basic offline inference** :
[code] 
    from vllm import LLM, SamplingParams  
      
    llm = LLM(model="meta-llama/Llama-3-8B-Instruct")  
    sampling = SamplingParams(temperature=0.7, max_tokens=256)  
      
    outputs = llm.generate(["Explain quantum computing"], sampling)  
    print(outputs[0].outputs[0].text)  
    
[/code]
**OpenAI-compatible server** :
[code] 
    vllm serve meta-llama/Llama-3-8B-Instruct  
      
    # Query with OpenAI SDK  
    python -c "  
    from openai import OpenAI  
    client = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')  
    print(client.chat.completions.create(  
        model='meta-llama/Llama-3-8B-Instruct',  
        messages=[{'role': 'user', 'content': 'Hello!'}]  
    ).choices[0].message.content)  
    "  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: Production API deployment[​](<#workflow-1-production-api-deployment> "Direct link to Workflow 1: Production API deployment")
Copy this checklist and track progress:
[code] 
    Deployment Progress:  
    - [ ] Step 1: Configure server settings  
    - [ ] Step 2: Test with limited traffic  
    - [ ] Step 3: Enable monitoring  
    - [ ] Step 4: Deploy to production  
    - [ ] Step 5: Verify performance metrics  
    
[/code]
**Step 1: Configure server settings**
Choose configuration based on your model size:
[code] 
    # For 7B-13B models on single GPU  
    vllm serve meta-llama/Llama-3-8B-Instruct \  
      --gpu-memory-utilization 0.9 \  
      --max-model-len 8192 \  
      --port 8000  
      
    # For 30B-70B models with tensor parallelism  
    vllm serve meta-llama/Llama-2-70b-hf \  
      --tensor-parallel-size 4 \  
      --gpu-memory-utilization 0.9 \  
      --quantization awq \  
      --port 8000  
      
    # For production with caching and metrics  
    vllm serve meta-llama/Llama-3-8B-Instruct \  
      --gpu-memory-utilization 0.9 \  
      --enable-prefix-caching \  
      --enable-metrics \  
      --metrics-port 9090 \  
      --port 8000 \  
      --host 0.0.0.0  
    
[/code]
**Step 2: Test with limited traffic**
Run load test before production:
[code] 
    # Install load testing tool  
    pip install locust  
      
    # Create test_load.py with sample requests  
    # Run: locust -f test_load.py --host http://localhost:8000  
    
[/code]
Verify TTFT (time to first token) < 500ms and throughput > 100 req/sec.
**Step 3: Enable monitoring**
vLLM exposes Prometheus metrics on port 9090:
[code] 
    curl http://localhost:9090/metrics | grep vllm  
    
[/code]
Key metrics to monitor:
  * `vllm:time_to_first_token_seconds` \- Latency
  * `vllm:num_requests_running` \- Active requests
  * `vllm:gpu_cache_usage_perc` \- KV cache utilization


**Step 4: Deploy to production**
Use Docker for consistent deployment:
[code] 
    # Run vLLM in Docker  
    docker run --gpus all -p 8000:8000 \  
      vllm/vllm-openai:latest \  
      --model meta-llama/Llama-3-8B-Instruct \  
      --gpu-memory-utilization 0.9 \  
      --enable-prefix-caching  
    
[/code]
**Step 5: Verify performance metrics**
Check that deployment meets targets:
  * TTFT < 500ms (for short prompts)
  * Throughput > target req/sec
  * GPU utilization > 80%
  * No OOM errors in logs


### Workflow 2: Offline batch inference[​](<#workflow-2-offline-batch-inference> "Direct link to Workflow 2: Offline batch inference")
For processing large datasets without server overhead.
Copy this checklist:
[code] 
    Batch Processing:  
    - [ ] Step 1: Prepare input data  
    - [ ] Step 2: Configure LLM engine  
    - [ ] Step 3: Run batch inference  
    - [ ] Step 4: Process results  
    
[/code]
**Step 1: Prepare input data**
[code] 
    # Load prompts from file  
    prompts = []  
    with open("prompts.txt") as f:  
        prompts = [line.strip() for line in f]  
      
    print(f"Loaded {len(prompts)} prompts")  
    
[/code]
**Step 2: Configure LLM engine**
[code] 
    from vllm import LLM, SamplingParams  
      
    llm = LLM(  
        model="meta-llama/Llama-3-8B-Instruct",  
        tensor_parallel_size=2,  # Use 2 GPUs  
        gpu_memory_utilization=0.9,  
        max_model_len=4096  
    )  
      
    sampling = SamplingParams(  
        temperature=0.7,  
        top_p=0.95,  
        max_tokens=512,  
        stop=["</s>", "\n\n"]  
    )  
    
[/code]
**Step 3: Run batch inference**
vLLM automatically batches requests for efficiency:
[code] 
    # Process all prompts in one call  
    outputs = llm.generate(prompts, sampling)  
      
    # vLLM handles batching internally  
    # No need to manually chunk prompts  
    
[/code]
**Step 4: Process results**
[code] 
    # Extract generated text  
    results = []  
    for output in outputs:  
        prompt = output.prompt  
        generated = output.outputs[0].text  
        results.append({  
            "prompt": prompt,  
            "generated": generated,  
            "tokens": len(output.outputs[0].token_ids)  
        })  
      
    # Save to file  
    import json  
    with open("results.jsonl", "w") as f:  
        for result in results:  
            f.write(json.dumps(result) + "\n")  
      
    print(f"Processed {len(results)} prompts")  
    
[/code]
### Workflow 3: Quantized model serving[​](<#workflow-3-quantized-model-serving> "Direct link to Workflow 3: Quantized model serving")
Fit large models in limited GPU memory.
[code] 
    Quantization Setup:  
    - [ ] Step 1: Choose quantization method  
    - [ ] Step 2: Find or create quantized model  
    - [ ] Step 3: Launch with quantization flag  
    - [ ] Step 4: Verify accuracy  
    
[/code]
**Step 1: Choose quantization method**
  * **AWQ** : Best for 70B models, minimal accuracy loss
  * **GPTQ** : Wide model support, good compression
  * **FP8** : Fastest on H100 GPUs


**Step 2: Find or create quantized model**
Use pre-quantized models from HuggingFace:
[code] 
    # Search for AWQ models  
    # Example: TheBloke/Llama-2-70B-AWQ  
    
[/code]
**Step 3: Launch with quantization flag**
[code] 
    # Using pre-quantized model  
    vllm serve TheBloke/Llama-2-70B-AWQ \  
      --quantization awq \  
      --tensor-parallel-size 1 \  
      --gpu-memory-utilization 0.95  
      
    # Results: 70B model in ~40GB VRAM  
    
[/code]
**Step 4: Verify accuracy**
Test outputs match expected quality:
[code] 
    # Compare quantized vs non-quantized responses  
    # Verify task-specific performance unchanged  
    
[/code]
## When to use vs alternatives[​](<#when-to-use-vs-alternatives> "Direct link to When to use vs alternatives")
**Use vLLM when:**
  * Deploying production LLM APIs (100+ req/sec)
  * Serving OpenAI-compatible endpoints
  * Limited GPU memory but need large models
  * Multi-user applications (chatbots, assistants)
  * Need low latency with high throughput


**Use alternatives instead:**
  * **llama.cpp** : CPU/edge inference, single-user
  * **HuggingFace transformers** : Research, prototyping, one-off generation
  * **TensorRT-LLM** : NVIDIA-only, need absolute maximum performance
  * **Text-Generation-Inference** : Already in HuggingFace ecosystem


## Common issues[​](<#common-issues> "Direct link to Common issues")
**Issue: Out of memory during model loading**
Reduce memory usage:
[code] 
    vllm serve MODEL \  
      --gpu-memory-utilization 0.7 \  
      --max-model-len 4096  
    
[/code]
Or use quantization:
[code] 
    vllm serve MODEL --quantization awq  
    
[/code]
**Issue: Slow first token (TTFT > 1 second)**
Enable prefix caching for repeated prompts:
[code] 
    vllm serve MODEL --enable-prefix-caching  
    
[/code]
For long prompts, enable chunked prefill:
[code] 
    vllm serve MODEL --enable-chunked-prefill  
    
[/code]
**Issue: Model not found error**
Use `--trust-remote-code` for custom models:
[code] 
    vllm serve MODEL --trust-remote-code  
    
[/code]
**Issue: Low throughput ( <50 req/sec)**
Increase concurrent sequences:
[code] 
    vllm serve MODEL --max-num-seqs 512  
    
[/code]
Check GPU utilization with `nvidia-smi` \- should be >80%.
**Issue: Inference slower than expected**
Verify tensor parallelism uses power of 2 GPUs:
[code] 
    vllm serve MODEL --tensor-parallel-size 4  # Not 3  
    
[/code]
Enable speculative decoding for faster generation:
[code] 
    vllm serve MODEL --speculative-model DRAFT_MODEL  
    
[/code]
## Advanced topics[​](<#advanced-topics> "Direct link to Advanced topics")
**Server deployment patterns** : See [references/server-deployment.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/server-deployment.md>) for Docker, Kubernetes, and load balancing configurations.
**Performance optimization** : See [references/optimization.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/optimization.md>) for PagedAttention tuning, continuous batching details, and benchmark results.
**Quantization guide** : See [references/quantization.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/quantization.md>) for AWQ/GPTQ/FP8 setup, model preparation, and accuracy comparisons.
**Troubleshooting** : See [references/troubleshooting.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/troubleshooting.md>) for detailed error messages, debugging steps, and performance diagnostics.
## Hardware requirements[​](<#hardware-requirements> "Direct link to Hardware requirements")
  * **Small models (7B-13B)** : 1x A10 (24GB) or A100 (40GB)
  * **Medium models (30B-40B)** : 2x A100 (40GB) with tensor parallelism
  * **Large models (70B+)** : 4x A100 (40GB) or 2x A100 (80GB), use AWQ/GPTQ


Supported platforms: NVIDIA (primary), AMD ROCm, Intel GPUs, TPUs
## Resources[​](<#resources> "Direct link to Resources")
  * Official docs: <https://docs.vllm.ai>
  * GitHub: <https://github.com/vllm-project/vllm>
  * Paper: "Efficient Memory Management for Large Language Model Serving with PagedAttention" (SOSP 2023)
  * Community: <https://discuss.vllm.ai>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Quick start](<#quick-start>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: Production API deployment](<#workflow-1-production-api-deployment>)
    * [Workflow 2: Offline batch inference](<#workflow-2-offline-batch-inference>)
    * [Workflow 3: Quantized model serving](<#workflow-3-quantized-model-serving>)
  * [When to use vs alternatives](<#when-to-use-vs-alternatives>)
  * [Common issues](<#common-issues>)
  * [Advanced topics](<#advanced-topics>)
  * [Hardware requirements](<#hardware-requirements>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-inference-vllm -->
