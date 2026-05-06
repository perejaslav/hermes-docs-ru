On this page
Thank you for contributing to Hermes Agent! This guide covers setting up your dev environment, understanding the codebase, and getting your PR merged.
## Contribution Priorities[​](<#contribution-priorities> "Direct link to Contribution Priorities")
We value contributions in this order:
  1. **Bug fixes** — crashes, incorrect behavior, data loss
  2. **Cross-platform compatibility** — macOS, different Linux distros, WSL2
  3. **Security hardening** — shell injection, prompt injection, path traversal
  4. **Performance and robustness** — retry logic, error handling, graceful degradation
  5. **New skills** — broadly useful ones (see [Creating Skills](</docs/developer-guide/creating-skills>))
  6. **New tools** — rarely needed; most capabilities should be skills
  7. **Documentation** — fixes, clarifications, new examples


## Common contribution paths[​](<#common-contribution-paths> "Direct link to Common contribution paths")
  * Building a custom/local tool without modifying Hermes core? Start with [Build a Hermes Plugin](</docs/guides/build-a-hermes-plugin>)
  * Building a new built-in core tool for Hermes itself? Start with [Adding Tools](</docs/developer-guide/adding-tools>)
  * Building a new skill? Start with [Creating Skills](</docs/developer-guide/creating-skills>)
  * Building a new inference provider? Start with [Adding Providers](</docs/developer-guide/adding-providers>)


## Development Setup[​](<#development-setup> "Direct link to Development Setup")
### Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
Requirement| Notes  
---|---  
**Git**|  With `--recurse-submodules` support, and the `git-lfs` extension installed  
**Python 3.11+**|  uv will install it if missing  
**uv**|  Fast Python package manager ([install](<https://docs.astral.sh/uv/>))  
**Node.js 20+**|  Optional — needed for browser tools and WhatsApp bridge (matches root `package.json` engines)  
### Clone and Install[​](<#clone-and-install> "Direct link to Clone and Install")
[code] 
    git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git  
    cd hermes-agent  
      
    # Create venv with Python 3.11  
    uv venv venv --python 3.11  
    export VIRTUAL_ENV="$(pwd)/venv"  
      
    # Install with all extras (messaging, cron, CLI menus, dev tools)  
    uv pip install -e ".[all,dev]"  
    uv pip install -e "./tinker-atropos"  
      
    # Optional: browser tools  
    npm install  
    
[/code]
### Configure for Development[​](<#configure-for-development> "Direct link to Configure for Development")
[code] 
    mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}  
    cp cli-config.yaml.example ~/.hermes/config.yaml  
    touch ~/.hermes/.env  
      
    # Add at minimum an LLM provider key:  
    echo 'OPENROUTER_API_KEY=sk-or-v1-your-key' >> ~/.hermes/.env  
    
[/code]
### Run[​](<#run> "Direct link to Run")
[code] 
    # Symlink for global access  
    mkdir -p ~/.local/bin  
    ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes  
      
    # Verify  
    hermes doctor  
    hermes chat -q "Hello"  
    
[/code]
### Run Tests[​](<#run-tests> "Direct link to Run Tests")
[code] 
    pytest tests/ -v  
    
[/code]
## Code Style[​](<#code-style> "Direct link to Code Style")
  * **PEP 8** with practical exceptions (no strict line length enforcement)
  * **Comments** : Only when explaining non-obvious intent, trade-offs, or API quirks
  * **Error handling** : Catch specific exceptions. Use `logger.warning()`/`logger.error()` with `exc_info=True` for unexpected errors
  * **Cross-platform** : Never assume Unix (see below)
  * **Profile-safe paths** : Never hardcode `~/.hermes` — use `get_hermes_home()` from `hermes_constants` for code paths and `display_hermes_home()` for user-facing messages. See [AGENTS.md](<https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md#profiles-multi-instance-support>) for full rules.


## Cross-Platform Compatibility[​](<#cross-platform-compatibility> "Direct link to Cross-Platform Compatibility")
Hermes officially supports Linux, macOS, and WSL2. Native Windows is **not supported** , but the codebase includes some defensive coding patterns to avoid hard crashes in edge cases. Key rules:
### 1\. `termios` and `fcntl` are Unix-only[​](<#1-termios-and-fcntl-are-unix-only> "Direct link to 1-termios-and-fcntl-are-unix-only")
Always catch both `ImportError` and `NotImplementedError`:
[code] 
    try:  
        from simple_term_menu import TerminalMenu  
        menu = TerminalMenu(options)  
        idx = menu.show()  
    except (ImportError, NotImplementedError):  
        # Fallback: numbered menu  
        for i, opt in enumerate(options):  
            print(f"  {i+1}. {opt}")  
        idx = int(input("Choice: ")) - 1  
    
[/code]
### 2\. File encoding[​](<#2-file-encoding> "Direct link to 2. File encoding")
Some environments may save `.env` files in non-UTF-8 encodings:
[code] 
    try:  
        load_dotenv(env_path)  
    except UnicodeDecodeError:  
        load_dotenv(env_path, encoding="latin-1")  
    
[/code]
### 3\. Process management[​](<#3-process-management> "Direct link to 3. Process management")
`os.setsid()`, `os.killpg()`, and signal handling differ across platforms:
[code] 
    import platform  
    if platform.system() != "Windows":  
        kwargs["preexec_fn"] = os.setsid  
    
[/code]
### 4\. Path separators[​](<#4-path-separators> "Direct link to 4. Path separators")
Use `pathlib.Path` instead of string concatenation with `/`.
## Security Considerations[​](<#security-considerations> "Direct link to Security Considerations")
Hermes has terminal access. Security matters.
### Existing Protections[​](<#existing-protections> "Direct link to Existing Protections")
Layer| Implementation  
---|---  
**Sudo password piping**|  Uses `shlex.quote()` to prevent shell injection  
**Dangerous command detection**|  Regex patterns in `tools/approval.py` with user approval flow  
**Cron prompt injection**|  Scanner blocks instruction-override patterns  
**Write deny list**|  Protected paths resolved via `os.path.realpath()` to prevent symlink bypass  
**Skills guard**|  Security scanner for hub-installed skills  
**Code execution sandbox**|  Child process runs with API keys stripped  
**Container hardening**|  Docker: all capabilities dropped, no privilege escalation, PID limits  
### Contributing Security-Sensitive Code[​](<#contributing-security-sensitive-code> "Direct link to Contributing Security-Sensitive Code")
  * Always use `shlex.quote()` when interpolating user input into shell commands
  * Resolve symlinks with `os.path.realpath()` before access control checks
  * Don't log secrets
  * Catch broad exceptions around tool execution
  * Test on all platforms if your change touches file paths or processes


## Pull Request Process[​](<#pull-request-process> "Direct link to Pull Request Process")
### Branch Naming[​](<#branch-naming> "Direct link to Branch Naming")
[code] 
    fix/description        # Bug fixes  
    feat/description       # New features  
    docs/description       # Documentation  
    test/description       # Tests  
    refactor/description   # Code restructuring  
    
[/code]
### Before Submitting[​](<#before-submitting> "Direct link to Before Submitting")
  1. **Run tests** : `pytest tests/ -v`
  2. **Test manually** : Run `hermes` and exercise the code path you changed
  3. **Check cross-platform impact** : Consider macOS and different Linux distros
  4. **Keep PRs focused** : One logical change per PR


### PR Description[​](<#pr-description> "Direct link to PR Description")
Include:
  * **What** changed and **why**
  * **How to test** it
  * **What platforms** you tested on
  * Reference any related issues


### Commit Messages[​](<#commit-messages> "Direct link to Commit Messages")
We use [Conventional Commits](<https://www.conventionalcommits.org/>):
[code] 
    <type>(<scope>): <description>  
    
[/code]
Type| Use for  
---|---  
`fix`| Bug fixes  
`feat`| New features  
`docs`| Documentation  
`test`| Tests  
`refactor`| Code restructuring  
`chore`| Build, CI, dependency updates  
Scopes: `cli`, `gateway`, `tools`, `skills`, `agent`, `install`, `whatsapp`, `security`
Examples:
[code] 
    fix(cli): prevent crash in save_config_value when model is a string  
    feat(gateway): add WhatsApp multi-user session isolation  
    fix(security): prevent shell injection in sudo password piping  
    
[/code]
## Reporting Issues[​](<#reporting-issues> "Direct link to Reporting Issues")
  * Use [GitHub Issues](<https://github.com/NousResearch/hermes-agent/issues>)
  * Include: OS, Python version, Hermes version (`hermes version`), full error traceback
  * Include steps to reproduce
  * Check existing issues before creating duplicates
  * For security vulnerabilities, please report privately


## Community[​](<#community> "Direct link to Community")
  * **Discord** : [discord.gg/NousResearch](<https://discord.gg/NousResearch>)
  * **GitHub Discussions** : For design proposals and architecture discussions
  * **Skills Hub** : Upload specialized skills and share with the community


## License[​](<#license> "Direct link to License")
By contributing, you agree that your contributions will be licensed under the [MIT License](<https://github.com/NousResearch/hermes-agent/blob/main/LICENSE>).
  * [Contribution Priorities](<#contribution-priorities>)
  * [Common contribution paths](<#common-contribution-paths>)
  * [Development Setup](<#development-setup>)
    * [Prerequisites](<#prerequisites>)
    * [Clone and Install](<#clone-and-install>)
    * [Configure for Development](<#configure-for-development>)
    * [Run](<#run>)
    * [Run Tests](<#run-tests>)
  * [Code Style](<#code-style>)
  * [Cross-Platform Compatibility](<#cross-platform-compatibility>)
    * [1\. `termios` and `fcntl` are Unix-only](<#1-termios-and-fcntl-are-unix-only>)
    * [2\. File encoding](<#2-file-encoding>)
    * [3\. Process management](<#3-process-management>)
    * [4\. Path separators](<#4-path-separators>)
  * [Security Considerations](<#security-considerations>)
    * [Existing Protections](<#existing-protections>)
    * [Contributing Security-Sensitive Code](<#contributing-security-sensitive-code>)
  * [Pull Request Process](<#pull-request-process>)
    * [Branch Naming](<#branch-naming>)
    * [Before Submitting](<#before-submitting>)
    * [PR Description](<#pr-description>)
    * [Commit Messages](<#commit-messages>)
  * [Reporting Issues](<#reporting-issues>)
  * [Community](<#community>)
  * [License](<#license>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/contributing -->
