On this page
Connect Hermes Agent to Microsoft Teams as a bot. Unlike Slack's Socket Mode, Teams delivers messages by calling a **public HTTPS webhook** , so your instance needs a publicly reachable endpoint — either a dev tunnel (local dev) or a real domain (production).
## How the Bot Responds[​](<#how-the-bot-responds> "Direct link to How the Bot Responds")
Context| Behavior  
---|---  
**Personal chat (DM)**|  Bot responds to every message. No @mention needed.  
**Group chat**|  Bot only responds when @mentioned.  
**Channel**|  Bot only responds when @mentioned.  
Teams delivers @mentions as regular messages with `<at>BotName</at>` tags, which Hermes strips automatically before processing.
* * *
## Step 1: Install the Teams CLI[​](<#step-1-install-the-teams-cli> "Direct link to Step 1: Install the Teams CLI")
The `@microsoft/teams.cli` automates bot registration — no Azure portal needed.
[code] 
    npm install -g @microsoft/teams.cli@preview  
    teams login  
    
[/code]
To verify your login and find your own AAD object ID (needed for `TEAMS_ALLOWED_USERS`):
[code] 
    teams status --verbose  
    
[/code]
* * *
## Step 2: Expose the Webhook Port[​](<#step-2-expose-the-webhook-port> "Direct link to Step 2: Expose the Webhook Port")
Teams cannot deliver messages to `localhost`. For local development, use any tunnel tool to get a public HTTPS URL. The default port is `3978` — change it with `TEAMS_PORT` if needed.
[code] 
    # devtunnel (Microsoft)  
    devtunnel create hermes-bot --allow-anonymous  
    devtunnel port create hermes-bot -p 3978 --protocol https  # replace 3978 with TEAMS_PORT if changed  
    devtunnel host hermes-bot  
      
    # ngrok  
    ngrok http 3978  # replace 3978 with TEAMS_PORT if changed  
      
    # cloudflared  
    cloudflared tunnel --url http://localhost:3978  # replace 3978 with TEAMS_PORT if changed  
    
[/code]
Copy the `https://` URL from the output — you'll use it in the next step. Leave the tunnel running while developing.
For production, point your bot's endpoint at your server's public domain instead (see [Production Deployment](<#production-deployment>)).
* * *
## Step 3: Create the Bot[​](<#step-3-create-the-bot> "Direct link to Step 3: Create the Bot")
[code] 
    teams app create \  
      --name "Hermes" \  
      --endpoint "https://<your-tunnel-url>/api/messages"  
    
[/code]
The CLI outputs your `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID`, plus an install link for Step 6. Save the client secret — it won't be shown again.
* * *
## Step 4: Configure Environment Variables[​](<#step-4-configure-environment-variables> "Direct link to Step 4: Configure Environment Variables")
Add to `~/.hermes/.env`:
[code] 
    # Required  
    TEAMS_CLIENT_ID=<your-client-id>  
    TEAMS_CLIENT_SECRET=<your-client-secret>  
    TEAMS_TENANT_ID=<your-tenant-id>  
      
    # Restrict access to specific users (recommended)  
    # Use AAD object IDs from `teams status --verbose`  
    TEAMS_ALLOWED_USERS=<your-aad-object-id>  
    
[/code]
* * *
## Step 5: Start the Gateway[​](<#step-5-start-the-gateway> "Direct link to Step 5: Start the Gateway")
[code] 
    HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d gateway  
    
[/code]
This starts the gateway. The default webhook port is `3978` (override with `TEAMS_PORT`). Check that it's running:
[code] 
    curl http://localhost:3978/health   # should return: ok  
    docker logs -f hermes  
    
[/code]
Look for:
[code] 
    [teams] Webhook server listening on 0.0.0.0:3978/api/messages  
    
[/code]
* * *
## Step 6: Install the App in Teams[​](<#step-6-install-the-app-in-teams> "Direct link to Step 6: Install the App in Teams")
[code] 
    teams app get <teamsAppId> --install-link  
    
[/code]
Open the printed link in your browser — it opens directly in the Teams client. After installing, send a direct message to your bot — it's ready.
* * *
## Configuration Reference[​](<#configuration-reference> "Direct link to Configuration Reference")
### Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
Variable| Description  
---|---  
`TEAMS_CLIENT_ID`| Azure AD App (client) ID  
`TEAMS_CLIENT_SECRET`| Azure AD client secret  
`TEAMS_TENANT_ID`| Azure AD tenant ID  
`TEAMS_ALLOWED_USERS`| Comma-separated AAD object IDs allowed to use the bot  
`TEAMS_ALLOW_ALL_USERS`| Set `true` to skip the allowlist and allow anyone  
`TEAMS_HOME_CHANNEL`| Conversation ID for cron/proactive message delivery  
`TEAMS_HOME_CHANNEL_NAME`| Display name for the home channel  
`TEAMS_PORT`| Webhook port (default: `3978`)  
### config.yaml[​](<#configyaml> "Direct link to config.yaml")
Alternatively, configure via `~/.hermes/config.yaml`:
[code] 
    platforms:  
      teams:  
        enabled: true  
        extra:  
          client_id: "your-client-id"  
          client_secret: "your-secret"  
          tenant_id: "your-tenant-id"  
          port: 3978  
    
[/code]
* * *
## Features[​](<#features> "Direct link to Features")
### Interactive Approval Cards[​](<#interactive-approval-cards> "Direct link to Interactive Approval Cards")
When the agent needs to run a potentially dangerous command, it sends an Adaptive Card with four buttons instead of asking you to type `/approve`:
  * **Allow Once** — approve this specific command
  * **Allow Session** — approve this pattern for the rest of the session
  * **Always Allow** — permanently approve this pattern
  * **Deny** — reject the command


Clicking a button resolves the approval inline and replaces the card with the decision.
* * *
## Production Deployment[​](<#production-deployment> "Direct link to Production Deployment")
For a permanent server, skip devtunnel and register your bot with your server's public HTTPS endpoint:
[code] 
    teams app create \  
      --name "Hermes" \  
      --endpoint "https://your-domain.com/api/messages"  
    
[/code]
If you've already created the bot and just need to update the endpoint:
[code] 
    teams app update --id <teamsAppId> --endpoint "https://your-domain.com/api/messages"  
    
[/code]
Make sure your configured port (`TEAMS_PORT`, default `3978`) is reachable from the internet and that your TLS certificate is valid — Teams rejects self-signed certificates.
* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
Problem| Solution  
---|---  
`health` endpoint works but bot doesn't respond| Check that your tunnel is still running and the bot's messaging endpoint matches the tunnel URL  
`KeyError: 'teams'` in logs| Restart the container — this is fixed in the current version  
Bot responds with auth errors| Verify `TEAMS_CLIENT_ID`, `TEAMS_CLIENT_SECRET`, and `TEAMS_TENANT_ID` are all set correctly  
`No inference provider configured`| Check that `ANTHROPIC_API_KEY` (or another provider key) is set in `~/.hermes/.env`  
Bot receives messages but ignores them| Your AAD object ID may not be in `TEAMS_ALLOWED_USERS`. Run `teams status --verbose` to find it  
Tunnel URL changes on restart| devtunnel URLs are persistent if you use a named tunnel (`devtunnel create hermes-bot`). ngrok and cloudflared generate a new URL each run unless you have a paid plan — update the bot endpoint with `teams app update` when it changes  
Teams shows "This bot is not responding"| The webhook returned an error. Check `docker logs hermes` for tracebacks  
`[teams] Failed to connect` in logs| The SDK failed to authenticate. Double-check your credentials and that the tenant ID matches the account you used in `teams login`  
* * *
## Security[​](<#security> "Direct link to Security")
warning
**Always set`TEAMS_ALLOWED_USERS`** with the AAD object IDs of authorized users. Without this, anyone who can find or install your bot can interact with it.
Treat `TEAMS_CLIENT_SECRET` like a password — rotate it periodically via the Azure portal or Teams CLI.
  * Store credentials in `~/.hermes/.env` with permissions `600` (`chmod 600 ~/.hermes/.env`)
  * The bot only accepts messages from users in `TEAMS_ALLOWED_USERS`; unauthorized messages are silently dropped
  * Your public endpoint (`/api/messages`) is authenticated by the Teams Bot Framework — requests without valid JWTs are rejected


  * [How the Bot Responds](<#how-the-bot-responds>)
  * [Step 1: Install the Teams CLI](<#step-1-install-the-teams-cli>)
  * [Step 2: Expose the Webhook Port](<#step-2-expose-the-webhook-port>)
  * [Step 3: Create the Bot](<#step-3-create-the-bot>)
  * [Step 4: Configure Environment Variables](<#step-4-configure-environment-variables>)
  * [Step 5: Start the Gateway](<#step-5-start-the-gateway>)
  * [Step 6: Install the App in Teams](<#step-6-install-the-app-in-teams>)
  * [Configuration Reference](<#configuration-reference>)
    * [Environment Variables](<#environment-variables>)
    * [config.yaml](<#configyaml>)
  * [Features](<#features>)
    * [Interactive Approval Cards](<#interactive-approval-cards>)
  * [Production Deployment](<#production-deployment>)
  * [Troubleshooting](<#troubleshooting>)
  * [Security](<#security>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams -->
