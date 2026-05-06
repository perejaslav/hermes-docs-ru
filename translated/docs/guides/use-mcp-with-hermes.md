On this page
Это руководство показывает, как использовать MCP с Hermes Agent в повседневной работе.
Если на странице описания функции объясняется, что такое MCP, то это руководство — о том, как быстро и безопасно получить от него пользу.
## Когда следует использовать MCP?[​](<#when-should-you-use-mcp> "Прямая ссылка на «Когда следует использовать MCP?»")
Используйте MCP, когда:
  * инструмент уже существует в виде MCP, и вы не хотите создавать нативный инструмент Hermes
  * вы хотите, чтобы Hermes работал с локальной или удалённой системой через чистый слой RPC
  * вам нужен тонкий контроль над видимостью каждого сервера
  * вы хотите подключить Hermes к внутренним API, базам данных или корпоративным системам без изменения ядра Hermes


Не используйте MCP, когда:
  * встроенный инструмент Hermes уже хорошо решает задачу
  * сервер предоставляет огромную опасную поверхность инструментов, и вы не готовы её фильтровать
  * вам нужна только одна узкая интеграция, и нативный инструмент был бы проще и безопаснее


## Ментальная модель[​](<#mental-model> "Прямая ссылка на «Ментальная модель»")
Воспринимайте MCP как уровень адаптации:
  * Hermes остаётся агентом
  * MCP-серверы предоставляют инструменты
  * Hermes обнаруживает эти инструменты при запуске или перезагрузке
  * модель может использовать их как обычные инструменты
  * вы контролируете, какая часть каждого сервера видна


Последний пункт важен. Хорошее использование MCP — это не просто «подключить всё». Это «подключить то, что нужно, с минимальной полезной поверхностью воздействия».
## Шаг 1: установите поддержку MCP[​](<#step-1-install-mcp-support> "Прямая ссылка на «Шаг 1: установите поддержку MCP»")
Если вы установили Hermes стандартным скриптом, поддержка MCP уже включена (установщик выполняет `uv pip install -e ".[all]"`).
Если вы установили без дополнительных пакетов и хотите добавить MCP отдельно:
[code] 
    cd ~/.hermes/hermes-agent  
    uv pip install -e ".[mcp]"  
    
[/code]
Для серверов на основе npm убедитесь, что Node.js и `npx` доступны.
Для многих MCP-серверов на Python `uvx` является удобным вариантом по умолчанию.
## Шаг 2: сначала добавьте один сервер[​](<#step-2-add-one-server-first> "Прямая ссылка на «Шаг 2: сначала добавьте один сервер»")
Начните с одного безопасного сервера.
Пример: доступ к файловой системе только для одного каталога проекта.
[code] 
    mcp_servers:  
      project_fs:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]  
    
[/code]
Затем запустите Hermes:
[code] 
    hermes chat  
    
[/code]
Теперь задайте что-нибудь конкретное:
[code] 
    Inspect this project and summarize the repo layout.  
    
[/code]
## Шаг 3: проверьте загрузку MCP[​](<#step-3-verify-mcp-loaded> "Прямая ссылка на «Шаг 3: проверьте загрузку MCP»")
Проверить загрузку MCP можно несколькими способами:
  * баннер/статус Hermes должен показывать интеграцию MCP при наличии конфигурации
  * спросите у Hermes, какие инструменты доступны
  * используйте `/reload-mcp` после изменений конфигурации
  * проверьте логи, если сервер не подключился


Практический тестовый запрос:
[code] 
    Tell me which MCP-backed tools are available right now.  
    
[/code]
## Шаг 4: начинайте фильтрацию немедленно[​](<#step-4-start-filtering-immediately> "Прямая ссылка на «Шаг 4: начинайте фильтрацию немедленно»")
Не откладывайте, если сервер предоставляет много инструментов.
### Пример: разрешите только то, что нужно[​](<#example-whitelist-only-what-you-want> "Прямая ссылка на «Пример: разрешите только то, что нужно»")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [list_issues, create_issue, search_code]  
    
[/code]
Это обычно лучший вариант по умолчанию для чувствительных систем.
## WSL2: мост Hermes в WSL к Chrome на Windows[​](<#wsl2-bridge-hermes-in-wsl-to-windows-chrome> "Прямая ссылка на «WSL2: мост Hermes в WSL к Chrome на Windows»")
Это практическая настройка, когда:
  * Hermes запущен внутри WSL2
  * браузер, которым вы хотите управлять, — это ваш обычный Chrome на Windows, где вы авторизованы
  * `/browser connect` неудобен или ненадёжен из WSL


В такой настройке Hermes **не** подключается к Chrome напрямую. Вместо этого:
  * Hermes запущен в WSL
  * Hermes запускает локальный MCP-сервер через stdio
  * этот MCP-сервер запускается через механизм взаимодействия с Windows (`cmd.exe` или `powershell.exe`)
  * MCP-сервер подключается к вашему активному сеансу Chrome в Windows


Ментальная модель:
[code] 
    Hermes (WSL) -> MCP stdio bridge -> Windows Chrome  
    
[/code]
### Зачем нужен этот режим[​](<#why-this-mode-is-useful> "Прямая ссылка на «Зачем нужен этот режим»")
  * сохраняется ваш реальный профиль браузера Windows, куки и логины
  * Hermes остаётся в поддерживаемой среде Unix (WSL2)
  * управление браузером предоставляется через MCP-инструменты вместо использования встроенного транспортного механизма Hermes


### Рекомендуемый сервер[​](<#recommended-server> "Прямая ссылка на «Рекомендуемый сервер»")
Используйте `chrome-devtools-mcp`.
Если в вашем Chrome на Windows уже включена удалённая отладка через `chrome://inspect/#remote-debugging`, добавьте его из WSL следующим образом:
[code] 
    hermes mcp add chrome-devtools-win --command cmd.exe --args /c "npx -y chrome-devtools-mcp@latest --autoConnect --no-usage-statistics"  
    
[/code]
После сохранения сервера:
[code] 
    hermes mcp test chrome-devtools-win  
    
[/code]
Затем запустите новый сеанс Hermes или выполните:
[code] 
    /reload-mcp  
    
[/code]
### Типичный запрос[​](<#typical-prompt> "Прямая ссылка на «Типичный запрос»")
После загрузки Hermes может напрямую использовать MCP-инструменты для браузера. Например:
[code] 
    调用 MCP 工具 mcp_chrome_devtools_win_list_pages，列出当前浏览器标签页。  
    
[/code]
### Когда `/browser connect` — неподходящий инструмент[​](<#when-browser-connect-is-the-wrong-tool> "Прямая ссылка на «Когда /browser connect — неподходящий инструмент»")
Если Hermes работает в WSL, а Chrome — на Windows, `/browser connect` может не работать, даже если Chrome открыт и доступен для отладки.
Распространённые причины:
  * WSL не может подключиться к той же локальной конечной точке, которую Chrome предоставляет инструментам Windows
  * новые механизмы отладки Chrome отличаются от классического `ws://localhost:9222`
  * к браузеру проще подключиться через вспомогательный инструмент на стороне Windows, например `chrome-devtools-mcp`


В таких случаях оставьте `/browser connect` для сценариев в одной среде и используйте MCP для связи WSL с браузером Windows.
### Известные проблемы[​](<#known-pitfalls> "Прямая ссылка на «Известные проблемы»")
  * Запускайте Hermes из каталога, смонтированного в Windows, например `/mnt/c/Users/<you>` или `/mnt/c/workspace/...`, при использовании исполняемых файлов Windows через MCP через stdio.
  * Если запустить Hermes из `/root` или `/home/...`, Windows может выдать предупреждение о текущем каталоге UNC перед запуском MCP-сервера.
  * Если `chrome-devtools-mcp --autoConnect` зависает при перечислении страниц, уменьшите количество фоновых/замороженных вкладок в Chrome и повторите попытку.


### Пример: заблокируйте опасные действия[​](<#example-blacklist-dangerous-actions> "Прямая ссылка на «Пример: заблокируйте опасные действия»")
[code] 
    mcp_servers:  
      stripe:  
        url: "https://mcp.stripe.com"  
        headers:  
          Authorization: "Bearer ***"  
        tools:  
          exclude: [delete_customer, refund_payment]  
    
[/code]
### Пример: отключите вспомогательные обёртки[​](<#example-disable-utility-wrappers-too> "Прямая ссылка на «Пример: отключите вспомогательные обёртки»")
[code] 
    mcp_servers:  
      docs:  
        url: "https://mcp.docs.example.com"  
        tools:  
          prompts: false  
          resources: false  
    
[/code]
## Что именно фильтруется?[​](<#what-does-filtering-actually-affect> "Прямая ссылка на «Что именно фильтруется?»")
В Hermes есть две категории функциональности, предоставляемой через MCP:
  1. Собственные MCP-инструменты сервера


  * фильтруются с помощью:
    * `tools.include`
    * `tools.exclude`


  2. Вспомогательные обёртки, добавляемые Hermes


  * фильтруются с помощью:
    * `tools.resources`
    * `tools.prompts`


### Вспомогательные обёртки, которые вы можете увидеть[​](<#utility-wrappers-you-may-see> "Прямая ссылка на «Вспомогательные обёртки, которые вы можете увидеть»")
Ресурсы:
  * `list_resources`
  * `read_resource`


Промпты:
  * `list_prompts`
  * `get_prompt`


Эти обёртки появляются только если:
  * ваша конфигурация их разрешает, и
  * сеанс MCP-сервера действительно поддерживает эти возможности


Таким образом, Hermes не будет делать вид, что у сервера есть ресурсы/промпты, если их нет.
## Типовые сценарии[​](<#common-patterns> "Прямая ссылка на «Типовые сценарии»")
### Сценарий 1: локальный помощник по проекту[​](<#pattern-1-local-project-assistant> "Прямая ссылка на «Сценарий 1: локальный помощник по проекту»")
Используйте MCP для файловой системы или git-сервера, ограниченного репозиторием, когда хотите, чтобы Hermes оперировал в пределах ограниченной рабочей области.
[code] 
    mcp_servers:  
      fs:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]  
      
      git:  
        command: "uvx"  
        args: ["mcp-server-git", "--repository", "/home/user/project"]  
    
[/code]
Хорошие запросы:
[code] 
    Review the project structure and identify where configuration lives.  
    
[/code]
[code] 
    Check the local git state and summarize what changed recently.  
    
[/code]
### Сценарий 2: помощник для сортировки задач GitHub[​](<#pattern-2-github-triage-assistant> "Прямая ссылка на «Сценарий 2: помощник для сортировки задач GitHub»")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [list_issues, create_issue, update_issue, search_code]  
          prompts: false  
          resources: false  
    
[/code]
Хорошие запросы:
[code] 
    List open issues about MCP, cluster them by theme, and draft a high-quality issue for the most common bug.  
    
[/code]
[code] 
    Search the repo for uses of _discover_and_register_server and explain how MCP tools are registered.  
    
[/code]
### Сценарий 3: помощник для внутреннего API[​](<#pattern-3-internal-api-assistant> "Прямая ссылка на «Сценарий 3: помощник для внутреннего API»")
[code] 
    mcp_servers:  
      internal_api:  
        url: "https://mcp.internal.example.com"  
        headers:  
          Authorization: "Bearer ***"  
        tools:  
          include: [list_customers, get_customer, list_invoices]  
          resources: false  
          prompts: false  
    
[/code]
Хорошие запросы:
[code] 
    Look up customer ACME Corp and summarize recent invoice activity.  
    
[/code]
Это как раз тот случай, когда строгий белый список намного лучше списка исключений.
### Сценарий 4: серверы документации и знаний[​](<#pattern-4-documentation--knowledge-servers> "Прямая ссылка на «Сценарий 4: серверы документации и знаний»")
Некоторые MCP-серверы предоставляют промпты или ресурсы, которые больше похожи на общие активы знаний, чем на прямые действия.
[code] 
    mcp_servers:  
      docs:  
        url: "https://mcp.docs.example.com"  
        tools:  
          prompts: true  
          resources: true  
    
[/code]
Хорошие запросы:
[code] 
    List available MCP resources from the docs server, then read the onboarding guide and summarize it.  
    
[/code]
[code] 
    List prompts exposed by the docs server and tell me which ones would help with incident response.  
    
[/code]
## Учебный пример: сквозная настройка с фильтрацией[​](<#tutorial-end-to-end-setup-with-filtering> "Прямая ссылка на «Учебный пример: сквозная настройка с фильтрацией»")
Вот практическая последовательность действий.
### Этап 1: добавьте GitHub MCP с жёстким белым списком[​](<#phase-1-add-github-mcp-with-a-tight-whitelist> "Прямая ссылка на «Этап 1: добавьте GitHub MCP с жёстким белым списком»")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [list_issues, create_issue, search_code]  
          prompts: false  
          resources: false  
    
[/code]
Запустите Hermes и спросите:
[code] 
    Search the codebase for references to MCP and summarize the main integration points.  
    
[/code]
### Этап 2: расширяйте только по необходимости[​](<#phase-2-expand-only-when-needed> "Прямая ссылка на «Этап 2: расширяйте только по необходимости»")
Если позже понадобится обновление задач:
[code] 
    tools:  
      include: [list_issues, create_issue, update_issue, search_code]  
    
[/code]
Затем перезагрузите:
[code] 
    /reload-mcp  
    
[/code]
### Этап 3: добавьте второй сервер с другой политикой[​](<#phase-3-add-a-second-server-with-different-policy> "Прямая ссылка на «Этап 3: добавьте второй сервер с другой политикой»")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "***"  
        tools:  
          include: [list_issues, create_issue, update_issue, search_code]  
          prompts: false  
          resources: false  
      
      filesystem:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]  
    
[/code]
Теперь Hermes может комбинировать их:
[code] 
    Inspect the local project files, then create a GitHub issue summarizing the bug you find.  
    
[/code]
Вот где MCP становится мощным: многосистемные рабочие процессы без изменения ядра Hermes.
## Рекомендации по безопасному использованию[​](<#safe-usage-recommendations> "Прямая ссылка на «Рекомендации по безопасному использованию»")
### Для опасных систем предпочитайте белые списки[​](<#prefer-allowlists-for-dangerous-systems> "Прямая ссылка на «Для опасных систем предпочитайте белые списки»")
Для всего, что связано с финансами, клиентами или разрушительными действиями:
  * используйте `tools.include`
  * начинайте с минимально возможного набора


### Отключайте неиспользуемые утилиты[​](<#disable-unused-utilities> "Прямая ссылка на «Отключайте неиспользуемые утилиты»")
Если вы не хотите, чтобы модель просматривала предоставляемые сервером ресурсы/промпты, отключите их:
[code] 
    tools:  
      resources: false  
      prompts: false  
    
[/code]
### Ограничивайте область действия серверов[​](<#keep-servers-scoped-narrowly> "Прямая ссылка на «Ограничивайте область действия серверов»")
Примеры:
  * файловый сервер, ограниченный одним каталогом проекта, а не всей домашней директорией
  * git-сервер, указывающий на один репозиторий
  * сервер внутреннего API с преимущественно read-доступом по умолчанию


### Перезагружайте после изменений конфигурации[​](<#reload-after-config-changes> "Прямая ссылка на «Перезагружайте после изменений конфигурации»")
[code] 
    /reload-mcp  
    
[/code]
Делайте это после изменения:
  * списков include/exclude
  * флагов enabled
  * переключателей resources/prompts
  * заголовков аутентификации / переменных окружения


## Устранение неполадок по симптомам[​](<#troubleshooting-by-symptom> "Прямая ссылка на «Устранение неполадок по симптомам»")
### «Сервер подключается, но ожидаемые инструменты отсутствуют»[​](<#the-server-connects-but-the-tools-i-expected-are-missing> "Прямая ссылка на «Сервер подключается, но ожидаемые инструменты отсутствуют»")
Возможные причины:
  * отфильтровано через `tools.include`
  * исключено через `tools.exclude`
  * вспомогательные обёртки отключены через `resources: false` или `prompts: false`
  * сервер на самом деле не поддерживает ресурсы/промпты


### «Сервер настроен, но ничего не загружается»[​](<#the-server-is-configured-but-nothing-loads> "Прямая ссылка на «Сервер настроен, но ничего не загружается»")
Проверьте:
  * не осталось ли в конфигурации `enabled: false`
  * существует ли команда/среда выполнения (`npx`, `uvx` и т.д.)
  * доступна ли HTTP-конечная точка
  * правильны ли переменные окружения аутентификации или заголовки


### «Почему я вижу меньше инструментов, чем рекламирует MCP-сервер?»[​](<#why-do-i-see-fewer-tools-than-the-mcp-server-advertises> "Прямая ссылка на «Почему я вижу меньше инструментов, чем рекламирует MCP-сервер?»")
Потому что Hermes теперь соблюдает вашу политику на сервер и регистрацию с учётом возможностей. Это ожидаемо и, как правило, желательно.
### «Как удалить MCP-сервер без удаления конфигурации?»[​](<#how-do-i-remove-an-mcp-server-without-deleting-the-config> "Прямая ссылка на «Как удалить MCP-сервер без удаления конфигурации?»")
Используйте:
[code] 
    enabled: false  
    
[/code]
Это сохраняет конфигурацию, но предотвращает подключение и регистрацию.
## Рекомендуемые первые MCP-настройки[​](<#recommended-first-mcp-setups> "Прямая ссылка на «Рекомендуемые первые MCP-настройки»")
Хорошие первые серверы для большинства пользователей:
  * filesystem
  * git
  * GitHub
  * fetch / серверы документации MCP
  * один узкий внутренний API


Не очень хорошие первые серверы:
  * огромные бизнес-системы с множеством разрушительных действий и без фильтрации
  * всё, что вы недостаточно хорошо понимаете, чтобы ограничивать


## Связанные материалы[​](<#related-docs> "Прямая ссылка на «Связанные материалы»")
  * [MCP (Model Context Protocol)](</docs/user-guide/features/mcp>)
  * [FAQ](</docs/reference/faq>)
  * [Слэш-команды](</docs/reference/slash-commands>)


  * [Когда следует использовать MCP?](<#when-should-you-use-mcp>)
  * [Ментальная модель](<#mental-model>)
  * [Шаг 1: установите поддержку MCP](<#step-1-install-mcp-support>)
  * [Шаг 2: сначала добавьте один сервер](<#step-2-add-one-server-first>)
  * [Шаг 3: проверьте загрузку MCP](<#step-3-verify-mcp-loaded>)
  * [Шаг 4: начинайте фильтрацию немедленно](<#step-4-start-filtering-immediately>)
    * [Пример: разрешите только то, что нужно](<#example-whitelist-only-what-you-want>)
  * [WSL2: мост Hermes в WSL к Chrome на Windows](<#wsl2-bridge-hermes-in-wsl-to-windows-chrome>)
    * [Зачем нужен этот режим](<#why-this-mode-is-useful>)
    * [Рекомендуемый сервер](<#recommended-server>)
    * [Типичный запрос](<#typical-prompt>)
    * [Когда `/browser connect` — неподходящий инструмент](<#when-browser-connect-is-the-wrong-tool>)
    * [Известные проблемы](<#known-pitfalls>)
    * [Пример: заблокируйте опасные действия](<#example-blacklist-dangerous-actions>)
    * [Пример: отключите вспомогательные обёртки](<#example-disable-utility-wrappers-too>)
  * [Что именно фильтруется?](<#what-does-filtering-actually-affect>)
    * [Вспомогательные обёртки, которые вы можете увидеть](<#utility-wrappers-you-may-see>)
  * [Типовые сценарии](<#common-patterns>)
    * [Сценарий 1: локальный помощник по проекту](<#pattern-1-local-project-assistant>)
    * [Сценарий 2: помощник для сортировки задач GitHub](<#pattern-2-github-triage-assistant>)
    * [Сценарий 3: помощник для внутреннего API](<#pattern-3-internal-api-assistant>)
    * [Сценарий 4: серверы документации и знаний](<#pattern-4-documentation--knowledge-servers>)
  * [Учебный пример: сквозная настройка с фильтрацией](<#tutorial-end-to-end-setup-with-filtering>)
    * [Этап 1: добавьте GitHub MCP с жёстким белым списком](<#phase-1-add-github-mcp-with-a-tight-whitelist>)
    * [Этап 2: расширяйте только по необходимости](<#phase-2-expand-only-when-needed>)
    * [Этап 3: добавьте второй сервер с другой политикой](<#phase-3-add-a-second-server-with-different-policy>)
  * [Рекомендации по безопасному использованию](<#safe-usage-recommendations>)
    * [Для опасных систем предпочитайте белые списки](<#prefer-allowlists-for-dangerous-systems>)
    * [Отключайте неиспользуемые утилиты](<#disable-unused-utilities>)
    * [Ограничивайте область действия серверов](<#keep-servers-scoped-narrowly>)
    * [Перезагружайте после изменений конфигурации](<#reload-after-config-changes>)
  * [Устранение неполадок по симптомам](<#troubleshooting-by-symptom>)
    * [«Сервер подключается, но ожидаемые инструменты отсутствуют»](<#the-server-connects-but-the-tools-i-expected-are-missing>)
    * [«Сервер настроен, но ничего не загружается»](<#the-server-is-configured-but-nothing-loads>)
    * [«Почему я вижу меньше инструментов, чем рекламирует MCP-сервер?»](<#why-do-i-see-fewer-tools-than-the-mcp-server-advertises>)
    * [«Как удалить MCP-сервер без удаления конфигурации?»](<#how-do-i-remove-an-mcp-server-without-deleting-the-config>)
  * [Рекомендуемые первые MCP-настройки](<#recommended-first-mcp-setups>)
  * [Связанные материалы](<#related-docs>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes -->
