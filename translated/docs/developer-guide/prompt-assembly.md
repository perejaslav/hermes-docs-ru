На этой странице

Hermes намеренно разделяет:
  * **кэшированное состояние системного промпта**
  * **эфемерные добавления при вызове API**


Это одно из самых важных проектных решений в проекте, поскольку оно влияет на:
  * использование токенов
  * эффективность кэширования промптов
  * непрерывность сессии
  * корректность памяти


Основные файлы:
  * `run_agent.py`
  * `agent/prompt_builder.py`
  * `tools/memory_tool.py`


## Кэшированные слои системного промпта[​](<#cached-system-prompt-layers> "Direct link to Cached system prompt layers")

Кэшированный системный промпт собирается примерно в таком порядке:
  1. идентичность агента — `SOUL.md` из `HERMES_HOME`, если доступен, иначе используется `DEFAULT_AGENT_IDENTITY` в `prompt_builder.py`
  2. инструкции по поведению с учётом инструментов
  3. статический блок Honcho (когда активен)
  4. опциональное системное сообщение
  5. замороженный снимок MEMORY
  6. замороженный снимок профиля USER
  7. индекс навыков
  8. контекстные файлы (`AGENTS.md`, `.cursorrules`, `.cursor/rules/*.mdc`) — `SOUL.md` **не** включается сюда, если он уже был загружен как идентичность на шаге 1
  9. метка времени / опциональный ID сессии
  10. подсказка платформы


Когда установлен `skip_context_files` (например, при делегировании под-агенту), `SOUL.md` не загружается, и вместо него используется жёстко заданный `DEFAULT_AGENT_IDENTITY`.

### Конкретный пример: собранный системный промпт[​](<#concrete-example-assembled-system-prompt> "Direct link to Concrete example: assembled system prompt")

Вот упрощённое представление того, как выглядит финальный системный промпт, когда присутствуют все слои (комментарии показывают источник каждой секции):

[code]
    # Layer 1: Agent Identity (from ~/.hermes/SOUL.md)
    You are Hermes, an AI assistant created by Nous Research.
    You are an expert software engineer and researcher.
    You value correctness, clarity, and efficiency.
    ...

    # Layer 2: Tool-aware behavior guidance
    You have persistent memory across sessions. Save durable facts using
    the memory tool: user preferences, environment details, tool quirks,
    and stable conventions. Memory is injected into every turn, so keep
    it compact and focused on facts that will still matter later.
    ...
    When the user references something from a past conversation or you
    suspect relevant cross-session context exists, use session_search
    to recall it before asking them to repeat themselves.

    # Tool-use enforcement (for GPT/Codex models only)
    You MUST use your tools to take action — do not describe what you
    would do or plan to do without actually doing it.
    ...

    # Layer 3: Honcho static block (when active)
    [Honcho personality/context data]

    # Layer 4: Optional system message (from config or API)
    [User-configured system message override]

    # Layer 5: Frozen MEMORY snapshot
    ## Persistent Memory
    - User prefers Python 3.12, uses pyproject.toml
    - Default editor is nvim
    - Working on project "atlas" in ~/code/atlas
    - Timezone: US/Pacific

    # Layer 6: Frozen USER profile snapshot
    ## User Profile
    - Name: Alice
    - GitHub: alice-dev

    # Layer 7: Skills index
    ## Skills (mandatory)
    Before replying, scan the skills below. If one clearly matches
    your task, load it with skill_view(name) and follow its instructions.
    ...
    <available_skills>
      software-development:
        - code-review: Structured code review workflow
        - test-driven-development: TDD methodology
      research:
        - arxiv: Search and summarize arXiv papers
    </available_skills>

    # Layer 8: Context files (from project directory)
    # Project Context
    The following project context files have been loaded and should be followed:

    ## AGENTS.md
    This is the atlas project. Use pytest for testing. The main
    entry point is src/atlas/main.py. Always run `make lint` before
    committing.

    # Layer 9: Timestamp + session
    Current time: 2026-03-30T14:30:00-07:00
    Session: abc123

    # Layer 10: Platform hint
    You are a CLI AI Agent. Try not to use markdown but simple text
    renderable inside a terminal.

[/code]

## Как SOUL.md появляется в промпте[​](<#how-soulmd-appears-in-the-prompt> "Direct link to How SOUL.md appears in the prompt")

`SOUL.md` находится по пути `~/.hermes/SOUL.md` и служит идентичностью агента — самой первой секцией системного промпта. Логика загрузки в `prompt_builder.py` работает следующим образом:

[code]
    # From agent/prompt_builder.py (simplified)
    def load_soul_md() -> Optional[str]:
        soul_path = get_hermes_home() / "SOUL.md"
        if not soul_path.exists():
            return None
        content = soul_path.read_text(encoding="utf-8").strip()
        content = _scan_context_content(content, "SOUL.md")  # Security scan
        content = _truncate_content(content, "SOUL.md")       # Cap at 20k chars
        return content

[/code]

Когда `load_soul_md()` возвращает содержимое, оно заменяет жёстко заданный `DEFAULT_AGENT_IDENTITY`. Функция `build_context_files_prompt()` затем вызывается с `skip_soul=True`, чтобы предотвратить появление `SOUL.md` дважды (один раз как идентичность и ещё раз как контекстный файл).

Если `SOUL.md` не существует, система использует запасной вариант:

[code]
    You are Hermes Agent, an intelligent AI assistant created by Nous Research.
    You are helpful, knowledgeable, and direct. You assist users with a wide
    range of tasks including answering questions, writing and editing code,
    analyzing information, creative work, and executing actions via your tools.
    You communicate clearly, admit uncertainty when appropriate, and prioritize
    being genuinely useful over being verbose unless otherwise directed below.
    Be targeted and efficient in your exploration and investigations.

[/code]

## Как внедряются контекстные файлы[​](<#how-context-files-are-injected> "Direct link to How context files are injected")

`build_context_files_prompt()` использует **систему приоритетов** — загружается только один тип проектного контекста (первый подходящий):

[code]
    # From agent/prompt_builder.py (simplified)
    def build_context_files_prompt(cwd=None, skip_soul=False):
        cwd_path = Path(cwd).resolve()

        # Priority: first match wins — only ONE project context loaded
        project_context = (
            _load_hermes_md(cwd_path)       # 1. .hermes.md / HERMES.md (walks to git root)
            or _load_agents_md(cwd_path)    # 2. AGENTS.md (cwd only)
            or _load_claude_md(cwd_path)    # 3. CLAUDE.md (cwd only)
            or _load_cursorrules(cwd_path)  # 4. .cursorrules / .cursor/rules/*.mdc
        )

        sections = []
        if project_context:
            sections.append(project_context)

        # SOUL.md from HERMES_HOME (independent of project context)
        if not skip_soul:
            soul_content = load_soul_md()
            if soul_content:
                sections.append(soul_content)

        if not sections:
            return ""

        return (
            "# Project Context\n\n"
            "The following project context files have been loaded "
            "and should be followed:\n\n"
            + "\n".join(sections)
        )

[/code]

### Детали обнаружения контекстных файлов[​](<#context-file-discovery-details> "Direct link to Context file discovery details")

| Приоритет | Файлы | Область поиска | Примечания |
|---|---|---|---|
| 1 | `.hermes.md`, `HERMES.md` | От CWD до корня git | Собственная конфигурация проекта Hermes |
| 2 | `AGENTS.md` | Только CWD | Общий файл инструкций для агента |
| 3 | `CLAUDE.md` | Только CWD | Совместимость с Claude Code |
| 4 | `.cursorrules`, `.cursor/rules/*.mdc` | Только CWD | Совместимость с Cursor |

Все контекстные файлы:
  * **Проверяются на безопасность** — проверка на паттерны инъекций в промпт (невидимый юникод, «игнорируй предыдущие инструкции», попытки кражи учётных данных)
  * **Усекаются** — ограничены 20 000 символов с соотношением 70/20 head/tail и маркером усечения
  * **Очищаются от YAML frontmatter** — frontmatter `.hermes.md` удаляется (зарезервировано для будущих переопределений конфигурации)


## Слои, добавляемые только при вызове API[​](<#api-call-time-only-layers> "Direct link to API-call-time-only layers")

Эти слои намеренно _не сохраняются_ как часть кэшированного системного промпта:
  * `ephemeral_system_prompt`
  * сообщения prefill
  * оверлеи контекста сессии от шлюза
  * последующий вызов Honcho, внедрённый в сообщение пользователя текущего оборота


Это разделение сохраняет стабильный префикс стабильным для кэширования.

## Снимки памяти[​](<#memory-snapshots> "Direct link to Memory snapshots")

Локальная память и данные профиля пользователя внедряются как замороженные снимки при запуске сессии. Записи в середине сессии обновляют состояние на диске, но не изменяют уже построенный системный промпт до начала новой сессии или принудительной перестройки.

## Контекстные файлы[​](<#context-files> "Direct link to Context files")

`agent/prompt_builder.py` сканирует и очищает контекстные файлы проекта, используя **систему приоритетов** — загружается только один тип (первый подходящий):
  1. `.hermes.md` / `HERMES.md` (поиск до корня git)
  2. `AGENTS.md` (CWD при запуске; поддиректории обнаруживаются постепенно во время сессии через `agent/subdirectory_hints.py`)
  3. `CLAUDE.md` (только CWD)
  4. `.cursorrules` / `.cursor/rules/*.mdc` (только CWD)


`SOUL.md` загружается отдельно через `load_soul_md()` для слоя идентичности. Когда он успешно загружен, `build_context_files_prompt(skip_soul=True)` предотвращает его появление дважды.

Длинные файлы усекаются перед внедрением.

## Индекс навыков[​](<#skills-index> "Direct link to Skills index")

Система навыков добавляет компактный индекс навыков в промпт, когда инструментарий навыков доступен.

## Поддерживаемые поверхности кастомизации промпта[​](<#supported-prompt-customization-surfaces> "Direct link to Supported prompt customization surfaces")

Большинству пользователей следует рассматривать `agent/prompt_builder.py` как внутренний код, а не как поверхность для настройки. Рекомендуемый путь кастомизации — изменять входные данные промпта, которые Hermes уже загружает, а не редактировать Python-шаблоны на месте.

### Используйте эти поверхности в первую очередь[​](<#use-these-surfaces-first> "Direct link to Use these surfaces first")

  * `~/.hermes/SOUL.md` — замените встроенный блок идентичности по умолчанию на свою собственную персону агента и постоянное поведение.
  * `~/.hermes/MEMORY.md` и `~/.hermes/USER.md` — предоставьте долговременные межсессионные факты и данные профиля пользователя, которые должны попадать в снимки новых сессий.
  * Контекстные файлы проекта, такие как `.hermes.md`, `HERMES.md`, `AGENTS.md`, `CLAUDE.md` или `.cursorrules` — добавьте рабочие правила, специфичные для репозитория.
  * Навыки — упакуйте переиспользуемые рабочие процессы и справочные материалы без редактирования основного кода промпта.
  * Опциональная конфигурация системного промпта / переопределения API — добавьте инструкции, специфичные для развёртывания, без форка Hermes.
  * Эфемерные оверлеи, такие как `HERMES_EPHEMERAL_SYSTEM_PROMPT` или сообщения prefill — добавьте руководство в рамках одного оборота, которое не должно становиться частью кэшированного префикса промпта.


### Когда вместо этого редактировать код[​](<#when-to-edit-code-instead> "Direct link to When to edit code instead")

Редактируйте `agent/prompt_builder.py` только если вы намеренно поддерживаете форк или вносите изменения в upstream. Этот файл собирает всю структуру промпта, границы кэша и порядок внедрения для каждой сессии. Прямые правки там — это глобальные изменения продукта, а не кастомизация промпта для конкретного пользователя.

Иными словами:
  * если вам нужна другая идентичность ассистента, редактируйте `SOUL.md`
  * если вам нужны другие правила репозитория, редактируйте контекстные файлы проекта
  * если вам нужны переиспользуемые операционные процедуры, добавьте или измените навыки
  * если вы хотите изменить то, как Hermes собирает промпты для всех, меняйте Python и рассматривайте это как вклад в код


## Почему сборка промпта разделена именно так[​](<#why-prompt-assembly-is-split-this-way> "Direct link to Why prompt assembly is split this way")

Архитектура намеренно оптимизирована для:
  * сохранения кэширования промптов на стороне провайдера
  * избежания ненужных мутаций истории
  * сохранения понятной семантики памяти
  * возможности добавления контекста шлюзом/ACP/CLI без отравления постоянного состояния промпта


## Связанная документация[​](<#related-docs> "Direct link to Related docs")

  * [Сжатие контекста и кэширование промптов](</docs/developer-guide/context-compression-and-caching>)
  * [Хранилище сессий](</docs/developer-guide/session-storage>)
  * [Внутреннее устройство шлюза](</docs/developer-guide/gateway-internals>)


  * [Кэшированные слои системного промпта](<#cached-system-prompt-layers>)
    * [Конкретный пример: собранный системный промпт](<#concrete-example-assembled-system-prompt>)
  * [Как SOUL.md появляется в промпте](<#how-soulmd-appears-in-the-prompt>)
  * [Как внедряются контекстные файлы](<#how-context-files-are-injected>)
    * [Детали обнаружения контекстных файлов](<#context-file-discovery-details>)
  * [Слои, добавляемые только при вызове API](<#api-call-time-only-layers>)
  * [Снимки памяти](<#memory-snapshots>)
  * [Контекстные файлы](<#context-files>)
  * [Индекс навыков](<#skills-index>)
  * [Поддерживаемые поверхности кастомизации промпта](<#supported-prompt-customization-surfaces>)
    * [Используйте эти поверхности в первую очередь](<#use-these-surfaces-first>)
    * [Когда вместо этого редактировать код](<#when-to-edit-code-instead>)
  * [Почему сборка промпта разделена именно так](<#why-prompt-assembly-is-split-this-way>)
  * [Связанная документация](<#related-docs>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly -->
