On this page
API Notion через curl: страницы, базы данных, блоки, поиск.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/productivity/notion` |
|Версия| `1.0.0` |
|Автор| community |
|Лицензия| MIT |
|Теги| `Notion`, `Productivity`, `Notes`, `Database`, `API` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Notion API
Используйте Notion API через curl для создания, чтения и обновления страниц, баз данных (источников данных) и блоков. Никаких дополнительных инструментов не требуется — только curl и ключ API Notion.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  1. Создайте интеграцию на <https://notion.so/my-integrations>
  2. Скопируйте ключ API (начинается с `ntn_` или `secret_`)
  3. Сохраните его в `~/.hermes/.env`:
[code] NOTION_API_KEY=ntn_your_key_here  
         
[/code]
  4. **Важно:** Предоставьте доступ к целевым страницам/базам данных вашей интеграции в Notion (нажмите «...» → «Connect to» → название вашей интеграции)


## Основы API[​](<#api-basics> "Прямая ссылка на Основы API")
Все запросы используют этот шаблон:
[code] 
    curl -s -X GET \"https://api.notion.com/v1/...\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\"  
    
[/code]
Заголовок `Notion-Version` обязателен. Этот навык использует `2025-09-03` (последняя версия). В этой версии базы данных называются «источниками данных» (data sources) в API.
## Распространённые операции[​](<#common-operations> "Прямая ссылка на Распространённые операции")
### Поиск[​](<#search> "Прямая ссылка на Поиск")
[code] 
    curl -s -X POST \"https://api.notion.com/v1/search\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{\"query\": \"page title\"}'  
    
[/code]
### Получить страницу[​](<#get-page> "Прямая ссылка на Получить страницу")
[code] 
    curl -s \"https://api.notion.com/v1/pages/{page_id}\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\"  
    
[/code]
### Получить содержимое страницы (блоки)[​](<#get-page-content-blocks> "Прямая ссылка на Получить содержимое страницы \\(блоки\\)")
[code] 
    curl -s \"https://api.notion.com/v1/blocks/{page_id}/children\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\"  
    
[/code]
### Создать страницу в базе данных[​](<#create-page-in-a-database> "Прямая ссылка на Создать страницу в базе данных")
[code] 
    curl -s -X POST \"https://api.notion.com/v1/pages\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{  
        \"parent\": {\"database_id\": \"xxx\"},  
        \"properties\": {  
          \"Name\": {\"title\": [{\"text\": {\"content\": \"New Item\"}}]},  
          \"Status\": {\"select\": {\"name\": \"Todo\"}}  
        }  
      }'  
    
[/code]
### Запросить базу данных[​](<#query-a-database> "Прямая ссылка на Запросить базу данных")
[code] 
    curl -s -X POST \"https://api.notion.com/v1/data_sources/{data_source_id}/query\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{  
        \"filter\": {\"property\": \"Status\", \"select\": {\"equals\": \"Active\"}},  
        \"sorts\": [{\"property\": \"Date\", \"direction\": \"descending\"}]  
      }'  
    
[/code]
### Создать базу данных[​](<#create-a-database> "Прямая ссылка на Создать базу данных")
[code] 
    curl -s -X POST \"https://api.notion.com/v1/data_sources\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{  
        \"parent\": {\"page_id\": \"xxx\"},  
        \"title\": [{\"text\": {\"content\": \"My Database\"}}],  
        \"properties\": {  
          \"Name\": {\"title\": {}},  
          \"Status\": {\"select\": {\"options\": [{\"name\": \"Todo\"}, {\"name\": \"Done\"}]}},  
          \"Date\": {\"date\": {}}  
        }  
      }'  
    
[/code]
### Обновить свойства страницы[​](<#update-page-properties> "Прямая ссылка на Обновить свойства страницы")
[code] 
    curl -s -X PATCH \"https://api.notion.com/v1/pages/{page_id}\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{\"properties\": {\"Status\": {\"select\": {\"name\": \"Done\"}}}}'  
    
[/code]
### Добавить содержимое на страницу[​](<#add-content-to-a-page> "Прямая ссылка на Добавить содержимое на страницу")
[code] 
    curl -s -X PATCH \"https://api.notion.com/v1/blocks/{page_id}/children\" \\  
      -H \"Authorization: Bearer $NOTION_API_KEY\" \\  
      -H \"Notion-Version: 2025-09-03\" \\  
      -H \"Content-Type: application/json\" \\  
      -d '{  
        \"children\": [  
          {\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"text\": {\"content\": \"Hello from Hermes!\"}}]}}  
        ]  
      }'  
    
[/code]
## Типы свойств[​](<#property-types> "Прямая ссылка на Типы свойств")
Распространённые форматы свойств для элементов базы данных:
  * **Title:** `{\"title\": [{\"text\": {\"content\": \"...\"}}]}`
  * **Rich text:** `{\"rich_text\": [{\"text\": {\"content\": \"...\"}}]}`
  * **Select:** `{\"select\": {\"name\": \"Option\"}}`
  * **Multi-select:** `{\"multi_select\": [{\"name\": \"A\"}, {\"name\": \"B\"}]}`
  * **Date:** `{\"date\": {\"start\": \"2026-01-15\", \"end\": \"2026-01-16\"}}`
  * **Checkbox:** `{\"checkbox\": true}`
  * **Number:** `{\"number\": 42}`
  * **URL:** `{\"url\": \"https://...\"}`
  * **Email:** `{\"email\": \"user@example.com\"}`
  * **Relation:** `{\"relation\": [{\"id\": \"page_id\"}]}`


## Ключевые отличия в версии API 2025-09-03[​](<#key-differences-in-api-version-2025-09-03> "Прямая ссылка на Ключевые отличия в версии API 2025-09-03")
  * **Базы данных → Источники данных:** Используйте эндпоинты `/data_sources/` для запросов и получения данных
  * **Два ID:** Каждая база данных имеет как `database_id`, так и `data_source_id`
    * Используйте `database_id` при создании страниц (`parent: {\"database_id\": \"...\"}`)
    * Используйте `data_source_id` при запросах (`POST /v1/data_sources/{id}/query`)
  * **Результаты поиска:** Базы данных возвращаются как `\"object\": \"data_source\"` с их `data_source_id`


## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * ID страниц/баз данных — это UUID (с дефисами или без)
  * Лимит запросов: ~3 запроса/секунду в среднем
  * API не может устанавливать фильтры представлений базы данных — это только через интерфейс
  * Используйте `is_inline: true` при создании источников данных для встраивания их на страницы
  * Добавьте флаг `-s` к curl для подавления индикаторов прогресса (более чистый вывод для Hermes)
  * Передавайте вывод через `jq` для читаемого JSON: `... | jq '.results[0].properties'`


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
  * [Основы API](<#api-basics>)
  * [Распространённые операции](<#common-operations>)
    * [Поиск](<#search>)
    * [Получить страницу](<#get-page>)
    * [Получить содержимое страницы (блоки)](<#get-page-content-blocks>)
    * [Создать страницу в базе данных](<#create-page-in-a-database>)
    * [Запросить базу данных](<#query-a-database>)
    * [Создать базу данных](<#create-a-database>)
    * [Обновить свойства страницы](<#update-page-properties>)
    * [Добавить содержимое на страницу](<#add-content-to-a-page>)
  * [Типы свойств](<#property-types>)
  * [Ключевые отличия в версии API 2025-09-03](<#key-differences-in-api-version-2025-09-03>)
  * [Примечания](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-notion -->
