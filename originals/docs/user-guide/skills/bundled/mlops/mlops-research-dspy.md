On this page
DSPy: declarative LM programs, auto-optimize prompts, RAG.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/mlops/research/dspy`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `dspy`, `openai`, `anthropic`  
Tags| `Prompt Engineering`, `DSPy`, `Declarative Programming`, `RAG`, `Agents`, `Prompt Optimization`, `LM Programming`, `Stanford NLP`, `Automatic Optimization`, `Modular AI`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# DSPy: Declarative Language Model Programming
## When to Use This Skill[​](<#when-to-use-this-skill> "Direct link to When to Use This Skill")
Use DSPy when you need to:
  * **Build complex AI systems** with multiple components and workflows
  * **Program LMs declaratively** instead of manual prompt engineering
  * **Optimize prompts automatically** using data-driven methods
  * **Create modular AI pipelines** that are maintainable and portable
  * **Improve model outputs systematically** with optimizers
  * **Build RAG systems, agents, or classifiers** with better reliability


**GitHub Stars** : 22,000+ | **Created By** : Stanford NLP
## Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Stable release  
    pip install dspy  
      
    # Latest development version  
    pip install git+https://github.com/stanfordnlp/dspy.git  
      
    # With specific LM providers  
    pip install dspy[openai]        # OpenAI  
    pip install dspy[anthropic]     # Anthropic Claude  
    pip install dspy[all]           # All providers  
    
[/code]
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
### Basic Example: Question Answering[​](<#basic-example-question-answering> "Direct link to Basic Example: Question Answering")
[code] 
    import dspy  
      
    # Configure your language model  
    lm = dspy.Claude(model="claude-sonnet-4-5-20250929")  
    dspy.settings.configure(lm=lm)  
      
    # Define a signature (input → output)  
    class QA(dspy.Signature):  
        """Answer questions with short factual answers."""  
        question = dspy.InputField()  
        answer = dspy.OutputField(desc="often between 1 and 5 words")  
      
    # Create a module  
    qa = dspy.Predict(QA)  
      
    # Use it  
    response = qa(question="What is the capital of France?")  
    print(response.answer)  # "Paris"  
    
[/code]
### Chain of Thought Reasoning[​](<#chain-of-thought-reasoning> "Direct link to Chain of Thought Reasoning")
[code] 
    import dspy  
      
    lm = dspy.Claude(model="claude-sonnet-4-5-20250929")  
    dspy.settings.configure(lm=lm)  
      
    # Use ChainOfThought for better reasoning  
    class MathProblem(dspy.Signature):  
        """Solve math word problems."""  
        problem = dspy.InputField()  
        answer = dspy.OutputField(desc="numerical answer")  
      
    # ChainOfThought generates reasoning steps automatically  
    cot = dspy.ChainOfThought(MathProblem)  
      
    response = cot(problem="If John has 5 apples and gives 2 to Mary, how many does he have?")  
    print(response.rationale)  # Shows reasoning steps  
    print(response.answer)     # "3"  
    
[/code]
## Core Concepts[​](<#core-concepts> "Direct link to Core Concepts")
### 1\. Signatures[​](<#1-signatures> "Direct link to 1. Signatures")
Signatures define the structure of your AI task (inputs → outputs):
[code] 
    # Inline signature (simple)  
    qa = dspy.Predict("question -> answer")  
      
    # Class signature (detailed)  
    class Summarize(dspy.Signature):  
        """Summarize text into key points."""  
        text = dspy.InputField()  
        summary = dspy.OutputField(desc="bullet points, 3-5 items")  
      
    summarizer = dspy.ChainOfThought(Summarize)  
    
[/code]
**When to use each:**
  * **Inline** : Quick prototyping, simple tasks
  * **Class** : Complex tasks, type hints, better documentation


### 2\. Modules[​](<#2-modules> "Direct link to 2. Modules")
Modules are reusable components that transform inputs to outputs:
#### dspy.Predict[​](<#dspypredict> "Direct link to dspy.Predict")
Basic prediction module:
[code] 
    predictor = dspy.Predict("context, question -> answer")  
    result = predictor(context="Paris is the capital of France",  
                       question="What is the capital?")  
    
[/code]
#### dspy.ChainOfThought[​](<#dspychainofthought> "Direct link to dspy.ChainOfThought")
Generates reasoning steps before answering:
[code] 
    cot = dspy.ChainOfThought("question -> answer")  
    result = cot(question="Why is the sky blue?")  
    print(result.rationale)  # Reasoning steps  
    print(result.answer)     # Final answer  
    
[/code]
#### dspy.ReAct[​](<#dspyreact> "Direct link to dspy.ReAct")
Agent-like reasoning with tools:
[code] 
    from dspy.predict import ReAct  
      
    class SearchQA(dspy.Signature):  
        """Answer questions using search."""  
        question = dspy.InputField()  
        answer = dspy.OutputField()  
      
    def search_tool(query: str) -> str:  
        """Search Wikipedia."""  
        # Your search implementation  
        return results  
      
    react = ReAct(SearchQA, tools=[search_tool])  
    result = react(question="When was Python created?")  
    
[/code]
#### dspy.ProgramOfThought[​](<#dspyprogramofthought> "Direct link to dspy.ProgramOfThought")
Generates and executes code for reasoning:
[code] 
    pot = dspy.ProgramOfThought("question -> answer")  
    result = pot(question="What is 15% of 240?")  
    # Generates: answer = 240 * 0.15  
    
[/code]
### 3\. Optimizers[​](<#3-optimizers> "Direct link to 3. Optimizers")
Optimizers improve your modules automatically using training data:
#### BootstrapFewShot[​](<#bootstrapfewshot> "Direct link to BootstrapFewShot")
Learns from examples:
[code] 
    from dspy.teleprompt import BootstrapFewShot  
      
    # Training data  
    trainset = [  
        dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),  
        dspy.Example(question="What is 3+5?", answer="8").with_inputs("question"),  
    ]  
      
    # Define metric  
    def validate_answer(example, pred, trace=None):  
        return example.answer == pred.answer  
      
    # Optimize  
    optimizer = BootstrapFewShot(metric=validate_answer, max_bootstrapped_demos=3)  
    optimized_qa = optimizer.compile(qa, trainset=trainset)  
      
    # Now optimized_qa performs better!  
    
[/code]
#### MIPRO (Most Important Prompt Optimization)[​](<#mipro-most-important-prompt-optimization> "Direct link to MIPRO \(Most Important Prompt Optimization\)")
Iteratively improves prompts:
[code] 
    from dspy.teleprompt import MIPRO  
      
    optimizer = MIPRO(  
        metric=validate_answer,  
        num_candidates=10,  
        init_temperature=1.0  
    )  
      
    optimized_cot = optimizer.compile(  
        cot,  
        trainset=trainset,  
        num_trials=100  
    )  
    
[/code]
#### BootstrapFinetune[​](<#bootstrapfinetune> "Direct link to BootstrapFinetune")
Creates datasets for model fine-tuning:
[code] 
    from dspy.teleprompt import BootstrapFinetune  
      
    optimizer = BootstrapFinetune(metric=validate_answer)  
    optimized_module = optimizer.compile(qa, trainset=trainset)  
      
    # Exports training data for fine-tuning  
    
[/code]
### 4\. Building Complex Systems[​](<#4-building-complex-systems> "Direct link to 4. Building Complex Systems")
#### Multi-Stage Pipeline[​](<#multi-stage-pipeline> "Direct link to Multi-Stage Pipeline")
[code] 
    import dspy  
      
    class MultiHopQA(dspy.Module):  
        def __init__(self):  
            super().__init__()  
            self.retrieve = dspy.Retrieve(k=3)  
            self.generate_query = dspy.ChainOfThought("question -> search_query")  
            self.generate_answer = dspy.ChainOfThought("context, question -> answer")  
      
        def forward(self, question):  
            # Stage 1: Generate search query  
            search_query = self.generate_query(question=question).search_query  
      
            # Stage 2: Retrieve context  
            passages = self.retrieve(search_query).passages  
            context = "\n".join(passages)  
      
            # Stage 3: Generate answer  
            answer = self.generate_answer(context=context, question=question).answer  
            return dspy.Prediction(answer=answer, context=context)  
      
    # Use the pipeline  
    qa_system = MultiHopQA()  
    result = qa_system(question="Who wrote the book that inspired the movie Blade Runner?")  
    
[/code]
#### RAG System with Optimization[​](<#rag-system-with-optimization> "Direct link to RAG System with Optimization")
[code] 
    import dspy  
    from dspy.retrieve.chromadb_rm import ChromadbRM  
      
    # Configure retriever  
    retriever = ChromadbRM(  
        collection_name="documents",  
        persist_directory="./chroma_db"  
    )  
      
    class RAG(dspy.Module):  
        def __init__(self, num_passages=3):  
            super().__init__()  
            self.retrieve = dspy.Retrieve(k=num_passages)  
            self.generate = dspy.ChainOfThought("context, question -> answer")  
      
        def forward(self, question):  
            context = self.retrieve(question).passages  
            return self.generate(context=context, question=question)  
      
    # Create and optimize  
    rag = RAG()  
      
    # Optimize with training data  
    from dspy.teleprompt import BootstrapFewShot  
      
    optimizer = BootstrapFewShot(metric=validate_answer)  
    optimized_rag = optimizer.compile(rag, trainset=trainset)  
    
[/code]
## LM Provider Configuration[​](<#lm-provider-configuration> "Direct link to LM Provider Configuration")
### Anthropic Claude[​](<#anthropic-claude> "Direct link to Anthropic Claude")
[code] 
    import dspy  
      
    lm = dspy.Claude(  
        model="claude-sonnet-4-5-20250929",  
        api_key="your-api-key",  # Or set ANTHROPIC_API_KEY env var  
        max_tokens=1000,  
        temperature=0.7  
    )  
    dspy.settings.configure(lm=lm)  
    
[/code]
### OpenAI[​](<#openai> "Direct link to OpenAI")
[code] 
    lm = dspy.OpenAI(  
        model="gpt-4",  
        api_key="your-api-key",  
        max_tokens=1000  
    )  
    dspy.settings.configure(lm=lm)  
    
[/code]
### Local Models (Ollama)[​](<#local-models-ollama> "Direct link to Local Models \(Ollama\)")
[code] 
    lm = dspy.OllamaLocal(  
        model="llama3.1",  
        base_url="http://localhost:11434"  
    )  
    dspy.settings.configure(lm=lm)  
    
[/code]
### Multiple Models[​](<#multiple-models> "Direct link to Multiple Models")
[code] 
    # Different models for different tasks  
    cheap_lm = dspy.OpenAI(model="gpt-3.5-turbo")  
    strong_lm = dspy.Claude(model="claude-sonnet-4-5-20250929")  
      
    # Use cheap model for retrieval, strong model for reasoning  
    with dspy.settings.context(lm=cheap_lm):  
        context = retriever(question)  
      
    with dspy.settings.context(lm=strong_lm):  
        answer = generator(context=context, question=question)  
    
[/code]
## Common Patterns[​](<#common-patterns> "Direct link to Common Patterns")
### Pattern 1: Structured Output[​](<#pattern-1-structured-output> "Direct link to Pattern 1: Structured Output")
[code] 
    from pydantic import BaseModel, Field  
      
    class PersonInfo(BaseModel):  
        name: str = Field(description="Full name")  
        age: int = Field(description="Age in years")  
        occupation: str = Field(description="Current job")  
      
    class ExtractPerson(dspy.Signature):  
        """Extract person information from text."""  
        text = dspy.InputField()  
        person: PersonInfo = dspy.OutputField()  
      
    extractor = dspy.TypedPredictor(ExtractPerson)  
    result = extractor(text="John Doe is a 35-year-old software engineer.")  
    print(result.person.name)  # "John Doe"  
    print(result.person.age)   # 35  
    
[/code]
### Pattern 2: Assertion-Driven Optimization[​](<#pattern-2-assertion-driven-optimization> "Direct link to Pattern 2: Assertion-Driven Optimization")
[code] 
    import dspy  
    from dspy.primitives.assertions import assert_transform_module, backtrack_handler  
      
    class MathQA(dspy.Module):  
        def __init__(self):  
            super().__init__()  
            self.solve = dspy.ChainOfThought("problem -> solution: float")  
      
        def forward(self, problem):  
            solution = self.solve(problem=problem).solution  
      
            # Assert solution is numeric  
            dspy.Assert(  
                isinstance(float(solution), float),  
                "Solution must be a number",  
                backtrack=backtrack_handler  
            )  
      
            return dspy.Prediction(solution=solution)  
    
[/code]
### Pattern 3: Self-Consistency[​](<#pattern-3-self-consistency> "Direct link to Pattern 3: Self-Consistency")
[code] 
    import dspy  
    from collections import Counter  
      
    class ConsistentQA(dspy.Module):  
        def __init__(self, num_samples=5):  
            super().__init__()  
            self.qa = dspy.ChainOfThought("question -> answer")  
            self.num_samples = num_samples  
      
        def forward(self, question):  
            # Generate multiple answers  
            answers = []  
            for _ in range(self.num_samples):  
                result = self.qa(question=question)  
                answers.append(result.answer)  
      
            # Return most common answer  
            most_common = Counter(answers).most_common(1)[0][0]  
            return dspy.Prediction(answer=most_common)  
    
[/code]
### Pattern 4: Retrieval with Reranking[​](<#pattern-4-retrieval-with-reranking> "Direct link to Pattern 4: Retrieval with Reranking")
[code] 
    class RerankedRAG(dspy.Module):  
        def __init__(self):  
            super().__init__()  
            self.retrieve = dspy.Retrieve(k=10)  
            self.rerank = dspy.Predict("question, passage -> relevance_score: float")  
            self.answer = dspy.ChainOfThought("context, question -> answer")  
      
        def forward(self, question):  
            # Retrieve candidates  
            passages = self.retrieve(question).passages  
      
            # Rerank passages  
            scored = []  
            for passage in passages:  
                score = float(self.rerank(question=question, passage=passage).relevance_score)  
                scored.append((score, passage))  
      
            # Take top 3  
            top_passages = [p for _, p in sorted(scored, reverse=True)[:3]]  
            context = "\n\n".join(top_passages)  
      
            # Generate answer  
            return self.answer(context=context, question=question)  
    
[/code]
## Evaluation and Metrics[​](<#evaluation-and-metrics> "Direct link to Evaluation and Metrics")
### Custom Metrics[​](<#custom-metrics> "Direct link to Custom Metrics")
[code] 
    def exact_match(example, pred, trace=None):  
        """Exact match metric."""  
        return example.answer.lower() == pred.answer.lower()  
      
    def f1_score(example, pred, trace=None):  
        """F1 score for text overlap."""  
        pred_tokens = set(pred.answer.lower().split())  
        gold_tokens = set(example.answer.lower().split())  
      
        if not pred_tokens:  
            return 0.0  
      
        precision = len(pred_tokens & gold_tokens) / len(pred_tokens)  
        recall = len(pred_tokens & gold_tokens) / len(gold_tokens)  
      
        if precision + recall == 0:  
            return 0.0  
      
        return 2 * (precision * recall) / (precision + recall)  
    
[/code]
### Evaluation[​](<#evaluation> "Direct link to Evaluation")
[code] 
    from dspy.evaluate import Evaluate  
      
    # Create evaluator  
    evaluator = Evaluate(  
        devset=testset,  
        metric=exact_match,  
        num_threads=4,  
        display_progress=True  
    )  
      
    # Evaluate model  
    score = evaluator(qa_system)  
    print(f"Accuracy: {score}")  
      
    # Compare optimized vs unoptimized  
    score_before = evaluator(qa)  
    score_after = evaluator(optimized_qa)  
    print(f"Improvement: {score_after - score_before:.2%}")  
    
[/code]
## Best Practices[​](<#best-practices> "Direct link to Best Practices")
### 1\. Start Simple, Iterate[​](<#1-start-simple-iterate> "Direct link to 1. Start Simple, Iterate")
[code] 
    # Start with Predict  
    qa = dspy.Predict("question -> answer")  
      
    # Add reasoning if needed  
    qa = dspy.ChainOfThought("question -> answer")  
      
    # Add optimization when you have data  
    optimized_qa = optimizer.compile(qa, trainset=data)  
    
[/code]
### 2\. Use Descriptive Signatures[​](<#2-use-descriptive-signatures> "Direct link to 2. Use Descriptive Signatures")
[code] 
    # ❌ Bad: Vague  
    class Task(dspy.Signature):  
        input = dspy.InputField()  
        output = dspy.OutputField()  
      
    # ✅ Good: Descriptive  
    class SummarizeArticle(dspy.Signature):  
        """Summarize news articles into 3-5 key points."""  
        article = dspy.InputField(desc="full article text")  
        summary = dspy.OutputField(desc="bullet points, 3-5 items")  
    
[/code]
### 3\. Optimize with Representative Data[​](<#3-optimize-with-representative-data> "Direct link to 3. Optimize with Representative Data")
[code] 
    # Create diverse training examples  
    trainset = [  
        dspy.Example(question="factual", answer="...).with_inputs("question"),  
        dspy.Example(question="reasoning", answer="...").with_inputs("question"),  
        dspy.Example(question="calculation", answer="...").with_inputs("question"),  
    ]  
      
    # Use validation set for metric  
    def metric(example, pred, trace=None):  
        return example.answer in pred.answer  
    
[/code]
### 4\. Save and Load Optimized Models[​](<#4-save-and-load-optimized-models> "Direct link to 4. Save and Load Optimized Models")
[code] 
    # Save  
    optimized_qa.save("models/qa_v1.json")  
      
    # Load  
    loaded_qa = dspy.ChainOfThought("question -> answer")  
    loaded_qa.load("models/qa_v1.json")  
    
[/code]
### 5\. Monitor and Debug[​](<#5-monitor-and-debug> "Direct link to 5. Monitor and Debug")
[code] 
    # Enable tracing  
    dspy.settings.configure(lm=lm, trace=[])  
      
    # Run prediction  
    result = qa(question="...")  
      
    # Inspect trace  
    for call in dspy.settings.trace:  
        print(f"Prompt: {call['prompt']}")  
        print(f"Response: {call['response']}")  
    
[/code]
## Comparison to Other Approaches[​](<#comparison-to-other-approaches> "Direct link to Comparison to Other Approaches")
Feature| Manual Prompting| LangChain| DSPy  
---|---|---|---  
Prompt Engineering| Manual| Manual| Automatic  
Optimization| Trial & error| None| Data-driven  
Modularity| Low| Medium| High  
Type Safety| No| Limited| Yes (Signatures)  
Portability| Low| Medium| High  
Learning Curve| Low| Medium| Medium-High  
**When to choose DSPy:**
  * You have training data or can generate it
  * You need systematic prompt improvement
  * You're building complex multi-stage systems
  * You want to optimize across different LMs


**When to choose alternatives:**
  * Quick prototypes (manual prompting)
  * Simple chains with existing tools (LangChain)
  * Custom optimization logic needed


## Resources[​](<#resources> "Direct link to Resources")
  * **Documentation** : <https://dspy.ai>
  * **GitHub** : <https://github.com/stanfordnlp/dspy> (22k+ stars)
  * **Discord** : <https://discord.gg/XCGy2WDCQB>
  * **Twitter** : @DSPyOSS
  * **Paper** : "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"


## See Also[​](<#see-also> "Direct link to See Also")
  * `references/modules.md` \- Detailed module guide (Predict, ChainOfThought, ReAct, ProgramOfThought)
  * `references/optimizers.md` \- Optimization algorithms (BootstrapFewShot, MIPRO, BootstrapFinetune)
  * `references/examples.md` \- Real-world examples (RAG, agents, classifiers)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use This Skill](<#when-to-use-this-skill>)
  * [Installation](<#installation>)
  * [Quick Start](<#quick-start>)
    * [Basic Example: Question Answering](<#basic-example-question-answering>)
    * [Chain of Thought Reasoning](<#chain-of-thought-reasoning>)
  * [Core Concepts](<#core-concepts>)
    * [1\. Signatures](<#1-signatures>)
    * [2\. Modules](<#2-modules>)
    * [3\. Optimizers](<#3-optimizers>)
    * [4\. Building Complex Systems](<#4-building-complex-systems>)
  * [LM Provider Configuration](<#lm-provider-configuration>)
    * [Anthropic Claude](<#anthropic-claude>)
    * [OpenAI](<#openai>)
    * [Local Models (Ollama)](<#local-models-ollama>)
    * [Multiple Models](<#multiple-models>)
  * [Common Patterns](<#common-patterns>)
    * [Pattern 1: Structured Output](<#pattern-1-structured-output>)
    * [Pattern 2: Assertion-Driven Optimization](<#pattern-2-assertion-driven-optimization>)
    * [Pattern 3: Self-Consistency](<#pattern-3-self-consistency>)
    * [Pattern 4: Retrieval with Reranking](<#pattern-4-retrieval-with-reranking>)
  * [Evaluation and Metrics](<#evaluation-and-metrics>)
    * [Custom Metrics](<#custom-metrics>)
    * [Evaluation](<#evaluation>)
  * [Best Practices](<#best-practices>)
    * [1\. Start Simple, Iterate](<#1-start-simple-iterate>)
    * [2\. Use Descriptive Signatures](<#2-use-descriptive-signatures>)
    * [3\. Optimize with Representative Data](<#3-optimize-with-representative-data>)
    * [4\. Save and Load Optimized Models](<#4-save-and-load-optimized-models>)
    * [5\. Monitor and Debug](<#5-monitor-and-debug>)
  * [Comparison to Other Approaches](<#comparison-to-other-approaches>)
  * [Resources](<#resources>)
  * [See Also](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-research-dspy -->
