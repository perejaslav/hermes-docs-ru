On this page

Hermes Agent сохраняет траектории разговоров в совместимом с ShareGPT формате JSONL для использования в качестве обучающих данных, артефактов отладки и наборов данных для обучения с подкреплением.

Исходные файлы: `agent/trajectory.py`, `run_agent.py` (поиск `_save_trajectory`), `batch_runner.py`

## Соглашение об именовании файлов[​](<#file-naming-convention> "Прямая ссылка на Соглашение об именовании файлов")

Траектории записываются в файлы в текущей рабочей директории:

Файл| Когда  
---|---  
`trajectory_samples.jsonl`| Разговоры, завершённые успешно (`completed=True`)  
`failed_trajectories.jsonl`| Разговоры, завершившиеся неудачей или прерванные (`completed=False`)  

Пакетный запуск (`batch_runner.py`) записывает результат в пользовательский выходной файл для каждого пакета (например, `batch_001_output.jsonl`) с дополнительными полями метаданных.

Вы можете переопределить имя файла через параметр `filename` в `save_trajectory()`.

## Формат записи JSONL[​](<#jsonl-entry-format> "Прямая ссылка на Формат записи JSONL")

Каждая строка в файле — это самодостаточный JSON-объект. Существует два варианта:

### Формат CLI/Интерактивный (из `_save_trajectory`)[​](<#cliinteractive-format-from-_save_trajectory> "Прямая ссылка на cliinteractive-format-from-_save_trajectory")

[code] 
    {  
      "conversations": [ ... ],  
      "timestamp": "2026-03-30T14:22:31.456789",  
      "model": "anthropic/claude-sonnet-4.6",  
      "completed": true  
    }  
    
[/code]

### Формат пакетного запуска (из `batch_runner.py`)[​](<#batch-runner-format-from-batch_runnerpy> "Прямая ссылка на batch-runner-format-from-batch_runnerpy")

[code] 
    {  
      "prompt_index": 42,  
      "conversations": [ ... ],  
      "metadata": { "prompt_source": "gsm8k", "difficulty": "hard" },  
      "completed": true,  
      "partial": false,  
      "api_calls": 7,  
      "toolsets_used": ["code_tools", "file_tools"],  
      "tool_stats": {  
        "terminal": {"count": 3, "success": 3, "failure": 0},  
        "read_file": {"count": 2, "success": 2, "failure": 0},  
        "write_file": {"count": 0, "success": 0, "failure": 0}  
      },  
      "tool_error_counts": {  
        "terminal": 0,  
        "read_file": 0,  
        "write_file": 0  
      }  
    }  
    
[/code]

Словари `tool_stats` и `tool_error_counts` нормализованы так, чтобы включать ВСЕ возможные инструменты (из `model_tools.TOOL_TO_TOOLSET_MAP`) с нулевыми значениями по умолчанию, обеспечивая единую схему для всех записей при загрузке наборов данных HuggingFace.

## Массив разговоров (формат ShareGPT)[​](<#conversations-array-sharegpt-format> "Прямая ссылка на Массив разговоров (формат ShareGPT)")

Массив `conversations` использует ролевые соглашения ShareGPT:

Роль API| ShareGPT `from`  
---|---  
system| `"system"`  
user| `"human"`  
assistant| `"gpt"`  
tool| `"tool"`  

### Полный пример[​](<#complete-example> "Прямая ссылка на Полный пример")

[code] 
    {  
      "conversations": [  
        {  
          "from": "system",  
          "value": "You are a function calling AI model. You are provided with function signatures within <tools> </tools> XML tags. You may call one or more functions to assist with the user query. If available tools are not relevant in assisting with user query, just respond in natural conversational language. Don't make assumptions about what values to plug into functions. After calling & executing the functions, you will be provided with function results within <tool_response> </tool_response> XML tags. Here are the available tools:\n<tools>\n[{\"name\": \"terminal\", \"description\": \"Execute shell commands\", \"parameters\": {\"type\": \"object\", \"properties\": {\"command\": {\"type\": \"string\"}}}, \"required\": null}]\n</tools>\nFor each function call return a JSON object, with the following pydantic model json schema for each:\n{'title': 'FunctionCall', 'type': 'object', 'properties': {'name': {'title': 'Name', 'type': 'string'}, 'arguments': {'title': 'Arguments', 'type': 'object'}}, 'required': ['name', 'arguments']}\nEach function call should be enclosed within <tool_call> </tool_call> XML tags.\nExample:\n<tool_call>\n{'name': <function-name>,'arguments': <args-dict>}\n</tool_call>"  
        },  
        {  
          "from": "human",  
          "value": "What Python version is installed?"  
        },  
        {  
          "from": "gpt",  
          "value": "<think>\nThe user wants to know the Python version. I should run python3 --version.\n</think>\n<tool_call>\n{\"name\": \"terminal\", \"arguments\": {\"command\": \"python3 --version\"}}\n</tool_call>"  
        },  
        {  
          "from": "tool",  
          "value": "<tool_response>\n{\"tool_call_id\": \"call_abc123\", \"name\": \"terminal\", \"content\": \"Python 3.11.6\"}\n</tool_response>"  
        },  
        {  
          "from": "gpt",  
          "value": "<think>\nGot the version. I can now answer the user.\n</think>\nPython 3.11.6 is installed on this system."  
        }  
      ],  
      "timestamp": "2026-03-30T14:22:31.456789",  
      "model": "anthropic/claude-sonnet-4.6",  
      "completed": true  
    }  
    
[/code]

## Правила нормализации[​](<#normalization-rules> "Прямая ссылка на Правила нормализации")

### Разметка содержимого рассуждений[​](<#reasoning-content-markup> "Прямая ссылка на Разметка содержимого рассуждений")

Конвертер траекторий нормализует ВСЕ рассуждения в теги `<think>`, независимо от того, как модель их изначально сгенерировала:

  1. **Нативные токены рассуждений** (поле `msg["reasoning"]` от провайдеров вроде Anthropic, OpenAI o-series): Оборачиваются как `<think>\n{reasoning}\n</think>\n` и добавляются перед содержимым.
  2. **REASONING_SCRATCHPAD XML** (когда нативное рассуждение отключено и модель рассуждает через XML, заданный системным промптом): Теги `<REASONING_SCRATCHPAD>` преобразуются в `<think>` через `convert_scratchpad_to_think()`.
  3. **Пустые блоки think**: Каждый ход `gpt` гарантированно содержит блок `<think>`. Если рассуждений не было, вставляется пустой блок: `<think>\n</think>\n` — это обеспечивает единый формат для обучающих данных.

### Нормализация вызовов инструментов[​](<#tool-call-normalization> "Прямая ссылка на Нормализацию вызовов инструментов")

Вызовы инструментов из формата API (с `tool_call_id`, именем функции, аргументами в виде JSON-строки) преобразуются в JSON, обёрнутый в XML:

[code] 
    <tool_call>  
    {"name": "terminal", "arguments": {"command": "ls -la"}}  
    </tool_call>  
    
[/code]

  * Аргументы парсятся из JSON-строк обратно в объекты (не двойное кодирование)
  * Если парсинг JSON не удался (не должно происходить — проверяется во время разговора), используется пустой `{}` с записью предупреждения в лог
  * Несколько вызовов инструментов за один ход ассистента порождают несколько блоков `<tool_call>` в одном сообщении `gpt`

### Нормализация ответов инструментов[​](<#tool-response-normalization> "Прямая ссылка на Нормализацию ответов инструментов")

Все результаты выполнения инструментов, следующие за сообщением ассистента, группируются в один ход `tool` с JSON-ответами, обёрнутыми в XML:

[code] 
    <tool_response>  
    {"tool_call_id": "call_abc123", "name": "terminal", "content": "output here"}  
    </tool_response>  
    
[/code]

  * Если содержимое инструмента выглядит как JSON (начинается с `{` или `[`), оно парсится, чтобы поле content содержало JSON-объект/массив, а не строку
  * Несколько результатов инструментов объединяются через перевод строки в одном сообщении
  * Имя инструмента сопоставляется по позиции с массивом `tool_calls` родительского ассистента

### Системное сообщение[​](<#system-message> "Прямая ссылка на Системное сообщение")

Системное сообщение генерируется в момент сохранения (не берётся из разговора). Оно следует шаблону промпта вызова функций Hermes и содержит:

  * Вступление, объясняющее протокол вызова функций
  * XML-блок `<tools>`, содержащий JSON-определения инструментов
  * Ссылку на схему для объектов `FunctionCall`
  * Пример `<tool_call>`

Определения инструментов включают `name`, `description`, `parameters` и `required` (установлено в `null` для соответствия каноническому формату).

## Загрузка траекторий[​](<#loading-trajectories> "Прямая ссылка на Загрузку траекторий")

Траектории — это стандартный JSONL; загружайте любым JSON-lines ридером:

[code] 
    import json  
      
    def load_trajectories(path: str):  
        """Загрузка записей траекторий из JSONL-файла."""  
        entries = []  
        with open(path, "r", encoding="utf-8") as f:  
            for line in f:  
                line = line.strip()  
                if line:  
                    entries.append(json.loads(line))  
        return entries  
      
    # Фильтрация только успешных завершений  
    successful = [e for e in load_trajectories("trajectory_samples.jsonl")  
                  if e.get("completed")]  
      
    # Извлечение только разговоров для обучения  
    training_data = [e["conversations"] for e in successful]  
    
[/code]

### Загрузка для наборов данных HuggingFace[​](<#loading-for-huggingface-datasets> "Прямая ссылка на Загрузку для наборов данных HuggingFace")

[code] 
    from datasets import load_dataset  
      
    ds = load_dataset("json", data_files="trajectory_samples.jsonl")  
    
[/code]

Нормализованная схема `tool_stats` гарантирует, что все записи имеют одинаковые столбцы, предотвращая ошибки несоответствия схемы Arrow при загрузке набора данных.

## Управление сохранением траекторий[​](<#controlling-trajectory-saving> "Прямая ссылка на Управление сохранением траекторий")

В CLI сохранение траекторий управляется через:

[code] 
    # config.yaml  
    agent:  
      save_trajectories: true  # по умолчанию: false  
    
[/code]

Или через флаг `--save-trajectories`. Когда агент инициализируется с `save_trajectories=True`, метод `_save_trajectory()` вызывается в конце каждого хода разговора.

Пакетный запуск всегда сохраняет траектории (это его основная цель).

Сэмплы с нулевым количеством рассуждений во всех ходах автоматически отбрасываются пакетным запуском, чтобы избежать загрязнения обучающих данных примерами без рассуждений.

  * [Соглашение об именовании файлов](<#file-naming-convention>)
  * [Формат записи JSONL](<#jsonl-entry-format>)
    * [Формат CLI/Интерактивный (из `_save_trajectory`)](<#cliinteractive-format-from-_save_trajectory>)
    * [Формат пакетного запуска (из `batch_runner.py`)](<#batch-runner-format-from-batch_runnerpy>)
  * [Массив разговоров (формат ShareGPT)](<#conversations-array-sharegpt-format>)
    * [Полный пример](<#complete-example>)
  * [Правила нормализации](<#normalization-rules>)
    * [Разметка содержимого рассуждений](<#reasoning-content-markup>)
    * [Нормализация вызовов инструментов](<#tool-call-normalization>)
    * [Нормализация ответов инструментов](<#tool-response-normalization>)
    * [Системное сообщение](<#system-message>)
  * [Загрузка траекторий](<#loading-trajectories>)
    * [Загрузка для наборов данных HuggingFace](<#loading-for-huggingface-datasets>)
  * [Управление сохранением траекторий](<#controlling-trajectory-saving>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format -->
