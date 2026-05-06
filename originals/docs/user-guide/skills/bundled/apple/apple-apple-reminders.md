On this page
Apple Reminders via remindctl: add, list, complete.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/apple/apple-reminders`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Platforms| macos  
Tags| `Reminders`, `tasks`, `todo`, `macOS`, `Apple`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Apple Reminders
Use `remindctl` to manage Apple Reminders directly from the terminal. Tasks sync across all Apple devices via iCloud.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **macOS** with Reminders.app
  * Install: `brew install steipete/tap/remindctl`
  * Grant Reminders permission when prompted
  * Check: `remindctl status` / Request: `remindctl authorize`


## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * User mentions "reminder" or "Reminders app"
  * Creating personal to-dos with due dates that sync to iOS
  * Managing Apple Reminders lists
  * User wants tasks to appear on their iPhone/iPad


## When NOT to Use[​](<#when-not-to-use> "Direct link to When NOT to Use")
  * Scheduling agent alerts → use the cronjob tool instead
  * Calendar events → use Apple Calendar or Google Calendar
  * Project task management → use GitHub Issues, Notion, etc.
  * If user says "remind me" but means an agent alert → clarify first


## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
### View Reminders[​](<#view-reminders> "Direct link to View Reminders")
[code] 
    remindctl                    # Today's reminders  
    remindctl today              # Today  
    remindctl tomorrow           # Tomorrow  
    remindctl week               # This week  
    remindctl overdue            # Past due  
    remindctl all                # Everything  
    remindctl 2026-01-04         # Specific date  
    
[/code]
### Manage Lists[​](<#manage-lists> "Direct link to Manage Lists")
[code] 
    remindctl list               # List all lists  
    remindctl list Work          # Show specific list  
    remindctl list Projects --create    # Create list  
    remindctl list Work --delete        # Delete list  
    
[/code]
### Create Reminders[​](<#create-reminders> "Direct link to Create Reminders")
[code] 
    remindctl add "Buy milk"  
    remindctl add --title "Call mom" --list Personal --due tomorrow  
    remindctl add --title "Meeting prep" --due "2026-02-15 09:00"  
    
[/code]
### Complete / Delete[​](<#complete--delete> "Direct link to Complete / Delete")
[code] 
    remindctl complete 1 2 3          # Complete by ID  
    remindctl delete 4A83 --force     # Delete by ID  
    
[/code]
### Output Formats[​](<#output-formats> "Direct link to Output Formats")
[code] 
    remindctl today --json       # JSON for scripting  
    remindctl today --plain      # TSV format  
    remindctl today --quiet      # Counts only  
    
[/code]
## Date Formats[​](<#date-formats> "Direct link to Date Formats")
Accepted by `--due` and date filters:
  * `today`, `tomorrow`, `yesterday`
  * `YYYY-MM-DD`
  * `YYYY-MM-DD HH:mm`
  * ISO 8601 (`2026-01-04T12:34:56Z`)


## Rules[​](<#rules> "Direct link to Rules")
  1. When user says "remind me", clarify: Apple Reminders (syncs to phone) vs agent cronjob alert
  2. Always confirm reminder content and due date before creating
  3. Use `--json` for programmatic parsing


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [When to Use](<#when-to-use>)
  * [When NOT to Use](<#when-not-to-use>)
  * [Quick Reference](<#quick-reference>)
    * [View Reminders](<#view-reminders>)
    * [Manage Lists](<#manage-lists>)
    * [Create Reminders](<#create-reminders>)
    * [Complete / Delete](<#complete--delete>)
    * [Output Formats](<#output-formats>)
  * [Date Formats](<#date-formats>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/apple/apple-apple-reminders -->
