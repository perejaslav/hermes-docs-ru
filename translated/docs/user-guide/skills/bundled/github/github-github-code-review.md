On this page
Обзор PR: диффы, инлайн-комментарии через gh или REST.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default)  |
|Path| `skills/github/github-code-review`  |
|Version| `1.1.0`  |
|Author| Hermes Agent  |
|License| MIT  |
|Tags| `GitHub`, `Code-Review`, `Pull-Requests`, `Git`, `Quality`  |
|Related skills| [`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>), [`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# GitHub Code Review
Выполняйте ревью кода локальных изменений перед отправкой (push) или ревью открытых PR на GitHub. Большая часть этого навыка использует обычный `git` — разделение `gh`/`curl` имеет значение только для взаимодействия на уровне PR.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * Аутентификация на GitHub (см. навык `github-auth`)
  * Нахождение внутри git-репозитория


### Setup (for PR interactions)[​](<#setup-for-pr-interactions> "Direct link to Setup (for PR interactions)")
[code] 
    if command -v gh &>/dev/null && gh auth status &>/dev/null; then  
      AUTH="gh"  
    else  
      AUTH="git"  
      if [ -z "$GITHUB_TOKEN" ]; then  
        if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then  
          GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\\n\\r')  
        elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then  
          GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\\([^@]*\\)@.*|\\1|')  
        fi  
      fi  
    fi  
      
    REMOTE_URL=$(git remote get-url origin)  
    OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\\.com[:/]||; s|\\.git$||')  
    OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)  
    REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)  
    
[/code]
* * *
## 1\. Reviewing Local Changes (Pre-Push)[​](<#1-reviewing-local-changes-pre-push> "Direct link to 1. Reviewing Local Changes (Pre-Push)")
Это чистый `git` — работает везде, API не требуется.
### Get the Diff[​](<#get-the-diff> "Direct link to Get the Diff")
[code] 
    # Staged changes (what would be committed)  
    git diff --staged  
      
    # All changes vs main (what a PR would contain)  
    git diff main...HEAD  
      
    # File names only  
    git diff main...HEAD --name-only  
      
    # Stat summary (insertions/deletions per file)  
    git diff main...HEAD --stat  
    
[/code]
### Review Strategy[​](<#review-strategy> "Direct link to Review Strategy")
  1. **Сначала получите общую картину:**


[code] 
    git diff main...HEAD --stat  
    git log main..HEAD --oneline  
    
[/code]
  2. **Ревью файл за файлом** — используйте `read_file` для изменённых файлов, чтобы получить полный контекст, и дифф, чтобы увидеть, что именно изменилось:


[code] 
    git diff main...HEAD -- src/auth/login.py  
    
[/code]
  3. **Проверьте на типичные проблемы:**


[code] 
    # Debug statements, TODOs, console.logs left behind  
    git diff main...HEAD | grep -n "print(\\|console\\.log\\|TODO\\|FIXME\\|HACK\\|XXX\\|debugger"  
      
    # Large files accidentally staged  
    git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -10  
      
    # Secrets or credential patterns  
    git diff main...HEAD | grep -in "password\\|secret\\|api_key\\|token.*=\\|private_key"  
      
    # Merge conflict markers  
    git diff main...HEAD | grep -n "<<<<<<\\|>>>>>>\\|======="  
    
[/code]
  4. **Представьте структурированную обратную связь** пользователю.


### Review Output Format[​](<#review-output-format> "Direct link to Review Output Format")
При ревью локальных изменений представляйте результаты в следующей структуре:
[code] 
    ## Code Review Summary  
      
    ### Critical  
    - **src/auth.py:45** — SQL injection: user input passed directly to query.  
      Suggestion: Use parameterized queries.  
      
    ### Warnings  
    - **src/models/user.py:23** — Password stored in plaintext. Use bcrypt or argon2.  
    - **src/api/routes.py:112** — No rate limiting on login endpoint.  
      
    ### Suggestions  
    - **src/utils/helpers.py:8** — Duplicates logic in `src/core/utils.py:34`. Consolidate.  
    - **tests/test_auth.py** — Missing edge case: expired token test.  
      
    ### Looks Good  
    - Clean separation of concerns in the middleware layer  
    - Good test coverage for the happy path  
    
[/code]
* * *
## 2\. Reviewing a Pull Request on GitHub[​](<#2-reviewing-a-pull-request-on-github> "Direct link to 2. Reviewing a Pull Request on GitHub")
### View PR Details[​](<#view-pr-details> "Direct link to View PR Details")
**С помощью gh:**
[code] 
    gh pr view 123  
    gh pr diff 123  
    gh pr diff 123 --name-only  
    
[/code]
**С помощью git + curl:**
[code] 
    PR_NUMBER=123  
      
    # Get PR details  
    curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \\  
      | python3 -c "  
    import sys, json  
    pr = json.load(sys.stdin)  
    print(f\\\"Title: {pr['title']}\\\")  
    print(f\\\"Author: {pr['user']['login']}\\\")  
    print(f\\\"Branch: {pr['head']['ref']} -> {pr['base']['ref']}\\\")  
    print(f\\\"State: {pr['state']}\\\")  
    print(f\\\"Body:\\n{pr['body']}\\\")"  
      
    # List changed files  
    curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/files \\  
      | python3 -c "  
    import sys, json  
    for f in json.load(sys.stdin):  
        print(f\\\"{f['status']:10} +{f['additions']:-4} -{f['deletions']:-4}  {f['filename']}\\\")"  
    
[/code]
### Check Out PR Locally for Full Review[​](<#check-out-pr-locally-for-full-review> "Direct link to Check Out PR Locally for Full Review")
Это работает с обычным `git` — `gh` не требуется:
[code] 
    # Fetch the PR branch and check it out  
    git fetch origin pull/123/head:pr-123  
    git checkout pr-123  
      
    # Now you can use read_file, search_files, run tests, etc.  
      
    # View diff against the base branch  
    git diff main...pr-123  
    
[/code]
**С помощью gh (сокращение):**
[code] 
    gh pr checkout 123  
    
[/code]
### Leave Comments on a PR[​](<#leave-comments-on-a-pr> "Direct link to Leave Comments on a PR")
**Общий комментарий к PR — с помощью gh:**
[code] 
    gh pr comment 123 --body "Overall looks good, a few suggestions below."  
    
[/code]
**Общий комментарий к PR — с помощью curl:**
[code] 
    curl -s -X POST \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/issues/$PR_NUMBER/comments \\  
      -d '{"body": "Overall looks good, a few suggestions below."}'  
    
[/code]
### Leave Inline Review Comments[​](<#leave-inline-review-comments> "Direct link to Leave Inline Review Comments")
**Одиночный инлайн-комментарий — с помощью gh (через API):**
[code] 
    HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')  
      
    gh api repos/$OWNER/$REPO/pulls/123/comments \\  
      --method POST \\  
      -f body="This could be simplified with a list comprehension." \\  
      -f path="src/auth/login.py" \\  
      -f commit_id="$HEAD_SHA" \\  
      -f line=45 \\  
      -f side="RIGHT"  
    
[/code]
**Одиночный инлайн-комментарий — с помощью curl:**
[code] 
    # Get the head commit SHA  
    HEAD_SHA=$(curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \\  
      | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")  
      
    curl -s -X POST \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments \\  
      -d "{  
        \\\"body\\\": \\\"This could be simplified with a list comprehension.\\\",  
        \\\"path\\\": \\\"src/auth/login.py\\\",  
        \\\"commit_id\\\": \\\"$HEAD_SHA\\\",  
        \\\"line\\\": 45,  
        \\\"side\\\": \\\"RIGHT\\\"  
      }"  
    
[/code]
### Submit a Formal Review (Approve / Request Changes)[​](<#submit-a-formal-review-approve--request-changes> "Direct link to Submit a Formal Review (Approve / Request Changes)")
**С помощью gh:**
[code] 
    gh pr review 123 --approve --body "LGTM!"  
    gh pr review 123 --request-changes --body "See inline comments."  
    gh pr review 123 --comment --body "Some suggestions, nothing blocking."  
    
[/code]
**С помощью curl — атомарная отправка многокомментарного ревью:**
[code] 
    HEAD_SHA=$(curl -s \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \\  
      | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")  
      
    curl -s -X POST \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/reviews \\  
      -d "{  
        \\\"commit_id\\\": \\\"$HEAD_SHA\\\",  
        \\\"event\\\": \\\"COMMENT\\\",  
        \\\"body\\\": \\\"Code review from Hermes Agent\\\",  
        \\\"comments\\\": [  
          {\\\"path\\\": \\\"src/auth.py\\\", \\\"line\\\": 45, \\\"body\\\": \\\"Use parameterized queries to prevent SQL injection.\\\"},  
          {\\\"path\\\": \\\"src/models/user.py\\\", \\\"line\\\": 23, \\\"body\\\": \\\"Hash passwords with bcrypt before storing.\\\"},  
          {\\\"path\\\": \\\"tests/test_auth.py\\\", \\\"line\\\": 1, \\\"body\\\": \\\"Add test for expired token edge case.\\\"}  
        ]  
      }"  
    
[/code]
Event values: `"APPROVE"`, `"REQUEST_CHANGES"`, `"COMMENT"`
The `line` field refers to the line number in the _new_ version of the file. For deleted lines, use `"side": "LEFT"`.
* * *
## 3\. Review Checklist[​](<#3-review-checklist> "Direct link to 3. Review Checklist")
При выполнении ревью кода (локального или PR) систематически проверяйте:
### Correctness[​](<#correctness> "Direct link to Correctness")
  * Соответствует ли код заявленному поведению?
  * Обработаны ли граничные случаи (пустые входные данные, null, большие объёмы данных, конкурентный доступ)?
  * Корректно ли обрабатываются пути ошибок?


### Security[​](<#security> "Direct link to Security")
  * Нет жёстко закодированных секретов, учётных данных или API-ключей
  * Валидация входных данных от пользователя
  * Нет SQL-инъекций, XSS или path traversal
  * Проверки аутентификации/авторизации там, где необходимо


### Code Quality[​](<#code-quality> "Direct link to Code Quality")
  * Понятные имена (переменные, функции, классы)
  * Нет излишней сложности или преждевременной абстракции
  * DRY — нет дублированной логики, которую можно вынести
  * Функции сфокусированы (единственная ответственность)


### Testing[​](<#testing> "Direct link to Testing")
  * Протестированы ли новые участки кода?
  * Покрыты ли сценарий happy path и случаи ошибок?
  * Читаемы ли и поддерживаемы ли тесты?


### Performance[​](<#performance> "Direct link to Performance")
  * Нет N+1 запросов или излишних циклов
  * Используется соответствующее кэширование, где это полезно
  * Нет блокирующих операций в асинхронных участках кода


### Documentation[​](<#documentation> "Direct link to Documentation")
  * Документированы публичные API
  * Неочевидная логика содержит комментарии, объясняющие «почему»
  * README обновлён, если изменилось поведение


* * *
## 4\. Pre-Push Review Workflow[​](<#4-pre-push-review-workflow> "Direct link to 4. Pre-Push Review Workflow")
Когда пользователь просит вас «проверить код» или «проверить перед отправкой»:
  1. `git diff main...HEAD --stat` — оцените объём изменений
  2. `git diff main...HEAD` — прочитайте полный дифф
  3. Для каждого изменённого файла используйте `read_file`, если нужен дополнительный контекст
  4. Примените чеклист выше
  5. Представьте результаты в структурированном формате (Critical / Warnings / Suggestions / Looks Good)
  6. Если найдены критические проблемы, предложите исправить их перед отправкой


* * *
## 5\. PR Review Workflow (End-to-End)[​](<#5-pr-review-workflow-end-to-end> "Direct link to 5. PR Review Workflow (End-to-End)")
Когда пользователь просит вас «проверить PR #N», «посмотреть на этот PR» или даёт URL PR, следуйте этому рецепту:
### Step 1: Set up environment[​](<#step-1-set-up-environment> "Direct link to Step 1: Set up environment")
[code] 
    source "${HERMES_HOME:-$HOME/.hermes}/skills/github/github-auth/scripts/gh-env.sh"  
    # Or run the inline setup block from the top of this skill  
    
[/code]
### Step 2: Gather PR context[​](<#step-2-gather-pr-context> "Direct link to Step 2: Gather PR context")
Получите метаданные PR, описание и список изменённых файлов, чтобы понять масштаб перед погружением в код.
**С помощью gh:**
[code] 
    gh pr view 123  
    gh pr diff 123 --name-only  
    gh pr checks 123  
    
[/code]
**С помощью curl:**
[code] 
    PR_NUMBER=123  
      
    # PR details (title, author, description, branch)  
    curl -s -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER  
      
    # Changed files with line counts  
    curl -s -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/files  
    
[/code]
### Step 3: Check out the PR locally[​](<#step-3-check-out-the-pr-locally> "Direct link to Step 3: Check out the PR locally")
Это даёт вам полный доступ к `read_file`, `search_files` и возможность запускать тесты.
[code] 
    git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER  
    git checkout pr-$PR_NUMBER  
    
[/code]
### Step 4: Read the diff and understand changes[​](<#step-4-read-the-diff-and-understand-changes> "Direct link to Step 4: Read the diff and understand changes")
[code] 
    # Full diff against the base branch  
    git diff main...HEAD  
      
    # Or file-by-file for large PRs  
    git diff main...HEAD --name-only  
    # Then for each file:  
    git diff main...HEAD -- path/to/file.py  
    
[/code]
Для каждого изменённого файла используйте `read_file`, чтобы увидеть полный контекст изменений — одних диффов может быть недостаточно, чтобы заметить проблемы, видимые только в окружающем коде.
### Step 5: Run automated checks locally (if applicable)[​](<#step-5-run-automated-checks-locally-if-applicable> "Direct link to Step 5: Run automated checks locally (if applicable)")
[code] 
    # Run tests if there's a test suite  
    python -m pytest 2>&1 | tail -20  
    # or: npm test, cargo test, go test ./..., etc.  
      
    # Run linter if configured  
    ruff check . 2>&1 | head -30  
    # or: eslint, clippy, etc.  
    
[/code]
### Step 6: Apply the review checklist (Section 3)[​](<#step-6-apply-the-review-checklist-section-3> "Direct link to Step 6: Apply the review checklist (Section 3)")
Пройдитесь по каждой категории: Correctness, Security, Code Quality, Testing, Performance, Documentation.
### Step 7: Post the review to GitHub[​](<#step-7-post-the-review-to-github> "Direct link to Step 7: Post the review to GitHub")
Соберите свои результаты и отправьте их как формальное ревью с инлайн-комментариями.
**С помощью gh:**
[code] 
    # If no issues — approve  
    gh pr review $PR_NUMBER --approve --body "Reviewed by Hermes Agent. Code looks clean — good test coverage, no security concerns."  
      
    # If issues found — request changes with inline comments  
    gh pr review $PR_NUMBER --request-changes --body "Found a few issues — see inline comments."  
    
[/code]
**С помощью curl — атомарное ревью с несколькими инлайн-комментариями:**
[code] 
    HEAD_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER \\  
      | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")  
      
    # Build the review JSON — event is APPROVE, REQUEST_CHANGES, or COMMENT  
    curl -s -X POST \\  
      -H "Authorization: token $GITHUB_TOKEN" \\  
      https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/reviews \\  
      -d "{  
        \\\"commit_id\\\": \\\"$HEAD_SHA\\\",  
        \\\"event\\\": \\\"REQUEST_CHANGES\\\",  
        \\\"body\\\": \\\"## Hermes Agent Review\\n\\nFound 2 issues, 1 suggestion. See inline comments.\\\",  
        \\\"comments\\\": [  
          {\\\"path\\\": \\\"src/auth.py\\\", \\\"line\\\": 45, \\\"body\\\": \\\"🔴 **Critical:** User input passed directly to SQL query — use parameterized queries.\\\"},  
          {\\\"path\\\": \\\"src/models.py\\\", \\\"line\\\": 23, \\\"body\\\": \\\"⚠️ **Warning:** Password stored without hashing.\\\"},  
          {\\\"path\\\": \\\"src/utils.py\\\", \\\"line\\\": 8, \\\"body\\\": \\\"💡 **Suggestion:** This duplicates logic in core/utils.py:34.\\\"}  
        ]  
      }"  
    
[/code]
### Step 8: Also post a summary comment[​](<#step-8-also-post-a-summary-comment> "Direct link to Step 8: Also post a summary comment")
В дополнение к инлайн-комментариям оставьте сводный комментарий верхнего уровня, чтобы автор PR получил полную картину с первого взгляда. Используйте формат вывода ревью из `references/review-output-template.md`.
**С помощью gh:**
[code] 
    gh pr comment $PR_NUMBER --body "$(cat <<'EOF'  
    ## Code Review Summary  
      
    **Verdict: Changes Requested** (2 issues, 1 suggestion)  
      
    ### 🔴 Critical  
    - **src/auth.py:45** — SQL injection vulnerability  
      
    ### ⚠️ Warnings  
    - **src/models.py:23** — Plaintext password storage  
      
    ### 💡 Suggestions  
    - **src/utils.py:8** — Duplicated logic, consider consolidating  
      
    ### ✅ Looks Good  
    - Clean API design  
    - Good error handling in the middleware layer  
      
    ---  
    *Reviewed by Hermes Agent*  
    EOF  
    )"  
    
[/code]
### Step 9: Clean up[​](<#step-9-clean-up> "Direct link to Step 9: Clean up")
[code] 
    git checkout main  
    git branch -D pr-$PR_NUMBER  
    
[/code]
### Decision: Approve vs Request Changes vs Comment[​](<#decision-approve-vs-request-changes-vs-comment> "Direct link to Decision: Approve vs Request Changes vs Comment")
  * **Approve** — нет критических проблем и предупреждений, только незначительные предложения или всё чисто
  * **Request Changes** — есть критические проблемы или предупреждения, которые следует исправить перед слиянием
  * **Comment** — наблюдения и предложения, но ничего блокирующего (используйте, когда не уверены или PR является черновиком)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
    * [Setup (for PR interactions)](<#setup-for-pr-interactions>)
  * [1\. Reviewing Local Changes (Pre-Push)](<#1-reviewing-local-changes-pre-push>)
    * [Get the Diff](<#get-the-diff>)
    * [Review Strategy](<#review-strategy>)
    * [Review Output Format](<#review-output-format>)
  * [2\. Reviewing a Pull Request on GitHub](<#2-reviewing-a-pull-request-on-github>)
    * [View PR Details](<#view-pr-details>)
    * [Check Out PR Locally for Full Review](<#check-out-pr-locally-for-full-review>)
    * [Leave Comments on a PR](<#leave-comments-on-a-pr>)
    * [Leave Inline Review Comments](<#leave-inline-review-comments>)
    * [Submit a Formal Review (Approve / Request Changes)](<#submit-a-formal-review-approve--request-changes>)
  * [3\. Review Checklist](<#3-review-checklist>)
    * [Correctness](<#correctness>)
    * [Security](<#security>)
    * [Code Quality](<#code-quality>)
    * [Testing](<#testing>)
    * [Performance](<#performance>)
    * [Documentation](<#documentation>)
  * [4\. Pre-Push Review Workflow](<#4-pre-push-review-workflow>)
  * [5\. PR Review Workflow (End-to-End)](<#5-pr-review-workflow-end-to-end>)
    * [Step 1: Set up environment](<#step-1-set-up-environment>)
    * [Step 2: Gather PR context](<#step-2-gather-pr-context>)
    * [Step 3: Check out the PR locally](<#step-3-check-out-the-pr-locally>)
    * [Step 4: Read the diff and understand changes](<#step-4-read-the-diff-and-understand-changes>)
    * [Step 5: Run automated checks locally (if applicable)](<#step-5-run-automated-checks-locally-if-applicable>)
    * [Step 6: Apply the review checklist (Section 3)](<#step-6-apply-the-review-checklist-section-3>)
    * [Step 7: Post the review to GitHub](<#step-7-post-the-review-to-github>)
    * [Step 8: Also post a summary comment](<#step-8-also-post-a-summary-comment>)
    * [Step 9: Clean up](<#step-9-clean-up>)
    * [Decision: Approve vs Request Changes vs Comment](<#decision-approve-vs-request-changes-vs-comment>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-code-review -->
