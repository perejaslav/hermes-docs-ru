On this page
Создание, триаж, маркировка и назначение задач GitHub через gh или REST.
## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Источник| Встроенный (установлен по умолчанию)  |
|Путь| `skills/github/github-issues`  |
|Версия| `1.1.0`  |
|Автор| Hermes Agent  |
|Лицензия| MIT  |
|Теги| `GitHub`, `Issues`, `Project-Management`, `Bug-Tracking`, `Triage`  |
|Связанные навыки| [`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>), [`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# Управление задачами GitHub
Создание, поиск, триаж и управление задачами GitHub. В каждом разделе сначала показана команда `gh`, затем запасной вариант с `curl`.
## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")
  * Аутентификация в GitHub (см. навык `github-auth`)
  * Нахождение внутри git-репозитория с GitHub-удалённым репозиторием или явное указание репозитория


### Настройка[​](<#setup> "Direct link to Setup")
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
## 1\\. Просмотр задач[​](<#1-viewing-issues> "Direct link to 1. Viewing Issues")
**С помощью gh:**
[code] 
    gh issue list  
    gh issue list --state open --label "bug"  
    gh issue list --assignee @me  
    gh issue list --search "authentication error" --state all  
    gh issue view 42  
    
[/code]
**С помощью curl:**
[code] 
    # Список открытых задач  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin):  
        if 'pull_request' not in i:  # GitHub API также возвращает PR в /issues  
            labels = ', '.join(l['name'] for l in i['labels'])  
            print(f\\\"#{i['number']:5}  {i['state']:6}  {labels:30}  {i['title']}\\\")"  
      
    # Фильтр по метке  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&labels=bug&per_page=20" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin):  
        if 'pull_request' not in i:  
            print(f\\\"#{i['number']}  {i['title']}\\\")"  
      
    # Просмотр конкретной задачи  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42 \  
      | python3 -c "  
    import sys, json  
    i = json.load(sys.stdin)  
    labels = ', '.join(l['name'] for l in i['labels'])  
    assignees = ', '.join(a['login'] for a in i['assignees'])  
    print(f\\\"#{i['number']}: {i['title']}\\\")  
    print(f\\\"State: {i['state']}  Labels: {labels}  Assignees: {assignees}\\\")  
    print(f\\\"Author: {i['user']['login']}  Created: {i['created_at']}\\\")  
    print(f\\\"\\n{i['body']}\\\")"  
      
    # Поиск задач  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/search/issues?q=authentication+error+repo:$OWNER/$REPO" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin)['items']:  
        print(f\\\"#{i['number']}  {i['state']:6}  {i['title']}\\\")"  
    
[/code]
## 2\\. Создание задач[​](<#2-creating-issues> "Direct link to 2. Creating Issues")
**С помощью gh:**
[code] 
    gh issue create \  
      --title \"Login redirect ignores ?next= parameter\" \  
      --body \"## Description  
    After logging in, users always land on /dashboard.  
      
    ## Steps to Reproduce  
    1. Navigate to /settings while logged out  
    2. Get redirected to /login?next=/settings  
    3. Log in  
    4. Actual: redirected to /dashboard (should go to /settings)  
      
    ## Expected Behavior  
    Respect the ?next= query parameter.\" \  
      --label \"bug,backend\" \  
      --assignee \"username\"  
    
[/code]
**С помощью curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues \  
      -d '{  
        \"title\": \"Login redirect ignores ?next= parameter\",  
        \"body\": \"## Description\\nAfter logging in, users always land on /dashboard.\\n\\n## Steps to Reproduce\\n1. Navigate to /settings while logged out\\n2. Get redirected to /login?next=/settings\\n3. Log in\\n4. Actual: redirected to /dashboard\\n\\n## Expected Behavior\\nRespect the ?next= query parameter.\",  
        \"labels\": [\"bug\", \"backend\"],  
        \"assignees\": [\"username\"]  
      }'  
    
[/code]
### Шаблон отчёта об ошибке[​](<#bug-report-template> "Direct link to Bug Report Template")
[code] 
    ## Bug Description  
    <Что происходит>  
      
    ## Steps to Reproduce  
    1. <шаг>  
    2. <шаг>  
      
    ## Expected Behavior  
    <Что должно произойти>  
      
    ## Actual Behavior  
    <Что происходит на самом деле>  
      
    ## Environment  
    - OS: <ОС>  
    - Version: <версия>  
    
[/code]
### Шаблон запроса функции[​](<#feature-request-template> "Direct link to Feature Request Template")
[code] 
    ## Feature Description  
    <Что вы хотите>  
      
    ## Motivation  
    <Почему это было бы полезно>  
      
    ## Proposed Solution  
    <Как это может работать>  
      
    ## Alternatives Considered  
    <Другие подходы>  
    
[/code]
## 3\\. Управление задачами[​](<#3-managing-issues> "Direct link to 3. Managing Issues")
### Добавление/удаление меток[​](<#addremove-labels> "Direct link to Add/Remove Labels")
**С помощью gh:**
[code] 
    gh issue edit 42 --add-label \"priority:high,bug\"  
    gh issue edit 42 --remove-label \"needs-triage\"  
    
[/code]
**С помощью curl:**
[code] 
    # Добавить метки  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \  
      -d '{\"labels\": [\"priority:high\", \"bug\"]}'  
      
    # Удалить метку  
    curl -s -X DELETE \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/labels/needs-triage  
      
    # Список доступных меток в репозитории  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/labels \  
      | python3 -c "  
    import sys, json  
    for l in json.load(sys.stdin):  
        print(f\\\"  {l['name']:30}  {l.get('description', '')}\\\")"  
    
[/code]
### Назначение[​](<#assignment> "Direct link to Assignment")
**С помощью gh:**
[code] 
    gh issue edit 42 --add-assignee username  
    gh issue edit 42 --add-assignee @me  
    
[/code]
**С помощью curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/assignees \  
      -d '{\"assignees\": [\"username\"]}'  
    
[/code]
### Комментирование[​](<#commenting> "Direct link to Commenting")
**С помощью gh:**
[code] 
    gh issue comment 42 --body \"Investigated — root cause is in auth middleware. Working on a fix.\"  
    
[/code]
**С помощью curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/comments \  
      -d '{\"body\": \"Investigated — root cause is in auth middleware. Working on a fix.\"}'  
    
[/code]
### Закрытие и повторное открытие[​](<#closing-and-reopening> "Direct link to Closing and Reopening")
**С помощью gh:**
[code] 
    gh issue close 42  
    gh issue close 42 --reason \"not planned\"  
    gh issue reopen 42  
    
[/code]
**С помощью curl:**
[code] 
    # Закрыть  
    curl -s -X PATCH \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42 \  
      -d '{\"state\": \"closed\", \"state_reason\": \"completed\"}'  
      
    # Открыть заново  
    curl -s -X PATCH \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42 \  
      -d '{\"state\": \"open\"}'  
    
[/code]
### Привязка задач к PR[​](<#linking-issues-to-prs> "Direct link to Linking Issues to PRs")
Задачи автоматически закрываются, когда PR сливается с соответствующими ключевыми словами в теле:
[code] 
    Closes #42  
    Fixes #42  
    Resolves #42  
    
[/code]
Чтобы создать ветку из задачи:
**С помощью gh:**
[code] 
    gh issue develop 42 --checkout  
    
[/code]
**С помощью git (ручной эквивалент):**
[code] 
    git checkout main && git pull origin main  
    git checkout -b fix/issue-42-login-redirect  
    
[/code]
## 4\\. Рабочий процесс триажа задач[​](<#4-issue-triage-workflow> "Direct link to 4. Issue Triage Workflow")
Когда требуется провести триаж задач:
  1. **Список нетриаженных задач:**
  

[code] 
    # С помощью gh  
    gh issue list --label \"needs-triage\" --state open  
      
    # С помощью curl  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      \"https://api.github.com/repos/$OWNER/$REPO/issues?labels=needs-triage&state=open\" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin):  
        if 'pull_request' not in i:  
            print(f\\\"#{i['number']}  {i['title']}\\\")"  
    
[/code]
  2. **Прочитайте и классифицируйте** каждую задачу (просмотрите детали, поймите, ошибка это или функция)
  3. **Примените метки и приоритет** (см. «Управление задачами» выше)
  4. **Назначьте**, если ответственный известен
  5. **Оставьте комментарий с заметками по триажу** при необходимости


## 5\\. Массовые операции[​](<#5-bulk-operations> "Direct link to 5. Bulk Operations")
Для пакетных операций комбинируйте вызовы API с shell-скриптингом:
**С помощью gh:**
[code] 
    # Закрыть все задачи с определённой меткой  
    gh issue list --label \"wontfix\" --json number --jq '.[].number' | \  
      xargs -I {} gh issue close {} --reason \"not planned\"  
    
[/code]
**С помощью curl:**
[code] 
    # Получить номера задач с меткой, затем закрыть каждую  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      \"https://api.github.com/repos/$OWNER/$REPO/issues?labels=wontfix&state=open\" \  
      | python3 -c \"import sys,json; [print(i['number']) for i in json.load(sys.stdin)]\" \  
      | while read num; do  
        curl -s -X PATCH \  
          -H "Authorization: token $GITHUB_TOKEN" \  
          https://api.github.com/repos/$OWNER/$REPO/issues/$num \  
          -d '{\"state\": \"closed\", \"state_reason\": \"not_planned\"}'  
        echo \"Closed #$num\"  
      done  
    
[/code]
## Таблица быстрого доступа[​](<#quick-reference-table> "Direct link to Quick Reference Table")
|Действие| gh| curl endpoint  |
|---|---|---|
|Список задач| `gh issue list`| `GET /repos/{o}/{r}/issues`  |
|Просмотр задачи| `gh issue view N`| `GET /repos/{o}/{r}/issues/N`  |
|Создание задачи| `gh issue create ...`| `POST /repos/{o}/{r}/issues`  |
|Добавление меток| `gh issue edit N --add-label ...`| `POST /repos/{o}/{r}/issues/N/labels`  |
|Назначение| `gh issue edit N --add-assignee ...`| `POST /repos/{o}/{r}/issues/N/assignees`  |
|Комментарий| `gh issue comment N --body ...`| `POST /repos/{o}/{r}/issues/N/comments`  |
|Закрытие| `gh issue close N`| `PATCH /repos/{o}/{r}/issues/N`  |
|Поиск| `gh issue list --search \"...\"`| `GET /search/issues?q=...`  |
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
    * [Настройка](<#setup>)
  * [1\\. Просмотр задач](<#1-viewing-issues>)
  * [2\\. Создание задач](<#2-creating-issues>)
    * [Шаблон отчёта об ошибке](<#bug-report-template>)
    * [Шаблон запроса функции](<#feature-request-template>)
  * [3\\. Управление задачами](<#3-managing-issues>)
    * [Добавление/удаление меток](<#addremove-labels>)
    * [Назначение](<#assignment>)
    * [Комментирование](<#commenting>)
    * [Закрытие и повторное открытие](<#closing-and-reopening>)
    * [Привязка задач к PR](<#linking-issues-to-prs>)
  * [4\\. Рабочий процесс триажа задач](<#4-issue-triage-workflow>)
  * [5\\. Массовые операции](<#5-bulk-operations>)
  * [Таблица быстрого доступа](<#quick-reference-table>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-issues -->
