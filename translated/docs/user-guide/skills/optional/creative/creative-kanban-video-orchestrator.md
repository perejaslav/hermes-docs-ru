На этой странице
Планирование, настройка и мониторинг многопрофильного конвейера производства видео на базе Hermes Kanban. Используйте, когда пользователь хочет создать ЛЮБОЕ видео — нарративный фильм, продуктовый/маркетинговый ролик, музыкальный клип, объясняющее видео, ASCII/терминальное искусство, абстрактный/генеративный цикл, комикс, 3D, инсталляцию реального времени — и задача оправдывает декомпозицию на специализированные профили (сценарист, дизайнер, аниматор, рендерер, озвучка, монтажёр и т.д.), координируемые через канбан-доску. Выполняет адаптивный опрос для уточнения брифа, проектирует подходящую команду для запрошенного стиля, генерирует скрипт настройки, создающий профили Hermes + начальную задачу канбана, затем помогает отслеживать выполнение и вмешиваться, когда задачи застревают или терпят неудачу. Направляет сцены к тем навыкам рендеринга/аудио/дизайна Hermes, которые подходят под каждый такт (`ascii-video`, `manim-video`, `p5js`, `comfyui`, `touchdesigner-mcp`, `blender-mcp`, `pixel-art`, `baoyu-comic`, `claude-design`, `excalidraw`, `songsee`, `heartmula`, …), а также к внешним API для TTS, генерации изображений и преобразования изображений в видео по мере необходимости.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Опциональный — установка через `hermes skills install official/creative/kanban-video-orchestrator`  |
|Путь| `optional-skills/creative/kanban-video-orchestrator`  |
|Версия| `1.0.0`  |
|Автор| ['SHL0MS', 'alt-glitch']  |
|Лицензия| MIT  |
|Теги| `video`, `kanban`, `multi-agent`, `orchestration`, `production-pipeline`  |
|Связанные навыки| [`kanban-orchestrator`](</docs/user-guide/skills/bundled/devops/devops-kanban-orchestrator>), [`kanban-worker`](</docs/user-guide/skills/bundled/devops/devops-kanban-worker>), [`ascii-video`](</docs/user-guide/skills/bundled/creative/creative-ascii-video>), [`manim-video`](</docs/user-guide/skills/bundled/creative/creative-manim-video>), [`p5js`](</docs/user-guide/skills/bundled/creative/creative-p5js>), [`comfyui`](</docs/user-guide/skills/bundled/creative/creative-comfyui>), [`touchdesigner-mcp`](</docs/user-guide/skills/bundled/creative/creative-touchdesigner-mcp>), [`blender-mcp`](</docs/user-guide/skills/optional/creative/creative-blender-mcp>), [`pixel-art`](</docs/user-guide/skills/bundled/creative/creative-pixel-art>), [`ascii-art`](</docs/user-guide/skills/bundled/creative/creative-ascii-art>), [`songwriting-and-ai-music`](</docs/user-guide/skills/bundled/creative/creative-songwriting-and-ai-music>), [`heartmula`](</docs/user-guide/skills/bundled/media/media-heartmula>), [`songsee`](</docs/user-guide/skills/bundled/media/media-songsee>), [`spotify`](</docs/user-guide/skills/bundled/media/media-spotify>), [`youtube-content`](</docs/user-guide/skills/bundled/media/media-youtube-content>), [`claude-design`](</docs/user-guide/skills/bundled/creative/creative-claude-design>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>), [`architecture-diagram`](</docs/user-guide/skills/bundled/creative/creative-architecture-diagram>), [`concept-diagrams`](</docs/user-guide/skills/optional/creative/creative-concept-diagrams>), [`baoyu-comic`](</docs/user-guide/skills/bundled/creative/creative-baoyu-comic>), [`baoyu-infographic`](</docs/user-guide/skills/bundled/creative/creative-baoyu-infographic>), [`humanizer`](</docs/user-guide/skills/bundled/creative/creative-humanizer>), [`gif-search`](</docs/user-guide/skills/bundled/media/media-gif-search>), [`meme-generation`](</docs/user-guide/skills/optional/creative/creative-meme-generation>), [`photon-flux`](</docs/user-guide/skills/optional/creative/creative-photon-flux>), [`hermes-agent`](</docs/user-guide/skills/bundled/productivity/productivity-hermes-agent>), [`systematic-debugging`](</docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging>), [`manim-math-viz`](</docs/user-guide/skills/optional/creative/creative-manim-math-viz>), [`touchdesigner-cc`](</docs/user-guide/skills/optional/creative/creative-touchdesigner-cc>), [`desync-motif`](</docs/user-guide/skills/optional/creative/creative-desync-motif>), [`binary-music`](</docs/user-guide/skills/optional/creative/creative-binary-music>), [`hypermaze`](</docs/user-guide/skills/optional/creative/creative-hypermaze>), [`infinite-canvas-mural`](</docs/user-guide/skills/optional/creative/creative-infinite-canvas-mural>), [`particle-life`](</docs/user-guide/skills/optional/creative/creative-particle-life>), [`slime-mold`](</docs/user-guide/skills/optional/creative/creative-slime-mold>), [`spiral-gallery`](</docs/user-guide/skills/optional/creative/creative-spiral-gallery>), [`stochastic-musical-text`](</docs/user-guide/skills/optional/creative/creative-stochastic-musical-text>), [`mandelbrot-explorer`](</docs/user-guide/skills/optional/creative/creative-mandelbrot-explorer>), [`breath-visualization`](</docs/user-guide/skills/optional/creative/creative-breath-visualization>), [`life-in-words`](</docs/user-guide/skills/optional/creative/creative-life-in-words>), [`gol-sim`](</docs/user-guide/skills/optional/creative/creative-gol-sim>), [`color-picker`](</docs/user-guide/skills/optional/creative/creative-color-picker>), [`color-theory`](</docs/user-guide/skills/optional/creative/creative-color-theory>), [`eye-tracking-heatmap`](</docs/user-guide/skills/optional/creative/creative-eye-tracking-heatmap>), [`ink-art`](</docs/user-guide/skills/optional/creative/creative-ink-art>), [`marble-run`](</docs/user-guide/skills/optional/creative/creative-marble-run>), [`mono-repo`](</docs/user-guide/skills/optional/devops/devops-mono-repo>), [`revision-history`](</docs/user-guide/skills/bundled/productivity/productivity-revision-history>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что видит агент в качестве инструкций, когда навык активен.
# Kanban Video Orchestrator
Оборачивает любой видео-запрос — от 15-секундного тизера продукта до 5-минутного нарративного короткометражного фильма, музыкального клипа или ASCII-цикла — в конвейер Hermes Kanban, который декомпозирует работу на специализированные профили агентов.
Этот навык **не** выполняет рендеринг самостоятельно. Это мета-конвейер, который:
  1. **Определяет объём** запроса через целевой опрос
  2. **Проектирует** подходящую команду (какие роли, какие инструменты для каждой роли) на основе стиля
  3. **Генерирует** скрипт настройки, создающий профили Hermes, рабочее пространство проекта и начальную задачу канбана
  4. **Передаёт управление** профилю режиссёра, который декомпозирует задачу через канбан
  5. **Отслеживает** выполнение, помогает вмешиваться, когда задачи застревают или терпят неудачу


Фактический рендеринг происходит внутри канбана после его запуска, через существующие навыки и инструменты, подходящие для каждой сцены — `ascii-video`, `manim-video`, `p5js`, `comfyui`, `touchdesigner-mcp`, `blender-mcp`, `songwriting-and-ai-music`, `heartmula`, внешние API или обычный Python с PIL + ffmpeg.
## Когда НЕ использовать этот навык[​](<#when-not-to-use-this-skill> "Прямая ссылка на Когда НЕ использовать этот навык")
  * Видео представляет собой один непрерывный процедурный проект, не требующий специалистов. Просто напишите код напрямую.
  * Пользователь хочет быстрое одноразовое преобразование (например, «конвертировать этот mp4 в GIF») — используйте ffmpeg напрямую.
  * Результат — статическое изображение, GIF или только аудио — используйте соответствующий специализированный навык (`ascii-art`, `gifs`, `meme-generation`, `songwriting-and-ai-music`).
  * Работа полностью укладывается в один существующий навык (например, чисто ASCII-видео — просто используйте `ascii-video`).


## Рабочий процесс[​](<#workflow> "Прямая ссылка на Рабочий процесс")
[code] 
    DISCOVER  →  BRIEF  →  TEAM DESIGN  →  SETUP  →  EXECUTE  →  MONITOR  
    
[/code]
### Шаг 1 — Опрос (задайте правильные вопросы)[​](<#step-1--discover-ask-the-right-questions> "Прямая ссылка на Шаг 1 — Опрос \\(задайте правильные вопросы\\)")
Процесс опроса **адаптивный**: спрашивайте только то, что действительно нужно. Всегда начинайте с трёх вопросов, чтобы определить общий контур:
  * **Что это за видео?** (краткое описание в одно предложение)
  * **Какой длительности?** (5-30 сек тизер / 30-90 сек короткометражка / 90 сек-3 мин объясняющее / 3-10 мин фильм / длиннее)
  * **Какое соотношение сторон и целевая платформа?** (1:1 / 9:16 / 16:9; X, IG, YouTube, внутреннее и т.д.)


Исходя из ответа, классифицируйте категорию стиля. Стиль определяет, какие дополнительные вопросы задавать. **Не задавайте все вопросы сразу.** Спрашивайте по 2-4 за раз, слушайте, затем продолжайте. Делайте разумные предположения, когда пользователь подразумевает ответ.
Полные шаблоны сбора информации и наборы вопросов по стилям см. в **[references/intake.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/kanban-video-orchestrator/references/intake.md>)**.
### Шаг 2 — Бриф[​](<#step-2--brief> "Прямая ссылка на Шаг 2 — Бриф")
Когда информации достаточно, создайте структурированный `brief.md`, используя шаблон из `assets/brief.md.tmpl`. Этапы:
  1. **Концепция** — питч в одно предложение + эмоциональный ориентир
  2. **Объём** — длительность, соотношение сторон, платформа, срок
  3. **Стиль** — визуальные референсы, брендовые ограничения, тон
  4. **Сцены** — покадровая разбивка (длительности, содержание, целевой инструмент)
  5. **Аудио** — озвучка / музыка / звуковые эффекты / тишина (по сценам при необходимости)
  6. **Результаты** — формат файла, разрешение, опциональные альтернативы (вертикальная версия, GIF и т.д.)


Покажите бриф пользователю для подтверждения перед проектированием команды. **Бриф — это контракт** — каждая последующая задача ссылается на него.
### Шаг 3 — Проектирование команды[​](<#step-3--team-design> "Прямая ссылка на Шаг 3 — Проектирование команды")
Выберите архетипы ролей из библиотеки, подходящие для этого видео. **Комбинируйте, не копируйте.** Большинству видео требуется 4-7 профилей. Режиссёр присутствует всегда; остальные выбираются исходя из того, что действительно требуется по брифингу.
Библиотеку ролей и составы команд по стилям см. в **[references/role-archetypes.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/kanban-video-orchestrator/references/role-archetypes.md>)**.
Соответствие ролей навыкам и инструментам Hermes см. в **[references/tool-matrix.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/kanban-video-orchestrator/references/tool-matrix.md>)**.
### Шаг 4 — Настройка[​](<#step-4--setup> "Прямая ссылка на Шаг 4 — Настройка")
Сгенерируйте скрипт настройки (`setup.sh`) и запустите его. Скрипт:
  1. Создаёт рабочее пространство проекта (`~/projects/video-pipeline/<slug>/`)
  2. Копирует предоставленные ресурсы в `taste/`, `audio/`, `assets/`
  3. Создаёт каждый профиль Hermes через `hermes profile create --clone`
  4. Записывает `SOUL.md` для каждого профиля (личность + определение роли)
  5. Конфигурирует YAML профилей (наборы инструментов, навыки always_load, рабочая директория)
  6. Записывает `brief.md`, `TEAM.md` и содержимое `taste/`
  7. Запускает начальную задачу `hermes kanban create`, назначенную режиссёру


Используйте `scripts/bootstrap_pipeline.py` для генерации setup.sh из брифа + JSON-описания команды. См. **[references/kanban-setup.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/kanban-video-orchestrator/references/kanban-setup.md>)** для структуры скрипта настройки, шаблонов конфигурации профилей и критически важного правила «общего рабочего пространства».
### Шаг 5 — Выполнение[​](<#step-5--execute> "Прямая ссылка на Шаг 5 — Выполнение")
Запустите `setup.sh`. Затем предоставьте пользователю команды для мониторинга:
[code] 
    hermes kanban watch --tenant <project-tenant>     # события в реальном времени  
    hermes kanban list  --tenant <project-tenant>     # снимок доски  
    hermes dashboard                                   # визуальный интерфейс доски  
    
[/code]
Профиль режиссёра берёт управление на себя, декомпозируя работу и направляя задачи специализированным профилям через инструментарий канбана.
### Шаг 6 — Мониторинг и вмешательство[​](<#step-6--monitor-and-intervene> "Прямая ссылка на Шаг 6 — Мониторинг и вмешательство")
Оставайтесь вовлечённым — канбан работает автономно, но застрявшая задача или некорректный результат требуют человеческого (или ИИ) суждения.
Паттерны мониторинга: периодически опрашивайте `kanban list`, инспектируйте любую задачу в статусе RUNNING, превысившую ожидаемую длительность, через `kanban show <id>`, и проверяйте heartbeats. Когда результат работы воркера не проходит проверку, стандартные меры вмешательства:
  1. Оставить комментарий к задаче воркера с конкретной обратной связью (`kanban_comment`)
  2. Создать задачу на повторный запуск с исходной задачей в качестве родительской
  3. Скорректировать объём брифа и позволить режиссёру выполнить повторную декомпозицию


О паттернах диагностики, рецептах вмешательства и сценарии «задача застряла» см. **[references/monitoring.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/kanban-video-orchestrator/references/monitoring.md>)**.
## Справочник: примеры работ[​](<#reference-worked-examples> "Прямая ссылка на Справочник: примеры работ")
Шесть конкретных конвейеров, охватывающих совершенно разные стили видео — нарративный фильм, продуктовый/маркетинговый ролик, музыкальный клип, объясняющее видео по математике/алгоритмам, ASCII-видео, инсталляция реального времени — показывающих, как один и тот же рабочий процесс приводит к совершенно разным командам и графам задач. См. **[references/examples.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/kanban-video-orchestrator/references/examples.md>)**.
## Критически важные правила[​](<#critical-rules> "Прямая ссылка на Критически важные правила")
  1. **Сначала опрос, потом действие.** Никогда не начинайте генерировать бриф или команду, не задав как минимум три базовых вопроса. Плохой бриф каскадно влияет на весь конвейер.
  2. **Подбирайте команду под видео.** Не используйте один и тот же набор из 4 профилей для каждой задачи. Музыкальный клип без профиля анализа битов даст сбой. Нарративный фильм без профиля сценариста создаст бессвязные сцены. См. `references/role-archetypes.md`.
  3. **Одно рабочее пространство на проект.** Все профили для данного видео используют общее рабочее пространство `dir:`. Задачи передают артефакты через общую файловую систему и структурированные передачи. **Каждый** вызов `kanban_create` передаёт `workspace_kind="dir"` + `workspace_path="<абсолютный путь к проекту>"`.
  4. **Тенант для каждого проекта.** Используйте тенант, специфичный для проекта (`--tenant <project-slug>`). Это сохраняет область видимости дашборда и предотвращает перекрёстное загрязнение с другими активными канбанами.
  5. **Уважайте существующие навыки.** Когда сцена подходит под существующий навык, соответствующий рендерер должен загружать этот навык через `--skill <name>` в своей задаче или `always_load` в своём профиле. Не изобретайте заново то, что уже предоставляет навык.
  6. **Режиссёр никогда не выполняет.** Даже с полным набором инструментов `kanban + terminal + file`, правила `SOUL.md` режиссёра запрещают ему выполнять работу самостоятельно. Он только декомпозирует и направляет — каждая конкретная задача становится вызовом `hermes kanban create` для специализированного профиля. Навык `kanban-orchestrator` подробнее раскрывает это.
  7. **Не пере-декомпозируйте.** 30-секундному видеоролику продукта НЕ нужно 20 задач. Стремитесь к минимальному графу задач, который всё ещё хорошо параллелится и предоставляет правильные точки проверки человеком.
  8. **Проверяйте API-ключи ДО запуска.** Внешние API (TTS, генерация изображений, image-to-video) требуют ключи в `~/.hermes/.env` или в хранилище секретов пользователя. Воркер, наткнувшийся на ошибку отсутствующего ключа, тратит слот задачи впустую. Хелпер `check_key` в скрипте настройки чисто завершает работу, если требуемый ключ отсутствует.


## Карта файлов[​](<#file-map> "Прямая ссылка на Карта файлов")
[code] 
    SKILL.md                            ← этот файл (рабочий процесс + правила)  
    references/  
      intake.md                         ← наборы вопросов для опроса по стилям  
      role-archetypes.md                ← библиотека ролей (сценарист, дизайнер, аниматор, …)  
      tool-matrix.md                    ← соответствие навыков и инструментов для каждой роли  
      kanban-setup.md                   ← структура скрипта настройки и конфигурация профилей  
      monitoring.md                     ← паттерны наблюдения и вмешательства  
      examples.md                       ← шесть проработанных конвейеров  
    assets/  
      brief.md.tmpl                     ← шаблон брифа  
      setup.sh.tmpl                     ← шаблон скрипта настройки  
      soul.md.tmpl                      ← шаблон личности профиля  
    scripts/  
      bootstrap_pipeline.py             ← генерация setup.sh из брифа + JSON команды  
      monitor.py                        ← хелперы для опроса и вмешательства  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда НЕ использовать этот навык](<#when-not-to-use-this-skill>)
  * [Рабочий процесс](<#workflow>)
    * [Шаг 1 — Опрос (задайте правильные вопросы)](<#step-1--discover-ask-the-right-questions>)
    * [Шаг 2 — Бриф](<#step-2--brief>)
    * [Шаг 3 — Проектирование команды](<#step-3--team-design>)
    * [Шаг 4 — Настройка](<#step-4--setup>)
    * [Шаг 5 — Выполнение](<#step-5--execute>)
    * [Шаг 6 — Мониторинг и вмешательство](<#step-6--monitor-and-intervene>)
  * [Справочник: примеры работ](<#reference-worked-examples>)
  * [Критически важные правила](<#critical-rules>)
  * [Карта файлов](<#file-map>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-kanban-video-orchestrator -->
