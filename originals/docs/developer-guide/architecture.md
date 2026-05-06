On this page
This page is the top-level map of Hermes Agent internals. Use it to orient yourself in the codebase, then dive into subsystem-specific docs for implementation details.
## System Overview[​](<#system-overview> "Direct link to System Overview")
[code] 
    ┌─────────────────────────────────────────────────────────────────────┐  
    │                        Entry Points                                  │  
    │                                                                      │  
    │  CLI (cli.py)    Gateway (gateway/run.py)    ACP (acp_adapter/)     │  
    │  Batch Runner    API Server                  Python Library          │  
    └──────────┬──────────────┬───────────────────────┬───────────────────┘  
               │              │                       │  
               ▼              ▼                       ▼  
    ┌─────────────────────────────────────────────────────────────────────┐  
    │                     AIAgent (run_agent.py)                          │  
    │                                                                     │  
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  
    │  │ Prompt       │  │ Provider     │  │ Tool         │               │  
    │  │ Builder      │  │ Resolution   │  │ Dispatch     │               │  
    │  │ (prompt_     │  │ (runtime_    │  │ (model_      │               │  
    │  │  builder.py) │  │  provider.py)│  │  tools.py)   │               │  
    │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │  
    │         │                 │                 │                       │  
    │  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐               │  
    │  │ Compression  │  │ 3 API Modes  │  │ Tool Registry│               │  
    │  │ & Caching    │  │ chat_compl.  │  │ (registry.py)│               │  
    │  │              │  │ codex_resp.  │  │ 61 tools     │               │  
    │  │              │  │ anthropic    │  │ 52 toolsets  │               │  
    │  └──────────────┘  └──────────────┘  └──────────────┘               │  
    └─────────┴─────────────────┴─────────────────┴───────────────────────┘  
               │                                    │  
               ▼                                    ▼  
    ┌───────────────────┐              ┌──────────────────────┐  
    │ Session Storage   │              │ Tool Backends         │  
    │ (SQLite + FTS5)   │              │ Terminal (7 backends) │  
    │ hermes_state.py   │              │ Browser (5 backends)  │  
    │ gateway/session.py│              │ Web (4 backends)      │  
    └───────────────────┘              │ MCP (dynamic)         │  
                                       │ File, Vision, etc.    │  
                                       └──────────────────────┘  
    
[/code]
## Directory Structure[​](<#directory-structure> "Direct link to Directory Structure")
[code] 
    hermes-agent/  
    ├── run_agent.py              # AIAgent — core conversation loop (~13,700 lines)  
    ├── cli.py                    # HermesCLI — interactive terminal UI (~11,500 lines)  
    ├── model_tools.py            # Tool discovery, schema collection, dispatch  
    ├── toolsets.py               # Tool groupings and platform presets  
    ├── hermes_state.py           # SQLite session/state database with FTS5  
    ├── hermes_constants.py       # HERMES_HOME, profile-aware paths  
    ├── batch_runner.py           # Batch trajectory generation  
    │  
    ├── agent/                    # Agent internals  
    │   ├── prompt_builder.py     # System prompt assembly  
    │   ├── context_engine.py     # ContextEngine ABC (pluggable)  
    │   ├── context_compressor.py # Default engine — lossy summarization  
    │   ├── prompt_caching.py     # Anthropic prompt caching  
    │   ├── auxiliary_client.py   # Auxiliary LLM for side tasks (vision, summarization)  
    │   ├── model_metadata.py     # Model context lengths, token estimation  
    │   ├── models_dev.py         # models.dev registry integration  
    │   ├── anthropic_adapter.py  # Anthropic Messages API format conversion  
    │   ├── display.py            # KawaiiSpinner, tool preview formatting  
    │   ├── skill_commands.py     # Skill slash commands  
    │   ├── memory_manager.py    # Memory manager orchestration  
    │   ├── memory_provider.py   # Memory provider ABC  
    │   └── trajectory.py         # Trajectory saving helpers  
    │  
    ├── hermes_cli/               # CLI subcommands and setup  
    │   ├── main.py               # Entry point — all `hermes` subcommands (~10,400 lines)  
    │   ├── config.py             # DEFAULT_CONFIG, OPTIONAL_ENV_VARS, migration  
    │   ├── commands.py           # COMMAND_REGISTRY — central slash command definitions  
    │   ├── auth.py               # PROVIDER_REGISTRY, credential resolution  
    │   ├── runtime_provider.py   # Provider → api_mode + credentials  
    │   ├── models.py             # Model catalog, provider model lists  
    │   ├── model_switch.py       # /model command logic (CLI + gateway shared)  
    │   ├── setup.py              # Interactive setup wizard (~3,500 lines)  
    │   ├── skin_engine.py        # CLI theming engine  
    │   ├── skills_config.py      # hermes skills — enable/disable per platform  
    │   ├── skills_hub.py         # /skills slash command  
    │   ├── tools_config.py       # hermes tools — enable/disable per platform  
    │   ├── plugins.py            # PluginManager — discovery, loading, hooks  
    │   ├── callbacks.py          # Terminal callbacks (clarify, sudo, approval)  
    │   └── gateway.py            # hermes gateway start/stop  
    │  
    ├── tools/                    # Tool implementations (one file per tool)  
    │   ├── registry.py           # Central tool registry  
    │   ├── approval.py           # Dangerous command detection  
    │   ├── terminal_tool.py      # Terminal orchestration  
    │   ├── process_registry.py   # Background process management  
    │   ├── file_tools.py         # read_file, write_file, patch, search_files  
    │   ├── web_tools.py          # web_search, web_extract  
    │   ├── browser_tool.py       # 10 browser automation tools  
    │   ├── code_execution_tool.py # execute_code sandbox  
    │   ├── delegate_tool.py      # Subagent delegation  
    │   ├── mcp_tool.py           # MCP client (~3,100 lines)  
    │   ├── credential_files.py   # File-based credential passthrough  
    │   ├── env_passthrough.py    # Env var passthrough for sandboxes  
    │   ├── ansi_strip.py         # ANSI escape stripping  
    │   └── environments/         # Terminal backends (local, docker, ssh, modal, daytona, singularity)  
    │  
    ├── gateway/                  # Messaging platform gateway  
    │   ├── run.py                # GatewayRunner — message dispatch (~12,200 lines)  
    │   ├── session.py            # SessionStore — conversation persistence  
    │   ├── delivery.py           # Outbound message delivery  
    │   ├── pairing.py            # DM pairing authorization  
    │   ├── hooks.py              # Hook discovery and lifecycle events  
    │   ├── mirror.py             # Cross-session message mirroring  
    │   ├── status.py             # Token locks, profile-scoped process tracking  
    │   ├── builtin_hooks/        # Extension point for always-registered hooks (none shipped)  
    │   └── platforms/            # 20 adapters: telegram, discord, slack, whatsapp,  
    │                             #   signal, matrix, mattermost, email, sms,  
    │                             #   dingtalk, feishu, wecom, wecom_callback, weixin,  
    │                             #   bluebubbles, qqbot, homeassistant, webhook, api_server,  
    │                             #   yuanbao  
    │  
    ├── acp_adapter/              # ACP server (VS Code / Zed / JetBrains)  
    ├── cron/                     # Scheduler (jobs.py, scheduler.py)  
    ├── plugins/memory/           # Memory provider plugins  
    ├── plugins/context_engine/   # Context engine plugins  
    ├── environments/             # RL training environments (Atropos)  
    ├── skills/                   # Bundled skills (always available)  
    ├── optional-skills/          # Official optional skills (install explicitly)  
    ├── website/                  # Docusaurus documentation site  
    └── tests/                    # Pytest suite (~3,000+ tests)  
    
[/code]
## Data Flow[​](<#data-flow> "Direct link to Data Flow")
### CLI Session[​](<#cli-session> "Direct link to CLI Session")
[code] 
    User input → HermesCLI.process_input()  
      → AIAgent.run_conversation()  
        → prompt_builder.build_system_prompt()  
        → runtime_provider.resolve_runtime_provider()  
        → API call (chat_completions / codex_responses / anthropic_messages)  
        → tool_calls? → model_tools.handle_function_call() → loop  
        → final response → display → save to SessionDB  
    
[/code]
### Gateway Message[​](<#gateway-message> "Direct link to Gateway Message")
[code] 
    Platform event → Adapter.on_message() → MessageEvent  
      → GatewayRunner._handle_message()  
        → authorize user  
        → resolve session key  
        → create AIAgent with session history  
        → AIAgent.run_conversation()  
        → deliver response back through adapter  
    
[/code]
### Cron Job[​](<#cron-job> "Direct link to Cron Job")
[code] 
    Scheduler tick → load due jobs from jobs.json  
      → create fresh AIAgent (no history)  
      → inject attached skills as context  
      → run job prompt  
      → deliver response to target platform  
      → update job state and next_run  
    
[/code]
## Recommended Reading Order[​](<#recommended-reading-order> "Direct link to Recommended Reading Order")
If you are new to the codebase:
  1. **This page** — orient yourself
  2. **[Agent Loop Internals](</docs/developer-guide/agent-loop>)** — how AIAgent works
  3. **[Prompt Assembly](</docs/developer-guide/prompt-assembly>)** — system prompt construction
  4. **[Provider Runtime Resolution](</docs/developer-guide/provider-runtime>)** — how providers are selected
  5. **[Adding Providers](</docs/developer-guide/adding-providers>)** — practical guide to adding a new provider
  6. **[Tools Runtime](</docs/developer-guide/tools-runtime>)** — tool registry, dispatch, environments
  7. **[Session Storage](</docs/developer-guide/session-storage>)** — SQLite schema, FTS5, session lineage
  8. **[Gateway Internals](</docs/developer-guide/gateway-internals>)** — messaging platform gateway
  9. **[Context Compression& Prompt Caching](</docs/developer-guide/context-compression-and-caching>)** — compression and caching
  10. **[ACP Internals](</docs/developer-guide/acp-internals>)** — IDE integration
  11. **[Environments, Benchmarks& Data Generation](</docs/developer-guide/environments>)** — RL training


## Major Subsystems[​](<#major-subsystems> "Direct link to Major Subsystems")
### Agent Loop[​](<#agent-loop> "Direct link to Agent Loop")
The synchronous orchestration engine (`AIAgent` in `run_agent.py`). Handles provider selection, prompt construction, tool execution, retries, fallback, callbacks, compression, and persistence. Supports three API modes for different provider backends.
→ [Agent Loop Internals](</docs/developer-guide/agent-loop>)
### Prompt System[​](<#prompt-system> "Direct link to Prompt System")
Prompt construction and maintenance across the conversation lifecycle:
  * **`prompt_builder.py`** — Assembles the system prompt from: personality (SOUL.md), memory (MEMORY.md, USER.md), skills, context files (AGENTS.md, .hermes.md), tool-use guidance, and model-specific instructions
  * **`prompt_caching.py`** — Applies Anthropic cache breakpoints for prefix caching
  * **`context_compressor.py`** — Summarizes middle conversation turns when context exceeds thresholds


→ [Prompt Assembly](</docs/developer-guide/prompt-assembly>), [Context Compression & Prompt Caching](</docs/developer-guide/context-compression-and-caching>)
### Provider Resolution[​](<#provider-resolution> "Direct link to Provider Resolution")
A shared runtime resolver used by CLI, gateway, cron, ACP, and auxiliary calls. Maps `(provider, model)` tuples to `(api_mode, api_key, base_url)`. Handles 18+ providers, OAuth flows, credential pools, and alias resolution.
→ [Provider Runtime Resolution](</docs/developer-guide/provider-runtime>)
### Tool System[​](<#tool-system> "Direct link to Tool System")
Central tool registry (`tools/registry.py`) with 61 registered tools across 52 toolsets. Each tool file self-registers at import time. The registry handles schema collection, dispatch, availability checking, and error wrapping. Terminal tools support 7 backends (local, Docker, SSH, Daytona, Modal, Singularity, Vercel Sandbox).
→ [Tools Runtime](</docs/developer-guide/tools-runtime>)
### Session Persistence[​](<#session-persistence> "Direct link to Session Persistence")
SQLite-based session storage with FTS5 full-text search. Sessions have lineage tracking (parent/child across compressions), per-platform isolation, and atomic writes with contention handling.
→ [Session Storage](</docs/developer-guide/session-storage>)
### Messaging Gateway[​](<#messaging-gateway> "Direct link to Messaging Gateway")
Long-running process with 20 platform adapters, unified session routing, user authorization (allowlists + DM pairing), slash command dispatch, hook system, cron ticking, and background maintenance.
→ [Gateway Internals](</docs/developer-guide/gateway-internals>)
### Plugin System[​](<#plugin-system> "Direct link to Plugin System")
Three discovery sources: `~/.hermes/plugins/` (user), `.hermes/plugins/` (project), and pip entry points. Plugins register tools, hooks, and CLI commands through a context API. Two specialized plugin types exist: memory providers (`plugins/memory/`) and context engines (`plugins/context_engine/`). Both are single-select — only one of each can be active at a time, configured via `hermes plugins` or `config.yaml`.
→ [Plugin Guide](</docs/guides/build-a-hermes-plugin>), [Memory Provider Plugin](</docs/developer-guide/memory-provider-plugin>)
### Cron[​](<#cron> "Direct link to Cron")
First-class agent tasks (not shell tasks). Jobs store in JSON, support multiple schedule formats, can attach skills and scripts, and deliver to any platform.
→ [Cron Internals](</docs/developer-guide/cron-internals>)
### ACP Integration[​](<#acp-integration> "Direct link to ACP Integration")
Exposes Hermes as an editor-native agent over stdio/JSON-RPC for VS Code, Zed, and JetBrains.
→ [ACP Internals](</docs/developer-guide/acp-internals>)
### RL / Environments / Trajectories[​](<#rl--environments--trajectories> "Direct link to RL / Environments / Trajectories")
Full environment framework for evaluation and RL training. Integrates with Atropos, supports multiple tool-call parsers, and generates ShareGPT-format trajectories.
→ [Environments, Benchmarks & Data Generation](</docs/developer-guide/environments>), [Trajectories & Training Format](</docs/developer-guide/trajectory-format>)
## Design Principles[​](<#design-principles> "Direct link to Design Principles")
Principle| What it means in practice  
---|---  
**Prompt stability**|  System prompt doesn't change mid-conversation. No cache-breaking mutations except explicit user actions (`/model`).  
**Observable execution**|  Every tool call is visible to the user via callbacks. Progress updates in CLI (spinner) and gateway (chat messages).  
**Interruptible**|  API calls and tool execution can be cancelled mid-flight by user input or signals.  
**Platform-agnostic core**|  One AIAgent class serves CLI, gateway, ACP, batch, and API server. Platform differences live in the entry point, not the agent.  
**Loose coupling**|  Optional subsystems (MCP, plugins, memory providers, RL environments) use registry patterns and check_fn gating, not hard dependencies.  
**Profile isolation**|  Each profile (`hermes -p <name>`) gets its own HERMES_HOME, config, memory, sessions, and gateway PID. Multiple profiles run concurrently.  
## File Dependency Chain[​](<#file-dependency-chain> "Direct link to File Dependency Chain")
[code] 
    tools/registry.py  (no deps — imported by all tool files)  
           ↑  
    tools/*.py  (each calls registry.register() at import time)  
           ↑  
    model_tools.py  (imports tools/registry + triggers tool discovery)  
           ↑  
    run_agent.py, cli.py, batch_runner.py, environments/  
    
[/code]
This chain means tool registration happens at import time, before any agent instance is created. Any `tools/*.py` file with a top-level `registry.register()` call is auto-discovered — no manual import list needed.
  * [System Overview](<#system-overview>)
  * [Directory Structure](<#directory-structure>)
  * [Data Flow](<#data-flow>)
    * [CLI Session](<#cli-session>)
    * [Gateway Message](<#gateway-message>)
    * [Cron Job](<#cron-job>)
  * [Recommended Reading Order](<#recommended-reading-order>)
  * [Major Subsystems](<#major-subsystems>)
    * [Agent Loop](<#agent-loop>)
    * [Prompt System](<#prompt-system>)
    * [Provider Resolution](<#provider-resolution>)
    * [Tool System](<#tool-system>)
    * [Session Persistence](<#session-persistence>)
    * [Messaging Gateway](<#messaging-gateway>)
    * [Plugin System](<#plugin-system>)
    * [Cron](<#cron>)
    * [ACP Integration](<#acp-integration>)
    * [RL / Environments / Trajectories](<#rl--environments--trajectories>)
  * [Design Principles](<#design-principles>)
  * [File Dependency Chain](<#file-dependency-chain>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture -->
