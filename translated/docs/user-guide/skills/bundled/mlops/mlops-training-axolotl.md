На этой странице
Axolotl: YAML-тонкая настройка LLM (LoRA, DPO, GRPO).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/mlops/training/axolotl` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `axolotl`, `torch`, `transformers`, `datasets`, `peft`, `accelerate`, `deepspeed` |
|Теги| `Fine-Tuning`, `Axolotl`, `LLM`, `LoRA`, `QLoRA`, `DPO`, `KTO`, `ORPO`, `GRPO`, `YAML`, `HuggingFace`, `DeepSpeed`, `Multimodal` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Агент видит эти инструкции, когда навык активен.
# Навык Axolotl
## Что внутри[​](<#whats-inside> "Прямая ссылка на Что внутри")
Экспертное руководство по тонкой настройке LLM с помощью Axolotl — YAML-конфиги, 100+ моделей, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, поддержка мультимодальности.
Всесторонняя помощь по разработке с axolotl, сгенерированная из официальной документации.
## Когда использовать этот навык[​](<#when-to-use-this-skill> "Прямая ссылка на Когда использовать этот навык")
Этот навык следует активировать, когда:
  * Вы работаете с axolotl
  * Вы задаёте вопросы о возможностях или API axolotl
  * Вы реализуете решения на основе axolotl
  * Вы отлаживаете код axolotl
  * Вы изучаете лучшие практики axolotl


## Краткий справочник[​](<#quick-reference> "Прямая ссылка на Краткий справочник")
### Типовые паттерны[​](<#common-patterns> "Прямая ссылка на Типовые паттерны")
**Паттерн 1:** Чтобы убедиться, что скорость передачи данных достаточна для вашей задачи обучения, запуск NCCL Tests поможет выявить узкие места, например:
[code] 
    ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 3  
    
[/code]
**Паттерн 2:** Настройте вашу модель на использование FSDP в YAML-файле Axolotl. Например:
[code] 
    fsdp_version: 2  
    fsdp_config:  
      offload_params: true  
      state_dict_type: FULL_STATE_DICT  
      auto_wrap_policy: TRANSFORMER_BASED_WRAP  
      transformer_layer_cls_to_wrap: LlamaDecoderLayer  
      reshard_after_forward: true  
    
[/code]
**Паттерн 3:** Значение context_parallel_size должно быть делителем общего количества GPU. Например:
[code] 
    context_parallel_size  
    
[/code]
**Паттерн 4:** Например: - С 8 GPU и без параллелизма последовательностей: 8 разных батчей обрабатывается за шаг - С 8 GPU и context_parallel_size=4: только 2 разных батча обрабатывается за шаг (каждый разделён на 4 GPU) - Если ваш micro_batch_size на GPU равен 2, глобальный размер батча уменьшается с 16 до 4
[code] 
    context_parallel_size=4  
    
[/code]
**Паттерн 5:** Установка save_compressed: true в вашей конфигурации включает сохранение моделей в сжатом формате, что: - Сокращает использование дискового пространства примерно на 40% - Сохраняет совместимость с vLLM для ускоренного инференса - Сохраняет совместимость с llmcompressor для дальнейшей оптимизации (например, квантование)
[code] 
    save_compressed: true  
    
[/code]
**Паттерн 6:** Примечание: Нет необходимости размещать вашу интеграцию в папке integrations. Она может находиться в любом месте, главное, чтобы она была установлена как пакет в вашем Python-окружении. Смотрите пример в этом репозитории: <https://github.com/axolotl-ai-cloud/diff-transformer>
[code] 
    integrations  
    
[/code]
**Паттерн 7:** Обрабатывайте как одиночные примеры, так и батчированные данные. - одиночный пример: sample[‘input_ids’] — это list[int] - батчированные данные: sample[‘input_ids’] — это list[list[int]]
[code] 
    utils.trainer.drop_long_seq(sample, sequence_len=2048, min_sequence_len=2)  
    
[/code]
### Примеры кода[​](<#example-code-patterns> "Прямая ссылка на Примеры кода")
**Пример 1** (python):
[code] 
    cli.cloud.modal_.ModalCloud(config, app=None)  
    
[/code]
**Пример 2** (python):
[code] 
    cli.cloud.modal_.run_cmd(cmd, run_folder, volumes=None)  
    
[/code]
**Пример 3** (python):
[code] 
    core.trainers.base.AxolotlTrainer(  
        *_args,  
        bench_data_collator=None,  
        eval_data_collator=None,  
        dataset_tags=None,  
        **kwargs,  
    )  
    
[/code]
**Пример 4** (python):
[code] 
    core.trainers.base.AxolotlTrainer.log(logs, start_time=None)  
    
[/code]
**Пример 5** (python):
[code] 
    prompt_strategies.input_output.RawInputOutputPrompter()  
    
[/code]
## Справочные файлы[​](<#reference-files> "Прямая ссылка на Справочные файлы")
Этот навык включает подробную документацию в `references/`:
  * **api.md** — Документация по API
  * **dataset-formats.md** — Документация по форматам наборов данных
  * **other.md** — Прочая документация


Используйте `view` для чтения конкретных справочных файлов, когда требуется детальная информация.
## Работа с этим навыком[​](<#working-with-this-skill> "Прямая ссылка на Работа с этим навыком")
### Для новичков[​](<#for-beginners> "Прямая ссылка на Для новичков")
Начните со справочных файлов getting_started или tutorials для освоения фундаментальных концепций.
### Для конкретных функций[​](<#for-specific-features> "Прямая ссылка на Для конкретных функций")
Используйте соответствующий категорийный справочный файл (api, guides и т.д.) для получения подробной информации.
### Для примеров кода[​](<#for-code-examples> "Прямая ссылка на Для примеров кода")
Раздел краткого справочника выше содержит типовые паттерны, извлечённые из официальной документации.
## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
### references/[​](<#references> "Прямая ссылка на references/")
Организованная документация, извлечённая из официальных источников. Эти файлы содержат:
  * Подробные объяснения
  * Примеры кода с аннотациями языка
  * Ссылки на оригинальную документацию
  * Оглавление для быстрой навигации


### scripts/[​](<#scripts> "Прямая ссылка на scripts/")
Добавляйте вспомогательные скрипты для типовых задач автоматизации.
### assets/[​](<#assets> "Прямая ссылка на assets/")
Добавляйте шаблоны, заготовки или примеры проектов.
## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * Этот навык был автоматически сгенерирован из официальной документации
  * Справочные файлы сохраняют структуру и примеры из исходных документов
  * Примеры кода включают определение языка для лучшей подсветки синтаксиса
  * Паттерны краткого справочника извлечены из типовых примеров использования в документации


## Обновление[​](<#updating> "Прямая ссылка на Обновление")
Чтобы обновить этот навык с новой документацией:
  1. Запустите парсер повторно с той же конфигурацией
  2. Навык будет перестроен с актуальной информацией


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Что внутри](<#whats-inside>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Краткий справочник](<#quick-reference>)
    * [Типовые паттерны](<#common-patterns>)
    * [Примеры кода](<#example-code-patterns>)
  * [Справочные файлы](<#reference-files>)
  * [Работа с этим навыком](<#working-with-this-skill>)
    * [Для новичков](<#for-beginners>)
    * [Для конкретных функций](<#for-specific-features>)
    * [Для примеров кода](<#for-code-examples>)
  * [Ресурсы](<#resources>)
    * [references/](<#references>)
    * [scripts/](<#scripts>)
    * [assets/](<#assets>)
  * [Примечания](<#notes>)
  * [Обновление](<#updating>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-training-axolotl -->
