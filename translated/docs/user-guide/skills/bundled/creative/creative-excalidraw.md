On this page
Рисованные от руки Excalidraw JSON-диаграммы (архитектура, потоки, последовательности).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/excalidraw`  |
Version| `1.0.0`  |
Author| Hermes Agent  |
License| MIT  |
Tags| `Excalidraw`, `Diagrams`, `Flowcharts`, `Architecture`, `Visualization`, `JSON`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Excalidraw Diagram Skill
Создавайте диаграммы, записывая стандартный JSON элементов Excalidraw и сохраняя в файлы `.excalidraw`. Эти файлы можно перетаскивать на [excalidraw.com](<https://excalidraw.com>) для просмотра и редактирования. Никаких аккаунтов, API-ключей или библиотек рендеринга — просто JSON.
## When to use[​](<#when-to-use> "Direct link to When to use")
Создавайте файлы `.excalidraw` для диаграмм архитектуры, блок-схем, диаграмм последовательностей, карт понятий и многого другого. Файлы можно открывать на excalidraw.com или загружать для получения ссылок для общего доступа.
## Workflow[​](<#workflow> "Direct link to Workflow")
  1. **Загрузите этот навык** (вы уже это сделали)
  2. **Напишите JSON элементов** — массив объектов элементов Excalidraw
  3. **Сохраните файл** с помощью `write_file`, чтобы создать файл `.excalidraw`
  4. **Опционально загрузите** для получения ссылки через `scripts/upload.py` с помощью `terminal`


### Saving a Diagram[​](<#saving-a-diagram> "Direct link to Saving a Diagram")
Оборачивайте массив элементов в стандартный конверт `.excalidraw` и сохраняйте с помощью `write_file`:
[code] 
    {  
      "type": "excalidraw",  
      "version": 2,  
      "source": "hermes-agent",  
      "elements": [ ...ваш массив элементов... ],  
      "appState": {  
        "viewBackgroundColor": "#ffffff"  
      }  
    }  
    
[/code]
Сохраняйте в любой путь, например `~/diagrams/my_diagram.excalidraw`.
### Uploading for a Shareable Link[​](<#uploading-for-a-shareable-link> "Direct link to Uploading for a Shareable Link")
Запустите скрипт загрузки (находится в директории `scripts/` этого навыка) через терминал:
[code] 
    python skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw  
    
[/code]
Это загружает на excalidraw.com (не требуется аккаунт) и выводит ссылку для общего доступа. Требуется pip-пакет `cryptography` (`pip install cryptography`).
* * *
## Element Format Reference[​](<#element-format-reference> "Direct link to Element Format Reference")
### Required Fields (all elements)[​](<#required-fields-all-elements> "Direct link to Required Fields (all elements)")
`type`, `id` (уникальная строка), `x`, `y`, `width`, `height`
### Defaults (skip these — they're applied automatically)[​](<#defaults-skip-these----theyre-applied-automatically> "Direct link to Defaults (skip these — they're applied automatically)")
  * `strokeColor`: `"#1e1e1e"`
  * `backgroundColor`: `"transparent"`
  * `fillStyle`: `"solid"`
  * `strokeWidth`: `2`
  * `roughness`: `1` (рисованный от руки вид)
  * `opacity`: `100`


Фон холста — белый.
### Element Types[​](<#element-types> "Direct link to Element Types")
**Rectangle** :
[code] 
    { "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }  
    
[/code]
  * `roundness: { "type": 3 }` для скруглённых углов
  * `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` для заливки


**Ellipse** :
[code] 
    { "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }  
    
[/code]
**Diamond** :
[code] 
    { "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }  
    
[/code]
**Labeled shape (container binding)** — создайте текстовый элемент, привязанный к фигуре:
> **ПРЕДУПРЕЖДЕНИЕ:** НЕ используйте `"label": { "text": "..." }` на фигурах. Это НЕ валидное свойство Excalidraw и будет молча проигнорировано, в результате чего фигуры будут пустыми. Вы ОБЯЗАНЫ использовать подход с привязкой контейнера, описанный ниже.
Фигуре нужен `boundElements`, перечисляющий текст, а тексту нужен `containerId`, указывающий обратно:
[code] 
    { "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,  
      "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",  
      "boundElements": [{ "id": "t_r1", "type": "text" }] },  
    { "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,  
      "text": "Привет", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",  
      "textAlign": "center", "verticalAlign": "middle",  
      "containerId": "r1", "originalText": "Привет", "autoResize": true }  
    
[/code]
  * Работает на rectangle, ellipse, diamond
  * Текст автоматически центрируется Excalidraw при установленном `containerId`
  * `x`/`y`/`width`/`height` текста приблизительны — Excalidraw пересчитывает их при загрузке
  * `originalText` должен совпадать с `text`
  * Всегда включайте `fontFamily: 1` (Virgil/рисованный шрифт)


**Labeled arrow** — тот же подход с привязкой контейнера:
[code] 
    { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,  
      "points": [[0,0],[200,0]], "endArrowhead": "arrow",  
      "boundElements": [{ "id": "t_a1", "type": "text" }] },  
    { "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,  
      "text": "соединяет", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",  
      "textAlign": "center", "verticalAlign": "middle",  
      "containerId": "a1", "originalText": "соединяет", "autoResize": true }  
    
[/code]
**Standalone text** (только заголовки и аннотации — без контейнера):
[code] 
    { "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Привет", "fontSize": 20,  
      "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Привет", "autoResize": true }  
    
[/code]
  * `x` — это ЛЕВЫЙ край. Чтобы отцентрировать в позиции `cx`: `x = cx - (text.length * fontSize * 0.5) / 2`
  * НЕ полагайтесь на `textAlign` или `width` для позиционирования


**Arrow** :
[code] 
    { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,  
      "points": [[0,0],[200,0]], "endArrowhead": "arrow" }  
    
[/code]
  * `points`: смещения `[dx, dy]` от `x`, `y` элемента
  * `endArrowhead`: `null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
  * `strokeStyle`: `"solid"` (по умолч.) | `"dashed"` | `"dotted"`


### Arrow Bindings (connect arrows to shapes)[​](<#arrow-bindings-connect-arrows-to-shapes> "Direct link to Arrow Bindings (connect arrows to shapes)")
[code] 
    {  
      "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,  
      "points": [[0,0],[150,0]], "endArrowhead": "arrow",  
      "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },  
      "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }  
    }  
    
[/code]
Координаты `fixedPoint`: `top=[0.5,0]`, `bottom=[0.5,1]`, `left=[0,0.5]`, `right=[1,0.5]`
### Drawing Order (z-order)[​](<#drawing-order-z-order> "Direct link to Drawing Order (z-order)")
  * Порядок массива = z-порядок (первый = задний, последний = передний)
  * Выводите последовательно: фоновые зоны → фигура → её привязанный текст → её стрелки → следующая фигура
  * ПЛОХО: все прямоугольники, потом все тексты, потом все стрелки
  * ХОРОШО: bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
  * Всегда размещайте привязанный текстовый элемент сразу после его контейнерной фигуры


### Sizing Guidelines[​](<#sizing-guidelines> "Direct link to Sizing Guidelines")
**Размеры шрифтов:**
  * Минимальный `fontSize`: **16** для основного текста, подписей, описаний
  * Минимальный `fontSize`: **20** для заголовков
  * Минимальный `fontSize`: **14** только для второстепенных аннотаций (экономно)
  * НИКОГДА не используйте `fontSize` меньше 14


**Размеры элементов:**
  * Минимальный размер фигуры: 120x60 для подписанных прямоугольников/эллипсов
  * Оставляйте минимум 20-30px зазоров между элементами
  * Предпочитайте меньшее количество более крупных элементов множеству крошечных


### Color Palette[​](<#color-palette> "Direct link to Color Palette")
См. `references/colors.md` для полных таблиц цветов. Краткая справка:
Использование| Цвет заливки| Hex  
---|---|---  
Основной / Ввод| Светло-голубой| `#a5d8ff`  
Успех / Вывод| Светло-зелёный| `#b2f2bb`  
Предупреждение / Внешний| Светло-оранжевый| `#ffd8a8`  
Обработка / Специальный| Светло-фиолетовый| `#d0bfff`  
Ошибка / Критический| Светло-красный| `#ffc9c9`  
Заметки / Решения| Светло-жёлтый| `#fff3bf`  
Хранилище / Данные| Светло-бирюзовый| `#c3fae8`  
### Tips[​](<#tips> "Direct link to Tips")
  * Используйте цветовую палитру единообразно по всей диаграмме
  * **Контраст текста КРИТИЧЕСКИ ВАЖЕН** — никогда не используйте светло-серый на белом фоне. Минимальный цвет текста на белом: `#757575`
  * НЕ используйте эмодзи в тексте — они не отображаются в шрифте Excalidraw
  * Для диаграмм в тёмной теме см. `references/dark-mode.md`
  * Для более крупных примеров см. `references/examples.md`


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Workflow](<#workflow>)
    * [Saving a Diagram](<#saving-a-diagram>)
    * [Uploading for a Shareable Link](<#uploading-for-a-shareable-link>)
  * [Element Format Reference](<#element-format-reference>)
    * [Required Fields (all elements)](<#required-fields-all-elements>)
    * [Defaults (skip these -- they're applied automatically)](<#defaults-skip-these----theyre-applied-automatically>)
    * [Element Types](<#element-types>)
    * [Arrow Bindings (connect arrows to shapes)](<#arrow-bindings-connect-arrows-to-shapes>)
    * [Drawing Order (z-order)](<#drawing-order-z-order>)
    * [Sizing Guidelines](<#sizing-guidelines>)
    * [Color Palette](<#color-palette>)
    * [Tips](<#tips>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-excalidraw -->
