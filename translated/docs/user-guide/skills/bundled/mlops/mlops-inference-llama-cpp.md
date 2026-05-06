On this page
Локальный GGUF-инференс через llama.cpp и поиск моделей на Hugging Face Hub.
## Информация о навыке[​](<#skill-metadata> "Прямая ссылка на информацию о навыке")

|---|---  
|Source| Встроенный (устанавливается по умолчанию)  
|Path| `skills/mlops/inference/llama-cpp`  
|Version| `2.1.2`  
|Author| Orchestra Research  
|License| MIT  
|Dependencies| `llama-cpp-python>=0.2.0`  
|Tags| `llama.cpp`, `GGUF`, `Quantization`, `Hugging Face Hub`, `CPU Inference`, `Apple Silicon`, `Edge Deployment`, `AMD GPUs`, `Intel GPUs`, `NVIDIA`, `URL-first`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# llama.cpp + GGUF
Используйте этот навык для локального GGUF-инференса, выбора квантизации или поиска репозиториев на Hugging Face для llama.cpp.
## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Запуск локальных моделей на CPU, Apple Silicon, CUDA, ROCm или Intel GPU
  * Поиск подходящего GGUF для конкретного репозитория на Hugging Face
  * Сборка команды `llama-server` или `llama-cli` из Hub
  * Поиск на Hub моделей, которые уже поддерживают llama.cpp
  * Перечисление доступных `.gguf`-файлов и их размеров для репозитория
  * Выбор между вариантами Q4/Q5/Q6/IQ в зависимости от RAM или VRAM пользователя


## Рабочий процесс поиска моделей[​](<#model-discovery-workflow> "Прямая ссылка на Рабочий процесс поиска моделей")
Предпочитайте URL-ориентированные workflow до того, как запрашивать `hf`, Python или пользовательские скрипты.
  1. Поиск подходящих репозиториев на Hub:
     * Базовый: `https://huggingface.co/models?apps=llama.cpp&sort=trending`
     * Добавьте `search=<термин>` для семейства моделей
     * Добавьте `num_parameters=min:0,max:24B` или аналогично, если у пользователя есть ограничения по размеру
  2. Откройте репозиторий в представлении локального приложения llama.cpp:
     * `https://huggingface.co/<repo>?local-app=llama.cpp`
  3. Используйте сниппет из local-app как источник истины, когда он виден:
     * скопируйте точную команду `llama-server` или `llama-cli`
     * сообщите рекомендуемый квантизатор точно так, как его показывает HF
  4. Прочитайте ту же страницу `?local-app=llama.cpp` как текст или HTML и извлеките раздел `Hardware compatibility`:
     * предпочитайте его точные метки квантизаторов и размеры общим таблицам
     * сохраняйте специфичные для репозитория метки, такие как `UD-Q4_K_M` или `IQ4_NL_XL`
     * если этот раздел не виден в загруженном исходном коде страницы, сообщите об этом и вернитесь к tree API плюс общие рекомендации по квантизации
  5. Запросите tree API для подтверждения того, что на самом деле существует:
     * `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`
     * оставьте записи, где `type` равен `file` и `path` заканчивается на `.gguf`
     * используйте `path` и `size` как источник истины для имён файлов и размеров в байтах
     * отделяйте квантизованные чекпоинты от файлов проектора `mmproj-*.gguf` и файлов шардинга `BF16/`
     * используйте `https://huggingface.co/<repo>/tree/main` только как запасной вариант для человека
  6. Если сниппет local-app не виден в тексте, восстановите команду из репозитория и выбранного квантизатора:
     * сокращённый выбор квантизатора: `llama-server -hf <repo>:<QUANT>`
     * запасной вариант с точным файлом: `llama-server --hf-repo <repo> --hf-file <filename.gguf>`
  7. Предлагайте конвертацию из весов Transformers только в том случае, если репозиторий уже не содержит GGUF-файлы.


## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Установка llama.cpp[​](<#install-llamacpp> "Прямая ссылка на Установка llama.cpp")
[code] 
    # macOS / Linux (simplest)  
    brew install llama.cpp  
    
[/code]
[code] 
    winget install llama.cpp  
    
[/code]
[code] 
    git clone https://github.com/ggml-org/llama.cpp  
    cd llama.cpp  
    cmake -B build  
    cmake --build build --config Release  
    
[/code]
### Запуск напрямую с Hugging Face Hub[​](<#run-directly-from-the-hugging-face-hub> "Прямая ссылка на Запуск напрямую с Hugging Face Hub")
[code] 
    llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0  
    
[/code]
[code] 
    llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0  
    
[/code]
### Запуск точного GGUF-файла с Hub[​](<#run-an-exact-gguf-file-from-the-hub> "Прямая ссылка на Запуск точного GGUF-файла с Hub")
Используйте, когда tree API показывает нестандартные имена файлов или точный сниппет HF отсутствует.
[code] 
    llama-server \\  
        --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \\  
        --hf-file Phi-3-mini-4k-instruct-q4.gguf \\  
        -c 4096  
    
[/code]
### Проверка сервера на совместимость с OpenAI[​](<#openai-compatible-server-check> "Прямая ссылка на Проверка сервера на совместимость с OpenAI")
[code] 
    curl http://localhost:8080/v1/chat/completions \\  
      -H "Content-Type: application/json" \\  
      -d '{  
        "messages": [  
          {"role": "user", "content": "Write a limerick about Python exceptions"}  
        ]  
      }'  
    
[/code]
## Привязки Python (llama-cpp-python)[​](<#python-bindings-llama-cpp-python> "Прямая ссылка на Привязки Python (llama-cpp-python)")
`pip install llama-cpp-python` (CUDA: `CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir`; Metal: `CMAKE_ARGS="-DGGML_METAL=on" ...`).
### Базовая генерация[​](<#basic-generation> "Прямая ссылка на Базовая генерация")
[code] 
    from llama_cpp import Llama  
      
    llm = Llama(  
        model_path="./model-q4_k_m.gguf",  
        n_ctx=4096,  
        n_gpu_layers=35,     # 0 for CPU, 99 to offload everything  
        n_threads=8,  
    )  
      
    out = llm("What is machine learning?", max_tokens=256, temperature=0.7)  
    print(out["choices"][0]["text"])  
    
[/code]
### Чат + стриминг[​](<#chat--streaming> "Прямая ссылка на Чат + стриминг")
[code] 
    llm = Llama(  
        model_path="./model-q4_k_m.gguf",  
        n_ctx=4096,  
        n_gpu_layers=35,  
        chat_format="llama-3",   # or "chatml", "mistral", etc.  
    )  
      
    resp = llm.create_chat_completion(  
        messages=[  
            {"role": "system", "content": "You are a helpful assistant."},  
            {"role": "user", "content": "What is Python?"},  
        ],  
        max_tokens=256,  
    )  
    print(resp["choices"][0]["message"]["content"])  
      
    # Streaming  
    for chunk in llm("Explain quantum computing:", max_tokens=256, stream=True):  
        print(chunk["choices"][0]["text"], end="", flush=True)  
    
[/code]
### Эмбеддинги[​](<#embeddings> "Прямая ссылка на Эмбеддинги")
[code] 
    llm = Llama(model_path="./model-q4_k_m.gguf", embedding=True, n_gpu_layers=35)  
    vec = llm.embed("This is a test sentence.")  
    print(f"Embedding dimension: {len(vec)}")  
    
[/code]
Вы также можете загрузить GGUF напрямую с Hub:
[code] 
    llm = Llama.from_pretrained(  
        repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",  
        filename="*Q4_K_M.gguf",  
        n_gpu_layers=35,  
    )  
    
[/code]
## Выбор квантизатора[​](<#choosing-a-quant> "Прямая ссылка на Выбор квантизатора")
Сначала используйте страницу Hub, затем общие эвристики.
  * Предпочитайте точный квантизатор, который HF помечает как совместимый с профилем оборудования пользователя.
  * Для общего чата начинайте с `Q4_K_M`.
  * Для кода или технической работы предпочитайте `Q5_K_M` или `Q6_K`, если позволяет память.
  * При очень ограниченном бюджете RAM рассмотрите `Q3_K_M`, варианты `IQ` или `Q2` только если пользователь явно ставит вместимость выше качества.
  * Для мультимодальных репозиториев упоминайте `mmproj-*.gguf` отдельно. Проектор — это не основной файл модели.
  * Не нормализуйте собственные метки репозитория. Если на странице указано `UD-Q4_K_M`, сообщайте `UD-Q4_K_M`.


## Извлечение доступных GGUF из репозитория[​](<#extracting-available-ggufs-from-a-repo> "Прямая ссылка на Извлечение доступных GGUF из репозитория")
Когда пользователь спрашивает, какие GGUF существуют, возвращайте:
  * имя файла
  * размер файла
  * метку квантизатора
  * является ли это основной моделью или вспомогательным проектором


Игнорируйте, если не запрошено:
  * README
  * файлы шардинга BF16
  * imatrix-блоб или артефакты калибровки


Используйте tree API для этого шага:
  * `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`


Для репозитория вроде `unsloth/Qwen3.6-35B-A3B-GGUF` страница local-app может показывать чипы квантизаторов, такие как `UD-Q4_K_M`, `UD-Q5_K_M`, `UD-Q6_K` и `Q8_0`, в то время как tree API предоставляет точные пути к файлам, такие как `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` и `Qwen3.6-35B-A3B-Q8_0.gguf` с размерами в байтах. Используйте tree API для преобразования метки квантизатора в точное имя файла.
## Шаблоны поиска[​](<#search-patterns> "Прямая ссылка на Шаблоны поиска")
Используйте эти формы URL напрямую:
[code] 
    https://huggingface.co/models?apps=llama.cpp&sort=trending  
    https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending  
    https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending  
    https://huggingface.co/<repo>?local-app=llama.cpp  
    https://huggingface.co/api/models/<repo>/tree/main?recursive=true  
    https://huggingface.co/<repo>/tree/main  
    
[/code]
## Формат вывода[​](<#output-format> "Прямая ссылка на Формат вывода")
При ответе на запросы о поиске предпочитайте компактный структурированный результат вроде:
[code] 
    Repo: <repo>  
    Recommended quant from HF: <label> (<size>)  
    llama-server: <command>  
    Other GGUFs:  
    - <filename> - <size>  
    - <filename> - <size>  
    Source URLs:  
    - <local-app URL>  
    - <tree API URL>  
    
[/code]
## Ссылки[​](<#references> "Прямая ссылка на Ссылки")
  * **[hub-discovery.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/hub-discovery.md>)** \- URL-ориентированные workflow Hugging Face, шаблоны поиска, извлечение GGUF и восстановление команд
  * **[advanced-usage.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/advanced-usage.md>)** — спекулятивное декодирование, пакетный инференс, грамматически-ограниченная генерация, LoRA, multi-GPU, пользовательские сборки, бенчмарк-скрипты
  * **[quantization.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/quantization.md>)** — компромиссы качества квантизации, когда использовать Q4/Q5/Q6/IQ, масштабирование размера модели, imatrix
  * **[server.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/server.md>)** — запуск сервера напрямую с Hub, эндпоинты OpenAI API, развёртывание Docker, балансировка нагрузки NGINX, мониторинг
  * **[optimization.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/optimization.md>)** — многопоточность CPU, BLAS, эвристика выгрузки на GPU, настройка батчей, бенчмарки
  * **[troubleshooting.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/inference/llama-cpp/references/troubleshooting.md>)** — проблемы установки/конвертации/квантизации/инференса/сервера, Apple Silicon, отладка


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **GitHub** : <https://github.com/ggml-org/llama.cpp>
  * **Hugging Face GGUF + llama.cpp docs** : <https://huggingface.co/docs/hub/gguf-llamacpp>
  * **Hugging Face Local Apps docs** : <https://huggingface.co/docs/hub/main/local-apps>
  * **Hugging Face Local Agents docs** : <https://huggingface.co/docs/hub/agents-local>
  * **Example local-app page** : <https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF?local-app=llama.cpp>
  * **Example tree API** : <https://huggingface.co/api/models/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main?recursive=true>
  * **Example llama.cpp search** : [https://huggingface.co/models?num_parameters=min:0,max:24B&apps=llama.cpp&sort=trending](<https://huggingface.co/models?num_parameters=min:0,max:24B&apps=llama.cpp&sort=trending>)
  * **License** : MIT


  * [Информация о навыке](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Рабочий процесс поиска моделей](<#model-discovery-workflow>)
  * [Быстрый старт](<#quick-start>)
    * [Установка llama.cpp](<#install-llamacpp>)
    * [Запуск напрямую с Hugging Face Hub](<#run-directly-from-the-hugging-face-hub>)
    * [Запуск точного GGUF-файла с Hub](<#run-an-exact-gguf-file-from-the-hub>)
    * [Проверка сервера на совместимость с OpenAI](<#openai-compatible-server-check>)
  * [Привязки Python (llama-cpp-python)](<#python-bindings-llama-cpp-python>)
    * [Базовая генерация](<#basic-generation>)
    * [Чат + стриминг](<#chat--streaming>)
    * [Эмбеддинги](<#embeddings>)
  * [Выбор квантизатора](<#choosing-a-quant>)
  * [Извлечение доступных GGUF из репозитория](<#extracting-available-ggufs-from-a-repo>)
  * [Шаблоны поиска](<#search-patterns>)
  * [Формат вывода](<#output-format>)
  * [Ссылки](<#references>)
  * [Ресурсы](<#resources>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-inference-llama-cpp -->
