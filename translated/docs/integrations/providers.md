На этой странице

Эта страница описывает настройку провайдеров инференса для Hermes Agent — от облачных API, таких как OpenRouter и Anthropic, до самостоятельно размещённых эндпоинтов, таких как Ollama и vLLM, а также продвинутую маршрутизацию и конфигурации с резервными провайдерами. Вам нужен хотя бы один настроенный провайдер для использования Hermes.

## Провайдеры инференса[​](<#inference-providers> "Прямая ссылка на Провайдеры инференса")

Вам нужен как минимум один способ подключения к LLM. Используйте `hermes model` для интерактивного переключения провайдеров и моделей, или настройте напрямую:

| Провайдер | Настройка |
|---|---|
| **Nous Portal** | `hermes model` (OAuth, по подписке) |
| **OpenAI Codex** | `hermes model` (OAuth ChatGPT, использует модели Codex) |
| **GitHub Copilot** | `hermes model` (OAuth с потоком кода устройства, `COPILOT_GITHUB_TOKEN`, `GH_TOKEN` или `gh auth token`) |
| **GitHub Copilot ACP** | `hermes model` (запускает локальный `copilot --acp --stdio`) |
| **Anthropic** | `hermes model` (Claude Max + дополнительный кредит использования через OAuth; также поддерживает API-ключ Anthropic или ручной setup-token — см. примечание ниже) |
| **OpenRouter** | `OPENROUTER_API_KEY` в `~/.hermes/.env` |
| **AI Gateway** | `AI_GATEWAY_API_KEY` в `~/.hermes/.env` (провайдер: `ai-gateway`) |
| **z.ai / GLM** | `GLM_API_KEY` в `~/.hermes/.env` (провайдер: `zai`) |
| **Kimi / Moonshot** | `KIMI_API_KEY` в `~/.hermes/.env` (провайдер: `kimi-coding`) |
| **Kimi / Moonshot (Китай)** | `KIMI_CN_API_KEY` в `~/.hermes/.env` (провайдер: `kimi-coding-cn`; алиасы: `kimi-cn`, `moonshot-cn`) |
| **Arcee AI** | `ARCEEAI_API_KEY` в `~/.hermes/.env` (провайдер: `arcee`; алиасы: `arcee-ai`, `arceeai`) |
| **GMI Cloud** | `GMI_API_KEY` в `~/.hermes/.env` (провайдер: `gmi`; алиасы: `gmi-cloud`, `gmicloud`) |
| **MiniMax** | `MINIMAX_API_KEY` в `~/.hermes/.env` (провайдер: `minimax`) |
| **MiniMax (Китай)** | `MINIMAX_CN_API_KEY` в `~/.hermes/.env` (провайдер: `minimax-cn`) |
| **Alibaba Cloud** | `DASHSCOPE_API_KEY` в `~/.hermes/.env` (провайдер: `alibaba`) |
| **Alibaba Coding Plan** | `DASHSCOPE_API_KEY` (провайдер: `alibaba-coding-plan`, алиас: `alibaba_coding`) — отдельный биллинговый SKU, другой эндпоинт |
| **Kilo Code** | `KILOCODE_API_KEY` в `~/.hermes/.env` (провайдер: `kilocode`) |
| **Xiaomi MiMo** | `XIAOMI_API_KEY` в `~/.hermes/.env` (провайдер: `xiaomi`, алиасы: `mimo`, `xiaomi-mimo`) |
| **Tencent TokenHub** | `TOKENHUB_API_KEY` в `~/.hermes/.env` (провайдер: `tencent-tokenhub`, алиасы: `tencent`, `tokenhub`, `tencentmaas`) |
| **OpenCode Zen** | `OPENCODE_ZEN_API_KEY` в `~/.hermes/.env` (провайдер: `opencode-zen`) |
| **OpenCode Go** | `OPENCODE_GO_API_KEY` в `~/.hermes/.env` (провайдер: `opencode-go`) |
| **DeepSeek** | `DEEPSEEK_API_KEY` в `~/.hermes/.env` (провайдер: `deepseek`) |
| **Hugging Face** | `HF_TOKEN` в `~/.hermes/.env` (провайдер: `huggingface`, алиасы: `hf`) |
| **Google / Gemini** | `GOOGLE_API_KEY` (или `GEMINI_API_KEY`) в `~/.hermes/.env` (провайдер: `gemini`) |
| **Google Gemini (OAuth)** | `hermes model` → «Google Gemini (OAuth)» (провайдер: `google-gemini-cli`, поддерживается бесплатный тариф, браузерный PKCE-логин) |
| **LM Studio** | `hermes model` → «LM Studio» (провайдер: `lmstudio`, опционально `LM_API_KEY`) |
| **Пользовательский эндпоинт** | `hermes model` → выберите «Custom endpoint» (сохраняется в `config.yaml`) |

Официальный путь с API-ключом описан в специальном [руководстве по Google Gemini](</docs/guides/google-gemini>).

Алиас ключа модели
В секции конфигурации `model:` вы можете использовать `default:` или `model:` в качестве имени ключа для ID вашей модели. Оба варианта — `model: { default: my-model }` и `model: { model: my-model }` — работают одинаково.

### Google Gemini через OAuth (`google-gemini-cli`)[​](<#google-gemini-via-oauth-google-gemini-cli> "Прямая ссылка на google-gemini-via-oauth-google-gemini-cli")

Провайдер `google-gemini-cli` использует бэкенд Google Cloud Code Assist — тот же API, который использует собственный инструмент Google `gemini-cli`. Он поддерживает как **бесплатный тариф** (щедрый дневной лимит для личных аккаунтов), так и **платные тарифы** (Standard/Enterprise с проектом GCP).

**Быстрый старт:**

[code] 
    hermes model  
    # → выберите «Google Gemini (OAuth)»
    # → прочитайте предупреждение о политике, подтвердите
    # → откроется браузер с accounts.google.com, войдите
    # → готово — Hermes автоматически подготовит ваш бесплатный тариф при первом запросе
    
[/code]

Hermes поставляется с **публичным** OAuth-клиентом `gemini-cli` от Google — те же учётные данные, которые Google включает в свой открытый `gemini-cli`. Десктопные OAuth-клиенты не являются конфиденциальными (безопасность обеспечивает PKCE). Вам не нужно устанавливать `gemini-cli` или регистрировать собственный OAuth-клиент GCP.

**Как работает аутентификация:**

  * Поток PKCE Authorization Code через `accounts.google.com`
  * Обратный вызов браузера на `http://127.0.0.1:8085/oauth2callback` (с запасным эфемерным портом, если занят)
  * Токены сохраняются в `~/.hermes/auth/google_oauth.json` (chmod 0600, атомарная запись, межпроцессная блокировка `fcntl`)
  * Автоматическое обновление за 60 с до истечения срока
  * Окружения без браузера (SSH, `HERMES_HEADLESS=1`) → запасной режим с копированием ссылки
  * Дедупликация одновременных обновлений — два параллельных запроса не вызовут двойное обновление
  * `invalid_grant` (отозванный refresh-токен) → файл учётных данных удаляется, пользователь получает запрос на повторный вход

**Как работает инференс:**

  * Трафик идёт на `https://cloudcode-pa.googleapis.com/v1internal:generateContent` (или `:streamGenerateContent?alt=sse` для стриминга), а НЕ на платный эндпоинт `v1beta/openai`
  * Тело запроса обёрнуто в `{project, model, user_prompt_id, request}`
  * OpenAI-образные `messages[]`, `tools[]`, `tool_choice` преобразуются в нативные форматы Gemini: `contents[]`, `tools[].functionDeclarations`, `toolConfig`
  * Ответы преобразуются обратно в OpenAI-формат, чтобы остальная часть Hermes работала без изменений

**Тарифы и ID проектов:**

| Ваша ситуация | Что делать |
|---|---|
| Личный аккаунт Google, нужен бесплатный тариф | Ничего — войдите и начинайте общение |
| Аккаунт Workspace / Standard / Enterprise | Установите `HERMES_GEMINI_PROJECT_ID` или `GOOGLE_CLOUD_PROJECT` в ID вашего GCP-проекта |
| Организация с VPC-SC | Hermes обнаруживает `SECURITY_POLICY_VIOLATED` и автоматически переключает на `standard-tier` |

Бесплатный тариф автоматически подготавливает управляемый Google проект при первом использовании. Настройка GCP не требуется.

**Мониторинг квоты:**

[code] 
    /gquota
    
[/code]

Показывает оставшуюся квоту Code Assist по моделям с прогресс-барами:

[code] 
    Gemini Code Assist quota  (project: 123-abc)
      
      gemini-2.5-pro                      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░   85%
      gemini-2.5-flash [input]            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░   92%
    
[/code]

Риск, связанный с политикой
Google считает использование OAuth-клиента Gemini CLI со сторонним программным обеспечением нарушением политики. Некоторые пользователи сообщали об ограничениях аккаунта. Для минимизации риска используйте собственный API-ключ через провайдер `gemini`. Hermes показывает предупреждение и требует явного подтверждения перед началом OAuth.

**Пользовательский OAuth-клиент (опционально):**

Если вы хотите зарегистрировать собственный OAuth-клиент Google — например, чтобы квота и согласие были привязаны к вашему проекту GCP — установите:

[code] 
    HERMES_GEMINI_CLIENT_ID=your-client.apps.googleusercontent.com
    HERMES_GEMINI_CLIENT_SECRET=...   # опционально для Desktop-клиентов
    
[/code]

Зарегистрируйте OAuth-клиент типа **Desktop app** в [console.cloud.google.com/apis/credentials](<https://console.cloud.google.com/apis/credentials>) с включённым Generative Language API.

Примечание о Codex
Провайдер OpenAI Codex аутентифицируется через код устройства (откройте URL, введите код). Hermes сохраняет полученные учётные данные в своём хранилище (`~/.hermes/auth.json`) и может импортировать существующие учётные данные Codex CLI из `~/.codex/auth.json`, если они есть. Установка Codex CLI не требуется.

Предупреждение
Даже при использовании Nous Portal, Codex или пользовательского эндпоинта некоторые инструменты (зрение, суммаризация веба, MoA) используют отдельную «вспомогательную» модель. По умолчанию (`auxiliary.*.provider: "auto"`) Hermes направляет эти задачи на **вашу основную модель чата** — ту же, что вы выбрали в `hermes model`. Вы можете переопределить каждую задачу индивидуально, чтобы направлять её на более дешёвую/быструю модель (например, Gemini Flash через OpenRouter) — см. [Вспомогательные модели](</docs/user-guide/configuration#auxiliary-models>).

Nous Tool Gateway
Платные подписчики Nous Portal также получают доступ к **[Tool Gateway](</docs/user-guide/features/tool-gateway>)** — поиск в вебе, генерация изображений, TTS и автоматизация браузера через вашу подписку. Никаких дополнительных API-ключей не требуется. Он предлагается автоматически во время настройки `hermes model`, или вы можете включить его позже с помощью `hermes tools`.

### Две команды для управления моделями[​](<#two-commands-for-model-management> "Прямая ссылка на Две команды для управления моделями")

Hermes имеет **две** команды для работы с моделями, которые служат разным целям:

| Команда | Где запускать | Что делает |
|---|---|---|
| **`hermes model`** | В вашем терминале (вне сессии чата) | Полный мастер настройки — добавление провайдеров, запуск OAuth, ввод API-ключей, настройка эндпоинтов |
| **`/model`** | Внутри сессии чата Hermes | Быстрое переключение между **уже настроенными** провайдерами и моделями |

Если вы пытаетесь переключиться на провайдера, которого ещё не настроили (например, у вас настроен только OpenRouter, а вы хотите использовать Anthropic), вам нужна команда `hermes model`, а не `/model`. Выйдите из сессии (`Ctrl+C` или `/quit`), выполните `hermes model`, завершите настройку провайдера, затем начните новую сессию.

### Anthropic (нативный)[​](<#anthropic-native> "Прямая ссылка на Anthropic (нативный)")

Используйте модели Claude напрямую через API Anthropic — без прокси OpenRouter. Поддерживает три метода аутентификации:

Требуются кредиты «extra usage» Claude Max
Когда вы аутентифицируетесь через `hermes model` → Anthropic OAuth (или через `hermes auth add anthropic --type oauth`), Hermes подключается как Claude Code к вашему аккаунту Anthropic. **Это работает, только если у вас есть план Claude Max и вы приобрели дополнительные кредиты использования.** Базовая квота плана Max (использование, включённое в Claude Code по умолчанию) не расходуется Hermes — используются только дополнительные кредиты, которые вы добавили сверху. Подписчики Claude Pro не могут использовать этот путь.

Если у вас нет Max + дополнительных кредитов, используйте `ANTHROPIC_API_KEY` — запросы тарифицируются по принципу «плати за токен» для организации этого ключа (стандартные цены API, независимо от подписки Claude).

[code] 
    # С API-ключом (плата за токен)
    export ANTHROPIC_API_KEY=***
    hermes chat --provider anthropic --model claude-sonnet-4-6
      
    # Предпочтительно: аутентификация через `hermes model`
    # Hermes будет использовать хранилище учётных данных Claude Code напрямую, когда оно доступно
    hermes model
      
    # Ручное переопределение с setup-токеном (запасной / устаревший)
    export ANTHROPIC_TOKEN=***  # setup-token или ручной OAuth-токен
    hermes chat --provider anthropic
      
    # Автоопределение учётных данных Claude Code (если вы уже используете Claude Code)
    hermes chat --provider anthropic  # читает файлы учётных данных Claude Code автоматически
    
[/code]

Когда вы выбираете Anthropic OAuth через `hermes model`, Hermes предпочитает использовать собственное хранилище учётных данных Claude Code, а не копировать токен в `~/.hermes/.env`. Это позволяет сохранять возможность обновления refreshable-учётных данных Claude.

Или установите постоянно:

[code] 
    model:
      provider: "anthropic"
      default: "claude-sonnet-4-6"
    
[/code]

Алиасы
`--provider claude` и `--provider claude-code` также работают как сокращение для `--provider anthropic`.

### GitHub Copilot[​](<#github-copilot> "Прямая ссылка на GitHub Copilot")

Hermes поддерживает GitHub Copilot как полноценного провайдера с двумя режимами:

**`copilot` — прямой API Copilot** (рекомендуется). Использует вашу подписку GitHub Copilot для доступа к GPT-5.x, Claude, Gemini и другим моделям через API Copilot.

[code] 
    hermes chat --provider copilot --model gpt-5.4
    
[/code]

**Варианты аутентификации** (проверяются в следующем порядке):

  1. Переменная окружения `COPILOT_GITHUB_TOKEN`
  2. Переменная окружения `GH_TOKEN`
  3. Переменная окружения `GITHUB_TOKEN`
  4. Запасной вариант через `gh auth token`

Если токен не найден, `hermes model` предлагает **OAuth-логин через код устройства** — тот же поток, который используется в Copilot CLI и opencode.

Типы токенов
API Copilot **не** поддерживает классические Personal Access Tokens (`ghp_*`). Поддерживаемые типы токенов:

| Тип | Префикс | Как получить |
|---|---|---|
| OAuth-токен | `gho_` | `hermes model` → GitHub Copilot → Login with GitHub |
| Fine-grained PAT | `github_pat_` | GitHub Settings → Developer settings → Fine-grained tokens (требуется разрешение **Copilot Requests**) |
| GitHub App-токен | `ghu_` | Через установку GitHub App |

Если ваш `gh auth token` возвращает токен `ghp_*`, используйте `hermes model` для аутентификации через OAuth.

Поведение аутентификации Copilot в Hermes
Hermes отправляет поддерживаемый GitHub-токен (`gho_*`, `github_pat_*` или `ghu_*`) напрямую на `api.githubcopilot.com` и включает Copilot-специфичные заголовки (`Editor-Version`, `Copilot-Integration-Id`, `Openai-Intent`, `x-initiator`).

При HTTP 401 Hermes выполняет одноразовое восстановление учётных данных перед переходом к запасному варианту:

  1. Повторное получение токена через стандартную цепочку приоритетов (`COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN` → `gh auth token`)
  2. Пересборка общего OpenAI-клиента с обновлёнными заголовками
  3. Однократная повторная попытка запроса

Некоторые старые прокси сообщества используют поток обмена `api.github.com/copilot_internal/v2/token`. Этот эндпоинт может быть недоступен для некоторых типов аккаунтов (возвращает 404). Поэтому Hermes использует прямую аутентификацию по токену как основной путь и полагается на восстановление учётных данных во время выполнения с повторной попыткой для надёжности.

**Маршрутизация API:** Модели GPT-5+ (кроме `gpt-5-mini`) автоматически используют Responses API. Все остальные модели (GPT-4o, Claude, Gemini и т.д.) используют Chat Completions. Модели автоматически определяются из живого каталога Copilot.

**`copilot-acp` — бэкенд агента Copilot ACP.** Запускает локальный Copilot CLI как подпроцесс:

[code] 
    hermes chat --provider copilot-acp --model copilot-acp
    # Требуется GitHub Copilot CLI в PATH и существующая сессия `copilot login`
    
[/code]

**Постоянная конфигурация:**

[code] 
    model:
      provider: "copilot"
      default: "gpt-5.4"
    
[/code]

| Переменная окружения | Описание |
|---|---|
| `COPILOT_GITHUB_TOKEN` | GitHub-токен для API Copilot (наивысший приоритет) |
| `HERMES_COPILOT_ACP_COMMAND` | Переопределить путь к бинарнику Copilot CLI (по умолчанию: `copilot`) |
| `HERMES_COPILOT_ACP_ARGS` | Переопределить аргументы ACP (по умолчанию: `--acp --stdio`) |

### Полноценные провайдеры с API-ключом[​](<#first-class-api-key-providers> "Прямая ссылка на Полноценные провайдеры с API-ключом")

Эти провайдеры имеют встроенную поддержку с выделенными ID провайдеров. Установите API-ключ и используйте `--provider` для выбора:

[code] 
    # z.ai / ZhipuAI GLM
    hermes chat --provider zai --model glm-5
    # Требуется: GLM_API_KEY в ~/.hermes/.env
      
    # Kimi / Moonshot AI (международный: api.moonshot.ai)
    hermes chat --provider kimi-coding --model kimi-for-coding
    # Требуется: KIMI_API_KEY в ~/.hermes/.env
      
    # Kimi / Moonshot AI (Китай: api.moonshot.cn)
    hermes chat --provider kimi-coding-cn --model kimi-k2.5
    # Требуется: KIMI_CN_API_KEY в ~/.hermes/.env
      
    # MiniMax (глобальный эндпоинт)
    hermes chat --provider minimax --model MiniMax-M2.7
    # Требуется: MINIMAX_API_KEY в ~/.hermes/.env
      
    # MiniMax (эндпоинт в Китае)
    hermes chat --provider minimax-cn --model MiniMax-M2.7
    # Требуется: MINIMAX_CN_API_KEY в ~/.hermes/.env
      
    # Alibaba Cloud / DashScope (модели Qwen)
    hermes chat --provider alibaba --model qwen3.5-plus
    # Требуется: DASHSCOPE_API_KEY в ~/.hermes/.env
      
    # Xiaomi MiMo
    hermes chat --provider xiaomi --model mimo-v2-pro
    # Требуется: XIAOMI_API_KEY в ~/.hermes/.env
      
    # Tencent TokenHub (Hy3 Preview)
    hermes chat --provider tencent-tokenhub --model hy3-preview
    # Требуется: TOKENHUB_API_KEY в ~/.hermes/.env
      
    # Arcee AI (модели Trinity)
    hermes chat --provider arcee --model trinity-large-thinking
    # Требуется: ARCEEAI_API_KEY в ~/.hermes/.env
      
    # GMI Cloud
    # Используйте точный ID модели, возвращаемый эндпоинтом GMI /v1/models.
    hermes chat --provider gmi --model zai-org/GLM-5.1-FP8
    # Требуется: GMI_API_KEY в ~/.hermes/.env
    
[/code]

Или установите провайдера постоянно в `config.yaml`:

[code] 
    model:
      provider: "gmi"
      default: "zai-org/GLM-5.1-FP8"
    
[/code]

Базовые URL можно переопределить с помощью переменных окружения `GLM_BASE_URL`, `KIMI_BASE_URL`, `MINIMAX_BASE_URL`, `MINIMAX_CN_BASE_URL`, `DASHSCOPE_BASE_URL`, `XIAOMI_BASE_URL`, `GMI_BASE_URL` или `TOKENHUB_BASE_URL`.

Автоопределение эндпоинта Z.AI
При использовании провайдера Z.AI / GLM Hermes автоматически проверяет несколько эндпоинтов (глобальный, китайский, варианты для кодинга), чтобы найти тот, который принимает ваш API-ключ. Вам не нужно устанавливать `GLM_BASE_URL` вручную — рабочий эндпоинт определяется и кэшируется автоматически.

### xAI (Grok) — Responses API + Кэширование промптов[​](<#xai-grok--responses-api--prompt-caching> "Прямая ссылка на xAI (Grok) — Responses API + Кэширование промптов")

xAI подключён через Responses API (транспорт `codex_responses`) для автоматической поддержки рассуждений на моделях Grok 4 — параметр `reasoning_effort` не нужен, сервер рассуждает по умолчанию. Установите `XAI_API_KEY` в `~/.hermes/.env` и выберите xAI в `hermes model`, или используйте сокращение `grok` как `/model grok-4-1-fast-reasoning`.

При использовании xAI в качестве провайдера (любой базовый URL, содержащий `x.ai`), Hermes автоматически включает кэширование промптов, отправляя заголовок `x-grok-conv-id` с каждым API-запросом. Это направляет запросы на один и тот же сервер в рамках сессии разговора, позволяя инфраструктуре xAI повторно использовать кэшированные системные промпты и историю беседы.

Никакой настройки не требуется — кэширование активируется автоматически, когда обнаружен эндпоинт xAI и доступен ID сессии. Это снижает задержку и стоимость для многошаговых разговоров.

xAI также предоставляет выделенный TTS-эндпоинт (`/v1/tts`). Выберите **xAI TTS** в `hermes tools` → Voice & TTS, или см. страницу [Voice & TTS](</docs/user-guide/features/tts#text-to-speech>).

### Ollama Cloud — Управляемые модели Ollama, OAuth + API-ключ[​](<#ollama-cloud--managed-ollama-models-oauth--api-key> "Прямая ссылка на Ollama Cloud — Управляемые модели Ollama, OAuth + API-ключ")

[Ollama Cloud](<https://ollama.com/cloud>) размещает тот же каталог открытых моделей, что и локальный Ollama, но без необходимости в GPU. Выберите **Ollama Cloud** в `hermes model`, вставьте ваш API-ключ с [ollama.com/settings/keys](<https://ollama.com/settings/keys>), и Hermes автоматически обнаружит доступные модели.

[code] 
    hermes model
    # → выберите «Ollama Cloud»
    # → вставьте ваш OLLAMA_API_KEY
    # → выберите из обнаруженных моделей (gpt-oss:120b, glm-4.6:cloud, qwen3-coder:480b-cloud и т.д.)
    
[/code]

Или напрямую в `config.yaml`:

[code] 
    model:
      provider: "ollama-cloud"
      default: "gpt-oss:120b"
    
[/code]

Каталог моделей загружается динамически с `ollama.com/v1/models` и кэшируется на один час. Обозначение `model:tag` (например, `qwen3-coder:480b-cloud`) сохраняется при нормализации — не используйте дефисы.

Ollama Cloud vs локальный Ollama
Оба используют одинаковый OpenAI-совместимый API. Cloud — полноценный провайдер (`--provider ollama-cloud`, `OLLAMA_API_KEY`); локальный Ollama доступен через поток настройки пользовательского эндпоинта (базовый URL `http://localhost:11434/v1`, без ключа). Используйте Cloud для больших моделей, которые нельзя запустить локально; используйте локальный вариант для приватности или офлайн-работы.

### AWS Bedrock[​](<#aws-bedrock> "Прямая ссылка на AWS Bedrock")

Anthropic Claude, Amazon Nova, DeepSeek v3.2, Meta Llama 4 и другие модели через AWS Bedrock. Использует цепочку учётных данных AWS SDK (`boto3`) — без API-ключа, только стандартная аутентификация AWS.

[code] 
    # Простейший способ — именованный профиль в ~/.aws/credentials
    hermes chat --provider bedrock --model us.anthropic.claude-sonnet-4-6
      
    # Или с явными переменными окружения
    AWS_PROFILE=myprofile AWS_REGION=us-east-1 hermes chat --provider bedrock --model us.anthropic.claude-sonnet-4-6
    
[/code]

Или постоянно в `config.yaml`:

[code] 
    model:
      provider: "bedrock"
      default: "us.anthropic.claude-sonnet-4-6"
    bedrock:
      region: "us-east-1"          # или установите AWS_REGION
      # profile: "myprofile"       # или установите AWS_PROFILE
      # discovery: true            # автоопределение региона из IAM
      # guardrail:                 # опционально: Bedrock Guardrails
      #   id: "your-guardrail-id"
      #   version: "DRAFT"
    
[/code]

Аутентификация использует стандартную цепочку boto3: явные `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, `AWS_PROFILE` из `~/.aws/credentials`, роль IAM на EC2/ECS/Lambda, IMDS или SSO. Никакие переменные окружения не требуются, если вы уже аутентифицированы через AWS CLI.

Bedrock использует **Converse API** под капотом — запросы преобразуются в агностический формат Bedrock, поэтому одна и та же конфигурация работает для моделей Claude, Nova, DeepSeek и Llama. Устанавливайте `BEDROCK_BASE_URL` только если вы обращаетесь к нестандартному региональному эндпоинту.

См. [руководство по AWS Bedrock](</docs/guides/aws-bedrock>) для пошаговой настройки IAM, выбора региона и кросс-регионального инференса.

### Qwen Portal (OAuth)[​](<#qwen-portal-oauth> "Прямая ссылка на Qwen Portal (OAuth)")

Портал Qwen от Alibaba с браузерным OAuth-логином. Выберите **Qwen OAuth (Portal)** в `hermes model`, войдите через браузер, и Hermes сохранит refresh-токен.

[code] 
    hermes model
    # → выберите «Qwen OAuth (Portal)»
    # → откроется браузер; войдите с аккаунтом Alibaba
    # → подтвердите — учётные данные сохраняются в ~/.hermes/auth.json
      
    hermes chat   # использует эндпоинт portal.qwen.ai/v1
    
[/code]

Или настройте `config.yaml`:

[code] 
    model:
      provider: "qwen-oauth"
      default: "qwen3-coder-plus"
    
[/code]

Устанавливайте `HERMES_QWEN_BASE_URL` только если эндпоинт портала изменится (по умолчанию: `https://portal.qwen.ai/v1`).

Qwen OAuth vs DashScope (Alibaba)
`qwen-oauth` использует пользовательский портал Qwen с OAuth-логином — идеально для индивидуальных пользователей. Провайдер `alibaba` использует корпоративный API DashScope с `DASHSCOPE_API_KEY` — идеально для программных/производственных нагрузок. Оба направляют к моделям семейства Qwen, но находятся на разных эндпоинтах.

### Alibaba Coding Plan[​](<#alibaba-coding-plan> "Прямая ссылка на Alibaba Coding Plan")

Если вы подписаны на **Coding Plan** от Alibaba (отдельный биллинговый SKU, отличный от стандартного доступа к API DashScope), Hermes предоставляет его как отдельного полноценного провайдера: `alibaba-coding-plan`. Эндпоинт: `https://coding-intl.dashscope.aliyuncs.com/v1`. Он совместим с OpenAI, как и обычный провайдер `alibaba`, но с другим базовым URL и системой тарификации.

[code] 
    model:
      provider: alibaba_coding     # алиас для alibaba-coding-plan
      model: qwen3-coder-plus
    
[/code]

Или из CLI:

[code] 
    hermes chat --provider alibaba_coding --model qwen3-coder-plus
    
[/code]

`alibaba_coding` использует тот же `DASHSCOPE_API_KEY`, который уже используется вашим провайдером `alibaba` — отдельный ключ не нужен, только другой целевой маршрут. До регистрации этого провайдера пользователи, установившие `provider: alibaba_coding` в `config.yaml`, незаметно перенаправлялись на маршрутизацию OpenRouter.

### MiniMax (OAuth)[​](<#minimax-oauth> "Прямая ссылка на MiniMax (OAuth)")

MiniMax-M2.7 через браузерный OAuth-логин — никакого API-ключа не нужно. Выберите **MiniMax (OAuth)** в `hermes model`, войдите через браузер, и Hermes сохранит access + refresh токены. Использует эндпоинт, совместимый с Anthropic Messages (`/anthropic`), под капотом.

[code] 
    hermes model
    # → выберите «MiniMax (OAuth)»
    # → откроется браузер; войдите с аккаунтом MiniMax (глобальный или китайский регион)
    # → подтвердите — учётные данные сохраняются в ~/.hermes/auth.json
      
    hermes chat   # использует эндпоинт api.minimax.io/anthropic
    
[/code]

Или настройте `config.yaml`:

[code] 
    model:
      provider: "minimax-oauth"
      default: "MiniMax-M2.7"
    
[/code]

Поддерживаемые модели: `MiniMax-M2.7` (основная) и `MiniMax-M2.7-highspeed` (используется как вспомогательная модель по умолчанию). Путь OAuth игнорирует `MINIMAX_API_KEY` / `MINIMAX_BASE_URL`.

MiniMax OAuth vs API-ключ
`minimax-oauth` использует пользовательский портал MiniMax с OAuth-логином — настройка биллинга не требуется. Провайдеры `minimax` и `minimax-cn` используют `MINIMAX_API_KEY` / `MINIMAX_CN_API_KEY` — для программного доступа. См. [руководство по MiniMax OAuth](</docs/guides/minimax-oauth>) для полного пошагового описания.

### NVIDIA NIM[​](<#nvidia-nim> "Прямая ссылка на NVIDIA NIM")

Nemotron и другие модели с открытым исходным кодом через [build.nvidia.com](<https://build.nvidia.com>) (бесплатный API-ключ) или локальный эндпоинт NIM.

[code] 
    # Облако (build.nvidia.com)
    hermes chat --provider nvidia --model nvidia/nemotron-3-super-120b-a12b
    # Требуется: NVIDIA_API_KEY в ~/.hermes/.env
      
    # Локальный эндпоинт NIM — переопределите базовый URL
    NVIDIA_BASE_URL=http://localhost:8000/v1 hermes chat --provider nvidia --model nvidia/nemotron-3-super-120b-a12b
    
[/code]

Или установите постоянно в `config.yaml`:

[code] 
    model:
      provider: "nvidia"
      default: "nvidia/nemotron-3-super-120b-a12b"
    
[/code]

Локальный NIM
Для локальных развёртываний (DGX Spark, локальный GPU) установите `NVIDIA_BASE_URL=http://localhost:8000/v1`. NIM предоставляет тот же OpenAI-совместимый API чат-дополнений, что и build.nvidia.com, поэтому переключение между облаком и локальным сервером — это изменение одной строки переменной окружения.

### GMI Cloud[​](<#gmi-cloud> "Прямая ссылка на GMI Cloud")

Открытые модели и модели рассуждений через [GMI Cloud](<https://inference.gmi.ai>) — OpenAI-совместимый API, аутентификация по API-ключу.

[code] 
    # GMI Cloud
    hermes chat --provider gmi --model deepseek-ai/DeepSeek-R1
    # Требуется: GMI_API_KEY в ~/.hermes/.env
    
[/code]

Или установите постоянно в `config.yaml`:

[code] 
    model:
      provider: "gmi"
      default: "deepseek-ai/DeepSeek-R1"
    
[/code]

Базовый URL можно переопределить с помощью `GMI_BASE_URL` (по умолчанию: `https://api.gmi.ai/v1`).

### StepFun[​](<#stepfun> "Прямая ссылка на StepFun")

Модели серии Step через [StepFun](<https://platform.stepfun.com>) — OpenAI-совместимый API, аутентификация по API-ключу.

[code] 
    # StepFun
    hermes chat --provider stepfun --model step-3-mini
    # Требуется: STEPFUN_API_KEY в ~/.hermes/.env
    
[/code]

Или установите постоянно в `config.yaml`:

[code] 
    model:
      provider: "stepfun"
      default: "step-3-mini"
    
[/code]

Базовый URL можно переопределить с помощью `STEPFUN_BASE_URL` (по умолчанию: `https://api.stepfun.com/v1`).

### Hugging Face Inference Providers[​](<#hugging-face-inference-providers> "Прямая ссылка на Hugging Face Inference Providers")

[Hugging Face Inference Providers](<https://huggingface.co/docs/inference-providers>) направляет к 20+ открытым моделям через единый OpenAI-совместимый эндпоинт (`router.huggingface.co/v1`). Запросы автоматически направляются на самый быстрый доступный бэкенд (Groq, Together, SambaNova и т.д.) с автоматическим восстановлением при сбоях.

[code] 
    # Используйте любую доступную модель
    hermes chat --provider huggingface --model Qwen/Qwen3-235B-A22B-Thinking-2507
    # Требуется: HF_TOKEN в ~/.hermes/.env
      
    # Короткий алиас
    hermes chat --provider hf --model deepseek-ai/DeepSeek-V3.2
    
[/code]

Или установите постоянно в `config.yaml`:

[code] 
    model:
      provider: "huggingface"
      default: "Qwen/Qwen3-235B-A22B-Thinking-2507"
    
[/code]

Получите токен на [huggingface.co/settings/tokens](<https://huggingface.co/settings/tokens>) — не забудьте включить разрешение «Make calls to Inference Providers». Включён бесплатный тариф (кредит $0.10/месяц, без наценки на тарифы провайдеров).

Вы можете добавлять суффиксы маршрутизации к именам моделей: `:fastest` (по умолчанию), `:cheapest` или `:provider_name` для принудительного использования конкретного бэкенда.

Базовый URL можно переопределить с помощью `HF_BASE_URL`.

## Пользовательские и самостоятельно размещённые LLM-провайдеры[​](<#custom--self-hosted-llm-providers> "Прямая ссылка на Пользовательские и самостоятельно размещённые LLM-провайдеры")

Hermes Agent работает с **любым OpenAI-совместимым API-эндпоинтом**. Если сервер реализует `/v1/chat/completions`, вы можете указать Hermes на него. Это означает, что вы можете использовать локальные модели, GPU-серверы инференса, многопровайдерные маршрутизаторы или любые сторонние API.

### Общая настройка[​](<#general-setup> "Прямая ссылка на Общая настройка")

Три способа настроить пользовательский эндпоинт:

**Интерактивная настройка (рекомендуется):**

[code] 
    hermes model
    # Выберите «Custom endpoint (self-hosted / VLLM / etc.)»
    # Введите: API base URL, API key, Model name
    
[/code]

**Ручная конфигурация (`config.yaml`):**

[code] 
    # В ~/.hermes/config.yaml
    model:
      default: your-model-name
      provider: custom
      base_url: http://localhost:8000/v1
      api_key: your-key-or-leave-empty-for-local
    
[/code]

Устаревшие переменные окружения
`OPENAI_BASE_URL` и `LLM_MODEL` в `.env` **удалены**. Ни одна часть Hermes их не читает — `config.yaml` является единственным источником истины для конфигурации модели и эндпоинта. Если у вас есть устаревшие записи в `.env`, они будут автоматически очищены при следующем `hermes setup` или миграции конфигурации. Используйте `hermes model` или редактируйте `config.yaml` напрямую.

Оба подхода сохраняют настройки в `config.yaml`, который является источником истины для модели, провайдера и базового URL.

### Переключение моделей с помощью `/model`[​](<#switching-models-with-model> "Прямая ссылка на переключение моделей с помощью /model")

hermes model vs /model
**`hermes model`** (запускается из терминала, вне сессии чата) — это **полный мастер настройки провайдеров**. Используйте его для добавления новых провайдеров, запуска OAuth-потоков, ввода API-ключей и настройки пользовательских эндпоинтов.
**`/model`** (вводится внутри активной сессии чата Hermes) может только **переключаться между уже настроенными провайдерами и моделями**. Он не может добавлять новых провайдеров, запускать OAuth или запрашивать API-ключи. Если вы настроили только одного провайдера (например, OpenRouter), `/model` покажет только модели этого провайдера.
**Чтобы добавить нового провайдера:** Выйдите из сессии (`Ctrl+C` или `/quit`), выполните `hermes model`, настройте нового провайдера, затем начните новую сессию.

После того как у вас настроен хотя бы один пользовательский эндпоинт, вы можете переключать модели в середине сессии:

[code] 
    /model custom:qwen-2.5          # Переключиться на модель на вашем пользовательском эндпоинте
    /model custom                    # Автоопределить модель из эндпоинта
    /model openrouter:claude-sonnet-4 # Переключиться обратно на облачного провайдера
    
[/code]

Если у вас настроены **именованные пользовательские провайдеры** (см. ниже), используйте тройной синтаксис:

[code] 
    /model custom:local:qwen-2.5    # Использовать пользовательского провайдера «local» с моделью qwen-2.5
    /model custom:work:llama3       # Использовать пользовательского провайдера «work» с llama3
    
[/code]

При переключении провайдеров Hermes сохраняет базовый URL и провайдера в конфиг, чтобы изменения сохранялись после перезапуска. При переключении с пользовательского эндпоинта на встроенного провайдера устаревший базовый URL автоматически очищается.

Совет
`/model custom` (без имени модели) запрашивает `/models` API вашего эндпоинта и автоматически выбирает модель, если загружена ровно одна. Полезно для локальных серверов, работающих с одной моделью.

Всё ниже следует этому же шаблону — просто измените URL, ключ и имя модели.

* * *

### Ollama — Локальные модели, без настройки[​](<#ollama--local-models-zero-config> "Прямая ссылка на Ollama — Локальные модели, без настройки")

[Ollama](<https://ollama.com/>) запускает модели с открытым весом локально одной командой. Лучше всего подходит для: быстрых локальных экспериментов, работы с конфиденциальными данными, офлайн-использования. Поддерживает вызов инструментов через OpenAI-совместимый API.

[code] 
    # Установите и запустите модель
    ollama pull qwen2.5-coder:32b
    ollama serve   # Запускается на порту 11434
    
[/code]

Затем настройте Hermes:

[code] 
    hermes model
    # Выберите «Custom endpoint (self-hosted / VLLM / etc.)»
    # Введите URL: http://localhost:11434/v1
    # Пропустите API-ключ (Ollama не требует ключа)
    # Введите имя модели (например, qwen2.5-coder:32b)
    
[/code]

Или настройте `config.yaml` напрямую:

[code] 
    model:
      default: qwen2.5-coder:32b
      provider: custom
      base_url: http://localhost:11434/v1
      context_length: 32768   # См. предупреждение ниже
    
[/code]

Ollama по умолчанию использует очень малую длину контекста
Ollama **не** использует полное окно контекста вашей модели по умолчанию. В зависимости от вашей VRAM, значение по умолчанию:

| Доступная VRAM | Контекст по умолчанию |
|---|---|
| Менее 24 ГБ | **4 096 токенов** |
| 24–48 ГБ | 32 768 токенов |
| 48+ ГБ | 256 000 токенов |

Для использования агента с инструментами **вам нужно как минимум 16k–32k контекста**. При 4k системный промпт + схемы инструментов могут заполнить окно, не оставив места для разговора.

**Как увеличить** (выберите один вариант):

[code]
    # Вариант 1: Установить общесерверно через переменную окружения (рекомендуется)
    OLLAMA_CONTEXT_LENGTH=32768 ollama serve
      
    # Вариант 2: Для Ollama под управлением systemd
    sudo systemctl edit ollama.service
    # Добавьте: Environment="OLLAMA_CONTEXT_LENGTH=32768"
    # Затем: sudo systemctl daemon-reload && sudo systemctl restart ollama
      
    # Вариант 3: Встроить в пользовательскую модель (постоянно для конкретной модели)
    echo -e "FROM qwen2.5-coder:32b\nPARAMETER num_ctx 32768" > Modelfile
    ollama create qwen2.5-coder-32k -f Modelfile
    
[/code]

**Вы не можете установить длину контекста через OpenAI-совместимый API** (`/v1/chat/completions`). Она должна быть настроена на стороне сервера или через Modelfile. Это источник #1 путаницы при интеграции Ollama с инструментами, такими как Hermes.

**Проверьте, что контекст установлен правильно:**

[code] 
    ollama ps
    # Посмотрите на столбец CONTEXT — он должен показывать ваше настроенное значение
    
[/code]

Совет
Список доступных моделей: `ollama list`. Скачайте любую модель из [библиотеки Ollama](<https://ollama.com/library>) с помощью `ollama pull <model>`. Ollama автоматически обрабатывает выгрузку на GPU — для большинства конфигураций настройка не требуется.

* * *

### vLLM — Высокопроизводительный GPU-инференс[​](<#vllm--high-performance-gpu-inference> "Прямая ссылка на vLLM — Высокопроизводительный GPU-инференс")

[vLLM](<https://docs.vllm.ai/>) — стандарт для продакшн-обслуживания LLM. Лучше всего подходит для: максимальной пропускной способности на GPU-оборудовании, обслуживания больших моделей, непрерывного пакетирования.

[code] 
    pip install vllm
    vllm serve meta-llama/Llama-3.1-70B-Instruct \
      --port 8000 \
      --max-model-len 65536 \
      --tensor-parallel-size 2 \
      --enable-auto-tool-choice \
      --tool-call-parser hermes
    
[/code]

Затем настройте Hermes:

[code] 
    hermes model
    # Выберите «Custom endpoint (self-hosted / VLLM / etc.)»
    # Введите URL: http://localhost:8000/v1
    # Пропустите API-ключ (или введите, если вы настроили vLLM с --api-key)
    # Введите имя модели: meta-llama/Llama-3.1-70B-Instruct
    
[/code]

**Длина контекста:** vLLM считывает `max_position_embeddings` модели по умолчанию. Если это превышает вашу GPU-память, он выдаёт ошибку и просит установить `--max-model-len` меньше. Вы также можете использовать `--max-model-len auto` для автоматического поиска максимального значения, которое помещается. Установите `--gpu-memory-utilization 0.95` (по умолчанию 0.9), чтобы выжать больше контекста в VRAM.

**Вызов инструментов требует явных флагов:**

| Флаг | Назначение |
|---|---|
| `--enable-auto-tool-choice` | Требуется для `tool_choice: "auto"` (по умолчанию в Hermes) |
| `--tool-call-parser <name>` | Парсер для формата вызова инструментов модели |

Поддерживаемые парсеры: `hermes` (Qwen 2.5, Hermes 2/3), `llama3_json` (Llama 3.x), `mistral`, `deepseek_v3`, `deepseek_v31`, `xlam`, `pythonic`. Без этих флагов вызов инструментов не будет работать — модель будет выводить вызовы инструментов как текст.

Совет
vLLM поддерживает человекочитаемые размеры: `--max-model-len 64k` (строчная k = 1000, заглавная K = 1024).

* * *

### SGLang — Быстрое обслуживание с RadixAttention[​](<#sglang--fast-serving-with-radixattention> "Прямая ссылка на SGLang — Быстрое обслуживание с RadixAttention")

[SGLang](<https://github.com/sgl-project/sglang>) — альтернатива vLLM с RadixAttention для повторного использования KV-кэша. Лучше всего подходит для: многошаговых разговоров (кэширование префиксов), ограниченной декодировки, структурированного вывода.

[code] 
    pip install "sglang[all]"
    python -m sglang.launch_server \
      --model meta-llama/Llama-3.1-70B-Instruct \
      --port 30000 \
      --context-length 65536 \
      --tp 2 \
      --tool-call-parser qwen
    
[/code]

Затем настройте Hermes:

[code] 
    hermes model
    # Выберите «Custom endpoint (self-hosted / VLLM / etc.)»
    # Введите URL: http://localhost:30000/v1
    # Введите имя модели: meta-llama/Llama-3.1-70B-Instruct
    
[/code]

**Длина контекста:** SGLang считывает из конфига модели по умолчанию. Используйте `--context-length` для переопределения. Если вам нужно превысить заявленный максимум модели, установите `SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1`.

**Вызов инструментов:** Используйте `--tool-call-parser` с соответствующим парсером для вашего семейства моделей: `qwen` (Qwen 2.5), `llama3`, `llama4`, `deepseekv3`, `mistral`, `glm`. Без этого флага вызовы инструментов будут возвращаться как обычный текст.

SGLang по умолчанию ограничивает вывод 128 токенами
Если ответы кажутся обрезанными, добавьте `max_tokens` в ваши запросы или установите `--default-max-tokens` на сервере. По умолчанию SGLang выводит только 128 токенов за ответ, если не указано в запросе.

* * *

### llama.cpp / llama-server — CPU и Metal инференс[​](<#llamacpp--llama-server--cpu--metal-inference> "Прямая ссылка на llama.cpp / llama-server — CPU и Metal инференс")

[llama.cpp](<https://github.com/ggml-org/llama.cpp>) запускает квантизованные модели на CPU, Apple Silicon (Metal) и потребительских GPU. Лучше всего подходит для: запуска моделей без датацентрового GPU, пользователей Mac, пограничных развёртываний.

[code] 
    # Сборка и запуск llama-server
    cmake -B build && cmake --build build --config Release
    ./build/bin/llama-server \
      --jinja -fa \
      -c 32768 \
      -ngl 99 \
      -m models/qwen2.5-coder-32b-instruct-Q4_K_M.gguf \
      --port 8080 --host 0.0.0.0
    
[/code]

**Длина контекста (`-c`):** Новые сборки по умолчанию используют `0`, что считывает контекст обучения модели из GGUF-метаданных. Для моделей с 128k+ контекстом обучения это может вызвать нехватку памяти при попытке выделить полный KV-кэш. Устанавливайте `-c` явно на нужное вам значение (32k–64k — хороший диапазон для использования агента). При использовании параллельных слотов (`-np`) общий контекст делится между слотами — с `-c 32768 -np 4` каждый слот получает только 8k.

Затем настройте Hermes, чтобы указать на него:

[code] 
    hermes model
    # Выберите «Custom endpoint (self-hosted / VLLM / etc.)»
    # Введите URL: http://localhost:8080/v1
    # Пропустите API-ключ (локальные серверы не требуют ключа)
    # Введите имя модели — или оставьте пустым для автоопределения, если загружена только одна модель
    
[/code]

Это сохраняет эндпоинт в `config.yaml`, так что он сохраняется между сессиями.

`--jinja` требуется для вызова инструментов
Без `--jinja` llama-server полностью игнорирует параметр `tools`. Модель попытается вызывать инструменты, записывая JSON в тексте ответа, но Hermes не распознает это как вызов инструмента — вы увидите сырой JSON вида `{"name": "web_search", ...}` выведенный как сообщение вместо реального поиска.

Встроенная поддержка вызова инструментов (наилучшая производительность): Llama 3.x, Qwen 2.5 (включая Coder), Hermes 2/3, Mistral, DeepSeek, Functionary. Все остальные модели используют универсальный обработчик, который работает, но может быть менее эффективным. См. полный список в [документации llama.cpp по вызову функций](<https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md>).

Вы можете проверить, активна ли поддержка инструментов, запросив `http://localhost:8080/props` — поле `chat_template` должно присутствовать.

Совет
Скачивайте GGUF-модели с [Hugging Face](<https://huggingface.co/models?library=gguf>). Квантизация Q4_K_M предлагает наилучший баланс между качеством и использованием памяти.

* * *

### LM Studio — Десктопное приложение с локальными моделями[​](<#lm-studio--desktop-app-with-local-models> "Прямая ссылка на LM Studio — Десктопное приложение с локальными моделями")

[LM Studio](<https://lmstudio.ai/>) — десктопное приложение для запуска локальных моделей с графическим интерфейсом. Лучше всего подходит для: пользователей, предпочитающих визуальный интерфейс, быстрого тестирования моделей, разработчиков на macOS/Windows/Linux.

Запустите сервер из приложения LM Studio (вкладка Developer → Start Server) или используйте CLI:

[code] 
    lms server start                        # Запускается на порту 1234
    lms load qwen2.5-coder --context-length 32768
    
[/code]

Затем настройте Hermes:

[code] 
    hermes model
    # Выберите «LM Studio»
    # Нажмите Enter, чтобы использовать http://localhost:1234/v1
    # Выберите одну из обнаруженных моделей
    # Если аутентификация сервера LM Studio включена, введите LM_API_KEY при запросе
    
[/code]

Hermes автоматически загрузит модель LM Studio с длиной контекста 64K
Чтобы изменить длину контекста в LM Studio:

  1. Нажмите на значок шестерёнки рядом с выбором модели
  2. Установите «Context Length» как минимум 64000 для комфортной работы
  3. Перезагрузите модель, чтобы изменения вступили в силу
  4. Если ваша машина не может вместить 64000, рассмотрите использование модели меньшего размера с большей длиной контекста.

Альтернативно, используйте CLI: `lms load model-name --context-length 64000`
Вы можете использовать CLI для оценки, поместится ли модель: `lms load model-name --context-length 64000 --estimate-only`
Чтобы установить постоянные значения по умолчанию для каждой модели: вкладка My Models → значок шестерёнки на модели → установите размер контекста. :::

**Вызов инструментов:** Поддерживается с LM Studio 0.3.6. Модели с нативным обучением вызову инструментов (Qwen 2.5, Llama 3.x, Mistral, Hermes) автоматически определяются и отображаются со значком инструмента. Другие модели используют универсальный запасной вариант, который может быть менее надёжным.

* * *

### Сетевое взаимодействие WSL2 (пользователи Windows)[​](<#wsl2-networking-windows-users> "Прямая ссылка на Сетевое взаимодействие WSL2 (пользователи Windows)")

Поскольку Hermes Agent требует Unix-окружения, пользователи Windows запускают его внутри WSL2. Если ваш сервер моделей (Ollama, LM Studio и т.д.) работает на **хост-машине Windows**, вам нужно преодолеть сетевой разрыв — WSL2 использует виртуальный сетевой адаптер с собственной подсетью, поэтому `localhost` внутри WSL2 ссылается на Linux VM, **а не** на хост Windows.

Оба в WSL2? Нет проблем.
Если ваш сервер моделей также работает внутри WSL2 (обычно для vLLM, SGLang и llama-server), `localhost` работает как ожидается — они находятся в одном сетевом пространстве. Пропустите этот раздел.

#### Вариант 1: Режим зеркальной сети (рекомендуется)[​](<#option-1-mirrored-networking-mode-recommended> "Прямая ссылка на Вариант 1: Режим зеркальной сети (рекомендуется)")

Доступно на **Windows 11 22H2+** , зеркальный режим заставляет `localhost` работать двунаправленно между Windows и WSL2 — самое простое решение.

  1. Создайте или отредактируйте `%USERPROFILE%\\.wslconfig` (например, `C:\\Users\\YourName\\.wslconfig`):

[code] [wsl2]
         networkingMode=mirrored
         
[/code]

  2. Перезапустите WSL из PowerShell:

[code] wsl --shutdown
         
[/code]

  3. Откройте терминал WSL2 снова. `localhost` теперь достигает сервисов Windows:

[code] curl http://localhost:11434/v1/models   # Ollama на Windows — работает
         
[/code]

Брандмауэр Hyper-V
В некоторых сборках Windows 11 брандмауэр Hyper-V блокирует зеркальные соединения по умолчанию. Если `localhost` всё ещё не работает после включения зеркального режима, выполните это в **PowerShell от имени администратора**:

[code]
    Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow
    
[/code]

#### Вариант 2: Использование IP хоста Windows (Windows 10 / старые сборки)[​](<#option-2-use-the-windows-host-ip-windows-10--older-builds> "Прямая ссылка на Вариант 2: Использование IP хоста Windows (Windows 10 / старые сборки)")

Если вы не можете использовать зеркальный режим, найдите IP хоста Windows изнутри WSL2 и используйте его вместо `localhost`:

[code] 
    # Получить IP хоста Windows (шлюз по умолчанию виртуальной сети WSL2)
    ip route show | grep -i default | awk '{ print $3 }'
    # Пример вывода: 172.29.192.1
    
[/code]

Используйте этот IP в конфигурации Hermes:

[code] 
    model:
      default: qwen2.5-coder:32b
      provider: custom
      base_url: http://172.29.192.1:11434/v1   # IP хоста Windows, не localhost
    
[/code]

Динамический помощник
IP хоста может меняться при перезапуске WSL2. Вы можете получать его динамически в вашей оболочке:

[code]
    export WSL_HOST=$(ip route show | grep -i default | awk '{ print $3 }')
    echo "Windows host at: $WSL_HOST"
    curl http://$WSL_HOST:11434/v1/models   # Тест Ollama
    
[/code]

Или используйте mDNS-имя вашей машины (требуется `libnss-mdns` в WSL2):

[code]
    sudo apt install libnss-mdns
    curl http://$(hostname).local:11434/v1/models
    
[/code]

#### Привязка сервера (требуется для NAT-режима)[​](<#server-bind-address-required-for-nat-mode> "Прямая ссылка на Привязка сервера (требуется для NAT-режима)")

Если вы используете **Вариант 2** (NAT-режим с IP хоста), сервер моделей на Windows должен принимать соединения не только с `127.0.0.1`. По умолчанию большинство серверов слушают только localhost — соединения из WSL2 в NAT-режиме приходят из другой виртуальной подсети и будут отклонены. В зеркальном режиме `localhost` отображается напрямую, поэтому привязка к `127.0.0.1` по умолчанию работает нормально.

| Сервер | Привязка по умолчанию | Как исправить |
|---|---|---|
| **Ollama** | `127.0.0.1` | Установите переменную окружения `OLLAMA_HOST=0.0.0.0` перед запуском Ollama (System Settings → Environment Variables в Windows, или отредактируйте службу Ollama) |
| **LM Studio** | `127.0.0.1` | Включите **«Serve on Network»** на вкладке Developer → Server settings |
| **llama-server** | `127.0.0.1` | Добавьте `--host 0.0.0.0` в команду запуска |
| **vLLM** | `0.0.0.0` | Уже привязан ко всем интерфейсам по умолчанию |
| **SGLang** | `127.0.0.1` | Добавьте `--host 0.0.0.0` в команду запуска |
| **Ollama на Windows (подробно):** Ollama работает как служба Windows. Чтобы установить `OLLAMA_HOST`:

  1. Откройте **System Properties** → **Environment Variables**
  2. Добавьте новую **системную переменную**: `OLLAMA_HOST` = `0.0.0.0`
  3. Перезапустите службу Ollama (или перезагрузите компьютер)

#### Брандмауэр Windows[​](<#windows-firewall> "Прямая ссылка на Брандмауэр Windows")

Брандмауэр Windows рассматривает WSL2 как отдельную сеть (как в NAT, так и в зеркальном режиме). Если соединения всё равно не работают после выполнения шагов выше, добавьте правило брандмауэра для порта вашего сервера моделей:

[code] 
    # Выполните в PowerShell от имени администратора — замените PORT на порт вашего сервера
    New-NetFirewallRule -DisplayName "Allow WSL2 to Model Server" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 11434
    
[/code]

Распространённые порты: Ollama `11434`, vLLM `8000`, SGLang `30000`, llama-server `8080`, LM Studio `1234`.

#### Быстрая проверка[​](<#quick-verification> "Прямая ссылка на Быстрая проверка")

Изнутри WSL2 проверьте, что вы можете подключиться к вашему серверу моделей:

[code] 
    # Замените URL на адрес и порт вашего сервера
    curl http://localhost:11434/v1/models          # Зеркальный режим
    curl http://172.29.192.1:11434/v1/models       # NAT-режим (используйте ваш фактический IP хоста)
    
[/code]

Если вы получили JSON-ответ со списком ваших моделей, всё в порядке. Используйте тот же URL в качестве `base_url` в конфигурации Hermes.

* * *

### Устранение неполадок локальных моделей[​](<#troubleshooting-local-models> "Прямая ссылка на Устранение неполадок локальных моделей")

Эти проблемы затрагивают **все** локальные серверы инференса при использовании с Hermes.

#### «Connection refused» из WSL2 к серверу моделей на Windows[​](<#connection-refused-from-wsl2-to-a-windows-hosted-model-server> "Прямая ссылка на «Connection refused» из WSL2 к серверу моделей на Windows")

Если вы запускаете Hermes внутри WSL2, а ваш сервер моделей на хост-машине Windows, `http://localhost:<port>` не будет работать в режиме сети NAT по умолчанию WSL2. См. [Сетевое взаимодействие WSL2](<#wsl2-networking-windows-users>) выше для решения.

#### Вызовы инструментов отображаются как текст вместо выполнения[​](<#tool-calls-appear-as-text-instead-of-executing> "Прямая ссылка на Вызовы инструментов отображаются как текст вместо выполнения")

Модель выводит что-то вроде `{"name": "web_search", "arguments": {...}}` как сообщение вместо фактического вызова инструмента.

**Причина:** На вашем сервере не включена поддержка вызова инструментов, или модель не поддерживает его через реализацию вызова инструментов сервера.

| Сервер | Исправление |
|---|---|
| **llama.cpp** | Добавьте `--jinja` в команду запуска |
| **vLLM** | Добавьте `--enable-auto-tool-choice --tool-call-parser hermes` |
| **SGLang** | Добавьте `--tool-call-parser qwen` (или соответствующий парсер) |
| **Ollama** | Вызов инструментов включён по умолчанию — убедитесь, что ваша модель его поддерживает (проверьте с помощью `ollama show model-name`) |
| **LM Studio** | Обновитесь до 0.3.6+ и используйте модель с нативной поддержкой инструментов |

#### Модель забывает контекст или выдаёт бессвязные ответы[​](<#model-seems-to-forget-context-or-give-incoherent-responses> "Прямая ссылка на Модель забывает контекст или выдаёт бессвязные ответы")

**Причина:** Слишком маленькое окно контекста. Когда разговор превышает лимит контекста, большинство серверов молча отбрасывают старые сообщения. Системный промпт + схемы инструментов Hermes сами по себе могут использовать 4k–8k токенов.

**Диагностика:**

[code] 
    # Проверьте, какой контекст видит Hermes
    # Посмотрите на строку запуска: «Context limit: X tokens»
      
    # Проверьте фактический контекст вашего сервера
    # Ollama: ollama ps (столбец CONTEXT)
    # llama.cpp: curl http://localhost:8080/props | jq '.default_generation_settings.n_ctx'
    # vLLM: проверьте --max-model-len в аргументах запуска
    
[/code]

**Исправление:** Установите контекст как минимум **32 768 токенов** для использования агента. См. раздел каждого сервера выше для соответствующего флага.

#### «Context limit: 2048 tokens» при запуске[​](<#context-limit-2048-tokens-at-startup> "Прямая ссылка на «Context limit: 2048 tokens» при запуске")

Hermes автоматически определяет длину контекста из эндпоинта `/v1/models` вашего сервера. Если сервер сообщает низкое значение (или не сообщает его вообще), Hermes использует заявленный лимит модели, который может быть неверным.

**Исправление:** Установите явно в `config.yaml`:

[code] 
    model:
      default: your-model
      provider: custom
      base_url: http://localhost:11434/v1
      context_length: 32768
    
[/code]

#### Ответы обрезаются на середине предложения[​](<#responses-get-cut-off-mid-sentence> "Прямая ссылка на Ответы обрезаются на середине предложения")

**Возможные причины:**

  1. **Низкий лимит вывода (`max_tokens`) на сервере** — SGLang по умолчанию выдаёт 128 токенов за ответ. Установите `--default-max-tokens` на сервере или настройте Hermes с помощью `model.max_tokens` в config.yaml. Примечание: `max_tokens` управляет длиной ответа — он не связан с длиной истории вашего разговора (за это отвечает `context_length`).
  2. **Истощение контекста** — Модель заполнила своё окно контекста. Увеличьте `model.context_length` или включите [сжатие контекста](</docs/user-guide/configuration#context-compression>) в Hermes.

* * *

### LiteLLM Proxy — Многопровайдерный шлюз[​](<#litellm-proxy--multi-provider-gateway> "Прямая ссылка на LiteLLM Proxy — Многопровайдерный шлюз")

[LiteLLM](<https://docs.litellm.ai/>) — это OpenAI-совместимый прокси, который объединяет 100+ LLM-провайдеров за единым API. Лучше всего подходит для: переключения между провайдерами без изменения конфигурации, балансировки нагрузки, цепочек резервных провайдеров, контроля бюджета.

[code] 
    # Установка и запуск
    pip install "litellm[proxy]"
    litellm --model anthropic/claude-sonnet-4 --port 4000
      
    # Или с файлом конфигурации для нескольких моделей:
    litellm --config litellm_config.yaml --port 4000
    
[/code]

Затем настройте Hermes с помощью `hermes model` → Custom endpoint → `http://localhost:4000/v1`.

Пример `litellm_config.yaml` с резервным провайдером:

[code] 
    model_list:
      - model_name: "best"
        litellm_params:
          model: anthropic/claude-sonnet-4
          api_key: sk-ant-...
      - model_name: "best"
        litellm_params:
          model: openai/gpt-4o
          api_key: sk-...
    router_settings:
      routing_strategy: "latency-based-routing"
    
[/code]

* * *

### ClawRouter — Маршрутизация с оптимизацией стоимости[​](<#clawrouter--cost-optimized-routing> "Прямая ссылка на ClawRouter — Маршрутизация с оптимизацией стоимости")

[ClawRouter](<https://github.com/BlockRunAI/ClawRouter>) от BlockRunAI — это локальный прокси-маршрутизатор, который автоматически выбирает модели на основе сложности запроса. Он классифицирует запросы по 14 измерениям и направляет к самой дешёвой модели, способной выполнить задачу. Оплата производится криптовалютой USDC (без API-ключей).

[code] 
    # Установка и запуск
    npx @blockrun/clawrouter    # Запускается на порту 8402
    
[/code]

Затем настройте Hermes с помощью `hermes model` → Custom endpoint → `http://localhost:8402/v1` → имя модели `blockrun/auto`.

Профили маршрутизации:

| Профиль | Стратегия | Экономия |
|---|---|---|
| `blockrun/auto` | Сбалансированное качество/стоимость | 74-100% |
| `blockrun/eco` | Максимально дешёвый | 95-100% |
| `blockrun/premium` | Модели наилучшего качества | 0% |
| `blockrun/free` | Только бесплатные модели | 100% |
| `blockrun/agentic` | Оптимизировано для использования инструментов | варьируется |

Примечание
ClawRouter требует кошелёк, пополненный в USDC на Base или Solana для оплаты. Все запросы направляются через бэкенд API BlockRun. Выполните `npx @blockrun/clawrouter doctor` для проверки статуса кошелька.

* * *

### Другие совместимые провайдеры[​](<#other-compatible-providers> "Прямая ссылка на Другие совместимые провайдеры")

Любой сервис с OpenAI-совместимым API работает. Некоторые популярные варианты:

| Провайдер | Базовый URL | Примечания |
|---|---|---|
| [Together AI](<https://together.ai>) | `https://api.together.xyz/v1` | Облачные открытые модели |
| [Groq](<https://groq.com>) | `https://api.groq.com/openai/v1` | Сверхбыстрый инференс |
| [DeepSeek](<https://deepseek.com>) | `https://api.deepseek.com/v1` | Модели DeepSeek |
| [Fireworks AI](<https://fireworks.ai>) | `https://api.fireworks.ai/inference/v1` | Быстрый хостинг открытых моделей |
| [GMI Cloud](<https://www.gmicloud.ai/>) | `https://api.gmi-serving.com/v1` | Управляемый OpenAI-совместимый инференс |
| [Cerebras](<https://cerebras.ai>) | `https://api.cerebras.ai/v1` | Инференс на пластинах |
| [Mistral AI](<https://mistral.ai>) | `https://api.mistral.ai/v1` | Модели Mistral |
| [OpenAI](<https://openai.com>) | `https://api.openai.com/v1` | Прямой доступ к OpenAI |
| [Azure OpenAI](<https://azure.microsoft.com>) | `https://YOUR.openai.azure.com/` | Корпоративный OpenAI |
| [LocalAI](<https://localai.io>) | `http://localhost:8080/v1` | Самостоятельный хостинг, несколько моделей |
| [Jan](<https://jan.ai>) | `http://localhost:1337/v1` | Десктопное приложение с локальными моделями |

Настройте любой из них с помощью `hermes model` → Custom endpoint, или в `config.yaml`:

[code] 
    model:
      default: meta-llama/Llama-3.1-70B-Instruct-Turbo
      provider: custom
      base_url: https://api.together.xyz/v1
      api_key: your-together-key
    
[/code]

* * *

### Определение длины контекста[​](<#context-length-detection> "Прямая ссылка на Определение длины контекста")

Две настройки, которые легко перепутать
**`context_length`** — это **общее окно контекста** — совокупный бюджет для входных _и_ выходных токенов (например, 200 000 для Claude Opus 4.6). Hermes использует это для решения, когда сжимать историю, и для проверки API-запросов.
**`model.max_tokens`** — это **лимит вывода** — максимальное количество токенов, которое модель может сгенерировать в _одном ответе_. Это не имеет никакого отношения к длине истории вашего разговора. Стандартное отраслевое имя `max_tokens` является распространённым источником путаницы; нативный API Anthropic переименовал его в `max_output_tokens` для ясности.

Устанавливайте `context_length`, когда автоопределение ошибается с размером окна. Устанавливайте `model.max_tokens` только когда вам нужно ограничить длину отдельных ответов.

Hermes использует многозвенную цепочку разрешения для определения правильного окна контекста для вашей модели и провайдера:

  1. **Переопределение в конфиге** — `model.context_length` в config.yaml (наивысший приоритет)
  2. **Пользовательский провайдер для модели** — `custom_providers[].models.<id>.context_length`
  3. **Постоянный кэш** — ранее найденные значения (сохраняются между перезапусками)
  4. **Эндпоинт `/models`** — запрос к API вашего сервера (локальные/пользовательские эндпоинты)
  5. **Anthropic `/v1/models`** — запрос к API Anthropic для `max_input_tokens` (только для пользователей API-ключа)
  6. **OpenRouter API** — живые метаданные моделей от OpenRouter
  7. **Nous Portal** — сопоставление суффиксов ID моделей Nous с метаданными OpenRouter
  8. **[models.dev](<https://models.dev>)** — реестр, поддерживаемый сообществом, с длинами контекста для конкретных провайдеров для 3800+ моделей от 100+ провайдеров
  9. **Запасные значения по умолчанию** — общие шаблоны семейств моделей (128K по умолчанию)

Для большинства конфигураций это работает «из коробки». Система учитывает провайдера — одна и та же модель может иметь разные лимиты контекста в зависимости от того, кто её обслуживает (например, `claude-opus-4.6` имеет 1M напрямую от Anthropic, но 128K на GitHub Copilot).

Чтобы установить длину контекста явно, добавьте `context_length` в конфигурацию модели:

[code] 
    model:
      default: "qwen3.5:9b"
      base_url: "http://localhost:8080/v1"
      context_length: 131072  # токенов
    
[/code]

Для пользовательских эндпоинтов вы также можете установить длину контекста для каждой модели:

[code] 
    custom_providers:
      - name: "My Local LLM"
        base_url: "http://localhost:11434/v1"
        models:
          qwen3.5:27b:
            context_length: 32768
          deepseek-r1:70b:
            context_length: 65536
    
[/code]

`hermes model` запросит длину контекста при настройке пользовательского эндпоинта. Оставьте пустым для автоопределения.

Когда устанавливать это вручную

  * Вы используете Ollama с пользовательским `num_ctx`, который ниже максимума модели
  * Вы хотите ограничить контекст ниже максимума модели (например, 8k на 128k модели для экономии VRAM)
  * Вы работаете за прокси, который не предоставляет `/v1/models`

* * *

### Именованные пользовательские провайдеры[​](<#named-custom-providers> "Прямая ссылка на Именованные пользовательские провайдеры")

Если вы работаете с несколькими пользовательскими эндпоинтами (например, локальный сервер разработки и удалённый GPU-сервер), вы можете определить их как именованные пользовательские провайдеры в `config.yaml`:

[code] 
    custom_providers:
      - name: local
        base_url: http://localhost:8080/v1
        # api_key опущен — Hermes использует «no-key-required» для серверов без ключа
      - name: work
        base_url: https://gpu-server.internal.corp/v1
        key_env: CORP_API_KEY
        api_mode: chat_completions   # опционально, автоопределяется из URL
      - name: anthropic-proxy
        base_url: https://proxy.example.com/anthropic
        key_env: ANTHROPIC_PROXY_KEY
        api_mode: anthropic_messages  # для прокси, совместимых с Anthropic
    
[/code]

Переключайтесь между ними в середине сессии с помощью тройного синтаксиса:

[code] 
    /model custom:local:qwen-2.5       # Использовать эндпоинт «local» с qwen-2.5
    /model custom:work:llama3-70b      # Использовать эндпоинт «work» с llama3-70b
    /model custom:anthropic-proxy:claude-sonnet-4  # Использовать прокси
    
[/code]

Вы также можете выбирать именованные пользовательские провайдеры из интерактивного меню `hermes model`.

* * *

### Кулинарная книга: Together AI, Groq, Perplexity[​](<#cookbook-together-ai-groq-perplexity> "Прямая ссылка на Кулинарная книга: Together AI, Groq, Perplexity")

Облачные провайдеры, перечисленные в [Другие совместимые провайдеры](<#other-compatible-providers>), все говорят на REST-диалекте OpenAI, поэтому они настраиваются одинаково в разделе `custom_providers:`. Ниже приведены три рабочих рецепта. Каждый вставляется в `~/.hermes/config.yaml`, а соответствующий API-ключ — в `~/.hermes/.env`.

#### Together AI[​](<#together-ai> "Прямая ссылка на Together AI")

Хостит модели с открытым весом (Llama, MiniMax, Gemma, DeepSeek, Qwen) по ценам значительно ниже, чем у первых сторон. Хороший выбор для работы с несколькими моделями.

[code] 
    # ~/.hermes/config.yaml
    custom_providers:
      - name: together
        base_url: https://api.together.xyz/v1
        key_env: TOGETHER_API_KEY
        # api_mode: chat_completions  # по умолчанию — не нужно устанавливать
      
    model:
      default: MiniMaxAI/MiniMax-M2.7   # или любая модель с together.ai/models
      provider: custom:together
    
[/code]

[code] 
    # ~/.hermes/.env
    TOGETHER_API_KEY=your-together-key
    
[/code]

Переключайте модели в середине сессии:

[code] 
    /model custom:together:meta-llama/Llama-3.3-70B-Instruct-Turbo
    /model custom:together:google/gemma-4-31b-it
    /model custom:together:deepseek-ai/DeepSeek-V3
    
[/code]

Эндпоинт `/v1/models` Together работает, поэтому `hermes model` может автоматически обнаруживать доступные модели.

#### Groq[​](<#groq> "Прямая ссылка на Groq")

Сверхбыстрый инференс (~500 токенов/с на Llama-3.3-70B). Небольшой каталог, но мощный для интерактивного использования, чувствительного к задержкам.

[code] 
    # ~/.hermes/config.yaml
    custom_providers:
      - name: groq
        base_url: https://api.groq.com/openai/v1
        key_env: GROQ_API_KEY
      
    model:
      default: llama-3.3-70b-versatile
      provider: custom:groq
    
[/code]

[code] 
    # ~/.hermes/.env
    GROQ_API_KEY=your-groq-key
    
[/code]

#### Perplexity[​](<#perplexity> "Прямая ссылка на Perplexity")

Полезно, когда вам нужна модель, которая автоматически выполняет поиск в вебе и цитирование. Строгая политика доступности моделей — проверьте [perplexity.ai/settings/api](<https://www.perplexity.ai/settings/api>) для актуального списка.

[code] 
    # ~/.hermes/config.yaml
    custom_providers:
      - name: perplexity
        base_url: https://api.perplexity.ai
        key_env: PERPLEXITY_API_KEY
      
    model:
      default: sonar
      provider: custom:perplexity
    
[/code]

[code] 
    # ~/.hermes/.env
    PERPLEXITY_API_KEY=your-perplexity-key
    
[/code]

#### Несколько провайдеров в одной конфигурации[​](<#multiple-providers-in-one-config> "Прямая ссылка на Несколько провайдеров в одной конфигурации")

Три рецепта объединяются — используйте все вместе и переключайтесь между шагами с помощью `/model custom:<name>:<model>`:

[code] 
    custom_providers:
      - name: together
        base_url: https://api.together.xyz/v1
        key_env: TOGETHER_API_KEY
      - name: groq
        base_url: https://api.groq.com/openai/v1
        key_env: GROQ_API_KEY
      - name: perplexity
        base_url: https://api.perplexity.ai
        key_env: PERPLEXITY_API_KEY
      
    model:
      default: MiniMaxAI/MiniMax-M2.7
      provider: custom:together      # старт с Together; переключайтесь свободно после
    
[/code]

Устранение неполадок

  * `hermes doctor` не должен выводить предупреждений «Unknown provider» для любых из этих имён после исправлений валидатора CLI в #15083.
  * Если эндпоинт `/v1/models` провайдера недоступен (Perplexity — частый случай), `hermes model` сохранит модель с предупреждением, а не жёстко отвергнет — см. #15136.
  * Чтобы полностью пропустить `custom_providers:` и использовать обычный `provider: custom` с переменной окружения `CUSTOM_BASE_URL`, см. #15103.

* * *

### Выбор правильной конфигурации[​](<#choosing-the-right-setup> "Прямая ссылка на Выбор правильной конфигурации")

| Сценарий использования | Рекомендация |
|---|---|
| **Просто чтобы работало** | OpenRouter (по умолчанию) или Nous Portal |
| **Локальные модели, простая настройка** | Ollama |
| **Продакшн GPU-обслуживание** | vLLM или SGLang |
| **Mac / нет GPU** | Ollama или llama.cpp |
| **Многопровайдерная маршрутизация** | LiteLLM Proxy или OpenRouter |
| **Оптимизация стоимости** | ClawRouter или OpenRouter с `sort: "price"` |
| **Максимальная приватность** | Ollama, vLLM или llama.cpp (полностью локально) |
| **Корпоративный / Azure** | Azure OpenAI с пользовательским эндпоинтом |
| **Китайские AI-модели** | z.ai (GLM), Kimi/Moonshot (`kimi-coding` или `kimi-coding-cn`), MiniMax, Xiaomi MiMo или Tencent TokenHub (полноценные провайдеры) |

Совет
Вы можете переключаться между провайдерами в любое время с помощью `hermes model` — перезапуск не требуется. История вашего разговора, память и навыки сохраняются независимо от того, какого провайдера вы используете.

## Опциональные API-ключи[​](<#optional-api-keys> "Прямая ссылка на Опциональные API-ключи")

| Функция | Провайдер | Переменная окружения |
|---|---|---|
| Веб-скрапинг | [Firecrawl](<https://firecrawl.dev/>) | `FIRECRAWL_API_KEY`, `FIRECRAWL_API_URL` |
| Автоматизация браузера | [Browserbase](<https://browserbase.com/>) | `BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID` |
| Генерация изображений | [FAL](<https://fal.ai/>) | `FAL_KEY` |
| Премиум TTS-голоса | [ElevenLabs](<https://elevenlabs.io/>) | `ELEVENLABS_API_KEY` |
| OpenAI TTS + транскрипция голоса | [OpenAI](<https://platform.openai.com/api-keys>) | `VOICE_TOOLS_OPENAI_KEY` |
| Mistral TTS + транскрипция голоса | [Mistral](<https://console.mistral.ai/>) | `MISTRAL_API_KEY` |
| RL-обучение | [Tinker](<https://tinker-console.thinkingmachines.ai/>) + [WandB](<https://wandb.ai/>) | `TINKER_API_KEY`, `WANDB_API_KEY` |
| Моделирование пользователя между сессиями | [Honcho](<https://honcho.dev/>) | `HONCHO_API_KEY` |
| Семантическая долговременная память | [Supermemory](<https://supermemory.ai>) | `SUPERMEMORY_API_KEY` |

### Самостоятельный хостинг Firecrawl[​](<#self-hosting-firecrawl> "Прямая ссылка на Самостоятельный хостинг Firecrawl")

По умолчанию Hermes использует [облачное API Firecrawl](<https://firecrawl.dev/>) для веб-поиска и скрапинга. Если вы предпочитаете запускать Firecrawl локально, вы можете указать Hermes на самостоятельный экземпляр. См. [SELF_HOST.md](<https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md>) Firecrawl для полных инструкций по настройке.

**Что вы получаете:** Без API-ключа, без лимитов запросов, без затрат на страницу, полный суверенитет данных.

**Что вы теряете:** Облачная версия использует проприетарный «Fire-engine» Firecrawl для продвинутого обхода анти-бот-систем (Cloudflare, CAPTCHA, ротация IP). Самостоятельный хостинг использует базовый fetch + Playwright, поэтому некоторые защищённые сайты могут не работать. Поиск использует DuckDuckGo вместо Google.

**Настройка:**

  1. Клонируйте и запустите Docker-стек Firecrawl (5 контейнеров: API, Playwright, Redis, RabbitMQ, PostgreSQL — требуется ~4-8 ГБ ОЗУ):

[code] git clone https://github.com/firecrawl/firecrawl
         cd firecrawl
         # В .env установите: USE_DB_AUTHENTICATION=false, HOST=0.0.0.0, PORT=3002
         docker compose up -d
         
[/code]

  2. Укажите Hermes на ваш экземпляр (API-ключ не нужен):

[code] hermes config set FIRECRAWL_API_URL http://localhost:3002
         
[/code]

Вы также можете установить оба `FIRECRAWL_API_KEY` и `FIRECRAWL_API_URL`, если на вашем экземпляре включена аутентификация.

## Маршрутизация провайдеров OpenRouter[​](<#openrouter-provider-routing> "Прямая ссылка на Маршрутизация провайдеров OpenRouter")

При использовании OpenRouter вы можете управлять тем, как запросы направляются между провайдерами. Добавьте секцию `provider_routing` в `~/.hermes/config.yaml`:

[code] 
    provider_routing:
      sort: "throughput"          # «price» (по умолчанию), «throughput» или «latency»
      # only: ["anthropic"]      # Использовать только этих провайдеров
      # ignore: ["deepinfra"]    # Пропускать этих провайдеров
      # order: ["anthropic", "google"]  # Пробовать провайдеров в этом порядке
      # require_parameters: true  # Использовать только провайдеров, поддерживающих все параметры запроса
      # data_collection: "deny"   # Исключить провайдеров, которые могут хранить/обучаться на данных
    
[/code]

**Сокращения:** Добавьте `:nitro` к любому имени модели для сортировки по пропускной способности (например, `anthropic/claude-sonnet-4:nitro`), или `:floor` для сортировки по цене.

## Резервная модель[​](<#fallback-model> "Прямая ссылка на Резервная модель")

Настройте резервного провайдера:модель, на которую Hermes автоматически переключится, когда ваша основная модель выйдет из строя (ограничения запросов, ошибки сервера, сбои аутентификации):

[code] 
    fallback_model:
      provider: openrouter                    # обязательно
      model: anthropic/claude-sonnet-4        # обязательно
      # base_url: http://localhost:8000/v1    # опционально, для пользовательских эндпоинтов
      # key_env: MY_CUSTOM_KEY               # опционально, имя переменной окружения для API-ключа пользовательского эндпоинта
    
[/code]

При активации резервная модель заменяет модель и провайдера в середине сессии без потери разговора. Срабатывает **не более одного раза** за сессию.

Поддерживаемые провайдеры: `openrouter`, `nous`, `openai-codex`, `copilot`, `copilot-acp`, `anthropic`, `gemini`, `google-gemini-cli`, `qwen-oauth`, `huggingface`, `zai`, `kimi-coding`, `kimi-coding-cn`, `minimax`, `minimax-cn`, `minimax-oauth`, `deepseek`, `nvidia`, `xai`, `ollama-cloud`, `bedrock`, `ai-gateway`, `opencode-zen`, `opencode-go`, `kilocode`, `xiaomi`, `arcee`, `gmi`, `stepfun`, `alibaba`, `tencent-tokenhub`, `custom`.

Совет
Резервная модель настраивается исключительно через `config.yaml` — для неё нет переменных окружения. Полные сведения о том, когда она срабатывает, поддерживаемых провайдерах и её взаимодействии со вспомогательными задачами и делегированием, см. в [Резервные провайдеры](</docs/user-guide/features/fallback-providers>).

* * *

## См. также[​](<#see-also> "Прямая ссылка на См. также")

  * [Конфигурация](</docs/user-guide/configuration>) — Общая конфигурация (структура директорий, приоритет конфигов, бэкенды терминала, память, сжатие и другое)
  * [Переменные окружения](</docs/reference/environment-variables>) — Полный справочник всех переменных окружения

  * [Провайдеры инференса](<#inference-providers>)
    * [Google Gemini через OAuth (`google-gemini-cli`)](<#google-gemini-via-oauth-google-gemini-cli>)
    * [Две команды для управления моделями](<#two-commands-for-model-management>)
    * [Anthropic (нативный)](<#anthropic-native>)
    * [GitHub Copilot](<#github-copilot>)
    * [Полноценные провайдеры с API-ключом](<#first-class-api-key-providers>)
    * [xAI (Grok) — Responses API + Кэширование промптов](<#xai-grok--responses-api--prompt-caching>)
    * [Ollama Cloud — Управляемые модели Ollama, OAuth + API-ключ](<#ollama-cloud--managed-ollama-models-oauth--api-key>)
    * [AWS Bedrock](<#aws-bedrock>)
    * [Qwen Portal (OAuth)](<#qwen-portal-oauth>)
    * [Alibaba Coding Plan](<#alibaba-coding-plan>)
    * [MiniMax (OAuth)](<#minimax-oauth>)
    * [NVIDIA NIM](<#nvidia-nim>)
    * [GMI Cloud](<#gmi-cloud>)
    * [StepFun](<#stepfun>)
    * [Hugging Face Inference Providers](<#hugging-face-inference-providers>)
  * [Пользовательские и самостоятельно размещённые LLM-провайдеры](<#custom--self-hosted-llm-providers>)
    * [Общая настройка](<#general-setup>)
    * [Переключение моделей с помощью `/model`](<#switching-models-with-model>)
    * [Ollama — Локальные модели, без настройки](<#ollama--local-models-zero-config>)
    * [vLLM — Высокопроизводительный GPU-инференс](<#vllm--high-performance-gpu-inference>)
    * [SGLang — Быстрое обслуживание с RadixAttention](<#sglang--fast-serving-with-radixattention>)
    * [llama.cpp / llama-server — CPU и Metal инференс](<#llamacpp--llama-server--cpu--metal-inference>)
    * [LM Studio — Десктопное приложение с локальными моделями](<#lm-studio--desktop-app-with-local-models>)
    * [Сетевое взаимодействие WSL2 (пользователи Windows)](<#wsl2-networking-windows-users>)
    * [Устранение неполадок локальных моделей](<#troubleshooting-local-models>)
    * [LiteLLM Proxy — Многопровайдерный шлюз](<#litellm-proxy--multi-provider-gateway>)
    * [ClawRouter — Маршрутизация с оптимизацией стоимости](<#clawrouter--cost-optimized-routing>)
    * [Другие совместимые провайдеры](<#other-compatible-providers>)
    * [Определение длины контекста](<#context-length-detection>)
    * [Именованные пользовательские провайдеры](<#named-custom-providers>)
    * [Кулинарная книга: Together AI, Groq, Perplexity](<#cookbook-together-ai-groq-perplexity>)
    * [Выбор правильной конфигурации](<#choosing-the-right-setup>)
  * [Опциональные API-ключи](<#optional-api-keys>)
    * [Самостоятельный хостинг Firecrawl](<#self-hosting-firecrawl>)
  * [Маршрутизация провайдеров OpenRouter](<#openrouter-provider-routing>)
  * [Резервная модель](<#fallback-model>)
  * [См. также](<#see-also>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/integrations/providers -->
