На этой странице
Hermes Agent использует базу данных SQLite (`~/.hermes/state.db`) для хранения метаданных сессий, полной истории сообщений и конфигурации моделей в CLI- и gateway-сессиях. Это заменяет прежний подход с отдельными JSONL-файлами на сессию.
Исходный файл: `hermes_state.py`
## Обзор архитектуры[​](<#architecture-overview> "Прямая ссылка на Обзор архитектуры")
[code] 
    ~/.hermes/state.db (SQLite, WAL mode)  
    ├── sessions              — Метаданные сессии, количество токенов, биллинг
    ├── messages              — Полная история сообщений по каждой сессии
    ├── messages_fts          — FTS5 виртуальная таблица (content + tool_name + tool_calls)
    ├── messages_fts_trigram  — FTS5 виртуальная таблица с триграммным токенизатором (CJK / поиск по подстроке)
    ├── state_meta            — Таблица метаданных ключ/значение
    └── schema_version        — Таблица с одной строкой, отслеживающая состояние миграций
    
[/code]
Ключевые проектные решения:
  * **Режим WAL** для конкурентных читателей + один писатель (мультиплатформенный gateway)
  * **FTS5 виртуальная таблица** для быстрого полнотекстового поиска по всем сообщениям сессий
  * **Линейка сессий** через цепочки `parent_session_id` (разделение при сжатии контекста)
  * **Маркировка источника** (`cli`, `telegram`, `discord` и т.д.) для фильтрации по платформе
  * Batch-раннер и RL-траектории НЕ хранятся здесь (отдельные системы)


## Схема SQLite[​](<#sqlite-schema> "Прямая ссылка на Схему SQLite")
### Таблица Sessions[​](<#sessions-table> "Прямая ссылка на Таблицу Sessions")
[code] 
    CREATE TABLE IF NOT EXISTS sessions (  
        id TEXT PRIMARY KEY,  
        source TEXT NOT NULL,  
        user_id TEXT,  
        model TEXT,  
        model_config TEXT,  
        system_prompt TEXT,  
        parent_session_id TEXT,  
        started_at REAL NOT NULL,  
        ended_at REAL,  
        end_reason TEXT,  
        message_count INTEGER DEFAULT 0,  
        tool_call_count INTEGER DEFAULT 0,  
        input_tokens INTEGER DEFAULT 0,  
        output_tokens INTEGER DEFAULT 0,  
        cache_read_tokens INTEGER DEFAULT 0,  
        cache_write_tokens INTEGER DEFAULT 0,  
        reasoning_tokens INTEGER DEFAULT 0,  
        billing_provider TEXT,  
        billing_base_url TEXT,  
        billing_mode TEXT,  
        estimated_cost_usd REAL,  
        actual_cost_usd REAL,  
        cost_status TEXT,  
        cost_source TEXT,  
        pricing_version TEXT,  
        title TEXT,  
        api_call_count INTEGER DEFAULT 0,  
        FOREIGN KEY (parent_session_id) REFERENCES sessions(id)  
    );  
      
    CREATE INDEX IF NOT EXISTS idx_sessions_source ON sessions(source);  
    CREATE INDEX IF NOT EXISTS idx_sessions_parent ON sessions(parent_session_id);  
    CREATE INDEX IF NOT EXISTS idx_sessions_started ON sessions(started_at DESC);  
    CREATE UNIQUE INDEX IF NOT EXISTS idx_sessions_title_unique  
        ON sessions(title) WHERE title IS NOT NULL;  
    
[/code]
### Таблица Messages[​](<#messages-table> "Прямая ссылка на Таблицу Messages")
[code] 
    CREATE TABLE IF NOT EXISTS messages (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        session_id TEXT NOT NULL REFERENCES sessions(id),  
        role TEXT NOT NULL,  
        content TEXT,  
        tool_call_id TEXT,  
        tool_calls TEXT,  
        tool_name TEXT,  
        timestamp REAL NOT NULL,  
        token_count INTEGER,  
        finish_reason TEXT,  
        reasoning TEXT,  
        reasoning_content TEXT,  
        reasoning_details TEXT,  
        codex_reasoning_items TEXT,  
        codex_message_items TEXT  
    );  
      
    CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, timestamp);  
    
[/code]
Примечания:
  * `tool_calls` хранится как JSON-строка (сериализованный список объектов вызовов инструментов)
  * `reasoning_details`, `codex_reasoning_items` и `codex_message_items` хранятся как JSON-строки
  * `reasoning` хранит сырой текст рассуждений для провайдеров, которые его раскрывают
  * Метки времени — числа с плавающей точкой Unix epoch (`time.time()`)


### FTS5 Полнотекстовый поиск[​](<#fts5-full-text-search> "Прямая ссылка на FTS5 Полнотекстовый поиск")
[code] 
    CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(  
        content,  
        content=messages,  
        content_rowid=id  
    );  
    
[/code]
FTS5-таблица синхронизируется с помощью трёх триггеров, срабатывающих при INSERT, UPDATE и DELETE в таблице `messages`:
[code] 
    CREATE TRIGGER IF NOT EXISTS messages_fts_insert AFTER INSERT ON messages BEGIN  
        INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);  
    END;  
      
    CREATE TRIGGER IF NOT EXISTS messages_fts_delete AFTER DELETE ON messages BEGIN  
        INSERT INTO messages_fts(messages_fts, rowid, content)  
            VALUES('delete', old.id, old.content);  
    END;  
      
    CREATE TRIGGER IF NOT EXISTS messages_fts_update AFTER UPDATE ON messages BEGIN  
        INSERT INTO messages_fts(messages_fts, rowid, content)  
            VALUES('delete', old.id, old.content);  
        INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);  
    END;  
    
[/code]
## Версия схемы и миграции[​](<#schema-version-and-migrations> "Прямая ссылка на Версию схемы и миграции")
Текущая версия схемы: **11**
Таблица `schema_version` хранит одно целое число. Простые добавления столбцов обрабатываются декларативно с помощью `_reconcile_columns()` (которая сравнивает текущие столбцы с `SCHEMA_SQL` и ADD-ит недостающие). Цепочка с привязкой к версии зарезервирована для миграций данных и изменений индексов/FTS, которые нельзя выразить декларативно:
Версия| Изменение  
---|---  
1| Начальная схема (sessions, messages, FTS5)  
2| Добавлен столбец `finish_reason` в messages  
3| Добавлен столбец `title` в sessions  
4| Добавлен уникальный индекс по `title` (NULL разрешены, не-NULL должны быть уникальны)  
5| Добавлены столбцы биллинга: `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `billing_provider`, `billing_base_url`, `billing_mode`, `estimated_cost_usd`, `actual_cost_usd`, `cost_status`, `cost_source`, `pricing_version`  
6| Добавлены столбцы рассуждений в messages: `reasoning`, `reasoning_details`, `codex_reasoning_items`  
7| Добавлен столбец `reasoning_content` в messages  
8| Добавлен столбец `api_call_count` в sessions  
9| Добавлен столбец `codex_message_items` в messages для воспроизведения id/фазы ответов Codex  
10| Добавлена виртуальная таблица `messages_fts_trigram` (триграммный токенизатор для CJK / поиск по подстроке) и обратное заполнение существующих строк  
11| Переиндексация `messages_fts` и `messages_fts_trigram` для покрытия `tool_name` + `tool_calls` и переключение с режима external-content на inline; удаление старых триггеров и обратное заполнение каждой строки сообщений  
Декларативные добавления столбцов используют `ALTER TABLE ADD COLUMN`, обёрнутый в try/except для обработки случая, когда столбец уже существует (идемпотентность). Номер версии увеличивается после каждого успешного блока миграции.
## Обработка конкурентной записи[​](<#write-contention-handling> "Прямая ссылка на Обработку конкурентной записи")
Несколько процессов Hermes (gateway + CLI-сессии + worktree-агенты) используют один `state.db`. Класс `SessionDB` обрабатывает конкурентную запись с помощью:
  * **Короткий таймаут SQLite** (1 секунда) вместо стандартных 30 с
  * **Повторные попытки на уровне приложения** со случайной задержкой (20–150 мс, до 15 повторений)
  * **Транзакции BEGIN IMMEDIATE** для выявления конфликтов блокировки в начале транзакции
  * **Периодические контрольные точки WAL** каждые 50 успешных записей (режим PASSIVE)


Это позволяет избежать «эффекта конвоя», когда детерминированная внутренняя задержка SQLite заставляет всех конкурирующих писателей повторять попытки с одинаковыми интервалами.
[code] 
    _WRITE_MAX_RETRIES = 15  
    _WRITE_RETRY_MIN_S = 0.020   # 20ms  
    _WRITE_RETRY_MAX_S = 0.150   # 150ms  
    _CHECKPOINT_EVERY_N_WRITES = 50  
    
[/code]
## Типовые операции[​](<#common-operations> "Прямая ссылка на Типовые операции")
### Инициализация[​](<#initialize> "Прямая ссылка на Инициализацию")
[code] 
    from hermes_state import SessionDB  
      
    db = SessionDB()                           # По умолчанию: ~/.hermes/state.db  
    db = SessionDB(db_path=Path("/tmp/test.db"))  # Свой путь  
    
[/code]
### Создание и управление сессиями[​](<#create-and-manage-sessions> "Прямая ссылка на Создание и управление сессиями")
[code] 
    # Создание новой сессии  
    db.create_session(  
        session_id="sess_abc123",  
        source="cli",  
        model="anthropic/claude-sonnet-4.6",  
        user_id="user_1",  
        parent_session_id=None,  # или ID предыдущей сессии для lineage  
    )  
      
    # Завершение сессии  
    db.end_session("sess_abc123", end_reason="user_exit")  
      
    # Переоткрытие сессии (очистка ended_at/end_reason)  
    db.reopen_session("sess_abc123")  
    
[/code]
### Сохранение сообщений[​](<#store-messages> "Прямая ссылка на Сохранение сообщений")
[code] 
    msg_id = db.append_message(  
        session_id="sess_abc123",  
        role="assistant",  
        content="Вот ответ...",  
        tool_calls=[{"id": "call_1", "function": {"name": "terminal", "arguments": "{}"}}],  
        token_count=150,  
        finish_reason="stop",  
        reasoning="Давайте подумаем об этом...",  
    )  
    
[/code]
### Получение сообщений[​](<#retrieve-messages> "Прямая ссылка на Получение сообщений")
[code] 
    # Сырые сообщения со всеми метаданными  
    messages = db.get_messages("sess_abc123")  
      
    # Формат разговора OpenAI (для воспроизведения через API)  
    conversation = db.get_messages_as_conversation("sess_abc123")  
    # Возвращает: [{"role": "user", "content": "..."}, {"role": "assistant", ...}]  
    
[/code]
### Названия сессий[​](<#session-titles> "Прямая ссылка на Названия сессий")
[code] 
    # Установка названия (должно быть уникальным среди не-NULL названий)  
    db.set_session_title("sess_abc123", "Fix Docker Build")  
      
    # Поиск по названию (возвращает самую последнюю в линейке)  
    session_id = db.resolve_session_by_title("Fix Docker Build")  
      
    # Автоматическая генерация следующего названия в линейке  
    next_title = db.get_next_title_in_lineage("Fix Docker Build")  
    # Возвращает: "Fix Docker Build #2"  
    
[/code]
## Полнотекстовый поиск[​](<#full-text-search> "Прямая ссылка на Полнотекстовый поиск")
Метод `search_messages()` поддерживает синтаксис запросов FTS5 с автоматической санитазацией пользовательского ввода.
### Базовый поиск[​](<#basic-search> "Прямая ссылка на Базовый поиск")
[code] 
    results = db.search_messages("docker deployment")  
    
[/code]
### Синтаксис запросов FTS5[​](<#fts5-query-syntax> "Прямая ссылка на Синтаксис запросов FTS5")
Синтаксис| Пример| Значение  
---|---|---  
Ключевые слова| `docker deployment`| Оба термина (неявное AND)  
Фраза в кавычках| `"exact phrase"`| Точное совпадение фразы  
Логическое OR| `docker OR kubernetes`| Любой из терминов  
Логическое NOT| `python NOT java`| Исключить термин  
Префикс| `deploy*`| Поиск по префиксу  
### Фильтрованный поиск[​](<#filtered-search> "Прямая ссылка на Фильтрованный поиск")
[code] 
    # Поиск только по CLI-сессиям  
    results = db.search_messages("error", source_filter=["cli"])  
      
    # Исключение gateway-сессий  
    results = db.search_messages("bug", exclude_sources=["telegram", "discord"])  
      
    # Поиск только по сообщениям пользователя  
    results = db.search_messages("help", role_filter=["user"])  
    
[/code]
### Формат результатов поиска[​](<#search-results-format> "Прямая ссылка на Формат результатов поиска")
Каждый результат включает:
  * `id`, `session_id`, `role`, `timestamp`
  * `snippet` — сгенерированный FTS5 сниппет с маркерами `>>>match<<<`
  * `context` — 1 сообщение до и после совпадения (содержимое усечено до 200 символов)
  * `source`, `model`, `session_started` — от родительской сессии


Метод `_sanitize_fts5_query()` обрабатывает граничные случаи:
  * Удаляет незакрытые кавычки и специальные символы
  * Оборачивает дефисные термины в кавычки (`chat-send` → `"chat-send"`)
  * Удаляет висячие логические операторы (`hello AND` → `hello`)


## Линейка сессий[​](<#session-lineage> "Прямая ссылка на Линейку сессий")
Сессии могут образовывать цепочки через `parent_session_id`. Это происходит, когда сжатие контекста вызывает разделение сессии в gateway.
### Запрос: Найти линейку сессии[​](<#query-find-session-lineage> "Прямая ссылка на Запрос: Найти линейку сессии")
[code] 
    -- Найти всех предков сессии  
    WITH RECURSIVE lineage AS (  
        SELECT * FROM sessions WHERE id = ?  
        UNION ALL  
        SELECT s.* FROM sessions s  
        JOIN lineage l ON s.id = l.parent_session_id  
    )  
    SELECT id, title, started_at, parent_session_id FROM lineage;  
      
    -- Найти всех потомков сессии  
    WITH RECURSIVE descendants AS (  
        SELECT * FROM sessions WHERE id = ?  
        UNION ALL  
        SELECT s.* FROM sessions s  
        JOIN descendants d ON s.parent_session_id = d.id  
    )  
    SELECT id, title, started_at FROM descendants;  
    
[/code]
### Запрос: Последние сессии с превью[​](<#query-recent-sessions-with-preview> "Прямая ссылка на Запрос: Последние сессии с превью")
[code] 
    SELECT s.*,  
        COALESCE(  
            (SELECT SUBSTR(m.content, 1, 63)  
             FROM messages m  
             WHERE m.session_id = s.id AND m.role = 'user' AND m.content IS NOT NULL  
             ORDER BY m.timestamp, m.id LIMIT 1),  
            ''  
        ) AS preview,  
        COALESCE(  
            (SELECT MAX(m2.timestamp) FROM messages m2 WHERE m2.session_id = s.id),  
            s.started_at  
        ) AS last_active  
    FROM sessions s  
    ORDER BY s.started_at DESC  
    LIMIT 20;  
    
[/code]
### Запрос: Статистика использования токенов[​](<#query-token-usage-statistics> "Прямая ссылка на Запрос: Статистика использования токенов")
[code] 
    -- Всего токенов по моделям  
    SELECT model,  
           COUNT(*) as session_count,  
           SUM(input_tokens) as total_input,  
           SUM(output_tokens) as total_output,  
           SUM(estimated_cost_usd) as total_cost  
    FROM sessions  
    WHERE model IS NOT NULL  
    GROUP BY model  
    ORDER BY total_cost DESC;  
      
    -- Сессии с наибольшим использованием токенов  
    SELECT id, title, model, input_tokens + output_tokens AS total_tokens,  
           estimated_cost_usd  
    FROM sessions  
    ORDER BY total_tokens DESC  
    LIMIT 10;  
    
[/code]
## Экспорт и очистка[​](<#export-and-cleanup> "Прямая ссылка на Экспорт и очистку")
[code] 
    # Экспорт одной сессии с сообщениями  
    data = db.export_session("sess_abc123")  
      
    # Экспорт всех сессий (с сообщениями) в виде списка словарей  
    all_data = db.export_all(source="cli")  
      
    # Удаление старых сессий (только завершённые)  
    deleted_count = db.prune_sessions(older_than_days=90)  
    deleted_count = db.prune_sessions(older_than_days=30, source="telegram")  
      
    # Очистка сообщений, но сохранение записи о сессии  
    db.clear_messages("sess_abc123")  
      
    # Удаление сессии и всех сообщений  
    db.delete_session("sess_abc123")  
    
[/code]
## Расположение базы данных[​](<#database-location> "Прямая ссылка на Расположение базы данных")
Путь по умолчанию: `~/.hermes/state.db`
Этот путь определяется из `hermes_constants.get_hermes_home()`, которая по умолчанию возвращает `~/.hermes/`, или значение переменной окружения `HERMES_HOME`.
Файл базы данных, WAL-файл (`state.db-wal`) и файл разделяемой памяти (`state.db-shm`) создаются в одном каталоге.
  * [Обзор архитектуры](<#architecture-overview>)
  * [Схема SQLite](<#sqlite-schema>)
    * [Таблица Sessions](<#sessions-table>)
    * [Таблица Messages](<#messages-table>)
    * [FTS5 Полнотекстовый поиск](<#fts5-full-text-search>)
  * [Версия схемы и миграции](<#schema-version-and-migrations>)
  * [Обработка конкурентной записи](<#write-contention-handling>)
  * [Типовые операции](<#common-operations>)
    * [Инициализация](<#initialize>)
    * [Создание и управление сессиями](<#create-and-manage-sessions>)
    * [Сохранение сообщений](<#store-messages>)
    * [Получение сообщений](<#retrieve-messages>)
    * [Названия сессий](<#session-titles>)
  * [Полнотекстовый поиск](<#full-text-search>)
    * [Базовый поиск](<#basic-search>)
    * [Синтаксис запросов FTS5](<#fts5-query-syntax>)
    * [Фильтрованный поиск](<#filtered-search>)
    * [Формат результатов поиска](<#search-results-format>)
  * [Линейка сессий](<#session-lineage>)
    * [Запрос: Найти линейку сессии](<#query-find-session-lineage>)
    * [Запрос: Последние сессии с превью](<#query-recent-sessions-with-preview>)
    * [Запрос: Статистика использования токенов](<#query-token-usage-statistics>)
  * [Экспорт и очистка](<#export-and-cleanup>)
  * [Расположение базы данных](<#database-location>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage -->
