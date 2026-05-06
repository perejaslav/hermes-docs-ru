На этой странице
Содержит руководство по пост-тренировке LLM с RL с использованием slime — фреймворка на базе Megatron+SGLang. Используйте при обучении моделей GLM, реализации собственных рабочих процессов генерации данных или при необходимости тесной интеграции с Megatron-LM для масштабирования RL.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Опционально — установка: `hermes skills install official/mlops/slime`  |
|Путь| `optional-skills/mlops/slime`  |
|Версия| `1.0.0`  |
|Автор| Orchestra Research  |
|Лицензия| MIT  |
|Зависимости| `sglang-router>=0.2.3`, `ray`, `torch>=2.0.0`, `transformers>=4.40.0`  |
|Теги| `Reinforcement Learning`, `Megatron-LM`, `SGLang`, `GRPO`, `Post-Training`, `GLM`  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые агент видит, когда навык активен.
# slime: Фреймворк пост-тренировки LLM для масштабирования RL
slime — это фреймворк пост-тренировки LLM от команды THUDM из Университета Цинхуа, на базе которого работают GLM-4.5, GLM-4.6 и GLM-4.7. Он объединяет Megatron-LM для обучения и SGLang для высокопроизводительной генерации прогонов (rollout).
## Когда использовать slime[​](<#when-to-use-slime> "Прямая ссылка на Когда использовать slime")
**Выбирайте slime, когда вам нужно:**
  * Нативное обучение Megatron-LM с инференсом SGLang
  * Собственные рабочие процессы генерации данных с гибкими буферами данных
  * Обучение моделей GLM, Qwen3, DeepSeek V3 или Llama 3
  * Исследовательский фреймворк с производственной поддержкой (Z.ai)


**Рассмотрите альтернативы, когда:**
  * Вам нужны функции корпоративной стабильности → используйте **miles**
  * Вы хотите гибкую смену бэкенда → используйте **verl**
  * Вам нужны абстракции, родные для PyTorch → используйте **torchforge**


## Ключевые особенности[​](<#key-features> "Прямая ссылка на Ключевые особенности")
  * **Обучение**: Megatron-LM с полной поддержкой параллелизма (TP, PP, DP, SP)
  * **Прогон (Rollout)**: Высокопроизводительная генерация на SGLang с маршрутизатором
  * **Буфер данных**: Гибкое управление промптами и хранение семплов
  * **Модели**: GLM-4.x, Qwen3, DeepSeek V3/R1, Llama 3


## Обзор архитектуры[​](<#architecture-overview> "Прямая ссылка на Обзор архитектуры")
[code] 
    ┌─────────────────────────────────────────────────────────┐  
    │                    Буфер данных (Data Buffer)            │  
    │ - Инициализация и управление промптами                   │  
    │ - Пользовательская генерация и фильтрация данных         │  
    │ - Хранение семплов прогонов (rollout)                    │  
    └─────────────┬───────────────────────────┬───────────────┘  
                  │                           │  
    ┌─────────────▼───────────┐ ┌─────────────▼───────────────┐  
    │ Обучение (Megatron-LM)  │ │ Прогон (SGLang + Router)    │  
    │ - Обучение модели-актора│ │ - Генерация ответов         │  
    │ - Критик (опционально)  │ │ - Вывод награды/верификатора│  
    │ - Синхронизация весов   │ │ - Поддержка нескольких ходов│  
    └─────────────────────────┘ └─────────────────────────────┘  
    
[/code]
## Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Рекомендуется: Docker  
    docker pull slimerl/slime:latest  
    docker run --rm --gpus all --ipc=host --shm-size=16g \  
      -it slimerl/slime:latest /bin/bash  
      
    # Внутри контейнера  
    cd /root/slime && pip install -e . --no-deps  
    
[/code]
### Из исходников[​](<#from-source> "Прямая ссылка на Из исходников")
[code] 
    git clone https://github.com/THUDM/slime.git  
    cd slime  
    pip install -r requirements.txt  
    pip install -e .  
    
[/code]
## Быстрый старт: GRPO обучение[​](<#quick-start-grpo-training> "Прямая ссылка на Быстрый старт: GRPO обучение")
[code] 
    # Конфигурация исходной модели  
    source scripts/models/qwen3-4B.sh  
      
    # Запуск обучения  
    python train.py \  
        --actor-num-nodes 1 \  
        --actor-num-gpus-per-node 4 \  
        --rollout-num-gpus 4 \  
        --advantage-estimator grpo \  
        --use-kl-loss --kl-loss-coef 0.001 \  
        --rollout-batch-size 32 \  
        --n-samples-per-prompt 8 \  
        --global-batch-size 256 \  
        --num-rollout 3000 \  
        --prompt-data /path/to/data.jsonl \  
        ${MODEL_ARGS[@]} ${CKPT_ARGS[@]}  
    
[/code]
* * *
## Рабочий процесс 1: Стандартное GRPO обучение[​](<#workflow-1-standard-grpo-training> "Прямая ссылка на Рабочий процесс 1: Стандартное GRPO обучение")
Используйте этот рабочий процесс для обучения моделей рассуждения с групповыми относительными преимуществами.
### Контрольный список предварительных требований[​](<#prerequisites-checklist> "Прямая ссылка на Контрольный список предварительных требований")
  * Docker-среда или установленные Megatron-LM + SGLang
  * Контрольная точка модели (формат HuggingFace или Megatron)
  * Обучающие данные в формате JSONL


### Шаг 1: Подготовка данных[​](<#step-1-prepare-data> "Прямая ссылка на Шаг 1: Подготовка данных")
[code] 
    # Формат data.jsonl  
    {"prompt": "What is 2 + 2?", "label": "4"}  
    {"prompt": "Solve: 3x = 12", "label": "x = 4"}  
    
[/code]
Или в чат-формате:
[code] 
    {  
        "prompt": [  
            {"role": "system", "content": "You are a math tutor."},  
            {"role": "user", "content": "What is 15 + 27?"}  
        ],  
        "label": "42"  
    }  
    
[/code]
### Шаг 2: Настройка модели[​](<#step-2-configure-model> "Прямая ссылка на Шаг 2: Настройка модели")
Выберите предварительно настроенный скрипт модели:
[code] 
    # Список доступных моделей  
    ls scripts/models/  
    # glm4-9B.sh, qwen3-4B.sh, qwen3-30B-A3B.sh, deepseek-v3.sh, llama3-8B.sh, ...  
      
    # Загрузите вашу модель  
    source scripts/models/qwen3-4B.sh  
    
[/code]
### Шаг 3: Запуск обучения[​](<#step-3-launch-training> "Прямая ссылка на Шаг 3: Запуск обучения")
[code] 
    python train.py \  
        --actor-num-nodes 1 \  
        --actor-num-gpus-per-node 8 \  
        --rollout-num-gpus 8 \  
        --advantage-estimator grpo \  
        --use-kl-loss \  
        --kl-loss-coef 0.001 \  
        --prompt-data /path/to/train.jsonl \  
        --input-key prompt \  
        --label-key label \  
        --apply-chat-template \  
        --rollout-batch-size 32 \  
        --n-samples-per-prompt 8 \  
        --global-batch-size 256 \  
        --num-rollout 3000 \  
        --save-interval 100 \  
        --eval-interval 50 \  
        ${MODEL_ARGS[@]}  
    
[/code]
### Шаг 4: Мониторинг обучения[​](<#step-4-monitor-training> "Прямая ссылка на Шаг 4: Мониторинг обучения")
  * Проверьте TensorBoard: `tensorboard --logdir outputs/`
  * Убедитесь, что кривые наград растут
  * Мониторьте использование GPU на всех узлах


* * *
## Рабочий процесс 2: Асинхронное обучение[​](<#workflow-2-asynchronous-training> "Прямая ссылка на Рабочий процесс 2: Асинхронное обучение")
Используйте асинхронный режим для более высокой пропускной способности за счёт перекрытия прогонов и обучения.
### Когда использовать асинхронный режим[​](<#when-to-use-async> "Прямая ссылка на Когда использовать асинхронный режим")
  * Крупные модели с длительным временем генерации
  * Высокий простой GPU в синхронном режиме
  * Достаточный объём памяти для буферизации


### Запуск асинхронного обучения[​](<#launch-async-training> "Прямая ссылка на Запуск асинхронного обучения")
[code] 
    python train_async.py \  
        --actor-num-nodes 1 \  
        --actor-num-gpus-per-node 8 \  
        --rollout-num-gpus 8 \  
        --advantage-estimator grpo \  
        --async-buffer-size 4 \  
        --prompt-data /path/to/train.jsonl \  
        ${MODEL_ARGS[@]}  
    
[/code]
### Специфичные параметры асинхронного режима[​](<#async-specific-parameters> "Прямая ссылка на Специфичные параметры асинхронного режима")
[code] 
    --async-buffer-size 4        # Количество буферизируемых прогонов  
    --update-weights-interval 2  # Частота синхронизации весов (каждые N прогонов)  
    
[/code]
* * *
## Рабочий процесс 3: Многоходовое агентное обучение[​](<#workflow-3-multi-turn-agentic-training> "Прямая ссылка на Рабочий процесс 3: Многоходовое агентное обучение")
Используйте этот рабочий процесс для обучения агентов с использованием инструментов или многошаговых рассуждений.
### Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  * Пользовательская функция генерации для многоходовой логики
  * Интерфейс инструментов/окружения


### Шаг 1: Определение пользовательской функции генерации[​](<#step-1-define-custom-generate-function> "Прямая ссылка на Шаг 1: Определение пользовательской функции генерации")
[code] 
    # custom_generate.py  
    async def custom_generate(args, samples, evaluation=False):  
        """Многоходовая генерация с вызовом инструментов."""  
        for sample in samples:  
            conversation = sample.prompt  
      
            for turn in range(args.max_turns):  
                # Генерация ответа  
                response = await generate_single(conversation)  
      
                # Проверка на вызов инструмента  
                tool_call = extract_tool_call(response)  
                if tool_call:  
                    tool_result = execute_tool(tool_call)  
                    conversation.append({"role": "assistant", "content": response})  
                    conversation.append({"role": "tool", "content": tool_result})  
                else:  
                    break  
      
            sample.response = response  
            sample.reward = compute_reward(sample)  
      
        return samples  
    
[/code]
### Шаг 2: Запуск с пользовательской функцией[​](<#step-2-launch-with-custom-function> "Прямая ссылка на Шаг 2: Запуск с пользовательской функцией")
[code] 
    python train.py \  
        --custom-generate-function-path custom_generate.py \  
        --max-turns 5 \  
        --prompt-data /path/to/agent_data.jsonl \  
        ${MODEL_ARGS[@]}  
    
[/code]
Смотрите `examples/search-r1/` для полного примера многоходового поиска.
* * *
## Справочник по конфигурации[​](<#configuration-reference> "Прямая ссылка на Справочник по конфигурации")
### Три категории аргументов[​](<#three-argument-categories> "Прямая ссылка на Три категории аргументов")
slime использует три типа аргументов:
**1\\. Аргументы Megatron** (передаются напрямую):
[code] 
    --tensor-model-parallel-size 2  
    --pipeline-model-parallel-size 1  
    --num-layers 32  
    --hidden-size 4096  
    
[/code]
**2\\. Аргументы SGLang** (с префиксом `--sglang-`):
[code] 
    --sglang-mem-fraction-static 0.8  
    --sglang-context-length 8192  
    --sglang-log-level INFO  
    
[/code]
**3\\. Аргументы slime**:
[code] 
    # Выделение ресурсов  
    --actor-num-nodes 1  
    --actor-num-gpus-per-node 8  
    --rollout-num-gpus 8  
    --colocate  # Совместное использование GPU между обучением/инференсом  
      
    # Данные  
    --prompt-data /path/to/data.jsonl  
    --input-key prompt  
    --label-key label  
      
    # Цикл обучения  
    --num-rollout 3000  
    --rollout-batch-size 32  
    --n-samples-per-prompt 8  
    --global-batch-size 256  
      
    # Алгоритм  
    --advantage-estimator grpo  # или: gspo, ppo, reinforce_plus_plus  
    --use-kl-loss  
    --kl-loss-coef 0.001  
    
[/code]
### Ключевые ограничения[​](<#key-constraints> "Прямая ссылка на Ключевые ограничения")
[code] 
    rollout_batch_size × n_samples_per_prompt = global_batch_size × num_steps_per_rollout  
    
[/code]
Пример: 32 × 8 = 256 × 1
* * *
## Система буфера данных[​](<#data-buffer-system> "Прямая ссылка на Система буфера данных")
Буфер данных slime обеспечивает гибкое управление данными:
### Базовый источник данных[​](<#basic-data-source> "Прямая ссылка на Базовый источник данных")
[code] 
    class RolloutDataSource:  
        def get_samples(self, num_samples):  
            """Получить промпты из набора данных."""  
            return self.dataset.sample(num_samples)  
      
        def add_samples(self, samples):  
            """Вызывается после генерации (по умолчанию ничего не делает)."""  
            pass  
    
[/code]
### Буферизированный источник данных (Off-Policy)[​](<#buffered-data-source-off-policy> "Прямая ссылка на Буферизированный источник данных (Off-Policy)")
[code] 
    class RolloutDataSourceWithBuffer(RolloutDataSource):  
        def __init__(self):  
            self.buffer = []  
      
        def add_samples(self, samples):  
            """Сохранить сгенерированные семплы для повторного использования."""  
            self.buffer.extend(samples)  
      
        def buffer_filter(self, args, buffer, num_samples):  
            """Пользовательская логика выбора (приоритетная, стратифицированная и т.д.)."""  
            return select_best(buffer, num_samples)  
    
[/code]
* * *
## Частые проблемы и решения[​](<#common-issues-and-solutions> "Прямая ссылка на Частые проблемы и решения")
### Проблема: Сбой SGLang Engine[​](<#issue-sglang-engine-crash> "Прямая ссылка на Проблема: Сбой SGLang Engine")
**Симптомы**: Движок инференса падает во время обучения
**Решения**:
[code] 
    # Включить отказоустойчивость  
    --use-fault-tolerance  
      
    # Увеличить выделение памяти  
    --sglang-mem-fraction-static 0.85  
      
    # Уменьшить размер батча  
    --rollout-batch-size 16  
    
[/code]
### Проблема: Тайм-аут синхронизации весов[​](<#issue-weight-sync-timeout> "Прямая ссылка на Проблема: Тайм-аут синхронизации весов")
**Симптомы**: Обучение зависает после прогона
**Решения**:
[code] 
    # Увеличить интервал синхронизации  
    --update-weights-interval 5  
      
    # Использовать режим совместного размещения (без сетевой передачи)  
    --colocate  
    
[/code]
### Проблема: OOM во время обучения[​](<#issue-oom-during-training> "Прямая ссылка на Проблема: OOM во время обучения")
**Симптомы**: CUDA OOM при обратном проходе
**Решения**:
[code] 
    # Включить градиентную контрольную точку  
    --recompute-activations  
      
    # Уменьшить размер микро-батча  
    --micro-batch-size 1  
      
    # Включить последовательный параллелизм  
    --sequence-parallel  
    
[/code]
### Проблема: Медленная загрузка данных[​](<#issue-slow-data-loading> "Прямая ссылка на Проблема: Медленная загрузка данных")
**Симптомы**: GPU простаивает во время выборки данных
**Решения**:
[code] 
    # Увеличить количество рабочих процессов данных  
    --num-data-workers 4  
      
    # Использовать потоковый набор данных  
    --streaming-data  
    
[/code]
* * *
## Поддерживаемые модели[​](<#supported-models> "Прямая ссылка на Поддерживаемые модели")
Семейство моделей| Конфигурации  
---|---  
GLM| GLM-4.5, GLM-4.6, GLM-4.7, GLM-Z1-9B  
Qwen| Qwen3 (4B, 8B, 30B-A3B), Qwen3-MoE, Qwen2.5  
DeepSeek| V3, V3.1, R1  
Llama| Llama 3 (8B, 70B)  
Другие| Kimi K2, Moonlight-16B  
Для каждой модели есть предварительно настроенные скрипты в `scripts/models/`.
* * *
## Продвинутые темы[​](<#advanced-topics> "Прямая ссылка на Продвинутые темы")
### Режим совместного размещения (Co-location)[​](<#co-location-mode> "Прямая ссылка на Режим совместного размещения (Co-location)")
Совместное использование GPU между обучением и инференсом для уменьшения потребления памяти:
[code] 
    python train.py \  
        --colocate \  
        --actor-num-gpus-per-node 8 \  
        --sglang-mem-fraction-static 0.4 \  
        ${MODEL_ARGS[@]}  
    
[/code]
### Пользовательская модель награды[​](<#custom-reward-model> "Прямая ссылка на Пользовательская модель награды")
[code] 
    # custom_rm.py  
    class CustomRewardModel:  
        def __init__(self, model_path):  
            self.model = load_model(model_path)  
      
        def compute_reward(self, prompts, responses):  
            inputs = self.tokenize(prompts, responses)  
            scores = self.model(inputs)  
            return scores.tolist()  
    
[/code]
[code] 
    --custom-rm-path custom_rm.py  
    
[/code]
### Оценка нескольких задач[​](<#evaluation-multi-task> "Прямая ссылка на Оценка нескольких задач")
[code] 
    --eval-prompt-data aime /path/to/aime.jsonl \  
    --eval-prompt-data gsm8k /path/to/gsm8k.jsonl \  
    --n-samples-per-eval-prompt 16  
    
[/code]
* * *
## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **Документация**: <https://thudm.github.io/slime/>
  * **GitHub**: <https://github.com/THUDM/slime>
  * **Блог**: <https://lmsys.org/blog/2025-07-09-slime/>
  * **Примеры**: Смотрите директорию `examples/` — 14+ готовых примеров


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать slime](<#when-to-use-slime>)
  * [Ключевые особенности](<#key-features>)
  * [Обзор архитектуры](<#architecture-overview>)
  * [Установка](<#installation>)
    * [Из исходников](<#from-source>)
  * [Быстрый старт: GRPO обучение](<#quick-start-grpo-training>)
  * [Рабочий процесс 1: Стандартное GRPO обучение](<#workflow-1-standard-grpo-training>)
    * [Контрольный список предварительных требований](<#prerequisites-checklist>)
    * [Шаг 1: Подготовка данных](<#step-1-prepare-data>)
    * [Шаг 2: Настройка модели](<#step-2-configure-model>)
    * [Шаг 3: Запуск обучения](<#step-3-launch-training>)
    * [Шаг 4: Мониторинг обучения](<#step-4-monitor-training>)
  * [Рабочий процесс 2: Асинхронное обучение](<#workflow-2-asynchronous-training>)
    * [Когда использовать асинхронный режим](<#when-to-use-async>)
    * [Запуск асинхронного обучения](<#launch-async-training>)
    * [Специфичные параметры асинхронного режима](<#async-specific-parameters>)
  * [Рабочий процесс 3: Многоходовое агентное обучение](<#workflow-3-multi-turn-agentic-training>)
    * [Предварительные требования](<#prerequisites>)
    * [Шаг 1: Определение пользовательской функции генерации](<#step-1-define-custom-generate-function>)
    * [Шаг 2: Запуск с пользовательской функцией](<#step-2-launch-with-custom-function>)
  * [Справочник по конфигурации](<#configuration-reference>)
    * [Три категории аргументов](<#three-argument-categories>)
    * [Ключевые ограничения](<#key-constraints>)
  * [Система буфера данных](<#data-buffer-system>)
    * [Базовый источник данных](<#basic-data-source>)
    * [Буферизированный источник данных (Off-Policy)](<#buffered-data-source-off-policy>)
  * [Частые проблемы и решения](<#common-issues-and-solutions>)
    * [Проблема: Сбой SGLang Engine](<#issue-sglang-engine-crash>)
    * [Проблема: Тайм-аут синхронизации весов](<#issue-weight-sync-timeout>)
    * [Проблема: OOM во время обучения](<#issue-oom-during-training>)
    * [Проблема: Медленная загрузка данных](<#issue-slow-data-loading>)
  * [Поддерживаемые модели](<#supported-models>)
  * [Продвинутые темы](<#advanced-topics>)
    * [Режим совместного размещения (Co-location)](<#co-location-mode>)
    * [Пользовательская модель награды](<#custom-reward-model>)
    * [Оценка нескольких задач](<#evaluation-multi-task>)
  * [Ресурсы](<#resources>)



