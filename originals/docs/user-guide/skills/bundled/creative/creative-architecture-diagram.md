On this page
Dark-themed SVG architecture/cloud/infra diagrams as HTML.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/creative/architecture-diagram`  
Version| `1.0.0`  
Author| Cocoon AI ([hello@cocoon-ai.com](<mailto:hello@cocoon-ai.com>)), ported by Hermes Agent  
License| MIT  
Tags| `architecture`, `diagrams`, `SVG`, `HTML`, `visualization`, `infrastructure`, `cloud`  
Related skills| [`concept-diagrams`](</docs/user-guide/skills/optional/creative/creative-concept-diagrams>), [`excalidraw`](</docs/user-guide/skills/bundled/creative/creative-excalidraw>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Architecture Diagram Skill
Generate professional, dark-themed technical architecture diagrams as standalone HTML files with inline SVG graphics. No external tools, no API keys, no rendering libraries — just write the HTML file and open it in a browser.
## Scope[​](<#scope> "Direct link to Scope")
**Best suited for:**
  * Software system architecture (frontend / backend / database layers)
  * Cloud infrastructure (VPC, regions, subnets, managed services)
  * Microservice / service-mesh topology
  * Database + API map, deployment diagrams
  * Anything with a tech-infra subject that fits a dark, grid-backed aesthetic


**Look elsewhere first for:**
  * Physics, chemistry, math, biology, or other scientific subjects
  * Physical objects (vehicles, hardware, anatomy, cross-sections)
  * Floor plans, narrative journeys, educational / textbook-style visuals
  * Hand-drawn whiteboard sketches (consider `excalidraw`)
  * Animated explainers (consider an animation skill)


If a more specialized skill is available for the subject, prefer that. If none fits, this skill can also serve as a general SVG diagram fallback — the output will just carry the dark tech aesthetic described below.
Based on [Cocoon AI's architecture-diagram-generator](<https://github.com/Cocoon-AI/architecture-diagram-generator>) (MIT).
## Workflow[​](<#workflow> "Direct link to Workflow")
  1. User describes their system architecture (components, connections, technologies)
  2. Generate the HTML file following the design system below
  3. Save with `write_file` to a `.html` file (e.g. `~/architecture-diagram.html`)
  4. User opens in any browser — works offline, no dependencies


### Output Location[​](<#output-location> "Direct link to Output Location")
Save diagrams to a user-specified path, or default to the current working directory:
[code] 
    ./[project-name]-architecture.html  
    
[/code]
### Preview[​](<#preview> "Direct link to Preview")
After saving, suggest the user open it:
[code] 
    # macOS  
    open ./my-architecture.html  
    # Linux  
    xdg-open ./my-architecture.html  
    
[/code]
## Design System & Visual Language[​](<#design-system--visual-language> "Direct link to Design System & Visual Language")
### Color Palette (Semantic Mapping)[​](<#color-palette-semantic-mapping> "Direct link to Color Palette \(Semantic Mapping\)")
Use specific `rgba` fills and hex strokes to categorize components:
Component Type| Fill (rgba)| Stroke (Hex)  
---|---|---  
**Frontend**| `rgba(8, 51, 68, 0.4)`| `#22d3ee` (cyan-400)  
**Backend**| `rgba(6, 78, 59, 0.4)`| `#34d399` (emerald-400)  
**Database**| `rgba(76, 29, 149, 0.4)`| `#a78bfa` (violet-400)  
**AWS/Cloud**| `rgba(120, 53, 15, 0.3)`| `#fbbf24` (amber-400)  
**Security**| `rgba(136, 19, 55, 0.4)`| `#fb7185` (rose-400)  
**Message Bus**| `rgba(251, 146, 60, 0.3)`| `#fb923c` (orange-400)  
**External**| `rgba(30, 41, 59, 0.5)`| `#94a3b8` (slate-400)  
### Typography & Background[​](<#typography--background> "Direct link to Typography & Background")
  * **Font:** JetBrains Mono (Monospace), loaded from Google Fonts
  * **Sizes:** 12px (Names), 9px (Sublabels), 8px (Annotations), 7px (Tiny labels)
  * **Background:** Slate-950 (`#020617`) with a subtle 40px grid pattern


[code] 
    <!-- Background Grid Pattern -->  
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">  
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>  
    </pattern>  
    
[/code]
## Technical Implementation Details[​](<#technical-implementation-details> "Direct link to Technical Implementation Details")
### Component Rendering[​](<#component-rendering> "Direct link to Component Rendering")
Components are rounded rectangles (`rx="6"`) with 1.5px strokes. To prevent arrows from showing through semi-transparent fills, use a **double-rect masking technique** :
  1. Draw an opaque background rect (`#0f172a`)
  2. Draw the semi-transparent styled rect on top


### Connection Rules[​](<#connection-rules> "Direct link to Connection Rules")
  * **Z-Order:** Draw arrows _early_ in the SVG (after the grid) so they render behind component boxes
  * **Arrowheads:** Defined via SVG markers
  * **Security Flows:** Use dashed lines in rose color (`#fb7185`)
  * **Boundaries:**
    * _Security Groups:_ Dashed (`4,4`), rose color
    * _Regions:_ Large dashed (`8,4`), amber color, `rx="12"`


### Spacing & Layout Logic[​](<#spacing--layout-logic> "Direct link to Spacing & Layout Logic")
  * **Standard Height:** 60px (Services); 80-120px (Large components)
  * **Vertical Gap:** Minimum 40px between components
  * **Message Buses:** Must be placed _in the gap_ between services, not overlapping them
  * **Legend Placement:** **CRITICAL.** Must be placed outside all boundary boxes. Calculate the lowest Y-coordinate of all boundaries and place the legend at least 20px below it.


## Document Structure[​](<#document-structure> "Direct link to Document Structure")
The generated HTML file follows a four-part layout:
  1. **Header:** Title with a pulsing dot indicator and subtitle
  2. **Main SVG:** The diagram contained within a rounded border card
  3. **Summary Cards:** A grid of three cards below the diagram for high-level details
  4. **Footer:** Minimal metadata


### Info Card Pattern[​](<#info-card-pattern> "Direct link to Info Card Pattern")
[code] 
    <div class="card">  
      <div class="card-header">  
        <div class="card-dot cyan"></div>  
        <h3>Title</h3>  
      </div>  
      <ul>  
        <li>• Item one</li>  
        <li>• Item two</li>  
      </ul>  
    </div>  
    
[/code]
## Output Requirements[​](<#output-requirements> "Direct link to Output Requirements")
  * **Single File:** One self-contained `.html` file
  * **No External Dependencies:** All CSS and SVG must be inline (except Google Fonts)
  * **No JavaScript:** Use pure CSS for any animations (like pulsing dots)
  * **Compatibility:** Must render correctly in any modern web browser


## Template Reference[​](<#template-reference> "Direct link to Template Reference")
Load the full HTML template for the exact structure, CSS, and SVG component examples:
[code] 
    skill_view(name="architecture-diagram", file_path="templates/template.html")  
    
[/code]
The template contains working examples of every component type (frontend, backend, database, cloud, security), arrow styles (standard, dashed, curved), security groups, region boundaries, and the legend — use it as your structural reference when generating diagrams.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Scope](<#scope>)
  * [Workflow](<#workflow>)
    * [Output Location](<#output-location>)
    * [Preview](<#preview>)
  * [Design System & Visual Language](<#design-system--visual-language>)
    * [Color Palette (Semantic Mapping)](<#color-palette-semantic-mapping>)
    * [Typography & Background](<#typography--background>)
  * [Technical Implementation Details](<#technical-implementation-details>)
    * [Component Rendering](<#component-rendering>)
    * [Connection Rules](<#connection-rules>)
    * [Spacing & Layout Logic](<#spacing--layout-logic>)
  * [Document Structure](<#document-structure>)
    * [Info Card Pattern](<#info-card-pattern>)
  * [Output Requirements](<#output-requirements>)
  * [Template Reference](<#template-reference>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-architecture-diagram -->
