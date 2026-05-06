На этой странице
Поиск статей arXiv по ключевому слову, автору, категории или ID.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---  |---
|Источник| Встроенный (установлен по умолчанию)
|Путь| `skills/research/arxiv`
|Версия| `1.0.0`
|Автор| Hermes Agent
|Лицензия| MIT
|Теги| `Research`, `Arxiv`, `Papers`, `Academic`, `Science`, `API`
|Связанные навыки| [`ocr-and-documents`](</docs/user-guide/skills/bundled/productivity/productivity-ocr-and-documents>)
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что видит агент в качестве инструкций, когда навык активен.
# arXiv Research
Поиск и получение академических статей из arXiv через их бесплатный REST API. Никакого API-ключа, никаких зависимостей — только curl.
## Быстрая справка[​](<#quick-reference> "Прямая ссылка на Быстрая справка")
Действие| Команда
---|---
Поиск статей| `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"`
Получение конкретной статьи| `curl "https://export.arxiv.org/api/query?id_list=2402.03300"`
Чтение аннотации (веб)| `web_extract(urls=["https://arxiv.org/abs/2402.03300"])`
Чтение полного текста (PDF)| `web_extract(urls=["https://arxiv.org/pdf/2402.03300"])`
## Поиск статей[​](<#searching-papers> "Прямая ссылка на Поиск статей")
API возвращает Atom XML. Парсите с помощью `grep`/`sed` или передавайте через `python3` для чистого вывода.
### Базовый поиск[​](<#basic-search> "Прямая ссылка на Базовый поиск")
[code] 
    curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5"  
    
[/code]
### Чистый вывод (парсинг XML в читаемый формат)[​](<#clean-output-parse-xml-to-readable-format> "Прямая ссылка на Чистый вывод \\(парсинг XML в читаемый формат\\)")
[code] 
    curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=submittedDate&sortOrder=descending" | python3 -c "
    import sys, xml.etree.ElementTree as ET
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    root = ET.parse(sys.stdin).getroot()
    for i, entry in enumerate(root.findall('a:entry', ns)):
        title = entry.find('a:title', ns).text.strip().replace('\\n', ' ')
        arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
        published = entry.find('a:published', ns).text[:10]
        authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
        summary = entry.find('a:summary', ns).text.strip()[:200]
        cats = ', '.join(c.get('term') for c in entry.findall('a:category', ns))
        print(f'{i+1}. [{arxiv_id}] {title}')
        print(f'   Authors: {authors}')
        print(f'   Published: {published} | Categories: {cats}')
        print(f'   Abstract: {summary}...')
        print(f'   PDF: https://arxiv.org/pdf/{arxiv_id}')
        print()
    "
    
[/code]
## Синтаксис поискового запроса[​](<#search-query-syntax> "Прямая ссылка на Синтаксис поискового запроса")
Префикс| Поиск по| Пример
---|---|---
`all:`| Всем полям| `all:transformer+attention`
`ti:`| Названию| `ti:large+language+models`
`au:`| Автору| `au:vaswani`
`abs:`| Аннотации| `abs:reinforcement+learning`
`cat:`| Категории| `cat:cs.AI`
`co:`| Комментарию| `co:accepted+NeurIPS`
### Булевы операторы[​](<#boolean-operators> "Прямая ссылка на Булевы операторы")
[code] 
    # AND (по умолчанию при использовании +)
    search_query=all:transformer+attention
     
    # OR
    search_query=all:GPT+OR+all:BERT
     
    # AND NOT
    search_query=all:language+model+ANDNOT+all:vision
     
    # Точная фраза
    search_query=ti:"chain+of+thought"
     
    # Комбинированный
    search_query=au:hinton+AND+cat:cs.LG
    
[/code]
## Сортировка и пагинация[​](<#sort-and-pagination> "Прямая ссылка на Сортировка и пагинация")
Параметр| Опции
---|---
`sortBy`| `relevance`, `lastUpdatedDate`, `submittedDate`
`sortOrder`| `ascending`, `descending`
`start`| Смещение результатов (начиная с 0)
`max_results`| Количество результатов (по умолчанию 10, макс. 30000)
[code] 
    # Последние 10 статей в cs.AI
    curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10"
    
[/code]
## Получение конкретных статей[​](<#fetching-specific-papers> "Прямая ссылка на Получение конкретных статей")
[code] 
    # По arXiv ID
    curl -s "https://export.arxiv.org/api/query?id_list=2402.03300"
     
    # Несколько статей
    curl -s "https://export.arxiv.org/api/query?id_list=2402.03300,2401.12345,2403.00001"
    
[/code]
## Генерация BibTeX[​](<#bibtex-generation> "Прямая ссылка на Генерация BibTeX")
После получения метаданных статьи можно сгенерировать BibTeX-запись:
{% raw %}
[code] 
    curl -s "https://export.arxiv.org/api/query?id_list=1706.03762" | python3 -c "
    import sys, xml.etree.ElementTree as ET
    ns = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    root = ET.parse(sys.stdin).getroot()
    entry = root.find('a:entry', ns)
    if entry is None: sys.exit('Paper not found')
    title = entry.find('a:title', ns).text.strip().replace('\\n', ' ')
    authors = ' and '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    year = entry.find('a:published', ns).text[:4]
    raw_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    cat = entry.find('arxiv:primary_category', ns)
    primary = cat.get('term') if cat is not None else 'cs.LG'
    last_name = entry.find('a:author', ns).find('a:name', ns).text.split()[-1]
    print(f'@article{{{last_name}{year}_{raw_id.replace(\".\", \"\")},')
    print(f'  title     = {{{title}}},')
    print(f'  author    = {{{authors}}},')
    print(f'  year      = {{{year}}},')
    print(f'  eprint    = {{{raw_id}}},')
    print(f'  archivePrefix = {{arXiv}},')
    print(f'  primaryClass  = {{{primary}}},')
    print(f'  url       = {{https://arxiv.org/abs/{raw_id}}}')
    print('}')
    "
    
[/code]
{% endraw %}
## Чтение содержимого статей[​](<#reading-paper-content> "Прямая ссылка на Чтение содержимого статей")
После нахождения статьи вы можете прочитать её:
[code] 
    # Страница с аннотацией (быстро, метаданные + аннотация)
    web_extract(urls=["https://arxiv.org/abs/2402.03300"])
     
    # Полный текст статьи (PDF → markdown через Firecrawl)
    web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
    
[/code]
Для локальной обработки PDF см. навык `ocr-and-documents`.
## Распространённые категории[​](<#common-categories> "Прямая ссылка на Распространённые категории")
Категория| Область
---|---
`cs.AI`| Artificial Intelligence (Искусственный интеллект)
`cs.CL`| Computation and Language (NLP) (Вычисления и язык)
`cs.CV`| Computer Vision (Компьютерное зрение)
`cs.LG`| Machine Learning (Машинное обучение)
`cs.CR`| Cryptography and Security (Криптография и безопасность)
`stat.ML`| Machine Learning (Statistics) (Машинное обучение, статистика)
`math.OC`| Optimization and Control (Оптимизация и управление)
`physics.comp-ph`| Computational Physics (Вычислительная физика)
Полный список: <https://arxiv.org/category_taxonomy>
## Вспомогательный скрипт[​](<#helper-script> "Прямая ссылка на Вспомогательный скрипт")
Скрипт `scripts/search_arxiv.py` обрабатывает парсинг XML и предоставляет чистый вывод:
[code] 
    python scripts/search_arxiv.py "GRPO reinforcement learning"
    python scripts/search_arxiv.py "transformer attention" --max 10 --sort date
    python scripts/search_arxiv.py --author "Yann LeCun" --max 5
    python scripts/search_arxiv.py --category cs.AI --sort date
    python scripts/search_arxiv.py --id 2402.03300
    python scripts/search_arxiv.py --id 2402.03300,2401.12345
    
[/code]
Без зависимостей — используется только стандартная библиотека Python.
* * *
## Semantic Scholar (Цитирования, Похожие статьи, Профили авторов)[​](<#semantic-scholar-citations-related-papers-author-profiles> "Прямая ссылка на Semantic Scholar \\(Цитирования, Похожие статьи, Профили авторов\\)")
arXiv не предоставляет данные о цитированиях или рекомендации. Используйте **Semantic Scholar API** для этого — бесплатно, без ключа для базового использования (1 запрос/сек), возвращает JSON.
### Получение информации о статье + цитирования[​](<#get-paper-details--citations> "Прямая ссылка на Получение информации о статье + цитирования")
[code] 
    # По arXiv ID
    curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=title,authors,citationCount,referenceCount,influentialCitationCount,year,abstract" | python3 -m json.tool
     
    # По Semantic Scholar paper ID или DOI
    curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example?fields=title,citationCount"
    
[/code]
### Получение цитирований статьи (кто на неё сослался)[​](<#get-citations-of-a-paper-who-cited-it> "Прямая ссылка на Получение цитирований статьи \\(кто на неё сослался\\)")
[code] 
    curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool
    
[/code]
### Получение ссылок из статьи (на что она ссылается)[​](<#get-references-from-a-paper-what-it-cites> "Прямая ссылка на Получение ссылок из статьи \\(на что она ссылается\\)")
[code] 
    curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool
    
[/code]
### Поиск статей (альтернатива поиску arXiv, возвращает JSON)[​](<#search-papers-alternative-to-arxiv-search-returns-json> "Прямая ссылка на Поиск статей \\(альтернатива поиску arXiv, возвращает JSON\\)")
[code] 
    curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=GRPO+reinforcement+learning&limit=5&fields=title,authors,year,citationCount,externalIds" | python3 -m json.tool
    
[/code]
### Получение рекомендаций статей[​](<#get-paper-recommendations> "Прямая ссылка на Получение рекомендаций статей")
[code] 
    curl -s -X POST "https://api.semanticscholar.org/recommendations/v1/papers/" \
      -H "Content-Type: application/json" \
      -d '{"positivePaperIds": ["arXiv:2402.03300"], "negativePaperIds": []}' | python3 -m json.tool
    
[/code]
### Профиль автора[​](<#author-profile> "Прямая ссылка на Профиль автора")
[code] 
    curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&fields=name,hIndex,citationCount,paperCount" | python3 -m json.tool
    
[/code]
### Полезные поля Semantic Scholar[​](<#useful-semantic-scholar-fields> "Прямая ссылка на Полезные поля Semantic Scholar")
`title`, `authors`, `year`, `abstract`, `citationCount`, `referenceCount`, `influentialCitationCount`, `isOpenAccess`, `openAccessPdf`, `fieldsOfStudy`, `publicationVenue`, `externalIds` (содержит arXiv ID, DOI и т.д.)
* * *
## Полный рабочий процесс исследования[​](<#complete-research-workflow> "Прямая ссылка на Полный рабочий процесс исследования")
  1. **Поиск**: `python scripts/search_arxiv.py "ваша тема" --sort date --max 10`
  2. **Оценка влияния**: `curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=citationCount,influentialCitationCount"`
  3. **Чтение аннотации**: `web_extract(urls=["https://arxiv.org/abs/ID"])`
  4. **Чтение полного текста**: `web_extract(urls=["https://arxiv.org/pdf/ID"])`
  5. **Поиск связанных работ**: `curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID/references?fields=title,citationCount&limit=20"`
  6. **Получение рекомендаций**: POST к endpoint рекомендаций Semantic Scholar
  7. **Отслеживание авторов**: `curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=ИМЯ"`


## Ограничения частоты запросов[​](<#rate-limits> "Прямая ссылка на Ограничения частоты запросов")
API| Ограничение| Авторизация
---|---|---|
arXiv| ~1 запрос / 3 секунды| Не требуется
Semantic Scholar| 1 запрос / секунду| Не требуется (100/сек с API-ключом)
## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * arXiv возвращает Atom XML — используйте вспомогательный скрипт или сниппет для парсинга, чтобы получить чистый вывод
  * Semantic Scholar возвращает JSON — передавайте через `python3 -m json.tool` для читаемости
  * arXiv ID: старый формат (`hep-th/0601001`) и новый (`2402.03300`)
  * PDF: `https://arxiv.org/pdf/{id}` — Аннотация: `https://arxiv.org/abs/{id}`
  * HTML (если доступно): `https://arxiv.org/html/{id}`
  * Для локальной обработки PDF см. навык `ocr-and-documents`


## Версионирование ID[​](<#id-versioning> "Прямая ссылка на Версионирование ID")
  * `arxiv.org/abs/1706.03762` всегда разрешается в **последнюю** версию
  * `arxiv.org/abs/1706.03762v1` указывает на **конкретную** неизменяемую версию
  * При создании цитирований сохраняйте суффикс версии, которую вы фактически читали, чтобы предотвратить дрейф цитирований (более поздняя версия может существенно изменить содержание)
  * Поле `<id>` API возвращает URL с версией (например, `http://arxiv.org/abs/1706.03762v7`)


## Отозванные статьи[​](<#withdrawn-papers> "Прямая ссылка на Отозванные статьи")
Статьи могут быть отозваны после отправки. В этом случае:
  * Поле `<summary>` содержит уведомление об отзыве (ищите "withdrawn" или "retracted")
  * Поля метаданных могут быть неполными
  * Всегда проверяйте аннотацию, прежде чем считать результат валидной статьёй


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Быстрая справка](<#quick-reference>)
  * [Поиск статей](<#searching-papers>)
    * [Базовый поиск](<#basic-search>)
    * [Чистый вывод (парсинг XML в читаемый формат)](<#clean-output-parse-xml-to-readable-format>)
  * [Синтаксис поискового запроса](<#search-query-syntax>)
    * [Булевы операторы](<#boolean-operators>)
  * [Сортировка и пагинация](<#sort-and-pagination>)
  * [Получение конкретных статей](<#fetching-specific-papers>)
  * [Генерация BibTeX](<#bibtex-generation>)
  * [Чтение содержимого статей](<#reading-paper-content>)
  * [Распространённые категории](<#common-categories>)
  * [Вспомогательный скрипт](<#helper-script>)
  * [Semantic Scholar (Цитирования, Похожие статьи, Профили авторов)](<#semantic-scholar-citations-related-papers-author-profiles>)
    * [Получение информации о статье + цитирования](<#get-paper-details--citations>)
    * [Получение цитирований статьи (кто на неё сослался)](<#get-citations-of-a-paper-who-cited-it>)
    * [Получение ссылок из статьи (на что она ссылается)](<#get-references-from-a-paper-what-it-cites>)
    * [Поиск статей (альтернатива поиску arXiv, возвращает JSON)](<#search-papers-alternative-to-arxiv-search-returns-json>)
    * [Получение рекомендаций статей](<#get-paper-recommendations>)
    * [Профиль автора](<#author-profile>)
    * [Полезные поля Semantic Scholar](<#useful-semantic-scholar-fields>)
  * [Полный рабочий процесс исследования](<#complete-research-workflow>)
  * [Ограничения частоты запросов](<#rate-limits>)
  * [Примечания](<#notes>)
  * [Версионирование ID](<#id-versioning>)
  * [Отозванные статьи](<#withdrawn-papers>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-arxiv -->
