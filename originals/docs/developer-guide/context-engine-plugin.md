On this page
Context engine plugins replace the built-in `ContextCompressor` with an alternative strategy for managing conversation context. For example, a Lossless Context Management (LCM) engine that builds a knowledge DAG instead of lossy summarization.
## How it works[​](<#how-it-works> "Direct link to How it works")
The agent's context management is built on the `ContextEngine` ABC (`agent/context_engine.py`). The built-in `ContextCompressor` is the default implementation. Plugin engines must implement the same interface.
Only **one** context engine can be active at a time. Selection is config-driven:
[code] 
    # config.yaml  
    context:  
      engine: "compressor"    # default built-in  
      engine: "lcm"           # activates a plugin engine named "lcm"  
    
[/code]
Plugin engines are **never auto-activated** — the user must explicitly set `context.engine` to the plugin's name.
## Directory structure[​](<#directory-structure> "Direct link to Directory structure")
Each context engine lives in `plugins/context_engine/<name>/`:
[code] 
    plugins/context_engine/lcm/  
    ├── __init__.py      # exports the ContextEngine subclass  
    ├── plugin.yaml      # metadata (name, description, version)  
    └── ...              # any other modules your engine needs  
    
[/code]
## The ContextEngine ABC[​](<#the-contextengine-abc> "Direct link to The ContextEngine ABC")
Your engine must implement these **required** methods:
[code] 
    from agent.context_engine import ContextEngine  
      
    class LCMEngine(ContextEngine):  
      
        @property  
        def name(self) -> str:  
            """Short identifier, e.g. 'lcm'. Must match config.yaml value."""  
            return "lcm"  
      
        def update_from_response(self, usage: dict) -> None:  
            """Called after every LLM call with the usage dict.  
      
            Update self.last_prompt_tokens, self.last_completion_tokens,  
            self.last_total_tokens from the response.  
            """  
      
        def should_compress(self, prompt_tokens: int = None) -> bool:  
            """Return True if compaction should fire this turn."""  
      
        def compress(self, messages: list, current_tokens: int = None,  
                     focus_topic: str = None) -> list:  
            """Compact the message list and return a new (possibly shorter) list.  
      
            The returned list must be a valid OpenAI-format message sequence.  
      
            ``focus_topic`` is an optional topic string from manual  
            ``/compress <focus>``; engines that support guided compression should  
            prioritise preserving information related to it, others may ignore it.  
            """  
    
[/code]
### Class attributes your engine must maintain[​](<#class-attributes-your-engine-must-maintain> "Direct link to Class attributes your engine must maintain")
The agent reads these directly for display and logging:
[code] 
    last_prompt_tokens: int = 0  
    last_completion_tokens: int = 0  
    last_total_tokens: int = 0  
    threshold_tokens: int = 0        # when compression triggers  
    context_length: int = 0          # model's full context window  
    compression_count: int = 0       # how many times compress() has run  
    
[/code]
### Optional methods[​](<#optional-methods> "Direct link to Optional methods")
These have sensible defaults in the ABC. Override as needed:
Method| Default| Override when  
---|---|---  
`on_session_start(session_id, **kwargs)`| No-op| You need to load persisted state (DAG, DB)  
`on_session_end(session_id, messages)`| No-op| You need to flush state, close connections  
`on_session_reset()`| Resets token counters| You have per-session state to clear  
`update_model(model, context_length, ...)`| Updates context_length + threshold| You need to recalculate budgets on model switch  
`get_tool_schemas()`| Returns `[]`| Your engine provides agent-callable tools (e.g., `lcm_grep`)  
`handle_tool_call(name, args, **kwargs)`| Returns error JSON| You implement tool handlers  
`should_compress_preflight(messages)`| Returns `False`| You can do a cheap pre-API-call estimate  
`get_status()`| Standard token/threshold dict| You have custom metrics to expose  
## Engine tools[​](<#engine-tools> "Direct link to Engine tools")
Context engines can expose tools the agent calls directly. Return schemas from `get_tool_schemas()` and handle calls in `handle_tool_call()`:
[code] 
    def get_tool_schemas(self):  
        return [{  
            "name": "lcm_grep",  
            "description": "Search the context knowledge graph",  
            "parameters": {  
                "type": "object",  
                "properties": {  
                    "query": {"type": "string", "description": "Search query"}  
                },  
                "required": ["query"],  
            },  
        }]  
      
    def handle_tool_call(self, name, args, **kwargs):  
        if name == "lcm_grep":  
            results = self._search_dag(args["query"])  
            return json.dumps({"results": results})  
        return json.dumps({"error": f"Unknown tool: {name}"})  
    
[/code]
Engine tools are injected into the agent's tool list at startup and dispatched automatically — no registry registration needed.
## Registration[​](<#registration> "Direct link to Registration")
### Via directory (recommended)[​](<#via-directory-recommended> "Direct link to Via directory \(recommended\)")
Place your engine in `plugins/context_engine/<name>/`. The `__init__.py` must export a `ContextEngine` subclass. The discovery system finds and instantiates it automatically.
### Via general plugin system[​](<#via-general-plugin-system> "Direct link to Via general plugin system")
A general plugin can also register a context engine:
[code] 
    def register(ctx):  
        engine = LCMEngine(context_length=200000)  
        ctx.register_context_engine(engine)  
    
[/code]
Only one engine can be registered. A second plugin attempting to register is rejected with a warning.
## Lifecycle[​](<#lifecycle> "Direct link to Lifecycle")
[code] 
    1. Engine instantiated (plugin load or directory discovery)  
    2. on_session_start() — conversation begins  
    3. update_from_response() — after each API call  
    4. should_compress() — checked each turn  
    5. compress() — called when should_compress() returns True  
    6. on_session_end() — session boundary (CLI exit, /reset, gateway expiry)  
    
[/code]
`on_session_reset()` is called on `/new` or `/reset` to clear per-session state without a full shutdown.
## Configuration[​](<#configuration> "Direct link to Configuration")
Users select your engine via `hermes plugins` → Provider Plugins → Context Engine, or by editing `config.yaml`:
[code] 
    context:  
      engine: "lcm"   # must match your engine's name property  
    
[/code]
The `compression` config block (`compression.threshold`, `compression.protect_last_n`, etc.) is specific to the built-in `ContextCompressor`. Your engine should define its own config format if needed, reading from `config.yaml` during initialization.
## Testing[​](<#testing> "Direct link to Testing")
[code] 
    from agent.context_engine import ContextEngine  
      
    def test_engine_satisfies_abc():  
        engine = YourEngine(context_length=200000)  
        assert isinstance(engine, ContextEngine)  
        assert engine.name == "your-name"  
      
    def test_compress_returns_valid_messages():  
        engine = YourEngine(context_length=200000)  
        msgs = [{"role": "user", "content": "hello"}]  
        result = engine.compress(msgs)  
        assert isinstance(result, list)  
        assert all("role" in m for m in result)  
    
[/code]
See `tests/agent/test_context_engine.py` for the full ABC contract test suite.
## See also[​](<#see-also> "Direct link to See also")
  * [Context Compression and Caching](</docs/developer-guide/context-compression-and-caching>) — how the built-in compressor works
  * [Memory Provider Plugins](</docs/developer-guide/memory-provider-plugin>) — analogous single-select plugin system for memory
  * [Plugins](</docs/user-guide/features/plugins>) — general plugin system overview


  * [How it works](<#how-it-works>)
  * [Directory structure](<#directory-structure>)
  * [The ContextEngine ABC](<#the-contextengine-abc>)
    * [Class attributes your engine must maintain](<#class-attributes-your-engine-must-maintain>)
    * [Optional methods](<#optional-methods>)
  * [Engine tools](<#engine-tools>)
  * [Registration](<#registration>)
    * [Via directory (recommended)](<#via-directory-recommended>)
    * [Via general plugin system](<#via-general-plugin-system>)
  * [Lifecycle](<#lifecycle>)
  * [Configuration](<#configuration>)
  * [Testing](<#testing>)
  * [See also](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin -->
