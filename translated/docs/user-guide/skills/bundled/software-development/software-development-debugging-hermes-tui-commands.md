On this page
Отладка TUI-команд слэша Hermes: Python, gateway, Ink UI.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
|Source| Встроенный (установлен по умолчанию)  |
|Path| `skills/software-development/debugging-hermes-tui-commands`  |
|Version| `1.0.0`  |
|Author| Hermes Agent  |
|License| MIT  |
|Tags| `debugging`, `hermes-agent`, `tui`, `slash-commands`, `typescript`, `python`  |
|Related skills| [`python-debugpy`](</docs/user-guide/skills/bundled/software-development/software-development-python-debugpy>), [`node-inspect-debugger`](</docs/user-guide/skills/bundled/software-development/software-development-node-inspect-debugger>), [`systematic-debugging`](</docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при активации этого навыка. Это те инструкции, которые видит агент, когда навык активен.
# Debugging Hermes TUI Slash Commands
## Overview[​](<#overview> "Direct link to Overview")
Слэш-команды Hermes охватывают три уровня — реестр команд Python, JSON-RPC-мост tui_gateway и фронтенд Ink/TypeScript. Когда команда ведёт себя некорректно (отсутствует в автодополнении, работает в CLI, но не в TUI, конфигурация сохраняется, но интерфейс не обновляется), ошибка почти всегда вызвана рассогласованием одного из уровней с другим.
Используйте этот навык при возникновении проблем со слэш-командами в TUI Hermes, особенно когда команды не отображаются в автодополнении, некорректно работают в TUI или их необходимо добавить/обновить.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Слэш-команда существует в одной части кодовой базы, но работает не полностью
  * Команду нужно добавить как в бэкенд, так и во фронтенд
  * Автодополнение команд не работает для определённых команд
  * Поведение команды различается между CLI и TUI
  * Команда сохраняет конфигурацию, но не применяет изменения в реальном времени в TUI


## Architecture Overview[​](<#architecture-overview> "Direct link to Architecture Overview")
[code] 
    Python backend (hermes_cli/commands.py)     <- канонический COMMAND_REGISTRY  
           │  
           ▼  
    TUI gateway (tui_gateway/server.py)         <- slash.exec / command.dispatch  
           │  
           ▼  
    TUI frontend (ui-tui/src/app/slash/)        <- локальные обработчики + fallthrough  
    
[/code]
Определения команд должны быть согласованно зарегистрированы в Python и TypeScript для корректной работы. Python `COMMAND_REGISTRY` является источником истины для: диспетчеризации CLI, справки gateway, меню Telegram BotCommand, карты подкоманд Slack и данных автодополнения, отправляемых в Ink.
## Investigation Steps[​](<#investigation-steps> "Direct link to Investigation Steps")
  1. **Проверьте, существует ли команда во фронтенде TUI:**
[code] search_files --pattern "/commandname" --file_glob "*.ts" --path ui-tui/  
         search_files --pattern "/commandname" --file_glob "*.tsx" --path ui-tui/  
         
[/code]
  2. **Изучите определение команды в TUI:**
[code] read_file ui-tui/src/app/slash/commands/core.ts  
         # Если не там:  
         search_files --pattern "commandname" --path ui-tui/src/app/slash/commands --target files  
         
[/code]
  3. **Проверьте, существует ли команда в бэкенде Python:**
[code] search_files --pattern "CommandDef" --file_glob "*.py" --path hermes_cli/  
         search_files --pattern "commandname" --path hermes_cli/commands.py --context 3  
         
[/code]
  4. **Изучите реализацию gateway:**
[code] search_files --pattern "complete.slash|slash.exec" --path tui_gateway/  
         
[/code]


## Fix: Missing Command Autocomplete[​](<#fix-missing-command-autocomplete> "Direct link to Fix: Missing Command Autocomplete")
Если команда существует в TUI, но не отображается в автодополнении:
  1. Добавьте запись `CommandDef` в `COMMAND_REGISTRY` в `hermes_cli/commands.py`:
[code] CommandDef("commandname", "Описание команды", "Session",  
                    cli_only=True, aliases=("alias",),  
                    args_hint="[arg1|arg2|arg3]",  
                    subcommands=("arg1", "arg2", "arg3")),  
         
[/code]
  2. Внимательно выбирайте `cli_only` и доступность через gateway:
     * `cli_only=True` — только в интерактивном CLI/TUI
     * `gateway_only=True` — только в мессенджер-платформах
     * ни один — доступно везде
     * `gateway_config_gate="display.foo"` — доступность через gateway, управляемая конфигом
  3. Убедитесь, что `subcommands` соответствует ожидаемым опциям автодополнения по табуляции, показываемым TUI.
  4. Если команда выполняется на стороне сервера, добавьте обработчик в `HermesCLI.process_command()` в `cli.py`:
[code] elif canonical == "commandname":  
             self._handle_commandname(cmd_original)  
         
[/code]
  5. Для команд, доступных через gateway, добавьте обработчик в `gateway/run.py`:
[code] if canonical == "commandname":  
             return await self._handle_commandname(event)  
         
[/code]


## Common Issues[​](<#common-issues> "Direct link to Common Issues")
  1. **Команда отображается в TUI, но не в автодополнении.** Команда определена в коде TUI, но отсутствует в `COMMAND_REGISTRY` в `hermes_cli/commands.py`. Данные автодополнения приходят из Python.
  2. **Команда отображается в автодополнении, но не работает.** Проверьте обработчик команды в `tui_gateway/server.py` и обработчик фронтенда в `ui-tui/src/app/createSlashHandler.ts`. Если команда является локальной в Ink, она должна обрабатываться в ветке `app.tsx` built-in; в противном случае она попадает в `slash.exec` и должна иметь обработчик на Python.
  3. **Поведение команды различается между CLI и TUI.** Возможно, у команды разные реализации. Проверьте оба — `cli.py::process_command` и локальный обработчик TUI. Локальные обработчики TUI имеют приоритет над диспетчеризацией через gateway.
  4. **Команда сохраняет конфигурацию, но не применяет изменения в реальном времени.** Для локальных команд TUI простого вызова `config.set` недостаточно. Также необходимо немедленно обновить соответствующее состояние nanostore (обычно через `patchUiState(...)`) и передать новое состояние через компоненты рендеринга. Пример: `/details collapsed` должен обновить видимость деталей в реальном времени, а не просто сохранить `details_mode`; глобальная `/details <mode>` в рамках сессии может потребовать отдельного флага переопределения команды, чтобы команды реального времени могли переопределять встроенные умолчания разделов, в то время как запуск/синхронизация конфигурации сохраняют стандартное поведение развёрнутых блоков thinking/tools.
  5. **Gateway-диспетчеризация молча игнорирует команду.** Gateway диспетчеризирует только известные ему команды. Проверьте, что `GATEWAY_KNOWN_COMMANDS` (формируется автоматически из `COMMAND_REGISTRY`) включает каноническое имя. Если команда `cli_only` с `gateway_config_gate`, убедитесь, что значение конфига для гейта истинно.


## Debugging Tactics[​](<#debugging-tactics> "Direct link to Debugging Tactics")
Когда поверхностная проверка не выявляет ошибку:
  * **Зависание или некорректное поведение на стороне Python:** используйте навык `python-debugpy` для остановки внутри `_SlashWorker.exec` или обработчика команды. `remote-pdb` на входе в обработчик — самый быстрый путь.
  * **Ink-сторона не реагирует:** используйте навык `node-inspect-debugger` для остановки в диспетчере слэш-команд `app.tsx` или в ветке локальной команды. `sb('dist/app.js', <line>)` после `npm run build`.
  * **Несоответствие реестра / неясно, какая сторона неверна:** сравните каноническую запись `COMMAND_REGISTRY` со списком локальных команд TUI бок о бок.


## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * Не забудьте указать правильную категорию для команды в `CommandDef` (например, "Session", "Configuration", "Tools & Skills", "Info", "Exit")
  * Убедитесь, что все псевдонимы правильно зарегистрированы в кортеже `aliases` — никаких других изменений в файлах не требуется, всё остальное (меню Telegram, отображение Slack, автодополнение, справка) формируется на основе этого
  * Для команд с подкомандами убедитесь, что кортеж `subcommands` в `CommandDef` соответствует тому, что указано в коде TUI
  * Команды с `cli_only=True` не будут работать на платформах gateway/мессенджеров — если только не добавлен `gateway_config_gate` и гейт не истинен
  * После добавления состояния живого UI проверьте всех потребителей старого свойства/помощника и пробросьте новое состояние через все пути рендеринга, а не только через активный поток. Рендеринг деталей TUI имеет как минимум два важных пути: живые `StreamingAssistant`/`ToolTrail` и строки `MessageLine` в стенограмме/ожидающие. Проход `/clean` должен явно проверять оба.
  * Пересоберите TUI (`npm --prefix ui-tui run build`) перед тестированием — режим наблюдения tsx может отставать при первом запуске


## Verification[​](<#verification> "Direct link to Verification")
После исправления:
  1. Пересоберите TUI:
[code] cd /home/bb/hermes-agent && npm --prefix ui-tui run build  
         
[/code]
  2. Запустите TUI и протестируйте команду:
[code] hermes --tui  
         
[/code]
  3. Введите `/` и убедитесь, что команда отображается в предложениях автодополнения с ожидаемым описанием и подсказкой аргументов.
  4. Выполните команду и подтвердите:
     * Ожидаемое поведение сработало
     * Любые сохранённые изменения конфигурации корректны (`read_file ~/.hermes/config.yaml`)
     * Состояние живого UI отражает изменения немедленно (а не только после перезапуска)
  5. Если команда также доступна через gateway, протестируйте её хотя бы с одной платформы мессенджеров (или запустите тесты gateway: `scripts/run_tests.sh tests/gateway/`).


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Overview](<#overview>)
  * [When to Use](<#when-to-use>)
  * [Architecture Overview](<#architecture-overview>)
  * [Investigation Steps](<#investigation-steps>)
  * [Fix: Missing Command Autocomplete](<#fix-missing-command-autocomplete>)
  * [Common Issues](<#common-issues>)
  * [Debugging Tactics](<#debugging-tactics>)
  * [Pitfalls](<#pitfalls>)
  * [Verification](<#verification>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-debugging-hermes-tui-commands -->
