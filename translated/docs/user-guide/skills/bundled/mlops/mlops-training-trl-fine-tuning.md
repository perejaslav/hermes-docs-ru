На этой странице

TRL: SFT, DPO, PPO, GRPO, модели вознаграждения для RLHF LLM.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
| Источник | Встроенный (установлен по умолчанию) |
| Путь | `skills/mlops/training/trl-fine-tuning` |
| Версия | `1.0.0` |
| Автор | Orchestra Research |
| Лицензия | MIT |
| Зависимости | `trl`, `transformers`, `datasets`, `peft`, `accelerate`, `torch` |
| Теги | `Post-Training`, `TRL`, `Reinforcement Learning`, `Fine-Tuning`, `SFT`, `DPO`, `PPO`, `GRPO`, `RLHF`, `Preference Alignment`, `HuggingFace` |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое загружает Hermes при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# TRL - Transformer Reinforcement Learning

## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")

TRL предоставляет методы пост-обучения для согласования языковых моделей с человеческими предпочтениями.

**Установка**:

[code]
    pip install trl transformers datasets peft accelerate

[/code]

**Supervised Fine-Tuning** (настройка на инструкции):

[code]
    from trl import SFTTrainer
    
    trainer = SFTTrainer(
        model="Qwen/Qwen2.5-0.5B",
        train_dataset=dataset,  # Пары промпт-ответ
    )
    trainer.train()

[/code]

**DPO** (согласование с предпочтениями):

[code]
    from trl import DPOTrainer, DPOConfig
    
    config = DPOConfig(output_dir="model-dpo", beta=0.1)
    trainer = DPOTrainer(
        model=model,
        args=config,
        train_dataset=preference_dataset,  # Пары chosen/rejected
        processing_class=tokenizer
    )
    trainer.train()

[/code]

## Типовые рабочие процессы[​](<#common-workflows> "Прямая ссылка на Типовые рабочие процессы")

### Рабочий процесс 1: Полный конвейер RLHF (SFT → Модель вознаграждения → PPO)[​](<#workflow-1-full-rlhf-pipeline-sft--reward-model--ppo> "Прямая ссылка на Рабочий процесс 1: Полный конвейер RLHF (SFT → Модель вознаграждения → PPO)")

Полный конвейер от базовой модели до согласованной с человеком модели.
Скопируйте этот чек-лист:

[code]
    RLHF Training:
    - [ ] Шаг 1: Supervised fine-tuning (SFT)
    - [ ] Шаг 2: Обучение модели вознаграждения
    - [ ] Шаг 3: PPO — обучение с подкреплением
    - [ ] Шаг 4: Оценка согласованной модели

[/code]

**Шаг 1: Supervised fine-tuning**
Обучение базовой модели на данных следования инструкциям:

[code]
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTTrainer, SFTConfig
    from datasets import load_dataset
    
    # Загрузка модели
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
    
    # Загрузка набора данных инструкций
    dataset = load_dataset("trl-lib/Capybara", split="train")
    
    # Настройка обучения
    training_args = SFTConfig(
        output_dir="Qwen2.5-0.5B-SFT",
        per_device_train_batch_size=4,
        num_train_epochs=1,
        learning_rate=2e-5,
        logging_steps=10,
        save_strategy="epoch"
    )
    
    # Обучение
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer
    )
    trainer.train()
    trainer.save_model()

[/code]

**Шаг 2: Обучение модели вознаграждения**
Обучение модели предсказывать человеческие предпочтения:

[code]
    from transformers import AutoModelForSequenceClassification
    from trl import RewardTrainer, RewardConfig
    
    # Загрузка SFT-модели как базы
    model = AutoModelForSequenceClassification.from_pretrained(
        "Qwen2.5-0.5B-SFT",
        num_labels=1  # Один показатель вознаграждения
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen2.5-0.5B-SFT")
    
    # Загрузка данных предпочтений (пары chosen/rejected)
    dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
    
    # Настройка обучения
    training_args = RewardConfig(
        output_dir="Qwen2.5-0.5B-Reward",
        per_device_train_batch_size=2,
        num_train_epochs=1,
        learning_rate=1e-5
    )
    
    # Обучение модели вознаграждения
    trainer = RewardTrainer(
        model=model,
        args=training_args,
        processing_class=tokenizer,
        train_dataset=dataset
    )
    trainer.train()
    trainer.save_model()

[/code]

**Шаг 3: PPO — обучение с подкреплением**
Оптимизация политики с использованием модели вознаграждения:

[code]
    python -m trl.scripts.ppo \
        --model_name_or_path Qwen2.5-0.5B-SFT \
        --reward_model_path Qwen2.5-0.5B-Reward \
        --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \
        --output_dir Qwen2.5-0.5B-PPO \
        --learning_rate 3e-6 \
        --per_device_train_batch_size 64 \
        --total_episodes 10000

[/code]

**Шаг 4: Оценка**

[code]
    from transformers import pipeline
    
    # Загрузка согласованной модели
    generator = pipeline("text-generation", model="Qwen2.5-0.5B-PPO")
    
    # Тест
    prompt = "Объясни квантовые вычисления 10-летнему ребёнку"
    output = generator(prompt, max_length=200)[0]["generated_text"]
    print(output)

[/code]

### Рабочий процесс 2: Простое согласование предпочтений с DPO[​](<#workflow-2-simple-preference-alignment-with-dpo> "Прямая ссылка на Рабочий процесс 2: Простое согласование предпочтений с DPO")

Согласование модели с предпочтениями без модели вознаграждения.
Скопируйте этот чек-лист:

[code]
    DPO Training:
    - [ ] Шаг 1: Подготовка набора данных предпочтений
    - [ ] Шаг 2: Настройка DPO
    - [ ] Шаг 3: Обучение с DPOTrainer
    - [ ] Шаг 4: Оценка согласования

[/code]

**Шаг 1: Подготовка набора данных предпочтений**
Формат набора данных:

[code]
    {
      "prompt": "Какая столица Франции?",
      "chosen": "Столица Франции — Париж.",
      "rejected": "Я не знаю."
    }

[/code]

Загрузка набора данных:

[code]
    from datasets import load_dataset
    
    dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
    # Или загрузите свой
    # dataset = load_dataset("json", data_files="preferences.json")

[/code]

**Шаг 2: Настройка DPO**

[code]
    from trl import DPOConfig
    
    config = DPOConfig(
        output_dir="Qwen2.5-0.5B-DPO",
        per_device_train_batch_size=4,
        num_train_epochs=1,
        learning_rate=5e-7,
        beta=0.1,  # Сила KL-штрафа
        max_prompt_length=512,
        max_length=1024,
        logging_steps=10
    )

[/code]

**Шаг 3: Обучение с DPOTrainer**

[code]
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import DPOTrainer
    
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    
    trainer = DPOTrainer(
        model=model,
        args=config,
        train_dataset=dataset,
        processing_class=tokenizer
    )
    
    trainer.train()
    trainer.save_model()

[/code]

**Альтернатива через CLI**:

[code]
    trl dpo \
        --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
        --dataset_name argilla/Capybara-Preferences \
        --output_dir Qwen2.5-0.5B-DPO \
        --per_device_train_batch_size 4 \
        --learning_rate 5e-7 \
        --beta 0.1

[/code]

### Рабочий процесс 3: Энергоэффективное онлайн-обучение с GRPO[​](<#workflow-3-memory-efficient-online-rl-with-grpo> "Прямая ссылка на Рабочий процесс 3: Энергоэффективное онлайн-обучение с GRPO")

Обучение с подкреплением с минимальным потреблением памяти.

За подробным руководством по GRPO — проектированию функций вознаграждения, критическим аспектам обучения (поведению функции потерь, коллапсу мод, настройке) и продвинутым многоэтапным паттернам — обращайтесь к **[references/grpo-training.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/references/grpo-training.md>)**. Готовый к использованию обучающий скрипт находится в **[templates/basic_grpo_training.py](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/templates/basic_grpo_training.py>)**.

Скопируйте этот чек-лист:

[code]
    GRPO Training:
    - [ ] Шаг 1: Определение функции вознаграждения
    - [ ] Шаг 2: Настройка GRPO
    - [ ] Шаг 3: Обучение с GRPOTrainer

[/code]

**Шаг 1: Определение функции вознаграждения**

[code]
    def reward_function(completions, **kwargs):
        """
        Вычисление вознаграждения для сгенерированных текстов.

        Args:
            completions: Список сгенерированных текстов

        Returns:
            Список оценок вознаграждения (float)
        """
        rewards = []
        for completion in completions:
            # Пример: вознаграждение на основе длины и уникальных слов
            score = len(completion.split())  # Поощрение длинных ответов
            score += len(set(completion.lower().split()))  # Поощрение уникальных слов
            rewards.append(score)
        return rewards

[/code]

Или используйте модель вознаграждения:

[code]
    from transformers import pipeline
    
    reward_model = pipeline("text-classification", model="reward-model-path")
    
    def reward_from_model(completions, prompts, **kwargs):
        # Объединение промпта и ответа
        full_texts = [p + c for p, c in zip(prompts, completions)]
        # Получение оценок вознаграждения
        results = reward_model(full_texts)
        return [r["score"] for r in results]

[/code]

**Шаг 2: Настройка GRPO**

[code]
    from trl import GRPOConfig
    
    config = GRPOConfig(
        output_dir="Qwen2-GRPO",
        per_device_train_batch_size=4,
        num_train_epochs=1,
        learning_rate=1e-5,
        num_generations=4,  # Генерация 4 ответов на каждый промпт
        max_new_tokens=128
    )

[/code]

**Шаг 3: Обучение с GRPOTrainer**

[code]
    from datasets import load_dataset
    from trl import GRPOTrainer
    
    # Загрузка набора данных только с промптами
    dataset = load_dataset("trl-lib/tldr", split="train")
    
    trainer = GRPOTrainer(
        model="Qwen/Qwen2-0.5B-Instruct",
        reward_funcs=reward_function,  # Ваша функция вознаграждения
        args=config,
        train_dataset=dataset
    )
    
    trainer.train()

[/code]

**CLI**:

[code]
    trl grpo \
        --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
        --dataset_name trl-lib/tldr \
        --output_dir Qwen2-GRPO \
        --num_generations 4

[/code]

## Когда использовать vs альтернативы[​](<#when-to-use-vs-alternatives> "Прямая ссылка на Когда использовать vs альтернативы")

**Используйте TRL когда:**

* Нужно согласовать модель с человеческими предпочтениями
* Есть данные предпочтений (пары chosen/rejected)
* Требуется обучение с подкреплением (PPO, GRPO)
* Нужно обучение модели вознаграждения
* Выполняется RLHF (полный конвейер)

**Выбор метода:**

* **SFT**: Есть пары промпт-ответ, требуется базовое следование инструкциям
* **DPO**: Есть предпочтения, нужно простое согласование (модель вознаграждения не требуется)
* **PPO**: Есть модель вознаграждения, нужен максимальный контроль над RL
* **GRPO**: Ограниченная память, требуется онлайн-обучение с подкреплением
* **Модель вознаграждения**: Создание конвейера RLHF, требуется оценка генераций

**Используйте альтернативы вместо:**

* **HuggingFace Trainer**: Базовая донастройка без RL
* **Axolotl**: YAML-конфигурация обучения
* **LitGPT**: Образовательная, минимальная донастройка
* **Unsloth**: Быстрое LoRA-обучение

## Частые проблемы[​](<#common-issues> "Прямая ссылка на Частые проблемы")

**Проблема: OOM во время DPO-обучения**
Уменьшите размер батча и длину последовательности:

[code]
    config = DPOConfig(
        per_device_train_batch_size=1,  # Уменьшить с 4
        max_length=512,  # Уменьшить с 1024
        gradient_accumulation_steps=8  # Сохранение эффективного размера батча
    )

[/code]

Или используйте градиентную контрольную точку:

[code]
    model.gradient_checkpointing_enable()

[/code]

**Проблема: Низкое качество согласования**
Настройте параметр beta:

[code]
    # Выше beta = более консервативно (ближе к эталону)
    config = DPOConfig(beta=0.5)  # По умолчанию 0.1
    
    # Ниже beta = более агрессивное согласование
    config = DPOConfig(beta=0.01)

[/code]

**Проблема: Модель вознаграждения не обучается**
Проверьте тип функции потерь и скорость обучения:

[code]
    config = RewardConfig(
        learning_rate=1e-5,  # Попробуйте другую скорость обучения
        num_train_epochs=3  # Увеличьте длительность обучения
    )

[/code]

Убедитесь, что набор данных предпочтений имеет явных победителей:

[code]
    # Проверка набора данных
    print(dataset[0])
    # Должен быть явно chosen > rejected

[/code]

**Проблема: Нестабильное PPO-обучение**
Настройте коэффициент KL:

[code]
    config = PPOConfig(
        kl_coef=0.1,  # Увеличить с 0.05
        cliprange=0.1  # Уменьшить с 0.2
    )

[/code]

## Продвинутые темы[​](<#advanced-topics> "Прямая ссылка на Продвинутые темы")

**Руководство по SFT-обучению**: См. [references/sft-training.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/references/sft-training.md>) о форматах наборов данных, чат-шаблонах, стратегиях упаковки и многогпу-обучении.

**Варианты DPO**: См. [references/dpo-variants.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/references/dpo-variants.md>) об IPO, cDPO, RPO и других функциях потерь DPO с рекомендуемыми гиперпараметрами.

**Модели вознаграждения**: См. [references/reward-modeling.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/references/reward-modeling.md>) о вознаграждении по результату и процессу, функции потерь Брэдли-Терри и оценке моделей вознаграждения.

**Методы онлайн-RL**: См. [references/online-rl.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/references/online-rl.md>) о PPO, GRPO, RLOO и OnlineDPO с подробными конфигурациями.

**Углублённое изучение GRPO**: См. [references/grpo-training.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/references/grpo-training.md>) для экспертных паттернов GRPO — философия проектирования функций вознаграждения, идеи обучения (почему loss растёт, обнаружение коллапса мод), настройка гиперпараметров, многоэтапное обучение и устранение неполадок. Готовый шаблон в [templates/basic_grpo_training.py](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/training/trl-fine-tuning/templates/basic_grpo_training.py>).

## Требования к оборудованию[​](<#hardware-requirements> "Прямая ссылка на Требования к оборудованию")

* **GPU**: NVIDIA (CUDA обязательна)
* **VRAM**: Зависит от модели и метода
  * SFT 7B: 16 ГБ (с LoRA)
  * DPO 7B: 24 ГБ (хранит эталонную модель)
  * PPO 7B: 40 ГБ (политика + модель вознаграждения)
  * GRPO 7B: 24 ГБ (более эффективно по памяти)
* **Multi-GPU**: Поддерживается через `accelerate`
* **Mixed precision**: Рекомендуется BF16 (A100/H100)

**Оптимизация памяти:**

* Используйте LoRA/QLoRA для всех методов
* Включите градиентную контрольную точку
* Используйте меньшие размеры батча с накоплением градиента

## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")

* Документация: <https://huggingface.co/docs/trl/>
* GitHub: <https://github.com/huggingface/trl>
* Статьи:
  * "Training language models to follow instructions with human feedback" (InstructGPT, 2022)
  * "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (DPO, 2023)
  * "Group Relative Policy Optimization" (GRPO, 2024)
* Примеры: <https://github.com/huggingface/trl/tree/main/examples/scripts>

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Быстрый старт](<#quick-start>)
* [Типовые рабочие процессы](<#common-workflows>)
  * [Рабочий процесс 1: Полный конвейер RLHF (SFT → Модель вознаграждения → PPO)](<#workflow-1-full-rlhf-pipeline-sft--reward-model--ppo>)
  * [Рабочий процесс 2: Простое согласование предпочтений с DPO](<#workflow-2-simple-preference-alignment-with-dpo>)
  * [Рабочий процесс 3: Энергоэффективное онлайн-обучение с GRPO](<#workflow-3-memory-efficient-online-rl-with-grpo>)
* [Когда использовать vs альтернативы](<#when-to-use-vs-alternatives>)
* [Частые проблемы](<#common-issues>)
* [Продвинутые темы](<#advanced-topics>)
* [Требования к оборудованию](<#hardware-requirements>)
* [Ресурсы](<#resources>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-training-trl-fine-tuning -->
