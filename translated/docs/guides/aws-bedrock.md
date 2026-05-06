На этой странице
Hermes Agent поддерживает Amazon Bedrock как нативного провайдера, используя **Converse API** — а не OpenAI-совместимую конечную точку. Это даёт вам полный доступ к экосистеме Bedrock: IAM-аутентификация, Guardrails, кросс-региональные профили инференса и все фундаментальные модели.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  * **Учётные данные AWS** — любой источник, поддерживаемый [цепочкой учётных данных boto3](<https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html>):
    * IAM-роль инстанса (EC2, ECS, Lambda — без конфигурации)
    * Переменные окружения `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`
    * `AWS_PROFILE` для SSO или именованных профилей
    * `aws configure` для локальной разработки
  * **boto3** — установка: `pip install hermes-agent[bedrock]`
  * **IAM-разрешения** — как минимум:
    * `bedrock:InvokeModel` и `bedrock:InvokeModelWithResponseStream` (для инференса)
    * `bedrock:ListFoundationModels` и `bedrock:ListInferenceProfiles` (для обнаружения моделей)


EC2 / ECS / Lambda
На вычислительных ресурсах AWS прикрепите IAM-роль с `AmazonBedrockFullAccess` — и всё готово. Никаких API-ключей, никакой конфигурации `.env` — Hermes автоматически определяет роль инстанса.
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
[code] 
    # Установка с поддержкой Bedrock  
    pip install hermes-agent[bedrock]  
      
    # Выберите Bedrock как ваш провайдер  
    hermes model  
    # → Выберите "More providers..." → "AWS Bedrock"  
    # → Выберите регион и модель  
      
    # Начните чат  
    hermes chat  
    
[/code]
## Конфигурация[​](<#configuration> "Прямая ссылка на Конфигурация")
После выполнения `hermes model` ваш `~/.hermes/config.yaml` будет содержать:
[code] 
    model:  
      default: us.anthropic.claude-sonnet-4-6  
      provider: bedrock  
      base_url: https://bedrock-runtime.us-east-2.amazonaws.com  
      
    bedrock:  
      region: us-east-2  
    
[/code]
### Регион[​](<#region> "Прямая ссылка на Регион")
Установите AWS-регион любым из этих способов (наивысший приоритет первым):
  1. `bedrock.region` в `config.yaml`
  2. Переменная окружения `AWS_REGION`
  3. Переменная окружения `AWS_DEFAULT_REGION`
  4. По умолчанию: `us-east-1`


### Guardrails[​](<#guardrails> "Прямая ссылка на Guardrails")
Чтобы применить [Amazon Bedrock Guardrails](<https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html>) ко всем вызовам моделей:
[code] 
    bedrock:  
      region: us-east-2  
      guardrail:  
        guardrail_identifier: "abc123def456"  # Из консоли Bedrock  
        guardrail_version: "1"                # Номер версии или "DRAFT"  
        stream_processing_mode: "async"       # "sync" или "async"  
        trace: "disabled"                     # "enabled", "disabled" или "enabled_full"  
    
[/code]
### Обнаружение моделей[​](<#model-discovery> "Прямая ссылка на Обнаружение моделей")
Hermes автоматически обнаруживает доступные модели через управляющую плоскость Bedrock. Вы можете настроить обнаружение:
[code] 
    bedrock:  
      discovery:  
        enabled: true  
        provider_filter: ["anthropic", "amazon"]  # Показывать только этих провайдеров  
        refresh_interval: 3600                     # Кэширование на 1 час  
    
[/code]
## Доступные модели[​](<#available-models> "Прямая ссылка на Доступные модели")
Модели Bedrock используют **ID профилей инференса** для вызова по требованию. Средство выбора `hermes model` отображает их автоматически, с рекомендуемыми моделями наверху:
| Модель | ID | Примечания  |
|---|---|---  |
|Claude Sonnet 4.6| `us.anthropic.claude-sonnet-4-6`| Рекомендуется — лучший баланс скорости и возможностей  |
|Claude Opus 4.6| `us.anthropic.claude-opus-4-6-v1`| Самая мощная  |
|Claude Haiku 4.5| `us.anthropic.claude-haiku-4-5-20251001-v1:0`| Самый быстрый Claude  |
|Amazon Nova Pro| `us.amazon.nova-pro-v1:0`| Флагман Amazon  |
|Amazon Nova Micro| `us.amazon.nova-micro-v1:0`| Самая быстрая, самая дешёвая  |
|DeepSeek V3.2| `deepseek.v3.2`| Мощная открытая модель  |
|Llama 4 Scout 17B| `us.meta.llama4-scout-17b-instruct-v1:0`| Последняя от Meta  |
Кросс-региональный инференс
Модели с префиксом `us.` используют кросс-региональные профили инференса, которые обеспечивают лучшую пропускную способность и автоматическое переключение между регионами AWS. Модели с префиксом `global.` маршрутизируются через все доступные регионы по всему миру.
## Переключение моделей во время сессии[​](<#switching-models-mid-session> "Прямая ссылка на Переключение моделей во время сессии")
Используйте команду `/model` во время разговора:
[code] 
    /model us.amazon.nova-pro-v1:0  
    /model deepseek.v3.2  
    /model us.anthropic.claude-opus-4-6-v1  
    
[/code]
## Диагностика[​](<#diagnostics> "Прямая ссылка на Диагностика")
[code] 
    hermes doctor  
    
[/code]
Доктор проверяет:
  * Доступны ли учётные данные AWS (переменные окружения, IAM-роль, SSO)
  * Установлен ли `boto3`
  * Доступен ли Bedrock API (ListFoundationModels)
  * Количество доступных моделей в вашем регионе


## Шлюз (мессенджеры)[​](<#gateway-messaging-platforms> "Прямая ссылка на Шлюз (мессенджеры)")
Bedrock работает со всеми платформами шлюза Hermes (Telegram, Discord, Slack, Feishu и т.д.). Настройте Bedrock как ваш провайдер, затем запустите шлюз обычным образом:
[code] 
    hermes gateway setup  
    hermes gateway start  
    
[/code]
Шлюз читает `config.yaml` и использует ту же конфигурацию провайдера Bedrock.
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")
### «API-ключ не найден» / «Нет учётных данных AWS»[​](<#no-api-key-found--no-aws-credentials> "Прямая ссылка на «API-ключ не найден» / «Нет учётных данных AWS»")
Hermes проверяет учётные данные в следующем порядке:
  1. `AWS_BEARER_TOKEN_BEDROCK`
  2. `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`
  3. `AWS_PROFILE`
  4. Метаданные инстанса EC2 (IMDS)
  5. Учётные данные контейнера ECS
  6. Роль выполнения Lambda


Если ничего не найдено, выполните `aws configure` или прикрепите IAM-роль к вашему вычислительному инстансу.
### «Вызов модели ... с пропускной способностью по требованию не поддерживается»[​](<#invocation-of-model-id--with-on-demand-throughput-isnt-supported> "Прямая ссылка на «Вызов модели ... с пропускной способностью по требованию не поддерживается»")
Используйте **ID профиля инференса** (с префиксом `us.` или `global.`) вместо обычного ID фундаментальной модели. Например:
  * ❌ `anthropic.claude-sonnet-4-6`
  * ✅ `us.anthropic.claude-sonnet-4-6`


### «ThrottlingException»[​](<#throttlingexception> "Прямая ссылка на «ThrottlingException»")
Вы достигли лимита скорости Bedrock для данной модели. Hermes автоматически повторяет запрос с экспоненциальной задержкой. Чтобы увеличить лимиты, запросите увеличение квоты в [консоли AWS Service Quotas](<https://console.aws.amazon.com/servicequotas/>).
## Развёртывание на AWS в один клик[​](<#one-click-aws-deployment> "Прямая ссылка на Развёртывание на AWS в один клик")
Для полностью автоматизированного развёртывания на EC2 с CloudFormation:
**[sample-hermes-agent-on-aws-with-bedrock](<https://github.com/JiaDe-Wu/sample-hermes-agent-on-aws-with-bedrock>)** — создаёт VPC, IAM-роль, инстанс EC2 и автоматически настраивает Bedrock. Развёртывание в любом регионе одним кликом.
  * [Предварительные требования](<#prerequisites>)
  * [Быстрый старт](<#quick-start>)
  * [Конфигурация](<#configuration>)
    * [Регион](<#region>)
    * [Guardrails](<#guardrails>)
    * [Обнаружение моделей](<#model-discovery>)
  * [Доступные модели](<#available-models>)
  * [Переключение моделей во время сессии](<#switching-models-mid-session>)
  * [Диагностика](<#diagnostics>)
  * [Шлюз (мессенджеры)](<#gateway-messaging-platforms>)
  * [Устранение неполадок](<#troubleshooting>)
    * [«API-ключ не найден» / «Нет учётных данных AWS»](<#no-api-key-found--no-aws-credentials>)
    * [«Вызов модели ... с пропускной способностью по требованию не поддерживается»](<#invocation-of-model-id--with-on-demand-throughput-isnt-supported>)
    * [«ThrottlingException»](<#throttlingexception>)
  * [Развёртывание на AWS в один клик](<#one-click-aws-deployment>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/aws-bedrock -->
