На этой странице

Пакетная обработка позволяет запускать агента Hermes на сотнях или тысячах промптов параллельно, генерируя структурированные данные траекторий. В первую очередь это используется для **генерации обучающих данных** — создания траекторий в формате ShareGPT со статистикой использования инструментов, которые могут применяться для дообучения или оценки.

## Обзор[​](<#overview> "Direct link to Overview")

Пакетный запуск (`batch_runner.py`) обрабатывает JSONL-набор данных с промптами, пропуская каждый через полноценную сессию агента с доступом к инструментам. Каждый промпт получает своё изолированное окружение. На выходе получаются структурированные данные траекторий с полной историей диалога, статистикой вызовов инструментов и метриками покрытия рассуждений.

## Быстрый старт[​](<#quick-start> "Direct link to Quick Start")

[code] 
    # Базовый пакетный запуск  
    python batch_runner.py \  
        --dataset_file=data/prompts.jsonl \  
        --batch_size=10 \  
        --run_name=my_first_run \  
        --model=anthropic/claude-sonnet-4.6 \  
        --num_workers=4  
      
    # Возобновление прерванного запуска  
    python batch_runner.py \  
        --dataset_file=data/prompts.jsonl \  
        --batch_size=10 \  
        --run_name=my_first_run \  
        --resume  
      
    # Список доступных дистрибутивов наборов инструментов  
    python batch_runner.py --list_distributions  
    
[/code]

## Формат набора данных[​](<#dataset-format> "Direct link to Dataset Format")

Входной набор данных — это JSONL-файл (один JSON-объект на строку). Каждая запись должна содержать поле `prompt`:

[code] 
    {"prompt": "Write a Python function that finds the longest palindromic substring"}  
    {"prompt": "Create a REST API endpoint for user authentication using Flask"}  
    {"prompt": "Debug this error: TypeError: cannot unpack non-iterable NoneType object"}  
    
[/code]

Записи могут опционально включать:
  * `image` или `docker_image`: образ контейнера для песочницы данного промпта (работает с бэкендами Docker, Modal и Singularity)
  * `cwd`: переопределение рабочей директории для терминальной сессии задачи



## Параметры конфигурации[​](<#configuration-options> "Direct link to Configuration Options")

Параметр| По умолчанию| Описание  
---|---|---  
`--dataset_file`| (обязательно)| Путь к JSONL-набору данных  
`--batch_size`| (обязательно)| Промптов в пакете  
`--run_name`| (обязательно)| Имя запуска (используется для выходной директории и контрольных точек)  
`--distribution`| `"default"`| Дистрибутив наборов инструментов для выборки  
`--model`| `claude-sonnet-4.6`| Используемая модель  
`--base_url`| `https://openrouter.ai/api/v1`| Базовый URL API  
`--api_key`| (переменная окружения)| API-ключ для модели  
`--max_turns`| `10`| Максимальное количество итераций вызова инструментов на один промпт  
`--num_workers`| `4`| Количество параллельных рабочих процессов  
`--resume`| `false`| Возобновить из контрольной точки  
`--verbose`| `false`| Включить подробное логирование  
`--max_samples`| все| Обработать только первые N образцов из набора данных  
`--max_tokens`| по умолчанию модели| Максимальное количество токенов на ответ модели  

### Маршрутизация провайдеров (OpenRouter)[​](<#provider-routing-openrouter> "Direct link to Provider Routing (OpenRouter)")

Параметр| Описание  
---|---  
`--providers_allowed`| Разрешённые провайдеры через запятую (например, `"anthropic,openai"`)  
`--providers_ignored`| Игнорируемые провайдеры через запятую (например, `"together,deepinfra"`)  
`--providers_order`| Предпочтительный порядок провайдеров через запятую  
`--provider_sort`| Сортировка по `"price"`, `"throughput"` или `"latency"`  

### Управление рассуждениями[​](<#reasoning-control> "Direct link to Reasoning Control")

Параметр| Описание  
---|---  
`--reasoning_effort`| Уровень усилий: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`  
`--reasoning_disabled`| Полное отключение токенов рассуждения/размышления  

### Расширенные опции[​](<#advanced-options> "Direct link to Advanced Options")

Параметр| Описание  
---|---  
`--ephemeral_system_prompt`| Системный промпт, используемый во время выполнения, НО не сохраняемый в траектории  
`--log_prefix_chars`| Количество символов, показываемых в предпросмотре лога (по умолчанию: 100)  
`--prefill_messages_file`| Путь к JSON-файлу с prefill-сообщениями для few-shot прайминга  

## Дистрибутивы наборов инструментов[​](<#toolset-distributions> "Direct link to Toolset Distributions")

Каждый промпт получает случайно выбранный набор инструментов из **дистрибутива**. Это гарантирует, что обучающие данные покрывают разнообразные комбинации инструментов. Используйте `--list_distributions`, чтобы увидеть все доступные дистрибутивы.

В текущей реализации дистрибутивы назначают вероятность **каждому отдельному набору инструментов**. Сэмплер независимо проверяет каждый набор, затем гарантирует, что хотя бы один набор включён. Это отличается от таблицы предварительно собранных комбинаций, написанной вручную.

## Выходной формат[​](<#output-format> "Direct link to Output Format")

Все выходные данные сохраняются в `data/<run_name>/`:

[code] 
    data/my_run/  
    ├── trajectories.jsonl    # Итоговый объединённый результат (все пакеты слиты)  
    ├── batch_0.jsonl         # Результаты отдельных пакетов  
    ├── batch_1.jsonl  
    ├── ...  
    ├── checkpoint.json       # Контрольная точка для возобновления  
    └── statistics.json       # Агрегированная статистика использования инструментов  
    
[/code]

### Формат траекторий[​](<#trajectory-format> "Direct link to Trajectory Format")

Каждая строка в `trajectories.jsonl` — это JSON-объект:

[code] 
    {  
      "prompt_index": 42,  
      "conversations": [  
        {"from": "human", "value": "Write a function..."},  
        {"from": "gpt", "value": "I'll create that function...",  
         "tool_calls": [...]},  
        {"from": "tool", "value": "..."},  
        {"from": "gpt", "value": "Here's the completed function..."}  
      ],  
      "metadata": {  
        "batch_num": 2,  
        "timestamp": "2026-01-15T10:30:00",  
        "model": "anthropic/claude-sonnet-4.6"  
      },  
      "completed": true,  
      "partial": false,  
      "api_calls": 3,  
      "toolsets_used": ["terminal", "file"],  
      "tool_stats": {  
        "terminal": {"count": 2, "success": 2, "failure": 0},  
        "read_file": {"count": 1, "success": 1, "failure": 0}  
      },  
      "tool_error_counts": {  
        "terminal": 0,  
        "read_file": 0  
      }  
    }  
    
[/code]

Поле `conversations` использует формат, подобный ShareGPT, с полями `from` и `value`. Статистика по инструментам нормализована так, чтобы включать все возможные инструменты с нулевыми значениями по умолчанию, обеспечивая единообразную схему для всех записей для совместимости с наборами данных HuggingFace.

## Контрольные точки[​](<#checkpointing> "Direct link to Checkpointing")

Пакетный запуск имеет надёжную систему контрольных точек для отказоустойчивости:
  * **Файл контрольной точки:** Сохраняется после завершения каждого пакета, отслеживая, какие индексы промптов уже обработаны
  * **Возобновление на основе содержимого:** При `--resume` запускатор сканирует существующие пакетные файлы и сопоставляет завершённые промпты по их фактическому текстовому содержимому (а не только по индексам), что позволяет восстановиться даже при изменении порядка набора данных
  * **Неудачные промпты:** Только успешно завершённые промпты помечаются как выполненные — неудачные промпты будут повторно обработаны при возобновлении
  * **Слияние пакетов:** По завершении все пакетные файлы (включая файлы от предыдущих запусков) сливаются в единый `trajectories.jsonl`



### Как работает возобновление[​](<#how-resume-works> "Direct link to How Resume Works")

  1. Сканировать все файлы `batch_*.jsonl` на предмет завершённых промптов (по совпадению содержимого)
  2. Отфильтровать набор данных, исключив уже завершённые промпты
  3. Перепакетировать оставшиеся промпты
  4. Обработать только оставшиеся промпты
  5. Слить все пакетные файлы (старые + новые) в итоговый результат



## Фильтрация качества[​](<#quality-filtering> "Direct link to Quality Filtering")

Пакетный запуск применяет автоматическую фильтрацию качества:
  * **Фильтр отсутствия рассуждений:** Образцы, в которых ни один из раундов ассистента не содержит рассуждений (нет `<REASONING_SCRATCHPAD>` или нативных токенов размышления), отбрасываются
  * **Фильтр повреждённых записей:** Записи с вымышленными именами инструментов (не входящими в допустимый список инструментов) отфильтровываются во время финального слияния
  * **Статистика рассуждений:** Отслеживается процент раундов с/без рассуждений за весь запуск



## Статистика[​](<#statistics> "Direct link to Statistics")

После завершения запускатор выводит полную статистику:
  * **Использование инструментов:** Количество вызовов, частоту успехов/неудач по каждому инструменту
  * **Покрытие рассуждениями:** Процент раундов ассистента с рассуждениями
  * **Отброшенные образцы:** Количество образцов, отфильтрованных за отсутствие рассуждений
  * **Длительность:** Общее время обработки



Статистика также сохраняется в `statistics.json` для программного анализа.

## Варианты использования[​](<#use-cases> "Direct link to Use Cases")

### Генерация обучающих данных[​](<#training-data-generation> "Direct link to Training Data Generation")

Генерация разнообразных траекторий использования инструментов для дообучения:

[code] 
    python batch_runner.py \  
        --dataset_file=data/coding_prompts.jsonl \  
        --batch_size=20 \  
        --run_name=coding_v1 \  
        --model=anthropic/claude-sonnet-4.6 \  
        --num_workers=8 \  
        --distribution=default \  
        --max_turns=15  
    
[/code]

### Оценка модели[​](<#model-evaluation> "Direct link to Model Evaluation")

Оценка того, насколько хорошо модель использует инструменты на стандартизированных промптах:

[code] 
    python batch_runner.py \  
        --dataset_file=data/eval_suite.jsonl \  
        --batch_size=10 \  
        --run_name=eval_gpt4 \  
        --model=openai/gpt-4o \  
        --num_workers=4 \  
        --max_turns=10  
    
[/code]

### Индивидуальные образы контейнеров для каждого промпта[​](<#per-prompt-container-images> "Direct link to Per-Prompt Container Images")

Для бенчмарков, требующих специфических окружений, каждый промпт может указывать свой образ контейнера:

[code] 
    {"prompt": "Install numpy and compute eigenvalues of a 3x3 matrix", "image": "python:3.11-slim"}  
    {"prompt": "Compile this Rust program and run it", "image": "rust:1.75"}  
    {"prompt": "Set up a Node.js Express server", "image": "node:20-alpine", "cwd": "/app"}  
    
[/code]

Пакетный запуск проверяет доступность Docker-образов перед запуском каждого промпта.

  * [Обзор](<#overview>)
  * [Быстрый старт](<#quick-start>)
  * [Формат набора данных](<#dataset-format>)
  * [Параметры конфигурации](<#configuration-options>)
    * [Маршрутизация провайдеров (OpenRouter)](<#provider-routing-openrouter>)
    * [Управление рассуждениями](<#reasoning-control>)
    * [Расширенные опции](<#advanced-options>)
  * [Дистрибутивы наборов инструментов](<#toolset-distributions>)
  * [Выходной формат](<#output-format>)
    * [Формат траекторий](<#trajectory-format>)
  * [Контрольные точки](<#checkpointing>)
    * [Как работает возобновление](<#how-resume-works>)
  * [Фильтрация качества](<#quality-filtering>)
  * [Статистика](<#statistics>)
  * [Варианты использования](<#use-cases>)
    * [Генерация обучающих данных](<#training-data-generation>)
    * [Оценка модели](<#model-evaluation>)
    * [Индивидуальные образы контейнеров для каждого промпта](<#per-prompt-container-images>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing -->
