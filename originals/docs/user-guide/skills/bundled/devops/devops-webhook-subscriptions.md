On this page
Webhook subscriptions: event-driven agent runs.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/devops/webhook-subscriptions`  
Version| `1.1.0`  
Tags| `webhook`, `events`, `automation`, `integrations`, `notifications`, `push`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Webhook Subscriptions
Create dynamic webhook subscriptions so external services (GitHub, GitLab, Stripe, CI/CD, IoT sensors, monitoring tools) can trigger Hermes agent runs by POSTing events to a URL.
## Setup (Required First)[​](<#setup-required-first> "Direct link to Setup \(Required First\)")
The webhook platform must be enabled before subscriptions can be created. Check with:
[code] 
    hermes webhook list  
    
[/code]
If it says "Webhook platform is not enabled", set it up:
### Option 1: Setup wizard[​](<#option-1-setup-wizard> "Direct link to Option 1: Setup wizard")
[code] 
    hermes gateway setup  
    
[/code]
Follow the prompts to enable webhooks, set the port, and set a global HMAC secret.
### Option 2: Manual config[​](<#option-2-manual-config> "Direct link to Option 2: Manual config")
Add to `~/.hermes/config.yaml`:
[code] 
    platforms:  
      webhook:  
        enabled: true  
        extra:  
          host: "0.0.0.0"  
          port: 8644  
          secret: "generate-a-strong-secret-here"  
    
[/code]
### Option 3: Environment variables[​](<#option-3-environment-variables> "Direct link to Option 3: Environment variables")
Add to `~/.hermes/.env`:
[code] 
    WEBHOOK_ENABLED=true  
    WEBHOOK_PORT=8644  
    WEBHOOK_SECRET=generate-a-strong-secret-here  
    
[/code]
After configuration, start (or restart) the gateway:
[code] 
    hermes gateway run  
    # Or if using systemd:  
    systemctl --user restart hermes-gateway  
    
[/code]
Verify it's running:
[code] 
    curl http://localhost:8644/health  
    
[/code]
## Commands[​](<#commands> "Direct link to Commands")
All management is via the `hermes webhook` CLI command:
### Create a subscription[​](<#create-a-subscription> "Direct link to Create a subscription")
[code] 
    hermes webhook subscribe <name> \  
      --prompt "Prompt template with {payload.fields}" \  
      --events "event1,event2" \  
      --description "What this does" \  
      --skills "skill1,skill2" \  
      --deliver telegram \  
      --deliver-chat-id "12345" \  
      --secret "optional-custom-secret"  
    
[/code]
Returns the webhook URL and HMAC secret. The user configures their service to POST to that URL.
### List subscriptions[​](<#list-subscriptions> "Direct link to List subscriptions")
[code] 
    hermes webhook list  
    
[/code]
### Remove a subscription[​](<#remove-a-subscription> "Direct link to Remove a subscription")
[code] 
    hermes webhook remove <name>  
    
[/code]
### Test a subscription[​](<#test-a-subscription> "Direct link to Test a subscription")
[code] 
    hermes webhook test <name>  
    hermes webhook test <name> --payload '{"key": "value"}'  
    
[/code]
## Prompt Templates[​](<#prompt-templates> "Direct link to Prompt Templates")
Prompts support `{dot.notation}` for accessing nested payload fields:
  * `{issue.title}` — GitHub issue title
  * `{pull_request.user.login}` — PR author
  * `{data.object.amount}` — Stripe payment amount
  * `{sensor.temperature}` — IoT sensor reading


If no prompt is specified, the full JSON payload is dumped into the agent prompt.
## Common Patterns[​](<#common-patterns> "Direct link to Common Patterns")
### GitHub: new issues[​](<#github-new-issues> "Direct link to GitHub: new issues")
[code] 
    hermes webhook subscribe github-issues \  
      --events "issues" \  
      --prompt "New GitHub issue #{issue.number}: {issue.title}\n\nAction: {action}\nAuthor: {issue.user.login}\nBody:\n{issue.body}\n\nPlease triage this issue." \  
      --deliver telegram \  
      --deliver-chat-id "-100123456789"  
    
[/code]
Then in GitHub repo Settings → Webhooks → Add webhook:
  * Payload URL: the returned webhook_url
  * Content type: application/json
  * Secret: the returned secret
  * Events: "Issues"


### GitHub: PR reviews[​](<#github-pr-reviews> "Direct link to GitHub: PR reviews")
[code] 
    hermes webhook subscribe github-prs \  
      --events "pull_request" \  
      --prompt "PR #{pull_request.number} {action}: {pull_request.title}\nBy: {pull_request.user.login}\nBranch: {pull_request.head.ref}\n\n{pull_request.body}" \  
      --skills "github-code-review" \  
      --deliver github_comment  
    
[/code]
### Stripe: payment events[​](<#stripe-payment-events> "Direct link to Stripe: payment events")
[code] 
    hermes webhook subscribe stripe-payments \  
      --events "payment_intent.succeeded,payment_intent.payment_failed" \  
      --prompt "Payment {data.object.status}: {data.object.amount} cents from {data.object.receipt_email}" \  
      --deliver telegram \  
      --deliver-chat-id "-100123456789"  
    
[/code]
### CI/CD: build notifications[​](<#cicd-build-notifications> "Direct link to CI/CD: build notifications")
[code] 
    hermes webhook subscribe ci-builds \  
      --events "pipeline" \  
      --prompt "Build {object_attributes.status} on {project.name} branch {object_attributes.ref}\nCommit: {commit.message}" \  
      --deliver discord \  
      --deliver-chat-id "1234567890"  
    
[/code]
### Generic monitoring alert[​](<#generic-monitoring-alert> "Direct link to Generic monitoring alert")
[code] 
    hermes webhook subscribe alerts \  
      --prompt "Alert: {alert.name}\nSeverity: {alert.severity}\nMessage: {alert.message}\n\nPlease investigate and suggest remediation." \  
      --deliver origin  
    
[/code]
### Direct delivery (no agent, zero LLM cost)[​](<#direct-delivery-no-agent-zero-llm-cost> "Direct link to Direct delivery \(no agent, zero LLM cost\)")
For use cases where you just want to push a notification through to a user's chat — no reasoning, no agent loop — add `--deliver-only`. The rendered `--prompt` template becomes the literal message body and is dispatched directly to the target adapter.
Use this for:
  * External service push notifications (Supabase/Firebase webhooks → Telegram)
  * Monitoring alerts that should forward verbatim
  * Inter-agent pings where one agent is telling another agent's user something
  * Any webhook where an LLM round trip would be wasted effort


[code] 
    hermes webhook subscribe antenna-matches \  
      --deliver telegram \  
      --deliver-chat-id "123456789" \  
      --deliver-only \  
      --prompt "🎉 New match: {match.user_name} matched with you!" \  
      --description "Antenna match notifications"  
    
[/code]
The POST returns `200 OK` on successful delivery, `502` on target failure — so upstream services can retry intelligently. HMAC auth, rate limits, and idempotency still apply.
Requires `--deliver` to be a real target (telegram, discord, slack, github_comment, etc.) — `--deliver log` is rejected because log-only direct delivery is pointless.
## Security[​](<#security> "Direct link to Security")
  * Each subscription gets an auto-generated HMAC-SHA256 secret (or provide your own with `--secret`)
  * The webhook adapter validates signatures on every incoming POST
  * Static routes from config.yaml cannot be overwritten by dynamic subscriptions
  * Subscriptions persist to `~/.hermes/webhook_subscriptions.json`


## How It Works[​](<#how-it-works> "Direct link to How It Works")
  1. `hermes webhook subscribe` writes to `~/.hermes/webhook_subscriptions.json`
  2. The webhook adapter hot-reloads this file on each incoming request (mtime-gated, negligible overhead)
  3. When a POST arrives matching a route, the adapter formats the prompt and triggers an agent run
  4. The agent's response is delivered to the configured target (Telegram, Discord, GitHub comment, etc.)


## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
If webhooks aren't working:
  1. **Is the gateway running?** Check with `systemctl --user status hermes-gateway` or `ps aux | grep gateway`
  2. **Is the webhook server listening?** `curl http://localhost:8644/health` should return `{"status": "ok"}`
  3. **Check gateway logs:** `grep webhook ~/.hermes/logs/gateway.log | tail -20`
  4. **Signature mismatch?** Verify the secret in your service matches the one from `hermes webhook list`. GitHub sends `X-Hub-Signature-256`, GitLab sends `X-Gitlab-Token`.
  5. **Firewall/NAT?** The webhook URL must be reachable from the service. For local development, use a tunnel (ngrok, cloudflared).
  6. **Wrong event type?** Check `--events` filter matches what the service sends. Use `hermes webhook test <name>` to verify the route works.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Setup (Required First)](<#setup-required-first>)
    * [Option 1: Setup wizard](<#option-1-setup-wizard>)
    * [Option 2: Manual config](<#option-2-manual-config>)
    * [Option 3: Environment variables](<#option-3-environment-variables>)
  * [Commands](<#commands>)
    * [Create a subscription](<#create-a-subscription>)
    * [List subscriptions](<#list-subscriptions>)
    * [Remove a subscription](<#remove-a-subscription>)
    * [Test a subscription](<#test-a-subscription>)
  * [Prompt Templates](<#prompt-templates>)
  * [Common Patterns](<#common-patterns>)
    * [GitHub: new issues](<#github-new-issues>)
    * [GitHub: PR reviews](<#github-pr-reviews>)
    * [Stripe: payment events](<#stripe-payment-events>)
    * [CI/CD: build notifications](<#cicd-build-notifications>)
    * [Generic monitoring alert](<#generic-monitoring-alert>)
    * [Direct delivery (no agent, zero LLM cost)](<#direct-delivery-no-agent-zero-llm-cost>)
  * [Security](<#security>)
  * [How It Works](<#how-it-works>)
  * [Troubleshooting](<#troubleshooting>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/devops/devops-webhook-subscriptions -->
