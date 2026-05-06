На этой странице
MCP позволяет Hermes Agent подключаться к внешним серверам инструментов, чтобы агент мог использовать инструменты, находящиеся за пределами самого Hermes — GitHub, базы данных, файловые системы, браузерные стеки, внутренние API и многое другое.
Если вы когда-либо хотели, чтобы Hermes использовал инструмент, который уже существует где-то ещё, MCP обычно является самым чистым способом сделать это.
## Что даёт MCP[​](<#what-mcp-gives-you> "Прямая ссылка на Что даёт MCP")
  * Доступ к внешним экосистемам инструментов без необходимости сначала писать нативный инструмент Hermes
  * Локальные stdio-серверы и удалённые HTTP MCP-серверы в одной конфигурации
  * Автоматическое обнаружение и регистрация инструментов при запуске
  * Вспомогательные обёртки для ресурсов и промптов MCP, когда они поддерживаются сервером
  * Фильтрация по серверам, чтобы вы могли открыть для Hermes только те MCP-инструменты, которые действительно нужны

## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
  1. Установите поддержку MCP (уже включена, если вы использовали стандартный установочный скрипт):

[code] 
    cd ~/.hermes/hermes-agent  
    uv pip install -e ".[mcp]"  
    
[/code]
  2. Добавьте MCP-сервер в `~/.hermes/config.yaml`:

[code] 
    mcp_servers:  
      filesystem:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]  
    
[/code]
  3. Запустите Hermes:

[code] 
    hermes chat  
    
[/code]
  4. Попросите Hermes использовать возможности, предоставляемые MCP.

Например:
[code] 
    List the files in /home/user/projects and summarize the repo structure.  
    
[/code]
Hermes обнаружит инструменты MCP-сервера и будет использовать их как любые другие инструменты.
## Два вида MCP-серверов[​](<#two-kinds-of-mcp-servers> "Прямая ссылка на Два вида MCP-серверов")
### Stdio-серверы[​](<#stdio-servers> "Прямая ссылка на Stdio-серверы")
Stdio-серверы запускаются как локальные подпроцессы и общаются через stdin/stdout.
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
    
[/code]
Используйте stdio-серверы, когда:
  * сервер установлен локально
  * вам нужен низко-задержный доступ к локальным ресурсам
  * вы следуете документации MCP-сервера, где показаны `command`, `args` и `env`

### HTTP-серверы[​](<#http-servers> "Прямая ссылка на HTTP-серверы")
HTTP MCP-серверы — это удалённые endpoints, к которым Hermes подключается напрямую.
[code] 
    mcp_servers:  
      remote_api:  
        url: "https://mcp.example.com/mcp"  
        headers:  
          Authorization: "Bearer ***"  
    
[/code]
Используйте HTTP-серверы, когда:
  * MCP-сервер размещён где-то ещё
  * ваша организация предоставляет внутренние MCP-точки доступа
  * вы не хотите, чтобы Hermes запускал локальный подпроцесс для этой интеграции

## Основная конфигурация[​](<#basic-configuration-reference> "Прямая ссылка на Основная конфигурация")
Hermes читает конфигурацию MCP из `~/.hermes/config.yaml` в разделе `mcp_servers`.
### Общие ключи[​](<#common-keys> "Прямая ссылка на Общие ключи")
Ключ| Тип| Значение  
---|---|---  
`command`| string| Исполняемый файл для stdio MCP-сервера  
`args`| list| Аргументы для stdio-сервера  
`env`| mapping| Переменные окружения, передаваемые stdio-серверу  
`url`| string| HTTP MCP endpoint  
`headers`| mapping| HTTP-заголовки для удалённых серверов  
`timeout`| number| Таймаут вызова инструмента  
`connect_timeout`| number| Таймаут начального подключения  
`enabled`| bool| Если `false`, Hermes полностью пропускает сервер  
`tools`| mapping| Фильтрация инструментов и политика утилит для сервера  
### Минимальный пример stdio[​](<#minimal-stdio-example> "Прямая ссылка на Минимальный пример stdio")
[code] 
    mcp_servers:  
      filesystem:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]  
    
[/code]
### Минимальный пример HTTP[​](<#minimal-http-example> "Прямая ссылка на Минимальный пример HTTP")
[code] 
    mcp_servers:  
      company_api:  
        url: "https://mcp.internal.example.com"  
        headers:  
          Authorization: "Bearer ***"  
    
[/code]
## Как Hermes регистрирует MCP-инструменты[​](<#how-hermes-registers-mcp-tools> "Прямая ссылка на Как Hermes регистрирует MCP-инструменты")
Hermes добавляет префикс к MCP-инструментам, чтобы они не конфликтовали со встроенными именами:
[code] 
    mcp_<имя_сервера>_<имя_инструмента>  
    
[/code]
Примеры:
Сервер| MCP-инструмент| Зарегистрированное имя  
---|---|---  
`filesystem`| `read_file`| `mcp_filesystem_read_file`  
`github`| `create-issue`| `mcp_github_create_issue`  
`my-api`| `query.data`| `mcp_my_api_query_data`  
На практике вам обычно не нужно вызывать имя с префиксом вручную — Hermes видит инструмент и выбирает его во время обычного рассуждения.
## Утилиты MCP[​](<#mcp-utility-tools> "Прямая ссылка на Утилиты MCP")
Если поддерживается, Hermes также регистрирует вспомогательные инструменты для ресурсов и промптов MCP:
  * `list_resources`
  * `read_resource`
  * `list_prompts`
  * `get_prompt`

Они регистрируются для каждого сервера с тем же шаблоном префикса, например:
  * `mcp_github_list_resources`
  * `mcp_github_get_prompt`

### Важно[​](<#important> "Прямая ссылка на Важно")
Эти утилиты теперь учитывают возможности:
  * Hermes регистрирует утилиты ресурсов, только если сессия MCP действительно поддерживает операции с ресурсами
  * Hermes регистрирует утилиты промптов, только если сессия MCP действительно поддерживает операции с промптами

Таким образом, сервер, который предоставляет вызываемые инструменты, но не имеет ресурсов/промптов, не получит этих дополнительных обёрток.
## Фильтрация по серверам[​](<#per-server-filtering> "Прямая ссылка на Фильтрация по серверам")
Вы можете управлять тем, какие инструменты каждый MCP-сервер предоставляет Hermes, что позволяет тонко настраивать пространство имён инструментов.
### Полное отключение сервера[​](<#disable-a-server-entirely> "Прямая ссылка на Полное отключение сервера")
[code] 
    mcp_servers:  
      legacy:  
        url: "https://mcp.legacy.internal"  
        enabled: false  
    
[/code]
Если `enabled: false`, Hermes полностью пропускает сервер и даже не пытается установить соединение.
### Белый список инструментов сервера[​](<#whitelist-server-tools> "Прямая ссылка на Белый список инструментов сервера")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [create_issue, list_issues]  
    
[/code]
Регистрируются только указанные MCP-инструменты сервера.
### Чёрный список инструментов сервера[​](<#blacklist-server-tools> "Прямая ссылка на Чёрный список инструментов сервера")
[code] 
    mcp_servers:  
      stripe:  
        url: "https://mcp.stripe.com"  
        tools:  
          exclude: [delete_customer]  
    
[/code]
Все инструменты сервера регистрируются, кроме исключённых.
### Правило приоритета[​](<#precedence-rule> "Прямая ссылка на Правило приоритета")
Если указаны оба:
[code] 
    tools:  
      include: [create_issue]  
      exclude: [create_issue, delete_issue]  
    
[/code]
`include` побеждает.
### Фильтрация утилит тоже[​](<#filter-utility-tools-too> "Прямая ссылка на Фильтрация утилит тоже")
Вы также можете отдельно отключить добавленные Hermes вспомогательные обёртки:
[code] 
    mcp_servers:  
      docs:  
        url: "https://mcp.docs.example.com"  
        tools:  
          prompts: false  
          resources: false  
    
[/code]
Это означает:
  * `tools.resources: false` отключает `list_resources` и `read_resource`
  * `tools.prompts: false` отключает `list_prompts` и `get_prompt`

### Полный пример[​](<#full-example> "Прямая ссылка на Полный пример")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [create_issue, list_issues, search_code]  
          prompts: false  
      
      stripe:  
        url: "https://mcp.stripe.com"  
        headers:  
          Authorization: "Bearer ***"  
        tools:  
          exclude: [delete_customer]  
          resources: false  
      
      legacy:  
        url: "https://mcp.legacy.internal"  
        enabled: false  
    
[/code]
## Что будет, если всё отфильтровано?[​](<#what-happens-if-everything-is-filtered-out> "Прямая ссылка на Что будет, если всё отфильтровано?")
Если ваша конфигурация отфильтровывает все вызываемые инструменты и отключает или опускает все поддерживаемые утилиты, Hermes не создаёт пустой набор MCP-инструментов для этого сервера.
Это сохраняет список инструментов чистым.
## Поведение во время выполнения[​](<#runtime-behavior> "Прямая ссылка на Поведение во время выполнения")
### Время обнаружения[​](<#discovery-time> "Прямая ссылка на Время обнаружения")
Hermes обнаруживает MCP-серверы при запуске и регистрирует их инструменты в обычном реестре инструментов.
### Динамическое обнаружение инструментов[​](<#dynamic-tool-discovery> "Прямая ссылка на Динамическое обнаружение инструментов")
MCP-серверы могут уведомлять Hermes об изменении доступных инструментов во время выполнения, отправляя уведомление `notifications/tools/list_changed`. Когда Hermes получает это уведомление, он автоматически перезапрашивает список инструментов сервера и обновляет реестр — ручной `/reload-mcp` не требуется.
Это полезно для MCP-серверов, чьи возможности динамически меняются (например, сервер, который добавляет инструменты при загрузке новой схемы БД или удаляет инструменты, когда сервис становится недоступен).
Обновление защищено блокировкой, чтобы быстрые уведомления от одного и того же сервера не вызывали перекрывающиеся обновления. Уведомления об изменении промптов и ресурсов (`prompts/list_changed`, `resources/list_changed`) принимаются, но пока не обрабатываются.
### Перезагрузка[​](<#reloading> "Прямая ссылка на Перезагрузка")
Если вы изменили конфигурацию MCP, используйте:
[code] 
    /reload-mcp  
    
[/code]
Это перезагружает MCP-серверы из конфигурации и обновляет список доступных инструментов. Об изменениях инструментов во время выполнения, отправленных самим сервером, см. раздел [Динамическое обнаружение инструментов](<#dynamic-tool-discovery>) выше.
### Наборы инструментов[​](<#toolsets> "Прямая ссылка на Наборы инструментов")
Каждый настроенный MCP-сервер также создаёт набор инструментов во время выполнения, если он предоставляет хотя бы один зарегистрированный инструмент:
[code] 
    mcp-<сервер>  
    
[/code]
Это упрощает работу с MCP-серверами на уровне наборов инструментов.
## Модель безопасности[​](<#security-model> "Прямая ссылка на Модель безопасности")
### Фильтрация окружения stdio[​](<#stdio-env-filtering> "Прямая ссылка на Фильтрация окружения stdio")
Для stdio-серверов Hermes не передаёт слепо всё ваше shell-окружение.
Передаются только явно настроенные `env` плюс безопасный базовый набор. Это снижает риск случайной утечки секретов.
### Контроль доступа на уровне конфигурации[​](<#config-level-exposure-control> "Прямая ссылка на Контроль доступа на уровне конфигурации")
Новая поддержка фильтрации также является средством контроля безопасности:
  * отключайте опасные инструменты, которые вы не хотите показывать модели
  * открывайте только минимальный белый список для чувствительного сервера
  * отключайте обёртки ресурсов/промптов, если вы не хотите открывать эту поверхность

## Примеры использования[​](<#example-use-cases> "Прямая ссылка на Примеры использования")
### GitHub-сервер с минимальной поверхностью управления задачами[​](<#github-server-with-a-minimal-issue-management-surface> "Прямая ссылка на GitHub-сервер с минимальной поверхностью управления задачами")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [list_issues, create_issue, update_issue]  
          prompts: false  
          resources: false  
    
[/code]
Используйте так:
[code] 
    Show me open issues labeled bug, then draft a new issue for the flaky MCP reconnection behavior.  
    
[/code]
### Stripe-сервер с удалёнными опасными действиями[​](<#stripe-server-with-dangerous-actions-removed> "Прямая ссылка на Stripe-сервер с удалёнными опасными действиями")
[code] 
    mcp_servers:  
      stripe:  
        url: "https://mcp.stripe.com"  
        headers:  
          Authorization: "Bearer ***"  
        tools:  
          exclude: [delete_customer, refund_payment]  
    
[/code]
Используйте так:
[code] 
    Look up the last 10 failed payments and summarize common failure reasons.  
    
[/code]
### Файловый сервер для одного корня проекта[​](<#filesystem-server-for-a-single-project-root> "Прямая ссылка на Файловый сервер для одного корня проекта")
[code] 
    mcp_servers:  
      project_fs:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]  
    
[/code]
Используйте так:
[code] 
    Inspect the project root and explain the directory layout.  
    
[/code]
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")
### MCP-сервер не подключается[​](<#mcp-server-not-connecting> "Прямая ссылка на MCP-сервер не подключается")
Проверьте:
[code] 
    # Verify MCP deps are installed (already included in standard install)  
    cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"  
      
    node --version  
    npx --version  
    
[/code]
Затем проверьте вашу конфигурацию и перезапустите Hermes.
### Инструменты не появляются[​](<#tools-not-appearing> "Прямая ссылка на Инструменты не появляются")
Возможные причины:
  * сервер не смог подключиться
  * не удалось обнаружить инструменты
  * ваша конфигурация фильтрации исключила инструменты
  * возможность утилиты не существует на этом сервере
  * сервер отключён с помощью `enabled: false`

Если вы намеренно фильтруете, это ожидаемо.
### Почему утилиты ресурсов или промптов не появились?[​](<#why-didnt-resource-or-prompt-utilities-appear> "Прямая ссылка на Почему утилиты ресурсов или промптов не появились?")
Потому что теперь Hermes регистрирует эти обёртки только при выполнении обоих условий:
  1. ваша конфигурация разрешает их
  2. сессия сервера действительно поддерживает эту возможность

Это сделано намеренно и сохраняет список инструментов честным.
## Поддержка сэмплирования MCP[​](<#mcp-sampling-support> "Прямая ссылка на Поддержка сэмплирования MCP")
MCP-серверы могут запрашивать LLM-инференс у Hermes через протокол `sampling/createMessage`. Это позволяет MCP-серверу попросить Hermes сгенерировать текст от его имени — полезно для серверов, которым нужны LLM-возможности, но нет собственного доступа к модели.
Сэмплирование **включено по умолчанию** для всех MCP-серверов (когда MCP SDK это поддерживает). Настраивается для каждого сервера с помощью ключа `sampling`:
[code] 
    mcp_servers:  
      my_server:  
        command: "my-mcp-server"  
        sampling:  
          enabled: true            # Включить сэмплирование (по умолчанию: true)  
          model: "openai/gpt-4o"  # Переопределить модель для запросов сэмплирования (опционально)  
          max_tokens_cap: 4096     # Максимум токенов на один ответ сэмплирования (по умолчанию: 4096)  
          timeout: 30              # Таймаут в секундах на один запрос (по умолчанию: 30)  
          max_rpm: 10              # Лимит скорости: макс. запросов в минуту (по умолчанию: 10)  
          max_tool_rounds: 5       # Макс. раундов использования инструментов в циклах сэмплирования (по умолчанию: 5)  
          allowed_models: []       # Белый список имён моделей, которые сервер может запрашивать (пусто = любые)  
          log_level: "info"        # Уровень журнала аудита: debug, info или warning (по умолчанию: info)  
    
[/code]
Обработчик сэмплирования включает скользящий ограничитель скорости, таймауты на каждый запрос и ограничения глубины циклов инструментов для предотвращения неконтролируемого использования. Метрики (количество запросов, ошибки, использованные токены) отслеживаются для каждого экземпляра сервера.
Чтобы отключить сэмплирование для конкретного сервера:
[code] 
    mcp_servers:  
      untrusted_server:  
        url: "https://mcp.example.com"  
        sampling:  
          enabled: false  
    
[/code]
## Запуск Hermes как MCP-сервера[​](<#running-hermes-as-an-mcp-server> "Прямая ссылка на Запуск Hermes как MCP-сервера")
В дополнение к подключению **к** MCP-серверам, Hermes также может **быть** MCP-сервером. Это позволяет другим MCP-совместимым агентам (Claude Code, Cursor, Codex или любому MCP-клиенту) использовать возможности обмена сообщениями Hermes — просматривать беседы, читать историю сообщений и отправлять сообщения через все ваши подключённые платформы.
### Когда это использовать[​](<#when-to-use-this> "Прямая ссылка на Когда это использовать")
  * Вы хотите, чтобы Claude Code, Cursor или другой агент-кодировщик отправлял и читал сообщения Telegram/Discord/Slack через Hermes
  * Вы хотите один MCP-сервер, который объединяет все подключённые платформы обмена сообщениями Hermes
  * У вас уже есть работающий шлюз Hermes с подключёнными платформами

### Быстрый старт[​](<#quick-start-1> "Прямая ссылка на Быстрый старт")
[code] 
    hermes mcp serve  
    
[/code]
Это запускает stdio MCP-сервер. MCP-клиент (не вы) управляет жизненным циклом процесса.
### Конфигурация MCP-клиента[​](<#mcp-client-configuration> "Прямая ссылка на Конфигурация MCP-клиента")
Добавьте Hermes в конфигурацию вашего MCP-клиента. Например, в `~/.claude/claude_desktop_config.json` от Claude Code:
[code] 
    {  
      "mcpServers": {  
        "hermes": {  
          "command": "hermes",  
          "args": ["mcp", "serve"]  
        }  
      }  
    }  
    
[/code]
Или если вы установили Hermes в определённое место:
[code] 
    {  
      "mcpServers": {  
        "hermes": {  
          "command": "/home/user/.hermes/hermes-agent/venv/bin/hermes",  
          "args": ["mcp", "serve"]  
        }  
      }  
    }  
    
[/code]
### Доступные инструменты[​](<#available-tools> "Прямая ссылка на Доступные инструменты")
MCP-сервер предоставляет 10 инструментов, соответствующих поверхности моста каналов OpenClaw, плюс браузер каналов, специфичный для Hermes:
Инструмент| Описание  
---|---  
`conversations_list`| Список активных бесед обмена сообщениями. Фильтрация по платформе или поиск по имени.  
`conversation_get`| Получить подробную информацию об одной беседе по ключу сессии.  
`messages_read`| Прочитать недавнюю историю сообщений для беседы.  
`attachments_fetch`| Извлечь нетекстовые вложения (изображения, медиа) из конкретного сообщения.  
`events_poll`| Опрашивать новые события беседы с определённой позиции курсора.  
`events_wait`| Длинный опрос / блокировка до прибытия следующего события (почти реальное время).  
`messages_send`| Отправить сообщение через платформу (например, `telegram:123456`, `discord:#general`).  
`channels_list`| Список доступных целей обмена сообщениями на всех платформах.  
`permissions_list_open`| Список ожидающих запросов на одобрение, наблюдаемых во время сессии моста.  
`permissions_respond`| Разрешить или отклонить ожидающий запрос на одобрение.  
### Система событий[​](<#event-system> "Прямая ссылка на Система событий")
MCP-сервер включает живой мост событий, который опрашивает базу сессий Hermes на предмет новых сообщений. Это даёт MCP-клиентам осведомлённость о входящих беседах почти в реальном времени:
[code] 
    # Poll for new events (non-blocking)  
    events_poll(after_cursor=0)  
      
    # Wait for next event (blocks up to timeout)  
    events_wait(after_cursor=42, timeout_ms=30000)  
    
[/code]
Типы событий: `message`, `approval_requested`, `approval_resolved`
Очередь событий находится в памяти и запускается при подключении моста. Более старые сообщения доступны через `messages_read`.
### Параметры[​](<#options> "Прямая ссылка на Параметры")
[code] 
    hermes mcp serve              # Обычный режим  
    hermes mcp serve --verbose    # Отладочный вывод в stderr  
    
[/code]
### Как это работает[​](<#how-it-works> "Прямая ссылка на Как это работает")
MCP-сервер читает данные бесед напрямую из хранилища сессий Hermes (`~/.hermes/sessions/sessions.json` и базы данных SQLite). Фоновый поток опрашивает базу данных на предмет новых сообщений и поддерживает очередь событий в памяти. Для отправки сообщений используется та же инфраструктура `send_message`, что и у самого агента Hermes.
Шлюз НЕ должен быть запущен для операций чтения (список бесед, чтение истории, опрос событий). Он ДОЛЖЕН быть запущен для операций отправки, так как адаптерам платформ нужны активные соединения.
### Текущие ограничения[​](<#current-limits> "Прямая ссылка на Текущие ограничения")
  * Только stdio-транспорт (транспорт HTTP MCP пока отсутствует)
  * Опрос событий с интервалом ~200 мс через оптимизированный по mtime опрос БД (пропускает работу, когда файлы не изменялись)
  * Протокол push-уведомлений `claude/channel` пока отсутствует
  * Только текстовая отправка (нет отправки медиа/вложений через `messages_send`)

## Связанная документация[​](<#related-docs> "Прямая ссылка на Связанная документация")
  * [Использование MCP с Hermes](</docs/guides/use-mcp-with-hermes>)
  * [Команды CLI](</docs/reference/cli-commands>)
  * [Слэш-команды](</docs/reference/slash-commands>)
  * [Часто задаваемые вопросы](</docs/reference/faq>)

  * [Что даёт MCP](<#what-mcp-gives-you>)
  * [Быстрый старт](<#quick-start>)
  * [Два вида MCP-серверов](<#two-kinds-of-mcp-servers>)
    * [Stdio-серверы](<#stdio-servers>)
    * [HTTP-серверы](<#http-servers>)
  * [Основная конфигурация](<#basic-configuration-reference>)
    * [Общие ключи](<#common-keys>)
    * [Минимальный пример stdio](<#minimal-stdio-example>)
    * [Минимальный пример HTTP](<#minimal-http-example>)
  * [Как Hermes регистрирует MCP-инструменты](<#how-hermes-registers-mcp-tools>)
  * [Утилиты MCP](<#mcp-utility-tools>)
    * [Важно](<#important>)
  * [Фильтрация по серверам](<#per-server-filtering>)
    * [Полное отключение сервера](<#disable-a-server-entirely>)
    * [Белый список инструментов сервера](<#whitelist-server-tools>)
    * [Чёрный список инструментов сервера](<#blacklist-server-tools>)
    * [Правило приоритета](<#precedence-rule>)
    * [Фильтрация утилит тоже](<#filter-utility-tools-too>)
    * [Полный пример](<#full-example>)
  * [Что будет, если всё отфильтровано?](<#what-happens-if-everything-is-filtered-out>)
  * [Поведение во время выполнения](<#runtime-behavior>)
    * [Время обнаружения](<#discovery-time>)
    * [Динамическое обнаружение инструментов](<#dynamic-tool-discovery>)
    * [Перезагрузка](<#reloading>)
    * [Наборы инструментов](<#toolsets>)
  * [Модель безопасности](<#security-model>)
    * [Фильтрация окружения stdio](<#stdio-env-filtering>)
    * [Контроль доступа на уровне конфигурации](<#config-level-exposure-control>)
  * [Примеры использования](<#example-use-cases>)
    * [GitHub-сервер с минимальной поверхностью управления задачами](<#github-server-with-a-minimal-issue-management-surface>)
    * [Stripe-сервер с удалёнными опасными действиями](<#stripe-server-with-dangerous-actions-removed>)
    * [Файловый сервер для одного корня проекта](<#filesystem-server-for-a-single-project-root>)
  * [Устранение неполадок](<#troubleshooting>)
    * [MCP-сервер не подключается](<#mcp-server-not-connecting>)
    * [Инструменты не появляются](<#tools-not-appearing>)
    * [Почему утилиты ресурсов или промптов не появились?](<#why-didnt-resource-or-prompt-utilities-appear>)
  * [Поддержка сэмплирования MCP](<#mcp-sampling-support>)
  * [Запуск Hermes как MCP-сервера](<#running-hermes-as-an-mcp-server>)
    * [Когда это использовать](<#when-to-use-this>)
    * [Быстрый старт](<#quick-start-1>)
    * [Конфигурация MCP-клиента](<#mcp-client-configuration>)
    * [Доступные инструменты](<#available-tools>)
    * [Система событий](<#event-system>)
    * [Параметры](<#options>)
    * [Как это работает](<#how-it-works>)
    * [Текущие ограничения](<#current-limits>)
  * [Связанная документация](<#related-docs>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp -->
