On this page
Геокодирование, POI, маршруты, часовые пояса через OpenStreetMap/OSRM.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Skill metadata")
|   
|---|---  
|Источник| Встроенный (установлен по умолчанию)  
|Путь| `skills/productivity/maps`  
|Версия| `1.2.0`  
|Автор| Mibayy  
|Лицензия| MIT  
|Теги| `maps`, `geocoding`, `places`, `routing`, `distance`, `directions`, `nearby`, `location`, `openstreetmap`, `nominatim`, `overpass`, `osrm`  
## Справка: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# Навык «Карты»
Геолокационная аналитика с использованием бесплатных открытых источников данных. 8 команд, 44 категории POI, ноль зависимостей (только стандартная библиотека Python), не требуется API-ключ.
Источники данных: OpenStreetMap/Nominatim, Overpass API, OSRM, TimeAPI.io.
Этот навык заменяет старый навык `find-nearby` — весь функционал find-nearby покрыт командой `nearby` ниже, с тем же сокращением `--near "<место>"` и поддержкой нескольких категорий.
## Когда использовать[​](<#when-to-use> "Прямая ссылка на When to Use")
  * Пользователь отправляет геометку в Telegram (широта/долгота в сообщении) → `nearby`
  * Пользователь хочет получить координаты по названию места → `search`
  * У пользователя есть координаты, и он хочет узнать адрес → `reverse`
  * Пользователь спрашивает о ближайших ресторанах, больницах, аптеках, отелях и т.д. → `nearby`
  * Пользователь хочет узнать расстояние или время в пути на машине/пешком/велосипеде → `distance`
  * Пользователь хочет получить пошаговые инструкции между двумя точками → `directions`
  * Пользователь хочет узнать часовой пояс для местоположения → `timezone`
  * Пользователь хочет найти POI в пределах географической области → `area` \+ `bbox`


## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Prerequisites")
Python 3.8+ (только стандартная библиотека — установка через pip не требуется).
Путь к скрипту: `~/.hermes/skills/maps/scripts/maps_client.py`
## Команды[​](<#commands> "Прямая ссылка на Commands")
[code] 
    MAPS=~/.hermes/skills/maps/scripts/maps_client.py  
    
[/code]
### search — Геокодирование названия места[​](<#search--geocode-a-place-name> "Прямая ссылка на search — Geocode a place name")
[code] 
    python3 $MAPS search "Eiffel Tower"  
    python3 $MAPS search "1600 Pennsylvania Ave, Washington DC"  
    
[/code]
Возвращает: широту, долготу, отображаемое название, тип, ограничивающий прямоугольник, оценку важности.
### reverse — Координаты в адрес[​](<#reverse--coordinates-to-address> "Прямая ссылка на reverse — Coordinates to address")
[code] 
    python3 $MAPS reverse 48.8584 2.2945  
    
[/code]
Возвращает: полный адрес с разбивкой (улица, город, штат, страна, почтовый индекс).
### nearby — Поиск мест по категории[​](<#nearby--find-places-by-category> "Прямая ссылка на nearby — Find places by category")
[code] 
    # By coordinates (from a Telegram location pin, for example)  
    python3 $MAPS nearby 48.8584 2.2945 restaurant --limit 10  
    python3 $MAPS nearby 40.7128 -74.0060 hospital --radius 2000  
      
    # By address / city / zip / landmark — --near auto-geocodes  
    python3 $MAPS nearby --near "Times Square, New York" --category cafe  
    python3 $MAPS nearby --near "90210" --category pharmacy  
      
    # Multiple categories merged into one query  
    python3 $MAPS nearby --near "downtown austin" --category restaurant --category bar --limit 10  
    
[/code]
46 категорий: restaurant, cafe, bar, hospital, pharmacy, hotel, guest_house, camp_site, supermarket, atm, gas_station, parking, museum, park, school, university, bank, police, fire_station, library, airport, train_station, bus_stop, church, mosque, synagogue, dentist, doctor, cinema, theatre, gym, swimming_pool, post_office, convenience_store, bakery, bookshop, laundry, car_wash, car_rental, bicycle_rental, taxi, veterinary, zoo, playground, stadium, nightclub.
Каждый результат включает: `name`, `address`, `lat`/`lon`, `distance_m`, `maps_url` (кликабельная ссылка Google Maps), `directions_url` (маршруты Google Maps от точки поиска), а также продвигаемые теги при наличии — `cuisine`, `hours` (часы работы), `phone`, `website`.
### distance — Расстояние и время в пути[​](<#distance--travel-distance-and-time> "Прямая ссылка на distance — Travel distance and time")
[code] 
    python3 $MAPS distance "Paris" --to "Lyon"  
    python3 $MAPS distance "New York" --to "Boston" --mode driving  
    python3 $MAPS distance "Big Ben" --to "Tower Bridge" --mode walking  
    
[/code]
Режимы: driving (по умолчанию), walking, cycling. Возвращает расстояние по дороге, продолжительность и расстояние по прямой для сравнения.
### directions — Пошаговая навигация[​](<#directions--turn-by-turn-navigation> "Прямая ссылка на directions — Turn-by-turn navigation")
[code] 
    python3 $MAPS directions "Eiffel Tower" --to "Louvre Museum" --mode walking  
    python3 $MAPS directions "JFK Airport" --to "Times Square" --mode driving  
    
[/code]
Возвращает пронумерованные шаги с инструкцией, расстоянием, продолжительностью, названием дороги и типом манёвра (поворот, отправление, прибытие и т.д.).
### timezone — Часовой пояс по координатам[​](<#timezone--timezone-for-coordinates> "Прямая ссылка на timezone — Timezone for coordinates")
[code] 
    python3 $MAPS timezone 48.8584 2.2945  
    python3 $MAPS timezone 35.6762 139.6503  
    
[/code]
Возвращает название часового пояса, смещение UTC и текущее местное время.
### area — Ограничивающий прямоугольник и площадь места[​](<#area--bounding-box-and-area-for-a-place> "Прямая ссылка на area — Bounding box and area for a place")
[code] 
    python3 $MAPS area "Manhattan, New York"  
    python3 $MAPS area "London"  
    
[/code]
Возвращает координаты ограничивающего прямоугольника, ширину/высоту в км и примерную площадь. Полезно как входные данные для команды bbox.
### bbox — Поиск внутри ограничивающего прямоугольника[​](<#bbox--search-within-a-bounding-box> "Прямая ссылка на bbox — Search within a bounding box")
[code] 
    python3 $MAPS bbox 40.75 -74.00 40.77 -73.98 restaurant --limit 20  
    
[/code]
Находит POI внутри географического прямоугольника. Используйте `area` сначала, чтобы получить координаты ограничивающего прямоугольника для именованного места.
## Работа с геометками Telegram[​](<#working-with-telegram-location-pins> "Прямая ссылка на Working With Telegram Location Pins")
Когда пользователь отправляет геометку, сообщение содержит поля `latitude:` и `longitude:`. Извлеките их и передайте напрямую в `nearby`:
[code] 
    # User sent a pin at 36.17, -115.14 and asked "find cafes nearby"  
    python3 $MAPS nearby 36.17 -115.14 cafe --radius 1500  
    
[/code]
Представляйте результаты в виде нумерованного списка с названиями, расстояниями и полем `maps_url`, чтобы пользователь получил кликабельную ссылку в чате. Для вопросов «работает ли сейчас?» проверяйте поле `hours`; если оно отсутствует или неясно, уточните через `web_search`, так как часы работы в OSM поддерживаются сообществом и не всегда актуальны.
## Примеры рабочих процессов[​](<#workflow-examples> "Прямая ссылка на Workflow Examples")
**«Найди итальянские рестораны рядом с Колизеем»:**
  1. `nearby --near "Colosseum Rome" --category restaurant --radius 500` — одна команда, автоматическое геокодирование


**«Что рядом с этой геометкой, которую они отправили?»:**
  1. Извлеките широту/долготу из сообщения Telegram
  2. `nearby LAT LON cafe --radius 1500`


**«Как мне пройти пешком от отеля до конференц-центра?»:**
  1. `directions "Hotel Name" --to "Conference Center" --mode walking`


**«Какие рестораны есть в центре Сиэтла?»:**
  1. `area "Downtown Seattle"` → получить ограничивающий прямоугольник
  2. `bbox S W N E restaurant --limit 30`


## Проблемные моменты[​](<#pitfalls> "Прямая ссылка на Pitfalls")
  * Условия использования Nominatim: максимум 1 запрос/с (обрабатывается автоматически скриптом)
  * `nearby` требует широту/долготу ИЛИ `--near "<адрес>"` — необходимо одно из двух
  * Покрытие маршрутов OSRM лучше всего в Европе и Северной Америке
  * Overpass API может быть медленным в часы пик; скрипт автоматически переключается между зеркалами (overpass-api.de → overpass.kumi.systems)
  * `distance` и `directions` используют флаг `--to` для указания пункта назначения (не позиционный аргумент)
  * Если один почтовый индекс даёт неоднозначные результаты по всему миру, укажите страну/штат


## Проверка[​](<#verification> "Прямая ссылка на Verification")
[code] 
    python3 ~/.hermes/skills/maps/scripts/maps_client.py search "Statue of Liberty"  
    # Should return lat ~40.689, lon ~-74.044  
      
    python3 ~/.hermes/skills/maps/scripts/maps_client.py nearby --near "Times Square" --category restaurant --limit 3  
    # Should return a list of restaurants within ~500m of Times Square  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справка: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Предварительные требования](<#prerequisites>)
  * [Команды](<#commands>)
    * [search — Геокодирование названия места](<#search--geocode-a-place-name>)
    * [reverse — Координаты в адрес](<#reverse--coordinates-to-address>)
    * [nearby — Поиск мест по категории](<#nearby--find-places-by-category>)
    * [distance — Расстояние и время в пути](<#distance--travel-distance-and-time>)
    * [directions — Пошаговая навигация](<#directions--turn-by-turn-navigation>)
    * [timezone — Часовой пояс по координатам](<#timezone--timezone-for-coordinates>)
    * [area — Ограничивающий прямоугольник и площадь места](<#area--bounding-box-and-area-for-a-place>)
    * [bbox — Поиск внутри ограничивающего прямоугольника](<#bbox--search-within-a-bounding-box>)
  * [Работа с геометками Telegram](<#working-with-telegram-location-pins>)
  * [Примеры рабочих процессов](<#workflow-examples>)
  * [Проблемные моменты](<#pitfalls>)
  * [Проверка](<#verification>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-maps -->
