На этой странице
На этой странице описаны **команды терминала**, которые вы выполняете в оболочке.
Для слэш-команд внутри чата см. [Справочник слэш-команд](</docs/reference/slash-commands>).
## Глобальная точка входа[​](<#global-entrypoint> "Прямая ссылка на Глобальная точка входа")
[code]
    hermes [global-options] <command> [subcommand/options]
    
[/code]
### Глобальные параметры[​](<#global-options> "Прямая ссылка на Глобальные параметры")
Параметр| Описание
---|---
`--version`, `-V`| Показать версию и выйти.
`--profile <name>`, `-p <name>`| Выбрать профиль Hermes для этого вызова. Переопределяет фиксированный профиль по умолчанию, установленный командой `hermes profile use`.
`--resume <session>`, `-r <session>`| Возобновить предыдущую сессию по ID или названию.
`--continue [name]`, `-c [name]`| Возобновить самую последнюю сессию или самую последнюю сессию, соответствующую названию.
`--worktree`, `-w`| Запустить в изолированном git worktree для параллельных рабочих процессов агента.
`--yolo`| Пропустить запросы подтверждения опасных команд.
`--pass-session-id`| Включить идентификатор сессии в системный промпт агента.
`--ignore-user-config`| Игнорировать `~/.hermes/config.yaml` и использовать встроенные настройки по умолчанию. Учётные данные из `.env` по-прежнему загружаются.
`--ignore-rules`| Пропустить автоматическое внедрение `AGENTS.md`, `SOUL.md`, `.cursorrules`, памяти и предзагруженных навыков.
`--tui`| Запустить [TUI](</docs/user-guide/tui>) вместо классического CLI. Эквивалентно `HERMES_TUI=1`.
`--dev`| С `--tui`: запускать исходники TypeScript напрямую через `tsx` вместо предварительно собранного пакета (для участников разработки TUI).
## Команды верхнего уровня[​](<#top-level-commands> "Прямая ссылка на Команды верхнего уровня")
Команда| Назначение
---|---
`hermes chat`| Интерактивный или одноразовый чат с агентом.
`hermes model`| Интерактивный выбор провайдера и модели по умолчанию.
`hermes fallback`| Управление резервными провайдерами, используемыми при ошибке основной модели.
`hermes gateway`| Запуск или управление службой шлюза обмена сообщениями.
`hermes setup`| Интерактивный мастер настройки всей конфигурации или её части.
`hermes whatsapp`| Настройка и сопряжение моста WhatsApp.
`hermes slack`| Вспомогательные инструменты Slack (в настоящее время: создание манифеста приложения с каждой командой как родной слэш-командой).
`hermes auth`| Управление учётными данными — добавление, список, удаление, сброс, настройка стратегии. Обрабатывает OAuth-потоки для Codex/Nous/Anthropic.
`hermes login` / `logout`| **Устарело** — используйте `hermes auth`.
`hermes status`| Показать статус агента, аутентификации и платформы.
`hermes cron`| Просмотр и запуск планировщика cron.
`hermes kanban`| Многопрофильная доска совместной работы (задачи, ссылки, диспетчер).
`hermes webhook`| Управление динамическими подписками вебхуков для событийно-ориентированной активации.
`hermes hooks`| Просмотр, одобрение или удаление скриптов-хуков, объявленных в `config.yaml`.
`hermes doctor`| Диагностика конфигурации и проблем с зависимостями.
`hermes dump`| Сводка настройки для копирования и вставки при обращении в поддержку/отладку.
`hermes debug`| Инструменты отладки — загрузка логов и информации о системе для поддержки.
`hermes backup`| Создание резервной копии домашней директории Hermes в zip-файл.
`hermes checkpoints`| Просмотр / очистка `~/.hermes/checkpoints/` (хранилище теней, используемое `/rollback`). Запуск без аргументов показывает обзор состояния.
`hermes import`| Восстановление резервной копии Hermes из zip-файла.
`hermes logs`| Просмотр, отслеживание и фильтрация файлов логов агента/шлюза/ошибок.
`hermes config`| Просмотр, редактирование, миграция и запрос конфигурационных файлов.
`hermes pairing`| Одобрение или отзыв кодов сопряжения для обмена сообщениями.
`hermes skills`| Просмотр, установка, публикация, аудит и настройка навыков.
`hermes curator`| Фоновое обслуживание навыков — статус, запуск, пауза, закрепление. См. [Куратор](</docs/user-guide/features/curator>).
`hermes memory`| Настройка внешнего провайдера памяти. Подкоманды конкретных плагинов (например, `hermes honcho`) регистрируются автоматически, когда их провайдер активен.
`hermes acp`| Запуск Hermes как ACP-сервера для интеграции с редактором.
`hermes mcp`| Управление конфигурациями MCP-серверов и запуск Hermes как MCP-сервера.
`hermes plugins`| Управление плагинами Hermes Agent (установка, включение, отключение, удаление).
`hermes tools`| Настройка включённых инструментов для каждой платформы.
`hermes sessions`| Просмотр, экспорт, очистка, переименование и удаление сессий.
`hermes insights`| Показ аналитики токенов/затрат/активности.
`hermes fallback`| Интерактивный менеджер цепочки резервных провайдеров.
`hermes claw`| Вспомогательные инструменты миграции из OpenClaw.
`hermes dashboard`| Запуск веб-панели управления для настройки конфигурации, ключей API и сессий.
`hermes profile`| Управление профилями — несколькими изолированными экземплярами Hermes.
`hermes completion`| Вывод скриптов автодополнения для оболочки (bash/zsh/fish).
`hermes version`| Показать информацию о версии.
`hermes update`| Получить последний код и переустановить зависимости. `--check` выводит diff коммитов без загрузки; `--backup` создаёт снимок `HERMES_HOME` до загрузки.
`hermes uninstall`| Удалить Hermes из системы.
## `hermes chat`[​](<#hermes-chat> "Прямая ссылка на hermes-chat")
[code]
    hermes chat [options]
    
[/code]
Общие параметры:
Параметр| Описание
---|---
`-q`, `--query "..."`| Одноразовый неинтерактивный запрос.
`-m`, `--model <model>`| Переопределить модель для этого запуска.
`-t`, `--toolsets <csv>`| Включить набор инструментов через запятую.
`--provider <provider>`| Принудительно указать провайдера: `auto`, `openrouter`, `nous`, `openai-codex`, `copilot-acp`, `copilot`, `anthropic`, `gemini`, `google-gemini-cli`, `huggingface`, `zai`, `kimi-coding`, `kimi-coding-cn`, `minimax`, `minimax-cn`, `minimax-oauth`, `kilocode`, `xiaomi`, `arcee`, `gmi`, `alibaba`, `alibaba-coding-plan` (псевдоним `alibaba_coding`), `deepseek`, `nvidia`, `ollama-cloud`, `xai` (псевдоним `grok`), `qwen-oauth`, `bedrock`, `opencode-zen`, `opencode-go`, `ai-gateway`, `azure-foundry`, `tencent-tokenhub` (псевдонимы `tencent`, `tokenhub`).
`-s`, `--skills <name>`| Предзагрузить один или несколько навыков для сессии (можно повторить или указать через запятую).
`-v`, `--verbose`| Подробный вывод.
`-Q`, `--quiet`| Программный режим: скрыть баннер/спиннер/предпросмотр инструментов.
`--image <path>`| Прикрепить локальное изображение к одному запросу.
`--resume <session>` / `--continue [name]`| Возобновить сессию напрямую из `chat`.
`--worktree`| Создать изолированный git worktree для этого запуска.
`--checkpoints`| Включить контрольные точки файловой системы перед опасными изменениями файлов.
`--yolo`| Пропустить запросы подтверждения.
`--pass-session-id`| Передать идентификатор сессии в системный промпт.
`--ignore-user-config`| Игнорировать `~/.hermes/config.yaml` и использовать встроенные настройки по умолчанию. Учётные данные из `.env` по-прежнему загружаются. Полезно для изолированных CI-запусков, воспроизводимых отчётов об ошибках и сторонних интеграций.
`--ignore-rules`| Пропустить автоматическое внедрение `AGENTS.md`, `SOUL.md`, `.cursorrules`, постоянной памяти и предзагруженных навыков. Комбинируется с `--ignore-user-config` для полностью изолированного запуска.
`--source <tag>`| Тег источника сессии для фильтрации (по умолчанию: `cli`). Используйте `tool` для сторонних интеграций, которые не должны появляться в списке пользовательских сессий.
`--max-turns <N>`| Максимальное количество итераций вызова инструментов за один оборот разговора (по умолчанию: 90 или `agent.max_turns` в конфиге).
Примеры:
[code]
    hermes
    hermes chat -q "Summarize the latest PRs"
    hermes chat --provider openrouter --model anthropic/claude-sonnet-4.6
    hermes chat --toolsets web,terminal,skills
    hermes chat --quiet -q "Return only JSON"
    hermes chat --worktree -q "Review this repo and open a PR"
    hermes chat --ignore-user-config --ignore-rules -q "Repro without my personal setup"
    
[/code]
### `hermes -z <prompt>` — скриптовый одноразовый запрос[​](<#hermes--z-prompt--scripted-one-shot> "Прямая ссылка на hermes--z-prompt--scripted-one-shot")
Для программных вызывающих программ (shell-скрипты, CI, cron, родительские процессы, передающие запрос через pipe) `hermes -z` — это самая чистая одноразовая точка входа: **один запрос на входе, текст финального ответа на выходе, ничего лишнего в stdout или stderr.** Ни баннера, ни спиннера, ни предпросмотра инструментов, ни строки `Session:` — только финальный ответ агента в виде обычного текста.
[code]
    hermes -z "What's the capital of France?"
    # → Paris.
      
    # Parent scripts can cleanly capture the response:
    answer=$(hermes -z "summarize this" < /path/to/file.txt)
    
[/code]
Переопределения на один запуск (без изменения `~/.hermes/config.yaml`):
Флаг| Эквивалентная переменная окружения| Назначение
---|---|---
`-m` / `--model <model>`| `HERMES_INFERENCE_MODEL`| Переопределить модель для этого запуска
`--provider <provider>`| `HERMES_INFERENCE_PROVIDER`| Переопределить провайдера для этого запуска
[code]
    hermes -z "…" --provider openrouter --model openai/gpt-5.5
    # or:
    HERMES_INFERENCE_MODEL=anthropic/claude-sonnet-4.6 hermes -z "…"
    
[/code]
Тот же агент, те же инструменты, те же навыки — просто убирает все интерактивные/оформительские слои. Если вам также нужен вывод инструментов в расшифровке, используйте `hermes chat -q`; `-z` предназначен строго для «мне нужен только финальный ответ».
## `hermes model`[​](<#hermes-model> "Прямая ссылка на hermes-model")
Интерактивный выбор провайдера и модели. **Это команда для добавления новых провайдеров, настройки ключей API и выполнения OAuth-потоков.** Запускайте её из терминала — не из активной чат-сессии Hermes.
[code]
    hermes model
    
[/code]
Используйте это, когда хотите:
  * **добавить нового провайдера** (OpenRouter, Anthropic, Copilot, DeepSeek, собственный и т.д.)
  * войти в провайдеров с поддержкой OAuth (Anthropic, Copilot, Codex, Nous Portal)
  * ввести или обновить ключи API
  * выбрать из списка моделей конкретного провайдера
  * настроить собственную/самостоятельно размещённую конечную точку
  * сохранить новые настройки по умолчанию в конфиг


hermes model vs /model — знайте разницу
**`hermes model`** (запускается из терминала, вне любой сессии Hermes) — это **полный мастер настройки провайдера**. Он может добавлять новых провайдеров, выполнять OAuth-потоки, запрашивать ключи API и настраивать конечные точки.
**`/model`** (вводится внутри активной чат-сессии Hermes) может только **переключаться между уже настроенными провайдерами и моделями**. Он не может добавлять новых провайдеров, выполнять OAuth или запрашивать ключи API.
**Если вам нужно добавить нового провайдера:** Выйдите из сессии Hermes (`Ctrl+C` или `/quit`), затем выполните `hermes model` из терминала.
### `/model` слэш-команда (внутри сессии)[​](<#model-slash-command-mid-session> "Прямая ссылка на model-slash-command-mid-session")
Переключение между уже настроенными моделями без выхода из сессии:
[code]
    /model                              # Show current model and available options
    /model claude-sonnet-4              # Switch model (auto-detects provider)
    /model zai:glm-5                    # Switch provider and model
    /model custom:qwen-2.5              # Use model on your custom endpoint
    /model custom                       # Auto-detect model from custom endpoint
    /model custom:local:qwen-2.5        # Use a named custom provider
    /model openrouter:anthropic/claude-sonnet-4  # Switch back to cloud
    
[/code]
По умолчанию изменения `/model` применяются **только к текущей сессии**. Добавьте `--global`, чтобы сохранить изменение в `config.yaml`:
[code]
    /model claude-sonnet-4 --global     # Switch and save as new default
    
[/code]
Что делать, если я вижу только модели OpenRouter?
Если вы настроили только OpenRouter, `/model` покажет только модели OpenRouter. Чтобы добавить другого провайдера (Anthropic, DeepSeek, Copilot и т.д.), выйдите из сессии и выполните `hermes model` из терминала.
Изменения провайдера и базового URL автоматически сохраняются в `config.yaml`. При переключении с собственной конечной точки устаревший базовый URL очищается, чтобы не просочиться в других провайдеров.
## `hermes gateway`[​](<#hermes-gateway> "Прямая ссылка на hermes-gateway")
[code]
    hermes gateway <subcommand>
    
[/code]
Подкоманды:
Подкоманда| Описание
---|---
`run`| Запустить шлюз в интерактивном режиме. Рекомендуется для WSL, Docker и Termux.
`start`| Запустить установленный фоновый сервис systemd/launchd.
`stop`| Остановить сервис (или процесс в интерактивном режиме).
`restart`| Перезапустить сервис.
`status`| Показать статус сервиса.
`install`| Установить как фоновый сервис systemd (Linux) или launchd (macOS).
`uninstall`| Удалить установленный сервис.
`setup`| Интерактивная настройка платформ обмена сообщениями.
Параметры:
Параметр| Описание
---|---
`--all`| При `start` / `restart` / `stop`: воздействовать на шлюз **каждого профиля**, а не только активного `HERMES_HOME`. Полезно, если вы запускаете несколько профилей одновременно и хотите перезапустить их все после `hermes update`.
Пользователи WSL
Используйте `hermes gateway run` вместо `hermes gateway start` — поддержка systemd в WSL ненадёжна. Запустите его в tmux для сохранения: `tmux new -s hermes 'hermes gateway run'`. См. [WSL FAQ](</docs/reference/faq#wsl-gateway-keeps-disconnecting-or-hermes-gateway-start-fails>) для подробностей.
## `hermes setup`[​](<#hermes-setup> "Прямая ссылка на hermes-setup")
[code]
    hermes setup [model|tts|terminal|gateway|tools|agent] [--non-interactive] [--reset] [--quick] [--reconfigure]
    
[/code]
**Первый запуск:** запускает мастер первого запуска.
**Повторный пользователь (уже настроен):** переходит прямо в полный мастер перенастройки — каждый запрос показывает текущее значение по умолчанию, нажмите Enter, чтобы оставить, или введите новое значение. Без меню.
Переход к одному разделу вместо полного мастера:
Раздел| Описание
---|---
`model`| Настройка провайдера и модели.
`terminal`| Настройка терминального бэкенда и песочницы.
`gateway`| Настройка платформы обмена сообщениями.
`tools`| Включение/отключение инструментов для каждой платформы.
`agent`| Настройки поведения агента.
Параметры:
Параметр| Описание
---|---
`--quick`| Для повторных запусков: запрашивать только отсутствующие или ненастроенные элементы. Пропустить уже настроенные элементы.
`--non-interactive`| Использовать значения по умолчанию / переменные окружения без запросов.
`--reset`| Сбросить конфигурацию на значения по умолчанию перед настройкой.
`--reconfigure`| Псевдоним для обратной совместимости — простой `hermes setup` на существующей установке теперь делает это по умолчанию.
## `hermes whatsapp`[​](<#hermes-whatsapp> "Прямая ссылка на hermes-whatsapp")
[code]
    hermes whatsapp
    
[/code]
Запускает процесс сопряжения/настройки WhatsApp, включая выбор режима и сопряжение по QR-коду.
## `hermes slack`[​](<#hermes-slack> "Прямая ссылка на hermes-slack")
[code]
    hermes slack manifest              # print manifest to stdout
    hermes slack manifest --write      # write to ~/.hermes/slack-manifest.json
    hermes slack manifest --slashes-only  # just the features.slash_commands array
    
[/code]
Создаёт манифест приложения Slack, который регистрирует каждую команду шлюза из `COMMAND_REGISTRY` (`/btw`, `/stop`, `/model`, …) как полноценную слэш-команду Slack — для паритета с Discord и Telegram. Вставьте вывод в конфигурацию приложения Slack на <https://api.slack.com/apps> → ваше приложение → **Features → App Manifest → Edit**, затем **Save**. Slack предложит переустановку, если изменились области видимости или слэш-команды.
Флаг| По умолчанию| Назначение
---|---|---
`--write [PATH]`| stdout| Записать в файл вместо stdout. Простой `--write` записывает в `$HERMES_HOME/slack-manifest.json`.
`--name NAME`| `Hermes`| Отображаемое имя бота в Slack.
`--description DESC`| описание по умолчанию| Описание бота, показываемое в каталоге приложений Slack.
`--slashes-only`| выкл| Выдать только `features.slash_commands` для объединения с вручную поддерживаемым манифестом.
Запустите `hermes slack manifest --write` снова после `hermes update`, чтобы подхватить новые команды.
## `hermes login` / `hermes logout` _(Устарело)_[​](<#hermes-login--hermes-logout-deprecated> "Прямая ссылка на hermes-login--hermes-logout-deprecated")
предупреждение
`hermes login` удалена. Используйте `hermes auth` для управления учётными данными OAuth, `hermes model` для выбора провайдера или `hermes setup` для полной интерактивной настройки.
## `hermes auth`[​](<#hermes-auth> "Прямая ссылка на hermes-auth")
Управление пулами учётных данных для ротации ключей одного провайдера. См. [Пулы учётных данных](</docs/user-guide/features/credential-pools>) для полной документации.
[code]
    hermes auth                                              # Interactive wizard
    hermes auth list                                         # Show all pools
    hermes auth list openrouter                              # Show specific provider
    hermes auth add openrouter --api-key sk-or-v1-xxx        # Add API key
    hermes auth add anthropic --type oauth                   # Add OAuth credential
    hermes auth remove openrouter 2                          # Remove by index
    hermes auth reset openrouter                             # Clear cooldowns
    
[/code]
Подкоманды: `add`, `list`, `remove`, `reset`. При вызове без подкоманды запускает интерактивный мастер управления.
## `hermes status`[​](<#hermes-status> "Прямая ссылка на hermes-status")
[code]
    hermes status [--all] [--deep]
    
[/code]
Параметр| Описание
---|---
`--all`| Показать все детали в формате, пригодном для публикации с редактированием.
`--deep`| Выполнить более глубокие проверки, которые могут занять больше времени.
## `hermes cron`[​](<#hermes-cron> "Прямая ссылка на hermes-cron")
[code]
    hermes cron <list|create|edit|pause|resume|run|remove|status|tick>
    
[/code]
Подкоманда| Описание
---|---
`list`| Показать запланированные задания.
`create` / `add`| Создать запланированное задание из промпта, опционально прикрепив один или несколько навыков через повторяемый `--skill`.
`edit`| Обновить расписание, промпт, имя, доставку, количество повторов или прикреплённые навыки задания. Поддерживает `--clear-skills`, `--add-skill` и `--remove-skill`.
`pause`| Приостановить задание без удаления.
`resume`| Возобновить приостановленное задание и вычислить его следующий запуск.
`run`| Запустить задание при следующем тике планировщика.
`remove`| Удалить запланированное задание.
`status`| Проверить, запущен ли планировщик cron.
`tick`| Выполнить задания, срок которых наступил, и выйти.
## `hermes kanban`[​](<#hermes-kanban> "Прямая ссылка на hermes-kanban")
[code]
    hermes kanban [--board <slug>] <action> [options]
    
[/code]
Многопрофильная, многопроектная доска совместной работы. Каждая установка может содержать несколько досок (по одной на проект, репозиторий или домен); каждая доска представляет собой отдельную очередь с собственной БД SQLite и областью действия диспетчера. Новая установка начинается с одной доски под названием `default`, чья БД находится в `~/.hermes/kanban.db` для обратной совместимости; дополнительные доски находятся в `~/.hermes/kanban/boards/<slug>/kanban.db`. Диспетчер, встроенный в шлюз, обрабатывает каждую доску за каждый тик.
**Глобальные флаги (применяются ко всем действиям ниже):**
Флаг| Назначение
---|---
`--board <slug>`| Работать с конкретной доской. По умолчанию — текущая доска (установленная через `hermes kanban boards switch`, переменную окружения `HERMES_KANBAN_BOARD` или `default`).
**Это интерфейс для человека / скриптов.** Рабочие агенты, запущенные диспетчером, управляют доской через выделенный набор инструментов `kanban_*` [toolset](</docs/user-guide/features/kanban#how-workers-interact-with-the-board>) (`kanban_show`, `kanban_complete`, `kanban_block`, `kanban_create`, `kanban_link`, `kanban_comment`, `kanban_heartbeat`), а не через вызов `hermes kanban` в оболочке. Рабочие агенты имеют `HERMES_KANBAN_BOARD` закреплённым в своём окружении, поэтому физически не могут видеть другие доски.
Действие| Назначение
---|---
`init`| Создать `kanban.db`, если отсутствует. Идемпотентно.
`boards list` / `boards ls`| Список всех досок с количеством задач. `--json`, `--all` (включая архивированные).
`boards create <slug>`| Создать новую доску. Флаги: `--name`, `--description`, `--icon`, `--color`, `--switch` (сделать активной). Slug в kebab-case, автоматически приводится к нижнему регистру.
`boards switch <slug>` / `boards use`| Сохранить `<slug>` как активную доску (записывает `~/.hermes/kanban/current`).
`boards show` / `boards current`| Вывести имя текущей активной доски, путь к БД и количество задач.
`boards rename <slug> "<name>"`| Изменить отображаемое имя доски. Slug неизменяем.
`boards rm <slug>`| Архивировать (по умолчанию) или полностью удалить доску. `--delete` пропускает шаг архивации. Архивированные доски перемещаются в `boards/_archived/<slug>-<ts>/`. Отказано для `default`.
`create "<title>"`| Создать новую задачу на активной доске. Флаги: `--body`, `--assignee`, `--parent` (повторяемый), `--workspace scratch|worktree|dir:<path>`, `--tenant`, `--priority`, `--triage`, `--idempotency-key`, `--max-runtime`, `--skill` (повторяемый).
`list` / `ls`| Список задач на активной доске. Фильтр с `--mine`, `--assignee`, `--status`, `--tenant`, `--archived`, `--json`.
`show <id>`| Показать задачу с комментариями и событиями. `--json` для машинного вывода.
`assign <id> <profile>`| Назначить или переназначить. Используйте `none` для снятия назначения. Отказано, пока задача выполняется.
`link <parent> <child>`| Добавить зависимость. С обнаружением циклов. Обе задачи должны быть на одной доске.
`unlink <parent> <child>`| Удалить зависимость.
`claim <id>`| Атомарно забрать готовую задачу. Выводит разрешённый путь рабочего пространства.
`comment <id> "<text>"`| Добавить комментарий. Следующий работник, забравший задачу, прочитает его как часть ответа `kanban_show()`.
`complete <id>`| Отметить задачу как выполненную. Флаги: `--result`, `--summary`, `--metadata`.
`block <id> "<reason>"`| Отметить задачу как заблокированную. Также добавляет причину как комментарий.
`unblock <id>`| Вернуть заблокированную задачу в состояние готовности.
`archive <id>`| Скрыть из списка по умолчанию. `gc` удалит временные рабочие пространства.
`tail <id>`| Следить за потоком событий задачи.
`dispatch`| Один проход диспетчера по активной доске. Флаги: `--dry-run`, `--max N`, `--json`.
`context <id>`| Вывести полный контекст, который увидит работник (заголовок + тело + результаты родительской задачи + комментарии).
`gc`| Удалить временные рабочие пространства для архивированных задач.
Примеры:
[code]
    # Create a second board and put a task on it without switching away.
    hermes kanban boards create atm10-server --name "ATM10 Server" --icon 🎮
    hermes kanban --board atm10-server create "Restart server" --assignee ops
      
    # Switch the active board for subsequent calls.
    hermes kanban boards switch atm10-server
    hermes kanban list                  # shows atm10-server tasks
      
    # Archive a board (recoverable) or hard-delete it.
    hermes kanban boards rm atm10-server
    hermes kanban boards rm atm10-server --delete
    
[/code]
Порядок разрешения доски (от высшего к низшему приоритету): флаг `--board <slug>` → переменная окружения `HERMES_KANBAN_BOARD` → файл `~/.hermes/kanban/current` → `default`.
Все действия также доступны как слэш-команда в шлюзе (`/kanban …`) с тем же набором аргументов — включая подкоманды `boards` и флаг `--board`.
Полное описание — сравнение с Cline Kanban / Paperclip / NanoClaw / Gemini Enterprise, восемь паттернов совместной работы, четыре пользовательских сценария, доказательство корректности конкурентности — см. `docs/hermes-kanban-v1-spec.pdf` в репозитории или [руководство пользователя Kanban](</docs/user-guide/features/kanban>).
## `hermes webhook`[​](<#hermes-webhook> "Прямая ссылка на hermes-webhook")
[code]
    hermes webhook <subscribe|list|remove|test>
    
[/code]
Управление динамическими подписками вебхуков для событийно-ориентированной активации агента. Требует, чтобы платформа вебхуков была включена в конфиге — если не настроена, выводит инструкции по настройке.
Подкоманда| Описание
---|---
`subscribe` / `add`| Создать маршрут вебхука. Возвращает URL и HMAC-секрет для настройки в вашем сервисе.
`list` / `ls`| Показать все подписки, созданные агентом.
`remove` / `rm`| Удалить динамическую подписку. Статические маршруты из `config.yaml` не затрагиваются.
`test`| Отправить тестовый POST-запрос для проверки работоспособности подписки.
### `hermes webhook subscribe`[​](<#hermes-webhook-subscribe> "Прямая ссылка на hermes-webhook-subscribe")
[code]
    hermes webhook subscribe <name> [options]
    
[/code]
Параметр| Описание
---|---
`--prompt`| Шаблон промпта со ссылками на полезную нагрузку в формате `{dot.notation}`.
`--events`| Типы событий через запятую для принятия (например, `issues,pull_request`). Пусто = все.
`--description`| Описание, читаемое человеком.
`--skills`| Имена навыков через запятую для загрузки во время запуска агента.
`--deliver`| Цель доставки: `log` (по умолчанию), `telegram`, `discord`, `slack`, `github_comment`.
`--deliver-chat-id`| ID целевого чата/канала для кросс-платформенной доставки.
`--secret`| Пользовательский HMAC-секрет. Автоматически генерируется, если не указан.
`--deliver-only`| Пропустить агента — доставить обработанный `--prompt` как буквальное сообщение. Нулевая стоимость LLM, доставка за доли секунды. Требует, чтобы `--deliver` указывал на реальную цель (не `log`).
Подписки сохраняются в `~/.hermes/webhook_subscriptions.json` и горячо перезагружаются адаптером вебхуков без перезапуска шлюза.
## `hermes doctor`[​](<#hermes-doctor> "Прямая ссылка на hermes-doctor")
[code]
    hermes doctor [--fix]
    
[/code]
Параметр| Описание
---|---
`--fix`| Попытаться автоматически исправить проблемы, где это возможно.
## `hermes dump`[​](<#hermes-dump> "Прямая ссылка на hermes-dump")
[code]
    hermes dump [--show-keys]
    
[/code]
Выводит компактную текстовую сводку всей вашей настройки Hermes. Предназначена для копирования и вставки в Discord, GitHub issues или Telegram при обращении за поддержкой — без ANSI-цветов, без специального форматирования, только данные.
Параметр| Описание
---|---
`--show-keys`| Показать сокращённые префиксы ключей API (первые и последние 4 символа) вместо просто `set`/`not set`.
### Что включает[​](<#what-it-includes> "Прямая ссылка на Что включает")
Раздел| Детали
---|---
**Заголовок**| Версия Hermes, дата релиза, хеш коммита git
**Окружение**| ОС, версия Python, версия OpenAI SDK
**Идентификация**| Имя активного профиля, путь HERMES_HOME
**Модель**| Настроенная модель и провайдер по умолчанию
**Терминал**| Тип бэкенда (local, docker, ssh и т.д.)
**Ключи API**| Проверка наличия всех 22 ключей API провайдеров/инструментов
**Функции**| Включённые наборы инструментов, количество MCP-серверов, провайдер памяти
**Сервисы**| Статус шлюза, настроенные платформы обмена сообщениями
**Нагрузка**| Количество заданий cron, количество установленных навыков
**Переопределения конфига**| Любые значения конфига, отличающиеся от значений по умолчанию
### Пример вывода[​](<#example-output> "Прямая ссылка на Пример вывода")
[code]
    --- hermes dump ---
    version:          0.8.0 (2026.4.8) [af4abd2f]
    os:               Linux 6.14.0-37-generic x86_64
    python:           3.11.14
    openai_sdk:       2.24.0
    profile:          default
    hermes_home:      ~/.hermes
    model:            anthropic/claude-opus-4.6
    provider:         openrouter
    terminal:         local
      
    api_keys:
      openrouter           set
      openai               not set
      anthropic            set
      nous                 not set
      firecrawl            set
      ...
      
    features:
      toolsets:           all
      mcp_servers:        0
      memory_provider:    built-in
      gateway:            running (systemd)
      platforms:          telegram, discord
      cron_jobs:          3 active / 5 total
      skills:             42
      
    config_overrides:
      agent.max_turns: 250
      compression.threshold: 0.85
      display.streaming: True
    --- end dump ---
    
[/code]
### Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Сообщение об ошибке на GitHub — вставьте дамп в свой issue
  * Просьба о помощи в Discord — поделитесь в блоке кода
  * Сравнение своей настройки с чужой
  * Быстрая проверка работоспособности, когда что-то не работает


совет
`hermes dump` специально разработан для обмена. Для интерактивной диагностики используйте `hermes doctor`. Для визуального обзора используйте `hermes status`.
## `hermes debug`[​](<#hermes-debug> "Прямая ссылка на hermes-debug")
[code]
    hermes debug share [options]
    
[/code]
Загрузить отладочный отчёт (информация о системе + последние логи) в сервис вставок и получить URL для обмена. Полезно для быстрых запросов в поддержку — включает всё, что нужно помощнику для диагностики вашей проблемы.
Параметр| Описание
---|---
`--lines <N>`| Количество строк лога для включения на файл (по умолчанию: 200).
`--expire <days>`| Срок действия вставки в днях (по умолчанию: 7).
`--local`| Вывести отчёт локально вместо загрузки.
Отчёт включает информацию о системе (ОС, версия Python, версия Hermes), последние логи агента и шлюза (ограничение 512 КБ на файл) и статус ключей API (с редактированием). Ключи всегда редактируются — никакие секреты не загружаются.
Сервисы вставок пробуются по порядку: paste.rs, dpaste.com.
### Примеры[​](<#examples> "Прямая ссылка на Примеры")
[code]
    hermes debug share              # Upload debug report, print URL
    hermes debug share --lines 500  # Include more log lines
    hermes debug share --expire 30  # Keep paste for 30 days
    hermes debug share --local      # Print report to terminal (no upload)
    
[/code]
## `hermes backup`[​](<#hermes-backup> "Прямая ссылка на hermes-backup")
[code]
    hermes backup [options]
    
[/code]
Создать zip-архив вашей конфигурации Hermes, навыков, сессий и данных. Резервная копия исключает саму кодовую базу hermes-agent.
Параметр| Описание
---|---
`-o`, `--output <path>`| Путь вывода для zip-файла (по умолчанию: `~/hermes-backup-<timestamp>.zip`).
`-q`, `--quick`| Быстрый снимок: только критически важные файлы состояния (config.yaml, state.db, .env, auth, cron jobs). Намного быстрее полной резервной копии.
`-l`, `--label <name>`| Метка для снимка (используется только с `--quick`).
Резервное копирование использует API `backup()` SQLite для безопасного копирования, поэтому работает корректно, даже когда Hermes запущен (безопасно в режиме WAL).
**Что исключено из zip:**
  * `*.db-wal`, `*.db-shm`, `*.db-journal` — WAL / разделяемая память / журнальные файлы SQLite. Файл `*.db` уже получил консистентный снимок через `sqlite3.backup()`; включение живых дополнительных файлов может привести к восстановлению частично зафиксированного состояния.
  * `checkpoints/` — кэши траекторий для каждой сессии. Хранятся по хешу и перегенерируются для каждой сессии; всё равно не перенесутся чисто на другую установку.
  * Сам код `hermes-agent` (это резервная копия пользовательских данных, а не снимок репозитория).


### Примеры[​](<#examples-1> "Прямая ссылка на Примеры")
[code]
    hermes backup                           # Full backup to ~/hermes-backup-*.zip
    hermes backup -o /tmp/hermes.zip        # Full backup to specific path
    hermes backup --quick                   # Quick state-only snapshot
    hermes backup --quick --label "pre-upgrade"  # Quick snapshot with label
    
[/code]
## `hermes checkpoints`[​](<#hermes-checkpoints> "Прямая ссылка на hermes-checkpoints")
[code]
    hermes checkpoints [COMMAND]
    
[/code]
Просмотр и управление хранилищем теневых git-репозиториев в `~/.hermes/checkpoints/` — слоем хранения, используемым внутрисессионной командой `/rollback`. Безопасно запускать в любое время; не требует, чтобы агент был запущен.
Подкоманда| Описание
---|---
`status` (по умолчанию)| Показать общий размер, количество проектов и разбивку по проектам. Простой `hermes checkpoints` эквивалентен.
`list`| Псевдоним для `status`.
`prune`| Принудительная очистка — удаление осиротевших и устаревших проектов, сборка мусора в хранилище, соблюдение лимита размера. Игнорирует 24-часовую метку идемпотентности.
`clear`| Удалить всю базу контрольных точек. Необратимо; запрашивает подтверждение, если не указан `-f`.
`clear-legacy`| Удалить только архивы `legacy-<timestamp>/`, созданные при миграции v1→v2.
### Параметры[​](<#options> "Прямая ссылка на Параметры")
Параметр| Подкоманда| Описание
---|---|---
`--limit N`| `status`, `list`| Максимум проектов для отображения (по умолчанию 20).
`--retention-days N`| `prune`| Удалить проекты, чей `last_touch` старше N дней (по умолчанию 7).
`--max-size-mb N`| `prune`| После прохода осиротевших/устаревших удалить самые старые коммиты каждого проекта, пока общий размер хранилища не станет ≤ N МБ (по умолчанию 500).
`--keep-orphans`| `prune`| Пропустить удаление проектов, чья рабочая директория больше не существует.
`-f`, `--force`| `clear`, `clear-legacy`| Пропустить запрос подтверждения.
### Примеры[​](<#examples-2> "Прямая ссылка на Примеры")
[code]
    hermes checkpoints                                  # status overview
    hermes checkpoints prune --retention-days 3         # aggressive cleanup
    hermes checkpoints prune --max-size-mb 200          # tighten size cap once
    hermes checkpoints clear-legacy -f                  # drop v1 archive dirs
    hermes checkpoints clear -f                         # wipe everything
    
[/code]
См. [Контрольные точки и `/rollback`](</docs/user-guide/checkpoints-and-rollback>) для полной архитектуры и внутрисессионных команд.
## `hermes import`[​](<#hermes-import> "Прямая ссылка на hermes-import")
[code]
    hermes import <zipfile> [options]
    
[/code]
Восстановить ранее созданную резервную копию Hermes в вашу домашнюю директорию Hermes. Все файлы в архиве перезаписывают существующие файлы в вашей домашней директории Hermes; `--force` только пропускает запрос подтверждения, который появляется, когда целевая директория уже содержит установку Hermes.
Параметр| Описание
---|---
`-f`, `--force`| Пропустить запрос подтверждения существующей установки.
предупреждение
Остановите шлюз перед импортом, чтобы избежать конфликтов с запущенными процессами.
### Примеры[​](<#examples-3> "Прямая ссылка на Примеры")
[code]
    hermes import ~/hermes-backup-20260423.zip           # Prompts before overwriting existing config
    hermes import ~/hermes-backup-20260423.zip --force   # Overwrite without prompting
    
[/code]
## `hermes logs`[​](<#hermes-logs> "Прямая ссылка на hermes-logs")
[code]
    hermes logs [log_name] [options]
    
[/code]
Просмотр, отслеживание и фильтрация файлов логов Hermes. Все логи хранятся в `~/.hermes/logs/` (или `<profile>/logs/` для нестандартных профилей).
### Файлы логов[​](<#log-files> "Прямая ссылка на Файлы логов")
Имя| Файл| Что записывает
---|---|---
`agent` (по умолчанию)| `agent.log`| Вся активность агента — вызовы API, диспетчеризация инструментов, жизненный цикл сессий (INFO и выше)
`errors`| `errors.log`| Только предупреждения и ошибки — отфильтрованное подмножество agent.log
`gateway`| `gateway.log`| Активность шлюза обмена сообщениями — подключения к платформам, диспетчеризация сообщений, события вебхуков
### Параметры[​](<#options-1> "Прямая ссылка на Параметры")
Параметр| Описание
---|---
`log_name`| Какой лог просмотреть: `agent` (по умолчанию), `errors`, `gateway` или `list` для показа доступных файлов с размерами.
`-n`, `--lines <N>`| Количество строк для показа (по умолчанию: 50).
`-f`, `--follow`| Отслеживать лог в реальном времени, как `tail -f`. Нажмите Ctrl+C для остановки.
`--level <LEVEL>`| Минимальный уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
`--session <ID>`| Фильтр строк, содержащих подстроку ID сессии.
`--since <TIME>`| Показать строки с относительного времени: `30m`, `1h`, `2d` и т.д. Поддерживает `s` (секунды), `m` (минуты), `h` (часы), `d` (дни).
`--component <NAME>`| Фильтр по компоненту: `gateway`, `agent`, `tools`, `cli`, `cron`.
### Примеры[​](<#examples-4> "Прямая ссылка на Примеры")
[code]
    # View the last 50 lines of agent.log (default)
    hermes logs
      
    # Follow agent.log in real time
    hermes logs -f
      
    # View the last 100 lines of gateway.log
    hermes logs gateway -n 100
      
    # Show only warnings and errors from the last hour
    hermes logs --level WARNING --since 1h
      
    # Filter by a specific session
    hermes logs --session abc123
      
    # Follow errors.log, starting from 30 minutes ago
    hermes logs errors --since 30m -f
      
    # List all log files with their sizes
    hermes logs list
    
[/code]
### Фильтрация[​](<#filtering> "Прямая ссылка на Фильтрация")
Фильтры можно комбинировать. Когда активно несколько фильтров, строка лога должна пройти **все** их, чтобы быть показанной:
[code]
    # WARNING+ lines from the last 2 hours containing session "tg-12345"
    hermes logs --level WARNING --since 2h --session tg-12345
    
[/code]
Строки без разбираемой временной метки включаются, когда активен `--since` (это могут быть строки продолжения многстрочной записи лога). Строки без определяемого уровня включаются, когда активен `--level`.
### Ротация логов[​](<#log-rotation> "Прямая ссылка на Ротация логов")
Hermes использует `RotatingFileHandler` из Python. Старые логи ротируются автоматически — ищите `agent.log.1`, `agent.log.2` и т.д. Подкоманда `hermes logs list` показывает все файлы логов, включая ротированные.
## `hermes config`[​](<#hermes-config> "Прямая ссылка на hermes-config")
[code]
    hermes config <subcommand>
    
[/code]
Подкоманды:
Подкоманда| Описание
---|---
`show`| Показать текущие значения конфига.
`edit`| Открыть `config.yaml` в вашем редакторе.
`set <key> <value>`| Установить значение конфига.
`path`| Вывести путь к файлу конфига.
`env-path`| Вывести путь к файлу `.env`.
`check`| Проверить на отсутствующие или устаревшие настройки конфига.
`migrate`| Добавить новые опции интерактивно.
## `hermes pairing`[​](<#hermes-pairing> "Прямая ссылка на hermes-pairing")
[code]
    hermes pairing <list|approve|revoke|clear-pending>
    
[/code]
Подкоманда| Описание
---|---
`list`| Показать ожидающих и одобренных пользователей.
`approve <platform> <code>`| Одобрить код сопряжения.
`revoke <platform> <user-id>`| Отозвать доступ пользователя.
`clear-pending`| Очистить ожидающие коды сопряжения.
## `hermes skills`[​](<#hermes-skills> "Прямая ссылка на hermes-skills")
[code]
    hermes skills <subcommand>
    
[/code]
Подкоманды:
Подкоманда| Описание
---|---
`browse`| Постраничный просмотр реестров навыков.
`search`| Поиск в реестрах навыков.
`install`| Установить навык.
`inspect`| Просмотреть навык без установки.
`list`| Список установленных навыков.
`check`| Проверить установленные навыки из хаба на наличие обновлений.
`update`| Переустановить навыки из хаба с изменениями, когда они доступны.
`audit`| Повторное сканирование установленных навыков из хаба.
`uninstall`| Удалить навык, установленный из хаба.
`reset`| Снять блокировку встроенного навыка, помеченного как `user_modified`, путём очистки записи в манифесте. С `--restore` также заменяет пользовательскую копию встроенной версией.
`publish`| Опубликовать навык в реестре.
`snapshot`| Экспорт/импорт конфигураций навыков.
`tap`| Управление пользовательскими источниками навыков.
`config`| Интерактивное включение/отключение навыков для каждой платформы.
Общие примеры:
[code]
    hermes skills browse
    hermes skills browse --source official
    hermes skills search react --source skills-sh
    hermes skills search https://mintlify.com/docs --source well-known
    hermes skills inspect official/security/1password
    hermes skills inspect skills-sh/vercel-labs/json-render/json-render-react
    hermes skills install official/migration/openclaw-migration
    hermes skills install skills-sh/anthropics/skills/pdf --force
    hermes skills install https://sharethis.chat/SKILL.md                     # Direct URL (single-file SKILL.md)
    hermes skills install https://example.com/SKILL.md --name my-skill        # Override name when frontmatter has none
    hermes skills check
    hermes skills update
    hermes skills config
    hermes skills reset google-workspace
    hermes skills reset google-workspace --restore --yes
    
[/code]
Примечания:
  * `--force` может переопределять неопасные блокировки политик для сторонних/сообщественных навыков.
  * `--force` не переопределяет вердикт сканирования `dangerous`.
  * `--source skills-sh` выполняет поиск в публичном каталоге `skills.sh`.
  * `--source well-known` позволяет указать Hermes сайт, предоставляющий `/.well-known/skills/index.json`.
  * Передача URL `http(s)://…/*.md` устанавливает однофайловый SKILL.md напрямую. Если во frontmatter нет `name:` и slug URL не является допустимым идентификатором, интерактивный терминал запрашивает имя; неинтерактивные поверхности (`/skills install` внутри TUI, платформы шлюза) требуют `--name <x>`.


## `hermes curator`[​](<#hermes-curator> "Прямая ссылка на hermes-curator")
[code]
    hermes curator <subcommand>
    
[/code]
Куратор — это фоновая задача вспомогательной модели, которая периодически просматривает созданные агентом навыки, удаляет устаревшие, объединяет пересекающиеся и архивирует устаревшие навыки. Встроенные навыки и навыки, установленные из хаба, никогда не трогаются. Архивы восстанавливаемы; автоудаление никогда не происходит.
Подкоманда| Описание
---|---
`status`| Показать статус куратора и статистику навыков.
`run`| Запустить проверку куратора сейчас.
`run --sync`| Блокироваться до завершения прохода LLM.
`run --dry-run`| Только предпросмотр — создать отчёт проверки без изменений.
`backup`| Создать ручной tar.gz-снимок `~/.hermes/skills/` (куратор также создаёт снимки автоматически перед каждым реальным запуском).
`rollback`| Восстановить `~/.hermes/skills/` из снимка (по умолчанию самый новый).
`rollback --list`| Список доступных снимков.
`rollback --id <ts>`| Восстановить конкретный снимок по id.
`rollback -y`| Пропустить запрос подтверждения.
`pause`| Приостановить куратора до возобновления.
`resume`| Возобновить приостановленного куратора.
`pin <skill>`| Закрепить навык, чтобы куратор никогда не переводил его автоматически.
`unpin <skill>`| Открепить навык.
`restore <skill>`| Восстановить архивированный навык.
На новой установке первый запланированный проход откладывается на полный `interval_hours` (7 дней по умолчанию) — шлюз не будет запускать куратор сразу после первого тика после `hermes update`. Используйте `hermes curator run --dry-run` для предпросмотра до этого.
См. [Куратор](</docs/user-guide/features/curator>) для описания поведения и конфигурации.
## `hermes fallback`[​](<#hermes-fallback> "Прямая ссылка на hermes-fallback")
[code]
    hermes fallback <subcommand>
    
[/code]
Управление цепочкой резервных провайдеров. Резервные провайдеры пробуются по порядку, когда основная модель не работает из-за ошибок ограничения скорости, перегрузки или подключения.
Подкоманда| Описание
---|---
`list` (псевдоним: `ls`)| Показать текущую цепочку резервных провайдеров (по умолчанию, когда нет подкоманды).
`add`| Выбрать провайдера + модель (тот же выборщик, что и в `hermes model`) и добавить в конец цепочки.
`remove` (псевдоним: `rm`)| Выбрать запись для удаления из цепочки.
`clear`| Удалить все резервные записи.
См. [Резервные провайдеры](</docs/user-guide/features/fallback-providers>).
## `hermes hooks`[​](<#hermes-hooks> "Прямая ссылка на hermes-hooks")
[code]
    hermes hooks <subcommand>
    
[/code]
Просмотр скриптов-хуков, объявленных в `~/.hermes/config.yaml`, их тестирование с синтетическими полезными нагрузками и управление белым списком согласий при первом использовании в `~/.hermes/shell-hooks-allowlist.json`.
Подкоманда| Описание
---|---
`list` (псевдоним: `ls`)| Список настроенных хуков с сопоставителем, таймаутом и статусом согласия.
`test <event>`| Запустить все хуки, соответствующие `<event>`, с синтетической полезной нагрузкой.
`revoke` (псевдонимы: `remove`, `rm`)| Удалить записи из белого списка для команды (вступает в силу после следующего перезапуска).
`doctor`| Проверить каждый настроенный хук: бит исполняемости, белый список, расхождение mtime, валидность JSON и время выполнения синтетического запуска.
См. [Хуки](</docs/user-guide/features/hooks>) для сигнатур событий и форм полезных нагрузок.
## `hermes memory`[​](<#hermes-memory> "Прямая ссылка на hermes-memory")
[code]
    hermes memory <subcommand>
    
[/code]
Настройка и управление плагинами внешней памяти. Доступные провайдеры: honcho, openviking, mem0, hindsight, holographic, retaindb, byterover, supermemory. Одновременно может быть активен только один внешний провайдер. Встроенная память (MEMORY.md/USER.md) всегда активна.
Подкоманды:
Подкоманда| Описание
---|---
`setup`| Интерактивный выбор и настройка провайдера.
`status`| Показать текущую конфигурацию провайдера памяти.
`off`| Отключить внешнего провайдера (только встроенная память).
Подкоманды конкретного провайдера
Когда внешний провайдер памяти активен, он может зарегистрировать собственную команду верхнего уровня `hermes <provider>` для управления, специфичного для провайдера (например, `hermes honcho`, когда активен Honcho). Неактивные провайдеры не раскрывают свои подкоманды. Выполните `hermes --help`, чтобы увидеть, что в данный момент подключено.
## `hermes acp`[​](<#hermes-acp> "Прямая ссылка на hermes-acp")
[code]
    hermes acp
    
[/code]
Запускает Hermes как stdio-сервер ACP (Agent Client Protocol) для интеграции с редактором.
Связанные точки входа:
[code]
    hermes-acp
    python -m acp_adapter
    
[/code]
Сначала установите поддержку:
[code]
    pip install -e '.[acp]'
    
[/code]
См. [Интеграция ACP с редактором](</docs/user-guide/features/acp>) и [Внутреннее устройство ACP](</docs/developer-guide/acp-internals>).
## `hermes mcp`[​](<#hermes-mcp> "Прямая ссылка на hermes-mcp")
[code]
    hermes mcp <subcommand>
    
[/code]
Управление конфигурациями MCP-серверов (Model Context Protocol) и запуск Hermes как MCP-сервера.
Подкоманда| Описание
---|---
`serve [-v|--verbose]`| Запустить Hermes как MCP-сервер — предоставить диалоги другим агентам.
`add <name> [--url URL] [--command CMD] [--args ...] [--auth oauth|header]`| Добавить MCP-сервер с автоматическим обнаружением инструментов.
`remove <name>` (псевдоним: `rm`)| Удалить MCP-сервер из конфигурации.
`list` (псевдоним: `ls`)| Список настроенных MCP-серверов.
`test <name>`| Проверить подключение к MCP-серверу.
`configure <name>` (псевдоним: `config`)| Переключить выбор инструментов для сервера.
См. [Справочник конфигурации MCP](</docs/reference/mcp-config-reference>), [Использование MCP с Hermes](</docs/guides/use-mcp-with-hermes>) и [Режим MCP-сервера](</docs/user-guide/features/mcp#running-hermes-as-an-mcp-server>).
## `hermes plugins`[​](<#hermes-plugins> "Прямая ссылка на hermes-plugins")
[code]
    hermes plugins [subcommand]
    
[/code]
Унифицированное управление плагинами — общие плагины, провайдеры памяти и контекстные движки в одном месте. Запуск `hermes plugins` без подкоманды открывает составной интерактивный экран с двумя разделами:
  * **Общие плагины** — флажки для множественного выбора для включения/отключения установленных плагинов.
  * **Плагины-провайдеры** — конфигурация с одним выбором для провайдера памяти и контекстного движка. Нажмите ENTER на категории, чтобы открыть переключатель.


Подкоманда| Описание
---|---
 _(нет)_|  Составной интерактивный интерфейс — переключатели общих плагинов + конфигурация плагинов-провайдеров.
`install <identifier> [--force]`| Установить плагин из Git URL или `owner/repo`.
`update <name>`| Получить последние изменения для установленного плагина.
`remove <name>` (псевдонимы: `rm`, `uninstall`)| Удалить установленный плагин.
`enable <name>`| Включить отключённый плагин.
`disable <name>`| Отключить плагин без удаления.
`list` (псевдоним: `ls`)| Список установленных плагинов со статусом включения/отключения.
Выбор плагинов-провайдеров сохраняется в `config.yaml`:
  * `memory.provider` — активный провайдер памяти (пусто = только встроенный).
  * `context.engine` — активный контекстный движок (`"compressor"` = встроенный по умолчанию).


Список отключённых общих плагинов хранится в `config.yaml` в разделе `plugins.disabled`.
См. [Плагины](</docs/user-guide/features/plugins>) и [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>).
## `hermes tools`[​](<#hermes-tools> "Прямая ссылка на hermes-tools")
[code]
    hermes tools [--summary]
    
[/code]
Параметр| Описание
---|---
`--summary`| Вывести сводку текущих включённых инструментов и выйти.
Без `--summary` запускает интерактивный интерфейс настройки инструментов для каждой платформы.
## `hermes sessions`[​](<#hermes-sessions> "Прямая ссылка на hermes-sessions")
[code]
    hermes sessions <subcommand>
    
[/code]
Подкоманды:
Подкоманда| Описание
---|---
`list`| Список последних сессий.
`browse`| Интерактивный выбор сессии с поиском и возобновлением.
`export <output> [--session-id ID]`| Экспорт сессий в JSONL.
`delete <session-id>`| Удалить одну сессию.
`prune`| Удалить старые сессии.
`stats`| Показать статистику хранилища сессий.
`rename <session-id> <title>`| Установить или изменить название сессии.
## `hermes insights`[​](<#hermes-insights> "Прямая ссылка на hermes-insights")
[code]
    hermes insights [--days N] [--source platform]
    
[/code]
Параметр| Описание
---|---
`--days <n>`| Анализировать последние `n` дней (по умолчанию: 30).
`--source <platform>`| Фильтр по источнику, например `cli`, `telegram` или `discord`.
## `hermes claw`[​](<#hermes-claw> "Прямая ссылка на hermes-claw")
[code]
    hermes claw migrate [options]
    
[/code]
Перенесите вашу настройку OpenClaw в Hermes. Читает из `~/.openclaw` (или пользовательского пути) и записывает в `~/.hermes`. Автоматически обнаруживает устаревшие имена директорий (`~/.clawdbot`, `~/.moltbot`) и имена файлов конфигов (`clawdbot.json`, `moltbot.json`).
Параметр| Описание
---|---
`--dry-run`| Предпросмотр того, что будет перенесено, без записи.
`--preset <name>`| Пресет миграции: `full` (все совместимые настройки) или `user-data` (исключает инфраструктурную конфигурацию). Ни один пресет не импортирует секреты — передайте `--migrate-secrets` явно.
`--overwrite`| Перезаписывать существующие файлы Hermes при конфликтах (по умолчанию: отказываться применять, когда в плане есть конфликты).
`--migrate-secrets`| Включить ключи API в миграцию. Требуется даже с `--preset full`.
`--no-backup`| Пропустить создание zip-снимка `~/.hermes/` до миграции (по умолчанию один архив точки восстановления записывается в `~/.hermes/backups/pre-migration-*.zip` перед применением; восстанавливается командой `hermes import`).
`--source <path>`| Пользовательская директория OpenClaw (по умолчанию: `~/.openclaw`).
`--workspace-target <path>`| Целевая директория для инструкций рабочего пространства (AGENTS.md).
`--skill-conflict <mode>`| Обработка конфликтов имён навыков: `skip` (по умолчанию), `overwrite` или `rename`.
`--yes`| Пропустить запрос подтверждения.
### Что переносится[​](<#what-gets-migrated> "Прямая ссылка на Что переносится")
Миграция охватывает 30+ категорий: персона, память, навыки, провайдеры моделей, платформы обмена сообщениями, поведение агента, политики сессий, MCP-серверы, TTS и многое другое. Элементы либо **напрямую импортируются** в эквиваленты Hermes, либо **архивируются** для ручного просмотра.
**Напрямую импортируются:** SOUL.md, MEMORY.md, USER.md, AGENTS.md, навыки (4 исходные директории), модель по умолчанию, пользовательские провайдеры, MCP-серверы, токены платформ обмена сообщениями и белые списки (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost), значения по умолчанию агента (усиление рассуждений, сжатие, задержка человека, часовой пояс, песочница), политики сброса сессий, правила одобрения, конфигурация TTS, настройки браузера, настройки инструментов, таймаут выполнения, белый список команд, конфигурация шлюза и ключи API из 3 источников.
**Архивируются для ручного просмотра:** задания cron, плагины, хуки/вебхуки, бэкенд памяти (QMD), конфигурация реестра навыков, UI/идентичность, логирование, многопользовательская настройка, привязки каналов, IDENTITY.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md.
**Разрешение ключей API** проверяет три источника в порядке приоритета: значения конфига → `~/.openclaw/.env` → `auth-profiles.json`. Все поля токенов обрабатывают простые строки, шаблоны env (`${VAR}`) и объекты SecretRef.
Полное соответствие ключей конфига, детали обработки SecretRef и контрольный список после миграции см. в **[полном руководстве по миграции](</docs/guides/migrate-from-openclaw>)**.
### Примеры[​](<#examples-5> "Прямая ссылка на Примеры")
[code]
    # Preview what would be migrated
    hermes claw migrate --dry-run
      
    # Full migration (all compatible settings, no secrets)
    hermes claw migrate --preset full
      
    # Full migration including API keys
    hermes claw migrate --preset full --migrate-secrets
      
    # Migrate user data only (no secrets), overwrite conflicts
    hermes claw migrate --preset user-data --overwrite
      
    # Migrate from a custom OpenClaw path
    hermes claw migrate --source /home/user/old-openclaw
    
[/code]
## `hermes dashboard`[​](<#hermes-dashboard> "Прямая ссылка на hermes-dashboard")
[code]
    hermes dashboard [options]
    
[/code]
Запустить веб-панель управления — браузерный интерфейс для управления конфигурацией, ключами API и мониторинга сессий. Требует `pip install hermes-agent[web]` (FastAPI + Uvicorn). См. [Веб-панель управления](</docs/user-guide/features/web-dashboard>) для полной документации.
Параметр| По умолчанию| Описание
---|---|---
`--port`| `9119`| Порт для запуска веб-сервера
`--host`| `127.0.0.1`| Адрес привязки
`--no-open`| —| Не открывать браузер автоматически
[code]
    # Default — opens browser to http://127.0.0.1:9119
    hermes dashboard
      
    # Custom port, no browser
    hermes dashboard --port 8080 --no-open
    
[/code]
## `hermes profile`[​](<#hermes-profile> "Прямая ссылка на hermes-profile")
[code]
    hermes profile <subcommand>
    
[/code]
Управление профилями — несколькими изолированными экземплярами Hermes, каждый со своей конфигурацией, сессиями, навыками и домашней директорией.
Подкоманда| Описание
---|---
`list`| Список всех профилей.
`use <name>`| Установить фиксированный профиль по умолчанию.
`create <name> [--clone] [--clone-all] [--clone-from <source>] [--no-alias]`| Создать новый профиль. `--clone` копирует конфиг, `.env` и `SOUL.md` из активного профиля. `--clone-all` копирует всё состояние. `--clone-from` указывает исходный профиль.
`delete <name> [-y]`| Удалить профиль.
`show <name>`| Показать детали профиля (домашняя директория, конфиг и т.д.).
`alias <name> [--remove] [--name NAME]`| Управление скриптами-обёртками для быстрого доступа к профилю.
`rename <old> <new>`| Переименовать профиль.
`export <name> [-o FILE]`| Экспортировать профиль в архив `.tar.gz`.
`import <archive> [--name NAME]`| Импортировать профиль из архива `.tar.gz`.
Примеры:
[code]
    hermes profile list
    hermes profile create work --clone
    hermes profile use work
    hermes profile alias work --name h-work
    hermes profile export work -o work-backup.tar.gz
    hermes profile import work-backup.tar.gz --name restored
    hermes -p work chat -q "Hello from work profile"
    
[/code]
## `hermes completion`[​](<#hermes-completion> "Прямая ссылка на hermes-completion")
[code]
    hermes completion [bash|zsh|fish]
    
[/code]
Вывести скрипт автодополнения оболочки в stdout. Добавьте вывод в ваш профиль оболочки для автодополнения команд Hermes, подкоманд и имён профилей по табуляции.
Примеры:
[code]
    # Bash
    hermes completion bash >> ~/.bashrc
      
    # Zsh
    hermes completion zsh >> ~/.zshrc
      
    # Fish
    hermes completion fish > ~/.config/fish/completions/hermes.fish
    
[/code]
## `hermes update`[​](<#hermes-update> "Прямая ссылка на hermes-update")
[code]
    hermes update [--check] [--backup] [--restart-gateway]
    
[/code]
Загружает последний код `hermes-agent` и переустанавливает зависимости в вашем виртуальном окружении, затем повторно запускает хуки после установки (MCP-серверы, синхронизация навыков, установка автодополнения). Безопасно запускать на работающей установке.
Параметр| Описание
---|---
`--check`| Вывести рядом текущий коммит и последний коммит `origin/main` и выйти с кодом 0, если синхронизировано, или 1, если есть отставание. Не загружает, не устанавливает и не перезапускает ничего.
`--backup`| Создать помеченный снимок `HERMES_HOME` до обновления (конфиг, аутентификация, сессии, навыки, данные сопряжения) перед загрузкой. По умолчанию **выключен** — предыдущее поведение с постоянным резервным копированием добавляло минуты к каждому обновлению на больших домашних директориях. Включите его постоянно через `update.backup: true` в `config.yaml`.
`--restart-gateway`| После успешного обновления перезапустить работающий сервис шлюза. Подразумевает семантику `--all`, если установлено несколько профилей.
Дополнительное поведение:
  * **Снимок данных сопряжения.** Даже когда `--backup` выключен, `hermes update` создаёт лёгкий снимок `~/.hermes/pairing/` и правил комментариев Feishu перед `git pull`. Вы можете откатить его с помощью `hermes backup restore --state pre-update`, если загрузка перезаписывает файл, который вы редактировали.
  * **Предупреждение о legacy `hermes.service`.** Если Hermes обнаруживает systemd-юнит `hermes.service` (до переименования) вместо текущего `hermes-gateway.service`, выводится одноразовая подсказка по миграции, чтобы избежать проблем с циклом флапа.
  * **Коды выхода.** `0` при успехе, `1` при ошибках загрузки/установки/пост-установки, `2` при неожиданных изменениях в рабочем дереве, блокирующих `git pull`.


## `hermes fallback`[​](<#hermes-fallback-1> "Прямая ссылка на hermes-fallback-1")
[code]
    hermes fallback           # interactive manager
    
[/code]
Управление цепочкой резервных провайдеров (используется, когда ваш основной провайдер достигает ограничения скорости или возвращает фатальную ошибку) без ручного редактирования `config.yaml`. Повторно использует выборщик провайдера из `hermes model` — тот же список провайдеров, те же запросы учётных данных, та же валидация.
Типичная сессия:
  1. Нажмите `a`, чтобы добавить резервного провайдера → выберите провайдера (OAuth-провайдеры открывают браузер; провайдеры с API-ключами запрашивают ключ), затем выберите конкретную модель.
  2. Используйте `↑`/`↓` для изменения порядка резервных провайдеров (первый в списке пробуется первым).
  3. Нажмите `d`, чтобы удалить один.


Все изменения сохраняются в список `fallback_providers:` верхнего уровня в `config.yaml`. Взаимодействует с [Пулами учётных данных](</docs/user-guide/features/credential-pools>): пулы вращают ключи _внутри_ провайдера, резервные провайдеры переключаются на _другого_ провайдера полностью.
См. [Резервные провайдеры](</docs/user-guide/features/fallback-providers>) для деталей поведения и взаимодействия с `fallback_model` (устаревший ключ с одним резервным провайдером).
## Команды обслуживания[​](<#maintenance-commands> "Прямая ссылка на Команды обслуживания")
Команда| Описание
---|---
`hermes version`| Вывести информацию о версии.
`hermes update`| Загрузить последние изменения и переустановить зависимости.
`hermes uninstall [--full] [--yes]`| Удалить Hermes, опционально удалив все конфиги/данные.
## См. также[​](<#see-also> "Прямая ссылка на См. также")
  * [Справочник слэш-команд](</docs/reference/slash-commands>)
  * [Интерфейс CLI](</docs/user-guide/cli>)
  * [Сессии](</docs/user-guide/sessions>)
  * [Система навыков](</docs/user-guide/features/skills>)
  * [Скины и темы](</docs/user-guide/features/skins>)


  * [Глобальная точка входа](<#global-entrypoint>)
    * [Глобальные параметры](<#global-options>)
  * [Команды верхнего уровня](<#top-level-commands>)
  * [`hermes chat`](<#hermes-chat>)
    * [`hermes -z <prompt>` — скриптовый одноразовый запрос](<#hermes--z-prompt--scripted-one-shot>)
  * [`hermes model`](<#hermes-model>)
    * [`/model` слэш-команда (внутри сессии)](<#model-slash-command-mid-session>)
  * [`hermes gateway`](<#hermes-gateway>)
  * [`hermes setup`](<#hermes-setup>)
  * [`hermes whatsapp`](<#hermes-whatsapp>)
  * [`hermes slack`](<#hermes-slack>)
  * [`hermes login` / `hermes logout` _(Устарело)_](<#hermes-login--hermes-logout-deprecated>)
  * [`hermes auth`](<#hermes-auth>)
  * [`hermes status`](<#hermes-status>)
  * [`hermes cron`](<#hermes-cron>)
  * [`hermes kanban`](<#hermes-kanban>)
  * [`hermes webhook`](<#hermes-webhook>)
    * [`hermes webhook subscribe`](<#hermes-webhook-subscribe>)
  * [`hermes doctor`](<#hermes-doctor>)
  * [`hermes dump`](<#hermes-dump>)
    * [Что включает](<#what-it-includes>)
    * [Пример вывода](<#example-output>)
    * [Когда использовать](<#when-to-use>)
  * [`hermes debug`](<#hermes-debug>)
    * [Примеры](<#examples>)
  * [`hermes backup`](<#hermes-backup>)
    * [Примеры](<#examples-1>)
  * [`hermes checkpoints`](<#hermes-checkpoints>)
    * [Параметры](<#options>)
    * [Примеры](<#examples-2>)
  * [`hermes import`](<#hermes-import>)
    * [Примеры](<#examples-3>)
  * [`hermes logs`](<#hermes-logs>)
    * [Файлы логов](<#log-files>)
    * [Параметры](<#options-1>)
    * [Примеры](<#examples-4>)
    * [Фильтрация](<#filtering>)
    * [Ротация логов](<#log-rotation>)
  * [`hermes config`](<#hermes-config>)
  * [`hermes pairing`](<#hermes-pairing>)
  * [`hermes skills`](<#hermes-skills>)
  * [`hermes curator`](<#hermes-curator>)
  * [`hermes fallback`](<#hermes-fallback>)
  * [`hermes hooks`](<#hermes-hooks>)
  * [`hermes memory`](<#hermes-memory>)
  * [`hermes acp`](<#hermes-acp>)
  * [`hermes mcp`](<#hermes-mcp>)
  * [`hermes plugins`](<#hermes-plugins>)
  * [`hermes tools`](<#hermes-tools>)
  * [`hermes sessions`](<#hermes-sessions>)
  * [`hermes insights`](<#hermes-insights>)
  * [`hermes claw`](<#hermes-claw>)
    * [Что переносится](<#what-gets-migrated>)
    * [Примеры](<#examples-5>)
  * [`hermes dashboard`](<#hermes-dashboard>)
  * [`hermes profile`](<#hermes-profile>)
  * [`hermes completion`](<#hermes-completion>)
  * [`hermes update`](<#hermes-update>)
  * [`hermes fallback`](<#hermes-fallback-1>)
  * [Команды обслуживания](<#maintenance-commands>)
  * [См. также](<#see-also>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/cli-commands -->
