On this page

Высокоуровневый фреймворк PyTorch с классом Trainer, автоматическим распределённым обучением (DDP/FSDP/DeepSpeed), системой колбэков и минимальным шаблонным кодом. Масштабируется от ноутбука до суперкомпьютера на одном и том же коде. Используйте, когда нужны чистые тренировочные циклы со встроенными лучшими практиками.

## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")

|  
---|---  
Источник| Опционально — установка: `hermes skills install official/mlops/pytorch-lightning`  
Путь| `optional-skills/mlops/pytorch-lightning`  
Версия| `1.0.0`  
Автор| Orchestra Research  
Лицензия| MIT  
Зависимости| `lightning`, `torch`, `transformers`  
Теги| `PyTorch Lightning`, `Training Framework`, `Distributed Training`, `DDP`, `FSDP`, `DeepSpeed`, `High-Level API`, `Callbacks`, `Best Practices`, `Scalable`  

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# PyTorch Lightning — Высокоуровневый фреймворк для обучения

## Быстрый старт[​](<#quick-start> "Direct link to Quick start")

PyTorch Lightning организует код PyTorch, устраняя шаблонный код, сохраняя при этом гибкость.

**Установка**:

[code] 
    pip install lightning  
    
[/code]

**Преобразование PyTorch в Lightning** (3 шага):

[code] 
    import lightning as L  
    import torch  
    from torch import nn  
    from torch.utils.data import DataLoader, Dataset  
      
    # Шаг 1: Определите LightningModule (организуйте свой PyTorch-код)  
    class LitModel(L.LightningModule):  
        def __init__(self, hidden_size=128):  
            super().__init__()  
            self.model = nn.Sequential(  
                nn.Linear(28 * 28, hidden_size),  
                nn.ReLU(),  
                nn.Linear(hidden_size, 10)  
            )  
      
        def training_step(self, batch, batch_idx):  
            x, y = batch  
            y_hat = self.model(x)  
            loss = nn.functional.cross_entropy(y_hat, y)  
            self.log('train_loss', loss)  # Автоматически логируется в TensorBoard  
            return loss  
      
        def configure_optimizers(self):  
            return torch.optim.Adam(self.parameters(), lr=1e-3)  
      
    # Шаг 2: Создайте данные  
    train_loader = DataLoader(train_dataset, batch_size=32)  
      
    # Шаг 3: Обучайте с Trainer (он обрабатывает всё остальное!)  
    trainer = L.Trainer(max_epochs=10, accelerator='gpu', devices=2)  
    model = LitModel()  
    trainer.fit(model, train_loader)  
    
[/code]

**Вот и всё!** Trainer обрабатывает:

  * Переключение GPU/TPU/CPU
  * Распределённое обучение (DDP, FSDP, DeepSpeed)
  * Смешанную точность (FP16, BF16)
  * Накопление градиентов
  * Сохранение контрольных точек
  * Логирование
  * Индикаторы выполнения


## Типовые рабочие процессы[​](<#common-workflows> "Direct link to Common workflows")

### Процесс 1: От PyTorch к Lightning[​](<#workflow-1-from-pytorch-to-lightning> "Direct link to Workflow 1: From PyTorch to Lightning")

**Исходный код PyTorch**:

[code] 
    model = MyModel()  
    optimizer = torch.optim.Adam(model.parameters())  
    model.to('cuda')  
      
    for epoch in range(max_epochs):  
        for batch in train_loader:  
            batch = batch.to('cuda')  
            optimizer.zero_grad()  
            loss = model(batch)  
            loss.backward()  
            optimizer.step()  
    
[/code]

**Версия Lightning**:

[code] 
    class LitModel(L.LightningModule):  
        def __init__(self):  
            super().__init__()  
            self.model = MyModel()  
      
        def training_step(self, batch, batch_idx):  
            loss = self.model(batch)  # .to('cuda') не нужен!  
            return loss  
      
        def configure_optimizers(self):  
            return torch.optim.Adam(self.parameters())  
      
    # Обучение  
    trainer = L.Trainer(max_epochs=10, accelerator='gpu')  
    trainer.fit(LitModel(), train_loader)  
    
[/code]

**Преимущества**: 40+ строк → 15 строк, никакого управления устройствами, автоматическое распределённое обучение

### Процесс 2: Валидация и тестирование[​](<#workflow-2-validation-and-testing> "Direct link to Workflow 2: Validation and testing")

[code] 
    class LitModel(L.LightningModule):  
        def __init__(self):  
            super().__init__()  
            self.model = MyModel()  
      
        def training_step(self, batch, batch_idx):  
            x, y = batch  
            y_hat = self.model(x)  
            loss = nn.functional.cross_entropy(y_hat, y)  
            self.log('train_loss', loss)  
            return loss  
      
        def validation_step(self, batch, batch_idx):  
            x, y = batch  
            y_hat = self.model(x)  
            val_loss = nn.functional.cross_entropy(y_hat, y)  
            acc = (y_hat.argmax(dim=1) == y).float().mean()  
            self.log('val_loss', val_loss)  
            self.log('val_acc', acc)  
      
        def test_step(self, batch, batch_idx):  
            x, y = batch  
            y_hat = self.model(x)  
            test_loss = nn.functional.cross_entropy(y_hat, y)  
            self.log('test_loss', test_loss)  
      
        def configure_optimizers(self):  
            return torch.optim.Adam(self.parameters(), lr=1e-3)  
      
    # Обучение с валидацией  
    trainer = L.Trainer(max_epochs=10)  
    trainer.fit(model, train_loader, val_loader)  
      
    # Тестирование  
    trainer.test(model, test_loader)  
    
[/code]

**Автоматические возможности**:

  * Валидация выполняется каждую эпоху по умолчанию
  * Метрики логируются в TensorBoard
  * Сохранение лучшей модели на основе val_loss


### Процесс 3: Распределённое обучение (DDP)[​](<#workflow-3-distributed-training-ddp> "Direct link to Workflow 3: Distributed training (DDP)")

[code] 
    # Тот же код, что и для одного GPU!  
    model = LitModel()  
      
    # 8 GPU с DDP (автоматически!)  
    trainer = L.Trainer(  
        accelerator='gpu',  
        devices=8,  
        strategy='ddp'  # Или 'fsdp', 'deepspeed'  
    )  
      
    trainer.fit(model, train_loader)  
    
[/code]

**Запуск**:

[code] 
    # Одна команда, Lightning делает всё остальное  
    python train.py  
    
[/code]

**Никаких изменений не требуется**:

  * Автоматическое распределение данных
  * Синхронизация градиентов
  * Поддержка нескольких узлов (просто укажите `num_nodes=2`)


### Процесс 4: Колбэки для мониторинга[​](<#workflow-4-callbacks-for-monitoring> "Direct link to Workflow 4: Callbacks for monitoring")

[code] 
    from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor  
      
    # Создание колбэков  
    checkpoint = ModelCheckpoint(  
        monitor='val_loss',  
        mode='min',  
        save_top_k=3,  
        filename='model-{epoch:02d}-{val_loss:.2f}'  
    )  
      
    early_stop = EarlyStopping(  
        monitor='val_loss',  
        patience=5,  
        mode='min'  
    )  
      
    lr_monitor = LearningRateMonitor(logging_interval='epoch')  
      
    # Добавление в Trainer  
    trainer = L.Trainer(  
        max_epochs=100,  
        callbacks=[checkpoint, early_stop, lr_monitor]  
    )  
      
    trainer.fit(model, train_loader, val_loader)  
    
[/code]

**Результат**:

  * Автосохранение 3 лучших моделей
  * Досрочная остановка, если нет улучшений в течение 5 эпох
  * Логирование скорости обучения в TensorBoard


### Процесс 5: Планирование скорости обучения[​](<#workflow-5-learning-rate-scheduling> "Direct link to Workflow 5: Learning rate scheduling")

[code] 
    class LitModel(L.LightningModule):  
        # ... (training_step, и т.д.)  
      
        def configure_optimizers(self):  
            optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)  
      
            # Cosine annealing  
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(  
                optimizer,  
                T_max=100,  
                eta_min=1e-5  
            )  
      
            return {  
                'optimizer': optimizer,  
                'lr_scheduler': {  
                    'scheduler': scheduler,  
                    'interval': 'epoch',  # Обновление каждую эпоху  
                    'frequency': 1  
                }  
            }  
      
    # Скорость обучения логируется автоматически!  
    trainer = L.Trainer(max_epochs=100)  
    trainer.fit(model, train_loader)  
    
[/code]

## Когда использовать и сравнение с альтернативами[​](<#when-to-use-vs-alternatives> "Direct link to When to use vs alternatives")

**Используйте PyTorch Lightning, когда**:

  * Нужен чистый, организованный код
  * Требуются готовые к продакшену тренировочные циклы
  * Переключаетесь между одним GPU, несколькими GPU и TPU
  * Нужны встроенные колбэки и логирование
  * Работаете в команде (стандартизированная структура)


**Ключевые преимущества**:

  * **Организованность**: Отделяет исследовательский код от инженерного
  * **Автоматизация**: DDP, FSDP, DeepSpeed одной строкой
  * **Колбэки**: Модульные расширения для обучения
  * **Воспроизводимость**: Меньше шаблонного кода = меньше ошибок
  * **Проверен**: 1M+ загрузок в месяц, проверен в бою


**Используйте альтернативы вместо этого**:

  * **Accelerate**: Минимальные изменения существующего кода, больше гибкости
  * **Ray Train**: Оркестрация на нескольких узлах, настройка гиперпараметров
  * **Чистый PyTorch**: Максимальный контроль, в учебных целях
  * **Keras**: Экосистема TensorFlow


## Часто встречающиеся проблемы[​](<#common-issues> "Direct link to Common issues")

**Проблема: Loss не уменьшается**

Проверьте данные и настройку модели:

[code] 
    # Добавьте в training_step  
    def training_step(self, batch, batch_idx):  
        if batch_idx == 0:  
            print(f"Batch shape: {batch[0].shape}")  
            print(f"Labels: {batch[1]}")  
        loss = ...  
        return loss  
    
[/code]

**Проблема: Не хватает памяти**

Уменьшите размер батча или используйте накопление градиентов:

[code] 
    trainer = L.Trainer(  
        accumulate_grad_batches=4,  # Эффективный батч = batch_size × 4  
        precision='bf16'  # Или 'fp16', уменьшает потребление памяти на 50%  
    )  
    
[/code]

**Проблема: Валидация не запускается**

Убедитесь, что вы передаёте val_loader:

[code] 
    # НЕПРАВИЛЬНО  
    trainer.fit(model, train_loader)  
      
    # ПРАВИЛЬНО  
    trainer.fit(model, train_loader, val_loader)  
    
[/code]

**Проблема: DDP неожиданно порождает несколько процессов**

Lightning автоматически определяет GPU. Явно укажите устройства:

[code] 
    # Сначала тест на CPU  
    trainer = L.Trainer(accelerator='cpu', devices=1)  
      
    # Затем GPU  
    trainer = L.Trainer(accelerator='gpu', devices=1)  
    
[/code]

## Продвинутые темы[​](<#advanced-topics> "Direct link to Advanced topics")

**Колбэки**: См. [references/callbacks.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/pytorch-lightning/references/callbacks.md>) для EarlyStopping, ModelCheckpoint, пользовательских колбэков и хуков колбэков.

**Стратегии распределённого обучения**: См. [references/distributed.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/pytorch-lightning/references/distributed.md>) для DDP, FSDP, интеграции DeepSpeed ZeRO, настройки нескольких узлов.

**Настройка гиперпараметров**: См. [references/hyperparameter-tuning.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/pytorch-lightning/references/hyperparameter-tuning.md>) для интеграции с Optuna, Ray Tune и WandB sweeps.

## Требования к оборудованию[​](<#hardware-requirements> "Direct link to Hardware requirements")

  * **CPU**: Работает (хорошо для отладки)
  * **Один GPU**: Работает
  * **Несколько GPU**: DDP (по умолчанию), FSDP или DeepSpeed
  * **Несколько узлов**: DDP, FSDP, DeepSpeed
  * **TPU**: Поддерживается (8 ядер)
  * **Apple MPS**: Поддерживается


**Варианты точности**:

  * FP32 (по умолчанию)
  * FP16 (V100, старые GPU)
  * BF16 (A100/H100, рекомендуется)
  * FP8 (H100)


## Ресурсы[​](<#resources> "Direct link to Resources")

  * Документация: <https://lightning.ai/docs/pytorch/stable/>
  * GitHub: <https://github.com/Lightning-AI/pytorch-lightning> ⭐ 29,000+
  * Версия: 2.5.5+
  * Примеры: <https://github.com/Lightning-AI/pytorch-lightning/tree/master/examples>
  * Discord: <https://discord.gg/lightning-ai>
  * Используется: победителями Kaggle, исследовательскими лабораториями, продакшен-командами


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Быстрый старт](<#quick-start>)
  * [Типовые рабочие процессы](<#common-workflows>)
    * [Процесс 1: От PyTorch к Lightning](<#workflow-1-from-pytorch-to-lightning>)
    * [Процесс 2: Валидация и тестирование](<#workflow-2-validation-and-testing>)
    * [Процесс 3: Распределённое обучение (DDP)](<#workflow-3-distributed-training-ddp>)
    * [Процесс 4: Колбэки для мониторинга](<#workflow-4-callbacks-for-monitoring>)
    * [Процесс 5: Планирование скорости обучения](<#workflow-5-learning-rate-scheduling>)
  * [Когда использовать и сравнение с альтернативами](<#when-to-use-vs-alternatives>)
  * [Часто встречающиеся проблемы](<#common-issues>)
  * [Продвинутые темы](<#advanced-topics>)
  * [Требования к оборудованию](<#hardware-requirements>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-pytorch-lightning -->
