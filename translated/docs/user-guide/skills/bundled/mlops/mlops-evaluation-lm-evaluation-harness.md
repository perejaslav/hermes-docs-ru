На этой странице
lm-eval-harness: бенчмаркинг LLM (MMLU, GSM8K и др.).

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/mlops/evaluation/lm-evaluation-harness` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `lm-eval`, `transformers`, `vllm` |
|Теги| `Evaluation`, `LM Evaluation Harness`, `Benchmarking`, `MMLU`, `HumanEval`, `GSM8K`, `EleutherAI`, `Model Quality`, `Academic Benchmarks`, `Industry Standard` |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# lm-evaluation-harness - Бенчмаркинг LLM

## Что внутри[​](<#whats-inside> "Прямая ссылка на Что внутри")

Оценивает LLM на 60+ академических бенчмарках (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Используется для бенчмаркинга качества моделей, сравнения моделей, публикации академических результатов или отслеживания прогресса обучения. Отраслевой стандарт, используемый EleutherAI, HuggingFace и ведущими лабораториями. Поддерживает HuggingFace, vLLM, API.

## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")

lm-evaluation-harness оценивает LLM на 60+ академических бенчмарках, используя стандартизированные промпты и метрики.

**Установка**:

```bash
pip install lm-eval
```

**Оценка любой модели HuggingFace**:

```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8
```

**Просмотр доступных задач**:

```bash
lm_eval --tasks list
```

## Типовые рабочие процессы[​](<#common-workflows> "Прямая ссылка на Типовые рабочие процессы")

### Рабочий процесс 1: Стандартная оценка бенчмарков[​](<#workflow-1-standard-benchmark-evaluation> "Прямая ссылка на Рабочий процесс 1: Стандартная оценка бенчмарков")

Оцените модель на основных бенчмарках (MMLU, GSM8K, HumanEval).

Скопируйте этот чек-лист:

```bash
Benchmark Evaluation:
- [ ] Step 1: Choose benchmark suite
- [ ] Step 2: Configure model
- [ ] Step 3: Run evaluation
- [ ] Step 4: Analyze results
```

**Шаг 1: Выбор набора бенчмарков**

**Основные бенчмарки рассуждений**:
* **MMLU** (Massive Multitask Language Understanding) — 57 предметов, множественный выбор
* **GSM8K** — Математические задачи на уровне начальной школы
* **HellaSwag** — Рассуждения на основе здравого смысла
* **TruthfulQA** — Правдивость и фактическая точность
* **ARC** (AI2 Reasoning Challenge) — Вопросы по естественным наукам

**Бенчмарки кода**:
* **HumanEval** — Генерация кода на Python (164 задачи)
* **MBPP** (Mostly Basic Python Problems) — Программирование на Python

**Стандартный набор** (рекомендуется для релизов моделей):

```bash
--tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge
```

**Шаг 2: Настройка модели**

**Модель HuggingFace**:

```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,dtype=bfloat16 \
  --tasks mmlu \
  --device cuda:0 \
  --batch_size auto  # Автоопределение оптимального размера батча
```

**Квантованная модель (4-бит/8-бит)**:

```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,load_in_4bit=True \
  --tasks mmlu \
  --device cuda:0
```

**Пользовательский чекпоинт**:

```bash
lm_eval --model hf \
  --model_args pretrained=/path/to/my-model,tokenizer=/path/to/tokenizer \
  --tasks mmlu \
  --device cuda:0
```

**Шаг 3: Запуск оценки**

```bash
# Полная оценка MMLU (57 предметов)
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --num_fewshot 5 \  # 5-shot оценка (стандарт)
  --batch_size 8 \
  --output_path results/ \
  --log_samples  # Сохранить индивидуальные предсказания
  
# Несколько бенчмарков одновременно
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --num_fewshot 5 \
  --batch_size 8 \
  --output_path results/llama2-7b-eval.json
```

**Шаг 4: Анализ результатов**

Результаты сохраняются в `results/llama2-7b-eval.json`:

```json
{
  "results": {
    "mmlu": {
      "acc": 0.459,
      "acc_stderr": 0.004
    },
    "gsm8k": {
      "exact_match": 0.142,
      "exact_match_stderr": 0.006
    },
    "hellaswag": {
      "acc_norm": 0.765,
      "acc_norm_stderr": 0.004
    }
  },
  "config": {
    "model": "hf",
    "model_args": "pretrained=meta-llama/Llama-2-7b-hf",
    "num_fewshot": 5
  }
}
```

### Рабочий процесс 2: Отслеживание прогресса обучения[​](<#workflow-2-track-training-progress> "Прямая ссылка на Рабочий процесс 2: Отслеживание прогресса обучения")

Оценивайте чекпоинты во время обучения.

```bash
Training Progress Tracking:
- [ ] Step 1: Set up periodic evaluation
- [ ] Step 2: Choose quick benchmarks
- [ ] Step 3: Automate evaluation
- [ ] Step 4: Plot learning curves
```

**Шаг 1: Настройка периодической оценки**

Оценка каждые N шагов обучения:

```bash
#!/bin/bash
# eval_checkpoint.sh
  
CHECKPOINT_DIR=$1
STEP=$2
  
lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 \  # 0-shot для скорости
  --batch_size 16 \
  --output_path results/step-$STEP.json
```

**Шаг 2: Выбор быстрых бенчмарков**

Быстрые бенчмарки для частой оценки:
* **HellaSwag**: ~10 минут на 1 GPU
* **GSM8K**: ~5 минут
* **PIQA**: ~2 минуты

Избегайте для частой оценки (слишком медленно):
* **MMLU**: ~2 часа (57 предметов)
* **HumanEval**: Требует выполнения кода

**Шаг 3: Автоматизация оценки**

Интеграция с тренировочным скриптом:

```python
# In training loop
if step % eval_interval == 0:
    model.save_pretrained(f"checkpoints/step-{step}")
  
    # Run evaluation
    os.system(f"./eval_checkpoint.sh checkpoints step-{step}")
```

Или используйте колбэки PyTorch Lightning:

```python
from pytorch_lightning import Callback
  
class EvalHarnessCallback(Callback):
    def on_validation_epoch_end(self, trainer, pl_module):
        step = trainer.global_step
        checkpoint_path = f"checkpoints/step-{step}"
  
        # Save checkpoint
        trainer.save_checkpoint(checkpoint_path)
  
        # Run lm-eval
        os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} ...")
```

**Шаг 4: Построение кривых обучения**

```python
import json
import matplotlib.pyplot as plt
  
# Load all results
steps = []
mmlu_scores = []
  
for file in sorted(glob.glob("results/step-*.json")):
    with open(file) as f:
        data = json.load(f)
        step = int(file.split("-")[1].split(".")[0])
        steps.append(step)
        mmlu_scores.append(data["results"]["mmlu"]["acc"])
  
# Plot
plt.plot(steps, mmlu_scores)
plt.xlabel("Training Step")
plt.ylabel("MMLU Accuracy")
plt.title("Training Progress")
plt.savefig("training_curve.png")
```

### Рабочий процесс 3: Сравнение нескольких моделей[​](<#workflow-3-compare-multiple-models> "Прямая ссылка на Рабочий процесс 3: Сравнение нескольких моделей")

Набор бенчмарков для сравнения моделей.

```bash
Model Comparison:
- [ ] Step 1: Define model list
- [ ] Step 2: Run evaluations
- [ ] Step 3: Generate comparison table
```

**Шаг 1: Определение списка моделей**

```bash
# models.txt
meta-llama/Llama-2-7b-hf
meta-llama/Llama-2-13b-hf
mistralai/Mistral-7B-v0.1
microsoft/phi-2
```

**Шаг 2: Запуск оценок**

```bash
#!/bin/bash
# eval_all_models.sh
  
TASKS="mmlu,gsm8k,hellaswag,truthfulqa"
  
while read model; do
    echo "Evaluating $model"
  
    # Extract model name for output file
    model_name=$(echo $model | sed 's/\//-/g')
  
    lm_eval --model hf \
      --model_args pretrained=$model,dtype=bfloat16 \
      --tasks $TASKS \
      --num_fewshot 5 \
      --batch_size auto \
      --output_path results/$model_name.json
  
done < models.txt
```

**Шаг 3: Генерация таблицы сравнения**

```python
import json
import pandas as pd
  
models = [
    "meta-llama-Llama-2-7b-hf",
    "meta-llama-Llama-2-13b-hf",
    "mistralai-Mistral-7B-v0.1",
    "microsoft-phi-2"
]
  
tasks = ["mmlu", "gsm8k", "hellaswag", "truthfulqa"]
  
results = []
for model in models:
    with open(f"results/{model}.json") as f:
        data = json.load(f)
        row = {"Model": model.replace("-", "/")}
        for task in tasks:
            # Get primary metric for each task
            metrics = data["results"][task]
            if "acc" in metrics:
                row[task.upper()] = f"{metrics['acc']:.3f}"
            elif "exact_match" in metrics:
                row[task.upper()] = f"{metrics['exact_match']:.3f}"
        results.append(row)
  
df = pd.DataFrame(results)
print(df.to_markdown(index=False))
```

Результат:

```bash
| Model                  | MMLU  | GSM8K | HELLASWAG | TRUTHFULQA |
|------------------------|-------|-------|-----------|------------|
| meta-llama/Llama-2-7b  | 0.459 | 0.142 | 0.765     | 0.391      |
| meta-llama/Llama-2-13b | 0.549 | 0.287 | 0.801     | 0.430      |
| mistralai/Mistral-7B   | 0.626 | 0.395 | 0.812     | 0.428      |
| microsoft/phi-2        | 0.560 | 0.613 | 0.682     | 0.447      |
```

### Рабочий процесс 4: Оценка с vLLM (более быстрый инференс)[​](<#workflow-4-evaluate-with-vllm-faster-inference> "Прямая ссылка на Рабочий процесс 4: Оценка с vLLM (более быстрый инференс)")

Используйте бэкенд vLLM для оценки в 5-10 раз быстрее.

```bash
vLLM Evaluation:
- [ ] Step 1: Install vLLM
- [ ] Step 2: Configure vLLM backend
- [ ] Step 3: Run evaluation
```

**Шаг 1: Установка vLLM**

```bash
pip install vllm
```

**Шаг 2: Настройка бэкенда vLLM**

```bash
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8 \
  --tasks mmlu \
  --batch_size auto
```

**Шаг 3: Запуск оценки**

vLLM работает в 5-10× быстрее стандартного HuggingFace:

```bash
# Стандартный HF: ~2 часа на MMLU для модели 7B
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --batch_size 8
  
# vLLM: ~15-20 минут на MMLU для модели 7B
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu \
  --batch_size auto
```

## Когда использовать и альтернативы[​](<#when-to-use-vs-alternatives> "Прямая ссылка на Когда использовать и альтернативы")

**Используйте lm-evaluation-harness когда:**
* Нужно бенчмаркировать модели для академических статей
* Сравниваете качество моделей по стандартным задачам
* Отслеживаете прогресс обучения
* Нужно предоставить стандартизированные метрики (все используют одинаковые промпты)
* Требуется воспроизводимая оценка

**Используйте альтернативы вместо:**
* **HELM** (Stanford): Более широкая оценка (честность, эффективность, калибровка)
* **AlpacaEval**: Оценка следования инструкциям с LLM-судьями
* **MT-Bench**: Оценка диалогов с несколькими витками
* **Пользовательские скрипты**: Доменно-специфичная оценка

## Часто встречающиеся проблемы[​](<#common-issues> "Прямая ссылка на Часто встречающиеся проблемы")

**Проблема: Оценка слишком медленная**

Используйте бэкенд vLLM:

```bash
lm_eval --model vllm \
  --model_args pretrained=model-name,tensor_parallel_size=2
```

Или уменьшите количество fewshot-примеров:

```bash
--num_fewshot 0  # Вместо 5
```

Или оцените подмножество MMLU:

```bash
--tasks mmlu_stem  # Только STEM-предметы
```

**Проблема: Не хватает памяти**

Уменьшите размер батча:

```bash
--batch_size 1  # Или --batch_size auto
```

Используйте квантизацию:

```bash
--model_args pretrained=model-name,load_in_8bit=True
```

Включите выгрузку на CPU:

```bash
--model_args pretrained=model-name,device_map=auto,offload_folder=offload
```

**Проблема: Результаты отличаются от опубликованных**

Проверьте количество fewshot:

```bash
--num_fewshot 5  # В большинстве статей используется 5-shot
```

Проверьте точное название задачи:

```bash
--tasks mmlu  # Не mmlu_direct или mmlu_fewshot
```

Убедитесь, что модель и токенизатор совпадают:

```bash
--model_args pretrained=model-name,tokenizer=same-model-name
```

**Проблема: HumanEval не выполняет код**

Установите зависимости для выполнения:

```bash
pip install human-eval
```

Включите выполнение кода:

```bash
lm_eval --model hf \
  --model_args pretrained=model-name \
  --tasks humaneval \
  --allow_code_execution  # Требуется для HumanEval
```

## Продвинутые темы[​](<#advanced-topics> "Прямая ссылка на Продвинутые темы")

**Описания бенчмарков**: См. [references/benchmark-guide.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/benchmark-guide.md>) для подробного описания всех 60+ задач, что они измеряют и как интерпретировать.

**Пользовательские задачи**: См. [references/custom-tasks.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/custom-tasks.md>) для создания доменно-специфичных задач оценки.

**Оценка через API**: См. [references/api-evaluation.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/api-evaluation.md>) для оценки моделей OpenAI, Anthropic и других API-моделей.

**Стратегии Multi-GPU**: См. [references/distributed-eval.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/distributed-eval.md>) для data parallel и tensor parallel оценки.

## Требования к оборудованию[​](<#hardware-requirements> "Прямая ссылка на Требования к оборудованию")

* **GPU**: NVIDIA (CUDA 11.8+), работает на CPU (очень медленно)
* **VRAM**:
  * Модель 7B: 16GB (bf16) или 8GB (8-бит)
  * Модель 13B: 28GB (bf16) или 14GB (8-бит)
  * Модель 70B: Требуется multi-GPU или квантизация
* **Время** (модель 7B, один A100):
  * HellaSwag: 10 минут
  * GSM8K: 5 минут
  * MMLU (полный): 2 часа
  * HumanEval: 20 минут

## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")

* GitHub: <https://github.com/EleutherAI/lm-evaluation-harness>
* Документация: <https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs>
* Библиотека задач: 60+ задач, включая MMLU, GSM8K, HumanEval, TruthfulQA, HellaSwag, ARC, WinoGrande и др.
* Лидерборд: <https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard> (использует этот harness)

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Что внутри](<#whats-inside>)
* [Быстрый старт](<#quick-start>)
* [Типовые рабочие процессы](<#common-workflows>)
  * [Рабочий процесс 1: Стандартная оценка бенчмарков](<#workflow-1-standard-benchmark-evaluation>)
  * [Рабочий процесс 2: Отслеживание прогресса обучения](<#workflow-2-track-training-progress>)
  * [Рабочий процесс 3: Сравнение нескольких моделей](<#workflow-3-compare-multiple-models>)
  * [Рабочий процесс 4: Оценка с vLLM (более быстрый инференс)](<#workflow-4-evaluate-with-vllm-faster-inference>)
* [Когда использовать и альтернативы](<#when-to-use-vs-alternatives>)
* [Часто встречающиеся проблемы](<#common-issues>)
* [Продвинутые темы](<#advanced-topics>)
* [Требования к оборудованию](<#hardware-requirements>)
* [Ресурсы](<#resources>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-evaluation-lm-evaluation-harness -->
