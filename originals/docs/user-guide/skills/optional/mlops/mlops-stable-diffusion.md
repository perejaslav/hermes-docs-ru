On this page
State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/stable-diffusion`  
Path| `optional-skills/mlops/stable-diffusion`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `diffusers>=0.30.0`, `transformers>=4.41.0`, `accelerate>=0.31.0`, `torch>=2.0.0`  
Tags| `Image Generation`, `Stable Diffusion`, `Diffusers`, `Text-to-Image`, `Multimodal`, `Computer Vision`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Stable Diffusion Image Generation
Comprehensive guide to generating images with Stable Diffusion using the HuggingFace Diffusers library.
## When to use Stable Diffusion[​](<#when-to-use-stable-diffusion> "Direct link to When to use Stable Diffusion")
**Use Stable Diffusion when:**
  * Generating images from text descriptions
  * Performing image-to-image translation (style transfer, enhancement)
  * Inpainting (filling in masked regions)
  * Outpainting (extending images beyond boundaries)
  * Creating variations of existing images
  * Building custom image generation workflows


**Key features:**
  * **Text-to-Image** : Generate images from natural language prompts
  * **Image-to-Image** : Transform existing images with text guidance
  * **Inpainting** : Fill masked regions with context-aware content
  * **ControlNet** : Add spatial conditioning (edges, poses, depth)
  * **LoRA Support** : Efficient fine-tuning and style adaptation
  * **Multiple Models** : SD 1.5, SDXL, SD 3.0, Flux support


**Use alternatives instead:**
  * **DALL-E 3** : For API-based generation without GPU
  * **Midjourney** : For artistic, stylized outputs
  * **Imagen** : For Google Cloud integration
  * **Leonardo.ai** : For web-based creative workflows


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    pip install diffusers transformers accelerate torch  
    pip install xformers  # Optional: memory-efficient attention  
    
[/code]
### Basic text-to-image[​](<#basic-text-to-image> "Direct link to Basic text-to-image")
[code] 
    from diffusers import DiffusionPipeline  
    import torch  
      
    # Load pipeline (auto-detects model type)  
    pipe = DiffusionPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        torch_dtype=torch.float16  
    )  
    pipe.to("cuda")  
      
    # Generate image  
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
      
    # Enable memory optimization  
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
Diffusers is built around three core components:
[code] 
    Pipeline (orchestration)  
    ├── Model (neural networks)  
    │   ├── UNet / Transformer (noise prediction)  
    │   ├── VAE (latent encoding/decoding)  
    │   └── Text Encoder (CLIP/T5)  
    └── Scheduler (denoising algorithm)  
    
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
Pipelines orchestrate complete workflows:
Pipeline| Purpose  
---|---  
`StableDiffusionPipeline`| Text-to-image (SD 1.x/2.x)  
`StableDiffusionXLPipeline`| Text-to-image (SDXL)  
`StableDiffusion3Pipeline`| Text-to-image (SD 3.0)  
`FluxPipeline`| Text-to-image (Flux models)  
`StableDiffusionImg2ImgPipeline`| Image-to-image  
`StableDiffusionInpaintPipeline`| Inpainting  
### Schedulers[​](<#schedulers> "Direct link to Schedulers")
Schedulers control the denoising process:
Scheduler| Steps| Quality| Use Case  
---|---|---|---  
`EulerDiscreteScheduler`| 20-50| Good| Default choice  
`EulerAncestralDiscreteScheduler`| 20-50| Good| More variation  
`DPMSolverMultistepScheduler`| 15-25| Excellent| Fast, high quality  
`DDIMScheduler`| 50-100| Good| Deterministic  
`LCMScheduler`| 4-8| Good| Very fast  
`UniPCMultistepScheduler`| 15-25| Excellent| Fast convergence  
### Swapping schedulers[​](<#swapping-schedulers> "Direct link to Swapping schedulers")
[code] 
    from diffusers import DPMSolverMultistepScheduler  
      
    # Swap for faster generation  
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(  
        pipe.scheduler.config  
    )  
      
    # Now generate with fewer steps  
    image = pipe(prompt, num_inference_steps=20).images[0]  
    
[/code]
## Generation parameters[​](<#generation-parameters> "Direct link to Generation parameters")
### Key parameters[​](<#key-parameters> "Direct link to Key parameters")
Parameter| Default| Description  
---|---|---  
`prompt`| Required| Text description of desired image  
`negative_prompt`| None| What to avoid in the image  
`num_inference_steps`| 50| Denoising steps (more = better quality)  
`guidance_scale`| 7.5| Prompt adherence (7-12 typical)  
`height`, `width`| 512/1024| Output dimensions (multiples of 8)  
`generator`| None| Torch generator for reproducibility  
`num_images_per_prompt`| 1| Batch size  
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
Transform existing images with text guidance:
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
        strength=0.75,  # How much to transform (0-1)  
        num_inference_steps=50  
    ).images[0]  
    
[/code]
## Inpainting[​](<#inpainting> "Direct link to Inpainting")
Fill masked regions:
[code] 
    from diffusers import AutoPipelineForInpainting  
    from PIL import Image  
      
    pipe = AutoPipelineForInpainting.from_pretrained(  
        "runwayml/stable-diffusion-inpainting",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    image = Image.open("photo.jpg")  
    mask = Image.open("mask.png")  # White = inpaint region  
      
    result = pipe(  
        prompt="A red car parked on the street",  
        image=image,  
        mask_image=mask,  
        num_inference_steps=50  
    ).images[0]  
    
[/code]
## ControlNet[​](<#controlnet> "Direct link to ControlNet")
Add spatial conditioning for precise control:
[code] 
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel  
    import torch  
      
    # Load ControlNet for edge conditioning  
    controlnet = ControlNetModel.from_pretrained(  
        "lllyasviel/control_v11p_sd15_canny",  
        torch_dtype=torch.float16  
    )  
      
    pipe = StableDiffusionControlNetPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        controlnet=controlnet,  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    # Use Canny edge image as control  
    control_image = get_canny_image(input_image)  
      
    image = pipe(  
        prompt="A beautiful house in the style of Van Gogh",  
        image=control_image,  
        num_inference_steps=30  
    ).images[0]  
    
[/code]
### Available ControlNets[​](<#available-controlnets> "Direct link to Available ControlNets")
ControlNet| Input Type| Use Case  
---|---|---  
`canny`| Edge maps| Preserve structure  
`openpose`| Pose skeletons| Human poses  
`depth`| Depth maps| 3D-aware generation  
`normal`| Normal maps| Surface details  
`mlsd`| Line segments| Architectural lines  
`scribble`| Rough sketches| Sketch-to-image  
## LoRA adapters[​](<#lora-adapters> "Direct link to LoRA adapters")
Load fine-tuned style adapters:
[code] 
    from diffusers import DiffusionPipeline  
      
    pipe = DiffusionPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    # Load LoRA weights  
    pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")  
      
    # Generate with LoRA style  
    image = pipe("A portrait in the trained style").images[0]  
      
    # Adjust LoRA strength  
    pipe.fuse_lora(lora_scale=0.8)  
      
    # Unload LoRA  
    pipe.unload_lora_weights()  
    
[/code]
### Multiple LoRAs[​](<#multiple-loras> "Direct link to Multiple LoRAs")
[code] 
    # Load multiple LoRAs  
    pipe.load_lora_weights("lora1", adapter_name="style")  
    pipe.load_lora_weights("lora2", adapter_name="character")  
      
    # Set weights for each  
    pipe.set_adapters(["style", "character"], adapter_weights=[0.7, 0.5])  
      
    image = pipe("A portrait").images[0]  
    
[/code]
## Memory optimization[​](<#memory-optimization> "Direct link to Memory optimization")
### Enable CPU offloading[​](<#enable-cpu-offloading> "Direct link to Enable CPU offloading")
[code] 
    # Model CPU offload - moves models to CPU when not in use  
    pipe.enable_model_cpu_offload()  
      
    # Sequential CPU offload - more aggressive, slower  
    pipe.enable_sequential_cpu_offload()  
    
[/code]
### Attention slicing[​](<#attention-slicing> "Direct link to Attention slicing")
[code] 
    # Reduce memory by computing attention in chunks  
    pipe.enable_attention_slicing()  
      
    # Or specific chunk size  
    pipe.enable_attention_slicing("max")  
    
[/code]
### xFormers memory-efficient attention[​](<#xformers-memory-efficient-attention> "Direct link to xFormers memory-efficient attention")
[code] 
    # Requires xformers package  
    pipe.enable_xformers_memory_efficient_attention()  
    
[/code]
### VAE slicing for large images[​](<#vae-slicing-for-large-images> "Direct link to VAE slicing for large images")
[code] 
    # Decode latents in tiles for large images  
    pipe.enable_vae_slicing()  
    pipe.enable_vae_tiling()  
    
[/code]
## Model variants[​](<#model-variants> "Direct link to Model variants")
### Loading different precisions[​](<#loading-different-precisions> "Direct link to Loading different precisions")
[code] 
    # FP16 (recommended for GPU)  
    pipe = DiffusionPipeline.from_pretrained(  
        "model-id",  
        torch_dtype=torch.float16,  
        variant="fp16"  
    )  
      
    # BF16 (better precision, requires Ampere+ GPU)  
    pipe = DiffusionPipeline.from_pretrained(  
        "model-id",  
        torch_dtype=torch.bfloat16  
    )  
    
[/code]
### Loading specific components[​](<#loading-specific-components> "Direct link to Loading specific components")
[code] 
    from diffusers import UNet2DConditionModel, AutoencoderKL  
      
    # Load custom VAE  
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")  
      
    # Use with pipeline  
    pipe = DiffusionPipeline.from_pretrained(  
        "stable-diffusion-v1-5/stable-diffusion-v1-5",  
        vae=vae,  
        torch_dtype=torch.float16  
    )  
    
[/code]
## Batch generation[​](<#batch-generation> "Direct link to Batch generation")
Generate multiple images efficiently:
[code] 
    # Multiple prompts  
    prompts = [  
        "A cat playing piano",  
        "A dog reading a book",  
        "A bird painting a picture"  
    ]  
      
    images = pipe(prompts, num_inference_steps=30).images  
      
    # Multiple images per prompt  
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
      
    # 1. Load SDXL with optimizations  
    pipe = StableDiffusionXLPipeline.from_pretrained(  
        "stabilityai/stable-diffusion-xl-base-1.0",  
        torch_dtype=torch.float16,  
        variant="fp16"  
    )  
    pipe.to("cuda")  
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)  
    pipe.enable_model_cpu_offload()  
      
    # 2. Generate with quality settings  
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
      
    # Use LCM for 4-8 step generation  
    pipe = AutoPipelineForText2Image.from_pretrained(  
        "stabilityai/stable-diffusion-xl-base-1.0",  
        torch_dtype=torch.float16  
    ).to("cuda")  
      
    # Load LCM LoRA for fast generation  
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")  
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)  
    pipe.fuse_lora()  
      
    # Generate in ~1 second  
    image = pipe(  
        "A beautiful landscape",  
        num_inference_steps=4,  
        guidance_scale=1.0  
    ).images[0]  
    
[/code]
## Common issues[​](<#common-issues> "Direct link to Common issues")
**CUDA out of memory:**
[code] 
    # Enable memory optimizations  
    pipe.enable_model_cpu_offload()  
    pipe.enable_attention_slicing()  
    pipe.enable_vae_slicing()  
      
    # Or use lower precision  
    pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)  
    
[/code]
**Black/noise images:**
[code] 
    # Check VAE configuration  
    # Use safety checker bypass if needed  
    pipe.safety_checker = None  
      
    # Ensure proper dtype consistency  
    pipe = pipe.to(dtype=torch.float16)  
    
[/code]
**Slow generation:**
[code] 
    # Use faster scheduler  
    from diffusers import DPMSolverMultistepScheduler  
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)  
      
    # Reduce steps  
    image = pipe(prompt, num_inference_steps=20).images[0]  
    
[/code]
## References[​](<#references> "Direct link to References")
  * **[Advanced Usage](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/stable-diffusion/references/advanced-usage.md>)** \- Custom pipelines, fine-tuning, deployment
  * **[Troubleshooting](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/stable-diffusion/references/troubleshooting.md>)** \- Common issues and solutions


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
