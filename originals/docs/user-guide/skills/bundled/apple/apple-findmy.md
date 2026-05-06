On this page
Track Apple devices/AirTags via FindMy.app on macOS.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/apple/findmy`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Platforms| macos  
Tags| `FindMy`, `AirTag`, `location`, `tracking`, `macOS`, `Apple`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Find My (Apple)
Track Apple devices and AirTags via the FindMy.app on macOS. Since Apple doesn't provide a CLI for FindMy, this skill uses AppleScript to open the app and screen capture to read device locations.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **macOS** with Find My app and iCloud signed in
  * Devices/AirTags already registered in Find My
  * Screen Recording permission for terminal (System Settings → Privacy → Screen Recording)
  * **Optional but recommended** : Install `peekaboo` for better UI automation: `brew install steipete/tap/peekaboo`


## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * User asks "where is my [device/cat/keys/bag]?"
  * Tracking AirTag locations
  * Checking device locations (iPhone, iPad, Mac, AirPods)
  * Monitoring pet or item movement over time (AirTag patrol routes)


## Method 1: AppleScript + Screenshot (Basic)[​](<#method-1-applescript--screenshot-basic> "Direct link to Method 1: AppleScript + Screenshot \(Basic\)")
### Open FindMy and Navigate[​](<#open-findmy-and-navigate> "Direct link to Open FindMy and Navigate")
[code] 
    # Open Find My app  
    osascript -e 'tell application "FindMy" to activate'  
      
    # Wait for it to load  
    sleep 3  
      
    # Take a screenshot of the Find My window  
    screencapture -w -o /tmp/findmy.png  
    
[/code]
Then use `vision_analyze` to read the screenshot:
[code] 
    vision_analyze(image_url="/tmp/findmy.png", question="What devices/items are shown and what are their locations?")  
    
[/code]
### Switch Between Tabs[​](<#switch-between-tabs> "Direct link to Switch Between Tabs")
[code] 
    # Switch to Devices tab  
    osascript -e '  
    tell application "System Events"  
        tell process "FindMy"  
            click button "Devices" of toolbar 1 of window 1  
        end tell  
    end tell'  
      
    # Switch to Items tab (AirTags)  
    osascript -e '  
    tell application "System Events"  
        tell process "FindMy"  
            click button "Items" of toolbar 1 of window 1  
        end tell  
    end tell'  
    
[/code]
## Method 2: Peekaboo UI Automation (Recommended)[​](<#method-2-peekaboo-ui-automation-recommended> "Direct link to Method 2: Peekaboo UI Automation \(Recommended\)")
If `peekaboo` is installed, use it for more reliable UI interaction:
[code] 
    # Open Find My  
    osascript -e 'tell application "FindMy" to activate'  
    sleep 3  
      
    # Capture and annotate the UI  
    peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png  
      
    # Click on a specific device/item by element ID  
    peekaboo click --on B3 --app "FindMy"  
      
    # Capture the detail view  
    peekaboo image --app "FindMy" --path /tmp/findmy-detail.png  
    
[/code]
Then analyze with vision:
[code] 
    vision_analyze(image_url="/tmp/findmy-detail.png", question="What is the location shown for this device/item? Include address and coordinates if visible.")  
    
[/code]
## Workflow: Track AirTag Location Over Time[​](<#workflow-track-airtag-location-over-time> "Direct link to Workflow: Track AirTag Location Over Time")
For monitoring an AirTag (e.g., tracking a cat's patrol route):
[code] 
    # 1. Open FindMy to Items tab  
    osascript -e 'tell application "FindMy" to activate'  
    sleep 3  
      
    # 2. Click on the AirTag item (stay on page — AirTag only updates when page is open)  
      
    # 3. Periodically capture location  
    while true; do  
        screencapture -w -o /tmp/findmy-$(date +%H%M%S).png  
        sleep 300  # Every 5 minutes  
    done  
    
[/code]
Analyze each screenshot with vision to extract coordinates, then compile a route.
## Limitations[​](<#limitations> "Direct link to Limitations")
  * FindMy has **no CLI or API** — must use UI automation
  * AirTags only update location while the FindMy page is actively displayed
  * Location accuracy depends on nearby Apple devices in the FindMy network
  * Screen Recording permission required for screenshots
  * AppleScript UI automation may break across macOS versions


## Rules[​](<#rules> "Direct link to Rules")
  1. Keep FindMy app in the foreground when tracking AirTags (updates stop when minimized)
  2. Use `vision_analyze` to read screenshot content — don't try to parse pixels
  3. For ongoing tracking, use a cronjob to periodically capture and log locations
  4. Respect privacy — only track devices/items the user owns


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [When to Use](<#when-to-use>)
  * [Method 1: AppleScript + Screenshot (Basic)](<#method-1-applescript--screenshot-basic>)
    * [Open FindMy and Navigate](<#open-findmy-and-navigate>)
    * [Switch Between Tabs](<#switch-between-tabs>)
  * [Method 2: Peekaboo UI Automation (Recommended)](<#method-2-peekaboo-ui-automation-recommended>)
  * [Workflow: Track AirTag Location Over Time](<#workflow-track-airtag-location-over-time>)
  * [Limitations](<#limitations>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/apple/apple-findmy -->
