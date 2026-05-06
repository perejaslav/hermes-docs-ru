На этой странице
Опциональные навыки поставляются с hermes-agent в папке `optional-skills/`, но **не активны по умолчанию**. Установите их явно:
[code] 
    hermes skills install official/<категория>/<навык>  
    
[/code]
Например:
[code] 
    hermes skills install official/blockchain/solana  
    hermes skills install official/mlops/flash-attention  
    
[/code]
Каждый навык ниже содержит ссылку на соответствующую страницу с полным определением, настройкой и использованием.
Чтобы удалить:
[code] 
    hermes skills uninstall <имя-навыка>  
    
[/code]
## autonomous-ai-agents[​](<#autonomous-ai-agents> "Прямая ссылка на autonomous-ai-agents")
Навык| Описание  
---|---  
[**blackbox**](</docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-blackbox>)|  Делегирование задач кодирования CLI-агенту Blackbox AI. Мульти-модельный агент со встроенным судьёй, который запускает задачи через несколько LLM и выбирает лучший результат. Требуется CLI blackbox и API-ключ Blackbox AI.  
[**honcho**](</docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-honcho>)|  Настройка и использование памяти Honcho с Hermes — межсессионное моделирование пользователя, изоляция нескольких профилей, конфигурация наблюдений, диалектическое рассуждение, сводки сессий и контроль бюджета контекста. Используйте при настройке Honcho, устранении неполадок...  
## blockchain[​](<#blockchain> "Прямая ссылка на blockchain")
Навык| Описание  
---|---  
[**base**](</docs/user-guide/skills/optional/blockchain/blockchain-base>)|  Запросы к блокчейну Base (Ethereum L2) с ценами в USD — балансы кошельков, информация о токенах, детали транзакций, анализ газа, проверка контрактов, обнаружение «китов» и статистика сети в реальном времени. Использует Base RPC + CoinGecko. API-ключ не требуется.  
[**solana**](</docs/user-guide/skills/optional/blockchain/blockchain-solana>)|  Запросы к блокчейну Solana с ценами в USD — балансы кошельков, портфели токенов с оценкой, детали транзакций, NFT, обнаружение «китов» и статистика сети в реальном времени. Использует Solana RPC + CoinGecko. API-ключ не требуется.  
## communication[​](<#communication> "Прямая ссылка на communication")
Навык| Описание  
---|---  
[**one-three-one-rule**](</docs/user-guide/skills/optional/communication/communication-one-three-one-rule>)|  Структурированная система принятия решений для технических предложений и анализа компромиссов. Когда пользователь стоит перед выбором между несколькими подходами (архитектурные решения, выбор инструментов, стратегии рефакторинга, пути миграции), этот навык п...  
## creative[​](<#creative> "Прямая ссылка на creative")
Навык| Описание  
---|---  
[**blender-mcp**](</docs/user-guide/skills/optional/creative/creative-blender-mcp>)|  Управление Blender напрямую из Hermes через socket-соединение с аддоном blender-mcp. Создание 3D-объектов, материалов, анимаций и выполнение произвольного Python-кода Blender (bpy). Используйте, когда пользователь хочет создать или изменить что-либо в Blender.  
[**concept-diagrams**](</docs/user-guide/skills/optional/creative/creative-concept-diagrams>)|  Генерация плоских минималистичных SVG-диаграмм с адаптацией под светлую/тёмную тему в виде отдельных HTML-файлов, использующих единый образовательный визуальный язык с 9 семантическими цветовыми рядами, типографикой в стиле предложений и автоматическим тёмным режимом. Лучше всего подходит для образовательных и н...  
[**hyperframes**](</docs/user-guide/skills/optional/creative/creative-hyperframes>)|  Создание HTML-видеокомпозиций, анимированных титров, социальных наложений, видео с говорящей головой с субтитрами, аудио-реактивных визуализаций и шейдерных переходов с помощью HyperFrames. HTML является источником истины для видео. Используйте, когда пользователь хочет...  
[**kanban-video-orchestrator**](</docs/user-guide/skills/optional/creative/creative-kanban-video-orchestrator>)|  Планирование, настройка и мониторинг мульти-агентного конвейера видеопроизводства на базе Hermes Kanban. Используйте, когда пользователь хочет создать ЛЮБОЕ видео — нарративный фильм, продукт/маркетинг, музыкальный клип, объясняющее видео, ASCII/терминальное искусство, абстрактный/генеративный ло...  
[**meme-generation**](</docs/user-guide/skills/optional/creative/creative-meme-generation>)|  Генерация настоящих изображений мемов путём выбора шаблона и наложения текста с помощью Pillow. Создаёт реальные .png файлы мемов.  
## devops[​](<#devops> "Прямая ссылка на devops")
Навык| Описание  
---|---  
[**inference-sh-cli**](</docs/user-guide/skills/optional/devops/devops-cli>)|  Запуск 150+ AI-приложений через CLI inference.sh (infsh) — генерация изображений, создание видео, LLM, поиск, 3D, социальная автоматизация. Использует инструмент терминала. Триггеры: inference.sh, infsh, ai apps, flux, veo, генерация изображений, генерация видео, seedrea...  
[**docker-management**](</docs/user-guide/skills/optional/devops/devops-docker-management>)|  Управление контейнерами Docker, образами, томами, сетями и стеками Compose — операции жизненного цикла, отладка, очистка и оптимизация Dockerfile.  
## dogfood[​](<#dogfood> "Прямая ссылка на dogfood")
Навык| Описание  
---|---  
[**adversarial-ux-test**](</docs/user-guide/skills/optional/dogfood/dogfood-adversarial-ux-test>)|  Сыграйте роль самого сложного, технически не подкованного пользователя вашего продукта. Изучите приложение как этот персонаж, найдите все болевые точки UX, затем отфильтруйте жалобы через слой прагматизма, чтобы отделить реальные проблемы от шума. Создаёт действенные тике...  
## email[​](<#email> "Прямая ссылка на email")
Навык| Описание  
---|---  
[**agentmail**](</docs/user-guide/skills/optional/email/email-agentmail>)|  Предоставьте агенту собственный выделенный почтовый ящик через AgentMail. Отправляйте, получайте и управляйте электронной почтой автономно, используя адреса электронной почты агента (например, [hermes-agent@agentmail.to](<mailto:hermes-agent@agentmail.to>)).  
## health[​](<#health> "Прямая ссылка на health")
Навык| Описание  
---|---  
[**fitness-nutrition**](</docs/user-guide/skills/optional/health/health-fitness-nutrition>)|  Планировщик тренировок в спортзале и трекер питания. Поиск 690+ упражнений по мышцам, оборудованию или категории через wger. Поиск макронутриентов и калорий для 380 000+ продуктов через USDA FoodData Central. Расчёт ИМТ, TDEE, одноповторного максимума, распределения макронутриентов и телос...  
[**neuroskill-bci**](</docs/user-guide/skills/optional/health/health-neuroskill-bci>)|  Подключение к запущенному экземпляру NeuroSkill и включение когнитивного и эмоционального состояния пользователя в реальном времени (фокус, расслабление, настроение, когнитивная нагрузка, сонливость, частота сердечных сокращений, HRV, стадии сна и 40+ производных EXG-оценок) в ответы....  
## mcp[​](<#mcp> "Прямая ссылка на mcp")
Навык| Описание  
---|---  
[**fastmcp**](</docs/user-guide/skills/optional/mcp/mcp-fastmcp>)|  Создание, тестирование, проверка, установка и развёртывание MCP-серверов с FastMCP на Python. Используйте при создании нового MCP-сервера, обёртывании API или базы данных в виде MCP-инструментов, предоставлении ресурсов или промптов, или подготовке FastMCP-сервера для Claude Code, Cur...  
[**mcporter**](</docs/user-guide/skills/optional/mcp/mcp-mcporter>)|  Использование CLI mcporter для вывода списка, настройки, аутентификации и вызова MCP-серверов/инструментов напрямую (HTTP или stdio), включая ad-hoc серверы, редактирование конфигурации и CLI/генерацию типов.  
## migration[​](<#migration> "Прямая ссылка на migration")
Навык| Описание  
---|---  
[**openclaw-migration**](</docs/user-guide/skills/optional/migration/migration-openclaw-migration>)|  Миграция следов кастомизации пользователя OpenClaw в Hermes Agent. Импортирует совместимые с Hermes воспоминания, SOUL.md, списки разрешённых команд, пользовательские навыки и выбранные рабочие ресурсы из ~/.openclaw, затем сообщает, что именно не удалось перенес...  
## mlops[​](<#mlops> "Прямая ссылка на mlops")
Навык| Описание  
---|---  
[**huggingface-accelerate**](</docs/user-guide/skills/optional/mlops/mlops-accelerate>)|  Простейший API распределённого обучения. 4 строки для добавления поддержки распределённых вычислений в любой PyTorch-скрипт. Единый API для DeepSpeed/FSDP/Megatron/DDP. Автоматическое размещение устройств, смешанная точность (FP16/BF16/FP8). Интерактивная конфигурация, единая команда за...  
[**chroma**](</docs/user-guide/skills/optional/mlops/mlops-chroma>)|  Открытая база данных эмбеддингов для AI-приложений. Хранение эмбеддингов и метаданных, выполнение векторного и полнотекстового поиска, фильтрация по метаданным. Простой 4-функциональный API. Масштабируется от блокнотов до производственных кластеров. Используйте для семантического поиска, RAG...  
[**clip**](</docs/user-guide/skills/optional/mlops/mlops-clip>)|  Модель OpenAI, соединяющая зрение и язык. Позволяет выполнять zero-shot классификацию изображений, сопоставление изображений с текстом и кросс-модальный поиск. Обучена на 400M парах изображение-текст. Используйте для поиска изображений, модерации контента или задач на стыке зрения и языка б...  
[**faiss**](</docs/user-guide/skills/optional/mlops/mlops-faiss>)|  Библиотека Facebook для эффективного поиска схожести и кластеризации плотных векторов. Поддерживает миллиарды векторов, GPU-ускорение и различные типы индексов (Flat, IVF, HNSW). Используйте для быстрого k-NN поиска, крупномасштабного векторного поиска или когда...  
[**optimizing-attention-flash**](</docs/user-guide/skills/optional/mlops/mlops-flash-attention>)|  Оптимизация внимания трансформеров с помощью Flash Attention для ускорения в 2-4 раза и снижения использования памяти в 10-20 раз. Используйте при обучении/запуске трансформеров с длинными последовательностями (>512 токенов), при возникновении проблем с памятью GPU при работе с attention, или когда требуется более быстрое ин...  
[**guidance**](</docs/user-guide/skills/optional/mlops/mlops-guidance>)|  Контроль вывода LLM с помощью regex и грамматик, гарантия генерации валидного JSON/XML/кода, обеспечение структурированных форматов и создание многошаговых рабочих процессов с Guidance — фреймворком ограниченной генерации от Microsoft Research  
[**hermes-atropos-environments**](</docs/user-guide/skills/optional/mlops/mlops-hermes-atropos-environments>)|  Создание, тестирование и отладка RL-сред Hermes Agent для обучения Atropos. Охватывает интерфейс HermesAgentBaseEnv, функции вознаграждения, интеграцию с циклом агента, оценку с инструментами, логирование wandb и три режима CLI (serve/process/eva...  
[**huggingface-tokenizers**](</docs/user-guide/skills/optional/mlops/mlops-huggingface-tokenizers>)|  Быстрые токенизаторы, оптимизированные для исследований и производства. Реализация на Rust токенизирует 1 ГБ менее чем за 20 секунд. Поддерживает алгоритмы BPE, WordPiece и Unigram. Обучение собственных словарей, отслеживание выравниваний, обработка дополнения/усечения. Интег...  
[**instructor**](</docs/user-guide/skills/optional/mlops/mlops-instructor>)|  Извлечение структурированных данных из ответов LLM с валидацией Pydantic, автоматический повтор неудачных извлечений, парсинг сложного JSON с типобезопасностью и потоковая передача частичных результатов с Instructor — проверенной в бою библиотекой структурированного вывода  
[**lambda-labs-gpu-cloud**](</docs/user-guide/skills/optional/mlops/mlops-lambda-labs>)|  Зарезервированные и по требованию GPU-инстансы в облаке для ML-обучения и инференса. Используйте, когда нужны выделенные GPU-инстансы с простым SSH-доступом, постоянными файловыми системами или высокопроизводительными мульти-узловыми кластерами для крупномасштабного обучения.  
[**llava**](</docs/user-guide/skills/optional/mlops/mlops-llava>)|  Large Language and Vision Assistant. Позволяет выполнять визуальную настройку инструкций и диалоги на основе изображений. Сочетает кодировщик зрения CLIP с языковыми моделями Vicuna/LLaMA. Поддерживает многошаговый чат с изображениями, ответы на визуальные вопросы и инструк...  
[**modal-serverless-gpu**](</docs/user-guide/skills/optional/mlops/mlops-modal>)|  Бессерверная GPU-облачная платформа для выполнения ML-нагрузок. Используйте, когда нужен доступ к GPU по требованию без управления инфраструктурой, развёртывание ML-моделей в качестве API или выполнение пакетных задач с автоматическим масштабированием.  
[**nemo-curator**](</docs/user-guide/skills/optional/mlops/mlops-nemo-curator>)|  Курирование данных с GPU-ускорением для обучения LLM. Поддерживает текст/изображения/видео/аудио. Включает нечёткую дедупликацию (в 16× быстрее), фильтрацию качества (30+ эвристик), семантическую дедупликацию, редактирование PII, обнаружение NSFW. Масштабируется на несколько GPU с...  
[**peft-fine-tuning**](</docs/user-guide/skills/optional/mlops/mlops-peft>)|  Параметрически эффективная донастройка LLM с использованием LoRA, QLoRA и 25+ методов. Используйте при донастройке больших моделей (7B-70B) с ограниченной памятью GPU, когда нужно обучить <1% параметров с минимальной потерей точности, или для много-адаптерной се...  
[**pinecone**](</docs/user-guide/skills/optional/mlops/mlops-pinecone>)|  Управляемая векторная база данных для производственных AI-приложений. Полностью управляемая, с авто-масштабированием, гибридным поиском (плотный + разреженный), фильтрацией по метаданным и пространствами имён. Низкая задержка (<100 мс p95). Используйте для продакшн RAG, рекомендательных систем или се...  
[**pytorch-fsdp**](</docs/user-guide/skills/optional/mlops/mlops-pytorch-fsdp>)|  Экспертное руководство по Fully Sharded Data Parallel обучению с PyTorch FSDP — шардирование параметров, смешанная точность, выгрузка на CPU, FSDP2  
[**pytorch-lightning**](</docs/user-guide/skills/optional/mlops/mlops-pytorch-lightning>)|  Высокоуровневый PyTorch-фреймворк с классом Trainer, автоматическим распределённым обучением (DDP/FSDP/DeepSpeed), системой callback и минимальным шаблонным кодом. Масштабируется от ноутбука до суперкомпьютера с одним и тем же кодом. Используйте, когда нужны чистые циклы обучения б...  
[**qdrant-vector-search**](</docs/user-guide/skills/optional/mlops/mlops-qdrant>)|  Высокопроизводительный движок векторного поиска по схожести для RAG и семантического поиска. Используйте при создании продакшн RAG-систем, требующих быстрого поиска ближайших соседей, гибридного поиска с фильтрацией или масштабируемого векторного хранилища на базе производительности Rust...  
[**sparse-autoencoder-training**](</docs/user-guide/skills/optional/mlops/mlops-saelens>)|  Предоставляет руководство по обучению и анализу разреженных автоэнкодеров (SAE) с использованием SAELens для разложения активаций нейронных сетей на интерпретируемые признаки. Используйте для обнаружения интерпретируемых признаков, анализа суперпозиции или изучения...  
[**simpo-training**](</docs/user-guide/skills/optional/mlops/mlops-simpo>)|  Simple Preference Optimization для выравнивания LLM. Альтернатива DPO без эталонной модели с лучшей производительностью (+6.4 балла на AlpacaEval 2.0). Эталонная модель не требуется, эффективнее DPO. Используйте для выравнивания по предпочтениям, когда нужна прост...  
[**slime-rl-training**](</docs/user-guide/skills/optional/mlops/mlops-slime>)|  Предоставляет руководство по пост-обучению LLM с RL с использованием slime — фреймворка на базе Megatron+SGLang. Используйте при обучении моделей GLM, реализации собственных рабочих процессов генерации данных или когда требуется тесная интеграция с Megatron-LM для масштабирования RL.  
[**stable-diffusion-image-generation**](</docs/user-guide/skills/optional/mlops/mlops-stable-diffusion>)|  Современная генерация изображений по тексту с помощью моделей Stable Diffusion через HuggingFace Diffusers. Используйте для генерации изображений по текстовым запросам, трансляции изображение-в-изображение, инпейнтинга или создания собственных конвейеров диффузии.  
[**tensorrt-llm**](</docs/user-guide/skills/optional/mlops/mlops-tensorrt-llm>)|  Оптимизация инференса LLM с помощью NVIDIA TensorRT для максимальной пропускной способности и минимальной задержки. Используйте для продакшн-развёртывания на NVIDIA GPU (A100/H100), когда требуется в 10-100 раз более быстрый инференс по сравнению с PyTorch, или для обслуживания моделей с квантизаци...  
[**distributed-llm-pretraining-torchtitan**](</docs/user-guide/skills/optional/mlops/mlops-torchtitan>)|  Предоставляет нативное для PyTorch распределённое предобучение LLM с использованием torchtitan и 4D-параллелизмом (FSDP2, TP, PP, CP). Используйте при предобучении Llama 3.1, DeepSeek V3 или пользовательских моделей в масштабе от 8 до 512+ GPU с Float8, torch.compile и распре...  
[**whisper**](</docs/user-guide/skills/optional/mlops/mlops-whisper>)|  Универсальная модель распознавания речи от OpenAI. Поддерживает 99 языков, транскрипцию, перевод на английский и определение языка. Шесть размеров модели от tiny (39M параметров) до large (1550M параметров). Используйте для распознавания речи, подкас...  
## productivity[​](<#productivity> "Прямая ссылка на productivity")
Навык| Описание  
---|---  
[**canvas**](</docs/user-guide/skills/optional/productivity/productivity-canvas>)|  Интеграция с Canvas LMS — получение записанных курсов и заданий с использованием аутентификации по API-токену.  
[**here.now**](</docs/user-guide/skills/optional/productivity/productivity-here-now>)|  Публикация статических сайтов на {slug}.here.now и хранение приватных файлов в облачных дисках для передачи между агентами.  
[**memento-flashcards**](</docs/user-guide/skills/optional/productivity/productivity-memento-flashcards>)|  Система карточек для запоминания с интервальными повторениями. Создание карточек из фактов или текста, общение с карточками с помощью ответов в свободной форме, оцениваемых агентом, генерация викторин из расшифровок YouTube, повторение карточек по расписанию с адаптивным планированием, экспорт/имп...  
[**shop-app**](</docs/user-guide/skills/optional/productivity/productivity-shop-app>)|  Shop.app: поиск товаров, отслеживание заказов, возвраты, повторный заказ.  
[**shopify**](</docs/user-guide/skills/optional/productivity/productivity-shopify>)|  GraphQL API Shopify Admin и Storefront через curl. Товары, заказы, клиенты, инвентарь, метаполя.  
[**siyuan**](</docs/user-guide/skills/optional/productivity/productivity-siyuan>)|  API SiYuan Note для поиска, чтения, создания и управления блоками и документами в собственной базе знаний через curl.  
[**telephony**](</docs/user-guide/skills/optional/productivity/productivity-telephony>)|  Предоставление Hermes телефонных возможностей без изменений в основных инструментах. Выделение и сохранение номера Twilio, отправка и получение SMS/MMS, совершение прямых звонков и размещение AI-управляемых исходящих звонков через Bland.ai или Vapi.  
## research[​](<#research> "Прямая ссылка на research")
Навык| Описание  
---|---  
[**bioinformatics**](</docs/user-guide/skills/optional/research/research-bioinformatics>)|  Шлюз к 400+ навыкам биоинформатики из bioSkills и ClawBio. Охватывает геномику, транскриптомику, одноклеточный анализ, поиск вариантов, фармакогеномику, метагеномику, структурную биологию и многое другое. Загружает предметные справочные материалы по...  
[**domain-intel**](</docs/user-guide/skills/optional/research/research-domain-intel>)|  Пассивная разведка доменов с использованием стандартной библиотеки Python. Обнаружение поддоменов, проверка SSL-сертификатов, WHOIS-запросы, DNS-записи, проверка доступности доменов и массовый анализ нескольких доменов. API-ключи не требуются.  
[**drug-discovery**](</docs/user-guide/skills/optional/research/research-drug-discovery>)|  Помощник фармацевтических исследований для рабочих процессов открытия лекарств. Поиск биоактивных соединений в ChEMBL, расчёт лекарственно-подобных свойств (Lipinski Ro5, QED, TPSA, синтетическая доступность), поиск лекарственных взаимодействий через OpenFDA, интерпретация ADMET...  
[**duckduckgo-search**](</docs/user-guide/skills/optional/research/research-duckduckgo-search>)|  Бесплатный веб-поиск через DuckDuckGo — текст, новости, изображения, видео. API-ключ не нужен. Предпочитайте CLI `ddgs` при его установке; используйте Python-библиотеку DDGS только после проверки доступности `ddgs` в текущем окружении.  
[**gitnexus-explorer**](</docs/user-guide/skills/optional/research/research-gitnexus-explorer>)|  Индексация кодовой базы с GitNexus и предоставление интерактивного графа знаний через веб-интерфейс + Cloudflare tunnel.  
[**parallel-cli**](</docs/user-guide/skills/optional/research/research-parallel-cli>)|  Опциональный сторонний навык для Parallel CLI — веб-поиск, извлечение, глубокое исследование, обогащение, FindAll и мониторинг на уровне агента. Предпочитайте JSON-вывод и неинтерактивные потоки.  
[**qmd**](</docs/user-guide/skills/optional/research/research-qmd>)|  Поиск в личных базах знаний, заметках, документах и расшифровках встреч локально с помощью qmd — гибридного поискового движка с BM25, векторным поиском и переранжированием LLM. Поддерживает интеграцию с CLI и MCP.  
[**scrapling**](</docs/user-guide/skills/optional/research/research-scrapling>)|  Веб-скрапинг с Scrapling — HTTP-загрузка, скрытая автоматизация браузера, обход Cloudflare и обход сайтов с помощью паука через CLI и Python.  
[**searxng-search**](</docs/user-guide/skills/optional/research/research-searxng-search>)|  Бесплатный мета-поиск через SearXNG — агрегирует результаты из 70+ поисковых систем. Самостоятельное размещение или использование публичного экземпляра. API-ключ не нужен. Автоматически переключается, когда набор инструментов веб-поиска недоступен.  
## security[​](<#security> "Прямая ссылка на security")
Навык| Описание  
---|---  
[**1password**](</docs/user-guide/skills/optional/security/security-1password>)|  Настройка и использование 1Password CLI (op). Используйте при установке CLI, включении интеграции с десктопным приложением, входе в систему, чтении и внедрении секретов для команд.  
[**oss-forensics**](</docs/user-guide/skills/optional/security/security-oss-forensics>)|  Исследование цепочек поставок, восстановление улик и криминалистический анализ для репозиториев GitHub. Охватывает восстановление удалённых коммитов, обнаружение force-push, извлечение IOC, сбор улик из нескольких источников, формирование/проверку гипотез и ст...  
[**sherlock**](</docs/user-guide/skills/optional/security/security-sherlock>)|  Поиск имени пользователя в OSINT по 400+ социальным сетям. Розыск аккаунтов в социальных сетях по имени пользователя.  
## web-development[​](<#web-development> "Прямая ссылка на web-development")
Навык| Описание  
---|---  
[**page-agent**](</docs/user-guide/skills/optional/web-development/web-development-page-agent>)|  Встраивание alibaba/page-agent в ваше веб-приложение — внутристраничный GUI-агент на чистом JavaScript, который поставляется в виде одного тега `<script>` или npm-пакета и позволяет конечным пользователям вашего сайта управлять интерфейсом с помощью естественного языка («нажми войти, заполни имя пользова...  
* * *
## Вклад в опциональные навыки[​](<#contributing-optional-skills> "Прямая ссылка на Вклад в опциональные навыки")
Чтобы добавить новый опциональный навык в репозиторий:
  1. Создайте директорию в `optional-skills/<категория>/<имя-навыка>/`
  2. Добавьте `SKILL.md` со стандартным frontmatter (имя, описание, версия, автор)
  3. Включите любые вспомогательные файлы в поддиректории `references/`, `templates/` или `scripts/`
  4. Отправьте pull request — навык появится в этом каталоге и получит свою собственную страницу документации после слияния


  * [autonomous-ai-agents](<#autonomous-ai-agents>)
  * [blockchain](<#blockchain>)
  * [communication](<#communication>)
  * [creative](<#creative>)
  * [devops](<#devops>)
  * [dogfood](<#dogfood>)
  * [email](<#email>)
  * [health](<#health>)
  * [mcp](<#mcp>)
  * [migration](<#migration>)
  * [mlops](<#mlops>)
  * [productivity](<#productivity>)
  * [research](<#research>)
  * [security](<#security>)
  * [web-development](<#web-development>)
  * [Вклад в опциональные навыки](<#contributing-optional-skills>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog -->
