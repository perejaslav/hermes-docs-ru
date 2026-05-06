On this page
В этом руководстве описано, как подключить Hermes Agent к GitHub, чтобы он автоматически получал diff пул-реквеста, анализировал изменения в коде и публиковал комментарий — запускаемый вебхук-событием без ручного вмешательства.
Когда PR открывается или обновляется, GitHub отправляет POST-запрос вебхука на ваш экземпляр Hermes. Hermes запускает агента с промптом, который предписывает ему получить diff через CLI `gh`, а ответ публикуется обратно в ветку PR.
Хотите более простую настройку без публичного эндпоинта?
Если у вас нет публичного URL или вы просто хотите быстро начать, посмотрите [Создание агента ревью PR на GitHub](</docs/guides/github-pr-review-agent>) — использует cron-задачи для опроса PR по расписанию, работает за NAT и файрволами.
Справочная документация
Полную справочную документацию по платформе вебхуков (все параметры конфигурации, типы доставки, динамические подписки, модель безопасности) см. в [Вебхуки](</docs/user-guide/messaging/webhooks>).
Риск внедрения промптов
Полезные данные вебхука содержат данные, контролируемые злоумышленником — заголовки PR, сообщения коммитов и описания могут содержать вредоносные инструкции. Если ваш эндпоинт вебхука доступен из интернета, запускайте шлюз в изолированной среде (Docker, SSH-бэкенд). См. [раздел безопасности](<#security-notes>) ниже.
* * *
## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")
  * Hermes Agent установлен и запущен (`hermes gateway`)
  * [`gh` CLI](<https://cli.github.com/>) установлен и аутентифицирован на хосте шлюза (`gh auth login`)
  * Публично доступный URL для вашего экземпляра Hermes (см. [Локальное тестирование с ngrok](<#local-testing-with-ngrok>) если запускаете локально)
  * Административный доступ к репозиторию GitHub (требуется для управления вебхуками)


* * *
## Шаг 1 — Включение платформы вебхуков[​](<#step-1--enable-the-webhook-platform> "Direct link to Step 1 — Enable the webhook platform")
Добавьте следующее в ваш `~/.hermes/config.yaml`:
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          port: 8644          # значение по умолчанию; измените, если порт занят другим сервисом  
          rate_limit: 30      # макс. запросов в минуту на маршрут (не глобальное ограничение)  
      
          routes:  
            github-pr-review:  
              secret: "your-webhook-secret-here"   # должно точно совпадать с секретом вебхука GitHub  
              events:  
                - pull_request  
      
              # Агенту даётся инструкция получить актуальный diff перед ревью.  
              # {number} и {repository.full_name} извлекаются из полезной нагрузки GitHub.  
              prompt: |  
                A pull request event was received (action: {action}).  
      
                PR #{number}: {pull_request.title}  
                Author: {pull_request.user.login}  
                Branch: {pull_request.head.ref} → {pull_request.base.ref}  
                Description: {pull_request.body}  
                URL: {pull_request.html_url}  
      
                If the action is "closed" or "labeled", stop here and do not post a comment.  
      
                Otherwise:  
                1. Run: gh pr diff {number} --repo {repository.full_name}  
                2. Review the code changes for correctness, security issues, and clarity.  
                3. Write a concise, actionable review comment and post it.  
      
              deliver: github_comment  
              deliver_extra:  
                repo: "{repository.full_name}"  
                pr_number: "{number}"  
    
[/code]
**Ключевые поля:**
Поле| Описание  
---|---  
`secret` (на уровне маршрута)| HMAC-секрет для этого маршрута. Если опущен, используется глобальный `extra.secret`.  
`events`| Список значений заголовка `X-GitHub-Event` для приёма. Пустой список = принимать все.  
`prompt`| Шаблон; `{field}` и `{nested.field}` извлекаются из полезной нагрузки GitHub.  
`deliver`| `github_comment` публикует через `gh pr comment`. `log` просто записывает в лог шлюза.  
`deliver_extra.repo`| Извлекается, например, в `org/repo` из полезной нагрузки.  
`deliver_extra.pr_number`| Извлекается в номер PR из полезной нагрузки.  
Полезная нагрузка не содержит код
Полезная нагрузка вебхука GitHub включает метаданные PR (заголовок, описание, имена веток, URL), но **не diff**. Промпт выше даёт агенту инструкцию выполнить `gh pr diff` для получения актуальных изменений. Инструмент `terminal` входит в стандартный набор инструментов `hermes-webhook`, поэтому дополнительная настройка не требуется.
* * *
## Шаг 2 — Запуск шлюза[​](<#step-2--start-the-gateway> "Direct link to Step 2 — Start the gateway")
[code] 
    hermes gateway  
    
[/code]
Вы должны увидеть:
[code] 
    [webhook] Listening on 0.0.0.0:8644 — routes: github-pr-review  
    
[/code]
Проверьте, что он работает:
[code] 
    curl http://localhost:8644/health  
    # {"status": "ok", "platform": "webhook"}  
    
[/code]
* * *
## Шаг 3 — Регистрация вебхука на GitHub[​](<#step-3--register-the-webhook-on-github> "Direct link to Step 3 — Register the webhook on GitHub")
  1. Перейдите в ваш репозиторий → **Settings** → **Webhooks** → **Add webhook**
  2. Заполните:
     * **Payload URL:** `https://your-public-url.example.com/webhooks/github-pr-review`
     * **Content type:** `application/json`
     * **Secret:** то же значение, которое вы указали в `secret` в конфигурации маршрута
     * **Which events?** → Выберите отдельные события → отметьте **Pull requests**
  3. Нажмите **Add webhook**


GitHub немедленно отправит событие `ping` для подтверждения соединения. Оно безопасно игнорируется — `ping` нет в вашем списке `events` — и возвращает `{"status": "ignored", "event": "ping"}`. Оно логируется только на уровне DEBUG, поэтому не появится в консоли при стандартном уровне логирования.
* * *
## Шаг 4 — Открытие тестового PR[​](<#step-4--open-a-test-pr> "Direct link to Step 4 — Open a test PR")
Создайте ветку, запушьте изменение и откройте PR. В течение 30–90 секунд (в зависимости от размера PR и модели) Hermes должен опубликовать комментарий с ревью.
Чтобы следить за прогрессом агента в реальном времени:
[code] 
    tail -f "${HERMES_HOME:-$HOME/.hermes}/logs/gateway.log"  
    
[/code]
* * *
## Локальное тестирование с ngrok[​](<#local-testing-with-ngrok> "Direct link to Local testing with ngrok")
Если Hermes запущен на вашем ноутбуке, используйте [ngrok](<https://ngrok.com/>) чтобы открыть доступ к нему:
[code] 
    ngrok http 8644  
    
[/code]
Скопируйте URL `https://...ngrok-free.app` и используйте его как Payload URL на GitHub. На бесплатном тарифе ngrok URL меняется при каждом перезапуске ngrok — обновляйте вебхук GitHub в каждой сессии. Платные аккаунты ngrok получают статический домен.
Вы можете протестировать статический маршрут напрямую через `curl` — без аккаунта GitHub или настоящего PR.
Используйте `deliver: log` при локальном тестировании
Замените `deliver: github_comment` на `deliver: log` в вашей конфигурации на время тестирования. Иначе агент попытается опубликовать комментарий в фиктивный репозиторий `org/repo#99` из тестовой полезной нагрузки, что приведёт к ошибке. Переключитесь обратно на `deliver: github_comment`, когда результат промпта вас устроит.
[code] 
    SECRET="your-webhook-secret-here"  
    BODY='{"action":"opened","number":99,"pull_request":{"title":"Test PR","body":"Adds a feature.","user":{"login":"testuser"},"head":{"ref":"feat/x"},"base":{"ref":"main"},"html_url":"https://github.com/org/repo/pull/99"},"repository":{"full_name":"org/repo"}}'  
    SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$SECRET" -hex | awk '{print "sha256="$2}')  
      
    curl -s -X POST http://localhost:8644/webhooks/github-pr-review \  
      -H "Content-Type: application/json" \  
      -H "X-GitHub-Event: pull_request" \  
      -H "X-Hub-Signature-256: $SIG" \  
      -d "$BODY"  
    # Expected: {"status":"accepted","route":"github-pr-review","event":"pull_request","delivery_id":"..."}  
    
[/code]
Затем наблюдайте за работой агента:
[code] 
    tail -f "${HERMES_HOME:-$HOME/.hermes}/logs/gateway.log"  
    
[/code]
note
`hermes webhook test <name>` работает только для **динамических подписок**, созданных с помощью `hermes webhook subscribe`. Он не читает маршруты из `config.yaml`.
* * *
## Фильтрация по конкретным действиям[​](<#filtering-to-specific-actions> "Direct link to Filtering to specific actions")
GitHub отправляет события `pull_request` для многих действий: `opened`, `synchronize`, `reopened`, `closed`, `labeled` и т.д. Список `events` фильтрует только по значению заголовка `X-GitHub-Event` — он не может фильтровать по подтипу действия на уровне маршрутизации.
Промпт из Шага 1 уже обрабатывает это, давая агенту инструкцию остановиться для событий `closed` и `labeled`.
Агент всё равно запускается и расходует токены
Инструкция «остановись здесь» предотвращает осмысленное ревью, но агент всё равно выполняется до конца для каждого события `pull_request` независимо от действия. Вебхуки GitHub могут фильтровать только по типу события (`pull_request`, `push`, `issues` и т.д.) — не по подтипу действия (`opened`, `closed`, `labeled`). Фильтрации поддействий на уровне маршрутизации нет. Для репозиториев с высокой нагрузкой примите эти затраты или фильтруйте вышестоящим образом с помощью рабочего процесса GitHub Actions, который вызывает URL вашего вебхука условно.
> Синтаксис Jinja2 или условных шаблонов отсутствует. Поддерживаются только подстановки `{field}` и `{nested.field}`. Всё остальное передаётся агенту как есть.
* * *
## Использование навыка для единообразного стиля ревью[​](<#using-a-skill-for-consistent-review-style> "Direct link to Using a skill for consistent review style")
Загрузите [навык Hermes](</docs/user-guide/features/skills>) чтобы задать агенту единообразную персону ревьюера. Добавьте `skills` в ваш маршрут внутри `platforms.webhook.extra.routes` в `config.yaml`:
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          routes:  
            github-pr-review:  
              secret: "your-webhook-secret-here"  
              events: [pull_request]  
              prompt: |  
                A pull request event was received (action: {action}).  
                PR #{number}: {pull_request.title} by {pull_request.user.login}  
                URL: {pull_request.html_url}  
      
                If the action is "closed" or "labeled", stop here and do not post a comment.  
      
                Otherwise:  
                1. Run: gh pr diff {number} --repo {repository.full_name}  
                2. Review the diff using your review guidelines.  
                3. Write a concise, actionable review comment and post it.  
              skills:  
                - review  
              deliver: github_comment  
              deliver_extra:  
                repo: "{repository.full_name}"  
                pr_number: "{number}"  
    
[/code]
> **Примечание:** Загружается только первый найденный навык из списка. Hermes не накапливает несколько навыков — последующие записи игнорируются.
* * *
## Отправка ответов в Slack или Discord[​](<#sending-responses-to-slack-or-discord-instead> "Direct link to Sending responses to Slack or Discord instead")
Замените поля `deliver` и `deliver_extra` внутри вашего маршрута на целевую платформу:
[code] 
    # Inside platforms.webhook.extra.routes.<route-name>:  
      
    # Slack  
    deliver: slack  
    deliver_extra:  
      chat_id: "C0123456789"   # ID канала Slack (опустите для использования настроенного домашнего канала)  
      
    # Discord  
    deliver: discord  
    deliver_extra:  
      chat_id: "987654321012345678"  # ID канала Discord (опустите для использования домашнего канала)  
    
[/code]
Целевая платформа также должна быть включена и подключена в шлюзе. Если `chat_id` опущен, ответ отправляется в настроенный домашний канал этой платформы.
Допустимые значения `deliver`: `log` · `github_comment` · `telegram` · `discord` · `slack` · `signal` · `sms`
* * *
## Поддержка GitLab[​](<#gitlab-support> "Direct link to GitLab support")
Тот же адаптер работает с GitLab. GitLab использует `X-Gitlab-Token` для аутентификации (простое строковое сравнение, не HMAC) — Hermes обрабатывает оба варианта автоматически.
Для фильтрации событий GitLab устанавливает `X-GitLab-Event` в значения типа `Merge Request Hook`, `Push Hook`, `Pipeline Hook`. Используйте точное значение заголовка в `events`:
[code] 
    events:  
      - Merge Request Hook  
    
[/code]
Поля полезной нагрузки GitLab отличаются от GitHub — например, `{object_attributes.title}` для заголовка MR и `{object_attributes.iid}` для номера MR. Самый простой способ узнать полную структуру полезной нагрузки — использовать кнопку **Test** GitLab в настройках вебхука в сочетании с журналом **Recent Deliveries**. Альтернативно, опустите `prompt` в конфигурации маршрута — тогда Hermes передаст агенту полную полезную нагрузку в виде отформатированного JSON, и ответ агента (видимый в логе шлюза с `deliver: log`) опишет её структуру.
* * *
## Замечания по безопасности[​](<#security-notes> "Direct link to Security notes")
  * **Никогда не используйте`INSECURE_NO_AUTH`** в продакшене — это полностью отключает проверку подписи. Только для локальной разработки.
  * **Регулярно меняйте секрет вебхука** и обновляйте его как на GitHub (настройки вебхука), так и в вашем `config.yaml`.
  * **Ограничение частоты запросов** — 30 запр./мин на маршрут по умолчанию (настраивается через `extra.rate_limit`). Превышение возвращает `429`.
  * **Дублирующиеся доставки** (повторные попытки вебхука) дедуплицируются через кэш идемпотентности на 1 час. Ключ кэша — `X-GitHub-Delivery` (если есть), затем `X-Request-ID`, затем метка времени в миллисекундах. Если ни один из заголовков ID доставки не установлен, повторные попытки **не** дедуплицируются.
  * **Внедрение промптов:** заголовки PR, описания и сообщения коммитов контролируются злоумышленником. Вредоносные PR могут попытаться манипулировать действиями агента. Запускайте шлюз в изолированной среде (Docker, VM) при доступе из публичного интернета.


* * *
## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")
Симптом| Проверка  
---|---  
`401 Invalid signature`| Секрет в config.yaml не совпадает с секретом вебхука GitHub  
`404 Unknown route`| Имя маршрута в URL не совпадает с ключом в `routes:`  
`429 Rate limit exceeded`| Превышено 30 запр./мин на маршрут — часто при повторной доставке тестовых событий из UI GitHub; подождите минуту или увеличьте `extra.rate_limit`  
Комментарий не опубликован| `gh` не установлен, не найден в PATH или не аутентифицирован (`gh auth login`)  
Агент запускается, но комментария нет| Проверьте лог шлюза — если вывод агента был пустым или содержал только «SKIP», доставка всё равно будет предпринята  
Порт уже занят| Измените `extra.port` в config.yaml  
Агент запускается, но ревьюит только описание PR| В промпте нет инструкции `gh pr diff` — diff отсутствует в полезной нагрузке вебхука  
Не видно ping-событие| Игнорируемые события возвращают `{"status":"ignored","event":"ping"}` только на уровне DEBUG — проверьте журнал доставки GitHub (репозиторий → Settings → Webhooks → ваш вебхук → Recent Deliveries)  
**Вкладка Recent Deliveries на GitHub** (репозиторий → Settings → Webhooks → ваш вебхук) показывает точные заголовки запроса, полезную нагрузку, HTTP-статус и тело ответа для каждой доставки. Это самый быстрый способ диагностировать ошибки без обращения к вашим серверным логам.
* * *
## Полная справочная конфигурация[​](<#full-config-reference> "Direct link to Full config reference")
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          host: "0.0.0.0"         # адрес привязки (по умолч.: 0.0.0.0)  
          port: 8644               # порт прослушивания (по умолч.: 8644)  
          secret: ""               # опциональный глобальный секрет запасного варианта  
          rate_limit: 30           # запросов в минуту на маршрут  
          max_body_bytes: 1048576  # лимит размера полезной нагрузки в байтах (по умолч.: 1 МБ)  
      
          routes:  
            <route-name>:  
              secret: "required-per-route"  
              events: []            # [] = принимать все; иначе список значений X-GitHub-Event  
              prompt: ""            # {field} / {nested.field} извлекаются из полезной нагрузки  
              skills: []            # загружается первый подходящий навык (только один)  
              deliver: "log"        # log | github_comment | telegram | discord | slack | signal | sms  
              deliver_extra: {}     # repo + pr_number для github_comment; chat_id для остальных  
    
[/code]
* * *
## Что дальше?[​](<#whats-next> "Direct link to What's Next?")
  * **[Ревью PR на основе Cron](</docs/guides/github-pr-review-agent>)** — опрос PR по расписанию, без публичного эндпоинта
  * **[Справочник по вебхукам](</docs/user-guide/messaging/webhooks>)** — полная справочная конфигурация платформы вебхуков
  * **[Создание плагина](</docs/guides/build-a-hermes-plugin>)** — упаковка логики ревью в распространяемый плагин
  * **[Профили](</docs/user-guide/profiles>)** — запуск выделенного профиля ревьюера с собственной памятью и конфигурацией


  * [Предварительные требования](<#prerequisites>)
  * [Шаг 1 — Включение платформы вебхуков](<#step-1--enable-the-webhook-platform>)
  * [Шаг 2 — Запуск шлюза](<#step-2--start-the-gateway>)
  * [Шаг 3 — Регистрация вебхука на GitHub](<#step-3--register-the-webhook-on-github>)
  * [Шаг 4 — Открытие тестового PR](<#step-4--open-a-test-pr>)
  * [Локальное тестирование с ngrok](<#local-testing-with-ngrok>)
  * [Фильтрация по конкретным действиям](<#filtering-to-specific-actions>)
  * [Использование навыка для единообразного стиля ревью](<#using-a-skill-for-consistent-review-style>)
  * [Отправка ответов в Slack или Discord](<#sending-responses-to-slack-or-discord-instead>)
  * [Поддержка GitLab](<#gitlab-support>)
  * [Замечания по безопасности](<#security-notes>)
  * [Устранение неполадок](<#troubleshooting>)
  * [Полная справочная конфигурация](<#full-config-reference>)
  * [Что дальше?](<#whats-next>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/webhook-github-pr-review -->
