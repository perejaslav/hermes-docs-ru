На этой странице

Hermes Agent поддерживает Azure AI Foundry (и Azure OpenAI) как провайдера первого класса. Один ресурс Azure может размещать модели с двумя различными сетевыми форматами:

  * **OpenAI-стиль** — `POST /v1/chat/completions` на эндпоинтах вида `https://<resource>.openai.azure.com/openai/v1`. Используется для GPT-4.x, GPT-5.x, Llama, Mistral и большинства моделей с открытыми весами.
  * **Anthropic-стиль** — `POST /v1/messages` на эндпоинтах вида `https://<resource>.services.ai.azure.com/anthropic`. Используется, когда Azure Foundry обслуживает модели Claude через формат Anthropic Messages API.

Мастер настройки проверяет ваш эндпоинт и автоматически определяет, какой транспорт используется, какие развёртывания доступны и какова длина контекста каждой модели.

## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")

  * Ресурс Azure AI Foundry или Azure OpenAI как минимум с одним развёртыванием
  * API-ключ для этого ресурса (доступен на портале Azure в разделе «Keys and Endpoint»)
  * URL эндпоинта развёртывания

## Быстрый старт[​](<#quick-start> "Direct link to Quick Start")

[code] 
    hermes model  
    # → Выберите «Azure Foundry»  
    # → Введите URL вашего эндпоинта  
    # → Введите ваш API-ключ  
    # Hermes проверяет эндпоинт и автоматически определяет транспорт + модели  
    # → Выберите модель из списка (или введите имя развёртывания вручную)  
    
[/code]

Мастер выполнит следующие действия:

  1. **Анализирует путь URL** — URL, оканчивающиеся на `/anthropic`, распознаются как маршруты Azure Foundry Claude.
  2. **Проверяет `GET <base>/models`** — если эндпоинт возвращает список моделей в формате OpenAI, Hermes переключается на `chat_completions` и заполняет список выбора идентификаторами развёртываний.
  3. **Проверяет формат Anthropic Messages** — запасной вариант для эндпоинтов, которые не предоставляют `/models`, но принимают формат Anthropic Messages.
  4. **Ручной ввод как запасной вариант** — частные/закрытые эндпоинты, отвергающие все проверки, всё равно работают; вы выбираете режим API и вводите имя развёртывания вручную.

Длина контекста для выбранной модели определяется через стандартную цепочку метаданных Hermes (`models.dev`, метаданные провайдера и жёстко заданные запасные варианты для семейств моделей) и сохраняется в `config.yaml`, чтобы модель могла правильно определить размер своего контекстного окна.

## Конфигурация (записывается в `config.yaml`)[​](<#configuration-written-to-configyaml> "Direct link to configuration-written-to-configyaml")

После запуска мастера вы увидите нечто подобное:

[code] 
    model:  
      provider: azure-foundry  
      base_url: https://my-resource.openai.azure.com/openai/v1  
      api_mode: chat_completions         # или "anthropic_messages"  
      default: gpt-5.4-mini              # имя вашего развёртывания / модели  
      context_length: 400000             # определено автоматически  
    
[/code]

И в `~/.hermes/.env`:

[code] 
    AZURE_FOUNDRY_API_KEY=<your-azure-key>  
    
[/code]

## Эндпоинты OpenAI-стиля (GPT, Llama и др.)[​](<#openai-style-endpoints-gpt-llama-etc> "Direct link to OpenAI-style endpoints (GPT, Llama, etc.)")

Azure OpenAI v1 GA эндпоинт принимает стандартный Python-клиент `openai` с минимальными изменениями:

[code] 
    model:  
      provider: azure-foundry  
      base_url: https://my-resource.openai.azure.com/openai/v1  
      api_mode: chat_completions  
      default: gpt-5.4  
    
[/code]

Важные особенности:

  * **GPT-5.x, codex и o-серия автоматически направляются в Responses API.** Azure Foundry развёртывает модели GPT-5 / codex / o1 / o3 / o4 только через Responses API — вызов `/chat/completions` для них возвращает `400 "The requested operation is unsupported."`. Hermes определяет эти семейства моделей по имени и прозрачно повышает `api_mode` до `codex_responses`, даже если в `config.yaml` всё ещё указано `api_mode: chat_completions`. GPT-4, GPT-4o, Llama, Mistral и другие развёртывания остаются на `/chat/completions`.
  * **`max_completion_tokens` используется автоматически.** Azure OpenAI (как и прямой OpenAI) требует `max_completion_tokens` для моделей gpt-4o, o-серии и gpt-5.x. Hermes отправляет правильный параметр на основе эндпоинта.
  * **Эндпоинты до v1, требующие `api-version`.** Если у вас устаревший базовый URL вида `https://<resource>.openai.azure.com/openai?api-version=2025-04-01-preview`, Hermes извлекает строку запроса и передаёт её через `default_query` в каждом запросе (иначе OpenAI SDK удаляет её при объединении путей).

## Эндпоинты Anthropic-стиля (Claude через Azure Foundry)[​](<#anthropic-style-endpoints-claude-via-azure-foundry> "Direct link to Anthropic-style endpoints (Claude via Azure Foundry)")

Для развёртываний Claude используйте маршрут Anthropic-стиля:

[code] 
    model:  
      provider: azure-foundry  
      base_url: https://my-resource.services.ai.azure.com/anthropic  
      api_mode: anthropic_messages  
      default: claude-sonnet-4-6  
    
[/code]

Важные особенности:

  * **`/v1` удаляется из базового URL.** Anthropic SDK добавляет `/v1/messages` к каждому URL запроса — Hermes удаляет завершающий `/v1` перед передачей URL в SDK, чтобы избежать двойных путей `/v1`.
  * **`api-version` передаётся через `default_query`, а не добавляется к URL.** Azure Anthropic требует строку запроса `api-version`. Встраивание её в базовый URL приводит к некорректным путям вида `/anthropic?api-version=.../v1/messages` и возвращает 404. Hermes передаёт `api-version=2025-04-15` через `default_query` Anthropic SDK.
  * **Обновление OAuth-токена отключено.** В развёртываниях Azure используются статические API-ключи. Цикл обновления OAuth-токена из `~/.claude/.credentials.json`, применяемый для Anthropic Console, явно пропускается для эндпоинтов Azure, чтобы предотвратить перезапись вашего Azure-ключа OAuth-токеном Claude Code в середине сессии.

## Альтернатива: `provider: anthropic` + базовый URL Azure[​](<#alternative-provider-anthropic--azure-base-url> "Direct link to alternative-provider-anthropic--azure-base-url")

Если у вас уже настроен `provider: anthropic` и вы просто хотите направить его на Azure AI Foundry для Claude, можно полностью пропустить провайдер `azure-foundry`:

[code] 
    model:  
      provider: anthropic  
      base_url: https://my-resource.services.ai.azure.com/anthropic  
      key_env: AZURE_ANTHROPIC_KEY  
      default: claude-sonnet-4-6  
    
[/code]

С `AZURE_ANTHROPIC_KEY`, установленным в `~/.hermes/.env`. Hermes обнаруживает `azure.com` в базовом URL и обходит цепочку OAuth-токенов Claude Code, чтобы Azure-ключ использовался напрямую с аутентификацией `x-api-key`.

`key_env` — это каноническое имя поля в snake_case; `api_key_env` (а также camelCase `keyEnv` / `apiKeyEnv`) принимаются как псевдонимы. Если установлены и `key_env`, и `AZURE_ANTHROPIC_KEY`/`ANTHROPIC_API_KEY`, то переменная окружения, указанная в `key_env`, имеет приоритет.

## Обнаружение моделей[​](<#model-discovery> "Direct link to Model discovery")

Azure **не предоставляет** чисто API-ключевой эндпоинт для просмотра ваших _развёрнутых_ моделей. Перечисление развёртываний требует аутентификации Azure Resource Manager (`az cognitiveservices account deployment list`) с субъектом Azure AD, а не ключом API вывода.

Что может сделать Hermes:

  * Эндпоинты Azure OpenAI v1 (`<resource>.openai.azure.com/openai/v1`) предоставляют `GET /models` с каталогом **доступных** моделей ресурса. Hermes использует этот список для предварительного заполнения выбора модели.
  * Маршруты Azure Foundry `/anthropic`: определяются по пути URL, имя модели вводится вручную.
  * Частные/защищённые файрволом эндпоинты: ручной ввод с сообщением «не удалось выполнить проверку».

Вы всегда можете ввести имя развёртывания напрямую — Hermes не проверяет его по возвращённому списку.

## Переменные окружения[​](<#environment-variables> "Direct link to Environment variables")

| Переменная | Назначение |
|---|---|
| `AZURE_FOUNDRY_API_KEY` | Основной API-ключ для Azure AI Foundry / Azure OpenAI |
| `AZURE_FOUNDRY_BASE_URL` | URL эндпоинта (устанавливается через `hermes model`; переменная окружения используется как запасной вариант) |
| `AZURE_ANTHROPIC_KEY` | Используется `provider: anthropic` + базовый URL Azure (альтернатива `ANTHROPIC_API_KEY`) |

## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")

**401 Unauthorized на развёртываниях gpt-5.x.** Azure обслуживает gpt-5.x через `/chat/completions`, а не `/responses`. Hermes обрабатывает это автоматически, если URL содержит `openai.azure.com`, но если вы видите 401 с сообщением `Invalid API key`, проверьте, что `api_mode` в вашем `config.yaml` установлено в `chat_completions`.

**404 на `/v1/messages?api-version=.../v1/messages`.** Это ошибка некорректного URL из старых настроек Azure Anthropic. Обновите Hermes — параметр `api-version` теперь передаётся через `default_query`, а не встраивается в базовый URL, поэтому SDK не может повредить его при объединении путей.

**Мастер сообщает «Auto-detection incomplete».** Эндпоинт отклонил как проверку `/models`, так и проверку Anthropic Messages. Это нормально для частных эндпоинтов за файрволом или с IP-белым списком. Переключитесь на ручной выбор режима API и введите имя развёртывания — всё будет работать, просто Hermes не сможет предварительно заполнить список выбора.

**Выбран неправильный транспорт.** Запустите `hermes model` снова, и мастер выполнит повторную проверку. Если проверка по-прежнему выбирает неправильный режим, вы можете отредактировать `config.yaml` напрямую:

[code] 
    model:  
      provider: azure-foundry  
      api_mode: anthropic_messages   # или chat_completions  
    
[/code]

## Связанные разделы[​](<#related> "Direct link to Related")

  * [Переменные окружения](</docs/reference/environment-variables>)
  * [Конфигурация](</docs/user-guide/configuration>)
  * [AWS Bedrock](</docs/guides/aws-bedrock>) — интеграция с другим крупным облачным провайдером

  * [Предварительные требования](<#prerequisites>)
  * [Быстрый старт](<#quick-start>)
  * [Конфигурация (записывается в `config.yaml`)](<#configuration-written-to-configyaml>)
  * [Эндпоинты OpenAI-стиля (GPT, Llama и др.)](<#openai-style-endpoints-gpt-llama-etc>)
  * [Эндпоинты Anthropic-стиля (Claude через Azure Foundry)](<#anthropic-style-endpoints-claude-via-azure-foundry>)
  * [Альтернатива: `provider: anthropic` + базовый URL Azure](<#alternative-provider-anthropic--azure-base-url>)
  * [Обнаружение моделей](<#model-discovery>)
  * [Переменные окружения](<#environment-variables>)
  * [Устранение неполадок](<#troubleshooting>)
  * [Связанные разделы](<#related>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/azure-foundry -->
