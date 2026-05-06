On this page
Create, triage, label, assign GitHub issues via gh or REST.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/github/github-issues`  
Version| `1.1.0`  
Author| Hermes Agent  
License| MIT  
Tags| `GitHub`, `Issues`, `Project-Management`, `Bug-Tracking`, `Triage`  
Related skills| [`github-auth`](</docs/user-guide/skills/bundled/github/github-github-auth>), [`github-pr-workflow`](</docs/user-guide/skills/bundled/github/github-github-pr-workflow>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# GitHub Issues Management
Create, search, triage, and manage GitHub issues. Each section shows `gh` first, then the `curl` fallback.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * Authenticated with GitHub (see `github-auth` skill)
  * Inside a git repo with a GitHub remote, or specify the repo explicitly


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
      
    REMOTE_URL=$(git remote get-url origin)  
    OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')  
    OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)  
    REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)  
    
[/code]
* * *
## 1\. Viewing Issues[​](<#1-viewing-issues> "Direct link to 1. Viewing Issues")
**With gh:**
[code] 
    gh issue list  
    gh issue list --state open --label "bug"  
    gh issue list --assignee @me  
    gh issue list --search "authentication error" --state all  
    gh issue view 42  
    
[/code]
**With curl:**
[code] 
    # List open issues  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin):  
        if 'pull_request' not in i:  # GitHub API returns PRs in /issues too  
            labels = ', '.join(l['name'] for l in i['labels'])  
            print(f\"#{i['number']:5}  {i['state']:6}  {labels:30}  {i['title']}\")"  
      
    # Filter by label  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&labels=bug&per_page=20" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin):  
        if 'pull_request' not in i:  
            print(f\"#{i['number']}  {i['title']}\")"  
      
    # View a specific issue  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42 \  
      | python3 -c "  
    import sys, json  
    i = json.load(sys.stdin)  
    labels = ', '.join(l['name'] for l in i['labels'])  
    assignees = ', '.join(a['login'] for a in i['assignees'])  
    print(f\"#{i['number']}: {i['title']}\")  
    print(f\"State: {i['state']}  Labels: {labels}  Assignees: {assignees}\")  
    print(f\"Author: {i['user']['login']}  Created: {i['created_at']}\")  
    print(f\"\n{i['body']}\")"  
      
    # Search issues  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/search/issues?q=authentication+error+repo:$OWNER/$REPO" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin)['items']:  
        print(f\"#{i['number']}  {i['state']:6}  {i['title']}\")"  
    
[/code]
## 2\. Creating Issues[​](<#2-creating-issues> "Direct link to 2. Creating Issues")
**With gh:**
[code] 
    gh issue create \  
      --title "Login redirect ignores ?next= parameter" \  
      --body "## Description  
    After logging in, users always land on /dashboard.  
      
    ## Steps to Reproduce  
    1. Navigate to /settings while logged out  
    2. Get redirected to /login?next=/settings  
    3. Log in  
    4. Actual: redirected to /dashboard (should go to /settings)  
      
    ## Expected Behavior  
    Respect the ?next= query parameter." \  
      --label "bug,backend" \  
      --assignee "username"  
    
[/code]
**With curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues \  
      -d '{  
        "title": "Login redirect ignores ?next= parameter",  
        "body": "## Description\nAfter logging in, users always land on /dashboard.\n\n## Steps to Reproduce\n1. Navigate to /settings while logged out\n2. Get redirected to /login?next=/settings\n3. Log in\n4. Actual: redirected to /dashboard\n\n## Expected Behavior\nRespect the ?next= query parameter.",  
        "labels": ["bug", "backend"],  
        "assignees": ["username"]  
      }'  
    
[/code]
### Bug Report Template[​](<#bug-report-template> "Direct link to Bug Report Template")
[code] 
    ## Bug Description  
    <What's happening>  
      
    ## Steps to Reproduce  
    1. <step>  
    2. <step>  
      
    ## Expected Behavior  
    <What should happen>  
      
    ## Actual Behavior  
    <What actually happens>  
      
    ## Environment  
    - OS: <os>  
    - Version: <version>  
    
[/code]
### Feature Request Template[​](<#feature-request-template> "Direct link to Feature Request Template")
[code] 
    ## Feature Description  
    <What you want>  
      
    ## Motivation  
    <Why this would be useful>  
      
    ## Proposed Solution  
    <How it could work>  
      
    ## Alternatives Considered  
    <Other approaches>  
    
[/code]
## 3\. Managing Issues[​](<#3-managing-issues> "Direct link to 3. Managing Issues")
### Add/Remove Labels[​](<#addremove-labels> "Direct link to Add/Remove Labels")
**With gh:**
[code] 
    gh issue edit 42 --add-label "priority:high,bug"  
    gh issue edit 42 --remove-label "needs-triage"  
    
[/code]
**With curl:**
[code] 
    # Add labels  
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \  
      -d '{"labels": ["priority:high", "bug"]}'  
      
    # Remove a label  
    curl -s -X DELETE \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/labels/needs-triage  
      
    # List available labels in the repo  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/labels \  
      | python3 -c "  
    import sys, json  
    for l in json.load(sys.stdin):  
        print(f\"  {l['name']:30}  {l.get('description', '')}\")"  
    
[/code]
### Assignment[​](<#assignment> "Direct link to Assignment")
**With gh:**
[code] 
    gh issue edit 42 --add-assignee username  
    gh issue edit 42 --add-assignee @me  
    
[/code]
**With curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/assignees \  
      -d '{"assignees": ["username"]}'  
    
[/code]
### Commenting[​](<#commenting> "Direct link to Commenting")
**With gh:**
[code] 
    gh issue comment 42 --body "Investigated — root cause is in auth middleware. Working on a fix."  
    
[/code]
**With curl:**
[code] 
    curl -s -X POST \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42/comments \  
      -d '{"body": "Investigated — root cause is in auth middleware. Working on a fix."}'  
    
[/code]
### Closing and Reopening[​](<#closing-and-reopening> "Direct link to Closing and Reopening")
**With gh:**
[code] 
    gh issue close 42  
    gh issue close 42 --reason "not planned"  
    gh issue reopen 42  
    
[/code]
**With curl:**
[code] 
    # Close  
    curl -s -X PATCH \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42 \  
      -d '{"state": "closed", "state_reason": "completed"}'  
      
    # Reopen  
    curl -s -X PATCH \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      https://api.github.com/repos/$OWNER/$REPO/issues/42 \  
      -d '{"state": "open"}'  
    
[/code]
### Linking Issues to PRs[​](<#linking-issues-to-prs> "Direct link to Linking Issues to PRs")
Issues are automatically closed when a PR merges with the right keywords in the body:
[code] 
    Closes #42  
    Fixes #42  
    Resolves #42  
    
[/code]
To create a branch from an issue:
**With gh:**
[code] 
    gh issue develop 42 --checkout  
    
[/code]
**With git (manual equivalent):**
[code] 
    git checkout main && git pull origin main  
    git checkout -b fix/issue-42-login-redirect  
    
[/code]
## 4\. Issue Triage Workflow[​](<#4-issue-triage-workflow> "Direct link to 4. Issue Triage Workflow")
When asked to triage issues:
  1. **List untriaged issues:**


[code] 
    # With gh  
    gh issue list --label "needs-triage" --state open  
      
    # With curl  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/issues?labels=needs-triage&state=open" \  
      | python3 -c "  
    import sys, json  
    for i in json.load(sys.stdin):  
        if 'pull_request' not in i:  
            print(f\"#{i['number']}  {i['title']}\")"  
    
[/code]
  2. **Read and categorize** each issue (view details, understand the bug/feature)
  3. **Apply labels and priority** (see Managing Issues above)
  4. **Assign** if the owner is clear
  5. **Comment with triage notes** if needed


## 5\. Bulk Operations[​](<#5-bulk-operations> "Direct link to 5. Bulk Operations")
For batch operations, combine API calls with shell scripting:
**With gh:**
[code] 
    # Close all issues with a specific label  
    gh issue list --label "wontfix" --json number --jq '.[].number' | \  
      xargs -I {} gh issue close {} --reason "not planned"  
    
[/code]
**With curl:**
[code] 
    # List issue numbers with a label, then close each  
    curl -s \  
      -H "Authorization: token $GITHUB_TOKEN" \  
      "https://api.github.com/repos/$OWNER/$REPO/issues?labels=wontfix&state=open" \  
      | python3 -c "import sys,json; [print(i['number']) for i in json.load(sys.stdin)]" \  
      | while read num; do  
        curl -s -X PATCH \  
          -H "Authorization: token $GITHUB_TOKEN" \  
          https://api.github.com/repos/$OWNER/$REPO/issues/$num \  
          -d '{"state": "closed", "state_reason": "not_planned"}'  
        echo "Closed #$num"  
      done  
    
[/code]
## Quick Reference Table[​](<#quick-reference-table> "Direct link to Quick Reference Table")
Action| gh| curl endpoint  
---|---|---  
List issues| `gh issue list`| `GET /repos/{o}/{r}/issues`  
View issue| `gh issue view N`| `GET /repos/{o}/{r}/issues/N`  
Create issue| `gh issue create ...`| `POST /repos/{o}/{r}/issues`  
Add labels| `gh issue edit N --add-label ...`| `POST /repos/{o}/{r}/issues/N/labels`  
Assign| `gh issue edit N --add-assignee ...`| `POST /repos/{o}/{r}/issues/N/assignees`  
Comment| `gh issue comment N --body ...`| `POST /repos/{o}/{r}/issues/N/comments`  
Close| `gh issue close N`| `PATCH /repos/{o}/{r}/issues/N`  
Search| `gh issue list --search "..."`| `GET /search/issues?q=...`  
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
    * [Setup](<#setup>)
  * [1\. Viewing Issues](<#1-viewing-issues>)
  * [2\. Creating Issues](<#2-creating-issues>)
    * [Bug Report Template](<#bug-report-template>)
    * [Feature Request Template](<#feature-request-template>)
  * [3\. Managing Issues](<#3-managing-issues>)
    * [Add/Remove Labels](<#addremove-labels>)
    * [Assignment](<#assignment>)
    * [Commenting](<#commenting>)
    * [Closing and Reopening](<#closing-and-reopening>)
    * [Linking Issues to PRs](<#linking-issues-to-prs>)
  * [4\. Issue Triage Workflow](<#4-issue-triage-workflow>)
  * [5\. Bulk Operations](<#5-bulk-operations>)
  * [Quick Reference Table](<#quick-reference-table>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-github-issues -->
