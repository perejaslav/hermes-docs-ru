On this page
Hermes подключается к Signal через демон [signal-cli](<https://github.com/AsamK/signal-cli>), работающий в HTTP-режиме. Адаптер передаёт сообщения в реальном времени через SSE (Server-Sent Events) и отправляет ответы через JSON-RPC.
Signal — самый конфиденциальный из массовых мессенджеров: сквозное шифрование по умолчанию, протокол с открытым исходным кодом, минимальный сбор метаданных. Это делает его идеальным для агентских workflows, чувствительных к безопасности.
No New Python Dependencies
Адаптер Signal использует `httpx` (уже входит в основные зависимости Hermes) для всей коммуникации. Никаких дополнительных Python-пакетов не требуется. Вам нужно лишь установить signal-cli извне.
* * *
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **signal-cli** — Signal-клиент на Java ([GitHub](<https://github.com/AsamK/signal-cli>))
  * **Java 17+** — среда выполнения, необходимая для signal-cli
  * **Номер телефона** с установленным Signal (для подключения в качестве вторичного устройства)


### Installing signal-cli[​](<#installing-signal-cli> "Direct link to Installing signal-cli")
[code] 
    # macOS  
    brew install signal-cli  
      
    # Linux (download latest release)  
    VERSION=$(curl -Ls -o /dev/null -w %{url_effective} \\  
      https://github.com/AsamK/signal-cli/releases/latest | sed 's/^.*\\/v//')  
    curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}.tar.gz"  
    sudo tar xf "signal-cli-${VERSION}.tar.gz" -C /opt  
    sudo ln -sf "/opt/signal-cli-${VERSION}/bin/signal-cli" /usr/local/bin/  
    
[/code]
caution
signal-cli **не** находится в репозиториях apt или snap. Установка на Linux, приведённая выше, загружает напрямую из [GitHub releases](<https://github.com/AsamK/signal-cli/releases>).
* * *
## Step 1: Link Your Signal Account[​](<#step-1-link-your-signal-account> "Direct link to Step 1: Link Your Signal Account")
Signal-cli работает как **подключённое устройство** — как WhatsApp Web, но для Signal. Ваш телефон остаётся основным устройством.
[code] 
    # Generate a linking URI (displays a QR code or link)  
    signal-cli link -n "HermesAgent"  
    
[/code]
  1. Откройте **Signal** на вашем телефоне
  2. Перейдите в **Настройки → Подключённые устройства**
  3. Нажмите **Подключить новое устройство**
  4. Отсканируйте QR-код или введите URI


* * *
## Step 2: Start the signal-cli Daemon[​](<#step-2-start-the-signal-cli-daemon> "Direct link to Step 2: Start the signal-cli Daemon")
[code] 
    # Replace +1234567890 with your Signal phone number (E.164 format)  
    signal-cli --account +1234567890 daemon --http 127.0.0.1:8080  
    
[/code]
tip
Держите это работающим в фоне. Вы можете использовать `systemd`, `tmux`, `screen` или запустить как службу.
Проверьте, что он работает:
[code] 
    curl http://127.0.0.1:8080/api/v1/check  
    # Should return: {"versions":{"signal-cli":...}}  
    
[/code]
* * *
## Step 3: Configure Hermes[​](<#step-3-configure-hermes> "Direct link to Step 3: Configure Hermes")
Самый простой способ:
[code] 
    hermes gateway setup  
    
[/code]
Выберите **Signal** в меню платформ. Мастер:
  1. Проверит, установлен ли signal-cli
  2. Запросит HTTP URL (по умолчанию: `http://127.0.0.1:8080`)
  3. Протестирует подключение к демону
  4. Запросит номер телефона аккаунта
  5. Настроит разрешённых пользователей и политики доступа


### Manual Configuration[​](<#manual-configuration> "Direct link to Manual Configuration")
Добавьте в `~/.hermes/.env`:
[code] 
    # Required  
    SIGNAL_HTTP_URL=http://127.0.0.1:8080  
    SIGNAL_ACCOUNT=+1234567890  
      
    # Security (recommended)  
    SIGNAL_ALLOWED_USERS=+1234567890,+0987654321    # Comma-separated E.164 numbers or UUIDs  
      
    # Optional  
    SIGNAL_GROUP_ALLOWED_USERS=groupId1,groupId2     # Enable groups (omit to disable, * for all)  
    SIGNAL_HOME_CHANNEL=+1234567890                  # Default delivery target for cron jobs  
    
[/code]
Затем запустите шлюз:
[code] 
    hermes gateway              # Foreground  
    hermes gateway install      # Install as a user service  
    sudo hermes gateway install --system   # Linux only: boot-time system service  
    
[/code]
* * *
## Access Control[​](<#access-control> "Direct link to Access Control")
### DM Access[​](<#dm-access> "Direct link to DM Access")
Доступ к ЛС следует тому же принципу, что и на других платформах Hermes:
  1. **Установлен `SIGNAL_ALLOWED_USERS`** → только эти пользователи могут писать
  2. **Список не установлен** → неизвестные пользователи получают код привязки в ЛС (подтвердите через `hermes pairing approve signal CODE`)
  3. **Установлен `SIGNAL_ALLOW_ALL_USERS=true`** → писать может кто угодно (используйте с осторожностью)


### Group Access[​](<#group-access> "Direct link to Group Access")
Доступ к группам контролируется переменной окружения `SIGNAL_GROUP_ALLOWED_USERS`:
Конфигурация| Поведение  
---|---  
Не установлена (по умолчанию)| Все групповые сообщения игнорируются. Бот отвечает только в ЛС.  
Установлена с ID групп| Отслеживаются только перечисленные группы (например, `groupId1,groupId2`).  
Установлена в `*`| Бот отвечает в любой группе, в которой состоит.  
* * *
## Features[​](<#features> "Direct link to Features")
### Attachments[​](<#attachments> "Direct link to Attachments")
Адаптер поддерживает отправку и получение медиа в обоих направлениях.
**Входящие** (пользователь → агент):
  * **Изображения** — PNG, JPEG, GIF, WebP (автоопределение по magic bytes)
  * **Аудио** — MP3, OGG, WAV, M4A (голосовые сообщения транскрибируются, если настроен Whisper)
  * **Документы** — PDF, ZIP и другие типы файлов


**Исходящие** (агент → пользователь):
Агент может отправлять медиафайлы через теги `MEDIA:` в ответах. Поддерживаются следующие способы доставки:
  * **Изображения** — `send_multiple_images` и `send_image_file` отправляют PNG, JPEG, GIF, WebP как стандартные Signal-вложения
  * **Голос** — `send_voice` отправляет аудиофайлы (OGG, MP3, WAV, M4A, AAC) как вложения
  * **Видео** — `send_video` отправляет MP4-видеофайлы
  * **Документы** — `send_document` отправляет файлы любого типа (PDF, ZIP и т.д.)


Все исходящие медиа проходят через стандартный API вложений Signal. В отличие от некоторых платформ, Signal не различает голосовые сообщения и файловые вложения на уровне протокола.
Лимит размера вложений: **100 MB** (в обоих направлениях).
warning
**Серверы Signal ограничивают скорость загрузки вложений**, адаптер использует планировщик для отправки нескольких изображений, группируя их в пакеты по 32 и регулируя загрузку в соответствии с политикой сервера Signal.
### Native Formatting, Reply Quotes, and Reactions[​](<#native-formatting-reply-quotes-and-reactions> "Direct link to Native Formatting, Reply Quotes, and Reactions")
Сообщения Signal отображаются с **нативным форматированием** вместо буквальных символов markdown. Адаптер преобразует markdown (`**bold**`, `*italic*`, ``code``, `~~strike~~`, `||spoiler||`, заголовки) в Signal `bodyRanges`, так что текст отображается с реальным стилем в клиенте получателя, а не в виде видимых символов `**` / `` ` ``.
**Цитирование ответов.** Когда Hermes отвечает на конкретное сообщение, он теперь отправляет нативный ответ с цитированием исходного — такой же элемент интерфейса, какой видят пользователи Signal при использовании «Ответить». Это происходит автоматически для ответов, сгенерированных на входящее сообщение.
**Реакции.** Агент может реагировать на сообщения через стандартный API реакций; реакции отображаются в Signal как emoji-реакции на указанное сообщение, а не как дополнительный текст.
Никаких дополнительных настроек не требуется — эта функциональность включена по умолчанию в последних сборках signal-cli. Если ваша версия `signal-cli` слишком старая, Hermes переходит на обычную текстовую доставку и выводит однократное предупреждение в лог.
### Typing Indicators[​](<#typing-indicators> "Direct link to Typing Indicators")
Бот отправляет индикаторы набора текста во время обработки сообщений, обновляя их каждые 8 секунд.
### Phone Number Redaction[​](<#phone-number-redaction> "Direct link to Phone Number Redaction")
Все номера телефонов автоматически маскируются в логах:
  * `+15551234567` → `+155****4567`
  * Это относится как к логам шлюза Hermes, так и к глобальной системе маскировки


### Note to Self (Single-Number Setup)[​](<#note-to-self-single-number-setup> "Direct link to Note to Self \(Single-Number Setup\)")
Если вы запускаете signal-cli как **подключённое вторичное устройство** на своём собственном номере телефона (а не на отдельном номере бота), вы можете взаимодействовать с Hermes через функцию «Заметка себе» в Signal.
Просто отправьте сообщение самому себе с телефона — signal-cli подхватит его, и Hermes ответит в том же диалоге.
**Как это работает:**
  * Сообщения «Заметка себе» приходят как конверты `syncMessage.sentMessage`
  * Адаптер определяет, когда они адресованы аккаунту самого бота, и обрабатывает их как обычные входящие сообщения
  * Защита от эхо-ответов (отслеживание временных меток отправленных сообщений) предотвращает бесконечные циклы — собственные ответы бота автоматически фильтруются


**Никакой дополнительной настройки не требуется.** Это работает автоматически, если `SIGNAL_ACCOUNT` совпадает с вашим номером телефона.
### Health Monitoring[​](<#health-monitoring> "Direct link to Health Monitoring")
Адаптер отслеживает SSE-соединение и автоматически переподключается, если:
  * Соединение разорвано (с экспоненциальной задержкой: 2с → 60с)
  * Активность не обнаружена в течение 120 секунд (отправляет ping signal-cli для проверки)


* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
Проблема| Решение  
---|---  
**«Cannot reach signal-cli»** при настройке| Убедитесь, что демон signal-cli запущен: `signal-cli --account +YOUR_NUMBER daemon --http 127.0.0.1:8080`  
**Сообщения не приходят**|  Проверьте, что `SIGNAL_ALLOWED_USERS` включает номер отправителя в формате E.164 (с префиксом `+`)  
**«signal-cli not found on PATH»**|  Установите signal-cli и убедитесь, что он находится в PATH, или используйте Docker  
**Соединение постоянно разрывается**|  Проверьте логи signal-cli на наличие ошибок. Убедитесь, что установлена Java 17+.  
**Групповые сообщения игнорируются**|  Настройте `SIGNAL_GROUP_ALLOWED_USERS` с конкретными ID групп или `*` для разрешения всех групп.  
**Бот никому не отвечает**|  Настройте `SIGNAL_ALLOWED_USERS`, используйте привязку в ЛС или явно разрешите всех пользователей через политику шлюза, если нужен более широкий доступ.  
**Дублирующиеся сообщения**|  Убедитесь, что только один экземпляр signal-cli слушает ваш номер телефона  
* * *
## Security[​](<#security> "Direct link to Security")
warning
**Всегда настраивайте контроль доступа.** У бота по умолчанию есть доступ к терминалу. Без `SIGNAL_ALLOWED_USERS` или привязки в ЛС шлюз отклоняет все входящие сообщения в целях безопасности.
  * Номера телефонов маскируются во всех логах
  * Используйте привязку в ЛС или явные списки разрешений для безопасного подключения новых пользователей
  * Держите группы отключёнными, если вам не нужна поддержка групп, или добавляйте в список только те группы, которым доверяете
  * Сквозное шифрование Signal защищает содержимое сообщений при передаче
  * Данные сессии signal-cli в `~/.local/share/signal-cli/` содержат учётные данные аккаунта — защищайте их как пароль


* * *
## Environment Variables Reference[​](<#environment-variables-reference> "Direct link to Environment Variables Reference")
Переменная| Обязательная| По умолчанию| Описание  
---|---|---|---  
`SIGNAL_HTTP_URL`| Да| —| HTTP-эндпоинт signal-cli  
`SIGNAL_ACCOUNT`| Да| —| Номер телефона бота (E.164)  
`SIGNAL_ALLOWED_USERS`| Нет| —| Номера телефонов/UUID через запятую  
`SIGNAL_GROUP_ALLOWED_USERS`| Нет| —| ID групп для отслеживания или `*` для всех (не указывайте для отключения групп)  
`SIGNAL_ALLOW_ALL_USERS`| Нет| `false`| Разрешить любому пользователю взаимодействие (пропустить список разрешений)  
`SIGNAL_HOME_CHANNEL`| Нет| —| Цель доставки по умолчанию для cron-задач  
  * [Prerequisites](<#prerequisites>)
    * [Installing signal-cli](<#installing-signal-cli>)
  * [Step 1: Link Your Signal Account](<#step-1-link-your-signal-account>)
  * [Step 2: Start the signal-cli Daemon](<#step-2-start-the-signal-cli-daemon>)
  * [Step 3: Configure Hermes](<#step-3-configure-hermes>)
    * [Manual Configuration](<#manual-configuration>)
  * [Access Control](<#access-control>)
    * [DM Access](<#dm-access>)
    * [Group Access](<#group-access>)
  * [Features](<#features>)
    * [Attachments](<#attachments>)
    * [Native Formatting, Reply Quotes, and Reactions](<#native-formatting-reply-quotes-and-reactions>)
    * [Typing Indicators](<#typing-indicators>)
    * [Phone Number Redaction](<#phone-number-redaction>)
    * [Note to Self (Single-Number Setup)](<#note-to-self-single-number-setup>)
    * [Health Monitoring](<#health-monitoring>)
  * [Troubleshooting](<#troubleshooting>)
  * [Security](<#security>)
  * [Environment Variables Reference](<#environment-variables-reference>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal -->
