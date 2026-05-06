On this page
Отслеживание устройств Apple/AirTags через FindMy.app на macOS.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/apple/findmy` |
|Version| `1.0.0` |
|Author| Hermes Agent |
|License| MIT |
|Platforms| macos |
|Tags| `FindMy`, `AirTag`, `location`, `tracking`, `macOS`, `Apple` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Find My (Apple)
Отслеживай устройства Apple и AirTags через FindMy.app на macOS. Поскольку Apple не предоставляет CLI для FindMy, этот навык использует AppleScript для открытия приложения и захват экрана для чтения местоположений устройств.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **macOS** с приложением Find My и выполненным входом в iCloud
  * Устройства/AirTags уже зарегистрированы в Find My
  * Разрешение на запись экрана для терминала (System Settings → Privacy → Screen Recording)
  * **Опционально, но рекомендуется** : Установи `peekaboo` для улучшенной автоматизации UI: `brew install steipete/tap/peekaboo`


## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь спрашивает «где моё [устройство/кот/ключи/сумка]?»
  * Отслеживание местоположений AirTag
  * Проверка местоположений устройств (iPhone, iPad, Mac, AirPods)
  * Мониторинг перемещения питомца или предмета с течением времени (маршруты патрулирования AirTag)


## Method 1: AppleScript + Screenshot (Basic)[​](<#method-1-applescript--screenshot-basic> "Direct link to Method 1: AppleScript + Screenshot \(Basic\)")
### Open FindMy and Navigate[​](<#open-findmy-and-navigate> "Direct link to Open FindMy and Navigate")
[code] 
    # Открыть приложение Find My  
    osascript -e 'tell application "FindMy" to activate'  
      
    # Подождать загрузки  
    sleep 3  
      
    # Сделать скриншот окна Find My  
    screencapture -w -o /tmp/findmy.png  
    
[/code]
Затем используй `vision_analyze` для чтения скриншота:
[code] 
    vision_analyze(image_url="/tmp/findmy.png", question="Какие устройства/предметы показаны и где они находятся?")  
    
[/code]
### Switch Between Tabs[​](<#switch-between-tabs> "Direct link to Switch Between Tabs")
[code] 
    # Переключиться на вкладку Devices  
    osascript -e '  
    tell application "System Events"  
        tell process "FindMy"  
            click button "Devices" of toolbar 1 of window 1  
        end tell  
    end tell'  
      
    # Переключиться на вкладку Items (AirTags)  
    osascript -e '  
    tell application "System Events"  
        tell process "FindMy"  
            click button "Items" of toolbar 1 of window 1  
        end tell  
    end tell'  
    
[/code]
## Method 2: Peekaboo UI Automation (Recommended)[​](<#method-2-peekaboo-ui-automation-recommended> "Direct link to Method 2: Peekaboo UI Automation \(Recommended\)")
Если установлен `peekaboo`, используй его для более надёжного взаимодействия с UI:
[code] 
    # Открыть Find My  
    osascript -e 'tell application "FindMy" to activate'  
    sleep 3  
      
    # Захватить и аннотировать UI  
    peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png  
      
    # Нажать на конкретное устройство/предмет по ID элемента  
    peekaboo click --on B3 --app "FindMy"  
      
    # Захватить детальный вид  
    peekaboo image --app "FindMy" --path /tmp/findmy-detail.png  
    
[/code]
Затем проанализируй с помощью vision:
[code] 
    vision_analyze(image_url="/tmp/findmy-detail.png", question="Какое местоположение показано для этого устройства/предмета? Включи адрес и координаты, если видны.")  
    
[/code]
## Workflow: Track AirTag Location Over Time[​](<#workflow-track-airtag-location-over-time> "Direct link to Workflow: Track AirTag Location Over Time")
Для мониторинга AirTag (например, отслеживание маршрута патрулирования кота):
[code] 
    # 1. Открыть FindMy на вкладке Items  
    osascript -e 'tell application "FindMy" to activate'  
    sleep 3  
      
    # 2. Нажать на элемент AirTag (оставаться на странице — AirTag обновляется только когда страница открыта)  
      
    # 3. Периодически захватывать местоположение  
    while true; do  
        screencapture -w -o /tmp/findmy-$(date +%H%M%S).png  
        sleep 300  # Каждые 5 минут  
    done  
    
[/code]
Проанализируй каждый скриншот с помощью vision для извлечения координат, затем составь маршрут.
## Limitations[​](<#limitations> "Direct link to Limitations")
  * У FindMy **нет CLI или API** — необходимо использовать автоматизацию UI
  * AirTags обновляют местоположение только когда страница FindMy активно отображается
  * Точность местоположения зависит от находящихся рядом устройств Apple в сети FindMy
  * Требуется разрешение на запись экрана для скриншотов
  * Автоматизация UI через AppleScript может ломаться при обновлениях macOS


## Rules[​](<#rules> "Direct link to Rules")
  1. Держи приложение FindMy на переднем плане при отслеживании AirTags (обновления прекращаются при сворачивании)
  2. Используй `vision_analyze` для чтения содержимого скриншотов — не пытайся анализировать пиксели
  3. Для длительного отслеживания используй cronjob для периодического захвата и записи местоположений
  4. Уважай приватность — отслеживай только устройства/предметы, принадлежащие пользователю


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [When to Use](<#when-to-use>)
  * [Method 1: AppleScript + Screenshot (Basic)](<#method-1-applescript--screenshot-basic>)
    * [Open FindMy and Navigate](<#open-findmy-and-navigate>)
    * [Switch Between Tabs](<#switch-between-tabs>)
  * [Method 2: Peekaboo UI Automation (Recommended)](<#method-2-peekaboo-ui-automation-recommended>)
  * [Workflow: Track AirTag Location Over Time](<#workflow-track-airtag-location-over-time>)
  * [Limitations](<#limitations>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/apple/apple-findmy -->
