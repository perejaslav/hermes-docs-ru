На этой странице
На этой странице описаны все команды, относящиеся к [профилям Hermes](</docs/user-guide/profiles>). Общие команды CLI см. в [Справочнике команд CLI](</docs/reference/cli-commands>).
## `hermes profile`[​](<#hermes-profile> "Прямая ссылка на hermes-profile")
[code] 
    hermes profile <подкоманда>  
    
[/code]
Главная команда для управления профилями. Запуск `hermes profile` без подкоманды показывает справку.
Подкоманда| Описание  
---|---  
`list`| Список всех профилей.  
`use`| Установить активный (используемый по умолчанию) профиль.  
`create`| Создать новый профиль.  
`delete`| Удалить профиль.  
`show`| Показать сведения о профиле.  
`alias`| Пересоздать псевдоним (alias) для профиля.  
`rename`| Переименовать профиль.  
`export`| Экспортировать профиль в tar.gz-архив.  
`import`| Импортировать профиль из tar.gz-архива.  
## `hermes profile list`[​](<#hermes-profile-list> "Прямая ссылка на hermes-profile-list")
[code] 
    hermes profile list  
    
[/code]
Выводит список всех профилей. Текущий активный профиль помечен символом `*`.
**Пример:**
[code] 
    $ hermes profile list  
      default  
    * work  
      dev  
      personal  
    
[/code]
Опций нет.
## `hermes profile use`[​](<#hermes-profile-use> "Прямая ссылка на hermes-profile-use")
[code] 
    hermes profile use <имя>  
    
[/code]
Устанавливает `<имя>` в качестве активного профиля. Все последующие команды `hermes` (без `-p`) будут использовать этот профиль.
Аргумент| Описание  
---|---  
`<имя>`| Имя профиля для активации. Используйте `default`, чтобы вернуться к базовому профилю.  
**Пример:**
[code] 
    hermes profile use work  
    hermes profile use default  
    
[/code]
## `hermes profile create`[​](<#hermes-profile-create> "Прямая ссылка на hermes-profile-create")
[code] 
    hermes profile create <имя> [опции]  
    
[/code]
Создаёт новый профиль.
Аргумент / Опция| Описание  
---|---  
`<имя>`| Имя нового профиля. Должно быть допустимым именем каталога (буквы, цифры, дефисы, подчёркивания).  
`--clone`| Скопировать `config.yaml`, `.env` и `SOUL.md` из текущего профиля.  
`--clone-all`| Скопировать всё (конфиг, воспоминания, навыки, сессии, состояние) из текущего профиля.  
`--clone-from <профиль>`| Клонировать из указанного профиля вместо текущего. Используется с `--clone` или `--clone-all`.  
`--no-alias`| Пропустить создание скрипта-обёртки.  
Создание профиля **не** делает этот каталог профиля каталогом проекта/рабочей области по умолчанию для терминальных команд. Если вы хотите, чтобы профиль запускался в определённом проекте, установите `terminal.cwd` в `config.yaml` этого профиля.
**Примеры:**
[code] 
    # Пустой профиль — требует полной настройки  
    hermes profile create mybot  
      
    # Клонировать только конфиг из текущего профиля  
    hermes profile create work --clone  
      
    # Клонировать всё из текущего профиля  
    hermes profile create backup --clone-all  
      
    # Клонировать конфиг из определённого профиля  
    hermes profile create work2 --clone --clone-from work  
    
[/code]
## `hermes profile delete`[​](<#hermes-profile-delete> "Прямая ссылка на hermes-profile-delete")
[code] 
    hermes profile delete <имя> [опции]  
    
[/code]
Удаляет профиль и удаляет его псевдоним (alias).
Аргумент / Опция| Описание  
---|---  
`<имя>`| Профиль для удаления.  
`--yes`, `-y`| Пропустить запрос подтверждения.  
**Пример:**
[code] 
    hermes profile delete mybot  
    hermes profile delete mybot --yes  
    
[/code]
warning
Это действие безвозвратно удаляет весь каталог профиля, включая все конфиги, воспоминания, сессии и навыки. Нельзя удалить текущий активный профиль.
## `hermes profile show`[​](<#hermes-profile-show> "Прямая ссылка на hermes-profile-show")
[code] 
    hermes profile show <имя>  
    
[/code]
Отображает сведения о профиле: домашний каталог, используемую модель, статус шлюза (gateway), количество навыков и состояние файлов конфигурации.
Здесь показан домашний каталог профиля Hermes, а не рабочая директория терминала. Команды терминала запускаются из `terminal.cwd` (или из каталога запуска на локальном бэкенде, когда `cwd: "."`).
Аргумент| Описание  
---|---  
`<имя>`| Профиль для просмотра.  
**Пример:**
[code] 
    $ hermes profile show work  
    Profile: work  
    Path:    ~/.hermes/profiles/work  
    Model:   anthropic/claude-sonnet-4 (anthropic)  
    Gateway: stopped  
    Skills:  12  
    .env:    exists  
    SOUL.md: exists  
    Alias:   ~/.local/bin/work  
    
[/code]
## `hermes profile alias`[​](<#hermes-profile-alias> "Прямая ссылка на hermes-profile-alias")
[code] 
    hermes profile alias <имя> [опции]  
    
[/code]
Пересоздаёт скрипт псевдонима (alias) в `~/.local/bin/<имя>`. Полезно, если псевдоним был случайно удалён или его нужно обновить после перемещения установки Hermes.
Аргумент / Опция| Описание  
---|---  
`<имя>`| Профиль, для которого нужно создать/обновить псевдоним.  
`--remove`| Удалить скрипт-обёртку вместо его создания.  
`--name <псевдоним>`| Пользовательское имя псевдонима (по умолчанию — имя профиля).  
**Пример:**
[code] 
    hermes profile alias work  
    # Создаёт/обновляет ~/.local/bin/work  
      
    hermes profile alias work --name mywork  
    # Создаёт ~/.local/bin/mywork  
      
    hermes profile alias work --remove  
    # Удаляет скрипт-обёртку  
    
[/code]
## `hermes profile rename`[​](<#hermes-profile-rename> "Прямая ссылка на hermes-profile-rename")
[code] 
    hermes profile rename <старое-имя> <новое-имя>  
    
[/code]
Переименовывает профиль. Обновляет каталог и псевдоним (alias).
Аргумент| Описание  
---|---  
`<старое-имя>`| Текущее имя профиля.  
`<новое-имя>`| Новое имя профиля.  
**Пример:**
[code] 
    hermes profile rename mybot assistant  
    # ~/.hermes/profiles/mybot → ~/.hermes/profiles/assistant  
    # ~/.local/bin/mybot → ~/.local/bin/assistant  
    
[/code]
## `hermes profile export`[​](<#hermes-profile-export> "Прямая ссылка на hermes-profile-export")
[code] 
    hermes profile export <имя> [опции]  
    
[/code]
Экспортирует профиль в виде сжатого tar.gz-архива.
Аргумент / Опция| Описание  
---|---  
`<имя>`| Профиль для экспорта.  
`-o`, `--output <путь>`| Путь к выходному файлу (по умолчанию: `<имя>.tar.gz`).  
**Пример:**
[code] 
    hermes profile export work  
    # Создаёт work.tar.gz в текущем каталоге  
      
    hermes profile export work -o ./work-2026-03-29.tar.gz  
    
[/code]
## `hermes profile import`[​](<#hermes-profile-import> "Прямая ссылка на hermes-profile-import")
[code] 
    hermes profile import <архив> [опции]  
    
[/code]
Импортирует профиль из tar.gz-архива.
Аргумент / Опция| Описание  
---|---  
`<архив>`| Путь к tar.gz-архиву для импорта.  
`--name <имя>`| Имя для импортированного профиля (по умолчанию определяется из архива).  
**Пример:**
[code] 
    hermes profile import ./work-2026-03-29.tar.gz  
    # Определяет имя профиля из архива  
      
    hermes profile import ./work-2026-03-29.tar.gz --name work-restored  
    
[/code]
## `hermes -p` / `hermes --profile`[​](<#hermes--p--hermes---profile> "Прямая ссылка на hermes--p--hermes---profile")
[code] 
    hermes -p <имя> <команда> [опции]  
    hermes --profile <имя> <команда> [опции]  
    
[/code]
Глобальный флаг для запуска любой команды Hermes в контексте определённого профиля без изменения фиксированного профиля по умолчанию. Переопределяет активный профиль на время выполнения команды.
Опция| Описание  
---|---  
`-p <имя>`, `--profile <имя>`| Профиль, используемый для этой команды.  
**Примеры:**
[code] 
    hermes -p work chat -q "Check the server status"  
    hermes --profile dev gateway start  
    hermes -p personal skills list  
    hermes -p work config edit  
    
[/code]
## `hermes completion`[​](<#hermes-completion> "Прямая ссылка на hermes-completion")
[code] 
    hermes completion <оболочка>  
    
[/code]
Генерирует скрипты автодополнения для оболочки. Включает дополнение имён профилей и подкоманд профилей.
Аргумент| Описание  
---|---  
`<оболочка>`| Оболочка, для которой генерируются автодополнения: `bash` или `zsh`.  
**Примеры:**
[code] 
    # Установка автодополнений  
    hermes completion bash >> ~/.bashrc  
    hermes completion zsh >> ~/.zshrc  
      
    # Перезагрузка оболочки  
    source ~/.bashrc  
    
[/code]
После установки автодополнение по табуляции работает для:
  * `hermes profile <TAB>` — подкоманды (list, use, create и т.д.)
  * `hermes profile use <TAB>` — имена профилей
  * `hermes -p <TAB>` — имена профилей


## См. также[​](<#see-also> "Прямая ссылка на См. также")
  * [Руководство по профилям](</docs/user-guide/profiles>)
  * [Справочник команд CLI](</docs/reference/cli-commands>)
  * [FAQ — раздел «Профили»](</docs/reference/faq#profiles>)


  * [`hermes profile`](<#hermes-profile>)
  * [`hermes profile list`](<#hermes-profile-list>)
  * [`hermes profile use`](<#hermes-profile-use>)
  * [`hermes profile create`](<#hermes-profile-create>)
  * [`hermes profile delete`](<#hermes-profile-delete>)
  * [`hermes profile show`](<#hermes-profile-show>)
  * [`hermes profile alias`](<#hermes-profile-alias>)
  * [`hermes profile rename`](<#hermes-profile-rename>)
  * [`hermes profile export`](<#hermes-profile-export>)
  * [`hermes profile import`](<#hermes-profile-import>)
  * [`hermes -p` / `hermes --profile`](<#hermes--p--hermes---profile>)
  * [`hermes completion`](<#hermes-completion>)
  * [См. также](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/profile-commands -->
