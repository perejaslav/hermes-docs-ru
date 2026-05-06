On this page
Outlines: структурированная генерация LLM в форматах JSON/регулярных выражений/Pydantic.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Встроенный (установлен по умолчанию)  |
|Путь| `skills/mlops/inference/outlines`  |
|Версия| `1.0.0`  |
|Автор| Orchestra Research  |
|Лицензия| MIT  |
|Зависимости| `outlines`, `transformers`, `vllm`, `pydantic`  |
|Теги| `Prompt Engineering`, `Outlines`, `Structured Generation`, `JSON Schema`, `Pydantic`, `Local Models`, `Grammar-Based Generation`, `vLLM`, `Transformers`, `Type Safety`  |
|## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# Outlines: Структурированная генерация текста
## Когда использовать этот навык[​](<#when-to-use-this-skill> "Прямая ссылка на Когда использовать этот навык")
Используйте Outlines, когда вам нужно:
  * **Гарантировать корректную структуру JSON/XML/кода** во время генерации
  * **Использовать Pydantic-модели** для типобезопасного вывода
  * **Поддерживать локальные модели** (Transformers, llama.cpp, vLLM)
  * **Максимизировать скорость инференса** с нулевыми накладными расходами на структурированную генерацию
  * **Генерировать по JSON-схемам** автоматически
  * **Контролировать сэмплирование токенов** на уровне грамматики


**Звёзд на GitHub** : 8 000+ | **От** : dottxt.ai (ранее .txt)
## Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Базовая установка  
    pip install outlines  
      
    # С конкретными бэкендами  
    pip install outlines transformers  # Модели Hugging Face  
    pip install outlines llama-cpp-python  # llama.cpp  
    pip install outlines vllm  # vLLM для высокой пропускной способности  
    
[/code]
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Базовый пример: Классификация[​](<#basic-example-classification> "Прямая ссылка на Базовый пример: Классификация")
[code] 
    import outlines  
    from typing import Literal  
      
    # Загрузка модели  
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
      
    # Генерация с ограничением по типу  
    prompt = "Sentiment of 'This product is amazing!': "  
    generator = outlines.generate.choice(model, ["positive", "negative", "neutral"])  
    sentiment = generator(prompt)  
      
    print(sentiment)  # "positive" (гарантированно одно из значений)  
    
[/code]
### С Pydantic-моделями[​](<#with-pydantic-models> "Прямая ссылка на С Pydantic-моделями")
[code] 
    from pydantic import BaseModel  
    import outlines  
      
    class User(BaseModel):  
        name: str  
        age: int  
        email: str  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
      
    # Генерация структурированного вывода  
    prompt = "Extract user: John Doe, 30 years old, john@example.com"  
    generator = outlines.generate.json(model, User)  
    user = generator(prompt)  
      
    print(user.name)   # "John Doe"  
    print(user.age)    # 30  
    print(user.email)  # "john@example.com"  
    
[/code]
## Основные концепции[​](<#core-concepts> "Прямая ссылка на Основные концепции")
### 1\\. Ограниченное сэмплирование токенов[​](<#1-constrained-token-sampling> "Прямая ссылка на 1. Ограниченное сэмплирование токенов")
Outlines использует конечные автоматы (FSM) для ограничения генерации токенов на уровне логитов.
**Как это работает:**
  1. Преобразование схемы (JSON/Pydantic/regex) в контекстно-свободную грамматику (CFG)
  2. Преобразование CFG в конечный автомат (FSM)
  3. Фильтрация недопустимых токенов на каждом шаге генерации
  4. Быстрый пропуск (fast-forward), когда существует только один допустимый токен


**Преимущества:**
  * **Нулевые накладные расходы** : Фильтрация происходит на уровне токенов
  * **Ускорение** : Быстрый пропуск детерминированных путей
  * **Гарантированная корректность** : Некорректные выходные данные невозможны


[code] 
    import outlines  
      
    # Pydantic-модель -> JSON-схема -> CFG -> FSM  
    class Person(BaseModel):  
        name: str  
        age: int  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
      
    # Что происходит внутри:  
    # 1. Person -> JSON-схема  
    # 2. JSON-схема -> CFG  
    # 3. CFG -> FSM  
    # 4. FSM фильтрует токены во время генерации  
      
    generator = outlines.generate.json(model, Person)  
    result = generator("Generate person: Alice, 25")  
    
[/code]
### 2\\. Структурированные генераторы[​](<#2-structured-generators> "Прямая ссылка на 2. Структурированные генераторы")
Outlines предоставляет специализированные генераторы для различных типов вывода.
#### Генератор выбора (Choice)[​](<#choice-generator> "Прямая ссылка на Генератор выбора \\(Choice\\)")
[code] 
    # Выбор из нескольких вариантов  
    generator = outlines.generate.choice(  
        model,  
        ["positive", "negative", "neutral"]  
    )  
      
    sentiment = generator("Review: This is great!")  
    # Результат: Один из трёх вариантов  
    
[/code]
#### JSON-генератор[​](<#json-generator> "Прямая ссылка на JSON-генератор")
[code] 
    from pydantic import BaseModel  
      
    class Product(BaseModel):  
        name: str  
        price: float  
        in_stock: bool  
      
    # Генерация корректного JSON по схеме  
    generator = outlines.generate.json(model, Product)  
    product = generator("Extract: iPhone 15, $999, available")  
      
    # Гарантированно корректный экземпляр Product  
    print(type(product))  # <class '__main__.Product'>  
    
[/code]
#### Генератор регулярных выражений[​](<#regex-generator> "Прямая ссылка на Генератор регулярных выражений")
[code] 
    # Генерация текста по регулярному выражению  
    generator = outlines.generate.regex(  
        model,  
        r"[0-9]{3}-[0-9]{3}-[0-9]{4}"  # Шаблон номера телефона  
    )  
      
    phone = generator("Generate phone number:")  
    # Результат: "555-123-4567" (гарантированно соответствует шаблону)  
    
[/code]
#### Генераторы целых чисел и чисел с плавающей точкой[​](<#integerfloat-generators> "Прямая ссылка на Генераторы целых чисел и чисел с плавающей точкой")
[code] 
    # Генерация определённых числовых типов  
    int_generator = outlines.generate.integer(model)  
    age = int_generator("Person's age:")  # Гарантированно целое число  
      
    float_generator = outlines.generate.float(model)  
    price = float_generator("Product price:")  # Гарантированно число с плавающей точкой  
    
[/code]
### 3\\. Модельные бэкенды[​](<#3-model-backends> "Прямая ссылка на 3. Модельные бэкенды")
Outlines поддерживает несколько локальных и API-бэкендов.
#### Transformers (Hugging Face)[​](<#transformers-hugging-face> "Прямая ссылка на Transformers \\(Hugging Face\\)")
[code] 
    import outlines  
      
    # Загрузка из Hugging Face  
    model = outlines.models.transformers(  
        "microsoft/Phi-3-mini-4k-instruct",  
        device="cuda"  # Или "cpu"  
    )  
      
    # Использование с любым генератором  
    generator = outlines.generate.json(model, YourModel)  
    
[/code]
#### llama.cpp[​](<#llamacpp> "Прямая ссылка на llama.cpp")
[code] 
    # Загрузка GGUF-модели  
    model = outlines.models.llamacpp(  
        "./models/llama-3.1-8b-instruct.Q4_K_M.gguf",  
        n_gpu_layers=35  
    )  
      
    generator = outlines.generate.json(model, YourModel)  
    
[/code]
#### vLLM (Высокая пропускная способность)[​](<#vllm-high-throughput> "Прямая ссылка на vLLM \\(Высокая пропускная способность\\)")
[code] 
    # Для production-развёртываний  
    model = outlines.models.vllm(  
        "meta-llama/Llama-3.1-8B-Instruct",  
        tensor_parallel_size=2  # Несколько GPU  
    )  
      
    generator = outlines.generate.json(model, YourModel)  
    
[/code]
#### OpenAI (Ограниченная поддержка)[​](<#openai-limited-support> "Прямая ссылка на OpenAI \\(Ограниченная поддержка\\)")
[code] 
    # Базовая поддержка OpenAI  
    model = outlines.models.openai(  
        "gpt-4o-mini",  
        api_key="your-api-key"  
    )  
      
    # Примечание: некоторые функции ограничены для API-моделей  
    generator = outlines.generate.json(model, YourModel)  
    
[/code]
### 4\\. Интеграция с Pydantic[​](<#4-pydantic-integration> "Прямая ссылка на 4. Интеграция с Pydantic")
Outlines имеет первоклассную поддержку Pydantic с автоматическим преобразованием схем.
#### Базовые модели[​](<#basic-models> "Прямая ссылка на Базовые модели")
[code] 
    from pydantic import BaseModel, Field  
      
    class Article(BaseModel):  
        title: str = Field(description="Название статьи")  
        author: str = Field(description="Имя автора")  
        word_count: int = Field(description="Количество слов", gt=0)  
        tags: list[str] = Field(description="Список тегов")  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
    generator = outlines.generate.json(model, Article)  
      
    article = generator("Generate article about AI")  
    print(article.title)  
    print(article.word_count)  # Гарантированно > 0  
    
[/code]
#### Вложенные модели[​](<#nested-models> "Прямая ссылка на Вложенные модели")
[code] 
    class Address(BaseModel):  
        street: str  
        city: str  
        country: str  
      
    class Person(BaseModel):  
        name: str  
        age: int  
        address: Address  # Вложенная модель  
      
    generator = outlines.generate.json(model, Person)  
    person = generator("Generate person in New York")  
      
    print(person.address.city)  # "New York"  
    
[/code]
#### Перечисления и литералы[​](<#enums-and-literals> "Прямая ссылка на Перечисления и литералы")
[code] 
    from enum import Enum  
    from typing import Literal  
      
    class Status(str, Enum):  
        PENDING = "pending"  
        APPROVED = "approved"  
        REJECTED = "rejected"  
      
    class Application(BaseModel):  
        applicant: str  
        status: Status  # Должно быть одним из значений перечисления  
        priority: Literal["low", "medium", "high"]  # Должно быть одним из литералов  
      
    generator = outlines.generate.json(model, Application)  
    app = generator("Generate application")  
      
    print(app.status)  # Status.PENDING (или APPROVED/REJECTED)  
    
[/code]
## Типовые шаблоны[​](<#common-patterns> "Прямая ссылка на Типовые шаблоны")
### Шаблон 1: Извлечение данных[​](<#pattern-1-data-extraction> "Прямая ссылка на Шаблон 1: Извлечение данных")
[code] 
    from pydantic import BaseModel  
    import outlines  
      
    class CompanyInfo(BaseModel):  
        name: str  
        founded_year: int  
        industry: str  
        employees: int  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
    generator = outlines.generate.json(model, CompanyInfo)  
      
    text = """  
    Apple Inc. was founded in 1976 in the technology industry.  
    The company employs approximately 164,000 people worldwide.  
    """  
      
    prompt = f"Extract company information:\n{text}\n\nCompany:"  
    company = generator(prompt)  
      
    print(f"Name: {company.name}")  
    print(f"Founded: {company.founded_year}")  
    print(f"Industry: {company.industry}")  
    print(f"Employees: {company.employees}")  
    
[/code]
### Шаблон 2: Классификация[​](<#pattern-2-classification> "Прямая ссылка на Шаблон 2: Классификация")
[code] 
    from typing import Literal  
    import outlines  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
      
    # Бинарная классификация  
    generator = outlines.generate.choice(model, ["spam", "not_spam"])  
    result = generator("Email: Buy now! 50% off!")  
      
    # Многоклассовая классификация  
    categories = ["technology", "business", "sports", "entertainment"]  
    category_gen = outlines.generate.choice(model, categories)  
    category = category_gen("Article: Apple announces new iPhone...")  
      
    # С уверенностью  
    class Classification(BaseModel):  
        label: Literal["positive", "negative", "neutral"]  
        confidence: float  
      
    classifier = outlines.generate.json(model, Classification)  
    result = classifier("Review: This product is okay, nothing special")  
    
[/code]
### Шаблон 3: Структурированные формы[​](<#pattern-3-structured-forms> "Прямая ссылка на Шаблон 3: Структурированные формы")
[code] 
    class UserProfile(BaseModel):  
        full_name: str  
        age: int  
        email: str  
        phone: str  
        country: str  
        interests: list[str]  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
    generator = outlines.generate.json(model, UserProfile)  
      
    prompt = """  
    Extract user profile from:  
    Name: Alice Johnson  
    Age: 28  
    Email: alice@example.com  
    Phone: 555-0123  
    Country: USA  
    Interests: hiking, photography, cooking  
    """  
      
    profile = generator(prompt)  
    print(profile.full_name)  
    print(profile.interests)  # ["hiking", "photography", "cooking"]  
    
[/code]
### Шаблон 4: Извлечение нескольких сущностей[​](<#pattern-4-multi-entity-extraction> "Прямая ссылка на Шаблон 4: Извлечение нескольких сущностей")
[code] 
    class Entity(BaseModel):  
        name: str  
        type: Literal["PERSON", "ORGANIZATION", "LOCATION"]  
      
    class DocumentEntities(BaseModel):  
        entities: list[Entity]  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
    generator = outlines.generate.json(model, DocumentEntities)  
      
    text = "Tim Cook met with Satya Nadella at Microsoft headquarters in Redmond."  
    prompt = f"Extract entities from: {text}"  
      
    result = generator(prompt)  
    for entity in result.entities:  
        print(f"{entity.name} ({entity.type})")  
    
[/code]
### Шаблон 5: Генерация кода[​](<#pattern-5-code-generation> "Прямая ссылка на Шаблон 5: Генерация кода")
[code] 
    class PythonFunction(BaseModel):  
        function_name: str  
        parameters: list[str]  
        docstring: str  
        body: str  
      
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
    generator = outlines.generate.json(model, PythonFunction)  
      
    prompt = "Generate a Python function to calculate factorial"  
    func = generator(prompt)  
      
    print(f"def {func.function_name}({', '.join(func.parameters)}):")  
    print(f'    """{func.docstring}"""')  
    print(f"    {func.body}")  
    
[/code]
### Шаблон 6: Пакетная обработка[​](<#pattern-6-batch-processing> "Прямая ссылка на Шаблон 6: Пакетная обработка")
[code] 
    def batch_extract(texts: list[str], schema: type[BaseModel]):  
        """Извлечение структурированных данных из нескольких текстов."""  
        model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
        generator = outlines.generate.json(model, schema)  
      
        results = []  
        for text in texts:  
            result = generator(f"Extract from: {text}")  
            results.append(result)  
      
        return results  
      
    class Person(BaseModel):  
        name: str  
        age: int  
      
    texts = [  
        "John is 30 years old",  
        "Alice is 25 years old",  
        "Bob is 40 years old"  
    ]  
      
    people = batch_extract(texts, Person)  
    for person in people:  
        print(f"{person.name}: {person.age}")  
    
[/code]
## Настройка бэкендов[​](<#backend-configuration> "Прямая ссылка на Настройка бэкендов")
### Transformers[​](<#transformers> "Прямая ссылка на Transformers")
[code] 
    import outlines  
      
    # Базовое использование  
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")  
      
    # Настройка GPU  
    model = outlines.models.transformers(  
        "microsoft/Phi-3-mini-4k-instruct",  
        device="cuda",  
        model_kwargs={"torch_dtype": "float16"}  
    )  
      
    # Популярные модели  
    model = outlines.models.transformers("meta-llama/Llama-3.1-8B-Instruct")  
    model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.3")  
    model = outlines.models.transformers("Qwen/Qwen2.5-7B-Instruct")  
    
[/code]
### llama.cpp[​](<#llamacpp-1> "Прямая ссылка на llama.cpp")
[code] 
    # Загрузка GGUF-модели  
    model = outlines.models.llamacpp(  
        "./models/llama-3.1-8b.Q4_K_M.gguf",  
        n_ctx=4096,         # Окно контекста  
        n_gpu_layers=35,    # Слои GPU  
        n_threads=8         # Потоки CPU  
    )  
      
    # Полная выгрузка на GPU  
    model = outlines.models.llamacpp(  
        "./models/model.gguf",  
        n_gpu_layers=-1  # Все слои на GPU  
    )  
    
[/code]
### vLLM (Production)[​](<#vllm-production> "Прямая ссылка на vLLM \\(Production\\)")
[code] 
    # Один GPU  
    model = outlines.models.vllm("meta-llama/Llama-3.1-8B-Instruct")  
      
    # Несколько GPU  
    model = outlines.models.vllm(  
        "meta-llama/Llama-3.1-70B-Instruct",  
        tensor_parallel_size=4  # 4 GPU  
    )  
      
    # С квантизацией  
    model = outlines.models.vllm(  
        "meta-llama/Llama-3.1-8B-Instruct",  
        quantization="awq"  # Или "gptq"  
    )  
    
[/code]
## Лучшие практики[​](<#best-practices> "Прямая ссылка на Лучшие практики")
### 1\\. Используйте конкретные типы[​](<#1-use-specific-types> "Прямая ссылка на 1. Используйте конкретные типы")
[code] 
    # ✅ Хорошо: конкретные типы  
    class Product(BaseModel):  
        name: str  
        price: float  # Не str  
        quantity: int  # Не str  
        in_stock: bool  # Не str  
      
    # ❌ Плохо: всё как строка  
    class Product(BaseModel):  
        name: str  
        price: str  # Должно быть float  
        quantity: str  # Должно быть int  
    
[/code]
### 2\\. Добавляйте ограничения[​](<#2-add-constraints> "Прямая ссылка на 2. Добавляйте ограничения")
[code] 
    from pydantic import Field  
      
    # ✅ Хорошо: с ограничениями  
    class User(BaseModel):  
        name: str = Field(min_length=1, max_length=100)  
        age: int = Field(ge=0, le=120)  
        email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")  
      
    # ❌ Плохо: без ограничений  
    class User(BaseModel):  
        name: str  
        age: int  
        email: str  
    
[/code]
### 3\\. Используйте перечисления для категорий[​](<#3-use-enums-for-categories> "Прямая ссылка на 3. Используйте перечисления для категорий")
[code] 
    # ✅ Хорошо: перечисление для фиксированного набора  
    class Priority(str, Enum):  
        LOW = "low"  
        MEDIUM = "medium"  
        HIGH = "high"  
      
    class Task(BaseModel):  
        title: str  
        priority: Priority  
      
    # ❌ Плохо: свободная строка  
    class Task(BaseModel):  
        title: str  
        priority: str  # Может быть чем угодно  
    
[/code]
### 4\\. Предоставляйте контекст в промптах[​](<#4-provide-context-in-prompts> "Прямая ссылка на 4. Предоставляйте контекст в промптах")
[code] 
    # ✅ Хорошо: чёткий контекст  
    prompt = """  
    Extract product information from the following text.  
    Text: iPhone 15 Pro costs $999 and is currently in stock.  
    Product:  
    """  
      
    # ❌ Плохо: минимальный контекст  
    prompt = "iPhone 15 Pro costs $999 and is currently in stock."  
    
[/code]
### 5\\. Обрабатывайте необязательные поля[​](<#5-handle-optional-fields> "Прямая ссылка на 5. Обрабатывайте необязательные поля")
[code] 
    from typing import Optional  
      
    # ✅ Хорошо: необязательные поля для неполных данных  
    class Article(BaseModel):  
        title: str  # Обязательное  
        author: Optional[str] = None  # Необязательное  
        date: Optional[str] = None  # Необязательное  
        tags: list[str] = []  # Пустой список по умолчанию  
      
    # Может быть успешно обработано, даже если автор/дата отсутствуют  
    
[/code]
## Сравнение с альтернативами[​](<#comparison-to-alternatives> "Прямая ссылка на Сравнение с альтернативами")
Возможность| Outlines| Instructor| Guidance| LMQL  
|---|---|---|---|---  
Поддержка Pydantic| ✅ Встроенная| ✅ Встроенная| ❌ Нет| ❌ Нет  
JSON Schema| ✅ Да| ✅ Да| ⚠️ Ограниченно| ✅ Да  
Ограничения через regex| ✅ Да| ❌ Нет| ✅ Да| ✅ Да  
Локальные модели| ✅ Полная| ⚠️ Ограниченно| ✅ Полная| ✅ Полная  
API-модели| ⚠️ Ограниченно| ✅ Полная| ✅ Полная| ✅ Полная  
Нулевые накладные расходы| ✅ Да| ❌ Нет| ⚠️ Частично| ✅ Да  
Автоматические повторные попытки| ❌ Нет| ✅ Да| ❌ Нет| ❌ Нет  
Порог входа| Низкий| Низкий| Низкий| Высокий  
**Когда выбирать Outlines:**
  * Используются локальные модели (Transformers, llama.cpp, vLLM)
  * Нужна максимальная скорость инференса
  * Требуется поддержка Pydantic-моделей
  * Необходима структурированная генерация с нулевыми накладными расходами
  * Требуется контроль процесса сэмплирования токенов


**Когда выбирать альтернативы:**
  * Instructor: нужны API-модели с автоматическими повторными попытками
  * Guidance: нужны токен-хилинг и сложные рабочие процессы
  * LMQL: предпочтительнее декларативный синтаксис запросов


## Характеристики производительности[​](<#performance-characteristics> "Прямая ссылка на Характеристики производительности")
**Скорость:**
  * **Нулевые накладные расходы** : Структурированная генерация так же быстра, как и без ограничений
  * **Оптимизация fast-forward** : Пропускает детерминированные токены
  * **В 1.2-2 раза быстрее** подходов с пост-генерационной валидацией


**Память:**
  * FSM компилируется один раз на схему (кэшируется)
  * Минимальные накладные расходы во время выполнения
  * Эффективен с vLLM для высокой пропускной способности


**Точность:**
  * **100% корректных выходных данных** (гарантируется FSM)
  * Не требуется циклов повторных попыток
  * Детерминированная фильтрация токенов


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **Документация** : <https://outlines-dev.github.io/outlines>
  * **GitHub** : <https://github.com/outlines-dev/outlines> (8k+ звёзд)
  * **Discord** : <https://discord.gg/R9DSu34mGd>
  * **Блог** : <https://blog.dottxt.co>


## См. также[​](<#see-also> "Прямая ссылка на См. также")
  * `references/json_generation.md` \\- Подробные шаблоны JSON и Pydantic
  * `references/backends.md` \\- Конфигурация под конкретные бэкенды
  * `references/examples.md` \\- Примеры для production


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Установка](<#installation>)
  * [Быстрый старт](<#quick-start>)
    * [Базовый пример: Классификация](<#basic-example-classification>)
    * [С Pydantic-моделями](<#with-pydantic-models>)
  * [Основные концепции](<#core-concepts>)
    * [1\\. Ограниченное сэмплирование токенов](<#1-constrained-token-sampling>)
    * [2\\. Структурированные генераторы](<#2-structured-generators>)
    * [3\\. Модельные бэкенды](<#3-model-backends>)
    * [4\\. Интеграция с Pydantic](<#4-pydantic-integration>)
  * [Типовые шаблоны](<#common-patterns>)
    * [Шаблон 1: Извлечение данных](<#pattern-1-data-extraction>)
    * [Шаблон 2: Классификация](<#pattern-2-classification>)
    * [Шаблон 3: Структурированные формы](<#pattern-3-structured-forms>)
    * [Шаблон 4: Извлечение нескольких сущностей](<#pattern-4-multi-entity-extraction>)
    * [Шаблон 5: Генерация кода](<#pattern-5-code-generation>)
    * [Шаблон 6: Пакетная обработка](<#pattern-6-batch-processing>)
  * [Настройка бэкендов](<#backend-configuration>)
    * [Transformers](<#transformers>)
    * [llama.cpp](<#llamacpp-1>)
    * [vLLM (Production)](<#vllm-production>)
  * [Лучшие практики](<#best-practices>)
    * [1\\. Используйте конкретные типы](<#1-use-specific-types>)
    * [2\\. Добавляйте ограничения](<#2-add-constraints>)
    * [3\\. Используйте перечисления для категорий](<#3-use-enums-for-categories>)
    * [4\\. Предоставляйте контекст в промптах](<#4-provide-context-in-prompts>)
    * [5\\. Обрабатывайте необязательные поля](<#5-handle-optional-fields>)
  * [Сравнение с альтернативами](<#comparison-to-alternatives>)
  * [Характеристики производительности](<#performance-characteristics>)
  * [Ресурсы](<#resources>)
  * [См. также](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-inference-outlines -->
