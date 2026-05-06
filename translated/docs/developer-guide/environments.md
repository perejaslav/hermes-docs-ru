На этой странице
Hermes Agent включает полноценный фреймворк окружений, который связывает возможности вызова инструментов с фреймворком RL-обучения [Atropos](<https://github.com/NousResearch/atropos>). Это обеспечивает три рабочих процесса:
  1. **RL-обучение** — обучение языковых моделей на многопользовательских агентных задачах с GRPO
  2. **Бенчмарки** — оценка моделей на стандартизированных агентных бенчмарках
  3. **Генерация данных** — создание SFT-данных для обучения из развёртываний агента


Все три используют одну и ту же основу: класс **окружения**, который определяет задачи, запускает цикл агента и оценивает результат.
Окружения репозитория и инструменты RL-обучения
Фреймворк окружений на Python, описанный здесь, находится в директории `environments/` репозитория и представляет собой API уровня реализации для интеграции Hermes/Atropos. Он отделён от пользовательских инструментов `rl_*`, которые работают как оркестрационная оболочка для удалённых процессов RL-обучения.
Быстрые ссылки
  * **Хотите запустить бенчмарки?** Переходите к [Доступные бенчмарки](<#available-benchmarks>)
  * **Хотите обучать с RL?** Смотрите [Инструменты RL-обучения](</docs/user-guide/features/rl-training>) для агентного интерфейса или [Запуск окружений](<#running-environments>) для ручного выполнения
  * **Хотите создать новое окружение?** Смотрите [Создание окружений](<#creating-environments>)


## Архитектура[​](<#architecture> "Прямая ссылка на Архитектура")
Система окружений построена на трёхуровневой цепочке наследования:
### BaseEnv (Atropos)[​](<#baseenv-atropos> "Прямая ссылка на BaseEnv \\(Atropos\\)")
Фундамент из `atroposlib`. Предоставляет:
  * **Управление сервером** — подключение к API, совместимым с OpenAI (VLLM, SGLang, OpenRouter)
  * **Планирование задач** — координация параллельных развёртываний
  * **Интеграция с Wandb** — логирование метрик и визуализация развёртываний
  * **CLI-интерфейс** — три подкоманды: `serve`, `process`, `evaluate`
  * **Логирование оценок** — `evaluate_log()` сохраняет результаты в JSON + JSONL


### HermesAgentBaseEnv[​](<#hermesagentbaseenv> "Прямая ссылка на HermesAgentBaseEnv")
Слой hermes-agent (`environments/hermes_base_env.py`). Добавляет:
  * **Конфигурация терминального бэкенда** — устанавливает `TERMINAL_ENV` для изолированного выполнения (local, Docker, Modal, Daytona, SSH, Singularity)
  * **Разрешение инструментов** — `_resolve_tools_for_group()` вызывает `get_tool_definitions()` из hermes-agent для получения правильных схем инструментов на основе включённых/отключённых наборов
  * **Интеграция цикла агента** — `collect_trajectory()` запускает `HermesAgentLoop` и оценивает результат
  * **Двухфазная работа** — Фаза 1 (сервер OpenAI) для eval/SFT, Фаза 2 (VLLM ManagedServer) для полноценного RL с logprobs
  * **Патчи для асинхронной безопасности** — monkey-patch для Modal-бэкенда для работы внутри цикла событий Atropos


### Конкретные окружения[​](<#concrete-environments> "Прямая ссылка на Конкретные окружения")
Ваше окружение наследуется от `HermesAgentBaseEnv` и реализует пять методов:
Метод| Назначение  
---|---  
`setup()`| Загрузка датасета, инициализация состояния  
`get_next_item()`| Возврат следующего элемента для развёртывания  
`format_prompt(item)`| Преобразование элемента в сообщение пользователя  
`compute_reward(item, result, ctx)`| Оценка развёртывания (0.0–1.0)  
`evaluate()`| Периодическая логика оценки  
## Основные компоненты[​](<#core-components> "Прямая ссылка на Основные компоненты")
### Цикл агента[​](<#agent-loop> "Прямая ссылка на Цикл агента")
`HermesAgentLoop` (`environments/agent_loop.py`) — это переиспользуемый движок многопользовательского агента. Он выполняет тот же шаблон вызова инструментов, что и основной цикл hermes-agent:
  1. Отправляет сообщения + схемы инструментов в API через `server.chat_completion()`
  2. Если ответ содержит `tool_calls`, отправляет каждый через `handle_function_call()`
  3. Добавляет результаты инструментов в диалог, возвращается к шагу 1
  4. Если `tool_calls` нет, агент завершает работу


Вызовы инструментов выполняются в пуле потоков (`ThreadPoolExecutor(128)`), чтобы асинхронные бэкенды (Modal, Docker) не вызывали взаимоблокировку внутри цикла событий Atropos.
Возвращает `AgentResult`:
[code] 
    @dataclass  
    class AgentResult:  
        messages: List[Dict[str, Any]]       # Полная история диалога  
        turns_used: int                       # Количество вызовов LLM  
        finished_naturally: bool              # True, если модель остановилась сама  
        reasoning_per_turn: List[Optional[str]]  # Извлечённое содержимое рассуждений  
        tool_errors: List[ToolError]          # Ошибки при выполнении инструментов  
        managed_state: Optional[Dict]         # Состояние VLLM ManagedServer (Фаза 2)  
    
[/code]
### Контекст инструментов[​](<#tool-context> "Прямая ссылка на Контекст инструментов")
`ToolContext` (`environments/tool_context.py`) предоставляет функциям награды прямой доступ к той же **песочнице**, которую модель использовала во время развёртывания. Область видимости `task_id` гарантирует сохранение всего состояния (файлы, процессы, вкладки браузера).
[code] 
    async def compute_reward(self, item, result, ctx: ToolContext):  
        # Запуск тестов в терминальной песочнице модели  
        test = ctx.terminal(\"pytest -v\")  
        if test[\"exit_code\"] == 0:  
            return 1.0  
      
        # Проверка, был ли создан файл  
        content = ctx.read_file(\"/workspace/solution.py\")  
        if content.get(\"content\"):  
            return 0.5  
      
        # Загрузка файлов для локальной проверки  
        ctx.download_file(\"/remote/output.bin\", \"/local/output.bin\")  
        return 0.0  
    
[/code]
Доступные методы:
Категория| Методы  
---|---  
**Терминал**| `terminal(command, timeout)`  
**Файлы**| `read_file(path)`, `write_file(path, content)`, `search(query, path)`  
**Передача**| `upload_file()`, `upload_dir()`, `download_file()`, `download_dir()`  
**Веб**| `web_search(query)`, `web_extract(urls)`  
**Браузер**| `browser_navigate(url)`, `browser_snapshot()`  
**Общее**| `call_tool(name, args)` — запасной выход для любого инструмента hermes-agent  
**Очистка**| `cleanup()` — освобождение всех ресурсов  
### Парсеры вызовов инструментов[​](<#tool-call-parsers> "Прямая ссылка на Парсеры вызовов инструментов")
Для **Фазы 2** (VLLM ManagedServer) сервер возвращает неформатированный текст без структурированных вызовов инструментов. Клиентские парсеры в `environments/tool_call_parsers/` извлекают `tool_calls` из необработанного вывода:
[code] 
    from environments.tool_call_parsers import get_parser  
      
    parser = get_parser(\"hermes\")  # или \"mistral\", \"llama3_json\", \"qwen\", \"deepseek_v3\", и т.д.  
    content, tool_calls = parser.parse(raw_model_output)  
    
[/code]
Доступные парсеры: `hermes`, `mistral`, `llama3_json`, `qwen`, `qwen3_coder`, `deepseek_v3`, `deepseek_v3_1`, `kimi_k2`, `longcat`, `glm45`, `glm47`.
В Фазе 1 (тип сервера OpenAI) парсеры не нужны — сервер обрабатывает разбор вызовов инструментов нативно.
## Доступные бенчмарки[​](<#available-benchmarks> "Прямая ссылка на Доступные бенчмарки")
### TerminalBench2[​](<#terminalbench2> "Прямая ссылка на TerminalBench2")
**89 сложных терминальных задач** с индивидуальными Docker-песочницами для каждой задачи.
|   
---|---  
**Что тестирует**|  Способность к выполнению одной задачи (кодинг/сисадмин)  
**Оценка**|  Бинарный провал/успех (проверка тестовым набором)  
**Песочница**|  Облачные песочницы Modal (индивидуальные Docker-образы для каждой задачи)  
**Инструменты**| `terminal` \\+ `file`  
**Задачи**|  89 задач из нескольких категорий  
**Стоимость**|  ~$50–200 за полную оценку (параллельное выполнение)  
**Время**|  ~2–4 часа
[code] 
    python environments/benchmarks/terminalbench_2/terminalbench2_env.py evaluate \\  
        --config environments/benchmarks/terminalbench_2/default.yaml  
      
    # Запуск конкретных задач  
    python environments/benchmarks/terminalbench_2/terminalbench2_env.py evaluate \\  
        --config environments/benchmarks/terminalbench_2/default.yaml \\  
        --env.task_filter fix-git,git-multibranch  
    
[/code]  
Датасет: [NousResearch/terminal-bench-2](<https://huggingface.co/datasets/NousResearch/terminal-bench-2>) на HuggingFace.
### TBLite (OpenThoughts Terminal Bench Lite)[​](<#tblite-openthoughts-terminal-bench-lite> "Прямая ссылка на TBLite \\(OpenThoughts Terminal Bench Lite\\)")
**100 задач с калиброванной сложностью** — более быстрый прокси для TerminalBench2.
|   
---|---  
**Что тестирует**|  То же, что и TB2 (кодинг/сисадмин), калиброванные уровни сложности  
**Оценка**|  Бинарный провал/успех  
**Песочница**|  Облачные песочницы Modal  
**Инструменты**| `terminal` \\+ `file`  
**Задачи**|  100 задач: Лёгкие (40), Средние (26), Сложные (26), Экстремальные (8)  
**Корреляция**|  r=0.911 с полным TB2  
**Скорость**|  в 2.6–8× быстрее TB2
[code] 
    python environments/benchmarks/tblite/tblite_env.py evaluate \\  
        --config environments/benchmarks/tblite/default.yaml  
    
[/code]  
TBLite — тонкий подкласс TerminalBench2: отличаются только датасет и таймауты. Создан командой OpenThoughts Agent (Snorkel AI + Bespoke Labs). Датасет: [NousResearch/openthoughts-tblite](<https://huggingface.co/datasets/NousResearch/openthoughts-tblite>).
### YC-Bench[​](<#yc-bench> "Прямая ссылка на YC-Bench")
**Стратегический бенчмарк с длинным горизонтом** — агент играет роль CEO AI-стартапа.
|   
---|---  
**Что тестирует**|  Многопользовательская стратегическая согласованность на сотнях шагов  
**Оценка**|  Составная: `0.5 × выживание + 0.5 × нормализованные_средства`  
**Песочница**|  Локальный терминал (Modal не требуется)  
**Инструменты**|  только `terminal`  
**Запуски**|  9 по умолчанию (3 пресета × 3 сида), последовательно  
**Стоимость**|  ~$50–200 за полную оценку  
**Время**|  ~3–6 часов
[code] 
    # Установка yc-bench (опциональная зависимость)  
    pip install \"hermes-agent[yc-bench]\"  
      
    # Запуск оценки  
    bash environments/benchmarks/yc_bench/run_eval.sh  
      
    # Или напрямую  
    python environments/benchmarks/yc_bench/yc_bench_env.py evaluate \\  
        --config environments/benchmarks/yc_bench/default.yaml  
      
    # Быстрый тест с одним пресетом  
    python environments/benchmarks/yc_bench/yc_bench_env.py evaluate \\  
        --config environments/benchmarks/yc_bench/default.yaml \\  
        --env.presets '[\"fast_test\"]' --env.seeds '[1]'  
    
[/code]  
YC-Bench использует [collinear-ai/yc-bench](<https://github.com/collinear-ai/yc-bench>) — детерминированную симуляцию с 4 областями навыков (research, inference, data_environment, training), системой престижа, управлением сотрудниками и финансовым давлением. В отличие от бинарной оценки по задачам TB2, YC-Bench измеряет, способен ли агент поддерживать согласованную стратегию на протяжении сотен взаимосвязанных решений.
## Учебные окружения[​](<#training-environments> "Прямая ссылка на Учебные окружения")
### TerminalTestEnv[​](<#terminaltestenv> "Прямая ссылка на TerminalTestEnv")
Минимальное самодостаточное окружение со встроенными задачами (без внешнего датасета). Используется для **сквозной проверки всего стека**. Каждая задача просит модель создать файл по известному пути; верификатор проверяет содержимое.
[code] 
    # Режим process (сохраняет развёртывания в JSONL, не требует сервера обучения)  
    python environments/terminal_test_env/terminal_test_env.py process \\  
        --env.data_path_to_save_groups terminal_test_output.jsonl  
      
    # Режим serve (подключается к API Atropos для RL-обучения)  
    python environments/terminal_test_env/terminal_test_env.py serve  
    
[/code]
### HermesSweEnv[​](<#hermessweenv> "Прямая ссылка на HermesSweEnv")
Учебное окружение в стиле SWE-bench. Модель получает задачу по программированию, использует инструменты terminal + file + web для её решения, а функция награды запускает тесты в той же Modal-песочнице.
[code] 
    python environments/hermes_swe_env/hermes_swe_env.py serve \\  
        --openai.model_name YourModel \\  
        --env.dataset_name bigcode/humanevalpack \\  
        --env.terminal_backend modal  
    
[/code]
## Запуск окружений[​](<#running-environments> "Прямая ссылка на Запуск окружений")
Каждое окружение — это отдельный Python-скрипт с тремя CLI-подкомандами:
### `evaluate` — Запуск бенчмарка[​](<#evaluate--run-a-benchmark> "Прямая ссылка на evaluate--run-a-benchmark")
Для окружений, предназначенных только для оценки (бенчмарков). Запускает все элементы, вычисляет метрики, логирует в wandb.
[code] 
    python environments/benchmarks/tblite/tblite_env.py evaluate \\  
        --config environments/benchmarks/tblite/default.yaml \\  
        --openai.model_name anthropic/claude-sonnet-4.6  
    
[/code]
Не требует сервера обучения или `run-api`. Окружение обрабатывает всё самостоятельно.
### `process` — Генерация SFT-данных[​](<#process--generate-sft-data> "Прямая ссылка на process--generate-sft-data")
Запускает развёртывания и сохраняет оценённые траектории в JSONL. Полезно для генерации данных обучения без полного цикла RL.
[code] 
    python environments/terminal_test_env/terminal_test_env.py process \\  
        --env.data_path_to_save_groups output.jsonl \\  
        --openai.model_name anthropic/claude-sonnet-4.6  
    
[/code]
Формат вывода: каждая строка — это оценённая траектория с полной историей диалога, наградой и метаданными.
### `serve` — Подключение к Atropos для RL-обучения[​](<#serve--connect-to-atropos-for-rl-training> "Прямая ссылка на serve--connect-to-atropos-for-rl-training")
Подключает окружение к работающему API-серверу Atropos (`run-api`). Используется во время активного RL-обучения.
[code] 
    # Терминал 1: Запуск API Atropos  
    run-api  
      
    # Терминал 2: Запуск окружения  
    python environments/hermes_swe_env/hermes_swe_env.py serve \\  
        --openai.model_name YourModel  
    
[/code]
Окружение получает элементы от Atropos, запускает развёртывания агента, вычисляет награды и отправляет оценённые траектории обратно для обучения.
## Двухфазная работа[​](<#two-phase-operation> "Прямая ссылка на Двухфазная работа")
### Фаза 1: Сервер OpenAI (Оценка / SFT)[​](<#phase-1-openai-server-eval--sft> "Прямая ссылка на Фаза 1: Сервер OpenAI \\(Оценка / SFT\\)")
Использует `server.chat_completion()` с параметром `tools=`. Сервер (VLLM, SGLang, OpenRouter, OpenAI) обрабатывает разбор вызовов инструментов нативно. Возвращает объекты `ChatCompletion` со структурированными `tool_calls`.
  * **Используется для**: оценки, генерации SFT-данных, бенчмарков, тестирования
  * **Плейсхолдеры токенов** создаются для конвейера Atropos (поскольку реальные ID токенов недоступны из API OpenAI)


### Фаза 2: VLLM ManagedServer (Полный RL)[​](<#phase-2-vllm-managedserver-full-rl> "Прямая ссылка на Фаза 2: VLLM ManagedServer \\(Полный RL\\)")
Использует ManagedServer для точных ID токенов + logprobs через `/generate`. Клиентский [парсер вызовов инструментов](<#tool-call-parsers>) восстанавливает структурированные `tool_calls` из необработанного вывода.
  * **Используется для**: полного RL-обучения с GRPO/PPO
  * **Реальные токены**, маски и logprobs проходят через конвейер
  * Установите `tool_call_parser` в конфиге в соответствии с форматом вашей модели (например, `\"hermes\"`, `\"qwen\"`, `\"mistral\"`)


## Создание окружений[​](<#creating-environments> "Прямая ссылка на Создание окружений")
### Учебное окружение[​](<#training-environment> "Прямая ссылка на Учебное окружение")
[code] 
    from environments.hermes_base_env import HermesAgentBaseEnv, HermesAgentEnvConfig  
    from atroposlib.envs.server_handling.server_manager import APIServerConfig  
      
    class MyEnvConfig(HermesAgentEnvConfig):  
        my_custom_field: str = \"default_value\"  
      
    class MyEnv(HermesAgentBaseEnv):  
        name = \"my-env\"  
        env_config_cls = MyEnvConfig  
      
        @classmethod  
        def config_init(cls):  
            env_config = MyEnvConfig(  
                enabled_toolsets=[\"terminal\", \"file\"],  
                terminal_backend=\"modal\",  
                max_agent_turns=30,  
            )  
            server_configs = [APIServerConfig(  
                base_url=\"https://openrouter.ai/api/v1\",  
                model_name=\"anthropic/claude-sonnet-4.6\",  
                server_type=\"openai\",  
            )]  
            return env_config, server_configs  
      
        async def setup(self):  
            from datasets import load_dataset  
            self.dataset = list(load_dataset(\"my-dataset\", split=\"train\"))  
            self.iter = 0  
      
        async def get_next_item(self):  
            item = self.dataset[self.iter % len(self.dataset)]  
            self.iter += 1  
            return item  
      
        def format_prompt(self, item):  
            return item[\"instruction\"]  
      
        async def compute_reward(self, item, result, ctx):  
            # ctx предоставляет полный доступ к инструментам песочницы развёртывания  
            test = ctx.terminal(\"pytest -v\")  
            return 1.0 if test[\"exit_code\"] == 0 else 0.0  
      
        async def evaluate(self, *args, **kwargs):  
            # Периодическая оценка во время обучения  
            pass  
      
    if __name__ == \"__main__\":  
        MyEnv.cli()  
    
[/code]
### Бенчмарк только для оценки[​](<#eval-only-benchmark> "Прямая ссылка на Бенчмарк только для оценки")
Для бенчмарков следуйте шаблону, используемому в TerminalBench2, TBLite и YC-Bench:
  1. **Создайте в** `environments/benchmarks/ваш-бенчмарк/`
  2. **Установите конфиг только для оценки**: `eval_handling=STOP_TRAIN`, `steps_per_eval=1`, `total_steps=1`
  3. **Заглушите методы обучения**: `collect_trajectories()` возвращает `(None, [])`, `score()` возвращает `None`
  4. **Реализуйте** `rollout_and_score_eval(eval_item)` — цикл агента + оценка для каждого элемента
  5. **Реализуйте** `evaluate()` — оркестрирует все запуски, вычисляет агрегированные метрики
  6. **Добавьте потоковый JSONL** для отказоустойчивого сохранения результатов
  7. **Добавьте очистку**: обработка `KeyboardInterrupt`, `cleanup_all_environments()`, `_tool_executor.shutdown()`
  8. **Запускайте с** подкомандой `evaluate`


Смотрите `environments/benchmarks/yc_bench/yc_bench_env.py` как чистый, хорошо документированный эталонный пример.
## Справочник по конфигурации[​](<#configuration-reference> "Прямая ссылка на Справочник по конфигурации")
### Поля HermesAgentEnvConfig[​](<#hermesagentenvconfig-fields> "Прямая ссылка на Поля HermesAgentEnvConfig")
Поле| Тип| По умолчанию| Описание  
---|---|---|---  
`enabled_toolsets`| `List[str]`| `None` (все)| Какие наборы инструментов hermes включить  
`disabled_toolsets`| `List[str]`| `None`| Наборы инструментов для исключения  
`distribution`| `str`| `None`| Имя вероятностного распределения наборов инструментов  
`max_agent_turns`| `int`| `30`| Максимальное количество вызовов LLM на одно развёртывание  
`agent_temperature`| `float`| `1.0`| Температура сэмплирования  
`system_prompt`| `str`| `None`| Системное сообщение для агента  
`terminal_backend`| `str`| `\"local\"`| `local`, `docker`, `modal`, `daytona`, `ssh`, `singularity`  
`terminal_timeout`| `int`| `120`| Секунд на одну терминальную команду  
`terminal_lifetime`| `int`| `3600`| Максимальное время жизни песочницы  
`dataset_name`| `str`| `None`| Идентификатор датасета HuggingFace  
`tool_pool_size`| `int`| `128`| Размер пула потоков для выполнения инструментов  
`tool_call_parser`| `str`| `\"hermes\"`| Парсер для необработанного вывода Фазы 2  
`extra_body`| `Dict`| `None`| Дополнительные параметры для OpenAI API (например, предпочтения провайдера OpenRouter)  
`eval_handling`| `Enum`| `STOP_TRAIN`| `STOP_TRAIN`, `LIMIT_TRAIN`, `NONE`  
### YAML-конфигурация[​](<#yaml-configuration> "Прямая ссылка на YAML-конфигурация")
Окружения могут быть настроены через YAML-файлы, передаваемые с `--config`:
[code] 
    env:  
      enabled_toolsets: [\"terminal\", \"file\"]  
      max_agent_turns: 60  
      max_token_length: 32000  
      agent_temperature: 0.8  
      terminal_backend: \"modal\"  
      terminal_timeout: 300  
      dataset_name: \"NousResearch/terminal-bench-2\"  
      tokenizer_name: \"NousResearch/Hermes-3-Llama-3.1-8B\"  
      use_wandb: true  
      wandb_name: \"my-benchmark\"  
      
    openai:  
      base_url: \"https://openrouter.ai/api/v1\"  
      model_name: \"anthropic/claude-sonnet-4.6\"  
      server_type: \"openai\"  
      health_check: false  
    
[/code]
Значения YAML переопределяют значения по умолчанию из `config_init()`. Аргументы CLI переопределяют значения YAML:
[code] 
    python my_env.py evaluate \\  
        --config my_config.yaml \\  
        --openai.model_name anthropic/claude-opus-4.6  # переопределяет YAML  
    
[/code]
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
### Для всех окружений[​](<#for-all-environments> "Прямая ссылка на Для всех окружений")
  * Python >= 3.11
  * `atroposlib`: `pip install git+https://github.com/NousResearch/atropos.git`
  * Ключ API LLM (OpenRouter, OpenAI или собственный VLLM/SGLang)


### Для бенчмарков с Modal-песочницами (TB2, TBLite)[​](<#for-modal-sandboxed-benchmarks-tb2-tblite> "Прямая ссылка на Для бенчмарков с Modal-песочницами \\(TB2, TBLite\\)")
  * Аккаунт [Modal](<https://modal.com>) и CLI: `pip install \"hermes-agent[modal]\"`
  * Переменные окружения `MODAL_TOKEN_ID` и `MODAL_TOKEN_SECRET`


### Для YC-Bench[​](<#for-yc-bench> "Прямая ссылка на Для YC-Bench")
  * `pip install \"hermes-agent[yc-bench]\"` (устанавливает CLI yc-bench + SQLAlchemy)
  * Modal не требуется — работает с локальным терминальным бэкендом


### Для RL-обучения[​](<#for-rl-training> "Прямая ссылка на Для RL-обучения")
  * `TINKER_API_KEY` — ключ API для сервиса обучения [Tinker](<https://tinker.computer>)
  * `WANDB_API_KEY` — для отслеживания метрик Weights & Biases
  * Подмодуль `tinker-atropos` (находится в `tinker-atropos/` в репозитории)


Смотрите [RL-обучение](</docs/user-guide/features/rl-training>) для агентного рабочего процесса RL.
## Структура директорий[​](<#directory-structure> "Прямая ссылка на Структура директорий")
[code] 
    environments/  
    ├── hermes_base_env.py          # Абстрактный базовый класс (HermesAgentBaseEnv)  
    ├── agent_loop.py               # Движок многопользовательского агента (HermesAgentLoop)  
    ├── tool_context.py             # Доступ к инструментам для функций награды (по развёртыванию)  
    ├── patches.py                  # Патчи асинхронной безопасности для Modal-бэкенда  
    │  
    ├── tool_call_parsers/          # Клиентские парсеры для Фазы 2  
    │   ├── hermes_parser.py        # Формат Hermes/ChatML <tool_call>  
    │   ├── mistral_parser.py       # Формат Mistral [TOOL_CALLS]  
    │   ├── llama_parser.py         # JSON-вызов инструментов Llama 3  
    │   ├── qwen_parser.py          # Формат Qwen  
    │   ├── deepseek_v3_parser.py   # Формат DeepSeek V3  
    │   └── ...                     # + kimi_k2, longcat, glm45/47, и т.д.  
    │  
    ├── terminal_test_env/          # Проверка стека (встроенные задачи)  
    ├── hermes_swe_env/             # Учебное окружение SWE-bench  
    │  
    └── benchmarks/                 # Бенчмарки для оценки  
        ├── terminalbench_2/        # 89 терминальных задач, Modal-песочницы  
        ├── tblite/                 # 100 калиброванных задач (быстрый прокси TB2)  
        └── yc_bench/               # Стратегический бенчмарк с длинным горизонтом  
    
[/code]
  * [Архитектура](<#architecture>)
    * [BaseEnv (Atropos)](<#baseenv-atropos>)
    * [HermesAgentBaseEnv](<#hermesagentbaseenv>)
    * [Конкретные окружения](<#concrete-environments>)
  * [Основные компоненты](<#core-components>)
    * [Цикл агента](<#agent-loop>)
    * [Контекст инструментов](<#tool-context>)
    * [Парсеры вызовов инструментов](<#tool-call-parsers>)
  * [Доступные бенчмарки](<#available-benchmarks>)
    * [TerminalBench2](<#terminalbench2>)
    * [TBLite (OpenThoughts Terminal Bench Lite)](<#tblite-openthoughts-terminal-bench-lite>)
    * [YC-Bench](<#yc-bench>)
  * [Учебные окружения](<#training-environments>)
    * [TerminalTestEnv](<#terminaltestenv>)
    * [HermesSweEnv](<#hermessweenv>)
  * [Запуск окружений](<#running-environments>)
    * [`evaluate` — Запуск бенчмарка](<#evaluate--run-a-benchmark>)
    * [`process` — Генерация SFT-данных](<#process--generate-sft-data>)
    * [`serve` — Подключение к Atropos для RL-обучения](<#serve--connect-to-atropos-for-rl-training>)
  * [Двухфазная работа](<#two-phase-operation>)
    * [Фаза 1: Сервер OpenAI (Оценка / SFT)](<#phase-1-openai-server-eval--sft>)
    * [Фаза 2: VLLM ManagedServer (Полный RL)](<#phase-2-vllm-managedserver-full-rl>)
  * [Создание окружений](<#creating-environments>)
    * [Учебное окружение](<#training-environment>)
    * [Бенчмарк только для оценки](<#eval-only-benchmark>)
  * [Справочник по конфигурации](<#configuration-reference>)
    * [Поля HermesAgentEnvConfig](<#hermesagentenvconfig-fields>)
    * [YAML-конфигурация](<#yaml-configuration>)
  * [Предварительные требования](<#prerequisites>)
    * [Для всех окружений](<#for-all-environments>)
    * [Для бенчмарков с Modal-песочницами (TB2, TBLite)](<#for-modal-sandboxed-benchmarks-tb2-tblite>)
    * [Для YC-Bench](<#for-yc-bench>)
    * [Для RL-обучения](<#for-rl-training>)
  * [Структура директорий](<#directory-structure>)




<!-- Источник: https://hermes-agent.nousresearch.com/docs/developer-guide/environments -->
