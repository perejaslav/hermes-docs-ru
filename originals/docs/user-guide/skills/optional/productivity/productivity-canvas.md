On this page
Canvas LMS integration — fetch enrolled courses and assignments using API token authentication.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/productivity/canvas`  
Path| `optional-skills/productivity/canvas`  
Version| `1.0.0`  
Author| community  
License| MIT  
Tags| `Canvas`, `LMS`, `Education`, `Courses`, `Assignments`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Canvas LMS — Course & Assignment Access
Read-only access to Canvas LMS for listing courses and assignments.
## Scripts[​](<#scripts> "Direct link to Scripts")
  * `scripts/canvas_api.py` — Python CLI for Canvas API calls


## Setup[​](<#setup> "Direct link to Setup")
  1. Log in to your Canvas instance in a browser
  2. Go to **Account → Settings** (click your profile icon, then Settings)
  3. Scroll to **Approved Integrations** and click **\+ New Access Token**
  4. Name the token (e.g., "Hermes Agent"), set an optional expiry, and click **Generate Token**
  5. Copy the token and add to `~/.hermes/.env`:


[code] 
    CANVAS_API_TOKEN=your_token_here  
    CANVAS_BASE_URL=https://yourschool.instructure.com  
    
[/code]
The base URL is whatever appears in your browser when you're logged into Canvas (no trailing slash).
## Usage[​](<#usage> "Direct link to Usage")
[code] 
    CANVAS="python $HERMES_HOME/skills/productivity/canvas/scripts/canvas_api.py"  
      
    # List all active courses  
    $CANVAS list_courses --enrollment-state active  
      
    # List all courses (any state)  
    $CANVAS list_courses  
      
    # List assignments for a specific course  
    $CANVAS list_assignments 12345  
      
    # List assignments ordered by due date  
    $CANVAS list_assignments 12345 --order-by due_at  
    
[/code]
## Output Format[​](<#output-format> "Direct link to Output Format")
**list_courses** returns:
[code] 
    [{"id": 12345, "name": "Intro to CS", "course_code": "CS101", "workflow_state": "available", "start_at": "...", "end_at": "..."}]  
    
[/code]
**list_assignments** returns:
[code] 
    [{"id": 67890, "name": "Homework 1", "due_at": "2025-02-15T23:59:00Z", "points_possible": 100, "submission_types": ["online_upload"], "html_url": "...", "description": "...", "course_id": 12345}]  
    
[/code]
Note: Assignment descriptions are truncated to 500 characters. The `html_url` field links to the full assignment page in Canvas.
## API Reference (curl)[​](<#api-reference-curl> "Direct link to API Reference \(curl\)")
[code] 
    # List courses  
    curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \  
      "$CANVAS_BASE_URL/api/v1/courses?enrollment_state=active&per_page=10"  
      
    # List assignments for a course  
    curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \  
      "$CANVAS_BASE_URL/api/v1/courses/COURSE_ID/assignments?per_page=10&order_by=due_at"  
    
[/code]
Canvas uses `Link` headers for pagination. The Python script handles pagination automatically.
## Rules[​](<#rules> "Direct link to Rules")
  * This skill is **read-only** — it only fetches data, never modifies courses or assignments
  * On first use, verify auth by running `$CANVAS list_courses` — if it fails with 401, guide the user through setup
  * Canvas rate-limits to ~700 requests per 10 minutes; check `X-Rate-Limit-Remaining` header if hitting limits


## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
Problem| Fix  
---|---  
401 Unauthorized| Token invalid or expired — regenerate in Canvas Settings  
403 Forbidden| Token lacks permission for this course  
Empty course list| Try `--enrollment-state active` or omit the flag to see all states  
Wrong institution| Verify `CANVAS_BASE_URL` matches the URL in your browser  
Timeout errors| Check network connectivity to your Canvas instance  
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Scripts](<#scripts>)
  * [Setup](<#setup>)
  * [Usage](<#usage>)
  * [Output Format](<#output-format>)
  * [API Reference (curl)](<#api-reference-curl>)
  * [Rules](<#rules>)
  * [Troubleshooting](<#troubleshooting>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-canvas -->
