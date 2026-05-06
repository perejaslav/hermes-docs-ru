On this page
[Open WebUI](<https://github.com/open-webui/open-webui>) (126k★) — это самый популярный самостоятельный чат-интерфейс для ИИ. Со встроенным API-сервером Hermes Agent вы можете использовать Open WebUI как полноценный веб-фронтенд для вашего агента — с управлением беседами, учётными записями пользователей и современным чат-интерфейсом.
## Архитектура[​](<#architecture> "Direct link to Architecture")
Open WebUI подключается к API-серверу Hermes Agent точно так же, как подключался бы к OpenAI. Ваш агент обрабатывает запросы со всем своим набором инструментов — терминал, файловые операции, веб-поиск, память, навыки — и возвращает финальный ответ.
Open WebUI взаимодействует с Hermes по схеме «сервер-сервер», поэтому вам не нужен `API_SERVER_CORS_ORIGINS` для этой интеграции.
## Быстрая настройка[​](<#quick-setup> "Direct link to Quick Setup")
### Быстрый локальный запуск одной командой (macOS/Linux, без Docker)[​](<#one-command-local-bootstrap-macoslinux-no-docker> "Direct link to One-command local bootstrap (macOS/Linux, no Docker)")
Если вы хотите локально связать Hermes + Open WebUI с переиспользуемым лаунчером, выполните:
[code] 
    cd ~/.hermes/hermes-agent  
    bash scripts/setup_open_webui.sh  
    
[/code]
Что делает скрипт:
  * проверяет, что `~/.hermes/.env` содержит `API_SERVER_ENABLED`, `API_SERVER_HOST`, `API_SERVER_KEY`, `API_SERVER_PORT` и `API_SERVER_MODEL_NAME`
  * перезапускает шлюз Hermes, чтобы API-сервер запустился
  * устанавливает Open WebUI в `~/.local/open-webui-venv`
  * создаёт лаунчер в `~/.local/bin/start-open-webui-hermes.sh`
  * на macOS устанавливает пользовательский сервис `launchd`; на Linux с `systemd --user` устанавливает пользовательский сервис там же


Значения по умолчанию:
  * API Hermes: `http://127.0.0.1:8642/v1`
  * Open WebUI: `http://127.0.0.1:8080`
  * имя модели, отображаемое в Open WebUI: `Hermes Agent`


Полезные переопределения:
[code] 
    OPEN_WEBUI_NAME='My Hermes UI' \  
    OPEN_WEBUI_ENABLE_SIGNUP=true \  
    HERMES_API_MODEL_NAME='My Hermes Agent' \  
    bash scripts/setup_open_webui.sh  
    
[/code]
На Linux автоматическая настройка фонового сервиса требует работающей сессии `systemd --user`. Если вы находитесь на безголовом SSH-сервере и хотите пропустить установку сервиса, выполните:
[code] 
    OPEN_WEBUI_ENABLE_SERVICE=false bash scripts/setup_open_webui.sh  
    
[/code]
### 1\. Включение API-сервера[​](<#1-enable-the-api-server> "Direct link to 1. Enable the API server")
[code] 
    hermes config set API_SERVER_ENABLED true  
    hermes config set API_SERVER_KEY your-secret-key  
    
[/code]
`hermes config set` автоматически направляет флаг в `config.yaml`, а секрет — в `~/.hermes/.env`. Если шлюз уже запущен, перезапустите его, чтобы изменения вступили в силу:
[code] 
    hermes gateway stop && hermes gateway  
    
[/code]
### 2\. Запуск шлюза Hermes Agent[​](<#2-start-hermes-agent-gateway> "Direct link to 2. Start Hermes Agent gateway")
[code] 
    hermes gateway  
    
[/code]
Вы должны увидеть:
[code] 
    [API Server] API server listening on http://127.0.0.1:8642  
    
[/code]
### 3\. Проверка доступности API-сервера[​](<#3-verify-the-api-server-is-reachable> "Direct link to 3. Verify the API server is reachable")
[code] 
    curl -s http://127.0.0.1:8642/health  
    # {"status": "ok", ...}  
      
    curl -s -H "Authorization: Bearer your-secret-key" http://127.0.0.1:8642/v1/models  
    # {"object":"list","data":[{"id":"hermes-agent", ...}]}  
    
[/code]
Если `/health` не отвечает, шлюз не подхватил `API_SERVER_ENABLED=true` — перезапустите его. Если `/v1/models` возвращает `401`, ваш заголовок `Authorization` не соответствует `API_SERVER_KEY`.
### 4\. Запуск Open WebUI[​](<#4-start-open-webui> "Direct link to 4. Start Open WebUI")
[code] 
    docker run -d -p 3000:8080 \  
      -e OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1 \  
      -e OPENAI_API_KEY=your-secret-key \  
      -e ENABLE_OLLAMA_API=false \  
      --add-host=host.docker.internal:host-gateway \  
      -v open-webui:/app/backend/data \  
      --name open-webui \  
      --restart always \  
      ghcr.io/open-webui/open-webui:main  
    
[/code]
`ENABLE_OLLAMA_API=false` отключает стандартный бэкенд Ollama, который иначе отображался бы пустым и засорял выбор моделей. Опустите этот флаг, если у вас действительно запущен Ollama.
Первый запуск занимает 15–30 секунд: Open WebUI загружает модели эмбеддингов sentence-transformer (~150 МБ) при первом старте. Дождитесь, пока `docker logs open-webui` перестанет выводить сообщения, прежде чем открывать интерфейс.
### 5\. Открытие интерфейса[​](<#5-open-the-ui> "Direct link to 5. Open the UI")
Перейдите на **<http://localhost:3000>**. Создайте учётную запись администратора (первый пользователь становится администратором). Вы должны увидеть своего агента в выпадающем списке моделей (названном по имени вашего профиля или **hermes-agent** для профиля по умолчанию). Начинайте общение!
## Настройка через Docker Compose[​](<#docker-compose-setup> "Direct link to Docker Compose Setup")
Для более постоянной настройки создайте `docker-compose.yml`:
[code] 
    services:  
      open-webui:  
        image: ghcr.io/open-webui/open-webui:main  
        ports:  
          - "3000:8080"  
        volumes:  
          - open-webui:/app/backend/data  
        environment:  
          - OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1  
          - OPENAI_API_KEY=your-secret-key  
          - ENABLE_OLLAMA_API=false  
        extra_hosts:  
          - "host.docker.internal:host-gateway"  
        restart: always  
      
    volumes:  
      open-webui:  
    
[/code]
Затем:
[code] 
    docker compose up -d  
    
[/code]
## Настройка через интерфейс администратора[​](<#configuring-via-the-admin-ui> "Direct link to Configuring via the Admin UI")
Если вы предпочитаете настраивать подключение через интерфейс, а не через переменные окружения:
  1. Войдите в Open WebUI по адресу **<http://localhost:3000>**
  2. Нажмите на **аватар профиля** → **Admin Settings**
  3. Перейдите в **Connections**
  4. В разделе **OpenAI API** нажмите на **иконку гаечного ключа** (Manage)
  5. Нажмите **\+ Add New Connection**
  6. Введите:
     * **URL**: `http://host.docker.internal:8642/v1`
     * **API Key**: то же значение, что и `API_SERVER_KEY` в Hermes
  7. Нажмите **галочку**, чтобы проверить подключение
  8. **Save**


Модель вашего агента должна появиться в выпадающем списке (названная по имени вашего профиля или **hermes-agent** для профиля по умолчанию).
warning
Переменные окружения действуют только при **первом запуске** Open WebUI. После этого настройки подключения сохраняются во внутренней базе данных. Чтобы изменить их позже, используйте интерфейс администратора или удалите том Docker и начните заново.
## Тип API: Chat Completions vs Responses[​](<#api-type-chat-completions-vs-responses> "Direct link to API Type: Chat Completions vs Responses")
Open WebUI поддерживает два режима API при подключении к бэкенду:
Режим| Формат| Когда использовать  
|---|---|---  
**Chat Completions** (по умолчанию)| `/v1/chat/completions`| Рекомендуется. Работает «из коробки».  
**Responses** (экспериментальный)| `/v1/responses`| Для состояния беседы на стороне сервера через `previous_response_id`.  
### Использование Chat Completions (рекомендуется)[​](<#using-chat-completions-recommended> "Direct link to Using Chat Completions (recommended)")
Этот режим используется по умолчанию и не требует дополнительной настройки. Open WebUI отправляет стандартные запросы в формате OpenAI, и Hermes Agent отвечает соответствующим образом. Каждый запрос включает полную историю беседы.
### Использование Responses API[​](<#using-responses-api> "Direct link to Using Responses API")
Чтобы использовать режим Responses API:
  1. Перейдите в **Admin Settings** → **Connections** → **OpenAI** → **Manage**
  2. Отредактируйте ваше подключение hermes-agent
  3. Измените **API Type** с «Chat Completions» на **«Responses (Experimental)»**
  4. Нажмите **Save**


С помощью Responses API Open WebUI отправляет запросы в формате Responses (массив `input` + `instructions`), и Hermes Agent может сохранять полную историю вызовов инструментов между раундами через `previous_response_id`. Когда `stream: true`, Hermes также передаёт потоковые элементы `function_call` и `function_call_output` в нативном формате, что позволяет создавать пользовательский структурированный интерфейс вызовов инструментов в клиентах, которые поддерживают события Responses.
note
В настоящее время Open WebUI управляет историей беседы на стороне клиента даже в режиме Responses — он отправляет полную историю сообщений в каждом запросе вместо использования `previous_response_id`. Главное преимущество режима Responses сегодня — это структурированный поток событий: текстовые дельты, элементы `function_call` и `function_call_output` приходят как события OpenAI Responses SSE вместо фрагментов Chat Completions.
## Как это работает[​](<#how-it-works> "Direct link to How It Works")
Когда вы отправляете сообщение в Open WebUI:
  1. Open WebUI отправляет запрос `POST /v1/chat/completions` с вашим сообщением и историей беседы
  2. Hermes Agent создаёт экземпляр AIAgent с полным набором инструментов
  3. Агент обрабатывает ваш запрос — он может вызывать инструменты (терминал, файловые операции, веб-поиск и т.д.)
  4. По мере выполнения инструментов **промежуточные сообщения о прогрессе передаются в интерфейс**, так что вы видите, что делает агент (например, ``💻 ls -la``, ``🔍 Python 3.12 release``)
  5. Финальный текстовый ответ агента передаётся обратно в Open WebUI
  6. Open WebUI отображает ответ в своём чат-интерфейсе


Ваш агент имеет доступ ко всем тем же инструментам и возможностям, что и при использовании CLI или Telegram — единственное отличие — это интерфейс.
Tool Progress
При включённой потоковой передаче (по умолчанию) вы будете видеть краткие индикаторы во время выполнения инструментов — эмодзи инструмента и его ключевой аргумент. Они появляются в потоке ответа перед финальным ответом агента, давая вам представление о том, что происходит «за кулисами».
## Справочник по настройке[​](<#configuration-reference> "Direct link to Configuration Reference")
### Hermes Agent (API-сервер)[​](<#hermes-agent-api-server> "Direct link to Hermes Agent (API server)")
Переменная| По умолчанию| Описание  
|---|---|---  
`API_SERVER_ENABLED`| `false`| Включить API-сервер  
`API_SERVER_PORT`| `8642`| Порт HTTP-сервера  
`API_SERVER_HOST`| `127.0.0.1`| Адрес привязки  
`API_SERVER_KEY`|  _(обязательно)_|  Bearer-токен для аутентификации. Должен совпадать с `OPENAI_API_KEY`.  
### Open WebUI[​](<#open-webui> "Direct link to Open WebUI")
Переменная| Описание  
|---|---  
`OPENAI_API_BASE_URL`| URL API Hermes Agent (включая `/v1`)  
`OPENAI_API_KEY`| Должен быть непустым. Должен совпадать с вашим `API_SERVER_KEY`.  
## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")
### Модели не отображаются в выпадающем списке[​](<#no-models-appear-in-the-dropdown> "Direct link to No models appear in the dropdown")
  * **Проверьте наличие суффикса`/v1` в URL**: `http://host.docker.internal:8642/v1` (не просто `:8642`)
  * **Убедитесь, что шлюз работает**: `curl http://localhost:8642/health` должен вернуть `{"status": "ok"}`
  * **Проверьте список моделей**: `curl -H "Authorization: Bearer your-secret-key" http://localhost:8642/v1/models` должен вернуть список с `hermes-agent`
  * **Сетевое взаимодействие Docker**: Изнутри Docker `localhost` означает контейнер, а не ваш хост. Используйте `host.docker.internal` или `--network=host`.
  * **Пустой бэкенд Ollama перекрывает выбор моделей**: Если вы опустили `ENABLE_OLLAMA_API=false`, Open WebUI отображает пустую секцию Ollama над моделями Hermes. Перезапустите контейнер с `-e ENABLE_OLLAMA_API=false` или отключите Ollama в **Admin Settings → Connections**.


### Тест подключения проходит, но модели не загружаются[​](<#connection-test-passes-but-no-models-load> "Direct link to Connection test passes but no models load")
Почти всегда это отсутствие суффикса `/v1`. Тест подключения Open WebUI — это базовая проверка связности, он не проверяет загрузку списка моделей.
### Ответ занимает много времени[​](<#response-takes-a-long-time> "Direct link to Response takes a long time")
Hermes Agent может выполнять несколько вызовов инструментов (чтение файлов, запуск команд, поиск в Интернете) перед формированием финального ответа. Это нормально для сложных запросов. Ответ появляется целиком, когда агент завершает работу.
### Ошибки «Invalid API key»[​](<#invalid-api-key-errors> "Direct link to \"Invalid API key\" errors")
Убедитесь, что ваш `OPENAI_API_KEY` в Open WebUI соответствует `API_SERVER_KEY` в Hermes Agent.
warning
Open WebUI сохраняет настройки OpenAI-совместимых подключений в своей собственной базе данных после первого запуска. Если вы случайно сохранили неверный ключ в интерфейсе администратора, исправления переменных окружения недостаточно — обновите или удалите сохранённое подключение в **Admin Settings → Connections** или сбросьте каталог данных / базу данных Open WebUI.
## Многопользовательская настройка с профилями[​](<#multi-user-setup-with-profiles> "Direct link to Multi-User Setup with Profiles")
Чтобы запускать отдельные экземпляры Hermes для каждого пользователя — с собственными настройками, памятью и навыками — используйте [профили](</docs/user-guide/profiles>). Каждый профиль запускает свой собственный API-сервер на отдельном порту и автоматически указывает имя профиля как модель в Open WebUI.
### 1\. Создание профилей и настройка API-серверов[​](<#1-create-profiles-and-configure-api-servers> "Direct link to 1. Create profiles and configure API servers")
[code] 
    hermes profile create alice  
    hermes -p alice config set API_SERVER_ENABLED true  
    hermes -p alice config set API_SERVER_PORT 8643  
    hermes -p alice config set API_SERVER_KEY alice-secret  
      
    hermes profile create bob  
    hermes -p bob config set API_SERVER_ENABLED true  
    hermes -p bob config set API_SERVER_PORT 8644  
    hermes -p bob config set API_SERVER_KEY bob-secret  
    
[/code]
### 2\. Запуск каждого шлюза[​](<#2-start-each-gateway> "Direct link to 2. Start each gateway")
[code] 
    hermes -p alice gateway &  
    hermes -p bob gateway &  
    
[/code]
### 3\. Добавление подключений в Open WebUI[​](<#3-add-connections-in-open-webui> "Direct link to 3. Add connections in Open WebUI")
В **Admin Settings** → **Connections** → **OpenAI API** → **Manage** добавьте по одному подключению для каждого профиля:
Подключение| URL| API Key  
|---|---|---  
Alice| `http://host.docker.internal:8643/v1`| `alice-secret`  
Bob| `http://host.docker.internal:8644/v1`| `bob-secret`  
В выпадающем списке моделей появятся `alice` и `bob` как отдельные модели. Вы можете назначать модели пользователям Open WebUI через панель администратора, предоставляя каждому пользователю своего изолированного агента Hermes.
Custom Model Names
Имя модели по умолчанию соответствует имени профиля. Чтобы переопределить его, установите `API_SERVER_MODEL_NAME` в `.env` профиля:
[code]
    hermes -p alice config set API_SERVER_MODEL_NAME "Alice's Agent"
    
[/code]
## Linux Docker (без Docker Desktop)[​](<#linux-docker-no-docker-desktop> "Direct link to Linux Docker (no Docker Desktop)")
На Linux без Docker Desktop `host.docker.internal` не разрешается по умолчанию. Варианты:
[code] 
    # Вариант 1: Добавить сопоставление хоста  
    docker run --add-host=host.docker.internal:host-gateway ...  
      
    # Вариант 2: Использовать host-сеть  
    docker run --network=host -e OPENAI_API_BASE_URL=http://localhost:8642/v1 ...  
      
    # Вариант 3: Использовать IP моста Docker  
    docker run -e OPENAI_API_BASE_URL=http://172.17.0.1:8642/v1 ...  
    
[/code]
  * [Архитектура](<#architecture>)
  * [Быстрая настройка](<#quick-setup>)
    * [Быстрый локальный запуск одной командой (macOS/Linux, без Docker)](<#one-command-local-bootstrap-macoslinux-no-docker>)
    * [1\. Включение API-сервера](<#1-enable-the-api-server>)
    * [2\. Запуск шлюза Hermes Agent](<#2-start-hermes-agent-gateway>)
    * [3\. Проверка доступности API-сервера](<#3-verify-the-api-server-is-reachable>)
    * [4\. Запуск Open WebUI](<#4-start-open-webui>)
    * [5\. Открытие интерфейса](<#5-open-the-ui>)
  * [Настройка через Docker Compose](<#docker-compose-setup>)
  * [Настройка через интерфейс администратора](<#configuring-via-the-admin-ui>)
  * [Тип API: Chat Completions vs Responses](<#api-type-chat-completions-vs-responses>)
    * [Использование Chat Completions (рекомендуется)](<#using-chat-completions-recommended>)
    * [Использование Responses API](<#using-responses-api>)
  * [Как это работает](<#how-it-works>)
  * [Справочник по настройке](<#configuration-reference>)
    * [Hermes Agent (API-сервер)](<#hermes-agent-api-server>)
    * [Open WebUI](<#open-webui>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Модели не отображаются в выпадающем списке](<#no-models-appear-in-the-dropdown>)
    * [Тест подключения проходит, но модели не загружаются](<#connection-test-passes-but-no-models-load>)
    * [Ответ занимает много времени](<#response-takes-a-long-time>)
    * [Ошибки «Invalid API key»](<#invalid-api-key-errors>)
  * [Многопользовательская настройка с профилями](<#multi-user-setup-with-profiles>)
    * [1\. Создание профилей и настройка API-серверов](<#1-create-profiles-and-configure-api-servers>)
    * [2\. Запуск каждого шлюза](<#2-start-each-gateway>)
    * [3\. Добавление подключений в Open WebUI](<#3-add-connections-in-open-webui>)
  * [Linux Docker (без Docker Desktop)](<#linux-docker-no-docker-desktop>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui -->
