On this page
4-phase root cause debugging: understand bugs before fixing.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/software-development/systematic-debugging`  
Version| `1.1.0`  
Author| Hermes Agent (adapted from obra/superpowers)  
License| MIT  
Tags| `debugging`, `troubleshooting`, `problem-solving`, `root-cause`, `investigation`  
Related skills| [`test-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-test-driven-development>), [`writing-plans`](</docs/user-guide/skills/bundled/software-development/software-development-writing-plans>), [`subagent-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Systematic Debugging
## Overview[​](<#overview> "Direct link to Overview")
Random fixes waste time and create new bugs. Quick patches mask underlying issues.
**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.
**Violating the letter of this process is violating the spirit of debugging.**
## The Iron Law[​](<#the-iron-law> "Direct link to The Iron Law")
[code] 
    NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST  
    
[/code]
If you haven't completed Phase 1, you cannot propose fixes.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
Use for ANY technical issue:
  * Test failures
  * Bugs in production
  * Unexpected behavior
  * Performance problems
  * Build failures
  * Integration issues


**Use this ESPECIALLY when:**
  * Under time pressure (emergencies make guessing tempting)
  * "Just one quick fix" seems obvious
  * You've already tried multiple fixes
  * Previous fix didn't work
  * You don't fully understand the issue


**Don't skip when:**
  * Issue seems simple (simple bugs have root causes too)
  * You're in a hurry (rushing guarantees rework)
  * Someone wants it fixed NOW (systematic is faster than thrashing)


## The Four Phases[​](<#the-four-phases> "Direct link to The Four Phases")
You MUST complete each phase before proceeding to the next.
* * *
## Phase 1: Root Cause Investigation[​](<#phase-1-root-cause-investigation> "Direct link to Phase 1: Root Cause Investigation")
**BEFORE attempting ANY fix:**
### 1\. Read Error Messages Carefully[​](<#1-read-error-messages-carefully> "Direct link to 1. Read Error Messages Carefully")
  * Don't skip past errors or warnings
  * They often contain the exact solution
  * Read stack traces completely
  * Note line numbers, file paths, error codes


**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.
### 2\. Reproduce Consistently[​](<#2-reproduce-consistently> "Direct link to 2. Reproduce Consistently")
  * Can you trigger it reliably?
  * What are the exact steps?
  * Does it happen every time?
  * If not reproducible → gather more data, don't guess


**Action:** Use the `terminal` tool to run the failing test or trigger the bug:
[code] 
    # Run specific failing test  
    pytest tests/test_module.py::test_name -v  
      
    # Run with verbose output  
    pytest tests/test_module.py -v --tb=long  
    
[/code]
### 3\. Check Recent Changes[​](<#3-check-recent-changes> "Direct link to 3. Check Recent Changes")
  * What changed that could cause this?
  * Git diff, recent commits
  * New dependencies, config changes


**Action:**
[code] 
    # Recent commits  
    git log --oneline -10  
      
    # Uncommitted changes  
    git diff  
      
    # Changes in specific file  
    git log -p --follow src/problematic_file.py | head -100  
    
[/code]
### 4\. Gather Evidence in Multi-Component Systems[​](<#4-gather-evidence-in-multi-component-systems> "Direct link to 4. Gather Evidence in Multi-Component Systems")
**WHEN system has multiple components (API → service → database, CI → build → deploy):**
**BEFORE proposing fixes, add diagnostic instrumentation:**
For EACH component boundary:
  * Log what data enters the component
  * Log what data exits the component
  * Verify environment/config propagation
  * Check state at each layer


Run once to gather evidence showing WHERE it breaks. THEN analyze evidence to identify the failing component. THEN investigate that specific component.
### 5\. Trace Data Flow[​](<#5-trace-data-flow> "Direct link to 5. Trace Data Flow")
**WHEN error is deep in the call stack:**
  * Where does the bad value originate?
  * What called this function with the bad value?
  * Keep tracing upstream until you find the source
  * Fix at the source, not at the symptom


**Action:** Use `search_files` to trace references:
[code] 
    # Find where the function is called  
    search_files("function_name(", path="src/", file_glob="*.py")  
      
    # Find where the variable is set  
    search_files("variable_name\\s*=", path="src/", file_glob="*.py")  
    
[/code]
### Phase 1 Completion Checklist[​](<#phase-1-completion-checklist> "Direct link to Phase 1 Completion Checklist")
  * Error messages fully read and understood
  * Issue reproduced consistently
  * Recent changes identified and reviewed
  * Evidence gathered (logs, state, data flow)
  * Problem isolated to specific component/code
  * Root cause hypothesis formed


**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.
* * *
## Phase 2: Pattern Analysis[​](<#phase-2-pattern-analysis> "Direct link to Phase 2: Pattern Analysis")
**Find the pattern before fixing:**
### 1\. Find Working Examples[​](<#1-find-working-examples> "Direct link to 1. Find Working Examples")
  * Locate similar working code in the same codebase
  * What works that's similar to what's broken?


**Action:** Use `search_files` to find comparable patterns:
[code] 
    search_files("similar_pattern", path="src/", file_glob="*.py")  
    
[/code]
### 2\. Compare Against References[​](<#2-compare-against-references> "Direct link to 2. Compare Against References")
  * If implementing a pattern, read the reference implementation COMPLETELY
  * Don't skim — read every line
  * Understand the pattern fully before applying


### 3\. Identify Differences[​](<#3-identify-differences> "Direct link to 3. Identify Differences")
  * What's different between working and broken?
  * List every difference, however small
  * Don't assume "that can't matter"


### 4\. Understand Dependencies[​](<#4-understand-dependencies> "Direct link to 4. Understand Dependencies")
  * What other components does this need?
  * What settings, config, environment?
  * What assumptions does it make?


* * *
## Phase 3: Hypothesis and Testing[​](<#phase-3-hypothesis-and-testing> "Direct link to Phase 3: Hypothesis and Testing")
**Scientific method:**
### 1\. Form a Single Hypothesis[​](<#1-form-a-single-hypothesis> "Direct link to 1. Form a Single Hypothesis")
  * State clearly: "I think X is the root cause because Y"
  * Write it down
  * Be specific, not vague


### 2\. Test Minimally[​](<#2-test-minimally> "Direct link to 2. Test Minimally")
  * Make the SMALLEST possible change to test the hypothesis
  * One variable at a time
  * Don't fix multiple things at once


### 3\. Verify Before Continuing[​](<#3-verify-before-continuing> "Direct link to 3. Verify Before Continuing")
  * Did it work? → Phase 4
  * Didn't work? → Form NEW hypothesis
  * DON'T add more fixes on top


### 4\. When You Don't Know[​](<#4-when-you-dont-know> "Direct link to 4. When You Don't Know")
  * Say "I don't understand X"
  * Don't pretend to know
  * Ask the user for help
  * Research more


* * *
## Phase 4: Implementation[​](<#phase-4-implementation> "Direct link to Phase 4: Implementation")
**Fix the root cause, not the symptom:**
### 1\. Create Failing Test Case[​](<#1-create-failing-test-case> "Direct link to 1. Create Failing Test Case")
  * Simplest possible reproduction
  * Automated test if possible
  * MUST have before fixing
  * Use the `test-driven-development` skill


### 2\. Implement Single Fix[​](<#2-implement-single-fix> "Direct link to 2. Implement Single Fix")
  * Address the root cause identified
  * ONE change at a time
  * No "while I'm here" improvements
  * No bundled refactoring


### 3\. Verify Fix[​](<#3-verify-fix> "Direct link to 3. Verify Fix")
[code] 
    # Run the specific regression test  
    pytest tests/test_module.py::test_regression -v  
      
    # Run full suite — no regressions  
    pytest tests/ -q  
    
[/code]
### 4\. If Fix Doesn't Work — The Rule of Three[​](<#4-if-fix-doesnt-work--the-rule-of-three> "Direct link to 4. If Fix Doesn't Work — The Rule of Three")
  * **STOP.**
  * Count: How many fixes have you tried?
  * If < 3: Return to Phase 1, re-analyze with new information
  * **If ≥ 3: STOP and question the architecture (step 5 below)**
  * DON'T attempt Fix #4 without architectural discussion


### 5\. If 3+ Fixes Failed: Question Architecture[​](<#5-if-3-fixes-failed-question-architecture> "Direct link to 5. If 3+ Fixes Failed: Question Architecture")
**Pattern indicating an architectural problem:**
  * Each fix reveals new shared state/coupling in a different place
  * Fixes require "massive refactoring" to implement
  * Each fix creates new symptoms elsewhere


**STOP and question fundamentals:**
  * Is this pattern fundamentally sound?
  * Are we "sticking with it through sheer inertia"?
  * Should we refactor the architecture vs. continue fixing symptoms?


**Discuss with the user before attempting more fixes.**
This is NOT a failed hypothesis — this is a wrong architecture.
* * *
## Red Flags — STOP and Follow Process[​](<#red-flags--stop-and-follow-process> "Direct link to Red Flags — STOP and Follow Process")
If you catch yourself thinking:
  * "Quick fix for now, investigate later"
  * "Just try changing X and see if it works"
  * "Add multiple changes, run tests"
  * "Skip the test, I'll manually verify"
  * "It's probably X, let me fix that"
  * "I don't fully understand but this might work"
  * "Pattern says X but I'll adapt it differently"
  * "Here are the main problems: [lists fixes without investigation]"
  * Proposing solutions before tracing data flow
  * **"One more fix attempt" (when already tried 2+)**
  * **Each fix reveals a new problem in a different place**


**ALL of these mean: STOP. Return to Phase 1.**
**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).
## Common Rationalizations[​](<#common-rationalizations> "Direct link to Common Rationalizations")
Excuse| Reality  
---|---  
"Issue is simple, don't need process"| Simple issues have root causes too. Process is fast for simple bugs.  
"Emergency, no time for process"| Systematic debugging is FASTER than guess-and-check thrashing.  
"Just try this first, then investigate"| First fix sets the pattern. Do it right from the start.  
"I'll write test after confirming fix works"| Untested fixes don't stick. Test first proves it.  
"Multiple fixes at once saves time"| Can't isolate what worked. Causes new bugs.  
"Reference too long, I'll adapt the pattern"| Partial understanding guarantees bugs. Read it completely.  
"I see the problem, let me fix it"| Seeing symptoms ≠ understanding root cause.  
"One more fix attempt" (after 2+ failures)| 3+ failures = architectural problem. Question the pattern, don't fix again.  
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
Phase| Key Activities| Success Criteria  
---|---|---  
**1\. Root Cause**|  Read errors, reproduce, check changes, gather evidence, trace data flow| Understand WHAT and WHY  
**2\. Pattern**|  Find working examples, compare, identify differences| Know what's different  
**3\. Hypothesis**|  Form theory, test minimally, one variable at a time| Confirmed or new hypothesis  
**4\. Implementation**|  Create regression test, fix root cause, verify| Bug resolved, all tests pass  
## Hermes Agent Integration[​](<#hermes-agent-integration> "Direct link to Hermes Agent Integration")
### Investigation Tools[​](<#investigation-tools> "Direct link to Investigation Tools")
Use these Hermes tools during Phase 1:
  * **`search_files`** — Find error strings, trace function calls, locate patterns
  * **`read_file`** — Read source code with line numbers for precise analysis
  * **`terminal`** — Run tests, check git history, reproduce bugs
  * **`web_search`/`web_extract`** — Research error messages, library docs


### With delegate_task[​](<#with-delegate_task> "Direct link to With delegate_task")
For complex multi-component debugging, dispatch investigation subagents:
[code] 
    delegate_task(  
        goal="Investigate why [specific test/behavior] fails",  
        context="""  
        Follow systematic-debugging skill:  
        1. Read the error message carefully  
        2. Reproduce the issue  
        3. Trace the data flow to find root cause  
        4. Report findings — do NOT fix yet  
      
        Error: [paste full error]  
        File: [path to failing code]  
        Test command: [exact command]  
        """,  
        toolsets=['terminal', 'file']  
    )  
    
[/code]
### With test-driven-development[​](<#with-test-driven-development> "Direct link to With test-driven-development")
When fixing bugs:
  1. Write a test that reproduces the bug (RED)
  2. Debug systematically to find root cause
  3. Fix the root cause (GREEN)
  4. The test proves the fix and prevents regression


## Real-World Impact[​](<#real-world-impact> "Direct link to Real-World Impact")
From debugging sessions:
  * Systematic approach: 15-30 minutes to fix
  * Random fixes approach: 2-3 hours of thrashing
  * First-time fix rate: 95% vs 40%
  * New bugs introduced: Near zero vs common


**No shortcuts. No guessing. Systematic always wins.**
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Overview](<#overview>)
  * [The Iron Law](<#the-iron-law>)
  * [When to Use](<#when-to-use>)
  * [The Four Phases](<#the-four-phases>)
  * [Phase 1: Root Cause Investigation](<#phase-1-root-cause-investigation>)
    * [1\. Read Error Messages Carefully](<#1-read-error-messages-carefully>)
    * [2\. Reproduce Consistently](<#2-reproduce-consistently>)
    * [3\. Check Recent Changes](<#3-check-recent-changes>)
    * [4\. Gather Evidence in Multi-Component Systems](<#4-gather-evidence-in-multi-component-systems>)
    * [5\. Trace Data Flow](<#5-trace-data-flow>)
    * [Phase 1 Completion Checklist](<#phase-1-completion-checklist>)
  * [Phase 2: Pattern Analysis](<#phase-2-pattern-analysis>)
    * [1\. Find Working Examples](<#1-find-working-examples>)
    * [2\. Compare Against References](<#2-compare-against-references>)
    * [3\. Identify Differences](<#3-identify-differences>)
    * [4\. Understand Dependencies](<#4-understand-dependencies>)
  * [Phase 3: Hypothesis and Testing](<#phase-3-hypothesis-and-testing>)
    * [1\. Form a Single Hypothesis](<#1-form-a-single-hypothesis>)
    * [2\. Test Minimally](<#2-test-minimally>)
    * [3\. Verify Before Continuing](<#3-verify-before-continuing>)
    * [4\. When You Don't Know](<#4-when-you-dont-know>)
  * [Phase 4: Implementation](<#phase-4-implementation>)
    * [1\. Create Failing Test Case](<#1-create-failing-test-case>)
    * [2\. Implement Single Fix](<#2-implement-single-fix>)
    * [3\. Verify Fix](<#3-verify-fix>)
    * [4\. If Fix Doesn't Work — The Rule of Three](<#4-if-fix-doesnt-work--the-rule-of-three>)
    * [5\. If 3+ Fixes Failed: Question Architecture](<#5-if-3-fixes-failed-question-architecture>)
  * [Red Flags — STOP and Follow Process](<#red-flags--stop-and-follow-process>)
  * [Common Rationalizations](<#common-rationalizations>)
  * [Quick Reference](<#quick-reference>)
  * [Hermes Agent Integration](<#hermes-agent-integration>)
    * [Investigation Tools](<#investigation-tools>)
    * [With delegate_task](<#with-delegate_task>)
    * [With test-driven-development](<#with-test-driven-development>)
  * [Real-World Impact](<#real-world-impact>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging -->
