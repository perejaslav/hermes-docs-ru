On this page
Hermes Agent поддерживает Google Gemini в качестве нативного провайдера через **Google AI Studio / Gemini API** — а не через OpenAI-совместимый эндпоинт. Это позволяет Hermes преобразовывать свой внутренний цикл сообщений и инструментов, основанный на OpenAI-формате, в нативный API Gemini `generateContent`, сохраняя при этом вызов инструментов, стриминг, мультимодальные входные данные и метаданные ответов Gemini.

Hermes также поддерживает отдельного провайдера **Google Gemini (OAuth)**, использующего тот же бэкенд Cloud Code Assist, что и CLI Gemini от Google. Используйте провайдера с API-ключом (`gemini`) для наименее рискованного официального пути API.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

  * **API-ключ Google AI Studio** — создайте на [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
  * **Google Cloud проект с включённым биллингом** — рекомендуется для агентного использования. Бесплатный тариф Gemini слишком мал для длительных агентных сессий, поскольку Hermes может делать несколько вызовов модели на один шаг пользователя.
  * **Установленный Hermes** — для нативного провайдера Gemini не требуется дополнительных Python-пакетов.

API-ключ
Установите `GOOGLE_API_KEY` или `GEMINI_API_KEY`. Hermes проверяет оба имени для провайдера `gemini`.

## Quick Start[​](#quick-start "Direct link to Quick Start")

[code] 
    # Добавьте ваш Gemini API-ключ  
    echo "GOOGLE_API_KEY=..." >> ~/.hermes/.env  
      
    # Выберите Gemini в качестве провайдера  
    hermes model  
    # → Выберите "More providers..." → "Google AI Studio"  
    # → Hermes проверит ваш тарифный уровень и покажет модели Gemini  
    # → Выберите модель  
      
    # Начните общение  
    hermes chat  
    
[/code]

Если вы предпочитаете редактировать конфиг напрямую, используйте нативный базовый URL Gemini API:

[code] 
    model:  
      default: gemini-3-flash-preview  
      provider: gemini  
      base_url: https://generativelanguage.googleapis.com/v1beta  
    
[/code]

## Configuration[​](#configuration "Direct link to Configuration")

После запуска `hermes model` ваш `~/.hermes/config.yaml` будет содержать:

[code] 
    model:  
      default: gemini-3-flash-preview  
      provider: gemini  
      base_url: https://generativelanguage.googleapis.com/v1beta  
    
[/code]

А в `~/.hermes/.env`:

[code] 
    GOOGLE_API_KEY=...  
    
[/code]

### Native Gemini API[​](#native-gemini-api "Direct link to Native Gemini API")

Рекомендуемый эндпоинт:

[code] 
    https://generativelanguage.googleapis.com/v1beta  
    
[/code]

Hermes обнаруживает этот эндпоинт и создаёт свой нативный адаптер Gemini. Внутренне Hermes продолжает вести агентный цикл в OpenAI-формате сообщений, а затем преобразует каждый запрос в нативную схему Gemini:

  * `messages[]` → `contents[]` (Gemini)
  * системные промпты → `systemInstruction` (Gemini)
  * схемы инструментов → `functionDeclarations` (Gemini)
  * результаты инструментов → `functionResponse` parts (Gemini)
  * стриминговые ответы → чанки стрима в OpenAI-формате для цикла Hermes

Сигнатуры мысли Gemini 3

Для использования инструментов Gemini 3 Hermes сохраняет значения `thoughtSignature`, прикреплённые к частям вызова функций, и воспроизводит их на следующем шаге с инструментами. Это покрывает критически важный для валидации путь в многошаговых агентных рабочих процессах.

Gemini 3 также может прикреплять сигнатуры мысли к другим частям ответа. Нативный адаптер Hermes сегодня оптимизирован для агентных циклов с инструментами, поэтому он пока не воспроизводит каждую сигнатуру, не связанную с вызовом инструментов, с полной точностью на уровне частей.

### Prefer the Native Endpoint[​](#prefer-the-native-endpoint "Direct link to Prefer the Native Endpoint")

Google также предоставляет OpenAI-совместимый эндпоинт:

[code] 
    https://generativelanguage.googleapis.com/v1beta/openai/  
    
[/code]

Для агентных сессий Hermes предпочитайте нативный эндпоинт Gemini, указанный выше. Hermes включает нативный адаптер Gemini, поэтому он может напрямую отображать многошаговое использование инструментов, результаты вызовов инструментов, стриминг, мультимодальные входные данные и метаданные ответов Gemini на API `generateContent`. OpenAI-совместимый эндпоинт по-прежнему полезен, когда вам нужна совместимость именно с OpenAI API.

Если вы ранее установили `GEMINI_BASE_URL` на URL `/openai`, удалите его или измените:

[code] 
    GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta  
    
[/code]

### OAuth Provider[​](#oauth-provider "Direct link to OAuth Provider")

Hermes также имеет провайдера `google-gemini-cli`:

[code] 
    hermes model  
    # → Выберите "Google Gemini (OAuth)"  
    
[/code]

Он использует браузерный PKCE-логин и бэкенд Cloud Code Assist. Это может быть полезно для пользователей, которые хотят OAuth в стиле Gemini CLI, но Hermes показывает явное предупреждение, поскольку Google может расценивать использование OAuth-клиента Gemini CLI сторонним программным обеспечением как нарушение политики. Для продакшена или наименее рискованного использования предпочитайте провайдера с API-ключом, описанного выше.

## Available Models[​](#available-models "Direct link to Available Models")

Выбор моделей `hermes model` показывает модели Gemini, поддерживаемые в реестре провайдеров Hermes. Распространённые варианты:

Model| ID| Notes  
---|---|---  
Gemini 3.1 Pro Preview| `gemini-3.1-pro-preview`| Наиболее capable preview-модель, когда доступна  
Gemini 3 Pro Preview| `gemini-3-pro-preview`| Мощная модель для рассуждений и кода  
Gemini 3 Flash Preview| `gemini-3-flash-preview`| Рекомендуемый баланс скорости и возможностей  
Gemini 3.1 Flash Lite Preview| `gemini-3.1-flash-lite-preview`| Самый быстрый / дешёвый вариант, когда доступен  

Доступность моделей меняется со временем. Если модель исчезла или не включена для вашего ключа, снова запустите `hermes model` и выберите одну из текущего списка.

Идентификаторы моделей

Используйте нативные идентификаторы моделей Gemini, такие как `gemini-3-flash-preview`, а не идентификаторы в стиле OpenRouter, например `google/gemini-3-flash-preview`, когда `provider: gemini`.

### Latest Aliases[​](#latest-aliases "Direct link to Latest Aliases")

Google публикует плавающие псевдонимы для семейств Pro и Flash Gemini. `gemini-pro-latest` и `gemini-flash-latest` полезны, когда вы хотите, чтобы Google автоматически обновлял модель без изменения вашего конфига Hermes.

Alias| Currently tracks| Notes  
---|---|---  
`gemini-pro-latest`| Последняя модель Gemini Pro| Лучший выбор, когда нужна текущая Pro-модель Google по умолчанию  
`gemini-flash-latest`| Последняя модель Gemini Flash| Лучший выбор, когда нужна текущая Flash-модель Google по умолчанию  

[code] 
    model:  
      default: gemini-pro-latest  
      provider: gemini  
      base_url: https://generativelanguage.googleapis.com/v1beta  
    
[/code]  

Если вам нужна строгая воспроизводимость, предпочитайте явные идентификаторы моделей, такие как `gemini-3.1-pro-preview` или `gemini-3-flash-preview`.

### Gemma via the Gemini API[​](#gemma-via-the-gemini-api "Direct link to Gemma via the Gemini API")

Google также предоставляет модели Gemma через Gemini API. Hermes распознаёт их как модели Google, но скрывает модели Gemma с низкой пропускной способностью из стандартного выбора моделей, чтобы новые пользователи случайно не выбрали оценочную модель для длительной агентной сессии.

Полезные идентификаторы для оценки:

Model| ID| Notes  
---|---|---  
Gemma 4 31B IT| `gemma-4-31b-it`| Более крупная модель Gemma; полезна для проверки совместимости и качества  
Gemma 4 26B A4B IT| `gemma-4-26b-a4b-it`| Вариант с меньшим количеством активных параметров, когда доступен  

Эти модели лучше всего использовать как варианты для оценки на ключах Gemini API. Ценообразование Gemma API от Google — только бесплатный тариф, и лимиты использования низки по сравнению с продакшен-моделями Gemini, поэтому для продолжительного использования агента Hermes следует перейти на платную модель Gemini, самостоятельное развёртывание или другого провайдера с соответствующими квотами.

Чтобы использовать модель Gemma, скрытую из выбора, укажите её напрямую:

[code] 
    model:  
      default: gemma-4-31b-it  
      provider: gemini  
      base_url: https://generativelanguage.googleapis.com/v1beta  
    
[/code]

## Switching Models Mid-Session[​](#switching-models-mid-session "Direct link to Switching Models Mid-Session")

Используйте команду `/model` во время разговора:

[code] 
    /model gemini-3-flash-preview  
    /model gemini-flash-latest  
    /model gemini-3-pro-preview  
    /model gemini-pro-latest  
    /model gemma-4-31b-it  
    /model gemini-3.1-flash-lite-preview  
    
[/code]

Если вы ещё не настроили Gemini, выйдите из сессии и сначала запустите `hermes model`. `/model` переключает между уже настроенными провайдерами и моделями; он не собирает новые API-ключи.

## Diagnostics[​](#diagnostics "Direct link to Diagnostics")

[code] 
    hermes doctor  
    
[/code]

Doctor проверяет:

  * Доступен ли `GOOGLE_API_KEY` или `GEMINI_API_KEY`
  * Существуют ли учётные данные OAuth Gemini для `google-gemini-cli`
  * Можно ли разрешить учётные данные настроенного провайдера

Для информации о квоте OAuth выполните внутри сессии Hermes:

[code] 
    /gquota  
    
[/code]

`/gquota` относится к OAuth-провайдеру `google-gemini-cli`, а не к провайдеру с API-ключом AI Studio.

## Gateway (Messaging Platforms)[​](#gateway-messaging-platforms "Direct link to Gateway (Messaging Platforms)")

Gemini работает со всеми платформами-шлюзами Hermes (Telegram, Discord, Slack, WhatsApp, LINE, Feishu и др.). Настройте Gemini как провайдера, затем запустите шлюз обычным способом:

[code] 
    hermes gateway setup  
    hermes gateway start  
    
[/code]

Шлюз читает `config.yaml` и использует ту же конфигурацию провайдера Gemini.

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

### "Gemini native client requires an API key"[​](#gemini-native-client-requires-an-api-key "Direct link to "Gemini native client requires an API key"")

Hermes не смог найти используемый API-ключ. Добавьте один из них в `~/.hermes/.env`:

[code] 
    GOOGLE_API_KEY=...  
    # или  
    GEMINI_API_KEY=...  
    
[/code]

Затем снова запустите `hermes model`.

### "This Google API key is on the free tier"[​](#this-google-api-key-is-on-the-free-tier "Direct link to "This Google API key is on the free tier"")

Hermes проверяет уровень API-ключей Gemini во время настройки. Квоты бесплатного тарифа могут быть исчерпаны после нескольких агентных шагов, поскольку использование инструментов, повторы, сжатие и вспомогательные задачи могут потребовать множественных вызовов модели.

Включите биллинг в проекте Google Cloud, привязанном к вашему ключу, при необходимости перегенерируйте ключ, затем выполните:

[code] 
    hermes model  
    
[/code]

### "404 model not found"[​](#404-model-not-found "Direct link to "404 model not found"")

Выбранная модель недоступна для вашей учётной записи, региона или ключа. Снова запустите `hermes model` и выберите другую модель Gemini из текущего списка.

### Gemma model is not shown in `hermes model`[​](#gemma-model-is-not-shown-in-hermes-model "Direct link to gemma-model-is-not-shown-in-hermes-model")

Hermes может скрывать модели Gemma с низкой пропускной способностью из выбора по умолчанию. Если вы намеренно хотите оценить одну из них, укажите идентификатор модели напрямую в `~/.hermes/config.yaml`.

### "429 quota exceeded" on Gemma[​](#429-quota-exceeded-on-gemma "Direct link to "429 quota exceeded" on Gemma")

Модели Gemma, доступные через Gemini API, полезны для оценки, но их квоты бесплатного тарифа Gemini API невелики. Используйте их для тестирования совместимости, затем переключитесь на платную модель Gemini или другого провайдера для длительных агентных сессий.

### OpenAI-compatible endpoint is configured[​](#openai-compatible-endpoint-is-configured "Direct link to OpenAI-compatible endpoint is configured")

Проверьте `~/.hermes/.env` на наличие:

[code] 
    GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/  
    
[/code]

Измените его на нативный эндпоинт или удалите переопределение:

[code] 
    GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta  
    
[/code]

### OAuth login warning[​](#oauth-login-warning "Direct link to OAuth login warning")

Провайдер `google-gemini-cli` использует OAuth-поток Gemini CLI / Cloud Code Assist. Hermes предупреждает перед его запуском, поскольку он отличается от официального пути с API-ключом AI Studio. Используйте `provider: gemini` с `GOOGLE_API_KEY` для официальной интеграции через API-ключ.

### Tool calling fails with schema errors[​](#tool-calling-fails-with-schema-errors "Direct link to Tool calling fails with schema errors")

Обновите Hermes и повторно запустите `hermes model`. Нативный адаптер Gemini очищает схемы инструментов для более строгого формата объявления функций Gemini; старые сборки или кастомные эндпоинты могут этого не делать.

## Related[​](#related "Direct link to Related")

  * [AI Providers](/docs/integrations/providers)
  * [Configuration](/docs/user-guide/configuration)
  * [Fallback Providers](/docs/user-guide/features/fallback-providers)
  * [AWS Bedrock](/docs/guides/aws-bedrock) — нативная облачная интеграция с использованием учётных данных AWS

  * [Prerequisites](#prerequisites)
  * [Quick Start](#quick-start)
  * [Configuration](#configuration)
    * [Native Gemini API](#native-gemini-api)
    * [Prefer the Native Endpoint](#prefer-the-native-endpoint)
    * [OAuth Provider](#oauth-provider)
  * [Available Models](#available-models)
    * [Latest Aliases](#latest-aliases)
    * [Gemma via the Gemini API](#gemma-via-the-gemini-api)
  * [Switching Models Mid-Session](#switching-models-mid-session)
  * [Diagnostics](#diagnostics)
  * [Gateway (Messaging Platforms)](#gateway-messaging-platforms)
  * [Troubleshooting](#troubleshooting)
    * ["Gemini native client requires an API key"](#gemini-native-client-requires-an-api-key)
    * ["This Google API key is on the free tier"](#this-google-api-key-is-on-the-free-tier)
    * ["404 model not found"](#404-model-not-found)
    * [Gemma model is not shown in `hermes model`](#gemma-model-is-not-shown-in-hermes-model)
    * ["429 quota exceeded" on Gemma](#429-quota-exceeded-on-gemma)
    * [OpenAI-compatible endpoint is configured](#openai-compatible-endpoint-is-configured)
    * [OAuth login warning](#oauth-login-warning)
    * [Tool calling fails with schema errors](#tool-calling-fails-with-schema-errors)
  * [Related](#related)

<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/google-gemini -->
