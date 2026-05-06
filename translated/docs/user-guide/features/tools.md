On this page

Инструменты — это функции, расширяющие возможности агента. Они организованы в логические **наборы инструментов (toolsets)**, которые можно включать или отключать для каждой платформы.

## Доступные инструменты[​](<#available-tools> "Прямая ссылка на Доступные инструменты")

Hermes поставляется с обширным встроенным реестром инструментов, охватывающим веб-поиск, автоматизацию браузера, выполнение команд в терминале, редактирование файлов, память, делегирование, обучение с подкреплением, доставку сообщений, Home Assistant и многое другое.

note
**Honcho cross-session memory** доступна как плагин провайдера памяти (`plugins/memory/honcho/`), а не как встроенный набор инструментов. Установку см. в разделе [Плагины](</docs/user-guide/features/plugins>).

Категории верхнего уровня:

Категория| Примеры| Описание  
---|---|---  
**Веб**| `web_search`, `web_extract`| Поиск в интернете и извлечение содержимого страниц.  
**Терминал и файлы**| `terminal`, `process`, `read_file`, `patch`| Выполнение команд и работа с файлами.  
**Браузер**| `browser_navigate`, `browser_snapshot`, `browser_vision`| Интерактивная автоматизация браузера с поддержкой текста и зрения.  
**Медиа**| `vision_analyze`, `image_generate`, `text_to_speech`| Мультимодальный анализ и генерация.  
**Оркестрация агентов**| `todo`, `clarify`, `execute_code`, `delegate_task`| Планирование, уточнение, выполнение кода и делегирование подагентам.  
**Память и поиск**| `memory`, `session_search`| Постоянная память и поиск по сессиям.  
**Автоматизация и доставка**| `cronjob`, `send_message`| Запланированные задачи с действиями создания/списка/обновления/паузы/возобновления/запуска/удаления, а также доставка исходящих сообщений.  
**Интеграции**| `ha_*`, серверные инструменты MCP, `rl_*`| Home Assistant, MCP, обучение с подкреплением и другие интеграции.  

Актуальный реестр на основе кода см. в [Справочнике встроенных инструментов](</docs/reference/tools-reference>) и [Справочнике наборов инструментов](</docs/reference/toolsets-reference>).

Nous Tool Gateway

Платные подписчики [Nous Portal](<https://portal.nousresearch.com>) могут использовать веб-поиск, генерацию изображений, TTS и автоматизацию браузера через **[Tool Gateway](</docs/user-guide/features/tool-gateway>)** — без отдельных API-ключей. Выполните `hermes model` для его включения или настройте отдельные инструменты с помощью `hermes tools`.

## Использование наборов инструментов[​](<#using-toolsets> "Прямая ссылка на Использование наборов инструментов")

[code] 
    # Использование определённых наборов инструментов  
    hermes chat --toolsets "web,terminal"  
      
    # Просмотр всех доступных инструментов  
    hermes tools  
      
    # Настройка инструментов для каждой платформы (интерактивно)  
    hermes tools  
    
[/code]

Распространённые наборы инструментов включают `web`, `search`, `terminal`, `file`, `browser`, `vision`, `image_gen`, `moa`, `skills`, `tts`, `todo`, `memory`, `session_search`, `cronjob`, `code_execution`, `delegation`, `clarify`, `homeassistant`, `messaging`, `spotify`, `discord`, `discord_admin`, `debugging`, `safe` и `rl`.

Полный перечень см. в [Справочнике наборов инструментов](</docs/reference/toolsets-reference>), включая предустановки платформ, такие как `hermes-cli`, `hermes-telegram`, и динамические MCP-наборы, такие как `mcp-<server>`.

## Бэкенды терминала[​](<#terminal-backends> "Прямая ссылка на Бэкенды терминала")

Инструмент терминала может выполнять команды в разных средах:

Бэкенд| Описание| Сценарий использования  
---|---|---  
`local`| Запуск на вашей машине (по умолчанию)| Разработка, доверенные задачи  
`docker`| Изолированные контейнеры| Безопасность, воспроизводимость  
`ssh`| Удалённый сервер| Песочница, изоляция агента от его собственного кода  
`singularity`| HPC-контейнеры| Кластерные вычисления, без root  
`modal`| Облачное выполнение| Бессерверные вычисления, масштабирование  
`daytona`| Облачная рабочая среда-песочница| Постоянные удалённые среды разработки  
`vercel_sandbox`| Облачная микро-ВМ Vercel Sandbox| Облачное выполнение с сохраняемой снапшотами файловой системой  

### Конфигурация[​](<#configuration> "Прямая ссылка на Конфигурацию")

[code] 
    # В ~/.hermes/config.yaml  
    terminal:  
      backend: local    # или: docker, ssh, singularity, modal, daytona, vercel_sandbox  
      cwd: "."          # Рабочая директория  
      timeout: 180      # Таймаут команды в секундах  
    
[/code]

### Docker Бэкенд[​](<#docker-backend> "Прямая ссылка на Docker Бэкенд")

[code] 
    terminal:  
      backend: docker  
      docker_image: python:3.11-slim  
    
[/code]

**Один постоянный контейнер, общий для всего процесса.** Hermes запускает единственный долгоживущий контейнер при первом использовании (`docker run -d ... sleep 2h`) и направляет каждый вызов терминала, файловых операций и `execute_code` через `docker exec` в тот же контейнер. Изменения рабочей директории, установленные пакеты, настройки окружения и файлы, записанные в `/workspace`, сохраняются между вызовами инструментов, включая `/new`, `/reset` и подагентов `delegate_task`, в течение всего времени жизни процесса Hermes. Контейнер останавливается и удаляется при завершении работы.

Это означает, что Docker-бэкенд ведёт себя как постоянная ВМ-песочница, а не как свежий контейнер для каждой команды. Если вы один раз выполнили `pip install foo`, пакет останется на всю сессию. Если вы выполнили `cd /workspace/project`, последующие вызовы `ls` увидят эту директорию. Полные детали жизненного цикла и флаг `container_persistent`, управляющий сохранением `/workspace` и `/root` между перезапусками Hermes, см. в разделе [Конфигурация → Docker Бэкенд](</docs/user-guide/configuration#docker-backend>).

### SSH Бэкенд[​](<#ssh-backend> "Прямая ссылка на SSH Бэкенд")

Рекомендуется для безопасности — агент не может изменять свой собственный код:

[code] 
    terminal:  
      backend: ssh  
    
[/code]

[code] 
    # Установка учётных данных в ~/.hermes/.env  
    TERMINAL_SSH_HOST=my-server.example.com  
    TERMINAL_SSH_USER=myuser  
    TERMINAL_SSH_KEY=~/.ssh/id_rsa  
    
[/code]

### Singularity/Apptainer[​](<#singularityapptainer> "Прямая ссылка на Singularity/Apptainer")

[code] 
    # Предварительная сборка SIF для параллельных воркеров  
    apptainer build ~/python.sif docker://python:3.11-slim  
      
    # Настройка  
    hermes config set terminal.backend singularity  
    hermes config set terminal.singularity_image ~/python.sif  
    
[/code]

### Modal (Бессерверное облако)[​](<#modal-serverless-cloud> "Прямая ссылка на Modal (Бессерверное облако)")

[code] 
    uv pip install modal  
    modal setup  
    hermes config set terminal.backend modal  
    
[/code]

### Vercel Sandbox[​](<#vercel-sandbox> "Прямая ссылка на Vercel Sandbox")

[code] 
    pip install 'hermes-agent[vercel]'  
    hermes config set terminal.backend vercel_sandbox  
    hermes config set terminal.vercel_runtime node24  
    
[/code]

Аутентификация требуется по всем трём параметрам: `VERCEL_TOKEN`, `VERCEL_PROJECT_ID` и `VERCEL_TEAM_ID`. Эта настройка с токеном доступа является поддерживаемым способом для развёртываний и обычных долгоживущих процессов Hermes на Render, Railway, Docker и аналогичных хостах. Поддерживаемые рантаймы: `node24`, `node22` и `python3.13`; Hermes по умолчанию использует `/vercel/sandbox` как удалённый корень рабочей области.

Для одноразовой локальной разработки Hermes также принимает кратковременные Vercel OIDC-токены:

[code] 
    VERCEL_OIDC_TOKEN="$(vc project token <project-name>)" hermes chat  
    
[/code]

Из привязанной директории проекта Vercel:

[code] 
    VERCEL_OIDC_TOKEN="$(vc project token)" hermes chat  
    
[/code]

С параметром `container_persistent: true` Hermes использует снапшоты Vercel для сохранения состояния файловой системы при пересоздании песочницы для той же задачи. Это может включать синхронизированные учётные данные Hermes, навыки и кэш-файлы внутри песочницы. Снапшоты не сохраняют работающие процессы, пространство PID или идентичность текущей песочницы.

Фоновые команды терминала используют общий процесс Hermes для нелокальных процессов: spawn, poll, wait, log и kill работают через стандартный инструмент управления процессами, пока песочница активна, но Hermes не предоставляет нативного восстановления отсоединённых процессов Vercel после очистки или перезапуска.

Оставляйте `container_disk` неустановленным или со значением общего умолчания `51200`; пользовательский размер диска не поддерживается для Vercel Sandbox и приведёт к ошибкам диагностики/создания бэкенда.

### Ресурсы контейнера[​](<#container-resources> "Прямая ссылка на Ресурсы контейнера")

Настройка CPU, памяти, диска и сохранения для всех контейнерных бэкендов:

[code] 
    terminal:  
      backend: docker  # или singularity, modal, daytona, vercel_sandbox  
      container_cpu: 1              # Ядра CPU (по умолчанию: 1)  
      container_memory: 5120        # Память в МБ (по умолчанию: 5 ГБ)  
      container_disk: 51200         # Диск в МБ (по умолчанию: 50 ГБ)  
      container_persistent: true    # Сохранять файловую систему между сессиями (по умолчанию: true)  
    
[/code]

Когда `container_persistent: true`, установленные пакеты, файлы и конфигурация сохраняются между сессиями.

### Безопасность контейнера[​](<#container-security> "Прямая ссылка на Безопасность контейнера")

Все контейнерные бэкенды работают с усиленной безопасностью:

  * Корневая файловая система только для чтения (Docker)
  * Все возможности Linux отозваны
  * Без повышения привилегий
  * Лимиты PID (256 процессов)
  * Полная изоляция пространств имён
  * Постоянная рабочая область через тома, а не через записываемый корневой слой

Docker может дополнительно получать явный разрешённый список переменных окружения через `terminal.docker_forward_env`, но перенаправленные переменные видны командам внутри контейнера, и их следует считать раскрытыми для этой сессии.

## Управление фоновыми процессами[​](<#background-process-management> "Прямая ссылка на Управление фоновыми процессами")

Запуск фоновых процессов и управление ими:

[code] 
    terminal(command="pytest -v tests/", background=true)  
    # Возвращает: {"session_id": "proc_abc123", "pid": 12345}  
      
    # Затем управление через инструмент process:  
    process(action="list")       # Показать все запущенные процессы  
    process(action="poll", session_id="proc_abc123")   # Проверить статус  
    process(action="wait", session_id="proc_abc123")   # Блокировать до завершения  
    process(action="log", session_id="proc_abc123")    # Полный вывод  
    process(action="kill", session_id="proc_abc123")   # Завершить  
    process(action="write", session_id="proc_abc123", data="y")  # Отправить ввод  
    
[/code]

Режим PTY (`pty=true`) включает интерактивные CLI-инструменты, такие как Codex и Claude Code.

## Поддержка Sudo[​](<#sudo-support> "Прямая ссылка на Поддержка Sudo")

Если команде требуется sudo, вам будет предложено ввести пароль (кэшируется на время сессии). Или установите `SUDO_PASSWORD` в `~/.hermes/.env`.

warning
На платформах обмена сообщениями, если sudo не удаётся, вывод содержит подсказку добавить `SUDO_PASSWORD` в `~/.hermes/.env`.

  * [Доступные инструменты](<#available-tools>)
  * [Использование наборов инструментов](<#using-toolsets>)
  * [Бэкенды терминала](<#terminal-backends>)
    * [Конфигурация](<#configuration>)
    * [Docker Бэкенд](<#docker-backend>)
    * [SSH Бэкенд](<#ssh-backend>)
    * [Singularity/Apptainer](<#singularityapptainer>)
    * [Modal (Бессерверное облако)](<#modal-serverless-cloud>)
    * [Vercel Sandbox](<#vercel-sandbox>)
    * [Ресурсы контейнера](<#container-resources>)
    * [Безопасность контейнера](<#container-security>)
  * [Управление фоновыми процессами](<#background-process-management>)
  * [Поддержка Sudo](<#sudo-support>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools -->
