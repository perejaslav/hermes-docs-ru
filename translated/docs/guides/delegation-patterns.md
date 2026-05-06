На этой странице
Hermes может запускать изолированные дочерние агенты для параллельной работы над задачами. Каждый подчиненный агент получает собственный диалог, терминальную сессию и набор инструментов. Назад возвращается только итоговая сводка — промежуточные вызовы инструментов никогда не попадают в ваш контекст.

Полную справку по функционалу см. [Делегирование подчиненным агентам](</docs/user-guide/features/delegation>).

* * *

## Когда делегировать[​](<#when-to-delegate> "Прямая ссылка на «Когда делегировать»")

**Хорошие кандидаты для делегирования:**

- Подзадачи, требующие глубоких рассуждений (отладка, ревью кода, синтез исследований)
- Задачи, которые засорили бы ваш контекст промежуточными данными
- Параллельные независимые направления работы (исследование A и B одновременно)
- Задачи с «чистым» контекстом, где вы хотите, чтобы агент подошёл без предвзятости

**Используйте другое:**

- Одиночный вызов инструмента → просто используйте инструмент напрямую
- Механическая многошаговая работа с логикой между шагами → `execute_code`
- Задачи, требующие взаимодействия с пользователем → подчиненные агенты не могут использовать `clarify`
- Быстрые правки файлов → делайте их напрямую
- Долговременная работа, которая должна пережить текущий шаг → `cronjob` или `terminal(background=True, notify_on_complete=True)`. `delegate_task` является **синхронным**: если родительский шаг прерван, активные дочерние задачи отменяются, а их работа отбрасывается.

* * *

## Паттерн: Параллельное исследование[​](<#pattern-parallel-research> "Прямая ссылка на «Паттерн: Параллельное исследование»")

Исследуйте три темы одновременно и получите структурированные сводки:

[code]
    Исследуй эти три темы параллельно:
    1. Текущее состояние WebAssembly вне браузера
    2. Внедрение серверных чипов RISC-V в 2025 году
    3. Практические применения квантовых вычислений

    Сосредоточься на последних разработках и ключевых игроках.

[/code]

За кулисами Hermes использует:

[code]
    delegate_task(tasks=[
        {
            "goal": "Research WebAssembly outside the browser in 2025",
            "context": "Focus on: runtimes (Wasmtime, Wasmer), cloud/edge use cases, WASI progress",
            "toolsets": ["web"]
        },
        {
            "goal": "Research RISC-V server chip adoption",
            "context": "Focus on: server chips shipping, cloud providers adopting, software ecosystem",
            "toolsets": ["web"]
        },
        {
            "goal": "Research practical quantum computing applications",
            "context": "Focus on: error correction breakthroughs, real-world use cases, key companies",
            "toolsets": ["web"]
        }
    ])

[/code]

Все три выполняются одновременно. Каждый подчиненный агент независимо ищет в интернете и возвращает сводку. Затем родительский агент синтезирует их в связный обзор.

* * *

## Паттерн: Ревью кода[​](<#pattern-code-review> "Прямая ссылка на «Паттерн: Ревью кода»")

Делегируйте проверку безопасности подчиненному агенту с «чистым» контекстом, который подойдёт к коду без предубеждений:

[code]
    Проверь модуль аутентификации в src/auth/ на предмет проблем безопасности.
    Проверь SQL-инъекции, проблемы с валидацией JWT, обработку паролей
    и управление сессиями. Исправь всё, что найдёшь, и запусти тесты.

[/code]

Ключевое значение имеет поле `context` — оно должно включать всё, что нужно подчиненному агенту:

[code]
    delegate_task(
        goal="Review src/auth/ for security issues and fix any found",
        context="""Project at /home/user/webapp. Python 3.11, Flask, PyJWT, bcrypt.
        Auth files: src/auth/login.py, src/auth/jwt.py, src/auth/middleware.py
        Test command: pytest tests/auth/ -v
        Focus on: SQL injection, JWT validation, password hashing, session management.
        Fix issues found and verify tests pass.""",
        toolsets=["terminal", "file"]
    )

[/code]

**Проблема контекста**

Подчиненные агенты **абсолютно ничего** не знают о вашем разговоре. Они начинают с полностью чистого листа. Если вы делегируете «исправь баг, который мы обсуждали», подчиненный агент понятия не имеет, о каком баге речь. Всегда явно передавайте пути к файлам, сообщения об ошибках, структуру проекта и ограничения.

* * *

## Паттерн: Сравнение альтернатив[​](<#pattern-compare-alternatives> "Прямая ссылка на «Паттерн: Сравнение альтернатив»")

Оцените несколько подходов к одной и той же задаче параллельно, затем выберите лучший:

[code]
    Мне нужно добавить полнотекстовый поиск в наше Django-приложение. Оцени три подхода
    параллельно:
    1. PostgreSQL tsvector (встроенный)
    2. Elasticsearch через django-elasticsearch-dsl
    3. Meilisearch через meilisearch-python

    Для каждого: сложность настройки, возможности запросов, требования к ресурсам
    и затраты на поддержку. Сравни их и порекомендуй один.

[/code]

Каждый подчиненный агент независимо исследует один вариант. Благодаря изоляции отсутствует перекрёстное влияние — каждая оценка объективна сама по себе. Родительский агент получает все три сводки и проводит сравнение.

* * *

## Паттерн: Многофайловый рефакторинг[​](<#pattern-multi-file-refactoring> "Прямая ссылка на «Паттерн: Многофайловый рефакторинг»")

Разделите крупную задачу рефакторинга между параллельными подчиненными агентами, каждый из которых обрабатывает свою часть кодовой базы:

[code]
    delegate_task(tasks=[
        {
            "goal": "Refactor all API endpoint handlers to use the new response format",
            "context": """Project at /home/user/api-server.
            Files: src/handlers/users.py, src/handlers/auth.py, src/handlers/billing.py
            Old format: return {"data": result, "status": "ok"}
            New format: return APIResponse(data=result, status=200).to_dict()
            Import: from src.responses import APIResponse
            Run tests after: pytest tests/handlers/ -v""",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Update all client SDK methods to handle the new response format",
            "context": """Project at /home/user/api-server.
            Files: sdk/python/client.py, sdk/python/models.py
            Old parsing: result = response.json()["data"]
            New parsing: result = response.json()["data"] (same key, but add status code checking)
            Also update sdk/python/tests/test_client.py""",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Update API documentation to reflect the new response format",
            "context": """Project at /home/user/api-server.
            Docs at: docs/api/. Format: Markdown with code examples.
            Update all response examples from old format to new format.
            Add a 'Response Format' section to docs/api/overview.md explaining the schema.""",
            "toolsets": ["terminal", "file"]
        }
    ])

[/code]

> **Совет**
> Каждый подчиненный агент получает собственную терминальную сессию. Они могут работать в одном каталоге проекта, не мешая друг другу — при условии, что редактируют разные файлы. Если два подчиненных агента могут затронуть один и тот же файл, обработайте этот файл самостоятельно после завершения параллельной работы.

* * *

## Паттерн: Сбор, затем анализ[​](<#pattern-gather-then-analyze> "Прямая ссылка на «Паттерн: Сбор, затем анализ»")

Используйте `execute_code` для механического сбора данных, затем делегируйте анализ, требующий рассуждений:

[code]
    # Шаг 1: Механический сбор (execute_code подходит лучше — рассуждения не нужны)
    execute_code("""
    from hermes_tools import web_search, web_extract

    results = []
    for query in ["AI funding Q1 2026", "AI startup acquisitions 2026", "AI IPOs 2026"]:
        r = web_search(query, limit=5)
        for item in r["data"]["web"]:
            results.append({"title": item["title"], "url": item["url"], "desc": item["description"]})

    # Извлечь полное содержимое из 5 наиболее релевантных
    urls = [r["url"] for r in results[:5]]
    content = web_extract(urls)

    # Сохранить для этапа анализа
    import json
    with open("/tmp/ai-funding-data.json", "w") as f:
        json.dump({"search_results": results, "extracted": content["results"]}, f)
    print(f"Collected {len(results)} results, extracted {len(content['results'])} pages")
    """)

    # Шаг 2: Анализ, требующий рассуждений (делегирование подходит лучше)
    delegate_task(
        goal="Analyze AI funding data and write a market report",
        context="""Raw data at /tmp/ai-funding-data.json contains search results and
        extracted web pages about AI funding, acquisitions, and IPOs in Q1 2026.
        Write a structured market report: key deals, trends, notable players,
        and outlook. Focus on deals over $100M.""",
        toolsets=["terminal", "file"]
    )

[/code]

Это часто самый эффективный паттерн: `execute_code` дешево обрабатывает 10+ последовательных вызовов инструментов, а затем подчиненный агент выполняет единственную дорогую задачу рассуждения с чистым контекстом.

* * *

## Выбор набора инструментов[​](<#toolset-selection> "Прямая ссылка на «Выбор набора инструментов»")

Выбирайте наборы инструментов в зависимости от того, что нужно подчиненному агенту:

| Тип задачи | Наборы инструментов | Почему |
|---|---|---|
| Веб-исследование | `["web"]` | Только web_search + web_extract |
| Работа с кодом | `["terminal", "file"]` | Доступ к оболочке + операции с файлами |
| Полный стек | `["terminal", "file", "web"]` | Всё, кроме обмена сообщениями |
| Анализ только для чтения | `["file"]` | Может только читать файлы, без оболочки |

Ограничение наборов инструментов удерживает подчиненного агента в фокусе и предотвращает случайные побочные эффекты (например, подчиненный агент-исследователь, выполняющий команды оболочки).

* * *

## Ограничения[​](<#constraints> "Прямая ссылка на «Ограничения»")

- **По умолчанию 3 параллельные задачи**: пакеты по умолчанию запускают 3 одновременных подчиненных агента (настраивается через `delegation.max_concurrent_children` в config.yaml, без жесткого потолка, только минимум 1)
- **Вложенное делегирование — опционально**: листовые подчиненные агенты (по умолчанию) не могут вызывать `delegate_task`, `clarify`, `memory`, `send_message` или `execute_code`. Агенты-оркестраторы (`role="orchestrator"`) сохраняют возможность `delegate_task` для дальнейшего делегирования, но только когда `delegation.max_spawn_depth` поднят выше значения по умолчанию 1 (поддерживается 1–3); остальные четыре остаются заблокированными. Отключите глобально через `delegation.orchestrator_enabled: false`.

### Настройка параллельности и глубины[​](<#tuning-concurrency-and-depth> "Прямая ссылка на «Настройка параллельности и глубины»")

| Параметр | По умолч. | Диапазон | Эффект |
|---|---|---|---|
| `max_concurrent_children` | 3 | >=1 | Размер параллельного пакета на один вызов `delegate_task` |
| `max_spawn_depth` | 1 | 1–3 | Сколько уровней делегирования могут порождать дальнейшие |

Пример: запуск 30 параллельных рабочих с вложенными подчиненными агентами:

[code]
    delegation:
      max_concurrent_children: 30
      max_spawn_depth: 2

[/code]

- **Отдельные терминалы** — каждый подчиненный агент получает собственную терминальную сессию с отдельной рабочей директорией и состоянием
- **Нет истории разговора** — подчиненные агенты видят только `goal` и `context`, которые передает родительский агент при вызове `delegate_task`
- **По умолчанию 50 итераций** — установите `max_iterations` ниже для простых задач, чтобы сэкономить затраты
- **Не сохраняется** — `delegate_task` является синхронным и выполняется внутри родительского шага. Если родительский шаг прерван (новое сообщение пользователя, `/stop`, `/new`), все активные дочерние задачи отменяются (`status="interrupted"`), а их работа отбрасывается. Для работы, которая должна пережить текущий шаг, используйте `cronjob` или `terminal(background=True, notify_on_complete=True)`.

* * *

## Советы[​](<#tips> "Прямая ссылка на «Советы»")

**Будьте конкретны в целях.** «Исправь баг» — слишком расплывчато. «Исправь TypeError в api/handlers.py на строке 47, где process_request() получает None от parse_body()» — даёт подчиненному агенту достаточно информации для работы.

**Указывайте пути к файлам.** Подчиненные агенты не знают структуру вашего проекта. Всегда передавайте абсолютные пути к соответствующим файлам, корень проекта и команду для запуска тестов.

**Используйте делегирование для изоляции контекста.** Иногда нужен свежий взгляд. Делегирование заставляет вас чётко сформулировать проблему, а подчиненный агент подходит к ней без предположений, накопившихся в вашем разговоре.

**Проверяйте результаты.** Сводки подчиненных агентов — это всего лишь сводки. Если подчиненный агент говорит «баг исправлен, тесты проходят», проверьте, запустив тесты самостоятельно или прочитав дифф.

* * *

_Полную справку по делегированию — все параметры, интеграцию с ACP и расширенную настройку — см. в разделе [Делегирование подчиненным агентам](</docs/user-guide/features/delegation>)._

- [Когда делегировать](#when-to-delegate)
- [Паттерн: Параллельное исследование](#pattern-parallel-research)
- [Паттерн: Ревью кода](#pattern-code-review)
- [Паттерн: Сравнение альтернатив](#pattern-compare-alternatives)
- [Паттерн: Многофайловый рефакторинг](#pattern-multi-file-refactoring)
- [Паттерн: Сбор, затем анализ](#pattern-gather-then-analyze)
- [Выбор набора инструментов](#toolset-selection)
- [Ограничения](#constraints)
  - [Настройка параллельности и глубины](#tuning-concurrency-and-depth)
- [Советы](#tips)

<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns -->
