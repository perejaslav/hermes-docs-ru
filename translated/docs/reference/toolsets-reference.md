On this page

Наборы инструментов (toolsets) — это именованные пакеты инструментов, определяющие, что может делать агент. Это основной механизм настройки доступности инструментов для каждой платформы, сессии или задачи.

## Как работают наборы инструментов[​](<#how-toolsets-work> "Прямая ссылка на «Как работают наборы инструментов»")

Каждый инструмент принадлежит ровно одному набору. Когда вы включаете набор, все инструменты в этом пакете становятся доступны агенту. Наборы инструментов бывают трёх видов:

  * **Базовый (Core)** — единая логическая группа связанных инструментов (например, `file` объединяет `read_file`, `write_file`, `patch`, `search_files`)
  * **Составной (Composite)** — объединяет несколько базовых наборов для общего сценария (например, `debugging` объединяет файловые, терминальные и веб-инструменты)
  * **Платформенный (Platform)** — полная конфигурация инструментов для конкретного контекста развёртывания (например, `hermes-cli` — набор по умолчанию для интерактивных CLI-сессий)

## Настройка наборов инструментов[​](<#configuring-toolsets> "Прямая ссылка на «Настройка наборов инструментов»")

### Для сессии (CLI)[​](<#per-session-cli> "Прямая ссылка на «Для сессии (CLI)»")

[code] 
    hermes chat --toolsets web,file,terminal  
    hermes chat --toolsets debugging        # составной — расширяется до file + terminal + web  
    hermes chat --toolsets all              # всё  
    
[/code]

### Для платформы (config.yaml)[​](<#per-platform-configyaml> "Прямая ссылка на «Для платформы (config.yaml)»")

[code] 
    toolsets:  
      - hermes-cli          # по умолчанию для CLI  
      # - hermes-telegram   # переопределение для шлюза Telegram  
    
[/code]

### Интерактивное управление[​](<#interactive-management> "Прямая ссылка на «Интерактивное управление»")

[code] 
    hermes tools                            # curses-интерфейс для включения/отключения для каждой платформы  
    
[/code]

Или внутри сессии:

[code] 
    /tools list  
    /tools disable browser  
    /tools enable rl  
    
[/code]

## Базовые наборы инструментов[​](<#core-toolsets> "Прямая ссылка на «Базовые наборы инструментов»")

| Набор | Инструменты | Назначение |
|---|---|---|
| `browser` | `browser_back`, `browser_click`, `browser_console`, `browser_get_images`, `browser_navigate`, `browser_press`, `browser_scroll`, `browser_snapshot`, `browser_type`, `browser_vision`, `web_search` | Базовая автоматизация браузера. Включает `web_search` как запасной вариант для быстрых поисковых запросов. `browser_cdp` и `browser_dialog` находятся в отдельном наборе `browser-cdp` и регистрируются только при достижимости CDP-эндпоинта на старте сессии — через `/browser connect`, `browser.cdp_url` в конфиге, Browserbase или Camofox. `browser_dialog` работает совместно с полями `pending_dialogs` и `frame_tree`, которые `browser_snapshot` добавляет при подключённом CDP-супервизоре. |
| `clarify` | `clarify` | Задать вопрос пользователю, когда агенту нужно уточнение. |
| `code_execution` | `execute_code` | Запуск Python-скриптов, программно вызывающих инструменты Hermes. |
| `cronjob` | `cronjob` | Планирование и управление повторяющимися задачами. |
| `debugging` | составной (`file` + `terminal` + `web`) | Пакет для отладки — файлы, процессы/терминал, веб-извлечение/поиск. |
| `delegation` | `delegate_task` | Запуск изолированных экземпляров под-агентов для параллельной работы. |
| `discord` | `discord` | Базовые действия Discord (текст/встраивания/ЛС, только через шлюз). Активен в наборе `hermes-discord`. |
| `discord_admin` | `discord_admin` | Модерация Discord (баны, изменение ролей, управление каналами). Активен в наборе `hermes-discord`; требует, чтобы бот обладал соответствующими правами Discord. |
| `feishu_doc` | `feishu_doc_read` | Чтение содержимого документов Feishu/Lark. Используется обработчиком интеллектуальных ответов на комментарии в документах Feishu. |
| `feishu_drive` | `feishu_drive_add_comment`, `feishu_drive_list_comments`, `feishu_drive_list_comment_replies`, `feishu_drive_reply_comment` | Операции с комментариями в Feishu/Lark Drive. Ограничен агентом комментариев; не доступен в `hermes-cli` или других наборах для мессенджеров. |
| `file` | `patch`, `read_file`, `search_files`, `write_file` | Чтение, запись, поиск и редактирование файлов. |
| `homeassistant` | `ha_call_service`, `ha_get_state`, `ha_list_entities`, `ha_list_services` | Управление умным домом через Home Assistant. Доступен только при установленной переменной `HASS_TOKEN`. |
| `image_gen` | `image_generate` | Генерация изображений по текстовому описанию через FAL.ai (с опциональными бэкендами OpenAI / xAI). |
| `memory` | `memory` | Управление постоянной памятью между сессиями. |
| `messaging` | `send_message` | Отправка сообщений на другие платформы (Telegram, Discord и др.) из текущей сессии. |
| `moa` | `mixture_of_agents` | Многомодельный консенсус через Mixture of Agents. |
| `rl` | `rl_check_status`, `rl_edit_config`, `rl_get_current_config`, `rl_get_results`, `rl_list_environments`, `rl_list_runs`, `rl_select_environment`, `rl_start_training`, `rl_stop_training`, `rl_test_inference` | Управление окружением RL-обучения (Atropos). |
| `safe` | `image_generate`, `vision_analyze`, `web_extract`, `web_search` (через `includes`) | Исследование только для чтения + генерация медиа. Нет записи файлов, нет терминала, нет выполнения кода. |
| `search` | `web_search` | Только веб-поиск (без извлечения). |
| `session_search` | `session_search` | Поиск по прошлым сессиям диалогов. |
| `skills` | `skill_manage`, `skill_view`, `skills_list` | CRUD-операции и просмотр навыков. |
| `spotify` | `spotify_albums`, `spotify_devices`, `spotify_library`, `spotify_playback`, `spotify_playlists`, `spotify_queue`, `spotify_search` | Нативное управление Spotify (воспроизведение, очередь, поиск, плейлисты, альбомы, библиотека). Регистрируется встроенным плагином `spotify`. |
| `terminal` | `process`, `terminal` | Выполнение команд оболочки и управление фоновыми процессами. |
| `todo` | `todo` | Управление списком задач в рамках сессии. |
| `tts` | `text_to_speech` | Генерация аудио из текста (Text-to-Speech). |
| `vision` | `vision_analyze` | Анализ изображений через модели, поддерживающие компьютерное зрение. |
| `web` | `web_extract`, `web_search` | Веб-поиск и извлечение содержимого страниц. |
| `yuanbao` | `yb_query_group_info`, `yb_query_group_members`, `yb_search_sticker`, `yb_send_dm`, `yb_send_sticker` | Действия с личными сообщениями и группами Yuanbao, поиск стикеров. Регистрируется только в `hermes-yuanbao`. |

## Платформенные наборы инструментов[​](<#platform-toolsets> "Прямая ссылка на «Платформенные наборы инструментов»")

Платформенные наборы инструментов определяют полную конфигурацию инструментов для целевого развёртывания. Большинство платформ обмена сообщениями используют тот же набор, что и `hermes-cli`:

| Набор | Отличия от `hermes-cli` |
|---|---|
| `hermes-cli` | Полный набор — 38 инструментов. Используется по умолчанию для интерактивных CLI-сессий. |
| `hermes-acp` | Исключает `clarify`, `cronjob`, `image_generate`, `send_message`, `text_to_speech` и все четыре инструмента Home Assistant. Ориентирован на задачи кодирования в контексте IDE. |
| `hermes-api-server` | Исключает `clarify`, `send_message` и `text_to_speech`. Оставляет всё остальное — подходит для программного доступа, где взаимодействие с пользователем невозможно. |
| `hermes-cron` | Совпадает с `hermes-cli`. |
| `hermes-telegram` | Совпадает с `hermes-cli`. |
| `hermes-discord` | Добавляет `discord` и `discord_admin` поверх `hermes-cli`. |
| `hermes-slack` | Совпадает с `hermes-cli`. |
| `hermes-whatsapp` | Совпадает с `hermes-cli`. |
| `hermes-signal` | Совпадает с `hermes-cli`. |
| `hermes-matrix` | Совпадает с `hermes-cli`. |
| `hermes-mattermost` | Совпадает с `hermes-cli`. |
| `hermes-email` | Совпадает с `hermes-cli`. |
| `hermes-sms` | Совпадает с `hermes-cli`. |
| `hermes-bluebubbles` | Совпадает с `hermes-cli`. |
| `hermes-dingtalk` | Совпадает с `hermes-cli`. |
| `hermes-feishu` | Добавляет пять инструментов `feishu_doc_*` / `feishu_drive_*` (используются только обработчиком комментариев к документам, а не обычным адаптером чата). |
| `hermes-qqbot` | Совпадает с `hermes-cli`. |
| `hermes-wecom` | Совпадает с `hermes-cli`. |
| `hermes-wecom-callback` | Совпадает с `hermes-cli`. |
| `hermes-weixin` | Совпадает с `hermes-cli`. |
| `hermes-yuanbao` | Добавляет пять инструментов `yb_*` (ЛС/группы/стикеры) поверх `hermes-cli`. |
| `hermes-homeassistant` | Совпадает с `hermes-cli` (инструменты Home Assistant уже присутствуют по умолчанию и активируются при установке `HASS_TOKEN`). |
| `hermes-webhook` | Совпадает с `hermes-cli`. |
| `hermes-gateway` | Внутренний набор инструментов оркестратора шлюза — объединение всех наборов `hermes-<platform>`; используется когда шлюзу нужно принимать сообщения из любого источника. |

## Динамические наборы инструментов[​](<#dynamic-toolsets> "Прямая ссылка на «Динамические наборы инструментов»")

### Наборы инструментов MCP-серверов[​](<#mcp-server-toolsets> "Прямая ссылка на «Наборы инструментов MCP-серверов»")

Каждый настроенный MCP-сервер генерирует набор `mcp-<server>` во время выполнения. Например, если вы настроили MCP-сервер `github`, создаётся набор `mcp-github`, содержащий все инструменты этого сервера.

[code] 
    # config.yaml  
    mcp_servers:  
      github:  
        command: npx  
        args: ["-y", "@modelcontextprotocol/server-github"]  
    
[/code]

Это создаёт набор `mcp-github`, на который можно ссылаться в `--toolsets` или в конфигурациях платформ.

### Наборы инструментов плагинов[​](<#plugin-toolsets> "Прямая ссылка на «Наборы инструментов плагинов»")

Плагины могут регистрировать собственные наборы инструментов через `ctx.register_tool()` во время инициализации плагина. Они отображаются рядом со встроенными наборами и могут быть включены/отключены тем же способом.

### Пользовательские наборы инструментов[​](<#custom-toolsets> "Прямая ссылка на «Пользовательские наборы инструментов»")

Определите собственные наборы инструментов в `config.yaml` для создания пакетов под конкретные проекты:

[code] 
    toolsets:  
      - hermes-cli  
    custom_toolsets:  
      data-science:  
        - file  
        - terminal  
        - code_execution  
        - web  
        - vision  
    
[/code]

### Подстановочные знаки[​](<#wildcards> "Прямая ссылка на «Подстановочные знаки»")

  * `all` или `*` — раскрывается во все зарегистрированные наборы инструментов (встроенные + динамические + плагины)

## Связь с командой `hermes tools`[​](<#relationship-to-hermes-tools> "Прямая ссылка на «Связь с командой hermes tools»")

Команда `hermes tools` предоставляет curses-интерфейс для включения или отключения отдельных инструментов для каждой платформы. Это работает на уровне инструментов (более детально, чем наборы) и сохраняется в `config.yaml`. Отключённые инструменты фильтруются, даже если их набор включён.

См. также: [Справочник по инструментам](</docs/reference/tools-reference>) для полного списка отдельных инструментов и их параметров.

  * [Как работают наборы инструментов](<#how-toolsets-work>)
  * [Настройка наборов инструментов](<#configuring-toolsets>)
    * [Для сессии (CLI)](<#per-session-cli>)
    * [Для платформы (config.yaml)](<#per-platform-configyaml>)
    * [Интерактивное управление](<#interactive-management>)
  * [Базовые наборы инструментов](<#core-toolsets>)
  * [Платформенные наборы инструментов](<#platform-toolsets>)
  * [Динамические наборы инструментов](<#dynamic-toolsets>)
    * [Наборы инструментов MCP-серверов](<#mcp-server-toolsets>)
    * [Наборы инструментов плагинов](<#plugin-toolsets>)
    * [Пользовательские наборы инструментов](<#custom-toolsets>)
    * [Подстановочные знаки](<#wildcards>)
  * [Связь с командой `hermes tools`](<#relationship-to-hermes-tools>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference -->
