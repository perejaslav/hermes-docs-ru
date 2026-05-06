На этой странице

## Проблема[​](<#the-problem> "Direct link to The Problem")

Облачные LLM API взимают плату за каждый токен. Интенсивная сессия кодинга может стоить $5–20. Для личных проектов, обучения или работы с чувствительными данными это накапливается — к тому же каждый диалог отправляется третьей стороне.

## Что решает это руководство[​](<#what-this-guide-solves> "Direct link to What This Guide Solves")

Вы настроите Hermes Agent, работающий полностью на вашем собственном оборудовании, используя [Ollama](<https://ollama.com>) в качестве бэкенда для модели. Никаких API-ключей, никаких подписок, никакие данные не покидают вашу машину. После настройки Hermes работает точно так же, как с OpenRouter или Anthropic — команды терминала, редактирование файлов, веб-сёрфинг, делегирование — но модель выполняется локально.

По итогу вы получите:
  * Ollama, обслуживающая одну или несколько моделей с открытым весом
  * Hermes, подключённый к Ollama как пользовательская конечная точка
  * Работающий локальный агент, который может редактировать файлы, выполнять команды и просматривать веб-страницы
  * Опционально: Telegram/Discord бот, работающий полностью на вашем оборудовании


## Что вам понадобится[​](<#what-you-need> "Direct link to What You Need")

| Компонент | Минимум | Рекомендуется |
|---|---|---|
| **ОЗУ** | 8 ГБ (для моделей 3B) | 32+ ГБ (для моделей 27B+) |
| **Хранилище** | 5 ГБ свободно | 30+ ГБ (для нескольких моделей) |
| **CPU** | 4 ядра | 8+ ядер (AMD EPYC, Ryzen, Intel Xeon) |
| **GPU** | Не обязателен | NVIDIA GPU с 8+ ГБ VRAM значительно ускоряет работу |

Работа только на CPU возможна, но ожидайте медленных ответов.

Ollama работает на серверах только с CPU. Модель 9B на современном 8-ядерном CPU выдаёт ~10 токенов/сек. Модель 31B на CPU медленнее (~2–5 токенов/сек) — каждый ответ занимает 30–120 секунд, но это работает. GPU значительно улучшает ситуацию. Для конфигураций только с CPU увеличьте таймаут API в конфиге:

[code]
    agent:
      api_timeout: 1800   # 30 минут — щедро для медленных локальных моделей

[/code]

## Шаг 1: Установка Ollama[​](<#step-1-install-ollama> "Direct link to Step 1: Install Ollama")

[code]
    curl -fsSL https://ollama.com/install.sh | sh

[/code]

Проверьте, что она запущена:

[code]
    ollama --version
    curl http://localhost:11434/api/tags   # Должен вернуть {"models":[]}

[/code]

## Шаг 2: Загрузка модели[​](<#step-2-pull-a-model> "Direct link to Step 2: Pull a Model")

Выберите на основе вашего оборудования:

| Модель | Размер на диске | Требуется ОЗУ | Вызов инструментов | Лучше всего для |
|---|---|---|---|---|
| `gemma4:31b` | ~20 ГБ | 24+ ГБ | Да | Лучшее качество — сильное использование инструментов и рассуждение |
| `gemma2:27b` | ~16 ГБ | 20+ ГБ | Нет | Разговорные задачи, без вызова инструментов |
| `gemma2:9b` | ~5 ГБ | 8+ ГБ | Нет | Быстрый чат, вопросы и ответы — не может вызывать инструменты |
| `llama3.2:3b` | ~2 ГБ | 4+ ГБ | Нет | Только лёгкие быстрые ответы |

Вызов инструментов важен

Hermes — это **агентный** ассистент — он редактирует файлы, выполняет команды и просматривает веб-страницы через вызовы инструментов. Модели без поддержки вызова инструментов могут только общаться; они не могут совершать действия. Для полного опыта Hermes используйте модель, поддерживающую инструменты (например, `gemma4:31b`).

Загрузите выбранную модель:

[code]
    ollama pull gemma4:31b

[/code]

Несколько моделей

Вы можете загрузить несколько моделей и переключаться между ними внутри Hermes с помощью `/model`. Ollama загружает активную модель в память по требованию и автоматически выгружает неактивные.

Проверьте, что модель работает:

[code]
    curl http://localhost:11434/v1/chat/completions \
      -H "Content-Type: application/json" \
      -d '{
        "model": "gemma4:31b",
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 50
      }'

[/code]

Вы должны увидеть JSON-ответ с ответом модели.

## Шаг 3: Настройка Hermes[​](<#step-3-configure-hermes> "Direct link to Step 3: Configure Hermes")

Запустите мастер настройки Hermes:

[code]
    hermes setup

[/code]

Когда будет предложено выбрать провайдера, выберите **Custom Endpoint** и введите:
  * **Base URL:** `http://localhost:11434/v1`
  * **API Key:** Оставьте пустым или введите `no-key` (Ollama не требует ключа)
  * **Model:** `gemma4:31b` (или ту модель, которую вы загрузили)


В качестве альтернативы, отредактируйте `~/.hermes/config.yaml` напрямую:

[code]
    model:
      default: "gemma4:31b"
      provider: "custom"
      base_url: "http://localhost:11434/v1"

[/code]

## Шаг 4: Начало работы с Hermes[​](<#step-4-start-using-hermes> "Direct link to Step 4: Start Using Hermes")

[code]
    hermes

[/code]

Вот и всё. Теперь вы запускаете полностью локального агента. Попробуйте:

[code]
    You: List all Python files in this directory and count the lines of code in each

    You: Read the README.md and summarize what this project does

    You: Create a Python script that fetches the weather for Ho Chi Minh City

[/code]

Hermes будет использовать инструмент терминала, файловые операции и вашу локальную модель — никаких облачных вызовов.

## Шаг 5: Выбор подходящей модели для задачи[​](<#step-5-pick-the-right-model-for-your-task> "Direct link to Step 5: Pick the Right Model for Your Task")

Не каждая задача требует самую большую модель. Вот практическое руководство:

| Задача | Рекомендуемая модель | Почему |
|---|---|---|
| Редактирование файлов, код, команды терминала | `gemma4:31b` | Единственная модель с надёжным вызовом инструментов |
| Быстрые вопросы и ответы (без инструментов) | `gemma2:9b` | Быстрые ответы для разговорных задач |
| Лёгкий чат | `llama3.2:3b` | Самая быстрая, но с очень ограниченными возможностями |

Примечание

Для полноценной агентной работы (редактирование файлов, выполнение команд, просмотр веб-страниц) `gemma4:31b` в настоящее время — лучший локальный вариант с поддержкой вызова инструментов. Проверяйте [библиотеку моделей Ollama](<https://ollama.com/library>) на предмет более новых моделей — поддержка вызова инструментов быстро расширяется.

Переключайте модели на лету внутри сессии:

[code]
    /model gemma2:9b

[/code]

## Шаг 6: Оптимизация скорости[​](<#step-6-optimize-for-speed> "Direct link to Step 6: Optimize for Speed")

### Увеличение контекстного окна Ollama[​](<#increase-ollamas-context-window> "Direct link to Increase Ollama's Context Window")

По умолчанию Ollama использует контекст из 2048 токенов. Для агентной работы (вызовы инструментов, длинные диалоги) вам нужно больше:

[code]
    # Create a Modelfile that extends context
    cat > /tmp/Modelfile << 'EOF'
    FROM gemma4:31b
    PARAMETER num_ctx 16384
    EOF

    ollama create gemma4-16k -f /tmp/Modelfile

[/code]

Затем обновите конфиг Hermes, указав `gemma4-16k` в качестве имени модели.

### Держите модель загруженной[​](<#keep-the-model-loaded> "Direct link to Keep the Model Loaded")

По умолчанию Ollama выгружает модели после 5 минут бездействия. Для постоянного бота через шлюз держите её загруженной:

[code]
    # Set keep-alive to 24 hours
    curl http://localhost:11434/api/generate \
      -d '{"model": "gemma4:31b", "keep_alive": "24h"}'

[/code]

Или установите глобально в окружении Ollama:

[code]
    # /etc/systemd/system/ollama.service.d/override.conf
    [Service]
    Environment="OLLAMA_KEEP_ALIVE=24h"

[/code]

### Использование GPU (если доступно)[​](<#use-gpu-offloading-if-available> "Direct link to Use GPU Offloading (If Available)")

Если у вас есть NVIDIA GPU, Ollama автоматически выгружает слои на неё. Проверьте с помощью:

[code]
    ollama ps   # Показывает, какая модель загружена и сколько слоёв на GPU

[/code]

Для модели 31B на GPU с 12 ГБ вы получите частичную выгрузку (~40 слоёв на GPU, остальное на CPU), что всё равно даёт значительное ускорение.

## Шаг 7: Запуск в качестве бота через шлюз (опционально)[​](<#step-7-run-as-a-gateway-bot-optional> "Direct link to Step 7: Run as a Gateway Bot (Optional)")

Как только Hermes заработает локально в CLI, вы можете выставить его как Telegram или Discord бота — всё ещё работающего полностью на вашем оборудовании.

### Telegram[​](<#telegram> "Direct link to Telegram")

  1. Создайте бота через [@BotFather](<https://t.me/BotFather>) и получите токен
  2. Добавьте в ваш `~/.hermes/config.yaml`:


[code]
    model:
      default: "gemma4:31b"
      provider: "custom"
      base_url: "http://localhost:11434/v1"

    platforms:
      telegram:
        enabled: true
        token: "YOUR_TELEGRAM_BOT_TOKEN"

[/code]

  3. Запустите шлюз:


[code]
    hermes gateway

[/code]

Теперь напишите вашему боту в Telegram — он отвечает, используя вашу локальную модель.

### Discord[​](<#discord> "Direct link to Discord")

  1. Создайте Discord-приложение на [discord.com/developers](<https://discord.com/developers/applications>)
  2. Добавьте в конфиг:


[code]
    platforms:
      discord:
        enabled: true
        token: "YOUR_DISCORD_BOT_TOKEN"

[/code]

  3. Запустите: `hermes gateway`


## Шаг 8: Настройка запасных вариантов (опционально)[​](<#step-8-set-up-fallbacks-optional> "Direct link to Step 8: Set Up Fallbacks (Optional)")

Локальные модели могут испытывать трудности со сложными задачами. Настройте облачный запасной вариант, который активируется только когда локальная модель не справляется:

[code]
    model:
      default: "gemma4:31b"
      provider: "custom"
      base_url: "http://localhost:11434/v1"

    fallback_providers:
      - provider: openrouter
        model: anthropic/claude-sonnet-4

[/code]

Таким образом, 90% использования будет бесплатным (локальным), и только сложные задачи будут обращаться к платному API.

## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")

### «Connection refused» при запуске[​](<#connection-refused-on-startup> "Direct link to \"Connection refused\" on startup")

Ollama не запущена. Запустите её:

[code]
    sudo systemctl start ollama
    # или
    ollama serve

[/code]

### Медленные ответы[​](<#slow-responses> "Direct link to Slow responses")

  * **Проверьте размер модели vs ОЗУ:** Если вашей модели нужно больше ОЗУ, чем доступно, происходит подкачка на диск. Используйте модель поменьше или добавьте ОЗУ.
  * **Проверьте `ollama ps`:** Если слои GPU не выгружаются, ответы ограничены CPU. Это нормально для серверов только с CPU.
  * **Уменьшите контекст:** Большие диалоги замедляют инференс. Регулярно используйте `/compress` или установите более низкий порог сжатия в конфиге.


### Модель не следует вызовам инструментов[​](<#model-doesnt-follow-tool-calls> "Direct link to Model doesn't follow tool calls")

Меньшие модели (3B, 7B) иногда игнорируют инструкции по вызову инструментов и выдают обычный текст вместо структурированных вызовов функций. Решения:
  * **Используйте модель побольше** — `gemma4:31b` или `gemma2:27b` обрабатывают вызовы инструментов значительно лучше, чем модели 3B/7B.
  * **У Hermes есть автовосстановление** — он обнаруживает некорректные вызовы инструментов и пытается исправить их автоматически.
  * **Настройте запасной вариант** — если локальная модель не справляется 3 раза, Hermes переключается на облачного провайдера.


### Ошибки контекстного окна[​](<#context-window-errors> "Direct link to Context window errors")

Контекст Ollama по умолчанию (2048 токенов) слишком мал для агентной работы. Смотрите [Шаг 6](<#step-6-optimize-for-speed>), чтобы увеличить его.

## Сравнение стоимости[​](<#cost-comparison> "Direct link to Cost Comparison")

Вот что даёт локальный запуск по сравнению с облачными API, на основе типичной сессии кодинга (~100K токенов на вход, ~20K токенов на выход):

| Провайдер | Стоимость за сессию | В месяц (ежедневное использование) |
|---|---|---|
| Anthropic Claude Sonnet | ~$0.80 | ~$24 |
| OpenRouter (GPT-4o) | ~$0.60 | ~$18 |
| **Ollama (локально)** | **$0.00** | **$0.00** |

Единственные затраты — электричество, примерно $0.01–0.05 за сессию в зависимости от оборудования.

## Что хорошо работает локально[​](<#what-works-well-locally> "Direct link to What Works Well Locally")

  * **Редактирование файлов и генерация кода** — модели 9B+ справляются хорошо
  * **Команды терминала** — Hermes оборачивает команду, выполняет её, читает вывод независимо от модели
  * **Веб-сёрфинг** — инструмент браузера выполняет загрузку; модель просто интерпретирует результаты
  * **Cron-задачи и запланированные задания** — работают так же, как в облачных конфигурациях
  * **Мультиплатформенный шлюз** — Telegram, Discord, Slack — всё работает с локальными моделями


## Что лучше с облачными моделями[​](<#whats-better-with-cloud-models> "Direct link to What's Better with Cloud Models")

  * **Очень сложные многошаговые рассуждения** — модели 70B+ или облачные модели, такие как Claude Opus, заметно лучше
  * **Длинные контекстные окна** — облачные модели предлагают 100K–1M токенов; локальные модели обычно 8K–32K
  * **Скорость при больших ответах** — облачный инференс быстрее, чем локальный только на CPU, для длинных генераций


Золотая середина: используйте локальные модели для повседневных задач, настройте облачный запасной вариант для сложных.

  * [Проблема](<#the-problem>)
  * [Что решает это руководство](<#what-this-guide-solves>)
  * [Что вам понадобится](<#what-you-need>)
  * [Шаг 1: Установка Ollama](<#step-1-install-ollama>)
  * [Шаг 2: Загрузка модели](<#step-2-pull-a-model>)
  * [Шаг 3: Настройка Hermes](<#step-3-configure-hermes>)
  * [Шаг 4: Начало работы с Hermes](<#step-4-start-using-hermes>)
  * [Шаг 5: Выбор подходящей модели для задачи](<#step-5-pick-the-right-model-for-your-task>)
  * [Шаг 6: Оптимизация скорости](<#step-6-optimize-for-speed>)
    * [Увеличение контекстного окна Ollama](<#increase-ollamas-context-window>)
    * [Держите модель загруженной](<#keep-the-model-loaded>)
    * [Использование GPU (если доступно)](<#use-gpu-offloading-if-available>)
  * [Шаг 7: Запуск в качестве бота через шлюз (опционально)](<#step-7-run-as-a-gateway-bot-optional>)
    * [Telegram](<#telegram>)
    * [Discord](<#discord>)
  * [Шаг 8: Настройка запасных вариантов (опционально)](<#step-8-set-up-fallbacks-optional>)
  * [Устранение неполадок](<#troubleshooting>)
    * [«Connection refused» при запуске](<#connection-refused-on-startup>)
    * [Медленные ответы](<#slow-responses>)
    * [Модель не следует вызовам инструментов](<#model-doesnt-follow-tool-calls>)
    * [Ошибки контекстного окна](<#context-window-errors>)
  * [Сравнение стоимости](<#cost-comparison>)
  * [Что хорошо работает локально](<#what-works-well-locally>)
  * [Что лучше с облачными моделями](<#whats-better-with-cloud-models>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup -->
