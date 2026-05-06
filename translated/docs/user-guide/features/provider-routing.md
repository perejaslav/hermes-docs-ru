На этой странице
При использовании [OpenRouter](<https://openrouter.ai>) в качестве провайдера LLM, Hermes Agent поддерживает **маршрутизацию провайдеров (provider routing)** — детальный контроль над тем, какие базовые AI-провайдеры обрабатывают ваши запросы и как они приоритизируются.
OpenRouter направляет запросы ко многим провайдерам (например, Anthropic, Google, AWS Bedrock, Together AI). Маршрутизация провайдеров позволяет оптимизировать стоимость, скорость, качество или обеспечить выполнение требований конкретного провайдера.
## Конфигурация[​](<#configuration> "Прямая ссылка на Конфигурация")
Добавьте секцию `provider_routing` в ваш `~/.hermes/config.yaml`:
[code] 
    provider_routing:  
      sort: "price"           # Как ранжировать провайдеров  
      only: []                # Белый список: использовать только этих провайдеров  
      ignore: []              # Чёрный список: никогда не использовать этих провайдеров  
      order: []               # Явный порядок приоритета провайдеров  
      require_parameters: false  # Использовать только провайдеров, поддерживающих все параметры  
      data_collection: null   # Управление сбором данных ("allow" или "deny")  
    
[/code]
info
Маршрутизация провайдеров применяется только при использовании OpenRouter. Она не действует при прямых подключениях к провайдерам (например, прямое подключение к API Anthropic).
## Опции[​](<#options> "Прямая ссылка на Опции")
### `sort`[​](<#sort> "Прямая ссылка на sort")
Управляет тем, как OpenRouter ранжирует доступных провайдеров для вашего запроса.
Значение| Описание  
---|---  
`"price"`| Сначала самый дешёвый провайдер  
`"throughput"`| Сначала самый быстрый по токенам в секунду  
`"latency"`| Сначала с наименьшей задержкой до первого токена
[code] 
    provider_routing:  
      sort: "price"  
    
[/code]  
### `only`[​](<#only> "Прямая ссылка на only")
Белый список имён провайдеров. Если задан, будут использоваться **только** эти провайдеры. Все остальные исключаются.
[code] 
    provider_routing:  
      only:  
        - "Anthropic"  
        - "Google"  
    
[/code]
### `ignore`[​](<#ignore> "Прямая ссылка на ignore")
Чёрный список имён провайдеров. Эти провайдеры **никогда** не будут использоваться, даже если они предлагают самый дешёвый или быстрый вариант.
[code] 
    provider_routing:  
      ignore:  
        - "Together"  
        - "DeepInfra"  
    
[/code]
### `order`[​](<#order> "Прямая ссылка на order")
Явный порядок приоритета. Провайдеры, указанные первыми, имеют преимущество. Неперечисленные провайдеры используются как запасные.
[code] 
    provider_routing:  
      order:  
        - "Anthropic"  
        - "Google"  
        - "AWS Bedrock"  
    
[/code]
### `require_parameters`[​](<#require_parameters> "Прямая ссылка на require_parameters")
Если `true`, OpenRouter будет направлять запросы только провайдерам, поддерживающим **все** параметры вашего запроса (такие как `temperature`, `top_p`, `tools` и т.д.). Это позволяет избежать незаметного игнорирования параметров.
[code] 
    provider_routing:  
      require_parameters: true  
    
[/code]
### `data_collection`[​](<#data_collection> "Прямая ссылка на data_collection")
Управляет тем, могут ли провайдеры использовать ваши запросы для обучения. Возможные значения: `"allow"` или `"deny"`.
[code] 
    provider_routing:  
      data_collection: "deny"  
    
[/code]
## Практические примеры[​](<#practical-examples> "Прямая ссылка на Практические примеры")
### Оптимизация по стоимости[​](<#optimize-for-cost> "Прямая ссылка на Оптимизация по стоимости")
Направляйте запросы самому дешёвому доступному провайдеру. Хорошо для большого объёма использования и разработки:
[code] 
    provider_routing:  
      sort: "price"  
    
[/code]
### Оптимизация по скорости[​](<#optimize-for-speed> "Прямая ссылка на Оптимизация по скорости")
Приоритизация провайдеров с низкой задержкой для интерактивного использования:
[code] 
    provider_routing:  
      sort: "latency"  
    
[/code]
### Оптимизация по пропускной способности[​](<#optimize-for-throughput> "Прямая ссылка на Оптимизация по пропускной способности")
Лучше всего подходит для длительной генерации, где важны токены в секунду:
[code] 
    provider_routing:  
      sort: "throughput"  
    
[/code]
### Фиксация на конкретных провайдерах[​](<#lock-to-specific-providers> "Прямая ссылка на Фиксация на конкретных провайдерах")
Гарантирует, что все запросы проходят через определённого провайдера для обеспечения согласованности:
[code] 
    provider_routing:  
      only:  
        - "Anthropic"  
    
[/code]
### Исключение определённых провайдеров[​](<#avoid-specific-providers> "Прямая ссылка на Исключение определённых провайдеров")
Исключите провайдеров, которых вы не хотите использовать (например, для конфиденциальности данных):
[code] 
    provider_routing:  
      ignore:  
        - "Together"  
        - "Lepton"  
      data_collection: "deny"  
    
[/code]
### Предпочтительный порядок с запасными вариантами[​](<#preferred-order-with-fallbacks> "Прямая ссылка на Предпочтительный порядок с запасными вариантами")
Сначала пробуйте предпочтительных провайдеров, используйте запасных, если они недоступны:
[code] 
    provider_routing:  
      order:  
        - "Anthropic"  
        - "Google"  
      require_parameters: true  
    
[/code]
## Как это работает[​](<#how-it-works> "Прямая ссылка на Как это работает")
Настройки маршрутизации провайдеров передаются в API OpenRouter через поле `extra_body.provider` при каждом вызове API. Это относится как к:
  * **Режиму CLI** — настраивается в `~/.hermes/config.yaml`, загружается при запуске
  * **Режиму Gateway** — тот же файл конфигурации, загружается при запуске gateway


Конфигурация маршрутизации читается из `config.yaml` и передаётся в качестве параметров при создании `AIAgent`:
[code] 
    providers_allowed  ← from provider_routing.only  
    providers_ignored  ← from provider_routing.ignore  
    providers_order    ← from provider_routing.order  
    provider_sort      ← from provider_routing.sort  
    provider_require_parameters ← from provider_routing.require_parameters  
    provider_data_collection    ← from provider_routing.data_collection  
    
[/code]
tip
Вы можете комбинировать несколько опций. Например, сортировать по цене, но исключить определённых провайдеров и требовать поддержку параметров:
[code]
    provider_routing:  
      sort: "price"  
      ignore: ["Together"]  
      require_parameters: true  
      data_collection: "deny"  
    
[/code]
## Поведение по умолчанию[​](<#default-behavior> "Прямая ссылка на Поведение по умолчанию")
Если секция `provider_routing` не настроена (по умолчанию), OpenRouter использует свою собственную логику маршрутизации по умолчанию, которая обычно автоматически балансирует стоимость и доступность.
Маршрутизация провайдеров vs. Запасные провайдеры
Маршрутизация провайдеров управляет тем, какие **суб-провайдеры внутри OpenRouter** обрабатывают ваши запросы. Для автоматического переключения на совершенно другого провайдера, когда ваша основная модель недоступна, см. [Запасные провайдеры (Fallback Providers)](</docs/user-guide/features/fallback-providers>).
  * [Конфигурация](<#configuration>)
  * [Опции](<#options>)
    * [`sort`](<#sort>)
    * [`only`](<#only>)
    * [`ignore`](<#ignore>)
    * [`order`](<#order>)
    * [`require_parameters`](<#require_parameters>)
    * [`data_collection`](<#data_collection>)
  * [Практические примеры](<#practical-examples>)
    * [Оптимизация по стоимости](<#optimize-for-cost>)
    * [Оптимизация по скорости](<#optimize-for-speed>)
    * [Оптимизация по пропускной способности](<#optimize-for-throughput>)
    * [Фиксация на конкретных провайдерах](<#lock-to-specific-providers>)
    * [Исключение определённых провайдеров](<#avoid-specific-providers>)
    * [Предпочтительный порядок с запасными вариантами](<#preferred-order-with-fallbacks>)
  * [Как это работает](<#how-it-works>)
  * [Поведение по умолчанию](<#default-behavior>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing -->
