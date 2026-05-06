На этой странице
Параметро-эффективный тонкий тюнинг (Parameter-efficient fine-tuning) для LLM с использованием LoRA, QLoRA и 25+ методов. Используйте, когда требуется дообучать большие модели (7B-70B) при ограниченной памяти GPU, когда нужно тренировать <1% параметров с минимальной потерей качества, или для мульти-адаптерного обслуживания. Официальная библиотека HuggingFace, интегрированная с экосистемой transformers.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   | 
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/mlops/peft`|
|Путь| `optional-skills/mlops/peft`|
|Версия| `1.0.0`|
|Автор| Orchestra Research|
|Лицензия| MIT|
|Зависимости| `peft>=0.13.0`, `transformers>=4.45.0`, `torch>=2.0.0`, `bitsandbytes>=0.43.0`|
|Теги| `Fine-Tuning`, `PEFT`, `LoRA`, `QLoRA`, `Parameter-Efficient`, `Adapters`, `Low-Rank`, `Memory Optimization`, `Multi-Adapter`|
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.
# PEFT (Parameter-Efficient Fine-Tuning)
Дообучайте LLM, тренируя <1% параметров с помощью LoRA, QLoRA и 25+ методов адаптеров.
## Когда использовать PEFT[​](<#when-to-use-peft> "Прямая ссылка на Когда использовать PEFT")
**Используйте PEFT/LoRA когда:**
  * Дообучаете модели 7B-70B на потребительских GPU (RTX 4090, A100)
  * Нужно тренировать <1% параметров (адаптеры 6MB против 14GB полной модели)
  * Хотите быструю итерацию с несколькими адаптерами под разные задачи
  * Развёртываете несколько дообученных вариантов из одной базовой модели


**Используйте QLoRA (PEFT + квантизация) когда:**
  * Дообучаете модели 70B на одной 24GB GPU
  * Память является основным ограничением
  * Можете принять ~5% компромисс по качеству относительно полного дообучения


**Используйте полное дообучение когда:**
  * Тренируете маленькие модели (<1B параметров)
  * Нужно максимальное качество и есть бюджет на вычисления
  * Значительный сдвиг домена требует обновления всех весов


## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Basic installation  
    pip install peft  
      
    # With quantization support (recommended)  
    pip install peft bitsandbytes  
      
    # Full stack  
    pip install peft transformers accelerate bitsandbytes datasets  
    
[/code]
### LoRA дообучение (стандартное)[​](<#lora-fine-tuning-standard> "Прямая ссылка на LoRA дообучение (стандартное)")
[code] 
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer  
    from peft import get_peft_model, LoraConfig, TaskType  
    from datasets import load_dataset  
      
    # Load base model  
    model_name = "meta-llama/Llama-3.1-8B"  
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")  
    tokenizer = AutoTokenizer.from_pretrained(model_name)  
    tokenizer.pad_token = tokenizer.eos_token  
      
    # LoRA configuration  
    lora_config = LoraConfig(  
        task_type=TaskType.CAUSAL_LM,  
        r=16,                          # Rank (8-64, higher = more capacity)  
        lora_alpha=32,                 # Scaling factor (typically 2*r)  
        lora_dropout=0.05,             # Dropout for regularization  
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Attention layers  
        bias="none"                    # Don't train biases  
    )  
      
    # Apply LoRA  
    model = get_peft_model(model, lora_config)  
    model.print_trainable_parameters()  
    # Output: trainable params: 13,631,488 || all params: 8,043,307,008 || trainable%: 0.17%  
      
    # Prepare dataset  
    dataset = load_dataset("databricks/databricks-dolly-15k", split="train")  
      
    def tokenize(example):  
        text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"  
        return tokenizer(text, truncation=True, max_length=512, padding="max_length")  
      
    tokenized = dataset.map(tokenize, remove_columns=dataset.column_names)  
      
    # Training  
    training_args = TrainingArguments(  
        output_dir="./lora-llama",  
        num_train_epochs=3,  
        per_device_train_batch_size=4,  
        gradient_accumulation_steps=4,  
        learning_rate=2e-4,  
        fp16=True,  
        logging_steps=10,  
        save_strategy="epoch"  
    )  
      
    trainer = Trainer(  
        model=model,  
        args=training_args,  
        train_dataset=tokenized,  
        data_collator=lambda data: {"input_ids": torch.stack([f["input_ids"] for f in data]),  
                                     "attention_mask": torch.stack([f["attention_mask"] for f in data]),  
                                     "labels": torch.stack([f["input_ids"] for f in data])}  
    )  
      
    trainer.train()  
      
    # Save adapter only (6MB vs 16GB)  
    model.save_pretrained("./lora-llama-adapter")  
    
[/code]
### QLoRA дообучение (память-эффективное)[​](<#qlora-fine-tuning-memory-efficient> "Прямая ссылка на QLoRA дообучение (память-эффективное)")
[code] 
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig  
    from peft import get_peft_model, LoraConfig, prepare_model_for_kbit_training  
      
    # 4-bit quantization config  
    bnb_config = BitsAndBytesConfig(  
        load_in_4bit=True,  
        bnb_4bit_quant_type="nf4",           # NormalFloat4 (best for LLMs)  
        bnb_4bit_compute_dtype="bfloat16",   # Compute in bf16  
        bnb_4bit_use_double_quant=True       # Nested quantization  
    )  
      
    # Load quantized model  
    model = AutoModelForCausalLM.from_pretrained(  
        "meta-llama/Llama-3.1-70B",  
        quantization_config=bnb_config,  
        device_map="auto"  
    )  
      
    # Prepare for training (enables gradient checkpointing)  
    model = prepare_model_for_kbit_training(model)  
      
    # LoRA config for QLoRA  
    lora_config = LoraConfig(  
        r=64,                              # Higher rank for 70B  
        lora_alpha=128,  
        lora_dropout=0.1,  
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],  
        bias="none",  
        task_type="CAUSAL_LM"  
    )  
      
    model = get_peft_model(model, lora_config)  
    # 70B model now fits on single 24GB GPU!  
    
[/code]
## Выбор параметров LoRA[​](<#lora-parameter-selection> "Прямая ссылка на Выбор параметров LoRA")
### Ранг (r) — ёмкость против эффективности[​](<#rank-r---capacity-vs-efficiency> "Прямая ссылка на Ранг (r) — ёмкость против эффективности")
Ранг| Обучаемые параметры| Память| Качество| Сценарий использования  
|---|---|---|---|---  
4| ~3M| Минимально| Ниже| Простые задачи, прототипирование  
**8**|  ~7M| Низко| Хорошо| **Рекомендуемая отправная точка**  
**16**|  ~14M| Средне| Лучше| **Общее дообучение**  
32| ~27M| Выше| Высоко| Сложные задачи  
64| ~54M| Высоко| Наивысшее| Адаптация домена, модели 70B  
### Alpha (lora_alpha) — коэффициент масштабирования[​](<#alpha-lora_alpha---scaling-factor> "Прямая ссылка на Alpha (lora_alpha) — коэффициент масштабирования")
[code] 
    # Rule of thumb: alpha = 2 * rank  
    LoraConfig(r=16, lora_alpha=32)  # Standard  
    LoraConfig(r=16, lora_alpha=16)  # Conservative (lower learning rate effect)  
    LoraConfig(r=16, lora_alpha=64)  # Aggressive (higher learning rate effect)  
    
[/code]
### Целевые модули по архитектуре[​](<#target-modules-by-architecture> "Прямая ссылка на Целевые модули по архитектуре")
[code] 
    # Llama / Mistral / Qwen  
    target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]  
      
    # GPT-2 / GPT-Neo  
    target_modules = ["c_attn", "c_proj", "c_fc"]  
      
    # Falcon  
    target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]  
      
    # BLOOM  
    target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]  
      
    # Auto-detect all linear layers  
    target_modules = "all-linear"  # PEFT 0.6.0+  
    
[/code]
## Загрузка и слияние адаптеров[​](<#loading-and-merging-adapters> "Прямая ссылка на Загрузка и слияние адаптеров")
### Загрузить обученный адаптер[​](<#load-trained-adapter> "Прямая ссылка на Загрузить обученный адаптер")
[code] 
    from peft import PeftModel, AutoPeftModelForCausalLM  
    from transformers import AutoModelForCausalLM  
      
    # Option 1: Load with PeftModel  
    base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")  
    model = PeftModel.from_pretrained(base_model, "./lora-llama-adapter")  
      
    # Option 2: Load directly (recommended)  
    model = AutoPeftModelForCausalLM.from_pretrained(  
        "./lora-llama-adapter",  
        device_map="auto"  
    )  
    
[/code]
### Слияние адаптера с базовой моделью[​](<#merge-adapter-into-base-model> "Прямая ссылка на Слияние адаптера с базовой моделью")
[code] 
    # Merge for deployment (no adapter overhead)  
    merged_model = model.merge_and_unload()  
      
    # Save merged model  
    merged_model.save_pretrained("./llama-merged")  
    tokenizer.save_pretrained("./llama-merged")  
      
    # Push to Hub  
    merged_model.push_to_hub("username/llama-finetuned")  
    
[/code]
### Мульти-адаптерное обслуживание[​](<#multi-adapter-serving> "Прямая ссылка на Мульти-адаптерное обслуживание")
[code] 
    from peft import PeftModel  
      
    # Load base with first adapter  
    model = AutoPeftModelForCausalLM.from_pretrained("./adapter-task1")  
      
    # Load additional adapters  
    model.load_adapter("./adapter-task2", adapter_name="task2")  
    model.load_adapter("./adapter-task3", adapter_name="task3")  
      
    # Switch between adapters at runtime  
    model.set_adapter("task1")  # Use task1 adapter  
    output1 = model.generate(**inputs)  
      
    model.set_adapter("task2")  # Switch to task2  
    output2 = model.generate(**inputs)  
      
    # Disable adapters (use base model)  
    with model.disable_adapter():  
        base_output = model.generate(**inputs)  
    
[/code]
## Сравнение методов PEFT[​](<#peft-methods-comparison> "Прямая ссылка на Сравнение методов PEFT")
Метод| Обучаемые %| Память| Скорость| Лучше всего для  
|---|---|---|---|---  
**LoRA**|  0.1-1%| Низкая| Быстро| Общее дообучение  
**QLoRA**|  0.1-1%| Очень низкая| Средне| Ограниченная память  
AdaLoRA| 0.1-1%| Низкая| Средне| Автоматический выбор ранга  
IA3| 0.01%| Минимальная| Быстрейший| Few-shot адаптация  
Prefix Tuning| 0.1%| Низкая| Средне| Управление генерацией  
Prompt Tuning| 0.001%| Минимальная| Быстро| Простая адаптация задач  
P-Tuning v2| 0.1%| Низкая| Средне| NLU задачи  
### IA3 (минимальные параметры)[​](<#ia3-minimal-parameters> "Прямая ссылка на IA3 (минимальные параметры)")
[code] 
    from peft import IA3Config  
      
    ia3_config = IA3Config(  
        target_modules=["q_proj", "v_proj", "k_proj", "down_proj"],  
        feedforward_modules=["down_proj"]  
    )  
    model = get_peft_model(model, ia3_config)  
    # Trains only 0.01% of parameters!  
    
[/code]
### Prefix Tuning[​](<#prefix-tuning> "Прямая ссылка на Prefix Tuning")
[code] 
    from peft import PrefixTuningConfig  
      
    prefix_config = PrefixTuningConfig(  
        task_type="CAUSAL_LM",  
        num_virtual_tokens=20,      # Prepended tokens  
        prefix_projection=True       # Use MLP projection  
    )  
    model = get_peft_model(model, prefix_config)  
    
[/code]
## Паттерны интеграции[​](<#integration-patterns> "Прямая ссылка на Паттерны интеграции")
### С TRL (SFTTrainer)[​](<#with-trl-sfttrainer> "Прямая ссылка на С TRL (SFTTrainer)")
[code] 
    from trl import SFTTrainer, SFTConfig  
    from peft import LoraConfig  
      
    lora_config = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear")  
      
    trainer = SFTTrainer(  
        model=model,  
        args=SFTConfig(output_dir="./output", max_seq_length=512),  
        train_dataset=dataset,  
        peft_config=lora_config,  # Pass LoRA config directly  
    )  
    trainer.train()  
    
[/code]
### С Axolotl (YAML конфиг)[​](<#with-axolotl-yaml-config> "Прямая ссылка на С Axolotl (YAML конфиг)")
[code] 
    # axolotl config.yaml  
    adapter: lora  
    lora_r: 16  
    lora_alpha: 32  
    lora_dropout: 0.05  
    lora_target_modules:  
      - q_proj  
      - v_proj  
      - k_proj  
      - o_proj  
    lora_target_linear: true  # Target all linear layers  
    
[/code]
### С vLLM (инференс)[​](<#with-vllm-inference> "Прямая ссылка на С vLLM (инференс)")
[code] 
    from vllm import LLM  
    from vllm.lora.request import LoRARequest  
      
    # Load base model with LoRA support  
    llm = LLM(model="meta-llama/Llama-3.1-8B", enable_lora=True)  
      
    # Serve with adapter  
    outputs = llm.generate(  
        prompts,  
        lora_request=LoRARequest("adapter1", 1, "./lora-adapter")  
    )  
    
[/code]
## Бенчмарки производительности[​](<#performance-benchmarks> "Прямая ссылка на Бенчмарки производительности")
### Использование памяти (Llama 3.1 8B)[​](<#memory-usage-llama-31-8b> "Прямая ссылка на Использование памяти (Llama 3.1 8B)")
Метод| Память GPU| Обучаемые параметры  
|---|---|---  
Полное дообучение| 60+ GB| 8B (100%)  
LoRA r=16| 18 GB| 14M (0.17%)  
QLoRA r=16| 6 GB| 14M (0.17%)  
IA3| 16 GB| 800K (0.01%)  
### Скорость обучения (A100 80GB)[​](<#training-speed-a100-80gb> "Прямая ссылка на Скорость обучения (A100 80GB)")
Метод| Токенов/сек| vs Полное FT  
|---|---|---  
Полное FT| 2,500| 1x  
LoRA| 3,200| 1.3x  
QLoRA| 2,100| 0.84x  
### Качество (бенчмарк MMLU)[​](<#quality-mmlu-benchmark> "Прямая ссылка на Качество (бенчмарк MMLU)")
Модель| Полное FT| LoRA| QLoRA  
|---|---|---|---  
Llama 2-7B| 45.3| 44.8| 44.1  
Llama 2-13B| 54.8| 54.2| 53.5  
## Частые проблемы[​](<#common-issues> "Прямая ссылка на Частые проблемы")
### CUDA OOM во время обучения[​](<#cuda-oom-during-training> "Прямая ссылка на CUDA OOM во время обучения")
[code] 
    # Solution 1: Enable gradient checkpointing  
    model.gradient_checkpointing_enable()  
      
    # Solution 2: Reduce batch size + increase accumulation  
    TrainingArguments(  
        per_device_train_batch_size=1,  
        gradient_accumulation_steps=16  
    )  
      
    # Solution 3: Use QLoRA  
    from transformers import BitsAndBytesConfig  
    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")  
    
[/code]
### Адаптер не применяется[​](<#adapter-not-applying> "Прямая ссылка на Адаптер не применяется")
[code] 
    # Verify adapter is active  
    print(model.active_adapters)  # Should show adapter name  
      
    # Check trainable parameters  
    model.print_trainable_parameters()  
      
    # Ensure model in training mode  
    model.train()  
    
[/code]
### Ухудшение качества[​](<#quality-degradation> "Прямая ссылка на Ухудшение качества")
[code] 
    # Increase rank  
    LoraConfig(r=32, lora_alpha=64)  
      
    # Target more modules  
    target_modules = "all-linear"  
      
    # Use more training data and epochs  
    TrainingArguments(num_train_epochs=5)  
      
    # Lower learning rate  
    TrainingArguments(learning_rate=1e-4)  
    
[/code]
## Лучшие практики[​](<#best-practices> "Прямая ссылка на Лучшие практики")
  1. **Начинайте с r=8-16**, увеличивайте, если качество недостаточно
  2. **Используйте alpha = 2 * rank** как отправную точку
  3. **Нацеливайтесь на слои attention + MLP** для лучшего соотношения качества/эффективности
  4. **Включите gradient checkpointing** для экономии памяти
  5. **Сохраняйте адаптеры часто** (маленькие файлы, лёгкий откат)
  6. **Тестируйте на отложенных данных** перед слиянием
  7. **Используйте QLoRA для моделей 70B+** на потребительском оборудовании


## Ссылки[​](<#references> "Прямая ссылка на Ссылки")
  * **[Расширенное использование](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/peft/references/advanced-usage.md>)** \\- DoRA, LoftQ, стабилизация ранга, пользовательские модули
  * **[Устранение неполадок](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/peft/references/troubleshooting.md>)** \\- Частые ошибки, отладка, оптимизация


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **GitHub** : <https://github.com/huggingface/peft>
  * **Документация** : <https://huggingface.co/docs/peft>
  * **Статья LoRA** : arXiv:2106.09685
  * **Статья QLoRA** : arXiv:2305.14314
  * **Модели** : <https://huggingface.co/models?library=peft>


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать PEFT](<#when-to-use-peft>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [LoRA дообучение (стандартное)](<#lora-fine-tuning-standard>)
    * [QLoRA дообучение (память-эффективное)](<#qlora-fine-tuning-memory-efficient>)
  * [Выбор параметров LoRA](<#lora-parameter-selection>)
    * [Ранг (r) — ёмкость против эффективности](<#rank-r---capacity-vs-efficiency>)
    * [Alpha (lora_alpha) — коэффициент масштабирования](<#alpha-lora_alpha---scaling-factor>)
    * [Целевые модули по архитектуре](<#target-modules-by-architecture>)
  * [Загрузка и слияние адаптеров](<#loading-and-merging-adapters>)
    * [Загрузить обученный адаптер](<#load-trained-adapter>)
    * [Слияние адаптера с базовой моделью](<#merge-adapter-into-base-model>)
    * [Мульти-адаптерное обслуживание](<#multi-adapter-serving>)
  * [Сравнение методов PEFT](<#peft-methods-comparison>)
    * [IA3 (минимальные параметры)](<#ia3-minimal-parameters>)
    * [Prefix Tuning](<#prefix-tuning>)
  * [Паттерны интеграции](<#integration-patterns>)
    * [С TRL (SFTTrainer)](<#with-trl-sfttrainer>)
    * [С Axolotl (YAML конфиг)](<#with-axolotl-yaml-config>)
    * [С vLLM (инференс)](<#with-vllm-inference>)
  * [Бенчмарки производительности](<#performance-benchmarks>)
    * [Использование памяти (Llama 3.1 8B)](<#memory-usage-llama-31-8b>)
    * [Скорость обучения (A100 80GB)](<#training-speed-a100-80gb>)
    * [Качество (бенчмарк MMLU)](<#quality-mmlu-benchmark>)
  * [Частые проблемы](<#common-issues>)
    * [CUDA OOM во время обучения](<#cuda-oom-during-training>)
    * [Адаптер не применяется](<#adapter-not-applying>)
    * [Ухудшение качества](<#quality-degradation>)
  * [Лучшие практики](<#best-practices>)
  * [Ссылки](<#references>)
  * [Ресурсы](<#resources>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-peft -->
