On this page
Edit PDF text/typos/titles via nano-pdf CLI (NL prompts).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/productivity/nano-pdf`  
Version| `1.0.0`  
Author| community  
License| MIT  
Tags| `PDF`, `Documents`, `Editing`, `NLP`, `Productivity`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# nano-pdf
Edit PDFs using natural-language instructions. Point it at a page and describe what to change.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
[code] 
    # Install with uv (recommended — already available in Hermes)  
    uv pip install nano-pdf  
      
    # Or with pip  
    pip install nano-pdf  
    
[/code]
## Usage[​](<#usage> "Direct link to Usage")
[code] 
    nano-pdf edit <file.pdf> <page_number> "<instruction>"  
    
[/code]
## Examples[​](<#examples> "Direct link to Examples")
[code] 
    # Change a title on page 1  
    nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"  
      
    # Update a date on a specific page  
    nano-pdf edit report.pdf 3 "Update the date from January to February 2026"  
      
    # Fix content  
    nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"  
    
[/code]
## Notes[​](<#notes> "Direct link to Notes")
  * Page numbers may be 0-based or 1-based depending on version — if the edit hits the wrong page, retry with ±1
  * Always verify the output PDF after editing (use `read_file` to check file size, or open it)
  * The tool uses an LLM under the hood — requires an API key (check `nano-pdf --help` for config)
  * Works well for text changes; complex layout modifications may need a different approach


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [Usage](<#usage>)
  * [Examples](<#examples>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-nano-pdf -->
