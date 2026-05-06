На этой странице
ASCII-арт: pyfiglet, cowsay, boxes, image-to-ascii.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/creative/ascii-art` |
|Версия| `4.0.0` |
|Автор| 0xbyt4, Hermes Agent |
|Лицензия| MIT |
|Теги| `ASCII`, `Art`, `Banners`, `Creative`, `Unicode`, `Text-Art`, `pyfiglet`, `figlet`, `cowsay`, `boxes` |
|Связанные навыки| [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>) |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# Навык ASCII Art

Несколько инструментов для различных нужд ASCII-арта. Все инструменты — локальные CLI-программы или бесплатные REST API — никаких ключей API не требуется.

## Инструмент 1: Текстовые баннеры (pyfiglet — локально)[​](<#tool-1-text-banners-pyfiglet--local> "Прямая ссылка на Инструмент 1: Текстовые баннеры (pyfiglet — локально)")

Преобразует текст в крупные ASCII-баннеры. 571 встроенный шрифт.

### Установка[​](<#setup> "Прямая ссылка на Установка")

```bash
pip install pyfiglet --break-system-packages -q
```

### Использование[​](<#usage> "Прямая ссылка на Использование")

```bash
python3 -m pyfiglet "YOUR TEXT" -f slant
python3 -m pyfiglet "TEXT" -f doom -w 80    # Задать ширину
python3 -m pyfiglet --list_fonts             # Список всех 571 шрифтов
```

### Рекомендуемые шрифты[​](<#recommended-fonts> "Прямая ссылка на Рекомендуемые шрифты")

|Стиль| Шрифт| Для чего лучше всего|
|---|---|---|
|Чистый и современный| `slant`| Названия проектов, заголовки|
|Жирный и блочный| `doom`| Титулы, логотипы|
|Крупный и читаемый| `big`| Баннеры|
|Классический баннер| `banner3`| Широкие экраны|
|Компактный| `small`| Подзаголовки|
|Киберпанк| `cyberlarge`| Тематика технологий|
|3D-эффект| `3-d`| Заставки|
|Готический| `gothic`| Драматический текст|

### Советы[​](<#tips> "Прямая ссылка на Советы")

* Предложите 2-3 шрифта на выбор, чтобы пользователь выбрал понравившийся
* Короткий текст (1-8 символов) лучше всего смотрится с детализированными шрифтами, такими как `doom` или `block`
* Длинный текст лучше работает с компактными шрифтами, такими как `small` или `mini`

## Инструмент 2: Текстовые баннеры (asciified API — удалённо, без установки)[​](<#tool-2-text-banners-asciified-api--remote-no-install> "Прямая ссылка на Инструмент 2: Текстовые баннеры (asciified API — удалённо, без установки)")

Бесплатный REST API, преобразующий текст в ASCII-арт. 250+ FIGlet-шрифтов. Возвращает обычный текст напрямую — не требует парсинга. Используйте это, когда pyfiglet не установлен, или как быструю альтернативу.

### Использование (через curl в терминале)[​](<#usage-via-terminal-curl> "Прямая ссылка на Использование (через curl в терминале)")

```bash
# Базовый текстовый баннер (шрифт по умолчанию)
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello+World"
  
# С определённым шрифтом
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Doom"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Star+Wars"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=3-D"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Banner3"
  
# Список всех доступных шрифтов (возвращает JSON-массив)
curl -s "https://asciified.thelicato.io/api/v2/fonts"
```

### Советы[​](<#tips-1> "Прямая ссылка на Советы")

* URL-кодируйте пробелы как `+` в параметре text
* Ответ представляет собой обычный текст ASCII-арта — без JSON-обёртки, готов к отображению
* Названия шрифтов чувствительны к регистру; используйте endpoint fonts для получения точных названий
* Работает из любого терминала с curl — не требует Python или pip

## Инструмент 3: Cowsay (Искусство сообщений)[​](<#tool-3-cowsay-message-art> "Прямая ссылка на Инструмент 3: Cowsay (Искусство сообщений)")

Классический инструмент, оборачивающий текст в речевой пузырь с ASCII-персонажем.

### Установка[​](<#setup-1> "Прямая ссылка на Установка")

```bash
sudo apt install cowsay -y    # Debian/Ubuntu
# brew install cowsay         # macOS
```

### Использование[​](<#usage-1> "Прямая ссылка на Использование")

```bash
cowsay "Hello World"
cowsay -f tux "Linux rules"       # Пингвин Tux
cowsay -f dragon "Rawr!"          # Дракон
cowsay -f stegosaurus "Roar!"     # Стегозавр
cowthink "Hmm..."                  # Пузырь с мыслями
cowsay -l                          # Список всех персонажей
```

### Доступные персонажи (50+)[​](<#available-characters-50> "Прямая ссылка на Доступные персонажи (50+)")

`beavis.zen`, `bong`, `bunny`, `cheese`, `daemon`, `default`, `dragon`, `dragon-and-cow`, `elephant`, `eyes`, `flaming-skull`, `ghostbusters`, `hellokitty`, `kiss`, `kitty`, `koala`, `luke-koala`, `mech-and-cow`, `meow`, `moofasa`, `moose`, `ren`, `sheep`, `skeleton`, `small`, `stegosaurus`, `stimpy`, `supermilker`, `surgery`, `three-eyes`, `turkey`, `turtle`, `tux`, `udder`, `vader`, `vader-koala`, `www`

### Модификаторы глаз/языка[​](<#eyetongue-modifiers> "Прямая ссылка на Модификаторы глаз/языка")

```bash
cowsay -b "Borg"       # =_= глаза
cowsay -d "Dead"       # x_x глаза
cowsay -g "Greedy"     # $_$ глаза
cowsay -p "Paranoid"   # @_@ глаза
cowsay -s "Stoned"     # *_* глаза
cowsay -w "Wired"      # O_O глаза
cowsay -e "OO" "Msg"   # Пользовательские глаза
cowsay -T "U " "Msg"   # Пользовательский язык
```

## Инструмент 4: Boxes (Декоративные рамки)[​](<#tool-4-boxes-decorative-borders> "Прямая ссылка на Инструмент 4: Boxes (Декоративные рамки)")

Рисует декоративные ASCII-рамки/границы вокруг любого текста. 70+ встроенных дизайнов.

### Установка[​](<#setup-2> "Прямая ссылка на Установка")

```bash
sudo apt install boxes -y    # Debian/Ubuntu
# brew install boxes         # macOS
```

### Использование[​](<#usage-2> "Прямая ссылка на Использование")

```bash
echo "Hello World" | boxes                    # Рамка по умолчанию
echo "Hello World" | boxes -d stone           # Каменная рамка
echo "Hello World" | boxes -d parchment       # Свиток из пергамента
echo "Hello World" | boxes -d cat             # Рамка с котиком
echo "Hello World" | boxes -d dog             # Рамка с собакой
echo "Hello World" | boxes -d unicornsay      # Единорог
echo "Hello World" | boxes -d diamonds        # Ромбовидный узор
echo "Hello World" | boxes -d c-cmt           # Комментарий в стиле C
echo "Hello World" | boxes -d html-cmt        # HTML-комментарий
echo "Hello World" | boxes -a c               # Центрировать текст
boxes -l                                       # Список всех 70+ дизайнов
```

### Комбинирование с pyfiglet или asciified[​](<#combine-with-pyfiglet-or-asciified> "Прямая ссылка на Комбинирование с pyfiglet или asciified")

```bash
python3 -m pyfiglet "HERMES" -f slant | boxes -d stone
# Или без установленного pyfiglet:
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=HERMES&font=Slant" | boxes -d stone
```

## Инструмент 5: TOIlet (Цветное текстовое искусство)[​](<#tool-5-toilet-colored-text-art> "Прямая ссылка на Инструмент 5: TOIlet (Цветное текстовое искусство)")

Как pyfiglet, но с ANSI-цветовыми эффектами и визуальными фильтрами. Отлично подходит для украшения терминала.

### Установка[​](<#setup-3> "Прямая ссылка на Установка")

```bash
sudo apt install toilet toilet-fonts -y    # Debian/Ubuntu
# brew install toilet                      # macOS
```

### Использование[​](<#usage-3> "Прямая ссылка на Использование")

```bash
toilet "Hello World"                    # Базовое текстовое искусство
toilet -f bigmono12 "Hello"            # Определённый шрифт
toilet --gay "Rainbow!"                 # Радужная раскраска
toilet --metal "Metal!"                 # Металлический эффект
toilet -F border "Bordered"             # Добавить рамку
toilet -F border --gay "Fancy!"         # Комбинированные эффекты
toilet -f pagga "Block"                 # Блочный шрифт (уникальный для toilet)
toilet -F list                          # Список доступных фильтров
```

### Фильтры[​](<#filters> "Прямая ссылка на Фильтры")

`crop`, `gay` (радуга), `metal`, `flip`, `flop`, `180`, `left`, `right`, `border`

**Примечание**: toilet выводит ANSI-escape-последовательности для цветов — работает в терминалах, но может не отображаться во всех контекстах (например, в текстовых файлах, некоторых чат-платформах).

## Инструмент 6: Изображение в ASCII-арт[​](<#tool-6-image-to-ascii-art> "Прямая ссылка на Инструмент 6: Изображение в ASCII-арт")

Конвертирует изображения (PNG, JPEG, GIF, WEBP) в ASCII-арт.

### Вариант A: ascii-image-converter (рекомендуемый, современный)[​](<#option-a-ascii-image-converter-recommended-modern> "Прямая ссылка на Вариант A: ascii-image-converter (рекомендуемый, современный)")

```bash
# Установка
sudo snap install ascii-image-converter
# ИЛИ: go install github.com/TheZoraiz/ascii-image-converter@latest
```

```bash
ascii-image-converter image.png                  # Базовое
ascii-image-converter image.png -C               # Цветной вывод
ascii-image-converter image.png -d 60,30         # Задать размеры
ascii-image-converter image.png -b               # Шрифт Брайля
ascii-image-converter image.png -n               # Негатив/инверсия
ascii-image-converter https://url/image.jpg      # Прямой URL
ascii-image-converter image.png --save-txt out   # Сохранить как текст
```

### Вариант B: jp2a (лёгкий, только JPEG)[​](<#option-b-jp2a-lightweight-jpeg-only> "Прямая ссылка на Вариант B: jp2a (лёгкий, только JPEG)")

```bash
sudo apt install jp2a -y
jp2a --width=80 image.jpg
jp2a --colors image.jpg              # Цветной
```

## Инструмент 7: Поиск готового ASCII-арта[​](<#tool-7-search-pre-made-ascii-art> "Прямая ссылка на Инструмент 7: Поиск готового ASCII-арта")

Ищите готовый ASCII-арт из интернета. Используйте `terminal` с `curl`.

### Источник A: ascii.co.uk (рекомендуется для готового арта)[​](<#source-a-asciicouk-recommended-for-pre-made-art> "Прямая ссылка на Источник A: ascii.co.uk (рекомендуется для готового арта)")

Большая коллекция классического ASCII-арта, организованная по темам. Арт находится внутри HTML-тегов `<pre>`. Получите страницу через curl, затем извлеките арт с помощью небольшого Python-скрипта.

**Шаблон URL:** `https://ascii.co.uk/art/{subject}`

**Шаг 1 — Получить страницу:**

```bash
curl -s 'https://ascii.co.uk/art/cat' -o /tmp/ascii_art.html
```

**Шаг 2 — Извлечь арт из тегов pre:**

```python
import re, html
with open('/tmp/ascii_art.html') as f:
    text = f.read()
arts = re.findall(r'<pre[^>]*>(.*?)</pre>', text, re.DOTALL)
for art in arts:
    clean = re.sub(r'<[^>]+>', '', art)
    clean = html.unescape(clean).strip()
    if len(clean) > 30:
        print(clean)
        print('\n---\n')
```

**Доступные темы** (используйте как путь в URL):
* Животные: `cat`, `dog`, `horse`, `bird`, `fish`, `dragon`, `snake`, `rabbit`, `elephant`, `dolphin`, `butterfly`, `owl`, `wolf`, `bear`, `penguin`, `turtle`
* Объекты: `car`, `ship`, `airplane`, `rocket`, `guitar`, `computer`, `coffee`, `beer`, `cake`, `house`, `castle`, `sword`, `crown`, `key`
* Природа: `tree`, `flower`, `sun`, `moon`, `star`, `mountain`, `ocean`, `rainbow`
* Персонажи: `skull`, `robot`, `angel`, `wizard`, `pirate`, `ninja`, `alien`
* Праздники: `christmas`, `halloween`, `valentine`

**Советы:**
* Сохраняйте подписи/инициалы художников — важный этикет
* На каждой странице может быть несколько произведений — выбирайте лучшее для пользователя
* Надёжно работает через curl, JavaScript не требуется

### Источник B: GitHub Octocat API (забавное пасхальное яйцо)[​](<#source-b-github-octocat-api-fun-easter-egg> "Прямая ссылка на Источник B: GitHub Octocat API (забавное пасхальное яйцо)")

Возвращает случайного GitHub Octocat с мудрой цитатой. Авторизация не требуется.

```bash
curl -s https://api.github.com/octocat
```

## Инструмент 8: Забавные ASCII-утилиты (через curl)[​](<#tool-8-fun-ascii-utilities-via-curl> "Прямая ссылка на Инструмент 8: Забавные ASCII-утилиты (через curl)")

Эти бесплатные сервисы возвращают ASCII-арт напрямую — отлично подходят для дополнительного развлечения.

### QR-коды в виде ASCII-арта[​](<#qr-codes-as-ascii-art> "Прямая ссылка на QR-коды в виде ASCII-арта")

```bash
curl -s "qrenco.de/Hello+World"
curl -s "qrenco.de/https://example.com"
```

### Погода в виде ASCII-арта[​](<#weather-as-ascii-art> "Прямая ссылка на Погода в виде ASCII-арта")

```bash
curl -s "wttr.in/London"          # Полный прогноз погоды с ASCII-графикой
curl -s "wttr.in/Moon"            # Фаза луны в ASCII-арте
curl -s "v2.wttr.in/London"       # Детальная версия
```

## Инструмент 9: Пользовательский арт от LLM (запасной вариант)[​](<#tool-9-llm-generated-custom-art-fallback> "Прямая ссылка на Инструмент 9: Пользовательский арт от LLM (запасной вариант)")

Когда инструменты выше не имеют нужного, генерируйте ASCII-арт напрямую, используя эти Unicode-символы:

### Палитра символов[​](<#character-palette> "Прямая ссылка на Палитра символов")

**Box Drawing:** `╔ ╗ ╚ ╝ ║ ═ ╠ ╣ ╦ ╩ ╬ ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╰ ╯`
**Block Elements:** `░ ▒ ▓ █ ▄ ▀ ▌ ▐ ▖ ▗ ▘ ▝ ▚ ▞`
**Geometric & Symbols:** `◆ ◇ ◈ ● ○ ◉ ■ □ ▲ △ ▼ ▽ ★ ☆ ✦ ✧ ◀ ▶ ◁ ▷ ⬡ ⬢ ⌂`

### Правила[​](<#rules> "Прямая ссылка на Правила")

* Максимальная ширина: 60 символов на строку (безопасно для терминала)
* Максимальная высота: 15 строк для баннеров, 25 для сцен
* Только моноширинный: вывод должен корректно отображаться в шрифтах фиксированной ширины

## Схема принятия решений[​](<#decision-flow> "Прямая ссылка на Схема принятия решений")

1. **Текст как баннер** → pyfiglet, если установлен, иначе asciified API через curl
2. **Оборачивание сообщения в забавный персонаж** → cowsay
3. **Добавление декоративной рамки/границы** → boxes (можно комбинировать с pyfiglet/asciified)
4. **Арт определённой вещи** (котик, ракета, дракон) → ascii.co.uk через curl + парсинг
5. **Конвертация изображения в ASCII** → ascii-image-converter или jp2a
6. **QR-код** → qrenco.de через curl
7. **Погода/луна** → wttr.in через curl
8. **Что-то нестандартное/креативное** → генерация LLM с Unicode-палитрой
9. **Любой инструмент не установлен** → установить его, или перейти к следующему варианту

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Инструмент 1: Текстовые баннеры (pyfiglet — локально)](<#tool-1-text-banners-pyfiglet--local>)
  * [Установка](<#setup>)
  * [Использование](<#usage>)
  * [Рекомендуемые шрифты](<#recommended-fonts>)
  * [Советы](<#tips>)
* [Инструмент 2: Текстовые баннеры (asciified API — удалённо, без установки)](<#tool-2-text-banners-asciified-api--remote-no-install>)
  * [Использование (через curl в терминале)](<#usage-via-terminal-curl>)
  * [Советы](<#tips-1>)
* [Инструмент 3: Cowsay (Искусство сообщений)](<#tool-3-cowsay-message-art>)
  * [Установка](<#setup-1>)
  * [Использование](<#usage-1>)
  * [Доступные персонажи (50+)](<#available-characters-50>)
  * [Модификаторы глаз/языка](<#eyetongue-modifiers>)
* [Инструмент 4: Boxes (Декоративные рамки)](<#tool-4-boxes-decorative-borders>)
  * [Установка](<#setup-2>)
  * [Использование](<#usage-2>)
  * [Комбинирование с pyfiglet или asciified](<#combine-with-pyfiglet-or-asciified>)
* [Инструмент 5: TOIlet (Цветное текстовое искусство)](<#tool-5-toilet-colored-text-art>)
  * [Установка](<#setup-3>)
  * [Использование](<#usage-3>)
  * [Фильтры](<#filters>)
* [Инструмент 6: Изображение в ASCII-арт](<#tool-6-image-to-ascii-art>)
  * [Вариант A: ascii-image-converter (рекомендуемый, современный)](<#option-a-ascii-image-converter-recommended-modern>)
  * [Вариант B: jp2a (лёгкий, только JPEG)](<#option-b-jp2a-lightweight-jpeg-only>)
* [Инструмент 7: Поиск готового ASCII-арта](<#tool-7-search-pre-made-ascii-art>)
  * [Источник A: ascii.co.uk (рекомендуется для готового арта)](<#source-a-asciicouk-recommended-for-pre-made-art>)
  * [Источник B: GitHub Octocat API (забавное пасхальное яйцо)](<#source-b-github-octocat-api-fun-easter-egg>)
* [Инструмент 8: Забавные ASCII-утилиты (через curl)](<#tool-8-fun-ascii-utilities-via-curl>)
  * [QR-коды в виде ASCII-арта](<#qr-codes-as-ascii-art>)
  * [Погода в виде ASCII-арта](<#weather-as-ascii-art>)
* [Инструмент 9: Пользовательский арт от LLM (запасной вариант)](<#tool-9-llm-generated-custom-art-fallback>)
  * [Палитра символов](<#character-palette>)
  * [Правила](<#rules>)
* [Схема принятия решений](<#decision-flow>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-ascii-art -->
