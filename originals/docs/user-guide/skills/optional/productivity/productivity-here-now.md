On this page
Publish static sites to {slug}.here.now and store private files in cloud Drives for agent-to-agent handoff.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/productivity/here-now`  
Path| `optional-skills/productivity/here-now`  
Version| `1.15.3`  
Author| here.now  
License| MIT  
Platforms| macos, linux  
Tags| `here.now`, `herenow`, `publish`, `deploy`, `hosting`, `static-site`, `web`, `share`, `URL`, `drive`, `storage`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# here.now
here.now lets agents publish websites and store private files in cloud Drives.
Use here.now for two jobs:
  * **Sites** : publish websites and files at `{slug}.here.now`.
  * **Drives** : store private agent files in cloud folders.


## Current docs[​](<#current-docs> "Direct link to Current docs")
**Before answering questions about here.now capabilities, features, or workflows, read the current docs:**
→ **<https://here.now/docs>**
Read the docs:
  * at the first here.now-related interaction in a conversation
  * any time the user asks how to do something
  * any time the user asks what is possible, supported, or recommended
  * before telling the user a feature is unsupported


Topics that require current docs (do not rely on local skill text alone):
  * Drives and Drive sharing
  * custom domains
  * payments and payment gating
  * forking
  * proxy routes and service variables
  * handles and links
  * limits and quotas
  * SPA routing
  * error handling and remediation
  * feature availability


**If docs and live API behavior disagree, trust the live API behavior.**
If the docs fetch fails or times out, continue with the local skill and live API/script output. Prefer live API behavior for active operations.
## Requirements[​](<#requirements> "Direct link to Requirements")
  * Required binaries: `curl`, `file`, `jq`
  * Optional environment variable: `$HERENOW_API_KEY`
  * Optional Drive token variable: `$HERENOW_DRIVE_TOKEN`
  * Optional credentials file: `~/.herenow/credentials`
  * Skill helper paths:
    * `${HERMES_SKILL_DIR}/scripts/publish.sh` for publishing sites
    * `${HERMES_SKILL_DIR}/scripts/drive.sh` for private Drive storage


## Create a site[​](<#create-a-site> "Direct link to Create a site")
[code] 
    PUBLISH="${HERMES_SKILL_DIR}/scripts/publish.sh"  
    bash "$PUBLISH" {file-or-dir} --client hermes  
    
[/code]
Outputs the live URL (e.g. `https://bright-canvas-a7k2.here.now/`).
Under the hood this is a three-step flow: create/update -> upload files -> finalize. A site is not live until finalize succeeds.
Without an API key this creates an **anonymous site** that expires in 24 hours. With a saved API key, the site is permanent.
**File structure:** For HTML sites, place `index.html` at the root of the directory you publish, not inside a subdirectory. The directory's contents become the site root. For example, publish `my-site/` where `my-site/index.html` exists — don't publish a parent folder that contains `my-site/`.
You can also publish raw files without any HTML. Single files get a rich auto-viewer (images, PDF, video, audio). Multiple files get an auto-generated directory listing with folder navigation and an image gallery.
## Update an existing site[​](<#update-an-existing-site> "Direct link to Update an existing site")
[code] 
    PUBLISH="${HERMES_SKILL_DIR}/scripts/publish.sh"  
    bash "$PUBLISH" {file-or-dir} --slug {slug} --client hermes  
    
[/code]
The script auto-loads the `claimToken` from `.herenow/state.json` when updating anonymous sites. Pass `--claim-token {token}` to override.
Authenticated updates require a saved API key.
## Use a Drive[​](<#use-a-drive> "Direct link to Use a Drive")
Use a Drive when the user wants private cloud storage for agent files: documents, context, memory, plans, assets, media, research, code, and anything else that should persist without being published as a website.
Every signed-in account has a default Drive named `My Drive`.
[code] 
    DRIVE="${HERMES_SKILL_DIR}/scripts/drive.sh"  
    bash "$DRIVE" default  
    bash "$DRIVE" ls "My Drive"  
    bash "$DRIVE" put "My Drive" notes/today.md --from ./notes/today.md  
    bash "$DRIVE" cat "My Drive" notes/today.md  
    bash "$DRIVE" share "My Drive" --perms write --prefix notes/ --ttl 7d  
    
[/code]
Use scoped Drive tokens for agent-to-agent handoff. If you receive a `herenow_drive` share block, use its `token` as `Authorization: Bearer <token>` against `api_base`, respect `pathPrefix` when present, and preserve ETags on writes. A `pathPrefix` of `null` means full-Drive access. If the skill is available, prefer `drive.sh`; otherwise call the listed API operations directly.
## API key storage[​](<#api-key-storage> "Direct link to API key storage")
The publish script reads the API key from these sources (first match wins):
  1. `--api-key {key}` flag (CI/scripting only — avoid in interactive use)
  2. `$HERENOW_API_KEY` environment variable
  3. `~/.herenow/credentials` file (recommended for agents)


To store a key, write it to the credentials file:
[code] 
    mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials  
    
[/code]
**IMPORTANT** : After receiving an API key, save it immediately — run the command above yourself. Do not ask the user to run it manually. Avoid passing the key via CLI flags (e.g. `--api-key`) in interactive sessions; the credentials file is the preferred storage method.
Never commit credentials or local state files (`~/.herenow/credentials`, `.herenow/state.json`) to source control.
## Getting an API key[​](<#getting-an-api-key> "Direct link to Getting an API key")
To upgrade from anonymous (24h) to permanent sites:
  1. Ask the user for their email address.
  2. Request a one-time sign-in code:


[code] 
    curl -sS https://here.now/api/auth/agent/request-code \  
      -H "content-type: application/json" \  
      -d '{"email": "user@example.com"}'  
    
[/code]
  3. Tell the user: "Check your inbox for a sign-in code from here.now and paste it here."
  4. Verify the code and get the API key:


[code] 
    curl -sS https://here.now/api/auth/agent/verify-code \  
      -H "content-type: application/json" \  
      -d '{"email":"user@example.com","code":"ABCD-2345"}'  
    
[/code]
  5. Save the returned `apiKey` yourself (do not ask the user to do this):


[code] 
    mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials  
    
[/code]
## State file[​](<#state-file> "Direct link to State file")
After every site create/update, the script writes to `.herenow/state.json` in the working directory:
[code] 
    {  
      "publishes": {  
        "bright-canvas-a7k2": {  
          "siteUrl": "https://bright-canvas-a7k2.here.now/",  
          "claimToken": "abc123",  
          "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123",  
          "expiresAt": "2026-02-18T01:00:00.000Z"  
        }  
      }  
    }  
    
[/code]
Before creating or updating sites, you may check this file to find prior slugs. Treat `.herenow/state.json` as internal cache only. Never present this local file path as a URL, and never use it as source of truth for auth mode, expiry, or claim URL.
## What to tell the user[​](<#what-to-tell-the-user> "Direct link to What to tell the user")
For published sites:
  * Always share the `siteUrl` from the current script run.
  * Read and follow `publish_result.*` lines from script stderr to determine auth mode.
  * When `publish_result.auth_mode=authenticated`: tell the user the site is **permanent** and saved to their account. No claim URL is needed.
  * When `publish_result.auth_mode=anonymous`: tell the user the site **expires in 24 hours**. Share the claim URL (if `publish_result.claim_url` is non-empty and starts with `https://`) so they can keep it permanently. Warn that claim tokens are only returned once and cannot be recovered.
  * Never tell the user to inspect `.herenow/state.json` for claim URLs or auth status.


For Drives:
  * Do not describe Drive files as public URLs.
  * Tell the user Drive contents are private unless shared with a scoped token.
  * When sharing access with another agent, prefer a scoped token with a narrow `pathPrefix` and short TTL.


## publish.sh options[​](<#publishsh-options> "Direct link to publish.sh options")
Flag| Description  
---|---  
`--slug {slug}`| Update an existing site instead of creating  
`--claim-token {token}`| Override claim token for anonymous updates  
`--title {text}`| Viewer title (non-HTML sites)  
`--description {text}`| Viewer description  
`--ttl {seconds}`| Set expiry (authenticated only)  
`--client {name}`| Agent name for attribution (e.g. `hermes`)  
`--base-url {url}`| API base URL (default: `https://here.now`)  
`--allow-nonherenow-base-url`| Allow sending auth to non-default `--base-url`  
`--api-key {key}`| API key override (prefer credentials file)  
`--spa`| Enable SPA routing (serve index.html for unknown paths)  
`--forkable`| Allow others to fork this site  
## Beyond publish.sh[​](<#beyond-publishsh> "Direct link to Beyond publish.sh")
For Drive operations, use `drive.sh` or the Drive API. For broader account and site management — delete, metadata, passwords, payments, domains, handles, links, variables, proxy routes, forking, duplication, and more — see the current docs:
→ **<https://here.now/docs>**
Full docs: <https://here.now/docs>
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Current docs](<#current-docs>)
  * [Requirements](<#requirements>)
  * [Create a site](<#create-a-site>)
  * [Update an existing site](<#update-an-existing-site>)
  * [Use a Drive](<#use-a-drive>)
  * [API key storage](<#api-key-storage>)
  * [Getting an API key](<#getting-an-api-key>)
  * [State file](<#state-file>)
  * [What to tell the user](<#what-to-tell-the-user>)
  * [publish.sh options](<#publishsh-options>)
  * [Beyond publish.sh](<#beyond-publishsh>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-here-now -->
