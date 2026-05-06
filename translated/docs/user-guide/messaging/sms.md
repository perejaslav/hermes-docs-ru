On this page
Hermes подключается к SMS через API [Twilio](<https://www.twilio.com/>). Люди пишут на ваш номер Twilio и получают ответы от AI — тот же диалоговый опыт, что и в Telegram или Discord, но через обычные текстовые сообщения.
Shared Credentials
SMS-шлюз использует те же учётные данные, что и опциональный [telephony skill](</docs/reference/skills-catalog>). Если вы уже настроили Twilio для голосовых звонков или отдельных SMS, шлюз работает с теми же `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` и `TWILIO_PHONE_NUMBER`.
* * *
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **Аккаунт Twilio** — [Зарегистрируйтесь на twilio.com](<https://www.twilio.com/try-twilio>) (доступна бесплатная пробная версия)
  * **Номер телефона Twilio** с поддержкой SMS
  * **Общедоступный сервер** — Twilio отправляет вебхуки на ваш сервер при получении SMS
  * **aiohttp** — `pip install 'hermes-agent[sms]'`


* * *
## Step 1: Get Your Twilio Credentials[​](<#step-1-get-your-twilio-credentials> "Direct link to Step 1: Get Your Twilio Credentials")
  1. Перейдите в [Twilio Console](<https://console.twilio.com/>)
  2. Скопируйте **Account SID** и **Auth Token** с панели управления
  3. Перейдите в **Phone Numbers → Manage → Active Numbers** — запишите ваш номер телефона в формате E.164 (например, `+15551234567`)


* * *
## Step 2: Configure Hermes[​](<#step-2-configure-hermes> "Direct link to Step 2: Configure Hermes")
### Interactive setup (recommended)[​](<#interactive-setup-recommended> "Direct link to Interactive setup \\(recommended\\)")
[code] 
    hermes gateway setup  
    
[/code]
Выберите **SMS (Twilio)** из списка платформ. Мастер запросит ваши учётные данные.
### Manual setup[​](<#manual-setup> "Direct link to Manual setup")
Добавьте в `~/.hermes/.env`:
[code] 
    TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
    TWILIO_AUTH_TOKEN=your_auth_token_here  
    TWILIO_PHONE_NUMBER=+15551234567  
      
    # Security: restrict to specific phone numbers (recommended)  
    SMS_ALLOWED_USERS=+15559876543,+15551112222  
      
    # Optional: set a home channel for cron job delivery  
    SMS_HOME_CHANNEL=+15559876543  
    
[/code]
* * *
## Step 3: Configure Twilio Webhook[​](<#step-3-configure-twilio-webhook> "Direct link to Step 3: Configure Twilio Webhook")
Twilio должен знать, куда отправлять входящие сообщения. В [Twilio Console](<https://console.twilio.com/>):
  1. Перейдите в **Phone Numbers → Manage → Active Numbers**
  2. Нажмите на ваш номер телефона
  3. В разделе **Messaging → A MESSAGE COMES IN** укажите:
     * **Webhook**: `https://your-server:8080/webhooks/twilio`
     * **HTTP Method**: `POST`


Exposing Your Webhook
Если вы запускаете Hermes локально, используйте туннель для публичного доступа к вебхуку:
[code]
    # Using cloudflared  
    cloudflared tunnel --url http://localhost:8080  
      
    # Using ngrok  
    ngrok http 8080  
    
[/code]
Укажите полученный публичный URL в качестве вебхука в Twilio.
**Установите `SMS_WEBHOOK_URL` в тот же URL, который вы настроили в Twilio.** Это требуется для проверки подписи Twilio — адаптер откажется запускаться без него:
[code] 
    # Must match the webhook URL in your Twilio Console  
    SMS_WEBHOOK_URL=https://your-server:8080/webhooks/twilio  
    
[/code]
Порт вебхука по умолчанию `8080`. Переопределить можно так:
[code] 
    SMS_WEBHOOK_PORT=3000  
    
[/code]
* * *
## Step 4: Start the Gateway[​](<#step-4-start-the-gateway> "Direct link to Step 4: Start the Gateway")
[code] 
    hermes gateway  
    
[/code]
Вы должны увидеть:
[code] 
    [sms] Twilio webhook server listening on 0.0.0.0:8080, from: +1555***4567  
    
[/code]
Если вы видите `Refusing to start: SMS_WEBHOOK_URL is required`, установите `SMS_WEBHOOK_URL` в публичный URL, настроенный в вашей консоли Twilio (см. Шаг 3).
Отправьте сообщение на ваш номер Twilio — Hermes ответит через SMS.
* * *
## Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
Variable| Required| Description  
---|---|---  
`TWILIO_ACCOUNT_SID`| Да| Account SID Twilio (начинается с `AC`)  
`TWILIO_AUTH_TOKEN`| Да| Auth Token Twilio (также используется для проверки подписи вебхука)  
`TWILIO_PHONE_NUMBER`| Да| Номер телефона Twilio (формат E.164)  
`SMS_WEBHOOK_URL`| Да| Публичный URL для проверки подписи Twilio — должен совпадать с URL вебхука в консоли Twilio  
`SMS_WEBHOOK_PORT`| Нет| Порт вебхука (по умолчанию: `8080`)  
`SMS_WEBHOOK_HOST`| Нет| Адрес привязки вебхука (по умолчанию: `0.0.0.0`)  
`SMS_INSECURE_NO_SIGNATURE`| Нет| Установите `true` для отключения проверки подписи (только локальная разработка — **не для продакшена**)  
`SMS_ALLOWED_USERS`| Нет| Список номеров в формате E.164 через запятую, которым разрешено общаться  
`SMS_ALLOW_ALL_USERS`| Нет| Установите `true`, чтобы разрешить всем (не рекомендуется)  
`SMS_HOME_CHANNEL`| Нет| Номер телефона для доставки cron-задач и уведомлений  
`SMS_HOME_CHANNEL_NAME`| Нет| Отображаемое имя домашнего канала (по умолчанию: `Home`)  
* * *
## SMS-Specific Behavior[​](<#sms-specific-behavior> "Direct link to SMS-Specific Behavior")
  * **Только обычный текст** — Markdown автоматически удаляется, так как SMS отображает его как буквальные символы
  * **Лимит 1600 символов** — Длинные ответы разбиваются на несколько сообщений по естественным границам (сначала переносы строк, затем пробелы)
  * **Защита от эха** — Сообщения с вашего собственного номера Twilio игнорируются для предотвращения зацикливания
  * **Редактирование номеров телефонов** — Номера телефонов скрываются в логах для конфиденциальности


* * *
## Security[​](<#security> "Direct link to Security")
### Webhook signature validation[​](<#webhook-signature-validation> "Direct link to Webhook signature validation")
Hermes проверяет, что входящие вебхуки действительно исходят от Twilio, верифицируя заголовок `X-Twilio-Signature` (HMAC-SHA1). Это предотвращает внедрение поддельных сообщений злоумышленниками.
**`SMS_WEBHOOK_URL` обязателен.** Установите его в публичный URL, настроенный в вашей консоли Twilio. Адаптер откажется запускаться без него.
Для локальной разработки без публичного URL можно отключить проверку:
[code] 
    # Local dev only — NOT for production  
    SMS_INSECURE_NO_SIGNATURE=true  
    
[/code]
### User allowlists[​](<#user-allowlists> "Direct link to User allowlists")
**Шлюз по умолчанию запрещает всех пользователей.** Настройте белый список:
[code] 
    # Recommended: restrict to specific phone numbers  
    SMS_ALLOWED_USERS=+15559876543,+15551112222  
      
    # Or allow all (NOT recommended for bots with terminal access)  
    SMS_ALLOW_ALL_USERS=true  
    
[/code]
warning
SMS не имеет встроенного шифрования. Не используйте SMS для чувствительных операций, если вы не понимаете последствия для безопасности. Для чувствительных сценариев используйте Signal или Telegram.
* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### Messages not arriving[​](<#messages-not-arriving> "Direct link to Messages not arriving")
  1. Проверьте, что URL вебхука в Twilio корректен и общедоступен
  2. Проверьте правильность `TWILIO_ACCOUNT_SID` и `TWILIO_AUTH_TOKEN`
  3. Проверьте Twilio Console → **Monitor → Logs → Messaging** на наличие ошибок доставки
  4. Убедитесь, что ваш номер есть в `SMS_ALLOWED_USERS` (или установлен `SMS_ALLOW_ALL_USERS=true`)


### Replies not sending[​](<#replies-not-sending> "Direct link to Replies not sending")
  1. Проверьте, что `TWILIO_PHONE_NUMBER` указан корректно (формат E.164 с `+`)
  2. Убедитесь, что ваш аккаунт Twilio имеет номера с поддержкой SMS
  3. Проверьте логи шлюза Hermes на наличие ошибок API Twilio


### Webhook port conflicts[​](<#webhook-port-conflicts> "Direct link to Webhook port conflicts")
Если порт 8080 уже занят, измените его:
[code] 
    SMS_WEBHOOK_PORT=3001  
    
[/code]
Обновите URL вебхука в консоли Twilio соответственно.
  * [Prerequisites](<#prerequisites>)
  * [Step 1: Get Your Twilio Credentials](<#step-1-get-your-twilio-credentials>)
  * [Step 2: Configure Hermes](<#step-2-configure-hermes>)
    * [Interactive setup (recommended)](<#interactive-setup-recommended>)
    * [Manual setup](<#manual-setup>)
  * [Step 3: Configure Twilio Webhook](<#step-3-configure-twilio-webhook>)
  * [Step 4: Start the Gateway](<#step-4-start-the-gateway>)
  * [Environment Variables](<#environment-variables>)
  * [SMS-Specific Behavior](<#sms-specific-behavior>)
  * [Security](<#security>)
    * [Webhook signature validation](<#webhook-signature-validation>)
    * [User allowlists](<#user-allowlists>)
  * [Troubleshooting](<#troubleshooting>)
    * [Messages not arriving](<#messages-not-arriving>)
    * [Replies not sending](<#replies-not-sending>)
    * [Webhook port conflicts](<#webhook-port-conflicts>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms -->
