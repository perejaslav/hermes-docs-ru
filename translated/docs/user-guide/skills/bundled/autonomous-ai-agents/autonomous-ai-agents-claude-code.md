On this page
Делегирование задач по кодингу Claude Code CLI (фичи, PR).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/autonomous-ai-agents/claude-code` |
|Version| `2.2.0` |
|Author| Hermes Agent + Teknium |
|License| MIT |
|Tags| `Coding-Agent`, `Claude`, `Anthropic`, `Code-Review`, `Refactoring`, `PTY`, `Automation` |
|Related skills| [`codex`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>), [`hermes-agent`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent>), [`opencode`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode>) |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Claude Code — Hermes Orchestration Guide
Делегируй задачи по кодингу [Claude Code](<https://code.claude.com/docs/en/cli-reference>) (автономный агент-кодировщик Anthropic в виде CLI) через терминал Hermes. Claude Code v2.x может читать файлы, писать код, запускать shell-команды, порождать сабагентов и автономно управлять git-рабочими процессами.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **Установка:** `npm install -g @anthropic-ai/claude-code`
  * **Аутентификация:** запусти `claude` один раз для входа (браузерный OAuth для Pro/Max, или установи `ANTHROPIC_API_KEY`)
  * **Консольная аутентификация:** `claude auth login --console` для биллинга по API-ключу
  * **SSO-аутентификация:** `claude auth login --sso` для Enterprise
  * **Проверка статуса:** `claude auth status` (JSON) или `claude auth status --text` (человекочитаемый)
  * **Проверка здоровья:** `claude doctor` — проверяет автообновление и здоровье установки
  * **Проверка версии:** `claude --version` (требуется v2.x+)
  * **Обновление:** `claude update` или `claude upgrade`


## Two Orchestration Modes[​](<#two-orchestration-modes> "Direct link to Two Orchestration Modes")
Hermes взаимодействует с Claude Code двумя принципиально разными способами. Выбирай в зависимости от задачи.
### Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED for most tasks)[​](<#mode-1-print-mode--p--non-interactive-preferred-for-most-tasks> "Direct link to mode-1-print-mode--p--non-interactive-preferred-for-most-tasks")
Print Mode выполняет одноразовую задачу, возвращает результат и завершается. PTY не нужен. Никаких интерактивных подсказок. Это самый чистый путь интеграции.
[code] 
    terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)  
    
[/code]
**Когда использовать print mode:**
  * Одноразовые задачи по кодингу (исправить баг, добавить функционал, рефакторинг)
  * Автоматизация CI/CD и скрипты
  * Структурированное извлечение данных с `--json-schema`
  * Обработка конвейерного ввода (`cat file | claude -p "analyze this"`)
  * Любая задача, где не нужен многошаговый диалог


**Print mode пропускает ВСЕ интерактивные диалоги** — никакого запроса доверия к рабочей области, никаких подтверждений разрешений. Это делает его идеальным для автоматизации.
### Mode 2: Interactive PTY via tmux — Multi-Turn Sessions[​](<#mode-2-interactive-pty-via-tmux--multi-turn-sessions> "Direct link to Mode 2: Interactive PTY via tmux — Multi-Turn Sessions")
Интерактивный режим даёт полноценный диалоговый REPL, где можно отправлять дополнительные запросы, использовать слеш-команды и наблюдать за работой Claude в реальном времени. **Требует оркестрации через tmux.**
[code] 
    # Запустить tmux-сессию  
    terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")  
      
    # Запустить Claude Code внутри неё  
    terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")  
      
    # Подождать запуска, затем отправить задачу  
    # (через ~3-5 секунд для экрана приветствия)  
    terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor the auth module to use JWT tokens' Enter")  
      
    # Мониторить прогресс, захватывая панель  
    terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")  
      
    # Отправить дополнительные задачи  
    terminal(command="tmux send-keys -t claude-work 'Now add unit tests for the new JWT code' Enter")  
      
    # Выйти по завершении  
    terminal(command="tmux send-keys -t claude-work '/exit' Enter")  
    
[/code]
**Когда использовать интерактивный режим:**
  * Многошаговая итеративная работа (рефакторинг → ревью → исправление → тестирование)
  * Задачи, требующие решений человека в цикле
  * Исследовательские сессии кодинга
  * Когда нужно использовать слеш-команды Claude (`/compact`, `/review`, `/model`)


## PTY Dialog Handling (CRITICAL for Interactive Mode)[​](<#pty-dialog-handling-critical-for-interactive-mode> "Direct link to PTY Dialog Handling \(CRITICAL for Interactive Mode\)")
Claude Code показывает до двух диалогов подтверждения при первом запуске. Ты ОБЯЗАН обработать их через tmux send-keys:
### Dialog 1: Workspace Trust (first visit to a directory)[​](<#dialog-1-workspace-trust-first-visit-to-a-directory> "Direct link to Dialog 1: Workspace Trust \(first visit to a directory\)")
[code] 
    ❯ 1. Yes, I trust this folder    ← ПО УМОЛЧАНИЮ (просто нажми Enter)  
      2. No, exit  
    
[/code]
**Обработка:** `tmux send-keys -t <session> Enter` — выбор по умолчанию правильный.
### Dialog 2: Bypass Permissions Warning (only with --dangerously-skip-permissions)[​](<#dialog-2-bypass-permissions-warning-only-with---dangerously-skip-permissions> "Direct link to Dialog 2: Bypass Permissions Warning \(only with --dangerously-skip-permissions\)")
[code] 
    ❯ 1. No, exit                    ← ПО УМОЛЧАНИЮ (НЕПРАВИЛЬНЫЙ выбор!)  
      2. Yes, I accept  
    
[/code]
**Обработка:** Сначала нужно перейти вниз, затем Enter:
[code] 
    tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter  
    
[/code]
### Robust Dialog Handling Pattern[​](<#robust-dialog-handling-pattern> "Direct link to Robust Dialog Handling Pattern")
[code] 
    # Запустить с обходом разрешений  
    terminal(command="tmux send-keys -t claude-work 'claude --dangerously-skip-permissions \\\"your task\\\"' Enter")  
      
    # Обработать диалог доверия (Enter для выбора "Yes" по умолчанию)  
    terminal(command="sleep 4 && tmux send-keys -t claude-work Enter")  
      
    # Обработать диалог разрешений (Down затем Enter для "Yes, I accept")  
    terminal(command="sleep 3 && tmux send-keys -t claude-work Down && sleep 0.3 && tmux send-keys -t claude-work Enter")  
      
    # Теперь подождать, пока Claude работает  
    terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -60")  
    
[/code]
**Примечание:** После первого принятия доверия для директории этот диалог больше не появится. Только диалог разрешений повторяется каждый раз при использовании `--dangerously-skip-permissions`.
## CLI Subcommands[​](<#cli-subcommands> "Direct link to CLI Subcommands")
Subcommand| Purpose  
---|---  
`claude`| Запустить интерактивный REPL  
`claude "query"`| Запустить REPL с начальным запросом  
`claude -p "query"`| Print mode (неинтерактивный, завершается по готовности)  
`cat file | claude -p "query"`| Передать содержимое как контекст stdin  
`claude -c`| Продолжить последний разговор в этой директории  
`claude -r "id"`| Возобновить конкретную сессию по ID или имени  
`claude auth login`| Войти (добавь `--console` для биллинга API, `--sso` для Enterprise)  
`claude auth status`| Проверить статус входа (возвращает JSON; `--text` для человекочитаемого)  
`claude mcp add <name> -- <cmd>`| Добавить MCP-сервер  
`claude mcp list`| Список настроенных MCP-серверов  
`claude mcp remove <name>`| Удалить MCP-сервер  
`claude agents`| Список настроенных агентов  
`claude doctor`| Запустить проверки здоровья установки и автообновления  
`claude update` / `claude upgrade`| Обновить Claude Code до последней версии  
`claude remote-control`| Запустить сервер для управления Claude с claude.ai или мобильного приложения  
`claude install [target]`| Установить нативную сборку (stable, latest или конкретную версию)  
`claude setup-token`| Настроить долгоживущий токен аутентификации (требуется подписка)  
`claude plugin` / `claude plugins`| Управление плагинами Claude Code  
`claude auto-mode`| Просмотр конфигурации классификатора auto-mode  
## Print Mode Deep Dive[​](<#print-mode-deep-dive> "Direct link to Print Mode Deep Dive")
### Structured JSON Output[​](<#structured-json-output> "Direct link to Structured JSON Output")
[code] 
    terminal(command="claude -p 'Analyze auth.py for security issues' --output-format json --max-turns 5", workdir="/project", timeout=120)  
    
[/code]
Возвращает JSON-объект с:
[code] 
    {  
      "type": "result",  
      "subtype": "success",  
      "result": "The analysis text...",  
      "session_id": "75e2167f-...",  
      "num_turns": 3,  
      "total_cost_usd": 0.0787,  
      "duration_ms": 10276,  
      "stop_reason": "end_turn",  
      "terminal_reason": "completed",  
      "usage": { "input_tokens": 5, "output_tokens": 603, ... },  
      "modelUsage": { "claude-sonnet-4-6": { "costUSD": 0.078, "contextWindow": 200000 } }  
    }  
    
[/code]
**Ключевые поля:** `session_id` для возобновления, `num_turns` для подсчёта циклов агента, `total_cost_usd` для отслеживания расходов, `subtype` для обнаружения успеха/ошибки (`success`, `error_max_turns`, `error_budget`).
### Streaming JSON Output[​](<#streaming-json-output> "Direct link to Streaming JSON Output")
Для потоковой передачи токенов в реальном времени используй `stream-json` с `--verbose`:
[code] 
    terminal(command="claude -p 'Write a summary' --output-format stream-json --verbose --include-partial-messages", timeout=60)  
    
[/code]
Возвращает события JSON, разделённые новой строкой. Фильтруй с помощью jq для живого текста:
[code] 
    claude -p "Explain X" --output-format stream-json --verbose --include-partial-messages | \  
      jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'  
    
[/code]
Stream-события включают `system/api_retry` с полями `attempt`, `max_retries` и `error` (например, `rate_limit`, `billing_error`).
### Bidirectional Streaming[​](<#bidirectional-streaming> "Direct link to Bidirectional Streaming")
Для потоковой передачи ввода И вывода в реальном времени:
[code] 
    claude -p "task" --input-format stream-json --output-format stream-json --replay-user-messages  
    
[/code]
`--replay-user-messages` повторно отправляет сообщения пользователя в stdout для подтверждения.
### Piped Input[​](<#piped-input> "Direct link to Piped Input")
[code] 
    # Передать файл для анализа  
    terminal(command="cat src/auth.py | claude -p 'Review this code for bugs' --max-turns 1", timeout=60)  
      
    # Передать несколько файлов  
    terminal(command="cat src/*.py | claude -p 'Find all TODO comments' --max-turns 1", timeout=60)  
      
    # Передать вывод команды  
    terminal(command="git diff HEAD~3 | claude -p 'Summarize these changes' --max-turns 1", timeout=60)  
    
[/code]
### JSON Schema for Structured Extraction[​](<#json-schema-for-structured-extraction> "Direct link to JSON Schema for Structured Extraction")
[code] 
    terminal(command="claude -p 'List all functions in src/' --output-format json --json-schema '{\"type\":\"object\",\"properties\":{\"functions\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}}},\"required\":[\"functions\"]}' --max-turns 5", workdir="/project", timeout=90)  
    
[/code]
Извлеки `structured_output` из JSON-результата. Claude проверяет вывод на соответствие схеме перед возвратом.
### Session Continuation[​](<#session-continuation> "Direct link to Session Continuation")
[code] 
    # Начать задачу  
    terminal(command="claude -p 'Start refactoring the database layer' --output-format json --max-turns 10 > /tmp/session.json", workdir="/project", timeout=180)  
      
    # Возобновить по ID сессии  
    terminal(command="claude -p 'Continue and add connection pooling' --resume $(cat /tmp/session.json | python3 -c 'import json,sys; print(json.load(sys.stdin)[\"session_id\"])') --max-turns 5", workdir="/project", timeout=120)  
      
    # Или возобновить самую последнюю сессию в той же директории  
    terminal(command="claude -p 'What did you do last time?' --continue --max-turns 1", workdir="/project", timeout=30)  
      
    # Форкнуть сессию (новый ID, сохраняет историю)  
    terminal(command="claude -p 'Try a different approach' --resume <id> --fork-session --max-turns 10", workdir="/project", timeout=120)  
    
[/code]
### Bare Mode for CI/Scripting[​](<#bare-mode-for-ciscripting> "Direct link to Bare Mode for CI/Scripting")
[code] 
    terminal(command="claude --bare -p 'Run all tests and report failures' --allowedTools 'Read,Bash' --max-turns 10", workdir="/project", timeout=180)  
    
[/code]
`--bare` пропускает хуки, плагины, обнаружение MCP и загрузку CLAUDE.md. Самый быстрый запуск. Требует `ANTHROPIC_API_KEY` (пропускает OAuth).
Чтобы выборочно загрузить контекст в bare mode:
Для загрузки| Флаг  
---|---  
Дополнения к system prompt| `--append-system-prompt "text"` или `--append-system-prompt-file path`  
Настройки| `--settings <file-or-json>`  
MCP-серверы| `--mcp-config <file-or-json>`  
Пользовательские агенты| `--agents '<json>'`  
### Fallback Model for Overload[​](<#fallback-model-for-overload> "Direct link to Fallback Model for Overload")
[code] 
    terminal(command="claude -p 'task' --fallback-model haiku --max-turns 5", timeout=90)  
    
[/code]
Автоматически переключается на указанную модель, когда модель по умолчанию перегружена (только print mode).
## Complete CLI Flags Reference[​](<#complete-cli-flags-reference> "Direct link to Complete CLI Flags Reference")
### Session & Environment[​](<#session--environment> "Direct link to Session & Environment")
Flag| Effect  
---|---  
`-p, --print`| Неинтерактивный одноразовый режим (завершается по готовности)  
`-c, --continue`| Возобновить последний разговор в текущей директории  
`-r, --resume <id>`| Возобновить конкретную сессию по ID или имени (интерактивный выбор, если ID не указан)  
`--fork-session`| При возобновлении создать новый ID сессии вместо повторного использования оригинального  
`--session-id <uuid>`| Использовать конкретный UUID для разговора  
`--no-session-persistence`| Не сохранять сессию на диск (только print mode)  
`--add-dir <paths...>`| Предоставить Claude доступ к дополнительным рабочим директориям  
`-w, --worktree [name]`| Запустить в изолированном git worktree в `.claude/worktrees/<name>`  
`--tmux`| Создать tmux-сессию для worktree (требует `--worktree`)  
`--ide`| Автоподключение к действующей IDE при запуске  
`--chrome` / `--no-chrome`| Включить/отключить интеграцию с браузером Chrome для веб-тестирования  
`--from-pr [number]`| Возобновить сессию, привязанную к конкретному GitHub PR  
`--file <specs...>`| Файловые ресурсы для загрузки при запуске (формат: `file_id:relative_path`)  
### Model & Performance[​](<#model--performance> "Direct link to Model & Performance")
Flag| Effect  
---|---  
`--model <alias>`| Выбор модели: `sonnet`, `opus`, `haiku` или полное имя вроде `claude-sonnet-4-6`  
`--effort <level>`| Глубина рассуждения: `low`, `medium`, `high`, `max`, `auto`  
`--max-turns <n>`| Лимит циклов агента (только print mode; предотвращает бесконечные циклы)  
`--max-budget-usd <n>`| Лимит расходов API в долларах (только print mode)  
`--fallback-model <model>`| Автопереключение при перегрузке модели по умолчанию (только print mode)  
`--betas <betas...>`| Beta-заголовки для включения в API-запросы (только для пользователей API-ключа)  
### Permission & Safety[​](<#permission--safety> "Direct link to Permission & Safety")
Flag| Effect  
---|---  
`--dangerously-skip-permissions`| Автоодобрение ВСЕХ инструментов (запись файлов, bash, сеть и т.д.)  
`--allow-dangerously-skip-permissions`| Включить обход как _опцию_, не включая её по умолчанию  
`--permission-mode <mode>`| `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`  
`--allowedTools <tools...>`| Белый список конкретных инструментов (через запятую или пробел)  
`--disallowedTools <tools...>`| Чёрный список инструментов  
`--tools <tools...>`| Переопределить встроенный набор инструментов (`""` = нет, `"default"` = все, или имена)  
### Output & Input Format[​](<#output--input-format> "Direct link to Output & Input Format")
Flag| Effect  
---|---  
`--output-format <fmt>`| `text` (по умолчанию), `json` (один объект результата), `stream-json` (с разделением строками)  
`--input-format <fmt>`| `text` (по умолчанию) или `stream-json` (потоковый ввод в реальном времени)  
`--json-schema <schema>`| Принудительный структурированный JSON-вывод, соответствующий схеме  
`--verbose`| Полный пошаговый вывод  
`--include-partial-messages`| Включать частичные чанки сообщений по мере поступления (stream-json + print)  
`--replay-user-messages`| Повторно отправлять сообщения пользователя в stdout (stream-json двунаправленный)  
### System Prompt & Context[​](<#system-prompt--context> "Direct link to System Prompt & Context")
Flag| Effect  
---|---  
`--append-system-prompt <text>`| **Добавить** к системному промпту по умолчанию (сохраняет встроенные возможности)  
`--append-system-prompt-file <path>`| **Добавить** содержимое файла к системному промпту по умолчанию  
`--system-prompt <text>`| **Заменить** весь системный промпт (обычно используй --append)  
`--system-prompt-file <path>`| **Заменить** системный промпт содержимым файла  
`--bare`| Пропустить хуки, плагины, обнаружение MCP, CLAUDE.md, OAuth (самый быстрый запуск)  
`--agents '<json>'`| Динамически определить пользовательских сабагентов как JSON  
`--mcp-config <path>`| Загрузить MCP-серверы из JSON-файла (повторяемый)  
`--strict-mcp-config`| Использовать только MCP-серверы из `--mcp-config`, игнорируя все остальные MCP-конфиги  
`--settings <file-or-json>`| Загрузить дополнительные настройки из JSON-файла или встроенного JSON  
`--setting-sources <sources>`| Источники настроек через запятую: `user`, `project`, `local`  
`--plugin-dir <paths...>`| Загрузить плагины из директорий только для этой сессии  
`--disable-slash-commands`| Отключить все навыки/слеш-команды  
### Debugging[​](<#debugging> "Direct link to Debugging")
Flag| Effect  
---|---  
`-d, --debug [filter]`| Включить отладочное логирование с опциональным фильтром категорий (например, `"api,hooks"`, `"!1p,!file"`)  
`--debug-file <path>`| Записывать отладочные логи в файл (неявно включает режим отладки)  
### Agent Teams[​](<#agent-teams> "Direct link to Agent Teams")
Flag| Effect  
---|---  
`--teammate-mode <mode>`| Как отображаются команды агентов: `auto`, `in-process` или `tmux`  
`--brief`| Включить инструмент `SendUserMessage` для связи агента с пользователем  
### Tool Name Syntax for --allowedTools / --disallowedTools[​](<#tool-name-syntax-for---allowedtools----disallowedtools> "Direct link to Tool Name Syntax for --allowedTools / --disallowedTools")
[code] 
    Read                    # Всё чтение файлов  
    Edit                    # Редактирование файлов (существующих)  
    Write                   # Создание файлов (новых)  
    Bash                    # Все shell-команды  
    Bash(git *)             # Только git-команды  
    Bash(git commit *)      # Только команды git commit  
    Bash(npm run lint:*)    # Сопоставление по шаблону с wildcards  
    WebSearch               # Возможность веб-поиска  
    WebFetch                # Получение веб-страниц  
    mcp__<server>__<tool>   # Конкретный MCP-инструмент  
    
[/code]
## Settings & Configuration[​](<#settings--configuration> "Direct link to Settings & Configuration")
### Settings Hierarchy (highest to lowest priority)[​](<#settings-hierarchy-highest-to-lowest-priority> "Direct link to Settings Hierarchy \(highest to lowest priority\)")
  1. **CLI-флаги** — переопределяют всё
  2. **Локальный проект:** `.claude/settings.local.json` (личный, gitignored)
  3. **Проект:** `.claude/settings.json` (общий, git-tracked)
  4. **Пользователь:** `~/.claude/settings.json` (глобальный)


### Permissions in Settings[​](<#permissions-in-settings> "Direct link to Permissions in Settings")
[code] 
    {  
      "permissions": {  
        "allow": ["Bash(npm run lint:*)", "WebSearch", "Read"],  
        "ask": ["Write(*.ts)", "Bash(git push*)"],  
        "deny": ["Read(.env)", "Bash(rm -rf *)"]  
      }  
    }  
    
[/code]
### Memory Files (CLAUDE.md) Hierarchy[​](<#memory-files-claudemd-hierarchy> "Direct link to Memory Files \(CLAUDE.md\) Hierarchy")
  1. **Глобальный:** `~/.claude/CLAUDE.md` — применяется ко всем проектам
  2. **Проект:** `./CLAUDE.md` — контекст конкретного проекта (git-tracked)
  3. **Локальный:** `.claude/CLAUDE.local.md` — личные переопределения проекта (gitignored)


Используй префикс `#` в интерактивном режиме для быстрого добавления в память: `# Всегда используй отступ в 2 пробела`.
## Interactive Session: Slash Commands[​](<#interactive-session-slash-commands> "Direct link to Interactive Session: Slash Commands")
### Session & Context[​](<#session--context> "Direct link to Session & Context")
Command| Purpose  
---|---  
`/help`| Показать все команды (включая пользовательские и MCP-команды)  
`/compact [focus]`| Сжать контекст для экономии токенов; CLAUDE.md сохраняется при сжатии. Например: `/compact focus on auth logic`  
`/clear`| Очистить историю разговора для свежего старта  
`/context`| Визуализировать использование контекста в виде цветной сетки с советами по оптимизации  
`/cost`| Просмотреть использование токенов с разбивкой по моделям и попаданиям в кэш  
`/resume`| Переключиться на другую сессию или возобновить её  
`/rewind`| Откатиться к предыдущей контрольной точке в разговоре или коде  
`/btw <question>`| Задать побочный вопрос без увеличения стоимости контекста  
`/status`| Показать версию, подключение и информацию о сессии  
`/todos`| Список отслеживаемых пунктов действий из разговора  
`/exit` или `Ctrl+D`| Завершить сессию  
### Development & Review[​](<#development--review> "Direct link to Development & Review")
Command| Purpose  
---|---  
`/review`| Запросить ревью кода текущих изменений  
`/security-review`| Выполнить анализ безопасности текущих изменений  
`/plan [description]`| Войти в режим Plan с автостартом для планирования задач  
`/loop [interval]`| Запланировать повторяющиеся задачи в рамках сессии  
`/batch`| Автоматически создать worktree для больших параллельных изменений (5-30 worktree)  
### Configuration & Tools[​](<#configuration--tools> "Direct link to Configuration & Tools")
Command| Purpose  
---|---  
`/model [model]`| Переключить модель в середине сессии (используй стрелки для настройки усилий)  
`/effort [level]`| Установить уровень усилий рассуждения: `low`, `medium`, `high`, `max` или `auto`  
`/init`| Создать файл CLAUDE.md для памяти проекта  
`/memory`| Открыть CLAUDE.md для редактирования  
`/config`| Открыть интерактивную настройку конфигурации  
`/permissions`| Просмотреть/обновить разрешения инструментов  
`/agents`| Управлять специализированными сабагентами  
`/mcp`| Интерактивный UI для управления MCP-серверами  
`/add-dir`| Добавить дополнительные рабочие директории (полезно для монорепозиториев)  
`/usage`| Показать лимиты плана и статус ограничения скорости  
`/voice`| Включить голосовой режим push-to-talk (20 языков; удерживай Space для записи, отпусти для отправки)  
`/release-notes`| Интерактивный выбор релизных заметок версии  
### Custom Slash Commands[​](<#custom-slash-commands> "Direct link to Custom Slash Commands")
Создай `.claude/commands/<name>.md` (общий для проекта) или `~/.claude/commands/<name>.md` (личный):
[code] 
    # .claude/commands/deploy.md  
    Запустить пайплайн развёртывания:  
    1. Запустить все тесты  
    2. Собрать Docker-образ  
    3. Отправить в регистр  
    4. Обновить окружение $ARGUMENTS (по умолчанию: staging)  
    
[/code]
Использование: `/deploy production` — `$ARGUMENTS` заменяется на ввод пользователя.
### Skills (Natural Language Invocation)[​](<#skills-natural-language-invocation> "Direct link to Skills \(Natural Language Invocation\)")
В отличие от слеш-команд (вызываемых вручную), навыки в `.claude/skills/` — это markdown-руководства, которые Claude вызывает автоматически через естественный язык, когда задача совпадает:
[code] 
    # .claude/skills/database-migration.md  
    Когда просят создать или изменить миграции базы данных:  
    1. Используй Alembic для генерации миграций  
    2. Всегда создавай функцию отката  
    3. Тестируй миграции на локальной копии базы данных  
    
[/code]
## Interactive Session: Keyboard Shortcuts[​](<#interactive-session-keyboard-shortcuts> "Direct link to Interactive Session: Keyboard Shortcuts")
### General Controls[​](<#general-controls> "Direct link to General Controls")
Key| Action  
---|---  
`Ctrl+C`| Отменить текущий ввод или генерацию  
`Ctrl+D`| Выйти из сессии  
`Ctrl+R`| Обратный поиск по истории команд  
`Ctrl+B`| Отправить выполняющуюся задачу в фон  
`Ctrl+V`| Вставить изображение в разговор  
`Ctrl+O`| Режим транскрипта — увидеть процесс мышления Claude  
`Ctrl+G` или `Ctrl+X Ctrl+E`| Открыть промпт во внешнем редакторе  
`Esc Esc`| Откатить разговор или состояние кода / подвести итог  
### Mode Toggles[​](<#mode-toggles> "Direct link to Mode Toggles")
Key| Action  
---|---  
`Shift+Tab`| Циклическое переключение режимов разрешений (Normal → Auto-Accept → Plan)  
`Alt+P`| Переключить модель  
`Alt+T`| Переключить режим размышления  
`Alt+O`| Переключить Fast Mode  
### Multiline Input[​](<#multiline-input> "Direct link to Multiline Input")
Key| Action  
---|---  
`\` \+ `Enter`| Быстрый перевод строки  
`Shift+Enter`| Перевод строки (альтернатива)  
`Ctrl+J`| Перевод строки (альтернатива)  
### Input Prefixes[​](<#input-prefixes> "Direct link to Input Prefixes")
Prefix| Action  
---|---  
`!`| Выполнить bash напрямую, минуя AI (например, `!npm test`). Используй `!` отдельно для переключения в shell-режим.  
`@`| Ссылка на файлы/директории с автодополнением (например, `@./src/api/`)  
`#`| Быстрое добавление в память CLAUDE.md (например, `# Используй отступ в 2 пробела`)  
`/`| Слеш-команды  
### Pro Tip: "ultrathink"[​](<#pro-tip-ultrathink> "Direct link to Pro Tip: \"ultrathink\"")
Используй ключевое слово "ultrathink" в своём промпте для максимального усилия рассуждения на конкретном шаге. Это включает самый глубокий режим мышления независимо от текущей настройки `/effort`.
## PR Review Pattern[​](<#pr-review-pattern> "Direct link to PR Review Pattern")
### Quick Review (Print Mode)[​](<#quick-review-print-mode> "Direct link to Quick Review \(Print Mode\)")
[code] 
    terminal(command="cd /path/to/repo && git diff main...feature-branch | claude -p 'Review this diff for bugs, security issues, and style problems. Be thorough.' --max-turns 1", timeout=60)  
    
[/code]
### Deep Review (Interactive + Worktree)[​](<#deep-review-interactive--worktree> "Direct link to Deep Review \(Interactive + Worktree\)")
[code] 
    terminal(command="tmux new-session -d -s review -x 140 -y 40")  
    terminal(command="tmux send-keys -t review 'cd /path/to/repo && claude -w pr-review' Enter")  
    terminal(command="sleep 5 && tmux send-keys -t review Enter")  # Диалог доверия  
    terminal(command="sleep 2 && tmux send-keys -t review 'Review all changes vs main. Check for bugs, security issues, race conditions, and missing tests.' Enter")  
    terminal(command="sleep 30 && tmux capture-pane -t review -p -S -60")  
    
[/code]
### PR Review from Number[​](<#pr-review-from-number> "Direct link to PR Review from Number")
[code] 
    terminal(command="claude -p 'Review this PR thoroughly' --from-pr 42 --max-turns 10", workdir="/path/to/repo", timeout=120)  
    
[/code]
### Claude Worktree with tmux[​](<#claude-worktree-with-tmux> "Direct link to Claude Worktree with tmux")
[code] 
    terminal(command="claude -w feature-x --tmux", workdir="/path/to/repo")  
    
[/code]
Создаёт изолированный git worktree в `.claude/worktrees/feature-x` И tmux-сессию для него. Использует нативные панели iTerm2, если доступно; добавь `--tmux=classic` для традиционного tmux.
## Parallel Claude Instances[​](<#parallel-claude-instances> "Direct link to Parallel Claude Instances")
Запускай несколько независимых задач Claude одновременно:
[code] 
    # Задача 1: Исправить бэкенд  
    terminal(command="tmux new-session -d -s task1 -x 140 -y 40 && tmux send-keys -t task1 'cd ~/project && claude -p \"Fix the auth bug in src/auth.py\" --allowedTools \"Read,Edit\" --max-turns 10' Enter")  
      
    # Задача 2: Написать тесты  
    terminal(command="tmux new-session -d -s task2 -x 140 -y 40 && tmux send-keys -t task2 'cd ~/project && claude -p \"Write integration tests for the API endpoints\" --allowedTools \"Read,Write,Bash\" --max-turns 15' Enter")  
      
    # Задача 3: Обновить документацию  
    terminal(command="tmux new-session -d -s task3 -x 140 -y 40 && tmux send-keys -t task3 'cd ~/project && claude -p \"Update README.md with the new API endpoints\" --allowedTools \"Read,Edit\" --max-turns 5' Enter")  
      
    # Мониторинг всех  
    terminal(command="sleep 30 && for s in task1 task2 task3; do echo '=== '$s' ==='; tmux capture-pane -t $s -p -S -5 2>/dev/null; done")  
    
[/code]
## CLAUDE.md — Project Context File[​](<#claudemd--project-context-file> "Direct link to CLAUDE.md — Project Context File")
Claude Code автоматически загружает `CLAUDE.md` из корня проекта. Используй его для сохранения контекста проекта:
[code] 
    # Project: My API  
      
    ## Architecture  
    - FastAPI backend with SQLAlchemy ORM  
    - PostgreSQL database, Redis cache  
    - pytest for testing with 90% coverage target  
      
    ## Key Commands  
    - `make test` — run full test suite  
    - `make lint` — ruff + mypy  
    - `make dev` — start dev server on :8000  
      
    ## Code Standards  
    - Type hints on all public functions  
    - Docstrings in Google style  
    - 2-space indentation for YAML, 4-space for Python  
    - No wildcard imports  
    
[/code]
**Будь конкретен.** Вместо «Пиши хороший код» используй «Используй отступ в 2 пробела для JS» или «Называй тестовые файлы с суффиксом `.test.ts`». Конкретные инструкции экономят циклы исправлений.
### Rules Directory (Modular CLAUDE.md)[​](<#rules-directory-modular-claudemd> "Direct link to Rules Directory \(Modular CLAUDE.md\)")
Для проектов с множеством правил используй директорию правил вместо одного массивного CLAUDE.md:
  * **Правила проекта:** `.claude/rules/*.md` — общие для команды, git-tracked
  * **Пользовательские правила:** `~/.claude/rules/*.md` — личные, глобальные


Каждый `.md`-файл в директории правил загружается как дополнительный контекст. Это чище, чем втискивать всё в один CLAUDE.md.
### Auto-Memory[​](<#auto-memory> "Direct link to Auto-Memory")
Claude автоматически сохраняет изученный контекст проекта в `~/.claude/projects/<project>/memory/`.
  * **Лимит:** 25 КБ или 200 строк на проект
  * Это отдельно от CLAUDE.md — это собственные заметки Claude о проекте, накопленные за сессии


## Custom Subagents[​](<#custom-subagents> "Direct link to Custom Subagents")
Определяй специализированных агентов в `.claude/agents/` (проект), `~/.claude/agents/` (личные) или через CLI-флаг `--agents` (сессия):
### Agent Location Priority[​](<#agent-location-priority> "Direct link to Agent Location Priority")
  1. `.claude/agents/` — уровень проекта, общие для команды
  2. `--agents` CLI-флаг — для конкретной сессии, динамические
  3. `~/.claude/agents/` — уровень пользователя, личные


### Creating an Agent[​](<#creating-an-agent> "Direct link to Creating an Agent")
[code] 
    # .claude/agents/security-reviewer.md  
    ---  
    name: security-reviewer  
    description: Security-focused code review  
    model: opus  
    tools: [Read, Bash]  
    ---  
    You are a senior security engineer. Review code for:  
    - Injection vulnerabilities (SQL, XSS, command injection)  
    - Authentication/authorization flaws  
    - Secrets in code  
    - Unsafe deserialization  
    
[/code]
Вызов через: `@security-reviewer review the auth module`
### Dynamic Agents via CLI[​](<#dynamic-agents-via-cli> "Direct link to Dynamic Agents via CLI")
[code] 
    terminal(command="claude --agents '{\"reviewer\": {\"description\": \"Reviews code\", \"prompt\": \"You are a code reviewer focused on performance\"}}' -p 'Use @reviewer to check auth.py'", timeout=120)  
    
[/code]
Claude может оркестровать несколько агентов: «Используй @db-expert для оптимизации запросов, затем @security для аудита изменений.»
## Hooks — Automation on Events[​](<#hooks--automation-on-events> "Direct link to Hooks — Automation on Events")
Настрой в `.claude/settings.json` (проект) или `~/.claude/settings.json` (глобальный):
[code] 
    {  
      "hooks": {  
        "PostToolUse": [{  
          "matcher": "Write(*.py)",  
          "hooks": [{"type": "command", "command": "ruff check --fix $CLAUDE_FILE_PATHS"}]  
        }],  
        "PreToolUse": [{  
          "matcher": "Bash",  
          "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'Blocked!' && exit 2; fi"}]  
        }],  
        "Stop": [{  
          "hooks": [{"type": "command", "command": "echo 'Claude finished a response' >> /tmp/claude-activity.log"}]  
        }]  
      }  
    }  
    
[/code]
### All 8 Hook Types[​](<#all-8-hook-types> "Direct link to All 8 Hook Types")
Hook| Когда срабатывает| Обычное использование  
---|---|---  
`UserPromptSubmit`| Перед обработкой промпта пользователя| Валидация ввода, логирование  
`PreToolUse`| Перед выполнением инструмента| Шлюзы безопасности, блокировка опасных команд (exit 2 = блокировка)  
`PostToolUse`| После завершения инструмента| Автоформатирование кода, запуск линтеров  
`Notification`| При запросах разрешений или ожидании ввода| Десктопные уведомления, оповещения  
`Stop`| Когда Claude завершает ответ| Логирование завершения, обновления статуса  
`SubagentStop`| Когда завершается сабагент| Оркестрация агентов  
`PreCompact`| Перед очисткой контекстной памяти| Резервное копирование транскриптов сессии  
`SessionStart`| Когда начинается сессия| Загрузка контекста разработки (например, `git status`)  
### Hook Environment Variables[​](<#hook-environment-variables> "Direct link to Hook Environment Variables")
Variable| Content  
---|---  
`CLAUDE_PROJECT_DIR`| Текущий путь проекта  
`CLAUDE_FILE_PATHS`| Файлы, которые изменяются  
`CLAUDE_TOOL_INPUT`| Параметры инструмента в JSON  
### Security Hook Examples[​](<#security-hook-examples> "Direct link to Security Hook Examples")
[code] 
    {  
      "PreToolUse": [{  
        "matcher": "Bash",  
        "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|git push.*--force|:(){ :|:& };:'; then echo 'Dangerous command blocked!' && exit 2; fi"}]  
      }]  
    }  
    
[/code]
## MCP Integration[​](<#mcp-integration> "Direct link to MCP Integration")
Добавляй внешние серверы инструментов для баз данных, API и сервисов:
[code] 
    # Интеграция GitHub  
    terminal(command="claude mcp add -s user github -- npx @modelcontextprotocol/server-github", timeout=30)  
      
    # Запросы PostgreSQL  
    terminal(command="claude mcp add -s local postgres -- npx @anthropic-ai/server-postgres --connection-string postgresql://localhost/mydb", timeout=30)  
      
    # Puppeteer для веб-тестирования  
    terminal(command="claude mcp add puppeteer -- npx @anthropic-ai/server-puppeteer", timeout=30)  
    
[/code]
### MCP Scopes[​](<#mcp-scopes> "Direct link to MCP Scopes")
Flag| Scope| Хранилище  
---|---|---  
`-s user`| Глобальный (все проекты)| `~/.claude.json`  
`-s local`| Этот проект (личный)| `.claude/settings.local.json` (gitignored)  
`-s project`| Этот проект (общий для команды)| `.claude/settings.json` (git-tracked)  
### MCP in Print/CI Mode[​](<#mcp-in-printci-mode> "Direct link to MCP in Print/CI Mode")
[code] 
    terminal(command="claude --bare -p 'Query database' --mcp-config mcp-servers.json --strict-mcp-config", timeout=60)  
    
[/code]
`--strict-mcp-config` игнорирует все MCP-серверы, кроме указанных в `--mcp-config`.
Ссылайся на MCP-ресурсы в чате: `@github:issue://123`
### MCP Limits & Tuning[​](<#mcp-limits--tuning> "Direct link to MCP Limits & Tuning")
  * **Описания инструментов:** лимит 2 КБ на сервер для описаний инструментов и инструкций сервера
  * **Размер результата:** по умолчанию ограничен; используй аннотацию `maxResultSizeChars` для разрешения до **500К** символов для больших выводов
  * **Выходные токены:** `export MAX_MCP_OUTPUT_TOKENS=50000` — ограничение вывода от MCP-серверов для предотвращения переполнения контекста
  * **Транспорты:** `stdio` (локальный процесс), `http` (удалённый), `sse` (server-sent events)


## Monitoring Interactive Sessions[​](<#monitoring-interactive-sessions> "Direct link to Monitoring Interactive Sessions")
### Reading the TUI Status[​](<#reading-the-tui-status> "Direct link to Reading the TUI Status")
[code] 
    # Периодический захват для проверки, работает ли Claude или ждёт ввода  
    terminal(command="tmux capture-pane -t dev -p -S -10")  
    
[/code]
Ищи эти индикаторы:
  * `❯` внизу = ожидание твоего ввода (Claude закончил или задаёт вопрос)
  * `●` строки = Claude активно использует инструменты (читает, пишет, запускает команды)
  * `⏵⏵ bypass permissions on` = строка состояния, показывающая режим разрешений
  * `◐ medium · /effort` = текущий уровень усилий в строке состояния
  * `ctrl+o to expand` = вывод инструмента был обрезан (можно развернуть интерактивно)


### Context Window Health[​](<#context-window-health> "Direct link to Context Window Health")
Используй `/context` в интерактивном режиме для просмотра цветной сетки использования контекста. Ключевые пороги:
  * **< 70%** — Нормальная работа, полная точность
  * **70-85%** — Точность начинает падать, рассмотри `/compact`
  * **> 85%** — Риск галлюцинаций значительно возрастает, используй `/compact` или `/clear`


## Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
Variable| Effect  
---|---  
`ANTHROPIC_API_KEY`| API-ключ для аутентификации (альтернатива OAuth)  
`CLAUDE_CODE_EFFORT_LEVEL`| Уровень усилий по умолчанию: `low`, `medium`, `high`, `max` или `auto`  
`MAX_THINKING_TOKENS`| Ограничение токенов мышления (установи `0` для полного отключения)  
`MAX_MCP_OUTPUT_TOKENS`| Ограничение вывода от MCP-серверов (значение по умолчанию варьируется; установи, например, `50000`)  
`CLAUDE_CODE_NO_FLICKER=1`| Включить альтернативный рендеринг экрана для устранения мерцания терминала  
`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`| Удалять учётные данные из дочерних процессов для безопасности  
## Cost & Performance Tips[​](<#cost--performance-tips> "Direct link to Cost & Performance Tips")
  1. **Используй`--max-turns`** в print mode для предотвращения бесконечных циклов. Начинай с 5-10 для большинства задач.
  2. **Используй`--max-budget-usd`** для лимитов расходов. Примечание: минимум ~$0.05 для создания кэша системного промпта.
  3. **Используй`--effort low`** для простых задач (быстрее, дешевле). `high` или `max` для сложных рассуждений.
  4. **Используй`--bare`** для CI/скриптов, чтобы пропустить накладные расходы на обнаружение плагинов/хуков.
  5. **Используй`--allowedTools`** для ограничения только необходимым (например, только `Read` для ревью).
  6. **Используй`/compact`** в интерактивных сессиях, когда контекст становится большим.
  7. **Передавай ввод через pipe** вместо чтения файлов Claude, когда нужен просто анализ известного содержимого.
  8. **Используй`--model haiku`** для простых задач (дешевле) и `--model opus` для сложной многошаговой работы.
  9. **Используй`--fallback-model haiku`** в print mode для корректной обработки перегрузки модели.
  10. **Начинай новые сессии для разных задач** — сессии длятся 5 часов; свежий контекст эффективнее.
  11. **Используй`--no-session-persistence`** в CI, чтобы избежать накопления сохранённых сессий на диске.


## Pitfalls & Gotchas[​](<#pitfalls--gotchas> "Direct link to Pitfalls & Gotchas")
  1. **Интерактивный режим ТРЕБУЕТ tmux** — Claude Code — полноценное TUI-приложение. Использование только `pty=true` в терминале Hermes работает, но tmux даёт `capture-pane` для мониторинга и `send-keys` для ввода, что необходимо для оркестрации.
  2. **Диалог`--dangerously-skip-permissions` по умолчанию выбирает «No, exit»** — ты должен отправить Down, затем Enter для принятия. Print mode (`-p`) полностью пропускает это.
  3. **Минимум`--max-budget-usd` составляет ~$0.05** — только создание кэша системного промпта стоит столько. Установка меньшего значения вызовет ошибку немедленно.
  4. **`--max-turns` работает только в print mode** — игнорируется в интерактивных сессиях.
  5. **Claude может использовать`python` вместо `python3`** — на системах без symlink `python` bash-команды Claude сначала упадут, но он сам исправится.
  6. **Возобновление сессии требует той же директории** — `--continue` находит последнюю сессию для текущей рабочей директории.
  7. **`--json-schema` требует достаточно `--max-turns`** — Claude должен прочитать файлы перед созданием структурированного вывода, что требует нескольких шагов.
  8. **Диалог доверия появляется только один раз на директорию** — только в первый раз, затем кэшируется.
  9. **Фоновые tmux-сессии сохраняются** — всегда очищай их с помощью `tmux kill-session -t <name>` по завершении.
  10. **Слеш-команды (например,`/commit`) работают только в интерактивном режиме** — в режиме `-p` опиши задачу на естественном языке.
  11. **`--bare` пропускает OAuth** — требует переменную окружения `ANTHROPIC_API_KEY` или `apiKeyHelper` в настройках.
  12. **Деградация контекста реальна** — качество вывода AI заметно снижается при использовании контекстного окна выше 70%. Мониторь с помощью `/context` и проактивно используй `/compact`.


## Rules for Hermes Agents[​](<#rules-for-hermes-agents> "Direct link to Rules for Hermes Agents")
  1. **Предпочитай print mode (`-p`) для одиночных задач** — чище, без обработки диалогов, структурированный вывод
  2. **Используй tmux для многошаговой интерактивной работы** — единственный надёжный способ оркестрации TUI
  3. **Всегда устанавливай`workdir`** — держи Claude сфокусированным на правильной директории проекта
  4. **Устанавливай`--max-turns` в print mode** — предотвращает бесконечные циклы и неконтролируемые расходы
  5. **Мониторь tmux-сессии** — используй `tmux capture-pane -t <session> -p -S -50` для проверки прогресса
  6. **Ищи приглашение`❯`** — указывает, что Claude ожидает ввода (закончил или задаёт вопрос)
  7. **Очищай tmux-сессии** — завершай их по готовности, чтобы избежать утечки ресурсов
  8. **Сообщай результаты пользователю** — после завершения опиши, что сделал Claude и что изменилось
  9. **Не убивай медленные сессии** — Claude может выполнять многошаговую работу; проверь прогресс вместо этого
  10. **Используй`--allowedTools`** — ограничивай возможности тем, что действительно нужно для задачи


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [Two Orchestration Modes](<#two-orchestration-modes>)
    * [Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED for most tasks)](<#mode-1-print-mode--p--non-interactive-preferred-for-most-tasks>)
    * [Mode 2: Interactive PTY via tmux — Multi-Turn Sessions](<#mode-2-interactive-pty-via-tmux--multi-turn-sessions>)
  * [PTY Dialog Handling (CRITICAL for Interactive Mode)](<#pty-dialog-handling-critical-for-interactive-mode>)
    * [Dialog 1: Workspace Trust (first visit to a directory)](<#dialog-1-workspace-trust-first-visit-to-a-directory>)
    * [Dialog 2: Bypass Permissions Warning (only with --dangerously-skip-permissions)](<#dialog-2-bypass-permissions-warning-only-with---dangerously-skip-permissions>)
    * [Robust Dialog Handling Pattern](<#robust-dialog-handling-pattern>)
  * [CLI Subcommands](<#cli-subcommands>)
  * [Print Mode Deep Dive](<#print-mode-deep-dive>)
    * [Structured JSON Output](<#structured-json-output>)
    * [Streaming JSON Output](<#streaming-json-output>)
    * [Bidirectional Streaming](<#bidirectional-streaming>)
    * [Piped Input](<#piped-input>)
    * [JSON Schema for Structured Extraction](<#json-schema-for-structured-extraction>)
    * [Session Continuation](<#session-continuation>)
    * [Bare Mode for CI/Scripting](<#bare-mode-for-ciscripting>)
    * [Fallback Model for Overload](<#fallback-model-for-overload>)
  * [Complete CLI Flags Reference](<#complete-cli-flags-reference>)
    * [Session & Environment](<#session--environment>)
    * [Model & Performance](<#model--performance>)
    * [Permission & Safety](<#permission--safety>)
    * [Output & Input Format](<#output--input-format>)
    * [System Prompt & Context](<#system-prompt--context>)
    * [Debugging](<#debugging>)
    * [Agent Teams](<#agent-teams>)
    * [Tool Name Syntax for --allowedTools / --disallowedTools](<#tool-name-syntax-for---allowedtools----disallowedtools>)
  * [Settings & Configuration](<#settings--configuration>)
    * [Settings Hierarchy (highest to lowest priority)](<#settings-hierarchy-highest-to-lowest-priority>)
    * [Permissions in Settings](<#permissions-in-settings>)
    * [Memory Files (CLAUDE.md) Hierarchy](<#memory-files-claudemd-hierarchy>)
  * [Interactive Session: Slash Commands](<#interactive-session-slash-commands>)
    * [Session & Context](<#session--context>)
    * [Development & Review](<#development--review>)
    * [Configuration & Tools](<#configuration--tools>)
    * [Custom Slash Commands](<#custom-slash-commands>)
    * [Skills (Natural Language Invocation)](<#skills-natural-language-invocation>)
  * [Interactive Session: Keyboard Shortcuts](<#interactive-session-keyboard-shortcuts>)
    * [General Controls](<#general-controls>)
    * [Mode Toggles](<#mode-toggles>)
    * [Multiline Input](<#multiline-input>)
    * [Input Prefixes](<#input-prefixes>)
    * [Pro Tip: "ultrathink"](<#pro-tip-ultrathink>)
  * [PR Review Pattern](<#pr-review-pattern>)
    * [Quick Review (Print Mode)](<#quick-review-print-mode>)
    * [Deep Review (Interactive + Worktree)](<#deep-review-interactive--worktree>)
    * [PR Review from Number](<#pr-review-from-number>)
    * [Claude Worktree with tmux](<#claude-worktree-with-tmux>)
  * [Parallel Claude Instances](<#parallel-claude-instances>)
  * [CLAUDE.md — Project Context File](<#claudemd--project-context-file>)
    * [Rules Directory (Modular CLAUDE.md)](<#rules-directory-modular-claudemd>)
    * [Auto-Memory](<#auto-memory>)
  * [Custom Subagents](<#custom-subagents>)
    * [Agent Location Priority](<#agent-location-priority>)
    * [Creating an Agent](<#creating-an-agent>)
    * [Dynamic Agents via CLI](<#dynamic-agents-via-cli>)
  * [Hooks — Automation on Events](<#hooks--automation-on-events>)
    * [All 8 Hook Types](<#all-8-hook-types>)
    * [Hook Environment Variables](<#hook-environment-variables>)
    * [Security Hook Examples](<#security-hook-examples>)
  * [MCP Integration](<#mcp-integration>)
    * [MCP Scopes](<#mcp-scopes>)
    * [MCP in Print/CI Mode](<#mcp-in-printci-mode>)
    * [MCP Limits & Tuning](<#mcp-limits--tuning>)
  * [Monitoring Interactive Sessions](<#monitoring-interactive-sessions>)
    * [Reading the TUI Status](<#reading-the-tui-status>)
    * [Context Window Health](<#context-window-health>)
  * [Environment Variables](<#environment-variables>)
  * [Cost & Performance Tips](<#cost--performance-tips>)
  * [Pitfalls & Gotchas](<#pitfalls--gotchas>)
  * [Rules for Hermes Agents](<#rules-for-hermes-agents>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code -->
