На этой странице
Быстрые ответы и решения самых частых вопросов и проблем.
* * *
## Часто задаваемые вопросы[​](<#frequently-asked-questions> "Direct link to Frequently Asked Questions")
### Какие LLM-провайдеры работают с Hermes?[​](<#what-llm-providers-work-with-hermes> "Direct link to What LLM providers work with Hermes?")
Hermes Agent работает с любым API, совместимым с OpenAI. Поддерживаемые провайдеры:
  * **[OpenRouter](<https://openrouter.ai/>)** — доступ к сотням моделей через один API-ключ (рекомендуется для гибкости)
  * **Nous Portal** — собственный inference-энdpoint Nous Research
  * **OpenAI** — GPT-4o, o1, o3 и др.
  * **Anthropic** — модели Claude (через OpenRouter или совместимый прокси)
  * **Google** — модели Gemini (через OpenRouter или совместимый прокси)
  * **z.ai / ZhipuAI** — модели GLM
  * **Kimi / Moonshot AI** — модели Kimi
  * **MiniMax** — глобальные и китайские endpoint'ы
  * **Локальные модели** — через [Ollama](<https://ollama.com/>), [vLLM](<https://docs.vllm.ai/>), [llama.cpp](<https://github.com/ggerganov/llama.cpp>), [SGLang](<https://github.com/sgl-project/sglang>) или любой совместимый с OpenAI сервер


Укажите своего провайдера командой `hermes model` или отредактировав `~/.hermes/.env`. См. справочник [Переменные окружения](</docs/reference/environment-variables>) для всех ключей провайдеров.
### Работает ли на Windows?[​](<#does-it-work-on-windows> "Direct link to Does it work on Windows?")
**Не нативно.** Hermes Agent требует Unix-подобного окружения. В Windows установите [WSL2](<https://learn.microsoft.com/en-us/windows/wsl/install>) и запускайте Hermes из него. Стандартная команда установки отлично работает в WSL2:
[code]
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    
[/code]
### Я запускаю Hermes в WSL2. Как лучше всего управлять обычным Windows Chrome?[​](<#i-run-hermes-in-wsl2-whats-the-best-way-to-control-my-normal-windows-chrome> "Direct link to I run Hermes in WSL2. What's the best way to control my normal Windows Chrome?")
Предпочтительнее использовать MCP-мост вместо `/browser connect`.
Рекомендуемая схема:
  * запустите Hermes внутри WSL2
  * продолжайте использовать ваш обычный Chrome с авторизацией в Windows
  * добавьте `chrome-devtools-mcp` в качестве MCP-сервера через `cmd.exe` или `powershell.exe`
  * позвольте Hermes использовать полученные MCP-инструменты для браузера


Это надёжнее, чем пытаться заставить встроенный браузерный транспорт Hermes подключаться напрямую через границу WSL2/Windows.
См.:
  * [Использование MCP с Hermes](</docs/guides/use-mcp-with-hermes#wsl2-bridge-hermes-in-wsl-to-windows-chrome>)
  * [Автоматизация браузера](</docs/user-guide/features/browser#wsl2--windows-chrome-prefer-mcp-over-browser-connect>)


### Работает ли на Android / Termux?[​](<#does-it-work-on-android--termux> "Direct link to Does it work on Android / Termux?")
Да — у Hermes есть проверенный путь установки в Termux на Android-устройствах.
Быстрая установка:
[code]
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    
[/code]
Полные пошаговые инструкции, поддерживаемые расширения и текущие ограничения см. в [руководстве по Termux](</docs/getting-started/termux>).
Важное замечание: полное расширение `.[all]` пока недоступно на Android, поскольку расширение `voice` зависит от `faster-whisper` → `ctranslate2`, а `ctranslate2` не публикует сборки для Android. Используйте проверенное расширение `.[termux]`.
### Передаются ли мои данные куда-либо?[​](<#is-my-data-sent-anywhere> "Direct link to Is my data sent anywhere?")
API-вызовы направляются **только тому LLM-провайдеру, которого вы настроили** (например, OpenRouter или ваш локальный экземпляр Ollama). Hermes Agent не собирает телеметрию, данные об использовании или аналитику. Ваши беседы, память и навыки хранятся локально в `~/.hermes/`.
### Можно ли использовать офлайн / с локальными моделями?[​](<#can-i-use-it-offline--with-local-models> "Direct link to Can I use it offline / with local models?")
Да. Запустите `hermes model`, выберите **Custom endpoint** и введите URL вашего сервера:
[code]
    hermes model
    # Выберите: Custom endpoint (enter URL manually)
    # API base URL: http://localhost:11434/v1
    # API key: ollama
    # Model name: qwen3.5:27b
    # Context length: 32768   ← установите в соответствии с реальным контекстным окном вашего сервера
    
[/code]
Или настройте напрямую в `config.yaml`:
[code]
    model:
      default: qwen3.5:27b
      provider: custom
      base_url: http://localhost:11434/v1
    
[/code]
Hermes сохраняет endpoint, провайдера и base URL в `config.yaml`, так что настройки переживают перезапуски. Если на вашем локальном сервере загружена ровно одна модель, `/model custom` определит её автоматически. Вы также можете установить `provider: custom` в config.yaml — это полноценный провайдер, а не псевдоним чего-либо ещё.
Это работает с Ollama, vLLM, llama.cpp server, SGLang, LocalAI и другими. Подробнее см. в [руководстве по настройке](</docs/user-guide/configuration>).
Пользователям Ollama
Если вы установили пользовательский `num_ctx` в Ollama (например, `ollama run --num_ctx 16384`), обязательно укажите соответствующий размер контекста в Hermes — API `/api/show` в Ollama сообщает _максимальный_ контекст модели, а не эффективный `num_ctx`, который вы настроили.
Таймауты с локальными моделями
Hermes автоматически определяет локальные endpoint'ы и смягчает таймауты потоковой передачи (таймаут чтения увеличен со 120 с до 1800 с, обнаружение устаревшего потока отключено). Если вы всё равно сталкиваетесь с таймаутами при очень больших контекстах, установите `HERMES_STREAM_READ_TIMEOUT=1800` в вашем `.env`. Подробности см. в [руководстве по локальным LLM](</docs/guides/local-llm-on-mac#timeouts>).
### Сколько это стоит?[​](<#how-much-does-it-cost> "Direct link to How much does it cost?")
Hermes Agent — **бесплатный проект с открытым исходным кодом** (лицензия MIT). Вы платите только за использование LLM API вашего провайдера. Локальные модели полностью бесплатны в запуске.
### Могут ли несколько человек использовать один экземпляр?[​](<#can-multiple-people-use-one-instance> "Direct link to Can multiple people use one instance?")
Да. [Шлюз обмена сообщениями](</docs/user-guide/messaging/>) позволяет нескольким пользователям взаимодействовать с одним экземпляром Hermes Agent через Telegram, Discord, Slack, WhatsApp или Home Assistant. Доступ контролируется через белые списки (конкретные ID пользователей) и DM-сопряжение (первый пользователь, написавший в личку, получает доступ).
### В чём разница между памятью (memory) и навыками (skills)?[​](<#whats-the-difference-between-memory-and-skills> "Direct link to What's the difference between memory and skills?")
  * **Память** хранит **факты** — то, что агент знает о вас, ваших проектах и предпочтениях. Воспоминания извлекаются автоматически на основе релевантности.
  * **Навыки** хранят **процедуры** — пошаговые инструкции о том, как что-то делать. Навыки вызываются, когда агент сталкивается с похожей задачей.


И то, и другое сохраняется между сессиями. Подробнее см. [Память](</docs/user-guide/features/memory>) и [Навыки](</docs/user-guide/features/skills>).
### Можно ли использовать Hermes в своём Python-проекте?[​](<#can-i-use-it-in-my-own-python-project> "Direct link to Can I use it in my own Python project?")
Да. Импортируйте класс `AIAgent` и используйте Hermes программно:
[code]
    from run_agent import AIAgent
    
    agent = AIAgent(model="anthropic/claude-opus-4.7")
    response = agent.chat("Explain quantum computing briefly")
    
[/code]
Полное описание API см. в [руководстве по Python-библиотеке](</docs/user-guide/features/code-execution>).
* * *
## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")
### Проблемы установки[​](<#installation-issues> "Direct link to Installation Issues")
#### `hermes: command not found` после установки[​](<#hermes-command-not-found-after-installation> "Direct link to hermes-command-not-found-after-installation")
**Причина:** Ваша оболочка ещё не перезагрузила обновлённый PATH.
**Решение:**
[code]
    # Перезагрузите профиль оболочки
    source ~/.bashrc    # bash
    source ~/.zshrc     # zsh
    
    # Или откройте новый терминал
    
[/code]
Если это не помогло, проверьте расположение установки:
[code]
    which hermes
    ls ~/.local/bin/hermes
    
[/code]
tip
Установщик добавляет `~/.local/bin` в PATH. Если вы используете нестандартную конфигурацию оболочки, добавьте `export PATH="$HOME/.local/bin:$PATH"` вручную.
#### Версия Python слишком старая[​](<#python-version-too-old> "Direct link to Python version too old")
**Причина:** Hermes требует Python 3.11 или новее.
**Решение:**
[code]
    python3 --version   # Проверьте текущую версию
    
    # Установите более новую версию Python
    sudo apt install python3.12   # Ubuntu/Debian
    brew install python@3.12      # macOS
    
[/code]
Установщик делает это автоматически — если вы видите эту ошибку при ручной установке, сначала обновите Python.
#### Команды в терминале говорят `node: command not found` (или `nvm`, `pyenv`, `asdf`, …)[​](<#terminal-commands-say-node-command-not-found-or-nvm-pyenv-asdf-> "Direct link to terminal-commands-say-node-command-not-found-or-nvm-pyenv-asdf-")
**Причина:** Hermes создаёт снимок окружения для каждой сессии, запуская `bash -l` один раз при старте. Входная оболочка bash читает `/etc/profile`, `~/.bash_profile` и `~/.profile`, но **не обрабатывает`~/.bashrc`** — поэтому инструменты, устанавливающие себя туда (`nvm`, `asdf`, `pyenv`, `cargo`, пользовательские `PATH`), остаются невидимыми для снимка. Чаще всего это происходит, когда Hermes запускается под systemd или в минимальной оболочке, где не был предварительно загружен профиль интерактивной оболочки.
**Решение:** По умолчанию Hermes автоматически подгружает `~/.bashrc`. Если этого недостаточно — например, вы пользователь zsh, чей PATH находится в `~/.zshrc`, или вы инициализируете `nvm` из отдельного файла — укажите дополнительные файлы для загрузки в `~/.hermes/config.yaml`:
[code]
    terminal:
      shell_init_files:
        - ~/.zshrc                     # пользователи zsh: подтягивает PATH из zsh в bash-снимок
        - ~/.nvm/nvm.sh                # прямая инициализация nvm (работает независимо от оболочки)
        - /etc/profile.d/cargo.sh      # общесистемные rc-файлы
      # Когда этот список задан, авто-загрузка ~/.bashrc по умолчанию НЕ добавляется —
      # включите его явно, если хотите оба:
      #   - ~/.bashrc
      #   - ~/.zshrc
    
[/code]
Отсутствующие файлы пропускаются без сообщений. Загрузка происходит в bash, поэтому файлы, использующие синтаксис, специфичный для zsh, могут вызвать ошибки — если это важно, загружайте только часть, устанавливающую PATH (например, `nvm.sh` напрямую), а не весь rc-файл.
Чтобы отключить авто-загрузку (строгая семантика входной оболочки):
[code]
    terminal:
      auto_source_bashrc: false
    
[/code]
#### `uv: command not found`[​](<#uv-command-not-found> "Direct link to uv-command-not-found")
**Причина:** Менеджер пакетов `uv` не установлен или отсутствует в PATH.
**Решение:**
[code]
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
    
[/code]
#### Ошибки отказа в доступе (Permission denied) во время установки[​](<#permission-denied-errors-during-install> "Direct link to Permission denied errors during install")
**Причина:** Недостаточно прав для записи в каталог установки.
**Решение:**
[code]
    # Не используйте sudo с установщиком — он устанавливает в ~/.local/bin
    # Если вы ранее устанавливали через sudo, очистите:
    sudo rm /usr/local/bin/hermes
    # Затем перезапустите стандартный установщик
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    
[/code]
* * *
### Проблемы с провайдерами и моделями[​](<#provider--model-issues> "Direct link to Provider & Model Issues")
#### `/model` показывает только одного провайдера / не могу переключить провайдера[​](<#model-only-shows-one-provider--cant-switch-providers> "Direct link to model-only-shows-one-provider--cant-switch-providers")
**Причина:** `/model` (внутри чат-сессии) может переключаться только между провайдерами, которых вы **уже настроили**. Если вы настроили только OpenRouter, `/model` покажет только его.
**Решение:** Выйдите из сессии и используйте `hermes model` в терминале, чтобы добавить новых провайдеров:
[code]
    # Сначала выйдите из чат-сессии Hermes (Ctrl+C или /quit)
    
    # Запустите мастер настройки провайдеров
    hermes model
    
    # Это позволит вам: добавлять провайдеров, проходить OAuth, вводить API-ключи, настраивать endpoint'ы
    
[/code]
После добавления нового провайдера через `hermes model` начните новую чат-сессию — `/model` теперь покажет всех настроенных провайдеров.
Краткая справка
Если хотите...| Используйте
---|---
Добавить нового провайдера| `hermes model` (из терминала)
Ввести/изменить API-ключи| `hermes model` (из терминала)
Переключить модель в середине сессии| `/model <имя>` (внутри сессии)
Переключиться на другого настроенного провайдера| `/model provider:model` (внутри сессии)
#### API-ключ не работает[​](<#api-key-not-working> "Direct link to API key not working")
**Причина:** Ключ отсутствует, истёк, неправильно установлен или относится к другому провайдеру.
**Решение:**
[code]
    # Проверьте вашу конфигурацию
    hermes config show
    
    # Перенастройте провайдера
    hermes model
    
    # Или установите напрямую
    hermes config set OPENROUTER_API_KEY sk-or-v1-xxxxxxxxxxxx
    
[/code]
warning
Убедитесь, что ключ соответствует провайдеру. Ключ OpenAI не будет работать с OpenRouter и наоборот. Проверьте `~/.hermes/.env` на наличие конфликтующих записей.
#### Модель недоступна / модель не найдена[​](<#model-not-available--model-not-found> "Direct link to Model not available / model not found")
**Причина:** Идентификатор модели неверен или недоступен у вашего провайдера.
**Решение:**
[code]
    # Список доступных моделей для вашего провайдера
    hermes model
    
    # Установите корректную модель
    hermes config set HERMES_MODEL anthropic/claude-opus-4.7
    
    # Или укажите для конкретной сессии
    hermes chat --model openrouter/meta-llama/llama-3.1-70b-instruct
    
[/code]
#### Ограничение частоты запросов (ошибки 429)[​](<#rate-limiting-429-errors> "Direct link to Rate limiting (429 errors)")
**Причина:** Превышены лимиты частоты запросов вашего провайдера.
**Решение:** Подождите немного и повторите попытку. При интенсивном использовании рассмотрите:
  * Переход на более дорогой тариф провайдера
  * Смену модели или провайдера
  * Использование `hermes chat --provider <альтернатива>` для маршрутизации к другому бэкенду


#### Превышение длины контекста[​](<#context-length-exceeded> "Direct link to Context length exceeded")
**Причина:** Беседа стала слишком длинной для контекстного окна модели, или Hermes определил неправильную длину контекста для вашей модели.
**Решение:**
[code]
    # Сожмите текущую сессию
    /compress
    
    # Или начните новую сессию
    hermes chat
    
    # Используйте модель с большим контекстным окном
    hermes chat --model openrouter/google/gemini-3-flash-preview
    
[/code]
Если это происходит в первом длинном разговоре, возможно, Hermes определил неправильный размер контекста для вашей модели. Проверьте, что он обнаружил:
Посмотрите на строку запуска CLI — она показывает определённый размер контекста (например, `📊 Context limit: 128000 tokens`). Вы также можете проверить с помощью `/usage` во время сессии.
Чтобы исправить определение контекста, укажите его явно:
[code]
    # В ~/.hermes/config.yaml
    model:
      default: your-model-name
      context_length: 131072  # реальный контекст вашей модели
    
[/code]
Или для пользовательских endpoint'ов укажите для каждой модели:
[code]
    custom_providers:
      - name: "My Server"
        base_url: "http://localhost:11434/v1"
        models:
          qwen3.5:27b:
            context_length: 32768
    
[/code]
См. [Определение длины контекста](</docs/integrations/providers#context-length-detection>) о том, как работает автоопределение и все опции переопределения.
* * *
### Проблемы с терминалом[​](<#terminal-issues> "Direct link to Terminal Issues")
#### Команда заблокирована как опасная[​](<#command-blocked-as-dangerous> "Direct link to Command blocked as dangerous")
**Причина:** Hermes обнаружил потенциально деструктивную команду (например, `rm -rf`, `DROP TABLE`). Это функция безопасности.
**Решение:** При запросе проверьте команду и введите `y` для подтверждения. Вы также можете:
  * Попросить агента использовать более безопасную альтернативу
  * Посмотреть полный список опасных шаблонов в [документации по безопасности](</docs/user-guide/security>)


tip
Это работает по замыслу — Hermes никогда не выполняет деструктивные команды молча. Запрос подтверждения показывает вам, что именно будет выполнено.
#### `sudo` не работает через шлюз обмена сообщениями[​](<#sudo-not-working-via-messaging-gateway> "Direct link to sudo-not-working-via-messaging-gateway")
**Причина:** Шлюз обмена сообщениями работает без интерактивного терминала, поэтому `sudo` не может запросить пароль.
**Решение:**
  * Избегайте `sudo` в сообщениях — попросите агента найти альтернативы
  * Если необходимо использовать `sudo`, настройте `sudo` без пароля для конкретных команд в `/etc/sudoers`
  * Или переключитесь на терминальный интерфейс для административных задач: `hermes chat`


#### Docker-бэкенд не подключается[​](<#docker-backend-not-connecting> "Direct link to Docker backend not connecting")
**Причина:** Демон Docker не запущен или у пользователя нет прав.
**Решение:**
[code]
    # Проверьте, запущен ли Docker
    docker info
    
    # Добавьте пользователя в группу docker
    sudo usermod -aG docker $USER
    newgrp docker
    
    # Проверьте
    docker run hello-world
    
[/code]
* * *
### Проблемы с обменом сообщениями[​](<#messaging-issues> "Direct link to Messaging Issues")
#### Бот не отвечает на сообщения[​](<#bot-not-responding-to-messages> "Direct link to Bot not responding to messages")
**Причина:** Бот не запущен, не авторизован, или ваш пользователь не находится в белом списке.
**Решение:**
[code]
    # Проверьте, запущен ли шлюз
    hermes gateway status
    
    # Запустите шлюз
    hermes gateway start
    
    # Проверьте логи на наличие ошибок
    cat ~/.hermes/logs/gateway.log | tail -50
    
[/code]
#### Сообщения не доставляются[​](<#messages-not-delivering> "Direct link to Messages not delivering")
**Причина:** Проблемы с сетью, истёк токен бота или неверная конфигурация вебхука платформы.
**Решение:**
  * Проверьте валидность токена бота: `hermes gateway setup`
  * Проверьте логи шлюза: `cat ~/.hermes/logs/gateway.log | tail -50`
  * Для платформ на вебхуках (Slack, WhatsApp) убедитесь, что ваш сервер доступен из интернета


#### Путаница с белым списком — кто может общаться с ботом?[​](<#allowlist-confusion--who-can-talk-to-the-bot> "Direct link to Allowlist confusion — who can talk to the bot")
**Причина:** Режим авторизации определяет, кто получает доступ.
**Решение:**
Режим| Как это работает
---|---
**Белый список**|  Только ID пользователей, указанные в конфиге, могут взаимодействовать
**DM-сопряжение**|  Первый пользователь, написавший в личку, получает исключительный доступ
**Открытый**|  Любой может взаимодействовать (не рекомендуется для продакшена)
Настраивается в `~/.hermes/config.yaml` в разделе настроек вашего шлюза. См. [документацию по обмену сообщениями](</docs/user-guide/messaging/>).
#### Шлюз не запускается[​](<#gateway-wont-start> "Direct link to Gateway won't start")
**Причина:** Отсутствуют зависимости, конфликты портов или неверно настроенные токены.
**Решение:**
[code]
    # Установите основные зависимости шлюза обмена сообщениями
    pip install "hermes-agent[messaging]"  # Telegram, Discord, Slack и общие зависимости шлюза
    
    # Проверьте конфликты портов
    lsof -i :8080
    
    # Проверьте конфигурацию
    hermes config show
    
[/code]
#### WSL: Шлюз постоянно отключается или `hermes gateway start` завершается ошибкой[​](<#wsl-gateway-keeps-disconnecting-or-hermes-gateway-start-fails> "Direct link to wsl-gateway-keeps-disconnecting-or-hermes-gateway-start-fails")
**Причина:** Поддержка systemd в WSL ненадёжна. Во многих установках WSL2 systemd не включён, и даже при включении службы могут не переживать перезагрузки WSL или отключение Windows в режиме ожидания.
**Решение:** Используйте режим переднего плана вместо systemd-службы:
[code]
    # Вариант 1: Напрямую в режиме переднего плана (проще всего)
    hermes gateway run
    
    # Вариант 2: Постоянный процесс через tmux (переживает закрытие терминала)
    tmux new -s hermes 'hermes gateway run'
    # Подключиться позже: tmux attach -t hermes
    
    # Вариант 3: Фоновый процесс через nohup
    nohup hermes gateway run > ~/.hermes/logs/gateway.log 2>&1 &
    
[/code]
Если вы всё же хотите попробовать systemd, убедитесь, что он включён:
  1. Откройте `/etc/wsl.conf` (создайте его, если не существует)
  2. Добавьте:
[code] [boot]
         systemd=true
         
[/code]
  3. Из PowerShell: `wsl --shutdown`
  4. Снова откройте терминал WSL
  5. Проверьте: `systemctl is-system-running` должно сказать "running" или "degraded"


Автозапуск при загрузке Windows
Для надёжного автозапуска используйте Планировщик задач Windows для запуска WSL + шлюза при входе в систему:
  1. Создайте задачу, выполняющую `wsl -d Ubuntu -- bash -lc 'hermes gateway run'`
  2. Установите триггер на вход пользователя в систему


#### macOS: Node.js / ffmpeg / другие инструменты не найдены шлюзом[​](<#macos-nodejs--ffmpeg--other-tools-not-found-by-gateway> "Direct link to macOS: Node.js / ffmpeg / other tools not found by gateway")
**Причина:** Службы launchd наследуют минимальный PATH (`/usr/bin:/bin:/usr/sbin:/sbin`), который не включает каталоги инструментов, установленных пользователем (Homebrew, nvm, cargo и т.д.). Это часто ломает WhatsApp-мост (`node not found`) или распознавание голоса (`ffmpeg not found`).
**Решение:** Шлюз захватывает PATH вашей оболочки, когда вы запускаете `hermes gateway install`. Если вы установили инструменты после настройки шлюза, перезапустите установку, чтобы захватить обновлённый PATH:
[code]
    hermes gateway install    # Повторно снимает снимок текущего PATH
    hermes gateway start      # Обнаруживает обновлённый plist и перезагружается
    
[/code]
Вы можете проверить, что plist содержит правильный PATH:
[code]
    /usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:PATH" \
      ~/Library/LaunchAgents/ai.hermes.gateway.plist
    
[/code]
* * *
### Проблемы с производительностью[​](<#performance-issues> "Direct link to Performance Issues")
#### Медленные ответы[​](<#slow-responses> "Direct link to Slow responses")
**Причина:** Большая модель, удалённый API-сервер или тяжёлый системный промпт с множеством инструментов.
**Решение:**
  * Попробуйте более быструю/маленькую модель: `hermes chat --model openrouter/meta-llama/llama-3.1-8b-instruct`
  * Уменьшите количество активных инструментов: `hermes chat -t "terminal"`
  * Проверьте задержку сети до провайдера
  * Для локальных моделей убедитесь, что у вас достаточно видеопамяти GPU


#### Высокое потребление токенов[​](<#high-token-usage> "Direct link to High token usage")
**Причина:** Длинные беседы, многословные системные промпты или множество вызовов инструментов, накапливающих контекст.
**Решение:**
[code]
    # Сожмите беседу для уменьшения количества токенов
    /compress
    
    # Проверьте использование токенов в сессии
    /usage
    
[/code]
tip
Используйте `/compress` регулярно во время длительных сессий. Он сжимает историю разговора и значительно уменьшает использование токенов, сохраняя при этом контекст.
#### Сессия становится слишком длинной[​](<#session-getting-too-long> "Direct link to Session getting too long")
**Причина:** Продолжительные беседы накапливают сообщения и результаты работы инструментов, приближаясь к лимитам контекста.
**Решение:**
[code]
    # Сожмите текущую сессию (сохраняет ключевой контекст)
    /compress
    
    # Начните новую сессию со ссылкой на старую
    hermes chat
    
    # При необходимости возобновите конкретную сессию позже
    hermes chat --continue
    
[/code]
* * *
### Проблемы с MCP[​](<#mcp-issues> "Direct link to MCP Issues")
#### MCP-сервер не подключается[​](<#mcp-server-not-connecting> "Direct link to MCP server not connecting")
**Причина:** Бинарный файл сервера не найден, неверный путь к команде или отсутствует среда выполнения.
**Решение:**
[code]
    # Убедитесь, что зависимости MCP установлены (уже включены в стандартную установку)
    cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"
    
    # Для серверов на npm убедитесь, что Node.js доступен
    node --version
    npx --version
    
    # Протестируйте сервер вручную
    npx -y @modelcontextprotocol/server-filesystem /tmp
    
[/code]
Проверьте конфигурацию MCP в `~/.hermes/config.yaml`:
[code]
    mcp_servers:
      filesystem:
        command: "npx"
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/docs"]
    
[/code]
#### Инструменты не отображаются от MCP-сервера[​](<#tools-not-showing-up-from-mcp-server> "Direct link to Tools not showing up from MCP server")
**Причина:** Сервер запущен, но обнаружение инструментов не удалось, инструменты были отфильтрованы конфигурацией или сервер не поддерживает ожидаемую возможность MCP.
**Решение:**
  * Проверьте логи шлюза/агента на наличие ошибок подключения MCP
  * Убедитесь, что сервер отвечает на RPC-метод `tools/list`
  * Проверьте настройки `tools.include`, `tools.exclude`, `tools.resources`, `tools.prompts` или `enabled` для этого сервера
  * Помните, что утилиты ресурсов/промптов регистрируются только тогда, когда сессия действительно поддерживает эти возможности
  * Используйте `/reload-mcp` после изменения конфигурации


[code]
    # Проверьте, настроены ли MCP-серверы
    hermes config show | grep -A 12 mcp_servers
    
    # Перезапустите Hermes или перезагрузите MCP после изменения конфигурации
    hermes chat
    
[/code]
См. также:
  * [MCP (Model Context Protocol)](</docs/user-guide/features/mcp>)
  * [Использование MCP с Hermes](</docs/guides/use-mcp-with-hermes>)
  * [Справочник конфигурации MCP](</docs/reference/mcp-config-reference>)


#### Ошибки таймаута MCP[​](<#mcp-timeout-errors> "Direct link to MCP timeout errors")
**Причина:** MCP-сервер отвечает слишком долго или завершился сбоем во время выполнения.
**Решение:**
  * Увеличьте таймаут в конфигурации MCP-сервера, если это поддерживается
  * Проверьте, работает ли процесс MCP-сервера
  * Для удалённых HTTP MCP-серверов проверьте сетевое подключение


warning
Если MCP-сервер завершается сбоем во время запроса, Hermes сообщит о таймауте. Проверьте логи самого сервера (не только логи Hermes), чтобы диагностировать первопричину.
* * *
## Профили[​](<#profiles> "Direct link to Profiles")
### Чем профили отличаются от простой установки HERMES_HOME?[​](<#how-do-profiles-differ-from-just-setting-hermes_home> "Direct link to How do profiles differ from just setting HERMES_HOME?")
Профили — это управляемый слой поверх `HERMES_HOME`. Вы _могли_ бы вручную устанавливать `HERMES_HOME=/some/path` перед каждой командой, но профили берут на себя всю инфраструктуру: создание структуры каталогов, генерацию псевдонимов оболочки (`hermes-work`), отслеживание активного профиля в `~/.hermes/active_profile` и автоматическую синхронизацию обновлений навыков во всех профилях. Они также интегрируются с автодополнением вкладок, так что вам не нужно запоминать пути.
### Могут ли два профиля использовать один и тот же токен бота?[​](<#can-two-profiles-share-the-same-bot-token> "Direct link to Can two profiles share the same bot token?")
Нет. Каждая платформа обмена сообщениями (Telegram, Discord и т.д.) требует исключительного доступа к токену бота. Если два профиля попытаются использовать один токен одновременно, второй шлюз не сможет подключиться. Создайте отдельного бота для каждого профиля — для Telegram обратитесь к [@BotFather](<https://t.me/BotFather>), чтобы создать дополнительных ботов.
### Делят ли профили память или сессии?[​](<#do-profiles-share-memory-or-sessions> "Direct link to Do profiles share memory or sessions?")
Нет. Каждый профиль имеет собственное хранилище памяти, базу данных сессий и каталог навыков. Они полностью изолированы. Если вы хотите начать новый профиль с существующими воспоминаниями и сессиями, используйте `hermes profile create newname --clone-all`, чтобы скопировать всё из текущего профиля.
### Что происходит при запуске `hermes update`?[​](<#what-happens-when-i-run-hermes-update> "Direct link to what-happens-when-i-run-hermes-update")
`hermes update` загружает последний код и переустанавливает зависимости **один раз** (не для каждого профиля). Затем он автоматически синхронизирует обновлённые навыки во всех профилях. Вам нужно запустить `hermes update` только один раз — он охватывает все профили на машине.
### Сколько профилей можно запустить?[​](<#how-many-profiles-can-i-run> "Direct link to How many profiles can I run?")
Жёсткого лимита нет. Каждый профиль — это просто каталог в `~/.hermes/profiles/`. Практическое ограничение зависит от места на диске и того, сколько одновременных шлюзов может выдержать ваша система (каждый шлюз — это лёгкий Python-процесс). Запуск десятков профилей — нормально; каждый неактивный профиль не использует ресурсы.
* * *
## Рабочие процессы и шаблоны[​](<#workflows--patterns> "Direct link to Workflows & Patterns")
### Использование разных моделей для разных задач (многомодельные рабочие процессы)[​](<#using-different-models-for-different-tasks-multi-model-workflows> "Direct link to Using different models for different tasks (multi-model workflows)")
**Сценарий:** Вы используете GPT-5.4 как основную модель, но Gemini или Grok лучше пишут контент для соцсетей. Вручную переключать модели каждый раз утомительно.
**Решение: Конфигурация делегирования.** Hermes может автоматически направлять сабагентов на другую модель. Настройте это в `~/.hermes/config.yaml`:
[code]
    delegation:
      model: "google/gemini-3-flash-preview"   # сабагенты используют эту модель
      provider: "openrouter"                    # провайдер для сабагентов
    
[/code]
Теперь, когда вы говорите Hermes «напиши тред для Twitter о X» и он запускает сабагент `delegate_task`, этот сабагент работает на Gemini, а не на вашей основной модели. Ваш основной разговор остаётся на GPT-5.4.
Вы также можете явно указать в промпте: _«Делегируй задачу написать посты для соцсетей о запуске нашего продукта. Используй для написания сабагента.»_ Агент воспользуется `delegate_task`, который автоматически подхватит конфигурацию делегирования.
Для разовых переключений модели без делегирования используйте `/model` в CLI:
[code]
    /model google/gemini-3-flash-preview    # переключение для этой сессии
    # ... напишите ваш контент ...
    /model openai/gpt-5.4                   # переключение обратно
    
[/code]
См. [Делегирование сабагентам](</docs/user-guide/features/delegation>) для получения дополнительной информации о том, как работает делегирование.
### Запуск нескольких агентов на одном номере WhatsApp (привязка к чату)[​](<#running-multiple-agents-on-one-whatsapp-number-per-chat-binding> "Direct link to Running multiple agents on one WhatsApp number (per-chat binding)")
**Сценарий:** В OpenClaw у вас было несколько независимых агентов, привязанных к определённым чатам WhatsApp — один для семейного списка покупок, другой для личного чата. Может ли Hermes сделать это?
**Текущее ограничение:** Каждый профиль Hermes требует собственного номера/сессии WhatsApp. Вы не можете привязать несколько профилей к разным чатам на одном номере WhatsApp — мост WhatsApp (Baileys) использует одну аутентифицированную сессию на номер.
**Обходные пути:**
  1. **Используйте один профиль с переключением личности.** Создайте разные контекстные файлы `AGENTS.md` или используйте команду `/personality`, чтобы менять поведение для каждого чата. Агент видит, в каком чате находится, и может адаптироваться.
  2. **Используйте cron-задачи для специализированных задач.** Для трекера списка покупок настройте cron-задачу, которая отслеживает определённый чат и управляет списком — отдельный агент не нужен.
  3. **Используйте отдельные номера.** Если вам нужны действительно независимые агенты, свяжите каждый профиль с собственным номером WhatsApp. Виртуальные номера от сервисов типа Google Voice подойдут для этого.
  4. **Используйте Telegram или Discord.** Эти платформы поддерживают привязку к чату более естественно — каждая группа Telegram или канал Discord получает свою сессию, и вы можете запускать несколько токенов ботов (один на профиль) в одной учётной записи.


См. [Профили](</docs/user-guide/profiles>) и [Настройка WhatsApp](</docs/user-guide/messaging/whatsapp>) для подробностей.
### Управление отображением в Telegram (скрытие логов и рассуждений)[​](<#controlling-what-shows-up-in-telegram-hiding-logs-and-reasoning> "Direct link to Controlling what shows up in Telegram (hiding logs and reasoning)")
**Сценарий:** В Telegram отображаются логи выполнения шлюза, рассуждения Hermes и детали вызовов инструментов вместо финального ответа.
**Решение:** Настройка `display.tool_progress` в `config.yaml` управляет тем, сколько активности инструментов показывается:
[code]
    display:
      tool_progress: "off"   # варианты: off, new, all, verbose
    
[/code]
  * **`off`** — Только финальный ответ. Ни вызовов инструментов, ни рассуждений, ни логов.
  * **`new`** — Показывает новые вызовы инструментов по мере их выполнения (краткие однострочники).
  * **`all`** — Показывает всю активность инструментов, включая результаты.
  * **`verbose`** — Полная детализация, включая аргументы и выводы инструментов.


Для платформ обмена сообщениями обычно нужно `off` или `new`. После редактирования `config.yaml` перезапустите шлюз, чтобы изменения вступили в силу.
Вы также можете переключать это для каждой сессии командой `/verbose` (если включено):
[code]
    display:
      tool_progress_command: true   # включает /verbose в шлюзе
    
[/code]
### Управление навыками в Telegram (лимит слэш-команд)[​](<#managing-skills-on-telegram-slash-command-limit> "Direct link to Managing skills on Telegram (slash command limit)")
**Сценарий:** В Telegram есть лимит в 100 слэш-команд, и ваши навыки превышают его. Вы хотите отключить ненужные навыки в Telegram, но настройки `hermes skills config` не вступают в силу.
**Решение:** Используйте `hermes skills config`, чтобы отключить навыки для отдельных платформ. Это записывается в `config.yaml`:
[code]
    skills:
      disabled: []                    # глобально отключённые навыки
      platform_disabled:
        telegram: [skill-a, skill-b]  # отключены только в Telegram
    
[/code]
После изменения **перезапустите шлюз** (`hermes gateway restart` или завершите и запустите заново). Меню команд Telegram-бота перестраивается при запуске.
tip
Навыки с очень длинными описаниями обрезаются до 40 символов в меню Telegram, чтобы оставаться в пределах лимита размера полезной нагрузки. Если навыки не отображаются, это может быть проблемой общего размера полезной нагрузки, а не лимита в 100 команд — отключение неиспользуемых навыков помогает в обоих случаях.
### Общие сессии в тредах (несколько пользователей, один разговор)[​](<#shared-thread-sessions-multiple-users-one-conversation> "Direct link to Shared thread sessions (multiple users, one conversation)")
**Сценарий:** У вас есть тред в Telegram или Discord, где несколько человек упоминают бота. Вы хотите, чтобы все упоминания в этом треде были частью одного общего разговора, а не отдельных сессий для каждого пользователя.
**Текущее поведение:** Hermes создаёт сессии по ID пользователя на большинстве платформ, поэтому каждый человек получает свой контекст разговора. Это сделано намеренно для конфиденциальности и изоляции контекста.
**Обходные пути:**
  1. **Используйте Slack.** Сессии в Slack привязаны к нити обсуждения, а не к пользователю. Несколько пользователей в одной нити разделяют один разговор — именно то поведение, которое вы описываете. Это наиболее естественное решение.
  2. **Используйте групповой чат с одним пользователем.** Если один человек является назначенным «оператором», который передаёт вопросы, сессия остаётся единой. Остальные могут читать.
  3. **Используйте канал Discord.** Сессии в Discord привязаны к каналу, поэтому все пользователи в одном канале разделяют контекст. Используйте выделенный канал для общего разговора.


### Экспорт Hermes на другую машину[​](<#exporting-hermes-to-another-machine> "Direct link to Exporting Hermes to another machine")
**Сценарий:** Вы накопили навыки, cron-задачи и воспоминания на одной машине и хотите перенести всё на новый выделенный Linux-сервер.
**Решение:**
  1. Установите Hermes Agent на новой машине:
[code] curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
         
[/code]
  2. На **исходной машине** создайте полную резервную копию:
[code] hermes backup
         
[/code]
Это создаёт zip-архив всего каталога `~/.hermes/` — конфигурации, API-ключей, воспоминаний, навыков, сессий и профилей — сохранённый в вашей домашней директории как `~/hermes-backup-<timestamp>.zip`.
  3. Скопируйте архив на новую машину и импортируйте его:
[code] # На исходной машине
         scp ~/hermes-backup-<timestamp>.zip newmachine:~/
         
         # На новой машине
         hermes import ~/hermes-backup-<timestamp>.zip
         
[/code]
  4. На новой машине запустите `hermes setup`, чтобы убедиться, что API-ключи и конфигурация провайдера работают.


### Перенос одного профиля на другую машину[​](<#moving-a-single-profile-to-another-machine> "Direct link to Moving a single profile to another machine")
**Сценарий:** Вы хотите перенести или поделиться одним определённым профилем — не всей установкой.
[code]
    # На исходной машине
    hermes profile export work ./work-backup.tar.gz
    
    # Скопируйте файл на целевую машину, затем:
    hermes profile import ./work-backup.tar.gz work
    
[/code]
Импортированный профиль будет содержать все конфиги, воспоминания, сессии и навыки из экспорта. Возможно, вам потребуется обновить пути или повторно аутентифицироваться у провайдеров, если на новой машине другая настройка.
### `hermes backup` vs `hermes profile export`[​](<#hermes-backup-vs-hermes-profile-export> "Direct link to hermes-backup-vs-hermes-profile-export")
Функция| `hermes backup`| `hermes profile export`
---|---|---
**Сценарий**| **Полная миграция машины**| **Перенос/передача определённого профиля**
**Область**|  Глобальная (весь каталог `~/.hermes`)| Локальная (каталог одного профиля)
**Включает**|  Все профили, глобальную конфигурацию, API-ключи, сессии| Один профиль: SOUL.md, воспоминания, сессии, навыки
**Учётные данные**| **Включены** (`.env` и `auth.json`)| **Исключены** (удалены для безопасной передачи)
**Формат**| `.zip`| `.tar.gz`
**Ручной способ (rsync):** Если вы предпочитаете копировать файлы напрямую, исключите репозиторий кода:
[code]
    rsync -av --exclude='hermes-agent' ~/.hermes/ newmachine:~/.hermes/
    
[/code]
tip
`hermes backup` создаёт консистентный снимок даже при активной работе Hermes. Восстановленный архив исключает локальные для машины файлы времени выполнения, такие как `gateway.pid` и `cron.pid`.
### Отказано в доступе при перезагрузке оболочки после установки[​](<#permission-denied-when-reloading-shell-after-install> "Direct link to Permission denied when reloading shell after install")
**Сценарий:** После запуска установщика Hermes `source ~/.zshrc` выдаёт ошибку отказа в доступе.
**Причина:** Обычно это происходит, когда `~/.zshrc` (или `~/.bashrc`) имеет неверные права доступа к файлу, или когда установщик не смог корректно записать в него. Это не специфическая проблема Hermes — это проблема прав доступа к конфигу оболочки.
**Решение:**
[code]
    # Проверьте права доступа
    ls -la ~/.zshrc
    
    # Исправьте, если необходимо (должно быть -rw-r--r-- или 644)
    chmod 644 ~/.zshrc
    
    # Затем перезагрузите
    source ~/.zshrc
    
    # Или просто откройте новое окно терминала — оно подхватывает изменения PATH автоматически
    
[/code]
Если установщик добавил строку PATH, но права доступа неправильные, вы можете добавить её вручную:
[code]
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    
[/code]
### Ошибка 400 при первом запуске агента[​](<#error-400-on-first-agent-run> "Direct link to Error 400 on first agent run")
**Сценарий:** Установка завершается успешно, но первая попытка чата завершается ошибкой HTTP 400.
**Причина:** Обычно несоответствие имени модели — настроенная модель не существует у вашего провайдера, или API-ключ не имеет к ней доступа.
**Решение:**
[code]
    # Проверьте, какая модель и провайдер настроены
    hermes config show | head -20
    
    # Повторно запустите выбор модели
    hermes model
    
    # Или протестируйте с заведомо рабочей моделью
    hermes chat -q "hello" --model anthropic/claude-opus-4.7
    
[/code]
Если вы используете OpenRouter, убедитесь, что на вашем API-ключе есть средства. Ошибка 400 от OpenRouter часто означает, что модель требует платного тарифа или в ID модели есть опечатка.
* * *
## Всё ещё застряли?[​](<#still-stuck> "Direct link to Still Stuck?")
Если ваша проблема не описана здесь:
  1. **Поищите в существующих issue:** [GitHub Issues](<https://github.com/NousResearch/hermes-agent/issues>)
  2. **Спросите сообщество:** [Nous Research Discord](<https://discord.gg/nousresearch>)
  3. **Сообщите об ошибке:** Укажите вашу ОС, версию Python (`python3 --version`), версию Hermes (`hermes --version`) и полный текст ошибки


  * [Часто задаваемые вопросы](<#frequently-asked-questions>)
    * [Какие LLM-провайдеры работают с Hermes?](<#what-llm-providers-work-with-hermes>)
    * [Работает ли на Windows?](<#does-it-work-on-windows>)
    * [Я запускаю Hermes в WSL2. Как лучше всего управлять обычным Windows Chrome?](<#i-run-hermes-in-wsl2-whats-the-best-way-to-control-my-normal-windows-chrome>)
    * [Работает ли на Android / Termux?](<#does-it-work-on-android--termux>)
    * [Передаются ли мои данные куда-либо?](<#is-my-data-sent-anywhere>)
    * [Можно ли использовать офлайн / с локальными моделями?](<#can-i-use-it-offline--with-local-models>)
    * [Сколько это стоит?](<#how-much-does-it-cost>)
    * [Могут ли несколько человек использовать один экземпляр?](<#can-multiple-people-use-one-instance>)
    * [В чём разница между памятью (memory) и навыками (skills)?](<#whats-the-difference-between-memory-and-skills>)
    * [Можно ли использовать Hermes в своём Python-проекте?](<#can-i-use-it-in-my-own-python-project>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Проблемы установки](<#installation-issues>)
    * [Проблемы с провайдерами и моделями](<#provider--model-issues>)
    * [Проблемы с терминалом](<#terminal-issues>)
    * [Проблемы с обменом сообщениями](<#messaging-issues>)
    * [Проблемы с производительностью](<#performance-issues>)
    * [Проблемы с MCP](<#mcp-issues>)
  * [Профили](<#profiles>)
    * [Чем профили отличаются от простой установки HERMES_HOME?](<#how-do-profiles-differ-from-just-setting-hermes_home>)
    * [Могут ли два профиля использовать один и тот же токен бота?](<#can-two-profiles-share-the-same-bot-token>)
    * [Делят ли профили память или сессии?](<#do-profiles-share-memory-or-sessions>)
    * [Что происходит при запуске `hermes update`?](<#what-happens-when-i-run-hermes-update>)
    * [Сколько профилей можно запустить?](<#how-many-profiles-can-i-run>)
  * [Рабочие процессы и шаблоны](<#workflows--patterns>)
    * [Использование разных моделей для разных задач (многомодельные рабочие процессы)](<#using-different-models-for-different-tasks-multi-model-workflows>)
    * [Запуск нескольких агентов на одном номере WhatsApp (привязка к чату)](<#running-multiple-agents-on-one-whatsapp-number-per-chat-binding>)
    * [Управление отображением в Telegram (скрытие логов и рассуждений)](<#controlling-what-shows-up-in-telegram-hiding-logs-and-reasoning>)
    * [Управление навыками в Telegram (лимит слэш-команд)](<#managing-skills-on-telegram-slash-command-limit>)
    * [Общие сессии в тредах (несколько пользователей, один разговор)](<#shared-thread-sessions-multiple-users-one-conversation>)
    * [Экспорт Hermes на другую машину](<#exporting-hermes-to-another-machine>)
    * [Перенос одного профиля на другую машину](<#moving-a-single-profile-to-another-machine>)
    * [`hermes backup` vs `hermes profile export`](<#hermes-backup-vs-hermes-profile-export>)
    * [Отказано в доступе при перезагрузке оболочки после установки](<#permission-denied-when-reloading-shell-after-install>)
    * [Ошибка 400 при первом запуске агента](<#error-400-on-first-agent-run>)
  * [Всё ещё застряли?](<#still-stuck>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/faq -->
