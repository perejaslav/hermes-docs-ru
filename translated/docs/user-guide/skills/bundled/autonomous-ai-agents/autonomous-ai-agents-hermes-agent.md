На этой странице
Настройка, расширение и участие в разработке Hermes Agent.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")

|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию)  |
|Путь| `skills/autonomous-ai-agents/hermes-agent`  |
|Версия| `2.1.0`  |
|Автор| Hermes Agent + Teknium  |
|Лицензия| MIT  |
|Теги| `hermes`, `setup`, `configuration`, `multi-agent`, `spawning`, `cli`, `gateway`, `development`  |
|Связанные навыки| [`claude-code`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code>), [`codex`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>), [`opencode`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

> **info**
> Ниже представлено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.

# Hermes Agent
Hermes Agent — это фреймворк для создания AI-агентов с открытым исходным кодом от Nous Research, работающий в вашем терминале, мессенджерах и IDE. Он относится к той же категории, что и Claude Code (Anthropic), Codex (OpenAI) и OpenClaw — автономные агенты для написания кода и выполнения задач, использующие вызов инструментов для взаимодействия с вашей системой. Hermes работает с любым LLM-провайдером (OpenRouter, Anthropic, OpenAI, DeepSeek, локальные модели и ещё 15+) и поддерживает Linux, macOS и WSL.

Что делает Hermes особенным:
  * **Самообучение через навыки** — Hermes учится на опыте, сохраняя многократно используемые процедуры в виде навыков. Когда он решает сложную задачу, находит рабочий процесс или получает исправление, он может сохранить эти знания как документ навыка, который загружается в будущие сессии. Навыки накапливаются со временем, делая агента более эффективным в ваших конкретных задачах и окружении.
  * **Постоянная память между сессиями** — запоминает, кто вы, ваши предпочтения, детали окружения и извлечённые уроки. Подключаемые бэкенды памяти (встроенный, Honcho, Mem0 и другие) позволяют выбирать, как работает память.
  * **Мультиплатформенный шлюз** — один и тот же агент работает в Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email и на 10+ других платформах с полным доступом к инструментам, а не только к чату.
  * **Независимость от провайдера** — меняйте модели и провайдеров на ходу, ничего больше не меняя. Пул учётных данных автоматически ротируется между несколькими API-ключами.
  * **Профили** — запускайте несколько независимых экземпляров Hermes с изолированными конфигами, сессиями, навыками и памятью.
  * **Расширяемость** — плагины, MCP-серверы, пользовательские инструменты, вебхуки, cron-планировщик и вся экосистема Python.

Люди используют Hermes для разработки ПО, исследований, администрирования систем, анализа данных, создания контента, домашней автоматизации и всего остального, что выигрывает от AI-агента с постоянным контекстом и полным доступом к системе.
**Этот навык помогает эффективно работать с Hermes Agent** — настраивать его, конфигурировать функции, порождать дополнительные экземпляры агента, устранять неполадки, находить нужные команды и настройки, а также понимать, как система устроена, когда требуется её расширить или внести вклад в её развитие.
**Документация:** <https://hermes-agent.nousresearch.com/docs/>
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")

[code] 
    # Установка  
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash  
      
    # Интерактивный чат (по умолчанию)  
    hermes  
      
    # Одиночный запрос  
    hermes chat -q "What is the capital of France?"  
      
    # Мастер настройки  
    hermes setup  
      
    # Смена модели/провайдера  
    hermes model  
      
    # Проверка здоровья  
    hermes doctor  
    
[/code]

* * *
## Справочник CLI[​](<#cli-reference> "Прямая ссылка на Справочник CLI")

### Глобальные флаги[​](<#global-flags> "Прямая ссылка на Глобальные флаги")

[code] 
    hermes [flags] [command]  
      
      --version, -V             Показать версию  
      --resume, -r SESSION      Возобновить сессию по ID или заголовку  
      --continue, -c [NAME]     Возобновить по имени или самую последнюю сессию  
      --worktree, -w            Изолированный git worktree-режим (параллельные агенты)  
      --skills, -s SKILL        Предзагрузить навыки (через запятую или повторением)  
      --profile, -p NAME        Использовать именованный профиль  
      --yolo                    Пропускать подтверждение опасных команд  
      --pass-session-id         Включать ID сессии в системный промпт  
    
[/code]

Если подкоманда не указана, по умолчанию используется `chat`.

### Чат[​](<#chat> "Прямая ссылка на Чат")

[code] 
    hermes chat [flags]  
      -q, --query TEXT          Одиночный запрос, неинтерактивный режим  
      -m, --model MODEL         Модель (например, anthropic/claude-sonnet-4)  
      -t, --toolsets LIST       Список наборов инструментов через запятую  
      --provider PROVIDER       Принудительно указать провайдера (openrouter, anthropic, nous и т.д.)  
      -v, --verbose             Подробный вывод  
      -Q, --quiet               Скрыть баннер, спиннер, превью инструментов  
      --checkpoints             Включить контрольные точки файловой системы (/rollback)  
      --source TAG              Тег источника сессии (по умолчанию: cli)  
    
[/code]

### Конфигурация[​](<#configuration> "Прямая ссылка на Конфигурация")

[code] 
    hermes setup [section]      Интерактивный мастер (model|terminal|gateway|tools|agent)  
    hermes model                Интерактивный выбор модели/провайдера  
    hermes config               Просмотр текущей конфигурации  
    hermes config edit          Открыть config.yaml в $EDITOR  
    hermes config set KEY VAL   Установить значение конфигурации  
    hermes config path          Показать путь к config.yaml  
    hermes config env-path      Показать путь к .env  
    hermes config check         Проверить отсутствующие/устаревшие настройки  
    hermes config migrate       Обновить конфигурацию новыми опциями  
    hermes login [--provider P] OAuth-вход (nous, openai-codex)  
    hermes logout               Очистить сохранённую аутентификацию  
    hermes doctor [--fix]       Проверить зависимости и конфигурацию  
    hermes status [--all]       Показать состояние компонентов  
    
[/code]

### Инструменты и навыки[​](<#tools--skills> "Прямая ссылка на Инструменты и навыки")

[code] 
    hermes tools                Интерактивное включение/отключение инструментов (curses UI)  
    hermes tools list           Показать все инструменты и их статус  
    hermes tools enable NAME    Включить набор инструментов  
    hermes tools disable NAME   Отключить набор инструментов  
      
    hermes skills list          Список установленных навыков  
    hermes skills search QUERY  Поиск в хабе навыков  
    hermes skills install ID    Установить навык (ID может быть идентификатором хаба ИЛИ прямой https://…/SKILL.md URL; используйте --name для переопределения, если в frontmatter нет имени)  
    hermes skills inspect ID    Предпросмотр без установки  
    hermes skills config        Включение/отключение навыков по платформам  
    hermes skills check         Проверить наличие обновлений  
    hermes skills update        Обновить устаревшие навыки  
    hermes skills uninstall N   Удалить навык из хаба  
    hermes skills publish PATH  Опубликовать в реестре  
    hermes skills browse        Просмотр всех доступных навыков  
    hermes skills tap add REPO  Добавить GitHub-репозиторий как источник навыков  
    
[/code]

### MCP-серверы[​](<#mcp-servers> "Прямая ссылка на MCP-серверы")

[code] 
    hermes mcp serve            Запустить Hermes как MCP-сервер  
    hermes mcp add NAME         Добавить MCP-сервер (--url или --command)  
    hermes mcp remove NAME      Удалить MCP-сервер  
    hermes mcp list             Список настроенных серверов  
    hermes mcp test NAME        Проверить соединение  
    hermes mcp configure NAME   Переключить выбор инструментов  
    
[/code]

### Gateway (мессенджеры)[​](<#gateway-messaging-platforms> "Прямая ссылка на Gateway (мессенджеры)")

[code] 
    hermes gateway run          Запустить gateway на переднем плане  
    hermes gateway install      Установить как фоновый сервис  
    hermes gateway start/stop   Управление сервисом  
    hermes gateway restart      Перезапустить сервис  
    hermes gateway status       Проверить статус  
    hermes gateway setup        Настроить платформы  
    
[/code]

Поддерживаемые платформы: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI подключается через адаптер API Server.
Документация по платформам: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>

### Сессии[​](<#sessions> "Прямая ссылка на Сессии")

[code] 
    hermes sessions list        Список последних сессий  
    hermes sessions browse      Интерактивный выбор  
    hermes sessions export OUT  Экспорт в JSONL  
    hermes sessions rename ID T Переименовать сессию  
    hermes sessions delete ID   Удалить сессию  
    hermes sessions prune       Очистить старые сессии (--older-than N дней)  
    hermes sessions stats       Статистика хранилища сессий  
    
[/code]

### Cron-задачи[​](<#cron-jobs> "Прямая ссылка на Cron-задачи")

[code] 
    hermes cron list            Список задач (--all для отключённых)  
    hermes cron create SCHED    Создать: '30m', 'every 2h', '0 9 * * *'  
    hermes cron edit ID         Редактировать расписание, промпт, доставку  
    hermes cron pause/resume ID Управление состоянием задачи  
    hermes cron run ID          Запустить при следующем тике  
    hermes cron remove ID       Удалить задачу  
    hermes cron status          Статус планировщика  
    
[/code]

### Вебхуки[​](<#webhooks> "Прямая ссылка на Вебхуки")

[code] 
    hermes webhook subscribe N  Создать маршрут по адресу /webhooks/<name>  
    hermes webhook list         Список подписок  
    hermes webhook remove NAME  Удалить подписку  
    hermes webhook test NAME    Отправить тестовый POST  
    
[/code]

### Профили[​](<#profiles> "Прямая ссылка на Профили")

[code] 
    hermes profile list         Список всех профилей  
    hermes profile create NAME  Создать (--clone, --clone-all, --clone-from)  
    hermes profile use NAME     Установить как постоянный по умолчанию  
    hermes profile delete NAME  Удалить профиль  
    hermes profile show NAME    Показать детали  
    hermes profile alias NAME   Управление скриптами-обёртками  
    hermes profile rename A B   Переименовать профиль  
    hermes profile export NAME  Экспорт в tar.gz  
    hermes profile import FILE  Импорт из архива  
    
[/code]

### Пулы учётных данных[​](<#credential-pools> "Прямая ссылка на Пулы учётных данных")

[code] 
    hermes auth add             Интерактивный мастер учётных данных  
    hermes auth list [PROVIDER] Список учётных данных в пуле  
    hermes auth remove P INDEX  Удалить по провайдеру и индексу  
    hermes auth reset PROVIDER  Сбросить статус исчерпания  
    
[/code]

### Прочее[​](<#other> "Прямая ссылка на Прочее")

[code] 
    hermes insights [--days N]  Аналитика использования  
    hermes update               Обновление до последней версии  
    hermes pairing list/approve/revoke  Авторизация DM  
    hermes plugins list/install/remove  Управление плагинами  
    hermes honcho setup/status  Интеграция памяти Honcho (требуется плагин honcho)  
    hermes memory setup/status/off  Настройка провайдера памяти  
    hermes completion bash|zsh  Автодополнение для оболочки  
    hermes acp                  ACP-сервер (интеграция с IDE)  
    hermes claw migrate         Миграция из OpenClaw  
    hermes uninstall            Удаление Hermes  
    
[/code]

* * *
## Слэш-команды (внутри сессии)[​](<#slash-commands-in-session> "Прямая ссылка на Слэш-команды (внутри сессии)")

Вводите эти команды во время интерактивной чат-сессии. Новые команды появляются довольно часто; если что-то ниже выглядит устаревшим, выполните `/help` в сессии для получения актуального списка или обратитесь к [справочнику слэш-команд](<https://hermes-agent.nousresearch.com/docs/reference/slash-commands>). Основной реестр находится в `hermes_cli/commands.py` — каждый потребитель (автодополнение, меню Telegram, привязка Slack, `/help`) берёт данные из него.

### Управление сессией[​](<#session-control> "Прямая ссылка на Управление сессией")

[code] 
    /new (/reset)        Новая сессия  
    /clear               Очистить экран + новая сессия (CLI)  
    /retry               Отправить последнее сообщение заново  
    /undo                Удалить последний обмен  
    /title [name]        Назвать сессию  
    /compress            Сжать контекст вручную  
    /stop                Остановить фоновые процессы  
    /rollback [N]        Восстановить контрольную точку файловой системы  
    /snapshot [sub]      Создать или восстановить снимки состояния конфигурации/состояния Hermes (CLI)  
    /background <prompt> Выполнить промпт в фоне  
    /queue <prompt>      Поставить в очередь на следующий ход  
    /steer <prompt>      Вставить сообщение после следующего вызова инструмента без прерывания  
    /agents (/tasks)     Показать активных агентов и запущенные задачи  
    /resume [name]       Возобновить именованную сессию  
    /goal [text|sub]     Установить постоянную цель, над которой Hermes работает между ходами до достижения  
                         (подкоманды: status, pause, resume, clear)  
    /redraw              Принудительная полная перерисовка UI (CLI)  
    
[/code]

### Конфигурация[​](<#configuration-1> "Прямая ссылка на Конфигурация")

[code] 
    /config              Показать конфигурацию (CLI)  
    /model [name]        Показать или сменить модель  
    /personality [name]  Установить личность  
    /reasoning [level]   Установить уровень рассуждения (none|minimal|low|medium|high|xhigh|show|hide)  
    /verbose             Цикл: off → new → all → verbose  
    /voice [on|off|tts]  Голосовой режим  
    /yolo                Переключить обход подтверждения  
    /busy [sub]          Управление действием Enter, пока Hermes работает (CLI)  
                         (подкоманды: queue, steer, interrupt, status)  
    /indicator [style]   Выбрать стиль индикатора занятости TUI (CLI)  
                         (стили: kaomoji, emoji, unicode, ascii)  
    /footer [on|off]     Переключить метаданные времени выполнения gateway в финальных ответах  
    /skin [name]         Сменить тему (CLI)  
    /statusbar           Переключить строку состояния (CLI)  
    
[/code]

### Инструменты и навыки[​](<#tools--skills-1> "Прямая ссылка на Инструменты и навыки")

[code] 
    /tools               Управление инструментами (CLI)  
    /toolsets            Список наборов инструментов (CLI)  
    /skills              Поиск/установка навыков (CLI)  
    /skill <name>        Загрузить навык в сессию  
    /reload-skills       Пересканировать ~/.hermes/skills/ на предмет добавленных/удалённых навыков  
    /reload              Перезагрузить переменные .env в текущую сессию (CLI)  
    /reload-mcp          Перезагрузить MCP-серверы  
    /cron                Управление cron-задачами (CLI)  
    /curator [sub]       Фоновое обслуживание навыков (status, run, pin, archive, …)  
    /kanban [sub]        Мультипрофильная доска совместной работы (tasks, links, comments)  
    /plugins             Список плагинов (CLI)  
    
[/code]

### Gateway[​](<#gateway> "Прямая ссылка на Gateway")

[code] 
    /approve             Подтвердить ожидающую команду (gateway)  
    /deny                Отклонить ожидающую команду (gateway)  
    /restart             Перезапустить gateway (gateway)  
    /sethome             Установить текущий чат как домашний канал (gateway)  
    /update              Обновить Hermes до последней версии (gateway)  
    /topic [sub]         Включить или просмотреть сессии Telegram DM по темам (gateway)  
    /platforms (/gateway) Показать статус подключения платформ (gateway)  
    
[/code]

### Утилиты[​](<#utility> "Прямая ссылка на Утилиты")

[code] 
    /branch (/fork)      Разветвить текущую сессию  
    /fast                Переключить приоритет/быструю обработку  
    /browser             Открыть соединение CDP-браузера  
    /history             Показать историю разговора (CLI)  
    /save                Сохранить разговор в файл (CLI)  
    /copy [N]            Скопировать последний ответ ассистента в буфер обмена (CLI)  
    /paste               Прикрепить изображение из буфера обмена (CLI)  
    /image               Прикрепить локальный файл изображения (CLI)  
    
[/code]

### Информация[​](<#info> "Прямая ссылка на Информация")

[code] 
    /help                Показать команды  
    /commands [page]     Просмотреть все команды (gateway)  
    /usage               Использование токенов  
    /insights [days]     Аналитика использования  
    /gquota              Показать использование квоты Google Gemini Code Assist (CLI)  
    /status              Информация о сессии (gateway)  
    /profile             Информация об активном профиле  
    /debug               Загрузить отчёт об отладке (информация о системе + логи) и получить ссылки для отправки  
    
[/code]

### Выход[​](<#exit> "Прямая ссылка на Выход")

[code] 
    /quit (/exit, /q)    Выйти из CLI  
    
[/code]

* * *
## Ключевые пути и конфигурация[​](<#key-paths--config> "Прямая ссылка на Ключевые пути и конфигурация")

[code] 
    ~/.hermes/config.yaml       Основная конфигурация  
    ~/.hermes/.env              API-ключи и секреты  
    $HERMES_HOME/skills/        Установленные навыки  
    ~/.hermes/sessions/         Транскрипты сессий  
    ~/.hermes/logs/             Логи gateway и ошибок  
    ~/.hermes/auth.json         OAuth-токены и пулы учётных данных  
    ~/.hermes/hermes-agent/     Исходный код (если установлен через git)  
    
[/code]

Профили используют `~/.hermes/profiles/<name>/` с такой же структурой.

### Секции конфигурации[​](<#config-sections> "Прямая ссылка на Секции конфигурации")

Редактируйте через `hermes config edit` или `hermes config set section.key value`.

| Секция | Ключевые опции |
|---|---|
|`model`| `default`, `provider`, `base_url`, `api_key`, `context_length`  |
|`agent`| `max_turns` (90), `tool_use_enforcement`  |
|`terminal`| `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180)  |
|`compression`| `enabled`, `threshold` (0.50), `target_ratio` (0.20)  |
|`display`| `skin`, `tool_progress`, `show_reasoning`, `show_cost`  |
|`stt`| `enabled`, `provider` (local/groq/openai/mistral)  |
|`tts`| `provider` (edge/elevenlabs/openai/minimax/mistral/neutts)  |
|`memory`| `memory_enabled`, `user_profile_enabled`, `provider`  |
|`security`| `tirith_enabled`, `website_blocklist`  |
|`delegation`| `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort`  |
|`checkpoints`| `enabled`, `max_snapshots` (50)  |

Полный справочник конфигурации: <https://hermes-agent.nousresearch.com/docs/user-guide/configuration>

### Провайдеры[​](<#providers> "Прямая ссылка на Провайдеры")

Поддерживается 20+ провайдеров. Настраиваются через `hermes model` или `hermes setup`.

| Провайдер | Аутентификация | Переменная окружения для ключа |
|---|---|---|
|OpenRouter| API-ключ| `OPENROUTER_API_KEY`  |
|Anthropic| API-ключ| `ANTHROPIC_API_KEY`  |
|Nous Portal| OAuth| `hermes auth`  |
|OpenAI Codex| OAuth| `hermes auth`  |
|GitHub Copilot| Токен| `COPILOT_GITHUB_TOKEN`  |
|Google Gemini| API-ключ| `GOOGLE_API_KEY` или `GEMINI_API_KEY`  |
|DeepSeek| API-ключ| `DEEPSEEK_API_KEY`  |
|xAI / Grok| API-ключ| `XAI_API_KEY`  |
|Hugging Face| Токен| `HF_TOKEN`  |
|Z.AI / GLM| API-ключ| `GLM_API_KEY`  |
|MiniMax| API-ключ| `MINIMAX_API_KEY`  |
|MiniMax CN| API-ключ| `MINIMAX_CN_API_KEY`  |
|Kimi / Moonshot| API-ключ| `KIMI_API_KEY`  |
|Alibaba / DashScope| API-ключ| `DASHSCOPE_API_KEY`  |
|Xiaomi MiMo| API-ключ| `XIAOMI_API_KEY`  |
|Kilo Code| API-ключ| `KILOCODE_API_KEY`  |
|AI Gateway (Vercel)| API-ключ| `AI_GATEWAY_API_KEY`  |
|OpenCode Zen| API-ключ| `OPENCODE_ZEN_API_KEY`  |
|OpenCode Go| API-ключ| `OPENCODE_GO_API_KEY`  |
|Qwen OAuth| OAuth| `hermes login --provider qwen-oauth`  |
|Пользовательская endpoint| Конфиг| `model.base_url` + `model.api_key` в config.yaml  |
|GitHub Copilot ACP| Внешняя| `COPILOT_CLI_PATH` или Copilot CLI  |

Полная документация по провайдерам: <https://hermes-agent.nousresearch.com/docs/integrations/providers>

### Наборы инструментов[​](<#toolsets> "Прямая ссылка на Наборы инструментов")

Включение/отключение через `hermes tools` (интерактивно) или `hermes tools enable/disable NAME`.

| Набор инструментов | Что предоставляет |
|---|---|
|`web`| Веб-поиск и извлечение содержимого  |
|`search`| Только веб-поиск (подмножество `web`)  |
|`browser`| Автоматизация браузера (Browserbase, Camofox или локальный Chromium)  |
|`terminal`| Команды оболочки и управление процессами  |
|`file`| Чтение/запись/поиск/патчинг файлов  |
|`code_execution`| Изолированное выполнение Python  |
|`vision`| Анализ изображений  |
|`image_gen`| Генерация изображений AI  |
|`video`| Анализ и генерация видео  |
|`tts`| Синтез речи  |
|`skills`| Просмотр и управление навыками  |
|`memory`| Постоянная память между сессиями  |
|`session_search`| Поиск по прошлым разговорам  |
|`delegation`| Делегирование задач саб-агентам  |
|`cronjob`| Управление запланированными задачами  |
|`clarify`| Запрос уточняющих вопросов у пользователя  |
|`messaging`| Кроссплатформенная отправка сообщений  |
|`todo`| Планирование и отслеживание задач внутри сессии  |
|`kanban`| Инструменты многозадачной очереди работ (ограничены для воркеров)  |
|`debugging`| Дополнительные инструменты интроспекции/отладки (отключено по умолчанию)  |
|`safe`| Минимальный набор инструментов с низким риском для изолированных сессий  |
|`spotify`| Управление воспроизведением и плейлистами Spotify  |
|`homeassistant`| Управление умным домом (отключено по умолчанию)  |
|`discord`| Инструменты интеграции Discord  |
|`discord_admin`| Инструменты администрирования/модерации Discord  |
|`feishu_doc`| Инструменты для документов Feishu (Lark)  |
|`feishu_drive`| Инструменты для диска Feishu (Lark)  |
|`yuanbao`| Инструменты интеграции Yuanbao  |
|`rl`| Инструменты обучения с подкреплением (отключено по умолчанию)  |
|`moa`| Mixture of Agents (отключено по умолчанию)  |

Полный перечень находится в `toolsets.py` как словарь `TOOLSETS`; `_HERMES_CORE_TOOLS` — это набор по умолчанию, который наследуется большинством платформ.
Изменения инструментов вступают в силу после `/reset` (новая сессия). Они НЕ применяются в середине разговора, чтобы сохранить кэширование промптов.

* * *
## Переключатели безопасности и конфиденциальности[​](<#security--privacy-toggles> "Прямая ссылка на Переключатели безопасности и конфиденциальности")

Распространённые переключатели на вопрос «почему Hermes делает X с моим выводом / вызовами инструментов / командами?» — и точные команды для их изменения. Большинство из них требуют новой сессии (`/reset` в чате или запуск нового вызова `hermes`), поскольку считываются однократно при запуске.

### Редактирование секретов в выводе инструментов[​](<#secret-redaction-in-tool-output> "Прямая ссылка на Редактирование секретов в выводе инструментов")

Редактирование секретов **отключено по умолчанию** — вывод инструментов (stdout терминала, `read_file`, веб-содержимое, сводки саб-агентов и т.д.) передаётся без изменений. Если пользователь хочет, чтобы Hermes автоматически маскировал строки, похожие на API-ключи, токены и секреты, прежде чем они попадут в контекст разговора и логи:

[code] 
    hermes config set security.redact_secrets true       # включить глобально  
    
[/code]

**Требуется перезапуск.** `security.redact_secrets` фиксируется во время импорта — переключение в середине сессии (например, через `export HERMES_REDACT_SECRETS=true` из вызова инструмента) НЕ повлияет на работающий процесс. Сообщите пользователю выполнить `hermes config set security.redact_secrets true` в терминале, а затем запустить новую сессию. Это сделано намеренно — чтобы LLM не могла переключить эту настройку сама себе в середине задачи.

Отключить снова:

[code] 
    hermes config set security.redact_secrets false  
    
[/code]

### Редактирование PII в сообщениях gateway[​](<#pii-redaction-in-gateway-messages> "Прямая ссылка на Редактирование PII в сообщениях gateway")

Отдельно от редактирования секретов. При включении gateway хеширует ID пользователей и удаляет номера телефонов из контекста сессии до того, как он попадёт к модели:

[code] 
    hermes config set privacy.redact_pii true    # включить  
    hermes config set privacy.redact_pii false   # отключить (по умолчанию)  
    
[/code]

### Подтверждение команд[​](<#command-approval-prompts> "Прямая ссылка на Подтверждение команд")

По умолчанию (`approvals.mode: manual`) Hermes запрашивает подтверждение пользователя перед выполнением команд оболочки, помеченных как опасные (`rm -rf`, `git reset --hard` и т.д.). Режимы:
  * `manual` — всегда запрашивать (по умолчанию)
  * `smart` — использовать вспомогательную LLM для автоматического одобрения низкорисковых команд, запрашивать для высокорисковых
  * `off` — пропускать все запросы (эквивалент `--yolo`)

[code] 
    hermes config set approvals.mode smart       # рекомендуемый компромисс  
    hermes config set approvals.mode off         # пропускать всё (не рекомендуется)  
    
[/code]

Обход без изменения конфигурации для одного запуска:
  * `hermes --yolo …`
  * `export HERMES_YOLO_MODE=1`

Примечание: YOLO / `approvals.mode: off` НЕ отключает редактирование секретов. Это независимые настройки.

### Белый список хуков оболочки[​](<#shell-hooks-allowlist> "Прямая ссылка на Белый список хуков оболочки")

Некоторые интеграции с хуками оболочки требуют явного добавления в белый список перед срабатыванием. Управляется через `~/.hermes/shell-hooks-allowlist.json` — запрос появляется интерактивно при первой попытке выполнения хука.

### Отключение инструментов web/browser/image-gen[​](<#disabling-the-webbrowserimage-gen-tools> "Прямая ссылка на Отключение инструментов web/browser/image-gen")

Чтобы полностью ограничить доступ модели к сети или медиа-инструментам, откройте `hermes tools` и переключите настройки для каждой платформы. Изменения вступят в силу при следующей сессии (`/reset`). См. раздел «Инструменты и навыки» выше.

* * *
## Голос и транскрипция[​](<#voice--transcription> "Прямая ссылка на Голос и транскрипция")

### STT (голос → текст)[​](<#stt-voice--text> "Прямая ссылка на STT (голос → текст)")

Голосовые сообщения из мессенджеров автоматически транскрибируются.
Приоритет провайдера (автоопределение):
  1. **Локальный faster-whisper** — бесплатно, не требует API-ключа: `pip install faster-whisper`
  2. **Groq Whisper** — бесплатный тариф: установите `GROQ_API_KEY`
  3. **OpenAI Whisper** — платный: установите `VOICE_TOOLS_OPENAI_KEY`
  4. **Mistral Voxtral** — установите `MISTRAL_API_KEY`

Конфигурация:

[code] 
    stt:  
      enabled: true  
      provider: local        # local, groq, openai, mistral  
      local:  
        model: base          # tiny, base, small, medium, large-v3  
    
[/code]

### TTS (текст → голос)[​](<#tts-text--voice> "Прямая ссылка на TTS (текст → голос)")

| Провайдер | Переменная окружения | Бесплатно? |
|---|---|---|
|Edge TTS| Нет| Да (по умолчанию)  |
|ElevenLabs| `ELEVENLABS_API_KEY`| Бесплатный тариф  |
|OpenAI| `VOICE_TOOLS_OPENAI_KEY`| Платно  |
|MiniMax| `MINIMAX_API_KEY`| Платно  |
|Mistral (Voxtral)| `MISTRAL_API_KEY`| Платно  |
|NeuTTS (локальный)| Нет (`pip install neutts[all]` + `espeak-ng`)| Бесплатно  |

Голосовые команды: `/voice on` (голос-в-голос), `/voice tts` (только голос), `/voice off`.

* * *
## Порожденение дополнительных экземпляров Hermes[​](<#spawning-additional-hermes-instances> "Прямая ссылка на Порожденение дополнительных экземпляров Hermes")

Запускайте дополнительные процессы Hermes как полностью независимые подпроцессы — отдельные сессии, инструменты и окружения.

### Когда использовать это вместо delegate_task[​](<#when-to-use-this-vs-delegate_task> "Прямая ссылка на Когда использовать это вместо delegate_task")

| | `delegate_task` | Порожденение процесса `hermes` |
|---|---|---|
|Изоляция| Отдельный разговор, общий процесс| Полностью независимый процесс  |
|Длительность| Минуты (ограничено родительским циклом)| Часы/дни  |
|Доступ к инструментам| Подмножество инструментов родителя| Полный доступ к инструментам  |
|Интерактивность| Нет| Да (PTY-режим)  |
|Сценарий| Быстрые параллельные подзадачи| Длительные автономные миссии  |

### Одноразовый режим[​](<#one-shot-mode> "Прямая ссылка на Одноразовый режим")

[code] 
    terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)  
      
    # Фоновый режим для длительных задач:  
    terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)  
    
[/code]

### Интерактивный PTY-режим (через tmux)[​](<#interactive-pty-mode-via-tmux> "Прямая ссылка на Интерактивный PTY-режим (через tmux)")

Hermes использует prompt_toolkit, которому требуется настоящий терминал. Используйте tmux для интерактивного порождения:

[code] 
    # Запуск  
    terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)  
      
    # Дождаться запуска, затем отправить сообщение  
    terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)  
      
    # Прочитать вывод  
    terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)  
      
    # Отправить дополнительное сообщение  
    terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)  
      
    # Выход  
    terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)  
    
[/code]

### Мультиагентная координация[​](<#multi-agent-coordination> "Прямая ссылка на Мультиагентная координация")

[code] 
    # Агент A: бэкенд  
    terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)  
    terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)  
      
    # Агент B: фронтенд  
    terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)  
    terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)  
      
    # Проверить прогресс, передать контекст между ними  
    terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)  
    terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)  
    
[/code]

### Возобновление сессии[​](<#session-resume> "Прямая ссылка на Возобновление сессии")

[code] 
    # Возобновить самую последнюю сессию  
    terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)  
      
    # Возобновить конкретную сессию  
    terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)  
    
[/code]

### Советы[​](<#tips> "Прямая ссылка на Советы")

  * **Предпочитайте `delegate_task` для быстрых подзадач** — меньше накладных расходов, чем порождение полного процесса
  * **Используйте `-w` (worktree-режим)** при порождении агентов, редактирующих код — предотвращает конфликты git
  * **Устанавливайте тайм-ауты** для одноразового режима — сложные задачи могут занимать 5-10 минут
  * **Используйте `hermes chat -q` для fire-and-forget** — PTY не требуется
  * **Используйте tmux для интерактивных сессий** — у сырого PTY-режима есть проблемы с `\r` vs `\n` в prompt_toolkit
  * **Для запланированных задач** используйте инструмент `cronjob` вместо порождения — он обрабатывает доставку и повторные попытки

* * *
## Постоянные и фоновые системы[​](<#durable--background-systems> "Прямая ссылка на Постоянные и фоновые системы")

Четыре системы работают параллельно с основным циклом разговора. Краткий справочник здесь; полная документация для разработчиков находится в `AGENTS.md`, пользовательская — в `website/docs/user-guide/features/`.

### Делегирование (`delegate_task`)[​](<#delegation-delegate_task> "Прямая ссылка на Делегирование (delegate_task)")

Синхронное порождение саб-агента — родитель ждёт сводки от дочернего агента, прежде чем продолжить свой цикл. Изолированный контекст + сессия терминала.
  * **Одиночный:** `delegate_task(goal, context, toolsets)`.
  * **Пакетный:** `delegate_task(tasks=[{goal, ...}, ...])` запускает дочерние агенты параллельно, ограничено `delegation.max_concurrent_children` (по умолчанию 3).
  * **Роли:** `leaf` (по умолчанию; не может делегировать дальше) vs `orchestrator` (может порождать своих воркеров, ограничено `delegation.max_spawn_depth`).
  * **Непостоянный.** Если родитель прерван, дочерний процесс отменяется. Для работы, которая должна пережить ход, используйте `cronjob` или `terminal(background=True, notify_on_complete=True)`.

Конфигурация: `delegation.*` в `config.yaml`.

### Cron (запланированные задачи)[​](<#cron-scheduled-jobs> "Прямая ссылка на Cron (запланированные задачи)")

Постоянный планировщик — `cron/jobs.py` + `cron/scheduler.py`. Управляется через инструмент `cronjob`, CLI `hermes cron` (`list`, `add`, `edit`, `pause`, `resume`, `run`, `remove`) или слэш-команду `/cron`.
  * **Расписания:** длительность (`"30m"`, `"2h"`), фраза «every» (`"every monday 9am"`), 5-польный cron (`"0 9 * * *"`) или ISO-метка времени.
  * **Настройки для каждой задачи:** `skills`, переопределение `model`/`provider`, `script` (сбор данных перед запуском; `no_agent=True` делает скрипт всей задачей), `context_from` (цепочка: вывод задачи A → задача B), `workdir` (запуск в определённой директории с её `AGENTS.md` / `CLAUDE.md`), мультиплатформенная доставка.
  * **Инварианты:** жёсткое прерывание через 3 минуты на один запуск, файл `.tick.lock` предотвращает дублирование тиков между процессами, cron-сессии по умолчанию передают `skip_memory=True`, а доставка cron обрамляется верхним и нижним колонтитулами вместо зеркалирования в целевую gateway-сессию (сохраняет чередование ролей).

Пользовательская документация: <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>

### Curator (жизненный цикл навыков)[​](<#curator-skill-lifecycle> "Прямая ссылка на Curator (жизненный цикл навыков)")

Фоновое обслуживание навыков, созданных агентом. Отслеживает использование, помечает неиспользуемые навыки как устаревшие, архивирует устаревшие, сохраняет предварительный tar.gz-бэкап, чтобы ничего не потерялось.
  * **CLI:** `hermes curator <verb>` — `status`, `run`, `pause`, `resume`, `pin`, `unpin`, `archive`, `restore`, `prune`, `backup`, `rollback`.
  * **Слэш:** `/curator <subcommand>` повторяет CLI.
  * **Область действия:** затрагивает только навыки с происхождением `created_by: "agent"`. Встроенные навыки и установленные из хаба не трогает. **Никогда не удаляет** — максимальное деструктивное действие — архивация. Закреплённые навыки освобождены от любых авто-переходов и любых проходов LLM-рецензирования.
  * **Телеметрия:** sidecar-файл `~/.hermes/skills/.usage.json` содержит для каждого навыка `use_count`, `view_count`, `patch_count`, `last_activity_at`, `state`, `pinned`.

Конфигурация: `curator.*` (`enabled`, `interval_hours`, `min_idle_hours`, `stale_after_days`, `archive_after_days`, `backup.*`). Пользовательская документация: <https://hermes-agent.nousresearch.com/docs/user-guide/features/curator>

### Kanban (многозадачная очередь работ)[​](<#kanban-multi-agent-work-queue> "Прямая ссылка на Kanban (многозадачная очередь работ)")

Постоянная SQLite-доска для мультипрофильной / мультиворкерной совместной работы. Пользователи управляют ей через `hermes kanban <verb>`; воркеры, порождённые диспетчером, видят ограниченный набор инструментов `kanban_*`, ограниченный `HERMES_KANBAN_TASK`, так что footprint схемы равен нулю вне процессов воркеров.
  * **CLI-команды (основные):** `init`, `create`, `list` (алиас `ls`), `show`, `assign`, `link`, `unlink`, `comment`, `complete`, `block`, `unblock`, `archive`, `tail`. Менее распространённые: `watch`, `stats`, `runs`, `log`, `dispatch`, `daemon`, `gc`.
  * **Набор инструментов воркера:** `kanban_show`, `kanban_complete`, `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`, `kanban_link`.
  * **Диспетчер** запускается внутри gateway по умолчанию (`kanban.dispatch_in_gateway: true`) — отзывает устаревшие заявки, продвигает готовые задачи, атомарно назначает, порождает назначенные профили. Автоматически блокирует задачу после ~5 последовательных неудач порождения.
  * **Изоляция:** доска — жёсткая граница (воркеры получают `HERMES_KANBAN_BOARD` закреплённым в окружении); tenant — мягкое пространство имён в пределах доски для изоляции путей рабочего пространства и ключей памяти.

Пользовательская документация: <https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban>

* * *
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")

### Голос не работает[​](<#voice-not-working> "Прямая ссылка на Голос не работает")

  1. Проверьте `stt.enabled: true` в config.yaml
  2. Проверьте провайдера: `pip install faster-whisper` или установите API-ключ
  3. В gateway: `/restart`. В CLI: выйти и запустить заново.

### Инструмент недоступен[​](<#tool-not-available> "Прямая ссылка на Инструмент недоступен")

  1. `hermes tools` — проверьте, включён ли набор инструментов для вашей платформы
  2. Некоторые инструменты требуют переменных окружения (проверьте `.env`)
  3. `/reset` после включения инструментов

### Проблемы с моделью/провайдером[​](<#modelprovider-issues> "Прямая ссылка на Проблемы с моделью/провайдером")

  1. `hermes doctor` — проверьте конфигурацию и зависимости
  2. `hermes login` — повторная аутентификация OAuth-провайдеров
  3. Проверьте, что в `.env` указан правильный API-ключ
  4. **Copilot 403**: токены `gh auth login` НЕ работают для Copilot API. Необходимо использовать специальный OAuth-поток с кодом устройства для Copilot через `hermes model` → GitHub Copilot.

### Изменения не вступают в силу[​](<#changes-not-taking-effect> "Прямая ссылка на Изменения не вступают в силу")

  * **Инструменты/навыки:** `/reset` запускает новую сессию с обновлённым набором инструментов
  * **Изменения конфигурации:** В gateway: `/restart`. В CLI: выйти и запустить заново.
  * **Изменения кода:** Перезапустите CLI или процесс gateway

### Навыки не отображаются[​](<#skills-not-showing> "Прямая ссылка на Навыки не отображаются")

  1. `hermes skills list` — проверьте, установлены ли навыки
  2. `hermes skills config` — проверьте включение для платформы
  3. Загрузите явно: `/skill name` или `hermes -s name`

### Проблемы с gateway[​](<#gateway-issues> "Прямая ссылка на Проблемы с gateway")

Сначала проверьте логи:

[code] 
    grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20  
    
[/code]

Распространённые проблемы gateway:
  * **Gateway умирает при выходе из SSH**: включите linger: `sudo loginctl enable-linger $USER`
  * **Gateway умирает при закрытии WSL2**: WSL2 требует `systemd=true` в `/etc/wsl.conf` для работы systemd-сервисов. Без него gateway переключается на `nohup` (умирает при закрытии сессии).
  * **Циклический сбой gateway**: Сбросьте состояние ошибки: `systemctl --user reset-failed hermes-gateway`

### Платформо-специфичные проблемы[​](<#platform-specific-issues> "Прямая ссылка на Платформо-специфичные проблемы")

  * **Discord-бот молчит**: необходимо включить **Message Content Intent** в Bot → Privileged Gateway Intents.
  * **Slack-бот работает только в ЛС**: необходимо подписаться на событие `message.channels`. Без него бот игнорирует публичные каналы.
  * **Windows HTTP 400 "No models provided"**: проблема с кодировкой файла конфигурации (BOM). Убедитесь, что `config.yaml` сохранён в UTF-8 без BOM.

### Вспомогательные модели не работают[​](<#auxiliary-models-not-working> "Прямая ссылка на Вспомогательные модели не работают")

Если вспомогательные задачи (vision, compression, session_search) молча не работают, провайдер `auto` не может найти бэкенд. Установите `OPENROUTER_API_KEY` или `GOOGLE_API_KEY`, либо явно настройте провайдера для каждой вспомогательной задачи:

[code] 
    hermes config set auxiliary.vision.provider <your_provider>  
    hermes config set auxiliary.vision.model <model_name>  
    
[/code]

* * *
## Где что искать[​](<#where-to-find-things> "Прямая ссылка на Где что искать")

| Ищете… | Расположение |
|---|---|
|Опции конфигурации| `hermes config edit` или [документация по конфигурации](<https://hermes-agent.nousresearch.com/docs/user-guide/configuration>)  |
|Доступные инструменты| `hermes tools list` или [справочник инструментов](<https://hermes-agent.nousresearch.com/docs/reference/tools-reference>)  |
|Слэш-команды| `/help` в сессии или [справочник слэш-команд](<https://hermes-agent.nousresearch.com/docs/reference/slash-commands>)  |
|Каталог навыков| `hermes skills browse` или [каталог навыков](<https://hermes-agent.nousresearch.com/docs/reference/skills-catalog>)  |
|Настройка провайдера| `hermes model` или [руководство по провайдерам](<https://hermes-agent.nousresearch.com/docs/integrations/providers>)  |
|Настройка платформ| `hermes gateway setup` или [документация по мессенджерам](<https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>)  |
|MCP-серверы| `hermes mcp list` или [руководство по MCP](<https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp>)  |
|Профили| `hermes profile list` или [документация по профилям](<https://hermes-agent.nousresearch.com/docs/user-guide/profiles>)  |
|Cron-задачи| `hermes cron list` или [документация по cron](<https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>)  |
|Память| `hermes memory status` или [документация по памяти](<https://hermes-agent.nousresearch.com/docs/user-guide/features/memory>)  |
|Переменные окружения| `hermes config env-path` или [справочник переменных окружения](<https://hermes-agent.nousresearch.com/docs/reference/environment-variables>)  |
|CLI-команды| `hermes --help` или [справочник CLI](<https://hermes-agent.nousresearch.com/docs/reference/cli-commands>)  |
|Логи gateway| `~/.hermes/logs/gateway.log`  |
|Файлы сессий| `~/.hermes/sessions/` или `hermes sessions browse`  |
|Исходный код| `~/.hermes/hermes-agent/`  |

* * *
## Краткий справочник контрибьютора[​](<#contributor-quick-reference> "Прямая ссылка на Краткий справочник контрибьютора")

Для эпизодических контрибьюторов и авторов PR. Полная документация для разработчиков: <https://hermes-agent.nousresearch.com/docs/developer-guide/>

### Структура проекта[​](<#project-layout> "Прямая ссылка на Структура проекта")

[code] 
    hermes-agent/  
    ├── run_agent.py          # AIAgent — основной цикл разговора  
    ├── model_tools.py        # Обнаружение и диспетчеризация инструментов  
    ├── toolsets.py           # Определения наборов инструментов  
    ├── cli.py                # Интерактивный CLI (HermesCLI)  
    ├── hermes_state.py       # SQLite-хранилище сессий  
    ├── agent/                # Построитель промптов, сжатие контекста, память, маршрутизация моделей, пулы учётных данных, диспетчеризация навыков  
    ├── hermes_cli/           # Подкоманды CLI, конфигурация, настройка, команды  
    │   ├── commands.py       # Реестр слэш-команд (CommandDef)  
    │   ├── config.py         # DEFAULT_CONFIG, определения переменных окружения  
    │   └── main.py           # Точка входа CLI и argparse  
    ├── tools/                # По одному файлу на инструмент  
    │   └── registry.py       # Центральный реестр инструментов  
    ├── gateway/              # Шлюз для мессенджеров  
    │   └── platforms/        # Адаптеры платформ (telegram, discord и т.д.)  
    ├── cron/                 # Планировщик задач  
    ├── tests/                # ~3000 pytest-тестов  
    └── website/              # Сайт документации Docusaurus  
    
[/code]

Конфигурация: `~/.hermes/config.yaml` (настройки), `~/.hermes/.env` (API-ключи).

### Добавление инструмента (3 файла)[​](<#adding-a-tool-3-files> "Прямая ссылка на Добавление инструмента (3 файла)")

**1. Создайте `tools/your_tool.py`:**

[code] 
    import json, os  
    from tools.registry import registry  
      
    def check_requirements() -> bool:  
        return bool(os.getenv("EXAMPLE_API_KEY"))  
      
    def example_tool(param: str, task_id: str = None) -> str:  
        return json.dumps({"success": True, "data": "..."})  
      
    registry.register(  
        name="example_tool",  
        toolset="example",  
        schema={"name": "example_tool", "description": "...", "parameters": {...}},  
        handler=lambda args, **kw: example_tool(  
            param=args.get("param", ""), task_id=kw.get("task_id")),  
        check_fn=check_requirements,  
        requires_env=["EXAMPLE_API_KEY"],  
    )  
    
[/code]

**2. Добавьте в `toolsets.py`** → список `_HERMES_CORE_TOOLS`.
Автообнаружение: любой файл `tools/*.py` с вызовом `registry.register()` на верхнем уровне импортируется автоматически — ручной список не требуется.
Все обработчики должны возвращать строки JSON. Используйте `get_hermes_home()` для путей, никогда не прописывайте `~/.hermes` жёстко.

### Добавление слэш-команды[​](<#adding-a-slash-command> "Прямая ссылка на Добавление слэш-команды")

  1. Добавьте `CommandDef` в `COMMAND_REGISTRY` в `hermes_cli/commands.py`
  2. Добавьте обработчик в `cli.py` → `process_command()`
  3. (Опционально) Добавьте обработчик gateway в `gateway/run.py`

Все потребители (текст справки, автодополнение, меню Telegram, привязка Slack) автоматически берут данные из центрального реестра.

### Цикл агента (высокоуровнево)[​](<#agent-loop-high-level> "Прямая ссылка на Цикл агента (высокоуровнево)")

[code] 
    run_conversation():  
      1. Собрать системный промпт  
      2. Цикл, пока iterations < max:  
         a. Вызвать LLM (сообщения формата OpenAI + схемы инструментов)  
         b. Если tool_calls → диспетчеризовать каждый через handle_function_call() → добавить результаты → продолжить  
         c. Если текстовый ответ → вернуть  
      3. Сжатие контекста срабатывает автоматически около лимита токенов  
    
[/code]

### Тестирование[​](<#testing> "Прямая ссылка на Тестирование")

[code] 
    python -m pytest tests/ -o 'addopts=' -q   # Полный набор  
    python -m pytest tests/tools/ -q            # Конкретная область  
    
[/code]

  * Тесты автоматически перенаправляют `HERMES_HOME` во временные директории — никогда не трогают реальный `~/.hermes/`
  * Запускайте полный набор перед отправкой любых изменений
  * Используйте `-o 'addopts='` для очистки любых встроенных флагов pytest

### Соглашения о коммитах[​](<#commit-conventions> "Прямая ссылка на Соглашения о коммитах")

[code] 
    type: краткая тема сообщения  
      
    Опциональное тело.  
    
[/code]

Типы: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

### Ключевые правила[​](<#key-rules> "Прямая ссылка на Ключевые правила")

  * **Никогда не ломайте кэширование промптов** — не меняйте контекст, инструменты или системный промпт в середине разговора
  * **Чередование ролей сообщений** — никогда не должно быть двух сообщений ассистента или двух сообщений пользователя подряд
  * Используйте `get_hermes_home()` из `hermes_constants` для всех путей (профиль-безопасно)
  * Значения конфигурации — в `config.yaml`, секреты — в `.env`
  * Новые инструменты должны иметь `check_fn`, чтобы они появлялись только при выполнении требований

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Быстрый старт](<#quick-start>)
  * [Справочник CLI](<#cli-reference>)
    * [Глобальные флаги](<#global-flags>)
    * [Чат](<#chat>)
    * [Конфигурация](<#configuration>)
    * [Инструменты и навыки](<#tools--skills>)
    * [MCP-серверы](<#mcp-servers>)
    * [Gateway (мессенджеры)](<#gateway-messaging-platforms>)
    * [Сессии](<#sessions>)
    * [Cron-задачи](<#cron-jobs>)
    * [Вебхуки](<#webhooks>)
    * [Профили](<#profiles>)
    * [Пулы учётных данных](<#credential-pools>)
    * [Прочее](<#other>)
  * [Слэш-команды (внутри сессии)](<#slash-commands-in-session>)
    * [Управление сессией](<#session-control>)
    * [Конфигурация](<#configuration-1>)
    * [Инструменты и навыки](<#tools--skills-1>)
    * [Gateway](<#gateway>)
    * [Утилиты](<#utility>)
    * [Информация](<#info>)
    * [Выход](<#exit>)
  * [Ключевые пути и конфигурация](<#key-paths--config>)
    * [Секции конфигурации](<#config-sections>)
    * [Провайдеры](<#providers>)
    * [Наборы инструментов](<#toolsets>)
  * [Переключатели безопасности и конфиденциальности](<#security--privacy-toggles>)
    * [Редактирование секретов в выводе инструментов](<#secret-redaction-in-tool-output>)
    * [Редактирование PII в сообщениях gateway](<#pii-redaction-in-gateway-messages>)
    * [Подтверждение команд](<#command-approval-prompts>)
    * [Белый список хуков оболочки](<#shell-hooks-allowlist>)
    * [Отключение инструментов web/browser/image-gen](<#disabling-the-webbrowserimage-gen-tools>)
  * [Голос и транскрипция](<#voice--transcription>)
    * [STT (голос → текст)](<#stt-voice--text>)
    * [TTS (текст → голос)](<#tts-text--voice>)
  * [Порожденение дополнительных экземпляров Hermes](<#spawning-additional-hermes-instances>)
    * [Когда использовать это вместо delegate_task](<#when-to-use-this-vs-delegate_task>)
    * [Одноразовый режим](<#one-shot-mode>)
    * [Интерактивный PTY-режим (через tmux)](<#interactive-pty-mode-via-tmux>)
    * [Мультиагентная координация](<#multi-agent-coordination>)
    * [Возобновление сессии](<#session-resume>)
    * [Советы](<#tips>)
  * [Постоянные и фоновые системы](<#durable--background-systems>)
    * [Делегирование (`delegate_task`)](<#delegation-delegate_task>)
    * [Cron (запланированные задачи)](<#cron-scheduled-jobs>)
    * [Curator (жизненный цикл навыков)](<#curator-skill-lifecycle>)
    * [Kanban (многозадачная очередь работ)](<#kanban-multi-agent-work-queue>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Голос не работает](<#voice-not-working>)
    * [Инструмент недоступен](<#tool-not-available>)
    * [Проблемы с моделью/провайдером](<#modelprovider-issues>)
    * [Изменения не вступают в силу](<#changes-not-taking-effect>)
    * [Навыки не отображаются](<#skills-not-showing>)
    * [Проблемы с gateway](<#gateway-issues>)
    * [Платформо-специфичные проблемы](<#platform-specific-issues>)
    * [Вспомогательные модели не работают](<#auxiliary-models-not-working>)
  * [Где что искать](<#where-to-find-things>)
  * [Краткий справочник контрибьютора](<#contributor-quick-reference>)
    * [Структура проекта](<#project-layout>)
    * [Добавление инструмента (3 файла)](<#adding-a-tool-3-files>)
    * [Добавление слэш-команды](<#adding-a-slash-command>)
    * [Цикл агента (высокоуровнево)](<#agent-loop-high-level>)
    * [Тестирование](<#testing>)
    * [Соглашения о коммитах](<#commit-conventions>)
    * [Ключевые правила](<#key-rules>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent -->
