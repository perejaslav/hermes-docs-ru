On this page

Эта страница — компактный справочник, дополняющий основную документацию по MCP.
Для концептуального руководства см.:
  * [MCP (Model Context Protocol)](</docs/user-guide/features/mcp>)
  * [Использование MCP с Hermes](</docs/guides/use-mcp-with-hermes>)

## Формат корневой конфигурации[​](<#root-config-shape> "Прямая ссылка на Формат корневой конфигурации")

[code]
    mcp_servers:
      <server_name>:
        command: "..."      # stdio-серверы
        args: []
        env: {}

        # ИЛИ
        url: "..."          # HTTP-серверы
        headers: {}

        enabled: true
        timeout: 120
        connect_timeout: 60
        tools:
          include: []
          exclude: []
          resources: true
          prompts: true

[/code]

## Ключи сервера[​](<#server-keys> "Прямая ссылка на Ключи сервера")

Ключ| Тип| Применяется к| Значение
---|---|---|---
`command`| string| stdio| Исполняемый файл для запуска
`args`| list| stdio| Аргументы для подпроцесса
`env`| mapping| stdio| Переменные окружения для подпроцесса
`url`| string| HTTP| Удалённая MCP-точка
`headers`| mapping| HTTP| Заголовки для запросов к удалённому серверу
`enabled`| bool| оба| Полностью пропустить сервер, если false
`timeout`| number| оба| Тайм-аут вызова инструмента
`connect_timeout`| number| оба| Тайм-аут начального подключения
`tools`| mapping| оба| Политика фильтрации и служебных инструментов
`auth`| string| HTTP| Метод аутентификации. Установите `oauth` для включения OAuth 2.1 с PKCE
`sampling`| mapping| оба| Политика LLM-запросов, инициированных сервером (см. руководство по MCP)

## Ключи политики `tools`[​](<#tools-policy-keys> "Прямая ссылка на Ключи политики tools")

Ключ| Тип| Значение
---|---|---
`include`| string или list| Белый список родных MCP-инструментов сервера
`exclude`| string или list| Чёрный список родных MCP-инструментов сервера
`resources`| bool-like| Включение/отключение `list_resources` + `read_resource`
`prompts`| bool-like| Включение/отключение `list_prompts` + `get_prompt`

## Семантика фильтрации[​](<#filtering-semantics> "Прямая ссылка на Семантика фильтрации")

### `include`[​](<#include> "Прямая ссылка на include")

Если `include` задан, регистрируются только указанные родные MCP-инструменты сервера.

[code]
    tools:
      include: [create_issue, list_issues]

[/code]

### `exclude`[​](<#exclude> "Прямая ссылка на exclude")

Если задан `exclude`, а `include` — нет, регистрируются все родные MCP-инструменты сервера, кроме указанных.

[code]
    tools:
      exclude: [delete_customer]

[/code]

### Приоритет[​](<#precedence> "Прямая ссылка на Приоритет")

Если заданы оба параметра, приоритет у `include`.

[code]
    tools:
      include: [create_issue]
      exclude: [create_issue, delete_issue]

[/code]

Результат:

* `create_issue` всё равно разрешён
* `delete_issue` игнорируется, так как `include` имеет приоритет

## Политика служебных инструментов[​](<#utility-tool-policy> "Прямая ссылка на Политика служебных инструментов")

Hermes может регистрировать следующие служебные обёртки для каждого MCP-сервера:

Ресурсы:

* `list_resources`
* `read_resource`

Промпты:

* `list_prompts`
* `get_prompt`

### Отключение ресурсов[​](<#disable-resources> "Прямая ссылка на Отключение ресурсов")

[code]
    tools:
      resources: false

[/code]

### Отключение промптов[​](<#disable-prompts> "Прямая ссылка на Отключение промптов")

[code]
    tools:
      prompts: false

[/code]

### Регистрация с учётом возможностей[​](<#capability-aware-registration> "Прямая ссылка на Регистрация с учётом возможностей")

Даже при `resources: true` или `prompts: true` Hermes регистрирует эти служебные инструменты только в том случае, если MCP-сессия действительно предоставляет соответствующую возможность.

Поэтому это нормально:

* вы включаете промпты,
* но служебные инструменты для промптов не появляются,
* потому что сервер не поддерживает промпты.

## `enabled: false`[​](<#enabled-false> "Прямая ссылка на enabled: false")

[code]
    mcp_servers:
      legacy:
        url: "https://mcp.legacy.internal"
        enabled: false

[/code]

Поведение:

* нет попытки подключения
* нет обнаружения
* нет регистрации инструментов
* конфигурация остаётся на месте для последующего использования

## Поведение при пустом результате[​](<#empty-result-behavior> "Прямая ссылка на Поведение при пустом результате")

Если фильтрация удаляет все родные инструменты сервера и не зарегистрировано ни одного служебного инструмента, Hermes не создаёт пустой набор MCP-инструментов для этого сервера.

## Примеры конфигураций[​](<#example-configs> "Прямая ссылка на Примеры конфигураций")

### Безопасный белый список для GitHub[​](<#safe-github-allowlist> "Прямая ссылка на Безопасный белый список для GitHub")

[code]
    mcp_servers:
      github:
        command: "npx"
        args: ["-y", "@modelcontextprotocol/server-github"]
        env:
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"
        tools:
          include: [list_issues, create_issue, update_issue, search_code]
          resources: false
          prompts: false

[/code]

### Чёрный список для Stripe[​](<#stripe-blacklist> "Прямая ссылка на Чёрный список для Stripe")

[code]
    mcp_servers:
      stripe:
        url: "https://mcp.stripe.com"
        headers:
          Authorization: "Bearer ***"
        tools:
          exclude: [delete_customer, refund_payment]

[/code]

### Сервер документации только с ресурсами[​](<#resource-only-docs-server> "Прямая ссылка на Сервер документации только с ресурсами")

[code]
    mcp_servers:
      docs:
        url: "https://mcp.docs.example.com"
        tools:
          include: []
          resources: true
          prompts: false

[/code]

## Перезагрузка конфигурации[​](<#reloading-config> "Прямая ссылка на Перезагрузка конфигурации")

После изменения конфигурации MCP перезагрузите серверы командой:

[code]
    /reload-mcp

[/code]

## Именование инструментов[​](<#tool-naming> "Прямая ссылка на Именование инструментов")

Родные MCP-инструменты сервера становятся:

[code]
    mcp_<server>_<tool>

[/code]

Примеры:

* `mcp_github_create_issue`
* `mcp_filesystem_read_file`
* `mcp_my_api_query_data`

Служебные инструменты следуют тому же шаблону префикса:

* `mcp_<server>_list_resources`
* `mcp_<server>_read_resource`
* `mcp_<server>_list_prompts`
* `mcp_<server>_get_prompt`

### Санитизация имён[​](<#name-sanitization> "Прямая ссылка на Санитизация имён")

Дефисы (`-`) и точки (`.`) в именах серверов и инструментов заменяются на подчёркивания перед регистрацией. Это гарантирует, что имена инструментов будут допустимыми идентификаторами для API вызова функций LLM.

Например, сервер с именем `my-api`, предоставляющий инструмент `list-items.v2`, становится:

[code]
    mcp_my_api_list_items_v2

[/code]

Учитывайте это при написании фильтров `include` / `exclude` — используйте **оригинальное** имя MCP-инструмента (с дефисами/точками), а не санитизированную версию.

## Аутентификация OAuth 2.1[​](<#oauth-21-authentication> "Прямая ссылка на Аутентификация OAuth 2.1")

Для HTTP-серверов, требующих OAuth, укажите `auth: oauth` в записи сервера:

[code]
    mcp_servers:
      protected_api:
        url: "https://mcp.example.com/mcp"
        auth: oauth

[/code]

Поведение:

* Hermes использует OAuth 2.1 PKCE flow из MCP SDK (обнаружение метаданных, динамическая регистрация клиента, обмен токенами и обновление)
* При первом подключении открывается окно браузера для авторизации
* Токены сохраняются в `~/.hermes/mcp-tokens/<server>.json` и используются повторно между сессиями
* Обновление токенов происходит автоматически; повторная авторизация требуется только при сбое обновления
* Применяется только к транспорту HTTP/StreamableHTTP (серверы на основе `url`)

* [Формат корневой конфигурации](<#root-config-shape>)
* [Ключи сервера](<#server-keys>)
* [Ключи политики `tools`](<#tools-policy-keys>)
* [Семантика фильтрации](<#filtering-semantics>)
  * [`include`](<#include>)
  * [`exclude`](<#exclude>)
  * [Приоритет](<#precedence>)
* [Политика служебных инструментов](<#utility-tool-policy>)
  * [Отключение ресурсов](<#disable-resources>)
  * [Отключение промптов](<#disable-prompts>)
  * [Регистрация с учётом возможностей](<#capability-aware-registration>)
* [`enabled: false`](<#enabled-false>)
* [Поведение при пустом результате](<#empty-result-behavior>)
* [Примеры конфигураций](<#example-configs>)
  * [Безопасный белый список для GitHub](<#safe-github-allowlist>)
  * [Чёрный список для Stripe](<#stripe-blacklist>)
  * [Сервер документации только с ресурсами](<#resource-only-docs-server>)
* [Перезагрузка конфигурации](<#reloading-config>)
* [Именование инструментов](<#tool-naming>)
  * [Санитизация имён](<#name-sanitization>)
* [Аутентификация OAuth 2.1](<#oauth-21-authentication>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference -->
