On this page

Hermes поставляется с большой встроенной библиотекой навыков, которая копируется в `~/.hermes/skills/` при установке. Каждый навык ниже ведёт на отдельную страницу с его полным определением, настройкой и использованием.

Hermes также синхронизирует встроенные навыки при `hermes update`, но манифест синхронизации учитывает локальные удаления и изменения пользователя. Если навык из этого списка отсутствует в дереве `~/.hermes/skills/` вашего профиля, он всё равно поставляется с Hermes; восстановите его командой `hermes skills reset <name> --restore`.

Если навыка нет в этом списке, но он присутствует в репозитории, каталог можно перегенерировать скриптом `website/scripts/generate-skill-docs.py`.

## apple[​](<#apple> "Direct link to apple")

Skill| Описание| Path
|---|---|---
[`apple-notes`](</docs/user-guide/skills/bundled/apple/apple-apple-notes>)| Управление Apple Notes через memo CLI: создание, поиск, редактирование.| `apple/apple-notes`
[`apple-reminders`](</docs/user-guide/skills/bundled/apple/apple-apple-reminders>)| Apple Reminders через remindctl: добавление, просмотр, завершение.| `apple/apple-reminders`
[`findmy`](</docs/user-guide/skills/bundled/apple/apple-findmy>)| Отслеживание устройств Apple/AirTags через FindMy.app на macOS.| `apple/findmy`
[`imessage`](</docs/user-guide/skills/bundled/apple/apple-imessage>)| Отправка и получение iMessages/SMS через imsg CLI на macOS.| `apple/imessage`

## autonomous-ai-agents[​](<#autonomous-ai-agents> "Direct link to autonomous-ai-agents")

Skill| Описание| Path
|---|---|---
[`claude-code`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code>)| Делегирование кодинга Claude Code CLI (фичи, PRs).| `autonomous-ai-agents/claude-code`
[`codex`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>)| Делегирование кодинга OpenAI Codex CLI (фичи, PRs).| `autonomous-ai-agents/codex`
[`hermes-agent`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent>)| Настройка, расширение или участие в разработке Hermes Agent.| `autonomous-ai-agents/hermes-agent`
[`opencode`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode>)| Делегирование кодинга OpenCode CLI (фичи, ревью PR).| `autonomous-ai-agents/opencode`

## creative[​](<#creative> "Direct link to creative")

Skill| Описание| Path
|---|---|---
[`architecture-diagram`](</docs/user-guide/skills/bundled/creative/creative-architecture-diagram>)| SVG-диаграммы архитектуры/облака/инфраструктуры в тёмной теме как HTML.| `creative/architecture-diagram`
[`ascii-art`](</docs/user-guide/skills/bundled/creative/creative-ascii-art>)| ASCII-арт: pyfiglet, cowsay, boxes, image-to-ascii.| `creative/ascii-art`
[`ascii-video`](</docs/user-guide/skills/bundled/creative/creative-ascii-video>)| ASCII-видео: конвертация видео/аудио в цветной ASCII MP4/GIF.| `creative/ascii-video`
[`baoyu-comic`](</docs/user-guide/skills/bundled/creative/creative-baoyu-comic>)| Обучающие комиксы (知识漫画): образовательные, биографии, туториалы.| `creative/baoyu-comic`
[`baoyu-infographic`](</docs/user-guide/skills/bundled/creative/creative-baoyu-infographic>)| Инфографика: 21 макет x 21 стиль (信息图, 可视化).| `creative/baoyu-infographic`
[`claude-design`](</docs/user-guide/skills/bundled/creative/creative-claude-design>)| Создание одноразовых HTML-артефактов (лендинг, презентация, прототип).| `creative/claude-design`
[`comfyui`](</docs/user-guide/skills/bundled/creative/creative-comfyui>)| Генерация изображений, видео и аудио с ComfyUI — установка, запуск, управление узлами/моделями, запуск рабочих процессов с инъекцией параметров. Использует официальный comfy-cli для жизненного цикла и прямой REST/WebSocket API для выполнения.| `creative/comfyui`
[`ideation`](</docs/user-guide/skills/bundled/creative/creative-creative-ideation>)| Генерация идей проектов через творческие ограничения.| `creative/creative-ideation`
[`design-md`](</docs/user-guide/skills/bundled/creative/creative-design-md>)| Создание/валидация/экспорт файлов спецификации токенов Google DESIGN.md.| `creative/design-md`
[`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>)| Диаграммы Excalidraw в формате JSON от руки (архитектура, поток, последовательность).| `creative/excalidraw`
[`humanizer`](</docs/user-guide/skills/bundled/creative/creative-humanizer>)| Очеловечивание текста: удаление AI-маркеров и добавление живого голоса.| `creative/humanizer`
[`manim-video`](</docs/user-guide/skills/bundled/creative/creative-manim-video>)| Анимации Manim CE: математические/алгоритмические видео в стиле 3Blue1Brown.| `creative/manim-video`
[`p5js`](</docs/user-guide/skills/bundled/creative/creative-p5js>)| Скетчи p5.js: генеративное искусство, шейдеры, интерактив, 3D.| `creative/p5js`
[`pixel-art`](</docs/user-guide/skills/bundled/creative/creative-pixel-art>)| Пиксель-арт с палитрами эпох (NES, Game Boy, PICO-8).| `creative/pixel-art`
[`popular-web-designs`](</docs/user-guide/skills/bundled/creative/creative-popular-web-designs>)| 54 реальных дизайн-системы (Stripe, Linear, Vercel) в HTML/CSS.| `creative/popular-web-designs`
[`pretext`](</docs/user-guide/skills/bundled/creative/creative-pretext>)| Используйте при создании креативных браузерных демо с @chenglou/pretext — верстка текста без DOM для ASCII-арта, типографический поток вокруг препятствий, игры «текст-как-геометрия», кинетическая типографика и генеративное искусство на основе текста. Создаёт однофайловый HT...| `creative/pretext`
[`sketch`](</docs/user-guide/skills/bundled/creative/creative-sketch>)| Одноразовые HTML-макеты: 2-3 варианта дизайна для сравнения.| `creative/sketch`
[`songwriting-and-ai-music`](</docs/user-guide/skills/bundled/creative/creative-songwriting-and-ai-music>)| Мастерство написания песен и музыкальные промпты Suno AI.| `creative/songwriting-and-ai-music`
[`touchdesigner-mcp`](</docs/user-guide/skills/bundled/creative/creative-touchdesigner-mcp>)| Управление запущенным экземпляром TouchDesigner через twozero MCP — создание операторов, установка параметров, соединения, выполнение Python, создание визуализаций в реальном времени. 36 встроенных инструментов.| `creative/touchdesigner-mcp`

## data-science[​](<#data-science> "Direct link to data-science")

Skill| Описание| Path
|---|---|---
[`jupyter-live-kernel`](</docs/user-guide/skills/bundled/data-science/data-science-jupyter-live-kernel>)| Итеративный Python через живой Jupyter-ядро (hamelnb).| `data-science/jupyter-live-kernel`

## devops[​](<#devops> "Direct link to devops")

Skill| Описание| Path
|---|---|---
[`kanban-orchestrator`](</docs/user-guide/skills/bundled/devops/devops-kanban-orchestrator>)| Плейбук декомпозиции + соглашения о ролях специалистов + правила анти-искушения для профиля оркестратора, направляющего работу через Kanban. Правило «не делай работу сам» и базовый жизненный цикл автоматически внедряются в каждый kanban wor...| `devops/kanban-orchestrator`
[`kanban-worker`](</docs/user-guide/skills/bundled/devops/devops-kanban-worker>)| Подводные камни, примеры и граничные случаи для работников Hermes Kanban. Сам жизненный цикл автоматически внедряется в системный промпт каждого работника как KANBAN_GUIDANCE (из agent/prompt_builder.py); этот навык загружается, когда нужно более глубокое оп...| `devops/kanban-worker`
[`webhook-subscriptions`](</docs/user-guide/skills/bundled/devops/devops-webhook-subscriptions>)| Подписки на вебхуки: событийно-ориентированные запуски агента.| `devops/webhook-subscriptions`

## dogfood[​](<#dogfood> "Direct link to dogfood")

Skill| Описание| Path
|---|---|---
[`dogfood`](</docs/user-guide/skills/bundled/dogfood/dogfood-dogfood>)| Исследовательское QA веб-приложений: поиск багов, доказательств, отчётов.| `dogfood`

## email[​](<#email> "Direct link to email")

Skill| Описание| Path
|---|---|---
[`himalaya`](</docs/user-guide/skills/bundled/email/email-himalaya>)| Himalaya CLI: IMAP/SMTP электронная почта из терминала.| `email/himalaya`

## gaming[​](<#gaming> "Direct link to gaming")

Skill| Описание| Path
|---|---|---
[`minecraft-modpack-server`](</docs/user-guide/skills/bundled/gaming/gaming-minecraft-modpack-server>)| Хостинг модифицированных серверов Minecraft (CurseForge, Modrinth).| `gaming/minecraft-modpack-server`
[`pokemon-player`](</docs/user-guide/skills/bundled/gaming/gaming-pokemon-player>)| Игра в Pokemon через headless-эмулятор + чтение RAM.| `gaming/pokemon-player`

## github[​](<#github> "Direct link to github")

Skill| Описание| Path
|---|---|---
[`codebase-inspection`](</docs/user-guide/skills/bundled/github/github-codebase-inspection>)| Инспекция кодовых баз с pygount: LOC, языки, соотношения.| `github/codebase-inspection`
[`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>)| Настройка GitHub аутентификации: HTTPS токены, SSH ключи, gh CLI логин.| `github/github-auth`
[`github-code-review`](</docs/user-guide/skills/bundled/github/github-github-code-review>)| Ревью PR: diffs, инлайн-комментарии через gh или REST.| `github/github-code-review`
[`github-issues`](</docs/user-guide/skills/bundled/github/github-github-issues>)| Создание, триаж, маркировка, назначение GitHub issues через gh или REST.| `github/github-issues`
[`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>)| Жизненный цикл GitHub PR: ветка, коммит, открытие, CI, слияние.| `github/github-pr-workflow`
[`github-repo-management`](</docs/user-guide/skills/bundled/github/github-github-repo-management>)| Клонирование/создание/форк репозиториев; управление удалёнными репозиториями, релизами.| `github/github-repo-management`

## mcp[​](<#mcp> "Direct link to mcp")

Skill| Описание| Path
|---|---|---
[`native-mcp`](</docs/user-guide/skills/bundled/mcp/mcp-native-mcp>)| MCP клиент: подключение серверов, регистрация инструментов (stdio/HTTP).| `mcp/native-mcp`

## media[​](<#media> "Direct link to media")

Skill| Описание| Path
|---|---|---
[`gif-search`](</docs/user-guide/skills/bundled/media/media-gif-search>)| Поиск/скачивание GIF с Tenor через curl + jq.| `media/gif-search`
[`heartmula`](</docs/user-guide/skills/bundled/media/media-heartmula>)| HeartMuLa: генерация песен в стиле Suno из текста + тегов.| `media/heartmula`
[`songsee`](</docs/user-guide/skills/bundled/media/media-songsee>)| Аудио спектрограммы/признаки (mel, chroma, MFCC) через CLI.| `media/songsee`
[`spotify`](</docs/user-guide/skills/bundled/media/media-spotify>)| Spotify: воспроизведение, поиск, очередь, управление плейлистами и устройствами.| `media/spotify`
[`youtube-content`](</docs/user-guide/skills/bundled/media/media-youtube-content>)| Транскрипты YouTube в саммари, треды, блоги.| `media/youtube-content`

## mlops[​](<#mlops> "Direct link to mlops")

Skill| Описание| Path
|---|---|---
[`audiocraft-audio-generation`](</docs/user-guide/skills/bundled/mlops/mlops-models-audiocraft>)| AudioCraft: MusicGen текст-в-музыку, AudioGen текст-в-звук.| `mlops/models/audiocraft`
[`axolotl`](</docs/user-guide/skills/bundled/mlops/mlops-training-axolotl>)| Axolotl: YAML тонкая настройка LLM (LoRA, DPO, GRPO).| `mlops/training/axolotl`
[`dspy`](</docs/user-guide/skills/bundled/mlops/mlops-research-dspy>)| DSPy: декларативные LM-программы, авто-оптимизация промптов, RAG.| `mlops/research/dspy`
[`huggingface-hub`](</docs/user-guide/skills/bundled/mlops/mlops-huggingface-hub>)| HuggingFace hf CLI: поиск/скачивание/загрузка моделей, датасетов.| `mlops/huggingface-hub`
[`llama-cpp`](</docs/user-guide/skills/bundled/mlops/mlops-inference-llama-cpp>)| llama.cpp локальный GGPU инференс + HF Hub поиск моделей.| `mlops/inference/llama-cpp`
[`evaluating-llms-harness`](</docs/user-guide/skills/bundled/mlops/mlops-evaluation-lm-evaluation-harness>)| lm-eval-harness: бенчмаркинг LLM (MMLU, GSM8K и др.).| `mlops/evaluation/lm-evaluation-harness`
[`obliteratus`](</docs/user-guide/skills/bundled/mlops/mlops-inference-obliteratus>)| OBLITERATUS: аблитерация отказов LLM (diff-in-means).| `mlops/inference/obliteratus`
[`outlines`](</docs/user-guide/skills/bundled/mlops/mlops-inference-outlines>)| Outlines: структурированная JSON/regex/Pydantic генерация LLM.| `mlops/inference/outlines`
[`segment-anything-model`](</docs/user-guide/skills/bundled/mlops/mlops-models-segment-anything>)| SAM: zero-shot сегментация изображений по точкам, рамкам, маскам.| `mlops/models/segment-anything`
[`fine-tuning-with-trl`](</docs/user-guide/skills/bundled/mlops/mlops-training-trl-fine-tuning>)| TRL: SFT, DPO, PPO, GRPO, моделирование вознаграждения для RLHF LLM.| `mlops/training/trl-fine-tuning`
[`unsloth`](</docs/user-guide/skills/bundled/mlops/mlops-training-unsloth>)| Unsloth: в 2-5x более быстрая LoRA/QLoRA тонкая настройка, меньше VRAM.| `mlops/training/unsloth`
[`serving-llms-vllm`](</docs/user-guide/skills/bundled/mlops/mlops-inference-vllm>)| vLLM: высокопроизводительный сервинг LLM, OpenAI API, квантизация.| `mlops/inference/vllm`
[`weights-and-biases`](</docs/user-guide/skills/bundled/mlops/mlops-evaluation-weights-and-biases>)| W&B: логирование ML экспериментов, sweeps, реестр моделей, дашборды.| `mlops/evaluation/weights-and-biases`

## note-taking[​](<#note-taking> "Direct link to note-taking")

Skill| Описание| Path
|---|---|---
[`obsidian`](</docs/user-guide/skills/bundled/note-taking/note-taking-obsidian>)| Чтение, поиск, создание и редактирование заметок в хранилище Obsidian.| `note-taking/obsidian`

## productivity[​](<#productivity> "Direct link to productivity")

Skill| Описание| Path
|---|---|---
[`airtable`](</docs/user-guide/skills/bundled/productivity/productivity-airtable>)| REST API Airtable через curl. CRUD записей, фильтры, апсерты.| `productivity/airtable`
[`google-workspace`](</docs/user-guide/skills/bundled/productivity/productivity-google-workspace>)| Gmail, Calendar, Drive, Docs, Sheets через gws CLI или Python.| `productivity/google-workspace`
[`linear`](</docs/user-guide/skills/bundled/productivity/productivity-linear>)| Linear: управление задачами, проектами, командами через GraphQL + curl.| `productivity/linear`
[`maps`](</docs/user-guide/skills/bundled/productivity/productivity-maps>)| Геокодирование, POI, маршруты, часовые пояса через OpenStreetMap/OSRM.| `productivity/maps`
[`nano-pdf`](</docs/user-guide/skills/bundled/productivity/productivity-nano-pdf>)| Редактирование текста/опечаток/заголовков PDF через nano-pdf CLI (NL-промпты).| `productivity/nano-pdf`
[`notion`](</docs/user-guide/skills/bundled/productivity/productivity-notion>)| Notion API через curl: страницы, базы данных, блоки, поиск.| `productivity/notion`
[`ocr-and-documents`](</docs/user-guide/skills/bundled/productivity/productivity-ocr-and-documents>)| Извлечение текста из PDF/сканов (pymupdf, marker-pdf).| `productivity/ocr-and-documents`
[`powerpoint`](</docs/user-guide/skills/bundled/productivity/productivity-powerpoint>)| Создание, чтение, редактирование .pptx презентаций, слайдов, заметок, шаблонов.| `productivity/powerpoint`

## red-teaming[​](<#red-teaming> "Direct link to red-teaming")

Skill| Описание| Path
|---|---|---
[`godmode`](</docs/user-guide/skills/bundled/red-teaming/red-teaming-godmode>)| Джейлбрейк LLM: Parseltongue, GODMODE, ULTRAPLINIAN.| `red-teaming/godmode`

## research[​](<#research> "Direct link to research")

Skill| Описание| Path
|---|---|---
[`arxiv`](</docs/user-guide/skills/bundled/research/research-arxiv>)| Поиск статей arXiv по ключевым словам, автору, категории или ID.| `research/arxiv`
[`blogwatcher`](</docs/user-guide/skills/bundled/research/research-blogwatcher>)| Мониторинг блогов и RSS/Atom лент через blogwatcher-cli.| `research/blogwatcher`
[`llm-wiki`](</docs/user-guide/skills/bundled/research/research-llm-wiki>)| Karpathy's LLM Wiki: создание/запросы взаимосвязанной markdown базы знаний.| `research/llm-wiki`
[`polymarket`](</docs/user-guide/skills/bundled/research/research-polymarket>)| Запросы Polymarket: рынки, цены, книги ордеров, история.| `research/polymarket`
[`research-paper-writing`](</docs/user-guide/skills/bundled/research/research-research-paper-writing>)| Написание ML статей для NeurIPS/ICML/ICLR: от дизайна до подачи.| `research/research-paper-writing`

## smart-home[​](<#smart-home> "Direct link to smart-home")

Skill| Описание| Path
|---|---|---
[`openhue`](</docs/user-guide/skills/bundled/smart-home/smart-home-openhue>)| Управление Philips Hue лампами, сценами, комнатами через OpenHue CLI.| `smart-home/openhue`

## social-media[​](<#social-media> "Direct link to social-media")

Skill| Описание| Path
|---|---|---
[`xurl`](</docs/user-guide/skills/bundled/social-media/social-media-xurl>)| X/Twitter через xurl CLI: пост, поиск, DM, медиа, v2 API.| `social-media/xurl`

## software-development[​](<#software-development> "Direct link to software-development")

Skill| Описание| Path
|---|---|---
[`debugging-hermes-tui-commands`](</docs/user-guide/skills/bundled/software-development/software-development-debugging-hermes-tui-commands>)| Отладка слэш-команд Hermes TUI: Python, шлюз, Ink UI.| `software-development/debugging-hermes-tui-commands`
[`hermes-agent-skill-authoring`](</docs/user-guide/skills/bundled/software-development/software-development-hermes-agent-skill-authoring>)| Создание SKILL.md в репозитории: frontmatter, валидатор, структура.| `software-development/hermes-agent-skill-authoring`
[`node-inspect-debugger`](</docs/user-guide/skills/bundled/software-development/software-development-node-inspect-debugger>)| Отладка Node.js через --inspect + Chrome DevTools Protocol CLI.| `software-development/node-inspect-debugger`
[`plan`](</docs/user-guide/skills/bundled/software-development/software-development-plan>)| Режим планирования: запись markdown плана в .hermes/plans/, без выполнения.| `software-development/plan`
[`python-debugpy`](</docs/user-guide/skills/bundled/software-development/software-development-python-debugpy>)| Отладка Python: pdb REPL + debugpy удалённо (DAP).| `software-development/python-debugpy`
[`requesting-code-review`](</docs/user-guide/skills/bundled/software-development/software-development-requesting-code-review>)| Предкоммитное ревью: сканирование безопасности, контроль качества, авто-исправление.| `software-development/requesting-code-review`
[`spike`](</docs/user-guide/skills/bundled/software-development/software-development-spike>)| Одноразовые эксперименты для проверки идеи перед разработкой.| `software-development/spike`
[`subagent-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development>)| Выполнение планов через delegate_task саб-агентов (2-этапное ревью).| `software-development/subagent-driven-development`
[`systematic-debugging`](</docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging>)| 4-фазная отладка первопричины: понимание багов перед исправлением.| `software-development/systematic-debugging`
[`test-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-test-driven-development>)| TDD: соблюдение RED-GREEN-REFACTOR, тесты перед кодом.| `software-development/test-driven-development`
[`writing-plans`](</docs/user-guide/skills/bundled/software-development/software-development-writing-plans>)| Написание планов реализации: небольшие задачи, пути, код.| `software-development/writing-plans`

## yuanbao[​](<#yuanbao> "Direct link to yuanbao")

Skill| Описание| Path
|---|---|---
[`yuanbao`](</docs/user-guide/skills/bundled/yuanbao/yuanbao-yuanbao>)| Yuanbao (元宝) группы: @упоминания пользователей, запрос информации/участников.| `yuanbao`

  * [apple](<#apple>)
  * [autonomous-ai-agents](<#autonomous-ai-agents>)
  * [creative](<#creative>)
  * [data-science](<#data-science>)
  * [devops](<#devops>)
  * [dogfood](<#dogfood>)
  * [email](<#email>)
  * [gaming](<#gaming>)
  * [github](<#github>)
  * [mcp](<#mcp>)
  * [media](<#media>)
  * [mlops](<#mlops>)
  * [note-taking](<#note-taking>)
  * [productivity](<#productivity>)
  * [red-teaming](<#red-teaming>)
  * [research](<#research>)
  * [smart-home](<#smart-home>)
  * [social-media](<#social-media>)
  * [software-development](<#software-development>)
  * [yuanbao](<#yuanbao>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/skills-catalog -->
