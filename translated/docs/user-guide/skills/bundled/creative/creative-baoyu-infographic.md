On this page
Инфографика: 21 макет × 21 стиль (信息图, 可视化).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/baoyu-infographic`  |
Version| `1.56.1`  |
Author| 宝玉 (JimLiu)  |
License| MIT  |
Tags| `infographic`, `visual-summary`, `creative`, `image-generation`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Infographic Generator
Адаптировано из [baoyu-infographic](<https://github.com/JimLiu/baoyu-skills>) для экосистемы инструментов Hermes Agent.
Два измерения: **макет** (информационная структура) × **стиль** (визуальная эстетика). Свободно комбинируйте любой макет с любым стилем.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
Активируйте этот навык, когда пользователь просит создать инфографику, визуальную сводку, информационную графику, или использует термины вроде «信息图», «可视化» или «высокоплотная информационная графика». Пользователь предоставляет контент (текст, путь к файлу, URL или тему) и опционально указывает макет, стиль, соотношение сторон или язык.
## Options[​](<#options> "Direct link to Options")
Опция| Значения  
---|---  
Макет| 21 опция (см. Галерею макетов), по умолч.: bento-grid  
Стиль| 21 опция (см. Галерею стилей), по умолч.: craft-handmade  
Соотношение| Именованные: landscape (16:9), portrait (9:16), square (1:1). Пользовательское: любое соотношение W:H (например, 3:4, 4:3, 2.35:1)  
Язык| en, zh, ja и т.д.  
## Layout Gallery[​](<#layout-gallery> "Direct link to Layout Gallery")
Макет| Лучше всего для  
---|---  
`linear-progression`| Таймлайны, процессы, обучалки  
`binary-comparison`| A vs B, до-после, плюсы-минусы  
`comparison-matrix`| Многофакторные сравнения  
`hierarchical-layers`| Пирамиды, уровни приоритетов  
`tree-branching`| Категории, таксономии  
`hub-spoke`| Центральная концепция со связанными элементами  
`structural-breakdown`| Взрыв-схемы, сечения  
`bento-grid`| Множество тем, обзор (по умолчанию)  
`iceberg`| Поверхностные vs скрытые аспекты  
`bridge`| Проблема-решение  
`funnel`| Конверсия, фильтрация  
`isometric-map`| Пространственные отношения  
`dashboard`| Метрики, KPI  
`periodic-table`| Категоризированные коллекции  
`comic-strip`| Нарративы, последовательности  
`story-mountain`| Сюжетная структура, дуги напряжения  
`jigsaw`| Взаимосвязанные части  
`venn-diagram`| Пересекающиеся концепции  
`winding-roadmap`| Путешествие, этапы  
`circular-flow`| Циклы, повторяющиеся процессы  
`dense-modules`| Высокоплотные модули, руководства с данными  
Полные определения: `references/layouts/<layout>.md`
## Style Gallery[​](<#style-gallery> "Direct link to Style Gallery")
Стиль| Описание  
---|---  
`craft-handmade`| Рисованный от руки, бумажная работа (по умолчанию)  
`claymation`| 3D глиняные фигурки, stop-motion  
`kawaii`| Японское милое, пастельные тона  
`storybook-watercolor`| Мягкая акварель, причудливый  
`chalkboard`| Мел на чёрной доске  
`cyberpunk-neon`| Неоновое свечение, футуристичный  
`bold-graphic`| Комикс-стиль, полутон  
`aged-academia`| Винтажная наука, сепия  
`corporate-memphis`| Плоский вектор, яркий  
`technical-schematic`| Чертеж, инженерный  
`origami`| Складная бумага, геометричный  
`pixel-art`| Ретро 8-bit  
`ui-wireframe`| Оттенки серого, макет интерфейса  
`subway-map`| Транзитная диаграмма  
`ikea-manual`| Минимальная линейная графика  
`knolling`| Организованная раскладка  
`lego-brick`| Конструктор из кирпичиков  
`pop-laboratory`| Чертежная сетка, координатные маркеры, лабораторная точность  
`morandi-journal`| Рисованные от руки каракули, тёплые тона Morandi  
`retro-pop-grid`| Ретро поп-арт 1970-х, швейцарская сетка, толстые контуры  
`hand-drawn-edu`| Пастельные тона macaron, дрожание от руки, палочные фигурки  
Полные определения: `references/styles/<style>.md`
## Recommended Combinations[​](<#recommended-combinations> "Direct link to Recommended Combinations")
Тип контента| Макет + Стиль  
---|---  
Таймлайн/История| `linear-progression` + `craft-handmade`  
Пошаговый| `linear-progression` + `ikea-manual`  
A vs B| `binary-comparison` + `corporate-memphis`  
Иерархия| `hierarchical-layers` + `craft-handmade`  
Пересечение| `venn-diagram` + `craft-handmade`  
Конверсия| `funnel` + `corporate-memphis`  
Циклы| `circular-flow` + `craft-handmade`  
Технический| `structural-breakdown` + `technical-schematic`  
Метрики| `dashboard` + `corporate-memphis`  
Образовательный| `bento-grid` + `chalkboard`  
Путешествие| `winding-roadmap` + `storybook-watercolor`  
Категории| `periodic-table` + `bold-graphic`  
Руководство по продукту| `dense-modules` + `morandi-journal`  
Техническое руководство| `dense-modules` + `pop-laboratory`  
Модное руководство| `dense-modules` + `retro-pop-grid`  
Образовательная диаграмма| `hub-spoke` + `hand-drawn-edu`  
Обучающий процесс| `linear-progression` + `hand-drawn-edu`  
По умолчанию: `bento-grid` + `craft-handmade`
## Keyword Shortcuts[​](<#keyword-shortcuts> "Direct link to Keyword Shortcuts")
Когда ввод пользователя содержит эти ключевые слова, **автоматически выбирайте** связанный макет и предлагайте связанные стили как лучшие рекомендации на Шаге 3. Пропускайте вывод макета на основе контента для совпавших ключевых слов.
Если у ярлыка есть **Prompt Notes** (Заметки к промпту), добавляйте их к сгенерированному промпту (Шаг 5) как дополнительные инструкции по стилю.
Ключевое слово пользователя| Макет| Рекомендуемые стили| Соотношение по умолч.| Заметки к промпту  
---|---|---|---|---  
高密度信息大图 / high-density-info| `dense-modules`| `morandi-journal`, `pop-laboratory`, `retro-pop-grid`| portrait| —  
信息图 / infographic| `bento-grid`| `craft-handmade`| landscape| Минимализм: чистый холст, достаточно пустого пространства, без сложных текстур фона. Только простые мультяшные элементы и иконки.  
## Output Structure[​](<#output-structure> "Direct link to Output Structure")
[code] 
    infographic/{topic-slug}/  
    ├── source-{slug}.{ext}  
    ├── analysis.md  
    ├── structured-content.md  
    ├── prompts/infographic.md  
    └── infographic.png  
    
[/code]
Slug: 2-4 слова kebab-case из темы. Конфликт: добавьте `-YYYYMMDD-HHMMSS`.
## Core Principles[​](<#core-principles> "Direct link to Core Principles")
  * Сохраняйте исходные данные точно — без обобщения или перефразирования (но **удаляйте любые учётные данные, API-ключи, токены или секреты** перед включением в выводы)
  * Определяйте цели обучения перед структурированием контента
  * Структурируйте для визуальной коммуникации (заголовки, подписи, визуальные элементы)


## Workflow[​](<#workflow> "Direct link to Workflow")
### Step 1: Analyze Content[​](<#step-1-analyze-content> "Direct link to Step 1: Analyze Content")
**Загрузите референсы:** Прочитайте `references/analysis-framework.md` из этого навыка.
  1. Сохраните исходный контент (путь к файлу или вставка → `source.md` с помощью `write_file`)
     * **Правило бекапа:** Если `source.md` существует, переименуйте в `source-backup-YYYYMMDD-HHMMSS.md`
  2. Проанализируйте: тема, тип данных, сложность, тон, аудитория
  3. Определите язык источника и язык пользователя
  4. Извлеките инструкции по дизайну из ввода пользователя
  5. Сохраните анализ в `analysis.md`
     * **Правило бекапа:** Если `analysis.md` существует, переименуйте в `analysis-backup-YYYYMMDD-HHMMSS.md`


См. `references/analysis-framework.md` для подробного формата.
### Step 2: Generate Structured Content → `structured-content.md`[​](<#step-2-generate-structured-content--structured-contentmd> "Direct link to step-2-generate-structured-content--structured-contentmd")
Трансформируйте контент в структуру инфографики:
  1. Название и цели обучения
  2. Секции с: ключевой концепцией, контентом (дословно), визуальным элементом, текстовыми подписями
  3. Точки данных (все статистики/цитаты копируются точно)
  4. Инструкции по дизайну от пользователя


**Правила:** Только Markdown. Никакой новой информации. Сохраняйте данные точно. Удаляйте любые учётные данные или секреты из вывода.
См. `references/structured-content-template.md` для подробного формата.
### Step 3: Recommend Combinations[​](<#step-3-recommend-combinations> "Direct link to Step 3: Recommend Combinations")
**3.1 Проверьте Keyword Shortcuts сначала:** Если ввод пользователя совпадает с ключевым словом из таблицы **Keyword Shortcuts**, автоматически выберите связанный макет и приоритизируйте связанные стили как лучшие рекомендации. Пропустите вывод макета на основе контента.
**3.2 Иначе** , рекомендуйте 3-5 комбинаций макет×стиль на основе:
  * Структуры данных → соответствующий макет
  * Тона контента → соответствующий стиль
  * Ожиданий аудитории
  * Инструкций пользователя по дизайну


### Step 4: Confirm Options[​](<#step-4-confirm-options> "Direct link to Step 4: Confirm Options")
Используйте инструмент `clarify` для подтверждения опций с пользователем. Поскольку `clarify` обрабатывает один вопрос за раз, задайте самый важный вопрос первым:
**Q1 — Комбинация:** Представьте 3+ комбинации макет×стиль с обоснованием. Попросите пользователя выбрать одну.
**Q2 — Соотношение:** Спросите о предпочтении соотношения сторон (landscape/portrait/square или пользовательское W:H).
**Q3 — Язык** (только если источник ≠ язык пользователя): Спросите, на каком языке должен быть текстовый контент.
### Step 5: Generate Prompt → `prompts/infographic.md`[​](<#step-5-generate-prompt--promptsinfographicmd> "Direct link to step-5-generate-prompt--promptsinfographicmd")
**Правило бекапа:** Если `prompts/infographic.md` существует, переименуйте в `prompts/infographic-backup-YYYYMMDD-HHMMSS.md`
**Загрузите референсы:** Прочитайте выбранный макет из `references/layouts/<layout>.md` и стиль из `references/styles/<style>.md`.
Скомбинируйте:
  1. Определение макета из `references/layouts/<layout>.md`
  2. Определение стиля из `references/styles/<style>.md`
  3. Базовый шаблон из `references/base-prompt.md`
  4. Структурированный контент из Шага 2
  5. Весь текст на подтверждённом языке


**Разрешение соотношения сторон** для `{{ASPECT_RATIO}}`:
  * Именованные пресеты → строка соотношения: landscape→`16:9`, portrait→`9:16`, square→`1:1`
  * Пользовательские W:H → используйте как есть (например, `3:4`, `4:3`, `2.35:1`)


Сохраните собранный промпт в `prompts/infographic.md` с помощью `write_file`.
### Step 6: Generate Image[​](<#step-6-generate-image> "Direct link to Step 6: Generate Image")
Используйте инструмент `image_generate` с собранным промптом из Шага 5.
  * Преобразуйте соотношение сторон в формат image_generate: `16:9` → `landscape`, `9:16` → `portrait`, `1:1` → `square`
  * Для пользовательских соотношений выберите ближайшее именованное
  * При сбое автоматически повторите один раз
  * Сохраните полученный URL/путь изображения в выходную директорию


### Step 7: Output Summary[​](<#step-7-output-summary> "Direct link to Step 7: Output Summary")
Отчёт: тема, макет, стиль, соотношение, язык, путь вывода, созданные файлы.
## References[​](<#references> "Direct link to References")
  * `references/analysis-framework.md` — Методология анализа
  * `references/structured-content-template.md` — Формат контента
  * `references/base-prompt.md` — Шаблон промпта
  * `references/layouts/<layout>.md` — 21 определение макета
  * `references/styles/<style>.md` — 21 определение стиля


## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  1. **Целостность данных имеет первостепенное значение** — никогда не обобщайте, не перефразируйте и не изменяйте исходные статистики. «73% increase» должно остаться «73% increase», а не «значительное увеличение».
  2. **Удаляйте секреты** — всегда проверяйте исходный контент на API-ключи, токены или учётные данные перед включением в любой выходной файл.
  3. **Одно сообщение на секцию** — каждая секция инфографики должна передавать одну чёткую концепцию. Перегрузка секций снижает читаемость.
  4. **Согласованность стиля** — определение стиля из файла референсов должно применяться единообразно ко всей инфографике. Не смешивайте стили.
  5. **Соотношения сторон image_generate** — инструмент поддерживает только `landscape`, `portrait` и `square`. Пользовательские соотношения вроде `3:4` должны преобразовываться в ближайшую опцию (portrait в этом случае).


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Options](<#options>)
  * [Layout Gallery](<#layout-gallery>)
  * [Style Gallery](<#style-gallery>)
  * [Recommended Combinations](<#recommended-combinations>)
  * [Keyword Shortcuts](<#keyword-shortcuts>)
  * [Output Structure](<#output-structure>)
  * [Core Principles](<#core-principles>)
  * [Workflow](<#workflow>)
    * [Step 1: Analyze Content](<#step-1-analyze-content>)
    * [Step 2: Generate Structured Content → `structured-content.md`](<#step-2-generate-structured-content--structured-contentmd>)
    * [Step 3: Recommend Combinations](<#step-3-recommend-combinations>)
    * [Step 4: Confirm Options](<#step-4-confirm-options>)
    * [Step 5: Generate Prompt → `prompts/infographic.md`](<#step-5-generate-prompt--promptsinfographicmd>)
    * [Step 6: Generate Image](<#step-6-generate-image>)
    * [Step 7: Output Summary](<#step-7-output-summary>)
  * [References](<#references>)
  * [Pitfalls](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-baoyu-infographic -->
