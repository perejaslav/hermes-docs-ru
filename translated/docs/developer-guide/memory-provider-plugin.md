На этой странице
Плагины провайдеров памяти дают Hermes Agent постоянные, межсессионные знания, выходящие за рамки встроенных MEMORY.md и USER.md. Это руководство объясняет, как создать такой плагин.
tip
Провайдеры памяти — это один из двух типов **провайдерских плагинов**. Другой — [Плагины контекстных движков](</docs/developer-guide/context-engine-plugin>), которые заменяют встроенный компрессор контекста. Оба следуют одному шаблону: одиночный выбор, управление через конфигурацию, администрирование через `hermes plugins`.
## Структура директории[​](<#directory-structure> "Прямая ссылка на «Структура директории»")
Каждый провайдер памяти находится в `plugins/memory/<имя>/`:
[code] 
    plugins/memory/my-provider/  
    ├── __init__.py      # Реализация MemoryProvider + точка входа register()  
    ├── plugin.yaml      # Метаданные (имя, описание, хуки)  
    └── README.md        # Инструкции по установке, справка по конфигурации, инструменты  
    
[/code]
## Абстрактный базовый класс MemoryProvider[​](<#the-memoryprovider-abc> "Прямая ссылка на «Абстрактный базовый класс MemoryProvider»")
Ваш плагин реализует абстрактный базовый класс `MemoryProvider` из `agent/memory_provider.py`:
[code] 
    from agent.memory_provider import MemoryProvider  
      
    class MyMemoryProvider(MemoryProvider):  
        @property  
        def name(self) -> str:  
            return "my-provider"  
      
        def is_available(self) -> bool:  
            """Проверить, может ли этот провайдер активироваться. Без сетевых вызовов."""  
            return bool(os.environ.get("MY_API_KEY"))  
      
        def initialize(self, session_id: str, **kwargs) -> None:  
            """Вызывается один раз при запуске агента.  
      
            kwargs всегда включает:  
              hermes_home (str): Путь к активному HERMES_HOME. Используйте для хранения.  
            """  
            self._api_key = os.environ.get("MY_API_KEY", "")  
            self._session_id = session_id  
      
        # ... реализация остальных методов  
    
[/code]
## Обязательные методы[​](<#required-methods> "Прямая ссылка на «Обязательные методы»")
### Основной жизненный цикл[​](<#core-lifecycle> "Прямая ссылка на «Основной жизненный цикл»")
Метод| Когда вызывается| Обязателен?  
|---|---|---  
`name` (свойство)| Всегда| **Да**  
`is_available()`| Инициализация агента, до активации| **Да** — без сетевых вызовов  
`initialize(session_id, **kwargs)`| Запуск агента| **Да**  
`get_tool_schemas()`| После инициализации, для внедрения инструментов| **Да**  
`handle_tool_call(name, args)`| Когда агент использует ваши инструменты| **Да** (если есть инструменты)  
### Конфигурация[​](<#config> "Прямая ссылка на «Конфигурация»")
Метод| Назначение| Обязателен?  
|---|---|---  
`get_config_schema()`| Объявить поля конфигурации для `hermes memory setup`| **Да**  
`save_config(values, hermes_home)`| Записать несекретную конфигурацию в собственное хранилище| **Да** (если не только env-переменные)  
### Опциональные хуки[​](<#optional-hooks> "Прямая ссылка на «Опциональные хуки»")
Метод| Когда вызывается| Сценарий использования  
|---|---|---  
`system_prompt_block()`| Сборка системного промпта| Статическая информация о провайдере  
`prefetch(query)`| Перед каждым API-вызовом| Возврат извлечённого контекста  
`queue_prefetch(query)`| После каждого оборота| Предварительная загрузка для следующего оборота  
`sync_turn(user, assistant)`| После каждого завершённого оборота| Сохранение диалога  
`on_session_end(messages)`| Разговор завершается| Финальное извлечение/сброс  
`on_pre_compress(messages)`| Перед сжатием контекста| Сохранение инсайтов до удаления  
`on_memory_write(action, target, content)`| Встроенные записи памяти| Зеркалирование в ваш бэкенд  
`shutdown()`| Завершение процесса| Закрытие соединений  
## Схема конфигурации[​](<#config-schema> "Прямая ссылка на «Схема конфигурации»")
`get_config_schema()` возвращает список описателей полей, используемых `hermes memory setup`:
[code] 
    def get_config_schema(self):  
        return [  
            {  
                "key": "api_key",  
                "description": "API-ключ My Provider",  
                "secret": True,           # → записывается в .env  
                "required": True,  
                "env_var": "MY_API_KEY",   # явное имя переменной окружения  
                "url": "https://my-provider.com/keys",  # где получить  
            },  
            {  
                "key": "region",  
                "description": "Регион сервера",  
                "default": "us-east",  
                "choices": ["us-east", "eu-west", "ap-south"],  
            },  
            {  
                "key": "project",  
                "description": "Идентификатор проекта",  
                "default": "hermes",  
            },  
        ]  
    
[/code]
Поля с `secret: True` и `env_var` попадают в `.env`. Несекретные поля передаются в `save_config()`.
Минимальная vs Полная схема
Каждое поле в `get_config_schema()` запрашивается во время `hermes memory setup`. Провайдерам с множеством опций следует делать схему минимальной — включать только те поля, которые пользователь **обязан** настроить (API-ключ, обязательные учётные данные). Дополнительные настройки документируйте в справочнике конфигурационного файла (например, `$HERMES_HOME/myprovider.json`), а не запрашивайте их все при установке. Это ускоряет мастер установки, сохраняя при этом поддержку расширенной конфигурации. Пример — провайдер Supermemory: он запрашивает только API-ключ; все остальные опции хранятся в `supermemory.json`.
## Сохранение конфигурации[​](<#save-config> "Прямая ссылка на «Сохранение конфигурации»")
[code] 
    def save_config(self, values: dict, hermes_home: str) -> None:  
        """Записать несекретную конфигурацию в ваше собственное хранилище."""  
        import json  
        from pathlib import Path  
        config_path = Path(hermes_home) / "my-provider.json"  
        config_path.write_text(json.dumps(values, indent=2))  
    
[/code]
Для провайдеров, использующих только переменные окружения, оставьте реализацию по умолчанию (пустую).
## Точка входа плагина[​](<#plugin-entry-point> "Прямая ссылка на «Точка входа плагина»")
[code] 
    def register(ctx) -> None:  
        """Вызывается системой обнаружения плагинов памяти."""  
        ctx.register_memory_provider(MyMemoryProvider())  
    
[/code]
## plugin.yaml[​](<#pluginyaml> "Прямая ссылка на «plugin.yaml»")
[code] 
    name: my-provider  
    version: 1.0.0  
    description: "Краткое описание того, что делает этот провайдер."  
    hooks:  
      - on_session_end    # перечислите хуки, которые вы реализуете  
    
[/code]
## Контракт многопоточности[​](<#threading-contract> "Прямая ссылка на «Контракт многопоточности»")
**`sync_turn()` НЕ ДОЛЖЕН быть блокирующим.** Если ваш бэкенд имеет задержки (API-вызовы, LLM-обработка), выполняйте работу в фоновом потоке-демоне:
[code] 
    def sync_turn(self, user_content, assistant_content):  
        def _sync():  
            try:  
                self._api.ingest(user_content, assistant_content)  
            except Exception as e:  
                logger.warning("Синхронизация не удалась: %s", e)  
      
        if self._sync_thread and self._sync_thread.is_alive():  
            self._sync_thread.join(timeout=5.0)  
        self._sync_thread = threading.Thread(target=_sync, daemon=True)  
        self._sync_thread.start()  
    
[/code]
## Изоляция профилей[​](<#profile-isolation> "Прямая ссылка на «Изоляция профилей»")
Все пути хранения **обязаны** использовать параметр `hermes_home` из `initialize()`, а не жёстко заданный `~/.hermes`:
[code] 
    # ПРАВИЛЬНО — в рамках профиля  
    from hermes_constants import get_hermes_home  
    data_dir = get_hermes_home() / "my-provider"  
      
    # НЕПРАВИЛЬНО — общий для всех профилей  
    data_dir = Path("~/.hermes/my-provider").expanduser()  
    
[/code]
## Тестирование[​](<#testing> "Прямая ссылка на «Тестирование»")
Полный шаблон E2E-тестирования с использованием реального SQLite-провайдера см. в `tests/agent/test_memory_plugin_e2e.py`.
[code] 
    from agent.memory_manager import MemoryManager  
      
    mgr = MemoryManager()  
    mgr.add_provider(my_provider)  
    mgr.initialize_all(session_id="test-1", platform="cli")  
      
    # Тестирование маршрутизации инструментов  
    result = mgr.handle_tool_call("my_tool", {"action": "add", "content": "test"})  
      
    # Тестирование жизненного цикла  
    mgr.sync_all("user msg", "assistant msg")  
    mgr.on_session_end([])  
    mgr.shutdown_all()  
    
[/code]
## Добавление CLI-команд[​](<#adding-cli-commands> "Прямая ссылка на «Добавление CLI-команд»")
Плагины провайдеров памяти могут регистрировать собственное дерево подкоманд CLI (например, `hermes my-provider status`, `hermes my-provider config`). Это использует систему обнаружения на основе соглашений — без изменений в основных файлах.
### Как это работает[​](<#how-it-works> "Прямая ссылка на «Как это работает»")
  1. Добавьте файл `cli.py` в директорию вашего плагина
  2. Определите функцию `register_cli(subparser)`, которая строит дерево argparse
  3. Система плагинов памяти обнаруживает его при запуске через `discover_plugin_cli_commands()`
  4. Ваши команды появляются в виде `hermes <имя-провайдера> <подкоманда>`


**Ограничение активным провайдером:** Ваши CLI-команды отображаются только когда ваш провайдер является активным `memory.provider` в конфигурации. Если пользователь не настроил ваш провайдер, ваши команды не будут показаны в `hermes --help`.
### Пример[​](<#example> "Прямая ссылка на «Пример»")
[code] 
    # plugins/memory/my-provider/cli.py  
      
    def my_command(args):  
        """Обработчик, вызываемый argparse."""  
        sub = getattr(args, "my_command", None)  
        if sub == "status":  
            print("Провайдер активен и подключён.")  
        elif sub == "config":  
            print("Показываю конфигурацию...")  
        else:  
            print("Использование: hermes my-provider <status|config>")  
      
    def register_cli(subparser) -> None:  
        """Построить дерево argparse для hermes my-provider.  
      
        Вызывается discover_plugin_cli_commands() при настройке argparse.  
        """  
        subs = subparser.add_subparsers(dest="my_command")  
        subs.add_parser("status", help="Показать статус провайдера")  
        subs.add_parser("config", help="Показать конфигурацию провайдера")  
        subparser.set_defaults(func=my_command)  
    
[/code]
### Эталонная реализация[​](<#reference-implementation> "Прямая ссылка на «Эталонная реализация»")
Полный пример с 13 подкомандами, кросс-профильным управлением (`--target-profile`) и чтением/записью конфигурации см. в `plugins/memory/honcho/cli.py`.
### Структура директории с CLI[​](<#directory-structure-with-cli> "Прямая ссылка на «Структура директории с CLI»")
[code] 
    plugins/memory/my-provider/  
    ├── __init__.py      # Реализация MemoryProvider + register()  
    ├── plugin.yaml      # Метаданные  
    ├── cli.py           # register_cli(subparser) — CLI-команды  
    └── README.md        # Инструкции по установке  
    
[/code]
## Правило одного провайдера[​](<#single-provider-rule> "Прямая ссылка на «Правило одного провайдера»")
Одновременно может быть активен **только один** внешний провайдер памяти. Если пользователь попытается зарегистрировать второй, MemoryManager отклонит его с предупреждением. Это предотвращает раздувание схем инструментов и конфликты бэкендов.
  * [Структура директории](<#directory-structure>)
  * [Абстрактный базовый класс MemoryProvider](<#the-memoryprovider-abc>)
  * [Обязательные методы](<#required-methods>)
    * [Основной жизненный цикл](<#core-lifecycle>)
    * [Конфигурация](<#config>)
    * [Опциональные хуки](<#optional-hooks>)
  * [Схема конфигурации](<#config-schema>)
  * [Сохранение конфигурации](<#save-config>)
  * [Точка входа плагина](<#plugin-entry-point>)
  * [plugin.yaml](<#pluginyaml>)
  * [Контракт многопоточности](<#threading-contract>)
  * [Изоляция профилей](<#profile-isolation>)
  * [Тестирование](<#testing>)
  * [Добавление CLI-команд](<#adding-cli-commands>)
    * [Как это работает](<#how-it-works>)
    * [Пример](<#example>)
    * [Эталонная реализация](<#reference-implementation>)
    * [Структура директории с CLI](<#directory-structure-with-cli>)
  * [Правило одного провайдера](<#single-provider-rule>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin -->
