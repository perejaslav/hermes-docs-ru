On this page
Игра в Pokemon через headless-эмулятор с чтением RAM.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию)  |
|Путь| `skills/gaming/pokemon-player`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Pokemon Player
Игра в Pokemon через headless-эмуляцию с помощью пакета `pokemon-agent`.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь говорит «play pokemon», «start pokemon», «pokemon game»
  * Пользователь спрашивает о Pokemon Red, Blue, Yellow, FireRed и т.д.
  * Пользователь хочет посмотреть, как ИИ играет в Pokemon
  * Пользователь ссылается на ROM-файл (.gb, .gbc, .gba)


## Startup Procedure[​](<#startup-procedure> "Direct link to Startup Procedure")
### 1\\. First-time setup (clone, venv, install)[​](<#1-first-time-setup-clone-venv-install> "Direct link to 1. First-time setup (clone, venv, install)")
Репозиторий находится на GitHub: NousResearch/pokemon-agent. Склонируйте его, затем настройте виртуальное окружение Python 3.10+. Используйте uv (предпочтительно из-за скорости) для создания venv и установки пакета в режиме editable с расширением pyboy. Если uv недоступен, используйте python3 -m venv + pip.
На этой машине он уже настроен в /home/teknium/pokemon-agent с готовым venv — просто перейдите туда и выполните source .venv/bin/activate.
Вам также понадобится ROM-файл. Спросите его у пользователя. На этой машине один существует в roms/pokemon_red.gb внутри этой директории. НИКОГДА не загружайте и не предоставляйте ROM-файлы — всегда спрашивайте пользователя.
### 2\\. Start the game server[​](<#2-start-the-game-server> "Direct link to 2. Start the game server")
Из директории pokemon-agent с активированным venv запустите pokemon-agent serve с --rom, указывающим на ROM, и --port 9876. Запустите в фоне с &. Чтобы продолжить сохранённую игру, добавьте --load-state с именем сохранения. Подождите 4 секунды для запуска, затем проверьте с помощью GET /health.
### 3\\. Set up live dashboard for user to watch[​](<#3-set-up-live-dashboard-for-user-to-watch> "Direct link to 3. Set up live dashboard for user to watch")
Используйте обратный SSH-туннель через localhost.run, чтобы пользователь мог просматривать дашборд в своём браузере. Подключитесь через ssh, перенаправив локальный порт 9876 на удалённый порт 80 на [nokey@localhost.run](<mailto:nokey@localhost.run>). Перенаправьте вывод в лог-файл, подождите 10 секунд, затем найдите в логе URL с .lhr.life. Дайте пользователю URL с добавлением /dashboard/. URL туннеля меняется каждый раз — сообщайте пользователю новый при перезапуске.
## Save and Load[​](<#save-and-load> "Direct link to Save and Load")
### When to save[​](<#when-to-save> "Direct link to When to save")
  * Каждые 15-20 ходов игры
  * ВСЕГДА перед битвами с лидерами залов, встречами с соперником или рискованными боями
  * Перед входом в новый город или подземелье
  * Перед любым действием, в котором вы не уверены


### How to save[​](<#how-to-save> "Direct link to How to save")
POST /save с описательным именем. Хорошие примеры: before_brock, route1_start, mt_moon_entrance, got_cut
### How to load[​](<#how-to-load> "Direct link to How to load")
POST /load с именем сохранения.
### List available saves[​](<#list-available-saves> "Direct link to List available saves")
GET /saves возвращает все сохранённые состояния.
### Loading on server startup[​](<#loading-on-server-startup> "Direct link to Loading on server startup")
Используйте флаг --load-state при запуске сервера для автоматической загрузки сохранения. Это быстрее, чем загрузка через API после запуска.
## The Gameplay Loop[​](<#the-gameplay-loop> "Direct link to The Gameplay Loop")
### Step 1: OBSERVE — check state AND take a screenshot[​](<#step-1-observe--check-state-and-take-a-screenshot> "Direct link to Step 1: OBSERVE — check state AND take a screenshot")
GET /state для получения позиции, HP, статуса боя, диалога. GET /screenshot и сохраните в /tmp/pokemon.png, затем используйте vision_analyze. Всегда делайте ОБА — RAM-состояние даёт числа, vision даёт пространственное восприятие.
### Step 2: ORIENT[​](<#step-2-orient> "Direct link to Step 2: ORIENT")
  * Диалог/текст на экране → продвинуть его
  * В бою → сражаться или убежать
  * Отряд ранен → направиться в Pokemon Center
  * Рядом с целью → перемещаться осторожно


### Step 3: DECIDE[​](<#step-3-decide> "Direct link to Step 3: DECIDE")
Приоритет: диалог > бой > лечение > сюжетная цель > тренировка > исследование
### Step 4: ACT — move 2-4 steps max, then re-check[​](<#step-4-act--move-2-4-steps-max-then-re-check> "Direct link to Step 4: ACT — move 2-4 steps max, then re-check")
POST /action с КОРОТКИМ списком действий (2-4 действия, не 10-15).
### Step 5: VERIFY — screenshot after every move sequence[​](<#step-5-verify--screenshot-after-every-move-sequence> "Direct link to Step 5: VERIFY — screenshot after every move sequence")
Сделайте скриншот и используйте vision_analyze, чтобы подтвердить, что вы переместились туда, куда планировали. Это САМЫЙ ВАЖНЫЙ шаг. Без vision вы ОБЯЗАТЕЛЬНО заблудитесь.
### Step 6: RECORD progress to memory with PKM: prefix[​](<#step-6-record-progress-to-memory-with-pkm-prefix> "Direct link to Step 6: RECORD progress to memory with PKM: prefix")
### Step 7: SAVE periodically[​](<#step-7-save-periodically> "Direct link to Step 7: SAVE periodically")
## Action Reference[​](<#action-reference> "Direct link to Action Reference")
  * press_a — подтвердить, говорить, выбрать
  * press_b — отмена, закрыть меню
  * press_start — открыть игровое меню
  * walk_up/down/left/right — переместиться на одну клетку
  * hold_b_N — удерживать B в течение N кадров (используется для ускорения текста)
  * wait_60 — подождать около 1 секунды (60 кадров)
  * a_until_dialog_end — нажимать A, пока диалог не закончится


## Critical Tips from Experience[​](<#critical-tips-from-experience> "Direct link to Critical Tips from Experience")
### USE VISION CONSTANTLY[​](<#use-vision-constantly> "Direct link to USE VISION CONSTANTLY")
  * Делайте скриншот каждые 2-4 шага движения
  * RAM-состояние сообщает позицию и HP, но НЕ то, что вас окружает
  * Уступы, заборы, таблички, двери зданий, NPC — видны только на скриншоте
  * Задавайте модели vision конкретные вопросы: «что находится на одну клетку севернее меня?»
  * Когда застряли, всегда делайте скриншот перед попыткой случайных направлений


### Warp Transitions Need Extra Wait Time[​](<#warp-transitions-need-extra-wait-time> "Direct link to Warp Transitions Need Extra Wait Time")
При проходе через дверь или лестницу экран затемняется во время смены карты. Вы ОБЯЗАНЫ дождаться завершения. Добавляйте 2-3 действия wait_60 после любого прохода через дверь/лестницу. Без ожидания позиция будет устаревшей, и вы будете думать, что всё ещё находитесь на старой карте.
### Building Exit Trap[​](<#building-exit-trap> "Direct link to Building Exit Trap")
Когда вы выходите из здания, вы оказываетесь ПРЯМО ПЕРЕД дверью. Если пойти на север, вы снова войдёте внутрь. ВСЕГДА сначала делайте шаг в сторону, переместившись на 2 клетки влево или вправо, затем продолжайте движение в нужном направлении.
### Dialog Handling[​](<#dialog-handling> "Direct link to Dialog Handling")
В 1-м поколении текст прокручивается медленно, буква за буквой. Чтобы ускорить диалог, удерживайте B в течение 120 кадров, затем нажмите A. Повторяйте по необходимости. Удержание B заставляет текст отображаться на максимальной скорости. Затем нажмите A, чтобы перейти к следующей строке. Действие a_until_dialog_end проверяет флаг диалога в RAM, но этот флаг перехватывает НЕ ВСЕ текстовые состояния. Если диалог кажется зависшим, используйте ручной шаблон hold_b + press_a и проверяйте через скриншот.
### Ledges Are One-Way[​](<#ledges-are-one-way> "Direct link to Ledges Are One-Way")
Уступы (небольшие обрывы) можно только ПЕРЕПРЫГНУТЬ ВНИЗ (на юг), но НЕЛЬЗЯ забраться наверх (на север). Если путь на север заблокирован уступом, нужно обойти его слева или справа. Используйте vision, чтобы определить, с какой стороны проход. Спрашивайте модель vision явно.
### Navigation Strategy[​](<#navigation-strategy> "Direct link to Navigation Strategy")
  * Перемещайтесь по 2-4 шага за раз, затем делайте скриншот для проверки позиции
  * При входе в новую область сразу делайте скриншот для ориентации
  * Спрашивайте модель vision «в каком направлении [к цели]?»
  * Если застряли на 3+ попытки, сделайте скриншот и полностью переоцените ситуацию
  * Не выполняйте 10-15 действий подряд — вы проскочите цель или застрянете


### Running from Wild Battles[​](<#running-from-wild-battles> "Direct link to Running from Wild Battles")
В меню битвы RUN (БЕГСТВО) находится в правом нижнем углу. Чтобы добраться до него из позиции курсора по умолчанию (FIGHT, верхний левый угол): нажмите вниз, затем вправо, чтобы переместить курсор на RUN, затем нажмите A. Используйте hold_b для ускорения текста/анимаций.
### Battling (FIGHT)[​](<#battling-fight> "Direct link to Battling (FIGHT)")
В меню битвы FIGHT находится в верхнем левом углу (позиция курсора по умолчанию). Нажмите A для входа в выбор атаки, снова A для использования первой атаки. Затем удерживайте B для ускорения анимаций атак и текста.
## Battle Strategy[​](<#battle-strategy> "Direct link to Battle Strategy")
### Decision Tree[​](<#decision-tree> "Direct link to Decision Tree")
  1. Хотите поймать? → Ослабить, затем бросить Poke Ball
  2. Дикий, не нужен? → RUN (БЕЖАТЬ)
  3. Есть преимущество по типу? → Использовать суперэффективную атаку
  4. Нет преимущества? → Использовать сильнейшую STAB-атаку
  5. Мало HP? → Сменить покемона или использовать Potion


### Gen 1 Type Chart (key matchups)[​](<#gen-1-type-chart-key-matchups> "Direct link to Gen 1 Type Chart (key matchups)")
  * Water побеждает Fire, Ground, Rock
  * Fire побеждает Grass, Bug, Ice
  * Grass побеждает Water, Ground, Rock
  * Electric побеждает Water, Flying
  * Ground побеждает Fire, Electric, Rock, Poison
  * Psychic побеждает Fighting, Poison (доминирует в 1-м поколении!)


### Gen 1 Quirks[​](<#gen-1-quirks> "Direct link to Gen 1 Quirks")
  * Характеристика Special = одновременно атака И защита для специальных атак
  * Psychic-тип слишком силён (атаки Ghost багованы)
  * Критические удары зависят от характеристики Speed
  * Wrap/Bind не дают противнику действовать
  * Баг Focus Energy: УМЕНЬШАЕТ шанс крита вместо его повышения


## Memory Conventions[​](<#memory-conventions> "Direct link to Memory Conventions")
Префикс| Назначение| Пример  
|---|---|---  
PKM:OBJECTIVE| Текущая цель| Get Parcel from Viridian Mart  
PKM:MAP| Информация о навигации| Viridian: mart is northeast  
PKM:STRATEGY| Планы битв/команды| Need Grass type before Misty  
PKM:PROGRESS| Отслеживание этапов| Beat rival, heading to Viridian  
PKM:STUCK| Ситуации застревания| Ledge at y=28 go right to bypass  
PKM:TEAM| Заметки о команде| Squirtle Lv6, Tackle + Tail Whip  
## Progression Milestones[​](<#progression-milestones> "Direct link to Progression Milestones")
  * Выбор стартового покемона
  * Доставка посылки из Viridian Mart, получение Pokedex
  * Boulder Badge — Брок (Rock) → использовать Water/Grass
  * Cascade Badge — Мисти (Water) → использовать Grass/Electric
  * Thunder Badge — Лейтенант Сёрдж (Electric) → использовать Ground
  * Rainbow Badge — Эрика (Grass) → использовать Fire/Ice/Flying
  * Soul Badge — Кога (Poison) → использовать Ground/Psychic
  * Marsh Badge — Сабрина (Psychic) → сложнейший зал
  * Volcano Badge — Блейн (Fire) → использовать Water/Ground
  * Earth Badge — Джованни (Ground) → использовать Water/Grass/Ice
  * Elite Four → Чемпион!


## Stopping Play[​](<#stopping-play> "Direct link to Stopping Play")
  1. Сохраните игру с описательным именем через POST /save
  2. Обновите память с PKM:PROGRESS
  3. Сообщите пользователю: «Игра сохранена как [имя]! Скажите 'play pokemon', чтобы продолжить.»
  4. Завершите процессы сервера и туннеля


## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * НИКОГДА не загружайте и не предоставляйте ROM-файлы
  * Не отправляйте более 4-5 действий без проверки через vision
  * Всегда делайте шаг в сторону после выхода из зданий перед движением на север
  * Всегда добавляйте wait_60 x2-3 после прохода через двери/лестницы
  * Обнаружение диалога через RAM ненадёжно — проверяйте скриншотами
  * Сохраняйтесь ПЕРЕД рискованными встречами
  * URL туннеля меняется каждый раз при перезапуске


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Startup Procedure](<#startup-procedure>)
    * [1\\. First-time setup (clone, venv, install)](<#1-first-time-setup-clone-venv-install>)
    * [2\\. Start the game server](<#2-start-the-game-server>)
    * [3\\. Set up live dashboard for user to watch](<#3-set-up-live-dashboard-for-user-to-watch>)
  * [Save and Load](<#save-and-load>)
    * [When to save](<#when-to-save>)
    * [How to save](<#how-to-save>)
    * [How to load](<#how-to-load>)
    * [List available saves](<#list-available-saves>)
    * [Loading on server startup](<#loading-on-server-startup>)
  * [The Gameplay Loop](<#the-gameplay-loop>)
    * [Step 1: OBSERVE — check state AND take a screenshot](<#step-1-observe--check-state-and-take-a-screenshot>)
    * [Step 2: ORIENT](<#step-2-orient>)
    * [Step 3: DECIDE](<#step-3-decide>)
    * [Step 4: ACT — move 2-4 steps max, then re-check](<#step-4-act--move-2-4-steps-max-then-re-check>)
    * [Step 5: VERIFY — screenshot after every move sequence](<#step-5-verify--screenshot-after-every-move-sequence>)
    * [Step 6: RECORD progress to memory with PKM: prefix](<#step-6-record-progress-to-memory-with-pkm-prefix>)
    * [Step 7: SAVE periodically](<#step-7-save-periodically>)
  * [Action Reference](<#action-reference>)
  * [Critical Tips from Experience](<#critical-tips-from-experience>)
    * [USE VISION CONSTANTLY](<#use-vision-constantly>)
    * [Warp Transitions Need Extra Wait Time](<#warp-transitions-need-extra-wait-time>)
    * [Building Exit Trap](<#building-exit-trap>)
    * [Dialog Handling](<#dialog-handling>)
    * [Ledges Are One-Way](<#ledges-are-one-way>)
    * [Navigation Strategy](<#navigation-strategy>)
    * [Running from Wild Battles](<#running-from-wild-battles>)
    * [Battling (FIGHT)](<#battling-fight>)
  * [Battle Strategy](<#battle-strategy>)
    * [Decision Tree](<#decision-tree>)
    * [Gen 1 Type Chart (key matchups)](<#gen-1-type-chart-key-matchups>)
    * [Gen 1 Quirks](<#gen-1-quirks>)
  * [Memory Conventions](<#memory-conventions>)
  * [Progression Milestones](<#progression-milestones>)
  * [Stopping Play](<#stopping-play>)
  * [Pitfalls](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/gaming/gaming-pokemon-player -->
