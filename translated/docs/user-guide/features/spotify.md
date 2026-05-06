На этой странице
Hermes может напрямую управлять Spotify — воспроизведением, очередью, поиском, плейлистами, сохранёнными треками/альбомами и историей прослушивания — используя официальный Spotify Web API с PKCE OAuth. Токены сохраняются в `~/.hermes/auth.json` и автоматически обновляются при 401; вам нужно войти только один раз на каждом устройстве.
В отличие от встроенных OAuth-интеграций Hermes (Google, GitHub Copilot, Codex), Spotify требует от каждого пользователя регистрации собственного лёгкого приложения разработчика. Spotify не позволяет третьим лицам публиковать общедоступное OAuth-приложение. Это занимает около двух минут, и `hermes auth spotify` проведёт вас через весь процесс.
## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")
  * Учётная запись Spotify. **Бесплатная** работает для поиска, плейлистов, библиотеки и активности. **Premium** требуется для управления воспроизведением (воспроизведение, пауза, пропуск, перемотка, громкость, добавление в очередь, передача).
  * Hermes Agent установлен и запущен.
  * Для инструментов управления воспроизведением: **активное устройство Spotify Connect** — приложение Spotify должно быть открыто хотя бы на одном устройстве (телефон, ПК, веб-плеер, колонка), чтобы Web API было чем управлять. Если ничего не активно, вы получите `403 Forbidden` с сообщением «no active device»; откройте Spotify на любом устройстве и повторите попытку.


## Настройка[​](<#setup> "Direct link to Setup")
### Один шаг: `hermes tools`[​](<#one-shot-hermes-tools> "Direct link to one-shot-hermes-tools")
Самый быстрый путь. Выполните:
[code] 
    hermes tools  
    
[/code]
Прокрутите до `🎵 Spotify`, нажмите пробел, чтобы включить, затем `s` для сохранения. Hermes сразу переведёт вас в поток OAuth — если у вас ещё нет приложения Spotify, он проведёт вас через его создание. После завершения набор инструментов будет включён И аутентифицирован за один проход.
Если вы предпочитаете выполнять шаги отдельно (или перенастраиваете аутентификацию позже), используйте двухшаговый поток ниже.
### Двухшаговый поток[​](<#two-step-flow> "Direct link to Two-step flow")
#### 1\\. Включение набора инструментов[​](<#1-enable-the-toolset> "Direct link to 1. Enable the toolset")
[code] 
    hermes tools  
    
[/code]
Включите `🎵 Spotify`, сохраните, и когда откроется встроенный мастер, закройте его (Ctrl+C). Набор инструментов останется включённым; этап аутентификации будет отложен.
#### 2\\. Запуск мастера входа[​](<#2-run-the-login-wizard> "Direct link to 2. Run the login wizard")
[code] 
    hermes auth spotify  
    
[/code]
7 инструментов Spotify появляются в наборе инструментов агента только после шага 1 — они отключены по умолчанию, чтобы пользователи, которым они не нужны, не отправляли лишние схемы инструментов с каждым API-запросом.
Если `HERMES_SPOTIFY_CLIENT_ID` не задан, Hermes проводит вас через регистрацию приложения:
  1. Открывает `https://developer.spotify.com/dashboard` в вашем браузере
  2. Выводит точные значения для вставки в форму Spotify «Create app»
  3. Запрашивает Client ID, который вы получите
  4. Сохраняет его в `~/.hermes/.env`, чтобы будущие запуски пропускали этот шаг
  5. Продолжает сразу к потоку согласия OAuth


После подтверждения токены записываются в `providers.spotify` в `~/.hermes/auth.json`. Активный провайдер вывода НЕ меняется — аутентификация Spotify независима от вашего LLM-провайдера.
### Создание приложения Spotify (что запрашивает мастер)[​](<#creating-the-spotify-app-what-the-wizard-asks-for> "Direct link to Creating the Spotify app (what the wizard asks for)")
Когда панель управления откроется, нажмите **Create app** и заполните:
Поле| Значение  
---|---  
Название приложения| любое (например, `hermes-agent`)  
Описание приложения| любое (например, `personal Hermes integration`)  
Веб-сайт| оставьте пустым  
Redirect URI| `http://127.0.0.1:43827/spotify/callback`  
Какие API/SDK?| отметьте **Web API**  
Примите условия и нажмите **Save**. На следующей странице нажмите **Settings** → скопируйте **Client ID** и вставьте его в запрос Hermes. Это единственное значение, которое нужно Hermes — PKCE не использует секрет клиента.
### Работа через SSH / в безголовом окружении[​](<#running-over-ssh--in-a-headless-environment> "Direct link to Running over SSH / in a headless environment")
Если установлены `SSH_CLIENT` или `SSH_TTY`, Hermes пропускает автоматическое открытие браузера как во время мастера, так и на этапе OAuth. Скопируйте URL панели управления и URL авторизации, которые выведет Hermes, откройте их в браузере на вашем локальном компьютере и действуйте как обычно — локальный HTTP-слушатель всё ещё работает на удалённом хосте на порту 43827. Если вам нужно подключиться через SSH-туннель, пробросьте этот порт: `ssh -L 43827:127.0.0.1:43827 remote`.
## Проверка[​](<#verify> "Direct link to Verify")
[code] 
    hermes auth status spotify  
    
[/code]
Показывает, присутствуют ли токены и когда истекает срок действия токена доступа. Обновление происходит автоматически: когда любой API-запрос к Spotify возвращает 401, клиент обменивает токен обновления и повторяет попытку один раз. Токены обновления сохраняются между перезапусками Hermes, так что повторная аутентификация нужна только если вы отзовёте приложение в настройках учётной записи Spotify или выполните `hermes auth logout spotify`.
## Использование[​](<#using-it> "Direct link to Using it")
После входа в систему агент получает доступ к 7 инструментам Spotify. Общайтесь с агентом естественным языком — он выберет подходящий инструмент и действие. Для наилучшей работы агент загружает сопутствующий скилл, который обучает каноническим шаблонам использования (поиск-затем-воспроизведение, когда не нужно предварительно вызывать `get_state` и т.д.).
[code] 
    > play some miles davis  
    > what am I listening to  
    > add this track to my Late Night Jazz playlist  
    > skip to the next song  
    > make a new playlist called "Focus 2026" and add the last three songs I played  
    > which of my saved albums are by Radiohead  
    > search for acoustic covers of Blackbird  
    > transfer playback to my kitchen speaker  
    
[/code]
### Справочник инструментов[​](<#tool-reference> "Direct link to Tool reference")
Все действия, изменяющие воспроизведение, принимают опциональный `device_id` для указания конкретного устройства. Если он опущен, Spotify использует текущее активное устройство.
#### `spotify_playback`[​](<#spotify_playback> "Direct link to spotify_playback")
Управление и просмотр воспроизведения, а также получение истории недавно прослушанного.
Действие| Назначение| Premium?  
---|---|---  
`get_state`| Полное состояние воспроизведения (трек, устройство, прогресс, перемешивание/повтор)| Нет  
`get_currently_playing`| Только текущий трек (возвращает пустой результат при 204 — см. ниже)| Нет  
`play`| Запуск/возобновление воспроизведения. Опционально: `context_uri`, `uris`, `offset`, `position_ms`| Да  
`pause`| Пауза воспроизведения| Да  
`next` / `previous`| Пропуск трека| Да  
`seek`| Переход к `position_ms`| Да  
`set_repeat`| `state` = `track` / `context` / `off`| Да  
`set_shuffle`| `state` = `true` / `false`| Да  
`set_volume`| `volume_percent` = 0–100| Да  
`recently_played`| Последние прослушанные треки. Опционально: `limit`, `before`, `after` (в миллисекундах Unix)| Нет  
#### `spotify_devices`[​](<#spotify_devices> "Direct link to spotify_devices")
Действие| Назначение  
---|---  
`list`| Все устройства Spotify Connect, видимые для вашей учётной записи  
`transfer`| Перенос воспроизведения на `device_id`. Опционально `play: true` запускает воспроизведение при переносе  
#### `spotify_queue`[​](<#spotify_queue> "Direct link to spotify_queue")
Действие| Назначение| Premium?  
---|---|---  
`get`| Текущие треки в очереди| Нет  
`add`| Добавить `uri` в очередь| Да  
#### `spotify_search`[​](<#spotify_search> "Direct link to spotify_search")
Поиск по каталогу. `query` обязателен. Опционально: `types` (массив из `track` / `album` / `artist` / `playlist` / `show` / `episode`), `limit`, `offset`, `market`.
#### `spotify_playlists`[​](<#spotify_playlists> "Direct link to spotify_playlists")
Действие| Назначение| Обязательные аргументы  
---|---|---  
`list`| Плейлисты пользователя| —  
`get`| Один плейлист + треки| `playlist_id`  
`create`| Новый плейлист| `name` (+ опционально `description`, `public`, `collaborative`)  
`add_items`| Добавить треки| `playlist_id`, `uris` (опционально `position`)  
`remove_items`| Удалить треки| `playlist_id`, `uris` (+ опционально `snapshot_id`)  
`update_details`| Переименовать / редактировать| `playlist_id` + любое из `name`, `description`, `public`, `collaborative`  
#### `spotify_albums`[​](<#spotify_albums> "Direct link to spotify_albums")
Действие| Назначение| Обязательные аргументы  
---|---|---  
`get`| Метаданные альбома| `album_id`  
`tracks`| Список треков альбома| `album_id`  
#### `spotify_library`[​](<#spotify_library> "Direct link to spotify_library")
Единый доступ к сохранённым трекам и сохранённым альбомам. Выберите коллекцию с помощью аргумента `kind`.
Действие| Назначение  
---|---  
`list`| Постраничный список библиотеки  
`save`| Добавить `ids` / `uris` в библиотеку  
`remove`| Удалить `ids` / `uris` из библиотеки  
Обязательно: `kind` = `tracks` или `albums`, плюс `action`.
### Таблица возможностей: Free vs Premium[​](<#feature-matrix-free-vs-premium> "Direct link to Feature matrix: Free vs Premium")
Инструменты только для чтения работают с бесплатными аккаунтами. Всё, что изменяет воспроизведение или очередь, требует Premium.
Работает с Free| Требуется Premium  
---|---  
`spotify_search` (всё)| `spotify_playback` — play, pause, next, previous, seek, set_repeat, set_shuffle, set_volume  
`spotify_playback` — get_state, get_currently_playing, recently_played| `spotify_queue` — add  
`spotify_devices` — list| `spotify_devices` — transfer  
`spotify_queue` — get|  
`spotify_playlists` (всё)|  
`spotify_albums` (всё)|  
`spotify_library` (всё)|  
## Планирование: Spotify + cron[​](<#scheduling-spotify--cron> "Direct link to Scheduling: Spotify + cron")
Поскольку инструменты Spotify — это обычные инструменты Hermes, задача cron, запущенная в сессии Hermes, может запускать воспроизведение по любому расписанию. Новый код не требуется.
### Утренний плейлист для пробуждения[​](<#morning-wake-up-playlist> "Direct link to Morning wake-up playlist")
[code] 
    hermes cron add \  
      --name "morning-commute" \  
      "0 7 * * 1-5" \  
      "Transfer playback to my kitchen speaker and start my 'Morning Commute' playlist. Volume to 40. Shuffle on."  
    
[/code]
Что произойдёт в 7 утра каждый будний день:
  1. Cron запускает безголовую сессию Hermes.
  2. Агент читает запрос, вызывает `spotify_devices list` для поиска «kitchen speaker» по имени, затем `spotify_devices transfer` → `spotify_playback set_volume` → `spotify_playback set_shuffle` → `spotify_search` + `spotify_playback play`.
  3. Музыка начинается на целевой колонке. Итого: одна сессия, несколько вызовов инструментов, без участия человека.


### Расслабление вечером[​](<#wind-down-at-night> "Direct link to Wind-down at night")
[code] 
    hermes cron add \  
      --name "wind-down" \  
      "30 22 * * *" \  
      "Pause Spotify. Then set volume to 20 so it's quiet when I start it again tomorrow."  
    
[/code]
### Особенности[​](<#gotchas> "Direct link to Gotchas")
  * **На момент срабатывания cron должно быть активно устройство.** Если ни один клиент Spotify не запущен (телефон/ПК/колонка Connect), действия с воспроизведением вернут `403 no active device`. Для утренних плейлистов рекомендуем указывать устройство, которое всегда включено (Sonos, Echo, умная колонка), а не телефон.
  * **Premium требуется для всего, что изменяет воспроизведение** — play, pause, skip, volume, transfer. Задачи cron только для чтения (например, «отправь мне по email мои недавно прослушанные треки») отлично работают с Free.
  * **Агент cron наследует ваши активные наборы инструментов.** Spotify должен быть включён в `hermes tools`, чтобы сессия cron видела инструменты Spotify.
  * **Задачи cron выполняются с `skip_memory=True`**, поэтому они не записывают данные в ваше хранилище памяти.


Полный справочник по cron: [Cron Jobs](</docs/user-guide/features/cron>).
## Выход[​](<#sign-out> "Direct link to Sign out")
[code] 
    hermes auth logout spotify  
    
[/code]
Удаляет токены из `~/.hermes/auth.json`. Чтобы также очистить конфигурацию приложения, удалите `HERMES_SPOTIFY_CLIENT_ID` (и `HERMES_SPOTIFY_REDIRECT_URI`, если вы его задавали) из `~/.hermes/.env` или запустите мастер заново.
Чтобы отозвать приложение на стороне Spotify, перейдите в [Приложения, подключённые к вашей учётной записи](<https://www.spotify.com/account/apps/>) и нажмите **REMOVE ACCESS**.
## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")
**`403 Forbidden — Player command failed: No active device found`** — Необходимо, чтобы Spotify был запущен хотя бы на одном устройстве. Откройте приложение Spotify на телефоне, ПК или веб-плеере, запустите любой трек на секунду, чтобы зарегистрировать устройство, и повторите попытку. `spotify_devices list` показывает, что сейчас видно.
**`403 Forbidden — Premium required`** — У вас бесплатный аккаунт, и вы пытаетесь выполнить действие, изменяющее воспроизведение. См. таблицу возможностей выше.
**`204 No Content` при `get_currently_playing`** — на данный момент ничего не воспроизводится ни на одном устройстве. Это нормальный ответ Spotify, а не ошибка; Hermes отображает его как пустой результат с пояснением (`is_playing: false`).
**`INVALID_CLIENT: Invalid redirect URI`** — URI перенаправления в настройках вашего приложения Spotify не совпадает с тем, что использует Hermes. По умолчанию используется `http://127.0.0.1:43827/spotify/callback`. Либо добавьте этот URI в список разрешённых в настройках приложения, либо задайте `HERMES_SPOTIFY_REDIRECT_URI` в `~/.hermes/.env` в соответствии с тем, что вы зарегистрировали.
**`429 Too Many Requests`** — Ограничение скорости запросов Spotify. Hermes возвращает понятную ошибку; подождите минуту и повторите. Если это повторяется, вероятно, вы запустили密集ный цикл в скрипте — квота Spotify сбрасывается примерно каждые 30 секунд.
**`401 Unauthorized` повторяется постоянно** — Ваш токен обновления был отозван (обычно из-за того, что вы удалили приложение из учётной записи или приложение было удалено). Выполните `hermes auth spotify` снова.
**Мастер не открывает браузер** — Если вы работаете через SSH или в контейнере без дисплея, Hermes обнаруживает это и пропускает автоматическое открытие. Скопируйте URL панели управления, который он выводит, и откройте его вручную.
## Расширенное: собственные области доступа[​](<#advanced-custom-scopes> "Direct link to Advanced: custom scopes")
По умолчанию Hermes запрашивает области доступа, необходимые для всех поставляемых инструментов. Измените, если хотите ограничить доступ:
[code] 
    hermes auth spotify --scope "user-read-playback-state user-modify-playback-state playlist-read-private"  
    
[/code]
Справочник по областям доступа: [Scopes Spotify Web API](<https://developer.spotify.com/documentation/web-api/concepts/scopes>). Если вы запросите меньше областей, чем нужно инструменту, вызовы этого инструмента будут завершаться с ошибкой 403.
## Расширенное: собственный Client ID / Redirect URI[​](<#advanced-custom-client-id--redirect-uri> "Direct link to Advanced: custom client ID / redirect URI")
[code] 
    hermes auth spotify --client-id <id> --redirect-uri http://localhost:3000/callback  
    
[/code]
Или установите их постоянно в `~/.hermes/.env`:
[code] 
    HERMES_SPOTIFY_CLIENT_ID=<your_id>  
    HERMES_SPOTIFY_REDIRECT_URI=http://localhost:3000/callback  
    
[/code]
URI перенаправления должен быть добавлен в белый список в настройках вашего приложения Spotify. Значение по умолчанию подходит почти всем — меняйте его, только если порт 43827 занят.
## Где что находится[​](<#where-things-live> "Direct link to Where things live")
Файл| Содержимое  
---|---  
`~/.hermes/auth.json` → `providers.spotify`| токен доступа, токен обновления, срок действия, область доступа, URI перенаправления  
`~/.hermes/.env`| `HERMES_SPOTIFY_CLIENT_ID`, опционально `HERMES_SPOTIFY_REDIRECT_URI`  
Приложение Spotify| принадлежит вам на [developer.spotify.com/dashboard](<https://developer.spotify.com/dashboard>); содержит Client ID и список разрешённых URI перенаправления  
  * [Предварительные требования](<#prerequisites>)
  * [Настройка](<#setup>)
    * [Один шаг: `hermes tools`](<#one-shot-hermes-tools>)
    * [Двухшаговый поток](<#two-step-flow>)
    * [Создание приложения Spotify (что запрашивает мастер)](<#creating-the-spotify-app-what-the-wizard-asks-for>)
    * [Работа через SSH / в безголовом окружении](<#running-over-ssh--in-a-headless-environment>)
  * [Проверка](<#verify>)
  * [Использование](<#using-it>)
    * [Справочник инструментов](<#tool-reference>)
    * [Таблица возможностей: Free vs Premium](<#feature-matrix-free-vs-premium>)
  * [Планирование: Spotify + cron](<#scheduling-spotify--cron>)
    * [Утренний плейлист для пробуждения](<#morning-wake-up-playlist>)
    * [Расслабление вечером](<#wind-down-at-night>)
    * [Особенности](<#gotchas>)
  * [Выход](<#sign-out>)
  * [Устранение неполадок](<#troubleshooting>)
  * [Расширенное: собственные области доступа](<#advanced-custom-scopes>)
  * [Расширенное: собственный Client ID / Redirect URI](<#advanced-custom-client-id--redirect-uri>)
  * [Где что находится](<#where-things-live>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/spotify -->
