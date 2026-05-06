On this page

Gmail, Календарь, Диск, Документы, Таблицы через CLI-утилиту gws или Python.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |
|---|---|
Источник| Встроенный (устанавливается по умолчанию)
Путь| `skills/productivity/google-workspace`
Версия| `1.0.1`
Автор| Nous Research
Лицензия| MIT
Теги| `Google`, `Gmail`, `Calendar`, `Drive`, `Sheets`, `Docs`, `Contacts`, `Email`, `OAuth`
Связанные навыки| [`himalaya`](</docs/user-guide/skills/bundled/email/email-himalaya>)

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.

# Google Workspace

Gmail, Календарь, Диск, Контакты, Таблицы и Документы — через управляемый Hermes OAuth и тонкую CLI-обёртку. Когда установлен `gws`, навык использует его как исполнительный бэкенд для более широкого покрытия Google Workspace; в противном случае используется встроенная реализация на Python.

## Ссылки[​](<#references> "Прямая ссылка на Ссылки")

  * `references/gmail-search-syntax.md` — Операторы поиска Gmail (is:unread, from:, newer_than: и т.д.)

## Скрипты[​](<#scripts> "Прямая ссылка на Скрипты")

  * `scripts/setup.py` — Настройка OAuth2 (запустить один раз для авторизации)
  * `scripts/google_api.py` — Совместимая обёртка CLI. При возможности предпочитает `gws` для операций, сохраняя при этом существующий JSON-контракт вывода Hermes.

## Первоначальная настройка[​](<#first-time-setup> "Прямая ссылка на Первоначальная настройка")

Настройка полностью неинтерактивна — вы управляете ей шаг за шагом, чтобы она работала в CLI, Telegram, Discord или на любой платформе.

Сначала определите сокращение:

[code] 
    GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"  
    
[/code]

### Шаг 0: Проверка, выполнена ли настройка[​](<#step-0-check-if-already-set-up> "Прямая ссылка на Шаг 0: Проверка, выполнена ли настройка")

[code] 
    $GSETUP --check  
    
[/code]

Если выводится `AUTHENTICATED`, переходите к разделу Использование — настройка уже выполнена.

### Шаг 1: Сортировка — спросите пользователя, что ему нужно[​](<#step-1-triage--ask-the-user-what-they-need> "Прямая ссылка на Шаг 1: Сортировка — спросите пользователя, что ему нужно")

Перед началом настройки OAuth задайте пользователю ДВА вопроса:

**Вопрос 1: «Какие сервисы Google вам нужны? Только почта или также Календарь/Диск/Таблицы/Документы?»**

  * **Только почта** → Этот навык не нужен. Используйте навык `himalaya` — он работает с паролем приложения Gmail (Настройки → Безопасность → Пароли приложений) и настраивается за 2 минуты. Проект Google Cloud не требуется. Загрузите навык himalaya и следуйте его инструкциям по настройке.
  * **Почта + Календарь** → Продолжайте с этим навыком, но используйте `--services email,calendar` при авторизации, чтобы экран согласия запрашивал только необходимые разрешения.
  * **Только Календарь/Диск/Таблицы/Документы** → Продолжайте с этим навыком и используйте более узкий набор `--services`, например `calendar,drive,sheets,docs`.
  * **Полный доступ к Workspace** → Продолжайте с этим навыком и используйте набор сервисов по умолчанию `all`.

**Вопрос 2: «Использует ли ваш аккаунт Google расширенную защиту (Advanced Protection — для входа требуются аппаратные ключи безопасности)? Если вы не уверены, скорее всего нет — это то, на что вы подписывались бы явно.»**

  * **Нет / Не уверен** → Обычная настройка. Продолжайте ниже.
  * **Да** → Администратор Workspace должен добавить OAuth-клиент ID в список разрешённых приложений организации, прежде чем Шаг 4 сработает. Сообщите им об этом заранее.

### Шаг 2: Создание OAuth-учётных данных (однократно, ~5 минут)[​](<#step-2-create-oauth-credentials-one-time-5-minutes> "Прямая ссылка на Шаг 2: Создание OAuth-учётных данных (однократно, ~5 минут)")

Сообщите пользователю:

> Вам нужен OAuth-клиент Google Cloud. Это однократная настройка:
>   1. Создайте или выберите проект: <https://console.cloud.google.com/projectselector2/home/dashboard>
>   2. Включите необходимые API в библиотеке API: <https://console.cloud.google.com/apis/library> Включите: Gmail API, Google Calendar API, Google Drive API, Google Sheets API, Google Docs API, People API
>   3. Создайте OAuth-клиент здесь: <https://console.cloud.google.com/apis/credentials> Учётные данные → Создать учётные данные → OAuth 2.0 Client ID
>   4. Тип приложения: «Desktop app» → Создать
>   5. Если приложение ещё в режиме тестирования, добавьте аккаунт пользователя Google как тестового пользователя здесь: <https://console.cloud.google.com/auth/audience> Audience → Test users → Add users
>   6. Скачайте JSON-файл и сообщите мне путь к файлу
>
> Важное примечание для CLI Hermes: если путь к файлу начинается с `/`, НЕ отправляйте голый путь отдельным сообщением в CLI, так как его можно принять за слэш-команду. Отправьте его в предложении, например: «Путь к JSON-файлу: /home/user/Downloads/client_secret_....json»

После того как они укажут путь:

[code] 
    $GSETUP --client-secret /path/to/client_secret.json  
    
[/code]

Если они вставляют значения client ID / client secret вместо пути к файлу, создайте для них корректный JSON-файл Desktop OAuth самостоятельно, сохраните его в явно указанное место (например, `~/Downloads/hermes-google-client-secret.json`), затем запустите `--client-secret` с этим файлом.

### Шаг 3: Получение URL авторизации[​](<#step-3-get-authorization-url> "Прямая ссылка на Шаг 3: Получение URL авторизации")

Используйте набор сервисов, выбранный на Шаге 1. Примеры:

[code] 
    $GSETUP --auth-url --services email,calendar --format json  
    $GSETUP --auth-url --services calendar,drive,sheets,docs --format json  
    $GSETUP --auth-url --services all --format json  
    
[/code]

Это возвращает JSON с полем `auth_url`, а также сохраняет точный URL в `~/.hermes/google_oauth_last_url.txt`.

Правила агента для этого шага:

  * Извлеките поле `auth_url` и отправьте этот точный URL пользователю одной строкой.
  * Сообщите пользователю, что браузер, скорее всего, покажет ошибку на `http://localhost:1` после подтверждения, и что это ожидаемо.
  * Скажите им скопировать ВЕСЬ перенаправленный URL из адресной строки браузера.
  * Если пользователь получил `Error 403: access_denied`, отправьте их напрямую на `https://console.cloud.google.com/auth/audience`, чтобы добавить себя как тестового пользователя.

### Шаг 4: Обмен кода[​](<#step-4-exchange-the-code> "Прямая ссылка на Шаг 4: Обмен кода")

Пользователь вставит либо URL вида `http://localhost:1/?code=4/0A...&scope=...`, либо просто строку кода. Любой вариант подходит. На шаге `--auth-url` временно сохраняется ожидающая OAuth-сессия локально, чтобы `--auth-code` мог завершить обмен PKCE позже, даже на безголовых системах:

[code] 
    $GSETUP --auth-code "URL_ИЛИ_КОД_КОТОРЫЙ_ВСТАВИЛ_ПОЛЬЗОВАТЕЛЬ" --format json  
    
[/code]

Если `--auth-code` завершается ошибкой из-за того, что код истёк, уже был использован или пришёл из старой вкладки браузера, теперь он возвращает свежий `fresh_auth_url`. В этом случае немедленно отправьте новый URL пользователю и попросите его повторить попытку только с перенаправлением из новейшей вкладки браузера.

### Шаг 5: Проверка[​](<#step-5-verify> "Прямая ссылка на Шаг 5: Проверка")

[code] 
    $GSETUP --check  
    
[/code]

Должно вывести `AUTHENTICATED`. Настройка завершена — токен будет автоматически обновляться в дальнейшем.

### Примечания[​](<#notes> "Прямая ссылка на Примечания")

  * Токен хранится в `~/.hermes/google_token.json` и автоматически обновляется.
  * Состояние ожидающей OAuth-сессии/верификатор временно хранятся в `~/.hermes/google_oauth_pending.json` до завершения обмена.
  * Если установлен `gws`, `google_api.py` направляет его на тот же файл учётных данных `~/.hermes/google_token.json`. Пользователям не нужно запускать отдельный процесс `gws auth login`.
  * Для отзыва: `$GSETUP --revoke`

## Использование[​](<#usage> "Прямая ссылка на Использование")

Все команды проходят через API-скрипт. Установите `GAPI` как сокращение:

[code] 
    GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"  
    
[/code]

### Gmail[​](<#gmail> "Прямая ссылка на Gmail")

[code] 
    # Поиск (возвращает JSON-массив с id, from, subject, date, snippet)  
    $GAPI gmail search "is:unread" --max 10  
    $GAPI gmail search "from:boss@company.com newer_than:1d"  
    $GAPI gmail search "has:attachment filename:pdf newer_than:7d"  
      
    # Чтение полного сообщения (возвращает JSON с телом письма)  
    $GAPI gmail get ID_СООБЩЕНИЯ  
      
    # Отправка  
    $GAPI gmail send --to user@example.com --subject "Привет" --body "Текст сообщения"  
    $GAPI gmail send --to user@example.com --subject "Отчёт" --body "<h1>Q4</h1><p>Детали...</p>" --html  
    $GAPI gmail send --to user@example.com --subject "Привет" --from '"Research Agent" <user@example.com>' --body "Текст сообщения"  
      
    # Ответ (автоматически создаёт цепочку и устанавливает In-Reply-To)  
    $GAPI gmail reply ID_СООБЩЕНИЯ --body "Спасибо, меня устраивает."  
    $GAPI gmail reply ID_СООБЩЕНИЯ --from '"Support Bot" <user@example.com>' --body "Спасибо"  
      
    # Метки  
    $GAPI gmail labels  
    $GAPI gmail modify ID_СООБЩЕНИЯ --add-labels ID_МЕТКИ  
    $GAPI gmail modify ID_СООБЩЕНИЯ --remove-labels UNREAD  
    
[/code]

### Календарь[​](<#calendar> "Прямая ссылка на Календарь")

[code] 
    # Список событий (по умолчанию следующие 7 дней)  
    $GAPI calendar list  
    $GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z  
      
    # Создание события (требуется ISO 8601 с часовым поясом)  
    $GAPI calendar create --summary "Командный стендап" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00  
    $GAPI calendar create --summary "Обед" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Кафе"  
    $GAPI calendar create --summary "Ревью" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"  
      
    # Удаление события  
    $GAPI calendar delete ID_СОБЫТИЯ  
    
[/code]

### Диск[​](<#drive> "Прямая ссылка на Диск")

[code] 
    $GAPI drive search "ежеквартальный отчёт" --max 10  
    $GAPI drive search "mimeType='application/pdf'" --raw-query --max 5  
    
[/code]

### Контакты[​](<#contacts> "Прямая ссылка на Контакты")

[code] 
    $GAPI contacts list --max 20  
    
[/code]

### Таблицы[​](<#sheets> "Прямая ссылка на Таблицы")

[code] 
    # Чтение  
    $GAPI sheets get ID_ТАБЛИЦЫ "Sheet1!A1:D10"  
      
    # Запись  
    $GAPI sheets update ID_ТАБЛИЦЫ "Sheet1!A1:B2" --values '[[\"Name\",\"Score\"],[\"Alice\",\"95\"]]'  
      
    # Добавление строк  
    $GAPI sheets append ID_ТАБЛИЦЫ "Sheet1!A:C" --values '[[\"new\",\"row\",\"data\"]]'  
    
[/code]

### Документы[​](<#docs> "Прямая ссылка на Документы")

[code] 
    $GAPI docs get ID_ДОКУМЕНТА  
    
[/code]

## Формат вывода[​](<#output-format> "Прямая ссылка на Формат вывода")

Все команды возвращают JSON. Разбирайте с помощью `jq` или читайте напрямую. Ключевые поля:

  * **Gmail search**: `[{id, threadId, from, to, subject, date, snippet, labels}]`
  * **Gmail get**: `{id, threadId, from, to, subject, date, labels, body}`
  * **Gmail send/reply**: `{status: "sent", id, threadId}`
  * **Calendar list**: `[{id, summary, start, end, location, description, htmlLink}]`
  * **Calendar create**: `{status: "created", id, summary, htmlLink}`
  * **Drive search**: `[{id, name, mimeType, modifiedTime, webViewLink}]`
  * **Contacts list**: `[{name, emails: [...], phones: [...]}]`
  * **Sheets get**: `[[cell, cell, ...], ...]`

## Правила[​](<#rules> "Прямая ссылка на Правила")

  1. **Никогда не отправляйте email и не создавайте/удаляйте события без подтверждения пользователя.** Покажите черновик содержимого и запросите одобрение.
  2. **Проверяйте авторизацию перед первым использованием** — запустите `setup.py --check`. Если не удаётся, проведите пользователя через настройку.
  3. **Используйте справочник синтаксиса поиска Gmail** для сложных запросов — загрузите его с помощью `skill_view("google-workspace", file_path="references/gmail-search-syntax.md")`.
  4. **Время в календаре должно включать часовой пояс** — всегда используйте ISO 8601 со смещением (например, `2026-03-01T10:00:00-06:00`) или UTC (`Z`).
  5. **Соблюдайте лимиты запросов** — избегайте быстрых последовательных вызовов API. По возможности группируйте чтения.

## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")

Проблема| Исправление  
---|---  
`NOT_AUTHENTICATED`| Выполните шаги 2-5 настройки выше  
`REFRESH_FAILED`| Токен отозван или истёк — повторите шаги 3-5  
`HttpError 403: Insufficient Permission`| Не хватает области API — `$GSETUP --revoke`, затем повторите шаги 3-5  
`HttpError 403: Access Not Configured`| API не включён — пользователю нужно включить его в Google Cloud Console  
`ModuleNotFoundError`| Запустите `$GSETUP --install-deps`  
Расширенная защита блокирует авторизацию| Администратор Workspace должен добавить OAuth-клиент ID в белый список  

## Отзыв доступа[​](<#revoking-access> "Прямая ссылка на Отзыв доступа")

[code] 
    $GSETUP --revoke  
    
[/code]

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Ссылки](<#references>)
  * [Скрипты](<#scripts>)
  * [Первоначальная настройка](<#first-time-setup>)
    * [Шаг 0: Проверка, выполнена ли настройка](<#step-0-check-if-already-set-up>)
    * [Шаг 1: Сортировка — спросите пользователя, что ему нужно](<#step-1-triage--ask-the-user-what-they-need>)
    * [Шаг 2: Создание OAuth-учётных данных (однократно, ~5 минут)](<#step-2-create-oauth-credentials-one-time-5-minutes>)
    * [Шаг 3: Получение URL авторизации](<#step-3-get-authorization-url>)
    * [Шаг 4: Обмен кода](<#step-4-exchange-the-code>)
    * [Шаг 5: Проверка](<#step-5-verify>)
    * [Примечания](<#notes>)
  * [Использование](<#usage>)
    * [Gmail](<#gmail>)
    * [Календарь](<#calendar>)
    * [Диск](<#drive>)
    * [Контакты](<#contacts>)
    * [Таблицы](<#sheets>)
    * [Документы](<#docs>)
  * [Формат вывода](<#output-format>)
  * [Правила](<#rules>)
  * [Устранение неполадок](<#troubleshooting>)
  * [Отзыв доступа](<#revoking-access>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-google-workspace -->
