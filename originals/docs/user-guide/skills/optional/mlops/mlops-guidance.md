On this page
Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/guidance`  
Path| `optional-skills/mlops/guidance`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `guidance`, `transformers`  
Tags| `Prompt Engineering`, `Guidance`, `Constrained Generation`, `Structured Output`, `JSON Validation`, `Grammar`, `Microsoft Research`, `Format Enforcement`, `Multi-Step Workflows`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Guidance: Constrained LLM Generation
## When to Use This Skill[​](<#when-to-use-this-skill> "Direct link to When to Use This Skill")
Use Guidance when you need to:
  * **Control LLM output syntax** with regex or grammars
  * **Guarantee valid JSON/XML/code** generation
  * **Reduce latency** vs traditional prompting approaches
  * **Enforce structured formats** (dates, emails, IDs, etc.)
  * **Build multi-step workflows** with Pythonic control flow
  * **Prevent invalid outputs** through grammatical constraints


**GitHub Stars** : 18,000+ | **From** : Microsoft Research
## Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Base installation  
    pip install guidance  
      
    # With specific backends  
    pip install guidance[transformers]  # Hugging Face models  
    pip install guidance[llama_cpp]     # llama.cpp models  
    
[/code]
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
### Basic Example: Structured Generation[​](<#basic-example-structured-generation> "Direct link to Basic Example: Structured Generation")
[code] 
    from guidance import models, gen  
      
    # Load model (supports OpenAI, Transformers, llama.cpp)  
    lm = models.OpenAI("gpt-4")  
      
    # Generate with constraints  
    result = lm + "The capital of France is " + gen("capital", max_tokens=5)  
      
    print(result["capital"])  # "Paris"  
    
[/code]
### With Anthropic Claude[​](<#with-anthropic-claude> "Direct link to With Anthropic Claude")
[code] 
    from guidance import models, gen, system, user, assistant  
      
    # Configure Claude  
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    # Use context managers for chat format  
    with system():  
        lm += "You are a helpful assistant."  
      
    with user():  
        lm += "What is the capital of France?"  
      
    with assistant():  
        lm += gen(max_tokens=20)  
    
[/code]
## Core Concepts[​](<#core-concepts> "Direct link to Core Concepts")
### 1\. Context Managers[​](<#1-context-managers> "Direct link to 1. Context Managers")
Guidance uses Pythonic context managers for chat-style interactions.
[code] 
    from guidance import system, user, assistant, gen  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    # System message  
    with system():  
        lm += "You are a JSON generation expert."  
      
    # User message  
    with user():  
        lm += "Generate a person object with name and age."  
      
    # Assistant response  
    with assistant():  
        lm += gen("response", max_tokens=100)  
      
    print(lm["response"])  
    
[/code]
**Benefits:**
  * Natural chat flow
  * Clear role separation
  * Easy to read and maintain


### 2\. Constrained Generation[​](<#2-constrained-generation> "Direct link to 2. Constrained Generation")
Guidance ensures outputs match specified patterns using regex or grammars.
#### Regex Constraints[​](<#regex-constraints> "Direct link to Regex Constraints")
[code] 
    from guidance import models, gen  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    # Constrain to valid email format  
    lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")  
      
    # Constrain to date format (YYYY-MM-DD)  
    lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}")  
      
    # Constrain to phone number  
    lm += "Phone: " + gen("phone", regex=r"\d{3}-\d{3}-\d{4}")  
      
    print(lm["email"])  # Guaranteed valid email  
    print(lm["date"])   # Guaranteed YYYY-MM-DD format  
    
[/code]
**How it works:**
  * Regex converted to grammar at token level
  * Invalid tokens filtered during generation
  * Model can only produce matching outputs


#### Selection Constraints[​](<#selection-constraints> "Direct link to Selection Constraints")
[code] 
    from guidance import models, gen, select  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    # Constrain to specific choices  
    lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")  
      
    # Multiple-choice selection  
    lm += "Best answer: " + select(  
        ["A) Paris", "B) London", "C) Berlin", "D) Madrid"],  
        name="answer"  
    )  
      
    print(lm["sentiment"])  # One of: positive, negative, neutral  
    print(lm["answer"])     # One of: A, B, C, or D  
    
[/code]
### 3\. Token Healing[​](<#3-token-healing> "Direct link to 3. Token Healing")
Guidance automatically "heals" token boundaries between prompt and generation.
**Problem:** Tokenization creates unnatural boundaries.
[code] 
    # Without token healing  
    prompt = "The capital of France is "  
    # Last token: " is "  
    # First generated token might be " Par" (with leading space)  
    # Result: "The capital of France is  Paris" (double space!)  
    
[/code]
**Solution:** Guidance backs up one token and regenerates.
[code] 
    from guidance import models, gen  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    # Token healing enabled by default  
    lm += "The capital of France is " + gen("capital", max_tokens=5)  
    # Result: "The capital of France is Paris" (correct spacing)  
    
[/code]
**Benefits:**
  * Natural text boundaries
  * No awkward spacing issues
  * Better model performance (sees natural token sequences)


### 4\. Grammar-Based Generation[​](<#4-grammar-based-generation> "Direct link to 4. Grammar-Based Generation")
Define complex structures using context-free grammars.
[code] 
    from guidance import models, gen  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    # JSON grammar (simplified)  
    json_grammar = """  
    {  
        "name": <gen name regex="[A-Za-z ]+" max_tokens=20>,  
        "age": <gen age regex="[0-9]+" max_tokens=3>,  
        "email": <gen email regex="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" max_tokens=50>  
    }  
    """  
      
    # Generate valid JSON  
    lm += gen("person", grammar=json_grammar)  
      
    print(lm["person"])  # Guaranteed valid JSON structure  
    
[/code]
**Use cases:**
  * Complex structured outputs
  * Nested data structures
  * Programming language syntax
  * Domain-specific languages


### 5\. Guidance Functions[​](<#5-guidance-functions> "Direct link to 5. Guidance Functions")
Create reusable generation patterns with the `@guidance` decorator.
[code] 
    from guidance import guidance, gen, models  
      
    @guidance  
    def generate_person(lm):  
        """Generate a person with name and age."""  
        lm += "Name: " + gen("name", max_tokens=20, stop="\n")  
        lm += "\nAge: " + gen("age", regex=r"[0-9]+", max_tokens=3)  
        return lm  
      
    # Use the function  
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
    lm = generate_person(lm)  
      
    print(lm["name"])  
    print(lm["age"])  
    
[/code]
**Stateful Functions:**
[code] 
    @guidance(stateless=False)  
    def react_agent(lm, question, tools, max_rounds=5):  
        """ReAct agent with tool use."""  
        lm += f"Question: {question}\n\n"  
      
        for i in range(max_rounds):  
            # Thought  
            lm += f"Thought {i+1}: " + gen("thought", stop="\n")  
      
            # Action  
            lm += "\nAction: " + select(list(tools.keys()), name="action")  
      
            # Execute tool  
            tool_result = tools[lm["action"]]()  
            lm += f"\nObservation: {tool_result}\n\n"  
      
            # Check if done  
            lm += "Done? " + select(["Yes", "No"], name="done")  
            if lm["done"] == "Yes":  
                break  
      
        # Final answer  
        lm += "\nFinal Answer: " + gen("answer", max_tokens=100)  
        return lm  
    
[/code]
## Backend Configuration[​](<#backend-configuration> "Direct link to Backend Configuration")
### Anthropic Claude[​](<#anthropic-claude> "Direct link to Anthropic Claude")
[code] 
    from guidance import models  
      
    lm = models.Anthropic(  
        model="claude-sonnet-4-5-20250929",  
        api_key="your-api-key"  # Or set ANTHROPIC_API_KEY env var  
    )  
    
[/code]
### OpenAI[​](<#openai> "Direct link to OpenAI")
[code] 
    lm = models.OpenAI(  
        model="gpt-4o-mini",  
        api_key="your-api-key"  # Or set OPENAI_API_KEY env var  
    )  
    
[/code]
### Local Models (Transformers)[​](<#local-models-transformers> "Direct link to Local Models \(Transformers\)")
[code] 
    from guidance.models import Transformers  
      
    lm = Transformers(  
        "microsoft/Phi-4-mini-instruct",  
        device="cuda"  # Or "cpu"  
    )  
    
[/code]
### Local Models (llama.cpp)[​](<#local-models-llamacpp> "Direct link to Local Models \(llama.cpp\)")
[code] 
    from guidance.models import LlamaCpp  
      
    lm = LlamaCpp(  
        model_path="/path/to/model.gguf",  
        n_ctx=4096,  
        n_gpu_layers=35  
    )  
    
[/code]
## Common Patterns[​](<#common-patterns> "Direct link to Common Patterns")
### Pattern 1: JSON Generation[​](<#pattern-1-json-generation> "Direct link to Pattern 1: JSON Generation")
[code] 
    from guidance import models, gen, system, user, assistant  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    with system():  
        lm += "You generate valid JSON."  
      
    with user():  
        lm += "Generate a user profile with name, age, and email."  
      
    with assistant():  
        lm += """{  
        "name": """ + gen("name", regex=r'"[A-Za-z ]+"', max_tokens=30) + """,  
        "age": """ + gen("age", regex=r"[0-9]+", max_tokens=3) + """,  
        "email": """ + gen("email", regex=r'"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"', max_tokens=50) + """  
    }"""  
      
    print(lm)  # Valid JSON guaranteed  
    
[/code]
### Pattern 2: Classification[​](<#pattern-2-classification> "Direct link to Pattern 2: Classification")
[code] 
    from guidance import models, gen, select  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
      
    text = "This product is amazing! I love it."  
      
    lm += f"Text: {text}\n"  
    lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")  
    lm += "\nConfidence: " + gen("confidence", regex=r"[0-9]+", max_tokens=3) + "%"  
      
    print(f"Sentiment: {lm['sentiment']}")  
    print(f"Confidence: {lm['confidence']}%")  
    
[/code]
### Pattern 3: Multi-Step Reasoning[​](<#pattern-3-multi-step-reasoning> "Direct link to Pattern 3: Multi-Step Reasoning")
[code] 
    from guidance import models, gen, guidance  
      
    @guidance  
    def chain_of_thought(lm, question):  
        """Generate answer with step-by-step reasoning."""  
        lm += f"Question: {question}\n\n"  
      
        # Generate multiple reasoning steps  
        for i in range(3):  
            lm += f"Step {i+1}: " + gen(f"step_{i+1}", stop="\n", max_tokens=100) + "\n"  
      
        # Final answer  
        lm += "\nTherefore, the answer is: " + gen("answer", max_tokens=50)  
      
        return lm  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
    lm = chain_of_thought(lm, "What is 15% of 200?")  
      
    print(lm["answer"])  
    
[/code]
### Pattern 4: ReAct Agent[​](<#pattern-4-react-agent> "Direct link to Pattern 4: ReAct Agent")
[code] 
    from guidance import models, gen, select, guidance  
      
    @guidance(stateless=False)  
    def react_agent(lm, question):  
        """ReAct agent with tool use."""  
        tools = {  
            "calculator": lambda expr: eval(expr),  
            "search": lambda query: f"Search results for: {query}",  
        }  
      
        lm += f"Question: {question}\n\n"  
      
        for round in range(5):  
            # Thought  
            lm += f"Thought: " + gen("thought", stop="\n") + "\n"  
      
            # Action selection  
            lm += "Action: " + select(["calculator", "search", "answer"], name="action")  
      
            if lm["action"] == "answer":  
                lm += "\nFinal Answer: " + gen("answer", max_tokens=100)  
                break  
      
            # Action input  
            lm += "\nAction Input: " + gen("action_input", stop="\n") + "\n"  
      
            # Execute tool  
            if lm["action"] in tools:  
                result = tools[lm["action"]](lm["action_input"])  
                lm += f"Observation: {result}\n\n"  
      
        return lm  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
    lm = react_agent(lm, "What is 25 * 4 + 10?")  
    print(lm["answer"])  
    
[/code]
### Pattern 5: Data Extraction[​](<#pattern-5-data-extraction> "Direct link to Pattern 5: Data Extraction")
[code] 
    from guidance import models, gen, guidance  
      
    @guidance  
    def extract_entities(lm, text):  
        """Extract structured entities from text."""  
        lm += f"Text: {text}\n\n"  
      
        # Extract person  
        lm += "Person: " + gen("person", stop="\n", max_tokens=30) + "\n"  
      
        # Extract organization  
        lm += "Organization: " + gen("organization", stop="\n", max_tokens=30) + "\n"  
      
        # Extract date  
        lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}", max_tokens=10) + "\n"  
      
        # Extract location  
        lm += "Location: " + gen("location", stop="\n", max_tokens=30) + "\n"  
      
        return lm  
      
    text = "Tim Cook announced at Apple Park on 2024-09-15 in Cupertino."  
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")  
    lm = extract_entities(lm, text)  
      
    print(f"Person: {lm['person']}")  
    print(f"Organization: {lm['organization']}")  
    print(f"Date: {lm['date']}")  
    print(f"Location: {lm['location']}")  
    
[/code]
## Best Practices[​](<#best-practices> "Direct link to Best Practices")
### 1\. Use Regex for Format Validation[​](<#1-use-regex-for-format-validation> "Direct link to 1. Use Regex for Format Validation")
[code] 
    # ✅ Good: Regex ensures valid format  
    lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")  
      
    # ❌ Bad: Free generation may produce invalid emails  
    lm += "Email: " + gen("email", max_tokens=50)  
    
[/code]
### 2\. Use select() for Fixed Categories[​](<#2-use-select-for-fixed-categories> "Direct link to 2. Use select\(\) for Fixed Categories")
[code] 
    # ✅ Good: Guaranteed valid category  
    lm += "Status: " + select(["pending", "approved", "rejected"], name="status")  
      
    # ❌ Bad: May generate typos or invalid values  
    lm += "Status: " + gen("status", max_tokens=20)  
    
[/code]
### 3\. Leverage Token Healing[​](<#3-leverage-token-healing> "Direct link to 3. Leverage Token Healing")
[code] 
    # Token healing is enabled by default  
    # No special action needed - just concatenate naturally  
    lm += "The capital is " + gen("capital")  # Automatic healing  
    
[/code]
### 4\. Use stop Sequences[​](<#4-use-stop-sequences> "Direct link to 4. Use stop Sequences")
[code] 
    # ✅ Good: Stop at newline for single-line outputs  
    lm += "Name: " + gen("name", stop="\n")  
      
    # ❌ Bad: May generate multiple lines  
    lm += "Name: " + gen("name", max_tokens=50)  
    
[/code]
### 5\. Create Reusable Functions[​](<#5-create-reusable-functions> "Direct link to 5. Create Reusable Functions")
[code] 
    # ✅ Good: Reusable pattern  
    @guidance  
    def generate_person(lm):  
        lm += "Name: " + gen("name", stop="\n")  
        lm += "\nAge: " + gen("age", regex=r"[0-9]+")  
        return lm  
      
    # Use multiple times  
    lm = generate_person(lm)  
    lm += "\n\n"  
    lm = generate_person(lm)  
    
[/code]
### 6\. Balance Constraints[​](<#6-balance-constraints> "Direct link to 6. Balance Constraints")
[code] 
    # ✅ Good: Reasonable constraints  
    lm += gen("name", regex=r"[A-Za-z ]+", max_tokens=30)  
      
    # ❌ Too strict: May fail or be very slow  
    lm += gen("name", regex=r"^(John|Jane)$", max_tokens=10)  
    
[/code]
## Comparison to Alternatives[​](<#comparison-to-alternatives> "Direct link to Comparison to Alternatives")
Feature| Guidance| Instructor| Outlines| LMQL  
---|---|---|---|---  
Regex Constraints| ✅ Yes| ❌ No| ✅ Yes| ✅ Yes  
Grammar Support| ✅ CFG| ❌ No| ✅ CFG| ✅ CFG  
Pydantic Validation| ❌ No| ✅ Yes| ✅ Yes| ❌ No  
Token Healing| ✅ Yes| ❌ No| ✅ Yes| ❌ No  
Local Models| ✅ Yes| ⚠️ Limited| ✅ Yes| ✅ Yes  
API Models| ✅ Yes| ✅ Yes| ⚠️ Limited| ✅ Yes  
Pythonic Syntax| ✅ Yes| ✅ Yes| ✅ Yes| ❌ SQL-like  
Learning Curve| Low| Low| Medium| High  
**When to choose Guidance:**
  * Need regex/grammar constraints
  * Want token healing
  * Building complex workflows with control flow
  * Using local models (Transformers, llama.cpp)
  * Prefer Pythonic syntax


**When to choose alternatives:**
  * Instructor: Need Pydantic validation with automatic retrying
  * Outlines: Need JSON schema validation
  * LMQL: Prefer declarative query syntax


## Performance Characteristics[​](<#performance-characteristics> "Direct link to Performance Characteristics")
**Latency Reduction:**
  * 30-50% faster than traditional prompting for constrained outputs
  * Token healing reduces unnecessary regeneration
  * Grammar constraints prevent invalid token generation


**Memory Usage:**
  * Minimal overhead vs unconstrained generation
  * Grammar compilation cached after first use
  * Efficient token filtering at inference time


**Token Efficiency:**
  * Prevents wasted tokens on invalid outputs
  * No need for retry loops
  * Direct path to valid outputs


## Resources[​](<#resources> "Direct link to Resources")
  * **Documentation** : <https://guidance.readthedocs.io>
  * **GitHub** : <https://github.com/guidance-ai/guidance> (18k+ stars)
  * **Notebooks** : <https://github.com/guidance-ai/guidance/tree/main/notebooks>
  * **Discord** : Community support available


## See Also[​](<#see-also> "Direct link to See Also")
  * `references/constraints.md` \- Comprehensive regex and grammar patterns
  * `references/backends.md` \- Backend-specific configuration
  * `references/examples.md` \- Production-ready examples


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use This Skill](<#when-to-use-this-skill>)
  * [Installation](<#installation>)
  * [Quick Start](<#quick-start>)
    * [Basic Example: Structured Generation](<#basic-example-structured-generation>)
    * [With Anthropic Claude](<#with-anthropic-claude>)
  * [Core Concepts](<#core-concepts>)
    * [1\. Context Managers](<#1-context-managers>)
    * [2\. Constrained Generation](<#2-constrained-generation>)
    * [3\. Token Healing](<#3-token-healing>)
    * [4\. Grammar-Based Generation](<#4-grammar-based-generation>)
    * [5\. Guidance Functions](<#5-guidance-functions>)
  * [Backend Configuration](<#backend-configuration>)
    * [Anthropic Claude](<#anthropic-claude>)
    * [OpenAI](<#openai>)
    * [Local Models (Transformers)](<#local-models-transformers>)
    * [Local Models (llama.cpp)](<#local-models-llamacpp>)
  * [Common Patterns](<#common-patterns>)
    * [Pattern 1: JSON Generation](<#pattern-1-json-generation>)
    * [Pattern 2: Classification](<#pattern-2-classification>)
    * [Pattern 3: Multi-Step Reasoning](<#pattern-3-multi-step-reasoning>)
    * [Pattern 4: ReAct Agent](<#pattern-4-react-agent>)
    * [Pattern 5: Data Extraction](<#pattern-5-data-extraction>)
  * [Best Practices](<#best-practices>)
    * [1\. Use Regex for Format Validation](<#1-use-regex-for-format-validation>)
    * [2\. Use select() for Fixed Categories](<#2-use-select-for-fixed-categories>)
    * [3\. Leverage Token Healing](<#3-leverage-token-healing>)
    * [4\. Use stop Sequences](<#4-use-stop-sequences>)
    * [5\. Create Reusable Functions](<#5-create-reusable-functions>)
    * [6\. Balance Constraints](<#6-balance-constraints>)
  * [Comparison to Alternatives](<#comparison-to-alternatives>)
  * [Performance Characteristics](<#performance-characteristics>)
  * [Resources](<#resources>)
  * [See Also](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-guidance -->
