На этой странице

**Проблема:** Ваша команда открывает PR быстрее, чем вы успеваете их ревьюить. PR неделями ждут проверки. Младшие разработчики сливают баги, потому что никто не успел проверить код. Вы тратите утро на изучение диффов вместо создания нового.

**Решение:** ИИ-агент, который круглосуточно следит за вашими репозиториями, проверяет каждый новый PR на баги, проблемы безопасности и качество кода, и присылает вам сводку — так вы тратите время только на те PR, которые действительно требуют человеческого суждения.

**Что вы создадите:**

[code] 
    ┌───────────────────────────────────────────────────────────────────┐  
    │                                                                   │  
    │   Cron Таймер  ──▶  Hermes Agent  ──▶  GitHub API  ──▶  Доставка  │  
    │   (каждые 2ч)       + gh CLI           (PR diffs)       ревью     │  
    │                    + skill                             (Telegram, │  
    │                    + память                            Discord,   │  
    │                                                        локально)  │  
    │                                                                   │  
    └───────────────────────────────────────────────────────────────────┘  
    
[/code]

Это руководство использует **cron-задачи** для опроса PR по расписанию — без необходимости в сервере или публичном эндпоинте. Работает за NAT и файрволами.

**Хотите ревью в реальном времени?**

Если у вас есть публичный эндпоинт, ознакомьтесь с [Автоматизированные ревью PR на GitHub с вебхуками](/docs/guides/webhook-github-pr-review) — GitHub мгновенно отправляет события Hermes, когда PR открыт или обновлён.

* * *

## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")

- **Hermes Agent установлен** — см. [Руководство по установке](/docs/getting-started/installation)
- **Gateway запущен** для cron-задач:

[code] hermes gateway install   # Установить как службу  
        # или  
        hermes gateway           # Запустить в режиме foreground  
        
[/code]

- **GitHub CLI (`gh`) установлен и аутентифицирован**:

[code] # Установка  
        brew install gh        # macOS  
        sudo apt install gh    # Ubuntu/Debian  
          
        # Аутентификация  
        gh auth login  
        
[/code]

- **Мессенджер настроен** (опционально) — [Telegram](/docs/user-guide/messaging/telegram) или [Discord](/docs/user-guide/messaging/discord)

**Нет мессенджера? Не проблема**

Используйте `deliver: "local"` для сохранения ревью в `~/.hermes/cron/output/`. Отлично подходит для тестирования перед настройкой уведомлений.

* * *

## Шаг 1: Проверка настройки[​](<#step-1-verify-the-setup> "Direct link to Step 1: Verify the Setup")

Убедитесь, что Hermes может получить доступ к GitHub. Запустите чат:

[code] 
    hermes  
    
[/code]

Проверьте простой командой:

[code] 
    Выполни: gh pr list --repo NousResearch/hermes-agent --state open --limit 3  
    
[/code]

Вы должны увидеть список открытых PR. Если это работает, вы готовы.

* * *

## Шаг 2: Попробуйте ручное ревью[​](<#step-2-try-a-manual-review> "Direct link to Step 2: Try a Manual Review")

Всё ещё в чате, попросите Hermes проверить реальный PR:

[code] 
    Сделай ревью этого pull request. Прочитай diff, проверь на баги, проблемы безопасности  
    и качество кода. Будь конкретен, указывай номера строк и цитируй проблемный код.  
      
    Выполни: gh pr diff 3888 --repo NousResearch/hermes-agent  
    
[/code]

Hermes сделает следующее:

1. Выполнит `gh pr diff` для получения изменений кода
2. Прочитает весь diff
3. Сформирует структурированное ревью с конкретными замечаниями

Если вас устраивает качество, пора автоматизировать.

* * *

## Шаг 3: Создайте навык ревью[​](<#step-3-create-a-review-skill> "Direct link to Step 3: Create a Review Skill")

Навык (skill) даёт Hermes последовательные рекомендации по ревью, которые сохраняются между сессиями и запусками cron. Без него качество ревью будет нестабильным.

[code] 
    mkdir -p ~/.hermes/skills/code-review  
    
[/code]

Создайте `~/.hermes/skills/code-review/SKILL.md`:

[code] 
    ---  
    name: code-review  
    description: Проверять pull request на баги, проблемы безопасности и качество кода  
    ---  
      
    # Рекомендации по ревью кода  
      
    При ревью pull request:  
      
    ## Что проверять  
    1. **Баги** — Логические ошибки, off-by-one, обработка null/undefined  
    2. **Безопасность** — Инъекции, обход аутентификации, секреты в коде, SSRF  
    3. **Производительность** — N+1 запросы, бесконечные циклы, утечки памяти  
    4. **Стиль** — Соглашения об именовании, мёртвый код, отсутствие обработки ошибок  
    5. **Тесты** — Проверены ли изменения? Покрывают ли тесты крайние случаи?  
      
    ## Формат вывода  
    Для каждого замечания:  
    - **Файл:Строка** — точное местоположение  
    - **Серьёзность** — Критично / Предупреждение / Предложение  
    - **Что не так** — одно предложение  
    - **Исправление** — как исправить  
      
    ## Правила  
    - Будь конкретен. Цитируй проблемный код.  
    - Не отмечай мелкие придирки к стилю, если они не влияют на читаемость.  
    - Если PR выглядит хорошо, так и скажи. Не выдумывай проблемы.  
    - Завершай одним из: APPROVE / REQUEST_CHANGES / COMMENT  
    
[/code]

Проверьте, что навык загружен — запустите `hermes`, и вы должны увидеть `code-review` в списке навыков при запуске.

* * *

## Шаг 4: Обучите своим соглашениям[​](<#step-4-teach-it-your-conventions> "Direct link to Step 4: Teach It Your Conventions")

Это то, что делает ревью действительно полезным. Запустите сессию и обучите Hermes стандартам вашей команды:

[code] 
    Запомни: В нашем бэкенд-репозитории мы используем Python с FastAPI.  
    Все эндпоинты должны иметь аннотации типов и Pydantic-модели.  
    Мы не разрешаем сырой SQL — только SQLAlchemy ORM.  
    Файлы тестов находятся в tests/ и должны использовать pytest фикстуры.  
    
[/code]

[code] 
    Запомни: В нашем фронтенд-репозитории мы используем TypeScript с React.  
    Тип `any` не допускается. Все компоненты должны иметь интерфейсы пропсов.  
    Мы используем React Query для получения данных, никогда useEffect для API-вызовов.  
    
[/code]

Эти воспоминания сохраняются навсегда — ревьюер будет соблюдать ваши соглашения без необходимости каждый раз напоминать.

* * *

## Шаг 5: Создайте автоматическую cron-задачу[​](<#step-5-create-the-automated-cron-job> "Direct link to Step 5: Create the Automated Cron Job")

Теперь свяжите всё вместе. Создайте cron-задачу, которая запускается каждые 2 часа:

[code] 
    hermes cron create "0 */2 * * *" \  
      "Проверь новые открытые PR и сделай их ревью.  
      
    Репозитории для мониторинга:  
    - myorg/backend-api  
    - myorg/frontend-app  
      
    Шаги:  
    1. Выполни: gh pr list --repo REPO --state open --limit 5 --json number,title,author,createdAt  
    2. Для каждого PR, созданного или обновлённого за последние 4 часа:  
       - Выполни: gh pr diff NUMBER --repo REPO  
       - Сделай ревью diff, используя рекомендации code-review  
    3. Отформатируй вывод как:  
      
    ## PR Reviews — сегодня  
      
    ### [repo] #[number]: [title]  
    **Автор:** [name] | **Вердикт:** APPROVE/REQUEST_CHANGES/COMMENT  
    [замечания]  
      
    Если новых PR нет, скажи: Новых PR для ревью нет." \  
      --name "pr-review" \  
      --deliver telegram \  
      --skill code-review  
    
[/code]

Проверьте, что задача запланирована:

[code] 
    hermes cron list  
    
[/code]

### Другие полезные расписания[​](<#other-useful-schedules> "Direct link to Other useful schedules")

| Расписание | Когда |
|---|---|
| `0 */2 * * *` | Каждые 2 часа |
| `0 9,13,17 * * 1-5` | Три раза в день, только будни |
| `0 9 * * 1` | Еженедельный утренний дайджест по понедельникам |
| `30m` | Каждые 30 минут (для репозиториев с высокой нагрузкой) |

* * *

## Шаг 6: Запуск по требованию[​](<#step-6-run-it-on-demand> "Direct link to Step 6: Run It On Demand")

Не хотите ждать расписания? Запустите вручную:

[code] 
    hermes cron run pr-review  
    
[/code]

Или из сессии чата:

[code] 
    /cron run pr-review  
    
[/code]

* * *

## Дальнейшие возможности[​](<#going-further> "Direct link to Going Further")

### Публикация ревью напрямую в GitHub[​](<#post-reviews-directly-to-github> "Direct link to Post Reviews Directly to GitHub")

Вместо доставки в Telegram, агент может комментировать прямо в PR:

Добавьте это в ваш cron-промпт:

[code] 
    После ревью опубликуй свой отзыв:  
    - Для замечаний: gh pr review NUMBER --repo REPO --comment --body "YOUR_REVIEW"  
    - Для критических проблем: gh pr review NUMBER --repo REPO --request-changes --body "YOUR_REVIEW"  
    - Для чистых PR: gh pr review NUMBER --repo REPO --approve --body "Выглядит хорошо"  
    
[/code]

**Внимание**

Убедитесь, что `gh` имеет токен с областью `repo`. Ревью публикуются от имени пользователя, под которым аутентифицирован `gh`.

### Еженедельная PR-панель[​](<#weekly-pr-dashboard> "Direct link to Weekly PR Dashboard")

Создайте утренний обзор всех ваших репозиториев по понедельникам:

[code] 
    hermes cron create "0 9 * * 1" \  
      "Сгенерируй еженедельную PR-панель:  
    - myorg/backend-api  
    - myorg/frontend-app  
    - myorg/infra  
      
    Для каждого репозитория покажи:  
    1. Количество открытых PR и возраст самого старого PR  
    2. PR, слитые на этой неделе  
    3. Застарёвшие PR (старше 5 дней)  
    4. PR без назначенного ревьюера  
      
    Отформатируй как чистую сводку." \  
      --name "weekly-dashboard" \  
      --deliver telegram  
    
[/code]

### Мониторинг нескольких репозиториев[​](<#multi-repo-monitoring> "Direct link to Multi-Repo Monitoring")

Масштабируйтесь, добавляя больше репозиториев в промпт. Агент обрабатывает их последовательно — никакой дополнительной настройки не требуется.

* * *

## Устранение неполадок[​](<#troubleshooting> "Direct link to Troubleshooting")

### "gh: command not found"[​](<#gh-command-not-found> "Direct link to \"gh: command not found\"")

Gateway запускается в минимальном окружении. Убедитесь, что `gh` находится в системном PATH, и перезапустите gateway.

### Ревью слишком общие[​](<#reviews-are-too-generic> "Direct link to Reviews are too generic")

1. Добавьте навык `code-review` (Шаг 3)
2. Обучите Hermes своим соглашениям через память (Шаг 4)
3. Чем больше контекста о вашем стеке, тем лучше будут ревью

### Cron-задача не запускается[​](<#cron-job-doesnt-run> "Direct link to Cron job doesn't run")

[code] 
    hermes gateway status    # Gateway запущен?  
    hermes cron list         # Задача включена?  
    
[/code]

### Ограничения запросов[​](<#rate-limits> "Direct link to Rate limits")

GitHub позволяет 5 000 API-запросов/час для аутентифицированных пользователей. Каждое ревью PR использует ~3-5 запросов (список + diff + опциональные комментарии). Даже ревью 100 PR/день остаётся в рамках лимита.

* * *

## Что дальше?[​](<#whats-next> "Direct link to What's Next?")

- **[Ревью PR на основе вебхуков](/docs/guides/webhook-github-pr-review)** — получайте мгновенные ревью при открытии PR (требуется публичный эндпоинт)
- **[Бот ежедневного дайджеста](/docs/guides/daily-briefing-bot)** — объедините ревью PR с утренним дайджестом новостей
- **[Создание плагина](/docs/guides/build-a-hermes-plugin)** — упакуйте логику ревью в распространяемый плагин
- **[Профили](/docs/user-guide/profiles)** — запустите выделенный профиль ревьюера с собственной памятью и конфигурацией
- **[Резервные провайдеры](/docs/user-guide/features/fallback-providers)** — обеспечьте выполнение ревью, даже если один провайдер недоступен

- [Предварительные требования](#prerequisites)
- [Шаг 1: Проверка настройки](#step-1-verify-the-setup)
- [Шаг 2: Попробуйте ручное ревью](#step-2-try-a-manual-review)
- [Шаг 3: Создайте навык ревью](#step-3-create-a-review-skill)
- [Шаг 4: Обучите своим соглашениям](#step-4-teach-it-your-conventions)
- [Шаг 5: Создайте автоматическую cron-задачу](#step-5-create-the-automated-cron-job)
  - [Другие полезные расписания](#other-useful-schedules)
- [Шаг 6: Запуск по требованию](#step-6-run-it-on-demand)
- [Дальнейшие возможности](#going-further)
  - [Публикация ревью напрямую в GitHub](#post-reviews-directly-to-github)
  - [Еженедельная PR-панель](#weekly-pr-dashboard)
  - [Мониторинг нескольких репозиториев](#multi-repo-monitoring)
- [Устранение неполадок](#troubleshooting)
  - ["gh: command not found"](#gh-command-not-found)
  - [Ревью слишком общие](#reviews-are-too-generic)
  - [Cron-задача не запускается](#cron-job-doesnt-run)
  - [Ограничения запросов](#rate-limits)
- [Что дальше?](#whats-next)

<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent -->
