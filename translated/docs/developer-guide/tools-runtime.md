На этой странице
Инструменты Hermes — это саморегистрирующиеся функции, сгруппированные в наборы инструментов и выполняемые через центральную систему реестра/диспетчеризации.
Основные файлы:
  * `tools/registry.py`
  * `model_tools.py`
  * `toolsets.py`
  * `tools/terminal_tool.py`
  * `tools/environments/*`


## Модель регистрации инструментов[​](<#tool-registration-model> "Прямая ссылка на Модель регистрации инструментов")
Каждый модуль инструментов вызывает `registry.register(...)` во время импорта.
`model_tools.py` отвечает за импорт/обнаружение модулей инструментов и построение списка схем, используемых моделью.
### Как работает `registry.register()`[​](<#how-registryregister-works> "Прямая ссылка на как работает registry-register")
Каждый файл инструментов в `tools/` вызывает `registry.register()` на уровне модуля, чтобы зарегистрировать себя. Сигнатура функции:
[code] 
    registry.register(  
        name="terminal",               # Unique tool name (used in API schemas)  
        toolset="terminal",            # Toolset this tool belongs to  
        schema={...},                  # OpenAI function-calling schema (description, parameters)  
        handler=handle_terminal,       # The function that executes when the tool is called  
        check_fn=check_terminal,       # Optional: returns True/False for availability  
        requires_env=["SOME_VAR"],     # Optional: env vars needed (for UI display)  
        is_async=False,                # Whether the handler is an async coroutine  
        description="Run commands",    # Human-readable description  
        emoji="💻",                    # Emoji for spinner/progress display  
    )  
    
[/code]
Каждый вызов создаёт `ToolEntry`, хранящийся в словаре `ToolRegistry._tools` (синглтон) с ключом по имени инструмента. При коллизии имён между наборами инструментов регистрируется предупреждение, и более поздняя регистрация перезаписывает предыдущую.
### Обнаружение: `discover_builtin_tools()`[​](<#discovery-discover_builtin_tools> "Прямая ссылка на обнаружение-discover_builtin_tools")
При импорте `model_tools.py` вызывается `discover_builtin_tools()` из `tools/registry.py`. Эта функция сканирует все файлы `tools/*.py` с помощью AST-парсинга для поиска модулей, содержащих вызовы `registry.register()` верхнего уровня, затем импортирует их:
[code] 
    # tools/registry.py (simplified)  
    def discover_builtin_tools(tools_dir=None):  
        tools_path = Path(tools_dir) if tools_dir else Path(__file__).parent  
        for path in sorted(tools_path.glob("*.py")):  
            if path.name in {"__init__.py", "registry.py", "mcp_tool.py"}:  
                continue  
            if _module_registers_tools(path):  # AST check for top-level registry.register()  
                importlib.import_module(f"tools.{path.stem}")  
    
[/code]
Это автообнаружение означает, что новые файлы инструментов подхватываются автоматически — не нужно поддерживать ручной список. AST-проверка сопоставляет только вызовы `registry.register()` верхнего уровня (не вызовы внутри функций), поэтому вспомогательные модули в `tools/` не импортируются.
Каждый импорт запускает вызовы `registry.register()` модуля. Ошибки в опциональных инструментах (например, отсутствие `fal_client` для генерации изображений) перехватываются и логируются — они не препятствуют загрузке остальных инструментов.
После обнаружения основных инструментов также обнаруживаются MCP-инструменты и плагины:
  1. **MCP-инструменты** — `tools.mcp_tool.discover_mcp_tools()` читает конфигурацию MCP-сервера и регистрирует инструменты из внешних серверов.
  2. **Плагины** — `hermes_cli.plugins.discover_plugins()` загружает пользовательские/проектные/pip-плагины, которые могут регистрировать дополнительные инструменты.


## Проверка доступности инструментов (`check_fn`)[​](<#tool-availability-checking-check_fn> "Прямая ссылка на проверку-доступности-инструментов-check_fn")
Каждый инструмент может опционально предоставлять `check_fn` — вызываемый объект, который возвращает `True`, когда инструмент доступен, и `False` в противном случае. Типичные проверки включают:
  * **Наличие API-ключа** — например, `lambda: bool(os.environ.get("SERP_API_KEY"))` для веб-поиска
  * **Запущен ли сервис** — например, проверка настроен ли сервер Honcho
  * **Установлен ли бинарник** — например, проверка доступности `playwright` для инструментов браузера


Когда `registry.get_definitions()` строит список схем для модели, он запускает `check_fn()` каждого инструмента:
[code] 
    # Simplified from registry.py  
    if entry.check_fn:  
        try:  
            available = bool(entry.check_fn())  
        except Exception:  
            available = False   # Exceptions = unavailable  
        if not available:  
            continue            # Skip this tool entirely  
    
[/code]
Ключевые особенности:
  * Результаты проверки **кэшируются на один вызов** — если несколько инструментов используют одинаковый `check_fn`, он выполняется только один раз.
  * Исключения в `check_fn()` трактуются как «недоступен» (отказобезопасное поведение).
  * Метод `is_toolset_available()` проверяет, проходит ли `check_fn` набора инструментов; используется для отображения в UI и разрешения наборов инструментов.


## Разрешение наборов инструментов[​](<#toolset-resolution> "Прямая ссылка на Разрешение наборов инструментов")
Наборы инструментов — это именованные группы инструментов. Hermes разрешает их через:
  * явные списки включённых/отключённых наборов инструментов
  * предустановки платформы (`hermes-cli`, `hermes-telegram` и т.д.)
  * динамические MCP-наборы
  * специальные наборы для конкретных целей, такие как `hermes-acp`


### Как `get_tool_definitions()` фильтрует инструменты[​](<#how-get_tool_definitions-filters-tools> "Прямая ссылка на как-get_tool_definitions-фильтрует-инструменты")
Основная точка входа — `model_tools.get_tool_definitions(enabled_toolsets, disabled_toolsets, quiet_mode)`:
  1. **Если указан `enabled_toolsets`** — включаются только инструменты из этих наборов. Каждое имя набора разрешается через `resolve_toolset()`, которая раскрывает составные наборы в отдельные имена инструментов.
  2. **Если указан `disabled_toolsets`** — начинаем со ВСЕХ наборов, затем вычитаем отключённые.
  3. **Если не указано ни то, ни другое** — включаются все известные наборы инструментов.
  4. **Фильтрация реестром** — разрешённый набор имён инструментов передаётся в `registry.get_definitions()`, который применяет фильтрацию через `check_fn` и возвращает схемы в формате OpenAI.
  5. **Динамическое изменение схем** — после фильтрации схемы `execute_code` и `browser_navigate` динамически корректируются, чтобы ссылаться только на инструменты, прошедшие фильтрацию (предотвращает галлюцинирование модели о недоступных инструментах).


### Устаревшие имена наборов инструментов[​](<#legacy-toolset-names> "Прямая ссылка на Устаревшие имена наборов инструментов")
Старые имена наборов с суффиксами `_tools` (например, `web_tools`, `terminal_tools`) сопоставляются с современными именами через `_LEGACY_TOOLSET_MAP` для обратной совместимости.
## Диспетчеризация[​](<#dispatch> "Прямая ссылка на Диспетчеризация")
Во время выполнения инструменты диспетчеризируются через центральный реестр, с исключениями для некоторых инструментов уровня агента, таких как обработка memory/todo/session-search.
### Поток диспетчеризации: model tool_call → выполнение обработчика[​](<#dispatch-flow-model-tool_call--handler-execution> "Прямая ссылка на Поток диспетчеризации: model tool_call → выполнение обработчика")
Когда модель возвращает `tool_call`, поток выглядит следующим образом:
[code] 
    Model response with tool_call  
        ↓  
    run_agent.py agent loop  
        ↓  
    model_tools.handle_function_call(name, args, task_id, user_task)  
        ↓  
    [Agent-loop tools?] → handled directly by agent loop (todo, memory, session_search, delegate_task)  
        ↓  
    [Plugin pre-hook] → invoke_hook("pre_tool_call", ...)  
        ↓  
    registry.dispatch(name, args, **kwargs)  
        ↓  
    Look up ToolEntry by name  
        ↓  
    [Async handler?] → bridge via _run_async()  
    [Sync handler?]  → call directly  
        ↓  
    Return result string (or JSON error)  
        ↓  
    [Plugin post-hook] → invoke_hook("post_tool_call", ...)  
    
[/code]
### Оборачивание ошибок[​](<#error-wrapping> "Прямая ссылка на Оборачивание ошибок")
Всё выполнение инструментов обёрнуто в обработку ошибок на двух уровнях:
  1. **`registry.dispatch()`** — перехватывает любое исключение из обработчика и возвращает `{"error": "Tool execution failed: ExceptionType: message"}` в формате JSON.
  2. **`handle_function_call()`** — оборачивает всю диспетчеризацию во вторичный try/except, который возвращает `{"error": "Error executing tool_name: message"}`.


Это гарантирует, что модель всегда получает корректно сформированную JSON-строку, а не необработанное исключение.
### Инструменты цикла агента[​](<#agent-loop-tools> "Прямая ссылка на Инструменты цикла агента")
Четыре инструмента перехватываются до диспетчеризации через реестр, поскольку им требуется состояние уровня агента (TodoStore, MemoryStore и т.д.):
  * `todo` — планирование/отслеживание задач
  * `memory` — запись в постоянную память
  * `session_search` — поиск по сессиям
  * `delegate_task` — запуск дочерних сессий агента


Схемы этих инструментов по-прежнему регистрируются в реестре (для `get_tool_definitions`), но их обработчики возвращают заглушку с ошибкой, если диспетчеризация каким-то образом достигает их напрямую.
### Асинхронный мост[​](<#async-bridging> "Прямая ссылка на Асинхронный мост")
Когда обработчик инструмента асинхронный, `_run_async()` соединяет его с синхронным путём диспетчеризации:
  * **CLI-путь (нет запущенного цикла)** — использует постоянный цикл событий для поддержания кэшированных асинхронных клиентов
  * **Gateway-путь (есть запущенный цикл)** — запускает одноразовый поток с `asyncio.run()`
  * **Рабочие потоки (параллельные инструменты)** — использует постоянные циклы для каждого потока, хранящиеся в thread-local storage


## Процесс подтверждения DANGEROUS_PATTERNS[​](<#the-dangerous_patterns-approval-flow> "Прямая ссылка на Процесс подтверждения DANGEROUS_PATTERNS")
Терминальный инструмент включает систему подтверждения опасных команд, определённую в `tools/approval.py`:
  1. **Обнаружение шаблонов** — `DANGEROUS_PATTERNS` — это список кортежей `(regex, description)`, охватывающих деструктивные операции:
     * Рекурсивное удаление (`rm -rf`)
     * Форматирование файловой системы (`mkfs`, `dd`)
     * Деструктивные операции SQL (`DROP TABLE`, `DELETE FROM` без `WHERE`)
     * Перезапись системных конфигов (`> /etc/`)
     * Управление сервисами (`systemctl stop`)
     * Удалённое выполнение кода (`curl | sh`)
     * Fork bomb, завершение процессов и т.д.
  2. **Обнаружение** — перед выполнением любой терминальной команды `detect_dangerous_command(command)` проверяет её по всем шаблонам.
  3. **Запрос подтверждения** — при совпадении:
     * **CLI-режим** — интерактивный запрос предлагает пользователю подтвердить, отклонить или разрешить навсегда
     * **Gateway-режим** — асинхронный callback подтверждения отправляет запрос на платформу обмена сообщениями
     * **Умное подтверждение** — опционально, вспомогательная LLM может автоматически подтверждать низкорисковые команды, совпадающие с шаблонами (например, `rm -rf node_modules/` безопасно, но совпадает с «рекурсивное удаление»)
  4. **Состояние сессии** — подтверждения отслеживаются в рамках сессии. После подтверждения «рекурсивное удаление» для сессии последующие команды `rm -rf` не запрашивают повторного подтверждения.
  5. **Постоянный белый список** — опция «разрешить навсегда» записывает шаблон в `config.yaml` в `command_allowlist`, сохраняя его между сессиями.


## Терминальные/исполнительные окружения[​](<#terminalruntime-environments> "Прямая ссылка на Терминальные/исполнительные окружения")
Система терминала поддерживает несколько бэкендов:
  * local
  * docker
  * ssh
  * singularity
  * modal
  * daytona
  * vercel_sandbox


Она также поддерживает:
  * переопределение рабочей директории для каждой задачи
  * управление фоновыми процессами
  * режим PTY
  * callback-запросы подтверждения для опасных команд


## Конкурентность[​](<#concurrency> "Прямая ссылка на Конкурентность")
Вызовы инструментов могут выполняться последовательно или конкурентно в зависимости от комбинации инструментов и требований взаимодействия.
## Связанные документы[​](<#related-docs> "Прямая ссылка на Связанные документы")
  * [Справочник наборов инструментов](</docs/reference/toolsets-reference>)
  * [Справочник встроенных инструментов](</docs/reference/tools-reference>)
  * [Внутреннее устройство цикла агента](</docs/developer-guide/agent-loop>)
  * [Внутреннее устройство ACP](</docs/developer-guide/acp-internals>)


  * [Модель регистрации инструментов](<#tool-registration-model>)
    * [Как работает `registry.register()`](<#how-registryregister-works>)
    * [Обнаружение: `discover_builtin_tools()`](<#discovery-discover_builtin_tools>)
  * [Проверка доступности инструментов (`check_fn`)](<#tool-availability-checking-check_fn>)
  * [Разрешение наборов инструментов](<#toolset-resolution>)
    * [Как `get_tool_definitions()` фильтрует инструменты](<#how-get_tool_definitions-filters-tools>)
    * [Устаревшие имена наборов инструментов](<#legacy-toolset-names>)
  * [Диспетчеризация](<#dispatch>)
    * [Поток диспетчеризации: model tool_call → выполнение обработчика](<#dispatch-flow-model-tool_call--handler-execution>)
    * [Оборачивание ошибок](<#error-wrapping>)
    * [Инструменты цикла агента](<#agent-loop-tools>)
    * [Асинхронный мост](<#async-bridging>)
  * [Процесс подтверждения DANGEROUS_PATTERNS](<#the-dangerous_patterns-approval-flow>)
  * [Терминальные/исполнительные окружения](<#terminalruntime-environments>)
  * [Конкурентность](<#concurrency>)
  * [Связанные документы](<#related-docs>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/tools-runtime -->
