На этой странице
Это руководство проведёт вас через настройку Telegram-бота на базе Hermes Agent, которым сможет пользоваться вся команда. В результате ваша команда получит общего AI-ассистента, которому можно писать для помощи с кодом, исследованиями, администрированием системы и многим другим — защищённого поштучной авторизацией пользователей.
## Что мы создаём[​](<#what-were-building> "Прямая ссылка на Что мы создаём")
Telegram-бот, который:
  * **Любой авторизованный член команды** может написать в личку за помощью — код-ревью, исследования, shell-команды, отладка
  * **Запускается на вашем сервере** с полным доступом к инструментам — терминал, редактирование файлов, веб-поиск, выполнение кода
  * **Индивидуальные сессии** — у каждого пользователя свой контекст беседы
  * **Безопасен по умолчанию** — только одобренные пользователи могут взаимодействовать, два метода авторизации
  * **Запланированные задачи** — ежедневные стендапы, проверки здоровья и напоминания, доставляемые в командный канал


* * *
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
Перед началом убедитесь, что у вас есть:
  * **Hermes Agent установлен** на сервере или VPS (не на ноутбуке — бот должен работать постоянно). Следуйте [руководству по установке](</docs/getting-started/installation>), если ещё не сделали этого.
  * **Аккаунт Telegram** для себя (владельца бота)
  * **Настроен LLM-провайдер** — как минимум API-ключ для OpenAI, Anthropic или другого поддерживаемого провайдера в `~/.hermes/.env`


tip
VPS за $5/месяц более чем достаточно для запуска шлюза. Сам Hermes лёгковесный — затраты идут на LLM API-вызовы, которые выполняются удалённо.
* * *
## Шаг 1: Создайте Telegram-бота[​](<#step-1-create-a-telegram-bot> "Прямая ссылка на Шаг 1: Создайте Telegram-бота")
Каждый Telegram-бот начинается с **@BotFather** — официального бота Telegram для создания ботов.
  1. **Откройте Telegram** и найдите `@BotFather` или перейдите по ссылке [t.me/BotFather](<https://t.me/BotFather>)
  2. **Отправьте`/newbot`** — BotFather задаст два вопроса:
     * **Отображаемое имя** — то, что видят пользователи (например, `Team Hermes Assistant`)
     * **Имя пользователя** — должно заканчиваться на `bot` (например, `myteam_hermes_bot`)
  3. **Скопируйте токен бота** — BotFather ответит примерно таким сообщением:
[code] Use this token to access the HTTP API:  
         7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...  
         
[/code]
Сохраните этот токен — он понадобится на следующем шаге.
  4. **Установите описание** (необязательно, но рекомендуется):
[code] /setdescription  
         
[/code]
Выберите своего бота, затем введите что-то вроде:
[code] Team AI assistant powered by Hermes Agent. DM me for help with code, research, debugging, and more.  
         
[/code]
  5. **Установите команды бота** (необязательно — даёт пользователям меню команд):
[code] /setcommands  
         
[/code]
Выберите своего бота, затем вставьте:
[code] new - Start a fresh conversation  
         model - Show or change the AI model  
         status - Show session info  
         help - Show available commands  
         stop - Stop the current task  
         
[/code]


warning
Держите токен бота в секрете. Любой, у кого есть токен, может управлять ботом. Если токен утёк, используйте `/revoke` в BotFather для生成 нового.
* * *
## Шаг 2: Настройте шлюз[​](<#step-2-configure-the-gateway> "Прямая ссылка на Шаг 2: Настройте шлюз")
У вас есть два варианта: интерактивный мастер настройки (рекомендуется) или ручная конфигурация.
### Вариант A: Интерактивная настройка (рекомендуется)[​](<#option-a-interactive-setup-recommended> "Прямая ссылка на Вариант A: Интерактивная настройка (рекомендуется)")
[code] 
    hermes gateway setup  
    
[/code]
Мастер проведёт вас через все этапы с выбором с помощью стрелок. Выберите **Telegram**, вставьте токен бота и введите свой ID пользователя по запросу.
### Вариант B: Ручная настройка[​](<#option-b-manual-configuration> "Прямая ссылка на Вариант B: Ручная настройка")
Добавьте эти строки в `~/.hermes/.env`:
[code] 
    # Telegram bot token from BotFather  
    TELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...  
      
    # Your Telegram user ID (numeric)  
    TELEGRAM_ALLOWED_USERS=123456789  
    
[/code]
### Как узнать свой ID пользователя[​](<#finding-your-user-id> "Прямая ссылка на Как узнать свой ID пользователя")
Ваш ID пользователя Telegram — это числовое значение (не имя пользователя). Чтобы узнать его:
  1. Напишите [@userinfobot](<https://t.me/userinfobot>) в Telegram
  2. Он мгновенно ответит вашим числовым ID пользователя
  3. Скопируйте это число в `TELEGRAM_ALLOWED_USERS`


info
ID пользователей Telegram — это постоянные числа, например `123456789`. Они отличаются от `@username`, который может меняться. Всегда используйте числовой ID для списков разрешений.
* * *
## Шаг 3: Запустите шлюз[​](<#step-3-start-the-gateway> "Прямая ссылка на Шаг 3: Запустите шлюз")
### Быстрая проверка[​](<#quick-test> "Прямая ссылка на Быстрая проверка")
Сначала запустите шлюз в режиме переднего плана, чтобы убедиться, что всё работает:
[code] 
    hermes gateway  
    
[/code]
Вы должны увидеть вывод, похожий на:
[code] 
    [Gateway] Starting Hermes Gateway...  
    [Gateway] Telegram adapter connected  
    [Gateway] Cron scheduler started (tick every 60s)  
    
[/code]
Откройте Telegram, найдите своего бота и отправьте ему сообщение. Если он отвечает — вы в деле. Нажмите `Ctrl+C` для остановки.
### Продакшн: Установка как сервис[​](<#production-install-as-a-service> "Прямая ссылка на Продакшн: Установка как сервис")
Для постоянного развёртывания, которое переживает перезагрузки:
[code] 
    hermes gateway install  
    sudo hermes gateway install --system   # Linux only: boot-time system service  
    
[/code]
Это создаёт фоновый сервис: пользовательский **systemd**-сервис на Linux по умолчанию, **launchd**-сервис на macOS или системный сервис Linux для автозагрузки, если передать `--system`.
[code] 
    # Linux — manage the default user service  
    hermes gateway start  
    hermes gateway stop  
    hermes gateway status  
      
    # View live logs  
    journalctl --user -u hermes-gateway -f  
      
    # Keep running after SSH logout  
    sudo loginctl enable-linger $USER  
      
    # Linux servers — explicit system-service commands  
    sudo hermes gateway start --system  
    sudo hermes gateway status --system  
    journalctl -u hermes-gateway -f  
    
[/code]
[code] 
    # macOS — manage the service  
    hermes gateway start  
    hermes gateway stop  
    tail -f ~/.hermes/logs/gateway.log  
    
[/code]
macOS PATH
Файл launchd plist захватывает ваш shell PATH при установке, чтобы подпроцессы шлюза могли найти такие инструменты, как Node.js и ffmpeg. Если вы установите новые инструменты позже, повторно запустите `hermes gateway install`, чтобы обновить plist.
### Проверьте, что он запущен[​](<#verify-its-running> "Прямая ссылка на Проверьте, что он запущен")
[code] 
    hermes gateway status  
    
[/code]
Затем отправьте тестовое сообщение своему боту в Telegram. Вы должны получить ответ в течение нескольких секунд.
* * *
## Шаг 4: Настройте доступ для команды[​](<#step-4-set-up-team-access> "Прямая ссылка на Шаг 4: Настройте доступ для команды")
Теперь давайте предоставим доступ вашим коллегам. Есть два подхода.
### Подход A: Статический список разрешений[​](<#approach-a-static-allowlist> "Прямая ссылка на Подход A: Статический список разрешений")
Соберите ID пользователей Telegram каждого члена команды (пусть они напишут [@userinfobot](<https://t.me/userinfobot>)) и добавьте их в виде списка через запятую:
[code] 
    # In ~/.hermes/.env  
    TELEGRAM_ALLOWED_USERS=123456789,987654321,555555555  
    
[/code]
Перезапустите шлюз после изменений:
[code] 
    hermes gateway stop && hermes gateway start  
    
[/code]
### Подход B: Привязка через личные сообщения (рекомендуется для команд)[​](<#approach-b-dm-pairing-recommended-for-teams> "Прямая ссылка на Подход B: Привязка через личные сообщения (рекомендуется для команд)")
Привязка через личные сообщения гибче — вам не нужно собирать ID пользователей заранее. Вот как это работает:
  1. **Коллега пишет боту в личку** — так как его нет в списке разрешений, бот отвечает одноразовым кодом привязки:
[code] 🔐 Pairing code: XKGH5N7P  
         Send this code to the bot owner for approval.  
         
[/code]
  2. **Коллега отправляет вам код** (любым каналом — Slack, email, лично)
  3. **Вы подтверждаете его** на сервере:
[code] hermes pairing approve telegram XKGH5N7P  
         
[/code]
  4. **Он в деле** — бот немедленно начинает отвечать на его сообщения


**Управление привязанными пользователями:**
[code] 
    # See all pending and approved users  
    hermes pairing list  
      
    # Revoke someone's access  
    hermes pairing revoke telegram 987654321  
      
    # Clear expired pending codes  
    hermes pairing clear-pending  
    
[/code]
tip
Привязка через личные сообщения идеальна для команд, потому что вам не нужно перезапускать шлюз при добавлении новых пользователей. Подтверждения вступают в силу немедленно.
### Вопросы безопасности[​](<#security-considerations> "Прямая ссылка на Вопросы безопасности")
  * **Никогда не устанавливайте`GATEWAY_ALLOW_ALL_USERS=true`** для бота с доступом к терминалу — любой, кто найдёт вашего бота, сможет выполнять команды на вашем сервере
  * Коды привязки истекают через **1 час** и используют криптографическую случайность
  * Ограничение скорости предотвращает атаки перебором: 1 запрос на пользователя за 10 минут, макс. 3 ожидающих кода на платформу
  * После 5 неудачных попыток подтверждения платформа блокируется на 1 час
  * Все данные привязки хранятся с правами доступа `chmod 0600`


* * *
## Шаг 5: Настройте бота[​](<#step-5-configure-the-bot> "Прямая ссылка на Шаг 5: Настройте бота")
### Установите домашний канал[​](<#set-a-home-channel> "Прямая ссылка на Установите домашний канал")
**Домашний канал** — это канал, куда бот доставляет результаты cron-задач и проактивные сообщения. Без него у запланированных задач нет места для вывода.
**Вариант 1:** Используйте команду `/sethome` в любой Telegram-группе или чате, где состоит бот.
**Вариант 2:** Установите вручную в `~/.hermes/.env`:
[code] 
    TELEGRAM_HOME_CHANNEL=-1001234567890  
    TELEGRAM_HOME_CHANNEL_NAME="Team Updates"  
    
[/code]
Чтобы узнать ID канала, добавьте [@userinfobot](<https://t.me/userinfobot>) в группу — он сообщит ID чата группы.
### Настройте отображение прогресса инструментов[​](<#configure-tool-progress-display> "Прямая ссылка на Настройте отображение прогресса инструментов")
Управляйте тем, сколько деталей показывает бот при использовании инструментов. В `~/.hermes/config.yaml`:
[code] 
    display:  
      tool_progress: new    # off | new | all | verbose  
    
[/code]
Режим| Что вы видите  
---|---  
`off`| Только чистые ответы — без активности инструментов  
`new`| Краткий статус для каждого нового вызова инструмента (рекомендуется для мессенджеров)  
`all`| Каждый вызов инструмента с деталями  
`verbose`| Полный вывод инструментов, включая результаты команд  
Пользователи также могут изменить это в рамках сессии командой `/verbose` в чате.
### Настройте личность с помощью SOUL.md[​](<#set-up-a-personality-with-soulmd> "Прямая ссылка на Настройте личность с помощью SOUL.md")
Настройте стиль общения бота, отредактировав `~/.hermes/SOUL.md`:
Полное руководство см. в [Использование SOUL.md с Hermes](</docs/guides/use-soul-with-hermes>).
[code] 
    # Soul  
    You are a helpful team assistant. Be concise and technical.  
    Use code blocks for any code. Skip pleasantries — the team  
    values directness. When debugging, always ask for error logs  
    before guessing at solutions.  
    
[/code]
### Добавьте контекст проекта[​](<#add-project-context> "Прямая ссылка на Добавьте контекст проекта")
Если ваша команда работает над конкретными проектами, создайте файлы контекста, чтобы бот знал ваш стек:
[code] 
    <!-- ~/.hermes/AGENTS.md -->  
    # Team Context  
    - We use Python 3.12 with FastAPI and SQLAlchemy  
    - Frontend is React with TypeScript  
    - CI/CD runs on GitHub Actions  
    - Production deploys to AWS ECS  
    - Always suggest writing tests for new code  
    
[/code]
info
Файлы контекста внедряются в системный промпт каждой сессии. Держите их краткими — каждый символ учитывается в вашем токенном бюджете.
* * *
## Шаг 6: Настройте запланированные задачи[​](<#step-6-set-up-scheduled-tasks> "Прямая ссылка на Шаг 6: Настройте запланированные задачи")
С запущенным шлюзом вы можете планировать повторяющиеся задачи, результаты которых будут доставляться в ваш командный канал.
### Ежедневная сводка стендапа[​](<#daily-standup-summary> "Прямая ссылка на Ежедневная сводка стендапа")
Напишите боту в Telegram:
[code] 
    Every weekday at 9am, check the GitHub repository at  
    github.com/myorg/myproject for:  
    1. Pull requests opened/merged in the last 24 hours  
    2. Issues created or closed  
    3. Any CI/CD failures on the main branch  
    Format as a brief standup-style summary.  
    
[/code]
Агент автоматически создаёт cron-задачу и доставляет результаты в чат, где вы запросили (или в домашний канал).
### Проверка здоровья сервера[​](<#server-health-check> "Прямая ссылка на Проверка здоровья сервера")
[code] 
    Every 6 hours, check disk usage with 'df -h', memory with 'free -h',  
    and Docker container status with 'docker ps'. Report anything unusual —  
    partitions above 80%, containers that have restarted, or high memory usage.  
    
[/code]
### Управление запланированными задачами[​](<#managing-scheduled-tasks> "Прямая ссылка на Управление запланированными задачами")
[code] 
    # From the CLI  
    hermes cron list          # View all scheduled jobs  
    hermes cron status        # Check if scheduler is running  
      
    # From Telegram chat  
    /cron list                # View jobs  
    /cron remove <job_id>     # Remove a job  
    
[/code]
warning
Промпты cron-задач выполняются в полностью новых сессиях без памяти о предыдущих разговорах. Убедитесь, что каждый промпт содержит **весь** контекст, необходимый агенту — пути к файлам, URL, адреса серверов и чёткие инструкции.
* * *
## Советы для продакшна[​](<#production-tips> "Прямая ссылка на Советы для продакшна")
### Используйте Docker для безопасности[​](<#use-docker-for-safety> "Прямая ссылка на Используйте Docker для безопасности")
Для общего командного бота используйте Docker в качестве бэкенда терминала, чтобы команды агента выполнялись в контейнере, а не на вашем хосте:
[code] 
    # In ~/.hermes/.env  
    TERMINAL_BACKEND=docker  
    TERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20  
    
[/code]
Или в `~/.hermes/config.yaml`:
[code] 
    terminal:  
      backend: docker  
      container_cpu: 1  
      container_memory: 5120  
      container_persistent: true  
    
[/code]
Таким образом, даже если кто-то попросит бота выполнить что-то разрушительное, ваша хост-система будет защищена.
### Мониторинг шлюза[​](<#monitor-the-gateway> "Прямая ссылка на Мониторинг шлюза")
[code] 
    # Check if the gateway is running  
    hermes gateway status  
      
    # Watch live logs (Linux)  
    journalctl --user -u hermes-gateway -f  
      
    # Watch live logs (macOS)  
    tail -f ~/.hermes/logs/gateway.log  
    
[/code]
### Держите Hermes обновлённым[​](<#keep-hermes-updated> "Прямая ссылка на Держите Hermes обновлённым")
Из Telegram отправьте боту `/update` — он скачает последнюю версию и перезапустится. Или с сервера:
[code] 
    hermes update  
    hermes gateway stop && hermes gateway start  
    
[/code]
### Расположение логов[​](<#log-locations> "Прямая ссылка на Расположение логов")
Что| Расположение  
---|---  
Логи шлюза| `journalctl --user -u hermes-gateway` (Linux) или `~/.hermes/logs/gateway.log` (macOS)  
Вывод cron-задач| `~/.hermes/cron/output/{job_id}/{timestamp}.md`  
Определения cron-задач| `~/.hermes/cron/jobs.json`  
Данные привязки| `~/.hermes/pairing/`  
История сессий| `~/.hermes/sessions/`  
* * *
## Дальнейшие шаги[​](<#going-further> "Прямая ссылка на Дальнейшие шаги")
У вас есть работающий командный Telegram-ассистент. Вот несколько следующих шагов:
  * **[Руководство по безопасности](</docs/user-guide/security>)** — глубокое погружение в авторизацию, изоляцию контейнеров и одобрение команд
  * **[Шлюз сообщений](</docs/user-guide/messaging>)** — полный справочник по архитектуре шлюза, управлению сессиями и командам чата
  * **[Настройка Telegram](</docs/user-guide/messaging/telegram>)** — платформо-специфичные детали, включая голосовые сообщения и TTS
  * **[Запланированные задачи](</docs/user-guide/features/cron>)** — продвинутое cron-планирование с вариантами доставки и cron-выражениями
  * **[Файлы контекста](</docs/user-guide/features/context-files>)** — AGENTS.md, SOUL.md и .cursorrules для проектных знаний
  * **[Личность](</docs/user-guide/features/personality>)** — встроенные пресеты личности и пользовательские определения персонажей
  * **Добавьте больше платформ** — тот же шлюз может одновременно запускать [Discord](</docs/user-guide/messaging/discord>), [Slack](</docs/user-guide/messaging/slack>) и [WhatsApp](</docs/user-guide/messaging/whatsapp>)


* * *
_Вопросы или проблемы? Откройте issue на GitHub — вклад приветствуется._
  * [Что мы создаём](<#what-were-building>)
  * [Предварительные требования](<#prerequisites>)
  * [Шаг 1: Создайте Telegram-бота](<#step-1-create-a-telegram-bot>)
  * [Шаг 2: Настройте шлюз](<#step-2-configure-the-gateway>)
    * [Вариант A: Интерактивная настройка (рекомендуется)](<#option-a-interactive-setup-recommended>)
    * [Вариант B: Ручная настройка](<#option-b-manual-configuration>)
    * [Как узнать свой ID пользователя](<#finding-your-user-id>)
  * [Шаг 3: Запустите шлюз](<#step-3-start-the-gateway>)
    * [Быстрая проверка](<#quick-test>)
    * [Продакшн: Установка как сервис](<#production-install-as-a-service>)
    * [Проверьте, что он запущен](<#verify-its-running>)
  * [Шаг 4: Настройте доступ для команды](<#step-4-set-up-team-access>)
    * [Подход A: Статический список разрешений](<#approach-a-static-allowlist>)
    * [Подход B: Привязка через личные сообщения (рекомендуется для команд)](<#approach-b-dm-pairing-recommended-for-teams>)
    * [Вопросы безопасности](<#security-considerations>)
  * [Шаг 5: Настройте бота](<#step-5-configure-the-bot>)
    * [Установите домашний канал](<#set-a-home-channel>)
    * [Настройте отображение прогресса инструментов](<#configure-tool-progress-display>)
    * [Настройте личность с помощью SOUL.md](<#set-up-a-personality-with-soulmd>)
    * [Добавьте контекст проекта](<#add-project-context>)
  * [Шаг 6: Настройте запланированные задачи](<#step-6-set-up-scheduled-tasks>)
    * [Ежедневная сводка стендапа](<#daily-standup-summary>)
    * [Проверка здоровья сервера](<#server-health-check>)
    * [Управление запланированными задачами](<#managing-scheduled-tasks>)
  * [Советы для продакшна](<#production-tips>)
    * [Используйте Docker для безопасности](<#use-docker-for-safety>)
    * [Мониторинг шлюза](<#monitor-the-gateway>)
    * [Держите Hermes обновлённым](<#keep-hermes-updated>)
    * [Расположение логов](<#log-locations>)
  * [Дальнейшие шаги](<#going-further>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant -->
