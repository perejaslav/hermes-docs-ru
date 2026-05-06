На этой странице

Hermes имеет систему плагинов для добавления пользовательских инструментов, хуков и интеграций без изменения основного кода.

Если вы хотите создать собственный инструмент для себя, своей команды или одного проекта — это обычно правильный путь. Страница руководства разработчика [Добавление инструментов](</docs/developer-guide/adding-tools>) предназначена для встроенных инструментов ядра Hermes, которые находятся в `tools/` и `toolsets.py`.

**→[Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>)** — пошаговое руководство с полным рабочим примером.

## Краткий обзор[​](<#quick-overview> "Прямая ссылка на Краткий обзор")

Поместите директорию в `~/.hermes/plugins/` с `plugin.yaml` и кодом Python:

[code]
    ~/.hermes/plugins/my-plugin/
    ├── plugin.yaml      # манифест
    ├── __init__.py      # register() — связывает схемы с обработчиками
    ├── schemas.py       # схемы инструментов (то, что видит LLM)
    └── tools.py         # обработчики инструментов (что выполняется при вызове)
    
[/code]

Запустите Hermes — ваши инструменты появятся рядом со встроенными. Модель может вызывать их немедленно.

### Минимальный рабочий пример[​](<#minimal-working-example> "Прямая ссылка на Минимальный рабочий пример")

Вот полный плагин, который добавляет инструмент `hello_world` и логирует каждый вызов инструмента через хук.

**`~/.hermes/plugins/hello-world/plugin.yaml`**

[code]
    name: hello-world
    version: "1.0"
    description: Пример минимального плагина
    
[/code]

**`~/.hermes/plugins/hello-world/__init__.py`**

[code]
    """Минимальный плагин Hermes — регистрирует инструмент и хук."""
      
    import json
      
      
    def register(ctx):
        # --- Инструмент: hello_world ---
        schema = {
            "name": "hello_world",
            "description": "Возвращает дружеское приветствие для указанного имени.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Имя для приветствия",
                    }
                },
                "required": ["name"],
            },
        }
      
        def handle_hello(params, **kwargs):
            del kwargs
            name = params.get("name", "World")
            return json.dumps({"success": True, "greeting": f"Hello, {name}!"})
      
        ctx.register_tool(
            name="hello_world",
            toolset="hello_world",
            schema=schema,
            handler=handle_hello,
            description="Возвращает дружеское приветствие для указанного имени.",
        )
      
        # --- Хук: логирование каждого вызова инструмента ---
        def on_tool_call(tool_name, params, result):
            print(f"[hello-world] вызван инструмент: {tool_name}")
      
        ctx.register_hook("post_tool_call", on_tool_call)
    
[/code]

Поместите оба файла в `~/.hermes/plugins/hello-world/`, перезапустите Hermes, и модель сможет немедленно вызывать `hello_world`. Хук выводит строку лога после каждого вызова инструмента.

Проектные плагины в `./.hermes/plugins/` по умолчанию отключены. Включайте их только для доверенных репозиториев, установив `HERMES_ENABLE_PROJECT_PLUGINS=true` перед запуском Hermes.

## Что могут делать плагины[​](<#what-plugins-can-do> "Прямая ссылка на Что могут делать плагины")

Каждый API `ctx.*` ниже доступен внутри функции `register(ctx)` плагина.

| Возможность | Как |
|---|---|
| Добавлять инструменты | `ctx.register_tool(name=..., toolset=..., schema=..., handler=...)` |
| Добавлять хуки | `ctx.register_hook("post_tool_call", callback)` |
| Добавлять слеш-команды | `ctx.register_command(name, handler, description)` — добавляет `/name` в CLI и шлюзовых сессиях |
| Отправлять инструменты из команд | `ctx.dispatch_tool(name, args)` — вызывает зарегистрированный инструмент с автоматическим подключением контекста родительского агента |
| Добавлять CLI-команды | `ctx.register_cli_command(name, help, setup_fn, handler_fn)` — добавляет `hermes <plugin> <subcommand>` |
| Внедрять сообщения | `ctx.inject_message(content, role="user")` — см. [Внедрение сообщений](<#injecting-messages>) |
| Поставлять файлы данных | `Path(__file__).parent / "data" / "file.yaml"` |
| Встраивать навыки | `ctx.register_skill(name, path)` — пространство имён `plugin:skill`, загружается через `skill_view("plugin:skill")` |
| Ограничивать по переменным окружения | `requires_env: [API_KEY]` в plugin.yaml — запрашивается во время `hermes plugins install` |
| Распространять через pip | `[project.entry-points."hermes_agent.plugins"]` |
| Регистрировать шлюзовую платформу (Discord, Telegram, IRC, …) | `ctx.register_platform(name, label, adapter_factory, check_fn, ...)` — см. [Добавление адаптеров платформ](</docs/developer-guide/adding-platform-adapters>) |
| Регистрировать бэкенд генерации изображений | `ctx.register_image_gen_provider(provider)` — см. [Плагины провайдеров генерации изображений](</docs/developer-guide/image-gen-provider-plugin>) |
| Регистрировать движок сжатия контекста | `ctx.register_context_engine(engine)` — см. [Плагины движков контекста](</docs/developer-guide/context-engine-plugin>) |
| Регистрировать бэкенд памяти | Создайте подкласс `MemoryProvider` в `plugins/memory/<name>/__init__.py` — см. [Плагины провайдеров памяти](</docs/developer-guide/memory-provider-plugin>) (использует отдельную систему обнаружения) |
| Регистрировать бэкенд вывода (LLM-провайдер) | `register_provider(ProviderProfile(...))` в `plugins/model-providers/<name>/__init__.py` — см. [Плагины провайдеров моделей](</docs/developer-guide/model-provider-plugin>) (использует отдельную систему обнаружения) |

## Обнаружение плагинов[​](<#plugin-discovery> "Прямая ссылка на Обнаружение плагинов")

| Источник | Путь | Сценарий использования |
|---|---|---|
| Встроенные | `<repo>/plugins/` | Поставляются с Hermes — см. [Встроенные плагины](</docs/user-guide/features/built-in-plugins>) |
| Пользовательские | `~/.hermes/plugins/` | Личные плагины |
| Проектные | `.hermes/plugins/` | Плагины для конкретного проекта (требуется `HERMES_ENABLE_PROJECT_PLUGINS=true`) |
| pip | `hermes_agent.plugins` entry_points | Распространяемые пакеты |
| Nix | `services.hermes-agent.extraPlugins` / `extraPythonPackages` | Декларативные установки NixOS — см. [Настройка Nix](</docs/getting-started/nix-setup#plugins>) |

Поздние источники переопределяют ранние при совпадении имён, поэтому пользовательский плагин с тем же именем, что и встроенный, заменяет его.

### Подкатегории плагинов[​](<#plugin-sub-categories> "Прямая ссылка на Подкатегории плагинов")

В каждом источнике Hermes также распознаёт подкатегории директорий, которые направляют плагины в специализированные системы обнаружения:

| Поддиректория | Что содержит | Система обнаружения |
|---|---|---|
| `plugins/` (корень) | Общие плагины — инструменты, хуки, слеш-команды, CLI-команды, встроенные навыки | `PluginManager` (kind: `standalone` или `backend`) |
| `plugins/platforms/<name>/` | Адаптеры шлюзовых каналов (`ctx.register_platform()`) | `PluginManager` (kind: `platform`, на один уровень глубже) |
| `plugins/image_gen/<name>/` | Бэкенды генерации изображений (`ctx.register_image_gen_provider()`) | `PluginManager` (kind: `backend`, на один уровень глубже) |
| `plugins/memory/<name>/` | Провайдеры памяти (подкласс `MemoryProvider`) | **Собственный загрузчик** в `plugins/memory/__init__.py` (kind: `exclusive` — один активный за раз) |
| `plugins/context_engine/<name>/` | Движки сжатия контекста (`ctx.register_context_engine()`) | **Собственный загрузчик** в `plugins/context_engine/__init__.py` (один активный за раз) |
| `plugins/model-providers/<name>/` | Профили LLM-провайдеров (`register_provider(ProviderProfile(...))`) | **Собственный загрузчик** в `providers/__init__.py` (ленивое сканирование при первом вызове `get_provider_profile()`) |

Пользовательские плагины в `~/.hermes/plugins/model-providers/<name>/` и `~/.hermes/plugins/memory/<name>/` переопределяют встроенные плагины с тем же именем — побеждает последний зарегистрированный в `register_provider()` / `register_memory_provider()`. Просто поместите директорию, и она заменит встроенную без изменений в репозитории.

## Плагины требуют явного согласия (за некоторыми исключениями)[​](<#plugins-are-opt-in-with-a-few-exceptions> "Прямая ссылка на Плагины требуют явного согласия (за некоторыми исключениями)")

**Общие плагины и установленные пользователем бэкенды по умолчанию отключены** — обнаружение находит их (поэтому они отображаются в `hermes plugins` и `/plugins`), но ничто с хуками или инструментами не загружается, пока вы не добавите имя плагина в `plugins.enabled` в `~/.hermes/config.yaml`. Это предотвращает выполнение стороннего кода без вашего явного согласия.

[code]
    plugins:
      enabled:
        - my-tool-plugin
        - disk-cleanup
      disabled:       # опциональный чёрный список — всегда побеждает, если имя есть в обоих
        - noisy-plugin
    
[/code]

Три способа изменить состояние:

[code]
    hermes plugins                    # интерактивное переключение (пробел — отметить/снять)
    hermes plugins enable <name>      # добавить в белый список
    hermes plugins disable <name>     # удалить из белого списка + добавить в отключённые
    
[/code]

После `hermes plugins install owner/repo` будет задан вопрос `Включить 'name' сейчас? [y/N]` — по умолчанию нет. Пропустите запрос для скриптовых установок с `--enable` или `--no-enable`.

### Что НЕ контролируется белым списком[​](<#what-the-allow-list-does-not-gate> "Прямая ссылка на Что НЕ контролируется белым списком")

Несколько категорий плагинов обходят `plugins.enabled` — они являются частью встроенной функциональности Hermes, и их отключение сломало бы базовую работу:

| Вид плагина | Как активируется вместо этого |
|---|---|
| **Встроенные шлюзовые плагины** (IRC, Teams и т.д. в `plugins/platforms/`) | Автозагрузка, чтобы все поставляемые каналы были доступны. Сам канал включается через `gateway.platforms.<name>.enabled` в `config.yaml`. |
| **Встроенные бэкенды** (провайдеры генерации изображений в `plugins/image_gen/` и т.д.) | Автозагрузка, чтобы бэкенд по умолчанию «просто работал». Выбор осуществляется через `<category>.provider` в `config.yaml` (например, `image_gen.provider: openai`). |
| **Провайдеры памяти** (`plugins/memory/`) | Все обнаружены; ровно один активен, выбирается через `memory.provider` в `config.yaml`. |
| **Движки контекста** (`plugins/context_engine/`) | Все обнаружены; один активен, выбирается через `context.engine` в `config.yaml`. |
| **Провайдеры моделей** (`plugins/model-providers/`) | Все 33 провайдера обнаруживаются и регистрируются при первом вызове `get_provider_profile()`. Пользователь выбирает один за раз через `--provider` или `config.yaml`. |
| **Pip-установленные `backend` плагины** | Требуют явного согласия через `plugins.enabled` (как и обычные плагины). |
| **Установленные пользователем платформы** (в `~/.hermes/plugins/platforms/`) | Требуют явного согласия через `plugins.enabled` — сторонние шлюзовые адаптеры требуют явного разрешения. |

Коротко: **встроенная инфраструктура «всегда работает» загружается автоматически; сторонние общие плагины требуют явного включения.** Белый список `plugins.enabled` — это шлюз, специально предназначенный для произвольного кода, который пользователь помещает в `~/.hermes/plugins/`.

### Миграция для существующих пользователей[​](<#migration-for-existing-users> "Прямая ссылка на Миграция для существующих пользователей")

При обновлении до версии Hermes с плагинами, требующими явного включения (схема конфига v21+), любые уже установленные пользовательские плагины в `~/.hermes/plugins/`, которые не были в `plugins.disabled`, **автоматически наследуются** в `plugins.enabled`. Ваша существующая настройка продолжит работать. Встроенные отдельные плагины НЕ наследуются — даже существующие пользователи должны явно их включать. (Встроенные шлюзовые/бэкенд-плагины никогда не нуждались в наследовании, поскольку они никогда не были отключены по умолчанию.)

## Доступные хуки[​](<#available-hooks> "Прямая ссылка на Доступные хуки")

Плагины могут регистрировать обратные вызовы для следующих событий жизненного цикла. Подробности, сигнатуры обратных вызовов и примеры см. на странице **[Хуки событий](</docs/user-guide/features/hooks#plugin-hooks>)**.

| Хук | Срабатывает когда |
|---|---|
| [`pre_tool_call`](</docs/user-guide/features/hooks#pre_tool_call>) | Перед выполнением любого инструмента |
| [`post_tool_call`](</docs/user-guide/features/hooks#post_tool_call>) | После возврата любого инструмента |
| [`pre_llm_call`](</docs/user-guide/features/hooks#pre_llm_call>) | Один раз за шаг, перед циклом LLM — может вернуть `{"context": "..."}` для [внедрения контекста в сообщение пользователя](</docs/user-guide/features/hooks#pre_llm_call>) |
| [`post_llm_call`](</docs/user-guide/features/hooks#post_llm_call>) | Один раз за шаг, после цикла LLM (только успешные шаги) |
| [`on_session_start`](</docs/user-guide/features/hooks#on_session_start>) | Создана новая сессия (только первый шаг) |
| [`on_session_end`](</docs/user-guide/features/hooks#on_session_end>) | Окончание каждого вызова `run_conversation` + обработчик выхода из CLI |
| [`on_session_finalize`](</docs/user-guide/features/hooks#on_session_finalize>) | CLI/шлюз завершает активную сессию (`/new`, GC, выход из CLI) |
| [`on_session_reset`](</docs/user-guide/features/hooks#on_session_reset>) | Шлюз заменяет ключ сессии (`/new`, `/reset`, `/clear`, ротация при бездействии) |
| [`subagent_stop`](</docs/user-guide/features/hooks#subagent_stop>) | Один раз для каждого дочернего агента после завершения `delegate_task` |
| [`pre_gateway_dispatch`](</docs/user-guide/features/hooks#pre_gateway_dispatch>) | Шлюз получил сообщение пользователя, перед аутентификацией и отправкой. Верните `{"action": "skip" | "rewrite" | "allow", ...}` чтобы повлиять на поток. |

## Типы плагинов[​](<#plugin-types> "Прямая ссылка на Типы плагинов")

У Hermes есть четыре вида плагинов:

| Тип | Что делает | Выбор | Расположение |
|---|---|---|---|
| **Общие плагины** | Добавляют инструменты, хуки, слеш-команды, CLI-команды | Множественный выбор (вкл/выкл) | `~/.hermes/plugins/` |
| **Провайдеры памяти** | Заменяют или дополняют встроенную память | Одиночный выбор (один активный) | `plugins/memory/` |
| **Движки контекста** | Заменяют встроенный компрессор контекста | Одиночный выбор (один активный) | `plugins/context_engine/` |
| **Провайдеры моделей** | Объявляют бэкенд вывода (OpenRouter, Anthropic, …) | Множественная регистрация, выбор через `--provider` / `config.yaml` | `plugins/model-providers/` |

Провайдеры памяти и движки контекста являются **провайдерскими плагинами** — только один каждого типа может быть активен одновременно. Провайдеры моделей также являются плагинами, но многие загружаются одновременно; пользователь выбирает один за раз через `--provider` или `config.yaml`. Общие плагины можно включать в любой комбинации.

## Расширяемые интерфейсы — куда обращаться для каждого[​](<#pluggable-interfaces--where-to-go-for-each> "Прямая ссылка на Расширяемые интерфейсы — куда обращаться для каждого")

Таблица выше показывает четыре категории плагинов, но внутри «Общих плагинов» `PluginContext` предоставляет несколько различных точек расширения — и Hermes также принимает расширения вне системы Python-плагинов (бэкенды, управляемые конфигом, команды с привязкой к оболочке, внешние серверы и т.д.). Используйте эту таблицу, чтобы найти подходящую документацию для того, что вы хотите создать:

| Хотите добавить… | Как | Руководство |
|---|---|---|
| **Инструмент**, который может вызывать LLM | Python-плагин — `ctx.register_tool()` | [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>) · [Добавление инструментов](</docs/developer-guide/adding-tools>) |
| **Хук жизненного цикла** (до/после LLM, начало/конец сессии, фильтр инструментов) | Python-плагин — `ctx.register_hook()` | [Справочник по хукам](</docs/user-guide/features/hooks>) · [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>) |
| **Слеш-команду** для CLI/шлюза | Python-плагин — `ctx.register_command()` | [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>) · [Расширение CLI](</docs/developer-guide/extending-the-cli>) |
| **Подкоманду** для `hermes <thing>` | Python-плагин — `ctx.register_cli_command()` | [Расширение CLI](</docs/developer-guide/extending-the-cli>) |
| Встроенный **навык**, который поставляет ваш плагин | Python-плагин — `ctx.register_skill()` | [Создание навыков](</docs/developer-guide/creating-skills>) |
| **Бэкенд вывода** (LLM-провайдер: совместимый с OpenAI, Codex, Anthropic-Messages, Bedrock) | Провайдерский плагин — `register_provider(ProviderProfile(...))` в `plugins/model-providers/<name>/` | **[Плагины провайдеров моделей](</docs/developer-guide/model-provider-plugin>)** · [Добавление провайдеров](</docs/developer-guide/adding-providers>) |
| **Шлюзовый канал** (Discord / Telegram / IRC / Teams / и т.д.) | Платформенный плагин — `ctx.register_platform()` в `plugins/platforms/<name>/` | [Добавление адаптеров платформ](</docs/developer-guide/adding-platform-adapters>) |
| **Бэкенд памяти** (Honcho, Mem0, Supermemory, …) | Плагин памяти — подкласс `MemoryProvider` в `plugins/memory/<name>/` | [Плагины провайдеров памяти](</docs/developer-guide/memory-provider-plugin>) |
| **Стратегию сжатия контекста** | Плагин движка контекста — `ctx.register_context_engine()` | [Плагины движков контекста](</docs/developer-guide/context-engine-plugin>) |
| **Бэкенд генерации изображений** (DALL·E, SDXL, …) | Бэкенд-плагин — `ctx.register_image_gen_provider()` | [Плагины провайдеров генерации изображений](</docs/developer-guide/image-gen-provider-plugin>) |
| **Бэкенд TTS** (любой CLI — Piper, VoxCPM, Kokoro, xtts, скрипты клонирования голоса, …) | Управляется конфигом — объявите в `tts.providers.<name>` с `type: command` в `config.yaml` | [Настройка TTS](</docs/user-guide/features/tts#custom-command-providers>) |
| **Бэкенд STT** (пользовательский бинарник whisper, локальный ASR CLI) | Управляется конфигом — установите переменную окружения `HERMES_LOCAL_STT_COMMAND` как шаблон оболочки | [Транскрипция голосовых сообщений (STT)](</docs/user-guide/features/tts#voice-message-transcription-stt>) |
| **Внешние инструменты через MCP** (файловая система, GitHub, Linear, Notion, любой MCP-сервер) | Управляется конфигом — объявите `mcp_servers.<name>` с `command:` / `url:` в `config.yaml`. Hermes автоматически обнаруживает инструменты сервера и регистрирует их рядом со встроенными. | [MCP](</docs/user-guide/features/mcp>) |
| **Дополнительные источники навыков** (пользовательские GitHub-репозитории, частные индексы навыков) | CLI — `hermes skills tap add <repo>` | [Центр навыков](</docs/user-guide/features/skills#skills-hub>) · [Публикация пользовательского источника](</docs/user-guide/features/skills#publishing-a-custom-skill-tap>) |
| **Хуки шлюзовых событий** (срабатывают на `gateway:startup`, `session:start`, `agent:end`, `command:*`) | Поместите `HOOK.yaml` + `handler.py` в `~/.hermes/hooks/<name>/` | [Хуки событий](</docs/user-guide/features/hooks#gateway-event-hooks>) |
| **Хуки оболочки** (выполняют команду оболочки при событиях — уведомления, журналы аудита, оповещения на рабочем столе) | Управляется конфигом — объявите в `hooks:` в `config.yaml` | [Хуки оболочки](</docs/user-guide/features/hooks#shell-hooks>) |

> **Примечание**
> Не всё является Python-плагином. Некоторые поверхности расширения намеренно используют **команды оболочки, управляемые конфигом** (TTS, STT, хуки оболочки), чтобы любой уже имеющийся CLI стал плагином без написания Python-кода. Другие — это **внешние серверы** (MCP), к которым агент подключается и автоматически регистрирует их инструменты. А некоторые — это **директории для размещения** (шлюзовые хуки) со своим форматом манифеста. Выберите подходящую поверхность под стиль интеграции, который соответствует вашему сценарию; руководства в таблице выше охватывают заполнители, обнаружение и примеры.

## Декларативные плагины NixOS[​](<#nixos-declarative-plugins> "Прямая ссылка на Декларативные плагины NixOS")

На NixOS плагины могут быть установлены декларативно через опции модуля — без `hermes plugins install`. Подробности см. в **[руководстве по настройке Nix](</docs/getting-started/nix-setup#plugins>)**.

[code]
    services.hermes-agent = {
      # Директория плагина (исходное дерево с plugin.yaml)
      extraPlugins = [ (pkgs.fetchFromGitHub { ... }) ];
      # Entry-point плагин (pip пакет)
      extraPythonPackages = [ (pkgs.python312Packages.buildPythonPackage { ... }) ];
      # Включить в конфиге
      settings.plugins.enabled = [ "my-plugin" ];
    };
    
[/code]

Декларативные плагины символически link-уются с префиксом `nix-managed-` — они сосуществуют с вручную установленными плагинами и автоматически очищаются при удалении из конфига Nix.

## Управление плагинами[​](<#managing-plugins> "Прямая ссылка на Управление плагинами")

[code]
    hermes plugins                               # единый интерактивный интерфейс
    hermes plugins list                          # таблица: включено / отключено / не включено
    hermes plugins install user/repo             # установить из Git, затем запрос Включить? [y/N]
    hermes plugins install user/repo --enable    # установить И включить (без запроса)
    hermes plugins install user/repo --no-enable # установить, но оставить отключённым (без запроса)
    hermes plugins update my-plugin              # загрузить последнюю версию
    hermes plugins remove my-plugin              # удалить
    hermes plugins enable my-plugin              # добавить в белый список
    hermes plugins disable my-plugin             # удалить из белого списка + добавить в отключённые
    
[/code]

### Интерактивный интерфейс[​](<#interactive-ui> "Прямая ссылка на Интерактивный интерфейс")

Запуск `hermes plugins` без аргументов открывает составной интерактивный экран:

[code]
    Plugins
      ↑↓ навигация  SPACE переключить  ENTER настроить/подтвердить  ESC готово
      
      Общие плагины
     → [✓] my-tool-plugin — Пользовательский поисковый инструмент
       [ ] webhook-notifier — Хуки событий
       [ ] disk-cleanup — Автоматическая очистка временных файлов [встроенный]
      
      Провайдерские плагины
         Провайдер памяти          ▸ honcho
         Движок контекста           ▸ compressor
    
[/code]

* **Раздел общих плагинов** — флажки, переключение пробелом. Отмечено = в `plugins.enabled`, не отмечено = в `plugins.disabled` (явное отключение).
* **Раздел провайдерских плагинов** — показывает текущий выбор. Нажмите ENTER, чтобы войти в радиокнопку, где вы выбираете одного активного провайдера.
* Встроенные плагины отображаются в том же списке с тегом `[встроенный]`.

Выбор провайдерских плагинов сохраняется в `config.yaml`:

[code]
    memory:
      provider: "honcho"      # пустая строка = только встроенный
      
    context:
      engine: "compressor"    # встроенный компрессор по умолчанию
    
[/code]

### Включено vs. отключено vs. ни то, ни другое[​](<#enabled-vs-disabled-vs-neither> "Прямая ссылка на Включено vs. отключено vs. ни то, ни другое")

Плагины находятся в одном из трёх состояний:

| Состояние | Значение | В `plugins.enabled`? | В `plugins.disabled`? |
|---|---|---|---|
| `enabled` | Загружен при следующей сессии | Да | Нет |
| `disabled` | Явно выключен — не загрузится, даже если также в `enabled` | (неважно) | Да |
| `not enabled` | Обнаружен, но никогда не включён | Нет | Нет |

По умолчанию для нового установленного или встроенного плагина — `not enabled`. `hermes plugins list` показывает все три различных состояния, чтобы вы могли видеть, что было явно отключено, а что просто ожидает включения.

В работающей сессии `/plugins` показывает, какие плагины загружены в данный момент.

## Внедрение сообщений[​](<#injecting-messages> "Прямая ссылка на Внедрение сообщений")

Плагины могут внедрять сообщения в активный разговор с помощью `ctx.inject_message()`:

[code]
    ctx.inject_message("Новые данные получены от вебхука", role="user")
    
[/code]

**Сигнатура:** `ctx.inject_message(content: str, role: str = "user") -> bool`

Как это работает:

* Если агент **бездействует** (ожидает ввода пользователя), сообщение помещается в очередь как следующий ввод и начинает новый шаг.
* Если агент **в середине шага** (активно работает), сообщение прерывает текущую операцию — так же, как если бы пользователь ввёл новое сообщение и нажал Enter.
* Для ролей, отличных от `"user"`, содержимое предваряется `[role]` (например, `[system] ...`).
* Возвращает `True`, если сообщение было успешно поставлено в очередь, `False`, если нет доступной CLI-ссылки (например, в режиме шлюза).

Это позволяет таким плагинам, как пульты удалённого управления, мосты обмена сообщениями или приёмники вебхуков, передавать сообщения в разговор из внешних источников.

> **Примечание**
> `inject_message` доступен только в режиме CLI. В режиме шлюза нет CLI-ссылки, и метод возвращает `False`.

Полное руководство см. в **[полном руководстве](</docs/guides/build-a-hermes-plugin>)** — контракты обработчиков, формат схемы, поведение хуков, обработка ошибок и распространённые ошибки.

* [Краткий обзор](<#quick-overview>)
  * [Минимальный рабочий пример](<#minimal-working-example>)
* [Что могут делать плагины](<#what-plugins-can-do>)
* [Обнаружение плагинов](<#plugin-discovery>)
  * [Подкатегории плагинов](<#plugin-sub-categories>)
* [Плагины требуют явного согласия (за некоторыми исключениями)](<#plugins-are-opt-in-with-a-few-exceptions>)
  * [Что НЕ контролируется белым списком](<#what-the-allow-list-does-not-gate>)
  * [Миграция для существующих пользователей](<#migration-for-existing-users>)
* [Доступные хуки](<#available-hooks>)
* [Типы плагинов](<#plugin-types>)
* [Расширяемые интерфейсы — куда обращаться для каждого](<#pluggable-interfaces--where-to-go-for-each>)
* [Декларативные плагины NixOS](<#nixos-declarative-plugins>)
* [Управление плагинами](<#managing-plugins>)
  * [Интерактивный интерфейс](<#interactive-ui>)
  * [Включено vs. отключено vs. ни то, ни другое](<#enabled-vs-disabled-vs-neither>)
* [Внедрение сообщений](<#injecting-messages>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins -->
