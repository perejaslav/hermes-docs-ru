На этой странице
Простейший API для распределённого обучения. 4 строки для добавления поддержки распределённых вычислений в любой PyTorch-скрипт. Единый API для DeepSpeed/FSDP/Megatron/DDP. Автоматическое размещение устройств, смешанная точность (FP16/BF16/FP8). Интерактивная конфигурация, одна команда запуска. Стандарт экосистемы HuggingFace.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   
|---|---  
Источник| Опционально — установка: `hermes skills install official/mlops/accelerate`  
Путь| `optional-skills/mlops/accelerate`  
Версия| `1.0.0`  
Автор| Orchestra Research  
Лицензия| MIT  
Зависимости| `accelerate`, `torch`, `transformers`  
Теги| `Distributed Training`, `HuggingFace`, `Accelerate`, `DeepSpeed`, `FSDP`, `Mixed Precision`, `PyTorch`, `DDP`, `Unified API`, `Simple`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное описание навыка, которое загружает Hermes при его активации. Это то, что видит агент в качестве инструкций, когда навык активен.
# HuggingFace Accelerate — Единое распределённое обучение
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
Accelerate упрощает распределённое обучение до 4 строк кода.
**Установка**:
[code] 
    pip install accelerate  
    
[/code]
**Преобразование PyTorch-скрипта** (4 строки):
[code] 
    import torch  
    + from accelerate import Accelerator  
      
    + accelerator = Accelerator()  
      
      model = torch.nn.Transformer()  
      optimizer = torch.optim.Adam(model.parameters())  
      dataloader = torch.utils.data.DataLoader(dataset)  
      
    + model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  
      
      for batch in dataloader:  
          optimizer.zero_grad()  
          loss = model(batch)  
    -     loss.backward()  
    +     accelerator.backward(loss)  
          optimizer.step()  
    
[/code]
**Запуск** (одна команда):
[code] 
    accelerate launch train.py  
    
[/code]
## Типовые рабочие процессы[​](<#common-workflows> "Прямая ссылка на Типовые рабочие процессы")
### Рабочий процесс 1: От одного GPU к нескольким[​](<#workflow-1-from-single-gpu-to-multi-gpu> "Прямая ссылка на Рабочий процесс 1: От одного GPU к нескольким")
**Исходный скрипт**:
[code] 
    # train.py  
    import torch  
      
    model = torch.nn.Linear(10, 2).to('cuda')  
    optimizer = torch.optim.Adam(model.parameters())  
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)  
      
    for epoch in range(10):  
        for batch in dataloader:  
            batch = batch.to('cuda')  
            optimizer.zero_grad()  
            loss = model(batch).mean()  
            loss.backward()  
            optimizer.step()  
    
[/code]
**С Accelerate** (добавлено 4 строки):
[code] 
    # train.py  
    import torch  
    from accelerate import Accelerator  # +1  
      
    accelerator = Accelerator()  # +2  
      
    model = torch.nn.Linear(10, 2)  
    optimizer = torch.optim.Adam(model.parameters())  
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)  
      
    model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  # +3  
      
    for epoch in range(10):  
        for batch in dataloader:  
            # .to('cuda') больше не нужен — автоматически!  
            optimizer.zero_grad()  
            loss = model(batch).mean()  
            accelerator.backward(loss)  # +4  
            optimizer.step()  
    
[/code]
**Настройка** (интерактивно):
[code] 
    accelerate config  
    
[/code]
**Вопросы**:
  * Какая машина? (single/multi GPU/TPU/CPU)
  * Сколько машин? (1)
  * Смешанная точность? (no/fp16/bf16/fp8)
  * DeepSpeed? (no/yes)


**Запуск** (работает на любой конфигурации):
[code] 
    # Один GPU  
    accelerate launch train.py  
      
    # Несколько GPU (8 GPU)  
    accelerate launch --multi_gpu --num_processes 8 train.py  
      
    # Несколько узлов  
    accelerate launch --multi_gpu --num_processes 16 \\  
      --num_machines 2 --machine_rank 0 \\  
      --main_process_ip $MASTER_ADDR \\  
      train.py  
    
[/code]
### Рабочий процесс 2: Обучение со смешанной точностью[​](<#workflow-2-mixed-precision-training> "Прямая ссылка на Рабочий процесс 2: Обучение со смешанной точностью")
**Включение FP16/BF16**:
[code] 
    from accelerate import Accelerator  
      
    # FP16 (с масштабированием градиентов)  
    accelerator = Accelerator(mixed_precision='fp16')  
      
    # BF16 (без масштабирования, более стабильно)  
    accelerator = Accelerator(mixed_precision='bf16')  
      
    # FP8 (H100+)  
    accelerator = Accelerator(mixed_precision='fp8')  
      
    model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  
      
    # Всё остальное автоматически!  
    for batch in dataloader:  
        with accelerator.autocast():  # Опционально, делается автоматически  
            loss = model(batch)  
        accelerator.backward(loss)  
    
[/code]
### Рабочий процесс 3: Интеграция DeepSpeed ZeRO[​](<#workflow-3-deepspeed-zero-integration> "Прямая ссылка на Рабочий процесс 3: Интеграция DeepSpeed ZeRO")
**Включение DeepSpeed ZeRO-2**:
[code] 
    from accelerate import Accelerator  
      
    accelerator = Accelerator(  
        mixed_precision='bf16',  
        deepspeed_plugin={  
            "zero_stage": 2,  # ZeRO-2  
            "offload_optimizer": False,  
            "gradient_accumulation_steps": 4  
        }  
    )  
      
    # Тот же код, что и раньше!  
    model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  
    
[/code]
**Или через конфиг**:
[code] 
    accelerate config  
    # Выберите: DeepSpeed → ZeRO-2  
    
[/code]
**deepspeed_config.json**:
[code] 
    {  
        "fp16": {"enabled": false},  
        "bf16": {"enabled": true},  
        "zero_optimization": {  
            "stage": 2,  
            "offload_optimizer": {"device": "cpu"},  
            "allgather_bucket_size": 5e8,  
            "reduce_bucket_size": 5e8  
        }  
    }  
    
[/code]
**Запуск**:
[code] 
    accelerate launch --config_file deepspeed_config.json train.py  
    
[/code]
### Рабочий процесс 4: FSDP (Fully Sharded Data Parallel)[​](<#workflow-4-fsdp-fully-sharded-data-parallel> "Прямая ссылка на Рабочий процесс 4: FSDP (Fully Sharded Data Parallel)")
**Включение FSDP**:
[code] 
    from accelerate import Accelerator, FullyShardedDataParallelPlugin  
      
    fsdp_plugin = FullyShardedDataParallelPlugin(  
        sharding_strategy="FULL_SHARD",  # Эквивалент ZeRO-3  
        auto_wrap_policy="TRANSFORMER_AUTO_WRAP",  
        cpu_offload=False  
    )  
      
    accelerator = Accelerator(  
        mixed_precision='bf16',  
        fsdp_plugin=fsdp_plugin  
    )  
      
    model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  
    
[/code]
**Или через конфиг**:
[code] 
    accelerate config  
    # Выберите: FSDP → Full Shard → No CPU Offload  
    
[/code]
### Рабочий процесс 5: Накопление градиентов[​](<#workflow-5-gradient-accumulation> "Прямая ссылка на Рабочий процесс 5: Накопление градиентов")
**Накопление градиентов**:
[code] 
    from accelerate import Accelerator  
      
    accelerator = Accelerator(gradient_accumulation_steps=4)  
      
    model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)  
      
    for batch in dataloader:  
        with accelerator.accumulate(model):  # Управляет накоплением  
            optimizer.zero_grad()  
            loss = model(batch)  
            accelerator.backward(loss)  
            optimizer.step()  
    
[/code]
**Эффективный размер батча**: `batch_size * num_gpus * gradient_accumulation_steps`
## Когда использовать vs альтернативы[​](<#when-to-use-vs-alternatives> "Прямая ссылка на Когда использовать vs альтернативы")
**Используйте Accelerate, когда**:
  * Нужно простейшее распределённое обучение
  * Нужен единый скрипт для любого оборудования
  * Используете экосистему HuggingFace
  * Нужна гибкость (DDP/DeepSpeed/FSDP/Megatron)
  * Нужно быстрое прототипирование


**Ключевые преимущества**:
  * **4 строки**: Минимальные изменения кода
  * **Единый API**: Тот же код для DDP, DeepSpeed, FSDP, Megatron
  * **Автоматически**: Размещение устройств, смешанная точность, шардирование
  * **Интерактивный конфиг**: Без ручной настройки лаунчера
  * **Один запуск**: Работает везде


**Используйте альтернативы, если**:
  * **PyTorch Lightning**: Нужны колбэки, высокоуровневые абстракции
  * **Ray Train**: Оркестрация нескольких узлов, настройка гиперпараметров
  * **DeepSpeed**: Прямой контроль API, продвинутые функции
  * **Сырой DDP**: Максимальный контроль, минимум абстракций


## Частые проблемы[​](<#common-issues> "Прямая ссылка на Частые проблемы")
**Проблема: Неправильное размещение устройства**
Не перемещайте данные на устройство вручную:
[code] 
    # НЕПРАВИЛЬНО  
    batch = batch.to('cuda')  
      
    # ПРАВИЛЬНО  
    # Accelerate делает это автоматически после prepare()  
    
[/code]
**Проблема: Накопление градиентов не работает**
Используйте контекстный менеджер:
[code] 
    # ПРАВИЛЬНО  
    with accelerator.accumulate(model):  
        optimizer.zero_grad()  
        accelerator.backward(loss)  
        optimizer.step()  
    
[/code]
**Проблема: Сохранение контрольных точек в распределённом режиме**
Используйте методы accelerator:
[code] 
    # Сохранять только на главном процессе  
    if accelerator.is_main_process:  
        accelerator.save_state('checkpoint/')  
      
    # Загружать на всех процессах  
    accelerator.load_state('checkpoint/')  
    
[/code]
**Проблема: Разные результаты с FSDP**
Убедитесь, что начальное значение генератора одинаковое:
[code] 
    from accelerate.utils import set_seed  
    set_seed(42)  
    
[/code]
## Продвинутые темы[​](<#advanced-topics> "Прямая ссылка на Продвинутые темы")
**Интеграция Megatron**: См. [references/megatron-integration.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/accelerate/references/megatron-integration.md>) для настройки тензорного параллелизма, конвейерного параллелизма и параллелизма последовательностей.
**Пользовательские плагины**: См. [references/custom-plugins.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/accelerate/references/custom-plugins.md>) для создания собственных плагинов распределённых вычислений и продвинутой конфигурации.
**Настройка производительности**: См. [references/performance.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/accelerate/references/performance.md>) для профилирования, оптимизации памяти и лучших практик.
## Требования к оборудованию[​](<#hardware-requirements> "Прямая ссылка на Требования к оборудованию")
  * **CPU**: Работает (медленно)
  * **Один GPU**: Работает
  * **Несколько GPU**: DDP (по умолчанию), DeepSpeed или FSDP
  * **Несколько узлов**: DDP, DeepSpeed, FSDP, Megatron
  * **TPU**: Поддерживается
  * **Apple MPS**: Поддерживается


**Требования к лаунчеру**:
  * **DDP**: `torch.distributed.run` (встроенный)
  * **DeepSpeed**: `deepspeed` (pip install deepspeed)
  * **FSDP**: PyTorch 1.12+ (встроенный)
  * **Megatron**: Пользовательская настройка


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * Документация: <https://huggingface.co/docs/accelerate>
  * GitHub: <https://github.com/huggingface/accelerate>
  * Версия: 1.11.0+
  * Учебник: «Accelerate your scripts»
  * Примеры: <https://github.com/huggingface/accelerate/tree/main/examples>
  * Используется: HuggingFace Transformers, TRL, PEFT, все HF-библиотеки


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Быстрый старт](<#quick-start>)
  * [Типовые рабочие процессы](<#common-workflows>)
    * [Рабочий процесс 1: От одного GPU к нескольким](<#workflow-1-from-single-gpu-to-multi-gpu>)
    * [Рабочий процесс 2: Обучение со смешанной точностью](<#workflow-2-mixed-precision-training>)
    * [Рабочий процесс 3: Интеграция DeepSpeed ZeRO](<#workflow-3-deepspeed-zero-integration>)
    * [Рабочий процесс 4: FSDP (Fully Sharded Data Parallel)](<#workflow-4-fsdp-fully-sharded-data-parallel>)
    * [Рабочий процесс 5: Накопление градиентов](<#workflow-5-gradient-accumulation>)
  * [Когда использовать vs альтернативы](<#when-to-use-vs-alternatives>)
  * [Частые проблемы](<#common-issues>)
  * [Продвинутые темы](<#advanced-topics>)
  * [Требования к оборудованию](<#hardware-requirements>)
  * [Ресурсы](<#resources>)


<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-accelerate -->
