On this page
Manim CE анимации: математические/алгоритмические видео в стиле 3Blue1Brown.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/manim-video`  |
Version| `1.0.0`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Manim Video Production Pipeline
## When to use[​](<#when-to-use> "Direct link to When to use")
Используйте, когда пользователи запрашивают: анимированные объяснения, математические анимации, визуализацию концепций, пошаговые алгоритмы, технические объяснения, видео в стиле 3Blue1Brown или любые программные анимации с геометрическим/математическим содержанием. Создаёт объяснительные видео в стиле 3Blue1Brown, визуализации алгоритмов, выводы уравнений, диаграммы архитектуры и истории данных с использованием Manim Community Edition.
## Creative Standard[​](<#creative-standard> "Direct link to Creative Standard")
Это образовательное кино. Каждый кадр учит. Каждая анимация раскрывает структуру.
**Прежде чем написать хотя бы строку кода** , сформулируйте нарративную дугу. Какое заблуждение это исправляет? В чём «момент озарения»? Какая визуальная история ведёт зрителя от непонимания к пониманию? Промпт пользователя — это отправная точка; интерпретируйте его с педагогической амбицией.
**Геометрия перед алгеброй.** Покажите форму сначала, уравнение потом. Визуальная память кодируется быстрее символической. Когда зритель видит геометрический паттерн перед формулой, уравнение кажется заслуженным.
**Качество первого рендера не подлежит обсуждению.** Вывод должен быть визуально чистым и эстетически целостным без итераций правки. Если что-то выглядит загромождённым, плохо синхронизированным или как «AI-сгенерированные слайды» — это неправильно.
**Наслоение прозрачности направляет внимание.** Никогда не показывайте всё на полной яркости. Основные элементы на 1.0, контекстные элементы на 0.4, структурные элементы (оси, сетки) на 0.15. Мозг обрабатывает визуальную значимость слоями.
**Пространство для дыхания.** Каждой анимации нужен `self.wait()` после неё. Зрителю нужно время, чтобы усвоить появившееся. Никогда не спешите от одной анимации к другой. Пауза в 2 секунды после ключевого раскрытия никогда не бывает лишней.
**Целостный визуальный язык.** Все сцены разделяют цветовую палитру, согласованные размеры шрифтов, одинаковую скорость анимации. Технически правильное видео, где каждая сцена использует случайные разные цвета — это эстетическая неудача.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
Запустите `scripts/setup.sh` для проверки всех зависимостей. Требуется: Python 3.10+, Manim Community Edition v0.20+ (`pip install manim`), LaTeX (`texlive-full` на Linux, `mactex` на macOS), и ffmpeg. Справочные документы протестированы с Manim CE v0.20.1.
## Modes[​](<#modes> "Direct link to Modes")
Режим| Ввод| Вывод| Референс  
---|---|---|---  
**Концептуальное объяснение**|  Тема/концепция| Анимированное объяснение с геометрической интуицией| `references/scene-planning.md`  
**Вывод уравнения**|  Математические выражения| Пошаговое анимированное доказательство| `references/equations.md`  
**Визуализация алгоритма**|  Описание алгоритма| Пошаговое выполнение со структурами данных| `references/graphs-and-data.md`  
**История данных**|  Данные/метрики| Анимированные графики, сравнения, счётчики| `references/graphs-and-data.md`  
**Диаграмма архитектуры**|  Описание системы| Компоненты, собирающиеся с соединениями| `references/mobjects.md`  
**Объяснение статьи**|  Научная статья| Ключевые результаты и методы анимированы| `references/scene-planning.md`  
**3D-визуализация**|  3D-концепция| Вращающиеся поверхности, параметрические кривые, пространственная геометрия| `references/camera-and-3d.md`  
## Stack[​](<#stack> "Direct link to Stack")
Один Python-скрипт на проект. Никакого браузера, Node.js или GPU не требуется.
Слой| Инструмент| Назначение  
---|---|---  
Ядро| Manim Community Edition| Рендеринг сцен, движок анимации  
Математика| LaTeX (texlive/MiKTeX)| Рендеринг уравнений через `MathTex`  
Видео I/O| ffmpeg| Склейка сцен, конвертация форматов, сведение аудио  
TTS| ElevenLabs / Qwen3-TTS (опционально)| Озвучка повествования  
## Pipeline[​](<#pipeline> "Direct link to Pipeline")
[code] 
    PLAN --> CODE --> RENDER --> STITCH --> AUDIO (optional) --> REVIEW  
    
[/code]
  1. **PLAN** — Напишите `plan.md` с нарративной дугой, списком сцен, визуальными элементами, цветовой палитрой, сценарием озвучки
  2. **CODE** — Напишите `script.py` с одним классом на сцену, каждый независимо рендерится
  3. **RENDER** — `manim -ql script.py Scene1 Scene2 ...` для черновика, `-qh` для продакшена
  4. **STITCH** — ffmpeg конкатенация клипов сцен в `final.mp4`
  5. **AUDIO** (опционально) — Добавьте озвучку и/или фоновую музыку через ffmpeg. См. `references/rendering.md`
  6. **REVIEW** — Рендер превью-кадров, проверка по плану, корректировка


## Project Structure[​](<#project-structure> "Direct link to Project Structure")
[code] 
    project-name/  
      plan.md                # Нарративная дуга, разбивка по сценам  
      script.py              # Все сцены в одном файле  
      concat.txt             # ffmpeg список сцен  
      final.mp4              # Сшитый вывод  
      media/                 # Авто-генерируется Manim  
        videos/script/480p15/  
    
[/code]
## Creative Direction[​](<#creative-direction> "Direct link to Creative Direction")
### Color Palettes[​](<#color-palettes> "Direct link to Color Palettes")
Палитра| Фон| Основной| Вторичный| Акцент| Применение  
---|---|---|---|---|---  
**Classic 3B1B**| `#1C1C1C`| `#58C4DD` (СИНИЙ)| `#83C167` (ЗЕЛЁНЫЙ)| `#FFFF00` (ЖЁЛТЫЙ)| Общая математика/CS  
**Warm academic**| `#2D2B55`| `#FF6B6B`| `#FFD93D`| `#6BCB77`| Дружелюбный  
**Neon tech**| `#0A0A0A`| `#00F5FF`| `#FF00FF`| `#39FF14`| Системы, архитектура  
**Monochrome**| `#1A1A2E`| `#EAEAEA`| `#888888`| `#FFFFFF`| Минимализм  
### Animation Speed[​](<#animation-speed> "Direct link to Animation Speed")
Контекст| run_time| self.wait() после  
---|---|---  
Появление заголовка/интро| 1.5s| 1.0s  
Раскрытие ключевого уравнения| 2.0s| 2.0s  
Трансформация/морфинг| 1.5s| 1.5s  
Вспомогательная подпись| 0.8s| 0.5s  
FadeOut очистка| 0.5s| 0.3s  
Раскрытие «момента озарения»| 2.5s| 3.0s  
### Typography Scale[​](<#typography-scale> "Direct link to Typography Scale")
Роль| Размер шрифта| Использование  
---|---|---  
Заголовок| 48| Заголовки сцен, вступительный текст  
Подзаголовок| 36| Заголовки секций в сцене  
Основной текст| 30| Пояснительный текст  
Подпись| 24| Аннотации, подписи осей  
Титр| 20| Субтитры, мелкий текст  
### Fonts[​](<#fonts> "Direct link to Fonts")
**Используйте моноширинные шрифты для всего текста.** Рендерер Pango в Manim производит сломанный кернинг с пропорциональными шрифтами любого размера. См. `references/visual-design.md` для полных рекомендаций.
[code] 
    MONO = "Menlo"  # определите один раз вверху файла  
      
    Text("Fourier Series", font_size=48, font=MONO, weight=BOLD)  # заголовки  
    Text("n=1: sin(x)", font_size=20, font=MONO)                  # подписи  
    MathTex(r"\nabla L")                                            # математика (использует LaTeX)  
    
[/code]
Минимальный `font_size=18` для читаемости.
### Per-Scene Variation[​](<#per-scene-variation> "Direct link to Per-Scene Variation")
Никогда не используйте одинаковую конфигурацию для всех сцен. Для каждой сцены:
  * **Другой доминирующий цвет** из палитры
  * **Другой макет** — не всегда центрируйте всё
  * **Другой тип анимации входа** — варьируйте между Write, FadeIn, GrowFromCenter, Create
  * **Разный визуальный вес** — одни сцены плотные, другие разреженные


## Workflow[​](<#workflow> "Direct link to Workflow")
### Step 1: Plan (plan.md)[​](<#step-1-plan-planmd> "Direct link to Step 1: Plan (plan.md)")
Прежде чем любой код, напишите `plan.md`. См. `references/scene-planning.md` для полного шаблона.
### Step 2: Code (script.py)[​](<#step-2-code-scriptpy> "Direct link to Step 2: Code (script.py)")
Один класс на сцену. Каждая сцена независимо рендерится.
[code] 
    from manim import *  
      
    BG = "#1C1C1C"  
    PRIMARY = "#58C4DD"  
    SECONDARY = "#83C167"  
    ACCENT = "#FFFF00"  
    MONO = "Menlo"  
      
    class Scene1_Introduction(Scene):  
        def construct(self):  
            self.camera.background_color = BG  
            title = Text("Why Does This Work?", font_size=48, color=PRIMARY, weight=BOLD, font=MONO)  
            self.add_subcaption("Why does this work?", duration=2)  
            self.play(Write(title), run_time=1.5)  
            self.wait(1.0)  
            self.play(FadeOut(title), run_time=0.5)  
    
[/code]
Ключевые паттерны:
  * **Субтитры** на каждой анимации: `self.add_subcaption("текст", duration=N)` или `subcaption="текст"` на `self.play()`
  * **Общие цветовые константы** вверху файла для согласованности между сценами
  * **`self.camera.background_color`** устанавливается в каждой сцене
  * **Чистые выходы** — FadeOut всех объектов в конце сцены: `self.play(FadeOut(Group(*self.mobjects)))`


### Step 3: Render[​](<#step-3-render> "Direct link to Step 3: Render")
[code] 
    manim -ql script.py Scene1_Introduction Scene2_CoreConcept  # draft  
    manim -qh script.py Scene1_Introduction Scene2_CoreConcept  # production  
    
[/code]
### Step 4: Stitch[​](<#step-4-stitch> "Direct link to Step 4: Stitch")
[code] 
    cat > concat.txt << 'EOF'  
    file 'media/videos/script/480p15/Scene1_Introduction.mp4'  
    file 'media/videos/script/480p15/Scene2_CoreConcept.mp4'  
    EOF  
    ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4  
    
[/code]
### Step 5: Review[​](<#step-5-review> "Direct link to Step 5: Review")
[code] 
    manim -ql --format=png -s script.py Scene2_CoreConcept  # preview still  
    
[/code]
## Critical Implementation Notes[​](<#critical-implementation-notes> "Direct link to Critical Implementation Notes")
### Raw Strings for LaTeX[​](<#raw-strings-for-latex> "Direct link to Raw Strings for LaTeX")
[code] 
    # НЕПРАВИЛЬНО: MathTex("\frac{1}{2}")  
    # ПРАВИЛЬНО:  
    MathTex(r"\frac{1}{2}")  
    
[/code]
### buff >= 0.5 for Edge Text[​](<#buff--05-for-edge-text> "Direct link to buff >= 0.5 for Edge Text")
[code] 
    label.to_edge(DOWN, buff=0.5)  # никогда не < 0.5  
    
[/code]
### FadeOut Before Replacing Text[​](<#fadeout-before-replacing-text> "Direct link to FadeOut Before Replacing Text")
[code] 
    self.play(ReplacementTransform(note1, note2))  # не Write(note2) поверх  
    
[/code]
### Never Animate Non-Added Mobjects[​](<#never-animate-non-added-mobjects> "Direct link to Never Animate Non-Added Mobjects")
[code] 
    self.play(Create(circle))  # сначала должно быть добавлено  
    self.play(circle.animate.set_color(RED))  # затем анимируйте  
    
[/code]
## Performance Targets[​](<#performance-targets> "Direct link to Performance Targets")
Качество| Разрешение| FPS| Скорость  
---|---|---|---  
`-ql` (черновик)| 854x480| 15| 5-15с/сцена  
`-qm` (среднее)| 1280x720| 30| 15-60с/сцена  
`-qh` (продакшен)| 1920x1080| 60| 30-120с/сцена  
Всегда итерируйте на `-ql`. Только рендерьте `-qh` для финального вывода.
## References[​](<#references> "Direct link to References")
Файл| Содержание  
---|---  
`references/animations.md`| Основные анимации, функции скорости, композиция, синтаксис `.animate`, паттерны тайминга  
`references/mobjects.md`| Текст, фигуры, VGroup/Group, позиционирование, стилизация, пользовательские mobjects  
`references/visual-design.md`| 12 принципов дизайна, наслоение прозрачности, шаблоны макетов, цветовые палитры  
`references/equations.md`| LaTeX в Manim, TransformMatchingTex, паттерны вывода  
`references/graphs-and-data.md`| Оси, построение графиков, BarChart, анимированные данные, визуализация алгоритмов  
`references/camera-and-3d.md`| MovingCameraScene, ThreeDScene, 3D-поверхности, управление камерой  
`references/scene-planning.md`| Нарративные дуги, шаблоны макетов, переходы между сценами, шаблон планирования  
`references/rendering.md`| Справка по CLI, пресеты качества, ffmpeg, workflow озвучки, экспорт GIF  
`references/troubleshooting.md`| Ошибки LaTeX, ошибки анимации, частые ошибки, отладка  
`references/animation-design-thinking.md`| Когда анимировать vs показывать статику, декомпозиция, темп, синхронизация повествования  
`references/updaters-and-trackers.md`| ValueTracker, add_updater, always_redraw, updater'ы на основе времени, паттерны  
`references/paper-explainer.md`| Превращение научных статей в анимации — workflow, шаблоны, предметные паттерны  
`references/decorations.md`| SurroundingRectangle, Brace, стрелки, DashedLine, Angle, жизненный цикл аннотации  
`references/production-quality.md`| Чеклисты до кода, до рендера, после рендера, пространственный макет, цвет, темп  
* * *
## Creative Divergence (use only when user requests experimental/creative/unique output)[​](<#creative-divergence-use-only-when-user-requests-experimentalcreativeunique-output> "Direct link to Creative Divergence (use only when user requests experimental/creative/unique output)")
Если пользователь просит креативный, экспериментальный или нестандартный подход к объяснению, выберите стратегию и продумайте её ДО проектирования анимации.
  * **SCAMPER** — когда пользователь хочет свежий взгляд на стандартное объяснение
  * **Assumption Reversal** — когда пользователь хочет оспорить то, как что-то обычно преподают


### SCAMPER Transformation[​](<#scamper-transformation> "Direct link to SCAMPER Transformation")
Возьмите стандартную математическую/техническую визуализацию и трансформируйте её:
  * **Substitute** : замените стандартную визуальную метафору (числовая прямая → извилистый путь, матрица → городская сетка)
  * **Combine** : объедините два подхода к объяснению (алгебраический + геометрический одновременно)
  * **Reverse** : выводите задом наперёд — начните с результата и деконструируйте до аксиом
  * **Modify** : преувеличьте параметр, чтобы показать, почему он важен (10x скорость обучения, 1000x размер выборки)
  * **Eliminate** : удалите все обозначения — объясняйте чисто через анимацию и пространственные отношения


### Assumption Reversal[​](<#assumption-reversal> "Direct link to Assumption Reversal")
  1. Перечислите, что «стандартно» для визуализации этой темы (слева направо, 2D, дискретные шаги, формальные обозначения)
  2. Выберите самое фундаментальное допущение
  3. Переверните его (вывод справа налево, 3D-вложение 2D-концепции, непрерывный морфинг вместо шагов, нулевые обозначения)
  4. Исследуйте, что переворот раскрывает, что скрывает стандартный подход


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Creative Standard](<#creative-standard>)
  * [Prerequisites](<#prerequisites>)
  * [Modes](<#modes>)
  * [Stack](<#stack>)
  * [Pipeline](<#pipeline>)
  * [Project Structure](<#project-structure>)
  * [Creative Direction](<#creative-direction>)
    * [Color Palettes](<#color-palettes>)
    * [Animation Speed](<#animation-speed>)
    * [Typography Scale](<#typography-scale>)
    * [Fonts](<#fonts>)
    * [Per-Scene Variation](<#per-scene-variation>)
  * [Workflow](<#workflow>)
    * [Step 1: Plan (plan.md)](<#step-1-plan-planmd>)
    * [Step 2: Code (script.py)](<#step-2-code-scriptpy>)
    * [Step 3: Render](<#step-3-render>)
    * [Step 4: Stitch](<#step-4-stitch>)
    * [Step 5: Review](<#step-5-review>)
  * [Critical Implementation Notes](<#critical-implementation-notes>)
    * [Raw Strings for LaTeX](<#raw-strings-for-latex>)
    * [buff >= 0.5 for Edge Text](<#buff--05-for-edge-text>)
    * [FadeOut Before Replacing Text](<#fadeout-before-replacing-text>)
    * [Never Animate Non-Added Mobjects](<#never-animate-non-added-mobjects>)
  * [Performance Targets](<#performance-targets>)
  * [References](<#references>)
  * [Creative Divergence (use only when user requests experimental/creative/unique output)](<#creative-divergence-use-only-when-user-requests-experimentalcreativeunique-output>)
    * [SCAMPER Transformation](<#scamper-transformation>)
    * [Assumption Reversal](<#assumption-reversal>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-manim-video -->
