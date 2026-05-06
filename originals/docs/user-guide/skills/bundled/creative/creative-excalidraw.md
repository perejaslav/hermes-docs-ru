On this page
Hand-drawn Excalidraw JSON diagrams (arch, flow, seq).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/creative/excalidraw`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Tags| `Excalidraw`, `Diagrams`, `Flowcharts`, `Architecture`, `Visualization`, `JSON`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Excalidraw Diagram Skill
Create diagrams by writing standard Excalidraw element JSON and saving as `.excalidraw` files. These files can be drag-and-dropped onto [excalidraw.com](<https://excalidraw.com>) for viewing and editing. No accounts, no API keys, no rendering libraries -- just JSON.
## When to use[​](<#when-to-use> "Direct link to When to use")
Generate `.excalidraw` files for architecture diagrams, flowcharts, sequence diagrams, concept maps, and more. Files can be opened at excalidraw.com or uploaded for shareable links.
## Workflow[​](<#workflow> "Direct link to Workflow")
  1. **Load this skill** (you already did)
  2. **Write the elements JSON** \-- an array of Excalidraw element objects
  3. **Save the file** using `write_file` to create a `.excalidraw` file
  4. **Optionally upload** for a shareable link using `scripts/upload.py` via `terminal`


### Saving a Diagram[​](<#saving-a-diagram> "Direct link to Saving a Diagram")
Wrap your elements array in the standard `.excalidraw` envelope and save with `write_file`:
[code] 
    {  
      "type": "excalidraw",  
      "version": 2,  
      "source": "hermes-agent",  
      "elements": [ ...your elements array here... ],  
      "appState": {  
        "viewBackgroundColor": "#ffffff"  
      }  
    }  
    
[/code]
Save to any path, e.g. `~/diagrams/my_diagram.excalidraw`.
### Uploading for a Shareable Link[​](<#uploading-for-a-shareable-link> "Direct link to Uploading for a Shareable Link")
Run the upload script (located in this skill's `scripts/` directory) via terminal:
[code] 
    python skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw  
    
[/code]
This uploads to excalidraw.com (no account needed) and prints a shareable URL. Requires the `cryptography` pip package (`pip install cryptography`).
* * *
## Element Format Reference[​](<#element-format-reference> "Direct link to Element Format Reference")
### Required Fields (all elements)[​](<#required-fields-all-elements> "Direct link to Required Fields \(all elements\)")
`type`, `id` (unique string), `x`, `y`, `width`, `height`
### Defaults (skip these -- they're applied automatically)[​](<#defaults-skip-these----theyre-applied-automatically> "Direct link to Defaults \(skip these -- they're applied automatically\)")
  * `strokeColor`: `"#1e1e1e"`
  * `backgroundColor`: `"transparent"`
  * `fillStyle`: `"solid"`
  * `strokeWidth`: `2`
  * `roughness`: `1` (hand-drawn look)
  * `opacity`: `100`


Canvas background is white.
### Element Types[​](<#element-types> "Direct link to Element Types")
**Rectangle** :
[code] 
    { "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }  
    
[/code]
  * `roundness: { "type": 3 }` for rounded corners
  * `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled


**Ellipse** :
[code] 
    { "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }  
    
[/code]
**Diamond** :
[code] 
    { "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }  
    
[/code]
**Labeled shape (container binding)** \-- create a text element bound to the shape:
> **WARNING:** Do NOT use `"label": { "text": "..." }` on shapes. This is NOT a valid Excalidraw property and will be silently ignored, producing blank shapes. You MUST use the container binding approach below.
The shape needs `boundElements` listing the text, and the text needs `containerId` pointing back:
[code] 
    { "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,  
      "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",  
      "boundElements": [{ "id": "t_r1", "type": "text" }] },  
    { "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,  
      "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",  
      "textAlign": "center", "verticalAlign": "middle",  
      "containerId": "r1", "originalText": "Hello", "autoResize": true }  
    
[/code]
  * Works on rectangle, ellipse, diamond
  * Text is auto-centered by Excalidraw when `containerId` is set
  * The text `x`/`y`/`width`/`height` are approximate -- Excalidraw recalculates them on load
  * `originalText` should match `text`
  * Always include `fontFamily: 1` (Virgil/hand-drawn font)


**Labeled arrow** \-- same container binding approach:
[code] 
    { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,  
      "points": [[0,0],[200,0]], "endArrowhead": "arrow",  
      "boundElements": [{ "id": "t_a1", "type": "text" }] },  
    { "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,  
      "text": "connects", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",  
      "textAlign": "center", "verticalAlign": "middle",  
      "containerId": "a1", "originalText": "connects", "autoResize": true }  
    
[/code]
**Standalone text** (titles and annotations only -- no container):
[code] 
    { "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20,  
      "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Hello", "autoResize": true }  
    
[/code]
  * `x` is the LEFT edge. To center at position `cx`: `x = cx - (text.length * fontSize * 0.5) / 2`
  * Do NOT rely on `textAlign` or `width` for positioning


**Arrow** :
[code] 
    { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,  
      "points": [[0,0],[200,0]], "endArrowhead": "arrow" }  
    
[/code]
  * `points`: `[dx, dy]` offsets from element `x`, `y`
  * `endArrowhead`: `null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
  * `strokeStyle`: `"solid"` (default) | `"dashed"` | `"dotted"`


### Arrow Bindings (connect arrows to shapes)[​](<#arrow-bindings-connect-arrows-to-shapes> "Direct link to Arrow Bindings \(connect arrows to shapes\)")
[code] 
    {  
      "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,  
      "points": [[0,0],[150,0]], "endArrowhead": "arrow",  
      "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },  
      "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }  
    }  
    
[/code]
`fixedPoint` coordinates: `top=[0.5,0]`, `bottom=[0.5,1]`, `left=[0,0.5]`, `right=[1,0.5]`
### Drawing Order (z-order)[​](<#drawing-order-z-order> "Direct link to Drawing Order \(z-order\)")
  * Array order = z-order (first = back, last = front)
  * Emit progressively: background zones → shape → its bound text → its arrows → next shape
  * BAD: all rectangles, then all texts, then all arrows
  * GOOD: bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
  * Always place the bound text element immediately after its container shape


### Sizing Guidelines[​](<#sizing-guidelines> "Direct link to Sizing Guidelines")
**Font sizes:**
  * Minimum `fontSize`: **16** for body text, labels, descriptions
  * Minimum `fontSize`: **20** for titles and headings
  * Minimum `fontSize`: **14** for secondary annotations only (sparingly)
  * NEVER use `fontSize` below 14


**Element sizes:**
  * Minimum shape size: 120x60 for labeled rectangles/ellipses
  * Leave 20-30px gaps between elements minimum
  * Prefer fewer, larger elements over many tiny ones


### Color Palette[​](<#color-palette> "Direct link to Color Palette")
See `references/colors.md` for full color tables. Quick reference:
Use| Fill Color| Hex  
---|---|---  
Primary / Input| Light Blue| `#a5d8ff`  
Success / Output| Light Green| `#b2f2bb`  
Warning / External| Light Orange| `#ffd8a8`  
Processing / Special| Light Purple| `#d0bfff`  
Error / Critical| Light Red| `#ffc9c9`  
Notes / Decisions| Light Yellow| `#fff3bf`  
Storage / Data| Light Teal| `#c3fae8`  
### Tips[​](<#tips> "Direct link to Tips")
  * Use the color palette consistently across the diagram
  * **Text contrast is CRITICAL** \-- never use light gray on white backgrounds. Minimum text color on white: `#757575`
  * Do NOT use emoji in text -- they don't render in Excalidraw's font
  * For dark mode diagrams, see `references/dark-mode.md`
  * For larger examples, see `references/examples.md`


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Workflow](<#workflow>)
    * [Saving a Diagram](<#saving-a-diagram>)
    * [Uploading for a Shareable Link](<#uploading-for-a-shareable-link>)
  * [Element Format Reference](<#element-format-reference>)
    * [Required Fields (all elements)](<#required-fields-all-elements>)
    * [Defaults (skip these -- they're applied automatically)](<#defaults-skip-these----theyre-applied-automatically>)
    * [Element Types](<#element-types>)
    * [Arrow Bindings (connect arrows to shapes)](<#arrow-bindings-connect-arrows-to-shapes>)
    * [Drawing Order (z-order)](<#drawing-order-z-order>)
    * [Sizing Guidelines](<#sizing-guidelines>)
    * [Color Palette](<#color-palette>)
    * [Tips](<#tips>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-excalidraw -->
