On this page
Настройка аутентификации GitHub: HTTPS-токены, SSH-ключи, вход через gh CLI.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   |
|---|---|
|Source| Встроенный (устанавливается по умолчанию) |
|Path| `skills/github/github-auth` |
|Version| `1.1.0` |
|Author| Hermes Agent |
|License| MIT |
|Tags| `GitHub`, `Authentication`, `Git`, `gh-cli`, `SSH`, `Setup` |
|Related skills| [`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>), [`github-code-review`](</docs/user-guide/skills/bundled/github/github-github-code-review>), [`github-issues`](</docs/user-guide/skills/bundled/github/github-github-issues>), [`github-repo-management`](</docs/user-guide/skills/bundled/github/github-github-repo-management>) |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Агент видит эти инструкции, когда навык активен.
# Настройка аутентификации GitHub
Этот навык настраивает аутентификацию, чтобы агент мог работать с репозиториями GitHub, PR, issues и CI. Он охватывает два пути:
  * **`git` (всегда доступен)** — использует HTTPS-персональные токены доступа или SSH-ключи
  * **`gh` CLI (если установлен)** — более широкий доступ к GitHub API с упрощённым流程ом аутентификации


## Detection Flow[​](<#detection-flow> "Прямая ссылка на Detection Flow")
Когда пользователь просит вас работать с GitHub, сначала выполните эту проверку:
[code] 
    # Check what's available  
    git --version  
    gh --version 2>/dev/null || echo "gh not installed"  
      
    # Check if already authenticated  
    gh auth status 2>/dev/null || echo "gh not authenticated"  
    git config --global credential.helper 2>/dev/null || echo "no git credential helper"  
    
[/code]
**Decision tree:**
  1. Если `gh auth status` показывает аутентифицировано → всё в порядке, используйте `gh` для всего
  2. Если `gh` установлен, но не аутентифицирован → используйте метод "gh auth" ниже
  3. Если `gh` не установлен → используйте метод "только git" ниже (sudo не требуется)


* * *
## Method 1: Git-Only Authentication (No gh, No sudo)[​](<#method-1-git-only-authentication-no-gh-no-sudo> "Прямая ссылка на Method 1: Git-Only Authentication (No gh, No sudo)")
Это работает на любой машине с установленным `git`. Права root не требуются.
### Option A: HTTPS with Personal Access Token (Recommended)[​](<#option-a-https-with-personal-access-token-recommended> "Прямая ссылка на Option A: HTTPS with Personal Access Token (Recommended)")
Это самый портативный метод — работает везде, настройка SSH не требуется.
**Step 1: Create a personal access token**
Сообщите пользователю перейти по адресу: **<https://github.com/settings/tokens>**
  * Нажмите «Generate new token (classic)»
  * Дайте ему имя, например «hermes-agent»
  * Выберите области доступа (scopes):
    * `repo` (полный доступ к репозиторию — чтение, запись, push, PR)
    * `workflow` (запуск и управление GitHub Actions)
    * `read:org` (при работе с репозиториями организации)
  * Установите срок действия (90 дней — хорошее значение по умолчанию)
  * Скопируйте токен — он больше не будет показан


**Step 2: Configure git to store the token**
[code] 
    # Set up the credential helper to cache credentials  
    # "store" saves to ~/.git-credentials in plaintext (simple, persistent)  
    git config --global credential.helper store  
      
    # Now do a test operation that triggers auth — git will prompt for credentials  
    # Username: <their-github-username>  
    # Password: <paste the personal access token, NOT their GitHub password>  
    git ls-remote https://github.com/<their-username>/<any-repo>.git  
    
[/code]
После однократного ввода учётных данных они сохраняются и используются для всех последующих операций.
**Alternative: cache helper (credentials expire from memory)**
[code] 
    # Cache in memory for 8 hours (28800 seconds) instead of saving to disk  
    git config --global credential.helper 'cache --timeout=28800'  
    
[/code]
**Alternative: set the token directly in the remote URL (per-repo)**
[code] 
    # Embed token in the remote URL (avoids credential prompts entirely)  
    git remote set-url origin https://<username>:<token>@github.com/<owner>/<repo>.git  
    
[/code]
**Step 3: Configure git identity**
[code] 
    # Required for commits — set name and email  
    git config --global user.name "Their Name"  
    git config --global user.email "their-email@example.com"  
    
[/code]
**Step 4: Verify**
[code] 
    # Test push access (this should work without any prompts now)  
    git ls-remote https://github.com/<their-username>/<any-repo>.git  
      
    # Verify identity  
    git config --global user.name  
    git config --global user.email  
    
[/code]
### Option B: SSH Key Authentication[​](<#option-b-ssh-key-authentication> "Прямая ссылка на Option B: SSH Key Authentication")
Подходит для пользователей, которые предпочитают SSH или уже настроили ключи.
**Step 1: Check for existing SSH keys**
[code] 
    ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"  
    
[/code]
**Step 2: Generate a key if needed**
[code] 
    # Generate an ed25519 key (modern, secure, fast)  
    ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""  
      
    # Display the public key for them to add to GitHub  
    cat ~/.ssh/id_ed25519.pub  
    
[/code]
Сообщите пользователю добавить открытый ключ по адресу: **<https://github.com/settings/keys>**
  * Нажмите «New SSH key»
  * Вставьте содержимое открытого ключа
  * Дайте ему название, например «hermes-agent-<machine-name>»


**Step 3: Test the connection**
[code] 
    ssh -T git@github.com  
    # Expected: "Hi <username>! You've successfully authenticated..."  
    
[/code]
**Step 4: Configure git to use SSH for GitHub**
[code] 
    # Rewrite HTTPS GitHub URLs to SSH automatically  
    git config --global url."git@github.com:".insteadOf "https://github.com/"  
    
[/code]
**Step 5: Configure git identity**
[code] 
    git config --global user.name "Their Name"  
    git config --global user.email "their-email@example.com"  
    
[/code]
* * *
## Method 2: gh CLI Authentication[​](<#method-2-gh-cli-authentication> "Прямая ссылка на Method 2: gh CLI Authentication")
Если `gh` установлен, он обрабатывает как доступ к API, так и учётные данные git за один шаг.
### Interactive Browser Login (Desktop)[​](<#interactive-browser-login-desktop> "Прямая ссылка на Interactive Browser Login (Desktop)")
[code] 
    gh auth login  
    # Select: GitHub.com  
    # Select: HTTPS  
    # Authenticate via browser  
    
[/code]
### Token-Based Login (Headless / SSH Servers)[​](<#token-based-login-headless--ssh-servers> "Прямая ссылка на Token-Based Login (Headless / SSH Servers)")
[code] 
    echo "<THEIR_TOKEN>" | gh auth login --with-token  
      
    # Set up git credentials through gh  
    gh auth setup-git  
    
[/code]
### Verify[​](<#verify> "Прямая ссылка на Verify")
[code] 
    gh auth status  
    
[/code]
* * *
## Using the GitHub API Without gh[​](<#using-the-github-api-without-gh> "Прямая ссылка на Using the GitHub API Without gh")
Если `gh` недоступен, вы всё равно можете использовать полный GitHub API через `curl` с персональным токеном доступа. Так другие навыки GitHub реализуют свои запасные варианты.
### Setting the Token for API Calls[​](<#setting-the-token-for-api-calls> "Прямая ссылка на Setting the Token for API Calls")
[code] 
    # Option 1: Export as env var (preferred — keeps it out of commands)  
    export GITHUB_TOKEN="<token>"  
      
    # Then use in curl calls:  
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
      https://api.github.com/user  
    
[/code]
### Extracting the Token from Git Credentials[​](<#extracting-the-token-from-git-credentials> "Прямая ссылка на Extracting the Token from Git Credentials")
Если учётные данные git уже настроены (через credential.helper store), токен можно извлечь:
[code] 
    # Read from git credential store  
    grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'  
    
[/code]
### Helper: Detect Auth Method[​](<#helper-detect-auth-method> "Прямая ссылка на Helper: Detect Auth Method")
Используйте этот шаблон в начале любого GitHub-процесса:
[code] 
    # Try gh first, fall back to git + curl  
    if command -v gh &>/dev/null && gh auth status &>/dev/null; then  
      echo "AUTH_METHOD=gh"  
    elif [ -n "$GITHUB_TOKEN" ]; then  
      echo "AUTH_METHOD=curl"  
    elif [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then  
      export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')  
      echo "AUTH_METHOD=curl"  
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then  
      export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')  
      echo "AUTH_METHOD=curl"  
    else  
      echo "AUTH_METHOD=none"  
      echo "Need to set up authentication first"  
    fi  
    
[/code]
* * *
## Troubleshooting[​](<#troubleshooting> "Прямая ссылка на Troubleshooting")
Проблема| Решение  
|---|---  
`git push` запрашивает пароль| GitHub отключил аутентификацию по паролю. Используйте персональный токен доступа в качестве пароля или переключитесь на SSH  
`remote: Permission to X denied`| Токену может не хватать области `repo` — сгенерируйте новый с правильными областями  
`fatal: Authentication failed`| Кешированные учётные данные могли устареть — выполните `git credential reject`, затем повторную аутентификацию  
`ssh: connect to host github.com port 22: Connection refused`| Попробуйте SSH через HTTPS-порт: добавьте `Host github.com` с `Port 443` и `Hostname ssh.github.com` в `~/.ssh/config`  
Учётные данные не сохраняются| Проверьте `git config --global credential.helper` — должно быть `store` или `cache`  
Несколько аккаунтов GitHub| Используйте SSH с разными ключами для каждого псевдонима хоста в `~/.ssh/config` или URL-адреса учётных данных для каждого репозитория  
`gh: command not found` + нет sudo| Используйте метод только с git (Method 1) — установка не требуется  
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Detection Flow](<#detection-flow>)
  * [Method 1: Git-Only Authentication (No gh, No sudo)](<#method-1-git-only-authentication-no-gh-no-sudo>)
    * [Option A: HTTPS with Personal Access Token (Recommended)](<#option-a-https-with-personal-access-token-recommended>)
    * [Option B: SSH Key Authentication](<#option-b-ssh-key-authentication>)
  * [Method 2: gh CLI Authentication](<#method-2-gh-cli-authentication>)
    * [Interactive Browser Login (Desktop)](<#interactive-browser-login-desktop>)
    * [Token-Based Login (Headless / SSH Servers)](<#token-based-login-headless--ssh-servers>)
    * [Verify](<#verify>)
  * [Using the GitHub API Without gh](<#using-the-github-api-without-gh>)
    * [Setting the Token for API Calls](<#setting-the-token-for-api-calls>)
    * [Extracting the Token from Git Credentials](<#extracting-the-token-from-git-credentials>)
    * [Helper: Detect Auth Method](<#helper-detect-auth-method>)
  * [Troubleshooting](<#troubleshooting>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-auth -->
