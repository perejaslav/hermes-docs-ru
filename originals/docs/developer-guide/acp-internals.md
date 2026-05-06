On this page
The ACP adapter wraps Hermes' synchronous `AIAgent` in an async JSON-RPC stdio server.
Key implementation files:
  * `acp_adapter/entry.py`
  * `acp_adapter/server.py`
  * `acp_adapter/session.py`
  * `acp_adapter/events.py`
  * `acp_adapter/permissions.py`
  * `acp_adapter/tools.py`
  * `acp_adapter/auth.py`
  * `acp_registry/agent.json`


## Boot flow[​](<#boot-flow> "Direct link to Boot flow")
[code] 
    hermes acp / hermes-acp / python -m acp_adapter  
      -> acp_adapter.entry.main()  
      -> load ~/.hermes/.env  
      -> configure stderr logging  
      -> construct HermesACPAgent  
      -> acp.run_agent(agent, use_unstable_protocol=True)  
    
[/code]
Stdout is reserved for ACP JSON-RPC transport. Human-readable logs go to stderr.
## Major components[​](<#major-components> "Direct link to Major components")
### `HermesACPAgent`[​](<#hermesacpagent> "Direct link to hermesacpagent")
`acp_adapter/server.py` implements the ACP agent protocol.
Responsibilities:
  * initialize / authenticate
  * new/load/resume/fork/list/cancel session methods
  * prompt execution
  * session model switching
  * wiring sync AIAgent callbacks into ACP async notifications


### `SessionManager`[​](<#sessionmanager> "Direct link to sessionmanager")
`acp_adapter/session.py` tracks live ACP sessions.
Each session stores:
  * `session_id`
  * `agent`
  * `cwd`
  * `model`
  * `history`
  * `cancel_event`


The manager is thread-safe and supports:
  * create
  * get
  * remove
  * fork
  * list
  * cleanup
  * cwd updates


### Event bridge[​](<#event-bridge> "Direct link to Event bridge")
`acp_adapter/events.py` converts AIAgent callbacks into ACP `session_update` events.
Bridged callbacks:
  * `tool_progress_callback`
  * `thinking_callback`
  * `step_callback`
  * `message_callback`


Because `AIAgent` runs in a worker thread while ACP I/O lives on the main event loop, the bridge uses:
[code] 
    asyncio.run_coroutine_threadsafe(...)  
    
[/code]
### Permission bridge[​](<#permission-bridge> "Direct link to Permission bridge")
`acp_adapter/permissions.py` adapts dangerous terminal approval prompts into ACP permission requests.
Mapping:
  * `allow_once` -> Hermes `once`
  * `allow_always` -> Hermes `always`
  * reject options -> Hermes `deny`


Timeouts and bridge failures deny by default.
### Tool rendering helpers[​](<#tool-rendering-helpers> "Direct link to Tool rendering helpers")
`acp_adapter/tools.py` maps Hermes tools to ACP tool kinds and builds editor-facing content.
Examples:
  * `patch` / `write_file` -> file diffs
  * `terminal` -> shell command text
  * `read_file` / `search_files` -> text previews
  * large results -> truncated text blocks for UI safety


## Session lifecycle[​](<#session-lifecycle> "Direct link to Session lifecycle")
[code] 
    new_session(cwd)  
      -> create SessionState  
      -> create AIAgent(platform="acp", enabled_toolsets=["hermes-acp"])  
      -> bind task_id/session_id to cwd override  
      
    prompt(..., session_id)  
      -> extract text from ACP content blocks  
      -> reset cancel event  
      -> install callbacks + approval bridge  
      -> run AIAgent in ThreadPoolExecutor  
      -> update session history  
      -> emit final agent message chunk  
    
[/code]
### Cancelation[​](<#cancelation> "Direct link to Cancelation")
`cancel(session_id)`:
  * sets the session cancel event
  * calls `agent.interrupt()` when available
  * causes the prompt response to return `stop_reason="cancelled"`


### Forking[​](<#forking> "Direct link to Forking")
`fork_session()` deep-copies message history into a new live session, preserving conversation state while giving the fork its own session ID and cwd.
## Provider/auth behavior[​](<#providerauth-behavior> "Direct link to Provider/auth behavior")
ACP does not implement its own auth store.
Instead it reuses Hermes' runtime resolver:
  * `acp_adapter/auth.py`
  * `hermes_cli/runtime_provider.py`


So ACP advertises and uses the currently configured Hermes provider/credentials.
## Working directory binding[​](<#working-directory-binding> "Direct link to Working directory binding")
ACP sessions carry an editor cwd.
The session manager binds that cwd to the ACP session ID via task-scoped terminal/file overrides, so file and terminal tools operate relative to the editor workspace.
## Duplicate same-name tool calls[​](<#duplicate-same-name-tool-calls> "Direct link to Duplicate same-name tool calls")
The event bridge tracks tool IDs FIFO per tool name, not just one ID per name. This is important for:
  * parallel same-name calls
  * repeated same-name calls in one step


Without FIFO queues, completion events would attach to the wrong tool invocation.
## Approval callback restoration[​](<#approval-callback-restoration> "Direct link to Approval callback restoration")
ACP temporarily installs an approval callback on the terminal tool during prompt execution, then restores the previous callback afterward. This avoids leaving ACP session-specific approval handlers installed globally forever.
## Current limitations[​](<#current-limitations> "Direct link to Current limitations")
  * ACP sessions are persisted to the shared `~/.hermes/state.db` (SessionDB) and transparently restored across process restarts; they appear in `session_search`
  * non-text prompt blocks are currently ignored for request text extraction
  * editor-specific UX varies by ACP client implementation


## Related files[​](<#related-files> "Direct link to Related files")
  * `tests/acp/` — ACP test suite
  * `toolsets.py` — `hermes-acp` toolset definition
  * `hermes_cli/main.py` — `hermes acp` CLI subcommand
  * `pyproject.toml` — `[acp]` optional dependency + `hermes-acp` script


  * [Boot flow](<#boot-flow>)
  * [Major components](<#major-components>)
    * [`HermesACPAgent`](<#hermesacpagent>)
    * [`SessionManager`](<#sessionmanager>)
    * [Event bridge](<#event-bridge>)
    * [Permission bridge](<#permission-bridge>)
    * [Tool rendering helpers](<#tool-rendering-helpers>)
  * [Session lifecycle](<#session-lifecycle>)
    * [Cancelation](<#cancelation>)
    * [Forking](<#forking>)
  * [Provider/auth behavior](<#providerauth-behavior>)
  * [Working directory binding](<#working-directory-binding>)
  * [Duplicate same-name tool calls](<#duplicate-same-name-tool-calls>)
  * [Approval callback restoration](<#approval-callback-restoration>)
  * [Current limitations](<#current-limitations>)
  * [Related files](<#related-files>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals -->
