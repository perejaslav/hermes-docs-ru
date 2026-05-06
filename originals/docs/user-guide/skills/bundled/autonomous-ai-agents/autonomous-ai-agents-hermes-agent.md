On this page
Configure, extend, or contribute to Hermes Agent.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/autonomous-ai-agents/hermes-agent`  
Version| `2.1.0`  
Author| Hermes Agent + Teknium  
License| MIT  
Tags| `hermes`, `setup`, `configuration`, `multi-agent`, `spawning`, `cli`, `gateway`, `development`  
Related skills| [`claude-code`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code>), [`codex`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>), [`opencode`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Hermes Agent
Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others) and runs on Linux, macOS, and WSL.
What makes Hermes different:
  * **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
  * **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
  * **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
  * **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
  * **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
  * **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.


People use Hermes for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.
**This skill helps you work with Hermes Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.
**Docs:** <https://hermes-agent.nousresearch.com/docs/>
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
[code] 
    # Install  
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash  
      
    # Interactive chat (default)  
    hermes  
      
    # Single query  
    hermes chat -q "What is the capital of France?"  
      
    # Setup wizard  
    hermes setup  
      
    # Change model/provider  
    hermes model  
      
    # Check health  
    hermes doctor  
    
[/code]
* * *
## CLI Reference[​](<#cli-reference> "Direct link to CLI Reference")
### Global Flags[​](<#global-flags> "Direct link to Global Flags")
[code] 
    hermes [flags] [command]  
      
      --version, -V             Show version  
      --resume, -r SESSION      Resume session by ID or title  
      --continue, -c [NAME]     Resume by name, or most recent session  
      --worktree, -w            Isolated git worktree mode (parallel agents)  
      --skills, -s SKILL        Preload skills (comma-separate or repeat)  
      --profile, -p NAME        Use a named profile  
      --yolo                    Skip dangerous command approval  
      --pass-session-id         Include session ID in system prompt  
    
[/code]
No subcommand defaults to `chat`.
### Chat[​](<#chat> "Direct link to Chat")
[code] 
    hermes chat [flags]  
      -q, --query TEXT          Single query, non-interactive  
      -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)  
      -t, --toolsets LIST       Comma-separated toolsets  
      --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)  
      -v, --verbose             Verbose output  
      -Q, --quiet               Suppress banner, spinner, tool previews  
      --checkpoints             Enable filesystem checkpoints (/rollback)  
      --source TAG              Session source tag (default: cli)  
    
[/code]
### Configuration[​](<#configuration> "Direct link to Configuration")
[code] 
    hermes setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)  
    hermes model                Interactive model/provider picker  
    hermes config               View current config  
    hermes config edit          Open config.yaml in $EDITOR  
    hermes config set KEY VAL   Set a config value  
    hermes config path          Print config.yaml path  
    hermes config env-path      Print .env path  
    hermes config check         Check for missing/outdated config  
    hermes config migrate       Update config with new options  
    hermes login [--provider P] OAuth login (nous, openai-codex)  
    hermes logout               Clear stored auth  
    hermes doctor [--fix]       Check dependencies and config  
    hermes status [--all]       Show component status  
    
[/code]
### Tools & Skills[​](<#tools--skills> "Direct link to Tools & Skills")
[code] 
    hermes tools                Interactive tool enable/disable (curses UI)  
    hermes tools list           Show all tools and status  
    hermes tools enable NAME    Enable a toolset  
    hermes tools disable NAME   Disable a toolset  
      
    hermes skills list          List installed skills  
    hermes skills search QUERY  Search the skills hub  
    hermes skills install ID    Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override when frontmatter has no name)  
    hermes skills inspect ID    Preview without installing  
    hermes skills config        Enable/disable skills per platform  
    hermes skills check         Check for updates  
    hermes skills update        Update outdated skills  
    hermes skills uninstall N   Remove a hub skill  
    hermes skills publish PATH  Publish to registry  
    hermes skills browse        Browse all available skills  
    hermes skills tap add REPO  Add a GitHub repo as skill source  
    
[/code]
### MCP Servers[​](<#mcp-servers> "Direct link to MCP Servers")
[code] 
    hermes mcp serve            Run Hermes as an MCP server  
    hermes mcp add NAME         Add an MCP server (--url or --command)  
    hermes mcp remove NAME      Remove an MCP server  
    hermes mcp list             List configured servers  
    hermes mcp test NAME        Test connection  
    hermes mcp configure NAME   Toggle tool selection  
    
[/code]
### Gateway (Messaging Platforms)[​](<#gateway-messaging-platforms> "Direct link to Gateway \(Messaging Platforms\)")
[code] 
    hermes gateway run          Start gateway foreground  
    hermes gateway install      Install as background service  
    hermes gateway start/stop   Control the service  
    hermes gateway restart      Restart the service  
    hermes gateway status       Check status  
    hermes gateway setup        Configure platforms  
    
[/code]
Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.
Platform docs: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>
### Sessions[​](<#sessions> "Direct link to Sessions")
[code] 
    hermes sessions list        List recent sessions  
    hermes sessions browse      Interactive picker  
    hermes sessions export OUT  Export to JSONL  
    hermes sessions rename ID T Rename a session  
    hermes sessions delete ID   Delete a session  
    hermes sessions prune       Clean up old sessions (--older-than N days)  
    hermes sessions stats       Session store statistics  
    
[/code]
### Cron Jobs[​](<#cron-jobs> "Direct link to Cron Jobs")
[code] 
    hermes cron list            List jobs (--all for disabled)  
    hermes cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'  
    hermes cron edit ID         Edit schedule, prompt, delivery  
    hermes cron pause/resume ID Control job state  
    hermes cron run ID          Trigger on next tick  
    hermes cron remove ID       Delete a job  
    hermes cron status          Scheduler status  
    
[/code]
### Webhooks[​](<#webhooks> "Direct link to Webhooks")
[code] 
    hermes webhook subscribe N  Create route at /webhooks/<name>  
    hermes webhook list         List subscriptions  
    hermes webhook remove NAME  Remove a subscription  
    hermes webhook test NAME    Send a test POST  
    
[/code]
### Profiles[​](<#profiles> "Direct link to Profiles")
[code] 
    hermes profile list         List all profiles  
    hermes profile create NAME  Create (--clone, --clone-all, --clone-from)  
    hermes profile use NAME     Set sticky default  
    hermes profile delete NAME  Delete a profile  
    hermes profile show NAME    Show details  
    hermes profile alias NAME   Manage wrapper scripts  
    hermes profile rename A B   Rename a profile  
    hermes profile export NAME  Export to tar.gz  
    hermes profile import FILE  Import from archive  
    
[/code]
### Credential Pools[​](<#credential-pools> "Direct link to Credential Pools")
[code] 
    hermes auth add             Interactive credential wizard  
    hermes auth list [PROVIDER] List pooled credentials  
    hermes auth remove P INDEX  Remove by provider + index  
    hermes auth reset PROVIDER  Clear exhaustion status  
    
[/code]
### Other[​](<#other> "Direct link to Other")
[code] 
    hermes insights [--days N]  Usage analytics  
    hermes update               Update to latest version  
    hermes pairing list/approve/revoke  DM authorization  
    hermes plugins list/install/remove  Plugin management  
    hermes honcho setup/status  Honcho memory integration (requires honcho plugin)  
    hermes memory setup/status/off  Memory provider config  
    hermes completion bash|zsh  Shell completions  
    hermes acp                  ACP server (IDE integration)  
    hermes claw migrate         Migrate from OpenClaw  
    hermes uninstall            Uninstall Hermes  
    
[/code]
* * *
## Slash Commands (In-Session)[​](<#slash-commands-in-session> "Direct link to Slash Commands \(In-Session\)")
Type these during an interactive chat session. New commands land fairly often; if something below looks stale, run `/help` in-session for the authoritative list or see the [live slash commands reference](<https://hermes-agent.nousresearch.com/docs/reference/slash-commands>). The registry of record is `hermes_cli/commands.py` — every consumer (autocomplete, Telegram menu, Slack mapping, `/help`) derives from it.
### Session Control[​](<#session-control> "Direct link to Session Control")
[code] 
    /new (/reset)        Fresh session  
    /clear               Clear screen + new session (CLI)  
    /retry               Resend last message  
    /undo                Remove last exchange  
    /title [name]        Name the session  
    /compress            Manually compress context  
    /stop                Kill background processes  
    /rollback [N]        Restore filesystem checkpoint  
    /snapshot [sub]      Create or restore state snapshots of Hermes config/state (CLI)  
    /background <prompt> Run prompt in background  
    /queue <prompt>      Queue for next turn  
    /steer <prompt>      Inject a message after the next tool call without interrupting  
    /agents (/tasks)     Show active agents and running tasks  
    /resume [name]       Resume a named session  
    /goal [text|sub]     Set a standing goal Hermes works on across turns until achieved  
                         (subcommands: status, pause, resume, clear)  
    /redraw              Force a full UI repaint (CLI)  
    
[/code]
### Configuration[​](<#configuration-1> "Direct link to Configuration")
[code] 
    /config              Show config (CLI)  
    /model [name]        Show or change model  
    /personality [name]  Set personality  
    /reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)  
    /verbose             Cycle: off → new → all → verbose  
    /voice [on|off|tts]  Voice mode  
    /yolo                Toggle approval bypass  
    /busy [sub]          Control what Enter does while Hermes is working (CLI)  
                         (subcommands: queue, steer, interrupt, status)  
    /indicator [style]   Pick the TUI busy-indicator style (CLI)  
                         (styles: kaomoji, emoji, unicode, ascii)  
    /footer [on|off]     Toggle gateway runtime-metadata footer on final replies  
    /skin [name]         Change theme (CLI)  
    /statusbar           Toggle status bar (CLI)  
    
[/code]
### Tools & Skills[​](<#tools--skills-1> "Direct link to Tools & Skills")
[code] 
    /tools               Manage tools (CLI)  
    /toolsets            List toolsets (CLI)  
    /skills              Search/install skills (CLI)  
    /skill <name>        Load a skill into session  
    /reload-skills       Re-scan ~/.hermes/skills/ for added/removed skills  
    /reload              Reload .env variables into the running session (CLI)  
    /reload-mcp          Reload MCP servers  
    /cron                Manage cron jobs (CLI)  
    /curator [sub]       Background skill maintenance (status, run, pin, archive, …)  
    /kanban [sub]        Multi-profile collaboration board (tasks, links, comments)  
    /plugins             List plugins (CLI)  
    
[/code]
### Gateway[​](<#gateway> "Direct link to Gateway")
[code] 
    /approve             Approve a pending command (gateway)  
    /deny                Deny a pending command (gateway)  
    /restart             Restart gateway (gateway)  
    /sethome             Set current chat as home channel (gateway)  
    /update              Update Hermes to latest (gateway)  
    /topic [sub]         Enable or inspect Telegram DM topic sessions (gateway)  
    /platforms (/gateway) Show platform connection status (gateway)  
    
[/code]
### Utility[​](<#utility> "Direct link to Utility")
[code] 
    /branch (/fork)      Branch the current session  
    /fast                Toggle priority/fast processing  
    /browser             Open CDP browser connection  
    /history             Show conversation history (CLI)  
    /save                Save conversation to file (CLI)  
    /copy [N]            Copy the last assistant response to clipboard (CLI)  
    /paste               Attach clipboard image (CLI)  
    /image               Attach local image file (CLI)  
    
[/code]
### Info[​](<#info> "Direct link to Info")
[code] 
    /help                Show commands  
    /commands [page]     Browse all commands (gateway)  
    /usage               Token usage  
    /insights [days]     Usage analytics  
    /gquota              Show Google Gemini Code Assist quota usage (CLI)  
    /status              Session info (gateway)  
    /profile             Active profile info  
    /debug               Upload debug report (system info + logs) and get shareable links  
    
[/code]
### Exit[​](<#exit> "Direct link to Exit")
[code] 
    /quit (/exit, /q)    Exit CLI  
    
[/code]
* * *
## Key Paths & Config[​](<#key-paths--config> "Direct link to Key Paths & Config")
[code] 
    ~/.hermes/config.yaml       Main configuration  
    ~/.hermes/.env              API keys and secrets  
    $HERMES_HOME/skills/        Installed skills  
    ~/.hermes/sessions/         Session transcripts  
    ~/.hermes/logs/             Gateway and error logs  
    ~/.hermes/auth.json         OAuth tokens and credential pools  
    ~/.hermes/hermes-agent/     Source code (if git-installed)  
    
[/code]
Profiles use `~/.hermes/profiles/<name>/` with the same layout.
### Config Sections[​](<#config-sections> "Direct link to Config Sections")
Edit with `hermes config edit` or `hermes config set section.key value`.
Section| Key options  
---|---  
`model`| `default`, `provider`, `base_url`, `api_key`, `context_length`  
`agent`| `max_turns` (90), `tool_use_enforcement`  
`terminal`| `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180)  
`compression`| `enabled`, `threshold` (0.50), `target_ratio` (0.20)  
`display`| `skin`, `tool_progress`, `show_reasoning`, `show_cost`  
`stt`| `enabled`, `provider` (local/groq/openai/mistral)  
`tts`| `provider` (edge/elevenlabs/openai/minimax/mistral/neutts)  
`memory`| `memory_enabled`, `user_profile_enabled`, `provider`  
`security`| `tirith_enabled`, `website_blocklist`  
`delegation`| `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort`  
`checkpoints`| `enabled`, `max_snapshots` (50)  
Full config reference: <https://hermes-agent.nousresearch.com/docs/user-guide/configuration>
### Providers[​](<#providers> "Direct link to Providers")
20+ providers supported. Set via `hermes model` or `hermes setup`.
Provider| Auth| Key env var  
---|---|---  
OpenRouter| API key| `OPENROUTER_API_KEY`  
Anthropic| API key| `ANTHROPIC_API_KEY`  
Nous Portal| OAuth| `hermes auth`  
OpenAI Codex| OAuth| `hermes auth`  
GitHub Copilot| Token| `COPILOT_GITHUB_TOKEN`  
Google Gemini| API key| `GOOGLE_API_KEY` or `GEMINI_API_KEY`  
DeepSeek| API key| `DEEPSEEK_API_KEY`  
xAI / Grok| API key| `XAI_API_KEY`  
Hugging Face| Token| `HF_TOKEN`  
Z.AI / GLM| API key| `GLM_API_KEY`  
MiniMax| API key| `MINIMAX_API_KEY`  
MiniMax CN| API key| `MINIMAX_CN_API_KEY`  
Kimi / Moonshot| API key| `KIMI_API_KEY`  
Alibaba / DashScope| API key| `DASHSCOPE_API_KEY`  
Xiaomi MiMo| API key| `XIAOMI_API_KEY`  
Kilo Code| API key| `KILOCODE_API_KEY`  
AI Gateway (Vercel)| API key| `AI_GATEWAY_API_KEY`  
OpenCode Zen| API key| `OPENCODE_ZEN_API_KEY`  
OpenCode Go| API key| `OPENCODE_GO_API_KEY`  
Qwen OAuth| OAuth| `hermes login --provider qwen-oauth`  
Custom endpoint| Config| `model.base_url` \+ `model.api_key` in config.yaml  
GitHub Copilot ACP| External| `COPILOT_CLI_PATH` or Copilot CLI  
Full provider docs: <https://hermes-agent.nousresearch.com/docs/integrations/providers>
### Toolsets[​](<#toolsets> "Direct link to Toolsets")
Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.
Toolset| What it provides  
---|---  
`web`| Web search and content extraction  
`search`| Web search only (subset of `web`)  
`browser`| Browser automation (Browserbase, Camofox, or local Chromium)  
`terminal`| Shell commands and process management  
`file`| File read/write/search/patch  
`code_execution`| Sandboxed Python execution  
`vision`| Image analysis  
`image_gen`| AI image generation  
`video`| Video analysis and generation  
`tts`| Text-to-speech  
`skills`| Skill browsing and management  
`memory`| Persistent cross-session memory  
`session_search`| Search past conversations  
`delegation`| Subagent task delegation  
`cronjob`| Scheduled task management  
`clarify`| Ask user clarifying questions  
`messaging`| Cross-platform message sending  
`todo`| In-session task planning and tracking  
`kanban`| Multi-agent work-queue tools (gated to workers)  
`debugging`| Extra introspection/debug tools (off by default)  
`safe`| Minimal, low-risk toolset for locked-down sessions  
`spotify`| Spotify playback and playlist control  
`homeassistant`| Smart home control (off by default)  
`discord`| Discord integration tools  
`discord_admin`| Discord admin/moderation tools  
`feishu_doc`| Feishu (Lark) document tools  
`feishu_drive`| Feishu (Lark) drive tools  
`yuanbao`| Yuanbao integration tools  
`rl`| Reinforcement learning tools (off by default)  
`moa`| Mixture of Agents (off by default)  
Full enumeration lives in `toolsets.py` as the `TOOLSETS` dict; `_HERMES_CORE_TOOLS` is the default bundle most platforms inherit from.
Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.
* * *
## Security & Privacy Toggles[​](<#security--privacy-toggles> "Direct link to Security & Privacy Toggles")
Common "why is Hermes doing X to my output / tool calls / commands?" toggles — and the exact commands to change them. Most of these need a fresh session (`/reset` in chat, or start a new `hermes` invocation) because they're read once at startup.
### Secret redaction in tool output[​](<#secret-redaction-in-tool-output> "Direct link to Secret redaction in tool output")
Secret redaction is **off by default** — tool output (terminal stdout, `read_file`, web content, subagent summaries, etc.) passes through unmodified. If the user wants Hermes to auto-mask strings that look like API keys, tokens, and secrets before they enter the conversation context and logs:
[code] 
    hermes config set security.redact_secrets true       # enable globally  
    
[/code]
**Restart required.** `security.redact_secrets` is snapshotted at import time — toggling it mid-session (e.g. via `export HERMES_REDACT_SECRETS=true` from a tool call) will NOT take effect for the running process. Tell the user to run `hermes config set security.redact_secrets true` in a terminal, then start a new session. This is deliberate — it prevents an LLM from flipping the toggle on itself mid-task.
Disable again with:
[code] 
    hermes config set security.redact_secrets false  
    
[/code]
### PII redaction in gateway messages[​](<#pii-redaction-in-gateway-messages> "Direct link to PII redaction in gateway messages")
Separate from secret redaction. When enabled, the gateway hashes user IDs and strips phone numbers from the session context before it reaches the model:
[code] 
    hermes config set privacy.redact_pii true    # enable  
    hermes config set privacy.redact_pii false   # disable (default)  
    
[/code]
### Command approval prompts[​](<#command-approval-prompts> "Direct link to Command approval prompts")
By default (`approvals.mode: manual`), Hermes prompts the user before running shell commands flagged as destructive (`rm -rf`, `git reset --hard`, etc.). The modes are:
  * `manual` — always prompt (default)
  * `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt on high-risk
  * `off` — skip all approval prompts (equivalent to `--yolo`)


[code] 
    hermes config set approvals.mode smart       # recommended middle ground  
    hermes config set approvals.mode off         # bypass everything (not recommended)  
    
[/code]
Per-invocation bypass without changing config:
  * `hermes --yolo …`
  * `export HERMES_YOLO_MODE=1`


Note: YOLO / `approvals.mode: off` does NOT turn off secret redaction. They are independent.
### Shell hooks allowlist[​](<#shell-hooks-allowlist> "Direct link to Shell hooks allowlist")
Some shell-hook integrations require explicit allowlisting before they fire. Managed via `~/.hermes/shell-hooks-allowlist.json` — prompted interactively the first time a hook wants to run.
### Disabling the web/browser/image-gen tools[​](<#disabling-the-webbrowserimage-gen-tools> "Direct link to Disabling the web/browser/image-gen tools")
To keep the model away from network or media tools entirely, open `hermes tools` and toggle per-platform. Takes effect on next session (`/reset`). See the Tools & Skills section above.
* * *
## Voice & Transcription[​](<#voice--transcription> "Direct link to Voice & Transcription")
### STT (Voice → Text)[​](<#stt-voice--text> "Direct link to STT \(Voice → Text\)")
Voice messages from messaging platforms are auto-transcribed.
Provider priority (auto-detected):
  1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
  2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
  3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
  4. **Mistral Voxtral** — set `MISTRAL_API_KEY`


Config:
[code] 
    stt:  
      enabled: true  
      provider: local        # local, groq, openai, mistral  
      local:  
        model: base          # tiny, base, small, medium, large-v3  
    
[/code]
### TTS (Text → Voice)[​](<#tts-text--voice> "Direct link to TTS \(Text → Voice\)")
Provider| Env var| Free?  
---|---|---  
Edge TTS| None| Yes (default)  
ElevenLabs| `ELEVENLABS_API_KEY`| Free tier  
OpenAI| `VOICE_TOOLS_OPENAI_KEY`| Paid  
MiniMax| `MINIMAX_API_KEY`| Paid  
Mistral (Voxtral)| `MISTRAL_API_KEY`| Paid  
NeuTTS (local)| None (`pip install neutts[all]` \+ `espeak-ng`)| Free  
Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.
* * *
## Spawning Additional Hermes Instances[​](<#spawning-additional-hermes-instances> "Direct link to Spawning Additional Hermes Instances")
Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.
### When to Use This vs delegate_task[​](<#when-to-use-this-vs-delegate_task> "Direct link to When to Use This vs delegate_task")
| `delegate_task`| Spawning `hermes` process  
---|---|---  
Isolation| Separate conversation, shared process| Fully independent process  
Duration| Minutes (bounded by parent loop)| Hours/days  
Tool access| Subset of parent's tools| Full tool access  
Interactive| No| Yes (PTY mode)  
Use case| Quick parallel subtasks| Long autonomous missions  
### One-Shot Mode[​](<#one-shot-mode> "Direct link to One-Shot Mode")
[code] 
    terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)  
      
    # Background for long tasks:  
    terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)  
    
[/code]
### Interactive PTY Mode (via tmux)[​](<#interactive-pty-mode-via-tmux> "Direct link to Interactive PTY Mode \(via tmux\)")
Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:
[code] 
    # Start  
    terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)  
      
    # Wait for startup, then send a message  
    terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)  
      
    # Read output  
    terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)  
      
    # Send follow-up  
    terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)  
      
    # Exit  
    terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)  
    
[/code]
### Multi-Agent Coordination[​](<#multi-agent-coordination> "Direct link to Multi-Agent Coordination")
[code] 
    # Agent A: backend  
    terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)  
    terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)  
      
    # Agent B: frontend  
    terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)  
    terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)  
      
    # Check progress, relay context between them  
    terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)  
    terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)  
    
[/code]
### Session Resume[​](<#session-resume> "Direct link to Session Resume")
[code] 
    # Resume most recent session  
    terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)  
      
    # Resume specific session  
    terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)  
    
[/code]
### Tips[​](<#tips> "Direct link to Tips")
  * **Prefer`delegate_task` for quick subtasks** — less overhead than spawning a full process
  * **Use`-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
  * **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
  * **Use`hermes chat -q` for fire-and-forget** — no PTY needed
  * **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit
  * **For scheduled tasks** , use the `cronjob` tool instead of spawning — handles delivery and retry


* * *
## Durable & Background Systems[​](<#durable--background-systems> "Direct link to Durable & Background Systems")
Four systems run alongside the main conversation loop. Quick reference here; full developer notes live in `AGENTS.md`, user-facing docs under `website/docs/user-guide/features/`.
### Delegation (`delegate_task`)[​](<#delegation-delegate_task> "Direct link to delegation-delegate_task")
Synchronous subagent spawn — the parent waits for the child's summary before continuing its own loop. Isolated context + terminal session.
  * **Single:** `delegate_task(goal, context, toolsets)`.
  * **Batch:** `delegate_task(tasks=[{goal, ...}, ...])` runs children in parallel, capped by `delegation.max_concurrent_children` (default 3).
  * **Roles:** `leaf` (default; cannot re-delegate) vs `orchestrator` (can spawn its own workers, bounded by `delegation.max_spawn_depth`).
  * **Not durable.** If the parent is interrupted, the child is cancelled. For work that must outlive the turn, use `cronjob` or `terminal(background=True, notify_on_complete=True)`.


Config: `delegation.*` in `config.yaml`.
### Cron (scheduled jobs)[​](<#cron-scheduled-jobs> "Direct link to Cron \(scheduled jobs\)")
Durable scheduler — `cron/jobs.py` \+ `cron/scheduler.py`. Drive it via the `cronjob` tool, the `hermes cron` CLI (`list`, `add`, `edit`, `pause`, `resume`, `run`, `remove`), or the `/cron` slash command.
  * **Schedules:** duration (`"30m"`, `"2h"`), "every" phrase (`"every monday 9am"`), 5-field cron (`"0 9 * * *"`), or ISO timestamp.
  * **Per-job knobs:** `skills`, `model`/`provider` override, `script` (pre-run data collection; `no_agent=True` makes the script the whole job), `context_from` (chain job A's output into job B), `workdir` (run in a specific dir with its `AGENTS.md` / `CLAUDE.md` loaded), multi-platform delivery.
  * **Invariants:** 3-minute hard interrupt per run, `.tick.lock` file prevents duplicate ticks across processes, cron sessions pass `skip_memory=True` by default, and cron deliveries are framed with a header/footer instead of being mirrored into the target gateway session (keeps role alternation intact).


User docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>
### Curator (skill lifecycle)[​](<#curator-skill-lifecycle> "Direct link to Curator \(skill lifecycle\)")
Background maintenance for agent-created skills. Tracks usage, marks idle skills stale, archives stale ones, keeps a pre-run tar.gz backup so nothing is lost.
  * **CLI:** `hermes curator <verb>` — `status`, `run`, `pause`, `resume`, `pin`, `unpin`, `archive`, `restore`, `prune`, `backup`, `rollback`.
  * **Slash:** `/curator <subcommand>` mirrors the CLI.
  * **Scope:** only touches skills with `created_by: "agent"` provenance. Bundled + hub-installed skills are off-limits. **Never deletes** — max destructive action is archive. Pinned skills are exempt from every auto-transition and every LLM review pass.
  * **Telemetry:** sidecar at `~/.hermes/skills/.usage.json` holds per-skill `use_count`, `view_count`, `patch_count`, `last_activity_at`, `state`, `pinned`.


Config: `curator.*` (`enabled`, `interval_hours`, `min_idle_hours`, `stale_after_days`, `archive_after_days`, `backup.*`). User docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/curator>
### Kanban (multi-agent work queue)[​](<#kanban-multi-agent-work-queue> "Direct link to Kanban \(multi-agent work queue\)")
Durable SQLite board for multi-profile / multi-worker collaboration. Users drive it via `hermes kanban <verb>`; dispatcher-spawned workers see a focused `kanban_*` toolset gated by `HERMES_KANBAN_TASK` so the schema footprint is zero outside worker processes.
  * **CLI verbs (common):** `init`, `create`, `list` (alias `ls`), `show`, `assign`, `link`, `unlink`, `comment`, `complete`, `block`, `unblock`, `archive`, `tail`. Less common: `watch`, `stats`, `runs`, `log`, `dispatch`, `daemon`, `gc`.
  * **Worker toolset:** `kanban_show`, `kanban_complete`, `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`, `kanban_link`.
  * **Dispatcher** runs inside the gateway by default (`kanban.dispatch_in_gateway: true`) — reclaims stale claims, promotes ready tasks, atomically claims, spawns assigned profiles. Auto-blocks a task after ~5 consecutive spawn failures.
  * **Isolation:** board is the hard boundary (workers get `HERMES_KANBAN_BOARD` pinned in env); tenant is a soft namespace within a board for workspace-path + memory-key isolation.


User docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban>
* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### Voice not working[​](<#voice-not-working> "Direct link to Voice not working")
  1. Check `stt.enabled: true` in config.yaml
  2. Verify provider: `pip install faster-whisper` or set API key
  3. In gateway: `/restart`. In CLI: exit and relaunch.


### Tool not available[​](<#tool-not-available> "Direct link to Tool not available")
  1. `hermes tools` — check if toolset is enabled for your platform
  2. Some tools need env vars (check `.env`)
  3. `/reset` after enabling tools


### Model/provider issues[​](<#modelprovider-issues> "Direct link to Model/provider issues")
  1. `hermes doctor` — check config and dependencies
  2. `hermes login` — re-authenticate OAuth providers
  3. Check `.env` has the right API key
  4. **Copilot 403** : `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.


### Changes not taking effect[​](<#changes-not-taking-effect> "Direct link to Changes not taking effect")
  * **Tools/skills:** `/reset` starts a new session with updated toolset
  * **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
  * **Code changes:** Restart the CLI or gateway process


### Skills not showing[​](<#skills-not-showing> "Direct link to Skills not showing")
  1. `hermes skills list` — verify installed
  2. `hermes skills config` — check platform enablement
  3. Load explicitly: `/skill name` or `hermes -s name`


### Gateway issues[​](<#gateway-issues> "Direct link to Gateway issues")
Check logs first:
[code] 
    grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20  
    
[/code]
Common gateway problems:
  * **Gateway dies on SSH logout** : Enable linger: `sudo loginctl enable-linger $USER`
  * **Gateway dies on WSL2 close** : WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
  * **Gateway crash loop** : Reset the failed state: `systemctl --user reset-failed hermes-gateway`


### Platform-specific issues[​](<#platform-specific-issues> "Direct link to Platform-specific issues")
  * **Discord bot silent** : Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
  * **Slack bot only works in DMs** : Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
  * **Windows HTTP 400 "No models provided"** : Config file encoding issue (BOM). Ensure `config.yaml` is saved as UTF-8 without BOM.


### Auxiliary models not working[​](<#auxiliary-models-not-working> "Direct link to Auxiliary models not working")
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
[code] 
    hermes config set auxiliary.vision.provider <your_provider>  
    hermes config set auxiliary.vision.model <model_name>  
    
[/code]
* * *
## Where to Find Things[​](<#where-to-find-things> "Direct link to Where to Find Things")
Looking for...| Location  
---|---  
Config options| `hermes config edit` or [Configuration docs](<https://hermes-agent.nousresearch.com/docs/user-guide/configuration>)  
Available tools| `hermes tools list` or [Tools reference](<https://hermes-agent.nousresearch.com/docs/reference/tools-reference>)  
Slash commands| `/help` in session or [Slash commands reference](<https://hermes-agent.nousresearch.com/docs/reference/slash-commands>)  
Skills catalog| `hermes skills browse` or [Skills catalog](<https://hermes-agent.nousresearch.com/docs/reference/skills-catalog>)  
Provider setup| `hermes model` or [Providers guide](<https://hermes-agent.nousresearch.com/docs/integrations/providers>)  
Platform setup| `hermes gateway setup` or [Messaging docs](<https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>)  
MCP servers| `hermes mcp list` or [MCP guide](<https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp>)  
Profiles| `hermes profile list` or [Profiles docs](<https://hermes-agent.nousresearch.com/docs/user-guide/profiles>)  
Cron jobs| `hermes cron list` or [Cron docs](<https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>)  
Memory| `hermes memory status` or [Memory docs](<https://hermes-agent.nousresearch.com/docs/user-guide/features/memory>)  
Env variables| `hermes config env-path` or [Env vars reference](<https://hermes-agent.nousresearch.com/docs/reference/environment-variables>)  
CLI commands| `hermes --help` or [CLI reference](<https://hermes-agent.nousresearch.com/docs/reference/cli-commands>)  
Gateway logs| `~/.hermes/logs/gateway.log`  
Session files| `~/.hermes/sessions/` or `hermes sessions browse`  
Source code| `~/.hermes/hermes-agent/`  
* * *
## Contributor Quick Reference[​](<#contributor-quick-reference> "Direct link to Contributor Quick Reference")
For occasional contributors and PR authors. Full developer docs: <https://hermes-agent.nousresearch.com/docs/developer-guide/>
### Project Layout[​](<#project-layout> "Direct link to Project Layout")
[code] 
    hermes-agent/  
    ├── run_agent.py          # AIAgent — core conversation loop  
    ├── model_tools.py        # Tool discovery and dispatch  
    ├── toolsets.py           # Toolset definitions  
    ├── cli.py                # Interactive CLI (HermesCLI)  
    ├── hermes_state.py       # SQLite session store  
    ├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch  
    ├── hermes_cli/           # CLI subcommands, config, setup, commands  
    │   ├── commands.py       # Slash command registry (CommandDef)  
    │   ├── config.py         # DEFAULT_CONFIG, env var definitions  
    │   └── main.py           # CLI entry point and argparse  
    ├── tools/                # One file per tool  
    │   └── registry.py       # Central tool registry  
    ├── gateway/              # Messaging gateway  
    │   └── platforms/        # Platform adapters (telegram, discord, etc.)  
    ├── cron/                 # Job scheduler  
    ├── tests/                # ~3000 pytest tests  
    └── website/              # Docusaurus docs site  
    
[/code]
Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys).
### Adding a Tool (3 files)[​](<#adding-a-tool-3-files> "Direct link to Adding a Tool \(3 files\)")
**1\. Create`tools/your_tool.py`:**
[code] 
    import json, os  
    from tools.registry import registry  
      
    def check_requirements() -> bool:  
        return bool(os.getenv("EXAMPLE_API_KEY"))  
      
    def example_tool(param: str, task_id: str = None) -> str:  
        return json.dumps({"success": True, "data": "..."})  
      
    registry.register(  
        name="example_tool",  
        toolset="example",  
        schema={"name": "example_tool", "description": "...", "parameters": {...}},  
        handler=lambda args, **kw: example_tool(  
            param=args.get("param", ""), task_id=kw.get("task_id")),  
        check_fn=check_requirements,  
        requires_env=["EXAMPLE_API_KEY"],  
    )  
    
[/code]
**2\. Add to`toolsets.py`** → `_HERMES_CORE_TOOLS` list.
Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.
All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `~/.hermes`.
### Adding a Slash Command[​](<#adding-a-slash-command> "Direct link to Adding a Slash Command")
  1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
  2. Add handler in `cli.py` → `process_command()`
  3. (Optional) Add gateway handler in `gateway/run.py`


All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.
### Agent Loop (High Level)[​](<#agent-loop-high-level> "Direct link to Agent Loop \(High Level\)")
[code] 
    run_conversation():  
      1. Build system prompt  
      2. Loop while iterations < max:  
         a. Call LLM (OpenAI-format messages + tool schemas)  
         b. If tool_calls → dispatch each via handle_function_call() → append results → continue  
         c. If text response → return  
      3. Context compression triggers automatically near token limit  
    
[/code]
### Testing[​](<#testing> "Direct link to Testing")
[code] 
    python -m pytest tests/ -o 'addopts=' -q   # Full suite  
    python -m pytest tests/tools/ -q            # Specific area  
    
[/code]
  * Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`
  * Run full suite before pushing any change
  * Use `-o 'addopts='` to clear any baked-in pytest flags


### Commit Conventions[​](<#commit-conventions> "Direct link to Commit Conventions")
[code] 
    type: concise subject line  
      
    Optional body.  
    
[/code]
Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`
### Key Rules[​](<#key-rules> "Direct link to Key Rules")
  * **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
  * **Message role alternation** — never two assistant or two user messages in a row
  * Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
  * Config values go in `config.yaml`, secrets go in `.env`
  * New tools need a `check_fn` so they only appear when requirements are met


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Quick Start](<#quick-start>)
  * [CLI Reference](<#cli-reference>)
    * [Global Flags](<#global-flags>)
    * [Chat](<#chat>)
    * [Configuration](<#configuration>)
    * [Tools & Skills](<#tools--skills>)
    * [MCP Servers](<#mcp-servers>)
    * [Gateway (Messaging Platforms)](<#gateway-messaging-platforms>)
    * [Sessions](<#sessions>)
    * [Cron Jobs](<#cron-jobs>)
    * [Webhooks](<#webhooks>)
    * [Profiles](<#profiles>)
    * [Credential Pools](<#credential-pools>)
    * [Other](<#other>)
  * [Slash Commands (In-Session)](<#slash-commands-in-session>)
    * [Session Control](<#session-control>)
    * [Configuration](<#configuration-1>)
    * [Tools & Skills](<#tools--skills-1>)
    * [Gateway](<#gateway>)
    * [Utility](<#utility>)
    * [Info](<#info>)
    * [Exit](<#exit>)
  * [Key Paths & Config](<#key-paths--config>)
    * [Config Sections](<#config-sections>)
    * [Providers](<#providers>)
    * [Toolsets](<#toolsets>)
  * [Security & Privacy Toggles](<#security--privacy-toggles>)
    * [Secret redaction in tool output](<#secret-redaction-in-tool-output>)
    * [PII redaction in gateway messages](<#pii-redaction-in-gateway-messages>)
    * [Command approval prompts](<#command-approval-prompts>)
    * [Shell hooks allowlist](<#shell-hooks-allowlist>)
    * [Disabling the web/browser/image-gen tools](<#disabling-the-webbrowserimage-gen-tools>)
  * [Voice & Transcription](<#voice--transcription>)
    * [STT (Voice → Text)](<#stt-voice--text>)
    * [TTS (Text → Voice)](<#tts-text--voice>)
  * [Spawning Additional Hermes Instances](<#spawning-additional-hermes-instances>)
    * [When to Use This vs delegate_task](<#when-to-use-this-vs-delegate_task>)
    * [One-Shot Mode](<#one-shot-mode>)
    * [Interactive PTY Mode (via tmux)](<#interactive-pty-mode-via-tmux>)
    * [Multi-Agent Coordination](<#multi-agent-coordination>)
    * [Session Resume](<#session-resume>)
    * [Tips](<#tips>)
  * [Durable & Background Systems](<#durable--background-systems>)
    * [Delegation (`delegate_task`)](<#delegation-delegate_task>)
    * [Cron (scheduled jobs)](<#cron-scheduled-jobs>)
    * [Curator (skill lifecycle)](<#curator-skill-lifecycle>)
    * [Kanban (multi-agent work queue)](<#kanban-multi-agent-work-queue>)
  * [Troubleshooting](<#troubleshooting>)
    * [Voice not working](<#voice-not-working>)
    * [Tool not available](<#tool-not-available>)
    * [Model/provider issues](<#modelprovider-issues>)
    * [Changes not taking effect](<#changes-not-taking-effect>)
    * [Skills not showing](<#skills-not-showing>)
    * [Gateway issues](<#gateway-issues>)
    * [Platform-specific issues](<#platform-specific-issues>)
    * [Auxiliary models not working](<#auxiliary-models-not-working>)
  * [Where to Find Things](<#where-to-find-things>)
  * [Contributor Quick Reference](<#contributor-quick-reference>)
    * [Project Layout](<#project-layout>)
    * [Adding a Tool (3 files)](<#adding-a-tool-3-files>)
    * [Adding a Slash Command](<#adding-a-slash-command>)
    * [Agent Loop (High Level)](<#agent-loop-high-level>)
    * [Testing](<#testing>)
    * [Commit Conventions](<#commit-conventions>)
    * [Key Rules](<#key-rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent -->
