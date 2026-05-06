На этой странице
OBLITERATUS: абляция отказов LLM (diff-in-means).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---|---  
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/mlops/inference/obliteratus`  
|Версия| `2.0.0`  
|Автор| Hermes Agent  
|Лицензия| MIT  
|Зависимости| `obliteratus`, `torch`, `transformers`, `bitsandbytes`, `accelerate`, `safetensors`  
|Теги| `Abliteration`, `Uncensoring`, `Refusal-Removal`, `LLM`, `Weight-Projection`, `SVD`, `Mechanistic-Interpretability`, `HuggingFace`, `Model-Surgery`  
|Связанные навыки| `vllm`, `gguf`, [`huggingface-tokenizers`](</docs/user-guide/skills/optional/mlops/mlops-huggingface-tokenizers>)  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Навык OBLITERATUS
## Что внутри[​](<#whats-inside> "Прямая ссылка на Что внутри")
9 CLI-методов, 28 аналитических модулей, 116 предустановок моделей для 5 вычислительных уровней, турнирная оценка и рекомендации на основе телеметрии.
Удаляет поведение отказа (ограничения) из LLM с открытым весом без переобучения или дообучения. Использует методы механистической интерпретируемости — включая diff-in-means, SVD, отбеленный SVD, LEACE-стирание концепций, SAE-декомпозицию, байесовское проецирование ядра и другие — для выявления и хирургического удаления направлений отказа из весов модели с сохранением способности к рассуждению.
**Предупреждение о лицензии:** OBLITERATUS распространяется под лицензией AGPL-3.0. НИКОГДА не импортируйте его как Python-библиотеку. Всегда вызывайте через CLI (команда `obliteratus`) или подпроцесс. Это сохраняет лицензию Hermes Agent (MIT) чистой.
## Видео-гид[​](<#video-guide> "Прямая ссылка на Видео-гид")
Обзор использования OBLITERATUS агентом Hermes для абляции Gemma: <https://www.youtube.com/watch?v=8fG9BrNTeHs> («OBLITERATUS: AI-агент удалил защитные ограничения Gemma 4»)
Полезно, когда пользователь хочет получить визуальный обзор всего рабочего процесса перед самостоятельным запуском.
## Когда использовать этот навык[​](<#when-to-use-this-skill> "Прямая ссылка на Когда использовать этот навык")
Запускать, когда пользователь:
  * Хочет «расцензурировать» или «аблятировать» LLM
  * Спрашивает об удалении отказов/ограничений из модели
  * Хочет создать нецензурированную версию Llama, Qwen, Mistral и т.д.
  * Упоминает «refusal removal», «abliteration», «weight projection»
  * Хочет проанализировать, как работает механизм отказа модели
  * Упоминает OBLITERATUS, abliterator или направления отказа


## Шаг 1: Установка[​](<#step-1-installation> "Прямая ссылка на Шаг 1: Установка")
Проверьте, установлен ли уже инструмент:
[code] 
    obliteratus --version 2>/dev/null && echo "INSTALLED" || echo "NOT INSTALLED"  
    
[/code]
Если не установлен, клонируйте и установите из GitHub:
[code] 
    git clone https://github.com/elder-plinius/OBLITERATUS.git  
    cd OBLITERATUS  
    pip install -e .  
    # Для поддержки веб-интерфейса Gradio:  
    # pip install -e ".[spaces]"  
    
[/code]
**ВАЖНО:** Подтвердите с пользователем перед установкой. Это загружает ~5-10 ГБ зависимостей (PyTorch, Transformers, bitsandbytes и т.д.).
## Шаг 2: Проверка оборудования[​](<#step-2-check-hardware> "Прямая ссылка на Шаг 2: Проверка оборудования")
Прежде всего, проверьте доступный GPU:
[code] 
    python3 -c "  
    import torch  
    if torch.cuda.is_available():  
        gpu = torch.cuda.get_device_name(0)  
        vram = torch.cuda.get_device_properties(0).total_memory / 1024**3  
        print(f'GPU: {gpu}')  
        print(f'VRAM: {vram:.1f} GB')  
        if vram < 4: print('TIER: tiny (models under 1B)')  
        elif vram < 8: print('TIER: small (models 1-4B)')  
        elif vram < 16: print('TIER: medium (models 4-9B with 4bit quant)')  
        elif vram < 32: print('TIER: large (models 8-32B with 4bit quant)')  
        else: print('TIER: frontier (models 32B+)')  
    else:  
        print('NO GPU - only tiny models (under 1B) on CPU')  
    "  
    
[/code]
### Требования к VRAM (с 4-битной квантизацией)[​](<#vram-requirements-with-4-bit-quantization> "Прямая ссылка на Требования к VRAM (с 4-битной квантизацией)")
VRAM| Макс. размер модели| Примеры моделей  
---|---|---  
Только CPU| ~1B параметров| GPT-2, TinyLlama, SmolLM  
4-8 ГБ| ~4B параметров| Qwen2.5-1.5B, Phi-3.5 mini, Llama 3.2 3B  
8-16 ГБ| ~9B параметров| Llama 3.1 8B, Mistral 7B, Gemma 2 9B  
24 ГБ| ~32B параметров| Qwen3-32B, Llama 3.1 70B (сжато), Command-R  
48 ГБ+| ~72B+ параметров| Qwen2.5-72B, DeepSeek-R1  
Multi-GPU| 200B+ параметров| Llama 3.1 405B, DeepSeek-V3 (685B MoE)  
## Шаг 3: Просмотр доступных моделей и получение рекомендаций[​](<#step-3-browse-available-models--get-recommendations> "Прямая ссылка на Шаг 3: Просмотр доступных моделей и получение рекомендаций")
[code] 
    # Просмотр моделей по вычислительному уровню  
    obliteratus models --tier medium  
      
    # Информация об архитектуре конкретной модели  
    obliteratus info <model_name>  
      
    # Рекомендация лучшего метода и параметров на основе телеметрии  
    obliteratus recommend <model_name>  
    obliteratus recommend <model_name> --insights  # глобальные кросс-архитектурные рейтинги  
    
[/code]
## Шаг 4: Выбор метода[​](<#step-4-choose-a-method> "Прямая ссылка на Шаг 4: Выбор метода")
### Руководство по выбору метода[​](<#method-selection-guide> "Прямая ссылка на Руководство по выбору метода")
**По умолчанию / рекомендуется для большинства случаев: `advanced`.** Использует многомерное SVD с проекцией, сохраняющей норму, и хорошо протестирован.
Ситуация| Рекомендуемый метод| Почему  
---|---|---  
По умолчанию / большинство моделей| `advanced`| Многомерное SVD, сохранение нормы, надёжно  
Быстрое тестирование / прототипирование| `basic`| Быстро, просто, достаточно для оценки  
Плотная модель (Llama, Mistral)| `advanced`| Многомерное, сохранение нормы  
MoE модель (DeepSeek, Mixtral)| `nuclear`| Поэкспертная детализация, работает со сложностью MoE  
Модель рассуждений (R1 дистилляты)| `surgical`| С учётом CoT, сохраняет цепочку мыслей  
Упорные отказы сохраняются| `aggressive`| Отбеленный SVD + хирургия голов + джейлбрейк  
Нужны обратимые изменения| Используйте управляющие векторы (см. раздел Анализ)|  
Максимальное качество, время не важно| `optimized`| Байесовский поиск лучших параметров  
Экспериментальное автоопределение| `informed`| Автоопределение типа выравнивания — экспериментально, может не всегда превосходить advanced  
### 9 CLI-методов[​](<#9-cli-methods> "Прямая ссылка на 9 CLI-методов")
  * **basic** — Одно направление отказа через diff-in-means. Быстро (~5-10 мин для 8B).
  * **advanced** (ПО УМОЛЧАНИЮ, РЕКОМЕНДУЕТСЯ) — Несколько SVD-направлений, проекция с сохранением нормы, 2 прохода уточнения. Средняя скорость (~10-20 мин).
  * **aggressive** — Отбеленный SVD + контрастивный джейлбрейк + хирургия голов внимания. Выше риск повреждения связности.
  * **spectral_cascade** — DCT-декомпозиция в частотной области. Исследовательский/новый подход.
  * **informed** — Запускает анализ ВО ВРЕМЯ абляции для автонастройки. Экспериментально — медленнее и менее предсказуемо, чем advanced.
  * **surgical** — SAE-признаки + маскировка нейронов + хирургия голов + поэкспертно. Очень медленно (~1-2 ч). Лучше всего для моделей рассуждений.
  * **optimized** — Байесовский поиск гиперпараметров (Optuna TPE). Самое долгое выполнение, но находит оптимальные параметры.
  * **inverted** — Инвертирует направление отказа. Модель становится активно сговорчивой.
  * **nuclear** — Максимальная комбинация для упорных MoE-моделей. Поэкспертная детализация.


### Методы извлечения направлений (флаг --direction-method)[​](<#direction-extraction-methods---direction-method-flag> "Прямая ссылка на Методы извлечения направлений (флаг --direction-method)")
  * **diff_means** (по умолчанию) — Простая разница средних между активациями отказа и подчинения. Надёжно.
  * **svd** — Многомерное SVD-извлечение. Лучше для сложного выравнивания.
  * **leace** — LEACE (линейное стирание через оценку в замкнутой форме). Оптимальное линейное стирание.


### 4 метода только через Python API[​](<#4-python-api-only-methods> "Прямая ссылка на 4 метода только через Python API")
(НЕДОСТУПНЫ через CLI — требуют импорта Python, что нарушает границу AGPL. Упоминать пользователю только если он явно хочет использовать OBLITERATUS как библиотеку в своём AGPL-проекте.)
  * failspy, gabliteration, heretic, rdo


## Шаг 5: Запуск абляции[​](<#step-5-run-abliteration> "Прямая ссылка на Шаг 5: Запуск абляции")
### Стандартное использование[​](<#standard-usage> "Прямая ссылка на Стандартное использование")
[code] 
    # Метод по умолчанию (advanced) — рекомендуется для большинства моделей  
    obliteratus obliterate <model_name> --method advanced --output-dir ./abliterated-models  
      
    # С 4-битной квантизацией (экономит VRAM)  
    obliteratus obliterate <model_name> --method advanced --quantization 4bit --output-dir ./abliterated-models  
      
    # Большие модели (70B+) — консервативные настройки по умолчанию  
    obliteratus obliterate <model_name> --method advanced --quantization 4bit --large-model --output-dir ./abliterated-models  
    
[/code]
### Точная настройка параметров[​](<#fine-tuning-parameters> "Прямая ссылка на Точная настройка параметров")
[code] 
    obliteratus obliterate <model_name> \  
      --method advanced \  
      --direction-method diff_means \  
      --n-directions 4 \  
      --refinement-passes 2 \  
      --regularization 0.1 \  
      --quantization 4bit \  
      --output-dir ./abliterated-models \  
      --contribute  # опциональная телеметрия для исследований сообщества  
    
[/code]
### Ключевые флаги[​](<#key-flags> "Прямая ссылка на Ключевые флаги")
Флаг| Описание| По умолчанию  
---|---|---  
`--method`| Метод абляции| advanced  
`--direction-method`| Извлечение направления| diff_means  
`--n-directions`| Количество направлений отказа (1-32)| зависит от метода  
`--refinement-passes`| Количество итеративных проходов (1-5)| 2  
`--regularization`| Сила регуляризации (0.0-1.0)| 0.1  
`--quantization`| Загрузка в 4bit или 8bit| нет (полная точность)  
`--large-model`| Консервативные настройки для 120B+| false  
`--output-dir`| Куда сохранять аблятированную модель| ./obliterated_model  
`--contribute`| Делиться анонимными результатами для исследований| false  
`--verify-sample-size`| Количество тестовых запросов для проверки отказов| 20  
`--dtype`| Тип данных модели (float16, bfloat16)| auto  
### Другие режимы выполнения[​](<#other-execution-modes> "Прямая ссылка на Другие режимы выполнения")
[code] 
    # Интерактивный режим с подсказками (оборудование → модель → предустановка)  
    obliteratus interactive  
      
    # Веб-интерфейс (Gradio)  
    obliteratus ui --port 7860  
      
    # Запуск полного абляционного исследования из YAML-конфига  
    obliteratus run config.yaml --preset quick  
      
    # Турнир: соревнование всех методов друг с другом  
    obliteratus tourney <model_name>  
    
[/code]
## Шаг 6: Проверка результатов[​](<#step-6-verify-results> "Прямая ссылка на Шаг 6: Проверка результатов")
После абляции проверьте выходные метрики:
Метрика| Хорошее значение| Предупреждение  
---|---|---  
Частота отказов| < 5% (в идеале ~0%)| > 10% — отказы сохраняются  
Изменение перплексии| < 10% увеличения| > 15% — повреждение связности  
KL-дивергенция| < 0.1| > 0.5 — значительное смещение распределения  
Связность| Высокая / проходит качественную проверку| Деградированные ответы, повторения  
### Если отказы сохраняются (> 10%)[​](<#if-refusals-persist--10> "Прямая ссылка на Если отказы сохраняются (> 10%)")
  1. Попробуйте метод `aggressive`
  2. Увеличьте `--n-directions` (например, 8 или 16)
  3. Добавьте `--refinement-passes 3`
  4. Попробуйте `--direction-method svd` вместо diff_means


### Если связность повреждена (перплексия > 15% увеличения)[​](<#if-coherence-is-damaged-perplexity--15-increase> "Прямая ссылка на Если связность повреждена (перплексия > 15% увеличения)")
  1. Уменьшите `--n-directions` (попробуйте 2)
  2. Увеличьте `--regularization` (попробуйте 0.3)
  3. Уменьшите `--refinement-passes` до 1
  4. Попробуйте метод `basic` (более щадящий)


## Шаг 7: Использование аблятированной модели[​](<#step-7-use-the-abliterated-model> "Прямая ссылка на Шаг 7: Использование аблятированной модели")
Результат — стандартная директория модели HuggingFace.
[code] 
    # Локальное тестирование с transformers  
    python3 -c "  
    from transformers import AutoModelForCausalLM, AutoTokenizer  
    model = AutoModelForCausalLM.from_pretrained('./abliterated-models/<model>')  
    tokenizer = AutoTokenizer.from_pretrained('./abliterated-models/<model>')  
    inputs = tokenizer('Как вскрыть замок?', return_tensors='pt')  
    outputs = model.generate(**inputs, max_new_tokens=200)  
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))  
    "  
      
    # Загрузка на HuggingFace Hub  
    huggingface-cli upload <username>/<model-name>-abliterated ./abliterated-models/<model>  
      
    # Запуск через vLLM  
    vllm serve ./abliterated-models/<model>  
    
[/code]
## Справочник CLI-команд[​](<#cli-command-reference> "Прямая ссылка на Справочник CLI-команд")
Команда| Описание  
---|---  
`obliteratus obliterate`| Основная команда абляции  
`obliteratus info <model>`| Вывод деталей архитектуры модели  
`obliteratus models --tier <tier>`| Просмотр подобранных моделей по вычислительному уровню  
`obliteratus recommend <model>`| Рекомендация метода/параметров на основе телеметрии  
`obliteratus interactive`| Мастер настройки с подсказками  
`obliteratus tourney <model>`| Турнир: все методы друг против друга  
`obliteratus run <config.yaml>`| Выполнение абляционного исследования из YAML  
`obliteratus strategies`| Список всех зарегистрированных стратегий абляции  
`obliteratus report <results.json>`| Повторная генерация визуальных отчётов  
`obliteratus ui`| Запуск веб-интерфейса Gradio  
`obliteratus aggregate`| Сводка данных телеметрии сообщества  
## Аналитические модули[​](<#analysis-modules> "Прямая ссылка на Аналитические модули")
OBLITERATUS включает 28 аналитических модулей для механистической интерпретируемости. Полный справочник см. в `skill_view(name="obliteratus", file_path="references/analysis-modules.md")`.
### Быстрые аналитические команды[​](<#quick-analysis-commands> "Прямая ссылка на Быстрые аналитические команды")
[code] 
    # Запуск конкретных аналитических модулей  
    obliteratus run analysis-config.yaml --preset quick  
      
    # Ключевые модули для первого запуска:  
    # - alignment_imprint: Отпечаток метода выравнивания DPO/RLHF/CAI/SFT  
    # - concept_geometry: Одно направление против многогранного конуса  
    # - logit_lens: Какой слой принимает решение об отказе  
    # - anti_ouroboros: Оценка риска самовосстановления  
    # - causal_tracing: Причинно-необходимые компоненты  
    
[/code]
### Управляющие векторы (обратимая альтернатива)[​](<#steering-vectors-reversible-alternative> "Прямая ссылка на Управляющие векторы (обратимая альтернатива)")
Вместо постоянного изменения весов используйте управление во время инференса:
[code] 
    # Только Python API — для собственных проектов пользователя  
    from obliteratus.analysis.steering_vectors import SteeringVectorFactory, SteeringHookManager  
    
[/code]
## Стратегии абляции[​](<#ablation-strategies> "Прямая ссылка на Стратегии абляции")
Помимо абляции на основе направлений, OBLITERATUS включает структурные стратегии абляции:
  * **Embedding Ablation** — Воздействие на компоненты слоя эмбеддингов
  * **FFN Ablation** — Удаление блоков прямого распространения
  * **Head Pruning** — Обрезка голов внимания
  * **Layer Removal** — Полное удаление слоёв


Список всех доступных: `obliteratus strategies`
## Оценка[​](<#evaluation> "Прямая ссылка на Оценка")
OBLITERATUS включает встроенные инструменты оценки:
  * Бенчмаркинг частоты отказов
  * Сравнение перплексии (до/после)
  * Интеграция с LM Eval Harness для академических бенчмарков
  * Попарное сравнение с конкурентами
  * Отслеживание базовой производительности


## Поддержка платформ[​](<#platform-support> "Прямая ссылка на Поддержка платформ")
  * **CUDA** — Полная поддержка (GPU NVIDIA)
  * **Apple Silicon (MLX)** — Поддерживается через MLX-бэкенд
  * **CPU** — Поддерживается для маленьких моделей (< 1B параметров)


## Шаблоны YAML-конфигов[​](<#yaml-config-templates> "Прямая ссылка на Шаблоны YAML-конфигов")
Загрузка шаблонов для воспроизводимых запусков через `skill_view`:
  * `templates/abliteration-config.yaml` — Стандартный конфиг для одной модели
  * `templates/analysis-study.yaml` — Аналитическое исследование перед абляцией
  * `templates/batch-abliteration.yaml` — Пакетная обработка нескольких моделей


## Телеметрия[​](<#telemetry> "Прямая ссылка на Телеметрия")
OBLITERATUS может опционально отправлять анонимные данные о запусках в глобальный исследовательский датасет. Включите флагом `--contribute`. Никакие личные данные не собираются — только имя модели, метод и метрики.
## Типичные ошибки[​](<#common-pitfalls> "Прямая ссылка на Типичные ошибки")
  1. **Не используйте `informed` по умолчанию** — он экспериментальный и медленнее. Используйте `advanced` для надёжных результатов.
  2. **Модели менее ~1B плохо реагируют на абляцию** — их механизмы отказа поверхностны и фрагментированы, что затрудняет чистое извлечение направления. Ожидайте частичных результатов (20-40% остаточных отказов). Модели от 3B+ имеют более чистые направления отказа и работают значительно лучше (часто 0% отказов с `advanced`).
  3. **`aggressive` может ухудшить ситуацию** — на маленьких моделях он может повредить связность и даже увеличить частоту отказов. Используйте его только если `advanced` оставляет > 10% отказов на модели от 3B+.
  4. **Всегда проверяйте перплексию** — если она подскочила > 15%, модель повреждена. Уменьшите агрессивность.
  5. **MoE-модели требуют особого подхода** — используйте метод `nuclear` для Mixtral, DeepSeek-MoE и т.д.
  6. **Квантизированные модели нельзя повторно квантизировать** — аблятируйте модель в полной точности, затем квантизируйте результат.
  7. **Оценка VRAM приблизительна** — 4-битная квантизация помогает, но пиковое потребление может скачкообразно расти во время извлечения.
  8. **Модели рассуждений чувствительны** — используйте `surgical` для R1-дистиллятов, чтобы сохранить цепочку мыслей.
  9. **Проверьте `obliteratus recommend`** — данные телеметрии могут предложить лучшие параметры, чем стандартные.
  10. **Лицензия AGPL** — никогда не делайте `import obliteratus` в MIT/Apache проектах. Только вызов через CLI.
  11. **Большие модели (70B+)** — всегда используйте флаг `--large-model` для консервативных настроек по умолчанию.
  12. **Спектральная сертификация RED — обычное дело** — спектральная проверка часто помечает результат как «неполный», даже когда практическая частота отказов составляет 0%. Проверяйте фактическую частоту отказов, а не полагайтесь только на спектральную сертификацию.


## Дополнительные навыки[​](<#complementary-skills> "Прямая ссылка на Дополнительные навыки")
  * **vllm** — Запуск аблятированных моделей с высокой пропускной способностью
  * **gguf** — Конвертация аблятированных моделей в GGUF для llama.cpp
  * **huggingface-tokenizers** — Работа с токенизаторами моделей


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Что внутри](<#whats-inside>)
  * [Видео-гид](<#video-guide>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Шаг 1: Установка](<#step-1-installation>)
  * [Шаг 2: Проверка оборудования](<#step-2-check-hardware>)
    * [Требования к VRAM (с 4-битной квантизацией)](<#vram-requirements-with-4-bit-quantization>)
  * [Шаг 3: Просмотр доступных моделей и получение рекомендаций](<#step-3-browse-available-models--get-recommendations>)
  * [Шаг 4: Выбор метода](<#step-4-choose-a-method>)
    * [Руководство по выбору метода](<#method-selection-guide>)
    * [9 CLI-методов](<#9-cli-methods>)
    * [Методы извлечения направлений (флаг --direction-method)](<#direction-extraction-methods---direction-method-flag>)
    * [4 метода только через Python API](<#4-python-api-only-methods>)
  * [Шаг 5: Запуск абляции](<#step-5-run-abliteration>)
    * [Стандартное использование](<#standard-usage>)
    * [Точная настройка параметров](<#fine-tuning-parameters>)
    * [Ключевые флаги](<#key-flags>)
    * [Другие режимы выполнения](<#other-execution-modes>)
  * [Шаг 6: Проверка результатов](<#step-6-verify-results>)
    * [Если отказы сохраняются (> 10%)](<#if-refusals-persist--10>)
    * [Если связность повреждена (перплексия > 15% увеличения)](<#if-coherence-is-damaged-perplexity--15-increase>)
  * [Шаг 7: Использование аблятированной модели](<#step-7-use-the-abliterated-model>)
  * [Справочник CLI-команд](<#cli-command-reference>)
  * [Аналитические модули](<#analysis-modules>)
    * [Быстрые аналитические команды](<#quick-analysis-commands>)
    * [Управляющие векторы (обратимая альтернатива)](<#steering-vectors-reversible-alternative>)
  * [Стратегии абляции](<#ablation-strategies>)
  * [Оценка](<#evaluation>)
  * [Поддержка платформ](<#platform-support>)
  * [Шаблоны YAML-конфигов](<#yaml-config-templates>)
  * [Телеметрия](<#telemetry>)
  * [Типичные ошибки](<#common-pitfalls>)
  * [Дополнительные навыки](<#complementary-skills>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-inference-obliteratus -->
