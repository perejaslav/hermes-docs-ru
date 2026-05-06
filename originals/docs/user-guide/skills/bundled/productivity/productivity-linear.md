On this page
Linear: manage issues, projects, teams via GraphQL + curl.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/productivity/linear`  
Version| `1.0.0`  
Author| Hermes Agent  
License| MIT  
Tags| `Linear`, `Project Management`, `Issues`, `GraphQL`, `API`, `Productivity`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Linear — Issue & Project Management
Manage Linear issues, projects, and teams directly via the GraphQL API using `curl`. No MCP server, no OAuth flow, no extra dependencies.
## Setup[​](<#setup> "Direct link to Setup")
  1. Get a personal API key from **Linear Settings > Account > Security & access > Personal API keys** (URL: <https://linear.app/settings/account/security>). Note: the org-level _Settings > API_ page only shows OAuth apps and workspace-member keys, not personal keys.
  2. Set `LINEAR_API_KEY` in your environment (via `hermes setup` or your env config)


## API Basics[​](<#api-basics> "Direct link to API Basics")
  * **Endpoint:** `https://api.linear.app/graphql` (POST)
  * **Auth header:** `Authorization: $LINEAR_API_KEY` (no "Bearer" prefix for API keys)
  * **All requests are POST** with `Content-Type: application/json`
  * **Both UUIDs and short identifiers** (e.g., `ENG-123`) work for `issue(id:)`


Base curl pattern:
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ viewer { id name } }"}' | python3 -m json.tool  
    
[/code]
## Python helper script (ergonomic alternative)[​](<#python-helper-script-ergonomic-alternative> "Direct link to Python helper script \(ergonomic alternative\)")
For faster one-liners that don't need hand-written GraphQL, this skill ships a stdlib Python CLI at `scripts/linear_api.py`. Zero dependencies. Same auth (reads `LINEAR_API_KEY`).
[code] 
    SCRIPT=$(dirname "$(find ~/.hermes -path '*skills/productivity/linear/scripts/linear_api.py' 2>/dev/null | head -1)")/linear_api.py  
      
    python3 "$SCRIPT" whoami  
    python3 "$SCRIPT" list-teams  
    python3 "$SCRIPT" get-issue ENG-42  
    python3 "$SCRIPT" get-document 38359beef67c      # fetch a doc by slugId from the URL  
    python3 "$SCRIPT" raw 'query { viewer { name } }'  
    
[/code]
All subcommands: `whoami`, `list-teams`, `list-projects`, `list-states`, `list-issues`, `get-issue`, `search-issues`, `create-issue`, `update-issue`, `update-status`, `add-comment`, `list-documents`, `get-document`, `search-documents`, `raw`. Run with `--help` for flags.
Use the script when: you want a quick answer without crafting GraphQL. Use curl when: you need a query the script doesn't wrap, or you want to compose filters inline.
## Workflow States[​](<#workflow-states> "Direct link to Workflow States")
Linear uses `WorkflowState` objects with a `type` field. **6 state types:**
Type| Description  
---|---  
`triage`| Incoming issues needing review  
`backlog`| Acknowledged but not yet planned  
`unstarted`| Planned/ready but not started  
`started`| Actively being worked on  
`completed`| Done  
`canceled`| Won't do  
Each team has its own named states (e.g., "In Progress" is type `started`). To change an issue's status, you need the `stateId` (UUID) of the target state — query workflow states first.
**Priority values:** 0 = None, 1 = Urgent, 2 = High, 3 = Medium, 4 = Low
## Common Queries[​](<#common-queries> "Direct link to Common Queries")
### Get current user[​](<#get-current-user> "Direct link to Get current user")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ viewer { id name email } }"}' | python3 -m json.tool  
    
[/code]
### List teams[​](<#list-teams> "Direct link to List teams")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ teams { nodes { id name key } } }"}' | python3 -m json.tool  
    
[/code]
### List workflow states for a team[​](<#list-workflow-states-for-a-team> "Direct link to List workflow states for a team")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ workflowStates(filter: { team: { key: { eq: \"ENG\" } } }) { nodes { id name type } } }"}' | python3 -m json.tool  
    
[/code]
### List issues (first 20)[​](<#list-issues-first-20> "Direct link to List issues \(first 20\)")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issues(first: 20) { nodes { identifier title priority state { name type } assignee { name } team { key } url } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool  
    
[/code]
### List my assigned issues[​](<#list-my-assigned-issues> "Direct link to List my assigned issues")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ viewer { assignedIssues(first: 25) { nodes { identifier title state { name type } priority url } } } }"}' | python3 -m json.tool  
    
[/code]
### Get a single issue (by identifier like ENG-123)[​](<#get-a-single-issue-by-identifier-like-eng-123> "Direct link to Get a single issue \(by identifier like ENG-123\)")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issue(id: \"ENG-123\") { id identifier title description priority state { id name type } assignee { id name } team { key } project { name } labels { nodes { name } } comments { nodes { body user { name } createdAt } } url } }"}' | python3 -m json.tool  
    
[/code]
### Search issues by text[​](<#search-issues-by-text> "Direct link to Search issues by text")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issueSearch(query: \"bug login\", first: 10) { nodes { identifier title state { name } assignee { name } url } } }"}' | python3 -m json.tool  
    
[/code]
### Filter issues by state type[​](<#filter-issues-by-state-type> "Direct link to Filter issues by state type")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issues(filter: { state: { type: { in: [\"started\"] } } }, first: 20) { nodes { identifier title state { name } assignee { name } } } }"}' | python3 -m json.tool  
    
[/code]
### Filter by team and assignee[​](<#filter-by-team-and-assignee> "Direct link to Filter by team and assignee")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issues(filter: { team: { key: { eq: \"ENG\" } }, assignee: { email: { eq: \"user@example.com\" } } }, first: 20) { nodes { identifier title state { name } priority } } }"}' | python3 -m json.tool  
    
[/code]
### List projects[​](<#list-projects> "Direct link to List projects")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ projects(first: 20) { nodes { id name description progress lead { name } teams { nodes { key } } url } } }"}' | python3 -m json.tool  
    
[/code]
### List team members[​](<#list-team-members> "Direct link to List team members")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ users { nodes { id name email active } } }"}' | python3 -m json.tool  
    
[/code]
### List labels[​](<#list-labels> "Direct link to List labels")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issueLabels { nodes { id name color } } }"}' | python3 -m json.tool  
    
[/code]
## Common Mutations[​](<#common-mutations> "Direct link to Common Mutations")
### Create an issue[​](<#create-an-issue> "Direct link to Create an issue")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "query": "mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }",  
        "variables": {  
          "input": {  
            "teamId": "TEAM_UUID",  
            "title": "Fix login bug",  
            "description": "Users cannot login with SSO",  
            "priority": 2  
          }  
        }  
      }' | python3 -m json.tool  
    
[/code]
### Update issue status[​](<#update-issue-status> "Direct link to Update issue status")
First get the target state UUID from the workflow states query above, then:
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { stateId: \"STATE_UUID\" }) { success issue { identifier state { name type } } } }"}' | python3 -m json.tool  
    
[/code]
### Assign an issue[​](<#assign-an-issue> "Direct link to Assign an issue")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { assigneeId: \"USER_UUID\" }) { success issue { identifier assignee { name } } } }"}' | python3 -m json.tool  
    
[/code]
### Set priority[​](<#set-priority> "Direct link to Set priority")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { priority: 1 }) { success issue { identifier priority } } }"}' | python3 -m json.tool  
    
[/code]
### Add a comment[​](<#add-a-comment> "Direct link to Add a comment")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { commentCreate(input: { issueId: \"ISSUE_UUID\", body: \"Investigated. Root cause is X.\" }) { success comment { id body } } }"}' | python3 -m json.tool  
    
[/code]
### Set due date[​](<#set-due-date> "Direct link to Set due date")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { dueDate: \"2026-04-01\" }) { success issue { identifier dueDate } } }"}' | python3 -m json.tool  
    
[/code]
### Add labels to an issue[​](<#add-labels-to-an-issue> "Direct link to Add labels to an issue")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { labelIds: [\"LABEL_UUID_1\", \"LABEL_UUID_2\"] }) { success issue { identifier labels { nodes { name } } } } }"}' | python3 -m json.tool  
    
[/code]
### Add issue to a project[​](<#add-issue-to-a-project> "Direct link to Add issue to a project")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { projectId: \"PROJECT_UUID\" }) { success issue { identifier project { name } } } }"}' | python3 -m json.tool  
    
[/code]
### Create a project[​](<#create-a-project> "Direct link to Create a project")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{  
        "query": "mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { success project { id name url } } }",  
        "variables": {  
          "input": {  
            "name": "Q2 Auth Overhaul",  
            "description": "Replace legacy auth with OAuth2 and PKCE",  
            "teamIds": ["TEAM_UUID"]  
          }  
        }  
      }' | python3 -m json.tool  
    
[/code]
## Documents[​](<#documents> "Direct link to Documents")
Linear **Documents** are prose docs (RFCs, specs, notes) stored alongside issues. They have their own `documents` root query and `document(id:)` single-fetch.
### Document URLs and `slugId`[​](<#document-urls-and-slugid> "Direct link to document-urls-and-slugid")
Document URLs look like:
[code] 
    https://linear.app/<workspace>/document/<slug>-<hexSlugId>  
    
[/code]
The trailing hex segment is the `slugId`. Example: `https://linear.app/nousresearch/document/rfc-hermes-permission-gateway-discord-38359beef67c` → `slugId` is `38359beef67c`.
**Important schema detail:** the Markdown body is in the `content` field. The ProseMirror JSON is in `contentState` (not `contentData` — that field does not exist and the API returns 400).
### Fetch a document by slugId[​](<#fetch-a-document-by-slugid> "Direct link to Fetch a document by slugId")
`document(id:)` only accepts UUIDs. To fetch by the URL's hex slug, filter the collection:
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "query($s: String!) { documents(filter: { slugId: { eq: $s } }, first: 1) { nodes { id title content contentState slugId url creator { name } project { name } updatedAt } } }", "variables": {"s": "38359beef67c"}}' \  
      | python3 -m json.tool  
    
[/code]
Or via the Python helper:
[code] 
    python3 scripts/linear_api.py get-document 38359beef67c  
    
[/code]
### Fetch a document by UUID[​](<#fetch-a-document-by-uuid> "Direct link to Fetch a document by UUID")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ document(id: \"11700cff-b514-4db3-afcc-3ed1afacba1c\") { title content url } }"}' \  
      | python3 -m json.tool  
    
[/code]
### List recent documents[​](<#list-recent-documents> "Direct link to List recent documents")
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ documents(first: 25, orderBy: updatedAt) { nodes { id title slugId url updatedAt project { name } } } }"}' \  
      | python3 -m json.tool  
    
[/code]
### Search documents by title[​](<#search-documents-by-title> "Direct link to Search documents by title")
Linear's schema has no `searchDocuments` root. Use a title-substring filter instead:
[code] 
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ documents(filter: { title: { containsIgnoreCase: \"RFC\" } }, first: 25) { nodes { title slugId url } } }"}' \  
      | python3 -m json.tool  
    
[/code]
## Pagination[​](<#pagination> "Direct link to Pagination")
Linear uses Relay-style cursor pagination:
[code] 
    # First page  
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issues(first: 20) { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool  
      
    # Next page — use endCursor from previous response  
    curl -s -X POST https://api.linear.app/graphql \  
      -H "Authorization: $LINEAR_API_KEY" \  
      -H "Content-Type: application/json" \  
      -d '{"query": "{ issues(first: 20, after: \"CURSOR_FROM_PREVIOUS\") { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool  
    
[/code]
Default page size: 50. Max: 250. Always use `first: N` to limit results.
## Filtering Reference[​](<#filtering-reference> "Direct link to Filtering Reference")
Comparators: `eq`, `neq`, `in`, `nin`, `lt`, `lte`, `gt`, `gte`, `contains`, `startsWith`, `containsIgnoreCase`
Combine filters with `or: [...]` for OR logic (default is AND within a filter object).
## Typical Workflow[​](<#typical-workflow> "Direct link to Typical Workflow")
  1. **Query teams** to get team IDs and keys
  2. **Query workflow states** for target team to get state UUIDs
  3. **List or search issues** to find what needs work
  4. **Create issues** with team ID, title, description, priority
  5. **Update status** by setting `stateId` to the target workflow state
  6. **Add comments** to track progress
  7. **Mark complete** by setting `stateId` to the team's "completed" type state


## Rate Limits[​](<#rate-limits> "Direct link to Rate Limits")
  * 5,000 requests/hour per API key
  * 3,000,000 complexity points/hour
  * Use `first: N` to limit results and reduce complexity cost
  * Monitor `X-RateLimit-Requests-Remaining` response header


## Important Notes[​](<#important-notes> "Direct link to Important Notes")
  * Always use `terminal` tool with `curl` for API calls — do NOT use `web_extract` or `browser`
  * Always check the `errors` array in GraphQL responses — HTTP 200 can still contain errors
  * If `stateId` is omitted when creating issues, Linear defaults to the first backlog state
  * The `description` field supports Markdown
  * Use `python3 -m json.tool` or `jq` to format JSON responses for readability


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Setup](<#setup>)
  * [API Basics](<#api-basics>)
  * [Python helper script (ergonomic alternative)](<#python-helper-script-ergonomic-alternative>)
  * [Workflow States](<#workflow-states>)
  * [Common Queries](<#common-queries>)
    * [Get current user](<#get-current-user>)
    * [List teams](<#list-teams>)
    * [List workflow states for a team](<#list-workflow-states-for-a-team>)
    * [List issues (first 20)](<#list-issues-first-20>)
    * [List my assigned issues](<#list-my-assigned-issues>)
    * [Get a single issue (by identifier like ENG-123)](<#get-a-single-issue-by-identifier-like-eng-123>)
    * [Search issues by text](<#search-issues-by-text>)
    * [Filter issues by state type](<#filter-issues-by-state-type>)
    * [Filter by team and assignee](<#filter-by-team-and-assignee>)
    * [List projects](<#list-projects>)
    * [List team members](<#list-team-members>)
    * [List labels](<#list-labels>)
  * [Common Mutations](<#common-mutations>)
    * [Create an issue](<#create-an-issue>)
    * [Update issue status](<#update-issue-status>)
    * [Assign an issue](<#assign-an-issue>)
    * [Set priority](<#set-priority>)
    * [Add a comment](<#add-a-comment>)
    * [Set due date](<#set-due-date>)
    * [Add labels to an issue](<#add-labels-to-an-issue>)
    * [Add issue to a project](<#add-issue-to-a-project>)
    * [Create a project](<#create-a-project>)
  * [Documents](<#documents>)
    * [Document URLs and `slugId`](<#document-urls-and-slugid>)
    * [Fetch a document by slugId](<#fetch-a-document-by-slugid>)
    * [Fetch a document by UUID](<#fetch-a-document-by-uuid>)
    * [List recent documents](<#list-recent-documents>)
    * [Search documents by title](<#search-documents-by-title>)
  * [Pagination](<#pagination>)
  * [Filtering Reference](<#filtering-reference>)
  * [Typical Workflow](<#typical-workflow>)
  * [Rate Limits](<#rate-limits>)
  * [Important Notes](<#important-notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-linear -->
