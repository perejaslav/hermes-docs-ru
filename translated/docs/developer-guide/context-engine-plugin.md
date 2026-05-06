On this page
Плагины контекстного движка заменяют встроенный `ContextCompressor` альтернативной стратегией управления контекстом беседы. Например, Lossless Context Management (LCM) — движок, который строит граф знаний вместо сжатия с потерями.
## Как это работает[​](<#how-it-works> "Direct link to How it works")
Управление контекстом агента построено на абстрактном классе `ContextEngine` (`agent/context_engine.py`). Встроенный `ContextCompressor` — реализация по умолчанию. Плагинные движки должны реализовывать тот же интерфейс.
Одновременно может быть активен **только один** контекстный движок. Выбор осуществляется через конфиг:
[code] 
    # config.yaml  
    context:  
      engine: "compressor"    # встроенный по умолчанию  
      engine: "lcm"           # активирует плагинный движок с именем "lcm"  
    
[/code]
Плагинные движки **никогда не активируются автоматически** — пользователь должен явно установить `context.engine` на имя плагина.
## Структура директории[​](<#directory-structure> "Direct link to Directory structure")
Каждый контекстный движок находится в `plugins/context_engine/<name>/`:
[code] 
    plugins/context_engine/lcm/  
    ├── __init__.py      # экспортирует подкласс ContextEngine  
    ├── plugin.yaml      # метаданные (name, description, version)  
    └── ...              # любые другие модули, необходимые вашему движку  
    
[/code]
## Абстрактный класс ContextEngine[​](<#the-contextengine-abc> "Direct link to The ContextEngine ABC")
Ваш движок должен реализовать следующие **обязательные** методы:
[code] 
    from agent.context_engine import ContextEngine  
      
    class LCMEngine(ContextEngine):  
      
        @property  
        def name(self) -> str:  
            """Краткий идентификатор, например 'lcm'. Должен совпадать со значением в config.yaml."""  
            return "lcm"  
      
        def update_from_response(self, usage: dict) -> None:  
            """Вызывается после каждого вызова LLM со словарём usage.  
      
            Обновите self.last_prompt_tokens, self.last_completion_tokens,  
            self.last_total_tokens из ответа.  
            """  
      
        def should_compress(self, prompt_tokens: int = None) -> bool:  
            """Верните True, если сжатие должно сработать в этом шаге."""  
      
        def compress(self, messages: list, current_tokens: int = None,  
                     focus_topic: str = None) -> list:  
            """Сожмите список сообщений и верните новый (возможно, более короткий) список.  
      
            Возвращённый список должен быть корректной последовательностью сообщений в формате OpenAI.  
      
            ``focus_topic`` — опциональная строка темы из ручного  
            ``/compress <focus>``; движки, поддерживающие направленное сжатие, должны  
            в первую очередь сохранять информацию, связанную с этой темой; остальные могут игнорировать её.  
            """  
    
[/code]
### Атрибуты класса, которые ваш движок должен поддерживать[​](<#class-attributes-your-engine-must-maintain> "Direct link to Class attributes your engine must maintain")
Агент читает их напрямую для отображения и логирования:
[code] 
    last_prompt_tokens: int = 0  
    last_completion_tokens: int = 0  
    last_total_tokens: int = 0  
    threshold_tokens: int = 0        # порог срабатывания сжатия  
    context_length: int = 0          # полное окно контекста модели  
    compression_count: int = 0       # сколько раз вызывался compress()  
    
[/code]
### Опциональные методы[​](<#optional-methods> "Direct link to Optional methods")
У них есть разумные значения по умолчанию в абстрактном классе. Переопределите при необходимости:
Метод| По умолчанию| Когда переопределять  
|---|---|---  
`on_session_start(session_id, **kwargs)`| Нет операции| Нужно загрузить сохранённое состояние (граф, БД)  
`on_session_end(session_id, messages)`| Нет операции| Нужно сбросить состояние, закрыть соединения  
`on_session_reset()`| Сбрасывает счётчики токенов| Есть состояние сессии, которое нужно очистить  
`update_model(model, context_length, ...)`| Обновляет context_length + threshold| Нужно пересчитать бюджеты при смене модели  
`get_tool_schemas()`| Возвращает `[]`| Ваш движок предоставляет инструменты, вызываемые агентом (например, `lcm_grep`)  
`handle_tool_call(name, args, **kwargs)`| Возвращает JSON с ошибкой| Вы реализуете обработчики инструментов  
`should_compress_preflight(messages)`| Возвращает `False`| Можно сделать дешёвую предварительную оценку до вызова API  
`get_status()`| Стандартный словарь токенов/порога| Есть собственные метрики для отображения  
## Инструменты движка[​](<#engine-tools> "Direct link to Engine tools")
Контекстные движки могут предоставлять инструменты, которые агент вызывает напрямую. Верните схемы из `get_tool_schemas()` и обрабатывайте вызовы в `handle_tool_call()`:
[code] 
    def get_tool_schemas(self):  
        return [{  
            "name": "lcm_grep",  
            "description": "Поиск по графу знаний контекста",  
            "parameters": {  
                "type": "object",  
                "properties": {  
                    "query": {"type": "string", "description": "Поисковый запрос"}  
                },  
                "required": ["query"],  
            },  
        }]  
      
    def handle_tool_call(self, name, args, **kwargs):  
        if name == "lcm_grep":  
            results = self._search_dag(args["query"])  
            return json.dumps({"results": results})  
        return json.dumps({"error": f"Неизвестный инструмент: {name}"})  
    
[/code]
Инструменты движка внедряются в список инструментов агента при запуске и диспетчеризуются автоматически — регистрация не требуется.
## Регистрация[​](<#registration> "Direct link to Registration")
### Через директорию (рекомендуется)[​](<#via-directory-recommended> "Direct link to Via directory (recommended)")
Поместите ваш движок в `plugins/context_engine/<name>/`. Файл `__init__.py` должен экспортировать подкласс `ContextEngine`. Система обнаружения находит и инстанцирует его автоматически.
### Через общую систему плагинов[​](<#via-general-plugin-system> "Direct link to Via general plugin system")
Общий плагин также может зарегистрировать контекстный движок:
[code] 
    def register(ctx):  
        engine = LCMEngine(context_length=200000)  
        ctx.register_context_engine(engine)  
    
[/code]
Может быть зарегистрирован только один движок. Попытка второго плагина зарегистрироваться отклоняется с предупреждением.
## Жизненный цикл[​](<#lifecycle> "Direct link to Lifecycle")
[code] 
    1. Движок инстанцирован (загрузка плагина или обнаружение через директорию)  
    2. on_session_start() — начало беседы  
    3. update_from_response() — после каждого вызова API  
    4. should_compress() — проверяется каждый шаг  
    5. compress() — вызывается, когда should_compress() возвращает True  
    6. on_session_end() — завершение сессии (выход из CLI, /reset, истечение срока gateway)  
    
[/code]
`on_session_reset()` вызывается при `/new` или `/reset` для очистки состояния сессии без полного завершения работы.
## Конфигурация[​](<#configuration> "Direct link to Configuration")
Пользователи выбирают ваш движок через `hermes plugins` → Provider Plugins → Context Engine, либо редактируя `config.yaml`:
[code] 
    context:  
      engine: "lcm"   # должно совпадать со свойством name вашего движка  
    
[/code]
Блок конфигурации `compression` (`compression.threshold`, `compression.protect_last_n` и т.д.) специфичен для встроенного `ContextCompressor`. Ваш движок должен определять собственный формат конфигурации при необходимости, читая из `config.yaml` во время инициализации.
## Тестирование[​](<#testing> "Direct link to Testing")
[code] 
    from agent.context_engine import ContextEngine  
      
    def test_engine_satisfies_abc():  
        engine = YourEngine(context_length=200000)  
        assert isinstance(engine, ContextEngine)  
        assert engine.name == "your-name"  
      
    def test_compress_returns_valid_messages():  
        engine = YourEngine(context_length=200000)  
        msgs = [{"role": "user", "content": "hello"}]  
        result = engine.compress(msgs)  
        assert isinstance(result, list)  
        assert all("role" in m for m in result)  
    
[/code]
Полный набор тестов для контракта абстрактного класса см. в `tests/agent/test_context_engine.py`.
## См. также[​](<#see-also> "Direct link to See also")
  * [Сжатие контекста и кэширование](</docs/developer-guide/context-compression-and-caching>) — как работает встроенный компрессор
  * [Плагины провайдеров памяти](</docs/developer-guide/memory-provider-plugin>) — аналогичная система плагинов с единичным выбором для памяти
  * [Плагины](</docs/user-guide/features/plugins>) — обзор общей системы плагинов


  * [Как это работает](<#how-it-works>)
  * [Структура директории](<#directory-structure>)
  * [Абстрактный класс ContextEngine](<#the-contextengine-abc>)
    * [Атрибуты класса, которые ваш движок должен поддерживать](<#class-attributes-your-engine-must-maintain>)
    * [Опциональные методы](<#optional-methods>)
  * [Инструменты движка](<#engine-tools>)
  * [Регистрация](<#registration>)
    * [Через директорию (рекомендуется)](<#via-directory-recommended>)
    * [Через общую систему плагинов](<#via-general-plugin-system>)
  * [Жизненный цикл](<#lifecycle>)
  * [Конфигурация](<#configuration>)
  * [Тестирование](<#testing>)
  * [См. также](<#see-also>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin -->
