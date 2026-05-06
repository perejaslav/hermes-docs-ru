На этой странице
Обеспечивает нативное для PyTorch распределённое предварительное обучение LLM с использованием torchtitan и 4D-параллелизма (FSDP2, TP, PP, CP). Используйте при предварительном обучении Llama 3.1, DeepSeek V3 или пользовательских моделей в масштабе от 8 до 512+ GPU с Float8, torch.compile и распределёнными контрольными точками.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---|---  
|Источник| Опционально — установка с помощью `hermes skills install official/mlops/torchtitan`  
|Путь| `optional-skills/mlops/torchtitan`  
|Версия| `1.0.0`  
|Автор| Orchestra Research  
|Лицензия| MIT  
|Зависимости| `torch>=2.6.0`, `torchtitan>=0.2.0`, `torchao>=0.5.0`  
|Теги| `Model Architecture`, `Distributed Training`, `TorchTitan`, `FSDP2`, `Tensor Parallel`, `Pipeline Parallel`, `Context Parallel`, `Float8`, `Llama`, `Pretraining`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Агент видит эти инструкции, когда навык активен.
# TorchTitan — нативное распределённое предварительное обучение LLM на PyTorch
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
TorchTitan — это официальная платформа PyTorch для крупномасштабного предварительного обучения LLM с композируемым 4D-параллелизмом (FSDP2, TP, PP, CP), обеспечивающая ускорение более 65% по сравнению с базовыми решениями на GPU H100.
**Установка** :
[code] 
    # Из PyPI (стабильная версия)  
    pip install torchtitan  
      
    # Из исходников (новейшие функции, требует PyTorch nightly)  
    git clone https://github.com/pytorch/torchtitan  
    cd torchtitan  
    pip install -r requirements.txt  
    
[/code]
**Загрузка токенизатора** :
[code] 
    # Получите HF токен на https://huggingface.co/settings/tokens  
    python scripts/download_hf_assets.py --repo_id meta-llama/Llama-3.1-8B --assets tokenizer --hf_token=...  
    
[/code]
**Запуск обучения на 8 GPU** :
[code] 
    CONFIG_FILE="./torchtitan/models/llama3/train_configs/llama3_8b.toml" ./run_train.sh  
    
[/code]
## Типовые сценарии работы[​](<#common-workflows> "Прямая ссылка на Типовые сценарии работы")
### Сценарий 1: Предварительное обучение Llama 3.1 8B на одном узле[​](<#workflow-1-pretrain-llama-31-8b-on-single-node> "Прямая ссылка на Сценарий 1: Предварительное обучение Llama 3.1 8B на одном узле")
Скопируйте этот чек-лист:
[code] 
    Single Node Pretraining:  
    - [ ] Step 1: Download tokenizer  
    - [ ] Step 2: Configure training  
    - [ ] Step 3: Launch training  
    - [ ] Step 4: Monitor and checkpoint  
    
[/code]
**Шаг 1: Загрузка токенизатора**
[code] 
    python scripts/download_hf_assets.py \  
      --repo_id meta-llama/Llama-3.1-8B \  
      --assets tokenizer \  
      --hf_token=YOUR_HF_TOKEN  
    
[/code]
**Шаг 2: Настройка конфигурации обучения**
Создайте или отредактируйте TOML-конфиг:
[code] 
    # llama3_8b_custom.toml  
    [job]  
    dump_folder = "./outputs"  
    description = "Llama 3.1 8B training"  
      
    [model]  
    name = "llama3"  
    flavor = "8B"  
    hf_assets_path = "./assets/hf/Llama-3.1-8B"  
      
    [optimizer]  
    name = "AdamW"  
    lr = 3e-4  
      
    [lr_scheduler]  
    warmup_steps = 200  
      
    [training]  
    local_batch_size = 2  
    seq_len = 8192  
    max_norm = 1.0  
    steps = 1000  
    dataset = "c4"  
      
    [parallelism]  
    data_parallel_shard_degree = -1  # Use all GPUs for FSDP  
      
    [activation_checkpoint]  
    mode = "selective"  
    selective_ac_option = "op"  
      
    [checkpoint]  
    enable = true  
    folder = "checkpoint"  
    interval = 500  
    
[/code]
**Шаг 3: Запуск обучения**
[code] 
    # 8 GPUs on single node  
    CONFIG_FILE="./llama3_8b_custom.toml" ./run_train.sh  
      
    # Or explicitly with torchrun  
    torchrun --nproc_per_node=8 \  
      -m torchtitan.train \  
      --job.config_file ./llama3_8b_custom.toml  
    
[/code]
**Шаг 4: Мониторинг и контрольные точки**
Логи TensorBoard сохраняются в `./outputs/tb/`:
[code] 
    tensorboard --logdir ./outputs/tb  
    
[/code]
### Сценарий 2: Многоузловое обучение с SLURM[​](<#workflow-2-multi-node-training-with-slurm> "Прямая ссылка на Сценарий 2: Многоузловое обучение с SLURM")
[code] 
    Multi-Node Training:  
    - [ ] Step 1: Configure parallelism for scale  
    - [ ] Step 2: Set up SLURM script  
    - [ ] Step 3: Submit job  
    - [ ] Step 4: Resume from checkpoint  
    
[/code]
**Шаг 1: Настройка параллелизма для масштабирования**
Для модели 70B на 256 GPU (32 узла):
[code] 
    [parallelism]  
    data_parallel_shard_degree = 32  # FSDP across 32 ranks  
    tensor_parallel_degree = 8        # TP within node  
    pipeline_parallel_degree = 1      # No PP for 70B  
    context_parallel_degree = 1       # Increase for long sequences  
    
[/code]
**Шаг 2: Создание SLURM-скрипта**
[code] 
    #!/bin/bash  
    #SBATCH --job-name=llama70b  
    #SBATCH --nodes=32  
    #SBATCH --ntasks-per-node=8  
    #SBATCH --gpus-per-node=8  
      
    srun torchrun \  
      --nnodes=32 \  
      --nproc_per_node=8 \  
      --rdzv_backend=c10d \  
      --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \  
      -m torchtitan.train \  
      --job.config_file ./llama3_70b.toml  
    
[/code]
**Шаг 3: Отправка задания**
[code] 
    sbatch multinode_trainer.slurm  
    
[/code]
**Шаг 4: Возобновление из контрольной точки**
Обучение автоматически возобновляется, если контрольная точка существует в настроенной папке.
### Сценарий 3: Включение Float8 для H100[​](<#workflow-3-enable-float8-training-for-h100s> "Прямая ссылка на Сценарий 3: Включение Float8 для H100")
Float8 обеспечивает ускорение на 30-50% на GPU H100.
[code] 
    Float8 Training:  
    - [ ] Step 1: Install torchao  
    - [ ] Step 2: Configure Float8  
    - [ ] Step 3: Launch with compile  
    
[/code]
**Шаг 1: Установка torchao**
[code] 
    USE_CPP=0 pip install git+https://github.com/pytorch/ao.git  
    
[/code]
**Шаг 2: Настройка Float8**
Добавьте в ваш TOML-конфиг:
[code] 
    [model]  
    converters = ["quantize.linear.float8"]  
      
    [quantize.linear.float8]  
    enable_fsdp_float8_all_gather = true  
    precompute_float8_dynamic_scale_for_fsdp = true  
    filter_fqns = ["output"]  # Exclude output layer  
      
    [compile]  
    enable = true  
    components = ["model", "loss"]  
    
[/code]
**Шаг 3: Запуск с компиляцией**
[code] 
    CONFIG_FILE="./llama3_8b.toml" ./run_train.sh \  
      --model.converters="quantize.linear.float8" \  
      --quantize.linear.float8.enable_fsdp_float8_all_gather \  
      --compile.enable  
    
[/code]
### Сценарий 4: 4D-параллелизм для моделей 405B[​](<#workflow-4-4d-parallelism-for-405b-models> "Прямая ссылка на Сценарий 4: 4D-параллелизм для моделей 405B")
[code] 
    4D Parallelism (FSDP + TP + PP + CP):  
    - [ ] Step 1: Create seed checkpoint  
    - [ ] Step 2: Configure 4D parallelism  
    - [ ] Step 3: Launch on 512 GPUs  
    
[/code]
**Шаг 1: Создание начальной контрольной точки**
Необходимо для единообразной инициализации между стадиями PP:
[code] 
    NGPU=1 CONFIG_FILE=./llama3_405b.toml ./run_train.sh \  
      --checkpoint.enable \  
      --checkpoint.create_seed_checkpoint \  
      --parallelism.data_parallel_shard_degree 1 \  
      --parallelism.tensor_parallel_degree 1 \  
      --parallelism.pipeline_parallel_degree 1  
    
[/code]
**Шаг 2: Настройка 4D-параллелизма**
[code] 
    [parallelism]  
    data_parallel_shard_degree = 8   # FSDP  
    tensor_parallel_degree = 8       # TP within node  
    pipeline_parallel_degree = 8     # PP across nodes  
    context_parallel_degree = 1      # CP for long sequences  
      
    [training]  
    local_batch_size = 32  
    seq_len = 8192  
    
[/code]
**Шаг 3: Запуск на 512 GPU**
[code] 
    # 64 nodes x 8 GPUs = 512 GPUs  
    srun torchrun --nnodes=64 --nproc_per_node=8 \  
      -m torchtitan.train \  
      --job.config_file ./llama3_405b.toml  
    
[/code]
## Когда использовать и альтернативы[​](<#when-to-use-vs-alternatives> "Прямая ссылка на Когда использовать и альтернативы")
**Используйте TorchTitan когда:**
  * Выполняется предварительное обучение LLM с нуля (8B до 405B+)
  * Требуется нативное решение на PyTorch без сторонних зависимостей
  * Необходим композируемый 4D-параллелизм (FSDP2, TP, PP, CP)
  * Обучение на H100 с поддержкой Float8
  * Нужны совместимые контрольные точки с torchtune/HuggingFace


**Альтернативы:**
  * **Megatron-LM** : Максимальная производительность для развёртываний только на NVIDIA
  * **DeepSpeed** : Более широкая экосистема оптимизации ZeRO, поддержка инференса
  * **Axolotl/TRL** : Донастройка, а не предварительное обучение
  * **LitGPT** : Образовательные цели, обучение меньшего масштаба


## Часто встречающиеся проблемы[​](<#common-issues> "Прямая ссылка на Часто встречающиеся проблемы")
**Проблема: Нехватка памяти на больших моделях**
Включите активационное контрольное точки (activation checkpointing) и уменьшите размер батча:
[code] 
    [activation_checkpoint]  
    mode = "full"  # Instead of "selective"  
      
    [training]  
    local_batch_size = 1  
    
[/code]
Или используйте накопление градиентов:
[code] 
    [training]  
    local_batch_size = 1  
    global_batch_size = 32  # Accumulates gradients  
    
[/code]
**Проблема: TP вызывает высокое потребление памяти с асинхронными коллективными операциями**
Установите переменную окружения:
[code] 
    export TORCH_NCCL_AVOID_RECORD_STREAMS=1  
    
[/code]
**Проблема: Float8 не ускоряет обучение**
Float8 выгоден только для больших GEMM. Отфильтруйте маленькие слои:
[code] 
    [quantize.linear.float8]  
    filter_fqns = ["attention.wk", "attention.wv", "output", "auto_filter_small_kn"]  
    
[/code]
**Проблема: Загрузка контрольной точки не удаётся после изменения параллелизма**
Используйте возможность перешардирования DCP:
[code] 
    # Convert sharded checkpoint to single file  
    python -m torch.distributed.checkpoint.format_utils \  
      dcp_to_torch checkpoint/step-1000 checkpoint.pt  
    
[/code]
**Проблема: Инициализация конвейерного параллелизма**
Сначала создайте начальную контрольную точку (см. Сценарий 4, Шаг 1).
## Поддерживаемые модели[​](<#supported-models> "Прямая ссылка на Поддерживаемые модели")
Модель| Размеры| Статус  
|---|---|---  
Llama 3.1| 8B, 70B, 405B| Production  
Llama 4| Различные| Experimental  
DeepSeek V3| 16B, 236B, 671B (MoE)| Experimental  
GPT-OSS| 20B, 120B (MoE)| Experimental  
Qwen 3| Различные| Experimental  
Flux| Diffusion| Experimental  
## Бенчмарки производительности (H100)[​](<#performance-benchmarks-h100> "Прямая ссылка на Бенчмарки производительности \\(H100\\)")
Модель| GPU| Параллелизм| TPS/GPU| Техники  
|---|---|---|---|---  
Llama 8B| 8| FSDP| 5,762| Базовый  
Llama 8B| 8| FSDP+compile+FP8| 8,532| +48%  
Llama 70B| 256| FSDP+TP+AsyncTP| 876| 2D parallel  
Llama 405B| 512| FSDP+TP+PP| 128| 3D parallel  
## Продвинутые темы[​](<#advanced-topics> "Прямая ссылка на Продвинутые темы")
**Конфигурация FSDP2** : См. [references/fsdp.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/torchtitan/references/fsdp.md>) для подробного сравнения FSDP2 и FSDP1 и эквивалентов ZeRO.
**Float8 обучение** : См. [references/float8.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/torchtitan/references/float8.md>) для рецептов тензорного и построчного масштабирования.
**Контрольные точки** : См. [references/checkpoint.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/torchtitan/references/checkpoint.md>) для конвертации в HuggingFace и асинхронных контрольных точек.
**Добавление пользовательских моделей** : См. [references/custom-models.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/torchtitan/references/custom-models.md>) для протокола TrainSpec.
## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * GitHub: <https://github.com/pytorch/torchtitan>
  * Статья: <https://arxiv.org/abs/2410.06511>
  * ICLR 2025: <https://iclr.cc/virtual/2025/poster/29620>
  * PyTorch Forum: <https://discuss.pytorch.org/c/distributed/torchtitan/44>


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Быстрый старт](<#quick-start>)
  * [Типовые сценарии работы](<#common-workflows>)
    * [Сценарий 1: Предварительное обучение Llama 3.1 8B на одном узле](<#workflow-1-pretrain-llama-31-8b-on-single-node>)
    * [Сценарий 2: Многоузловое обучение с SLURM](<#workflow-2-multi-node-training-with-slurm>)
    * [Сценарий 3: Включение Float8 для H100](<#workflow-3-enable-float8-training-for-h100s>)
    * [Сценарий 4: 4D-параллелизм для моделей 405B](<#workflow-4-4d-parallelism-for-405b-models>)
  * [Когда использовать и альтернативы](<#when-to-use-vs-alternatives>)
  * [Часто встречающиеся проблемы](<#common-issues>)
  * [Поддерживаемые модели](<#supported-models>)
  * [Бенчмарки производительности (H100)](<#performance-benchmarks-h100>)
  * [Продвинутые темы](<#advanced-topics>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-torchtitan -->
