На этой странице
Готовые рецепты (copy-paste) для типовых сценариев автоматизации. Каждый шаблон использует встроенный [планировщик cron](</docs/user-guide/features/cron>) Hermes для временных триггеров и [платформу вебхуков](</docs/user-guide/messaging/webhooks>) для событийных триггеров.
Каждый шаблон работает с **любой моделью** — не привязан к конкретному провайдеру.
Три типа триггеров
Триггер| Как| Инструмент  
---|---|---  
**Расписание**|  Запускается по расписанию (ежечасно, каждую ночь, еженедельно)| Инструмент `cronjob` или слэш-команда `/cron`  
**Событие GitHub**|  Срабатывает при открытии PR, пушах, issues, результатах CI| Платформа вебхуков (`hermes webhook subscribe`)  
**API-вызов**|  Внешний сервис отправляет POST с JSON на ваш эндпоинт| Платформа вебхуков (маршруты config.yaml или `hermes webhook subscribe`)  
Все три поддерживают доставку в Telegram, Discord, Slack, SMS, email, комментарии GitHub или локальные файлы.
* * *
## Рабочий процесс разработки[​](<#development-workflow> "Прямая ссылка на Рабочий процесс разработки")
### Ночная триаж бэклога[​](<#nightly-backlog-triage> "Прямая ссылка на Ночная триаж бэклога")
Каждую ночь маркировать, приоритизировать и обобщать новые issues. Доставляет дайджест в командный канал.
**Триггер:** Расписание (еженощно)
[code] 
    hermes cron create "0 2 * * *" \  
      "You are a project manager triaging the NousResearch/hermes-agent GitHub repo.  
      
    1. Run: gh issue list --repo NousResearch/hermes-agent --state open --json number,title,labels,author,createdAt --limit 30  
    2. Identify issues opened in the last 24 hours  
    3. For each new issue:  
       - Suggest a priority label (P0-critical, P1-high, P2-medium, P3-low)  
       - Suggest a category label (bug, feature, docs, security)  
       - Write a one-line triage note  
    4. Summarize: total open issues, new today, breakdown by priority  
      
    Format as a clean digest. If no new issues, respond with [SILENT]." \  
      --name "Nightly backlog triage" \  
      --deliver telegram  
    
[/code]
### Автоматическое ревью кода PR[​](<#automatic-pr-code-review> "Прямая ссылка на Автоматическое ревью кода PR")
Автоматически рецензировать каждый pull request при его открытии. Публикует комментарий ревью прямо в PR.
**Триггер:** Вебхук GitHub
**Вариант A — Динамическая подписка (CLI):**
[code] 
    hermes webhook subscribe github-pr-review \  
      --events "pull_request" \  
      --prompt "Review this pull request:  
    Repository: {repository.full_name}  
    PR #{pull_request.number}: {pull_request.title}  
    Author: {pull_request.user.login}  
    Action: {action}  
    Diff URL: {pull_request.diff_url}  
      
    Fetch the diff with: curl -sL {pull_request.diff_url}  
      
    Review for:  
    - Security issues (injection, auth bypass, secrets in code)  
    - Performance concerns (N+1 queries, unbounded loops, memory leaks)  
    - Code quality (naming, duplication, error handling)  
    - Missing tests for new behavior  
      
    Post a concise review. If the PR is a trivial docs/typo change, say so briefly." \  
      --skills "github-code-review" \  
      --deliver github_comment  
    
[/code]
**Вариант B — Статический маршрут (config.yaml):**
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          port: 8644  
          secret: "your-global-secret"  
          routes:  
            github-pr-review:  
              events: ["pull_request"]  
              secret: "github-webhook-secret"  
              prompt: |  
                Review PR #{pull_request.number}: {pull_request.title}  
                Repository: {repository.full_name}  
                Author: {pull_request.user.login}  
                Diff URL: {pull_request.diff_url}  
                Review for security, performance, and code quality.  
              skills: ["github-code-review"]  
              deliver: "github_comment"  
              deliver_extra:  
                repo: "{repository.full_name}"  
                pr_number: "{pull_request.number}"  
    
[/code]
Затем в GitHub: **Settings → Webhooks → Add webhook** → Payload URL: `http://your-server:8644/webhooks/github-pr-review`, Content type: `application/json`, Secret: `github-webhook-secret`, Events: **Pull requests**.
### Обнаружение расхождения документации[​](<#docs-drift-detection> "Прямая ссылка на Обнаружение расхождения документации")
Еженедельное сканирование объединённых PR для поиска изменений API, требующих обновления документации.
**Триггер:** Расписание (еженедельно)
[code] 
    hermes cron create "0 9 * * 1" \  
      "Scan the NousResearch/hermes-agent repo for documentation drift.  
      
    1. Run: gh pr list --repo NousResearch/hermes-agent --state merged --json number,title,files,mergedAt --limit 30  
    2. Filter to PRs merged in the last 7 days  
    3. For each merged PR, check if it modified:  
       - Tool schemas (tools/*.py) — may need docs/reference/tools-reference.md update  
       - CLI commands (hermes_cli/commands.py, hermes_cli/main.py) — may need docs/reference/cli-commands.md update  
       - Config options (hermes_cli/config.py) — may need docs/user-guide/configuration.md update  
       - Environment variables — may need docs/reference/environment-variables.md update  
    4. Cross-reference: for each code change, check if the corresponding docs page was also updated in the same PR  
      
    Report any gaps where code changed but docs didn't. If everything is in sync, respond with [SILENT]." \  
      --name "Docs drift detection" \  
      --deliver telegram  
    
[/code]
### Аудит безопасности зависимостей[​](<#dependency-security-audit> "Прямая ссылка на Аудит безопасности зависимостей")
Ежедневное сканирование на известные уязвимости в зависимостях проекта.
**Триггер:** Расписание (ежедневно)
[code] 
    hermes cron create "0 6 * * *" \  
      "Run a dependency security audit on the hermes-agent project.  
      
    1. cd ~/.hermes/hermes-agent && source .venv/bin/activate  
    2. Run: pip audit --format json 2>/dev/null || pip audit 2>&1  
    3. Run: npm audit --json 2>/dev/null (in website/ directory if it exists)  
    4. Check for any CVEs with CVSS score >= 7.0  
      
    If vulnerabilities found:  
    - List each one with package name, version, CVE ID, severity  
    - Check if an upgrade is available  
    - Note if it's a direct dependency or transitive  
      
    If no vulnerabilities, respond with [SILENT]." \  
      --name "Dependency audit" \  
      --deliver telegram  
    
[/code]
* * *
## DevOps и Мониторинг[​](<#devops--monitoring> "Прямая ссылка на DevOps и Мониторинг")
### Проверка развёртывания[​](<#deploy-verification> "Прямая ссылка на Проверка развёртывания")
Запускать smoke-тесты после каждого развёртывания. Ваш CI/CD пайплайн отправляет POST на вебхук, когда деплой завершён.
**Триггер:** API-вызов (вебхук)
[code] 
    hermes webhook subscribe deploy-verify \  
      --events "deployment" \  
      --prompt "A deployment just completed:  
    Service: {service}  
    Environment: {environment}  
    Version: {version}  
    Deployed by: {deployer}  
      
    Run these verification steps:  
    1. Check if the service is responding: curl -s -o /dev/null -w '%{http_code}' {health_url}  
    2. Search recent logs for errors: check the deployment payload for any error indicators  
    3. Verify the version matches: curl -s {health_url}/version  
      
    Report: deployment status (healthy/degraded/failed), response time, any errors found.  
    If healthy, keep it brief. If degraded or failed, provide detailed diagnostics." \  
      --deliver telegram  
    
[/code]
Ваш CI/CD пайплайн запускает его:
[code] 
    curl -X POST http://your-server:8644/webhooks/deploy-verify \  
      -H "Content-Type: application/json" \  
      -H "X-Hub-Signature-256: sha256=$(echo -n '{"service":"api","environment":"prod","version":"2.1.0","deployer":"ci","health_url":"https://api.example.com/health"}' | openssl dgst -sha256 -hmac 'your-secret' | cut -d' ' -f2)" \  
      -d '{"service":"api","environment":"prod","version":"2.1.0","deployer":"ci","health_url":"https://api.example.com/health"}'  
    
[/code]
### Триаж оповещений[​](<#alert-triage> "Прямая ссылка на Триаж оповещений")
Сопоставлять оповещения мониторинга с недавними изменениями для составления ответа. Работает с Datadog, PagerDuty, Grafana или любой системой оповещения, которая может отправлять POST с JSON.
**Триггер:** API-вызов (вебхук)
[code] 
    hermes webhook subscribe alert-triage \  
      --prompt "Monitoring alert received:  
    Alert: {alert.name}  
    Severity: {alert.severity}  
    Service: {alert.service}  
    Message: {alert.message}  
    Timestamp: {alert.timestamp}  
      
    Investigate:  
    1. Search the web for known issues with this error pattern  
    2. Check if this correlates with any recent deployments or config changes  
    3. Draft a triage summary with:  
       - Likely root cause  
       - Suggested first response steps  
       - Escalation recommendation (P1-P4)  
      
    Be concise. This goes to the on-call channel." \  
      --deliver slack  
    
[/code]
### Мониторинг доступности[​](<#uptime-monitor> "Прямая ссылка на Мониторинг доступности")
Проверять эндпоинты каждые 30 минут. Уведомлять только при сбое.
**Триггер:** Расписание (каждые 30 мин)
~/.hermes/scripts/check-uptime.py
[code]
    import urllib.request, json, time  
      
    ENDPOINTS = [  
        {"name": "API", "url": "https://api.example.com/health"},  
        {"name": "Web", "url": "https://www.example.com"},  
        {"name": "Docs", "url": "https://docs.example.com"},  
    ]  
      
    results = []  
    for ep in ENDPOINTS:  
        try:  
            start = time.time()  
            req = urllib.request.Request(ep["url"], headers={"User-Agent": "Hermes-Monitor/1.0"})  
            resp = urllib.request.urlopen(req, timeout=10)  
            elapsed = round((time.time() - start) * 1000)  
            results.append({"name": ep["name"], "status": resp.getcode(), "ms": elapsed})  
        except Exception as e:  
            results.append({"name": ep["name"], "status": "DOWN", "error": str(e)})  
      
    down = [r for r in results if r.get("status") == "DOWN" or (isinstance(r.get("status"), int) and r["status"] >= 500)]  
    if down:  
        print("OUTAGE DETECTED")  
        for r in down:  
            print(f"  {r['name']}: {r.get('error', f'HTTP {r[\"status\"]}')} ")  
        print(f"\nAll results: {json.dumps(results, indent=2)}")  
    else:  
        print("NO_ISSUES")  
    
[/code]
[code] 
    hermes cron create "every 30m" \  
      "If the script reports OUTAGE DETECTED, summarize which services are down and suggest likely causes. If NO_ISSUES, respond with [SILENT]." \  
      --script ~/.hermes/scripts/check-uptime.py \  
      --name "Uptime monitor" \  
      --deliver telegram  
    
[/code]
* * *
## Исследования и аналитика[​](<#research--intelligence> "Прямая ссылка на Исследования и аналитика")
### Разведка конкурентных репозиториев[​](<#competitive-repository-scout> "Прямая ссылка на Разведка конкурентных репозиториев")
Отслеживать репозитории конкурентов на предмет интересных PR, функций и архитектурных решений.
**Триггер:** Расписание (ежедневно)
[code] 
    hermes cron create "0 8 * * *" \  
      "Scout these AI agent repositories for notable activity in the last 24 hours:  
      
    Repos to check:  
    - anthropics/claude-code  
    - openai/codex  
    - All-Hands-AI/OpenHands  
    - Aider-AI/aider  
      
    For each repo:  
    1. gh pr list --repo <repo> --state all --json number,title,author,createdAt,mergedAt --limit 15  
    2. gh issue list --repo <repo> --state open --json number,title,labels,createdAt --limit 10  
      
    Focus on:  
    - New features being developed  
    - Architectural changes  
    - Integration patterns we could learn from  
    - Security fixes that might affect us too  
      
    Skip routine dependency bumps and CI fixes. If nothing notable, respond with [SILENT].  
    If there are findings, organize by repo with brief analysis of each item." \  
      --skills "competitive-pr-scout" \  
      --name "Competitor scout" \  
      --deliver telegram  
    
[/code]
### AI-дайджест новостей[​](<#ai-news-digest> "Прямая ссылка на AI-дайджест новостей")
Еженедельный обзор событий в сфере AI/ML.
**Триггер:** Расписание (еженедельно)
[code] 
    hermes cron create "0 9 * * 1" \  
      "Generate a weekly AI news digest covering the past 7 days:  
      
    1. Search the web for major AI announcements, model releases, and research breakthroughs  
    2. Search for trending ML repositories on GitHub  
    3. Check arXiv for highly-cited papers on language models and agents  
      
    Structure:  
    ## Headlines (3-5 major stories)  
    ## Notable Papers (2-3 papers with one-sentence summaries)  
    ## Open Source (interesting new repos or major releases)  
    ## Industry Moves (funding, acquisitions, launches)  
      
    Keep each item to 1-2 sentences. Include links. Total under 600 words." \  
      --name "Weekly AI digest" \  
      --deliver telegram  
    
[/code]
### Дайджест статей с заметками[​](<#paper-digest-with-notes> "Прямая ссылка на Дайджест статей с заметками")
Ежедневное сканирование arXiv с сохранением кратких обзоров в вашу систему заметок.
**Триггер:** Расписание (ежедневно)
[code] 
    hermes cron create "0 8 * * *" \  
      "Search arXiv for the 3 most interesting papers on 'language model reasoning' OR 'tool-use agents' from the past day. For each paper, create an Obsidian note with the title, authors, abstract summary, key contribution, and potential relevance to Hermes Agent development." \  
      --skills "arxiv,obsidian" \  
      --name "Paper digest" \  
      --deliver local  
    
[/code]
* * *
## Автоматизация событий GitHub[​](<#github-event-automations> "Прямая ссылка на Автоматизация событий GitHub")
### Авто-маркировка issues[​](<#issue-auto-labeling> "Прямая ссылка на Авто-маркировка issues")
Автоматически маркировать и отвечать на новые issues.
**Триггер:** Вебхук GitHub
[code] 
    hermes webhook subscribe github-issues \  
      --events "issues" \  
      --prompt "New GitHub issue received:  
    Repository: {repository.full_name}  
    Issue #{issue.number}: {issue.title}  
    Author: {issue.user.login}  
    Action: {action}  
    Body: {issue.body}  
    Labels: {issue.labels}  
      
    If this is a new issue (action=opened):  
    1. Read the issue title and body carefully  
    2. Suggest appropriate labels (bug, feature, docs, security, question)  
    3. If it's a bug report, check if you can identify the affected component from the description  
    4. Post a helpful initial response acknowledging the issue  
      
    If this is a label or assignment change, respond with [SILENT]." \  
      --deliver github_comment  
    
[/code]
### Анализ сбоев CI[​](<#ci-failure-analysis> "Прямая ссылка на Анализ сбоев CI")
Анализировать сбои CI и публиковать диагностику в PR.
**Триггер:** Вебхук GitHub
[code] 
    # config.yaml route  
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          routes:  
            ci-failure:  
              events: ["check_run"]  
              secret: "ci-secret"  
              prompt: |  
                CI check failed:  
                Repository: {repository.full_name}  
                Check: {check_run.name}  
                Status: {check_run.conclusion}  
                PR: #{check_run.pull_requests.0.number}  
                Details URL: {check_run.details_url}  
      
                If conclusion is "failure":  
                1. Fetch the log from the details URL if accessible  
                2. Identify the likely cause of failure  
                3. Suggest a fix  
                If conclusion is "success", respond with [SILENT].  
              deliver: "github_comment"  
              deliver_extra:  
                repo: "{repository.full_name}"  
                pr_number: "{check_run.pull_requests.0.number}"  
    
[/code]
### Авто-перенос изменений между репозиториями[​](<#auto-port-changes-across-repos> "Прямая ссылка на Авто-перенос изменений между репозиториями")
Когда PR объединяется в одном репозитории, автоматически перенести эквивалентные изменения в другой.
**Триггер:** Вебхук GitHub
[code] 
    hermes webhook subscribe auto-port \  
      --events "pull_request" \  
      --prompt "PR merged in the source repository:  
    Repository: {repository.full_name}  
    PR #{pull_request.number}: {pull_request.title}  
    Author: {pull_request.user.login}  
    Action: {action}  
    Merge commit: {pull_request.merge_commit_sha}  
      
    If action is 'closed' and pull_request.merged is true:  
    1. Fetch the diff: curl -sL {pull_request.diff_url}  
    2. Analyze what changed  
    3. Determine if this change needs to be ported to the Go SDK equivalent  
    4. If yes, create a branch, apply the equivalent changes, and open a PR on the target repo  
    5. Reference the original PR in the new PR description  
      
    If action is not 'closed' or not merged, respond with [SILENT]." \  
      --skills "github-pr-workflow" \  
      --deliver log  
    
[/code]
* * *
## Бизнес-операции[​](<#business-operations> "Прямая ссылка на Бизнес-операции")
### Мониторинг платежей Stripe[​](<#stripe-payment-monitoring> "Прямая ссылка на Мониторинг платежей Stripe")
Отслеживать события платежей и получать сводки по сбоям.
**Триггер:** API-вызов (вебхук)
[code] 
    hermes webhook subscribe stripe-payments \  
      --events "payment_intent.succeeded,payment_intent.payment_failed,charge.dispute.created" \  
      --prompt "Stripe event received:  
    Event type: {type}  
    Amount: {data.object.amount} cents ({data.object.currency})  
    Customer: {data.object.customer}  
    Status: {data.object.status}  
      
    For payment_intent.payment_failed:  
    - Identify the failure reason from {data.object.last_payment_error}  
    - Suggest whether this is a transient issue (retry) or permanent (contact customer)  
      
    For charge.dispute.created:  
    - Flag as urgent  
    - Summarize the dispute details  
      
    For payment_intent.succeeded:  
    - Brief confirmation only  
      
    Keep responses concise for the ops channel." \  
      --deliver slack  
    
[/code]
### Ежедневная сводка доходов[​](<#daily-revenue-summary> "Прямая ссылка на Ежедневная сводка доходов")
Составлять ключевые бизнес-показатели каждое утро.
**Триггер:** Расписание (ежедневно)
[code] 
    hermes cron create "0 8 * * *" \  
      "Generate a morning business metrics summary.  
      
    Search the web for:  
    1. Current Bitcoin and Ethereum prices  
    2. S&P 500 status (pre-market or previous close)  
    3. Any major tech/AI industry news from the last 12 hours  
      
    Format as a brief morning briefing, 3-4 bullet points max.  
    Deliver as a clean, scannable message." \  
      --name "Morning briefing" \  
      --deliver telegram  
    
[/code]
* * *
## Многоскилловые рабочие процессы[​](<#multi-skill-workflows> "Прямая ссылка на Многоскилловые рабочие процессы")
### Пайплайн аудита безопасности[​](<#security-audit-pipeline> "Прямая ссылка на Пайплайн аудита безопасности")
Объединить несколько навыков для комплексной еженедельной проверки безопасности.
**Триггер:** Расписание (еженедельно)
[code] 
    hermes cron create "0 3 * * 0" \  
      "Run a comprehensive security audit of the hermes-agent codebase.  
      
    1. Check for dependency vulnerabilities (pip audit, npm audit)  
    2. Search the codebase for common security anti-patterns:  
       - Hardcoded secrets or API keys  
       - SQL injection vectors (string formatting in queries)  
       - Path traversal risks (user input in file paths without validation)  
       - Unsafe deserialization (pickle.loads, yaml.load without SafeLoader)  
    3. Review recent commits (last 7 days) for security-relevant changes  
    4. Check if any new environment variables were added without being documented  
      
    Write a security report with findings categorized by severity (Critical, High, Medium, Low).  
    If nothing found, report a clean bill of health." \  
      --skills "codebase-security-audit" \  
      --name "Weekly security audit" \  
      --deliver telegram  
    
[/code]
### Контентный пайплайн[​](<#content-pipeline> "Прямая ссылка на Контентный пайплайн")
Исследовать, черновиковать и подготавливать контент по расписанию.
**Триггер:** Расписание (еженедельно)
[code] 
    hermes cron create "0 10 * * 3" \  
      "Research and draft a technical blog post outline about a trending topic in AI agents.  
      
    1. Search the web for the most discussed AI agent topics this week  
    2. Pick the most interesting one that's relevant to open-source AI agents  
    3. Create an outline with:  
       - Hook/intro angle  
       - 3-4 key sections  
       - Technical depth appropriate for developers  
       - Conclusion with actionable takeaway  
    4. Save the outline to ~/drafts/blog-$(date +%Y%m%d).md  
      
    Keep the outline to ~300 words. This is a starting point, not a finished post." \  
      --name "Blog outline" \  
      --deliver local  
    
[/code]
* * *
## Краткий справочник[​](<#quick-reference> "Прямая ссылка на Краткий справочник")
### Синтаксис расписания Cron[​](<#cron-schedule-syntax> "Прямая ссылка на Синтаксис расписания Cron")
Выражение| Значение  
---|---  
`every 30m`| Каждые 30 минут  
`every 2h`| Каждые 2 часа  
`0 2 * * *`| Ежедневно в 2:00  
`0 9 * * 1`| Каждый понедельник в 9:00  
`0 9 * * 1-5`| По будням в 9:00  
`0 3 * * 0`| Каждое воскресенье в 3:00  
`0 */6 * * *`| Каждые 6 часов  
### Цели доставки[​](<#delivery-targets> "Прямая ссылка на Цели доставки")
Цель| Флаг| Примечания  
---|---|---  
Тот же чат| `--deliver origin`| По умолчанию — доставляет туда, где была создана задача  
Локальный файл| `--deliver local`| Сохраняет вывод, без уведомления  
Telegram| `--deliver telegram`| Домашний канал или `telegram:CHAT_ID` для конкретного  
Discord| `--deliver discord`| Домашний канал или `discord:CHANNEL_ID`  
Slack| `--deliver slack`| Домашний канал  
SMS| `--deliver sms:+15551234567`| Прямо на номер телефона  
Конкретная ветка| `--deliver telegram:-100123:456`| Тема форума Telegram  
### Переменные шаблонов вебхуков[​](<#webhook-template-variables> "Прямая ссылка на Переменные шаблонов вебхуков")
Переменная| Описание  
---|---  
`{pull_request.title}`| Заголовок PR  
`{issue.number}`| Номер issue  
`{repository.full_name}`| `owner/repo`  
`{action}`| Действие события (opened, closed и т.д.)  
`{__raw__}`| Полный JSON-пейлоад (обрезается до 4000 символов)  
`{sender.login}`| Пользователь GitHub, вызвавший событие  
### Шаблон [SILENT][​](<#the-silent-pattern> "Прямая ссылка на Шаблон [SILENT]")
Если ответ cron-задачи содержит `[SILENT]`, доставка подавляется. Используйте это, чтобы избежать спама уведомлениями в тихие запуски:
[code] 
    If nothing noteworthy happened, respond with [SILENT].  
    
[/code]
Это означает, что вы получите уведомление только тогда, когда агенту есть что сообщить.
  * [Рабочий процесс разработки](<#development-workflow>)
    * [Ночная триаж бэклога](<#nightly-backlog-triage>)
    * [Автоматическое ревью кода PR](<#automatic-pr-code-review>)
    * [Обнаружение расхождения документации](<#docs-drift-detection>)
    * [Аудит безопасности зависимостей](<#dependency-security-audit>)
  * [DevOps и Мониторинг](<#devops--monitoring>)
    * [Проверка развёртывания](<#deploy-verification>)
    * [Триаж оповещений](<#alert-triage>)
    * [Мониторинг доступности](<#uptime-monitor>)
  * [Исследования и аналитика](<#research--intelligence>)
    * [Разведка конкурентных репозиториев](<#competitive-repository-scout>)
    * [AI-дайджест новостей](<#ai-news-digest>)
    * [Дайджест статей с заметками](<#paper-digest-with-notes>)
  * [Автоматизация событий GitHub](<#github-event-automations>)
    * [Авто-маркировка issues](<#issue-auto-labeling>)
    * [Анализ сбоев CI](<#ci-failure-analysis>)
    * [Авто-перенос изменений между репозиториями](<#auto-port-changes-across-repos>)
  * [Бизнес-операции](<#business-operations>)
    * [Мониторинг платежей Stripe](<#stripe-payment-monitoring>)
    * [Ежедневная сводка доходов](<#daily-revenue-summary>)
  * [Многоскилловые рабочие процессы](<#multi-skill-workflows>)
    * [Пайплайн аудита безопасности](<#security-audit-pipeline>)
    * [Контентный пайплайн](<#content-pipeline>)
  * [Краткий справочник](<#quick-reference>)
    * [Синтаксис расписания Cron](<#cron-schedule-syntax>)
    * [Цели доставки](<#delivery-targets>)
    * [Переменные шаблонов вебхуков](<#webhook-template-variables>)
    * [Шаблон [SILENT]](<#the-silent-pattern>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/automation-templates -->
