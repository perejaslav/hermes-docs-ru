На этой странице
Hermes Agent распространяется как Nix-флейк с тремя уровнями интеграции:
Уровень| Для кого| Что вы получаете  
---|---|---  
**`nix run` / `nix profile install`**| Любой пользователь Nix (macOS, Linux)| Предварительно собранный бинарник со всеми зависимостями — далее используется стандартный CLI-процесс  
**Модуль NixOS (нативный)**| Серверные развёртывания NixOS| Декларативная конфигурация, усиленный systemd-сервис, управляемые секреты  
**Модуль NixOS (контейнер)**| Агенты, которым нужна самомодификация| Всё вышеперечисленное, плюс постоянный Ubuntu-контейнер, где агент может выполнять `apt`/`pip`/`npm install`  
Чем отличается от стандартной установки
Установщик `curl | bash` сам управляет Python, Node и зависимостями. Nix-флейк заменяет всё это — каждая Python-зависимость является Nix-деривацией, собранной с помощью [uv2nix](<https://github.com/pyproject-nix/uv2nix>), а инструменты времени выполнения (Node.js, git, ripgrep, ffmpeg) встроены в PATH бинарника. Нет runtime pip, нет активации venv, нет `npm install`.
**Для пользователей не-NixOS** это меняет только шаг установки. Всё остальное (`hermes setup`, `hermes gateway install`, редактирование конфигурации) работает идентично стандартной установке.
**Для пользователей модуля NixOS** весь жизненный цикл отличается: конфигурация находится в `configuration.nix`, секреты передаются через sops-nix/agenix, сервис является systemd-юнитом, а CLI-команды конфигурации заблокированы. Вы управляете hermes так же, как любым другим NixOS-сервисом.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  * **Nix с включёнными флейками** — рекомендуется [Determinate Nix](<https://install.determinate.systems>) (включает флейки по умолчанию)
  * **API-ключи** для сервисов, которые вы планируете использовать (как минимум: ключ OpenRouter или Anthropic)


* * *
## Быстрый старт (любой пользователь Nix)[​](<#quick-start-any-nix-user> "Прямая ссылка на Быстрый старт (любой пользователь Nix)")
Клонирование не требуется. Nix загружает, собирает и запускает всё:
[code] 
    # Запустить напрямую (сборка при первом использовании, далее кэшируется)  
    nix run github:NousResearch/hermes-agent -- setup  
    nix run github:NousResearch/hermes-agent -- chat  
      
    # Или установить постоянно  
    nix profile install github:NousResearch/hermes-agent  
    hermes setup  
    hermes chat  
    
[/code]
После `nix profile install` команды `hermes`, `hermes-agent` и `hermes-acp` оказываются в вашем PATH. Отсюда процесс идентичен [стандартной установке](</docs/getting-started/installation>) — `hermes setup` проведёт вас через выбор провайдера, `hermes gateway install` настраивает launchd (macOS) или systemd-сервис пользователя, а конфигурация хранится в `~/.hermes/`.
**Сборка из локального клона**
[code]
     git clone https://github.com/NousResearch/hermes-agent.git  
    cd hermes-agent  
    nix build  
    ./result/bin/hermes setup  
    
[/code]
* * *
## Модуль NixOS[​](<#nixos-module> "Прямая ссылка на Модуль NixOS")
Флейк экспортирует `nixosModules.default` — полноценный модуль NixOS-сервиса, который декларативно управляет созданием пользователя, директориями, генерацией конфигурации, секретами, документами и жизненным циклом сервиса.
note
Этот модуль требует NixOS. Для систем не-NixOS (macOS, другие дистрибутивы Linux) используйте `nix profile install` и стандартный CLI-процесс, описанный выше.
### Добавление флейк-входа[​](<#add-the-flake-input> "Прямая ссылка на Добавление флейк-входа")
[code] 
    # /etc/nixos/flake.nix (или ваш системный флейк)  
    {  
      inputs = {  
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";  
        hermes-agent.url = "github:NousResearch/hermes-agent";  
      };  
      
      outputs = { nixpkgs, hermes-agent, ... }: {  
        nixosConfigurations.your-host = nixpkgs.lib.nixosSystem {  
          system = "x86_64-linux";  
          modules = [  
            hermes-agent.nixosModules.default  
            ./configuration.nix  
          ];  
        };  
      };  
    }  
    
[/code]
### Минимальная конфигурация[​](<#minimal-configuration> "Прямая ссылка на Минимальная конфигурация")
[code] 
    # configuration.nix  
    { config, ... }: {  
      services.hermes-agent = {  
        enable = true;  
        settings.model.default = "anthropic/claude-sonnet-4";  
        environmentFiles = [ config.sops.secrets."hermes-env".path ];  
        addToSystemPackages = true;  
      };  
    }  
    
[/code]
Вот и всё. `nixos-rebuild switch` создаёт пользователя `hermes`, генерирует `config.yaml`, подключает секреты и запускает шлюз — долгоживущий сервис, который соединяет агента с платформами обмена сообщениями (Telegram, Discord и т.д.) и слушает входящие сообщения.
Секреты обязательны
Строка `environmentFiles` выше предполагает, что у вас настроен [sops-nix](<https://github.com/Mic92/sops-nix>) или [agenix](<https://github.com/ryantm/agenix>). Файл должен содержать как минимум один ключ LLM-провайдера (например, `OPENROUTER_API_KEY=sk-or-...`). Полную настройку см. в разделе [Управление секретами](<#secrets-management>). Если у вас ещё нет менеджера секретов, можете начать с обычного файла — просто убедитесь, что он не читается всеми:
[code]
    echo "OPENROUTER_API_KEY=sk-or-your-key" | sudo install -m 0600 -o hermes /dev/stdin /var/lib/hermes/env  
    
[/code]
[code]
    services.hermes-agent.environmentFiles = [ "/var/lib/hermes/env" ];  
    
[/code]
addToSystemPackages
Установка `addToSystemPackages = true` делает две вещи: добавляет CLI `hermes` в системный PATH **и** устанавливает `HERMES_HOME` общесистемно, чтобы интерактивный CLI разделял состояние (сессии, навыки, cron) с сервисом шлюза. Без этого запуск `hermes` в вашей оболочке создаёт отдельную директорию `~/.hermes/`.
### CLI с поддержкой контейнера[​](<#container-aware-cli> "Прямая ссылка на CLI с поддержкой контейнера")
info
Когда `container.enable = true` и `addToSystemPackages = true`, **каждая** команда `hermes` на хосте автоматически направляется в управляемый контейнер. Это означает, что ваша интерактивная CLI-сессия работает в том же окружении, что и сервис шлюза — с доступом ко всем установленным в контейнере пакетам и инструментам.
  * Маршрутизация прозрачна: `hermes chat`, `hermes sessions list`, `hermes version` и т.д. все выполняются внутри контейнера под капотом
  * Все CLI-флаги передаются как есть
  * Если контейнер не запущен, CLI делает несколько попыток (5 с со спиннером для интерактивного использования, 10 с беззвучно для скриптов), затем завершается с понятной ошибкой — без беззвучного отката
  * Для разработчиков, работающих над кодовой базой hermes, установите `HERMES_DEV=1`, чтобы обойти маршрутизацию в контейнер и запускать локальную копию напрямую


Установите `container.hostUsers`, чтобы создать символическую ссылку `~/.hermes` на директорию состояния сервиса, тогда CLI на хосте и контейнер будут совместно использовать сессии, конфигурацию и воспоминания:
[code]
    services.hermes-agent = {  
      container.enable = true;  
      container.hostUsers = [ "your-username" ];  
      addToSystemPackages = true;  
    };  
    
[/code]
Пользователи, перечисленные в `hostUsers`, автоматически добавляются в группу `hermes` для доступа к файлам.
**Пользователи Podman:** Сервис NixOS запускает контейнер от root. Пользователи Docker получают доступ через сокет группы `docker`, но rootful-контейнеры Podman требуют sudo. Предоставьте sudo без пароля для вашей контейнерной среды выполнения:
[code]
    security.sudo.extraRules = [{  
      users = [ "your-username" ];  
      commands = [{  
        command = "/run/current-system/sw/bin/podman";  
        options = [ "NOPASSWD" ];  
      }];  
    }];  
    
[/code]
CLI автоматически определяет, когда нужен sudo, и использует его прозрачно. Без этого вам придётся запускать `sudo hermes chat` вручную.
### Проверка работоспособности[​](<#verify-it-works> "Прямая ссылка на Проверка работоспособности")
После `nixos-rebuild switch` проверьте, что сервис запущен:
[code] 
    # Проверка статуса сервиса  
    systemctl status hermes-agent  
      
    # Просмотр логов (Ctrl+C для остановки)  
    journalctl -u hermes-agent -f  
      
    # Если addToSystemPackages true, протестируйте CLI  
    hermes version  
    hermes config       # показывает сгенерированную конфигурацию  
    
[/code]
### Выбор режима развёртывания[​](<#choosing-a-deployment-mode> "Прямая ссылка на Выбор режима развёртывания")
Модуль поддерживает два режима, управляемых через `container.enable`:
| **Нативный** (по умолчанию)| **Контейнерный**  
---|---|---  
Как работает| Усиленный systemd-сервис на хосте| Постоянный Ubuntu-контейнер с bind-mount `/nix/store`  
Безопасность| `NoNewPrivileges`, `ProtectSystem=strict`, `PrivateTmp`| Изоляция контейнера, запуск от непривилегированного пользователя внутри  
Агент может самостоятельно устанавливать пакеты| Нет — только инструменты из Nix-пути PATH| Да — `apt`, `pip`, `npm` установки сохраняются после перезапуска  
Поверхность конфигурации| Та же| Та же  
Когда выбирать| Стандартные развёртывания, максимальная безопасность, воспроизводимость| Агенту требуется установка пакетов во время выполнения, изменяемое окружение, экспериментальные инструменты  
Чтобы включить контейнерный режим, добавьте одну строку:
[code] 
    {  
      services.hermes-agent = {  
        enable = true;  
        container.enable = true;  
        # ... остальная конфигурация идентична  
      };  
    }  
    
[/code]
info
Контейнерный режим автоматически включает `virtualisation.docker.enable` через `mkDefault`. Если вы используете Podman, установите `container.backend = "podman"` и `virtualisation.docker.enable = false`.
* * *
## Конфигурация[​](<#configuration> "Прямая ссылка на Конфигурация")
### Декларативные настройки[​](<#declarative-settings> "Прямая ссылка на Декларативные настройки")
Опция `settings` принимает произвольный attrset, который преобразуется в `config.yaml`. Она поддерживает глубокое слияние (deep merge) между несколькими определениями модуля (через `lib.recursiveUpdate`), поэтому вы можете разделять конфигурацию по файлам:
[code] 
    # base.nix  
    services.hermes-agent.settings = {  
      model.default = "anthropic/claude-sonnet-4";  
      toolsets = [ "all" ];  
      terminal = { backend = "local"; timeout = 180; };  
    };  
      
    # personality.nix  
    services.hermes-agent.settings = {  
      display = { compact = false; personality = "kawaii"; };  
      memory = { memory_enabled = true; user_profile_enabled = true; };  
    };  
    
[/code]
Оба объединяются глубоким слиянием на этапе оценки. Ключи, объявленные в Nix, всегда имеют приоритет над ключами в существующем `config.yaml` на диске, но **ключи, добавленные пользователем, которые Nix не затрагивает, сохраняются**. Это означает, что если агент или ручное редактирование добавляет ключи вроде `skills.disabled` или `streaming.enabled`, они переживают `nixos-rebuild switch`.
Именование моделей
`settings.model.default` использует идентификатор модели, который ожидает ваш провайдер. С [OpenRouter](<https://openrouter.ai>) (по умолчанию) они выглядят как `"anthropic/claude-sonnet-4"` или `"google/gemini-3-flash"`. Если вы используете провайдера напрямую (Anthropic, OpenAI), установите `settings.model.base_url` для указания на их API и используйте их родные идентификаторы моделей (например, `"claude-sonnet-4-20250514"`). Когда `base_url` не задан, Hermes по умолчанию использует OpenRouter.
Поиск доступных ключей конфигурации
Выполните `nix build .#configKeys && cat result`, чтобы увидеть все конечные ключи конфигурации, извлечённые из `DEFAULT_CONFIG` в Python. Вы можете вставить существующий `config.yaml` в attrset `settings` — структура соответствует 1:1.
**Полный пример: все часто настраиваемые параметры**
[code]
    { config, ... }: {  
      services.hermes-agent = {  
        enable = true;  
        container.enable = true;  
      
        # ── Модель ──────────────────────────────────────────────────────────  
        settings = {  
          model = {  
            base_url = "https://openrouter.ai/api/v1";  
            default = "anthropic/claude-opus-4.6";  
          };  
          toolsets = [ "all" ];  
          max_turns = 100;  
          terminal = { backend = "local"; cwd = "."; timeout = 180; };  
          compression = {  
            enabled = true;  
            threshold = 0.85;  
            summary_model = "google/gemini-3-flash-preview";  
          };  
          memory = { memory_enabled = true; user_profile_enabled = true; };  
          display = { compact = false; personality = "kawaii"; };  
          agent = { max_turns = 60; verbose = false; };  
        };  
      
        # ── Секреты ────────────────────────────────────────────────────────  
        environmentFiles = [ config.sops.secrets."hermes-env".path ];  
      
        # ── Документы ──────────────────────────────────────────────────────  
        documents = {  
          "USER.md" = ./documents/USER.md;  
        };  
      
        # ── MCP-серверы ────────────────────────────────────────────────────  
        mcpServers.filesystem = {  
          command = "npx";  
          args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];  
        };  
      
        # ── Параметры контейнера ───────────────────────────────────────────  
        container = {  
          image = "ubuntu:24.04";  
          backend = "docker";  
          hostUsers = [ "your-username" ];  
          extraVolumes = [ "/home/user/projects:/projects:rw" ];  
          extraOptions = [ "--gpus" "all" ];  
        };  
      
        # ── Тюнинг сервиса ─────────────────────────────────────────────────  
        addToSystemPackages = true;  
        extraArgs = [ "--verbose" ];  
        restart = "always";  
        restartSec = 5;  
      };  
    }  
    
[/code]
### Запасной вариант: собственная конфигурация[​](<#escape-hatch-bring-your-own-config> "Прямая ссылка на Запасной вариант: собственная конфигурация")
Если вы предпочитаете управлять `config.yaml` полностью вне Nix, используйте `configFile`:
[code] 
    services.hermes-agent.configFile = /etc/hermes/config.yaml;  
    
[/code]
Это полностью обходит `settings` — никакого слияния, никакой генерации. Файл копируется как есть в `$HERMES_HOME/config.yaml` при каждой активации.
### Шпаргалка по настройке[​](<#customization-cheatsheet> "Прямая ссылка на Шпаргалка по настройке")
Быстрый справочник по самым частым вещам, которые пользователи Nix хотят настроить:
Я хочу...| Опция| Пример  
---|---|---  
Изменить LLM-модель| `settings.model.default`| `"anthropic/claude-sonnet-4"`  
Использовать другую конечную точку провайдера| `settings.model.base_url`| `"https://openrouter.ai/api/v1"`  
Добавить API-ключи| `environmentFiles`| `[ config.sops.secrets."hermes-env".path ]`  
Наделить агента личностью| `${services.hermes-agent.stateDir}/.hermes/SOUL.md`| управляйте файлом напрямую  
Добавить MCP-серверы инструментов| `mcpServers.<name>`| См. [MCP-серверы](<#mcp-servers>)  
Смонтировать хостовые директории в контейнер| `container.extraVolumes`| `[ "/data:/data:rw" ]`  
Передать GPU в контейнер| `container.extraOptions`| `[ "--gpus" "all" ]`  
Использовать Podman вместо Docker| `container.backend`| `"podman"`  
Разделять состояние между хостовым CLI и контейнером| `container.hostUsers`| `[ "sidbin" ]`  
Сделать дополнительные инструменты доступными агенту| `extraPackages`| `[ pkgs.pandoc pkgs.imagemagick ]`  
Использовать собственный базовый образ| `container.image`| `"ubuntu:24.04"`  
Переопределить пакет hermes| `package`| `inputs.hermes-agent.packages.${system}.default.override { ... }`  
Изменить директорию состояния| `stateDir`| `"/opt/hermes"`  
Установить рабочую директорию агента| `workingDirectory`| `"/home/user/projects"`  
* * *
## Управление секретами[​](<#secrets-management> "Прямая ссылка на Управление секретами")
Никогда не помещайте API-ключи в `settings` или `environment`
Значения в Nix-выражениях попадают в `/nix/store`, который доступен для чтения всем. Всегда используйте `environmentFiles` с менеджером секретов.
И `environment` (несекретные переменные), и `environmentFiles` (файлы с секретами) объединяются в `$HERMES_HOME/.env` при активации (`nixos-rebuild switch`). Hermes читает этот файл при каждом запуске, поэтому изменения вступают в силу после `systemctl restart hermes-agent` — пересоздание контейнера не требуется.
### sops-nix[​](<#sops-nix> "Прямая ссылка на sops-nix")
[code] 
    {  
      sops = {  
        defaultSopsFile = ./secrets/hermes.yaml;  
        age.keyFile = "/home/user/.config/sops/age/keys.txt";  
        secrets."hermes-env" = { format = "yaml"; };  
      };  
      
      services.hermes-agent.environmentFiles = [  
        config.sops.secrets."hermes-env".path  
      ];  
    }  
    
[/code]
Файл секретов содержит пары ключ-значение:
[code] 
    # secrets/hermes.yaml (зашифрован с помощью sops)  
    hermes-env: |  
        OPENROUTER_API_KEY=sk-or-...  
        TELEGRAM_BOT_TOKEN=123456:ABC...  
        ANTHROPIC_API_KEY=sk-ant-...  
    
[/code]
### agenix[​](<#agenix> "Прямая ссылка на agenix")
[code] 
    {  
      age.secrets.hermes-env.file = ./secrets/hermes-env.age;  
      
      services.hermes-agent.environmentFiles = [  
        config.age.secrets.hermes-env.path  
      ];  
    }  
    
[/code]
### OAuth / Предзагрузка аутентификации[​](<#oauth--auth-seeding> "Прямая ссылка на OAuth / Предзагрузка аутентификации")
Для платформ, требующих OAuth (например, Discord), используйте `authFile` для предзагрузки учётных данных при первом развёртывании:
[code] 
    {  
      services.hermes-agent = {  
        authFile = config.sops.secrets."hermes/auth.json".path;  
        # authFileForceOverwrite = true;  # перезаписывать при каждой активации  
      };  
    }  
    
[/code]
Файл копируется только если `auth.json` ещё не существует (если только `authFileForceOverwrite = true`). Обновления OAuth-токенов во время выполнения записываются в директорию состояния и сохраняются при пересборках.
* * *
## Документы[​](<#documents> "Прямая ссылка на Документы")
Опция `documents` устанавливает файлы в рабочую директорию агента (значение `workingDirectory`, которую агент читает как своё рабочее пространство). Hermes ищет определённые имена файлов по соглашению:
  * **`USER.md`** — контекст о пользователе, с которым взаимодействует агент.
  * Любые другие файлы, которые вы сюда поместите, видны агенту как файлы рабочего пространства.


Файл личности агента находится отдельно: Hermes загружает свой основной `SOUL.md` из `$HERMES_HOME/SOUL.md`, который в модуле NixOS находится по пути `${services.hermes-agent.stateDir}/.hermes/SOUL.md`. Помещение `SOUL.md` в `documents` создаст только файл рабочего пространства и не заменит основной файл личности.
[code] 
    {  
      services.hermes-agent.documents = {  
        "USER.md" = ./documents/USER.md;  # ссылка на путь, копируется из Nix store  
      };  
    }  
    
[/code]
Значениями могут быть строки напрямую или ссылки на пути. Файлы устанавливаются при каждом `nixos-rebuild switch`.
* * *
## MCP-серверы[​](<#mcp-servers> "Прямая ссылка на MCP-серверы")
Опция `mcpServers` декларативно настраивает [MCP-серверы (Model Context Protocol)](<https://modelcontextprotocol.io>). Каждый сервер использует либо **stdio** (локальная команда), либо **HTTP** (удалённый URL) транспорт.
### Stdio-транспорт (локальные серверы)[​](<#stdio-transport-local-servers> "Прямая ссылка на Stdio-транспорт (локальные серверы)")
[code] 
    {  
      services.hermes-agent.mcpServers = {  
        filesystem = {  
          command = "npx";  
          args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];  
        };  
        github = {  
          command = "npx";  
          args = [ "-y" "@modelcontextprotocol/server-github" ];  
          env.GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_TOKEN}"; # извлекается из .env  
        };  
      };  
    }  
    
[/code]
tip
Переменные окружения в значениях `env` извлекаются из `$HERMES_HOME/.env` во время выполнения. Используйте `environmentFiles` для внедрения секретов — никогда не помещайте токены напрямую в Nix-конфигурацию.
### HTTP-транспорт (удалённые серверы)[​](<#http-transport-remote-servers> "Прямая ссылка на HTTP-транспорт (удалённые серверы)")
[code] 
    {  
      services.hermes-agent.mcpServers.remote-api = {  
        url = "https://mcp.example.com/v1/mcp";  
        headers.Authorization = "Bearer ${MCP_REMOTE_API_KEY}";  
        timeout = 180;  
      };  
    }  
    
[/code]
### HTTP-транспорт с OAuth[​](<#http-transport-with-oauth> "Прямая ссылка на HTTP-транспорт с OAuth")
Установите `auth = "oauth"` для серверов, использующих OAuth 2.1. Hermes реализует полный PKCE-процесс — обнаружение метаданных, динамическую регистрацию клиента, обмен токенами и автоматическое обновление.
[code] 
    {  
      services.hermes-agent.mcpServers.my-oauth-server = {  
        url = "https://mcp.example.com/mcp";  
        auth = "oauth";  
      };  
    }  
    
[/code]
Токены хранятся в `$HERMES_HOME/mcp-tokens/<имя-сервера>.json` и сохраняются между перезапусками и пересборками.
**Первоначальная OAuth-авторизация на серверах без головного интерфейса**
Первая OAuth-авторизация требует браузерного процесса согласия. В развёртывании без головного интерфейса Hermes выводит URL авторизации в stdout/логи вместо открытия браузера.
**Вариант А: Интерактивная начальная настройка** — выполните процесс однократно через `docker exec` (контейнер) или `sudo -u hermes` (нативный режим):
[code]
    # Контейнерный режим  
    docker exec -it hermes-agent \  
      hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth  
      
    # Нативный режим  
    sudo -u hermes HERMES_HOME=/var/lib/hermes/.hermes \  
      hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth  
    
[/code]
Контейнер использует `--network=host`, поэтому слушатель OAuth-обратного вызова на `127.0.0.1` доступен из браузера на хосте.
**Вариант Б: Предзагрузка токенов** — выполните процесс на рабочей станции, затем скопируйте токены:
[code]
    hermes mcp add my-oauth-server --url https://mcp.example.com/mcp --auth oauth  
    scp ~/.hermes/mcp-tokens/my-oauth-server{,.client}.json \  
        server:/var/lib/hermes/.hermes/mcp-tokens/  
    # Убедитесь: chown hermes:hermes, chmod 0600  
    
[/code]
### Сэмплинг (запросы LLM, инициированные сервером)[​](<#sampling-server-initiated-llm-requests> "Прямая ссылка на Сэмплинг (запросы LLM, инициированные сервером)")
Некоторые MCP-серверы могут запрашивать завершения LLM у агента:
[code] 
    {  
      services.hermes-agent.mcpServers.analysis = {  
        command = "npx";  
        args = [ "-y" "analysis-server" ];  
        sampling = {  
          enabled = true;  
          model = "google/gemini-3-flash";  
          max_tokens_cap = 4096;  
          timeout = 30;  
          max_rpm = 10;  
        };  
      };  
    }  
    
[/code]
* * *
## Управляемый режим[​](<#managed-mode> "Прямая ссылка на Управляемый режим")
Когда hermes работает через модуль NixOS, следующие CLI-команды **заблокированы** с описательной ошибкой, указывающей на `configuration.nix`:
Заблокированная команда| Почему  
---|---  
`hermes setup`| Конфигурация декларативна — редактируйте `settings` в вашей Nix-конфигурации  
`hermes config edit`| Конфигурация генерируется из `settings`  
`hermes config set <key> <value>`| Конфигурация генерируется из `settings`  
`hermes gateway install`| systemd-сервис управляется NixOS  
`hermes gateway uninstall`| systemd-сервис управляется NixOS  
Это предотвращает расхождение между тем, что объявляет Nix, и тем, что находится на диске. Обнаружение использует два сигнала:
  1. **Переменная окружения `HERMES_MANAGED=true`** — устанавливается systemd-сервисом, видна процессу шлюза
  2. **Файл-маркер `.managed`** в `HERMES_HOME` — устанавливается скриптом активации, виден интерактивным оболочкам (например, `docker exec -it hermes-agent hermes config set ...` также блокируется)


Чтобы изменить конфигурацию, отредактируйте вашу Nix-конфигурацию и выполните `sudo nixos-rebuild switch`.
* * *
## Архитектура контейнера[​](<#container-architecture> "Прямая ссылка на Архитектура контейнера")
info
Этот раздел актуален только если вы используете `container.enable = true`. Пропустите его для развёртываний в нативном режиме.
Когда контейнерный режим включён, hermes работает внутри постоянного Ubuntu-контейнера с Nix-собранным бинарником, примонтированным только для чтения с хоста:
[code] 
    Хост                                    Контейнер  
    ────                                    ─────────  
    /nix/store/...-hermes-agent-0.1.0  ──►  /nix/store/... (ro)  
    ~/.hermes -> /var/lib/hermes/.hermes       (символьная ссылка-мост, по hostUsers)  
    /var/lib/hermes/                    ──►  /data/          (rw)  
      ├── current-package -> /nix/store/...    (символьная ссылка, обновляется при каждой пересборке)  
      ├── .gc-root -> /nix/store/...           (предотвращает nix-collect-garbage)  
      ├── .container-identity                  (sha256-хэш, инициирует пересоздание)  
      ├── .hermes/                             (HERMES_HOME)  
      │   ├── .env                             (объединено из environment + environmentFiles)  
      │   ├── config.yaml                      (сгенерировано Nix, глубокое слияние при активации)  
      │   ├── .managed                         (файл-маркер)  
      │   ├── .container-mode                  (метаданные маршрутизации: backend, exec_user и т.д.)  
      │   ├── state.db, sessions/, memories/   (состояние времени выполнения)  
      │   └── mcp-tokens/                      (OAuth-токены для MCP-серверов)  
      ├── home/                                ──►  /home/hermes    (rw)  
      └── workspace/                           (MESSAGING_CWD)  
          ├── SOUL.md                          (из опции documents)  
          └── (файлы, созданные агентом)  
      
    Записываемый слой контейнера (apt/pip/npm):   /usr, /usr/local, /tmp  
    
[/code]
Nix-собранный бинарник работает внутри Ubuntu-контейнера, потому что `/nix/store` примонтирован — он содержит собственный интерпретатор и все зависимости, поэтому нет зависимости от системных библиотек контейнера. Точка входа контейнера разрешается через символьную ссылку `current-package`: `/data/current-package/bin/hermes gateway run --replace`. При `nixos-rebuild switch` обновляется только символьная ссылка — контейнер продолжает работу.
### Что сохраняется при каких событиях[​](<#what-persists-across-what> "Прямая ссылка на Что сохраняется при каких событиях")
Событие| Контейнер пересоздаётся?| `/data` (состояние)| `/home/hermes`| Записываемый слой (`apt`/`pip`/`npm`)  
---|---|---|---|---  
`systemctl restart hermes-agent`| Нет| Сохраняется| Сохраняется| Сохраняется  
`nixos-rebuild switch` (изменение кода)| Нет (символьная ссылка обновлена)| Сохраняется| Сохраняется| Сохраняется  
Перезагрузка хоста| Нет| Сохраняется| Сохраняется| Сохраняется  
`nix-collect-garbage`| Нет (GC root)| Сохраняется| Сохраняется| Сохраняется  
Изменение образа (`container.image`)| **Да**| Сохраняется| Сохраняется| **Потерян**  
Изменение томов/параметров| **Да**| Сохраняется| Сохраняется| **Потерян**  
Изменение `environment`/`environmentFiles`| Нет| Сохраняется| Сохраняется| Сохраняется  
Контейнер пересоздаётся только когда изменяется его **идентификационный хэш**. Хэш включает: версию схемы, образ, `extraVolumes`, `extraOptions` и скрипт точки входа. Изменения переменных окружения, настроек, документов или самого пакета hermes **не** инициируют пересоздание.
Потеря записываемого слоя
Когда идентификационный хэш изменяется (обновление образа, новые тома, новые параметры контейнера), контейнер уничтожается и пересоздаётся из свежего образа `container.image`. Любые пакеты, установленные через `apt install`, `pip install` или `npm install` в записываемом слое, теряются. Состояние в `/data` и `/home/hermes` сохраняется (это bind-монтирования).
Если агент полагается на определённые пакеты, рассмотрите возможность включения их в пользовательский образ (`container.image = "my-registry/hermes-base:latest"`) или скриптовой установки в `SOUL.md` агента.
### Защита GC Root[​](<#gc-root-protection> "Прямая ссылка на Защита GC Root")
Скрипт `preStart` создаёт GC root по пути `${stateDir}/.gc-root`, указывающий на текущий пакет hermes. Это предотвращает удаление запущенного бинарника командой `nix-collect-garbage`. Если GC root по какой-то причине сломается, перезапуск сервиса воссоздаст его.
* * *
## Плагины[​](<#plugins> "Прямая ссылка на Плагины")
Модуль NixOS поддерживает декларативную установку плагинов — без необходимости в императивном `hermes plugins install`.
### Директориальные плагины (`extraPlugins`)[​](<#directory-plugins-extraplugins> "Прямая ссылка на Директориальные плагины (extraPlugins)")
Для плагинов, которые представляют собой просто дерево исходников с `plugin.yaml` + `__init__.py` (например, [hermes-lcm](<https://github.com/stephenschoettler/hermes-lcm>)):
[code] 
    services.hermes-agent.extraPlugins = [  
      (pkgs.fetchFromGitHub {  
        owner = "stephenschoettler";  
        repo = "hermes-lcm";  
        rev = "v0.7.0";  
        hash = "sha256-...";  
      })  
    ];  
    
[/code]
Плагины симлинкуются в `$HERMES_HOME/plugins/` при активации. Hermes обнаруживает их через обычное сканирование директории. Удаление плагина из списка и выполнение `nixos-rebuild switch` удаляет символьную ссылку.
### Плагины с точкой входа (`extraPythonPackages`)[​](<#entry-point-plugins-extrapythonpackages> "Прямая ссылка на Плагины с точкой входа (extraPythonPackages)")
Для плагинов, упакованных через pip, которые регистрируются через `[project.entry-points."hermes_agent.plugins"]` (например, [rtk-hermes](<https://github.com/ogallotti/rtk-hermes>)):
[code] 
    services.hermes-agent.extraPythonPackages = [  
      (pkgs.python312Packages.buildPythonPackage {  
        pname = "rtk-hermes";  
        version = "1.0.0";  
        src = pkgs.fetchFromGitHub {  
          owner = "ogallotti";  
          repo = "rtk-hermes";  
          rev = "v1.0.0";  
          hash = "sha256-...";  
        };  
        format = "pyproject";  
        build-system = [ pkgs.python312Packages.setuptools ];  
      })  
    ];  
    
[/code]
`site-packages` пакета добавляется в PYTHONPATH в обёртке hermes. `importlib.metadata` обнаруживает точку входа при запуске сессии.
### Комбинирование обоих подходов[​](<#combining-both> "Прямая ссылка на Комбинирование обоих подходов")
Директориальному плагину со сторонними Python-зависимостями нужны обе опции:
[code] 
    services.hermes-agent = {  
      extraPlugins = [ my-plugin-src ];          # исходник плагина  
      extraPythonPackages = [ pkgs.python312Packages.redis ];  # его Python-зависимость  
      extraPackages = [ pkgs.redis ];            # системный бинарник, который ему нужен  
    };  
    
[/code]
### Использование оверлея[​](<#using-the-overlay> "Прямая ссылка на Использование оверлея")
Внешние флейки могут переопределять пакет напрямую:
[code] 
    {  
      inputs.hermes-agent.url = "github:NousResearch/hermes-agent";  
      outputs = { hermes-agent, nixpkgs, ... }: {  
        nixpkgs.overlays = [ hermes-agent.overlays.default ];  
        # Затем: pkgs.hermes-agent.override { extraPythonPackages = [...]; }  
      };  
    }  
    
[/code]
### Конфигурация плагинов[​](<#plugin-configuration> "Прямая ссылка на Конфигурация плагинов")
Плагины всё ещё нужно включать в `config.yaml`. Добавьте их через декларативные настройки:
[code] 
    services.hermes-agent.settings.plugins.enabled = [  
      "hermes-lcm"  
      "rtk-rewrite"  
    ];  
    
[/code]
note
Проверка коллизий на этапе сборки предотвращает перекрытие пакетами плагинов основных зависимостей hermes. Если плагин предоставляет пакет, уже существующий в изолированном venv, `nixos-rebuild` завершится ошибкой с понятным сообщением.
* * *
## Разработка[​](<#development> "Прямая ссылка на Разработка")
### Dev Shell[​](<#dev-shell> "Прямая ссылка на Dev Shell")
Флейк предоставляет оболочку для разработки с Python 3.11, uv, Node.js и всеми инструментами времени выполнения:
[code] 
    cd hermes-agent  
    nix develop  
      
    # Оболочка предоставляет:  
    #   - Python 3.11 + uv (зависимости устанавливаются в .venv при первом входе)  
    #   - Node.js 20, ripgrep, git, openssh, ffmpeg в PATH  
    #   - Оптимизация через stamp-файл: повторный вход почти мгновенный, если зависимости не изменились  
      
    hermes setup  
    hermes chat  
    
[/code]
### direnv (рекомендуется)[​](<#direnv-recommended> "Прямая ссылка на direnv (рекомендуется)")
Включённый `.envrc` активирует dev shell автоматически:
[code] 
    cd hermes-agent  
    direnv allow    # однократно  
    # Последующие входы почти мгновенны (stamp-файл пропускает установку зависимостей)  
    
[/code]
### Проверки флейка[​](<#flake-checks> "Прямая ссылка на Проверки флейка")
Флейк включает проверки на этапе сборки, которые выполняются в CI и локально:
[code] 
    # Запустить все проверки  
    nix flake check  
      
    # Отдельные проверки  
    nix build .#checks.x86_64-linux.package-contents   # бинарники существуют + версия  
    nix build .#checks.x86_64-linux.entry-points-sync  # синхронизация pyproject.toml ↔ Nix пакет  
    nix build .#checks.x86_64-linux.cli-commands        # подкоманды gateway/config  
    nix build .#checks.x86_64-linux.managed-guard       # HERMES_MANAGED блокирует мутацию  
    nix build .#checks.x86_64-linux.bundled-skills      # навыки присутствуют в пакете  
    nix build .#checks.x86_64-linux.config-roundtrip    # скрипт слияния сохраняет ключи пользователя  
    
[/code]
**Что проверяет каждая проверка**
Проверка| Что тестирует  
---|---  
`package-contents`| Бинарники `hermes` и `hermes-agent` существуют и `hermes version` выполняется  
`entry-points-sync`| Каждая запись `[project.scripts]` в `pyproject.toml` имеет обёрнутый бинарник в Nix-пакете  
`cli-commands`| `hermes --help` отображает подкоманды `gateway` и `config`  
`managed-guard`| `HERMES_MANAGED=true hermes config set ...` выводит ошибку NixOS  
`bundled-skills`| Директория навыков существует, содержит SKILL.md, `HERMES_BUNDLED_SKILLS` установлена в обёртке  
`config-roundtrip`| 7 сценариев слияния: чистая установка, переопределение Nix, сохранение ключей пользователя, смешанное слияние, аддитивное слияние MCP, вложенное глубокое слияние, идемпотентность  
* * *
## Справочник опций[​](<#options-reference> "Прямая ссылка на Справочник опций")
### Основные[​](<#core> "Прямая ссылка на Основные")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`enable`| `bool`| `false`| Включить сервис hermes-agent  
`package`| `package`| `hermes-agent`| Используемый пакет hermes-agent  
`user`| `str`| `"hermes"`| Системный пользователь  
`group`| `str`| `"hermes"`| Системная группа  
`createUser`| `bool`| `true`| Автосоздание пользователя/группы  
`stateDir`| `str`| `"/var/lib/hermes"`| Директория состояния (родительская для `HERMES_HOME`)  
`workingDirectory`| `str`| `"${stateDir}/workspace"`| Рабочая директория агента (`MESSAGING_CWD`)  
`addToSystemPackages`| `bool`| `false`| Добавить CLI `hermes` в системный PATH и установить `HERMES_HOME` общесистемно  
### Конфигурация[​](<#configuration-1> "Прямая ссылка на Конфигурация")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`settings`| `attrs` (глубокое слияние)| `{}`| Декларативная конфигурация, преобразуемая в `config.yaml`. Поддерживает произвольную вложенность; несколько определений сливаются через `lib.recursiveUpdate`  
`configFile`| `null` или `path`| `null`| Путь к существующему `config.yaml`. Полностью переопределяет `settings`, если задан  
### Секреты и окружение[​](<#secrets--environment> "Прямая ссылка на Секреты и окружение")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`environmentFiles`| `listOf str`| `[]`| Пути к файлам окружения с секретами. Объединяются в `$HERMES_HOME/.env` при активации  
`environment`| `attrsOf str`| `{}`| Несекретные переменные окружения. **Видимы в Nix store** — не помещайте сюда секреты  
`authFile`| `null` или `path`| `null`| Предзагрузка OAuth-учётных данных. Копируется только при первом развёртывании  
`authFileForceOverwrite`| `bool`| `false`| Всегда перезаписывать `auth.json` из `authFile` при активации  
### Документы[​](<#documents-1> "Прямая ссылка на Документы")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`documents`| `attrsOf (either str path)`| `{}`| Файлы рабочего пространства. Ключи — имена файлов, значения — строки напрямую или пути. Устанавливаются в `workingDirectory` при активации  
### MCP-серверы[​](<#mcp-servers-1> "Прямая ссылка на MCP-серверы")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`mcpServers`| `attrsOf submodule`| `{}`| Определения MCP-серверов, объединяемые в `settings.mcp_servers`  
`mcpServers.<name>.command`| `null` или `str`| `null`| Команда сервера (stdio-транспорт)  
`mcpServers.<name>.args`| `listOf str`| `[]`| Аргументы команды  
`mcpServers.<name>.env`| `attrsOf str`| `{}`| Переменные окружения для процесса сервера  
`mcpServers.<name>.url`| `null` или `str`| `null`| URL конечной точки сервера (HTTP/StreamableHTTP транспорт)  
`mcpServers.<name>.headers`| `attrsOf str`| `{}`| HTTP-заголовки, например `Authorization`  
`mcpServers.<name>.auth`| `null` или `"oauth"`| `null`| Метод аутентификации. `"oauth"` включает OAuth 2.1 PKCE  
`mcpServers.<name>.enabled`| `bool`| `true`| Включить или отключить этот сервер  
`mcpServers.<name>.timeout`| `null` или `int`| `null`| Тайм-аут вызова инструмента в секундах (по умолчанию: 120)  
`mcpServers.<name>.connect_timeout`| `null` или `int`| `null`| Тайм-аут подключения в секундах (по умолчанию: 60)  
`mcpServers.<name>.tools`| `null` или `submodule`| `null`| Фильтрация инструментов (списки `include`/`exclude`)  
`mcpServers.<name>.sampling`| `null` или `submodule`| `null`| Конфигурация сэмплинга для запросов LLM, инициированных сервером  
### Поведение сервиса[​](<#service-behavior> "Прямая ссылка на Поведение сервиса")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`extraArgs`| `listOf str`| `[]`| Дополнительные аргументы для `hermes gateway`  
`extraPackages`| `listOf package`| `[]`| Дополнительные пакеты, доступные агенту. Добавляются в per-user профиль пользователя hermes, так что терминальные команды, навыки и cron-задачи все их видят  
`extraPlugins`| `listOf package`| `[]`| Пакеты директориальных плагинов для симлинкования в `$HERMES_HOME/plugins/`. Каждый должен содержать `plugin.yaml`  
`extraPythonPackages`| `listOf package`| `[]`| Python-пакеты, добавляемые в PYTHONPATH для обнаружения плагинов с точкой входа. Собирайте с помощью `python312Packages`  
`restart`| `str`| `"always"`| Политика systemd `Restart=`  
`restartSec`| `int`| `5`| Значение systemd `RestartSec=`  
### Контейнер[​](<#container> "Прямая ссылка на Контейнер")
Опция| Тип| По умолчанию| Описание  
---|---|---|---  
`container.enable`| `bool`| `false`| Включить режим OCI-контейнера  
`container.backend`| `enum ["docker" "podman"]`| `"docker"`| Среда выполнения контейнера  
`container.image`| `str`| `"ubuntu:24.04"`| Базовый образ (загружается во время выполнения)  
`container.extraVolumes`| `listOf str`| `[]`| Дополнительные монтирования томов (`хост:контейнер:режим`)  
`container.extraOptions`| `listOf str`| `[]`| Дополнительные аргументы, передаваемые в `docker create`  
`container.hostUsers`| `listOf str`| `[]`| Интерактивные пользователи, которые получают символьную ссылку `~/.hermes` на stateDir сервиса и автоматически добавляются в группу `hermes`  
* * *
## Структура директорий[​](<#directory-layout> "Прямая ссылка на Структура директорий")
### Нативный режим[​](<#native-mode> "Прямая ссылка на Нативный режим")
[code] 
    /var/lib/hermes/                     # stateDir (владелец hermes:hermes, 0750)  
    ├── .hermes/                         # HERMES_HOME  
    │   ├── config.yaml                  # сгенерировано Nix (глубокое слияние при каждой пересборке)  
    │   ├── .managed                     # Маркер: мутация CLI-конфигурации заблокирована  
    │   ├── .env                         # Объединено из environment + environmentFiles  
    │   ├── auth.json                    # OAuth-учётные данные (предзагружены, затем самоуправляемы)  
    │   ├── gateway.pid  
    │   ├── state.db  
    │   ├── mcp-tokens/                  # OAuth-токены для MCP-серверов  
    │   ├── sessions/  
    │   ├── memories/  
    │   ├── skills/  
    │   ├── cron/  
    │   └── logs/  
    ├── home/                            # HOME агента  
    └── workspace/                       # MESSAGING_CWD  
        ├── SOUL.md                      # Из опции documents  
        └── (файлы, созданные агентом)  
    
[/code]
### Контейнерный режим[​](<#container-mode> "Прямая ссылка на Контейнерный режим")
Та же структура, смонтированная в контейнер:
Путь в контейнере| Путь на хосте| Режим| Примечания  
---|---|---|---|---  
`/nix/store`| `/nix/store`| `ro`| Бинарник Hermes + все Nix-зависимости  
`/data`| `/var/lib/hermes`| `rw`| Всё состояние, конфигурация, рабочее пространство  
`/home/hermes`| `${stateDir}/home`| `rw`| Постоянный home агента — `pip install --user`, кэши инструментов  
`/usr`, `/usr/local`, `/tmp`| (записываемый слой)| `rw`| Установки `apt`/`pip`/`npm` — сохраняются между перезапусками, теряются при пересоздании  
* * *
## Обновление[​](<#updating> "Прямая ссылка на Обновление")
[code] 
    # Обновить вход флейка  
    nix flake update hermes-agent --flake /etc/nixos  
      
    # Пересобрать  
    sudo nixos-rebuild switch  
    
[/code]
В контейнерном режиме символьная ссылка `current-package` обновляется, и агент подхватывает новый бинарник при перезапуске. Без пересоздания контейнера, без потери установленных пакетов.
* * *
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")
Пользователи Podman
Все команды `docker` ниже работают так же с `podman`. Заменяйте соответственно, если вы установили `container.backend = "podman"`.
### Логи сервиса[​](<#service-logs> "Прямая ссылка на Логи сервиса")
[code] 
    # Оба режима используют один и тот же systemd-юнит  
    journalctl -u hermes-agent -f  
      
    # Контейнерный режим: также доступно напрямую  
    docker logs -f hermes-agent  
    
[/code]
### Инспекция контейнера[​](<#container-inspection> "Прямая ссылка на Инспекция контейнера")
[code] 
    systemctl status hermes-agent  
    docker ps -a --filter name=hermes-agent  
    docker inspect hermes-agent --format='{{.State.Status}}'  
    docker exec -it hermes-agent bash  
    docker exec hermes-agent readlink /data/current-package  
    docker exec hermes-agent cat /data/.container-identity  
    
[/code]
### Принудительное пересоздание контейнера[​](<#force-container-recreation> "Прямая ссылка на Принудительное пересоздание контейнера")
Если вам нужно сбросить записываемый слой (свежий Ubuntu):
[code] 
    sudo systemctl stop hermes-agent  
    docker rm -f hermes-agent  
    sudo rm /var/lib/hermes/.container-identity  
    sudo systemctl start hermes-agent  
    
[/code]
### Проверка загрузки секретов[​](<#verify-secrets-are-loaded> "Прямая ссылка на Проверка загрузки секретов")
Если агент запускается, но не может аутентифицироваться у LLM-провайдера, проверьте, что файл `.env` был объединён корректно:
[code] 
    # Нативный режим  
    sudo -u hermes cat /var/lib/hermes/.hermes/.env  
      
    # Контейнерный режим  
    docker exec hermes-agent cat /data/.hermes/.env  
    
[/code]
### Проверка GC Root[​](<#gc-root-verification> "Прямая ссылка на Проверка GC Root")
[code] 
    nix-store --query --roots $(docker exec hermes-agent readlink /data/current-package)  
    
[/code]
### Частые проблемы[​](<#common-issues> "Прямая ссылка на Частые проблемы")
Симптом| Причина| Исправление  
---|---|---  
`Cannot save configuration: managed by NixOS`| Активны CLI-ограничения| Отредактируйте `configuration.nix` и выполните `nixos-rebuild switch`  
Контейнер неожиданно пересоздан| Изменились `extraVolumes`, `extraOptions` или `image`| Ожидаемо — записываемый слой сбрасывается. Переустановите пакеты или используйте пользовательский образ  
`hermes version` показывает старую версию| Контейнер не перезапущен| `systemctl restart hermes-agent`  
Отказано в доступе к `/var/lib/hermes`| Директория состояния имеет `0750 hermes:hermes`| Используйте `docker exec` или `sudo -u hermes`  
`nix-collect-garbage` удалил hermes| Отсутствует GC root| Перезапустите сервис (preStart воссоздаёт GC root)  
`no container with name or ID "hermes-agent"` (Podman)| Rootful-контейнер Podman не виден обычному пользователю| Добавьте sudo без пароля для podman (см. раздел [Контейнерный режим](<#container-mode>))  
`unable to find user hermes`| Контейнер всё ещё запускается (точка входа ещё не создала пользователя)| Подождите несколько секунд и повторите — CLI повторяет попытку автоматически  
Инструмент, добавленный через `extraPackages`, не найден в терминале| Требуется `nixos-rebuild switch` для обновления per-user профиля| Пересоберите и перезапустите: `nixos-rebuild switch && systemctl restart hermes-agent`  
  * [Предварительные требования](<#prerequisites>)
  * [Быстрый старт (любой пользователь Nix)](<#quick-start-any-nix-user>)
  * [Модуль NixOS](<#nixos-module>)
    * [Добавление флейк-входа](<#add-the-flake-input>)
    * [Минимальная конфигурация](<#minimal-configuration>)
    * [CLI с поддержкой контейнера](<#container-aware-cli>)
    * [Проверка работоспособности](<#verify-it-works>)
    * [Выбор режима развёртывания](<#choosing-a-deployment-mode>)
  * [Конфигурация](<#configuration>)
    * [Декларативные настройки](<#declarative-settings>)
    * [Запасной вариант: собственная конфигурация](<#escape-hatch-bring-your-own-config>)
    * [Шпаргалка по настройке](<#customization-cheatsheet>)
  * [Управление секретами](<#secrets-management>)
    * [sops-nix](<#sops-nix>)
    * [agenix](<#agenix>)
    * [OAuth / Предзагрузка аутентификации](<#oauth--auth-seeding>)
  * [Документы](<#documents>)
  * [MCP-серверы](<#mcp-servers>)
    * [Stdio-транспорт (локальные серверы)](<#stdio-transport-local-servers>)
    * [HTTP-транспорт (удалённые серверы)](<#http-transport-remote-servers>)
    * [HTTP-транспорт с OAuth](<#http-transport-with-oauth>)
    * [Сэмплинг (запросы LLM, инициированные сервером)](<#sampling-server-initiated-llm-requests>)
  * [Управляемый режим](<#managed-mode>)
  * [Архитектура контейнера](<#container-architecture>)
    * [Что сохраняется при каких событиях](<#what-persists-across-what>)
    * [Защита GC Root](<#gc-root-protection>)
  * [Плагины](<#plugins>)
    * [Директориальные плагины (`extraPlugins`)](<#directory-plugins-extraplugins>)
    * [Плагины с точкой входа (`extraPythonPackages`)](<#entry-point-plugins-extrapythonpackages>)
    * [Комбинирование обоих подходов](<#combining-both>)
    * [Использование оверлея](<#using-the-overlay>)
    * [Конфигурация плагинов](<#plugin-configuration>)
  * [Разработка](<#development>)
    * [Dev Shell](<#dev-shell>)
    * [direnv (рекомендуется)](<#direnv-recommended>)
    * [Проверки флейка](<#flake-checks>)
  * [Справочник опций](<#options-reference>)
    * [Основные](<#core>)
    * [Конфигурация](<#configuration-1>)
    * [Секреты и окружение](<#secrets--environment>)
    * [Документы](<#documents-1>)
    * [MCP-серверы](<#mcp-servers-1>)
    * [Поведение сервиса](<#service-behavior>)
    * [Контейнер](<#container>)
  * [Структура директорий](<#directory-layout>)
    * [Нативный режим](<#native-mode>)
    * [Контейнерный режим](<#container-mode>)
  * [Обновление](<#updating>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Логи сервиса](<#service-logs>)
    * [Инспекция контейнера](<#container-inspection>)
    * [Принудительное пересоздание контейнера](<#force-container-recreation>)
    * [Проверка загрузки секретов](<#verify-secrets-are-loaded>)
    * [Проверка GC Root](<#gc-root-verification>)
    * [Частые проблемы](<#common-issues>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup -->
