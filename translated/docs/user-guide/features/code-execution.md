На этой странице
Инструмент `execute_code` позволяет агенту писать скрипты на Python, которые программно вызывают инструменты Hermes, сворачивая многошаговые рабочие процессы в один шаг LLM. Скрипт выполняется в дочернем процессе на хосте агента, взаимодействуя с Hermes через RPC по Unix domain socket.

## Как это работает[​](<#how-it-works> "Прямая ссылка на раздел")

  1. Агент пишет скрипт на Python, используя `from hermes_tools import ...`
  2. Hermes генерирует модуль-заглушку `hermes_tools.py` с RPC-функциями
  3. Hermes открывает Unix domain socket и запускает поток RPC-слушателя
  4. Скрипт выполняется в дочернем процессе — вызовы инструментов идут через сокет обратно к Hermes
  5. В LLM возвращается только `print()`-вывод скрипта; промежуточные результаты инструментов не попадают в контекстное окно

[code]
    # Агент может писать скрипты наподобие:
    from hermes_tools import web_search, web_extract

    results = web_search("Python 3.13 features", limit=5)
    for r in results["data"]["web"]:
        content = web_extract([r["url"]])
        # ... фильтрация и обработка ...
    print(summary)

[/code]
**Доступные инструменты внутри скриптов:** `web_search`, `web_extract`, `read_file`, `write_file`, `search_files`, `patch`, `terminal` (только в режиме переднего плана).

## Когда агент использует это[​](<#when-the-agent-uses-this> "Прямая ссылка на раздел")

Агент использует `execute_code`, когда есть:
  * **3+ вызова инструментов** с логикой обработки между ними
  * Массовая фильтрация данных или условное ветвление
  * Циклы по результатам

Ключевое преимущество: промежуточные результаты инструментов никогда не попадают в контекстное окно — возвращается только финальный `print()`-вывод, что значительно сокращает расход токенов.

## Практические примеры[​](<#practical-examples> "Прямая ссылка на раздел")

### Конвейер обработки данных[​](<#data-processing-pipeline> "Прямая ссылка на раздел")

[code]
    from hermes_tools import search_files, read_file
    import json

    # Найти все конфигурационные файлы и извлечь настройки БД
    matches = search_files("database", path=".", file_glob="*.yaml", limit=20)
    configs = []
    for match in matches.get("matches", []):
        content = read_file(match["path"])
        configs.append({"file": match["path"], "preview": content["content"][:200]})

    print(json.dumps(configs, indent=2))

[/code]

### Многошаговое веб-исследование[​](<#multi-step-web-research> "Прямая ссылка на раздел")

[code]
    from hermes_tools import web_search, web_extract
    import json

    # Поиск, извлечение и обобщение за один шаг
    results = web_search("Rust async runtime comparison 2025", limit=5)
    summaries = []
    for r in results["data"]["web"]:
        page = web_extract([r["url"]])
        for p in page.get("results", []):
            if p.get("content"):
                summaries.append({
                    "title": r["title"],
                    "url": r["url"],
                    "excerpt": p["content"][:500]
                })

    print(json.dumps(summaries, indent=2))

[/code]

### Массовый рефакторинг файлов[​](<#bulk-file-refactoring> "Прямая ссылка на раздел")

[code]
    from hermes_tools import search_files, read_file, patch

    # Найти все Python-файлы, использующие устаревший API, и исправить их
    matches = search_files("old_api_call", path="src/", file_glob="*.py")
    fixed = 0
    for match in matches.get("matches", []):
        result = patch(
            path=match["path"],
            old_string="old_api_call(",
            new_string="new_api_call(",
            replace_all=True
        )
        if "error" not in str(result):
            fixed += 1

    print(f"Fixed {fixed} files out of {len(matches.get('matches', []))} matches")

[/code]

### Конвейер сборки и тестирования[​](<#build-and-test-pipeline> "Прямая ссылка на раздел")

[code]
    from hermes_tools import terminal, read_file
    import json

    # Запустить тесты, разобрать результаты и отчитаться
    result = terminal("cd /project && python -m pytest --tb=short -q 2>&1", timeout=120)
    output = result.get("output", "")

    # Разбор вывода тестов
    passed = output.count(" passed")
    failed = output.count(" failed")
    errors = output.count(" error")

    report = {
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "exit_code": result.get("exit_code", -1),
        "summary": output[-500:] if len(output) > 500 else output
    }

    print(json.dumps(report, indent=2))

[/code]

## Режим выполнения[​](<#execution-mode> "Прямая ссылка на раздел")

`execute_code` имеет два режима выполнения, управляемых параметром `code_execution.mode` в `~/.hermes/config.yaml`:

| Режим | Рабочая директория | Интерпретатор Python |
|---|---|---|
| **`project`** (по умолчанию) | Рабочая директория сессии (как у `terminal()`) | Активный `VIRTUAL_ENV` / `CONDA_PREFIX` python, с запасным вариантом на собственный python Hermes |
| `strict` | Временная изолированная директория, отделённая от проекта пользователя | `sys.executable` (собственный python Hermes) |

**Когда оставить `project`:** вам нужно, чтобы `import pandas`, `from my_project import foo` или относительные пути вроде `open(".env")` работали так же, как в `terminal()`. Это почти всегда то, что нужно.

**Когда переключиться на `strict`:** когда требуется максимальная воспроизводимость — чтобы каждый сеанс использовал один и тот же интерпретатор независимо от того, какое виртуальное окружение активировал пользователь, и чтобы скрипты были изолированы от дерева проекта (без риска случайного чтения файлов проекта через относительный путь).

[code]
    # ~/.hermes/config.yaml
    code_execution:
      mode: project   # или "strict"

[/code]

Поведение при откате в режиме `project`: если `VIRTUAL_ENV` / `CONDA_PREFIX` не задан, повреждён или указывает на Python старше 3.8, резолвер чисто откатывается к `sys.executable` — агент никогда не остаётся без рабочего интерпретатора.

Критически важные для безопасности инварианты идентичны в обоих режимах:
  * очистка окружения (ключи API, токены, учётные данные удаляются)
  * белый список инструментов (скрипты не могут рекурсивно вызывать `execute_code`, `delegate_task` или MCP-инструменты)
  * ограничения ресурсов (таймаут, лимит stdout, лимит вызовов инструментов)

Смена режима изменяет то, где выполняются скрипты и какой интерпретатор их запускает, а не то, какие учётные данные они видят или какие инструменты могут вызывать.

## Ограничения ресурсов[​](<#resource-limits> "Прямая ссылка на раздел")

| Ресурс | Лимит | Примечания |
|---|---|---|
| **Таймаут** | 5 минут (300 с) | Скрипт завершается сигналом SIGTERM, затем SIGKILL через 5 с льготного периода |
| **Stdout** | 50 КБ | Вывод усекается с уведомлением `[output truncated at 50KB]` |
| **Stderr** | 10 КБ | Включается в вывод при ненулевом коде завершения для отладки |
| **Вызовы инструментов** | 50 на выполнение | Возвращается ошибка при достижении лимита |

Все лимиты настраиваются через `config.yaml`:

[code]
    # В ~/.hermes/config.yaml
    code_execution:
      mode: project      # project (по умолчанию) | strict
      timeout: 300       # Макс. секунд на скрипт (по умолчанию: 300)
      max_tool_calls: 50 # Макс. вызовов инструментов на выполнение (по умолчанию: 50)

[/code]

## Как работают вызовы инструментов внутри скриптов[​](<#how-tool-calls-work-inside-scripts> "Прямая ссылка на раздел")

Когда ваш скрипт вызывает функцию вроде `web_search("query")`:
  1. Вызов сериализуется в JSON и отправляется через Unix domain socket в родительский процесс
  2. Родительский процесс диспетчеризует вызов через стандартный обработчик `handle_function_call`
  3. Результат отправляется обратно через сокет
  4. Функция возвращает разобранный результат

Это означает, что вызовы инструментов внутри скриптов ведут себя идентично обычным вызовам инструментов — те же лимиты скорости, та же обработка ошибок, те же возможности. Единственное ограничение: `terminal()` работает только в режиме переднего плана (без параметров `background` или `pty`).

## Обработка ошибок[​](<#error-handling> "Прямая ссылка на раздел")

Когда скрипт завершается с ошибкой, агент получает структурированную информацию об ошибке:
  * **Ненулевой код завершения**: stderr включается в вывод, чтобы агент видел полный traceback
  * **Таймаут**: Скрипт завершается, и агент видит `"Script timed out after 300s and was killed."`
  * **Прерывание**: Если пользователь отправляет новое сообщение во время выполнения, скрипт завершается, и агент видит `[execution interrupted — user sent a new message]`
  * **Лимит вызовов инструментов**: При достижении лимита в 50 вызовов последующие вызовы возвращают сообщение об ошибке

Ответ всегда включает `status` (success/error/timeout/interrupted), `output`, `tool_calls_made` и `duration_seconds`.

## Безопасность[​](<#security> "Прямая ссылка на раздел")

Модель безопасности

Дочерний процесс выполняется с **минимальным окружением**. Ключи API, токены и учётные данные по умолчанию удаляются. Скрипт получает доступ к инструментам исключительно через RPC-канал — он не может читать секреты из переменных окружения, если это явно не разрешено.

Переменные окружения, содержащие в названии `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, `PASSWD` или `AUTH`, исключаются. Пропускаются только безопасные системные переменные (`PATH`, `HOME`, `LANG`, `SHELL`, `PYTHONPATH`, `VIRTUAL_ENV` и т.д.).

### Проброс переменных окружения навыков[​](<#skill-environment-variable-passthrough> "Прямая ссылка на раздел")

Когда навык объявляет `required_environment_variables` в своём frontmatter, эти переменные **автоматически пробрасываются** в дочерние процессы `execute_code` и `terminal` после загрузки навыка. Это позволяет навыкам использовать свои объявленные ключи API, не ослабляя политику безопасности для произвольного кода.

Для случаев использования без навыков вы можете явно разрешить переменные в `config.yaml`:

[code]
    terminal:
      env_passthrough:
        - MY_CUSTOM_KEY
        - ANOTHER_TOKEN

[/code]

Подробнее см. в [Руководстве по безопасности](</docs/user-guide/security#environment-variable-passthrough>).

Hermes всегда записывает скрипт и автоматически сгенерированную RPC-заглушку `hermes_tools.py` во временную директорию, которая очищается после выполнения. В режиме `strict` скрипт также _выполняется_ там; в режиме `project` он выполняется в рабочей директории сессии (при этом временная директория остаётся в `PYTHONPATH`, чтобы импорты продолжали работать). Дочерний процесс работает в собственной группе процессов, чтобы его можно было чисто завершить по таймауту или прерыванию.

## execute_code против terminal[​](<#execute_code-vs-terminal> "Прямая ссылка на раздел")

| Сценарий использования | execute_code | terminal |
|---|---|---|
| Многошаговые рабочие процессы с вызовами инструментов между шагами | ✅ | ❌ |
| Простая shell-команда | ❌ | ✅ |
| Фильтрация/обработка больших выводов инструментов | ✅ | ❌ |
| Запуск сборки или набора тестов | ❌ | ✅ |
| Циклы по результатам поиска | ✅ | ❌ |
| Интерактивные/фоновые процессы | ❌ | ✅ |
| Требуются ключи API в окружении | ⚠️ Только через [проброс](</docs/user-guide/security#environment-variable-passthrough>) | ✅ (большинство пробрасывается) |

**Эмпирическое правило:** Используйте `execute_code`, когда нужно программно вызывать инструменты Hermes с логикой между вызовами. Используйте `terminal` для запуска shell-команд, сборок и процессов.

## Поддержка платформ[​](<#platform-support> "Прямая ссылка на раздел")

Выполнение кода требует Unix domain sockets и доступно только на **Linux и macOS**. На Windows оно автоматически отключается — агент переходит к обычным последовательным вызовам инструментов.

  * [Как это работает](<#how-it-works>)
  * [Когда агент использует это](<#when-the-agent-uses-this>)
  * [Практические примеры](<#practical-examples>)
    * [Конвейер обработки данных](<#data-processing-pipeline>)
    * [Многошаговое веб-исследование](<#multi-step-web-research>)
    * [Массовый рефакторинг файлов](<#bulk-file-refactoring>)
    * [Конвейер сборки и тестирования](<#build-and-test-pipeline>)
  * [Режим выполнения](<#execution-mode>)
  * [Ограничения ресурсов](<#resource-limits>)
  * [Как работают вызовы инструментов внутри скриптов](<#how-tool-calls-work-inside-scripts>)
  * [Обработка ошибок](<#error-handling>)
  * [Безопасность](<#security>)
    * [Проброс переменных окружения навыков](<#skill-environment-variable-passthrough>)
  * [execute_code против terminal](<#execute_code-vs-terminal>)
  * [Поддержка платформ](<#platform-support>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution -->
