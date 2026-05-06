On this page
**The problem:** Your team opens PRs faster than you can review them. PRs sit for days waiting for eyeballs. Junior devs merge bugs because nobody had time to check. You spend your mornings catching up on diffs instead of building.
**The solution:** An AI agent that watches your repos around the clock, reviews every new PR for bugs, security issues, and code quality, and sends you a summary — so you only spend time on PRs that actually need human judgment.
**What you'll build:**
[code] 
    ┌───────────────────────────────────────────────────────────────────┐  
    │                                                                   │  
    │   Cron Timer  ──▶  Hermes Agent  ──▶  GitHub API  ──▶  Review     │  
    │   (every 2h)       + gh CLI           (PR diffs)       delivery   │  
    │                    + skill                             (Telegram, │  
    │                    + memory                            Discord,   │  
    │                                                        local)     │  
    │                                                                   │  
    └───────────────────────────────────────────────────────────────────┘  
    
[/code]
This guide uses **cron jobs** to poll for PRs on a schedule — no server or public endpoint needed. Works behind NAT and firewalls.
Want real-time reviews instead?
If you have a public endpoint available, check out [Automated GitHub PR Comments with Webhooks](</docs/guides/webhook-github-pr-review>) — GitHub pushes events to Hermes instantly when PRs are opened or updated.
* * *
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **Hermes Agent installed** — see the [Installation guide](</docs/getting-started/installation>)
  * **Gateway running** for cron jobs:
[code] hermes gateway install   # Install as a service  
        # or  
        hermes gateway           # Run in foreground  
        
[/code]
  * **GitHub CLI (`gh`) installed and authenticated**:
[code] # Install  
        brew install gh        # macOS  
        sudo apt install gh    # Ubuntu/Debian  
          
        # Authenticate  
        gh auth login  
        
[/code]
  * **Messaging configured** (optional) — [Telegram](</docs/user-guide/messaging/telegram>) or [Discord](</docs/user-guide/messaging/discord>)


No messaging? No problem
Use `deliver: "local"` to save reviews to `~/.hermes/cron/output/`. Great for testing before wiring up notifications.
* * *
## Step 1: Verify the Setup[​](<#step-1-verify-the-setup> "Direct link to Step 1: Verify the Setup")
Make sure Hermes can access GitHub. Start a chat:
[code] 
    hermes  
    
[/code]
Test with a simple command:
[code] 
    Run: gh pr list --repo NousResearch/hermes-agent --state open --limit 3  
    
[/code]
You should see a list of open PRs. If this works, you're ready.
* * *
## Step 2: Try a Manual Review[​](<#step-2-try-a-manual-review> "Direct link to Step 2: Try a Manual Review")
Still in the chat, ask Hermes to review a real PR:
[code] 
    Review this pull request. Read the diff, check for bugs, security issues,  
    and code quality. Be specific about line numbers and quote problematic code.  
      
    Run: gh pr diff 3888 --repo NousResearch/hermes-agent  
    
[/code]
Hermes will:
  1. Execute `gh pr diff` to fetch the code changes
  2. Read through the entire diff
  3. Produce a structured review with specific findings


If you're happy with the quality, time to automate it.
* * *
## Step 3: Create a Review Skill[​](<#step-3-create-a-review-skill> "Direct link to Step 3: Create a Review Skill")
A skill gives Hermes consistent review guidelines that persist across sessions and cron runs. Without one, review quality varies.
[code] 
    mkdir -p ~/.hermes/skills/code-review  
    
[/code]
Create `~/.hermes/skills/code-review/SKILL.md`:
[code] 
    ---  
    name: code-review  
    description: Review pull requests for bugs, security issues, and code quality  
    ---  
      
    # Code Review Guidelines  
      
    When reviewing a pull request:  
      
    ## What to Check  
    1. **Bugs** — Logic errors, off-by-one, null/undefined handling  
    2. **Security** — Injection, auth bypass, secrets in code, SSRF  
    3. **Performance** — N+1 queries, unbounded loops, memory leaks  
    4. **Style** — Naming conventions, dead code, missing error handling  
    5. **Tests** — Are changes tested? Do tests cover edge cases?  
      
    ## Output Format  
    For each finding:  
    - **File:Line** — exact location  
    - **Severity** — Critical / Warning / Suggestion  
    - **What's wrong** — one sentence  
    - **Fix** — how to fix it  
      
    ## Rules  
    - Be specific. Quote the problematic code.  
    - Don't flag style nitpicks unless they affect readability.  
    - If the PR looks good, say so. Don't invent problems.  
    - End with: APPROVE / REQUEST_CHANGES / COMMENT  
    
[/code]
Verify it loaded — start `hermes` and you should see `code-review` in the skills list at startup.
* * *
## Step 4: Teach It Your Conventions[​](<#step-4-teach-it-your-conventions> "Direct link to Step 4: Teach It Your Conventions")
This is what makes the reviewer actually useful. Start a session and teach Hermes your team's standards:
[code] 
    Remember: In our backend repo, we use Python with FastAPI.  
    All endpoints must have type annotations and Pydantic models.  
    We don't allow raw SQL — only SQLAlchemy ORM.  
    Test files go in tests/ and must use pytest fixtures.  
    
[/code]
[code] 
    Remember: In our frontend repo, we use TypeScript with React.  
    No `any` types allowed. All components must have props interfaces.  
    We use React Query for data fetching, never useEffect for API calls.  
    
[/code]
These memories persist forever — the reviewer will enforce your conventions without being told each time.
* * *
## Step 5: Create the Automated Cron Job[​](<#step-5-create-the-automated-cron-job> "Direct link to Step 5: Create the Automated Cron Job")
Now wire it all together. Create a cron job that runs every 2 hours:
[code] 
    hermes cron create "0 */2 * * *" \  
      "Check for new open PRs and review them.  
      
    Repos to monitor:  
    - myorg/backend-api  
    - myorg/frontend-app  
      
    Steps:  
    1. Run: gh pr list --repo REPO --state open --limit 5 --json number,title,author,createdAt  
    2. For each PR created or updated in the last 4 hours:  
       - Run: gh pr diff NUMBER --repo REPO  
       - Review the diff using the code-review guidelines  
    3. Format output as:  
      
    ## PR Reviews — today  
      
    ### [repo] #[number]: [title]  
    **Author:** [name] | **Verdict:** APPROVE/REQUEST_CHANGES/COMMENT  
    [findings]  
      
    If no new PRs found, say: No new PRs to review." \  
      --name "pr-review" \  
      --deliver telegram \  
      --skill code-review  
    
[/code]
Verify it's scheduled:
[code] 
    hermes cron list  
    
[/code]
### Other useful schedules[​](<#other-useful-schedules> "Direct link to Other useful schedules")
Schedule| When  
---|---  
`0 */2 * * *`| Every 2 hours  
`0 9,13,17 * * 1-5`| Three times a day, weekdays only  
`0 9 * * 1`| Weekly Monday morning roundup  
`30m`| Every 30 minutes (high-traffic repos)  
* * *
## Step 6: Run It On Demand[​](<#step-6-run-it-on-demand> "Direct link to Step 6: Run It On Demand")
Don't want to wait for the schedule? Trigger it manually:
[code] 
    hermes cron run pr-review  
    
[/code]
Or from within a chat session:
[code] 
    /cron run pr-review  
    
[/code]
* * *
## Going Further[​](<#going-further> "Direct link to Going Further")
### Post Reviews Directly to GitHub[​](<#post-reviews-directly-to-github> "Direct link to Post Reviews Directly to GitHub")
Instead of delivering to Telegram, have the agent comment on the PR itself:
Add this to your cron prompt:
[code] 
    After reviewing, post your review:  
    - For issues: gh pr review NUMBER --repo REPO --comment --body "YOUR_REVIEW"  
    - For critical issues: gh pr review NUMBER --repo REPO --request-changes --body "YOUR_REVIEW"  
    - For clean PRs: gh pr review NUMBER --repo REPO --approve --body "Looks good"  
    
[/code]
caution
Make sure `gh` has a token with `repo` scope. Reviews are posted as whoever `gh` is authenticated as.
### Weekly PR Dashboard[​](<#weekly-pr-dashboard> "Direct link to Weekly PR Dashboard")
Create a Monday morning overview of all your repos:
[code] 
    hermes cron create "0 9 * * 1" \  
      "Generate a weekly PR dashboard:  
    - myorg/backend-api  
    - myorg/frontend-app  
    - myorg/infra  
      
    For each repo show:  
    1. Open PR count and oldest PR age  
    2. PRs merged this week  
    3. Stale PRs (older than 5 days)  
    4. PRs with no reviewer assigned  
      
    Format as a clean summary." \  
      --name "weekly-dashboard" \  
      --deliver telegram  
    
[/code]
### Multi-Repo Monitoring[​](<#multi-repo-monitoring> "Direct link to Multi-Repo Monitoring")
Scale up by adding more repos to the prompt. The agent processes them sequentially — no extra setup needed.
* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### "gh: command not found"[​](<#gh-command-not-found> "Direct link to "gh: command not found"")
The gateway runs in a minimal environment. Ensure `gh` is in the system PATH and restart the gateway.
### Reviews are too generic[​](<#reviews-are-too-generic> "Direct link to Reviews are too generic")
  1. Add the `code-review` skill (Step 3)
  2. Teach Hermes your conventions via memory (Step 4)
  3. The more context it has about your stack, the better the reviews


### Cron job doesn't run[​](<#cron-job-doesnt-run> "Direct link to Cron job doesn't run")
[code] 
    hermes gateway status    # Is the gateway running?  
    hermes cron list         # Is the job enabled?  
    
[/code]
### Rate limits[​](<#rate-limits> "Direct link to Rate limits")
GitHub allows 5,000 API requests/hour for authenticated users. Each PR review uses ~3-5 requests (list + diff + optional comments). Even reviewing 100 PRs/day stays well within limits.
* * *
## What's Next?[​](<#whats-next> "Direct link to What's Next?")
  * **[Webhook-Based PR Reviews](</docs/guides/webhook-github-pr-review>)** — get instant reviews when PRs are opened (requires a public endpoint)
  * **[Daily Briefing Bot](</docs/guides/daily-briefing-bot>)** — combine PR reviews with your morning news digest
  * **[Build a Plugin](</docs/guides/build-a-hermes-plugin>)** — wrap the review logic into a shareable plugin
  * **[Profiles](</docs/user-guide/profiles>)** — run a dedicated reviewer profile with its own memory and config
  * **[Fallback Providers](</docs/user-guide/features/fallback-providers>)** — ensure reviews run even when one provider is down


  * [Prerequisites](<#prerequisites>)
  * [Step 1: Verify the Setup](<#step-1-verify-the-setup>)
  * [Step 2: Try a Manual Review](<#step-2-try-a-manual-review>)
  * [Step 3: Create a Review Skill](<#step-3-create-a-review-skill>)
  * [Step 4: Teach It Your Conventions](<#step-4-teach-it-your-conventions>)
  * [Step 5: Create the Automated Cron Job](<#step-5-create-the-automated-cron-job>)
    * [Other useful schedules](<#other-useful-schedules>)
  * [Step 6: Run It On Demand](<#step-6-run-it-on-demand>)
  * [Going Further](<#going-further>)
    * [Post Reviews Directly to GitHub](<#post-reviews-directly-to-github>)
    * [Weekly PR Dashboard](<#weekly-pr-dashboard>)
    * [Multi-Repo Monitoring](<#multi-repo-monitoring>)
  * [Troubleshooting](<#troubleshooting>)
    * ["gh: command not found"](<#gh-command-not-found>)
    * [Reviews are too generic](<#reviews-are-too-generic>)
    * [Cron job doesn't run](<#cron-job-doesnt-run>)
    * [Rate limits](<#rate-limits>)
  * [What's Next?](<#whats-next>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent -->
