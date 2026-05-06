On this page
У Hermes есть три системы перехватчиков (hooks), которые выполняют пользовательский код в ключевых точках жизненного цикла:

Система| Регистрация| Где выполняется| Назначение  
---|---|---|---  
**[Gateway-хуки](<#gateway-event-hooks>)**| `HOOK.yaml` + `handler.py` в `~/.hermes/hooks/`| Только gateway| Логирование, оповещения, вебхуки  
**[Plugin-хуки](<#plugin-hooks>)**| `ctx.register_hook()` в [плагине](</docs/user-guide/features/plugins>)| CLI + Gateway| Перехват инструментов, метрики, ограничения  
**[Shell-хуки](<#shell-hooks>)**| Блок `hooks:` в `~/.hermes/config.yaml`, указывающий на shell-скрипты| CLI + Gateway| Готовые скрипты для блокировки, автоформатирования, внедрения контекста  

Все три системы неблокирующие — ошибки в любом хуке перехватываются и логируются, не приводя к падению агента.

## Gateway Event Hooks[​](<#gateway-event-hooks> "Прямая ссылка на Gateway Event Hooks")
Gateway-хуки срабатывают автоматически во время работы gateway (Telegram, Discord, Slack, WhatsApp, Teams), не блокируя основной конвейер агента.

### Создание хука[​](<#creating-a-hook> "Прямая ссылка на Создание хука")
Каждый хук представляет собой директорию в `~/.hermes/hooks/`, содержащую два файла:

[code] 
    ~/.hermes/hooks/  
    └── my-hook/  
        ├── HOOK.yaml      # Объявляет, какие события слушать  
        └── handler.py     # Обработчик на Python  
    
[/code]

#### HOOK.yaml[​](<#hookyaml> "Прямая ссылка на HOOK.yaml")
[code] 
    name: my-hook  
    description: Log all agent activity to a file  
    events:  
      - agent:start  
      - agent:end  
      - agent:step  
    
[/code]

Список `events` определяет, какие события запускают ваш обработчик. Вы можете подписаться на любую комбинацию событий, включая шаблоны вида `command:*`.

#### handler.py[​](<#handlerpy> "Прямая ссылка на handler.py")
[code] 
    import json  
    from datetime import datetime  
    from pathlib import Path  
      
    LOG_FILE = Path.home() / ".hermes" / "hooks" / "my-hook" / "activity.log"  
      
    async def handle(event_type: str, context: dict):  
        """Called for each subscribed event. Must be named 'handle'."""  
        entry = {  
            "timestamp": datetime.now().isoformat(),  
            "event": event_type,  
            **context,  
        }  
        with open(LOG_FILE, "a") as f:  
            f.write(json.dumps(entry) + "\n")  
    
[/code]

**Правила для обработчика:**
  * Должен называться `handle`
  * Получает `event_type` (строка) и `context` (словарь)
  * Может быть `async def` или обычным `def` — работают оба варианта
  * Ошибки перехватываются и логируются, никогда не приводят к падению агента

### Доступные события[​](<#available-events> "Прямая ссылка на Доступные события")
Событие| Когда срабатывает| Ключи контекста  
---|---|---|---  
`gateway:startup`| Запуск процесса gateway| `platforms` (список активных платформ)  
`session:start`| Создана новая сессия обмена сообщениями| `platform`, `user_id`, `session_id`, `session_key`  
`session:end`| Сессия завершена (до сброса)| `platform`, `user_id`, `session_key`  
`session:reset`| Пользователь выполнил `/new` или `/reset`| `platform`, `user_id`, `session_key`  
`agent:start`| Агент начинает обработку сообщения| `platform`, `user_id`, `session_id`, `message`  
`agent:step`| Каждая итерация цикла вызова инструментов| `platform`, `user_id`, `session_id`, `iteration`, `tool_names`  
`agent:end`| Агент завершает обработку| `platform`, `user_id`, `session_id`, `message`, `response`  
`command:*`| Выполнена любая слэш-команда| `platform`, `user_id`, `command`, `args`  

#### Подстановочные шаблоны (Wildcard Matching)[​](<#wildcard-matching> "Прямая ссылка на Подстановочные шаблоны")
Обработчики, зарегистрированные на `command:*`, срабатывают для любого события `command:` (`command:model`, `command:reset` и т.д.). Отслеживайте все слэш-команды одной подпиской.

### Примеры[​](<#examples> "Прямая ссылка на Примеры")

#### Оповещение в Telegram о долгих задачах[​](<#telegram-alert-on-long-tasks> "Прямая ссылка на Оповещение в Telegram о долгих задачах")
Отправьте себе сообщение, когда агент выполняет более 10 шагов:

[code] 
    # ~/.hermes/hooks/long-task-alert/HOOK.yaml  
    name: long-task-alert  
    description: Alert when agent is taking many steps  
    events:  
      - agent:step  
    
[/code]

[code] 
    # ~/.hermes/hooks/long-task-alert/handler.py  
    import os  
    import httpx  
      
    THRESHOLD = 10  
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  
    CHAT_ID = os.getenv("TELEGRAM_HOME_CHANNEL")  
      
    async def handle(event_type: str, context: dict):  
        iteration = context.get("iteration", 0)  
        if iteration == THRESHOLD and BOT_TOKEN and CHAT_ID:  
            tools = ", ".join(context.get("tool_names", []))  
            text = f"⚠️ Agent has been running for {iteration} steps. Last tools: {tools}"  
            async with httpx.AsyncClient() as client:  
                await client.post(  
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",  
                    json={"chat_id": CHAT_ID, "text": text},  
                )  
    
[/code]

#### Логирование использования команд[​](<#command-usage-logger> "Прямая ссылка на Логирование использования команд")
Отслеживайте, какие слэш-команды используются:

[code] 
    # ~/.hermes/hooks/command-logger/HOOK.yaml  
    name: command-logger  
    description: Log slash command usage  
    events:  
      - command:*  
    
[/code]

[code] 
    # ~/.hermes/hooks/command-logger/handler.py  
    import json  
    from datetime import datetime  
    from pathlib import Path  
      
    LOG = Path.home() / ".hermes" / "logs" / "command_usage.jsonl"  
      
    def handle(event_type: str, context: dict):  
        LOG.parent.mkdir(parents=True, exist_ok=True)  
        entry = {  
            "ts": datetime.now().isoformat(),  
            "command": context.get("command"),  
            "args": context.get("args"),  
            "platform": context.get("platform"),  
            "user": context.get("user_id"),  
        }  
        with open(LOG, "a") as f:  
            f.write(json.dumps(entry) + "\n")  
    
[/code]

#### Вебхук при старте сессии[​](<#session-start-webhook> "Прямая ссылка на Вебхук при старте сессии")
Отправка POST-запроса во внешний сервис при создании новых сессий:

[code] 
    # ~/.hermes/hooks/session-webhook/HOOK.yaml  
    name: session-webhook  
    description: Notify external service on new sessions  
    events:  
      - session:start  
      - session:reset  
    
[/code]

[code] 
    # ~/.hermes/hooks/session-webhook/handler.py  
    import httpx  
      
    WEBHOOK_URL = "https://your-service.example.com/hermes-events"  
      
    async def handle(event_type: str, context: dict):  
        async with httpx.AsyncClient() as client:  
            await client.post(WEBHOOK_URL, json={  
                "event": event_type,  
                **context,  
            }, timeout=5)  
    
[/code]

### Учебник: BOOT.md — Запуск стартового чек-листа при каждом запуске Gateway[​](<#tutorial-bootmd--run-a-startup-checklist-on-every-gateway-boot> "Прямая ссылка на Учебник: BOOT.md — Запуск стартового чек-листа при каждом запуске Gateway")
Популярный паттерн из сообщества: поместите Markdown-чеклист в `~/.hermes/BOOT.md`, и агент выполнит его один раз при каждом запуске gateway. Полезно для задач вида «при каждом запуске проверь ночные ошибки cron и отправь мне сообщение в Discord, если что-то сломалось» или «собери сводку deploy.log за последние 24 часа и опубликуй в Slack #ops».

Этот учебник покажет, как создать такой механизм самостоятельно с помощью пользовательского хука. В Hermes нет встроенного BOOT.md-хука — вы сами реализуете именно то поведение, которое вам нужно.

#### Что мы создаём[​](<#what-were-building> "Прямая ссылка на Что мы создаём")
  1. Файл `~/.hermes/BOOT.md` с инструкциями по запуску на естественном языке.
  2. Gateway-хук, который срабатывает на `gateway:startup`, создаёт одноразового агента с разрешённой моделью/учётными данными вашего gateway и выполняет инструкции из BOOT.md.
  3. Соглашение `[SILENT]`, позволяющее агенту не отправлять сообщение, если нечего сообщить.

#### Шаг 1: Напишите свой чек-лист[​](<#step-1-write-your-checklist> "Прямая ссылка на Шаг 1: Напишите свой чек-лист")
Создайте `~/.hermes/BOOT.md`. Пишите так, как если бы давали инструкции человеку-ассистенту:

[code] 
    # Startup Checklist  
      
    1. Run `hermes cron list` and check if any scheduled jobs failed overnight.  
    2. If any failed, send a summary to Discord #ops using the `send_message` tool.  
    3. Check if `/opt/app/deploy.log` has any ERROR lines from the last 24 hours. If yes, summarize them and include in the same Discord message.  
    4. If nothing went wrong, reply with only `[SILENT]` so no message is sent.  
    
[/code]

Агент видит это как часть своего промпта, поэтому всё, что можно описать на естественном языке, работает — вызовы инструментов, shell-команды, отправка сообщений, обобщение файлов.

#### Шаг 2: Создайте хук[​](<#step-2-create-the-hook> "Прямая ссылка на Шаг 2: Создайте хук")
[code] 
    ~/.hermes/hooks/boot-md/  
    ├── HOOK.yaml  
    └── handler.py  
    
[/code]

**`~/.hermes/hooks/boot-md/HOOK.yaml`**

[code] 
    name: boot-md  
    description: Run ~/.hermes/BOOT.md on gateway startup  
    events:  
      - gateway:startup  
    
[/code]

**`~/.hermes/hooks/boot-md/handler.py`**

[code] 
    """Run ~/.hermes/BOOT.md on every gateway startup."""  
      
    import logging  
    import threading  
    from pathlib import Path  
      
    logger = logging.getLogger("hooks.boot-md")  
      
    BOOT_FILE = Path.home() / ".hermes" / "BOOT.md"  
      
      
    def _build_prompt(content: str) -> str:  
        return (  
            "You are running a startup boot checklist. Follow the instructions "  
            "below exactly.\n\n"  
            "---\n"  
            f"{content}\n"  
            "---\n\n"  
            "Execute each instruction. Use the send_message tool to deliver any "  
            "messages to platforms like Discord or Slack.\n"  
            "If nothing needs attention and there is nothing to report, reply "  
            "with ONLY: [SILENT]"  
        )  
      
      
    def _run_boot_agent(content: str) -> None:  
        """Spawn a one-shot agent and execute the checklist.  
      
        Uses the gateway's resolved model and runtime credentials so this works  
        against custom endpoints, aggregators, and OAuth-based providers alike.  
        """  
        try:  
            from gateway.run import _resolve_gateway_model, _resolve_runtime_agent_kwargs  
            from run_agent import AIAgent  
      
            agent = AIAgent(  
                model=_resolve_gateway_model(),  
                **_resolve_runtime_agent_kwargs(),  
                platform="gateway",  
                quiet_mode=True,  
                skip_context_files=True,  
                skip_memory=True,  
                max_iterations=20,  
            )  
            result = agent.run_conversation(_build_prompt(content))  
            response = result.get("final_response", "")  
            if response and "[SILENT]" not in response:  
                logger.info("boot-md completed: %s", response[:200])  
            else:  
                logger.info("boot-md completed (nothing to report)")  
        except Exception as e:  
            logger.error("boot-md agent failed: %s", e)  
      
      
    async def handle(event_type: str, context: dict) -> None:  
        if not BOOT_FILE.exists():  
            return  
        content = BOOT_FILE.read_text(encoding="utf-8").strip()  
        if not content:  
            return  
      
        logger.info("Running BOOT.md (%d chars)", len(content))  
      
        # Background thread so gateway startup isn't blocked on a full agent turn.  
        thread = threading.Thread(  
            target=_run_boot_agent,  
            args=(content,),  
            name="boot-md",  
            daemon=True,  
        )  
        thread.start()  
    
[/code]

Две ключевые строки:
  * `_resolve_gateway_model()` — читает текущую настроенную модель gateway.
  * `_resolve_runtime_agent_kwargs()` — разрешает учётные данные провайдера так же, как это делает обычный обмен сообщениями в gateway, включая API-ключи, базовые URL, OAuth-токены и пулы учётных данных.

Без них обычный `AIAgent()` использует встроенные значения по умолчанию и получит ошибку 401 при попытке обращения к любому нестандартному эндпоинту.

#### Шаг 3: Протестируйте[​](<#step-3-test-it> "Прямая ссылка на Шаг 3: Протестируйте")
Перезапустите gateway:

[code] 
    hermes gateway restart  
    
[/code]

Следите за логами:

[code] 
    hermes logs --follow --level INFO | grep boot-md  
    
[/code]

Вы должны увидеть `Running BOOT.md (N chars)`, а затем либо `boot-md completed: ...` (сводка того, что сделал агент), либо `boot-md completed (nothing to report)`, если агент ответил `[SILENT]`.

Удалите `~/.hermes/BOOT.md`, чтобы отключить чек-лист — хук останется загруженным, но будет молча пропускать выполнение, когда файла нет.

#### Расширение паттерна[​](<#extending-the-pattern> "Прямая ссылка на Расширение паттерна")
  * **Чек-листы с учётом расписания:** используйте `datetime.now().weekday()` внутри инструкций BOOT.md («если сегодня понедельник, также проверь лог еженедельного деплоя»). Инструкции — это произвольный текст, поэтому агент может обработать любые разумные указания.
  * **Несколько чек-листов:** укажите хуку другой файл (`STARTUP.md`, `MORNING.md` и т.д.) и зарегистрируйте отдельные директории хуков для каждого.
  * **Вариант без агента:** если вам не нужен полный цикл агента,完全可以 обойтись без `AIAgent` и отправлять фиксированное уведомление напрямую через `httpx`. Дешевле, быстрее и не требует зависимости от провайдера.

#### Почему это не встроенная функция[​](<#why-this-isnt-a-built-in> "Прямая ссылка на Почему это не встроенная функция")
В более ранней версии Hermes это было встроенным хуком, который молча запускал агента с настройками по умолчанию при каждом запуске gateway. Это удивляло пользователей с нестандартными эндпоинтами и делало функцию невидимой для тех, кто не знал о её существовании. Оставляя это как документированный паттерн — который вы создаёте сами, в своей директории хуков — вы точно видите, что он делает, и добровольно включаете его, создавая файлы.

### Как это работает[​](<#how-it-works> "Прямая ссылка на Как это работает")
  1. При запуске gateway `HookRegistry.discover_and_load()` сканирует `~/.hermes/hooks/`
  2. Каждая поддиректория с `HOOK.yaml` + `handler.py` загружается динамически
  3. Обработчики регистрируются для указанных событий
  4. В каждой точке жизненного цикла `hooks.emit()` запускает все подходящие обработчики
  5. Ошибки в любом обработчике перехватываются и логируются — сломанный хук никогда не приводит к падению агента

info
Gateway-хуки срабатывают только в **gateway** (Telegram, Discord, Slack, WhatsApp, Teams). CLI не загружает gateway-хуки. Для хуков, работающих везде, используйте [plugin-хуки](<#plugin-hooks>).

## Plugin Hooks[​](<#plugin-hooks> "Прямая ссылка на Plugin Hooks")
[Плагины](</docs/user-guide/features/plugins>) могут регистрировать хуки, которые срабатывают как в **CLI**, так и в **gateway**-сессиях. Они регистрируются программно через `ctx.register_hook()` в функции `register()` вашего плагина.

[code] 
    def register(ctx):  
        ctx.register_hook("pre_tool_call", my_tool_observer)  
        ctx.register_hook("post_tool_call", my_tool_logger)  
        ctx.register_hook("pre_llm_call", my_memory_callback)  
        ctx.register_hook("post_llm_call", my_sync_callback)  
        ctx.register_hook("on_session_start", my_init_callback)  
        ctx.register_hook("on_session_end", my_cleanup_callback)  
    
[/code]

**Общие правила для всех хуков:**
  * Колбэки получают **именованные аргументы**. Всегда используйте `**kwargs` для обратной совместимости — в будущих версиях могут быть добавлены новые параметры, и ваш плагин продолжит работать.
  * Если колбэк **вызывает ошибку**, она логируется и пропускается. Остальные хуки и агент продолжают работу. Некорректный плагин никогда не может сломать агента.
  * Возвращаемые значения двух хуков влияют на поведение: [`pre_tool_call`](<#pre_tool_call>) может **блокировать** инструмент, а [`pre_llm_call`](<#pre_llm_call>) может **внедрять контекст** в LLM-вызов. Все остальные хуки работают по принципу «запустил и забыл».

### Краткий справочник[​](<#quick-reference> "Прямая ссылка на Краткий справочник")
Хук| Срабатывает| Возвращает  
---|---|---|---  
[`pre_tool_call`](<#pre_tool_call>)| Перед выполнением любого инструмента| `{"action": "block", "message": str}` для блокировки вызова  
[`post_tool_call`](<#post_tool_call>)| После возврата любого инструмента| игнорируется  
[`pre_llm_call`](<#pre_llm_call>)| Один раз за оборот, перед циклом вызова инструментов| `{"context": str}` для добавления контекста к сообщению пользователя  
[`post_llm_call`](<#post_llm_call>)| Один раз за оборот, после цикла вызова инструментов| игнорируется  
[`on_session_start`](<#on_session_start>)| Создана новая сессия (только первый оборот)| игнорируется  
[`on_session_end`](<#on_session_end>)| Сессия завершена| игнорируется  
[`on_session_finalize`](<#on_session_finalize>)| CLI/gateway закрывает активную сессию (сброс, сохранение, статистика)| игнорируется  
[`on_session_reset`](<#on_session_reset>)| Gateway заменяет ключ сессии (например, `/new`, `/reset`)| игнорируется  
[`subagent_stop`](<#subagent_stop>)| Дочерний процесс `delegate_task` завершился| игнорируется  
[`pre_gateway_dispatch`](<#pre_gateway_dispatch>)| Gateway получил сообщение пользователя, перед аутентификацией и диспетчеризацией| `{"action": "skip" | "rewrite" | "allow", ...}` для управления потоком  
[`pre_approval_request`](<#pre_approval_request>)| Опасная команда требует подтверждения пользователя, перед отправкой запроса/уведомления| игнорируется  
[`post_approval_response`](<#post_approval_response>)| Пользователь ответил на запрос подтверждения (или истекло время ожидания)| игнорируется  
[`transform_tool_result`](<#transform_tool_result>)| После возврата любого инструмента, перед передачей результата модели| `str` для замены результата, `None` чтобы оставить без изменений  
[`transform_terminal_output`](<#transform_terminal_output>)| Внутри инструмента `terminal`, перед усечением/удалением ANSI/редактированием| `str` для замены сырого вывода, `None` чтобы оставить без изменений  

* * *

### `pre_tool_call`[​](<#pre_tool_call> "Прямая ссылка на pre_tool_call")
Срабатывает **непосредственно перед** каждым выполнением инструмента — как встроенных, так и инструментов плагинов.

**Сигнатура колбэка:**

[code] 
    def my_callback(tool_name: str, args: dict, task_id: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`tool_name`| `str`| Имя инструмента, который будет выполнен (например, `"terminal"`, `"web_search"`, `"read_file"`)  
`args`| `dict`| Аргументы, переданные моделью инструменту  
`task_id`| `str`| Идентификатор сессии/задачи. Пустая строка, если не задан.  

**Срабатывает:** В `model_tools.py`, внутри `handle_function_call()`, перед запуском обработчика инструмента. Срабатывает один раз на каждый вызов инструмента — если модель вызывает 3 инструмента параллельно, сработает 3 раза.

**Возвращаемое значение — блокировка вызова:**

[code] 
    return {"action": "block", "message": "Reason the tool call was blocked"}  
    
[/code]

Агент прерывает выполнение инструмента, возвращая модели `message` как сообщение об ошибке. Побеждает первая директива блокировки (сначала регистрируются Python-плагины, затем shell-хуки). Любое другое возвращаемое значение игнорируется, поэтому существующие колбэки-наблюдатели продолжают работать без изменений.

**Варианты использования:** Логирование, аудит, счётчики вызовов инструментов, блокировка опасных операций, ограничение частоты, применение политик для отдельных пользователей.

**Пример — аудит вызовов инструментов:**

[code] 
    import json, logging  
    from datetime import datetime  
      
    logger = logging.getLogger(__name__)  
      
    def audit_tool_call(tool_name, args, task_id, **kwargs):  
        logger.info("TOOL_CALL session=%s tool=%s args=%s",  
                    task_id, tool_name, json.dumps(args)[:200])  
      
    def register(ctx):  
        ctx.register_hook("pre_tool_call", audit_tool_call)  
    
[/code]

**Пример — предупреждение об опасных инструментах:**

[code] 
    DANGEROUS = {"terminal", "write_file", "patch"}  
      
    def warn_dangerous(tool_name, **kwargs):  
        if tool_name in DANGEROUS:  
            print(f"⚠ Executing potentially dangerous tool: {tool_name}")  
      
    def register(ctx):  
        ctx.register_hook("pre_tool_call", warn_dangerous)  
    
[/code]

* * *

### `post_tool_call`[​](<#post_tool_call> "Прямая ссылка на post_tool_call")
Срабатывает **непосредственно после** выполнения каждого инструмента.

**Сигнатура колбэка:**

[code] 
    def my_callback(tool_name: str, args: dict, result: str, task_id: str,  
                    duration_ms: int, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`tool_name`| `str`| Имя выполненного инструмента  
`args`| `dict`| Аргументы, переданные моделью инструменту  
`result`| `str`| Возвращаемое значение инструмента (всегда строка JSON)  
`task_id`| `str`| Идентификатор сессии/задачи. Пустая строка, если не задан.  
`duration_ms`| `int`| Время выполнения инструмента в миллисекундах (измеряется с помощью `time.monotonic()` вокруг `registry.dispatch()`).  

**Срабатывает:** В `model_tools.py`, внутри `handle_function_call()`, после возврата обработчика инструмента. Срабатывает один раз на каждый вызов инструмента. **Не** срабатывает, если инструмент вызвал необработанное исключение (ошибка перехватывается и возвращается как строка JSON с ошибкой, и `post_tool_call` срабатывает с этой строкой ошибки в качестве `result`).

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Логирование результатов инструментов, сбор метрик, отслеживание успешности/отказов, панели задержек, бюджеты на инструменты, отправка уведомлений при завершении определённых инструментов.

**Пример — отслеживание метрик использования инструментов:**

[code] 
    from collections import Counter, defaultdict  
    import json  
      
    _tool_counts = Counter()  
    _error_counts = Counter()  
    _latency_ms = defaultdict(list)  
      
    def track_metrics(tool_name, result, duration_ms=0, **kwargs):  
        _tool_counts[tool_name] += 1  
        _latency_ms[tool_name].append(duration_ms)  
        try:  
            parsed = json.loads(result)  
            if "error" in parsed:  
                _error_counts[tool_name] += 1  
        except (json.JSONDecodeError, TypeError):  
            pass  
      
    def register(ctx):  
        ctx.register_hook("post_tool_call", track_metrics)  
    
[/code]

* * *

### `pre_llm_call`[​](<#pre_llm_call> "Прямая ссылка на pre_llm_call")
Срабатывает **один раз за оборот**, перед началом цикла вызова инструментов. Это **единственный хук, возвращаемое значение которого используется** — он может внедрять контекст в сообщение пользователя текущего оборота.

**Сигнатура колбэка:**

[code] 
    def my_callback(session_id: str, user_message: str, conversation_history: list,  
                    is_first_turn: bool, model: str, platform: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`session_id`| `str`| Уникальный идентификатор текущей сессии  
`user_message`| `str`| Исходное сообщение пользователя для этого оборота (до внедрения контекста навыков)  
`conversation_history`| `list`| Копия полного списка сообщений (формат OpenAI: `[{"role": "user", "content": "..."}]`)  
`is_first_turn`| `bool`| `True`, если это первый оборот новой сессии, `False` для последующих оборотов  
`model`| `str`| Идентификатор модели (например, `"anthropic/claude-sonnet-4.6"`)  
`platform`| `str`| Где выполняется сессия: `"cli"`, `"telegram"`, `"discord"` и т.д.  

**Срабатывает:** В `run_agent.py`, внутри `run_conversation()`, после сжатия контекста, но до основного цикла `while`. Срабатывает один раз за вызов `run_conversation()` (т.е. один раз за оборот пользователя), а не один раз за API-вызов внутри цикла инструментов.

**Возвращаемое значение:** Если колбэк возвращает словарь с ключом `"context"` или просто непустую строку, текст добавляется к сообщению пользователя текущего оборота. Верните `None`, чтобы ничего не внедрять.

[code] 
    # Внедрение контекста  
    return {"context": "Recalled memories:\n- User likes Python\n- Working on hermes-agent"}  
      
    # Простая строка (эквивалентно)  
    return "Recalled memories:\n- User likes Python"  
      
    # Без внедрения  
    return None  
    
[/code]

**Куда внедряется контекст:** Всегда в **сообщение пользователя**, никогда в системный промпт. Это сохраняет кэш промптов — системный промпт остаётся неизменным между оборотами, поэтому кэшированные токены используются повторно. Системный промпт — это зона ответственности Hermes (управление моделью, контроль инструментов, личность, навыки). Плагины добавляют контекст вместе с вводом пользователя.

Весь внедрённый контекст **эфемерен** — добавляется только во время API-вызова. Исходное сообщение пользователя в истории беседы никогда не изменяется, и ничего не сохраняется в базу данных сессии.

Когда **несколько плагинов** возвращают контекст, их выводы объединяются двойными переносами строк в порядке обнаружения плагинов (по алфавиту имени директории).

**Варианты использования:** Восстановление контекста из памяти, внедрение RAG-контекста, ограничения, аналитика по оборотам.

**Пример — восстановление из памяти:**

[code] 
    import httpx  
      
    MEMORY_API = "https://your-memory-api.example.com"  
      
    def recall(session_id, user_message, is_first_turn, **kwargs):  
        try:  
            resp = httpx.post(f"{MEMORY_API}/recall", json={  
                "session_id": session_id,  
                "query": user_message,  
            }, timeout=3)  
            memories = resp.json().get("results", [])  
            if not memories:  
                return None  
            text = "Recalled context:\n" + "\n".join(f"- {m['text']}" for m in memories)  
            return {"context": text}  
        except Exception:  
            return None  
      
    def register(ctx):  
        ctx.register_hook("pre_llm_call", recall)  
    
[/code]

**Пример — ограничения (guardrails):**

[code] 
    POLICY = "Never execute commands that delete files without explicit user confirmation."  
      
    def guardrails(**kwargs):  
        return {"context": POLICY}  
      
    def register(ctx):  
        ctx.register_hook("pre_llm_call", guardrails)  
    
[/code]

* * *

### `post_llm_call`[​](<#post_llm_call> "Прямая ссылка на post_llm_call")
Срабатывает **один раз за оборот**, после завершения цикла вызова инструментов и формирования агентом финального ответа. Срабатывает только для **успешных** оборотов — не срабатывает, если оборот был прерван.

**Сигнатура колбэка:**

[code] 
    def my_callback(session_id: str, user_message: str, assistant_response: str,  
                    conversation_history: list, model: str, platform: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`session_id`| `str`| Уникальный идентификатор текущей сессии  
`user_message`| `str`| Исходное сообщение пользователя для этого оборота  
`assistant_response`| `str`| Финальный текстовый ответ агента для этого оборота  
`conversation_history`| `list`| Копия полного списка сообщений после завершения оборота  
`model`| `str`| Идентификатор модели  
`platform`| `str`| Где выполняется сессия  

**Срабатывает:** В `run_agent.py`, внутри `run_conversation()`, после выхода из цикла инструментов с финальным ответом. Защищён условием `if final_response and not interrupted` — поэтому **не** срабатывает, когда пользователь прерывает оборот или агент достигает лимита итераций без формирования ответа.

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Синхронизация данных беседы с внешней системой памяти, вычисление метрик качества ответов, логирование сводок по оборотам, запуск последующих действий.

**Пример — синхронизация с внешней памятью:**

[code] 
    import httpx  
      
    MEMORY_API = "https://your-memory-api.example.com"  
      
    def sync_memory(session_id, user_message, assistant_response, **kwargs):  
        try:  
            httpx.post(f"{MEMORY_API}/store", json={  
                "session_id": session_id,  
                "user": user_message,  
                "assistant": assistant_response,  
            }, timeout=5)  
        except Exception:  
            pass  # best-effort  
      
    def register(ctx):  
        ctx.register_hook("post_llm_call", sync_memory)  
    
[/code]

**Пример — отслеживание длины ответов:**

[code] 
    import logging  
    logger = logging.getLogger(__name__)  
      
    def log_response_length(session_id, assistant_response, model, **kwargs):  
        logger.info("RESPONSE session=%s model=%s chars=%d",  
                    session_id, model, len(assistant_response or ""))  
      
    def register(ctx):  
        ctx.register_hook("post_llm_call", log_response_length)  
    
[/code]

* * *

### `on_session_start`[​](<#on_session_start> "Прямая ссылка на on_session_start")
Срабатывает **один раз** при создании новой сессии. **Не** срабатывает при продолжении сессии (когда пользователь отправляет второе сообщение в существующей сессии).

**Сигнатура колбэка:**

[code] 
    def my_callback(session_id: str, model: str, platform: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`session_id`| `str`| Уникальный идентификатор новой сессии  
`model`| `str`| Идентификатор модели  
`platform`| `str`| Где выполняется сессия  

**Срабатывает:** В `run_agent.py`, внутри `run_conversation()`, во время первого оборота новой сессии — а именно после построения системного промпта, но до запуска цикла инструментов. Проверка: `if not conversation_history` (нет предыдущих сообщений = новая сессия).

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Инициализация состояния сессии, прогрев кэшей, регистрация сессии во внешнем сервисе, логирование начала сессий.

**Пример — инициализация кэша сессии:**

[code] 
    _session_caches = {}  
      
    def init_session(session_id, model, platform, **kwargs):  
        _session_caches[session_id] = {  
            "model": model,  
            "platform": platform,  
            "tool_calls": 0,  
            "started": __import__("datetime").datetime.now().isoformat(),  
        }  
      
    def register(ctx):  
        ctx.register_hook("on_session_start", init_session)  
    
[/code]

* * *

### `on_session_end`[​](<#on_session_end> "Прямая ссылка на on_session_end")
Срабатывает в **самом конце** каждого вызова `run_conversation()`, независимо от результата. Также срабатывает из обработчика выхода CLI, если агент был в середине оборота, когда пользователь завершил работу.

**Сигнатура колбэка:**

[code] 
    def my_callback(session_id: str, completed: bool, interrupted: bool,  
                    model: str, platform: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`session_id`| `str`| Уникальный идентификатор сессии  
`completed`| `bool`| `True`, если агент сформировал финальный ответ, `False` в противном случае  
`interrupted`| `bool`| `True`, если оборот был прерван (пользователь отправил новое сообщение, `/stop` или вышел)  
`model`| `str`| Идентификатор модели  
`platform`| `str`| Где выполняется сессия  

**Срабатывает:** В двух местах:
  1. **`run_agent.py`** — в конце каждого вызова `run_conversation()`, после всей очистки. Всегда срабатывает, даже если оборот завершился ошибкой.
  2. **`cli.py`** — в обработчике atexit CLI, но **только** если агент был в середине оборота (`_agent_running=True`) в момент завершения. Это перехватывает Ctrl+C и `/exit` во время обработки. В этом случае `completed=False` и `interrupted=True`.

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Сброс буферов, закрытие соединений, сохранение состояния сессии, логирование длительности сессии, очистка ресурсов, инициализированных в `on_session_start`.

**Пример — сброс и очистка:**

[code] 
    _session_caches = {}  
      
    def cleanup_session(session_id, completed, interrupted, **kwargs):  
        cache = _session_caches.pop(session_id, None)  
        if cache:  
            # Сброс накопленных данных на диск или во внешний сервис  
            status = "completed" if completed else ("interrupted" if interrupted else "failed")  
            print(f"Session {session_id} ended: {status}, {cache['tool_calls']} tool calls")  
      
    def register(ctx):  
        ctx.register_hook("on_session_end", cleanup_session)  
    
[/code]

**Пример — отслеживание длительности сессии:**

[code] 
    import time, logging  
    logger = logging.getLogger(__name__)  
      
    _start_times = {}  
      
    def on_start(session_id, **kwargs):  
        _start_times[session_id] = time.time()  
      
    def on_end(session_id, completed, interrupted, **kwargs):  
        start = _start_times.pop(session_id, None)  
        if start:  
            duration = time.time() - start  
            logger.info("SESSION_DURATION session=%s seconds=%.1f completed=%s interrupted=%s",  
                         session_id, duration, completed, interrupted)  
      
    def register(ctx):  
        ctx.register_hook("on_session_start", on_start)  
        ctx.register_hook("on_session_end", on_end)  
    
[/code]

* * *

### `on_session_finalize`[​](<#on_session_finalize> "Прямая ссылка на on_session_finalize")
Срабатывает, когда CLI или gateway **закрывают** активную сессию — например, когда пользователь выполняет `/new`, gateway удаляет неактивную сессию сборщиком мусора или CLI завершает работу с активным агентом. Это последний шанс сохранить состояние, связанное с уходящей сессией, прежде чем её идентификатор исчезнет.

**Сигнатура колбэка:**

[code] 
    def my_callback(session_id: str | None, platform: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`session_id`| `str` или `None`| Идентификатор уходящей сессии. Может быть `None`, если активной сессии не существовало.  
`platform`| `str`| `"cli"` или название платформы обмена сообщениями (`"telegram"`, `"discord"` и т.д.).  

**Срабатывает:** В `cli.py` (при `/new` / завершении CLI) и `gateway/run.py` (при сбросе сессии или сборке мусора). Всегда сопровождается `on_session_reset` на стороне gateway.

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Сохранение финальных метрик сессии перед удалением идентификатора сессии, закрытие ресурсов сессии, отправка финального телеметрического события, сброс данных из очереди на запись.

* * *

### `on_session_reset`[​](<#on_session_reset> "Прямая ссылка на on_session_reset")
Срабатывает, когда gateway **заменяет ключ сессии** для активного чата — пользователь вызвал `/new`, `/reset`, `/clear` или адаптер выбрал новую сессию после периода бездействия. Это позволяет плагинам реагировать на то, что состояние беседы было очищено, не дожидаясь следующего `on_session_start`.

**Сигнатура колбэка:**

[code] 
    def my_callback(session_id: str, platform: str, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`session_id`| `str`| Идентификатор новой сессии (уже заменён на свежее значение).  
`platform`| `str`| Название платформы обмена сообщениями.  

**Срабатывает:** В `gateway/run.py`, сразу после выделения нового ключа сессии, но до обработки следующего входящего сообщения. На gateway порядок такой: `on_session_finalize(old_id)` → замена → `on_session_reset(new_id)` → `on_session_start(new_id)` при первом входящем обороте.

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Сброс кэшей сессии, привязанных к `session_id`, отправка аналитики «сессия сменена», подготовка нового контейнера состояния.

* * *

Смотрите **[Руководство по созданию плагина](</docs/guides/build-a-hermes-plugin>)** для полного пошагового руководства, включая схемы инструментов, обработчики и продвинутые паттерны хуков.

* * *

### `subagent_stop`[​](<#subagent_stop> "Прямая ссылка на subagent_stop")
Срабатывает **один раз для каждого дочернего агента** после завершения `delegate_task`. Независимо от того, делегировали вы одну задачу или три, этот хук срабатывает один раз для каждого дочернего агента, последовательно в родительском потоке.

**Сигнатура колбэка:**

[code] 
    def my_callback(parent_session_id: str, child_role: str | None,  
                    child_summary: str | None, child_status: str,  
                    duration_ms: int, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`parent_session_id`| `str`| Идентификатор сессии родительского агента, делегировавшего задачу  
`child_role`| `str | None`| Роль-тег оркестратора, установленная для дочернего агента (`None`, если функция не включена)  
`child_summary`| `str | None`| Финальный ответ, который дочерний агент вернул родителю  
`child_status`| `str`| `"completed"`, `"failed"`, `"interrupted"` или `"error"`  
`duration_ms`| `int`| Время выполнения дочернего агента в миллисекундах  

**Срабатывает:** В `tools/delegate_tool.py`, после того как `ThreadPoolExecutor.as_completed()` завершит все дочерние фьючерсы. Вызов маршалируется в родительский поток, чтобы авторам хуков не приходилось думать о конкурентном выполнении колбэков.

**Возвращаемое значение:** Игнорируется.

**Варианты использования:** Логирование активности оркестрации, накопление длительности дочерних процессов для биллинга, запись пост-делегационных аудиторских записей.

**Пример — логирование активности оркестратора:**

[code] 
    import logging  
    logger = logging.getLogger(__name__)  
      
    def log_subagent(parent_session_id, child_role, child_status, duration_ms, **kwargs):  
        logger.info(  
            "SUBAGENT parent=%s role=%s status=%s duration_ms=%d",  
            parent_session_id, child_role, child_status, duration_ms,  
        )  
      
    def register(ctx):  
        ctx.register_hook("subagent_stop", log_subagent)  
    
[/code]

info
При интенсивном делегировании (например, роли оркестратора × 5 листьев × вложенная глубина) `subagent_stop` может срабатывать много раз за оборот. Старайтесь, чтобы ваш колбэк был быстрым; ресурсоёмкие операции выносите в фоновую очередь.

* * *

### `pre_gateway_dispatch`[​](<#pre_gateway_dispatch> "Прямая ссылка на pre_gateway_dispatch")
Срабатывает **один раз для каждого входящего`MessageEvent`** в gateway, после проверки на внутреннее событие, но **до** аутентификации/спаривания и диспетчеризации агента. Это точка перехвата для политик управления потоком сообщений на уровне gateway (режимы «только чтение», передача человеку, маршрутизация по чатам и т.д.), которые не вписываются ни в один отдельный адаптер платформы.

**Сигнатура колбэка:**

[code] 
    def my_callback(event, gateway, session_store, **kwargs):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`event`| `MessageEvent`| Нормализованное входящее сообщение (содержит `.text`, `.source`, `.message_id`, `.internal` и т.д.).  
`gateway`| `GatewayRunner`| Активный раннер gateway, чтобы плагины могли вызывать `gateway.adapters[platform].send(...)` для побочных ответов (уведомления владельцу и т.д.).  
`session_store`| `SessionStore`| Для тихого добавления в транскрипт через `session_store.append_to_transcript(...)`.  

**Срабатывает:** В `gateway/run.py`, внутри `GatewayRunner._handle_message()`, сразу после вычисления `is_internal`. **Внутренние события полностью пропускают хук** (они генерируются системой — завершения фоновых процессов и т.п. — и не должны контролироваться пользовательскими политиками).

**Возвращаемое значение:** `None` или словарь. Побеждает первый распознанный словарь с действием; остальные результаты плагинов игнорируются. Исключения в колбэках плагинов перехватываются и логируются; при ошибке gateway всегда переходит к обычной диспетчеризации.

Возврат| Эффект  
---|---  
`{"action": "skip", "reason": "..."}`| Отбросить сообщение — никакого ответа агента, никакого процесса спаривания, никакой аутентификации. Предполагается, что плагин уже обработал сообщение (например, тихо добавил в транскрипт).  
`{"action": "rewrite", "text": "new text"}`| Заменить `event.text`, затем продолжить обычную диспетчеризацию с изменённым событием. Полезно для объединения буферизованных фоновых сообщений в один промпт.  
`{"action": "allow"}` / `None`| Обычная диспетчеризация — выполняется полная цепочка аутентификации/спаривания/цикла агента.  

**Варианты использования:** Групповые чаты только для чтения (отвечать только при упоминании; буферизировать фоновые сообщения в контекст); передача человеку (тихо добавлять сообщения клиента в транскрипт, пока владелец ведёт чат вручную); ограничение частоты по профилям; маршрутизация на основе политик.

**Пример — тихое отклонение неавторизованных личных сообщений без запуска кода спаривания:**

[code] 
    def deny_unauthorized_dms(event, **kwargs):  
        src = event.source  
        if src.chat_type == "dm" and not _is_approved_user(src.user_id):  
            return {"action": "skip", "reason": "unauthorized-dm"}  
        return None  
      
    def register(ctx):  
        ctx.register_hook("pre_gateway_dispatch", deny_unauthorized_dms)  
    
[/code]

**Пример — объединение буфера фоновых сообщений в один промпт при упоминании:**

[code] 
    _buffers = {}  
      
    def buffer_or_rewrite(event, **kwargs):  
        key = (event.source.platform, event.source.chat_id)  
        buf = _buffers.setdefault(key, [])  
        if _bot_mentioned(event.text):  
            combined = "\n".join(buf + [event.text])  
            buf.clear()  
            return {"action": "rewrite", "text": combined}  
        buf.append(event.text)  
        return {"action": "skip", "reason": "ambient-buffered"}  
      
    def register(ctx):  
        ctx.register_hook("pre_gateway_dispatch", buffer_or_rewrite)  
    
[/code]

* * *

### `pre_approval_request`[​](<#pre_approval_request> "Прямая ссылка на pre_approval_request")
Срабатывает **непосредственно перед** показом запроса на подтверждение пользователю — охватывает все поверхности: интерактивный CLI, Ink TUI, платформы gateway (Telegram, Discord, Slack, WhatsApp, Matrix и т.д.) и ACP-клиенты (VS Code, Zed, JetBrains).

Это правильное место для подключения пользовательского уведомителя — например, приложения в строке меню macOS, которое показывает уведомление с кнопками «Разрешить»/«Отклонить», или аудиторского лога, записывающего каждый запрос на подтверждение с контекстом.

**Сигнатура колбэка:**

[code] 
    def my_callback(  
        command: str,  
        description: str,  
        pattern_key: str,  
        pattern_keys: list[str],  
        session_key: str,  
        surface: str,  
        **kwargs,  
    ):  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`command`| `str`| Shell-команда, ожидающая подтверждения  
`description`| `str`| Понятные человеку причины, по которым команда отмечена (объединяются, если совпало несколько шаблонов)  
`pattern_key`| `str`| Основной ключ шаблона, вызвавшего запрос подтверждения (например, `"rm_rf"`, `"sudo"`)  
`pattern_keys`| `list[str]`| Все ключи шаблонов, которые совпали  
`session_key`| `str`| Идентификатор сессии, полезен для ограничения уведомлений по чатам  
`surface`| `str`| `"cli"` для интерактивных CLI/TUI-промптов, `"gateway"` для асинхронных подтверждений на платформах  

**Возвращаемое значение:** игнорируется. Хуки здесь являются только наблюдателями; они не могут заблокировать или предварительно ответить на запрос подтверждения. Используйте [`pre_tool_call`](<#pre_tool_call>) для блокировки инструмента до того, как он достигнет системы подтверждений.

**Варианты использования:** Уведомления на рабочем столе, push-оповещения, аудит, вебхуки в Slack, маршрутизация эскалаций, метрики.

**Пример — уведомление на рабочем столе в macOS:**

[code] 
    import subprocess  
      
    def notify_approval(command, description, session_key, **kwargs):  
        title = "Hermes needs approval"  
        body = f"{description}: {command[:80]}"  
        subprocess.Popen([  
            "osascript", "-e",  
            f'display notification "{body}" with title "{title}"',  
        ])  
      
    def register(ctx):  
        ctx.register_hook("pre_approval_request", notify_approval)  
    
[/code]

* * *

### `post_approval_response`[​](<#post_approval_response> "Прямая ссылка на post_approval_response")
Срабатывает **после** того, как пользователь ответил на запрос подтверждения (или истекло время ожидания).

**Сигнатура колбэка:**

[code] 
    def my_callback(  
        command: str,  
        description: str,  
        pattern_key: str,  
        pattern_keys: list[str],  
        session_key: str,  
        surface: str,  
        choice: str,  
        **kwargs,  
    ):  
    
[/code]

Те же аргументы, что и у `pre_approval_request`, плюс:

Параметр| Тип| Описание  
---|---|---|---  
`choice`| `str`| Одно из: `"once"`, `"session"`, `"always"`, `"deny"` или `"timeout"`  

**Возвращаемое значение:** игнорируется.

**Варианты использования:** Закрыть соответствующее уведомление на рабочем столе, записать финальное решение в аудиторский лог, обновить метрики, применить ограничитель частоты.

[code] 
    def log_decision(command, choice, session_key, **kwargs):  
        logger.info("approval %s: %s for session %s", choice, command[:60], session_key)  
      
    def register(ctx):  
        ctx.register_hook("post_approval_response", log_decision)  
    
[/code]

* * *

### `transform_tool_result`[​](<#transform_tool_result> "Прямая ссылка на transform_tool_result")
Срабатывает **после** возврата инструмента и **до** добавления результата в беседу. Позволяет плагину переписать строку результата ЛЮБОГО инструмента — не только вывода терминала — прежде чем модель его увидит.

**Сигнатура колбэка:**

[code] 
    def my_callback(  
        tool_name: str,  
        arguments: dict,  
        result: str,  
        task_id: str | None,  
        **kwargs,  
    ) -> str | None:  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`tool_name`| `str`| Инструмент, который сгенерировал результат (`read_file`, `web_extract`, `delegate_task`, …).  
`arguments`| `dict`| Аргументы, с которыми модель вызвала инструмент.  
`result`| `str`| Сырой результат инструмента после усечения и удаления ANSI-кодов.  
`task_id`| `str | None`| Идентификатор задачи/сессии при работе в средах RL/бенчмарков.  

**Возвращаемое значение:** `str` для замены результата (возвращённая строка — то, что увидит модель), `None` чтобы оставить без изменений.

**Варианты использования:** Редактирование PII, специфичной для организации, из вывода `web_extract`, обёртка длинных JSON-ответов инструментов в сводный заголовок, внедрение подсказок из RAG в результаты `read_file`, переписывание отчётов дочерних агентов `delegate_task` в схему, специфичную для проекта.

[code] 
    import re  
    SECRET = re.compile(r"sk-[A-Za-z0-9]{32,}")  
      
    def redact_secrets(tool_name, result, **kwargs):  
        if SECRET.search(result):  
            return SECRET.sub("[REDACTED]", result)  
        return None  
      
    def register(ctx):  
        ctx.register_hook("transform_tool_result", redact_secrets)  
    
[/code]

Применяется ко всем инструментам. Для перезаписи только вывода терминала см. `transform_terminal_output` ниже — он уже и запускается раньше в конвейере (до усечения, до редактирования).

* * *

### `transform_terminal_output`[​](<#transform_terminal_output> "Прямая ссылка на transform_terminal_output")
Срабатывает внутри конвейера вывода инструмента `terminal`, **до** стандартного усечения на 50 КБ, удаления ANSI-кодов и редактирования секретов. Позволяет плагинам переписывать сырой stdout/stderr shell-команды до того, как его обработают последующие этапы.

**Сигнатура колбэка:**

[code] 
    def my_callback(  
        command: str,  
        output: str,  
        exit_code: int,  
        cwd: str,  
        task_id: str | None,  
        **kwargs,  
    ) -> str | None:  
    
[/code]

Параметр| Тип| Описание  
---|---|---|---  
`command`| `str`| Shell-команда, сгенерировавшая вывод.  
`output`| `str`| Сырой объединённый stdout/stderr (может быть очень большим — усечение происходит после хука).  
`exit_code`| `int`| Код завершения процесса.  
`cwd`| `str`| Рабочая директория, в которой выполнялась команда.  

**Возвращаемое значение:** `str` для замены вывода, `None` чтобы оставить без изменений.

**Варианты использования:** Добавление сводок для команд, генерирующих огромный вывод (`du -ah`, `find`, `tree`), пометка вывода маркером, специфичным для проекта, чтобы последующие хуки знали, как его обрабатывать, удаление временных шумов, которые меняются между запусками и мешают кэшированию промптов.

[code] 
    def summarize_find(command, output, **kwargs):  
        if command.startswith("find ") and len(output) > 50_000:  
            lines = output.count("\n")  
            head = "\n".join(output.splitlines()[:40])  
            return f"{head}\n\n[summary: {lines} paths total, showing first 40]"  
        return None  
      
    def register(ctx):  
        ctx.register_hook("transform_terminal_output", summarize_find)  
    
[/code]

Хорошо сочетается с `transform_tool_result` (который охватывает все остальные инструменты).

* * *

## Shell Hooks[​](<#shell-hooks> "Прямая ссылка на Shell Hooks")
Объявите shell-скриптовые хуки в вашем `cli-config.yaml`, и Hermes будет запускать их как подпроцессы при каждом срабатывании соответствующего события plugin-хука — как в CLI, так и в gateway-сессиях. Для этого не требуется писать плагин на Python.

Используйте shell-хуки, когда вам нужен готовый однофайловый скрипт (Bash, Python или любой другой с shebang) для:

  * **Блокировки вызова инструмента** — отклонение опасных команд `terminal`, применение политик для конкретных директорий, запрос подтверждения для деструктивных операций `write_file` / `patch`.
  * **Запуска после вызова инструмента** — автоформатирование Python или TypeScript файлов, которые только что написал агент, логирование API-вызовов, запуск CI-пайплайна.
  * **Внедрения контекста в следующий LLM-оборот** — добавление вывода `git status`, текущего дня недели или извлечённых документов к сообщению пользователя (см. [`pre_llm_call`](<#pre_llm_call>)).
  * **Наблюдения за событиями жизненного цикла** — запись лога при завершении дочернего агента (`subagent_stop`) или начале сессии (`on_session_start`).

Shell-хуки регистрируются вызовом `agent.shell_hooks.register_from_config(cfg)` как при запуске CLI (`hermes_cli/main.py`), так и gateway (`gateway/run.py`). Они естественным образом сочетаются с Python-плагинами — оба типа проходят через один и тот же диспетчер.

### Сравнение[​](<#comparison-at-a-glance> "Прямая ссылка на Сравнение")
Характеристика| Shell-хуки| [Plugin-хуки](<#plugin-hooks>)| [Gateway-хуки](<#gateway-event-hooks>)  
---|---|---|---|---  
Объявляются в| Блоке `hooks:` в `~/.hermes/config.yaml`| `register()` в плагине `plugin.yaml`| Директории `HOOK.yaml` + `handler.py`  
Расположение| `~/.hermes/agent-hooks/` (по соглашению)| `~/.hermes/plugins/<name>/`| `~/.hermes/hooks/<name>/`  
Язык| Любой (Bash, Python, Go бинарник, …)| Только Python| Только Python  
Где выполняется| CLI + Gateway| CLI + Gateway| Только Gateway  
События| `VALID_HOOKS` (включая `subagent_stop`)| `VALID_HOOKS`| Жизненный цикл gateway (`gateway:startup`, `agent:*`, `command:*`)  
Может блокировать вызов инструмента| Да (`pre_tool_call`)| Да (`pre_tool_call`)| Нет  
Может внедрять LLM-контекст| Да (`pre_llm_call`)| Да (`pre_llm_call`)| Нет  
Согласие| Запрос при первом использовании для каждой пары `(event, command)`| Неявное (доверие Python-плагину)| Неявное (доверие директории)  
Межпроцессная изоляция| Да (подпроцесс)| Нет (внутри процесса)| Нет (внутри процесса)  

### Схема конфигурации[​](<#configuration-schema> "Прямая ссылка на Схема конфигурации")
[code] 
    hooks:  
      <event_name>:                  # Должно быть в VALID_HOOKS  
        - matcher: "<regex>"         # Опционально; используется только для pre/post_tool_call  
          command: "<shell command>" # Обязательно; выполняется через shlex.split, shell=False  
          timeout: <seconds>         # Опционально; по умолчанию 60, максимум 300  
      
    hooks_auto_accept: false         # См. «Модель согласия» ниже  
    
[/code]

Имена событий должны быть одними из [событий plugin-хуков](<#plugin-hooks>); опечатки вызывают предупреждение «Возможно, вы имели в виду X?» и пропускаются. Неизвестные ключи внутри одной записи игнорируются; отсутствие `command` — пропуск с предупреждением. `timeout > 300` принудительно ограничивается с предупреждением.

### JSON wire protocol[​](<#json-wire-protocol> "Прямая ссылка на JSON wire protocol")
Каждый раз при срабатывании события Hermes создаёт подпроцесс для каждого подходящего хука (при наличии matcher'а), передаёт JSON-полезную нагрузку в **stdin** и читает **stdout** обратно в формате JSON.

**stdin — полезная нагрузка, получаемая скриптом:**

[code] 
    {  
      "hook_event_name": "pre_tool_call",  
      "tool_name":       "terminal",  
      "tool_input":      {"command": "rm -rf /"},  
      "session_id":      "sess_abc123",  
      "cwd":             "/home/user/project",  
      "extra":           {"task_id": "...", "tool_call_id": "..."}  
    }  
    
[/code]

`tool_name` и `tool_input` равны `null` для событий, не связанных с инструментами (`pre_llm_call`, `subagent_stop`, жизненный цикл сессии). Словарь `extra` содержит все специфичные для события именованные аргументы (`user_message`, `conversation_history`, `child_role`, `duration_ms`, …). Несериализуемые значения преобразуются в строки, а не опускаются.

**stdout — опциональный ответ:**

[code] 
    // Блокировка pre_tool_call (оба формата принимаются; внутри нормализуются):  
    {"decision": "block", "reason":  "Forbidden: rm -rf"}   // Стиль Claude-Code  
    {"action":   "block", "message": "Forbidden: rm -rf"}   // Канонический Hermes  
      
    // Внедрение контекста для pre_llm_call:  
    {"context": "Today is Friday, 2026-04-17"}  
      
    // Тихий no-op — подходит любой пустой / несовпадающий вывод:  
    
[/code]

Некорректный JSON, ненулевые коды завершения и таймауты логируют предупреждение, но никогда не прерывают цикл агента.

### Примеры[​](<#worked-examples> "Прямая ссылка на Примеры")

#### 1. Автоформатирование Python-файлов после каждой записи[​](<#1-auto-format-python-files-after-every-write> "Прямая ссылка на 1. Автоформатирование Python-файлов после каждой записи")
[code] 
    # ~/.hermes/config.yaml  
    hooks:  
      post_tool_call:  
        - matcher: "write_file|patch"  
          command: "~/.hermes/agent-hooks/auto-format.sh"  
    
[/code]

[code] 
    #!/usr/bin/env bash  
    # ~/.hermes/agent-hooks/auto-format.sh  
    payload="$(cat -)"  
    path=$(echo "$payload" | jq -r '.tool_input.path // empty')  
    [[ "$path" == *.py ]] && command -v black >/dev/null && black "$path" 2>/dev/null  
    printf '{}\n'  
    
[/code]

Представление файла в контексте агента **не** перечитывается автоматически — переформатирование влияет только на файл на диске. Последующие вызовы `read_file` подхватят отформатированную версию.

#### 2. Блокировка деструктивных команд `terminal`[​](<#2-block-destructive-terminal-commands> "Прямая ссылка на 2. Блокировка деструктивных команд terminal")
[code] 
    hooks:  
      pre_tool_call:  
        - matcher: "terminal"  
          command: "~/.hermes/agent-hooks/block-rm-rf.sh"  
          timeout: 5  
    
[/code]

[code] 
    #!/usr/bin/env bash  
    # ~/.hermes/agent-hooks/block-rm-rf.sh  
    payload="$(cat -)"  
    cmd=$(echo "$payload" | jq -r '.tool_input.command // empty')  
    if echo "$cmd" | grep -qE 'rm[[:space:]]+-rf?[[:space:]]+/'; then  
      printf '{"decision": "block", "reason": "blocked: rm -rf / is not permitted"}\n'  
    else  
      printf '{}\n'  
    fi  
    
[/code]

#### 3. Внедрение `git status` в каждый оборот (аналог Claude-Code `UserPromptSubmit`)[​](<#3-inject-git-status-into-every-turn-claude-code-userpromptsubmit-equivalent> "Прямая ссылка на 3. Внедрение git status в каждый оборот (аналог Claude-Code UserPromptSubmit)")
[code] 
    hooks:  
      pre_llm_call:  
        - command: "~/.hermes/agent-hooks/inject-cwd-context.sh"  
    
[/code]

[code] 
    #!/usr/bin/env bash  
    # ~/.hermes/agent-hooks/inject-cwd-context.sh  
    cat - >/dev/null   # discard stdin payload  
    if status=$(git status --porcelain 2>/dev/null) && [[ -n "$status" ]]; then  
      jq --null-input --arg s "$status" \  
         '{context: ("Uncommitted changes in cwd:\n" + $s)}'  
    else  
      printf '{}\n'  
    fi  
    
[/code]

Событие `UserPromptSubmit` от Claude Code намеренно не является отдельным событием Hermes — `pre_llm_call` срабатывает в том же месте и уже поддерживает внедрение контекста. Используйте его здесь.

#### 4. Логирование завершения каждого дочернего агента[​](<#4-log-every-subagent-completion> "Прямая ссылка на 4. Логирование завершения каждого дочернего агента")
[code] 
    hooks:  
      subagent_stop:  
        - command: "~/.hermes/agent-hooks/log-orchestration.sh"  
    
[/code]

[code] 
    #!/usr/bin/env bash  
    # ~/.hermes/agent-hooks/log-orchestration.sh  
    log=~/.hermes/logs/orchestration.log  
    jq -c '{ts: now, parent: .session_id, extra: .extra}' < /dev/stdin >> "$log"  
    printf '{}\n'  
    
[/code]

### Модель согласия[​](<#consent-model> "Прямая ссылка на Модель согласия")
Каждая уникальная пара `(event, command)` запрашивает у пользователя подтверждение при первом обнаружении Hermes, после чего решение сохраняется в `~/.hermes/shell-hooks-allowlist.json`. Последующие запуски (CLI или gateway) пропускают запрос.

Три способа обойти интерактивный запрос — достаточно любого:

  1. Флаг `--accept-hooks` в CLI (например, `hermes --accept-hooks chat`)
  2. Переменная окружения `HERMES_ACCEPT_HOOKS=1`
  3. `hooks_auto_accept: true` в `cli-config.yaml`

Для запусков не в TTY (gateway, cron, CI) требуется один из этих трёх способов — иначе любой недавно добавленный хук молча остаётся незарегистрированным и логирует предупреждение.

**Редактирование скриптов доверяется неявно.** Белый список ключей привязан к точной строке команды, а не к хешу скрипта, поэтому редактирование скрипта на диске не аннулирует согласие. `hermes hooks doctor` проверяет расхождение mtime, чтобы вы могли заметить изменения и решить, нужно ли повторное одобрение.

### CLI `hermes hooks`[​](<#the-hermes-hooks-cli> "Прямая ссылка на CLI hermes hooks")
Команда| Что делает  
---|---  
`hermes hooks list`| Выводит настроенные хуки с matcher'ом, таймаутом и статусом согласия  
`hermes hooks test <event> [--for-tool X] [--payload-file F]`| Запускает все подходящие хуки с синтетической полезной нагрузкой и выводит разобранный ответ  
`hermes hooks revoke <command>`| Удаляет все записи из белого списка, соответствующие `<command>` (вступает в силу после перезапуска)  
`hermes hooks doctor`| Для каждого настроенного хука: проверяет бит исполняемости, статус в белом списке, расхождение mtime, валидность JSON-вывода и примерное время выполнения  

### Безопасность[​](<#security> "Прямая ссылка на Безопасность")
Shell-хуки выполняются с **вашими полными учётными данными** — та же граница доверия, что и у записи cron или алиаса в shell. Относитесь к блоку `hooks:` в `config.yaml` как к привилегированной конфигурации:

  * Используйте только те скрипты, которые вы написали или полностью проверили.
  * Храните скрипты внутри `~/.hermes/agent-hooks/`, чтобы путь было легко проверять.
  * Запускайте `hermes hooks doctor` после получения обновлённой конфигурации, чтобы заметить новые хуки до их регистрации.
  * Если ваш `config.yaml` хранится в системе контроля версий и используется командой, проверяйте PR, изменяющие секцию `hooks:`, так же, как вы проверяете CI-конфигурацию.

### Порядок и приоритет[​](<#ordering-and-precedence> "Прямая ссылка на Порядок и приоритет")
И Python-плагины, и shell-хуки проходят через один и тот же диспетчер `invoke_hook()`. Python-плагины регистрируются первыми (`discover_and_load()`), shell-хуки вторыми (`register_from_config()`), поэтому решения о блокировке `pre_tool_call` от Python-плагинов имеют приоритет в спорных случаях. Побеждает первая валидная блокировка — агрегатор возвращает результат, как только любой колбэк возвращает `{"action": "block", "message": str}` с непустым сообщением.

  * [Gateway Event Hooks](<#gateway-event-hooks>)
    * [Создание хука](<#creating-a-hook>)
    * [Доступные события](<#available-events>)
    * [Примеры](<#examples>)
    * [Учебник: BOOT.md — Запуск стартового чек-листа при каждом запуске Gateway](<#tutorial-bootmd--run-a-startup-checklist-on-every-gateway-boot>)
    * [Как это работает](<#how-it-works>)
  * [Plugin Hooks](<#plugin-hooks>)
    * [Краткий справочник](<#quick-reference>)
    * [`pre_tool_call`](<#pre_tool_call>)
    * [`post_tool_call`](<#post_tool_call>)
    * [`pre_llm_call`](<#pre_llm_call>)
    * [`post_llm_call`](<#post_llm_call>)
    * [`on_session_start`](<#on_session_start>)
    * [`on_session_end`](<#on_session_end>)
    * [`on_session_finalize`](<#on_session_finalize>)
    * [`on_session_reset`](<#on_session_reset>)
    * [`subagent_stop`](<#subagent_stop>)
    * [`pre_gateway_dispatch`](<#pre_gateway_dispatch>)
    * [`pre_approval_request`](<#pre_approval_request>)
    * [`post_approval_response`](<#post_approval_response>)
    * [`transform_tool_result`](<#transform_tool_result>)
    * [`transform_terminal_output`](<#transform_terminal_output>)
  * [Shell Hooks](<#shell-hooks>)
    * [Сравнение](<#comparison-at-a-glance>)
    * [Схема конфигурации](<#configuration-schema>)
    * [JSON wire protocol](<#json-wire-protocol>)
    * [Примеры](<#worked-examples>)
    * [Модель согласия](<#consent-model>)
    * [CLI `hermes hooks`](<#the-hermes-hooks-cli>)
    * [Безопасность](<#security>)
    * [Порядок и приоритет](<#ordering-and-precedence>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks -->
