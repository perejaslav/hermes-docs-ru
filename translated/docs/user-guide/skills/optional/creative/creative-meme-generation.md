On this page
Генерируйте настоящие изображения мемов, выбирая шаблон и накладывая текст с помощью Pillow. Создаёт реальные .png-файлы мемов.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/creative/meme-generation`  |
|Путь| `optional-skills/creative/meme-generation`  |
|Версия| `2.0.0`  |
|Автор| adanaleycio  |
|Лицензия| MIT  |
|Теги| `creative`, `memes`, `humor`, `images`  |
|Связанные навыки| [`ascii-art`](</docs/user-guide/skills/bundled/creative/creative-ascii-art>), `generative-widgets`  |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

> **info**
> Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.

# Генерация мемов
Создавайте настоящие изображения мемов по теме. Выбирает шаблон, пишет подписи и рендерит реальный .png-файл с наложением текста.

## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")

  * Пользователь просит сделать или сгенерировать мем
  * Пользователь хочет мем на определённую тему, ситуацию или проблему
  * Пользователь говорит «мем это» или что-то подобное

## Доступные шаблоны[​](<#available-templates> "Прямая ссылка на Доступные шаблоны")

Скрипт поддерживает **любые из ~100 популярных шаблонов imgflip** по имени или ID, а также 10 курируемых шаблонов с точно настроенным позиционированием текста.

### Курируемые шаблоны (пользовательское размещение текста)[​](<#curated-templates-custom-text-placement> "Прямая ссылка на Курируемые шаблоны (пользовательское размещение текста)")

| ID | Имя | Поля | Лучше всего для |
|---|---|---|---|
| `this-is-fine` | This is Fine | верх, низ | хаос, отрицание |
| `drake` | Drake Hotline Bling | отвергаю, одобряю | отвержение/предпочтение |
| `distracted-boyfriend` | Distracted Boyfriend | отвлечение, текущее, персона | искушение, смена приоритетов |
| `two-buttons` | Two Buttons | лево, право, персона | невозможный выбор |
| `expanding-brain` | Expanding Brain | 4 уровня | нарастающая ирония |
| `change-my-mind` | Change My Mind | утверждение | хот-тейки |
| `woman-yelling-at-cat` | Woman Yelling at Cat | женщина, кот | споры |
| `one-does-not-simply` | One Does Not Simply | верх, низ | обманчиво сложные вещи |
| `grus-plan` | Gru's Plan | шаг1-3, осознание | планы, которые идут не так |
| `batman-slapping-robin` | Batman Slapping Robin | robin, batman | пресечение плохих идей |

### Динамические шаблоны (из imgflip API)[​](<#dynamic-templates-from-imgflip-api> "Прямая ссылка на Динамические шаблоны (из imgflip API)")

Любой шаблон, отсутствующий в курируемом списке, можно использовать по имени или imgflip ID. Они получают интеллектуальное позиционирование текста по умолчанию (верх/низ для 2 полей, равномерно для 3+). Поиск:

[code]
    python "$SKILL_DIR/scripts/generate_meme.py" --search "disaster"
    
[/code]

## Процедура[​](<#procedure> "Прямая ссылка на Процедура")

### Режим 1: Классический шаблон (по умолчанию)[​](<#mode-1-classic-template-default> "Прямая ссылка на Режим 1: Классический шаблон (по умолчанию)")

  1. Прочитайте тему пользователя и определите основную динамику (хаос, дилемма, предпочтение, ирония и т.д.)
  2. Выберите наиболее подходящий шаблон. Используйте колонку «Лучше всего для» или поиск с `--search`.
  3. Напишите короткие подписи для каждого поля (макс. 8–12 слов на поле, чем короче, тем лучше).
  4. Найдите директорию скриптов навыка:

[code] SKILL_DIR=$(dirname "$(find ~/.hermes/skills -path '*/meme-generation/SKILL.md' 2>/dev/null | head -1)")
         
[/code]

  5. Запустите генератор:

[code] python "$SKILL_DIR/scripts/generate_meme.py" <template_id> /tmp/meme.png "caption 1" "caption 2" ...
         
[/code]

  6. Верните изображение с помощью `MEDIA:/tmp/meme.png`

### Режим 2: Пользовательское AI-изображение (когда доступен image_generate)[​](<#mode-2-custom-ai-image-when-image_generate-is-available> "Прямая ссылка на Режим 2: Пользовательское AI-изображение (когда доступен image_generate)")

Используйте этот режим, когда ни один классический шаблон не подходит или пользователь хочет что-то оригинальное.

  1. Сначала напишите подписи.
  2. Используйте `image_generate` для создания сцены, соответствующей концепции мема. НЕ включайте текст в запрос изображения — текст будет добавлен скриптом. Опишите только визуальную сцену.
  3. Найдите путь к сгенерированному изображению из URL-результата image_generate. При необходимости скачайте его в локальную директорию.
  4. Запустите скрипт с `--image` для наложения текста, выбрав режим:
     * **Overlay** (текст прямо на изображении, белый с чёрной обводкой):

[code] python "$SKILL_DIR/scripts/generate_meme.py" --image /path/to/scene.png /tmp/meme.png "top text" "bottom text"
           
[/code]

     * **Bars** (чёрные полосы сверху/снизу с белым текстом — чище, всегда читаемо):

[code] python "$SKILL_DIR/scripts/generate_meme.py" --image /path/to/scene.png --bars /tmp/meme.png "top text" "bottom text"
           
[/code]

Используйте `--bars`, когда изображение загружено/детализировано и текст поверх него будет плохо читаться.

  5. **Проверьте с помощью vision** (если доступен `vision_analyze`): убедитесь, что результат выглядит хорошо:

[code] vision_analyze(image_url="/tmp/meme.png", question="Is the text legible and well-positioned? Does the meme work visually?")
         
[/code]

Если модель vision сообщает о проблемах (текст трудно читать, плохое расположение и т.д.), попробуйте другой режим (переключайтесь между overlay и bars) или создайте новую сцену.

  6. Верните изображение с помощью `MEDIA:/tmp/meme.png`

## Примеры[​](<#examples> "Прямая ссылка на Примеры")

**«отладка продакшена в 2 часа ночи»:**

[code]
    python generate_meme.py this-is-fine /tmp/meme.png "SERVERS ARE ON FIRE" "This is fine"
    
[/code]

**«выбор между сном и ещё одной серией»:**

[code]
    python generate_meme.py drake /tmp/meme.png "Getting 8 hours of sleep" "One more episode at 3 AM"
    
[/code]

**«этапы утра понедельника»:**

[code]
    python generate_meme.py expanding-brain /tmp/meme.png "Setting an alarm" "Setting 5 alarms" "Sleeping through all alarms" "Working from bed"
    
[/code]

## Список шаблонов[​](<#listing-templates> "Прямая ссылка на Список шаблонов")

Чтобы увидеть все доступные шаблоны:

[code]
    python generate_meme.py --list
    
[/code]

## Ошибки и советы[​](<#pitfalls> "Прямая ссылка на Ошибки и советы")

  * Делайте подписи КОРОТКИМИ. Мемы с длинным текстом выглядят ужасно.
  * Количество текстовых аргументов должно соответствовать количеству полей шаблона.
  * Выбирайте шаблон, который подходит под структуру шутки, а не только под тему.
  * Не создавайте оскорбительный, агрессивный или направленный на личность контент.
  * Скрипт кэширует изображения шаблонов в `scripts/.cache/` после первой загрузки.

## Проверка результата[​](<#verification> "Прямая ссылка на Проверка результата")

Результат корректен, если:

  * .png-файл создан по указанному пути вывода
  * Текст читаем (белый с чёрной обводкой) на шаблоне
  * Шутка срабатывает — подпись соответствует структуре шаблона
  * Файл можно доставить через MEDIA: путь

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Доступные шаблоны](<#available-templates>)
    * [Курируемые шаблоны (пользовательское размещение текста)](<#curated-templates-custom-text-placement>)
    * [Динамические шаблоны (из imgflip API)](<#dynamic-templates-from-imgflip-api>)
  * [Процедура](<#procedure>)
    * [Режим 1: Классический шаблон (по умолчанию)](<#mode-1-classic-template-default>)
    * [Режим 2: Пользовательское AI-изображение (когда доступен image_generate)](<#mode-2-custom-ai-image-when-image_generate-is-available>)
  * [Примеры](<#examples>)
  * [Список шаблонов](<#listing-templates>)
  * [Ошибки и советы](<#pitfalls>)
  * [Проверка результата](<#verification>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-meme-generation -->
