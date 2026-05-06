On this page
Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. Use when training/running transformers with long sequences (>512 tokens), encountering GPU memory issues with attention, or need faster inference. Supports PyTorch native SDPA, flash-attn library, H100 FP8, and sliding window attention.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/flash-attention`  
Path| `optional-skills/mlops/flash-attention`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `flash-attn`, `torch`, `transformers`  
Tags| `Optimization`, `Flash Attention`, `Attention Optimization`, `Memory Efficiency`, `Speed Optimization`, `Long Context`, `PyTorch`, `SDPA`, `H100`, `FP8`, `Transformers`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Flash Attention - Fast Memory-Efficient Attention
## Quick start[​](<#quick-start> "Direct link to Quick start")
Flash Attention provides 2-4x speedup and 10-20x memory reduction for transformer attention through IO-aware tiling and recomputation.
**PyTorch native (easiest, PyTorch 2.2+)** :
[code] 
    import torch  
    import torch.nn.functional as F  
      
    q = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  # [batch, heads, seq, dim]  
    k = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  
    v = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  
      
    # Automatically uses Flash Attention if available  
    out = F.scaled_dot_product_attention(q, k, v)  
    
[/code]
**flash-attn library (more features)** :
[code] 
    pip install flash-attn --no-build-isolation  
    
[/code]
[code] 
    from flash_attn import flash_attn_func  
      
    # q, k, v: [batch, seqlen, nheads, headdim]  
    out = flash_attn_func(q, k, v, dropout_p=0.0, causal=True)  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: Enable in existing PyTorch model[​](<#workflow-1-enable-in-existing-pytorch-model> "Direct link to Workflow 1: Enable in existing PyTorch model")
Copy this checklist:
[code] 
    Flash Attention Integration:  
    - [ ] Step 1: Check PyTorch version (≥2.2)  
    - [ ] Step 2: Enable Flash Attention backend  
    - [ ] Step 3: Verify speedup with profiling  
    - [ ] Step 4: Test accuracy matches baseline  
    
[/code]
**Step 1: Check PyTorch version**
[code] 
    python -c "import torch; print(torch.__version__)"  
    # Should be ≥2.2.0  
    
[/code]
If <2.2, upgrade:
[code] 
    pip install --upgrade torch  
    
[/code]
**Step 2: Enable Flash Attention backend**
Replace standard attention:
[code] 
    # Before (standard attention)  
    attn_weights = torch.softmax(q @ k.transpose(-2, -1) / math.sqrt(d_k), dim=-1)  
    out = attn_weights @ v  
      
    # After (Flash Attention)  
    import torch.nn.functional as F  
    out = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)  
    
[/code]
Force Flash Attention backend:
[code] 
    with torch.backends.cuda.sdp_kernel(  
        enable_flash=True,  
        enable_math=False,  
        enable_mem_efficient=False  
    ):  
        out = F.scaled_dot_product_attention(q, k, v)  
    
[/code]
**Step 3: Verify speedup with profiling**
[code] 
    import torch.utils.benchmark as benchmark  
      
    def test_attention(use_flash):  
        q, k, v = [torch.randn(2, 8, 2048, 64, device='cuda', dtype=torch.float16) for _ in range(3)]  
      
        if use_flash:  
            with torch.backends.cuda.sdp_kernel(enable_flash=True):  
                return F.scaled_dot_product_attention(q, k, v)  
        else:  
            attn = (q @ k.transpose(-2, -1) / 8.0).softmax(dim=-1)  
            return attn @ v  
      
    # Benchmark  
    t_flash = benchmark.Timer(stmt='test_attention(True)', globals=globals())  
    t_standard = benchmark.Timer(stmt='test_attention(False)', globals=globals())  
      
    print(f"Flash: {t_flash.timeit(100).mean:.3f}s")  
    print(f"Standard: {t_standard.timeit(100).mean:.3f}s")  
    
[/code]
Expected: 2-4x speedup for sequences >512 tokens.
**Step 4: Test accuracy matches baseline**
[code] 
    # Compare outputs  
    q, k, v = [torch.randn(1, 8, 512, 64, device='cuda', dtype=torch.float16) for _ in range(3)]  
      
    # Flash Attention  
    out_flash = F.scaled_dot_product_attention(q, k, v)  
      
    # Standard attention  
    attn_weights = torch.softmax(q @ k.transpose(-2, -1) / 8.0, dim=-1)  
    out_standard = attn_weights @ v  
      
    # Check difference  
    diff = (out_flash - out_standard).abs().max()  
    print(f"Max difference: {diff:.6f}")  
    # Should be <1e-3 for float16  
    
[/code]
### Workflow 2: Use flash-attn library for advanced features[​](<#workflow-2-use-flash-attn-library-for-advanced-features> "Direct link to Workflow 2: Use flash-attn library for advanced features")
For multi-query attention, sliding window, or H100 FP8.
Copy this checklist:
[code] 
    flash-attn Library Setup:  
    - [ ] Step 1: Install flash-attn library  
    - [ ] Step 2: Modify attention code  
    - [ ] Step 3: Enable advanced features  
    - [ ] Step 4: Benchmark performance  
    
[/code]
**Step 1: Install flash-attn library**
[code] 
    # NVIDIA GPUs (CUDA 12.0+)  
    pip install flash-attn --no-build-isolation  
      
    # Verify installation  
    python -c "from flash_attn import flash_attn_func; print('Success')"  
    
[/code]
**Step 2: Modify attention code**
[code] 
    from flash_attn import flash_attn_func  
      
    # Input: [batch_size, seq_len, num_heads, head_dim]  
    # Transpose from [batch, heads, seq, dim] if needed  
    q = q.transpose(1, 2)  # [batch, seq, heads, dim]  
    k = k.transpose(1, 2)  
    v = v.transpose(1, 2)  
      
    out = flash_attn_func(  
        q, k, v,  
        dropout_p=0.1,  
        causal=True,  # For autoregressive models  
        window_size=(-1, -1),  # No sliding window  
        softmax_scale=None  # Auto-scale  
    )  
      
    out = out.transpose(1, 2)  # Back to [batch, heads, seq, dim]  
    
[/code]
**Step 3: Enable advanced features**
Multi-query attention (shared K/V across heads):
[code] 
    from flash_attn import flash_attn_func  
      
    # q: [batch, seq, num_q_heads, dim]  
    # k, v: [batch, seq, num_kv_heads, dim]  # Fewer KV heads  
    out = flash_attn_func(q, k, v)  # Automatically handles MQA  
    
[/code]
Sliding window attention (local attention):
[code] 
    # Only attend to window of 256 tokens before/after  
    out = flash_attn_func(  
        q, k, v,  
        window_size=(256, 256),  # (left, right) window  
        causal=True  
    )  
    
[/code]
**Step 4: Benchmark performance**
[code] 
    import torch  
    from flash_attn import flash_attn_func  
    import time  
      
    q, k, v = [torch.randn(4, 4096, 32, 64, device='cuda', dtype=torch.float16) for _ in range(3)]  
      
    # Warmup  
    for _ in range(10):  
        _ = flash_attn_func(q, k, v)  
      
    # Benchmark  
    torch.cuda.synchronize()  
    start = time.time()  
    for _ in range(100):  
        out = flash_attn_func(q, k, v)  
        torch.cuda.synchronize()  
    end = time.time()  
      
    print(f"Time per iteration: {(end-start)/100*1000:.2f}ms")  
    print(f"Memory allocated: {torch.cuda.max_memory_allocated()/1e9:.2f}GB")  
    
[/code]
### Workflow 3: H100 FP8 optimization (FlashAttention-3)[​](<#workflow-3-h100-fp8-optimization-flashattention-3> "Direct link to Workflow 3: H100 FP8 optimization \(FlashAttention-3\)")
For maximum performance on H100 GPUs.
[code] 
    FP8 Setup:  
    - [ ] Step 1: Verify H100 GPU available  
    - [ ] Step 2: Install flash-attn with FP8 support  
    - [ ] Step 3: Convert inputs to FP8  
    - [ ] Step 4: Run with FP8 attention  
    
[/code]
**Step 1: Verify H100 GPU**
[code] 
    nvidia-smi --query-gpu=name --format=csv  
    # Should show "H100" or "H800"  
    
[/code]
**Step 2: Install flash-attn with FP8 support**
[code] 
    pip install flash-attn --no-build-isolation  
    # FP8 support included for H100  
    
[/code]
**Step 3: Convert inputs to FP8**
[code] 
    import torch  
      
    q = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)  
    k = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)  
    v = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)  
      
    # Convert to float8_e4m3 (FP8)  
    q_fp8 = q.to(torch.float8_e4m3fn)  
    k_fp8 = k.to(torch.float8_e4m3fn)  
    v_fp8 = v.to(torch.float8_e4m3fn)  
    
[/code]
**Step 4: Run with FP8 attention**
[code] 
    from flash_attn import flash_attn_func  
      
    # FlashAttention-3 automatically uses FP8 kernels on H100  
    out = flash_attn_func(q_fp8, k_fp8, v_fp8)  
    # Result: ~1.2 PFLOPS, 1.5-2x faster than FP16  
    
[/code]
## When to use vs alternatives[​](<#when-to-use-vs-alternatives> "Direct link to When to use vs alternatives")
**Use Flash Attention when:**
  * Training transformers with sequences >512 tokens
  * Running inference with long context (>2K tokens)
  * GPU memory constrained (OOM with standard attention)
  * Need 2-4x speedup without accuracy loss
  * Using PyTorch 2.2+ or can install flash-attn


**Use alternatives instead:**
  * **Standard attention** : Sequences <256 tokens (overhead not worth it)
  * **xFormers** : Need more attention variants (not just speed)
  * **Memory-efficient attention** : CPU inference (Flash Attention needs GPU)


## Common issues[​](<#common-issues> "Direct link to Common issues")
**Issue: ImportError: cannot import flash_attn**
Install with no-build-isolation flag:
[code] 
    pip install flash-attn --no-build-isolation  
    
[/code]
Or install CUDA toolkit first:
[code] 
    conda install cuda -c nvidia  
    pip install flash-attn --no-build-isolation  
    
[/code]
**Issue: Slower than expected (no speedup)**
Flash Attention benefits increase with sequence length:
  * <512 tokens: Minimal speedup (10-20%)
  * 512-2K tokens: 2-3x speedup
  * > 2K tokens: 3-4x speedup


Check sequence length is sufficient.
**Issue: RuntimeError: CUDA error**
Verify GPU supports Flash Attention:
[code] 
    import torch  
    print(torch.cuda.get_device_capability())  
    # Should be ≥(7, 5) for Turing+  
    
[/code]
Flash Attention requires:
  * Ampere (A100, A10): ✅ Full support
  * Turing (T4): ✅ Supported
  * Volta (V100): ❌ Not supported


**Issue: Accuracy degradation**
Check dtype is float16 or bfloat16 (not float32):
[code] 
    q = q.to(torch.float16)  # Or torch.bfloat16  
    
[/code]
Flash Attention uses float16/bfloat16 for speed. Float32 not supported.
## Advanced topics[​](<#advanced-topics> "Direct link to Advanced topics")
**Integration with HuggingFace Transformers** : See [references/transformers-integration.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/flash-attention/references/transformers-integration.md>) for enabling Flash Attention in BERT, GPT, Llama models.
**Performance benchmarks** : See [references/benchmarks.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/flash-attention/references/benchmarks.md>) for detailed speed and memory comparisons across GPUs and sequence lengths.
## Hardware requirements[​](<#hardware-requirements> "Direct link to Hardware requirements")
  * **GPU** : NVIDIA Ampere+ (A100, A10, A30) or AMD MI200+
  * **VRAM** : Same as standard attention (Flash Attention doesn't increase memory)
  * **CUDA** : 12.0+ (11.8 minimum)
  * **PyTorch** : 2.2+ for native support


**Not supported** : V100 (Volta), CPU inference
## Resources[​](<#resources> "Direct link to Resources")
  * Paper: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness" (NeurIPS 2022)
  * Paper: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning" (ICLR 2024)
  * Blog: <https://tridao.me/blog/2024/flash3/>
  * GitHub: <https://github.com/Dao-AILab/flash-attention>
  * PyTorch docs: <https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Quick start](<#quick-start>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: Enable in existing PyTorch model](<#workflow-1-enable-in-existing-pytorch-model>)
    * [Workflow 2: Use flash-attn library for advanced features](<#workflow-2-use-flash-attn-library-for-advanced-features>)
    * [Workflow 3: H100 FP8 optimization (FlashAttention-3)](<#workflow-3-h100-fp8-optimization-flashattention-3>)
  * [When to use vs alternatives](<#when-to-use-vs-alternatives>)
  * [Common issues](<#common-issues>)
  * [Advanced topics](<#advanced-topics>)
  * [Hardware requirements](<#hardware-requirements>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-flash-attention -->
