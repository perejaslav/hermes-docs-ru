On this page

Оптимизирует инференс LLM с помощью NVIDIA TensorRT для максимальной пропускной способности и минимальной задержки. Используйте для продакшн-развёртывания на NVIDIA GPU (A100/H100), когда требуется в 10–100 раз более быстрый инференс по сравнению с PyTorch, или для обслуживания моделей с квантизацией (FP8/INT4), пакетной обработкой «на лету» (in-flight batching) и масштабированием на несколько GPU.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/mlops/tensorrt-llm` |
|Путь| `optional-skills/mlops/tensorrt-llm` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `tensorrt-llm`, `torch` |
|Теги| `Inference Serving`, `TensorRT-LLM`, `NVIDIA`, `Inference Optimization`, `High Throughput`, `Low Latency`, `Production`, `FP8`, `INT4`, `In-Flight Batching`, `Multi-GPU` |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

> **info**
> Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Агент видит эти инструкции, когда навык активен.

# TensorRT-LLM

Библиотека NVIDIA с открытым исходным кодом для оптимизации инференса LLM с производительностью передового уровня на GPU NVIDIA.

## Когда использовать TensorRT-LLM[​](<#when-to-use-tensorrt-llm> "Прямая ссылка на Когда использовать TensorRT-LLM")

**Используйте TensorRT-LLM если:**

* Развёртываете на NVIDIA GPU (A100, H100, GB200)
* Нужна максимальная пропускная способность (24 000+ токенов/сек на Llama 3)
* Требуется низкая задержка для приложений реального времени
* Работаете с квантизованными моделями (FP8, INT4, FP4)
* Масштабируетесь на несколько GPU или узлов

**Используйте vLLM вместо TensorRT-LLM если:**

* Нужна более простая настройка и Python-ориентированный API
* Хотите PagedAttention без компиляции TensorRT
* Работаете с AMD GPU или оборудованием не от NVIDIA

**Используйте llama.cpp вместо TensorRT-LLM если:**

* Развёртываете на CPU или Apple Silicon
* Нужно развёртывание на периферийных устройствах без NVIDIA GPU
* Хотите более простой формат квантизации GGUF

## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")

### Установка[​](<#installation> "Прямая ссылка на Установка")

[code]
    # Docker (рекомендуется)
    docker pull nvidia/tensorrt_llm:latest

    # pip install
    pip install tensorrt_llm==1.2.0rc3

    # Требуется CUDA 13.0.0, TensorRT 10.13.2, Python 3.10-3.12

[/code]

### Базовый инференс[​](<#basic-inference> "Прямая ссылка на Базовый инференс")

[code]
    from tensorrt_llm import LLM, SamplingParams

    # Инициализация модели
    llm = LLM(model="meta-llama/Meta-Llama-3-8B")

    # Настройка сэмплирования
    sampling_params = SamplingParams(
        max_tokens=100,
        temperature=0.7,
        top_p=0.9
    )

    # Генерация
    prompts = ["Explain quantum computing"]
    outputs = llm.generate(prompts, sampling_params)

    for output in outputs:
        print(output.text)

[/code]

### Запуск сервера с trtllm-serve[​](<#serving-with-trtllm-serve> "Прямая ссылка на Запуск сервера с trtllm-serve")

[code]
    # Запуск сервера (автоматическая загрузка и компиляция модели)
    trtllm-serve meta-llama/Meta-Llama-3-8B \
        --tp_size 4 \              # Tensor parallelism (4 GPU)
        --max_batch_size 256 \
        --max_num_tokens 4096

    # Запрос клиента
    curl -X POST http://localhost:8000/v1/chat/completions \
      -H "Content-Type: application/json" \
      -d '{
        "model": "meta-llama/Meta-Llama-3-8B",
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7,
        "max_tokens": 100
      }'

[/code]

## Ключевые возможности[​](<#key-features> "Прямая ссылка на Ключевые возможности")

### Оптимизация производительности[​](<#performance-optimizations> "Прямая ссылка на Оптимизация производительности")

* **Пакетная обработка «на лету» (In-flight batching)**: динамическое пакетирование во время генерации
* **Страничный KV-кэш (Paged KV cache)**: эффективное управление памятью
* **Flash Attention**: оптимизированные ядра внимания
* **Квантизация**: FP8, INT4, FP4 для ускорения инференса в 2–4 раза
* **CUDA graphs**: снижение накладных расходов на запуск ядер

### Параллелизм[​](<#parallelism> "Прямая ссылка на Параллелизм")

* **Тензорный параллелизм (TP)**: разделение модели между GPU
* **Конвейерный параллелизм (PP)**: послойное распределение
* **Экспертный параллелизм**: для моделей типа Mixture-of-Experts
* **Многоузловой**: масштабирование за пределы одной машины

### Расширенные возможности[​](<#advanced-features> "Прямая ссылка на Расширенные возможности")

* **Спекулятивное декодирование**: более быстрая генерация с моделями-черновиками
* **LoRA сервинг**: эффективное развёртывание нескольких адаптеров
* **Раздельный сервинг (Disaggregated serving)**: разделение префилла и генерации

## Типовые сценарии[​](<#common-patterns> "Прямая ссылка на Типовые сценарии")

### Квантизованная модель (FP8)[​](<#quantized-model-fp8> "Прямая ссылка на Квантизованная модель (FP8)")

[code]
    from tensorrt_llm import LLM

    # Загрузка FP8 квантизованной модели (в 2 раза быстрее, на 50% меньше памяти)
    llm = LLM(
        model="meta-llama/Meta-Llama-3-70B",
        dtype="fp8",
        max_num_tokens=8192
    )

    # Инференс как обычно
    outputs = llm.generate(["Summarize this article..."])

[/code]

### Многопроцессорное развёртывание (Multi-GPU)[​](<#multi-gpu-deployment> "Прямая ссылка на Многопроцессорное развёртывание (Multi-GPU)")

[code]
    # Тензорный параллелизм на 8 GPU
    llm = LLM(
        model="meta-llama/Meta-Llama-3-405B",
        tensor_parallel_size=8,
        dtype="fp8"
    )

[/code]

### Пакетный инференс[​](<#batch-inference> "Прямая ссылка на Пакетный инференс")

[code]
    # Эффективная обработка 100 промптов
    prompts = [f"Question {i}: ..." for i in range(100)]

    outputs = llm.generate(
        prompts,
        sampling_params=SamplingParams(max_tokens=200)
    )

    # Автоматическая пакетная обработка «на лету» для максимальной пропускной способности

[/code]

## Бенчмарки производительности[​](<#performance-benchmarks> "Прямая ссылка на Бенчмарки производительности")

**Meta Llama 3-8B** (H100 GPU):

* Пропускная способность: 24 000 токенов/сек
* Задержка: ~10 мс на токен
* По сравнению с PyTorch: **в 100× быстрее**

**Llama 3-70B** (8× A100 80GB):

* Квантизация FP8: в 2 раза быстрее FP16
* Память: снижение на 50% с FP8

## Поддерживаемые модели[​](<#supported-models> "Прямая ссылка на Поддерживаемые модели")

* **Семейство LLaMA**: Llama 2, Llama 3, CodeLlama
* **Семейство GPT**: GPT-2, GPT-J, GPT-NeoX
* **Qwen**: Qwen, Qwen2, QwQ
* **DeepSeek**: DeepSeek-V2, DeepSeek-V3
* **Mixtral**: Mixtral-8x7B, Mixtral-8x22B
* **Vision**: LLaVA, Phi-3-vision
* **100+ моделей** на HuggingFace

## Ссылки[​](<#references> "Прямая ссылка на Ссылки")

* **[Руководство по оптимизации](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/tensorrt-llm/references/optimization.md>)** — Квантизация, пакетирование, настройка KV-кэша
* **[Настройка Multi-GPU](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/tensorrt-llm/references/multi-gpu.md>)** — Тензорный/конвейерный параллелизм, несколько узлов
* **[Руководство по сервингу](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/tensorrt-llm/references/serving.md>)** — Продакшн-развёртывание, мониторинг, автоскалинг

## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")

* **Документация**: <https://nvidia.github.io/TensorRT-LLM/>
* **GitHub**: <https://github.com/NVIDIA/TensorRT-LLM>
* **Модели**: <https://huggingface.co/models?library=tensorrt_llm>

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Когда использовать TensorRT-LLM](<#when-to-use-tensorrt-llm>)
* [Быстрый старт](<#quick-start>)
  * [Установка](<#installation>)
  * [Базовый инференс](<#basic-inference>)
  * [Запуск сервера с trtllm-serve](<#serving-with-trtllm-serve>)
* [Ключевые возможности](<#key-features>)
  * [Оптимизация производительности](<#performance-optimizations>)
  * [Параллелизм](<#parallelism>)
  * [Расширенные возможности](<#advanced-features>)
* [Типовые сценарии](<#common-patterns>)
  * [Квантизованная модель (FP8)](<#quantized-model-fp8>)
  * [Многопроцессорное развёртывание (Multi-GPU)](<#multi-gpu-deployment>)
  * [Пакетный инференс](<#batch-inference>)
* [Бенчмарки производительности](<#performance-benchmarks>)
* [Поддерживаемые модели](<#supported-models>)
* [Ссылки](<#references>)
* [Ресурсы](<#resources>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-tensorrt-llm -->
