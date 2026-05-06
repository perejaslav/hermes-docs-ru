On this page
There are two distinct ways Docker intersects with Hermes Agent:
  1. **Running Hermes IN Docker** — the agent itself runs inside a container (this page's primary focus)
  2. **Docker as a terminal backend** — the agent runs on your host but executes every command inside a single, persistent Docker sandbox container that survives across tool calls, `/new`, and subagents for the life of the Hermes process (see [Configuration → Docker Backend](</docs/user-guide/configuration#docker-backend>))


This page covers option 1. The container stores all user data (config, API keys, sessions, skills, memories) in a single directory mounted from the host at `/opt/data`. The image itself is stateless and can be upgraded by pulling a new version without losing any configuration.
## Quick start[​](<#quick-start> "Direct link to Quick start")
If this is your first time running Hermes Agent, create a data directory on the host and start the container interactively to run the setup wizard:
[code] 
    mkdir -p ~/.hermes  
    docker run -it --rm \  
      -v ~/.hermes:/opt/data \  
      nousresearch/hermes-agent setup  
    
[/code]
This drops you into the setup wizard, which will prompt you for your API keys and write them to `~/.hermes/.env`. You only need to do this once. It is highly recommended to set up a chat system for the gateway to work with at this point.
## Running in gateway mode[​](<#running-in-gateway-mode> "Direct link to Running in gateway mode")
Once configured, run the container in the background as a persistent gateway (Telegram, Discord, Slack, WhatsApp, etc.):
[code] 
    docker run -d \  
      --name hermes \  
      --restart unless-stopped \  
      -v ~/.hermes:/opt/data \  
      -p 8642:8642 \  
      nousresearch/hermes-agent gateway run  
    
[/code]
Port 8642 exposes the gateway's [OpenAI-compatible API server](</docs/user-guide/features/api-server>) and health endpoint. It's optional if you only use chat platforms (Telegram, Discord, etc.), but required if you want the dashboard or external tools to reach the gateway.
Note: the API server is gated on `API_SERVER_ENABLED=true`. To expose it beyond `127.0.0.1` inside the container, also set `API_SERVER_HOST=0.0.0.0` and an `API_SERVER_KEY` (minimum 8 characters — generate one with `openssl rand -hex 32`). Example:
[code] 
    docker run -d \  
      --name hermes \  
      --restart unless-stopped \  
      -v ~/.hermes:/opt/data \  
      -p 8642:8642 \  
      -e API_SERVER_ENABLED=true \  
      -e API_SERVER_HOST=0.0.0.0 \  
      -e API_SERVER_KEY=your_api_key_here \  
      -e API_SERVER_CORS_ORIGINS='*' \  
      nousresearch/hermes-agent gateway run  
    
[/code]
Opening any port on an internet facing machine is a security risk. You should not do it unless you understand the risks.
## Running the dashboard[​](<#running-the-dashboard> "Direct link to Running the dashboard")
The built-in web dashboard runs as an optional side-process inside the same container as the gateway. Set `HERMES_DASHBOARD=1` and expose port `9119` alongside the gateway's `8642`:
[code] 
    docker run -d \  
      --name hermes \  
      --restart unless-stopped \  
      -v ~/.hermes:/opt/data \  
      -p 8642:8642 \  
      -p 9119:9119 \  
      -e HERMES_DASHBOARD=1 \  
      nousresearch/hermes-agent gateway run  
    
[/code]
The entrypoint starts `hermes dashboard` in the background (running as the non-root `hermes` user) before `exec`-ing the main command. Dashboard output is prefixed with `[dashboard]` in `docker logs` so it's easy to separate from gateway logs.
Environment variable| Description| Default  
---|---|---  
`HERMES_DASHBOARD`| Set to `1` (or `true` / `yes`) to launch the dashboard alongside the main command|  _(unset — dashboard not started)_  
`HERMES_DASHBOARD_HOST`| Bind address for the dashboard HTTP server| `0.0.0.0`  
`HERMES_DASHBOARD_PORT`| Port for the dashboard HTTP server| `9119`  
`HERMES_DASHBOARD_TUI`| Set to `1` to expose the in-browser Chat tab (embedded `hermes --tui` via PTY/WebSocket)| _(unset)_  
The default `HERMES_DASHBOARD_HOST=0.0.0.0` is required for the host to reach the dashboard through the published port; the entrypoint automatically passes `--insecure` to `hermes dashboard` in that case. Override to `127.0.0.1` if you want to restrict the dashboard to in-container access only (e.g. behind a reverse proxy in a sidecar).
note
The dashboard side-process is **not supervised** — if it crashes, it stays down until the container restarts. Running it as a separate container is not supported: the dashboard's gateway-liveness detection requires a shared PID namespace with the gateway process.
## Running interactively (CLI chat)[​](<#running-interactively-cli-chat> "Direct link to Running interactively \(CLI chat\)")
To open an interactive chat session against a running data directory:
[code] 
    docker run -it --rm \  
      -v ~/.hermes:/opt/data \  
      nousresearch/hermes-agent  
    
[/code]
Or if you have already opened a terminal in your running container (via Docker Desktop for instance), just run:
[code] 
    /opt/hermes/.venv/bin/hermes  
    
[/code]
## Persistent volumes[​](<#persistent-volumes> "Direct link to Persistent volumes")
The `/opt/data` volume is the single source of truth for all Hermes state. It maps to your host's `~/.hermes/` directory and contains:
Path| Contents  
---|---  
`.env`| API keys and secrets  
`config.yaml`| All Hermes configuration  
`SOUL.md`| Agent personality/identity  
`sessions/`| Conversation history  
`memories/`| Persistent memory store  
`skills/`| Installed skills  
`cron/`| Scheduled job definitions  
`hooks/`| Event hooks  
`logs/`| Runtime logs  
`skins/`| Custom CLI skins  
warning
Never run two Hermes **gateway** containers against the same data directory simultaneously — session files and memory stores are not designed for concurrent write access.
## Multi-profile support[​](<#multi-profile-support> "Direct link to Multi-profile support")
Hermes supports [multiple profiles](</docs/reference/profile-commands>) — separate `~/.hermes/` directories that let you run independent agents (different SOUL, skills, memory, sessions, credentials) from a single installation. **When running under Docker, using Hermes' built-in multi-profile feature is not recommended.**
Instead, the recommended pattern is **one container per profile** , with each container bind-mounting its own host directory as `/opt/data`:
[code] 
    # Work profile  
    docker run -d \  
      --name hermes-work \  
      --restart unless-stopped \  
      -v ~/.hermes-work:/opt/data \  
      -p 8642:8642 \  
      nousresearch/hermes-agent gateway run  
      
    # Personal profile  
    docker run -d \  
      --name hermes-personal \  
      --restart unless-stopped \  
      -v ~/.hermes-personal:/opt/data \  
      -p 8643:8642 \  
      nousresearch/hermes-agent gateway run  
    
[/code]
Why separate containers over profiles in Docker:
  * **Isolation** — each container has its own filesystem, process table, and resource limits. A crash, dependency change, or runaway session in one profile can't affect another.
  * **Independent lifecycle** — upgrade, restart, pause, or roll back each agent separately (`docker restart hermes-work` leaves `hermes-personal` untouched).
  * **Clean port and network separation** — each gateway binds its own host port; there's no risk of cross-talk between chat platforms or API servers.
  * **Simpler mental model** — the container _is_ the profile. Backups, migrations, and permissions all follow the bind-mounted directory, with no extra `--profile` flags to remember.
  * **Avoids concurrent-write risk** — the warning above about never running two gateways against the same data directory still applies to profiles within a single container.


In Docker Compose, this just means declaring one service per profile with distinct `container_name`, `volumes`, and `ports`:
[code] 
    services:  
      hermes-work:  
        image: nousresearch/hermes-agent:latest  
        container_name: hermes-work  
        restart: unless-stopped  
        command: gateway run  
        ports:  
          - "8642:8642"  
        volumes:  
          - ~/.hermes-work:/opt/data  
      
      hermes-personal:  
        image: nousresearch/hermes-agent:latest  
        container_name: hermes-personal  
        restart: unless-stopped  
        command: gateway run  
        ports:  
          - "8643:8642"  
        volumes:  
          - ~/.hermes-personal:/opt/data  
    
[/code]
## Environment variable forwarding[​](<#environment-variable-forwarding> "Direct link to Environment variable forwarding")
API keys are read from `/opt/data/.env` inside the container. You can also pass environment variables directly:
[code] 
    docker run -it --rm \  
      -v ~/.hermes:/opt/data \  
      -e ANTHROPIC_API_KEY="sk-ant-..." \  
      -e OPENAI_API_KEY="sk-..." \  
      nousresearch/hermes-agent  
    
[/code]
Direct `-e` flags override values from `.env`. This is useful for CI/CD or secrets-manager integrations where you don't want keys on disk.
## Docker Compose example[​](<#docker-compose-example> "Direct link to Docker Compose example")
For persistent deployment with both the gateway and dashboard, a `docker-compose.yaml` is convenient:
[code] 
    services:  
      hermes:  
        image: nousresearch/hermes-agent:latest  
        container_name: hermes  
        restart: unless-stopped  
        command: gateway run  
        ports:  
          - "8642:8642"   # gateway API  
          - "9119:9119"   # dashboard (only reached when HERMES_DASHBOARD=1)  
        volumes:  
          - ~/.hermes:/opt/data  
        environment:  
          - HERMES_DASHBOARD=1  
          # Uncomment to forward specific env vars instead of using .env file:  
          # - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}  
          # - OPENAI_API_KEY=${OPENAI_API_KEY}  
          # - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}  
        deploy:  
          resources:  
            limits:  
              memory: 4G  
              cpus: "2.0"  
    
[/code]
Start with `docker compose up -d` and view logs with `docker compose logs -f`. Dashboard output is prefixed with `[dashboard]` so it's easy to filter from gateway logs.
## Resource limits[​](<#resource-limits> "Direct link to Resource limits")
The Hermes container needs moderate resources. Recommended minimums:
Resource| Minimum| Recommended  
---|---|---  
Memory| 1 GB| 2–4 GB  
CPU| 1 core| 2 cores  
Disk (data volume)| 500 MB| 2+ GB (grows with sessions/skills)  
Browser automation (Playwright/Chromium) is the most memory-hungry feature. If you don't need browser tools, 1 GB is sufficient. With browser tools active, allocate at least 2 GB.
Set limits in Docker:
[code] 
    docker run -d \  
      --name hermes \  
      --restart unless-stopped \  
      --memory=4g --cpus=2 \  
      -v ~/.hermes:/opt/data \  
      nousresearch/hermes-agent gateway run  
    
[/code]
## What the Dockerfile does[​](<#what-the-dockerfile-does> "Direct link to What the Dockerfile does")
The official image is based on `debian:13.4` and includes:
  * Python 3 with all Hermes dependencies (`uv pip install -e ".[all]"`)
  * Node.js + npm (for browser automation and WhatsApp bridge)
  * Playwright with Chromium (`npx playwright install --with-deps chromium --only-shell`)
  * ripgrep, ffmpeg, git, and tini as system utilities
  * **`docker-cli`** — so agents running inside the container can drive the host's Docker daemon (bind-mount `/var/run/docker.sock` to opt in) for `docker build`, `docker run`, container inspection, etc.
  * **`openssh-client`** — enables the [SSH terminal backend](</docs/user-guide/configuration#ssh-backend>) from inside the container. The SSH backend shells out to the system `ssh` binary; without this, it failed silently in containerized installs.
  * The WhatsApp bridge (`scripts/whatsapp-bridge/`)


The entrypoint script (`docker/entrypoint.sh`) bootstraps the data volume on first run:
  * Creates the directory structure (`sessions/`, `memories/`, `skills/`, etc.)
  * Copies `.env.example` → `.env` if no `.env` exists
  * Copies default `config.yaml` if missing
  * Copies default `SOUL.md` if missing
  * Syncs bundled skills using a manifest-based approach (preserves user edits)
  * Optionally launches `hermes dashboard` as a background side-process when `HERMES_DASHBOARD=1` (see [Running the dashboard](<#running-the-dashboard>))
  * Then runs `hermes` with whatever arguments you pass


## Upgrading[​](<#upgrading> "Direct link to Upgrading")
Pull the latest image and recreate the container. Your data directory is untouched.
[code] 
    docker pull nousresearch/hermes-agent:latest  
    docker rm -f hermes  
    docker run -d \  
      --name hermes \  
      --restart unless-stopped \  
      -v ~/.hermes:/opt/data \  
      nousresearch/hermes-agent gateway run  
    
[/code]
Or with Docker Compose:
[code] 
    docker compose pull  
    docker compose up -d  
    
[/code]
## Skills and credential files[​](<#skills-and-credential-files> "Direct link to Skills and credential files")
When using Docker as the execution environment (not the methods above, but when the agent runs commands inside a Docker sandbox — see [Configuration → Docker Backend](</docs/user-guide/configuration#docker-backend>)), Hermes reuses a single long-lived container for all tool calls and automatically bind-mounts the skills directory (`~/.hermes/skills/`) and any credential files declared by skills into that container as read-only volumes. Skill scripts, templates, and references are available inside the sandbox without manual configuration, and because the container persists for the life of the Hermes process, any dependencies you install or files you write stay around for the next tool call.
The same syncing happens for SSH and Modal backends — skills and credential files are uploaded via rsync or the Modal mount API before each command.
## Connecting to local inference servers (vLLM, Ollama, etc.)[​](<#connecting-to-local-inference-servers-vllm-ollama-etc> "Direct link to Connecting to local inference servers \(vLLM, Ollama, etc.\)")
When running Hermes in Docker and your inference server (vLLM, Ollama, text-generation-inference, etc.) is also running on the host or in another container, networking requires extra attention.
### Docker Compose (recommended)[​](<#docker-compose-recommended> "Direct link to Docker Compose \(recommended\)")
Put both services on the same Docker network. This is the most reliable approach:
[code] 
    services:  
      vllm:  
        image: vllm/vllm-openai:latest  
        container_name: vllm  
        command: >  
          --model Qwen/Qwen2.5-7B-Instruct  
          --served-model-name my-model  
          --host 0.0.0.0  
          --port 8000  
        ports:  
          - "8000:8000"  
        networks:  
          - hermes-net  
        deploy:  
          resources:  
            reservations:  
              devices:  
                - capabilities: [gpu]  
      
      hermes:  
        image: nousresearch/hermes-agent:latest  
        container_name: hermes  
        restart: unless-stopped  
        command: gateway run  
        ports:  
          - "8642:8642"  
        volumes:  
          - ~/.hermes:/opt/data  
        networks:  
          - hermes-net  
      
    networks:  
      hermes-net:  
        driver: bridge  
    
[/code]
Then in your `~/.hermes/config.yaml`, use the **container name** as the hostname:
[code] 
    model:  
      provider: custom  
      model: my-model  
      base_url: http://vllm:8000/v1  
      api_key: "none"  
    
[/code]
Key points
  * Use the **container name** (`vllm`) as the hostname — not `localhost` or `127.0.0.1`, which refer to the Hermes container itself.
  * The `model` value must match the `--served-model-name` you passed to vLLM.
  * Set `api_key` to any non-empty string (vLLM requires the header but doesn't validate it by default).
  * Do **not** include a trailing slash in `base_url`.


### Standalone Docker run (no Compose)[​](<#standalone-docker-run-no-compose> "Direct link to Standalone Docker run \(no Compose\)")
If your inference server runs directly on the host (not in Docker), use `host.docker.internal` on macOS/Windows, or `--network host` on Linux:
**macOS / Windows:**
[code] 
    docker run -d \  
      --name hermes \  
      -v ~/.hermes:/opt/data \  
      -p 8642:8642 \  
      nousresearch/hermes-agent gateway run  
    
[/code]
[code] 
    # config.yaml  
    model:  
      provider: custom  
      model: my-model  
      base_url: http://host.docker.internal:8000/v1  
      api_key: "none"  
    
[/code]
**Linux (host networking):**
[code] 
    docker run -d \  
      --name hermes \  
      --network host \  
      -v ~/.hermes:/opt/data \  
      nousresearch/hermes-agent gateway run  
    
[/code]
[code] 
    # config.yaml  
    model:  
      provider: custom  
      model: my-model  
      base_url: http://127.0.0.1:8000/v1  
      api_key: "none"  
    
[/code]
With `--network host`, the `-p` flag is ignored — all container ports are directly exposed on the host.
### Verifying connectivity[​](<#verifying-connectivity> "Direct link to Verifying connectivity")
From inside the Hermes container, confirm the inference server is reachable:
[code] 
    docker exec hermes curl -s http://vllm:8000/v1/models  
    
[/code]
You should see a JSON response listing your served model. If this fails, check:
  1. Both containers are on the same Docker network (`docker network inspect hermes-net`)
  2. The inference server is listening on `0.0.0.0`, not `127.0.0.1`
  3. The port number matches


### Ollama[​](<#ollama> "Direct link to Ollama")
Ollama works the same way. If Ollama runs on the host, use `host.docker.internal:11434` (macOS/Windows) or `127.0.0.1:11434` (Linux with `--network host`). If Ollama runs in its own container on the same Docker network:
[code] 
    model:  
      provider: custom  
      model: llama3  
      base_url: http://ollama:11434/v1  
      api_key: "none"  
    
[/code]
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### Container exits immediately[​](<#container-exits-immediately> "Direct link to Container exits immediately")
Check logs: `docker logs hermes`. Common causes:
  * Missing or invalid `.env` file — run interactively first to complete setup
  * Port conflicts if running with exposed ports


### "Permission denied" errors[​](<#permission-denied-errors> "Direct link to "Permission denied" errors")
The container's entrypoint drops privileges to the non-root `hermes` user (UID 10000) via `gosu`. If your host `~/.hermes/` is owned by a different UID, set `HERMES_UID`/`HERMES_GID` to match your host user, or ensure the data directory is writable:
[code] 
    chmod -R 755 ~/.hermes  
    
[/code]
### Browser tools not working[​](<#browser-tools-not-working> "Direct link to Browser tools not working")
Playwright needs shared memory. Add `--shm-size=1g` to your Docker run command:
[code] 
    docker run -d \  
      --name hermes \  
      --shm-size=1g \  
      -v ~/.hermes:/opt/data \  
      nousresearch/hermes-agent gateway run  
    
[/code]
### Gateway not reconnecting after network issues[​](<#gateway-not-reconnecting-after-network-issues> "Direct link to Gateway not reconnecting after network issues")
The `--restart unless-stopped` flag handles most transient failures. If the gateway is stuck, restart the container:
[code] 
    docker restart hermes  
    
[/code]
### Checking container health[​](<#checking-container-health> "Direct link to Checking container health")
[code] 
    docker logs --tail 50 hermes          # Recent logs  
    docker run -it --rm nousresearch/hermes-agent:latest version     # Verify version  
    docker stats hermes                    # Resource usage  
    
[/code]
  * [Quick start](<#quick-start>)
  * [Running in gateway mode](<#running-in-gateway-mode>)
  * [Running the dashboard](<#running-the-dashboard>)
  * [Running interactively (CLI chat)](<#running-interactively-cli-chat>)
  * [Persistent volumes](<#persistent-volumes>)
  * [Multi-profile support](<#multi-profile-support>)
  * [Environment variable forwarding](<#environment-variable-forwarding>)
  * [Docker Compose example](<#docker-compose-example>)
  * [Resource limits](<#resource-limits>)
  * [What the Dockerfile does](<#what-the-dockerfile-does>)
  * [Upgrading](<#upgrading>)
  * [Skills and credential files](<#skills-and-credential-files>)
  * [Connecting to local inference servers (vLLM, Ollama, etc.)](<#connecting-to-local-inference-servers-vllm-ollama-etc>)
    * [Docker Compose (recommended)](<#docker-compose-recommended>)
    * [Standalone Docker run (no Compose)](<#standalone-docker-run-no-compose>)
    * [Verifying connectivity](<#verifying-connectivity>)
    * [Ollama](<#ollama>)
  * [Troubleshooting](<#troubleshooting>)
    * [Container exits immediately](<#container-exits-immediately>)
    * ["Permission denied" errors](<#permission-denied-errors>)
    * [Browser tools not working](<#browser-tools-not-working>)
    * [Gateway not reconnecting after network issues](<#gateway-not-reconnecting-after-network-issues>)
    * [Checking container health](<#checking-container-health>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/docker -->
