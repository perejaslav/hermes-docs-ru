On this page
Hermes Agent поставляется с 8 плагинами внешних провайдеров памяти, которые дают агенту постоянное, межсессионное знание помимо встроенных MEMORY.md и USER.md. Одновременно может быть активен только **один** внешний провайдер — встроенная память всегда активна вместе с ним.
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
[code] 
    hermes memory setup      # интерактивный выбор + настройка  
    hermes memory status     # проверка активного провайдера  
    hermes memory off        # отключение внешнего провайдера  
    
[/code]
Вы также можете выбрать активный провайдер памяти через `hermes plugins` → Provider Plugins → Memory Provider.
Или установить вручную в `~/.hermes/config.yaml`:
[code] 
    memory:  
      provider: openviking   # или honcho, mem0, hindsight, holographic, retaindb, byterover, supermemory  
    
[/code]
## How It Works[​](<#how-it-works> "Direct link to How It Works")
Когда провайдер памяти активен, Hermes автоматически:
  1. **Внедряет контекст провайдера** в системный промпт (то, что знает провайдер)
  2. **Предзагружает релевантные воспоминания** перед каждым шагом (в фоне, неблокирующе)
  3. **Синхронизирует шаги разговора** с провайдером после каждого ответа
  4. **Извлекает воспоминания по завершении сессии** (для провайдеров, которые это поддерживают)
  5. **Зеркалирует записи встроенной памяти** во внешний провайдер
  6. **Добавляет инструменты, специфичные для провайдера**, чтобы агент мог искать, сохранять и управлять воспоминаниями


Встроенная память (MEMORY.md / USER.md) продолжает работать как прежде. Внешний провайдер является дополнением.
## Available Providers[​](<#available-providers> "Direct link to Available Providers")
### Honcho[​](<#honcho> "Direct link to Honcho")
AI-native межсессионное моделирование пользователя с диалектическим мышлением, внедрением контекста в рамках сессии, семантическим поиском и постоянными выводами. Базовый контекст теперь включает сводку сессии наряду с представлением пользователя и карточками пиров, давая агенту понимание того, что уже было обсуждено.
|   
|---|---  
**Best for**|  Мультиагентные системы с межсессионным контекстом, выравнивание пользователь-агент  
**Requires**| `pip install honcho-ai` + [API key](<https://app.honcho.dev>) или самостоятельно размещённый экземпляр  
**Data storage**|  Honcho Cloud или самостоятельно размещённое  
**Cost**|  Цены Honcho (облако) / бесплатно (самостоятельно)  
**Tools (5):** `honcho_profile` (чтение/обновление карточки пира), `honcho_search` (семантический поиск), `honcho_context` (контекст сессии — сводка, представление, карточка, сообщения), `honcho_reasoning` (синтезированный LLM), `honcho_conclude` (создание/удаление выводов)
**Architecture:** Двухуровневое внедрение контекста — базовый слой (сводка сессии + представление + карточка пира, обновляется с частотой `contextCadence`) плюс диалектическое дополнение (рассуждения LLM, обновляется с частотой `dialecticCadence`). Диалектика автоматически выбирает холодные стартовые промпты (общие факты о пользователе) против тёплых промптов (контекст в рамках сессии) в зависимости от того, существует ли базовый контекст.
**Три ортогональные конфигурационные ручки** управляют стоимостью и глубиной независимо:
  * `contextCadence` — как часто обновляется базовый слой (частота API-вызовов)
  * `dialecticCadence` — как часто срабатывает диалектический LLM (частота вызовов LLM)
  * `dialecticDepth` — сколько проходов `.chat()` на один вызов диалектики (1–3, глубина рассуждений)


**Setup Wizard:**
[code] 
    hermes honcho setup        # (устаревшая команда)   
    # или  
    hermes memory setup        # выберите "honcho"  
    
[/code]
**Config:** `$HERMES_HOME/honcho.json` (локальный для профиля) или `~/.honcho/config.json` (глобальный). Порядок разрешения: `$HERMES_HOME/honcho.json` > `~/.hermes/honcho.json` > `~/.honcho/config.json`. См. [справочник по конфигурации](<https://github.com/hermes-ai/hermes-agent/blob/main/plugins/memory/honcho/README.md>) и [руководство по интеграции Honcho](<https://docs.honcho.dev/v3/guides/integrations/hermes>).
Full config reference
Key| Default| Description  
---|---|---|---  
`apiKey`| \\--| API-ключ из [app.honcho.dev](<https://app.honcho.dev>)  
`baseUrl`| \\--| Базовый URL для самостоятельно размещённого Honcho  
`peerName`| \\--| Идентичность пира-пользователя  
`aiPeer`| host key| Идентичность AI-пира (один на профиль)  
`workspace`| host key| ID общего рабочего пространства  
`contextTokens`| `null` (без лимита)| Бюджет токенов для автоматически внедряемого контекста на шаг. Обрезается по границам слов  
`contextCadence`| `1`| Минимальное количество шагов между API-вызовами `context()` (обновление базового слоя)  
`dialecticCadence`| `2`| Минимальное количество шагов между вызовами LLM `peer.chat()`. Рекомендуется 1–5. Применяется только к режимам `hybrid`/`context`  
`dialecticDepth`| `1`| Количество проходов `.chat()` на один вызов диалектики. Ограничено 1–3. Проход 0: холодный/тёплый промпт, проход 1: самопроверка, проход 2: согласование  
`dialecticDepthLevels`| `null`| Опциональный массив уровней рассуждений на проход, например `["minimal", "low", "medium"]`. Переопределяет пропорциональные значения по умолчанию  
`dialecticReasoningLevel`| `'low'`| Базовый уровень рассуждений: `minimal`, `low`, `medium`, `high`, `max`  
`dialecticDynamic`| `true`| Если `true`, модель может переопределять уровень рассуждений при каждом вызове через параметр инструмента  
`dialecticMaxChars`| `600`| Максимальное количество символов результата диалектики, внедряемого в системный промпт  
`recallMode`| `'hybrid'`| `hybrid` (автовнедрение + инструменты), `context` (только внедрение), `tools` (только инструменты)  
`writeFrequency`| `'async'`| Когда сбрасывать сообщения: `async` (фоновый поток), `turn` (синхронно), `session` (пакетно по окончании), или целое число N  
`saveMessages`| `true`| Сохранять ли сообщения в Honcho API  
`observationMode`| `'directional'`| `directional` (все включены) или `unified` (общий пул). Переопределяется объектом `observation`  
`messageMaxChars`| `25000`| Максимальное количество символов на сообщение (разбивается на части при превышении)  
`dialecticMaxInputChars`| `10000`| Максимальное количество символов для ввода запроса диалектики в `peer.chat()`  
`sessionStrategy`| `'per-directory'`| `per-directory`, `per-repo`, `per-session`, `global`  
Minimal honcho.json (cloud)
[code]
    {  
      "apiKey": "your-key-from-app.honcho.dev",  
      "hosts": {  
        "hermes": {  
          "enabled": true,  
          "aiPeer": "hermes",  
          "peerName": "your-name",  
          "workspace": "hermes"  
        }  
      }  
    }  
    
[/code]
Minimal honcho.json (self-hosted)
[code]
    {  
      "baseUrl": "http://localhost:8000",  
      "hosts": {  
        "hermes": {  
          "enabled": true,  
          "aiPeer": "hermes",  
          "peerName": "your-name",  
          "workspace": "hermes"  
        }  
      }  
    }  
    
[/code]
Migrating from `hermes honcho`
Если вы ранее использовали `hermes honcho setup`, ваша конфигурация и все данные на стороне сервера сохраняются. Просто повторно включите через мастер настройки или вручную установите `memory.provider: honcho`, чтобы реактивировать через новую систему.
**Multi-peer setup:**
Honcho моделирует разговоры как пиров, обменивающихся сообщениями — один пир-пользователь плюс один AI-пир на профиль Hermes, все в общем рабочем пространстве. Рабочее пространство — это общая среда: пир-пользователь глобален для всех профилей, каждый AI-пир имеет свою собственную идентичность. Каждый AI-пир строит независимое представление/карточку из своих собственных наблюдений, поэтому профиль `coder` остаётся ориентированным на код, а профиль `writer` остаётся редакционным для того же пользователя.
The mapping:
Concept| What it is  
---|---  
**Workspace**|  Общая среда. Все профили Hermes в одном рабочем пространстве видят одну и ту же идентичность пользователя.  
**User peer** (`peerName`)| Человек. Общий для всех профилей в рабочем пространстве.  
**AI peer** (`aiPeer`)| Один на профиль Hermes. Ключ хоста `hermes` → по умолчанию; `hermes.<profile>` для других.  
**Observation**|  Переключатели для каждого пира, управляющие тем, что Honcho моделирует из чьих сообщений. `directional` (по умолчанию, все четыре включены) или `unified` (единый пул наблюдателя).  
### New profile, fresh Honcho peer[​](<#new-profile-fresh-honcho-peer> "Direct link to New profile, fresh Honcho peer")
[code] 
    hermes profile create coder --clone  
    
[/code]
`--clone` создаёт блок хоста `hermes.coder` в `honcho.json` с `aiPeer: "coder"`, общим `workspace`, унаследованными `peerName`, `recallMode`, `writeFrequency`, `observation` и т.д. AI-пир eagerly создаётся в Honcho, чтобы существовать до первого сообщения.
### Existing profiles, backfill Honcho peers[​](<#existing-profiles-backfill-honcho-peers> "Direct link to Existing profiles, backfill Honcho peers")
[code] 
    hermes honcho sync  
    
[/code]
Сканирует каждый профиль Hermes, создаёт блоки хостов для любого профиля без него, наследуя настройки из блока `hermes` по умолчанию, и eagerly создаёт новые AI-пиры. Идемпотентно — пропускает профили, у которых уже есть блок хоста.
### Per-profile observation[​](<#per-profile-observation> "Direct link to Per-profile observation")
Каждый блок хоста может независимо переопределять конфигурацию наблюдения. Пример: профиль, ориентированный на код, где AI-пир наблюдает пользователя, но не моделирует себя:
[code] 
    "hermes.coder": {  
      "aiPeer": "coder",  
      "observation": {  
        "user": { "observeMe": true, "observeOthers": true },  
        "ai":   { "observeMe": false, "observeOthers": true }  
      }  
    }  
    
[/code]
**Observation toggles (one set per peer):**
Toggle| Effect  
---|---  
`observeMe`| Honcho строит представление этого пира из его собственных сообщений  
`observeOthers`| Этот пир наблюдает сообщения другого пира (питает межпировое мышление)  
Presets via `observationMode`:
  * **`"directional"`** (по умолчанию) — все четыре флага включены. Полное взаимное наблюдение; включает межпировую диалектику.
  * **`"unified"`** — пользователь `observeMe: true`, AI `observeOthers: true`, остальные false. Единый пул наблюдателя; AI моделирует пользователя, но не себя, пир-пользователь моделирует только себя.


Переключатели на стороне сервера, установленные через [панель Honcho](<https://app.honcho.dev>), имеют приоритет над локальными значениями по умолчанию — синхронизируются обратно при инициализации сессии.
См. [страницу Honcho](</docs/user-guide/features/honcho#observation-directional-vs-unified>) для полного справочника по наблюдению.
Full honcho.json example (multi-profile)
[code]
    {  
      "apiKey": "your-key",  
      "workspace": "hermes",  
      "peerName": "eri",  
      "hosts": {  
        "hermes": {  
          "enabled": true,  
          "aiPeer": "hermes",  
          "workspace": "hermes",  
          "peerName": "eri",  
          "recallMode": "hybrid",  
          "writeFrequency": "async",  
          "sessionStrategy": "per-directory",  
          "observation": {  
            "user": { "observeMe": true, "observeOthers": true },  
            "ai": { "observeMe": true, "observeOthers": true }  
          },  
          "dialecticReasoningLevel": "low",  
          "dialecticDynamic": true,  
          "dialecticCadence": 2,  
          "dialecticDepth": 1,  
          "dialecticMaxChars": 600,  
          "contextCadence": 1,  
          "messageMaxChars": 25000,  
          "saveMessages": true  
        },  
        "hermes.coder": {  
          "enabled": true,  
          "aiPeer": "coder",  
          "workspace": "hermes",  
          "peerName": "eri",  
          "recallMode": "tools",  
          "observation": {  
            "user": { "observeMe": true, "observeOthers": false },  
            "ai": { "observeMe": true, "observeOthers": true }  
          }  
        },  
        "hermes.writer": {  
          "enabled": true,  
          "aiPeer": "writer",  
          "workspace": "hermes",  
          "peerName": "eri"  
        }  
      },  
      "sessions": {  
        "/home/user/myproject": "myproject-main"  
      }  
    }  
    
[/code]
См. [справочник по конфигурации](<https://github.com/hermes-ai/hermes-agent/blob/main/plugins/memory/honcho/README.md>) и [руководство по интеграции Honcho](<https://docs.honcho.dev/v3/guides/integrations/hermes>).
* * *
### OpenViking[​](<#openviking> "Direct link to OpenViking")
Контекстная база данных от Volcengine (ByteDance) с иерархией знаний в стиле файловой системы, многоуровневым поиском и автоматическим извлечением памяти в 6 категорий.
|   
|---|---  
**Best for**|  Самостоятельно размещённое управление знаниями со структурированным просмотром  
**Requires**| `pip install openviking` + работающий сервер  
**Data storage**|  Самостоятельно размещённое (локально или в облаке)  
**Cost**|  Бесплатно (открытый исходный код, AGPL-3.0)  
**Tools:** `viking_search` (семантический поиск), `viking_read` (многоуровневый: абстракт/обзор/полный), `viking_browse` (навигация по файловой системе), `viking_remember` (сохранение фактов), `viking_add_resource` (загрузка URL/документов)
**Setup:**
[code] 
    # Сначала запустите сервер OpenViking  
    pip install openviking  
    openviking-server  
      
    # Затем настройте Hermes  
    hermes memory setup    # выберите "openviking"  
    # Или вручную:  
    hermes config set memory.provider openviking  
    echo "OPENVIKING_ENDPOINT=http://localhost:1933" >> ~/.hermes/.env  
    
[/code]
**Key features:**
  * Многоуровневая загрузка контекста: L0 (~100 токенов) → L1 (~2k) → L2 (полный)
  * Автоматическое извлечение памяти при завершении сессии (профиль, предпочтения, сущности, события, случаи, шаблоны)
  * Схема URI `viking://` для иерархического просмотра знаний


* * *
### Mem0[​](<#mem0> "Direct link to Mem0")
Серверное извлечение фактов LLM с семантическим поиском, переранжированием и автоматической дедупликацией.
|   
|---|---  
**Best for**|  Автоматическое управление памятью без вмешательства — Mem0 обрабатывает извлечение автоматически  
**Requires**| `pip install mem0ai` + API-ключ  
**Data storage**|  Mem0 Cloud  
**Cost**|  Цены Mem0  
**Tools:** `mem0_profile` (все сохранённые воспоминания), `mem0_search` (семантический поиск + переранжирование), `mem0_conclude` (сохранение дословных фактов)
**Setup:**
[code] 
    hermes memory setup    # выберите "mem0"  
    # Или вручную:  
    hermes config set memory.provider mem0  
    echo "MEM0_API_KEY=your-key" >> ~/.hermes/.env  
    
[/code]
**Config:** `$HERMES_HOME/mem0.json`
Key| Default| Description  
---|---|---|---  
`user_id`| `hermes-user`| Идентификатор пользователя  
`agent_id`| `hermes`| Идентификатор агента  
* * *
### Hindsight[​](<#hindsight> "Direct link to Hindsight")
Долговременная память с графом знаний, разрешением сущностей и многостратегическим поиском. Инструмент `hindsight_reflect` обеспечивает кросc-мемориальный синтез, который не предлагает ни один другой провайдер. Автоматически сохраняет полные шаги разговора (включая вызовы инструментов) с отслеживанием документов на уровне сессии.
|   
|---|---  
**Best for**|  Поиск на основе графа знаний с отношениями сущностей  
**Requires**|  Облако: API-ключ из [ui.hindsight.vectorize.io](<https://ui.hindsight.vectorize.io>). Локально: API-ключ LLM (OpenAI, Groq, OpenRouter и т.д.)  
**Data storage**|  Hindsight Cloud или локальный встроенный PostgreSQL  
**Cost**|  Цены Hindsight (облако) или бесплатно (локально)  
**Tools:** `hindsight_retain` (сохранение с извлечением сущностей), `hindsight_recall` (многостратегический поиск), `hindsight_reflect` (кросc-мемориальный синтез)
**Setup:**
[code] 
    hermes memory setup    # выберите "hindsight"  
    # Или вручную:  
    hermes config set memory.provider hindsight  
    echo "HINDSIGHT_API_KEY=your-key" >> ~/.hermes/.env  
    
[/code]
Мастер настройки устанавливает зависимости автоматически и устанавливает только то, что необходимо для выбранного режима (`hindsight-client` для облака, `hindsight-all` для локального). Требуется `hindsight-client >= 0.4.22` (автоматически обновляется при запуске сессии, если версия устарела).
**Local mode UI:** `hindsight-embed -p hermes ui start`
**Config:** `$HERMES_HOME/hindsight/config.json`
Key| Default| Description  
---|---|---|---  
`mode`| `cloud`| `cloud` или `local`  
`bank_id`| `hermes`| Идентификатор банка памяти  
`recall_budget`| `mid`| Тщательность поиска: `low` / `mid` / `high`  
`memory_mode`| `hybrid`| `hybrid` (контекст + инструменты), `context` (только автовнедрение), `tools` (только инструменты)  
`auto_retain`| `true`| Автоматически сохранять шаги разговора  
`auto_recall`| `true`| Автоматически извлекать воспоминания перед каждым шагом  
`retain_async`| `true`| Обрабатывать сохранение асинхронно на сервере  
`retain_context`| `conversation between Hermes Agent and the User`| Метка контекста для сохранённых воспоминаний  
`retain_tags`| —| Теги по умолчанию, применяемые к сохранённым воспоминаниям; объединяются с тегами из вызовов инструментов  
`retain_source`| —| Опционально `metadata.source`, прикрепляемый к сохранённым воспоминаниям  
`retain_user_prefix`| `User`| Метка перед шагами пользователя в автоматически сохраняемых транскриптах  
`retain_assistant_prefix`| `Assistant`| Метка перед шагами ассистента в автоматически сохраняемых транскриптах  
`recall_tags`| —| Теги для фильтрации при поиске  
См. [README плагина](<https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/hindsight/README.md>) для полного справочника по конфигурации.
* * *
### Holographic[​](<#holographic> "Direct link to Holographic")
Локальное хранилище фактов SQLite с полнотекстовым поиском FTS5, оценкой доверия и HRR (Holographic Reduced Representations) для композиционных алгебраических запросов.
|   
|---|---  
**Best for**|  Локальная память с расширенным поиском, без внешних зависимостей  
**Requires**|  Ничего (SQLite всегда доступен). NumPy опционально для HRR-алгебры.  
**Data storage**|  Локальный SQLite  
**Cost**|  Бесплатно  
**Tools:** `fact_store` (9 действий: add, search, probe, related, reason, contradict, update, remove, list), `fact_feedback` (оценка helpful/unhelpful, обучающая оценки доверия)
**Setup:**
[code] 
    hermes memory setup    # выберите "holographic"  
    # Или вручную:  
    hermes config set memory.provider holographic  
    
[/code]
**Config:** `config.yaml` в разделе `plugins.hermes-memory-store`
Key| Default| Description  
---|---|---|---  
`db_path`| `$HERMES_HOME/memory_store.db`| Путь к базе данных SQLite  
`auto_extract`| `false`| Автоматически извлекать факты по завершении сессии  
`default_trust`| `0.5`| Оценка доверия по умолчанию (0.0–1.0)  
**Unique capabilities:**
  * `probe` — алгебраический поиск по конкретной сущности (все факты о человеке/вещи)
  * `reason` — композиционные AND-запросы по нескольким сущностям
  * `contradict` — автоматическое обнаружение противоречащих фактов
  * Оценка доверия с асимметричной обратной связью (+0.05 helpful / -0.10 unhelpful)


* * *
### RetainDB[​](<#retaindb> "Direct link to RetainDB")
Облачное API памяти с гибридным поиском (Vector + BM25 + Reranking), 7 типами памяти и дельта-сжатием.
|   
|---|---  
**Best for**|  Команды, уже использующие инфраструктуру RetainDB  
**Requires**|  Аккаунт RetainDB + API-ключ  
**Data storage**|  RetainDB Cloud  
**Cost**|  $20/месяц  
**Tools:** `retaindb_profile` (профиль пользователя), `retaindb_search` (семантический поиск), `retaindb_context` (контекст, релевантный задаче), `retaindb_remember` (сохранение с типом + важностью), `retaindb_forget` (удаление воспоминаний)
**Setup:**
[code] 
    hermes memory setup    # выберите "retaindb"  
    # Или вручную:  
    hermes config set memory.provider retaindb  
    echo "RETAINDB_API_KEY=your-key" >> ~/.hermes/.env  
    
[/code]
* * *
### ByteRover[​](<#byterover> "Direct link to ByteRover")
Постоянная память через CLI `brv` — иерархическое дерево знаний с многоуровневым поиском (нечёткий текст → поиск через LLM). Локально-ориентированная с опциональной облачной синхронизацией.
|   
|---|---  
**Best for**|  Разработчики, которым нужна портативная локально-ориентированная память с CLI  
**Requires**|  ByteRover CLI (`npm install -g byterover-cli` или [скрипт установки](<https://byterover.dev>))  
**Data storage**|  Локально (по умолчанию) или ByteRover Cloud (опциональная синхронизация)  
**Cost**|  Бесплатно (локально) или цены ByteRover (облако)  
**Tools:** `brv_query` (поиск по дереву знаний), `brv_curate` (сохранение фактов/решений/шаблонов), `brv_status` (версия CLI + статистика дерева)
**Setup:**
[code] 
    # Сначала установите CLI  
    curl -fsSL https://byterover.dev/install.sh | sh  
      
    # Затем настройте Hermes  
    hermes memory setup    # выберите "byterover"  
    # Или вручную:  
    hermes config set memory.provider byterover  
    
[/code]
**Key features:**
  * Автоматическое извлечение до сжатия (сохраняет инсайты до того, как сжатие контекста их отбросит)
  * Дерево знаний хранится в `$HERMES_HOME/byterover/` (в рамках профиля)
  * SOC2 Type II сертифицированная облачная синхронизация (опционально)


* * *
### Supermemory[​](<#supermemory> "Direct link to Supermemory")
Семантическая долговременная память с поиском по профилю, семантическим поиском, явными инструментами памяти и загрузкой разговора по завершении сессии через графовое API Supermemory.
|   
|---|---  
**Best for**|  Семантический поиск с профилированием пользователя и построением графа на уровне сессии  
**Requires**| `pip install supermemory` + [API key](<https://supermemory.ai>)  
**Data storage**|  Supermemory Cloud  
**Cost**|  Цены Supermemory  
**Tools:** `supermemory_store` (сохранение явных воспоминаний), `supermemory_search` (поиск по семантическому сходству), `supermemory_forget` (забыть по ID или по запросу наилучшего соответствия), `supermemory_profile` (постоянный профиль + недавний контекст)
**Setup:**
[code] 
    hermes memory setup    # выберите "supermemory"  
    # Или вручную:  
    hermes config set memory.provider supermemory  
    echo 'SUPERMEMORY_API_KEY=***' >> ~/.hermes/.env  
    
[/code]
**Config:** `$HERMES_HOME/supermemory.json`
Key| Default| Description  
---|---|---|---  
`container_tag`| `hermes`| Тег контейнера, используемый для поиска и записи. Поддерживает шаблон `{identity}` для тегов в рамках профиля.  
`auto_recall`| `true`| Внедрять релевантный контекст памяти перед шагами  
`auto_capture`| `true`| Сохранять очищенные шаги пользователь-ассистент после каждого ответа  
`max_recall_results`| `10`| Максимум извлечённых элементов для форматирования в контекст  
`profile_frequency`| `50`| Включать факты профиля на первом шаге и каждые N шагов  
`capture_mode`| `all`| Пропускать крошечные или тривиальные шаги по умолчанию  
`search_mode`| `hybrid`| Режим поиска: `hybrid`, `memories` или `documents`  
`api_timeout`| `5.0`| Тайм-аут для SDK и запросов загрузки  
**Environment variables:** `SUPERMEMORY_API_KEY` (обязательно), `SUPERMEMORY_CONTAINER_TAG` (переопределяет конфигурацию).
**Key features:**
  * Автоматическое ограждение контекста — удаляет извлечённые воспоминания из захваченных шагов для предотвращения рекурсивного загрязнения памяти
  * Загрузка разговора по завершении сессии для более богатого построения знаний на уровне графа
  * Факты профиля внедряются на первом шаге и с настраиваемыми интервалами
  * Фильтрация тривиальных сообщений (пропускает "ok", "thanks" и т.д.)
  * **Контейнеры в рамках профиля** — используйте `{identity}` в `container_tag` (например, `hermes-{identity}` → `hermes-coder`) для изоляции воспоминаний по профилю Hermes
  * **Многоконтейнерный режим** — включите `enable_custom_container_tags` со списком `custom_containers`, чтобы агент мог читать/записывать в именованные контейнеры. Автоматические операции (синхронизация, предзагрузка) остаются в основном контейнере.

Multi-container example
[code]
    {  
      "container_tag": "hermes",  
      "enable_custom_container_tags": true,  
      "custom_containers": ["project-alpha", "shared-knowledge"],  
      "custom_container_instructions": "Используйте project-alpha для контекста программирования."  
    }  
    
[/code]
**Support:** [Discord](<https://supermemory.link/discord>) · [support@supermemory.com](<mailto:support@supermemory.com>)
* * *
## Provider Comparison[​](<#provider-comparison> "Direct link to Provider Comparison")
Provider| Storage| Cost| Tools| Dependencies| Unique Feature  
---|---|---|---|---|---  
**Honcho**|  Cloud| Paid| 5| `honcho-ai`| Диалектическое моделирование пользователя + контекст в рамках сессии  
**OpenViking**|  Self-hosted| Free| 5| `openviking` + server| Иерархия файловой системы + многоуровневая загрузка  
**Mem0**|  Cloud| Paid| 3| `mem0ai`| Серверное извлечение LLM  
**Hindsight**|  Cloud/Local| Free/Paid| 3| `hindsight-client`| Граф знаний + синтез reflect  
**Holographic**|  Local| Free| 2| None| HRR-алгебра + оценка доверия  
**RetainDB**|  Cloud| $20/mo| 5| `requests`| Дельта-сжатие  
**ByteRover**|  Local/Cloud| Free/Paid| 3| `brv` CLI| Извлечение до сжатия  
**Supermemory**|  Cloud| Paid| 4| `supermemory`| Ограждение контекста + загрузка сессионного графа + мультиконтейнер  
## Profile Isolation[​](<#profile-isolation> "Direct link to Profile Isolation")
Данные каждого провайдера изолированы по [профилю](</docs/user-guide/profiles>):
  * **Провайдеры локального хранения** (Holographic, ByteRover) используют пути `$HERMES_HOME/`, которые различаются для каждого профиля
  * **Провайдеры файлов конфигурации** (Honcho, Mem0, Hindsight, Supermemory) хранят конфигурацию в `$HERMES_HOME/`, поэтому каждый профиль имеет свои собственные учётные данные
  * **Облачные провайдеры** (RetainDB) автоматически формируют имена проектов с учётом профиля
  * **Провайдеры переменных окружения** (OpenViking) настраиваются через файл `.env` каждого профиля


## Building a Memory Provider[​](<#building-a-memory-provider> "Direct link to Building a Memory Provider")
См. [Руководство разработчика: Плагины провайдеров памяти](</docs/developer-guide/memory-provider-plugin>) для создания собственного провайдера.
  * [Quick Start](<#quick-start>)
  * [How It Works](<#how-it-works>)
  * [Available Providers](<#available-providers>)
    * [Honcho](<#honcho>)
    * [New profile, fresh Honcho peer](<#new-profile-fresh-honcho-peer>)
    * [Existing profiles, backfill Honcho peers](<#existing-profiles-backfill-honcho-peers>)
    * [Per-profile observation](<#per-profile-observation>)
    * [OpenViking](<#openviking>)
    * [Mem0](<#mem0>)
    * [Hindsight](<#hindsight>)
    * [Holographic](<#holographic>)
    * [RetainDB](<#retaindb>)
    * [ByteRover](<#byterover>)
    * [Supermemory](<#supermemory>)
  * [Provider Comparison](<#provider-comparison>)
  * [Profile Isolation](<#profile-isolation>)
  * [Building a Memory Provider](<#building-a-memory-provider>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers -->
