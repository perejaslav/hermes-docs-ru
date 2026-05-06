On this page
Knowledge comics (知识漫画): образовательные, биографические, обучающие.
## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/creative/baoyu-comic` |
|Версия| `1.56.1` |
|Автор| 宝玉 (JimLiu) |
|Лицензия| MIT |
|Теги| `comic`, `knowledge-comic`, `creative`, `image-generation` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это те инструкции, которые видит агент, когда навык активен.
# Knowledge Comic Creator
Адаптировано из [baoyu-comic](<https://github.com/JimLiu/baoyu-skills>) для экосистемы инструментов Hermes Agent.
Создавайте оригинальные образовательные комиксы с гибкими комбинациями стиля рисования и тона.
## Когда использовать[​](<#when-to-use> "Direct link to When to Use")
Активируйте этот навык, когда пользователь просит создать образовательный/познавательный комикс, комикс-биографию, обучающий комикс или использует такие термины, как «知识漫画», «教育漫画» или «в стиле Logicomix». Пользователь предоставляет контент (текст, путь к файлу, URL или тему) и, опционально, указывает стиль рисования, тон, макет, соотношение сторон или язык.
## Референтные изображения[​](<#reference-images> "Direct link to Reference Images")
Инструмент `image_generate` в Hermes — **только по промпту** — он принимает текстовый промпт и соотношение сторон и возвращает URL изображения. Он **НЕ** принимает референтные изображения. Если пользователь предоставляет референтное изображение, используйте его для **извлечения характеристик в текст**, которые встраиваются в каждый промпт страницы:
**Приём** : Принимайте пути к файлам, когда пользователь их предоставляет (или вставляет изображения в разговор).
  * Путь(и) к файлу → скопируйте в `refs/NN-ref-{slug}.{ext}` рядом с выходным комиксом для отслеживания происхождения
  * Вставленное изображение без пути → запросите путь у пользователя через `clarify`, или извлеките стилевые характеристики вербально как текстовый запасной вариант
  * Нет референса → пропустите этот раздел


**Режимы использования** (на референс):
Использование| Эффект  
---|---
`style`| Извлечение стилевых характеристик (штрихи, текстура, настроение) и добавление к каждому промпту страницы  
`palette`| Извлечение HEX-цветов и добавление к каждому промпту страницы  
`scene`| Извлечение композиции сцены или заметок о субъекте и добавление к соответствующим страницам  
**Записывайте в frontmatter промпта каждой страницы** при наличии референсов:
[code] 
    references:  
      - ref_id: 01  
        filename: 01-ref-scene.png  
        usage: style  
        traits: "muted earth tones, soft-edged ink wash, low-contrast backgrounds"  
    
[/code]
Согласованность персонажей обеспечивается **текстовыми описаниями** в `characters/characters.md` (создаётся на Шаге 3), которые встраиваются в каждый промпт страницы (Шаг 5). Опциональный PNG-лист персонажей, созданный на Шаге 7.1, — это артефакт для просмотра человеком, а не входной параметр для `image_generate`.
## Опции[​](<#options> "Direct link to Options")
### Визуальные параметры[​](<#visual-dimensions> "Direct link to Visual Dimensions")
Опция| Значения| Описание  
---|---|---
Art| ligne-claire (по умолч.), manga, realistic, ink-brush, chalk, minimalist| Стиль рисования / техника рендеринга  
Tone| neutral (по умолч.), warm, dramatic, romantic, energetic, vintage, action| Настроение / атмосфера  
Layout| standard (по умолч.), cinematic, dense, splash, mixed, webtoon, four-panel| Расположение панелей  
Aspect| 3:4 (по умолч., портрет), 4:3 (ландшафт), 16:9 (широкий экран)| Соотношение сторон страницы  
Language| auto (по умолч.), zh, en, ja и др.| Язык вывода  
Refs| Пути к файлам| Референтные изображения для извлечения стилевых/палитрных характеристик (не передаются модели генерации изображений). См. [Референтные изображения](<#reference-images>) выше.  
### Опции частичного рабочего процесса[​](<#partial-workflow-options> "Direct link to Partial Workflow Options")
Опция| Описание  
---|---
Storyboard only| Создать только раскадровку, пропустить промпты и изображения  
Prompts only| Создать раскадровку + промпты, пропустить изображения  
Images only| Создать изображения из существующего каталога промптов  
Regenerate N| Перегенерировать только указанные страницы (напр., `3` или `2,5,8`)  
Подробности: [references/partial-workflows.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/partial-workflows.md>)
### Каталог стилей, тонов и пресетов[​](<#art-tone--preset-catalogue> "Direct link to Art, Tone & Preset Catalogue")
  * **Стили рисования** (6): `ligne-claire`, `manga`, `realistic`, `ink-brush`, `chalk`, `minimalist`. Полные определения в `references/art-styles/<style>.md`.
  * **Тоны** (7): `neutral`, `warm`, `dramatic`, `romantic`, `energetic`, `vintage`, `action`. Полные определения в `references/tones/<tone>.md`.
  * **Пресеты** (5) с особыми правилами, выходящими за рамки простого стиль+тон:
Пресет| Эквивалент| Особенность  
---|---|---
`ohmsha`| manga + neutral| Визуальные метафоры, без «говорящих голов», раскрытие гаджетов  
`wuxia`| ink-brush + action| Эффекты ци, боевая графика, атмосферность  
`shoujo`| manga + romantic| Декоративные элементы, детали глаз, романтические сцены  
`concept-story`| manga + warm| Система визуальных символов, арка роста, баланс диалогов и действия  
`four-panel`| minimalist + neutral + four-panel layout| Структура 起承转合, Ч/Б + акцентный цвет, стикмен-персонажи  
Полные правила в `references/presets/<preset>.md` — загрузите файл при выборе пресета.
  * **Матрица совместимости** и таблица **контент-сигнал → пресет** находятся в [references/auto-selection.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/auto-selection.md>). Прочитайте перед рекомендацией комбинаций на Шаге 2.


## Файловая структура[​](<#file-structure> "Direct link to File Structure")
Каталог вывода: `comic/{topic-slug}/`
  * Slug: 2-4 слова в kebab-case из темы (напр., `alan-turing-bio`)
  * Конфликт: добавить метку времени (напр., `turing-story-20260118-143052`)


**Содержимое** :
Файл| Описание  
---|---
`source-{slug}.md`| Сохранённый исходный контент (slug в kebab-case совпадает с каталогом вывода)  
`analysis.md`| Анализ контента  
`storyboard.md`| Раскадровка с разбивкой по панелям  
`characters/characters.md`| Определения персонажей  
`characters/characters.png`| Референтный лист персонажей (скачивается из `image_generate`)  
`prompts/NN-{cover|page}-[slug].md`| Промпты для генерации  
`NN-{cover|page}-[slug].png`| Сгенерированные изображения (скачиваются из `image_generate`)  
`refs/NN-ref-{slug}.{ext}`| Референтные изображения от пользователя (опционально, для отслеживания происхождения)  
## Обработка языка[​](<#language-handling> "Direct link to Language Handling")
**Приоритет определения** :
  1. Язык, указанный пользователем (явная опция)
  2. Язык разговора пользователя
  3. Язык исходного контента


**Правило** : Используйте язык ввода пользователя для ВСЕХ взаимодействий:
  * Структура раскадровки и описания сцен
  * Промпты для генерации изображений
  * Опции выбора для пользователя и подтверждения
  * Обновления прогресса, вопросы, ошибки, сводки


Технические термины остаются на английском.
## Рабочий процесс[​](<#workflow> "Direct link to Workflow")
### Контрольный список прогресса[​](<#progress-checklist> "Direct link to Progress Checklist")
[code] 
    Comic Progress:  
    - [ ] Step 1: Setup & Analyze  
      - [ ] 1.1 Analyze content  
      - [ ] 1.2 Check existing directory  
    - [ ] Step 2: Confirmation - Style & options ⚠️ REQUIRED  
    - [ ] Step 3: Generate storyboard + characters  
    - [ ] Step 4: Review outline (conditional)  
    - [ ] Step 5: Generate prompts  
    - [ ] Step 6: Review prompts (conditional)  
    - [ ] Step 7: Generate images  
      - [ ] 7.1 Generate character sheet (if needed) → characters/characters.png  
      - [ ] 7.2 Generate pages (with character descriptions embedded in prompt)  
    - [ ] Step 8: Completion report  
    
[/code]
### Поток[​](<#flow> "Direct link to Flow")
[code] 
    Input → Analyze → [Check Existing?] → [Confirm: Style + Reviews] → Storyboard → [Review?] → Prompts → [Review?] → Images → Complete  
    
[/code]
### Сводка шагов[​](<#step-summary> "Direct link to Step Summary")
Шаг| Действие| Ключевой результат  
---|---|---
1.1| Анализ контента| `analysis.md`, `source-{slug}.md`  
1.2| Проверка существующего каталога| Обработка конфликтов  
2| Подтверждение стиля, фокуса, аудитории, ревью| Предпочтения пользователя  
3| Создание раскадровки + персонажей| `storyboard.md`, `characters/`  
4| Ревью структуры (если запрошено)| Одобрение пользователя  
5| Создание промптов| `prompts/*.md`  
6| Ревью промптов (если запрошено)| Одобрение пользователя  
7.1| Создание листа персонажей (если нужно)| `characters/characters.png`  
7.2| Генерация страниц| `*.png` файлы  
8| Отчёт о завершении| Сводка  
### Вопросы пользователю[​](<#user-questions> "Direct link to User Questions")
Используйте инструмент `clarify` для подтверждения опций. Поскольку `clarify` обрабатывает один вопрос за раз, задавайте сначала самый важный вопрос и действуйте последовательно. Полный набор вопросов Шага 2 см. в [references/workflow.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/workflow.md>).
**Обработка тайм-аута (КРИТИЧНО)** : `clarify` может вернуть `"The user did not provide a response within the time limit. Use your best judgement to make the choice and proceed."` — это НЕ является согласием пользователя на всё по умолчанию.
  * Считайте это значением по умолчанию **только для этого одного вопроса**. Продолжайте задавать остальные вопросы Шага 2 последовательно; каждый вопрос — независимая точка согласия.
  * **Явно показывайте значение по умолчанию пользователю** в вашем следующем сообщении, чтобы у него была возможность исправить: например, `«Стиль: по умолчанию выбран пресет ohmsha (clarify превысил тайм-аут). Скажите слово, чтобы изменить.»` — незадокументированное значение по умолчанию неотличимо от ситуации, когда вопрос никогда не задавался.
  * НЕ сворачивайте Шаг 2 в единый проход «использовать все значения по умолчанию» после одного тайм-аута. Если пользователь действительно отсутствует, он с равной вероятностью будет отсутствовать на все пять вопросов — но он может исправить видимые значения по умолчанию, когда вернётся, и не может исправить невидимые.


### Шаг 7: Генерация изображений[​](<#step-7-image-generation> "Direct link to Step 7: Image Generation")
Используйте встроенный инструмент Hermes `image_generate` для всего рендеринга изображений. Его схема принимает только `prompt` и `aspect_ratio` (`landscape` | `portrait` | `square`); он **возвращает URL**, а не локальный файл. Каждая сгенерированная страница или лист персонажей должны быть скачаны в каталог вывода.
**Требование к файлу промпта (жёсткое)** : записывайте полный, финальный промпт каждого изображения в отдельный файл в каталоге `prompts/` (именование: `NN-{type}-[slug].md`) ПЕРЕД вызовом `image_generate`. Файл промпта — это запись воспроизводимости.
**Сопоставление соотношений сторон** — поле `aspect_ratio` раскадровки сопоставляется с форматом `image_generate` следующим образом:
Соотношение раскадровки| Формат `image_generate`  
---|---
`3:4`, `9:16`, `2:3`| `portrait`  
`4:3`, `16:9`, `3:2`| `landscape`  
`1:1`| `square`  
**Шаг скачивания** — после каждого вызова `image_generate`:
  1. Прочитайте URL из результата инструмента
  2. Получите байты изображения, используя **абсолютный** путь вывода, например: `curl -fsSL "<url>" -o /abs/path/to/comic/<slug>/NN-page-<slug>.png`
  3. Проверьте, что файл существует и не пуст по этому точному пути, прежде чем переходить к следующей странице


**Никогда не полагайтесь на сохранение CWD оболочки между батчами для путей`-o`.** CWD постоянной оболочки терминального инструмента может измениться между батчами (истечение сессии, `TERMINAL_LIFETIME_SECONDS`, неудачный `cd`, оставляющий вас в неправильном каталоге). `curl -o relative/path.png` — это тихая мина: если CWD сместился, файл окажется в другом месте без ошибки. **Всегда передавайте полностью квалифицированный абсолютный путь в`-o`**, или передавайте `workdir=<abs path>` в терминальный инструмент. Инцидент, апрель 2026: страницы 06-09 10-страничного комика оказались в корне репозитория вместо `comic/<slug>/`, потому что батч 3 унаследовал устаревший CWD от батча 2, и `curl -o 06-page-skills.png` записал в неправильный каталог. Затем агент несколько тактов утверждал, что файлы существуют там, где их не было.
**7.1 Лист персонажей** — создавайте его (в `characters/characters.png`, aspect `landscape`), если комикс многостраничный с повторяющимися персонажами. Пропустите для простых пресетов (например, four-panel minimalist) или одностраничных комиксов. Файл промпта `characters/characters.md` должен существовать ДО вызова `image_generate`. Созданный PNG — это **артефакт для просмотра человеком** (чтобы пользователь мог визуально проверить дизайн персонажа) и референс для последующих регенераций или ручных правок промптов — он **не** управляет Шагом 7.2. Промпты страниц уже написаны на Шаге 5 на основе **текстовых описаний** в `characters/characters.md`; `image_generate` не может принимать изображения как визуальный вход.
**7.2 Страницы** — промпт каждой страницы ОБЯЗАТЕЛЬНО должен уже находиться в `prompts/NN-{cover|page}-[slug].md` перед вызовом `image_generate`. Поскольку `image_generate` работает только по промпту, согласованность персонажей обеспечивается **встраиванием описаний персонажей (из`characters/characters.md`) в каждый промпт страницы на Шаге 5**. Встраивание выполняется единообразно независимо от того, был ли создан PNG-лист на шаге 7.1; PNG — только вспомогательное средство для ревью/регенерации.
**Правило резервирования** : существующие файлы `prompts/…md` и `…png` → переименовать с суффиксом `-backup-YYYYMMDD-HHMMSS` перед регенерацией.
Полный пошаговый рабочий процесс (анализ, раскадровка, этапы ревью, варианты регенерации): [references/workflow.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/workflow.md>).
## Ссылки[​](<#references> "Direct link to References")
**Основные шаблоны** :
  * [analysis-framework.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/analysis-framework.md>) \\- Глубокий анализ контента
  * [character-template.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/character-template.md>) \\- Формат определения персонажей
  * [storyboard-template.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/storyboard-template.md>) \\- Структура раскадровки
  * [ohmsha-guide.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/ohmsha-guide.md>) \\- Особенности манги Ohmsha


**Определения стилей** :
  * `references/art-styles/` \\- Стили рисования (ligne-claire, manga, realistic, ink-brush, chalk, minimalist)
  * `references/tones/` \\- Тоны (neutral, warm, dramatic, romantic, energetic, vintage, action)
  * `references/presets/` \\- Пресеты с особыми правилами (ohmsha, wuxia, shoujo, concept-story, four-panel)
  * `references/layouts/` \\- Макеты (standard, cinematic, dense, splash, mixed, webtoon, four-panel)


**Рабочий процесс** :
  * [workflow.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/workflow.md>) \\- Полные детали рабочего процесса
  * [auto-selection.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/auto-selection.md>) \\- Анализ сигналов контента
  * [partial-workflows.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/baoyu-comic/references/partial-workflows.md>) \\- Опции частичного рабочего процесса


## Модификация страниц[​](<#page-modification> "Direct link to Page Modification")
Действие| Шаги  
---|---
**Редактировать**| **Сначала обновить файл промпта** → перегенерировать изображение → скачать новый PNG  
**Добавить**| Создать промпт на позиции → сгенерировать с встроенными описаниями персонажей → перенумеровать последующие → обновить раскадровку  
**Удалить**| Удалить файлы → перенумеровать последующие → обновить раскадровку  
**ВАЖНО** : При обновлении страниц ВСЕГДА сначала обновляйте файл промпта (`prompts/NN-{cover|page}-[slug].md`) перед регенерацией. Это гарантирует, что изменения задокументированы и воспроизводимы.
## Ловушки[​](<#pitfalls> "Direct link to Pitfalls")
  * Генерация изображений: 10-30 секунд на страницу; автоматический повтор при сбое (один раз)
  * **Всегда скачивайте** URL, возвращённый `image_generate`, в локальный PNG — последующие инструменты (и просмотр пользователем) ожидают файлы в каталоге вывода, а не эфемерные URL
  * **Используйте абсолютные пути для`curl -o`** — никогда не полагайтесь на сохранение CWD постоянной оболочки между батчами. Тихая мина: файлы оказываются в неправильном каталоге, и последующий `ls` в ожидаемом пути ничего не показывает. См. Шаг 7 «Шаг скачивания».
  * Используйте стилизованные альтернативы для чувствительных публичных фигур
  * **Подтверждение на Шаге 2 обязательно** — не пропускайте
  * **Шаги 4/6 условны** — только если пользователь запросил на Шаге 2
  * **Шаг 7.1 лист персонажей** — рекомендуется для многостраничных комиксов, опционально для простых пресетов. PNG — вспомогательное средство для ревью/регенерации; промпты страниц (написанные на Шаге 5) используют текстовые описания из `characters/characters.md`, а не PNG. `image_generate` не принимает изображения как визуальный вход
  * **Удаляйте секреты** — сканируйте исходный контент на наличие API-ключей, токенов или учётных данных перед записью любого выходного файла


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Референтные изображения](<#reference-images>)
  * [Опции](<#options>)
    * [Визуальные параметры](<#visual-dimensions>)
    * [Опции частичного рабочего процесса](<#partial-workflow-options>)
    * [Каталог стилей, тонов и пресетов](<#art-tone--preset-catalogue>)
  * [Файловая структура](<#file-structure>)
  * [Обработка языка](<#language-handling>)
  * [Рабочий процесс](<#workflow>)
    * [Контрольный список прогресса](<#progress-checklist>)
    * [Поток](<#flow>)
    * [Сводка шагов](<#step-summary>)
    * [Вопросы пользователю](<#user-questions>)
    * [Шаг 7: Генерация изображений](<#step-7-image-generation>)
  * [Ссылки](<#references>)
  * [Модификация страниц](<#page-modification>)
  * [Ловушки](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-baoyu-comic -->
