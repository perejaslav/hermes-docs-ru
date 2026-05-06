On this page
Эта страница — карта внутреннего устройства Hermes Agent верхнего уровня. Используйте её для ориентации в кодовой базе, затем переходите к документации по конкретным подсистемам для получения деталей реализации.
## System Overview[​](<#system-overview> "Direct link to System Overview")

[code] 
    ┌─────────────────────────────────────────────────────────────────────┐  
    │                        Entry Points                                  │  
    │                                                                      │  
    │  CLI (cli.py)    Gateway (gateway/run.py)    ACP (acp_adapter/)     │  
    │  Batch Runner    API Server                  Python Library          │  
    └──────────┬──────────────┬───────────────────────┬───────────────────┘  
               │              │                       │  
               ▼              ▼                       ▼  
    ┌─────────────────────────────────────────────────────────────────────┐  
    │                     AIAgent (run_agent.py)                          │  
    │                                                                     │  
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  
    │  │ Prompt       │  │ Provider     │  │ Tool         │               │  
    │  │ Builder      │  │ Resolution   │  │ Dispatch     │               │  
    │  │ (prompt_     │  │ (runtime_    │  │ (model_      │               │  
    │  │  builder.py) │  │  provider.py)│  │  tools.py)   │               │  
    │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │  
    │         │                 │                 │                       │  
    │  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐               │  
    │  │ Compression  │  │ 3 API Modes  │  │ Tool Registry│               │  
    │  │ & Caching    │  │ chat_compl.  │  │ (registry.py)│               │  
    │  │              │  │ codex_resp.  │  │ 61 tools     │               │  
    │  │              │  │ anthropic    │  │ 52 toolsets  │               │  
    │  └──────────────┘  └──────────────┘  └──────────────┘               │  
    └─────────┴─────────────────┴─────────────────┴───────────────────────┘  
               │                                    │  
               ▼                                    ▼  
    ┌───────────────────┐              ┌──────────────────────┐  
    │ Session Storage   │              │ Tool Backends         │  
    │ (SQLite + FTS5)   │              │ Terminal (7 backends) │  
    │ hermes_state.py   │              │ Browser (5 backends)  │  
    │ gateway/session.py│              │ Web (4 backends)      │  
    └───────────────────┘              │ MCP (dynamic)         │  
                                       │ File, Vision, etc.    │  
                                       └──────────────────────┘  
    
[/code]

## Directory Structure[​](<#directory-structure> "Direct link to Directory Structure")

[code] 
    hermes-agent/  
    ├── run_agent.py              # AIAgent — основной цикл диалога (~13 700 строк)  
    ├── cli.py                    # HermesCLI — интерактивный терминальный интерфейс (~11 500 строк)  
    ├── model_tools.py            # Обнаружение инструментов, сбор схем, диспетчеризация  
    ├── toolsets.py               # Группировка инструментов и предустановки для платформ  
    ├── hermes_state.py           # SQLite база данных сессий/состояния с FTS5  
    ├── hermes_constants.py       # HERMES_HOME, пути с учётом профиля  
    ├── batch_runner.py           # Пакетная генерация траекторий  
    │  
    ├── agent/                    # Внутренности агента  
    │   ├── prompt_builder.py     # Сборка системного промпта  
    │   ├── context_engine.py     # ContextEngine ABC (подключаемый)  
    │   ├── context_compressor.py # Движок по умолчанию — lossy-суммаризация  
    │   ├── prompt_caching.py     # Кеширование промптов Anthropic  
    │   ├── auxiliary_client.py   # Вспомогательная LLM для побочных задач (зрение, суммаризация)  
    │   ├── model_metadata.py     # Длины контекста моделей, оценка токенов  
    │   ├── models_dev.py         # Интеграция с реестром models.dev  
    │   ├── anthropic_adapter.py  # Конвертация формата Anthropic Messages API  
    │   ├── display.py            # KawaiiSpinner, форматирование предпросмотра инструментов  
    │   ├── skill_commands.py     # Слэш-команды скиллов  
    │   ├── memory_manager.py    # Оркестрация менеджера памяти  
    │   ├── memory_provider.py   # ABC провайдера памяти  
    │   └── trajectory.py         # Вспомогательные функции сохранения траекторий  
    │  
    ├── hermes_cli/               # Подкоманды CLI и настройка  
    │   ├── main.py               # Точка входа — все подкоманды `hermes` (~10 400 строк)  
    │   ├── config.py             # DEFAULT_CONFIG, OPTIONAL_ENV_VARS, миграция  
    │   ├── commands.py           # COMMAND_REGISTRY — центральное определение слэш-команд  
    │   ├── auth.py               # PROVIDER_REGISTRY, разрешение учётных данных  
    │   ├── runtime_provider.py   # Provider → api_mode + учётные данные  
    │   ├── models.py             # Каталог моделей, списки моделей провайдеров  
    │   ├── model_switch.py       # Логика /model (общая для CLI и gateway)  
    │   ├── setup.py              # Интерактивный мастер настройки (~3 500 строк)  
    │   ├── skin_engine.py        # Движок тем CLI  
    │   ├── skills_config.py      # hermes skills — включение/отключение по платформам  
    │   ├── skills_hub.py         # Слэш-команда /skills  
    │   ├── tools_config.py       # hermes tools — включение/отключение по платформам  
    │   ├── plugins.py            # PluginManager — обнаружение, загрузка, хуки  
    │   ├── callbacks.py          # Терминальные колбэки (clarify, sudo, approval)  
    │   └── gateway.py            # hermes gateway start/stop  
    │  
    ├── tools/                    # Реализации инструментов (один файл на инструмент)  
    │   ├── registry.py           # Центральный реестр инструментов  
    │   ├── approval.py           # Обнаружение опасных команд  
    │   ├── terminal_tool.py      # Оркестрация терминала  
    │   ├── process_registry.py   # Управление фоновыми процессами  
    │   ├── file_tools.py         # read_file, write_file, patch, search_files  
    │   ├── web_tools.py          # web_search, web_extract  
    │   ├── browser_tool.py       # 10 инструментов автоматизации браузера  
    │   ├── code_execution_tool.py # Песочница execute_code  
    │   ├── delegate_tool.py      # Делегирование сабагентам  
    │   ├── mcp_tool.py           # MCP-клиент (~3 100 строк)  
    │   ├── credential_files.py   # Передача учётных данных из файлов  
    │   ├── env_passthrough.py    # Проброс переменных окружения для песочниц  
    │   ├── ansi_strip.py         # Удаление ANSI-escape последовательностей  
    │   └── environments/         # Бэкенды терминала (local, docker, ssh, modal, daytona, singularity)  
    │  
    ├── gateway/                  # Шлюз для мессенджеров  
    │   ├── run.py                # GatewayRunner — диспетчеризация сообщений (~12 200 строк)  
    │   ├── session.py            # SessionStore — сохранение диалогов  
    │   ├── delivery.py           # Доставка исходящих сообщений  
    │   ├── pairing.py            # Авторизация через DM-привязку  
    │   ├── hooks.py              # Обнаружение хуков и события жизненного цикла  
    │   ├── mirror.py             # Межсессионное зеркалирование сообщений  
    │   ├── status.py             # Блокировки токенов, отслеживание процессов с учётом профиля  
    │   ├── builtin_hooks/        # Точка расширения для всегда зарегистрированных хуков (не поставляются)  
    │   └── platforms/            # 20 адаптеров: telegram, discord, slack, whatsapp,  
    │                             #   signal, matrix, mattermost, email, sms,  
    │                             #   dingtalk, feishu, wecom, wecom_callback, weixin,  
    │                             #   bluebubbles, qqbot, homeassistant, webhook, api_server,  
    │                             #   yuanbao  
    │  
    ├── acp_adapter/              # ACP-сервер (VS Code / Zed / JetBrains)  
    ├── cron/                     # Планировщик (jobs.py, scheduler.py)  
    ├── plugins/memory/           # Плагины провайдеров памяти  
    ├── plugins/context_engine/   # Плагины движка контекста  
    ├── environments/             # Среды для RL-обучения (Atropos)  
    ├── skills/                   # Встроенные скиллы (всегда доступны)  
    ├── optional-skills/          # Официальные опциональные скиллы (устанавливаются явно)  
    ├── website/                  # Сайт документации Docusaurus  
    └── tests/                    # Набор тестов pytest (~3 000+ тестов)  
    
[/code]

## Data Flow[​](<#data-flow> "Direct link to Data Flow")

### CLI Session[​](<#cli-session> "Direct link to CLI Session")

[code] 
    User input → HermesCLI.process_input()  
      → AIAgent.run_conversation()  
        → prompt_builder.build_system_prompt()  
        → runtime_provider.resolve_runtime_provider()  
        → API call (chat_completions / codex_responses / anthropic_messages)  
        → tool_calls? → model_tools.handle_function_call() → loop  
        → final response → display → save to SessionDB  
    
[/code]

### Gateway Message[​](<#gateway-message> "Direct link to Gateway Message")

[code] 
    Platform event → Adapter.on_message() → MessageEvent  
      → GatewayRunner._handle_message()  
        → authorize user  
        → resolve session key  
        → create AIAgent with session history  
        → AIAgent.run_conversation()  
        → deliver response back through adapter  
    
[/code]

### Cron Job[​](<#cron-job> "Direct link to Cron Job")

[code] 
    Scheduler tick → load due jobs from jobs.json  
      → create fresh AIAgent (no history)  
      → inject attached skills as context  
      → run job prompt  
      → deliver response to target platform  
      → update job state and next_run  
    
[/code]

## Recommended Reading Order[​](<#recommended-reading-order> "Direct link to Recommended Reading Order")

Если вы новичок в кодовой базе:
  1. **Эта страница** — сориентируйтесь
  2. **[Agent Loop Internals](</docs/developer-guide/agent-loop>)** — как работает AIAgent
  3. **[Prompt Assembly](</docs/developer-guide/prompt-assembly>)** — построение системного промпта
  4. **[Provider Runtime Resolution](</docs/developer-guide/provider-runtime>)** — как выбираются провайдеры
  5. **[Adding Providers](</docs/developer-guide/adding-providers>)** — практическое руководство по добавлению нового провайдера
  6. **[Tools Runtime](</docs/developer-guide/tools-runtime>)** — реестр инструментов, диспетчеризация, окружения
  7. **[Session Storage](</docs/developer-guide/session-storage>)** — схема SQLite, FTS5, lineage сессий
  8. **[Gateway Internals](</docs/developer-guide/gateway-internals>)** — шлюз для мессенджеров
  9. **[Context Compression & Prompt Caching](</docs/developer-guide/context-compression-and-caching>)** — сжатие и кеширование
  10. **[ACP Internals](</docs/developer-guide/acp-internals>)** — интеграция с IDE
  11. **[Environments, Benchmarks & Data Generation](</docs/developer-guide/environments>)** — RL-обучение


## Major Subsystems[​](<#major-subsystems> "Direct link to Major Subsystems")

### Agent Loop[​](<#agent-loop> "Direct link to Agent Loop")

Синхронный движок оркестрации (`AIAgent` в `run_agent.py`). Обрабатывает выбор провайдера, построение промпта, выполнение инструментов, повторные попытки, fallback, колбэки, сжатие и сохранение. Поддерживает три режима API для различных бэкендов провайдеров.
→ [Agent Loop Internals](</docs/developer-guide/agent-loop>)

### Prompt System[​](<#prompt-system> "Direct link to Prompt System")

Построение и поддержание промпта на протяжении жизненного цикла диалога:
  * **`prompt_builder.py`** — Собирает системный промпт из: личности (SOUL.md), памяти (MEMORY.md, USER.md), скиллов, контекстных файлов (AGENTS.md, .hermes.md), инструкций по использованию инструментов и инструкций, специфичных для модели
  * **`prompt_caching.py`** — Применяет Anthropic cache breakpoints для префиксного кеширования
  * **`context_compressor.py`** — Суммаризирует средние части диалога, когда контекст превышает пороговые значения


→ [Prompt Assembly](</docs/developer-guide/prompt-assembly>), [Context Compression & Prompt Caching](</docs/developer-guide/context-compression-and-caching>)

### Provider Resolution[​](<#provider-resolution> "Direct link to Provider Resolution")

Общий разрешитель времени выполнения, используемый CLI, gateway, cron, ACP и вспомогательными вызовами. Преобразует пары `(provider, model)` в `(api_mode, api_key, base_url)`. Обрабатывает 18+ провайдеров, OAuth-потоки, пулы учётных данных и разрешение алиасов.
→ [Provider Runtime Resolution](</docs/developer-guide/provider-runtime>)

### Tool System[​](<#tool-system> "Direct link to Tool System")

Центральный реестр инструментов (`tools/registry.py`) с 61 зарегистрированным инструментом в 52 наборах инструментов. Каждый файл инструмента саморегистрируется во время импорта. Реестр обрабатывает сбор схем, диспетчеризацию, проверку доступности и обёртывание ошибок. Инструменты терминала поддерживают 7 бэкендов (local, Docker, SSH, Daytona, Modal, Singularity, Vercel Sandbox).
→ [Tools Runtime](</docs/developer-guide/tools-runtime>)

### Session Persistence[​](<#session-persistence> "Direct link to Session Persistence")

Хранение сессий на базе SQLite с полнотекстовым поиском FTS5. Сессии имеют отслеживание lineage (родитель/потомок при сжатиях), изоляцию по платформам и атомарные записи с обработкой конкурентного доступа.
→ [Session Storage](</docs/developer-guide/session-storage>)

### Messaging Gateway[​](<#messaging-gateway> "Direct link to Messaging Gateway")

Долгоживущий процесс с 20 адаптерами платформ, единой маршрутизацией сессий, авторизацией пользователей (белые списки + DM-привязка), диспетчеризацией слэш-команд, системой хуков, тиканьем cron и фоновым обслуживанием.
→ [Gateway Internals](</docs/developer-guide/gateway-internals>)

### Plugin System[​](<#plugin-system> "Direct link to Plugin System")

Три источника обнаружения: `~/.hermes/plugins/` (пользователь), `.hermes/plugins/` (проект) и pip entry points. Плагины регистрируют инструменты, хуки и CLI-команды через контекстный API. Существует два специализированных типа плагинов: провайдеры памяти (`plugins/memory/`) и движки контекста (`plugins/context_engine/`). Оба являются single-select — одновременно может быть активен только один каждого типа, настраивается через `hermes plugins` или `config.yaml`.
→ [Plugin Guide](</docs/guides/build-a-hermes-plugin>), [Memory Provider Plugin](</docs/developer-guide/memory-provider-plugin>)

### Cron[​](<#cron> "Direct link to Cron")

Полноценные задачи агента (не shell-задачи). Задачи хранятся в JSON, поддерживают несколько форматов расписания, могут подключать скиллы и скрипты, доставляют результаты на любую платформу.
→ [Cron Internals](</docs/developer-guide/cron-internals>)

### ACP Integration[​](<#acp-integration> "Direct link to ACP Integration")

Предоставляет Hermes как агента, встроенного в редактор, через stdio/JSON-RPC для VS Code, Zed и JetBrains.
→ [ACP Internals](</docs/developer-guide/acp-internals>)

### RL / Environments / Trajectories[​](<#rl--environments--trajectories> "Direct link to RL / Environments / Trajectories")

Полная среда для оценки и RL-обучения. Интегрируется с Atropos, поддерживает несколько парсеров вызовов инструментов и генерирует траектории в формате ShareGPT.
→ [Environments, Benchmarks & Data Generation](</docs/developer-guide/environments>), [Trajectories & Training Format](</docs/developer-guide/trajectory-format>)

## Design Principles[​](<#design-principles> "Direct link to Design Principles")

Principle| What it means in practice  
---|---  
**Стабильность промпта**|  Системный промпт не меняется в середине диалога. Никаких мутаций, ломающих кеш, кроме явных действий пользователя (`/model`).  
**Наблюдаемое выполнение**|  Каждый вызов инструмента виден пользователю через колбэки. Обновления прогресса в CLI (спиннер) и gateway (сообщения в чате).  
**Прерываемость**|  API-вызовы и выполнение инструментов могут быть отменены на лету пользовательским вводом или сигналами.  
**Платформонезависимое ядро**|  Один класс AIAgent обслуживает CLI, gateway, ACP, batch и API-сервер. Различия платформ находятся в точке входа, а не в агенте.  
**Слабая связанность**|  Опциональные подсистемы (MCP, плагины, провайдеры памяти, RL-среды) используют паттерны реестров и gating через check_fn, а не жёсткие зависимости.  
**Изоляция профилей**|  Каждый профиль (`hermes -p <name>`) получает свой HERMES_HOME, конфиг, память, сессии и PID gateway. Несколько профилей работают одновременно.  

## File Dependency Chain[​](<#file-dependency-chain> "Direct link to File Dependency Chain")

[code] 
    tools/registry.py  (нет зависимостей — импортируется всеми файлами инструментов)  
           ↑  
    tools/*.py  (каждый вызывает registry.register() во время импорта)  
           ↑  
    model_tools.py  (импортирует tools/registry + запускает обнаружение инструментов)  
           ↑  
    run_agent.py, cli.py, batch_runner.py, environments/  
    
[/code]

Эта цепочка означает, что регистрация инструментов происходит во время импорта, до создания любого экземпляра агента. Любой файл `tools/*.py` с вызовом `registry.register()` на верхнем уровне обнаруживается автоматически — ручной импорт не требуется.

  * [System Overview](<#system-overview>)
  * [Directory Structure](<#directory-structure>)
  * [Data Flow](<#data-flow>)
    * [CLI Session](<#cli-session>)
    * [Gateway Message](<#gateway-message>)
    * [Cron Job](<#cron-job>)
  * [Recommended Reading Order](<#recommended-reading-order>)
  * [Major Subsystems](<#major-subsystems>)
    * [Agent Loop](<#agent-loop>)
    * [Prompt System](<#prompt-system>)
    * [Provider Resolution](<#provider-resolution>)
    * [Tool System](<#tool-system>)
    * [Session Persistence](<#session-persistence>)
    * [Messaging Gateway](<#messaging-gateway>)
    * [Plugin System](<#plugin-system>)
    * [Cron](<#cron>)
    * [ACP Integration](<#acp-integration>)
    * [RL / Environments / Trajectories](<#rl--environments--trajectories>)
  * [Design Principles](<#design-principles>)
  * [File Dependency Chain](<#file-dependency-chain>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture -->
