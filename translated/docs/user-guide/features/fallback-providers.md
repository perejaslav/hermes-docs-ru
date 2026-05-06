На этой странице
Hermes Agent имеет три уровня отказоустойчивости, которые поддерживают работу сессий при возникновении проблем у провайдеров:
  1. **[Пулы учётных данных](</docs/user-guide/features/credential-pools>)** — ротация нескольких API-ключей для _одного_ провайдера (проверяется в первую очередь)
  2. **Резервная модель основного провайдера** — автоматическое переключение на _другого_ провайдера:модель при сбое основной модели
  3. **Резервная модель вспомогательных задач** — независимое определение провайдера для побочных задач, таких как vision, сжатие и извлечение веб-страниц


Пулы учётных данных обрабатывают ротацию в рамках одного провайдера (например, несколько ключей OpenRouter). Эта страница описывает переключение между разными провайдерами. Оба механизма опциональны и работают независимо.
## Резервная модель основного провайдера[​](<#primary-model-fallback> "Прямая ссылка на Резервная модель основного провайдера")
Когда основной LLM-провайдер сталкивается с ошибками — превышение лимитов запросов, перегрузка сервера, сбои аутентификации, обрывы соединения — Hermes может автоматически переключиться на резервную пару провайдер:модель в середине сессии без потери истории разговора.
### Настройка[​](<#configuration> "Прямая ссылка на Настройка")
Самый простой путь — интерактивный менеджер:
[code] 
    hermes fallback  
    
[/code]
`hermes fallback` использует тот же выбор провайдера, что и `hermes model` — тот же список провайдеров, те же запросы учётных данных, та же валидация. Нажмите `a` для добавления резервного провайдера, `↑`/`↓` для изменения порядка, `d` для удаления, `q` для сохранения и выхода. Изменения сохраняются в `model.fallback_providers` в `config.yaml`.
Если вы предпочитаете редактировать YAML напрямую, добавьте секцию `fallback_model` в `~/.hermes/config.yaml`:
[code] 
    fallback_model:  
      provider: openrouter  
      model: anthropic/claude-sonnet-4  
    
[/code]
Оба поля — `provider` и `model` — **обязательны**. Если хотя бы одно отсутствует, резервный механизм отключается.
`fallback_model` vs `fallback_providers`
`fallback_model` (единственное число) — устаревший ключ с одним резервным провайдером — Hermes всё ещё поддерживает его для обратной совместимости. `fallback_providers` (множественное число, список) поддерживает несколько резервных провайдеров, перебираемых по порядку; `hermes fallback` записывает данные в этот ключ. Если заданы оба, Hermes объединяет их, при этом `fallback_providers` имеет приоритет.
### Поддерживаемые провайдеры[​](<#supported-providers> "Прямая ссылка на Поддерживаемые провайдеры")
Провайдер| Значение| Требования  
|---|---|---  
AI Gateway| `ai-gateway`| `AI_GATEWAY_API_KEY`  
OpenRouter| `openrouter`| `OPENROUTER_API_KEY`  
Nous Portal| `nous`| `hermes auth` (OAuth)  
OpenAI Codex| `openai-codex`| `hermes model` (ChatGPT OAuth)  
GitHub Copilot| `copilot`| `COPILOT_GITHUB_TOKEN`, `GH_TOKEN` или `GITHUB_TOKEN`  
GitHub Copilot ACP| `copilot-acp`| Внешний процесс (интеграция с редактором)  
Anthropic| `anthropic`| `ANTHROPIC_API_KEY` или учётные данные Claude Code  
z.ai / GLM| `zai`| `GLM_API_KEY`  
Kimi / Moonshot| `kimi-coding`| `KIMI_API_KEY`  
MiniMax| `minimax`| `MINIMAX_API_KEY`  
MiniMax (Китай)| `minimax-cn`| `MINIMAX_CN_API_KEY`  
DeepSeek| `deepseek`| `DEEPSEEK_API_KEY`  
NVIDIA NIM| `nvidia`| `NVIDIA_API_KEY` (опционально: `NVIDIA_BASE_URL`)  
GMI Cloud| `gmi`| `GMI_API_KEY` (опционально: `GMI_BASE_URL`)  
StepFun| `stepfun`| `STEPFUN_API_KEY` (опционально: `STEPFUN_BASE_URL`)  
Ollama Cloud| `ollama-cloud`| `OLLAMA_API_KEY`  
Google Gemini (OAuth)| `google-gemini-cli`| `hermes model` (Google OAuth; опционально: `HERMES_GEMINI_PROJECT_ID`)  
Google AI Studio| `gemini`| `GOOGLE_API_KEY` (псевдоним: `GEMINI_API_KEY`)  
xAI (Grok)| `xai` (псевдоним `grok`)| `XAI_API_KEY` (опционально: `XAI_BASE_URL`)  
AWS Bedrock| `bedrock`| Стандартная аутентификация boto3 (`AWS_REGION` + `AWS_PROFILE` или `AWS_ACCESS_KEY_ID`)  
Qwen Portal (OAuth)| `qwen-oauth`| `hermes model` (Qwen Portal OAuth; опционально: `HERMES_QWEN_BASE_URL`)  
MiniMax (OAuth)| `minimax-oauth`| `hermes model` (MiniMax portal OAuth)  
OpenCode Zen| `opencode-zen`| `OPENCODE_ZEN_API_KEY`  
OpenCode Go| `opencode-go`| `OPENCODE_GO_API_KEY`  
Kilo Code| `kilocode`| `KILOCODE_API_KEY`  
Xiaomi MiMo| `xiaomi`| `XIAOMI_API_KEY`  
Arcee AI| `arcee`| `ARCEEAI_API_KEY`  
GMI Cloud| `gmi`| `GMI_API_KEY`  
Alibaba / DashScope| `alibaba`| `DASHSCOPE_API_KEY`  
Alibaba Coding Plan| `alibaba-coding-plan`| `ALIBABA_CODING_PLAN_API_KEY` (запасной вариант: `DASHSCOPE_API_KEY`)  
Kimi / Moonshot (Китай)| `kimi-coding-cn`| `KIMI_CN_API_KEY`  
StepFun| `stepfun`| `STEPFUN_API_KEY`  
Tencent TokenHub| `tencent-tokenhub`| `TOKENHUB_API_KEY`  
Azure AI Foundry| `azure-foundry`| `AZURE_FOUNDRY_API_KEY` + `AZURE_FOUNDRY_BASE_URL`  
LM Studio (локально)| `lmstudio`| `LM_API_KEY` (или без ключа для локального) + `LM_BASE_URL`  
Hugging Face| `huggingface`| `HF_TOKEN`  
Пользовательский endpoint| `custom`| `base_url` + `key_env` (см. ниже)  
### Резервный пользовательский endpoint[​](<#custom-endpoint-fallback> "Прямая ссылка на Резервный пользовательский endpoint")
Для пользовательского endpoint, совместимого с OpenAI, добавьте `base_url` и опционально `key_env`:
[code] 
    fallback_model:  
      provider: custom  
      model: my-local-model  
      base_url: http://localhost:8000/v1  
      key_env: MY_LOCAL_KEY              # имя переменной окружения с API-ключом  
    
[/code]
### Когда срабатывает резервный механизм[​](<#when-fallback-triggers> "Прямая ссылка на Когда срабатывает резервный механизм")
Резервный механизм активируется автоматически, когда основная модель завершается с ошибкой:
  * **Превышение лимита запросов** (HTTP 429) — после исчерпания попыток повторного запроса
  * **Серверные ошибки** (HTTP 500, 502, 503) — после исчерпания попыток повторного запроса
  * **Ошибки аутентификации** (HTTP 401, 403) — немедленно (повторять бессмысленно)
  * **Не найдено** (HTTP 404) — немедленно
  * **Некорректные ответы** — когда API многократно возвращает повреждённые или пустые ответы


При срабатывании Hermes:
  1. Разрешает учётные данные для резервного провайдера
  2. Создаёт новый API-клиент
  3. Заменяет модель, провайдера и клиент на месте
  4. Сбрасывает счётчик повторов и продолжает разговор


Переключение происходит бесшовно — история разговора, вызовы инструментов и контекст сохраняются. Агент продолжает с того же места, просто используя другую модель.
Пошагово, а не по сессиям
Резервный механизм действует **в рамках одного шага (turn)**: каждое новое сообщение пользователя начинается с восстановления основной модели. Если основная модель сбоит в середине шага, резервная активируется только для этого шага. При следующем сообщении Hermes снова пробует основную модель. В рамках одного шага резервный механизм срабатывает не более одного раза — если резервная модель тоже сбоит, вступает в силу обычная обработка ошибок (повторы, затем сообщение об ошибке). Это предотвращает каскадные переключения в рамках одного шага, давая основной модели свежий шанс на каждом шаге.
### Примеры[​](<#examples> "Прямая ссылка на Примеры")
**OpenRouter как резервный для Anthropic native:**
[code] 
    model:  
      provider: anthropic  
      default: claude-sonnet-4-6  
      
    fallback_model:  
      provider: openrouter  
      model: anthropic/claude-sonnet-4  
    
[/code]
**Nous Portal как резервный для OpenRouter:**
[code] 
    model:  
      provider: openrouter  
      default: anthropic/claude-opus-4  
      
    fallback_model:  
      provider: nous  
      model: nous-hermes-3  
    
[/code]
**Локальная модель как резервная для облачной:**
[code] 
    fallback_model:  
      provider: custom  
      model: llama-3.1-70b  
      base_url: http://localhost:8000/v1  
      key_env: LOCAL_API_KEY  
    
[/code]
**Codex OAuth как резервный:**
[code] 
    fallback_model:  
      provider: openai-codex  
      model: gpt-5.3-codex  
    
[/code]
### Где работает резервный механизм[​](<#where-fallback-works> "Прямая ссылка на Где работает резервный механизм")
Контекст| Поддержка резервирования  
|---|---  
CLI-сессии| ✔  
Шлюз обмена сообщениями (Telegram, Discord и т.д.)| ✔  
Делегирование суб-агентам| ✘ (суб-агенты не наследуют конфигурацию резервирования)  
Cron-задачи| ✘ (выполняются с фиксированным провайдером)  
Вспомогательные задачи (vision, сжатие)| ✘ (используют собственную цепочку провайдеров — см. ниже)  
tip
Для `fallback_model` не существует переменных окружения — он настраивается исключительно через `config.yaml`. Это сделано намеренно: конфигурация резервирования — осознанный выбор, а не то, что должна переопределять устаревшая экспортная переменная оболочки.
* * *
## Резервная модель вспомогательных задач[​](<#auxiliary-task-fallback> "Прямая ссылка на Резервная модель вспомогательных задач")
Hermes использует отдельные лёгкие модели для побочных задач. Каждая задача имеет собственную цепочку определения провайдера, которая действует как встроенная система резервирования.
### Задачи с независимым определением провайдера[​](<#tasks-with-independent-provider-resolution> "Прямая ссылка на Задачи с независимым определением провайдера")
Задача| Что делает| Ключ конфигурации  
|---|---|---  
Vision| Анализ изображений, скриншоты браузера| `auxiliary.vision`  
Web Extract| Обобщение веб-страниц| `auxiliary.web_extract`  
Сжатие (Compression)| Сжатие контекста (саммари)| `auxiliary.compression`  
Поиск по сессиям (Session Search)| Обобщение прошлых сессий| `auxiliary.session_search`  
Skills Hub| Поиск навыков| `auxiliary.skills_hub`  
MCP| Вспомогательные операции MCP| `auxiliary.mcp`  
Подтверждение (Approval)| Классификация команд для подтверждения| `auxiliary.approval`  
Генерация заголовков (Title Generation)| Саммари заголовков сессий| `auxiliary.title_generation`  
### Цепочка автоопределения[​](<#auto-detection-chain> "Прямая ссылка на Цепочка автоопределения")
Когда провайдер задачи установлен в `"auto"` (по умолчанию), Hermes перебирает провайдеров по порядку, пока один не сработает:
**Для текстовых задач (сжатие, извлечение веб-страниц и т.д.):**
[code] 
    OpenRouter → Nous Portal → Пользовательский endpoint → Codex OAuth →  
    API-key провайдеры (z.ai, Kimi, MiniMax, Xiaomi MiMo, Hugging Face, Anthropic) → отказ  
    
[/code]
**Для задач vision:**
[code] 
    Основной провайдер (если поддерживает vision) → OpenRouter → Nous Portal →  
    Codex OAuth → Anthropic → Пользовательский endpoint → отказ  
    
[/code]
Если разрешённый провайдер сбоит при вызове, Hermes также имеет внутренний повтор: если провайдер не OpenRouter и не установлен явный `base_url`, он пробует OpenRouter как запасной вариант.
### Настройка вспомогательных провайдеров[​](<#configuring-auxiliary-providers> "Прямая ссылка на Настройка вспомогательных провайдеров")
Каждая задача может быть настроена независимо в `config.yaml`:
[code] 
    auxiliary:  
      vision:  
        provider: "auto"              # auto | openrouter | nous | codex | main | anthropic  
        model: ""                     # например "openai/gpt-4o"  
        base_url: ""                  # прямой endpoint (имеет приоритет над provider)  
        api_key: ""                   # API-ключ для base_url  
      
      web_extract:  
        provider: "auto"  
        model: ""  
      
      compression:  
        provider: "auto"  
        model: ""  
      
      session_search:  
        provider: "auto"  
        model: ""  
        timeout: 30  
        max_concurrency: 3  
        extra_body: {}  
      
      skills_hub:  
        provider: "auto"  
        model: ""  
      
      mcp:  
        provider: "auto"  
        model: ""  
    
[/code]
Каждая задача выше следует одному и тому же шаблону **provider / model / base_url**. Сжатие контекста настраивается в `auxiliary.compression`:
[code] 
    auxiliary:  
      compression:  
        provider: main                                    # Те же опции провайдеров, что и для других вспомогательных задач  
        model: google/gemini-3-flash-preview  
        base_url: null                                    # Пользовательский endpoint, совместимый с OpenAI  
    
[/code]
А резервная модель использует:
[code] 
    fallback_model:  
      provider: openrouter  
      model: anthropic/claude-sonnet-4  
      # base_url: http://localhost:8000/v1               # Опциональный пользовательский endpoint  
    
[/code]
Для `auxiliary.session_search` Hermes также поддерживает:
  * `max_concurrency` для ограничения количества одновременно выполняемых саммари сессий
  * `extra_body` для передачи специфичных для провайдера полей запроса, совместимых с OpenAI, при вызовах обобщения


Пример:
[code] 
    auxiliary:  
      session_search:  
        provider: main  
        model: glm-4.5-air  
        max_concurrency: 2  
        extra_body:  
          enable_thinking: false  
    
[/code]
Если ваш провайдер не поддерживает нативное поле управления рассуждениями, совместимое с OpenAI, `extra_body` в этом случае не поможет; однако `max_concurrency` всё ещё полезен для уменьшения количества всплесков ошибок 429.
Все три — auxiliary, compression, fallback — работают одинаково: установите `provider` для выбора обработчика запроса, `model` для выбора модели и `base_url` для указания пользовательского endpoint (переопределяет provider).
### Опции провайдеров для вспомогательных задач[​](<#provider-options-for-auxiliary-tasks> "Прямая ссылка на Опции провайдеров для вспомогательных задач")
Эти опции применяются только к конфигурациям `auxiliary:`, `compression:` и `fallback_model:` — `"main"` **не** является допустимым значением для вашего основного `model.provider`. Для пользовательских endpoint используйте `provider: custom` в секции `model:` (см. [Провайдеры AI](</docs/integrations/providers>)).
Провайдер| Описание| Требования  
|---|---|---  
`"auto"`| Перебирает провайдеров по порядку, пока один не сработает (по умолчанию)| Хотя бы один провайдер настроен  
`"openrouter"`| Принудительно OpenRouter| `OPENROUTER_API_KEY`  
`"nous"`| Принудительно Nous Portal| `hermes auth`  
`"codex"`| Принудительно Codex OAuth| `hermes model` → Codex  
`"main"`| Использовать провайдера основного агента (только для вспомогательных задач)| Активный основной провайдер настроен  
`"anthropic"`| Принудительно Anthropic native| `ANTHROPIC_API_KEY` или учётные данные Claude Code  
### Прямое переопределение endpoint[​](<#direct-endpoint-override> "Прямая ссылка на Прямое переопределение endpoint")
Для любой вспомогательной задачи установка `base_url` полностью обходит определение провайдера и отправляет запросы напрямую на указанный endpoint:
[code] 
    auxiliary:  
      vision:  
        base_url: "http://localhost:1234/v1"  
        api_key: "local-key"  
        model: "qwen2.5-vl"  
    
[/code]
`base_url` имеет приоритет над `provider`. Hermes использует настроенный `api_key` для аутентификации, а если он не задан — `OPENAI_API_KEY`. Он **не** использует повторно `OPENROUTER_API_KEY` для пользовательских endpoint.
* * *
## Резервное сжатие контекста[​](<#context-compression-fallback> "Прямая ссылка на Резервное сжатие контекста")
Сжатие контекста использует блок конфигурации `auxiliary.compression` для управления тем, какая модель и провайдер обрабатывают обобщение:
[code] 
    auxiliary:  
      compression:  
        provider: "auto"                              # auto | openrouter | nous | main  
        model: "google/gemini-3-flash-preview"  
    
[/code]
Миграция со старых версий
Старые конфиги с `compression.summary_model` / `compression.summary_provider` / `compression.summary_base_url` автоматически мигрируются в `auxiliary.compression.*` при первой загрузке (версия конфига 17).
Если для сжатия недоступен ни один провайдер, Hermes пропускает промежуточные шаги разговора без генерации саммари, а не завершает сессию ошибкой.
* * *
## Переопределение провайдера для делегирования[​](<#delegation-provider-override> "Прямая ссылка на Переопределение провайдера для делегирования")
Суб-агенты, порождённые через `delegate_task`, **не** используют основную резервную модель. Однако их можно направить на другую пару провайдер:модель для оптимизации затрат:
[code] 
    delegation:  
      provider: "openrouter"                      # переопределение провайдера для всех суб-агентов  
      model: "google/gemini-3-flash-preview"      # переопределение модели  
      # base_url: "http://localhost:1234/v1"      # или использование прямого endpoint  
      # api_key: "local-key"  
    
[/code]
См. [Делегирование суб-агентам](</docs/user-guide/features/delegation>) для полной информации по настройке.
* * *
## Провайдеры cron-задач[​](<#cron-job-providers> "Прямая ссылка на Провайдеры cron-задач")
Cron-задачи выполняются с тем провайдером, который настроен на момент выполнения. Они не поддерживают резервную модель. Чтобы использовать другого провайдера для cron-задач, настройте переопределения `provider` и `model` в самой задаче:
[code] 
    cronjob(  
        action="create",  
        schedule="every 2h",  
        prompt="Check server status",  
        provider="openrouter",  
        model="google/gemini-3-flash-preview"  
    )  
    
[/code]
См. [Плановые задачи (Cron)](</docs/user-guide/features/cron>) для полной информации по настройке.
* * *
## Сводка[​](<#summary> "Прямая ссылка на Сводка")
Функция| Механизм резервирования| Расположение в конфиге  
|---|---|---  
Модель основного агента| `fallback_model` в config.yaml — пошаговое переключение при ошибках (основная модель восстанавливается на каждом шаге)| `fallback_model:` (верхний уровень)  
Vision| Цепочка автоопределения + внутренний повтор через OpenRouter| `auxiliary.vision`  
Извлечение веб-страниц (Web extraction)| Цепочка автоопределения + внутренний повтор через OpenRouter| `auxiliary.web_extract`  
Сжатие контекста (Compression)| Цепочка автоопределения, откат до отсутствия саммари, если недоступно| `auxiliary.compression`  
Поиск по сессиям (Session search)| Цепочка автоопределения| `auxiliary.session_search`  
Skills Hub| Цепочка автоопределения| `auxiliary.skills_hub`  
MCP-помощники| Цепочка автоопределения| `auxiliary.mcp`  
Классификация подтверждений (Approval)| Цепочка автоопределения| `auxiliary.approval`  
Генерация заголовков (Title generation)| Цепочка автоопределения| `auxiliary.title_generation`  
Делегирование (Delegation)| Только переопределение провайдера (нет автоматического резервирования)| `delegation.provider` / `delegation.model`  
Cron-задачи| Переопределение провайдера на задачу (нет автоматического резервирования)| `provider` / `model` в задаче  
  * [Резервная модель основного провайдера](<#primary-model-fallback>)
    * [Настройка](<#configuration>)
    * [Поддерживаемые провайдеры](<#supported-providers>)
    * [Резервный пользовательский endpoint](<#custom-endpoint-fallback>)
    * [Когда срабатывает резервный механизм](<#when-fallback-triggers>)
    * [Примеры](<#examples>)
    * [Где работает резервный механизм](<#where-fallback-works>)
  * [Резервная модель вспомогательных задач](<#auxiliary-task-fallback>)
    * [Задачи с независимым определением провайдера](<#tasks-with-independent-provider-resolution>)
    * [Цепочка автоопределения](<#auto-detection-chain>)
    * [Настройка вспомогательных провайдеров](<#configuring-auxiliary-providers>)
    * [Опции провайдеров для вспомогательных задач](<#provider-options-for-auxiliary-tasks>)
    * [Прямое переопределение endpoint](<#direct-endpoint-override>)
  * [Резервное сжатие контекста](<#context-compression-fallback>)
  * [Переопределение провайдера для делегирования](<#delegation-provider-override>)
  * [Провайдеры cron-задач](<#cron-job-providers>)
  * [Сводка](<#summary>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers -->
