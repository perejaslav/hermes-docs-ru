On this page
Hermes — это не только CLI-инструмент. Вы можете импортировать `AIAgent` напрямую и использовать его программно в своих Python-скриптах, веб-приложениях или пайплайнах автоматизации. Это руководство покажет вам, как это сделать.
* * *
## Installation[​](<#installation> "Direct link to Installation")
Установите Hermes напрямую из репозитория:
[code] 
    pip install git+https://github.com/NousResearch/hermes-agent.git  
    
[/code]
Или с помощью [uv](<https://docs.astral.sh/uv/>):
[code] 
    uv pip install git+https://github.com/NousResearch/hermes-agent.git  
    
[/code]
Вы также можете зафиксировать его в своём `requirements.txt`:
[code] 
    hermes-agent @ git+https://github.com/NousResearch/hermes-agent.git  
    
[/code]
tip
При использовании Hermes как библиотеки требуются те же переменные окружения, что и для CLI. Как минимум установите `OPENROUTER_API_KEY` (или `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` при прямом доступе к провайдеру).
* * *
## Basic Usage[​](<#basic-usage> "Direct link to Basic Usage")
Самый простой способ использовать Hermes — метод `chat()`: передайте сообщение и получите строку в ответ:
[code] 
    from run_agent import AIAgent  
      
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        quiet_mode=True,  
    )  
    response = agent.chat("What is the capital of France?")  
    print(response)  
    
[/code]
`chat()` обрабатывает весь цикл диалога внутренне — вызовы инструментов, повторные попытки и всё остальное — и возвращает только итоговый текстовый ответ.
warning
Всегда устанавливайте `quiet_mode=True` при встраивании Hermes в ваш собственный код. Без этого агент будет выводить CLI-спиннеры, индикаторы прогресса и другой терминальный вывод, который засорит вывод вашего приложения.
* * *
## Full Conversation Control[​](<#full-conversation-control> "Direct link to Full Conversation Control")
Для более полного контроля над диалогом используйте `run_conversation()` напрямую. Он возвращает словарь с полным ответом, историей сообщений и метаданными:
[code] 
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        quiet_mode=True,  
    )  
      
    result = agent.run_conversation(  
        user_message="Search for recent Python 3.13 features",  
        task_id="my-task-1",  
    )  
      
    print(result["final_response"])  
    print(f"Messages exchanged: {len(result['messages'])}")  
    
[/code]
Возвращаемый словарь содержит:
  * **`final_response`** — Итоговый текстовый ответ агента
  * **`messages`** — Полная история сообщений (системное, пользователь, ассистент, вызовы инструментов)
  * **`task_id`** — Идентификатор задачи, используемый для изоляции ВМ


Вы также можете передать собственное системное сообщение, которое переопределяет эфемерный системный промпт для данного вызова:
[code] 
    result = agent.run_conversation(  
        user_message="Explain quicksort",  
        system_message="You are a computer science tutor. Use simple analogies.",  
    )  
    
[/code]
* * *
## Configuring Tools[​](<#configuring-tools> "Direct link to Configuring Tools")
Управляйте тем, какие наборы инструментов доступны агенту, с помощью `enabled_toolsets` или `disabled_toolsets`:
[code] 
    # Only enable web tools (browsing, search)  
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        enabled_toolsets=["web"],  
        quiet_mode=True,  
    )  
      
    # Enable everything except terminal access  
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        disabled_toolsets=["terminal"],  
        quiet_mode=True,  
    )  
    
[/code]
tip
Используйте `enabled_toolsets`, когда вам нужен минимальный, ограниченный агент (например, только веб-поиск для исследовательского бота). Используйте `disabled_toolsets`, когда вам нужно большинство возможностей, но требуется ограничить конкретные (например, без доступа к терминалу в общей среде).
* * *
## Multi-turn Conversations[​](<#multi-turn-conversations> "Direct link to Multi-turn Conversations")
Поддерживайте состояние диалога на протяжении нескольких шагов, передавая историю сообщений обратно:
[code] 
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        quiet_mode=True,  
    )  
      
    # First turn  
    result1 = agent.run_conversation("My name is Alice")  
    history = result1["messages"]  
      
    # Second turn — agent remembers the context  
    result2 = agent.run_conversation(  
        "What's my name?",  
        conversation_history=history,  
    )  
    print(result2["final_response"])  # "Your name is Alice."  
    
[/code]
Параметр `conversation_history` принимает список `messages` из предыдущего результата. Агент копирует его внутренне, поэтому ваш исходный список никогда не изменяется.
* * *
## Saving Trajectories[​](<#saving-trajectories> "Direct link to Saving Trajectories")
Включите сохранение траекторий для захвата диалогов в формате ShareGPT — полезно для генерации обучающих данных или отладки:
[code] 
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        save_trajectories=True,  
        quiet_mode=True,  
    )  
      
    agent.chat("Write a Python function to sort a list")  
    # Saves to trajectory_samples.jsonl in ShareGPT format  
    
[/code]
Каждый диалог добавляется в виде отдельной JSONL-строки, что упрощает сбор наборов данных из автоматических запусков.
* * *
## Custom System Prompts[​](<#custom-system-prompts> "Direct link to Custom System Prompts")
Используйте `ephemeral_system_prompt`, чтобы задать собственный системный промпт, который направляет поведение агента, но **не** сохраняется в файлы траекторий (поддерживая чистоту обучающих данных):
[code] 
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        ephemeral_system_prompt="You are a SQL expert. Only answer database questions.",  
        quiet_mode=True,  
    )  
      
    response = agent.chat("How do I write a JOIN query?")  
    print(response)  
    
[/code]
Это идеально подходит для создания специализированных агентов — ревьюера кода, документатора, SQL-ассистента — все с использованием одного и того же базового инструментария.
* * *
## Batch Processing[​](<#batch-processing> "Direct link to Batch Processing")
Для параллельной обработки множества промптов Hermes включает `batch_runner.py`. Он управляет одновременными экземплярами `AIAgent` с надлежащей изоляцией ресурсов:
[code] 
    python batch_runner.py --input prompts.jsonl --output results.jsonl  
    
[/code]
Каждый промпт получает собственный `task_id` и изолированное окружение. Если вам нужна собственная пакетная логика, вы можете построить её с использованием `AIAgent` напрямую:
[code] 
    import concurrent.futures  
    from run_agent import AIAgent  
      
    prompts = [  
        "Explain recursion",  
        "What is a hash table?",  
        "How does garbage collection work?",  
    ]  
      
    def process_prompt(prompt):  
        # Create a fresh agent per task for thread safety  
        agent = AIAgent(  
            model="anthropic/claude-sonnet-4",  
            quiet_mode=True,  
            skip_memory=True,  
        )  
        return agent.chat(prompt)  
      
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:  
        results = list(executor.map(process_prompt, prompts))  
      
    for prompt, result in zip(prompts, results):  
        print(f"Q: {prompt}\nA: {result}\n")  
    
[/code]
warning
Всегда создавайте **новый экземпляр `AIAgent`** для каждого потока или задачи. Агент поддерживает внутреннее состояние (история диалога, сессии инструментов, счётчики итераций), которое не является потокобезопасным для совместного использования.
* * *
## Integration Examples[​](<#integration-examples> "Direct link to Integration Examples")
### FastAPI Endpoint[​](<#fastapi-endpoint> "Direct link to FastAPI Endpoint")
[code] 
    from fastapi import FastAPI  
    from pydantic import BaseModel  
    from run_agent import AIAgent  
      
    app = FastAPI()  
      
    class ChatRequest(BaseModel):  
        message: str  
        model: str = "anthropic/claude-sonnet-4"  
      
    @app.post("/chat")  
    async def chat(request: ChatRequest):  
        agent = AIAgent(  
            model=request.model,  
            quiet_mode=True,  
            skip_context_files=True,  
            skip_memory=True,  
        )  
        response = agent.chat(request.message)  
        return {"response": response}  
    
[/code]
### Discord Bot[​](<#discord-bot> "Direct link to Discord Bot")
[code] 
    import discord  
    from run_agent import AIAgent  
      
    client = discord.Client(intents=discord.Intents.default())  
      
    @client.event  
    async def on_message(message):  
        if message.author == client.user:  
            return  
        if message.content.startswith("!hermes "):  
            query = message.content[8:]  
            agent = AIAgent(  
                model="anthropic/claude-sonnet-4",  
                quiet_mode=True,  
                skip_context_files=True,  
                skip_memory=True,  
                platform="discord",  
            )  
            response = agent.chat(query)  
            await message.channel.send(response[:2000])  
      
    client.run("YOUR_DISCORD_TOKEN")  
    
[/code]
### CI/CD Pipeline Step[​](<#cicd-pipeline-step> "Direct link to CI/CD Pipeline Step")
[code] 
    #!/usr/bin/env python3  
    """CI step: auto-review a PR diff."""  
    import subprocess  
    from run_agent import AIAgent  
      
    diff = subprocess.check_output(["git", "diff", "main...HEAD"]).decode()  
      
    agent = AIAgent(  
        model="anthropic/claude-sonnet-4",  
        quiet_mode=True,  
        skip_context_files=True,  
        skip_memory=True,  
        disabled_toolsets=["terminal", "browser"],  
    )  
      
    review = agent.chat(  
        f"Review this PR diff for bugs, security issues, and style problems:\n\n{diff}"  
    )  
    print(review)  
    
[/code]
* * *
## Key Constructor Parameters[​](<#key-constructor-parameters> "Direct link to Key Constructor Parameters")
Параметр| Тип| По умолчанию| Описание  
---|---|---|---  
`model`| `str`| `"anthropic/claude-opus-4.6"`| Модель в формате OpenRouter  
`quiet_mode`| `bool`| `False`| Подавлять вывод CLI  
`enabled_toolsets`| `List[str]`| `None`| Разрешить конкретные наборы инструментов  
`disabled_toolsets`| `List[str]`| `None`| Запретить конкретные наборы инструментов  
`save_trajectories`| `bool`| `False`| Сохранять диалоги в JSONL  
`ephemeral_system_prompt`| `str`| `None`| Собственный системный промпт (не сохраняется в траекториях)  
`max_iterations`| `int`| `90`| Максимальное количество итераций вызова инструментов на диалог  
`skip_context_files`| `bool`| `False`| Пропустить загрузку файлов AGENTS.md  
`skip_memory`| `bool`| `False`| Отключить чтение/запись постоянной памяти  
`api_key`| `str`| `None`| API-ключ (использует переменные окружения, если не указан)  
`base_url`| `str`| `None`| Пользовательский URL API-эндпоинта  
`platform`| `str`| `None`| Подсказка платформы (`"discord"`, `"telegram"` и т.д.)  
* * *
## Important Notes[​](<#important-notes> "Direct link to Important Notes")
tip
  * Установите **`skip_context_files=True`**, если вы не хотите, чтобы файлы `AGENTS.md` из рабочей директории загружались в системный промпт.
  * Установите **`skip_memory=True`**, чтобы предотвратить чтение или запись агентом постоянной памяти — рекомендуется для stateless API-эндпоинтов.
  * Параметр `platform` (например, `"discord"`, `"telegram"`) добавляет подсказки форматирования для конкретной платформы, чтобы агент адаптировал стиль вывода.


warning
  * **Потокобезопасность**: Создавайте один экземпляр `AIAgent` на поток или задачу. Никогда не используйте один экземпляр в конкурентных вызовах.
  * **Очистка ресурсов**: Агент автоматически очищает ресурсы (терминальные сессии, экземпляры браузера) после завершения диалога. Если вы работаете в долгоживущем процессе, убедитесь, что каждый диалог завершается нормально.
  * **Лимиты итераций**: Значение `max_iterations=90` по умолчанию является щедрым. Для простых сценариев вопросов-ответов рассмотрите возможность его снижения (например, `max_iterations=10`), чтобы предотвратить бесконечные циклы вызовов инструментов и контролировать расходы.


  * [Installation](<#installation>)
  * [Basic Usage](<#basic-usage>)
  * [Full Conversation Control](<#full-conversation-control>)
  * [Configuring Tools](<#configuring-tools>)
  * [Multi-turn Conversations](<#multi-turn-conversations>)
  * [Saving Trajectories](<#saving-trajectories>)
  * [Custom System Prompts](<#custom-system-prompts>)
  * [Batch Processing](<#batch-processing>)
  * [Integration Examples](<#integration-examples>)
    * [FastAPI Endpoint](<#fastapi-endpoint>)
    * [Discord Bot](<#discord-bot>)
    * [CI/CD Pipeline Step](<#cicd-pipeline-step>)
  * [Key Constructor Parameters](<#key-constructor-parameters>)
  * [Important Notes](<#important-notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/python-library -->
