On this page
Search/download GIFs from Tenor via curl + jq.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/media/gif-search`  
Version| `1.1.0`  
Author| Hermes Agent  
License| MIT  
Tags| `GIF`, `Media`, `Search`, `Tenor`, `API`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# GIF Search (Tenor API)
Search and download GIFs directly via the Tenor API using curl. No extra tools needed.
## When to use[​](<#when-to-use> "Direct link to When to use")
Useful for finding reaction GIFs, creating visual content, and sending GIFs in chat.
## Setup[​](<#setup> "Direct link to Setup")
Set your Tenor API key in your environment (add to `~/.hermes/.env`):
[code] 
    TENOR_API_KEY=your_key_here  
    
[/code]
Get a free API key at <https://developers.google.com/tenor/guides/quickstart> — the Google Cloud Console Tenor API key is free and has generous rate limits.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * `curl` and `jq` (both standard on macOS/Linux)
  * `TENOR_API_KEY` environment variable


## Search for GIFs[​](<#search-for-gifs> "Direct link to Search for GIFs")
[code] 
    # Search and get GIF URLs  
    curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'  
      
    # Get smaller/preview versions  
    curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'  
    
[/code]
## Download a GIF[​](<#download-a-gif> "Direct link to Download a GIF")
[code] 
    # Search and download the top result  
    URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')  
    curl -sL "$URL" -o celebration.gif  
    
[/code]
## Get Full Metadata[​](<#get-full-metadata> "Direct link to Get Full Metadata")
[code] 
    curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'  
    
[/code]
## API Parameters[​](<#api-parameters> "Direct link to API Parameters")
Parameter| Description  
---|---  
`q`| Search query (URL-encode spaces as `+`)  
`limit`| Max results (1-50, default 20)  
`key`| API key (from `$TENOR_API_KEY` env var)  
`media_filter`| Filter formats: `gif`, `tinygif`, `mp4`, `tinymp4`, `webm`  
`contentfilter`| Safety: `off`, `low`, `medium`, `high`  
`locale`| Language: `en_US`, `es`, `fr`, etc.  
## Available Media Formats[​](<#available-media-formats> "Direct link to Available Media Formats")
Each result has multiple formats under `.media_formats`:
Format| Use case  
---|---  
`gif`| Full quality GIF  
`tinygif`| Small preview GIF  
`mp4`| Video version (smaller file size)  
`tinymp4`| Small preview video  
`webm`| WebM video  
`nanogif`| Tiny thumbnail  
## Notes[​](<#notes> "Direct link to Notes")
  * URL-encode the query: spaces as `+`, special chars as `%XX`
  * For sending in chat, `tinygif` URLs are lighter weight
  * GIF URLs can be used directly in markdown: `![alt](https://github.com/NousResearch/hermes-agent/blob/main/skills/media/gif-search/url)`


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Setup](<#setup>)
  * [Prerequisites](<#prerequisites>)
  * [Search for GIFs](<#search-for-gifs>)
  * [Download a GIF](<#download-a-gif>)
  * [Get Full Metadata](<#get-full-metadata>)
  * [API Parameters](<#api-parameters>)
  * [Available Media Formats](<#available-media-formats>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/media/media-gif-search -->
