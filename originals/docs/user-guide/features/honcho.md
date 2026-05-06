On this page
[Honcho](<https://github.com/plastic-labs/honcho>) is an AI-native memory backend that adds dialectic reasoning and deep user modeling on top of Hermes's built-in memory system. Instead of simple key-value storage, Honcho maintains a running model of who the user is — their preferences, communication style, goals, and patterns — by reasoning about conversations after they happen.
Honcho is a Memory Provider Plugin
Honcho is integrated into the [Memory Providers](</docs/user-guide/features/memory-providers>) system. All features below are available through the unified memory provider interface.
## What Honcho Adds[​](<#what-honcho-adds> "Direct link to What Honcho Adds")
Capability| Built-in Memory| Honcho  
---|---|---  
Cross-session persistence| ✔ File-based MEMORY.md/USER.md| ✔ Server-side with API  
User profile| ✔ Manual agent curation| ✔ Automatic dialectic reasoning  
Session summary| —| ✔ Session-scoped context injection  
Multi-agent isolation| —| ✔ Per-peer profile separation  
Observation modes| —| ✔ Unified or directional observation  
Conclusions (derived insights)| —| ✔ Server-side reasoning about patterns  
Search across history| ✔ FTS5 session search| ✔ Semantic search over conclusions  
**Dialectic reasoning** : After each conversation turn (gated by `dialecticCadence`), Honcho analyzes the exchange and derives insights about the user's preferences, habits, and goals. These accumulate over time, giving the agent a deepening understanding that goes beyond what the user explicitly stated. The dialectic supports multi-pass depth (1–3 passes) with automatic cold/warm prompt selection — cold start queries focus on general user facts while warm queries prioritize session-scoped context.
**Session-scoped context** : Base context now includes the session summary alongside the user representation and peer card. This gives the agent awareness of what has already been discussed in the current session, reducing repetition and enabling continuity.
**Multi-agent profiles** : When multiple Hermes instances talk to the same user (e.g., a coding assistant and a personal assistant), Honcho maintains separate "peer" profiles. Each peer sees only its own observations and conclusions, preventing cross-contamination of context.
## Setup[​](<#setup> "Direct link to Setup")
[code] 
    hermes memory setup    # select "honcho" from the provider list  
    
[/code]
Or configure manually:
[code] 
    # ~/.hermes/config.yaml  
    memory:  
      provider: honcho  
    
[/code]
[code] 
    echo "HONCHO_API_KEY=*** >> ~/.hermes/.env  
    
[/code]
Get an API key at [honcho.dev](<https://honcho.dev>).
## Architecture[​](<#architecture> "Direct link to Architecture")
### Two-Layer Context Injection[​](<#two-layer-context-injection> "Direct link to Two-Layer Context Injection")
Every turn (in `hybrid` or `context` mode), Honcho assembles two layers of context injected into the system prompt:
  1. **Base context** — session summary, user representation, user peer card, AI self-representation, and AI identity card. Refreshed on `contextCadence`. This is the "who is this user" layer.
  2. **Dialectic supplement** — LLM-synthesized reasoning about the user's current state and needs. Refreshed on `dialecticCadence`. This is the "what matters right now" layer.


Both layers are concatenated and truncated to the `contextTokens` budget (if set).
### Cold/Warm Prompt Selection[​](<#coldwarm-prompt-selection> "Direct link to Cold/Warm Prompt Selection")
The dialectic automatically selects between two prompt strategies:
  * **Cold start** (no base context yet): General query — "Who is this person? What are their preferences, goals, and working style?"
  * **Warm session** (base context exists): Session-scoped query — "Given what's been discussed in this session so far, what context about this user is most relevant?"


This happens automatically based on whether base context has been populated.
### Three Orthogonal Config Knobs[​](<#three-orthogonal-config-knobs> "Direct link to Three Orthogonal Config Knobs")
Cost and depth are controlled by three independent knobs:
Knob| Controls| Default  
---|---|---  
`contextCadence`| Turns between `context()` API calls (base layer refresh)| `1`  
`dialecticCadence`| Turns between `peer.chat()` LLM calls (dialectic layer refresh)| `2` (recommended 1–5)  
`dialecticDepth`| Number of `.chat()` passes per dialectic invocation (1–3)| `1`  
These are orthogonal — you can have frequent context refreshes with infrequent dialectic, or deep multi-pass dialectic at low frequency. Example: `contextCadence: 1, dialecticCadence: 5, dialecticDepth: 2` refreshes base context every turn, runs dialectic every 5 turns, and each dialectic run makes 2 passes.
### Dialectic Depth (Multi-Pass)[​](<#dialectic-depth-multi-pass> "Direct link to Dialectic Depth \(Multi-Pass\)")
When `dialecticDepth` > 1, each dialectic invocation runs multiple `.chat()` passes:
  * **Pass 0** : Cold or warm prompt (see above)
  * **Pass 1** : Self-audit — identifies gaps in the initial assessment and synthesizes evidence from recent sessions
  * **Pass 2** : Reconciliation — checks for contradictions between prior passes and produces a final synthesis


Each pass uses a proportional reasoning level (lighter early passes, base level for the main pass). Override per-pass levels with `dialecticDepthLevels` — e.g., `["minimal", "medium", "high"]` for a depth-3 run.
Passes bail out early if the prior pass returned strong signal (long, structured output), so depth 3 doesn't always mean 3 LLM calls.
### Session-Start Prewarm[​](<#session-start-prewarm> "Direct link to Session-Start Prewarm")
On session init, Honcho fires a dialectic call in the background at the full configured `dialecticDepth` and hands the result directly to turn 1's context assembly. A single-pass prewarm on a cold peer often returns thin output — multi-pass depth runs the audit/reconcile cycle before the user ever speaks. If prewarm hasn't landed by turn 1, turn 1 falls back to a synchronous call with a bounded timeout.
### Query-Adaptive Reasoning Level[​](<#query-adaptive-reasoning-level> "Direct link to Query-Adaptive Reasoning Level")
The auto-injected dialectic scales `dialecticReasoningLevel` by query length: +1 level at ≥120 chars, +2 at ≥400, clamped at `reasoningLevelCap` (default `"high"`). Disable with `reasoningHeuristic: false` to pin every auto call to `dialecticReasoningLevel`. Available levels: `minimal`, `low`, `medium`, `high`, `max`.
## Configuration Options[​](<#configuration-options> "Direct link to Configuration Options")
Honcho is configured in `~/.honcho/config.json` (global) or `$HERMES_HOME/honcho.json` (profile-local). The setup wizard handles this for you.
### Full Config Reference[​](<#full-config-reference> "Direct link to Full Config Reference")
Key| Default| Description  
---|---|---  
`contextTokens`| `null` (uncapped)| Token budget for auto-injected context per turn. Set to an integer (e.g. 1200) to cap. Truncates at word boundaries  
`contextCadence`| `1`| Minimum turns between `context()` API calls (base layer refresh)  
`dialecticCadence`| `2`| Minimum turns between `peer.chat()` LLM calls (dialectic layer). Recommended 1–5. In `tools` mode, irrelevant — model calls explicitly  
`dialecticDepth`| `1`| Number of `.chat()` passes per dialectic invocation. Clamped to 1–3  
`dialecticDepthLevels`| `null`| Optional array of reasoning levels per pass, e.g. `["minimal", "low", "medium"]`. Overrides proportional defaults  
`dialecticReasoningLevel`| `'low'`| Base reasoning level: `minimal`, `low`, `medium`, `high`, `max`  
`dialecticDynamic`| `true`| When `true`, model can override reasoning level per-call via tool param  
`dialecticMaxChars`| `600`| Max chars of dialectic result injected into system prompt  
`recallMode`| `'hybrid'`| `hybrid` (auto-inject + tools), `context` (inject only), `tools` (tools only)  
`writeFrequency`| `'async'`| When to flush messages: `async` (background thread), `turn` (sync), `session` (batch on end), or integer N  
`saveMessages`| `true`| Whether to persist messages to Honcho API  
`observationMode`| `'directional'`| `directional` (all on) or `unified` (shared pool). Override with `observation` object for granular control  
`messageMaxChars`| `25000`| Max chars per message sent via `add_messages()`. Chunked if exceeded  
`dialecticMaxInputChars`| `10000`| Max chars for dialectic query input to `peer.chat()`  
`sessionStrategy`| `'per-directory'`| `per-directory`, `per-repo`, `per-session`, or `global`  
**Session strategy** controls how Honcho sessions map to your work:
  * `per-session` — each `hermes` run gets a fresh session. Clean starts, memory via tools. Recommended for new users.
  * `per-directory` — one Honcho session per working directory. Context accumulates across runs.
  * `per-repo` — one session per git repository.
  * `global` — single session across all directories.


**Recall mode** controls how memory flows into conversations:
  * `hybrid` — context auto-injected into system prompt AND tools available (model decides when to query).
  * `context` — auto-injection only, tools hidden.
  * `tools` — tools only, no auto-injection. Agent must explicitly call `honcho_reasoning`, `honcho_search`, etc.


**Settings per recall mode:**
Setting| `hybrid`| `context`| `tools`  
---|---|---|---  
`writeFrequency`| flushes messages| flushes messages| flushes messages  
`contextCadence`| gates base context refresh| gates base context refresh| irrelevant — no injection  
`dialecticCadence`| gates auto LLM calls| gates auto LLM calls| irrelevant — model calls explicitly  
`dialecticDepth`| multi-pass per invocation| multi-pass per invocation| irrelevant — model calls explicitly  
`contextTokens`| caps injection| caps injection| irrelevant — no injection  
`dialecticDynamic`| gates model override| N/A (no tools)| gates model override  
In `tools` mode, the model is fully in control — it calls `honcho_reasoning` when it wants, at whatever `reasoning_level` it picks. Cadence and budget settings only apply to modes with auto-injection (`hybrid` and `context`).
## Observation (Directional vs. Unified)[​](<#observation-directional-vs-unified> "Direct link to Observation \(Directional vs. Unified\)")
Honcho models a conversation as peers exchanging messages. Each peer has two observation toggles that map 1:1 to Honcho's `SessionPeerConfig`:
Toggle| Effect  
---|---  
`observeMe`| Honcho builds a representation of this peer from its own messages  
`observeOthers`| This peer observes the other peer's messages (feeds cross-peer reasoning)  
Two peers × two toggles = four flags. `observationMode` is a shorthand preset:
Preset| User flags| AI flags| Semantics  
---|---|---|---  
`"directional"` (default)| me: on, others: on| me: on, others: on| Full mutual observation. Enables cross-peer dialectic — "what does the AI know about the user, based on what the user said and the AI replied."  
`"unified"`| me: on, others: off| me: off, others: on| Shared-pool semantics — the AI observes the user's messages only, the user peer only self-models. Single-observer pool.  
Override the preset with an explicit `observation` block for per-peer control:
[code] 
    "observation": {  
      "user": { "observeMe": true,  "observeOthers": true },  
      "ai":   { "observeMe": true,  "observeOthers": false }  
    }  
    
[/code]
Common patterns:
Intent| Config  
---|---  
Full observation (most users)| `"observationMode": "directional"`  
AI shouldn't re-model the user from its own replies| `"ai": {"observeMe": true, "observeOthers": false}`  
Strong persona the AI peer shouldn't update from self-observation| `"ai": {"observeMe": false, "observeOthers": true}`  
Server-side toggles set via the [Honcho dashboard](<https://app.honcho.dev>) win over local defaults — Hermes syncs them back at session init.
## Tools[​](<#tools> "Direct link to Tools")
When Honcho is active as the memory provider, five tools become available:
Tool| Purpose  
---|---  
`honcho_profile`| Read or update peer card — pass `card` (list of facts) to update, omit to read  
`honcho_search`| Semantic search over context — raw excerpts, no LLM synthesis  
`honcho_context`| Full session context — summary, representation, card, recent messages  
`honcho_reasoning`| Synthesized answer from Honcho's LLM — pass `reasoning_level` (minimal/low/medium/high/max) to control depth  
`honcho_conclude`| Create or delete conclusions — pass `conclusion` to create, `delete_id` to remove (PII only)  
## CLI Commands[​](<#cli-commands> "Direct link to CLI Commands")
[code] 
    hermes honcho status          # Connection status, config, and key settings  
    hermes honcho setup           # Interactive setup wizard  
    hermes honcho strategy        # Show or set session strategy  
    hermes honcho peer            # Update peer names for multi-agent setups  
    hermes honcho mode            # Show or set recall mode  
    hermes honcho tokens          # Show or set context token budget  
    hermes honcho identity        # Show Honcho peer identity  
    hermes honcho sync            # Sync host blocks for all profiles  
    hermes honcho enable          # Enable Honcho  
    hermes honcho disable         # Disable Honcho  
    
[/code]
## Migrating from `hermes honcho`[​](<#migrating-from-hermes-honcho> "Direct link to migrating-from-hermes-honcho")
If you previously used the standalone `hermes honcho setup`:
  1. Your existing configuration (`honcho.json` or `~/.honcho/config.json`) is preserved
  2. Your server-side data (memories, conclusions, user profiles) is intact
  3. Set `memory.provider: honcho` in config.yaml to reactivate


No re-login or re-setup needed. Run `hermes memory setup` and select "honcho" — the wizard detects your existing config.
## Full Documentation[​](<#full-documentation> "Direct link to Full Documentation")
See [Memory Providers — Honcho](</docs/user-guide/features/memory-providers#honcho>) for the complete reference.
  * [What Honcho Adds](<#what-honcho-adds>)
  * [Setup](<#setup>)
  * [Architecture](<#architecture>)
    * [Two-Layer Context Injection](<#two-layer-context-injection>)
    * [Cold/Warm Prompt Selection](<#coldwarm-prompt-selection>)
    * [Three Orthogonal Config Knobs](<#three-orthogonal-config-knobs>)
    * [Dialectic Depth (Multi-Pass)](<#dialectic-depth-multi-pass>)
    * [Session-Start Prewarm](<#session-start-prewarm>)
    * [Query-Adaptive Reasoning Level](<#query-adaptive-reasoning-level>)
  * [Configuration Options](<#configuration-options>)
    * [Full Config Reference](<#full-config-reference>)
  * [Observation (Directional vs. Unified)](<#observation-directional-vs-unified>)
  * [Tools](<#tools>)
  * [CLI Commands](<#cli-commands>)
  * [Migrating from `hermes honcho`](<#migrating-from-hermes-honcho>)
  * [Full Documentation](<#full-documentation>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho -->
