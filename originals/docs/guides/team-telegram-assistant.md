On this page
This tutorial walks you through setting up a Telegram bot powered by Hermes Agent that multiple team members can use. By the end, your team will have a shared AI assistant they can message for help with code, research, system administration, and anything else — secured with per-user authorization.
## What We're Building[​](<#what-were-building> "Direct link to What We're Building")
A Telegram bot that:
  * **Any authorized team member** can DM for help — code reviews, research, shell commands, debugging
  * **Runs on your server** with full tool access — terminal, file editing, web search, code execution
  * **Per-user sessions** — each person gets their own conversation context
  * **Secure by default** — only approved users can interact, with two authorization methods
  * **Scheduled tasks** — daily standups, health checks, and reminders delivered to a team channel


* * *
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
Before starting, make sure you have:
  * **Hermes Agent installed** on a server or VPS (not your laptop — the bot needs to stay running). Follow the [installation guide](</docs/getting-started/installation>) if you haven't yet.
  * **A Telegram account** for yourself (the bot owner)
  * **An LLM provider configured** — at minimum, an API key for OpenAI, Anthropic, or another supported provider in `~/.hermes/.env`


tip
A $5/month VPS is plenty for running the gateway. Hermes itself is lightweight — the LLM API calls are what cost money, and those happen remotely.
* * *
## Step 1: Create a Telegram Bot[​](<#step-1-create-a-telegram-bot> "Direct link to Step 1: Create a Telegram Bot")
Every Telegram bot starts with **@BotFather** — Telegram's official bot for creating bots.
  1. **Open Telegram** and search for `@BotFather`, or go to [t.me/BotFather](<https://t.me/BotFather>)
  2. **Send`/newbot`** — BotFather will ask you two things:
     * **Display name** — what users see (e.g., `Team Hermes Assistant`)
     * **Username** — must end in `bot` (e.g., `myteam_hermes_bot`)
  3. **Copy the bot token** — BotFather replies with something like:
[code] Use this token to access the HTTP API:  
         7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...  
         
[/code]
Save this token — you'll need it in the next step.
  4. **Set a description** (optional but recommended):
[code] /setdescription  
         
[/code]
Choose your bot, then enter something like:
[code] Team AI assistant powered by Hermes Agent. DM me for help with code, research, debugging, and more.  
         
[/code]
  5. **Set bot commands** (optional — gives users a command menu):
[code] /setcommands  
         
[/code]
Choose your bot, then paste:
[code] new - Start a fresh conversation  
         model - Show or change the AI model  
         status - Show session info  
         help - Show available commands  
         stop - Stop the current task  
         
[/code]


warning
Keep your bot token secret. Anyone with the token can control the bot. If it leaks, use `/revoke` in BotFather to generate a new one.
* * *
## Step 2: Configure the Gateway[​](<#step-2-configure-the-gateway> "Direct link to Step 2: Configure the Gateway")
You have two options: the interactive setup wizard (recommended) or manual configuration.
### Option A: Interactive Setup (Recommended)[​](<#option-a-interactive-setup-recommended> "Direct link to Option A: Interactive Setup \(Recommended\)")
[code] 
    hermes gateway setup  
    
[/code]
This walks you through everything with arrow-key selection. Pick **Telegram** , paste your bot token, and enter your user ID when prompted.
### Option B: Manual Configuration[​](<#option-b-manual-configuration> "Direct link to Option B: Manual Configuration")
Add these lines to `~/.hermes/.env`:
[code] 
    # Telegram bot token from BotFather  
    TELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...  
      
    # Your Telegram user ID (numeric)  
    TELEGRAM_ALLOWED_USERS=123456789  
    
[/code]
### Finding Your User ID[​](<#finding-your-user-id> "Direct link to Finding Your User ID")
Your Telegram user ID is a numeric value (not your username). To find it:
  1. Message [@userinfobot](<https://t.me/userinfobot>) on Telegram
  2. It instantly replies with your numeric user ID
  3. Copy that number into `TELEGRAM_ALLOWED_USERS`


info
Telegram user IDs are permanent numbers like `123456789`. They're different from your `@username`, which can change. Always use the numeric ID for allowlists.
* * *
## Step 3: Start the Gateway[​](<#step-3-start-the-gateway> "Direct link to Step 3: Start the Gateway")
### Quick Test[​](<#quick-test> "Direct link to Quick Test")
Run the gateway in the foreground first to make sure everything works:
[code] 
    hermes gateway  
    
[/code]
You should see output like:
[code] 
    [Gateway] Starting Hermes Gateway...  
    [Gateway] Telegram adapter connected  
    [Gateway] Cron scheduler started (tick every 60s)  
    
[/code]
Open Telegram, find your bot, and send it a message. If it replies, you're in business. Press `Ctrl+C` to stop.
### Production: Install as a Service[​](<#production-install-as-a-service> "Direct link to Production: Install as a Service")
For a persistent deployment that survives reboots:
[code] 
    hermes gateway install  
    sudo hermes gateway install --system   # Linux only: boot-time system service  
    
[/code]
This creates a background service: a user-level **systemd** service on Linux by default, a **launchd** service on macOS, or a boot-time Linux system service if you pass `--system`.
[code] 
    # Linux — manage the default user service  
    hermes gateway start  
    hermes gateway stop  
    hermes gateway status  
      
    # View live logs  
    journalctl --user -u hermes-gateway -f  
      
    # Keep running after SSH logout  
    sudo loginctl enable-linger $USER  
      
    # Linux servers — explicit system-service commands  
    sudo hermes gateway start --system  
    sudo hermes gateway status --system  
    journalctl -u hermes-gateway -f  
    
[/code]
[code] 
    # macOS — manage the service  
    hermes gateway start  
    hermes gateway stop  
    tail -f ~/.hermes/logs/gateway.log  
    
[/code]
macOS PATH
The launchd plist captures your shell PATH at install time so gateway subprocesses can find tools like Node.js and ffmpeg. If you install new tools later, re-run `hermes gateway install` to update the plist.
### Verify It's Running[​](<#verify-its-running> "Direct link to Verify It's Running")
[code] 
    hermes gateway status  
    
[/code]
Then send a test message to your bot on Telegram. You should get a response within a few seconds.
* * *
## Step 4: Set Up Team Access[​](<#step-4-set-up-team-access> "Direct link to Step 4: Set Up Team Access")
Now let's give your teammates access. There are two approaches.
### Approach A: Static Allowlist[​](<#approach-a-static-allowlist> "Direct link to Approach A: Static Allowlist")
Collect each team member's Telegram user ID (have them message [@userinfobot](<https://t.me/userinfobot>)) and add them as a comma-separated list:
[code] 
    # In ~/.hermes/.env  
    TELEGRAM_ALLOWED_USERS=123456789,987654321,555555555  
    
[/code]
Restart the gateway after changes:
[code] 
    hermes gateway stop && hermes gateway start  
    
[/code]
### Approach B: DM Pairing (Recommended for Teams)[​](<#approach-b-dm-pairing-recommended-for-teams> "Direct link to Approach B: DM Pairing \(Recommended for Teams\)")
DM pairing is more flexible — you don't need to collect user IDs upfront. Here's how it works:
  1. **Teammate DMs the bot** — since they're not on the allowlist, the bot replies with a one-time pairing code:
[code] 🔐 Pairing code: XKGH5N7P  
         Send this code to the bot owner for approval.  
         
[/code]
  2. **Teammate sends you the code** (via any channel — Slack, email, in person)
  3. **You approve it** on the server:
[code] hermes pairing approve telegram XKGH5N7P  
         
[/code]
  4. **They're in** — the bot immediately starts responding to their messages


**Managing paired users:**
[code] 
    # See all pending and approved users  
    hermes pairing list  
      
    # Revoke someone's access  
    hermes pairing revoke telegram 987654321  
      
    # Clear expired pending codes  
    hermes pairing clear-pending  
    
[/code]
tip
DM pairing is ideal for teams because you don't need to restart the gateway when adding new users. Approvals take effect immediately.
### Security Considerations[​](<#security-considerations> "Direct link to Security Considerations")
  * **Never set`GATEWAY_ALLOW_ALL_USERS=true`** on a bot with terminal access — anyone who finds your bot could run commands on your server
  * Pairing codes expire after **1 hour** and use cryptographic randomness
  * Rate limiting prevents brute-force attacks: 1 request per user per 10 minutes, max 3 pending codes per platform
  * After 5 failed approval attempts, the platform enters a 1-hour lockout
  * All pairing data is stored with `chmod 0600` permissions


* * *
## Step 5: Configure the Bot[​](<#step-5-configure-the-bot> "Direct link to Step 5: Configure the Bot")
### Set a Home Channel[​](<#set-a-home-channel> "Direct link to Set a Home Channel")
A **home channel** is where the bot delivers cron job results and proactive messages. Without one, scheduled tasks have nowhere to send output.
**Option 1:** Use the `/sethome` command in any Telegram group or chat where the bot is a member.
**Option 2:** Set it manually in `~/.hermes/.env`:
[code] 
    TELEGRAM_HOME_CHANNEL=-1001234567890  
    TELEGRAM_HOME_CHANNEL_NAME="Team Updates"  
    
[/code]
To find a channel ID, add [@userinfobot](<https://t.me/userinfobot>) to the group — it will report the group's chat ID.
### Configure Tool Progress Display[​](<#configure-tool-progress-display> "Direct link to Configure Tool Progress Display")
Control how much detail the bot shows when using tools. In `~/.hermes/config.yaml`:
[code] 
    display:  
      tool_progress: new    # off | new | all | verbose  
    
[/code]
Mode| What You See  
---|---  
`off`| Clean responses only — no tool activity  
`new`| Brief status for each new tool call (recommended for messaging)  
`all`| Every tool call with details  
`verbose`| Full tool output including command results  
Users can also change this per-session with the `/verbose` command in chat.
### Set Up a Personality with SOUL.md[​](<#set-up-a-personality-with-soulmd> "Direct link to Set Up a Personality with SOUL.md")
Customize how the bot communicates by editing `~/.hermes/SOUL.md`:
For a full guide, see [Use SOUL.md with Hermes](</docs/guides/use-soul-with-hermes>).
[code] 
    # Soul  
    You are a helpful team assistant. Be concise and technical.  
    Use code blocks for any code. Skip pleasantries — the team  
    values directness. When debugging, always ask for error logs  
    before guessing at solutions.  
    
[/code]
### Add Project Context[​](<#add-project-context> "Direct link to Add Project Context")
If your team works on specific projects, create context files so the bot knows your stack:
[code] 
    <!-- ~/.hermes/AGENTS.md -->  
    # Team Context  
    - We use Python 3.12 with FastAPI and SQLAlchemy  
    - Frontend is React with TypeScript  
    - CI/CD runs on GitHub Actions  
    - Production deploys to AWS ECS  
    - Always suggest writing tests for new code  
    
[/code]
info
Context files are injected into every session's system prompt. Keep them concise — every character counts against your token budget.
* * *
## Step 6: Set Up Scheduled Tasks[​](<#step-6-set-up-scheduled-tasks> "Direct link to Step 6: Set Up Scheduled Tasks")
With the gateway running, you can schedule recurring tasks that deliver results to your team channel.
### Daily Standup Summary[​](<#daily-standup-summary> "Direct link to Daily Standup Summary")
Message the bot on Telegram:
[code] 
    Every weekday at 9am, check the GitHub repository at  
    github.com/myorg/myproject for:  
    1. Pull requests opened/merged in the last 24 hours  
    2. Issues created or closed  
    3. Any CI/CD failures on the main branch  
    Format as a brief standup-style summary.  
    
[/code]
The agent creates a cron job automatically and delivers results to the chat where you asked (or the home channel).
### Server Health Check[​](<#server-health-check> "Direct link to Server Health Check")
[code] 
    Every 6 hours, check disk usage with 'df -h', memory with 'free -h',  
    and Docker container status with 'docker ps'. Report anything unusual —  
    partitions above 80%, containers that have restarted, or high memory usage.  
    
[/code]
### Managing Scheduled Tasks[​](<#managing-scheduled-tasks> "Direct link to Managing Scheduled Tasks")
[code] 
    # From the CLI  
    hermes cron list          # View all scheduled jobs  
    hermes cron status        # Check if scheduler is running  
      
    # From Telegram chat  
    /cron list                # View jobs  
    /cron remove <job_id>     # Remove a job  
    
[/code]
warning
Cron job prompts run in completely fresh sessions with no memory of prior conversations. Make sure each prompt contains **all** the context the agent needs — file paths, URLs, server addresses, and clear instructions.
* * *
## Production Tips[​](<#production-tips> "Direct link to Production Tips")
### Use Docker for Safety[​](<#use-docker-for-safety> "Direct link to Use Docker for Safety")
On a shared team bot, use Docker as the terminal backend so agent commands run in a container instead of on your host:
[code] 
    # In ~/.hermes/.env  
    TERMINAL_BACKEND=docker  
    TERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20  
    
[/code]
Or in `~/.hermes/config.yaml`:
[code] 
    terminal:  
      backend: docker  
      container_cpu: 1  
      container_memory: 5120  
      container_persistent: true  
    
[/code]
This way, even if someone asks the bot to run something destructive, your host system is protected.
### Monitor the Gateway[​](<#monitor-the-gateway> "Direct link to Monitor the Gateway")
[code] 
    # Check if the gateway is running  
    hermes gateway status  
      
    # Watch live logs (Linux)  
    journalctl --user -u hermes-gateway -f  
      
    # Watch live logs (macOS)  
    tail -f ~/.hermes/logs/gateway.log  
    
[/code]
### Keep Hermes Updated[​](<#keep-hermes-updated> "Direct link to Keep Hermes Updated")
From Telegram, send `/update` to the bot — it will pull the latest version and restart. Or from the server:
[code] 
    hermes update  
    hermes gateway stop && hermes gateway start  
    
[/code]
### Log Locations[​](<#log-locations> "Direct link to Log Locations")
What| Location  
---|---  
Gateway logs| `journalctl --user -u hermes-gateway` (Linux) or `~/.hermes/logs/gateway.log` (macOS)  
Cron job output| `~/.hermes/cron/output/{job_id}/{timestamp}.md`  
Cron job definitions| `~/.hermes/cron/jobs.json`  
Pairing data| `~/.hermes/pairing/`  
Session history| `~/.hermes/sessions/`  
* * *
## Going Further[​](<#going-further> "Direct link to Going Further")
You've got a working team Telegram assistant. Here are some next steps:
  * **[Security Guide](</docs/user-guide/security>)** — deep dive into authorization, container isolation, and command approval
  * **[Messaging Gateway](</docs/user-guide/messaging>)** — full reference for gateway architecture, session management, and chat commands
  * **[Telegram Setup](</docs/user-guide/messaging/telegram>)** — platform-specific details including voice messages and TTS
  * **[Scheduled Tasks](</docs/user-guide/features/cron>)** — advanced cron scheduling with delivery options and cron expressions
  * **[Context Files](</docs/user-guide/features/context-files>)** — AGENTS.md, SOUL.md, and .cursorrules for project knowledge
  * **[Personality](</docs/user-guide/features/personality>)** — built-in personality presets and custom persona definitions
  * **Add more platforms** — the same gateway can simultaneously run [Discord](</docs/user-guide/messaging/discord>), [Slack](</docs/user-guide/messaging/slack>), and [WhatsApp](</docs/user-guide/messaging/whatsapp>)


* * *
_Questions or issues? Open an issue on GitHub — contributions are welcome._
  * [What We're Building](<#what-were-building>)
  * [Prerequisites](<#prerequisites>)
  * [Step 1: Create a Telegram Bot](<#step-1-create-a-telegram-bot>)
  * [Step 2: Configure the Gateway](<#step-2-configure-the-gateway>)
    * [Option A: Interactive Setup (Recommended)](<#option-a-interactive-setup-recommended>)
    * [Option B: Manual Configuration](<#option-b-manual-configuration>)
    * [Finding Your User ID](<#finding-your-user-id>)
  * [Step 3: Start the Gateway](<#step-3-start-the-gateway>)
    * [Quick Test](<#quick-test>)
    * [Production: Install as a Service](<#production-install-as-a-service>)
    * [Verify It's Running](<#verify-its-running>)
  * [Step 4: Set Up Team Access](<#step-4-set-up-team-access>)
    * [Approach A: Static Allowlist](<#approach-a-static-allowlist>)
    * [Approach B: DM Pairing (Recommended for Teams)](<#approach-b-dm-pairing-recommended-for-teams>)
    * [Security Considerations](<#security-considerations>)
  * [Step 5: Configure the Bot](<#step-5-configure-the-bot>)
    * [Set a Home Channel](<#set-a-home-channel>)
    * [Configure Tool Progress Display](<#configure-tool-progress-display>)
    * [Set Up a Personality with SOUL.md](<#set-up-a-personality-with-soulmd>)
    * [Add Project Context](<#add-project-context>)
  * [Step 6: Set Up Scheduled Tasks](<#step-6-set-up-scheduled-tasks>)
    * [Daily Standup Summary](<#daily-standup-summary>)
    * [Server Health Check](<#server-health-check>)
    * [Managing Scheduled Tasks](<#managing-scheduled-tasks>)
  * [Production Tips](<#production-tips>)
    * [Use Docker for Safety](<#use-docker-for-safety>)
    * [Monitor the Gateway](<#monitor-the-gateway>)
    * [Keep Hermes Updated](<#keep-hermes-updated>)
    * [Log Locations](<#log-locations>)
  * [Going Further](<#going-further>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant -->
