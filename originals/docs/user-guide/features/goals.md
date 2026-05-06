On this page
`/goal` gives Hermes a standing objective that survives across turns. After every turn a lightweight judge model checks whether the goal is satisfied by the assistant's last response. If not, Hermes automatically feeds a continuation prompt back into the same session and keeps working — until the goal is achieved, you pause or clear it, or the turn budget runs out.
It's our take on the **Ralph loop** , directly inspired by [Codex CLI 0.128.0's `/goal`](<https://github.com/openai/codex>) by Eric Traut (OpenAI). The core idea — keep a goal alive across turns and don't stop until it's achieved — is theirs. The implementation here is independent and adapted to Hermes' architecture.
## When to use it[​](<#when-to-use-it> "Direct link to When to use it")
Use `/goal` for tasks where you want Hermes to iterate on its own without you re-prompting every turn:
  * "Fix every lint error in `src/` and verify `ruff check` passes"
  * "Port feature X from repo Y, including tests, and get CI green"
  * "Investigate why session IDs sometimes drift on mid-run compression and write up a report"
  * "Build a small CLI to rename files by their EXIF dates, then test it against the photos/ folder"


Tasks where the agent does one turn and stops don't need `/goal`. Tasks where _you'd otherwise have to say "keep going" three times_ are where this shines.
## Quick start[​](<#quick-start> "Direct link to Quick start")
[code] 
    /goal Fix every failing test in tests/hermes_cli/ and make sure scripts/run_tests.sh passes for that directory  
    
[/code]
What you'll see:
  1. **Goal accepted** — `⊙ Goal set (20-turn budget): <your goal>`
  2. **Turn 1 runs** — Hermes starts working as if you'd sent the goal as a normal message.
  3. **Judge runs** — after the turn, the judge model decides `done` or `continue`.
  4. **Loop fires if needed** — if `continue`, you'll see `↻ Continuing toward goal (1/20): <judge's reason>` and Hermes takes the next step automatically.
  5. **Terminates** — eventually you see either `✓ Goal achieved: <reason>` or `⏸ Goal paused — N/20 turns used`.


## Commands[​](<#commands> "Direct link to Commands")
Command| What it does  
---|---  
`/goal <text>`| Set (or replace) the standing goal. Kicks off the first turn immediately so you don't need to send a separate message.  
`/goal` or `/goal status`| Show the current goal, its status, and turns used.  
`/goal pause`| Stop the auto-continuation loop without clearing the goal.  
`/goal resume`| Resume the loop (resets the turn counter back to zero).  
`/goal clear`| Drop the goal entirely.  
Works identically on the CLI and every gateway platform (Telegram, Discord, Slack, Matrix, Signal, WhatsApp, SMS, iMessage, Webhook, API server, and the web dashboard).
## Behavior details[​](<#behavior-details> "Direct link to Behavior details")
### The judge[​](<#the-judge> "Direct link to The judge")
After every turn, Hermes calls an auxiliary model with:
  * The standing goal text
  * The agent's most recent final response (last ~4 KB of text)
  * A system prompt telling the judge to reply with strict JSON: `{"done": <bool>, "reason": "<one-sentence rationale>"}`


The judge is deliberately conservative: it marks a goal `done` only when the response **explicitly** confirms the goal is complete, when the final deliverable is clearly produced, or when the goal is unachievable/blocked (treated as DONE with a block reason so we don't burn budget on impossible tasks).
### Fail-open semantics[​](<#fail-open-semantics> "Direct link to Fail-open semantics")
If the judge errors (network blip, malformed response, unavailable aux client), Hermes treats the verdict as `continue` — a broken judge never wedges progress. The **turn budget** is the real backstop.
### Turn budget[​](<#turn-budget> "Direct link to Turn budget")
Default is 20 continuation turns (`goals.max_turns` in `config.yaml`). When the budget is hit, Hermes auto-pauses and tells you exactly how to proceed:
[code] 
    ⏸ Goal paused — 20/20 turns used. Use /goal resume to keep going, or /goal clear to stop.  
    
[/code]
`/goal resume` resets the counter to zero, so you can keep going in measured chunks.
### User messages always preempt[​](<#user-messages-always-preempt> "Direct link to User messages always preempt")
Any real message you send while a goal is active takes priority over the continuation loop. On the CLI your message lands in `_pending_input` ahead of the queued continuation; on the gateway it goes through the adapter FIFO the same way. The judge runs again after your turn — so if your message happens to complete the goal, the judge will catch it and stop.
### Mid-run safety (gateway)[​](<#mid-run-safety-gateway> "Direct link to Mid-run safety \(gateway\)")
While an agent is already running, `/goal status`, `/goal pause`, and `/goal clear` are safe to run — they only touch control-plane state and don't interrupt the current turn. Setting a **new** goal mid-run (`/goal <new text>`) is rejected with a message telling you to `/stop` first, so the old continuation can't race the new one.
### Persistence[​](<#persistence> "Direct link to Persistence")
Goal state lives in `SessionDB.state_meta` keyed by `goal:<session_id>`. That means `/resume` picks up right where you left off — set a goal, close your laptop, come back tomorrow, `/resume`, and the goal is still standing exactly as you left it (active, paused, or done).
### Prompt cache[​](<#prompt-cache> "Direct link to Prompt cache")
The continuation prompt is a plain user-role message appended to history. It does **not** mutate the system prompt, swap toolsets, or touch the conversation in any way that invalidates Hermes' prompt cache. Running a 20-turn goal costs the same cache-wise as 20 turns of normal conversation.
## Configuration[​](<#configuration> "Direct link to Configuration")
Add to `~/.hermes/config.yaml`:
[code] 
    goals:  
      # Max continuation turns before Hermes auto-pauses and asks you to  
      # /goal resume. Default 20. Lower this if you want tighter loops;  
      # raise it for long-running refactors.  
      max_turns: 20  
    
[/code]
### Choosing the judge model[​](<#choosing-the-judge-model> "Direct link to Choosing the judge model")
The judge uses the `goal_judge` auxiliary task. By default it resolves to your main model (see [Auxiliary Models](</docs/user-guide/configuration#auxiliary-models>)). If you want to route the judge to a cheap fast model to keep costs down, add an override:
[code] 
    auxiliary:  
      goal_judge:  
        provider: openrouter  
        model: google/gemini-3-flash-preview  
    
[/code]
The judge call is small (~200 output tokens) and runs once per turn, so a cheap fast model is usually the right call.
## Example walkthrough[​](<#example-walkthrough> "Direct link to Example walkthrough")
[code] 
    You: /goal Create four files /tmp/note_{1..4}.txt, one per turn, each containing its number as text  
      
      ⊙ Goal set (20-turn budget): Create four files /tmp/note_{1..4}.txt, one per turn, each containing its number as text  
      
    Hermes: Creating /tmp/note_1.txt now.  
      💻 echo "1" > /tmp/note_1.txt   (0.1s)  
      I've created /tmp/note_1.txt with the content "1". I'll continue with the remaining files on the next turn as you specified.  
      
      ↻ Continuing toward goal (1/20): Only 1 of 4 files has been created; 3 files remain.  
      
    Hermes: [Continuing toward your standing goal]  
      💻 echo "2" > /tmp/note_2.txt   (0.1s)  
      Created /tmp/note_2.txt. Two more to go.  
      
      ↻ Continuing toward goal (2/20): 2 of 4 files created; 2 remain.  
      
    Hermes: [Continuing toward your standing goal]  
      💻 echo "3" > /tmp/note_3.txt   (0.1s)  
      Created /tmp/note_3.txt.  
      
      ↻ Continuing toward goal (3/20): 3 of 4 files created; 1 remains.  
      
    Hermes: [Continuing toward your standing goal]  
      💻 echo "4" > /tmp/note_4.txt   (0.1s)  
      All four files have been created: /tmp/note_1.txt through /tmp/note_4.txt, each containing its number.  
      
      ✓ Goal achieved: All four files were created with the specified content, completing the goal.  
      
    You: _  
    
[/code]
Four turns, one `/goal` invocation, zero "keep going" prompts from you.
## When the judge gets it wrong[​](<#when-the-judge-gets-it-wrong> "Direct link to When the judge gets it wrong")
No judge is perfect. Two failure modes to watch for:
**False negative — judge says continue when the goal is actually done.** The turn budget catches this. You'll see `⏸ Goal paused` and can `/goal clear` or just send a new message.
**False positive — judge says done when work remains.** You'll see `✓ Goal achieved` but you know better. Send a follow-up message to continue, or re-set the goal more precisely: `/goal <more specific text>`. The judge's system prompt is deliberately conservative to make false positives rarer than false negatives.
If you find a judge verdict unconvincing, the reason text in the `↻ Continuing toward goal` or `✓ Goal achieved` line tells you exactly what the judge saw. That's usually enough to diagnose whether the goal text was ambiguous or the model's response was.
## Attribution[​](<#attribution> "Direct link to Attribution")
`/goal` is Hermes' take on the **Ralph loop** pattern. The user-facing design — keep a goal alive across turns, don't stop until it's achieved, with create/pause/resume/clear controls — was popularised and shipped in [Codex CLI 0.128.0](<https://github.com/openai/codex>) by Eric Traut on OpenAI's Codex team. Our implementation is independent (central `CommandDef` registry, `SessionDB.state_meta` persistence, auxiliary-client judge, adapter-FIFO continuation on the gateway side) but the idea is theirs. Credit where credit's due.
  * [When to use it](<#when-to-use-it>)
  * [Quick start](<#quick-start>)
  * [Commands](<#commands>)
  * [Behavior details](<#behavior-details>)
    * [The judge](<#the-judge>)
    * [Fail-open semantics](<#fail-open-semantics>)
    * [Turn budget](<#turn-budget>)
    * [User messages always preempt](<#user-messages-always-preempt>)
    * [Mid-run safety (gateway)](<#mid-run-safety-gateway>)
    * [Persistence](<#persistence>)
    * [Prompt cache](<#prompt-cache>)
  * [Configuration](<#configuration>)
    * [Choosing the judge model](<#choosing-the-judge-model>)
  * [Example walkthrough](<#example-walkthrough>)
  * [When the judge gets it wrong](<#when-the-judge-gets-it-wrong>)
  * [Attribution](<#attribution>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/goals -->
