На этой странице

Подводные камни, примеры и граничные случаи для Kanban-воркеров Hermes. Сам жизненный цикл автоматически внедряется в системный промпт каждого воркера как KANBAN_GUIDANCE (из agent/prompt_builder.py); этот навык загружается, когда нужно больше деталей по конкретным сценариям.

## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")

|   |
|---|---|
Источник| Встроенный (установлен по умолчанию)  
Путь| `skills/devops/kanban-worker`  
Версия| `2.0.0`  
Теги| `kanban`, `multi-agent`, `collaboration`, `workflow`, `pitfalls`  
Связанные навыки| [`kanban-orchestrator`](</docs/user-guide/skills/bundled/devops/devops-kanban-orchestrator>)  

## Справка: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит как инструкции, когда навык активен.

# Kanban Worker — Подводные камни и примеры

> Вы видите этот навык, потому что диспетчер Kanban Hermes породил вас как воркера с `--skills kanban-worker` — он загружается автоматически для каждого отправленного воркера. **Жизненный цикл** (6 шагов: orient → work → heartbeat → block/complete) также находится в блоке `KANBAN_GUIDANCE`, который автоматически внедряется в ваш системный промпт. Этот навык — более глубокая детализация: правильные формы передачи данных, диагностика повторных попыток, граничные случаи.

## Обработка рабочего пространства[​](<#workspace-handling> "Direct link to Workspace handling")

Тип вашего рабочего пространства определяет, как вы должны вести себя внутри `$HERMES_KANBAN_WORKSPACE`:

Тип| Что это| Как работать  
---|---|---  
`scratch`| Свежая временная директория, только ваша| Читайте и пишите freely; она будет удалена сборщиком мусора при архивации задачи.  
`dir:<path>`| Общая постоянная директория| Другие запуски будут читать то, что вы напишете. Относитесь к ней как к долгоживущему состоянию. Путь гарантированно абсолютный (ядро отклоняет относительные пути).  
`worktree`| Git worktree по указанному пути| Если `.git` не существует, сначала выполните `git worktree add <path> <branch>` из основного репозитория, затем перейдите в директорию и работайте как обычно. Коммитьте работу сюда.  

## Изоляция тенантов[​](<#tenant-isolation> "Direct link to Tenant isolation")

Если установлена переменная `$HERMES_TENANT`, задача принадлежит пространству имён тенанта. При чтении или записи постоянной памяти добавляйте префикс тенанта к записям, чтобы контекст не просачивался между тенантами:
  * Хорошо: `business-a: Acme is our biggest customer`
  * Плохо (утечка): `Acme is our biggest customer`



## Хорошие формы сводок и метаданных[​](<#good-summary--metadata-shapes> "Direct link to Good summary + metadata shapes")

Передача `kanban_complete(summary=..., metadata=...)` — это то, как нижестоящие воркеры читают то, что вы сделали. Паттерны, которые работают:

**Задача по кодингу:**

[code] 
    kanban_complete(  
        summary="shipped rate limiter — token bucket, keys on user_id with IP fallback, 14 tests pass",  
        metadata={  
            "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],  
            "tests_run": 14,  
            "tests_passed": 14,  
            "decisions": ["user_id primary, IP fallback for unauthenticated requests"],  
        },  
    )  
    
[/code]

**Исследовательская задача:**

[code] 
    kanban_complete(  
        summary="3 competing libraries reviewed; vLLM wins on throughput, SGLang on latency, Tensorrt-LLM on memory efficiency",  
        metadata={  
            "sources_read": 12,  
            "recommendation": "vLLM",  
            "benchmarks": {"vllm": 1.0, "sglang": 0.87, "trtllm": 0.72},  
        },  
    )  
    
[/code]

**Задача по ревью:**

[code] 
    kanban_complete(  
        summary="reviewed PR #123; 2 blocking issues found (SQL injection in /search, missing CSRF on /settings)",  
        metadata={  
            "pr_number": 123,  
            "findings": [  
                {"severity": "critical", "file": "api/search.py", "line": 42, "issue": "raw SQL concat"},  
                {"severity": "high", "file": "api/settings.py", "issue": "missing CSRF middleware"},  
            ],  
            "approved": False,  
        },  
    )  
    
[/code]

Формируйте `metadata` так, чтобы нижестоящие парсеры (ревьюеры, агрегаторы, планировщики) могли использовать её без повторного чтения вашего текста.

## Заявление карточек, которые вы действительно создали[​](<#claiming-cards-you-actually-created> "Direct link to Claiming cards you actually created")

Если ваш запуск создал новые kanban-задачи (через `kanban_create`), передайте их id в `created_cards` при вызове `kanban_complete`. Ядро проверяет, что каждый id существует и был создан вашим профилем; любой фантомный id блокирует завершение с ошибкой, перечисляющей, что пошло не так, и отклонённая попытка навсегда записывается в журнал событий задачи. **Указывайте только те id, которые вы получили из успешного возвращаемого значения `kanban_create` — никогда не придумывайте id из текста, никогда не вставляйте id из предыдущих запусков, никогда не заявляйте карточки, созданные другим воркером.**

[code] 
    # ХОРОШО — захватываем возвращаемые значения, затем заявляем их.  
    c1 = kanban_create(title="fix SQL injection in /search", assignee="security-worker")  
    c2 = kanban_create(title="add CSRF middleware to /settings", assignee="web-worker")  
      
    kanban_complete(  
        summary="Review done; spawned remediations for both findings.",  
        metadata={"pr_number": 123, "approved": False},  
        created_cards=[c1["task_id"], c2["task_id"]],  
    )  
    
[/code]

[code] 
    # ПЛОХО — заявление id, для которых у вас нет возвращаемых значений.  
    kanban_complete(  
        summary="Created remediation cards t_a1b2c3d4, t_deadbeef",  # вымышленные  
        created_cards=["t_a1b2c3d4", "t_deadbeef"],                   # → шлюз отклоняет  
    )  
    
[/code]

Если вызов `kanban_create` завершился ошибкой (исключение, tool_error), карточка НЕ была создана — не включайте фантомный id для неё. Повторите создание или пропустите id и упомяните ошибку в своей сводке. Проход сканирования текста также ловит ссылки `t_<hex>` в вашей свободной сводке, которые не разрешаются; они не блокируют завершение, но отображаются как предупреждения на задаче в дашборде.

## Причины блокировки, на которые отвечают быстро[​](<#block-reasons-that-get-answered-fast> "Direct link to Block reasons that get answered fast")

Плохо: `"stuck"` — у человека нет контекста.
Хорошо: одно предложение, называющее конкретное решение, которое вам нужно. Оставляйте более подробный контекст в комментарии.

[code] 
    kanban_comment(  
        task_id=os.environ["HERMES_KANBAN_TASK"],  
        body="Full context: I have user IPs from Cloudflare headers but some users are behind NATs with thousands of peers. Keying on IP alone causes false positives.",  
    )  
    kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth, skips anonymous endpoints)?")  
    
[/code]

Сообщение блокировки отображается в дашборде / уведомителе шлюза. Комментарий — это более глубокий контекст, который человек читает, открывая задачу.

## Стоящие отправки heartbeat'ов[​](<#heartbeats-worth-sending> "Direct link to Heartbeats worth sending")

Хорошие heartbeat'ы называют прогресс: `"epoch 12/50, loss 0.31"`, `"scanned 1.2M/2.4M rows"`, `"uploaded 47/120 videos"`.
Плохие heartbeat'ы: `"still working"`, пустые заметки, интервалы менее секунды. Максимум раз в несколько минут; полностью пропускайте для задач короче ~2 минут.

## Сценарии повторных попыток[​](<#retry-scenarios> "Direct link to Retry scenarios")

Если вы открываете задачу и `kanban_show` возвращает `runs: [...]` с одним или несколькими завершёнными запусками, вы — повторная попытка. `outcome` / `summary` / `error` предыдущих запусков говорят вам, что не сработало. Не повторяйте этот путь. Типичная диагностика повторных попыток:
  * `outcome: "timed_out"` — предыдущая попытка достигла `max_runtime_seconds`. Возможно, вам нужно разбить работу на части или сократить её.
  * `outcome: "crashed"` — нехватка памяти (OOM) или segfault. Уменьшите потребление памяти.
  * `outcome: "spawn_failed"` + `error: "..."` — обычно проблема конфигурации профиля (отсутствующие учётные данные, неправильный PATH). Спросите человека через `kanban_block` вместо слепых повторных попыток.
  * `outcome: "reclaimed"` + `summary: "task archived..."` — оператор заархивировал задачу из-под предыдущего запуска; вероятно, вам вообще не следует запускаться, внимательно проверьте статус.
  * `outcome: "blocked"` — предыдущая попытка заблокировалась; комментарий разблокировки уже должен быть в треде.



## НЕЛЬЗЯ[​](<#do-not> "Direct link to Do NOT")

  * Вызывать `delegate_task` как замену `kanban_create`. `delegate_task` предназначен для коротких подзадач рассуждения ВНУТРИ вашего запуска; `kanban_create` — для кросс-агентских передач, которые переживают один цикл API.
  * Изменять файлы за пределами `$HERMES_KANBAN_WORKSPACE`, если тело задачи не говорит иного.
  * Создавать последующие задачи, назначенные себе — назначайте соответствующему специалисту.
  * Завершать задачу, которую вы на самом деле не закончили. Вместо этого заблокируйте её.



## Подводные камни[​](<#pitfalls> "Direct link to Pitfalls")

**Состояние задачи может измениться между отправкой и вашим запуском.** Между тем, как диспетчер захватил задачу, и моментом, когда ваш процесс фактически загрузился, задача могла быть заблокирована, переназначена или архивирована. Всегда сначала выполняйте `kanban_show`. Если он сообщает `blocked` или `archived`, остановитесь — вы не должны запускаться.

**В рабочем пространстве могут остаться устаревшие артефакты.** Особенно в рабочих пространствах `dir:` и `worktree` могут быть файлы от предыдущих запусков. Прочитайте тред комментариев — он обычно объясняет, почему вы запускаетесь снова и в каком состоянии находится рабочее пространство.

**Не полагайтесь на CLI, когда доступна инструкция.** Инструменты `kanban_*` работают во всех терминальных бэкендах (Docker, Modal, SSH). `hermes kanban <verb>` из вашего терминального инструмента не сработает в контейнерных бэкендах, потому что CLI там не установлен. Если сомневаетесь, используйте инструмент.

## CLI как запасной вариант (для скриптов)[​](<#cli-fallback-for-scripting> "Direct link to CLI fallback (for scripting)")

У каждого инструмента есть CLI-эквивалент для операторов-людей и скриптов:
  * `kanban_show` ↔ `hermes kanban show <id> --json`
  * `kanban_complete` ↔ `hermes kanban complete <id> --summary "..." --metadata '{...}'`
  * `kanban_block` ↔ `hermes kanban block <id> "reason"`
  * `kanban_create` ↔ `hermes kanban create "title" --assignee <profile> [--parent <id>]`
  * и т.д.


Используйте инструменты изнутри агента; CLI существует для человека за терминалом.

  * [Метаданные навыка](<#skill-metadata>)
  * [Справка: полный SKILL.md](<#reference-full-skillmd>)
  * [Обработка рабочего пространства](<#workspace-handling>)
  * [Изоляция тенантов](<#tenant-isolation>)
  * [Хорошие формы сводок и метаданных](<#good-summary--metadata-shapes>)
  * [Заявление карточек, которые вы действительно создали](<#claiming-cards-you-actually-created>)
  * [Причины блокировки, на которые отвечают быстро](<#block-reasons-that-get-answered-fast>)
  * [Стоящие отправки heartbeat'ов](<#heartbeats-worth-sending>)
  * [Сценарии повторных попыток](<#retry-scenarios>)
  * [НЕЛЬЗЯ](<#do-not>)
  * [Подводные камни](<#pitfalls>)
  * [CLI как запасной вариант (для скриптов)](<#cli-fallback-for-scripting>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/devops/devops-kanban-worker -->
