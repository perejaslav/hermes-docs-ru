On this page
Бесплатный мета-поиск через SearXNG — агрегирует результаты из 70+ поисковых систем. Самостоятельно размещаемый или с использованием публичного экземпляра. Не требует API-ключа. Автоматически переключается в режим запасного варианта, когда набор инструментов веб-поиска недоступен.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
|Source| Опциональный — установка через `hermes skills install official/research/searxng-search`  |
|Path| `optional-skills/research/searxng-search`  |
|Version| `1.0.0`  |
|Author| hermes-agent  |
|License| MIT  |
|Tags| `search`, `searxng`, `meta-search`, `self-hosted`, `free`, `fallback`  |
|Related skills| [`duckduckgo-search`](</docs/user-guide/skills/optional/research/research-duckduckgo-search>), [`domain-intel`](</docs/user-guide/skills/optional/research/research-domain-intel>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при активации этого навыка. Это те инструкции, которые видит агент, когда навык активен.
# SearXNG Search
Бесплатный мета-поиск с использованием [SearXNG](<https://searxng.org/>) — уважающего приватность, самостоятельно размещаемого поискового агрегатора, который одновременно запрашивает 70+ поисковых систем.
**Не требует API-ключа** при использовании публичного экземпляра. Может быть самостоятельно размещён для полного контроля. Автоматически появляется как запасной вариант, когда основной набор инструментов веб-поиска (`FIRECRAWL_API_KEY`) не настроен.
## Configuration[​](<#configuration> "Direct link to Configuration")
SearXNG требует указания переменной окружения `SEARXNG_URL`, указывающей на ваш экземпляр SearXNG:
[code] 
    # Публичные экземпляры (не требуют настройки)  
    SEARXNG_URL=https://searxng.example.com  
      
    # Самостоятельно размещённый SearXNG  
    SEARXNG_URL=http://localhost:8888  
    
[/code]
Если экземпляр не настроен, этот навык недоступен, и агент переключается на другие варианты поиска.
## Detection Flow[​](<#detection-flow> "Direct link to Detection Flow")
Проверьте, что реально доступно, прежде чем выбирать подход:
[code] 
    # Проверка, установлена ли SEARXNG_URL и доступен ли экземпляр  
    curl -s --max-time 5 "${SEARXNG_URL}/search?q=test&format=json" | head -c 200  
    
[/code]
Дерево решений:
  1. Если `SEARXNG_URL` установлен и экземпляр отвечает, используйте SearXNG
  2. Если `SEARXNG_URL` не установлен или недоступен, переключитесь на другие доступные инструменты поиска
  3. Если пользователь хочет использовать именно SearXNG, помогите ему настроить экземпляр или найти публичный


## Method 1: CLI via curl (Preferred)[​](<#method-1-cli-via-curl-preferred> "Direct link to Method 1: CLI via curl \\(Preferred\\)")
Используйте `curl` через `terminal` для вызова JSON API SearXNG. Это позволяет не предполагать наличие какого-либо конкретного Python-пакета.
[code] 
    # Текстовый поиск (вывод в JSON)  
    curl -s --max-time 10 \  
      "${SEARXNG_URL}/search?q=python+async+programming&format=json&engines=google,bing&limit=10"  
      
    # С отключённым безопасным поиском  
    curl -s --max-time 10 \  
      "${SEARXNG_URL}/search?q=example&format=json&safesearch=0"  
      
    # Определённые категории (general, news, science и т.д.)  
    curl -s --max-time 10 \  
      "${SEARXNG_URL}/search?q=AI+news&format=json&categories=news"  
    
[/code]
### Common CLI Flags[​](<#common-cli-flags> "Direct link to Common CLI Flags")
Флаг| Описание| Пример  
|---|---|---  
`q`| Строка запроса (URL-кодированная)| `q=python+async`  
`format`| Формат вывода: `json`, `csv`, `rss`| `format=json`  
`engines`| Разделённые запятыми имена движков| `engines=google,bing,ddg`  
`limit`| Макс. результатов на движок (по умолч. 10)| `limit=5`  
`categories`| Фильтр по категории| `categories=news,science`  
`safesearch`| 0=нет, 1=умеренный, 2=строгий| `safesearch=0`  
`time_range`| Фильтр: `day`, `week`, `month`, `year`| `time_range=week`  
### Parsing JSON Results[​](<#parsing-json-results> "Direct link to Parsing JSON Results")
[code] 
    # Извлечение заголовков и URL из JSON  
    curl -s --max-time 10 "${SEARXNG_URL}/search?q=fastapi&format=json&limit=5" \  
      | python3 -c "  
    import json, sys  
    data = json.load(sys.stdin)  
    for r in data.get('results', []):  
        print(r.get('title',''))  
        print(r.get('url',''))  
        print(r.get('content','')[:200])  
        print()  
    "  
    
[/code]
Возвращает для каждого результата: `title`, `url`, `content` (фрагмент), `engine`, `parsed_url`, `img_src`, `thumbnail`, `author`, `published_date`
## Method 2: Python API via `requests`[​](<#method-2-python-api-via-requests> "Direct link to method-2-python-api-via-requests")
Используйте REST API SearXNG напрямую из Python с библиотекой `requests`:
[code] 
    import os, requests, urllib.parse  
      
    base_url = os.environ.get("SEARXNG_URL", "")  
    if not base_url:  
        raise RuntimeError("SEARXNG_URL is not set")  
      
    query = "fastapi deployment guide"  
    params = {  
        "q": query,  
        "format": "json",  
        "limit": 5,  
        "engines": "google,bing",  
    }  
      
    resp = requests.get(f"{base_url}/search", params=params, timeout=10)  
    resp.raise_for_status()  
    data = resp.json()  
      
    for r in data.get("results", []):  
        print(r["title"])  
        print(r["url"])  
        print(r.get("content", "")[:200])  
        print()  
    
[/code]
## Method 3: searxng-data Python Package[​](<#method-3-searxng-data-python-package> "Direct link to Method 3: searxng-data Python Package")
Для более структурированного доступа установите пакет `searxng-data`:
[code] 
    pip install searxng-data  
    
[/code]
[code] 
    from searxng_data import engines  
      
    # Список доступных движков  
    print(engines.list_engines())  
    
[/code]
Примечание: Этот пакет предоставляет только метаданные движков, а не сам поисковый API.
## Self-Hosting SearXNG[​](<#self-hosting-searxng> "Direct link to Self-Hosting SearXNG")
Чтобы запустить собственный экземпляр SearXNG:
[code] 
    # Используя Docker  
    docker run -d -p 8888:8080 \  
      -v $(pwd)/searxng:/etc/searxng \  
      searxng/searxng:latest  
      
    # Затем установите  
    SEARXNG_URL=http://localhost:8888  
    
[/code]
Или установите через pip:
[code] 
    pip install searxng  
    # Отредактируйте /etc/searxng/settings.yml  
    searxng-run  
    
[/code]
Публичные экземпляры SearXNG доступны по адресу:
  * `https://searxng.example.com` (замените на любой публичный экземпляр)


## Workflow: Search then Extract[​](<#workflow-search-then-extract> "Direct link to Workflow: Search then Extract")
SearXNG возвращает заголовки, URL и фрагменты — но не полное содержимое страниц. Чтобы получить полное содержимое страницы, сначала выполните поиск, а затем извлеките наиболее релевантный URL с помощью `web_extract`, инструментов браузера или `curl`.
[code] 
    # Поиск релевантных страниц  
    curl -s "${SEARXNG_URL}/search?q=fastapi+deployment&format=json&limit=3"  
    # Вывод: список результатов с заголовками и URL  
      
    # Затем извлеките лучший URL с помощью web_extract  
    
[/code]
## Limitations[​](<#limitations> "Direct link to Limitations")
  * **Доступность экземпляра**: Если экземпляр SearXNG недоступен, поиск завершается ошибкой. Всегда проверяйте, что `SEARXNG_URL` установлен и экземпляр доступен.
  * **Нет извлечения содержимого**: SearXNG возвращает фрагменты, а не полное содержимое страниц. Используйте `web_extract`, инструменты браузера или `curl` для полных статей.
  * **Ограничение частоты запросов**: Некоторые публичные экземпляры ограничивают запросы. Самостоятельное размещение позволяет этого избежать.
  * **Охват движков**: Доступные движки зависят от конфигурации экземпляра SearXNG. Некоторые движки могут быть отключены.
  * **Свежесть результатов**: Мета-поиск агрегирует внешние движки — свежесть результатов зависит от этих движков.


## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
Проблема| Вероятная причина| Что делать  
|---|---|---  
`SEARXNG_URL` не установлен| Экземпляр не настроен| Используйте публичный экземпляр SearXNG или настройте свой собственный  
Соединение отклонено| Экземпляр не запущен или неверный URL| Проверьте корректность URL и то, что экземпляр запущен  
Пустые результаты| Экземпляр блокирует запрос| Попробуйте другой экземпляр или самостоятельное размещение  
Медленные ответы| Публичный экземпляр под нагрузкой| Разместите самостоятельно или используйте менее нагруженный публичный экземпляр  
Формат `json` не поддерживается| Старая версия SearXNG| Попробуйте `format=rss` или обновите SearXNG  
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **Всегда устанавливайте `SEARXNG_URL`**: Без него навык не может функционировать.
  * **URL-кодируйте запросы**: Пробелы и специальные символы должны быть URL-кодированы при использовании curl, или используйте `urllib.parse.quote()` в Python.
  * **Используйте `format=json`**: Формат по умолчанию может быть нечитаем для машин. Всегда явно запрашивайте JSON.
  * **Устанавливайте тайм-аут**: Всегда используйте `--max-time` или `timeout=`, чтобы избежать зависания при недоступных экземплярах.
  * **Самостоятельное размещение — лучший вариант**: Публичные экземпляры могут быть недоступны, ограничивать частоту запросов или блокировать. Самостоятельно размещённый экземпляр надёжен.


## Instance Discovery[​](<#instance-discovery> "Direct link to Instance Discovery")
Если `SEARXNG_URL` не установлен, а пользователь спрашивает о SearXNG, помогите ему либо:
  1. Найти публичный экземпляр SearXNG (поиск по запросу "public searxng instance")
  2. Настроить свой собственный с помощью Docker или pip


Публичные экземпляры перечислены на: <https://searxng.org/>
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Configuration](<#configuration>)
  * [Detection Flow](<#detection-flow>)
  * [Method 1: CLI via curl (Preferred)](<#method-1-cli-via-curl-preferred>)
    * [Common CLI Flags](<#common-cli-flags>)
    * [Parsing JSON Results](<#parsing-json-results>)
  * [Method 2: Python API via `requests`](<#method-2-python-api-via-requests>)
  * [Method 3: searxng-data Python Package](<#method-3-searxng-data-python-package>)
  * [Self-Hosting SearXNG](<#self-hosting-searxng>)
  * [Workflow: Search then Extract](<#workflow-search-then-extract>)
  * [Limitations](<#limitations>)
  * [Troubleshooting](<#troubleshooting>)
  * [Pitfalls](<#pitfalls>)
  * [Instance Discovery](<#instance-discovery>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-searxng-search -->
