На этой странице

**Скиллы** — это документы со знаниями, которые агент загружает по требованию. Они следуют принципу **прогрессивного раскрытия** для минимизации расхода токенов и совместимы с открытым стандартом [agentskills.io](<https://agentskills.io/specification>).

Все скиллы хранятся в **`~/.hermes/skills/`** — это основная директория и источник истины. При свежей установке встроенные скиллы копируются из репозитория. Скиллы, установленные из хаба или созданные агентом, также попадают сюда. Агент может изменять или удалять любой скилл.

Вы также можете указать Hermes **внешние директории скиллов** — дополнительные папки, которые сканируются наравне с локальной. См. [Внешние директории скиллов](#внешние-директории-скиллов) ниже.

См. также:
  * [Каталог встроенных скиллов](/docs/reference/skills-catalog)
  * [Каталог официальных опциональных скиллов](/docs/reference/optional-skills-catalog)


## Использование скиллов[​](#using-skills "Ссылка на раздел Использование скиллов")
Каждый установленный скилл автоматически доступен как слеш-команда:
[code] 
    # В CLI или любой платформе обмена сообщениями:  
    /gif-search funny cats  
    /axolotl help me fine-tune Llama 3 on my dataset  
    /github-pr-workflow create a PR for the auth refactor  
    /plan design a rollout for migrating our auth provider  
      
    # Просто имя скилла загружает его и позволяет агенту спросить, что вам нужно:  
    /excalidraw  
    
[/code]
Встроенный скилл `plan` — хороший пример. Запуск `/plan [запрос]` загружает инструкции скилла, сообщая Hermes изучить контекст (при необходимости), написать план реализации в формате markdown (вместо выполнения задачи) и сохранить результат в `.hermes/plans/` относительно активной рабочей области/рабочей директории бэкенда.

Вы также можете взаимодействовать со скиллами через обычный диалог:
[code] 
    hermes chat --toolsets skills -q "What skills do you have?"  
    hermes chat --toolsets skills -q "Show me the axolotl skill"  
    
[/code]

## Прогрессивное раскрытие[​](#progressive-disclosure "Ссылка на раздел Прогрессивное раскрытие")
Скиллы используют токен-эффективную схему загрузки:
[code] 
    Level 0: skills_list()           → [{name, description, category}, ...]   (~3k токенов)  
    Level 1: skill_view(name)        → Полное содержимое + метаданные       (различается)  
    Level 2: skill_view(name, path)  → Конкретный файл-справочник            (различается)  
    
[/code]
Агент загружает полное содержимое скилла только когда оно действительно нужно.

## Формат SKILL.md[​](#skillmd-format "Ссылка на раздел Формат SKILL.md")
[code] 
    ---  
    name: my-skill  
    description: Brief description of what this skill does  
    version: 1.0.0  
    platforms: [macos, linux]     # Опционально — ограничить конкретными ОС  
    metadata:  
      hermes:  
        tags: [python, automation]  
        category: devops  
        fallback_for_toolsets: [web]    # Опционально — условная активация (см. ниже)  
        requires_toolsets: [terminal]   # Опционально — условная активация (см. ниже)  
        config:                          # Опционально — настройки config.yaml  
          - key: my.setting  
            description: "Что это контролирует"  
            default: "значение"  
            prompt: "Подсказка для настройки"  
    ---  
      
    # Заголовок скилла  
      
    ## Когда использовать  
    Условия срабатывания для этого скилла.  
      
    ## Порядок действий  
    1. Шаг первый  
    2. Шаг второй  
      
    ## Возможные проблемы  
    - Известные режимы отказа и их исправления  
      
    ## Проверка  
    Как убедиться, что всё сработало.  
    
[/code]

### Платформозависимые скиллы[​](#platform-specific-skills "Ссылка на раздел Платформозависимые скиллы")
Скиллы могут ограничивать себя конкретными операционными системами с помощью поля `platforms`:

| Значение | Соответствие |
|---|---|
| `macos` | macOS (Darwin) |
| `linux` | Linux |
| `windows` | Windows |

[code] 
    platforms: [macos]            # Только macOS (например, iMessage, Apple Reminders, FindMy)  
    platforms: [macos, linux]     # macOS и Linux  
    
[/code]
Если поле задано, скилл автоматически скрывается из системного промпта, `skills_list()` и слеш-команд на несовместимых платформах. Если поле опущено, скилл загружается на всех платформах.

### Условная активация (запасные скиллы)[​](#conditional-activation-fallback-skills "Ссылка на раздел Условная активация (запасные скиллы)")
Скиллы могут автоматически показываться или скрываться в зависимости от того, какие инструменты доступны в текущей сессии. Это наиболее полезно для **запасных скиллов** — бесплатных или локальных альтернатив, которые должны появляться только когда премиум-инструмент недоступен.

[code] 
    metadata:  
      hermes:  
        fallback_for_toolsets: [web]      # Показывать ТОЛЬКО когда эти наборы инструментов недоступны  
        requires_toolsets: [terminal]     # Показывать ТОЛЬКО когда эти наборы инструментов доступны  
        fallback_for_tools: [web_search]  # Показывать ТОЛЬКО когда эти конкретные инструменты недоступны  
        requires_tools: [terminal]        # Показывать ТОЛЬКО когда эти конкретные инструменты доступны  
    
[/code]

| Поле | Поведение |
|---|---|
| `fallback_for_toolsets` | Скилл **скрыт**, когда указанные наборы инструментов доступны. Показывается, когда они отсутствуют. |
| `fallback_for_tools` | То же, но проверяет отдельные инструменты, а не наборы. |
| `requires_toolsets` | Скилл **скрыт**, когда указанные наборы инструментов недоступны. Показывается, когда они присутствуют. |
| `requires_tools` | То же, но проверяет отдельные инструменты. |

**Пример:** Встроенный скилл `duckduckgo-search` использует `fallback_for_toolsets: [web]`. Когда у вас установлен `FIRECRAWL_API_KEY`, набор инструментов web доступен и агент использует `web_search` — скилл DuckDuckGo остаётся скрытым. Если API-ключ отсутствует, набор инструментов web недоступен, и скилл DuckDuckGo автоматически появляется как запасной вариант.

Скиллы без каких-либо полей условной активации ведут себя как прежде — они всегда показываются.

## Безопасная настройка при загрузке[​](#secure-setup-on-load "Ссылка на раздел Безопасная настройка при загрузке")
Скиллы могут объявлять обязательные переменные окружения, не исчезая из списка обнаружения:

[code] 
    required_environment_variables:  
      - name: TENOR_API_KEY  
        prompt: Tenor API key  
        help: Get a key from https://developers.google.com/tenor  
        required_for: full functionality  
    
[/code]

Когда встречается отсутствующее значение, Hermes запрашивает его безопасно (только когда скилл реально загружается в локальном CLI). Вы можете пропустить настройку и продолжать использовать скилл. Поверхности обмена сообщениями никогда не запрашивают секреты в чате — вместо этого они предлагают использовать `hermes setup` или `~/.hermes/.env` локально.

После установки объявленные переменные окружения **автоматически пробрасываются** в песочницы `execute_code` и `terminal` — скрипты скилла могут напрямую использовать `$TENOR_API_KEY`. Для переменных окружения, не относящихся к скиллам, используйте опцию конфигурации `terminal.env_passthrough`. Подробности см. в разделе [Проброс переменных окружения](/docs/user-guide/security#environment-variable-passthrough).

### Настройки конфигурации скилла[​](#skill-config-settings "Ссылка на раздел Настройки конфигурации скилла")
Скиллы также могут объявлять несекретные настройки конфигурации (пути, предпочтения), хранящиеся в `config.yaml`:

[code] 
    metadata:  
      hermes:  
        config:  
          - key: myplugin.path  
            description: Path to the plugin data directory  
            default: "~/myplugin-data"  
            prompt: Plugin data directory path  
    
[/code]

Настройки хранятся в разделе `skills.config` вашего config.yaml. `hermes config migrate` запрашивает ненастроенные параметры, а `hermes config show` отображает их. Когда скилл загружается, его разрешённые значения конфигурации внедряются в контекст, так что агент автоматически знает настроенные значения.

Подробности см. в разделах [Настройки скиллов](/docs/user-guide/configuration#skill-settings) и [Создание скиллов — Настройки конфигурации](/docs/developer-guide/creating-skills#config-settings-configyaml).

## Структура директории скиллов[​](#skill-directory-structure "Ссылка на раздел Структура директории скиллов")
[code] 
    ~/.hermes/skills/                  # Единый источник истины  
    ├── mlops/                         # Директория категории  
    │   ├── axolotl/  
    │   │   ├── SKILL.md               # Основные инструкции (обязательно)  
    │   │   ├── references/            # Дополнительные документы  
    │   │   ├── templates/             # Форматы вывода  
    │   │   ├── scripts/               # Вспомогательные скрипты, вызываемые из скилла  
    │   │   └── assets/                # Дополнительные файлы  
    │   └── vllm/  
    │       └── SKILL.md  
    ├── devops/  
    │   └── deploy-k8s/                # Скилл, созданный агентом  
    │       ├── SKILL.md  
    │       └── references/  
    ├── .hub/                          # Состояние хаба скиллов  
    │   ├── lock.json  
    │   ├── quarantine/  
    │   └── audit.log  
    └── .bundled_manifest              # Отслеживает установленные встроенные скиллы  
    
[/code]

## Внешние директории скиллов[​](#external-skill-directories "Ссылка на раздел Внешние директории скиллов")
Если вы храните скиллы вне Hermes — например, общую директорию `~/.agents/skills/`, используемую несколькими AI-инструментами — вы можете указать Hermes также сканировать эти директории.

Добавьте `external_dirs` в раздел `skills` в `~/.hermes/config.yaml`:

[code] 
    skills:  
      external_dirs:  
        - ~/.agents/skills  
        - /home/shared/team-skills  
        - ${SKILLS_REPO}/skills  
    
[/code]

Пути поддерживают подстановку `~` и замену переменных окружения `${VAR}`.

### Как это работает[​](#how-it-works "Ссылка на раздел Как это работает")
  * **Только чтение**: Внешние директории сканируются только для обнаружения скиллов. Когда агент создаёт или редактирует скилл, он всегда записывает в `~/.hermes/skills/`.
  * **Приоритет локального**: Если одно и то же имя скилла существует и в локальной, и во внешней директории, локальная версия имеет приоритет.
  * **Полная интеграция**: Внешние скиллы отображаются в индексе системного промпта, `skills_list`, `skill_view` и как слеш-команды `/имя-скилла` — так же, как и локальные скиллы.
  * **Несуществующие пути молча пропускаются**: Если настроенная директория не существует, Hermes игнорирует её без ошибок. Полезно для опциональных общих директорий, которые могут отсутствовать на некоторых машинах.


### Пример[​](#example "Ссылка на раздел Пример")
[code] 
    ~/.hermes/skills/               # Локальная (основная, чтение-запись)  
    ├── devops/deploy-k8s/  
    │   └── SKILL.md  
    └── mlops/axolotl/  
        └── SKILL.md  
      
    ~/.agents/skills/               # Внешняя (только чтение, общая)  
    ├── my-custom-workflow/  
    │   └── SKILL.md  
    └── team-conventions/  
        └── SKILL.md  
    
[/code]

Все четыре скилла отображаются в вашем индексе скиллов. Если вы создадите новый скилл с именем `my-custom-workflow` локально, он перекроет внешнюю версию.

## Управляемые агентом скиллы (инструмент skill_manage)[​](#agent-managed-skills-skill_manage-tool "Ссылка на раздел Управляемые агентом скиллы (инструмент skill_manage)")
Агент может создавать, обновлять и удалять собственные скиллы через инструмент `skill_manage`. Это **процедурная память** агента — когда он разбирается в нетривиальном рабочем процессе, он сохраняет подход как скилл для будущего повторного использования.

### Когда агент создаёт скиллы[​](#when-the-agent-creates-skills "Ссылка на раздел Когда агент создаёт скиллы")
  * После успешного выполнения сложной задачи (5+ вызовов инструментов)
  * Когда он столкнулся с ошибками или тупиками и нашёл рабочий путь
  * Когда пользователь исправил его подход
  * Когда он обнаружил нетривиальный рабочий процесс


### Действия[​](#actions "Ссылка на раздел Действия")

| Действие | Для чего | Ключевые параметры |
|---|---|---|
| `create` | Новый скилл с нуля | `name`, `content` (полный SKILL.md), опционально `category` |
| `patch` | Точечные исправления (предпочтительно) | `name`, `old_string`, `new_string` |
| `edit` | Масштабные структурные переработки | `name`, `content` (замена полного SKILL.md) |
| `delete` | Полное удаление скилла | `name` |
| `write_file` | Добавление/обновление вспомогательных файлов | `name`, `file_path`, `file_content` |
| `remove_file` | Удаление вспомогательного файла | `name`, `file_path` |

tip
Действие `patch` предпочтительно для обновлений — оно более токен-эффективно, чем `edit`, потому что в вызове инструмента передаётся только изменённый текст.

## Хаб скиллов[​](#skills-hub "Ссылка на раздел Хаб скиллов")
Просматривайте, ищите, устанавливайте и управляйте скиллами из онлайн-реестров, `skills.sh`, прямых well-known эндпоинтов скиллов и официальных опциональных скиллов.

### Основные команды[​](#common-commands "Ссылка на раздел Основные команды")
[code] 
    hermes skills browse                              # Просмотр всех скиллов хаба (официальные первыми)  
    hermes skills browse --source official            # Просмотр только официальных опциональных скиллов  
    hermes skills search kubernetes                   # Поиск по всем источникам  
    hermes skills search react --source skills-sh     # Поиск в каталоге skills.sh  
    hermes skills search https://mintlify.com/docs --source well-known  
    hermes skills inspect openai/skills/k8s           # Предпросмотр перед установкой  
    hermes skills install openai/skills/k8s           # Установка со сканированием безопасности  
    hermes skills install official/security/1password  
    hermes skills install skills-sh/vercel-labs/json-render/json-render-react --force  
    hermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlify  
    hermes skills install https://sharethis.chat/SKILL.md              # Прямой URL (однофайловый SKILL.md)  
    hermes skills install https://example.com/SKILL.md --name my-skill # Переопределить имя, если во frontmatter его нет  
    hermes skills list --source hub                   # Список скиллов, установленных из хаба  
    hermes skills check                               # Проверка установленных скиллов хаба на наличие обновлений  
    hermes skills update                              # Переустановка скиллов хаба с изменениями от поставщика  
    hermes skills audit                               # Повторное сканирование всех скиллов хаба на безопасность  
    hermes skills uninstall k8s                       # Удаление скилла хаба  
    hermes skills reset google-workspace              # Отмена пометки "пользователь изменил" для встроенного скилла (см. ниже)  
    hermes skills reset google-workspace --restore    # Также восстановить встроенную версию, удалив ваши локальные правки  
    hermes skills publish skills/my-skill --to github --repo owner/repo  
    hermes skills snapshot export setup.json          # Экспорт конфигурации скиллов  
    hermes skills tap add myorg/skills-repo           # Добавление пользовательского GitHub-источника  
    
[/code]

### Поддерживаемые источники хаба[​](#supported-hub-sources "Ссылка на раздел Поддерживаемые источники хаба")

| Источник | Пример | Примечания |
|---|---|---|
| `official` | `official/security/1password` | Опциональные скиллы, поставляемые с Hermes. |
| `skills-sh` | `skills-sh/vercel-labs/agent-skills/vercel-react-best-practices` | Поиск через `hermes skills search <запрос> --source skills-sh`. Hermes разрешает скиллы с псевдонимами, когда slug на skills.sh отличается от папки в репозитории. |
| `well-known` | `well-known:https://mintlify.com/docs/.well-known/skills/mintlify` | Скиллы, предоставляемые напрямую через `/.well-known/skills/index.json` на веб-сайте. Поиск по URL сайта или документации. |
| `url` | `https://sharethis.chat/SKILL.md` | Прямой HTTP(S) URL к однофайловому `SKILL.md`. Разрешение имени: frontmatter → slug URL → интерактивный запрос → флаг `--name`. |
| `github` | `openai/skills/k8s` | Прямая установка из GitHub репозитория/пути и пользовательские taps. |
| `clawhub`, `lobehub`, `claude-marketplace` | Идентификаторы конкретных источников | Интеграции с сообществом или маркетплейсами. |

### Интегрированные хабы и реестры[​](#integrated-hubs-and-registries "Ссылка на раздел Интегрированные хабы и реестры")
Hermes в настоящее время интегрируется со следующими экосистемами скиллов и источниками обнаружения:

#### 1\\. Официальные опциональные скиллы (`official`)[​](#1-official-optional-skills-official "Ссылка на раздел 1-официальные-опциональные-скиллы-official")
Они поддерживаются в самом репозитории Hermes и устанавливаются со встроенным доверием.
  * Каталог: [Каталог официальных опциональных скиллов](/docs/reference/optional-skills-catalog)
  * Источник в репозитории: `optional-skills/`
  * Пример:


[code] 
    hermes skills browse --source official  
    hermes skills install official/security/1password  
    
[/code]

#### 2\\. skills.sh (`skills-sh`)[​](#2-skillssh-skills-sh "Ссылка на раздел 2-skillssh-skills-sh")
Это публичный каталог скиллов от Vercel. Hermes может напрямую искать в нём, просматривать страницы с деталями скиллов, разрешать псевдонимы и устанавливать из исходного репозитория.
  * Каталог: [skills.sh](<https://skills.sh/>)
  * Репозиторий CLI/инструментов: [vercel-labs/skills](<https://github.com/vercel-labs/skills>)
  * Официальный репозиторий скиллов Vercel: [vercel-labs/agent-skills](<https://github.com/vercel-labs/agent-skills>)
  * Пример:


[code] 
    hermes skills search react --source skills-sh  
    hermes skills inspect skills-sh/vercel-labs/json-render/json-render-react  
    hermes skills install skills-sh/vercel-labs/json-render/json-render-react --force  
    
[/code]

#### 3\\. Well-known эндпоинты скиллов (`well-known`)[​](#3-well-known-skill-endpoints-well-known "Ссылка на раздел 3-well-known-эндпоинты-скиллов-well-known")
Это обнаружение на основе URL с сайтов, публикующих `/.well-known/skills/index.json`. Это не единый централизованный хаб — это веб-конвенция для обнаружения.
  * Пример работающего эндпоинта: [Индекс скиллов Mintlify docs](<https://mintlify.com/docs/.well-known/skills/index.json>)
  * Эталонная реализация сервера: [vercel-labs/skills-handler](<https://github.com/vercel-labs/skills-handler>)
  * Пример:


[code] 
    hermes skills search https://mintlify.com/docs --source well-known  
    hermes skills inspect well-known:https://mintlify.com/docs/.well-known/skills/mintlify  
    hermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlify  
    
[/code]

#### 4\\. Прямые GitHub скиллы (`github`)[​](#4-direct-github-skills-github "Ссылка на раздел 4-прямые-github-скиллы-github")
Hermes может устанавливать скиллы напрямую из GitHub-репозиториев и GitHub-based taps. Это полезно, когда вы уже знаете репозиторий/путь или хотите добавить собственный репозиторий-источник.

Стандартные taps (доступны для просмотра без дополнительной настройки):
  * [openai/skills](<https://github.com/openai/skills>)
  * [anthropics/skills](<https://github.com/anthropics/skills>)
  * [VoltAgent/awesome-agent-skills](<https://github.com/VoltAgent/awesome-agent-skills>)
  * [garrytan/gstack](<https://github.com/garrytan/gstack>)
  * Пример:


[code] 
    hermes skills install openai/skills/k8s  
    hermes skills tap add myorg/skills-repo  
    
[/code]

#### 5\\. ClawHub (`clawhub`)[​](#5-clawhub-clawhub "Ссылка на раздел 5-clawhub-clawhub")
Сторонний маркетплейс скиллов, интегрированный как источник сообщества.
  * Сайт: [clawhub.ai](<https://clawhub.ai/>)
  * Идентификатор источника Hermes: `clawhub`


#### 6\\. Репозитории в стиле Claude marketplace (`claude-marketplace`)[​](#6-claude-marketplace-style-repos-claude-marketplace "Ссылка на раздел 6-репозитории-в-стиле-claude-marketplace-claude-marketplace")
Hermes поддерживает репозитории маркетплейсов, публикующие манифесты, совместимые с Claude.

Известные интегрированные источники включают:
  * [anthropics/skills](<https://github.com/anthropics/skills>)
  * [aiskillstore/marketplace](<https://github.com/aiskillstore/marketplace>)


Идентификатор источника Hermes: `claude-marketplace`

#### 7\\. LobeHub (`lobehub`)[​](#7-lobehub-lobehub "Ссылка на раздел 7-lobehub-lobehub")
Hermes может искать и конвертировать записи агентов из публичного каталога LobeHub в устанавливаемые скиллы Hermes.
  * Сайт: [LobeHub](<https://lobehub.com/>)
  * Публичный индекс агентов: [chat-agents.lobehub.com](<https://chat-agents.lobehub.com/>)
  * Исходный репозиторий: [lobehub/lobe-chat-agents](<https://github.com/lobehub/lobe-chat-agents>)
  * Идентификатор источника Hermes: `lobehub`


#### 8\\. Прямой URL (`url`)[​](#8-direct-url-url "Ссылка на раздел 8-прямой-url-url")
Установка однофайлового `SKILL.md` напрямую с любого HTTP(S) URL — полезно, когда автор размещает скилл на своём сайте (без листинга в хабе, без GitHub-пути). Hermes загружает URL, парсит YAML frontmatter, сканирует на безопасность и устанавливает.
  * Идентификатор источника Hermes: `url`
  * Идентификатор: сам URL (префикс не нужен)
  * Область применения: **только однофайловый `SKILL.md`**. Многофайловые скиллы с `references/` или `scripts/` требуют манифеста и должны публиковаться через один из других источников выше.


[code] 
    hermes skills install https://sharethis.chat/SKILL.md  
    hermes skills install https://example.com/my-skill/SKILL.md --category productivity  
    
[/code]

Разрешение имени, по порядку:
  1. Поле `name:` в YAML frontmatter SKILL.md (рекомендуется — каждый правильно оформленный скилл его содержит).
  2. Имя родительской директории из URL-пути (например, `.../my-skill/SKILL.md` → `my-skill`, или `.../my-skill.md` → `my-skill`), если это валидный идентификатор (`^[a-z][a-z0-9_-]*$`).
  3. Интерактивный запрос в терминале с TTY.
  4. На неинтерактивных поверхностях (слеш-команда `/skills install` в TUI, шлюзовые платформы, скрипты) — чёткая ошибка с указанием на флаг `--name`.


[code] 
    # Во frontmatter нет имени, и URL slug бесполезен — укажите имя:  
    hermes skills install https://example.com/SKILL.md --name sharethis-chat  
      
    # Или внутри чат-сессии:  
    /skills install https://example.com/SKILL.md --name sharethis-chat  
    
[/code]

Уровень доверия всегда `community` — выполняется то же сканирование безопасности, что и для любого другого источника. URL сохраняется как идентификатор установки, так что `hermes skills update` повторно загружает с того же URL при необходимости обновления.

### Сканирование безопасности и `--force`[​](#security-scanning-and---force "Ссылка на раздел Сканирование безопасности и --force")
Все скиллы, установленные из хаба, проходят через **сканер безопасности**, который проверяет на утечку данных, внедрение промптов, деструктивные команды, сигналы цепочки поставок и другие угрозы.

`hermes skills inspect ...` теперь также отображает метаданные от поставщика, когда они доступны:
  * URL репозитория
  * URL страницы с деталями на skills.sh
  * Команда установки
  * Еженедельные установки
  * Статусы аудита безопасности от поставщика
  * URL well-known индекса/эндпоинта


Используйте `--force`, когда вы проверили сторонний скилл и хотите переопределить неопасную блокировку политики:

[code] 
    hermes skills install skills-sh/anthropics/skills/pdf --force  
    
[/code]

Важное поведение:
  * `--force` может переопределять блокировки политики для предупреждений и находок типа "осторожно".
  * `--force` **не** переопределяет вердикт `dangerous` (опасно).
  * Официальные опциональные скиллы (`official/...`) считаются встроенным доверием и не показывают панель предупреждения о стороннем источнике.


### Уровни доверия[​](#trust-levels "Ссылка на раздел Уровни доверия")

| Уровень | Источник | Политика |
|---|---|---|
| `builtin` | Поставляется с Hermes | Всегда доверенный |
| `official` | `optional-skills/` в репозитории | Встроенное доверие, нет предупреждения о стороннем источнике |
| `trusted` | Доверенные реестры/репозитории, такие как `openai/skills`, `anthropics/skills` | Более разрешительная политика, чем у сообщественных источников |
| `community` | Всё остальное (`skills.sh`, well-known эндпоинты, пользовательские GitHub-репозитории, большинство маркетплейсов) | Неопасные находки могут быть переопределены с `--force`; вердикты `dangerous` остаются заблокированными |

### Жизненный цикл обновлений[​](#update-lifecycle "Ссылка на раздел Жизненный цикл обновлений")
Хаб теперь отслеживает достаточно метаданных происхождения, чтобы повторно проверять вышестоящие копии установленных скиллов:

[code] 
    hermes skills check          # Сообщить, какие установленные скиллы хаба изменились наверху  
    hermes skills update         # Переустановить только скиллы, для которых доступны обновления  
    hermes skills update react   # Обновить один конкретный установленный скилл хаба  
    
[/code]

Для обнаружения расхождений используется сохранённый идентификатор источника плюс текущий хеш содержимого вышестоящего пакета.

Лимиты GitHub API
Операции хаба скиллов используют GitHub API, который имеет лимит 60 запросов/час для неаутентифицированных пользователей. Если вы видите ошибки лимита запросов при установке или поиске, установите `GITHUB_TOKEN` в вашем `.env` файле, чтобы увеличить лимит до 5 000 запросов/час. Сообщение об ошибке содержит действенную подсказку, когда это происходит.

### Публикация пользовательского tap скиллов[​](#publishing-a-custom-skill-tap "Ссылка на раздел Публикация пользовательского tap скиллов")
Если вы хотите поделиться подобранным набором скиллов — для вашей команды, организации или публично — вы можете опубликовать их как **tap**: GitHub-репозиторий, который другие пользователи Hermes добавляют с помощью `hermes skills tap add <владелец/репозиторий>`. Никакого сервера, регистрации в реестре или пайплайна релизов. Просто директория с файлами `SKILL.md`.

#### Структура репозитория[​](#repo-layout "Ссылка на раздел Структура репозитория")
Tap — это любой GitHub-репозиторий (публичный или приватный — для приватного нужен `GITHUB_TOKEN`), организованный следующим образом:

[code] 
    owner/repo  
    ├── skills/                       # Путь по умолчанию; настраивается для каждого tap  
    │   ├── my-workflow/  
    │   │   ├── SKILL.md              # обязательно  
    │   │   ├── references/           # опциональные вспомогательные файлы  
    │   │   ├── templates/  
    │   │   └── scripts/  
    │   ├── another-skill/  
    │   │   └── SKILL.md  
    │   └── third-skill/  
    │       └── SKILL.md  
    └── README.md                     # опционально, но полезно  
    
[/code]

Правила:
  * Каждый скилл находится в своей собственной директории внутри корневого пути tap (по умолчанию `skills/`).
  * Имя директории становится установочным slug скилла.
  * Каждая директория скилла должна содержать `SKILL.md` со стандартным [frontmatter SKILL.md](#skillmd-format) (`name`, `description`, плюс опционально `metadata.hermes.tags`, `version`, `author`, `platforms`, `metadata.hermes.config`).
  * Поддиректории вроде `references/`, `templates/`, `scripts/`, `assets/` загружаются вместе с `SKILL.md` во время установки.
  * Скиллы, чьё имя директории начинается с `.` или `_`, игнорируются.


Hermes обнаруживает скиллы, перечисляя все поддиректории пути tap и проверяя каждую на наличие `SKILL.md`.

#### Минимальный пример tap[​](#minimal-tap-example "Ссылка на раздел Минимальный пример tap")
[code] 
    my-org/hermes-skills  
    └── skills/  
        └── deploy-runbook/  
            └── SKILL.md  
    
[/code]

`skills/deploy-runbook/SKILL.md`:
[code] 
    ---  
    name: deploy-runbook  
    description: Our deployment runbook — services, rollback, Slack channels  
    version: 1.0.0  
    author: My Org Platform Team  
    metadata:  
      hermes:  
        tags: [deployment, runbook, internal]  
    ---  
      
    # Deploy Runbook  
      
    Step 1: ...  
    
[/code]

После публикации на GitHub любой пользователь Hermes может подписаться и установить:
[code] 
    hermes skills tap add my-org/hermes-skills  
    hermes skills search deploy  
    hermes skills install my-org/hermes-skills/deploy-runbook  
    
[/code]

#### Нестандартные пути[​](#non-default-paths "Ссылка на раздел Нестандартные пути")
Если ваши скиллы не находятся в `skills/` (что часто бывает, когда вы добавляете поддерево `skills/` в существующий проект), отредактируйте запись tap в `~/.hermes/.hub/taps.json`:

[code] 
    {  
      "taps": [  
        {"repo": "my-org/platform-docs", "path": "internal/skills/"}  
      ]  
    }  
    
[/code]

CLI `hermes skills tap add` по умолчанию устанавливает для новых tap путь `path: "skills/"`; отредактируйте файл напрямую, если нужен другой путь. `hermes skills tap list` показывает действующий путь для каждого tap.

#### Установка отдельных скиллов напрямую (без добавления tap)[​](#installing-individual-skills-directly-without-adding-a-tap "Ссылка на раздел Установка отдельных скиллов напрямую (без добавления tap)")
Пользователи также могут установить один скилл из любого публичного GitHub-репозитория без добавления всего репозитория как tap:

[code] 
    hermes skills install owner/repo/skills/my-workflow  
    
[/code]

Полезно, когда вы хотите поделиться одним скиллом, не прося пользователя подписываться на весь ваш реестр.

#### Уровни доверия для taps[​](#trust-levels-for-taps "Ссылка на раздел Уровни доверия для taps")
Новым tap назначается уровень доверия `community` по умолчанию. Скиллы, установленные из них, проходят стандартное сканирование безопасности и показывают панель предупреждения о стороннем источнике при первой установке. Если ваша организация или широко доверенный источник должен получить более высокий уровень доверия, добавьте его репозиторий в `TRUSTED_REPOS` в `tools/skills_hub.py` (требуется PR в ядро Hermes).

#### Управление tap[​](#tap-management "Ссылка на раздел Управление tap")
[code] 
    hermes skills tap list                                # показать все настроенные tap  
    hermes skills tap add myorg/skills-repo               # добавить (путь по умолчанию: skills/)  
    hermes skills tap remove myorg/skills-repo            # удалить  
    
[/code]

Внутри запущенной сессии:
[code] 
    /skills tap list  
    /skills tap add myorg/skills-repo  
    /skills tap remove myorg/skills-repo  
    
[/code]

Tap хранятся в `~/.hermes/.hub/taps.json` (создаётся по требованию).

## Обновления встроенных скиллов (`hermes skills reset`)[​](#bundled-skill-updates-hermes-skills-reset "Ссылка на раздел Обновления встроенных скиллов (hermes skills reset)")
Hermes поставляется с набором встроенных скиллов в `skills/` внутри репозитория. При установке и при каждом `hermes update` синхронизация копирует их в `~/.hermes/skills/` и записывает манифест в `~/.hermes/skills/.bundled_manifest`, сопоставляя каждое имя скилла с хешем содержимого на момент синхронизации (**исходный хеш**).

При каждой синхронизации Hermes пересчитывает хеш вашей локальной копии и сравнивает его с исходным хешем:
  * **Не изменился** → можно безопасно применить изменения от поставщика, скопировать новую встроенную версию и записать новый исходный хеш.
  * **Изменился** → считается **пользовательским изменением** и навсегда пропускается, так что ваши правки никогда не будут перезаписаны.


Защита хорошая, но у неё есть один острый край. Если вы отредактировали встроенный скилл, а затем захотели отказаться от своих изменений и вернуться к встроенной версии, просто скопировав из `~/.hermes/hermes-agent/skills/`, манифест всё ещё содержит _старый_ исходный хеш с момента последней успешной синхронизации. Ваше свежее скопированное содержимое (текущий хеш встроенного скилла) не будет совпадать с этим устаревшим исходным хешем, поэтому синхронизация продолжит помечать его как пользовательское изменение.

`hermes skills reset` — это механизм выхода:
[code] 
    # Безопасно: очищает запись манифеста для этого скилла. Ваша текущая копия сохраняется,  
    # но следующая синхронизация перебазируется на неё, так что будущие обновления будут работать нормально.  
    hermes skills reset google-workspace  
      
    # Полное восстановление: также удаляет вашу локальную копию и повторно копирует текущую встроенную  
    # версию. Используйте это, когда хотите вернуть исходный скилл от поставщика.  
    hermes skills reset google-workspace --restore  
      
    # Неинтерактивно (например, в скриптах или TUI-режиме) — пропускает подтверждение --restore.  
    hermes skills reset google-workspace --restore --yes  
    
[/code]

Та же команда работает в чате как слеш-команда:
[code] 
    /skills reset google-workspace  
    /skills reset google-workspace --restore  
    
[/code]

Профили
У каждого профиля есть свой `.bundled_manifest` в собственном `HERMES_HOME`, так что `hermes -p coder skills reset <имя>` затрагивает только этот профиль.

### Слеш-команды (внутри чата)[​](#slash-commands-inside-chat "Ссылка на раздел Слеш-команды (внутри чата)")
Все те же команды работают с `/skills`:
[code] 
    /skills browse  
    /skills search react --source skills-sh  
    /skills search https://mintlify.com/docs --source well-known  
    /skills inspect skills-sh/vercel-labs/json-render/json-render-react  
    /skills install openai/skills/skill-creator --force  
    /skills check  
    /skills update  
    /skills reset google-workspace  
    /skills list  
    
[/code]

Официальные опциональные скиллы по-прежнему используют идентификаторы вида `official/security/1password` и `official/migration/openclaw-migration`.

  * [Использование скиллов](#using-skills)
  * [Прогрессивное раскрытие](#progressive-disclosure)
  * [Формат SKILL.md](#skillmd-format)
    * [Платформозависимые скиллы](#platform-specific-skills)
    * [Условная активация (запасные скиллы)](#conditional-activation-fallback-skills)
  * [Безопасная настройка при загрузке](#secure-setup-on-load)
    * [Настройки конфигурации скилла](#skill-config-settings)
  * [Структура директории скиллов](#skill-directory-structure)
  * [Внешние директории скиллов](#external-skill-directories)
    * [Как это работает](#how-it-works)
    * [Пример](#example)
  * [Управляемые агентом скиллы (инструмент skill_manage)](#agent-managed-skills-skill_manage-tool)
    * [Когда агент создаёт скиллы](#when-the-agent-creates-skills)
    * [Действия](#actions)
  * [Хаб скиллов](#skills-hub)
    * [Основные команды](#common-commands)
    * [Поддерживаемые источники хаба](#supported-hub-sources)
    * [Интегрированные хабы и реестры](#integrated-hubs-and-registries)
    * [Сканирование безопасности и `--force`](#security-scanning-and---force)
    * [Уровни доверия](#trust-levels)
    * [Жизненный цикл обновлений](#update-lifecycle)
    * [Публикация пользовательского tap скиллов](#publishing-a-custom-skill-tap)
  * [Обновления встроенных скиллов (`hermes skills reset`)](#bundled-skill-updates-hermes-skills-reset)
    * [Слеш-команды (внутри чата)](#slash-commands-inside-chat)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills -->
