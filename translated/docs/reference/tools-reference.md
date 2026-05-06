На этой странице
На этой странице описаны все 68 встроенных инструментов в реестре инструментов Hermes, сгруппированных по наборам инструментов. Доступность варьируется в зависимости от платформы, учетных данных и включенных наборов инструментов.
**Краткая статистика:** 10 инструментов браузера (основные) + 2 инструмента browser-cdp, 4 файловых инструмента, 10 инструментов RL, 4 инструмента Home Assistant, 2 инструмента терминала, 2 веб-инструмента, 5 инструментов Feishu, 7 инструментов Spotify, 5 инструментов Yuanbao, 2 инструмента Discord и 15 отдельных инструментов в других наборах.
Инструменты MCP
Помимо встроенных инструментов, Hermes может динамически загружать инструменты с MCP-серверов. Инструменты MCP отображаются с префиксом имени сервера (например, `github_create_issue` для MCP-сервера `github`). См. [MCP Integration](</docs/user-guide/features/mcp>) для настройки.
## `browser` toolset[​](<#browser-toolset> "Direct link to browser-toolset")
Tool| Description| Requires environment
|---|---|---
`browser_back`| Переход на предыдущую страницу в истории браузера. Требуется предварительный вызов browser_navigate.| —
`browser_click`| Клик по элементу, идентифицированному его ref ID из снимка (например, '@e5'). Ref ID отображаются в квадратных скобках в выводе снимка. Требуется предварительный вызов browser_navigate и browser_snapshot.| —
`browser_console`| Получение вывода консоли браузера и ошибок JavaScript с текущей страницы. Возвращает сообщения console.log/warn/error/info и неперехваченные JS-исключения. Используйте для обнаружения скрытых ошибок JavaScript, неудачных API-вызовов и предупреждений приложения. Требуется предварительный вызов browser_navigate.| —
`browser_get_images`| Получение списка всех изображений на текущей странице с их URL и alt-текстом. Полезно для поиска изображений для анализа с помощью инструмента vision. Требуется предварительный вызов browser_navigate.| —
`browser_navigate`| Переход по URL в браузере. Инициализирует сессию и загружает страницу. Должен быть вызван перед другими инструментами браузера. Для простого поиска информации предпочитайте web_search или web_extract (быстрее, дешевле). Используйте инструменты браузера, когда вам нужно...| —
`browser_press`| Нажатие клавиши на клавиатуре. Полезно для отправки форм (Enter), навигации (Tab) или клавиатурных сокращений. Требуется предварительный вызов browser_navigate.| —
`browser_scroll`| Прокрутка страницы в заданном направлении. Используйте для отображения содержимого, находящегося ниже или выше текущей области просмотра. Требуется предварительный вызов browser_navigate.| —
`browser_snapshot`| Получение текстового снимка дерева доступности текущей страницы. Возвращает интерактивные элементы с ref ID (например, @e1, @e2) для browser_click и browser_type. full=false (по умолчанию): компактное представление с интерактивными элементами. full=true: пол...| —
`browser_type`| Ввод текста в поле ввода, идентифицированное по его ref ID. Сначала очищает поле, затем вводит новый текст. Требуется предварительный вызов browser_navigate и browser_snapshot.| —
`browser_vision`| Создание снимка экрана текущей страницы и его анализ с помощью AI vision. Используйте, когда нужно визуально понять содержимое страницы — особенно полезно для CAPTCHA, задач визуальной проверки, сложных макетов или когда текстовый сним...| —
## `browser-cdp` toolset[​](<#browser-cdp-toolset> "Direct link to browser-cdp-toolset")
Регистрируется только при доступности конечной точки Chrome DevTools Protocol при запуске сессии — через `/browser connect`, конфигурацию `browser.cdp_url`, сессию Browserbase или Camofox.
Tool| Description| Requires environment
|---|---|---
`browser_cdp`| Отправка сырой команды Chrome DevTools Protocol. Запасной вариант для операций браузера, не охваченных высокоуровневыми инструментами `browser_*`. См. <https://chromedevtools.github.io/devtools-protocol/>| CDP endpoint
`browser_dialog`| Ответ на нативный диалог JavaScript (alert / confirm / prompt / beforeunload). Сначала вызовите `browser_snapshot` — ожидающие диалоги отображаются в поле `pending_dialogs`. Затем вызовите `browser_dialog(action='accept'|'dismiss')`.| CDP endpoint
## `clarify` toolset[​](<#clarify-toolset> "Direct link to clarify-toolset")
Tool| Description| Requires environment
|---|---|---
`clarify`| Задайте вопрос пользователю, когда вам нужно уточнение, обратная связь или решение перед продолжением. Поддерживает два режима: 1. **Множественный выбор** — до 4 вариантов. Пользователь выбирает один или вводит свой ответ через 5-й вариант 'Другое'. 2....| —
## `code_execution` toolset[​](<#code_execution-toolset> "Direct link to code_execution-toolset")
Tool| Description| Requires environment
|---|---|---
`execute_code`| Запуск Python-скрипта, который может программно вызывать инструменты Hermes. Используйте, когда нужно 3+ вызова инструментов с логикой обработки между ними, нужно фильтровать/сокращать большие выводы инструментов перед их попаданием в контекст, нужно условное ветвление (...| —
## `cronjob` toolset[​](<#cronjob-toolset> "Direct link to cronjob-toolset")
Tool| Description| Requires environment
|---|---|---
`cronjob`| Унифицированный менеджер запланированных задач. Используйте `action=\"create\"`, `\"list\"`, `\"update\"`, `\"pause\"`, `\"resume\"`, `\"run\"` или `\"remove\"` для управления заданиями. Поддерживает задания на основе навыков с одним или несколькими прикрепленными навыками, а `skills=[]` при обновлении удаляет прикрепленные навыки. Cron-запуски происходят в новых сессиях без контекста текущего чата.| —
## `delegation` toolset[​](<#delegation-toolset> "Direct link to delegation-toolset")
Tool| Description| Requires environment
|---|---|---
`delegate_task`| Запуск одного или нескольких подагентов для работы над задачами в изолированных контекстах. Каждый подагент получает свой собственный диалог, сессию терминала и набор инструментов. Возвращается только итоговая сводка — промежуточные результаты инструментов никогда не попадают в ваше окно контекста. ДВА...| —
## `feishu_doc` toolset[​](<#feishu_doc-toolset> "Direct link to feishu_doc-toolset")
Ограничено обработчиком интеллектуальных ответов на комментарии в документах Feishu (`gateway/platforms/feishu_comment.py`). Недоступно в `hermes-cli` или обычном адаптере чата Feishu.
Tool| Description| Requires environment
|---|---|---
`feishu_doc_read`| Чтение полного текстового содержимого документа Feishu/Lark (Docx, Doc или Sheet) по его file_type и token.| Учетные данные приложения Feishu
## `feishu_drive` toolset[​](<#feishu_drive-toolset> "Direct link to feishu_drive-toolset")
Ограничено обработчиком комментариев в документах Feishu. Обеспечивает операции чтения/записи комментариев в файлах диска.
Tool| Description| Requires environment
|---|---|---
`feishu_drive_add_comment`| Добавление комментария верхнего уровня к документу или файлу Feishu/Lark.| Учетные данные приложения Feishu
`feishu_drive_list_comments`| Список комментариев ко всему документу в файле Feishu/Lark, сначала самые новые.| Учетные данные приложения Feishu
`feishu_drive_list_comment_replies`| Список ответов в конкретной ветке комментариев Feishu (весь документ или локальное выделение).| Учетные данные приложения Feishu
`feishu_drive_reply_comment`| Отправка ответа в ветке комментариев Feishu с опциональным упоминанием через `@`.| Учетные данные приложения Feishu
## `file` toolset[​](<#file-toolset> "Direct link to file-toolset")
Tool| Description| Requires environment
|---|---|---
`patch`| Целенаправленные замены и исправления в файлах. Используйте вместо sed/awk в терминале. Использует нечеткое сопоставление (9 стратегий), поэтому небольшие различия в пробелах/отступах не нарушат работу. Возвращает унифицированный diff. Автоматически запускает синтаксические проверки после редактирования...| —
`read_file`| Чтение текстового файла с номерами строк и постраничным выводом. Используйте вместо cat/head/tail в терминале. Формат вывода: 'LINE_NUM|CONTENT'. Предлагает похожие имена файлов, если не найдено. Используйте offset и limit для больших файлов. ПРИМЕЧАНИЕ: Не может читать изображения или...| —
`search_files`| Поиск содержимого файлов или поиск файлов по имени. Используйте вместо grep/rg/find/ls в терминале. Работает на базе Ripgrep, быстрее shell-аналогов. Поиск по содержимому (target='content'): regex-поиск внутри файлов. Режимы вывода: полные совпадения с номерами строк...| —
`write_file`| Запись содержимого в файл с полной заменой существующего содержимого. Используйте вместо echo/cat heredoc в терминале. Автоматически создает родительские каталоги. ПЕРЕЗАПИСЫВАЕТ весь файл — используйте 'patch' для целевых правок.| —
## `homeassistant` toolset[​](<#homeassistant-toolset> "Direct link to homeassistant-toolset")
Tool| Description| Requires environment
|---|---|---
`ha_call_service`| Вызов сервиса Home Assistant для управления устройством. Используйте ha_list_services для обнаружения доступных сервисов и их параметров для каждого домена.| —
`ha_get_state`| Получение детального состояния одной сущности Home Assistant, включая все атрибуты (яркость, цвет, уставка температуры, показания датчиков и т.д.).| —
`ha_list_entities`| Список сущностей Home Assistant. Опционально фильтрация по домену (light, switch, climate, sensor, binary_sensor, cover, fan и т.д.) или по имени зоны (гостиная, кухня, спальня и т.д.).| —
`ha_list_services`| Список доступных сервисов Home Assistant (действий) для управления устройствами. Показывает, какие действия можно выполнять с каждым типом устройств и какие параметры они принимают. Используйте для обнаружения способов управления устройствами, найденными через ha_list_entities.| —
note
**Инструменты Honcho** (`honcho_profile`, `honcho_search`, `honcho_context`, `honcho_reasoning`, `honcho_conclude`) больше не являются встроенными. Они доступны через плагин провайдера памяти Honcho в `plugins/memory/honcho/`. См. [Memory Providers](</docs/user-guide/features/memory-providers>) для установки и использования.
## `image_gen` toolset[​](<#image_gen-toolset> "Direct link to image_gen-toolset")
Tool| Description| Requires environment
|---|---|---
`image_generate`| Генерация высококачественных изображений по текстовым запросам с использованием FAL.ai. Используемая модель настраивается пользователем (по умолчанию: FLUX 2 Klein 9B, генерация менее 1 секунды) и не выбирается агентом. Возвращает один URL изображения. Отобразите его с помощью...| FAL_KEY
## `memory` toolset[​](<#memory-toolset> "Direct link to memory-toolset")
Tool| Description| Requires environment
|---|---|---
`memory`| Сохранение важной информации в постоянную память, которая сохраняется между сессиями. Ваша память появляется в системном промпте при запуске сессии — так вы запоминаете информацию о пользователе и своем окружении между разговорами. КОГДА СОХРАНЯТЬ...| —
## `messaging` toolset[​](<#messaging-toolset> "Direct link to messaging-toolset")
Tool| Description| Requires environment
|---|---|---
`send_message`| Отправка сообщения в подключенную платформу обмена сообщениями или список доступных целей. ВАЖНО: Когда пользователь просит отправить в конкретный канал или человеку (не просто название платформы), сначала вызовите send_message(action='list'), чтобы увидеть доступные цели...| —
## `moa` toolset[​](<#moa-toolset> "Direct link to moa-toolset")
Tool| Description| Requires environment
|---|---|---
`mixture_of_agents`| Маршрутизация сложной задачи через несколько frontier LLM совместно. Выполняет 5 API-вызовов (4 эталонные модели + 1 агрегатор) с максимальными усилиями рассуждения — используйте экономно для действительно сложных задач. Лучше всего подходит для: сложной математики, продвинутых алгоритмов...| OPENROUTER_API_KEY
## `rl` toolset[​](<#rl-toolset> "Direct link to rl-toolset")
Tool| Description| Requires environment
|---|---|---
`rl_check_status`| Получение статуса и метрик для запуска обучения. С ОГРАНИЧЕНИЕМ СКОРОСТИ: минимум 30 минут между проверками для одного и того же запуска. Возвращает метрики WandB: step, state, reward_mean, loss, percent_correct.| TINKER_API_KEY, WANDB_API_KEY
`rl_edit_config`| Обновление поля конфигурации. Сначала используйте rl_get_current_config(), чтобы увидеть все доступные поля для выбранной среды. Каждая среда имеет разные настраиваемые опции. Параметры инфраструктуры (tokenizer, URLs, lora_rank, learning_rate...| TINKER_API_KEY, WANDB_API_KEY
`rl_get_current_config`| Получение текущей конфигурации среды. Возвращает только поля, которые могут быть изменены: group_size, max_token_length, total_steps, steps_per_eval, use_wandb, wandb_name, max_num_workers.| TINKER_API_KEY, WANDB_API_KEY
`rl_get_results`| Получение финальных результатов и метрик завершенного запуска обучения. Возвращает финальные метрики и путь к обученным весам.| TINKER_API_KEY, WANDB_API_KEY
`rl_list_environments`| Список всех доступных сред RL. Возвращает названия сред, пути и описания. СОВЕТ: Прочитайте file_path с помощью файловых инструментов, чтобы понять, как работает каждая среда (верификаторы, загрузка данных, награды).| TINKER_API_KEY, WANDB_API_KEY
`rl_list_runs`| Список всех запусков обучения (активных и завершенных) с их статусом.| TINKER_API_KEY, WANDB_API_KEY
`rl_select_environment`| Выбор среды RL для обучения. Загружает конфигурацию среды по умолчанию. После выбора используйте rl_get_current_config() для просмотра настроек и rl_edit_config() для их изменения.| TINKER_API_KEY, WANDB_API_KEY
`rl_start_training`| Запуск нового обучения RL с текущей средой и конфигурацией. Большинство параметров обучения (lora_rank, learning_rate и т.д.) фиксированы. Используйте rl_edit_config() для установки group_size, batch_size, wandb_project перед запуском. ПРЕДУПРЕЖДЕНИЕ: Обучение...| TINKER_API_KEY, WANDB_API_KEY
`rl_stop_training`| Остановка выполняющегося задания обучения. Используйте, если метрики выглядят плохо, обучение停滞 (застопорилось) или вы хотите попробовать другие настройки.| TINKER_API_KEY, WANDB_API_KEY
`rl_test_inference`| Быстрый тест инференса для любой среды. Выполняет несколько шагов инференса + оценки через OpenRouter. По умолчанию: 3 шага x 16 завершений = 48 разверток на модель, тестирование 3 моделей = 144 всего. Тестирует загрузку среды, построение промпта, ин...| TINKER_API_KEY, WANDB_API_KEY
## `session_search` toolset[​](<#session_search-toolset> "Direct link to session_search-toolset")
Tool| Description| Requires environment
|---|---|---
`session_search`| Поиск в вашей долговременной памяти прошлых разговоров. Это ваша способность вспоминать — каждая прошлая сессия доступна для поиска, и этот инструмент суммирует произошедшее. ИСПОЛЬЗУЙТЕ ЭТО ПРОАКТИВНО, когда: - Пользователь говорит 'мы делали это раньше', 'помнишь, когда', 'в прошлый ра...| —
## `skills` toolset[​](<#skills-toolset> "Direct link to skills-toolset")
Tool| Description| Requires environment
|---|---|---
`skill_manage`| Управление навыками (создание, обновление, удаление). Навыки — это ваша процедурная память — многократно используемые подходы для recurring типов задач. Новые навыки сохраняются в ~/.hermes/skills/; существующие навыки могут быть изменены независимо от их расположения. Действия: create (полный SKILL.m...| —
`skill_view`| Навыки позволяют загружать информацию о конкретных задачах и рабочих процессах, а также скрипты и шаблоны. Загружает полное содержимое навыка или открывает доступ к его связанным файлам (ссылки, шаблоны, скрипты). Первый вызов возвращает содержимое SKILL.md плюс с...| —
`skills_list`| Список доступных навыков (имя + описание). Используйте skill_view(name) для загрузки полного содержимого.| —
## `terminal` toolset[​](<#terminal-toolset> "Direct link to terminal-toolset")
Tool| Description| Requires environment
|---|---|---
`process`| Управление фоновыми процессами, запущенными с terminal(background=true). Действия: 'list' (показать все), 'poll' (проверить статус + новый вывод), 'log' (полный вывод с постраничным просмотром), 'wait' (ждать завершения или тайм-аута), 'kill' (завершить), 'write' (от...| —
`terminal`| Выполнение shell-команд в среде Linux. Файловая система сохраняется между вызовами. Установите `background=true` для долго работающих серверов. Установите `notify_on_complete=true` (с `background=true`) для автоматического уведомления о завершении процесса — опрос не требуется. НЕ ИСПОЛЬЗУЙТЕ cat/head/tail — используйте read_file. НЕ ИСПОЛЬЗУЙТЕ grep/rg/find — используйте search_files.| —
## `todo` toolset[​](<#todo-toolset> "Direct link to todo-toolset")
Tool| Description| Requires environment
|---|---|---
`todo`| Управление списком задач для текущей сессии. Используйте для сложных задач с 3+ шагами или когда пользователь дает несколько задач. Вызов без параметров для чтения текущего списка. Запись: - Передайте массив 'todos' для создания/обновления элементов - merge=...| —
## `vision` toolset[​](<#vision-toolset> "Direct link to vision-toolset")
Tool| Description| Requires environment
|---|---|---
`vision_analyze`| Анализ изображений с помощью AI vision. Предоставляет подробное описание и отвечает на конкретный вопрос о содержимом изображения.| —
## `web` toolset[​](<#web-toolset> "Direct link to web-toolset")
Tool| Description| Requires environment
|---|---|---
`web_search`| Поиск информации в интернете. Возвращает до 5 результатов по умолчанию с заголовками, URL и описаниями. Принимает опциональный `limit` (1-100, по умолчанию 5). Запрос передается настроенному бэкенду, поэтому операторы типа `site:domain`, `filetype:pdf`, `intitle:word`, `-term` и `\"точная фраза\"` могут работать, если бэкенд их поддерживает.| EXA_API_KEY или PARALLEL_API_KEY или FIRECRAWL_API_KEY или TAVILY_API_KEY
`web_extract`| Извлечение содержимого URL веб-страниц. Возвращает содержимое страницы в формате markdown. Также работает с URL PDF — передайте прямую ссылку на PDF, и она будет преобразована в markdown-текст. Страницы менее 5000 символов возвращают полный markdown; большие страницы суммаризируются LLM.| EXA_API_KEY или PARALLEL_API_KEY или FIRECRAWL_API_KEY или TAVILY_API_KEY
## `tts` toolset[​](<#tts-toolset> "Direct link to tts-toolset")
Tool| Description| Requires environment
|---|---|---
`text_to_speech`| Преобразование текста в аудио. Возвращает путь MEDIA:, который платформа доставляет как голосовое сообщение. В Telegram воспроизводится как голосовой пузырек, в Discord/WhatsApp как аудиовложение. В режиме CLI сохраняется в ~/voice-memos/. Голос и провайдер...| —
## `discord` toolset[​](<#discord-toolset> "Direct link to discord-toolset")
Зарегистрирован в наборе инструментов платформы `hermes-discord` (только шлюз). Использует тот же токен бота, что и адаптер обмена сообщениями.
Tool| Description| Requires environment
|---|---|---
`discord`| Чтение и участие в Discord-сервере. Действия включают `search_members`, `fetch_messages`, `send_message`, `react`, `fetch_channel`, `list_channels` и другие.| `DISCORD_BOT_TOKEN`
## `discord_admin` toolset[​](<#discord_admin-toolset> "Direct link to discord_admin-toolset")
Зарегистрирован в наборе инструментов платформы `hermes-discord`. Действия модерации требуют, чтобы бот имел соответствующие разрешения Discord.
Tool| Description| Requires environment
|---|---|---
`discord_admin`| Управление Discord-сервером через REST API: список guilds/каналов/ролей, создание/редактирование/удаление каналов, управление правами ролей, тайм-ауты, кики и баны.| `DISCORD_BOT_TOKEN` \\+ разрешения бота
## `spotify` toolset[​](<#spotify-toolset> "Direct link to spotify-toolset")
Регистрируется встроенным плагином `spotify`. Требуется OAuth-токен — запустите `hermes spotify setup` один раз для авторизации.
Tool| Description| Requires environment
|---|---|---
`spotify_playback`| Управление воспроизведением Spotify, проверка активного состояния воспроизведения или получение недавно прослушанных треков.| Spotify OAuth
`spotify_devices`| Список устройств Spotify Connect или перенос воспроизведения на другое устройство.| Spotify OAuth
`spotify_queue`| Просмотр очереди Spotify пользователя или добавление элемента в нее.| Spotify OAuth
`spotify_search`| Поиск в каталоге Spotify по трекам, альбомам, исполнителям, плейлистам, шоу или эпизодам.| Spotify OAuth
`spotify_playlists`| Список, просмотр, создание, обновление и изменение плейлистов Spotify.| Spotify OAuth
`spotify_albums`| Получение метаданных альбома Spotify или треков альбома.| Spotify OAuth
`spotify_library`| Список, сохранение или удаление сохраненных треков или альбомов Spotify пользователя.| Spotify OAuth
## `hermes-yuanbao` toolset[​](<#hermes-yuanbao-toolset> "Direct link to hermes-yuanbao-toolset")
Регистрируется только в наборе инструментов платформы `hermes-yuanbao`. Yuanbao — это чат-приложение Tencent; эти инструменты управляют его API для личных сообщений, групп и стикеров.
Tool| Description| Requires environment
|---|---|---
`yb_query_group_info`| Запрос базовой информации о группе (называется \"派/Pai\" в приложении): название, владелец, количество участников.| Учетные данные Yuanbao
`yb_query_group_members`| Запрос участников группы (для упоминаний через `@`, поиска пользователя по имени, списка ботов).| Учетные данные Yuanbao
`yb_send_dm`| Отправка личного/прямого сообщения пользователю в группе с опциональными медиафайлами.| Учетные данные Yuanbao
`yb_search_sticker`| Поиск во встроенном каталоге стикеров Yuanbao (TIM face) по ключевому слову.| Учетные данные Yuanbao
`yb_send_sticker`| Отправка встроенного стикера в текущий чат Yuanbao.| Учетные данные Yuanbao
  * [`browser` toolset](<#browser-toolset>)
  * [`browser-cdp` toolset](<#browser-cdp-toolset>)
  * [`clarify` toolset](<#clarify-toolset>)
  * [`code_execution` toolset](<#code_execution-toolset>)
  * [`cronjob` toolset](<#cronjob-toolset>)
  * [`delegation` toolset](<#delegation-toolset>)
  * [`feishu_doc` toolset](<#feishu_doc-toolset>)
  * [`feishu_drive` toolset](<#feishu_drive-toolset>)
  * [`file` toolset](<#file-toolset>)
  * [`homeassistant` toolset](<#homeassistant-toolset>)
  * [`image_gen` toolset](<#image_gen-toolset>)
  * [`memory` toolset](<#memory-toolset>)
  * [`messaging` toolset](<#messaging-toolset>)
  * [`moa` toolset](<#moa-toolset>)
  * [`rl` toolset](<#rl-toolset>)
  * [`session_search` toolset](<#session_search-toolset>)
  * [`skills` toolset](<#skills-toolset>)
  * [`terminal` toolset](<#terminal-toolset>)
  * [`todo` toolset](<#todo-toolset>)
  * [`vision` toolset](<#vision-toolset>)
  * [`web` toolset](<#web-toolset>)
  * [`tts` toolset](<#tts-toolset>)
  * [`discord` toolset](<#discord-toolset>)
  * [`discord_admin` toolset](<#discord_admin-toolset>)
  * [`spotify` toolset](<#spotify-toolset>)
  * [`hermes-yuanbao` toolset](<#hermes-yuanbao-toolset>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/tools-reference -->
