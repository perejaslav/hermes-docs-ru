На этой странице
Плагины провайдеров моделей объявляют бэкенд инференса — OpenAI-совместимую конечную точку, сервер Anthropic Messages, Responses API в стиле Codex или нативный интерфейс Bedrock — через который Hermes может направлять вызовы `AIAgent`. Каждый встроенный провайдер (OpenRouter, Anthropic, GMI, DeepSeek, Nvidia, …) поставляется как один из таких плагинов. Сторонние разработчики могут добавлять свои, поместив директорию в `$HERMES_HOME/plugins/model-providers/` без каких-либо изменений в репозитории.

tip
Плагины провайдеров моделей — это третий вид **провайдерских плагинов**. Другие — это [Плагины провайдеров памяти](</docs/developer-guide/memory-provider-plugin>) (межсессионные знания) и [Плагины контекстных движков](</docs/developer-guide/context-engine-plugin>) (стратегии сжатия контекста). Все три следуют одному шаблону «помести директорию, объяви профиль, без правок репозитория».

## Как работает обнаружение[​](<#how-discovery-works> "Прямая ссылка на Как работает обнаружение")

`providers/__init__.py._discover_providers()` выполняется лениво при первом вызове любого кода, обращающегося к `get_provider_profile()` или `list_providers()`. Порядок обнаружения:
  1. **Встроенные плагины** — `<repo>/plugins/model-providers/<name>/` — поставляются с Hermes
  2. **Пользовательские плагины** — `$HERMES_HOME/plugins/model-providers/<name>/` — поместите в любую директорию; не требуется перезапуск для последующих сессий
  3. **Устаревшие однофайловые** — `<repo>/providers/<name>.py` — обратная совместимость для внешних редактируемых установок


**Пользовательские плагины переопределяют встроенные плагины с тем же именем**, потому что `register_provider()` работает по принципу «последний записавший побеждает». Поместите директорию `$HERMES_HOME/plugins/model-providers/gmi/`, чтобы заменить встроенный профиль GMI без изменения репозитория.

## Структура директории[​](<#directory-structure> "Прямая ссылка на Структура директории")

[code]
    plugins/model-providers/my-provider/
    ├── __init__.py       # Вызывает register_provider(profile) на уровне модуля
    ├── plugin.yaml       # kind: model-provider + метаданные (опционально, но рекомендуется)
    └── README.md         # Инструкции по настройке (опционально)
    
[/code]
Единственный обязательный файл — `__init__.py`. `plugin.yaml` используется командой `hermes plugins` для интроспекции и общим PluginManager для маршрутизации плагина к правильному загрузчику; без него общий загрузчик использует эвристику на основе исходного текста.

## Минимальный пример — простой провайдер с API-ключом[​](<#minimal-example--a-simple-api-key-provider> "Прямая ссылка на Минимальный пример — простой провайдер с API-ключом")

[code]
    # plugins/model-providers/acme-inference/__init__.py
    from providers import register_provider
    from providers.base import ProviderProfile
    
    acme = ProviderProfile(
        name="acme-inference",
        aliases=("acme",),
        display_name="Acme Inference",
        description="Acme — OpenAI-совместимое прямое API",
        signup_url="https://acme.example.com/keys",
        env_vars=("ACME_API_KEY", "ACME_BASE_URL"),
        base_url="https://api.acme.example.com/v1",
        auth_type="api_key",
        default_aux_model="acme-small-fast",
        fallback_models=(
            "acme-large-v3",
            "acme-medium-v3",
            "acme-small-fast",
        ),
    )
    
    register_provider(acme)
    
[/code]
[code]
    # plugins/model-providers/acme-inference/plugin.yaml
    name: acme-inference
    kind: model-provider
    version: 1.0.0
    description: Acme Inference — OpenAI-совместимое прямое API
    author: Ваше Имя
    
[/code]
Вот и всё. После размещения этих двух файлов следующее **автоматически подключается** без других правок:

Интеграция| Где| Что получает
---|---|---
Разрешение учётных данных| `hermes_cli/auth.py`| `PROVIDER_REGISTRY["acme-inference"]` заполняется из профиля
Флаг `--provider` в CLI| `hermes_cli/main.py`| Принимает `acme-inference`
Выбор `hermes model`| `hermes_cli/models.py`| Появляется в `CANONICAL_PROVIDERS`, список моделей получается из `{base_url}/models`
`hermes doctor`| `hermes_cli/doctor.py`| Проверка `ACME_API_KEY` + запрос к `{base_url}/models`
`hermes setup`| `hermes_cli/config.py`| `ACME_API_KEY` появляется в `OPTIONAL_ENV_VARS` и мастере настройки
Обратное сопоставление URL| `agent/model_metadata.py`| Хост → имя провайдера для автоопределения
Вспомогательная модель| `agent/auxiliary_client.py`| Использует `default_aux_model` для сжатия / суммаризации
Разрешение во время выполнения| `hermes_cli/runtime_provider.py`| Возвращает правильные `base_url`, `api_key`, `api_mode`
Транспорт| `agent/transports/chat_completions.py`| Путь профиля генерирует kwargs через `prepare_messages` / `build_extra_body` / `build_api_kwargs_extras`

## Поля ProviderProfile[​](<#providerprofile-fields> "Прямая ссылка на Поля ProviderProfile")

Полное определение в `providers/base.py`. Наиболее полезные:

Поле| Тип| Назначение
---|---|---
`name`| str| Канонический id — соответствует вариантам `--provider` и `HERMES_INFERENCE_PROVIDER`
`aliases`| `tuple[str, ...]`| Альтернативные имена, разрешаемые `get_provider_profile()` (например `grok` → `xai`)
`api_mode`| str| `chat_completions` | `codex_responses` | `anthropic_messages` | `bedrock_converse`
`display_name`| str| Человекочитаемая метка, показываемая в выборе `hermes model`
`description`| str| Подзаголовок в выборе
`signup_url`| str| Показывается при первой настройке («получить API-ключ здесь»)
`env_vars`| `tuple[str, ...]`| Переменные окружения для API-ключа в порядке приоритета; запись `*_BASE_URL` в конце используется как пользовательское переопределение базового URL
`base_url`| str| Конечная точка инференса по умолчанию
`models_url`| str| Явный URL каталога (по умолчанию используется `{base_url}/models`)
`auth_type`| str| `api_key` | `oauth_device_code` | `oauth_external` | `copilot` | `aws_sdk` | `external_process`
`fallback_models`| `tuple[str, ...]`| Подобранный список, показываемый, когда получение живого каталога не удаётся
`default_headers`| `dict[str, str]`| Отправляется в каждом запросе (например, Copilot `Editor-Version`)
`fixed_temperature`| Any| `None` = использовать значение вызывающего; сентинел `OMIT_TEMPERATURE` = не отправлять температуру вообще (Kimi)
`default_max_tokens`| `int | None`| Лимит max_tokens на уровне провайдера (Nvidia: 16384)
`default_aux_model`| str| Дешёвая модель для вспомогательных задач (сжатие, зрение, суммаризация)

## Переопределяемые хуки[​](<#overridable-hooks> "Прямая ссылка на Переопределяемые хуки")

Унаследуйтесь от `ProviderProfile` для нетривиальных особенностей:
[code]
    from typing import Any
    from providers.base import ProviderProfile
    
    class AcmeProfile(ProviderProfile):
        def prepare_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
            """Специфичная для провайдера предобработка сообщений. Выполняется после
            санитизации codex, перед заменой developer-роли. По умолчанию: сквозная передача."""
            # Пример: Qwen нормализует текстовое содержимое в массив частей
            # и внедряет cache_control; Kimi перезаписывает JSON вызова инструментов
            return messages
    
        def build_extra_body(self, *, session_id=None, **context) -> dict:
            """Специфичные для провайдера поля extra_body, объединяемые с вызовом API.
            Контекст включает: session_id, provider_preferences, model, base_url,
            reasoning_config. По умолчанию: пустой словарь."""
            # Пример: блок provider-preferences OpenRouter,
            # преобразование thinking_config Gemini.
            return {}
    
        def build_api_kwargs_extras(self, *, reasoning_config=None, **context):
            """Возвращает (extra_body_additions, top_level_kwargs). Нужно, когда некоторые
            поля идут на верхний уровень (reasoning_effort у Kimi), а некоторые — в extra_body
            (словарь reasoning у OpenRouter). По умолчанию: ({}, {})."""
            return {}, {}
    
        def fetch_models(self, *, api_key=None, timeout=8.0) -> list[str] | None:
            """Получение живого каталога. По умолчанию обращается к {models_url или base_url}/models
            с Bearer-авторизацией. Переопределите для: нестандартной аутентификации (Anthropic),
            отсутствия REST-эндпоинта (Bedrock → None) или публичных/неаутентифицированных каталогов (OpenRouter)."""
            return super().fetch_models(api_key=api_key, timeout=timeout)
    
[/code]

## Справочные примеры хуков[​](<#hook-reference-examples> "Прямая ссылка на Справочные примеры хуков")

Посмотрите на эти встроенные плагины для идиом:

Плагин| Почему смотреть
---|---
`plugins/model-providers/openrouter/`| Агрегатор с предпочтениями провайдера, публичный каталог моделей
`plugins/model-providers/gemini/`| Преобразование `thinking_config` (нативные + вложенные формы OpenAI-совместимости)
`plugins/model-providers/kimi-coding/`| `OMIT_TEMPERATURE`, `extra_body.thinking`, `reasoning_effort` на верхнем уровне
`plugins/model-providers/qwen-oauth/`| Нормализация сообщений, внедрение `cache_control`, VL высокое разрешение
`plugins/model-providers/nous/`| Теги атрибуции, «опускать reasoning, когда отключено»
`plugins/model-providers/custom/`| Особенности `num_ctx` от Ollama + `think: false`
`plugins/model-providers/bedrock/`| `api_mode="bedrock_converse"`, `fetch_models` возвращает None (нет REST-эндпоинта)

## Пользовательские переопределения — замена встроенного без правки репозитория[​](<#user-overrides--replace-a-built-in-without-editing-the-repo> "Прямая ссылка на Пользовательские переопределения — замена встроенного без правки репозитория")

Допустим, вы хотите направить `gmi` на ваш приватный staging-эндпоинт для тестирования. Создайте `~/.hermes/plugins/model-providers/gmi/__init__.py`:
[code]
    from providers import register_provider
    from providers.base import ProviderProfile
    
    register_provider(ProviderProfile(
        name="gmi",
        aliases=("gmi-cloud", "gmicloud"),
        env_vars=("GMI_API_KEY",),
        base_url="https://gmi-staging.internal.example.com/v1",
        auth_type="api_key",
        default_aux_model="google/gemini-3.1-flash-lite-preview",
    ))
    
[/code]
В следующей сессии `get_provider_profile("gmi").base_url` вернёт staging URL. Никаких патчей репозитория, никакой пересборки. Поскольку пользовательские плагины обнаруживаются после встроенных, вызов `register_provider()` пользователя побеждает.

## Выбор api_mode[​](<#api_mode-selection> "Прямая ссылка на Выбор api_mode")

Распознаются четыре значения. Hermes выбирает на основе:
  1. Явное переопределение пользователем (`config.yaml` `model.api_mode`, если задано)
  2. Диспетчеризация по модели OpenCode (`opencode_model_api_mode` для Zen и Go)
  3. Автоопределение URL — суффикс `/anthropic` → `anthropic_messages`, `api.openai.com` → `codex_responses`, `api.x.ai` → `codex_responses`, `/coding` на доменах Kimi → `chat_completions`
  4. **`api_mode` профиля** как запасной вариант, когда определение URL ничего не находит
  5. По умолчанию `chat_completions`


Установите `profile.api_mode` в соответствии со значением по умолчанию, которое использует ваш провайдер — это действует как подсказка. Пользовательские переопределения URL всё равно имеют приоритет.

## Типы аутентификации[​](<#auth-types> "Прямая ссылка на Типы аутентификации")

`auth_type`| Значение| Кто использует
---|---|---
`api_key`| Одна переменная окружения содержит статический API-ключ| Большинство провайдеров
`oauth_device_code`| OAuth-поток с кодом устройства| —
`oauth_external`| Пользователь входит где-то ещё, токены попадают в `auth.json`| Anthropic OAuth, MiniMax OAuth, Gemini Cloud Code, Qwen Portal, Nous Portal
`copilot`| Цикл обновления токена GitHub Copilot| Только плагин `copilot`
`aws_sdk`| Цепочка учётных данных AWS SDK (роль IAM, профиль, окружение)| Только плагин `bedrock`
`external_process`| Аутентификация обрабатывается дочерним процессом, который запускает агент| Только плагин `copilot-acp`

`auth_type` определяет, какие кодовые пути обрабатывают ваш провайдер как «простой провайдер с API-ключом» — если это не `api_key`, PluginManager всё равно записывает манифест, но автоматизация на уровне CLI Hermes (проверки doctor, флаг `--provider`, делегирование мастеру настройки) может пропустить его.

## Время обнаружения[​](<#discovery-timing> "Прямая ссылка на Время обнаружения")

Обнаружение провайдеров является **ленивым** — запускается первым вызовом `get_provider_profile()` или `list_providers()` в процессе. На практике это происходит рано при запуске (загрузка модуля `auth.py` расширяет `PROVIDER_REGISTRY` активно). Если вам нужно проверить, что ваш плагин загрузился, выполните:
[code]
    hermes doctor
    
[/code]
— успешный профиль с `auth_type="api_key"` появится в разделе Provider Connectivity с запросом к `/models`.

Для программной проверки:
[code]
    from providers import list_providers
    for p in list_providers():
        print(p.name, p.base_url, p.api_mode)
    
[/code]

## Тестирование вашего плагина[​](<#testing-your-plugin> "Прямая ссылка на Тестирование вашего плагина")

Направьте `HERMES_HOME` во временную директорию, чтобы не загрязнять вашу реальную конфигурацию:
[code]
    export HERMES_HOME=/tmp/hermes-plugin-test
    mkdir -p $HERMES_HOME/plugins/model-providers/my-provider
    cat > $HERMES_HOME/plugins/model-providers/my-provider/__init__.py <<'EOF'
    from providers import register_provider
    from providers.base import ProviderProfile
    register_provider(ProviderProfile(
        name="my-provider",
        env_vars=("MY_API_KEY",),
        base_url="https://api.my-provider.example.com/v1",
        auth_type="api_key",
    ))
    EOF
    
    export MY_API_KEY=your-test-key
    hermes -z "hello" --provider my-provider -m some-model
    
[/code]

## Интеграция с общим PluginManager[​](<#general-pluginmanager-integration> "Прямая ссылка на Интеграция с общим PluginManager")

Общий `PluginManager` (то, с чем работает `hermes plugins`) **видит** плагины провайдеров моделей, но не импортирует их — `providers/__init__.py` владеет их жизненным циклом. Менеджер записывает манифест для интроспекции и категоризирует по `kind: model-provider`. Когда вы помещаете немаркированный пользовательский плагин в `$HERMES_HOME/plugins/`, который вызывает `register_provider` с `ProviderProfile`, менеджер автоматически приводит его к `kind: model-provider` через эвристику на основе исходного текста — поэтому плагин всё равно маршрутизируется правильно, даже без `plugin.yaml`.

## Распространение через pip[​](<#distribute-via-pip> "Прямая ссылка на Распространение через pip")

Как и любой плагин Hermes, провайдеры моделей могут распространяться как pip-пакет. Добавьте точку входа в ваш `pyproject.toml`:
[code]
    [project.entry-points."hermes.plugins"]
    acme-inference = "acme_hermes_plugin:register"
    
[/code]
…где `acme_hermes_plugin:register` — это функция, которая вызывает `register_provider(profile)`. Общий PluginManager подхватывает плагины точек входа во время `discover_and_load()`. Для pip-плагинов с `kind: model-provider` вам всё равно нужно объявить kind в вашем манифесте (или полагаться на эвристику исходного текста).
Смотрите [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin#distribute-via-pip>) для полной настройки точек входа.

## Связанные страницы[​](<#related-pages> "Прямая ссылка на Связанные страницы")

  * [Среда выполнения провайдера](</docs/developer-guide/provider-runtime>) — приоритет разрешения + где каждый слой читает профиль
  * [Добавление провайдеров](</docs/developer-guide/adding-providers>) — сквозной чеклист для новых бэкендов инференса (охватывает как быстрый путь через плагин, так и полную интеграцию CLI/аутентификации)
  * [Плагины провайдеров памяти](</docs/developer-guide/memory-provider-plugin>)
  * [Плагины контекстных движков](</docs/developer-guide/context-engine-plugin>)
  * [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>) — общее руководство по созданию плагинов


  * [Как работает обнаружение](<#how-discovery-works>)
  * [Структура директории](<#directory-structure>)
  * [Минимальный пример — простой провайдер с API-ключом](<#minimal-example--a-simple-api-key-provider>)
  * [Поля ProviderProfile](<#providerprofile-fields>)
  * [Переопределяемые хуки](<#overridable-hooks>)
  * [Справочные примеры хуков](<#hook-reference-examples>)
  * [Пользовательские переопределения — замена встроенного без правки репозитория](<#user-overrides--replace-a-built-in-without-editing-the-repo>)
  * [Выбор api_mode](<#api_mode-selection>)
  * [Типы аутентификации](<#auth-types>)
  * [Время обнаружения](<#discovery-timing>)
  * [Тестирование вашего плагина](<#testing-your-plugin>)
  * [Интеграция с общим PluginManager](<#general-pluginmanager-integration>)
  * [Распространение через pip](<#distribute-via-pip>)
  * [Связанные страницы](<#related-pages>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin -->
