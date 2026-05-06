On this page
This guide gets you from zero to a working Hermes setup that survives real use. Install, choose a provider, verify a working chat, and know exactly what to do when something breaks.
## Prefer to watch?[​](<#prefer-to-watch> "Direct link to Prefer to watch?")
**Onchain AI Garage** put together a Masterclass walkthrough of installation, setup, and basic commands — a good companion to this page if you'd rather follow along on video. For more, see the full [Hermes Agent Tutorials & Use Cases](<https://www.youtube.com/channel/UCqB1bhMwGsW-yefBxYwFCCg>) playlist.
## Who this is for[​](<#who-this-is-for> "Direct link to Who this is for")
  * Brand new and want the shortest path to a working setup
  * Switching providers and don't want to lose time to config mistakes
  * Setting up Hermes for a team, bot, or always-on workflow
  * Tired of "it installed, but it still does nothing"


## The fastest path[​](<#the-fastest-path> "Direct link to The fastest path")
Pick the row that matches your goal:
Goal| Do this first| Then do this  
---|---|---  
I just want Hermes working on my machine| `hermes setup`| Run a real chat and verify it responds  
I already know my provider| `hermes model`| Save the config, then start chatting  
I want a bot or always-on setup| `hermes gateway setup` after CLI works| Connect Telegram, Discord, Slack, or another platform  
I want a local or self-hosted model| `hermes model` → custom endpoint| Verify the endpoint, model name, and context length  
I want multi-provider fallback| `hermes model` first| Add routing and fallback only after the base chat works  
**Rule of thumb:** if Hermes cannot complete a normal chat, do not add more features yet. Get one clean conversation working first, then layer on gateway, cron, skills, voice, or routing.
* * *
## 1\. Install Hermes Agent[​](<#1-install-hermes-agent> "Direct link to 1. Install Hermes Agent")
Run the one-line installer:
[code] 
    # Linux / macOS / WSL2 / Android (Termux)  
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash  
    
[/code]
Android / Termux
If you're installing on a phone, see the dedicated [Termux guide](</docs/getting-started/termux>) for the tested manual path, supported extras, and current Android-specific limitations.
Windows Users
Install [WSL2](<https://learn.microsoft.com/en-us/windows/wsl/install>) first, then run the command above inside your WSL2 terminal.
After it finishes, reload your shell:
[code] 
    source ~/.bashrc   # or source ~/.zshrc  
    
[/code]
For detailed installation options, prerequisites, and troubleshooting, see the [Installation guide](</docs/getting-started/installation>).
## 2\. Choose a Provider[​](<#2-choose-a-provider> "Direct link to 2. Choose a Provider")
The single most important setup step. Use `hermes model` to walk through the choice interactively:
[code] 
    hermes model  
    
[/code]
Good defaults:
Provider| What it is| How to set up  
---|---|---  
**Nous Portal**|  Subscription-based, zero-config| OAuth login via `hermes model`  
**OpenAI Codex**|  ChatGPT OAuth, uses Codex models| Device code auth via `hermes model`  
**Anthropic**|  Claude models directly — Max plan + extra usage credits (OAuth), or API key for pay-per-token| `hermes model` → OAuth login (requires Max + extra credits), or an Anthropic API key  
**OpenRouter**|  Multi-provider routing across many models| Enter your API key  
**Z.AI**|  GLM / Zhipu-hosted models| Set `GLM_API_KEY` / `ZAI_API_KEY`  
**Kimi / Moonshot**|  Moonshot-hosted coding and chat models| Set `KIMI_API_KEY`  
**Kimi / Moonshot China**|  China-region Moonshot endpoint| Set `KIMI_CN_API_KEY`  
**Arcee AI**|  Trinity models| Set `ARCEEAI_API_KEY`  
**GMI Cloud**|  Multi-model direct API| Set `GMI_API_KEY`  
**MiniMax (OAuth)**|  MiniMax-M2.7 via browser OAuth — no API key needed| `hermes model` → MiniMax (OAuth)  
**MiniMax**|  International MiniMax endpoint| Set `MINIMAX_API_KEY`  
**MiniMax China**|  China-region MiniMax endpoint| Set `MINIMAX_CN_API_KEY`  
**Alibaba Cloud**|  Qwen models via DashScope| Set `DASHSCOPE_API_KEY`  
**Hugging Face**|  20+ open models via unified router (Qwen, DeepSeek, Kimi, etc.)| Set `HF_TOKEN`  
**AWS Bedrock**|  Claude, Nova, Llama, DeepSeek via native Converse API| IAM role or `aws configure` ([guide](</docs/guides/aws-bedrock>))  
**Kilo Code**|  KiloCode-hosted models| Set `KILOCODE_API_KEY`  
**OpenCode Zen**|  Pay-as-you-go access to curated models| Set `OPENCODE_ZEN_API_KEY`  
**OpenCode Go**|  $10/month subscription for open models| Set `OPENCODE_GO_API_KEY`  
**DeepSeek**|  Direct DeepSeek API access| Set `DEEPSEEK_API_KEY`  
**NVIDIA NIM**|  Nemotron models via build.nvidia.com or local NIM| Set `NVIDIA_API_KEY` (optional: `NVIDIA_BASE_URL`)  
**GitHub Copilot**|  GitHub Copilot subscription (GPT-5.x, Claude, Gemini, etc.)| OAuth via `hermes model`, or `COPILOT_GITHUB_TOKEN` / `GH_TOKEN`  
**GitHub Copilot ACP**|  Copilot ACP agent backend (spawns local `copilot` CLI)| `hermes model` (requires `copilot` CLI + `copilot login`)  
**Vercel AI Gateway**|  Vercel AI Gateway routing| Set `AI_GATEWAY_API_KEY`  
**Custom Endpoint**|  VLLM, SGLang, Ollama, or any OpenAI-compatible API| Set base URL + API key  
For most first-time users: choose a provider, accept the defaults unless you know why you're changing them. The full provider catalog with env vars and setup steps lives on the [Providers](</docs/integrations/providers>) page.
Minimum context: 64K tokens
Hermes Agent requires a model with at least **64,000 tokens** of context. Models with smaller windows cannot maintain enough working memory for multi-step tool-calling workflows and will be rejected at startup. Most hosted models (Claude, GPT, Gemini, Qwen, DeepSeek) meet this easily. If you're running a local model, set its context size to at least 64K (e.g. `--ctx-size 65536` for llama.cpp or `-c 65536` for Ollama).
tip
You can switch providers at any time with `hermes model` — no lock-in. For a full list of all supported providers and setup details, see [AI Providers](</docs/integrations/providers>).
### How settings are stored[​](<#how-settings-are-stored> "Direct link to How settings are stored")
Hermes separates secrets from normal config:
  * **Secrets and tokens** → `~/.hermes/.env`
  * **Non-secret settings** → `~/.hermes/config.yaml`


The easiest way to set values correctly is through the CLI:
[code] 
    hermes config set model anthropic/claude-opus-4.6  
    hermes config set terminal.backend docker  
    hermes config set OPENROUTER_API_KEY sk-or-...  
    
[/code]
The right value goes to the right file automatically.
## 3\. Run Your First Chat[​](<#3-run-your-first-chat> "Direct link to 3. Run Your First Chat")
[code] 
    hermes            # classic CLI  
    hermes --tui      # modern TUI (recommended)  
    
[/code]
You'll see a welcome banner with your model, available tools, and skills. Use a prompt that's specific and easy to verify:
Pick your interface
Hermes ships with two terminal interfaces: the classic `prompt_toolkit` CLI and a newer [TUI](</docs/user-guide/tui>) with modal overlays, mouse selection, and non-blocking input. Both share the same sessions, slash commands, and config — try each with `hermes` vs `hermes --tui`.
[code] 
    Summarize this repo in 5 bullets and tell me what the main entrypoint is.  
    
[/code]
[code] 
    Check my current directory and tell me what looks like the main project file.  
    
[/code]
[code] 
    Help me set up a clean GitHub PR workflow for this codebase.  
    
[/code]
**What success looks like:**
  * The banner shows your chosen model/provider
  * Hermes replies without error
  * It can use a tool if needed (terminal, file read, web search)
  * The conversation continues normally for more than one turn


If that works, you're past the hardest part.
## 4\. Verify Sessions Work[​](<#4-verify-sessions-work> "Direct link to 4. Verify Sessions Work")
Before moving on, make sure resume works:
[code] 
    hermes --continue    # Resume the most recent session  
    hermes -c            # Short form  
    
[/code]
That should bring you back to the session you just had. If it doesn't, check whether you're in the same profile and whether the session actually saved. This matters later when you're juggling multiple setups or machines.
## 5\. Try Key Features[​](<#5-try-key-features> "Direct link to 5. Try Key Features")
### Use the terminal[​](<#use-the-terminal> "Direct link to Use the terminal")
[code] 
    ❯ What's my disk usage? Show the top 5 largest directories.  
    
[/code]
The agent runs terminal commands on your behalf and shows results.
### Slash commands[​](<#slash-commands> "Direct link to Slash commands")
Type `/` to see an autocomplete dropdown of all commands:
Command| What it does  
---|---  
`/help`| Show all available commands  
`/tools`| List available tools  
`/model`| Switch models interactively  
`/personality pirate`| Try a fun personality  
`/save`| Save the conversation  
### Multi-line input[​](<#multi-line-input> "Direct link to Multi-line input")
Press `Alt+Enter` or `Ctrl+J` to add a new line. Great for pasting code or writing detailed prompts.
### Interrupt the agent[​](<#interrupt-the-agent> "Direct link to Interrupt the agent")
If the agent is taking too long, type a new message and press Enter — it interrupts the current task and switches to your new instructions. `Ctrl+C` also works.
## 6\. Add the Next Layer[​](<#6-add-the-next-layer> "Direct link to 6. Add the Next Layer")
Only after the base chat works. Pick what you need:
### Bot or shared assistant[​](<#bot-or-shared-assistant> "Direct link to Bot or shared assistant")
[code] 
    hermes gateway setup    # Interactive platform configuration  
    
[/code]
Connect [Telegram](</docs/user-guide/messaging/telegram>), [Discord](</docs/user-guide/messaging/discord>), [Slack](</docs/user-guide/messaging/slack>), [WhatsApp](</docs/user-guide/messaging/whatsapp>), [Signal](</docs/user-guide/messaging/signal>), [Email](</docs/user-guide/messaging/email>), or [Home Assistant](</docs/user-guide/messaging/homeassistant>), or [Microsoft Teams](</docs/user-guide/messaging/teams>).
### Automation and tools[​](<#automation-and-tools> "Direct link to Automation and tools")
  * `hermes tools` — tune tool access per platform
  * `hermes skills` — browse and install reusable workflows
  * Cron — only after your bot or CLI setup is stable


### Sandboxed terminal[​](<#sandboxed-terminal> "Direct link to Sandboxed terminal")
For safety, run the agent in a Docker container or on a remote server:
[code] 
    hermes config set terminal.backend docker    # Docker isolation  
    hermes config set terminal.backend ssh       # Remote server  
    
[/code]
### Voice mode[​](<#voice-mode> "Direct link to Voice mode")
[code] 
    pip install "hermes-agent[voice]"  
    # Includes faster-whisper for free local speech-to-text  
    
[/code]
Then in the CLI: `/voice on`. Press `Ctrl+B` to record. See [Voice Mode](</docs/user-guide/features/voice-mode>).
### Skills[​](<#skills> "Direct link to Skills")
[code] 
    hermes skills search kubernetes  
    hermes skills install openai/skills/k8s  
    
[/code]
Or use `/skills` inside a chat session.
### MCP servers[​](<#mcp-servers> "Direct link to MCP servers")
[code] 
    # Add to ~/.hermes/config.yaml  
    mcp_servers:  
      github:  
        command: npx  
        args: ["-y", "@modelcontextprotocol/server-github"]  
        env:  
          GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"  
    
[/code]
### Editor integration (ACP)[​](<#editor-integration-acp> "Direct link to Editor integration \(ACP\)")
[code] 
    pip install -e '.[acp]'  
    hermes acp  
    
[/code]
See [ACP Editor Integration](</docs/user-guide/features/acp>).
* * *
## Common Failure Modes[​](<#common-failure-modes> "Direct link to Common Failure Modes")
These are the problems that waste the most time:
Symptom| Likely cause| Fix  
---|---|---  
Hermes opens but gives empty or broken replies| Provider auth or model selection is wrong| Run `hermes model` again and confirm provider, model, and auth  
Custom endpoint "works" but returns garbage| Wrong base URL, model name, or not actually OpenAI-compatible| Verify the endpoint in a separate client first  
Gateway starts but nobody can message it| Bot token, allowlist, or platform setup is incomplete| Re-run `hermes gateway setup` and check `hermes gateway status`  
`hermes --continue` can't find old session| Switched profiles or session never saved| Check `hermes sessions list` and confirm you're in the right profile  
Model unavailable or odd fallback behavior| Provider routing or fallback settings are too aggressive| Keep routing off until the base provider is stable  
`hermes doctor` flags config problems| Config values are missing or stale| Fix the config, retest a plain chat before adding features  
## Recovery Toolkit[​](<#recovery-toolkit> "Direct link to Recovery Toolkit")
When something feels off, use this order:
  1. `hermes doctor`
  2. `hermes model`
  3. `hermes setup`
  4. `hermes sessions list`
  5. `hermes --continue`
  6. `hermes gateway status`


That sequence gets you from "broken vibes" back to a known state fast.
* * *
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
Command| Description  
---|---  
`hermes`| Start chatting  
`hermes model`| Choose your LLM provider and model  
`hermes tools`| Configure which tools are enabled per platform  
`hermes setup`| Full setup wizard (configures everything at once)  
`hermes doctor`| Diagnose issues  
`hermes update`| Update to latest version  
`hermes gateway`| Start the messaging gateway  
`hermes --continue`| Resume last session  
## Next Steps[​](<#next-steps> "Direct link to Next Steps")
  * **[CLI Guide](</docs/user-guide/cli>)** — Master the terminal interface
  * **[Configuration](</docs/user-guide/configuration>)** — Customize your setup
  * **[Messaging Gateway](</docs/user-guide/messaging/>)** — Connect Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, Teams, and more
  * **[Tools& Toolsets](</docs/user-guide/features/tools>)** — Explore available capabilities
  * **[AI Providers](</docs/integrations/providers>)** — Full provider list and setup details
  * **[Skills System](</docs/user-guide/features/skills>)** — Reusable workflows and knowledge
  * **[Tips& Best Practices](</docs/guides/tips>)** — Power user tips


  * [Prefer to watch?](<#prefer-to-watch>)
  * [Who this is for](<#who-this-is-for>)
  * [The fastest path](<#the-fastest-path>)
  * [1\. Install Hermes Agent](<#1-install-hermes-agent>)
  * [2\. Choose a Provider](<#2-choose-a-provider>)
    * [How settings are stored](<#how-settings-are-stored>)
  * [3\. Run Your First Chat](<#3-run-your-first-chat>)
  * [4\. Verify Sessions Work](<#4-verify-sessions-work>)
  * [5\. Try Key Features](<#5-try-key-features>)
    * [Use the terminal](<#use-the-terminal>)
    * [Slash commands](<#slash-commands>)
    * [Multi-line input](<#multi-line-input>)
    * [Interrupt the agent](<#interrupt-the-agent>)
  * [6\. Add the Next Layer](<#6-add-the-next-layer>)
    * [Bot or shared assistant](<#bot-or-shared-assistant>)
    * [Automation and tools](<#automation-and-tools>)
    * [Sandboxed terminal](<#sandboxed-terminal>)
    * [Voice mode](<#voice-mode>)
    * [Skills](<#skills>)
    * [MCP servers](<#mcp-servers>)
    * [Editor integration (ACP)](<#editor-integration-acp>)
  * [Common Failure Modes](<#common-failure-modes>)
  * [Recovery Toolkit](<#recovery-toolkit>)
  * [Quick Reference](<#quick-reference>)
  * [Next Steps](<#next-steps>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart -->
