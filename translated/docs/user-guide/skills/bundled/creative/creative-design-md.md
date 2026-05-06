On this page
Создание/проверка/экспорт файлов Google DESIGN.md со спецификацией токенов.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/design-md`  |
Version| `1.0.0`  |
Author| Hermes Agent  |
License| MIT  |
Tags| `design`, `design-system`, `tokens`, `ui`, `accessibility`, `wcag`, `tailwind`, `dtcg`, `google`  |
Related skills| [`popular-web-designs`](</docs/user-guide/skills/bundled/creative/creative-popular-web-designs>), [`claude-design`](</docs/user-guide/skills/bundled/creative/creative-claude-design>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>), [`architecture-diagram`](</docs/user-guide/skills/bundled/creative/creative-architecture-diagram>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# DESIGN.md Skill
DESIGN.md — это открытая спецификация Google (Apache-2.0, `google-labs-code/design.md`) для описания визуального стиля агентам кодирования. Один файл объединяет:
  * **YAML front matter** — машиночитаемые дизайн-токены (нормативные значения)
  * **Markdown тело** — человекочитаемые обоснования, organised в канонические секции


Токены дают точные значения. Проза объясняет агентам _почему_ эти значения существуют и как их применять. CLI (`npx @google/design.md`) проверяет структуру + WCAG-контрастность, сравнивает версии на регрессии и экспортирует в Tailwind или W3C DTCG JSON.
## When to use this skill[​](<#when-to-use-this-skill> "Direct link to When to use this skill")
  * Пользователь просит файл DESIGN.md, дизайн-токены или спецификацию дизайн-системы
  * Пользователь хочет единообразный UI/бренд в нескольких проектах или инструментах
  * Пользователь вставляет существующий DESIGN.md и просит проверить, сравнить, экспортировать или расширить его
  * Пользователь просит портировать гайдлайн стиля в формат, понятный агентам
  * Пользователь хочет проверку контрастности / WCAG-доступности своей цветовой палитры


Для чисто визуального вдохновения или примеров макетов используйте `popular-web-designs`. Для _процесса и вкуса_ при проектировании разового HTML-артефакта с нуля (прототип, презентация, лендинг, лаборатория компонентов) используйте `claude-design`. Этот навык предназначен для _формального файла спецификации_.
## File anatomy[​](<#file-anatomy> "Direct link to File anatomy")
[code] 
    ---  
    version: alpha  
    name: Heritage  
    description: Architectural minimalism meets journalistic gravitas.  
    colors:  
      primary: "#1A1C1E"  
      secondary: "#6C7278"  
      tertiary: "#B8422E"  
      neutral: "#F7F5F2"  
    typography:  
      h1:  
        fontFamily: Public Sans  
        fontSize: 3rem  
        fontWeight: 700  
        lineHeight: 1.1  
        letterSpacing: "-0.02em"  
      body-md:  
        fontFamily: Public Sans  
        fontSize: 1rem  
    rounded:  
      sm: 4px  
      md: 8px  
      lg: 16px  
    spacing:  
      sm: 8px  
      md: 16px  
      lg: 24px  
    components:  
      button-primary:  
        backgroundColor: "{colors.tertiary}"  
        textColor: "#FFFFFF"  
        rounded: "{rounded.sm}"  
        padding: 12px  
      button-primary-hover:  
        backgroundColor: "{colors.primary}"  
    ---  
      
    ## Overview  
      
    Architectural Minimalism meets Journalistic Gravitas...  
      
    ## Colors  
      
    - **Primary (#1A1C1E):** Deep ink for headlines and core text.  
    - **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction.  
      
    ## Typography  
      
    Public Sans for everything except small all-caps labels...  
      
    ## Components  
      
    `button-primary` is the only high-emphasis action on a page...  
    
[/code]
## Token types[​](<#token-types> "Direct link to Token types")
Тип| Формат| Пример  
---|---|---  
Color| `#` + hex (sRGB)| `"#1A1C1E"`  
Dimension| число + единица (`px`, `em`, `rem`)| `48px`, `-0.02em`  
Token reference| `{path.to.token}`| `{colors.primary}`  
Typography| объект с `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `fontFeature`, `fontVariation`| см. выше  
Белый список свойств компонентов: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`. Варианты (hover, active, pressed) — это **отдельные записи компонентов** со связанными именами ключей (`button-primary-hover`), не вложенные.
## Canonical section order[​](<#canonical-section-order> "Direct link to Canonical section order")
Секции опциональны, но присутствующие ДОЛЖНЫ быть в этом порядке. Повторяющиеся заголовки приводят к ошибке файла.
  1. Overview (псевдоним: Brand & Style)
  2. Colors
  3. Typography
  4. Layout (псевдоним: Layout & Spacing)
  5. Elevation & Depth (псевдоним: Elevation)
  6. Shapes
  7. Components
  8. Do's and Don'ts


Неизвестные секции сохраняются, ошибка не выдаётся. Неизвестные имена токенов принимаются, если тип значения корректен. Неизвестные свойства компонентов вызывают предупреждение.
## Workflow: authoring a new DESIGN.md[​](<#workflow-authoring-a-new-designmd> "Direct link to Workflow: authoring a new DESIGN.md")
  1. **Спросите пользователя** (или определите) тон бренда, акцентный цвет и направление типографики. Если он предоставил сайт, изображение или настроение, переведите это в форму токенов выше.
  2. **Напишите`DESIGN.md`** в корне проекта с помощью `write_file`. Всегда включайте `name:` и `colors:`; остальные секции опциональны, но приветствуются.
  3. **Используйте ссылки на токены** (`{colors.primary}`) в секции `components:` вместо повторного ввода hex-значений. Это сохраняет единственный источник истины для палитры.
  4. **Проверьте** (см. ниже). Исправьте все сломанные ссылки или WCAG-нарушения перед возвратом.
  5. **Если у пользователя есть существующий проект** , также запишите экспорт в Tailwind или DTCG рядом с файлом (`tailwind.theme.json`, `tokens.json`).


## Workflow: lint / diff / export[​](<#workflow-lint--diff--export> "Direct link to Workflow: lint / diff / export")
CLI — это `@google/design.md` (Node). Используйте `npx` — глобальная установка не требуется.
[code] 
    # Validate structure + token references + WCAG contrast  
    npx -y @google/design.md lint DESIGN.md  
      
    # Compare two versions, fail on regression (exit 1 = regression)  
    npx -y @google/design.md diff DESIGN.md DESIGN-v2.md  
      
    # Export to Tailwind theme JSON  
    npx -y @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json  
      
    # Export to W3C DTCG (Design Tokens Format Module) JSON  
    npx -y @google/design.md export --format dtcg DESIGN.md > tokens.json  
      
    # Print the spec itself — useful when injecting into an agent prompt  
    npx -y @google/design.md spec --rules-only --format json  
    
[/code]
Все команды принимают `-` для stdin. `lint` возвращает exit 1 при ошибках. Используйте флаг `--format json` и парсите вывод, если нужно структурированно сообщить о находках.
### Lint rule reference (what the 7 rules catch)[​](<#lint-rule-reference-what-the-7-rules-catch> "Direct link to Lint rule reference (what the 7 rules catch)")
  * `broken-ref` (ошибка) — `{colors.missing}` указывает на несуществующий токен
  * `duplicate-section` (ошибка) — одинаковый `## Heading` встречается дважды
  * `invalid-color`, `invalid-dimension`, `invalid-typography` (ошибка)
  * `wcag-contrast` (предупреждение/инфо) — соотношение `textColor` к `backgroundColor` компонента против WCAG AA (4.5:1) и AAA (7:1)
  * `unknown-component-property` (предупреждение) — вне указанного выше белого списка


Когда пользователь заботится о доступности, явно упомяните это в сводке — находки WCAG — самая весомая причина использовать CLI.
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **Не вкладывайте варианты компонентов.** `button-primary.hover` неправильно; `button-primary-hover` как отдельный ключ — правильно.
  * **Hex-цвета должны быть в кавычках.** YAML иначе споткнётся о `#` или странно обрежет значения вроде `#1A1C1E`.
  * **Отрицательные размеры тоже требуют кавычек.** `letterSpacing: -0.02em` парсится как YAML flow — пишите `letterSpacing: "-0.02em"`.
  * **Порядок секций обязателен.** Если пользователь дал текст в случайном порядке, переупорядочьте его в соответствии с каноническим списком перед сохранением.
  * **`version: alpha` — текущая версия спецификации** (на апрель 2026). Спецификация помечена как alpha — следите за изменениями.
  * **Ссылки на токены разрешаются по точечному пути.** `{colors.primary}` работает; `{primary}` — нет.


## Spec source of truth[​](<#spec-source-of-truth> "Direct link to Spec source of truth")
  * Репозиторий: <https://github.com/google-labs-code/design.md> (Apache-2.0)
  * CLI: `@google/design.md` на npm
  * Лицензия сгенерированных DESIGN.md файлов: зависит от проекта пользователя; сама спецификация под Apache-2.0.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use this skill](<#when-to-use-this-skill>)
  * [File anatomy](<#file-anatomy>)
  * [Token types](<#token-types>)
  * [Canonical section order](<#canonical-section-order>)
  * [Workflow: authoring a new DESIGN.md](<#workflow-authoring-a-new-designmd>)
  * [Workflow: lint / diff / export](<#workflow-lint--diff--export>)
    * [Lint rule reference (what the 7 rules catch)](<#lint-rule-reference-what-the-7-rules-catch>)
  * [Pitfalls](<#pitfalls>)
  * [Spec source of truth](<#spec-source-of-truth>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-design-md -->
