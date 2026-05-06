On this page
## Обновление[​](<#updating> "Прямая ссылка на Обновление")
Обновитесь до последней версии одной командой:
[code] 
    hermes update  
    
[/code]
Эта команда загружает последний код, обновляет зависимости и предлагает настроить новые параметры, добавленные с момента вашего последнего обновления.
tip
`hermes update` автоматически обнаруживает новые параметры конфигурации и предлагает их добавить. Если вы пропустили это предложение, вы можете вручную выполнить `hermes config check` для просмотра отсутствующих опций, а затем `hermes config migrate` для их интерактивного добавления.
### Что происходит во время обновления[​](<#what-happens-during-an-update> "Прямая ссылка на Что происходит во время обновления")
При запуске `hermes update` выполняются следующие шаги:
  1. **Снимок данных связывания (pairing-data)** — сохраняется облегчённый предобновительный снимок состояния (охватывает `~/.hermes/pairing/`, правила комментариев Feishu и другие файлы состояния, изменяемые во время выполнения). Откат возможен через `hermes backup restore --state pre-update`.
  2. **Git pull** — загружается последний код из ветки `main` и обновляются подмодули
  3. **Установка зависимостей** — выполняется `uv pip install -e ".[all]"` для установки новых или изменённых зависимостей
  4. **Миграция конфигурации** — обнаруживаются новые опции конфигурации, добавленные после вашей версии, и предлагается их настроить
  5. **Автоматический перезапуск шлюзов (gateways)** — работающие шлюзы обновляются после завершения обновления, чтобы новый код вступил в силу немедленно. Шлюзы, управляемые через сервисы (systemd на Linux, launchd на macOS), перезапускаются через менеджер служб. Ручные шлюзы перезапускаются автоматически, когда Hermes может сопоставить запущенный PID с профилем.


### Только проверка: `hermes update --check`[​](<#preview-only-hermes-update---check> "Прямая ссылка на only-hermes-update---check")
Хотите узнать, отстаёте ли вы от `origin/main`, не загружая изменения? Запустите `hermes update --check` — он выполнит fetch, выведет ваш локальный коммит и последний удалённый коммит рядом, и завершится с кодом `0`, если синхронизация актуальна, или `1`, если есть отставание. Файлы не изменяются, шлюзы не перезапускаются. Полезно в скриптах и cron-задачах, которые проверяют наличие обновления.
### Полное резервное копирование перед обновлением: `--backup`[​](<#full-pre-update-backup---backup> "Прямая ссылка на full-pre-update-backup---backup")
Для ценных профилей (продакшн-шлюзы, общие командные установки) вы можете включить полное резервное копирование `HERMES_HOME` (конфиг, аутентификация, сессии, навыки, связывание) перед загрузкой:
[code] 
    hermes update --backup  
    
[/code]
Или сделайте это поведением по умолчанию для каждого запуска:
[code] 
    # ~/.hermes/config.yaml  
    update:  
      backup: true  
    
[/code]
`--backup` был всегда включённым поведением в ранних сборках, но это добавляло минуты к каждому обновлению на больших домашних директориях, поэтому теперь это опционально. Облегчённый снимок данных связывания, описанный выше, всё ещё выполняется безусловно.
Ожидаемый вывод выглядит так:
[code] 
    $ hermes update  
    Updating Hermes Agent...  
    📥 Pulling latest code...  
    Already up to date.  (or: Updating abc1234..def5678)  
    📦 Updating dependencies...  
    ✅ Dependencies updated  
    🔍 Checking for new config options...  
    ✅ Config is up to date  (or: Found 2 new options — running migration...)  
    🔄 Restarting gateways...  
    ✅ Gateway restarted  
    ✅ Hermes Agent updated successfully!  
    
[/code]
### Рекомендуемая проверка после обновления[​](<#recommended-post-update-validation> "Прямая ссылка на Recommended Post-Update Validation")
`hermes update` выполняет основной процесс обновления, но быстрая проверка подтвердит, что всё прошло чисто:
  1. `git status --short` — если дерево неожиданно грязное, проверьте перед продолжением
  2. `hermes doctor` — проверяет конфиг, зависимости и состояние служб
  3. `hermes --version` — убедитесь, что версия обновилась как ожидалось
  4. Если вы используете шлюз: `hermes gateway status`
  5. Если `doctor` сообщает о проблемах npm audit: выполните `npm audit fix` в указанной директории


Грязное рабочее дерево после обновления
Если `git status --short` показывает неожиданные изменения после `hermes update`, остановитесь и проверьте их перед продолжением. Обычно это означает, что локальные изменения были повторно применены поверх обновлённого кода, или шаг с зависимостями обновил lock-файлы.
### Если ваш терминал отключился во время обновления[​](<#if-your-terminal-disconnects-mid-update> "Прямая ссылка на If your terminal disconnects mid-update")
`hermes update` защищает себя от случайной потери терминала:
  * Обновление игнорирует `SIGHUP`, поэтому закрытие SSH-сессии или окна терминала больше не прерывает процесс установки. Дочерние процессы `pip` и `git` наследуют эту защиту, так что окружение Python не может остаться наполовину установленным из-за разрыва соединения.
  * Весь вывод дублируется в `~/.hermes/logs/update.log` во время выполнения обновления. Если ваш терминал исчез, переподключитесь и проверьте лог, чтобы узнать, завершилось ли обновление и успешен ли перезапуск шлюза:


[code] 
    tail -f ~/.hermes/logs/update.log  
    
[/code]
  * `Ctrl-C` (SIGINT) и завершение системы (SIGTERM) по-прежнему обрабатываются — это намеренные отмены, а не случайности.


Вам больше не нужно оборачивать `hermes update` в `screen` или `tmux`, чтобы пережить отключение терминала.
### Проверка текущей версии[​](<#checking-your-current-version> "Прямая ссылка на Checking your current version")
[code] 
    hermes version  
    
[/code]
Сравните с последним релизом на [странице релизов GitHub](<https://github.com/NousResearch/hermes-agent/releases>).
### Обновление через мессенджеры[​](<#updating-from-messaging-platforms> "Прямая ссылка на Updating from Messaging Platforms")
Вы также можете обновиться напрямую из Telegram, Discord, Slack, WhatsApp или Teams, отправив:
[code] 
    /update  
    
[/code]
Это загружает последний код, обновляет зависимости и перезапускает работающие шлюзы. Бот ненадолго отключится во время перезапуска (обычно 5–15 секунд), а затем возобновит работу.
### Ручное обновление[​](<#manual-update> "Прямая ссылка на Manual Update")
Если вы устанавливали вручную (не через быстрый установщик):
[code] 
    cd /path/to/hermes-agent  
    export VIRTUAL_ENV="$(pwd)/venv"  
      
    # Pull latest code and submodules  
    git pull origin main  
    git submodule update --init --recursive  
      
    # Reinstall (picks up new dependencies)  
    uv pip install -e ".[all]"  
    uv pip install -e "./tinker-atropos"  
      
    # Check for new config options  
    hermes config check  
    hermes config migrate   # Interactively add any missing options  
    
[/code]
### Инструкции по откату[​](<#rollback-instructions> "Прямая ссылка на Rollback instructions")
Если обновление вызвало проблему, вы можете откатиться к предыдущей версии:
[code] 
    cd /path/to/hermes-agent  
      
    # List recent versions  
    git log --oneline -10  
      
    # Roll back to a specific commit  
    git checkout <commit-hash>  
    git submodule update --init --recursive  
    uv pip install -e ".[all]"  
      
    # Restart the gateway if running  
    hermes gateway restart  
    
[/code]
Чтобы откатиться к определённому релизному тегу:
[code] 
    git checkout v0.6.0  
    git submodule update --init --recursive  
    uv pip install -e ".[all]"  
    
[/code]
warning
Откат может вызвать несовместимость конфигурации, если были добавлены новые опции. Запустите `hermes config check` после отката и удалите нераспознанные опции из `config.yaml`, если возникнут ошибки.
### Примечание для пользователей Nix[​](<#note-for-nix-users> "Прямая ссылка на Note for Nix users")
Если вы устанавливали через Nix flake, обновления управляются через пакетный менеджер Nix:
[code] 
    # Update the flake input  
    nix flake update hermes-agent  
      
    # Or rebuild with the latest  
    nix profile upgrade hermes-agent  
    
[/code]
Установки Nix неизменяемы — откат обрабатывается системой поколений Nix:
[code] 
    nix profile rollback  
    
[/code]
См. [Настройка Nix](</docs/getting-started/nix-setup>) для подробностей.
* * *
## Удаление[​](<#uninstalling> "Прямая ссылка на Uninstalling")
[code] 
    hermes uninstall  
    
[/code]
Установщик предлагает сохранить ваши конфигурационные файлы (`~/.hermes/`) для будущей переустановки.
### Ручное удаление[​](<#manual-uninstall> "Прямая ссылка на Manual Uninstall")
[code] 
    rm -f ~/.local/bin/hermes  
    rm -rf /path/to/hermes-agent  
    rm -rf ~/.hermes            # Optional — keep if you plan to reinstall  
    
[/code]
info
Если вы установили шлюз как системную службу, сначала остановите и отключите его:
[code]
    hermes gateway stop  
    # Linux: systemctl --user disable hermes-gateway  
    # macOS: launchctl remove ai.hermes.gateway  
    
[/code]
  * [Обновление](<#updating>)
    * [Что происходит во время обновления](<#what-happens-during-an-update>)
    * [Только проверка: `hermes update --check`](<#preview-only-hermes-update---check>)
    * [Полное резервное копирование перед обновлением: `--backup`](<#full-pre-update-backup---backup>)
    * [Рекомендуемая проверка после обновления](<#recommended-post-update-validation>)
    * [Если ваш терминал отключился во время обновления](<#if-your-terminal-disconnects-mid-update>)
    * [Проверка текущей версии](<#checking-your-current-version>)
    * [Обновление через мессенджеры](<#updating-from-messaging-platforms>)
    * [Ручное обновление](<#manual-update>)
    * [Инструкции по откату](<#rollback-instructions>)
    * [Примечание для пользователей Nix](<#note-for-nix-users>)
  * [Удаление](<#uninstalling>)
    * [Ручное удаление](<#manual-uninstall>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/getting-started/updating -->
