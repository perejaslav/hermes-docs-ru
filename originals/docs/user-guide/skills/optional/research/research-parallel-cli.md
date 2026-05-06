On this page
Optional vendor skill for Parallel CLI — agent-native web search, extraction, deep research, enrichment, FindAll, and monitoring. Prefer JSON output and non-interactive flows.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/research/parallel-cli`  
Path| `optional-skills/research/parallel-cli`  
Version| `1.1.0`  
Author| Hermes Agent  
License| MIT  
Tags| `Research`, `Web`, `Search`, `Deep-Research`, `Enrichment`, `CLI`  
Related skills| [`duckduckgo-search`](</docs/user-guide/skills/optional/research/research-duckduckgo-search>), [`mcporter`](</docs/user-guide/skills/optional/mcp/mcp-mcporter>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Parallel CLI
Use `parallel-cli` when the user explicitly wants Parallel, or when a terminal-native workflow would benefit from Parallel's vendor-specific stack for web search, extraction, deep research, enrichment, entity discovery, or monitoring.
This is an optional third-party workflow, not a Hermes core capability.
Important expectations:
  * Parallel is a paid service with a free tier, not a fully free local tool.
  * It overlaps with Hermes native `web_search` / `web_extract`, so do not prefer it by default for ordinary lookups.
  * Prefer this skill when the user mentions Parallel specifically or needs capabilities like Parallel's enrichment, FindAll, or monitor workflows.


`parallel-cli` is designed for agents:
  * JSON output via `--json`
  * Non-interactive command execution
  * Async long-running jobs with `--no-wait`, `status`, and `poll`
  * Context chaining with `--previous-interaction-id`
  * Search, extract, research, enrichment, entity discovery, and monitoring in one CLI


## When to use it[​](<#when-to-use-it> "Direct link to When to use it")
Prefer this skill when:
  * The user explicitly mentions Parallel or `parallel-cli`
  * The task needs richer workflows than a simple one-shot search/extract pass
  * You need async deep research jobs that can be launched and polled later
  * You need structured enrichment, FindAll entity discovery, or monitoring


Prefer Hermes native `web_search` / `web_extract` for quick one-off lookups when Parallel is not specifically requested.
## Installation[​](<#installation> "Direct link to Installation")
Try the least invasive install path available for the environment.
### Homebrew[​](<#homebrew> "Direct link to Homebrew")
[code] 
    brew install parallel-web/tap/parallel-cli  
    
[/code]
### npm[​](<#npm> "Direct link to npm")
[code] 
    npm install -g parallel-web-cli  
    
[/code]
### Python package[​](<#python-package> "Direct link to Python package")
[code] 
    pip install "parallel-web-tools[cli]"  
    
[/code]
### Standalone installer[​](<#standalone-installer> "Direct link to Standalone installer")
[code] 
    curl -fsSL https://parallel.ai/install.sh | bash  
    
[/code]
If you want an isolated Python install, `pipx` can also work:
[code] 
    pipx install "parallel-web-tools[cli]"  
    pipx ensurepath  
    
[/code]
## Authentication[​](<#authentication> "Direct link to Authentication")
Interactive login:
[code] 
    parallel-cli login  
    
[/code]
Headless / SSH / CI:
[code] 
    parallel-cli login --device  
    
[/code]
API key environment variable:
[code] 
    export PARALLEL_API_KEY="***"  
    
[/code]
Verify current auth status:
[code] 
    parallel-cli auth  
    
[/code]
If auth requires browser interaction, run with `pty=true`.
## Core rule set[​](<#core-rule-set> "Direct link to Core rule set")
  1. Always prefer `--json` when you need machine-readable output.
  2. Prefer explicit arguments and non-interactive flows.
  3. For long-running jobs, use `--no-wait` and then `status` / `poll`.
  4. Cite only URLs returned by the CLI output.
  5. Save large JSON outputs to a temp file when follow-up questions are likely.
  6. Use background processes only for genuinely long-running workflows; otherwise run in foreground.
  7. Prefer Hermes native tools unless the user wants Parallel specifically or needs Parallel-only workflows.


## Quick reference[​](<#quick-reference> "Direct link to Quick reference")
[code] 
    parallel-cli  
    ├── auth  
    ├── login  
    ├── logout  
    ├── search  
    ├── extract / fetch  
    ├── research run|status|poll|processors  
    ├── enrich run|status|poll|plan|suggest|deploy  
    ├── findall run|ingest|status|poll|result|enrich|extend|schema|cancel  
    └── monitor create|list|get|update|delete|events|event-group|simulate  
    
[/code]
## Common flags and patterns[​](<#common-flags-and-patterns> "Direct link to Common flags and patterns")
Commonly useful flags:
  * `--json` for structured output
  * `--no-wait` for async jobs
  * `--previous-interaction-id <id>` for follow-up tasks that reuse earlier context
  * `--max-results <n>` for search result count
  * `--mode one-shot|agentic` for search behavior
  * `--include-domains domain1.com,domain2.com`
  * `--exclude-domains domain1.com,domain2.com`
  * `--after-date YYYY-MM-DD`


Read from stdin when convenient:
[code] 
    echo "What is the latest funding for Anthropic?" | parallel-cli search - --json  
    echo "Research question" | parallel-cli research run - --json  
    
[/code]
## Search[​](<#search> "Direct link to Search")
Use for current web lookups with structured results.
[code] 
    parallel-cli search "What is Anthropic's latest AI model?" --json  
    parallel-cli search "SEC filings for Apple" --include-domains sec.gov --json  
    parallel-cli search "bitcoin price" --after-date 2026-01-01 --max-results 10 --json  
    parallel-cli search "latest browser benchmarks" --mode one-shot --json  
    parallel-cli search "AI coding agent enterprise reviews" --mode agentic --json  
    
[/code]
Useful constraints:
  * `--include-domains` to narrow trusted sources
  * `--exclude-domains` to strip noisy domains
  * `--after-date` for recency filtering
  * `--max-results` when you need broader coverage


If you expect follow-up questions, save output:
[code] 
    parallel-cli search "latest React 19 changes" --json -o /tmp/react-19-search.json  
    
[/code]
When summarizing results:
  * lead with the answer
  * include dates, names, and concrete facts
  * cite only returned sources
  * avoid inventing URLs or source titles


## Extraction[​](<#extraction> "Direct link to Extraction")
Use to pull clean content or markdown from a URL.
[code] 
    parallel-cli extract https://example.com --json  
    parallel-cli extract https://company.com --objective "Find pricing info" --json  
    parallel-cli extract https://example.com --full-content --json  
    parallel-cli fetch https://example.com --json  
    
[/code]
Use `--objective` when the page is broad and you only need one slice of information.
## Deep research[​](<#deep-research> "Direct link to Deep research")
Use for deeper multi-step research tasks that may take time.
Common processor tiers:
  * `lite` / `base` for faster, cheaper passes
  * `core` / `pro` for more thorough synthesis
  * `ultra` for the heaviest research jobs


### Synchronous[​](<#synchronous> "Direct link to Synchronous")
[code] 
    parallel-cli research run \  
      "Compare the leading AI coding agents by pricing, model support, and enterprise controls" \  
      --processor core \  
      --json  
    
[/code]
### Async launch + poll[​](<#async-launch--poll> "Direct link to Async launch + poll")
[code] 
    parallel-cli research run \  
      "Compare the leading AI coding agents by pricing, model support, and enterprise controls" \  
      --processor ultra \  
      --no-wait \  
      --json  
      
    parallel-cli research status trun_xxx --json  
    parallel-cli research poll trun_xxx --json  
    parallel-cli research processors --json  
    
[/code]
### Context chaining / follow-up[​](<#context-chaining--follow-up> "Direct link to Context chaining / follow-up")
[code] 
    parallel-cli research run "What are the top AI coding agents?" --json  
    parallel-cli research run \  
      "What enterprise controls does the top-ranked one offer?" \  
      --previous-interaction-id trun_xxx \  
      --json  
    
[/code]
Recommended Hermes workflow:
  1. launch with `--no-wait --json`
  2. capture the returned run/task ID
  3. if the user wants to continue other work, keep moving
  4. later call `status` or `poll`
  5. summarize the final report with citations from the returned sources


## Enrichment[​](<#enrichment> "Direct link to Enrichment")
Use when the user has CSV/JSON/tabular inputs and wants additional columns inferred from web research.
### Suggest columns[​](<#suggest-columns> "Direct link to Suggest columns")
[code] 
    parallel-cli enrich suggest "Find the CEO and annual revenue" --json  
    
[/code]
### Plan a config[​](<#plan-a-config> "Direct link to Plan a config")
[code] 
    parallel-cli enrich plan -o config.yaml  
    
[/code]
### Inline data[​](<#inline-data> "Direct link to Inline data")
[code] 
    parallel-cli enrich run \  
      --data '[{"company": "Anthropic"}, {"company": "Mistral"}]' \  
      --intent "Find headquarters and employee count" \  
      --json  
    
[/code]
### Non-interactive file run[​](<#non-interactive-file-run> "Direct link to Non-interactive file run")
[code] 
    parallel-cli enrich run \  
      --source-type csv \  
      --source companies.csv \  
      --target enriched.csv \  
      --source-columns '[{"name": "company", "description": "Company name"}]' \  
      --intent "Find the CEO and annual revenue"  
    
[/code]
### YAML config run[​](<#yaml-config-run> "Direct link to YAML config run")
[code] 
    parallel-cli enrich run config.yaml  
    
[/code]
### Status / polling[​](<#status--polling> "Direct link to Status / polling")
[code] 
    parallel-cli enrich status <task_group_id> --json  
    parallel-cli enrich poll <task_group_id> --json  
    
[/code]
Use explicit JSON arrays for column definitions when operating non-interactively. Validate the output file before reporting success.
## FindAll[​](<#findall> "Direct link to FindAll")
Use for web-scale entity discovery when the user wants a discovered dataset rather than a short answer.
[code] 
    parallel-cli findall run "Find AI coding agent startups with enterprise offerings" --json  
    parallel-cli findall run "AI startups in healthcare" -n 25 --json  
    parallel-cli findall status <run_id> --json  
    parallel-cli findall poll <run_id> --json  
    parallel-cli findall result <run_id> --json  
    parallel-cli findall schema <run_id> --json  
    
[/code]
This is a better fit than ordinary search when the user wants a discovered set of entities that can be reviewed, filtered, or enriched later.
## Monitor[​](<#monitor> "Direct link to Monitor")
Use for ongoing change detection over time.
[code] 
    parallel-cli monitor list --json  
    parallel-cli monitor get <monitor_id> --json  
    parallel-cli monitor events <monitor_id> --json  
    parallel-cli monitor delete <monitor_id> --json  
    
[/code]
Creation is usually the sensitive part because cadence and delivery matter:
[code] 
    parallel-cli monitor create --help  
    
[/code]
Use this when the user wants recurring tracking of a page or source rather than a one-time fetch.
## Recommended Hermes usage patterns[​](<#recommended-hermes-usage-patterns> "Direct link to Recommended Hermes usage patterns")
### Fast answer with citations[​](<#fast-answer-with-citations> "Direct link to Fast answer with citations")
  1. Run `parallel-cli search ... --json`
  2. Parse titles, URLs, dates, excerpts
  3. Summarize with inline citations from the returned URLs only


### URL investigation[​](<#url-investigation> "Direct link to URL investigation")
  1. Run `parallel-cli extract URL --json`
  2. If needed, rerun with `--objective` or `--full-content`
  3. Quote or summarize the extracted markdown


### Long research workflow[​](<#long-research-workflow> "Direct link to Long research workflow")
  1. Run `parallel-cli research run ... --no-wait --json`
  2. Store the returned ID
  3. Continue other work or periodically poll
  4. Summarize the final report with citations


### Structured enrichment workflow[​](<#structured-enrichment-workflow> "Direct link to Structured enrichment workflow")
  1. Inspect the input file and columns
  2. Use `enrich suggest` or provide explicit enriched columns
  3. Run `enrich run`
  4. Poll for completion if needed
  5. Validate the output file before reporting success


## Error handling and exit codes[​](<#error-handling-and-exit-codes> "Direct link to Error handling and exit codes")
The CLI documents these exit codes:
  * `0` success
  * `2` bad input
  * `3` auth error
  * `4` API error
  * `5` timeout


If you hit auth errors:
  1. check `parallel-cli auth`
  2. confirm `PARALLEL_API_KEY` or run `parallel-cli login` / `parallel-cli login --device`
  3. verify `parallel-cli` is on `PATH`


## Maintenance[​](<#maintenance> "Direct link to Maintenance")
Check current auth / install state:
[code] 
    parallel-cli auth  
    parallel-cli --help  
    
[/code]
Update commands:
[code] 
    parallel-cli update  
    pip install --upgrade parallel-web-tools  
    parallel-cli config auto-update-check off  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * Do not omit `--json` unless the user explicitly wants human-formatted output.
  * Do not cite sources not present in the CLI output.
  * `login` may require PTY/browser interaction.
  * Prefer foreground execution for short tasks; do not overuse background processes.
  * For large result sets, save JSON to `/tmp/*.json` instead of stuffing everything into context.
  * Do not silently choose Parallel when Hermes native tools are already sufficient.
  * Remember this is a vendor workflow that usually requires account auth and paid usage beyond the free tier.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use it](<#when-to-use-it>)
  * [Installation](<#installation>)
    * [Homebrew](<#homebrew>)
    * [npm](<#npm>)
    * [Python package](<#python-package>)
    * [Standalone installer](<#standalone-installer>)
  * [Authentication](<#authentication>)
  * [Core rule set](<#core-rule-set>)
  * [Quick reference](<#quick-reference>)
  * [Common flags and patterns](<#common-flags-and-patterns>)
  * [Search](<#search>)
  * [Extraction](<#extraction>)
  * [Deep research](<#deep-research>)
    * [Synchronous](<#synchronous>)
    * [Async launch + poll](<#async-launch--poll>)
    * [Context chaining / follow-up](<#context-chaining--follow-up>)
  * [Enrichment](<#enrichment>)
    * [Suggest columns](<#suggest-columns>)
    * [Plan a config](<#plan-a-config>)
    * [Inline data](<#inline-data>)
    * [Non-interactive file run](<#non-interactive-file-run>)
    * [YAML config run](<#yaml-config-run>)
    * [Status / polling](<#status--polling>)
  * [FindAll](<#findall>)
  * [Monitor](<#monitor>)
  * [Recommended Hermes usage patterns](<#recommended-hermes-usage-patterns>)
    * [Fast answer with citations](<#fast-answer-with-citations>)
    * [URL investigation](<#url-investigation>)
    * [Long research workflow](<#long-research-workflow>)
    * [Structured enrichment workflow](<#structured-enrichment-workflow>)
  * [Error handling and exit codes](<#error-handling-and-exit-codes>)
  * [Maintenance](<#maintenance>)
  * [Pitfalls](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-parallel-cli -->
