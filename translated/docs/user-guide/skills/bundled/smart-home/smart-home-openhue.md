On this page
Управляй лампами Philips Hue, сценами и комнатами через OpenHue CLI.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
|Source| Bundled (installed by default)  |
|Path| `skills/smart-home/openhue`  |
|Version| `1.0.0`  |
|Author| community  |
|License| MIT  |
|Tags| `Smart-Home`, `Hue`, `Lights`, `IoT`, `Automation`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# OpenHue CLI
Управляй лампами и сценами Philips Hue через Hue Bridge из терминала.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
[code] 
    # Linux (pre-built binary)  
    curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue  
      
    # macOS  
    brew install openhue/cli/openhue-cli  
    
[/code]
При первом запуске требуется нажать кнопку на вашем Hue Bridge для сопряжения. Bridge должен находиться в той же локальной сети.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * «Включить/выключить свет»
  * «Уменьшить яркость света в гостиной»
  * «Установить сцену» или «режим кино»
  * Управление конкретными комнатами, зонами или отдельными лампочками Hue
  * Настройка яркости, цвета или цветовой температуры


## Common Commands[​](<#common-commands> "Direct link to Common Commands")
### List Resources[​](<#list-resources> "Direct link to List Resources")
[code] 
    openhue get light       # List all lights  
    openhue get room        # List all rooms  
    openhue get scene       # List all scenes  
    
[/code]
### Control Lights[​](<#control-lights> "Direct link to Control Lights")
[code] 
    # Turn on/off  
    openhue set light "Bedroom Lamp" --on  
    openhue set light "Bedroom Lamp" --off  
      
    # Brightness (0-100)  
    openhue set light "Bedroom Lamp" --on --brightness 50  
      
    # Color temperature (warm to cool: 153-500 mirek)  
    openhue set light "Bedroom Lamp" --on --temperature 300  
      
    # Color (by name or hex)  
    openhue set light "Bedroom Lamp" --on --color red  
    openhue set light "Bedroom Lamp" --on --rgb "#FF5500"  
    
[/code]
### Control Rooms[​](<#control-rooms> "Direct link to Control Rooms")
[code] 
    # Turn off entire room  
    openhue set room "Bedroom" --off  
      
    # Set room brightness  
    openhue set room "Bedroom" --on --brightness 30  
    
[/code]
### Scenes[​](<#scenes> "Direct link to Scenes")
[code] 
    openhue set scene "Relax" --room "Bedroom"  
    openhue set scene "Concentrate" --room "Office"  
    
[/code]
## Quick Presets[​](<#quick-presets> "Direct link to Quick Presets")
[code] 
    # Bedtime (dim warm)  
    openhue set room "Bedroom" --on --brightness 20 --temperature 450  
      
    # Work mode (bright cool)  
    openhue set room "Office" --on --brightness 100 --temperature 250  
      
    # Movie mode (dim)  
    openhue set room "Living Room" --on --brightness 10  
      
    # Everything off  
    openhue set room "Bedroom" --off  
    openhue set room "Office" --off  
    openhue set room "Living Room" --off  
    
[/code]
## Notes[​](<#notes> "Direct link to Notes")
  * Bridge должен находиться в той же локальной сети, что и машина с Hermes
  * При первом запуске требуется физически нажать кнопку на Hue Bridge для авторизации
  * Цвета работают только на цветных лампочках (не на моделях только с белым светом)
  * Имена ламп и комнат чувствительны к регистру — используй `openhue get light` для проверки точных имён
  * Отлично работает с cron-задачами для расписания освещения (например, приглушать перед сном, включать яркий свет при пробуждении)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [When to Use](<#when-to-use>)
  * [Common Commands](<#common-commands>)
    * [List Resources](<#list-resources>)
    * [Control Lights](<#control-lights>)
    * [Control Rooms](<#control-rooms>)
    * [Scenes](<#scenes>)
  * [Quick Presets](<#quick-presets>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/smart-home/smart-home-openhue -->
