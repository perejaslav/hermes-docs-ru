На этой странице
Адаптер ACP оборачивает синхронный `AIAgent` Hermes в асинхронный JSON-RPC stdio сервер.
Ключевые файлы реализации:
  * `acp_adapter/entry.py`
  * `acp_adapter/server.py`
  * `acp_adapter/session.py`
  * `acp_adapter/events.py`
  * `acp_adapter/permissions.py`
  * `acp_adapter/tools.py`
  * `acp_adapter/auth.py`
  * `acp_registry/agent.json`


## Порядок запуска[​](<#boot-flow> "Прямая ссылка на порядок запуска")
[code] 
    hermes acp / hermes-acp / python -m acp_adapter  
      -> acp_adapter.entry.main()  
      -> load ~/.hermes/.env  
      -> configure stderr logging  
      -> construct HermesACPAgent  
      -> acp.run_agent(agent, use_unstable_protocol=True)  
    
[/code]
Stdout зарезервирован для ACP JSON-RPC транспорта. Человекочитаемые логи направляются в stderr.
## Основные компоненты[​](<#major-components> "Прямая ссылка на основные компоненты")
### `HermesACPAgent`[​](<#hermesacpagent> "Прямая ссылка на HermesACPAgent")
`acp_adapter/server.py` реализует протокол агента ACP.
Обязанности:
  * инициализация / аутентификация
  * методы new/load/resume/fork/list/cancel для сессий
  * выполнение prompt
  * переключение модели сессии
  * подключение синхронных колбэков AIAgent к асинхронным уведомлениям ACP


### `SessionManager`[​](<#sessionmanager> "Прямая ссылка на SessionManager")
`acp_adapter/session.py` отслеживает активные ACP-сессии.
Каждая сессия хранит:
  * `session_id`
  * `agent`
  * `cwd`
  * `model`
  * `history`
  * `cancel_event`


Менеджер потокобезопасен и поддерживает:
  * создание
  * получение
  * удаление
  * ответвление
  * список
  * очистку
  * обновление cwd


### Мост событий[​](<#event-bridge> "Прямая ссылка на мост событий")
`acp_adapter/events.py` преобразует колбэки AIAgent в события ACP `session_update`.
Преобразованные колбэки:
  * `tool_progress_callback`
  * `thinking_callback`
  * `step_callback`
  * `message_callback`


Поскольку `AIAgent` выполняется в рабочем потоке, а ACP I/O находится в главном цикле событий, мост использует:
[code] 
    asyncio.run_coroutine_threadsafe(...)  
    
[/code]
### Мост разрешений[​](<#permission-bridge> "Прямая ссылка на мост разрешений")
`acp_adapter/permissions.py` адаптирует опасные запросы подтверждения терминала в запросы разрешений ACP.
Отображение:
  * `allow_once` -> Hermes `once`
  * `allow_always` -> Hermes `always`
  * опции отклонения -> Hermes `deny`


Тайм-ауты и сбои моста по умолчанию запрещены.
### Вспомогательные функции отображения инструментов[​](<#tool-rendering-helpers> "Прямая ссылка на вспомогательные функции отображения инструментов")
`acp_adapter/tools.py` отображает инструменты Hermes в типы инструментов ACP и создает содержимое для редактора.
Примеры:
  * `patch` / `write_file` -> разницы файлов
  * `terminal` -> текст команды оболочки
  * `read_file` / `search_files` -> текстовые превью
  * большие результаты -> усеченные текстовые блоки для безопасности UI


## Жизненный цикл сессии[​](<#session-lifecycle> "Прямая ссылка на жизненный цикл сессии")
[code] 
    new_session(cwd)  
      -> create SessionState  
      -> create AIAgent(platform="acp", enabled_toolsets=["hermes-acp"])  
      -> bind task_id/session_id to cwd override  
      
    prompt(..., session_id)  
      -> extract text from ACP content blocks  
      -> reset cancel event  
      -> install callbacks + approval bridge  
      -> run AIAgent in ThreadPoolExecutor  
      -> update session history  
      -> emit final agent message chunk  
    
[/code]
### Отмена[​](<#cancelation> "Прямая ссылка на отмену")
`cancel(session_id)`:
  * устанавливает событие отмены сессии
  * вызывает `agent.interrupt()`, если доступно
  * приводит к тому, что ответ prompt возвращает `stop_reason="cancelled"`


### Ответвление[​](<#forking> "Прямая ссылка на ответвление")
`fork_session()` выполняет глубокое копирование истории сообщений в новую активную сессию, сохраняя состояние разговора, но присваивая ответвлению свой собственный идентификатор сессии и cwd.
## Поведение провайдера/аутентификации[​](<#providerauth-behavior> "Прямая ссылка на поведение провайдера/аутентификации")
ACP не реализует собственное хранилище аутентификации.
Вместо этого он повторно использует runtime-резолвер Hermes:
  * `acp_adapter/auth.py`
  * `hermes_cli/runtime_provider.py`


Таким образом, ACP рекламирует и использует текущий настроенный провайдер/учетные данные Hermes.
## Привязка рабочей директории[​](<#working-directory-binding> "Прямая ссылка на привязку рабочей директории")
ACP-сессии передают cwd редактора.
Менеджер сессий привязывает этот cwd к идентификатору ACP-сессии через терминальные/файловые переопределения с областью задачи, поэтому файловые и терминальные инструменты работают относительно рабочей области редактора.
## Вызовы инструментов с одинаковыми именами[​](<#duplicate-same-name-tool-calls> "Прямая ссылка на вызовы инструментов с одинаковыми именами")
Мост событий отслеживает идентификаторы инструментов FIFO для каждого имени инструмента, а не только один идентификатор на имя.
Это важно для:
  * параллельных вызовов с одинаковыми именами
  * повторяющихся вызовов с одинаковыми именами в одном шаге


Без очередей FIFO события завершения прикреплялись бы к неправильному вызову инструмента.
## Восстановление колбэка утверждения[​](<#approval-callback-restoration> "Прямая ссылка на восстановление колбэка утверждения")
ACP временно устанавливает колбэк утверждения на инструмент терминала во время выполнения prompt, а затем восстанавливает предыдущий колбэк после.
Это позволяет избежать постоянной глобальной установки обработчиков утверждения, специфичных для ACP-сессии.
## Текущие ограничения[​](<#current-limitations> "Прямая ссылка на текущие ограничения")
  * ACP-сессии сохраняются в общую базу `~/.hermes/state.db` (SessionDB) и прозрачно восстанавливаются после перезапуска процесса; они появляются в `session_search`
  * не текстовые блоки prompt в настоящее время игнорируются при извлечении текста запроса
  * специфичный для редактора UX зависит от реализации ACP-клиента


## Связанные файлы[​](<#related-files> "Прямая ссылка на связанные файлы")
  * `tests/acp/` — набор тестов ACP
  * `toolsets.py` — определение набора инструментов `hermes-acp`
  * `hermes_cli/main.py` — подкоманда CLI `hermes acp`
  * `pyproject.toml` — опциональная зависимость `[acp]` + скрипт `hermes-acp`


  * [Порядок запуска](<#boot-flow>)
  * [Основные компоненты](<#major-components>)
    * [`HermesACPAgent`](<#hermesacpagent>)
    * [`SessionManager`](<#sessionmanager>)
    * [Мост событий](<#event-bridge>)
    * [Мост разрешений](<#permission-bridge>)
    * [Вспомогательные функции отображения инструментов](<#tool-rendering-helpers>)
  * [Жизненный цикл сессии](<#session-lifecycle>)
    * [Отмена](<#cancelation>)
    * [Ответвление](<#forking>)
  * [Поведение провайдера/аутентификации](<#providerauth-behavior>)
  * [Привязка рабочей директории](<#working-directory-binding>)
  * [Вызовы инструментов с одинаковыми именами](<#duplicate-same-name-tool-calls>)
  * [Восстановление колбэка утверждения](<#approval-callback-restoration>)
  * [Текущие ограничения](<#current-limitations>)
  * [Связанные файлы](<#related-files>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals -->