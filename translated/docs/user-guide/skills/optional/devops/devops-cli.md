На этой странице
Запускайте 150+ AI-приложений через CLI inference.sh (infsh) — генерация изображений, создание видео, LLM, поиск, 3D, социальная автоматизация. Использует инструмент terminal. Триггеры: inference.sh, infsh, ai apps, flux, veo, image generation, video generation, seedream, seedance, tavily
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Опциональный — установите через `hermes skills install official/devops/cli`|
|Путь| `optional-skills/devops/cli`|
|Версия| `1.0.0`|
|Автор| okaris|
|Лицензия| MIT|
|Теги| `AI`, `image-generation`, `video`, `LLM`, `search`, `inference`, `FLUX`, `Veo`, `Claude`|
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Именно эти инструкции видит агент, когда навык активен.
# inference.sh CLI
Запускайте 150+ AI-приложений в облаке с помощью простого CLI. GPU не требуется.
Все команды используют **инструмент terminal** для выполнения команд `infsh`.
## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
* Пользователь просит сгенерировать изображения (FLUX, Reve, Seedream, Grok, Gemini image)
* Пользователь просит сгенерировать видео (Veo, Wan, Seedance, OmniHuman)
* Пользователь спрашивает про inference.sh или infsh
* Пользователь хочет запускать AI-приложения без управления отдельными API-провайдерами
* Пользователь просит AI-поиск (Tavily, Exa)
* Пользователю нужна генерация аватаров/липсинка

## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
CLI `infsh` должен быть установлен и аутентифицирован. Проверьте командой:
[code]
    infsh me
    
[/code]
Если не установлен:
[code]
    curl -fsSL https://cli.inference.sh | sh
    infsh login
    
[/code]
Полные инструкции по настройке см. в `references/authentication.md`.
## Рабочий процесс[​](<#workflow> "Прямая ссылка на Рабочий процесс")
### 1\. Всегда сначала ищите[​](<#1-always-search-first> "Прямая ссылка на 1. Всегда сначала ищите")
Никогда не угадывайте названия приложений — всегда ищите, чтобы найти правильный ID:
[code]
    infsh app list --search flux
    infsh app list --search video
    infsh app list --search image
    
[/code]
### 2\. Запустите приложение[​](<#2-run-an-app> "Прямая ссылка на 2. Запустите приложение")
Используйте точный ID приложения из результатов поиска. Всегда используйте `--json` для машиночитаемого вывода:
[code]
    infsh app run <app-id> --input '{"prompt": "your prompt here"}' --json
    
[/code]
### 3\. Разберите вывод[​](<#3-parse-the-output> "Прямая ссылка на 3. Разберите вывод")
JSON-вывод содержит URL-адреса сгенерированного медиа. Предоставьте их пользователю с помощью `MEDIA:<url>` для встроенного отображения.
## Часто используемые команды[​](<#common-commands> "Прямая ссылка на Часто используемые команды")
### Генерация изображений[​](<#image-generation> "Прямая ссылка на Генерация изображений")
[code]
    # Поиск приложений для изображений
    infsh app list --search image
      
    # FLUX Dev с LoRA
    infsh app run falai/flux-dev-lora --input '{"prompt": "sunset over mountains", "num_images": 1}' --json
      
    # Gemini image generation
    infsh app run google/gemini-2-5-flash-image --input '{"prompt": "futuristic city", "num_images": 1}' --json
      
    # Seedream (ByteDance)
    infsh app run bytedance/seedream-5-lite --input '{"prompt": "nature scene"}' --json
      
    # Grok Imagine (xAI)
    infsh app run xai/grok-imagine-image --input '{"prompt": "abstract art"}' --json
    
[/code]
### Генерация видео[​](<#video-generation> "Прямая ссылка на Генерация видео")
[code]
    # Поиск приложений для видео
    infsh app list --search video
      
    # Veo 3.1 (Google)
    infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot of coastline"}' --json
      
    # Seedance (ByteDance)
    infsh app run bytedance/seedance-1-5-pro --input '{"prompt": "dancing figure", "resolution": "1080p"}' --json
      
    # Wan 2.5
    infsh app run falai/wan-2-5 --input '{"prompt": "person walking through city"}' --json
    
[/code]
### Загрузка локальных файлов[​](<#local-file-uploads> "Прямая ссылка на Загрузка локальных файлов")
CLI автоматически загружает локальные файлы, когда вы указываете путь:
[code]
    # Апскейл локального изображения
    infsh app run falai/topaz-image-upscaler --input '{"image": "/path/to/photo.jpg", "upscale_factor": 2}' --json
      
    # Изображение-в-видео из локального файла
    infsh app run falai/wan-2-5-i2v --input '{"image": "/path/to/image.png", "prompt": "make it move"}' --json
      
    # Аватар с аудио
    infsh app run bytedance/omnihuman-1-5 --input '{"audio": "/path/to/audio.mp3", "image": "/path/to/face.jpg"}' --json
    
[/code]
### Поиск и исследования[​](<#search--research> "Прямая ссылка на Поиск и исследования")
[code]
    infsh app list --search search
    infsh app run tavily/tavily-search --input '{"query": "latest AI news"}' --json
    infsh app run exa/exa-search --input '{"query": "machine learning papers"}' --json
    
[/code]
### Другие категории[​](<#other-categories> "Прямая ссылка на Другие категории")
[code]
    # 3D генерация
    infsh app list --search 3d
      
    # Аудио / TTS
    infsh app list --search tts
      
    # Автоматизация Twitter/X
    infsh app list --search twitter
    
[/code]
## Типичные ошибки[​](<#pitfalls> "Прямая ссылка на Типичные ошибки")
  1. **Никогда не угадывайте ID приложений** — всегда сначала выполняйте `infsh app list --search <термин>`. ID приложений меняются, и новые приложения добавляются часто.
  2. **Всегда используйте `--json`** — сырой вывод сложно парсить. Флаг `--json` даёт структурированный вывод с URL-адресами.
  3. **Проверяйте аутентификацию** — если команды завершаются ошибками аутентификации, выполните `infsh login` или убедитесь, что `INFSH_API_KEY` установлен.
  4. **Долго выполняющиеся приложения** — генерация видео может занимать 30–120 секунд. Таймаута инструмента terminal должно быть достаточно, но предупредите пользователя, что это может занять некоторое время.
  5. **Формат ввода** — флаг `--input` принимает JSON-строку. Убедитесь, что кавычки правильно экранированы.

## Справочные документы[​](<#reference-docs> "Прямая ссылка на Справочные документы")
  * `references/authentication.md` — Настройка, вход, API-ключи
  * `references/app-discovery.md` — Поиск и просмотр каталога приложений
  * `references/running-apps.md` — Запуск приложений, форматы ввода, обработка вывода
  * `references/cli-reference.md` — Полная справочная информация по командам CLI

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Предварительные требования](<#prerequisites>)
  * [Рабочий процесс](<#workflow>)
    * [1\. Всегда сначала ищите](<#1-always-search-first>)
    * [2\. Запустите приложение](<#2-run-an-app>)
    * [3\. Разберите вывод](<#3-parse-the-output>)
  * [Часто используемые команды](<#common-commands>)
    * [Генерация изображений](<#image-generation>)
    * [Генерация видео](<#video-generation>)
    * [Загрузка локальных файлов](<#local-file-uploads>)
    * [Поиск и исследования](<#search--research>)
    * [Другие категории](<#other-categories>)
  * [Типичные ошибки](<#pitfalls>)
  * [Справочные документы](<#reference-docs>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/devops/devops-cli -->
