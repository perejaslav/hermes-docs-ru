На этой странице

Подключите Hermes к Apple iMessage через [BlueBubbles](<https://bluebubbles.app/>) — бесплатный сервер с открытым исходным кодом для macOS, который связывает iMessage с любым устройством.

## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")

- **Mac** (постоянно включённый) с запущенным [BlueBubbles Server](<https://bluebubbles.app/>)
- Apple ID, вошедший в Messages.app на этом Mac
- BlueBubbles Server v1.0.0+ (вебхуки требуют этой версии)
- Сетевое соединение между Hermes и сервером BlueBubbles

## Настройка[​](<#setup> "Прямая ссылка на Настройка")

### 1\. Установите BlueBubbles Server[​](<#1-install-bluebubbles-server> "Прямая ссылка на 1. Установите BlueBubbles Server")

Скачайте и установите с [bluebubbles.app](<https://bluebubbles.app/>). Пройдите мастер настройки — войдите с вашим Apple ID и настройте способ подключения (локальная сеть, Ngrok, Cloudflare или Dynamic DNS).

### 2\. Получите URL сервера и пароль[​](<#2-get-your-server-url-and-password> "Прямая ссылка на 2. Получите URL сервера и пароль")

В BlueBubbles Server → **Settings → API** запишите:
- **Server URL** (например, `http://192.168.1.10:1234`)
- **Server Password**

### 3\. Настройте Hermes[​](<#3-configure-hermes> "Прямая ссылка на 3. Настройте Hermes")

Запустите мастер настройки:

[code]
    hermes gateway setup
    
[/code]

Выберите **BlueBubbles (iMessage)** и введите URL сервера и пароль.

Или укажите переменные окружения напрямую в `~/.hermes/.env`:

[code]
    BLUEBUBBLES_SERVER_URL=http://192.168.1.10:1234
    BLUEBUBBLES_PASSWORD=your-server-password
    
[/code]

### 4\. Авторизуйте пользователей[​](<#4-authorize-users> "Прямая ссылка на 4. Авторизуйте пользователей")

Выберите один из способов:

**Сопряжение по ЛС (рекомендуется):** Когда кто-то пишет вам в iMessage, Hermes автоматически отправляет им код сопряжения. Подтвердите его командой:

[code]
    hermes pairing approve bluebubbles <КОД>
    
[/code]

Используйте `hermes pairing list` для просмотра ожидающих кодов и подтверждённых пользователей.

**Предварительная авторизация конкретных пользователей** (в `~/.hermes/.env`):

[code]
    BLUEBUBBLES_ALLOWED_USERS=user@icloud.com,+15551234567
    
[/code]

**Открытый доступ** (в `~/.hermes/.env`):

[code]
    BLUEBUBBLES_ALLOW_ALL_USERS=true
    
[/code]

### 5\. Запустите шлюз[​](<#5-start-the-gateway> "Прямая ссылка на 5. Запустите шлюз")

[code]
    hermes gateway run
    
[/code]

Hermes подключится к вашему серверу BlueBubbles, зарегистрирует вебхук и начнёт прослушивание сообщений iMessage.

## Как это работает[​](<#how-it-works> "Прямая ссылка на Как это работает")

[code]
    iMessage → Messages.app → BlueBubbles Server → Webhook → Hermes
    Hermes → BlueBubbles REST API → Messages.app → iMessage
    
[/code]

- **Входящие:** BlueBubbles отправляет события вебхука локальному слушателю при поступлении новых сообщений. Никакого опроса — мгновенная доставка.
- **Исходящие:** Hermes отправляет сообщения через REST API BlueBubbles.
- **Медиа:** Изображения, голосовые сообщения, видео и документы поддерживаются в обоих направлениях. Входящие вложения загружаются и кэшируются локально для обработки агентом.

## Переменные окружения[​](<#environment-variables> "Прямая ссылка на Переменные окружения")

| Переменная | Обязательно | По умолчанию | Описание |
|---|---|---|---|
| `BLUEBUBBLES_SERVER_URL` | Да | — | URL сервера BlueBubbles |
| `BLUEBUBBLES_PASSWORD` | Да | — | Пароль сервера |
| `BLUEBUBBLES_WEBHOOK_HOST` | Нет | `127.0.0.1` | Адрес привязки слушателя вебхука |
| `BLUEBUBBLES_WEBHOOK_PORT` | Нет | `8645` | Порт слушателя вебхука |
| `BLUEBUBBLES_WEBHOOK_PATH` | Нет | `/bluebubbles-webhook` | Путь URL вебхука |
| `BLUEBUBBLES_HOME_CHANNEL` | Нет | — | Телефон/email для доставки cron |
| `BLUEBUBBLES_ALLOWED_USERS` | Нет | — | Авторизованные пользователи через запятую |
| `BLUEBUBBLES_ALLOW_ALL_USERS` | Нет | `false` | Разрешить всех пользователей |

Автоматическая отметка сообщений как прочитанных управляется ключом `send_read_receipts` в разделе `platforms.bluebubbles.extra` в `~/.hermes/config.yaml` (по умолчанию: `true`). Соответствующей переменной окружения нет.

## Возможности[​](<#features> "Прямая ссылка на Возможности")

### Текстовые сообщения[​](<#text-messaging> "Прямая ссылка на Текстовые сообщения")

Отправляйте и получайте iMessages. Markdown автоматически удаляется для чистой доставки в виде простого текста.

### Медиафайлы[​](<#rich-media> "Прямая ссылка на Медиафайлы")

- **Изображения:** Фотографии отображаются нативно в разговоре iMessage
- **Голосовые сообщения:** Аудиофайлы отправляются как голосовые сообщения iMessage
- **Видео:** Видеовложения
- **Документы:** Файлы отправляются как вложения iMessage

### Реакции Tapback[​](<#tapback-reactions> "Прямая ссылка на Реакции Tapback")

Реакции: люблю, нравится, не нравится, смех, подчёркивание и вопрос. Требуется [вспомогательный плагин Private API](<https://docs.bluebubbles.app/helper-bundle/installation>) BlueBubbles.

### Индикаторы печати[​](<#typing-indicators> "Прямая ссылка на Индикаторы печати")

Показывает «печатает...» в разговоре iMessage, пока агент обрабатывает ответ. Требуется Private API.

### Уведомления о прочтении[​](<#read-receipts> "Прямая ссылка на Уведомления о прочтении")

Автоматически помечает сообщения как прочитанные после обработки. Требуется Private API.

### Адресация чатов[​](<#chat-addressing> "Прямая ссылка на Адресация чатов")

Вы можете адресовать чаты по email или номеру телефона — Hermes автоматически преобразует их в GUID чата BlueBubbles. Нет необходимости использовать сырой формат GUID.

## Private API[​](<#private-api> "Прямая ссылка на Private API")

Некоторые функции требуют [вспомогательного плагина Private API](<https://docs.bluebubbles.app/helper-bundle/installation>) BlueBubbles:

- Реакции Tapback
- Индикаторы печати
- Уведомления о прочтении
- Создание новых чатов по адресу

Без Private API базовая отправка текстовых сообщений и медиафайлов продолжает работать.

## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")

### «Не удаётся подключиться к серверу»[​](<#cannot-reach-server> "Прямая ссылка на «Не удаётся подключиться к серверу»")

- Убедитесь, что URL сервера указан правильно и Mac включён
- Проверьте, запущен ли BlueBubbles Server
- Обеспечьте сетевое соединение (фаервол, проброс портов)

### Сообщения не приходят[​](<#messages-not-arriving> "Прямая ссылка на Сообщения не приходят")

- Проверьте, зарегистрирован ли вебхук в BlueBubbles Server → Settings → API → Webhooks
- Убедитесь, что URL вебхука доступен с Mac
- Проверьте `hermes logs gateway` на наличие ошибок вебхука (или `hermes logs -f` для отслеживания в реальном времени)

### «Вспомогательный плагин Private API не подключён»[​](<#private-api-helper-not-connected> "Прямая ссылка на «Вспомогательный плагин Private API не подключён»")

- Установите вспомогательный плагин Private API: [docs.bluebubbles.app](<https://docs.bluebubbles.app/helper-bundle/installation>)
- Базовая отправка сообщений работает и без него — реакции, индикаторы печати и уведомления о прочтении требуют его наличия

- [Предварительные требования](<#prerequisites>)
- [Настройка](<#setup>)
  - [1\. Установите BlueBubbles Server](<#1-install-bluebubbles-server>)
  - [2\. Получите URL сервера и пароль](<#2-get-your-server-url-and-password>)
  - [3\. Настройте Hermes](<#3-configure-hermes>)
  - [4\. Авторизуйте пользователей](<#4-authorize-users>)
  - [5\. Запустите шлюз](<#5-start-the-gateway>)
- [Как это работает](<#how-it-works>)
- [Переменные окружения](<#environment-variables>)
- [Возможности](<#features>)
- [Текстовые сообщения](<#text-messaging>)
- [Медиафайлы](<#rich-media>)
- [Реакции Tapback](<#tapback-reactions>)
- [Индикаторы печати](<#typing-indicators>)
- [Уведомления о прочтении](<#read-receipts>)
- [Адресация чатов](<#chat-addressing>)
- [Private API](<#private-api>)
- [Устранение неполадок](<#troubleshooting>)
  - [«Не удаётся подключиться к серверу»](<#cannot-reach-server>)
  - [Сообщения не приходят](<#messages-not-arriving>)
  - [«Вспомогательный плагин Private API не подключён»](<#private-api-helper-not-connected>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/bluebubbles -->
