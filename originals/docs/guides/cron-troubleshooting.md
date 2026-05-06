On this page
When a cron job isn't behaving as expected, work through these checks in order. Most issues fall into one of four categories: timing, delivery, permissions, or skill loading.
* * *
## Jobs Not Firing[​](<#jobs-not-firing> "Direct link to Jobs Not Firing")
### Check 1: Verify the job exists and is active[​](<#check-1-verify-the-job-exists-and-is-active> "Direct link to Check 1: Verify the job exists and is active")
[code] 
    hermes cron list  
    
[/code]
Look for the job and confirm its state is `[active]` (not `[paused]` or `[completed]`). If it shows `[completed]`, the repeat count may be exhausted — edit the job to reset it.
### Check 2: Confirm the schedule is correct[​](<#check-2-confirm-the-schedule-is-correct> "Direct link to Check 2: Confirm the schedule is correct")
A misformatted schedule silently defaults to one-shot or is rejected entirely. Test your expression:
Your expression| Should evaluate to  
---|---  
`0 9 * * *`| 9:00 AM every day  
`0 9 * * 1`| 9:00 AM every Monday  
`every 2h`| Every 2 hours from now  
`30m`| 30 minutes from now  
`2025-06-01T09:00:00`| June 1, 2025 at 9:00 AM UTC  
If the job fires once and then disappears from the list, it's a one-shot schedule (`30m`, `1d`, or an ISO timestamp) — expected behavior.
### Check 3: Is the gateway running?[​](<#check-3-is-the-gateway-running> "Direct link to Check 3: Is the gateway running?")
Cron jobs are fired by the gateway's background ticker thread, which ticks every 60 seconds. A regular CLI chat session does **not** automatically fire cron jobs.
If you're expecting jobs to fire automatically, you need a running gateway (`hermes gateway` or `hermes serve`). For one-off debugging, you can manually trigger a tick with `hermes cron tick`.
### Check 4: Check the system clock and timezone[​](<#check-4-check-the-system-clock-and-timezone> "Direct link to Check 4: Check the system clock and timezone")
Jobs use the local timezone. If your machine's clock is wrong or in a different timezone than expected, jobs will fire at the wrong times. Verify:
[code] 
    date  
    hermes cron list   # Compare next_run times with local time  
    
[/code]
* * *
## Delivery Failures[​](<#delivery-failures> "Direct link to Delivery Failures")
### Check 1: Verify the deliver target is correct[​](<#check-1-verify-the-deliver-target-is-correct> "Direct link to Check 1: Verify the deliver target is correct")
Delivery targets are case-sensitive and require the correct platform to be configured. A misconfigured target silently drops the response.
Target| Requires  
---|---  
`telegram`| `TELEGRAM_BOT_TOKEN` in `~/.hermes/.env`  
`discord`| `DISCORD_BOT_TOKEN` in `~/.hermes/.env`  
`slack`| `SLACK_BOT_TOKEN` in `~/.hermes/.env`  
`whatsapp`| WhatsApp gateway configured  
`signal`| Signal gateway configured  
`matrix`| Matrix homeserver configured  
`email`| SMTP configured in `config.yaml`  
`sms`| SMS provider configured  
`local`| Write access to `~/.hermes/cron/output/`  
`origin`| Delivers to the chat where the job was created  
Other supported platforms include `mattermost`, `homeassistant`, `dingtalk`, `feishu`, `wecom`, `weixin`, `bluebubbles`, `qqbot`, and `webhook`. You can also target a specific chat with `platform:chat_id` syntax (e.g., `telegram:-1001234567890`).
If delivery fails, the job still runs — it just won't send anywhere. Check `hermes cron list` for updated `last_error` field (if available).
### Check 2: Check `[SILENT]` usage[​](<#check-2-check-silent-usage> "Direct link to check-2-check-silent-usage")
If your cron job produces no output or the agent responds with `[SILENT]`, delivery is suppressed. This is intentional for monitoring jobs — but make sure your prompt isn't accidentally suppressing everything.
A prompt that says "respond with [SILENT] if nothing changed" will silently swallow non-empty responses too. Check your conditional logic.
### Check 3: Platform token permissions[​](<#check-3-platform-token-permissions> "Direct link to Check 3: Platform token permissions")
Each messaging platform bot needs specific permissions to receive messages. If delivery silently fails:
  * **Telegram** : Bot must be an admin in the target group/channel
  * **Discord** : Bot must have permission to send in the target channel
  * **Slack** : Bot must be added to the workspace and have `chat:write` scope


### Check 4: Response wrapping[​](<#check-4-response-wrapping> "Direct link to Check 4: Response wrapping")
By default, cron responses are wrapped with a header and footer (`cron.wrap_response: true` in `config.yaml`). Some platforms or integrations may not handle this well. To disable:
[code] 
    cron:  
      wrap_response: false  
    
[/code]
* * *
## Skill Loading Failures[​](<#skill-loading-failures> "Direct link to Skill Loading Failures")
### Check 1: Verify skills are installed[​](<#check-1-verify-skills-are-installed> "Direct link to Check 1: Verify skills are installed")
[code] 
    hermes skills list  
    
[/code]
Skills must be installed before they can be attached to cron jobs. If a skill is missing, install it first with `hermes skills install <skill-name>` or via `/skills` in the CLI.
### Check 2: Check skill name vs. skill folder name[​](<#check-2-check-skill-name-vs-skill-folder-name> "Direct link to Check 2: Check skill name vs. skill folder name")
Skill names are case-sensitive and must match the installed skill's folder name. If your job specifies `ai-funding-daily-report` but the skill folder is `ai-funding-daily-report`, confirm the exact name from `hermes skills list`.
### Check 3: Skills that require interactive tools[​](<#check-3-skills-that-require-interactive-tools> "Direct link to Check 3: Skills that require interactive tools")
Cron jobs run with the `cronjob`, `messaging`, and `clarify` toolsets disabled. This prevents recursive cron creation, direct message sending (delivery is handled by the scheduler), and interactive prompts. If a skill relies on these toolsets, it won't work in a cron context.
Check the skill's documentation to confirm it works in non-interactive (headless) mode.
### Check 4: Multi-skill ordering[​](<#check-4-multi-skill-ordering> "Direct link to Check 4: Multi-skill ordering")
When using multiple skills, they load in order. If Skill A depends on context from Skill B, make sure B loads first:
[code] 
    /cron add "0 9 * * *" "..." --skill context-skill --skill target-skill  
    
[/code]
In this example, `context-skill` loads before `target-skill`.
* * *
## Job Errors and Failures[​](<#job-errors-and-failures> "Direct link to Job Errors and Failures")
### Check 1: Review recent job output[​](<#check-1-review-recent-job-output> "Direct link to Check 1: Review recent job output")
If a job ran and failed, you may see error context in:
  1. The chat where the job delivers (if delivery succeeded)
  2. `~/.hermes/logs/agent.log` for scheduler messages (or `errors.log` for warnings)
  3. The job's `last_run` metadata via `hermes cron list`


### Check 2: Common error patterns[​](<#check-2-common-error-patterns> "Direct link to Check 2: Common error patterns")
**"No such file or directory" for scripts** The `script` path must be an absolute path (or relative to the Hermes config directory). Verify:
[code] 
    ls ~/.hermes/scripts/your-script.py   # Must exist  
    hermes cron edit <job_id> --script ~/.hermes/scripts/your-script.py  
    
[/code]
**"Skill not found" at job execution** The skill must be installed on the machine running the scheduler. If you move between machines, skills don't automatically sync — reinstall them with `hermes skills install <skill-name>`.
**Job runs but delivers nothing** Likely a delivery target issue (see Delivery Failures above) or a silently suppressed response (`[SILENT]`).
**Job hangs or times out** The scheduler uses an inactivity-based timeout (default 600s, configurable via `HERMES_CRON_TIMEOUT` env var, `0` for unlimited). The agent can run as long as it's actively calling tools — the timer only fires after sustained inactivity. Long-running jobs should use scripts to handle data collection and deliver only the result.
### Check 3: Lock contention[​](<#check-3-lock-contention> "Direct link to Check 3: Lock contention")
The scheduler uses file-based locking to prevent overlapping ticks. If two gateway instances are running (or a CLI session conflicts with a gateway), jobs may be delayed or skipped.
Kill duplicate gateway processes:
[code] 
    ps aux | grep hermes  
    # Kill duplicate processes, keep only one  
    
[/code]
### Check 4: Permissions on jobs.json[​](<#check-4-permissions-on-jobsjson> "Direct link to Check 4: Permissions on jobs.json")
Jobs are stored in `~/.hermes/cron/jobs.json`. If this file is not readable/writable by your user, the scheduler will fail silently:
[code] 
    ls -la ~/.hermes/cron/jobs.json  
    chmod 600 ~/.hermes/cron/jobs.json   # Your user should own it  
    
[/code]
* * *
## Performance Issues[​](<#performance-issues> "Direct link to Performance Issues")
### Slow job startup[​](<#slow-job-startup> "Direct link to Slow job startup")
Each cron job creates a fresh AIAgent session, which may involve provider authentication and model loading. For time-sensitive schedules, add buffer time (e.g., `0 8 * * *` instead of `0 9 * * *`).
### Too many overlapping jobs[​](<#too-many-overlapping-jobs> "Direct link to Too many overlapping jobs")
The scheduler executes jobs sequentially within each tick. If multiple jobs are due at the same time, they run one after another. Consider staggering schedules (e.g., `0 9 * * *` and `5 9 * * *` instead of both at `0 9 * * *`) to avoid delays.
### Large script output[​](<#large-script-output> "Direct link to Large script output")
Scripts that dump megabytes of output will slow down the agent and may hit token limits. Filter/summarize at the script level — emit only what the agent needs to reason about.
* * *
## Diagnostic Commands[​](<#diagnostic-commands> "Direct link to Diagnostic Commands")
[code] 
    hermes cron list                    # Show all jobs, states, next_run times  
    hermes cron run <job_id>            # Schedule for next tick (for testing)  
    hermes cron edit <job_id>           # Fix configuration issues  
    hermes logs                         # View recent Hermes logs  
    hermes skills list                  # Verify installed skills  
    
[/code]
* * *
## Getting More Help[​](<#getting-more-help> "Direct link to Getting More Help")
If you've worked through this guide and the issue persists:
  1. Run the job with `hermes cron run <job_id>` (fires on next gateway tick) and watch for errors in the chat output
  2. Check `~/.hermes/logs/agent.log` for scheduler messages and `~/.hermes/logs/errors.log` for warnings
  3. Open an issue at [github.com/NousResearch/hermes-agent](<https://github.com/NousResearch/hermes-agent>) with:
     * The job ID and schedule
     * The delivery target
     * What you expected vs. what happened
     * Relevant error messages from the logs


* * *
_For the complete cron reference, see[Automate Anything with Cron](</docs/guides/automate-with-cron>) and [Scheduled Tasks (Cron)](</docs/user-guide/features/cron>)._
  * [Jobs Not Firing](<#jobs-not-firing>)
    * [Check 1: Verify the job exists and is active](<#check-1-verify-the-job-exists-and-is-active>)
    * [Check 2: Confirm the schedule is correct](<#check-2-confirm-the-schedule-is-correct>)
    * [Check 3: Is the gateway running?](<#check-3-is-the-gateway-running>)
    * [Check 4: Check the system clock and timezone](<#check-4-check-the-system-clock-and-timezone>)
  * [Delivery Failures](<#delivery-failures>)
    * [Check 1: Verify the deliver target is correct](<#check-1-verify-the-deliver-target-is-correct>)
    * [Check 2: Check `[SILENT]` usage](<#check-2-check-silent-usage>)
    * [Check 3: Platform token permissions](<#check-3-platform-token-permissions>)
    * [Check 4: Response wrapping](<#check-4-response-wrapping>)
  * [Skill Loading Failures](<#skill-loading-failures>)
    * [Check 1: Verify skills are installed](<#check-1-verify-skills-are-installed>)
    * [Check 2: Check skill name vs. skill folder name](<#check-2-check-skill-name-vs-skill-folder-name>)
    * [Check 3: Skills that require interactive tools](<#check-3-skills-that-require-interactive-tools>)
    * [Check 4: Multi-skill ordering](<#check-4-multi-skill-ordering>)
  * [Job Errors and Failures](<#job-errors-and-failures>)
    * [Check 1: Review recent job output](<#check-1-review-recent-job-output>)
    * [Check 2: Common error patterns](<#check-2-common-error-patterns>)
    * [Check 3: Lock contention](<#check-3-lock-contention>)
    * [Check 4: Permissions on jobs.json](<#check-4-permissions-on-jobsjson>)
  * [Performance Issues](<#performance-issues>)
    * [Slow job startup](<#slow-job-startup>)
    * [Too many overlapping jobs](<#too-many-overlapping-jobs>)
    * [Large script output](<#large-script-output>)
  * [Diagnostic Commands](<#diagnostic-commands>)
  * [Getting More Help](<#getting-more-help>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/cron-troubleshooting -->
