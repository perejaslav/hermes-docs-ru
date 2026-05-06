On this page
Поиск по личным базам знаний, заметкам, документам и стенограммам встреч локально с помощью qmd — гибридного поискового движка с BM25, векторным поиском и переранжированием через LLM. Поддерживает CLI и интеграцию с MCP.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")

|---|---  
|Source| Optional — install with `hermes skills install official/research/qmd`  
|Path| `optional-skills/research/qmd`  
|Version| `1.0.0`  
|Author| Hermes Agent + Teknium  
|License| MIT  
|Platforms| macos, linux  
|Tags| `Search`, `Knowledge-Base`, `RAG`, `Notes`, `MCP`, `Local-AI`  
|Related skills| [`obsidian`](</docs/user-guide/skills/bundled/note-taking/note-taking-obsidian>), [`native-mcp`](</docs/user-guide/skills/bundled/mcp/mcp-native-mcp>), [`arxiv`](</docs/user-guide/skills/bundled/research/research-arxiv>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# QMD — Query Markup Documents
Локальный поисковый движок на устройстве для личных баз знаний. Индексирует markdown-заметки, стенограммы встреч, документацию и любые текстовые файлы, затем предоставляет гибридный поиск, сочетающий поиск по ключевым словам, семантическое понимание и переранжирование на базе LLM — всё работает локально, без облачных зависимостей.
Создан [Tobi Lütke](<https://github.com/tobi/qmd>). Лицензия MIT.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь просит найти что-то в своих заметках, документах, базе знаний или стенограммах встреч
  * Пользователь хочет найти информацию в большой коллекции markdown/текстовых файлов
  * Пользователь хочет семантический поиск («найди заметки о концепции X»), а не просто grep по ключевым словам
  * Пользователь уже настроил коллекции qmd и хочет выполнять по ним запросы
  * Пользователь просит настроить локальную базу знаний или систему поиска по документам
  * Ключевые слова: «поиск в заметках», «найти в документах», «база знаний», «qmd»


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
### Node.js >= 22 (required)[​](<#nodejs--22-required> "Direct link to Node.js >= 22 \(required\)")
[code] 
    # Проверка версии  
    node --version  # должно быть >= 22  
      
    # macOS — установка или обновление через Homebrew  
    brew install node@22  
      
    # Linux — используйте NodeSource или nvm  
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -  
    sudo apt-get install -y nodejs  
    # или с помощью nvm:  
    nvm install 22 && nvm use 22  
    
[/code]
### SQLite with Extension Support (macOS only)[​](<#sqlite-with-extension-support-macos-only> "Direct link to SQLite with Extension Support \(macOS only\)")
Системный SQLite на macOS не поддерживает загрузку расширений. Установите через Homebrew:
[code] 
    brew install sqlite  
    
[/code]
### Install qmd[​](<#install-qmd> "Direct link to Install qmd")
[code] 
    npm install -g @tobilu/qmd  
    # или с помощью Bun:  
    bun install -g @tobilu/qmd  
    
[/code]
При первом запуске автоматически загружаются 3 локальные GGUF-модели (~2 ГБ в сумме):
Model| Purpose| Size  
---|---|---|---  
embeddinggemma-300M-Q8_0| Векторные эмбеддинги| ~300 МБ  
qwen3-reranker-0.6b-q8_0| Переранжирование результатов| ~640 МБ  
qmd-query-expansion-1.7B| Расширение запросов| ~1,1 ГБ  
### Verify Installation[​](<#verify-installation> "Direct link to Verify Installation")
[code] 
    qmd --version  
    qmd status  
    
[/code]
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
Command| What It Does| Speed  
---|---|---|---  
`qmd search "query"`| Поиск по ключевым словам BM25 (без моделей)| ~0,2 с  
`qmd vsearch "query"`| Семантический векторный поиск (1 модель)| ~3 с  
`qmd query "query"`| Гибридный поиск + переранжирование (все 3 модели)| ~2-3 с в тёплом режиме, ~19 с в холодном  
`qmd get <docid>`| Получение полного содержимого документа| мгновенно  
`qmd multi-get "glob"`| Получение нескольких файлов| мгновенно  
`qmd collection add <path> --name <n>`| Добавление директории как коллекции| мгновенно  
`qmd context add <path> "description"`| Добавление контекстных метаданных для улучшения поиска| мгновенно  
`qmd embed`| Генерация/обновление векторных эмбеддингов| зависит от объёма  
`qmd status`| Показ состояния индекса и информации о коллекциях| мгновенно  
`qmd mcp`| Запуск MCP-сервера (stdio)| постоянно  
`qmd mcp --http --daemon`| Запуск MCP-сервера (HTTP, модели в тёплом состоянии)| постоянно  
## Setup Workflow[​](<#setup-workflow> "Direct link to Setup Workflow")
### 1\\. Add Collections[​](<#1-add-collections> "Direct link to 1. Add Collections")
Укажите qmd директории, содержащие ваши документы:
[code] 
    # Добавление директории с заметками  
    qmd collection add ~/notes --name notes  
      
    # Добавление проектной документации  
    qmd collection add ~/projects/myproject/docs --name project-docs  
      
    # Добавление стенограмм встреч  
    qmd collection add ~/meetings --name meetings  
      
    # Список всех коллекций  
    qmd collection list  
    
[/code]
### 2\\. Add Context Descriptions[​](<#2-add-context-descriptions> "Direct link to 2. Add Context Descriptions")
Контекстные метаданные помогают поисковому движку понять, что содержит каждая коллекция. Это значительно улучшает качество поиска:
[code] 
    qmd context add qmd://notes "Personal notes, ideas, and journal entries"  
    qmd context add qmd://project-docs "Technical documentation for the main project"  
    qmd context add qmd://meetings "Meeting transcripts and action items from team syncs"  
    
[/code]
### 3\\. Generate Embeddings[​](<#3-generate-embeddings> "Direct link to 3. Generate Embeddings")
[code] 
    qmd embed  
    
[/code]
Это обрабатывает все документы во всех коллекциях и генерирует векторные эмбеддинги. Повторно запускайте после добавления новых документов или коллекций.
### 4\\. Verify[​](<#4-verify> "Direct link to 4. Verify")
[code] 
    qmd status   # показывает состояние индекса, статистику коллекций, информацию о моделях  
    
[/code]
## Search Patterns[​](<#search-patterns> "Direct link to Search Patterns")
### Fast Keyword Search (BM25)[​](<#fast-keyword-search-bm25> "Direct link to Fast Keyword Search \(BM25\)")
Лучше всего подходит для: точных терминов, идентификаторов кода, имён, известных фраз. Модели не загружаются — результаты практически мгновенные.
[code] 
    qmd search "authentication middleware"  
    qmd search "handleError async"  
    
[/code]
### Semantic Vector Search[​](<#semantic-vector-search> "Direct link to Semantic Vector Search")
Лучше всего подходит для: вопросов на естественном языке, концептуальных запросов. Загружает модель эмбеддингов (~3 с на первый запрос).
[code] 
    qmd vsearch "how does the rate limiter handle burst traffic"  
    qmd vsearch "ideas for improving onboarding flow"  
    
[/code]
### Hybrid Search with Reranking (Best Quality)[​](<#hybrid-search-with-reranking-best-quality> "Direct link to Hybrid Search with Reranking \(Best Quality\)")
Лучше всего подходит для: важных запросов, где качество важнее всего. Использует все 3 модели — расширение запроса, параллельный BM25+векторный поиск, переранжирование.
[code] 
    qmd query "what decisions were made about the database migration"  
    
[/code]
### Structured Multi-Mode Queries[​](<#structured-multi-mode-queries> "Direct link to Structured Multi-Mode Queries")
Комбинируйте разные типы поиска в одном запросе для точности:
[code] 
    # BM25 для точного термина + векторный для концепции  
    qmd query $'lex: rate limiter\nvec: how does throttling work under load'  
      
    # С расширением запроса  
    qmd query $'expand: database migration plan\nlex: "schema change"'  
    
[/code]
### Query Syntax (lex/BM25 mode)[​](<#query-syntax-lexbm25-mode> "Direct link to Query Syntax \(lex/BM25 mode\)")
Syntax| Effect| Example  
---|---|---|---  
`term`| Префиксное совпадение| `perf` совпадает с «performance»  
`"phrase"`| Точная фраза| `"rate limiter"`  
`-term`| Исключить термин| `performance -sports`  
### HyDE (Hypothetical Document Embeddings)[​](<#hyde-hypothetical-document-embeddings> "Direct link to HyDE \(Hypothetical Document Embeddings\)")
Для сложных тем напишите, как, по вашему мнению, должен выглядеть ответ:
[code] 
    qmd query $'hyde: The migration plan involves three phases. First, we add the new columns without dropping the old ones. Then we backfill data. Finally we cut over and remove legacy columns.'  
    
[/code]
### Scoping to Collections[​](<#scoping-to-collections> "Direct link to Scoping to Collections")
[code] 
    qmd search "query" --collection notes  
    qmd query "query" --collection project-docs  
    
[/code]
### Output Formats[​](<#output-formats> "Direct link to Output Formats")
[code] 
    qmd search "query" --json        # JSON-вывод (лучше всего для парсинга)  
    qmd search "query" --limit 5     # Ограничение результатов  
    qmd get "#abc123"                # Получение по ID документа  
    qmd get "path/to/file.md"       # Получение по пути к файлу  
    qmd get "file.md:50" -l 100     # Получение конкретного диапазона строк  
    qmd multi-get "journals/*.md" --json  # Пакетное получение по glob-шаблону  
    
[/code]
## MCP Integration (Recommended)[​](<#mcp-integration-recommended> "Direct link to MCP Integration \(Recommended\)")
qmd предоставляет MCP-сервер, который даёт инструменты поиска напрямую агенту Hermes через встроенный MCP-клиент. Это предпочтительный способ интеграции — после настройки агент получает инструменты qmd автоматически, без необходимости загружать этот навык.
### Option A: Stdio Mode (Simple)[​](<#option-a-stdio-mode-simple> "Direct link to Option A: Stdio Mode \(Simple\)")
Добавьте в `~/.hermes/config.yaml`:
[code] 
    mcp_servers:  
      qmd:  
        command: "qmd"  
        args: ["mcp"]  
        timeout: 30  
        connect_timeout: 45  
    
[/code]
Это регистрирует инструменты: `mcp_qmd_search`, `mcp_qmd_vsearch`, `mcp_qmd_deep_search`, `mcp_qmd_get`, `mcp_qmd_status`.
**Компромисс:** Модели загружаются при первом поисковом запросе (~19 с холодный старт), затем остаются в памяти на время сессии. Приемлемо для периодического использования.
### Option B: HTTP Daemon Mode (Fast, Recommended for Heavy Use)[​](<#option-b-http-daemon-mode-fast-recommended-for-heavy-use> "Direct link to Option B: HTTP Daemon Mode \(Fast, Recommended for Heavy Use\)")
Запустите демон qmd отдельно — он держит модели в памяти в тёплом состоянии:
[code] 
    # Запуск демона (сохраняется между перезапусками агента)  
    qmd mcp --http --daemon  
      
    # По умолчанию работает на http://localhost:8181  
    
[/code]
Затем настройте Hermes Agent на подключение через HTTP:
[code] 
    mcp_servers:  
      qmd:  
        url: "http://localhost:8181/mcp"  
        timeout: 30  
    
[/code]
**Компромисс:** Использует ~2 ГБ ОЗУ во время работы, но каждый запрос быстрый (~2-3 с). Лучше всего для пользователей, которые часто ищут.
### Keeping the Daemon Running[​](<#keeping-the-daemon-running> "Direct link to Keeping the Daemon Running")
#### macOS (launchd)[​](<#macos-launchd> "Direct link to macOS \(launchd\)")
[code] 
    cat > ~/Library/LaunchAgents/com.qmd.daemon.plist << 'EOF'  
    <?xml version="1.0" encoding="UTF-8"?>  
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"  
      "http://www.apple.com/DTDs/PropertyList-1.0.dtd">  
    <plist version="1.0">  
    <dict>  
      <key>Label</key>  
      <string>com.qmd.daemon</string>  
      <key>ProgramArguments</key>  
      <array>  
        <string>qmd</string>  
        <string>mcp</string>  
        <string>--http</string>  
        <string>--daemon</string>  
      </array>  
      <key>RunAtLoad</key>  
      <true/>  
      <key>KeepAlive</key>  
      <true/>  
      <key>StandardOutPath</key>  
      <string>/tmp/qmd-daemon.log</string>  
      <key>StandardErrorPath</key>  
      <string>/tmp/qmd-daemon.log</string>  
    </dict>  
    </plist>  
    EOF  
      
    launchctl load ~/Library/LaunchAgents/com.qmd.daemon.plist  
    
[/code]
#### Linux (systemd user service)[​](<#linux-systemd-user-service> "Direct link to Linux \(systemd user service\)")
[code] 
    mkdir -p ~/.config/systemd/user  
      
    cat > ~/.config/systemd/user/qmd-daemon.service << 'EOF'  
    [Unit]  
    Description=QMD MCP Daemon  
    After=network.target  
      
    [Service]  
    ExecStart=qmd mcp --http --daemon  
    Restart=on-failure  
    RestartSec=10  
    Environment=PATH=/usr/local/bin:/usr/bin:/bin  
      
    [Install]  
    WantedBy=default.target  
    EOF  
      
    systemctl --user daemon-reload  
    systemctl --user enable --now qmd-daemon  
    systemctl --user status qmd-daemon  
    
[/code]
### MCP Tools Reference[​](<#mcp-tools-reference> "Direct link to MCP Tools Reference")
После подключения эти инструменты доступны как `mcp_qmd_*`:
MCP Tool| Maps To| Description  
---|---|---|---  
`mcp_qmd_search`| `qmd search`| Поиск по ключевым словам BM25  
`mcp_qmd_vsearch`| `qmd vsearch`| Семантический векторный поиск  
`mcp_qmd_deep_search`| `qmd query`| Гибридный поиск + переранжирование  
`mcp_qmd_get`| `qmd get`| Получение документа по ID или пути  
`mcp_qmd_status`| `qmd status`| Состояние и статистика индекса  
Инструменты MCP принимают структурированные JSON-запросы для многомодового поиска:
[code] 
    {  
      "searches": [  
        {"type": "lex", "query": "authentication middleware"},  
        {"type": "vec", "query": "how user login is verified"}  
      ],  
      "collections": ["project-docs"],  
      "limit": 10  
    }  
    
[/code]
## CLI Usage (Without MCP)[​](<#cli-usage-without-mcp> "Direct link to CLI Usage \(Without MCP\)")
Если MCP не настроен, используйте qmd напрямую через терминал:
[code] 
    terminal(command="qmd query 'what was decided about the API redesign' --json", timeout=30)  
    
[/code]
Для задач настройки и управления всегда используйте терминал:
[code] 
    terminal(command="qmd collection add ~/Documents/notes --name notes")  
    terminal(command="qmd context add qmd://notes 'Personal research notes and ideas'")  
    terminal(command="qmd embed")  
    terminal(command="qmd status")  
    
[/code]
## How the Search Pipeline Works[​](<#how-the-search-pipeline-works> "Direct link to How the Search Pipeline Works")
Понимание внутреннего устройства помогает выбрать правильный режим поиска:
  1. **Query Expansion** — Тонко настроенная модель на 1,7B параметров генерирует 2 альтернативных запроса. Оригинальный запрос получает вес 2x при слиянии.
  2. **Parallel Retrieval** — BM25 (SQLite FTS5) и векторный поиск выполняются параллельно для всех вариантов запроса.
  3. **RRF Fusion** — Reciprocal Rank Fusion (k=60) объединяет результаты. Бонус за высокий ранг: #1 получает +0,05, #2-3 получают +0,02.
  4. **LLM Reranking** — qwen3-reranker оценивает топ-30 кандидатов (0,0-1,0).
  5. **Position-Aware Blending** — Ранги 1-3: 75% поиск / 25% переранжировщик. Ранги 4-10: 60/40. Ранги 11+: 40/60 (больше доверия переранжировщику для длинного хвоста).


**Smart Chunking:** Документы разбиваются на естественные границы (заголовки, блоки кода, пустые строки) с целевым размером ~900 токенов и 15% перекрытием. Блоки кода никогда не разбиваются посередине.
## Best Practices[​](<#best-practices> "Direct link to Best Practices")
  1. **Всегда добавляйте описания контекста** — `qmd context add` значительно улучшает точность поиска. Опишите, что содержит каждая коллекция.
  2. **Повторно генерируйте эмбеддинги после добавления документов** — `qmd embed` нужно запускать заново при добавлении новых файлов в коллекции.
  3. **Используйте `qmd search` для скорости** — когда нужен быстрый поиск по ключевым словам (идентификаторы кода, точные имена), BM25 работает мгновенно и не требует моделей.
  4. **Используйте `qmd query` для качества** — когда вопрос концептуальный или пользователю нужны наилучшие возможные результаты, используйте гибридный поиск.
  5. **Предпочитайте интеграцию MCP** — после настройки агент получает встроенные инструменты без необходимости каждый раз загружать этот навык.
  6. **Режим демона для частых пользователей** — если пользователь регулярно ищет в своей базе знаний, рекомендую настройку HTTP-демона.
  7. **Первый запрос в структурированном поиске получает вес 2x** — ставьте самый важный/точный запрос первым при комбинировании lex и vec.


## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### "Models downloading on first run"[​](<#models-downloading-on-first-run> "Direct link to \"Models downloading on first run\"")
Нормальное поведение — qmd автоматически загружает ~2 ГБ GGUF-моделей при первом использовании. Это разовая операция.
### Cold start latency (~19s)[​](<#cold-start-latency-19s> "Direct link to Cold start latency \(~19s\)")
Это происходит, когда модели не загружены в память. Решения:
  * Используйте режим HTTP-демона (`qmd mcp --http --daemon`) для поддержания в тёплом состоянии
  * Используйте `qmd search` (только BM25), когда модели не нужны
  * Режим MCP stdio загружает модели при первом поиске, остаётся в тёплом состоянии на время сессии


### macOS: "unable to load extension"[​](<#macos-unable-to-load-extension> "Direct link to macOS: \"unable to load extension\"")
Установите Homebrew SQLite: `brew install sqlite`. Затем убедитесь, что он находится в PATH перед системным SQLite.
### "No collections found"[​](<#no-collections-found> "Direct link to \"No collections found\"")
Запустите `qmd collection add <path> --name <name>` для добавления директорий, затем `qmd embed` для индексации.
### Embedding model override (CJK/multilingual)[​](<#embedding-model-override-cjkmultilingual> "Direct link to Embedding model override \(CJK/multilingual\)")
Установите переменную окружения `QMD_EMBED_MODEL` для неанглийского контента:
[code] 
    export QMD_EMBED_MODEL="your-multilingual-model"  
    
[/code]
## Data Storage[​](<#data-storage> "Direct link to Data Storage")
  * **Index & vectors:** `~/.cache/qmd/index.sqlite`
  * **Models:** Автоматически загружаются в локальный кэш при первом запуске
  * **No cloud dependencies** — всё работает локально


## References[​](<#references> "Direct link to References")
  * [GitHub: tobi/qmd](<https://github.com/tobi/qmd>)
  * [QMD Changelog](<https://github.com/tobi/qmd/blob/main/CHANGELOG.md>)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
    * [Node.js >= 22 (required)](<#nodejs--22-required>)
    * [SQLite with Extension Support (macOS only)](<#sqlite-with-extension-support-macos-only>)
    * [Install qmd](<#install-qmd>)
    * [Verify Installation](<#verify-installation>)
  * [Quick Reference](<#quick-reference>)
  * [Setup Workflow](<#setup-workflow>)
    * [1\\. Add Collections](<#1-add-collections>)
    * [2\\. Add Context Descriptions](<#2-add-context-descriptions>)
    * [3\\. Generate Embeddings](<#3-generate-embeddings>)
    * [4\\. Verify](<#4-verify>)
  * [Search Patterns](<#search-patterns>)
    * [Fast Keyword Search (BM25)](<#fast-keyword-search-bm25>)
    * [Semantic Vector Search](<#semantic-vector-search>)
    * [Hybrid Search with Reranking (Best Quality)](<#hybrid-search-with-reranking-best-quality>)
    * [Structured Multi-Mode Queries](<#structured-multi-mode-queries>)
    * [Query Syntax (lex/BM25 mode)](<#query-syntax-lexbm25-mode>)
    * [HyDE (Hypothetical Document Embeddings)](<#hyde-hypothetical-document-embeddings>)
    * [Scoping to Collections](<#scoping-to-collections>)
    * [Output Formats](<#output-formats>)
  * [MCP Integration (Recommended)](<#mcp-integration-recommended>)
    * [Option A: Stdio Mode (Simple)](<#option-a-stdio-mode-simple>)
    * [Option B: HTTP Daemon Mode (Fast, Recommended for Heavy Use)](<#option-b-http-daemon-mode-fast-recommended-for-heavy-use>)
    * [Keeping the Daemon Running](<#keeping-the-daemon-running>)
    * [MCP Tools Reference](<#mcp-tools-reference>)
  * [CLI Usage (Without MCP)](<#cli-usage-without-mcp>)
  * [How the Search Pipeline Works](<#how-the-search-pipeline-works>)
  * [Best Practices](<#best-practices>)
  * [Troubleshooting](<#troubleshooting>)
    * ["Models downloading on first run"](<#models-downloading-on-first-run>)
    * [Cold start latency (~19s)](<#cold-start-latency-19s>)
    * [macOS: "unable to load extension"](<#macos-unable-to-load-extension>)
    * ["No collections found"](<#no-collections-found>)
    * [Embedding model override (CJK/multilingual)](<#embedding-model-override-cjkmultilingual>)
  * [Data Storage](<#data-storage>)
  * [References](<#references>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-qmd -->
