On this page
MCP client: connect servers, register tools (stdio/HTTP).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/mcp/native-mcp`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Tags| `MCP`, `Tools`, `Integrations`  
Related skills| [`mcporter`](</docs/user-guide/skills/optional/mcp/mcp-mcporter>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Native MCP Client
Hermes Agent has a built-in MCP client that connects to MCP servers at startup, discovers their tools, and makes them available as first-class tools the agent can call directly. No bridge CLI needed -- tools from MCP servers appear alongside built-in tools like `terminal`, `read_file`, etc.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
Use this whenever you want to:
  * Connect to MCP servers and use their tools from within Hermes Agent
  * Add external capabilities (filesystem access, GitHub, databases, APIs) via MCP
  * Run local stdio-based MCP servers (npx, uvx, or any command)
  * Connect to remote HTTP/StreamableHTTP MCP servers
  * Have MCP tools auto-discovered and available in every conversation


For ad-hoc, one-off MCP tool calls from the terminal without configuring anything, see the `mcporter` skill instead.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **mcp Python package** \-- optional dependency; install with `pip install mcp`. If not installed, MCP support is silently disabled.
  * **Node.js** \-- required for `npx`-based MCP servers (most community servers)
  * **uv** \-- required for `uvx`-based MCP servers (Python-based servers)


Install the MCP SDK:
[code] 
    pip install mcp  
    # or, if using uv:  
    uv pip install mcp  
    
[/code]
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
Add MCP servers to `~/.hermes/config.yaml` under the `mcp_servers` key:
[code] 
    mcp_servers:  
      time:  
        command: "uvx"  
        args: ["mcp-server-time"]  
    
[/code]
Restart Hermes Agent. On startup it will:
  1. Connect to the server
  2. Discover available tools
  3. Register them with the prefix `mcp_time_*`
  4. Inject them into all platform toolsets


You can then use the tools naturally -- just ask the agent to get the current time.
## Configuration Reference[​](<#configuration-reference> "Direct link to Configuration Reference")
Each entry under `mcp_servers` is a server name mapped to its config. There are two transport types: **stdio** (command-based) and **HTTP** (url-based).
### Stdio Transport (command + args)[​](<#stdio-transport-command--args> "Direct link to Stdio Transport \(command + args\)")
[code] 
    mcp_servers:  
      server_name:  
        command: "npx"             # (required) executable to run  
        args: ["-y", "pkg-name"]   # (optional) command arguments, default: []  
        env:                       # (optional) environment variables for the subprocess  
          SOME_API_KEY: "value"  
        timeout: 120               # (optional) per-tool-call timeout in seconds, default: 120  
        connect_timeout: 60        # (optional) initial connection timeout in seconds, default: 60  
    
[/code]
### HTTP Transport (url)[​](<#http-transport-url> "Direct link to HTTP Transport \(url\)")
[code] 
    mcp_servers:  
      server_name:  
        url: "https://my-server.example.com/mcp"   # (required) server URL  
        headers:                                     # (optional) HTTP headers  
          Authorization: "Bearer sk-..."  
        timeout: 180               # (optional) per-tool-call timeout in seconds, default: 120  
        connect_timeout: 60        # (optional) initial connection timeout in seconds, default: 60  
    
[/code]
### All Config Options[​](<#all-config-options> "Direct link to All Config Options")
Option| Type| Default| Description  
---|---|---|---  
`command`| string| \--| Executable to run (stdio transport, required)  
`args`| list| `[]`| Arguments passed to the command  
`env`| dict| `{}`| Extra environment variables for the subprocess  
`url`| string| \--| Server URL (HTTP transport, required)  
`headers`| dict| `{}`| HTTP headers sent with every request  
`timeout`| int| `120`| Per-tool-call timeout in seconds  
`connect_timeout`| int| `60`| Timeout for initial connection and discovery  
Note: A server config must have either `command` (stdio) or `url` (HTTP), not both.
## How It Works[​](<#how-it-works> "Direct link to How It Works")
### Startup Discovery[​](<#startup-discovery> "Direct link to Startup Discovery")
When Hermes Agent starts, `discover_mcp_tools()` is called during tool initialization:
  1. Reads `mcp_servers` from `~/.hermes/config.yaml`
  2. For each server, spawns a connection in a dedicated background event loop
  3. Initializes the MCP session and calls `list_tools()` to discover available tools
  4. Registers each tool in the Hermes tool registry


### Tool Naming Convention[​](<#tool-naming-convention> "Direct link to Tool Naming Convention")
MCP tools are registered with the naming pattern:
[code] 
    mcp_{server_name}_{tool_name}  
    
[/code]
Hyphens and dots in names are replaced with underscores for LLM API compatibility.
Examples:
  * Server `filesystem`, tool `read_file` → `mcp_filesystem_read_file`
  * Server `github`, tool `list-issues` → `mcp_github_list_issues`
  * Server `my-api`, tool `fetch.data` → `mcp_my_api_fetch_data`


### Auto-Injection[​](<#auto-injection> "Direct link to Auto-Injection")
After discovery, MCP tools are automatically injected into all `hermes-*` platform toolsets (CLI, Discord, Telegram, etc.). This means MCP tools are available in every conversation without any additional configuration.
### Connection Lifecycle[​](<#connection-lifecycle> "Direct link to Connection Lifecycle")
  * Each server runs as a long-lived asyncio Task in a background daemon thread
  * Connections persist for the lifetime of the agent process
  * If a connection drops, automatic reconnection with exponential backoff kicks in (up to 5 retries, max 60s backoff)
  * On agent shutdown, all connections are gracefully closed


### Idempotency[​](<#idempotency> "Direct link to Idempotency")
`discover_mcp_tools()` is idempotent -- calling it multiple times only connects to servers that aren't already connected. Failed servers are retried on subsequent calls.
## Transport Types[​](<#transport-types> "Direct link to Transport Types")
### Stdio Transport[​](<#stdio-transport> "Direct link to Stdio Transport")
The most common transport. Hermes launches the MCP server as a subprocess and communicates over stdin/stdout.
[code] 
    mcp_servers:  
      filesystem:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]  
    
[/code]
The subprocess inherits a **filtered** environment (see Security section below) plus any variables you specify in `env`.
### HTTP / StreamableHTTP Transport[​](<#http--streamablehttp-transport> "Direct link to HTTP / StreamableHTTP Transport")
For remote or shared MCP servers. Requires the `mcp` package to include HTTP client support (`mcp.client.streamable_http`).
[code] 
    mcp_servers:  
      remote_api:  
        url: "https://mcp.example.com/mcp"  
        headers:  
          Authorization: "Bearer sk-..."  
    
[/code]
If HTTP support is not available in your installed `mcp` version, the server will fail with an ImportError and other servers will continue normally.
## Security[​](<#security> "Direct link to Security")
### Environment Variable Filtering[​](<#environment-variable-filtering> "Direct link to Environment Variable Filtering")
For stdio servers, Hermes does NOT pass your full shell environment to MCP subprocesses. Only safe baseline variables are inherited:
  * `PATH`, `HOME`, `USER`, `LANG`, `LC_ALL`, `TERM`, `SHELL`, `TMPDIR`
  * Any `XDG_*` variables


All other environment variables (API keys, tokens, secrets) are excluded unless you explicitly add them via the `env` config key. This prevents accidental credential leakage to untrusted MCP servers.
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          # Only this token is passed to the subprocess  
          GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."  
    
[/code]
### Credential Stripping in Error Messages[​](<#credential-stripping-in-error-messages> "Direct link to Credential Stripping in Error Messages")
If an MCP tool call fails, any credential-like patterns in the error message are automatically redacted before being shown to the LLM. This covers:
  * GitHub PATs (`ghp_...`)
  * OpenAI-style keys (`sk-...`)
  * Bearer tokens
  * Generic `token=`, `key=`, `API_KEY=`, `password=`, `secret=` patterns


## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### "MCP SDK not available -- skipping MCP tool discovery"[​](<#mcp-sdk-not-available----skipping-mcp-tool-discovery> "Direct link to "MCP SDK not available -- skipping MCP tool discovery"")
The `mcp` Python package is not installed. Install it:
[code] 
    pip install mcp  
    
[/code]
### "No MCP servers configured"[​](<#no-mcp-servers-configured> "Direct link to "No MCP servers configured"")
No `mcp_servers` key in `~/.hermes/config.yaml`, or it's empty. Add at least one server.
### "Failed to connect to MCP server 'X'"[​](<#failed-to-connect-to-mcp-server-x> "Direct link to "Failed to connect to MCP server 'X'"")
Common causes:
  * **Command not found** : The `command` binary isn't on PATH. Ensure `npx`, `uvx`, or the relevant command is installed.
  * **Package not found** : For npx servers, the npm package may not exist or may need `-y` in args to auto-install.
  * **Timeout** : The server took too long to start. Increase `connect_timeout`.
  * **Port conflict** : For HTTP servers, the URL may be unreachable.


### "MCP server 'X' requires HTTP transport but mcp.client.streamable_http is not available"[​](<#mcp-server-x-requires-http-transport-but-mcpclientstreamable_http-is-not-available> "Direct link to "MCP server 'X' requires HTTP transport but mcp.client.streamable_http is not available"")
Your `mcp` package version doesn't include HTTP client support. Upgrade:
[code] 
    pip install --upgrade mcp  
    
[/code]
### Tools not appearing[​](<#tools-not-appearing> "Direct link to Tools not appearing")
  * Check that the server is listed under `mcp_servers` (not `mcp` or `servers`)
  * Ensure the YAML indentation is correct
  * Look at Hermes Agent startup logs for connection messages
  * Tool names are prefixed with `mcp_{server}_{tool}` \-- look for that pattern


### Connection keeps dropping[​](<#connection-keeps-dropping> "Direct link to Connection keeps dropping")
The client retries up to 5 times with exponential backoff (1s, 2s, 4s, 8s, 16s, capped at 60s). If the server is fundamentally unreachable, it gives up after 5 attempts. Check the server process and network connectivity.
## Examples[​](<#examples> "Direct link to Examples")
### Time Server (uvx)[​](<#time-server-uvx> "Direct link to Time Server \(uvx\)")
[code] 
    mcp_servers:  
      time:  
        command: "uvx"  
        args: ["mcp-server-time"]  
    
[/code]
Registers tools like `mcp_time_get_current_time`.
### Filesystem Server (npx)[​](<#filesystem-server-npx> "Direct link to Filesystem Server \(npx\)")
[code] 
    mcp_servers:  
      filesystem:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]  
        timeout: 30  
    
[/code]
Registers tools like `mcp_filesystem_read_file`, `mcp_filesystem_write_file`, `mcp_filesystem_list_directory`.
### GitHub Server with Authentication[​](<#github-server-with-authentication> "Direct link to GitHub Server with Authentication")
[code] 
    mcp_servers:  
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"  
        timeout: 60  
    
[/code]
Registers tools like `mcp_github_list_issues`, `mcp_github_create_pull_request`, etc.
### Remote HTTP Server[​](<#remote-http-server> "Direct link to Remote HTTP Server")
[code] 
    mcp_servers:  
      company_api:  
        url: "https://mcp.mycompany.com/v1/mcp"  
        headers:  
          Authorization: "Bearer sk-xxxxxxxxxxxxxxxxxxxx"  
          X-Team-Id: "engineering"  
        timeout: 180  
        connect_timeout: 30  
    
[/code]
### Multiple Servers[​](<#multiple-servers> "Direct link to Multiple Servers")
[code] 
    mcp_servers:  
      time:  
        command: "uvx"  
        args: ["mcp-server-time"]  
      
      filesystem:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]  
      
      github:  
        command: "npx"  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"  
      
      company_api:  
        url: "https://mcp.internal.company.com/mcp"  
        headers:  
          Authorization: "Bearer sk-xxxxxxxxxxxxxxxxxxxx"  
        timeout: 300  
    
[/code]
All tools from all servers are registered and available simultaneously. Each server's tools are prefixed with its name to avoid collisions.
## Sampling (Server-Initiated LLM Requests)[​](<#sampling-server-initiated-llm-requests> "Direct link to Sampling \(Server-Initiated LLM Requests\)")
Hermes supports MCP's `sampling/createMessage` capability — MCP servers can request LLM completions through the agent during tool execution. This enables agent-in-the-loop workflows (data analysis, content generation, decision-making).
Sampling is **enabled by default**. Configure per server:
[code] 
    mcp_servers:  
      my_server:  
        command: "npx"  
        args: ["-y", "my-mcp-server"]  
        sampling:  
          enabled: true           # default: true  
          model: "gemini-3-flash" # model override (optional)  
          max_tokens_cap: 4096    # max tokens per request  
          timeout: 30             # LLM call timeout (seconds)  
          max_rpm: 10             # max requests per minute  
          allowed_models: []      # model whitelist (empty = all)  
          max_tool_rounds: 5      # tool loop limit (0 = disable)  
          log_level: "info"       # audit verbosity  
    
[/code]
Servers can also include `tools` in sampling requests for multi-turn tool-augmented workflows. The `max_tool_rounds` config prevents infinite tool loops. Per-server audit metrics (requests, errors, tokens, tool use count) are tracked via `get_mcp_status()`.
Disable sampling for untrusted servers with `sampling: { enabled: false }`.
## Notes[​](<#notes> "Direct link to Notes")
  * MCP tools are called synchronously from the agent's perspective but run asynchronously on a dedicated background event loop
  * Tool results are returned as JSON with either `{"result": "..."}` or `{"error": "..."}`
  * The native MCP client is independent of `mcporter` \-- you can use both simultaneously
  * Server connections are persistent and shared across all conversations in the same agent process
  * Adding or removing servers requires restarting the agent (no hot-reload currently)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [Quick Start](<#quick-start>)
  * [Configuration Reference](<#configuration-reference>)
    * [Stdio Transport (command + args)](<#stdio-transport-command--args>)
    * [HTTP Transport (url)](<#http-transport-url>)
    * [All Config Options](<#all-config-options>)
  * [How It Works](<#how-it-works>)
    * [Startup Discovery](<#startup-discovery>)
    * [Tool Naming Convention](<#tool-naming-convention>)
    * [Auto-Injection](<#auto-injection>)
    * [Connection Lifecycle](<#connection-lifecycle>)
    * [Idempotency](<#idempotency>)
  * [Transport Types](<#transport-types>)
    * [Stdio Transport](<#stdio-transport>)
    * [HTTP / StreamableHTTP Transport](<#http--streamablehttp-transport>)
  * [Security](<#security>)
    * [Environment Variable Filtering](<#environment-variable-filtering>)
    * [Credential Stripping in Error Messages](<#credential-stripping-in-error-messages>)
  * [Troubleshooting](<#troubleshooting>)
    * ["MCP SDK not available -- skipping MCP tool discovery"](<#mcp-sdk-not-available----skipping-mcp-tool-discovery>)
    * ["No MCP servers configured"](<#no-mcp-servers-configured>)
    * ["Failed to connect to MCP server 'X'"](<#failed-to-connect-to-mcp-server-x>)
    * ["MCP server 'X' requires HTTP transport but mcp.client.streamable_http is not available"](<#mcp-server-x-requires-http-transport-but-mcpclientstreamable_http-is-not-available>)
    * [Tools not appearing](<#tools-not-appearing>)
    * [Connection keeps dropping](<#connection-keeps-dropping>)
  * [Examples](<#examples>)
    * [Time Server (uvx)](<#time-server-uvx>)
    * [Filesystem Server (npx)](<#filesystem-server-npx>)
    * [GitHub Server with Authentication](<#github-server-with-authentication>)
    * [Remote HTTP Server](<#remote-http-server>)
    * [Multiple Servers](<#multiple-servers>)
  * [Sampling (Server-Initiated LLM Requests)](<#sampling-server-initiated-llm-requests>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mcp/mcp-native-mcp -->
