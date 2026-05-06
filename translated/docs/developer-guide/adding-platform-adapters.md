На этой странице
Это руководство описывает добавление новой платформы обмена сообщениями в шлюз Hermes. Адаптер платформы подключает Hermes к внешнему сервису обмена сообщениями (Telegram, Discord, WeCom и т.д.), позволяя пользователям взаимодействовать с агентом через этот сервис.
tip
Есть два способа добавления платформы:
  * **Плагин** (рекомендуется для сообщества/сторонних разработчиков): Поместите директорию плагина в `~/.hermes/plugins/` — изменения основного кода не требуются. См. [Путь плагина](<#plugin-path-recommended>) ниже.
  * **Встроенная** : Измените 20+ файлов кода, конфигурации и документации. Используйте [Чек-лист встроенной платформы](<#step-by-step-checklist>) ниже.

## Обзор архитектуры[​](<#architecture-overview> "Прямая ссылка на Обзор архитектуры")
[code] 
    Пользователь ↔ Платформа обмена сообщениями ↔ Адаптер платформы ↔ Исполнитель шлюза ↔ AIAgent  
    
[/code]
Каждый адаптер расширяет `BasePlatformAdapter` из `gateway/platforms/base.py` и реализует:
  * **`connect()`** — Установить соединение (WebSocket, long-poll, HTTP-сервер и т.д.) _(абстрактный)_
  * **`disconnect()`** — Корректное завершение _(абстрактный)_
  * **`send()`** — Отправить текстовое сообщение в чат _(абстрактный)_
  * **`send_typing()`** — Показать индикатор набора текста (необязательное переопределение)
  * **`get_chat_info()`** — Вернуть метаданные чата (необязательное переопределение)


Входящие сообщения принимаются адаптером и передаются через `self.handle_message(event)`, который базовый класс направляет исполнителю шлюза.
## Путь плагина (Рекомендуется)[​](<#plugin-path-recommended> "Прямая ссылка на Путь плагина \(Рекомендуется\)")
Система плагинов позволяет добавить адаптер платформы без изменения основного кода Hermes. Ваш плагин представляет собой директорию с двумя файлами:
[code] 
    ~/.hermes/plugins/my-platform/  
      PLUGIN.yaml      # Метаданные плагина  
      adapter.py       # Класс адаптера + точка входа register()  
    
[/code]
### PLUGIN.yaml[​](<#pluginyaml> "Прямая ссылка на PLUGIN.yaml")
[code] 
    name: my-platform  
    version: 1.0.0  
    description: Мой адаптер пользовательской платформы обмена сообщениями  
    requires_env:  
      - MY_PLATFORM_TOKEN  
      - MY_PLATFORM_CHANNEL  
    
[/code]
### adapter.py[​](<#adapterpy> "Прямая ссылка на adapter.py")
[code] 
    import os  
    from gateway.platforms.base import (  
        BasePlatformAdapter, SendResult, MessageEvent, MessageType,  
    )  
    from gateway.config import Platform, PlatformConfig  
      
      
    class MyPlatformAdapter(BasePlatformAdapter):  
        def __init__(self, config: PlatformConfig):  
            super().__init__(config, Platform("my_platform"))  
            extra = config.extra or {}  
            self.token = os.getenv("MY_PLATFORM_TOKEN") or extra.get("token", "")  
      
        async def connect(self) -> bool:  
            # Подключиться к API платформы, запустить слушатели  
            self._mark_connected()  
            return True  
      
        async def disconnect(self) -> None:  
            self._mark_disconnected()  
      
        async def send(self, chat_id, content, reply_to=None, metadata=None):  
            # Отправить сообщение через API платформы  
            return SendResult(success=True, message_id="...")  
      
        async def get_chat_info(self, chat_id):  
            return {"name": chat_id, "type": "dm"}  
      
      
    def check_requirements() -> bool:  
        return bool(os.getenv("MY_PLATFORM_TOKEN"))  
      
      
    def validate_config(config) -> bool:  
        extra = getattr(config, "extra", {}) or {}  
        return bool(os.getenv("MY_PLATFORM_TOKEN") or extra.get("token"))  
      
      
    def register(ctx):  
        """Точка входа плагина — вызывается системой плагинов Hermes."""  
        ctx.register_platform(  
            name="my_platform",  
            label="My Platform",  
            adapter_factory=lambda cfg: MyPlatformAdapter(cfg),  
            check_fn=check_requirements,  
            validate_config=validate_config,  
            required_env=["MY_PLATFORM_TOKEN"],  
            install_hint="pip install my-platform-sdk",  
            # Переменные окружения для авторизации пользователей на платформе  
            allowed_users_env="MY_PLATFORM_ALLOWED_USERS",  
            allow_all_env="MY_PLATFORM_ALLOW_ALL_USERS",  
            # Лимит длины сообщения для умного разбиения (0 = без лимита)  
            max_message_length=4000,  
            # Подсказка для LLM, внедряемая в системный промпт  
            platform_hint=(  
                "Вы общаетесь через My Platform. "  
                "Она поддерживает Markdown-форматирование."  
            ),  
            # Отображение  
            emoji="💬",  
        )  
      
        # Опционально: зарегистрировать инструменты, специфичные для платформы  
        ctx.register_tool(  
            name="my_platform_search",  
            toolset="my_platform",  
            schema={...},  
            handler=my_search_handler,  
        )  
    
[/code]
### Конфигурация[​](<#configuration> "Прямая ссылка на Конфигурация")
Пользователи настраивают платформу в `config.yaml`:
[code] 
    gateway:  
      platforms:  
        my_platform:  
          enabled: true  
          extra:  
            token: "..."  
            channel: "#general"  
    
[/code]
Или через переменные окружения (которые адаптер считывает в `__init__`).
### Что система плагинов обрабатывает автоматически[​](<#what-the-plugin-system-handles-automatically> "Прямая ссылка на Что система плагинов обрабатывает автоматически")
Когда вы вызываете `ctx.register_platform()», следующие точки интеграции обрабатываются за вас — изменения основного кода не требуются:
Точка интеграции| Как это работает  
---|---  
Создание адаптера шлюза| Реестр проверяется до встроенной цепочки if/elif  
Парсинг конфигурации| `Platform._missing_()` принимает любое имя платформы  
Проверка подключенной платформы| Вызывается `Registry validate_config()`  
Авторизация пользователя| Проверяется `allowed_users_env` / `allow_all_env`  
Доставка по расписанию (cron)| `Platform()` разрешает любое зарегистрированное имя  
Инструмент send_message| Маршрутизируется через активный адаптер шлюза  
Кроссплатформенная доставка вебхуков| Реестр проверяется на известные платформы  
Доступ к команде `/update`| Флаг `allow_update_command`  
Каталог каналов| Платформы-плагины включаются в перечисление  
Подсказки для системного промпта| `platform_hint` внедряется в контекст LLM  
Разбиение сообщений| `max_message_length` для умного разделения  
Сокрытие PII| Флаг `pii_safe`  
`hermes status`| Показывает платформы-плагины с тегом `(plugin)`  
`hermes gateway setup`| Платформы-плагины появляются в меню настройки  
`hermes tools` / `hermes skills`| Платформы-плагины в конфигурации на платформу  
Блокировка токена (мульти-профиль)| Используйте `acquire_scoped_lock()` в вашем `connect()`  
Предупреждение об осиротевшей конфигурации| Информативное сообщение в логе, если плагин отсутствует  
### Эталонная реализация[​](<#reference-implementation> "Прямая ссылка на Эталонная реализация")
Смотрите `plugins/platforms/irc/` в репозитории для полного рабочего примера — полноценный асинхронный IRC-адаптер без внешних зависимостей.
* * *
## Пошаговый чек-лист (Встроенный путь)[​](<#step-by-step-checklist-built-in-path> "Прямая ссылка на Пошаговый чек-лист \(Встроенный путь\)"))
note
Этот чек-лист предназначен для добавления платформы непосредственно в основной код Hermes — обычно выполняется основными участниками для официально поддерживаемых платформ. Сторонние платформы должны использовать [Путь плагина](<#plugin-path-recommended>) выше.
### 1\. Перечисление платформ[​](<#1-platform-enum> "Прямая ссылка на 1. Перечисление платформ")
Добавьте вашу платформу в перечисление `Platform` в `gateway/config.py`:
[code] 
    class Platform(str, Enum):  
        # ... существующие платформы ...  
        NEWPLAT = "newplat"  
    
[/code]
### 2\. Файл адаптера[​](<#2-adapter-file> "Прямая ссылка на 2. Файл адаптера")
Создайте `gateway/platforms/newplat.py`:
[code] 
    from gateway.config import Platform, PlatformConfig  
    from gateway.platforms.base import (  
        BasePlatformAdapter, MessageEvent, MessageType, SendResult,  
    )  
      
    def check_newplat_requirements() -> bool:  
        """Вернуть True, если зависимости доступны."""  
        return SOME_SDK_AVAILABLE  
      
    class NewPlatAdapter(BasePlatformAdapter):  
        def __init__(self, config: PlatformConfig):  
            super().__init__(config, Platform.NEWPLAT)  
            # Чтение конфигурации из словаря config.extra  
            extra = config.extra or {}  
            self._api_key = extra.get("api_key") or os.getenv("NEWPLAT_API_KEY", "")  
      
        async def connect(self) -> bool:  
            # Настроить соединение, запустить опрос/вебхук  
            self._mark_connected()  
            return True  
      
        async def disconnect(self) -> None:  
            self._running = False  
            self._mark_disconnected()  
      
        async def send(self, chat_id, content, reply_to=None, metadata=None):  
            # Отправить сообщение через API платформы  
            return SendResult(success=True, message_id="...")  
      
        async def get_chat_info(self, chat_id):  
            return {"name": chat_id, "type": "dm"}  
    
[/code]
Для входящих сообщений создайте `MessageEvent` и вызовите `self.handle_message(event)`:
[code] 
    source = self.build_source(  
        chat_id=chat_id,  
        chat_name=name,  
        chat_type="dm",  # или "group"  
        user_id=user_id,  
        user_name=user_name,  
    )  
    event = MessageEvent(  
        text=content,  
        message_type=MessageType.TEXT,  
        source=source,  
        message_id=msg_id,  
    )  
    await self.handle_message(event)  
    
[/code]
### 3\. Конфигурация шлюза (`gateway/config.py`)[​](<#3-gateway-config-gatewayconfigpy> "Прямая ссылка на 3-gateway-config-gatewayconfigpy")
Три точки касания:
  1. **`get_connected_platforms()`** — Добавьте проверку обязательных учетных данных для вашей платформы
  2. **`load_gateway_config()`** — Добавьте запись карты токенов окружения: `Platform.NEWPLAT: "NEWPLAT_TOKEN"`
  3. **`_apply_env_overrides()`** — Сопоставьте все переменные окружения `NEWPLAT_*` с конфигурацией


### 4\. Исполнитель шлюза (`gateway/run.py`)[​](<#4-gateway-runner-gatewayrunpy> "Прямая ссылка на 4-gateway-runner-gatewayrunpy")
Пять точек касания:
  1. **`_create_adapter()`** — Добавьте ветвь `elif platform == Platform.NEWPLAT:`
  2. **`_is_user_authorized()` карта allowed_users** — `Platform.NEWPLAT: "NEWPLAT_ALLOWED_USERS"`
  3. **`_is_user_authorized()` карта allow_all** — `Platform.NEWPLAT: "NEWPLAT_ALLOW_ALL_USERS"`
  4. **Ранняя проверка окружения`_any_allowlist` кортеж** — Добавьте `"NEWPLAT_ALLOWED_USERS"`
  5. **Ранняя проверка окружения`_allow_all` кортеж** — Добавьте `"NEWPLAT_ALLOW_ALL_USERS"`
  6. **`_UPDATE_ALLOWED_PLATFORMS` frozenset** — Добавьте `Platform.NEWPLAT`


### 5\. Кроссплатформенная доставка[​](<#5-cross-platform-delivery> "Прямая ссылка на 5. Кроссплатформенная доставка")
  1. **`gateway/platforms/webhook.py`** — Добавьте `"newplat"» в кортеж типов доставки
  2. **`cron/scheduler.py`** — Добавьте в frozenset `_KNOWN_DELIVERY_PLATFORMS» и карту платформ `_deliver_result()`


### 6\. Интеграция с CLI[​](<#6-cli-integration> "Прямая ссылка на 6. Интеграция с CLI")
  1. **`hermes_cli/config.py`** — Добавьте все переменные `NEWPLAT_*` в `_EXTRA_ENV_KEYS`
  2. **`hermes_cli/gateway.py`** — Добавьте запись в список `_PLATFORMS` с ключом, меткой, эмодзи, token_var, setup_instructions и vars
  3. **`hermes_cli/platforms.py`** — Добавьте запись `PlatformInfo` с меткой и default_toolset (используется в TUI `skills_config` и `tools_config`)
  4. **`hermes_cli/setup.py`** — Добавьте функцию `_setup_newplat()` (может делегировать в `gateway.py`) и добавьте кортеж в список платформ обмена сообщениями
  5. **`hermes_cli/status.py`** — Добавьте запись обнаружения платформы: `"NewPlat": ("NEWPLAT_TOKEN", "NEWPLAT_HOME_CHANNEL")`
  6. **`hermes_cli/dump.py`** — Добавьте `"newplat": "NEWPLAT_TOKEN"` в словарь обнаружения платформ


### 7\. Инструменты[​](<#7-tools> "Прямая ссылка на 7. Инструменты")
  1. **`tools/send_message_tool.py`** — Добавьте `"newplat": Platform.NEWPLAT` в карту платформ
  2. **`tools/cronjob_tools.py`** — Добавьте `newplat` в строку описания цели доставки


### 8\. Наборы инструментов[​](<#8-toolsets> "Прямая ссылка на 8. Наборы инструментов")
  1. **`toolsets.py`** — Добавьте определение набора инструментов `"hermes-newplat"` с `_HERMES_CORE_TOOLS`
  2. **`toolsets.py`** — Добавьте `"hermes-newplat"` в список includes для `"hermes-gateway"`


### 9\. Опционально: Подсказки для платформы[​](<#9-optional-platform-hints> "Прямая ссылка на 9. Опционально: Подсказки для платформы")
**`agent/prompt_builder.py`** — Если ваша платформа имеет специфические ограничения рендеринга (нет Markdown, лимиты длины сообщений и т.д.), добавьте запись в словарь `_PLATFORM_HINTS`. Это внедряет специфические для платформы рекомендации в системный промпт:
[code] 
    _PLATFORM_HINTS = {  
        # ...  
        "newplat": (  
            "Вы общаетесь через NewPlat. Он поддерживает Markdown-форматирование, "  
            "но имеет ограничение на длину сообщения в 4000 символов."  
        ),  
    }  
    
[/code]
Не все платформы нуждаются в подсказках — добавляйте только если поведение агента должно отличаться.
### 10\. Тесты[​](<#10-tests> "Прямая ссылка на 10. Тесты")
Создайте `tests/gateway/test_newplat.py`, покрывающий:
  * Создание адаптера из конфигурации
  * Построение события сообщения
  * Метод send (мокировать внешнее API)
  * Специфические функции платформы (шифрование, маршрутизация и т.д.)


### 11\. Документация[​](<#11-documentation> "Прямая ссылка на 11. Документация")
Файл| Что добавить  
---|---  
`website/docs/user-guide/messaging/newplat.md`| Полная страница настройки платформы  
`website/docs/user-guide/messaging/index.md`| Таблица сравнения платформ, диаграмма архитектуры, таблица наборов инструментов, раздел безопасности, ссылка на следующие шаги  
`website/docs/reference/environment-variables.md`| Все переменные окружения NEWPLAT_*  
`website/docs/reference/toolsets-reference.md`| Набор инструментов hermes-newplat  
`website/docs/integrations/index.md`| Ссылка на платформу  
`website/sidebars.ts`| Запись в боковом меню для страницы документации  
`website/docs/developer-guide/architecture.md`| Количество адаптеров + перечисление  
`website/docs/developer-guide/gateway-internals.md`| Перечисление файлов адаптеров  
## Аудит паритета[​](<#parity-audit> "Прямая ссылка на Аудит паритета")
Перед тем как пометить PR новой платформы как завершенный, выполните аудит паритета относительно установленной платформы:
[code] 
    # Найти все .py файлы, упоминающие эталонную платформу  
    search_files "bluebubbles" output_mode="files_only" file_glob="*.py"  
      
    # Найти все .py файлы, упоминающие новую платформу  
    search_files "newplat" output_mode="files_only" file_glob="*.py"  
      
    # Любой файл из первого набора, отсутствующий во втором, является потенциальным пробелом  
    
[/code]
Повторите для файлов `.md` и `.ts`. Исследуйте каждый пробел — это перечисление платформы (требует обновления) или специфическая ссылка на платформу (пропустить)?
## Общие паттерны[​](<#common-patterns> "Прямая ссылка на Общие паттерны")
### Адаптеры с long-polling[​](<#long-poll-adapters> "Прямая ссылка на Адаптеры с long-polling")
Если ваш адаптер использует long-polling (например, Telegram или Weixin), используйте задачу цикла опроса:
[code] 
    async def connect(self):  
        self._poll_task = asyncio.create_task(self._poll_loop())  
        self._mark_connected()  
      
    async def _poll_loop(self):  
        while self._running:  
            messages = await self._fetch_updates()  
            for msg in messages:  
                await self.handle_message(self._build_event(msg))  
    
[/code]
### Адаптеры с обратным вызовом/вебхуком[​](<#callbackwebhook-adapters> "Прямая ссылка на Адаптеры с обратным вызовом/вебхуком")
Если платформа отправляет сообщения на вашу конечную точку (например, WeCom Callback), запустите HTTP-сервер:
[code] 
    async def connect(self):  
        self._app = web.Application()  
        self._app.router.add_post("/callback", self._handle_callback)  
        # ... запустить aiohttp сервер  
        self._mark_connected()  
      
    async def _handle_callback(self, request):  
        event = self._build_event(await request.text())  
        await self._message_queue.put(event)  
        return web.Response(text="success")  # Немедленно подтвердить  
    
[/code]
Для платформ с жесткими сроками ответа (например, лимит WeCom в 5 секунд) всегда немедленно подтверждайте получение и доставляйте ответ агента заранее через API позже. Сессии агента длятся 3–30 минут — встроенные ответы в окне обратного вызова невозможны.
### Блокировки токенов[​](<#token-locks> "Прямая ссылка на Блокировки токенов")
Если адаптер поддерживает постоянное соединение с уникальными учетными данными, добавьте блокировку области видимости, чтобы предотвратить использование одних и тех же учетных данных двумя профилями:
[code] 
    from gateway.status import acquire_scoped_lock, release_scoped_lock  
      
    async def connect(self):  
        if not acquire_scoped_lock("newplat", self._token):  
            logger.error("Токен уже используется другим профилем")  
            return False  
        # ... подключение  
      
    async def disconnect(self):  
        release_scoped_lock("newplat", self._token)  
    
[/code]
## Эталонные реализации[​](<#reference-implementations> "Прямая ссылка на Эталонные реализации")
Адаптер| Паттерн| Сложность| Хороший пример для  
---|---|---|---  
`bluebubbles.py`| REST + вебхук| Средняя| Простая интеграция REST API  
`weixin.py`| Long-poll + CDN| Высокая| Обработка медиа, шифрование  
`wecom_callback.py`| Обратный вызов/вебхук| Средняя| HTTP-сервер, AES шифрование, мульти-приложение  
`telegram.py`| Long-poll + Bot API| Высокая| Полнофункциональный адаптер с группами, тредами  
  * [Обзор архитектуры](<#architecture-overview>)
  * [Путь плагина (Рекомендуется)](<#plugin-path-recommended>)
    * [PLUGIN.yaml](<#pluginyaml>)
    * [adapter.py](<#adapterpy>)
    * [Конфигурация](<#configuration>)
    * [Что система плагинов обрабатывает автоматически](<#what-the-plugin-system-handles-automatically>)
    * [Эталонная реализация](<#reference-implementation>)
  * [Пошаговый чек-лист (Встроенный путь)](<#step-by-step-checklist-built-in-path>)
    * [1. Перечисление платформ](<#1-platform-enum>)
    * [2. Файл адаптера](<#2-adapter-file>)
    * [3. Конфигурация шлюза (`gateway/config.py`)](<#3-gateway-config-gatewayconfigpy>)
    * [4. Исполнитель шлюза (`gateway/run.py`)](<#4-gateway-runner-gatewayrunpy>)
    * [5. Кроссплатформенная доставка](<#5-cross-platform-delivery>)
    * [6. Интеграция с CLI](<#6-cli-integration>)
    * [7. Инструменты](<#7-tools>)
    * [8. Наборы инструментов](<#8-toolsets>)
    * [9. Опционально: Подсказки для платформы](<#9-optional-platform-hints>)
    * [10. Тесты](<#10-tests>)
    * [11. Документация](<#11-documentation>)
  * [Аудит паритета](<#parity-audit>)
  * [Общие паттерны](<#common-patterns>)
    * [Адаптеры с long-polling](<#long-poll-adapters>)
    * [Адаптеры с обратным вызовом/вебхуком](<#callbackwebhook-adapters>)
    * [Блокировки токенов](<#token-locks>)
  * [Эталонные реализации](<#reference-implementations>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters -->