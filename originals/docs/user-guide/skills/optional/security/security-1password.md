On this page
Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in, and reading/injecting secrets for commands.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/security/1password`  
Path| `optional-skills/security/1password`  
Version| `1.0.0`  
Author| arceus77-7, enhanced by Hermes Agent  
License| MIT  
Tags| `security`, `secrets`, `1password`, `op`, `cli`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# 1Password CLI
Use this skill when the user wants secrets managed through 1Password instead of plaintext env vars or files.
## Requirements[​](<#requirements> "Direct link to Requirements")
  * 1Password account
  * 1Password CLI (`op`) installed
  * One of: desktop app integration, service account token (`OP_SERVICE_ACCOUNT_TOKEN`), or Connect server
  * `tmux` available for stable authenticated sessions during Hermes terminal calls (desktop app flow only)


## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Install or configure 1Password CLI
  * Sign in with `op signin`
  * Read secret references like `op://Vault/Item/field`
  * Inject secrets into config/templates using `op inject`
  * Run commands with secret env vars via `op run`


## Authentication Methods[​](<#authentication-methods> "Direct link to Authentication Methods")
### Service Account (recommended for Hermes)[​](<#service-account-recommended-for-hermes> "Direct link to Service Account \(recommended for Hermes\)")
Set `OP_SERVICE_ACCOUNT_TOKEN` in `~/.hermes/.env` (the skill will prompt for this on first load). No desktop app needed. Supports `op read`, `op inject`, `op run`.
[code] 
    export OP_SERVICE_ACCOUNT_TOKEN="your-token-here"  
    op whoami  # verify — should show Type: SERVICE_ACCOUNT  
    
[/code]
### Desktop App Integration (interactive)[​](<#desktop-app-integration-interactive> "Direct link to Desktop App Integration \(interactive\)")
  1. Enable in 1Password desktop app: Settings → Developer → Integrate with 1Password CLI
  2. Ensure app is unlocked
  3. Run `op signin` and approve the biometric prompt


### Connect Server (self-hosted)[​](<#connect-server-self-hosted> "Direct link to Connect Server \(self-hosted\)")
[code] 
    export OP_CONNECT_HOST="http://localhost:8080"  
    export OP_CONNECT_TOKEN="your-connect-token"  
    
[/code]
## Setup[​](<#setup> "Direct link to Setup")
  1. Install CLI:


[code] 
    # macOS  
    brew install 1password-cli  
      
    # Linux (official package/install docs)  
    # See references/get-started.md for distro-specific links.  
      
    # Windows (winget)  
    winget install AgileBits.1Password.CLI  
    
[/code]
  2. Verify:


[code] 
    op --version  
    
[/code]
  3. Choose an auth method above and configure it.


## Hermes Execution Pattern (desktop app flow)[​](<#hermes-execution-pattern-desktop-app-flow> "Direct link to Hermes Execution Pattern \(desktop app flow\)")
Hermes terminal commands are non-interactive by default and can lose auth context between calls. For reliable `op` use with desktop app integration, run sign-in and secret operations inside a dedicated tmux session.
Note: This is NOT needed when using `OP_SERVICE_ACCOUNT_TOKEN` — the token persists across terminal calls automatically.
[code] 
    SOCKET_DIR="${TMPDIR:-/tmp}/hermes-tmux-sockets"  
    mkdir -p "$SOCKET_DIR"  
    SOCKET="$SOCKET_DIR/hermes-op.sock"  
    SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"  
      
    tmux -S "$SOCKET" new -d -s "$SESSION" -n shell  
      
    # Sign in (approve in desktop app when prompted)  
    tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "eval \"\$(op signin --account my.1password.com)\"" Enter  
      
    # Verify auth  
    tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter  
      
    # Example read  
    tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op read 'op://Private/Npmjs/one-time password?attribute=otp'" Enter  
      
    # Capture output when needed  
    tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200  
      
    # Cleanup  
    tmux -S "$SOCKET" kill-session -t "$SESSION"  
    
[/code]
## Common Operations[​](<#common-operations> "Direct link to Common Operations")
### Read a secret[​](<#read-a-secret> "Direct link to Read a secret")
[code] 
    op read "op://app-prod/db/password"  
    
[/code]
### Get OTP[​](<#get-otp> "Direct link to Get OTP")
[code] 
    op read "op://app-prod/npm/one-time password?attribute=otp"  
    
[/code]
### Inject into template[​](<#inject-into-template> "Direct link to Inject into template")
[code] 
    echo "db_password: {{ op://app-prod/db/password }}" | op inject  
    
[/code]
### Run a command with secret env var[​](<#run-a-command-with-secret-env-var> "Direct link to Run a command with secret env var")
[code] 
    export DB_PASSWORD="op://app-prod/db/password"  
    op run -- sh -c '[ -n "$DB_PASSWORD" ] && echo "DB_PASSWORD is set" || echo "DB_PASSWORD missing"'  
    
[/code]
## Guardrails[​](<#guardrails> "Direct link to Guardrails")
  * Never print raw secrets back to user unless they explicitly request the value.
  * Prefer `op run` / `op inject` instead of writing secrets into files.
  * If command fails with "account is not signed in", run `op signin` again in the same tmux session.
  * If desktop app integration is unavailable (headless/CI), use service account token flow.


## CI / Headless note[​](<#ci--headless-note> "Direct link to CI / Headless note")
For non-interactive use, authenticate with `OP_SERVICE_ACCOUNT_TOKEN` and avoid interactive `op signin`. Service accounts require CLI v2.18.0+.
## References[​](<#references> "Direct link to References")
  * `references/get-started.md`
  * `references/cli-examples.md`
  * <https://developer.1password.com/docs/cli/>
  * <https://developer.1password.com/docs/service-accounts/>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Requirements](<#requirements>)
  * [When to Use](<#when-to-use>)
  * [Authentication Methods](<#authentication-methods>)
    * [Service Account (recommended for Hermes)](<#service-account-recommended-for-hermes>)
    * [Desktop App Integration (interactive)](<#desktop-app-integration-interactive>)
    * [Connect Server (self-hosted)](<#connect-server-self-hosted>)
  * [Setup](<#setup>)
  * [Hermes Execution Pattern (desktop app flow)](<#hermes-execution-pattern-desktop-app-flow>)
  * [Common Operations](<#common-operations>)
    * [Read a secret](<#read-a-secret>)
    * [Get OTP](<#get-otp>)
    * [Inject into template](<#inject-into-template>)
    * [Run a command with secret env var](<#run-a-command-with-secret-env-var>)
  * [Guardrails](<#guardrails>)
  * [CI / Headless note](<#ci--headless-note>)
  * [References](<#references>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/security/security-1password -->
