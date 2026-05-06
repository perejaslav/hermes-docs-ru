На этой странице
`hermes claw migrate` импортирует вашу конфигурацию OpenClaw (или устаревших Clawdbot/Moldbot) в Hermes. Это руководство описывает, что именно переносится, соответствие ключей конфигурации и что нужно проверить после миграции.
## Быстрый старт[​](<#quick-start> "Прямая ссылка на раздел Быстрый старт")
[code]
    # Предпросмотр, затем миграция (всегда показывает предпросмотр, затем запрашивает подтверждение)
    hermes claw migrate

    # Только предпросмотр, без изменений
    hermes claw migrate --dry-run

    # Полная миграция, включая API-ключи, без подтверждения
    hermes claw migrate --preset full --migrate-secrets --yes

[/code]
Миграция всегда показывает полный предпросмотр того, что будет импортировано, перед внесением каких-либо изменений. Просмотрите список, затем подтвердите для продолжения.
По умолчанию читает из `~/.openclaw//`. Устаревшие директории `~/.clawdbot/` или `~/.moltbot/` обнаруживаются автоматически. То же самое касается устаревших имён файлов конфигурации (`clawdbot.json`, `moltbot.json`).
## Параметры[​](<#options> "Прямая ссылка на раздел Параметры")
| Параметр | Описание |
|---|---|
| `--dry-run` | Только предпросмотр — остановиться после отображения того, что будет перенесено. |
| `--preset <имя>` | `full` (все совместимые настройки) или `user-data` (исключает инфраструктурную конфигурацию). Ни один пресет не импортирует секреты по умолчанию — явно укажите `--migrate-secrets`. |
| `--overwrite` | Перезаписывать существующие файлы Hermes при конфликтах (по умолчанию: отказ от применения, когда в плане есть конфликты). |
| `--migrate-secrets` | Включает API-ключи. Требуется даже при `--preset full` — ни один пресет не импортирует секреты молча. |
| `--no-backup` | Пропустить создание zip-снимка `~/.hermes/` перед миграцией (по умолчанию перед применением записывается один архив точки восстановления в `~/.hermes/backups/pre-migration-*.zip`; можно восстановить с помощью `hermes import`). |
| `--source <путь>` | Пользовательская директория OpenClaw. |
| `--workspace-target <путь>` | Куда поместить `AGENTS.md`. |
| `--skill-conflict <режим>` | `skip` (по умолчанию), `overwrite` или `rename`. |
| `--yes` | Пропустить запрос подтверждения после предпросмотра. |
## Что переносится[​](<#what-gets-migrated> "Прямая ссылка на раздел Что переносится")
### Личность, память и инструкции[​](<#persona-memory-and-instructions> "Прямая ссылка на раздел Личность, память и инструкции")
| Что | Источник OpenClaw | Назначение Hermes | Примечания |
|---|---|---|---|
| Личность | `workspace/SOUL.md` | `~/.hermes/SOUL.md` | Прямое копирование |
| Инструкции рабочего пространства | `workspace/AGENTS.md` | `AGENTS.md` в `--workspace-target` | Требуется флаг `--workspace-target` |
| Долговременная память | `workspace/MEMORY.md` | `~/.hermes/memories/MEMORY.md` | Разбирается на записи, объединяется с существующими, дедуплицируется. Использует разделитель `§`. |
| Профиль пользователя | `workspace/USER.md` | `~/.hermes/memories/USER.md` | Та же логика объединения записей, что и для памяти. |
| Ежедневные файлы памяти | `workspace/memory/*.md` | `~/.hermes/memories/MEMORY.md` | Все ежедневные файлы объединяются в основную память. |
Файлы рабочего пространства также проверяются в `workspace.default/` и `workspace-main/` как запасные пути (OpenClaw переименовал `workspace/` в `workspace-main/` в последних версиях и использует `workspace-{agentId}` для многопользовательских конфигураций).
### Навыки (4 источника)[​](<#skills-4-sources> "Прямая ссылка на раздел Навыки (4 источника)")
| Источник | Расположение OpenClaw | Назначение Hermes |
|---|---|---|
| Навыки рабочего пространства | `workspace/skills/` | `~/.hermes/skills/openclaw-imports/` |
| Управляемые/общие навыки | `~/.openclaw/skills/` | `~/.hermes/skills/openclaw-imports/` |
| Личные межпроектные | `~/.agents/skills/` | `~/.hermes/skills/openclaw-imports/` |
| Общие на уровне проекта | `workspace/.agents/skills/` | `~/.hermes/skills/openclaw-imports/` |
Конфликты навыков обрабатываются с помощью `--skill-conflict`: `skip` оставляет существующий навык Hermes, `overwrite` заменяет его, `rename` создаёт копию с суффиксом `-imported`.
### Конфигурация модели и провайдера[​](<#model-and-provider-configuration> "Прямая ссылка на раздел Конфигурация модели и провайдера")
| Что | Путь конфигурации OpenClaw | Назначение Hermes | Примечания |
|---|---|---|---|
| Модель по умолчанию | `agents.defaults.model` | `config.yaml` → `model` | Может быть строкой или объектом `{primary, fallbacks}` |
| Пользовательские провайдеры | `models.providers.*` | `config.yaml` → `custom_providers` | Преобразует `baseUrl`, `apiType`/`api` — обрабатывает как краткие («openai», «anthropic»), так и составные («openai-completions», «anthropic-messages», «google-generative-ai») значения |
| API-ключи провайдеров | `models.providers.*.apiKey` | `~/.hermes/.env` | Требуется `--migrate-secrets`. См. [Разрешение API-ключей](<#api-key-resolution>) ниже. |
### Поведение агента[​](<#agent-behavior> "Прямая ссылка на раздел Поведение агента")
| Что | Путь конфигурации OpenClaw | Путь конфигурации Hermes | Преобразование |
|---|---|---|---|
| Макс. шагов | `agents.defaults.timeoutSeconds` | `agent.max_turns` | `timeoutSeconds / 10`, максимум 200 |
| Подробный режим | `agents.defaults.verboseDefault` | `agent.verbose` | «off» / «on» / «full» |
| Уровень рассуждений | `agents.defaults.thinkingDefault` | `agent.reasoning_effort` | «always»/«high»/«xhigh» → «high», «auto»/«medium»/«adaptive» → «medium», «off»/«low»/«none»/«minimal» → «low» |
| Сжатие | `agents.defaults.compaction.mode` | `compression.enabled` | «off» → false, всё остальное → true |
| Модель сжатия | `agents.defaults.compaction.model` | `compression.summary_model` | Прямое копирование строки |
| Задержка человека | `agents.defaults.humanDelay.mode` | `human_delay.mode` | «natural» / «custom» / «off» |
| Время задержки человека | `agents.defaults.humanDelay.minMs` / `.maxMs` | `human_delay.min_ms` / `.max_ms` | Прямое копирование |
| Часовой пояс | `agents.defaults.userTimezone` | `timezone` | Прямое копирование строки |
| Таймаут выполнения | `tools.exec.timeoutSec` | `terminal.timeout` | Прямое копирование (поле — `timeoutSec`, не `timeout`) |
| Docker-песочница | `agents.defaults.sandbox.backend` | `terminal.backend` | «docker» → «docker» |
| Docker-образ | `agents.defaults.sandbox.docker.image` | `terminal.docker_image` | Прямое копирование |
### Политики сброса сессий[​](<#session-reset-policies> "Прямая ссылка на раздел Политики сброса сессий")
| Путь конфигурации OpenClaw | Путь конфигурации Hermes | Примечания |
|---|---|---|
| `session.reset.mode` | `session_reset.mode` | «daily», «idle» или оба |
| `session.reset.atHour` | `session_reset.at_hour` | Час (0–23) для ежедневного сброса |
| `session.reset.idleMinutes` | `session_reset.idle_minutes` | Минуты бездействия |
Примечание: OpenClaw также имеет `session.resetTriggers` (простой массив строк, например `["daily", "idle"]`). Если структурированный `session.reset` отсутствует, миграция выводит настройки из `resetTriggers`.
### MCP-серверы[​](<#mcp-servers> "Прямая ссылка на раздел MCP-серверы")
| Поле OpenClaw | Поле Hermes | Примечания |
|---|---|---|
| `mcp.servers.*.command` | `mcp_servers.*.command` | Stdio-транспорт |
| `mcp.servers.*.args` | `mcp_servers.*.args` | |
| `mcp.servers.*.env` | `mcp_servers.*.env` | |
| `mcp.servers.*.cwd` | `mcp_servers.*.cwd` | |
| `mcp.servers.*.url` | `mcp_servers.*.url` | HTTP/SSE-транспорт |
| `mcp.servers.*.tools.include` | `mcp_servers.*.tools.include` | Фильтрация инструментов |
| `mcp.servers.*.tools.exclude` | `mcp_servers.*.tools.exclude` | |
### TTS (текст-в-речь)[​](<#tts-text-to-speech> "Прямая ссылка на раздел TTS (текст-в-речь)")
Настройки TTS читаются из **двух** расположений в конфигурации OpenClaw со следующим приоритетом:
  1. `messages.tts.providers.{provider}.*` (каноническое расположение)
  2. `talk.providers.{provider}.*` на верхнем уровне (запасной вариант)
  3. Устаревшие плоские ключи `messages.tts.{provider}.*` (старейший формат)

| Что | Назначение Hermes |
|---|---|
| Имя провайдера | `config.yaml` → `tts.provider` |
| ID голоса ElevenLabs | `config.yaml` → `tts.elevenlabs.voice_id` |
| ID модели ElevenLabs | `config.yaml` → `tts.elevenlabs.model_id` |
| Модель OpenAI | `config.yaml` → `tts.openai.model` |
| Голос OpenAI | `config.yaml` → `tts.openai.voice` |
| Голос Edge TTS | `config.yaml` → `tts.edge.voice` (OpenClaw переименовал «edge» в «microsoft» — оба распознаются) |
| TTS-ресурсы | `~/.hermes/tts/` (копирование файлов) |
### Платформы обмена сообщениями[​](<#messaging-platforms> "Прямая ссылка на раздел Платформы обмена сообщениями")
| Платформа | Путь конфигурации OpenClaw | Переменная `.env` в Hermes | Примечания |
|---|---|---|---|
| Telegram | `channels.telegram.botToken` или `.accounts.default.botToken` | `TELEGRAM_BOT_TOKEN` | Токен может быть строкой или [SecretRef](<#secretref-handling>). Поддерживаются как плоская, так и многопрофильная структуры. |
| Telegram | `credentials/telegram-default-allowFrom.json` | `TELEGRAM_ALLOWED_USERS` | Объединение через запятую из массива `allowFrom[]` |
| Discord | `channels.discord.token` или `.accounts.default.token` | `DISCORD_BOT_TOKEN` | |
| Discord | `channels.discord.allowFrom` или `.accounts.default.allowFrom` | `DISCORD_ALLOWED_USERS` | |
| Slack | `channels.slack.botToken` или `.accounts.default.botToken` | `SLACK_BOT_TOKEN` | |
| Slack | `channels.slack.appToken` или `.accounts.default.appToken` | `SLACK_APP_TOKEN` | |
| Slack | `channels.slack.allowFrom` или `.accounts.default.allowFrom` | `SLACK_ALLOWED_USERS` | |
| WhatsApp | `channels.whatsapp.allowFrom` или `.accounts.default.allowFrom` | `WHATSAPP_ALLOWED_USERS` | Аутентификация через QR-связывание Baileys — требуется повторное связывание после миграции |
| Signal | `channels.signal.account` или `.accounts.default.account` | `SIGNAL_ACCOUNT` | |
| Signal | `channels.signal.httpUrl` или `.accounts.default.httpUrl` | `SIGNAL_HTTP_URL` | |
| Signal | `channels.signal.allowFrom` или `.accounts.default.allowFrom` | `SIGNAL_ALLOWED_USERS` | |
| Matrix | `channels.matrix.accessToken` или `.accounts.default.accessToken` | `MATRIX_ACCESS_TOKEN` | Использует `accessToken` (не `botToken`) |
| Mattermost | `channels.mattermost.botToken` или `.accounts.default.botToken` | `MATTERMOST_BOT_TOKEN` | |
### Прочие настройки[​](<#other-config> "Прямая ссылка на раздел Прочие настройки")
| Что | Путь OpenClaw | Путь Hermes | Примечания |
|---|---|---|---|
| Режим подтверждения | `approvals.exec.mode` | `config.yaml` → `approvals.mode` | «auto»→«off», «always»→«manual», «smart»→«smart» |
| Белый список команд | `exec-approvals.json` | `config.yaml` → `command_allowlist` | Шаблоны объединяются и дедуплицируются |
| URL браузера CDP | `browser.cdpUrl` | `config.yaml` → `browser.cdp_url` | |
| Безголовый браузер | `browser.headless` | `config.yaml` → `browser.headless` | |
| Ключ поиска Brave | `tools.web.search.brave.apiKey` | `.env` → `BRAVE_API_KEY` | Требуется `--migrate-secrets` |
| Токен аутентификации шлюза | `gateway.auth.token` | `.env` → `HERMES_GATEWAY_TOKEN` | Требуется `--migrate-secrets` |
| Рабочая директория | `agents.defaults.workspace` | `.env` → `MESSAGING_CWD` | |
### В архиве (нет прямого аналога в Hermes)[​](<#archived-no-direct-hermes-equivalent> "Прямая ссылка на раздел В архиве (нет прямого аналога в Hermes)")
Они сохраняются в `~/.hermes/migration/openclaw/<timestamp>/archive/` для ручного просмотра:
| Что | Файл архива | Как воссоздать в Hermes |
|---|---|---|
| `IDENTITY.md` | `archive/workspace/IDENTITY.md` | Объединить в `SOUL.md` |
| `TOOLS.md` | `archive/workspace/TOOLS.md` | У Hermes есть встроенные инструкции по инструментам |
| `HEARTBEAT.md` | `archive/workspace/HEARTBEAT.md` | Используйте cron-задачи для периодических заданий |
| `BOOTSTRAP.md` | `archive/workspace/BOOTSTRAP.md` | Используйте контекстные файлы или навыки |
| Cron-задачи | `archive/cron-config.json` | Воссоздать с помощью `hermes cron create` |
| Плагины | `archive/plugins-config.json` | См. [руководство по плагинам](</docs/user-guide/features/hooks>) |
| Хуки/вебхуки | `archive/hooks-config.json` | Используйте `hermes webhook` или хуки шлюза |
| Бэкенд памяти | `archive/memory-backend-config.json` | Настройте через `hermes honcho` |
| Реестр навыков | `archive/skills-registry-config.json` | Используйте `hermes skills config` |
| UI/идентификация | `archive/ui-identity-config.json` | Используйте команду `/skin` |
| Логирование | `archive/logging-diagnostics-config.json` | Установите в разделе logging в `config.yaml` |
| Список мультиагентов | `archive/agents-list.json` | Используйте профили Hermes |
| Привязки каналов | `archive/bindings.json` | Ручная настройка для каждой платформы |
| Сложные каналы | `archive/channels-deep-config.json` | Ручная настройка платформы |
## Разрешение API-ключей[​](<#api-key-resolution> "Прямая ссылка на раздел Разрешение API-ключей")
Когда `--migrate-secrets` включён, API-ключи собираются из **четырёх источников** в порядке приоритета:
  1. **Значения конфигурации** — `models.providers.*.apiKey` и ключи TTS-провайдеров в `openclaw.json`
  2. **Файл окружения** — `~/.openclaw/.env` (ключи вида `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY` и т.д.)
  3. **Подобъект env конфигурации** — `openclaw.json` → `"env"` или `"env"."vars"` (некоторые конфигурации хранят ключи здесь вместо отдельного файла `.env`)
  4. **Профили аутентификации** — `~/.openclaw/agents/main/agent/auth-profiles.json` (учётные данные для каждого агента)

Значения конфигурации имеют приоритет. Каждый последующий источник заполняет оставшиеся пробелы.
### Поддерживаемые целевые ключи[​](<#supported-key-targets> "Прямая ссылка на раздел Поддерживаемые целевые ключи")
`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `ZAI_API_KEY`, `MINIMAX_API_KEY`, `ELEVENLABS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `VOICE_TOOLS_OPENAI_KEY`
Ключи, отсутствующие в этом белом списке, никогда не копируются.
## Обработка SecretRef[​](<#secretref-handling> "Прямая ссылка на раздел Обработка SecretRef")
Значения конфигурации OpenClaw для токенов и API-ключей могут быть в трёх форматах:
[code]
    // Простая строка
    "channels": { "telegram": { "botToken": "123456:ABC-DEF..." } }

    // Шаблон окружения
    "channels": { "telegram": { "botToken": "${TELEGRAM_BOT_TOKEN}" } }

    // Объект SecretRef
    "channels": { "telegram": { "botToken": { "source": "env", "id": "TELEGRAM_BOT_TOKEN" } } }

[/code]
Миграция разрешает все три формата. Для шаблонов окружения и объектов SecretRef с `source: "env"` значение ищется в `~/.openclaw/.env` и в под-объекте env конфигурации `openclaw.json`. Объекты SecretRef с `source: "file"` или `source: "exec"` не могут быть разрешены автоматически — миграция предупреждает о них, и эти значения необходимо добавить в Hermes вручную через `hermes config set`.
## После миграции[​](<#after-migration> "Прямая ссылка на раздел После миграции")
  1. **Проверьте отчёт о миграции** — выводится по завершении с количеством перенесённых, пропущенных и конфликтующих элементов.
  2. **Просмотрите архивированные файлы** — всё в `~/.hermes/migration/openclaw/<timestamp>/archive/` требует ручного внимания.
  3. **Начните новую сессию** — импортированные навыки и записи памяти вступают в силу в новых сессиях, а не в текущей.
  4. **Проверьте API-ключи** — запустите `hermes status` для проверки аутентификации провайдеров.
  5. **Протестируйте обмен сообщениями** — если вы перенесли токены платформ, перезапустите шлюз: `systemctl --user restart hermes-gateway`
  6. **Проверьте политики сессий** — убедитесь, что `hermes config get session_reset` соответствует вашим ожиданиям.
  7. **Повторно свяжите WhatsApp** — WhatsApp использует QR-связывание (Baileys), а не перенос токенов. Запустите `hermes whatsapp` для связывания.
  8. **Очистка архива** — после подтверждения, что всё работает, запустите `hermes claw cleanup`, чтобы переименовать оставшиеся директории OpenClaw в `.pre-migration/` (предотвращает путаницу состояний).


## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на раздел Устранение неполадок")
### «Директория OpenClaw не найдена»[​](<#openclaw-directory-not-found> "Прямая ссылка на раздел «Директория OpenClaw не найдена»")
Миграция проверяет `~/.openclaw/`, затем `~/.clawdbot/`, затем `~/.moltbot/`. Если ваша установка находится в другом месте, используйте `--source /путь/к/вашему/openclaw`.
### «Не найдены API-ключи провайдеров»[​](<#no-provider-api-keys-found> "Прямая ссылка на раздел «Не найдены API-ключи провайдеров»")
Ключи могут храниться в нескольких местах в зависимости от версии OpenClaw: встроенные в `openclaw.json` в `models.providers.*.apiKey`, в `~/.openclaw/.env`, в под-объекте `"env"` в `openclaw.json` или в `agents/main/agent/auth-profiles.json`. Миграция проверяет все четыре. Если ключи используют SecretRef с `source: "file"` или `source: "exec"`, они не могут быть разрешены автоматически — добавьте их через `hermes config set`.
### Навыки не отображаются после миграции[​](<#skills-not-appearing-after-migration> "Прямая ссылка на раздел Навыки не отображаются после миграции")
Импортированные навыки попадают в `~/.hermes/skills/openclaw-imports/`. Начните новую сессию, чтобы они вступили в силу, или выполните `/skills` для проверки их загрузки.
### TTS-голос не перенесён[​](<#tts-voice-not-migrated> "Прямая ссылка на раздел TTS-голос не перенесён")
OpenClaw хранит настройки TTS в двух местах: `messages.tts.providers.*` и конфигурация `talk` на верхнем уровне. Миграция проверяет оба. Если ваш ID голоса был установлен через UI OpenClaw (хранится в другом пути), вам может потребоваться установить его вручную: `hermes config set tts.elevenlabs.voice_id YOUR_VOICE_ID`.
  * [Быстрый старт](<#quick-start>)
  * [Параметры](<#options>)
  * [Что переносится](<#what-gets-migrated>)
    * [Личность, память и инструкции](<#persona-memory-and-instructions>)
    * [Навыки (4 источника)](<#skills-4-sources>)
    * [Конфигурация модели и провайдера](<#model-and-provider-configuration>)
    * [Поведение агента](<#agent-behavior>)
    * [Политики сброса сессий](<#session-reset-policies>)
    * [MCP-серверы](<#mcp-servers>)
    * [TTS (текст-в-речь)](<#tts-text-to-speech>)
    * [Платформы обмена сообщениями](<#messaging-platforms>)
    * [Прочие настройки](<#other-config>)
    * [В архиве (нет прямого аналога в Hermes)](<#archived-no-direct-hermes-equivalent>)
  * [Разрешение API-ключей](<#api-key-resolution>)
    * [Поддерживаемые целевые ключи](<#supported-key-targets>)
  * [Обработка SecretRef](<#secretref-handling>)
  * [После миграции](<#after-migration>)
  * [Устранение неполадок](<#troubleshooting>)
    * [«Директория OpenClaw не найдена»](<#openclaw-directory-not-found>)
    * [«Не найдены API-ключи провайдеров»](<#no-provider-api-keys-found>)
    * [Навыки не отображаются после миграции](<#skills-not-appearing-after-migration>)
    * [TTS-голос не перенесён](<#tts-voice-not-migrated>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw -->
