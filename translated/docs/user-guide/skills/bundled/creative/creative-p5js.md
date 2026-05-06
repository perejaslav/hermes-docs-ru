On this page
p5.js скетчи: генеративное искусство, шейдеры, интерактив, 3D.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/creative/p5js` |
|Version| `1.0.0` |
|Tags| `creative-coding`, `generative-art`, `p5js`, `canvas`, `interactive`, `visualization`, `webgl`, `shaders`, `animation` |
|Related skills| [`ascii-video`](</docs/user-guide/skills/bundled/creative/creative-ascii-video>), [`manim-video`](</docs/user-guide/skills/bundled/creative/creative-manim-video>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>) |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# p5.js Production Pipeline
## Когда использовать[​](<#when-to-use> "Direct link to When to use")
Используй, когда пользователи запрашивают: p5.js скетчи, креативное программирование, генеративное искусство, интерактивные визуализации, анимации на холсте, браузерное визуальное искусство, визуализацию данных, шейдерные эффекты или любой проект на p5.js.
## Что внутри[​](<#whats-inside> "Direct link to What's inside")
Производственный пайплайн для интерактивного и генеративного визуального искусства с использованием p5.js. Создаёт браузерные скетчи, генеративное искусство, визуализации данных, интерактивные проекты, 3D-сцены, аудио-реактивные визуалы и моушн-графику — экспорт в HTML, PNG, GIF, MP4 или SVG. Охватывает: 2D/3D рендеринг, шум и системы частиц, поля потоков, шейдеры (GLSL), попиксельную обработку, кинетическую типографику, WebGL-сцены, анализ аудио, взаимодействие с мышью/клавиатурой и headless-экспорт высокого разрешения.
## Creative Standard[​](<#creative-standard> "Direct link to Creative Standard")
Это визуальное искусство, отображаемое в браузере. Холст — это среда; алгоритм — это кисть.
**Прежде чем написать хоть одну строку кода** , сформулируй креативную концепцию. Что передаёт этот фрагмент? Что заставляет зрителя остановить скролл? Что отличает это от учебного примера кода? Запрос пользователя — это отправная точка; интерпретируй его с творческой амбицией.
**Превосходство при первом рендере обязательно.** Результат должен быть визуально впечатляющим при первой загрузке. Если это выглядит как учебное упражнение по p5.js, конфигурация по умолчанию или «AI-сгенерированный креативный код», это неправильно. Передумай, прежде чем отправлять.
**Выйди за рамки эталонного словаря.** Функции шума, системы частиц, цветовые палитры и шейдерные эффекты из документации — это начальный словарь. Для каждого проекта комбинируй, наслаивай и изобретай. Каталог — это палитра красок; ты пишешь картину.
**Будь проактивно креативным.** Если пользователь просит «систему частиц», создай систему частиц с эмерджентным стайным поведением, шлейфовыми тенями, цвето-смещённым туманом глубины и дышащим фоновым шумовым полем. Включи как минимум одну визуальную деталь, о которой пользователь не просил, но которую оценит.
**Плотный, многослойный, продуманный.** Каждый кадр должен вознаграждать просмотр. Никогда не используй плоские белые фоны. Всегда композиционная иерархия. Всегда осмысленный цвет. Всегда микродетали, которые проявляются только при близком рассмотрении.
**Целостная эстетика важнее количества функций.** Все элементы должны служить единому визуальному языку — общая цветовая температура, единая словарная толщина штриха, гармоничные скорости движения. Скетч с десятью несвязанными эффектами хуже, чем один с тремя, которые сочетаются друг с другом.
## Modes[​](<#modes> "Direct link to Modes")
Mode| Input| Output| Reference  
---|---|---|---|---  
**Generative art**| Seed / параметры| Процедурная визуальная композиция (статическая или анимированная)| `references/visual-effects.md`  
**Data visualization**| Набор данных / API| Интерактивные диаграммы, графики, пользовательские отображения данных| `references/interaction.md`  
**Interactive experience**| Нет (управляет пользователь)| Скетч с управлением мышью/клавиатурой/тач-вводом| `references/interaction.md`  
**Animation / motion graphics**| Таймлайн / раскадровка| Временные последовательности, кинетическая типографика, переходы| `references/animation.md`  
**3D scene**| Описание концепции| WebGL геометрия, освещение, камера, материалы| `references/webgl-and-3d.md`  
**Image processing**| Файл(ы) изображений| Попиксельная обработка, фильтры, мозаика, пуантилизм| `references/visual-effects.md` § Pixel Manipulation  
**Audio-reactive**| Аудиофайл / микрофон| Звукоуправляемые генеративные визуалы| `references/interaction.md` § Audio Input  
## Stack[​](<#stack> "Direct link to Stack")
Один самодостаточный HTML-файл на проект. Без шага сборки.
Layer| Tool| Purpose  
---|---|---|---  
Core| p5.js 1.11.3 (CDN)| Рендеринг холста, математика, трансформации, обработка событий  
3D| p5.js WebGL mode| 3D-геометрия, камера, освещение, GLSL-шейдеры  
Audio| p5.sound.js (CDN)| FFT-анализ, амплитуда, микрофонный вход, осцилляторы  
Export| Встроенный `saveCanvas()` / `saveGif()` / `saveFrames()`| Вывод PNG, GIF, последовательности кадров  
Capture| CCapture.js (опционально)| Детерминированный захват видео с фиксированным FPS (WebM, GIF)  
Headless| Puppeteer + Node.js (опционально)| Автоматизированный рендеринг высокого разрешения, MP4 через ffmpeg  
SVG| p5.js-svg 1.6.0 (опционально)| Векторный вывод для печати — требует p5.js 1.x  
Natural media| p5.brush (опционально)| Акварель, уголь, перо — требует p5.js 2.x + WEBGL  
Texture| p5.grain (опционально)| Зернистость плёнки, текстурные наложения  
Fonts| Google Fonts / `loadFont()`| Пользовательская типографика через OTF/TTF/WOFF2  
### Version Note[​](<#version-note> "Direct link to Version Note")
**p5.js 1.x** (1.11.3) — стандарт по умолчанию: стабильный, хорошо документированный, широкая совместимость с библиотеками. Используй эту версию, если проект не требует функций 2.x.
**p5.js 2.x** (2.2+) добавляет: `async setup()` вместо `preload()`, цветовые режимы OKLCH/OKLAB, `splineVertex()`, API `.modify()` для шейдеров, вариативные шрифты, `textToContours()`, указательные события. Требуется для p5.brush. См. `references/core-api.md` § p5.js 2.0.
## Pipeline[​](<#pipeline> "Direct link to Pipeline")
Каждый проект проходит один и тот же 6-этапный путь:
[code] 
    CONCEPT → DESIGN → CODE → PREVIEW → EXPORT → VERIFY  
    
[/code]
  1. **CONCEPT** — Сформулируй творческое видение: настроение, цветовой мир, словарь движения, что делает это уникальным
  2. **DESIGN** — Выбери режим, размер холста, модель взаимодействия, цветовую систему, формат экспорта. Сопоставь концепцию с техническими решениями
  3. **CODE** — Напиши один HTML-файл со встроенным p5.js. Структура: глобалы → `preload()` → `setup()` → `draw()` → хелперы → классы → обработчики событий
  4. **PREVIEW** — Открой в браузере, проверь визуальное качество. Протестируй на целевом разрешении. Проверь производительность
  5. **EXPORT** — Захвати вывод: `saveCanvas()` для PNG, `saveGif()` для GIF, `saveFrames()` + ffmpeg для MP4, Puppeteer для headless-пакетов
  6. **VERIFY** — Соответствует ли результат концепции? Визуально ли он впечатляет при целевом размере отображения? Поставил бы ты его в рамку?


## Creative Direction[​](<#creative-direction> "Direct link to Creative Direction")
### Aesthetic Dimensions[​](<#aesthetic-dimensions> "Direct link to Aesthetic Dimensions")
Dimension| Options| Reference  
---|---|---|---  
**Color system**| HSB/HSL, RGB, именованные палитры, процедурная гармония, градиентная интерполяция| `references/color-systems.md`  
**Noise vocabulary**| Perlin noise, simplex, fractal (octaved), domain warping, curl noise| `references/visual-effects.md` § Noise  
**Particle systems**| Физические, стайные, рисующие следы, управляемые аттракторами, следующие полю потока| `references/visual-effects.md` § Particles  
**Shape language**| Геометрические примитивы, пользовательские вершины, кривые Безье, SVG-пути| `references/shapes-and-geometry.md`  
**Motion style**| Смягчённый, пружинный, шумовой, физическая симуляция, lerp, ступенчатый| `references/animation.md`  
**Typography**| Системные шрифты, загруженные OTF, `textToPoints()` частичный текст, кинетический| `references/typography.md`  
**Shader effects**| GLSL fragment/vertex, фильтр-шейдеры, постобработка, петли обратной связи| `references/webgl-and-3d.md` § Shaders  
**Composition**| Сетка, радиальная, золотое сечение, правило третей, органический разброс, мозаика| `references/core-api.md` § Composition  
**Interaction model**| Следование за мышью, клик-спавн, перетаскивание, состояние клавиатуры, скролл, микрофонный вход| `references/interaction.md`  
**Blend modes**| `BLEND`, `ADD`, `MULTIPLY`, `SCREEN`, `DIFFERENCE`, `EXCLUSION`, `OVERLAY`| `references/color-systems.md` § Blend Modes  
**Layering**| `createGraphics()` внеэкранные буферы, альфа-композитинг, маскирование| `references/core-api.md` § Offscreen Buffers  
**Texture**| Поверхность Перлина, стипплинг, штриховка, полутон, сортировка пикселей| `references/visual-effects.md` § Texture Generation  
### Per-Project Variation Rules[​](<#per-project-variation-rules> "Direct link to Per-Project Variation Rules")
Никогда не используй конфигурации по умолчанию. Для каждого проекта:
  * **Пользовательская цветовая палитра** — никогда сырое `fill(255, 0, 0)`. Всегда продуманная палитра из 3–7 цветов
  * **Пользовательский словарь толщины штриха** — тонкие акценты (0.5), средняя структура (1–2), жирный акцент (3–5)
  * **Обработка фона** — никогда просто `background(0)` или `background(255)`. Всегда текстурированный, градиентный или многослойный
  * **Разнообразие движения** — разные скорости для разных элементов. Основные на 1x, второстепенные на 0.3x, окружающие на 0.1x
  * **Как минимум один изобретённый элемент** — пользовательское поведение частиц, новое применение шума, уникальная реакция на взаимодействие


### Project-Specific Invention[​](<#project-specific-invention> "Direct link to Project-Specific Invention")
Для каждого проекта придумай как минимум одно из:
  * Пользовательская цветовая палитра, соответствующая настроению (не предустановка)
  * Новая комбинация шумовых полей (например, curl noise + domain warp + feedback)
  * Уникальное поведение частиц (пользовательские силы, пользовательские следы, пользовательский спавн)
  * Механика взаимодействия, которую пользователь не запрашивал, но которая возвышает произведение
  * Композиционная техника, создающая визуальную иерархию


### Parameter Design Philosophy[​](<#parameter-design-philosophy> "Direct link to Parameter Design Philosophy")
Параметры должны вытекать из алгоритма, а не из универсального меню. Спроси: «Какие свойства _этой_ системы должны быть настраиваемыми?»
**Хорошие параметры** раскрывают характер алгоритма:
  * **Количества** — сколько частиц, ветвей, ячеек (управляет плотностью)
  * **Масштабы** — частота шума, размер элемента, интервалы (управляет текстурой)
  * **Скорости** — скорость, скорость роста, затухание (управляет энергией)
  * **Пороги** — когда поведение меняется? (управляет драматизмом)
  * **Соотношения** — пропорции, баланс между силами (управляет гармонией)


**Плохие параметры** — это общие элементы управления, не связанные с алгоритмом:
  * «color1», «color2», «size» — бессмысленно без контекста
  * Переключатели для несвязанных эффектов
  * Параметры, меняющие только косметику, а не поведение


Каждый параметр должен влиять на то, как алгоритм _мыслит_, а не только на то, как он _выглядит_. Параметр «турбулентность», меняющий октавы шума, — хорош. Ползунок «размер частиц», меняющий только радиус `ellipse()`, — поверхностен.
## Workflow[​](<#workflow> "Direct link to Workflow")
### Step 1: Creative Vision[​](<#step-1-creative-vision> "Direct link to Step 1: Creative Vision")
Перед любым кодом сформулируй:
  * **Настроение / атмосфера**: Что должен чувствовать зритель? Задумчивость? Энергию? Беспокойство? Игривость?
  * **Визуальная история**: Что происходит со временем (или при взаимодействии)? Построение? Угасание? Трансформация? Колебание?
  * **Цветовой мир**: Тёплый/холодный? Монохромный? Комплементарный? Какой доминирующий оттенок? Акцент?
  * **Язык форм**: Органические кривые? Острые геометрические формы? Точки? Линии? Смешанный?
  * **Словарь движения**: Медленный дрейф? Взрывной выброс? Дышащий пульс? Механическая точность?
  * **ЧТО ДЕЛАЕТ ЭТО ОСОБЕННЫМ**: Что является той единственной вещью, которая делает этот скетч уникальным?


Сопоставь запрос пользователя с эстетическими выборами. «Расслабляющий генеративный фон» требует совсем другого подхода, чем «глитч-визуализация данных».
### Step 2: Technical Design[​](<#step-2-technical-design> "Direct link to Step 2: Technical Design")
  * **Режим** — какой из 7 режимов из таблицы выше
  * **Размер холста** — альбомный 1920x1080, портретный 1080x1920, квадратный 1080x1080 или адаптивный `windowWidth/windowHeight`
  * **Рендерер** — `P2D` (по умолчанию) или `WEBGL` (для 3D, шейдеров, продвинутых режимов смешивания)
  * **Частота кадров** — 60fps (интерактив), 30fps (фоновая анимация) или `noLoop()` (статический генератив)
  * **Цель экспорта** — отображение в браузере, PNG-кадр, GIF-цикл, MP4-видео, SVG-вектор
  * **Модель взаимодействия** — пассивная (нет ввода), мышь, клавиатура, аудио-реактивная, скролл
  * **UI для зрителя** — для интерактивного генеративного искусства начинай с `templates/viewer.html`, который предоставляет навигацию по seed, ползунки параметров и скачивание. Для простых скетчей или экспорта видео используй голый HTML


### Step 3: Code the Sketch[​](<#step-3-code-the-sketch> "Direct link to Step 3: Code the Sketch")
Для **интерактивного генеративного искусства** (исследование seed, настройка параметров): начинай с `templates/viewer.html`. Прочитай шаблон сначала, сохрани фиксированные секции (навигация по seed, действия), замени алгоритм и элементы управления параметрами. Это даёт пользователю навигацию prev/next/random/jump по seed, ползунки параметров с обновлением в реальном времени и скачивание PNG — всё готовое.
Для **анимаций, экспорта видео или простых скетчей**: используй голый HTML:
Один HTML-файл. Структура:
[code] 
    <!DOCTYPE html>  
    <html lang="en">  
    <head>  
      <meta charset="UTF-8">  
      <meta name="viewport" content="width=device-width, initial-scale=1.0">  
      <title>Project Name</title>  
      <script>p5.disableFriendlyErrors = true;</script>  
      <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>  
      <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/addons/p5.sound.min.js"></script> -->  
      <!-- <script src="https://unpkg.com/p5.js-svg@1.6.0"></script> -->  <!-- SVG export -->  
      <!-- <script src="https://cdn.jsdelivr.net/npm/ccapture.js-npmfixed/build/CCapture.all.min.js"></script> -->  <!-- video capture -->  
      <style>  
        html, body { margin: 0; padding: 0; overflow: hidden; }  
        canvas { display: block; }  
      </style>  
    </head>  
    <body>  
    <script>  
    // === Configuration ===  
    const CONFIG = {  
      seed: 42,  
      // ... project-specific params  
    };  
      
    // === Color Palette ===  
    const PALETTE = {  
      bg: '#0a0a0f',  
      primary: '#e8d5b7',  
      // ...  
    };  
      
    // === Global State ===  
    let particles = [];  
      
    // === Preload (fonts, images, data) ===  
    function preload() {  
      // font = loadFont('...');  
    }  
      
    // === Setup ===  
    function setup() {  
      createCanvas(1920, 1080);  
      randomSeed(CONFIG.seed);  
      noiseSeed(CONFIG.seed);  
      colorMode(HSB, 360, 100, 100, 100);  
      // Initialize state...  
    }  
      
    // === Draw Loop ===  
    function draw() {  
      // Render frame...  
    }  
      
    // === Helper Functions ===  
    // ...  
      
    // === Classes ===  
    class Particle {  
      // ...  
    }  
      
    // === Event Handlers ===  
    function mousePressed() { /* ... */ }  
    function keyPressed() { /* ... */ }  
    function windowResized() { resizeCanvas(windowWidth, windowHeight); }  
    </script>  
    </body>  
    </html>  
    
[/code]
Ключевые паттерны реализации:
  * **Сидовая случайность**: Всегда `randomSeed()` + `noiseSeed()` для воспроизводимости
  * **Цветовой режим**: Используй `colorMode(HSB, 360, 100, 100, 100)` для интуитивного управления цветом
  * **Разделение состояния**: CONFIG для параметров, PALETTE для цветов, глобалы для изменяемого состояния
  * **Сущности на классах**: Частицы, агенты, формы как классы с методами `update()` + `display()`
  * **Внеэкранные буферы**: `createGraphics()` для многослойной композиции, следов, масок


### Step 4: Preview & Iterate[​](<#step-4-preview--iterate> "Direct link to Step 4: Preview & Iterate")
  * Открой HTML-файл напрямую в браузере — для базовых скетчей сервер не нужен
  * Для `loadImage()`/`loadFont()` из локальных файлов: используй `scripts/serve.sh` или `python3 -m http.server`
  * Chrome DevTools Performance tab для проверки 60fps
  * Тестируй на целевом разрешении экспорта, а не только на размере окна
  * Настраивай параметры, пока визуал не совпадёт с концепцией из Step 1


### Step 5: Export[​](<#step-5-export> "Direct link to Step 5: Export")
Format| Method| Command  
---|---|---|---  
**PNG**| `saveCanvas('output', 'png')` в `keyPressed()`| Нажми 's' для сохранения  
**High-res PNG**| Puppeteer headless capture| `node scripts/export-frames.js sketch.html --width 3840 --height 2160 --frames 1`  
**GIF**| `saveGif('output', 5)` — захватывает N секунд| Нажми 'g' для сохранения  
**Frame sequence**| `saveFrames('frame', 'png', 10, 30)` — 10с при 30fps| Затем `ffmpeg -i frame-%04d.png -c:v libx264 output.mp4`  
**MP4**| Puppeteer захват кадров + ffmpeg| `bash scripts/render.sh sketch.html output.mp4 --duration 30 --fps 30`  
**SVG**| `createCanvas(w, h, SVG)` с p5.js-svg| `save('output.svg')`  
### Step 6: Quality Verification[​](<#step-6-quality-verification> "Direct link to Step 6: Quality Verification")
  * **Соответствует ли это видению?** Сравни результат с креативной концепцией. Если выглядит шаблонно, вернись к Step 1
  * **Проверка разрешения**: Чёткий ли результат при целевом размере отображения? Нет ли артефактов алиасинга?
  * **Проверка производительности**: Держит ли 60fps в браузере? (минимум 30fps для анимаций)
  * **Проверка цвета**: Работают ли цвета вместе? Протестируй на светлых и тёмных мониторах
  * **Граничные случаи**: Что происходит на краях холста? При изменении размера? После 10 минут работы?


## Critical Implementation Notes[​](<#critical-implementation-notes> "Direct link to Critical Implementation Notes")
### Performance — Disable FES First[​](<#performance--disable-fes-first> "Direct link to Performance — Disable FES First")
Friendly Error System (FES) добавляет до 10x накладных расходов. Отключай в каждом продакшн-скетче:
[code] 
    p5.disableFriendlyErrors = true;  // BEFORE setup()  
      
    function setup() {  
      pixelDensity(1);  // prevent 2x-4x overdraw on retina  
      createCanvas(1920, 1080);  
    }  
    
[/code]
В горячих циклах (частицы, попиксельные операции) используй `Math.*` вместо p5-обёрток — измеримо быстрее:
[code] 
    // In draw() or update() hot paths:  
    let a = Math.sin(t);          // not sin(t)  
    let r = Math.sqrt(dx*dx+dy*dy); // not dist() — or better: skip sqrt, compare magSq  
    let v = Math.random();        // not random() — when seed not needed  
    let m = Math.min(a, b);       // not min(a, b)  
    
[/code]
Никогда не используй `console.log()` внутри `draw()`. Никогда не манипулируй DOM в `draw()`. См. `references/troubleshooting.md` § Performance.
### Seeded Randomness — Always[​](<#seeded-randomness--always> "Direct link to Seeded Randomness — Always")
Каждый генеративный скетч должен быть воспроизводимым. Одинаковый seed — одинаковый результат.
[code] 
    function setup() {  
      randomSeed(CONFIG.seed);  
      noiseSeed(CONFIG.seed);  
      // All random() and noise() calls now deterministic  
    }  
    
[/code]
Никогда не используй `Math.random()` для генеративного контента — только для критичного по производительности невизуального кода. Всегда используй `random()` для визуальных элементов. Если нужен случайный seed: `CONFIG.seed = floor(random(99999))`.
### Generative Art Platform Support (fxhash / Art Blocks)[​](<#generative-art-platform-support-fxhash--art-blocks> "Direct link to Generative Art Platform Support (fxhash / Art Blocks)")
Для платформ генеративного искусства замени PRNG p5 на детерминированную случайность платформы:
[code] 
    // fxhash convention  
    const SEED = $fx.hash;              // unique per mint  
    const rng = $fx.rand;               // deterministic PRNG  
    $fx.features({ palette: 'warm', complexity: 'high' });  
      
    // In setup():  
    randomSeed(SEED);   // for p5's noise()  
    noiseSeed(SEED);  
      
    // Replace random() with rng() for platform determinism  
    let x = rng() * width;  // instead of random(width)  
    
[/code]
См. `references/export-pipeline.md` § Platform Export.
### Color Mode — Use HSB[​](<#color-mode--use-hsb> "Direct link to Color Mode — Use HSB")
HSB (Hue, Saturation, Brightness) значительно проще в работе, чем RGB, для генеративного искусства:
[code] 
    colorMode(HSB, 360, 100, 100, 100);  
    // Now: fill(hue, sat, bri, alpha)  
    // Rotate hue: fill((baseHue + offset) % 360, 80, 90)  
    // Desaturate: fill(hue, sat * 0.3, bri)  
    // Darken: fill(hue, sat, bri * 0.5)  
    
[/code]
Никогда не хардкодь сырые RGB-значения. Определи объект палитры, выводи вариации процедурно. См. `references/color-systems.md`.
### Noise — Multi-Octave, Not Raw[​](<#noise--multi-octave-not-raw> "Direct link to Noise — Multi-Octave, Not Raw")
Сырой `noise(x, y)` выглядит как гладкие пятна. Наслаивай октавы для естественной текстуры:
[code] 
    function fbm(x, y, octaves = 4) {  
      let val = 0, amp = 1, freq = 1, sum = 0;  
      for (let i = 0; i < octaves; i++) {  
        val += noise(x * freq, y * freq) * amp;  
        sum += amp;  
        amp *= 0.5;  
        freq *= 2;  
      }  
      return val / sum;  
    }  
    
[/code]
Для текучих органических форм используй **domain warping**: подавай вывод шума обратно как координаты входа шума. См. `references/visual-effects.md`.
### createGraphics() for Layers — Not Optional[​](<#creategraphics-for-layers--not-optional> "Direct link to createGraphics() for Layers — Not Optional")
Плоский однопроходный рендеринг выглядит плоско. Используй внеэкранные буферы для композиции:
[code] 
    let bgLayer, fgLayer, trailLayer;  
    function setup() {  
      createCanvas(1920, 1080);  
      bgLayer = createGraphics(width, height);  
      fgLayer = createGraphics(width, height);  
      trailLayer = createGraphics(width, height);  
    }  
    function draw() {  
      renderBackground(bgLayer);  
      renderTrails(trailLayer);   // persistent, fading  
      renderForeground(fgLayer);  // cleared each frame  
      image(bgLayer, 0, 0);  
      image(trailLayer, 0, 0);  
      image(fgLayer, 0, 0);  
    }  
    
[/code]
### Performance — Vectorize Where Possible[​](<#performance--vectorize-where-possible> "Direct link to Performance — Vectorize Where Possible")
Вызовы p5.js draw дороги. Для тысяч частиц:
[code] 
    // SLOW: individual shapes  
    for (let p of particles) {  
      ellipse(p.x, p.y, p.size);  
    }  
      
    // FAST: single shape with beginShape()  
    beginShape(POINTS);  
    for (let p of particles) {  
      vertex(p.x, p.y);  
    }  
    endShape();  
      
    // FASTEST: pixel buffer for massive counts  
    loadPixels();  
    for (let p of particles) {  
      let idx = 4 * (floor(p.y) * width + floor(p.x));  
      pixels[idx] = r; pixels[idx+1] = g; pixels[idx+2] = b; pixels[idx+3] = 255;  
    }  
    updatePixels();  
    
[/code]
См. `references/troubleshooting.md` § Performance.
### Instance Mode for Multiple Sketches[​](<#instance-mode-for-multiple-sketches> "Direct link to Instance Mode for Multiple Sketches")
Глобальный режим засоряет `window`. Для продакшна используй instance mode:
[code] 
    const sketch = (p) => {  
      p.setup = function() {  
        p.createCanvas(800, 800);  
      };  
      p.draw = function() {  
        p.background(0);  
        p.ellipse(p.mouseX, p.mouseY, 50);  
      };  
    };  
    new p5(sketch, 'canvas-container');  
    
[/code]
Требуется при встраивании нескольких скетчей на одну страницу или интеграции с фреймворками.
### WebGL Mode Gotchas[​](<#webgl-mode-gotchas> "Direct link to WebGL Mode Gotchas")
  * `createCanvas(w, h, WEBGL)` — начало координат в центре, а не в верхнем левом углу
  * Ось Y инвертирована (положительный Y идёт вверх в WEBGL, вниз в P2D)
  * `translate(-width/2, -height/2)` для получения координат, подобных P2D
  * `push()`/`pop()` вокруг каждой трансформации — стек матриц переполняется молча
  * `texture()` перед `rect()`/`plane()` — не после
  * Пользовательские шейдеры: `createShader(vert, frag)` — тестируй на нескольких браузерах


### Export — Key Bindings Convention[​](<#export--key-bindings-convention> "Direct link to Export — Key Bindings Convention")
Каждый скетч должен включать эти хоткеи в `keyPressed()`:
[code] 
    function keyPressed() {  
      if (key === 's' || key === 'S') saveCanvas('output', 'png');  
      if (key === 'g' || key === 'G') saveGif('output', 5);  
      if (key === 'r' || key === 'R') { randomSeed(millis()); noiseSeed(millis()); }  
      if (key === ' ') CONFIG.paused = !CONFIG.paused;  
    }  
    
[/code]
### Headless Video Export — Use noLoop()[​](<#headless-video-export--use-noloop> "Direct link to Headless Video Export — Use noLoop()")
Для headless-рендеринга через Puppeteer скетч **обязан** использовать `noLoop()` в setup. Без него цикл draw p5 работает свободно, пока скриншоты медленные — скетч убегает вперёд, и вы получаете пропущенные/дублированные кадры.
[code] 
    function setup() {  
      createCanvas(1920, 1080);  
      pixelDensity(1);  
      noLoop();                    // capture script controls frame advance  
      window._p5Ready = true;      // signal readiness to capture script  
    }  
    
[/code]
Встроенный `scripts/export-frames.js` обнаруживает `_p5Ready` и вызывает `redraw()` один раз за захват для точного соответствия кадров 1:1. См. `references/export-pipeline.md` § Deterministic Capture.
Для мультисценовых видео используй архитектуру покадрового рендеринга: один HTML на сцену, рендеринг независимо, склейка через `ffmpeg -f concat`. См. `references/export-pipeline.md` § Per-Clip Architecture.
### Agent Workflow[​](<#agent-workflow> "Direct link to Agent Workflow")
При создании p5.js скетчей:
  1. **Напиши HTML-файл** — один самодостаточный файл, весь код встроен
  2. **Открой в браузере** — `open sketch.html` (macOS) или `xdg-open sketch.html` (Linux)
  3. **Локальные ассеты** (шрифты, изображения) требуют сервера: `python3 -m http.server 8080` в директории проекта, затем открой `http://localhost:8080/sketch.html`
  4. **Экспорт PNG/GIF** — добавь сокращения `keyPressed()` как показано выше, скажи пользователю, какую клавишу нажать
  5. **Headless экспорт** — `node scripts/export-frames.js sketch.html --frames 300` для автоматического захвата кадров (скетч должен использовать `noLoop()` + `_p5Ready`)
  6. **Рендеринг MP4** — `bash scripts/render.sh sketch.html output.mp4 --duration 30`
  7. **Итеративное улучшение** — редактируй HTML-файл, пользователь обновляет браузер, чтобы увидеть изменения
  8. **Загружай референсы по запросу** — используй `skill_view(name="p5js", file_path="references/...")` для загрузки конкретных справочных файлов по мере необходимости


## Performance Targets[​](<#performance-targets> "Direct link to Performance Targets")
Metric| Target  
---|---  
Frame rate (interactive)| 60fps sustained  
Frame rate (animated export)| 30fps minimum  
Particle count (P2D shapes)| 5,000-10,000 at 60fps  
Particle count (pixel buffer)| 50,000-100,000 at 60fps  
Canvas resolution| Up to 3840x2160 (export), 1920x1080 (interactive)  
File size (HTML)| < 100KB (excluding CDN libraries)  
Load time| < 2s to first frame  
## References[​](<#references> "Direct link to References")
File| Contents  
---|---  
`references/core-api.md`| Настройка холста, система координат, цикл draw, `push()`/`pop()`, внеэкранные буферы, паттерны композиции, `pixelDensity()`, адаптивный дизайн  
`references/shapes-and-geometry.md`| 2D-примитивы, `beginShape()`/`endShape()`, кривые Безье/Catmull-Rom, системы `vertex()`, пользовательские формы, `p5.Vector`, поля расстояний со знаком, конвертация SVG-путей  
`references/visual-effects.md`| Шум (Perlin, fractal, domain warp, curl), поля потоков, системы частиц (физика, стайное поведение, следы), попиксельная обработка, генерация текстур (стипплинг, штриховка, полутон), петли обратной связи, реакция-диффузия  
`references/animation.md`| Покадровая анимация, функции смягчения, `lerp()`/`map()`, пружинная физика, конечные автоматы, временные последовательности, тайминг на основе `millis()`, паттерны переходов  
`references/typography.md`| `text()`, `loadFont()`, `textToPoints()`, кинетическая типографика, текстовые маски, метрики шрифтов, адаптивный размер текста  
`references/color-systems.md`| `colorMode()`, HSB/HSL/RGB, `lerpColor()`, `paletteLerp()`, процедурные палитры, цветовая гармония, `blendMode()`, градиентный рендеринг, библиотека курированных палитр  
`references/webgl-and-3d.md`| Рендерер WEBGL, 3D-примитивы, камера, освещение, материалы, пользовательская геометрия, GLSL-шейдеры (`createShader()`, `createFilterShader()`), фреймбуферы, постобработка  
`references/interaction.md`| События мыши, состояние клавиатуры, тач-ввод, DOM-элементы, `createSlider()`/`createButton()`, аудиовход (p5.sound FFT/амплитуда), анимация на основе скролла, адаптивные события  
`references/export-pipeline.md`| `saveCanvas()`, `saveGif()`, `saveFrames()`, детерминированный headless-захват, ffmpeg кадры-в-видео, CCapture.js, SVG-экспорт, архитектура покадрового рендеринга, платформенный экспорт (fxhash), видео-проблемы  
`references/troubleshooting.md`| Профилирование производительности, попиксельные бюджеты, частые ошибки, совместимость браузеров, отладка WebGL, проблемы загрузки шрифтов, ловушки pixel density, утечки памяти, CORS  
`templates/viewer.html`| Шаблон интерактивного просмотрщика: навигация по seed (prev/next/random/jump), ползунки параметров, скачивание PNG, адаптивный холст. Начинай отсюда для исследуемого генеративного искусства  
* * *
## Creative Divergence (используй только когда пользователь запрашивает экспериментальный/креативный/уникальный вывод)[​](<#creative-divergence-use-only-when-user-requests-experimentalcreativeunique-output> "Direct link to Creative Divergence (use only when user requests experimental/creative/unique output)")
Если пользователь просит креативный, экспериментальный, удивительный или нетрадиционный вывод, выбери стратегию, которая лучше всего подходит, и продумай её шаги ПЕРЕД генерацией кода.
  * **Conceptual Blending** — когда пользователь называет две вещи для объединения или хочет гибридную эстетику
  * **SCAMPER** — когда пользователь хочет вариацию на известный паттерн генеративного искусства
  * **Distance Association** — когда пользователь даёт одну концепцию и хочет исследования («сделай что-нибудь о времени»)


### Conceptual Blending[​](<#conceptual-blending> "Direct link to Conceptual Blending")
  1. Назови две различные визуальные системы (например, физика частиц + почерк)
  2. Сопоставь соответствия (частицы = капли чернил, силы = нажим пера, поля = формы букв)
  3. Объединяй выборочно — оставляй соответствия, которые производят интересные эмерджентные визуалы
  4. Закодируй объединение как единую систему, а не две системы рядом


### SCAMPER Transformation[​](<#scamper-transformation> "Direct link to SCAMPER Transformation")
Возьми известный паттерн генеративного искусства (поле потока, система частиц, L-система, клеточный автомат) и систематически трансформируй его:
  * **Substitute (Замени)** : замени круги на текстовые символы, линии на градиенты
  * **Combine (Объедини)** : слей два паттерна (поле потока + вороной)
  * **Adapt (Адаптируй)** : примени 2D-паттерн к 3D-проекции
  * **Modify (Модифицируй)** : утрируй масштаб, искази координатное пространство
  * **Purpose (Назначь)** : используй физическую симуляцию для типографики, алгоритм сортировки для цвета
  * **Eliminate (Удали)** : убери сетку, убери цвет, убери симметрию
  * **Reverse (Инвертируй)** : запусти симуляцию задом наперёд, инвертируй пространство параметров


### Distance Association[​](<#distance-association> "Direct link to Distance Association")
  1. Закрепись на концепции пользователя (например, «одиночество»)
  2. Сгенерируй ассоциации на трёх расстояниях:
     * Близкое (очевидное): пустая комната, одинокая фигура, тишина
     * Среднее (интересное): одна рыба в косяке, плывущая не в ту сторону; телефон без уведомлений; промежуток между вагонами метро
     * Далекое (абстрактное): простые числа, асимптотические кривые, цвет 3 часов ночи
  3. Развивай ассоциации среднего расстояния — они достаточно конкретны для визуализации, но достаточно неожиданны, чтобы быть интересными


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Что внутри](<#whats-inside>)
  * [Creative Standard](<#creative-standard>)
  * [Modes](<#modes>)
  * [Stack](<#stack>)
    * [Version Note](<#version-note>)
  * [Pipeline](<#pipeline>)
  * [Creative Direction](<#creative-direction>)
    * [Aesthetic Dimensions](<#aesthetic-dimensions>)
    * [Per-Project Variation Rules](<#per-project-variation-rules>)
    * [Project-Specific Invention](<#project-specific-invention>)
    * [Parameter Design Philosophy](<#parameter-design-philosophy>)
  * [Workflow](<#workflow>)
    * [Step 1: Creative Vision](<#step-1-creative-vision>)
    * [Step 2: Technical Design](<#step-2-technical-design>)
    * [Step 3: Code the Sketch](<#step-3-code-the-sketch>)
    * [Step 4: Preview & Iterate](<#step-4-preview--iterate>)
    * [Step 5: Export](<#step-5-export>)
    * [Step 6: Quality Verification](<#step-6-quality-verification>)
  * [Critical Implementation Notes](<#critical-implementation-notes>)
    * [Performance — Disable FES First](<#performance--disable-fes-first>)
    * [Seeded Randomness — Always](<#seeded-randomness--always>)
    * [Generative Art Platform Support (fxhash / Art Blocks)](<#generative-art-platform-support-fxhash--art-blocks>)
    * [Color Mode — Use HSB](<#color-mode--use-hsb>)
    * [Noise — Multi-Octave, Not Raw](<#noise--multi-octave-not-raw>)
    * [createGraphics() for Layers — Not Optional](<#creategraphics-for-layers--not-optional>)
    * [Performance — Vectorize Where Possible](<#performance--vectorize-where-possible>)
    * [Instance Mode for Multiple Sketches](<#instance-mode-for-multiple-sketches>)
    * [WebGL Mode Gotchas](<#webgl-mode-gotchas>)
    * [Export — Key Bindings Convention](<#export--key-bindings-convention>)
    * [Headless Video Export — Use noLoop()](<#headless-video-export--use-noloop>)
    * [Agent Workflow](<#agent-workflow>)
  * [Performance Targets](<#performance-targets>)
  * [References](<#references>)
  * [Creative Divergence (используй только когда пользователь запрашивает экспериментальный/креативный/уникальный вывод)](<#creative-divergence-use-only-when-user-requests-experimentalcreativeunique-output>)
    * [Conceptual Blending](<#conceptual-blending>)
    * [SCAMPER Transformation](<#scamper-transformation>)
    * [Distance Association](<#distance-association>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-p5js -->
