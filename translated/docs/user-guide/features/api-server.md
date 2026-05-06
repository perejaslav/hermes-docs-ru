На этой странице
API-сервер предоставляет hermes-agent в качестве HTTP-эндпоинта, совместимого с OpenAI. Любой фронтенд, поддерживающий формат OpenAI — Open WebUI, LobeChat, LibreChat, NextChat, ChatBox и сотни других — может подключиться к hermes-agent и использовать его в качестве бэкенда.
Ваш агент обрабатывает запросы со своим полным набором инструментов (терминал, файловые операции, веб-поиск, память, навыки) и возвращает финальный ответ. При стриминге индикаторы прогресса инструментов отображаются встроенно, чтобы фронтенды могли показывать, что делает агент.
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
### 1\\. Включите API-сервер[​](<#1-enable-the-api-server> "Direct link to 1. Enable the API server")
Добавьте в `~/.hermes/.env`:
[code]
    API_SERVER_ENABLED=true
    API_SERVER_KEY=change-me-local-dev
    # Опционально: только если браузер должен вызывать Hermes напрямую
    # API_SERVER_CORS_ORIGINS=http://localhost:3000

[/code]
### 2\\. Запустите шлюз[​](<#2-start-the-gateway> "Direct link to 2. Start the gateway")
[code]
    hermes gateway

[/code]
Вы увидите:
[code]
    [API Server] API server listening on http://127.0.0.1:8642

[/code]
### 3\\. Подключите фронтенд[​](<#3-connect-a-frontend> "Direct link to 3. Connect a frontend")
Направьте любой OpenAI-совместимый клиент на `http://localhost:8642/v1`:
[code]
    # Тест с curl
    curl http://localhost:8642/v1/chat/completions \
      -H "Authorization: Bearer change-me-local-dev" \
      -H "Content-Type: application/json" \
      -d '{"model": "hermes-agent", "messages": [{"role": "user", "content": "Hello!"}]}'

[/code]
Или подключите Open WebUI, LobeChat или любой другой фронтенд — см. [руководство по интеграции Open WebUI](</docs/user-guide/messaging/open-webui>) для пошаговых инструкций.
## Endpoints[​](<#endpoints> "Direct link to Endpoints")
### POST /v1/chat/completions[​](<#post-v1chatcompletions> "Direct link to POST /v1/chat/completions")
Стандартный формат OpenAI Chat Completions. Не сохраняет состояние — полный диалог включается в каждый запрос через массив `messages`.
**Запрос:**
[code]
    {
      "model": "hermes-agent",
      "messages": [
        {"role": "system", "content": "You are a Python expert."},
        {"role": "user", "content": "Write a fibonacci function"}
      ],
      "stream": false
    }

[/code]
**Ответ:**
[code]
    {
      "id": "chatcmpl-abc123",
      "object": "chat.completion",
      "created": 1710000000,
      "model": "hermes-agent",
      "choices": [{
        "index": 0,
        "message": {"role": "assistant", "content": "Here's a fibonacci function..."},
        "finish_reason": "stop"
      }],
      "usage": {"prompt_tokens": 50, "completion_tokens": 200, "total_tokens": 250}
    }

[/code]
**Встроенный ввод изображений:** в сообщениях пользователя `content` может передаваться как массив частей `text` и `image_url`. Поддерживаются как удаленные `http(s)` URL, так и `data:image/...` URL:
[code]
    {
      "model": "hermes-agent",
      "messages": [
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What is in this image?"},
            {"type": "image_url", "image_url": {"url": "https://example.com/cat.png", "detail": "high"}}
          ]
        }
      ]
    }

[/code]
Загруженные файлы (`file` / `input_file` / `file_id`) и не-изображения с `data:` URL возвращают `400 unsupported_content_type`.
**Стриминг** (`"stream": true`): Возвращает Server-Sent Events (SSE) с чанками ответа токен за токеном. Для **Chat Completions** поток использует стандартные события `chat.completion.chunk` плюс пользовательские события `hermes.tool.progress` для UX при запуске инструментов. Для **Responses** поток использует типы событий OpenAI Responses, такие как `response.created`, `response.output_text.delta`, `response.output_item.added`, `response.output_item.done` и `response.completed`.
**Прогресс инструментов в потоках:**
  * **Chat Completions**: Hermes отправляет `event: hermes.tool.progress` для отображения запуска инструмента без засорения постоянного текста ассистента.
  * **Responses**: Hermes отправляет нативные для спецификации элементы вывода `function_call` и `function_call_output` во время SSE-потока, чтобы клиенты могли отображать структурированный UI инструментов в реальном времени.


### POST /v1/responses[​](<#post-v1responses> "Direct link to POST /v1/responses")
Формат OpenAI Responses API. Поддерживает состояние диалога на стороне сервера через `previous_response_id` — сервер хранит полную историю диалога (включая вызовы инструментов и результаты), поэтому контекст многошагового общения сохраняется без управления им со стороны клиента.
**Запрос:**
[code]
    {
      "model": "hermes-agent",
      "input": "What files are in my project?",
      "instructions": "You are a helpful coding assistant.",
      "store": true
    }

[/code]
**Ответ:**
[code]
    {
      "id": "resp_abc123",
      "object": "response",
      "status": "completed",
      "model": "hermes-agent",
      "output": [
        {"type": "function_call", "name": "terminal", "arguments": "{\"command\": \"ls\"}", "call_id": "call_1"},
        {"type": "function_call_output", "call_id": "call_1", "output": "README.md src/ tests/"},
        {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Your project has..."}]}
      ],
      "usage": {"input_tokens": 50, "output_tokens": 200, "total_tokens": 250}
    }

[/code]
**Встроенный ввод изображений:** `input[].content` может содержать части `input_text` и `input_image`. Поддерживаются как удаленные URL, так и `data:image/...` URL:
[code]
    {
      "model": "hermes-agent",
      "input": [
        {
          "role": "user",
          "content": [
            {"type": "input_text", "text": "Describe this screenshot."},
            {"type": "input_image", "image_url": "data:image/png;base64,iVBORw0K..."}
          ]
        }
      ]
    }

[/code]
Загруженные файлы (`input_file` / `file_id`) и не-изображения с `data:` URL возвращают `400 unsupported_content_type`.
#### Многошаговые диалоги с previous_response_id[​](<#multi-turn-with-previous_response_id> "Direct link to Multi-turn with previous_response_id")
Цепочка ответов для поддержания полного контекста (включая вызовы инструментов) между шагами:
[code]
    {
      "input": "Now show me the README",
      "previous_response_id": "resp_abc123"
    }

[/code]
Сервер восстанавливает полный диалог из сохраненной цепочки ответов — все предыдущие вызовы инструментов и результаты сохраняются. Цепочные запросы также используют одну и ту же сессию, поэтому многошаговые диалоги отображаются как одна запись на панели управления и в истории сессий.
#### Именованные диалоги[​](<#named-conversations> "Direct link to Named conversations")
Используйте параметр `conversation` вместо отслеживания ID ответов:
[code]
    {"input": "Hello", "conversation": "my-project"}
    {"input": "What's in src/?", "conversation": "my-project"}
    {"input": "Run the tests", "conversation": "my-project"}

[/code]
Сервер автоматически связывает запрос с последним ответом в этом диалоге. Аналогично команде `/title` для сессий шлюза.
### GET /v1/responses/{id}[​](<#get-v1responsesid> "Direct link to GET /v1/responses/{id}")
Получение ранее сохраненного ответа по ID.
### DELETE /v1/responses/{id}[​](<#delete-v1responsesid> "Direct link to DELETE /v1/responses/{id}")
Удаление сохраненного ответа.
### GET /v1/models[​](<#get-v1models> "Direct link to GET /v1/models")
Выводит агента как доступную модель. Отображаемое имя модели по умолчанию соответствует имени [профиля](</docs/user-guide/profiles>) (или `hermes-agent` для профиля по умолчанию). Требуется большинством фронтендов для обнаружения модели.
### GET /v1/capabilities[​](<#get-v1capabilities> "Direct link to GET /v1/capabilities")
Возвращает машиночитаемое описание стабильной поверхности API-сервера для внешних UI, оркестраторов и плагинных мостов.
[code]
    {
      "object": "hermes.api_server.capabilities",
      "platform": "hermes-agent",
      "model": "hermes-agent",
      "auth": {"type": "bearer", "required": true},
      "features": {
        "chat_completions": true,
        "responses_api": true,
        "run_submission": true,
        "run_status": true,
        "run_events_sse": true,
        "run_stop": true
      }
    }

[/code]
Используйте этот эндпоинт при интеграции панелей управления, браузерных UI или контрольных панелей, чтобы они могли определить, поддерживает ли работающая версия Hermes запуски, стриминг, отмену и непрерывность сессий, не полагаясь на внутренние Python-интерфейсы.
### GET /health[​](<#get-health> "Direct link to GET /health")
Проверка работоспособности. Возвращает `{"status": "ok"}`. Также доступен по адресу **GET /v1/health** для OpenAI-совместимых клиентов, ожидающих префикс `/v1/`.
### GET /health/detailed[​](<#get-healthdetailed> "Direct link to GET /health/detailed")
Расширенная проверка работоспособности, которая также сообщает об активных сессиях, работающих агентах и использовании ресурсов. Полезно для инструментов мониторинга/наблюдаемости.
## Runs API (альтернатива для стриминга)[​](<#runs-api-streaming-friendly-alternative> "Direct link to Runs API (streaming-friendly alternative)")
В дополнение к `/v1/chat/completions` и `/v1/responses` сервер предоставляет **runs** API для длительных сессий, где клиент хочет подписаться на события прогресса вместо самостоятельного управления стримингом.
### POST /v1/runs[​](<#post-v1runs> "Direct link to POST /v1/runs")
Создание нового запуска агента. Возвращает `run_id`, который можно использовать для подписки на события прогресса.
[code]
    {
      "run_id": "run_abc123",
      "status": "started"
    }

[/code]
Запуски принимают простую строку `input` и опциональные `session_id`, `instructions`, `conversation_history` или `previous_response_id`. Когда указан `session_id`, Hermes отображает его в статусе запуска, чтобы внешние UI могли связывать запуски со своими ID диалогов.
### GET /v1/runs/{run_id}[​](<#get-v1runsrun_id> "Direct link to GET /v1/runs/{run_id}")
Опрос текущего состояния запуска. Полезно для панелей управления, которым нужен статус без удержания SSE-соединения, или для UI, переподключающихся после навигации.
[code]
    {
      "object": "hermes.run",
      "run_id": "run_abc123",
      "status": "completed",
      "session_id": "space-session",
      "model": "hermes-agent",
      "output": "Done.",
      "usage": {"input_tokens": 50, "output_tokens": 200, "total_tokens": 250}
    }

[/code]
Статусы сохраняются недолго после терминальных состояний (`completed`, `failed` или `cancelled`) для опроса и синхронизации UI.
### GET /v1/runs/{run_id}/events[​](<#get-v1runsrun_idevents> "Direct link to GET /v1/runs/{run_id}/events")
Поток Server-Sent Events с прогрессом вызовов инструментов, дельтами токенов и событиями жизненного цикла запуска. Предназначен для панелей управления и толстых клиентов, которые хотят подключаться/отключаться без потери состояния.
### POST /v1/runs/{run_id}/stop[​](<#post-v1runsrun_idstop> "Direct link to POST /v1/runs/{run_id}/stop")
Прерывание активного шага агента. Эндпоинт немедленно возвращает `{"status": "stopping"}`, пока Hermes просит активного агента остановиться в ближайшей безопасной точке прерывания.
## Jobs API (фоновая запланированная работа)[​](<#jobs-api-background-scheduled-work> "Direct link to Jobs API (background scheduled work)")
Сервер предоставляет легковесную CRUD-поверхность для управления запланированными/фоновыми запусками агентов из удаленного клиента. Все эндпоинты защищены той же bearer-аутентификацией.
### GET /api/jobs[​](<#get-apijobs> "Direct link to GET /api/jobs")
Список всех запланированных заданий.
### POST /api/jobs[​](<#post-apijobs> "Direct link to POST /api/jobs")
Создание нового запланированного задания. Тело принимает ту же структуру, что и `hermes cron` — prompt, schedule, skills, provider override, delivery target.
### GET /api/jobs/{job_id}[​](<#get-apijobsjob_id> "Direct link to GET /api/jobs/{job_id}")
Получение определения одного задания и состояния последнего запуска.
### PATCH /api/jobs/{job_id}[​](<#patch-apijobsjob_id> "Direct link to PATCH /api/jobs/{job_id}")
Обновление полей существующего задания (prompt, schedule и т.д.). Частичные обновления объединяются.
### DELETE /api/jobs/{job_id}[​](<#delete-apijobsjob_id> "Direct link to DELETE /api/jobs/{job_id}")
Удаление задания. Также отменяет любой выполняющийся запуск.
### POST /api/jobs/{job_id}/pause[​](<#post-apijobsjob_idpause> "Direct link to POST /api/jobs/{job_id}/pause")
Приостановка задания без его удаления. Временные метки следующего запланированного запуска приостанавливаются до возобновления.
### POST /api/jobs/{job_id}/resume[​](<#post-apijobsjob_idresume> "Direct link to POST /api/jobs/{job_id}/resume")
Возобновление ранее приостановленного задания.
### POST /api/jobs/{job_id}/run[​](<#post-apijobsjob_idrun> "Direct link to POST /api/jobs/{job_id}/run")
Запуск задания немедленно, вне расписания.
## Обработка системного промпта[​](<#system-prompt-handling> "Direct link to System Prompt Handling")
Когда фронтенд отправляет сообщение `system` (Chat Completions) или поле `instructions` (Responses API), hermes-agent **накладывает его поверх** своего основного системного промпта. Ваш агент сохраняет все свои инструменты, память и навыки — системный промпт фронтенда добавляет дополнительные инструкции.
Это означает, что вы можете настраивать поведение для каждого фронтенда без потери возможностей:
  * Системный промпт Open WebUI: "You are a Python expert. Always include type hints."
  * Агент по-прежнему имеет терминал, файловые инструменты, веб-поиск, память и т.д.


## Аутентификация[​](<#authentication> "Direct link to Authentication")
Аутентификация через Bearer-токен в заголовке `Authorization`:
[code]
    Authorization: Bearer ***

[/code]
Настройте ключ через переменную окружения `API_SERVER_KEY`. Если вам нужно, чтобы браузер вызывал Hermes напрямую, также установите `API_SERVER_CORS_ORIGINS` в явный белый список.
Безопасность
API-сервер предоставляет полный доступ к набору инструментов hermes-agent, **включая команды терминала**. При привязке к не-loopback-адресу, например `0.0.0.0`, `API_SERVER_KEY` **обязателен**. Также держите `API_SERVER_CORS_ORIGINS` узким для контроля доступа браузера.
Адрес привязки по умолчанию (`127.0.0.1`) предназначен только для локального использования. Доступ из браузера отключен по умолчанию; включайте его только для явно доверенных источников.
## Конфигурация[​](<#configuration> "Direct link to Configuration")
### Переменные окружения[​](<#environment-variables> "Direct link to Environment Variables")
Variable| Default| Description
---|---|---
`API_SERVER_ENABLED`| `false`| Включить API-сервер
`API_SERVER_PORT`| `8642`| Порт HTTP-сервера
`API_SERVER_HOST`| `127.0.0.1`| Адрес привязки (только localhost по умолчанию)
`API_SERVER_KEY`|  _(нет)_|  Bearer-токен для аутентификации
`API_SERVER_CORS_ORIGINS`|  _(нет)_|  Разрешенные источники браузера через запятую
`API_SERVER_MODEL_NAME`|  _(имя профиля)_|  Имя модели на `/v1/models`. По умолчанию имя профиля или `hermes-agent` для профиля по умолчанию.
### config.yaml[​](<#configyaml> "Direct link to config.yaml")
[code]
    # Пока не поддерживается — используйте переменные окружения.
    # Поддержка config.yaml появится в одном из будущих релизов.

[/code]
## Заголовки безопасности[​](<#security-headers> "Direct link to Security Headers")
Все ответы включают заголовки безопасности:
  * `X-Content-Type-Options: nosniff` — предотвращает подмену MIME-типа
  * `Referrer-Policy: no-referrer` — предотвращает утечку реферера


## CORS[​](<#cors> "Direct link to CORS")
API-сервер **не** включает CORS для браузеров по умолчанию.
Для прямого доступа из браузера установите явный белый список:
[code]
    API_SERVER_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

[/code]
Когда CORS включен:
  * **Preflight-ответы** включают `Access-Control-Max-Age: 600` (кэш на 10 минут)
  * **SSE-стриминг ответов** включает CORS-заголовки, чтобы браузерные EventSource-клиенты работали корректно
  * **`Idempotency-Key`** является разрешенным заголовком запроса — клиенты могут отправлять его для дедупликации (ответы кэшируются по ключу на 5 минут)


Большинство документированных фронтендов, таких как Open WebUI, подключаются по схеме сервер-к-серверу и не нуждаются в CORS.
## Совместимые фронтенды[​](<#compatible-frontends> "Direct link to Compatible Frontends")
Любой фронтенд, поддерживающий формат API OpenAI, работает. Протестированные/документированные интеграции:
Frontend| Stars| Подключение
---|---|---
[Open WebUI](</docs/user-guide/messaging/open-webui>)| 126k| Полное руководство
LobeChat| 73k| Пользовательский эндпоинт провайдера
LibreChat| 34k| Пользовательский эндпоинт в librechat.yaml
AnythingLLM| 56k| Универсальный провайдер OpenAI
NextChat| 87k| Переменная окружения BASE_URL
ChatBox| 39k| Настройка API Host
Jan| 26k| Конфигурация удаленной модели
HF Chat-UI| 8k| OPENAI_BASE_URL
big-AGI| 7k| Пользовательский эндпоинт
OpenAI Python SDK| —| `OpenAI(base_url=\"http://localhost:8642/v1\")`
curl| —| Прямые HTTP-запросы
## Многопользовательская настройка с профилями[​](<#multi-user-setup-with-profiles> "Direct link to Multi-User Setup with Profiles")
Чтобы предоставить нескольким пользователям их собственные изолированные экземпляры Hermes (отдельная конфигурация, память, навыки), используйте [профили](</docs/user-guide/profiles>):
[code]
    # Создайте профиль для каждого пользователя
    hermes profile create alice
    hermes profile create bob

    # Настройте API-сервер каждого профиля на разных портах
    hermes -p alice config set API_SERVER_ENABLED true
    hermes -p alice config set API_SERVER_PORT 8643
    hermes -p alice config set API_SERVER_KEY alice-secret

    hermes -p bob config set API_SERVER_ENABLED true
    hermes -p bob config set API_SERVER_PORT 8644
    hermes -p bob config set API_SERVER_KEY bob-secret

    # Запустите шлюз каждого профиля
    hermes -p alice gateway &
    hermes -p bob gateway &

[/code]
API-сервер каждого профиля автоматически рекламирует имя профиля как ID модели:
  * `http://localhost:8643/v1/models` → модель `alice`
  * `http://localhost:8644/v1/models` → модель `bob`


В Open WebUI добавьте каждое как отдельное подключение. Выпадающий список моделей показывает `alice` и `bob` как отдельные модели, каждая из которых работает на полностью изолированном экземпляре Hermes. См. [руководство по Open WebUI](</docs/user-guide/messaging/open-webui#multi-user-setup-with-profiles>) для подробностей.
## Ограничения[​](<#limitations> "Direct link to Limitations")
  * **Хранение ответов** — сохраненные ответы (для `previous_response_id`) хранятся в SQLite и переживают перезапуски шлюза. Максимум 100 сохраненных ответов (LRU-вытеснение).
  * **Нет загрузки файлов** — встроенные изображения поддерживаются как в `/v1/chat/completions`, так и в `/v1/responses`, но загруженные файлы (`file`, `input_file`, `file_id`) и не-изображения не поддерживаются через API.
  * **Поле model — косметическое** — поле `model` в запросах принимается, но фактическая используемая LLM-модель настраивается на стороне сервера в config.yaml.


## Режим прокси[​](<#proxy-mode> "Direct link to Proxy Mode")
API-сервер также служит бэкендом для **режима прокси шлюза**. Когда другой экземпляр шлюза Hermes настроен с `GATEWAY_PROXY_URL`, указывающим на этот API-сервер, он перенаправляет все сообщения сюда вместо запуска собственного агента. Это позволяет разделенные развертывания — например, Docker-контейнер, обрабатывающий Matrix E2EE, который ретранслирует на агент на хост-машине.
См. [Matrix Proxy Mode](</docs/user-guide/messaging/matrix#proxy-mode-e2ee-on-macos>) для полного руководства по настройке.
  * [Quick Start](<#quick-start>)
    * [1\\. Включите API-сервер](<#1-enable-the-api-server>)
    * [2\\. Запустите шлюз](<#2-start-the-gateway>)
    * [3\\. Подключите фронтенд](<#3-connect-a-frontend>)
  * [Endpoints](<#endpoints>)
    * [POST /v1/chat/completions](<#post-v1chatcompletions>)
    * [POST /v1/responses](<#post-v1responses>)
    * [GET /v1/responses/{id}](<#get-v1responsesid>)
    * [DELETE /v1/responses/{id}](<#delete-v1responsesid>)
    * [GET /v1/models](<#get-v1models>)
    * [GET /v1/capabilities](<#get-v1capabilities>)
    * [GET /health](<#get-health>)
    * [GET /health/detailed](<#get-healthdetailed>)
  * [Runs API (альтернатива для стриминга)](<#runs-api-streaming-friendly-alternative>)
    * [POST /v1/runs](<#post-v1runs>)
    * [GET /v1/runs/{run_id}](<#get-v1runsrun_id>)
    * [GET /v1/runs/{run_id}/events](<#get-v1runsrun_idevents>)
    * [POST /v1/runs/{run_id}/stop](<#post-v1runsrun_idstop>)
  * [Jobs API (фоновая запланированная работа)](<#jobs-api-background-scheduled-work>)
    * [GET /api/jobs](<#get-apijobs>)
    * [POST /api/jobs](<#post-apijobs>)
    * [GET /api/jobs/{job_id}](<#get-apijobsjob_id>)
    * [PATCH /api/jobs/{job_id}](<#patch-apijobsjob_id>)
    * [DELETE /api/jobs/{job_id}](<#delete-apijobsjob_id>)
    * [POST /api/jobs/{job_id}/pause](<#post-apijobsjob_idpause>)
    * [POST /api/jobs/{job_id}/resume](<#post-apijobsjob_idresume>)
    * [POST /api/jobs/{job_id}/run](<#post-apijobsjob_idrun>)
  * [Обработка системного промпта](<#system-prompt-handling>)
  * [Аутентификация](<#authentication>)
  * [Конфигурация](<#configuration>)
    * [Переменные окружения](<#environment-variables>)
    * [config.yaml](<#configyaml>)
  * [Заголовки безопасности](<#security-headers>)
  * [CORS](<#cors>)
  * [Совместимые фронтенды](<#compatible-frontends>)
  * [Многопользовательская настройка с профилями](<#multi-user-setup-with-profiles>)
  * [Ограничения](<#limitations>)
  * [Режим прокси](<#proxy-mode>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server -->
