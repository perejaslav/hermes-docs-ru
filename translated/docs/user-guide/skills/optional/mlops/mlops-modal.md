On this page
Serverless GPU облачная платформа для выполнения ML-задач. Используйте, когда нужен доступ к GPU по требованию без управления инфраструктурой, развёртывание ML-моделей в виде API или выполнение пакетных задач с автоматическим масштабированием.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на метаданные скилла")
|   |
|---|---|
|Source| Optional — install with `hermes skills install official/mlops/modal` |
|Path| `optional-skills/mlops/modal` |
|Version| `1.0.0` |
|Author| Orchestra Research |
|License| MIT |
|Dependencies| `modal>=0.64.0` |
|Tags| `Infrastructure`, `Serverless`, `GPU`, `Cloud`, `Deployment`, `Modal` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Modal Serverless GPU
Comprehensive guide to running ML workloads on Modal's serverless GPU cloud platform.
## When to use Modal[​](<#when-to-use-modal> "Прямая ссылка на When to use Modal")
**Используйте Modal когда:**
  * Нужно выполнять GPU-интенсивные ML-задачи без управления инфраструктурой
  * Развёртываете ML-модели как само-масштабируемые API
  * Запускаете пакетные задачи (обучение, инференс, обработка данных)
  * Нужна посекундная оплата GPU без затрат на простой
  * Быстро прототипируете ML-приложения
  * Запускаете задачи по расписанию (cron-подобные задачи)


**Ключевые возможности:**
  * **Serverless GPU** : T4, L4, A10G, L40S, A100, H100, H200, B200 по требованию
  * **Python-native** : Определение инфраструктуры в Python-коде, без YAML
  * **Автомасштабирование** : Масштабирование до нуля, масштабирование до 100+ GPU мгновенно
  * **Субсекундный холодный старт** : Rust-инфраструктура для быстрого запуска контейнеров
  * **Кэширование контейнеров** : Слои образов кэшируются для быстрой итерации
  * **Веб-эндпоинты** : Развёртывание функций как REST API с обновлениями без даунтайма


**Используйте альтернативы вместо:**
  * **RunPod** : Для долгоживущих подов с постоянным состоянием
  * **Lambda Labs** : Для зарезервированных GPU-инстансов
  * **SkyPilot** : Для мультиоблачной оркестрации и оптимизации затрат
  * **Kubernetes** : Для сложных многосервисных архитектур


## Quick start[​](<#quick-start> "Прямая ссылка на Quick start")
### Installation[​](<#installation> "Прямая ссылка на Installation")
[code] 
    pip install modal  
    modal setup  # Opens browser for authentication  
    
[/code]
### Hello World with GPU[​](<#hello-world-with-gpu> "Прямая ссылка на Hello World with GPU")
[code] 
    import modal  
      
    app = modal.App("hello-gpu")  
      
    @app.function(gpu="T4")  
    def gpu_info():  
        import subprocess  
        return subprocess.run(["nvidia-smi"], capture_output=True, text=True).stdout  
      
    @app.local_entrypoint()  
    def main():  
        print(gpu_info.remote())  
    
[/code]
Запуск: `modal run hello_gpu.py`
### Basic inference endpoint[​](<#basic-inference-endpoint> "Прямая ссылка на Basic inference endpoint")
[code] 
    import modal  
      
    app = modal.App("text-generation")  
    image = modal.Image.debian_slim().pip_install("transformers", "torch", "accelerate")  
      
    @app.cls(gpu="A10G", image=image)  
    class TextGenerator:  
        @modal.enter()  
        def load_model(self):  
            from transformers import pipeline  
            self.pipe = pipeline("text-generation", model="gpt2", device=0)  
      
        @modal.method()  
        def generate(self, prompt: str) -> str:  
            return self.pipe(prompt, max_length=100)[0]["generated_text"]  
      
    @app.local_entrypoint()  
    def main():  
        print(TextGenerator().generate.remote("Hello, world"))  
    
[/code]
## Core concepts[​](<#core-concepts> "Прямая ссылка на Core concepts")
### Key components[​](<#key-components> "Прямая ссылка на Key components")
Компонент| Назначение  
---|---  
`App`| Контейнер для функций и ресурсов  
`Function`| Serverless функция с характеристиками вычислений  
`Cls`| Классовые функции с хуками жизненного цикла  
`Image`| Определение контейнерного образа  
`Volume`| Постоянное хранилище для моделей/данных  
`Secret`| Безопасное хранение учётных данных  
### Execution modes[​](<#execution-modes> "Прямая ссылка на Execution modes")
Команда| Описание  
---|---  
`modal run script.py`| Выполнить и завершить  
`modal serve script.py`| Разработка с живой перезагрузкой  
`modal deploy script.py`| Постоянное облачное развёртывание  
## GPU configuration[​](<#gpu-configuration> "Прямая ссылка на GPU configuration")
### Available GPUs[​](<#available-gpus> "Прямая ссылка на Available GPUs")
GPU| VRAM| Лучше всего подходит для  
---|---|---  
`T4`| 16GB| Бюджетный инференс, маленькие модели  
`L4`| 24GB| Инференс, архитектура Ada Lovelace  
`A10G`| 24GB| Обучение/инференс, в 3.3x быстрее T4  
`L40S`| 48GB| Рекомендуется для инференса (лучшее соотношение цена/производительность)  
`A100-40GB`| 40GB| Обучение больших моделей  
`A100-80GB`| 80GB| Очень большие модели  
`H100`| 80GB| Самый быстрый, FP8 + Transformer Engine  
`H200`| 141GB| Авто-обновление с H100, пропускная способность 4.8TB/s  
`B200`| Lastest| Архитектура Blackwell  
### GPU specification patterns[​](<#gpu-specification-patterns> "Прямая ссылка на GPU specification patterns")
[code] 
    # Single GPU  
    @app.function(gpu="A100")  
      
    # Specific memory variant  
    @app.function(gpu="A100-80GB")  
      
    # Multiple GPUs (up to 8)  
    @app.function(gpu="H100:4")  
      
    # GPU with fallbacks  
    @app.function(gpu=["H100", "A100", "L40S"])  
      
    # Any available GPU  
    @app.function(gpu="any")  
    
[/code]
## Container images[​](<#container-images> "Прямая ссылка на Container images")
[code] 
    # Basic image with pip  
    image = modal.Image.debian_slim(python_version="3.11").pip_install(  
        "torch==2.1.0", "transformers==4.36.0", "accelerate"  
    )  
      
    # From CUDA base  
    image = modal.Image.from_registry(  
        "nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04",  
        add_python="3.11"  
    ).pip_install("torch", "transformers")  
      
    # With system packages  
    image = modal.Image.debian_slim().apt_install("git", "ffmpeg").pip_install("whisper")  
    
[/code]
## Persistent storage[​](<#persistent-storage> "Прямая ссылка на Persistent storage")
[code] 
    volume = modal.Volume.from_name("model-cache", create_if_missing=True)  
      
    @app.function(gpu="A10G", volumes={"/models": volume})  
    def load_model():  
        import os  
        model_path = "/models/llama-7b"  
        if not os.path.exists(model_path):  
            model = download_model()  
            model.save_pretrained(model_path)  
            volume.commit()  # Persist changes  
        return load_from_path(model_path)  
    
[/code]
## Web endpoints[​](<#web-endpoints> "Прямая ссылка на Web endpoints")
### FastAPI endpoint decorator[​](<#fastapi-endpoint-decorator> "Прямая ссылка на FastAPI endpoint decorator")
[code] 
    @app.function()  
    @modal.fastapi_endpoint(method="POST")  
    def predict(text: str) -> dict:  
        return {"result": model.predict(text)}  
    
[/code]
### Full ASGI app[​](<#full-asgi-app> "Прямая ссылка на Full ASGI app")
[code] 
    from fastapi import FastAPI  
    web_app = FastAPI()  
      
    @web_app.post("/predict")  
    async def predict(text: str):  
        return {"result": await model.predict.remote.aio(text)}  
      
    @app.function()  
    @modal.asgi_app()  
    def fastapi_app():  
        return web_app  
    
[/code]
### Web endpoint types[​](<#web-endpoint-types> "Прямая ссылка на Web endpoint types")
Декоратор| Сценарий использования  
---|---  
`@modal.fastapi_endpoint()`| Простая функция → API  
`@modal.asgi_app()`| Полноценные FastAPI/Starlette приложения  
`@modal.wsgi_app()`| Django/Flask приложения  
`@modal.web_server(port)`| Произвольные HTTP-серверы  
## Dynamic batching[​](<#dynamic-batching> "Прямая ссылка на Dynamic batching")
[code] 
    @app.function()  
    @modal.batched(max_batch_size=32, wait_ms=100)  
    async def batch_predict(inputs: list[str]) -> list[dict]:  
        # Inputs automatically batched  
        return model.batch_predict(inputs)  
    
[/code]
## Secrets management[​](<#secrets-management> "Прямая ссылка на Secrets management")
[code] 
    # Create secret  
    modal secret create huggingface HF_TOKEN=hf_xxx  
    
[/code]
[code] 
    @app.function(secrets=[modal.Secret.from_name("huggingface")])  
    def download_model():  
        import os  
        token = os.environ["HF_TOKEN"]  
    
[/code]
## Scheduling[​](<#scheduling> "Прямая ссылка на Scheduling")
[code] 
    @app.function(schedule=modal.Cron("0 0 * * *"))  # Daily midnight  
    def daily_job():  
        pass  
      
    @app.function(schedule=modal.Period(hours=1))  
    def hourly_job():  
        pass  
    
[/code]
## Performance optimization[​](<#performance-optimization> "Прямая ссылка на Performance optimization")
### Cold start mitigation[​](<#cold-start-mitigation> "Прямая ссылка на Cold start mitigation")
[code] 
    @app.function(  
        container_idle_timeout=300,  # Keep warm 5 min  
        allow_concurrent_inputs=10,  # Handle concurrent requests  
    )  
    def inference():  
        pass  
    
[/code]
### Model loading best practices[​](<#model-loading-best-practices> "Прямая ссылка на Model loading best practices")
[code] 
    @app.cls(gpu="A100")  
    class Model:  
        @modal.enter()  # Run once at container start  
        def load(self):  
            self.model = load_model()  # Load during warm-up  
      
        @modal.method()  
        def predict(self, x):  
            return self.model(x)  
    
[/code]
## Parallel processing[​](<#parallel-processing> "Прямая ссылка на Parallel processing")
[code] 
    @app.function()  
    def process_item(item):  
        return expensive_computation(item)  
      
    @app.function()  
    def run_parallel():  
        items = list(range(1000))  
        # Fan out to parallel containers  
        results = list(process_item.map(items))  
        return results  
    
[/code]
## Common configuration[​](<#common-configuration> "Прямая ссылка на Common configuration")
[code] 
    @app.function(  
        gpu="A100",  
        memory=32768,              # 32GB RAM  
        cpu=4,                     # 4 CPU cores  
        timeout=3600,              # 1 hour max  
        container_idle_timeout=120,# Keep warm 2 min  
        retries=3,                 # Retry on failure  
        concurrency_limit=10,      # Max concurrent containers  
    )  
    def my_function():  
        pass  
    
[/code]
## Debugging[​](<#debugging> "Прямая ссылка на Debugging")
[code] 
    # Test locally  
    if __name__ == "__main__":  
        result = my_function.local()  
      
    # View logs  
    # modal app logs my-app  
    
[/code]
## Common issues[​](<#common-issues> "Прямая ссылка на Common issues")
Проблема| Решение  
---|---  
Задержка холодного старта| Увеличьте `container_idle_timeout`, используйте `@modal.enter()`  
GPU OOM| Используйте GPU побольше (`A100-80GB`), включите gradient checkpointing  
Сборка образа падает| Зафиксируйте версии зависимостей, проверьте совместимость CUDA  
Таймауты| Увеличьте `timeout`, добавьте checkpointing  
## References[​](<#references> "Прямая ссылка на References")
  * **[Advanced Usage](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/modal/references/advanced-usage.md>)** \\- Мульти-GPU, распределённое обучение, оптимизация затрат
  * **[Troubleshooting](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/modal/references/troubleshooting.md>)** \\- Частые проблемы и решения


## Resources[​](<#resources> "Прямая ссылка на Resources")
  * **Documentation** : <https://modal.com/docs>
  * **Examples** : <https://github.com/modal-labs/modal-examples>
  * **Pricing** : <https://modal.com/pricing>
  * **Discord** : <https://discord.gg/modal>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use Modal](<#when-to-use-modal>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Hello World with GPU](<#hello-world-with-gpu>)
    * [Basic inference endpoint](<#basic-inference-endpoint>)
  * [Core concepts](<#core-concepts>)
    * [Key components](<#key-components>)
    * [Execution modes](<#execution-modes>)
  * [GPU configuration](<#gpu-configuration>)
    * [Available GPUs](<#available-gpus>)
    * [GPU specification patterns](<#gpu-specification-patterns>)
  * [Container images](<#container-images>)
  * [Persistent storage](<#persistent-storage>)
  * [Web endpoints](<#web-endpoints>)
    * [FastAPI endpoint decorator](<#fastapi-endpoint-decorator>)
    * [Full ASGI app](<#full-asgi-app>)
    * [Web endpoint types](<#web-endpoint-types>)
  * [Dynamic batching](<#dynamic-batching>)
  * [Secrets management](<#secrets-management>)
  * [Scheduling](<#scheduling>)
  * [Performance optimization](<#performance-optimization>)
    * [Cold start mitigation](<#cold-start-mitigation>)
    * [Model loading best practices](<#model-loading-best-practices>)
  * [Parallel processing](<#parallel-processing>)
  * [Common configuration](<#common-configuration>)
  * [Debugging](<#debugging>)
  * [Common issues](<#common-issues>)
  * [References](<#references>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-modal -->
