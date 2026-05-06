На этой странице
Опциональный сторонний скилл для Parallel CLI — поиск в интернете, извлечение данных, глубокое исследование, обогащение, FindAll и мониторинг, ориентированные на агентов. Предпочитайте JSON-вывод и неинтерактивные сценарии.
## Метаданные скилла[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Источник| Опционально — установка: `hermes skills install official/research/parallel-cli`  |
|Путь| `optional-skills/research/parallel-cli`  |
|Версия| `1.1.0`  |
|Автор| Hermes Agent  |
|Лицензия| MIT  |
|Теги| `Research`, `Web`, `Search`, `Deep-Research`, `Enrichment`, `CLI`  |
|Связанные скиллы| [`duckduckgo-search`](</docs/user-guide/skills/optional/research/research-duckduckgo-search>), [`mcporter`](</docs/user-guide/skills/optional/mcp/mcp-mcporter>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение скилла, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда скилл активен.
# Parallel CLI
Используйте `parallel-cli`, когда пользователь явно хочет Parallel, или когда рабочий процесс в терминале выиграет от проприетарного стека Parallel для поиска в интернете, извлечения данных, глубокого исследования, обогащения, обнаружения сущностей или мониторинга.
Это опциональный сторонний рабочий процесс, а не базовое ядро Hermes.
Важные ожидания:
  * Parallel — это платный сервис с бесплатным тарифом, а не полностью бесплатный локальный инструмент.
  * Он пересекается с родными инструментами Hermes `web_search` / `web_extract`, поэтому не используйте его по умолчанию для обычных запросов.
  * Используйте этот скилл, когда пользователь упоминает Parallel конкретно или когда нужны возможности, такие как обогащение (enrichment), FindAll или мониторинг от Parallel.


`parallel-cli` спроектирован для агентов:
  * JSON-вывод через `--json`
  * Неинтерактивное выполнение команд
  * Асинхронные долгоиграющие задачи с `--no-wait`, `status` и `poll`
  * Цепочки контекста с `--previous-interaction-id`
  * Поиск, извлечение, исследование, обогащение, обнаружение сущностей и мониторинг в одном CLI


## Когда использовать[​](<#when-to-use-it> "Direct link to When to use it")
Используйте этот скилл, когда:
  * Пользователь явно упоминает Parallel или `parallel-cli`
  * Задача требует более сложных рабочих процессов, чем простой одноразовый поиск/извлечение
  * Вам нужны асинхронные задачи глубокого исследования, которые можно запустить и опросить позже
  * Вам нужно структурированное обогащение, обнаружение сущностей FindAll или мониторинг


Используйте родные инструменты Hermes `web_search` / `web_extract` для быстрых одноразовых запросов, когда Parallel не был явно запрошен.
## Установка[​](<#installation> "Direct link to Installation")
Попробуйте наименее инвазивный способ установки, доступный для вашего окружения.
### Homebrew[​](<#homebrew> "Direct link to Homebrew")
[code] 
    brew install parallel-web/tap/parallel-cli  
    
[/code]
### npm[​](<#npm> "Direct link to npm")
[code] 
    npm install -g parallel-web-cli  
    
[/code]
### Пакет Python[​](<#python-package> "Direct link to Python package")
[code] 
    pip install "parallel-web-tools[cli]"  
    
[/code]
### Автономный установщик[​](<#standalone-installer> "Direct link to Standalone installer")
[code] 
    curl -fsSL https://parallel.ai/install.sh | bash  
    
[/code]
Если вам нужна изолированная установка Python, также подойдёт `pipx`:
[code] 
    pipx install "parallel-web-tools[cli]"  
    pipx ensurepath  
    
[/code]
## Аутентификация[​](<#authentication> "Direct link to Authentication")
Интерактивный вход:
[code] 
    parallel-cli login  
    
[/code]
Безголовый режим / SSH / CI:
[code] 
    parallel-cli login --device  
    
[/code]
Переменная окружения для API-ключа:
[code] 
    export PARALLEL_API_KEY="***"  
    
[/code]
Проверка текущего статуса аутентификации:
[code] 
    parallel-cli auth  
    
[/code]
Если аутентификация требует взаимодействия с браузером, запускайте с `pty=true`.
## Основные правила[​](<#core-rule-set> "Direct link to Core rule set")
  1. Всегда используйте `--json`, когда вам нужен машиночитаемый вывод.
  2. Предпочитайте явные аргументы и неинтерактивные сценарии.
  3. Для долгоиграющих задач используйте `--no-wait`, а затем `status` / `poll`.
  4. Цитируйте только URL-адреса, возвращённые в выводе CLI.
  5. Сохраняйте большие JSON-выводы во временный файл, если вероятны уточняющие вопросы.
  6. Используйте фоновые процессы только для действительно долгих задач; в остальных случаях запускайте в обычном режиме.
  7. Предпочитайте родные инструменты Hermes, если пользователь не хочет Parallel конкретно или если нужны только функции Parallel.


## Краткая справка[​](<#quick-reference> "Direct link to Quick reference")
[code] 
    parallel-cli  
    ├── auth  
    ├── login  
    ├── logout  
    ├── search  
    ├── extract / fetch  
    ├── research run|status|poll|processors  
    ├── enrich run|status|poll|plan|suggest|deploy  
    ├── findall run|ingest|status|poll|result|enrich|extend|schema|cancel  
    └── monitor create|list|get|update|delete|events|event-group|simulate  
    
[/code]
## Распространённые флаги и шаблоны[​](<#common-flags-and-patterns> "Direct link to Common flags and patterns")
Полезные флаги:
  * `--json` для структурированного вывода
  * `--no-wait` для асинхронных задач
  * `--previous-interaction-id <id>` для последующих задач, использующих ранее полученный контекст
  * `--max-results <n>` для ограничения количества результатов поиска
  * `--mode one-shot|agentic` для выбора режима поиска
  * `--include-domains domain1.com,domain2.com`
  * `--exclude-domains domain1.com,domain2.com`
  * `--after-date YYYY-MM-DD`


Чтение из stdin, когда удобно:
[code] 
    echo "What is the latest funding for Anthropic?" | parallel-cli search - --json  
    echo "Research question" | parallel-cli research run - --json  
    
[/code]
## Поиск[​](<#search> "Direct link to Search")
Используйте для текущих веб-запросов со структурированными результатами.
[code] 
    parallel-cli search "What is Anthropic's latest AI model?" --json  
    parallel-cli search "SEC filings for Apple" --include-domains sec.gov --json  
    parallel-cli search "bitcoin price" --after-date 2026-01-01 --max-results 10 --json  
    parallel-cli search "latest browser benchmarks" --mode one-shot --json  
    parallel-cli search "AI coding agent enterprise reviews" --mode agentic --json  
    
[/code]
Полезные ограничения:
  * `--include-domains` для сужения круга доверенных источников
  * `--exclude-domains` для исключения зашумлённых доменов
  * `--after-date` для фильтрации по дате
  * `--max-results` когда нужно больше результатов


Если ожидаются уточняющие вопросы, сохраните вывод:
[code] 
    parallel-cli search "latest React 19 changes" --json -o /tmp/react-19-search.json  
    
[/code]
При обобщении результатов:
  * начинайте с ответа
  * включайте даты, имена и конкретные факты
  * ссылайтесь только на возвращённые источники
  * не выдумывайте URL-адреса или названия источников


## Извлечение данных[​](<#extraction> "Direct link to Extraction")
Используйте для получения чистого содержимого или markdown по URL-адресу.
[code] 
    parallel-cli extract https://example.com --json  
    parallel-cli extract https://company.com --objective "Find pricing info" --json  
    parallel-cli extract https://example.com --full-content --json  
    parallel-cli fetch https://example.com --json  
    
[/code]
Используйте `--objective`, когда страница широкая, а вам нужен только один фрагмент информации.
## Глубокое исследование[​](<#deep-research> "Direct link to Deep research")
Используйте для более глубоких многошаговых исследовательских задач, которые могут занять время.
Распространённые уровни процессора:
  * `lite` / `base` для более быстрых и дешёвых проходов
  * `core` / `pro` для более тщательного синтеза
  * `ultra` для самых тяжёлых исследовательских задач


### Синхронный режим[​](<#synchronous> "Direct link to Synchronous")
[code] 
    parallel-cli research run \  
      "Compare the leading AI coding agents by pricing, model support, and enterprise controls" \  
      --processor core \  
      --json  
    
[/code]
### Асинхронный запуск + опрос[​](<#async-launch--poll> "Direct link to Async launch + poll")
[code] 
    parallel-cli research run \  
      "Compare the leading AI coding agents by pricing, model support, and enterprise controls" \  
      --processor ultra \  
      --no-wait \  
      --json  
      
    parallel-cli research status trun_xxx --json  
    parallel-cli research poll trun_xxx --json  
    parallel-cli research processors --json  
    
[/code]
### Цепочки контекста / уточнение[​](<#context-chaining--follow-up> "Direct link to Context chaining / follow-up")
[code] 
    parallel-cli research run "What are the top AI coding agents?" --json  
    parallel-cli research run \  
      "What enterprise controls does the top-ranked one offer?" \  
      --previous-interaction-id trun_xxx \  
      --json  
    
[/code]
Рекомендуемый рабочий процесс в Hermes:
  1. Запустите с `--no-wait --json`
  2. Захватите возвращённый ID задачи/запуска
  3. Если пользователь хочет продолжить работу, двигайтесь дальше
  4. Позже вызовите `status` или `poll`
  5. Обобщите итоговый отчёт с цитированием из возвращённых источников


## Обогащение[​](<#enrichment> "Direct link to Enrichment")
Используйте, когда у пользователя есть CSV/JSON/табличные данные и он хочет добавить дополнительные столбцы на основе веб-исследования.
### Предложение столбцов[​](<#suggest-columns> "Direct link to Suggest columns")
[code] 
    parallel-cli enrich suggest "Find the CEO and annual revenue" --json  
    
[/code]
### Планирование конфигурации[​](<#plan-a-config> "Direct link to Plan a config")
[code] 
    parallel-cli enrich plan -o config.yaml  
    
[/code]
### Встроенные данные[​](<#inline-data> "Direct link to Inline data")
[code] 
    parallel-cli enrich run \  
      --data '[{"company": "Anthropic"}, {"company": "Mistral"}]' \  
      --intent "Find headquarters and employee count" \  
      --json  
    
[/code]
### Неинтерактивный запуск с файлом[​](<#non-interactive-file-run> "Direct link to Non-interactive file run")
[code] 
    parallel-cli enrich run \  
      --source-type csv \  
      --source companies.csv \  
      --target enriched.csv \  
      --source-columns '[{"name": "company", "description": "Company name"}]' \  
      --intent "Find the CEO and annual revenue"  
    
[/code]
### Запуск через YAML-конфиг[​](<#yaml-config-run> "Direct link to YAML config run")
[code] 
    parallel-cli enrich run config.yaml  
    
[/code]
### Статус / опрос[​](<#status--polling> "Direct link to Status / polling")
[code] 
    parallel-cli enrich status <task_group_id> --json  
    parallel-cli enrich poll <task_group_id> --json  
    
[/code]
Используйте явные JSON-массивы для определения столбцов при неинтерактивной работе. Проверьте выходной файл перед тем, как сообщить об успехе.
## FindAll[​](<#findall> "Direct link to FindAll")
Используйте для поиска сущностей в веб-масштабе, когда пользователь хочет получить найденный набор данных, а не краткий ответ.
[code] 
    parallel-cli findall run "Find AI coding agent startups with enterprise offerings" --json  
    parallel-cli findall run "AI startups in healthcare" -n 25 --json  
    parallel-cli findall status <run_id> --json  
    parallel-cli findall poll <run_id> --json  
    parallel-cli findall result <run_id> --json  
    parallel-cli findall schema <run_id> --json  
    
[/code]
Это лучше подходит, чем обычный поиск, когда пользователь хочет получить набор обнаруженных сущностей, которые можно просмотреть, отфильтровать или обогатить позже.
## Мониторинг[​](<#monitor> "Direct link to Monitor")
Используйте для постоянного отслеживания изменений с течением времени.
[code] 
    parallel-cli monitor list --json  
    parallel-cli monitor get <monitor_id> --json  
    parallel-cli monitor events <monitor_id> --json  
    parallel-cli monitor delete <monitor_id> --json  
    
[/code]
Создание обычно самая чувствительная часть, так как важны периодичность и доставка:
[code] 
    parallel-cli monitor create --help  
    
[/code]
Используйте это, когда пользователь хочет регулярно отслеживать страницу или источник, а не выполнять одноразовый запрос.
## Рекомендуемые шаблоны использования в Hermes[​](<#recommended-hermes-usage-patterns> "Direct link to Recommended Hermes usage patterns")
### Быстрый ответ с цитированием[​](<#fast-answer-with-citations> "Direct link to Fast answer with citations")
  1. Выполните `parallel-cli search ... --json`
  2. Извлеките заголовки, URL-адреса, даты, фрагменты
  3. Обобщите с цитатами только из возвращённых URL-адресов


### Исследование URL[​](<#url-investigation> "Direct link to URL investigation")
  1. Выполните `parallel-cli extract URL --json`
  2. При необходимости повторите с `--objective` или `--full-content`
  3. Процитируйте или обобщите извлечённый markdown


### Долгий исследовательский процесс[​](<#long-research-workflow> "Direct link to Long research workflow")
  1. Выполните `parallel-cli research run ... --no-wait --json`
  2. Сохраните возвращённый ID
  3. Продолжайте другую работу или периодически опрашивайте
  4. Обобщите итоговый отчёт с цитированием


### Структурированный процесс обогащения[​](<#structured-enrichment-workflow> "Direct link to Structured enrichment workflow")
  1. Изучите входной файл и столбцы
  2. Используйте `enrich suggest` или укажите явные столбцы для обогащения
  3. Запустите `enrich run`
  4. При необходимости опросите статус завершения
  5. Проверьте выходной файл перед сообщением об успехе


## Коды ошибок и их обработка[​](<#error-handling-and-exit-codes> "Direct link to Error handling and exit codes")
CLI документирует следующие коды возврата:
  * `0` — успех
  * `2` — неверные входные данные
  * `3` — ошибка аутентификации
  * `4` — ошибка API
  * `5` — тайм-аут


При ошибках аутентификации:
  1. проверьте `parallel-cli auth`
  2. убедитесь, что `PARALLEL_API_KEY` установлена, или выполните `parallel-cli login` / `parallel-cli login --device`
  3. проверьте, что `parallel-cli` находится в `PATH`


## Обслуживание[​](<#maintenance> "Direct link to Maintenance")
Проверка текущего состояния аутентификации/установки:
[code] 
    parallel-cli auth  
    parallel-cli --help  
    
[/code]
Команды обновления:
[code] 
    parallel-cli update  
    pip install --upgrade parallel-web-tools  
    parallel-cli config auto-update-check off  
    
[/code]
## Типичные ошибки[​](<#pitfalls> "Direct link to Pitfalls")
  * Не опускайте `--json`, если пользователь явно не хочет человекочитаемый вывод.
  * Не ссылайтесь на источники, отсутствующие в выводе CLI.
  * `login` может требовать PTY/взаимодействия с браузером.
  * Отдавайте предпочтение обычному выполнению для коротких задач; не злоупотребляйте фоновыми процессами.
  * Для больших наборов результатов сохраняйте JSON в `/tmp/*.json`, вместо того чтобы помещать всё в контекст.
  * Не выбирайте Parallel молча, если родных инструментов Hermes уже достаточно.
  * Помните, что это сторонний рабочий процесс, который обычно требует регистрации аккаунта и платного использования за пределами бесплатного тарифа.


  * [Метаданные скилла](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use-it>)
  * [Установка](<#installation>)
    * [Homebrew](<#homebrew>)
    * [npm](<#npm>)
    * [Пакет Python](<#python-package>)
    * [Автономный установщик](<#standalone-installer>)
  * [Аутентификация](<#authentication>)
  * [Основные правила](<#core-rule-set>)
  * [Краткая справка](<#quick-reference>)
  * [Распространённые флаги и шаблоны](<#common-flags-and-patterns>)
  * [Поиск](<#search>)
  * [Извлечение данных](<#extraction>)
  * [Глубокое исследование](<#deep-research>)
    * [Синхронный режим](<#synchronous>)
    * [Асинхронный запуск + опрос](<#async-launch--poll>)
    * [Цепочки контекста / уточнение](<#context-chaining--follow-up>)
  * [Обогащение](<#enrichment>)
    * [Предложение столбцов](<#suggest-columns>)
    * [Планирование конфигурации](<#plan-a-config>)
    * [Встроенные данные](<#inline-data>)
    * [Неинтерактивный запуск с файлом](<#non-interactive-file-run>)
    * [Запуск через YAML-конфиг](<#yaml-config-run>)
    * [Статус / опрос](<#status--polling>)
  * [FindAll](<#findall>)
  * [Мониторинг](<#monitor>)
  * [Рекомендуемые шаблоны использования в Hermes](<#recommended-hermes-usage-patterns>)
    * [Быстрый ответ с цитированием](<#fast-answer-with-citations>)
    * [Исследование URL](<#url-investigation>)
    * [Долгий исследовательский процесс](<#long-research-workflow>)
    * [Структурированный процесс обогащения](<#structured-enrichment-workflow>)
  * [Коды ошибок и их обработка](<#error-handling-and-exit-codes>)
  * [Обслуживание](<#maintenance>)
  * [Типичные ошибки](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-parallel-cli -->
