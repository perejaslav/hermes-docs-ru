On this page
54 реальных дизайн-системы (Stripe, Linear, Vercel) в HTML/CSS.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/popular-web-designs`  |
Version| `1.0.0`  |
Author| Hermes Agent + Teknium (дизайн-системы из VoltAgent/awesome-design-md)  |
License| MIT  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Popular Web Designs
54 реальные дизайн-системы, готовые к использованию при генерации HTML/CSS. Каждый шаблон содержит полный визуальный язык сайта: цветовую палитру, иерархию типографики, стили компонентов, систему отступов, тени, адаптивное поведение и практические подсказки для агента с точными CSS-значениями.
## Related design skills[​](<#related-design-skills> "Direct link to Related design skills")
  * **`claude-design`** — используйте для _процесса и вкуса_ в дизайне (определение брифа, создание вариантов, проверка локального HTML-артефакта, избегание AI-дизайн-слабости). Сочетайте с этим навыком, когда пользователь хочет продуманную страницу в стиле известного бренда: `claude-design` управляет процессом, а этот навык предоставляет визуальный словарь.
  * **`design-md`** — используйте, когда результат должен быть формальным файлом спецификации DESIGN.md с токенами, а не готовым артефактом.


## How to Use[​](<#how-to-use> "Direct link to How to Use")
  1. Выберите дизайн из каталога ниже
  2. Загрузите его: `skill_view(name="popular-web-designs", file_path="templates/<site>.md")`
  3. Используйте токены дизайна и спецификации компонентов при генерации HTML
  4. Сочетайте с навыком `generative-widgets` для публикации результата через cloudflared-туннель


Каждый шаблон включает блок **Hermes Implementation Notes** вверху с:
  * CDN-заменой шрифта и тегом Google Fonts `<link>` (готов к вставке)
  * CSS font-family стеками для основного и моноширинного шрифта
  * Напоминаниями использовать `write_file` для создания HTML и `browser_vision` для проверки


## HTML Generation Pattern[​](<#html-generation-pattern> "Direct link to HTML Generation Pattern")
[code] 
    <!DOCTYPE html>  
    <html lang="ru">  
    <head>  
      <meta charset="UTF-8">  
      <meta name="viewport" content="width=device-width, initial-scale=1.0">  
      <title>Заголовок страницы</title>  
      <!-- Вставьте Google Fonts <link> из заметок Hermes в шаблоне -->  
      <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">  
      <style>  
        /* Примените цветовую палитру шаблона как CSS custom properties */  
        :root {  
          --color-bg: #ffffff;  
          --color-text: #171717;  
          --color-accent: #533afd;  
          /* ... ещё из раздела 2 шаблона */  
        }  
        /* Примените типографику из раздела 3 шаблона */  
        body {  
          font-family: 'Inter', system-ui, sans-serif;  
          color: var(--color-text);  
          background: var(--color-bg);  
        }  
        /* Примените стили компонентов из раздела 4 шаблона */  
        /* Примените макет из раздела 5 шаблона */  
        /* Примените тени из раздела 6 шаблона */  
      </style>  
    </head>  
    <body>  
      <!-- Создавайте, используя спецификации компонентов из шаблона -->  
    </body>  
    </html>  
    
[/code]
Запишите файл с помощью `write_file`, опубликуйте через workflow `generative-widgets` (cloudflared-туннель) и проверьте результат с помощью `browser_vision` для подтверждения визуальной точности.
## Font Substitution Reference[​](<#font-substitution-reference> "Direct link to Font Substitution Reference")
Большинство сайтов используют проприетарные шрифты, недоступные через CDN. Каждый шаблон сопоставляется с заменой из Google Fonts, сохраняющей характер дизайна. Типичные соответствия:
Проприетарный шрифт| CDN-замена| Характер  
---|---|---  
Geist / Geist Sans| Geist (на Google Fonts)| Геометрический, сжатый трекинг  
Geist Mono| Geist Mono (на Google Fonts)| Чистый моноширинный, лигатуры  
sohne-var (Stripe)| Source Sans 3| Элегантность светлого веса  
Berkeley Mono| JetBrains Mono| Технический моноширинный  
Airbnb Cereal VF| DM Sans| Округлый, дружелюбный геометрический  
Circular (Spotify)| DM Sans| Геометрический, тёплый  
figmaSans| Inter| Чистый гуманистический  
Pin Sans (Pinterest)| DM Sans| Дружелюбный, округлый  
NVIDIA-EMEA| Inter (или Arial system)| Индустриальный, чистый  
CoinbaseDisplay/Sans| DM Sans| Геометрический, надёжный  
UberMove| DM Sans| Жирный, плотный  
HashiCorp Sans| Inter| Корпоративный, нейтральный  
waldenburgNormal (Sanity)| Space Grotesk| Геометрический, слегка сжатый  
IBM Plex Sans/Mono| IBM Plex Sans/Mono| Доступен на Google Fonts  
Rubik (Sentry)| Rubik| Доступен на Google Fonts  
Когда CDN-шрифт шаблона совпадает с оригиналом (Inter, IBM Plex, Rubik, Geist), потери от замены нет. Когда используется замена (DM Sans для Circular, Source Sans 3 для sohne-var), следуйте значениям веса, размера и межбуквенного расстояния из шаблона — они несут больше визуальной идентичности, чем конкретный гарнитура шрифта.
## Design Catalog[​](<#design-catalog> "Direct link to Design Catalog")
### AI & Machine Learning[​](<#ai--machine-learning> "Direct link to AI & Machine Learning")
Шаблон| Сайт| Стиль  
---|---|---  
`claude.md`| Anthropic Claude| Тёплый терракотовый акцент, чистый редакторский макет  
`cohere.md`| Cohere| Яркие градиенты, эстетика информационных панелей  
`elevenlabs.md`| ElevenLabs| Тёмный кинематографичный UI, эстетика аудиоволн  
`minimax.md`| Minimax| Смелый тёмный интерфейс с неоновыми акцентами  
`mistral.ai.md`| Mistral AI| Французский инженерный минимализм, фиолетовые тона  
`ollama.md`| Ollama| Терминал-ориентированный, монохромная простота  
`opencode.ai.md`| OpenCode AI| Разработчик-центричная тёмная тема, полный моноширинный  
`replicate.md`| Replicate| Чистый белый холст, код-ориентированный  
`runwayml.md`| RunwayML| Кинематографичный тёмный UI, медиа-насыщенный макет  
`together.ai.md`| Together AI| Технический, стиль чертежа  
`voltagent.md`| VoltAgent| Чёрный как смоль холст, изумрудный акцент, терминал-нативный  
`x.ai.md`| xAI| Суровая монохромия, футуристический минимализм, полный моноширинный  
### Developer Tools & Platforms[​](<#developer-tools--platforms> "Direct link to Developer Tools & Platforms")
Шаблон| Сайт| Стиль  
---|---|---  
`cursor.md`| Cursor| Гладкий тёмный интерфейс, градиентные акценты  
`expo.md`| Expo| Тёмная тема, плотный межбуквенный интервал, код-центричный  
`linear.app.md`| Linear| Ультра-минималистичный тёмный режим, точный, фиолетовый акцент  
`lovable.md`| Lovable| Игривые градиенты, дружелюбная разработческая эстетика  
`mintlify.md`| Mintlify| Чистый, зелёный акцент, оптимизирован для чтения  
`posthog.md`| PostHog| Игривый брендинг, разработчик-дружелюбный тёмный UI  
`raycast.md`| Raycast| Гладкий тёмный хром, яркие градиентные акценты  
`resend.md`| Resend| Минималистичная тёмная тема, моноширинные акценты  
`sentry.md`| Sentry| Тёмная панель, насыщенный данными, розово-фиолетовый акцент  
`supabase.md`| Supabase| Тёмная изумрудная тема, код-ориентированный инструмент разработчика  
`superhuman.md`| Superhuman| Премиальный тёмный UI, клавиатура-ориентированный, фиолетовое свечение  
`vercel.md`| Vercel| Чёрно-белая точность, система шрифтов Geist  
`warp.md`| Warp| Тёмный интерфейс как в IDE, блочный UI команд  
`zapier.md`| Zapier| Тёплый оранжевый, дружелюбный, с иллюстрациями  
### Infrastructure & Cloud[​](<#infrastructure--cloud> "Direct link to Infrastructure & Cloud")
Шаблон| Сайт| Стиль  
---|---|---  
`clickhouse.md`| ClickHouse| Жёлтый акцент, стиль технической документации  
`composio.md`| Composio| Современный тёмный с красочными иконками интеграций  
`hashicorp.md`| HashiCorp| Корпоративно-чистый, чёрный и белый  
`mongodb.md`| MongoDB| Зелёный брендинг с листом, фокус на документацию разработчика  
`sanity.md`| Sanity| Красный акцент, контент-ориентированный редакторский макет  
`stripe.md`| Stripe| Фирменные фиолетовые градиенты, элегантность weight-300  
### Design & Productivity[​](<#design--productivity> "Direct link to Design & Productivity")
Шаблон| Сайт| Стиль  
---|---|---  
`airtable.md`| Airtable| Красочный, дружелюбный, эстетика структурированных данных  
`cal.md`| Cal.com| Чистый нейтральный UI, разработчик-ориентированная простота  
`clay.md`| Clay| Органические формы, мягкие градиенты, художественный макет  
`figma.md`| Figma| Яркий многоцветный, игривый, но профессиональный  
`framer.md`| Framer| Смелый чёрный и синий, движение-ориентированный, дизайн-направленный  
`intercom.md`| Intercom| Дружелюбная синяя палитра, шаблоны разговорного UI  
`miro.md`| Miro| Яркий жёлтый акцент, эстетика бесконечного холста  
`notion.md`| Notion| Тёплый минимализм, заголовки с засечками, мягкие поверхности  
`pinterest.md`| Pinterest| Красный акцент, сетка-масонка, макет с фокусом на изображения  
`webflow.md`| Webflow| Синий акцент, эстетика отполированного маркетингового сайта  
### Fintech & Crypto[​](<#fintech--crypto> "Direct link to Fintech & Crypto")
Шаблон| Сайт| Стиль  
---|---|---  
`coinbase.md`| Coinbase| Чистый синий стиль, ориентирован на доверие, институциональное ощущение  
`kraken.md`| Kraken| Фиолетовый акцент в тёмном UI, информационные панели с данными  
`revolut.md`| Revolut| Гладкий тёмный интерфейс, градиентные карты, финтех-точность  
`wise.md`| Wise| Яркий зелёный акцент, дружелюбный и понятный  
### Enterprise & Consumer[​](<#enterprise--consumer> "Direct link to Enterprise & Consumer")
Шаблон| Сайт| Стиль  
---|---|---  
`airbnb.md`| Airbnb| Тёплый коралловый акцент, фотография-ориентированный, округлый UI  
`apple.md`| Apple| Премиальное белое пространство, SF Pro, кинематографичные изображения  
`bmw.md`| BMW| Тёмные премиальные поверхности, точный инженерный эстетика  
`ibm.md`| IBM| Дизайн-система Carbon, структурированная синяя палитра  
`nvidia.md`| NVIDIA| Зелёно-чёрная энергия, эстетика технической мощи  
`spacex.md`| SpaceX| Суровый чёрный и белый, изображения во весь экран, футуристичный  
`spotify.md`| Spotify| Яркий зелёный на тёмном, жирный шрифт, обложки альбомов  
`uber.md`| Uber| Смелый чёрный и белый, плотный шрифт, городская энергия  
## Choosing a Design[​](<#choosing-a-design> "Direct link to Choosing a Design")
Сопоставляйте дизайн с содержанием:
  * **Инструменты разработчика / панели управления:** Linear, Vercel, Supabase, Raycast, Sentry
  * **Документация / контентные сайты:** Mintlify, Notion, Sanity, MongoDB
  * **Маркетинг / лендинги:** Stripe, Framer, Apple, SpaceX
  * **Тёмные UI:** Linear, Cursor, ElevenLabs, Warp, Superhuman
  * **Светлые / чистые UI:** Vercel, Stripe, Notion, Cal.com, Replicate
  * **Игривые / дружелюбные:** PostHog, Figma, Lovable, Zapier, Miro
  * **Премиальные / люксовые:** Apple, BMW, Stripe, Superhuman, Revolut
  * **Насыщенные данными / панели:** Sentry, Kraken, Cohere, ClickHouse
  * **Моноширинные / терминальные:** Ollama, OpenCode, x.ai, VoltAgent


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Related design skills](<#related-design-skills>)
  * [How to Use](<#how-to-use>)
  * [HTML Generation Pattern](<#html-generation-pattern>)
  * [Font Substitution Reference](<#font-substitution-reference>)
  * [Design Catalog](<#design-catalog>)
    * [AI & Machine Learning](<#ai--machine-learning>)
    * [Developer Tools & Platforms](<#developer-tools--platforms>)
    * [Infrastructure & Cloud](<#infrastructure--cloud>)
    * [Design & Productivity](<#design--productivity>)
    * [Fintech & Crypto](<#fintech--crypto>)
    * [Enterprise & Consumer](<#enterprise--consumer>)
  * [Choosing a Design](<#choosing-a-design>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-popular-web-designs -->
