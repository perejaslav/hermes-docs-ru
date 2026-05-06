На этой странице
Жизненный цикл PR в GitHub: ветка, коммит, открытие, CI, слияние.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/github/github-pr-workflow` |
|Версия| `1.1.0` |
|Автор| Hermes Agent |
|Лицензия| MIT |
|Теги| `GitHub`, `Pull-Requests`, `CI/CD`, `Git`, `Automation`, `Merge` |
|Связанные навыки| [`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>), [`github-code-review`](</docs/user-guide/skills/bundled/github/github-github-code-review>) |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает, когда этот навык активируется. Это то, что агент видит как инструкции, когда навык активен.

# Рабочий процесс pull request в GitHub

Полное руководство по управлению жизненным циклом PR. В каждом разделе сначала показан способ через `gh`, затем запасной вариант через `git` + `curl` для машин без `gh`.

## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")

  * Аутентификация в GitHub (см. навык `github-auth`)
  * Нахождение внутри git-репозитория с удалённым репозиторием на GitHub

### Быстрое определение способа аутентификации[​](<#quick-auth-detection> "Прямая ссылка на Быстрое определение способа аутентификации")

[code] 
    # Determine which method to use throughout this workflow  
    if command -v gh &>/dev/null && gh auth status &>/dev/null; then  
      AUTH="gh"  
    else  
      AUTH="git"  
      # Ensure we have a token for API calls  
      if [ -z "$GITHUB_TOKEN" ]; then  
        if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then  
          GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\\n\\r')  
        elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then  
          GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\\([^@]*\\)@.*|\\1|')  
        fi  
      fi  
    fi  
    echo "Using: $AUTH"  
    
[/code]

### Извлечение владельца/репозитория из git-удалёнки[​](<#extracting-ownerrepo-from-the-git-remote> "Прямая ссылка на Извлечение владельца/репозитория из git-удалёнки")

Многим командам `curl` требуется `owner/repo`. Извлеките его из git-удалёнки:

[code] 
    # Works for both HTTPS and SSH remote URLs  
    REMOTE_URL=$(git remote get-url origin)  
    OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\\.com[:/]||; s|\\.git$||')  
    OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)  
    REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)  
    echo "Owner: $OWNER, Repo: $REPO"  
    
[/code]

* * *

## 1\. Создание ветки[​](<#1-branch-creation> "Прямая ссылка на 1. Создание ветки")

Эта часть — чистый `git` — одинакова в обоих случаях:

[code] 
    # Make sure you're up to date  
    git fetch origin  
    git checkout main && git pull origin main  
      
    # Create and switch to a new branch  
    git checkout -b feat/add-user-authentication  
    
[/code]

Соглашения об именовании веток:

  * `feat/описание` — новые функции
  * `fix/описание` — исправления ошибок
  * `refactor/описание` — реструктуризация кода
  * `docs/описание` — документация
  * `ci/описание` — изменения в CI/CD

## 2\. Создание коммитов[​](<#2-making-commits> "Прямая ссылка на 2. Создание коммитов")

Используйте файловые инструменты агента (`write_file`, `patch`) для внесения изменений, затем создайте коммит:

[code] 
    # Stage specific files  
    git add src/auth.py src/models/user.py tests/test_auth.py  
      
    # Commit with a conventional commit message  
    git commit -m "feat: add JWT-based user authentication  
      
    - Add login/register endpoints  
    - Add User model with password hashing  
    - Add auth middleware for protected routes  
    - Add unit tests for auth flow"  
    
[/code]

Формат сообщения коммита (Conventional Commits):

[code] 
    type(scope): short description  
      
    Longer explanation if needed. Wrap at 72 characters.  
    
[/code]

Типы: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

## 3\. Отправка и создание PR[​](<#3-pushing-and-creating-a-pr> "Прямая ссылка на 3. Отправка и создание PR")

### Отправка ветки (одинаково в обоих случаях)[​](<#push-the-branch-same-either-way> "Прямая ссылка на Отправка ветки (одинаково в обоих случаях)")

[code] 
    git push -u origin HEAD  
    
[/code]

### Создание PR[​](<#create-the-pr> "Прямая ссылка на Создание PR")

**С помощью gh:**

[code] 
    gh pr create \\  
      --title "feat: add JWT-based user authentication" \\  
      --body "## Summary  
    - Adds login and register API endpoints  
    - JWT token generation and validation  
      
    ## Test Plan  
    - [ ] Unit tests pass  
      
    Closes #42"  
    
[/code]

Опции: `--draft`, `--reviewer user1,user2`, `--label "enhancement"`, `--base develop`

**С помощью git + curl:**

[code] 
    BRANCH=$(git branch --show-current)  
      
    curl -s -X POST \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      -H "Accept: application/vnd.github.v3+json" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls \\  
      -d "{  
        \\\"title\\\": \\\"feat: add JWT-based user authentication\\\",  
        \\\"body\\\": \\\"## Summary\\nAdds login and register API endpoints.\\n\\nCloses #42\\\",  
        \\\"head\\\": \\\"$BRANCH\\\",  
        \\\"base\\\": \\\"main\\\"  
      }"  
    
[/code]

Ответ JSON содержит `number` PR — сохраните его для последующих команд.
Чтобы создать черновик, добавьте `"draft": true` в тело JSON.

## 4\. Мониторинг статуса CI[​](<#4-monitoring-ci-status> "Прямая ссылка на 4. Мониторинг статуса CI")

### Проверка статуса CI[​](<#check-ci-status> "Прямая ссылка на Проверка статуса CI")

**С помощью gh:**

[code] 
    # One-shot check  
    gh pr checks  
      
    # Watch until all checks finish (polls every 10s)  
    gh pr checks --watch  
    
[/code]

**С помощью git + curl:**

[code] 
    # Get the latest commit SHA on the current branch  
    SHA=$(git rev-parse HEAD)  
      
    # Query the combined status  
    curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \\  
      | python3 -c "  
    import sys, json  
    data = json.load(sys.stdin)  
    print(f\\\"Overall: {data['state']}\\\")  
    for s in data.get('statuses', []):  
        print(f\\\"  {s['context']}: {s['state']} - {s.get('description', '')}\\\")"  
      
    # Also check GitHub Actions check runs (separate endpoint)  
    curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \\  
      | python3 -c "  
    import sys, json  
    data = json.load(sys.stdin)  
    for cr in data.get('check_runs', []):  
        print(f\\\"  {cr['name']}: {cr['status']} / {cr['conclusion'] or 'pending'}\\\")"  
    
[/code]

### Ожидание завершения (git + curl)[​](<#poll-until-complete-git--curl> "Прямая ссылка на Ожидание завершения (git + curl)")

[code] 
    # Simple polling loop — check every 30 seconds, up to 10 minutes  
    SHA=$(git rev-parse HEAD)  
    for i in $(seq 1 20); do  
      STATUS=$(curl -s \\  
        -H "Authorization: token $GITHUB_TOKEN" \\  
        https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \\  
        | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")  
      echo "Check $i: $STATUS"  
      if [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] || [ "$STATUS" = "error" ]; then  
        break  
      fi  
      sleep 30  
    done  
    
[/code]

## 5\. Автоисправление ошибок CI[​](<#5-auto-fixing-ci-failures> "Прямая ссылка на 5. Автоисправление ошибок CI")

Когда CI падает, диагностируйте и исправляйте. Этот цикл работает с любым способом аутентификации.

### Шаг 1: Получение информации об ошибке[​](<#step-1-get-failure-details> "Прямая ссылка на Шаг 1: Получение информации об ошибке")

**С помощью gh:**

[code] 
    # List recent workflow runs on this branch  
    gh run list --branch $(git branch --show-current) --limit 5  
      
    # View failed logs  
    gh run view <RUN_ID> --log-failed  
    
[/code]

**С помощью git + curl:**

[code] 
    BRANCH=$(git branch --show-current)  
      
    # List workflow runs on this branch  
    curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" \\  
      | python3 -c "  
    import sys, json  
    runs = json.load(sys.stdin)['workflow_runs']  
    for r in runs:  
        print(f\\\"Run {r['id']}: {r['name']} - {r['conclusion'] or r['status']}\\\")"  
      
    # Get failed job logs (download as zip, extract, read)  
    RUN_ID=<run_id>  
    curl -s -L \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \\  
      -o /tmp/ci-logs.zip  
    cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt  
    
[/code]

### Шаг 2: Исправление и отправка[​](<#step-2-fix-and-push> "Прямая ссылка на Шаг 2: Исправление и отправка")

После выявления проблемы используйте файловые инструменты (`patch`, `write_file`) для её исправления:

[code] 
    git add <fixed_files>  
    git commit -m "fix: resolve CI failure in <check_name>"  
    git push  
    
[/code]

### Шаг 3: Проверка[​](<#step-3-verify> "Прямая ссылка на Шаг 3: Проверка")

Повторно проверьте статус CI, используя команды из раздела 4 выше.

### Шаблон цикла автоисправления[​](<#auto-fix-loop-pattern> "Прямая ссылка на Шаблон цикла автоисправления")

Если вас попросили автоматически исправить CI, следуйте этому циклу:

  1. Проверить статус CI → выявить ошибки
  2. Прочитать логи ошибок → понять проблему
  3. Использовать `read_file` + `patch`/`write_file` → исправить код
  4. `git add . && git commit -m "fix: ..." && git push`
  5. Дождаться CI → повторно проверить статус
  6. Повторить, если всё ещё падает (до 3 попыток, затем спросить пользователя)

## 6\. Слияние[​](<#6-merging> "Прямая ссылка на 6. Слияние")

**С помощью gh:**

[code] 
    # Squash merge + delete branch (cleanest for feature branches)  
    gh pr merge --squash --delete-branch  
      
    # Enable auto-merge (merges when all checks pass)  
    gh pr merge --auto --squash --delete-branch  
    
[/code]

**С помощью git + curl:**

[code] 
    PR_NUMBER=<number>  
      
    # Merge the PR via API (squash)  
    curl -s -X PUT \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \\  
      -d "{  
        \\\"merge_method\\\": \\\"squash\\\",  
        \\\"commit_title\\\": \\\"feat: add user authentication (#$PR_NUMBER)\\\"  
      }"  
      
    # Delete the remote branch after merge  
    BRANCH=$(git branch --show-current)  
    git push origin --delete $BRANCH  
      
    # Switch back to main locally  
    git checkout main && git pull origin main  
    git branch -d $BRANCH  
    
[/code]

Методы слияния: `"merge"` (коммит слияния), `"squash"`, `"rebase"`

### Включение автослияния (curl)[​](<#enable-auto-merge-curl> "Прямая ссылка на Включение автослияния (curl)")

[code] 
    # Auto-merge requires the repo to have it enabled in settings.  
    # This uses the GraphQL API since REST doesn't support auto-merge.  
    PR_NODE_ID=$(curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \\  
      | python3 -c "import sys,json; print(json.load(sys.stdin)['node_id'])")  
      
    curl -s -X POST \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/graphql \\  
      -d "{\\\"query\\\": \\\"mutation { enablePullRequestAutoMerge(input: {pullRequestId: \\\\\\\"$PR_NODE_ID\\\\\\\", mergeMethod: SQUASH}) { clientMutationId } }\\\"}"  
    
[/code]

## 7\. Полный пример рабочего процесса[​](<#7-complete-workflow-example> "Прямая ссылка на 7. Полный пример рабочего процесса")

[code] 
    # 1. Start from clean main  
    git checkout main && git pull origin main  
      
    # 2. Branch  
    git checkout -b fix/login-redirect-bug  
      
    # 3. (Agent makes code changes with file tools)  
      
    # 4. Commit  
    git add src/auth/login.py tests/test_login.py  
    git commit -m "fix: correct redirect URL after login  
      
    Preserves the ?next= parameter instead of always redirecting to /dashboard."  
      
    # 5. Push  
    git push -u origin HEAD  
      
    # 6. Create PR (picks gh or curl based on what's available)  
    # ... (see Section 3)  
      
    # 7. Monitor CI (see Section 4)  
      
    # 8. Merge when green (see Section 6)  
    
[/code]

## Справочник полезных команд PR[​](<#useful-pr-commands-reference> "Прямая ссылка на Справочник полезных команд PR")

| Действие | gh | git + curl |
|---|---|---|
|Список моих PR| `gh pr list --author @me`| `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"` |
|Просмотр diff PR| `gh pr diff`| `git diff main...HEAD` (локально) или `curl -H "Accept: application/vnd.github.diff" ...` |
|Добавить комментарий| `gh pr comment N --body "..."`| `curl -X POST .../issues/N/comments -d '{"body":"..."}'` |
|Запросить ревью| `gh pr edit N --add-reviewer user`| `curl -X POST .../pulls/N/requested_reviewers -d '{"reviewers":["user"]}'` |
|Закрыть PR| `gh pr close N`| `curl -X PATCH .../pulls/N -d '{"state":"closed"}'` |
|Посмотреть чужой PR| `gh pr checkout N`| `git fetch origin pull/N/head:pr-N && git checkout pr-N` |

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
    * [Быстрое определение способа аутентификации](<#quick-auth-detection>)
    * [Извлечение владельца/репозитория из git-удалёнки](<#extracting-ownerrepo-from-the-git-remote>)
  * [1\. Создание ветки](<#1-branch-creation>)
  * [2\. Создание коммитов](<#2-making-commits>)
  * [3\. Отправка и создание PR](<#3-pushing-and-creating-a-pr>)
    * [Отправка ветки (одинаково в обоих случаях)](<#push-the-branch-same-either-way>)
    * [Создание PR](<#create-the-pr>)
  * [4\. Мониторинг статуса CI](<#4-monitoring-ci-status>)
    * [Проверка статуса CI](<#check-ci-status>)
    * [Ожидание завершения (git + curl)](<#poll-until-complete-git--curl>)
  * [5\. Автоисправление ошибок CI](<#5-auto-fixing-ci-failures>)
    * [Шаг 1: Получение информации об ошибке](<#step-1-get-failure-details>)
    * [Шаг 2: Исправление и отправка](<#step-2-fix-and-push>)
    * [Шаг 3: Проверка](<#step-3-verify>)
    * [Шаблон цикла автоисправления](<#auto-fix-loop-pattern>)
  * [6\. Слияние](<#6-merging>)
    * [Включение автослияния (curl)](<#enable-auto-merge-curl>)
  * [7\. Полный пример рабочего процесса](<#7-complete-workflow-example>)
  * [Справочник полезных команд PR](<#useful-pr-commands-reference>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-pr-workflow -->
