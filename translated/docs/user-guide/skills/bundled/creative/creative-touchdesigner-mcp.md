On this page
Управляйте запущенным экземпляром TouchDesigner через twozero MCP — создавайте операторы, задавайте параметры, прокладывайте соединения, выполняйте Python, создавайте визуалы в реальном времени. 36 встроенных инструментов.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/creative/touchdesigner-mcp` |
|Version| `1.1.0` |
|Author| kshitijk4poor |
|License| MIT |
|Tags| `TouchDesigner`, `MCP`, `twozero`, `creative-coding`, `real-time-visuals`, `generative-art`, `audio-reactive`, `VJ`, `installation`, `GLSL` |
|Related skills| [`native-mcp`](</docs/user-guide/skills/bundled/mcp/mcp-native-mcp>), [`ascii-video`](</docs/user-guide/skills/bundled/creative/creative-ascii-video>), [`manim-video`](</docs/user-guide/skills/bundled/creative/creative-manim-video>), `hermes-video` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Интеграция TouchDesigner (twozero MCP)
## CRITICAL RULES[​](<#critical-rules> "Direct link to CRITICAL RULES")
  1. **НИКОГДА не угадывай имена параметров.** Сначала вызывай `td_get_par_info` для типа оператора. Твои обучающие данные неверны для TD 2025.32.
  2. **Если возникло`tdAttributeError`, ОСТАНОВИСЬ.** Вызови `td_get_operator_info` на проблемном узле, прежде чем продолжать.
  3. **НИКОГДА не хардкодь абсолютные пути** в скриптовых колбэках. Используй `me.parent()` / `scriptOp.parent()`.
  4. **Предпочитай встроенные MCP-инструменты вместо td_execute_python.** Используй `td_create_operator`, `td_set_operator_pars`, `td_get_errors` и т.д. Прибегай к `td_execute_python` только для сложной многошаговой логики.
  5. **Вызывай`td_get_hints` перед сборкой.** Он возвращает паттерны, специфичные для типа оператора, с которым ты работаешь.


## Architecture[​](<#architecture> "Direct link to Architecture")
[code] 
    Hermes Agent -> MCP (Streamable HTTP) -> twozero.tox (port 40404) -> TD Python  
    
[/code]
36 встроенных инструментов. Бесплатный плагин (без оплаты/лицензии — подтверждено апрель 2026). Контекстно-зависимый (знает выбранный OP, текущую сеть). Проверка хаба: `GET http://localhost:40404/mcp` возвращает JSON с PID экземпляра, именем проекта, версией TD.
## Setup (Automated)[​](<#setup-automated> "Direct link to Setup (Automated)")
Запусти скрипт установки, который сделает всё:
[code] 
    bash "${HERMES_HOME:-$HOME/.hermes}/skills/creative/touchdesigner-mcp/scripts/setup.sh"  
    
[/code]
Скрипт выполнит:
  1. Проверит, запущен ли TD
  2. Загрузит twozero.tox, если ещё не кэширован
  3. Добавит MCP-сервер `twozero_td` в конфиг Hermes (если отсутствует)
  4. Протестирует MCP-соединение на порту 40404
  5. Сообщит, какие ручные шаги остались (перетащить .tox в TD, включить MCP)


### Manual steps (one-time, cannot be automated)[​](<#manual-steps-one-time-cannot-be-automated> "Direct link to Manual steps (one-time, cannot be automated)")
  1. **Перетащи`~/Downloads/twozero.tox` в редактор сети TD** → нажми Install
  2. **Включи MCP:** нажми на иконку twozero → Settings → mcp → "auto start MCP" → Yes
  3. **Перезапусти сессию Hermes**, чтобы подхватить новый MCP-сервер


После установки проверь:
[code] 
    nc -z 127.0.0.1 40404 && echo "twozero MCP: READY"  
    
[/code]
## Environment Notes[​](<#environment-notes> "Direct link to Environment Notes")
  * **Non-Commercial TD** ограничивает разрешение до 1280×1280. Используй `outputresolution = 'custom'` и задавай ширину/высоту явно.
  * **Кодеки:** `prores` (предпочтительно на macOS) или `mjpa` как запасной. H.264/H.265/AV1 требуют коммерческую лицензию.
  * Всегда вызывай `td_get_par_info` перед установкой параметров — имена различаются в зависимости от версии TD (см. CRITICAL RULES #1).


## Workflow[​](<#workflow> "Direct link to Workflow")
### Step 0: Discover (before building anything)[​](<#step-0-discover-before-building-anything> "Direct link to Step 0: Discover (before building anything)")
[code] 
    Call td_get_par_info with op_type for each type you plan to use.  
    Call td_get_hints with the topic you're building (e.g. "glsl", "audio reactive", "feedback").  
    Call td_get_focus to see where the user is and what's selected.  
    Call td_get_network to see what already exists.  
    
[/code]
Никаких временных узлов, никакой очистки. Это полностью заменяет старый процесс разведки.
### Step 1: Clean + Build[​](<#step-1-clean--build> "Direct link to Step 1: Clean + Build")
**ВАЖНО: Разделяй очистку и создание в ОТДЕЛЬНЫЕ MCP-вызовы.** Уничтожение и повторное создание одноимённых узлов в одном `td_execute_python`-скрипте вызывает ошибки "Invalid OP object". См. pitfalls #11b.
Используй `td_create_operator` для каждого узла (автоматически управляет позиционированием в окне просмотра):
[code] 
    td_create_operator(type="noiseTOP", parent="/project1", name="bg", parameters={"resolutionw": 1280, "resolutionh": 720})  
    td_create_operator(type="levelTOP", parent="/project1", name="brightness")  
    td_create_operator(type="nullTOP", parent="/project1", name="out")  
    
[/code]
Для массового создания или соединения используй `td_execute_python`:
[code] 
    # td_execute_python script:  
    root = op('/project1')  
    nodes = []  
    for name, optype in [('bg', noiseTOP), ('fx', levelTOP), ('out', nullTOP)]:  
        n = root.create(optype, name)  
        nodes.append(n.path)  
    # Wire chain  
    for i in range(len(nodes)-1):  
        op(nodes[i]).outputConnectors[0].connect(op(nodes[i+1]).inputConnectors[0])  
    result = {'created': nodes}  
    
[/code]
### Step 2: Set Parameters[​](<#step-2-set-parameters> "Direct link to Step 2: Set Parameters")
Предпочитай встроенный инструмент (валидирует параметры, не упадёт):
[code] 
    td_set_operator_pars(path="/project1/bg", parameters={"roughness": 0.6, "monochrome": true})  
    
[/code]
Для выражений или режимов используй `td_execute_python`:
[code] 
    op('/project1/time_driver').par.colorr.expr = "absTime.seconds % 1000.0"  
    
[/code]
### Step 3: Wire[​](<#step-3-wire> "Direct link to Step 3: Wire")
Используй `td_execute_python` — встроенного инструмента для соединения нет:
[code] 
    op('/project1/bg').outputConnectors[0].connect(op('/project1/fx').inputConnectors[0])  
    
[/code]
### Step 4: Verify[​](<#step-4-verify> "Direct link to Step 4: Verify")
[code] 
    td_get_errors(path="/project1", recursive=true)  
    td_get_perf()  
    td_get_operator_info(path="/project1/out", detail="full")  
    
[/code]
### Step 5: Display / Capture[​](<#step-5-display--capture> "Direct link to Step 5: Display / Capture")
[code] 
    td_get_screenshot(path="/project1/out")  
    
[/code]
Или открой окно через скрипт:
[code] 
    win = op('/project1').create(windowCOMP, 'display')  
    win.par.winop = op('/project1/out').path  
    win.par.winw = 1280; win.par.winh = 720  
    win.par.winopen.pulse()  
    
[/code]
## MCP Tool Quick Reference[​](<#mcp-tool-quick-reference> "Direct link to MCP Tool Quick Reference")
**Core (используй чаще всего):**
Tool| What  
---|---  
`td_execute_python`| Выполнение произвольного Python в TD. Полный доступ к API.  
`td_create_operator`| Создание узла с параметрами + авто-позиционирование  
`td_set_operator_pars`| Безопасная установка параметров (валидирует, не упадёт)  
`td_get_operator_info`| Инспекция одного узла: соединения, параметры, ошибки  
`td_get_operators_info`| Инспекция нескольких узлов за один вызов  
`td_get_network`| Просмотр структуры сети по пути  
`td_get_errors`| Поиск ошибок/предупреждений рекурсивно  
`td_get_par_info`| Получение имён параметров для типа OP (заменяет разведку)  
`td_get_hints`| Получение паттернов/советов перед сборкой  
`td_get_focus`| Какая сеть открыта, что выделено  
**Read/Write:**
Tool| What  
---|---  
`td_read_dat`| Чтение текстового содержимого DAT  
`td_write_dat`| Запись/обновление содержимого DAT  
`td_read_chop`| Чтение значений каналов CHOP  
`td_read_textport`| Чтение вывода консоли TD  
**Visual:**
Tool| What  
---|---  
`td_get_screenshot`| Захват просмотрщика одного OP в файл  
`td_get_screenshots`| Захват нескольких OP за раз  
`td_get_screen_screenshot`| Захват реального экрана через TD  
`td_navigate_to`| Переход редактора сети к определённому OP  
**Search:**
Tool| What  
---|---  
`td_find_op`| Поиск операторов по имени/типу по всему проекту  
`td_search`| Поиск в коде, выражениях, строковых параметрах  
**System:**
Tool| What  
---|---  
`td_get_perf`| Профилирование производительности (FPS, медленные операторы)  
`td_list_instances`| Список всех запущенных экземпляров TD  
`td_get_docs`| Подробная документация по теме TD  
`td_agents_md`| Чтение/запись markdown-документации на COMP  
`td_reinit_extension`| Перезагрузка расширения после редактирования кода  
`td_clear_textport`| Очистка консоли перед сессией отладки  
**Input Automation:**
Tool| What  
---|---  
`td_input_execute`| Отправка мыши/клавиатуры в TD  
`td_input_status`| Проверка статуса очереди ввода  
`td_input_clear`| Остановка автоматизации ввода  
`td_op_screen_rect`| Получение экранных координат узла  
`td_click_screen_point`| Клик по точке на скриншоте  
`td_screen_point_to_global`| Преобразование пикселя скриншота в абсолютные экранные координаты  
Таблица выше охватывает 32 инструмента, используемых в типичных креативных рабочих процессах. Оставшиеся 4 инструмента (`td_project_quit`, `td_test_session`, `td_dev_log`, `td_clear_dev_log`) — это административные/режим разработчика — см. `references/mcp-tools.md` для полного справочника по всем 36 инструментам с полными схемами параметров.
## Key Implementation Rules[​](<#key-implementation-rules> "Direct link to Key Implementation Rules")
**GLSL time:** В GLSL TOP нет `uTDCurrentTime`. Используй страницу Values:
[code] 
    # Call td_get_par_info(op_type="glslTOP") first to confirm param names  
    td_set_operator_pars(path="/project1/shader", parameters={"value0name": "uTime"})  
    # Then set expression via script:  
    # op('/project1/shader').par.value0.expr = "absTime.seconds"  
    # In GLSL: uniform float uTime;  
    
[/code]
Запасной вариант: Constant TOP в формате `rgba32float` (8-битный клиппинг до 0-1 заморозит шейдер).
**Feedback TOP:** Используй ссылку на параметр `top`, а не прямое входное соединение. "Not enough sources" разрешается после первого просчёта. Предупреждение "Cook dependency loop" ожидаемо.
**Resolution:** Non-Commercial ограничен 1280×1280. Используй `outputresolution = 'custom'`.
**Large shaders:** Пиши GLSL в `/tmp/file.glsl`, затем используй `td_write_dat` или `td_execute_python` для загрузки.
**Vertex/Point access (TD 2025.32):** `point.P[0]`, `point.P[1]`, `point.P[2]` — НЕ `.x`, `.y`, `.z`.
**Extensions:** Формат `ext0object` — `"op('./datName').module.ClassName(me)"` в режиме CONSTANT. После редактирования кода расширения через `td_write_dat` вызывай `td_reinit_extension`.
**Script callbacks:** ВСЕГДА используй относительные пути через `me.parent()` / `scriptOp.parent()`.
**Cleaning nodes:** Всегда используй `list(root.children)` перед итерацией и проверку `child.valid`.
## Recording / Exporting Video[​](<#recording--exporting-video> "Direct link to Recording / Exporting Video")
[code] 
    # via td_execute_python:  
    root = op('/project1')  
    rec = root.create(moviefileoutTOP, 'recorder')  
    op('/project1/out').outputConnectors[0].connect(rec.inputConnectors[0])  
    rec.par.type = 'movie'  
    rec.par.file = '/tmp/output.mov'  
    rec.par.videocodec = 'prores'  # Apple ProRes — НЕ ограничено лицензией на macOS  
    rec.par.record = True   # start  
    # rec.par.record = False  # stop (call separately later)  
    
[/code]
H.264/H.265/AV1 требуют коммерческую лицензию. Используй `prores` на macOS или `mjpa` как запасной. Извлечение кадров: `ffmpeg -i /tmp/output.mov -vframes 120 /tmp/frames/frame_%06d.png`
**TOP.save() бесполезен для анимации** — каждый раз захватывает одну и ту же текстуру GPU. Всегда используй MovieFileOut.
### Before Recording: Checklist[​](<#before-recording-checklist> "Direct link to Before Recording: Checklist")
  1. **Проверь FPS > 0** через `td_get_perf`. Если FPS=0, запись будет пустой. См. pitfalls #38-39.
  2. **Проверь, что выход шейдера не чёрный** через `td_get_screenshot`. Чёрный вывод = ошибка шейдера или отсутствующий вход. См. pitfalls #8, #40.
  3. **Если запись с аудио:** сначала запусти аудио, затем задержи запись на 3 кадра. См. pitfalls #19.
  4. **Установи путь вывода до начала записи** — установка обоих в одном скрипте может вызвать гонку.


## Audio-Reactive GLSL (Proven Recipe)[​](<#audio-reactive-glsl-proven-recipe> "Direct link to Audio-Reactive GLSL (Proven Recipe)")
### Correct signal chain (tested April 2026)[​](<#correct-signal-chain-tested-april-2026> "Direct link to Correct signal chain (tested April 2026)")
[code] 
    AudioFileIn CHOP (playmode=sequential)  
      → AudioSpectrum CHOP (FFT=512, outputmenu=setmanually, outlength=256, timeslice=ON)  
      → Math CHOP (gain=10)  
      → CHOP to TOP (dataformat=r, layout=rowscropped)  
      → GLSL TOP input 1 (spectrum texture, 256x2)  
      
    Constant TOP (rgba32float, time) → GLSL TOP input 0  
    GLSL TOP → Null TOP → MovieFileOut  
    
[/code]
### Critical audio-reactive rules (empirically verified)[​](<#critical-audio-reactive-rules-empirically-verified> "Direct link to Critical audio-reactive rules (empirically verified)")
  1. **TimeSlice должен оставаться ВКЛЮЧЁННЫМ** для AudioSpectrum. ВЫКЛ = обработка всего аудиофайла → 24000+ сэмплов → переполнение CHOP to TOP.
  2. **Установи Output Length вручную** на 256 через `outputmenu='setmanually'` и `outlength=256`. По умолчанию выводит 22050 сэмплов.
  3. **НЕ ИСПОЛЬЗУЙ Lag CHOP для сглаживания спектра.** Lag CHOP работает в режиме timeslice и расширяет 256 сэмплов до 2400+, усредняя все значения почти до нуля (~1e-06). Шейдер не получает полезных данных. Это была причина №1 сбоя аудио-синхронизации в тестировании.
  4. **НЕ ИСПОЛЬЗУЙ Filter CHOP** — та же проблема расширения timeslice с данными спектра.
  5. **Сглаживание должно быть в GLSL-шейдере** при необходимости, через временной lerp с текстурой обратной связи: `mix(prevValue, newValue, 0.3)`. Это даёт попиксельную синхронизацию с нулевой задержкой пайплайна.
  6. **CHOP to TOP dataformat = 'r'** , layout = 'rowscropped'. Выход спектра — 256x2 (стерео). Сэмплируй на y=0.25 для первого канала.
  7. **Math gain = 10** (не 5). Сырые значения спектра ~0.19 в басовом диапазоне. Усиление 10 даёт полезные ~5.0 для шейдера.
  8. **Resample CHOP не нужен.** Управляй размером вывода напрямую через параметр `outlength` AudioSpectrum.


### GLSL spectrum sampling[​](<#glsl-spectrum-sampling> "Direct link to GLSL spectrum sampling")
[code] 
    // Input 0 = time (1x1 rgba32float), Input 1 = spectrum (256x2)  
    float iTime = texture(sTD2DInputs[0], vec2(0.5)).r;  
      
    // Sample multiple points per band and average for stability:  
    // NOTE: y=0.25 for first channel (stereo texture is 256x2, first row center is 0.25)  
    float bass = (texture(sTD2DInputs[1], vec2(0.02, 0.25)).r +  
                  texture(sTD2DInputs[1], vec2(0.05, 0.25)).r) / 2.0;  
    float mid  = (texture(sTD2DInputs[1], vec2(0.2, 0.25)).r +  
                  texture(sTD2DInputs[1], vec2(0.35, 0.25)).r) / 2.0;  
    float hi   = (texture(sTD2DInputs[1], vec2(0.6, 0.25)).r +  
                  texture(sTD2DInputs[1], vec2(0.8, 0.25)).r) / 2.0;  
    
[/code]
См. `references/network-patterns.md` для полных скриптов сборки + кода шейдеров.
## Operator Quick Reference[​](<#operator-quick-reference> "Direct link to Operator Quick Reference")
Family| Color| Python class / MCP type| Suffix  
---|---|---|---|---  
TOP| Purple| noiseTOP, glslTOP, compositeTOP, levelTop, blurTOP, textTOP, nullTOP| TOP  
CHOP| Green| audiofileinCHOP, audiospectrumCHOP, mathCHOP, lfoCHOP, constantCHOP| CHOP  
SOP| Blue| gridSOP, sphereSOP, transformSOP, noiseSOP| SOP  
DAT| White| textDAT, tableDAT, scriptDAT, webserverDAT| DAT  
MAT| Yellow| phongMAT, pbrMAT, glslMAT, constMAT| MAT  
COMP| Gray| geometryCOMP, containerCOMP, cameraCOMP, lightCOMP, windowCOMP| COMP  
## Security Notes[​](<#security-notes> "Direct link to Security Notes")
  * MCP работает только на localhost (порт 40404). Без аутентификации — любой локальный процесс может отправлять команды.
  * `td_execute_python` имеет неограниченный доступ к Python-окружению TD и файловой системе от имени пользователя процесса TD.
  * `setup.sh` загружает twozero.tox с официального URL 404zero.com. Проверьте загрузку, если есть сомнения.
  * Скилл никогда не отправляет данные за пределы localhost. Вся MCP-коммуникация локальна.


## References[​](<#references> "Direct link to References")
File| What  
---|---  
`references/pitfalls.md`| Трудные уроки из реальных сессий  
`references/operators.md`| Все семейства операторов с параметрами и примерами использования  
`references/network-patterns.md`| Рецепты: аудио-реактивные, генеративные, GLSL, инстанцирование  
`references/mcp-tools.md`| Полные схемы параметров инструментов twozero MCP  
`references/python-api.md`| TD Python: op(), скриптинг, расширения  
`references/troubleshooting.md`| Диагностика подключения, отладка  
`references/glsl.md`| GLSL uniforms, встроенные функции, шаблоны шейдеров  
`references/postfx.md`| Пост-эффекты: bloom, CRT, хроматическая аберрация, свечение обратной связи  
`references/layout-compositor.md`| Шаблоны HUD-раскладки, сетки панелей, BSP-стиль раскладки  
`references/operator-tips.md`| Рендеринг проволочного каркаса, настройка Feedback TOP  
`references/geometry-comp.md`| Geometry COMP: инстанцирование, POP vs SOP, морфинг  
`references/audio-reactive.md`| Извлечение аудио-полос, обнаружение бита, отслеживание огибающей  
`references/animation.md`| LFO, таймеры, ключевые кадры, easing, управление выражениями  
`references/midi-osc.md`| MIDI/OSC контроллеры, TouchOSC, синхронизация нескольких машин  
`references/particles.md`| POPs и устаревший particleSOP — эмиссия, силы, коллизии  
`references/projection-mapping.md`| Многооконный вывод, corner pin, mesh warp, смешивание краёв  
`references/external-data.md`| HTTP, WebSocket, MQTT, Serial, TCP, webserverDAT  
`references/panel-ui.md`| Пользовательские параметры, panel COMPs, кнопки/слайдеры/поля, panelExecuteDAT  
`references/replicator.md`| replicatorCOMP — клонирование на основе данных, раскладки, колбэки  
`references/dat-scripting.md`| Execute DAT family — chop/dat/parameter/panel/op/executeDAT  
`references/3d-scene.md`| Системы освещения, тени, IBL/cubemaps, мультикамера, PBR  
`scripts/setup.sh`| Скрипт автоматической установки  
* * *
> Ты не пишешь код. Ты направляешь свет.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [CRITICAL RULES](<#critical-rules>)
  * [Architecture](<#architecture>)
  * [Setup (Automated)](<#setup-automated>)
    * [Manual steps (one-time, cannot be automated)](<#manual-steps-one-time-cannot-be-automated>)
  * [Environment Notes](<#environment-notes>)
  * [Workflow](<#workflow>)
    * [Step 0: Discover (before building anything)](<#step-0-discover-before-building-anything>)
    * [Step 1: Clean + Build](<#step-1-clean--build>)
    * [Step 2: Set Parameters](<#step-2-set-parameters>)
    * [Step 3: Wire](<#step-3-wire>)
    * [Step 4: Verify](<#step-4-verify>)
    * [Step 5: Display / Capture](<#step-5-display--capture>)
  * [MCP Tool Quick Reference](<#mcp-tool-quick-reference>)
  * [Key Implementation Rules](<#key-implementation-rules>)
  * [Recording / Exporting Video](<#recording--exporting-video>)
    * [Before Recording: Checklist](<#before-recording-checklist>)
  * [Audio-Reactive GLSL (Proven Recipe)](<#audio-reactive-glsl-proven-recipe>)
    * [Correct signal chain (tested April 2026)](<#correct-signal-chain-tested-april-2026>)
    * [Critical audio-reactive rules (empirically verified)](<#critical-audio-reactive-rules-empirically-verified>)
    * [GLSL spectrum sampling](<#glsl-spectrum-sampling>)
  * [Operator Quick Reference](<#operator-quick-reference>)
  * [Security Notes](<#security-notes>)
  * [References](<#references>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-touchdesigner-mcp -->
