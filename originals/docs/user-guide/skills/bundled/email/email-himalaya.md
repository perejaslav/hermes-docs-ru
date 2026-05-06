On this page
Himalaya CLI: IMAP/SMTP email from terminal.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/email/himalaya`  
Version| `1.1.0`  
Author| community  
License| MIT  
Tags| `Email`, `IMAP`, `SMTP`, `CLI`, `Communication`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Himalaya Email CLI
Himalaya is a CLI email client that lets you manage emails from the terminal using IMAP, SMTP, Notmuch, or Sendmail backends.
## References[​](<#references> "Direct link to References")
  * `references/configuration.md` (config file setup + IMAP/SMTP authentication)
  * `references/message-composition.md` (MML syntax for composing emails)


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  1. Himalaya CLI installed (`himalaya --version` to verify)
  2. A configuration file at `~/.config/himalaya/config.toml`
  3. IMAP/SMTP credentials configured (password stored securely)


### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Pre-built binary (Linux/macOS — recommended)  
    curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh  
      
    # macOS via Homebrew  
    brew install himalaya  
      
    # Or via cargo (any platform with Rust)  
    cargo install himalaya --locked  
    
[/code]
## Configuration Setup[​](<#configuration-setup> "Direct link to Configuration Setup")
Run the interactive wizard to set up an account:
[code] 
    himalaya account configure  
    
[/code]
Or create `~/.config/himalaya/config.toml` manually:
[code] 
    [accounts.personal]  
    email = "you@example.com"  
    display-name = "Your Name"  
    default = true  
      
    backend.type = "imap"  
    backend.host = "imap.example.com"  
    backend.port = 993  
    backend.encryption.type = "tls"  
    backend.login = "you@example.com"  
    backend.auth.type = "password"  
    backend.auth.cmd = "pass show email/imap"  # or use keyring  
      
    message.send.backend.type = "smtp"  
    message.send.backend.host = "smtp.example.com"  
    message.send.backend.port = 587  
    message.send.backend.encryption.type = "start-tls"  
    message.send.backend.login = "you@example.com"  
    message.send.backend.auth.type = "password"  
    message.send.backend.auth.cmd = "pass show email/smtp"  
      
    # Folder aliases (himalaya v1.2.0+ syntax). Required whenever the  
    # server's folder names don't match himalaya's canonical names  
    # (inbox/sent/drafts/trash). Gmail is the common case — see  
    # `references/configuration.md` for the `[Gmail]/Sent Mail` mapping.  
    folder.aliases.inbox = "INBOX"  
    folder.aliases.sent = "Sent"  
    folder.aliases.drafts = "Drafts"  
    folder.aliases.trash = "Trash"  
    
[/code]
> **Heads up on the alias syntax.** Pre-v1.2.0 docs used a `[accounts.NAME.folder.alias]` sub-section (singular `alias`). v1.2.0 silently ignores that form — TOML parses fine, but the alias resolver never reads it, so every lookup falls through to the canonical name. On Gmail this means save-to-Sent fails _after_ SMTP delivery succeeds, and `himalaya message send` exits non-zero. Any caller (agent, script, user) that retries on that exit code will re-run the entire send — including SMTP — producing duplicate emails to recipients. Always use `folder.aliases.X` (plural, dotted keys, directly under `[accounts.NAME]`).
## Hermes Integration Notes[​](<#hermes-integration-notes> "Direct link to Hermes Integration Notes")
  * **Reading, listing, searching, moving, deleting** all work directly through the terminal tool
  * **Composing/replying/forwarding** — piped input (`cat << EOF | himalaya template send`) is recommended for reliability. Interactive `$EDITOR` mode works with `pty=true` \+ background + process tool, but requires knowing the editor and its commands
  * Use `--output json` for structured output that's easier to parse programmatically
  * The `himalaya account configure` wizard requires interactive input — use PTY mode: `terminal(command="himalaya account configure", pty=true)`


## Common Operations[​](<#common-operations> "Direct link to Common Operations")
### List Folders[​](<#list-folders> "Direct link to List Folders")
[code] 
    himalaya folder list  
    
[/code]
### List Emails[​](<#list-emails> "Direct link to List Emails")
List emails in INBOX (default):
[code] 
    himalaya envelope list  
    
[/code]
List emails in a specific folder:
[code] 
    himalaya envelope list --folder "Sent"  
    
[/code]
List with pagination:
[code] 
    himalaya envelope list --page 1 --page-size 20  
    
[/code]
### Search Emails[​](<#search-emails> "Direct link to Search Emails")
[code] 
    himalaya envelope list from john@example.com subject meeting  
    
[/code]
### Read an Email[​](<#read-an-email> "Direct link to Read an Email")
Read email by ID (shows plain text):
[code] 
    himalaya message read 42  
    
[/code]
Export raw MIME:
[code] 
    himalaya message export 42 --full  
    
[/code]
### Reply to an Email[​](<#reply-to-an-email> "Direct link to Reply to an Email")
To reply non-interactively from Hermes, read the original message, compose a reply, and pipe it:
[code] 
    # Get the reply template, edit it, and send  
    himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send  
    
[/code]
Or build the reply manually:
[code] 
    cat << 'EOF' | himalaya template send  
    From: you@example.com  
    To: sender@example.com  
    Subject: Re: Original Subject  
    In-Reply-To: <original-message-id>  
      
    Your reply here.  
    EOF  
    
[/code]
Reply-all (interactive — needs $EDITOR, use template approach above instead):
[code] 
    himalaya message reply 42 --all  
    
[/code]
### Forward an Email[​](<#forward-an-email> "Direct link to Forward an Email")
[code] 
    # Get forward template and pipe with modifications  
    himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send  
    
[/code]
### Write a New Email[​](<#write-a-new-email> "Direct link to Write a New Email")
**Non-interactive (use this from Hermes)** — pipe the message via stdin:
[code] 
    cat << 'EOF' | himalaya template send  
    From: you@example.com  
    To: recipient@example.com  
    Subject: Test Message  
      
    Hello from Himalaya!  
    EOF  
    
[/code]
Or with headers flag:
[code] 
    himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"  
    
[/code]
Note: `himalaya message write` without piped input opens `$EDITOR`. This works with `pty=true` \+ background mode, but piping is simpler and more reliable.
### Move/Copy Emails[​](<#movecopy-emails> "Direct link to Move/Copy Emails")
Move to folder:
[code] 
    himalaya message move 42 "Archive"  
    
[/code]
Copy to folder:
[code] 
    himalaya message copy 42 "Important"  
    
[/code]
### Delete an Email[​](<#delete-an-email> "Direct link to Delete an Email")
[code] 
    himalaya message delete 42  
    
[/code]
### Manage Flags[​](<#manage-flags> "Direct link to Manage Flags")
Add flag:
[code] 
    himalaya flag add 42 --flag seen  
    
[/code]
Remove flag:
[code] 
    himalaya flag remove 42 --flag seen  
    
[/code]
## Multiple Accounts[​](<#multiple-accounts> "Direct link to Multiple Accounts")
List accounts:
[code] 
    himalaya account list  
    
[/code]
Use a specific account:
[code] 
    himalaya --account work envelope list  
    
[/code]
## Attachments[​](<#attachments> "Direct link to Attachments")
Save attachments from a message:
[code] 
    himalaya attachment download 42  
    
[/code]
Save to specific directory:
[code] 
    himalaya attachment download 42 --dir ~/Downloads  
    
[/code]
## Output Formats[​](<#output-formats> "Direct link to Output Formats")
Most commands support `--output` for structured output:
[code] 
    himalaya envelope list --output json  
    himalaya envelope list --output plain  
    
[/code]
## Debugging[​](<#debugging> "Direct link to Debugging")
Enable debug logging:
[code] 
    RUST_LOG=debug himalaya envelope list  
    
[/code]
Full trace with backtrace:
[code] 
    RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list  
    
[/code]
## Tips[​](<#tips> "Direct link to Tips")
  * Use `himalaya --help` or `himalaya <command> --help` for detailed usage.
  * Message IDs are relative to the current folder; re-list after folder changes.
  * For composing rich emails with attachments, use MML syntax (see `references/message-composition.md`).
  * Store passwords securely using `pass`, system keyring, or a command that outputs the password.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [References](<#references>)
  * [Prerequisites](<#prerequisites>)
    * [Installation](<#installation>)
  * [Configuration Setup](<#configuration-setup>)
  * [Hermes Integration Notes](<#hermes-integration-notes>)
  * [Common Operations](<#common-operations>)
    * [List Folders](<#list-folders>)
    * [List Emails](<#list-emails>)
    * [Search Emails](<#search-emails>)
    * [Read an Email](<#read-an-email>)
    * [Reply to an Email](<#reply-to-an-email>)
    * [Forward an Email](<#forward-an-email>)
    * [Write a New Email](<#write-a-new-email>)
    * [Move/Copy Emails](<#movecopy-emails>)
    * [Delete an Email](<#delete-an-email>)
    * [Manage Flags](<#manage-flags>)
  * [Multiple Accounts](<#multiple-accounts>)
  * [Attachments](<#attachments>)
  * [Output Formats](<#output-formats>)
  * [Debugging](<#debugging>)
  * [Tips](<#tips>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/email/email-himalaya -->
