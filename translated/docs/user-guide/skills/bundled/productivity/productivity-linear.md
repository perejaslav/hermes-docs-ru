On this page
Linear: управление задачами, проектами и командами через GraphQL + curl.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   |
|---|---|
|Источник| Встроенный (установлен по умолчанию) |
|Путь| `skills/productivity/linear` |
|Версия| `1.0.0` |
|Автор| Hermes Agent |
|Лицензия| MIT |
|Теги| `Linear`, `Project Management`, `Issues`, `GraphQL`, `API`, `Productivity` |
## Справочная информация: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на справочную информацию: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Агент видит эти инструкции, когда навык активен.
# Linear — Управление задачами и проектами
Управляйте задачами, проектами и командами Linear напрямую через GraphQL API с помощью `curl`. Никакого MCP-сервера, OAuth-потока или дополнительных зависимостей.
## Настройка[​](<#setup> "Прямая ссылка на настройку")
 1. Получите личный API-ключ в **Linear Settings > Account > Security & access > Personal API keys** (URL: <https://linear.app/settings/account/security>). Примечание: страница _Settings > API_ на уровне организации показывает только OAuth-приложения и ключи участников рабочего пространства, а не личные ключи.
 2. Установите `LINEAR_API_KEY` в вашем окружении (через `hermes setup` или в конфигурации окружения).

## Основы API[​](<#api-basics> "Прямая ссылка на основы API")
  * **Endpoint:** `https://api.linear.app/graphql` (POST)
  * **Заголовок авторизации:** `Authorization: $LINEAR_API_KEY` (префикс \"Bearer\" для API-ключей не требуется)
  * **Все запросы — POST** с `Content-Type: application/json`
  * **UUID и короткие идентификаторы** (например, `ENG-123`) работают с `issue(id:)`

Базовый шаблон curl:
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ viewer { id name } }"}' | python3 -m json.tool
    
[/code]
## Python-скрипт-помощник (эргономичная альтернатива)[​](<#python-helper-script-ergonomic-alternative> "Прямая ссылка на Python-скрипт-помощник (эргономичная альтернатива)")
Для быстрых однострочных команд, не требующих написания GraphQL вручную, в состав навыка входит CLI на Python из стандартной библиотеки по пути `scripts/linear_api.py`. Без дополнительных зависимостей. Использует ту же авторизацию (читает `LINEAR_API_KEY`).
[code]
    SCRIPT=$(dirname "$(find ~/.hermes -path '*skills/productivity/linear/scripts/linear_api.py' 2>/dev/null | head -1)")/linear_api.py
      
    python3 "$SCRIPT" whoami
    python3 "$SCRIPT" list-teams
    python3 "$SCRIPT" get-issue ENG-42
    python3 "$SCRIPT" get-document 38359beef67c      # получить документ по slugId из URL
    python3 "$SCRIPT" raw 'query { viewer { name } }'
    
[/code]
Все подкоманды: `whoami`, `list-teams`, `list-projects`, `list-states`, `list-issues`, `get-issue`, `search-issues`, `create-issue`, `update-issue`, `update-status`, `add-comment`, `list-documents`, `get-document`, `search-documents`, `raw`. Запустите с `--help` для просмотра флагов.
Используйте скрипт, когда: нужен быстрый ответ без написания GraphQL. Используйте curl, когда: нужен запрос, который скрипт не реализует, или требуется составить фильтры вручную.
## Состояния рабочего процесса[​](<#workflow-states> "Прямая ссылка на состояния рабочего процесса")
Linear использует объекты `WorkflowState` с полем `type`. **6 типов состояний:**
| Тип | Описание |
|---|---|
| `triage` | Входящие задачи, требующие рассмотрения |
| `backlog` | Подтверждённые, но ещё не запланированные |
| `unstarted` | Запланированные/готовые, но не начатые |
| `started` | Активно выполняемые |
| `completed` | Завершённые |
| `canceled` | Не будут выполняться |
У каждой команды есть собственные именованные состояния (например, «In Progress» имеет тип `started`). Чтобы изменить статус задачи, нужен `stateId` (UUID) целевого состояния — сначала запросите состояния рабочего процесса.
**Значения приоритета:** 0 = Нет, 1 = Срочно, 2 = Высокий, 3 = Средний, 4 = Низкий
## Часто используемые запросы[​](<#common-queries> "Прямая ссылка на часто используемые запросы")
### Получить текущего пользователя[​](<#get-current-user> "Прямая ссылка на получение текущего пользователя")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ viewer { id name email } }"}' | python3 -m json.tool
    
[/code]
### Список команд[​](<#list-teams> "Прямая ссылка на список команд")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ teams { nodes { id name key } } }"}' | python3 -m json.tool
    
[/code]
### Список состояний рабочего процесса для команды[​](<#list-workflow-states-for-a-team> "Прямая ссылка на список состояний рабочего процесса для команды")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ workflowStates(filter: { team: { key: { eq: \\\"ENG\\\" } } }) { nodes { id name type } } }"}' | python3 -m json.tool
    
[/code]
### Список задач (первые 20)[​](<#list-issues-first-20> "Прямая ссылка на список задач (первые 20)")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issues(first: 20) { nodes { identifier title priority state { name type } assignee { name } team { key } url } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
    
[/code]
### Список моих назначенных задач[​](<#list-my-assigned-issues> "Прямая ссылка на список моих назначенных задач")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ viewer { assignedIssues(first: 25) { nodes { identifier title state { name type } priority url } } } }"}' | python3 -m json.tool
    
[/code]
### Получить одну задачу (по идентификатору, например ENG-123)[​](<#get-a-single-issue-by-identifier-like-eng-123> "Прямая ссылка на получение одной задачи (по идентификатору, например ENG-123)")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issue(id: \\\"ENG-123\\\") { id identifier title description priority state { id name type } assignee { id name } team { key } project { name } labels { nodes { name } } comments { nodes { body user { name } createdAt } } url } }"}' | python3 -m json.tool
    
[/code]
### Поиск задач по тексту[​](<#search-issues-by-text> "Прямая ссылка на поиск задач по тексту")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issueSearch(query: \\\"bug login\\\", first: 10) { nodes { identifier title state { name } assignee { name } url } } }"}' | python3 -m json.tool
    
[/code]
### Фильтрация задач по типу состояния[​](<#filter-issues-by-state-type> "Прямая ссылка на фильтрацию задач по типу состояния")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issues(filter: { state: { type: { in: [\\\"started\\\"] } } }, first: 20) { nodes { identifier title state { name } assignee { name } } } }"}' | python3 -m json.tool
    
[/code]
### Фильтрация по команде и исполнителю[​](<#filter-by-team-and-assignee> "Прямая ссылка на фильтрацию по команде и исполнителю")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issues(filter: { team: { key: { eq: \\\"ENG\\\" } }, assignee: { email: { eq: \\\"user@example.com\\\" } } }, first: 20) { nodes { identifier title state { name } priority } } }"}' | python3 -m json.tool
    
[/code]
### Список проектов[​](<#list-projects> "Прямая ссылка на список проектов")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ projects(first: 20) { nodes { id name description progress lead { name } teams { nodes { key } } url } } }"}' | python3 -m json.tool
    
[/code]
### Список участников команды[​](<#list-team-members> "Прямая ссылка на список участников команды")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ users { nodes { id name email active } } }"}' | python3 -m json.tool
    
[/code]
### Список меток[​](<#list-labels> "Прямая ссылка на список меток")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issueLabels { nodes { id name color } } }"}' | python3 -m json.tool
    
[/code]
## Часто используемые мутации[​](<#common-mutations> "Прямая ссылка на часто используемые мутации")
### Создать задачу[​](<#create-an-issue> "Прямая ссылка на создание задачи")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "query": "mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }",
        "variables": {
          "input": {
            "teamId": "TEAM_UUID",
            "title": "Fix login bug",
            "description": "Users cannot login with SSO",
            "priority": 2
          }
        }
      }' | python3 -m json.tool
    
[/code]
### Обновить статус задачи[​](<#update-issue-status> "Прямая ссылка на обновление статуса задачи")
Сначала получите UUID целевого состояния из запроса состояний рабочего процесса выше, затем:
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { issueUpdate(id: \\\"ENG-123\\\", input: { stateId: \\\"STATE_UUID\\\" }) { success issue { identifier state { name type } } } }"}' | python3 -m json.tool
    
[/code]
### Назначить задачу[​](<#assign-an-issue> "Прямая ссылка на назначение задачи")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { issueUpdate(id: \\\"ENG-123\\\", input: { assigneeId: \\\"USER_UUID\\\" }) { success issue { identifier assignee { name } } } }"}' | python3 -m json.tool
    
[/code]
### Установить приоритет[​](<#set-priority> "Прямая ссылка на установку приоритета")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { issueUpdate(id: \\\"ENG-123\\\", input: { priority: 1 }) { success issue { identifier priority } } }"}' | python3 -m json.tool
    
[/code]
### Добавить комментарий[​](<#add-a-comment> "Прямая ссылка на добавление комментария")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { commentCreate(input: { issueId: \\\"ISSUE_UUID\\\", body: \\\"Investigated. Root cause is X.\\\" }) { success comment { id body } } }"}' | python3 -m json.tool
    
[/code]
### Установить срок выполнения[​](<#set-due-date> "Прямая ссылка на установку срока выполнения")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { issueUpdate(id: \\\"ENG-123\\\", input: { dueDate: \\\"2026-04-01\\\" }) { success issue { identifier dueDate } } }"}' | python3 -m json.tool
    
[/code]
### Добавить метки к задаче[​](<#add-labels-to-an-issue> "Прямая ссылка на добавление меток к задаче")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { issueUpdate(id: \\\"ENG-123\\\", input: { labelIds: [\\\"LABEL_UUID_1\\\", \\\"LABEL_UUID_2\\\"] }) { success issue { identifier labels { nodes { name } } } } }"}' | python3 -m json.tool
    
[/code]
### Добавить задачу в проект[​](<#add-issue-to-a-project> "Прямая ссылка на добавление задачи в проект")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "mutation { issueUpdate(id: \\\"ENG-123\\\", input: { projectId: \\\"PROJECT_UUID\\\" }) { success issue { identifier project { name } } } }"}' | python3 -m json.tool
    
[/code]
### Создать проект[​](<#create-a-project> "Прямая ссылка на создание проекта")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "query": "mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { success project { id name url } } }",
        "variables": {
          "input": {
            "name": "Q2 Auth Overhaul",
            "description": "Replace legacy auth with OAuth2 and PKCE",
            "teamIds": ["TEAM_UUID"]
          }
        }
      }' | python3 -m json.tool
    
[/code]
## Документы[​](<#documents> "Прямая ссылка на документы")
**Документы** Linear — это текстовые документы (RFC, спецификации, заметки), хранящиеся вместе с задачами. У них есть собственный корневой запрос `documents` и единичная выборка `document(id:)`.
### URL-адреса документов и `slugId`[​](<#document-urls-and-slugid> "Прямая ссылка на URL-адреса документов и slugId")
URL-адреса документов выглядят так:
[code]
    https://linear.app/<workspace>/document/<slug>-<hexSlugId>
    
[/code]
Завершающий шестнадцатеричный сегмент — это `slugId`. Пример: `https://linear.app/nousresearch/document/rfc-hermes-permission-gateway-discord-38359beef67c` → `slugId` равен `38359beef67c`.
**Важная деталь схемы:** тело в Markdown находится в поле `content`. JSON в формате ProseMirror находится в `contentState` (не `contentData` — это поле не существует, и API вернёт 400).
### Получить документ по slugId[​](<#fetch-a-document-by-slugid> "Прямая ссылка на получение документа по slugId")
`document(id:)` принимает только UUID. Чтобы получить документ по шестнадцатеричному slug из URL, отфильтруйте коллекцию:
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "query($s: String!) { documents(filter: { slugId: { eq: $s } }, first: 1) { nodes { id title content contentState slugId url creator { name } project { name } updatedAt } } }", "variables": {"s": "38359beef67c"}}' \
      | python3 -m json.tool
    
[/code]
Или через Python-помощник:
[code]
    python3 scripts/linear_api.py get-document 38359beef67c
    
[/code]
### Получить документ по UUID[​](<#fetch-a-document-by-uuid> "Прямая ссылка на получение документа по UUID")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ document(id: \\\"11700cff-b514-4db3-afcc-3ed1afacba1c\\\") { title content url } }"}' \
      | python3 -m json.tool
    
[/code]
### Список недавних документов[​](<#list-recent-documents> "Прямая ссылка на список недавних документов")
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ documents(first: 25, orderBy: updatedAt) { nodes { id title slugId url updatedAt project { name } } } }"}' \
      | python3 -m json.tool
    
[/code]
### Поиск документов по названию[​](<#search-documents-by-title> "Прямая ссылка на поиск документов по названию")
В схеме Linear нет корневого запроса `searchDocuments`. Вместо этого используйте фильтр по подстроке названия:
[code]
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ documents(filter: { title: { containsIgnoreCase: \\\"RFC\\\" } }, first: 25) { nodes { title slugId url } } }"}' \
      | python3 -m json.tool
    
[/code]
## Пагинация[​](<#pagination> "Прямая ссылка на пагинацию")
Linear использует курсорную пагинацию в стиле Relay:
[code]
    # Первая страница
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issues(first: 20) { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
      
    # Следующая страница — используйте endCursor из предыдущего ответа
    curl -s -X POST https://api.linear.app/graphql \
      -H "Authorization: $LINEAR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ issues(first: 20, after: \\\"CURSOR_FROM_PREVIOUS\\\") { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
    
[/code]
Размер страницы по умолчанию: 50. Максимум: 250. Всегда используйте `first: N` для ограничения результатов.
## Справочник по фильтрации[​](<#filtering-reference> "Прямая ссылка на справочник по фильтрации")
Компараторы: `eq`, `neq`, `in`, `nin`, `lt`, `lte`, `gt`, `gte`, `contains`, `startsWith`, `containsIgnoreCase`
Комбинируйте фильтры с `or: [...]` для логики ИЛИ (по умолчанию внутри объекта фильтра применяется И).
## Типичный рабочий процесс[​](<#typical-workflow> "Прямая ссылка на типичный рабочий процесс")
 1. **Запросить команды**, чтобы получить ID команд и ключи
 2. **Запросить состояния рабочего процесса** для целевой команды, чтобы получить UUID состояний
 3. **Вывести список или выполнить поиск задач**, чтобы найти то, что требует работы
 4. **Создать задачи** с ID команды, заголовком, описанием, приоритетом
 5. **Обновить статус**, установив `stateId` в целевое состояние рабочего процесса
 6. **Добавить комментарии** для отслеживания прогресса
 7. **Отметить как выполненное**, установив `stateId` в состояние типа «completed» команды

## Лимиты запросов[​](<#rate-limits> "Прямая ссылка на лимиты запросов")
  * 5 000 запросов/час на один API-ключ
  * 3 000 000 единиц сложности/час
  * Используйте `first: N` для ограничения результатов и снижения стоимости сложности
  * Следите за заголовком ответа `X-RateLimit-Requests-Remaining`

## Важные замечания[​](<#important-notes> "Прямая ссылка на важные замечания")
  * Всегда используйте инструмент `terminal` с `curl` для API-вызовов — НЕ используйте `web_extract` или `browser`
  * Всегда проверяйте массив `errors` в ответах GraphQL — HTTP 200 может содержать ошибки
  * Если `stateId` опущен при создании задач, Linear по умолчанию использует первое состояние backlog
  * Поле `description` поддерживает Markdown
  * Используйте `python3 -m json.tool` или `jq` для форматирования JSON-ответов в удобочитаемый вид

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочная информация: полный SKILL.md](<#reference-full-skillmd>)
  * [Настройка](<#setup>)
  * [Основы API](<#api-basics>)
  * [Python-скрипт-помощник (эргономичная альтернатива)](<#python-helper-script-ergonomic-alternative>)
  * [Состояния рабочего процесса](<#workflow-states>)
  * [Часто используемые запросы](<#common-queries>)
    * [Получить текущего пользователя](<#get-current-user>)
    * [Список команд](<#list-teams>)
    * [Список состояний рабочего процесса для команды](<#list-workflow-states-for-a-team>)
    * [Список задач (первые 20)](<#list-issues-first-20>)
    * [Список моих назначенных задач](<#list-my-assigned-issues>)
    * [Получить одну задачу (по идентификатору, например ENG-123)](<#get-a-single-issue-by-identifier-like-eng-123>)
    * [Поиск задач по тексту](<#search-issues-by-text>)
    * [Фильтрация задач по типу состояния](<#filter-issues-by-state-type>)
    * [Фильтрация по команде и исполнителю](<#filter-by-team-and-assignee>)
    * [Список проектов](<#list-projects>)
    * [Список участников команды](<#list-team-members>)
    * [Список меток](<#list-labels>)
  * [Часто используемые мутации](<#common-mutations>)
    * [Создать задачу](<#create-an-issue>)
    * [Обновить статус задачи](<#update-issue-status>)
    * [Назначить задачу](<#assign-an-issue>)
    * [Установить приоритет](<#set-priority>)
    * [Добавить комментарий](<#add-a-comment>)
    * [Установить срок выполнения](<#set-due-date>)
    * [Добавить метки к задаче](<#add-labels-to-an-issue>)
    * [Добавить задачу в проект](<#add-issue-to-a-project>)
    * [Создать проект](<#create-a-project>)
  * [Документы](<#documents>)
    * [URL-адреса документов и `slugId`](<#document-urls-and-slugid>)
    * [Получить документ по slugId](<#fetch-a-document-by-slugid>)
    * [Получить документ по UUID](<#fetch-a-document-by-uuid>)
    * [Список недавних документов](<#list-recent-documents>)
    * [Поиск документов по названию](<#search-documents-by-title>)
  * [Пагинация](<#pagination>)
  * [Справочник по фильтрации](<#filtering-reference>)
  * [Типичный рабочий процесс](<#typical-workflow>)
  * [Лимиты запросов](<#rate-limits>)
  * [Важные замечания](<#important-notes>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-linear -->
