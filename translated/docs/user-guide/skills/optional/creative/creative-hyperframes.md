On this page
Создавайте HTML-видеокомпозиции, анимированные титульные карточки, социальные оверлеи, видео с диктором и субтитрами, аудио-реактивную графику и шейдерные переходы с помощью HyperFrames. HTML является источником истины для видео. Используйте, когда пользователь хочет получить готовый MP4/WebM из HTML-композиции, анимировать текст/логотипы/графики поверх медиа, нуждается в субтитрах, синхронизированных с аудио, хочет озвучку TTS или конвертировать веб-сайт в видео.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

| | |
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/creative/hyperframes`  |
|Путь| `optional-skills/creative/hyperframes`  |
|Версия| `1.0.0`  |
|Автор| heygen-com  |
|Лицензия| Apache-2.0  |
|Теги| `creative`, `video`, `animation`, `html`, `gsap`, `motion-graphics`  |
|Связанные навыки| [`manim-video`](</docs/user-guide/skills/bundled/creative/creative-manim-video>), [`meme-generation`](</docs/user-guide/skills/optional/creative/creative-meme-generation>)  |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

> **info**
> Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.

# HyperFrames
HTML является источником истины для видео. Композиция — это HTML-файл с атрибутами `data-*` для тайминга, GSAP-таймлайном для анимации и CSS для оформления. Движок HyperFrames захватывает страницу покадрово и кодирует в MP4/WebM с помощью FFmpeg.

**Дополнение к `manim-video`:** Используйте `manim-video` для математических/геометрических объяснений (уравнения, стиль 3B1B). Используйте `hyperframes` для моушн-графики, диктора с субтитрами, обзоров продуктов, социальных оверлеев, шейдерных переходов и всего, что основано на реальном видео/аудио-медиа.

## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")

  * Пользователь просит создать видео из текста, сценария или веб-сайта
  * Анимированные титульные карточки, нижние трети или типографические интро
  * Озвученное видео с субтитрами (TTS + субтитры, синхронизированные с аудио)
  * Аудио-реактивная графика (синхронизация с битом, спектр-бары, пульсирующее свечение)
  * Межсценные переходы (затухание, вытеснение, шейдерная деформация, вспышка через белый)
  * Социальные оверлеи (в стиле Instagram/TikTok/YouTube)
  * Конвейер «веб-сайт в видео» (захват URL, создание промо)
  * Любая HTML/CSS/JS анимация, которая должна быть детерминированно отрендерена в видеофайл

Не **используйте** этот навык для:

  * Чисто математической анимации уравнений (→ `manim-video`)
  * Генерации изображений или мемов (→ `meme-generation`, модели изображений)
  * Прямых видеотрансляций или стриминга

## Быстрая справка[​](<#quick-reference> "Прямая ссылка на Быстрая справка")

[code] 
    npx hyperframes init my-video               # создать проект
    cd my-video
    npx hyperframes lint                        # проверка перед предпросмотром/рендером
    npx hyperframes preview                     # предпросмотр в браузере с автоперезагрузкой (порт 3002)
    npx hyperframes render --output final.mp4   # рендер в MP4
    npx hyperframes doctor                      # диагностика окружения
    
[/code]

Флаги рендера: `--quality draft|standard|high` · `--fps 24|30|60` · `--format mp4|webm` · `--docker` (воспроизводимый) · `--strict`.

Полная справка по CLI: [references/cli.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/cli.md>).

## Установка (однократная)[​](<#setup-one-time> "Прямая ссылка на Установка (однократная)")

[code] 
    bash "$(dirname "$(find ~/.hermes/skills -path '*/hyperframes/SKILL.md' 2>/dev/null | head -1)")/scripts/setup.sh"
    
[/code]

Скрипт:

  1. Проверяет, что установлены Node.js >= 22 и FFmpeg (выводит инструкции по установке, если нет).
  2. Устанавливает CLI `hyperframes` глобально (`npm install -g hyperframes@>=0.4.2`).
  3. Предварительно кеширует `chrome-headless-shell` через Puppeteer — **требуется** для рендеринга наилучшего качества через путь захвата `HeadlessExperimental.beginFrame` Chrome.
  4. Запускает `npx hyperframes doctor` и сообщает результат.

См. [references/troubleshooting.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/troubleshooting.md>), если установка не удалась.

## Процедура[​](<#procedure> "Прямая ссылка на Процедура")

### 1\\. Планирование перед написанием HTML[​](<#1-plan-before-writing-html> "Прямая ссылка на 1. Планирование перед написанием HTML")

Перед тем как писать код, сформулируйте на высоком уровне:

  * **Что** — нарративная дуга, ключевые моменты, эмоциональные акценты
  * **Структура** — композиции, дорожки (видео/аудио/оверлеи), длительности
  * **Визуальная идентичность** — цвета, шрифты, характер движений (взрывной / кинематографичный / плавный / технический)
  * **Ключевой кадр** — для каждой сцены момент, когда одновременно видно больше всего элементов. Это статический макет, который вы строите в первую очередь.

**Шлюз визуальной идентичности (ЖЁСТКИЙ ШЛЮЗ).** Прежде чем писать ЛЮБОЙ HTML композиции, должна быть определена визуальная идентичность. НЕ пишите композиции со стандартными или общими цветами (`#333`, `#3b82f6`, `Roboto` — признаки того, что этот шаг был пропущен). Проверяйте по порядку:

  1. **`DESIGN.md` в корне проекта?** → Используйте его точные цвета, шрифты, правила движения и ограничения «Что НЕЛЬЗЯ делать».
  2. **Пользователь назвал стиль** (например, «Swiss Pulse», «тёмный и технологичный», «люксовый бренд»)? → Сгенерируйте минимальный `DESIGN.md` с разделами `## Style Prompt`, `## Colors` (3–5 hex с ролями), `## Typography` (1–2 семейства), `## What NOT to Do` (3–5 антипаттернов).
  3. **Ничего из вышеперечисленного?** → Задайте 3 вопроса перед написанием любого HTML:
     * Настроение? (взрывное / кинематографичное / плавное / техническое / хаотичное / тёплое)
     * Светлый или тёмный фон?
     * Есть ли фирменные цвета, шрифты или визуальные референсы?
Затем сгенерируйте `DESIGN.md` из ответов. Каждая композиция должна ссылаться свою палитру и типографику на `DESIGN.md` или явное указание пользователя.

### 2\\. Создание проекта[​](<#2-scaffold> "Прямая ссылка на 2. Создание проекта")

[code] 
    npx hyperframes init my-video --non-interactive
    
[/code]

Шаблоны: `blank`, `warm-grain`, `play-mode`, `swiss-grid`, `vignelli`, `decision-tree`, `kinetic-type`, `product-promo`, `nyt-graph`. Укажите `--example <name>` для выбора шаблона, `--video clip.mp4` или `--audio track.mp3` для добавления медиа.

### 3\\. Макет перед анимацией[​](<#3-layout-before-animation> "Прямая ссылка на 3. Макет перед анимацией")

Сначала напишите статический HTML+CSS для **ключевого кадра** — без GSAP. Контейнер `.scene-content` должен заполнять сцену (`width:100%; height:100%; padding:Npx`) с `display:flex` \+ `gap`. Используйте padding, чтобы сдвигать содержимое внутрь — никогда не используйте `position: absolute; top: Npx` для контейнера содержимого (содержимое выйдет за края, если станет выше оставшегося пространства).

Только после того, как ключевой кадр выглядит правильно, добавляйте входы `gsap.from()` (анимируйте **к** CSS-позиции) и выходы `gsap.to()` (анимируйте **от** неё).

См. [references/composition.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/composition.md>) для полной схемы data-атрибутов и правил композиции.

### 4\\. Анимация с GSAP[​](<#4-animate-with-gsap> "Прямая ссылка на 4. Анимация с GSAP")

Каждая композиция должна:

  * Зарегистрировать свой таймлайн: `window.__timelines["<composition-id>"] = tl`
  * Запускаться с паузы: `gsap.timeline({ paused: true })` — плеер управляет воспроизведением
  * Использовать конечные значения `repeat` (без `repeat: -1` — ломает движок захвата). Рассчитывайте: `repeat: Math.ceil(duration / cycleDuration) - 1`.
  * Быть детерминированной — никаких `Math.random()`, `Date.now()` или логики настенных часов. Используйте PRNG с зерном, если нужна псевдослучайность.
  * Строиться синхронно — никаких `async`/`await`, `setTimeout` или Promise вокруг построения таймлайна.

См. [references/gsap.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/gsap.md>) для основного GSAP API (твины, easing, stagger, таймлайны).

### 5\\. Переходы между сценами[​](<#5-transitions-between-scenes> "Прямая ссылка на 5. Переходы между сценами")

Многосценные композиции требуют переходов. Правила:

  1. **Всегда используйте переход между сценами** — никаких резких склеек.
  2. **Всегда используйте анимацию входа** для каждого элемента сцены (`gsap.from(...)`).
  3. **Никогда не используйте анимацию выхода**, кроме финальной сцены — переход И ЕСТЬ выход.
  4. Финальная сцена может затухать.

Используйте `npx hyperframes add <transition-name>` для установки шейдерных переходов (`flash-through-white`, `liquid-wipe` и т.д.). Полный список: `npx hyperframes add --list`.

### 6\\. Аудио, субтитры, TTS, аудио-реактивность, выделение[​](<#6-audio-captions-tts-audio-reactive-highlighting> "Прямая ссылка на 6. Аудио, субтитры, TTS, аудио-реактивность, выделение")

  * **Аудио:** всегда отдельный элемент `<audio>` (видео — `muted playsinline`).
  * **TTS:** `npx hyperframes tts "Текст сценария" --voice af_nova --output narration.wav`. Список голосов: `--list`. Первая буква ID голоса кодирует язык (`a`/`b`=английский, `e`=испанский, `f`=французский, `j`=японский, `z`=мандаринский и т.д.) — CLI автоматически определяет локаль фонемизатора; передавайте `--lang` только для переопределения. Фонемизация на неанглийских языках требует системной установки `espeak-ng`.
  * **Субтитры:** `npx hyperframes transcribe narration.wav` → транскрипция на уровне слов. Выберите стиль на основе тона транскрипции (хайп / корпоративный / обучающий / повествовательный / социальный — см. таблицу в `references/features.md`). **Правило языка:** никогда не используйте модели whisper `.en`, если аудио не на английском — `.en` переводит неанглийское аудио вместо транскрипции. Каждая группа субтитров ДОЛЖНА иметь жёсткое завершение `tl.set(el, { opacity: 0, visibility: "hidden" }, group.end)` после своего твина выхода — иначе группы будут накладываться видимыми на последующие.
  * **Аудио-реактивная графика:** предварительно извлеките аудио-диапазоны (бас / средние / высокие) и дискретизируйте покадрово внутри таймлайна с помощью цикла `for` с `tl.call(draw, [], f / fps)` — один длинный твин НЕ реагирует на аудио. Сопоставьте бас → `scale` (пульсация), высокие → `textShadow`/`boxShadow` (свечение), общую амплитуду → `opacity`/`y`/`backgroundColor`. Избегайте клише в виде полос эквалайзера — пусть контент ведёт визуал, а аудио управляет его поведением.
  * **Выделение в стиле маркера:** эффекты выделения, обводки, всплеска, каракулей, обводки контуром для акцентирования текста — это детерминированный CSS+GSAP — см. `references/features.md#marker-highlighting`. Полностью доступны для перемотки, без анимированных SVG-фильтров.
  * **Межсценные переходы:** каждая многосценная композиция ОБЯЗАНА использовать переходы (без резких склеек). Выбирайте из примитивов CSS (сдвиг push, размытое затухание, проход через зум, шахматные блоки) или шейдерных переходов (`flash-through-white`, `liquid-wipe`, `cross-warp-morph`, `chromatic-split` и т.д.) через `npx hyperframes add`. Таблицы настроения и энергичности находятся в `references/features.md#transitions`. Не смешивайте CSS и шейдерные переходы в одной композиции.

### 7\\. Линтинг, валидация, инспекция, предпросмотр, рендер[​](<#7-lint-validate-inspect-preview-render> "Прямая ссылка на 7. Линтинг, валидация, инспекция, предпросмотр, рендер")

[code] 
    npx hyperframes lint              # выявляет отсутствующие data-composition-id, пересекающиеся дорожки, незарегистрированные таймлайны
    npx hyperframes validate          # аудит контрастности WCAG в 5 временных метках
    npx hyperframes inspect           # аудит визуального макета — переполнение, элементы за кадром, скрытый текст
    npx hyperframes preview           # предпросмотр в браузере (живой)
    npx hyperframes render --quality draft --output draft.mp4    # быстрая итерация
    npx hyperframes render --quality high --output final.mp4     # финальный результат
    
[/code]

`hyperframes validate` сэмплирует фоновые пиксели под каждым текстовым элементом и предупреждает о коэффициентах контрастности ниже 4.5:1 (или 3:1 для крупного текста). `hyperframes inspect` — сопутствующая утилита для макета: запускает страницу на нескольких временных метках и отмечает проблемы, которые не видит статический линтинг (субтитр, выходящий за безопасную зону только на отметке 4.5 с; карточка, переполняющая контейнер, когда заголовок имеет самый длинный вариант; элемент, оказывающийся позади шейдера перехода). Запускайте `inspect` особенно для композиций с речевыми пузырями, карточками, субтитрами или плотной типографикой.

### 8\\. Веб-сайт в видео (если пользователь предоставил URL)[​](<#8-website-to-video-if-the-user-gives-a-url> "Прямая ссылка на 8. Веб-сайт в видео (если пользователь предоставил URL)")

Используйте 7-шаговый рабочий процесс «захват в видео» из [references/website-to-video.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/website-to-video.md>): захват → DESIGN.md → SCRIPT.md → раскадровка → композиция → рендер → доставка.

## Типичные ошибки[​](<#pitfalls> "Прямая ссылка на Типичные ошибки")

  * **`HeadlessExperimental.beginFrame' wasn't found`** — Chromium 147+ удалил этот протокол. Убедитесь, что у вас `hyperframes@>=0.4.2` (автоматически определяет и переключается в режим скриншотов). Запасной вариант: `export PRODUCER_FORCE_SCREENSHOT=true`. См. [hyperframes#294](<https://github.com/heygen-com/hyperframes/issues/294>) и [references/troubleshooting.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/troubleshooting.md>).
  * **Системный Chrome (не `chrome-headless-shell`)** — рендер зависает на 120 с и затем тайм-аут. Запустите `npx puppeteer browsers install chrome-headless-shell` (setup.sh делает это). `hyperframes doctor` сообщает, какой бинарник будет использован.
  * **`repeat: -1` где-либо** — ломает движок захвата. Всегда вычисляйте конечное количество повторений.
  * **`gsap.set()` для элементов клипа, которые появляются позже** — элемент не существует при загрузке страницы. Используйте `tl.set(selector, vars, timePosition)` внутри таймлайна, начиная с `data-start` клипа или позже.
  * **`<br>` внутри текста контента** — принудительные разрывы строк не знают ширины отрендеренного шрифта, поэтому естественный перенос + `<br>` создают двойной разрыв. Используйте `max-width`, чтобы текст переносился естественно. Исключение: короткие заголовки, где каждое слово преднамеренно на отдельной строке.
  * **Анимация `visibility` или `display`** — GSAP не может их анимировать. Используйте `autoAlpha` (работает и с visibility, и с opacity).
  * **Вызов `video.play()` или `audio.play()`** — фреймворк управляет воспроизведением. Никогда не вызывайте их самостоятельно.
  * **Асинхронное построение таймлайнов** — движок захвата читает `window.__timelines` синхронно после загрузки страницы. Никогда не оборачивайте построение таймлайна в `async`, `setTimeout` или Promise.
  * **Самостоятельный `index.html`, обёрнутый в `<template>`** — скрывает всё содержимое от браузера. Только **подкомпозиции**, загружаемые через `data-composition-src`, используют `<template>`.
  * **Использование видео для аудио** — всегда muted `<video>` \+ отдельный `<audio>`.

## Верификация[​](<#verification> "Прямая ссылка на Верификация")

До и после рендеринга:

  1. **Линтинг + валидация + инспекция пройдены:** `npx hyperframes lint --strict && npx hyperframes validate && npx hyperframes inspect` (lint выявляет структурные проблемы, validate — контрастность, inspect — визуальные проблемы макета/переполнения — см. troubleshooting.md, если появляются предупреждения).
  2. **Хореография анимации** — для новых композиций или значительных изменений анимации запустите карту анимации. `npx hyperframes init` копирует скрипты навыка в проект, поэтому путь локальный для проекта:

[code] node skills/hyperframes/scripts/animation-map.mjs <composition-dir> \  
           --out <composition-dir>/.hyperframes/anim-map
         
[/code]

Выводит единый `animation-map.json` с описаниями каждого твина, ASCII-диаграммой Gantt, обнаружением stagger, мёртвыми зонами (>1 с без анимации), жизненными циклами элементов и флагами (`offscreen`, `collision`, `invisible`, `paced-fast` <0.2 с, `paced-slow` >2 с). Просмотрите описания и флаги — исправьте или обоснуйте каждый. Пропускайте при небольших правках.

  3. **Файл существует и не равен нулю:** `ls -lh final.mp4`.
  4. **Длительность совпадает с `data-duration`:** `ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 final.mp4`.
  5. **Визуальная проверка:** извлеките кадр из середины композиции: `ffmpeg -i final.mp4 -ss 00:00:05 -vframes 1 preview.png`.
  6. **Аудио присутствует, если ожидается:** `ffprobe -v error -show_streams -select_streams a -of default=nw=1:nk=1 final.mp4 | head -1`.

Если `hyperframes render` не удался, запустите `npx hyperframes doctor` и приложите его вывод при сообщении об ошибке.

## Ссылки[​](<#references> "Прямая ссылка на Ссылки")

  * [composition.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/composition.md>) — data-атрибуты, контракт таймлайна, необсуждаемые правила, правила типографики/ассетов
  * [cli.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/cli.md>) — все команды CLI (init, capture, lint, validate, inspect, preview, render, transcribe, tts, doctor, browser, info, upgrade, benchmark)
  * [gsap.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/gsap.md>) — основной GSAP API для HyperFrames (твины, easing, stagger, таймлайны, matchMedia)
  * [features.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/features.md>) — субтитры, TTS, аудио-реактивность, выделение маркером, переходы (загружаются по требованию)
  * [website-to-video.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/website-to-video.md>) — 7-шаговый рабочий процесс «захват в видео»
  * [troubleshooting.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/hyperframes/references/troubleshooting.md>) — исправление OpenClaw, переменные окружения, частые ошибки рендера

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Быстрая справка](<#quick-reference>)
  * [Установка (однократная)](<#setup-one-time>)
  * [Процедура](<#procedure>)
    * [1\\. Планирование перед написанием HTML](<#1-plan-before-writing-html>)
    * [2\\. Создание проекта](<#2-scaffold>)
    * [3\\. Макет перед анимацией](<#3-layout-before-animation>)
    * [4\\. Анимация с GSAP](<#4-animate-with-gsap>)
    * [5\\. Переходы между сценами](<#5-transitions-between-scenes>)
    * [6\\. Аудио, субтитры, TTS, аудио-реактивность, выделение](<#6-audio-captions-tts-audio-reactive-highlighting>)
    * [7\\. Линтинг, валидация, инспекция, предпросмотр, рендер](<#7-lint-validate-inspect-preview-render>)
    * [8\\. Веб-сайт в видео (если пользователь предоставил URL)](<#8-website-to-video-if-the-user-gives-a-url>)
  * [Типичные ошибки](<#pitfalls>)
  * [Верификация](<#verification>)
  * [Ссылки](<#references>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-hyperframes -->
