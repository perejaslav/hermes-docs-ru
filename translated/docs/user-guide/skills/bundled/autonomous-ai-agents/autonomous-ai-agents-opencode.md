On this page
Делегирование задач по кодингу OpenCode CLI (фичи, ревью PR).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/autonomous-ai-agents/opencode` |
|Version| `1.2.0` |
|Author| Hermes Agent |
|License| MIT |
|Tags| `Coding-Agent`, `OpenCode`, `Autonomous`, `Refactoring`, `Code-Review` |
|Related skills| [`claude-code`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code>), [`codex`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>), [`hermes-agent`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent>) |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# OpenCode CLI
Используй [OpenCode](<https://opencode.ai>) как автономного рабочего по кодингу, управляемого через терминал Hermes и process-инструменты. OpenCode — это агент-кодировщик с открытым исходным кодом, не привязанный к конкретному провайдеру, с TUI и CLI.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь явно просит использовать OpenCode
  * Ты хочешь привлечь внешнего агента-кодировщика для реализации/рефакторинга/ревью кода
  * Нужны длительные сессии кодинга с проверкой прогресса
  * Нужно параллельное выполнение задач в изолированных workdir/worktree


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * OpenCode установлен: `npm i -g opencode-ai@latest` или `brew install anomalyco/tap/opencode`
  * Аутентификация настроена: `opencode auth login` или установи переменные окружения провайдера (OPENROUTER_API_KEY и т.д.)
  * Проверка: `opencode auth list` должен показывать хотя бы одного провайдера
  * Git-репозиторий для задач с кодом (рекомендуется)
  * `pty=true` для интерактивных TUI-сессий


## Binary Resolution (Important)[​](<#binary-resolution-important> "Direct link to Binary Resolution \(Important\)")
Окружения оболочки могут разрешать разные бинарники OpenCode. Если поведение отличается между твоим терминалом и Hermes, проверь:
[code] 
    terminal(command="which -a opencode")  
    terminal(command="opencode --version")  
    
[/code]
При необходимости зафиксируй явный путь к бинарнику:
[code] 
    terminal(command="$HOME/.opencode/bin/opencode run '...'", workdir="~/project", pty=true)  
    
[/code]
## One-Shot Tasks[​](<#one-shot-tasks> "Direct link to One-Shot Tasks")
Используй `opencode run` для ограниченных неинтерактивных задач:
[code] 
    terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")  
    
[/code]
Прикрепи файлы контекста с помощью `-f`:
[code] 
    terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")  
    
[/code]
Показывать размышления модели с `--thinking`:
[code] 
    terminal(command="opencode run 'Debug why tests fail in CI' --thinking", workdir="~/project")  
    
[/code]
Принудительно указать конкретную модель:
[code] 
    terminal(command="opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")  
    
[/code]
## Interactive Sessions (Background)[​](<#interactive-sessions-background> "Direct link to Interactive Sessions \(Background\)")
Для итеративной работы, требующей множества обменов, запусти TUI в фоне:
[code] 
    terminal(command="opencode", workdir="~/project", background=true, pty=true)  
    # Возвращает session_id  
      
    # Отправить запрос  
    process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")  
      
    # Мониторинг прогресса  
    process(action="poll", session_id="<id>")  
    process(action="log", session_id="<id>")  
      
    # Отправить дополнительный запрос  
    process(action="submit", session_id="<id>", data="Now add error handling for token expiry")  
      
    # Выйти чисто — Ctrl+C  
    process(action="write", session_id="<id>", data="\\x03")  
    # Или просто завершить процесс  
    process(action="kill", session_id="<id>")  
    
[/code]
**Важно:** НЕ используй `/exit` — это недопустимая команда OpenCode, и она откроет диалог выбора агента. Используй Ctrl+C (`\\x03`) или `process(action="kill")` для выхода.
### TUI Keybindings[​](<#tui-keybindings> "Direct link to TUI Keybindings")
Key| Action  
---|---  
`Enter`| Отправить сообщение (нажми дважды, если нужно)  
`Tab`| Переключение между агентами (build/plan)  
`Ctrl+P`| Открыть палитру команд  
`Ctrl+X L`| Переключить сессию  
`Ctrl+X M`| Переключить модель  
`Ctrl+X N`| Новая сессия  
`Ctrl+X E`| Открыть редактор  
`Ctrl+C`| Выйти из OpenCode  
### Resuming Sessions[​](<#resuming-sessions> "Direct link to Resuming Sessions")
После выхода OpenCode выводит ID сессии. Возобнови с помощью:
[code] 
    terminal(command="opencode -c", workdir="~/project", background=true, pty=true)  # Продолжить последнюю сессию  
    terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)  # Конкретная сессия  
    
[/code]
## Common Flags[​](<#common-flags> "Direct link to Common Flags")
Flag| Use  
---|---  
`run 'prompt'`| Одноразовое выполнение и выход  
`--continue` / `-c`| Продолжить последнюю сессию OpenCode  
`--session <id>` / `-s`| Продолжить конкретную сессию  
`--agent <name>`| Выбрать агента OpenCode (build или plan)  
`--model provider/model`| Принудительно указать модель  
`--format json`| Машиночитаемый вывод/события  
`--file <path>` / `-f`| Прикрепить файл(ы) к сообщению  
`--thinking`| Показать блоки размышлений модели  
`--variant <level>`| Усилия рассуждения (high, max, minimal)  
`--title <name>`| Назвать сессию  
`--attach <url>`| Подключиться к работающему серверу opencode  
## Procedure[​](<#procedure> "Direct link to Procedure")
  1. Проверь готовность инструмента:
     * `terminal(command="opencode --version")`
     * `terminal(command="opencode auth list")`
  2. Для ограниченных задач используй `opencode run '...'` (pty не нужен).
  3. Для итеративных задач запускай `opencode` с `background=true, pty=true`.
  4. Мониторь долгие задачи с помощью `process(action="poll"|"log")`.
  5. Если OpenCode запрашивает ввод, отвечай через `process(action="submit", ...)`.
  6. Выходи с помощью `process(action="write", data="\\x03")` или `process(action="kill")`.
  7. Сообщи пользователю об изменениях в файлах, результатах тестов и следующих шагах.


## PR Review Workflow[​](<#pr-review-workflow> "Direct link to PR Review Workflow")
У OpenCode есть встроенная команда PR:
[code] 
    terminal(command="opencode pr 42", workdir="~/project", pty=true)  
    
[/code]
Или сделай ревью во временном клоне для изоляции:
[code] 
    terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, and style issues.' -f $(git diff origin/main --name-only | head -20 | tr '\\n' ' ')", pty=true)  
    
[/code]
## Parallel Work Pattern[​](<#parallel-work-pattern> "Direct link to Parallel Work Pattern")
Используй отдельные workdir/worktree для избежания коллизий:
[code] 
    terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)  
    terminal(command="opencode run 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)  
    process(action="list")  
    
[/code]
## Session & Cost Management[​](<#session--cost-management> "Direct link to Session & Cost Management")
Список прошлых сессий:
[code] 
    terminal(command="opencode session list")  
    
[/code]
Проверка использования токенов и стоимости:
[code] 
    terminal(command="opencode stats")  
    terminal(command="opencode stats --days 7 --models anthropic/claude-sonnet-4")  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * Интерактивные сессии `opencode` (TUI) требуют `pty=true`. Команда `opencode run` НЕ требует pty.
  * `/exit` — НЕДОПУСТИМАЯ команда — она открывает выбор агента. Используй Ctrl+C для выхода из TUI.
  * Несовпадение PATH может привести к выбору неправильного бинарника/конфига модели OpenCode.
  * Если OpenCode завис, проверь логи перед завершением:
    * `process(action="log", session_id="<id>")`
  * Избегай использования одной рабочей директории для параллельных сессий OpenCode.
  * Enter, возможно, придётся нажать дважды для отправки в TUI (один раз для финализации текста, второй для отправки).


## Verification[​](<#verification> "Direct link to Verification")
Дымовой тест:
[code] 
    terminal(command="opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'")  
    
[/code]
Критерии успеха:
  * Вывод содержит `OPENCODE_SMOKE_OK`
  * Команда завершается без ошибок провайдера/модели
  * Для задач с кодом: ожидаемые файлы изменены и тесты проходят


## Rules[​](<#rules> "Direct link to Rules")
  1. Предпочитай `opencode run` для одноразовой автоматизации — это проще и не требует pty.
  2. Используй интерактивный фоновый режим только когда нужна итерация.
  3. Всегда ограничивай сессии OpenCode одним репозиторием/workdir.
  4. Для длительных задач предоставляй обновления прогресса из логов `process`.
  5. Сообщай о конкретных результатах (изменённые файлы, тесты, оставшиеся риски).
  6. Завершай интерактивные сессии через Ctrl+C или kill, никогда через `/exit`.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [Binary Resolution (Important)](<#binary-resolution-important>)
  * [One-Shot Tasks](<#one-shot-tasks>)
  * [Interactive Sessions (Background)](<#interactive-sessions-background>)
    * [TUI Keybindings](<#tui-keybindings>)
    * [Resuming Sessions](<#resuming-sessions>)
  * [Common Flags](<#common-flags>)
  * [Procedure](<#procedure>)
  * [PR Review Workflow](<#pr-review-workflow>)
  * [Parallel Work Pattern](<#parallel-work-pattern>)
  * [Session & Cost Management](<#session--cost-management>)
  * [Pitfalls](<#pitfalls>)
  * [Verification](<#verification>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode -->
