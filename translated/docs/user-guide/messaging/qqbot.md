On this page
Подключите Hermes к QQ через **Official QQ Bot API (v2)** — с поддержкой личных (C2C), групповых @-упоминаний, гильдий и прямых сообщений с транскрипцией голоса.
## Overview[​](<#overview> "Прямая ссылка на раздел \"Обзор\"")
Адаптер QQ Bot использует [Official QQ Bot API](<https://bot.q.qq.com/wiki/develop/api-v2/>) для:
  * Получения сообщений через постоянное **WebSocket**-соединение с QQ Gateway
  * Отправки текстовых и markdown-ответов через **REST API**
  * Загрузки и обработки изображений, голосовых сообщений и вложенных файлов
  * Транскрипции голосовых сообщений с помощью встроенного ASR от Tencent или настраиваемого STT-провайдера

## Prerequisites[​](<#prerequisites> "Прямая ссылка на раздел \"Предварительные требования\"")
  1. **Приложение QQ Bot** — Зарегистрируйтесь на [q.qq.com](<https://q.qq.com>):
     * Создайте новое приложение и запишите **App ID** и **App Secret**
     * Включите необходимые намерения (intents): C2C-сообщения, групповые @-сообщения, сообщения гильдий
     * Настройте бота в режиме песочницы для тестирования или опубликуйте для продакшена
  2. **Зависимости** — Адаптеру требуются `aiohttp` и `httpx`:
```
pip install aiohttp httpx
```

## Configuration[​](<#configuration> "Прямая ссылка на раздел \"Настройка\"")
### Interactive setup[​](<#interactive-setup> "Прямая ссылка на раздел \"Интерактивная настройка\"")
```
hermes gateway setup
```
Выберите **QQ Bot** из списка платформ и следуйте инструкциям.
### Manual configuration[​](<#manual-configuration> "Прямая ссылка на раздел \"Ручная настройка\"")
Установите необходимые переменные окружения в `~/.hermes/.env`:
```
QQ_APP_ID=your-app-id
QQ_CLIENT_SECRET=your-app-secret
```
## Environment Variables[​](<#environment-variables> "Прямая ссылка на раздел \"Переменные окружения\"")
| Переменная | Описание | По умолчанию |
|---|---|---|
|`QQ_APP_ID`| App ID бота QQ (обязательно)| —  |
|`QQ_CLIENT_SECRET`| App Secret бота QQ (обязательно)| —  |
|`QQBOT_HOME_CHANNEL`| OpenID для доставки cron-уведомлений| —  |
|`QQBOT_HOME_CHANNEL_NAME`| Отображаемое имя домашнего канала| `Home`  |
|`QQ_ALLOWED_USERS`| OpenID пользователей через запятую для доступа в ЛС| открыто (все пользователи)  |
|`QQ_GROUP_ALLOWED_USERS`| OpenID групп через запятую для доступа в группы| —  |
|`QQ_ALLOW_ALL_USERS`| Установите `true`, чтобы разрешить все ЛС| `false`  |
|`QQ_PORTAL_HOST`| Переопределить хост портала QQ (установите `sandbox.q.qq.com` для маршрутизации через песочницу)| `q.qq.com`  |
|`QQ_STT_API_KEY`| API-ключ для STT-провайдера| —  |
|`QQ_STT_BASE_URL`| Базовый URL для STT-провайдера| `https://open.bigmodel.cn/api/coding/paas/v4`  |
|`QQ_STT_MODEL`| Название STT-модели| `glm-asr`  |
## Advanced Configuration[​](<#advanced-configuration> "Прямая ссылка на раздел \"Расширенная настройка\"")
Для тонкой настройки добавьте параметры платформы в `~/.hermes/config.yaml`:
```yaml
platforms:
  qq:
    enabled: true
    extra:
      app_id: "your-app-id"
      client_secret: "your-secret"
      markdown_support: true       # включить QQ markdown (msg_type 2). Только в конфиге; переменной окружения нет.
      dm_policy: "open"          # open | allowlist | disabled
      allow_from:
        - "user_openid_1"
      group_policy: "open"       # open | allowlist | disabled
      group_allow_from:
        - "group_openid_1"
      stt:
        provider: "zai"          # zai (GLM-ASR), openai (Whisper) и т.д.
        baseUrl: "https://open.bigmodel.cn/api/coding/paas/v4"
        apiKey: "your-stt-key"
        model: "glm-asr"
```
## Voice Messages (STT)[​](<#voice-messages-stt> "Прямая ссылка на раздел \"Голосовые сообщения (STT)\"")
Транскрипция голоса работает в два этапа:
  1. **Встроенный ASR QQ** (бесплатно, всегда пробуется первым) — QQ предоставляет `asr_refer_text` в голосовых вложениях, используя собственное распознавание речи Tencent
  2. **Настроенный STT-провайдер** (запасной вариант) — Если ASR QQ не возвращает текст, адаптер вызывает STT API, совместимый с OpenAI:
     * **Zhipu/GLM (zai)** : Провайдер по умолчанию, использует модель `glm-asr`
     * **OpenAI Whisper** : Установите `QQ_STT_BASE_URL` и `QQ_STT_MODEL`
     * Любой STT-эндпоинт, совместимый с OpenAI

## Troubleshooting[​](<#troubleshooting> "Прямая ссылка на раздел \"Устранение неполадок\"")
### Bot disconnects immediately (quick disconnect)[​](<#bot-disconnects-immediately-quick-disconnect> "Прямая ссылка на раздел \"Бот сразу отключается (быстрое отключение)\"")
Обычно это означает:
  * **Неверный App ID / Secret** — Перепроверьте учётные данные на q.qq.com
  * **Отсутствуют разрешения** — Убедитесь, что у бота включены необходимые намерения (intents)
  * **Бот только в песочнице** — Если бот в режиме песочницы, он может получать сообщения только из тестового канала песочницы QQ

### Voice messages not transcribed[​](<#voice-messages-not-transcribed> "Прямая ссылка на раздел \"Голосовые сообщения не транскрибируются\"")
  1. Проверьте, присутствует ли встроенный `asr_refer_text` QQ в данных вложения
  2. При использовании пользовательского STT-провайдера проверьте, правильно ли установлен `QQ_STT_API_KEY`
  3. Проверьте журналы шлюза на наличие сообщений об ошибках STT

### Messages not delivered[​](<#messages-not-delivered> "Прямая ссылка на раздел \"Сообщения не доставляются\"")
  * Убедитесь, что **намерения (intents)** бота включены на q.qq.com
  * Проверьте `QQ_ALLOWED_USERS`, если доступ к ЛС ограничен
  * Для групповых сообщений убедитесь, что бот **упомянут через @** (групповая политика может требовать внесения в белый список)
  * Проверьте `QQBOT_HOME_CHANNEL` для доставки cron-уведомлений

### Connection errors[​](<#connection-errors> "Прямая ссылка на раздел \"Ошибки подключения\"")
  * Убедитесь, что `aiohttp` и `httpx` установлены: `pip install aiohttp httpx`
  * Проверьте сетевое подключение к `api.sgroup.qq.com` и WebSocket-шлюзу
  * Просмотрите журналы шлюза для получения подробных сообщений об ошибках и информации о переподключении

  * [Обзор](<#overview>)
  * [Предварительные требования](<#prerequisites>)
  * [Настройка](<#configuration>)
    * [Интерактивная настройка](<#interactive-setup>)
    * [Ручная настройка](<#manual-configuration>)
  * [Переменные окружения](<#environment-variables>)
  * [Расширенная настройка](<#advanced-configuration>)
  * [Голосовые сообщения (STT)](<#voice-messages-stt>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Бот сразу отключается (быстрое отключение)](<#bot-disconnects-immediately-quick-disconnect>)
    * [Голосовые сообщения не транскрибируются](<#voice-messages-not-transcribed>)
    * [Сообщения не доставляются](<#messages-not-delivered>)
    * [Ошибки подключения](<#connection-errors>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot -->
