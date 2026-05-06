On this page
Оптимизирует внимание трансформеров с помощью Flash Attention для ускорения в 2-4 раза и уменьшения потребления памяти в 10-20 раз. Используйте при обучении/запуске трансформеров с длинными последовательностями (>512 токенов), при проблемах с памятью GPU в механизме внимания или когда нужен более быстрый инференс. Поддерживает нативный PyTorch SDPA, библиотеку flash-attn, H100 FP8 и скользящее окно внимания.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на метаданные скилла")
|   |
|---|---|
|Source| Optional — install with `hermes skills install official/mlops/flash-attention` |
|Path| `optional-skills/mlops/flash-attention` |
|Version| `1.0.0` |
|Author| Orchestra Research |
|License| MIT |
|Dependencies| `flash-attn`, `torch`, `transformers` |
|Tags| `Optimization`, `Flash Attention`, `Attention Optimization`, `Memory Efficiency`, `Speed Optimization`, `Long Context`, `PyTorch`, `SDPA`, `H100`, `FP8`, `Transformers` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Flash Attention - Fast Memory-Efficient Attention
## Quick start[​](<#quick-start> "Прямая ссылка на Quick start")
Flash Attention обеспечивает ускорение в 2-4 раза и уменьшение потребления памяти в 10-20 раз для механизма внимания трансформеров за счёт IO-осведомлённого разбиения на плитки и перевычисления.
**PyTorch нативный (проще всего, PyTorch 2.2+)** :
[code] 
    import torch  
    import torch.nn.functional as F  
      
    q = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  # [batch, heads, seq, dim]  
    k = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  
    v = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  
      
    # Automatically uses Flash Attention if available  
    out = F.scaled_dot_product_attention(q, k, v)  
    
[/code]
**Библиотека flash-attn (больше возможностей)** :
[code] 
    pip install flash-attn --no-build-isolation  
    
[/code]
[code] 
    from flash_attn import flash_attn_func  
      
    # q, k, v: [batch, seqlen, nheads, headdim]  
    out = flash_attn_func(q, k, v, dropout_p=0.0, causal=True)  
    
[/code]
## Common workflows[​](<#common-workflows> "Прямая ссылка на Common workflows")
### Workflow 1: Enable in existing PyTorch model[​](<#workflow-1-enable-in-existing-pytorch-model> "Прямая ссылка на Workflow 1: Enable in existing PyTorch model")
Скопируйте этот чеклист:
[code] 
    Flash Attention Integration:  
    - [ ] Step 1: Check PyTorch version (≥2.2)  
    - [ ] Step 2: Enable Flash Attention backend  
    - [ ] Step 3: Verify speedup with profiling  
    - [ ] Step 4: Test accuracy matches baseline  
    
[/code]
**Шаг 1: Проверьте версию PyTorch**
[code] 
    python -c "import torch; print(torch.__version__)"  
    # Should be ≥2.2.0  
    
[/code]
Если <2.2, обновите:
[code] 
    pip install --upgrade torch  
    
[/code]
**Шаг 2: Включите бэкенд Flash Attention**
Замените стандартное внимание:
[code] 
    # Before (standard attention)  
    attn_weights = torch.softmax(q @ k.transpose(-2, -1) / math.sqrt(d_k), dim=-1)  
    out = attn_weights @ v  
      
    # After (Flash Attention)  
    import torch.nn.functional as F  
    out = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)  
    
[/code]
Принудительное использование бэкенда Flash Attention:
[code] 
    with torch.backends.cuda.sdp_kernel(  
        enable_flash=True,  
        enable_math=False,  
        enable_mem_efficient=False  
    ):  
        out = F.scaled_dot_product_attention(q, k, v)  
    
[/code]
**Шаг 3: Проверьте ускорение с помощью профилирования**
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
Ожидается: ускорение в 2-4 раза для последовательностей >512 токенов.
**Шаг 4: Проверьте, что точность совпадает с эталоном**
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
### Workflow 2: Use flash-attn library for advanced features[​](<#workflow-2-use-flash-attn-library-for-advanced-features> "Прямая ссылка на Workflow 2: Use flash-attn library for advanced features")
Для multi-query attention, скользящего окна или H100 FP8.
Скопируйте этот чеклист:
[code] 
    flash-attn Library Setup:  
    - [ ] Step 1: Install flash-attn library  
    - [ ] Step 2: Modify attention code  
    - [ ] Step 3: Enable advanced features  
    - [ ] Step 4: Benchmark performance  
    
[/code]
**Шаг 1: Установите библиотеку flash-attn**
[code] 
    # NVIDIA GPUs (CUDA 12.0+)  
    pip install flash-attn --no-build-isolation  
      
    # Verify installation  
    python -c "from flash_attn import flash_attn_func; print('Success')"  
    
[/code]
**Шаг 2: Измените код внимания**
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
**Шаг 3: Включите продвинутые возможности**
Multi-query attention (общие K/V для всех голов):
[code] 
    from flash_attn import flash_attn_func  
      
    # q: [batch, seq, num_q_heads, dim]  
    # k, v: [batch, seq, num_kv_heads, dim]  # Fewer KV heads  
    out = flash_attn_func(q, k, v)  # Automatically handles MQA  
    
[/code]
Скользящее окно внимания (локальное внимание):
[code] 
    # Only attend to window of 256 tokens before/after  
    out = flash_attn_func(  
        q, k, v,  
        window_size=(256, 256),  # (left, right) window  
        causal=True  
    )  
    
[/code]
**Шаг 4: Сравните производительность**
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
### Workflow 3: H100 FP8 optimization (FlashAttention-3)[​](<#workflow-3-h100-fp8-optimization-flashattention-3> "Прямая ссылка на Workflow 3: H100 FP8 optimization \\(FlashAttention-3\\)")
Для максимальной производительности на GPU H100.
[code] 
    FP8 Setup:  
    - [ ] Step 1: Verify H100 GPU available  
    - [ ] Step 2: Install flash-attn with FP8 support  
    - [ ] Step 3: Convert inputs to FP8  
    - [ ] Step 4: Run with FP8 attention  
    
[/code]
**Шаг 1: Проверьте GPU H100**
[code] 
    nvidia-smi --query-gpu=name --format=csv  
    # Should show "H100" or "H800"  
    
[/code]
**Шаг 2: Установите flash-attn с поддержкой FP8**
[code] 
    pip install flash-attn --no-build-isolation  
    # FP8 support included for H100  
    
[/code]
**Шаг 3: Преобразуйте входные данные в FP8**
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
**Шаг 4: Запустите с FP8 вниманием**
[code] 
    from flash_attn import flash_attn_func  
      
    # FlashAttention-3 automatically uses FP8 kernels on H100  
    out = flash_attn_func(q_fp8, k_fp8, v_fp8)  
    # Result: ~1.2 PFLOPS, 1.5-2x faster than FP16  
    
[/code]
## When to use vs alternatives[​](<#when-to-use-vs-alternatives> "Прямая ссылка на When to use vs alternatives")
**Используйте Flash Attention когда:**
  * Обучаете трансформеры с последовательностями >512 токенов
  * Запускаете инференс с длинным контекстом (>2K токенов)
  * Память GPU ограничена (OOM при стандартном внимании)
  * Нужно ускорение в 2-4 раза без потери точности
  * Используете PyTorch 2.2+ или можете установить flash-attn


**Используйте альтернативы вместо:**
  * **Стандартное внимание** : Последовательности <256 токенов (оверхед не оправдан)
  * **xFormers** : Нужно больше вариантов внимания (не только скорость)
  * **Memory-efficient attention** : Инференс на CPU (Flash Attention требует GPU)


## Common issues[​](<#common-issues> "Прямая ссылка на Common issues")
**Проблема: ImportError: cannot import flash_attn**
Установите с флагом no-build-isolation:
[code] 
    pip install flash-attn --no-build-isolation  
    
[/code]
Или сначала установите CUDA toolkit:
[code] 
    conda install cuda -c nvidia  
    pip install flash-attn --no-build-isolation  
    
[/code]
**Проблема: Медленнее, чем ожидалось (нет ускорения)**
Преимущества Flash Attention растут с длиной последовательности:
  * <512 токенов: Минимальное ускорение (10-20%)
  * 512-2K токенов: Ускорение в 2-3 раза
  * >2K токенов: Ускорение в 3-4 раза


Убедитесь, что длина последовательности достаточна.
**Проблема: RuntimeError: CUDA error**
Проверьте, что GPU поддерживает Flash Attention:
[code] 
    import torch  
    print(torch.cuda.get_device_capability())  
    # Should be ≥(7, 5) for Turing+  
    
[/code]
Flash Attention требует:
  * Ampere (A100, A10): ✅ Полная поддержка
  * Turing (T4): ✅ Поддерживается
  * Volta (V100): ❌ Не поддерживается


**Проблема: Снижение точности**
Проверьте, что dtype установлен в float16 или bfloat16 (не float32):
[code] 
    q = q.to(torch.float16)  # Or torch.bfloat16  
    
[/code]
Flash Attention использует float16/bfloat16 для скорости. Float32 не поддерживается.
## Advanced topics[​](<#advanced-topics> "Прямая ссылка на Advanced topics")
**Интеграция с HuggingFace Transformers** : См. [references/transformers-integration.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/flash-attention/references/transformers-integration.md>) для включения Flash Attention в моделях BERT, GPT, Llama.
**Сравнение производительности** : См. [references/benchmarks.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/flash-attention/references/benchmarks.md>) для детального сравнения скорости и памяти на разных GPU и длинах последовательностей.
## Hardware requirements[​](<#hardware-requirements> "Прямая ссылка на Hardware requirements")
  * **GPU** : NVIDIA Ampere+ (A100, A10, A30) или AMD MI200+
  * **VRAM** : Как и для стандартного внимания (Flash Attention не увеличивает потребление памяти)
  * **CUDA** : 12.0+ (минимум 11.8)
  * **PyTorch** : 2.2+ для нативной поддержки


**Не поддерживается** : V100 (Volta), инференс на CPU
## Resources[​](<#resources> "Прямая ссылка на Resources")
  * Статья: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness" (NeurIPS 2022)
  * Статья: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning" (ICLR 2024)
  * Блог: <https://tridao.me/blog/2024/flash3/>
  * GitHub: <https://github.com/Dao-AILab/flash-attention>
  * Документация PyTorch: <https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html>


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
