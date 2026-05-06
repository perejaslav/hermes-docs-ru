На этой странице

Управляйте выводом LLM с помощью регулярных выражений и грамматик, гарантируйте генерацию валидного JSON/XML/кода, обеспечивайте соблюдение структурированных форматов и создавайте многошаговые рабочие процессы с Guidance — фреймворком ограниченной генерации от Microsoft Research

## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")

|
|---|---
Источник| Опционально — установка с помощью `hermes skills install official/mlops/guidance`
Путь| `optional-skills/mlops/guidance`
Версия| `1.0.0`
Автор| Orchestra Research
Лицензия| MIT
Зависимости| `guidance`, `transformers`
Теги| `Prompt Engineering`, `Guidance`, `Constrained Generation`, `Structured Output`, `JSON Validation`, `Grammar`, `Microsoft Research`, `Format Enforcement`, `Multi-Step Workflows`

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info

Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# Guidance: Ограниченная генерация LLM

## Когда использовать этот навык[​](<#when-to-use-this-skill> "Direct link to When to Use This Skill")

Используйте Guidance, когда вам нужно:

  * **Контролировать синтаксис вывода LLM** с помощью регулярных выражений или грамматик
  * **Гарантировать генерацию валидного JSON/XML/кода**
  * **Снизить задержку** по сравнению с традиционными подходами с промптами
  * **Обеспечить соблюдение структурированных форматов** (даты, email, ID и т.д.)
  * **Создавать многошаговые рабочие процессы** с Python-подобным управлением потоком
  * **Предотвращать невалидный вывод** с помощью грамматических ограничений

**GitHub Stars:** 18 000+ | **От:** Microsoft Research

## Установка[​](<#installation> "Direct link to Installation")

[code]
    # Базовая установка
    pip install guidance
      
    # С конкретными бэкендами
    pip install guidance[transformers]  # Модели Hugging Face
    pip install guidance[llama_cpp]     # Модели llama.cpp
    
[/code]

## Быстрый старт[​](<#quick-start> "Direct link to Quick Start")

### Базовый пример: Структурированная генерация[​](<#basic-example-structured-generation> "Direct link to Basic Example: Structured Generation")

[code]
    from guidance import models, gen
      
    # Загрузка модели (поддерживает OpenAI, Transformers, llama.cpp)
    lm = models.OpenAI("gpt-4")
      
    # Генерация с ограничениями
    result = lm + "The capital of France is " + gen("capital", max_tokens=5)
      
    print(result["capital"])  # "Paris"
    
[/code]

### С Anthropic Claude[​](<#with-anthropic-claude> "Direct link to With Anthropic Claude")

[code]
    from guidance import models, gen, system, user, assistant
      
    # Настройка Claude
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
      
    # Использование контекстных менеджеров для чат-формата
    with system():
        lm += "You are a helpful assistant."
      
    with user():
        lm += "What is the capital of France?"
      
    with assistant():
        lm += gen(max_tokens=20)
    
[/code]

## Основные концепции[​](<#core-concepts> "Direct link to Core Concepts")

### 1. Контекстные менеджеры[​](<#1-context-managers> "Direct link to 1. Context Managers")

Guidance использует Python-подобные контекстные менеджеры для чат-взаимодействий.

[code]
    from guidance import system, user, assistant, gen
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
      
    # Системное сообщение
    with system():
        lm += "You are a JSON generation expert."
      
    # Сообщение пользователя
    with user():
        lm += "Generate a person object with name and age."
      
    # Ответ ассистента
    with assistant():
        lm += gen("response", max_tokens=100)
      
    print(lm["response"])
    
[/code]

**Преимущества:**

  * Естественный чат-поток
  * Чёткое разделение ролей
  * Легко читать и поддерживать

### 2. Ограниченная генерация[​](<#2-constrained-generation> "Direct link to 2. Constrained Generation")

Guidance гарантирует, что вывод соответствует заданным шаблонам с помощью регулярных выражений или грамматик.

#### Ограничения с помощью Regex[​](<#regex-constraints> "Direct link to Regex Constraints")

[code]
    from guidance import models, gen
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
      
    # Ограничение до валидного формата email
    lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
      
    # Ограничение до формата даты (YYYY-MM-DD)
    lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}")
      
    # Ограничение до номера телефона
    lm += "Phone: " + gen("phone", regex=r"\d{3}-\d{3}-\d{4}")
      
    print(lm["email"])  # Гарантированно валидный email
    print(lm["date"])   # Гарантированно формат YYYY-MM-DD
    
[/code]

**Как это работает:**

  * Regex преобразуется в грамматику на уровне токенов
  * Невалидные токены отфильтровываются во время генерации
  * Модель может производить только соответствующие результаты

#### Ограничения с помощью выбора[​](<#selection-constraints> "Direct link to Selection Constraints")

[code]
    from guidance import models, gen, select
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
      
    # Ограничение до конкретных вариантов
    lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")
      
    # Множественный выбор
    lm += "Best answer: " + select(
        ["A) Paris", "B) London", "C) Berlin", "D) Madrid"],
        name="answer"
    )
      
    print(lm["sentiment"])  # Один из: positive, negative, neutral
    print(lm["answer"])     # Один из: A, B, C или D
    
[/code]

### 3. Токен-хилинг (Token Healing)[​](<#3-token-healing> "Direct link to 3. Token Healing")

Guidance автоматически "исцеляет" границы токенов между промптом и генерацией.

**Проблема:** Токенизация создаёт неестественные границы.

[code]
    # Без токен-хилинга
    prompt = "The capital of France is "
    # Последний токен: " is "
    # Первый сгенерированный токен может быть " Par" (с ведущим пробелом)
    # Результат: "The capital of France is  Paris" (двойной пробел!)
    
[/code]

**Решение:** Guidance отступает на один токен и регенерирует.

[code]
    from guidance import models, gen
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
      
    # Токен-хилинг включён по умолчанию
    lm += "The capital of France is " + gen("capital", max_tokens=5)
    # Результат: "The capital of France is Paris" (правильные пробелы)
    
[/code]

**Преимущества:**

  * Естественные текстовые границы
  * Нет проблем с неудобными пробелами
  * Лучшая производительность модели (видит естественные последовательности токенов)

### 4. Генерация на основе грамматик[​](<#4-grammar-based-generation> "Direct link to 4. Grammar-Based Generation")

Определяйте сложные структуры с помощью контекстно-свободных грамматик.

[code]
    from guidance import models, gen
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
      
    # JSON грамматика (упрощённая)
    json_grammar = """
    {
        "name": <gen name regex="[A-Za-z ]+" max_tokens=20>,
        "age": <gen age regex="[0-9]+" max_tokens=3>,
        "email": <gen email regex="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" max_tokens=50>
    }
    """
      
    # Генерация валидного JSON
    lm += gen("person", grammar=json_grammar)
      
    print(lm["person"])  # Гарантированно валидная JSON-структура
    
[/code]

**Варианты использования:**

  * Сложные структурированные выводы
  * Вложенные структуры данных
  * Синтаксис языков программирования
  * Предметно-ориентированные языки

### 5. Функции Guidance[​](<#5-guidance-functions> "Direct link to 5. Guidance Functions")

Создавайте переиспользуемые шаблоны генерации с помощью декоратора `@guidance`.

[code]
    from guidance import guidance, gen, models
      
    @guidance
    def generate_person(lm):
        """Сгенерировать человека с именем и возрастом."""
        lm += "Name: " + gen("name", max_tokens=20, stop="\n")
        lm += "\nAge: " + gen("age", regex=r"[0-9]+", max_tokens=3)
        return lm
      
    # Использование функции
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
    lm = generate_person(lm)
      
    print(lm["name"])
    print(lm["age"])
    
[/code]

**Функции с состоянием:**

[code]
    @guidance(stateless=False)
    def react_agent(lm, question, tools, max_rounds=5):
        """ReAct агент с использованием инструментов."""
        lm += f"Question: {question}\n\n"
      
        for i in range(max_rounds):
            # Мысль
            lm += f"Thought {i+1}: " + gen("thought", stop="\n")
      
            # Действие
            lm += "\nAction: " + select(list(tools.keys()), name="action")
      
            # Выполнение инструмента
            tool_result = tools[lm["action"]]()
            lm += f"\nObservation: {tool_result}\n\n"
      
            # Проверка завершения
            lm += "Done? " + select(["Yes", "No"], name="done")
            if lm["done"] == "Yes":
                break
      
        # Финальный ответ
        lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
        return lm
    
[/code]

## Конфигурация бэкенда[​](<#backend-configuration> "Direct link to Backend Configuration")

### Anthropic Claude[​](<#anthropic-claude> "Direct link to Anthropic Claude")

[code]
    from guidance import models
      
    lm = models.Anthropic(
        model="claude-sonnet-4-5-20250929",
        api_key="your-api-key"  # Или установите переменную окружения ANTHROPIC_API_KEY
    )
    
[/code]

### OpenAI[​](<#openai> "Direct link to OpenAI")

[code]
    lm = models.OpenAI(
        model="gpt-4o-mini",
        api_key="your-api-key"  # Или установите переменную окружения OPENAI_API_KEY
    )
    
[/code]

### Локальные модели (Transformers)[​](<#local-models-transformers> "Direct link to Local Models (Transformers)")

[code]
    from guidance.models import Transformers
      
    lm = Transformers(
        "microsoft/Phi-4-mini-instruct",
        device="cuda"  # Или "cpu"
    )
    
[/code]

### Локальные модели (llama.cpp)[​](<#local-models-llamacpp> "Direct link to Local Models (llama.cpp)")

[code]
    from guidance.models import LlamaCpp
      
    lm = LlamaCpp(
        model_path="/path/to/model.gguf",
        n_ctx=4096,
        n_gpu_layers=35
    )
    
[/code]

## Типовые шаблоны[​](<#common-patterns> "Direct link to Common Patterns")

### Шаблон 1: Генерация JSON[​](<#pattern-1-json-generation> "Direct link to Pattern 1: JSON Generation")

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
      
    print(lm)  # Гарантированно валидный JSON
    
[/code]

### Шаблон 2: Классификация[​](<#pattern-2-classification> "Direct link to Pattern 2: Classification")

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

### Шаблон 3: Многошаговые рассуждения[​](<#pattern-3-multi-step-reasoning> "Direct link to Pattern 3: Multi-Step Reasoning")

[code]
    from guidance import models, gen, guidance
      
    @guidance
    def chain_of_thought(lm, question):
        """Сгенерировать ответ с пошаговыми рассуждениями."""
        lm += f"Question: {question}\n\n"
      
        # Генерация нескольких шагов рассуждений
        for i in range(3):
            lm += f"Step {i+1}: " + gen(f"step_{i+1}", stop="\n", max_tokens=100) + "\n"
      
        # Финальный ответ
        lm += "\nTherefore, the answer is: " + gen("answer", max_tokens=50)
      
        return lm
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
    lm = chain_of_thought(lm, "What is 15% of 200?")
      
    print(lm["answer"])
    
[/code]

### Шаблон 4: ReAct Агент[​](<#pattern-4-react-agent> "Direct link to Pattern 4: ReAct Agent")

[code]
    from guidance import models, gen, select, guidance
      
    @guidance(stateless=False)
    def react_agent(lm, question):
        """ReAct агент с использованием инструментов."""
        tools = {
            "calculator": lambda expr: eval(expr),
            "search": lambda query: f"Search results for: {query}",
        }
      
        lm += f"Question: {question}\n\n"
      
        for round in range(5):
            # Мысль
            lm += f"Thought: " + gen("thought", stop="\n") + "\n"
      
            # Выбор действия
            lm += "Action: " + select(["calculator", "search", "answer"], name="action")
      
            if lm["action"] == "answer":
                lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
                break
      
            # Ввод действия
            lm += "\nAction Input: " + gen("action_input", stop="\n") + "\n"
      
            # Выполнение инструмента
            if lm["action"] in tools:
                result = tools[lm["action"]](lm["action_input"])
                lm += f"Observation: {result}\n\n"
      
        return lm
      
    lm = models.Anthropic("claude-sonnet-4-5-20250929")
    lm = react_agent(lm, "What is 25 * 4 + 10?")
    print(lm["answer"])
    
[/code]

### Шаблон 5: Извлечение данных[​](<#pattern-5-data-extraction> "Direct link to Pattern 5: Data Extraction")

[code]
    from guidance import models, gen, guidance
      
    @guidance
    def extract_entities(lm, text):
        """Извлечь структурированные сущности из текста."""
        lm += f"Text: {text}\n\n"
      
        # Извлечение человека
        lm += "Person: " + gen("person", stop="\n", max_tokens=30) + "\n"
      
        # Извлечение организации
        lm += "Organization: " + gen("organization", stop="\n", max_tokens=30) + "\n"
      
        # Извлечение даты
        lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}", max_tokens=10) + "\n"
      
        # Извлечение места
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

## Лучшие практики[​](<#best-practices> "Direct link to Best Practices")

### 1. Используйте Regex для проверки формата[​](<#1-use-regex-for-format-validation> "Direct link to 1. Use Regex for Format Validation")

[code]
    # ✅ Хорошо: Regex обеспечивает валидный формат
    lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
      
    # ❌ Плохо: Свободная генерация может дать невалидные email
    lm += "Email: " + gen("email", max_tokens=50)
    
[/code]

### 2. Используйте select() для фиксированных категорий[​](<#2-use-select-for-fixed-categories> "Direct link to 2. Use select() for Fixed Categories")

[code]
    # ✅ Хорошо: Гарантированно валидная категория
    lm += "Status: " + select(["pending", "approved", "rejected"], name="status")
      
    # ❌ Плохо: Может сгенерировать опечатки или невалидные значения
    lm += "Status: " + gen("status", max_tokens=20)
    
[/code]

### 3. Используйте токен-хилинг[​](<#3-leverage-token-healing> "Direct link to 3. Leverage Token Healing")

[code]
    # Токен-хилинг включён по умолчанию
    # Никаких специальных действий не требуется — просто соединяйте естественно
    lm += "The capital is " + gen("capital")  # Автоматическое исцеление
    
[/code]

### 4. Используйте стоп-последовательности[​](<#4-use-stop-sequences> "Direct link to 4. Use stop Sequences")

[code]
    # ✅ Хорошо: Остановка на новой строке для однострочных выводов
    lm += "Name: " + gen("name", stop="\n")
      
    # ❌ Плохо: Может сгенерировать несколько строк
    lm += "Name: " + gen("name", max_tokens=50)
    
[/code]

### 5. Создавайте переиспользуемые функции[​](<#5-create-reusable-functions> "Direct link to 5. Create Reusable Functions")

[code]
    # ✅ Хорошо: Переиспользуемый шаблон
    @guidance
    def generate_person(lm):
        lm += "Name: " + gen("name", stop="\n")
        lm += "\nAge: " + gen("age", regex=r"[0-9]+")
        return lm
      
    # Использование несколько раз
    lm = generate_person(lm)
    lm += "\n\n"
    lm = generate_person(lm)
    
[/code]

### 6. Балансируйте ограничения[​](<#6-balance-constraints> "Direct link to 6. Balance Constraints")

[code]
    # ✅ Хорошо: Разумные ограничения
    lm += gen("name", regex=r"[A-Za-z ]+", max_tokens=30)
      
    # ❌ Слишком строго: Может не сработать или быть очень медленным
    lm += gen("name", regex=r"^(John|Jane)$", max_tokens=10)
    
[/code]

## Сравнение с альтернативами[​](<#comparison-to-alternatives> "Direct link to Comparison to Alternatives")

| Особенность | Guidance | Instructor | Outlines | LMQL |
|---|---|---|---|---|
| Regex-ограничения | ✅ Да | ❌ Нет | ✅ Да | ✅ Да |
| Поддержка грамматик | ✅ CFG | ❌ Нет | ✅ CFG | ✅ CFG |
| Pydantic-валидация | ❌ Нет | ✅ Да | ✅ Да | ❌ Нет |
| Токен-хилинг | ✅ Да | ❌ Нет | ✅ Да | ❌ Нет |
| Локальные модели | ✅ Да | ⚠️ Ограничено | ✅ Да | ✅ Да |
| API-модели | ✅ Да | ✅ Да | ⚠️ Ограничено | ✅ Да |
| Python-синтаксис | ✅ Да | ✅ Да | ✅ Да | ❌ SQL-подобный |
| Порог входа | Низкий | Низкий | Средний | Высокий |

**Когда выбирать Guidance:**

  * Нужны ограничения с помощью regex/грамматик
  * Нужен токен-хилинг
  * Создание сложных рабочих процессов с управлением потоком
  * Использование локальных моделей (Transformers, llama.cpp)
  * Предпочтение Python-синтаксиса

**Когда выбирать альтернативы:**

  * Instructor: Нужна Pydantic-валидация с автоматическими повторами
  * Outlines: Нужна валидация JSON-схем
  * LMQL: Предпочтение декларативного синтаксиса запросов

## Характеристики производительности[​](<#performance-characteristics> "Direct link to Performance Characteristics")

**Снижение задержки:**

  * На 30-50% быстрее, чем традиционный промптинг для ограниченного вывода
  * Токен-хилинг уменьшает ненужную регенерацию
  * Грамматические ограничения предотвращают генерацию невалидных токенов

**Использование памяти:**

  * Минимальные накладные расходы по сравнению с неограниченной генерацией
  * Компиляция грамматик кэшируется после первого использования
  * Эффективная фильтрация токенов во время инференса

**Эффективность токенов:**

  * Предотвращает трату токенов на невалидный вывод
  * Не требует циклов повторных попыток
  * Прямой путь к валидному выводу

## Ресурсы[​](<#resources> "Direct link to Resources")

  * **Документация:** <https://guidance.readthedocs.io>
  * **GitHub:** <https://github.com/guidance-ai/guidance> (18k+ звёзд)
  * **Notebooks:** <https://github.com/guidance-ai/guidance/tree/main/notebooks>
  * **Discord:** Доступна поддержка сообщества

## См. также[​](<#see-also> "Direct link to See Also")

  * `references/constraints.md` — Полные шаблоны regex и грамматик
  * `references/backends.md` — Конфигурация для конкретных бэкендов
  * `references/examples.md` — Примеры для production

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Установка](<#installation>)
  * [Быстрый старт](<#quick-start>)
    * [Базовый пример: Структурированная генерация](<#basic-example-structured-generation>)
    * [С Anthropic Claude](<#with-anthropic-claude>)
  * [Основные концепции](<#core-concepts>)
    * [1. Контекстные менеджеры](<#1-context-managers>)
    * [2. Ограниченная генерация](<#2-constrained-generation>)
    * [3. Токен-хилинг (Token Healing)](<#3-token-healing>)
    * [4. Генерация на основе грамматик](<#4-grammar-based-generation>)
    * [5. Функции Guidance](<#5-guidance-functions>)
  * [Конфигурация бэкенда](<#backend-configuration>)
    * [Anthropic Claude](<#anthropic-claude>)
    * [OpenAI](<#openai>)
    * [Локальные модели (Transformers)](<#local-models-transformers>)
    * [Локальные модели (llama.cpp)](<#local-models-llamacpp>)
  * [Типовые шаблоны](<#common-patterns>)
    * [Шаблон 1: Генерация JSON](<#pattern-1-json-generation>)
    * [Шаблон 2: Классификация](<#pattern-2-classification>)
    * [Шаблон 3: Многошаговые рассуждения](<#pattern-3-multi-step-reasoning>)
    * [Шаблон 4: ReAct Агент](<#pattern-4-react-agent>)
    * [Шаблон 5: Извлечение данных](<#pattern-5-data-extraction>)
  * [Лучшие практики](<#best-practices>)
    * [1. Используйте Regex для проверки формата](<#1-use-regex-for-format-validation>)
    * [2. Используйте select() для фиксированных категорий](<#2-use-select-for-fixed-categories>)
    * [3. Используйте токен-хилинг](<#3-leverage-token-healing>)
    * [4. Используйте стоп-последовательности](<#4-use-stop-sequences>)
    * [5. Создавайте переиспользуемые функции](<#5-create-reusable-functions>)
    * [6. Балансируйте ограничения](<#6-balance-constraints>)
  * [Сравнение с альтернативами](<#comparison-to-alternatives>)
  * [Характеристики производительности](<#performance-characteristics>)
  * [Ресурсы](<#resources>)
  * [См. также](<#see-also>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-guidance -->
