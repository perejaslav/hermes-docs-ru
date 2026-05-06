On this page
Тёмные SVG-диаграммы архитектуры/облака/инфраструктуры в формате HTML.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/architecture-diagram`  |
Version| `1.0.0`  |
Author| Cocoon AI ([hello@cocoon-ai.com](<mailto:hello@cocoon-ai.com>)), портировано Hermes Agent  |
License| MIT  |
Tags| `architecture`, `diagrams`, `SVG`, `HTML`, `visualization`, `infrastructure`, `cloud`  |
Related skills| [`concept-diagrams`](</docs/user-guide/skills/optional/creative/creative-concept-diagrams>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Architecture Diagram Skill
Создавайте профессиональные технические диаграммы архитектуры в тёмной теме как автономные HTML-файлы со встроенной SVG-графикой. Никаких внешних инструментов, API-ключей или библиотек рендеринга — просто напишите HTML-файл и откройте его в браузере.
## Scope[​](<#scope> "Direct link to Scope")
**Лучше всего подходит для:**
  * Архитектура программных систем (слои frontend / backend / database)
  * Облачная инфраструктура (VPC, регионы, подсети, управляемые сервисы)
  * Топология микросервисов / service-mesh
  * Карта базы данных + API, диаграммы развёртывания
  * Всё, что связано с тех-инфраструктурой и вписывается в тёмную эстетику с сеткой


**Для других целей используйте другие инструменты:**
  * Физика, химия, математика, биология и другие научные темы
  * Физические объекты (транспорт, железо, анатомия, сечения)
  * Планы этажей, повествовательные путешествия, образовательные / учебные визуализации
  * Скетчи от руки на доске (рассмотрите `excalidraw`)
  * Анимированные объяснения (рассмотрите навык анимации)


Если для темы доступен более специализированный навык, используйте его. Если ничего не подходит, этот навык может служить универсальным запасным вариантом для SVG-диаграмм — результат просто будет в тёмной тех-эстетике, описанной ниже.
Основано на [Cocoon AI's architecture-diagram-generator](<https://github.com/Cocoon-AI/architecture-diagram-generator>) (MIT).
## Workflow[​](<#workflow> "Direct link to Workflow")
  1. Пользователь описывает архитектуру своей системы (компоненты, соединения, технологии)
  2. Сгенерируйте HTML-файл, следуя описанной ниже дизайн-системе
  3. Сохраните с помощью `write_file` в `.html`-файл (например, `~/architecture-diagram.html`)
  4. Пользователь открывает в любом браузере — работает офлайн, без зависимостей


### Output Location[​](<#output-location> "Direct link to Output Location")
Сохраняйте диаграммы по указанному пользователем пути или по умолчанию в текущую рабочую директорию:
[code] 
    ./[project-name]-architecture.html  
    
[/code]
### Preview[​](<#preview> "Direct link to Preview")
После сохранения предложите пользователю открыть файл:
[code] 
    # macOS  
    open ./my-architecture.html  
    # Linux  
    xdg-open ./my-architecture.html  
    
[/code]
## Design System & Visual Language[​](<#design-system--visual-language> "Direct link to Design System & Visual Language")
### Color Palette (Semantic Mapping)[​](<#color-palette-semantic-mapping> "Direct link to Color Palette (Semantic Mapping)")
Используйте определённые заливки `rgba` и обводки hex для категоризации компонентов:
Тип компонента| Заливка (rgba)| Обводка (Hex)  
---|---|---  
**Frontend**| `rgba(8, 51, 68, 0.4)`| `#22d3ee` (cyan-400)  
**Backend**| `rgba(6, 78, 59, 0.4)`| `#34d399` (emerald-400)  
**Database**| `rgba(76, 29, 149, 0.4)`| `#a78bfa` (violet-400)  
**AWS/Cloud**| `rgba(120, 53, 15, 0.3)`| `#fbbf24` (amber-400)  
**Security**| `rgba(136, 19, 55, 0.4)`| `#fb7185` (rose-400)  
**Message Bus**| `rgba(251, 146, 60, 0.3)`| `#fb923c` (orange-400)  
**External**| `rgba(30, 41, 59, 0.5)`| `#94a3b8` (slate-400)  
### Typography & Background[​](<#typography--background> "Direct link to Typography & Background")
  * **Шрифт:** JetBrains Mono (Monospace), загружается из Google Fonts
  * **Размеры:** 12px (Названия), 9px (Подписи), 8px (Аннотации), 7px (Мелкие подписи)
  * **Фон:** Slate-950 (`#020617`) с едва заметным паттерном сетки 40px


[code] 
    <!-- Background Grid Pattern -->  
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">  
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>  
    </pattern>  
    
[/code]
## Technical Implementation Details[​](<#technical-implementation-details> "Direct link to Technical Implementation Details")
### Component Rendering[​](<#component-rendering> "Direct link to Component Rendering")
Компоненты — это скруглённые прямоугольники (`rx="6"`) с обводкой 1.5px. Чтобы стрелки не просвечивали сквозь полупрозрачные заливки, используйте **технику двойного прямоугольника (double-rect masking)** :
  1. Нарисуйте непрозрачный прямоугольник фона (`#0f172a`)
  2. Нарисуйте сверху полупрозрачный стилизованный прямоугольник


### Connection Rules[​](<#connection-rules> "Direct link to Connection Rules")
  * **Z-Order:** Рисуйте стрелки _раньше_ в SVG (после сетки), чтобы они отображались за блоками компонентов
  * **Наконечники стрелок:** Определяются через SVG-маркеры
  * **Потоки безопасности:** Используйте пунктирные линии розового цвета (`#fb7185`)
  * **Границы:**
    * _Группы безопасности:_ Пунктир (`4,4`), розовый цвет
    * _Регионы:_ Крупный пунктир (`8,4`), янтарный цвет, `rx="12"`


### Spacing & Layout Logic[​](<#spacing--layout-logic> "Direct link to Spacing & Layout Logic")
  * **Стандартная высота:** 60px (Сервисы); 80-120px (Крупные компоненты)
  * **Вертикальный отступ:** Минимум 40px между компонентами
  * **Шины сообщений (Message Buses):** Должны располагаться _в промежутке_ между сервисами, не перекрывая их
  * **Размещение легенды:** **КРИТИЧЕСКИ ВАЖНО.** Легенда должна располагаться за пределами всех граничных блоков. Вычислите самую низкую Y-координату всех границ и разместите легенду как минимум на 20px ниже.


## Document Structure[​](<#document-structure> "Direct link to Document Structure")
Сгенерированный HTML-файл состоит из четырёх частей:
  1. **Заголовок:** Название с пульсирующим индикатором и подзаголовком
  2. **Основной SVG:** Диаграмма, расположенная внутри карточки с скруглённой рамкой
  3. **Карточки сводки:** Сетка из трёх карточек под диаграммой для высокоуровневых деталей
  4. **Подвал:** Минимальные метаданные


### Info Card Pattern[​](<#info-card-pattern> "Direct link to Info Card Pattern")
[code] 
    <div class="card">  
      <div class="card-header">  
        <div class="card-dot cyan"></div>  
        <h3>Title</h3>  
      </div>  
      <ul>  
        <li>• Item one</li>  
        <li>• Item two</li>  
      </ul>  
    </div>  
    
[/code]
## Output Requirements[​](<#output-requirements> "Direct link to Output Requirements")
  * **Один файл:** Самостоятельный `.html`-файл
  * **Без внешних зависимостей:** Весь CSS и SVG должны быть встроенными (кроме Google Fonts)
  * **Без JavaScript:** Используйте чистый CSS для анимаций (например, пульсирующие точки)
  * **Совместимость:** Должен корректно отображаться в любом современном веб-браузере


## Template Reference[​](<#template-reference> "Direct link to Template Reference")
Загрузите полный HTML-шаблон для точной структуры, CSS и примеров SVG-компонентов:
[code] 
    skill_view(name="architecture-diagram", file_path="templates/template.html")  
    
[/code]
Шаблон содержит рабочие примеры каждого типа компонентов (frontend, backend, database, cloud, security), стили стрелок (стандартные, пунктирные, изогнутые), группы безопасности, границы регионов и легенду — используйте его как структурную основу при создании диаграмм.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Scope](<#scope>)
  * [Workflow](<#workflow>)
    * [Output Location](<#output-location>)
    * [Preview](<#preview>)
  * [Design System & Visual Language](<#design-system--visual-language>)
    * [Color Palette (Semantic Mapping)](<#color-palette-semantic-mapping>)
    * [Typography & Background](<#typography--background>)
  * [Technical Implementation Details](<#technical-implementation-details>)
    * [Component Rendering](<#component-rendering>)
    * [Connection Rules](<#connection-rules>)
    * [Spacing & Layout Logic](<#spacing--layout-logic>)
  * [Document Structure](<#document-structure>)
    * [Info Card Pattern](<#info-card-pattern>)
  * [Output Requirements](<#output-requirements>)
  * [Template Reference](<#template-reference>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-architecture-diagram -->
