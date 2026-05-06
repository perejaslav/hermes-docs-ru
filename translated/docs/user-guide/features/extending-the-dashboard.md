On this page
Веб-панель Hermes (`hermes dashboard`) спроектирована так, чтобы её можно было переоформлять и расширять без форка кодовой базы. Доступны три уровня:
  1. **Темы** — YAML-файлы, которые перекрашивают палитру, типографику, макет и хром отдельных компонентов панели. Положите файл в `~/.hermes/dashboard-themes/` — он появится в переключателе тем.
  2. **UI-плагины** — директория с `manifest.json` и JavaScript-бандлом, который регистрирует вкладку, заменяет встроенную страницу, дополняет её через слоты уровня страницы или внедряет компоненты в именованные слоты оболочки.
  3. **Бэкенд-плагины** — Python-файл внутри директории плагина, который предоставляет FastAPI `router`; маршруты монтируются по пути `/api/plugins/<name>/` и вызываются из UI плагина.

Все три уровня **подключаются во время выполнения без пересборки** : не нужно клонировать репозиторий, запускать `npm run build` или править исходники панели. Эта страница является каноническим справочником по всем трём.
Если вы просто хотите использовать панель, см. [Web Dashboard](</docs/user-guide/features/web-dashboard>). Если хотите переоформить терминальный CLI (а не веб-панель), см. [Skins & Themes](</docs/user-guide/features/skins>) — система скинов CLI не связана с темами панели.
Как сочетаются части
Темы и плагины независимы, но синергичны. Тема может существовать сама по себе (просто YAML-файл). Плагин может существовать сам по себе (просто вкладка). Вместе они позволяют создать полное визуальное переоформление с пользовательскими HUD — встроенная демонстрация `strike-freedom-cockpit` делает именно это. См. [Совместная демка темы и плагина](<#combined-theme--plugin-demo>).
* * *
## Содержание[​](<#table-of-contents> "Direct link to Содержание")
  * [Темы](<#themes>)
    * [Быстрый старт — ваша первая тема](<#quick-start--your-first-theme>)
    * [Палитра, типографика, макет](<#palette-typography-layout>)
    * [Варианты макета](<#layout-variants>)
    * [Ресурсы темы (изображения как CSS-переменные)](<#theme-assets-images-as-css-vars>)
    * [Переопределения хрома компонентов](<#component-chrome-overrides>)
    * [Переопределения цветов](<#color-overrides>)
    * [Сырой `customCSS`](<#raw-customcss>)
    * [Встроенные темы](<#built-in-themes>)
    * [Полный справочник темы YAML](<#full-theme-yaml-reference>)
  * [Плагины](<#plugins>)
    * [Быстрый старт — ваш первый плагин](<#quick-start--your-first-plugin>)
    * [Структура директории](<#directory-layout>)
    * [Справочник манифеста](<#manifest-reference>)
    * [Plugin SDK](<#the-plugin-sdk>)
    * [Слоты оболочки](<#shell-slots>)
    * [Замена встроенных страниц (`tab.override`)](<#replacing-built-in-pages-taboverride>)
    * [Дополнение встроенных страниц (слоты уровня страницы)](<#augmenting-built-in-pages-page-scoped-slots>)
    * [Плагины только со слотами (`tab.hidden`)](<#slot-only-plugins-tabhidden>)
    * [Маршруты бэкенд-API](<#backend-api-routes>)
    * [Свой CSS для каждого плагина](<#custom-css-per-plugin>)
    * [Обнаружение и перезагрузка плагинов](<#plugin-discovery--reload>)
  * [Совместная демка темы и плагина](<#combined-theme--plugin-demo>)
  * [Справочник API](<#api-reference>)
  * [Устранение неполадок](<#troubleshooting>)


* * *
## Темы[​](<#themes> "Direct link to Темы")
Темы — это YAML-файлы, хранящиеся в `~/.hermes/dashboard-themes/`. Имя файла не имеет значения (система использует поле `name:` темы), но по соглашению используется `<name>.yaml`. Каждое поле опционально — отсутствующие ключи возвращаются ко встроенной теме `default`, поэтому тема может быть размером с один цвет.
### Быстрый старт — ваша первая тема[​](<#quick-start--your-first-theme> "Direct link to Быстрый старт — ваша первая тема")
[code] 
    mkdir -p ~/.hermes/dashboard-themes  
    
[/code]
[code] 
    # ~/.hermes/dashboard-themes/neon.yaml  
    name: neon  
    label: Neon  
    description: Pure magenta on black  
      
    palette:  
      background: "#000000"  
      midground: "#ff00ff"  
    
[/code]
Обновите панель. Нажмите на иконку палитры в заголовке и выберите **Neon**. Фон станет чёрным, текст и акценты — малиновыми, а все производные цвета (карточка, граница, приглушённый, кольцо и т.д.) будут пересчитаны из этого триплета из двух цветов через `color-mix()` в CSS.
Вот и всё знакомство: один файл, два цвета. Всё остальное ниже — необязательное усовершенствование.
### Палитра, типографика, макет[​](<#palette-typography-layout> "Direct link to Палитра, типографика, макет")
Эти три блока — сердце темы. Каждый независим — переопределяйте один, оставляйте другие.
#### Палитра (3 уровня)[​](<#palette-3-layer> "Direct link to Палитра \\(3 уровня\\)")
Палитра — это триплет цветовых слоёв, плюс цвет виньетки тёплого свечения и множитель зернистости. Каскад дизайн-системы панели выводит все shadcn-совместимые токены (card, popover, muted, border, primary, destructive, ring и т.д.) из этого триплета через CSS `color-mix()`. Переопределение трёх цветов каскадно распространяется на весь интерфейс.
Ключ| Описание  
---|---  
`palette.background`| Самый глубокий цвет холста — обычно близкий к чёрному. Определяет фон страницы и заливку карточек.  
`palette.midground`| Основной текст и акцент. Большинство хрома UI использует его (цвет текста на переднем плане, обводка кнопок, фокусные кольца).  
`palette.foreground`| Верхний слой подсветки. Тема по умолчанию устанавливает его на белый с альфой 0 (невидимый); темы, желающие получить яркий акцент сверху, могут увеличить его альфу.  
`palette.warmGlow`| Строка `rgba(...)`, используемая в качестве цвета виньетки компонентом `<Backdrop />`.  
`palette.noiseOpacity`| Множитель 0–1.2 для наложения зернистости. Меньше = мягче, больше = грубее.  
Каждый слой принимает либо `{hex: "#RRGGBB", alpha: 0.0–1.0}`, либо строку шестнадцатеричного цвета (альфа по умолчанию 1.0).
[code] 
    palette:  
      background:  
        hex: "#05091a"  
        alpha: 1.0  
      midground: "#d8f0ff"          # короткая запись hex, alpha = 1.0  
      foreground:  
        hex: "#ffffff"  
        alpha: 0                    # невидимый верхний слой  
      warmGlow: "rgba(255, 199, 55, 0.24)"  
      noiseOpacity: 0.7  
    
[/code]
#### Типографика[​](<#typography> "Direct link to Типографика")
Ключ| Тип| Описание  
---|---|---  
`fontSans`| строка| CSS-стек font-family для основного текста (применяется к `html`, `body`).  
`fontMono`| строка| CSS-стек font-family для блоков кода, `<code>`, утилит `.font-mono`.  
`fontDisplay`| строка| Опциональный стек для заголовков/дисплея. Возвращается к `fontSans`.  
`fontUrl`| строка| Опциональный URL внешней таблицы стилей. Вставляется как `<link rel="stylesheet">` в `<head>` при переключении темы. Один и тот же URL не вставляется дважды. Работает с Google Fonts, Bunny Fonts, самодельными `@font-face` — всем, на что можно дать ссылку.  
`baseSize`| строка| Корневой размер шрифта — управляет rem-шкалой. Например `"14px"`, `"16px"`.  
`lineHeight`| строка| Межстрочный интервал по умолчанию. Например `"1.5"`, `"1.65"`.  
`letterSpacing`| строка| Межбуквенный интервал по умолчанию. Например `"0"`, `"0.01em"`, `"-0.01em"`.
[code] 
    typography:  
      fontSans: '"Orbitron", "Eurostile", "Impact", sans-serif'  
      fontMono: '"Share Tech Mono", ui-monospace, monospace'  
      fontDisplay: '"Orbitron", "Eurostile", sans-serif'  
      fontUrl: "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Share+Tech+Mono&display=swap"  
      baseSize: "14px"  
      lineHeight: "1.5"  
      letterSpacing: "0.04em"  
    
[/code]  
#### Макет[​](<#layout> "Direct link to Макет")
Ключ| Значения| Описание  
---|---|---  
`radius`| любая CSS-длина (`"0"`, `"0.25rem"`, `"0.5rem"`, `"1rem"`, ...)| Токен радиуса скругления. Отображается на `--radius` и каскадно распространяется на `--radius-sm/md/lg/xl` — все скруглённые элементы меняются вместе.  
`density`| `compact` | `comfortable` | `spacious`| Множитель интервалов, применяемый как CSS-переменная `--spacing-mul`. `compact = 0.85×`, `comfortable = 1.0×` (по умолчанию), `spacious = 1.2×`. Масштабирует базовые интервалы Tailwind, так что утилиты padding, gap и space-between меняются пропорционально.
[code] 
    layout:  
      radius: "0"  
      density: compact  
    
[/code]  
### Варианты макета[​](<#layout-variants> "Direct link to Варианты макета")
`layoutVariant` выбирает общий макет оболочки. По умолчанию `"standard"`, если отсутствует.
Вариант| Поведение  
---|---  
`standard`| Одна колонка, максимальная ширина 1600px (по умолчанию).  
`cockpit`| Левая боковая панель (260px) + основной контент. Заполняется плагинами через слот `sidebar` — см. [Слоты оболочки](<#shell-slots>). Без плагина панель показывает заглушку.  
`tiled`| Убирает ограничение максимальной ширины, чтобы страницы могли использовать всю ширину окна просмотра.
[code] 
    layoutVariant: cockpit  
    
[/code]  
Текущий вариант доступен как `document.documentElement.dataset.layoutVariant`, поэтому сырой CSS в `customCSS` может обращаться к нему через `:root[data-layout-variant=\"cockpit\"] ...`.
### Ресурсы темы (изображения как CSS-переменные)[​](<#theme-assets-images-as-css-vars> "Direct link to Ресурсы темы \\(изображения как CSS-переменные\\)")
Добавляйте URL изображений в тему. Каждый именованный слот становится CSS-переменной (`--theme-asset-<name>`), которую могут читать встроенная оболочка и любой плагин. Слот `bg` автоматически подключается к фону; остальные слоты предназначены для плагинов.
[code] 
    assets:  
      bg: "https://example.com/hero-bg.jpg"           # автоматически подключается к <Backdrop />  
      hero: "/my-images/strike-freedom.png"           # для боковых панелей плагинов  
      crest: "/my-images/crest.svg"                   # для плагинов в левой части заголовка  
      logo: "/my-images/logo.png"  
      sidebar: "/my-images/rail.png"  
      header: "/my-images/header-art.png"  
      custom:  
        scanLines: "/my-images/scanlines.png"         # → --theme-asset-custom-scanLines  
    
[/code]
Значения принимают:
  * Обычные URL — автоматически оборачиваются в `url(...)`.
  * Предварительно обёрнутые `url(...)`, `linear-gradient(...)`, `radial-gradient(...)` — используются как есть.
  * `"none"` — явный отказ.


Каждый ресурс также выдаётся как `--theme-asset-<name>-raw` (нераспакованный URL) на случай, если плагину нужно передать его в `<img src>` вместо `background-image`.
Плагины читают их через обычный CSS или JS:
[code] 
    // В слоте плагина  
    const hero = getComputedStyle(document.documentElement)  
      .getPropertyValue("--theme-asset-hero").trim();  
    
[/code]
### Переопределения хрома компонентов[​](<#component-chrome-overrides> "Direct link to Переопределения хрома компонентов")
`componentStyles` переопределяет стили отдельных компонентов оболочки без написания CSS-селекторов. Записи каждой группы становятся CSS-переменными (`--component-<bucket>-<kebab-property>`), которые читают общие компоненты оболочки. Таким образом, переопределения `card:` применяются к каждому `<Card>`, `header:` — к панели приложения и т.д.
[code] 
    componentStyles:  
      card:  
        clipPath: "polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px)"  
        background: "linear-gradient(180deg, rgba(10, 22, 52, 0.85), rgba(5, 9, 26, 0.92))"  
        boxShadow: "inset 0 0 0 1px rgba(64, 200, 255, 0.28)"  
      header:  
        background: "linear-gradient(180deg, rgba(16, 32, 72, 0.95), rgba(5, 9, 26, 0.9))"  
      tab:  
        clipPath: "polygon(6px 0, 100% 0, calc(100% - 6px) 100%, 0 100%)"  
      sidebar: {}  
      backdrop: {}  
      footer: {}  
      progress: {}  
      badge: {}  
      page: {}  
    
[/code]
Поддерживаемые группы: `card`, `header`, `footer`, `sidebar`, `tab`, `progress`, `badge`, `backdrop`, `page`.
Имена свойств используют camelCase (`clipPath`) и выдаются в kebab-нотации (`clip-path`). Значения — обычные CSS-строки; CSS принимает всё, что угодно (`clip-path`, `border-image`, `background`, `box-shadow`, `animation`, ...).
### Переопределения цветов[​](<#color-overrides> "Direct link to Переопределения цветов")
Большинству тем это не понадобится — 3-уровневая палитра выводит все shadcn-токены. Используйте `colorOverrides`, когда нужен специфический акцент, который не даёт деривация (более мягкий красный для разрушительного действия в пастельной теме, специфический зелёный для успеха в брендовой теме).
[code] 
    colorOverrides:  
      primary: "#ffce3a"  
      primaryForeground: "#05091a"  
      accent: "#3fd3ff"  
      ring: "#3fd3ff"  
      destructive: "#ff3a5e"  
      border: "rgba(64, 200, 255, 0.28)"  
    
[/code]
Поддерживаемые ключи: `card`, `cardForeground`, `popover`, `popoverForeground`, `primary`, `primaryForeground`, `secondary`, `secondaryForeground`, `muted`, `mutedForeground`, `accent`, `accentForeground`, `destructive`, `destructiveForeground`, `success`, `warning`, `border`, `input`, `ring`.
Каждый ключ соответствует 1:1 CSS-переменной `--color-<kebab>` (например, `primaryForeground` → `--color-primary-foreground`). Любой ключ, установленный здесь, имеет приоритет над каскадом палитры только для активной темы — переключение на другую тему очищает переопределения.
### Сырой `customCSS`[​](<#raw-customcss> "Direct link to raw-customcss")
Для хрома на уровне селекторов, который невозможно выразить через `componentStyles` — псевдоэлементы, анимации, медиа-запросы, переопределения в рамках темы — добавьте сырой CSS в `customCSS`:
[code] 
    customCSS: |  
      /* Наложение строк развёртки — видно только при активном варианте cockpit. */  
      :root[data-layout-variant="cockpit"] body::before {  
        content: "";  
        position: fixed;  
        inset: 0;  
        pointer-events: none;  
        z-index: 100;  
        background: repeating-linear-gradient(to bottom,  
          transparent 0px, transparent 2px,  
          rgba(64, 200, 255, 0.035) 3px, rgba(64, 200, 255, 0.035) 4px);  
        mix-blend-mode: screen;  
      }  
    
[/code]
CSS вставляется как один изолированный тег `<style data-hermes-theme-css>` при применении темы и удаляется при переключении темы. **Ограничение: 32 КБ на тему.**
### Встроенные темы[​](<#built-in-themes> "Direct link to Встроенные темы")
Каждая встроенная тема поставляется со своей палитрой, типографикой и макетом — переключение даёт видимые изменения, выходящие за рамки только цвета.
Тема| Палитра| Типографика| Макет  
---|---|---|---  
**Hermes Teal** (`default`)| Тёмный бирюзовый + кремовый| Системный стек, 15px| Радиус 0.5rem, comfortable  
**Hermes Teal (Large)** (`default-large`)| Та же, что default| Системный стек, 18px, line-height 1.65| Радиус 0.5rem, spacious  
**Midnight** (`midnight`)| Тёмный сине-фиолетовый| Inter + JetBrains Mono, 14px| Радиус 0.75rem, comfortable  
**Ember** (`ember`)| Тёплый малиновый + бронзовый| Spectral (с засечками) + IBM Plex Mono, 15px| Радиус 0.25rem, comfortable  
**Mono** (`mono`)| Оттенки серого| IBM Plex Sans + IBM Plex Mono, 13px| Радиус 0, compact  
**Cyberpunk** (`cyberpunk`)| Неоново-зелёный на чёрном| Share Tech Mono везде, 14px| Радиус 0, compact  
**Rosé** (`rose`)| Розовый + слоновая кость| Fraunces (с засечками) + DM Mono, 16px| Радиус 1rem, spacious  
Темы, которые ссылаются на Google Fonts (все, кроме Hermes Teal), загружают таблицу стилей по требованию — при первом переключении на них тег `<link>` вставляется в `<head>`.
### Полный справочник темы YAML[​](<#full-theme-yaml-reference> "Direct link to Полный справочник темы YAML")
Все настройки в одном файле — скопируйте и удалите то, что не нужно:
[code] 
    # ~/.hermes/dashboard-themes/ocean.yaml  
    name: ocean  
    label: Ocean Deep  
    description: Deep sea blues with coral accents  
      
    # 3-уровневая палитра (принимает {hex, alpha} или короткую запись hex)  
    palette:  
      background:  
        hex: "#0a1628"  
        alpha: 1.0  
      midground:  
        hex: "#a8d0ff"  
        alpha: 1.0  
      foreground:  
        hex: "#ffffff"  
        alpha: 0.0  
      warmGlow: "rgba(255, 107, 107, 0.35)"  
      noiseOpacity: 0.7  
      
    typography:  
      fontSans: "Poppins, system-ui, sans-serif"  
      fontMono: "Fira Code, ui-monospace, monospace"  
      fontDisplay: "Poppins, system-ui, sans-serif"   # опционально  
      fontUrl: "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap"  
      baseSize: "15px"  
      lineHeight: "1.6"  
      letterSpacing: "-0.003em"  
      
    layout:  
      radius: "0.75rem"  
      density: comfortable  
      
    layoutVariant: standard        # standard | cockpit | tiled  
      
    assets:  
      bg: "https://example.com/ocean-bg.jpg"  
      hero: "/my-images/kraken.png"  
      crest: "/my-images/anchor.svg"  
      logo: "/my-images/logo.png"  
      custom:  
        pattern: "/my-images/waves.svg"  
      
    componentStyles:  
      card:  
        boxShadow: "inset 0 0 0 1px rgba(168, 208, 255, 0.18)"  
      header:  
        background: "linear-gradient(180deg, rgba(10, 22, 40, 0.95), rgba(5, 9, 26, 0.9))"  
      
    colorOverrides:  
      destructive: "#ff6b6b"  
      ring: "#ff6b6b"  
      
    customCSS: |  
      /* Любые дополнительные корректировки на уровне селекторов */  
    
[/code]
Обновите панель после создания файла. Переключайте темы в реальном времени из панели заголовка — нажмите на иконку палитры. Выбор сохраняется в `config.yaml` в разделе `dashboard.theme` и восстанавливается при перезагрузке.
* * *
## Плагины[​](<#plugins> "Direct link to Плагины")
Плагин панели — это директория с `manifest.json`, предварительно собранным JS-бандлом и, опционально, CSS-файлом и Python-файлом с маршрутами FastAPI. Плагины располагаются рядом с другими плагинами Hermes в `~/.hermes/plugins/<name>/` — расширение панели находится в подпапке `dashboard/` внутри директории плагина, поэтому один плагин может расширять как CLI/шлюз, так и панель из одной установки.
Плагины не включают в себя React или UI-компоненты. Они используют **Plugin SDK**, доступный через `window.__HERMES_PLUGIN_SDK__`. Это позволяет сохранять бандлы плагинов крошечными (обычно несколько КБ) и избегать конфликтов версий.
### Быстрый старт — ваш первый плагин[​](<#quick-start--your-first-plugin> "Direct link to Быстрый старт — ваш первый плагин")
Создайте структуру директорий:
[code] 
    mkdir -p ~/.hermes/plugins/my-plugin/dashboard/dist  
    
[/code]
Напишите манифест:
[code] 
    // ~/.hermes/plugins/my-plugin/dashboard/manifest.json  
    {  
      "name": "my-plugin",  
      "label": "My Plugin",  
      "icon": "Sparkles",  
      "version": "1.0.0",  
      "tab": {  
        "path": "/my-plugin",  
        "position": "after:skills"  
      },  
      "entry": "dist/index.js"  
    }  
    
[/code]
Напишите JS-бандл (простая IIFE — шаг сборки не нужен):
[code] 
    // ~/.hermes/plugins/my-plugin/dashboard/dist/index.js  
    (function () {  
      "use strict";  
      
      const SDK = window.__HERMES_PLUGIN_SDK__;  
      const { React } = SDK;  
      const { Card, CardHeader, CardTitle, CardContent } = SDK.components;  
      
      function MyPage() {  
        return React.createElement(Card, null,  
          React.createElement(CardHeader, null,  
            React.createElement(CardTitle, null, "My Plugin"),  
          ),  
          React.createElement(CardContent, null,  
            React.createElement("p", { className: "text-sm text-muted-foreground" },  
              "Hello from my custom dashboard tab.",  
            ),  
          ),  
        );  
      }  
      
      window.__HERMES_PLUGINS__.register("my-plugin", MyPage);  
    })();  
    
[/code]
Обновите панель — ваша вкладка появится в навигационной панели после раздела **Skills**.
Пропуск React.createElement
Если вы предпочитаете JSX, используйте любой сборщик (esbuild, Vite, rollup) с React в качестве внешней зависимости и IIFE на выходе. Единственное жёсткое требование — итоговый файл должен быть одним JS-файлом, загружаемым через `<script>`. React никогда не включается в бандл; он берётся из `SDK.React`.
### Структура директории[​](<#directory-layout> "Direct link to Структура директории")
[code] 
    ~/.hermes/plugins/my-plugin/  
    ├── plugin.yaml              # опционально — существующий манифест плагина CLI/шлюза  
    ├── __init__.py              # опционально — существующие хуки CLI/шлюза  
    └── dashboard/               # расширение панели  
        ├── manifest.json        # обязательно — конфигурация вкладки, иконка, точка входа  
        ├── dist/  
        │   ├── index.js         # обязательно — предварительно собранный JS-бандл (IIFE)  
        │   └── style.css        # опционально — пользовательский CSS  
        └── plugin_api.py        # опционально — маршруты бэкенд-API (FastAPI)  
    
[/code]
Одна директория плагина может содержать три ортогональных расширения:
  * `plugin.yaml` + `__init__.py` — плагин CLI/шлюза ([см. страницу плагинов](</docs/user-guide/features/plugins>)).
  * `dashboard/manifest.json` + `dashboard/dist/index.js` — UI-плагин панели.
  * `dashboard/plugin_api.py` — маршруты бэкенда панели.


Ни одно из них не является обязательным; включайте только те уровни, которые вам нужны.
### Справочник манифеста[​](<#manifest-reference> "Direct link to Справочник манифеста")
[code] 
    {  
      "name": "my-plugin",  
      "label": "My Plugin",  
      "description": "What this plugin does",  
      "icon": "Sparkles",  
      "version": "1.0.0",  
      "tab": {  
        "path": "/my-plugin",  
        "position": "after:skills",  
        "override": "/",  
        "hidden": false  
      },  
      "slots": ["sidebar", "header-left"],  
      "entry": "dist/index.js",  
      "css": "dist/style.css",  
      "api": "plugin_api.py"  
    }  
    
[/code]
Поле| Обязательно| Описание  
---|---|---  
`name`| Да| Уникальный идентификатор плагина. Строчные буквы, дефисы допустимы. Используется в URL и регистрации.  
`label`| Да| Отображаемое имя, показываемое на вкладке навигации.  
`description`| Нет| Краткое описание (показывается в административных поверхностях панели).  
`icon`| Нет| Имя иконки Lucide. По умолчанию `Puzzle`. Неизвестные имена возвращаются к `Puzzle`.  
`version`| Нет| Строка Semver. По умолчанию `0.0.0`.  
`tab.path`| Да| URL-путь для вкладки (например `/my-plugin`).  
`tab.position`| Нет| Куда вставить вкладку. `"end"` (по умолчанию), `"after:<путь>"` или `"before:<путь>"` — значение после двоеточия — это **сегмент пути** целевой вкладки (без ведущего слеша). Примеры: `"after:skills"`, `"before:config"`.  
`tab.override`| Нет| Установите в маршрут встроенной страницы (`\"/\"`, `\"/sessions\"`, `\"/config\"`, ...), чтобы **заменить** эту страницу вместо добавления новой вкладки. См. [Замена встроенных страниц](<#replacing-built-in-pages-taboverride>).  
`tab.hidden`| Нет| Если `true`, регистрирует компонент и любые слоты без добавления вкладки в навигацию. Используется плагинами только со слотами. См. [Плагины только со слотами](<#slot-only-plugins-tabhidden>).  
`slots`| Нет| Именованные слоты оболочки, которые заполняет этот плагин. **Только для документации** — фактическая регистрация происходит из JS-бандла через `registerSlot()`. Перечисление слотов здесь делает поверхности обнаружения более информативными.  
`entry`| Да| Путь к JS-бандлу относительно `dashboard/`. По умолчанию `dist/index.js`.  
`css`| Нет| Путь к CSS-файлу для вставки в виде тега `<link>`.  
`api`| Нет| Путь к Python-файлу с маршрутами FastAPI. Монтируется по пути `/api/plugins/<name>/`.  
#### Доступные иконки[​](<#available-icons> "Direct link to Доступные иконки")
Плагины используют имена иконок Lucide. Панель сопоставляет их по имени — неизвестные имена молча возвращаются к `Puzzle`.
В настоящее время сопоставлены: `Activity`, `BarChart3`, `Clock`, `Code`, `Database`, `Eye`, `FileText`, `Globe`, `Heart`, `KeyRound`, `MessageSquare`, `Package`, `Puzzle`, `Settings`, `Shield`, `Sparkles`, `Star`, `Terminal`, `Wrench`, `Zap`.
Нужна другая иконка? Откройте PR в `ICON_MAP` в файле `web/src/App.tsx` — это чисто аддитивное изменение.
### Plugin SDK[​](<#the-plugin-sdk> "Direct link to Plugin SDK")
Всё, что нужно плагину, находится на `window.__HERMES_PLUGIN_SDK__`. Плагины никогда не должны импортировать React напрямую.
[code] 
    const SDK = window.__HERMES_PLUGIN_SDK__;  
      
    // React + хуки  
    SDK.React                    // экземпляр React  
    SDK.hooks.useState  
    SDK.hooks.useEffect  
    SDK.hooks.useCallback  
    SDK.hooks.useMemo  
    SDK.hooks.useRef  
    SDK.hooks.useContext  
    SDK.hooks.createContext  
      
    // UI-компоненты (примитивы shadcn/ui)  
    SDK.components.Card  
    SDK.components.CardHeader  
    SDK.components.CardTitle  
    SDK.components.CardContent  
    SDK.components.Badge  
    SDK.components.Button  
    SDK.components.Input  
    SDK.components.Label  
    SDK.components.Select  
    SDK.components.SelectOption  
    SDK.components.Separator  
    SDK.components.Tabs  
    SDK.components.TabsList  
    SDK.components.TabsTrigger  
    SDK.components.PluginSlot    // рендерит именованный слот (полезно для вложенных UI плагинов)  
      
    // API-клиент Hermes + сырой fetcher  
    SDK.api                      // типизированный клиент — getStatus, getSessions, getConfig, ...  
    SDK.fetchJSON                // сырой fetch для пользовательских endpoint'ов (маршруты, зарегистрированные плагином)  
      
    // Утилиты  
    SDK.utils.cn                 // объединитель классов Tailwind (clsx + twMerge)  
    SDK.utils.timeAgo            // "5м назад" из Unix-метки времени  
    SDK.utils.isoTimeAgo         // "5м назад" из ISO-строки  
      
    // Хуки  
    SDK.useI18n                  // i18n-хук для многоязычных плагинов  
    
[/code]
#### Вызов бэкенда вашего плагина[​](<#calling-your-plugins-backend> "Direct link to Вызов бэкенда вашего плагина")
[code] 
    SDK.fetchJSON("/api/plugins/my-plugin/data")  
      .then((data) => console.log(data))  
      .catch((err) => console.error("API call failed:", err));  
    
[/code]
`fetchJSON` внедряет токен аутентификации сессии, возвращает ошибки как выброшенные исключения и автоматически парсит JSON.
#### Вызов встроенных endpoint'ов Hermes[​](<#calling-built-in-hermes-endpoints> "Direct link to Вызов встроенных endpoint'ов Hermes")
[code] 
    // Статус агента  
    SDK.api.getStatus().then((s) => console.log("Version:", s.version));  
      
    // Недавние сессии  
    SDK.api.getSessions(10).then((resp) => console.log(resp.sessions.length));  
    
[/code]
См. [Web Dashboard → REST API](</docs/user-guide/features/web-dashboard#rest-api>) для полного списка.
### Слоты оболочки[​](<#shell-slots> "Direct link to Слоты оболочки")
Слоты позволяют плагину внедрять компоненты в именованные места оболочки приложения — боковую панель cockpit, заголовок, подвал, слой наложения — без занятия целой вкладки. Несколько плагинов могут заполнять один и тот же слот; они отображаются стопкой в порядке регистрации.
Регистрация из бандла плагина:
[code] 
    window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sidebar", MySidebar);  
    window.__HERMES_PLUGINS__.registerSlot("my-plugin", "header-left", MyCrest);  
    
[/code]
#### Каталог слотов[​](<#slot-catalogue> "Direct link to Каталог слотов")
**Слоты уровня оболочки** (рендерятся в любом месте хрома приложения):
Слот| Расположение  
---|---  
`backdrop`| Внутри стека слоёв `<Backdrop />`, над слоем шума.  
`header-left`| Перед брендом Hermes в верхней панели.  
`header-right`| Перед переключателями темы/языка в верхней панели.  
`header-banner`| Полноширинная полоса под навигацией.  
`sidebar`| Боковая панель cockpit — **рендерится только когда`layoutVariant === "cockpit"`**.  
`pre-main`| Над выходом маршрута (внутри `<main>`).  
`post-main`| Под выходом маршрута (внутри `<main>`).  
`footer-left`| Содержимое ячейки подвала (заменяет значение по умолчанию).  
`footer-right`| Содержимое ячейки подвала (заменяет значение по умолчанию).  
`overlay`| Слой с фиксированной позицией поверх всего остального. Полезен для хрома (строки развёртки, виньетки), который `customCSS` не может реализовать в одиночку.  
**Слоты уровня страницы** (рендерятся только на указанной встроенной странице — используйте их для внедрения виджетов, карточек или панелей инструментов на существующую страницу без переопределения всего маршрута):
Слот| Где рендерится  
---|---  
`analytics:top` / `analytics:bottom`| Вверху / внизу страницы `/analytics`.  
`sessions:top` / `sessions:bottom`| Вверху / внизу страницы `/sessions`.  
`logs:top` / `logs:bottom`| Вверху (над панелью фильтров) / внизу (под просмотрщиком логов) страницы `/logs`.  
`cron:top` / `cron:bottom`| Вверху / внизу страницы `/cron`.  
`skills:top` / `skills:bottom`| Вверху / внизу страницы `/skills`.  
`config:top` / `config:bottom`| Вверху / внизу страницы `/config`.  
`env:top` / `env:bottom`| Вверху / внизу страницы `/env` (Ключи).  
`docs:top` / `docs:bottom`| Вверху (над iframe) / внизу страницы `/docs`.  
`chat:top` / `chat:bottom`| Вверху / внизу страницы `/chat` (активно только когда встроенный чат включён).  
Пример — добавление карточки-баннера в верх страницы Sessions:
[code] 
    function PinnedSessionsBanner() {  
      return React.createElement(Card, null,  
        React.createElement(CardContent, { className: "py-2 text-xs" },  
          "Pinned note injected by my-plugin"),  
      );  
    }  
      
    window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sessions:top", PinnedSessionsBanner);  
    
[/code]
Сочетайте слоты уровня страницы с `tab.hidden: true`, если ваш плагин только дополняет существующие страницы и не требует собственной вкладки в боковой панели.
Оболочка рендерит `<PluginSlot name=\"...\" />` только для слотов, указанных выше. Дополнительные имена принимаются реестром для вложенных UI плагинов — плагин может предоставлять собственные слоты через `SDK.components.PluginSlot`.
#### Повторная регистрация и HMR[​](<#re-registration-and-hmr> "Direct link to Повторная регистрация и HMR")
Если одна и та же пара `(plugin, slot)` регистрируется дважды, более поздний вызов заменяет более ранний — это соответствует тому, как React HMR ожидает поведения перемонтирования плагинов.
### Замена встроенных страниц (`tab.override`)[​](<#replacing-built-in-pages-taboverride> "Direct link to Замена встроенных страниц")
Установка `tab.override` в маршрут встроенной страницы заставляет компонент плагина заменить эту страницу вместо добавления новой вкладки. Полезно, когда тема хочет иметь собственную домашнюю страницу (`/`), но сохранить остальную панель нетронутой.
[code] 
    {  
      "name": "my-home",  
      "label": "Home",  
      "tab": {  
        "path": "/my-home",  
        "override": "/",  
        "position": "end"  
      },  
      "entry": "dist/index.js"  
    }  
    
[/code]
При установленном `override`:
  * Исходный компонент страницы на `/` удаляется из маршрутизатора.
  * Ваш плагин рендерится на `/` вместо него.
  * Вкладка навигации для `tab.path` не добавляется (смысл в замене).


Только один плагин может переопределить данный путь. Если два плагина претендуют на одно и то же переопределение, побеждает первый, а второй игнорируется с предупреждением в режиме разработки.
Если вам нужно только добавить карточку или панель инструментов на существующую страницу без её захвата, используйте [слоты уровня страницы](<#augmenting-built-in-pages-page-scoped-slots>).
### Дополнение встроенных страниц (слоты уровня страницы)[​](<#augmenting-built-in-pages-page-scoped-slots> "Direct link to Дополнение встроенных страниц \\(слоты уровня страницы\\)")
Полная замена через `tab.override` — тяжёлый подход: теперь ваш плагин владеет всей страницей, включая любые будущие обновления, которые мы выпустим для неё. В большинстве случаев вы просто хотите добавить баннер, карточку или панель инструментов на существующую страницу. Для этого и предназначены **слоты уровня страницы**.
Каждая встроенная страница предоставляет слоты `<страница>:top` и `<страница>:bottom`, которые рендерятся вверху и внизу её области содержимого. Ваш плагин заполняет один из них, вызывая `registerSlot()` — встроенная страница продолжает работать нормально, а ваш компонент рендерится рядом с ней.
Доступные слоты: `sessions:*`, `analytics:*`, `logs:*`, `cron:*`, `skills:*`, `config:*`, `env:*`, `docs:*`, `chat:*` (каждый с `:top` и `:bottom`). См. полный каталог в [Слоты оболочки → Каталог слотов](<#slot-catalogue>).
Минимальный пример — закрепить баннер в верхней части страницы Sessions:
[code] 
    // ~/.hermes/plugins/session-notes/dashboard/manifest.json  
    {  
      "name": "session-notes",  
      "label": "Session Notes",  
      "tab": { "path": "/session-notes", "hidden": true },  
      "slots": ["sessions:top"],  
      "entry": "dist/index.js"  
    }  
    
[/code]
[code] 
    // ~/.hermes/plugins/session-notes/dashboard/dist/index.js  
    (function () {  
      const SDK = window.__HERMES_PLUGIN_SDK__;  
      const { React } = SDK;  
      const { Card, CardContent } = SDK.components;  
      
      function Banner() {  
        return React.createElement(Card, null,  
          React.createElement(CardContent, { className: "py-2 text-xs" },  
            "Remember to label important sessions before archiving."),  
        );  
      }  
      
      // Заглушка для скрытой вкладки.  
      window.__HERMES_PLUGINS__.register("session-notes", function () { return null; });  
      
      // Настоящая работа.  
      window.__HERMES_PLUGINS__.registerSlot("session-notes", "sessions:top", Banner);  
    })();  
    
[/code]
Ключевые моменты:
  * `tab.hidden: true` убирает плагин из боковой панели — у него нет отдельной страницы.
  * Поле `slots` в манифесте — только для документации. Фактическая привязка происходит в JS-бандле через `registerSlot()`.
  * Несколько плагинов могут претендовать на один и тот же слот уровня страницы. Они рендерятся стопкой в порядке регистрации.
  * Нулевой след, когда ни один плагин не зарегистрирован: встроенная страница рендерится точно так же, как и раньше.


Встроенный плагин `example-dashboard` содержит живую демонстрацию, которая внедряет баннер в `sessions:top` — установите его, чтобы увидеть паттерн от начала до конца.
### Плагины только со слотами (`tab.hidden`)[​](<#slot-only-plugins-tabhidden> "Direct link to Плагины только со слотами")
Когда `tab.hidden: true`, плагин регистрирует свой компонент (для прямых посещений URL) и любые слоты, но никогда не добавляет вкладку в навигацию. Используется плагинами, которые существуют только для внедрения в слоты — герб в заголовке, HUD в боковой панели, наложение.
[code] 
    {  
      "name": "header-crest",  
      "label": "Header Crest",  
      "tab": {  
        "path": "/header-crest",  
        "position": "end",  
        "hidden": true  
      },  
      "slots": ["header-left"],  
      "entry": "dist/index.js"  
    }  
    
[/code]
Бандл по-прежнему вызывает `register()` с компонентом-заглушкой (хорошая практика на случай, если кто-то перейдёт по URL напрямую), а затем `registerSlot()` для выполнения настоящей работы.
### Маршруты бэкенд-API[​](<#backend-api-routes> "Direct link to Маршруты бэкенд-API")
Плагины могут регистрировать маршруты FastAPI, указав `api` в манифесте. Создайте файл и экспортируйте `router`:
[code] 
    # ~/.hermes/plugins/my-plugin/dashboard/plugin_api.py  
    from fastapi import APIRouter  
      
    router = APIRouter()  
      
    @router.get("/data")  
    async def get_data():  
        return {"items": ["one", "two", "three"]}  
      
    @router.post("/action")  
    async def do_action(body: dict):  
        return {"ok": True, "received": body}  
    
[/code]
Маршруты монтируются по пути `/api/plugins/<name>/`, поэтому приведённые выше становятся:
  * `GET /api/plugins/my-plugin/data`
  * `POST /api/plugins/my-plugin/action`


Маршруты API плагинов обходят аутентификацию по токену сессии, поскольку сервер панели по умолчанию привязан к localhost. **Не открывайте панель на публичном интерфейсе с`--host 0.0.0.0`, если запускаете ненадёжные плагины** — их маршруты также станут доступны.
#### Доступ к внутренностям Hermes[​](<#accessing-hermes-internals> "Direct link to Доступ к внутренностям Hermes")
Маршруты бэкенда выполняются внутри процесса панели, поэтому они могут импортировать напрямую из кодовой базы hermes-agent:
[code] 
    from fastapi import APIRouter  
    from hermes_state import SessionDB  
    from hermes_cli.config import load_config  
      
    router = APIRouter()  
      
    @router.get("/session-count")  
    async def session_count():  
        db = SessionDB()  
        try:  
            count = len(db.list_sessions(limit=9999))  
            return {"count": count}  
        finally:  
            db.close()  
      
    @router.get("/config-snapshot")  
    async def config_snapshot():  
        cfg = load_config()  
        return {"model": cfg.get("model", {})}  
    
[/code]
### Свой CSS для каждого плагина[​](<#custom-css-per-plugin> "Direct link to Свой CSS для каждого плагина")
Если вашему плагину нужны стили, выходящие за рамки классов Tailwind и встроенного `style=`, добавьте CSS-файл и укажите его в манифесте:
[code] 
    {  
      "css": "dist/style.css"  
    }  
    
[/code]
Файл вставляется как тег `<link>` при загрузке плагина. Используйте специфичные имена классов, чтобы избежать конфликтов со стилями панели, и обращайтесь к CSS-переменным панели, чтобы оставаться в курсе темы:
[code] 
    /* dist/style.css */  
    .my-plugin-chart {  
      border: 1px solid var(--color-border);  
      background: var(--color-card);  
      color: var(--color-card-foreground);  
      padding: 1rem;  
    }  
    .my-plugin-chart:hover {  
      border-color: var(--color-ring);  
    }  
    
[/code]
Панель предоставляет каждый токен shadcn как `--color-*`, плюс дополнительные переменные темы (`--theme-asset-*`, `--component-<bucket>-*`, `--radius`, `--spacing-mul`). Используйте их, и ваш плагин будет автоматически переоформляться под активную тему.
### Обнаружение и перезагрузка плагинов[​](<#plugin-discovery--reload> "Direct link to Обнаружение и перезагрузка плагинов")
Панель сканирует три директории на наличие `dashboard/manifest.json`:
Приоритет| Директория| Метка источника  
---|---|---  
1 (побеждает при конфликте)| `~/.hermes/plugins/<name>/dashboard/`| `user`  
2| `<repo>/plugins/memory/<name>/dashboard/`| `bundled`  
2| `<repo>/plugins/<name>/dashboard/`| `bundled`  
3| `./.hermes/plugins/<name>/dashboard/`| `project` — только когда установлена `HERMES_ENABLE_PROJECT_PLUGINS`  
Результаты обнаружения кэшируются на каждый процесс панели. После добавления нового плагина либо:
[code] 
    # Принудительное повторное сканирование без перезапуска  
    curl http://127.0.0.1:9119/api/dashboard/plugins/rescan  
    
[/code]
…либо перезапустите `hermes dashboard`.
#### Жизненный цикл загрузки плагина[​](<#plugin-load-lifecycle> "Direct link to Жизненный цикл загрузки плагина")
  1. Панель загружается. `main.tsx` предоставляет SDK на `window.__HERMES_PLUGIN_SDK__` и реестр на `window.__HERMES_PLUGINS__`.
  2. `App.tsx` вызывает `usePlugins()` → получает `GET /api/dashboard/plugins`.
  3. Для каждого манифеста: вставляется CSS `<link>` (если объявлен), затем тег `<script>` загружает JS-бандл.
  4. IIFE плагина выполняется и вызывает `window.__HERMES_PLUGINS__.register(name, Component)` — и опционально `.registerSlot(name, slot, Component)` для каждого слота.
  5. Панель сопоставляет зарегистрированный компонент с манифестом, добавляет вкладку в навигацию (если не `hidden`) и монтирует компонент как маршрут.


У плагинов есть до **2 секунд** после загрузки их скрипта, чтобы вызвать `register()`. После этого панель перестаёт ждать и завершает начальный рендеринг. Если плагин регистрируется позже, он всё равно появится — навигация реактивна.
Если скрипт плагина не загружается (404, синтаксическая ошибка, исключение во время IIFE), панель записывает предупреждение в консоль браузера и продолжает работу без него.
* * *
## Совместная демка темы и плагина[​](<#combined-theme--plugin-demo> "Direct link to Совместная демка темы и плагина")
Репозиторий содержит `plugins/strike-freedom-cockpit/` как полную демонстрацию переоформления. Она объединяет YAML-тему с плагином только для слотов, чтобы создать HUD в стиле кокпита без форка панели.
**Что демонстрируется:**
  * Полная тема, использующая палитру, типографику, `fontUrl`, `layoutVariant: cockpit`, `assets`, `componentStyles` (зубчатые углы карточек, градиентные фоны), `colorOverrides` и `customCSS` (наложение строк развёртки).
  * Плагин только для слотов (`tab.hidden: true`), который регистрируется в трёх слотах:
    * `sidebar` — панель MS-STATUS с живыми телеметрическими шкалами, управляемыми `SDK.api.getStatus()`.
    * `header-left` — герб фракции, читающий `--theme-asset-crest` из активной темы.
    * `footer-right` — пользовательский слоган, заменяющий стандартную строку организации.
  * Плагин читает изображения, предоставленные темой, через CSS-переменные, поэтому смена темы меняет геройский рисунок/герб без изменения кода плагина.


**Установка:**
[code] 
    # Тема  
    cp plugins/strike-freedom-cockpit/theme/strike-freedom.yaml \  
       ~/.hermes/dashboard-themes/  
      
    # Плагин  
    cp -r plugins/strike-freedom-cockpit ~/.hermes/plugins/  
    
[/code]
Откройте панель, выберите **Strike Freedom** в переключателе тем. Появится боковая панель cockpit, герб отобразится в заголовке, слоган заменит подвал. Переключитесь обратно на **Hermes Teal** — плагин останется установленным, но станет невидимым (слот `sidebar` рендерится только при варианте макета `cockpit`).
Прочтите исходный код плагина (`plugins/strike-freedom-cockpit/dashboard/dist/index.js`), чтобы увидеть, как он читает CSS-переменные, проверяет наличие поддержки слотов в старых версиях панели и регистрирует три слота из одного бандла.
* * *
## Справочник API[​](<#api-reference> "Direct link to Справочник API")
### Endpoint'ы тем[​](<#theme-endpoints> "Direct link to Endpoint'ы тем")
Endpoint| Метод| Описание  
---|---|---  
`/api/dashboard/themes`| GET| Список доступных тем + имя активной. Встроенные возвращают `{name, label, description}`; пользовательские темы также включают поле `definition` с полным нормализованным объектом темы.  
`/api/dashboard/theme`| PUT| Установить активную тему. Тело: `{\"name\": \"midnight\"}`. Сохраняется в `config.yaml` в разделе `dashboard.theme`.  
### Endpoint'ы плагинов[​](<#plugin-endpoints> "Direct link to Endpoint'ы плагинов")
Endpoint| Метод| Описание  
---|---|---  
`/api/dashboard/plugins`| GET| Список обнаруженных плагинов (с манифестами, без внутренних полей).  
`/api/dashboard/plugins/rescan`| GET| Принудительное повторное сканирование директорий плагинов без перезапуска.  
`/dashboard-plugins/<name>/<path>`| GET| Обслуживание статических ресурсов из директории `dashboard/` плагина. Обход пути блокируется.  
`/api/plugins/<name>/*`| *| Маршруты бэкенда, зарегистрированные плагином.  
### SDK на `window`[​](<#sdk-on-window> "Direct link to SDK на window")
Глобальная переменная| Тип| Поставщик  
---|---|---  
`window.__HERMES_PLUGIN_SDK__`| object| `registry.ts` — React, хуки, UI-компоненты, API-клиент, утилиты.  
`window.__HERMES_PLUGINS__.register(name, Component)`| function| Зарегистрировать основной компонент плагина.  
`window.__HERMES_PLUGINS__.registerSlot(name, slot, Component)`| function| Зарегистрироваться в именованном слоте оболочки.  
* * *
## Устранение неполадок[​](<#troubleshooting> "Direct link to Устранение неполадок")
**Моя тема не появляется в переключателе.** Проверьте, что файл находится в `~/.hermes/dashboard-themes/` и заканчивается на `.yaml` или `.yml`. Обновите страницу. Выполните `curl http://127.0.0.1:9119/api/dashboard/themes` — ваша тема должна быть в ответе. Если в YAML есть ошибка парсинга, панель записывает её в `errors.log` в `~/.hermes/logs/`.
**Вкладка моего плагина не отображается.**
  1. Проверьте, что манифест находится по пути `~/.hermes/plugins/<name>/dashboard/manifest.json` (обратите внимание на поддиректорию `dashboard/`).
  2. Выполните `curl http://127.0.0.1:9119/api/dashboard/plugins/rescan` для принудительного повторного обнаружения.
  3. Откройте инструменты разработчика браузера → Сеть — убедитесь, что `manifest.json`, `index.js` и любые CSS загрузились без 404.
  4. Откройте инструменты разработчика браузера → Консоль — ищите ошибки во время IIFE или `window.__HERMES_PLUGINS__ is undefined` (указывает на то, что SDK не инициализировался, обычно из-за более раннего сбоя рендеринга React).
  5. Убедитесь, что ваш бандл вызывает `window.__HERMES_PLUGINS__.register(...)` с **тем же именем**, что и `manifest.json:name`.


**Компоненты, зарегистрированные в слотах, не рендерятся.** Слот `sidebar` рендерится только когда активная тема имеет `layoutVariant: cockpit`. Остальные слоты рендерятся всегда. Если вы регистрируетесь в слот без попаданий, добавьте `console.log` внутри `registerSlot`, чтобы подтвердить, что бандл плагина вообще выполнился.
**Маршруты бэкенда плагина возвращают 404.**
  1. Убедитесь, что в манифесте есть `"api": "plugin_api.py"`, указывающий на существующий файл внутри `dashboard/`.
  2. Перезапустите `hermes dashboard` — маршруты API плагина монтируются один раз при запуске, **а не** при повторном сканировании.
  3. Проверьте, что `plugin_api.py` экспортирует `router = APIRouter()` на уровне модуля. Другие имена экспорта не подхватываются.
  4. Отслеживайте `~/.hermes/logs/errors.log` на предмет `Failed to load plugin <name> API routes` — ошибки импорта записываются туда.


**Смена темы сбрасывает мои переопределения цветов.** `colorOverrides` ограничены активной темой и очищаются при переключении темы — это сделано намеренно. Если вам нужны переопределения, которые сохраняются, поместите их в YAML вашей темы, а не в интерактивный переключатель.
**Свой CSS темы (customCSS) обрезается.** Блок `customCSS` ограничен 32 КБ на тему. Разделите большие таблицы стилей на несколько тем или переключитесь на плагин, который внедряет полную таблицу стилей через своё поле `css` (без ограничения по размеру).
**Я хочу опубликовать плагин на PyPI.** Плагины панели устанавливаются через структуру директорий, а не через точку входа pip. Самый чистый путь распространения на сегодня — это git-репозиторий, который пользователь клонирует в `~/.hermes/plugins/`. Установщик на основе pip для плагинов панели в настоящее время не подключён.
  * [Содержание](<#table-of-contents>)
  * [Темы](<#themes>)
    * [Быстрый старт — ваша первая тема](<#quick-start--your-first-theme>)
    * [Палитра, типографика, макет](<#palette-typography-layout>)
    * [Варианты макета](<#layout-variants>)
    * [Ресурсы темы (изображения как CSS-переменные)](<#theme-assets-images-as-css-vars>)
    * [Переопределения хрома компонентов](<#component-chrome-overrides>)
    * [Переопределения цветов](<#color-overrides>)
    * [Сырой `customCSS`](<#raw-customcss>)
    * [Встроенные темы](<#built-in-themes>)
    * [Полный справочник темы YAML](<#full-theme-yaml-reference>)
  * [Плагины](<#plugins>)
    * [Быстрый старт — ваш первый плагин](<#quick-start--your-first-plugin>)
    * [Структура директории](<#directory-layout>)
    * [Справочник манифеста](<#manifest-reference>)
    * [Plugin SDK](<#the-plugin-sdk>)
    * [Слоты оболочки](<#shell-slots>)
    * [Замена встроенных страниц (`tab.override`)](<#replacing-built-in-pages-taboverride>)
    * [Дополнение встроенных страниц (слоты уровня страницы)](<#augmenting-built-in-pages-page-scoped-slots>)
    * [Плагины только со слотами (`tab.hidden`)](<#slot-only-plugins-tabhidden>)
    * [Маршруты бэкенд-API](<#backend-api-routes>)
    * [Свой CSS для каждого плагина](<#custom-css-per-plugin>)
    * [Обнаружение и перезагрузка плагинов](<#plugin-discovery--reload>)
  * [Совместная демка темы и плагина](<#combined-theme--plugin-demo>)
  * [Справочник API](<#api-reference>)
    * [Endpoint'ы тем](<#theme-endpoints>)
    * [Endpoint'ы плагинов](<#plugin-endpoints>)
    * [SDK на `window`](<#sdk-on-window>)
  * [Устранение неполадок](<#troubleshooting>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard -->
