On this page
Clone/create/fork repos; manage remotes, releases.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/github/github-repo-management`  
Version| `1.1.0`  
Author| Hermes Agent  
License| MIT  
Tags| `GitHub`, `Repositories`, `Git`, `Releases`, `Secrets`, `Configuration`  
Related skills| [`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>), [`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>), [`github-issues`](</docs/user-guide/skills/bundled/github/github-github-issues>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# GitHub Repository Management
Create, clone, fork, configure, and manage GitHub repositories. Each section shows `gh` first, then the `git` \+ `curl` fallback.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * Authenticated with GitHub (see `github-auth` skill)


### Setup[​](<#setup> "Direct link to Setup")
[code] 
    if command -v gh &>/dev/null && gh auth status &>/dev/null; then  
      AUTH="gh"  
    else  
      AUTH="git"  
      if [ -z "$GITHUB_TOKEN" ]; then  
        if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then  
          GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')  
        elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then  
          GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')  
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
If you're inside a repo already:
[code] 
    REMOTE_URL=$(git remote get-url origin)  
    OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')  
    OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)  
    REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)  
    
[/code]
* * *
## 1\. Cloning Repositories[​](<#1-cloning-repositories> "Direct link to 1. Cloning Repositories")
Cloning is pure `git` — works identically either way:
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
**With gh (shorthand):**
[code] 
    gh repo clone owner/repo-name  
    gh repo clone owner/repo-name -- --depth 1  
    
[/code]
## 2\. Creating Repositories[​](<#2-creating-repositories> "Direct link to 2. Creating Repositories")
**With gh:**
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
**With git + curl:**
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
To create under an organization:
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/orgs/my-org/repos \  
      -d '{"name": "my-new-project", "private": false}'  
    
[/code]
### From a Template[​](<#from-a-template> "Direct link to From a Template")
**With gh:**
[code] 
    gh repo create my-new-app --template owner/template-repo --public --clone  
    
[/code]
**With curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/owner/template-repo/generate \  
      -d '{"owner": "'"$GH_USER"'", "name": "my-new-app", "private": false}'  
    
[/code]
## 3\. Forking Repositories[​](<#3-forking-repositories> "Direct link to 3. Forking Repositories")
**With gh:**
[code] 
    gh repo fork owner/repo-name --clone  
    
[/code]
**With git + curl:**
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
### Keeping a Fork in Sync[​](<#keeping-a-fork-in-sync> "Direct link to Keeping a Fork in Sync")
[code] 
    # Pure git — works everywhere  
    git fetch upstream  
    git checkout main  
    git merge upstream/main  
    git push origin main  
    
[/code]
**With gh (shortcut):**
[code] 
    gh repo sync $GH_USER/repo-name  
    
[/code]
## 4\. Repository Information[​](<#4-repository-information> "Direct link to 4. Repository Information")
**With gh:**
[code] 
    gh repo view owner/repo-name  
    gh repo list --limit 20  
    gh search repos "machine learning" --language python --sort stars  
    
[/code]
**With curl:**
[code] 
    # View repo details  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO \  
      | python3 -c "  
    import sys, json  
    r = json.load(sys.stdin)  
    print(f\"Name: {r['full_name']}\")  
    print(f\"Description: {r['description']}\")  
    print(f\"Stars: {r['stargazers_count']}  Forks: {r['forks_count']}\")  
    print(f\"Default branch: {r['default_branch']}\")  
    print(f\"Language: {r['language']}\")"  
      
    # List your repos  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/user/repos?per_page=20&sort=updated" \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin):  
        vis = 'private' if r['private'] else 'public'  
        print(f\"  {r['full_name']:40}  {vis:8}  {r.get('language', ''):10}  ★{r['stargazers_count']}\")"  
      
    # Search repos  
    curl -s \  
      "https://api.github.com/search/repositories?q=machine+learning+language:python&sort=stars&per_page=10" \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin)['items']:  
        print(f\"  {r['full_name']:40}  ★{r['stargazers_count']:6}  {r['description'][:60] if r['description'] else ''}\")"  
    
[/code]
## 5\. Repository Settings[​](<#5-repository-settings> "Direct link to 5. Repository Settings")
**With gh:**
[code] 
    gh repo edit --description "Updated description" --visibility public  
    gh repo edit --enable-wiki=false --enable-issues=true  
    gh repo edit --default-branch main  
    gh repo edit --add-topic "machine-learning,python"  
    gh repo edit --enable-auto-merge  
    
[/code]
**With curl:**
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
## 6\. Branch Protection[​](<#6-branch-protection> "Direct link to 6. Branch Protection")
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
        "required_status_checks": {  
          "strict": true,  
          "contexts": ["ci/test", "ci/lint"]  
        },  
        "enforce_admins": false,  
        "required_pull_request_reviews": {  
          "required_approving_review_count": 1  
        },  
        "restrictions": null  
      }'  
    
[/code]
## 7\. Secrets Management (GitHub Actions)[​](<#7-secrets-management-github-actions> "Direct link to 7. Secrets Management \(GitHub Actions\)")
**With gh:**
[code] 
    gh secret set API_KEY --body "your-secret-value"  
    gh secret set SSH_KEY < ~/.ssh/id_rsa  
    gh secret list  
    gh secret delete API_KEY  
    
[/code]
**With curl:**
Secrets require encryption with the repo's public key — more involved via API:
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
        print(f\"  {s['name']:30}  updated: {s['updated_at']}\")"  
    
[/code]
Note: For secrets, `gh secret set` is dramatically simpler. If setting secrets is needed and `gh` isn't available, recommend installing it for just that operation.
## 8\. Releases[​](<#8-releases> "Direct link to 8. Releases")
**With gh:**
[code] 
    gh release create v1.0.0 --title "v1.0.0" --generate-notes  
    gh release create v2.0.0-rc1 --draft --prerelease --generate-notes  
    gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"  
    gh release list  
    gh release download v1.0.0 --dir ./downloads  
    
[/code]
**With curl:**
[code] 
    # Create a release  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/releases \  
      -d '{  
        "tag_name": "v1.0.0",  
        "name": "v1.0.0",  
        "body": "## Changelog\n- Feature A\n- Bug fix B",  
        "draft": false,  
        "prerelease": false,  
        "generate_release_notes": true  
      }'  
      
    # List releases  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/releases \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin):  
        tag = r.get('tag_name', 'no tag')  
        print(f\"  {tag:15}  {r['name']:30}  {'draft' if r['draft'] else 'published'}\")"  
      
    # Upload a release asset (binary file)  
    RELEASE_ID=<id_from_create_response>  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      -H "Content-Type: application/octet-stream" \  
      "https://uploads.github.com/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets?name=binary-amd64" \  
      --data-binary @./dist/binary-amd64  
    
[/code]
## 9\. GitHub Actions Workflows[​](<#9-github-actions-workflows> "Direct link to 9. GitHub Actions Workflows")
**With gh:**
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
**With curl:**
[code] 
    # List workflows  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/actions/workflows \  
      | python3 -c "  
    import sys, json  
    for w in json.load(sys.stdin)['workflows']:  
        print(f\"  {w['id']:10}  {w['name']:30}  {w['state']}\")"  
      
    # List recent runs  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10" \  
      | python3 -c "  
    import sys, json  
    for r in json.load(sys.stdin)['workflow_runs']:  
        print(f\"  Run {r['id']}  {r['name']:30}  {r['conclusion'] or r['status']}\")"  
      
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
      -d '{"ref": "main", "inputs": {"environment": "staging"}}'  
    
[/code]
## 10\. Gists[​](<#10-gists> "Direct link to 10. Gists")
**With gh:**
[code] 
    gh gist create script.py --public --desc "Useful script"  
    gh gist list  
    
[/code]
**With curl:**
[code] 
    # Create a gist  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/gists \  
      -d '{  
        "description": "Useful script",  
        "public": true,  
        "files": {  
          "script.py": {"content": "print(\"hello\")"}  
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
        print(f\"  {g['id']}  {g['description'] or '(no desc)':40}  {files}\")"  
    
[/code]
## Quick Reference Table[​](<#quick-reference-table> "Direct link to Quick Reference Table")
Action| gh| git + curl  
---|---|---  
Clone| `gh repo clone o/r`| `git clone https://github.com/o/r.git`  
Create repo| `gh repo create name --public`| `curl POST /user/repos`  
Fork| `gh repo fork o/r --clone`| `curl POST /repos/o/r/forks` \+ `git clone`  
Repo info| `gh repo view o/r`| `curl GET /repos/o/r`  
Edit settings| `gh repo edit --...`| `curl PATCH /repos/o/r`  
Create release| `gh release create v1.0`| `curl POST /repos/o/r/releases`  
List workflows| `gh workflow list`| `curl GET /repos/o/r/actions/workflows`  
Rerun CI| `gh run rerun ID`| `curl POST /repos/o/r/actions/runs/ID/rerun`  
Set secret| `gh secret set KEY`| `curl PUT /repos/o/r/actions/secrets/KEY` (+ encryption)  
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
    * [Setup](<#setup>)
  * [1\. Cloning Repositories](<#1-cloning-repositories>)
  * [2\. Creating Repositories](<#2-creating-repositories>)
    * [From a Template](<#from-a-template>)
  * [3\. Forking Repositories](<#3-forking-repositories>)
    * [Keeping a Fork in Sync](<#keeping-a-fork-in-sync>)
  * [4\. Repository Information](<#4-repository-information>)
  * [5\. Repository Settings](<#5-repository-settings>)
  * [6\. Branch Protection](<#6-branch-protection>)
  * [7\. Secrets Management (GitHub Actions)](<#7-secrets-management-github-actions>)
  * [8\. Releases](<#8-releases>)
  * [9\. GitHub Actions Workflows](<#9-github-actions-workflows>)
  * [10\. Gists](<#10-gists>)
  * [Quick Reference Table](<#quick-reference-table>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-repo-management -->
