On this page
Manage Apple Notes via memo CLI: create, search, edit.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/apple/apple-notes`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Platforms| macos  
Tags| `Notes`, `Apple`, `macOS`, `note-taking`  
Related skills| [`obsidian`](</docs/user-guide/skills/bundled/note-taking/note-taking-obsidian>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Apple Notes
Use `memo` to manage Apple Notes directly from the terminal. Notes sync across all Apple devices via iCloud.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **macOS** with Notes.app
  * Install: `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
  * Grant Automation access to Notes.app when prompted (System Settings → Privacy → Automation)


## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * User asks to create, view, or search Apple Notes
  * Saving information to Notes.app for cross-device access
  * Organizing notes into folders
  * Exporting notes to Markdown/HTML


## When NOT to Use[​](<#when-not-to-use> "Direct link to When NOT to Use")
  * Obsidian vault management → use the `obsidian` skill
  * Bear Notes → separate app (not supported here)
  * Quick agent-only notes → use the `memory` tool instead


## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
### View Notes[​](<#view-notes> "Direct link to View Notes")
[code] 
    memo notes                        # List all notes  
    memo notes -f "Folder Name"       # Filter by folder  
    memo notes -s "query"             # Search notes (fuzzy)  
    
[/code]
### Create Notes[​](<#create-notes> "Direct link to Create Notes")
[code] 
    memo notes -a                     # Interactive editor  
    memo notes -a "Note Title"        # Quick add with title  
    
[/code]
### Edit Notes[​](<#edit-notes> "Direct link to Edit Notes")
[code] 
    memo notes -e                     # Interactive selection to edit  
    
[/code]
### Delete Notes[​](<#delete-notes> "Direct link to Delete Notes")
[code] 
    memo notes -d                     # Interactive selection to delete  
    
[/code]
### Move Notes[​](<#move-notes> "Direct link to Move Notes")
[code] 
    memo notes -m                     # Move note to folder (interactive)  
    
[/code]
### Export Notes[​](<#export-notes> "Direct link to Export Notes")
[code] 
    memo notes -ex                    # Export to HTML/Markdown  
    
[/code]
## Limitations[​](<#limitations> "Direct link to Limitations")
  * Cannot edit notes containing images or attachments
  * Interactive prompts require terminal access (use pty=true if needed)
  * macOS only — requires Apple Notes.app


## Rules[​](<#rules> "Direct link to Rules")
  1. Prefer Apple Notes when user wants cross-device sync (iPhone/iPad/Mac)
  2. Use the `memory` tool for agent-internal notes that don't need to sync
  3. Use the `obsidian` skill for Markdown-native knowledge management


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [When to Use](<#when-to-use>)
  * [When NOT to Use](<#when-not-to-use>)
  * [Quick Reference](<#quick-reference>)
    * [View Notes](<#view-notes>)
    * [Create Notes](<#create-notes>)
    * [Edit Notes](<#edit-notes>)
    * [Delete Notes](<#delete-notes>)
    * [Move Notes](<#move-notes>)
    * [Export Notes](<#export-notes>)
  * [Limitations](<#limitations>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/apple/apple-apple-notes -->
