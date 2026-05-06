On this page
HuggingFace hf CLI: search/download/upload models, datasets.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/mlops/huggingface-hub`  
Version| `1.0.0`  
Author| Hugging Face  
License| MIT  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Hugging Face CLI (`hf`) Reference Guide
The `hf` command is the modern command-line interface for interacting with the Hugging Face Hub, providing tools to manage repositories, models, datasets, and Spaces.
> **IMPORTANT:** The `hf` command replaces the now deprecated `huggingface-cli` command.
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
  * **Installation:** `curl -LsSf https://hf.co/cli/install.sh | bash -s`
  * **Help:** Use `hf --help` to view all available functions and real-world examples.
  * **Authentication:** Recommended via `HF_TOKEN` environment variable or the `--token` flag.


* * *
## Core Commands[​](<#core-commands> "Direct link to Core Commands")
### General Operations[​](<#general-operations> "Direct link to General Operations")
  * `hf download REPO_ID`: Download files from the Hub.
  * `hf upload REPO_ID`: Upload files/folders (recommended for single-commit).
  * `hf upload-large-folder REPO_ID LOCAL_PATH`: Recommended for resumable uploads of large directories.
  * `hf sync`: Sync files between a local directory and a bucket.
  * `hf env` / `hf version`: View environment and version details.


### Authentication (`hf auth`)[​](<#authentication-hf-auth> "Direct link to authentication-hf-auth")
  * `login` / `logout`: Manage sessions using tokens from [huggingface.co/settings/tokens](<https://huggingface.co/settings/tokens>).
  * `list` / `switch`: Manage and toggle between multiple stored access tokens.
  * `whoami`: Identify the currently logged-in account.


### Repository Management (`hf repos`)[​](<#repository-management-hf-repos> "Direct link to repository-management-hf-repos")
  * `create` / `delete`: Create or permanently remove repositories.
  * `duplicate`: Clone a model, dataset, or Space to a new ID.
  * `move`: Transfer a repository between namespaces.
  * `branch` / `tag`: Manage Git-like references.
  * `delete-files`: Remove specific files using patterns.


* * *
## Specialized Hub Interactions[​](<#specialized-hub-interactions> "Direct link to Specialized Hub Interactions")
### Datasets & Models[​](<#datasets--models> "Direct link to Datasets & Models")
  * **Datasets:** `hf datasets list`, `info`, and `parquet` (list parquet URLs).
  * **SQL Queries:** `hf datasets sql SQL` — Execute raw SQL via DuckDB against dataset parquet URLs.
  * **Models:** `hf models list` and `info`.
  * **Papers:** `hf papers list` — View daily papers.


### Discussions & Pull Requests (`hf discussions`)[​](<#discussions--pull-requests-hf-discussions> "Direct link to discussions--pull-requests-hf-discussions")
  * Manage the lifecycle of Hub contributions: `list`, `create`, `info`, `comment`, `close`, `reopen`, and `rename`.
  * `diff`: View changes in a PR.
  * `merge`: Finalize pull requests.


### Infrastructure & Compute[​](<#infrastructure--compute> "Direct link to Infrastructure & Compute")
  * **Endpoints:** Deploy and manage Inference Endpoints (`deploy`, `pause`, `resume`, `scale-to-zero`, `catalog`).
  * **Jobs:** Run compute tasks on HF infrastructure. Includes `hf jobs uv` for running Python scripts with inline dependencies and `stats` for resource monitoring.
  * **Spaces:** Manage interactive apps. Includes `dev-mode` and `hot-reload` for Python files without full restarts.


### Storage & Automation[​](<#storage--automation> "Direct link to Storage & Automation")
  * **Buckets:** Full S3-like bucket management (`create`, `cp`, `mv`, `rm`, `sync`).
  * **Cache:** Manage local storage with `list`, `prune` (remove detached revisions), and `verify` (checksum checks).
  * **Webhooks:** Automate workflows by managing Hub webhooks (`create`, `watch`, `enable`/`disable`).
  * **Collections:** Organize Hub items into collections (`add-item`, `update`, `list`).


* * *
## Advanced Usage & Tips[​](<#advanced-usage--tips> "Direct link to Advanced Usage & Tips")
### Global Flags[​](<#global-flags> "Direct link to Global Flags")
  * `--format json`: Produces machine-readable output for automation.
  * `-q` / `--quiet`: Limits output to IDs only.


### Extensions & Skills[​](<#extensions--skills> "Direct link to Extensions & Skills")
  * **Extensions:** Extend CLI functionality via GitHub repositories using `hf extensions install REPO_ID`.
  * **Skills:** Manage AI assistant skills with `hf skills add`.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Quick Start](<#quick-start>)
  * [Core Commands](<#core-commands>)
    * [General Operations](<#general-operations>)
    * [Authentication (`hf auth`)](<#authentication-hf-auth>)
    * [Repository Management (`hf repos`)](<#repository-management-hf-repos>)
  * [Specialized Hub Interactions](<#specialized-hub-interactions>)
    * [Datasets & Models](<#datasets--models>)
    * [Discussions & Pull Requests (`hf discussions`)](<#discussions--pull-requests-hf-discussions>)
    * [Infrastructure & Compute](<#infrastructure--compute>)
    * [Storage & Automation](<#storage--automation>)
  * [Advanced Usage & Tips](<#advanced-usage--tips>)
    * [Global Flags](<#global-flags>)
    * [Extensions & Skills](<#extensions--skills>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-huggingface-hub -->
