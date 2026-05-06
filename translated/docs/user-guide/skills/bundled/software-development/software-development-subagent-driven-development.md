On this page
Выполнение планов через делегирование задач суб-агентам (двухэтапная проверка).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Source| Встроенный (устанавливается по умолчанию) |
|Path| `skills/software-development/subagent-driven-development` |
|Version| `1.1.0` |
|Author| Hermes Agent (адаптировано из obra/superpowers) |
|License| MIT |
|Tags| `delegation`, `subagent`, `implementation`, `workflow`, `parallel` |
|Related skills| [`writing-plans`](</docs/user-guide/skills/bundled/software-development/software-development-writing-plans>), [`requesting-code-review`](</docs/user-guide/skills/bundled/software-development/software-development-requesting-code-review>), [`test-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-test-driven-development>) |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
> [!info]
> Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Именно эти инструкции видит агент, когда навык активен.

# Subagent-Driven Development
## Overview[​](<#overview> "Direct link to Overview")
Выполняйте планы реализации, отправляя отдельные суб-агенты на каждую задачу с систематической двухэтапной проверкой.
**Ключевой принцип:** Новый суб-агент на каждую задачу + двухэтапная проверка (спецификация, затем качество) = высокое качество, быстрая итерация.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
Используйте этот навык, когда:
  * У вас есть план реализации (от навыка writing-plans или из требований пользователя)
  * Задачи в основном независимы
  * Качество и соответствие спецификации важны
  * Вы хотите автоматизированную проверку между задачами

**vs. ручное выполнение:**
  * Чистый контекст для каждой задачи (нет путаницы от накопленного состояния)
  * Автоматизированный процесс проверки выявляет проблемы на ранних этапах
  * Последовательные проверки качества по всем задачам
  * Суб-агенты могут задавать вопросы перед началом работы

## The Process[​](<#the-process> "Direct link to The Process")
### 1\\. Read and Parse Plan[​](<#1-read-and-parse-plan> "Direct link to 1. Read and Parse Plan")
Прочитайте файл плана. Извлеките ВСЕ задачи с полным текстом и контекстом заранее. Создайте список задач:
```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Ключевой момент:** Прочитайте план ОДИН РАЗ. Извлеките всё. Не заставляйте суб-агентов читать файл плана — передавайте полный текст задачи непосредственно в контексте.
### 2\\. Per-Task Workflow[​](<#2-per-task-workflow> "Direct link to 2. Per-Task Workflow")
Для КАЖДОЙ задачи в плане:
#### Step 1: Dispatch Implementer Subagent[​](<#step-1-dispatch-implementer-subagent> "Direct link to Step 1: Dispatch Implementer Subagent")
Используйте `delegate_task` с полным контекстом:
```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```
#### Step 2: Dispatch Spec Compliance Reviewer[​](<#step-2-dispatch-spec-compliance-reviewer> "Direct link to Step 2: Dispatch Spec Compliance Reviewer")
После завершения реализации проверьте соответствие исходной спецификации:
```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```
**Если найдены несоответствия спецификации:** Исправьте пробелы, затем повторно запустите проверку спецификации. Продолжайте только после соответствия спецификации.
#### Step 3: Dispatch Code Quality Reviewer[​](<#step-3-dispatch-code-quality-reviewer> "Direct link to Step 3: Dispatch Code Quality Reviewer")
После успешной проверки соответствия спецификации:
```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```
**Если найдены проблемы качества:** Исправьте проблемы, перепроверьте. Продолжайте только после одобрения.
#### Step 4: Mark Complete[​](<#step-4-mark-complete> "Direct link to Step 4: Mark Complete")
```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```
### 3\\. Final Review[​](<#3-final-review> "Direct link to 3. Final Review")
После завершения ВСЕХ задач отправьте финального проверяющего интеграцию:
```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```
### 4\\. Verify and Commit[​](<#4-verify-and-commit> "Direct link to 4. Verify and Commit")
```python
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```
## Task Granularity[​](<#task-granularity> "Direct link to Task Granularity")
**Каждая задача = 2-5 минут сфокусированной работы.**
**Слишком крупно:**
  * "Implement user authentication system"

**Правильный размер:**
  * "Create User model with email and password fields"
  * "Add password hashing function"
  * "Create login endpoint"
  * "Add JWT token generation"
  * "Create registration endpoint"

## Red Flags — Never Do These[​](<#red-flags--never-do-these> "Direct link to Red Flags — Never Do These")
  * Начинать реализацию без плана
  * Пропускать проверки (соответствие спецификации ИЛИ качество кода)
  * Продолжать работу с неисправленными критическими/важными проблемами
  * Отправлять несколько суб-агентов реализации на задачи, затрагивающие одни и те же файлы
  * Заставлять суб-агента читать файл плана (вместо этого передавайте полный текст в контексте)
  * Пропускать контекст сцены (суб-агент должен понимать, куда вписывается задача)
  * Игнорировать вопросы суб-агента (отвечайте, прежде чем позволить им продолжить)
  * Принимать «почти правильно» в отношении соответствия спецификации
  * Пропускать циклы проверки (проверяющий нашёл проблемы → исправление → снова проверка)
  * Позволять суб-агенту-исполнителю заменять собой настоящую проверку (нужны оба)
  * **Начинать проверку качества кода до того, как проверка спецификации пройдена** (неправильный порядок)
  * Переходить к следующей задаче, пока хотя бы одна проверка имеет открытые проблемы

## Handling Issues[​](<#handling-issues> "Direct link to Handling Issues")
### If Subagent Asks Questions[​](<#if-subagent-asks-questions> "Direct link to If Subagent Asks Questions")
  * Отвечайте чётко и полностью
  * Предоставьте дополнительный контекст при необходимости
  * Не торопите их с реализацией

### If Reviewer Finds Issues[​](<#if-reviewer-finds-issues> "Direct link to If Reviewer Finds Issues")
  * Суб-агент-исполнитель (или новый) исправляет их
  * Проверяющий проверяет снова
  * Повторяйте до одобрения
  * Не пропускайте повторную проверку

### If Subagent Fails a Task[​](<#if-subagent-fails-a-task> "Direct link to If Subagent Fails a Task")
  * Отправьте нового суб-агента для исправления с конкретными инструкциями о том, что пошло не так
  * Не пытайтесь исправлять вручную в сессии контроллера (загрязнение контекста)

## Efficiency Notes[​](<#efficiency-notes> "Direct link to Efficiency Notes")
**Почему новый суб-агент на каждую задачу:**
  * Предотвращает загрязнение контекста от накопленного состояния
  * Каждый суб-агент получает чистый, сфокусированный контекст
  * Нет путаницы от кода или рассуждений предыдущих задач

**Почему двухэтапная проверка:**
  * Проверка спецификации выявляет недо- или пере-строительство на ранних этапах
  * Проверка качества гарантирует, что реализация выполнена хорошо
  * Выявляет проблемы до того, как они накопятся между задачами

**Компромисс по стоимости:**
  * Больше вызовов суб-агентов (исполнитель + 2 проверяющих на задачу)
  * Но выявляет проблемы на ранних этапах (дешевле, чем отладка накопившихся проблем позже)

## Integration with Other Skills[​](<#integration-with-other-skills> "Direct link to Integration with Other Skills")
### With writing-plans[​](<#with-writing-plans> "Direct link to With writing-plans")
Этот навык ВЫПОЛНЯЕТ планы, созданные навыком writing-plans:
  1. Требования пользователя → writing-plans → план реализации
  2. План реализации → subagent-driven-development → рабочий код

### With test-driven-development[​](<#with-test-driven-development> "Direct link to With test-driven-development")
Суб-агенты-исполнители должны следовать TDD:
  1. Сначала напишите падающий тест
  2. Реализуйте минимальный код
  3. Убедитесь, что тест проходит
  4. Зафиксируйте изменения

Включайте инструкции TDD в контекст каждого исполнителя.
### With requesting-code-review[​](<#with-requesting-code-review> "Direct link to With requesting-code-review")
Процесс двухэтапной проверки И ЕСТЬ проверка кода. Для финальной проверки интеграции используйте измерения проверки кода из навыка requesting-code-review.
### With systematic-debugging[​](<#with-systematic-debugging> "Direct link to With systematic-debugging")
Если суб-агент сталкивается с ошибками во время реализации:
  1. Следуйте процессу systematic-debugging
  2. Найдите коренную причину перед исправлением
  3. Напишите регрессионный тест
  4. Возобновите реализацию

## Example Workflow[​](<#example-workflow> "Direct link to Example Workflow")
```python
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```
## Remember[​](<#remember> "Direct link to Remember")
```python
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```
**Качество — не случайность. Это результат систематического процесса.**
## Further reading (load when relevant)[​](<#further-reading-load-when-relevant> "Direct link to Further reading \(load when relevant\)")
Когда оркестрация включает значительное использование контекста, длительные циклы проверки или сложные контрольные точки валидации, загрузите эти справочники для соответствующей дисциплины:
  * **`references/context-budget-discipline.md`** — Четырёхуровневая модель деградации контекста (PEAK / GOOD / DEGRADING / POOR), правила глубины чтения, масштабируемые с размером окна контекста, и ранние признаки тихой деградации. Загружайте, когда запуск явно будет потреблять значительный контекст (многофазные планы, множество суб-агентов, крупные артефакты).
  * **`references/gates-taxonomy.md`** — Четыре канонических типа шлюзов (Pre-flight, Revision, Escalation, Abort) с поведением, восстановлением и примерами. Загружайте при проектировании или проверке любого рабочего процесса, имеющего контрольные точки валидации — используйте терминологию явно, чтобы каждый шлюз имел определённые правила входа, поведения при сбое и возобновления.

Оба справочника адаптированы из gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Overview](<#overview>)
  * [When to Use](<#when-to-use>)
  * [The Process](<#the-process>)
    * [1\\. Read and Parse Plan](<#1-read-and-parse-plan>)
    * [2\\. Per-Task Workflow](<#2-per-task-workflow>)
    * [3\\. Final Review](<#3-final-review>)
    * [4\\. Verify and Commit](<#4-verify-and-commit>)
  * [Task Granularity](<#task-granularity>)
  * [Red Flags — Never Do These](<#red-flags--never-do-these>)
  * [Handling Issues](<#handling-issues>)
    * [If Subagent Asks Questions](<#if-subagent-asks-questions>)
    * [If Reviewer Finds Issues](<#if-reviewer-finds-issues>)
    * [If Subagent Fails a Task](<#if-subagent-fails-a-task>)
  * [Efficiency Notes](<#efficiency-notes>)
  * [Integration with Other Skills](<#integration-with-other-skills>)
    * [With writing-plans](<#with-writing-plans>)
    * [With test-driven-development](<#with-test-driven-development>)
    * [With requesting-code-review](<#with-requesting-code-review>)
    * [With systematic-debugging](<#with-systematic-debugging>)
  * [Example Workflow](<#example-workflow>)
  * [Remember](<#remember>)
  * [Further reading (load when relevant)](<#further-reading-load-when-relevant>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development -->
