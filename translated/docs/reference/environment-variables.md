On this page
Все переменные находятся в `~/.hermes/.env`. Вы также можете задать их с помощью `hermes config set VAR value`.
## LLM-провайдеры[​](<#llm-providers> "Direct link to LLM Providers")
Переменная| Описание  
---|---  
`OPENROUTER_API_KEY`| API-ключ OpenRouter (рекомендуется для гибкости)  
`OPENROUTER_BASE_URL`| Переопределение базового URL, совместимого с OpenRouter  
`HERMES_OPENROUTER_CACHE`| Включить кеширование ответов OpenRouter (`1`/`true`/`yes`/`on`). Переопределяет `openrouter.response_cache` в config.yaml. См. [Response Caching](<https://openrouter.ai/docs/guides/features/response-caching>).  
`HERMES_OPENROUTER_CACHE_TTL`| Время жизни кеша в секундах (1-86400). Переопределяет `openrouter.response_cache_ttl` в config.yaml.  
`NOUS_BASE_URL`| Переопределение базового URL Nous Portal (требуется редко; только для разработки/тестирования)  
`NOUS_INFERENCE_BASE_URL`| Прямое переопределение эндпоинта инференса Nous  
`AI_GATEWAY_API_KEY`| API-ключ Vercel AI Gateway ([ai-gateway.vercel.sh](<https://ai-gateway.vercel.sh>))  
`AI_GATEWAY_BASE_URL`| Переопределение базового URL AI Gateway (по умолчанию: `https://ai-gateway.vercel.sh/v1`)  
`OPENAI_API_KEY`| API-ключ для пользовательских эндпоинтов, совместимых с OpenAI (используется с `OPENAI_BASE_URL`)  
`OPENAI_BASE_URL`| Базовый URL для пользовательского эндпоинта (VLLM, SGLang и т.д.)  
`COPILOT_GITHUB_TOKEN`| GitHub-токен для Copilot API — наивысший приоритет (OAuth `gho_*` или fine-grained PAT `github_pat_*`; классические PAT `ghp_*` **не поддерживаются**)  
`GH_TOKEN`| GitHub-токен — второй приоритет для Copilot (также используется CLI `gh`)  
`GITHUB_TOKEN`| GitHub-токен — третий приоритет для Copilot  
`HERMES_COPILOT_ACP_COMMAND`| Переопределение пути к бинарнику Copilot ACP CLI (по умолчанию: `copilot`)  
`COPILOT_CLI_PATH`| Псевдоним для `HERMES_COPILOT_ACP_COMMAND`  
`HERMES_COPILOT_ACP_ARGS`| Переопределение аргументов Copilot ACP (по умолчанию: `--acp --stdio`)  
`COPILOT_ACP_BASE_URL`| Переопределение базового URL Copilot ACP  
`GLM_API_KEY`| API-ключ z.ai / ZhipuAI GLM ([z.ai](<https://z.ai>))  
`ZAI_API_KEY`| Псевдоним для `GLM_API_KEY`  
`Z_AI_API_KEY`| Псевдоним для `GLM_API_KEY`  
`GLM_BASE_URL`| Переопределение базового URL z.ai (по умолчанию: `https://api.z.ai/api/paas/v4`)  
`KIMI_API_KEY`| API-ключ Kimi / Moonshot AI ([moonshot.ai](<https://platform.moonshot.ai>))  
`KIMI_BASE_URL`| Переопределение базового URL Kimi (по умолчанию: `https://api.moonshot.ai/v1`)  
`KIMI_CN_API_KEY`| API-ключ Kimi / Moonshot China ([moonshot.cn](<https://platform.moonshot.cn>))  
`ARCEEAI_API_KEY`| API-ключ Arcee AI ([chat.arcee.ai](<https://chat.arcee.ai/>))  
`ARCEE_BASE_URL`| Переопределение базового URL Arcee (по умолчанию: `https://api.arcee.ai/api/v1`)  
`GMI_API_KEY`| API-ключ GMI Cloud ([gmicloud.ai](<https://www.gmicloud.ai/>))  
`GMI_BASE_URL`| Переопределение базового URL GMI Cloud (по умолчанию: `https://api.gmi-serving.com/v1`)  
`MINIMAX_API_KEY`| API-ключ MiniMax — глобальный эндпоинт ([minimax.io](<https://www.minimax.io>)). **Не используется`minimax-oauth`** (OAuth-путь использует вход через браузер).  
`MINIMAX_BASE_URL`| Переопределение базового URL MiniMax (по умолчанию: `https://api.minimax.io/anthropic` — Hermes использует эндпоинт MiniMax, совместимый с Anthropic Messages). **Не используется`minimax-oauth`**.  
`MINIMAX_CN_API_KEY`| API-ключ MiniMax — китайский эндпоинт ([minimaxi.com](<https://www.minimaxi.com>)). **Не используется`minimax-oauth`** (OAuth-путь использует вход через браузер).  
`MINIMAX_CN_BASE_URL`| Переопределение базового URL MiniMax China (по умолчанию: `https://api.minimaxi.com/anthropic`). **Не используется`minimax-oauth`**.  
`KILOCODE_API_KEY`| API-ключ Kilo Code ([kilo.ai](<https://kilo.ai>))  
`KILOCODE_BASE_URL`| Переопределение базового URL Kilo Code (по умолчанию: `https://api.kilo.ai/api/gateway`)  
`XIAOMI_API_KEY`| API-ключ Xiaomi MiMo ([platform.xiaomimimo.com](<https://platform.xiaomimimo.com>))  
`XIAOMI_BASE_URL`| Переопределение базового URL Xiaomi MiMo (по умолчанию: `https://api.xiaomimimo.com/v1`)  
`TOKENHUB_API_KEY`| API-ключ Tencent TokenHub ([tokenhub.tencentmaas.com](<https://tokenhub.tencentmaas.com>))  
`TOKENHUB_BASE_URL`| Переопределение базового URL Tencent TokenHub (по умолчанию: `https://tokenhub.tencentmaas.com/v1`)  
`AZURE_FOUNDRY_API_KEY`| API-ключ Azure AI Foundry / Azure OpenAI ([ai.azure.com](<https://ai.azure.com/>))  
`AZURE_FOUNDRY_BASE_URL`| URL эндпоинта Azure AI Foundry (например, `https://<resource>.openai.azure.com/openai/v1` для OpenAI-стиля или `https://<resource>.services.ai.azure.com/anthropic` для Anthropic-стиля)  
`AZURE_ANTHROPIC_KEY`| API-ключ Azure Anthropic для `provider: anthropic` \\+ `base_url`, указывающего на развёртывание Claude в Azure Foundry (альтернатива `ANTHROPIC_API_KEY`, когда настроены и Anthropic, и Azure Anthropic)  
`HF_TOKEN`| Токен Hugging Face для Inference Providers ([huggingface.co/settings/tokens](<https://huggingface.co/settings/tokens>))  
`HF_BASE_URL`| Переопределение базового URL Hugging Face (по умолчанию: `https://router.huggingface.co/v1`)  
`GOOGLE_API_KEY`| API-ключ Google AI Studio ([aistudio.google.com/app/apikey](<https://aistudio.google.com/app/apikey>))  
`GEMINI_API_KEY`| Псевдоним для `GOOGLE_API_KEY`  
`GEMINI_BASE_URL`| Переопределение базового URL Google AI Studio  
`HERMES_GEMINI_CLIENT_ID`| OAuth client ID для входа `google-gemini-cli` PKCE (опционально; по умолчанию используется публичный gemini-cli клиент Google)  
`HERMES_GEMINI_CLIENT_SECRET`| OAuth client secret для `google-gemini-cli` (опционально)  
`HERMES_GEMINI_PROJECT_ID`| ID проекта GCP для платных тарифов Gemini (бесплатный тариф предоставляется автоматически)  
`ANTHROPIC_API_KEY`| API-ключ Anthropic Console ([console.anthropic.com](<https://console.anthropic.com/>))  
`ANTHROPIC_TOKEN`| Ручное или устаревшее переопределение OAuth/установочного токена Anthropic  
`DASHSCOPE_API_KEY`| API-ключ Alibaba Cloud DashScope для моделей Qwen ([modelstudio.console.alibabacloud.com](<https://modelstudio.console.alibabacloud.com/>))  
`DASHSCOPE_BASE_URL`| Пользовательский базовый URL DashScope (по умолчанию: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`; используйте `https://dashscope.aliyuncs.com/compatible-mode/v1` для материкового Китая)  
`DEEPSEEK_API_KEY`| API-ключ DeepSeek для прямого доступа к DeepSeek ([platform.deepseek.com](<https://platform.deepseek.com/api_keys>))  
`DEEPSEEK_BASE_URL`| Пользовательский базовый URL API DeepSeek  
`NVIDIA_API_KEY`| API-ключ NVIDIA NIM — модели Nemotron и открытые модели ([build.nvidia.com](<https://build.nvidia.com>))  
`NVIDIA_BASE_URL`| Переопределение базового URL NVIDIA (по умолчанию: `https://integrate.api.nvidia.com/v1`; установите `http://localhost:8000/v1` для локального эндпоинта NIM)  
`GMI_API_KEY`| API-ключ GMI Cloud — открытые и reasoning-модели ([inference.gmi.ai](<https://inference.gmi.ai>))  
`GMI_BASE_URL`| Переопределение базового URL GMI Cloud (по умолчанию: `https://api.gmi.ai/v1`)  
`STEPFUN_API_KEY`| API-ключ StepFun — модели серии Step ([platform.stepfun.com](<https://platform.stepfun.com>))  
`STEPFUN_BASE_URL`| Переопределение базового URL StepFun (по умолчанию: `https://api.stepfun.com/v1`)  
`OLLAMA_API_KEY`| API-ключ Ollama Cloud — управляемый каталог Ollama без локального GPU ([ollama.com/settings/keys](<https://ollama.com/settings/keys>))  
`OLLAMA_BASE_URL`| Переопределение базового URL Ollama Cloud (по умолчанию: `https://ollama.com/v1`)  
`XAI_API_KEY`| API-ключ xAI (Grok) для чата и TTS ([console.x.ai](<https://console.x.ai/>))  
`XAI_BASE_URL`| Переопределение базового URL xAI (по умолчанию: `https://api.x.ai/v1`)  
`MISTRAL_API_KEY`| API-ключ Mistral для Voxtral TTS и Voxtral STT ([console.mistral.ai](<https://console.mistral.ai>))  
`AWS_REGION`| Регион AWS для инференса Bedrock (например, `us-east-1`, `eu-central-1`). Читается boto3.  
`AWS_PROFILE`| Именованный профиль AWS для аутентификации Bedrock (читает `~/.aws/credentials`). Оставьте пустым для использования стандартной цепочки учётных данных boto3.  
`BEDROCK_BASE_URL`| Переопределение базового URL Bedrock runtime (по умолчанию: `https://bedrock-runtime.us-east-1.amazonaws.com`; обычно оставляйте пустым и используйте `AWS_REGION`)  
`HERMES_QWEN_BASE_URL`| Переопределение базового URL Qwen Portal (по умолчанию: `https://portal.qwen.ai/v1`)  
`OPENCODE_ZEN_API_KEY`| API-ключ OpenCode Zen — оплата по мере использования для подобранных моделей ([opencode.ai](<https://opencode.ai/auth>))  
`OPENCODE_ZEN_BASE_URL`| Переопределение базового URL OpenCode Zen  
`OPENCODE_GO_API_KEY`| API-ключ OpenCode Go — подписка $10/мес за открытые модели ([opencode.ai](<https://opencode.ai/auth>))  
`OPENCODE_GO_BASE_URL`| Переопределение базового URL OpenCode Go  
`CLAUDE_CODE_OAUTH_TOKEN`| Явное переопределение токена Claude Code, если вы экспортируете его вручную  
`HERMES_MODEL`| Переопределение модели на уровне процесса (используется планировщиком cron; для обычного использования предпочтительнее `config.yaml`)  
`VOICE_TOOLS_OPENAI_KEY`| Предпочтительный ключ OpenAI для провайдеров распознавания речи и синтеза речи OpenAI  
`HERMES_LOCAL_STT_COMMAND`| Опциональный шаблон локальной команды распознавания речи. Поддерживает плейсхолдеры `{input_path}`, `{output_dir}`, `{language}` и `{model}`  
`HERMES_LOCAL_STT_LANGUAGE`| Язык по умолчанию, передаваемый в `HERMES_LOCAL_STT_COMMAND` или в локальный CLI `whisper` (по умолчанию: `en`)  
`HERMES_HOME`| Переопределение директории конфигурации Hermes (по умолчанию: `~/.hermes`). Также определяет область видимости PID-файла шлюза и имени systemd-сервиса, позволяя нескольким установкам работать одновременно  
`HERMES_KANBAN_HOME`| Переопределение общей корневой директории Hermes, которая служит основой для канбан-доски (БД + рабочие области + логи воркеров). По умолчанию используется `get_default_hermes_root()` (родительская директория активного профиля). Полезно для тестов и нестандартных развёртываний  
`HERMES_KANBAN_BOARD`| Фиксация активной канбан-доски для данного процесса. Имеет приоритет над `~/.hermes/kanban/current`; диспетчер внедряет это в окружение подпроцессов воркеров, чтобы воркеры физически не могли видеть задачи с других досок. По умолчанию: `default`. Валидация slug: строчные буквы, цифры, дефисы и подчёркивания, 1–64 символа  
`HERMES_KANBAN_DB`| Прямая фиксация пути к файлу базы данных канбан (наивысший приоритет; переопределяет `HERMES_KANBAN_BOARD` и `HERMES_KANBAN_HOME`). Диспетчер внедряет это в окружение подпроцессов воркеров, чтобы воркеры профиля использовали доску диспетчера  
`HERMES_KANBAN_WORKSPACES_ROOT`| Прямая фиксация корня рабочих областей канбан (наивысший приоритет для рабочих областей; переопределяет `HERMES_KANBAN_HOME`). Диспетчер внедряет это в окружение подпроцессов воркеров  
## Аутентификация провайдеров (OAuth)[​](<#provider-auth-oauth> "Direct link to Provider Auth \\(OAuth\\)")
Для нативной аутентификации Anthropic Hermes предпочитает собственные файлы учётных данных Claude Code, когда они существуют, поскольку эти учётные данные могут обновляться автоматически. **OAuth через Anthropic требует плана Claude Max с приобретёнными дополнительными кредитами** — Hermes маршрутизируется как Claude Code, который использует только дополнительные кредиты плана Max, а не базовый лимит Max, и не работает с Claude Pro. Без Max + дополнительных кредитов используйте API-ключ. Переменные окружения, такие как `ANTHROPIC_TOKEN`, остаются полезными для ручного переопределения, но больше не являются предпочтительным способом для входа в Claude Max.
Переменная| Описание  
---|---  
`HERMES_INFERENCE_PROVIDER`| Переопределение выбора провайдера: `auto`, `custom`, `openrouter`, `nous`, `openai-codex`, `copilot`, `copilot-acp`, `anthropic`, `huggingface`, `gemini`, `zai`, `kimi-coding`, `kimi-coding-cn`, `minimax`, `minimax-cn`, `minimax-oauth` (вход через браузер OAuth — API-ключ не требуется; см. [MiniMax OAuth guide](</docs/guides/minimax-oauth>)), `kilocode`, `xiaomi`, `arcee`, `gmi`, `stepfun`, `alibaba`, `alibaba-coding-plan` (псевдоним `alibaba_coding`), `deepseek`, `nvidia`, `ollama-cloud`, `xai` (псевдоним `grok`), `google-gemini-cli`, `qwen-oauth`, `bedrock`, `opencode-zen`, `opencode-go`, `ai-gateway`, `tencent-tokenhub` (по умолчанию: `auto`)  
`HERMES_PORTAL_BASE_URL`| Переопределение URL Nous Portal (для разработки/тестирования)  
`NOUS_INFERENCE_BASE_URL`| Переопределение URL API инференса Nous  
`HERMES_NOUS_MIN_KEY_TTL_SECONDS`| Минимальное время жизни ключа агента до перевыпуска (по умолчанию: 1800 = 30 мин)  
`HERMES_NOUS_TIMEOUT_SECONDS`| Тайм-аут HTTP для потоков учётных данных / токенов Nous  
`HERMES_DUMP_REQUESTS`| Сохранять полезную нагрузку API-запросов в лог-файлы (`true`/`false`)  
`HERMES_PREFILL_MESSAGES_FILE`| Путь к JSON-файлу с эфемерными prefill-сообщениями, внедряемыми при вызове API  
`HERMES_TIMEZONE`| Переопределение часового пояса IANA (например, `America/New_York`)  
## Tool API[​](<#tool-apis> "Direct link to Tool APIs")
Переменная| Описание  
---|---  
`PARALLEL_API_KEY`| ИИ-нативный веб-поиск ([parallel.ai](<https://parallel.ai/>))  
`FIRECRAWL_API_KEY`| Веб-скрапинг и облачный браузер ([firecrawl.dev](<https://firecrawl.dev/>))  
`FIRECRAWL_API_URL`| Пользовательский эндпоинт Firecrawl API для самостоятельных инстансов (опционально)  
`TAVILY_API_KEY`| API-ключ Tavily для ИИ-нативного веб-поиска, извлечения и краулинга ([app.tavily.com](<https://app.tavily.com/home>))  
`SEARXNG_URL`| URL инстанса SearXNG для бесплатного самостоятельного веб-поиска — API-ключ не требуется ([searxng.github.io](<https://searxng.github.io/searxng/>))  
`TAVILY_BASE_URL`| Переопределение эндпоинта API Tavily. Полезно для корпоративных прокси и самостоятельных серверов поиска, совместимых с Tavily. Аналогично `GROQ_BASE_URL`.  
`EXA_API_KEY`| API-ключ Exa для ИИ-нативного веб-поиска и контента ([exa.ai](<https://exa.ai/>))  
`BROWSERBASE_API_KEY`| Автоматизация браузера ([browserbase.com](<https://browserbase.com/>))  
`BROWSERBASE_PROJECT_ID`| ID проекта Browserbase  
`BROWSER_USE_API_KEY`| API-ключ облачного браузера Browser Use ([browser-use.com](<https://browser-use.com/>))  
`FIRECRAWL_BROWSER_TTL`| Время жизни сессии браузера Firecrawl в секундах (по умолчанию: 300)  
`BROWSER_CDP_URL`| URL Chrome DevTools Protocol для локального браузера (устанавливается через `/browser connect`, например `ws://localhost:9222`)  
`CAMOFOX_URL`| URL локального браузера Camofox для антидетекта (по умолчанию: `http://localhost:9377`)  
`BROWSER_INACTIVITY_TIMEOUT`| Тайм-аут неактивности сессии браузера в секундах  
`FAL_KEY`| Генерация изображений ([fal.ai](<https://fal.ai/>))  
`GROQ_API_KEY`| API-ключ Groq Whisper STT ([groq.com](<https://groq.com/>))  
`ELEVENLABS_API_KEY`| Премиум-голоса TTS от ElevenLabs ([elevenlabs.io](<https://elevenlabs.io/>))  
`STT_GROQ_MODEL`| Переопределение модели Groq STT (по умолчанию: `whisper-large-v3-turbo`)  
`GROQ_BASE_URL`| Переопределение эндпоинта STT Groq, совместимого с OpenAI  
`STT_OPENAI_MODEL`| Переопределение модели OpenAI STT (по умолчанию: `whisper-1`)  
`STT_OPENAI_BASE_URL`| Переопределение эндпоинта STT, совместимого с OpenAI  
`GITHUB_TOKEN`| GitHub-токен для Skills Hub (более высокие лимиты API, публикация навыков)  
`HONCHO_API_KEY`| Кросс-сессионное моделирование пользователей ([honcho.dev](<https://honcho.dev/>))  
`HONCHO_BASE_URL`| Базовый URL для самостоятельных инстансов Honcho (по умолчанию: Honcho cloud). Для локальных инстансов API-ключ не требуется  
`HINDSIGHT_TIMEOUT`| Тайм-аут в секундах для вызовов API памяти Hindsight (по умолчанию: `60`). Увеличьте, если ваш инстанс Hindsight медленно отвечает во время `/sync` или `on_session_switch` и вы видите тайм-ауты в `errors.log`.  
`SUPERMEMORY_API_KEY`| Семантическая долговременная память с извлечением профиля и приёмом сессий ([supermemory.ai](<https://supermemory.ai>))  
`TINKER_API_KEY`| RL-тренировки ([tinker-console.thinkingmachines.ai](<https://tinker-console.thinkingmachines.ai/>))  
`WANDB_API_KEY`| Метрики RL-тренировок ([wandb.ai](<https://wandb.ai/>))  
`DAYTONA_API_KEY`| Облачные песочницы Daytona ([daytona.io](<https://daytona.io/>))  
`VERCEL_TOKEN`| Токен доступа к Vercel Sandbox ([vercel.com](<https://vercel.com/>))  
`VERCEL_PROJECT_ID`| ID проекта Vercel (требуется с `VERCEL_TOKEN`)  
`VERCEL_TEAM_ID`| ID команды Vercel (требуется с `VERCEL_TOKEN`)  
`VERCEL_OIDC_TOKEN`| Кратковременный OIDC-токен Vercel (альтернатива для разработки)  
### Langfuse Observability[​](<#langfuse-observability> "Direct link to Langfuse Observability")
Переменные окружения для встроенного плагина [`observability/langfuse`](</docs/user-guide/features/built-in-plugins#observabilitylangfuse>). Установите их через `hermes tools → Langfuse Observability` или вручную в `~/.hermes/.env`. Плагин также должен быть включён (`hermes plugins enable observability/langfuse`), прежде чем они начнут действовать.
Переменная| Описание  
---|---  
`HERMES_LANGFUSE_PUBLIC_KEY`| Публичный ключ проекта Langfuse (`pk-lf-...`). Обязателен.  
`HERMES_LANGFUSE_SECRET_KEY`| Секретный ключ проекта Langfuse (`sk-lf-...`). Обязателен.  
`HERMES_LANGFUSE_BASE_URL`| URL сервера Langfuse (по умолчанию: `https://cloud.langfuse.com`). Задаётся для самостоятельного размещения.  
`HERMES_LANGFUSE_ENV`| Тег окружения на трассах (`production`, `staging`, …)  
`HERMES_LANGFUSE_RELEASE`| Тег релиза/версии на трассах  
`HERMES_LANGFUSE_SAMPLE_RATE`| Коэффициент выборки SDK 0.0–1.0 (по умолчанию: `1.0`)  
`HERMES_LANGFUSE_MAX_CHARS`| Усечение полей для сериализованных полезных нагрузок (по умолчанию: `12000`)  
`HERMES_LANGFUSE_DEBUG`| `true` включает подробное логирование плагина в `agent.log`  
`LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_BASE_URL`| Стандартные имена SDK Langfuse. Принимаются как запасные, когда `HERMES_LANGFUSE_*` аналоги не заданы.  
### Nous Tool Gateway[​](<#nous-tool-gateway> "Direct link to Nous Tool Gateway")
Эти переменные настраивают [Tool Gateway](</docs/user-guide/features/tool-gateway>) для платных подписчиков Nous или самостоятельных развёртываний шлюза. Большинству пользователей не нужно их задавать — шлюз настраивается автоматически через `hermes model` или `hermes tools`.
Переменная| Описание  
---|---  
`TOOL_GATEWAY_DOMAIN`| Базовый домен для маршрутизации Tool Gateway (по умолчанию: `nousresearch.com`)  
`TOOL_GATEWAY_SCHEME`| Схема HTTP или HTTPS для URL шлюза (по умолчанию: `https`)  
`TOOL_GATEWAY_USER_TOKEN`| Токен аутентификации для Tool Gateway (обычно заполняется автоматически из аутентификации Nous)  
`FIRECRAWL_GATEWAY_URL`| Переопределение URL эндпоинта шлюза Firecrawl  
## Терминальный бэкенд[​](<#terminal-backend> "Direct link to Terminal Backend")
Переменная| Описание  
---|---  
`TERMINAL_ENV`| Бэкенд: `local`, `docker`, `ssh`, `singularity`, `modal`, `daytona`, `vercel_sandbox`  
`HERMES_DOCKER_BINARY`| Переопределение бинарника контейнера, который вызывает Hermes (например, `podman`, `/usr/local/bin/docker`). Если не задано, Hermes автоматически находит `docker` или `podman` в `PATH`. Требуется, когда установлены оба и вы хотите использовать нестандартный, или когда бинарник находится вне `PATH`.  
`TERMINAL_DOCKER_IMAGE`| Docker-образ (по умолчанию: `nikolaik/python-nodejs:python3.11-nodejs20`)  
`TERMINAL_DOCKER_FORWARD_ENV`| JSON-массив имён переменных окружения для явной передачи в Docker-сессии терминала. Примечание: объявленные навыком `required_environment_variables` передаются автоматически — это нужно только для переменных, не объявленных ни одним навыком.  
`TERMINAL_DOCKER_VOLUMES`| Дополнительные монтирования томов Docker (пары `host:container` через запятую)  
`TERMINAL_DOCKER_MOUNT_CWD_TO_WORKSPACE`| Расширенный opt-in: монтировать текущую рабочую директорию запуска в Docker `/workspace` (`true`/`false`, по умолчанию: `false`)  
`TERMINAL_SINGULARITY_IMAGE`| Singularity-образ или путь `.sif`  
`TERMINAL_MODAL_IMAGE`| Образ контейнера Modal  
`TERMINAL_DAYTONA_IMAGE`| Образ песочницы Daytona  
`TERMINAL_VERCEL_RUNTIME`| Среда выполнения Vercel Sandbox (`node24`, `node22`, `python3.13`)  
`TERMINAL_TIMEOUT`| Тайм-аут команды в секундах  
`TERMINAL_LIFETIME_SECONDS`| Максимальное время жизни сессий терминала в секундах  
`TERMINAL_CWD`| Рабочая директория для сессий терминала (только шлюз/cron; CLI использует директорию запуска)  
`SUDO_PASSWORD`| Включение sudo без интерактивного запроса  
Для облачных бэкендов-песочниц сохраняемость ориентирована на файловую систему. `TERMINAL_LIFETIME_SECONDS` определяет, когда Hermes очищает бездействующую сессию терминала, и при последующем возобновлении песочница может быть создана заново, а не поддерживать те же активные процессы.
## SSH-бэкенд[​](<#ssh-backend> "Direct link to SSH Backend")
Переменная| Описание  
---|---  
`TERMINAL_SSH_HOST`| Имя хоста удалённого сервера  
`TERMINAL_SSH_USER`| Имя пользователя SSH  
`TERMINAL_SSH_PORT`| Порт SSH (по умолчанию: 22)  
`TERMINAL_SSH_KEY`| Путь к приватному ключу  
`TERMINAL_SSH_PERSISTENT`| Переопределение постоянной оболочки для SSH (по умолчанию: следует за `TERMINAL_PERSISTENT_SHELL`)  
## Ресурсы контейнеров (Docker, Singularity, Modal, Daytona)[​](<#container-resources-docker-singularity-modal-daytona> "Direct link to Container Resources \\(Docker, Singularity, Modal, Daytona\\)")
Переменная| Описание  
---|---  
`TERMINAL_CONTAINER_CPU`| Ядра CPU (по умолчанию: 1)  
`TERMINAL_CONTAINER_MEMORY`| Память в МБ (по умолчанию: 5120)  
`TERMINAL_CONTAINER_DISK`| Диск в МБ (по умолчанию: 51200)  
`TERMINAL_CONTAINER_PERSISTENT`| Сохранять файловую систему контейнера между сессиями (по умолчанию: `true`)  
`TERMINAL_SANDBOX_DIR`| Хостовая директория для рабочих областей и оверлеев (по умолчанию: `~/.hermes/sandboxes/`)  
## Постоянная оболочка[​](<#persistent-shell> "Direct link to Persistent Shell")
Переменная| Описание  
---|---  
`TERMINAL_PERSISTENT_SHELL`| Включить постоянную оболочку для нелокальных бэкендов (по умолчанию: `true`). Также настраивается через `terminal.persistent_shell` в config.yaml  
`TERMINAL_LOCAL_PERSISTENT`| Включить постоянную оболочку для локального бэкенда (по умолчанию: `false`)  
`TERMINAL_SSH_PERSISTENT`| Переопределение постоянной оболочки для SSH-бэкенда (по умолчанию: следует за `TERMINAL_PERSISTENT_SHELL`)  
## Мессенджеры[​](<#messaging> "Direct link to Messaging")
Переменная| Описание  
---|---  
`TELEGRAM_BOT_TOKEN`| Токен Telegram-бота (от @BotFather)  
`TELEGRAM_ALLOWED_USERS`| ID пользователей (через запятую), которым разрешено использовать бота (применяется к личным сообщениям, группам и форумам)  
`TELEGRAM_GROUP_ALLOWED_USERS`| ID отправителей (через запятую), авторизованных только в группах/форумах (НЕ предоставляет доступ к ЛС). Значения в формате Chat-ID (начинающиеся с `-`) всё ещё воспринимаются как ID чатов для обратной совместимости с конфигами до #17686, с предупреждением об устаревании.  
`TELEGRAM_GROUP_ALLOWED_CHATS`| ID групповых чатов/форумов (через запятую); любой участник авторизован  
`TELEGRAM_HOME_CHANNEL`| Канал/чат Telegram по умолчанию для доставки cron  
`TELEGRAM_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала Telegram  
`TELEGRAM_WEBHOOK_URL`| Публичный HTTPS URL для режима вебхука (включает вебхук вместо polling)  
`TELEGRAM_WEBHOOK_PORT`| Локальный порт прослушивания для сервера вебхука (по умолчанию: `8443`)  
`TELEGRAM_WEBHOOK_SECRET`| Секретный токен, который Telegram отправляет обратно в каждом обновлении для проверки. **Обязателен, когда задан`TELEGRAM_WEBHOOK_URL`** — шлюз откажется запускаться без него (GHSA-3vpc-7q5r-276h). Сгенерируйте с помощью `openssl rand -hex 32`.  
`TELEGRAM_REACTIONS`| Включить emoji-реакции на сообщения во время обработки (по умолчанию: `false`)  
`TELEGRAM_REPLY_TO_MODE`| Поведение ответа-ссылки: `off`, `first` (по умолчанию) или `all`. Соответствует шаблону Discord.  
`TELEGRAM_IGNORED_THREADS`| ID тем/тредов форума Telegram (через запятую), в которых бот никогда не отвечает  
`TELEGRAM_PROXY`| URL прокси для подключений Telegram — переопределяет `HTTPS_PROXY`. Поддерживает `http://`, `https://`, `socks5://`  
`DISCORD_BOT_TOKEN`| Токен Discord-бота  
`DISCORD_ALLOWED_USERS`| ID пользователей Discord (через запятую), которым разрешено использовать бота  
`DISCORD_ALLOWED_ROLES`| ID ролей Discord (через запятую), которым разрешено использовать бота (логическое ИЛИ с `DISCORD_ALLOWED_USERS`). Автоматически включает Members intent. Полезно при текучке модераторов — разрешения ролей применяются автоматически.  
`DISCORD_ALLOWED_CHANNELS`| ID каналов Discord (через запятую). Если задано, бот отвечает только в этих каналах (плюс ЛС, если разрешено). Переопределяет `config.yaml` `discord.allowed_channels`.  
`DISCORD_PROXY`| URL прокси для подключений Discord — переопределяет `HTTPS_PROXY`. Поддерживает `http://`, `https://`, `socks5://`  
`DISCORD_HOME_CHANNEL`| Канал Discord по умолчанию для доставки cron  
`DISCORD_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала Discord  
`DISCORD_COMMAND_SYNC_POLICY`| Политика синхронизации слеш-команд Discord при запуске: `safe` (diff и согласование), `bulk` (устаревший `tree.sync()`) или `off`  
`DISCORD_REQUIRE_MENTION`| Требовать @упоминание перед ответом в серверных каналах  
`DISCORD_FREE_RESPONSE_CHANNELS`| ID каналов (через запятую), где упоминание не требуется  
`DISCORD_AUTO_THREAD`| Автоматически создавать тред для длинных ответов, где поддерживается  
`DISCORD_REACTIONS`| Включить emoji-реакции на сообщения во время обработки (по умолчанию: `true`)  
`DISCORD_IGNORED_CHANNELS`| ID каналов (через запятую), где бот никогда не отвечает  
`DISCORD_NO_THREAD_CHANNELS`| ID каналов (через запятую), где бот отвечает без автоматического создания тредов  
`DISCORD_REPLY_TO_MODE`| Поведение ответа-ссылки: `off`, `first` (по умолчанию) или `all`  
`DISCORD_ALLOW_MENTION_EVERYONE`| Разрешить боту упоминать `@everyone`/`@here` (по умолчанию: `false`). См. [Mention Control](</docs/user-guide/messaging/discord#mention-control>).  
`DISCORD_ALLOW_MENTION_ROLES`| Разрешить боту упоминать `@role` (по умолчанию: `false`).  
`DISCORD_ALLOW_MENTION_USERS`| Разрешить боту упоминать отдельных `@user` (по умолчанию: `true`).  
`DISCORD_ALLOW_MENTION_REPLIED_USER`| Упоминать автора при ответе на его сообщение (по умолчанию: `true`).  
`SLACK_BOT_TOKEN`| Токен Slack-бота (`xoxb-...`)  
`SLACK_APP_TOKEN`| Токен приложения Slack (`xapp-...`, требуется для Socket Mode)  
`SLACK_ALLOWED_USERS`| ID пользователей Slack (через запятую)  
`SLACK_HOME_CHANNEL`| Канал Slack по умолчанию для доставки cron  
`SLACK_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала Slack  
`WHATSAPP_ENABLED`| Включить мост WhatsApp (`true`/`false`)  
`WHATSAPP_MODE`| `bot` (отдельный номер) или `self-chat` (написать себе)  
`WHATSAPP_ALLOWED_USERS`| Номера телефонов (через запятую, с кодом страны, без `+`), или `*` для разрешения всем отправителям  
`WHATSAPP_ALLOW_ALL_USERS`| Разрешить всем отправителям WhatsApp без белого списка (`true`/`false`)  
`WHATSAPP_DEBUG`| Логировать сырые события сообщений в мосте для отладки (`true`/`false`)  
`SIGNAL_HTTP_URL`| HTTP-эндпоинт демона signal-cli (например, `http://127.0.0.1:8080`)  
`SIGNAL_ACCOUNT`| Номер телефона бота в формате E.164  
`SIGNAL_ALLOWED_USERS`| Номера телефонов E.164 или UUID (через запятую)  
`SIGNAL_GROUP_ALLOWED_USERS`| ID групп (через запятую) или `*` для всех групп  
`SIGNAL_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала Signal  
`SIGNAL_IGNORE_STORIES`| Игнорировать истории/статусы Signal  
`SIGNAL_ALLOW_ALL_USERS`| Разрешить всем пользователям Signal без белого списка  
`TWILIO_ACCOUNT_SID`| SID аккаунта Twilio (общий с навыком телефонии)  
`TWILIO_AUTH_TOKEN`| Auth Token Twilio (общий с навыком телефонии; также используется для проверки подписи вебхука)  
`TWILIO_PHONE_NUMBER`| Номер телефона Twilio в формате E.164 (общий с навыком телефонии)  
`SMS_WEBHOOK_URL`| Публичный URL для проверки подписи Twilio — должен совпадать с URL вебхука в консоли Twilio (обязательно)  
`SMS_WEBHOOK_PORT`| Порт прослушивания вебхука для входящих SMS (по умолчанию: `8080`)  
`SMS_WEBHOOK_HOST`| Адрес привязки вебхука (по умолчанию: `0.0.0.0`)  
`SMS_INSECURE_NO_SIGNATURE`| Установите `true` для отключения проверки подписи Twilio (только для локальной разработки — не для продакшена)  
`SMS_ALLOWED_USERS`| Номера телефонов E.164 (через запятую), которым разрешено общаться  
`SMS_ALLOW_ALL_USERS`| Разрешить всем отправителям SMS без белого списка  
`SMS_HOME_CHANNEL`| Номер телефона для доставки задач cron/уведомлений  
`SMS_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала SMS  
`EMAIL_ADDRESS`| Адрес электронной почты для адаптера шлюза Email  
`EMAIL_PASSWORD`| Пароль или пароль приложения для учётной записи email  
`EMAIL_IMAP_HOST`| IMAP-хост для адаптера email  
`EMAIL_IMAP_PORT`| Порт IMAP  
`EMAIL_SMTP_HOST`| SMTP-хост для адаптера email  
`EMAIL_SMTP_PORT`| Порт SMTP  
`EMAIL_ALLOWED_USERS`| Адреса email (через запятую), которым разрешено писать боту  
`EMAIL_HOME_ADDRESS`| Получатель по умолчанию для проактивной доставки email  
`EMAIL_HOME_ADDRESS_NAME`| Отображаемое имя для домашнего адреса email  
`EMAIL_POLL_INTERVAL`| Интервал опроса email в секундах  
`EMAIL_ALLOW_ALL_USERS`| Разрешить всех входящих отправителей email  
`DINGTALK_CLIENT_ID`| AppKey бота DingTalk из портала разработчика ([open.dingtalk.com](<https://open.dingtalk.com>))  
`DINGTALK_CLIENT_SECRET`| AppSecret бота DingTalk из портала разработчика  
`DINGTALK_ALLOWED_USERS`| ID пользователей DingTalk (через запятую), которым разрешено писать боту  
`FEISHU_APP_ID`| App ID бота Feishu/Lark из [open.feishu.cn](<https://open.feishu.cn/>)  
`FEISHU_APP_SECRET`| App Secret бота Feishu/Lark  
`FEISHU_DOMAIN`| `feishu` (Китай) или `lark` (международный). По умолчанию: `feishu`  
`FEISHU_CONNECTION_MODE`| `websocket` (рекомендуется) или `webhook`. По умолчанию: `websocket`  
`FEISHU_ENCRYPT_KEY`| Опциональный ключ шифрования для режима вебхука  
`FEISHU_VERIFICATION_TOKEN`| Опциональный токен проверки для режима вебхука  
`FEISHU_ALLOWED_USERS`| ID пользователей Feishu (через запятую), которым разрешено писать боту  
`FEISHU_ALLOW_BOTS`| `none` (по умолчанию) / `mentions` / `all` — принимать входящие сообщения от других ботов. См. [bot-to-bot messaging](</docs/user-guide/messaging/feishu#bot-to-bot-messaging>)  
`FEISHU_REQUIRE_MENTION`| `true` (по умолчанию) / `false` — требуется ли @упоминание бота в групповых сообщениях. Переопределяется для каждого чата через `group_rules.<chat_id>.require_mention`.  
`FEISHU_HOME_CHANNEL`| ID чата Feishu для доставки cron и уведомлений  
`WECOM_BOT_ID`| ID AI-бота WeCom из консоли администратора  
`WECOM_SECRET`| Секрет AI-бота WeCom  
`WECOM_WEBSOCKET_URL`| Пользовательский URL WebSocket (по умолчанию: `wss://openws.work.weixin.qq.com`)  
`WECOM_ALLOWED_USERS`| ID пользователей WeCom (через запятую), которым разрешено писать боту  
`WECOM_HOME_CHANNEL`| ID чата WeCom для доставки cron и уведомлений  
`WECOM_CALLBACK_CORP_ID`| Corp ID предприятия WeCom для callback-приложения  
`WECOM_CALLBACK_CORP_SECRET`| Corp secret для callback-приложения  
`WECOM_CALLBACK_AGENT_ID`| Agent ID callback-приложения  
`WECOM_CALLBACK_TOKEN`| Токен проверки callback  
`WECOM_CALLBACK_ENCODING_AES_KEY`| AES-ключ для шифрования callback  
`WECOM_CALLBACK_HOST`| Адрес привязки сервера callback (по умолчанию: `0.0.0.0`)  
`WECOM_CALLBACK_PORT`| Порт сервера callback (по умолчанию: `8645`)  
`WECOM_CALLBACK_ALLOWED_USERS`| ID пользователей (через запятую) для белого списка  
`WECOM_CALLBACK_ALLOW_ALL_USERS`| Установите `true`, чтобы разрешить всех пользователей без белого списка  
`WEIXIN_ACCOUNT_ID`| ID учётной записи Weixin, полученный через QR-вход через API iLink Bot  
`WEIXIN_TOKEN`| Токен аутентификации Weixin, полученный через QR-вход через API iLink Bot  
`WEIXIN_BASE_URL`| Переопределение базового URL API iLink Bot Weixin (по умолчанию: `https://ilinkai.weixin.qq.com`)  
`WEIXIN_CDN_BASE_URL`| Переопределение базового URL CDN Weixin для медиа (по умолчанию: `https://novac2c.cdn.weixin.qq.com/c2c`)  
`WEIXIN_DM_POLICY`| Политика личных сообщений: `open`, `allowlist`, `pairing`, `disabled` (по умолчанию: `open`)  
`WEIXIN_GROUP_POLICY`| Политика групповых сообщений: `open`, `allowlist`, `disabled` (по умолчанию: `disabled`)  
`WEIXIN_ALLOWED_USERS`| ID пользователей Weixin (через запятую), которым разрешено писать боту в ЛС  
`WEIXIN_GROUP_ALLOWED_USERS`| ID **групповых чатов** Weixin (через запятую, не ID участников), которым разрешено взаимодействовать с ботом. Название переменной устаревшее — ожидаются ID групп. Работает только когда iLink действительно доставляет групповые события; QR-логин iLink-боты (`...@im.bot`) обычно не получают обычные групповые сообщения WeChat.  
`WEIXIN_HOME_CHANNEL`| ID чата Weixin для доставки cron и уведомлений  
`WEIXIN_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала Weixin  
`WEIXIN_ALLOW_ALL_USERS`| Разрешить всех пользователей Weixin без белого списка (`true`/`false`)  
`BLUEBUBBLES_SERVER_URL`| URL сервера BlueBubbles (например, `http://192.168.1.10:1234`)  
`BLUEBUBBLES_PASSWORD`| Пароль сервера BlueBubbles  
`BLUEBUBBLES_WEBHOOK_HOST`| Адрес привязки прослушивателя вебхука (по умолчанию: `127.0.0.1`)  
`BLUEBUBBLES_WEBHOOK_PORT`| Порт прослушивателя вебхука (по умолчанию: `8645`)  
`BLUEBUBBLES_HOME_CHANNEL`| Телефон/email для доставки cron/уведомлений  
`BLUEBUBBLES_ALLOWED_USERS`| Авторизованные пользователи (через запятую)  
`BLUEBUBBLES_ALLOW_ALL_USERS`| Разрешить всех пользователей (`true`/`false`)  
`QQ_APP_ID`| App ID QQ-бота из [q.qq.com](<https://q.qq.com>)  
`QQ_CLIENT_SECRET`| App Secret QQ-бота из [q.qq.com](<https://q.qq.com>)  
`QQ_STT_API_KEY`| API-ключ для внешнего запасного STT-провайдера (опционально, используется когда встроенный ASR QQ не возвращает текст)  
`QQ_STT_BASE_URL`| Базовый URL для внешнего STT-провайдера (опционально)  
`QQ_STT_MODEL`| Имя модели для внешнего STT-провайдера (опционально)  
`QQ_ALLOWED_USERS`| openID пользователей QQ (через запятую), которым разрешено писать боту  
`QQ_GROUP_ALLOWED_USERS`| ID групп QQ (через запятую) для доступа к @-сообщениям в группах  
`QQ_ALLOW_ALL_USERS`| Разрешить всех пользователей (`true`/`false`, переопределяет `QQ_ALLOWED_USERS`)  
`QQBOT_HOME_CHANNEL`| openID пользователя/группы QQ для доставки cron и уведомлений  
`QQBOT_HOME_CHANNEL_NAME`| Отображаемое имя для домашнего канала QQ  
`QQ_PORTAL_HOST`| Переопределение хоста портала QQ (установите `sandbox.q.qq.com` для маршрутизации через песочницу; по умолчанию: `q.qq.com`).  
`MATTERMOST_URL`| URL сервера Mattermost (например, `https://mm.example.com`)  
`MATTERMOST_TOKEN`| Токен бота или персональный токен доступа для Mattermost  
`MATTERMOST_ALLOWED_USERS`| ID пользователей Mattermost (через запятую), которым разрешено писать боту  
`MATTERMOST_HOME_CHANNEL`| ID канала для проактивной доставки сообщений (cron, уведомления)  
`MATTERMOST_REQUIRE_MENTION`| Требовать `@упоминание` в каналах (по умолчанию: `true`). Установите `false` для ответа на все сообщения.  
`MATTERMOST_FREE_RESPONSE_CHANNELS`| ID каналов (через запятую), где бот отвечает без `@упоминания`  
`MATTERMOST_REPLY_MODE`| Стиль ответа: `thread` (ответы в тредах) или `off` (плоские сообщения, по умолчанию)  
`MATRIX_HOMESERVER`| URL homeserver Matrix (например, `https://matrix.org`)  
`MATRIX_ACCESS_TOKEN`| Токен доступа Matrix для аутентификации бота  
`MATRIX_USER_ID`| ID пользователя Matrix (например, `@hermes:matrix.org`) — требуется для входа по паролю, опционально с токеном доступа  
`MATRIX_PASSWORD`| Пароль Matrix (альтернатива токену доступа)  
`MATRIX_ALLOWED_USERS`| ID пользователей Matrix (через запятую), которым разрешено писать боту (например, `@alice:matrix.org`)  
`MATRIX_HOME_ROOM`| ID комнаты для проактивной доставки сообщений (например, `!abc123:matrix.org`)  
`MATRIX_ENCRYPTION`| Включить сквозное шифрование (`true`/`false`, по умолчанию: `false`)  
`MATRIX_DEVICE_ID`| Стабильный ID устройства Matrix для сохранения E2EE между перезапусками (например, `HERMES_BOT`). Без этого ключи E2EE меняются при каждом запуске, и расшифровка исторических комнат нарушается.  
`MATRIX_REACTIONS`| Включить emoji-реакции жизненного цикла обработки на входящие сообщения (по умолчанию: `true`). Установите `false` для отключения.  
`MATRIX_REQUIRE_MENTION`| Требовать `@упоминание` в комнатах (по умолчанию: `true`). Установите `false` для ответа на все сообщения.  
`MATRIX_FREE_RESPONSE_ROOMS`| ID комнат (через запятую), где бот отвечает без `@упоминания`  
`MATRIX_AUTO_THREAD`| Автоматически создавать треды для сообщений в комнатах (по умолчанию: `true`)  
`MATRIX_DM_MENTION_THREADS`| Создавать тред, когда бота `@упоминают` в ЛС (по умолчанию: `false`)  
`MATRIX_RECOVERY_KEY`| Ключ восстановления для проверки кросс-подписи после ротации ключей устройства. Рекомендуется для E2EE-конфигураций с включённой кросс-подписью.  
`HASS_TOKEN`| Long-Lived Access Token Home Assistant (включает платформу HA + инструменты)  
`HASS_URL`| URL Home Assistant (по умолчанию: `http://homeassistant.local:8123`)  
`WEBHOOK_ENABLED`| Включить адаптер платформы вебхука (`true`/`false`)  
`WEBHOOK_PORT`| Порт HTTP-сервера для приёма вебхуков (по умолчанию: `8644`)  
`WEBHOOK_SECRET`| Глобальный HMAC-секрет для проверки подписи вебхуков (используется как запасной, когда маршруты не задают свой собственный)  
`API_SERVER_ENABLED`| Включить API-сервер, совместимый с OpenAI (`true`/`false`). Работает параллельно с другими платформами.  
`API_SERVER_KEY`| Bearer-токен для аутентификации API-сервера. Обязателен для привязки не к loopback.  
`API_SERVER_CORS_ORIGINS`| Источники браузера (через запятую), которым разрешено вызывать API-сервер напрямую (например, `http://localhost:3000,http://127.0.0.1:3000`). По умолчанию: отключено.  
`API_SERVER_PORT`| Порт API-сервера (по умолчанию: `8642`)  
`API_SERVER_HOST`| Хост/адрес привязки API-сервера (по умолчанию: `127.0.0.1`). Используйте `0.0.0.0` для сетевого доступа — требуется `API_SERVER_KEY` и узкий белый список `API_SERVER_CORS_ORIGINS`.  
`API_SERVER_MODEL_NAME`| Имя модели, объявляемое на `/v1/models`. По умолчанию равно имени профиля (или `hermes-agent` для профиля по умолчанию). Полезно для многопользовательских конфигураций, где интерфейсы вроде Open WebUI требуют разные имена моделей для каждого подключения.  
`GATEWAY_PROXY_URL`| URL удалённого API-сервера Hermes для пересылки сообщений ([режим прокси](</docs/user-guide/messaging/matrix#proxy-mode-e2ee-on-macos>)). Когда задан, шлюз обрабатывает только ввод/вывод платформы — вся работа агента делегируется удалённому серверу. Также настраивается через `gateway.proxy_url` в `config.yaml`.  
`GATEWAY_PROXY_KEY`| Bearer-токен для аутентификации на удалённом API-сервере в режиме прокси. Должен совпадать с `API_SERVER_KEY` на удалённом хосте.  
`MESSAGING_CWD`| Рабочая директория для терминальных команд в режиме мессенджеров (по умолчанию: `~`)  
`GATEWAY_ALLOWED_USERS`| ID пользователей (через запятую), которым разрешено использование на всех платформах  
`GATEWAY_ALLOW_ALL_USERS`| Разрешить всех пользователей без белых списков (`true`/`false`, по умолчанию: `false`)  
### Продвинутая настройка мессенджеров[​](<#advanced-messaging-tuning> "Direct link to Advanced Messaging Tuning")
Продвинутые per-платформенные рычаги для регулировки пакетного отправителя исходящих сообщений. Большинству пользователей никогда не нужно их трогать; значения по умолчанию настроены так, чтобы соблюдать лимиты каждой платформы без ощущения задержек.
Переменная| Описание  
---|---  
`HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS`| Окно ожидания перед отправкой накопленного фрагмента текста Telegram (по умолчанию: `0.6`).  
`HERMES_TELEGRAM_TEXT_BATCH_SPLIT_DELAY_SECONDS`| Задержка между разделёнными фрагментами, когда одно сообщение Telegram превышает лимит длины (по умолчанию: `2.0`).  
`HERMES_TELEGRAM_MEDIA_BATCH_DELAY_SECONDS`| Окно ожидания перед отправкой накопленных медиа Telegram (по умолчанию: `0.6`).  
`HERMES_TELEGRAM_FOLLOWUP_GRACE_SECONDS`| Задержка перед отправкой дополнительного сообщения после завершения работы агента, чтобы избежать гонки с последним фрагментом стрима.  
`HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT` / `_READ_TIMEOUT` / `_WRITE_TIMEOUT` / `_POOL_TIMEOUT`| Переопределение тайм-аутов HTTP базовой библиотеки `python-telegram-bot` (секунды).  
`HERMES_TELEGRAM_HTTP_POOL_SIZE`| Максимальное количество одновременных HTTP-соединений с API Telegram.  
`HERMES_TELEGRAM_DISABLE_FALLBACK_IPS`| Отключить жёстко заданные запасные IP Cloudflare, используемые при сбое DNS (`true`/`false`).  
`HERMES_DISCORD_TEXT_BATCH_DELAY_SECONDS`| Окно ожидания перед отправкой накопленного фрагмента текста Discord (по умолчанию: `0.6`).  
`HERMES_DISCORD_TEXT_BATCH_SPLIT_DELAY_SECONDS`| Задержка между разделёнными фрагментами, когда сообщение Discord превышает лимит длины (по умолчанию: `2.0`).  
`HERMES_MATRIX_TEXT_BATCH_DELAY_SECONDS` / `_SPLIT_DELAY_SECONDS`| Аналоги Telegram для Matrix.  
`HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS` / `_SPLIT_DELAY_SECONDS` / `_MAX_CHARS` / `_MAX_MESSAGES`| Настройка пакетного отправителя Feishu — задержка, задержка разделения, макс. символов на сообщение, макс. сообщений в пакете.  
`HERMES_FEISHU_MEDIA_BATCH_DELAY_SECONDS`| Задержка отправки медиа Feishu.  
`HERMES_FEISHU_DEDUP_CACHE_SIZE`| Размер кеша дедупликации вебхуков Feishu (по умолчанию: `1024`).  
`HERMES_WECOM_TEXT_BATCH_DELAY_SECONDS` / `_SPLIT_DELAY_SECONDS`| Настройка пакетного отправителя WeCom.  
`HERMES_VISION_DOWNLOAD_TIMEOUT`| Тайм-аут в секундах для загрузки изображения перед передачей vision-моделям (по умолчанию: `30`).  
`HERMES_RESTART_DRAIN_TIMEOUT`| Шлюз: время ожидания в секундах завершения активных запусков при `/restart` до принудительного перезапуска (по умолчанию: `900`).  
`HERMES_GATEWAY_PLATFORM_CONNECT_TIMEOUT`| Тайм-аут подключения для каждой платформы при запуске шлюза (секунды).  
`HERMES_GATEWAY_BUSY_INPUT_MODE`| Режим поведения шлюза по умолчанию при занятости: `queue`, `steer` или `interrupt`. Можно переопределить для каждого чата через `/busy`.  
`HERMES_GATEWAY_BUSY_ACK_ENABLED`| Отправляет ли шлюз подтверждающее сообщение (⚡/⏳/⏩), когда пользователь отправляет ввод, пока агент занят (по умолчанию: `true`). Установите `false`, чтобы отключить эти сообщения — ввод всё равно ставится в очередь/направляется/прерывает как обычно, только ответ в чате отключается. Перенесено из `display.busy_ack_enabled` в `config.yaml`.  
`HERMES_CRON_TIMEOUT`| Тайм-аут бездействия для запусков агента по cron в секундах (по умолчанию: `600`). Агент может работать бесконечно, пока активно вызывает инструменты или получает токены стрима — это срабатывает только при бездействии. Установите `0` для отключения.  
`HERMES_CRON_SCRIPT_TIMEOUT`| Тайм-аут для скриптов предварительного запуска, прикреплённых к задачам cron, в секундах (по умолчанию: `120`). Переопределите для скриптов, которым нужно больше времени (например, рандомизированные задержки для анти-бот тайминга). Также настраивается через `cron.script_timeout_seconds` в `config.yaml`.  
`HERMES_CRON_MAX_PARALLEL`| Максимальное количество параллельных задач cron за один тик (по умолчанию: `4`).  
## Поведение агента[​](<#agent-behavior> "Direct link to Agent Behavior")
Переменная| Описание  
---|---  
`HERMES_MAX_ITERATIONS`| Максимальное количество итераций вызова инструментов за один разговор (по умолчанию: 90)  
`HERMES_INFERENCE_MODEL`| Переопределение имени модели на уровне процесса (имеет приоритет над `config.yaml` для сессии). Также задаётся через флаг `-m`/`--model`.  
`HERMES_YOLO_MODE`| Установите `1` для пропуска запросов подтверждения опасных команд. Эквивалент `--yolo`.  
`HERMES_ACCEPT_HOOKS`| Автоматически принимать любые неизвестные хуки оболочки, объявленные в `config.yaml`, без TTY-запроса. Эквивалент `--accept-hooks` или `hooks_auto_accept: true`.  
`HERMES_IGNORE_USER_CONFIG`| Пропустить `~/.hermes/config.yaml` и использовать встроенные значения по умолчанию (учётные данные в `.env` всё равно загружаются). Эквивалент `--ignore-user-config`.  
`HERMES_IGNORE_RULES`| Пропустить авто-внедрение `AGENTS.md`, `SOUL.md`, `.cursorrules`, памяти и предзагруженных навыков. Эквивалент `--ignore-rules`.  
`HERMES_MD_NAMES`| Список имён файлов правил (через запятую) для авто-внедрения (по умолчанию: `AGENTS.md,CLAUDE.md,.cursorrules,SOUL.md`).  
`HERMES_TOOL_PROGRESS`| Устаревшая переменная совместимости для отображения прогресса инструментов. Предпочтительнее использовать `display.tool_progress` в `config.yaml`.  
`HERMES_TOOL_PROGRESS_MODE`| Устаревшая переменная совместимости для режима прогресса инструментов. Предпочтительнее использовать `display.tool_progress` в `config.yaml`.  
`HERMES_HUMAN_DELAY_MODE`| Темп ответа: `off`/`natural`/`custom`  
`HERMES_HUMAN_DELAY_MIN_MS`| Минимум диапазона пользовательской задержки (мс)  
`HERMES_HUMAN_DELAY_MAX_MS`| Максимум диапазона пользовательской задержки (мс)  
`HERMES_QUIET`| Подавить несущественный вывод (`true`/`false`)  
`HERMES_API_TIMEOUT`| Тайм-аут вызова LLM API в секундах (по умолчанию: `1800`)  
`HERMES_API_CALL_STALE_TIMEOUT`| Тайм-аут устаревшего нестримингового вызова в секундах (по умолчанию: `300`). Автоматически отключается для локальных провайдеров, если оставлено пустым. Также настраивается через `providers.<id>.stale_timeout_seconds` или `providers.<id>.models.<model>.stale_timeout_seconds` в `config.yaml`.  
`HERMES_STREAM_READ_TIMEOUT`| Тайм-аут чтения стримингового сокета в секундах (по умолчанию: `120`). Автоматически увеличивается до `HERMES_API_TIMEOUT` для локальных провайдеров. Увеличьте, если локальные LLM выходят по тайм-ауту во время длительной генерации кода.  
`HERMES_STREAM_STALE_TIMEOUT`| Тайм-аут обнаружения устаревшего стрима в секундах (по умолчанию: `180`). Автоматически отключается для локальных провайдеров. Вызывает завершение соединения, если в течение этого окна не поступает чанков.  
`HERMES_STREAM_RETRIES`| Количество попыток переподключения в середине стрима при временных сетевых ошибках (по умолчанию: `3`).  
`HERMES_AGENT_TIMEOUT`| Тайм-аут бездействия шлюза для запущенного агента в секундах (по умолчанию: `900`). Сбрасывается при каждом вызове инструмента и полученном токене стрима. Установите `0` для отключения.  
`HERMES_AGENT_TIMEOUT_WARNING`| Шлюз: отправить предупреждение после этого количества секунд бездействия (по умолчанию: 75% от `HERMES_AGENT_TIMEOUT`).  
`HERMES_AGENT_NOTIFY_INTERVAL`| Шлюз: интервал в секундах между уведомлениями о прогрессе при длительных запусках агента.  
`HERMES_CHECKPOINT_TIMEOUT`| Тайм-аут для создания файловой точки сохранения в секундах (по умолчанию: `30`).  
`HERMES_EXEC_ASK`| Включить запросы подтверждения выполнения в режиме шлюза (`true`/`false`)  
`HERMES_ENABLE_PROJECT_PLUGINS`| Включить авто-обнаружение локальных плагинов репозитория из `./.hermes/plugins/` (`true`/`false`, по умолчанию: `false`)  
`HERMES_BACKGROUND_NOTIFICATIONS`| Режим уведомлений о фоновых процессах в шлюзе: `all` (по умолчанию), `result`, `error`, `off`  
`HERMES_EPHEMERAL_SYSTEM_PROMPT`| Эфемерный системный промпт, внедряемый при вызове API (никогда не сохраняется в сессиях)  
`HERMES_PREFILL_MESSAGES_FILE`| Путь к JSON-файлу с эфемерными prefill-сообщениями, внедряемыми при вызове API.  
`HERMES_ALLOW_PRIVATE_URLS`| `true`/`false` — разрешить инструментам загружать URL localhost/частной сети. По умолчанию отключено в режиме шлюза.  
`HERMES_REDACT_SECRETS`| `true`/`false` — управление редактированием секретов в логах и передаваемых выводах (по умолчанию: `true`).  
`HERMES_WRITE_SAFE_ROOT`| Опциональный префикс директории, ограничивающий запись `write_file`/`patch`; пути вне его требуют подтверждения.  
`HERMES_DISABLE_FILE_STATE_GUARD`| Установите `1` для отключения проверки «файл изменился с момента вашего чтения» для `patch`/`write_file`.  
`HERMES_CORE_TOOLS`| Переопределение канонического списка основных инструментов (через запятую; продвинутое, редко требуется).  
`HERMES_BUNDLED_SKILLS`| Переопределение списка встроенных навыков, загружаемых при запуске (через запятую).  
`HERMES_OPTIONAL_SKILLS`| Список имён опциональных навыков (через запятую) для авто-установки при первом запуске.  
`HERMES_DEBUG_INTERRUPT`| Установите `1` для подробного логирования прерываний/отмен в `agent.log`.  
`HERMES_DUMP_REQUESTS`| Сохранять полезную нагрузку API-запросов в лог-файлы (`true`/`false`)  
`HERMES_DUMP_REQUEST_STDOUT`| Сохранять полезную нагрузку API-запросов в stdout вместо лог-файлов.  
`HERMES_OAUTH_TRACE`| Установите `1` для логирования обмена и обновления OAuth-токенов. Включает редактированную информацию о времени.  
`HERMES_OAUTH_FILE`| Переопределение пути для хранения OAuth-учётных данных (по умолчанию: `~/.hermes/auth.json`).  
`HERMES_AGENT_HELP_GUIDANCE`| Добавить дополнительный направляющий текст в системный промпт для пользовательских развёртываний.  
`HERMES_AGENT_LOGO`| Переопределение ASCII-баннера с логотипом при запуске CLI.  
`DELEGATION_MAX_CONCURRENT_CHILDREN`| Максимальное количество параллельных подагентов на один пакет `delegate_task` (по умолчанию: `3`, минимум 1, без верхнего предела). Также настраивается через `delegation.max_concurrent_children` в `config.yaml` — значение из конфига имеет приоритет.  
## Интерфейс[​](<#interface> "Direct link to Interface")
Переменная| Описание  
---|---  
`HERMES_TUI`| Запустить [TUI](</docs/user-guide/tui>) вместо классического CLI, если установлено в `1`. Эквивалент флага `--tui`.  
`HERMES_TUI_DIR`| Путь к предварительно собранной директории `ui-tui/` (должна содержать `dist/entry.js` и заполненную `node_modules`). Используется дистрибутивами и Nix для пропуска `npm install` при первом запуске.  
`HERMES_TUI_RESUME`| Возобновить конкретную TUI-сессию по ID при запуске. Если задано, `hermes --tui` пропускает создание новой сессии и восстанавливает указанную — полезно для повторного подключения после отключения или сбоя терминала.  
`HERMES_TUI_THEME`| Принудительная цветовая тема TUI: `light`, `dark` или сырой 6-символьный шестнадцатеричный цвет фона (например, `ffffff` или `1a1a2e`). Если не задано, Hermes определяет автоматически через `COLORFGBG` и запросы фона терминала; эта переменная переопределяет определение на терминалах (Ghostty, Warp, iTerm2 и т.д.), которые не устанавливают `COLORFGBG`.  
`HERMES_INFERENCE_MODEL`| Принудительная модель для `hermes -z` / `hermes chat` без изменения `config.yaml`. Сочетается с `HERMES_INFERENCE_PROVIDER`. Полезно для вызывающих скриптов (свипер, CI, пакетные запуски), которым нужно переопределять модель по умолчанию для каждого запуска.  
## Настройки сессий[​](<#session-settings> "Direct link to Session Settings")
Переменная| Описание  
---|---  
`SESSION_IDLE_MINUTES`| Сброс сессий после N минут бездействия (по умолчанию: 1440)  
`SESSION_RESET_HOUR`| Час ежедневного сброса в 24-часовом формате (по умолчанию: 4 = 4:00 утра)  
## Сжатие контекста (только config.yaml)[​](<#context-compression-configyaml-only> "Direct link to Context Compression \\(config.yaml only\\)")
Сжатие контекста настраивается исключительно через `config.yaml` — для него нет переменных окружения. Пороговые значения находятся в блоке `compression:`, а модель суммаризации/провайдер — в `auxiliary.compression:`.
[code] 
    compression:  
      enabled: true  
      threshold: 0.50  
      target_ratio: 0.20         # доля порога, сохраняемая как недавний хвост  
      protect_last_n: 20         # минимальное количество последних сообщений для сохранения без сжатия  
    
[/code]
Миграция устаревших конфигов
Старые конфиги с `compression.summary_model`, `compression.summary_provider` и `compression.summary_base_url` автоматически переносятся в `auxiliary.compression.*` при первой загрузке.
## Переопределение вспомогательных задач[​](<#auxiliary-task-overrides> "Direct link to Auxiliary Task Overrides")
Переменная| Описание  
---|---  
`AUXILIARY_VISION_PROVIDER`| Переопределение провайдера для задач vision  
`AUXILIARY_VISION_MODEL`| Переопределение модели для задач vision  
`AUXILIARY_VISION_BASE_URL`| Прямой эндпоинт, совместимый с OpenAI, для задач vision  
`AUXILIARY_VISION_API_KEY`| API-ключ в паре с `AUXILIARY_VISION_BASE_URL`  
`AUXILIARY_WEB_EXTRACT_PROVIDER`| Переопределение провайдера для извлечения/суммаризации веб-страниц  
`AUXILIARY_WEB_EXTRACT_MODEL`| Переопределение модели для извлечения/суммаризации веб-страниц  
`AUXILIARY_WEB_EXTRACT_BASE_URL`| Прямой эндпоинт, совместимый с OpenAI, для извлечения/суммаризации веб-страниц  
`AUXILIARY_WEB_EXTRACT_API_KEY`| API-ключ в паре с `AUXILIARY_WEB_EXTRACT_BASE_URL`  
Для прямых эндпоинтов, специфичных для задачи, Hermes использует настроенный API-ключ задачи или `OPENAI_API_KEY`. Он не использует повторно `OPENROUTER_API_KEY` для этих пользовательских эндпоинтов.
## Запасные провайдеры (только config.yaml)[​](<#fallback-providers-configyaml-only> "Direct link to Fallback Providers \\(config.yaml only\\)")
Цепочка запасных провайдеров для основной модели настраивается исключительно через `config.yaml` — для неё нет переменных окружения. Добавьте список `fallback_providers` верхнего уровня с ключами `provider` и `model`, чтобы включить автоматическое переключение при ошибках вашей основной модели.
[code] 
    fallback_providers:  
      - provider: openrouter  
        model: anthropic/claude-sonnet-4  
    
[/code]
Старая форма `fallback_model` для одного провайдера всё ещё читается для обратной совместимости, но для новых конфигураций следует использовать `fallback_providers`.
См. [Fallback Providers](</docs/user-guide/features/fallback-providers>) для получения полной информации.
## Маршрутизация провайдеров (только config.yaml)[​](<#provider-routing-configyaml-only> "Direct link to Provider Routing \\(config.yaml only\\)")
Эти настройки размещаются в `~/.hermes/config.yaml` в разделе `provider_routing`:
Ключ| Описание  
---|---  
`sort`| Сортировать провайдеров: `"price"` (по умолчанию), `"throughput"` или `"latency"`  
`only`| Список разрешённых идентификаторов провайдеров (например, `[\"anthropic\", \"google\"]`)  
`ignore`| Список идентификаторов провайдеров для пропуска  
`order`| Список идентификаторов провайдеров для последовательного перебора  
`require_parameters`| Использовать только провайдеров, поддерживающих все параметры запроса (`true`/`false`)  
`data_collection`| `"allow"` (по умолчанию) или `"deny"` для исключения провайдеров, хранящих данные  
tip
Используйте `hermes config set` для установки переменных окружения — он автоматически сохраняет их в нужный файл (`.env` для секретов, `config.yaml` для всего остального).
  * [LLM-провайдеры](<#llm-providers>)
  * [Аутентификация провайдеров (OAuth)](<#provider-auth-oauth>)
  * [Tool API](<#tool-apis>)
    * [Langfuse Observability](<#langfuse-observability>)
    * [Nous Tool Gateway](<#nous-tool-gateway>)
  * [Терминальный бэкенд](<#terminal-backend>)
  * [SSH-бэкенд](<#ssh-backend>)
  * [Ресурсы контейнеров (Docker, Singularity, Modal, Daytona)](<#container-resources-docker-singularity-modal-daytona>)
  * [Постоянная оболочка](<#persistent-shell>)
  * [Мессенджеры](<#messaging>)
    * [Продвинутая настройка мессенджеров](<#advanced-messaging-tuning>)
  * [Поведение агента](<#agent-behavior>)
  * [Интерфейс](<#interface>)
  * [Настройки сессий](<#session-settings>)
  * [Сжатие контекста (только config.yaml)](<#context-compression-configyaml-only>)
  * [Переопределение вспомогательных задач](<#auxiliary-task-overrides>)
  * [Запасные провайдеры (только config.yaml)](<#fallback-providers-configyaml-only>)
  * [Маршрутизация провайдеров (только config.yaml)](<#provider-routing-configyaml-only>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/environment-variables -->
