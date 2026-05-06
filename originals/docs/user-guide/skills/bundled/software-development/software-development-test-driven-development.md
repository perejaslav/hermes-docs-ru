On this page
TDD: enforce RED-GREEN-REFACTOR, tests before code.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/software-development/test-driven-development`  
Version| `1.1.0`  
Author| Hermes Agent (adapted from obra/superpowers)  
License| MIT  
Tags| `testing`, `tdd`, `development`, `quality`, `red-green-refactor`  
Related skills| [`systematic-debugging`](</docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging>), [`writing-plans`](</docs/user-guide/skills/bundled/software-development/software-development-writing-plans>), [`subagent-driven-development`](</docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Test-Driven Development (TDD)
## Overview[​](<#overview> "Direct link to Overview")
Write the test first. Watch it fail. Write minimal code to pass.
**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.
**Violating the letter of the rules is violating the spirit of the rules.**
## When to Use[​](<#when-to-use> "Direct link to When to Use")
**Always:**
  * New features
  * Bug fixes
  * Refactoring
  * Behavior changes


**Exceptions (ask the user first):**
  * Throwaway prototypes
  * Generated code
  * Configuration files


Thinking "skip TDD just this once"? Stop. That's rationalization.
## The Iron Law[​](<#the-iron-law> "Direct link to The Iron Law")
[code] 
    NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST  
    
[/code]
Write code before the test? Delete it. Start over.
**No exceptions:**
  * Don't keep it as "reference"
  * Don't "adapt" it while writing tests
  * Don't look at it
  * Delete means delete


Implement fresh from tests. Period.
## Red-Green-Refactor Cycle[​](<#red-green-refactor-cycle> "Direct link to Red-Green-Refactor Cycle")
### RED — Write Failing Test[​](<#red--write-failing-test> "Direct link to RED — Write Failing Test")
Write one minimal test showing what should happen.
**Good test:**
[code] 
    def test_retries_failed_operations_3_times():  
        attempts = 0  
        def operation():  
            nonlocal attempts  
            attempts += 1  
            if attempts < 3:  
                raise Exception('fail')  
            return 'success'  
      
        result = retry_operation(operation)  
      
        assert result == 'success'  
        assert attempts == 3  
    
[/code]
Clear name, tests real behavior, one thing.
**Bad test:**
[code] 
    def test_retry_works():  
        mock = MagicMock()  
        mock.side_effect = [Exception(), Exception(), 'success']  
        result = retry_operation(mock)  
        assert result == 'success'  # What about retry count? Timing?  
    
[/code]
Vague name, tests mock not real code.
**Requirements:**
  * One behavior per test
  * Clear descriptive name ("and" in name? Split it)
  * Real code, not mocks (unless truly unavoidable)
  * Name describes behavior, not implementation


### Verify RED — Watch It Fail[​](<#verify-red--watch-it-fail> "Direct link to Verify RED — Watch It Fail")
**MANDATORY. Never skip.**
[code] 
    # Use terminal tool to run the specific test  
    pytest tests/test_feature.py::test_specific_behavior -v  
    
[/code]
Confirm:
  * Test fails (not errors from typos)
  * Failure message is expected
  * Fails because the feature is missing


**Test passes immediately?** You're testing existing behavior. Fix the test.
**Test errors?** Fix the error, re-run until it fails correctly.
### GREEN — Minimal Code[​](<#green--minimal-code> "Direct link to GREEN — Minimal Code")
Write the simplest code to pass the test. Nothing more.
**Good:**
[code] 
    def add(a, b):  
        return a + b  # Nothing extra  
    
[/code]
**Bad:**
[code] 
    def add(a, b):  
        result = a + b  
        logging.info(f"Adding {a} + {b} = {result}")  # Extra!  
        return result  
    
[/code]
Don't add features, refactor other code, or "improve" beyond the test.
**Cheating is OK in GREEN:**
  * Hardcode return values
  * Copy-paste
  * Duplicate code
  * Skip edge cases


We'll fix it in REFACTOR.
### Verify GREEN — Watch It Pass[​](<#verify-green--watch-it-pass> "Direct link to Verify GREEN — Watch It Pass")
**MANDATORY.**
[code] 
    # Run the specific test  
    pytest tests/test_feature.py::test_specific_behavior -v  
      
    # Then run ALL tests to check for regressions  
    pytest tests/ -q  
    
[/code]
Confirm:
  * Test passes
  * Other tests still pass
  * Output pristine (no errors, warnings)


**Test fails?** Fix the code, not the test.
**Other tests fail?** Fix regressions now.
### REFACTOR — Clean Up[​](<#refactor--clean-up> "Direct link to REFACTOR — Clean Up")
After green only:
  * Remove duplication
  * Improve names
  * Extract helpers
  * Simplify expressions


Keep tests green throughout. Don't add behavior.
**If tests fail during refactor:** Undo immediately. Take smaller steps.
### Repeat[​](<#repeat> "Direct link to Repeat")
Next failing test for next behavior. One cycle at a time.
## Why Order Matters[​](<#why-order-matters> "Direct link to Why Order Matters")
**"I'll write tests after to verify it works"**
Tests written after code pass immediately. Passing immediately proves nothing:
  * Might test the wrong thing
  * Might test implementation, not behavior
  * Might miss edge cases you forgot
  * You never saw it catch the bug


Test-first forces you to see the test fail, proving it actually tests something.
**"I already manually tested all the edge cases"**
Manual testing is ad-hoc. You think you tested everything but:
  * No record of what you tested
  * Can't re-run when code changes
  * Easy to forget cases under pressure
  * "It worked when I tried it" ≠ comprehensive


Automated tests are systematic. They run the same way every time.
**"Deleting X hours of work is wasteful"**
Sunk cost fallacy. The time is already gone. Your choice now:
  * Delete and rewrite with TDD (high confidence)
  * Keep it and add tests after (low confidence, likely bugs)


The "waste" is keeping code you can't trust.
**"TDD is dogmatic, being pragmatic means adapting"**
TDD IS pragmatic:
  * Finds bugs before commit (faster than debugging after)
  * Prevents regressions (tests catch breaks immediately)
  * Documents behavior (tests show how to use code)
  * Enables refactoring (change freely, tests catch breaks)


"Pragmatic" shortcuts = debugging in production = slower.
**"Tests after achieve the same goals — it's spirit not ritual"**
No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"
Tests-after are biased by your implementation. You test what you built, not what's required. Tests-first force edge case discovery before implementing.
## Common Rationalizations[​](<#common-rationalizations> "Direct link to Common Rationalizations")
Excuse| Reality  
---|---  
"Too simple to test"| Simple code breaks. Test takes 30 seconds.  
"I'll test after"| Tests passing immediately prove nothing.  
"Tests after achieve same goals"| Tests-after = "what does this do?" Tests-first = "what should this do?"  
"Already manually tested"| Ad-hoc ≠ systematic. No record, can't re-run.  
"Deleting X hours is wasteful"| Sunk cost fallacy. Keeping unverified code is technical debt.  
"Keep as reference, write tests first"| You'll adapt it. That's testing after. Delete means delete.  
"Need to explore first"| Fine. Throw away exploration, start with TDD.  
"Test hard = design unclear"| Listen to the test. Hard to test = hard to use.  
"TDD will slow me down"| TDD faster than debugging. Pragmatic = test-first.  
"Manual test faster"| Manual doesn't prove edge cases. You'll re-test every change.  
"Existing code has no tests"| You're improving it. Add tests for the code you touch.  
## Red Flags — STOP and Start Over[​](<#red-flags--stop-and-start-over> "Direct link to Red Flags — STOP and Start Over")
If you catch yourself doing any of these, delete the code and restart with TDD:
  * Code before test
  * Test after implementation
  * Test passes immediately on first run
  * Can't explain why test failed
  * Tests added "later"
  * Rationalizing "just this once"
  * "I already manually tested it"
  * "Tests after achieve the same purpose"
  * "Keep as reference" or "adapt existing code"
  * "Already spent X hours, deleting is wasteful"
  * "TDD is dogmatic, I'm being pragmatic"
  * "This is different because..."


**All of these mean: Delete code. Start over with TDD.**
## Verification Checklist[​](<#verification-checklist> "Direct link to Verification Checklist")
Before marking work complete:
  * Every new function/method has a test
  * Watched each test fail before implementing
  * Each test failed for expected reason (feature missing, not typo)
  * Wrote minimal code to pass each test
  * All tests pass
  * Output pristine (no errors, warnings)
  * Tests use real code (mocks only if unavoidable)
  * Edge cases and errors covered


Can't check all boxes? You skipped TDD. Start over.
## When Stuck[​](<#when-stuck> "Direct link to When Stuck")
Problem| Solution  
---|---  
Don't know how to test| Write the wished-for API. Write the assertion first. Ask the user.  
Test too complicated| Design too complicated. Simplify the interface.  
Must mock everything| Code too coupled. Use dependency injection.  
Test setup huge| Extract helpers. Still complex? Simplify the design.  
## Hermes Agent Integration[​](<#hermes-agent-integration> "Direct link to Hermes Agent Integration")
### Running Tests[​](<#running-tests> "Direct link to Running Tests")
Use the `terminal` tool to run tests at each step:
[code] 
    # RED — verify failure  
    terminal("pytest tests/test_feature.py::test_name -v")  
      
    # GREEN — verify pass  
    terminal("pytest tests/test_feature.py::test_name -v")  
      
    # Full suite — verify no regressions  
    terminal("pytest tests/ -q")  
    
[/code]
### With delegate_task[​](<#with-delegate_task> "Direct link to With delegate_task")
When dispatching subagents for implementation, enforce TDD in the goal:
[code] 
    delegate_task(  
        goal="Implement [feature] using strict TDD",  
        context="""  
        Follow test-driven-development skill:  
        1. Write failing test FIRST  
        2. Run test to verify it fails  
        3. Write minimal code to pass  
        4. Run test to verify it passes  
        5. Refactor if needed  
        6. Commit  
      
        Project test command: pytest tests/ -q  
        Project structure: [describe relevant files]  
        """,  
        toolsets=['terminal', 'file']  
    )  
    
[/code]
### With systematic-debugging[​](<#with-systematic-debugging> "Direct link to With systematic-debugging")
Bug found? Write failing test reproducing it. Follow TDD cycle. The test proves the fix and prevents regression.
Never fix bugs without a test.
## Testing Anti-Patterns[​](<#testing-anti-patterns> "Direct link to Testing Anti-Patterns")
  * **Testing mock behavior instead of real behavior** — mocks should verify interactions, not replace the system under test
  * **Testing implementation details** — test behavior/results, not internal method calls
  * **Happy path only** — always test edge cases, errors, and boundaries
  * **Brittle tests** — tests should verify behavior, not structure; refactoring shouldn't break them


## Final Rule[​](<#final-rule> "Direct link to Final Rule")
[code] 
    Production code → test exists and failed first  
    Otherwise → not TDD  
    
[/code]
No exceptions without the user's explicit permission.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Overview](<#overview>)
  * [When to Use](<#when-to-use>)
  * [The Iron Law](<#the-iron-law>)
  * [Red-Green-Refactor Cycle](<#red-green-refactor-cycle>)
    * [RED — Write Failing Test](<#red--write-failing-test>)
    * [Verify RED — Watch It Fail](<#verify-red--watch-it-fail>)
    * [GREEN — Minimal Code](<#green--minimal-code>)
    * [Verify GREEN — Watch It Pass](<#verify-green--watch-it-pass>)
    * [REFACTOR — Clean Up](<#refactor--clean-up>)
    * [Repeat](<#repeat>)
  * [Why Order Matters](<#why-order-matters>)
  * [Common Rationalizations](<#common-rationalizations>)
  * [Red Flags — STOP and Start Over](<#red-flags--stop-and-start-over>)
  * [Verification Checklist](<#verification-checklist>)
  * [When Stuck](<#when-stuck>)
  * [Hermes Agent Integration](<#hermes-agent-integration>)
    * [Running Tests](<#running-tests>)
    * [With delegate_task](<#with-delegate_task>)
    * [With systematic-debugging](<#with-systematic-debugging>)
  * [Testing Anti-Patterns](<#testing-anti-patterns>)
  * [Final Rule](<#final-rule>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-test-driven-development -->
