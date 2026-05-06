На этой странице
Мониторинг блогов и RSS/Atom-лент с помощью инструмента blogwatcher-cli.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию)  |
|Путь| `skills/research/blogwatcher` |
|Версия| `2.0.0` |
|Автор| JulienTant (форк Hyaxia/blogwatcher) |
|Лицензия| MIT |
|Теги| `RSS`, `Блоги`, `Читалка-лент`, `Мониторинг` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# Blogwatcher
Отслеживайте обновления блогов и RSS/Atom-лент с помощью инструмента `blogwatcher-cli`. Поддерживает автоматическое обнаружение лент, запасной вариант HTML-скрейпинга, импорт OPML и управление прочитанными/непрочитанными статьями.
## Установка[​](<#installation> "Прямая ссылка на Установка")
Выберите один из способов:
  * **Go:** `go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest`
  * **Docker:** `docker run --rm -v blogwatcher-cli:/data ghcr.io/julientant/blogwatcher-cli`
  * **Бинарный файл (Linux amd64):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  * **Бинарный файл (Linux arm64):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  * **Бинарный файл (macOS Apple Silicon):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  * **Бинарный файл (macOS Intel):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`


Все релизы: <https://github.com/JulienTant/blogwatcher-cli/releases>
### Docker с постоянным хранилищем[​](<#docker-with-persistent-storage> "Прямая ссылка на Docker с постоянным хранилищем")
По умолчанию база данных находится в `~/.blogwatcher-cli/blogwatcher-cli.db`. В Docker она теряется при перезапуске контейнера. Используйте `BLOGWATCHER_DB` или монтирование тома для сохранения данных:
[code] 
    # Именованный том (проще всего)  
    docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan  
      
    # Привязка к папке на хосте  
    docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan  
    
[/code]
### Миграция с оригинального blogwatcher[​](<#migrating-from-the-original-blogwatcher> "Прямая ссылка на Миграция с оригинального blogwatcher")
При обновлении с `Hyaxia/blogwatcher` переместите вашу базу данных:
[code] 
    mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db  
    
[/code]
Имя бинарного файла изменилось с `blogwatcher` на `blogwatcher-cli`.
## Основные команды[​](<#common-commands> "Прямая ссылка на Основные команды")
### Управление блогами[​](<#managing-blogs> "Прямая ссылка на Управление блогами")
  * Добавить блог: `blogwatcher-cli add "Мой блог" https://example.com`
  * Добавить с явным указанием ленты: `blogwatcher-cli add "Мой блог" https://example.com --feed-url https://example.com/feed.xml`
  * Добавить с HTML-скрейпингом: `blogwatcher-cli add "Мой блог" https://example.com --scrape-selector "article h2 a"`
  * Список отслеживаемых блогов: `blogwatcher-cli blogs`
  * Удалить блог: `blogwatcher-cli remove "Мой блог" --yes`
  * Импорт из OPML: `blogwatcher-cli import subscriptions.opml`


### Сканирование и чтение[​](<#scanning-and-reading> "Прямая ссылка на Сканирование и чтение")
  * Сканировать все блоги: `blogwatcher-cli scan`
  * Сканировать один блог: `blogwatcher-cli scan "Мой блог"`
  * Список непрочитанных статей: `blogwatcher-cli articles`
  * Список всех статей: `blogwatcher-cli articles --all`
  * Фильтр по блогу: `blogwatcher-cli articles --blog "Мой блог"`
  * Фильтр по категории: `blogwatcher-cli articles --category "Engineering"`
  * Отметить статью прочитанной: `blogwatcher-cli read 1`
  * Отметить статью непрочитанной: `blogwatcher-cli unread 1`
  * Отметить всё прочитанным: `blogwatcher-cli read-all`
  * Отметить всё прочитанным для блога: `blogwatcher-cli read-all --blog "Мой блог" --yes`


## Переменные окружения[​](<#environment-variables> "Прямая ссылка на Переменные окружения")
Все флаги могут быть заданы через переменные окружения с префиксом `BLOGWATCHER_`:
| Переменная | Описание |
|---|---|
|`BLOGWATCHER_DB`| Путь к файлу базы данных SQLite |
|`BLOGWATCHER_WORKERS`| Количество параллельных рабочих процессов сканирования (по умолчанию: 8) |
|`BLOGWATCHER_SILENT`| Выводить только «сканирование завершено» при сканировании |
|`BLOGWATCHER_YES`| Пропускать запросы подтверждения |
|`BLOGWATCHER_CATEGORY`| Фильтр по умолчанию для статей по категориям |
## Пример вывода[​](<#example-output> "Прямая ссылка на Пример вывода")
[code] 
    $ blogwatcher-cli blogs  
    Tracked blogs (1):  
      
      xkcd  
        URL: https://xkcd.com  
        Feed: https://xkcd.com/atom.xml  
        Last scanned: 2026-04-03 10:30  
    
[/code]
[code] 
    $ blogwatcher-cli scan  
    Scanning 1 blog(s)...  
      
      xkcd  
        Source: RSS | Found: 4 | New: 4  
      
    Found 4 new article(s) total!  
    
[/code]
[code] 
    $ blogwatcher-cli articles  
    Unread articles (2):  
      
      [1] [new] Barrel - Part 13  
           Blog: xkcd  
           URL: https://xkcd.com/3095/  
           Published: 2026-04-02  
           Categories: Comics, Science  
      
      [2] [new] Volcano Fact  
           Blog: xkcd  
           URL: https://xkcd.com/3094/  
           Published: 2026-04-01  
           Categories: Comics  
    
[/code]
## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * Автоматически обнаруживает RSS/Atom-ленты на домашних страницах блогов, если не указан `--feed-url`.
  * Использует запасной вариант HTML-скрейпинга, если RSS недоступен и настроен `--scrape-selector`.
  * Категории из RSS/Atom-лент сохраняются и могут использоваться для фильтрации статей.
  * Импортируйте блоги массово из OPML-файлов, экспортированных из Feedly, Inoreader, NewsBlur и других сервисов.
  * База данных по умолчанию хранится в `~/.blogwatcher-cli/blogwatcher-cli.db` (переопределяется через `--db` или `BLOGWATCHER_DB`).
  * Используйте `blogwatcher-cli <команда> --help`, чтобы узнать все флаги и параметры.


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Установка](<#installation>)
    * [Docker с постоянным хранилищем](<#docker-with-persistent-storage>)
    * [Миграция с оригинального blogwatcher](<#migrating-from-the-original-blogwatcher>)
  * [Основные команды](<#common-commands>)
    * [Управление блогами](<#managing-blogs>)
    * [Сканирование и чтение](<#scanning-and-reading>)
  * [Переменные окружения](<#environment-variables>)
  * [Пример вывода](<#example-output>)
  * [Примечания](<#notes>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-blogwatcher -->
