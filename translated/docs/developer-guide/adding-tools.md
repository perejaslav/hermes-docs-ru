На этой странице
Прежде чем писать инструмент, спросите себя: **не должен ли это быть[скилл](</docs/developer-guide/creating-skills>) вместо этого?**
Только встроенные основные инструменты
Эта страница предназначена для добавления **встроенного инструмента Hermes** непосредственно в репозиторий. Если вам нужен личный, локальный для проекта или иной пользовательский инструмент без изменения ядра Hermes, используйте вместо этого путь плагинов:
  * [Плагины](</docs/user-guide/features/plugins>)
  * [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>)


По умолчанию используйте плагины для большинства пользовательских инструментов. Следуйте этой странице только тогда, когда вы явно хотите добавить новый встроенный инструмент в `tools/` и `toolsets.py`.
Делайте это **Скиллом**, когда возможность может быть выражена как инструкции + shell-команды + существующие инструменты (поиск arXiv, git-процессы, управление Docker, обработка PDF).
Делайте это **Инструментом**, когда требуется сквозная интеграция с API-ключами, пользовательская логика обработки, работа с бинарными данными или стриминг (автоматизация браузера, TTS, анализ изображений).
## Обзор[​](<#overview> "Прямая ссылка на Обзор")
Добавление инструмента затрагивает **2 файла**:
  1. **`tools/your_tool.py`** — обработчик, схема, функция проверки, вызов `registry.register()`
  2. **`toolsets.py`** — добавление имени инструмента в `_HERMES_CORE_TOOLS` (или конкретный набор инструментов)


Любой файл `tools/*.py` с вызовом `registry.register()` на верхнем уровне автоматически обнаруживается при запуске — ручной список импорта не требуется.
## Шаг 1: Создание файла встроенного инструмента[​](<#step-1-create-the-built-in-tool-file> "Прямая ссылка на Шаг 1: Создание файла встроенного инструмента")
Каждый файл инструмента следует одной и той же структуре:
[code] 
    # tools/weather_tool.py  
    """Инструмент погоды — получение текущей погоды для местоположения."""  
      
    import json  
    import os  
    import logging  
      
    logger = logging.getLogger(__name__)  
      
      
    # --- Проверка доступности ---  
      
    def check_weather_requirements() -> bool:  
        """Вернуть True, если зависимости инструмента доступны."""  
        return bool(os.getenv("WEATHER_API_KEY"))  
      
      
    # --- Обработчик ---  
      
    def weather_tool(location: str, units: str = "metric") -> str:  
        """Получить погоду для местоположения. Возвращает JSON-строку."""  
        api_key = os.getenv("WEATHER_API_KEY")  
        if not api_key:  
            return json.dumps({"error": "WEATHER_API_KEY не настроен"})  
        try:  
            # ... вызов API погоды ...  
            return json.dumps({"location": location, "temp": 22, "units": units})  
        except Exception as e:  
            return json.dumps({"error": str(e)})  
      
      
    # --- Схема ---  
      
    WEATHER_SCHEMA = {  
        "name": "weather",  
        "description": "Получить текущую погоду для местоположения.",  
        "parameters": {  
            "type": "object",  
            "properties": {  
                "location": {  
                    "type": "string",  
                    "description": "Название города или координаты (например, 'Москва' или '55.7,37.6')"  
                },  
                "units": {  
                    "type": "string",  
                    "enum": ["metric", "imperial"],  
                    "description": "Единицы измерения температуры (по умолчанию: metric)",  
                    "default": "metric"  
                }  
            },  
            "required": ["location"]  
        }  
    }  
      
      
    # --- Регистрация ---  
      
    from tools.registry import registry  
      
    registry.register(  
        name="weather",  
        toolset="weather",  
        schema=WEATHER_SCHEMA,  
        handler=lambda args, **kw: weather_tool(  
            location=args.get("location", ""),  
            units=args.get("units", "metric")),  
        check_fn=check_weather_requirements,  
        requires_env=["WEATHER_API_KEY"],  
    )  
    
[/code]
### Ключевые правила[​](<#key-rules> "Прямая ссылка на Ключевые правила")
Важно
  * Обработчики **ОБЯЗАНЫ** возвращать JSON-строку (через `json.dumps()`), никогда не сырые словари
  * Ошибки **ОБЯЗАНЫ** возвращаться как `{"error": "message"}`, никогда не выбрасываться как исключения
  * `check_fn` вызывается при построении определений инструментов — если она возвращает `False`, инструмент молча исключается
  * `handler` получает `(args: dict, **kwargs)`, где `args` — аргументы вызова инструмента от LLM


## Шаг 2: Добавление встроенного инструмента в набор[​](<#step-2-add-the-built-in-tool-to-a-toolset> "Прямая ссылка на Шаг 2: Добавление встроенного инструмента в набор")
В `toolsets.py` добавьте имя инструмента:
[code] 
    # Если он должен быть доступен на всех платформах (CLI + мессенджеры):  
    _HERMES_CORE_TOOLS = [  
        ...  
        "weather",  # <-- добавить сюда  
    ]  
      
    # Или создайте новый отдельный набор инструментов:  
    "weather": {  
        "description": "Инструменты поиска погоды",  
        "tools": ["weather"],  
        "includes": []  
    },  
    
[/code]
## ~~Шаг 3: Добавление импорта обнаружения~~ (Больше не требуется)[​](<#step-3-add-discovery-import-no-longer-needed> "Прямая ссылка на step-3-add-discovery-import-no-longer-needed")
Модули инструментов с вызовом `registry.register()` на верхнем уровне автоматически обнаруживаются функцией `discover_builtin_tools()` в `tools/registry.py`. Никакого ручного списка импорта для поддержки — просто создайте файл в `tools/`, и он будет подхвачен при запуске.
## Асинхронные обработчики[​](<#async-handlers> "Прямая ссылка на Асинхронные обработчики")
Если вашему обработчику нужен асинхронный код, пометьте его параметром `is_async=True`:
[code] 
    async def weather_tool_async(location: str) -> str:  
        async with aiohttp.ClientSession() as session:  
            ...  
        return json.dumps(result)  
      
    registry.register(  
        name="weather",  
        toolset="weather",  
        schema=WEATHER_SCHEMA,  
        handler=lambda args, **kw: weather_tool_async(args.get("location", "")),  
        check_fn=check_weather_requirements,  
        is_async=True,  # registry вызывает _run_async() автоматически  
    )  
    
[/code]
Реестр обрабатывает асинхронное bridging прозрачно — вам никогда не нужно вызывать `asyncio.run()` самостоятельно.
## Обработчики, которым нужен task_id[​](<#handlers-that-need-task_id> "Прямая ссылка на Обработчики, которым нужен task_id")
Инструменты, управляющие состоянием сессии, получают `task_id` через `**kwargs`:
[code] 
    def _handle_weather(args, **kw):  
        task_id = kw.get("task_id")  
        return weather_tool(args.get("location", ""), task_id=task_id)  
      
    registry.register(  
        name="weather",  
        ...  
        handler=_handle_weather,  
    )  
    
[/code]
## Инструменты, перехватываемые циклом агента[​](<#agent-loop-intercepted-tools> "Прямая ссылка на Инструменты, перехватываемые циклом агента")
Некоторые инструменты (`todo`, `memory`, `session_search`, `delegate_task`) требуют доступа к состоянию агента сессии. Они перехватываются `run_agent.py` до того, как достигают реестра. Реестр всё ещё хранит их схемы, но `dispatch()` возвращает резервную ошибку, если перехват был обойдён.
## Опционально: интеграция с мастером настройки[​](<#optional-setup-wizard-integration> "Прямая ссылка на Опционально: интеграция с мастером настройки")
Если ваш инструмент требует API-ключ, добавьте его в `hermes_cli/config.py`:
[code] 
    OPTIONAL_ENV_VARS = {  
        ...  
        "WEATHER_API_KEY": {  
            "description": "API-ключ погоды для поиска погоды",  
            "prompt": "API-ключ погоды",  
            "url": "https://weatherapi.com/",  
            "tools": ["weather"],  
            "password": True,  
        },  
    }  
    
[/code]
## Контрольный список[​](<#checklist> "Прямая ссылка на Контрольный список")
  * Файл инструмента создан с обработчиком, схемой, функцией проверки и регистрацией
  * Добавлен в соответствующий набор инструментов в `toolsets.py`
  * Подтверждено, что это действительно должен быть встроенный/основной инструмент, а не плагин
  * Обработчик возвращает JSON-строки, ошибки возвращаются как `{"error": "..."}`
  * Опционально: API-ключ добавлен в `OPTIONAL_ENV_VARS` в `hermes_cli/config.py`
  * Опционально: Добавлен в `toolset_distributions.py` для пакетной обработки
  * Протестировано с помощью `hermes chat -q "Используй инструмент погоды для Москвы"`


  * [Обзор](<#overview>)
  * [Шаг 1: Создание файла встроенного инструмента](<#step-1-create-the-built-in-tool-file>)
    * [Ключевые правила](<#key-rules>)
  * [Шаг 2: Добавление встроенного инструмента в набор](<#step-2-add-the-built-in-tool-to-a-toolset>)
  * [~~Шаг 3: Добавление импорта обнаружения~~ (Больше не требуется)](<#step-3-add-discovery-import-no-longer-needed>)
  * [Асинхронные обработчики](<#async-handlers>)
  * [Обработчики, которым нужен task_id](<#handlers-that-need-task_id>)
  * [Инструменты, перехватываемые циклом агента](<#agent-loop-intercepted-tools>)
  * [Опционально: интеграция с мастером настройки](<#optional-setup-wizard-integration>)
  * [Контрольный список](<#checklist>)



<!-- Источник: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools -->
