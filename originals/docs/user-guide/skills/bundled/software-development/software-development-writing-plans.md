On this page
Write implementation plans: bite-sized tasks, paths, code.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/software-development/writing-plans`  
Version| `1.1.0`  
Author| Hermes Agent (adapted from obra/superpowers)  
License| MIT  
Tags| `planning`, `design`, `implementation`, `workflow`, `documentation`  
Related skills| [`subagent-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development>), [`test-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-test-driven-development>), [`requesting-code-review`](</docs/user-guide/skills/bundled/software-development/software-development-requesting-code-review>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Writing Implementation Plans
## Overview[​](<#overview> "Direct link to Overview")
Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.
Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.
**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
**Always use before:**
  * Implementing multi-step features
  * Breaking down complex requirements
  * Delegating to subagents via subagent-driven-development


**Don't skip when:**
  * Feature seems simple (assumptions cause bugs)
  * You plan to implement it yourself (future you needs guidance)
  * Working alone (documentation matters)


## Bite-Sized Task Granularity[​](<#bite-sized-task-granularity> "Direct link to Bite-Sized Task Granularity")
**Each task = 2-5 minutes of focused work.**
Every step is one action:
  * "Write the failing test" — step
  * "Run it to make sure it fails" — step
  * "Implement the minimal code to make the test pass" — step
  * "Run the tests and make sure they pass" — step
  * "Commit" — step


**Too big:**
[code] 
    ### Task 1: Build authentication system  
    [50 lines of code across 5 files]  
    
[/code]
**Right size:**
[code] 
    ### Task 1: Create User model with email field  
    [10 lines, 1 file]  
      
    ### Task 2: Add password hash field to User  
    [8 lines, 1 file]  
      
    ### Task 3: Create password hashing utility  
    [15 lines, 1 file]  
    
[/code]
## Plan Document Structure[​](<#plan-document-structure> "Direct link to Plan Document Structure")
### Header (Required)[​](<#header-required> "Direct link to Header \(Required\)")
Every plan MUST start with:
[code] 
    # [Feature Name] Implementation Plan  
      
    > **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.  
      
    **Goal:** [One sentence describing what this builds]  
      
    **Architecture:** [2-3 sentences about approach]  
      
    **Tech Stack:** [Key technologies/libraries]  
      
    ---  
    
[/code]
### Task Structure[​](<#task-structure> "Direct link to Task Structure")
Each task follows this format:
[code] 
    ### Task N: [Descriptive Name]  
      
    **Objective:** What this task accomplishes (one sentence)  
      
    **Files:**  
    - Create: `exact/path/to/new_file.py`  
    - Modify: `exact/path/to/existing.py:45-67` (line numbers if known)  
    - Test: `tests/path/to/test_file.py`  
      
    **Step 1: Write failing test**  
      
    ```python  
    def test_specific_behavior():  
        result = function(input)  
        assert result == expected  
    ```  
      
    **Step 2: Run test to verify failure**  
      
    Run: `pytest tests/path/test.py::test_specific_behavior -v`  
    Expected: FAIL — "function not defined"  
      
    **Step 3: Write minimal implementation**  
      
    ```python  
    def function(input):  
        return expected  
    ```  
      
    **Step 4: Run test to verify pass**  
      
    Run: `pytest tests/path/test.py::test_specific_behavior -v`  
    Expected: PASS  
      
    **Step 5: Commit**  
      
    ```bash  
    git add tests/path/test.py src/path/file.py  
    git commit -m "feat: add specific feature"  
    ```  
    
[/code]
## Writing Process[​](<#writing-process> "Direct link to Writing Process")
### Step 1: Understand Requirements[​](<#step-1-understand-requirements> "Direct link to Step 1: Understand Requirements")
Read and understand:
  * Feature requirements
  * Design documents or user description
  * Acceptance criteria
  * Constraints


### Step 2: Explore the Codebase[​](<#step-2-explore-the-codebase> "Direct link to Step 2: Explore the Codebase")
Use Hermes tools to understand the project:
[code] 
    # Understand project structure  
    search_files("*.py", target="files", path="src/")  
      
    # Look at similar features  
    search_files("similar_pattern", path="src/", file_glob="*.py")  
      
    # Check existing tests  
    search_files("*.py", target="files", path="tests/")  
      
    # Read key files  
    read_file("src/app.py")  
    
[/code]
### Step 3: Design Approach[​](<#step-3-design-approach> "Direct link to Step 3: Design Approach")
Decide:
  * Architecture pattern
  * File organization
  * Dependencies needed
  * Testing strategy


### Step 4: Write Tasks[​](<#step-4-write-tasks> "Direct link to Step 4: Write Tasks")
Create tasks in order:
  1. Setup/infrastructure
  2. Core functionality (TDD for each)
  3. Edge cases
  4. Integration
  5. Cleanup/documentation


### Step 5: Add Complete Details[​](<#step-5-add-complete-details> "Direct link to Step 5: Add Complete Details")
For each task, include:
  * **Exact file paths** (not "the config file" but `src/config/settings.py`)
  * **Complete code examples** (not "add validation" but the actual code)
  * **Exact commands** with expected output
  * **Verification steps** that prove the task works


### Step 6: Review the Plan[​](<#step-6-review-the-plan> "Direct link to Step 6: Review the Plan")
Check:
  * Tasks are sequential and logical
  * Each task is bite-sized (2-5 min)
  * File paths are exact
  * Code examples are complete (copy-pasteable)
  * Commands are exact with expected output
  * No missing context
  * DRY, YAGNI, TDD principles applied


### Step 7: Save the Plan[​](<#step-7-save-the-plan> "Direct link to Step 7: Save the Plan")
[code] 
    mkdir -p docs/plans  
    # Save plan to docs/plans/YYYY-MM-DD-feature-name.md  
    git add docs/plans/  
    git commit -m "docs: add implementation plan for [feature]"  
    
[/code]
## Principles[​](<#principles> "Direct link to Principles")
### DRY (Don't Repeat Yourself)[​](<#dry-dont-repeat-yourself> "Direct link to DRY \(Don't Repeat Yourself\)")
**Bad:** Copy-paste validation in 3 places **Good:** Extract validation function, use everywhere
### YAGNI (You Aren't Gonna Need It)[​](<#yagni-you-arent-gonna-need-it> "Direct link to YAGNI \(You Aren't Gonna Need It\)")
**Bad:** Add "flexibility" for future requirements **Good:** Implement only what's needed now
[code] 
    # Bad — YAGNI violation  
    class User:  
        def __init__(self, name, email):  
            self.name = name  
            self.email = email  
            self.preferences = {}  # Not needed yet!  
            self.metadata = {}     # Not needed yet!  
      
    # Good — YAGNI  
    class User:  
        def __init__(self, name, email):  
            self.name = name  
            self.email = email  
    
[/code]
### TDD (Test-Driven Development)[​](<#tdd-test-driven-development> "Direct link to TDD \(Test-Driven Development\)")
Every task that produces code should include the full TDD cycle:
  1. Write failing test
  2. Run to verify failure
  3. Write minimal code
  4. Run to verify pass


See `test-driven-development` skill for details.
### Frequent Commits[​](<#frequent-commits> "Direct link to Frequent Commits")
Commit after every task:
[code] 
    git add [files]  
    git commit -m "type: description"  
    
[/code]
## Common Mistakes[​](<#common-mistakes> "Direct link to Common Mistakes")
### Vague Tasks[​](<#vague-tasks> "Direct link to Vague Tasks")
**Bad:** "Add authentication" **Good:** "Create User model with email and password_hash fields"
### Incomplete Code[​](<#incomplete-code> "Direct link to Incomplete Code")
**Bad:** "Step 1: Add validation function" **Good:** "Step 1: Add validation function" followed by the complete function code
### Missing Verification[​](<#missing-verification> "Direct link to Missing Verification")
**Bad:** "Step 3: Test it works" **Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"
### Missing File Paths[​](<#missing-file-paths> "Direct link to Missing File Paths")
**Bad:** "Create the model file" **Good:** "Create: `src/models/user.py`"
## Execution Handoff[​](<#execution-handoff> "Direct link to Execution Handoff")
After saving the plan, offer the execution approach:
**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**
When executing, use the `subagent-driven-development` skill:
  * Fresh `delegate_task` per task with full context
  * Spec compliance review after each task
  * Code quality review after spec passes
  * Proceed only when both reviews approve


## Remember[​](<#remember> "Direct link to Remember")
[code] 
    Bite-sized tasks (2-5 min each)  
    Exact file paths  
    Complete code (copy-pasteable)  
    Exact commands with expected output  
    Verification steps  
    DRY, YAGNI, TDD  
    Frequent commits  
    
[/code]
**A good plan makes implementation obvious.**
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Overview](<#overview>)
  * [When to Use](<#when-to-use>)
  * [Bite-Sized Task Granularity](<#bite-sized-task-granularity>)
  * [Plan Document Structure](<#plan-document-structure>)
    * [Header (Required)](<#header-required>)
    * [Task Structure](<#task-structure>)
  * [Writing Process](<#writing-process>)
    * [Step 1: Understand Requirements](<#step-1-understand-requirements>)
    * [Step 2: Explore the Codebase](<#step-2-explore-the-codebase>)
    * [Step 3: Design Approach](<#step-3-design-approach>)
    * [Step 4: Write Tasks](<#step-4-write-tasks>)
    * [Step 5: Add Complete Details](<#step-5-add-complete-details>)
    * [Step 6: Review the Plan](<#step-6-review-the-plan>)
    * [Step 7: Save the Plan](<#step-7-save-the-plan>)
  * [Principles](<#principles>)
    * [DRY (Don't Repeat Yourself)](<#dry-dont-repeat-yourself>)
    * [YAGNI (You Aren't Gonna Need It)](<#yagni-you-arent-gonna-need-it>)
    * [TDD (Test-Driven Development)](<#tdd-test-driven-development>)
    * [Frequent Commits](<#frequent-commits>)
  * [Common Mistakes](<#common-mistakes>)
    * [Vague Tasks](<#vague-tasks>)
    * [Incomplete Code](<#incomplete-code>)
    * [Missing Verification](<#missing-verification>)
    * [Missing File Paths](<#missing-file-paths>)
  * [Execution Handoff](<#execution-handoff>)
  * [Remember](<#remember>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-writing-plans -->
