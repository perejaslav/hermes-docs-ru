On this page
Получайте события от внешних сервисов (GitHub, GitLab, JIRA, Stripe и т.д.) и автоматически запускайте выполнение агента Hermes. Адаптер вебхуков запускает HTTP-сервер, который принимает POST-запросы, проверяет HMAC-подписи, преобразует полезные нагрузки в промпты для агента и направляет ответы обратно источнику или на другую настроенную платформу.
Агент обрабатывает событие и может отвечать, оставляя комментарии в PR, отправляя сообщения в Telegram/Discord или записывая результат в лог.
## Video Tutorial[​](<#video-tutorial> "Direct link to Video Tutorial")
* * *
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
  1. Включите через `hermes gateway setup` или переменные окружения
  2. Определите маршруты в `config.yaml` **или** создайте их динамически с помощью `hermes webhook subscribe`
  3. Укажите вашему сервису URL `http://your-server:8644/webhooks/<route-name>`


* * *
## Setup[​](<#setup> "Direct link to Setup")
Есть два способа включить адаптер вебхуков.
### Via setup wizard[​](<#via-setup-wizard> "Direct link to Via setup wizard")
[code] 
    hermes gateway setup  
    
[/code]
Следуйте подсказкам, чтобы включить вебхуки, задать порт и глобальный HMAC-секрет.
### Via environment variables[​](<#via-environment-variables> "Direct link to Via environment variables")
Добавьте в `~/.hermes/.env`:
[code] 
    WEBHOOK_ENABLED=true  
    WEBHOOK_PORT=8644        # по умолчанию  
    WEBHOOK_SECRET=your-global-secret  
    
[/code]
### Verify the server[​](<#verify-the-server> "Direct link to Verify the server")
После запуска шлюза:
[code] 
    curl http://localhost:8644/health  
    
[/code]
Ожидаемый ответ:
[code] 
    {"status": "ok", "platform": "webhook"}  
    
[/code]
* * *
## Configuring Routes[​](<#configuring-routes> "Direct link to Configuring Routes")
Маршруты определяют, как обрабатываются различные источники вебхуков. Каждый маршрут — это именованная запись в разделе `platforms.webhook.extra.routes` вашего `config.yaml`.
### Route properties[​](<#route-properties> "Direct link to Route properties")
Свойство| Обязательно| Описание  
---|---|---  
`events`| Нет| Список типов событий для приёма (например, `["pull_request"]`). Если пусто, принимаются все события. Тип события читается из `X-GitHub-Event`, `X-GitLab-Event` или `event_type` в полезной нагрузке.  
`secret`| **Да**|  HMAC-секрет для проверки подписи. Если не задан на маршруте, используется глобальный `secret`. Установите `"INSECURE_NO_AUTH"` только для тестирования (пропускает проверку).  
`prompt`| Нет| Шаблонная строка с доступом к полям через точечную нотацию (например, `{pull_request.title}`). Если не указан, полная JSON-полезная нагрузка подставляется в промпт.  
`skills`| Нет| Список названий навыков для загрузки в сессию агента.  
`deliver`| Нет| Куда отправлять ответ: `github_comment`, `telegram`, `discord`, `slack`, `signal`, `sms`, `whatsapp`, `matrix`, `mattermost`, `homeassistant`, `email`, `dingtalk`, `feishu`, `wecom`, `weixin`, `bluebubbles`, `qqbot` или `log` (по умолчанию).  
`deliver_extra`| Нет| Дополнительные настройки доставки — ключи зависят от типа `deliver` (например, `repo`, `pr_number`, `chat_id`). Значения поддерживают те же шаблоны `{dot.notation}`, что и `prompt`.  
`deliver_only`| Нет| Если `true`, пропустить агента полностью — отрендеренный шаблон `prompt` становится буквальным сообщением для доставки. Нулевая стоимость LLM, доставка за доли секунды. Подробнее см. [Direct Delivery Mode](<#direct-delivery-mode>). Требует, чтобы `deliver` был реальной целью (не `log`).  
### Full example[​](<#full-example> "Direct link to Full example")
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          port: 8644  
          secret: "global-fallback-secret"  
          routes:  
            github-pr:  
              events: ["pull_request"]  
              secret: "github-webhook-secret"  
              prompt: |  
                Review this pull request:  
                Repository: {repository.full_name}  
                PR #{number}: {pull_request.title}  
                Author: {pull_request.user.login}  
                URL: {pull_request.html_url}  
                Diff URL: {pull_request.diff_url}  
                Action: {action}  
              skills: ["github-code-review"]  
              deliver: "github_comment"  
              deliver_extra:  
                repo: "{repository.full_name}"  
                pr_number: "{number}"  
            deploy-notify:  
              events: ["push"]  
              secret: "deploy-secret"  
              prompt: "New push to {repository.full_name} branch {ref}: {head_commit.message}"  
              deliver: "telegram"  
    
[/code]
### Prompt Templates[​](<#prompt-templates> "Direct link to Prompt Templates")
Промпты используют точечную нотацию для доступа к вложенным полям в полезной нагрузке вебхука:
  * `{pull_request.title}` преобразуется в `payload["pull_request"]["title"]`
  * `{repository.full_name}` преобразуется в `payload["repository"]["full_name"]`
  * `{__raw__}` — специальный токен, который подставляет **всю полезную нагрузку** в виде JSON с отступами (обрезается до 4000 символов). Полезен для мониторинговых оповещений или вебхуков общего назначения, где агенту нужен полный контекст.
  * Отсутствующие ключи остаются как буквальная строка `{key}` (без ошибки)
  * Вложенные словари и списки сериализуются в JSON и обрезаются до 2000 символов


Вы можете смешивать `{__raw__}` с обычными переменными шаблона:
[code] 
    prompt: "PR #{pull_request.number} by {pull_request.user.login}: {__raw__}"  
    
[/code]
Если для маршрута не настроен шаблон `prompt`, вся полезная нагрузка подставляется в виде JSON с отступами (обрезается до 4000 символов).
Те же шаблоны с точечной нотацией работают в значениях `deliver_extra`.
### Forum Topic Delivery[​](<#forum-topic-delivery> "Direct link to Forum Topic Delivery")
При доставке ответов вебхуков в Telegram можно указать конкретную тему форума, включив `message_thread_id` (или `thread_id`) в `deliver_extra`:
[code] 
    webhooks:  
      routes:  
        alerts:  
          events: ["alert"]  
          prompt: "Alert: {__raw__}"  
          deliver: "telegram"  
          deliver_extra:  
            chat_id: "-1001234567890"  
            message_thread_id: "42"  
    
[/code]
Если `chat_id` не указан в `deliver_extra`, доставка выполняется в домашний канал, настроенный для целевой платформы.
* * *
## GitHub PR Review (Step by Step)[​](<#github-pr-review> "Direct link to GitHub PR Review (Step by Step)")
Это пошаговое руководство настраивает автоматическое ревью кода на каждый pull request.
### 1\\. Create the webhook in GitHub[​](<#1-create-the-webhook-in-github> "Direct link to 1. Create the webhook in GitHub")
  1. Перейдите в ваш репозиторий → **Settings** → **Webhooks** → **Add webhook**
  2. Установите **Payload URL** на `http://your-server:8644/webhooks/github-pr`
  3. Установите **Content type** на `application/json`
  4. Установите **Secret** в соответствии с вашей конфигурацией маршрута (например, `github-webhook-secret`)
  5. В разделе **Which events?** выберите **Let me select individual events** и отметьте **Pull requests**
  6. Нажмите **Add webhook**


### 2\\. Add the route config[​](<#2-add-the-route-config> "Direct link to 2. Add the route config")
Добавьте маршрут `github-pr` в ваш `~/.hermes/config.yaml`, как показано в примере выше.
### 3\\. Ensure `gh` CLI is authenticated[​](<#3-ensure-gh-cli-is-authenticated> "Direct link to 3-ensure-gh-cli-is-authenticated")
Тип доставки `github_comment` использует GitHub CLI для публикации комментариев:
[code] 
    gh auth login  
    
[/code]
### 4\\. Test it[​](<#4-test-it> "Direct link to 4. Test it")
Откройте pull request в репозитории. Вебхук срабатывает, Hermes обрабатывает событие и публикует комментарий с ревью в PR.
* * *
## GitLab Webhook Setup[​](<#gitlab-webhook-setup> "Direct link to GitLab Webhook Setup")
Вебхуки GitLab работают аналогично, но используют другой механизм аутентификации. GitLab отправляет секрет в виде обычного заголовка `X-Gitlab-Token` (точное совпадение строки, не HMAC).
### 1\\. Create the webhook in GitLab[​](<#1-create-the-webhook-in-gitlab> "Direct link to 1. Create the webhook in GitLab")
  1. Перейдите в ваш проект → **Settings** → **Webhooks**
  2. Установите **URL** на `http://your-server:8644/webhooks/gitlab-mr`
  3. Введите ваш **Secret token**
  4. Выберите **Merge request events** (и любые другие нужные события)
  5. Нажмите **Add webhook**


### 2\\. Add the route config[​](<#2-add-the-route-config-1> "Direct link to 2. Add the route config")
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          routes:  
            gitlab-mr:  
              events: ["merge_request"]  
              secret: "your-gitlab-secret-token"  
              prompt: |  
                Review this merge request:  
                Project: {project.path_with_namespace}  
                MR !{object_attributes.iid}: {object_attributes.title}  
                Author: {object_attributes.last_commit.author.name}  
                URL: {object_attributes.url}  
                Action: {object_attributes.action}  
              deliver: "log"  
    
[/code]
* * *
## Delivery Options[​](<#delivery-options> "Direct link to Delivery Options")
Поле `deliver` определяет, куда направляется ответ агента после обработки события вебхука.
Тип доставки| Описание  
---|---  
`log`| Записывает ответ в лог шлюза. Это значение по умолчанию, полезно для тестирования.  
`github_comment`| Публикует ответ как комментарий в PR/issue через CLI `gh`. Требует `deliver_extra.repo` и `deliver_extra.pr_number`. CLI `gh` должен быть установлен и аутентифицирован на хосте шлюза (`gh auth login`).  
`telegram`| Направляет ответ в Telegram. Использует домашний канал или `chat_id` в `deliver_extra`.  
`discord`| Направляет ответ в Discord. Использует домашний канал или `chat_id` в `deliver_extra`.  
`slack`| Направляет ответ в Slack. Использует домашний канал или `chat_id` в `deliver_extra`.  
`signal`| Направляет ответ в Signal. Использует домашний канал или `chat_id` в `deliver_extra`.  
`sms`| Направляет ответ в SMS через Twilio. Использует домашний канал или `chat_id` в `deliver_extra`.  
`whatsapp`| Направляет ответ в WhatsApp. Использует домашний канал или `chat_id` в `deliver_extra`.  
`matrix`| Направляет ответ в Matrix. Использует домашний канал или `chat_id` в `deliver_extra`.  
`mattermost`| Направляет ответ в Mattermost. Использует домашний канал или `chat_id` в `deliver_extra`.  
`homeassistant`| Направляет ответ в Home Assistant. Использует домашний канал или `chat_id` в `deliver_extra`.  
`email`| Направляет ответ на Email. Использует домашний канал или `chat_id` в `deliver_extra`.  
`dingtalk`| Направляет ответ в DingTalk. Использует домашний канал или `chat_id` в `deliver_extra`.  
`feishu`| Направляет ответ в Feishu/Lark. Использует домашний канал или `chat_id` в `deliver_extra`.  
`wecom`| Направляет ответ в WeCom. Использует домашний канал или `chat_id` в `deliver_extra`.  
`weixin`| Направляет ответ в Weixin (WeChat). Использует домашний канал или `chat_id` в `deliver_extra`.  
`bluebubbles`| Направляет ответ в BlueBubbles (iMessage). Использует домашний канал или `chat_id` в `deliver_extra`.  
Для кросс-платформенной доставки целевая платформа также должна быть включена и подключена в шлюзе. Если `chat_id` не указан в `deliver_extra`, ответ отправляется в настроенный домашний канал этой платформы.
* * *
## Direct Delivery Mode[​](<#direct-delivery-mode> "Direct link to Direct Delivery Mode")
По умолчанию каждый POST-запрос вебхука запускает сессию агента — полезная нагрузка становится промптом, агент обрабатывает его, и ответ агента доставляется. Это消耗 токены LLM на каждое событие.
Для случаев, когда вам нужно просто **отправить простое уведомление** — без рассуждений, без цикла агента, просто доставить сообщение — установите `deliver_only: true` на маршруте. Отрендеренный шаблон `prompt` становится буквальным телом сообщения, и адаптер отправляет его напрямую в настроенный канал доставки.
### When to use direct delivery[​](<#when-to-use-direct-delivery> "Direct link to When to use direct delivery")
  * **Внешний push от сервиса** — вебхук Supabase/Firebase срабатывает при изменении в БД → мгновенно уведомить пользователя в Telegram
  * **Оповещения мониторинга** — вебхук оповещения Datadog/Grafana → отправить в канал Discord
  * **Межагентские уведомления** — Агент A уведомляет пользователя Агента B о завершении долгой задачи
  * **Завершение фоновых задач** — Cron-задача завершилась → отправить результат в Slack


Преимущества:
  * **Нулевая стоимость LLM** — агент никогда не вызывается
  * **Доставка за доли секунды** — один вызов адаптера, без цикла рассуждений
  * **Та же безопасность, что в режиме агента** — HMAC-аутентификация, лимиты запросов, идемпотентность и ограничения размера тела всё ещё действуют
  * **Синхронный ответ** — POST возвращает `200 OK` после успешной доставки или `502`, если цель отклонила запрос, чтобы ваш вышестоящий сервис мог интеллектуально повторить попытку


### Example: Telegram push from Supabase[​](<#example-telegram-push-from-supabase> "Direct link to Example: Telegram push from Supabase")
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          port: 8644  
          secret: "global-secret"  
          routes:  
            antenna-matches:  
              secret: "antenna-webhook-secret"  
              deliver: "telegram"  
              deliver_only: true  
              prompt: "🎉 New match: {match.user_name} matched with you!"  
              deliver_extra:  
                chat_id: "{match.telegram_chat_id}"  
    
[/code]
Ваша edge-функция Supabase подписывает полезную нагрузку с помощью HMAC-SHA256 и отправляет POST на `https://your-server:8644/webhooks/antenna-matches`. Адаптер вебхуков проверяет подпись, рендерит шаблон из полезной нагрузки, доставляет в Telegram и возвращает `200 OK`.
### Example: Dynamic subscription via CLI[​](<#example-dynamic-subscription-via-cli> "Direct link to Example: Dynamic subscription via CLI")
[code] 
    hermes webhook subscribe antenna-matches \  
      --deliver telegram \  
      --deliver-chat-id "123456789" \  
      --deliver-only \  
      --prompt "🎉 New match: {match.user_name} matched with you!" \  
      --description "Antenna match notifications"  
    
[/code]
### Response codes[​](<#response-codes> "Direct link to Response codes")
Статус| Значение  
---|---  
`200 OK`| Доставлено успешно. Тело: `{"status": "delivered", "route": "...", "target": "...", "delivery_id": "..."}`  
`200 OK` (status=duplicate)| Дубликат `X-GitHub-Delivery` ID в пределах TTL идемпотентности (1 час). Повторно не доставляется.  
`401 Unauthorized`| HMAC-подпись недействительна или отсутствует.  
`400 Bad Request`| Некорректное JSON-тело.  
`404 Not Found`| Неизвестное имя маршрута.  
`413 Payload Too Large`| Тело превысило `max_body_bytes`.  
`429 Too Many Requests`| Превышен лимит запросов для маршрута.  
`502 Bad Gateway`| Целевой адаптер отклонил сообщение или вызвал ошибку. Ошибка логируется на сервере; тело ответа — общее `Delivery failed` для предотвращения утечки внутренних данных адаптера.  
### Configuration gotchas[​](<#configuration-gotchas> "Direct link to Configuration gotchas")
  * `deliver_only: true` требует, чтобы `deliver` был реальной целью. `deliver: log` (или отсутствие `deliver`) вызывает ошибку при запуске — адаптер отказывается запускаться, если находит неправильно настроенный маршрут.
  * Поле `skills` игнорируется в режиме прямой доставки (запуск агента не происходит, поэтому некуда внедрять навыки).
  * Рендеринг шаблонов использует тот же синтаксис `{dot.notation}`, что и в режиме агента, включая токен `{__raw__}`.
  * Идемпотентность использует тот же заголовок `X-GitHub-Delivery` / `X-Request-ID` — повторные попытки с тем же ID возвращают `status=duplicate` и НЕ выполняют повторную доставку.


* * *
## Dynamic Subscriptions (CLI)[​](<#dynamic-subscriptions> "Direct link to Dynamic Subscriptions (CLI)")
В дополнение к статическим маршрутам в `config.yaml` вы можете динамически создавать подписки на вебхуки с помощью CLI-команды `hermes webhook`. Это особенно полезно, когда самому агенту нужно настроить управляемые событиями триггеры.
### Create a subscription[​](<#create-a-subscription> "Direct link to Create a subscription")
[code] 
    hermes webhook subscribe github-issues \  
      --events "issues" \  
      --prompt "New issue #{issue.number}: {issue.title}\nBy: {issue.user.login}\n\n{issue.body}" \  
      --deliver telegram \  
      --deliver-chat-id "-100123456789" \  
      --description "Triage new GitHub issues"  
    
[/code]
Эта команда возвращает URL вебхука и автоматически сгенерированный HMAC-секрет. Настройте ваш сервис на отправку POST-запросов на этот URL.
### List subscriptions[​](<#list-subscriptions> "Direct link to List subscriptions")
[code] 
    hermes webhook list  
    
[/code]
### Remove a subscription[​](<#remove-a-subscription> "Direct link to Remove a subscription")
[code] 
    hermes webhook remove github-issues  
    
[/code]
### Test a subscription[​](<#test-a-subscription> "Direct link to Test a subscription")
[code] 
    hermes webhook test github-issues  
    hermes webhook test github-issues --payload '{"issue": {"number": 42, "title": "Test"}}'  
    
[/code]
### How dynamic subscriptions work[​](<#how-dynamic-subscriptions-work> "Direct link to How dynamic subscriptions work")
  * Подписки хранятся в `~/.hermes/webhook_subscriptions.json`
  * Адаптер вебхуков автоматически перезагружает этот файл при каждом входящем запросе (проверка mtime, минимальные накладные расходы)
  * Статические маршруты из `config.yaml` всегда имеют приоритет над динамическими с тем же именем
  * Динамические подписки используют тот же формат и возможности маршрутов, что и статические (события, шаблоны промптов, навыки, доставка)
  * Перезапуск шлюза не требуется — подписка создаётся и сразу работает


### Agent-driven subscriptions[​](<#agent-driven-subscriptions> "Direct link to Agent-driven subscriptions")
Агент может создавать подписки через инструмент терминала, если ему предоставлен навык `webhook-subscriptions`. Попросите агента «настроить вебхук для GitHub issues», и он выполнит соответствующую команду `hermes webhook subscribe`.
* * *
## Security[​](<#security> "Direct link to Security")
Адаптер вебхуков включает несколько уровней безопасности:
### HMAC signature validation[​](<#hmac-signature-validation> "Direct link to HMAC signature validation")
Адаптер проверяет входящие подписи вебхуков, используя соответствующий метод для каждого источника:
  * **GitHub** : заголовок `X-Hub-Signature-256` — HMAC-SHA256 шестнадцатеричный дайджест с префиксом `sha256=`
  * **GitLab** : заголовок `X-Gitlab-Token` — обычное совпадение строки секрета
  * **Generic** : заголовок `X-Webhook-Signature` — сырой HMAC-SHA256 шестнадцатеричный дайджест


Если секрет настроен, но ни один распознанный заголовок подписи не присутствует, запрос отклоняется.
### Secret is required[​](<#secret-is-required> "Direct link to Secret is required")
Каждый маршрут должен иметь секрет — либо заданный непосредственно на маршруте, либо унаследованный от глобального `secret`. Маршруты без секрета вызывают ошибку при запуске адаптера. Только для разработки/тестирования вы можете установить секрет в `"INSECURE_NO_AUTH"`, чтобы полностью пропустить проверку.
### Rate limiting[​](<#rate-limiting> "Direct link to Rate limiting")
Каждый маршрут ограничен **30 запросами в минуту** по умолчанию (фиксированное окно). Настройте глобально:
[code] 
    platforms:  
      webhook:  
        extra:  
          rate_limit: 60  # запросов в минуту  
    
[/code]
Запросы, превышающие лимит, получают ответ `429 Too Many Requests`.
### Idempotency[​](<#idempotency> "Direct link to Idempotency")
Идентификаторы доставки (из `X-GitHub-Delivery`, `X-Request-ID` или запасной вариант на основе временной метки) кэшируются на **1 час**. Повторные доставки (например, повторные попытки вебхука) молча пропускаются с ответом `200`, предотвращая повторные запуски агента.
### Body size limits[​](<#body-size-limits> "Direct link to Body size limits")
Полезные нагрузки, превышающие **1 МБ**, отклоняются до чтения тела. Настройка:
[code] 
    platforms:  
      webhook:  
        extra:  
          max_body_bytes: 2097152  # 2 МБ  
    
[/code]
### Prompt injection risk[​](<#prompt-injection-risk> "Direct link to Prompt injection risk")
warning
Полезные нагрузки вебхуков содержат данные, контролируемые атакующим — заголовки PR, сообщения коммитов, описания issues и т.д. могут содержать вредоносные инструкции. Запускайте шлюз в изолированной среде (Docker, ВМ) при доступе из интернета. Рассмотрите использование Docker или SSH бэкенда терминала для изоляции.
* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### Webhook not arriving[​](<#webhook-not-arriving> "Direct link to Webhook not arriving")
  * Убедитесь, что порт открыт и доступен из источника вебхука
  * Проверьте правила брандмауэра — порт `8644` (или настроенный вами порт) должен быть открыт
  * Проверьте, что путь URL совпадает: `http://your-server:8644/webhooks/<имя-маршрута>`
  * Используйте эндпоинт `/health` чтобы убедиться, что сервер запущен


### Signature validation failing[​](<#signature-validation-failing> "Direct link to Signature validation failing")
  * Убедитесь, что секрет в вашей конфигурации маршрута точно совпадает с секретом, настроенным в источнике вебхука
  * Для GitHub секрет основан на HMAC — проверьте `X-Hub-Signature-256`
  * Для GitLab секрет — это обычный токен — проверьте `X-Gitlab-Token`
  * Проверьте логи шлюза на наличие предупреждений `Invalid signature`


### Event being ignored[​](<#event-being-ignored> "Direct link to Event being ignored")
  * Проверьте, что тип события входит в список `events` вашего маршрута
  * События GitHub используют значения, такие как `pull_request`, `push`, `issues` (значение заголовка `X-GitHub-Event`)
  * События GitLab используют значения, такие как `merge_request`, `push` (значение заголовка `X-GitLab-Event`)
  * Если `events` пуст или не задан, принимаются все события


### Agent not responding[​](<#agent-not-responding> "Direct link to Agent not responding")
  * Запустите шлюз в режиме переднего плана, чтобы видеть логи: `hermes gateway run`
  * Проверьте, что шаблон промпта рендерится корректно
  * Убедитесь, что целевой канал доставки настроен и подключён


### Duplicate responses[​](<#duplicate-responses> "Direct link to Duplicate responses")
  * Кэш идемпотентности должен предотвращать это — проверьте, что источник вебхука отправляет заголовок с ID доставки (`X-GitHub-Delivery` или `X-Request-ID`)
  * Идентификаторы доставки кэшируются на 1 час


### `gh` CLI errors (GitHub comment delivery)[​](<#gh-cli-errors-github-comment-delivery> "Direct link to gh-cli-errors-github-comment-delivery")
  * Запустите `gh auth login` на хосте шлюза
  * Убедитесь, что аутентифицированный пользователь GitHub имеет права на запись в репозиторий
  * Проверьте, что `gh` установлен и находится в PATH


* * *
## Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
Переменная| Описание| По умолчанию  
---|---|---  
`WEBHOOK_ENABLED`| Включить адаптер платформы вебхуков| `false`  
`WEBHOOK_PORT`| Порт HTTP-сервера для приёма вебхуков| `8644`  
`WEBHOOK_SECRET`| Глобальный HMAC-секрет (используется, когда маршруты не указывают свой собственный)| _(нет)_  
  * [Video Tutorial](<#video-tutorial>)
  * [Quick Start](<#quick-start>)
  * [Setup](<#setup>)
    * [Via setup wizard](<#via-setup-wizard>)
    * [Via environment variables](<#via-environment-variables>)
    * [Verify the server](<#verify-the-server>)
  * [Configuring Routes](<#configuring-routes>)
    * [Route properties](<#route-properties>)
    * [Full example](<#full-example>)
    * [Prompt Templates](<#prompt-templates>)
    * [Forum Topic Delivery](<#forum-topic-delivery>)
  * [GitHub PR Review (Step by Step)](<#github-pr-review>)
    * [1\\. Create the webhook in GitHub](<#1-create-the-webhook-in-github>)
    * [2\\. Add the route config](<#2-add-the-route-config>)
    * [3\\. Ensure `gh` CLI is authenticated](<#3-ensure-gh-cli-is-authenticated>)
    * [4\\. Test it](<#4-test-it>)
  * [GitLab Webhook Setup](<#gitlab-webhook-setup>)
    * [1\\. Create the webhook in GitLab](<#1-create-the-webhook-in-gitlab>)
    * [2\\. Add the route config](<#2-add-the-route-config-1>)
  * [Delivery Options](<#delivery-options>)
  * [Direct Delivery Mode](<#direct-delivery-mode>)
    * [When to use direct delivery](<#when-to-use-direct-delivery>)
    * [Example: Telegram push from Supabase](<#example-telegram-push-from-supabase>)
    * [Example: Dynamic subscription via CLI](<#example-dynamic-subscription-via-cli>)
    * [Response codes](<#response-codes>)
    * [Configuration gotchas](<#configuration-gotchas>)
  * [Dynamic Subscriptions (CLI)](<#dynamic-subscriptions>)
    * [Create a subscription](<#create-a-subscription>)
    * [List subscriptions](<#list-subscriptions>)
    * [Remove a subscription](<#remove-a-subscription>)
    * [Test a subscription](<#test-a-subscription>)
    * [How dynamic subscriptions work](<#how-dynamic-subscriptions-work>)
    * [Agent-driven subscriptions](<#agent-driven-subscriptions>)
  * [Security](<#security>)
    * [HMAC signature validation](<#hmac-signature-validation>)
    * [Secret is required](<#secret-is-required>)
    * [Rate limiting](<#rate-limiting>)
    * [Idempotency](<#idempotency>)
    * [Body size limits](<#body-size-limits>)
    * [Prompt injection risk](<#prompt-injection-risk>)
  * [Troubleshooting](<#troubleshooting>)
    * [Webhook not arriving](<#webhook-not-arriving>)
    * [Signature validation failing](<#signature-validation-failing>)
    * [Event being ignored](<#event-being-ignored>)
    * [Agent not responding](<#agent-not-responding>)
    * [Duplicate responses](<#duplicate-responses>)
    * [`gh` CLI errors (GitHub comment delivery)](<#gh-cli-errors-github-comment-delivery>)
  * [Environment Variables](<#environment-variables>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks -->
