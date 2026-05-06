On this page
This page covers all commands related to [Hermes profiles](</docs/user-guide/profiles>). For general CLI commands, see [CLI Commands Reference](</docs/reference/cli-commands>).
## `hermes profile`[​](<#hermes-profile> "Direct link to hermes-profile")
[code] 
    hermes profile <subcommand>  
    
[/code]
Top-level command for managing profiles. Running `hermes profile` without a subcommand shows help.
Subcommand| Description  
---|---  
`list`| List all profiles.  
`use`| Set the active (default) profile.  
`create`| Create a new profile.  
`delete`| Delete a profile.  
`show`| Show details about a profile.  
`alias`| Regenerate the shell alias for a profile.  
`rename`| Rename a profile.  
`export`| Export a profile to a tar.gz archive.  
`import`| Import a profile from a tar.gz archive.  
## `hermes profile list`[​](<#hermes-profile-list> "Direct link to hermes-profile-list")
[code] 
    hermes profile list  
    
[/code]
Lists all profiles. The currently active profile is marked with `*`.
**Example:**
[code] 
    $ hermes profile list  
      default  
    * work  
      dev  
      personal  
    
[/code]
No options.
## `hermes profile use`[​](<#hermes-profile-use> "Direct link to hermes-profile-use")
[code] 
    hermes profile use <name>  
    
[/code]
Sets `<name>` as the active profile. All subsequent `hermes` commands (without `-p`) will use this profile.
Argument| Description  
---|---  
`<name>`| Profile name to activate. Use `default` to return to the base profile.  
**Example:**
[code] 
    hermes profile use work  
    hermes profile use default  
    
[/code]
## `hermes profile create`[​](<#hermes-profile-create> "Direct link to hermes-profile-create")
[code] 
    hermes profile create <name> [options]  
    
[/code]
Creates a new profile.
Argument / Option| Description  
---|---  
`<name>`| Name for the new profile. Must be a valid directory name (alphanumeric, hyphens, underscores).  
`--clone`| Copy `config.yaml`, `.env`, and `SOUL.md` from the current profile.  
`--clone-all`| Copy everything (config, memories, skills, sessions, state) from the current profile.  
`--clone-from <profile>`| Clone from a specific profile instead of the current one. Used with `--clone` or `--clone-all`.  
`--no-alias`| Skip wrapper script creation.  
Creating a profile does **not** make that profile directory the default project/workspace directory for terminal commands. If you want a profile to start in a specific project, set `terminal.cwd` in that profile's `config.yaml`.
**Examples:**
[code] 
    # Blank profile — needs full setup  
    hermes profile create mybot  
      
    # Clone config only from current profile  
    hermes profile create work --clone  
      
    # Clone everything from current profile  
    hermes profile create backup --clone-all  
      
    # Clone config from a specific profile  
    hermes profile create work2 --clone --clone-from work  
    
[/code]
## `hermes profile delete`[​](<#hermes-profile-delete> "Direct link to hermes-profile-delete")
[code] 
    hermes profile delete <name> [options]  
    
[/code]
Deletes a profile and removes its shell alias.
Argument / Option| Description  
---|---  
`<name>`| Profile to delete.  
`--yes`, `-y`| Skip confirmation prompt.  
**Example:**
[code] 
    hermes profile delete mybot  
    hermes profile delete mybot --yes  
    
[/code]
warning
This permanently deletes the profile's entire directory including all config, memories, sessions, and skills. Cannot delete the currently active profile.
## `hermes profile show`[​](<#hermes-profile-show> "Direct link to hermes-profile-show")
[code] 
    hermes profile show <name>  
    
[/code]
Displays details about a profile including its home directory, configured model, gateway status, skills count, and configuration file status.
This shows the profile's Hermes home directory, not the terminal working directory. Terminal commands start from `terminal.cwd` (or the launch directory on the local backend when `cwd: "."`).
Argument| Description  
---|---  
`<name>`| Profile to inspect.  
**Example:**
[code] 
    $ hermes profile show work  
    Profile: work  
    Path:    ~/.hermes/profiles/work  
    Model:   anthropic/claude-sonnet-4 (anthropic)  
    Gateway: stopped  
    Skills:  12  
    .env:    exists  
    SOUL.md: exists  
    Alias:   ~/.local/bin/work  
    
[/code]
## `hermes profile alias`[​](<#hermes-profile-alias> "Direct link to hermes-profile-alias")
[code] 
    hermes profile alias <name> [options]  
    
[/code]
Regenerates the shell alias script at `~/.local/bin/<name>`. Useful if the alias was accidentally deleted or if you need to update it after moving your Hermes installation.
Argument / Option| Description  
---|---  
`<name>`| Profile to create/update the alias for.  
`--remove`| Remove the wrapper script instead of creating it.  
`--name <alias>`| Custom alias name (default: profile name).  
**Example:**
[code] 
    hermes profile alias work  
    # Creates/updates ~/.local/bin/work  
      
    hermes profile alias work --name mywork  
    # Creates ~/.local/bin/mywork  
      
    hermes profile alias work --remove  
    # Removes the wrapper script  
    
[/code]
## `hermes profile rename`[​](<#hermes-profile-rename> "Direct link to hermes-profile-rename")
[code] 
    hermes profile rename <old-name> <new-name>  
    
[/code]
Renames a profile. Updates the directory and shell alias.
Argument| Description  
---|---  
`<old-name>`| Current profile name.  
`<new-name>`| New profile name.  
**Example:**
[code] 
    hermes profile rename mybot assistant  
    # ~/.hermes/profiles/mybot → ~/.hermes/profiles/assistant  
    # ~/.local/bin/mybot → ~/.local/bin/assistant  
    
[/code]
## `hermes profile export`[​](<#hermes-profile-export> "Direct link to hermes-profile-export")
[code] 
    hermes profile export <name> [options]  
    
[/code]
Exports a profile as a compressed tar.gz archive.
Argument / Option| Description  
---|---  
`<name>`| Profile to export.  
`-o`, `--output <path>`| Output file path (default: `<name>.tar.gz`).  
**Example:**
[code] 
    hermes profile export work  
    # Creates work.tar.gz in the current directory  
      
    hermes profile export work -o ./work-2026-03-29.tar.gz  
    
[/code]
## `hermes profile import`[​](<#hermes-profile-import> "Direct link to hermes-profile-import")
[code] 
    hermes profile import <archive> [options]  
    
[/code]
Imports a profile from a tar.gz archive.
Argument / Option| Description  
---|---  
`<archive>`| Path to the tar.gz archive to import.  
`--name <name>`| Name for the imported profile (default: inferred from archive).  
**Example:**
[code] 
    hermes profile import ./work-2026-03-29.tar.gz  
    # Infers profile name from the archive  
      
    hermes profile import ./work-2026-03-29.tar.gz --name work-restored  
    
[/code]
## `hermes -p` / `hermes --profile`[​](<#hermes--p--hermes---profile> "Direct link to hermes--p--hermes---profile")
[code] 
    hermes -p <name> <command> [options]  
    hermes --profile <name> <command> [options]  
    
[/code]
Global flag to run any Hermes command under a specific profile without changing the sticky default. This overrides the active profile for the duration of the command.
Option| Description  
---|---  
`-p <name>`, `--profile <name>`| Profile to use for this command.  
**Examples:**
[code] 
    hermes -p work chat -q "Check the server status"  
    hermes --profile dev gateway start  
    hermes -p personal skills list  
    hermes -p work config edit  
    
[/code]
## `hermes completion`[​](<#hermes-completion> "Direct link to hermes-completion")
[code] 
    hermes completion <shell>  
    
[/code]
Generates shell completion scripts. Includes completions for profile names and profile subcommands.
Argument| Description  
---|---  
`<shell>`| Shell to generate completions for: `bash` or `zsh`.  
**Examples:**
[code] 
    # Install completions  
    hermes completion bash >> ~/.bashrc  
    hermes completion zsh >> ~/.zshrc  
      
    # Reload shell  
    source ~/.bashrc  
    
[/code]
After installation, tab completion works for:
  * `hermes profile <TAB>` — subcommands (list, use, create, etc.)
  * `hermes profile use <TAB>` — profile names
  * `hermes -p <TAB>` — profile names


## See also[​](<#see-also> "Direct link to See also")
  * [Profiles User Guide](</docs/user-guide/profiles>)
  * [CLI Commands Reference](</docs/reference/cli-commands>)
  * [FAQ — Profiles section](</docs/reference/faq#profiles>)


  * [`hermes profile`](<#hermes-profile>)
  * [`hermes profile list`](<#hermes-profile-list>)
  * [`hermes profile use`](<#hermes-profile-use>)
  * [`hermes profile create`](<#hermes-profile-create>)
  * [`hermes profile delete`](<#hermes-profile-delete>)
  * [`hermes profile show`](<#hermes-profile-show>)
  * [`hermes profile alias`](<#hermes-profile-alias>)
  * [`hermes profile rename`](<#hermes-profile-rename>)
  * [`hermes profile export`](<#hermes-profile-export>)
  * [`hermes profile import`](<#hermes-profile-import>)
  * [`hermes -p` / `hermes --profile`](<#hermes--p--hermes---profile>)
  * [`hermes completion`](<#hermes-completion>)
  * [See also](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/reference/profile-commands -->
