On this page

W&B: логирование ML экспериментов, sweeps, реестр моделей, дашборды.

## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")

|   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию) |
|Путь| `skills/mlops/evaluation/weights-and-biases` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `wandb` |
|Теги| `MLOps`, `Weights And Biases`, `WandB`, `Experiment Tracking`, `Hyperparameter Tuning`, `Model Registry`, `Collaboration`, `Real-Time Visualization`, `PyTorch`, `TensorFlow`, `HuggingFace` |

## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info

Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.

# Weights & Biases: ML Experiment Tracking & MLOps

## When to Use This Skill[​](<#when-to-use-this-skill> "Direct link to When to Use This Skill")

Используйте Weights & Biases (W&B), когда вам нужно:

  * **Отслеживать ML эксперименты** с автоматическим логированием метрик
  * **Визуализировать обучение** в реальном времени на дашбордах
  * **Сравнивать запуски** по гиперпараметрам и конфигурациям
  * **Оптимизировать гиперпараметры** с помощью автоматических sweeps
  * **Управлять реестром моделей** с версионированием и происхождением
  * **Совместно работать над ML проектами** в командных рабочих пространствах
  * **Отслеживать артефакты** (датасеты, модели, код) с происхождением



**Пользователи** : 200 000+ ML практиков | **GitHub Stars** : 10,5k+ | **Интеграции** : 100+

## Installation[​](<#installation> "Direct link to Installation")

[code] 
    # Install W&B  
    pip install wandb  
      
    # Login (creates API key)  
    wandb login  
      
    # Or set API key programmatically  
    export WANDB_API_KEY=your_api_key_here  
    
[/code]

## Quick Start[​](<#quick-start> "Direct link to Quick Start")

### Basic Experiment Tracking[​](<#basic-experiment-tracking> "Direct link to Basic Experiment Tracking")

[code] 
    import wandb  
      
    # Initialize a run  
    run = wandb.init(  
        project="my-project",  
        config={  
            "learning_rate": 0.001,  
            "epochs": 10,  
            "batch_size": 32,  
            "architecture": "ResNet50"  
        }  
    )  
      
    # Training loop  
    for epoch in range(run.config.epochs):  
        # Your training code  
        train_loss = train_epoch()  
        val_loss = validate()  
      
        # Log metrics  
        wandb.log({  
            "epoch": epoch,  
            "train/loss": train_loss,  
            "val/loss": val_loss,  
            "train/accuracy": train_acc,  
            "val/accuracy": val_acc  
        })  
      
    # Finish the run  
    wandb.finish()  
    
[/code]

### With PyTorch[​](<#with-pytorch> "Direct link to With PyTorch")

[code] 
    import torch  
    import wandb  
      
    # Initialize  
    wandb.init(project="pytorch-demo", config={  
        "lr": 0.001,  
        "epochs": 10  
    })  
      
    # Access config  
    config = wandb.config  
      
    # Training loop  
    for epoch in range(config.epochs):  
        for batch_idx, (data, target) in enumerate(train_loader):  
            # Forward pass  
            output = model(data)  
            loss = criterion(output, target)  
      
            # Backward pass  
            optimizer.zero_grad()  
            loss.backward()  
            optimizer.step()  
      
            # Log every 100 batches  
            if batch_idx % 100 == 0:  
                wandb.log({  
                    "loss": loss.item(),  
                    "epoch": epoch,  
                    "batch": batch_idx  
                })  
      
    # Save model  
    torch.save(model.state_dict(), "model.pth")  
    wandb.save("model.pth")  # Upload to W&B  
      
    wandb.finish()  
    
[/code]

## Core Concepts[​](<#core-concepts> "Direct link to Core Concepts")

### 1\. Projects and Runs[​](<#1-projects-and-runs> "Direct link to 1. Projects and Runs")

**Project** : Коллекция связанных экспериментов **Run** : Одно выполнение вашего тренировочного скрипта

[code] 
    # Create/use project  
    run = wandb.init(  
        project="image-classification",  
        name="resnet50-experiment-1",  # Optional run name  
        tags=["baseline", "resnet"],    # Organize with tags  
        notes="First baseline run"      # Add notes  
    )  
      
    # Each run has unique ID  
    print(f"Run ID: {run.id}")  
    print(f"Run URL: {run.url}")  
    
[/code]

### 2\. Configuration Tracking[​](<#2-configuration-tracking> "Direct link to 2. Configuration Tracking")

Отслеживайте гиперпараметры автоматически:

[code] 
    config = {  
        # Model architecture  
        "model": "ResNet50",  
        "pretrained": True,  
      
        # Training params  
        "learning_rate": 0.001,  
        "batch_size": 32,  
        "epochs": 50,  
        "optimizer": "Adam",  
      
        # Data params  
        "dataset": "ImageNet",  
        "augmentation": "standard"  
    }  
      
    wandb.init(project="my-project", config=config)  
      
    # Access config during training  
    lr = wandb.config.learning_rate  
    batch_size = wandb.config.batch_size  
    
[/code]

### 3\. Metric Logging[​](<#3-metric-logging> "Direct link to 3. Metric Logging")

[code] 
    # Log scalars  
    wandb.log({"loss": 0.5, "accuracy": 0.92})  
      
    # Log multiple metrics  
    wandb.log({  
        "train/loss": train_loss,  
        "train/accuracy": train_acc,  
        "val/loss": val_loss,  
        "val/accuracy": val_acc,  
        "learning_rate": current_lr,  
        "epoch": epoch  
    })  
      
    # Log with custom x-axis  
    wandb.log({"loss": loss}, step=global_step)  
      
    # Log media (images, audio, video)  
    wandb.log({"examples": [wandb.Image(img) for img in images]})  
      
    # Log histograms  
    wandb.log({"gradients": wandb.Histogram(gradients)})  
      
    # Log tables  
    table = wandb.Table(columns=["id", "prediction", "ground_truth"])  
    wandb.log({"predictions": table})  
    
[/code]

### 4\. Model Checkpointing[​](<#4-model-checkpointing> "Direct link to 4. Model Checkpointing")

[code] 
    import torch  
    import wandb  
      
    # Save model checkpoint  
    checkpoint = {  
        'epoch': epoch,  
        'model_state_dict': model.state_dict(),  
        'optimizer_state_dict': optimizer.state_dict(),  
        'loss': loss,  
    }  
      
    torch.save(checkpoint, 'checkpoint.pth')  
      
    # Upload to W&B  
    wandb.save('checkpoint.pth')  
      
    # Or use Artifacts (recommended)  
    artifact = wandb.Artifact('model', type='model')  
    artifact.add_file('checkpoint.pth')  
    wandb.log_artifact(artifact)  
    
[/code]

## Hyperparameter Sweeps[​](<#hyperparameter-sweeps> "Direct link to Hyperparameter Sweeps")

Автоматический поиск оптимальных гиперпараметров.

### Define Sweep Configuration[​](<#define-sweep-configuration> "Direct link to Define Sweep Configuration")

[code] 
    sweep_config = {  
        'method': 'bayes',  # or 'grid', 'random'  
        'metric': {  
            'name': 'val/accuracy',  
            'goal': 'maximize'  
        },  
        'parameters': {  
            'learning_rate': {  
                'distribution': 'log_uniform',  
                'min': 1e-5,  
                'max': 1e-1  
            },  
            'batch_size': {  
                'values': [16, 32, 64, 128]  
            },  
            'optimizer': {  
                'values': ['adam', 'sgd', 'rmsprop']  
            },  
            'dropout': {  
                'distribution': 'uniform',  
                'min': 0.1,  
                'max': 0.5  
            }  
        }  
    }  
      
    # Initialize sweep  
    sweep_id = wandb.sweep(sweep_config, project="my-project")  
    
[/code]

### Define Training Function[​](<#define-training-function> "Direct link to Define Training Function")

[code] 
    def train():  
        # Initialize run  
        run = wandb.init()  
      
        # Access sweep parameters  
        lr = wandb.config.learning_rate  
        batch_size = wandb.config.batch_size  
        optimizer_name = wandb.config.optimizer  
      
        # Build model with sweep config  
        model = build_model(wandb.config)  
        optimizer = get_optimizer(optimizer_name, lr)  
      
        # Training loop  
        for epoch in range(NUM_EPOCHS):  
            train_loss = train_epoch(model, optimizer, batch_size)  
            val_acc = validate(model)  
      
            # Log metrics  
            wandb.log({  
                "train/loss": train_loss,  
                "val/accuracy": val_acc  
            })  
      
    # Run sweep  
    wandb.agent(sweep_id, function=train, count=50)  # Run 50 trials  
    
[/code]

### Sweep Strategies[​](<#sweep-strategies> "Direct link to Sweep Strategies")

[code] 
    # Grid search - exhaustive  
    sweep_config = {  
        'method': 'grid',  
        'parameters': {  
            'lr': {'values': [0.001, 0.01, 0.1]},  
            'batch_size': {'values': [16, 32, 64]}  
        }  
    }  
      
    # Random search  
    sweep_config = {  
        'method': 'random',  
        'parameters': {  
            'lr': {'distribution': 'uniform', 'min': 0.0001, 'max': 0.1},  
            'dropout': {'distribution': 'uniform', 'min': 0.1, 'max': 0.5}  
        }  
    }  
      
    # Bayesian optimization (recommended)  
    sweep_config = {  
        'method': 'bayes',  
        'metric': {'name': 'val/loss', 'goal': 'minimize'},  
        'parameters': {  
            'lr': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1}  
        }  
    }  
    
[/code]

## Artifacts[​](<#artifacts> "Direct link to Artifacts")

Отслеживайте датасеты, модели и другие файлы с происхождением.

### Log Artifacts[​](<#log-artifacts> "Direct link to Log Artifacts")

[code] 
    # Create artifact  
    artifact = wandb.Artifact(  
        name='training-dataset',  
        type='dataset',  
        description='ImageNet training split',  
        metadata={'size': '1.2M images', 'split': 'train'}  
    )  
      
    # Add files  
    artifact.add_file('data/train.csv')  
    artifact.add_dir('data/images/')  
      
    # Log artifact  
    wandb.log_artifact(artifact)  
    
[/code]

### Use Artifacts[​](<#use-artifacts> "Direct link to Use Artifacts")

[code] 
    # Download and use artifact  
    run = wandb.init(project="my-project")  
      
    # Download artifact  
    artifact = run.use_artifact('training-dataset:latest')  
    artifact_dir = artifact.download()  
      
    # Use the data  
    data = load_data(f"{artifact_dir}/train.csv")  
    
[/code]

### Model Registry[​](<#model-registry> "Direct link to Model Registry")

[code] 
    # Log model as artifact  
    model_artifact = wandb.Artifact(  
        name='resnet50-model',  
        type='model',  
        metadata={'architecture': 'ResNet50', 'accuracy': 0.95}  
    )  
      
    model_artifact.add_file('model.pth')  
    wandb.log_artifact(model_artifact, aliases=['best', 'production'])  
      
    # Link to model registry  
    run.link_artifact(model_artifact, 'model-registry/production-models')  
    
[/code]

## Integration Examples[​](<#integration-examples> "Direct link to Integration Examples")

### HuggingFace Transformers[​](<#huggingface-transformers> "Direct link to HuggingFace Transformers")

[code] 
    from transformers import Trainer, TrainingArguments  
    import wandb  
      
    # Initialize W&B  
    wandb.init(project="hf-transformers")  
      
    # Training arguments with W&B  
    training_args = TrainingArguments(  
        output_dir="./results",  
        report_to="wandb",  # Enable W&B logging  
        run_name="bert-finetuning",  
        logging_steps=100,  
        save_steps=500  
    )  
      
    # Trainer automatically logs to W&B  
    trainer = Trainer(  
        model=model,  
        args=training_args,  
        train_dataset=train_dataset,  
        eval_dataset=eval_dataset  
    )  
      
    trainer.train()  
    
[/code]

### PyTorch Lightning[​](<#pytorch-lightning> "Direct link to PyTorch Lightning")

[code] 
    from pytorch_lightning import Trainer  
    from pytorch_lightning.loggers import WandbLogger  
    import wandb  
      
    # Create W&B logger  
    wandb_logger = WandbLogger(  
        project="lightning-demo",  
        log_model=True  # Log model checkpoints  
    )  
      
    # Use with Trainer  
    trainer = Trainer(  
        logger=wandb_logger,  
        max_epochs=10  
    )  
      
    trainer.fit(model, datamodule=dm)  
    
[/code]

### Keras/TensorFlow[​](<#kerastensorflow> "Direct link to Keras/TensorFlow")

[code] 
    import wandb  
    from wandb.keras import WandbCallback  
      
    # Initialize  
    wandb.init(project="keras-demo")  
      
    # Add callback  
    model.fit(  
        x_train, y_train,  
        validation_data=(x_val, y_val),  
        epochs=10,  
        callbacks=[WandbCallback()]  # Auto-logs metrics  
    )  
    
[/code]

## Visualization & Analysis[​](<#visualization--analysis> "Direct link to Visualization & Analysis")

### Custom Charts[​](<#custom-charts> "Direct link to Custom Charts")

[code] 
    # Log custom visualizations  
    import matplotlib.pyplot as plt  
      
    fig, ax = plt.subplots()  
    ax.plot(x, y)  
    wandb.log({"custom_plot": wandb.Image(fig)})  
      
    # Log confusion matrix  
    wandb.log({"conf_mat": wandb.plot.confusion_matrix(  
        probs=None,  
        y_true=ground_truth,  
        preds=predictions,  
        class_names=class_names  
    )})  
    
[/code]

### Reports[​](<#reports> "Direct link to Reports")

Создавайте доступные для общего доступа отчёты в интерфейсе W&B:

  * Объединение запусков, диаграмм и текста
  * Поддержка Markdown
  * Встраиваемые визуализации
  * Совместная работа в команде



## Best Practices[​](<#best-practices> "Direct link to Best Practices")

### 1\. Organize with Tags and Groups[​](<#1-organize-with-tags-and-groups> "Direct link to 1. Organize with Tags and Groups")

[code] 
    wandb.init(  
        project="my-project",  
        tags=["baseline", "resnet50", "imagenet"],  
        group="resnet-experiments",  # Group related runs  
        job_type="train"             # Type of job  
    )  
    
[/code]

### 2\. Log Everything Relevant[​](<#2-log-everything-relevant> "Direct link to 2. Log Everything Relevant")

[code] 
    # Log system metrics  
    wandb.log({  
        "gpu/util": gpu_utilization,  
        "gpu/memory": gpu_memory_used,  
        "cpu/util": cpu_utilization  
    })  
      
    # Log code version  
    wandb.log({"git_commit": git_commit_hash})  
      
    # Log data splits  
    wandb.log({  
        "data/train_size": len(train_dataset),  
        "data/val_size": len(val_dataset)  
    })  
    
[/code]

### 3\. Use Descriptive Names[​](<#3-use-descriptive-names> "Direct link to 3. Use Descriptive Names")

[code] 
    # ✅ Good: Descriptive run names  
    wandb.init(  
        project="nlp-classification",  
        name="bert-base-lr0.001-bs32-epoch10"  
    )  
      
    # ❌ Bad: Generic names  
    wandb.init(project="nlp", name="run1")  
    
[/code]

### 4\. Save Important Artifacts[​](<#4-save-important-artifacts> "Direct link to 4. Save Important Artifacts")

[code] 
    # Save final model  
    artifact = wandb.Artifact('final-model', type='model')  
    artifact.add_file('model.pth')  
    wandb.log_artifact(artifact)  
      
    # Save predictions for analysis  
    predictions_table = wandb.Table(  
        columns=["id", "input", "prediction", "ground_truth"],  
        data=predictions_data  
    )  
    wandb.log({"predictions": predictions_table})  
    
[/code]

### 5\. Use Offline Mode for Unstable Connections[​](<#5-use-offline-mode-for-unstable-connections> "Direct link to 5. Use Offline Mode for Unstable Connections")

[code] 
    import os  
      
    # Enable offline mode  
    os.environ["WANDB_MODE"] = "offline"  
      
    wandb.init(project="my-project")  
    # ... your code ...  
      
    # Sync later  
    # wandb sync <run_directory>  
    
[/code]

## Team Collaboration[​](<#team-collaboration> "Direct link to Team Collaboration")

### Share Runs[​](<#share-runs> "Direct link to Share Runs")

[code] 
    # Runs are automatically shareable via URL  
    run = wandb.init(project="team-project")  
    print(f"Share this URL: {run.url}")  
    
[/code]

### Team Projects[​](<#team-projects> "Direct link to Team Projects")

  * Создайте командный аккаунт на wandb.ai
  * Добавьте участников команды
  * Настройте видимость проекта (приватный/публичный)
  * Используйте командные артефакты и реестр моделей



## Pricing[​](<#pricing> "Direct link to Pricing")

  * **Free** : Неограниченное количество публичных проектов, 100 ГБ хранилища
  * **Academic** : Бесплатно для студентов/исследователей
  * **Teams** : $50/место/месяц, приватные проекты, безлимитное хранилище
  * **Enterprise** : Индивидуальное ценообразование, on-premise опции



## Resources[​](<#resources> "Direct link to Resources")

  * **Documentation** : <https://docs.wandb.ai>
  * **GitHub** : <https://github.com/wandb/wandb> (10,5k+ звезд)
  * **Examples** : <https://github.com/wandb/examples>
  * **Community** : <https://wandb.ai/community>
  * **Discord** : <https://wandb.me/discord>



## See Also[​](<#see-also> "Direct link to See Also")

  * `references/sweeps.md` — Полное руководство по оптимизации гиперпараметров
  * `references/artifacts.md` — Паттерны версионирования данных и моделей
  * `references/integrations.md` — Примеры для конкретных фреймворков



  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use This Skill](<#when-to-use-this-skill>)
  * [Installation](<#installation>)
  * [Quick Start](<#quick-start>)
    * [Basic Experiment Tracking](<#basic-experiment-tracking>)
    * [With PyTorch](<#with-pytorch>)
  * [Core Concepts](<#core-concepts>)
    * [1\. Projects and Runs](<#1-projects-and-runs>)
    * [2\. Configuration Tracking](<#2-configuration-tracking>)
    * [3\. Metric Logging](<#3-metric-logging>)
    * [4\. Model Checkpointing](<#4-model-checkpointing>)
  * [Hyperparameter Sweeps](<#hyperparameter-sweeps>)
    * [Define Sweep Configuration](<#define-sweep-configuration>)
    * [Define Training Function](<#define-training-function>)
    * [Sweep Strategies](<#sweep-strategies>)
  * [Artifacts](<#artifacts>)
    * [Log Artifacts](<#log-artifacts>)
    * [Use Artifacts](<#use-artifacts>)
    * [Model Registry](<#model-registry>)
  * [Integration Examples](<#integration-examples>)
    * [HuggingFace Transformers](<#huggingface-transformers>)
    * [PyTorch Lightning](<#pytorch-lightning>)
    * [Keras/TensorFlow](<#kerastensorflow>)
  * [Visualization & Analysis](<#visualization--analysis>)
    * [Custom Charts](<#custom-charts>)
    * [Reports](<#reports>)
  * [Best Practices](<#best-practices>)
    * [1\. Organize with Tags and Groups](<#1-organize-with-tags-and-groups>)
    * [2\. Log Everything Relevant](<#2-log-everything-relevant>)
    * [3\. Use Descriptive Names](<#3-use-descriptive-names>)
    * [4\. Save Important Artifacts](<#4-save-important-artifacts>)
    * [5\. Use Offline Mode for Unstable Connections](<#5-use-offline-mode-for-unstable-connections>)
  * [Team Collaboration](<#team-collaboration>)
    * [Share Runs](<#share-runs>)
    * [Team Projects](<#team-projects>)
  * [Pricing](<#pricing>)
  * [Resources](<#resources>)
  * [See Also](<#see-also>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-evaluation-weights-and-biases -->
