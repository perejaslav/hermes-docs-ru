На этой странице
DSPy: декларативные LM-программы, авто-оптимизация промптов, RAG.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Встроенный (установлен по умолчанию) |
|Путь| `skills/mlops/research/dspy` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `dspy`, `openai`, `anthropic` |
|Теги| `Prompt Engineering`, `DSPy`, `Declarative Programming`, `RAG`, `Agents`, `Prompt Optimization`, `LM Programming`, `Stanford NLP`, `Automatic Optimization`, `Modular AI` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.
# DSPy: Декларативное программирование языковых моделей
## Когда использовать этот навык[​](<#when-to-use-this-skill> "Прямая ссылка на Когда использовать этот навык")
Используйте DSPy, когда вам нужно:
  * **Создавать сложные AI-системы** с несколькими компонентами и рабочими процессами
  * **Программировать LM декларативно** вместо ручной инженерии промптов
  * **Автоматически оптимизировать промпты** с помощью методов, основанных на данных
  * **Создавать модульные AI-конвейеры**, которые поддерживаемы и переносимы
  * **Систематически улучшать выходные данные моделей** с помощью оптимизаторов
  * **Строить RAG-системы, агентов или классификаторы** с повышенной надёжностью


**Звёзд на GitHub**: 22 000+ | **Создатель**: Stanford NLP
## Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Стабильный релиз  
    pip install dspy  
      
    # Последняя версия для разработки  
    pip install git+https://github.com/stanfordnlp/dspy.git  
      
    # С конкретными LM-провайдерами  
    pip install dspy[openai]        # OpenAI  
    pip install dspy[anthropic]     # Anthropic Claude  
    pip install dspy[all]           # Все провайдеры  
    
[/code]
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Базовый пример: Ответы на вопросы[​](<#basic-example-question-answering> "Прямая ссылка на Базовый пример: Ответы на вопросы")
[code] 
    import dspy  
      
    # Настройка языковой модели  
    lm = dspy.Claude(model="claude-sonnet-4-5-20250929")  
    dspy.settings.configure(lm=lm)  
      
    # Определение сигнатуры (вход → выход)  
    class QA(dspy.Signature):  
        """Answer questions with short factual answers."""  
        question = dspy.InputField()  
        answer = dspy.OutputField(desc="often between 1 and 5 words")  
      
    # Создание модуля  
    qa = dspy.Predict(QA)  
      
    # Использование  
    response = qa(question="What is the capital of France?")  
    print(response.answer)  # "Paris"  
    
[/code]
### Цепочка рассуждений (Chain of Thought)[​](<#chain-of-thought-reasoning> "Прямая ссылка на Цепочка рассуждений (Chain of Thought)")
[code] 
    import dspy  
      
    lm = dspy.Claude(model="claude-sonnet-4-5-20250929")  
    dspy.settings.configure(lm=lm)  
      
    # Использование ChainOfThought для лучшего рассуждения  
    class MathProblem(dspy.Signature):  
        """Solve math word problems."""  
        problem = dspy.InputField()  
        answer = dspy.OutputField(desc="numerical answer")  
      
    # ChainOfThought генерирует шаги рассуждения автоматически  
    cot = dspy.ChainOfThought(MathProblem)  
      
    response = cot(problem="If John has 5 apples and gives 2 to Mary, how many does he have?")  
    print(response.rationale)  # Показывает шаги рассуждения  
    print(response.answer)     # "3"  
    
[/code]
## Основные концепции[​](<#core-concepts> "Прямая ссылка на Основные концепции")
### 1\\. Сигнатуры[​](<#1-signatures> "Прямая ссылка на 1. Сигнатуры")
Сигнатуры определяют структуру вашей AI-задачи (входы → выходы):
[code] 
    # Встроенная сигнатура (простая)  
    qa = dspy.Predict("question -> answer")  
      
    # Сигнатура класса (подробная)  
    class Summarize(dspy.Signature):  
        """Summarize text into key points."""  
        text = dspy.InputField()  
        summary = dspy.OutputField(desc="bullet points, 3-5 items")  
      
    summarizer = dspy.ChainOfThought(Summarize)  
    
[/code]
**Когда что использовать:**
  * **Встроенная**: Быстрое прототипирование, простые задачи
  * **Класс**: Сложные задачи, подсказки типов, лучшая документация


### 2\\. Модули[​](<#2-modules> "Прямая ссылка на 2. Модули")
Модули — это переиспользуемые компоненты, преобразующие входы в выходы:
#### dspy.Predict[​](<#dspypredict> "Прямая ссылка на dspy.Predict")
Базовый модуль предсказания:
[code] 
    predictor = dspy.Predict("context, question -> answer")  
    result = predictor(context="Paris is the capital of France",  
                       question="What is the capital?")  
    
[/code]
#### dspy.ChainOfThought[​](<#dspychainofthought> "Прямая ссылка на dspy.ChainOfThought")
Генерирует шаги рассуждения перед ответом:
[code] 
    cot = dspy.ChainOfThought("question -> answer")  
    result = cot(question="Why is the sky blue?")  
    print(result.rationale)  # Шаги рассуждения  
    print(result.answer)     # Финальный ответ  
    
[/code]
#### dspy.ReAct[​](<#dspyreact> "Прямая ссылка на dspy.ReAct")
Агентоподобное рассуждение с инструментами:
[code] 
    from dspy.predict import ReAct  
      
    class SearchQA(dspy.Signature):  
        """Answer questions using search."""  
        question = dspy.InputField()  
        answer = dspy.OutputField()  
      
    def search_tool(query: str) -> str:  
        """Search Wikipedia."""  
        # Ваша реализация поиска  
        return results  
      
    react = ReAct(SearchQA, tools=[search_tool])  
    result = react(question="When was Python created?")  
    
[/code]
#### dspy.ProgramOfThought[​](<#dspyprogramofthought> "Прямая ссылка на dspy.ProgramOfThought")
Генерирует и выполняет код для рассуждения:
[code] 
    pot = dspy.ProgramOfThought("question -> answer")  
    result = pot(question="What is 15% of 240?")  
    # Генерирует: answer = 240 * 0.15  
    
[/code]
### 3\\. Оптимизаторы[​](<#3-optimizers> "Прямая ссылка на 3. Оптимизаторы")
Оптимизаторы автоматически улучшают ваши модули, используя обучающие данные:
#### BootstrapFewShot[​](<#bootstrapfewshot> "Прямая ссылка на BootstrapFewShot")
Обучение на примерах:
[code] 
    from dspy.teleprompt import BootstrapFewShot  
      
    # Обучающие данные  
    trainset = [  
        dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),  
        dspy.Example(question="What is 3+5?", answer="8").with_inputs("question"),  
    ]  
      
    # Определение метрики  
    def validate_answer(example, pred, trace=None):  
        return example.answer == pred.answer  
      
    # Оптимизация  
    optimizer = BootstrapFewShot(metric=validate_answer, max_bootstrapped_demos=3)  
    optimized_qa = optimizer.compile(qa, trainset=trainset)  
      
    # Теперь optimized_qa работает лучше!  
    
[/code]
#### MIPRO (Оптимизация наиболее важных промптов)[​](<#mipro-most-important-prompt-optimization> "Прямая ссылка на MIPRO (Оптимизация наиболее важных промптов)")
Итеративное улучшение промптов:
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
#### BootstrapFinetune[​](<#bootstrapfinetune> "Прямая ссылка на BootstrapFinetune")
Создание наборов данных для тонкой настройки модели:
[code] 
    from dspy.teleprompt import BootstrapFinetune  
      
    optimizer = BootstrapFinetune(metric=validate_answer)  
    optimized_module = optimizer.compile(qa, trainset=trainset)  
      
    # Экспортирует обучающие данные для тонкой настройки  
    
[/code]
### 4\\. Построение сложных систем[​](<#4-building-complex-systems> "Прямая ссылка на 4. Построение сложных систем")
#### Многоступенчатый конвейер[​](<#multi-stage-pipeline> "Прямая ссылка на Многоступенчатый конвейер")
[code] 
    import dspy  
      
    class MultiHopQA(dspy.Module):  
        def __init__(self):  
            super().__init__()  
            self.retrieve = dspy.Retrieve(k=3)  
            self.generate_query = dspy.ChainOfThought("question -> search_query")  
            self.generate_answer = dspy.ChainOfThought("context, question -> answer")  
      
        def forward(self, question):  
            # Этап 1: Генерация поискового запроса  
            search_query = self.generate_query(question=question).search_query  
      
            # Этап 2: Получение контекста  
            passages = self.retrieve(search_query).passages  
            context = "\n".join(passages)  
      
            # Этап 3: Генерация ответа  
            answer = self.generate_answer(context=context, question=question).answer  
            return dspy.Prediction(answer=answer, context=context)  
      
    # Использование конвейера  
    qa_system = MultiHopQA()  
    result = qa_system(question="Who wrote the book that inspired the movie Blade Runner?")  
    
[/code]
#### RAG-система с оптимизацией[​](<#rag-system-with-optimization> "Прямая ссылка на RAG-система с оптимизацией")
[code] 
    import dspy  
    from dspy.retrieve.chromadb_rm import ChromadbRM  
      
    # Настройка поисковика  
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
      
    # Создание и оптимизация  
    rag = RAG()  
      
    # Оптимизация с обучающими данными  
    from dspy.teleprompt import BootstrapFewShot  
      
    optimizer = BootstrapFewShot(metric=validate_answer)  
    optimized_rag = optimizer.compile(rag, trainset=trainset)  
    
[/code]
## Конфигурация LM-провайдеров[​](<#lm-provider-configuration> "Прямая ссылка на Конфигурация LM-провайдеров")
### Anthropic Claude[​](<#anthropic-claude> "Прямая ссылка на Anthropic Claude")
[code] 
    import dspy  
      
    lm = dspy.Claude(  
        model="claude-sonnet-4-5-20250929",  
        api_key="your-api-key",  # Или установите переменную окружения ANTHROPIC_API_KEY  
        max_tokens=1000,  
        temperature=0.7  
    )  
    dspy.settings.configure(lm=lm)  
    
[/code]
### OpenAI[​](<#openai> "Прямая ссылка на OpenAI")
[code] 
    lm = dspy.OpenAI(  
        model="gpt-4",  
        api_key="your-api-key",  
        max_tokens=1000  
    )  
    dspy.settings.configure(lm=lm)  
    
[/code]
### Локальные модели (Ollama)[​](<#local-models-ollama> "Прямая ссылка на Локальные модели (Ollama)")
[code] 
    lm = dspy.OllamaLocal(  
        model="llama3.1",  
        base_url="http://localhost:11434"  
    )  
    dspy.settings.configure(lm=lm)  
    
[/code]
### Несколько моделей[​](<#multiple-models> "Прямая ссылка на Несколько моделей")
[code] 
    # Разные модели для разных задач  
    cheap_lm = dspy.OpenAI(model="gpt-3.5-turbo")  
    strong_lm = dspy.Claude(model="claude-sonnet-4-5-20250929")  
      
    # Использование дешёвой модели для поиска, сильной — для рассуждения  
    with dspy.settings.context(lm=cheap_lm):  
        context = retriever(question)  
      
    with dspy.settings.context(lm=strong_lm):  
        answer = generator(context=context, question=question)  
    
[/code]
## Типовые паттерны[​](<#common-patterns> "Прямая ссылка на Типовые паттерны")
### Паттерн 1: Структурированный вывод[​](<#pattern-1-structured-output> "Прямая ссылка на Паттерн 1: Структурированный вывод")
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
### Паттерн 2: Оптимизация на основе утверждений[​](<#pattern-2-assertion-driven-optimization> "Прямая ссылка на Паттерн 2: Оптимизация на основе утверждений")
[code] 
    import dspy  
    from dspy.primitives.assertions import assert_transform_module, backtrack_handler  
      
    class MathQA(dspy.Module):  
        def __init__(self):  
            super().__init__()  
            self.solve = dspy.ChainOfThought("problem -> solution: float")  
      
        def forward(self, problem):  
            solution = self.solve(problem=problem).solution  
      
            # Утверждение, что решение является числом  
            dspy.Assert(  
                isinstance(float(solution), float),  
                "Solution must be a number",  
                backtrack=backtrack_handler  
            )  
      
            return dspy.Prediction(solution=solution)  
    
[/code]
### Паттерн 3: Самосогласованность[​](<#pattern-3-self-consistency> "Прямая ссылка на Паттерн 3: Самосогласованность")
[code] 
    import dspy  
    from collections import Counter  
      
    class ConsistentQA(dspy.Module):  
        def __init__(self, num_samples=5):  
            super().__init__()  
            self.qa = dspy.ChainOfThought("question -> answer")  
            self.num_samples = num_samples  
      
        def forward(self, question):  
            # Генерация нескольких ответов  
            answers = []  
            for _ in range(self.num_samples):  
                result = self.qa(question=question)  
                answers.append(result.answer)  
      
            # Возврат самого частого ответа  
            most_common = Counter(answers).most_common(1)[0][0]  
            return dspy.Prediction(answer=most_common)  
    
[/code]
### Паттерн 4: Поиск с переранжированием[​](<#pattern-4-retrieval-with-reranking> "Прямая ссылка на Паттерн 4: Поиск с переранжированием")
[code] 
    class RerankedRAG(dspy.Module):  
        def __init__(self):  
            super().__init__()  
            self.retrieve = dspy.Retrieve(k=10)  
            self.rerank = dspy.Predict("question, passage -> relevance_score: float")  
            self.answer = dspy.ChainOfThought("context, question -> answer")  
      
        def forward(self, question):  
            # Поиск кандидатов  
            passages = self.retrieve(question).passages  
      
            # Переранжирование фрагментов  
            scored = []  
            for passage in passages:  
                score = float(self.rerank(question=question, passage=passage).relevance_score)  
                scored.append((score, passage))  
      
            # Выбор топ-3  
            top_passages = [p for _, p in sorted(scored, reverse=True)[:3]]  
            context = "\n\n".join(top_passages)  
      
            # Генерация ответа  
            return self.answer(context=context, question=question)  
    
[/code]
## Оценка и метрики[​](<#evaluation-and-metrics> "Прямая ссылка на Оценка и метрики")
### Пользовательские метрики[​](<#custom-metrics> "Прямая ссылка на Пользовательские метрики")
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
### Оценка[​](<#evaluation> "Прямая ссылка на Оценка")
[code] 
    from dspy.evaluate import Evaluate  
      
    # Создание оценщика  
    evaluator = Evaluate(  
        devset=testset,  
        metric=exact_match,  
        num_threads=4,  
        display_progress=True  
    )  
      
    # Оценка модели  
    score = evaluator(qa_system)  
    print(f"Accuracy: {score}")  
      
    # Сравнение оптимизированной и неоптимизированной версий  
    score_before = evaluator(qa)  
    score_after = evaluator(optimized_qa)  
    print(f"Improvement: {score_after - score_before:.2%}")  
    
[/code]
## Лучшие практики[​](<#best-practices> "Прямая ссылка на Лучшие практики")
### 1\\. Начинайте с простого, итерируйте[​](<#1-start-simple-iterate> "Прямая ссылка на 1. Начинайте с простого, итерируйте")
[code] 
    # Начните с Predict  
    qa = dspy.Predict("question -> answer")  
      
    # Добавьте рассуждение при необходимости  
    qa = dspy.ChainOfThought("question -> answer")  
      
    # Добавьте оптимизацию, когда появятся данные  
    optimized_qa = optimizer.compile(qa, trainset=data)  
    
[/code]
### 2\\. Используйте описательные сигнатуры[​](<#2-use-descriptive-signatures> "Прямая ссылка на 2. Используйте описательные сигнатуры")
[code] 
    # ❌ Плохо: Непонятно  
    class Task(dspy.Signature):  
        input = dspy.InputField()  
        output = dspy.OutputField()  
      
    # ✅ Хорошо: Описательно  
    class SummarizeArticle(dspy.Signature):  
        """Summarize news articles into 3-5 key points."""  
        article = dspy.InputField(desc="full article text")  
        summary = dspy.OutputField(desc="bullet points, 3-5 items")  
    
[/code]
### 3\\. Оптимизируйте на репрезентативных данных[​](<#3-optimize-with-representative-data> "Прямая ссылка на 3. Оптимизируйте на репрезентативных данных")
[code] 
    # Создание разнообразных обучающих примеров  
    trainset = [  
        dspy.Example(question="factual", answer="...).with_inputs("question"),  
        dspy.Example(question="reasoning", answer="...").with_inputs("question"),  
        dspy.Example(question="calculation", answer="...").with_inputs("question"),  
    ]  
      
    # Использование валидационного набора для метрики  
    def metric(example, pred, trace=None):  
        return example.answer in pred.answer  
    
[/code]
### 4\\. Сохраняйте и загружайте оптимизированные модели[​](<#4-save-and-load-optimized-models> "Прямая ссылка на 4. Сохраняйте и загружайте оптимизированные модели")
[code] 
    # Сохранение  
    optimized_qa.save("models/qa_v1.json")  
      
    # Загрузка  
    loaded_qa = dspy.ChainOfThought("question -> answer")  
    loaded_qa.load("models/qa_v1.json")  
    
[/code]
### 5\\. Мониторинг и отладка[​](<#5-monitor-and-debug> "Прямая ссылка на 5. Мониторинг и отладка")
[code] 
    # Включение трассировки  
    dspy.settings.configure(lm=lm, trace=[])  
      
    # Запуск предсказания  
    result = qa(question="...")  
      
    # Просмотр трассировки  
    for call in dspy.settings.trace:  
        print(f"Prompt: {call['prompt']}")  
        print(f"Response: {call['response']}")  
    
[/code]
## Сравнение с другими подходами[​](<#comparison-to-other-approaches> "Прямая ссылка на Сравнение с другими подходами")
| Функция | Ручное написание промптов | LangChain | DSPy |
|---|---|---|---|
|Инженерия промптов| Вручную| Вручную| Автоматически|
|Оптимизация| Проб и ошибок| Нет| На основе данных|
|Модульность| Низкая| Средняя| Высокая|
|Типобезопасность| Нет| Ограниченная| Да (сигнатуры)|
|Переносимость| Низкая| Средняя| Высокая|
|Порог входа| Низкий| Средний| Средне-высокий|
**Когда выбирать DSPy:**
  * У вас есть обучающие данные или возможность их сгенерировать
  * Вам нужно систематическое улучшение промптов
  * Вы строите сложные многоступенчатые системы
  * Вы хотите оптимизировать для разных LM


**Когда выбирать альтернативы:**
  * Быстрые прототипы (ручное написание промптов)
  * Простые цепочки с существующими инструментами (LangChain)
  * Когда нужна собственная логика оптимизации


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **Документация**: <https://dspy.ai>
  * **GitHub**: <https://github.com/stanfordnlp/dspy> (22k+ звёзд)
  * **Discord**: <https://discord.gg/XCGy2WDCQB>
  * **Twitter**: @DSPyOSS
  * **Статья**: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"


## См. также[​](<#see-also> "Прямая ссылка на См. также")
  * `references/modules.md` — Подробное руководство по модулям (Predict, ChainOfThought, ReAct, ProgramOfThought)
  * `references/optimizers.md` — Алгоритмы оптимизации (BootstrapFewShot, MIPRO, BootstrapFinetune)
  * `references/examples.md` — Примеры из реального мира (RAG, агенты, классификаторы)


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Установка](<#installation>)
  * [Быстрый старт](<#quick-start>)
    * [Базовый пример: Ответы на вопросы](<#basic-example-question-answering>)
    * [Цепочка рассуждений (Chain of Thought)](<#chain-of-thought-reasoning>)
  * [Основные концепции](<#core-concepts>)
    * [1\\. Сигнатуры](<#1-signatures>)
    * [2\\. Модули](<#2-modules>)
    * [3\\. Оптимизаторы](<#3-optimizers>)
    * [4\\. Построение сложных систем](<#4-building-complex-systems>)
  * [Конфигурация LM-провайдеров](<#lm-provider-configuration>)
    * [Anthropic Claude](<#anthropic-claude>)
    * [OpenAI](<#openai>)
    * [Локальные модели (Ollama)](<#local-models-ollama>)
    * [Несколько моделей](<#multiple-models>)
  * [Типовые паттерны](<#common-patterns>)
    * [Паттерн 1: Структурированный вывод](<#pattern-1-structured-output>)
    * [Паттерн 2: Оптимизация на основе утверждений](<#pattern-2-assertion-driven-optimization>)
    * [Паттерн 3: Самосогласованность](<#pattern-3-self-consistency>)
    * [Паттерн 4: Поиск с переранжированием](<#pattern-4-retrieval-with-reranking>)
  * [Оценка и метрики](<#evaluation-and-metrics>)
    * [Пользовательские метрики](<#custom-metrics>)
    * [Оценка](<#evaluation>)
  * [Лучшие практики](<#best-practices>)
    * [1\\. Начинайте с простого, итерируйте](<#1-start-simple-iterate>)
    * [2\\. Используйте описательные сигнатуры](<#2-use-descriptive-signatures>)
    * [3\\. Оптимизируйте на репрезентативных данных](<#3-optimize-with-representative-data>)
    * [4\\. Сохраняйте и загружайте оптимизированные модели](<#4-save-and-load-optimized-models>)
    * [5\\. Мониторинг и отладка](<#5-monitor-and-debug>)
  * [Сравнение с другими подходами](<#comparison-to-other-approaches>)
  * [Ресурсы](<#resources>)
  * [См. также](<#see-also>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-research-dspy -->
