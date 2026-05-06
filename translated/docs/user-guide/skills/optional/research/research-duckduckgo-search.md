На этой странице
Бесплатный веб-поиск через DuckDuckGo — текст, новости, изображения, видео. Не требуется API-ключ. Предпочитайте CLI `ddgs`, если он установлен; используйте Python-библиотеку DDGS только после проверки, что `ddgs` доступен в текущей среде выполнения.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

| | |
|---|---|
| Источник | Опционально — установка: `hermes skills install official/research/duckduckgo-search` |
| Путь | `optional-skills/research/duckduckgo-search` |
| Версия | `1.3.0` |
| Автор | gamedevCloudy |
| Лицензия | MIT |
| Теги | `search`, `duckduckgo`, `web-search`, `free`, `fallback` |
| Связанные навыки | [`arxiv`](</docs/user-guide/skills/bundled/research/research-arxiv>) |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Именно эти инструкции видит агент, когда навык активен.

# DuckDuckGo Search

Бесплатный веб-поиск с использованием DuckDuckGo. **Не требуется API-ключ.**

Предпочтителен, когда `web_search` недоступен или непригоден (например, если не задан `FIRECRAWL_API_KEY`). Также может использоваться как самостоятельный путь поиска, когда нужны именно результаты DuckDuckGo.

## Порядок обнаружения[​](<#detection-flow> "Прямая ссылка на Порядок обнаружения")

Проверьте, что реально доступно, прежде чем выбирать подход:

[code]
    # Проверить доступность CLI
    command -v ddgs >/dev/null && echo "DDGS_CLI=installed" || echo "DDGS_CLI=missing"
    
[/code]

Дерево решений:

1. Если CLI `ddgs` установлен, предпочесть `terminal` + `ddgs`
2. Если CLI `ddgs` отсутствует, не предполагать, что `execute_code` может импортировать `ddgs`
3. Если пользователю нужен именно DuckDuckGo, сначала установить `ddgs` в соответствующей среде
4. В противном случае использовать встроенные веб/браузерные инструменты

Важное замечание о средах выполнения:

* `Terminal` и `execute_code` — это разные среды выполнения
* Успешная установка в shell не гарантирует, что `execute_code` сможет импортировать `ddgs`
* Никогда не предполагайте, что сторонние Python-пакеты предустановлены внутри `execute_code`

## Установка[​](<#installation> "Прямая ссылка на Установка")

Устанавливайте `ddgs` только тогда, когда поиск DuckDuckGo действительно нужен и среда выполнения ещё не предоставляет его.

[code]
    # Python-пакет + точка входа CLI
    pip install ddgs
      
    # Проверить CLI
    ddgs --help
    
[/code]

Если рабочий процесс зависит от Python-импортов, сначала убедитесь, что эта же среда выполнения может импортировать `ddgs`, прежде чем использовать `from ddgs import DDGS`.

## Метод 1: CLI-поиск (предпочтительный)[​](<#method-1-cli-search-preferred> "Прямая ссылка на Метод 1: CLI-поиск (предпочтительный)")

Используйте команду `ddgs` через `terminal`, если она существует. Это предпочтительный путь, поскольку он не предполагает, что в песочнице `execute_code` установлен Python-пакет `ddgs`.

[code]
    # Поиск текста
    ddgs text -q "python async programming" -m 5
      
    # Поиск новостей
    ddgs news -q "artificial intelligence" -m 5
      
    # Поиск изображений
    ddgs images -q "landscape photography" -m 10
      
    # Поиск видео
    ddgs videos -q "python tutorial" -m 5
      
    # С фильтром по региону
    ddgs text -q "best restaurants" -m 5 -r us-en
      
    # Только недавние результаты (d=день, w=неделя, m=месяц, y=год)
    ddgs text -q "latest AI news" -m 5 -t w
      
    # JSON-вывод для парсинга
    ddgs text -q "fastapi tutorial" -m 5 -o json
    
[/code]

### Флаги CLI[​](<#cli-flags> "Прямая ссылка на Флаги CLI")

| Флаг | Описание | Пример |
|---|---|---|
| `-q` | Запрос — **обязательный** | `-q "поисковый запрос"` |
| `-m` | Максимум результатов | `-m 5` |
| `-r` | Регион | `-r us-en` |
| `-t` | Временной лимит | `-t w` (неделя) |
| `-s` | Безопасный поиск | `-s off` |
| `-o` | Формат вывода | `-o json` |

## Метод 2: Python API (только после проверки)[​](<#method-2-python-api-only-after-verification> "Прямая ссылка на Метод 2: Python API (только после проверки)")

Используйте класс `DDGS` в `execute_code` или другой Python-среде только после проверки, что `ddgs` там установлен. Не предполагайте, что `execute_code` включает сторонние пакеты по умолчанию.

Безопасные формулировки:
* «Используйте `execute_code` с `ddgs` после установки или проверки пакета, если необходимо»

Избегайте таких формулировок:
* «`execute_code` включает `ddgs`»
* «Поиск DuckDuckGo работает по умолчанию в `execute_code`»

**Важно:** `max_results` всегда должен передаваться как **именованный аргумент** — позиционное использование вызывает ошибку во всех методах.

### Поиск текста[​](<#text-search> "Прямая ссылка на Поиск текста")

Лучше всего подходит для: общих исследований, компаний, документации.

[code]
    from ddgs import DDGS
      
    with DDGS() as ddgs:
        for r in ddgs.text("python async programming", max_results=5):
            print(r["title"])
            print(r["href"])
            print(r.get("body", "")[:200])
            print()
    
[/code]

Возвращает: `title`, `href`, `body`

### Поиск новостей[​](<#news-search> "Прямая ссылка на Поиск новостей")

Лучше всего подходит для: текущих событий, срочных новостей, последних обновлений.

[code]
    from ddgs import DDGS
      
    with DDGS() as ddgs:
        for r in ddgs.news("AI regulation 2026", max_results=5):
            print(r["date"], "-", r["title"])
            print(r.get("source", ""), "|", r["url"])
            print(r.get("body", "")[:200])
            print()
    
[/code]

Возвращает: `date`, `title`, `body`, `url`, `image`, `source`

### Поиск изображений[​](<#image-search> "Прямая ссылка на Поиск изображений")

Лучше всего подходит для: визуальных материалов, изображений продуктов, диаграмм.

[code]
    from ddgs import DDGS
      
    with DDGS() as ddgs:
        for r in ddgs.images("semiconductor chip", max_results=5):
            print(r["title"])
            print(r["image"])
            print(r.get("thumbnail", ""))
            print(r.get("source", ""))
            print()
    
[/code]

Возвращает: `title`, `image`, `thumbnail`, `url`, `height`, `width`, `source`

### Поиск видео[​](<#video-search> "Прямая ссылка на Поиск видео")

Лучше всего подходит для: обучающих материалов, демонстраций, объяснений.

[code]
    from ddgs import DDGS
      
    with DDGS() as ddgs:
        for r in ddgs.videos("FastAPI tutorial", max_results=5):
            print(r["title"])
            print(r.get("content", ""))
            print(r.get("duration", ""))
            print(r.get("provider", ""))
            print(r.get("published", ""))
            print()
    
[/code]

Возвращает: `title`, `content`, `description`, `duration`, `provider`, `published`, `statistics`, `uploader`

### Краткая справка[​](<#quick-reference> "Прямая ссылка на Краткая справка")

| Метод | Когда использовать | Ключевые поля |
|---|---|---|
| `text()` | Общие исследования, компании | title, href, body |
| `news()` | Текущие события, обновления | date, title, source, body, url |
| `images()` | Визуальные материалы, диаграммы | title, image, thumbnail, url |
| `videos()` | Обучающие материалы, демонстрации | title, content, duration, provider |

## Процесс: поиск с последующим извлечением[​](<#workflow-search-then-extract> "Прямая ссылка на Процесс: поиск с последующим извлечением")

DuckDuckGo возвращает заголовки, URL и сниппеты — не полное содержимое страниц. Чтобы получить полное содержимое, сначала выполните поиск, затем извлеките наиболее релевантный URL с помощью `web_extract`, браузерных инструментов или curl.

Пример через CLI:

[code]
    ddgs text -q "fastapi deployment guide" -m 3 -o json
    
[/code]

Пример на Python, только после проверки, что `ddgs` установлен в этой среде:

[code]
    from ddgs import DDGS
      
    with DDGS() as ddgs:
        results = list(ddgs.text("fastapi deployment guide", max_results=3))
        for r in results:
            print(r["title"], "->", r["href"])
    
[/code]

Затем извлеките лучший URL с помощью `web_extract` или другого инструмента получения содержимого.

## Ограничения[​](<#limitations> "Прямая ссылка на Ограничения")

* **Ограничение частоты запросов:** DuckDuckGo может начать ограничивать после множества быстрых запросов. При необходимости добавляйте небольшую задержку между поисками.
* **Нет извлечения содержимого:** `ddgs` возвращает сниппеты, а не полное содержимое страниц. Используйте `web_extract`, браузерные инструменты или curl для полной статьи/страницы.
* **Качество результатов:** В целом хорошее, но менее настраиваемое, чем поиск Firecrawl.
* **Доступность:** DuckDuckGo может блокировать запросы с некоторых облачных IP-адресов. Если поиск возвращает пустые результаты, попробуйте другие ключевые слова или подождите несколько секунд.
* **Вариативность полей:** Возвращаемые поля могут различаться в зависимости от результатов или версии `ddgs`. Используйте `.get()` для опциональных полей, чтобы избежать `KeyError`.
* **Разные среды выполнения:** Успешная установка `ddgs` в терминале не означает автоматически, что `execute_code` может его импортировать.

## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")

| Проблема | Вероятная причина | Что делать |
|---|---|---|
| `ddgs: command not found` | CLI не установлен в окружении shell | Установите `ddgs` или используйте встроенные веб/браузерные инструменты |
| `ModuleNotFoundError: No module named 'ddgs'` | В среде Python не установлен пакет | Не используйте Python DDGS, пока эта среда не будет подготовлена |
| Поиск ничего не возвращает | Временное ограничение частоты или неудачный запрос | Подождите несколько секунд, повторите или измените запрос |
| CLI работает, но импорт в `execute_code` не удаётся | Terminal и execute_code — разные среды | Продолжайте использовать CLI или отдельно подготовьте Python-среду |

## Подводные камни[​](<#pitfalls> "Прямая ссылка на Подводные камни")

* **`max_results` — только именованный аргумент:** `ddgs.text("query", 5)` вызывает ошибку. Используйте `ddgs.text("query", max_results=5)`.
* **Не предполагайте, что CLI существует:** Проверьте `command -v ddgs` перед использованием.
* **Не предполагайте, что `execute_code` может импортировать `ddgs`:** `from ddgs import DDGS` может завершиться ошибкой `ModuleNotFoundError`, если среда не была подготовлена отдельно.
* **Имя пакета:** Пакет называется `ddgs` (ранее `duckduckgo-search`). Устанавливайте через `pip install ddgs`.
* **Не путайте `-q` и `-m` (CLI):** `-q` — для запроса, `-m` — для количества результатов.
* **Пустые результаты:** Если `ddgs` ничего не возвращает, возможно, сработало ограничение частоты. Подождите несколько секунд и повторите.

## Проверено с[​](<#validated-with> "Прямая ссылка на Проверено с")

Проверенные примеры на семантике `ddgs==9.11.2`. Теперь руководство разделяет доступность CLI и Python-импорта как разные аспекты, чтобы документированный процесс соответствовал реальному поведению среды выполнения.

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Порядок обнаружения](<#detection-flow>)
* [Установка](<#installation>)
* [Метод 1: CLI-поиск (предпочтительный)](<#method-1-cli-search-preferred>)
  * [Флаги CLI](<#cli-flags>)
* [Метод 2: Python API (только после проверки)](<#method-2-python-api-only-after-verification>)
  * [Поиск текста](<#text-search>)
  * [Поиск новостей](<#news-search>)
  * [Поиск изображений](<#image-search>)
  * [Поиск видео](<#video-search>)
  * [Краткая справка](<#quick-reference>)
* [Процесс: поиск с последующим извлечением](<#workflow-search-then-extract>)
* [Ограничения](<#limitations>)
* [Устранение неполадок](<#troubleshooting>)
* [Подводные камни](<#pitfalls>)
* [Проверено с](<#validated-with>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-duckduckgo-search -->
