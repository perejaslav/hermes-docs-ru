On this page
Plan mode: write markdown plan to .hermes/plans/, no exec.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/software-development/plan`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Tags| `planning`, `plan-mode`, `implementation`, `workflow`  
Related skills| [`writing-plans`](</docs/user-guide/skills/bundled/software-development/software-development-writing-plans>), [`subagent-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Plan Mode
Use this skill when the user wants a plan instead of execution.
## Core behavior[​](<#core-behavior> "Direct link to Core behavior")
For this turn, you are planning only.
  * Do not implement code.
  * Do not edit project files except the plan markdown file.
  * Do not run mutating terminal commands, commit, push, or perform external actions.
  * You may inspect the repo or other context with read-only commands/tools when needed.
  * Your deliverable is a markdown plan saved inside the active workspace under `.hermes/plans/`.


## Output requirements[​](<#output-requirements> "Direct link to Output requirements")
Write a markdown plan that is concrete and actionable.
Include, when relevant:
  * Goal
  * Current context / assumptions
  * Proposed approach
  * Step-by-step plan
  * Files likely to change
  * Tests / validation
  * Risks, tradeoffs, and open questions


If the task is code-related, include exact file paths, likely test targets, and verification steps.
## Save location[​](<#save-location> "Direct link to Save location")
Save the plan with `write_file` under:
  * `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`


Treat that as relative to the active working directory / backend workspace. Hermes file tools are backend-aware, so using this relative path keeps the plan with the workspace on local, docker, ssh, modal, and daytona backends.
If the runtime provides a specific target path, use that exact path. If not, create a sensible timestamped filename yourself under `.hermes/plans/`.
## Interaction style[​](<#interaction-style> "Direct link to Interaction style")
  * If the request is clear enough, write the plan directly.
  * If no explicit instruction accompanies `/plan`, infer the task from the current conversation context.
  * If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
  * After saving the plan, reply briefly with what you planned and the saved path.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Core behavior](<#core-behavior>)
  * [Output requirements](<#output-requirements>)
  * [Save location](<#save-location>)
  * [Interaction style](<#interaction-style>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-plan -->
