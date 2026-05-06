На этой странице
Установка и использование 1Password CLI (op). Используйте при установке CLI, включении интеграции с десктопным приложением, входе в систему и чтении/инъекции секретов для команд.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   |
|---|---|
|Источник| Опционально — установка `hermes skills install official/security/1password` |
|Путь| `optional-skills/security/1password` |
|Версия| `1.0.0` |
|Автор| arceus77-7, усовершенствовано Hermes Agent |
|Лицензия| MIT |
|Теги| `security`, `secrets`, `1password`, `op`, `cli` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Агент видит эти инструкции, когда навык активен.
# 1Password CLI
Используйте этот навык, когда пользователю нужно управлять секретами через 1Password вместо хранения в виде простых переменных окружения или файлов.
## Требования[​](<#requirements> "Прямая ссылка на Требования")
  * Учётная запись 1Password
  * Установленный 1Password CLI (`op`)
  * Один из вариантов: интеграция с десктопным приложением, токен сервисного аккаунта (`OP_SERVICE_ACCOUNT_TOKEN`) или Connect-сервер
  * Для стабильных аутентифицированных сессий при вызовах терминала Hermes необходим `tmux` (только для потока с десктопным приложением)


## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Установка или настройка 1Password CLI
  * Вход с помощью `op signin`
  * Чтение ссылок на секреты вида `op://Vault/Item/field`
  * Инъекция секретов в конфиги/шаблоны через `op inject`
  * Запуск команд с секретными переменными окружения через `op run`


## Методы аутентификации[​](<#authentication-methods> "Прямая ссылка на Методы аутентификации")
### Сервисный аккаунт (рекомендуется для Hermes)[​](<#service-account-recommended-for-hermes> "Прямая ссылка на Сервисный аккаунт \\(рекомендуется для Hermes\\))")
Установите `OP_SERVICE_ACCOUNT_TOKEN` в `~/.hermes/.env` (навык запросит его при первой загрузке). Десктопное приложение не требуется. Поддерживает `op read`, `op inject`, `op run`.
[code] 
    export OP_SERVICE_ACCOUNT_TOKEN="your-token-here"  
    op whoami  # проверка — должно показать Type: SERVICE_ACCOUNT  
    
[/code]
### Интеграция с десктопным приложением (интерактивно)[​](<#desktop-app-integration-interactive> "Прямая ссылка на Интеграция с десктопным приложением \\(интерактивно\\))")
  1. Включите в десктопном приложении 1Password: Настройки → Разработчик → Интеграция с 1Password CLI
  2. Убедитесь, что приложение разблокировано
  3. Выполните `op signin` и подтвердите биометрический запрос


### Connect Server (самостоятельный хостинг)[​](<#connect-server-self-hosted> "Прямая ссылка на Connect Server \\(самостоятельный хостинг\\))")
[code] 
    export OP_CONNECT_HOST="http://localhost:8080"  
    export OP_CONNECT_TOKEN="your-connect-token"  
    
[/code]
## Настройка[​](<#setup> "Прямая ссылка на Настройка")
  1. Установите CLI:


[code] 
    # macOS  
    brew install 1password-cli  
      
    # Linux (официальный пакет/документация по установке)  
    # Смотрите references/get-started.md для ссылок под конкретный дистрибутив.  
      
    # Windows (winget)  
    winget install AgileBits.1Password.CLI  
    
[/code]
  2. Проверьте:


[code] 
    op --version  
    
[/code]
  3. Выберите один из методов аутентификации выше и настройте его.


## Шаблон выполнения Hermes (поток с десктопным приложением)[​](<#hermes-execution-pattern-desktop-app-flow> "Прямая ссылка на Шаблон выполнения Hermes \\(поток с десктопным приложением\\))")
Команды терминала Hermes по умолчанию неинтерактивны и могут терять контекст аутентификации между вызовами. Для надёжной работы `op` с интеграцией десктопного приложения выполняйте вход и операции с секретами внутри выделенной tmux-сессии.
Примечание: Это НЕ требуется при использовании `OP_SERVICE_ACCOUNT_TOKEN` — токен сохраняется между вызовами терминала автоматически.
[code] 
    SOCKET_DIR="${TMPDIR:-/tmp}/hermes-tmux-sockets"  
    mkdir -p "$SOCKET_DIR"  
    SOCKET="$SOCKET_DIR/hermes-op.sock"  
    SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"  
      
    tmux -S "$SOCKET" new -d -s "$SESSION" -n shell  
      
    # Вход (подтвердите в десктопном приложении при запросе)  
    tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "eval \"\\$(op signin --account my.1password.com)\"" Enter  
      
    # Проверка аутентификации  
    tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter  
      
    # Пример чтения  
    tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op read 'op://Private/Npmjs/one-time password?attribute=otp'" Enter  
      
    # Получение вывода при необходимости  
    tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200  
      
    # Очистка  
    tmux -S "$SOCKET" kill-session -t "$SESSION"  
    
[/code]
## Часто используемые операции[​](<#common-operations> "Прямая ссылка на Часто используемые операции")
### Чтение секрета[​](<#read-a-secret> "Прямая ссылка на Чтение секрета")
[code] 
    op read "op://app-prod/db/password"  
    
[/code]
### Получение OTP[​](<#get-otp> "Прямая ссылка на Получение OTP")
[code] 
    op read "op://app-prod/npm/one-time password?attribute=otp"  
    
[/code]
### Инъекция в шаблон[​](<#inject-into-template> "Прямая ссылка на Инъекция в шаблон")
[code] 
    echo "db_password: {{ op://app-prod/db/password }}" | op inject  
    
[/code]
### Запуск команды с секретной переменной окружения[​](<#run-a-command-with-secret-env-var> "Прямая ссылка на Запуск команды с секретной переменной окружения")
[code] 
    export DB_PASSWORD="op://app-prod/db/password"  
    op run -- sh -c '[ -n "$DB_PASSWORD" ] && echo "DB_PASSWORD is set" || echo "DB_PASSWORD missing"'  
    
[/code]
## Ограничения[​](<#guardrails> "Прямая ссылка на Ограничения")
  * Никогда не выводите сырые секреты пользователю, если только он явно не запросил значение.
  * Предпочитайте `op run` / `op inject` вместо записи секретов в файлы.
  * Если команда завершается ошибкой «учётная запись не вошла в систему», выполните `op signin` повторно в той же tmux-сессии.
  * Если интеграция с десктопным приложением недоступна (headless/CI), используйте поток с токеном сервисного аккаунта.


## Примечание для CI / headless-сред[​](<#ci--headless-note> "Прямая ссылка на Примечание для CI / headless-сред")
Для неинтерактивного использования аутентифицируйтесь с помощью `OP_SERVICE_ACCOUNT_TOKEN` и избегайте интерактивного `op signin`. Сервисные аккаунты требуют CLI версии 2.18.0+.
## Ссылки[​](<#references> "Прямая ссылка на Ссылки")
  * `references/get-started.md`
  * `references/cli-examples.md`
  * <https://developer.1password.com/docs/cli/>
  * <https://developer.1password.com/docs/service-accounts/>


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Требования](<#requirements>)
  * [Когда использовать](<#when-to-use>)
  * [Методы аутентификации](<#authentication-methods>)
    * [Сервисный аккаунт (рекомендуется для Hermes)](<#service-account-recommended-for-hermes>)
    * [Интеграция с десктопным приложением (интерактивно)](<#desktop-app-integration-interactive>)
    * [Connect Server (самостоятельный хостинг)](<#connect-server-self-hosted>)
  * [Настройка](<#setup>)
  * [Шаблон выполнения Hermes (поток с десктопным приложением)](<#hermes-execution-pattern-desktop-app-flow>)
  * [Часто используемые операции](<#common-operations>)
    * [Чтение секрета](<#read-a-secret>)
    * [Получение OTP](<#get-otp>)
    * [Инъекция в шаблон](<#inject-into-template>)
    * [Запуск команды с секретной переменной окружения](<#run-a-command-with-secret-env-var>)
  * [Ограничения](<#guardrails>)
  * [Примечание для CI / headless-сред](<#ci--headless-note>)
  * [Ссылки](<#references>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/security/security-1password -->
