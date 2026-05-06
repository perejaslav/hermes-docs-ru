On this page
Зарезервированные и по требованию облачные GPU-инстансы для ML-обучения и инференса. Используйте, когда вам нужны выделенные GPU-инстансы с простым SSH-доступом, постоянными файловыми системами или высокопроизводительными многоузловыми кластерами для крупномасштабного обучения.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
|Source| Опционально — установка: `hermes skills install official/mlops/lambda-labs`  |
|Path| `optional-skills/mlops/lambda-labs`  |
|Version| `1.0.0`  |
|Author| Orchestra Research  |
|License| MIT  |
|Dependencies| `lambda-cloud-client>=1.0.0`  |
|Tags| `Infrastructure`, `GPU Cloud`, `Training`, `Inference`, `Lambda Labs`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Lambda Labs GPU Cloud
Полное руководство по запуску ML-нагрузок на GPU-облаке Lambda Labs с инстансами по требованию и 1-Click Clusters.
## When to use Lambda Labs[​](<#when-to-use-lambda-labs> "Direct link to When to use Lambda Labs")
**Используйте Lambda Labs когда:**
  * Нужны выделенные GPU-инстансы с полным SSH-доступом
  * Запускаете длительные задачи обучения (часы до дней)
  * Нужно простое ценообразование без платы за исходящий трафик
  * Требуется постоянное хранилище между сессиями
  * Нужны высокопроизводительные многоузловые кластеры (16-512 GPU)
  * Нужен предустановленный ML-стек (Lambda Stack с PyTorch, CUDA, NCCL)


**Ключевые возможности:**
  * **Разнообразие GPU** : B200, H100, GH200, A100, A10, A6000, V100
  * **Lambda Stack** : Предустановленные PyTorch, TensorFlow, CUDA, cuDNN, NCCL
  * **Постоянные файловые системы** : Сохраняйте данные между перезапусками инстансов
  * **1-Click Clusters** : Slurm-кластеры на 16-512 GPU с InfiniBand
  * **Простое ценообразование** : Оплата за минуту, без платы за исходящий трафик
  * **Глобальные регионы** : 12+ регионов по всему миру


**Вместо этого используйте альтернативы:**
  * **Modal** : Для бессерверных, автоматически масштабируемых нагрузок
  * **SkyPilot** : Для мультиоблачной оркестрации и оптимизации затрат
  * **RunPod** : Для более дешёвых spot-инстансов и бессерверных эндпоинтов
  * **Vast.ai** : Для маркетплейса GPU с самыми низкими ценами


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Account setup[​](<#account-setup> "Direct link to Account setup")
  1. Создайте аккаунт на <https://lambda.ai>
  2. Добавьте способ оплаты
  3. Сгенерируйте API-ключ в панели управления
  4. Добавьте SSH-ключ (требуется перед запуском инстансов)


### Launch via console[​](<#launch-via-console> "Direct link to Launch via console")
  1. Перейдите на <https://cloud.lambda.ai/instances>
  2. Нажмите «Launch instance»
  3. Выберите тип GPU и регион
  4. Выберите SSH-ключ
  5. Опционально подключите файловую систему
  6. Запустите и подождите 3-15 минут


### Connect via SSH[​](<#connect-via-ssh> "Direct link to Connect via SSH")
[code] 
    # Get instance IP from console  
    ssh ubuntu@<INSTANCE-IP>  
      
    # Or with specific key  
    ssh -i ~/.ssh/lambda_key ubuntu@<INSTANCE-IP>  
    
[/code]
## GPU instances[​](<#gpu-instances> "Direct link to GPU instances")
### Available GPUs[​](<#available-gpus> "Direct link to Available GPUs")
GPU| VRAM| Цена/GPU/ч| Лучше всего для  
---|---|---|---|---  
B200 SXM6| 180 GB| $4.99| Крупнейшие модели, самое быстрое обучение  
H100 SXM| 80 GB| $2.99-3.29| Обучение больших моделей  
H100 PCIe| 80 GB| $2.49| Экономичный H100  
GH200| 96 GB| $1.49| Крупные модели на одном GPU  
A100 80GB| 80 GB| $1.79| Продакшн-обучение  
A100 40GB| 40 GB| $1.29| Стандартное обучение  
A10| 24 GB| $0.75| Инференс, тонкая настройка  
A6000| 48 GB| $0.80| Хорошее соотношение VRAM/цена  
V100| 16 GB| $0.55| Бюджетное обучение  
### Instance configurations[​](<#instance-configurations> "Direct link to Instance configurations")
[code] 
    8x GPU: Best for distributed training (DDP, FSDP)  
    4x GPU: Large models, multi-GPU training  
    2x GPU: Medium workloads  
    1x GPU: Fine-tuning, inference, development  
    
[/code]
### Launch times[​](<#launch-times> "Direct link to Launch times")
  * Один GPU: 3-5 минут
  * Несколько GPU: 10-15 минут


## Lambda Stack[​](<#lambda-stack> "Direct link to Lambda Stack")
Все инстансы поставляются с предустановленным Lambda Stack:
[code] 
    # Included software  
    - Ubuntu 22.04 LTS  
    - NVIDIA drivers (latest)  
    - CUDA 12.x  
    - cuDNN 8.x  
    - NCCL (for multi-GPU)  
    - PyTorch (latest)  
    - TensorFlow (latest)  
    - JAX  
    - JupyterLab  
    
[/code]
### Verify installation[​](<#verify-installation> "Direct link to Verify installation")
[code] 
    # Check GPU  
    nvidia-smi  
      
    # Check PyTorch  
    python -c "import torch; print(torch.cuda.is_available())"  
      
    # Check CUDA version  
    nvcc --version  
    
[/code]
## Python API[​](<#python-api> "Direct link to Python API")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    pip install lambda-cloud-client  
    
[/code]
### Authentication[​](<#authentication> "Direct link to Authentication")
[code] 
    import os  
    import lambda_cloud_client  
      
    # Configure with API key  
    configuration = lambda_cloud_client.Configuration(  
        host="https://cloud.lambdalabs.com/api/v1",  
        access_token=os.environ["LAMBDA_API_KEY"]  
    )  
    
[/code]
### List available instances[​](<#list-available-instances> "Direct link to List available instances")
[code] 
    with lambda_cloud_client.ApiClient(configuration) as api_client:  
        api = lambda_cloud_client.DefaultApi(api_client)  
      
        # Get available instance types  
        types = api.instance_types()  
        for name, info in types.data.items():  
            print(f"{name}: {info.instance_type.description}")  
    
[/code]
### Launch instance[​](<#launch-instance> "Direct link to Launch instance")
[code] 
    from lambda_cloud_client.models import LaunchInstanceRequest  
      
    request = LaunchInstanceRequest(  
        region_name="us-west-1",  
        instance_type_name="gpu_1x_h100_sxm5",  
        ssh_key_names=["my-ssh-key"],  
        file_system_names=["my-filesystem"],  # Optional  
        name="training-job"  
    )  
      
    response = api.launch_instance(request)  
    instance_id = response.data.instance_ids[0]  
    print(f"Launched: {instance_id}")  
    
[/code]
### List running instances[​](<#list-running-instances> "Direct link to List running instances")
[code] 
    instances = api.list_instances()  
    for instance in instances.data:  
        print(f"{instance.name}: {instance.ip} ({instance.status})")  
    
[/code]
### Terminate instance[​](<#terminate-instance> "Direct link to Terminate instance")
[code] 
    from lambda_cloud_client.models import TerminateInstanceRequest  
      
    request = TerminateInstanceRequest(  
        instance_ids=[instance_id]  
    )  
    api.terminate_instance(request)  
    
[/code]
### SSH key management[​](<#ssh-key-management> "Direct link to SSH key management")
[code] 
    from lambda_cloud_client.models import AddSshKeyRequest  
      
    # Add SSH key  
    request = AddSshKeyRequest(  
        name="my-key",  
        public_key="ssh-rsa AAAA..."  
    )  
    api.add_ssh_key(request)  
      
    # List keys  
    keys = api.list_ssh_keys()  
      
    # Delete key  
    api.delete_ssh_key(key_id)  
    
[/code]
## CLI with curl[​](<#cli-with-curl> "Direct link to CLI with curl")
### List instance types[​](<#list-instance-types> "Direct link to List instance types")
[code] 
    curl -u $LAMBDA_API_KEY: \  
      https://cloud.lambdalabs.com/api/v1/instance-types | jq  
    
[/code]
### Launch instance[​](<#launch-instance-1> "Direct link to Launch instance")
[code] 
    curl -u $LAMBDA_API_KEY: \  
      -X POST https://cloud.lambdalabs.com/api/v1/instance-operations/launch \  
      -H "Content-Type: application/json" \  
      -d '{  
        "region_name": "us-west-1",  
        "instance_type_name": "gpu_1x_h100_sxm5",  
        "ssh_key_names": ["my-key"]  
      }' | jq  
    
[/code]
### Terminate instance[​](<#terminate-instance-1> "Direct link to Terminate instance")
[code] 
    curl -u $LAMBDA_API_KEY: \  
      -X POST https://cloud.lambdalabs.com/api/v1/instance-operations/terminate \  
      -H "Content-Type: application/json" \  
      -d '{"instance_ids": ["<INSTANCE-ID>"]}' | jq  
    
[/code]
## Persistent storage[​](<#persistent-storage> "Direct link to Persistent storage")
### Filesystems[​](<#filesystems> "Direct link to Filesystems")
Файловые системы сохраняют данные между перезапусками инстансов:
[code] 
    # Mount location  
    /lambda/nfs/<FILESYSTEM_NAME>  
      
    # Example: save checkpoints  
    python train.py --checkpoint-dir /lambda/nfs/my-storage/checkpoints  
    
[/code]
### Create filesystem[​](<#create-filesystem> "Direct link to Create filesystem")
  1. Перейдите в раздел Storage в консоли Lambda
  2. Нажмите «Create filesystem»
  3. Выберите регион (должен совпадать с регионом инстанса)
  4. Дайте имя и создайте


### Attach to instance[​](<#attach-to-instance> "Direct link to Attach to instance")
Файловые системы должны быть подключены при запуске инстанса:
  * Через консоль: Выберите файловую систему при запуске
  * Через API: Укажите `file_system_names` в запросе запуска


### Best practices[​](<#best-practices> "Direct link to Best practices")
[code] 
    # Store on filesystem (persists)  
    /lambda/nfs/storage/  
      ├── datasets/  
      ├── checkpoints/  
      ├── models/  
      └── outputs/  
      
    # Local SSD (faster, ephemeral)  
    /home/ubuntu/  
      └── working/  # Temporary files  
    
[/code]
## SSH configuration[​](<#ssh-configuration> "Direct link to SSH configuration")
### Add SSH key[​](<#add-ssh-key> "Direct link to Add SSH key")
[code] 
    # Generate key locally  
    ssh-keygen -t ed25519 -f ~/.ssh/lambda_key  
      
    # Add public key to Lambda console  
    # Or via API  
    
[/code]
### Multiple keys[​](<#multiple-keys> "Direct link to Multiple keys")
[code] 
    # On instance, add more keys  
    echo 'ssh-rsa AAAA...' >> ~/.ssh/authorized_keys  
    
[/code]
### Import from GitHub[​](<#import-from-github> "Direct link to Import from GitHub")
[code] 
    # On instance  
    ssh-import-id gh:username  
    
[/code]
### SSH tunneling[​](<#ssh-tunneling> "Direct link to SSH tunneling")
[code] 
    # Forward Jupyter  
    ssh -L 8888:localhost:8888 ubuntu@<IP>  
      
    # Forward TensorBoard  
    ssh -L 6006:localhost:6006 ubuntu@<IP>  
      
    # Multiple ports  
    ssh -L 8888:localhost:8888 -L 6006:localhost:6006 ubuntu@<IP>  
    
[/code]
## JupyterLab[​](<#jupyterlab> "Direct link to JupyterLab")
### Launch from console[​](<#launch-from-console> "Direct link to Launch from console")
  1. Перейдите на страницу Instances
  2. Нажмите «Launch» в колонке Cloud IDE
  3. JupyterLab откроется в браузере


### Manual access[​](<#manual-access> "Direct link to Manual access")
[code] 
    # On instance  
    jupyter lab --ip=0.0.0.0 --port=8888  
      
    # From local machine with tunnel  
    ssh -L 8888:localhost:8888 ubuntu@<IP>  
    # Open http://localhost:8888  
    
[/code]
## Training workflows[​](<#training-workflows> "Direct link to Training workflows")
### Single-GPU training[​](<#single-gpu-training> "Direct link to Single-GPU training")
[code] 
    # SSH to instance  
    ssh ubuntu@<IP>  
      
    # Clone repo  
    git clone https://github.com/user/project  
    cd project  
      
    # Install dependencies  
    pip install -r requirements.txt  
      
    # Train  
    python train.py --epochs 100 --checkpoint-dir /lambda/nfs/storage/checkpoints  
    
[/code]
### Multi-GPU training (single node)[​](<#multi-gpu-training-single-node> "Direct link to Multi-GPU training (single node)")
[code] 
    # train_ddp.py  
    import torch  
    import torch.distributed as dist  
    from torch.nn.parallel import DistributedDataParallel as DDP  
      
    def main():  
        dist.init_process_group("nccl")  
        rank = dist.get_rank()  
        device = rank % torch.cuda.device_count()  
      
        model = MyModel().to(device)  
        model = DDP(model, device_ids=[device])  
      
        # Training loop...  
      
    if __name__ == "__main__":  
        main()  
    
[/code]
[code] 
    # Launch with torchrun (8 GPUs)  
    torchrun --nproc_per_node=8 train_ddp.py  
    
[/code]
### Checkpoint to filesystem[​](<#checkpoint-to-filesystem> "Direct link to Checkpoint to filesystem")
[code] 
    import os  
      
    checkpoint_dir = "/lambda/nfs/my-storage/checkpoints"  
    os.makedirs(checkpoint_dir, exist_ok=True)  
      
    # Save checkpoint  
    torch.save({  
        'epoch': epoch,  
        'model_state_dict': model.state_dict(),  
        'optimizer_state_dict': optimizer.state_dict(),  
        'loss': loss,  
    }, f"{checkpoint_dir}/checkpoint_{epoch}.pt")  
    
[/code]
## 1-Click Clusters[​](<#1-click-clusters> "Direct link to 1-Click Clusters")
### Overview[​](<#overview> "Direct link to Overview")
Высокопроизводительные Slurm-кластеры с:
  * 16-512 NVIDIA H100 или B200 GPU
  * NVIDIA Quantum-2 400 Gb/s InfiniBand
  * GPUDirect RDMA на 3200 Gb/s
  * Предустановленным распределённым ML-стеком


### Included software[​](<#included-software> "Direct link to Included software")
  * Ubuntu 22.04 LTS + Lambda Stack
  * NCCL, Open MPI
  * PyTorch с DDP и FSDP
  * TensorFlow
  * OFED драйверы


### Storage[​](<#storage> "Direct link to Storage")
  * 24 ТБ NVMe на вычислительный узел (эфемерное)
  * Файловые системы Lambda для постоянных данных


### Multi-node training[​](<#multi-node-training> "Direct link to Multi-node training")
[code] 
    # On Slurm cluster  
    srun --nodes=4 --ntasks-per-node=8 --gpus-per-node=8 \  
      torchrun --nnodes=4 --nproc_per_node=8 \  
      --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:29500 \  
      train.py  
    
[/code]
## Networking[​](<#networking> "Direct link to Networking")
### Bandwidth[​](<#bandwidth> "Direct link to Bandwidth")
  * Между инстансами (один регион): до 200 Gbps
  * Исходящий интернет: макс. 20 Gbps


### Firewall[​](<#firewall> "Direct link to Firewall")
  * По умолчанию: Открыт только порт 22 (SSH)
  * Настройте дополнительные порты в консоли Lambda
  * ICMP-трафик разрешён по умолчанию


### Private IPs[​](<#private-ips> "Direct link to Private IPs")
[code] 
    # Find private IP  
    ip addr show | grep 'inet '  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: Fine-tuning LLM[​](<#workflow-1-fine-tuning-llm> "Direct link to Workflow 1: Fine-tuning LLM")
[code] 
    # 1. Launch 8x H100 instance with filesystem  
      
    # 2. SSH and setup  
    ssh ubuntu@<IP>  
    pip install transformers accelerate peft  
      
    # 3. Download model to filesystem  
    python -c "  
    from transformers import AutoModelForCausalLM  
    model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf')  
    model.save_pretrained('/lambda/nfs/storage/models/llama-2-7b')  
    "  
      
    # 4. Fine-tune with checkpoints on filesystem  
    accelerate launch --num_processes 8 train.py \  
      --model_path /lambda/nfs/storage/models/llama-2-7b \  
      --output_dir /lambda/nfs/storage/outputs \  
      --checkpoint_dir /lambda/nfs/storage/checkpoints  
    
[/code]
### Workflow 2: Batch inference[​](<#workflow-2-batch-inference> "Direct link to Workflow 2: Batch inference")
[code] 
    # 1. Launch A10 instance (cost-effective for inference)  
      
    # 2. Run inference  
    python inference.py \  
      --model /lambda/nfs/storage/models/fine-tuned \  
      --input /lambda/nfs/storage/data/inputs.jsonl \  
      --output /lambda/nfs/storage/data/outputs.jsonl  
    
[/code]
## Cost optimization[​](<#cost-optimization> "Direct link to Cost optimization")
### Choose right GPU[​](<#choose-right-gpu> "Direct link to Choose right GPU")
Задача| Рекомендуемый GPU  
---|---  
Тонкая настройка LLM (7B)| A100 40GB  
Тонкая настройка LLM (70B)| 8x H100  
Инференс| A10, A6000  
Разработка| V100, A10  
Максимальная производительность| B200  
### Reduce costs[​](<#reduce-costs> "Direct link to Reduce costs")
  1. **Используйте файловые системы** : Избегайте повторной загрузки данных
  2. **Сохраняйте контрольные точки часто** : Возобновляйте прерванное обучение
  3. **Правильный размер** : Не выделяйте лишних GPU
  4. **Завершайте простаивающие** : Нет автоостановки, завершайте вручную


### Monitor usage[​](<#monitor-usage> "Direct link to Monitor usage")
  * Панель управления показывает загрузку GPU в реальном времени
  * API для программного мониторинга


## Common issues[​](<#common-issues> "Direct link to Common issues")
Проблема| Решение  
---|---  
Инстанс не запускается| Проверьте доступность региона, попробуйте другой GPU  
SSH-соединение отклонено| Подождите инициализации инстанса (3-15 мин)  
Данные потеряны после завершения| Используйте постоянные файловые системы  
Медленная передача данных| Используйте файловую систему в том же регионе  
GPU не обнаружен| Перезагрузите инстанс, проверьте драйверы  
## References[​](<#references> "Direct link to References")
  * **[Advanced Usage](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/lambda-labs/references/advanced-usage.md>)** \\- Многоузловое обучение, автоматизация через API
  * **[Troubleshooting](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/lambda-labs/references/troubleshooting.md>)** \\- Частые проблемы и решения


## Resources[​](<#resources> "Direct link to Resources")
  * **Документация** : <https://docs.lambda.ai>
  * **Консоль** : <https://cloud.lambda.ai>
  * **Цены** : <https://lambda.ai/instances>
  * **Поддержка** : <https://support.lambdalabs.com>
  * **Блог** : <https://lambda.ai/blog>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use Lambda Labs](<#when-to-use-lambda-labs>)
  * [Quick start](<#quick-start>)
    * [Account setup](<#account-setup>)
    * [Launch via console](<#launch-via-console>)
    * [Connect via SSH](<#connect-via-ssh>)
  * [GPU instances](<#gpu-instances>)
    * [Available GPUs](<#available-gpus>)
    * [Instance configurations](<#instance-configurations>)
    * [Launch times](<#launch-times>)
  * [Lambda Stack](<#lambda-stack>)
    * [Verify installation](<#verify-installation>)
  * [Python API](<#python-api>)
    * [Installation](<#installation>)
    * [Authentication](<#authentication>)
    * [List available instances](<#list-available-instances>)
    * [Launch instance](<#launch-instance>)
    * [List running instances](<#list-running-instances>)
    * [Terminate instance](<#terminate-instance>)
    * [SSH key management](<#ssh-key-management>)
  * [CLI with curl](<#cli-with-curl>)
    * [List instance types](<#list-instance-types>)
    * [Launch instance](<#launch-instance-1>)
    * [Terminate instance](<#terminate-instance-1>)
  * [Persistent storage](<#persistent-storage>)
    * [Filesystems](<#filesystems>)
    * [Create filesystem](<#create-filesystem>)
    * [Attach to instance](<#attach-to-instance>)
    * [Best practices](<#best-practices>)
  * [SSH configuration](<#ssh-configuration>)
    * [Add SSH key](<#add-ssh-key>)
    * [Multiple keys](<#multiple-keys>)
    * [Import from GitHub](<#import-from-github>)
    * [SSH tunneling](<#ssh-tunneling>)
  * [JupyterLab](<#jupyterlab>)
    * [Launch from console](<#launch-from-console>)
    * [Manual access](<#manual-access>)
  * [Training workflows](<#training-workflows>)
    * [Single-GPU training](<#single-gpu-training>)
    * [Multi-GPU training (single node)](<#multi-gpu-training-single-node>)
    * [Checkpoint to filesystem](<#checkpoint-to-filesystem>)
  * [1-Click Clusters](<#1-click-clusters>)
    * [Overview](<#overview>)
    * [Included software](<#included-software>)
    * [Storage](<#storage>)
    * [Multi-node training](<#multi-node-training>)
  * [Networking](<#networking>)
    * [Bandwidth](<#bandwidth>)
    * [Firewall](<#firewall>)
    * [Private IPs](<#private-ips>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: Fine-tuning LLM](<#workflow-1-fine-tuning-llm>)
    * [Workflow 2: Batch inference](<#workflow-2-batch-inference>)
  * [Cost optimization](<#cost-optimization>)
    * [Choose right GPU](<#choose-right-gpu>)
    * [Reduce costs](<#reduce-costs>)
    * [Monitor usage](<#monitor-usage>)
  * [Common issues](<#common-issues>)
  * [References](<#references>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-lambda-labs -->
