On this page
Apple Reminders через remindctl: добавление, просмотр, завершение.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/apple/apple-reminders` |
|Version| `1.0.0` |
|Author| Hermes Agent |
|License| MIT |
|Platforms| macos |
|Tags| `Reminders`, `tasks`, `todo`, `macOS`, `Apple` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Apple Reminders
Используй `remindctl` для управления Apple Reminders прямо из терминала. Задачи синхронизируются между всеми устройствами Apple через iCloud.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **macOS** с Reminders.app
  * Установка: `brew install steipete/tap/remindctl`
  * Предоставь разрешение для Reminders при запросе
  * Проверка: `remindctl status` / Запрос: `remindctl authorize`


## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь упоминает «напоминание» или «Reminders app»
  * Создание личных дел со сроками, которые синхронизируются с iOS
  * Управление списками Apple Reminders
  * Пользователь хочет, чтобы задачи отображались на его iPhone/iPad


## When NOT to Use[​](<#when-not-to-use> "Direct link to When NOT to Use")
  * Планирование оповещений агента → используй инструмент cronjob
  * События календаря → используй Apple Calendar или Google Calendar
  * Управление проектными задачами → используй GitHub Issues, Notion и т.д.
  * Если пользователь говорит «напомни», но имеет в виду оповещение агента → сначала уточни


## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
### View Reminders[​](<#view-reminders> "Direct link to View Reminders")
[code] 
    remindctl                    # Напоминания на сегодня  
    remindctl today              # Сегодня  
    remindctl tomorrow           # Завтра  
    remindctl week               # Эта неделя  
    remindctl overdue            # Просроченные  
    remindctl all                # Всё  
    remindctl 2026-01-04         # Конкретная дата  
    
[/code]
### Manage Lists[​](<#manage-lists> "Direct link to Manage Lists")
[code] 
    remindctl list               # Список всех списков  
    remindctl list Work          # Показать конкретный список  
    remindctl list Projects --create    # Создать список  
    remindctl list Work --delete        # Удалить список  
    
[/code]
### Create Reminders[​](<#create-reminders> "Direct link to Create Reminders")
[code] 
    remindctl add "Buy milk"  
    remindctl add --title "Call mom" --list Personal --due tomorrow  
    remindctl add --title "Meeting prep" --due "2026-02-15 09:00"  
    
[/code]
### Complete / Delete[​](<#complete--delete> "Direct link to Complete / Delete")
[code] 
    remindctl complete 1 2 3          # Завершить по ID  
    remindctl delete 4A83 --force     # Удалить по ID  
    
[/code]
### Output Formats[​](<#output-formats> "Direct link to Output Formats")
[code] 
    remindctl today --json       # JSON для скриптов  
    remindctl today --plain      # TSV формат  
    remindctl today --quiet      # Только количество  
    
[/code]
## Date Formats[​](<#date-formats> "Direct link to Date Formats")
Принимаются параметрами `--due` и фильтрами дат:
  * `today`, `tomorrow`, `yesterday`
  * `YYYY-MM-DD`
  * `YYYY-MM-DD HH:mm`
  * ISO 8601 (`2026-01-04T12:34:56Z`)


## Rules[​](<#rules> "Direct link to Rules")
  1. Когда пользователь говорит «напомни», уточняй: Apple Reminders (синхронизируется с телефоном) или оповещение агента через cronjob
  2. Всегда подтверждай содержание напоминания и дату выполнения перед созданием
  3. Используй `--json` для программного разбора


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [When to Use](<#when-to-use>)
  * [When NOT to Use](<#when-not-to-use>)
  * [Quick Reference](<#quick-reference>)
    * [View Reminders](<#view-reminders>)
    * [Manage Lists](<#manage-lists>)
    * [Create Reminders](<#create-reminders>)
    * [Complete / Delete](<#complete--delete>)
    * [Output Formats](<#output-formats>)
  * [Date Formats](<#date-formats>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/apple/apple-apple-reminders -->
