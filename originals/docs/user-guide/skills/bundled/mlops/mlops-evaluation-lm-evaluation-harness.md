On this page
lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/mlops/evaluation/lm-evaluation-harness`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `lm-eval`, `transformers`, `vllm`  
Tags| `Evaluation`, `LM Evaluation Harness`, `Benchmarking`, `MMLU`, `HumanEval`, `GSM8K`, `EleutherAI`, `Model Quality`, `Academic Benchmarks`, `Industry Standard`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# lm-evaluation-harness - LLM Benchmarking
## What's inside[​](<#whats-inside> "Direct link to What's inside")
Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models, reporting academic results, or tracking training progress. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, APIs.
## Quick start[​](<#quick-start> "Direct link to Quick start")
lm-evaluation-harness evaluates LLMs across 60+ academic benchmarks using standardized prompts and metrics.
**Installation** :
[code] 
    pip install lm-eval  
    
[/code]
**Evaluate any HuggingFace model** :
[code] 
    lm_eval --model hf \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf \  
      --tasks mmlu,gsm8k,hellaswag \  
      --device cuda:0 \  
      --batch_size 8  
    
[/code]
**View available tasks** :
[code] 
    lm_eval --tasks list  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: Standard benchmark evaluation[​](<#workflow-1-standard-benchmark-evaluation> "Direct link to Workflow 1: Standard benchmark evaluation")
Evaluate model on core benchmarks (MMLU, GSM8K, HumanEval).
Copy this checklist:
[code] 
    Benchmark Evaluation:  
    - [ ] Step 1: Choose benchmark suite  
    - [ ] Step 2: Configure model  
    - [ ] Step 3: Run evaluation  
    - [ ] Step 4: Analyze results  
    
[/code]
**Step 1: Choose benchmark suite**
**Core reasoning benchmarks** :
  * **MMLU** (Massive Multitask Language Understanding) - 57 subjects, multiple choice
  * **GSM8K** \- Grade school math word problems
  * **HellaSwag** \- Common sense reasoning
  * **TruthfulQA** \- Truthfulness and factuality
  * **ARC** (AI2 Reasoning Challenge) - Science questions


**Code benchmarks** :
  * **HumanEval** \- Python code generation (164 problems)
  * **MBPP** (Mostly Basic Python Problems) - Python coding


**Standard suite** (recommended for model releases):
[code] 
    --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge  
    
[/code]
**Step 2: Configure model**
**HuggingFace model** :
[code] 
    lm_eval --model hf \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf,dtype=bfloat16 \  
      --tasks mmlu \  
      --device cuda:0 \  
      --batch_size auto  # Auto-detect optimal batch size  
    
[/code]
**Quantized model (4-bit/8-bit)** :
[code] 
    lm_eval --model hf \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf,load_in_4bit=True \  
      --tasks mmlu \  
      --device cuda:0  
    
[/code]
**Custom checkpoint** :
[code] 
    lm_eval --model hf \  
      --model_args pretrained=/path/to/my-model,tokenizer=/path/to/tokenizer \  
      --tasks mmlu \  
      --device cuda:0  
    
[/code]
**Step 3: Run evaluation**
[code] 
    # Full MMLU evaluation (57 subjects)  
    lm_eval --model hf \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf \  
      --tasks mmlu \  
      --num_fewshot 5 \  # 5-shot evaluation (standard)  
      --batch_size 8 \  
      --output_path results/ \  
      --log_samples  # Save individual predictions  
      
    # Multiple benchmarks at once  
    lm_eval --model hf \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf \  
      --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \  
      --num_fewshot 5 \  
      --batch_size 8 \  
      --output_path results/llama2-7b-eval.json  
    
[/code]
**Step 4: Analyze results**
Results saved to `results/llama2-7b-eval.json`:
[code] 
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
    
[/code]
### Workflow 2: Track training progress[​](<#workflow-2-track-training-progress> "Direct link to Workflow 2: Track training progress")
Evaluate checkpoints during training.
[code] 
    Training Progress Tracking:  
    - [ ] Step 1: Set up periodic evaluation  
    - [ ] Step 2: Choose quick benchmarks  
    - [ ] Step 3: Automate evaluation  
    - [ ] Step 4: Plot learning curves  
    
[/code]
**Step 1: Set up periodic evaluation**
Evaluate every N training steps:
[code] 
    #!/bin/bash  
    # eval_checkpoint.sh  
      
    CHECKPOINT_DIR=$1  
    STEP=$2  
      
    lm_eval --model hf \  
      --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \  
      --tasks gsm8k,hellaswag \  
      --num_fewshot 0 \  # 0-shot for speed  
      --batch_size 16 \  
      --output_path results/step-$STEP.json  
    
[/code]
**Step 2: Choose quick benchmarks**
Fast benchmarks for frequent evaluation:
  * **HellaSwag** : ~10 minutes on 1 GPU
  * **GSM8K** : ~5 minutes
  * **PIQA** : ~2 minutes


Avoid for frequent eval (too slow):
  * **MMLU** : ~2 hours (57 subjects)
  * **HumanEval** : Requires code execution


**Step 3: Automate evaluation**
Integrate with training script:
[code] 
    # In training loop  
    if step % eval_interval == 0:  
        model.save_pretrained(f"checkpoints/step-{step}")  
      
        # Run evaluation  
        os.system(f"./eval_checkpoint.sh checkpoints step-{step}")  
    
[/code]
Or use PyTorch Lightning callbacks:
[code] 
    from pytorch_lightning import Callback  
      
    class EvalHarnessCallback(Callback):  
        def on_validation_epoch_end(self, trainer, pl_module):  
            step = trainer.global_step  
            checkpoint_path = f"checkpoints/step-{step}"  
      
            # Save checkpoint  
            trainer.save_checkpoint(checkpoint_path)  
      
            # Run lm-eval  
            os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} ...")  
    
[/code]
**Step 4: Plot learning curves**
[code] 
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
    
[/code]
### Workflow 3: Compare multiple models[​](<#workflow-3-compare-multiple-models> "Direct link to Workflow 3: Compare multiple models")
Benchmark suite for model comparison.
[code] 
    Model Comparison:  
    - [ ] Step 1: Define model list  
    - [ ] Step 2: Run evaluations  
    - [ ] Step 3: Generate comparison table  
    
[/code]
**Step 1: Define model list**
[code] 
    # models.txt  
    meta-llama/Llama-2-7b-hf  
    meta-llama/Llama-2-13b-hf  
    mistralai/Mistral-7B-v0.1  
    microsoft/phi-2  
    
[/code]
**Step 2: Run evaluations**
[code] 
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
    
[/code]
**Step 3: Generate comparison table**
[code] 
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
    
[/code]
Output:
[code] 
    | Model                  | MMLU  | GSM8K | HELLASWAG | TRUTHFULQA |  
    |------------------------|-------|-------|-----------|------------|  
    | meta-llama/Llama-2-7b  | 0.459 | 0.142 | 0.765     | 0.391      |  
    | meta-llama/Llama-2-13b | 0.549 | 0.287 | 0.801     | 0.430      |  
    | mistralai/Mistral-7B   | 0.626 | 0.395 | 0.812     | 0.428      |  
    | microsoft/phi-2        | 0.560 | 0.613 | 0.682     | 0.447      |  
    
[/code]
### Workflow 4: Evaluate with vLLM (faster inference)[​](<#workflow-4-evaluate-with-vllm-faster-inference> "Direct link to Workflow 4: Evaluate with vLLM \(faster inference\)")
Use vLLM backend for 5-10x faster evaluation.
[code] 
    vLLM Evaluation:  
    - [ ] Step 1: Install vLLM  
    - [ ] Step 2: Configure vLLM backend  
    - [ ] Step 3: Run evaluation  
    
[/code]
**Step 1: Install vLLM**
[code] 
    pip install vllm  
    
[/code]
**Step 2: Configure vLLM backend**
[code] 
    lm_eval --model vllm \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8 \  
      --tasks mmlu \  
      --batch_size auto  
    
[/code]
**Step 3: Run evaluation**
vLLM is 5-10× faster than standard HuggingFace:
[code] 
    # Standard HF: ~2 hours for MMLU on 7B model  
    lm_eval --model hf \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf \  
      --tasks mmlu \  
      --batch_size 8  
      
    # vLLM: ~15-20 minutes for MMLU on 7B model  
    lm_eval --model vllm \  
      --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \  
      --tasks mmlu \  
      --batch_size auto  
    
[/code]
## When to use vs alternatives[​](<#when-to-use-vs-alternatives> "Direct link to When to use vs alternatives")
**Use lm-evaluation-harness when:**
  * Benchmarking models for academic papers
  * Comparing model quality across standard tasks
  * Tracking training progress
  * Reporting standardized metrics (everyone uses same prompts)
  * Need reproducible evaluation


**Use alternatives instead:**
  * **HELM** (Stanford): Broader evaluation (fairness, efficiency, calibration)
  * **AlpacaEval** : Instruction-following evaluation with LLM judges
  * **MT-Bench** : Conversational multi-turn evaluation
  * **Custom scripts** : Domain-specific evaluation


## Common issues[​](<#common-issues> "Direct link to Common issues")
**Issue: Evaluation too slow**
Use vLLM backend:
[code] 
    lm_eval --model vllm \  
      --model_args pretrained=model-name,tensor_parallel_size=2  
    
[/code]
Or reduce fewshot examples:
[code] 
    --num_fewshot 0  # Instead of 5  
    
[/code]
Or evaluate subset of MMLU:
[code] 
    --tasks mmlu_stem  # Only STEM subjects  
    
[/code]
**Issue: Out of memory**
Reduce batch size:
[code] 
    --batch_size 1  # Or --batch_size auto  
    
[/code]
Use quantization:
[code] 
    --model_args pretrained=model-name,load_in_8bit=True  
    
[/code]
Enable CPU offloading:
[code] 
    --model_args pretrained=model-name,device_map=auto,offload_folder=offload  
    
[/code]
**Issue: Different results than reported**
Check fewshot count:
[code] 
    --num_fewshot 5  # Most papers use 5-shot  
    
[/code]
Check exact task name:
[code] 
    --tasks mmlu  # Not mmlu_direct or mmlu_fewshot  
    
[/code]
Verify model and tokenizer match:
[code] 
    --model_args pretrained=model-name,tokenizer=same-model-name  
    
[/code]
**Issue: HumanEval not executing code**
Install execution dependencies:
[code] 
    pip install human-eval  
    
[/code]
Enable code execution:
[code] 
    lm_eval --model hf \  
      --model_args pretrained=model-name \  
      --tasks humaneval \  
      --allow_code_execution  # Required for HumanEval  
    
[/code]
## Advanced topics[​](<#advanced-topics> "Direct link to Advanced topics")
**Benchmark descriptions** : See [references/benchmark-guide.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/benchmark-guide.md>) for detailed description of all 60+ tasks, what they measure, and interpretation.
**Custom tasks** : See [references/custom-tasks.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/custom-tasks.md>) for creating domain-specific evaluation tasks.
**API evaluation** : See [references/api-evaluation.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/api-evaluation.md>) for evaluating OpenAI, Anthropic, and other API models.
**Multi-GPU strategies** : See [references/distributed-eval.md](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/evaluation/lm-evaluation-harness/references/distributed-eval.md>) for data parallel and tensor parallel evaluation.
## Hardware requirements[​](<#hardware-requirements> "Direct link to Hardware requirements")
  * **GPU** : NVIDIA (CUDA 11.8+), works on CPU (very slow)
  * **VRAM** :
    * 7B model: 16GB (bf16) or 8GB (8-bit)
    * 13B model: 28GB (bf16) or 14GB (8-bit)
    * 70B model: Requires multi-GPU or quantization
  * **Time** (7B model, single A100):
    * HellaSwag: 10 minutes
    * GSM8K: 5 minutes
    * MMLU (full): 2 hours
    * HumanEval: 20 minutes


## Resources[​](<#resources> "Direct link to Resources")
  * GitHub: <https://github.com/EleutherAI/lm-evaluation-harness>
  * Docs: <https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs>
  * Task library: 60+ tasks including MMLU, GSM8K, HumanEval, TruthfulQA, HellaSwag, ARC, WinoGrande, etc.
  * Leaderboard: <https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard> (uses this harness)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [What's inside](<#whats-inside>)
  * [Quick start](<#quick-start>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: Standard benchmark evaluation](<#workflow-1-standard-benchmark-evaluation>)
    * [Workflow 2: Track training progress](<#workflow-2-track-training-progress>)
    * [Workflow 3: Compare multiple models](<#workflow-3-compare-multiple-models>)
    * [Workflow 4: Evaluate with vLLM (faster inference)](<#workflow-4-evaluate-with-vllm-faster-inference>)
  * [When to use vs alternatives](<#when-to-use-vs-alternatives>)
  * [Common issues](<#common-issues>)
  * [Advanced topics](<#advanced-topics>)
  * [Hardware requirements](<#hardware-requirements>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-evaluation-lm-evaluation-harness -->
