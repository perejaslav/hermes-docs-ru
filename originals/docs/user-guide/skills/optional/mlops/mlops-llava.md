On this page
Large Language and Vision Assistant. Enables visual instruction tuning and image-based conversations. Combines CLIP vision encoder with Vicuna/LLaMA language models. Supports multi-turn image chat, visual question answering, and instruction following. Use for vision-language chatbots or image understanding tasks. Best for conversational image analysis.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/llava`  
Path| `optional-skills/mlops/llava`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `transformers`, `torch`, `pillow`  
Tags| `LLaVA`, `Vision-Language`, `Multimodal`, `Visual Question Answering`, `Image Chat`, `CLIP`, `Vicuna`, `Conversational AI`, `Instruction Tuning`, `VQA`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# LLaVA - Large Language and Vision Assistant
Open-source vision-language model for conversational image understanding.
## When to use LLaVA[​](<#when-to-use-llava> "Direct link to When to use LLaVA")
**Use when:**
  * Building vision-language chatbots
  * Visual question answering (VQA)
  * Image description and captioning
  * Multi-turn image conversations
  * Visual instruction following
  * Document understanding with images


**Metrics** :
  * **23,000+ GitHub stars**
  * GPT-4V level capabilities (targeted)
  * Apache 2.0 License
  * Multiple model sizes (7B-34B params)


**Use alternatives instead** :
  * **GPT-4V** : Highest quality, API-based
  * **CLIP** : Simple zero-shot classification
  * **BLIP-2** : Better for captioning only
  * **Flamingo** : Research, not open-source


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Clone repository  
    git clone https://github.com/haotian-liu/LLaVA  
    cd LLaVA  
      
    # Install  
    pip install -e .  
    
[/code]
### Basic usage[​](<#basic-usage> "Direct link to Basic usage")
[code] 
    from llava.model.builder import load_pretrained_model  
    from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token  
    from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN  
    from llava.conversation import conv_templates  
    from PIL import Image  
    import torch  
      
    # Load model  
    model_path = "liuhaotian/llava-v1.5-7b"  
    tokenizer, model, image_processor, context_len = load_pretrained_model(  
        model_path=model_path,  
        model_base=None,  
        model_name=get_model_name_from_path(model_path)  
    )  
      
    # Load image  
    image = Image.open("image.jpg")  
    image_tensor = process_images([image], image_processor, model.config)  
    image_tensor = image_tensor.to(model.device, dtype=torch.float16)  
      
    # Create conversation  
    conv = conv_templates["llava_v1"].copy()  
    conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\nWhat is in this image?")  
    conv.append_message(conv.roles[1], None)  
    prompt = conv.get_prompt()  
      
    # Generate response  
    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)  
      
    with torch.inference_mode():  
        output_ids = model.generate(  
            input_ids,  
            images=image_tensor,  
            do_sample=True,  
            temperature=0.2,  
            max_new_tokens=512  
        )  
      
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()  
    print(response)  
    
[/code]
## Available models[​](<#available-models> "Direct link to Available models")
Model| Parameters| VRAM| Quality  
---|---|---|---  
LLaVA-v1.5-7B| 7B| ~14 GB| Good  
LLaVA-v1.5-13B| 13B| ~28 GB| Better  
LLaVA-v1.6-34B| 34B| ~70 GB| Best
[code] 
    # Load different models  
    model_7b = "liuhaotian/llava-v1.5-7b"  
    model_13b = "liuhaotian/llava-v1.5-13b"  
    model_34b = "liuhaotian/llava-v1.6-34b"  
      
    # 4-bit quantization for lower VRAM  
    load_4bit = True  # Reduces VRAM by ~4×  
    
[/code]  
## CLI usage[​](<#cli-usage> "Direct link to CLI usage")
[code] 
    # Single image query  
    python -m llava.serve.cli \  
        --model-path liuhaotian/llava-v1.5-7b \  
        --image-file image.jpg \  
        --query "What is in this image?"  
      
    # Multi-turn conversation  
    python -m llava.serve.cli \  
        --model-path liuhaotian/llava-v1.5-7b \  
        --image-file image.jpg  
    # Then type questions interactively  
    
[/code]
## Web UI (Gradio)[​](<#web-ui-gradio> "Direct link to Web UI \(Gradio\)")
[code] 
    # Launch Gradio interface  
    python -m llava.serve.gradio_web_server \  
        --model-path liuhaotian/llava-v1.5-7b \  
        --load-4bit  # Optional: reduce VRAM  
      
    # Access at http://localhost:7860  
    
[/code]
## Multi-turn conversations[​](<#multi-turn-conversations> "Direct link to Multi-turn conversations")
[code] 
    # Initialize conversation  
    conv = conv_templates["llava_v1"].copy()  
      
    # Turn 1  
    conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\nWhat is in this image?")  
    conv.append_message(conv.roles[1], None)  
    response1 = generate(conv, model, image)  # "A dog playing in a park"  
      
    # Turn 2  
    conv.messages[-1][1] = response1  # Add previous response  
    conv.append_message(conv.roles[0], "What breed is the dog?")  
    conv.append_message(conv.roles[1], None)  
    response2 = generate(conv, model, image)  # "Golden Retriever"  
      
    # Turn 3  
    conv.messages[-1][1] = response2  
    conv.append_message(conv.roles[0], "What time of day is it?")  
    conv.append_message(conv.roles[1], None)  
    response3 = generate(conv, model, image)  
    
[/code]
## Common tasks[​](<#common-tasks> "Direct link to Common tasks")
### Image captioning[​](<#image-captioning> "Direct link to Image captioning")
[code] 
    question = "Describe this image in detail."  
    response = ask(model, image, question)  
    
[/code]
### Visual question answering[​](<#visual-question-answering> "Direct link to Visual question answering")
[code] 
    question = "How many people are in the image?"  
    response = ask(model, image, question)  
    
[/code]
### Object detection (textual)[​](<#object-detection-textual> "Direct link to Object detection \(textual\)")
[code] 
    question = "List all the objects you can see in this image."  
    response = ask(model, image, question)  
    
[/code]
### Scene understanding[​](<#scene-understanding> "Direct link to Scene understanding")
[code] 
    question = "What is happening in this scene?"  
    response = ask(model, image, question)  
    
[/code]
### Document understanding[​](<#document-understanding> "Direct link to Document understanding")
[code] 
    question = "What is the main topic of this document?"  
    response = ask(model, document_image, question)  
    
[/code]
## Training custom model[​](<#training-custom-model> "Direct link to Training custom model")
[code] 
    # Stage 1: Feature alignment (558K image-caption pairs)  
    bash scripts/v1_5/pretrain.sh  
      
    # Stage 2: Visual instruction tuning (150K instruction data)  
    bash scripts/v1_5/finetune.sh  
    
[/code]
## Quantization (reduce VRAM)[​](<#quantization-reduce-vram> "Direct link to Quantization \(reduce VRAM\)")
[code] 
    # 4-bit quantization  
    tokenizer, model, image_processor, context_len = load_pretrained_model(  
        model_path="liuhaotian/llava-v1.5-13b",  
        model_base=None,  
        model_name=get_model_name_from_path("liuhaotian/llava-v1.5-13b"),  
        load_4bit=True  # Reduces VRAM ~4×  
    )  
      
    # 8-bit quantization  
    load_8bit=True  # Reduces VRAM ~2×  
    
[/code]
## Best practices[​](<#best-practices> "Direct link to Best practices")
  1. **Start with 7B model** \- Good quality, manageable VRAM
  2. **Use 4-bit quantization** \- Reduces VRAM significantly
  3. **GPU required** \- CPU inference extremely slow
  4. **Clear prompts** \- Specific questions get better answers
  5. **Multi-turn conversations** \- Maintain conversation context
  6. **Temperature 0.2-0.7** \- Balance creativity/consistency
  7. **max_new_tokens 512-1024** \- For detailed responses
  8. **Batch processing** \- Process multiple images sequentially


## Performance[​](<#performance> "Direct link to Performance")
Model| VRAM (FP16)| VRAM (4-bit)| Speed (tokens/s)  
---|---|---|---  
7B| ~14 GB| ~4 GB| ~20  
13B| ~28 GB| ~8 GB| ~12  
34B| ~70 GB| ~18 GB| ~5  
_On A100 GPU_
## Benchmarks[​](<#benchmarks> "Direct link to Benchmarks")
LLaVA achieves competitive scores on:
  * **VQAv2** : 78.5%
  * **GQA** : 62.0%
  * **MM-Vet** : 35.4%
  * **MMBench** : 64.3%


## Limitations[​](<#limitations> "Direct link to Limitations")
  1. **Hallucinations** \- May describe things not in image
  2. **Spatial reasoning** \- Struggles with precise locations
  3. **Small text** \- Difficulty reading fine print
  4. **Object counting** \- Imprecise for many objects
  5. **VRAM requirements** \- Need powerful GPU
  6. **Inference speed** \- Slower than CLIP


## Integration with frameworks[​](<#integration-with-frameworks> "Direct link to Integration with frameworks")
### LangChain[​](<#langchain> "Direct link to LangChain")
[code] 
    from langchain.llms.base import LLM  
      
    class LLaVALLM(LLM):  
        def _call(self, prompt, stop=None):  
            # Custom LLaVA inference  
            return response  
      
    llm = LLaVALLM()  
    
[/code]
### Gradio App[​](<#gradio-app> "Direct link to Gradio App")
[code] 
    import gradio as gr  
      
    def chat(image, text, history):  
        response = ask_llava(model, image, text)  
        return response  
      
    demo = gr.ChatInterface(  
        chat,  
        additional_inputs=[gr.Image(type="pil")],  
        title="LLaVA Chat"  
    )  
    demo.launch()  
    
[/code]
## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/haotian-liu/LLaVA> ⭐ 23,000+
  * **Paper** : <https://arxiv.org/abs/2304.08485>
  * **Demo** : <https://llava.hliu.cc>
  * **Models** : <https://huggingface.co/liuhaotian>
  * **License** : Apache 2.0


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use LLaVA](<#when-to-use-llava>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Basic usage](<#basic-usage>)
  * [Available models](<#available-models>)
  * [CLI usage](<#cli-usage>)
  * [Web UI (Gradio)](<#web-ui-gradio>)
  * [Multi-turn conversations](<#multi-turn-conversations>)
  * [Common tasks](<#common-tasks>)
    * [Image captioning](<#image-captioning>)
    * [Visual question answering](<#visual-question-answering>)
    * [Object detection (textual)](<#object-detection-textual>)
    * [Scene understanding](<#scene-understanding>)
    * [Document understanding](<#document-understanding>)
  * [Training custom model](<#training-custom-model>)
  * [Quantization (reduce VRAM)](<#quantization-reduce-vram>)
  * [Best practices](<#best-practices>)
  * [Performance](<#performance>)
  * [Benchmarks](<#benchmarks>)
  * [Limitations](<#limitations>)
  * [Integration with frameworks](<#integration-with-frameworks>)
    * [LangChain](<#langchain>)
    * [Gradio App](<#gradio-app>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-llava -->
