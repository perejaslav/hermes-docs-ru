On this page
Экспертное руководство по Fully Sharded Data Parallel (полностью сегментированному параллелизму данных) с использованием PyTorch FSDP — сегментирование параметров, смешанная точность, выгрузка на CPU, FSDP2
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")

|   |   |
|---|---|
|Источник|Опционально — установка: `hermes skills install official/mlops/pytorch-fsdp`|
|Путь|`optional-skills/mlops/pytorch-fsdp`|
|Версия|`1.0.0`|
|Автор|Orchestra Research|
|Лицензия|MIT|
|Зависимости|`torch>=2.0`, `transformers`|
|Теги|`Distributed Training`, `PyTorch`, `FSDP`, `Data Parallel`, `Sharding`, `Mixed Precision`, `CPU Offloading`, `FSDP2`, `Large-Scale Training`|

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на справочник: полный SKILL.md")

info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# Pytorch-Fsdp Skill
Всесторонняя помощь в разработке с pytorch-fsdp, основанная на официальной документации.

## Когда использовать этот навык[​](<#when-to-use-this-skill> "Прямая ссылка на «Когда использовать этот навык»")

Этот навык следует активировать, когда:
  * Вы работаете с pytorch-fsdp
  * Вы задаёте вопросы о возможностях или API pytorch-fsdp
  * Вы реализуете решения на основе pytorch-fsdp
  * Вы отлаживаете код pytorch-fsdp
  * Вы изучаете лучшие практики pytorch-fsdp

## Краткий справочник[​](<#quick-reference> "Прямая ссылка на краткий справочник")

### Распространённые шаблоны[​](<#common-patterns> "Прямая ссылка на распространённые шаблоны")

**Шаблон 1:** Generic Join Context Manager# Создан: 06 июня 2025 | Последнее обновление: 06 июня 2025. Generic join context manager упрощает распределённое обучение на неоднородных входных данных. На этой странице описан API соответствующих классов: Join, Joinable и JoinHook. Учебное пособие см. в разделе Distributed Training with Uneven Inputs Using the Join Context Manager. class torch.distributed.algorithms.Join(joinables, enable=True, throw_on_early_termination=False, **kwargs)[source]# Этот класс определяет generic join context manager, который позволяет вызывать пользовательские хуки после присоединения процесса. Эти хуки должны дублировать коллективные коммуникации неприсоединившихся процессов, чтобы предотвратить зависания, ошибки и обеспечить корректность алгоритма. См. JoinHook для подробностей об определении хука. Warning Контекстный менеджер требует, чтобы каждый участвующий Joinable вызывал метод notify_join_context() перед собственными коллективными коммуникациями на каждой итерации для обеспечения корректности. Warning Контекстный менеджер требует, чтобы все атрибуты process_group в объектах JoinHook были одинаковыми. Если существует несколько объектов JoinHook, используется устройство первого из них. Информация о группе процессов и устройстве используется для проверки неприсоединившихся процессов и для уведомления процессов о необходимости выбросить исключение, если включён throw_on_early_termination, причём обе операции используют all-reduce. Параметры joinables (List[Joinable]) – список участвующих Joinable; их хуки обходятся в заданном порядке. enable (bool) – флаг, включающий обнаружение неоднородных входных данных; установка False отключает функциональность контекстного менеджера, и её следует устанавливать только в том случае, если пользователь уверен, что входные данные не будут неоднородными (по умолчанию: True). throw_on_early_termination (bool) – флаг, управляющий выбросом исключения при обнаружении неоднородных входных данных (по умолчанию: False). Пример: >>> import os >>> import torch >>> import torch.distributed as dist >>> import torch.multiprocessing as mp >>> import torch.nn.parall... [сокращено]

[code] 
    Join  
    
[/code]

**Шаблон 2:** Пакет распределённого взаимодействия — torch.distributed# Создан: 12 июля 2017 | Последнее обновление: 04 сентября 2025. Примечание. Пожалуйста, обратитесь к PyTorch Distributed Overview для краткого введения во все функции, связанные с распределённым обучением. Бэкенды# torch.distributed поддерживает четыре встроенных бэкенда, каждый с различными возможностями. В таблице ниже показано, какие функции доступны для использования с CPU или GPU для каждого бэкенда. Для NCCL GPU означает CUDA GPU, а для XCCL — XPU GPU. MPI поддерживает CUDA только в том случае, если реализация, использованная для сборки PyTorch, поддерживает это. Бэкенд gloo mpi nccl xccl Устройство CPU GPU CPU GPU CPU GPU CPU GPU send ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ recv ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ broadcast ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ all_reduce ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ reduce ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ all_gather ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ gather ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ scatter ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ reduce_scatter ✓ ✓ ✘ ✘ ✘ ✓ ✘ ✓ all_to_all ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ barrier ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ Бэкенды, поставляемые с PyTorch# Пакет distributed в PyTorch поддерживает Linux (стабильно), MacOS (стабильно) и Windows (прототип). По умолчанию для Linux бэкенды Gloo и NCCL собираются и включаются в PyTorch distributed (NCCL только при сборке с CUDA). MPI — опциональный бэкенд, который можно включить только при сборке PyTorch из исходного кода (например, сборка PyTorch на хосте с установленным MPI). Примечание. Начиная с PyTorch v1.8, Windows поддерживает все бэкенды коллективных коммуникаций, кроме NCCL. Если аргумент init_method функции init_process_group() указывает на файл, он должен соответствовать следующей схеме: Локальная файловая система: init_method="file:///d:/tmp/some_file". Общая файловая система: init_method="file://////{machine_name}/{share_folder_name}/some_file". Как и на платформе Linux, вы можете включить TcpStore, установив переменные окружения MASTER_ADDR и MASTER_PORT. Какой бэкенд использовать?# Раньше нас часто спрашивали: «Какой бэкенд следует использовать?». Эмпирическое правило Используйте бэкенд NCCL для распределённого обучения с CUDA GPU. Используйте бэкенд XCCL для распределённого обучения с... [сокращено]

[code] 
    torch.distributed  
    
[/code]

**Шаблон 3:** Инициализация# Пакет необходимо инициализировать с помощью функции torch.distributed.init_process_group() или torch.distributed.device_mesh.init_device_mesh() перед вызовом любых других методов. Обе функции блокируются до тех пор, пока все процессы не присоединятся. Warning Инициализация не является потокобезопасной. Создание группы процессов должно выполняться из одного потока, чтобы предотвратить несогласованное назначение UUID между рангами и избежать состояний гонки во время инициализации, которые могут привести к зависаниям. torch.distributed.is_available()[source]# Возвращает True, если пакет distributed доступен. В противном случае torch.distributed не предоставляет никаких других API. В настоящее время torch.distributed доступен на Linux, MacOS и Windows. Установите USE_DISTRIBUTED=1, чтобы включить его при сборке PyTorch из исходного кода. В настоящее время значение по умолчанию: USE_DISTRIBUTED=1 для Linux и Windows, USE_DISTRIBUTED=0 для MacOS. Тип возвращаемого значения bool torch.distributed.init_process_group(backend=None, init_method=None, timeout=None, world_size=-1, rank=-1, store=None, group_name='', pg_options=None, device_id=None)[source]# Инициализирует группу процессов по умолчанию. Это также инициализирует пакет distributed. Существует 2 основных способа инициализации группы процессов: Явно указать store, rank и world_size. Указать init_method (строку URL), которая определяет, где/как обнаруживать пиры. Опционально указать rank и world_size или закодировать все необходимые параметры в URL и опустить их. Если ни то, ни другое не указано, init_method считается равным «env://». Параметры backend (str или Backend, опционально) – Используемый бэкенд. В зависимости от конфигурации сборки допустимые значения включают mpi, gloo, nccl, ucc, xccl или бэкенд, зарегистрированный сторонним плагином. Начиная с версии 2.6, если backend не указан, c10d будет использовать бэкенд, зарегистрированный для типа устройства, указанного в аргументе device_id (если он предоставлен). Известные регистрации по умолчанию на сегодня: nccl для cuda, gloo для cpu, xccl для xpu. Если ни backend, ни device_id не предостав... [сокращено]

[code] 
    torch.distributed.init_process_group()  
    
[/code]

**Шаблон 4:** Пример:

[code] 
    >>> from torch.distributed.device_mesh import init_device_mesh  
    >>>  
    >>> mesh_1d = init_device_mesh("cuda", mesh_shape=(8,))  
    >>> mesh_2d = init_device_mesh("cuda", mesh_shape=(2, 8), mesh_dim_names=("dp", "tp"))  
    
[/code]

**Шаблон 5:** Группы# По умолчанию коллективные операции работают с группой по умолчанию (также называемой миром) и требуют, чтобы все процессы вызывали функцию распределённого взаимодействия. Однако некоторые рабочие нагрузки могут выиграть от более детальной коммуникации. Здесь на помощь приходят распределённые группы. Функция new_group() может использоваться для создания новых групп с произвольными подмножествами всех процессов. Она возвращает непрозрачный дескриптор группы, который может быть передан в качестве аргумента group всем коллективным операциям (коллективные операции — это распределённые функции для обмена информацией в определённых общеизвестных шаблонах программирования). torch.distributed.new_group(ranks=None, timeout=None, backend=None, pg_options=None, use_local_synchronization=False, group_desc=None, device_id=None)[source]# Создаёт новую распределённую группу. Эта функция требует, чтобы все процессы в основной группе (т.е. все процессы, являющиеся частью распределённой задачи) вызвали эту функцию, даже если они не будут членами группы. Кроме того, группы должны создаваться в одном и том же порядке во всех процессах. Warning Безопасное конкурентное использование: При использовании нескольких групп процессов с бэкендом NCCL пользователь должен обеспечить глобально согласованный порядок выполнения коллективных операций между рангами. Если несколько потоков в рамках одного процесса инициируют коллективные операции, необходима явная синхронизация для обеспечения согласованного порядка. При использовании асинхронных вариантов API torch.distributed возвращается объект work, и ядро связи ставится в очередь на отдельный поток CUDA, что позволяет совмещать коммуникацию и вычисления. После того как одна или несколько асинхронных операций были запущены в одной группе процессов, они должны быть синхронизированы с другими потоками CUDA с помощью вызова work.wait() перед использованием другой группы процессов. См. Using multiple NCCL communicators concurrently <[https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently>](<https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently%3E>) для получения дополнительных сведений.

[code] 
    new_group()  
    
[/code]

**Шаблон 6:** Warning Безопасное конкурентное использование: При использовании нескольких групп процессов с бэкендом NCCL пользователь должен обеспечить глобально согласованный порядок выполнения коллективных операций между рангами. Если несколько потоков в рамках одного процесса инициируют коллективные операции, необходима явная синхронизация для обеспечения согласованного порядка. При использовании асинхронных вариантов API torch.distributed возвращается объект work, и ядро связи ставится в очередь на отдельный поток CUDA, что позволяет совмещать коммуникацию и вычисления. После того как одна или несколько асинхронных операций были запущены в одной группе процессов, они должны быть синхронизированы с другими потоками CUDA с помощью вызова work.wait() перед использованием другой группы процессов. См. Using multiple NCCL communicators concurrently <[https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently>](<https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently%3E>) для получения дополнительных сведений.

[code] 
    NCCL  
    
[/code]

**Шаблон 7:** Примечание Если вы используете DistributedDataParallel в сочетании с Distributed RPC Framework, вы всегда должны использовать torch.distributed.autograd.backward() для вычисления градиентов и torch.distributed.optim.DistributedOptimizer для оптимизации параметров. Пример: >>> import torch.distributed.autograd as dist_autograd >>> from torch.nn.parallel import DistributedDataParallel as DDP >>> import torch >>> from torch import optim >>> from torch.distributed.optim import DistributedOptimizer >>> import torch.distributed.rpc as rpc >>> from torch.distributed.rpc import RRef >>> >>> t1 = torch.rand((3, 3), requires_grad=True) >>> t2 = torch.rand((3, 3), requires_grad=True) >>> rref = rpc.remote("worker1", torch.add, args=(t1, t2)) >>> ddp_model = DDP(my_model) >>> >>> # Setup optimizer >>> optimizer_params = [rref] >>> for param in ddp_model.parameters(): >>> optimizer_params.append(RRef(param)) >>> >>> dist_optim = DistributedOptimizer( >>> optim.SGD, >>> optimizer_params, >>> lr=0.05, >>> ) >>> >>> with dist_autograd.context() as context_id: >>> pred = ddp_model(rref.to_here()) >>> loss = loss_func(pred, target) >>> dist_autograd.backward(context_id, [loss]) >>> dist_optim.step(context_id)

[code] 
    torch.distributed.autograd.backward()  
    
[/code]

**Шаблон 8:** static_graph (bool) – Если установлено True, DDP знает, что обучаемый граф статичен. Статический граф означает: 1) Набор используемых и неиспользуемых параметров не изменится в течение всего цикла обучения; в этом случае не имеет значения, установил ли пользователь find_unused_parameters = True или нет. 2) Способ обучения графа не изменится в течение всего цикла обучения (т.е. отсутствует поток управления, зависящий от итераций). Когда static_graph установлен в True, DDP будет поддерживать случаи, которые ранее не поддерживались: 1) Рекуррентные обратные проходы. 2) Многократная активация checkpointing. 3) Активация checkpointing, когда модель имеет неиспользуемые параметры. 4) Наличие параметров модели, находящихся вне функции forward. 5) Потенциальное повышение производительности при наличии неиспользуемых параметров, так как DDP не будет искать граф на каждой итерации для обнаружения неиспользуемых параметров, когда static_graph установлен в True. Чтобы проверить, можно ли установить static_graph в True, один из способов — проверить данные логирования DDP в конце предыдущего обучения модели: если ddp_logging_data.get("can_set_static_graph") == True, то в большинстве случаев можно также установить static_graph = True. Пример::>>> model_DDP = torch.nn.parallel.DistributedDataParallel(model) >>> # Training loop >>> ... >>> ddp_logging_data = model_DDP._get_ddp_logging_data() >>> static_graph = ddp_logging_data.get("can_set_static_graph")

[code] 
    True  
    
[/code]

## Файлы для справки[​](<#reference-files> "Прямая ссылка на файлы для справки")

Этот навык включает подробную документацию в `references/`:
  * **other.md** \\- Прочая документация

Используйте `view` для чтения конкретных справочных файлов, когда требуется подробная информация.

## Работа с этим навыком[​](<#working-with-this-skill> "Прямая ссылка на «Работа с этим навыком»")

### Для начинающих[​](<#for-beginners> "Прямая ссылка на «Для начинающих»")

Начните с файлов getting_started или tutorials для изучения основополагающих концепций.

### Для конкретных функций[​](<#for-specific-features> "Прямая ссылка на «Для конкретных функций»")

Используйте соответствующий справочный файл категории (api, guides и т.д.) для получения подробной информации.

### Для примеров кода[​](<#for-code-examples> "Прямая ссылка на «Для примеров кода»")

Раздел краткого справочника выше содержит распространённые шаблоны, извлечённые из официальной документации.

## Ресурсы[​](<#resources> "Прямая ссылка на «Ресурсы»")

### references/[​](<#references> "Прямая ссылка на references/")

Организованная документация, извлечённая из официальных источников. Эти файлы содержат:
  * Подробные объяснения
  * Примеры кода с аннотациями языка
  * Ссылки на оригинальную документацию
  * Оглавление для быстрой навигации

### scripts/[​](<#scripts> "Прямая ссылка на scripts/")

Добавляйте вспомогательные скрипты для常见 задач автоматизации.

### assets/[​](<#assets> "Прямая ссылка на assets/")

Добавляйте шаблоны, boilerplate или примеры проектов сюда.

## Заметки[​](<#notes> "Прямая ссылка на «Заметки»")

  * Этот навык был автоматически создан на основе официальной документации
  * Справочные файлы сохраняют структуру и примеры из исходных документов
  * Примеры кода включают определение языка для лучшей подсветки синтаксиса
  * Шаблоны из краткого справочника извлечены из распространённых примеров использования в документации

## Обновление[​](<#updating> "Прямая ссылка на «Обновление»")

Чтобы обновить этот навык новой документацией:
  1. Повторно запустите скрапер с той же конфигурацией
  2. Навык будет перестроен с актуальной информацией

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Краткий справочник](<#quick-reference>)
    * [Распространённые шаблоны](<#common-patterns>)
  * [Файлы для справки](<#reference-files>)
  * [Работа с этим навыком](<#working-with-this-skill>)
    * [Для начинающих](<#for-beginners>)
    * [Для конкретных функций](<#for-specific-features>)
    * [Для примеров кода](<#for-code-examples>)
  * [Ресурсы](<#resources>)
    * [references/](<#references>)
    * [scripts/](<#scripts>)
    * [assets/](<#assets>)
  * [Заметки](<#notes>)
  * [Обновление](<#updating>)

<!-- Источник: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-pytorch-fsdp -->
