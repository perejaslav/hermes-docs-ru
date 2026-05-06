На этой странице
Вебхук-подписки: запуски агента по событиям.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на раздел «Метаданные навыка»")
|   |   
|---|---  
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/devops/webhook-subscriptions`  
|Версия| `1.1.0`  
|Теги| `webhook`, `events`, `automation`, `integrations`, `notifications`, `push`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на раздел «Справочник: полный SKILL.md»")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Webhook Subscriptions
Создавайте динамические вебхук-подписки, чтобы внешние сервисы (GitHub, GitLab, Stripe, CI/CD, IoT-сенсоры, инструменты мониторинга) могли запускать выполнение агента Hermes, отправляя POST-запросы с событиями на URL.
## Настройка (обязательно сначала)[​](<#setup-required-first> "Прямая ссылка на раздел «Настройка (обязательно сначала)»")
Платформа вебхуков должна быть включена до того, как можно будет создавать подписки. Проверьте с помощью:
[code] 
    hermes webhook list  
    
[/code]
Если выводится «Webhook platform is not enabled», выполните настройку:
### Вариант 1: Мастер настройки[​](<#option-1-setup-wizard> "Прямая ссылка на раздел «Вариант 1: Мастер настройки»")
[code] 
    hermes gateway setup  
    
[/code]
Следуйте подсказкам, чтобы включить вебхуки, установить порт и глобальный HMAC-секрет.
### Вариант 2: Ручная настройка[​](<#option-2-manual-config> "Прямая ссылка на раздел «Вариант 2: Ручная настройка»")
Добавьте в `~/.hermes/config.yaml`:
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          host: "0.0.0.0"  
          port: 8644  
          secret: "generate-a-strong-secret-here"  
    
[/code]
### Вариант 3: Переменные окружения[​](<#option-3-environment-variables> "Прямая ссылка на раздел «Вариант 3: Переменные окружения»")
Добавьте в `~/.hermes/.env`:
[code] 
    WEBHOOK_ENABLED=true  
    WEBHOOK_PORT=8644  
    WEBHOOK_SECRET=generate-a-strong-secret-here  
    
[/code]
После настройки запустите (или перезапустите) шлюз:
[code] 
    hermes gateway run  
    # Or if using systemd:  
    systemctl --user restart hermes-gateway  
    
[/code]
Проверьте, что он работает:
[code] 
    curl http://localhost:8644/health  
    
[/code]
## Команды[​](<#commands> "Прямая ссылка на раздел «Команды»")
Всё управление осуществляется через CLI-команду `hermes webhook`:
### Создать подписку[​](<#create-a-subscription> "Прямая ссылка на раздел «Создать подписку»")
[code] 
    hermes webhook subscribe <name> \  
      --prompt "Prompt template with {payload.fields}" \  
      --events "event1,event2" \  
      --description "What this does" \  
      --skills "skill1,skill2" \  
      --deliver telegram \  
      --deliver-chat-id "12345" \  
      --secret "optional-custom-secret"  
    
[/code]
Возвращает URL вебхука и HMAC-секрет. Пользователь настраивает свой сервис на отправку POST-запросов на этот URL.
### Список подписок[​](<#list-subscriptions> "Прямая ссылка на раздел «Список подписок»")
[code] 
    hermes webhook list  
    
[/code]
### Удалить подписку[​](<#remove-a-subscription> "Прямая ссылка на раздел «Удалить подписку»")
[code] 
    hermes webhook remove <name>  
    
[/code]
### Протестировать подписку[​](<#test-a-subscription> "Прямая ссылка на раздел «Протестировать подписку»")
[code] 
    hermes webhook test <name>  
    hermes webhook test <name> --payload '{"key": "value"}'  
    
[/code]
## Шаблоны промптов[​](<#prompt-templates> "Прямая ссылка на раздел «Шаблоны промптов»")
Промпты поддерживают `{dot.notation}` для доступа к вложенным полям payload:
  * `{issue.title}` — заголовок issue GitHub
  * `{pull_request.user.login}` — автор PR
  * `{data.object.amount}` — сумма платежа Stripe
  * `{sensor.temperature}` — показания IoT-сенсора


Если промпт не указан, полный JSON-пэйлоад помещается в промпт агента как есть.
## Типовые сценарии[​](<#common-patterns> "Прямая ссылка на раздел «Типовые сценарии»")
### GitHub: новые issues[​](<#github-new-issues> "Прямая ссылка на раздел «GitHub: новые issues»")
[code] 
    hermes webhook subscribe github-issues \  
      --events "issues" \  
      --prompt "New GitHub issue #{issue.number}: {issue.title}\n\nAction: {action}\nAuthor: {issue.user.login}\nBody:\n{issue.body}\n\nPlease triage this issue." \  
      --deliver telegram \  
      --deliver-chat-id "-100123456789"  
    
[/code]
Затем в настройках репозитория GitHub → Settings → Webhooks → Add webhook:
  * Payload URL: полученный webhook_url
  * Content type: application/json
  * Secret: полученный secret
  * Events: «Issues»


### GitHub: ревью PR[​](<#github-pr-reviews> "Прямая ссылка на раздел «GitHub: ревью PR»")
[code] 
    hermes webhook subscribe github-prs \  
      --events "pull_request" \  
      --prompt "PR #{pull_request.number} {action}: {pull_request.title}\nBy: {pull_request.user.login}\nBranch: {pull_request.head.ref}\n\n{pull_request.body}" \  
      --skills "github-code-review" \  
      --deliver github_comment  
    
[/code]
### Stripe: платежные события[​](<#stripe-payment-events> "Прямая ссылка на раздел «Stripe: платежные события»")
[code] 
    hermes webhook subscribe stripe-payments \  
      --events "payment_intent.succeeded,payment_intent.payment_failed" \  
      --prompt "Payment {data.object.status}: {data.object.amount} cents from {data.object.receipt_email}" \  
      --deliver telegram \  
      --deliver-chat-id "-100123456789"  
    
[/code]
### CI/CD: уведомления о сборках[​](<#cicd-build-notifications> "Прямая ссылка на раздел «CI/CD: уведомления о сборках»")
[code] 
    hermes webhook subscribe ci-builds \  
      --events "pipeline" \  
      --prompt "Build {object_attributes.status} on {project.name} branch {object_attributes.ref}\nCommit: {commit.message}" \  
      --deliver discord \  
      --deliver-chat-id "1234567890"  
    
[/code]
### Общее оповещение мониторинга[​](<#generic-monitoring-alert> "Прямая ссылка на раздел «Общее оповещение мониторинга»")
[code] 
    hermes webhook subscribe alerts \  
      --prompt "Alert: {alert.name}\nSeverity: {alert.severity}\nMessage: {alert.message}\n\nPlease investigate and suggest remediation." \  
      --deliver origin  
    
[/code]
### Прямая доставка (без агента, нулевая стоимость LLM)[​](<#direct-delivery-no-agent-zero-llm-cost> "Прямая ссылка на раздел «Прямая доставка (без агента, нулевая стоимость LLM)»")
Для сценариев, где вы просто хотите отправить уведомление в чат пользователя — без рассуждений, без цикла агента — добавьте `--deliver-only`. Отрендеренный шаблон `--prompt` становится буквальным телом сообщения и отправляется напрямую в целевой адаптер.
Используйте это для:
  * Внешних push-уведомлений сервисов (вебхуки Supabase/Firebase → Telegram)
  * Оповещений мониторинга, которые должны пересылаться дословно
  * Межагентских сигналов, когда один агент сообщает что-то пользователю другого агента
  * Любых вебхуков, где круглый обход LLM был бы напрасной тратой ресурсов


[code] 
    hermes webhook subscribe antenna-matches \  
      --deliver telegram \  
      --deliver-chat-id "123456789" \  
      --deliver-only \  
      --prompt "🎉 New match: {match.user_name} matched with you!" \  
      --description "Antenna match notifications"  
    
[/code]
POST-запрос возвращает `200 OK` при успешной доставке и `502` при сбое целевого сервиса — так вышестоящие сервисы могут интеллектуально повторять попытки. HMAC-аутентификация, ограничения скорости и идемпотентность по-прежнему применяются.
Требует, чтобы `--deliver` указывал на реальный целевой адаптер (telegram, discord, slack, github_comment и т.д.) — `--deliver log` отклоняется, так как лог-доставка без агента бессмысленна.
## Безопасность[​](<#security> "Прямая ссылка на раздел «Безопасность»")
  * Каждая подписка получает автоматически сгенерированный HMAC-SHA256 секрет (или вы можете указать свой через `--secret`)
  * Вебхук-адаптер проверяет подписи на каждом входящем POST-запросе
  * Статические маршруты из config.yaml не могут быть перезаписаны динамическими подписками
  * Подписки сохраняются в `~/.hermes/webhook_subscriptions.json`


## Как это работает[​](<#how-it-works> "Прямая ссылка на раздел «Как это работает»")
  1. `hermes webhook subscribe` записывает данные в `~/.hermes/webhook_subscriptions.json`
  2. Вебхук-адаптер «на лету» перезагружает этот файл при каждом входящем запросе (проверка mtime, минимальные накладные расходы)
  3. Когда приходит POST, совпадающий с маршрутом, адаптер форматирует промпт и запускает выполнение агента
  4. Ответ агента доставляется в настроенный целевой канал (Telegram, Discord, комментарий GitHub и т.д.)


## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на раздел «Устранение неполадок»")
Если вебхуки не работают:
  1. **Запущен ли шлюз?** Проверьте с помощью `systemctl --user status hermes-gateway` или `ps aux | grep gateway`
  2. **Слушает ли вебхук-сервер?** `curl http://localhost:8644/health` должен возвращать `{"status": "ok"}`
  3. **Проверьте логи шлюза:** `grep webhook ~/.hermes/logs/gateway.log | tail -20`
  4. **Несовпадение подписи?** Убедитесь, что секрет в вашем сервисе совпадает с тем, что выводит `hermes webhook list`. GitHub отправляет `X-Hub-Signature-256`, GitLab отправляет `X-Gitlab-Token`.
  5. **Фаервол/NAT?** URL вебхука должен быть доступен из сервиса. Для локальной разработки используйте туннель (ngrok, cloudflared).
  6. **Неверный тип события?** Проверьте, что фильтр `--events` соответствует тому, что отправляет сервис. Используйте `hermes webhook test <name>`, чтобы проверить, работает ли маршрут.


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Настройка (обязательно сначала)](<#setup-required-first>)
    * [Вариант 1: Мастер настройки](<#option-1-setup-wizard>)
    * [Вариант 2: Ручная настройка](<#option-2-manual-config>)
    * [Вариант 3: Переменные окружения](<#option-3-environment-variables>)
  * [Команды](<#commands>)
    * [Создать подписку](<#create-a-subscription>)
    * [Список подписок](<#list-subscriptions>)
    * [Удалить подписку](<#remove-a-subscription>)
    * [Протестировать подписку](<#test-a-subscription>)
  * [Шаблоны промптов](<#prompt-templates>)
  * [Типовые сценарии](<#common-patterns>)
    * [GitHub: новые issues](<#github-new-issues>)
    * [GitHub: ревью PR](<#github-pr-reviews>)
    * [Stripe: платежные события](<#stripe-payment-events>)
    * [CI/CD: уведомления о сборках](<#cicd-build-notifications>)
    * [Общее оповещение мониторинга](<#generic-monitoring-alert>)
    * [Прямая доставка (без агента, нулевая стоимость LLM)](<#direct-delivery-no-agent-zero-llm-cost>)
  * [Безопасность](<#security>)
  * [Как это работает](<#how-it-works>)
  * [Устранение неполадок](<#troubleshooting>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/devops/devops-webhook-subscriptions -->
