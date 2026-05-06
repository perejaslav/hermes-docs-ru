On this page
This is the tested path for running Hermes Agent directly on an Android phone through [Termux](<https://termux.dev/>).
It gives you a working local CLI on the phone, plus the core extras that are currently known to install cleanly on Android.
## What is supported in the tested path?[​](<#what-is-supported-in-the-tested-path> "Direct link to What is supported in the tested path?")
The tested Termux bundle installs:
  * the Hermes CLI
  * cron support
  * PTY/background terminal support
  * Telegram gateway support (manual / best-effort background runs)
  * MCP support
  * Honcho memory support
  * ACP support


Concretely, it maps to:
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
## What is not part of the tested path yet?[​](<#what-is-not-part-of-the-tested-path-yet> "Direct link to What is not part of the tested path yet?")
A few features still need desktop/server-style dependencies that are not published for Android, or have not been validated on phones yet:
  * `.[all]` is not supported on Android today
  * the `voice` extra is blocked by `faster-whisper -> ctranslate2`, and `ctranslate2` does not publish Android wheels
  * automatic browser / Playwright bootstrap is skipped in the Termux installer
  * Docker-based terminal isolation is not available inside Termux
  * Android may still suspend Termux background jobs, so gateway persistence is best-effort rather than a normal managed service


That does not stop Hermes from working well as a phone-native CLI agent — it just means the recommended mobile install is intentionally narrower than the desktop/server install.
* * *
## Option 1: One-line installer[​](<#option-1-one-line-installer> "Direct link to Option 1: One-line installer")
Hermes now ships a Termux-aware installer path:
[code] 
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash  
    
[/code]
On Termux, the installer automatically:
  * uses `pkg` for system packages
  * creates the venv with `python -m venv`
  * installs `.[termux]` with `pip`
  * links `hermes` into `$PREFIX/bin` so it stays on your Termux PATH
  * skips the untested browser / WhatsApp bootstrap


If you want the explicit commands or need to debug a failed install, use the manual path below.
* * *
## Option 2: Manual install (fully explicit)[​](<#option-2-manual-install-fully-explicit> "Direct link to Option 2: Manual install \(fully explicit\)")
### 1\. Update Termux and install system packages[​](<#1-update-termux-and-install-system-packages> "Direct link to 1. Update Termux and install system packages")
[code] 
    pkg update  
    pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg  
    
[/code]
Why these packages?
  * `python` — runtime + venv support
  * `git` — clone/update the repo
  * `clang`, `rust`, `make`, `pkg-config`, `libffi`, `openssl` — needed to build a few Python dependencies on Android
  * `nodejs` — optional Node runtime for experiments beyond the tested core path
  * `ripgrep` — fast file search
  * `ffmpeg` — media / TTS conversions


### 2\. Clone Hermes[​](<#2-clone-hermes> "Direct link to 2. Clone Hermes")
[code] 
    git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git  
    cd hermes-agent  
    
[/code]
If you already cloned without submodules:
[code] 
    git submodule update --init --recursive  
    
[/code]
### 3\. Create a virtual environment[​](<#3-create-a-virtual-environment> "Direct link to 3. Create a virtual environment")
[code] 
    python -m venv venv  
    source venv/bin/activate  
    export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"  
    python -m pip install --upgrade pip setuptools wheel  
    
[/code]
`ANDROID_API_LEVEL` is important for Rust / maturin-based packages such as `jiter`.
### 4\. Install the tested Termux bundle[​](<#4-install-the-tested-termux-bundle> "Direct link to 4. Install the tested Termux bundle")
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
If you only want the minimal core agent, this also works:
[code] 
    python -m pip install -e '.' -c constraints-termux.txt  
    
[/code]
### 5\. Put `hermes` on your Termux PATH[​](<#5-put-hermes-on-your-termux-path> "Direct link to 5-put-hermes-on-your-termux-path")
[code] 
    ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"  
    
[/code]
`$PREFIX/bin` is already on PATH in Termux, so this makes the `hermes` command persist across new shells without re-activating the venv every time.
### 6\. Verify the install[​](<#6-verify-the-install> "Direct link to 6. Verify the install")
[code] 
    hermes version  
    hermes doctor  
    
[/code]
### 7\. Start Hermes[​](<#7-start-hermes> "Direct link to 7. Start Hermes")
[code] 
    hermes  
    
[/code]
* * *
## Recommended follow-up setup[​](<#recommended-follow-up-setup> "Direct link to Recommended follow-up setup")
### Configure a model[​](<#configure-a-model> "Direct link to Configure a model")
[code] 
    hermes model  
    
[/code]
Or set keys directly in `~/.hermes/.env`.
### Re-run the full interactive setup wizard later[​](<#re-run-the-full-interactive-setup-wizard-later> "Direct link to Re-run the full interactive setup wizard later")
[code] 
    hermes setup  
    
[/code]
### Install optional Node dependencies manually[​](<#install-optional-node-dependencies-manually> "Direct link to Install optional Node dependencies manually")
The tested Termux path skips Node/browser bootstrap on purpose. If you want to experiment with browser tooling later:
[code] 
    pkg install nodejs-lts  
    npm install  
    
[/code]
The browser tool automatically includes Termux directories (`/data/data/com.termux/files/usr/bin`) in its PATH search, so `agent-browser` and `npx` are discovered without any extra PATH configuration.
Treat browser / WhatsApp tooling on Android as experimental until documented otherwise.
* * *
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### `No solution found` when installing `.[all]`[​](<#no-solution-found-when-installing-all> "Direct link to no-solution-found-when-installing-all")
Use the tested Termux bundle instead:
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
The blocker is currently the `voice` extra:
  * `voice` pulls `faster-whisper`
  * `faster-whisper` depends on `ctranslate2`
  * `ctranslate2` does not publish Android wheels


### `uv pip install` fails on Android[​](<#uv-pip-install-fails-on-android> "Direct link to uv-pip-install-fails-on-android")
Use the Termux path with the stdlib venv + `pip` instead:
[code] 
    python -m venv venv  
    source venv/bin/activate  
    export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"  
    python -m pip install --upgrade pip setuptools wheel  
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
### `jiter` / `maturin` complains about `ANDROID_API_LEVEL`[​](<#jiter--maturin-complains-about-android_api_level> "Direct link to jiter--maturin-complains-about-android_api_level")
Set the API level explicitly before installing:
[code] 
    export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"  
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
### `hermes doctor` says ripgrep or Node is missing[​](<#hermes-doctor-says-ripgrep-or-node-is-missing> "Direct link to hermes-doctor-says-ripgrep-or-node-is-missing")
Install them with Termux packages:
[code] 
    pkg install ripgrep nodejs  
    
[/code]
### Build failures while installing Python packages[​](<#build-failures-while-installing-python-packages> "Direct link to Build failures while installing Python packages")
Make sure the build toolchain is installed:
[code] 
    pkg install clang rust make pkg-config libffi openssl  
    
[/code]
Then retry:
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
* * *
## Known limitations on phones[​](<#known-limitations-on-phones> "Direct link to Known limitations on phones")
  * Docker backend is unavailable
  * local voice transcription via `faster-whisper` is unavailable in the tested path
  * browser automation setup is intentionally skipped by the installer
  * some optional extras may work, but only `.[termux]` is currently documented as the tested Android bundle


If you hit a new Android-specific issue, please open a GitHub issue with:
  * your Android version
  * `termux-info`
  * `python --version`
  * `hermes doctor`
  * the exact install command and full error output


  * [What is supported in the tested path?](<#what-is-supported-in-the-tested-path>)
  * [What is not part of the tested path yet?](<#what-is-not-part-of-the-tested-path-yet>)
  * [Option 1: One-line installer](<#option-1-one-line-installer>)
  * [Option 2: Manual install (fully explicit)](<#option-2-manual-install-fully-explicit>)
    * [1\. Update Termux and install system packages](<#1-update-termux-and-install-system-packages>)
    * [2\. Clone Hermes](<#2-clone-hermes>)
    * [3\. Create a virtual environment](<#3-create-a-virtual-environment>)
    * [4\. Install the tested Termux bundle](<#4-install-the-tested-termux-bundle>)
    * [5\. Put `hermes` on your Termux PATH](<#5-put-hermes-on-your-termux-path>)
    * [6\. Verify the install](<#6-verify-the-install>)
    * [7\. Start Hermes](<#7-start-hermes>)
  * [Recommended follow-up setup](<#recommended-follow-up-setup>)
    * [Configure a model](<#configure-a-model>)
    * [Re-run the full interactive setup wizard later](<#re-run-the-full-interactive-setup-wizard-later>)
    * [Install optional Node dependencies manually](<#install-optional-node-dependencies-manually>)
  * [Troubleshooting](<#troubleshooting>)
    * [`No solution found` when installing `.[all]`](<#no-solution-found-when-installing-all>)
    * [`uv pip install` fails on Android](<#uv-pip-install-fails-on-android>)
    * [`jiter` / `maturin` complains about `ANDROID_API_LEVEL`](<#jiter--maturin-complains-about-android_api_level>)
    * [`hermes doctor` says ripgrep or Node is missing](<#hermes-doctor-says-ripgrep-or-node-is-missing>)
    * [Build failures while installing Python packages](<#build-failures-while-installing-python-packages>)
  * [Known limitations on phones](<#known-limitations-on-phones>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/getting-started/termux -->
