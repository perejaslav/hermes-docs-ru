On this page
Пулы учётных данных позволяют регистрировать несколько API-ключей или OAuth-токенов для одного провайдера. Когда один ключ достигает лимита запросов или квоты биллинга, Hermes автоматически переключается на следующий рабочий ключ — поддерживая вашу сессию активной без смены провайдера.

Это отличается от [резервных провайдеров](</docs/user-guide/features/fallback-providers>), которые переключаются на _другого_ провайдера полностью. Пулы учётных данных — это ротация внутри одного провайдера; резервные провайдеры — это отказоустойчивость между провайдерами. Сначала используются пулы — если все ключи в пуле исчерпаны, _тогда_ активируется резервный провайдер.
## Как это работает[​](<#how-it-works> "Прямая ссылка на раздел Как это работает")

[code] 
    Your request  
      → Pick key from pool (round_robin / least_used / fill_first / random)  
      → Send to provider  
      → 429 rate limit?  
          → Retry same key once (transient blip)  
          → Second 429 → rotate to next pool key  
          → All keys exhausted → fallback_model (different provider)  
      → 402 billing error?  
          → Immediately rotate to next pool key (24h cooldown)  
      → 401 auth expired?  
          → Try refreshing the token (OAuth)  
          → Refresh failed → rotate to next pool key  
      → Success → continue normally  
    
[/code]
## Быстрый старт[​](<#quick-start> "Прямая ссылка на раздел Быстрый старт")

Если у вас уже есть API-ключ, заданный в `.env`, Hermes автоматически обнаружит его как пул из одного ключа. Чтобы воспользоваться преимуществами пула, добавьте больше ключей:

[code] 
    # Add a second OpenRouter key  
    hermes auth add openrouter --api-key sk-or-v1-your-second-key  
      
    # Add a second Anthropic key  
    hermes auth add anthropic --type api-key --api-key sk-ant-api03-your-second-key  
      
    # Add an Anthropic OAuth credential (requires Claude Max plan + extra usage credits)  
    hermes auth add anthropic --type oauth  
    # Opens browser for OAuth login  
    
[/code]
Проверьте свои пулы:

[code] 
    hermes auth list  
    
[/code]
Вывод:

[code] 
    openrouter (2 credentials):  
      #1  OPENROUTER_API_KEY   api_key env:OPENROUTER_API_KEY ←  
      #2  backup-key           api_key manual  
      
    anthropic (3 credentials):  
      #1  hermes_pkce          oauth   hermes_pkce ←  
      #2  claude_code          oauth   claude_code  
      #3  ANTHROPIC_API_KEY    api_key env:ANTHROPIC_API_KEY  
    
[/code]
Символ `←` отмечает текущее выбранное учётное данное.
## Интерактивное управление[​](<#interactive-management> "Прямая ссылка на раздел Интерактивное управление")

Запустите `hermes auth` без подкоманды для интерактивного мастера:

[code] 
    hermes auth  
    
[/code]
Это покажет полный статус вашего пула и предложит меню:

[code] 
    What would you like to do?  
      1. Add a credential  
      2. Remove a credential  
      3. Reset cooldowns for a provider  
      4. Set rotation strategy for a provider  
      5. Exit  
    
[/code]
Для провайдеров, поддерживающих как API-ключи, так и OAuth (Anthropic, Nous, Codex), мастер добавления запрашивает тип:

[code] 
    anthropic supports both API keys and OAuth login.  
      1. API key (paste a key from the provider dashboard)  
      2. OAuth login (authenticate via browser)  
    Type [1/2]:  
    
[/code]
## Команды CLI[​](<#cli-commands> "Прямая ссылка на раздел Команды CLI")

Команда| Описание  
---|---  
`hermes auth`| Интерактивный мастер управления пулом  
`hermes auth list`| Показать все пулы и учётные данные  
`hermes auth list <provider>`| Показать пул конкретного провайдера  
`hermes auth add <provider>`| Добавить учётные данные (запрашивает тип и ключ)  
`hermes auth add <provider> --type api-key --api-key <key>`| Добавить API-ключ в неинтерактивном режиме  
`hermes auth add <provider> --type oauth`| Добавить OAuth-учётные данные через вход в браузере  
`hermes auth remove <provider> <index>`| Удалить учётные данные по индексу (начиная с 1)  
`hermes auth reset <provider>`| Очистить все таймауты/статусы исчерпания  

## Стратегии ротации[​](<#rotation-strategies> "Прямая ссылка на раздел Стратегии ротации")

Настройка через `hermes auth` → "Set rotation strategy" или в `config.yaml`:

[code] 
    credential_pool_strategies:  
      openrouter: round_robin  
      anthropic: least_used  
    
[/code]
Стратегия| Поведение  
---|---  
`fill_first` (по умолчанию)| Использовать первый рабочий ключ, пока он не исчерпан, затем перейти к следующему  
`round_robin`| Равномерно перебирать ключи, ротируя после каждого выбора  
`least_used`| Всегда выбирать ключ с наименьшим количеством запросов  
`random`| Случайный выбор среди рабочих ключей  

## Обработка ошибок[​](<#error-recovery> "Прямая ссылка на раздел Обработка ошибок")

Пул обрабатывает разные ошибки по-разному:

Ошибка| Поведение| Таймаут  
---|---|---  
**429 Лимит запросов**|  Повторить тот же ключ один раз (временный сбой). Второй последовательный 429 — ротация на следующий ключ| 1 час  
**402 Биллинг/Квота**|  Немедленно переключиться на следующий ключ| 24 часа  
**401 Истёкший доступ**|  Сначала попытаться обновить OAuth-токен. Ротация только если обновление не удалось| —  
**Все ключи исчерпаны**|  Переход к `fallback_model`, если настроен| —  

Флаг `has_retried_429` сбрасывается при каждом успешном API-вызове, поэтому единичный временный 429 не вызывает ротацию.
## Пулы пользовательских endpoint'ов[​](<#custom-endpoint-pools> "Прямая ссылка на раздел Пулы пользовательских endpoint'ов")

Пользовательские endpoint'ы, совместимые с OpenAI (Together.ai, RunPod, локальные серверы), получают свои собственные пулы, сгруппированные по имени endpoint'а из `custom_providers` в config.yaml.

Когда вы настраиваете пользовательский endpoint через `hermes model`, автоматически генерируется имя, например "Together.ai" или "Local (localhost:8080)". Это имя становится ключом пула.

[code] 
    # After setting up a custom endpoint via hermes model:  
    hermes auth list  
    # Shows:  
    #   Together.ai (1 credential):  
    #     #1  config key    api_key config:Together.ai ←  
      
    # Add a second key for the same endpoint:  
    hermes auth add Together.ai --api-key sk-together-second-key  
    
[/code]
Пулы пользовательских endpoint'ов хранятся в `auth.json` в разделе `credential_pool` с префиксом `custom:`:

[code] 
    {  
      "credential_pool": {  
        "openrouter": [...],  
        "custom:together.ai": [...]  
      }  
    }  
    
[/code]
## Автообнаружение[​](<#auto-discovery> "Прямая ссылка на раздел Автообнаружение")

Hermes автоматически обнаруживает учётные данные из нескольких источников и заполняет пул при запуске:

Источник| Пример| Автозаполнение?  
---|---|---  
Переменные окружения| `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`| Да  
OAuth-токены (auth.json)| Codex device code, Nous device code| Да  
Учётные данные Claude Code| `~/.claude/.credentials.json`| Да (Anthropic)  
Hermes PKCE OAuth| `~/.hermes/auth.json`| Да (Anthropic)  
Конфигурация пользовательского endpoint'а| `model.api_key` в config.yaml| Да (пользовательские endpoint'ы)  
Ручные записи| Добавлены через `hermes auth add`| Сохраняются в auth.json  

Автоматически заполненные записи обновляются при каждой загрузке пула — если вы удалите переменную окружения, соответствующая запись в пуле автоматически удаляется. Ручные записи (добавленные через `hermes auth add`) никогда не удаляются автоматически.
## Делегирование и совместное использование суб-агентами[​](<#delegation--subagent-sharing> "Прямая ссылка на раздел Делегирование и совместное использование суб-агентами")

Когда агент порождает суб-агентов через `delegate_task`, пул учётных данных родителя автоматически передаётся дочерним агентам:
  * **Тот же провайдер** — дочерний агент получает полный пул родителя, обеспечивая ротацию ключей при лимитах запросов
  * **Другой провайдер** — дочерний агент загружает собственный пул этого провайдера (если настроен)
  * **Пул не настроен** — дочерний агент использует унаследованный одиночный API-ключ


Это означает, что суб-агенты получают такую же устойчивость к лимитам запросов, как и родитель, без необходимости дополнительной настройки. Аренда учётных данных на каждую задачу гарантирует, что дочерние агенты не конфликтуют друг с другом при одновременной ротации ключей.
## Потокобезопасность[​](<#thread-safety> "Прямая ссылка на раздел Потокобезопасность")

Пул учётных данных использует блокировку потоков для всех изменений состояния (`select()`, `mark_exhausted_and_rotate()`, `try_refresh_current()`, `mark_used()`). Это обеспечивает безопасный конкурентный доступ, когда шлюз обрабатывает несколько чат-сессий одновременно.
## Архитектура[​](<#architecture> "Прямая ссылка на раздел Архитектура")

Полную диаграмму потока данных см. в [`docs/credential-pool-flow.excalidraw`](<https://excalidraw.com/#json=2Ycqhqpi6f12E_3ITyiwh,c7u9jSt5BwrmiVzHGbm87g>) в репозитории.

Пул учётных данных интегрирован на уровне разрешения провайдера:
  1. **`agent/credential_pool.py`** — Менеджер пула: хранение, выбор, ротация, таймауты
  2. **`hermes_cli/auth_commands.py`** — Команды CLI и интерактивный мастер
  3. **`hermes_cli/runtime_provider.py`** — Разрешение учётных данных с учётом пула
  4. **`run_agent.py`** — Обработка ошибок: 429/402/401 → ротация пула → резервный провайдер


## Хранилище[​](<#storage> "Прямая ссылка на раздел Хранилище")

Состояние пула хранится в `~/.hermes/auth.json` в ключе `credential_pool`:

[code] 
    {  
      "version": 1,  
      "credential_pool": {  
        "openrouter": [  
          {  
            "id": "abc123",  
            "label": "OPENROUTER_API_KEY",  
            "auth_type": "api_key",  
            "priority": 0,  
            "source": "env:OPENROUTER_API_KEY",  
            "access_token": "sk-or-v1-...",  
            "last_status": "ok",  
            "request_count": 142  
          }  
        ]  
      },  
    }  
    
[/code]
Стратегии хранятся в `config.yaml` (не в `auth.json`):

[code] 
    credential_pool_strategies:  
      openrouter: round_robin  
      anthropic: least_used  
    
[/code]
  * [Как это работает](<#how-it-works>)
  * [Быстрый старт](<#quick-start>)
  * [Интерактивное управление](<#interactive-management>)
  * [Команды CLI](<#cli-commands>)
  * [Стратегии ротации](<#rotation-strategies>)
  * [Обработка ошибок](<#error-recovery>)
  * [Пулы пользовательских endpoint'ов](<#custom-endpoint-pools>)
  * [Автообнаружение](<#auto-discovery>)
  * [Делегирование и совместное использование суб-агентами](<#delegation--subagent-sharing>)
  * [Потокобезопасность](<#thread-safety>)
  * [Архитектура](<#architecture>)
  * [Хранилище](<#storage>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools -->
