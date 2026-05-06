On this page
Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/research/blogwatcher`  
Version| `2.0.0`  
Author| JulienTant (fork of Hyaxia/blogwatcher)  
License| MIT  
Tags| `RSS`, `Blogs`, `Feed-Reader`, `Monitoring`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Blogwatcher
Track blog and RSS/Atom feed updates with the `blogwatcher-cli` tool. Supports automatic feed discovery, HTML scraping fallback, OPML import, and read/unread article management.
## Installation[​](<#installation> "Direct link to Installation")
Pick one method:
  * **Go:** `go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest`
  * **Docker:** `docker run --rm -v blogwatcher-cli:/data ghcr.io/julientant/blogwatcher-cli`
  * **Binary (Linux amd64):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  * **Binary (Linux arm64):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  * **Binary (macOS Apple Silicon):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  * **Binary (macOS Intel):** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`


All releases: <https://github.com/JulienTant/blogwatcher-cli/releases>
### Docker with persistent storage[​](<#docker-with-persistent-storage> "Direct link to Docker with persistent storage")
By default the database lives at `~/.blogwatcher-cli/blogwatcher-cli.db`. In Docker this is lost on container restart. Use `BLOGWATCHER_DB` or a volume mount to persist it:
[code] 
    # Named volume (simplest)  
    docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan  
      
    # Host bind mount  
    docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan  
    
[/code]
### Migrating from the original blogwatcher[​](<#migrating-from-the-original-blogwatcher> "Direct link to Migrating from the original blogwatcher")
If upgrading from `Hyaxia/blogwatcher`, move your database:
[code] 
    mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db  
    
[/code]
The binary name changed from `blogwatcher` to `blogwatcher-cli`.
## Common Commands[​](<#common-commands> "Direct link to Common Commands")
### Managing blogs[​](<#managing-blogs> "Direct link to Managing blogs")
  * Add a blog: `blogwatcher-cli add "My Blog" https://example.com`
  * Add with explicit feed: `blogwatcher-cli add "My Blog" https://example.com --feed-url https://example.com/feed.xml`
  * Add with HTML scraping: `blogwatcher-cli add "My Blog" https://example.com --scrape-selector "article h2 a"`
  * List tracked blogs: `blogwatcher-cli blogs`
  * Remove a blog: `blogwatcher-cli remove "My Blog" --yes`
  * Import from OPML: `blogwatcher-cli import subscriptions.opml`


### Scanning and reading[​](<#scanning-and-reading> "Direct link to Scanning and reading")
  * Scan all blogs: `blogwatcher-cli scan`
  * Scan one blog: `blogwatcher-cli scan "My Blog"`
  * List unread articles: `blogwatcher-cli articles`
  * List all articles: `blogwatcher-cli articles --all`
  * Filter by blog: `blogwatcher-cli articles --blog "My Blog"`
  * Filter by category: `blogwatcher-cli articles --category "Engineering"`
  * Mark article read: `blogwatcher-cli read 1`
  * Mark article unread: `blogwatcher-cli unread 1`
  * Mark all read: `blogwatcher-cli read-all`
  * Mark all read for a blog: `blogwatcher-cli read-all --blog "My Blog" --yes`


## Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
All flags can be set via environment variables with the `BLOGWATCHER_` prefix:
Variable| Description  
---|---  
`BLOGWATCHER_DB`| Path to SQLite database file  
`BLOGWATCHER_WORKERS`| Number of concurrent scan workers (default: 8)  
`BLOGWATCHER_SILENT`| Only output "scan done" when scanning  
`BLOGWATCHER_YES`| Skip confirmation prompts  
`BLOGWATCHER_CATEGORY`| Default filter for articles by category  
## Example Output[​](<#example-output> "Direct link to Example Output")
[code] 
    $ blogwatcher-cli blogs  
    Tracked blogs (1):  
      
      xkcd  
        URL: https://xkcd.com  
        Feed: https://xkcd.com/atom.xml  
        Last scanned: 2026-04-03 10:30  
    
[/code]
[code] 
    $ blogwatcher-cli scan  
    Scanning 1 blog(s)...  
      
      xkcd  
        Source: RSS | Found: 4 | New: 4  
      
    Found 4 new article(s) total!  
    
[/code]
[code] 
    $ blogwatcher-cli articles  
    Unread articles (2):  
      
      [1] [new] Barrel - Part 13  
           Blog: xkcd  
           URL: https://xkcd.com/3095/  
           Published: 2026-04-02  
           Categories: Comics, Science  
      
      [2] [new] Volcano Fact  
           Blog: xkcd  
           URL: https://xkcd.com/3094/  
           Published: 2026-04-01  
           Categories: Comics  
    
[/code]
## Notes[​](<#notes> "Direct link to Notes")
  * Auto-discovers RSS/Atom feeds from blog homepages when no `--feed-url` is provided.
  * Falls back to HTML scraping if RSS fails and `--scrape-selector` is configured.
  * Categories from RSS/Atom feeds are stored and can be used to filter articles.
  * Import blogs in bulk from OPML files exported by Feedly, Inoreader, NewsBlur, etc.
  * Database stored at `~/.blogwatcher-cli/blogwatcher-cli.db` by default (override with `--db` or `BLOGWATCHER_DB`).
  * Use `blogwatcher-cli <command> --help` to discover all flags and options.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Installation](<#installation>)
    * [Docker with persistent storage](<#docker-with-persistent-storage>)
    * [Migrating from the original blogwatcher](<#migrating-from-the-original-blogwatcher>)
  * [Common Commands](<#common-commands>)
    * [Managing blogs](<#managing-blogs>)
    * [Scanning and reading](<#scanning-and-reading>)
  * [Environment Variables](<#environment-variables>)
  * [Example Output](<#example-output>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-blogwatcher -->
