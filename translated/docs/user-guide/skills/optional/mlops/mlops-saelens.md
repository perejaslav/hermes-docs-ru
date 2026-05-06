На этой странице
Содержит руководство по обучению и анализу разреженных автоэнкодеров (SAE) с использованием SAELens для декомпозиции активаций нейронных сетей в интерпретируемые признаки. Используйте, когда требуется обнаруживать интерпретируемые признаки, анализировать суперпозицию или изучать моносемантические представления в языковых моделях.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---  |
|Источник| Опционально — установка: `hermes skills install official/mlops/saelens`  |
|Путь| `optional-skills/mlops/saelens`  |
|Версия| `1.0.0`  |
|Автор| Orchestra Research  |
|Лицензия| MIT  |
|Зависимости| `sae-lens>=6.0.0`, `transformer-lens>=2.0.0`, `torch>=2.0.0`  |
|Теги| `Sparse Autoencoders`, `SAE`, `Mechanistic Interpretability`, `Feature Discovery`, `Superposition`  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# SAELens: Разреженные автоэнкодеры для механистической интерпретируемости
SAELens — основная библиотека для обучения и анализа разреженных автоэнкодеров (SAE) — техники декомпозиции полисемантических активаций нейронных сетей в разреженные, интерпретируемые признаки. Основана на новаторских исследованиях Anthropic по моносемантичности.
**GitHub**: [jbloomAus/SAELens](<https://github.com/jbloomAus/SAELens>) (более 1100 звёзд)
## Проблема: полисемантичность и суперпозиция[​](<#the-problem-polysemanticity--superposition> "Прямая ссылка на Проблема: полисемантичность и суперпозиция")
Отдельные нейроны в нейронных сетях являются **полисемантичными** — они активируются в множестве семантически различных контекстов. Это происходит потому, что модели используют **суперпозицию** для представления большего количества признаков, чем у них есть нейронов, что затрудняет интерпретируемость.
**SAE решают эту проблему** путем декомпозиции плотных активаций в разреженные, моносемантические признаки — обычно лишь небольшое количество признаков активируется для любого входного сигнала, и каждый признак соответствует интерпретируемому концепту.
## Когда использовать SAELens[​](<#when-to-use-saelens> "Прямая ссылка на Когда использовать SAELens")
**Используйте SAELens, когда вам нужно:**
  * Обнаруживать интерпретируемые признаки в активациях модели
  * Понимать, какие концепты изучила модель
  * Изучать суперпозицию и геометрию признаков
  * Выполнять управление на основе признаков или абляцию
  * Анализировать признаки, связанные с безопасностью (обман, предвзятость, вредоносный контент)

**Рассмотрите альтернативы, когда:**
  * Вам нужен базовый анализ активаций → Используйте **TransformerLens** напрямую
  * Вы хотите проводить эксперименты по каузальному вмешательству → Используйте **pyvene** или **TransformerLens**
  * Нужно производственное управление → Рассмотрите прямую инженерию активаций

## Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    pip install sae-lens  
    
[/code]
Требования: Python 3.10+, transformer-lens>=2.0.0
## Основные концепции[​](<#core-concepts> "Прямая ссылка на Основные концепции")
### Что изучают SAE[​](<#what-saes-learn> "Прямая ссылка на Что изучают SAE")
SAE обучаются реконструировать активации модели через разреженное узкое место:
[code] 
    Input Activation → Encoder → Sparse Features → Decoder → Reconstructed Activation  
        (d_model)       ↓        (d_sae >> d_model)    ↓         (d_model)  
                     sparsity                      reconstruction  
                     penalty                          loss  
    
[/code]
**Функция потерь**: `MSE(original, reconstructed) + L1_coefficient × L1(features)`
### Ключевое подтверждение (исследование Anthropic)[​](<#key-validation-anthropic-research> "Прямая ссылка на Ключевое подтверждение (исследование Anthropic)")
В работе «Towards Monosemanticity» эксперты-оценщики обнаружили, что **70% признаков SAE действительно интерпретируемы**. Найденные признаки включают:
  * Последовательности ДНК, юридический язык, HTTP-запросы
  * Текст на иврите, утверждения о питании, синтаксис кода
  * Тональность, именованные сущности, грамматические структуры

## Рабочий процесс 1: Загрузка и анализ предобученных SAE[​](<#workflow-1-loading-and-analyzing-pre-trained-saes> "Прямая ссылка на Рабочий процесс 1: Загрузка и анализ предобученных SAE")
### Пошаговая инструкция[​](<#step-by-step> "Прямая ссылка на Пошаговая инструкция")
[code] 
    from transformer_lens import HookedTransformer  
    from sae_lens import SAE  
      
    # 1. Load model and pre-trained SAE  
    model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")  
    sae, cfg_dict, sparsity = SAE.from_pretrained(  
        release="gpt2-small-res-jb",  
        sae_id="blocks.8.hook_resid_pre",  
        device="cuda"  
    )  
      
    # 2. Get model activations  
    tokens = model.to_tokens("The capital of France is Paris")  
    _, cache = model.run_with_cache(tokens)  
    activations = cache["resid_pre", 8]  # [batch, pos, d_model]  
      
    # 3. Encode to SAE features  
    sae_features = sae.encode(activations)  # [batch, pos, d_sae]  
    print(f"Active features: {(sae_features > 0).sum()}")  
      
    # 4. Find top features for each position  
    for pos in range(tokens.shape[1]):  
        top_features = sae_features[0, pos].topk(5)  
        token = model.to_str_tokens(tokens[0, pos:pos+1])[0]  
        print(f"Token '{token}': features {top_features.indices.tolist()}")  
      
    # 5. Reconstruct activations  
    reconstructed = sae.decode(sae_features)  
    reconstruction_error = (activations - reconstructed).norm()  
    
[/code]
### Доступные предобученные SAE[​](<#available-pre-trained-saes> "Прямая ссылка на Доступные предобученные SAE")
| Релиз | Модель | Слои  |
|---|---|---  |
|`gpt2-small-res-jb`| GPT-2 Small| Несколько остаточных потоков  |
|`gemma-2b-res`| Gemma 2B| Остаточные потоки  |
|Различные на HuggingFace| Тег поиска `saelens`| Различные  |
### Контрольный список[​](<#checklist> "Прямая ссылка на Контрольный список")
  * Загрузите модель с TransformerLens
  * Загрузите соответствующий SAE для целевого слоя
  * Кодируйте активации в разреженные признаки
  * Определите признаки с максимальной активацией для каждого токена
  * Проверьте качество реконструкции

## Рабочий процесс 2: Обучение пользовательского SAE[​](<#workflow-2-training-a-custom-sae> "Прямая ссылка на Рабочий процесс 2: Обучение пользовательского SAE")
### Пошаговая инструкция[​](<#step-by-step-1> "Прямая ссылка на Пошаговая инструкция")
[code] 
    from sae_lens import SAE, LanguageModelSAERunnerConfig, SAETrainingRunner  
      
    # 1. Configure training  
    cfg = LanguageModelSAERunnerConfig(  
        # Model  
        model_name="gpt2-small",  
        hook_name="blocks.8.hook_resid_pre",  
        hook_layer=8,  
        d_in=768,  # Model dimension  
      
        # SAE architecture  
        architecture="standard",  # or "gated", "topk"  
        d_sae=768 * 8,  # Expansion factor of 8  
        activation_fn="relu",  
      
        # Training  
        lr=4e-4,  
        l1_coefficient=8e-5,  # Sparsity penalty  
        l1_warm_up_steps=1000,  
        train_batch_size_tokens=4096,  
        training_tokens=100_000_000,  
      
        # Data  
        dataset_path="monology/pile-uncopyrighted",  
        context_size=128,  
      
        # Logging  
        log_to_wandb=True,  
        wandb_project="sae-training",  
      
        # Checkpointing  
        checkpoint_path="checkpoints",  
        n_checkpoints=5,  
    )  
      
    # 2. Train  
    trainer = SAETrainingRunner(cfg)  
    sae = trainer.run()  
      
    # 3. Evaluate  
    print(f"L0 (avg active features): {trainer.metrics['l0']}")  
    print(f"CE Loss Recovered: {trainer.metrics['ce_loss_score']}")  
    
[/code]
### Ключевые гиперпараметры[​](<#key-hyperparameters> "Прямая ссылка на Ключевые гиперпараметры")
| Параметр | Типичное значение | Эффект  |
|---|---|---  |
|`d_sae`| 4–16× d_model| Больше признаков, выше ёмкость  |
|`l1_coefficient`| 5e-5 до 1e-4| Выше = разреженнее, менее точно  |
|`lr`| 1e-4 до 1e-3| Стандартная скорость обучения  |
|`l1_warm_up_steps`| 500–2000| Предотвращает раннюю гибель признаков  |
### Метрики оценки[​](<#evaluation-metrics> "Прямая ссылка на Метрики оценки")
| Метрика | Цель | Значение  |
|---|---|---  |
|**L0**| 50–200| Среднее количество активных признаков на токен  |
|**CE Loss Score**| 80–95%| Восстановленная кросс-энтропия относительно оригинала  |
|**Dead Features**| <5%| Признаки, которые никогда не активируются  |
|**Explained Variance**| >90%| Качество реконструкции  |
### Контрольный список[​](<#checklist-1> "Прямая ссылка на Контрольный список")
  * Выберите целевой слой и точку подключения
  * Установите коэффициент расширения (d_sae = 4–16× d_model)
  * Настройте L1-коэффициент для желаемой разреженности
  * Включите прогрев L1 для предотвращения гибели признаков
  * Отслеживайте метрики во время обучения (W&B)
  * Проверьте восстановление L0 и CE loss
  * Проверьте долю мёртвых признаков

## Рабочий процесс 3: Анализ признаков и управление[​](<#workflow-3-feature-analysis-and-steering> "Прямая ссылка на Рабочий процесс 3: Анализ признаков и управление")
### Анализ отдельных признаков[​](<#analyzing-individual-features> "Прямая ссылка на Анализ отдельных признаков")
[code] 
    from transformer_lens import HookedTransformer  
    from sae_lens import SAE  
    import torch  
      
    model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")  
    sae, _, _ = SAE.from_pretrained(  
        release="gpt2-small-res-jb",  
        sae_id="blocks.8.hook_resid_pre",  
        device="cuda"  
    )  
      
    # Find what activates a specific feature  
    feature_idx = 1234  
    test_texts = [  
        "The scientist conducted an experiment",  
        "I love chocolate cake",  
        "The code compiles successfully",  
        "Paris is beautiful in spring",  
    ]  
      
    for text in test_texts:  
        tokens = model.to_tokens(text)  
        _, cache = model.run_with_cache(tokens)  
        features = sae.encode(cache["resid_pre", 8])  
        activation = features[0, :, feature_idx].max().item()  
        print(f"{activation:.3f}: {text}")  
    
[/code]
### Управление признаками[​](<#feature-steering> "Прямая ссылка на Управление признаками")
[code] 
    def steer_with_feature(model, sae, prompt, feature_idx, strength=5.0):  
        """Add SAE feature direction to residual stream."""  
        tokens = model.to_tokens(prompt)  
      
        # Get feature direction from decoder  
        feature_direction = sae.W_dec[feature_idx]  # [d_model]  
      
        def steering_hook(activation, hook):  
            # Add scaled feature direction at all positions  
            activation += strength * feature_direction  
            return activation  
      
        # Generate with steering  
        output = model.generate(  
            tokens,  
            max_new_tokens=50,  
            fwd_hooks=[("blocks.8.hook_resid_pre", steering_hook)]  
        )  
        return model.to_string(output[0])  
    
[/code]
### Атрибуция признаков[​](<#feature-attribution> "Прямая ссылка на Атрибуция признаков")
[code] 
    # Which features most affect a specific output?  
    tokens = model.to_tokens("The capital of France is")  
    _, cache = model.run_with_cache(tokens)  
      
    # Get features at final position  
    features = sae.encode(cache["resid_pre", 8])[0, -1]  # [d_sae]  
      
    # Get logit attribution per feature  
    # Feature contribution = feature_activation × decoder_weight × unembedding  
    W_dec = sae.W_dec  # [d_sae, d_model]  
    W_U = model.W_U    # [d_model, vocab]  
      
    # Contribution to "Paris" logit  
    paris_token = model.to_single_token(" Paris")  
    feature_contributions = features * (W_dec @ W_U[:, paris_token])  
      
    top_features = feature_contributions.topk(10)  
    print("Top features for 'Paris' prediction:")  
    for idx, val in zip(top_features.indices, top_features.values):  
        print(f"  Feature {idx.item()}: {val.item():.3f}")  
    
[/code]
## Типичные проблемы и решения[​](<#common-issues--solutions> "Прямая ссылка на Типичные проблемы и решения")
### Проблема: Высокая доля мёртвых признаков[​](<#issue-high-dead-feature-ratio> "Прямая ссылка на Проблема: Высокая доля мёртвых признаков")
[code] 
    # WRONG: No warm-up, features die early  
    cfg = LanguageModelSAERunnerConfig(  
        l1_coefficient=1e-4,  
        l1_warm_up_steps=0,  # Bad!  
    )  
      
    # RIGHT: Warm-up L1 penalty  
    cfg = LanguageModelSAERunnerConfig(  
        l1_coefficient=8e-5,  
        l1_warm_up_steps=1000,  # Gradually increase  
        use_ghost_grads=True,   # Revive dead features  
    )  
    
[/code]
### Проблема: Плохая реконструкция (низкое восстановление CE)[​](<#issue-poor-reconstruction-low-ce-recovery> "Прямая ссылка на Проблема: Плохая реконструкция (низкое восстановление CE)")
[code] 
    # Reduce sparsity penalty  
    cfg = LanguageModelSAERunnerConfig(  
        l1_coefficient=5e-5,  # Lower = better reconstruction  
        d_sae=768 * 16,       # More capacity  
    )  
    
[/code]
### Проблема: Признаки не интерпретируемы[​](<#issue-features-not-interpretable> "Прямая ссылка на Проблема: Признаки не интерпретируемы")
[code] 
    # Increase sparsity (higher L1)  
    cfg = LanguageModelSAERunnerConfig(  
        l1_coefficient=1e-4,  # Higher = sparser, more interpretable  
    )  
    # Or use TopK architecture  
    cfg = LanguageModelSAERunnerConfig(  
        architecture="topk",  
        activation_fn_kwargs={"k": 50},  # Exactly 50 active features  
    )  
    
[/code]
### Проблема: Ошибки памяти во время обучения[​](<#issue-memory-errors-during-training> "Прямая ссылка на Проблема: Ошибки памяти во время обучения")
[code] 
    cfg = LanguageModelSAERunnerConfig(  
        train_batch_size_tokens=2048,  # Reduce batch size  
        store_batch_size_prompts=4,    # Fewer prompts in buffer  
        n_batches_in_buffer=8,         # Smaller activation buffer  
    )  
    
[/code]
## Интеграция с Neuronpedia[​](<#integration-with-neuronpedia> "Прямая ссылка на Интеграция с Neuronpedia")
Просматривайте признаки предобученных SAE на [neuronpedia.org](<https://neuronpedia.org>):
[code] 
    # Features are indexed by SAE ID  
    # Example: gpt2-small layer 8 feature 1234  
    # → neuronpedia.org/gpt2-small/8-res-jb/1234  
    
[/code]
## Справочник ключевых классов[​](<#key-classes-reference> "Прямая ссылка на Справочник ключевых классов")
| Класс | Назначение  |
|---|---  |
|`SAE`| Модель разреженного автоэнкодера  |
|`LanguageModelSAERunnerConfig`| Конфигурация обучения  |
|`SAETrainingRunner`| Менеджер цикла обучения  |
|`ActivationsStore`| Сбор и пакетирование активаций  |
|`HookedSAETransformer`| Интеграция TransformerLens + SAE  |
## Справочная документация[​](<#reference-documentation> "Прямая ссылка на Справочная документация")
Подробную документацию по API, руководства и расширенное использование см. в папке `references/`:
| Файл | Содержание  |
|---|---  |
|[references/README.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/saelens/references/README.md>)| Обзор и краткое руководство  |
|[references/api.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/saelens/references/api.md>)| Полная справка по API для SAE, TrainingSAE, конфигураций  |
|[references/tutorials.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/saelens/references/tutorials.md>)| Пошаговые руководства по обучению, анализу, управлению  |
## Внешние ресурсы[​](<#external-resources> "Прямая ссылка на Внешние ресурсы")
### Руководства[​](<#tutorials> "Прямая ссылка на Руководства")
  * [Базовая загрузка и анализ](<https://github.com/jbloomAus/SAELens/blob/main/tutorials/basic_loading_and_analysing.ipynb>)
  * [Обучение разреженного автоэнкодера](<https://github.com/jbloomAus/SAELens/blob/main/tutorials/training_a_sparse_autoencoder.ipynb>)
  * [Учебная программа ARENA по SAE](<https://www.lesswrong.com/posts/LnHowHgmrMbWtpkxx/intro-to-superposition-and-sparse-autoencoders-colab>)

### Статьи[​](<#papers> "Прямая ссылка на Статьи")
  * [Towards Monosemanticity](<https://transformer-circuits.pub/2023/monosemantic-features>) — Anthropic (2023)
  * [Scaling Monosemanticity](<https://transformer-circuits.pub/2024/scaling-monosemanticity/>) — Anthropic (2024)
  * [Sparse Autoencoders Find Highly Interpretable Features](<https://arxiv.org/abs/2309.08600>) — Cunningham et al. (ICLR 2024)

### Официальная документация[​](<#official-documentation> "Прямая ссылка на Официальная документация")
  * [Документация SAELens](<https://jbloomaus.github.io/SAELens/>)
  * [Neuronpedia](<https://neuronpedia.org>) — Браузер признаков

## Архитектуры SAE[​](<#sae-architectures> "Прямая ссылка на Архитектуры SAE")
| Архитектура | Описание | Сценарий использования  |
|---|---|---  |
|**Standard**| ReLU + L1-штраф| Общего назначения  |
|**Gated**| Изучаемый механизм стробирования| Лучший контроль разреженности  |
|**TopK**| Ровно K активных признаков| Постоянная разреженность
[code] 
    # TopK SAE (exactly 50 features active)  
    cfg = LanguageModelSAERunnerConfig(  
        architecture="topk",  
        activation_fn="topk",  
        activation_fn_kwargs={"k": 50},  
    )  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Проблема: полисемантичность и суперпозиция](<#the-problem-polysemanticity--superposition>)
  * [Когда использовать SAELens](<#when-to-use-saelens>)
  * [Установка](<#installation>)
  * [Основные концепции](<#core-concepts>)
    * [Что изучают SAE](<#what-saes-learn>)
    * [Ключевое подтверждение (исследование Anthropic)](<#key-validation-anthropic-research>)
  * [Рабочий процесс 1: Загрузка и анализ предобученных SAE](<#workflow-1-loading-and-analyzing-pre-trained-saes>)
    * [Пошаговая инструкция](<#step-by-step>)
    * [Доступные предобученные SAE](<#available-pre-trained-saes>)
    * [Контрольный список](<#checklist>)
  * [Рабочий процесс 2: Обучение пользовательского SAE](<#workflow-2-training-a-custom-sae>)
    * [Пошаговая инструкция](<#step-by-step-1>)
    * [Ключевые гиперпараметры](<#key-hyperparameters>)
    * [Метрики оценки](<#evaluation-metrics>)
    * [Контрольный список](<#checklist-1>)
  * [Рабочий процесс 3: Анализ признаков и управление](<#workflow-3-feature-analysis-and-steering>)
    * [Анализ отдельных признаков](<#analyzing-individual-features>)
    * [Управление признаками](<#feature-steering>)
    * [Атрибуция признаков](<#feature-attribution>)
  * [Типичные проблемы и решения](<#common-issues--solutions>)
    * [Проблема: Высокая доля мёртвых признаков](<#issue-high-dead-feature-ratio>)
    * [Проблема: Плохая реконструкция (низкое восстановление CE)](<#issue-poor-reconstruction-low-ce-recovery>)
    * [Проблема: Признаки не интерпретируемы](<#issue-features-not-interpretable>)
    * [Проблема: Ошибки памяти во время обучения](<#issue-memory-errors-during-training>)
  * [Интеграция с Neuronpedia](<#integration-with-neuronpedia>)
  * [Справочник ключевых классов](<#key-classes-reference>)
  * [Справочная документация](<#reference-documentation>)
  * [Внешние ресурсы](<#external-resources>)
    * [Руководства](<#tutorials>)
    * [Статьи](<#papers>)
    * [Официальная документация](<#official-documentation>)
  * [Архитектуры SAE](<#sae-architectures>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-saelens -->
