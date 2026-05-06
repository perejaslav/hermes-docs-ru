На этой странице
Клонирование/создание/форк репозиториев; управление удалёнными репозиториями, релизами.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Встроенный (установлен по умолчанию) |
|Путь| `skills/github/github-repo-management` |
|Версия| `1.1.0` |
|Автор| Hermes Agent |
|Лицензия| MIT |
|Теги| `GitHub`, `Репозитории`, `Git`, `Релизы`, `Секреты`, `Конфигурация` |
|Связанные навыки| [`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>), [`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>), [`github-issues`](</docs/user-guide/skills/bundled/github/github-github-issues>) |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Именно эти инструкции видит агент, когда навык активен.
# Управление репозиториями GitHub
Создание, клонирование, форк, настройка и управление репозиториями GitHub. В каждом разделе сначала показана команда `gh`, затем запасной вариант с `git` + `curl`.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  * Аутентификация в GitHub (см. навык `github-auth`)


### Настройка[​](<#setup> "Прямая ссылка на Настройка")
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
      
    # Get your GitHub username (needed for several operations)  
    if [ "$AUTH" = "gh" ]; then  
      GH_USER=$(gh api user --jq '.login')  
    else  
      GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")  
    fi  
    
[/code]
Если вы уже находитесь внутри репозитория:
[code] 
    REMOTE_URL=$(git remote get-url origin)  
    OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\\.com[:/]||; s|\\.git$||')  
    OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)  
    REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)  
    
[/code]
* * *
## 1\. Клонирование репозиториев[​](<#1-cloning-repositories> "Прямая ссылка на 1. Клонирование репозиториев")
Клонирование — это чистый `git` — работает одинаково в обоих случаях:
[code] 
    # Clone via HTTPS (works with credential helper or token-embedded URL)  
    git clone https://github.com/owner/repo-name.git  
      
    # Clone into a specific directory  
    git clone https://github.com/owner/repo-name.git ./my-local-dir  
      
    # Shallow clone (faster for large repos)  
    git clone --depth 1 https://github.com/owner/repo-name.git  
      
    # Clone a specific branch  
    git clone --branch develop https://github.com/owner/repo-name.git  
      
    # Clone via SSH (if SSH is configured)  
    git clone git@github.com:owner/repo-name.git  
    
[/code]
**С gh (сокращённо):**
[code] 
    gh repo clone owner/repo-name  
    gh repo clone owner/repo-name -- --depth 1  
    
[/code]
## 2\. Создание репозиториев[​](<#2-creating-repositories> "Прямая ссылка на 2. Создание репозиториев")
**С gh:**
[code] 
    # Create a public repo and clone it  
    gh repo create my-new-project --public --clone  
      
    # Private, with description and license  
    gh repo create my-new-project --private --description "A useful tool" --license MIT --clone  
      
    # Under an organization  
    gh repo create my-org/my-new-project --public --clone  
      
    # From existing local directory  
    cd /path/to/existing/project  
    gh repo create my-project --source . --public --push  
    
[/code]
**С git + curl:**
[code] 
    # Create the remote repo via API  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/user/repos \  
      -d '{  
        "name": "my-new-project",  
        "description": "A useful tool",  
        "private": false,  
        "auto_init": true,  
        "license_template": "mit"  
      }'  
      
    # Clone it  
    git clone https://github.com/$GH_USER/my-new-project.git  
    cd my-new-project  
      
    # -- OR -- push an existing local directory to the new repo  
    cd /path/to/existing/project  
    git init  
    git add .  
    git commit -m "Initial commit"  
    git remote add origin https://github.com/$GH_USER/my-new-project.git  
    git push -u origin main  
    
[/code]
Чтобы создать репозиторий внутри организации:
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/orgs/my-org/repos \  
      -d '{"name": "my-new-project", "private": false}'  
    
[/code]
### Из шаблона[​](<#from-a-template> "Прямая ссылка на Из шаблона")
**С gh:**
[code] 
    gh repo create my-new-app --template owner/template-repo --public --clone  
    
[/code]
**С curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/owner/template-repo/generate \  
      -d '{"owner": "'"$GH_USER"'", "name": "my-new-app", "private": false}'  
    
[/code]
## 3\. Форк репозиториев[​](<#3-forking-repositories> "Прямая ссылка на 3. Форк репозиториев")
**С gh:**
[code] 
    gh repo fork owner/repo-name --clone  
    
[/code]
**С git + curl:**
[code] 
    # Create the fork via API  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/owner/repo-name/forks  
      
    # Wait a moment for GitHub to create it, then clone  
    sleep 3  
    git clone https://github.com/$GH_USER/repo-name.git  
    cd repo-name  
      
    # Add the original repo as "upstream" remote  
    git remote add upstream https://github.com/owner/repo-name.git  
    
[/code]
### Синхронизация форка[​](<#keeping-a-fork-in-sync> "Прямая ссылка на Синхронизация форка")
[code] 
    # Pure git — works everywhere  
    git fetch upstream  
    git checkout main  
    git merge upstream/main  
    git push origin main  
    
[/code]
**С gh (сокращённо):**
[code] 
    gh repo sync $GH_USER/repo-name  
    
[/code]
## 4\. Информация о репозитории[​](<#4-repository-information> "Прямая ссылка на 4. Информация о репозитории")
**С gh:**
[code] 
    gh repo view owner/repo-name  
    gh repo list --limit 20  
    gh search repos "machine learning" --language python --sort stars  
    
[/code]
**С curl:**
[code] 
    # View repo details  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO \  
      | python3 -c "  
    import sys, json  
    r = json.load(sys.stdin)  
    print(f\\\"Name: {r['full_name']}\\\")  
    print(f\\\"Description: {r['description']}\\\")  
    print(f\\\"Stars: {r['stargazers_count']}  Forks: {r['forks_count']}\\\")  
    print(f\\\"Default branch: {r['default_branch']}\\\")  
    print(f\\\"Language: {r['language']}\\\")"  
      
    # List your repos  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      \"https://api.github.com/user/repos?per_page=20&sort=updated\" \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin):  
        vis = 'private' if r['private'] else 'public'  
        print(f\\\"  {r['full_name']:40}  {vis:8}  {r.get('language', ''):10}  ★{r['stargazers_count']}\\\")"  
      
    # Search repos  
    curl -s \  
      \"https://api.github.com/search/repositories?q=machine+learning+language:python&sort=stars&per_page=10\" \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin)['items']:  
        print(f\\\"  {r['full_name']:40}  ★{r['stargazers_count']:6}  {r['description'][:60] if r['description'] else ''}\\\")"  
    
[/code]
## 5\. Настройки репозитория[​](<#5-repository-settings> "Прямая ссылка на 5. Настройки репозитория")
**С gh:**
[code] 
    gh repo edit --description "Updated description" --visibility public  
    gh repo edit --enable-wiki=false --enable-issues=true  
    gh repo edit --default-branch main  
    gh repo edit --add-topic "machine-learning,python"  
    gh repo edit --enable-auto-merge  
    
[/code]
**С curl:**
[code] 
    curl -s -X PATCH \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO \  
      -d '{  
        "description": "Updated description",  
        "has_wiki": false,  
        "has_issues": true,  
        "allow_auto_merge": true  
      }'  
      
    # Update topics  
    curl -s -X PUT \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      -H "Accept: application/vnd.github.mercy-preview+json" \  
      https://api.github.com/repos/$OWNER/$REPO/topics \  
      -d '{"names": ["machine-learning", "python", "automation"]}'  
    
[/code]
## 6\. Защита веток[​](<#6-branch-protection> "Прямая ссылка на 6. Защита веток")
[code] 
    # View current protection  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/branches/main/protection  
      
    # Set up branch protection  
    curl -s -X PUT \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \  
      -d '{  
        \"required_status_checks\": {  
          \"strict\": true,  
          \"contexts\": [\"ci/test\", \"ci/lint\"]  
        },  
        \"enforce_admins\": false,  
        \"required_pull_request_reviews\": {  
          \"required_approving_review_count\": 1  
        },  
        \"restrictions\": null  
      }'  
    
[/code]
## 7\. Управление секретами (GitHub Actions)[​](<#7-secrets-management-github-actions> "Прямая ссылка на 7. Управление секретами \\(GitHub Actions\\)")
**С gh:**
[code] 
    gh secret set API_KEY --body "your-secret-value"  
    gh secret set SSH_KEY < ~/.ssh/id_rsa  
    gh secret list  
    gh secret delete API_KEY  
    
[/code]
**С curl:**
Для секретов требуется шифрование с использованием публичного ключа репозитория — через API это более сложно:
[code] 
    # Get the repo's public key for encrypting secrets  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/secrets/public-key  
      
    # Encrypt and set (requires Python with PyNaCl)  
    python3 -c "  
    from base64 import b64encode  
    from nacl import encoding, public  
    import json, sys  
      
    # Get the public key  
    key_id = '<key_id_from_above>'  
    public_key = '<base64_key_from_above>'  
      
    # Encrypt  
    sealed = public.SealedBox(  
        public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder)  
    ).encrypt('your-secret-value'.encode('utf-8'))  
    print(json.dumps({  
        'encrypted_value': b64encode(sealed).decode('utf-8'),  
        'key_id': key_id  
    }))"  
      
    # Then PUT the encrypted secret  
    curl -s -X PUT \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/secrets/API_KEY \  
      -d '<output from python script above>'  
      
    # List secrets (names only, values hidden)  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/secrets \  
      | python3 -c "  
    import sys, json  
    for s in json.load(sys.stdin)['secrets']:  
        print(f\\\"  {s['name']:30}  updated: {s['updated_at']}\\\")"  
    
[/code]
Примечание: Для секретов `gh secret set` значительно проще. Если требуется установить секреты, а `gh` недоступен, рекомендуется установить его хотя бы для этой операции.
## 8\. Релизы[​](<#8-releases> "Прямая ссылка на 8. Релизы")
**С gh:**
[code] 
    gh release create v1.0.0 --title "v1.0.0" --generate-notes  
    gh release create v2.0.0-rc1 --draft --prerelease --generate-notes  
    gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"  
    gh release list  
    gh release download v1.0.0 --dir ./downloads  
    
[/code]
**С curl:**
[code] 
    # Create a release  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/releases \  
      -d '{  
        \"tag_name\": \"v1.0.0\",  
        \"name\": \"v1.0.0\",  
        \"body\": \"## Changelog\\n- Feature A\\n- Bug fix B\",  
        \"draft\": false,  
        \"prerelease\": false,  
        \"generate_release_notes\": true  
      }'  
      
    # List releases  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/releases \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin):  
        tag = r.get('tag_name', 'no tag')  
        print(f\\\"  {tag:15}  {r['name']:30}  {'draft' if r['draft'] else 'published'}\\\")"  
      
    # Upload a release asset (binary file)  
    RELEASE_ID=<id_from_create_response>  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      -H "Content-Type: application/octet-stream" \  
      \"https://uploads.github.com/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets?name=binary-amd64\" \  
      --data-binary @./dist/binary-amd64  
    
[/code]
## 9\. Рабочие процессы GitHub Actions[​](<#9-github-actions-workflows> "Прямая ссылка на 9. Рабочие процессы GitHub Actions")
**С gh:**
[code] 
    gh workflow list  
    gh run list --limit 10  
    gh run view <RUN_ID>  
    gh run view <RUN_ID> --log-failed  
    gh run rerun <RUN_ID>  
    gh run rerun <RUN_ID> --failed  
    gh workflow run ci.yml --ref main  
    gh workflow run deploy.yml -f environment=staging  
    
[/code]
**С curl:**
[code] 
    # List workflows  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/workflows \  
      | python3 -c "  
    import sys, json  
    for w in json.load(sys.stdin)['workflows']:  
        print(f\\\"  {w['id']:10}  {w['name']:30}  {w['state']}\\\")"  
      
    # List recent runs  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      \"https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10\" \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin)['workflow_runs']:  
        print(f\\\"  Run {r['id']}  {r['name']:30}  {r['conclusion'] or r['status']}\\\")"  
      
    # Download failed run logs  
    RUN_ID=<run_id>  
    curl -s -L \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \  
      -o /tmp/ci-logs.zip  
    cd /tmp && unzip -o ci-logs.zip -d ci-logs  
      
    # Re-run a failed workflow  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun  
      
    # Re-run only failed jobs  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun-failed-jobs  
      
    # Trigger a workflow manually (workflow_dispatch)  
    WORKFLOW_ID=<workflow_id_or_filename>  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW_ID/dispatches \  
      -d '{\"ref\": \"main\", \"inputs\": {\"environment\": \"staging\"}}'  
    
[/code]
## 10\. Gist[​](<#10-gists> "Прямая ссылка на 10. Gist")
**С gh:**
[code] 
    gh gist create script.py --public --desc "Useful script"  
    gh gist list  
    
[/code]
**С curl:**
[code] 
    # Create a gist  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/gists \  
      -d '{  
        \"description\": \"Useful script\",  
        \"public\": true,  
        \"files\": {  
          \"script.py\": {\"content\": \"print(\\\"hello\\\")\"}  
        }  
      }'  
      
    # List your gists  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/gists \  
      | python3 -c "  
    import sys, json  
    for g in json.load(sys.stdin):  
        files = ', '.join(g['files'].keys())  
        print(f\\\"  {g['id']}  {g['description'] or '(no desc)':40}  {files}\\\")"  
    
[/code]
## Краткая справочная таблица[​](<#quick-reference-table> "Прямая ссылка на Краткая справочная таблица")
Действие| gh| git + curl
---|---|---|
Клонирование| `gh repo clone o/r`| `git clone https://github.com/o/r.git`
Создание репозитория| `gh repo create name --public`| `curl POST /user/repos`
Форк| `gh repo fork o/r --clone`| `curl POST /repos/o/r/forks` + `git clone`
Информация о репозитории| `gh repo view o/r`| `curl GET /repos/o/r`
Редактирование настроек| `gh repo edit --...`| `curl PATCH /repos/o/r`
Создание релиза| `gh release create v1.0`| `curl POST /repos/o/r/releases`
Список workflow| `gh workflow list`| `curl GET /repos/o/r/actions/workflows`
Повторный запуск CI| `gh run rerun ID`| `curl POST /repos/o/r/actions/runs/ID/rerun`
Установка секрета| `gh secret set KEY`| `curl PUT /repos/o/r/actions/secrets/KEY` (+ шифрование)
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
    * [Настройка](<#setup>)
  * [1\. Клонирование репозиториев](<#1-cloning-repositories>)
  * [2\. Создание репозиториев](<#2-creating-repositories>)
    * [Из шаблона](<#from-a-template>)
  * [3\. Форк репозиториев](<#3-forking-repositories>)
    * [Синхронизация форка](<#keeping-a-fork-in-sync>)
  * [4\. Информация о репозитории](<#4-repository-information>)
  * [5\. Настройки репозитория](<#5-repository-settings>)
  * [6\. Защита веток](<#6-branch-protection>)
  * [7\. Управление секретами (GitHub Actions)](<#7-secrets-management-github-actions>)
  * [8\. Релизы](<#8-releases>)
  * [9\. Рабочие процессы GitHub Actions](<#9-github-actions-workflows>)
  * [10\. Gist](<#10-gists>)
  * [Краткая справочная таблица](<#quick-reference-table>)


<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-repo-management -->
