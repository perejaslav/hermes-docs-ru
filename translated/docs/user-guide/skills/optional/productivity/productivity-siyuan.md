On this page
API SiYuan Note для поиска, чтения, создания и управления блоками и документами в самостоятельной базе знаний через curl.
## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/productivity/siyuan`  |
|Путь| `optional-skills/productivity/siyuan`  |
|Версия| `1.0.0`  |
|Автор| FEUAZUR  |
|Лицензия| MIT  |
|Теги| `SiYuan`, `Notes`, `Knowledge Base`, `PKM`, `API`  |
|Связанные навыки| [`obsidian`](</docs/user-guide/skills/bundled/note-taking/note-taking-obsidian>), [`notion`](</docs/user-guide/skills/bundled/productivity/productivity-notion>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# API SiYuan Note
Используйте [SiYuan](<https://github.com/siyuan-note/siyuan>) kernel API через curl для поиска, чтения, создания, обновления и удаления блоков и документов в самостоятельной базе знаний. Никаких дополнительных инструментов не требуется — только curl и API-токен.
## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")
 1. Установите и запустите SiYuan (desktop или Docker)
 2. Получите API-токен: **Настройки > О программе > API token**
 3. Сохраните его в `~/.hermes/.env`:
[code] SIYUAN_TOKEN=your_token_here  
         SIYUAN_URL=http://127.0.0.1:6806  
         
[/code]
`SIYUAN_URL` по умолчанию равен `http://127.0.0.1:6806`, если не задан.


## Основы API[​](<#api-basics> "Direct link to API Basics")
Все вызовы API SiYuan — это **POST с JSON-телом**. Каждый запрос следует этому шаблону:
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/..." \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"param": "value"}'  
    
[/code]
Ответы имеют структуру JSON:
[code] 
    {"code": 0, "msg": "", "data": { ... }}  
    
[/code]
`code: 0` означает успех. Любое другое значение — ошибка; проверьте `msg` для подробностей.
**Формат ID:** ID SiYuan выглядят как `20210808180117-6v0mkxr` (14-значная временная метка + 7 буквенно-цифровых символов).
## Краткий справочник[​](<#quick-reference> "Direct link to Quick Reference")
|Операция| Endpoint  |
|---|---|
|Полнотекстовый поиск| `/api/search/fullTextSearchBlock`  |
|SQL-запрос| `/api/query/sql`  |
|Чтение блока| `/api/block/getBlockKramdown`  |
|Чтение дочерних блоков| `/api/block/getChildBlocks`  |
|Получение пути| `/api/filetree/getHPathByID`  |
|Получение атрибутов| `/api/attr/getBlockAttrs`  |
|Список блокнотов| `/api/notebook/lsNotebooks`  |
|Список документов| `/api/filetree/listDocsByPath`  |
|Создание блокнота| `/api/notebook/createNotebook`  |
|Создание документа| `/api/filetree/createDocWithMd`  |
|Добавление блока| `/api/block/appendBlock`  |
|Обновление блока| `/api/block/updateBlock`  |
|Переименование документа| `/api/filetree/renameDocByID`  |
|Установка атрибутов| `/api/attr/setBlockAttrs`  |
|Удаление блока| `/api/block/deleteBlock`  |
|Удаление документа| `/api/filetree/removeDocByID`  |
|Экспорт в Markdown| `/api/export/exportMdContent`  |
## Типовые операции[​](<#common-operations> "Direct link to Common Operations")
### Поиск (полнотекстовый)[​](<#search-full-text> "Direct link to Search (Full-Text)")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/search/fullTextSearchBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "meeting notes", "page": 0}' | jq '.data.blocks[:5]'  
    
[/code]
### Поиск (SQL)[​](<#search-sql> "Direct link to Search (SQL)")
Запросы напрямую к базе блоков. Безопасны только SELECT-выражения.
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/query/sql" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"stmt": "SELECT id, content, type, box FROM blocks WHERE content LIKE '\\''%keyword%'\\'' AND type='\\''p'\\'' LIMIT 20"}' | jq '.data'  
    
[/code]
Полезные колонки: `id`, `parent_id`, `root_id`, `box` (ID блокнота), `path`, `content`, `type`, `subtype`, `created`, `updated`.
### Чтение содержимого блока[​](<#read-block-content> "Direct link to Read Block Content")
Возвращает содержимое блока в формате Kramdown (похож на Markdown).
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getBlockKramdown" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data.kramdown'  
    
[/code]
### Чтение дочерних блоков[​](<#read-child-blocks> "Direct link to Read Child Blocks")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getChildBlocks" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'  
    
[/code]
### Получение человекочитаемого пути[​](<#get-human-readable-path> "Direct link to Get Human-Readable Path")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/getHPathByID" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'  
    
[/code]
### Получение атрибутов блока[​](<#get-block-attributes> "Direct link to Get Block Attributes")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/getBlockAttrs" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'  
    
[/code]
### Список блокнотов[​](<#list-notebooks> "Direct link to List Notebooks")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/lsNotebooks" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{}' | jq '.data.notebooks[] | {id, name, closed}'  
    
[/code]
### Список документов в блокноте[​](<#list-documents-in-a-notebook> "Direct link to List Documents in a Notebook")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/listDocsByPath" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"notebook": "NOTEBOOK_ID", "path": "/"}' | jq '.data.files[] | {id, name}'  
    
[/code]
### Создание документа[​](<#create-a-document> "Direct link to Create a Document")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/createDocWithMd" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "notebook": "NOTEBOOK_ID",  
        "path": "/Meeting Notes/2026-03-22",  
        "markdown": "# Meeting Notes\n\n- Discussed project timeline\n- Assigned tasks"  
      }' | jq '.data'  
    
[/code]
### Создание блокнота[​](<#create-a-notebook> "Direct link to Create a Notebook")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/createNotebook" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"name": "My New Notebook"}' | jq '.data.notebook.id'  
    
[/code]
### Добавление блока в документ[​](<#append-block-to-document> "Direct link to Append Block to Document")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/appendBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "parentID": "DOCUMENT_OR_BLOCK_ID",  
        "data": "New paragraph added at the end.",  
        "dataType": "markdown"  
      }' | jq '.data'  
    
[/code]
Также доступны: `/api/block/prependBlock` (те же параметры, вставляет в начало) и `/api/block/insertBlock` (использует `previousID` вместо `parentID` для вставки после определённого блока).
### Обновление содержимого блока[​](<#update-block-content> "Direct link to Update Block Content")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/updateBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "id": "BLOCK_ID",  
        "data": "Updated content here.",  
        "dataType": "markdown"  
      }' | jq '.data'  
    
[/code]
### Переименование документа[​](<#rename-a-document> "Direct link to Rename a Document")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/renameDocByID" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "DOCUMENT_ID", "title": "New Title"}'  
    
[/code]
### Установка атрибутов блока[​](<#set-block-attributes> "Direct link to Set Block Attributes")
Пользовательские атрибуты должны начинаться с префикса `custom-`:
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/setBlockAttrs" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "id": "BLOCK_ID",  
        "attrs": {  
          "custom-status": "reviewed",  
          "custom-priority": "high"  
        }  
      }'  
    
[/code]
### Удаление блока[​](<#delete-a-block> "Direct link to Delete a Block")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/deleteBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "BLOCK_ID"}'  
    
[/code]
Чтобы удалить целый документ: используйте `/api/filetree/removeDocByID` с `{"id": "DOC_ID"}`. Чтобы удалить блокнот: используйте `/api/notebook/removeNotebook` с `{"notebook": "NOTEBOOK_ID"}`.
### Экспорт документа в Markdown[​](<#export-document-as-markdown> "Direct link to Export Document as Markdown")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/export/exportMdContent" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "DOCUMENT_ID"}' | jq -r '.data.content'  
    
[/code]
## Типы блоков[​](<#block-types> "Direct link to Block Types")
Распространённые значения `type` в SQL-запросах:
|Тип| Описание  |
|---|---|
|`d`| Документ (корневой блок)  |
|`p`| Абзац  |
|`h`| Заголовок  |
|`l`| Список  |
|`i`| Элемент списка  |
|`c`| Блок кода  |
|`m`| Математический блок  |
|`t`| Таблица  |
|`b`| Цитата  |
|`s`| Суперблок  |
|`html`| HTML-блок  |
## Подводные камни[​](<#pitfalls> "Direct link to Pitfalls")
  * **Все endpoint'ы — POST** \\-- даже операции только для чтения. Не используйте GET.
  * **Безопасность SQL**: используйте только SELECT-запросы. INSERT/UPDATE/DELETE/DROP опасны и никогда не должны отправляться.
  * **Валидация ID**: ID соответствуют шаблону `YYYYMMDDHHmmss-xxxxxxx`. Отклоняйте всё остальное.
  * **Ответы с ошибками**: всегда проверяйте `code != 0` в ответах перед обработкой `data`.
  * **Большие документы**: содержимое блоков и результаты экспорта могут быть очень большими. Используйте `LIMIT` в SQL и передавайте через `jq`, чтобы извлекать только нужное.
  * **ID блокнотов**: при работе с конкретным блокнотом сначала получите его ID через `lsNotebooks`.


## Альтернатива: MCP-сервер[​](<#alternative-mcp-server> "Direct link to Alternative: MCP Server")
Если вы предпочитаете нативную интеграцию вместо curl, установите MCP-сервер SiYuan:
[code] 
    # В ~/.hermes/config.yaml в разделе mcp_servers:  
    mcp_servers:  
      siyuan:  
        command: npx  
        args: ["-y", "@porkll/siyuan-mcp"]  
        env:  
          SIYUAN_TOKEN: "your_token"  
          SIYUAN_URL: "http://127.0.0.1:6806"  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
  * [Основы API](<#api-basics>)
  * [Краткий справочник](<#quick-reference>)
  * [Типовые операции](<#common-operations>)
    * [Поиск (полнотекстовый)](<#search-full-text>)
    * [Поиск (SQL)](<#search-sql>)
    * [Чтение содержимого блока](<#read-block-content>)
    * [Чтение дочерних блоков](<#read-child-blocks>)
    * [Получение человекочитаемого пути](<#get-human-readable-path>)
    * [Получение атрибутов блока](<#get-block-attributes>)
    * [Список блокнотов](<#list-notebooks>)
    * [Список документов в блокноте](<#list-documents-in-a-notebook>)
    * [Создание документа](<#create-a-document>)
    * [Создание блокнота](<#create-a-notebook>)
    * [Добавление блока в документ](<#append-block-to-document>)
    * [Обновление содержимого блока](<#update-block-content>)
    * [Переименование документа](<#rename-a-document>)
    * [Установка атрибутов блока](<#set-block-attributes>)
    * [Удаление блока](<#delete-a-block>)
    * [Экспорт документа в Markdown](<#export-document-as-markdown>)
  * [Типы блоков](<#block-types>)
  * [Подводные камни](<#pitfalls>)
  * [Альтернатива: MCP-сервер](<#alternative-mcp-server>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-siyuan -->
