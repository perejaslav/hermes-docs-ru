On this page
Подключите Hermes Agent к Microsoft Teams в качестве бота. В отличие от Socket Mode в Slack, Teams доставляет сообщения, вызывая **публичный HTTPS вебхук**, поэтому вашему экземпляру требуется публично доступная конечная точка — либо dev-туннель (локальная разработка), либо реальный домен (продакшн).
## Как бот отвечает[​](<#how-the-bot-responds> "Прямая ссылка на раздел «Как бот отвечает»")
Контекст| Поведение  
---|---  
**Личный чат (ЛС)**|  Бот отвечает на каждое сообщение. Упоминание @ не требуется.  
**Групповой чат**|  Бот отвечает только при упоминании через @.  
**Канал**|  Бот отвечает только при упоминании через @.  
Teams передаёт @упоминания как обычные сообщения с тегами `<at>ИмяБота</at>`, которые Hermes автоматически удаляет перед обработкой.
* * *
## Шаг 1: Установите Teams CLI[​](<#step-1-install-the-teams-cli> "Прямая ссылка на раздел «Шаг 1: Установите Teams CLI»")
Пакет `@microsoft/teams.cli` автоматизирует регистрацию бота — портал Azure не требуется.
[code] 
    npm install -g @microsoft/teams.cli@preview  
    teams login  
    
[/code]
Чтобы проверить свой логин и узнать собственный AAD object ID (понадобится для `TEAMS_ALLOWED_USERS`):
[code] 
    teams status --verbose  
    
[/code]
* * *
## Шаг 2: Откройте порт вебхука[​](<#step-2-expose-the-webhook-port> "Прямая ссылка на раздел «Шаг 2: Откройте порт вебхука»")
Teams не может доставлять сообщения на `localhost`. Для локальной разработки используйте любой инструмент туннелирования, чтобы получить публичный HTTPS URL. Порт по умолчанию — `3978` — измените его с помощью `TEAMS_PORT` при необходимости.
[code] 
    # devtunnel (Microsoft)  
    devtunnel create hermes-bot --allow-anonymous  
    devtunnel port create hermes-bot -p 3978 --protocol https  # замените 3978 на TEAMS_PORT, если изменён  
    devtunnel host hermes-bot  
      
    # ngrok  
    ngrok http 3978  # замените 3978 на TEAMS_PORT, если изменён  
      
    # cloudflared  
    cloudflared tunnel --url http://localhost:3978  # замените 3978 на TEAMS_PORT, если изменён  
    
[/code]
Скопируйте `https://` URL из вывода — он понадобится на следующем шаге. Оставьте туннель работающим на время разработки.
Для продакшна укажите конечную точку бота на вашем публичном домене (см. [Развёртывание в продакшн](<#production-deployment>)).
* * *
## Шаг 3: Создайте бота[​](<#step-3-create-the-bot> "Прямая ссылка на раздел «Шаг 3: Создайте бота»")
[code] 
    teams app create \  
      --name "Hermes" \  
      --endpoint "https://<ваш-url-туннеля>/api/messages"  
    
[/code]
CLI выводит ваши `CLIENT_ID`, `CLIENT_SECRET` и `TENANT_ID`, а также ссылку для установки (шаг 6). Сохраните client secret — он больше не будет показан.
* * *
## Шаг 4: Настройте переменные окружения[​](<#step-4-configure-environment-variables> "Прямая ссылка на раздел «Шаг 4: Настройте переменные окружения»")
Добавьте в `~/.hermes/.env`:
[code] 
    # Обязательные  
    TEAMS_CLIENT_ID=<ваш-client-id>  
    TEAMS_CLIENT_SECRET=<ваш-client-secret>  
    TEAMS_TENANT_ID=<ваш-tenant-id>  
      
    # Ограничение доступа определёнными пользователями (рекомендуется)  
    # Используйте AAD object IDs из `teams status --verbose`  
    TEAMS_ALLOWED_USERS=<ваш-aad-object-id>  
    
[/code]
* * *
## Шаг 5: Запустите шлюз[​](<#step-5-start-the-gateway> "Прямая ссылка на раздел «Шаг 5: Запустите шлюз»")
[code] 
    HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d gateway  
    
[/code]
Это запускает шлюз. Порт вебхука по умолчанию — `3978` (переопределяется через `TEAMS_PORT`). Проверьте, что он работает:
[code] 
    curl http://localhost:3978/health   # должно вернуть: ok  
    docker logs -f hermes  
    
[/code]
Ищите в логах:
[code] 
    [teams] Webhook server listening on 0.0.0.0:3978/api/messages  
    
[/code]
* * *
## Шаг 6: Установите приложение в Teams[​](<#step-6-install-the-app-in-teams> "Прямая ссылка на раздел «Шаг 6: Установите приложение в Teams»")
[code] 
    teams app get <teamsAppId> --install-link  
    
[/code]
Откройте полученную ссылку в браузере — она открывается непосредственно в клиенте Teams. После установки отправьте боту личное сообщение — он готов к работе.
* * *
## Справочник по настройке[​](<#configuration-reference> "Прямая ссылка на раздел «Справочник по настройке»")
### Переменные окружения[​](<#environment-variables> "Прямая ссылка на раздел «Переменные окружения»")
Переменная| Описание  
---|---  
`TEAMS_CLIENT_ID`| ID приложения (клиента) Azure AD  
`TEAMS_CLIENT_SECRET`| Секрет клиента Azure AD  
`TEAMS_TENANT_ID`| ID тенанта Azure AD  
`TEAMS_ALLOWED_USERS`| Разделённые запятыми AAD object IDs пользователей, которым разрешено использовать бота  
`TEAMS_ALLOW_ALL_USERS`| Установите `true`, чтобы отключить белый список и разрешить всем  
`TEAMS_HOME_CHANNEL`| ID беседы для доставки cron/проактивных сообщений  
`TEAMS_HOME_CHANNEL_NAME`| Отображаемое имя домашнего канала  
`TEAMS_PORT`| Порт вебхука (по умолчанию: `3978`)  
### config.yaml[​](<#configyaml> "Прямая ссылка на раздел «config.yaml»")
В качестве альтернативы настройте через `~/.hermes/config.yaml`:
[code] 
    platforms:  
      teams:  
        enabled: true  
        extra:  
          client_id: "your-client-id"  
          client_secret: "your-secret"  
          tenant_id: "your-tenant-id"  
          port: 3978  
    
[/code]
* * *
## Возможности[​](<#features> "Прямая ссылка на раздел «Возможности»")
### Интерактивные карточки подтверждения[​](<#interactive-approval-cards> "Прямая ссылка на раздел «Интерактивные карточки подтверждения»")
Когда агенту нужно выполнить потенциально опасную команду, он отправляет адаптивную карточку (Adaptive Card) с четырьмя кнопками вместо того, чтобы просить вас ввести `/approve`:
  * **Allow Once** — подтвердить эту конкретную команду
  * **Allow Session** — подтвердить этот шаблон на оставшуюся часть сессии
  * **Always Allow** — навсегда подтвердить этот шаблон
  * **Deny** — отклонить команду


Нажатие на кнопку разрешает действие прямо в карточке и заменяет её на информацию о принятом решении.
* * *
## Развёртывание в продакшн[​](<#production-deployment> "Прямая ссылка на раздел «Развёртывание в продакшн»")
Для постоянного сервера пропустите devtunnel и зарегистрируйте бота с публичным HTTPS-адресом вашего сервера:
[code] 
    teams app create \  
      --name "Hermes" \  
      --endpoint "https://ваш-домен.com/api/messages"  
    
[/code]
Если бот уже создан и нужно лишь обновить конечную точку:
[code] 
    teams app update --id <teamsAppId> --endpoint "https://ваш-домен.com/api/messages"  
    
[/code]
Убедитесь, что настроенный порт (`TEAMS_PORT`, по умолчанию `3978`) доступен из интернета, и что ваш TLS-сертификат действителен — Teams отклоняет самоподписанные сертификаты.
* * *
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на раздел «Устранение неполадок»")
Проблема| Решение  
---|---  
Эндпоинт `/health` работает, но бот не отвечает| Проверьте, что ваш туннель всё ещё запущен, и что конечная точка обмена сообщениями бота совпадает с URL туннеля  
`KeyError: 'teams'` в логах| Перезапустите контейнер — эта проблема исправлена в текущей версии  
Бот отвечает ошибками аутентификации| Проверьте, что `TEAMS_CLIENT_ID`, `TEAMS_CLIENT_SECRET` и `TEAMS_TENANT_ID` указаны верно  
`No inference provider configured`| Проверьте, что `ANTHROPIC_API_KEY` (или ключ другого провайдера) указан в `~/.hermes/.env`  
Бот получает сообщения, но игнорирует их| Возможно, ваш AAD object ID отсутствует в `TEAMS_ALLOWED_USERS`. Выполните `teams status --verbose`, чтобы узнать его  
URL туннеля меняется при перезапуске| URL devtunnel постоянны, если используется именованный туннель (`devtunnel create hermes-bot`). ngrok и cloudflared генерируют новый URL при каждом запуске, если у вас нет платного плана — обновите конечную точку бота через `teams app update` при изменении URL  
Teams показывает «Этот бот не отвечает»| Вебхук вернул ошибку. Проверьте `docker logs hermes` на наличие traceback  
`[teams] Failed to connect` в логах| SDK не смог аутентифицироваться. Перепроверьте свои учётные данные и убедитесь, что ID тенанта соответствует учётной записи, использованной в `teams login`  
* * *
## Безопасность[​](<#security> "Прямая ссылка на раздел «Безопасность»")
warning
**Всегда указывайте`TEAMS_ALLOWED_USERS`** с AAD object IDs авторизованных пользователей. Без этого любой, кто найдёт или установит вашего бота, сможет с ним взаимодействовать.
Относитесь к `TEAMS_CLIENT_SECRET` как к паролю — периодически меняйте его через портал Azure или Teams CLI.
  * Храните учётные данные в `~/.hermes/.env` с правами `600` (`chmod 600 ~/.hermes/.env`)
  * Бот принимает сообщения только от пользователей из `TEAMS_ALLOWED_USERS`; неавторизованные сообщения молча игнорируются
  * Ваша публичная конечная точка (`/api/messages`) аутентифицируется через Teams Bot Framework — запросы без действительных JWT отклоняются


  * [Как бот отвечает](<#how-the-bot-responds>)
  * [Шаг 1: Установите Teams CLI](<#step-1-install-the-teams-cli>)
  * [Шаг 2: Откройте порт вебхука](<#step-2-expose-the-webhook-port>)
  * [Шаг 3: Создайте бота](<#step-3-create-the-bot>)
  * [Шаг 4: Настройте переменные окружения](<#step-4-configure-environment-variables>)
  * [Шаг 5: Запустите шлюз](<#step-5-start-the-gateway>)
  * [Шаг 6: Установите приложение в Teams](<#step-6-install-the-app-in-teams>)
  * [Справочник по настройке](<#configuration-reference>)
    * [Переменные окружения](<#environment-variables>)
    * [config.yaml](<#configyaml>)
  * [Возможности](<#features>)
    * [Интерактивные карточки подтверждения](<#interactive-approval-cards>)
  * [Развёртывание в продакшн](<#production-deployment>)
  * [Устранение неполадок](<#troubleshooting>)
  * [Безопасность](<#security>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams -->
