On this page
Генерируйте плоские, минималистичные SVG-диаграммы с учётом светлой/тёмной темы в виде отдельных HTML-файлов, используя единый образовательный визуальный язык с 9 семантическими цветовыми градиентами, типографикой в предложном регистре и автоматической тёмной темой. Лучше всего подходит для образовательных и не-программных визуализаций — физические установки, химические механизмы, математические кривые, физические объекты (самолёты, турбины, смартфоны, механические часы), анатомия, планы этажей, поперечные сечения, повествовательные путешествия (жизненный цикл X, процесс Y), интеграционные системы типа «звезда» (умный город, Интернет вещей) и разнесённые слои. Если для темы существует более специализированный навык (специализированные программные/облачные архитектуры, рисунки от руки, анимированные объяснения и т.д.), используйте его — в противном случае данный навык может служить универсальным запасным вариантом SVG-диаграммы с чистым образовательным стилем. Поставляется с 15 примерами диаграмм.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
|Source| Опционально — установка: `hermes skills install official/creative/concept-diagrams`  |
|Path| `optional-skills/creative/concept-diagrams`  |
|Version| `0.1.0`  |
|Author| v1k22 (оригинальный PR), портировано в hermes-agent  |
|License| MIT  |
|Tags| `diagrams`, `svg`, `visualization`, `education`, `physics`, `chemistry`, `engineering`  |
|Related skills| [`architecture-diagram`](</docs/user-guide/skills/bundled/creative/creative-architecture-diagram>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>), `generative-widgets`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Concept Diagrams
Создавайте SVG-диаграммы продакшн-качества с единой плоской минималистичной системой дизайна. Результат — один самодостаточный HTML-файл, который одинаково отображается в любом современном браузере, с автоматическим переключением светлой/тёмной темы.
## Scope[​](<#scope> "Direct link to Scope")
**Наилучшее применение:**
  * Физические установки, химические механизмы, математические кривые, биология
  * Физические объекты (самолёты, турбины, смартфоны, механические часы, клетки)
  * Анатомия, поперечные сечения, разнесённые слои
  * Планы этажей, архитектурные перепланировки
  * Повествовательные путешествия (жизненный цикл X, процесс Y)
  * Интеграционные системы типа «звезда» (умный город, IoT-сети, электросети)
  * Образовательные / учебниковые визуализации в любой области
  * Количественные графики (группированные столбцы, энергетические профили)


**Сначала ищите в других навыках:**
  * Специализированная программная / облачная инфраструктурная архитектура с тёмной технической эстетикой (рассмотрите `architecture-diagram`, если доступно)
  * Рисунки от руки, как на доске (рассмотрите `excalidraw`, если доступно)
  * Анимированные объяснения или видео (рассмотрите навык анимации)


Если для темы доступен более специализированный навык, используйте его. Если ничего не подходит, данный навык может служить универсальным запасным вариантом SVG-диаграммы — результат будет иметь чистый образовательный стиль, описанный ниже, который является разумным выбором по умолчанию почти для любой темы.
## Workflow[​](<#workflow> "Direct link to Workflow")
  1. Определите тип диаграммы (см. Типы диаграмм ниже).
  2. Разместите компоненты, используя правила системы дизайна.
  3. Напишите полную HTML-страницу, используя `templates/template.html` как обёртку — вставьте ваш SVG туда, где в шаблоне указано `<!-- PASTE SVG HERE -->`.
  4. Сохраните как отдельный `.html` файл (например, `~/my-diagram.html` или `./my-diagram.html`).
  5. Пользователь открывает файл прямо в браузере — не нужен сервер, нет зависимостей.


Опционально: если пользователь хочет просматриваемую галерею из нескольких диаграмм, см. «Локальный сервер предпросмотра» внизу.
Загрузите HTML-шаблон:
[code] 
    skill_view(name="concept-diagrams", file_path="templates/template.html")  
    
[/code]
Шаблон встраивает полную CSS-систему дизайна (цветовые классы `c-*`, классы текста, переменные светлой/тёмной темы, стили маркеров стрелок). Сгенерированный SVG полагается на наличие этих классов на странице.
* * *
## Design System[​](<#design-system> "Direct link to Design System")
### Philosophy[​](<#philosophy> "Direct link to Philosophy")
  * **Плоский** : никаких градиентов, теней, размытия, свечения или неоновых эффектов.
  * **Минималистичный** : покажите суть. Никаких декоративных иконок внутри блоков.
  * **Консистентный** : одинаковые цвета, отступы, типографика и толщина линий во всех диаграммах.
  * **Готов к тёмной теме** : все цвета автоматически адаптируются через CSS-классы — не нужно создавать SVG для каждой темы отдельно.


### Color Palette[​](<#color-palette> "Direct link to Color Palette")
9 цветовых градиентов, каждый с 7 ступенями. Поместите имя класса на элемент `<g>` или фигуру; CSS шаблона обрабатывает обе темы.
Class| 50 (самый светлый)| 100| 200| 400| 600| 800| 900 (самый тёмный)  
|---|---|---|---|---|---|---|---  
`c-purple`| #EEEDFE| #CECBF6| #AFA9EC| #7F77DD| #534AB7| #3C3489| #26215C  
`c-teal`| #E1F5EE| #9FE1CB| #5DCAA5| #1D9E75| #0F6E56| #085041| #04342C  
`c-coral`| #FAECE7| #F5C4B3| #F0997B| #D85A30| #993C1D| #712B13| #4A1B0C  
`c-pink`| #FBEAF0| #F4C0D1| #ED93B1| #D4537E| #993556| #72243E| #4B1528  
`c-gray`| #F1EFE8| #D3D1C7| #B4B2A9| #888780| #5F5E5A| #444441| #2C2C2A  
`c-blue`| #E6F1FB| #B5D4F4| #85B7EB| #378ADD| #185FA5| #0C447C| #042C53  
`c-green`| #EAF3DE| #C0DD97| #97C459| #639922| #3B6D11| #27500A| #173404  
`c-amber`| #FAEEDA| #FAC775| #EF9F27| #BA7517| #854F0B| #633806| #412402  
`c-red`| #FCEBEB| #F7C1C1| #F09595| #E24B4A| #A32D2D| #791F1F| #501313  
#### Color Assignment Rules[​](<#color-assignment-rules> "Direct link to Color Assignment Rules")
Цвет кодирует **смысл** , а не последовательность. Никогда не перебирайте цвета как радугу.
  * Группируйте узлы по **категориям** — все узлы одного типа используют один цвет.
  * Используйте `c-gray` для нейтральных/структурных узлов (начало, конец, типовые шаги, пользователи).
  * Используйте **2-3 цвета на диаграмму** , не 6+.
  * Предпочитайте `c-purple`, `c-teal`, `c-coral`, `c-pink` для общих категорий.
  * Резервируйте `c-blue`, `c-green`, `c-amber`, `c-red` для семантического значения (информация, успех, предупреждение, ошибка).


Соответствие ступеней для светлой/тёмной темы (обрабатывается CSS шаблона — просто используйте класс):
  * Светлая тема: заливка 50 + обводка 600 + заголовок 800 / подзаголовок 600
  * Тёмная тема: заливка 800 + обводка 200 + заголовок 100 / подзаголовок 200


### Typography[​](<#typography> "Direct link to Typography")
Всего два размера шрифта. Без исключений.
Class| Size| Weight| Use  
|---|---|---|---  
`th`| 14px| 500| Заголовки узлов, метки областей  
`ts`| 12px| 400| Подзаголовки, описания, метки стрелок  
`t`| 14px| 400| Основной текст  
  * **Всегда предложный регистр.** Никогда не используйте Заглавный Регистр Каждого Слова или ВСЕ ПРОПИСНЫЕ.
  * Каждый `<text>` ОБЯЗАТЕЛЬНО должен иметь класс (`t`, `ts` или `th`). Текст без класса недопустим.
  * `dominant-baseline=\"central\"` на всём тексте внутри блоков.
  * `text-anchor=\"middle\"` для центрированного текста в блоках.


**Оценка ширины (приблизительно):**
  * 14px вес 500: ~8px на символ
  * 12px вес 400: ~6.5px на символ
  * Всегда проверяйте: `box_width >= (char_count × px_per_char) + 48` (24px отступа с каждой стороны)


### Spacing & Layout[​](<#spacing--layout> "Direct link to Spacing & Layout")
  * **ViewBox** : `viewBox=\"0 0 680 H\"`, где H = высота контента + 40px буфера.
  * **Безопасная зона** : x=40 до x=640, y=40 до y=(H-40).
  * **Между блоками** : минимум 60px зазор.
  * **Внутри блоков** : 24px горизонтальный отступ, 12px вертикальный отступ.
  * **Зазор для наконечника стрелки** : 10px между наконечником и краем блока.
  * **Однострочный блок** : высота 44px.
  * **Двухстрочный блок** : высота 56px, 18px между базовыми линиями заголовка и подзаголовка.
  * **Отступ контейнера** : минимум 20px внутри каждого контейнера.
  * **Макс. вложенность** : 2-3 уровня. Глубже становится нечитаемо при ширине 680px.


### Stroke & Shape[​](<#stroke--shape> "Direct link to Stroke & Shape")
  * **Толщина обводки** : 0.5px на всех границах узлов. Не 1px, не 2px.
  * **Скругление прямоугольников** : `rx=\"8\"` для узлов, `rx=\"12\"` для внутренних контейнеров, `rx=\"16\"` до `rx=\"20\"` для внешних контейнеров.
  * **Пути соединений** : ОБЯЗАТЕЛЬНО должны иметь `fill=\"none\"`. Иначе SVG по умолчанию использует `fill: black`.


### Arrow Marker[​](<#arrow-marker> "Direct link to Arrow Marker")
Включайте этот блок `<defs>` в начало **каждого** SVG:
[code] 
    <defs>  
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"  
              markerWidth="6" markerHeight="6" orient="auto-start-reverse">  
        <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"  
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>  
      </marker>  
    </defs>  
    
[/code]
Используйте `marker-end=\"url(#arrow)\"` на линиях. Наконечник стрелки наследует цвет линии через `context-stroke`.
### CSS Classes (Provided by the Template)[​](<#css-classes-provided-by-the-template> "Direct link to CSS Classes (Provided by the Template)")
Шаблон страницы предоставляет:
  * Текст: `.t`, `.ts`, `.th`
  * Нейтральные: `.box`, `.arr`, `.leader`, `.node`
  * Цветовые градиенты: `.c-purple`, `.c-teal`, `.c-coral`, `.c-pink`, `.c-gray`, `.c-blue`, `.c-green`, `.c-amber`, `.c-red` (все с автоматическим переключением светлой/тёмной темы)


Вам **не нужно** переопределять их — просто применяйте в вашем SVG. Файл шаблона содержит полные CSS-определения.
* * *
## SVG Boilerplate[​](<#svg-boilerplate> "Direct link to SVG Boilerplate")
Каждый SVG внутри страницы шаблона начинается с этой точной структуры:
[code] 
    <svg width="100%" viewBox="0 0 680 {HEIGHT}" xmlns="http://www.w3.org/2000/svg">  
      <defs>  
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"  
                markerWidth="6" markerHeight="6" orient="auto-start-reverse">  
          <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"  
                stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>  
        </marker>  
      </defs>  
      
      <!-- Diagram content here -->  
      
    </svg>  
    
[/code]
Замените `{HEIGHT}` на реальную вычисленную высоту (нижняя граница последнего элемента + 40px).
### Node Patterns[​](<#node-patterns> "Direct link to Node Patterns")
**Однострочный узел (44px):**
[code] 
    <g class="node c-blue">  
      <rect x="100" y="20" width="180" height="44" rx="8" stroke-width="0.5"/>  
      <text class="th" x="190" y="42" text-anchor="middle" dominant-baseline="central">Service name</text>  
    </g>  
    
[/code]
**Двухстрочный узел (56px):**
[code] 
    <g class="node c-teal">  
      <rect x="100" y="20" width="200" height="56" rx="8" stroke-width="0.5"/>  
      <text class="th" x="200" y="38" text-anchor="middle" dominant-baseline="central">Service name</text>  
      <text class="ts" x="200" y="56" text-anchor="middle" dominant-baseline="central">Short description</text>  
    </g>  
    
[/code]
**Соединитель (без подписи):**
[code] 
    <line x1="200" y1="76" x2="200" y2="120" class="arr" marker-end="url(#arrow)"/>  
    
[/code]
**Контейнер (пунктирный или сплошной):**
[code] 
    <g class="c-purple">  
      <rect x="40" y="92" width="600" height="300" rx="16" stroke-width="0.5"/>  
      <text class="th" x="66" y="116">Container label</text>  
      <text class="ts" x="66" y="134">Subtitle info</text>  
    </g>  
    
[/code]
* * *
## Diagram Types[​](<#diagram-types> "Direct link to Diagram Types")
Выберите макет, соответствующий теме:
  1. **Блок-схема** — CI/CD пайплайны, жизненные циклы запросов, рабочие процессы утверждения, обработка данных. Однонаправленный поток (сверху вниз или слева направо). Макс. 4-5 узлов на строку.
  2. **Структурная / Вложенная** — Вложенность облачной инфраструктуры, системная архитектура с уровнями. Большие внешние контейнеры с внутренними областями. Пунктирные прямоугольники для логических групп.
  3. **Карта API / Эндпоинтов** — REST-маршруты, GraphQL-схемы. Дерево от корня, ветвление к группам ресурсов, каждая содержит узлы эндпоинтов.
  4. **Топология микросервисов** — Сервисная сетка, событийно-ориентированные системы. Сервисы как узлы, стрелки для паттернов коммуникации, очереди сообщений между ними.
  5. **Поток данных** — ETL пайплайны, стриминговая архитектура. Поток слева направо от источников через обработку к приёмникам.
  6. **Физическая / Структурная** — Транспортные средства, здания, оборудование, анатомия. Используйте фигуры, соответствующие физической форме — `<path>` для изогнутых корпусов, `<polygon>` для сужающихся форм, `<ellipse>`/`<circle>` для цилиндрических частей, вложенные `<rect>` для отсеков. См. `references/physical-shape-cookbook.md`.
  7. **Инфраструктура / Системная интеграция** — Умные города, IoT-сети, мультидоменные системы. Макет «звезда» с центральной платформой, соединяющей подсистемы. Семантические стили линий (`.data-line`, `.power-line`, `.water-pipe`, `.road`). См. `references/infrastructure-patterns.md`.
  8. **Макеты UI / Дашбордов** — Панели администратора, мониторинговые дашборды. Рамка экрана с вложенными элементами графиков/индикаторов. См. `references/dashboard-patterns.md`.


Для физических, инфраструктурных диаграмм и дашбордов загрузите соответствующий справочный файл перед генерацией — каждый предоставляет готовые CSS-классы и примитивы фигур.
* * *
## Validation Checklist[​](<#validation-checklist> "Direct link to Validation Checklist")
Перед финализацией любого SVG проверьте ВСЁ следующее:
  1. Каждый `<text>` имеет класс `t`, `ts` или `th`.
  2. Каждый `<text>` внутри блока имеет `dominant-baseline=\"central\"`.
  3. Каждый соединитель `<path>` или `<line>`, используемый как стрелка, имеет `fill=\"none\"`.
  4. Ни одна линия стрелки не пересекает посторонний блок.
  5. `box_width >= (длина_самой_длинной_подписи × 8) + 48` для текста 14px.
  6. `box_width >= (длина_самой_длинной_подписи × 6.5) + 48` для текста 12px.
  7. Высота ViewBox = самый нижний элемент + 40px.
  8. Весь контент остаётся в пределах x=40 до x=640.
  9. Цветовые классы (`c-*`) находятся на элементах `<g>` или фигурах, никогда на соединителях `<path>`.
  10. Блок `<defs>` со стрелкой присутствует.
  11. Нет градиентов, теней, размытия или эффектов свечения.
  12. Толщина обводки 0.5px на всех границах узлов.


* * *
## Output & Preview[​](<#output--preview> "Direct link to Output & Preview")
### Default: standalone HTML file[​](<#default-standalone-html-file> "Direct link to Default: standalone HTML file")
Запишите один `.html` файл, который пользователь сможет открыть напрямую. Без сервера, без зависимостей, работает офлайн. Шаблон:
[code] 
    # 1. Load the template  
    template = skill_view("concept-diagrams", "templates/template.html")  
      
    # 2. Fill in title, subtitle, and paste your SVG  
    html = template.replace(  
        "<!-- DIAGRAM TITLE HERE -->", "SN2 reaction mechanism"  
    ).replace(  
        "<!-- OPTIONAL SUBTITLE HERE -->", "Bimolecular nucleophilic substitution"  
    ).replace(  
        "<!-- PASTE SVG HERE -->", svg_content  
    )  
      
    # 3. Write to a user-chosen path (or ./ by default)  
    write_file("./sn2-mechanism.html", html)  
    
[/code]
Сообщите пользователю, как открыть файл:
[code] 
    # macOS  
    open ./sn2-mechanism.html  
    # Linux  
    xdg-open ./sn2-mechanism.html  
    
[/code]
### Optional: local preview server (multi-diagram gallery)[​](<#optional-local-preview-server-multi-diagram-gallery> "Direct link to Optional: local preview server (multi-diagram gallery)")
Используйте только когда пользователь явно хочет просматриваемую галерею из нескольких диаграмм.
**Правила:**
  * Привязывайтесь только к `127.0.0.1`. Никогда к `0.0.0.0`. Открытие диаграмм на всех сетевых интерфейсах — угроза безопасности в общих сетях.
  * Выберите свободный порт (НЕ задавайте жёстко) и сообщите пользователю выбранный URL.
  * Сервер опционален и включается по запросу — сначала предпочитайте отдельный HTML-файл.


Рекомендуемый шаблон (ОС выбирает свободный эфемерный порт):
[code] 
    # Put each diagram in its own folder under .diagrams/  
    mkdir -p .diagrams/sn2-mechanism  
    # ...write .diagrams/sn2-mechanism/index.html...  
      
    # Serve on loopback only, free port  
    cd .diagrams && python3 -c "  
    import http.server, socketserver  
    with socketserver.TCPServer(('127.0.0.1', 0), http.server.SimpleHTTPRequestHandler) as s:  
        print(f'Serving at http://127.0.0.1:{s.server_address[1]}/')  
        s.serve_forever()  
    " &  
    
[/code]
Если пользователь настаивает на фиксированном порте, используйте `127.0.0.1:<port>` — всё равно никогда `0.0.0.0`. Опишите, как остановить сервер (`kill %1` или `pkill -f "http.server"`).
* * *
## Examples Reference[​](<#examples-reference> "Direct link to Examples Reference")
Директория `examples/` содержит 15 полных, протестированных диаграмм. Просмотрите их для поиска рабочих шаблонов перед написанием новой диаграммы аналогичного типа:
File| Type| Demonstrates  
---|---|---|---  
`hospital-emergency-department-flow.md`| Блок-схема| Приоритетная маршрутизация с семантическими цветами  
`feature-film-production-pipeline.md`| Блок-схема| Поэтапный рабочий процесс, горизонтальные подпотоки  
`automated-password-reset-flow.md`| Блок-схема| Поток аутентификации с ветвями ошибок  
`autonomous-llm-research-agent-flow.md`| Блок-схема| Обратные стрелки, ветви решений  
`place-order-uml-sequence.md`| Последовательность| Стиль UML-диаграммы последовательности  
`commercial-aircraft-structure.md`| Физическая| Пути, полигоны, эллипсы для реалистичных форм  
`wind-turbine-structure.md`| Физическое сечение| Разделение подземной/надземной частей, цветовая кодировка  
`smartphone-layer-anatomy.md`| Разнесённый вид| Чередующиеся левые/правые подписи, многослойные компоненты  
`apartment-floor-plan-conversion.md`| План этажа| Стены, двери, предлагаемые изменения пунктирным красным  
`banana-journey-tree-to-smoothie.md`| Повествовательное путешествие| Извилистый путь, прогрессивные изменения состояния  
`cpu-ooo-microarchitecture.md`| Аппаратный конвейер| Разветвление, боковая панель иерархии памяти  
`sn2-reaction-mechanism.md`| Химия| Молекулы, изогнутые стрелки, энергетический профиль  
`smart-city-infrastructure.md`| Звезда| Семантические стили линий для каждой системы  
`electricity-grid-flow.md`| Многоэтапный поток| Иерархия напряжений, маркеры потока  
`ml-benchmark-grouped-bar-chart.md`| График| Группированные столбцы, двойная ось  
Загрузите любой пример с помощью:
[code] 
    skill_view(name="concept-diagrams", file_path="examples/<filename>")  
    
[/code]
* * *
## Quick Reference: What to Use When[​](<#quick-reference-what-to-use-when> "Direct link to Quick Reference: What to Use When")
Пользователь говорит| Тип диаграммы| Рекомендуемые цвета  
---|---|---  
«покажи пайплайн»| Блок-схема| серый начало/конец, фиолетовые шаги, красные ошибки, бирюзовый деплой  
«нарисуй поток данных»| Поток данных (слева направо)| серые источники, фиолетовая обработка, бирюзовые приёмники  
«визуализируй систему»| Структурная (вложенная)| фиолетовый контейнер, бирюзовые сервисы, коралловые данные  
«отобрази эндпоинты»| API-дерево| фиолетовый корень, один градиент на группу ресурсов  
«покажи сервисы»| Топология микросервисов| серый вход, бирюзовые сервисы, фиолетовая шина, коралловые воркеры  
«нарисуй самолёт/ТС»| Физическая| пути, полигоны, эллипсы для реалистичных форм  
«умный город / IoT»| Интеграция «звезда»| семантические стили линий для каждой подсистемы  
«покажи дашборд»| Макет UI| тёмный экран, цвета графиков: бирюзовый, фиолетовый, коралловый для алертов  
«электросеть / электричество»| Многоэтапный поток| иерархия напряжений (толщина линий ВН/СН/НН)  
«ветряк / турбина»| Физическое сечение| фундамент + разрез башни + цветокодированная гондола  
«путь X / жизненный цикл»| Повествовательное путешествие| извилистый путь, прогрессивные изменения состояния  
«слои X / разнесённый вид»| Разнесённый слой| вертикальный стек, чередующиеся подписи  
«CPU / конвейер»| Аппаратный конвейер| вертикальные стадии, разветвление к портам выполнения  
«план этажа / квартира»| План этажа| стены, двери, предлагаемые изменения пунктирным красным  
«механизм реакции»| Химия| атомы, связи, изогнутые стрелки, переходное состояние, энергетический профиль  
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Scope](<#scope>)
  * [Workflow](<#workflow>)
  * [Design System](<#design-system>)
    * [Philosophy](<#philosophy>)
    * [Color Palette](<#color-palette>)
    * [Typography](<#typography>)
    * [Spacing & Layout](<#spacing--layout>)
    * [Stroke & Shape](<#stroke--shape>)
    * [Arrow Marker](<#arrow-marker>)
    * [CSS Classes (Provided by the Template)](<#css-classes-provided-by-the-template>)
  * [SVG Boilerplate](<#svg-boilerplate>)
    * [Node Patterns](<#node-patterns>)
  * [Diagram Types](<#diagram-types>)
  * [Validation Checklist](<#validation-checklist>)
  * [Output & Preview](<#output--preview>)
    * [Default: standalone HTML file](<#default-standalone-html-file>)
    * [Optional: local preview server (multi-diagram gallery)](<#optional-local-preview-server-multi-diagram-gallery>)
  * [Examples Reference](<#examples-reference>)
  * [Quick Reference: What to Use When](<#quick-reference-what-to-use-when>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-concept-diagrams -->
