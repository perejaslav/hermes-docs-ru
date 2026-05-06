On this page
SiYuan Note API for searching, reading, creating, and managing blocks and documents in a self-hosted knowledge base via curl.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/productivity/siyuan`  
Path| `optional-skills/productivity/siyuan`  
Version| `1.0.0`  
Author| FEUAZUR  
License| MIT  
Tags| `SiYuan`, `Notes`, `Knowledge Base`, `PKM`, `API`  
Related skills| [`obsidian`](</docs/user-guide/skills/bundled/note-taking/note-taking-obsidian>), [`notion`](</docs/user-guide/skills/bundled/productivity/productivity-notion>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# SiYuan Note API
Use the [SiYuan](<https://github.com/siyuan-note/siyuan>) kernel API via curl to search, read, create, update, and delete blocks and documents in a self-hosted knowledge base. No extra tools needed -- just curl and an API token.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  1. Install and run SiYuan (desktop or Docker)
  2. Get your API token: **Settings > About > API token**
  3. Store it in `~/.hermes/.env`:
[code] SIYUAN_TOKEN=your_token_here  
         SIYUAN_URL=http://127.0.0.1:6806  
         
[/code]
`SIYUAN_URL` defaults to `http://127.0.0.1:6806` if not set.


## API Basics[​](<#api-basics> "Direct link to API Basics")
All SiYuan API calls are **POST with JSON body**. Every request follows this pattern:
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/..." \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"param": "value"}'  
    
[/code]
Responses are JSON with this structure:
[code] 
    {"code": 0, "msg": "", "data": { ... }}  
    
[/code]
`code: 0` means success. Any other value is an error -- check `msg` for details.
**ID format:** SiYuan IDs look like `20210808180117-6v0mkxr` (14-digit timestamp + 7 alphanumeric chars).
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
Operation| Endpoint  
---|---  
Full-text search| `/api/search/fullTextSearchBlock`  
SQL query| `/api/query/sql`  
Read block| `/api/block/getBlockKramdown`  
Read children| `/api/block/getChildBlocks`  
Get path| `/api/filetree/getHPathByID`  
Get attributes| `/api/attr/getBlockAttrs`  
List notebooks| `/api/notebook/lsNotebooks`  
List documents| `/api/filetree/listDocsByPath`  
Create notebook| `/api/notebook/createNotebook`  
Create document| `/api/filetree/createDocWithMd`  
Append block| `/api/block/appendBlock`  
Update block| `/api/block/updateBlock`  
Rename document| `/api/filetree/renameDocByID`  
Set attributes| `/api/attr/setBlockAttrs`  
Delete block| `/api/block/deleteBlock`  
Delete document| `/api/filetree/removeDocByID`  
Export as Markdown| `/api/export/exportMdContent`  
## Common Operations[​](<#common-operations> "Direct link to Common Operations")
### Search (Full-Text)[​](<#search-full-text> "Direct link to Search \(Full-Text\)")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/search/fullTextSearchBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "meeting notes", "page": 0}' | jq '.data.blocks[:5]'  
    
[/code]
### Search (SQL)[​](<#search-sql> "Direct link to Search \(SQL\)")
Query the blocks database directly. Only SELECT statements are safe.
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/query/sql" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"stmt": "SELECT id, content, type, box FROM blocks WHERE content LIKE '\''%keyword%'\'' AND type='\''p'\'' LIMIT 20"}' | jq '.data'  
    
[/code]
Useful columns: `id`, `parent_id`, `root_id`, `box` (notebook ID), `path`, `content`, `type`, `subtype`, `created`, `updated`.
### Read Block Content[​](<#read-block-content> "Direct link to Read Block Content")
Returns block content in Kramdown (Markdown-like) format.
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getBlockKramdown" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data.kramdown'  
    
[/code]
### Read Child Blocks[​](<#read-child-blocks> "Direct link to Read Child Blocks")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getChildBlocks" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'  
    
[/code]
### Get Human-Readable Path[​](<#get-human-readable-path> "Direct link to Get Human-Readable Path")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/getHPathByID" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'  
    
[/code]
### Get Block Attributes[​](<#get-block-attributes> "Direct link to Get Block Attributes")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/getBlockAttrs" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'  
    
[/code]
### List Notebooks[​](<#list-notebooks> "Direct link to List Notebooks")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/lsNotebooks" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{}' | jq '.data.notebooks[] | {id, name, closed}'  
    
[/code]
### List Documents in a Notebook[​](<#list-documents-in-a-notebook> "Direct link to List Documents in a Notebook")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/listDocsByPath" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"notebook": "NOTEBOOK_ID", "path": "/"}' | jq '.data.files[] | {id, name}'  
    
[/code]
### Create a Document[​](<#create-a-document> "Direct link to Create a Document")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/createDocWithMd" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "notebook": "NOTEBOOK_ID",  
        "path": "/Meeting Notes/2026-03-22",  
        "markdown": "# Meeting Notes\n\n- Discussed project timeline\n- Assigned tasks"  
      }' | jq '.data'  
    
[/code]
### Create a Notebook[​](<#create-a-notebook> "Direct link to Create a Notebook")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/createNotebook" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"name": "My New Notebook"}' | jq '.data.notebook.id'  
    
[/code]
### Append Block to Document[​](<#append-block-to-document> "Direct link to Append Block to Document")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/appendBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "parentID": "DOCUMENT_OR_BLOCK_ID",  
        "data": "New paragraph added at the end.",  
        "dataType": "markdown"  
      }' | jq '.data'  
    
[/code]
Also available: `/api/block/prependBlock` (same params, inserts at the beginning) and `/api/block/insertBlock` (uses `previousID` instead of `parentID` to insert after a specific block).
### Update Block Content[​](<#update-block-content> "Direct link to Update Block Content")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/updateBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "id": "BLOCK_ID",  
        "data": "Updated content here.",  
        "dataType": "markdown"  
      }' | jq '.data'  
    
[/code]
### Rename a Document[​](<#rename-a-document> "Direct link to Rename a Document")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/renameDocByID" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "DOCUMENT_ID", "title": "New Title"}'  
    
[/code]
### Set Block Attributes[​](<#set-block-attributes> "Direct link to Set Block Attributes")
Custom attributes must be prefixed with `custom-`:
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/setBlockAttrs" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "id": "BLOCK_ID",  
        "attrs": {  
          "custom-status": "reviewed",  
          "custom-priority": "high"  
        }  
      }'  
    
[/code]
### Delete a Block[​](<#delete-a-block> "Direct link to Delete a Block")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/deleteBlock" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "BLOCK_ID"}'  
    
[/code]
To delete a whole document: use `/api/filetree/removeDocByID` with `{"id": "DOC_ID"}`. To delete a notebook: use `/api/notebook/removeNotebook` with `{"notebook": "NOTEBOOK_ID"}`.
### Export Document as Markdown[​](<#export-document-as-markdown> "Direct link to Export Document as Markdown")
[code] 
    curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/export/exportMdContent" \  
      -H "Authorization: Token $SIYUAN_TOKEN" \  
      -H "Content-Type: application/json" \  
      -d '{"id": "DOCUMENT_ID"}' | jq -r '.data.content'  
    
[/code]
## Block Types[​](<#block-types> "Direct link to Block Types")
Common `type` values in SQL queries:
Type| Description  
---|---  
`d`| Document (root block)  
`p`| Paragraph  
`h`| Heading  
`l`| List  
`i`| List item  
`c`| Code block  
`m`| Math block  
`t`| Table  
`b`| Blockquote  
`s`| Super block  
`html`| HTML block  
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **All endpoints are POST** \-- even read-only operations. Do not use GET.
  * **SQL safety** : only use SELECT queries. INSERT/UPDATE/DELETE/DROP are dangerous and should never be sent.
  * **ID validation** : IDs match the pattern `YYYYMMDDHHmmss-xxxxxxx`. Reject anything else.
  * **Error responses** : always check `code != 0` in responses before processing `data`.
  * **Large documents** : block content and export results can be very large. Use `LIMIT` in SQL and pipe through `jq` to extract only what you need.
  * **Notebook IDs** : when working with a specific notebook, get its ID first via `lsNotebooks`.


## Alternative: MCP Server[​](<#alternative-mcp-server> "Direct link to Alternative: MCP Server")
If you prefer a native integration instead of curl, install the SiYuan MCP server:
[code] 
    # In ~/.hermes/config.yaml under mcp_servers:  
    mcp_servers:  
      siyuan:  
        command: npx  
        args: ["-y", "@porkll/siyuan-mcp"]  
        env:  
          SIYUAN_TOKEN: "your_token"  
          SIYUAN_URL: "http://127.0.0.1:6806"  
    
[/code]
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [API Basics](<#api-basics>)
  * [Quick Reference](<#quick-reference>)
  * [Common Operations](<#common-operations>)
    * [Search (Full-Text)](<#search-full-text>)
    * [Search (SQL)](<#search-sql>)
    * [Read Block Content](<#read-block-content>)
    * [Read Child Blocks](<#read-child-blocks>)
    * [Get Human-Readable Path](<#get-human-readable-path>)
    * [Get Block Attributes](<#get-block-attributes>)
    * [List Notebooks](<#list-notebooks>)
    * [List Documents in a Notebook](<#list-documents-in-a-notebook>)
    * [Create a Document](<#create-a-document>)
    * [Create a Notebook](<#create-a-notebook>)
    * [Append Block to Document](<#append-block-to-document>)
    * [Update Block Content](<#update-block-content>)
    * [Rename a Document](<#rename-a-document>)
    * [Set Block Attributes](<#set-block-attributes>)
    * [Delete a Block](<#delete-a-block>)
    * [Export Document as Markdown](<#export-document-as-markdown>)
  * [Block Types](<#block-types>)
  * [Pitfalls](<#pitfalls>)
  * [Alternative: MCP Server](<#alternative-mcp-server>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-siyuan -->
