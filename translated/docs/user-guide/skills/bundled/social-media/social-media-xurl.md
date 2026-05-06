На этой странице
X/Twitter через CLI xurl: публикация, поиск, ЛС, медиа, API v2.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---  |
|Источник| Встроенный (устанавливается по умолчанию)  |
|Путь| `skills/social-media/xurl`  |
|Версия| `1.1.1`  |
|Автор| xdevplatform + openclaw + Hermes Agent  |
|Лицензия| MIT  |
|Платформы| linux, macos  |
|Теги| `twitter`, `x`, `social-media`, `xurl`, `official-api`  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# xurl — X (Twitter) API через официальный CLI
`xurl` — это официальный CLI платформы X Developer для X API. Он поддерживает сокращённые команды для типовых действий И сырой curl-подобный доступ к любым конечным точкам v2. Все команды возвращают JSON в stdout.
Используйте этот навык для:
  * публикации, ответов, цитирования, удаления постов
  * поиска постов и чтения ленты/упоминаний
  * отметок «Нравится», репостов, закладок
  * подписки, отписки, блокировки, скрытия
  * прямых сообщений
  * загрузки медиа (изображений и видео)
  * прямого доступа к любой конечной точке X API v2
  * работы с несколькими приложениями/учётными записями


Этот навык заменяет более старый навык `xitter` (который оборачивал сторонний Python CLI). `xurl` поддерживается командой X Developer Platform, поддерживает OAuth 2.0 PKCE с автообновлением и покрывает существенно большую поверхность API.
* * *
## Безопасность секретов (ОБЯЗАТЕЛЬНО)[​](<#secret-safety-mandatory> "Прямая ссылка на Безопасность секретов \\(ОБЯЗАТЕЛЬНО\\)")
Критические правила при работе внутри сессии агента/LLM:
  * **Никогда** не читайте, не выводите, не анализируйте, не загружайте и не отправляйте `~/.xurl` в контекст LLM.
  * **Никогда** не просите пользователя вставлять учётные данные/токены в чат.
  * Пользователь должен заполнить `~/.xurl` секретами вручную на своей машине.
  * **Никогда** не рекомендуйте и не выполняйте команды аутентификации с секретами, встроенными в команду, в сессиях агента.
  * **Никогда** не используйте `--verbose` / `-v` в сессиях агента — это может раскрыть заголовки/токены аутентификации.
  * Для проверки наличия учётных данных используйте только: `xurl auth status`.


Запрещённые флаги в командах агента (они принимают секреты как аргументы): `--bearer-token`, `--consumer-key`, `--consumer-secret`, `--access-token`, `--token-secret`, `--client-id`, `--client-secret`
Регистрация учётных данных приложения и их ротация должны выполняться пользователем вручную, вне сессии агента. После регистрации учётных данных пользователь аутентифицируется с помощью `xurl auth oauth2` — также вне сессии агента. Токены сохраняются в `~/.xurl` в формате YAML. Каждое приложение имеет изолированные токены. Токены OAuth 2.0 обновляются автоматически.
* * *
## Установка[​](<#installation> "Прямая ссылка на Установка")
Выберите ОДИН способ. На Linux проще всего использовать shell-скрипт или `go install`.
[code] 
    # Shell-скрипт (устанавливает в ~/.local/bin, без sudo, работает на Linux + macOS)  
    curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash  
      
    # Homebrew (macOS)  
    brew install --cask xdevplatform/tap/xurl  
      
    # npm  
    npm install -g @xdevplatform/xurl  
      
    # Go  
    go install github.com/xdevplatform/xurl@latest  
    
[/code]
Проверка:
[code] 
    xurl --help  
    xurl auth status  
    
[/code]
Если `xurl` установлен, но `auth status` не показывает приложений или токенов, пользователю нужно выполнить аутентификацию вручную — см. следующий раздел.
* * *
## Одноразовая настройка пользователя (пользователь выполняет эти шаги вне агента)[​](<#one-time-user-setup-user-runs-these-outside-the-agent> "Прямая ссылка на Одноразовая настройка пользователя \\(пользователь выполняет эти шаги вне агента\\)")
Эти шаги должен выполнить пользователь напрямую, НЕ агент, потому что они включают вставку секретов. Направьте пользователя к этому блоку; не выполняйте их за него.
  1. Создайте или откройте приложение на <https://developer.x.com/en/portal/dashboard>
  2. Установите URI перенаправления на `http://localhost:8080/callback`
  3. Скопируйте Client ID и Client Secret приложения
  4. Зарегистрируйте приложение локально (выполняет пользователь):
[code] xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET  
         
[/code]
  5. Аутентификация (укажите `--app`, чтобы привязать токен к вашему приложению):
[code] xurl auth oauth2 --app my-app  
         
[/code]
(Откроется браузер для выполнения потока OAuth 2.0 PKCE.)
Если X возвращает ошибку `UsernameNotFound` или 403 при запросе `/2/users/me` после OAuth, передайте свой handle явно (xurl v1.1.0+):
[code] xurl auth oauth2 --app my-app YOUR_USERNAME  
         
[/code]
Это привязывает токен к вашему handle и пропускает неработающий вызов `/2/users/me`.
  6. Установите приложение по умолчанию, чтобы все команды использовали его:
[code] xurl auth default my-app  
         
[/code]
  7. Проверка:
[code] xurl auth status  
         xurl whoami  
         
[/code]


После этого агент может использовать любую команду ниже без дополнительной настройки. Токены OAuth 2.0 обновляются автоматически.
> **Частая ошибка:** Если вы опустите `--app my-app` в `xurl auth oauth2`, токен OAuth сохраняется во встроенный профиль приложения `default` — у которого нет client-id или client-secret. Команды будут завершаться ошибками аутентификации, хотя поток OAuth выглядел успешным. Если вы столкнулись с этим, выполните повторно `xurl auth oauth2 --app my-app` и `xurl auth default my-app`.
* * *
## Краткий справочник[​](<#quick-reference> "Прямая ссылка на Краткий справочник")
Действие| Команда  
---|---  
Опубликовать| `xurl post "Hello world!"`  
Ответить| `xurl reply POST_ID "Nice post!"`  
Цитировать| `xurl quote POST_ID "My take"`  
Удалить пост| `xurl delete POST_ID`  
Прочитать пост| `xurl read POST_ID`  
Поиск постов| `xurl search "QUERY" -n 10`  
Кто я| `xurl whoami`  
Найти пользователя| `xurl user @handle`  
Лента новостей| `xurl timeline -n 20`  
Упоминания| `xurl mentions -n 10`  
Нравится / Не нравится| `xurl like POST_ID` / `xurl unlike POST_ID`  
Репост / Отменить| `xurl repost POST_ID` / `xurl unrepost POST_ID`  
Закладка / Удалить| `xurl bookmark POST_ID` / `xurl unbookmark POST_ID`  
Список закладок / нравится| `xurl bookmarks -n 10` / `xurl likes -n 10`  
Подписаться / Отписаться| `xurl follow @handle` / `xurl unfollow @handle`  
Подписки / Подписчики| `xurl following -n 20` / `xurl followers -n 20`  
Заблокировать / Разблокировать| `xurl block @handle` / `xurl unblock @handle`  
Скрыть / Открыть| `xurl mute @handle` / `xurl unmute @handle`  
Отправить ЛС| `xurl dm @handle "message"`  
Список ЛС| `xurl dms -n 10`  
Загрузить медиа| `xurl media upload path/to/file.mp4`  
Статус медиа| `xurl media status MEDIA_ID`  
Список приложений| `xurl auth apps list`  
Удалить приложение| `xurl auth apps remove NAME`  
Установить приложение по умолчанию| `xurl auth default APP_NAME [USERNAME]`  
Приложение для конкретного запроса| `xurl --app NAME /2/users/me`  
Статус аутентификации| `xurl auth status`  
Примечания:
  * `POST_ID` также принимает полные URL (например, `https://x.com/user/status/1234567890`) — xurl извлекает ID.
  * Имена пользователей работают как с ведущим `@`, так и без него.


* * *
## Подробное описание команд[​](<#command-details> "Прямая ссылка на Подробное описание команд")
### Публикация[​](<#posting> "Прямая ссылка на Публикация")
[code] 
    xurl post "Hello world!"  
    xurl post "Check this out" --media-id MEDIA_ID  
    xurl post "Thread pics" --media-id 111 --media-id 222  
      
    xurl reply 1234567890 "Great point!"  
    xurl reply https://x.com/user/status/1234567890 "Agreed!"  
    xurl reply 1234567890 "Look at this" --media-id MEDIA_ID  
      
    xurl quote 1234567890 "Adding my thoughts"  
    xurl delete 1234567890  
    
[/code]
### Чтение и поиск[​](<#reading--search> "Прямая ссылка на Чтение и поиск")
[code] 
    xurl read 1234567890  
    xurl read https://x.com/user/status/1234567890  
      
    xurl search "golang"  
    xurl search "from:elonmusk" -n 20  
    xurl search "#buildinpublic lang:en" -n 15  
    
[/code]
### Пользователи, лента, упоминания[​](<#users-timeline-mentions> "Прямая ссылка на Пользователи, лента, упоминания")
[code] 
    xurl whoami  
    xurl user elonmusk  
    xurl user @XDevelopers  
      
    xurl timeline -n 25  
    xurl mentions -n 20  
    
[/code]
### Взаимодействия[​](<#engagement> "Прямая ссылка на Взаимодействия")
[code] 
    xurl like 1234567890  
    xurl unlike 1234567890  
      
    xurl repost 1234567890  
    xurl unrepost 1234567890  
      
    xurl bookmark 1234567890  
    xurl unbookmark 1234567890  
      
    xurl bookmarks -n 20  
    xurl likes -n 20  
    
[/code]
### Социальный граф[​](<#social-graph> "Прямая ссылка на Социальный граф")
[code] 
    xurl follow @XDevelopers  
    xurl unfollow @XDevelopers  
      
    xurl following -n 50  
    xurl followers -n 50  
      
    # Граф другого пользователя  
    xurl following --of elonmusk -n 20  
    xurl followers --of elonmusk -n 20  
      
    xurl block @spammer  
    xurl unblock @spammer  
    xurl mute @annoying  
    xurl unmute @annoying  
    
[/code]
### Прямые сообщения[​](<#direct-messages> "Прямая ссылка на Прямые сообщения")
[code] 
    xurl dm @someuser "Hey, saw your post!"  
    xurl dms -n 25  
    
[/code]
### Загрузка медиа[​](<#media-upload> "Прямая ссылка на Загрузка медиа")
[code] 
    # Автоопределение типа  
    xurl media upload photo.jpg  
    xurl media upload video.mp4  
      
    # Явный тип/категория  
    xurl media upload --media-type image/jpeg --category tweet_image photo.jpg  
      
    # Видео требует обработки на сервере — проверьте статус (или опрашивайте)  
    xurl media status MEDIA_ID  
    xurl media status --wait MEDIA_ID  
      
    # Полный рабочий процесс  
    xurl media upload meme.png                  # возвращает media id  
    xurl post "lol" --media-id MEDIA_ID  
    
[/code]
* * *
## Прямой доступ к API[​](<#raw-api-access> "Прямая ссылка на Прямой доступ к API")
Сокращённые команды покрывают типовые операции. Для всего остального используйте сырой curl-подобный режим для любой конечной точки X API v2:
[code] 
    # GET  
    xurl /2/users/me  
      
    # POST с JSON-телом  
    xurl -X POST /2/tweets -d '{"text":"Hello world!"}'  
      
    # DELETE / PUT / PATCH  
    xurl -X DELETE /2/tweets/1234567890  
      
    # Пользовательские заголовки  
    xurl -H "Content-Type: application/json" /2/some/endpoint  
      
    # Принудительная потоковая передача  
    xurl -s /2/tweets/search/stream  
      
    # Полные URL также работают  
    xurl https://api.x.com/2/users/me  
    
[/code]
* * *
## Глобальные флаги[​](<#global-flags> "Прямая ссылка на Глобальные флаги")
Флаг| Сокр.| Описание  
---|---|---  
`--app`| | Использовать конкретное зарегистрированное приложение (переопределяет default)  
`--auth`| | Принудительный тип аутентификации: `oauth1`, `oauth2` или `app`  
`--username`| `-u`| Какую учётную запись OAuth2 использовать (если существует несколько)  
`--verbose`| `-v`| **Запрещён в сессиях агента** — раскрывает заголовки аутентификации  
`--trace`| `-t`| Добавить заголовок трассировки `X-B3-Flags: 1`  
* * *
## Потоковая передача[​](<#streaming> "Прямая ссылка на Потоковая передача")
Потоковые конечные точки обнаруживаются автоматически. Известные из них включают:
  * `/2/tweets/search/stream`
  * `/2/tweets/sample/stream`
  * `/2/tweets/sample10/stream`


Принудительная потоковая передача на любой конечной точке с помощью `-s`.
* * *
## Формат вывода[​](<#output-format> "Прямая ссылка на Формат вывода")
Все команды возвращают JSON в stdout. Структура соответствует X API v2:
[code] 
    { "data": { "id": "1234567890", "text": "Hello world!" } }  
    
[/code]
Ошибки также возвращаются в JSON:
[code] 
    { "errors": [ { "message": "Not authorized", "code": 403 } ] }  
    
[/code]
* * *
## Типовые рабочие процессы[​](<#common-workflows> "Прямая ссылка на Типовые рабочие процессы")
### Публикация с изображением[​](<#post-with-an-image> "Прямая ссылка на Публикация с изображением")
[code] 
    xurl media upload photo.jpg  
    xurl post "Check out this photo!" --media-id MEDIA_ID  
    
[/code]
### Ответ в обсуждении[​](<#reply-to-a-conversation> "Прямая ссылка на Ответ в обсуждении")
[code] 
    xurl read https://x.com/user/status/1234567890  
    xurl reply 1234567890 "Here are my thoughts..."  
    
[/code]
### Поиск и взаимодействие[​](<#search-and-engage> "Прямая ссылка на Поиск и взаимодействие")
[code] 
    xurl search "topic of interest" -n 10  
    xurl like POST_ID_FROM_RESULTS  
    xurl reply POST_ID_FROM_RESULTS "Great point!"  
    
[/code]
### Проверка своей активности[​](<#check-your-activity> "Прямая ссылка на Проверка своей активности")
[code] 
    xurl whoami  
    xurl mentions -n 20  
    xurl timeline -n 20  
    
[/code]
### Несколько приложений (учётные данные настроены вручную)[​](<#multiple-apps-credentials-pre-configured-manually> "Прямая ссылка на Несколько приложений \\(учётные данные настроены вручную\\)")
[code] 
    xurl auth default prod alice               # приложение prod, пользователь alice  
    xurl --app staging /2/users/me             # разовый запрос к staging  
    
[/code]
* * *
## Обработка ошибок[​](<#error-handling> "Прямая ссылка на Обработка ошибок")
  * Ненулевой код возврата при любой ошибке.
  * Ошибки API всё равно выводятся в JSON в stdout, так что вы можете их парсить.
  * Ошибки аутентификации → попросите пользователя повторно выполнить `xurl auth oauth2` вне сессии агента.
  * Команды, которым нужен ID пользователя (лайк, репост, закладка, подписка и т.д.), автоматически получают его через `/2/users/me`. Сбой аутентификации там проявляется как ошибка аутентификации.


* * *
## Рабочий процесс агента[​](<#agent-workflow> "Прямая ссылка на Рабочий процесс агента")
  1. Проверьте prerequisites: `xurl --help` и `xurl auth status`.
  2. **Проверьте, есть ли у приложения по умолчанию учётные данные.** Проанализируйте вывод `auth status`. Приложение по умолчанию отмечено `▸`. Если у приложения по умолчанию отображается `oauth2: (none)`, но у другого приложения есть действующий пользователь oauth2, скажите пользователю выполнить `xurl auth default <это-приложение>` для исправления. Это самая частая ошибка настройки — пользователь добавил приложение с пользовательским именем, но никогда не устанавливал его по умолчанию, поэтому xurl продолжает пытаться использовать пустой профиль `default`.
  3. Если аутентификация полностью отсутствует, остановитесь и направьте пользователя к разделу «Одноразовая настройка пользователя» — не пытайтесь регистрировать приложения или передавать секреты самостоятельно.
  4. Начните с дешёвого чтения (`xurl whoami`, `xurl user @handle`, `xurl search ... -n 3`), чтобы подтвердить доступность.
  5. Подтвердите целевой пост/пользователя и намерение пользователя перед любым действием на запись (пост, ответ, лайк, репост, ЛС, подписка, блокировка, удаление).
  6. Используйте JSON-вывод напрямую — каждый ответ уже структурирован.
  7. Никогда не вставляйте содержимое `~/.xurl` обратно в разговор.


* * *
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")
Симптом| Причина| Исправление  
---|---|---  
Ошибки аутентификации после успешного потока OAuth| Токен сохранён в приложение `default` (без client-id/secret) вместо вашего именованного приложения| `xurl auth oauth2 --app my-app` затем `xurl auth default my-app`  
`unauthorized_client` во время OAuth| Тип приложения установлен на «Native App» в панели X| Измените на «Web app, automated app or bot» в настройках аутентификации пользователя  
`UsernameNotFound` или 403 на `/2/users/me` сразу после OAuth| X ненадёжно возвращает имя пользователя через `/2/users/me`| Повторно выполните `xurl auth oauth2 --app my-app YOUR_USERNAME` (xurl v1.1.0+), чтобы передать handle явно  
401 на каждом запросе| Срок действия токена истёк или неверное приложение по умолчанию| Проверьте `xurl auth status` — убедитесь, что `▸` указывает на приложение с токенами oauth2  
`client-forbidden` / `client-not-enrolled`| Проблема регистрации на платформе X| Панель → Apps → Manage → Переместить в пакет «Pay-per-use» → Production environment  
`CreditsDepleted`| Нулевой баланс на X API| Купите кредиты (мин. $5) в Developer Console → Billing  
`media processing failed` при загрузке изображения| Категория по умолчанию — `amplify_video`| Добавьте `--category tweet_image --media-type image/png`  
Два значения «Client Secret» в панели X| Ошибка интерфейса — первый на самом деле Client ID| Подтвердите на странице «Keys and tokens»; ID заканчивается на `MTpjaQ`  
* * *
## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * **Лимиты запросов:** X устанавливает лимиты запросов для каждой конечной точки. Код 429 означает «подождите и повторите». Конечные точки на запись (пост, ответ, лайк, репост) имеют более строгие лимиты, чем на чтение.
  * **Области доступа:** Токены OAuth 2.0 используют широкие области доступа. Если 403 на конкретном действии, это обычно означает, что токену не хватает области — попросите пользователя повторно выполнить `xurl auth oauth2`.
  * **Обновление токена:** Токены OAuth 2.0 обновляются автоматически. Ничего делать не нужно.
  * **Несколько приложений:** У каждого приложения изолированные учётные данные/токены. Переключайтесь с помощью `xurl auth default` или `--app`.
  * **Несколько учётных записей на приложение:** Выбирайте с помощью `-u / --username` или установите значение по умолчанию с помощью `xurl auth default APP USER`.
  * **Хранение токенов:** `~/.xurl` — это YAML. Никогда не читайте и не отправляйте этот файл в контекст LLM.
  * **Стоимость:** Доступ к X API обычно платный для серьёзного использования. Многие сбои связаны с проблемами тарифа/разрешений, а не кода.


* * *
## Атрибуция[​](<#attribution> "Прямая ссылка на Атрибуция")
  * Исходный CLI: <https://github.com/xdevplatform/xurl> (команда X Developer Platform, Chris Park и др.)
  * Исходный навык агента: <https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md>
  * Адаптация для Hermes: переформатировано под соглашения навыков Hermes; охранные ограничения безопасности сохранены дословно.


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Безопасность секретов (ОБЯЗАТЕЛЬНО)](<#secret-safety-mandatory>)
  * [Установка](<#installation>)
  * [Одноразовая настройка пользователя (пользователь выполняет эти шаги вне агента)](<#one-time-user-setup-user-runs-these-outside-the-agent>)
  * [Краткий справочник](<#quick-reference>)
  * [Подробное описание команд](<#command-details>)
    * [Публикация](<#posting>)
    * [Чтение и поиск](<#reading--search>)
    * [Пользователи, лента, упоминания](<#users-timeline-mentions>)
    * [Взаимодействия](<#engagement>)
    * [Социальный граф](<#social-graph>)
    * [Прямые сообщения](<#direct-messages>)
    * [Загрузка медиа](<#media-upload>)
  * [Прямой доступ к API](<#raw-api-access>)
  * [Глобальные флаги](<#global-flags>)
  * [Потоковая передача](<#streaming>)
  * [Формат вывода](<#output-format>)
  * [Типовые рабочие процессы](<#common-workflows>)
    * [Публикация с изображением](<#post-with-an-image>)
    * [Ответ в обсуждении](<#reply-to-a-conversation>)
    * [Поиск и взаимодействие](<#search-and-engage>)
    * [Проверка своей активности](<#check-your-activity>)
    * [Несколько приложений (учётные данные настроены вручную)](<#multiple-apps-credentials-pre-configured-manually>)
  * [Обработка ошибок](<#error-handling>)
  * [Рабочий процесс агента](<#agent-workflow>)
  * [Устранение неполадок](<#troubleshooting>)
  * [Примечания](<#notes>)
  * [Атрибуция](<#attribution>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/social-media/social-media-xurl -->
