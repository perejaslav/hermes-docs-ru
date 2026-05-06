На этой странице
vLLM: высокопроизводительный LLM-сервинг, OpenAI-совместимый API, квантование.
## Метаданные навыка[​](#skill-metadata "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Встроенный (установлен по умолчанию)|
|Путь| `skills/mlops/inference/vllm`|
|Версия| `1.0.0`|
|Автор| Orchestra Research|
|Лицензия| MIT|
|Зависимости| `vllm`, `torch`, `transformers`|
|Теги| `vLLM`, `Inference Serving`, `PagedAttention`, `Continuous Batching`, `High Throughput`, `Production`, `OpenAI API`, `Quantization`, `Tensor Parallelism`|
## Справочник: полный SKILL.md[​](#reference-full-skillmd "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# vLLM — высокопроизводительный LLM-сервинг
## Когда использовать[​](#when-to-use "Прямая ссылка на Когда использовать")
Используйте при развёртывании production LLM API, оптимизации задержки/пропускной способности инференса или обслуживании моделей с ограниченной видеопамятью. Поддерживает OpenAI-совместимые конечные точки, квантование (GPTQ/AWQ/FP8) и тензорный параллелизм.
## Быстрый старт[​](#quick-start "Прямая ссылка на Быстрый старт")
vLLM обеспечивает в 24 раза большую пропускную способность по сравнению со стандартными трансформерами благодаря PagedAttention (KV-кэш на основе блоков) и непрерывному пакетированию (смешивание запросов prefill/decode).
**Установка**:
[code]
    pip install vllm
    
[/code]
**Базовый офлайн-инференс**:
[code]
    from vllm import LLM, SamplingParams
    
    llm = LLM(model="meta-llama/Llama-3-8B-Instruct")
    sampling = SamplingParams(temperature=0.7, max_tokens=256)
    
    outputs = llm.generate(["Explain quantum computing"], sampling)
    print(outputs[0].outputs[0].text)
    
[/code]
**OpenAI-совместимый сервер**:
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
## Типовые сценарии[​](#common-workflows "Прямая ссылка на Типовые сценарии")
### Сценарий 1. Развёртывание production API[​](#workflow-1-production-api-deployment "Прямая ссылка на Сценарий 1. Развёртывание production API")
Скопируйте этот чеклист и отслеживайте прогресс:
[code]
    Deployment Progress:
    - [ ] Step 1: Configure server settings
    - [ ] Step 2: Test with limited traffic
    - [ ] Step 3: Enable monitoring
    - [ ] Step 4: Deploy to production
    - [ ] Step 5: Verify performance metrics
    
[/code]
**Шаг 1. Настройка параметров сервера**
Выберите конфигурацию в зависимости от размера модели:
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
**Шаг 2. Тестирование с ограниченным трафиком**
Запустите нагрузочное тестирование перед выходом в production:
[code]
    # Install load testing tool
    pip install locust
    
    # Create test_load.py with sample requests
    # Run: locust -f test_load.py --host http://localhost:8000
    
[/code]
Проверьте TTFT (время до первого токена) < 500 мс и пропускную способность > 100 запросов/сек.
**Шаг 3. Включение мониторинга**
vLLM предоставляет метрики Prometheus на порту 9090:
[code]
    curl http://localhost:9090/metrics | grep vllm
    
[/code]
Ключевые метрики для отслеживания:
  * `vllm:time_to_first_token_seconds` — задержка
  * `vllm:num_requests_running` — активные запросы
  * `vllm:gpu_cache_usage_perc` — использование KV-кэша


**Шаг 4. Развёртывание в production**
Используйте Docker для единообразного развёртывания:
[code]
    # Run vLLM in Docker
    docker run --gpus all -p 8000:8000 \
      vllm/vllm-openai:latest \
      --model meta-llama/Llama-3-8B-Instruct \
      --gpu-memory-utilization 0.9 \
      --enable-prefix-caching
    
[/code]
**Шаг 5. Проверка метрик производительности**
Убедитесь, что развёртывание соответствует целям:
  * TTFT < 500 мс (для коротких промптов)
  * Пропускная способность > целевого значения запросов/сек
  * Загрузка GPU > 80%
  * Отсутствие ошибок OOM в логах


### Сценарий 2. Пакетный офлайн-инференс[​](#workflow-2-offline-batch-inference "Прямая ссылка на Сценарий 2. Пакетный офлайн-инференс")
Для обработки больших наборов данных без накладных расходов на сервер.
Скопируйте этот чеклист:
[code]
    Batch Processing:
    - [ ] Step 1: Prepare input data
    - [ ] Step 2: Configure LLM engine
    - [ ] Step 3: Run batch inference
    - [ ] Step 4: Process results
    
[/code]
**Шаг 1. Подготовка входных данных**
[code]
    # Load prompts from file
    prompts = []
    with open("prompts.txt") as f:
        prompts = [line.strip() for line in f]
    
    print(f"Loaded {len(prompts)} prompts")
    
[/code]
**Шаг 2. Настройка LLM-движка**
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
**Шаг 3. Запуск пакетного инференса**
vLLM автоматически группирует запросы для эффективности:
[code]
    # Process all prompts in one call
    outputs = llm.generate(prompts, sampling)
    
    # vLLM handles batching internally
    # No need to manually chunk prompts
    
[/code]
**Шаг 4. Обработка результатов**
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
### Сценарий 3. Обслуживание квантованных моделей[​](#workflow-3-quantized-model-serving "Прямая ссылка на Сценарий 3. Обслуживание квантованных моделей")
Размещение больших моделей в ограниченной видеопамяти.
[code]
    Quantization Setup:
    - [ ] Step 1: Choose quantization method
    - [ ] Step 2: Find or create quantized model
    - [ ] Step 3: Launch with quantization flag
    - [ ] Step 4: Verify accuracy
    
[/code]
**Шаг 1. Выбор метода квантования**
  * **AWQ**: лучшее решение для моделей 70B, минимальная потеря точности
  * **GPTQ**: широкая поддержка моделей, хорошее сжатие
  * **FP8**: самый быстрый на GPU H100


**Шаг 2. Поиск или создание квантованной модели**
Используйте предварительно квантованные модели с HuggingFace:
[code]
    # Search for AWQ models
    # Example: TheBloke/Llama-2-70B-AWQ
    
[/code]
**Шаг 3. Запуск с флагом квантования**
[code]
    # Using pre-quantized model
    vllm serve TheBloke/Llama-2-70B-AWQ \
      --quantization awq \
      --tensor-parallel-size 1 \
      --gpu-memory-utilization 0.95
    
    # Results: 70B model in ~40GB VRAM
    
[/code]
**Шаг 4. Проверка точности**
Проверьте, что выходные данные соответствуют ожидаемому качеству:
[code]
    # Compare quantized vs non-quantized responses
    # Verify task-specific performance unchanged
    
[/code]
## Когда использовать vs альтернативы[​](#when-to-use-vs-alternatives "Прямая ссылка на Когда использовать vs альтернативы")
**Используйте vLLM, когда:**
  * Развёртываете production LLM API (100+ запросов/сек)
  * Нужны OpenAI-совместимые конечные точки
  * Ограниченная видеопамять, но нужны большие модели
  * Многопользовательские приложения (чат-боты, ассистенты)
  * Нужна низкая задержка при высокой пропускной способности


**Используйте альтернативы:**
  * **llama.cpp**: CPU/периферийный инференс, однопользовательский режим
  * **HuggingFace transformers**: исследования, прототипирование, разовая генерация
  * **TensorRT-LLM**: только NVIDIA, нужна максимальная производительность
  * **Text-Generation-Inference**: если уже в экосистеме HuggingFace


## Типичные проблемы[​](#common-issues "Прямая ссылка на Типичные проблемы")
**Проблема: нехватка памяти при загрузке модели**
Уменьшите использование памяти:
[code]
    vllm serve MODEL \
      --gpu-memory-utilization 0.7 \
      --max-model-len 4096
    
[/code]
Или используйте квантование:
[code]
    vllm serve MODEL --quantization awq
    
[/code]
**Проблема: медленный первый токен (TTFT > 1 секунда)**
Включите кэширование префиксов для повторяющихся промптов:
[code]
    vllm serve MODEL --enable-prefix-caching
    
[/code]
Для длинных промптов включите чанковый prefill:
[code]
    vllm serve MODEL --enable-chunked-prefill
    
[/code]
**Проблема: ошибка «Модель не найдена»**
Используйте `--trust-remote-code` для кастомных моделей:
[code]
    vllm serve MODEL --trust-remote-code
    
[/code]
**Проблема: низкая пропускная способность (<50 запросов/сек)**
Увеличьте количество конкурентных последовательностей:
[code]
    vllm serve MODEL --max-num-seqs 512
    
[/code]
Проверьте загрузку GPU с помощью `nvidia-smi` — должно быть >80%.
**Проблема: инференс медленнее ожидаемого**
Убедитесь, что тензорный параллелизм использует количество GPU, кратное степени двойки:
[code]
    vllm serve MODEL --tensor-parallel-size 4  # Not 3
    
[/code]
Включите спекулятивную декодировку для более быстрой генерации:
[code]
    vllm serve MODEL --speculative-model DRAFT_MODEL
    
[/code]
## Продвинутые темы[​](#advanced-topics "Прямая ссылка на Продвинутые темы")
**Схемы развёртывания сервера**: см. [references/server-deployment.md](https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/server-deployment.md) для конфигураций Docker, Kubernetes и балансировки нагрузки.
**Оптимизация производительности**: см. [references/optimization.md](https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/optimization.md) для настройки PagedAttention, деталей непрерывного пакетирования и результатов бенчмарков.
**Руководство по квантованию**: см. [references/quantization.md](https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/quantization.md) для настройки AWQ/GPTQ/FP8, подготовки модели и сравнения точности.
**Устранение неполадок**: см. [references/troubleshooting.md](https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/vllm/references/troubleshooting.md) для подробных сообщений об ошибках, шагов отладки и диагностики производительности.
## Требования к оборудованию[​](#hardware-requirements "Прямая ссылка на Требования к оборудованию")
  * **Малые модели (7B-13B)**: 1x A10 (24 ГБ) или A100 (40 ГБ)
  * **Средние модели (30B-40B)**: 2x A100 (40 ГБ) с тензорным параллелизмом
  * **Крупные модели (70B+)**: 4x A100 (40 ГБ) или 2x A100 (80 ГБ), используйте AWQ/GPTQ


Поддерживаемые платформы: NVIDIA (основная), AMD ROCm, Intel GPU, TPU
## Ресурсы[​](#resources "Прямая ссылка на Ресурсы")
  * Официальная документация: <https://docs.vllm.ai>
  * GitHub: <https://github.com/vllm-project/vllm>
  * Статья: «Efficient Memory Management for Large Language Model Serving with PagedAttention» (SOSP 2023)
  * Сообщество: <https://discuss.vllm.ai>


  * [Метаданные навыка](#skill-metadata)
  * [Справочник: полный SKILL.md](#reference-full-skillmd)
  * [Когда использовать](#when-to-use)
  * [Быстрый старт](#quick-start)
  * [Типовые сценарии](#common-workflows)
    * [Сценарий 1. Развёртывание production API](#workflow-1-production-api-deployment)
    * [Сценарий 2. Пакетный офлайн-инференс](#workflow-2-offline-batch-inference)
    * [Сценарий 3. Обслуживание квантованных моделей](#workflow-3-quantized-model-serving)
  * [Когда использовать vs альтернативы](#when-to-use-vs-alternatives)
  * [Типичные проблемы](#common-issues)
  * [Продвинутые темы](#advanced-topics)
  * [Требования к оборудованию](#hardware-requirements)
  * [Ресурсы](#resources)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-inference-vllm -->
