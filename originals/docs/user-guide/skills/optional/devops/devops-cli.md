On this page
Run 150+ AI apps via inference.sh CLI (infsh) — image generation, video creation, LLMs, search, 3D, social automation. Uses the terminal tool. Triggers: inference.sh, infsh, ai apps, flux, veo, image generation, video generation, seedream, seedance, tavily
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/devops/cli`  
Path| `optional-skills/devops/cli`  
Version| `1.0.0`  
Author| okaris  
License| MIT  
Tags| `AI`, `image-generation`, `video`, `LLM`, `search`, `inference`, `FLUX`, `Veo`, `Claude`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# inference.sh CLI
Run 150+ AI apps in the cloud with a simple CLI. No GPU required.
All commands use the **terminal tool** to run `infsh` commands.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * User asks to generate images (FLUX, Reve, Seedream, Grok, Gemini image)
  * User asks to generate video (Veo, Wan, Seedance, OmniHuman)
  * User asks about inference.sh or infsh
  * User wants to run AI apps without managing individual provider APIs
  * User asks for AI-powered search (Tavily, Exa)
  * User needs avatar/lipsync generation


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
The `infsh` CLI must be installed and authenticated. Check with:
[code] 
    infsh me  
    
[/code]
If not installed:
[code] 
    curl -fsSL https://cli.inference.sh | sh  
    infsh login  
    
[/code]
See `references/authentication.md` for full setup details.
## Workflow[​](<#workflow> "Direct link to Workflow")
### 1\. Always Search First[​](<#1-always-search-first> "Direct link to 1. Always Search First")
Never guess app names — always search to find the correct app ID:
[code] 
    infsh app list --search flux  
    infsh app list --search video  
    infsh app list --search image  
    
[/code]
### 2\. Run an App[​](<#2-run-an-app> "Direct link to 2. Run an App")
Use the exact app ID from the search results. Always use `--json` for machine-readable output:
[code] 
    infsh app run <app-id> --input '{"prompt": "your prompt here"}' --json  
    
[/code]
### 3\. Parse the Output[​](<#3-parse-the-output> "Direct link to 3. Parse the Output")
The JSON output contains URLs to generated media. Present these to the user with `MEDIA:<url>` for inline display.
## Common Commands[​](<#common-commands> "Direct link to Common Commands")
### Image Generation[​](<#image-generation> "Direct link to Image Generation")
[code] 
    # Search for image apps  
    infsh app list --search image  
      
    # FLUX Dev with LoRA  
    infsh app run falai/flux-dev-lora --input '{"prompt": "sunset over mountains", "num_images": 1}' --json  
      
    # Gemini image generation  
    infsh app run google/gemini-2-5-flash-image --input '{"prompt": "futuristic city", "num_images": 1}' --json  
      
    # Seedream (ByteDance)  
    infsh app run bytedance/seedream-5-lite --input '{"prompt": "nature scene"}' --json  
      
    # Grok Imagine (xAI)  
    infsh app run xai/grok-imagine-image --input '{"prompt": "abstract art"}' --json  
    
[/code]
### Video Generation[​](<#video-generation> "Direct link to Video Generation")
[code] 
    # Search for video apps  
    infsh app list --search video  
      
    # Veo 3.1 (Google)  
    infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot of coastline"}' --json  
      
    # Seedance (ByteDance)  
    infsh app run bytedance/seedance-1-5-pro --input '{"prompt": "dancing figure", "resolution": "1080p"}' --json  
      
    # Wan 2.5  
    infsh app run falai/wan-2-5 --input '{"prompt": "person walking through city"}' --json  
    
[/code]
### Local File Uploads[​](<#local-file-uploads> "Direct link to Local File Uploads")
The CLI automatically uploads local files when you provide a path:
[code] 
    # Upscale a local image  
    infsh app run falai/topaz-image-upscaler --input '{"image": "/path/to/photo.jpg", "upscale_factor": 2}' --json  
      
    # Image-to-video from local file  
    infsh app run falai/wan-2-5-i2v --input '{"image": "/path/to/image.png", "prompt": "make it move"}' --json  
      
    # Avatar with audio  
    infsh app run bytedance/omnihuman-1-5 --input '{"audio": "/path/to/audio.mp3", "image": "/path/to/face.jpg"}' --json  
    
[/code]
### Search & Research[​](<#search--research> "Direct link to Search & Research")
[code] 
    infsh app list --search search  
    infsh app run tavily/tavily-search --input '{"query": "latest AI news"}' --json  
    infsh app run exa/exa-search --input '{"query": "machine learning papers"}' --json  
    
[/code]
### Other Categories[​](<#other-categories> "Direct link to Other Categories")
[code] 
    # 3D generation  
    infsh app list --search 3d  
      
    # Audio / TTS  
    infsh app list --search tts  
      
    # Twitter/X automation  
    infsh app list --search twitter  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  1. **Never guess app IDs** — always run `infsh app list --search <term>` first. App IDs change and new apps are added frequently.
  2. **Always use`--json`** — raw output is hard to parse. The `--json` flag gives structured output with URLs.
  3. **Check authentication** — if commands fail with auth errors, run `infsh login` or verify `INFSH_API_KEY` is set.
  4. **Long-running apps** — video generation can take 30-120 seconds. The terminal tool timeout should be sufficient, but warn the user it may take a moment.
  5. **Input format** — the `--input` flag takes a JSON string. Make sure to properly escape quotes.


## Reference Docs[​](<#reference-docs> "Direct link to Reference Docs")
  * `references/authentication.md` — Setup, login, API keys
  * `references/app-discovery.md` — Searching and browsing the app catalog
  * `references/running-apps.md` — Running apps, input formats, output handling
  * `references/cli-reference.md` — Complete CLI command reference


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [Workflow](<#workflow>)
    * [1\. Always Search First](<#1-always-search-first>)
    * [2\. Run an App](<#2-run-an-app>)
    * [3\. Parse the Output](<#3-parse-the-output>)
  * [Common Commands](<#common-commands>)
    * [Image Generation](<#image-generation>)
    * [Video Generation](<#video-generation>)
    * [Local File Uploads](<#local-file-uploads>)
    * [Search & Research](<#search--research>)
    * [Other Categories](<#other-categories>)
  * [Pitfalls](<#pitfalls>)
  * [Reference Docs](<#reference-docs>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/devops/devops-cli -->
