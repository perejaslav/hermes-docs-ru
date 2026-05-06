На этой странице
Простая оптимизация предпочтений (Simple Preference Optimization) для выравнивания LLM. Альтернатива DPO без референсной модели с лучшей производительностью (+6,4 балла на AlpacaEval 2.0). Не требует референсной модели, эффективнее DPO. Используйте для выравнивания по предпочтениям, когда нужно более простое и быстрое обучение, чем DPO/PPO.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Опционально — установка через `hermes skills install official/mlops/simpo` |
|Путь| `optional-skills/mlops/simpo` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `torch`, `transformers`, `datasets`, `trl`, `accelerate` |
|Теги| `Post-Training`, `SimPO`, `Preference Optimization`, `Alignment`, `DPO Alternative`, `Reference-Free`, `LLM Alignment`, `Efficient Training` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# SimPO — Простая оптимизация предпочтений
## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
SimPO — это метод оптимизации предпочтений без референсной модели, который превосходит DPO без необходимости в референсной модели.
**Установка**:
[code] 
    # Create environment  
    conda create -n simpo python=3.10 && conda activate simpo  
      
    # Install PyTorch 2.2.2  
    # Visit: https://pytorch.org/get-started/locally/  
      
    # Install alignment-handbook  
    git clone https://github.com/huggingface/alignment-handbook.git  
    cd alignment-handbook  
    python -m pip install .  
      
    # Install Flash Attention 2  
    python -m pip install flash-attn --no-build-isolation  
    
[/code]
**Обучение** (Mistral 7B):
[code] 
    ACCELERATE_LOG_LEVEL=info accelerate launch \  
      --config_file accelerate_configs/deepspeed_zero3.yaml \  
      scripts/run_simpo.py \  
      training_configs/mistral-7b-base-simpo.yaml  
    
[/code]
## Типовые сценарии[​](<#common-workflows> "Прямая ссылка на Типовые сценарии")
### Сценарий 1: Обучение с базовой модели (Mistral 7B)[​](<#workflow-1-train-from-base-model-mistral-7b> "Прямая ссылка на Сценарий 1: Обучение с базовой модели \\(Mistral 7B\\)")
**Конфиг** (`mistral-7b-base-simpo.yaml`):
[code] 
    # Model  
    model_name_or_path: mistralai/Mistral-7B-v0.1  
    torch_dtype: bfloat16  
      
    # Dataset  
    dataset_mixer:  
      HuggingFaceH4/ultrafeedback_binarized: 1.0  
    dataset_splits:  
      - train_prefs  
      - test_prefs  
      
    # SimPO hyperparameters  
    beta: 2.0                  # Масштабирование награды (2.0-10.0)  
    gamma_beta_ratio: 0.5       # Целевой отступ (0-1)  
    loss_type: sigmoid          # sigmoid или hinge  
    sft_weight: 0.0             # Опциональная SFT-регуляризация  
      
    # Training  
    learning_rate: 5e-7         # Критично: 3e-7 до 1e-6  
    num_train_epochs: 1  
    per_device_train_batch_size: 1  
    gradient_accumulation_steps: 8  
      
    # Output  
    output_dir: ./outputs/mistral-7b-simpo  
    
[/code]
**Запуск обучения**:
[code] 
    accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \  
      scripts/run_simpo.py training_configs/mistral-7b-base-simpo.yaml  
    
[/code]
### Сценарий 2: Донастройка instruct-модели (Llama 3 8B)[​](<#workflow-2-fine-tune-instruct-model-llama-3-8b> "Прямая ссылка на Сценарий 2: Донастройка instruct-модели \\(Llama 3 8B\\)")
**Конфиг** (`llama3-8b-instruct-simpo.yaml`):
[code] 
    model_name_or_path: meta-llama/Meta-Llama-3-8B-Instruct  
      
    dataset_mixer:  
      argilla/ultrafeedback-binarized-preferences-cleaned: 1.0  
      
    beta: 2.5  
    gamma_beta_ratio: 0.5  
    learning_rate: 5e-7  
    sft_weight: 0.1             # Добавить SFT-лосс для сохранения способностей  
      
    num_train_epochs: 1  
    per_device_train_batch_size: 2  
    gradient_accumulation_steps: 4  
    output_dir: ./outputs/llama3-8b-simpo  
    
[/code]
**Запуск**:
[code] 
    accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \  
      scripts/run_simpo.py training_configs/llama3-8b-instruct-simpo.yaml  
    
[/code]
### Сценарий 3: Задачи, требующие рассуждений (низкая скорость обучения)[​](<#workflow-3-reasoning-intensive-tasks-lower-lr> "Прямая ссылка на Сценарий 3: Задачи, требующие рассуждений \\(низкая скорость обучения\\)")
**Для задач по математике/программированию**:
[code] 
    model_name_or_path: deepseek-ai/deepseek-math-7b-base  
      
    dataset_mixer:  
      argilla/distilabel-math-preference-dpo: 1.0  
      
    beta: 5.0                   # Выше для более сильного сигнала  
    gamma_beta_ratio: 0.7       # Больший отступ  
    learning_rate: 3e-7         # Меньше скорость обучения для рассуждений  
    sft_weight: 0.0  
      
    num_train_epochs: 1  
    per_device_train_batch_size: 1  
    gradient_accumulation_steps: 16  
    
[/code]
## Когда использовать vs альтернативы[​](<#when-to-use-vs-alternatives> "Прямая ссылка на Когда использовать vs альтернативы")
**Используйте SimPO когда**:
  * Нужно более простое обучение, чем DPO (без референсной модели)
  * Есть данные с предпочтениями (выбранные/отклонённые пары)
  * Нужна более высокая производительность, чем DPO
  * Ограниченные вычислительные ресурсы
  * Достаточно обучения на одном узле


**Выбор алгоритма**:
  * **SimPO**: Самый простой, лучшая производительность, без референсной модели
  * **DPO**: Нужен базовый уровень референсной модели, более консервативный
  * **PPO**: Максимальный контроль, нужна модель награды, сложная настройка
  * **GRPO**: Энергоэффективное RL, без критика


**Используйте альтернативы**:
  * **OpenRLHF**: Многоузловое распределённое обучение, PPO/GRPO
  * **TRL**: Нужно несколько методов в одном фреймворке
  * **DPO**: Устоявшийся базовый уровень для сравнения


## Частые проблемы[​](<#common-issues> "Прямая ссылка на Частые проблемы")
**Проблема: Расходимость функции потерь**
Уменьшите скорость обучения:
[code] 
    learning_rate: 3e-7  # Уменьшить с 5e-7  
    
[/code]
Уменьшите beta:
[code] 
    beta: 1.0  # Уменьшить с 2.0  
    
[/code]
**Проблема: Модель забывает способности**
Добавьте SFT-регуляризацию:
[code] 
    sft_weight: 0.1  # Добавить компонент SFT-лосса  
    
[/code]
**Проблема: Плохое разделение предпочтений**
Увеличьте beta и отступ:
[code] 
    beta: 5.0            # Увеличить с 2.0  
    gamma_beta_ratio: 0.8  # Увеличить с 0.5  
    
[/code]
**Проблема: OOM во время обучения**
Уменьшите размер батча:
[code] 
    per_device_train_batch_size: 1  
    gradient_accumulation_steps: 16  # Сохранить эффективный батч  
    
[/code]
Включите градиентную контрольную точку (gradient checkpointing):
[code] 
    gradient_checkpointing: true  
    
[/code]
## Продвинутые темы[​](<#advanced-topics> "Прямая ссылка на Продвинутые темы")
**Функции потерь**: См. [references/loss-functions.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/simpo/references/loss-functions.md>) для информации о sigmoid vs hinge loss, математических формулировках и о том, когда что использовать.
**Настройка гиперпараметров**: См. [references/hyperparameters.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/simpo/references/hyperparameters.md>) для руководства по выбору beta, gamma, скорости обучения и рекомендаций для разных размеров моделей.
**Подготовка датасета**: См. [references/datasets.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/simpo/references/datasets.md>) для форматов данных предпочтений, фильтрации качества и создания собственных датасетов.
## Требования к оборудованию[​](<#hardware-requirements> "Прямая ссылка на Требования к оборудованию")
  * **GPU**: Рекомендуется NVIDIA A100/H100
  * **VRAM**:
    * Модель 7B: 1× A100 40GB (DeepSpeed ZeRO-3)
    * Модель 8B: 2× A100 40GB
    * Модель 70B: 8× A100 80GB
  * **Один узел**: DeepSpeed ZeRO-3 достаточно
  * **Смешанная точность**: Рекомендуется BF16


**Оптимизация памяти**:
  * DeepSpeed ZeRO-3 (конфиг по умолчанию)
  * Градиентная контрольная точка (Gradient checkpointing)
  * Flash Attention 2


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * Статья: <https://arxiv.org/abs/2405.14734> (NeurIPS 2024)
  * GitHub: <https://github.com/princeton-nlp/SimPO>
  * Модели: <https://huggingface.co/princeton-nlp>
  * Alignment Handbook: <https://github.com/huggingface/alignment-handbook>


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Быстрый старт](<#quick-start>)
  * [Типовые сценарии](<#common-workflows>)
    * [Сценарий 1: Обучение с базовой модели (Mistral 7B)](<#workflow-1-train-from-base-model-mistral-7b>)
    * [Сценарий 2: Донастройка instruct-модели (Llama 3 8B)](<#workflow-2-fine-tune-instruct-model-llama-3-8b>)
    * [Сценарий 3: Задачи, требующие рассуждений (низкая скорость обучения)](<#workflow-3-reasoning-intensive-tasks-lower-lr>)
  * [Когда использовать vs альтернативы](<#when-to-use-vs-alternatives>)
  * [Частые проблемы](<#common-issues>)
  * [Продвинутые темы](<#advanced-topics>)
  * [Требования к оборудованию](<#hardware-requirements>)
  * [Ресурсы](<#resources>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-simpo -->
