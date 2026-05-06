On this page
[Open WebUI](<https://github.com/open-webui/open-webui>) (126k★) is the most popular self-hosted chat interface for AI. With Hermes Agent's built-in API server, you can use Open WebUI as a polished web frontend for your agent — complete with conversation management, user accounts, and a modern chat interface.
## Architecture[​](<#architecture> "Direct link to Architecture")
Open WebUI connects to Hermes Agent's API server just like it would connect to OpenAI. Your agent handles the requests with its full toolset — terminal, file operations, web search, memory, skills — and returns the final response.
Open WebUI talks to Hermes server-to-server, so you do not need `API_SERVER_CORS_ORIGINS` for this integration.
## Quick Setup[​](<#quick-setup> "Direct link to Quick Setup")
### One-command local bootstrap (macOS/Linux, no Docker)[​](<#one-command-local-bootstrap-macoslinux-no-docker> "Direct link to One-command local bootstrap \(macOS/Linux, no Docker\)")
If you want Hermes + Open WebUI wired together locally with a reusable launcher, run:
[code] 
    cd ~/.hermes/hermes-agent  
    bash scripts/setup_open_webui.sh  
    
[/code]
What the script does:
  * ensures `~/.hermes/.env` contains `API_SERVER_ENABLED`, `API_SERVER_HOST`, `API_SERVER_KEY`, `API_SERVER_PORT`, and `API_SERVER_MODEL_NAME`
  * restarts the Hermes gateway so the API server comes up
  * installs Open WebUI into `~/.local/open-webui-venv`
  * writes a launcher at `~/.local/bin/start-open-webui-hermes.sh`
  * on macOS, installs a `launchd` user service; on Linux with `systemd --user`, installs a user service there


Defaults:
  * Hermes API: `http://127.0.0.1:8642/v1`
  * Open WebUI: `http://127.0.0.1:8080`
  * model name advertised to Open WebUI: `Hermes Agent`


Useful overrides:
[code] 
    OPEN_WEBUI_NAME='My Hermes UI' \  
    OPEN_WEBUI_ENABLE_SIGNUP=true \  
    HERMES_API_MODEL_NAME='My Hermes Agent' \  
    bash scripts/setup_open_webui.sh  
    
[/code]
On Linux, automatic background service setup requires a working `systemd --user` session. If you are on a headless SSH box and want to skip service installation, run:
[code] 
    OPEN_WEBUI_ENABLE_SERVICE=false bash scripts/setup_open_webui.sh  
    
[/code]
### 1\. Enable the API server[​](<#1-enable-the-api-server> "Direct link to 1. Enable the API server")
[code] 
    hermes config set API_SERVER_ENABLED true  
    hermes config set API_SERVER_KEY your-secret-key  
    
[/code]
`hermes config set` auto-routes the flag to `config.yaml` and the secret to `~/.hermes/.env`. If the gateway is already running, restart it so the change takes effect:
[code] 
    hermes gateway stop && hermes gateway  
    
[/code]
### 2\. Start Hermes Agent gateway[​](<#2-start-hermes-agent-gateway> "Direct link to 2. Start Hermes Agent gateway")
[code] 
    hermes gateway  
    
[/code]
You should see:
[code] 
    [API Server] API server listening on http://127.0.0.1:8642  
    
[/code]
### 3\. Verify the API server is reachable[​](<#3-verify-the-api-server-is-reachable> "Direct link to 3. Verify the API server is reachable")
[code] 
    curl -s http://127.0.0.1:8642/health  
    # {"status": "ok", ...}  
      
    curl -s -H "Authorization: Bearer your-secret-key" http://127.0.0.1:8642/v1/models  
    # {"object":"list","data":[{"id":"hermes-agent", ...}]}  
    
[/code]
If `/health` fails, the gateway didn't pick up `API_SERVER_ENABLED=true` — restart it. If `/v1/models` returns `401`, your `Authorization` header doesn't match `API_SERVER_KEY`.
### 4\. Start Open WebUI[​](<#4-start-open-webui> "Direct link to 4. Start Open WebUI")
[code] 
    docker run -d -p 3000:8080 \  
      -e OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1 \  
      -e OPENAI_API_KEY=your-secret-key \  
      -e ENABLE_OLLAMA_API=false \  
      --add-host=host.docker.internal:host-gateway \  
      -v open-webui:/app/backend/data \  
      --name open-webui \  
      --restart always \  
      ghcr.io/open-webui/open-webui:main  
    
[/code]
`ENABLE_OLLAMA_API=false` suppresses the default Ollama backend, which would otherwise show up empty and clutter the model picker. Omit it if you actually have Ollama running alongside.
First launch takes 15–30 seconds: Open WebUI downloads sentence-transformer embedding models (~150MB) the first time it starts. Wait for `docker logs open-webui` to settle before opening the UI.
### 5\. Open the UI[​](<#5-open-the-ui> "Direct link to 5. Open the UI")
Go to **<http://localhost:3000>**. Create your admin account (the first user becomes admin). You should see your agent in the model dropdown (named after your profile, or **hermes-agent** for the default profile). Start chatting!
## Docker Compose Setup[​](<#docker-compose-setup> "Direct link to Docker Compose Setup")
For a more permanent setup, create a `docker-compose.yml`:
[code] 
    services:  
      open-webui:  
        image: ghcr.io/open-webui/open-webui:main  
        ports:  
          - "3000:8080"  
        volumes:  
          - open-webui:/app/backend/data  
        environment:  
          - OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1  
          - OPENAI_API_KEY=your-secret-key  
          - ENABLE_OLLAMA_API=false  
        extra_hosts:  
          - "host.docker.internal:host-gateway"  
        restart: always  
      
    volumes:  
      open-webui:  
    
[/code]
Then:
[code] 
    docker compose up -d  
    
[/code]
## Configuring via the Admin UI[​](<#configuring-via-the-admin-ui> "Direct link to Configuring via the Admin UI")
If you prefer to configure the connection through the UI instead of environment variables:
  1. Log in to Open WebUI at **<http://localhost:3000>**
  2. Click your **profile avatar** → **Admin Settings**
  3. Go to **Connections**
  4. Under **OpenAI API** , click the **wrench icon** (Manage)
  5. Click **\+ Add New Connection**
  6. Enter:
     * **URL** : `http://host.docker.internal:8642/v1`
     * **API Key** : the exact same value as `API_SERVER_KEY` in Hermes
  7. Click the **checkmark** to verify the connection
  8. **Save**


Your agent model should now appear in the model dropdown (named after your profile, or **hermes-agent** for the default profile).
warning
Environment variables only take effect on Open WebUI's **first launch**. After that, connection settings are stored in its internal database. To change them later, use the Admin UI or delete the Docker volume and start fresh.
## API Type: Chat Completions vs Responses[​](<#api-type-chat-completions-vs-responses> "Direct link to API Type: Chat Completions vs Responses")
Open WebUI supports two API modes when connecting to a backend:
Mode| Format| When to use  
---|---|---  
**Chat Completions** (default)| `/v1/chat/completions`| Recommended. Works out of the box.  
**Responses** (experimental)| `/v1/responses`| For server-side conversation state via `previous_response_id`.  
### Using Chat Completions (recommended)[​](<#using-chat-completions-recommended> "Direct link to Using Chat Completions \(recommended\)")
This is the default and requires no extra configuration. Open WebUI sends standard OpenAI-format requests and Hermes Agent responds accordingly. Each request includes the full conversation history.
### Using Responses API[​](<#using-responses-api> "Direct link to Using Responses API")
To use the Responses API mode:
  1. Go to **Admin Settings** → **Connections** → **OpenAI** → **Manage**
  2. Edit your hermes-agent connection
  3. Change **API Type** from "Chat Completions" to **"Responses (Experimental)"**
  4. Save


With the Responses API, Open WebUI sends requests in the Responses format (`input` array + `instructions`), and Hermes Agent can preserve full tool call history across turns via `previous_response_id`. When `stream: true`, Hermes also streams spec-native `function_call` and `function_call_output` items, which enables custom structured tool-call UI in clients that render Responses events.
note
Open WebUI currently manages conversation history client-side even in Responses mode — it sends the full message history in each request rather than using `previous_response_id`. The main advantage of Responses mode today is the structured event stream: text deltas, `function_call`, and `function_call_output` items arrive as OpenAI Responses SSE events instead of Chat Completions chunks.
## How It Works[​](<#how-it-works> "Direct link to How It Works")
When you send a message in Open WebUI:
  1. Open WebUI sends a `POST /v1/chat/completions` request with your message and conversation history
  2. Hermes Agent creates an AIAgent instance with its full toolset
  3. The agent processes your request — it may call tools (terminal, file operations, web search, etc.)
  4. As tools execute, **inline progress messages stream to the UI** so you can see what the agent is doing (e.g. ``💻 ls -la``, ``🔍 Python 3.12 release``)
  5. The agent's final text response streams back to Open WebUI
  6. Open WebUI displays the response in its chat interface


Your agent has access to all the same tools and capabilities as when using the CLI or Telegram — the only difference is the frontend.
Tool Progress
With streaming enabled (the default), you'll see brief inline indicators as tools run — the tool emoji and its key argument. These appear in the response stream before the agent's final answer, giving you visibility into what's happening behind the scenes.
## Configuration Reference[​](<#configuration-reference> "Direct link to Configuration Reference")
### Hermes Agent (API server)[​](<#hermes-agent-api-server> "Direct link to Hermes Agent \(API server\)")
Variable| Default| Description  
---|---|---  
`API_SERVER_ENABLED`| `false`| Enable the API server  
`API_SERVER_PORT`| `8642`| HTTP server port  
`API_SERVER_HOST`| `127.0.0.1`| Bind address  
`API_SERVER_KEY`|  _(required)_|  Bearer token for auth. Match `OPENAI_API_KEY`.  
### Open WebUI[​](<#open-webui> "Direct link to Open WebUI")
Variable| Description  
---|---  
`OPENAI_API_BASE_URL`| Hermes Agent's API URL (include `/v1`)  
`OPENAI_API_KEY`| Must be non-empty. Match your `API_SERVER_KEY`.  
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### No models appear in the dropdown[​](<#no-models-appear-in-the-dropdown> "Direct link to No models appear in the dropdown")
  * **Check the URL has`/v1` suffix**: `http://host.docker.internal:8642/v1` (not just `:8642`)
  * **Verify the gateway is running** : `curl http://localhost:8642/health` should return `{"status": "ok"}`
  * **Check model listing** : `curl -H "Authorization: Bearer your-secret-key" http://localhost:8642/v1/models` should return a list with `hermes-agent`
  * **Docker networking** : From inside Docker, `localhost` means the container, not your host. Use `host.docker.internal` or `--network=host`.
  * **Empty Ollama backend shadowing the picker** : If you omitted `ENABLE_OLLAMA_API=false`, Open WebUI shows an empty Ollama section above your Hermes models. Restart the container with `-e ENABLE_OLLAMA_API=false` or disable Ollama in **Admin Settings → Connections**.


### Connection test passes but no models load[​](<#connection-test-passes-but-no-models-load> "Direct link to Connection test passes but no models load")
This is almost always the missing `/v1` suffix. Open WebUI's connection test is a basic connectivity check — it doesn't verify model listing works.
### Response takes a long time[​](<#response-takes-a-long-time> "Direct link to Response takes a long time")
Hermes Agent may be executing multiple tool calls (reading files, running commands, searching the web) before producing its final response. This is normal for complex queries. The response appears all at once when the agent finishes.
### "Invalid API key" errors[​](<#invalid-api-key-errors> "Direct link to "Invalid API key" errors")
Make sure your `OPENAI_API_KEY` in Open WebUI matches the `API_SERVER_KEY` in Hermes Agent.
warning
Open WebUI persists OpenAI-compatible connection settings in its own database after first launch. If you accidentally saved a wrong key in the Admin UI, fixing the environment variables alone is not enough — update or delete the saved connection in **Admin Settings → Connections** , or reset the Open WebUI data directory / database.
## Multi-User Setup with Profiles[​](<#multi-user-setup-with-profiles> "Direct link to Multi-User Setup with Profiles")
To run separate Hermes instances per user — each with their own config, memory, and skills — use [profiles](</docs/user-guide/profiles>). Each profile runs its own API server on a different port and automatically advertises the profile name as the model in Open WebUI.
### 1\. Create profiles and configure API servers[​](<#1-create-profiles-and-configure-api-servers> "Direct link to 1. Create profiles and configure API servers")
[code] 
    hermes profile create alice  
    hermes -p alice config set API_SERVER_ENABLED true  
    hermes -p alice config set API_SERVER_PORT 8643  
    hermes -p alice config set API_SERVER_KEY alice-secret  
      
    hermes profile create bob  
    hermes -p bob config set API_SERVER_ENABLED true  
    hermes -p bob config set API_SERVER_PORT 8644  
    hermes -p bob config set API_SERVER_KEY bob-secret  
    
[/code]
### 2\. Start each gateway[​](<#2-start-each-gateway> "Direct link to 2. Start each gateway")
[code] 
    hermes -p alice gateway &  
    hermes -p bob gateway &  
    
[/code]
### 3\. Add connections in Open WebUI[​](<#3-add-connections-in-open-webui> "Direct link to 3. Add connections in Open WebUI")
In **Admin Settings** → **Connections** → **OpenAI API** → **Manage** , add one connection per profile:
Connection| URL| API Key  
---|---|---  
Alice| `http://host.docker.internal:8643/v1`| `alice-secret`  
Bob| `http://host.docker.internal:8644/v1`| `bob-secret`  
The model dropdown will show `alice` and `bob` as distinct models. You can assign models to Open WebUI users via the admin panel, giving each user their own isolated Hermes agent.
Custom Model Names
The model name defaults to the profile name. To override it, set `API_SERVER_MODEL_NAME` in the profile's `.env`:
[code]
    hermes -p alice config set API_SERVER_MODEL_NAME "Alice's Agent"  
    
[/code]
## Linux Docker (no Docker Desktop)[​](<#linux-docker-no-docker-desktop> "Direct link to Linux Docker \(no Docker Desktop\)")
On Linux without Docker Desktop, `host.docker.internal` doesn't resolve by default. Options:
[code] 
    # Option 1: Add host mapping  
    docker run --add-host=host.docker.internal:host-gateway ...  
      
    # Option 2: Use host networking  
    docker run --network=host -e OPENAI_API_BASE_URL=http://localhost:8642/v1 ...  
      
    # Option 3: Use Docker bridge IP  
    docker run -e OPENAI_API_BASE_URL=http://172.17.0.1:8642/v1 ...  
    
[/code]
  * [Architecture](<#architecture>)
  * [Quick Setup](<#quick-setup>)
    * [One-command local bootstrap (macOS/Linux, no Docker)](<#one-command-local-bootstrap-macoslinux-no-docker>)
    * [1\. Enable the API server](<#1-enable-the-api-server>)
    * [2\. Start Hermes Agent gateway](<#2-start-hermes-agent-gateway>)
    * [3\. Verify the API server is reachable](<#3-verify-the-api-server-is-reachable>)
    * [4\. Start Open WebUI](<#4-start-open-webui>)
    * [5\. Open the UI](<#5-open-the-ui>)
  * [Docker Compose Setup](<#docker-compose-setup>)
  * [Configuring via the Admin UI](<#configuring-via-the-admin-ui>)
  * [API Type: Chat Completions vs Responses](<#api-type-chat-completions-vs-responses>)
    * [Using Chat Completions (recommended)](<#using-chat-completions-recommended>)
    * [Using Responses API](<#using-responses-api>)
  * [How It Works](<#how-it-works>)
  * [Configuration Reference](<#configuration-reference>)
    * [Hermes Agent (API server)](<#hermes-agent-api-server>)
    * [Open WebUI](<#open-webui>)
  * [Troubleshooting](<#troubleshooting>)
    * [No models appear in the dropdown](<#no-models-appear-in-the-dropdown>)
    * [Connection test passes but no models load](<#connection-test-passes-but-no-models-load>)
    * [Response takes a long time](<#response-takes-a-long-time>)
    * ["Invalid API key" errors](<#invalid-api-key-errors>)
  * [Multi-User Setup with Profiles](<#multi-user-setup-with-profiles>)
    * [1\. Create profiles and configure API servers](<#1-create-profiles-and-configure-api-servers>)
    * [2\. Start each gateway](<#2-start-each-gateway>)
    * [3\. Add connections in Open WebUI](<#3-add-connections-in-open-webui>)
  * [Linux Docker (no Docker Desktop)](<#linux-docker-no-docker-desktop>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui -->
