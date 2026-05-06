На этой странице
Airtable REST API через curl. CRUD записей, фильтры, апсерты.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---  |
|Источник| Встроенный (устанавливается по умолчанию)  |
|Путь| `skills/productivity/airtable`  |
|Версия| `1.1.0`  |
|Автор| community  |
|Лицензия| MIT  |
|Теги| `Airtable`, `Productivity`, `Database`, `API`  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приводится полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Airtable — Базы, Таблицы и Записи
Работа с REST API Airtable напрямую через `curl` с помощью инструмента `terminal`. Никакого MCP-сервера, OAuth-потока или Python SDK — только `curl` и персональный токен доступа.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  1. Создайте **Персональный токен доступа (PAT)** на <https://airtable.com/create/tokens> (токены начинаются с `pat...`).
  2. Предоставьте следующие разрешения (минимум):
     * `data.records:read` — чтение строк
     * `data.records:write` — создание / обновление / удаление строк
     * `schema.bases:read` — просмотр списка баз и таблиц
  3. **Важно:** в том же интерфейсе токена добавьте каждую базу, к которой нужен доступ, в список **Access** токена. PAT действуют в разрезе каждой базы — валидный токен для не той базы вернёт `403`.
  4. Сохраните токен в `~/.hermes/.env` (или через `hermes setup`):
[code] AIRTABLE_API_KEY=pat_your_token_here  
         
[/code]

> Примечание: устаревшие ключи API вида `key...` были объявлены устаревшими в феврале 2024 г. Сейчас работают только PAT и OAuth-токены.
## Основы API[​](<#api-basics> "Прямая ссылка на Основы API")
  * **Эндпоинт:** `https://api.airtable.com/v0`
  * **Заголовок авторизации:** `Authorization: Bearer $AIRTABLE_API_KEY`
  * **Все запросы** используют JSON (`Content-Type: application/json` для любого тела POST/PATCH/PUT).
  * **ID объектов:** базы `app...`, таблицы `tbl...`, записи `rec...`, поля `fld...`. ID никогда не меняются; названия — могут. В автоматизации лучше используйте ID.
  * **Лимит запросов:** 5 запросов/сек/базу. `429` → снизьте темп. Пакетная отправка на одну базу будет ограничена.


Базовый шаблон curl:
[code] 
    curl -s \"https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=5\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
Флаг `-s` подавляет индикатор прогресса curl — оставляйте его в каждом вызове, чтобы вывод инструмента оставался чистым для Hermes. Передавайте через `python3 -m json.tool` (всегда доступен) или `jq` (если установлен) для читаемого JSON.
## Типы полей (формы тела запроса)[​](<#field-types-request-body-shapes> "Прямая ссылка на Типы полей (формы тела запроса)")
Тип поля| Форма для записи  
|---|---  
Однострочный текст| `\"Name\": \"hello\"`  
Длинный текст| `\"Notes\": \"multi\\nline\"`  
Число| `\"Score\": 42`  
Флажок| `\"Done\": true`  
Одиночный выбор| `\"Status\": \"Todo\"` (название должно уже существовать, если не указано `typecast: true`)  
Множественный выбор| `\"Tags\": [\"urgent\", \"bug\"]`  
Дата| `\"Due\": \"2026-04-01\"`  
Дата и время (UTC)| `\"At\": \"2026-04-01T14:30:00.000Z\"`  
URL / Email / Телефон| `\"Link\": \"https://…\"`  
Вложение| `\"Files\": [{\"url\": \"https://…\"}]` (Airtable загружает и размещает у себя)  
Связанная запись| `\"Owner\": [\"recXXXXXXXXXXXXXX\"]` (массив ID записей)  
Пользователь| `\"AssignedTo\": {\"id\": \"usrXXXXXXXXXXXXXX\"}`  
Передайте `\"typecast\": true` на верхнем уровне тела создания/обновления, чтобы Airtable автоматически приводил типы (например, создать новый вариант выбора на лету, преобразовать `\"42\"` → `42`).
## Часто используемые запросы[​](<#common-queries> "Прямая ссылка на Часто используемые запросы")
### Список баз, доступных токену[​](<#list-bases-the-token-can-see> "Прямая ссылка на Список баз, доступных токену")
[code] 
    curl -s \"https://api.airtable.com/v0/meta/bases\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
### Список таблиц и схемы для базы[​](<#list-tables--schema-for-a-base> "Прямая ссылка на Список таблиц и схемы для базы")
[code] 
    curl -s \"https://api.airtable.com/v0/meta/bases/$BASE_ID/tables\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
Используйте это ПЕРЕД изменением данных — позволяет уточнить точные названия полей и их ID, показывает `options.choices` для полей выбора и названия первичных полей.
### Список записей (первые 10)[​](<#list-records-first-10> "Прямая ссылка на Список записей (первые 10)")
[code] 
    curl -s \"https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=10\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
### Получение одной записи[​](<#get-a-single-record> "Прямая ссылка на Получение одной записи")
[code] 
    curl -s \"https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
### Фильтрация записей (filterByFormula)[​](<#filter-records-filterbyformula> "Прямая ссылка на Фильтрация записей (filterByFormula)")
Формулы Airtable должны быть URL-закодированы. Используйте стандартную библиотеку Python — никогда не кодируйте вручную:
[code] 
    FORMULA=\"{Status}='Todo'\"  
    ENC=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=\"\"))' \"$FORMULA\")  
    curl -s \"https://api.airtable.com/v0/$BASE_ID/$TABLE?filterByFormula=$ENC&maxRecords=20\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
Полезные шаблоны формул:
  * Точное совпадение: `{Email}='user@example.com'`
  * Содержит: `FIND('bug', LOWER({Title}))`
  * Несколько условий: `AND({Status}='Todo', {Priority}='High')`
  * Или: `OR({Owner}='alice', {Owner}='bob')`
  * Не пусто: `NOT({Assignee}='')`
  * Сравнение дат: `IS_AFTER({Due}, TODAY())`


### Сортировка и выбор определённых полей[​](<#sort--select-specific-fields> "Прямая ссылка на Сортировка и выбор определённых полей")
[code] 
    curl -s \"https://api.airtable.com/v0/$BASE_ID/$TABLE?sort%5B0%5D%5Bfield%5D=Priority&sort%5B0%5D%5Bdirection%5D=asc&fields%5B%5D=Name&fields%5B%5D=Status\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
Квадратные скобки в параметрах запроса ОБЯЗАТЕЛЬНО должны быть URL-закодированы (`%5B` / `%5D`).
### Использование именованного представления[​](<#use-a-named-view> "Прямая ссылка на Использование именованного представления")
[code] 
    curl -s \"https://api.airtable.com/v0/$BASE_ID/$TABLE?view=Grid%20view&maxRecords=50\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
Представления применяют свои сохранённые фильтры и сортировку на стороне сервера.
## Часто используемые изменения[​](<#common-mutations> "Прямая ссылка на Часто используемые изменения")
### Создание записи[​](<#create-a-record> "Прямая ссылка на Создание записи")
[code] 
    curl -s -X POST \"https://api.airtable.com/v0/$BASE_ID/$TABLE\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{\"fields\":{\"Name\":\"New task\",\"Status\":\"Todo\",\"Priority\":\"High\"}}' | python3 -m json.tool  
    
[/code]
### Создание до 10 записей за один вызов[​](<#create-up-to-10-records-in-one-call> "Прямая ссылка на Создание до 10 записей за один вызов")
[code] 
    curl -s -X POST \"https://api.airtable.com/v0/$BASE_ID/$TABLE\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{  
        \"typecast\": true,  
        \"records\": [  
          {\"fields\": {\"Name\": \"Task A\", \"Status\": \"Todo\"}},  
          {\"fields\": {\"Name\": \"Task B\", \"Status\": \"In progress\"}}  
        ]  
      }' | python3 -m json.tool  
    
[/code]
Пакетные эндпоинты ограничены **10 записями на запрос**. Для массовой вставки используйте цикл по 10 записей с небольшой паузой для соблюдения лимита 5 запросов/сек/базу.
### Обновление записи (PATCH — объединяет, сохраняет неизменённые поля)[​](<#update-a-record-patch--merges-preserves-unchanged-fields> "Прямая ссылка на Обновление записи (PATCH — объединяет, сохраняет неизменённые поля)")
[code] 
    curl -s -X PATCH \"https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{\"fields\":{\"Status\":\"Done\"}}' | python3 -m json.tool  
    
[/code]
### Апсерт по полю слияния (ID не требуется)[​](<#upsert-by-a-merge-field-no-id-needed> "Прямая ссылка на Апсерт по полю слияния (ID не требуется)")
[code] 
    curl -s -X PATCH \"https://api.airtable.com/v0/$BASE_ID/$TABLE\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{  
        \"performUpsert\": {\"fieldsToMergeOn\": [\"Email\"]},  
        \"records\": [  
          {\"fields\": {\"Email\": \"user@example.com\", \"Status\": \"Active\"}}  
        ]  
      }' | python3 -m json.tool  
    
[/code]
`performUpsert` создаёт записи, значения полей слияния которых являются новыми, и обновляет записи, значения полей слияния которых уже существуют. Отлично подходит для идемпотентной синхронизации.
### Удаление записи[​](<#delete-a-record> "Прямая ссылка на Удаление записи")
[code] 
    curl -s -X DELETE \"https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
### Удаление до 10 записей за один вызов[​](<#delete-up-to-10-records-in-one-call> "Прямая ссылка на Удаление до 10 записей за один вызов")
[code] 
    curl -s -X DELETE \"https://api.airtable.com/v0/$BASE_ID/$TABLE?records%5B%5D=rec1&records%5B%5D=rec2\" \\  
      -H \"Authorization: Bearer $AIRTABLE_API_KEY\" | python3 -m json.tool  
    
[/code]
## Пагинация[​](<#pagination> "Прямая ссылка на Пагинация")
Эндпоинты списков возвращают не более **100 записей на страницу**. Если ответ содержит `\"offset\": \"...\"`, передайте его обратно в следующем вызове. Выполняйте цикл, пока поле отсутствует:
[code] 
    OFFSET=""  
    while :; do  
      URL=\"https://api.airtable.com/v0/$BASE_ID/$TABLE?pageSize=100\"  
      [ -n \"$OFFSET\" ] && URL=\"$URL&offset=$OFFSET\"  
      RESP=$(curl -s \"$URL\" -H \"Authorization: Bearer $AIRTABLE_API_KEY\")  
      echo \"$RESP\" | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(r[\"id\"], r[\"fields\"].get(\"Name\",\"\")) for r in d[\"records\"]]'  
      OFFSET=$(echo \"$RESP\" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get(\"offset\",\"\"))')  
      [ -z \"$OFFSET\" ] && break  
    done  
    
[/code]
## Типичный рабочий процесс в Hermes[​](<#typical-hermes-workflow> "Прямая ссылка на Типичный рабочий процесс в Hermes")
  1. **Подтвердите авторизацию.** `curl -s -o /dev/null -w \"%{http_code}\\n\" https://api.airtable.com/v0/meta/bases -H \"Authorization: Bearer $AIRTABLE_API_KEY\"` — ожидайте `200`.
  2. **Найдите базу.** Выведите список баз (шаг выше) ИЛИ спросите у пользователя ID вида `app...` напрямую, если у токена нет разрешения `schema.bases:read`.
  3. **Изучите схему.** `GET /v0/meta/bases/$BASE_ID/tables` — сохраните точные названия полей и название первичного поля локально в сессии перед любыми изменениями.
  4. **Сначала читайте, потом пишите.** Для «обнови X, где Y» сначала используйте `filterByFormula`, чтобы получить ID записи `rec...`, затем `PATCH /v0/$BASE_ID/$TABLE/$RECORD_ID`. Никогда не угадывайте ID записей.
  5. **Пакетная запись.** Объединяйте связанные создания в один POST на 10 записей, чтобы оставаться в рамках бюджета 5 запросов/сек.
  6. **Деструктивные операции.** Удаления невозможно отменить через API. Если пользователь говорит «удали все X», выведите обратно фильтр и количество записей и запросите подтверждение перед выполнением.


## Подводные камни[​](<#pitfalls> "Прямая ссылка на Подводные камни")
  * **`filterByFormula` ОБЯЗАТЕЛЬНО должен быть URL-закодирован.** Названия полей с пробелами или не-ASCII символами также требуют кодирования (`{My Field}` → `%7BMy%20Field%7D`). Используйте стандартную библиотеку Python (шаблон выше) — никогда не экранируйте вручную.
  * **Пустые поля опускаются в ответах.** Отсутствие ключа `\"Assignee\"` не означает, что поля не существует — это значит, что значение данной записи пусто. Проверьте схему (шаг 3), прежде чем делать вывод об отсутствии поля.
  * **PATCH vs PUT.** `PATCH` объединяет переданные поля с записью. `PUT` полностью заменяет запись и очищает любое поле, которое вы не включили. По умолчанию используйте `PATCH`.
  * **Варианты одиночного выбора должны существовать.** Запись `\"Status\": \"Shipping\"`, когда `Shipping` нет в списке вариантов поля, вызовет ошибку `INVALID_MULTIPLE_CHOICE_OPTIONS`, если не передать `\"typecast\": true` (который автоматически создаст вариант).
  * **Область действия токена привязана к базе.** Если на одной базе `403`, а на другой работает, это означает, что база не добавлена в список Access токена — а не проблема с разрешениями или авторизацией. Отправьте пользователя на <https://airtable.com/create/tokens>, чтобы добавить её.
  * **Лимиты запросов действуют на базу, а не на токен.** 5 запросов/сек на `baseA` и 5 запросов/сек на `baseB` — нормально; 6 запросов/сек только на `baseA` будут ограничены. Следите за заголовком `Retry-After` при `429`.


## Важные замечания для Hermes[​](<#important-notes-for-hermes> "Прямая ссылка на Важные замечания для Hermes")
  * **Всегда используйте инструмент`terminal` с `curl`.** НЕ используйте `web_extract` (он не может отправлять заголовки авторизации) или `browser_navigate` (требует авторизации в UI и медленный).
  * **`AIRTABLE_API_KEY` автоматически передаётся из `~/.hermes/.env` в подпроцесс** при загрузке этого навыка — не нужно повторно экспортировать его перед каждым вызовом `curl`.
  * **Экранируйте фигурные скобки в формулах внимательно.** В теле heredoc `{Status}` — литерал. В аргументе оболочки `{Status}` безопасен вне контекста подстановки `{...}` — но передавайте динамические строки через `python3 urllib.parse.quote` перед вставкой в URL.
  * **Используйте `python3 -m json.tool`** (всегда доступен) вместо `jq` (опционально). Прибегайте к `jq` только когда нужна фильтрация или проекция.
  * **Пагинация постраничная, а не глобальная.** Лимит Airtable в 100 записей — жёсткое ограничение; увеличить его нельзя. Выполняйте цикл с `offset`, пока поле не исчезнет.
  * **Читайте массив`errors`** в ответах с кодом не 2xx — Airtable возвращает структурированные коды ошибок, такие как `AUTHENTICATION_REQUIRED`, `INVALID_PERMISSIONS`, `MODEL_ID_NOT_FOUND`, `INVALID_MULTIPLE_CHOICE_OPTIONS`, которые точно указывают на проблему.


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
  * [Основы API](<#api-basics>)
  * [Типы полей (формы тела запроса)](<#field-types-request-body-shapes>)
  * [Часто используемые запросы](<#common-queries>)
    * [Список баз, доступных токену](<#list-bases-the-token-can-see>)
    * [Список таблиц и схемы для базы](<#list-tables--schema-for-a-base>)
    * [Список записей (первые 10)](<#list-records-first-10>)
    * [Получение одной записи](<#get-a-single-record>)
    * [Фильтрация записей (filterByFormula)](<#filter-records-filterbyformula>)
    * [Сортировка и выбор определённых полей](<#sort--select-specific-fields>)
    * [Использование именованного представления](<#use-a-named-view>)
  * [Часто используемые изменения](<#common-mutations>)
    * [Создание записи](<#create-a-record>)
    * [Создание до 10 записей за один вызов](<#create-up-to-10-records-in-one-call>)
    * [Обновление записи (PATCH — объединяет, сохраняет неизменённые поля)](<#update-a-record-patch--merges-preserves-unchanged-fields>)
    * [Апсерт по полю слияния (ID не требуется)](<#upsert-by-a-merge-field-no-id-needed>)
    * [Удаление записи](<#delete-a-record>)
    * [Удаление до 10 записей за один вызов](<#delete-up-to-10-records-in-one-call>)
  * [Пагинация](<#pagination>)
  * [Типичный рабочий процесс в Hermes](<#typical-hermes-workflow>)
  * [Подводные камни](<#pitfalls>)
  * [Важные замечания для Hermes](<#important-notes-for-hermes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-airtable -->
