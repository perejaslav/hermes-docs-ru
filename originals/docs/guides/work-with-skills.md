On this page
Skills are on-demand knowledge documents that teach Hermes how to handle specific tasks — from generating ASCII art to managing GitHub PRs. This guide walks you through using them day to day.
For the full technical reference, see [Skills System](</docs/user-guide/features/skills>).
* * *
## Finding Skills[​](<#finding-skills> "Direct link to Finding Skills")
Every Hermes installation ships with bundled skills. See what's available:
[code] 
    # In any chat session:  
    /skills  
      
    # Or from the CLI:  
    hermes skills list  
    
[/code]
This shows a compact list with names and descriptions:
[code] 
    ascii-art         Generate ASCII art using pyfiglet, cowsay, boxes...  
    arxiv             Search and retrieve academic papers from arXiv...  
    github-pr-workflow Full PR lifecycle — create branches, commit...  
    plan              Plan mode — inspect context, write a markdown...  
    excalidraw        Create hand-drawn style diagrams using Excalidraw...  
    
[/code]
### Searching for a Skill[​](<#searching-for-a-skill> "Direct link to Searching for a Skill")
[code] 
    # Search by keyword  
    /skills search docker  
    /skills search music  
    
[/code]
### The Skills Hub[​](<#the-skills-hub> "Direct link to The Skills Hub")
Official optional skills (heavier or niche skills not active by default) are available via the Hub:
[code] 
    # Browse official optional skills  
    /skills browse  
      
    # Search the hub  
    /skills search blockchain  
    
[/code]
* * *
## Using a Skill[​](<#using-a-skill> "Direct link to Using a Skill")
Every installed skill is automatically a slash command. Just type its name:
[code] 
    # Load a skill and give it a task  
    /ascii-art Make a banner that says "HELLO WORLD"  
    /plan Design a REST API for a todo app  
    /github-pr-workflow Create a PR for the auth refactor  
      
    # Just the skill name (no task) loads it and lets you describe what you need  
    /excalidraw  
    
[/code]
You can also trigger skills through natural conversation — ask Hermes to use a specific skill, and it will load it via the `skill_view` tool.
### Progressive Disclosure[​](<#progressive-disclosure> "Direct link to Progressive Disclosure")
Skills use a token-efficient loading pattern. The agent doesn't load everything at once:
  1. **`skills_list()`** — compact list of all skills (~3k tokens). Loaded at session start.
  2. **`skill_view(name)`** — full SKILL.md content for one skill. Loaded when the agent decides it needs that skill.
  3. **`skill_view(name, file_path)`** — a specific reference file within the skill. Only loaded if needed.


This means skills don't cost tokens until they're actually used.
* * *
## Installing from the Hub[​](<#installing-from-the-hub> "Direct link to Installing from the Hub")
Official optional skills ship with Hermes but aren't active by default. Install them explicitly:
[code] 
    # Install an official optional skill  
    hermes skills install official/research/arxiv  
      
    # Install from the hub in a chat session  
    /skills install official/creative/songwriting-and-ai-music  
      
    # Install a single-file SKILL.md directly from any HTTP(S) URL  
    hermes skills install https://sharethis.chat/SKILL.md  
    /skills install https://example.com/SKILL.md --name my-skill  
    
[/code]
What happens:
  1. The skill directory is copied to `~/.hermes/skills/`
  2. It appears in your `skills_list` output
  3. It becomes available as a slash command


tip
Installed skills take effect in new sessions. If you want it available in the current session, use `/reset` to start fresh, or add `--now` to invalidate the prompt cache immediately (costs more tokens on the next turn).
### Verifying Installation[​](<#verifying-installation> "Direct link to Verifying Installation")
[code] 
    # Check it's there  
    hermes skills list | grep arxiv  
      
    # Or in chat  
    /skills search arxiv  
    
[/code]
* * *
## Plugin-Provided Skills[​](<#plugin-provided-skills> "Direct link to Plugin-Provided Skills")
Plugins can bundle their own skills using namespaced names (`plugin:skill`). This prevents name collisions with built-in skills.
[code] 
    # Load a plugin skill by its qualified name  
    skill_view("superpowers:writing-plans")  
      
    # Built-in skill with the same base name is unaffected  
    skill_view("writing-plans")  
    
[/code]
Plugin skills are **not** listed in the system prompt and don't appear in `skills_list`. They're opt-in — load them explicitly when you know a plugin provides one. When loaded, the agent sees a banner listing sibling skills from the same plugin.
For how to ship skills in your own plugin, see [Build a Hermes Plugin → Bundle skills](</docs/guides/build-a-hermes-plugin#bundle-skills>).
* * *
## Configuring Skill Settings[​](<#configuring-skill-settings> "Direct link to Configuring Skill Settings")
Some skills declare configuration they need in their frontmatter:
[code] 
    metadata:  
      hermes:  
        config:  
          - key: tenor.api_key  
            description: "Tenor API key for GIF search"  
            prompt: "Enter your Tenor API key"  
            url: "https://developers.google.com/tenor/guides/quickstart"  
    
[/code]
When a skill with config is first loaded, Hermes prompts you for the values. They're stored in `config.yaml` under `skills.config.*`.
Manage skill config from the CLI:
[code] 
    # Interactive config for a specific skill  
    hermes skills config gif-search  
      
    # View all skill config  
    hermes config get skills.config  
    
[/code]
* * *
## Creating Your Own Skill[​](<#creating-your-own-skill> "Direct link to Creating Your Own Skill")
Skills are just markdown files with YAML frontmatter. Creating one takes under five minutes.
### 1\. Create the Directory[​](<#1-create-the-directory> "Direct link to 1. Create the Directory")
[code] 
    mkdir -p ~/.hermes/skills/my-category/my-skill  
    
[/code]
### 2\. Write SKILL.md[​](<#2-write-skillmd> "Direct link to 2. Write SKILL.md")
~/.hermes/skills/my-category/my-skill/SKILL.md
[code]
    ---  
    name: my-skill  
    description: Brief description of what this skill does  
    version: 1.0.0  
    metadata:  
      hermes:  
        tags: [my-tag, automation]  
        category: my-category  
    ---  
      
    # My Skill  
      
    ## When to Use  
    Use this skill when the user asks about [specific topic] or needs to [specific task].  
      
    ## Procedure  
    1. First, check if [prerequisite] is available  
    2. Run `command --with-flags`  
    3. Parse the output and present results  
      
    ## Pitfalls  
    - Common failure: [description]. Fix: [solution]  
    - Watch out for [edge case]  
      
    ## Verification  
    Run `check-command` to confirm the result is correct.  
    
[/code]
### 3\. Add Reference Files (Optional)[​](<#3-add-reference-files-optional> "Direct link to 3. Add Reference Files \(Optional\)")
Skills can include supporting files the agent loads on demand:
[code] 
    my-skill/  
    ├── SKILL.md                    # Main skill document  
    ├── references/  
    │   ├── api-docs.md             # API reference the agent can consult  
    │   └── examples.md             # Example inputs/outputs  
    ├── templates/  
    │   └── config.yaml             # Template files the agent can use  
    └── scripts/  
        └── setup.sh                # Scripts the agent can execute  
    
[/code]
Reference these in your SKILL.md:
[code] 
    For API details, load the reference: `skill_view("my-skill", "references/api-docs.md")`  
    
[/code]
### 4\. Test It[​](<#4-test-it> "Direct link to 4. Test It")
Start a new session and try your skill:
[code] 
    hermes chat -q "/my-skill help me with the thing"  
    
[/code]
The skill appears automatically — no registration needed. Drop it in `~/.hermes/skills/` and it's live.
info
The agent can also create and update skills itself using `skill_manage`. After solving a complex problem, Hermes may offer to save the approach as a skill for next time.
* * *
## Per-Platform Skill Management[​](<#per-platform-skill-management> "Direct link to Per-Platform Skill Management")
Control which skills are available on which platforms:
[code] 
    hermes skills  
    
[/code]
This opens an interactive TUI where you can enable or disable skills per platform (CLI, Telegram, Discord, etc.). Useful when you want certain skills only available in specific contexts — for example, keeping development skills off Telegram.
* * *
## Skills vs Memory[​](<#skills-vs-memory> "Direct link to Skills vs Memory")
Both are persistent across sessions, but they serve different purposes:
| Skills| Memory  
---|---|---  
**What**|  Procedural knowledge — how to do things| Factual knowledge — what things are  
**When**|  Loaded on demand, only when relevant| Injected into every session automatically  
**Size**|  Can be large (hundreds of lines)| Should be compact (key facts only)  
**Cost**|  Zero tokens until loaded| Small but constant token cost  
**Examples**|  "How to deploy to Kubernetes"| "User prefers dark mode, lives in PST"  
**Who creates**|  You, the agent, or installed from Hub| The agent, based on conversations  
**Rule of thumb:** If you'd put it in a reference document, it's a skill. If you'd put it on a sticky note, it's memory.
* * *
## Tips[​](<#tips> "Direct link to Tips")
**Keep skills focused.** A skill that tries to cover "all of DevOps" will be too long and too vague. A skill that covers "deploy a Python app to Fly.io" is specific enough to be genuinely useful.
**Let the agent create skills.** After a complex multi-step task, Hermes will often offer to save the approach as a skill. Say yes — these agent-authored skills capture the exact workflow including pitfalls that were discovered along the way.
**Use categories.** Organize skills into subdirectories (`~/.hermes/skills/devops/`, `~/.hermes/skills/research/`, etc.). This keeps the list manageable and helps the agent find relevant skills faster.
**Update skills when they go stale.** If you use a skill and hit issues not covered by it, tell Hermes to update the skill with what you learned. Skills that aren't maintained become liabilities.
* * *
_For the complete skills reference — frontmatter fields, conditional activation, external directories, and more — see[Skills System](</docs/user-guide/features/skills>)._
  * [Finding Skills](<#finding-skills>)
    * [Searching for a Skill](<#searching-for-a-skill>)
    * [The Skills Hub](<#the-skills-hub>)
  * [Using a Skill](<#using-a-skill>)
    * [Progressive Disclosure](<#progressive-disclosure>)
  * [Installing from the Hub](<#installing-from-the-hub>)
    * [Verifying Installation](<#verifying-installation>)
  * [Plugin-Provided Skills](<#plugin-provided-skills>)
  * [Configuring Skill Settings](<#configuring-skill-settings>)
  * [Creating Your Own Skill](<#creating-your-own-skill>)
    * [1\. Create the Directory](<#1-create-the-directory>)
    * [2\. Write SKILL.md](<#2-write-skillmd>)
    * [3\. Add Reference Files (Optional)](<#3-add-reference-files-optional>)
    * [4\. Test It](<#4-test-it>)
  * [Per-Platform Skill Management](<#per-platform-skill-management>)
  * [Skills vs Memory](<#skills-vs-memory>)
  * [Tips](<#tips>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills -->
