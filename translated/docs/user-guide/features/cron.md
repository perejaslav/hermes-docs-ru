На этой странице
Планируйте задачи для автоматического выполнения с помощью описаний на естественном языке или cron-выражений. Hermes предоставляет управление cron через единый инструмент `cronjob` с операциями в стиле действий вместо отдельных инструментов для создания, просмотра и удаления.
## Что умеет cron[​](<#what-cron-can-do-now> "Direct link to What cron can do now")
Cron-задачи могут:
  * запускать одноразовые или повторяющиеся задачи
  * приостанавливать, возобновлять, редактировать, запускать и удалять задачи
  * прикреплять ноль, одну или несколько навыков (skills) к задаче
  * доставлять результаты обратно в исходный чат, в локальные файлы или на настроенные целевые платформы
  * запускаться в новых сессиях агента с обычным статическим списком инструментов
  * запускаться в **режиме без агента** — скрипт по расписанию, его stdout доставляется дословно, без участия LLM (см. раздел [режим без агента](<#no-agent-mode-script-only-jobs>) ниже)


Все это доступно самому Hermes через инструмент `cronjob`, так что вы можете создавать, приостанавливать, редактировать и удалять задачи, просто попросив об этом обычным языком — CLI не требуется.
warning
Сессии cron-задач не могут рекурсивно создавать новые cron-задачи. Hermes отключает инструменты управления cron внутри выполнения cron-задач, чтобы предотвратить бесконечные циклы планирования.
## Создание запланированных задач[​](<#creating-scheduled-tasks> "Direct link to Creating scheduled tasks")
### В чате через `/cron`[​](<#in-chat-with-cron> "Direct link to in-chat-with-cron")
[code] 
    /cron add 30m "Remind me to check the build"  
    /cron add "every 2h" "Check server status"  
    /cron add "every 1h" "Summarize new feed items" --skill blogwatcher  
    /cron add "every 1h" "Use both skills and combine the result" --skill blogwatcher --skill maps  
    
[/code]
### Из автономного CLI[​](<#from-the-standalone-cli> "Direct link to From the standalone CLI")
[code] 
    hermes cron create "every 2h" "Check server status"  
    hermes cron create "every 1h" "Summarize new feed items" --skill blogwatcher  
    hermes cron create "every 1h" "Use both skills and combine the result" \  
      --skill blogwatcher \  
      --skill maps \  
      --name "Skill combo"  
    
[/code]
### Через естественный разговор[​](<#through-natural-conversation> "Direct link to Through natural conversation")
Просто попросите Hermes обычным языком:
[code] 
    Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram.  
    
[/code]
Hermes использует единый инструмент `cronjob` внутри.
## Cron-задачи с навыками[​](<#skill-backed-cron-jobs> "Direct link to Skill-backed cron jobs")
Cron-задача может загружать один или несколько навыков перед выполнением запроса.
### Один навык[​](<#single-skill> "Direct link to Single skill")
[code] 
    cronjob(  
        action="create",  
        skill="blogwatcher",  
        prompt="Check the configured feeds and summarize anything new.",  
        schedule="0 9 * * *",  
        name="Morning feeds",  
    )  
    
[/code]
### Несколько навыков[​](<#multiple-skills> "Direct link to Multiple skills")
Навыки загружаются по порядку. Запрос (prompt) становится инструкцией задачи, наложенной поверх этих навыков.
[code] 
    cronjob(  
        action="create",  
        skills=["blogwatcher", "maps"],  
        prompt="Look for new local events and interesting nearby places, then combine them into one short brief.",  
        schedule="every 6h",  
        name="Local brief",  
    )  
    
[/code]
Это полезно, когда вы хотите, чтобы запланированный агент наследовал переиспользуемые рабочие процессы без необходимости вставлять полный текст навыка в сам cron-запрос.
## Запуск задачи внутри директории проекта[​](<#running-a-job-inside-a-project-directory> "Direct link to Running a job inside a project directory")
Cron-задачи по умолчанию выполняются отсоединёнными от какого-либо репозитория — `AGENTS.md`, `CLAUDE.md` или `.cursorrules` не загружаются, а инструменты терминала/файлов/кода запускаются из той рабочей директории, в которой был запущен шлюз (gateway). Передайте `--workdir` (CLI) или `workdir=` (вызов инструмента), чтобы изменить это:
[code] 
    # Standalone CLI (schedule and prompt are positional)  
    hermes cron create "every 1d at 09:00" \  
      "Audit open PRs, summarize CI health, and post to #eng" \  
      --workdir /home/me/projects/acme  
    
[/code]
[code] 
    # From a chat, via the cronjob tool  
    cronjob(  
        action="create",  
        schedule="every 1d at 09:00",  
        workdir="/home/me/projects/acme",  
        prompt="Audit open PRs, summarize CI health, and post to #eng",  
    )  
    
[/code]
Когда `workdir` установлен:
  * `AGENTS.md`, `CLAUDE.md` и `.cursorrules` из этой директории внедряются в системный промпт (тот же порядок обнаружения, что и в интерактивном CLI)
  * `terminal`, `read_file`, `write_file`, `patch`, `search_files` и `execute_code` используют эту директорию как свою рабочую (через `TERMINAL_CWD`)
  * Путь должен быть абсолютной существующей директорией — относительные пути и отсутствующие директории отклоняются при создании/обновлении
  * Передайте `--workdir ""` (или `workdir=""` через инструмент) при редактировании, чтобы очистить его и вернуть старое поведение


Сериализация
Задачи с `workdir` выполняются последовательно на каждом тике планировщика, а не в параллельном пуле. Это сделано намеренно — `TERMINAL_CWD` является глобальным для процесса, поэтому две задачи с workdir, запущенные одновременно, могли бы повредить cwd друг друга. Задачи без workdir по-прежнему выполняются параллельно, как и раньше.
## Редактирование задач[​](<#editing-jobs> "Direct link to Editing jobs")
Вам не нужно удалять и создавать задачи заново, чтобы изменить их.
### Чат[​](<#chat> "Direct link to Chat")
[code] 
    /cron edit <job_id> --schedule "every 4h"  
    /cron edit <job_id> --prompt "Use the revised task"  
    /cron edit <job_id> --skill blogwatcher --skill maps  
    /cron edit <job_id> --remove-skill blogwatcher  
    /cron edit <job_id> --clear-skills  
    
[/code]
### Автономный CLI[​](<#standalone-cli> "Direct link to Standalone CLI")
[code] 
    hermes cron edit <job_id> --schedule "every 4h"  
    hermes cron edit <job_id> --prompt "Use the revised task"  
    hermes cron edit <job_id> --skill blogwatcher --skill maps  
    hermes cron edit <job_id> --add-skill maps  
    hermes cron edit <job_id> --remove-skill blogwatcher  
    hermes cron edit <job_id> --clear-skills  
    
[/code]
Примечания:
  * повторяющийся `--skill` заменяет прикреплённый список навыков задачи
  * `--add-skill` добавляет к существующему списку, не заменяя его
  * `--remove-skill` удаляет конкретные прикреплённые навыки
  * `--clear-skills` удаляет все прикреплённые навыки


## Действия жизненного цикла[​](<#lifecycle-actions> "Direct link to Lifecycle actions")
Теперь cron-задачи имеют более полный жизненный цикл, чем просто создание/удаление.
### Чат[​](<#chat-1> "Direct link to Chat")
[code] 
    /cron list  
    /cron pause <job_id>  
    /cron resume <job_id>  
    /cron run <job_id>  
    /cron remove <job_id>  
    
[/code]
### Автономный CLI[​](<#standalone-cli-1> "Direct link to Standalone CLI")
[code] 
    hermes cron list  
    hermes cron pause <job_id>  
    hermes cron resume <job_id>  
    hermes cron run <job_id>  
    hermes cron remove <job_id>  
    hermes cron status  
    hermes cron tick  
    
[/code]
Что они делают:
  * `pause` — сохранить задачу, но остановить её планирование
  * `resume` — повторно включить задачу и вычислить следующий запуск
  * `run` — запустить задачу на следующем тике планировщика
  * `remove` — удалить задачу полностью


## Как это работает[​](<#how-it-works> "Direct link to How it works")
**Выполнение cron обрабатывается демоном шлюза (gateway daemon).** Шлюз тикает каждые 60 секунд, запуская все подлежащие выполнению задачи в изолированных сессиях агента.
[code] 
    hermes gateway install     # Установить как пользовательский сервис  
    sudo hermes gateway install --system   # Linux: системный сервис загрузки для серверов  
    hermes gateway             # Или запустить в foreground  
      
    hermes cron list  
    hermes cron status  
    
[/code]
### Поведение планировщика шлюза[​](<#gateway-scheduler-behavior> "Direct link to Gateway scheduler behavior")
На каждом тике Hermes:
  1. загружает задачи из `~/.hermes/cron/jobs.json`
  2. проверяет `next_run_at` относительно текущего времени
  3. запускает новую сессию `AIAgent` для каждой подлежащей выполнению задачи
  4. опционально внедряет один или несколько прикреплённых навыков в эту новую сессию
  5. выполняет запрос (prompt) до завершения
  6. доставляет финальный ответ
  7. обновляет метаданные выполнения и следующее запланированное время


Файловая блокировка `~/.hermes/cron/.tick.lock` предотвращает перекрытие тиков планировщика, чтобы одна и та же партия задач не была запущена дважды.
## Параметры доставки[​](<#delivery-options> "Direct link to Delivery options")
При планировании задач вы указываете, куда направлять вывод:
Параметр| Описание| Пример  
|---|---|---  
`"origin"`| Туда, где была создана задача| По умолчанию на платформах обмена сообщениями  
`"local"`| Сохранять только в локальные файлы (`~/.hermes/cron/output/`)| По умолчанию в CLI  
`"telegram"`| Домашний канал Telegram| Использует `TELEGRAM_HOME_CHANNEL`  
`"telegram:123456"`| Конкретный чат Telegram по ID| Прямая доставка  
`"telegram:-100123:17585"`| Конкретная тема Telegram| Формат `chat_id:thread_id`  
`"discord"`| Домашний канал Discord| Использует `DISCORD_HOME_CHANNEL`  
`"discord:#engineering"`| Конкретный канал Discord| По имени канала  
`"slack"`| Домашний канал Slack|  
`"whatsapp"`| Домашний чат WhatsApp|  
`"signal"`| Signal|  
`"matrix"`| Домашняя комната Matrix|  
`"mattermost"`| Домашний канал Mattermost|  
`"email"`| Email|  
`"sms"`| SMS через Twilio|  
`"homeassistant"`| Home Assistant|  
`"dingtalk"`| DingTalk|  
`"feishu"`| Feishu/Lark|  
`"wecom"`| WeCom|  
`"weixin"`| Weixin (WeChat)|  
`"bluebubbles"`| BlueBubbles (iMessage)|  
`"qqbot"`| QQ Bot (Tencent QQ)|  
Финальный ответ агента доставляется автоматически. Вам не нужно вызывать `send_message` в cron-запросе.
### Обёртка ответа[​](<#response-wrapping> "Direct link to Response wrapping")
По умолчанию доставляемый вывод cron оборачивается в заголовок и подвал, чтобы получатель знал, что это запланированная задача:
[code] 
    Cronjob Response: Morning feeds  
    -------------  
      
    <agent output here>  
      
    Note: The agent cannot see this message, and therefore cannot respond to it.  
    
[/code]
Чтобы доставлять сырой вывод агента без обёртки, установите `cron.wrap_response` в `false`:
[code] 
    # ~/.hermes/config.yaml  
    cron:  
      wrap_response: false  
    
[/code]
### Тихая отмена доставки[​](<#silent-suppression> "Direct link to Silent suppression")
Если финальный ответ агента начинается с `[SILENT]`, доставка полностью отменяется. Вывод всё равно сохраняется локально для аудита (в `~/.hermes/cron/output/`), но сообщение не отправляется целевому получателю.
Это полезно для мониторинговых задач, которые должны сообщать только когда что-то не так:
[code] 
    Check if nginx is running. If everything is healthy, respond with only [SILENT].  
    Otherwise, report the issue.  
    
[/code]
Неудачные задачи всегда доставляются независимо от маркера `[SILENT]` — только успешные запуски могут быть отменены.
## Тайм-аут скрипта[​](<#script-timeout> "Direct link to Script timeout")
Предварительные скрипты (прикреплённые через параметр `script`) имеют тайм-аут по умолчанию 120 секунд. Если вашим скриптам нужно больше времени — например, для включения рандомизированных задержек, чтобы избежать ботоподобных паттернов, — вы можете увеличить это значение:
[code] 
    # ~/.hermes/config.yaml  
    cron:  
      script_timeout_seconds: 300   # 5 минут  
    
[/code]
Или установите переменную окружения `HERMES_CRON_SCRIPT_TIMEOUT`. Порядок разрешения: переменная окружения → config.yaml → значение по умолчанию 120с.
## Режим без агента (только скрипты)[​](<#no-agent-mode-script-only-jobs> "Direct link to No-agent mode (script-only jobs)")
Для повторяющихся задач, которым не нужно рассуждение LLM — классические сторожевые скрипты, оповещения о диске/памяти, heartbeat-сигналы, CI-пинги — передайте `no_agent=True` при создании. Планировщик запускает ваш скрипт по расписанию и доставляет его stdout напрямую, полностью пропуская агента:
[code] 
    hermes cron create "every 5m" \  
      --no-agent \  
      --script memory-watchdog.sh \  
      --deliver telegram \  
      --name "memory-watchdog"  
    
[/code]
Семантика:
  * Stdout скрипта (обрезанный) → доставляется дословно как сообщение.
  * **Пустой stdout → тихий тик** , без доставки. Это паттерн сторожевого скрипта: «говори только тогда, когда что-то не так».
  * Ненулевой код возврата или тайм-аут → доставляется оповещение об ошибке, чтобы сломанный сторожевой скрипт не мог молча отказать.
  * `{"wakeAgent": false}` в последней строке → тихий тик (те же ворота, что используют LLM-задачи).
  * Никаких токенов, никакой модели, никакого резервного провайдера — задача никогда не касается уровня инференса.


Файлы `.sh`/`.bash` выполняются через `/bin/bash`; всё остальное — через текущий интерпретатор Python (`sys.executable`). Скрипты должны находиться в `~/.hermes/scripts/` (то же правило изоляции, что и для предварительных скриптов).
### Агент настраивает это за вас[​](<#the-agent-sets-these-up-for-you> "Direct link to The agent sets these up for you")
Схема инструмента `cronjob` предоставляет `no_agent` напрямую Hermes, так что вы можете описать сторожевой скрипт в чате, и агент сам всё настроит:
[code] 
    Ping me on Telegram if RAM is over 85%, every 5 minutes.  
    
[/code]
Hermes запишет проверочный скрипт в `~/.hermes/scripts/` через `write_file`, а затем вызовет:
[code] 
    cronjob(action="create", schedule="every 5m",  
            script="memory-watchdog.sh", no_agent=True,  
            deliver="telegram", name="memory-watchdog")  
    
[/code]
Он автоматически выбирает `no_agent=True`, когда содержимое сообщения полностью определяется скриптом (сторожевые скрипты, пороговые оповещения, heartbeat-сигналы). Тот же инструмент также позволяет агенту приостанавливать, возобновлять, редактировать и удалять задачи — так что весь жизненный цикл управляется через чат, без необходимости касаться CLI.
Смотрите руководство [Скриптовые Cron-задачи](</docs/guides/cron-script-only>) с примерами.
## Цепочки задач с `context_from`[​](<#chaining-jobs-with-context_from> "Direct link to chaining-jobs-with-context_from")
Cron-задачи выполняются в изолированных сессиях без памяти о предыдущих запусках. Но иногда вывод одной задачи — это именно то, что нужно следующей. Параметр `context_from` автоматически организует эту связь — запрос задачи B получает самый последний вывод задачи A, добавленный в качестве контекста во время выполнения.
[code] 
    # Job 1: Collect raw data  
    cronjob(  
        action="create",  
        prompt="Fetch the top 10 AI/ML stories from Hacker News. Save them to ~/.hermes/data/briefs/raw.md in markdown format with title, URL, and score.",  
        schedule="0 7 * * *",  
        name="AI News Collector",  
    )  
      
    # Job 2: Triage — receives Job 1's output as context  
    # Get Job 1's ID from: cronjob(action="list")  
    cronjob(  
        action="create",  
        prompt="Read ~/.hermes/data/briefs/raw.md. Score each story 1–10 for engagement potential and novelty. Output the top 5 to ~/.hermes/data/briefs/ranked.md.",  
        schedule="30 7 * * *",  
        context_from="<job1_id>",  
        name="AI News Triage",  
    )  
      
    # Job 3: Ship — receives Job 2's output as context  
    cronjob(  
        action="create",  
        prompt="Read ~/.hermes/data/briefs/ranked.md. Write 3 tweet drafts (hook + body + hashtags). Deliver to telegram:7976161601.",  
        schedule="0 8 * * *",  
        context_from="<job2_id>",  
        name="AI News Brief",  
    )  
    
[/code]
**Как это работает:**
  * Когда запускается задача 2, Hermes читает последний вывод задачи 1 из `~/.hermes/cron/output/{job1_id}/*.md`
  * Этот вывод автоматически добавляется в начало запроса задачи 2
  * Задаче 2 не нужно жёстко прописывать «прочитай этот файл» — она получает содержимое как контекст
  * Цепочка может быть любой длины: задача 1 → задача 2 → задача 3 → ...


**Что принимает `context_from`:**
Формат| Пример  
---|---  
Один ID задачи (строка)| `context_from="a1b2c3d4"`  
Несколько ID задач (список)| `context_from=["job_a", "job_b"]`  
Выводы объединяются в порядке перечисления.
**Когда это использовать:**
  * Многоэтапные конвейеры (сбор → фильтрация → форматирование → доставка)
  * Зависимые задачи, где результат шага N зависит от вывода шага N−1
  * Паттерны fan-out/fan-in, где одна задача агрегирует результаты нескольких других


## Восстановление провайдера[​](<#provider-recovery> "Direct link to Provider recovery")
Cron-задачи наследуют ваши настроенные резервные провайдеры и ротацию пула учётных данных. Если первичный API-ключ ограничен по скорости или провайдер возвращает ошибку, cron-агент может:
  * **Переключиться на альтернативного провайдера**, если у вас настроены `fallback_providers` (или устаревший `fallback_model`) в `config.yaml`
  * **Переключиться на следующее учётное данные** из вашего [пула учётных данных](</docs/user-guide/configuration#credential-pool-strategies>) для того же провайдера


Это означает, что cron-задачи, выполняющиеся с высокой частотой или в часы пик, становятся более устойчивыми — один ключ с ограничением скорости не приведёт к сбою всего выполнения.
## Форматы расписания[​](<#schedule-formats> "Direct link to Schedule formats")
Финальный ответ агента доставляется автоматически — вам **не** нужно включать `send_message` в cron-запрос для того же получателя. Если cron-запуск вызывает `send_message` в тот же целевой канал, в который планировщик уже доставит ответ, Hermes пропускает эту дублирующую отправку и сообщает модели, что пользовательский контент следует поместить в финальный ответ. Используйте `send_message` только для дополнительных или других получателей.
### Относительные задержки (однократно)[​](<#relative-delays-one-shot> "Direct link to Relative delays (one-shot)")
[code] 
    30m     → Выполнить один раз через 30 минут  
    2h      → Выполнить один раз через 2 часа  
    1d      → Выполнить один раз через 1 день  
    
[/code]
### Интервалы (повторяющиеся)[​](<#intervals-recurring> "Direct link to Intervals (recurring)")
[code] 
    every 30m    → Каждые 30 минут  
    every 2h     → Каждые 2 часа  
    every 1d     → Каждый день  
    
[/code]
### Cron-выражения[​](<#cron-expressions> "Direct link to Cron expressions")
[code] 
    0 9 * * *       → Ежедневно в 9:00  
    0 9 * * 1-5     → По будням в 9:00  
    0 */6 * * *     → Каждые 6 часов  
    30 8 1 * *      → Первого числа каждого месяца в 8:30  
    0 0 * * 0       → Каждое воскресенье в полночь  
    
[/code]
### ISO-метки времени[​](<#iso-timestamps> "Direct link to ISO timestamps")
[code] 
    2026-03-15T09:00:00    → Однократно 15 марта 2026 г. в 9:00  
    
[/code]
## Поведение повторов[​](<#repeat-behavior> "Direct link to Repeat behavior")
Тип расписания| Повтор по умолчанию| Поведение  
---|---|---  
Однократное (`30m`, метка времени)| 1| Выполняется один раз  
Интервал (`every 2h`)| бесконечно| Выполняется до удаления  
Cron-выражение| бесконечно| Выполняется до удаления  
Вы можете переопределить это:
[code] 
    cronjob(  
        action="create",  
        prompt="...",  
        schedule="every 2h",  
        repeat=5,  
    )  
    
[/code]
## Программное управление задачами[​](<#managing-jobs-programmatically> "Direct link to Managing jobs programmatically")
API для агента — это один инструмент:
[code] 
    cronjob(action="create", ...)  
    cronjob(action="list")  
    cronjob(action="update", job_id="...")  
    cronjob(action="pause", job_id="...")  
    cronjob(action="resume", job_id="...")  
    cronjob(action="run", job_id="...")  
    cronjob(action="remove", job_id="...")  
    
[/code]
Для `update` передайте `skills=[]`, чтобы удалить все прикреплённые навыки.
## Наборы инструментов, доступные cron-задачам[​](<#toolsets-available-to-cron-jobs> "Direct link to Toolsets available to cron jobs")
Cron запускает каждую задачу в новой сессии агента без привязанной чат-платформы. По умолчанию cron-агент получает **набор инструментов, который вы настроили для платформы`cron` в `hermes tools`** — не стандартный набор CLI, не «всё подряд».
[code] 
    hermes tools  
    # → выберите платформу "cron" в curses-интерфейсе  
    # → включайте/отключайте наборы инструментов так же, как для Telegram/Discord и т.д.  
    
[/code]
Более точный контроль для каждой задачи доступен через поле `enabled_toolsets` в `cronjob.create` (или для существующей задачи через `cronjob.update`):
[code] 
    cronjob(action="create", name="weekly-news-summary",  
            schedule="every sunday 9am",  
            enabled_toolsets=["web", "file"],      # только web + file, без terminal/browser и т.д.  
            prompt="Summarize this week's AI news: ...")  
    
[/code]
Когда `enabled_toolsets` установлен для задачи, он имеет приоритет; иначе применяется конфигурация cron-платформы из `hermes tools`; иначе Hermes возвращается к встроенным значениям по умолчанию. Это важно для контроля расходов: включение `moa`, `browser`, `delegation` в каждую маленькую задачу «загрузить новости» раздувает промпт со схемой инструментов при каждом LLM-запросе.
### Полный пропуск агента: `wakeAgent`[​](<#skipping-the-agent-entirely-wakeagent> "Direct link to skipping-the-agent-entirely-wakeagent")
Если ваша cron-задача прикрепляет предварительный проверочный скрипт (через `script=`), скрипт может решить во время выполнения, должен ли Hermes вообще вызывать агента. Выведите последнюю строку stdout в формате:
[code] 
    {"wakeAgent": false}  
    
[/code]
…и cron пропускает выполнение агента для этого тика. Полезно для частых опросов (каждые 1–5 минут), которые должны пробуждать LLM только когда состояние действительно изменилось — иначе вы платите за пустые вызовы агента снова и снова.
[code] 
    # pre-check script  
    import json, sys  
    latest = fetch_latest_issue_count()  
    prev = read_state("issue_count")  
    if latest == prev:  
        print(json.dumps({"wakeAgent": False}))   # пропустить этот тик  
        sys.exit(0)  
    write_state("issue_count", latest)  
    print(json.dumps({"wakeAgent": True, "context": {"new_issues": latest - prev}}))  
    
[/code]
Когда `wakeAgent` опущен, значение по умолчанию — `true` (пробудить агента как обычно).
### Цепочки задач: `context_from`[​](<#chaining-jobs-context_from> "Direct link to chaining-jobs-context_from")
Cron-задача может потреблять последний успешный вывод одной или нескольких других задач, перечислив их имена (или ID) в `context_from`:
[code] 
    cronjob(action="create", name="daily-digest",  
            schedule="every day 7am",  
            context_from=["ai-news-fetch", "github-prs-fetch"],  
            prompt="Write the daily digest using the outputs above.")  
    
[/code]
Выводы последних завершённых запусков указанных задач внедряются перед запросом как контекст для этого выполнения. Каждая上游 запись должна быть валидным ID или именем задачи (см. `cronjob action="list"`). Примечание: цепочка читает _последний завершённый_ вывод — она не ждёт выполняющиеся в том же тике вышестоящие задачи.
## Хранение задач[​](<#job-storage> "Direct link to Job storage")
Задачи хранятся в `~/.hermes/cron/jobs.json`. Вывод запусков задач сохраняется в `~/.hermes/cron/output/{job_id}/{timestamp}.md`.
Задачи могут хранить `model` и `provider` как `null`. Когда эти поля опущены, Hermes разрешает их во время выполнения из глобальной конфигурации. Они появляются в записи задачи только когда установлено переопределение для конкретной задачи.
Хранилище использует атомарную запись файлов, поэтому прерванные записи не оставляют частично записанный файл задачи.
## Самодостаточные запросы по-прежнему важны[​](<#self-contained-prompts-still-matter> "Direct link to Self-contained prompts still matter")
Важно
Cron-задачи выполняются в полностью новой сессии агента. Запрос (prompt) должен содержать всё, что нужно агенту, что уже не предоставлено прикреплёнными навыками.
**ПЛОХО:** `"Check on that server issue"`
**ХОРОШО:** `"SSH into server 192.168.1.100 as user 'deploy', check if nginx is running with 'systemctl status nginx', and verify https://example.com returns HTTP 200."`
## Безопасность[​](<#security> "Direct link to Security")
Запросы запланированных задач проверяются на наличие паттернов инъекций в промпт и эксфильтрации учётных данных при создании и обновлении. Запросы, содержащие невидимые Unicode-трюки, попытки SSH-бэкдоров или очевидные payload-ы для кражи секретов, блокируются.
  * [Что умеет cron](<#what-cron-can-do-now>)
  * [Создание запланированных задач](<#creating-scheduled-tasks>)
    * [В чате через `/cron`](<#in-chat-with-cron>)
    * [Из автономного CLI](<#from-the-standalone-cli>)
    * [Через естественный разговор](<#through-natural-conversation>)
  * [Cron-задачи с навыками](<#skill-backed-cron-jobs>)
    * [Один навык](<#single-skill>)
    * [Несколько навыков](<#multiple-skills>)
  * [Запуск задачи внутри директории проекта](<#running-a-job-inside-a-project-directory>)
  * [Редактирование задач](<#editing-jobs>)
    * [Чат](<#chat>)
    * [Автономный CLI](<#standalone-cli>)
  * [Действия жизненного цикла](<#lifecycle-actions>)
    * [Чат](<#chat-1>)
    * [Автономный CLI](<#standalone-cli-1>)
  * [Как это работает](<#how-it-works>)
    * [Поведение планировщика шлюза](<#gateway-scheduler-behavior>)
  * [Параметры доставки](<#delivery-options>)
    * [Обёртка ответа](<#response-wrapping>)
    * [Тихая отмена доставки](<#silent-suppression>)
  * [Тайм-аут скрипта](<#script-timeout>)
  * [Режим без агента (только скрипты)](<#no-agent-mode-script-only-jobs>)
    * [Агент настраивает это за вас](<#the-agent-sets-these-up-for-you>)
  * [Цепочки задач с `context_from`](<#chaining-jobs-with-context_from>)
  * [Восстановление провайдера](<#provider-recovery>)
  * [Форматы расписания](<#schedule-formats>)
    * [Относительные задержки (однократно)](<#relative-delays-one-shot>)
    * [Интервалы (повторяющиеся)](<#intervals-recurring>)
    * [Cron-выражения](<#cron-expressions>)
    * [ISO-метки времени](<#iso-timestamps>)
  * [Поведение повторов](<#repeat-behavior>)
  * [Программное управление задачами](<#managing-jobs-programmatically>)
  * [Наборы инструментов, доступные cron-задачам](<#toolsets-available-to-cron-jobs>)
    * [Полный пропуск агента: `wakeAgent`](<#skipping-the-agent-entirely-wakeagent>)
    * [Цепочки задач: `context_from`](<#chaining-jobs-context_from>)
  * [Хранение задач](<#job-storage>)
  * [Самодостаточные запросы по-прежнему важны](<#self-contained-prompts-still-matter>)
  * [Безопасность](<#security>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron -->
