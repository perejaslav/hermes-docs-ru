On this page
Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. Use for production deployment on NVIDIA GPUs (A100/H100), when you need 10-100x faster inference than PyTorch, or for serving models with quantization (FP8/INT4), in-flight batching, and multi-GPU scaling.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/tensorrt-llm`  
Path| `optional-skills/mlops/tensorrt-llm`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `tensorrt-llm`, `torch`  
Tags| `Inference Serving`, `TensorRT-LLM`, `NVIDIA`, `Inference Optimization`, `High Throughput`, `Low Latency`, `Production`, `FP8`, `INT4`, `In-Flight Batching`, `Multi-GPU`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# TensorRT-LLM
NVIDIA's open-source library for optimizing LLM inference with state-of-the-art performance on NVIDIA GPUs.
## When to use TensorRT-LLM[​](<#when-to-use-tensorrt-llm> "Direct link to When to use TensorRT-LLM")
**Use TensorRT-LLM when:**
  * Deploying on NVIDIA GPUs (A100, H100, GB200)
  * Need maximum throughput (24,000+ tokens/sec on Llama 3)
  * Require low latency for real-time applications
  * Working with quantized models (FP8, INT4, FP4)
  * Scaling across multiple GPUs or nodes


**Use vLLM instead when:**
  * Need simpler setup and Python-first API
  * Want PagedAttention without TensorRT compilation
  * Working with AMD GPUs or non-NVIDIA hardware


**Use llama.cpp instead when:**
  * Deploying on CPU or Apple Silicon
  * Need edge deployment without NVIDIA GPUs
  * Want simpler GGUF quantization format


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Docker (recommended)  
    docker pull nvidia/tensorrt_llm:latest  
      
    # pip install  
    pip install tensorrt_llm==1.2.0rc3  
      
    # Requires CUDA 13.0.0, TensorRT 10.13.2, Python 3.10-3.12  
    
[/code]
### Basic inference[​](<#basic-inference> "Direct link to Basic inference")
[code] 
    from tensorrt_llm import LLM, SamplingParams  
      
    # Initialize model  
    llm = LLM(model="meta-llama/Meta-Llama-3-8B")  
      
    # Configure sampling  
    sampling_params = SamplingParams(  
        max_tokens=100,  
        temperature=0.7,  
        top_p=0.9  
    )  
      
    # Generate  
    prompts = ["Explain quantum computing"]  
    outputs = llm.generate(prompts, sampling_params)  
      
    for output in outputs:  
        print(output.text)  
    
[/code]
### Serving with trtllm-serve[​](<#serving-with-trtllm-serve> "Direct link to Serving with trtllm-serve")
[code] 
    # Start server (automatic model download and compilation)  
    trtllm-serve meta-llama/Meta-Llama-3-8B \  
        --tp_size 4 \              # Tensor parallelism (4 GPUs)  
        --max_batch_size 256 \  
        --max_num_tokens 4096  
      
    # Client request  
    curl -X POST http://localhost:8000/v1/chat/completions \  
      -H "Content-Type: application/json" \  
      -d '{  
        "model": "meta-llama/Meta-Llama-3-8B",  
        "messages": [{"role": "user", "content": "Hello!"}],  
        "temperature": 0.7,  
        "max_tokens": 100  
      }'  
    
[/code]
## Key features[​](<#key-features> "Direct link to Key features")
### Performance optimizations[​](<#performance-optimizations> "Direct link to Performance optimizations")
  * **In-flight batching** : Dynamic batching during generation
  * **Paged KV cache** : Efficient memory management
  * **Flash Attention** : Optimized attention kernels
  * **Quantization** : FP8, INT4, FP4 for 2-4× faster inference
  * **CUDA graphs** : Reduced kernel launch overhead


### Parallelism[​](<#parallelism> "Direct link to Parallelism")
  * **Tensor parallelism (TP)** : Split model across GPUs
  * **Pipeline parallelism (PP)** : Layer-wise distribution
  * **Expert parallelism** : For Mixture-of-Experts models
  * **Multi-node** : Scale beyond single machine


### Advanced features[​](<#advanced-features> "Direct link to Advanced features")
  * **Speculative decoding** : Faster generation with draft models
  * **LoRA serving** : Efficient multi-adapter deployment
  * **Disaggregated serving** : Separate prefill and generation


## Common patterns[​](<#common-patterns> "Direct link to Common patterns")
### Quantized model (FP8)[​](<#quantized-model-fp8> "Direct link to Quantized model \(FP8\)")
[code] 
    from tensorrt_llm import LLM  
      
    # Load FP8 quantized model (2× faster, 50% memory)  
    llm = LLM(  
        model="meta-llama/Meta-Llama-3-70B",  
        dtype="fp8",  
        max_num_tokens=8192  
    )  
      
    # Inference same as before  
    outputs = llm.generate(["Summarize this article..."])  
    
[/code]
### Multi-GPU deployment[​](<#multi-gpu-deployment> "Direct link to Multi-GPU deployment")
[code] 
    # Tensor parallelism across 8 GPUs  
    llm = LLM(  
        model="meta-llama/Meta-Llama-3-405B",  
        tensor_parallel_size=8,  
        dtype="fp8"  
    )  
    
[/code]
### Batch inference[​](<#batch-inference> "Direct link to Batch inference")
[code] 
    # Process 100 prompts efficiently  
    prompts = [f"Question {i}: ..." for i in range(100)]  
      
    outputs = llm.generate(  
        prompts,  
        sampling_params=SamplingParams(max_tokens=200)  
    )  
      
    # Automatic in-flight batching for maximum throughput  
    
[/code]
## Performance benchmarks[​](<#performance-benchmarks> "Direct link to Performance benchmarks")
**Meta Llama 3-8B** (H100 GPU):
  * Throughput: 24,000 tokens/sec
  * Latency: ~10ms per token
  * vs PyTorch: **100× faster**


**Llama 3-70B** (8× A100 80GB):
  * FP8 quantization: 2× faster than FP16
  * Memory: 50% reduction with FP8


## Supported models[​](<#supported-models> "Direct link to Supported models")
  * **LLaMA family** : Llama 2, Llama 3, CodeLlama
  * **GPT family** : GPT-2, GPT-J, GPT-NeoX
  * **Qwen** : Qwen, Qwen2, QwQ
  * **DeepSeek** : DeepSeek-V2, DeepSeek-V3
  * **Mixtral** : Mixtral-8x7B, Mixtral-8x22B
  * **Vision** : LLaVA, Phi-3-vision
  * **100+ models** on HuggingFace


## References[​](<#references> "Direct link to References")
  * **[Optimization Guide](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/tensorrt-llm/references/optimization.md>)** \- Quantization, batching, KV cache tuning
  * **[Multi-GPU Setup](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/tensorrt-llm/references/multi-gpu.md>)** \- Tensor/pipeline parallelism, multi-node
  * **[Serving Guide](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/tensorrt-llm/references/serving.md>)** \- Production deployment, monitoring, autoscaling


## Resources[​](<#resources> "Direct link to Resources")
  * **Docs** : <https://nvidia.github.io/TensorRT-LLM/>
  * **GitHub** : <https://github.com/NVIDIA/TensorRT-LLM>
  * **Models** : <https://huggingface.co/models?library=tensorrt_llm>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use TensorRT-LLM](<#when-to-use-tensorrt-llm>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Basic inference](<#basic-inference>)
    * [Serving with trtllm-serve](<#serving-with-trtllm-serve>)
  * [Key features](<#key-features>)
    * [Performance optimizations](<#performance-optimizations>)
    * [Parallelism](<#parallelism>)
    * [Advanced features](<#advanced-features>)
  * [Common patterns](<#common-patterns>)
    * [Quantized model (FP8)](<#quantized-model-fp8>)
    * [Multi-GPU deployment](<#multi-gpu-deployment>)
    * [Batch inference](<#batch-inference>)
  * [Performance benchmarks](<#performance-benchmarks>)
  * [Supported models](<#supported-models>)
  * [References](<#references>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-tensorrt-llm -->
