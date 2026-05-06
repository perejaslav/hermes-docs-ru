On this page
The messaging gateway is the long-running process that connects Hermes to 14+ external messaging platforms through a unified architecture.
## Key Files[​](<#key-files> "Direct link to Key Files")
File| Purpose  
---|---  
`gateway/run.py`| `GatewayRunner` — main loop, slash commands, message dispatch (~12,000 lines)  
`gateway/session.py`| `SessionStore` — conversation persistence and session key construction  
`gateway/delivery.py`| Outbound message delivery to target platforms/channels  
`gateway/pairing.py`| DM pairing flow for user authorization  
`gateway/channel_directory.py`| Maps chat IDs to human-readable names for cron delivery  
`gateway/hooks.py`| Hook discovery, loading, and lifecycle event dispatch  
`gateway/mirror.py`| Cross-session message mirroring for `send_message`  
`gateway/status.py`| Token lock management for profile-scoped gateway instances  
`gateway/builtin_hooks/`| Extension point for always-registered hooks (none shipped)  
`gateway/platforms/`| Platform adapters (one per messaging platform)  
## Architecture Overview[​](<#architecture-overview> "Direct link to Architecture Overview")
[code] 
    ┌─────────────────────────────────────────────────┐  
    │                  GatewayRunner                  │  
    │                                                 │  
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │  
    │  │ Telegram │  │ Discord  │  │  Slack   │       │  
    │  │ Adapter  │  │ Adapter  │  │ Adapter  │       │  
    │  └────┬─────┘  └────┬─────┘  └────┬─────┘       │  
    │       │             │             │             │  
    │       └─────────────┼─────────────┘             │  
    │                     ▼                           │  
    │              _handle_message()                  │  
    │                     │                           │  
    │         ┌───────────┼───────────┐               │  
    │         ▼           ▼           ▼               │  
    │  Slash command   AIAgent    Queue/BG            │  
    │    dispatch      creation   sessions            │  
    │                     │                           │  
    │                     ▼                           │  
    │                 SessionStore                    │  
    │              (SQLite persistence)               │  
    └───────┴─────────────┴─────────────┴─────────────┘  
    
[/code]
## Message Flow[​](<#message-flow> "Direct link to Message Flow")
When a message arrives from any platform:
  1. **Platform adapter** receives raw event, normalizes it into a `MessageEvent`
  2. **Base adapter** checks active session guard:
     * If agent is running for this session → queue message, set interrupt event
     * If `/approve`, `/deny`, `/stop` → bypass guard (dispatched inline)
  3. **GatewayRunner._handle_message()** receives the event:
     * Resolve session key via `_session_key_for_source()` (format: `agent:main:{platform}:{chat_type}:{chat_id}`)
     * Check authorization (see Authorization below)
     * Check if it's a slash command → dispatch to command handler
     * Check if agent is already running → intercept commands like `/stop`, `/status`
     * Otherwise → create `AIAgent` instance and run conversation
  4. **Response** is sent back through the platform adapter


### Session Key Format[​](<#session-key-format> "Direct link to Session Key Format")
Session keys encode the full routing context:
[code] 
    agent:main:{platform}:{chat_type}:{chat_id}  
    
[/code]
For example: `agent:main:telegram:private:123456789`
Thread-aware platforms (Telegram forum topics, Discord threads, Slack threads) may include thread IDs in the chat_id portion. **Never construct session keys manually** — always use `build_session_key()` from `gateway/session.py`.
### Two-Level Message Guard[​](<#two-level-message-guard> "Direct link to Two-Level Message Guard")
When an agent is actively running, incoming messages pass through two sequential guards:
  1. **Level 1 — Base adapter** (`gateway/platforms/base.py`): Checks `_active_sessions`. If the session is active, queues the message in `_pending_messages` and sets an interrupt event. This catches messages _before_ they reach the gateway runner.
  2. **Level 2 — Gateway runner** (`gateway/run.py`): Checks `_running_agents`. Intercepts specific commands (`/stop`, `/new`, `/queue`, `/status`, `/approve`, `/deny`) and routes them appropriately. Everything else triggers `running_agent.interrupt()`.


Commands that must reach the runner while the agent is blocked (like `/approve`) are dispatched **inline** via `await self._message_handler(event)` — they bypass the background task system to avoid race conditions.
## Authorization[​](<#authorization> "Direct link to Authorization")
The gateway uses a multi-layer authorization check, evaluated in order:
  1. **Per-platform allow-all flag** (e.g., `TELEGRAM_ALLOW_ALL_USERS`) — if set, all users on that platform are authorized
  2. **Platform allowlist** (e.g., `TELEGRAM_ALLOWED_USERS`) — comma-separated user IDs
  3. **DM pairing** — authenticated users can pair new users via a pairing code
  4. **Global allow-all** (`GATEWAY_ALLOW_ALL_USERS`) — if set, all users across all platforms are authorized
  5. **Default: deny** — unauthorized users are rejected


### DM Pairing Flow[​](<#dm-pairing-flow> "Direct link to DM Pairing Flow")
[code] 
    Admin: /pair  
    Gateway: "Pairing code: ABC123. Share with the user."  
    New user: ABC123  
    Gateway: "Paired! You're now authorized."  
    
[/code]
Pairing state is persisted in `gateway/pairing.py` and survives restarts.
## Slash Command Dispatch[​](<#slash-command-dispatch> "Direct link to Slash Command Dispatch")
All slash commands in the gateway flow through the same resolution pipeline:
  1. `resolve_command()` from `hermes_cli/commands.py` maps input to canonical name (handles aliases, prefix matching)
  2. The canonical name is checked against `GATEWAY_KNOWN_COMMANDS`
  3. Handler in `_handle_message()` dispatches based on canonical name
  4. Some commands are gated on config (`gateway_config_gate` on `CommandDef`)


### Running-Agent Guard[​](<#running-agent-guard> "Direct link to Running-Agent Guard")
Commands that must NOT execute while the agent is processing are rejected early:
[code] 
    if _quick_key in self._running_agents:  
        if canonical == "model":  
            return "⏳ Agent is running — wait for it to finish or /stop first."  
    
[/code]
Bypass commands (`/stop`, `/new`, `/approve`, `/deny`, `/queue`, `/status`) have special handling.
## Config Sources[​](<#config-sources> "Direct link to Config Sources")
The gateway reads configuration from multiple sources:
Source| What it provides  
---|---  
`~/.hermes/.env`| API keys, bot tokens, platform credentials  
`~/.hermes/config.yaml`| Model settings, tool configuration, display options  
Environment variables| Override any of the above  
Unlike the CLI (which uses `load_cli_config()` with hardcoded defaults), the gateway reads `config.yaml` directly via YAML loader. This means config keys that exist in the CLI's defaults dict but not in the user's config file may behave differently between CLI and gateway.
## Platform Adapters[​](<#platform-adapters> "Direct link to Platform Adapters")
Each messaging platform has an adapter in `gateway/platforms/`:
[code] 
    gateway/platforms/  
    ├── base.py              # BaseAdapter — shared logic for all platforms  
    ├── telegram.py          # Telegram Bot API (long polling or webhook)  
    ├── discord.py           # Discord bot via discord.py  
    ├── slack.py             # Slack Socket Mode  
    ├── whatsapp.py          # WhatsApp Business Cloud API  
    ├── signal.py            # Signal via signal-cli REST API  
    ├── matrix.py            # Matrix via mautrix (optional E2EE)  
    ├── mattermost.py        # Mattermost WebSocket API  
    ├── email.py             # Email via IMAP/SMTP  
    ├── sms.py               # SMS via Twilio  
    ├── dingtalk.py          # DingTalk WebSocket  
    ├── feishu.py            # Feishu/Lark WebSocket or webhook  
    ├── wecom.py             # WeCom (WeChat Work) callback  
    ├── weixin.py            # Weixin (personal WeChat) via iLink Bot API  
    ├── bluebubbles.py       # Apple iMessage via BlueBubbles macOS server  
    ├── qqbot.py             # QQ Bot (Tencent QQ) via Official API v2  
    ├── webhook.py           # Inbound/outbound webhook adapter  
    ├── api_server.py        # REST API server adapter  
    └── homeassistant.py     # Home Assistant conversation integration  
    
[/code]
Adapters implement a common interface:
  * `connect()` / `disconnect()` — lifecycle management
  * `send_message()` — outbound message delivery
  * `on_message()` — inbound message normalization → `MessageEvent`


### Token Locks[​](<#token-locks> "Direct link to Token Locks")
Adapters that connect with unique credentials call `acquire_scoped_lock()` in `connect()` and `release_scoped_lock()` in `disconnect()`. This prevents two profiles from using the same bot token simultaneously.
## Delivery Path[​](<#delivery-path> "Direct link to Delivery Path")
Outgoing deliveries (`gateway/delivery.py`) handle:
  * **Direct reply** — send response back to the originating chat
  * **Home channel delivery** — route cron job outputs and background results to a configured home channel
  * **Explicit target delivery** — `send_message` tool specifying `telegram:-1001234567890`
  * **Cross-platform delivery** — deliver to a different platform than the originating message


Cron job deliveries are NOT mirrored into gateway session history — they live in their own cron session only. This is a deliberate design choice to avoid message alternation violations.
## Hooks[​](<#hooks> "Direct link to Hooks")
Gateway hooks are Python modules that respond to lifecycle events:
### Gateway Hook Events[​](<#gateway-hook-events> "Direct link to Gateway Hook Events")
Event| When fired  
---|---  
`gateway:startup`| Gateway process starts  
`session:start`| New conversation session begins  
`session:end`| Session completes or times out  
`session:reset`| User resets session with `/new`  
`agent:start`| Agent begins processing a message  
`agent:step`| Agent completes one tool-calling iteration  
`agent:end`| Agent finishes and returns response  
`command:*`| Any slash command is executed  
Hooks are discovered from `gateway/builtin_hooks/` (always active) and `~/.hermes/hooks/` (user-installed). Each hook is a directory with a `HOOK.yaml` manifest and `handler.py`.
## Memory Provider Integration[​](<#memory-provider-integration> "Direct link to Memory Provider Integration")
When a memory provider plugin (e.g., Honcho) is enabled:
  1. Gateway creates an `AIAgent` per message with the session ID
  2. The `MemoryManager` initializes the provider with the session context
  3. Provider tools (e.g., `honcho_profile`, `viking_search`) are routed through:


[code] 
    AIAgent._invoke_tool()  
      → self._memory_manager.handle_tool_call(name, args)  
        → provider.handle_tool_call(name, args)  
    
[/code]
  4. On session end/reset, `on_session_end()` fires for cleanup and final data flush


### Memory Flush Lifecycle[​](<#memory-flush-lifecycle> "Direct link to Memory Flush Lifecycle")
When a session is reset, resumed, or expires:
  1. Built-in memories are flushed to disk
  2. Memory provider's `on_session_end()` hook fires
  3. A temporary `AIAgent` runs a memory-only conversation turn
  4. Context is then discarded or archived


## Background Maintenance[​](<#background-maintenance> "Direct link to Background Maintenance")
The gateway runs periodic maintenance alongside message handling:
  * **Cron ticking** — checks job schedules and fires due jobs
  * **Session expiry** — cleans up abandoned sessions after timeout
  * **Memory flush** — proactively flushes memory before session expiry
  * **Cache refresh** — refreshes model lists and provider status


## Process Management[​](<#process-management> "Direct link to Process Management")
The gateway runs as a long-lived process, managed via:
  * `hermes gateway start` / `hermes gateway stop` — manual control
  * `systemctl` (Linux) or `launchctl` (macOS) — service management
  * PID file at `~/.hermes/gateway.pid` — profile-scoped process tracking


**Profile-scoped vs global** : `start_gateway()` uses profile-scoped PID files. `hermes gateway stop` stops only the current profile's gateway. `hermes gateway stop --all` uses global `ps aux` scanning to kill all gateway processes (used during updates).
## Related Docs[​](<#related-docs> "Direct link to Related Docs")
  * [Session Storage](</docs/developer-guide/session-storage>)
  * [Cron Internals](</docs/developer-guide/cron-internals>)
  * [ACP Internals](</docs/developer-guide/acp-internals>)
  * [Agent Loop Internals](</docs/developer-guide/agent-loop>)
  * [Messaging Gateway (User Guide)](</docs/user-guide/messaging>)


  * [Key Files](<#key-files>)
  * [Architecture Overview](<#architecture-overview>)
  * [Message Flow](<#message-flow>)
    * [Session Key Format](<#session-key-format>)
    * [Two-Level Message Guard](<#two-level-message-guard>)
  * [Authorization](<#authorization>)
    * [DM Pairing Flow](<#dm-pairing-flow>)
  * [Slash Command Dispatch](<#slash-command-dispatch>)
    * [Running-Agent Guard](<#running-agent-guard>)
  * [Config Sources](<#config-sources>)
  * [Platform Adapters](<#platform-adapters>)
    * [Token Locks](<#token-locks>)
  * [Delivery Path](<#delivery-path>)
  * [Hooks](<#hooks>)
    * [Gateway Hook Events](<#gateway-hook-events>)
  * [Memory Provider Integration](<#memory-provider-integration>)
    * [Memory Flush Lifecycle](<#memory-flush-lifecycle>)
  * [Background Maintenance](<#background-maintenance>)
  * [Process Management](<#process-management>)
  * [Related Docs](<#related-docs>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals -->
