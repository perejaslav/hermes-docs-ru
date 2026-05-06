On this page
Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance (+6.4 points on AlpacaEval 2.0). No reference model needed, more efficient than DPO. Use for preference alignment when want simpler, faster training than DPO/PPO.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/simpo`  
Path| `optional-skills/mlops/simpo`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `torch`, `transformers`, `datasets`, `trl`, `accelerate`  
Tags| `Post-Training`, `SimPO`, `Preference Optimization`, `Alignment`, `DPO Alternative`, `Reference-Free`, `LLM Alignment`, `Efficient Training`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# SimPO - Simple Preference Optimization
## Quick start[​](<#quick-start> "Direct link to Quick start")
SimPO is a reference-free preference optimization method that outperforms DPO without needing a reference model.
**Installation** :
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
**Training** (Mistral 7B):
[code] 
    ACCELERATE_LOG_LEVEL=info accelerate launch \  
      --config_file accelerate_configs/deepspeed_zero3.yaml \  
      scripts/run_simpo.py \  
      training_configs/mistral-7b-base-simpo.yaml  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: Train from base model (Mistral 7B)[​](<#workflow-1-train-from-base-model-mistral-7b> "Direct link to Workflow 1: Train from base model \(Mistral 7B\)")
**Config** (`mistral-7b-base-simpo.yaml`):
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
    beta: 2.0                  # Reward scaling (2.0-10.0)  
    gamma_beta_ratio: 0.5       # Target margin (0-1)  
    loss_type: sigmoid          # sigmoid or hinge  
    sft_weight: 0.0             # Optional SFT regularization  
      
    # Training  
    learning_rate: 5e-7         # Critical: 3e-7 to 1e-6  
    num_train_epochs: 1  
    per_device_train_batch_size: 1  
    gradient_accumulation_steps: 8  
      
    # Output  
    output_dir: ./outputs/mistral-7b-simpo  
    
[/code]
**Launch training** :
[code] 
    accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \  
      scripts/run_simpo.py training_configs/mistral-7b-base-simpo.yaml  
    
[/code]
### Workflow 2: Fine-tune instruct model (Llama 3 8B)[​](<#workflow-2-fine-tune-instruct-model-llama-3-8b> "Direct link to Workflow 2: Fine-tune instruct model \(Llama 3 8B\)")
**Config** (`llama3-8b-instruct-simpo.yaml`):
[code] 
    model_name_or_path: meta-llama/Meta-Llama-3-8B-Instruct  
      
    dataset_mixer:  
      argilla/ultrafeedback-binarized-preferences-cleaned: 1.0  
      
    beta: 2.5  
    gamma_beta_ratio: 0.5  
    learning_rate: 5e-7  
    sft_weight: 0.1             # Add SFT loss to preserve capabilities  
      
    num_train_epochs: 1  
    per_device_train_batch_size: 2  
    gradient_accumulation_steps: 4  
    output_dir: ./outputs/llama3-8b-simpo  
    
[/code]
**Launch** :
[code] 
    accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \  
      scripts/run_simpo.py training_configs/llama3-8b-instruct-simpo.yaml  
    
[/code]
### Workflow 3: Reasoning-intensive tasks (lower LR)[​](<#workflow-3-reasoning-intensive-tasks-lower-lr> "Direct link to Workflow 3: Reasoning-intensive tasks \(lower LR\)")
**For math/code tasks** :
[code] 
    model_name_or_path: deepseek-ai/deepseek-math-7b-base  
      
    dataset_mixer:  
      argilla/distilabel-math-preference-dpo: 1.0  
      
    beta: 5.0                   # Higher for stronger signal  
    gamma_beta_ratio: 0.7       # Larger margin  
    learning_rate: 3e-7         # Lower LR for reasoning  
    sft_weight: 0.0  
      
    num_train_epochs: 1  
    per_device_train_batch_size: 1  
    gradient_accumulation_steps: 16  
    
[/code]
## When to use vs alternatives[​](<#when-to-use-vs-alternatives> "Direct link to When to use vs alternatives")
**Use SimPO when** :
  * Want simpler training than DPO (no reference model)
  * Have preference data (chosen/rejected pairs)
  * Need better performance than DPO
  * Limited compute resources
  * Single-node training sufficient


**Algorithm selection** :
  * **SimPO** : Simplest, best performance, no reference model
  * **DPO** : Need reference model baseline, more conservative
  * **PPO** : Maximum control, need reward model, complex setup
  * **GRPO** : Memory-efficient RL, no critic


**Use alternatives instead** :
  * **OpenRLHF** : Multi-node distributed training, PPO/GRPO
  * **TRL** : Need multiple methods in one framework
  * **DPO** : Established baseline comparison


## Common issues[​](<#common-issues> "Direct link to Common issues")
**Issue: Loss divergence**
Reduce learning rate:
[code] 
    learning_rate: 3e-7  # Reduce from 5e-7  
    
[/code]
Reduce beta:
[code] 
    beta: 1.0  # Reduce from 2.0  
    
[/code]
**Issue: Model forgets capabilities**
Add SFT regularization:
[code] 
    sft_weight: 0.1  # Add SFT loss component  
    
[/code]
**Issue: Poor preference separation**
Increase beta and margin:
[code] 
    beta: 5.0            # Increase from 2.0  
    gamma_beta_ratio: 0.8  # Increase from 0.5  
    
[/code]
**Issue: OOM during training**
Reduce batch size:
[code] 
    per_device_train_batch_size: 1  
    gradient_accumulation_steps: 16  # Maintain effective batch  
    
[/code]
Enable gradient checkpointing:
[code] 
    gradient_checkpointing: true  
    
[/code]
## Advanced topics[​](<#advanced-topics> "Direct link to Advanced topics")
**Loss functions** : See [references/loss-functions.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/simpo/references/loss-functions.md>) for sigmoid vs hinge loss, mathematical formulations, and when to use each.
**Hyperparameter tuning** : See [references/hyperparameters.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/simpo/references/hyperparameters.md>) for beta, gamma, learning rate selection guide, and model-size-specific recommendations.
**Dataset preparation** : See [references/datasets.md](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/simpo/references/datasets.md>) for preference data formats, quality filtering, and custom dataset creation.
## Hardware requirements[​](<#hardware-requirements> "Direct link to Hardware requirements")
  * **GPU** : NVIDIA A100/H100 recommended
  * **VRAM** :
    * 7B model: 1× A100 40GB (DeepSpeed ZeRO-3)
    * 8B model: 2× A100 40GB
    * 70B model: 8× A100 80GB
  * **Single-node** : DeepSpeed ZeRO-3 sufficient
  * **Mixed precision** : BF16 recommended


**Memory optimization** :
  * DeepSpeed ZeRO-3 (default config)
  * Gradient checkpointing
  * Flash Attention 2


## Resources[​](<#resources> "Direct link to Resources")
  * Paper: <https://arxiv.org/abs/2405.14734> (NeurIPS 2024)
  * GitHub: <https://github.com/princeton-nlp/SimPO>
  * Models: <https://huggingface.co/princeton-nlp>
  * Alignment Handbook: <https://github.com/huggingface/alignment-handbook>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Quick start](<#quick-start>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: Train from base model (Mistral 7B)](<#workflow-1-train-from-base-model-mistral-7b>)
    * [Workflow 2: Fine-tune instruct model (Llama 3 8B)](<#workflow-2-fine-tune-instruct-model-llama-3-8b>)
    * [Workflow 3: Reasoning-intensive tasks (lower LR)](<#workflow-3-reasoning-intensive-tasks-lower-lr>)
  * [When to use vs alternatives](<#when-to-use-vs-alternatives>)
  * [Common issues](<#common-issues>)
  * [Advanced topics](<#advanced-topics>)
  * [Hardware requirements](<#hardware-requirements>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-simpo -->
