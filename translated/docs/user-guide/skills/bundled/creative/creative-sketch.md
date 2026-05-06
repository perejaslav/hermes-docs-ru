On this page
Одноразовые HTML-макеты: 2-3 варианта дизайна для сравнения.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/sketch`  |
Version| `1.0.0`  |
Author| Hermes Agent (адаптировано из gsd-build/get-shit-done)  |
License| MIT  |
Tags| `sketch`, `mockup`, `design`, `ui`, `prototype`, `html`, `variants`, `exploration`, `wireframe`, `comparison`  |
Related skills| [`spike`](</docs/user-guide/skills/bundled/software-development/software-development-spike>), [`claude-design`](</docs/user-guide/skills/bundled/creative/creative-claude-design>), [`popular-web-designs`](</docs/user-guide/skills/bundled/creative/creative-popular-web-designs>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Sketch
Используйте этот навык, когда пользователь хочет **увидеть направление дизайна перед тем, как принять решение** — исследовать идею UI/UX в виде одноразовых HTML-макетов. Смысл в том, чтобы сгенерировать 2-3 интерактивных варианта, чтобы пользователь мог сравнить визуальные направления бок о бок, а не создавать готовый к поставке код.
Загружайте это, когда пользователь говорит что-то вроде «набросай этот экран», «покажи, как X может выглядеть», «сравни макет A и B», «дай 2-3 подхода к этому UI», «дай посмотреть варианты», «сделай макет перед тем, как строить».
## When NOT to use this[​](<#when-not-to-use-this> "Direct link to When NOT to use this")
  * Пользователь хочет production-компонент — используйте `claude-design` или создайте его правильно
  * Пользователь хочет отполированный разовый HTML-артефакт (лендинг, презентация) — `claude-design`
  * Пользователь хочет диаграмму — `excalidraw`, `architecture-diagram`
  * Дизайн уже утверждён — просто воплотите его


## If the user has the full GSD system installed[​](<#if-the-user-has-the-full-gsd-system-installed> "Direct link to If the user has the full GSD system installed")
Если `gsd-sketch` доступен как смежный навык (установлен через `npx get-shit-done-cc --hermes`), предпочтите **`gsd-sketch`** для полного workflow: постоянная `.planning/sketches/` с MANIFEST, анализ frontier mode, проверки согласованности между прошлыми набросками и интеграция с остальной частью GSD. Этот навык — лёгкая автономная версия: одноразовые наброски без механизма состояний.
## Core method[​](<#core-method> "Direct link to Core method")
[code] 
    intake  →  variants  →  head-to-head  →  pick winner (or iterate)  
    
[/code]
### 1\\. Intake (skip if the user already gave you enough)[​](<#1-intake-skip-if-the-user-already-gave-you-enough> "Direct link to 1. Intake (skip if the user already gave you enough)")
Перед генерацией вариантов получите три вещи — по одному вопросу за раз, не все сразу:
  1. **Ощущение.** «Каким это должно быть на ощупь? Прилагательные, эмоции, настроение.» — _«спокойный, редакционный, как Linear»_ говорит больше, чем _«минималистичный»_.
  2. **Референсы.** «Какие приложения, сайты или продукты передают ощущение, которое вы представляете?» — реальные референсы лучше абстрактных описаний.
  3. **Основное действие.** «Что самое важное, что пользователь делает на этом экране?» — варианты должны все хорошо это обслуживать; если нет, это просто украшение.


Кратко отразите каждый ответ перед следующим вопросом. Если пользователь уже дал все три upfront, переходите сразу к вариантам.
### 2\\. Variants (2-3, never 1, rarely 4+)[​](<#2-variants-2-3-never-1-rarely-4> "Direct link to 2. Variants (2-3, never 1, rarely 4+)")
Создайте **2-3 варианта** за один раз. Каждый вариант — это полный, самостоятельный HTML-файл. Не описывайте варианты — создавайте их. Смысл в сравнении.
Каждый вариант должен занимать **разную дизайнерскую позицию**, а не отличаться значениями пикселей. Три хороших оси для вариантов:
  * **Плотность:** компактный / воздушный / сверхплотный (выберите два контрастных полюса)
  * **Акцент:** контент-важный / действие-важное / инструмент-важный
  * **Эстетика:** редакционный / утилитарный / игривый
  * **Макет:** одноколоночный / боковая панель / разделённый экран
  * **Основа:** карточный / чистый контент / стиль документа


Выберите одну ось и расходитесь от неё. Два варианта, различающиеся только акцентным цветом — напрасная трата усилий; пользователь их не различит.
**Именование вариантов:** описывайте позицию, а не номер.
[code] 
    sketches/  
    ├── 001-calm-editorial/  
    │   ├── index.html  
    │   └── README.md  
    ├── 001-utilitarian-dense/  
    │   ├── index.html  
    │   └── README.md  
    └── 001-playful-split/  
        ├── index.html  
        └── README.md  
    
[/code]
### 3\\. Make them real HTML[​](<#3-make-them-real-html> "Direct link to 3. Make them real HTML")
Каждый вариант — это **один самостоятельный HTML-файл**:
  * Встроенный `<style>` — без шага сборки, без внешнего CSS
  * Системные шрифты или один Google Font через `<link>`
  * Tailwind через CDN (`<script src="https://cdn.tailwindcss.com"></script>`) — вполне подходит
  * Реалистичный фейковый контент — настоящие предложения, настоящие имена, не «Lorem ipsum»
  * **Интерактивный:** ссылки кликабельны, hover'ы реальны, хотя бы один переход состояния (открыть/закрыть, фильтр, переключатель). Замороженное статическое изображение — худший вариант, чем неаккуратная анимированная версия.


Откройте в браузере. Если выглядит сломанным, исправьте перед показом пользователю.
**Проверяйте варианты визуально — используйте браузерные инструменты Hermes.** Не просто пишите HTML и надейтесь, что он отрендерится; загрузите каждый вариант и посмотрите на него:
[code] 
    browser_navigate(url="file:///absolute/path/to/sketches/001-calm-editorial/index.html")  
    browser_vision(question="Выглядит ли этот макет чистым и читаемым? Есть ли видимые баги (перекрывающийся текст, нестилизованные элементы, сломанные изображения)?")  
    
[/code]
`browser_vision` возвращает AI-описание того, что на странице, плюс путь к скриншоту — ловит ошибки макета, которые не видит проверка исходного кода (например, шрифт, загрузка которого молча не удалась, flex-контейнер, который схлопнулся). Исправляйте и повторяйте навигацию, пока каждый вариант не будет выглядеть правильно.
**CSS-сброс по умолчанию + системный шрифт для быстрого старта:**
[code] 
    <style>  
      * { box-sizing: border-box; margin: 0; padding: 0; }  
      body {  
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,  
                     "Helvetica Neue", Arial, sans-serif;  
        -webkit-font-smoothing: antialiased;  
        color: #1a1a1a;  
        background: #fafafa;  
        line-height: 1.5;  
      }  
    </style>  
    
[/code]
### 4\\. Variant README[​](<#4-variant-readme> "Direct link to 4. Variant README")
`README.md` каждого варианта отвечает на вопросы:
[code] 
    ## Variant: {название позиции}  
      
    ### Design stance  
    Одно предложение о принципе, движущем этим вариантом.  
      
    ### Key choices  
    - Layout: ...  
    - Typography: ...  
    - Color: ...  
    - Interaction: ...  
      
    ### Trade-offs  
    - Strong at: ...  
    - Weak at: ...  
      
    ### Best for  
    - Тип пользователя или сценария, которому этот вариант реально служит  
    
[/code]
### 5\\. Head-to-head[​](<#5-head-to-head> "Direct link to 5. Head-to-head")
После того как все варианты созданы, представьте их как сравнение. Не просто перечисляйте — **высказывайте мнение**:
[code] 
    ## Three takes on the home screen  
      
    | Dimension | Calm editorial | Utilitarian dense | Playful split |  
    |-----------|----------------|-------------------|---------------|  
    | Density   | Low            | High              | Medium        |  
    | Primary action visibility | Low | High | Medium |  
    | Scan-ability | High | Medium | Low |  
    | Feel | Calm, trusted | Sharp, tool-like | Inviting, energetic |  
      
    **My take:** Utilitarian dense for power users, calm editorial for content-forward audiences. Playful split is weakest — tries to do both and commits to neither.  
    
[/code]
Дайте пользователю выбрать победителя, или объединить два в гибрид, или попросить ещё один раунд.
## Theming (when the project has a visual identity)[​](<#theming-when-the-project-has-a-visual-identity> "Direct link to Theming (when the project has a visual identity)")
Если у пользователя есть существующая тема (цвета, шрифты, токены), поместите общие токены в `sketches/themes/tokens.css` и импортируйте их в каждый вариант через `@import`. Держите токены минимальными:
[code] 
    /* sketches/themes/tokens.css */  
    :root {  
      --color-bg: #fafafa;  
      --color-fg: #1a1a1a;  
      --color-accent: #0066ff;  
      --color-muted: #666;  
      --radius: 8px;  
      --font-display: "Inter", sans-serif;  
      --font-body: -apple-system, BlinkMacSystemFont, sans-serif;  
    }  
    
[/code]
Не переусердствуйте с токенизацией одноразового наброска — трёх цветов и одного шрифта обычно достаточно.
## Interactivity bar[​](<#interactivity-bar> "Direct link to Interactivity bar")
Набросок достаточно интерактивен, когда пользователь может:
  1. **Кликнуть по основному действию** и увидеть видимый результат (изменение состояния, модалку, toast, имитацию навигации)
  2. **Увидеть один значимый переход состояния** (отфильтровать список, переключить режим, открыть/закрыть панель)
  3. **Навести курсор на узнаваемые аффордансы** (кнопки, строки, вкладки)


Больше этого — избыточная инженерия одноразового наброска. Меньше этого — скриншот.
## Frontier mode (picking what to sketch next)[​](<#frontier-mode-picking-what-to-sketch-next> "Direct link to Frontier mode (picking what to sketch next)")
Если наброски уже существуют и пользователь говорит «что мне набросать дальше?»:
  * **Пробелы в согласованности** — два победивших варианта из разных набросков сделали независимые выборы, которые ещё не были скомпонованы вместе
  * **Ненабросанные экраны** — упомянуты, но никогда не исследованы
  * **Покрытие состояний** — счастливый путь набросан, но не пустое / загрузка / ошибка / 1000 элементов
  * **Адаптивные пробелы** — проверено на одном вьюпорте; работает ли на мобильном / ультрашироком?
  * **Паттерны взаимодействия** — статические макеты существуют; переходы, drag, скролл — нет


Предложите 2-4 именованных кандидата. Пусть пользователь выберет.
## Output[​](<#output> "Direct link to Output")
  * Создайте `sketches/` (или `.planning/sketches/`, если пользователь использует соглашения GSD) в корне репозитория
  * Одна поддиректория на вариант: `NNN-stance-name/index.html` + `README.md`
  * Сообщите пользователю, как открыть: `open sketches/001-calm-editorial/index.html` на macOS, `xdg-open` на Linux, `start` на Windows
  * Храните варианты как одноразовые — набросок, который вы захотели сохранить, следует продвинуть в настоящий код проекта, а не хранить как актив


**Типичная последовательность инструментов для одного варианта:**
[code] 
    terminal("mkdir -p sketches/001-calm-editorial")  
    write_file("sketches/001-calm-editorial/index.html", "<!doctype html>...")  
    write_file("sketches/001-calm-editorial/README.md", "## Variant: Calm editorial\n...")  
    browser_navigate(url="file://$(pwd)/sketches/001-calm-editorial/index.html")  
    browser_vision(question="Как это выглядит? Есть ли очевидные проблемы с макетом?")  
    
[/code]
Повторите для каждого варианта, затем представьте таблицу сравнения.
## Attribution[​](<#attribution> "Direct link to Attribution")
Адаптировано из workflow `/gsd-sketch` проекта GSD (Get Shit Done) — MIT © 2025 Lex Christopherson ([gsd-build/get-shit-done](<https://github.com/gsd-build/get-shit-done>)). Полная система GSD включает постоянное состояние набросков, ссылки на паттерны тем/вариантов и workflow проверки согласованности; установите с помощью `npx get-shit-done-cc --hermes --global`.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When NOT to use this](<#when-not-to-use-this>)
  * [If the user has the full GSD system installed](<#if-the-user-has-the-full-gsd-system-installed>)
  * [Core method](<#core-method>)
    * [1\\. Intake (skip if the user already gave you enough)](<#1-intake-skip-if-the-user-already-gave-you-enough>)
    * [2\\. Variants (2-3, never 1, rarely 4+)](<#2-variants-2-3-never-1-rarely-4>)
    * [3\\. Make them real HTML](<#3-make-them-real-html>)
    * [4\\. Variant README](<#4-variant-readme>)
    * [5\\. Head-to-head](<#5-head-to-head>)
  * [Theming (when the project has a visual identity)](<#theming-when-the-project-has-a-visual-identity>)
  * [Interactivity bar](<#interactivity-bar>)
  * [Frontier mode (picking what to sketch next)](<#frontier-mode-picking-what-to-sketch-next>)
  * [Output](<#output>)
  * [Attribution](<#attribution>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-sketch -->
