On this page

Плагины генерации изображений (image-gen provider plugins) регистрируют бэкенд, который обрабатывает каждый вызов инструмента `image_generate` — DALL·E, gpt-image, Grok, Flux, Imagen, Stable Diffusion, fal, Replicate, локальный ComfyUI и всё остальное. Встроенные провайдеры (OpenAI, OpenAI-Codex, xAI) поставляются как плагины. Вы можете добавить новый или переопределить встроенный, поместив директорию в `plugins/image_gen/<name>/`.

tip
Генерация изображений — один из нескольких **backend-плагинов**, которые поддерживает Hermes. Другие (с более специализированными ABC) — это [Memory Provider Plugins](</docs/developer-guide/memory-provider-plugin>), [Context Engine Plugins](</docs/developer-guide/context-engine-plugin>) и [Model Provider Plugins](</docs/developer-guide/model-provider-plugin>). Плагины общего назначения (инструменты, хуки, CLI-команды) описаны в разделе [Build a Hermes Plugin](</docs/guides/build-a-hermes-plugin>).

## Как работает обнаружение[​](<#how-discovery-works> "Прямая ссылка на Как работает обнаружение")

Hermes сканирует бэкенды генерации изображений в трёх местах:

  1. **Встроенные** — `<repo>/plugins/image_gen/<name>/` (автоматически загружаются с `kind: backend`, всегда доступны)
  2. **Пользовательские** — `~/.hermes/plugins/image_gen/<name>/` (подключаются через `plugins.enabled`)
  3. **Pip** — пакеты, объявляющие точку входа `hermes_agent.plugins`

Функция `register(ctx)` каждого плагина вызывает `ctx.register_image_gen_provider(...)` — это помещает провайдера в реестр в `agent/image_gen_registry.py`. Активный провайдер выбирается через `image_gen.provider` в `config.yaml`; `hermes tools` помогает пользователю пройти выбор.

Обёртка инструмента `image_generate` запрашивает у реестра активного провайдера и направляет запрос туда. Если ни один провайдер не зарегистрирован, инструмент выводит понятную ошибку с указанием на `hermes tools`.

## Структура директории[​](<#directory-structure> "Прямая ссылка на Структура директории")

[code] 
    plugins/image_gen/my-backend/  
    ├── __init__.py      # Подкласс ImageGenProvider + register()  
    └── plugin.yaml      # Манифест с kind: backend  
    
[/code]

На этом встроенный плагин готов. Пользовательские плагины в `~/.hermes/plugins/image_gen/<name>/` нужно добавить в `plugins.enabled` в `config.yaml` (или выполнить `hermes plugins enable <name>`).

## Абстрактный базовый класс ImageGenProvider[​](<#the-imagegenprovider-abc> "Прямая ссылка на Абстрактный базовый класс ImageGenProvider")

Унаследуйтесь от `agent.image_gen_provider.ImageGenProvider`. Единственные обязательные члены — это свойство `name` и метод `generate()` — всё остальное имеет разумные значения по умолчанию:

[code] 
    # plugins/image_gen/my-backend/__init__.py  
    from typing import Any, Dict, List, Optional  
    import os  
      
    from agent.image_gen_provider import (  
        DEFAULT_ASPECT_RATIO,  
        ImageGenProvider,  
        error_response,  
        resolve_aspect_ratio,  
        save_b64_image,  
        success_response,  
    )  
      
      
    class MyBackendImageGenProvider(ImageGenProvider):  
        @property  
        def name(self) -> str:  
            # Стабильный идентификатор, используемый в конфиге image_gen.provider. Только нижний регистр, без пробелов.  
            return "my-backend"  
      
        @property  
        def display_name(self) -> str:  
            # Человеческое название, отображаемое в `hermes tools`. По умолчанию name.title(), если не указано.  
            return "My Backend"  
      
        def is_available(self) -> bool:  
            # Верните False, если отсутствуют учётные данные или зависимости.  
            # Шлюз доступности инструмента вызывает это перед отправкой запроса.  
            if not os.environ.get("MY_BACKEND_API_KEY"):  
                return False  
            try:  
                import my_backend_sdk  # noqa: F401  
            except ImportError:  
                return False  
            return True  
      
        def list_models(self) -> List[Dict[str, Any]]:  
            # Каталог, отображаемый в выборе моделей `hermes tools`.  
            return [  
                {  
                    "id": "my-model-fast",  
                    "display": "My Model (Fast)",  
                    "speed": "~5s",  
                    "strengths": "Быстрая итерация",  
                    "price": "$0.01/image",  
                },  
                {  
                    "id": "my-model-hq",  
                    "display": "My Model (HQ)",  
                    "speed": "~30s",  
                    "strengths": "Максимальное качество",  
                    "price": "$0.04/image",  
                },  
            ]  
      
        def default_model(self) -> Optional[str]:  
            return "my-model-fast"  
      
        def get_setup_schema(self) -> Dict[str, Any]:  
            # Метаданные для выбора в `hermes tools` — ключи для запроса при настройке.  
            return {  
                "name": "My Backend",  
                "badge": "paid",        # необязательно; отображается как короткий тег в списке выбора  
                "tag": "Однострочное описание под названием",  
                "env_vars": [  
                    {  
                        "key": "MY_BACKEND_API_KEY",  
                        "prompt": "API-ключ My Backend",  
                        "url": "https://my-backend.example.com/api-keys",  
                    },  
                ],  
            }  
      
        def generate(  
            self,  
            prompt: str,  
            aspect_ratio: str = DEFAULT_ASPECT_RATIO,  
            **kwargs: Any,  
        ) -> Dict[str, Any]:  
            prompt = (prompt or "").strip()  
            aspect_ratio = resolve_aspect_ratio(aspect_ratio)  
      
            if not prompt:  
                return error_response(  
                    error="Требуется указать prompt",  
                    error_type="invalid_input",  
                    provider=self.name,  
                    prompt="",  
                    aspect_ratio=aspect_ratio,  
                )  
      
            # Приоритет выбора модели: переменная окружения → конфиг → значение по умолчанию. Вспомогательный метод  
            # _resolve_model() во встроенном плагине openai — хороший пример для подражания.  
            model_id = kwargs.get("model") or self.default_model() or "my-model-fast"  
      
            try:  
                import my_backend_sdk  
                client = my_backend_sdk.Client(api_key=os.environ["MY_BACKEND_API_KEY"])  
                result = client.generate(  
                    prompt=prompt,  
                    model=model_id,  
                    aspect_ratio=aspect_ratio,  
                )  
      
                # Поддерживаются два формата:  
                #   - URL-строка: вернуть её как `image`  
                #   - данные base64: сохранить в $HERMES_HOME/cache/images/ через save_b64_image()  
                if result.get("image_b64"):  
                    path = save_b64_image(  
                        result["image_b64"],  
                        prefix=self.name,  
                        extension="png",  
                    )  
                    image = str(path)  
                else:  
                    image = result["image_url"]  
      
                return success_response(  
                    image=image,  
                    model=model_id,  
                    prompt=prompt,  
                    aspect_ratio=aspect_ratio,  
                    provider=self.name,  
                )  
            except Exception as exc:  
                return error_response(  
                    error=str(exc),  
                    error_type=type(exc).__name__,  
                    provider=self.name,  
                    model=model_id,  
                    prompt=prompt,  
                    aspect_ratio=aspect_ratio,  
                )  
      
      
    def register(ctx) -> None:  
        \"\"\"Точка входа плагина — вызывается один раз при загрузке.\"\"\"  
        ctx.register_image_gen_provider(MyBackendImageGenProvider())  
    
[/code]

## plugin.yaml[​](<#pluginyaml> "Прямая ссылка на plugin.yaml")

[code] 
    name: my-backend  
    version: 1.0.0  
    description: Мой бэкенд изображений — текст-в-изображение через My Backend SDK  
    author: Ваше Имя  
    kind: backend  
    requires_env:  
      - MY_BACKEND_API_KEY  
    
[/code]

`kind: backend` указывает, что плагин должен быть зарегистрирован через путь регистрации генерации изображений. `requires_env` запрашивается во время `hermes plugins install`.

## Справочник по ABC[​](<#abc-reference> "Прямая ссылка на Справочник по ABC")

Полный контракт в `agent/image_gen_provider.py`. Методы, которые вы обычно переопределяете:

Член | Обязательный | По умолчанию | Назначение  
---|---|---|---  
`name` | ✅ | — | Стабильный ID, используемый в конфиге `image_gen.provider`  
`display_name` | — | `name.title()` | Название, отображаемое в `hermes tools`  
`is_available()` | — | `True` | Шлюз для отсутствующих учётных данных/зависимостей  
`list_models()` | — | `[]` | Каталог для выбора модели в `hermes tools`  
`default_model()` | — | первая из `list_models()` | Запасной вариант, когда модель не настроена  
`get_setup_schema()` | — | минимальный | Метаданные выбора + запрос переменных окружения  
`generate(prompt, aspect_ratio, **kwargs)` | ✅ | — | Непосредственно вызов  

## Формат ответа[​](<#response-format> "Прямая ссылка на Формат ответа")

`generate()` должен возвращать словарь, построенный с помощью `success_response()` или `error_response()`. Обе находятся в `agent/image_gen_provider.py`.

**Успех:**

[code] 
    success_response(  
        image=<url-или-абсолютный-путь>,  
        model=<id-модели>,  
        prompt=<возвращённый-prompt>,  
        aspect_ratio="landscape" | "square" | "portrait",  
        provider=<имя-вашего-провайдера>,  
        extra={...},  # необязательные поля бэкенда  
    )  
    
[/code]

**Ошибка:**

[code] 
    error_response(  
        error="человекочитаемое сообщение",  
        error_type="provider_error" | "invalid_input" | "<имя класса исключения>",  
        provider=<имя-вашего-провайдера>,  
        model=<id-модели>,  
        prompt=<prompt>,  
        aspect_ratio=<разрешённое соотношение сторон>,  
    )  
    
[/code]

Обёртка инструмента JSON-сериализует словарь и передаёт его LLM. Ошибки отображаются как результат инструмента; LLM решает, как объяснить их пользователю.

## Обработка вывода base64 vs URL[​](<#handling-base64-vs-url-output> "Прямая ссылка на Обработка вывода base64 vs URL")

Некоторые бэкенды возвращают URL изображений (fal, Replicate); другие — полезную нагрузку base64 (OpenAI gpt-image-2). Для случая base64 используйте `save_b64_image()` — она записывает файл в `$HERMES_HOME/cache/images/<префикс>_<метка времени>_<uuid>.<расширение>` и возвращает абсолютный `Path`. Передайте этот путь (как `str`) в параметре `image=` в `success_response()`. Доставка через шлюзы (Telegram photo bubble, Discord attachment) распознаёт как URL, так и абсолютные пути.

## Переопределение пользователем[​](<#user-overrides> "Прямая ссылка на Переопределение пользователем")

Поместите пользовательский плагин в `~/.hermes/plugins/image_gen/<name>/` с тем же свойством `name`, что и у встроенного, и включите его через `hermes plugins enable <name>` — в реестре действует правило «последний записавший побеждает», поэтому ваша версия заменит встроенную. Это полезно для направления плагина `openai` на частный прокси или замены каталога моделей.

## Тестирование[​](<#testing> "Прямая ссылка на Тестирование")

[code] 
    export HERMES_HOME=/tmp/hermes-imggen-test  
    mkdir -p $HERMES_HOME/plugins/image_gen/my-backend  
    # …скопируйте __init__.py + plugin.yaml в эту директорию…  
      
    export MY_BACKEND_API_KEY=your-test-key  
    hermes plugins enable my-backend  
      
    # Выберите его как активного провайдера  
    echo "image_gen:" >> $HERMES_HOME/config.yaml  
    echo "  provider: my-backend" >> $HERMES_HOME/config.yaml  
      
    # Проверьте  
    hermes -z "Сгенерируй изображение корги в скафандре"  
    
[/code]

Или интерактивно: `hermes tools` → «Image Generation» → выберите `my-backend` → введите API-ключ, если будет предложено.

## Эталонные реализации[​](<#reference-implementations> "Прямая ссылка на Эталонные реализации")

  * **`plugins/image_gen/openai/__init__.py`** — gpt-image-2 на трёх уровнях (низкий/средний/высокий) в виде трёх виртуальных ID моделей, использующих одну модель API с разными параметрами `quality`. Хороший пример многоуровневых моделей в одном бэкенде с цепочкой приоритетов config.yaml.
  * **`plugins/image_gen/xai/__init__.py`** — Grok Imagine через xAI. Другая форма (URL-вывод, упрощённый каталог).
  * **`plugins/image_gen/openai-codex/__init__.py`** — Вариант Responses API в стиле Codex, переиспользующий OpenAI SDK с другим базовым URL маршрутизации.

## Распространение через pip[​](<#distribute-via-pip> "Прямая ссылка на Распространение через pip")

[code] 
    # pyproject.toml  
    [project.entry-points."hermes_agent.plugins"]  
    my-backend-imggen = "my_backend_imggen_package"  
    
[/code]

`my_backend_imggen_package` должен предоставлять функцию `register` верхнего уровня. См. [Distribute via pip](</docs/guides/build-a-hermes-plugin#distribute-via-pip>) в общем руководстве по плагинам для полной настройки.

## Связанные страницы[​](<#related-pages> "Прямая ссылка на Связанные страницы")

  * [Image Generation](</docs/user-guide/features/image-generation>) — пользовательская документация функции
  * [Plugins overview](</docs/user-guide/features/plugins>) — все типы плагинов одним взглядом
  * [Build a Hermes Plugin](</docs/guides/build-a-hermes-plugin>) — руководство по созданию инструментов, хуков и слэш-команд

  * [Как работает обнаружение](<#how-discovery-works>)
  * [Структура директории](<#directory-structure>)
  * [Абстрактный базовый класс ImageGenProvider](<#the-imagegenprovider-abc>)
  * [plugin.yaml](<#pluginyaml>)
  * [Справочник по ABC](<#abc-reference>)
  * [Формат ответа](<#response-format>)
  * [Обработка вывода base64 vs URL](<#handling-base64-vs-url-output>)
  * [Переопределение пользователем](<#user-overrides>)
  * [Тестирование](<#testing>)
  * [Эталонные реализации](<#reference-implementations>)
  * [Распространение через pip](<#distribute-via-pip>)
  * [Связанные страницы](<#related-pages>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/image-gen-provider-plugin -->
