На этой странице

Есть два различных способа, которыми Docker пересекается с Hermes Agent:
  1. **Запуск Hermes В Docker** — сам агент работает внутри контейнера (основной фокус этой страницы)
  2. **Docker как терминальный бэкенд** — агент работает на вашем хосте, но каждую команду выполняет внутри одного постоянного контейнера-песочницы Docker, который сохраняется между вызовами инструментов, `/new` и сабагентами на всё время жизни процесса Hermes (см. [Конфигурация → Docker Backend](</docs/user-guide/configuration#docker-backend>))

Эта страница описывает вариант 1. Контейнер хранит все пользовательские данные (конфигурацию, ключи API, сессии, навыки, память) в единственном каталоге, смонтированном с хоста в `/opt/data`. Образ сам по себе не имеет состояния и может быть обновлён путём загрузки новой версии без потери каких-либо настроек.

## Быстрый старт[​](<#quick-start> "Direct link to Quick start")

Если вы запускаете Hermes Agent впервые, создайте каталог для данных на хосте и запустите контейнер в интерактивном режиме для работы мастера настройки:

[code]
    mkdir -p ~/.hermes
    docker run -it --rm \
      -v ~/.hermes:/opt/data \
      nousresearch/hermes-agent setup
    
[/code]

Это запустит мастер настройки, который запросит ваши ключи API и запишет их в `~/.hermes/.env`. Это нужно сделать только один раз. Настоятельно рекомендуется настроить систему чатов для работы шлюза на этом этапе.

## Запуск в режиме шлюза[​](<#running-in-gateway-mode> "Direct link to Running in gateway mode")

После настройки запустите контейнер в фоновом режиме как постоянный шлюз (Telegram, Discord, Slack, WhatsApp и т.д.):

[code]
    docker run -d \
      --name hermes \
      --restart unless-stopped \
      -v ~/.hermes:/opt/data \
      -p 8642:8642 \
      nousresearch/hermes-agent gateway run
    
[/code]

Порт 8642 открывает [OpenAI-совместимый API-сервер](</docs/user-guide/features/api-server>) шлюза и endpoint для проверки здоровья. Он опционален, если вы используете только чат-платформы (Telegram, Discord и т.д.), но обязателен, если вам нужна панель управления или внешние инструменты для доступа к шлюзу.

Примечание: API-сервер включается только при `API_SERVER_ENABLED=true`. Чтобы открыть доступ за пределы `127.0.0.1` внутри контейнера, также укажите `API_SERVER_HOST=0.0.0.0` и `API_SERVER_KEY` (минимум 8 символов — сгенерируйте с помощью `openssl rand -hex 32`). Пример:

[code]
    docker run -d \
      --name hermes \
      --restart unless-stopped \
      -v ~/.hermes:/opt/data \
      -p 8642:8642 \
      -e API_SERVER_ENABLED=true \
      -e API_SERVER_HOST=0.0.0.0 \
      -e API_SERVER_KEY=your_api_key_here \
      -e API_SERVER_CORS_ORIGINS='*' \
      nousresearch/hermes-agent gateway run
    
[/code]

Открытие любого порта на машине, подключённой к интернету, представляет угрозу безопасности. Не делайте этого, если не понимаете риски.

## Запуск панели управления[​](<#running-the-dashboard> "Direct link to Running the dashboard")

Встроенная веб-панель управления запускается как опциональный дополнительный процесс внутри того же контейнера, что и шлюз. Установите `HERMES_DASHBOARD=1` и откройте порт `9119` вместе с портом шлюза `8642`:

[code]
    docker run -d \
      --name hermes \
      --restart unless-stopped \
      -v ~/.hermes:/opt/data \
      -p 8642:8642 \
      -p 9119:9119 \
      -e HERMES_DASHBOARD=1 \
      nousresearch/hermes-agent gateway run
    
[/code]

Точка входа запускает `hermes dashboard` в фоновом режиме (от имени непривилегированного пользователя `hermes`) перед `exec` основного команды. Вывод панели управления помечается префиксом `[dashboard]` в `docker logs`, что позволяет легко отделить его от логов шлюза.

| Переменная окружения | Описание | По умолчанию |
|---|---|---|
| `HERMES_DASHBOARD` | Установите в `1` (или `true` / `yes`) для запуска панели управления вместе с основной командой | _(не задана — панель не запускается)_ |
| `HERMES_DASHBOARD_HOST` | Адрес привязки HTTP-сервера панели управления | `0.0.0.0` |
| `HERMES_DASHBOARD_PORT` | Порт HTTP-сервера панели управления | `9119` |
| `HERMES_DASHBOARD_TUI` | Установите в `1` для включения встроенной вкладки чата в браузере (встроенный `hermes --tui` через PTY/WebSocket) | _(не задана)_ |

Значение по умолчанию `HERMES_DASHBOARD_HOST=0.0.0.0` необходимо, чтобы хост мог обращаться к панели управления через опубликованный порт; точка входа автоматически передаёт `--insecure` в `hermes dashboard` в этом случае. Переопределите на `127.0.0.1`, если хотите ограничить доступ к панели управления только изнутри контейнера (например, за обратным прокси в соседнем контейнере).

note

Дополнительный процесс панели управления **не контролируется** — если он завершится с ошибкой, он останется остановленным до перезапуска контейнера. Запуск панели управления в отдельном контейнере не поддерживается: обнаружение активности шлюза панелью требует общего пространства имён PID с процессом шлюза.

## Интерактивный запуск (CLI-чат)[​](<#running-interactively-cli-chat> "Direct link to Running interactively (CLI chat)")

Чтобы открыть интерактивную сессию чата с существующим каталогом данных:

[code]
    docker run -it --rm \
      -v ~/.hermes:/opt/data \
      nousresearch/hermes-agent
    
[/code]

Или, если вы уже открыли терминал в запущенном контейнере (например, через Docker Desktop), просто выполните:

[code]
    /opt/hermes/.venv/bin/hermes
    
[/code]

## Постоянные тома[​](<#persistent-volumes> "Direct link to Persistent volumes")

Том `/opt/data` является единственным источником истины для всего состояния Hermes. Он отображается в каталог `~/.hermes/` на вашем хосте и содержит:

| Путь | Содержимое |
|---|---|
| `.env` | Ключи API и секреты |
| `config.yaml` | Вся конфигурация Hermes |
| `SOUL.md` | Личность/идентичность агента |
| `sessions/` | История разговоров |
| `memories/` | Постоянное хранилище памяти |
| `skills/` | Установленные навыки |
| `cron/` | Определения запланированных задач |
| `hooks/` | Хуки событий |
| `logs/` | Журналы выполнения |
| `skins/` | Пользовательские темы CLI |

warning

Никогда не запускайте два контейнера **шлюза** Hermes одновременно против одного и того же каталога данных — файлы сессий и хранилища памяти не предназначены для конкурентной записи.

## Поддержка нескольких профилей[​](<#multi-profile-support> "Direct link to Multi-profile support")

Hermes поддерживает [несколько профилей](</docs/reference/profile-commands>) — отдельные каталоги `~/.hermes/`, позволяющие запускать независимых агентов (разные SOUL, навыки, память, сессии, учётные данные) из одной установки. **При работе под Docker использовать встроенную функцию нескольких профилей Hermes не рекомендуется.**

Вместо этого рекомендуется шаблон **один контейнер на профиль**, где каждый контейнер монтирует свой собственный каталог хоста как `/opt/data`:

[code]
    # Рабочий профиль
    docker run -d \
      --name hermes-work \
      --restart unless-stopped \
      -v ~/.hermes-work:/opt/data \
      -p 8642:8642 \
      nousresearch/hermes-agent gateway run
      
    # Личный профиль
    docker run -d \
      --name hermes-personal \
      --restart unless-stopped \
      -v ~/.hermes-personal:/opt/data \
      -p 8643:8642 \
      nousresearch/hermes-agent gateway run
    
[/code]

Почему отдельные контейнеры предпочтительнее профилей в Docker:

  * **Изоляция** — каждый контейнер имеет свою файловую систему, таблицу процессов и ограничения ресурсов. Сбой, изменение зависимостей или вышедшая из-под контроля сессия в одном профиле не могут повлиять на другой.
  * **Независимый жизненный цикл** — обновляйте, перезапускайте, приостанавливайте или откатывайте каждого агента отдельно (`docker restart hermes-work` не затрагивает `hermes-personal`).
  * **Чистое разделение портов и сети** — каждый шлюз привязывается к своему порту хоста; нет риска перекрёстного взаимодействия между чат-платформами или API-серверами.
  * **Более простая ментальная модель** — контейнер _и есть_ профиль. Резервное копирование, миграции и права доступа следуют за смонтированным каталогом, без необходимости запоминать дополнительные флаги `--profile`.
  * **Избегает риска конкурентной записи** — предупреждение выше о недопустимости запуска двух шлюзов против одного каталога данных также применимо к профилям внутри одного контейнера.

В Docker Compose это означает объявление одного сервиса на профиль с разными `container_name`, `volumes` и `ports`:

[code]
    services:
      hermes-work:
        image: nousresearch/hermes-agent:latest
        container_name: hermes-work
        restart: unless-stopped
        command: gateway run
        ports:
          - "8642:8642"
        volumes:
          - ~/.hermes-work:/opt/data
      
      hermes-personal:
        image: nousresearch/hermes-agent:latest
        container_name: hermes-personal
        restart: unless-stopped
        command: gateway run
        ports:
          - "8643:8642"
        volumes:
          - ~/.hermes-personal:/opt/data
    
[/code]

## Передача переменных окружения[​](<#environment-variable-forwarding> "Direct link to Environment variable forwarding")

Ключи API считываются из `/opt/data/.env` внутри контейнера. Вы также можете передавать переменные окружения напрямую:

[code]
    docker run -it --rm \
      -v ~/.hermes:/opt/data \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      -e OPENAI_API_KEY="sk-..." \
      nousresearch/hermes-agent
    
[/code]

Прямые флаги `-e` переопределяют значения из `.env`. Это полезно для CI/CD или интеграции с менеджерами секретов, где не нужно хранить ключи на диске.

## Пример Docker Compose[​](<#docker-compose-example> "Direct link to Docker Compose example")

Для постоянного развёртывания с шлюзом и панелью управления удобно использовать `docker-compose.yaml`:

[code]
    services:
      hermes:
        image: nousresearch/hermes-agent:latest
        container_name: hermes
        restart: unless-stopped
        command: gateway run
        ports:
          - "8642:8642"   # API шлюза
          - "9119:9119"   # панель управления (доступна только при HERMES_DASHBOARD=1)
        volumes:
          - ~/.hermes:/opt/data
        environment:
          - HERMES_DASHBOARD=1
          # Раскомментируйте для передачи конкретных переменных окружения вместо использования .env файла:
          # - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
          # - OPENAI_API_KEY=${OPENAI_API_KEY}
          # - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
        deploy:
          resources:
            limits:
              memory: 4G
              cpus: "2.0"
    
[/code]

Запустите с помощью `docker compose up -d` и просматривайте логи с помощью `docker compose logs -f`. Вывод панели управления помечается префиксом `[dashboard]`, что позволяет легко отфильтровать его от логов шлюза.

## Ограничения ресурсов[​](<#resource-limits> "Direct link to Resource limits")

Контейнеру Hermes требуются умеренные ресурсы. Рекомендуемые минимумы:

| Ресурс | Минимум | Рекомендуется |
|---|---|---|
| Память | 1 ГБ | 2–4 ГБ |
| CPU | 1 ядро | 2 ядра |
| Диск (том данных) | 500 МБ | 2+ ГБ (растёт с сессиями/навыками) |

Автоматизация браузера (Playwright/Chromium) — самая требовательная к памяти функция. Если вам не нужны инструменты браузера, 1 ГБ достаточно. При активных инструментах браузера выделяйте не менее 2 ГБ.

Установка ограничений в Docker:

[code]
    docker run -d \
      --name hermes \
      --restart unless-stopped \
      --memory=4g --cpus=2 \
      -v ~/.hermes:/opt/data \
      nousresearch/hermes-agent gateway run
    
[/code]

## Что делает Dockerfile[​](<#what-the-dockerfile-does> "Direct link to What the Dockerfile does")

Официальный образ основан на `debian:13.4` и включает:

  * Python 3 со всеми зависимостями Hermes (`uv pip install -e ".[all]"`)
  * Node.js + npm (для автоматизации браузера и моста WhatsApp)
  * Playwright с Chromium (`npx playwright install --with-deps chromium --only-shell`)
  * ripgrep, ffmpeg, git и tini как системные утилиты
  * **`docker-cli`** — чтобы агенты, работающие внутри контейнера, могли управлять Docker-демоном хоста (примонтируйте `/var/run/docker.sock`, чтобы включить) для `docker build`, `docker run`, инспекции контейнеров и т.д.
  * **`openssh-client`** — включает [SSH терминальный бэкенд](</docs/user-guide/configuration#ssh-backend>) изнутри контейнера. SSH бэкенд вызывает системный бинарник `ssh`; без этого он молча не работал в контейнерных установках.
  * Мост WhatsApp (`scripts/whatsapp-bridge/`)

Скрипт точки входа (`docker/entrypoint.sh`) инициализирует том данных при первом запуске:

  * Создаёт структуру каталогов (`sessions/`, `memories/`, `skills/` и т.д.)
  * Копирует `.env.example` → `.env`, если `.env` не существует
  * Копирует `config.yaml` по умолчанию, если отсутствует
  * Копирует `SOUL.md` по умолчанию, если отсутствует
  * Синхронизирует встроенные навыки, используя подход на основе манифеста (сохраняет изменения пользователя)
  * Опционально запускает `hermes dashboard` как фоновый дополнительный процесс при `HERMES_DASHBOARD=1` (см. [Запуск панели управления](<#running-the-dashboard>))
  * Затем запускает `hermes` с переданными вами аргументами

## Обновление[​](<#upgrading> "Direct link to Upgrading")

Загрузите последний образ и пересоздайте контейнер. Ваш каталог данных остаётся нетронутым.

[code]
    docker pull nousresearch/hermes-agent:latest
    docker rm -f hermes
    docker run -d \
      --name hermes \
      --restart unless-stopped \
      -v ~/.hermes:/opt/data \
      nousresearch/hermes-agent gateway run
    
[/code]

Или с Docker Compose:

[code]
    docker compose pull
    docker compose up -d
    
[/code]

## Навыки и файлы учётных данных[​](<#skills-and-credential-files> "Direct link to Skills and credential files")

При использовании Docker в качестве среды выполнения (не описанными выше методами, а когда агент выполняет команды внутри Docker-песочницы — см. [Конфигурация → Docker Backend](</docs/user-guide/configuration#docker-backend>)), Hermes повторно использует один долгоживущий контейнер для всех вызовов инструментов и автоматически монтирует каталог навыков (`~/.hermes/skills/`) и любые файлы учётных данных, объявленные навыками, в этот контейнер как тома только для чтения. Скрипты навыков, шаблоны и ссылки доступны внутри песочницы без ручной настройки, и поскольку контейнер сохраняется на всё время жизни процесса Hermes, любые установленные вами зависимости или записанные файлы остаются для следующего вызова инструмента.

Та же синхронизация происходит для бэкендов SSH и Modal — навыки и файлы учётных данных загружаются через rsync или API монтирования Modal перед каждой командой.

## Подключение к локальным серверам инференса (vLLM, Ollama и т.д.)[​](<#connecting-to-local-inference-servers-vllm-ollama-etc> "Direct link to Connecting to local inference servers (vLLM, Ollama, etc.)")

При запуске Hermes в Docker, когда ваш сервер инференса (vLLM, Ollama, text-generation-inference и т.д.) также работает на хосте или в другом контейнере, сетевому взаимодействию требуется дополнительное внимание.

### Docker Compose (рекомендуется)[​](<#docker-compose-recommended> "Direct link to Docker Compose (recommended)")

Поместите оба сервиса в одну сеть Docker. Это наиболее надёжный подход:

[code]
    services:
      vllm:
        image: vllm/vllm-openai:latest
        container_name: vllm
        command: >
          --model Qwen/Qwen2.5-7B-Instruct
          --served-model-name my-model
          --host 0.0.0.0
          --port 8000
        ports:
          - "8000:8000"
        networks:
          - hermes-net
        deploy:
          resources:
            reservations:
              devices:
                - capabilities: [gpu]
      
      hermes:
        image: nousresearch/hermes-agent:latest
        container_name: hermes
        restart: unless-stopped
        command: gateway run
        ports:
          - "8642:8642"
        volumes:
          - ~/.hermes:/opt/data
        networks:
          - hermes-net
      
    networks:
      hermes-net:
        driver: bridge
    
[/code]

Затем в вашем `~/.hermes/config.yaml` используйте **имя контейнера** в качестве имени хоста:

[code]
    model:
      provider: custom
      model: my-model
      base_url: http://vllm:8000/v1
      api_key: "none"
    
[/code]

Ключевые моменты

  * Используйте **имя контейнера** (`vllm`) в качестве имени хоста — не `localhost` или `127.0.0.1`, которые относятся к самому контейнеру Hermes.
  * Значение `model` должно совпадать с `--served-model-name`, переданным vLLM.
  * Установите `api_key` в любую непустую строку (vLLM требует заголовок, но по умолчанию его не проверяет).
  * Не добавляйте завершающий слеш в `base_url`.

### Отдельный запуск Docker (без Compose)[​](<#standalone-docker-run-no-compose> "Direct link to Standalone Docker run (no Compose)")

Если ваш сервер инференса работает непосредственно на хосте (не в Docker), используйте `host.docker.internal` на macOS/Windows или `--network host` на Linux:

**macOS / Windows:**

[code]
    docker run -d \
      --name hermes \
      -v ~/.hermes:/opt/data \
      -p 8642:8642 \
      nousresearch/hermes-agent gateway run
    
[/code]

[code]
    # config.yaml
    model:
      provider: custom
      model: my-model
      base_url: http://host.docker.internal:8000/v1
      api_key: "none"
    
[/code]

**Linux (сетевое взаимодействие хоста):**

[code]
    docker run -d \
      --name hermes \
      --network host \
      -v ~/.hermes:/opt/data \
      nousresearch/hermes-agent gateway run
    
[/code]

[code]
    # config.yaml
    model:
      provider: custom
      model: my-model
      base_url: http://127.0.0.1:8000/v1
      api_key: "none"
    
[/code]

С флагом `--network host` флаг `-p` игнорируется — все порты контейнера напрямую открыты на хосте.

### Проверка подключения[​](<#verifying-connectivity> "Direct link to Verifying connectivity")

Изнутри контейнера Hermes убедитесь, что сервер инференса доступен:

[code]
    docker exec hermes curl -s http://vllm:8000/v1/models
    
[/code]

Вы должны увидеть JSON-ответ со списком вашей обслуживаемой модели. Если это не сработало, проверьте:

  1. Оба контейнера находятся в одной сети Docker (`docker network inspect hermes-net`)
  2. Сервер инференса слушает на `0.0.0.0`, а не на `127.0.0.1`
  3. Номер порта совпадает

### Ollama[​](<#ollama> "Direct link to Ollama")

Ollama работает так же. Если Ollama запущен на хосте, используйте `host.docker.internal:11434` (macOS/Windows) или `127.0.0.1:11434` (Linux с `--network host`). Если Ollama работает в своём собственном контейнере в той же сети Docker:

[code]
    model:
      provider: custom
      model: llama3
      base_url: http://ollama:11434/v1
      api_key: "none"
    
[/code]

## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")

### Контейнер немедленно завершает работу[​](<#container-exits-immediately> "Direct link to Container exits immediately")

Проверьте логи: `docker logs hermes`. Распространённые причины:

  * Отсутствует или недействителен файл `.env` — сначала запустите интерактивно для завершения настройки
  * Конфликт портов при запуске с открытыми портами

### Ошибки "Permission denied"[​](<#permission-denied-errors> "Direct link to \"Permission denied\" errors")

Точка входа контейнера понижает привилегии до непривилегированного пользователя `hermes` (UID 10000) через `gosu`. Если ваш каталог хоста `~/.hermes/` принадлежит другому UID, установите `HERMES_UID`/`HERMES_GID` в соответствие с вашим пользователем хоста или убедитесь, что каталог данных доступен для записи:

[code]
    chmod -R 755 ~/.hermes
    
[/code]

### Инструменты браузера не работают[​](<#browser-tools-not-working> "Direct link to Browser tools not working")

Playwright требует разделяемую память. Добавьте `--shm-size=1g` в вашу команду Docker run:

[code]
    docker run -d \
      --name hermes \
      --shm-size=1g \
      -v ~/.hermes:/opt/data \
      nousresearch/hermes-agent gateway run
    
[/code]

### Шлюз не переподключается после сетевых проблем[​](<#gateway-not-reconnecting-after-network-issues> "Direct link to Gateway not reconnecting after network issues")

Флаг `--restart unless-stopped` обрабатывает большинство временных сбоев. Если шлюз завис, перезапустите контейнер:

[code]
    docker restart hermes
    
[/code]

### Проверка здоровья контейнера[​](<#checking-container-health> "Direct link to Checking container health")

[code]
    docker logs --tail 50 hermes          # Последние логи
    docker run -it --rm nousresearch/hermes-agent:latest version     # Проверка версии
    docker stats hermes                    # Использование ресурсов
    
[/code]

  * [Быстрый старт](<#quick-start>)
  * [Запуск в режиме шлюза](<#running-in-gateway-mode>)
  * [Запуск панели управления](<#running-the-dashboard>)
  * [Интерактивный запуск (CLI-чат)](<#running-interactively-cli-chat>)
  * [Постоянные тома](<#persistent-volumes>)
  * [Поддержка нескольких профилей](<#multi-profile-support>)
  * [Передача переменных окружения](<#environment-variable-forwarding>)
  * [Пример Docker Compose](<#docker-compose-example>)
  * [Ограничения ресурсов](<#resource-limits>)
  * [Что делает Dockerfile](<#what-the-dockerfile-does>)
  * [Обновление](<#upgrading>)
  * [Навыки и файлы учётных данных](<#skills-and-credential-files>)
  * [Подключение к локальным серверам инференса (vLLM, Ollama и т.д.)](<#connecting-to-local-inference-servers-vllm-ollama-etc>)
    * [Docker Compose (рекомендуется)](<#docker-compose-recommended>)
    * [Отдельный запуск Docker (без Compose)](<#standalone-docker-run-no-compose>)
    * [Проверка подключения](<#verifying-connectivity>)
    * [Ollama](<#ollama>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Контейнер немедленно завершает работу](<#container-exits-immediately>)
    * [Ошибки "Permission denied"](<#permission-denied-errors>)
    * [Инструменты браузера не работают](<#browser-tools-not-working>)
    * [Шлюз не переподключается после сетевых проблем](<#gateway-not-reconnecting-after-network-issues>)
    * [Проверка здоровья контейнера](<#checking-container-health>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/docker -->
