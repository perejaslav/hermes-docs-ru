On this page
Интеграция Gmail, Calendar, Drive, Contacts, Sheets и Docs для Hermes. Использует OAuth2 с автоматическим обновлением токена. Предпочитает [Google Workspace CLI (`gws`)](<https://github.com/nicholasgasior/gws>) при его наличии для более широкого охвата, а в остальных случаях использует клиентские библиотеки Python от Google.

**Путь навыка:** `skills/productivity/google-workspace/`

## Настройка[​](<#setup> "Прямая ссылка на Настройка")

Настройка полностью управляется агентом — попросите Hermes настроить Google Workspace, и он проведёт вас через каждый шаг. Процесс:

  1. **Создайте проект в Google Cloud** и включите необходимые API (Gmail, Calendar, Drive, Sheets, Docs, People)
  2. **Создайте учётные данные OAuth 2.0** (тип «Десктопное приложение») и скачайте клиентский секрет в JSON
  3. **Авторизуйтесь** — Hermes генерирует URL для авторизации, вы одобряете доступ в браузере и вставляете обратно полученный redirect URL
  4. **Готово** — токен будет автоматически обновляться с этого момента

> **Только email**
> Если вам нужна только электронная почта (без Calendar/Drive/Sheets), используйте навык **himalaya** — он работает с паролем приложения Gmail и занимает 2 минуты. Проект в Google Cloud не требуется.

## Gmail[​](<#gmail> "Прямая ссылка на Gmail")

### Поиск[​](<#searching> "Прямая ссылка на Поиск")

[code]
    $GAPI gmail search "is:unread" --max 10
    $GAPI gmail search "from:boss@company.com newer_than:1d"
    $GAPI gmail search "has:attachment filename:pdf newer_than:7d"
    
[/code]

Возвращает JSON с полями `id`, `from`, `subject`, `date`, `snippet` и `labels` для каждого сообщения.

### Чтение[​](<#reading> "Прямая ссылка на Чтение")

[code]
    $GAPI gmail get MESSAGE_ID
    
[/code]

Возвращает полный текст сообщения (предпочитает обычный текст, при его отсутствии — HTML).

### Отправка[​](<#sending> "Прямая ссылка на Отправка")

[code]
    # Обычная отправка
    $GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
      
    # HTML-письмо
    $GAPI gmail send --to user@example.com --subject "Report" \
      --body "<h1>Q4 Results</h1><p>Details here</p>" --html
      
    # Пользовательский заголовок From (отображаемое имя + email)
    $GAPI gmail send --to user@example.com --subject "Hello" \
      --from '"Research Agent" <user@example.com>' --body "Message text"
      
    # С копией (CC)
    $GAPI gmail send --to user@example.com --cc "team@example.com" \
      --subject "Update" --body "FYI"
    
[/code]

### Пользовательский заголовок From[​](<#custom-from-header> "Прямая ссылка на Пользовательский заголовок From")

Флаг `--from` позволяет настроить отображаемое имя отправителя в исходящих письмах. Это полезно, когда несколько агентов используют один аккаунт Gmail, но вы хотите, чтобы получатели видели разные имена:

[code]
    # Агент 1
    $GAPI gmail send --to client@co.com --subject "Research Summary" \
      --from '"Research Agent" <shared@company.com>' --body "..."
      
    # Агент 2
    $GAPI gmail send --to client@co.com --subject "Code Review" \
      --from '"Code Assistant" <shared@company.com>' --body "..."
    
[/code]

**Как это работает:** Значение `--from` устанавливается как заголовок `From` в формате RFC 5322 в MIME-сообщении. Gmail позволяет настроить отображаемое имя для вашего собственного аутентифицированного адреса электронной почты без дополнительной конфигурации. Получатели видят настроенное отображаемое имя (например, «Research Agent»), при этом адрес электронной почты остаётся тем же.

**Важно:** Если вы используете в `--from` _другой адрес электронной почты_ (не аутентифицированный), Gmail требует, чтобы этот адрес был настроен как псевдоним [Send As](<https://support.google.com/mail/answer/22370>) в настройках Gmail → Аккаунты → Отправлять письма как.

Флаг `--from` работает как с `send`, так и с `reply`:

[code]
    $GAPI gmail reply MESSAGE_ID \
      --from '"Support Bot" <shared@company.com>' --body "We're on it"
    
[/code]

### Ответы[​](<#replying> "Прямая ссылка на Ответы")

[code]
    $GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
    
[/code]

Автоматически привязывает ответ к той же цепочке (устанавливает заголовки `In-Reply-To` и `References`) и использует thread ID исходного сообщения.

### Метки[​](<#labels> "Прямая ссылка на Метки")

[code]
    # Список всех меток
    $GAPI gmail labels
      
    # Добавление/удаление меток
    $GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
    $GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
    
[/code]

## Calendar[​](<#calendar> "Прямая ссылка на Calendar")

[code]
    # Список событий (по умолчанию на следующие 7 дней)
    $GAPI calendar list
    $GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z
      
    # Создание события (часовой пояс обязателен)
    $GAPI calendar create --summary "Team Standup" \
      --start 2026-03-01T10:00:00-07:00 --end 2026-03-01T10:30:00-07:00
      
    # С местом и участниками
    $GAPI calendar create --summary "Lunch" \
      --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z \
      --location "Cafe" --attendees "alice@co.com,bob@co.com"
      
    # Удаление события
    $GAPI calendar delete EVENT_ID
    
[/code]

> **warning**
> Время в Calendar **обязательно** должно включать часовой пояс (например, `-07:00`) или использовать UTC (`Z`). Простые даты вроде `2026-03-01T10:00:00` неоднозначны и будут интерпретироваться как UTC.

## Drive[​](<#drive> "Прямая ссылка на Drive")

[code]
    $GAPI drive search "quarterly report" --max 10
    $GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
    
[/code]

## Sheets[​](<#sheets> "Прямая ссылка на Sheets")

[code]
    # Чтение диапазона
    $GAPI sheets get SHEET_ID "Sheet1!A1:D10"
      
    # Запись в диапазон
    $GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'
      
    # Добавление строк
    $GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
    
[/code]

## Docs[​](<#docs> "Прямая ссылка на Docs")

[code]
    $GAPI docs get DOC_ID
    
[/code]

Возвращает заголовок документа и полное текстовое содержимое.

## Contacts[​](<#contacts> "Прямая ссылка на Contacts")

[code]
    $GAPI contacts list --max 20
    
[/code]

## Формат вывода[​](<#output-format> "Прямая ссылка на Формат вывода")

Все команды возвращают JSON. Ключевые поля для каждого сервиса:

| Команда | Поля |
|---|---|
| `gmail search` | `id`, `threadId`, `from`, `to`, `subject`, `date`, `snippet`, `labels` |
| `gmail get` | `id`, `threadId`, `from`, `to`, `subject`, `date`, `labels`, `body` |
| `gmail send/reply` | `status`, `id`, `threadId` |
| `calendar list` | `id`, `summary`, `start`, `end`, `location`, `description`, `htmlLink` |
| `calendar create` | `status`, `id`, `summary`, `htmlLink` |
| `drive search` | `id`, `name`, `mimeType`, `modifiedTime`, `webViewLink` |
| `contacts list` | `name`, `emails`, `phones` |
| `sheets get` | Двумерный массив значений ячеек |

## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")

| Проблема | Решение |
|---|---|
| `NOT_AUTHENTICATED` | Выполните настройку (попросите Hermes настроить Google Workspace) |
| `REFRESH_FAILED` | Токен отозван — повторите шаги авторизации |
| `HttpError 403: Insufficient Permission` | Не хватает области доступа — отзовите токен и авторизуйтесь снова с нужными сервисами |
| `HttpError 403: Access Not Configured` | API не включён в Google Cloud Console |
| `ModuleNotFoundError` | Запустите скрипт настройки с `--install-deps` |

  * [Настройка](<#setup>)
  * [Gmail](<#gmail>)
    * [Поиск](<#searching>)
    * [Чтение](<#reading>)
    * [Отправка](<#sending>)
    * [Пользовательский заголовок From](<#custom-from-header>)
    * [Ответы](<#replying>)
    * [Метки](<#labels>)
  * [Calendar](<#calendar>)
  * [Drive](<#drive>)
  * [Sheets](<#sheets>)
  * [Docs](<#docs>)
  * [Contacts](<#contacts>)
  * [Формат вывода](<#output-format>)
  * [Устранение неполадок](<#troubleshooting>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace -->
