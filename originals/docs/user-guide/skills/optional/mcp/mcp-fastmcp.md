On this page
Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. Use when creating a new MCP server, wrapping an API or database as MCP tools, exposing resources or prompts, or preparing a FastMCP server for Claude Code, Cursor, or HTTP deployment.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mcp/fastmcp`  
Path| `optional-skills/mcp/fastmcp`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Tags| `MCP`, `FastMCP`, `Python`, `Tools`, `Resources`, `Prompts`, `Deployment`  
Related skills| [`native-mcp`](</docs/user-guide/skills/bundled/mcp/mcp-native-mcp>), [`mcporter`](</docs/user-guide/skills/optional/mcp/mcp-mcporter>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# FastMCP
Build MCP servers in Python with FastMCP, validate them locally, install them into MCP clients, and deploy them as HTTP endpoints.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
Use this skill when the task is to:
  * create a new MCP server in Python
  * wrap an API, database, CLI, or file-processing workflow as MCP tools
  * expose resources or prompts in addition to tools
  * smoke-test a server with the FastMCP CLI before wiring it into Hermes or another client
  * install a server into Claude Code, Claude Desktop, Cursor, or a similar MCP client
  * prepare a FastMCP server repo for HTTP deployment


Use `native-mcp` when the server already exists and only needs to be connected to Hermes. Use `mcporter` when the goal is ad-hoc CLI access to an existing MCP server instead of building one.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
Install FastMCP in the working environment first:
[code] 
    pip install fastmcp  
    fastmcp version  
    
[/code]
For the API template, install `httpx` if it is not already present:
[code] 
    pip install httpx  
    
[/code]
## Included Files[​](<#included-files> "Direct link to Included Files")
### Templates[​](<#templates> "Direct link to Templates")
  * `templates/api_wrapper.py` \- REST API wrapper with auth header support
  * `templates/database_server.py` \- read-only SQLite query server
  * `templates/file_processor.py` \- text-file inspection and search server


### Scripts[​](<#scripts> "Direct link to Scripts")
  * `scripts/scaffold_fastmcp.py` \- copy a starter template and replace the server name placeholder


### References[​](<#references> "Direct link to References")
  * `references/fastmcp-cli.md` \- FastMCP CLI workflow, installation targets, and deployment checks


## Workflow[​](<#workflow> "Direct link to Workflow")
### 1\. Pick the Smallest Viable Server Shape[​](<#1-pick-the-smallest-viable-server-shape> "Direct link to 1. Pick the Smallest Viable Server Shape")
Choose the narrowest useful surface area first:
  * API wrapper: start with 1-3 high-value endpoints, not the whole API
  * database server: expose read-only introspection and a constrained query path
  * file processor: expose deterministic operations with explicit path arguments
  * prompts/resources: add only when the client needs reusable prompt templates or discoverable documents


Prefer a thin server with good names, docstrings, and schemas over a large server with vague tools.
### 2\. Scaffold from a Template[​](<#2-scaffold-from-a-template> "Direct link to 2. Scaffold from a Template")
Copy a template directly or use the scaffold helper:
[code] 
    python ~/.hermes/skills/mcp/fastmcp/scripts/scaffold_fastmcp.py \  
      --template api_wrapper \  
      --name "Acme API" \  
      --output ./acme_server.py  
    
[/code]
Available templates:
[code] 
    python ~/.hermes/skills/mcp/fastmcp/scripts/scaffold_fastmcp.py --list  
    
[/code]
If copying manually, replace `__SERVER_NAME__` with a real server name.
### 3\. Implement Tools First[​](<#3-implement-tools-first> "Direct link to 3. Implement Tools First")
Start with `@mcp.tool` functions before adding resources or prompts.
Rules for tool design:
  * Give every tool a concrete verb-based name
  * Write docstrings as user-facing tool descriptions
  * Keep parameters explicit and typed
  * Return structured JSON-safe data where possible
  * Validate unsafe inputs early
  * Prefer read-only behavior by default for first versions


Good tool examples:
  * `get_customer`
  * `search_tickets`
  * `describe_table`
  * `summarize_text_file`


Weak tool examples:
  * `run`
  * `process`
  * `do_thing`


### 4\. Add Resources and Prompts Only When They Help[​](<#4-add-resources-and-prompts-only-when-they-help> "Direct link to 4. Add Resources and Prompts Only When They Help")
Add `@mcp.resource` when the client benefits from fetching stable read-only content such as schemas, policy docs, or generated reports.
Add `@mcp.prompt` when the server should provide a reusable prompt template for a known workflow.
Do not turn every document into a prompt. Prefer:
  * tools for actions
  * resources for data/document retrieval
  * prompts for reusable LLM instructions


### 5\. Test the Server Before Integrating It Anywhere[​](<#5-test-the-server-before-integrating-it-anywhere> "Direct link to 5. Test the Server Before Integrating It Anywhere")
Use the FastMCP CLI for local validation:
[code] 
    fastmcp inspect acme_server.py:mcp  
    fastmcp list acme_server.py --json  
    fastmcp call acme_server.py search_resources query=router limit=5 --json  
    
[/code]
For fast iterative debugging, run the server locally:
[code] 
    fastmcp run acme_server.py:mcp  
    
[/code]
To test HTTP transport locally:
[code] 
    fastmcp run acme_server.py:mcp --transport http --host 127.0.0.1 --port 8000  
    fastmcp list http://127.0.0.1:8000/mcp --json  
    fastmcp call http://127.0.0.1:8000/mcp search_resources query=router --json  
    
[/code]
Always run at least one real `fastmcp call` against each new tool before claiming the server works.
### 6\. Install into a Client When Local Validation Passes[​](<#6-install-into-a-client-when-local-validation-passes> "Direct link to 6. Install into a Client When Local Validation Passes")
FastMCP can register the server with supported MCP clients:
[code] 
    fastmcp install claude-code acme_server.py  
    fastmcp install claude-desktop acme_server.py  
    fastmcp install cursor acme_server.py -e .  
    
[/code]
Use `fastmcp discover` to inspect named MCP servers already configured on the machine.
When the goal is Hermes integration, either:
  * configure the server in `~/.hermes/config.yaml` using the `native-mcp` skill, or
  * keep using FastMCP CLI commands during development until the interface stabilizes


### 7\. Deploy After the Local Contract Is Stable[​](<#7-deploy-after-the-local-contract-is-stable> "Direct link to 7. Deploy After the Local Contract Is Stable")
For managed hosting, Prefect Horizon is the path FastMCP documents most directly. Before deployment:
[code] 
    fastmcp inspect acme_server.py:mcp  
    
[/code]
Make sure the repo contains:
  * a Python file with the FastMCP server object
  * `requirements.txt` or `pyproject.toml`
  * any environment-variable documentation needed for deployment


For generic HTTP hosting, validate the HTTP transport locally first, then deploy on any Python-compatible platform that can expose the server port.
## Common Patterns[​](<#common-patterns> "Direct link to Common Patterns")
### API Wrapper Pattern[​](<#api-wrapper-pattern> "Direct link to API Wrapper Pattern")
Use when exposing a REST or HTTP API as MCP tools.
Recommended first slice:
  * one read path
  * one list/search path
  * optional health check


Implementation notes:
  * keep auth in environment variables, not hardcoded
  * centralize request logic in one helper
  * surface API errors with concise context
  * normalize inconsistent upstream payloads before returning them


Start from `templates/api_wrapper.py`.
### Database Pattern[​](<#database-pattern> "Direct link to Database Pattern")
Use when exposing safe query and inspection capabilities.
Recommended first slice:
  * `list_tables`
  * `describe_table`
  * one constrained read query tool


Implementation notes:
  * default to read-only DB access
  * reject non-`SELECT` SQL in early versions
  * limit row counts
  * return rows plus column names


Start from `templates/database_server.py`.
### File Processor Pattern[​](<#file-processor-pattern> "Direct link to File Processor Pattern")
Use when the server needs to inspect or transform files on demand.
Recommended first slice:
  * summarize file contents
  * search within files
  * extract deterministic metadata


Implementation notes:
  * accept explicit file paths
  * check for missing files and encoding failures
  * cap previews and result counts
  * avoid shelling out unless a specific external tool is required


Start from `templates/file_processor.py`.
## Quality Bar[​](<#quality-bar> "Direct link to Quality Bar")
Before handing off a FastMCP server, verify all of the following:
  * server imports cleanly
  * `fastmcp inspect <file.py:mcp>` succeeds
  * `fastmcp list <server spec> --json` succeeds
  * every new tool has at least one real `fastmcp call`
  * environment variables are documented
  * the tool surface is small enough to understand without guesswork


## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### FastMCP command missing[​](<#fastmcp-command-missing> "Direct link to FastMCP command missing")
Install the package in the active environment:
[code] 
    pip install fastmcp  
    fastmcp version  
    
[/code]
### `fastmcp inspect` fails[​](<#fastmcp-inspect-fails> "Direct link to fastmcp-inspect-fails")
Check that:
  * the file imports without side effects that crash
  * the FastMCP instance is named correctly in `<file.py:object>`
  * optional dependencies from the template are installed


### Tool works in Python but not through CLI[​](<#tool-works-in-python-but-not-through-cli> "Direct link to Tool works in Python but not through CLI")
Run:
[code] 
    fastmcp list server.py --json  
    fastmcp call server.py your_tool_name --json  
    
[/code]
This usually exposes naming mismatches, missing required arguments, or non-serializable return values.
### Hermes cannot see the deployed server[​](<#hermes-cannot-see-the-deployed-server> "Direct link to Hermes cannot see the deployed server")
The server-building part may be correct while the Hermes config is not. Load the `native-mcp` skill and configure the server in `~/.hermes/config.yaml`, then restart Hermes.
## References[​](<#references-1> "Direct link to References")
For CLI details, install targets, and deployment checks, read `references/fastmcp-cli.md`.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [Included Files](<#included-files>)
    * [Templates](<#templates>)
    * [Scripts](<#scripts>)
    * [References](<#references>)
  * [Workflow](<#workflow>)
    * [1\. Pick the Smallest Viable Server Shape](<#1-pick-the-smallest-viable-server-shape>)
    * [2\. Scaffold from a Template](<#2-scaffold-from-a-template>)
    * [3\. Implement Tools First](<#3-implement-tools-first>)
    * [4\. Add Resources and Prompts Only When They Help](<#4-add-resources-and-prompts-only-when-they-help>)
    * [5\. Test the Server Before Integrating It Anywhere](<#5-test-the-server-before-integrating-it-anywhere>)
    * [6\. Install into a Client When Local Validation Passes](<#6-install-into-a-client-when-local-validation-passes>)
    * [7\. Deploy After the Local Contract Is Stable](<#7-deploy-after-the-local-contract-is-stable>)
  * [Common Patterns](<#common-patterns>)
    * [API Wrapper Pattern](<#api-wrapper-pattern>)
    * [Database Pattern](<#database-pattern>)
    * [File Processor Pattern](<#file-processor-pattern>)
  * [Quality Bar](<#quality-bar>)
  * [Troubleshooting](<#troubleshooting>)
    * [FastMCP command missing](<#fastmcp-command-missing>)
    * [`fastmcp inspect` fails](<#fastmcp-inspect-fails>)
    * [Tool works in Python but not through CLI](<#tool-works-in-python-but-not-through-cli>)
    * [Hermes cannot see the deployed server](<#hermes-cannot-see-the-deployed-server>)
  * [References](<#references-1>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mcp/mcp-fastmcp -->
