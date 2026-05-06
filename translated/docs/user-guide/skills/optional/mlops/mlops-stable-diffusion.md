On this page
Современная генерация изображений по текстовому описанию с помощью моделей Stable Diffusion через библиотеку HuggingFace Diffusers. Используйте, когда нужно генерировать изображения из текстовых запросов, выполнять трансформацию «изображение-в-изображение», инпейнтинг или создавать собственные пайплайны диффузии.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")

|---|---  
|Source| Optional — install with `hermes skills install official/mlops/stable-diffusion`  
|Path| `optional-skills/mlops/stable-diffusion`  
|Version| `1.0.0`  
|Author| Orchestra Research  
|License| MIT  
|Dependencies| `diffusers>=0.30.0`, `transformers>=4.41.0`, `accelerate>=0.31.0`, `torch>=2.0.0`  
|Tags| `Image Generation`, `Stable Diffusion`, `Diffusers`, `Text-to-Image`, `Multimodal`, `Computer Vision`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Stable Diffusion Image Generation
Комплексное руководство по генерации изображений с помощью Stable Diffusion и библиотеки HuggingFace Diffusers.
## When to use Stable Diffusion[​](<#when-to-use-stable-diffusion> "Direct link to When to use Stable Diffusion")
**Используйте Stable Diffusion когда:**
  * Нужно генерировать изображения из текстовых описаний
  * Нужно выполнять трансформацию «изображение-в-изображение» (перенос стиля, улучшение)
  * Нужен инпейнтинг (заполнение замаскированных областей)
  * Нужен аутпейнтинг (расширение изображений за границы)
  * Нужно создавать вариации существующих изображений
  * Нужно строить собственные рабочие процессы генерации изображений


**Ключевые возможности:**
  * **Text-to-Image** : Генерация изображений из текстовых запросов на естественном языке
  * **Image-to-Image** : Преобразование существующих изображений по текстовой инструкции
  * **Inpainting** : Заполнение замаскированных областей с учётом контекста
  * **ControlNet** : Пространственное управление (контуры, позы, глубина)
  * **LoRA Support** : Эффективная донастройка и адаптация стиля
  * **Multiple Models** : Поддержка SD 1.5, SDXL, SD 3.0, Flux


**Используйте альтернативы вместо этого:**
  * **DALL-E 3** : Для API-генерации без GPU
  * **Midjourney** : Для художественных, стилизованных результатов
  * **Imagen** : Для интеграции с Google Cloud
  * **Leonardo.ai** : Для веб-ориентированных творческих рабочих процессов


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    pip install diffusers transformers accelerate torch  
    pip install xformers  # Опционально: энергоэффективное внимание  
    
[/code]
### Basic text-to-image[​](<#basic-text-to-image> "Direct link to Basic text-to-image")
[code] 
    from diffusers import DiffusionPipeline  
    import torch  
      
    # Загрузка пайплайна (автоопределение типа модели)  
    pipe = DiffusionPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        torch_dtype=torch.float16  
    )  
    pipe.to("cuda")  
      
    # Генерация изображения  
    image = pipe(  
        "A serene mountain landscape at sunset, highly detailed",  
        num_inference_steps=50,  
        guidance_scale=7.5  
    ).images[0]  
      
    image.save("output.png")  
    
[/code]
### Using SDXL (higher quality)[​](<#using-sdxl-higher-quality> "Direct link to Using SDXL \(higher quality\)")
[code] 
    from diffusers import AutoPipelineForText2Image  
    import torch  
      
    pipe = AutoPipelineForText2Image.from_pretrained(  
        "stabilityai/stable-diffusion-xl-base-1.0",  
        torch_dtype=torch.float16,  
        variant="fp16"  
    )  
    pipe.to("cuda")  
      
    # Включение оптимизации памяти  
    pipe.enable_model_cpu_offload()  
      
    image = pipe(  
        prompt="A futuristic city with flying cars, cinematic lighting",  
        height=1024,  
        width=1024,  
        num_inference_steps=30  
    ).images[0]  
    
[/code]
## Architecture overview[​](<#architecture-overview> "Direct link to Architecture overview")
### Three-pillar design[​](<#three-pillar-design> "Direct link to Three-pillar design")
Diffusers построен на трёх ключевых компонентах:
[code] 
    Pipeline (оркестрация)  
    ├── Model (нейронные сети)  
    │   ├── UNet / Transformer (предсказание шума)  
    │   ├── VAE (кодирование/декодирование латентного пространства)  
    │   └── Text Encoder (CLIP/T5)  
    └── Scheduler (алгоритм денойзинга)  
    
[/code]
### Pipeline inference flow[​](<#pipeline-inference-flow> "Direct link to Pipeline inference flow")
[code] 
    Text Prompt → Text Encoder → Text Embeddings  
                                        ↓  
    Random Noise → [Denoising Loop] ← Scheduler  
                          ↓  
                   Predicted Noise  
                          ↓  
                  VAE Decoder → Final Image  
    
[/code]
## Core concepts[​](<#core-concepts> "Direct link to Core concepts")
### Pipelines[​](<#pipelines> "Direct link to Pipelines")
Пайплайны оркестрируют полные рабочие процессы:
Pipeline| Purpose  
---|---  
`StableDiffusionPipeline`| Text-to-image (SD 1.x/2.x)  
`StableDiffusionXLPipeline`| Text-to-image (SDXL)  
`StableDiffusion3Pipeline`| Text-to-image (SD 3.0)  
`FluxPipeline`| Text-to-image (Flux models)  
`StableDiffusionImg2ImgPipeline`| Image-to-image  
`StableDiffusionInpaintPipeline`| Inpainting  
### Schedulers[​](<#schedulers> "Direct link to Schedulers")
Шедулеры управляют процессом денойзинга:
Scheduler| Steps| Quality| Use Case  
---|---|---|---|---  
`EulerDiscreteScheduler`| 20-50| Хорошее| Выбор по умолчанию  
`EulerAncestralDiscreteScheduler`| 20-50| Хорошее| Больше вариаций  
`DPMSolverMultistepScheduler`| 15-25| Отличное| Быстро, высокое качество  
`DDIMScheduler`| 50-100| Хорошее| Детерминированный  
`LCMScheduler`| 4-8| Хорошее| Очень быстро  
`UniPCMultistepScheduler`| 15-25| Отличное| Быстрая сходимость  
### Swapping schedulers[​](<#swapping-schedulers> "Direct link to Swapping schedulers")
[code] 
    from diffusers import DPMSolverMultistepScheduler  
      
    # Смена для более быстрой генерации  
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(  
        pipe.scheduler.config  
    )  
      
    # Теперь генерация с меньшим числом шагов  
    image = pipe(prompt, num_inference_steps=20).images[0]  
    
[/code]
## Generation parameters[​](<#generation-parameters> "Direct link to Generation parameters")
### Key parameters[​](<#key-parameters> "Direct link to Key parameters")
Parameter| Default| Description  
---|---|---|---  
`prompt`| Обязательный| Текстовое описание желаемого изображения  
`negative_prompt`| None| Чего следует избегать на изображении  
`num_inference_steps`| 50| Шаги денойзинга (больше = выше качество)  
`guidance_scale`| 7.5| Степень следования запросу (обычно 7-12)  
`height`, `width`| 512/1024| Размеры вывода (кратные 8)  
`generator`| None| Генератор torch для воспроизводимости  
`num_images_per_prompt`| 1| Размер батча  
### Reproducible generation[​](<#reproducible-generation> "Direct link to Reproducible generation")
[code] 
    import torch  
      
    generator = torch.Generator(device="cuda").manual_seed(42)  
      
    image = pipe(  
        prompt="A cat wearing a top hat",  
        generator=generator,  
        num_inference_steps=50  
    ).images[0]  
    
[/code]
### Negative prompts[​](<#negative-prompts> "Direct link to Negative prompts")
[code] 
    image = pipe(  
        prompt="Professional photo of a dog in a garden",  
        negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",  
        guidance_scale=7.5  
    ).images[0]  
    
[/code]
## Image-to-image[​](<#image-to-image> "Direct link to Image-to-image")
Преобразование существующих изображений с помощью текстовой инструкции:
[code] 
    from diffusers import AutoPipelineForImage2Image  
    from PIL import Image  
      
    pipe = AutoPipelineForImage2Image.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    init_image = Image.open("input.jpg").resize((512, 512))  
      
    image = pipe(  
        prompt="A watercolor painting of the scene",  
        image=init_image,  
        strength=0.75,  # Степень трансформации (0-1)  
        num_inference_steps=50  
    ).images[0]  
    
[/code]
## Inpainting[​](<#inpainting> "Direct link to Inpainting")
Заполнение замаскированных областей:
[code] 
    from diffusers import AutoPipelineForInpainting  
    from PIL import Image  
      
    pipe = AutoPipelineForInpainting.from_pretrained(  
        "runwayml/stable-diffusion-inpainting",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    image = Image.open("photo.jpg")  
    mask = Image.open("mask.png")  # Белый = область инпейнтинга  
      
    result = pipe(  
        prompt="A red car parked on the street",  
        image=image,  
        mask_image=mask,  
        num_inference_steps=50  
    ).images[0]  
    
[/code]
## ControlNet[​](<#controlnet> "Direct link to ControlNet")
Добавление пространственного управления для точного контроля:
[code] 
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel  
    import torch  
      
    # Загрузка ControlNet для управления по контурам  
    controlnet = ControlNetModel.from_pretrained(  
        "lllyasviel/control_v11p_sd15_canny",  
        torch_dtype=torch.float16  
    )  
      
    pipe = StableDiffusionControlNetPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        controlnet=controlnet,  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    # Использование Canny-изображения контуров для управления  
    control_image = get_canny_image(input_image)  
      
    image = pipe(  
        prompt="A beautiful house in the style of Van Gogh",  
        image=control_image,  
        num_inference_steps=30  
    ).images[0]  
    
[/code]
### Available ControlNets[​](<#available-controlnets> "Direct link to Available ControlNets")
ControlNet| Input Type| Use Case  
---|---|---|---  
`canny`| Карты контуров| Сохранение структуры  
`openpose`| Скелеты поз| Позы человека  
`depth`| Карты глубины| 3D-ориентированная генерация  
`normal`| Карты нормалей| Детали поверхности  
`mlsd`| Сегменты линий| Архитектурные линии  
`scribble`| Грубые наброски| Из наброска в изображение  
## LoRA adapters[​](<#lora-adapters> "Direct link to LoRA adapters")
Загрузка донастроенных адаптеров стиля:
[code] 
    from diffusers import DiffusionPipeline  
      
    pipe = DiffusionPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    # Загрузка весов LoRA  
    pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")  
      
    # Генерация с LoRA-стилем  
    image = pipe("A portrait in the trained style").images[0]  
      
    # Настройка силы LoRA  
    pipe.fuse_lora(lora_scale=0.8)  
      
    # Выгрузка LoRA  
    pipe.unload_lora_weights()  
    
[/code]
### Multiple LoRAs[​](<#multiple-loras> "Direct link to Multiple LoRAs")
[code] 
    # Загрузка нескольких LoRA  
    pipe.load_lora_weights("lora1", adapter_name="style")  
    pipe.load_lora_weights("lora2", adapter_name="character")  
      
    # Установка весов для каждой  
    pipe.set_adapters(["style", "character"], adapter_weights=[0.7, 0.5])  
      
    image = pipe("A portrait").images[0]  
    
[/code]
## Memory optimization[​](<#memory-optimization> "Direct link to Memory optimization")
### Enable CPU offloading[​](<#enable-cpu-offloading> "Direct link to Enable CPU offloading")
[code] 
    # Выгрузка модели на CPU — перемещает модели на CPU, когда они не используются  
    pipe.enable_model_cpu_offload()  
      
    # Последовательная выгрузка на CPU — более агрессивно, медленнее  
    pipe.enable_sequential_cpu_offload()  
    
[/code]
### Attention slicing[​](<#attention-slicing> "Direct link to Attention slicing")
[code] 
    # Снижение потребления памяти за счёт вычисления attention по частям  
    pipe.enable_attention_slicing()  
      
    # Или указание конкретного размера чанка  
    pipe.enable_attention_slicing("max")  
    
[/code]
### xFormers memory-efficient attention[​](<#xformers-memory-efficient-attention> "Direct link to xFormers memory-efficient attention")
[code] 
    # Требуется пакет xformers  
    pipe.enable_xformers_memory_efficient_attention()  
    
[/code]
### VAE slicing for large images[​](<#vae-slicing-for-large-images> "Direct link to VAE slicing for large images")
[code] 
    # Декодирование латентного пространства тайлами для больших изображений  
    pipe.enable_vae_slicing()  
    pipe.enable_vae_tiling()  
    
[/code]
## Model variants[​](<#model-variants> "Direct link to Model variants")
### Loading different precisions[​](<#loading-different-precisions> "Direct link to Loading different precisions")
[code] 
    # FP16 (рекомендуется для GPU)  
    pipe = DiffusionPipeline.from_pretrained(  
        "model-id",  
        torch_dtype=torch.float16,  
        variant="fp16"  
    )  
      
    # BF16 (лучшая точность, требует GPU Ampere+)  
    pipe = DiffusionPipeline.from_pretrained(  
        "model-id",  
        torch_dtype=torch.bfloat16  
    )  
    
[/code]
### Loading specific components[​](<#loading-specific-components> "Direct link to Loading specific components")
[code] 
    from diffusers import UNet2DConditionModel, AutoencoderKL  
      
    # Загрузка кастомной VAE  
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")  
      
    # Использование с пайплайном  
    pipe = DiffusionPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        vae=vae,  
        torch_dtype=torch.float16  
    )  
    
[/code]
## Batch generation[​](<#batch-generation> "Direct link to Batch generation")
Эффективная генерация нескольких изображений:
[code] 
    # Несколько запросов  
    prompts = [  
        "A cat playing piano",  
        "A dog reading a book",  
        "A bird painting a picture"  
    ]  
      
    images = pipe(prompts, num_inference_steps=30).images  
      
    # Несколько изображений на запрос  
    images = pipe(  
        "A beautiful sunset",  
        num_images_per_prompt=4,  
        num_inference_steps=30  
    ).images  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: High-quality generation[​](<#workflow-1-high-quality-generation> "Direct link to Workflow 1: High-quality generation")
[code] 
    from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler  
    import torch  
      
    # 1. Загрузка SDXL с оптимизациями  
    pipe = StableDiffusionXLPipeline.from_pretrained(  
        "stabilityai/stable-diffusion-xl-base-1.0",  
        torch_dtype=torch.float16,  
        variant="fp16"  
    )  
    pipe.to("cuda")  
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)  
    pipe.enable_model_cpu_offload()  
      
    # 2. Генерация с настройками качества  
    image = pipe(  
        prompt="A majestic lion in the savanna, golden hour lighting, 8k, detailed fur",  
        negative_prompt="blurry, low quality, cartoon, anime, sketch",  
        num_inference_steps=30,  
        guidance_scale=7.5,  
        height=1024,  
        width=1024  
    ).images[0]  
    
[/code]
### Workflow 2: Fast prototyping[​](<#workflow-2-fast-prototyping> "Direct link to Workflow 2: Fast prototyping")
[code] 
    from diffusers import AutoPipelineForText2Image, LCMScheduler  
    import torch  
      
    # Использование LCM для генерации за 4-8 шагов  
    pipe = AutoPipelineForText2Image.from_pretrained(  
        "stabilityai/stable-diffusion-xl-base-1.0",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    # Загрузка LCM LoRA для быстрой генерации  
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")  
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)  
    pipe.fuse_lora()  
      
    # Генерация за ~1 секунду  
    image = pipe(  
        "A beautiful landscape",  
        num_inference_steps=4,  
        guidance_scale=1.0  
    ).images[0]  
    
[/code]
## Common issues[​](<#common-issues> "Direct link to Common issues")
**CUDA out of memory:**
[code] 
    # Включение оптимизаций памяти  
    pipe.enable_model_cpu_offload()  
    pipe.enable_attention_slicing()  
    pipe.enable_vae_slicing()  
      
    # Или использование меньшей точности  
    pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)  
    
[/code]
**Black/noise images:**
[code] 
    # Проверка конфигурации VAE  
    # При необходимости отключение проверки безопасности  
    pipe.safety_checker = None  
      
    # Обеспечение согласованности dtype  
    pipe = pipe.to(dtype=torch.float16)  
    
[/code]
**Slow generation:**
[code] 
    # Использование более быстрого шедулера  
    from diffusers import DPMSolverMultistepScheduler  
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)  
      
    # Уменьшение числа шагов  
    image = pipe(prompt, num_inference_steps=20).images[0]  
    
[/code]
## References[​](<#references> "Direct link to References")
  * **[Advanced Usage](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/stable-diffusion/references/advanced-usage.md>)** \- Кастомные пайплайны, донастройка, развёртывание
  * **[Troubleshooting](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/stable-diffusion/references/troubleshooting.md>)** \- Частые проблемы и решения


## Resources[​](<#resources> "Direct link to Resources")
  * **Documentation** : <https://huggingface.co/docs/diffusers>
  * **Repository** : <https://github.com/huggingface/diffusers>
  * **Model Hub** : <https://huggingface.co/models?library=diffusers>
  * **Discord** : <https://discord.gg/diffusers>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use Stable Diffusion](<#when-to-use-stable-diffusion>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Basic text-to-image](<#basic-text-to-image>)
    * [Using SDXL (higher quality)](<#using-sdxl-higher-quality>)
  * [Architecture overview](<#architecture-overview>)
    * [Three-pillar design](<#three-pillar-design>)
    * [Pipeline inference flow](<#pipeline-inference-flow>)
  * [Core concepts](<#core-concepts>)
    * [Pipelines](<#pipelines>)
    * [Schedulers](<#schedulers>)
    * [Swapping schedulers](<#swapping-schedulers>)
  * [Generation parameters](<#generation-parameters>)
    * [Key parameters](<#key-parameters>)
    * [Reproducible generation](<#reproducible-generation>)
    * [Negative prompts](<#negative-prompts>)
  * [Image-to-image](<#image-to-image>)
  * [Inpainting](<#inpainting>)
  * [ControlNet](<#controlnet>)
  * [Available ControlNets](<#available-controlnets>)
  * [LoRA adapters](<#lora-adapters>)
    * [Multiple LoRAs](<#multiple-loras>)
  * [Memory optimization](<#memory-optimization>)
    * [Enable CPU offloading](<#enable-cpu-offloading>)
    * [Attention slicing](<#attention-slicing>)
    * [xFormers memory-efficient attention](<#xformers-memory-efficient-attention>)
    * [VAE slicing for large images](<#vae-slicing-for-large-images>)
  * [Model variants](<#model-variants>)
    * [Loading different precisions](<#loading-different-precisions>)
    * [Loading specific components](<#loading-specific-components>)
  * [Batch generation](<#batch-generation>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: High-quality generation](<#workflow-1-high-quality-generation>)
    * [Workflow 2: Fast prototyping](<#workflow-2-fast-prototyping>)
  * [Common issues](<#common-issues>)
  * [References](<#references>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-stable-diffusion -->
