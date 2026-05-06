На этой странице

Hermes Agent включает три веб-инструмента на базе нескольких провайдеров:

- **`web_search`** — поиск в интернете с ранжированными результатами
- **`web_extract`** — получение и извлечение читаемого содержимого из одного или нескольких URL
- **`web_crawl`** — рекурсивный обход сайта с возвратом структурированного содержимого

Все три инструмента настраиваются через единый выбор бэкенда. Провайдеры выбираются через `hermes tools` или задаются напрямую в `config.yaml`.

## Бэкенды[​](<#backends> "Direct link to Backends")

| Провайдер | Переменная окружения | Поиск | Извлечение | Обход | Бесплатный тариф |
|---|---|---|---|---|---|
| **Firecrawl** (по умолчанию) | `FIRECRAWL_API_KEY` | ✔ | ✔ | ✔ | 500 кредитов/мес |
| **SearXNG** | `SEARXNG_URL` | ✔ | — | — | ✔ Бесплатно (самостоятельный хостинг) |
| **Tavily** | `TAVILY_API_KEY` | ✔ | ✔ | ✔ | 1 000 поисков/мес |
| **Exa** | `EXA_API_KEY` | ✔ | ✔ | — | 1 000 поисков/мес |
| **Parallel** | `PARALLEL_API_KEY` | ✔ | ✔ | — | Платный |

**Разделение по возможностям:** вы можете использовать разных провайдеров для поиска и извлечения независимо — например, SearXNG (бесплатно) для поиска и Firecrawl для извлечения. См. [Конфигурация по возможностям](#per-capability-configuration) ниже.

### Подписчики Nous

Если у вас есть платная подписка [Nous Portal](https://portal.nousresearch.com), веб-поиск и извлечение доступны через **[Tool Gateway](/docs/user-guide/features/tool-gateway)** через управляемый Firecrawl — без необходимости API-ключа. Запустите `hermes tools`, чтобы включить.

* * *

## Настройка[​](<#setup> "Direct link to Setup")

### Быстрая настройка через `hermes tools`[​](<#quick-setup-via-hermes-tools> "Direct link to quick-setup-via-hermes-tools")

Запустите `hermes tools`, перейдите в **Web Search & Extract** и выберите провайдера. Мастер запросит необходимый URL или API-ключ и запишет его в вашу конфигурацию.

[code] 
    hermes tools  
    
[/code]

* * *

### Firecrawl (по умолчанию)[​](<#firecrawl-default> "Direct link to Firecrawl (default)")

Полнофункциональный поиск, извлечение и обход. Рекомендуется для большинства пользователей.

[code] 
    # ~/.hermes/.env  
    FIRECRAWL_API_KEY=fc-your-key-here  
    
[/code]

Получите ключ на [firecrawl.dev](https://firecrawl.dev). Бесплатный тариф включает 500 кредитов/месяц.

**Самостоятельный хостинг Firecrawl:** укажите на свой собственный экземпляр вместо облачного API:

[code] 
    # ~/.hermes/.env  
    FIRECRAWL_API_URL=http://localhost:3002  
    
[/code]

Когда `FIRECRAWL_API_URL` задан, API-ключ опционален (отключите аутентификацию сервера с помощью `USE_DB_AUTHENTICATION=false`).

* * *

### SearXNG (бесплатно, самостоятельный хостинг)[​](<#searxng-free-self-hosted> "Direct link to SearXNG (free, self-hosted)")

SearXNG — это уважающий конфиденциальность мета-поисковик с открытым исходным кодом, который агрегирует результаты из 70+ поисковых систем. **API-ключ не требуется** — просто укажите Hermes на работающий экземпляр SearXNG.

SearXNG — **только для поиска** — `web_extract` и `web_crawl` требуют отдельного провайдера для извлечения.

#### Вариант A — Самостоятельный хостинг с Docker (рекомендуется)[​](<#option-a--self-host-with-docker-recommended> "Direct link to Option A — Self-host with Docker (recommended)")

Это даёт вам приватный экземпляр без ограничений на количество запросов.

**1. Создайте рабочую директорию:**

[code] 
    mkdir -p ~/searxng/searxng  
    cd ~/searxng  
    
[/code]

**2. Напишите `docker-compose.yml`:**

[code] 
    # ~/searxng/docker-compose.yml  
    services:  
      searxng:  
        image: searxng/searxng:latest  
        container_name: searxng  
        ports:  
          - "8888:8080"  
        volumes:  
          - ./searxng:/etc/searxng:rw  
        environment:  
          - SEARXNG_BASE_URL=http://localhost:8888/  
        restart: unless-stopped  
    
[/code]

**3. Запустите контейнер:**

[code] 
    docker compose up -d  
    
[/code]

**4. Включите формат JSON API:**

SearXNG поставляется с отключённым выводом JSON по умолчанию. Скопируйте сгенерированную конфигурацию и включите его:

[code] 
    # Скопируйте автоматически сгенерированную конфигурацию из контейнера  
    docker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml  
    
[/code]

Откройте `~/searxng/searxng/settings.yml` и найдите блок `formats` (около строки 84):

[code] 
    # До (по умолчанию — JSON отключён):  
    formats:  
      - html  
      
    # После (включить JSON для Hermes):  
    formats:  
      - html  
      - json  
    
[/code]

**5. Перезапустите для применения изменений:**

[code] 
    docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.yml  
    docker restart searxng  
    
[/code]

**6. Проверьте, что всё работает:**

[code] 
    curl -s "http://localhost:8888/search?q=test&format=json" | python3 -c \
      "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"results\"])} results')"  
    
[/code]

Вы должны увидеть что-то вроде `10 results`. Если вы получили `403 Forbidden`, значит формат JSON всё ещё отключён — перепроверьте шаг 4.

**7. Настройте Hermes:**

[code] 
    # ~/.hermes/config.yaml  
    SEARXNG_URL: http://localhost:8888  
    
[/code]

Или установите через `hermes tools` → Web Search & Extract → SearXNG.

* * *

#### Вариант B — Использование публичного экземпляра[​](<#option-b--use-a-public-instance> "Direct link to Option B — Use a public instance")

Публичные экземпляры SearXNG перечислены на [searx.space](https://searx.space/). Отфильтруйте по экземплярам, у которых **включён формат JSON** (показано в таблице).

[code] 
    # ~/.hermes/config.yaml  
    SEARXNG_URL: https://searx.example.com  
    
[/code]

**Публичные экземпляры**

Публичные экземпляры имеют ограничения на количество запросов, нестабильное время работы и могут в любой момент отключить формат JSON. Для production-использования настоятельно рекомендуется самостоятельный хостинг.

* * *

#### Совмещение SearXNG с провайдером извлечения[​](<#pair-searxng-with-an-extract-provider> "Direct link to Pair SearXNG with an extract provider")

SearXNG обрабатывает поиск; вам нужен отдельный провайдер для `web_extract` и `web_crawl`. Используйте ключи для разделения по возможностям:

[code] 
    # ~/.hermes/config.yaml  
    web:  
      search_backend: "searxng"  
      extract_backend: "firecrawl"   # или tavily, exa, parallel  
    
[/code]

С такой конфигурацией Hermes использует SearXNG для всех поисковых запросов и Firecrawl для извлечения URL — сочетая бесплатный поиск с качественным извлечением.

* * *

### Tavily[​](<#tavily> "Direct link to Tavily")

Оптимизированный для ИИ поиск, извлечение и обход с щедрым бесплатным тарифом.

[code] 
    # ~/.hermes/.env  
    TAVILY_API_KEY=tvly-your-key-here  
    
[/code]

Получите ключ на [app.tavily.com](https://app.tavily.com/home). Бесплатный тариф включает 1 000 поисков/месяц.

* * *

### Exa[​](<#exa> "Direct link to Exa")

Нейронный поиск с семантическим пониманием. Хорош для исследований и поиска концептуально связанного контента.

[code] 
    # ~/.hermes/.env  
    EXA_API_KEY=your-exa-key-here  
    
[/code]

Получите ключ на [exa.ai](https://exa.ai). Бесплатный тариф включает 1 000 поисков/месяц.

* * *

### Parallel[​](<#parallel> "Direct link to Parallel")

ИИ-ориентированный поиск и извлечение с возможностями глубокого исследования.

[code] 
    # ~/.hermes/.env  
    PARALLEL_API_KEY=your-parallel-key-here  
    
[/code]

Получите доступ на [parallel.ai](https://parallel.ai).

* * *

## Конфигурация[​](<#configuration> "Direct link to Configuration")

### Единый бэкенд[​](<#single-backend> "Direct link to Single backend")

Установите одного провайдера для всех веб-возможностей:

[code] 
    # ~/.hermes/config.yaml  
    web:  
      backend: "searxng"   # firecrawl | searxng | tavily | exa | parallel  
    
[/code]

### Конфигурация по возможностям[​](<#per-capability-configuration> "Direct link to Per-capability configuration")

Используйте разных провайдеров для поиска и извлечения. Это позволяет сочетать бесплатный поиск (SearXNG) с платным провайдером извлечения или наоборот:

[code] 
    # ~/.hermes/config.yaml  
    web:  
      search_backend: "searxng"     # используется web_search  
      extract_backend: "firecrawl"  # используется web_extract и web_crawl  
    
[/code]

Когда ключи для отдельных возможностей пусты, они переходят к `web.backend`. Когда `web.backend` также пуст, бэкенд определяется автоматически по наличию API-ключа/URL.

**Приоритет (для каждой возможности):**

1. `web.search_backend` / `web.extract_backend` (явное указание для возможности)
2. `web.backend` (общий запасной вариант)
3. Автоопределение из переменных окружения

### Автоопределение[​](<#auto-detection> "Direct link to Auto-detection")

Если бэкенд явно не настроен, Hermes выбирает первый доступный на основе того, какие учётные данные заданы:

| Наличие учётных данных | Автоматически выбранный бэкенд |
|---|---|
| `FIRECRAWL_API_KEY` или `FIRECRAWL_API_URL` | firecrawl |
| `PARALLEL_API_KEY` | parallel |
| `TAVILY_API_KEY` | tavily |
| `EXA_API_KEY` | exa |
| `SEARXNG_URL` | searxng |

* * *

## Проверка настройки[​](<#verify-your-setup> "Direct link to Verify your setup")

Запустите `hermes setup`, чтобы увидеть, какой веб-бэкенд обнаружен:

[code] 
    ✅ Web Search & Extract (searxng)  
    
[/code]

Или проверьте через CLI:

[code] 
    # Активируйте venv и запустите модуль веб-инструментов напрямую  
    source ~/.hermes/hermes-agent/.venv/bin/activate  
    python -m tools.web_tools  
    
[/code]

Это выведет активный бэкенд и его статус:

[code] 
    ✅ Web backend: searxng  
       Using SearXNG (search only): http://localhost:8888  
    
[/code]

* * *

## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")

### `web_search` возвращает `{"success": false}`[​](<#web_search-returns-success-false> "Direct link to web_search-returns-success-false")

- Проверьте доступность `SEARXNG_URL`: `curl -s "http://localhost:8888/search?q=test&format=json"`
- Если вы получаете HTTP 403, значит формат JSON отключён — добавьте `json` в список `formats` в `settings.yml` и перезапустите
- Если вы получаете ошибку соединения, контейнер может не работать: `docker ps | grep searxng`

### `web_extract` сообщает "search-only backend"[​](<#web_extract-says-search-only-backend> "Direct link to web_extract-says-search-only-backend")

SearXNG не может извлекать содержимое URL. Установите `web.extract_backend` на провайдера, поддерживающего извлечение:

[code] 
    web:  
      search_backend: "searxng"  
      extract_backend: "firecrawl"  # или tavily / exa / parallel  
    
[/code]

### SearXNG возвращает 0 результатов[​](<#searxng-returns-0-results> "Direct link to SearXNG returns 0 results")

Некоторые публичные экземпляры отключают определённые поисковые системы или категории. Попробуйте:

- Другой запрос
- Другой публичный экземпляр с [searx.space](https://searx.space/)
- Самостоятельный хостинг своего экземпляра для надёжных результатов

### Ограничение запросов на публичном экземпляре[​](<#rate-limited-on-a-public-instance> "Direct link to Rate limited on a public instance")

Переключитесь на собственный экземпляр (см. [Вариант A](#option-a--self-host-with-docker-recommended) выше). С Docker ваш собственный экземпляр не имеет ограничений на количество запросов.

* * *

## Опциональный навык: `searxng-search`[​](<#optional-skill-searxng-search> "Direct link to optional-skill-searxng-search")

Для агентов, которым необходимо использовать SearXNG напрямую через `curl` (например, в качестве запасного варианта, когда набор веб-инструментов недоступен), установите опциональный навык `searxng-search`:

[code] 
    hermes skills install official/research/searxng-search  
    
[/code]

Это добавит навык, который обучает агента:

- Вызывать JSON API SearXNG через `curl` или Python
- Фильтровать по категориям (`general`, `news`, `science` и т.д.)
- Обрабатывать пагинацию и ошибки
- Корректно завершать работу, когда SearXNG недоступен

- [Бэкенды](#backends)
- [Настройка](#setup)
  - [Быстрая настройка через `hermes tools`](#quick-setup-via-hermes-tools)
  - [Firecrawl (по умолчанию)](#firecrawl-default)
  - [SearXNG (бесплатно, самостоятельный хостинг)](#searxng-free-self-hosted)
  - [Tavily](#tavily)
  - [Exa](#exa)
  - [Parallel](#parallel)
- [Конфигурация](#configuration)
  - [Единый бэкенд](#single-backend)
  - [Конфигурация по возможностям](#per-capability-configuration)
  - [Автоопределение](#auto-detection)
- [Проверка настройки](#verify-your-setup)
- [Устранение неполадок](#troubleshooting)
  - [`web_search` возвращает `{"success": false}`](#web_search-returns-success-false)
  - [`web_extract` сообщает "search-only backend"](#web_extract-says-search-only-backend)
  - [SearXNG возвращает 0 результатов](#searxng-returns-0-results)
  - [Ограничение запросов на публичном экземпляре](#rate-limited-on-a-public-instance)
- [Опциональный навык: `searxng-search`](#optional-skill-searxng-search)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search -->
