На этой странице
Начало работы
Tool Gateway включён в платные подписки Nous Portal. **[Управлять подпиской →](<https://portal.nousresearch.com/manage-subscription>)**
**Tool Gateway** позволяет платным подписчикам [Nous Portal](<https://portal.nousresearch.com>) использовать веб-поиск, генерацию изображений, преобразование текста в речь и автоматизацию браузера через существующую подписку — без необходимости регистрироваться для получения отдельных API-ключей от Firecrawl, FAL, OpenAI или Browser Use.
## Что входит[​](<#whats-included> "Прямая ссылка на Что входит")
Инструмент| Что делает| Прямая альтернатива
|---|---|---
**Веб-поиск и извлечение**| Поиск в интернете и извлечение содержимого страниц через Firecrawl| `FIRECRAWL_API_KEY`, `EXA_API_KEY`, `PARALLEL_API_KEY`, `TAVILY_API_KEY`
**Генерация изображений**| Генерация изображений через FAL (9 моделей: FLUX 2 Klein/Pro, GPT-Image 1.5/2, Nano Banana Pro, Ideogram V3, Recraft V4 Pro, Qwen, Z-Image Turbo)| `FAL_KEY`
**Преобразование текста в речь**| Преобразование текста в речь через OpenAI TTS| `VOICE_TOOLS_OPENAI_KEY`, `ELEVENLABS_API_KEY`
**Автоматизация браузера**| Управление облачными браузерами через Browser Use| `BROWSER_USE_API_KEY`, `BROWSERBASE_API_KEY`
Все четыре инструмента тарифицируются через вашу подписку Nous. Вы можете включить любую комбинацию — например, использовать шлюз для веб-поиска и генерации изображений, оставив собственный ключ ElevenLabs для TTS.
## Право доступа[​](<#eligibility> "Прямая ссылка на Право доступа")
Tool Gateway доступен **платным** подписчикам [Nous Portal](<https://portal.nousresearch.com/manage-subscription>). Аккаунты бесплатного тарифа не имеют доступа — [обновите подписку](<https://portal.nousresearch.com/manage-subscription>), чтобы разблокировать его.
Чтобы проверить свой статус:
[code] 
    hermes status  
    
[/code]
Ищите раздел **Nous Tool Gateway**. Он показывает, какие инструменты активны через шлюз, какие используют прямые ключи, а какие не настроены.
## Включение Tool Gateway[​](<#enabling-the-tool-gateway> "Прямая ссылка на Включение Tool Gateway")
### Во время настройки модели[​](<#during-model-setup> "Прямая ссылка на Во время настройки модели")
Когда вы запускаете `hermes model` и выбираете Nous Portal в качестве провайдера, Hermes автоматически предлагает включить Tool Gateway:
[code] 
    Your Nous subscription includes the Tool Gateway.  
      
      The Tool Gateway gives you access to web search, image generation,  
      text-to-speech, and browser automation through your Nous subscription.  
      No need to sign up for separate API keys — just pick the tools you want.  
      
      ○ Web search & extract (Firecrawl) — not configured  
      ○ Image generation (FAL) — not configured  
      ○ Text-to-speech (OpenAI TTS) — not configured  
      ○ Browser automation (Browser Use) — not configured  
      
      ● Enable Tool Gateway  
      ○ Skip  
    
[/code]
Выберите **Enable Tool Gateway** — и готово.
Если у вас уже есть прямые API-ключи для некоторых инструментов, приглашение адаптируется — вы можете включить шлюз для всех инструментов (существующие ключи останутся в `.env`, но не будут использоваться в рантайме), включить только для ненастроенных инструментов или пропустить полностью.
### Через `hermes tools`[​](<#via-hermes-tools> "Прямая ссылка на Через hermes tools")
Вы также можете включить шлюз поинструментно через интерактивную настройку инструментов:
[code] 
    hermes tools  
    
[/code]
Выберите категорию инструментов (Web, Browser, Image Generation или TTS), затем укажите **Nous Subscription** в качестве провайдера. Это устанавливает `use_gateway: true` для данного инструмента в вашей конфигурации.
### Ручная настройка[​](<#manual-configuration> "Прямая ссылка на Ручная настройка")
Установите флаг `use_gateway` напрямую в `~/.hermes/config.yaml`:
[code] 
    web:  
      backend: firecrawl  
      use_gateway: true  
      
    image_gen:  
      use_gateway: true  
      
    tts:  
      provider: openai  
      use_gateway: true  
      
    browser:  
      cloud_provider: browser-use  
      use_gateway: true  
    
[/code]
## Как это работает[​](<#how-it-works> "Прямая ссылка на Как это работает")
Когда для инструмента установлено `use_gateway: true`, среда выполнения направляет API-вызовы через Nous Tool Gateway вместо использования прямых API-ключей:
  1. **Веб-инструменты** — `web_search` и `web_extract` используют endpoint Firecrawl шлюза
  2. **Генерация изображений** — `image_generate` использует endpoint FAL шлюза
  3. **TTS** — `text_to_speech` использует endpoint OpenAI Audio шлюза
  4. **Браузер** — `browser_navigate` и другие инструменты браузера используют endpoint Browser Use шлюза


Шлюз аутентифицируется с использованием ваших учётных данных Nous Portal (хранятся в `~/.hermes/auth.json` после `hermes model`).
### Приоритет[​](<#precedence> "Прямая ссылка на Приоритет")
Каждый инструмент сначала проверяет `use_gateway`:
  * **`use_gateway: true`** → маршрутизация через шлюз, даже если в `.env` есть прямые API-ключи
  * **`use_gateway: false`** (или отсутствует) → использовать прямые API-ключи, если доступны; иначе использовать шлюз, только если прямых ключей нет


Это означает, что вы можете переключаться между шлюзом и прямыми ключами в любое время без удаления учётных данных из `.env`.
## Возврат к прямым ключам[​](<#switching-back-to-direct-keys> "Прямая ссылка на Возврат к прямым ключам")
Чтобы перестать использовать шлюз для конкретного инструмента:
[code] 
    hermes tools    # Выберите инструмент → укажите прямого провайдера  
    
[/code]
Или установите `use_gateway: false` в конфиге:
[code] 
    web:  
      backend: firecrawl  
      use_gateway: false  # Теперь используется FIRECRAWL_API_KEY из .env  
    
[/code]
Когда вы выбираете провайдера, не являющегося шлюзом, в `hermes tools`, флаг `use_gateway` автоматически устанавливается в `false`, чтобы предотвратить противоречивую конфигурацию.
## Проверка статуса[​](<#checking-status> "Прямая ссылка на Проверка статуса")
[code] 
    hermes status  
    
[/code]
Раздел **Nous Tool Gateway** показывает:
[code] 
    ◆ Nous Tool Gateway  
      Nous Portal   ✓ managed tools available  
      Web tools       ✓ active via Nous subscription  
      Image gen       ✓ active via Nous subscription  
      TTS             ✓ active via Nous subscription  
      Browser         ○ active via Browser Use key  
      Modal           ○ available via subscription (optional)  
    
[/code]
Инструменты, помеченные как «active via Nous subscription», маршрутизируются через шлюз. Инструменты с собственными ключами показывают, какой провайдер активен.
## Продвинутый: Самостоятельный шлюз[​](<#advanced-self-hosted-gateway> "Прямая ссылка на Продвинутый: Самостоятельный шлюз")
Для самостоятельных или кастомных развёртываний шлюза вы можете переопределить endpoints шлюза через переменные окружения в `~/.hermes/.env`:
[code] 
    TOOL_GATEWAY_DOMAIN=nousresearch.com     # Базовый домен для маршрутизации шлюза  
    TOOL_GATEWAY_SCHEME=https                 # HTTP или HTTPS (по умолчанию: https)  
    TOOL_GATEWAY_USER_TOKEN=your-token        # Токен аутентификации (обычно заполняется автоматически)  
    FIRECRAWL_GATEWAY_URL=https://...         # Переопределение endpoint Firecrawl  
    
[/code]
Эти переменные окружения всегда видны в конфигурации независимо от статуса подписки — они полезны для настройки собственной инфраструктуры.
## Часто задаваемые вопросы[​](<#faq> "Прямая ссылка на Часто задаваемые вопросы")
### Нужно ли удалять существующие API-ключи?[​](<#do-i-need-to-delete-my-existing-api-keys> "Прямая ссылка на Нужно ли удалять существующие API-ключи?")
Нет. Когда установлено `use_gateway: true`, среда выполнения пропускает прямые API-ключи и маршрутизирует запросы через шлюз. Ваши ключи остаются в `.env` нетронутыми. Если вы позже отключите шлюз, они снова начнут использоваться автоматически.
### Можно ли использовать шлюз для одних инструментов и прямые ключи для других?[​](<#can-i-use-the-gateway-for-some-tools-and-direct-keys-for-others> "Прямая ссылка на Можно ли использовать шлюз для одних инструментов и прямые ключи для других?")
Да. Флаг `use_gateway` настраивается для каждого инструмента отдельно. Вы можете комбинировать — например, шлюз для веб-поиска и генерации изображений, собственный ключ ElevenLabs для TTS и Browserbase для автоматизации браузера.
### Что если моя подписка истечёт?[​](<#what-if-my-subscription-expires> "Прямая ссылка на Что если моя подписка истечёт?")
Инструменты, маршрутизируемые через шлюз, перестанут работать, пока вы не [продлите подписку](<https://portal.nousresearch.com/manage-subscription>) или не переключитесь на прямые API-ключи через `hermes tools`.
### Работает ли шлюз с messaging-шлюзом?[​](<#does-the-gateway-work-with-the-messaging-gateway> "Прямая ссылка на Работает ли шлюз с messaging-шлюзом?")
Да. Tool Gateway маршрутизирует API-вызовы инструментов независимо от того, используете ли вы CLI, Telegram, Discord или любую другую платформу обмена сообщениями. Он работает на уровне среды выполнения инструментов, а не на уровне точки входа.
### Включён ли Modal?[​](<#is-modal-included> "Прямая ссылка на Включён ли Modal?")
Modal (серверный бэкенд терминала) доступен как опциональное дополнение через подписку Nous. Он не включается через приглашение Tool Gateway — настройте его отдельно через `hermes setup terminal` или в `config.yaml`.
  * [Что входит](<#whats-included>)
  * [Право доступа](<#eligibility>)
  * [Включение Tool Gateway](<#enabling-the-tool-gateway>)
    * [Во время настройки модели](<#during-model-setup>)
    * [Через `hermes tools`](<#via-hermes-tools>)
    * [Ручная настройка](<#manual-configuration>)
  * [Как это работает](<#how-it-works>)
    * [Приоритет](<#precedence>)
  * [Возврат к прямым ключам](<#switching-back-to-direct-keys>)
  * [Проверка статуса](<#checking-status>)
  * [Продвинутый: Самостоятельный шлюз](<#advanced-self-hosted-gateway>)
  * [Часто задаваемые вопросы](<#faq>)
    * [Нужно ли удалять существующие API-ключи?](<#do-i-need-to-delete-my-existing-api-keys>)
    * [Можно ли использовать шлюз для одних инструментов и прямые ключи для других?](<#can-i-use-the-gateway-for-some-tools-and-direct-keys-for-others>)
    * [Что если моя подписка истечёт?](<#what-if-my-subscription-expires>)
    * [Работает ли шлюз с messaging-шлюзом?](<#does-the-gateway-work-with-the-messaging-gateway>)
    * [Включён ли Modal?](<#is-modal-included>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway -->
