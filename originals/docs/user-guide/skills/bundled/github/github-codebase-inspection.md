On this page
Inspect codebases w/ pygount: LOC, languages, ratios.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/github/codebase-inspection`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Tags| `LOC`, `Code Analysis`, `pygount`, `Codebase`, `Metrics`, `Repository`  
Related skills| [`github-repo-management`](</docs/user-guide/skills/bundled/github/github-github-repo-management>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Codebase Inspection with pygount
Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * User asks for LOC (lines of code) count
  * User wants a language breakdown of a repo
  * User asks about codebase size or composition
  * User wants code-vs-comment ratios
  * General "how big is this repo" questions


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
[code] 
    pip install --break-system-packages pygount 2>/dev/null || pip install pygount  
    
[/code]
## 1\. Basic Summary (Most Common)[​](<#1-basic-summary-most-common> "Direct link to 1. Basic Summary \(Most Common\)")
Get a full language breakdown with file counts, code lines, and comment lines:
[code] 
    cd /path/to/repo  
    pygount --format=summary \  
      --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \  
      .  
    
[/code]
**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.
## 2\. Common Folder Exclusions[​](<#2-common-folder-exclusions> "Direct link to 2. Common Folder Exclusions")
Adjust based on the project type:
[code] 
    # Python projects  
    --folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"  
      
    # JavaScript/TypeScript projects  
    --folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"  
      
    # General catch-all  
    --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"  
    
[/code]
## 3\. Filter by Specific Language[​](<#3-filter-by-specific-language> "Direct link to 3. Filter by Specific Language")
[code] 
    # Only count Python files  
    pygount --suffix=py --format=summary .  
      
    # Only count Python and YAML  
    pygount --suffix=py,yaml,yml --format=summary .  
    
[/code]
## 4\. Detailed File-by-File Output[​](<#4-detailed-file-by-file-output> "Direct link to 4. Detailed File-by-File Output")
[code] 
    # Default format shows per-file breakdown  
    pygount --folders-to-skip=".git,node_modules,venv" .  
      
    # Sort by code lines (pipe through sort)  
    pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20  
    
[/code]
## 5\. Output Formats[​](<#5-output-formats> "Direct link to 5. Output Formats")
[code] 
    # Summary table (default recommendation)  
    pygount --format=summary .  
      
    # JSON output for programmatic use  
    pygount --format=json .  
      
    # Pipe-friendly: Language, file count, code, docs, empty, string  
    pygount --format=summary . 2>/dev/null  
    
[/code]
## 6\. Interpreting Results[​](<#6-interpreting-results> "Direct link to 6. Interpreting Results")
The summary table columns:
  * **Language** — detected programming language
  * **Files** — number of files of that language
  * **Code** — lines of actual code (executable/declarative)
  * **Comment** — lines that are comments or documentation
  * **%** — percentage of total


Special pseudo-languages:
  * `__empty__` — empty files
  * `__binary__` — binary files (images, compiled, etc.)
  * `__generated__` — auto-generated files (detected heuristically)
  * `__duplicate__` — files with identical content
  * `__unknown__` — unrecognized file types


## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
  2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
  3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
  4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [1\. Basic Summary (Most Common)](<#1-basic-summary-most-common>)
  * [2\. Common Folder Exclusions](<#2-common-folder-exclusions>)
  * [3\. Filter by Specific Language](<#3-filter-by-specific-language>)
  * [4\. Detailed File-by-File Output](<#4-detailed-file-by-file-output>)
  * [5\. Output Formats](<#5-output-formats>)
  * [6\. Interpreting Results](<#6-interpreting-results>)
  * [Pitfalls](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/github/github-codebase-inspection -->
