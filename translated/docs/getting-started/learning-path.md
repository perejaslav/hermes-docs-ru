On this page

Hermes Agent может многое — CLI-ассистент, Telegram/Discord бот, автоматизация задач, RL-обучение и многое другое. Эта страница поможет вам понять, с чего начать и что читать, исходя из вашего уровня опыта и поставленных целей.

## Начало работы

Если вы ещё не установили Hermes Agent, начните с [руководства по установке](</docs/getting-started/installation>), а затем пройдите [Быстрый старт](</docs/getting-started/quickstart>). Всё, что ниже, предполагает, что у вас есть работающая установка.

## Как использовать эту страницу[​](<#how-to-use-this-page> "Прямая ссылка на «Как использовать эту страницу»")

  * **Знаете свой уровень?** Перейдите к [таблице по уровню опыта](<#by-experience-level>) и следуйте порядку чтения для вашего уровня.
  * **У вас есть конкретная цель?** Перейдите к разделу [По сценариям использования](<#by-use-case>) и найдите подходящий сценарий.
  * **Просто просматриваете?** Ознакомьтесь с таблицей [Ключевые возможности](<#key-features-at-a-glance>) для быстрого обзора всего, что умеет Hermes Agent.

## По уровню опыта[​](<#by-experience-level> "Прямая ссылка на «По уровню опыта»")

| Уровень | Цель | Рекомендуемое чтение | Примерное время |
|---|---|---|---|
| **Начинающий** | Запустить, начать базовые диалоги, использовать встроенные инструменты | [Установка](</docs/getting-started/installation>) → [Быстрый старт](</docs/getting-started/quickstart>) → [Использование CLI](</docs/user-guide/cli>) → [Конфигурация](</docs/user-guide/configuration>) | ~1 час |
| **Средний** | Настроить мессенджер-ботов, использовать продвинутые функции: память, cron-задачи и навыки | [Сессии](</docs/user-guide/sessions>) → [Мессенджеры](</docs/user-guide/messaging>) → [Инструменты](</docs/user-guide/features/tools>) → [Навыки](</docs/user-guide/features/skills>) → [Память](</docs/user-guide/features/memory>) → [Cron](</docs/user-guide/features/cron>) | ~2–3 часа |
| **Продвинутый** | Создавать собственные инструменты, навыки, обучать модели с RL, вносить вклад в проект | [Архитектура](</docs/developer-guide/architecture>) → [Добавление инструментов](</docs/developer-guide/adding-tools>) → [Создание навыков](</docs/developer-guide/creating-skills>) → [RL-обучение](</docs/user-guide/features/rl-training>) → [Участие в разработке](</docs/developer-guide/contributing>) | ~4–6 часов |

## По сценариям использования[​](<#by-use-case> "Прямая ссылка на «По сценариям использования»")

Выберите сценарий, который соответствует вашим задачам. Каждый сценарий содержит ссылки на соответствующую документацию в порядке чтения.

### «Мне нужен CLI-ассистент для программирования»[​](<#i-want-a-cli-coding-assistant> "Прямая ссылка на «Мне нужен CLI-ассистент для программирования»")

Используйте Hermes Agent как интерактивного терминального ассистента для написания, ревью и запуска кода.

  1. [Установка](</docs/getting-started/installation>)
  2. [Быстрый старт](</docs/getting-started/quickstart>)
  3. [Использование CLI](</docs/user-guide/cli>)
  4. [Выполнение кода](</docs/user-guide/features/code-execution>)
  5. [Контекстные файлы](</docs/user-guide/features/context-files>)
  6. [Советы и рекомендации](</docs/guides/tips>)

> **tip**
> Передавайте файлы напрямую в диалог через контекстные файлы. Hermes Agent может читать, редактировать и запускать код в ваших проектах.

### «Мне нужен Telegram/Discord бот»[​](<#i-want-a-telegramdiscord-bot> "Прямая ссылка на «Мне нужен Telegram/Discord бот»")

Разверните Hermes Agent как бота на вашей любимой платформе обмена сообщениями.

  1. [Установка](</docs/getting-started/installation>)
  2. [Конфигурация](</docs/user-guide/configuration>)
  3. [Обзор мессенджеров](</docs/user-guide/messaging>)
  4. [Настройка Telegram](</docs/user-guide/messaging/telegram>)
  5. [Настройка Discord](</docs/user-guide/messaging/discord>)
  6. [Голосовой режим](</docs/user-guide/features/voice-mode>)
  7. [Использование голосового режима с Hermes](</docs/guides/use-voice-mode-with-hermes>)
  8. [Безопасность](</docs/user-guide/security>)

Полные примеры проектов:
  * [Бот с ежедневной сводкой](</docs/guides/daily-briefing-bot>)
  * [Командный Telegram-ассистент](</docs/guides/team-telegram-assistant>)

### «Я хочу автоматизировать задачи»[​](<#i-want-to-automate-tasks> "Прямая ссылка на «Я хочу автоматизировать задачи»")

Планируйте повторяющиеся задачи, запускайте пакетные задания или объединяйте действия агента в цепочки.

  1. [Быстрый старт](</docs/getting-started/quickstart>)
  2. [Планирование через Cron](</docs/user-guide/features/cron>)
  3. [Пакетная обработка](</docs/user-guide/features/batch-processing>)
  4. [Делегирование](</docs/user-guide/features/delegation>)
  5. [Хуки](</docs/user-guide/features/hooks>)

> **tip**
> Cron-задачи позволяют Hermes Agent выполнять задания по расписанию — ежедневные сводки, периодические проверки, автоматические отчёты — без вашего участия.

### «Я хочу создавать собственные инструменты и навыки»[​](<#i-want-to-build-custom-toolsskills> "Прямая ссылка на «Я хочу создавать собственные инструменты и навыки»")

Расширяйте Hermes Agent с помощью собственных инструментов и переиспользуемых пакетов навыков.

  1. [Плагины](</docs/user-guide/features/plugins>)
  2. [Создание плагина Hermes](</docs/guides/build-a-hermes-plugin>)
  3. [Обзор инструментов](</docs/user-guide/features/tools>)
  4. [Обзор навыков](</docs/user-guide/features/skills>)
  5. [MCP (Model Context Protocol)](</docs/user-guide/features/mcp>)
  6. [Архитектура](</docs/developer-guide/architecture>)
  7. [Добавление инструментов](</docs/developer-guide/adding-tools>)
  8. [Создание навыков](</docs/developer-guide/creating-skills>)

> **tip**
> Для создания собственных инструментов начните с плагинов. Страница [Добавление инструментов](</docs/developer-guide/adding-tools>) предназначена для разработки встроенных инструментов ядра Hermes, а не для обычного пользовательского пути создания инструментов.

### «Я хочу обучать модели»[​](<#i-want-to-train-models> "Прямая ссылка на «Я хочу обучать модели»")

Используйте обучение с подкреплением для тонкой настройки поведения моделей с помощью встроенного пайплайна RL-обучения Hermes Agent.

  1. [Быстрый старт](</docs/getting-started/quickstart>)
  2. [Конфигурация](</docs/user-guide/configuration>)
  3. [RL-обучение](</docs/user-guide/features/rl-training>)
  4. [Маршрутизация провайдеров](</docs/user-guide/features/provider-routing>)
  5. [Архитектура](</docs/developer-guide/architecture>)

> **tip**
> RL-обучение работает лучше всего, когда вы уже понимаете основы работы Hermes Agent с диалогами и вызовами инструментов. Если вы новичок, сначала пройдите путь начинающего.

### «Я хочу использовать Hermes как Python-библиотеку»[​](<#i-want-to-use-it-as-a-python-library> "Прямая ссылка на «Я хочу использовать Hermes как Python-библиотеку»")

Интегрируйте Hermes Agent в свои Python-приложения программно.

  1. [Установка](</docs/getting-started/installation>)
  2. [Быстрый старт](</docs/getting-started/quickstart>)
  3. [Руководство по Python-библиотеке](</docs/guides/python-library>)
  4. [Архитектура](</docs/developer-guide/architecture>)
  5. [Инструменты](</docs/user-guide/features/tools>)
  6. [Сессии](</docs/user-guide/sessions>)

## Ключевые возможности[​](<#key-features-at-a-glance> "Прямая ссылка на «Ключевые возможности»")

Не уверены, что доступно? Вот краткий перечень основных возможностей:

| Возможность | Описание | Ссылка |
|---|---|---|
| **Инструменты** | Встроенные инструменты, которые может вызывать агент (файловый ввод/вывод, поиск, оболочка и др.) | [Инструменты](</docs/user-guide/features/tools>) |
| **Навыки** | Устанавливаемые пакеты плагинов, добавляющие новые возможности | [Навыки](</docs/user-guide/features/skills>) |
| **Память** | Постоянная память между сессиями | [Память](</docs/user-guide/features/memory>) |
| **Контекстные файлы** | Передача файлов и директорий в диалоги | [Контекстные файлы](</docs/user-guide/features/context-files>) |
| **MCP** | Подключение к внешним серверам инструментов через Model Context Protocol | [MCP](</docs/user-guide/features/mcp>) |
| **Cron** | Планирование повторяющихся задач агента | [Cron](</docs/user-guide/features/cron>) |
| **Делегирование** | Запуск под-агентов для параллельной работы | [Делегирование](</docs/user-guide/features/delegation>) |
| **Выполнение кода** | Запуск Python-скриптов, программно вызывающих инструменты Hermes | [Выполнение кода](</docs/user-guide/features/code-execution>) |
| **Браузер** | Веб-сёрфинг и скрапинг | [Браузер](</docs/user-guide/features/browser>) |
| **Хуки** | Событийно-ориентированные колбэки и промежуточное ПО | [Хуки](</docs/user-guide/features/hooks>) |
| **Пакетная обработка** | Обработка множества входных данных пакетно | [Пакетная обработка](</docs/user-guide/features/batch-processing>) |
| **RL-обучение** | Тонкая настройка моделей с помощью обучения с подкреплением | [RL-обучение](</docs/user-guide/features/rl-training>) |
| **Маршрутизация провайдеров** | Маршрутизация запросов между несколькими LLM-провайдерами | [Маршрутизация провайдеров](</docs/user-guide/features/provider-routing>) |

## Что читать дальше[​](<#what-to-read-next> "Прямая ссылка на «Что читать дальше»")

Исходя из того, где вы сейчас находитесь:

  * **Только что завершили установку?** → Переходите к [Быстрому старту](</docs/getting-started/quickstart>), чтобы провести первый диалог.
  * **Прошли Быстрый старт?** → Прочитайте [Использование CLI](</docs/user-guide/cli>) и [Конфигурацию](</docs/user-guide/configuration>), чтобы настроить среду под себя.
  * **Уверенно владеете основами?** → Изучите [Инструменты](</docs/user-guide/features/tools>), [Навыки](</docs/user-guide/features/skills>) и [Память](</docs/user-guide/features/memory>), чтобы раскрыть полную мощь агента.
  * **Настраиваете для команды?** → Прочитайте [Безопасность](</docs/user-guide/security>) и [Сессии](</docs/user-guide/sessions>), чтобы разобраться с контролем доступа и управлением диалогами.
  * **Готовы к разработке?** → Переходите к [Руководству разработчика](</docs/developer-guide/architecture>), чтобы понять внутреннее устройство и начать вносить вклад.
  * **Хотите практических примеров?** → Ознакомьтесь с разделом [Руководства](</docs/guides/tips>) с реальными проектами и советами.

> **tip**
> Вам не нужно читать всё. Выберите путь, соответствующий вашей цели, следуйте ссылкам по порядку — и вы быстро станете продуктивны. В любой момент можно вернуться на эту страницу, чтобы найти следующий шаг.

  * [Как использовать эту страницу](<#how-to-use-this-page>)
  * [По уровню опыта](<#by-experience-level>)
  * [По сценариям использования](<#by-use-case>)
    * [«Мне нужен CLI-ассистент для программирования»](<#i-want-a-cli-coding-assistant>)
    * [«Мне нужен Telegram/Discord бот»](<#i-want-a-telegramdiscord-bot>)
    * [«Я хочу автоматизировать задачи»](<#i-want-to-automate-tasks>)
    * [«Я хочу создавать собственные инструменты и навыки»](<#i-want-to-build-custom-toolsskills>)
    * [«Я хочу обучать модели»](<#i-want-to-train-models>)
    * [«Я хочу использовать Hermes как Python-библиотеку»](<#i-want-to-use-it-as-a-python-library>)
  * [Ключевые возможности](<#key-features-at-a-glance>)
  * [Что читать дальше](<#what-to-read-next>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/getting-started/learning-path -->
