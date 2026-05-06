On this page
ASCII art: pyfiglet, cowsay, boxes, image-to-ascii.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/creative/ascii-art`  
Version| `4.0.0`  
Author| 0xbyt4, Hermes Agent  
License| MIT  
Tags| `ASCII`, `Art`, `Banners`, `Creative`, `Unicode`, `Text-Art`, `pyfiglet`, `figlet`, `cowsay`, `boxes`  
Related skills| [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# ASCII Art Skill
Multiple tools for different ASCII art needs. All tools are local CLI programs or free REST APIs — no API keys required.
## Tool 1: Text Banners (pyfiglet — local)[​](<#tool-1-text-banners-pyfiglet--local> "Direct link to Tool 1: Text Banners \(pyfiglet — local\)")
Render text as large ASCII art banners. 571 built-in fonts.
### Setup[​](<#setup> "Direct link to Setup")
[code] 
    pip install pyfiglet --break-system-packages -q  
    
[/code]
### Usage[​](<#usage> "Direct link to Usage")
[code] 
    python3 -m pyfiglet "YOUR TEXT" -f slant  
    python3 -m pyfiglet "TEXT" -f doom -w 80    # Set width  
    python3 -m pyfiglet --list_fonts             # List all 571 fonts  
    
[/code]
### Recommended fonts[​](<#recommended-fonts> "Direct link to Recommended fonts")
Style| Font| Best for  
---|---|---  
Clean & modern| `slant`| Project names, headers  
Bold & blocky| `doom`| Titles, logos  
Big & readable| `big`| Banners  
Classic banner| `banner3`| Wide displays  
Compact| `small`| Subtitles  
Cyberpunk| `cyberlarge`| Tech themes  
3D effect| `3-d`| Splash screens  
Gothic| `gothic`| Dramatic text  
### Tips[​](<#tips> "Direct link to Tips")
  * Preview 2-3 fonts and let the user pick their favorite
  * Short text (1-8 chars) works best with detailed fonts like `doom` or `block`
  * Long text works better with compact fonts like `small` or `mini`


## Tool 2: Text Banners (asciified API — remote, no install)[​](<#tool-2-text-banners-asciified-api--remote-no-install> "Direct link to Tool 2: Text Banners \(asciified API — remote, no install\)")
Free REST API that converts text to ASCII art. 250+ FIGlet fonts. Returns plain text directly — no parsing needed. Use this when pyfiglet is not installed or as a quick alternative.
### Usage (via terminal curl)[​](<#usage-via-terminal-curl> "Direct link to Usage \(via terminal curl\)")
[code] 
    # Basic text banner (default font)  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello+World"  
      
    # With a specific font  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant"  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Doom"  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Star+Wars"  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=3-D"  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Banner3"  
      
    # List all available fonts (returns JSON array)  
    curl -s "https://asciified.thelicato.io/api/v2/fonts"  
    
[/code]
### Tips[​](<#tips-1> "Direct link to Tips")
  * URL-encode spaces as `+` in the text parameter
  * The response is plain text ASCII art — no JSON wrapping, ready to display
  * Font names are case-sensitive; use the fonts endpoint to get exact names
  * Works from any terminal with curl — no Python or pip needed


## Tool 3: Cowsay (Message Art)[​](<#tool-3-cowsay-message-art> "Direct link to Tool 3: Cowsay \(Message Art\)")
Classic tool that wraps text in a speech bubble with an ASCII character.
### Setup[​](<#setup-1> "Direct link to Setup")
[code] 
    sudo apt install cowsay -y    # Debian/Ubuntu  
    # brew install cowsay         # macOS  
    
[/code]
### Usage[​](<#usage-1> "Direct link to Usage")
[code] 
    cowsay "Hello World"  
    cowsay -f tux "Linux rules"       # Tux the penguin  
    cowsay -f dragon "Rawr!"          # Dragon  
    cowsay -f stegosaurus "Roar!"     # Stegosaurus  
    cowthink "Hmm..."                  # Thought bubble  
    cowsay -l                          # List all characters  
    
[/code]
### Available characters (50+)[​](<#available-characters-50> "Direct link to Available characters \(50+\)")
`beavis.zen`, `bong`, `bunny`, `cheese`, `daemon`, `default`, `dragon`, `dragon-and-cow`, `elephant`, `eyes`, `flaming-skull`, `ghostbusters`, `hellokitty`, `kiss`, `kitty`, `koala`, `luke-koala`, `mech-and-cow`, `meow`, `moofasa`, `moose`, `ren`, `sheep`, `skeleton`, `small`, `stegosaurus`, `stimpy`, `supermilker`, `surgery`, `three-eyes`, `turkey`, `turtle`, `tux`, `udder`, `vader`, `vader-koala`, `www`
### Eye/tongue modifiers[​](<#eyetongue-modifiers> "Direct link to Eye/tongue modifiers")
[code] 
    cowsay -b "Borg"       # =_= eyes  
    cowsay -d "Dead"       # x_x eyes  
    cowsay -g "Greedy"     # $_$ eyes  
    cowsay -p "Paranoid"   # @_@ eyes  
    cowsay -s "Stoned"     # *_* eyes  
    cowsay -w "Wired"      # O_O eyes  
    cowsay -e "OO" "Msg"   # Custom eyes  
    cowsay -T "U " "Msg"   # Custom tongue  
    
[/code]
## Tool 4: Boxes (Decorative Borders)[​](<#tool-4-boxes-decorative-borders> "Direct link to Tool 4: Boxes \(Decorative Borders\)")
Draw decorative ASCII art borders/frames around any text. 70+ built-in designs.
### Setup[​](<#setup-2> "Direct link to Setup")
[code] 
    sudo apt install boxes -y    # Debian/Ubuntu  
    # brew install boxes         # macOS  
    
[/code]
### Usage[​](<#usage-2> "Direct link to Usage")
[code] 
    echo "Hello World" | boxes                    # Default box  
    echo "Hello World" | boxes -d stone           # Stone border  
    echo "Hello World" | boxes -d parchment       # Parchment scroll  
    echo "Hello World" | boxes -d cat             # Cat border  
    echo "Hello World" | boxes -d dog             # Dog border  
    echo "Hello World" | boxes -d unicornsay      # Unicorn  
    echo "Hello World" | boxes -d diamonds        # Diamond pattern  
    echo "Hello World" | boxes -d c-cmt           # C-style comment  
    echo "Hello World" | boxes -d html-cmt        # HTML comment  
    echo "Hello World" | boxes -a c               # Center text  
    boxes -l                                       # List all 70+ designs  
    
[/code]
### Combine with pyfiglet or asciified[​](<#combine-with-pyfiglet-or-asciified> "Direct link to Combine with pyfiglet or asciified")
[code] 
    python3 -m pyfiglet "HERMES" -f slant | boxes -d stone  
    # Or without pyfiglet installed:  
    curl -s "https://asciified.thelicato.io/api/v2/ascii?text=HERMES&font=Slant" | boxes -d stone  
    
[/code]
## Tool 5: TOIlet (Colored Text Art)[​](<#tool-5-toilet-colored-text-art> "Direct link to Tool 5: TOIlet \(Colored Text Art\)")
Like pyfiglet but with ANSI color effects and visual filters. Great for terminal eye candy.
### Setup[​](<#setup-3> "Direct link to Setup")
[code] 
    sudo apt install toilet toilet-fonts -y    # Debian/Ubuntu  
    # brew install toilet                      # macOS  
    
[/code]
### Usage[​](<#usage-3> "Direct link to Usage")
[code] 
    toilet "Hello World"                    # Basic text art  
    toilet -f bigmono12 "Hello"            # Specific font  
    toilet --gay "Rainbow!"                 # Rainbow coloring  
    toilet --metal "Metal!"                 # Metallic effect  
    toilet -F border "Bordered"             # Add border  
    toilet -F border --gay "Fancy!"         # Combined effects  
    toilet -f pagga "Block"                 # Block-style font (unique to toilet)  
    toilet -F list                          # List available filters  
    
[/code]
### Filters[​](<#filters> "Direct link to Filters")
`crop`, `gay` (rainbow), `metal`, `flip`, `flop`, `180`, `left`, `right`, `border`
**Note** : toilet outputs ANSI escape codes for colors — works in terminals but may not render in all contexts (e.g., plain text files, some chat platforms).
## Tool 6: Image to ASCII Art[​](<#tool-6-image-to-ascii-art> "Direct link to Tool 6: Image to ASCII Art")
Convert images (PNG, JPEG, GIF, WEBP) to ASCII art.
### Option A: ascii-image-converter (recommended, modern)[​](<#option-a-ascii-image-converter-recommended-modern> "Direct link to Option A: ascii-image-converter \(recommended, modern\)")
[code] 
    # Install  
    sudo snap install ascii-image-converter  
    # OR: go install github.com/TheZoraiz/ascii-image-converter@latest  
    
[/code]
[code] 
    ascii-image-converter image.png                  # Basic  
    ascii-image-converter image.png -C               # Color output  
    ascii-image-converter image.png -d 60,30         # Set dimensions  
    ascii-image-converter image.png -b               # Braille characters  
    ascii-image-converter image.png -n               # Negative/inverted  
    ascii-image-converter https://url/image.jpg      # Direct URL  
    ascii-image-converter image.png --save-txt out   # Save as text  
    
[/code]
### Option B: jp2a (lightweight, JPEG only)[​](<#option-b-jp2a-lightweight-jpeg-only> "Direct link to Option B: jp2a \(lightweight, JPEG only\)")
[code] 
    sudo apt install jp2a -y  
    jp2a --width=80 image.jpg  
    jp2a --colors image.jpg              # Colorized  
    
[/code]
## Tool 7: Search Pre-Made ASCII Art[​](<#tool-7-search-pre-made-ascii-art> "Direct link to Tool 7: Search Pre-Made ASCII Art")
Search curated ASCII art from the web. Use `terminal` with `curl`.
### Source A: ascii.co.uk (recommended for pre-made art)[​](<#source-a-asciicouk-recommended-for-pre-made-art> "Direct link to Source A: ascii.co.uk \(recommended for pre-made art\)")
Large collection of classic ASCII art organized by subject. Art is inside HTML `<pre>` tags. Fetch the page with curl, then extract art with a small Python snippet.
**URL pattern:** `https://ascii.co.uk/art/{subject}`
**Step 1 — Fetch the page:**
[code] 
    curl -s 'https://ascii.co.uk/art/cat' -o /tmp/ascii_art.html  
    
[/code]
**Step 2 — Extract art from pre tags:**
[code] 
    import re, html  
    with open('/tmp/ascii_art.html') as f:  
        text = f.read()  
    arts = re.findall(r'<pre[^>]*>(.*?)</pre>', text, re.DOTALL)  
    for art in arts:  
        clean = re.sub(r'<[^>]+>', '', art)  
        clean = html.unescape(clean).strip()  
        if len(clean) > 30:  
            print(clean)  
            print('\n---\n')  
    
[/code]
**Available subjects** (use as URL path):
  * Animals: `cat`, `dog`, `horse`, `bird`, `fish`, `dragon`, `snake`, `rabbit`, `elephant`, `dolphin`, `butterfly`, `owl`, `wolf`, `bear`, `penguin`, `turtle`
  * Objects: `car`, `ship`, `airplane`, `rocket`, `guitar`, `computer`, `coffee`, `beer`, `cake`, `house`, `castle`, `sword`, `crown`, `key`
  * Nature: `tree`, `flower`, `sun`, `moon`, `star`, `mountain`, `ocean`, `rainbow`
  * Characters: `skull`, `robot`, `angel`, `wizard`, `pirate`, `ninja`, `alien`
  * Holidays: `christmas`, `halloween`, `valentine`


**Tips:**
  * Preserve artist signatures/initials — important etiquette
  * Multiple art pieces per page — pick the best one for the user
  * Works reliably via curl, no JavaScript needed


### Source B: GitHub Octocat API (fun easter egg)[​](<#source-b-github-octocat-api-fun-easter-egg> "Direct link to Source B: GitHub Octocat API \(fun easter egg\)")
Returns a random GitHub Octocat with a wise quote. No auth needed.
[code] 
    curl -s https://api.github.com/octocat  
    
[/code]
## Tool 8: Fun ASCII Utilities (via curl)[​](<#tool-8-fun-ascii-utilities-via-curl> "Direct link to Tool 8: Fun ASCII Utilities \(via curl\)")
These free services return ASCII art directly — great for fun extras.
### QR Codes as ASCII Art[​](<#qr-codes-as-ascii-art> "Direct link to QR Codes as ASCII Art")
[code] 
    curl -s "qrenco.de/Hello+World"  
    curl -s "qrenco.de/https://example.com"  
    
[/code]
### Weather as ASCII Art[​](<#weather-as-ascii-art> "Direct link to Weather as ASCII Art")
[code] 
    curl -s "wttr.in/London"          # Full weather report with ASCII graphics  
    curl -s "wttr.in/Moon"            # Moon phase in ASCII art  
    curl -s "v2.wttr.in/London"       # Detailed version  
    
[/code]
## Tool 9: LLM-Generated Custom Art (Fallback)[​](<#tool-9-llm-generated-custom-art-fallback> "Direct link to Tool 9: LLM-Generated Custom Art \(Fallback\)")
When tools above don't have what's needed, generate ASCII art directly using these Unicode characters:
### Character Palette[​](<#character-palette> "Direct link to Character Palette")
**Box Drawing:** `╔ ╗ ╚ ╝ ║ ═ ╠ ╣ ╦ ╩ ╬ ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╰ ╯`
**Block Elements:** `░ ▒ ▓ █ ▄ ▀ ▌ ▐ ▖ ▗ ▘ ▝ ▚ ▞`
**Geometric & Symbols:** `◆ ◇ ◈ ● ○ ◉ ■ □ ▲ △ ▼ ▽ ★ ☆ ✦ ✧ ◀ ▶ ◁ ▷ ⬡ ⬢ ⌂`
### Rules[​](<#rules> "Direct link to Rules")
  * Max width: 60 characters per line (terminal-safe)
  * Max height: 15 lines for banners, 25 for scenes
  * Monospace only: output must render correctly in fixed-width fonts


## Decision Flow[​](<#decision-flow> "Direct link to Decision Flow")
  1. **Text as a banner** → pyfiglet if installed, otherwise asciified API via curl
  2. **Wrap a message in fun character art** → cowsay
  3. **Add decorative border/frame** → boxes (can combine with pyfiglet/asciified)
  4. **Art of a specific thing** (cat, rocket, dragon) → ascii.co.uk via curl + parsing
  5. **Convert an image to ASCII** → ascii-image-converter or jp2a
  6. **QR code** → qrenco.de via curl
  7. **Weather/moon art** → wttr.in via curl
  8. **Something custom/creative** → LLM generation with Unicode palette
  9. **Any tool not installed** → install it, or fall back to next option


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Tool 1: Text Banners (pyfiglet — local)](<#tool-1-text-banners-pyfiglet--local>)
    * [Setup](<#setup>)
    * [Usage](<#usage>)
    * [Recommended fonts](<#recommended-fonts>)
    * [Tips](<#tips>)
  * [Tool 2: Text Banners (asciified API — remote, no install)](<#tool-2-text-banners-asciified-api--remote-no-install>)
    * [Usage (via terminal curl)](<#usage-via-terminal-curl>)
    * [Tips](<#tips-1>)
  * [Tool 3: Cowsay (Message Art)](<#tool-3-cowsay-message-art>)
    * [Setup](<#setup-1>)
    * [Usage](<#usage-1>)
    * [Available characters (50+)](<#available-characters-50>)
    * [Eye/tongue modifiers](<#eyetongue-modifiers>)
  * [Tool 4: Boxes (Decorative Borders)](<#tool-4-boxes-decorative-borders>)
    * [Setup](<#setup-2>)
    * [Usage](<#usage-2>)
    * [Combine with pyfiglet or asciified](<#combine-with-pyfiglet-or-asciified>)
  * [Tool 5: TOIlet (Colored Text Art)](<#tool-5-toilet-colored-text-art>)
    * [Setup](<#setup-3>)
    * [Usage](<#usage-3>)
    * [Filters](<#filters>)
  * [Tool 6: Image to ASCII Art](<#tool-6-image-to-ascii-art>)
    * [Option A: ascii-image-converter (recommended, modern)](<#option-a-ascii-image-converter-recommended-modern>)
    * [Option B: jp2a (lightweight, JPEG only)](<#option-b-jp2a-lightweight-jpeg-only>)
  * [Tool 7: Search Pre-Made ASCII Art](<#tool-7-search-pre-made-ascii-art>)
    * [Source A: ascii.co.uk (recommended for pre-made art)](<#source-a-asciicouk-recommended-for-pre-made-art>)
    * [Source B: GitHub Octocat API (fun easter egg)](<#source-b-github-octocat-api-fun-easter-egg>)
  * [Tool 8: Fun ASCII Utilities (via curl)](<#tool-8-fun-ascii-utilities-via-curl>)
    * [QR Codes as ASCII Art](<#qr-codes-as-ascii-art>)
    * [Weather as ASCII Art](<#weather-as-ascii-art>)
  * [Tool 9: LLM-Generated Custom Art (Fallback)](<#tool-9-llm-generated-custom-art-fallback>)
    * [Character Palette](<#character-palette>)
    * [Rules](<#rules>)
  * [Decision Flow](<#decision-flow>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-ascii-art -->
